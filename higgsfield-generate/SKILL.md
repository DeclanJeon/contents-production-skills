---
version: 0.17.0
name: higgsfield-generate
description: |
  Generate videos/3D assets/audio via Higgsfield AI (image
  branches are craft/reference only under package image
  exclusion). Defaults: Seedance 2.5 for video, Marketing
  Studio for ads, Seed Audio 1.0 for audio.
  Use when: "generate an image", "make a video", "animate
  this photo", "image-to-video", "edit/stylize/remix this
  image", "reframe this video", "edit this video from a
  sketch", "create a 3D model/GLB", "create a sound effect",
  "make music", "text-to-audio", "create an ad", "make a UGC
  video", "unboxing", "presenter video", "import product from
  URL", or "analyze video virality". Supports generic generation,
  workflows, Marketing Studio, and Virality Predictor.
  Chain with higgsfield-soul-id for face/identity consistency.
  NOT for: Soul training, brand systems/brandbooks (use
  higgsfield-brandkit), photoshoots, cards, YouTube thumbnails
  (use higgsfield-youtube-thumbnail), explainers (use
  higgsfield-video-explainer), replicating or remaking an existing
  reference video (use higgsfield-video-replicate), playable
  games/assets (use higgsfield-websites), or TTS.
argument-hint: "[prompt-or-analysis-request] [--model <name>] [--image|--video <path-or-id>]"
allowed-tools: Bash
---

# Higgsfield Generate

Submit jobs to any Higgsfield model. Wraps the `higgsfield` CLI. Covers generic image/video/3D/audio generation, Marketing Studio (branded ads, avatars, products, hooks, settings), and, secondarily, Virality Predictor video scoring.

## Scope

`creative-production` is the sole project-level coordinator for content/video production; this skill is the Higgsfield generation executor. Standalone invocation: consult `creative-production` once for scope/route when the request is part of a larger content effort, then run only the requested generation. Delegated by `creative-production`: proceed without calling back — no recursive routing, second interview, or new approval ledger; consume the assigned input IDs/versions and return the canonical output join per `references/package-gate.md`. A single generation request implies no folder selection, project manifest, thumbnail, CTA, extra variants, or publication beyond the requested artifact. Named preset slash commands and MCP tool routes keep their own contracts.

## Package gate

Before ANY actual submission, apply the shared gate in `references/package-gate.md`: runtime check (no auto-install — report missing, install only on an explicit separate request), eligible operation, verified quote, bounded approval, current input versions, reuse of supplied choices. Eligible here: video, audio, 3D, workflow, and analysis jobs on the live schema. **Higgsfield image generation/editing is excluded by package policy — image model branches are craft/reference only** (`references/image-branches.md`); a missing image goes to the explicitly authorized eligible image executor (`codex-imagen` default), never to a silent fallback.

## Step 0 — Runtime check

Before any other command:

1. If `higgsfield` is not on `$PATH` or `higgsfield account status` fails with `Session expired` / `Not authenticated`, report the blocker and ask the user to run `higgsfield auth login` (interactive) or — only if they explicitly request installation — the official installer in `references/package-gate.md`. Never install automatically.
2. Inspect the live contract before submission: `higgsfield model get <jst> --json` for the chosen model, `higgsfield model list --json` when routing is uncertain.

## UX Rules

1. Be concise. No raw IDs, no JSON dumps in chat. Print the media URL for generated assets, or the text summary for Virality Predictor.
2. No internal jargon in user-facing chat. Cost/quote mechanics still happen — silently, at the package gate.
3. Detect the user's language from the first message and reply in it. Technical args (`--aspect_ratio 16:9`) stay English.
4. Don't batch-ask. Reuse every supplied choice; ask one thing at a time only for genuinely missing decisions.
5. Prefer the quality-first default inside the approved bounded scope. Cost status and aggregate quote are resolved at the package gate BEFORE submission — never submit on unverified or unapproved cost, and never add unrequested variants for cheapness or quality.
6. Pass `--wait` to `generate create` so the command blocks until done and prints the result URL itself. Avoid the two-step `create` → `wait` pattern.

## Discovery guardrail

When looking for a Higgsfield feature/model, do not rely only on semantic search or CLI `--help`. First run an unfiltered model list, then inspect likely `job_set_type` names. If the user says a model exists but search returns no results, trust that signal and verify with the full model list before answering.

Workflows are separate from models. Discover them with `higgsfield workflow list` and inspect params with `higgsfield workflow get <workflow_name>`.

Virality Predictor is exposed as:

- Customer-facing name: Virality Predictor
- Technical `job_set_type`: `brain_activity`
- Category/output: text report. This is video-in/text-out analysis, not a text/chat generation model.
- Input: uploaded video
- Purpose: finished-video hook, attention, retention, and virality analysis

If the user says "analyze this video", "score this ad", "evaluate the hook", or similar, route to `brain_activity` even though it appears under text/analysis models. Classify by task intent and required input, not by output category alone.

## Workflow — generic generation

1. **Pick a model.** Start with the core defaults:

   - Image-model defaults (GPT Image 2.5, Nano Banana 2, etc.) → craft/reference only; see `references/image-branches.md` — ineligible in this package.
   - **Seedance 2.5** (`seedance_2_5`) → SOTA default video model for serious motion, cinematic clips, multi-shot work, and image-to-video. Supports 4–30s output up to 1080p; use Seedance 2.0 when native 4K is required.
   - **Marketing Studio** → default for ads, UGC, product demos, unboxing, TV spots, presenter videos, and brand/product workflows.
   - **Seed Audio 1.0** → default audio model for text-to-audio, voice, sound effects, ambience, foley, and music-like audio unless the user names Sonilo/Mirelo.

   Only the models below are picked without being asked. Any other model is used only when the user names it or explicitly asks for what it offers (cheaper, faster, a specific look); see `references/model-catalog.md`. A model the user names stays in use for follow-ups on the same work.

   **Image:** Higgsfield image generation/editing is ineligible in this package — the model selection craft lives in `references/image-branches.md` for routing and non-package contexts. Route specialized image requests to their owners (brandkit, youtube-thumbnail, product-photoshoot, marketplace-cards, soul-id); a missing generic image goes to the authorized eligible image executor (`codex-imagen` default) with truthful scope, never to a Higgsfield image fallback.

   **Video:**
   - Complete narrated explainer from a topic, story, or document → use `higgsfield-video-explainer`, not generic video generation.
   - Replicate, remake, or restyle an existing reference video into a new multi-shot video → use `higgsfield-video-replicate`, not generic video generation.
   - All advertising / commercial / branded ad video → Marketing Studio (see Marketing Studio below)
   - Edit existing video from sketch/timestamp, or reframe to another aspect ratio → workflow (`draw_to_video` or `reframe`), not a model. See `references/workflows.md`.
   - **Default for everything else → Seedance 2.5** (`seedance_2_5`): multi-shot, consistent identity, motion-heavy, image-to-video, editing, extension, 4–30s. Modes `t2v` / `omni_reference` / `video_edit` / `video_extension`; use `omni_reference` for reference inputs, including start/end frames; `t2v` accepts no media. Up to 1080p. Do not downgrade because another model's schema looks simpler.
   - User asks for 4K → Seedance 2.0 (`seedance_2_0`); say why you switched.
   - User asks for cheaper or faster → Kling 3.0 Turbo (`kling3_0_turbo`), Veo 3.1 Lite, or Seedance 1.5 Pro.
   - Named by the user → use it, e.g. Cinema Studio 4.0 (`cinematic_studio_video_4_0`), Kling 3.0, Veo 3.1, Gemini Omni Flash (`gemini_omni`), or Grok Video 1.5 (`grok_video_v15`: one `--start-image` or `--image`, duration 2–15s, up to `1080p` without reference media).

   **Video analysis:**
   - Rate a finished video's hook, virality potential, attention, retention, or distraction risk → Virality Predictor (`brain_activity`). This is a video analysis model that returns a text score/report, not a generated media asset.

   **3D:**
   - A 3D asset within a playable game or game-wide asset system → use `higgsfield-websites` (game product type).
   - Create an actual 3D mesh/model/GLB from one or more object/product reference images → Multi-Image to 3D (`multi_image_to_3d`). Pass 1–4 images with repeated `--image`; use `--should_texture true` when the asset needs texture. If the user only asks for a 3D-rendered *picture*, that's an image job — authorized eligible executor, never a Higgsfield image model.

   **Audio:**
   - **Default for audio generation → Seed Audio 1.0 (`seed_audio`).** Use for text-to-audio, sound effects, ambience, foley, impacts, environmental audio, voice-style generations, and music-like audio. It requires `--prompt`; use optional `--audio-references`/`--image-references` only when the user provides references.
   - Use Sonilo Music (`sonilo_music`) only when the user explicitly asks for Sonilo or you need that specialist music model. It requires `--prompt` and `--duration`, and returns audio.
   - Use Mirelo Text to Audio (`mirelo_text_to_audio`) only when the user explicitly asks for Mirelo or you need that legacy SFX model. It requires `--prompt` and `--duration`, and returns audio.

   For the actual `--model` ID to pass to `higgsfield generate create`, run `higgsfield model list --json | jq` to map display names to IDs. See `references/model-catalog.md` for the full table; image-only rows are craft/reference (ineligible here).

2. **Pass media inputs straight to flags.** Media flags accept a local file path **or** a UUID. CLI auto-uploads paths and auto-detects job vs upload for UUIDs. No need to pre-upload. Each model declares accepted media roles or `*_references` params — see `references/media-inputs.md`.
3. **Validate quickly.** If unsure of params, run `higgsfield model get <jst> --json` once and pass only what's needed. Validate the preferred model before falling back to an older one. Use schema defaults otherwise. The server returns `adjustments` for non-fatal coercions (e.g. `aspect_ratio=99:99` → closest match) and a structured error for invalid declared-param values.
4. **Submit and wait in one shot.** `higgsfield generate create <jst> [--prompt "..."] [media flags] [param flags] --wait`. Blocks until terminal status and prints the result on stdout. Tunables: `--wait-timeout 20m` (default 10m), `--wait-interval 5s` (default 3s). Virality Predictor does not need a prompt; pass `--video`.
5. **Deliver.** For generated media and 3D assets, send the primary result URL plus a one-line summary (model, duration if video; GLB/asset URL for 3D). For Virality Predictor, deliver the scores, business interpretation, and the Open report link. Do not surface Virality Predictor `.glb`, `.bin`, or region-table internals in normal chat output.

To inspect or rerun later, `higgsfield generate list --json` and `higgsfield generate get <id> --json` work for retrospection. `higgsfield generate wait <id>` is still available if you ever need to rejoin a job started without `--wait`.

For workflow jobs, use `higgsfield generate workflow <workflow_name> ... --wait`. Cost syntax is `higgsfield generate cost workflow <workflow_name> ...`. See `references/workflows.md`.

## Media flags

| Flag | Purpose | Models that accept it |
|---|---|---|
| `--image <path-or-id>` | reference image | most image models, `grok_video_v15`, `multi_image_to_3d`, `seedance_2_0`, `seedance_2_5`, `veo3`, `marketing_studio_video` |
| `--start-image <path-or-id>` | first frame for image-to-video transitions | `grok_video_v15`, `kling3_0`, `kling3_0_turbo`, `kling2_6`, `veo3_1`, `seedance_2_0`, `seedance_2_5`, `marketing_studio_video` |
| `--end-image <path-or-id>` | last frame for transitions | `kling3_0`, `seedance_2_0`, `seedance_2_5`, `marketing_studio_video` |
| `--video <path-or-id>` | reference or analyzed video | `seedance_2_0`, `seedance_2_5`, `brain_activity` |
| `--audio <path-or-id>` | reference audio (lipsync, soundtrack match) | `seedance_2_0`, `seedance_2_5` (reference input; distinct from generating output audio) |

For reference-array models, the explicit flags are `--image-references`, `--video-references`, and `--audio-references`; `--image`, `--video`, and `--audio` are short aliases when the schema exposes those params.

Each flag accepts either a local file path (auto-uploaded) or a UUID (upload id from `higgsfield upload create`, or a previous job id). Each model declares its own media roles or `*_references` params. See `references/media-inputs.md` for the full table.

## Common params

Flags pass through to model schema. Use `higgsfield model get <jst>` to discover.

```bash
higgsfield generate create seedance_2_5 --prompt "camera dollies in" --mode omni_reference --start-image ./first.png --duration 12 --resolution 1080p --wait
higgsfield generate create grok_video_v15 --prompt "cinematic handheld shot, neon rainy street" --start-image ./image.png --duration 5 --resolution 720p --wait
higgsfield generate create multi_image_to_3d --image ./front.png --image ./side.png --should_texture true --wait
higgsfield generate create seed_audio --prompt "cinematic rain ambience with distant thunder" --wait
higgsfield generate create sonilo_music --prompt "cinematic synthwave track" --duration 12 --wait
higgsfield generate create mirelo_text_to_audio --prompt "glass breaking in a large hall" --duration 4 --wait
higgsfield generate create brain_activity --video ./ad.mp4 --wait
```

For machine-readable output (chained pipelines, agent context), add `--json`. With `--wait --json` you get the final job object array. Without `--wait`, you get the job IDs. Virality Predictor stores raw analysis and render artifacts in the job params, but the default text output should stay to scores plus Open report.

Stdin prompt: `echo "..." | higgsfield generate create <jst> --wait`.


## Marketing Studio

Branded ad generation: avatars + products + hooks/settings + ad-style modes on `marketing_studio_video` (eligible video output). `marketing_studio_image` is an image job — ineligible in this package. Load `references/marketing-studio.md` before any Marketing Studio work: concepts (avatar/product/webproduct/hook/setting/ad reference/brand kit/ad format), discovery commands, mutual-exclusion rules, the quick-ad-video and Click-to-Ad workflows, and per-mode contract details.

## Virality Predictor video scoring

Use Virality Predictor (`brain_activity`) when the user wants to evaluate a finished video as a business creative: hook strength, virality potential, attention, retention, or how well the content/product holds focus and minimizes distraction. Treat "Virality Predictor" as the customer-facing feature name; `brain_activity` is only the CLI/job_set_type.

```bash
higgsfield generate create brain_activity --video ./creative.mp4 --wait
```

The result is text, not a generated image/video. Report the overall score, peak hook second, sustain score, strongest/weakest regions, and report URL if present. Interpret it as an objective attention proxy for creative testing: higher Visual/Auditory/Language/Attention scores suggest stronger stimulus and focus; lower Default Mode is better because it suggests less mind-wandering.

The CLI prints an Open report URL like `https://<app-domain>/apps/virality-predictor?resultJobId=<job_id>`. Send that URL for the visual report. Raw artifact URLs such as `brain_example_url`, `vertexMapBinaryUrl`, and `vertexMapUrl` are implementation details; mention them only when the user asks for raw data or implementation details.

Good final shape:

```text
Overall score: 44/100
Peak hook: 49% at 1s
Sustain: 89%
Strongest region: Visual Cortex
Risk: Default Mode is high, which can indicate mind-wandering.

Open report: <report_url>
```

## Errors

- `Missing required params: prompt` → user gave no prompt; ask for it.
- `Missing required params: medias` on `brain_activity` / Virality Predictor → pass exactly one video via `--video <path-or-id>`.
- `Invalid values: aspect_ratio=99:99 (allowed: ...)` → bad enum; pick from allowed.
- `Unknown params: foo` → schema doesn't accept that flag; check `higgsfield model get <jst>`. If this happens for `hook_id` or `setting_id`, the selected model/job_set_type does not support Marketing Studio setup items.
- `Session expired` → `higgsfield auth login`.

See `references/troubleshooting.md` for more.

## Reference docs

Load on demand:

- `references/package-gate.md` — REQUIRED before any submission: runtime check, execution eligibility, bounded approval, canonical handoff join
- `references/image-branches.md` — image model routing/taxonomy/CLI craft (ineligible in this package)
- `references/marketing-studio.md` — Marketing Studio concepts, entities, modes, ad workflows
- `references/model-catalog.md` — picking the right model for the task
- `references/workflows.md` — `draw_to_video` and `reframe` workflow generation
- `references/prompt-engineering.md` — writing prompts that work
- `references/media-inputs.md` — image/video/audio reference flows and Virality Predictor video analysis
- `references/troubleshooting.md` — common errors and fixes
- `references/marketing-avatars.md` — preset vs custom avatars
- `references/marketing-products.md` — URL fetch vs manual product create
- `references/marketing-setup-items.md` — hooks/settings discovery and usage
- `references/marketing-ad-references.md` — ad reference videos (create/list/get)
- `references/marketing-brand-kits.md` — brand kits (fetch from URL, list, get)
- `references/marketing-dtc-ads.md` — DTC Ads Engine (`dtc-ads generate`)
- `references/marketing-modes.md` — every Marketing Studio mode
