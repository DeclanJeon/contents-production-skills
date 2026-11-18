---
name: higgsfield-video-replicate
version: 0.36.0
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

`creative-production`, when present, is the project-level coordinator; this skill is the reference-replication pipeline specialist. If no coordinator exists (standalone), run the requested replication directly without searching for one. Delegated by a coordinator: continue without calling back — no routing interview, no second approval ledger; consume the assigned input IDs/versions and return the canonical output join per `../higgsfield-generate/references/package-gate.md` (per-shot job UUIDs are provider locators mapped to canonical shot/asset IDs; a job UUID is never a `result_asset_id`). One replication implies no extra deliverables, variants, or publication.

**REQUIRED for dependent video generation, including standalone execution:** apply the [whole-storyline continuity gate](../video-production-assets/references/26-state-causality-continuity.md#storyline-continuity-gate). Before submission, inspect the accepted predecessor's actual selected source range/end frame and relevant history across inserts, reappearances and timeline changes; resolve current character/location/prop/look asset versions. New angles inherit state while using the current approved composition, not a forced copy of the old camera.

**REQUIRED:** use [sequence execution and pre-generation AV handoff](../video-production-assets/references/sequence-execution.md#3a-영상오디오-인계와-실제-호출-패킷--필수) for these dependent shots even in standalone mode: bind accepted predecessor visual/audio context and relevant history/asset state to the actual native selected references and submitted prompt, prepare the validated request, then audit the actual call. Missing/unverified evidence, unsupported reference inputs or an unregistered transport block dependent submission; CLI examples below do not bypass this gate. First shots/new voices need no nonexistent predecessor; explicit silence and approved editorial audio remain scoped by the canonical gate. Independent shots may run concurrently only after their lack of predecessor/history-state dependencies is established; changing angle or inserting another shot does not establish independence.

## Package gate

Apply `../higgsfield-generate/references/package-gate.md` before Phase 3 and before any paid auxiliary stage: runtime check (never auto-install; missing ffmpeg is a reported blocker), eligible operation, and ONE verified aggregate quote covering all N shot clips + soundtrack + approved retries + any authorized analysis — approved before submission. Eligible here: video generation, audio generation, `brain_activity` analysis (a separate authorized operation — include it in scope or omit it). **Higgsfield image generation/editing (character sheets, branding stills, style keys, Soul renders) is ineligible in this package** — Phase 1 uses extracted reference frames, supplied stills, or the authorized eligible image executor only.

## Routing

| Request | Skill |
|---|---|
| Replicate / remake / restyle an existing video | this skill |
| Narrated non-photoreal explainer from a topic or document | `higgsfield-video-explainer` |
| Ad with avatars/products, single-shot clips, images, audio | `higgsfield-generate` |
| Train a real person's face for reuse | `higgsfield-soul-id` |

## Bootstrap

1. If `higgsfield` is unavailable or `higgsfield account status` fails with `Session expired` / `Not authenticated`, report the blocker — ask the user to run `higgsfield auth login`, then wait. Never install automatically; installation is a separate explicit user request. A missing local `ffmpeg` is likewise a reported Phase 5 blocker, not a silent install.
2. Confirm contracts before the first submission:
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

## Ask first — model selection

Before Phase 0, resolve which video model generates the shots. Reuse a supplied choice: a user-named model or an approved model in the delegated brief is validated against the live schema and recorded — no question. Ask only when unresolved; the only silent path is the user explicitly delegating the choice — then use `seedance_2_5`. Present the live candidates:

Historical comparison tables are archived in [model-catalog](../higgsfield-generate/references/model-catalog.md#historical-replication-model-comparison); use the current list/schema for the actual choice.

Rules:

- Table facts are historical documentation; re-check against the live schema (`higgsfield model get <jst>`) at execution.
- The user names a model → use it. If it lacks `video_references`, explain the frame-anchor fallback and get agreement before proceeding.
- Ask the model question alone (one question per turn); duration and aspect default to matching the reference unless the user stated them.
- Record the chosen model for Phases 3, 5, and 6.

## Hard rules

1. Photoreal is allowed and expected. Do NOT apply video-explainer's non-photoreal constraint here.
2. Style transfer, not asset theft: never recreate the reference's real people, logos, or exact on-screen text unless the user owns them. When in doubt, use replacement branding and generic faces — produced by the authorized eligible image executor (`codex-imagen` default) or extracted/supplied stills, not a Higgsfield image job (ineligible here).
3. One clip per shot, within the chosen model's duration range (`seedance_2_5`: 4–30s — verify others with `model get`). Split longer targets into more shots.
4. The STYLE and CHARACTER descriptors repeat byte-identically in every shot prompt.
5. Write all prompts in English; keep beat sheets and analysis in the user's language.
6. When a single soundtrack covers the whole film, pass `--generate-audio false` on every clip and mix in Phase 5. Let a clip carry its own audio only when the beat needs it.
7. Assemble in the same run — returning loose clips is a failure. Local ffmpeg IS allowed here; video-explainer's ffmpeg ban applies only to that pipeline.
8. The model comes from the resolved gate decision (supplied or asked). Never silently swap it — if the chosen model is unavailable or fails twice, return to the user with the live catalog (`higgsfield model list`).

## Pipeline

| Phase | Output | Detail |
|---|---|---|
| **Gate** | chosen video model (supplied or asked) | Ask first above |
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

- **Style donors:** 2–4 representative reference frames (composition + grade anchors). Optionally normalize the look into one style key — via the authorized eligible image executor only; a Higgsfield image key is ineligible here.
- **Characters:** follow `references/consistency.md` — extracted reference frames for characters carried over, or a multi-angle character sheet for new ones produced by the authorized eligible image executor / supplied stills. `higgsfield-soul-id` is a separate explicitly-authorized real-person training lifecycle — never auto-invoked here; its downstream sheet renders are image jobs (ineligible in this package). `seedance_2_5` has no soul-id parameter, so video consistency always travels as reference images.
- **Branding:** when the reference shows a brand that cannot be reused, produce replacement packaging/logos as stills via the authorized eligible image executor (the preserved `gpt_image_2_5` recipe is craft/reference only — ineligible here).

## Phase 2 — shot prompts

Write exactly N English prompts from the template in `references/prompts.md`. STYLE and CHARACTER stay verbatim across shots; each shot carries one clear action completable within its duration. With a video reference attached, the prompt describes the NEW scene and camera — never re-describes the reference's look.

For a requested production/detailed storyboard, complete sheet or full preproduction package, REQUIRED: apply [the complete storyboard contract](../video-production-assets/references/storyboard-contract.md) through `creative-production` before this video-prompt phase. Carry approved synopsis beat/scene/shot/panel IDs, clean start/peak/end images, spatial/camera/VFX/speech/audio requirements and image-only review evidence into each shot. Preserve the supplied reference's inspected scope and authorized adaptation; a reference beat sheet or style match alone is not full visual-story acceptance. Keep already-approved narrow execution scoped; this pointer never authorizes images, extra clips or spend.


## Phases 3–6 — execute the assigned phase

Before generating clips, choosing/executing soundtrack or beat-level QC/repair, read [clip execution](references/clip-execution.md). It owns exact model modes/commands, per-shot UUID ordering, dependency-aware concurrency, soundtrack, assembly checkpoints and unknown-outcome recovery. Phase 5 additionally requires [assembly](references/assembly.md). No loose clips as completion, no duplicate pending submission, no retry outside approved scope.

## Deliver

The final MP4 (local path or uploaded URL), exact duration, aspect, model and shot count, soundtrack source, QC notes, and a one-line comparison against the reference. Keep intermediate job IDs and loose asset URLs internal unless asked. For delegated production work, additionally return the internal canonical join: output file path + hash, per-shot job UUID locators mapped to canonical shot IDs, chained-frame anchor provenance, observed terminal states, and measured cost.

## Acceptance

The replication is complete only when the reference was actually inspected over the reported scope, the user-selected or supplied model was schema-checked and used without silent substitution, all N shot jobs completed in order, the final MP4 was assembled and opened, and beat-level QC reports observed matches and deviations. Aggregate cost approval must cover submitted work and retries. Missing reference media, unauthorized likeness/branding, unavailable model, failed assembly, or uninspected output is a blocker; loose clips are not a finished replication.
