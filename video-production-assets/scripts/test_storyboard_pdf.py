"""PDF page order, safe writes and real renderer CLI integration."""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
from PIL import Image, PngImagePlugin

from storyboard_pdf import PDFExportError, export_storyboard_pdf, pdf_output_path
from test_validate_preproduction import image_package


def sheets(root: Path) -> list[Path]:
    paths: list[Path] = []
    for index, color in enumerate(("red", "blue"), 1):
        path = root / f"s{index}.png"
        metadata = PngImagePlugin.PngInfo()
        metadata.add_text("storyboard_sheet.sheet_index", str(index))
        metadata.add_text("storyboard_sheet.sheet_count", "2")
        with Image.new("RGB", (200, 100), color) as page:
            page.save(path, pnginfo=metadata)
        paths.append(path)
    return paths


def test_pdf_pages_and_no_overwrite(tmp_path: Path) -> None:
    output = tmp_path / "board.pdf"
    export_storyboard_pdf(sheets(tmp_path), output)
    original = output.read_bytes()
    assert original.startswith(b"%PDF-")
    assert b"/Count 2" in original
    with pytest.raises(PDFExportError, match="overwrite"):
        export_storyboard_pdf(sheets(tmp_path), output)
    assert output.read_bytes() == original
    assert not list(tmp_path.glob(".board-*"))


def test_order_and_missing_pages_rejected(tmp_path: Path) -> None:
    paths = sheets(tmp_path)
    for invalid in (paths[::-1], paths[:1], []):
        with pytest.raises(PDFExportError):
            export_storyboard_pdf(invalid, tmp_path / "bad.pdf")
        assert not (tmp_path / "bad.pdf").exists()


@pytest.mark.parametrize("relative", ["../escape.pdf", "/tmp/escape.pdf", "board.png", ""])
def test_output_confinement(tmp_path: Path, relative: str) -> None:
    with pytest.raises(PDFExportError):
        pdf_output_path(tmp_path, relative)


def test_symlink_output_escape(tmp_path: Path) -> None:
    (tmp_path / "outside").symlink_to(tmp_path.parent, target_is_directory=True)
    with pytest.raises(PDFExportError):
        pdf_output_path(tmp_path, "outside/escape.pdf")


def test_dangling_pdf_symlink_is_not_followed(tmp_path: Path) -> None:
    destination = tmp_path / 'board.pdf'
    destination.symlink_to(tmp_path / 'unwritten.pdf')
    with pytest.raises(PDFExportError, match='overwrite'):
        pdf_output_path(tmp_path, 'board.pdf')
    assert destination.is_symlink()
    assert not (tmp_path / 'unwritten.pdf').exists()


def test_real_renderer_cli_and_pdf_pixels(tmp_path: Path) -> None:
    project = tmp_path / "project.json"
    package = image_package(str(tmp_path))
    package['shots'][0]['speech'][0]['text'] = '안녕, 스토리보드 PDF 한글 확인'
    project.write_text(json.dumps(package, ensure_ascii=False), encoding="utf-8")
    command = [sys.executable, str(Path(__file__).with_name("render_storyboard_sheet.py")),
               str(project), "--base-dir", str(tmp_path), "--output", "sheets/board.png",
               "--panels-per-sheet", "4", "--pdf-output", "board.pdf", "--pdf-style", "sheets"]
    result = subprocess.run(command, capture_output=True, text=True, check=False)
    assert result.returncode == 0, result.stdout + result.stderr
    data = json.loads(result.stdout)
    assert data["pdf"]["page_count"] == len(data["sheets"]) == 2
    assert data["pdf"]["source_sheet_sha256"] == [s["sha256"] for s in data["sheets"]]
    # Existing PDF must be rejected before new PNG files are created.
    command[command.index("sheets/board.png")] = "should-not-exist.png"
    repeated = subprocess.run(command, capture_output=True, text=True, check=False)
    assert repeated.returncode == 2
    assert not list(tmp_path.glob("should-not-exist*"))
    if not shutil.which("pdftoppm"):
        pytest.skip("Poppler not installed; PDF render-back unavailable")
    subprocess.run(["pdftoppm", "-scale-to", "800", "-png", str(tmp_path / "board.pdf"),
                    str(tmp_path / "pdf-page")], capture_output=True, check=True)
    pages = sorted(tmp_path.glob("pdf-page-*.png"))
    assert len(pages) == 2
    for page_path in pages:
        with Image.open(page_path) as page:
            assert page.width > 0 and page.height > 0
