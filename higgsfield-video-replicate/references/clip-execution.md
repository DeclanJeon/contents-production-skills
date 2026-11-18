# Replication clip, soundtrack, assembly and recovery execution

Read before the assigned clip/soundtrack/QC phase; this is not needed for intake or reference-only analysis. Scope, model-selection gate, bounded aggregate approval and dependent native-reference gates remain in [SKILL](../SKILL.md). Current contracts override all historical example limits. `references/` recipe paths below are skill-root relative.

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

Verified limits for `seedance_2_5` (historical — re-check `model get`): total reference media ≤ 50 items; images including `start_image`/`end_image` ≤ 30; `start_image`/`end_image` only in `omni_reference`. Short aliases `--video` / `--image` / `--audio` also work. Record every job UUID in shot order. **Only continuity-independent shots may submit concurrently.** A shot inheriting predecessor/history state is dependency-ordered even with a new angle or its own storyboard start image: wait for the accepted source range, actual inspection and validated native handoff. Same-angle frame chaining additionally uses the approved extracted anchor (see `references/consistency.md`). Re-submit only failed shots, inside the approved retry bound.

## Phase 4 — soundtrack

Pick one route: (a) pass the reference audio as `--audio-references` when generating clips, (b) extract the reference's track and adapt it, or (c) generate fresh — `seed_audio` for ambience/SFX, `sonilo_music` for BGM. Cue timestamps come from the beat sheet.

## Phase 5 — assemble

Normalize clips → cut in beat order → apply one shared grade → fit and mix audio → loudness-normalize → export. Exact ffmpeg recipes: `references/assembly.md`.

## Phase 6 — QC

Extract a frame at every beat timestamp and compare with the reference frames for composition, grade, and character identity. Regenerate only the failing shots, each time with a changed prompt or re-anchored references (`references/consistency.md`, drift recovery) and always inside the approved retry bound. Two identical failures mean the approach must change, not the prompt. Optional finished-video score — a separate authorized operation (include it in the approved scope or skip it):

```bash
higgsfield generate create brain_activity --video ./final.mp4 --wait
```

## Checkpoints and recovery

- Before Phase 3: the model was resolved (supplied or asked), plus beat sheet, style bible, N prompts, and locked assets all exist; exactly one voice-free plan for audio; and the aggregate quote was approved at the package gate.
- Before Phase 5: N completed video jobs with exact one-to-one shot order, no missing or duplicate UUIDs.
- `mode 'omni_reference' requires at least one reference media item` → a media flag was dropped; re-add `--video-references`.
- `start_image and end_image are only allowed for mode 'omni_reference'` → fix the mode, do not remove the anchors.
- `Unknown params: <flag>` → run `higgsfield model get <chosen jst> --json`; never guess flag names.
- Character/wardrobe drift → `references/consistency.md` drift recovery section.
- Timeout → `higgsfield generate wait <job_id> --json`; never duplicate a running job.
- Pre-existing suite skills (`higgsfield-generate`, `higgsfield-video-explainer`) stay untouched by this pipeline's failures — their contracts are independent.

