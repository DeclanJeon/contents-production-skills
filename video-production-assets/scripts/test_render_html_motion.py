"""Tests for render_html_motion.mjs (skipped when Chrome, node or ffmpeg is missing)."""
from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parent / "render_html_motion.mjs"
CHROME = shutil.which("google-chrome") or shutil.which("chromium") or shutil.which("chromium-browser")
pytestmark = pytest.mark.skipif(not (CHROME and shutil.which("node") and shutil.which("ffmpeg")),
                                reason="needs node, ffmpeg and Chrome")

PIECE = """<!doctype html><html><body style="margin:0;background:#111">
<div id="box" style="position:absolute;width:40px;height:40px;background:#f60"></div>
<script>
window.__motion = {width: 160, height: 90, fps: 12, duration: 0.5,
  seek(t) { document.getElementById('box').style.left = (t * 200) + 'px'; }};
</script></body></html>"""


def render(tmp: Path, html: str, *extra: str) -> subprocess.CompletedProcess[str]:
    (tmp / "index.html").write_text(html, encoding="utf-8")
    return subprocess.run(["node", str(SCRIPT), str(tmp / "index.html"), str(tmp / "out.mp4"), *extra],
                          capture_output=True, text=True, timeout=180)


def probe(path: Path) -> dict:
    out = subprocess.run(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0", "-show_entries",
                          "stream=width,height,nb_read_frames,r_frame_rate,pix_fmt", "-of", "json", str(path)],
                         capture_output=True, text=True, check=True).stdout
    return json.loads(out)["streams"][0]


def test_renders_frames_report_and_contact_sheet(tmp_path: Path) -> None:
    result = render(tmp_path, PIECE, "--verify-frames", "3", "--contact-sheet", "4")
    assert result.returncode == 0, result.stderr
    stream = probe(tmp_path / "out.mp4")
    assert (stream["width"], stream["height"]) == (160, 90)
    assert int(stream["nb_read_frames"]) == 6
    assert stream["r_frame_rate"] == "12/1" and stream["pix_fmt"] == "yuv420p"
    report = json.loads((tmp_path / "out.render-report.json").read_text(encoding="utf-8"))
    for key in ("input_sha256", "output_sha256", "frames", "fps", "width", "height", "chrome", "ffmpeg",
                "determinism", "seconds"):
        assert key in report, key
    assert report["determinism"] == {"checked": 3, "pass": True}
    assert (tmp_path / "out.contact.png").is_file()


def test_rejects_nondeterministic_piece(tmp_path: Path) -> None:
    html = PIECE.replace("(t * 200)", "(Math.random() * 100)")
    result = render(tmp_path, html, "--verify-frames", "3")
    assert result.returncode != 0
    assert "nondeterministic" in result.stderr
    assert not (tmp_path / "out.mp4").exists()


def test_rejects_network_requests(tmp_path: Path) -> None:
    html = PIECE.replace("<body", '<body><img src="https://example.com/x.png"', 1)
    result = render(tmp_path, html)
    assert result.returncode != 0
    assert "network" in result.stderr


def test_rejects_missing_contract(tmp_path: Path) -> None:
    result = render(tmp_path, "<html><body>no contract</body></html>")
    assert result.returncode != 0
    assert "__motion" in result.stderr


def test_audio_length_must_match(tmp_path: Path) -> None:
    subprocess.run(["ffmpeg", "-v", "error", "-f", "lavfi", "-i", "sine=frequency=440:duration=2",
                    str(tmp_path / "tone.wav")], check=True)
    result = render(tmp_path, PIECE, "--audio", str(tmp_path / "tone.wav"))
    assert result.returncode != 0
    assert "audio duration" in result.stderr
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "sine=frequency=440:duration=0.5",
                    str(tmp_path / "tone.wav")], check=True)
    result = render(tmp_path, PIECE, "--audio", str(tmp_path / "tone.wav"))
    assert result.returncode == 0, result.stderr
    streams = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=codec_type", "-of", "csv=p=0",
                              str(tmp_path / "out.mp4")], capture_output=True, text=True, check=True).stdout.split()
    assert sorted(streams) == ["audio", "video"]


def test_frame_range_rerender(tmp_path: Path) -> None:
    result = render(tmp_path, PIECE, "--frames", "2:4")
    assert result.returncode == 0, result.stderr
    assert int(probe(tmp_path / "out.mp4")["nb_read_frames"]) == 2


def test_output_on_another_filesystem(tmp_path: Path) -> None:
    import tempfile

    (tmp_path / "index.html").write_text(PIECE, encoding="utf-8")
    with tempfile.TemporaryDirectory(dir=Path(__file__).parent) as other:
        out = Path(other) / "out.mp4"
        result = subprocess.run(["node", str(SCRIPT), str(tmp_path / "index.html"), str(out)],
                                capture_output=True, text=True, timeout=180)
        assert result.returncode == 0, result.stderr
        assert out.is_file() and (Path(other) / "out.render-report.json").is_file()
        assert not [p for p in Path(other).iterdir() if p.name.startswith(".html-motion-")]
