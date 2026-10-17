"""Consumer-visible delivery gate failures, exercised against a real local MP4."""
from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess

import pytest

MODULE = Path(__file__).with_name("verify_delivery.py")
spec = importlib.util.spec_from_file_location("verify_stills_delivery", MODULE)
verifier = importlib.util.module_from_spec(spec)
spec.loader.exec_module(verifier)


@pytest.fixture(scope="module")
def delivery_bytes(tmp_path_factory):
    if not shutil.which("ffmpeg") or not shutil.which("ffprobe"):
        pytest.skip("real delivery regression fixture requires ffmpeg and ffprobe")
    video = tmp_path_factory.mktemp("stills-delivery") / "delivery.mp4"
    subprocess.run([
        "ffmpeg", "-v", "error", "-f", "lavfi", "-i",
        "color=c=gray:s=1080x1920:r=30", "-f", "lavfi", "-i",
        "anullsrc=r=44100:cl=mono", "-t", "15", "-c:v", "libx264",
        "-preset", "ultrafast", "-pix_fmt", "yuv420p", "-c:a", "aac",
        "-shortest", str(video),
    ], check=True, capture_output=True)
    return video.read_bytes()


def make_delivery(tmp_path, delivery_bytes, **changes):
    video = tmp_path / "delivery.mp4"
    video.write_bytes(delivery_bytes)
    qa = {
        "speed": 4.0,
        "actual_duration_s": 15.0,
        "frames": 450,
        "video_sha256": hashlib.sha256(delivery_bytes).hexdigest(),
        "full_decode_verified": True,
        "publishable": False,
        "status": "RENDERED_NOT_PUBLISH_APPROVED",
    }
    qa.update(changes)
    return video, qa


@pytest.mark.parametrize("speed", [0, -1, True, None, "4", float("inf"), float("nan")])
def test_invalid_retiming_speed_is_a_failed_report(tmp_path, delivery_bytes, speed):
    video, qa = make_delivery(tmp_path, delivery_bytes, speed=speed)
    video.with_suffix(".qa.json").write_text(json.dumps(qa), encoding="utf-8")
    report = verifier.verify(video)
    assert report["ok"] is False
    assert any("speed" in problem for problem in report["problems"])


@pytest.mark.parametrize("digest", [None, "", "0" * 64])
def test_missing_or_foreign_hash_cannot_certify_media(tmp_path, delivery_bytes, digest):
    video, qa = make_delivery(tmp_path, delivery_bytes)
    if digest is None:
        del qa["video_sha256"]
    else:
        qa["video_sha256"] = digest
    video.with_suffix(".qa.json").write_text(json.dumps(qa), encoding="utf-8")
    report = verifier.verify(video)
    assert report["ok"] is False
    assert any("sidecar" in problem for problem in report["problems"])


@pytest.mark.parametrize("changes", [
    {"publishable": True},
    {"status": "PUBLISH_APPROVED"},
    {"publishable": None},
])
def test_unapproved_delivery_requires_consistent_approval_fields(tmp_path, delivery_bytes, changes):
    video, qa = make_delivery(tmp_path, delivery_bytes, **changes)
    video.with_suffix(".qa.json").write_text(json.dumps(qa), encoding="utf-8")
    report = verifier.verify(video)
    assert report["ok"] is False
    assert any("publishable" in problem for problem in report["problems"])
