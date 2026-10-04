# Reference Analysis

Turn a source video into a beat sheet and a style bible. Everything downstream (prompts, generation, assembly, QC) keys off these two documents.

## Extract frames

All commands assume local ffmpeg and a reference at `./reference.mp4`.

```bash
# Even sampling — first pass look (1 frame every ~N seconds, small)
mkdir -p frames
ffmpeg -i ./reference.mp4 -vf "fps=1/7,scale=640:-1" -frames:v 8 frames/sample_%02d.jpg

# Scene-change detection — finds actual cut points
ffmpeg -i ./reference.mp4 -vf "select='gt(scene,0.3)',showinfo" -vsync vfr frames/scene_%03d.jpg 2>&1 | findstr pts_time

# Contact sheet — one grid image for a quick overview
ffmpeg -i ./reference.mp4 -vf "fps=1/5,scale=320:-1,tile=4x4" -frames:v 1 frames/contact_sheet.jpg

# Full-res key frame at a chosen timestamp (for style donors / QC anchors)
ffmpeg -ss 14.2 -i ./reference.mp4 -frames:v 1 -q:v 2 frames/key_14.2s.jpg
```

If scene detection returns too many or too few cuts, adjust the threshold: `0.2` catches softer dissolves, `0.4` keeps only hard cuts.

## Extract audio

```bash
ffmpeg -i ./reference.mp4 -vn -acodec pcm_s16le -ar 16000 -ac 1 audio.wav
```

Characterize the track by listening or by waveform inspection: presence of narration, BGM genre and tempo, SFX per beat, loudness feel. If an ASR tool exists in the environment, transcribe narration; otherwise record what is audible. Keep the original audio file — Phase 4 may pass it as `--audio-references`.

## Beat sheet format

One row per distinct shot/beat. Target 4–8 beats for a 15–45s reference.

| t (s) | beat | subject | action | camera (size/angle/move) | grade / light | on-screen text | audio |
|---|---|---|---|---|---|---|---|
| 0–7 | hook | red-haired woman | stands, profile to camera | MCU profile, static, 85mm-like, shallow DOF | backlit rim, teal shadows | none | soft strings |
| 7–14 | ... | ... | ... | ... | ... | ... | ... |

Rules:

- Timestamps come from the scene-change pass, rounded to honest boundaries.
- One clear action per beat — if a beat contains two actions, split it.
- Mark transitions: hard cut (default), dissolve, whip — assembly needs this.
- Note any on-screen text, logos, or packaging shots; these become replacement-asset tasks (Hard rule 2).
- From the sheet, derive **N** (shot count) and each shot's `--duration` (seedance_2_5 allows 4–30s; for any other chosen model use its limits from `higgsfield model get <jst>`. Keep every action completable inside its duration — usually 5–8s).

## Style bible format

Fill every field; prompts copy from it verbatim.

```text
MEDIUM:      photoreal cinematic live-action / 3D / illustrated / ...
LENS & DOF:  35mm, shallow depth of field, gentle focus falloff
LIGHTING:    natural sunlight, hard rim backlight, ...
GRADE:       teal-green shadows, warm skin highlights, moderate contrast,
             film emulation (halation, subtle grain)
MOTION:      static tripods + slow push-ins, no handheld shake
CANVAS:      16:9, 24fps (match reference unless told otherwise)
AUDIO:       warm acoustic BGM, diegetic SFX, no narration
TEXT/LOGO:   none in-frame, or: fictional brand on packaging (replace)
```

The STYLE descriptor used in every prompt is built from MEDIUM + LENS + LIGHTING + GRADE + MOTION, plus an explicit style-stability tail, e.g. `photorealistic cinematic live-action, no text overlays, no watermark`.

## Similarity criteria (QC contract for Phase 6)

Per beat, state what "same as the reference" means before generating:

1. **Composition** — same shot size and subject placement (rule of thirds position).
2. **Grade** — shadow/highlight hues match the style bible, not necessarily pixel-exact.
3. **Character** — identity, wardrobe, hair per `references/consistency.md`.
4. **Motion type** — static/handheld/dolly behaves like the reference beat.
5. Allowed deviations — list them explicitly (different faces for rights reasons, replaced brand, different food, etc.).

## Output checklist

- [ ] `frames/` with samples + scene cuts + at least 2 full-res key frames
- [ ] `audio.wav` kept for Phase 4
- [ ] Beat sheet with N and per-shot durations
- [ ] Style bible with every field filled
- [ ] Similarity criteria + allowed deviations
