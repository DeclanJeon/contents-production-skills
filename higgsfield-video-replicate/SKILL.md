---
name: higgsfield-video-replicate
version: 0.15.0
description: |
  Replicate an existing reference video into a new similar-style video:
  analyze its shots, lock a style bible and characters, regenerate every
  shot with a user-chosen reference-capable video model (the model is a
  mandatory question before starting), then assemble locally with ffmpeg.
  Use when: "replicate this video", "make a video like this", "remake this
  reference", "copy the look and storyboard of this clip", "restyle this
  footage", "이 영상 비슷하게 만들어줘", "이 광고 같은 걸로".
  NOT for: narrated non-photoreal explainers (higgsfield-video-explainer),
  ads with avatars or products (Marketing Studio in higgsfield-generate),
  single-shot text-to-video (higgsfield-generate), or face training
  (higgsfield-soul-id).
argument-hint: "[reference video path] [target duration] [aspect]"
allowed-tools: Bash
---

# Higgsfield Video Replicate

Turn one reference video into a new video with the same look, rhythm, and structure: analyze the reference, lock a shared style bible and character references, generate one clip per shot with the user-chosen reference-capable model, then cut everything together locally with ffmpeg.

## Scope

`creative-production`, when present, is the project-level coordinator; this skill is the reference-replication pipeline specialist. If no coordinator exists (standalone), run the requested replication directly without searching for one. Delegated by a coordinator: continue without calling back — no routing interview, no second approval ledger. One replication implies no extra deliverables, variants, or publication.

## Routing

| Request | Skill |
|---|---|
| Replicate / remake / restyle an existing video | this skill |
| Narrated non-photoreal explainer from a topic or document | `higgsfield-video-explainer` |
| Ad with avatars/products, single-shot clips, images, audio | `higgsfield-generate` |
| Train a real person's face for reuse | `higgsfield-soul-id` |

## Bootstrap

1. If `higgsfield` is unavailable, install it:
   ```bash
   curl -fsSL https://raw.githubusercontent.com/higgsfield-ai/cli/main/install.sh | sh
   ```
2. If `higgsfield account status` fails with `Session expired` / `Not authenticated`, ask the user to run `higgsfield auth login`, then wait.
3. Confirm contracts before the first submission:
   ```bash
   higgsfield model list --json           # candidates for the gate question
   higgsfield model get <chosen jst> --json
   ffmpeg -version                        # Phase 5 assembly requires local ffmpeg
   ```

## Inputs

- Reference video as a local file (ask for a download when only a URL is given).
- Target duration and aspect — default: match the reference.
- Whether the reference's characters/branding may be reused (Hard rule 2).
- Optional: replacement subject, product, or brand for the new version.

## Ask first — model selection (mandatory)

Before Phase 0, ask the user which video model to generate the shots with. Never pick silently; the only exception is the user explicitly delegating the choice — then use `seedance_2_5`. Present the live candidates:

| Model | Video ref | Image refs | Audio ref | Resolution | Choose when |
|---|---|---|---|---|---|
| `seedance_2_5` | yes | ≤30 (≤50 media total) | yes | 480p–1080p | Recommended default: quality + full reference features + `video_edit`/`video_extension` modes + `--draft` |
| `seedance_2_0` | yes | yes | yes | 480p–**4k** | native 4K output is required |
| `gemini_omni` | yes | ≤7 (≤5 with a video ref) | no | 720p only | fast, cheap reference-to-video; default duration 8s |
| other (kling/veo/grok/…) | start_image only | — | — | — | frame-anchor fallback: extract key frames from the reference, animate each with `--start-image`; style match is looser |

Rules:

- Table facts verified against the live schema (`higgsfield model get <jst>`); re-check when the catalog changes.
- The user names a model → use it. If it lacks `video_references`, explain the frame-anchor fallback and get agreement before proceeding.
- Ask the model question alone (one question per turn); duration and aspect default to matching the reference unless the user stated them.
- Record the chosen model for Phases 3, 5, and 6.

## Hard rules

1. Photoreal is allowed and expected. Do NOT apply video-explainer's non-photoreal constraint here.
2. Style transfer, not asset theft: never recreate the reference's real people, logos, or exact on-screen text unless the user owns them. When in doubt, generate replacement branding and generic faces.
3. One clip per shot, within the chosen model's duration range (`seedance_2_5`: 4–30s — verify others with `model get`). Split longer targets into more shots.
4. The STYLE and CHARACTER descriptors repeat byte-identically in every shot prompt.
5. Write all prompts in English; keep beat sheets and analysis in the user's language.
6. When a single soundtrack covers the whole film, pass `--generate-audio false` on every clip and mix in Phase 5. Let a clip carry its own audio only when the beat needs it.
7. Assemble in the same run — returning loose clips is a failure. Local ffmpeg IS allowed here; video-explainer's ffmpeg ban applies only to that pipeline.
8. The model comes from the mandatory gate question. Never silently swap it — if the chosen model is unavailable or fails twice, return to the user with the live catalog (`higgsfield model list`).

## Pipeline

| Phase | Output | Detail |
|---|---|---|
| **Gate** | chosen video model (mandatory question) | Ask first above |
| 0 Analyze | beat sheet + style bible + extracted frames/audio | `references/analysis.md` |
| 1 Lock assets | style donors, character sheets, replacement branding | Phase 1 below |
| 2 Shot prompts | N English prompts sharing STYLE/CHARACTER | `references/prompts.md` |
| 3 Clips | N completed video jobs (gate-chosen model) | Phase 3 below |
| 4 Soundtrack | BGM/SFX plan or adapted reference audio | Phase 4 below |
| 5 Assemble | one final MP4 | `references/assembly.md` |
| 6 QC | beat-by-beat comparison, fixes, optional score | Phase 6 below |

Read `references/analysis.md` before Phase 0, `references/consistency.md` before Phase 1, `references/prompts.md` before Phase 2, and `references/assembly.md` before Phase 5.

## Phase 0 — analyze the reference

Extract frames and audio, then write two documents: a **beat sheet** (timestamp, shot, subject, action, camera, grade, audio per beat) and a **style bible** (medium, lens/DOF, lighting, color grade, motion character, aspect/fps, audio character). From them derive the shot count N and each shot's duration. Recipes and formats: `references/analysis.md`.

## Phase 1 — lock assets

- **Style donors:** 2–4 representative reference frames (composition + grade anchors). Optionally normalize the look into one generated style key.
- **Characters:** follow `references/consistency.md` — reference frames for characters carried over, a generated multi-angle character sheet for new ones. `higgsfield-soul-id` is for a real person the user owns, and only to produce the sheet: `seedance_2_5` has no soul-id parameter (verified), so video consistency always travels as reference images.
- **Branding:** when the reference shows a brand that cannot be reused, generate replacement packaging/logos as stills with `gpt_image_2_5`.

## Phase 2 — shot prompts

Write exactly N English prompts from the template in `references/prompts.md`. STYLE and CHARACTER stay verbatim across shots; each shot carries one clear action completable within its duration. With a video reference attached, the prompt describes the NEW scene and camera — never re-describes the reference's look.

## Phase 3 — generate clips

Generate with the model chosen at the gate. The example shows `seedance_2_5`; for any other model run `higgsfield model get <jst> --json` first and adapt the flags.

```bash
higgsfield generate create seedance_2_5 \
  --mode omni_reference \
  --prompt "<Shot N prompt>" \
  --video-references ./reference.mp4 \
  --image-references ./char_sheet.png \
  --start-image ./shot_N-1_lastframe.png \
  --duration 7 \
  --aspect_ratio 16:9 \
  --resolution 720p \
  --generate-audio false \
  --wait --json
```

Mode guide (`seedance_2_5` verified — other models expose different modes; check `model get`):

| Mode | Use | Rule |
|---|---|---|
| `omni_reference` | new shots in the reference's style — replication default | requires ≥1 reference media |
| `video_edit` | modify the reference clip itself | exactly one `video_references` item |
| `video_extension` | lengthen the reference | ≥1 video reference + `extension_mode` `backward`\|`forward` |
| `t2v` | plain generation | no reference media — never used for replication |

Verified limits for `seedance_2_5`: total reference media ≤ 50 items; images including `start_image`/`end_image` ≤ 30; `start_image`/`end_image` only in `omni_reference`. Short aliases `--video` / `--image` / `--audio` also work. Record every job UUID in shot order. Shots run concurrently within this phase; re-submit only failed shots.

## Phase 4 — soundtrack

Pick one route: (a) pass the reference audio as `--audio-references` when generating clips, (b) extract the reference's track and adapt it, or (c) generate fresh — `seed_audio` for ambience/SFX, `sonilo_music` for BGM. Cue timestamps come from the beat sheet.

## Phase 5 — assemble

Normalize clips → cut in beat order → apply one shared grade → fit and mix audio → loudness-normalize → export. Exact ffmpeg recipes: `references/assembly.md`.

## Phase 6 — QC

Extract a frame at every beat timestamp and compare with the reference frames for composition, grade, and character identity. Regenerate only the failing shots, each time with a changed prompt or re-anchored references (`references/consistency.md`, drift recovery). Two identical failures mean the approach must change, not the prompt. Optional finished-video score:

```bash
higgsfield generate create brain_activity --video ./final.mp4 --wait
```

## Checkpoints and recovery

- Before Phase 3: the gate model question was answered, plus beat sheet, style bible, N prompts, and locked assets all exist; exactly one voice-free plan for audio.
- Before Phase 5: N completed video jobs with exact one-to-one shot order, no missing or duplicate UUIDs.
- `mode 'omni_reference' requires at least one reference media item` → a media flag was dropped; re-add `--video-references`.
- `start_image and end_image are only allowed for mode 'omni_reference'` → fix the mode, do not remove the anchors.
- `Unknown params: <flag>` → run `higgsfield model get <chosen jst> --json`; never guess flag names.
- Character/wardrobe drift → `references/consistency.md` drift recovery section.
- Timeout → `higgsfield generate wait <job_id> --json`; never duplicate a running job.
- Pre-existing suite skills (`higgsfield-generate`, `higgsfield-video-explainer`) stay untouched by this pipeline's failures — their contracts are independent.

## Deliver

The final MP4 (local path or uploaded URL), exact duration, aspect, model and shot count, soundtrack source, QC notes, and a one-line comparison against the reference. Keep intermediate job IDs and loose asset URLs internal unless asked.
