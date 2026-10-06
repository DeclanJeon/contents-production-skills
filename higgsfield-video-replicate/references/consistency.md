# Photoreal Multi-Shot Character Consistency

Keep recurring characters recognizable across N independently generated shots.

> Limits below are **verified for `seedance_2_5` only**. If the gate question chose another model, re-check with `higgsfield model get <jst> --json` — nothing here transfers automatically.

## Verified constraints (`seedance_2_5`)

- **No soul-id parameter.** The schema has no `soul_id` / `custom_reference_id` — `--soul-id` works only on image models (`text2image_soul_v2`, `soul_cinematic`). Video consistency therefore always travels as **reference images** (`--image-references`, `--start-image`, `--end-image`).
- Images including `start_image`/`end_image` ≤ 30; total reference media ≤ 50; `start_image`/`end_image` allowed only in `omni_reference`.
- Practical per-shot budget: **1 video reference + 1–3 images + optional start frame**. More references rarely help and obscure which one governs identity.

## Strategy ladder (pick the first that applies)

### 1. Character carried from the reference video

Extract 2–3 clean frames per character from the reference (front, three-quarter, profile) at full resolution:

```bash
ffmpeg -ss 7.5  -i ./reference.mp4 -frames:v 1 -q:v 2 char/hero_front.jpg
ffmpeg -ss 28.1 -i ./reference.mp4 -frames:v 1 -q:v 2 char/hero_34.jpg
```

Pass them with `--image-references` on every shot that character appears in.

### 2. Original character (new design)

A **character sheet** — one image, multi-angle, with wardrobe spelled out — is an image-generation artifact. In this package Higgsfield image jobs are ineligible (package gate): obtain the sheet from the explicitly authorized eligible image executor (`codex-imagen` default) or a user-supplied still. Where image generation is permitted, the preserved recipe is:

```bash
higgsfield generate create seedream_v5_pro \
  --prompt "character sheet, three views front/three-quarter/profile of <person>, <hair>, <outfit details>, neutral studio background, photoreal" \
  --aspect_ratio 16:9 --resolution 2k --wait --json
```

`gpt_image_2_5` is the preserved fallback. The sheet (or its crops) becomes the `--image-references` input for all shots.

### 3. The character is a real person the user owns

`higgsfield-soul-id` training is a separate, explicitly-authorized lifecycle (5–20 photos → reference id) — never an implicit sub-step of replication. Even with a trained Soul, rendering the cinematic sheet via `soul_cinematic` / `text2image_soul_v2` is an image job — ineligible in this package; use a supplied sheet or the authorized eligible image executor instead. Any sheet still feeds the video model as plain reference images.

### 4. No recurring character

Skip this file; the video reference alone carries the look.

## Shot chaining (motion + appearance handoff)

Last frame of shot N becomes the start frame of shot N+1. **This creates a hard dependency:** shot N+1 cannot be submitted until shot N's clip has completed, its last frame extracted, and the anchor inspected — chained shots run strictly in order; only shots without a chaining anchor may submit concurrently.

```bash
# grab last frame of the previous generated clip
ffmpeg -sseof -0.1 -i ./shots/shot_03.mp4 -update 1 -frames:v 1 shots/shot_03_last.png

# use it as the anchor for the next clip
higgsfield generate create seedance_2_5 --mode omni_reference \
  --prompt "<Shot 4 prompt>" --video-references ./reference.mp4 \
  --image-references ./char/hero_front.jpg \
  --start-image ./shots/shot_03_last.png \
  --duration 7 ... 
```

Also pin shot 1's `--start-image` to the reference's first beat frame when the opening composition must match exactly. In delegated work, record which approved predecessor frame asset/version anchored each chained shot in the internal return.

## Wardrobe and props

- Put the wardrobe sentence in the CHARACTER block and repeat it byte-identically in every prompt (same rule as STYLE).
- When a distinctive prop or outfit detail is on screen, add one detail frame of it as an image reference for the shots that show it.

## Drift recovery

| Symptom | Fix |
|---|---|
| Face drifts between shots | Add a closer, straight-on character frame to `--image-references`; tighten the CHARACTER block; regenerate only that shot |
| Wardrobe/color drifts | Repeat wardrobe verbatim; add one wardrobe detail frame; regenerate that shot |
| Shot start doesn't continue the previous one | Re-anchor with `--start-image` from the previous shot's last frame |
| Two identical failures | Change the approach: split the shot, switch angle, or reduce references — do not resubmit the same prompt |
| Identity conflicts with the video reference | The reference video's own characters may be overriding the sheet — drop the video reference for that shot and lean on images + prompt (accepting a looser style match), or regenerate the sheet to resemble the reference's character |

## Anti-patterns

- Passing 10+ character frames per shot — pick representative frames, not a dump.
- Re-generating the sheet between shots — lock the sheet in Phase 1; all shots consume the same asset.
- Describing the character differently per prompt "for variety" — breaks identity; vary only SCENE/MOTION.
