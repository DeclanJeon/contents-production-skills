"""Sharing PDF derived from ordered PNG sheets; PNG metadata stays authoritative."""
from __future__ import annotations

import os
import tempfile
from contextlib import ExitStack
from dataclasses import dataclass
from pathlib import Path
from typing import Final

from PIL import Image

PDF_DPI: Final = 144.0


@dataclass(frozen=True, slots=True)
class PDFExportError(ValueError):
    reason: str

    def __str__(self) -> str:
        return self.reason


def pdf_output_path(base_dir: str | Path, output: str) -> Path:
    """Resolve a new project-relative PDF destination before rendering sheets."""
    base = Path(base_dir).resolve(strict=True)
    relative = Path(output)
    if not output.strip() or relative.is_absolute() or ":" in output:
        raise PDFExportError("PDF output must be a project-relative path")
    if os.path.lexists(base / relative):
        raise PDFExportError(f"PDF output already exists; refusing to overwrite: {base / relative}")
    destination = (base / relative).resolve()
    if base not in destination.parents or destination.suffix.lower() != ".pdf":
        raise PDFExportError("PDF output must be a .pdf file inside --base-dir")
    if destination.exists():
        raise PDFExportError(f"PDF output already exists; refusing to overwrite: {destination}")
    return destination


def export_storyboard_pdf(sheet_paths: list[Path], output: Path) -> None:
    """Write one uncropped page per PNG in verified sheet order, without overwrite.

    Native sheet aspect ratios and pixels are retained at 144 dpi, rather than
    forcing differently sized sheets onto A4. This is a raster review copy,
    not searchable text or an extraction source. A failed PDF leaves PNGs intact.
    """
    if not sheet_paths:
        raise PDFExportError("PDF requires at least one rendered sheet")
    if output.exists():
        raise PDFExportError(f"PDF output already exists; refusing to overwrite: {output}")
    with ExitStack() as resources:
        pages: list[Image.Image] = []
        for index, path in enumerate(sheet_paths, 1):
            source = resources.enter_context(Image.open(path))
            if source.info.get("storyboard_sheet.sheet_index") != str(index) or \
                    source.info.get("storyboard_sheet.sheet_count") != str(len(sheet_paths)):
                raise PDFExportError(f"incomplete or out-of-order storyboard sheets: {path}")
            page = source.convert("RGB")
            resources.callback(page.close)
            pages.append(page)
        output.parent.mkdir(parents=True, exist_ok=True)
        descriptor, name = tempfile.mkstemp(dir=output.parent, prefix=".board-", suffix=".pdf")
        temporary = Path(name)
        try:
            with os.fdopen(descriptor, "w+b") as stream:
                pages[0].save(stream, format="PDF", save_all=True,
                              append_images=pages[1:], resolution=PDF_DPI,
                              title=output.stem)
                stream.flush()
                os.fsync(stream.fileno())
            os.link(temporary, output)
        finally:
            temporary.unlink(missing_ok=True)
