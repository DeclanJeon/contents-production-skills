"""Real CLI/document rendering: text preservation, pagination and safe outputs."""
from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from unittest.mock import patch

import pytest
from PIL import Image, PngImagePlugin

from storyboard_document import check_document_output, document_tools
from storyboard_document_inputs import markdown_body, sheets_body
from storyboard_pdf import PDFExportError
from test_validate_preproduction import image_package


def require_tools() -> None:
    try:
        document_tools()
    except PDFExportError as exc:
        pytest.skip(str(exc))
    if not shutil.which("pdftotext"):
        pytest.skip("Poppler pdftotext required for extraction QA")


def extract(path: Path) -> str:
    return subprocess.run(["pdftotext", "-layout", str(path), "-"],
                          capture_output=True, text=True, check=True).stdout


def test_markdown_content_cannot_execute_html_or_embed_images() -> None:
    # Given untrusted plain Markdown, including active HTML and remote images.
    source = '<script>window.bad=1</script>\n\n![그림](https://example.invalid/a.png)'
    # When preparing the plan body.
    body = markdown_body(source)
    # Then neither script nor image tags are emitted.
    assert '<script>' not in body and '<img' not in body
    assert 'window.bad=1' in body and '그림' in body


def test_document_collision_and_missing_tools_write_nothing(tmp_path: Path) -> None:
    # Given a document renderer without installed tools.
    with patch("storyboard_document.shutil.which", return_value=None):
        # When preflighting the destination.
        with pytest.raises(PDFExportError, match="requires installed"):
            check_document_output(tmp_path / 'board.pdf')
    # Then no output is created.
    assert list(tmp_path.iterdir()) == []


def test_html_collision_rejects_pdf_before_render(tmp_path: Path) -> None:
    # Given an existing editable source.
    (tmp_path / '_internal').mkdir()
    (tmp_path / '_internal/board.html').write_text('keep', encoding='utf-8')
    # When preflighting its matching PDF.
    with pytest.raises(PDFExportError, match="overwrite"):
        check_document_output(tmp_path / 'board.pdf')
    # Then both the original and absence of PDF are preserved.
    assert (tmp_path / '_internal/board.html').read_text() == 'keep'
    assert not (tmp_path / 'board.pdf').exists()


def test_long_korean_table_survives_real_text_cli(tmp_path: Path) -> None:
    require_tools()
    # Given eight columns, three scenes and a multi-page Korean dialogue.
    dialogue = '\n'.join(f'대사{i:03d} 천천히 말해요. 마지막까지 빠짐없이 기록합니다.' for i in range(100))
    source = tmp_path / 'plan.md'
    source.write_text('# 긴 대사 검토\n\n|씬|샷|패널|카메라|동작|발화|음향|상태|\n'
                      '|---|---|---|---|---|---|---|---|\n'
                      '|SC01|SH01|P01|고정|기다림|첫번째발화|침묵|미검증|\n'
                      '|SC02|SH02|P02|이동|발견|두번째발화|환경음|계획|\n'
                      '|SC03|SH03|P03|유지|선택|세번째발화|없음|제안|\n\n'
                      + dialogue + '\n\n최종내용보존표식', encoding='utf-8')
    command = [sys.executable, str(Path(__file__).with_name('render_storyboard_document.py')),
               str(source), '--base-dir', str(tmp_path), '--output', 'board.pdf',
               '--title', '긴 한글 콘티', '--version', 'v007']
    # When driving the actual public CLI.
    run = subprocess.run(command, capture_output=True, text=True, check=False)
    assert run.returncode == 0, run.stdout + run.stderr
    result = json.loads(run.stdout)
    # Then every dialogue, scene and final marker is extractable in order.
    extracted = ''.join(extract(tmp_path / 'board.pdf').split())
    expected = [''.join(f'대사{i:03d} 천천히 말해요. 마지막까지 빠짐없이 기록합니다.'.split()) for i in range(100)]
    assert all(marker in extracted for marker in expected)
    assert [extracted.index(marker) for marker in expected] == sorted(extracted.index(marker) for marker in expected)
    assert all(marker in extracted for marker in ('SC01', 'SC02', 'SC03', '최종내용보존표식', 'v007'))
    assert result['page_count'] >= 4
    assert result['sources'][0]['sha256'] == hashlib.sha256(source.read_bytes()).hexdigest()
    # Verify every page's physical geometry and every word's bounding box.
    bbox = subprocess.run(['pdftotext', '-bbox', str(tmp_path / 'board.pdf'), '-'],
                          capture_output=True, text=True, check=True).stdout
    root = ET.fromstring(bbox)
    pages = root.findall('.//{*}page')
    assert len(pages) == result['page_count']
    for page in pages:
        width, height = float(page.attrib['width']), float(page.attrib['height'])
        assert 594 <= width <= 596 and 841 <= height <= 843
        for word in page.findall('.//{*}word'):
            assert 0 <= float(word.attrib['xMin']) < float(word.attrib['xMax']) <= width
            assert 0 <= float(word.attrib['yMin']) < float(word.attrib['yMax']) <= height


def test_default_sheet_cli_pdf_has_searchable_korean(tmp_path: Path) -> None:
    require_tools()
    # Given the canonical image-backed fixture with Korean speech.
    package = image_package(str(tmp_path))
    package['shots'][0]['speech'][0]['text'] = '검색되는한글대사'
    source = tmp_path / 'project.json'
    source.write_text(json.dumps(package, ensure_ascii=False), encoding='utf-8')
    command = [sys.executable, str(Path(__file__).with_name('render_storyboard_sheet.py')),
               str(source), '--base-dir', str(tmp_path), '--output', 'sheets/board.png',
               '--pdf-output', 'board.pdf']
    # When using the default PDF style (no document-style override).
    run = subprocess.run(command, capture_output=True, text=True, check=False)
    assert run.returncode == 0, run.stdout + run.stderr
    result = json.loads(run.stdout)
    # Then five cards share three body pages; only the PDF is top-level.
    assert result['pdf']['style'] == 'document'
    assert result['pdf']['page_count'] == 4
    assert '검색되는한글대사' in ''.join(extract(tmp_path / 'board.pdf').split())
    assert Path(result['pdf']['html_path']).is_file()
    assert Path(result['pdf']['html_path']).parent == tmp_path / '_internal'
    pages = extract(tmp_path / 'board.pdf').split('\f')
    assert 'P01' in pages[1] and 'P02' in pages[1]
    assert 'P03' in pages[2] and 'P04' in pages[2]


def test_sheet_metadata_mismatch_is_not_silently_dropped(tmp_path: Path) -> None:
    # Given readable pixels but no traceability/crop metadata.
    path = tmp_path / 'sheet.png'
    meta = PngImagePlugin.PngInfo()
    meta.add_text('storyboard_sheet.sheet_index', '1')
    meta.add_text('storyboard_sheet.sheet_count', '1')
    with Image.new('RGB', (80, 240), 'blue') as image:
        image.save(path, pnginfo=meta)
    # When preparing a document body.
    with pytest.raises(PDFExportError, match='metadata'):
        sheets_body([path])
    # Then no guess-based extraction/output occurs.
    assert sorted(p.name for p in tmp_path.iterdir()) == ['sheet.png']
