"""Webtoon-page episode renderer.

Reproduces a measured *layout grammar* (pale-yellow header bar, hamburger glyph, centered
channel label, title, meta line, thin rule, centered body text, square illustration panel on a
white page) over the episode's own still panels and narration audio.

The geometry is measured from `09_QA/reference-template/ref-*.png` scaled to 1080x1920; no
reference channel identity, view count, meta string, logo or artwork is reproduced. The channel
label is a caller-supplied string and is refused if it is the reference channel's name.

Stills only. No generative motion. Explicit `--technical-smoke` output is never publishable.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import subprocess
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps

W, H, FPS = 1080, 1920, 30

# --- measured template geometry (1080x1920 target; source frames scaled by 1080/608) ---
BAR_H = 213
BAR_BG = "#fdedb6"  # rgb(253,237,182)
ICON_X0, ICON_X1 = 63, 126
ICON_Y0, ICON_Y1 = 95, 152
ICON_LINES = 3
ICON_BAR_RATIO = 0.30  # measured bar thickness / pitch (rows 54-57, 69-71, 84-86)
TITLE_TOP = 286
META_TOP = 380
META_X = 128
RULE_Y, RULE_H = 449, 5
RULE_COLOR = "#5a5a5a"  # rgb(90,90,90)
BODY_TOP = 533
BODY_ADVANCE = 64
BODY_MAX_WIDTH = 830
PANEL_BOX = (85, 690, 993, 1890)  # 908x1200; artwork fills the box edge to edge
PANEL_CENTERING = (0.5, 0.50)  # vertical crop bias when the figure cannot be measured
PANEL_HEAD_MARGIN = 0.10  # keep this fraction of the crop above the top of the character's head
PANEL_INK_THRESHOLD = 110  # a pixel is "character line ink" below this luminance
PAGE_BG = "#ffffff"

SIZES = {"channel": 74, "title": 66, "meta": 36, "body": 46}
CHANNEL_MAX_WIDTH = 830
DEFAULT_FONT = Path("C:/Windows/Fonts/malgunbd.ttf")
SMOKE_LABEL = "LOCAL TEMPLATE / NOT FOR UPLOAD"

# --- delivery speed -------------------------------------------------------------
# The master is always authored at BASE_DURATION_S; delivery speed is a post-render
# time-base change applied to the finished master (video PTS + audio tempo together).
# The project ledger, shot windows, audio cues and captions are never re-timed.
BASE_DURATION_S = 60.0
SPEED_MIN, SPEED_MAX = 0.25, 4.0
SPEED_TOLERANCE_S = 0.15  # allowed drift from BASE_DURATION_S / speed

# the reference channel's identity and its fabricated in-video counters must never be reproduced
REFERENCE_CHANNEL_LABEL = "썰툰"
FORBIDDEN_META = re.compile(r"조회수|views?\b|\d{1,3}(,\d{3})+", re.IGNORECASE)


def call(args: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(args, check=True, capture_output=True, encoding="utf-8", errors="replace")


def probe(path: Path) -> dict:
    return json.loads(call(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)]).stdout)


def _font(font_path: Path, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(font_path), size)


def wrapped(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont, maxwidth: int) -> list[str]:
    """Greedy word wrap with per-character fallback for unbroken runs."""
    lines: list[str] = []
    for paragraph in text.split("\n"):
        line = ""
        for word in paragraph.split():
            candidate = f"{line} {word}" if line else word
            if draw.textlength(candidate, font=font) > maxwidth and line:
                lines.append(line)
                line = ""
            if draw.textlength(word, font=font) > maxwidth:
                for char in word:
                    if draw.textlength(line + char, font=font) > maxwidth and line:
                        lines.append(line)
                        line = ""
                    line += char
            else:
                line = f"{line} {word}" if line else word
        if line:
            lines.append(line)
    return lines


def _draw_centered(draw: ImageDraw.ImageDraw, text: str, y_top: int, font: ImageFont.FreeTypeFont, fill: str) -> None:
    box = font.getbbox(text)
    x = (W - (box[2] - box[0])) // 2 - box[0]
    draw.text((x, y_top - box[1]), text, font=font, fill=fill)


def _draw_left(draw: ImageDraw.ImageDraw, text: str, x_left: int, y_top: int, font: ImageFont.FreeTypeFont, fill: str) -> None:
    box = font.getbbox(text)
    draw.text((x_left - box[0], y_top - box[1]), text, font=font, fill=fill)


def draw_hamburger(draw: ImageDraw.ImageDraw) -> None:
    """Three stacked bars inside the measured icon box (measured bars are ~1/4 of the pitch)."""
    pitch = (ICON_Y1 - ICON_Y0) / (ICON_LINES - 1)
    thickness = pitch * ICON_BAR_RATIO
    for index in range(ICON_LINES):
        y0 = ICON_Y0 + index * pitch
        draw.rounded_rectangle((ICON_X0, y0, ICON_X1 - 1, y0 + thickness - 1), radius=thickness / 2, fill="#000000")


def fit_channel_label(draw: ImageDraw.ImageDraw, label: str, font_path: Path, size: int) -> ImageFont.FreeTypeFont:
    font = _font(font_path, size)
    while size > 24 and draw.textlength(label, font=font) > CHANNEL_MAX_WIDTH:
        size -= 2
        font = _font(font_path, size)
    if draw.textlength(label, font=font) > CHANNEL_MAX_WIDTH:
        raise ValueError("channel label is too wide for the header bar")
    return font


def panel_centering(artwork: Image.Image, box: tuple[int, int, int, int]) -> tuple[float, float]:
    """Vertical crop bias that fills `box` with `artwork` without beheading the figure.

    The panel art is 9:16 while the panel box is 3:4, so a full-width `cover` crop must discard
    rows. Anchor the crop on the drawn character: find the first source row carrying dark line
    ink in the middle of the frame (the character's line art is the darkest thing on a pale
    illustration), then leave PANEL_HEAD_MARGIN of the crop above it.
    """
    x0, y0, x1, y1 = box
    box_w, box_h = x1 - x0, y1 - y0
    source_w, source_h = artwork.size
    window = box_h * source_w / box_w  # source rows consumed by a full-width crop
    slack = source_h - window
    if slack <= 0:
        return PANEL_CENTERING
    grey = artwork.convert("L")
    band = grey.crop((int(source_w * 0.30), 0, int(source_w * 0.70), source_h))
    mask = band.point(lambda value: 255 if value < PANEL_INK_THRESHOLD else 0)
    bounds = mask.getbbox()
    if bounds is None:
        return PANEL_CENTERING
    head = bounds[1]
    bias = (head - window * PANEL_HEAD_MARGIN) / slack
    return (0.5, min(max(bias, 0.0), 1.0))


def page_frame(panel_path: Path, body: str, template: dict, font_path: Path) -> Image.Image:
    """Compose one 1080x1920 webtoon page: header bar, title, meta, rule, body text, panel."""
    card = Image.new("RGB", (W, H), PAGE_BG)
    draw = ImageDraw.Draw(card)
    draw.rectangle((0, 0, W, BAR_H), fill=BAR_BG)
    draw_hamburger(draw)

    channel_font = fit_channel_label(draw, template["channel_label"], font_path, SIZES["channel"])
    channel_box = channel_font.getbbox(template["channel_label"])
    channel_top = (BAR_H - (channel_box[3] - channel_box[1])) // 2 - channel_box[1]
    _draw_centered(draw, template["channel_label"], channel_top, channel_font, "#000000")

    _draw_centered(draw, template["episode_title"], TITLE_TOP, _font(font_path, SIZES["title"]), "#000000")
    _draw_left(draw, template["meta_label"], META_X, META_TOP, _font(font_path, SIZES["meta"]), "#000000")
    draw.rectangle((0, RULE_Y, W, RULE_Y + RULE_H - 1), fill=RULE_COLOR)

    body_font = _font(font_path, SIZES["body"])
    lines = wrapped(draw, body, body_font, BODY_MAX_WIDTH)
    if len(lines) > 3:
        raise ValueError(f"body text needs more than three lines: {body}")
    for index, line in enumerate(lines):
        _draw_centered(draw, line, BODY_TOP + index * BODY_ADVANCE, body_font, "#000000")

    x0, y0, x1, y1 = PANEL_BOX
    artwork = Image.open(panel_path).convert("RGB")
    centering = panel_centering(artwork, PANEL_BOX)
    artwork = ImageOps.fit(artwork, (x1 - x0, y1 - y0), method=Image.Resampling.LANCZOS, centering=centering)
    card.paste(artwork, (x0, y0))
    return card


def _shot_frames(start_s: float, end_s: float) -> int:
    """Frame count for a shot window; the ledger stores seconds rounded to 6 decimals."""
    length = end_s - start_s
    frames = round(length * FPS)
    if not math.isclose(length * FPS, frames, abs_tol=1e-3):
        raise ValueError(f"shot window {start_s}-{end_s} is not frame aligned at {FPS} fps")
    return frames


def speed_plan(speed: float, source_frames: int) -> dict:
    """Delivery time base for a post-render speed change; the master itself stays at 1.0x."""
    if not isinstance(speed, (int, float)) or isinstance(speed, bool) or not math.isfinite(speed):
        raise ValueError("speed must be a finite number")
    if not SPEED_MIN <= speed <= SPEED_MAX:
        raise ValueError(f"speed must be within {SPEED_MIN}..{SPEED_MAX}, got {speed}")
    if not isinstance(source_frames, int) or source_frames < 1:
        raise ValueError("source_frames must be a positive whole number of frames")
    expected_frames = round(source_frames / speed)
    return {
        "speed": float(speed),
        "source_frames": source_frames,
        "target_frames": expected_frames,
        "target_duration_s": round(BASE_DURATION_S / speed, 6),
        "frame_tolerance": max(1, math.ceil(FPS * SPEED_TOLERANCE_S)),
    }


def retime(source: Path, output: Path, plan: dict) -> tuple[float, int]:
    """Write the delivery-speed copy of a finished master and verify its measured runtime.

    Both streams are bounded to their own declared length before the speed change. A master
    concatenated from many AAC clips carries encoder padding that a decoder returns in full,
    which would otherwise give the retimed audio a silent tail longer than its video.
    """
    streams = probe(source)["streams"]
    video_duration = float(next(s for s in streams if s["codec_type"] == "video")["duration"])
    audio_duration = float(next(s for s in streams if s["codec_type"] == "audio")["duration"])
    expected_duration = video_duration / plan["speed"]
    expected_frames = round(video_duration * FPS / plan["speed"])
    call([
        "ffmpeg", "-v", "error", "-y", "-i", str(source),
        "-filter_complex",
        f"[0:v]trim=end={video_duration:.6f},setpts=(PTS-STARTPTS)/{plan['speed']}[v];"
        f"[0:a]atrim=end={audio_duration:.6f},asetpts=PTS-STARTPTS,atempo={plan['speed']}[a]",
        "-map", "[v]", "-map", "[a]", "-sn", "-dn",
        "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
        "-r", str(FPS), "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-ac", "2",
        "-t", f"{expected_duration:.6f}", "-movflags", "+faststart", str(output),
    ])
    meta = probe(output)
    actual = float(meta["format"]["duration"])
    if abs(actual - expected_duration) > SPEED_TOLERANCE_S:
        raise ValueError(
            f"speed change measured {actual}s, expected {expected_duration}s"
            f" +/- {SPEED_TOLERANCE_S}s from a {video_duration}s master"
        )
    out_streams = meta["streams"]
    stream_video = float(next(s for s in out_streams if s["codec_type"] == "video")["duration"])
    stream_audio = float(next(s for s in out_streams if s["codec_type"] == "audio")["duration"])
    if abs(stream_audio - audio_duration / plan["speed"]) > SPEED_TOLERANCE_S:
        raise ValueError(
            f"retimed audio measured {stream_audio}s, expected {audio_duration / plan['speed']}s"
            " - the source carries unpadded decode length"
        )
    if abs(stream_audio - stream_video) > SPEED_TOLERANCE_S:
        raise ValueError(f"retimed streams disagree: video {stream_video}s vs audio {stream_audio}s")
    counted = count_frames(output)
    if abs(counted - expected_frames) > plan["frame_tolerance"]:
        raise ValueError(f"speed change produced {counted} frames, expected {expected_frames}")
    call(["ffmpeg", "-v", "error", "-xerror", "-i", str(output), "-f", "null", "-"])
    return actual, counted


def count_frames(path: Path) -> int:
    out = call([
        "ffprobe", "-v", "error", "-select_streams", "v:0", "-count_frames",
        "-show_entries", "stream=nb_read_frames", "-of", "default=nokey=1:noprint_wrappers=1", str(path),
    ]).stdout.strip()
    return int(out)


def load_scenes(project_path: Path, audio_dir: Path) -> list[dict]:
    project = json.loads(project_path.read_text(encoding="utf-8"))
    base = project_path.resolve().parent
    registry = {a["id"]: a for a in project["asset_registry"]}
    scenes = []
    for index, shot in enumerate(project["shots"], start=1):
        speech = shot.get("speech") or []
        if len(speech) != 1 or not str(speech[0].get("text", "")).strip():
            raise ValueError(f"{shot['id']} must carry exactly one speech line")
        panel_ids = [a for a in shot["asset_ids"] if a.endswith("-IMAGE")]
        if len(panel_ids) != 1:
            raise ValueError(f"{shot['id']} must reference exactly one panel image asset")
        asset = registry.get(panel_ids[0])
        if not asset or not asset.get("path"):
            raise ValueError(f"{panel_ids[0]} is not a registered asset with a path")
        panel = (base / asset["path"]).resolve()
        if not panel.is_file():
            raise ValueError(f"missing panel image {panel}")
        audio = audio_dir / f"SP{index:02d}.wav"
        if not audio.is_file():
            raise ValueError(f"missing narration audio {audio}")
        scenes.append({
            "index": index,
            "shot_id": shot["id"],
            "speech_id": speech[0]["id"],
            "start_s": float(shot["start_s"]),
            "end_s": float(shot["end_s"]),
            "frames": _shot_frames(float(shot["start_s"]), float(shot["end_s"])),
            "body": speech[0]["text"],
            "panel_id": panel_ids[0],
            "panel": panel,
            "audio": audio,
        })
    return scenes


def validate_template(template: dict) -> None:
    label = template.get("channel_label")
    if not isinstance(label, str) or not label.strip():
        raise ValueError("template needs a non-empty channel_label")
    if label.strip() == REFERENCE_CHANNEL_LABEL:
        raise ValueError("channel_label must be this channel's own name, not the reference channel's")
    meta = template.get("meta_label", "")
    if not isinstance(meta, str) or not meta.strip():
        raise ValueError("template needs a non-empty meta_label")
    if FORBIDDEN_META.search(meta):
        raise ValueError("meta_label must not reproduce a view count or invented counter")
    if not str(template.get("episode_title", "")).strip():
        raise ValueError("template needs a non-empty episode_title")


def inside(base: Path, name: str) -> Path:
    target = (base / name).resolve()
    if not target.is_relative_to(base.resolve()) or not target.is_file():
        raise ValueError("Input must be an existing file inside the episode directory")
    return target


def _encode_master(rows: list[dict], template: dict, output: Path, font_path: Path, smoke: bool, total_s: float) -> int:
    """Render one webtoon page per row into a single master and bound both streams to `total_s`.

    Every per-clip AAC carries encoder padding; concatenating them would otherwise leave the
    master with a silent audio tail longer than its picture.
    """
    total_frames = round(total_s * FPS)
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="webtoon-", dir=output.parent) as tmp:
        temp = Path(tmp)
        clips = []
        for index, row in enumerate(rows, 1):
            duration = row["duration_s"]
            png = temp / f"{index:03d}.png"
            page_frame(Path(row["panel"]), row["body"], template, font_path).save(png)
            clip = temp / f"{index:03d}.mp4"
            args = ["ffmpeg", "-v", "error", "-y", "-loop", "1", "-framerate", str(FPS), "-i", str(png)]
            if smoke or row.get("audio") is None:
                args += ["-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=44100"]
            else:
                args += ["-i", str(row["audio"])]
            args += [
                "-af", "apad", "-t", f"{duration:.6f}", "-map", "0:v:0", "-map", "1:a:0",
                "-vf", "format=yuv420p", "-c:v", "libx264", "-preset", "medium", "-crf", "20",
                "-r", str(FPS), "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-ac", "2", str(clip),
            ]
            call(args)
            clips.append(clip)
        listing = temp / "concat.txt"
        listing.write_text("".join(f"file '{p.as_posix()}'\n" for p in clips), encoding="utf-8")
        joined = temp / "joined.mp4"
        call(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(listing), "-c", "copy", str(joined)])
        final = temp / "final.mp4"
        call([
            "ffmpeg", "-v", "error", "-y", "-i", str(joined),
            "-filter_complex",
            f"[0:v]trim=end={total_s:.6f},setpts=PTS-STARTPTS[v];"
            f"[0:a]atrim=end={total_s:.6f},asetpts=PTS-STARTPTS[a]",
            "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "medium", "-crf", "20",
            "-pix_fmt", "yuv420p", "-r", str(FPS), "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-ac", "2",
            "-t", f"{total_s:.6f}", "-movflags", "+faststart", str(final),
        ])
        actual = float(probe(final)["format"]["duration"])
        if abs(actual - total_s) > SPEED_TOLERANCE_S:
            raise ValueError(f"encoded master runtime {actual} drifted from the authored {total_s}")
        call(["ffmpeg", "-v", "error", "-xerror", "-i", str(final), "-f", "null", "-"])
        final.replace(output)
    return total_frames


def render(project_path: Path | None = None, template_path: Path | None = None, output: Path | None = None,
           audio_dir: Path | None = None, font_path: Path | None = None, smoke: bool = False,
           speed: float = 1.0, manifest: Path | None = None) -> dict:
    """Render a stills webtoon episode master and its delivery-speed copy.

    Two entry layouts are supported. A `project_path` + `template_path` + `audio_dir` trio renders
    straight from the episode ledger and a directory of `SPnn.wav` narration. A `manifest` renders
    from a run-built manifest whose scenes may come from a different narration layout; the manifest
    supplies its own `template`, `timebase_s` and optional `speed`.
    """
    if manifest is not None:
        return _render_manifest(Path(manifest), output, font_path, smoke, speed)
    template = json.loads(template_path.read_text(encoding="utf-8"))
    if smoke:
        template = {**template, "channel_label": SMOKE_LABEL}
    validate_template(template)
    if output.exists():
        raise ValueError("Refusing to overwrite existing output")
    scenes = load_scenes(project_path, audio_dir)
    total_frames = sum(s["frames"] for s in scenes)
    if total_frames != 60 * FPS:
        raise ValueError(f"frame-aligned shots must total {60 * FPS} frames, got {total_frames}")
    rows = [{"panel": Path(s["panel"]), "body": s["body"],
             "audio": None if smoke else Path(s["audio"]), "duration_s": s["frames"] / FPS} for s in scenes]
    plan = speed_plan(speed, total_frames)
    _encode_master(rows, template, output, font_path, smoke, total_frames / FPS)
    return _finish(output, plan, total_frames, smoke,
                   {"template_sha256": hashlib.sha256(template_path.read_bytes()).hexdigest(),
                    "project_sha256": hashlib.sha256(project_path.read_bytes()).hexdigest()})


def _render_manifest(manifest_path: Path, output: Path, font_path: Path, smoke: bool, speed: float) -> dict:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if type(manifest.get("technical_smoke")) is not bool or manifest["technical_smoke"] != smoke:
        raise ValueError("Manifest and explicit --technical-smoke flag must agree")
    if not smoke and (manifest.get("rights_status") != "cleared" or not manifest.get("source_url")):
        raise ValueError("Production rendering needs explicit rights and source provenance")
    template = manifest.get("template")
    if not isinstance(template, dict):
        raise ValueError("the manifest must carry the episode's webtoon-page template")
    if smoke:
        template = {**template, "channel_label": SMOKE_LABEL}
    validate_template(template)
    if output.exists():
        raise ValueError("Refusing to overwrite existing output")
    timebase_s = float(manifest.get("timebase_s", BASE_DURATION_S))
    speed = float(manifest.get("speed", speed))
    base = manifest_path.resolve().parent
    rows = []
    for scene in manifest["scenes"]:
        audio = None
        if not smoke:
            if not scene.get("audio"):
                raise ValueError("Production scenes must carry a real narration file")
            audio = inside(base, scene["audio"])
        rows.append({"panel": inside(base, scene["image"]), "body": scene.get("body", ""),
                     "audio": audio, "duration_s": float(scene["duration_s"])})
    total = sum(r["duration_s"] for r in rows)
    if abs(total - timebase_s) > SPEED_TOLERANCE_S or not 58 <= total <= 60.15:
        raise ValueError(f"manifest scene durations total {total}s, outside the {timebase_s}s time base")
    total_frames = _encode_master(rows, template, output, font_path, smoke, timebase_s)
    plan = speed_plan(speed, total_frames)
    return _finish(output, plan, total_frames, smoke,
                   {"source_manifest_sha256": hashlib.sha256(manifest_path.read_bytes()).hexdigest()})


def _finish(output: Path, plan: dict, total_frames: int, smoke: bool, provenance: dict) -> dict:
    meta = probe(output)
    actual = float(meta["format"]["duration"])
    actual_frames = total_frames
    if plan["speed"] != 1.0:
        with tempfile.TemporaryDirectory(prefix="webtoon-speed-", dir=output.parent) as stmp:
            fast = Path(stmp) / "speed.mp4"
            actual, actual_frames = retime(output, fast, plan)
            fast.replace(output)
    report = {
        "status": "TECHNICAL_SMOKE_ONLY" if smoke else "RENDERED_NOT_PUBLISH_APPROVED",
        "technical_smoke": smoke,
        "publishable": False,
        "runtime_seconds": actual,
        "frames": actual_frames,
        "master_runtime_seconds": total_frames / FPS,
        "master_frames": total_frames,
        "speed": plan["speed"],
        "target_runtime_seconds": round((total_frames / FPS) / plan["speed"], 6),
        "width": W, "height": H, "fps": FPS,
        "full_decode_verified": True,
        "audio_listening_verified": False,
        **provenance,
        "video_sha256": hashlib.sha256(output.read_bytes()).hexdigest(),
    }
    output.with_suffix(".qa.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, help="run-built manifest whose scenes carry their own template")
    parser.add_argument("--project", type=Path, help="episode project.json")
    parser.add_argument("--template", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--audio-dir", type=Path)
    parser.add_argument("--font", type=Path, default=DEFAULT_FONT)
    parser.add_argument("--speed", type=float, default=1.0, help="post-render delivery speed; the master stays at 1.0x")
    parser.add_argument("--technical-smoke", action="store_true")
    args = parser.parse_args()
    if args.manifest is None and not (args.project and args.template and args.audio_dir):
        parser.error("give either --manifest or --project with --template and --audio-dir")
    report = render(args.project, args.template, args.output, args.audio_dir, args.font,
                    args.technical_smoke, args.speed, manifest=args.manifest)
    print(json.dumps(report, ensure_ascii=False))


if __name__ == "__main__":
    main()
