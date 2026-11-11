#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["Pillow", "markdown-it-py", "pydantic>=2", "typer"]
# ///
# ─── How to run ───
# Use an environment with the declared packages and installed Chrome + pdfinfo.
# python3 render_storyboard_document.py board.md --base-dir PROJECT --output board.pdf
# uv run requires dependency installation approval if its cache is incomplete.
# ──────────────────
"""Render image-free Markdown or ordered PNG sheets as searchable A4 PDF."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Annotated

import typer

from storyboard_document import check_document_output, render_document
from storyboard_document_inputs import markdown_body, sheets_body
from storyboard_pdf import PDFExportError, pdf_output_path


def main(
    base_dir: Annotated[Path, typer.Option(help="Existing project root")],
    output: Annotated[str, typer.Option(help="New project-relative PDF path")],
    source: Annotated[Path | None, typer.Argument(help="Markdown plan; omit when using --sheet")] = None,
    sheet: Annotated[list[Path] | None, typer.Option(help="PNG sheet in canonical order; repeat for every sheet")] = None,
    title: Annotated[str, typer.Option()] = "스토리보드 검토본",
    version: Annotated[str, typer.Option()] = "미지정 (원본 참조)",
    panels_per_page: Annotated[int, typer.Option(help="Image cards per page: 1 (detail), 2 (default), 4 (brief)")] = 2,
) -> None:
    """Make PDF + editable self-contained HTML without image generation."""
    try:
        if (source is None) == (not sheet):
            raise PDFExportError("Supply either one Markdown source or ordered --sheet inputs, not both")
        destination = pdf_output_path(base_dir, output)
        check_document_output(destination)
        inputs = [source] if source is not None else list(sheet or [])
        # Snapshot source hashes before rendering; detect edits during the run.
        hashes = [hashlib.sha256(path.read_bytes()).hexdigest() for path in inputs]
        body = markdown_body(source.read_text(encoding="utf-8")) if source is not None else sheets_body(inputs, panels_per_page=panels_per_page)
        if hashes != [hashlib.sha256(path.read_bytes()).hexdigest() for path in inputs]:
            raise PDFExportError("Input changed while preparing the document")
        mode = "텍스트 계획본 / 이미지 없음" if source is not None else "이미지 보드 / 패널별 상세"
        result = render_document(body, destination, title=title, version=version, mode=mode)
    except (OSError, ValueError, RuntimeError) as exc:
        typer.echo(json.dumps({"ok": False, "errors": [str(exc)]}, ensure_ascii=False))
        raise typer.Exit(2) from exc
    typer.echo(json.dumps({
        "ok": True, "path": str(result.path), "html_path": str(result.html_path),
        "page_count": result.page_count, "format": "A4 landscape" if source is None and panels_per_page > 1 else "A4 portrait", "style": "document",
        "sha256": hashlib.sha256(result.path.read_bytes()).hexdigest(),
        "html_sha256": hashlib.sha256(result.html_path.read_bytes()).hexdigest(),
        "sources": [{"path": str(path.resolve()), "sha256": digest}
                    for path, digest in zip(inputs, hashes, strict=True)],
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    typer.run(main)
