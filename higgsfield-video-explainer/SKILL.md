---
version: 0.37.0
name: higgsfield-video-explainer
description: |
  Build a complete non-photoreal narrated explainer or story video from
  ordered 10-second blocks: one narrator, one universal style key, one Seed
  Audio take and one Gemini Omni clip per block, then server-side assembly
  with explainer_video. Use when: "make an explainer video", "explain this in
  a video", "turn this topic or document into a narrated video", "tell this
  story as an animated video", "make a faceless narrated video", or "show me
  explainer styles". Supports live CMS presets, custom style references,
  mascot/faceless modes, two aspects, and optional burned subtitles. NOT for:
  photoreal films, ads/UGC, talking heads, podcasts, motion typography reels,
  one-off clips without narration, editing a finished video, or
  replicating an existing reference video (use higgsfield-video-replicate).
argument-hint: "[topic or source files] [duration] [language] [aspect ratio]"
allowed-tools: Bash
---

# Higgsfield Video Explainer

Run the MCP video-explainer workflow through Higgsfield CLI. Lock one visual style key, write one narration line and one matching visual prompt per 10-second block, generate every voice take first, generate every clip second, then immediately assemble the ordered pairs with `explainer_video`.

## Scope

`creative-production` is the sole project-level coordinator for content/video production; this skill is the narrated-explainer pipeline specialist. Standalone invocation: consult `creative-production` once for scope/route, then run only the requested explainer. Delegated by `creative-production`: continue without calling back — the Phase 0 style/voice choices below are this pipeline's own contract, not a new coordination interview; do not re-run routing or add a second approval ledger. Consume assigned input IDs/versions and return the canonical output join per `../higgsfield-generate/references/package-gate.md`: block→job UUID mappings are provider locators paired to canonical shot/panel/asset IDs, never `result_asset_id` values themselves. A request for one explainer implies no additional deliverables or publication.

**REQUIRED for dependent video generation, including standalone execution:** apply the [whole-storyline continuity gate](../video-production-assets/references/26-state-causality-continuity.md#storyline-continuity-gate). Before submission, inspect the accepted predecessor's actual selected source range/end frame and relevant history across inserts, reappearances and timeline changes; resolve current character/location/prop/look asset versions. New angles inherit state while using the current approved composition, not a forced copy of the old camera.

**REQUIRED:** use [sequence execution and pre-generation AV handoff](../video-production-assets/references/sequence-execution.md#3a-영상오디오-인계와-실제-호출-패킷--필수) for these dependent shots even in standalone mode: bind accepted predecessor visual/audio context and relevant history/asset state to the actual native selected references and submitted prompt, prepare the validated request, then audit the actual call. Missing/unverified evidence, unsupported reference inputs or an unregistered transport block dependent submission; CLI examples below do not bypass this gate. First shots/new voices need no nonexistent predecessor; explicit silence and approved editorial audio remain scoped by the canonical gate. Independent shots may run concurrently only after their lack of predecessor/history-state dependencies is established; changing angle or inserting another shot does not establish independence.

## Package gate

Apply `../higgsfield-generate/references/package-gate.md` before Phase 1 and again before each submission phase: runtime check (never auto-install), eligible operation, and ONE verified aggregate quote covering the style key + all N audio jobs + all N video jobs + assembly + approved retries — submitted for bounded approval before any job runs. `seed_audio`, `gemini_omni`, `explainer_video` are eligible video/audio operations. Higgsfield **image** generation (a custom `nano_banana_2` style key) is ineligible in this package — see Phase 1 for the lawful style-key sources.

Never use the monolithic `video_explainer` job in this skill.

## Bootstrap

1. If `higgsfield` is unavailable or `higgsfield account status` fails, report the blocker — ask the user to run `higgsfield auth login`, then wait. Never install automatically; installation is a separate operation only on explicit user request.
2. Before any paid precursor, verify current `seed_audio`, `gemini_omni` and `explainer_video` contracts and the selected eligible style-key route. Do not query an unused Higgsfield image recipe as an execution prerequisite. Actual command/pairing details are deferred to [block execution](references/block-execution.md).

The ten-second block length is this lane's assembly contract, not a universal model limit. Before quoting or submitting, verify that the selected clip model accepts ten seconds AND that the live assembler accepts the typed ordered pairs, block timing, aspect and subtitle options below. On 2026-10-16 the read-only MCP catalog accepted `gemini_omni` (duration 4–10 seconds, 720p, 16:9/9:16), but returned `Model not found: explainer_video`; `higgsfield model get explainer_video --json` independently returned `No model with job_type "explainer_video"` (exit 4). This lane is therefore blocked at that checkpoint until a live assembler contract becomes available. Block before generating paid audio/clips. Do not silently switch to the newer `faceless-video` workflow or change block lengths.

## Phase 0 — ask first

Collect choices in two separate turns, in this order. Never merge them. Reuse any choice already supplied in the request or delegated brief (a supplied preset id, style donors, voice, duration, language, character mode, aspect, subtitles counts as that choice made); ask only what is materially unresolved. Every choice belongs to the user unless they explicitly delegate it.

### Turn 1 — style only

Always load the live CMS catalog:

```bash
higgsfield preset list video-explainer --json
```

Show the preset names with their thumbnail/video preview URLs. Say one short line asking the user to pick a preset, describe a custom style, or attach style-reference images, then end the turn. Do not ask production questions in the same turn. Choosing a style is mandatory; never choose silently unless the user explicitly says “you choose.”

Skip this turn when the request already supplies the style: an `explainer preset id: <uuid>` (confirm the UUID exists in the live catalog and keep it for Phase 1), supplied style-donor images, or an explicit existing style image.

### Turn 2 — production settings

Only after style selection, collect every *unresolved* setting:

- Duration: one to ten whole minutes. `N = duration_minutes × 6` fixed 10-second blocks.
- A request below one minute (including 40 seconds) is outside this lane's intake. State the conflict and ask whether the user wants to change duration or choose another workflow; never round up, add blocks, or switch workflows silently. A provisional four-by-ten-second arithmetic sketch is not an executable plan under this contract. Report an unavailable assembler independently; no paid precursor jobs may run while it is unresolved.
- Narration language: English by default; ask only when unresolved.
- Character: recurring mascot or faceless stylistic scenes. Ask when unresolved.
- Aspect: `16:9` by default or `9:16` vertical.
- Subtitles: off by default. State the CURRENT per-block subtitle cost from the live contract — do not quote a remembered price. If enabled, make the user choose `patrick`, `caveat`, `marker`, or `anton`; never choose silently.

## Inputs

- Topic or personal/philosophical story.
- Optional local source documents; read/extract them before scripting. They are factual input, not generation media.
- Optional preset UUID, mutually exclusive with custom style-reference images.
- Optional style-reference images. Use only their rendering style and color grading; never copy their people, text, logos, or objects unless requested.
- Duration, language, character mode, aspect, and subtitle choice from Phase 0.

Local style donors and web images (downloaded or already-uploaded media IDs) feed the lawful style-key sources in Phase 1 — they are style references for whichever eligible source produces the key, never a Higgsfield image submission.

## Hard rules

- Keep every visual strictly non-photorealistic. Repeat the same STYLE descriptor and non-realism negatives in every clip prompt.
- Keep all spoken words out of video generation. Clip audio is ambient sound or music only; no dialogue, lip-sync, or baked narration.
- Use exactly one narration take and one clip per labeled block. Block N audio always maps to Block N video.
- Attach the same style-key image to every clip.
- Write all image/video prompts in English. Only narration uses the selected language.
- Research real topics before scripting. Do not invent quotes, dates, numbers, or events.
- Assemble automatically in the same run. Returning loose clips is a failure.

## Pipeline

| Phase | Output | CLI |
|---|---|---|
| 0 Ask | style first; then duration, language, character, aspect, subtitles | `preset list` + user questions |
| R Research | verified facts and sources | available research tools |
| 1 Style key | one universal style image | `preset resolve` or an existing/authorized-executor image (`nano_banana_2` is craft-only here) |
| 2 Narration | N labeled narration lines | reasoning |
| 3 Block prompts | N labeled video prompts | reasoning |
| 4 Voice | user selects one voice; generate N takes | `voices list` + `seed_audio` |
| 5 Clips | generate N 10-second clips | `gemini_omni` |
| 6 Assemble | one final MP4 | `explainer_video` |

Read `references/prompts.md` before Phases 1–3.

## Phase R — research

For a real topic, use available web research tools and authoritative sources to verify enough facts for every block. Keep a short Sources list. Never script a factual explainer from memory alone.

For a personal story, skip web research and use only details supplied by the user. Invent nothing factual.

## Phases 1–6 — bounded block execution

- At style-key resolution, actual block execution, pairing/schema writing or repair, read [block execution](references/block-execution.md); do not preload its command/JSON appendix for an intake-only request. It owns preset/custom key resolution, exact narration/prompt formats, voice selection, UUID joins, live-model flags, assembler options and recovery.
- One STYLE key, exactly N lines/prompts and the user's selected/delegated single voice are required. Narration's 20–24-word/8–9-second sketch is only a heuristic; measure every real take, keep it roughly under 9.5 seconds, and fix overrun inside approval. Plain spoken narration has no stage directions/timecodes; spell numbers out and preserve personal facts.
- Every video prompt retains identical STYLE/non-realism constraints; one clear action per block, English prompt, selected-language narration. Mascot starts with a closed-mouth greeting and ends with a sign-off; faceless remains stylistic. No spoken words/lip-sync/baked narration in clips.
- Complete all N audio takes **before** clips. Only continuity-independent clips may run concurrently after the strict audio barrier and actual native handoff; pair Block N audio/video exactly once with no missing/duplicate IDs.
- Assemble in this run via the verified server-side `explainer_video` contract; no local ffmpeg, legacy assembler or monolithic `video_explainer`. Measure N×10 expected versus actual duration and inspect narration/captions. Unknown timeout needs job reconciliation, never duplicate submission; repairs stay within approved count/cost/retry bounds.

When this explainer is part of a full production package or the user requests a detailed storyboard/full sheet, REQUIRED: inherit `creative-production`'s [complete storyboard contract](../video-production-assets/references/storyboard-contract.md). Map all approved synopsis beats to the existing N blocks and their shot/panel IDs; integrate camera/spatial/VFX/narration timing/audio fields before final review. Preserve this lane's block format and closed-mouth narration approach rather than inventing lip-sync. Actual full clean-image story review precedes an approved storyboard-to-video handoff; text plans and style keys alone are not that review. An ordinary already-approved explainer execution does not acquire an unrequested new package.

## Deliver

Return the final assembled video URL, exact duration, aspect, narration language, selected style, narrator, subtitle status, and a Sources list for researched topics. Keep intermediate job IDs and loose asset URLs internal unless requested. For delegated production work, additionally return the internal canonical join (per the package gate): assembled output file path/hash and job locator, block→audio_job/video_job UUID pairs, STYLE_KEY_ID locator, observed terminal states, and measured cost.

## Acceptance

The final explainer is complete only when the selected style and voice are user-supplied or explicitly approved, the aggregate package gate covers the eligible operations and retries, and each of the `N` labeled narration takes is paired exactly once with one completed clip in the same order. The assembled result must have the requested aspect and exactly `N × 10` seconds; verify the final URL/status and report failures by block. A plan, loose clips, missing style key, or unassembled clips are not a completed explainer.
