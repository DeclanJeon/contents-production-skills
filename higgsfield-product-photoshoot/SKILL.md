---
version: 0.17.0
name: higgsfield-product-photoshoot
description: |
  Generate brand-quality product images through Higgsfield product-photoshoot
  prompt enhancement on GPT Image 2 / gpt_image_2. Photography specialist for
  professional brand/product visuals under creative-production project routing.
  Use when: "product photo", "studio shot", "lifestyle image", "Pinterest pin",
  "hero/banner", "carousel", "ad creative", "Meta ads", "virtual try-on",
  "model wearing", "person holding product", "closeup with hands",
  "levitating/floating/splash product", "CGI/surreal product", "restyle",
  "seasonal/aesthetic variation", or any product, brand, or paid-social creative.
  Modes: product_shot, lifestyle_scene, closeup_product_with_person,
  moodboard_pin, hero_banner, social_carousel, ad_creative_pack,
  virtual_model_tryout, conceptual_product, restyle. Backend assembles the final
  prompt; never freehand it.
  NOT for: no-product text-to-image (use higgsfield-generate), branded avatar
  video (use higgsfield-generate Marketing Studio), marketplace listing cards
  (use higgsfield-marketplace-cards), Soul Character training (use
  higgsfield-soul-id).
argument-hint: "[--mode <mode>] [--count N] [prompt]"
allowed-tools: Bash
---

# Product Photoshoot

Brand-image generation via the `higgsfield product-photoshoot create` command. The CLI calls a backend prompt enhancer that holds mode-specific photography vocabulary and structural templates, then submits to `gpt_image_2` and returns image URLs.

`creative-production` owns content/campaign project coordination; this skill owns selected Higgsfield product-photo execution. Establish its **Single coordinator, scoped specialists** contract once on standalone content use; on delegation, execute only the assigned scope without routing back — consume assigned input IDs/versions and return the canonical output join per `../higgsfield-generate/references/package-gate.md` (a returned image URL or job UUID is a provider locator, never a canonical `result_asset_id`). Keep native upload/preset workflows, prerequisites, and spend approval; standalone brand/UI design keeps its design owner.

## Package gate and eligibility

Apply `../higgsfield-generate/references/package-gate.md` before any actual run: runtime check (report missing CLI/auth — never auto-install; installation only on an explicit separate request), verified quote covering all `--count` outputs plus retries, bounded approval.

**In this package, `higgsfield product-photoshoot create` submits provider image jobs and is ineligible to execute** — package policy excludes Higgsfield image generation even when selected. The command contract below is preserved craft/reference; the backend's private mode-specific prompt enhancer cannot be reproduced by swapping in a generic image model. Two lawful paths:

1. Report the original backend workflow as blocked in this package.
2. Only with explicit user authorization for a narrower deliverable: run the authorized eligible image executor (`codex-imagen` default) using the mode taxonomy in `references/modes.md`, and disclose that the backend enhancer, mode-locked multi-slide systems, and photography templates are not reproduced.

## Runtime check

`higgsfield` on `$PATH`, `higgsfield account status` clean — else report the blocker (`higgsfield auth login` is a user action). Never install automatically.

## UX Rules

1. Be concise. Print only image URLs in the final reply.
2. Detect language, respond in it. Mode names and CLI flags stay English.
3. Ask at most 4 short questions before submitting — and only for materially unresolved choices. Supplied mode/count/style/use answers are reused, never re-asked.
4. Skip questions whose answer is obvious from context (uploaded image, prior turn, brand memory, delegated brief).
5. Never write the gpt_image_2 prompt yourself — backend assembles it.
6. Polling is silent. Wait until URLs are ready, then deliver.

## Modes and interview

Load `references/modes.md` before submitting: the ten modes (`product_shot`, `lifestyle_scene`, `closeup_product_with_person`, `moodboard_pin`, `hero_banner`, `social_carousel`, `ad_creative_pack`, `virtual_model_tryout`, `conceptual_product`, `restyle`), selection tie-breakers, and the Type A–F interview scripts. Pick by intent, not surface keyword; reuse every answer already supplied.

## Generation

Single command. Backend assembles the final prompt and submits to `gpt_image_2`. URLs print on stdout. (Preserved contract — ineligible to submit inside this package; see eligibility above.)

```bash
higgsfield product-photoshoot create \
  --mode <mode> \
  --prompt "<short user-intent description from interview answers>" \
  [--image <path-or-upload-id>]... \
  [--count <1-10>] \
  [--aspect_ratio <override>]
```

Examples:

```bash
higgsfield product-photoshoot create \
  --mode lifestyle_scene \
  --prompt "bottle of cold-brew on a sunlit kitchen counter, IG feed" \
  --image bottle.jpg \
  --count 3
```

```bash
higgsfield product-photoshoot create \
  --mode moodboard_pin \
  --prompt "vertical pin for my candle brand, cottagecore mood" \
  --image candle.jpg
```

```bash
higgsfield product-photoshoot create \
  --mode restyle \
  --prompt "Christmas version, quiet-luxury aesthetic" \
  --image existing-shot.jpg
```

## Image inputs

`--image` accepts a local file path (auto-uploaded) OR an existing upload UUID. Repeat the flag for multiple references.

## Multi-variant

`--count 3` returns 3 distinct image URLs. Backend asks the enhancer to vary preset, lighting, angle, and palette across variants — they will not be paraphrased copies of one another.

For `social_carousel` and `ad_creative_pack`, count = number of slides / variants in the pack. Backend locks the visual system across all slides automatically.

## Aspect ratio

Backend picks a sensible default per mode. Override with `--aspect_ratio` only if the user explicitly asks for a different one. Allowed values: `1:1`, `4:5`, `5:4`, `3:4`, `4:3`, `2:3`, `3:2`, `9:16`, `16:9`.

## Resolution

Use `2k` for every product-photoshoot job.

## Delivering results

Print the image URLs as a short bulleted list. No JSON, no IDs, no internal model names, no enhanced prompt text. If a job failed, mention it briefly with the failure status.

```
3 lifestyle shots ready:
- https://cdn.higgsfield.ai/.../job_abc.jpg
- https://cdn.higgsfield.ai/.../job_def.jpg
- https://cdn.higgsfield.ai/.../job_ghi.jpg
```

## What this skill does NOT do

- Does not write gpt_image_2 prompts directly. Backend owns prompt assembly.
- Does not auto-pick a different image-gen model. Always `gpt_image_2`.
- Does not replace `higgsfield-generate` Marketing Studio for branded video / avatar workflows.
- Does not replace `higgsfield-generate` for raw text-to-image without a product or brand context.

## Common mistakes to avoid

- Asking more than 4 interview questions in a single message.
- Picking the wrong mode (e.g. `product_shot` when the user wants a Pinterest pin).
- Calling `higgsfield generate create gpt_image_2 --prompt ...` directly instead of `higgsfield product-photoshoot create` — bypasses the prompt enhancer and produces noticeably worse output.
- Pasting the assembled prompt back to the user — they want the URLs.
- Using a `--mode` value not in the table in `references/modes.md`.
