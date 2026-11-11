"""Print safe, self-contained HTML as searchable A4 PDF using installed Chrome."""
from __future__ import annotations

import os
import re
import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from html import escape
from pathlib import Path

from storyboard_pdf import PDFExportError


@dataclass(frozen=True, slots=True)
class DocumentResult:
    path: Path
    html_path: Path
    page_count: int


def document_tools() -> tuple[str, str]:
    """Preflight installed tools; never download a browser or PDF dependency."""
    chrome = next((found for name in ("google-chrome", "chromium", "chromium-browser")
                   if (found := shutil.which(name))), None)
    pdfinfo = shutil.which("pdfinfo")
    if chrome is None or pdfinfo is None:
        raise PDFExportError("Document PDF requires installed Chrome/Chromium and Poppler pdfinfo; no automatic installation")
    return chrome, pdfinfo


def check_document_output(output: Path) -> Path:
    """Reserve neither file, but reject collisions before rendering any output."""
    html_path = output.parent / '_internal' / output.with_suffix('.html').name
    if html_path.parent.resolve() != output.parent.resolve() / '_internal':
        raise PDFExportError('internal HTML folder must not redirect outside the output folder')
    for path in (output, html_path):
        if os.path.lexists(path):
            raise PDFExportError(f"output already exists; refusing to overwrite: {path}")
    document_tools()
    return html_path


def render_document(body: str, output: Path, *, title: str, version: str,
                    mode: str) -> DocumentResult:
    """Render generated safe body HTML; atomically publish new PDF and HTML.

    Browser work uses a throwaway profile and local data URLs only. Output
    paths must already be confined by pdf_output_path at the CLI boundary.
    """
    html_path = check_document_output(output)
    chrome, pdfinfo = document_tools()
    css = (Path(__file__).parent.parent / "assets" / "storyboard-document.css").read_text(encoding="utf-8")
    markup = f'''<!doctype html><html lang="ko"><head><meta charset="utf-8">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; img-src data:; style-src 'unsafe-inline'">
<title>{escape(title)}</title><style>{css}</style></head><body class="{'compact' if 'class="spread ' in body else 'detail'}">
<section class="cover"><p class="eyebrow">STORYBOARD / PRODUCTION REVIEW</p>
<h1>{escape(title)}</h1><div class="meta"><p>버전: {escape(version)}</p>
<p>형식: {escape(mode)} · A4 · 검색/복사 가능한 텍스트</p></div>
<p class="notice">원본의 이야기·대사·패널 순서를 보존한 검토용 문서입니다.<br>
형식 변환은 제작·사실·권리 검증이나 사용자 승인을 의미하지 않습니다.<br>
이미지 없는 계획은 실제 그림을 검수한 보드가 아닙니다.</p></section>
<main>{body}</main></body></html>'''
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=output.parent, prefix=".board-document-") as scratch:
        work = Path(scratch)
        source = work / "source.html"
        pdf = work / "document.pdf"
        source.write_text(markup, encoding="utf-8")
        command = [chrome, "--headless", "--disable-gpu", "--disable-background-networking",
                   "--disable-extensions", "--no-first-run", "--no-default-browser-check",
                   f"--user-data-dir={work / 'profile'}", "--no-pdf-header-footer",
                   f"--print-to-pdf={pdf}", source.as_uri()]
        try:
            run = subprocess.run(command, capture_output=True, text=True, timeout=90, check=False)
        except subprocess.TimeoutExpired as exc:
            raise PDFExportError("Chrome PDF rendering timed out after 90 seconds") from exc
        if run.returncode or not pdf.is_file() or not pdf.read_bytes().startswith(b"%PDF-"):
            raise PDFExportError(f"Chrome PDF rendering failed: {run.stderr[-1500:]}")
        try:
            info = subprocess.run([pdfinfo, str(pdf)], capture_output=True, text=True,
                                  timeout=15, check=False)
        except subprocess.TimeoutExpired as exc:
            raise PDFExportError("PDF page verification timed out after 15 seconds") from exc
        match = re.search(r"^Pages:\s+(\d+)", info.stdout, re.MULTILINE)
        if info.returncode or match is None or int(match[1]) < 2:
            raise PDFExportError(f"PDF page verification failed: {info.stderr}")
        html_path.parent.mkdir(parents=True, exist_ok=True)
        published_html = False
        try:
            os.link(source, html_path)
            published_html = True
            os.link(pdf, output)
        except OSError:
            if published_html:
                html_path.unlink(missing_ok=True)
            raise
    return DocumentResult(output, html_path, int(match[1]))
