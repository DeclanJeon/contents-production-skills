---
version: 0.17.0
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

## Package gate

Apply `../higgsfield-generate/references/package-gate.md` before Phase 1 and again before each submission phase: runtime check (never auto-install), eligible operation, and ONE verified aggregate quote covering the style key + all N audio jobs + all N video jobs + assembly + approved retries — submitted for bounded approval before any job runs. `seed_audio`, `gemini_omni`, `explainer_video` are eligible video/audio operations. Higgsfield **image** generation (a custom `nano_banana_2` style key) is ineligible in this package — see Phase 1 for the lawful style-key sources.

Never use the monolithic `video_explainer` job in this skill.

## MCP-to-CLI mapping

| MCP workflow operation | CLI equivalent |
|---|---|
| `get_explainer_presets` | `higgsfield preset list video-explainer --json` |
| `resolve_explainer_preset` | `higgsfield preset resolve video-explainer <preset_id> --json` |
| `generate_image` / `nano_banana_pro` | `higgsfield generate create nano_banana_2 ...` — image job: ineligible in this package, see Phase 1 |
| `list_voices` | `higgsfield voices list --json` |
| `generate_audio` / `seed_audio` | `higgsfield generate create seed_audio ...` |
| `generate_video` / `gemini_omni` | `higgsfield generate create gemini_omni ...` |
| `job_status` | `--wait --json` or `higgsfield generate wait <job_id> --json` |
| `explainer_video` | `higgsfield generate create explainer_video ...` |

`nano_banana_2` is the public CLI id for the Nano Banana Pro style-key model used by the MCP workflow.

## Bootstrap

1. If `higgsfield` is unavailable or `higgsfield account status` fails, report the blocker — ask the user to run `higgsfield auth login`, then wait. Never install automatically; installation is a separate operation only on explicit user request.
2. Inspect the live contracts before the first submission:

   ```bash
   higgsfield model get nano_banana_2
   higgsfield model get seed_audio
   higgsfield model get gemini_omni
   higgsfield model get explainer_video
   ```

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

## Phase 1 — create or resolve the style key

Write one reusable STYLE descriptor: medium, palette, line/fill behavior, texture/finish, then `non-photorealistic, illustrated, not a photo, no live-action, no realism`.

### Selected CMS preset

Resolve the hidden style image into the active workspace:

```bash
higgsfield preset resolve video-explainer "<preset UUID>" --json
```

Keep the returned `media_id` as `STYLE_KEY_ID`. Skip image generation: this imported media is the style key. Build the STYLE descriptor from the returned preset name plus the mandatory non-photoreal rules. Do not recreate a preset from its name.

The preset reference controls framing. If it conflicts with the aspect requested in Phase 0, stop and let the user choose rather than silently fighting the reference.

### Custom style or reference images

The pipeline needs ONE key image. Generating it with `nano_banana_2` is a Higgsfield image job — **ineligible in this package** (package gate). Lawful sources, in preference order:

1. An existing image the user supplied or already has in storage — a local file, an uploaded media ID, or a previously completed image job UUID used as `STYLE_KEY_ID`. (Eligible: reusing an existing image is not an image generation.)
2. A CMS preset resolved through `preset resolve` (above) — it imports an existing CMS image, not a new generation.
3. A style key produced by the explicitly authorized eligible image executor (`codex-imagen` default) using the abstract-swatch or mascot template in `references/prompts.md`, then registered/passed by path or ID. Disclose it came from the authorized executor, not the provider recipe.

If none of those is available, the custom-style branch is blocked — report it and let the user pick a preset or supply a style image. Do not silently submit `nano_banana_2`. In contexts where image generation IS permitted, the preserved recipe is:

```bash
higgsfield generate create nano_banana_2 \
  --prompt "<style-key prompt>" \
  --aspect_ratio 16:9 \
  --resolution 2k \
  --wait \
  --json
```

Use `9:16` for vertical. Whichever lawful source produced it, `STYLE_KEY_ID` is a provider media or completed-job UUID — a locator mapped to the canonical style-key asset in the internal return.

## Phase 2 — write narration

Write exactly `N` labeled narration blocks in the selected language:

```text
Block 1
<line spoken over clip 1>
Block 2
<line spoken over clip 2>
```

- One line per block, usually 20–24 words and about 8–9 seconds.
- Keep every take under roughly 9.5 seconds.
- Use plain spoken text only: no timecodes, emotion cues, parentheticals, or stage directions.
- Spell numbers out.
- Use a concrete tone and never say “in this video.”
- For a topic, build from hook through payoff. For a personal story, preserve the user's details and protagonist.

When this explainer is part of a full production package or the user requests a detailed storyboard/full sheet, REQUIRED: inherit `creative-production`'s [complete storyboard contract](../video-production-assets/references/storyboard-contract.md). Map all approved synopsis beats to the existing N blocks and their shot/panel IDs; integrate camera/spatial/VFX/narration timing/audio fields before final review. Preserve this lane's block format and closed-mouth narration approach rather than inventing lip-sync. Actual full clean-image story review precedes an approved storyboard-to-video handoff; text plans and style keys alone are not that review. An ordinary already-approved explainer execution does not acquire an unrequested new package.


## Phase 3 — write matching video prompts

Write exactly `N` labeled English prompts using the template in `references/prompts.md`:

```text
Block N
STYLE REFERENCE: Match the attached reference image EXACTLY. <same STYLE descriptor>
SCENE: <one scene and action matching Block N narration>
MOTION: <camera move and animation behavior>
AUDIO: <ambient SFX or music only; no voice, dialogue, or narration>
NEGATIVE: <style drift and realism bans; no lip-sync, captions, text, logos, or watermark>
```

For mascot mode, Block 1 greets by gesture with mouth closed, the final block waves a sign-off, and middle blocks use consistent cameos only when useful. For faceless mode, use stylistic scenes only. Keep one clear action per block.

## Phase 4 — generate every voice take first

List the live voices, present the choices, and wait for the user to select one narrator — unless the request or delegated brief already supplies one (a `voice_id`/`type` pair or an explicit named voice): then validate it against the live list and use it, no re-asking:

```bash
higgsfield voices list --json
```

Keep the selected voice's exact `id` and `type` (`preset` or `element`). Never invent or auto-pick a voice unless the user explicitly delegates it. When the coordinator allocated a `voice_profile` entity for the narrator, return the selection joined to it explicitly (entity ID + provider `voice_id`/`voice_type` locator) — don't smuggle the provider ID into the canonical field.

Generate one completed `seed_audio` job per narration block, always with the same voice:

```bash
higgsfield generate create seed_audio \
  --prompt "<Block N narration only>" \
  --voice_type "<preset|element>" \
  --voice_id "<voice UUID>" \
  --wait \
  --json
```

Record every audio job UUID in block order. Regenerate only a failed or excessively long take. Shorten that block or adjust `--speech_rate` modestly when needed. Do not begin Phase 5 until all `N` audio jobs are complete.

## Phase 5 — generate every clip second

Generate one completed 10-second `gemini_omni` clip per block. Attach the same style key to every call:

```bash
higgsfield generate create gemini_omni \
  --prompt "<Block N video prompt>" \
  --image "<STYLE_KEY_ID>" \
  --duration 10 \
  --resolution 720p \
  --aspect_ratio 16:9 \
  --wait \
  --json
```

Use `9:16` when selected. Record every video job UUID in block order. Independent jobs may run concurrently inside this phase, but the audio-phase barrier is strict. Re-submit only failed blocks. Never silently replace `gemini_omni`; inspect the live video catalog if the model is unavailable.

## Phase 6 — assemble immediately

Create `blocks.json` with at least two ordered block pairs. The CLI model contract requires typed references, so use the generic completed-job types:

```json
[
  {
    "video": {"id": "<clip 1 job UUID>", "type": "video_job"},
    "audio": {"id": "<voice 1 job UUID>", "type": "audio_job"}
  },
  {
    "video": {"id": "<clip 2 job UUID>", "type": "video_job"},
    "audio": {"id": "<voice 2 job UUID>", "type": "audio_job"}
  }
]
```

Submit the server-side assembler immediately:

```bash
higgsfield generate create explainer_video \
  --items @blocks.json \
  --width 1280 \
  --height 720 \
  --wait \
  --json
```

Use `--width 720 --height 1280` for vertical. When subtitles are enabled, add the chosen font:

```bash
--subtitles '{"font":"patrick"}'
```

The assembler keeps each block at exactly 10 seconds: it centers short voice takes, pitch-safely speeds small overruns, never stretches video, concatenates blocks in order, and optionally burns timed captions. Total duration is exactly `N × 10` seconds.

Do not use local ffmpeg, the legacy assembly scripts, or the monolithic `video_explainer` job.

## Checkpoints and recovery

- Before Phase 5: require one style key, exactly `N` narration lines and prompts, one selected voice, and `N` completed audio jobs.
- Before Phase 6: require `N` completed video jobs and exact one-to-one block pairing with no missing or duplicate IDs.
- Preset missing: refresh `preset list`; never reuse or fabricate an ID.
- Preset resolve failure: verify workspace selection and retry once.
- Style drift or realism: strengthen the shared STYLE and NEGATIVE text, then regenerate only that clip.
- Timeout: rejoin with `higgsfield generate wait <job_id> --json`; never duplicate a running job.
- Two identical failures mean the prompt or parameters must change.
- Every regeneration/repair stays inside the bounded approval's retry and cost scope — re-check the package gate before exceeding it.

## Deliver

Return the final assembled video URL, exact duration, aspect, narration language, selected style, narrator, subtitle status, and a Sources list for researched topics. Keep intermediate job IDs and loose asset URLs internal unless requested. For delegated production work, additionally return the internal canonical join (per the package gate): assembled output file path/hash and job locator, block→audio_job/video_job UUID pairs, STYLE_KEY_ID locator, observed terminal states, and measured cost.
