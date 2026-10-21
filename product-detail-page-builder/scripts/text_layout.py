"""Exact-copy wrapping and text-panel composition."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import assert_never

from PIL import Image, ImageDraw, ImageFont

from errors import RenderError
from page_spec import ModuleLayout, PageModule, PageSpec


@dataclass(frozen=True, slots=True)
class TextBox:
    left: int
    top: int
    right: int
    bottom: int


@dataclass(frozen=True, slots=True)
class FittedText:
    font: ImageFont.FreeTypeFont
    lines: tuple[str, ...]
    spacing: int


@dataclass(frozen=True, slots=True)
class TextLayoutRequest:
    draw: ImageDraw.ImageDraw
    text: str
    font: ImageFont.FreeTypeFont
    max_width: int


@dataclass(frozen=True, slots=True)
class TextFitRequest:
    draw: ImageDraw.ImageDraw
    text: str
    box: TextBox
    font_path: Path
    base_size: int


@dataclass(frozen=True, slots=True)
class CopyDrawRequest:
    canvas: Image.Image
    module: PageModule
    spec: PageSpec
    box: TextBox
    font_path: Path


def _wrap_text(request: TextLayoutRequest) -> tuple[str, ...]:
    """Wrap copy by measured glyph width while preserving all source text."""
    lines: list[str] = []
    for paragraph in request.text.splitlines() or [""]:
        current = ""
        for char in paragraph:
            candidate = current + char
            if current and request.draw.textlength(candidate, font=request.font) > request.max_width:
                lines.append(current)
                current = char
            else:
                current = candidate
        lines.append(current)
    return tuple(lines)


def _fit_text(request: TextFitRequest) -> FittedText:
    """Find a font size that fits the entire exact copy in its assigned box."""
    width = request.box.right - request.box.left
    height = request.box.bottom - request.box.top
    for size in range(request.base_size, 15, -2):
        try:
            font = ImageFont.truetype(str(request.font_path), size=size)
        except OSError as exc:
            raise RenderError("configured font cannot be loaded", request.font_path) from exc
        lines = _wrap_text(TextLayoutRequest(request.draw, request.text, font, width))
        spacing = max(4, round(size * 0.22))
        bounds = request.draw.multiline_textbbox(
            (0, 0),
            "\n".join(lines),
            font=font,
            spacing=spacing,
        )
        if bounds[2] - bounds[0] <= width and bounds[3] - bounds[1] <= height:
            return FittedText(font, lines, spacing)
    raise RenderError("copy does not fit the module; shorten the copy or increase its height")


def draw_copy(request: CopyDrawRequest) -> None:
    """Draw exact approved title and body copy in a measured text panel."""
    draw = ImageDraw.Draw(request.canvas)
    box = request.box
    module = request.module
    spec = request.spec
    draw.rectangle(
        (box.left, box.top, box.right, box.bottom),
        fill=spec.style.surface,
    )
    draw.rectangle(
        (box.left, box.top, box.left + 6, box.bottom),
        fill=spec.style.accent,
    )
    inset = spec.style.content_margin_px
    content_box = TextBox(box.left + inset, box.top + inset, box.right - inset, box.bottom - inset)
    match module.layout:
        case ModuleLayout.TEXT_ONLY:
            title_layout = (
                _fit_text(
                    TextFitRequest(
                        draw,
                        module.title,
                        content_box,
                        request.font_path,
                        spec.style.font_size_px,
                    )
                )
                if module.title
                else None
            )
            title_height = 0
            if title_layout is not None:
                title_bounds = draw.multiline_textbbox(
                    (0, 0),
                    "\n".join(title_layout.lines),
                    font=title_layout.font,
                    spacing=title_layout.spacing,
                )
                title_height = title_bounds[3] - title_bounds[1]
            copy_gap = 16 if title_layout is not None and module.copy_text else 0
            copy_box = TextBox(
                content_box.left,
                content_box.top + title_height + copy_gap,
                content_box.right,
                content_box.bottom,
            )
            copy_layout = (
                _fit_text(
                    TextFitRequest(
                        draw,
                        module.copy_text,
                        copy_box,
                        request.font_path,
                        max(18, spec.style.font_size_px - 12),
                    )
                )
                if module.copy_text
                else None
            )
            copy_height = 0
            if copy_layout is not None:
                copy_bounds = draw.multiline_textbbox(
                    (0, 0),
                    "\n".join(copy_layout.lines),
                    font=copy_layout.font,
                    spacing=copy_layout.spacing,
                )
                copy_height = copy_bounds[3] - copy_bounds[1]
            content_height = content_box.bottom - content_box.top
            total_height = title_height + copy_gap + copy_height
            text_top = content_box.top + (content_height - total_height) // 2
            if title_layout is not None:
                draw.multiline_text(
                    (content_box.left, text_top),
                    "\n".join(title_layout.lines),
                    font=title_layout.font,
                    fill=spec.style.text,
                    spacing=title_layout.spacing,
                )
            if copy_layout is not None:
                draw.multiline_text(
                    (content_box.left, text_top + title_height + copy_gap),
                    "\n".join(copy_layout.lines),
                    font=copy_layout.font,
                    fill=spec.style.text,
                    spacing=copy_layout.spacing,
                )
            return
        case ModuleLayout.IMAGE_TOP | ModuleLayout.IMAGE_FULL | ModuleLayout.IMAGE_LEFT | ModuleLayout.IMAGE_RIGHT | ModuleLayout.SPECS:
            pass
        case ModuleLayout.PHOTO_ONLY:
            raise RenderError(f"photo-only module {module.id} cannot draw copy")
        case unreachable:
            assert_never(unreachable)

    text_top = content_box.top
    if module.title:
        title = _fit_text(
            TextFitRequest(
                draw,
                module.title,
                content_box,
                request.font_path,
                spec.style.font_size_px,
            )
        )
        title_text_value = "\n".join(title.lines)
        draw.multiline_text(
            (content_box.left, text_top),
            title_text_value,
            font=title.font,
            fill=spec.style.text,
            spacing=title.spacing,
        )
        title_bounds = draw.multiline_textbbox(
            (content_box.left, text_top),
            title_text_value,
            font=title.font,
            spacing=title.spacing,
        )
        text_top = title_bounds[3] + 16
    if module.copy_text:
        copy_box = TextBox(content_box.left, text_top, content_box.right, content_box.bottom)
        copy = _fit_text(
            TextFitRequest(
                draw,
                module.copy_text,
                copy_box,
                request.font_path,
                max(18, spec.style.font_size_px - 12),
            )
        )
        draw.multiline_text(
            (copy_box.left, copy_box.top),
            "\n".join(copy.lines),
            font=copy.font,
            fill=spec.style.text,
            spacing=copy.spacing,
        )
