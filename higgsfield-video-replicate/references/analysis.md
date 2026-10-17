# Reference Analysis

Turn a source video into a beat sheet and a style bible. Everything downstream (prompts, generation, assembly, QC) keys off these two documents.

## Extract frames

All commands assume local ffmpeg and a reference at `./reference.mp4`.

```bash
# Even sampling — first pass look (1 frame every ~N seconds, small)
mkdir -p frames
ffmpeg -i ./reference.mp4 -vf "fps=1/7,scale=640:-1" -frames:v 8 frames/sample_%02d.jpg

# Scene-change detection — proposes candidate cut points for visual inspection
ffmpeg -i ./reference.mp4 -vf "select='gt(scene,0.3)',showinfo" -vsync vfr frames/scene_%03d.jpg 2>&1 | findstr pts_time

# Contact sheet — one grid image for a quick overview
ffmpeg -i ./reference.mp4 -vf "fps=1/5,scale=320:-1,tile=4x4" -frames:v 1 frames/contact_sheet.jpg

# Full-res key frame at a chosen timestamp (for style donors / QC anchors)
ffmpeg -ss 14.2 -i ./reference.mp4 -frames:v 1 -q:v 2 frames/key_14.2s.jpg
```

If scene detection returns too many or too few candidates, tune the threshold and inspect transitions. `0.2` and `0.4` are example sensitivity settings, not guarantees of detecting dissolves or only hard cuts.

## Extract audio

```bash
ffmpeg -i ./reference.mp4 -vn -acodec pcm_s16le -ar 16000 -ac 1 audio.wav
```

Characterize the track by listening or by waveform inspection: presence of narration, BGM genre and tempo, SFX per beat, loudness feel. If an ASR tool exists in the environment, transcribe narration; otherwise record what is audible. Keep the original audio file — Phase 4 may pass it as `--audio-references`.

## Beat sheet format

One row per observed shot/beat. A 4–8-beat plan for a 15–45s reference is a house planning heuristic; preserve the observed structure rather than forcing that count.

| t (s) | beat | subject | action | camera (size/angle/move) | grade / light | on-screen text | audio |
|---|---|---|---|---|---|---|---|
| 0–7 | hook | red-haired woman | stands, profile to camera | MCU profile, static, 85mm-like, shallow DOF | backlit rim, teal shadows | none | soft strings |
| 7–14 | ... | ... | ... | ... | ... | ... | ... |

Rules:

- Record inspected shot boundaries and their method/uncertainty; scene-change timestamps are candidate evidence, not mandatory detected truth.
- Scene scores identify candidate cuts, not ground truth. Inspect adjacent frames and transitions; for dissolves or continuous takes, record manually inspected boundaries and their uncertainty instead of inventing detection results.
- One clear action per beat — if a beat contains two actions, split it.
- Mark transitions: hard cut (default), dissolve, whip — assembly needs this.
- Note any on-screen text, logos, or packaging shots; these become replacement-asset tasks (Hard rule 2).
- From the sheet, derive **N** (shot count) and planned shot durations. Read the selected model's current limits before mapping them to submission durations; any split/retime must preserve the approved timeline and be recorded.

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

Record evidence alongside each field: source file/hash, inspected timestamp or range, method (`metadata`, `visual`, `listening`, or `inference`) and confidence. A visual lens estimate such as “85mm-like” is not a measured focal length; color appearance is not a recovered LUT; sampled stills do not establish motion or audio. Leave inaccessible fields `unknown` and report the inspected scope. Keep observed reference facts separate from proposed adaptation choices; example rows above are format examples, never observations of the user's video.

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
