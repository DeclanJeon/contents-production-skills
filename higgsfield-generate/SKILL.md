---
version: 0.36.1
name: higgsfield-generate
description: |
  Generate requested video/3D/audio assets for video production via Higgsfield AI.
  Image branches remain craft/reference only under the package image exclusion.
  Routing cues only: discover the current model and verify its schema
  before selecting any model. Do not treat cached defaults as capability
  or quality claims.
  Use for video generation, photo animation, image-to-video, reframing,
  sketch edits, 3D/GLB, music/SFX, ads/UGC, unboxing, presenters,
  product-URL video workflows, or virality analysis.
  Supports generic generation, workflows, Marketing Studio, and Virality Predictor.
  Chain with higgsfield-soul-id for face/identity consistency.
  NOT for: Soul training, brand systems/brandbooks (use
  higgsfield-brandkit), photoshoots, cards, YouTube thumbnails
  (use higgsfield-youtube-thumbnail), explainers (use
  higgsfield-video-explainer), replicating or remaking an existing
  reference video (use higgsfield-video-replicate), playable
  games/websites, standalone images/social operations, or TTS.
argument-hint: "[prompt-or-analysis-request] [--model <name>] [--image|--video <path-or-id>]"
allowed-tools: Bash
---

# Higgsfield Generate

Submit jobs to any Higgsfield model. Wraps the `higgsfield` CLI. Covers generic image/video/3D/audio generation, Marketing Studio (branded ads, avatars, products, hooks, settings), and, secondarily, Virality Predictor video scoring.

Evidence scope: cached IDs, limits, examples, role tables and backend/quality claims are historical/unverified until checked against the selected live contract. [Historical source/read scope](references/model-catalog.md#historical-entrypoint-examples-and-media-flags) preserves the documentation evidence; CLI/MCP transports differ and documentation is not an exercised job.

## Scope

`creative-production` is the sole project-level coordinator for content/video production; this skill is the Higgsfield generation executor. Standalone invocation: consult `creative-production` once for scope/route when the request is part of a larger content effort, then run only the requested generation. Delegated by `creative-production`: proceed without calling back — no recursive routing, second interview, or new approval ledger; consume the assigned input IDs/versions and return the canonical output join per `references/package-gate.md`. A single generation request implies no folder selection, project manifest, thumbnail, CTA, extra variants, or publication beyond the requested artifact. Named preset slash commands and MCP tool routes keep their own contracts.

**REQUIRED for dependent video generation, including standalone execution:** apply the [whole-storyline continuity gate](../video-production-assets/references/26-state-causality-continuity.md#storyline-continuity-gate). Before submission, inspect the accepted predecessor's actual selected source range/end frame and relevant history across inserts, reappearances and timeline changes; resolve current character/location/prop/look asset versions. New angles inherit state while using the current approved composition, not a forced copy of the old camera.

**REQUIRED:** use [sequence execution and pre-generation AV handoff](../video-production-assets/references/sequence-execution.md#3a-영상오디오-인계와-실제-호출-패킷--필수) for these dependent shots even in standalone mode: bind accepted predecessor visual/audio context and relevant history/asset state to the actual native selected references and submitted prompt, prepare the validated request, then audit the actual call. Missing/unverified evidence, unsupported reference inputs or an unregistered transport block dependent submission; CLI examples below do not bypass this gate. First shots/new voices need no nonexistent predecessor; explicit silence and approved editorial audio remain scoped by the canonical gate. Independent shots may run concurrently only after their lack of predecessor/history-state dependencies is established; changing angle or inserting another shot does not establish independence.

## Package gate

Before ANY actual submission, apply the shared gate in `references/package-gate.md`: runtime check (no auto-install — report missing, install only on an explicit separate request), eligible operation, verified quote, bounded approval, current input versions, reuse of supplied choices. Eligible here: video, audio, 3D, workflow, and analysis jobs on the live schema. **Higgsfield image generation/editing is excluded by package policy — image model branches are craft/reference only** (`references/image-branches.md`); a missing image goes to the explicitly authorized eligible image executor (`codex-imagen` default), never to a silent fallback.

## Step 0 — Runtime check

When actual eligible Higgsfield execution is requested, before its commands (not during text-only preparation):

1. If `higgsfield` is not on `$PATH` or `higgsfield account status` fails with `Session expired` / `Not authenticated`, report the blocker and ask the user to run `higgsfield auth login` (interactive) or — only if they explicitly request installation — the official installer in `references/package-gate.md`. Never install automatically.
2. Inspect the live contract before submission: `higgsfield model get <jst> --json` for the chosen model, `higgsfield model list --json` when routing is uncertain.

## UX Rules

1. Be concise. No raw IDs, no JSON dumps in chat. Print the media URL for generated assets, or the text summary for Virality Predictor.
2. No internal jargon in user-facing chat. Cost/quote mechanics still happen — silently, at the package gate.
3. Detect the user's language from the first message and reply in it. Technical args (`--aspect_ratio 16:9`) stay English.
4. Don't batch-ask. Reuse every supplied choice; ask one thing at a time only for genuinely missing decisions.
5. Prefer the current schema fit and the user's stated priorities over any cached route label. Resolve eligibility and aggregate quote before submission; never submit on unverified or unapproved cost, and never add unrequested variants.
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

1. Discover candidates with `higgsfield model list --json` and inspect the exact selected ID with `higgsfield model get <jst> --json`. User choices are preserved; unresolved choices need only decision-changing questions. Never infer capability, resolution, duration, modes, roles, quality, speed or cost from [historical model notes](references/model-catalog.md).
2. Route complete narrated explainers to `higgsfield-video-explainer`, reference remakes to `higgsfield-video-replicate`, branded ad video to Marketing Studio only if its current contract supports it, sketch/timestamp edits and reframes to [workflows](references/workflows.md), and finished-video scoring to `brain_activity`. Playable-game assets belong to `higgsfield-websites`; actual mesh/GLB is 3D, a rendered picture is still an image job. Audio categories require their exact current schema.
3. Image models remain ineligible here. Specialized image owners retain their craft; missing stills go to the explicitly authorized eligible executor (`codex-imagen` default). No unsupported-model or provider fallback.
4. At actual media binding, read [media inputs](references/media-inputs.md): CLI paths may auto-upload; IDs and role/array params depend on the exact transport/schema. Upload requires authority. Pass only the selected model's declared fields.
5. After the package gate, submit the bounded eligible job with `higgsfield generate create <jst> [--prompt "..."] [media/param flags] --wait`. Historical parameter/media examples are in [model-catalog](references/model-catalog.md), not current defaults. Use `--json` for machine-readable joins; analysis uses the declared video input, not an invented text prompt.
6. Deliver only the terminal accessible result and canonical join, or the actually returned analysis report. Unknown timeout is not failure: reconcile the original job with `generate get/wait` before any retry; no absent URL or lost ID proves no job exists. For workflows, use the live workflow contract and [workflow guide](references/workflows.md), including its verified quote.

## Marketing Studio

Branded ad generation: avatars + products + hooks/settings + ad-style modes on `marketing_studio_video` (eligible video output). `marketing_studio_image` is an image job — ineligible in this package. Load `references/marketing-studio.md` before any Marketing Studio work: concepts (avatar/product/webproduct/hook/setting/ad reference/brand kit/ad format), discovery commands, mutual-exclusion rules, the quick-ad-video and Click-to-Ad workflows, and per-mode contract details.

## Virality Predictor video scoring

Use Virality Predictor (`brain_activity`) when the user wants to evaluate a finished video as a business creative: hook strength, virality potential, attention, retention, or how well the content/product holds focus and minimizes distraction. Treat "Virality Predictor" as the customer-facing feature name; `brain_activity` is only the CLI/job_set_type.

```bash
higgsfield generate create brain_activity --video ./creative.mp4 --wait
```

The result is an analysis report, not generated image/video. Report only fields actually returned, including the overall score, peak hook second, sustain score, regions, and report URL when present. Treat scores and brain-region labels as provider predictions/proxies, not measured audience response, neurological diagnosis, or a guarantee of retention or virality. Keep provider interpretation separate from observed business outcomes.

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
- `references/model-catalog.md` — historical routing notes only; verify candidates and capabilities against the live schema
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

## Acceptance

A generation request is complete only when the selected operation is eligible under the package gate, its model/input contract and aggregate quote are verified, the user’s bounded approval covers submission and retries, and the terminal result is recorded with its canonical asset join. Higgsfield image generation remains ineligible here; route to the authorized image executor or report the requested result blocked. Analysis requests return the observed report, not generated media.
