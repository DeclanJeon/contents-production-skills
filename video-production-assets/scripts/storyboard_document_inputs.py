"""Safe document bodies from canonical PNG metadata or image-free Markdown."""
from __future__ import annotations

import base64
import io
from html import escape
from pathlib import Path

from markdown_it import MarkdownIt
from markdown_it.token import Token
from PIL import Image
from pydantic import BaseModel, ConfigDict, TypeAdapter, ValidationError

from storyboard_pdf import PDFExportError


class Caption(BaseModel):
    model_config = ConfigDict(frozen=True, strict=True)
    panel_id: str
    scene_id: str
    shot_id: str
    caption: list[str]


class Bounds(BaseModel):
    model_config = ConfigDict(frozen=True, strict=True)
    panel_id: str
    bounds: list[int]


def sheets_body(paths: list[Path], *, panels_per_page: int = 2) -> str:
    """Decode clean panel crops, keeping metadata captions as real text."""
    if panels_per_page not in (1, 2, 4):
        raise PDFExportError("panels_per_page must be 1, 2 or 4")
    if not paths:
        raise PDFExportError("Document PDF requires at least one sheet")
    sections: list[str] = []
    seen: set[str] = set()
    for index, path in enumerate(paths, 1):
        with Image.open(path) as source:
            if source.info.get("storyboard_sheet.sheet_index") != str(index) or \
                    source.info.get("storyboard_sheet.sheet_count") != str(len(paths)):
                raise PDFExportError(f"incomplete or out-of-order storyboard sheets: {path}")
            try:
                captions = TypeAdapter(list[Caption]).validate_json(source.info.get("storyboard_sheet.panel_traceability", "null"))
                bounds = TypeAdapter(list[Bounds]).validate_json(source.info.get("storyboard_sheet.panel_bounds", "null"))
                ids = source.info.get("storyboard_sheet.panel_ids", "").split(",")
            except (ValidationError, TypeError) as exc:
                raise PDFExportError(f"missing or invalid panel metadata: {path}") from exc
            if not captions or ids != [c.panel_id for c in captions] or ids != [b.panel_id for b in bounds]:
                raise PDFExportError(f"panel order/bounds mismatch: {path}")
            for caption, box in zip(captions, bounds, strict=True):
                if caption.panel_id.casefold() in seen:
                    raise PDFExportError(f"duplicate panel ID: {caption.panel_id}")
                seen.add(caption.panel_id.casefold())
                if len(box.bounds) != 4:
                    raise PDFExportError(f"invalid crop: {caption.panel_id}")
                left, top, right, bottom = box.bounds
                if not (0 <= left < right <= source.width and 0 <= top < bottom <= source.height):
                    raise PDFExportError(f"crop outside sheet: {caption.panel_id}")
                with source.crop((left, top, right, bottom)) as crop, io.BytesIO() as buffer:
                    crop.save(buffer, format="PNG")
                    encoded = base64.b64encode(buffer.getvalue()).decode("ascii")
                lines = '<div class="caption">' + escape('\n'.join(caption.caption)) + '</div>'
                sections.append(f'<article class="panel"><h2>{escape(caption.panel_id)}</h2>'
                                f'<p class="identity">{escape(caption.scene_id)} / {escape(caption.shot_id)} · 원본 시트 {index}</p>'
                                f'<img alt="{escape(caption.panel_id)}" src="data:image/png;base64,{encoded}">'
                                f'{lines}</article>')
    if panels_per_page == 1:
        return "".join(sections)
    return ''.join(f'<section class="spread density-{panels_per_page}">' +
                   ''.join(sections[i:i + panels_per_page]) + '</section>'
                   for i in range(0, len(sections), panels_per_page))


def _table_cards(tokens: list[Token], md: MarkdownIt) -> str:
    """Reflow wide Markdown table rows into readable label/value records."""
    headers: list[str] = []
    rows: list[list[str]] = []
    current: list[str] = []
    in_header = False
    for token in tokens:
        if token.type == "thead_open":
            in_header = True
        if token.type == "thead_close":
            in_header = False
        if token.type == "tr_open":
            current = []
        if token.type == "inline":
            current.append(token.content)
        if token.type == "tr_close":
            if in_header:
                headers = current
            else:
                rows.append(current)
    cards: list[str] = []
    for row in rows:
        fields = "".join(f'<p class="field-label">{escape(label)}</p>'
                         f'<div class="field-value">{md.renderInline(value)}</div>'
                         for label, value in zip(headers, row, strict=True))
        cards.append(f'<section class="record">{fields}</section>')
    return "".join(cards)


def markdown_body(source: str) -> str:
    """Keep all text, disable raw HTML/images and reflow supported pipe tables.

    Markdown image references remain text/links; no remote or local image is
    fetched. This route is explicitly a plan document, not an image board.
    """
    if not source.strip():
        raise PDFExportError("Markdown storyboard is empty")
    md = MarkdownIt("commonmark", {"html": False, "breaks": True}).enable("table").disable("image")
    tokens = md.parse(source)
    output: list[str] = []
    cursor = 0
    while cursor < len(tokens):
        if tokens[cursor].type == "table_open":
            end = next(i for i in range(cursor + 1, len(tokens)) if tokens[i].type == "table_close")
            output.append(_table_cards(tokens[cursor:end + 1], md))
            cursor = end + 1
        else:
            end = cursor + 1
            while end < len(tokens) and tokens[end].type != "table_open":
                end += 1
            output.append(md.renderer.render(tokens[cursor:end], md.options, {}))
            cursor = end
    return '<p class="placeholder">텍스트 계획본 · 이미지 생성/검수 없음</p>' + "".join(output)
