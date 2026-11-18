# Explainer block execution and recovery

Read before actual style-key resolution, block execution, pairing/schema authoring or repair, not intake alone. Scope, intake, live-assembler preflight and approval gates remain in [SKILL](../SKILL.md). Higgsfield image commands below remain **craft/reference only and ineligible**. No paid precursor jobs until the current assembler contract is verified. `references/` recipe paths below are skill-root relative.

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
- Word count is a drafting heuristic, not a duration measurement. Inspect each completed audio take's actual runtime before accepting it; record measured seconds and any overrun. Do not infer timing from language, word count or a successful job status.
- Use plain spoken text only: no timecodes, emotion cues, parentheticals, or stage directions.
- Spell numbers out.
- Use a concrete tone and never say “in this video.”
- For a topic, build from hook through payoff. For a personal story, preserve the user's details and protagonist.




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

The preserved assembler recipe specifies ten-second blocks, centered short takes, pitch-safe handling of small overruns, ordered concatenation and optional timed captions. Treat these as required capabilities to verify in the live assembler contract, not observed output. After assembly, measure the actual duration and inspect narration alignment/captions; expected total is `N × 10` seconds. Report measured and expected duration separately.

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

