"""Pillow-based deterministic product-detail rendering."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Final, assert_never

from PIL import Image, ImageFont, ImageOps

from errors import RenderError
from page_spec import ImageFit, ModuleLayout, OutputFormat, PageModule, PageSpec
from text_layout import CopyDrawRequest, TextBox, draw_copy

FONT_CANDIDATES: Final = (
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
    "/System/Library/Fonts/AppleSDGothicNeo.ttc",
    "C:/Windows/Fonts/malgun.ttf",
    "C:/Windows/Fonts/malgunbd.ttf",
)
MAX_PREVIEW_PIXELS: Final = 60_000_000


@dataclass(frozen=True, slots=True)
class RenderContext:
    spec: PageSpec
    spec_path: Path
    output_dir: Path
    font_path: Path


@dataclass(frozen=True, slots=True)
class ImageRegion:
    left: int
    top: int
    right: int
    bottom: int


@dataclass(frozen=True, slots=True)
class ModuleRegions:
    image: ImageRegion | None
    text: TextBox | None


def find_font(spec: PageSpec) -> Path:
    """Resolve an explicit CJK font or the first installed system candidate."""
    if spec.style.font_path is not None:
        path = Path(spec.style.font_path).expanduser()
        if path.is_file():
            try:
                ImageFont.truetype(str(path), size=16)
            except OSError as exc:
                raise RenderError(f"configured font cannot be loaded: {path}", path) from exc
            return path.resolve()
        raise RenderError(f"configured font does not exist: {path}")
    for candidate in FONT_CANDIDATES:
        path = Path(candidate)
        if path.is_file():
            try:
                ImageFont.truetype(str(path), size=16)
            except OSError:
                continue
            return path
    raise RenderError("no Korean-capable font found; set style.font_path")


def _regions(module: PageModule, width: int) -> ModuleRegions:
    """Choose non-overlapping image and text areas for a module layout."""
    height = module.height_px
    match module.layout:
        case ModuleLayout.TEXT_ONLY:
            return ModuleRegions(None, TextBox(0, 0, width, height))
        case ModuleLayout.IMAGE_TOP:
            image_bottom = round(height * 0.58)
            return ModuleRegions(
                ImageRegion(0, 0, width, image_bottom),
                TextBox(48, image_bottom + 24, width - 48, height - 24),
            )
        case ModuleLayout.IMAGE_LEFT:
            image_right = round(width * 0.52)
            return ModuleRegions(
                ImageRegion(0, 0, image_right, height),
                TextBox(image_right + 32, 32, width - 32, height - 32),
            )
        case ModuleLayout.IMAGE_RIGHT:
            image_left = round(width * 0.48)
            return ModuleRegions(
                ImageRegion(image_left, 0, width, height),
                TextBox(32, 32, image_left - 32, height - 32),
            )
        case ModuleLayout.IMAGE_FULL:
            return ModuleRegions(
                ImageRegion(0, 0, width, height),
                TextBox(48, round(height * 0.62), width - 48, height - 32),
            )
        case ModuleLayout.SPECS:
            image_bottom = round(height * 0.42)
            return ModuleRegions(
                ImageRegion(0, 0, width, image_bottom),
                TextBox(48, image_bottom + 24, width - 48, height - 24),
            )
        case ModuleLayout.PHOTO_ONLY:
            return ModuleRegions(ImageRegion(0, 0, width, height), None)
        case unreachable:
            assert_never(unreachable)


def _resolve_background(module: PageModule, context: RenderContext) -> Path:
    """Resolve and require the actual selected module background."""
    background_image = module.background_image
    if background_image is None:
        raise RenderError(f"module {module.id} requires a background image")
    path = Path(background_image).expanduser()
    resolved = path if path.is_absolute() else context.spec_path.parent / path
    if not resolved.is_file():
        raise RenderError(f"module {module.id} background image is missing: {resolved}")
    return resolved.resolve()


def _load_background(path: Path, size: tuple[int, int], image_fit: ImageFit) -> Image.Image:
    """Fit an image without cropping unless the page spec explicitly requests it."""
    try:
        with Image.open(path) as source:
            source.load()
            match image_fit:
                case ImageFit.CONTAIN:
                    return ImageOps.contain(
                        source.convert("RGB"),
                        size,
                        method=Image.Resampling.LANCZOS,
                    )
                case ImageFit.COVER:
                    return ImageOps.fit(
                        source.convert("RGB"),
                        size,
                        method=Image.Resampling.LANCZOS,
                    )
                case unreachable:
                    assert_never(unreachable)
    except OSError as exc:
        raise RenderError("background image cannot be decoded", path) from exc


def render_module(module: PageModule, context: RenderContext) -> Path:
    """Render one page module to a deterministic raster image."""
    width = context.spec.output.width_px
    height = module.height_px
    canvas = Image.new("RGB", (width, height), context.spec.style.background)
    regions = _regions(module, width)
    image_box = regions.image
    if image_box is not None:
        background_path = _resolve_background(module, context)
        image_size = (image_box.right - image_box.left, image_box.bottom - image_box.top)
        image = _load_background(background_path, image_size, module.image_fit)
        x = image_box.left + (image_size[0] - image.width) // 2
        y = image_box.top + (image_size[1] - image.height) // 2
        canvas.paste(image, (x, y))
    if regions.text is not None:
        draw_copy(
            CopyDrawRequest(canvas, module, context.spec, regions.text, context.font_path)
        )

    context.output_dir.mkdir(parents=True, exist_ok=True)
    output = context.output_dir / f"{module.id}.{context.spec.output.format.value}"
    save_options: dict[str, int | str | bool] = {}
    match context.spec.output.format:
        case OutputFormat.JPG:
            save_options = {"format": "JPEG", "quality": context.spec.output.quality, "optimize": True}
        case OutputFormat.PNG:
            save_options = {"format": "PNG", "optimize": True}
        case unreachable:
            assert_never(unreachable)
    canvas.save(output, **save_options)
    return output


def render_preview(module_paths: tuple[Path, ...], output: Path, width: int) -> int:
    """Join ordered module images into one preview without changing their pixels."""
    sizes: list[tuple[int, int]] = []
    for path in module_paths:
        with Image.open(path) as image:
            sizes.append(image.size)
    total_height = sum(height for _, height in sizes)
    if total_height * width > MAX_PREVIEW_PIXELS:
        raise RenderError(
            f"preview would exceed {MAX_PREVIEW_PIXELS} pixels; reduce module heights"
        )
    preview = Image.new("RGB", (width, total_height), "#FFFFFF")
    y = 0
    for path, (image_width, image_height) in zip(module_paths, sizes, strict=True):
        with Image.open(path) as image:
            if image_width != width:
                raise RenderError(f"module width does not match preview width: {path}")
            preview.paste(image.convert("RGB"), (0, y))
        y += image_height
    output.parent.mkdir(parents=True, exist_ok=True)
    preview.save(output, format="JPEG", quality=90, optimize=True)
    return total_height
