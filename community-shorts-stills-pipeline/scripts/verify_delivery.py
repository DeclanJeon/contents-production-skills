"""Verify a delivered stills Short against its render QA sidecar.

Checks the artifact the pipeline actually ships: 9:16 geometry, 30 fps, both streams inside the
declared window, the streams agreeing with each other, a full decode, and a speed that makes the
retimed runtime consistent with the authored 60 s time base. Exits non-zero on any failure.

    python verify_delivery.py 10_DELIVERY/episode01-v003-x1.4.mp4

Reads the sidecar next to the video (`<name>.qa.json`) and cross-checks its hashes, so a sidecar
copied from another render cannot pass.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import subprocess
import sys
from pathlib import Path

W, H, FPS = 1080, 1920, 30
BASE_DURATION_S = 60.0
TOLERANCE_S = 0.15
SPEED_MIN, SPEED_MAX = 0.25, 4.0


def probe(path: Path) -> dict:
    out = subprocess.run(["ffprobe", "-v", "error", "-print_format", "json", "-show_format", "-show_streams", str(path)],
                         check=True, capture_output=True, text=True, encoding="utf-8")
    return json.loads(out.stdout)


def count_frames(path: Path, selector: str) -> int:
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", selector, "-count_frames",
                          "-show_entries", "stream=nb_read_frames", "-of", "csv=p=0", str(path)],
                         check=True, capture_output=True, text=True, encoding="utf-8")
    return int(out.stdout.strip())


def verify(video: Path) -> dict:
    problems: list[str] = []
    sidecar = video.with_suffix(".qa.json")
    if not sidecar.is_file():
        return {"ok": False, "problems": [f"missing QA sidecar {sidecar.name}"]}
    qa = json.loads(sidecar.read_text(encoding="utf-8"))
    meta = probe(video)
    streams = meta["streams"]
    video_stream = next((s for s in streams if s["codec_type"] == "video"), None)
    audio_stream = next((s for s in streams if s["codec_type"] == "audio"), None)
    if video_stream is None or audio_stream is None:
        return {"ok": False, "problems": ["the delivery must carry both a picture and a soundtrack"]}
    if (video_stream.get("width"), video_stream.get("height")) != (W, H):
        problems.append(f"geometry {video_stream.get('width')}x{video_stream.get('height')} is not {W}x{H}")
    if video_stream.get("r_frame_rate") != f"{FPS}/1":
        problems.append(f"frame rate {video_stream.get('r_frame_rate')} is not {FPS} fps")

    speed = qa.get("speed", 1.0)
    if type(speed) not in (int, float) or isinstance(speed, bool) or not math.isfinite(speed) or not SPEED_MIN <= speed <= SPEED_MAX:
        problems.append(f"QA speed {speed!r} is outside {SPEED_MIN}..{SPEED_MAX}")
        return {"ok": False, "problems": problems}

    runtime = float(meta["format"]["duration"])
    expected = BASE_DURATION_S / speed
    if not 58 <= runtime * speed <= 60.15:
        problems.append(f"delivered {runtime}s x {speed} is outside the authored 58..60.15 s window")
    if abs(runtime - expected) > TOLERANCE_S:
        problems.append(f"delivered {runtime}s drifted from the retimed target {expected:.6f}s")
    if qa.get("actual_duration_s") is not None and abs(float(qa["actual_duration_s"]) - runtime) > TOLERANCE_S:
        problems.append("the QA sidecar's runtime disagrees with the artifact")

    stream_video = float(video_stream["duration"])
    stream_audio = float(audio_stream["duration"])
    if abs(stream_audio - stream_video) > TOLERANCE_S:
        problems.append(f"picture {stream_video}s and soundtrack {stream_audio}s differ by more than {TOLERANCE_S}s")

    frames = int(video_stream.get("nb_frames") or 0)
    if frames != round(expected * FPS):
        problems.append(f"{frames} frames does not match the retimed target {round(expected * FPS)}")
    if qa.get("frames") is not None and qa["frames"] != frames:
        problems.append("the QA sidecar's frame count disagrees with the artifact")

    # a container duration can hide a longer raw audio decode (AAC encoder padding per clip)
    decoded = count_frames(video, "a:0")
    if not frames - 2 <= round(decoded * 1024 / 44100 * FPS) <= frames + 2 or decoded / 44100 > stream_audio + 0.2:
        problems.append(f"raw audio decode ({decoded} frames) runs past the picture")

    digest = hashlib.sha256(video.read_bytes()).hexdigest()
    if qa.get("video_sha256") != digest:
        problems.append("the QA sidecar is missing the matching SHA-256 for these bytes")

    if qa.get("full_decode_verified") is not True:
        problems.append("the QA sidecar does not record a full decode")
    if qa.get("publishable") is not False or qa.get("status") != "RENDERED_NOT_PUBLISH_APPROVED":
        problems.append("delivery requires status RENDERED_NOT_PUBLISH_APPROVED and publishable=false; technical smoke is not delivery")

    decode = subprocess.run(["ffmpeg", "-v", "error", "-xerror", "-i", str(video), "-f", "null", "-"],
                            capture_output=True, text=True, encoding="utf-8")
    if decode.returncode != 0:
        problems.append("a full decode reported errors: " + decode.stderr.strip()[-300:])

    return {"ok": not problems, "problems": problems, "runtime_seconds": runtime, "frames": frames, "speed": speed,
            "video_sha256": digest, "size": int(meta["format"]["size"])}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("video", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    if not args.video.is_file():
        print(f"not a file: {args.video}", file=sys.stderr)
        return 2
    report = verify(args.video)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    elif report["ok"]:
        print(f"OK {args.video.name} {report['runtime_seconds']}s {report['frames']} frames speed={report['speed']} sha={report['video_sha256'][:12]}")
    else:
        for problem in report["problems"]:
            print("FAIL " + problem, file=sys.stderr)
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
