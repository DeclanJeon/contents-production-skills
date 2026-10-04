"""Deterministic FFmpeg assembly for the 132 autumn 25s master.

Scope: post-render only. Run once videos/SH01.mp4 .. SH05.mp4 have been
downloaded by the orchestrator. This script never generates media, never
re-creates product art, and never substitutes held stills for source motion.

Pipeline per segment:
    source mp4 -> trim [0, trim_s] -> scale-fill 1080x1920 centered crop ->
    fps=30 -> optional product overlay (supplied RGBA, static, composited
    in post per the hybrid-accuracy strategy) -> H.264 intermediate.
Concat:
    five intermediates -> single silent H.264/yuv420p/faststart master at
    delivery/132-autumn-25s.mp4. SH05 additionally carries the transparent
    caption PNG rendered here by Pillow (closing copy for the final 4s),
    faded in over the last 0.7s.

Usage (from productions/132-autumn-25s):
    python scripts/render_ad.py            # probe inputs, render, write QA
    python scripts/render_ad.py --dry-run  # probe + print plan, no ffmpeg

Writes qa/assembly.json with the actual commands, probes, trims, hashes.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
from datetime import datetime, timezone
from typing import NoReturn
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VIDEOS = ROOT / "videos"
IMAGES = ROOT / "images"
QA = ROOT / "qa"
DELIVERY = ROOT / "delivery"
SEGMENTS = DELIVERY / "segments"
ASSEMBLY_JSON = QA / "assembly.json"
OUTPUT = DELIVERY / "132-autumn-25s.mp4"
CAPTION_PNG = DELIVERY / "caption-sh05.png"

W, H = 1080, 1920
FPS = 30
# Editorial trims from source time 0 (time selection, not time compression).
TRIMS = [4.0, 5.0, 6.0, 6.0, 4.0]
SHOTS = ["SH01", "SH02", "SH03", "SH04", "SH05"]

# Supplied-product RGBA layers already positioned on the 1080x1920 frame by
# scripts/composite_products.py (see qa/product-compositing.json). Composited
# deterministically in post so Flow never redraws label artwork.
PRODUCT_OVERLAYS = {"SH01": "P01_product_overlay.png", "SH05": "P10_product_overlay.png"}
PRODUCT_BOTTOMS = {"SH01": 1360, "SH05": 1300}  # lowest product pixel per compositing QA

CAPTION_LINES = [
    ("headline", "가을의 저녁, 빛을 담는 루틴.", 56),
    ("brand", "132 · VITA-C25.5", 64),
    ("detail", "15ml · 132.co.kr", 40),
]
CAPTION_OPACITY = 0.80  # applied to the rendered PNG; overlay uses PNG alpha
CAPTION_BLOCK_TOP = 1340  # strictly below every product bottom
CAPTION_BLOCK_BOTTOM = 1770  # safe margin: frame bottom 1920 - 150px
GOLD = (216, 182, 118)
NAVY = (13, 21, 40)
IVORY = (240, 236, 226)

# Installed Windows fonts with verified full coverage of the closing copy.
FONT_CANDIDATES = [
    r"C:\Windows\Fonts\malgun.ttf",
    r"C:\Windows\Fonts\malgunbd.ttf",
    r"C:\Windows\Fonts\NotoSansKR-VF.ttf",
    r"C:\Windows\Fonts\gulim.ttc",
]

SEG_CRF = "14"          # near-lossless intermediates
FINAL_CRF = "18"
FINAL_PRESET = "slow"
# Require the source to cover the trim; one output-frame tolerance only.
DURATION_TOLERANCE_S = 1.0 / FPS


def fail(msg: str) -> NoReturn:
    raise SystemExit(f"render_ad: {msg}")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def run(cmd: list[str], record: list[list[str]]) -> None:
    record.append(list(cmd))
    proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if proc.returncode != 0:
        tail = (proc.stderr or "").strip().splitlines()[-12:]
        fail(f"command failed ({proc.returncode}): {cmd[0]} …\n" + "\n".join(tail))


def probe(path: Path) -> dict:
    proc = subprocess.run(
        ["ffprobe", "-v", "error", "-print_format", "json",
         "-show_format", "-show_streams", str(path)],
        capture_output=True, text=True, encoding="utf-8", errors="replace")
    if proc.returncode != 0:
        fail(f"ffprobe failed for {rel(path)}: {proc.stderr.strip()}")
    return json.loads(proc.stdout)


def video_stream(meta: dict) -> dict:
    for s in meta.get("streams", []):
        if s.get("codec_type") == "video":
            return s
    fail("no video stream found")


def pick_font() -> str:
    for cand in FONT_CANDIDATES:
        if Path(cand).exists():
            return cand
    fail("no Korean-capable font found among: " + ", ".join(FONT_CANDIDATES))


def build_caption(path: Path) -> dict:
    """Render the 3-line closing copy to a transparent PNG (Pillow only)."""
    from PIL import Image, ImageDraw, ImageFont

    font_path = pick_font()
    fonts = {name: ImageFont.truetype(font_path, size) for name, _, size in CAPTION_LINES}
    card = Image.new("RGBA", (W, H), (0, 0, 0, 0))

    # Soft navy gradient band so type stays legible over the live plate.
    # Fully transparent above CAPTION_BLOCK_TOP-40, ramps to navy alpha ~190.
    band_top, band_bottom = CAPTION_BLOCK_TOP - 40, CAPTION_BLOCK_BOTTOM + 40
    band = Image.new("L", (1, H), 0)
    ramp_px = 30
    for y in range(band_top, min(band_bottom, H)):
        t = min(1.0, (y - band_top) / ramp_px)
        band.putpixel((0, y), round(190 * t))
    band = band.resize((W, H))
    card.paste(Image.new("RGBA", (W, H), NAVY + (255,)), (0, 0), band)

    draw = ImageDraw.Draw(card)
    ys = {"headline": 1410, "brand": 1530, "detail": 1640}
    colors = {"headline": IVORY, "brand": GOLD, "detail": IVORY}
    for name, text, _ in CAPTION_LINES:
        font = fonts[name]
        box = draw.textbbox((0, 0), text, font=font)
        x = (W - (box[2] - box[0])) // 2 - box[0]
        draw.text((x, ys[name]), text, font=font, fill=colors[name])

    # Hairline gold rule above the brand line.
    draw.rectangle([(W // 2 - 120, 1512), (W // 2 + 120, 1514)], fill=GOLD + (220,))

    # Apply global caption opacity through the alpha channel only.
    alpha = card.getchannel("A").point(lambda p: round(p * CAPTION_OPACITY))
    card.putalpha(alpha)
    path.parent.mkdir(parents=True, exist_ok=True)
    card.save(path)
    return {"path": rel(path), "font": font_path, "lines": [t for _, t, _ in CAPTION_LINES],
            "block": [CAPTION_BLOCK_TOP, CAPTION_BLOCK_BOTTOM], "opacity": CAPTION_OPACITY,
            "visible_s": TRIMS[-1], "sha256": sha256(path)}


def main() -> None:
    ap = argparse.ArgumentParser(description="Assemble the 132 autumn 25s master.")
    ap.add_argument("--dry-run", action="store_true", help="probe inputs and print the plan; run no ffmpeg")
    ap.add_argument("--keep-segments", action="store_true", help="keep per-shot intermediates")
    args = ap.parse_args()

    if shutil.which("ffmpeg") is None or shutil.which("ffprobe") is None:
        fail("ffmpeg/ffprobe not on PATH")
    try:
        import PIL  # noqa: F401
    except ImportError:
        fail("Pillow is required to render the caption PNG")

    # --- Probe every source and enforce the trim/duration contract. ---
    vinfo = []
    for shot, trim in zip(SHOTS, TRIMS):
        src = VIDEOS / f"{shot}.mp4"
        if not src.exists():
            fail(f"missing input {rel(src)} — download it before rendering; "
                 "refusing to substitute stills")
        meta = probe(src)
        vs = video_stream(meta)
        dur = float(meta["format"]["duration"])
        if dur + DURATION_TOLERANCE_S < trim:
            fail(f"{rel(src)} duration {dur:.3f}s < required trim {trim}s — "
                 "refusing to pad with repeated frames")
        fps_frac = Fraction(vs.get("avg_frame_rate", "0/1"))
        vinfo.append({
            "shot": shot, "file": rel(src), "sha256": sha256(src),
            "width": vs.get("width"), "height": vs.get("height"),
            "pix_fmt": vs.get("pix_fmt"), "avg_frame_rate": str(vs.get("avg_frame_rate")),
            "r_frame_rate": str(vs.get("r_frame_rate")),
            "duration_s": dur, "source_trim_s": [0.0, trim],
            "audio_streams": sum(1 for s in meta.get("streams", []) if s.get("codec_type") == "audio"),
            "fps_float": float(fps_frac) if fps_frac else None,
        })

    for name in set(PRODUCT_OVERLAYS.values()):
        if not (IMAGES / name).exists():
            fail(f"missing product overlay images/{name}")

    caption = build_caption(CAPTION_PNG)

    ffmpeg_v = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True,
                              encoding="utf-8", errors="replace").stdout.splitlines()[0]
    ffprobe_v = subprocess.run(["ffprobe", "-version"], capture_output=True, text=True,
                               encoding="utf-8", errors="replace").stdout.splitlines()[0]

    commands: list[list[str]] = []
    seg_paths = [SEGMENTS / f"{shot}.mp4" for shot in SHOTS]

    # --- Render one normalized, overlaid intermediate per shot. ---
    for i, (shot, info) in enumerate(zip(SHOTS, vinfo)):
        trim = info["source_trim_s"][1]
        inputs = []
        filters = [f"[0:v]scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,"
                   f"crop={W}:{H},fps={FPS},format=yuv420p,setsar=1[base]"]
        n = 0
        last = "[base]"
        if shot in PRODUCT_OVERLAYS:
            n += 1
            inputs += ["-loop", "1", "-i", str(IMAGES / PRODUCT_OVERLAYS[shot])]
            filters.append(f"{last}[{n}:v]overlay=0:0[ol{n}]")
            last = f"[ol{n}]"
        if shot == "SH05":
            n += 1
            inputs += ["-loop", "1", "-i", str(CAPTION_PNG)]
            filters.append(f"{last}[{n}:v]overlay=0:0[ol{n}]")
            last = f"[ol{n}]"
        cmd = (["ffmpeg", "-y", "-nostdin", "-i", str(VIDEOS / f"{shot}.mp4")]
               + inputs
               + ["-filter_complex", ";".join(filters), "-map", last,
                  "-t", f"{trim:.3f}", "-r", str(FPS),
                  "-c:v", "libx264", "-preset", "medium", "-crf", SEG_CRF,
                  "-pix_fmt", "yuv420p", "-an", str(seg_paths[i])])
        if args.dry_run:
            print("SEG", shot, " ".join(cmd))
        else:
            SEGMENTS.mkdir(parents=True, exist_ok=True)
            run(cmd, commands)
    concat_list = SEGMENTS / "concat.txt"
    concat_text = "".join(f"file '{p.name}'\n" for p in seg_paths)
    final_cmd = (["ffmpeg", "-y", "-nostdin", "-f", "concat", "-safe", "0",
                  "-i", str(concat_list), "-c:v", "libx264", "-preset", FINAL_PRESET,
                  "-crf", FINAL_CRF, "-pix_fmt", "yuv420p", "-r", str(FPS),
                  "-an", "-movflags", "+faststart", str(OUTPUT)])
    if args.dry_run:
        print("CONCAT", " ".join(final_cmd))
        print("DRY-RUN OK:", len(vinfo), "inputs probed; no ffmpeg executed")
        return

    SEGMENTS.mkdir(parents=True, exist_ok=True)
    concat_list.write_text(concat_text, encoding="utf-8")
    run(final_cmd, commands)

    out_meta = probe(OUTPUT)
    out_vs = video_stream(out_meta)
    out_dur = float(out_meta["format"]["duration"])
    expected_frames = round(sum(TRIMS) * FPS)
    record = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "tool_versions": {"ffmpeg": ffmpeg_v, "ffprobe": ffprobe_v},
        "inputs": vinfo,
        "overlays": {shot: {"file": f"images/{PRODUCT_OVERLAYS[shot]}",
                            "sha256": sha256(IMAGES / PRODUCT_OVERLAYS[shot]),
                            "mode": "static supplied-RGBA composite at 0:0",
                            "product_bottom_px": PRODUCT_BOTTOMS[shot]}
                     for shot in PRODUCT_OVERLAYS},
        "caption": caption,
        "assembly": {"width": W, "height": H, "fps": FPS, "trims_s": TRIMS,
                     "audio": "dropped (-an); no_dialogue, silent master"},
        "commands": commands,
        "output": {"file": rel(OUTPUT), "sha256": sha256(OUTPUT),
                   "duration_s": out_dur, "codec": out_vs.get("codec_name"),
                   "pix_fmt": out_vs.get("pix_fmt"), "avg_frame_rate": str(out_vs.get("avg_frame_rate")),
                   "expected_frames": expected_frames,
                   "expected_duration_s": sum(TRIMS)},
    }
    ASSEMBLY_JSON.parent.mkdir(parents=True, exist_ok=True)
    ASSEMBLY_JSON.write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")

    if not args.keep_segments:
        for p in seg_paths:
            p.unlink(missing_ok=True)
        concat_list.unlink(missing_ok=True)

    print(json.dumps({"output": record["output"], "qa": rel(ASSEMBLY_JSON)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
