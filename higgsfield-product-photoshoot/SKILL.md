---
version: 0.35.0
name: higgsfield-product-photoshoot
description: |
  Route product photography through the historical Higgsfield product-photoshoot
  recipe (GPT Image 2 backend unverified; inspect current contract).
  Photography specialist under creative-production project routing.
  Use when: "product photo", "studio shot", "lifestyle image", "Pinterest pin",
  "hero/banner", "carousel", "ad creative", "Meta ads", "virtual try-on",
  "model wearing", "person holding product", "closeup with hands",
  "levitating/floating/splash product", "CGI/surreal product", "restyle",
  "seasonal/aesthetic variation", or any product, brand, or paid-social creative.
  Modes: product_shot, lifestyle_scene, closeup_product_with_person,
  moodboard_pin, hero_banner, social_carousel, ad_creative_pack,
  virtual_model_tryout, conceptual_product, restyle. Historical recipe assigns
  prompt assembly to the backend; verify current behavior before relying on it.
  NOT for: no-product text-to-image (use higgsfield-generate), branded avatar
  video (use higgsfield-generate Marketing Studio), marketplace listing cards
  (use higgsfield-marketplace-cards), Soul Character training (use
  higgsfield-soul-id).
argument-hint: "[--mode <mode>] [--count N] [prompt]"
allowed-tools: Bash
---

# Product Photoshoot

Brand-image routing via `higgsfield product-photoshoot create`. The historical recipe describes a private mode-specific prompt enhancer submitting to `gpt_image_2` and returning image URLs; the inspected help does not verify that backend/model contract. Require a current official contract before relying on it. The package image exclusion below remains binding.

`creative-production` owns content/campaign project coordination; this skill owns selected Higgsfield product-photo execution. Establish its **Single coordinator, scoped specialists** contract once on standalone content use; on delegation, execute only the assigned scope without routing back — consume assigned input IDs/versions and return the canonical output join per `../higgsfield-generate/references/package-gate.md` (a returned image URL or job UUID is a provider locator, never a canonical `result_asset_id`). Keep native upload/preset workflows, prerequisites, and spend approval; standalone brand/UI design keeps its design owner.

## Package gate and eligibility

Apply `../higgsfield-generate/references/package-gate.md` before any actual run: runtime check (report missing CLI/auth — never auto-install; installation only on an explicit separate request), verified quote covering all `--count` outputs plus retries, bounded approval.

**In this package, `higgsfield product-photoshoot create` submits provider image jobs and is ineligible to execute** — package policy excludes Higgsfield image generation even when selected. The command contract below is preserved craft/reference; the backend's private mode-specific prompt enhancer cannot be reproduced by swapping in a generic image model. Two lawful paths:

Evidence scope (2026-10-17): directly executed CLI 1.1.26 `product-photoshoot create --help`;
it documents required `--mode`/`--prompt`, repeatable path/upload-UUID images, count 1–10,
aspect override, default 10m wait and 3s poll. It does not enumerate modes/aspect values
or expose resolution. All private enhancer/template/model/default-aspect/slide semantics
below and in `references/modes.md` remain historical/unverified, not successful-run evidence.
Confirm the exact current official contract before relying on those fields; help does
not authorize this ineligible image path.

1. Report the original backend workflow as blocked in this package.
2. Only with explicit user authorization for a narrower deliverable: run the authorized eligible image executor (`codex-imagen` default) using the mode taxonomy in `references/modes.md`, and disclose that the backend enhancer, mode-locked multi-slide systems, and photography templates are not reproduced.

## Runtime check

`higgsfield` on `$PATH`, `higgsfield account status` clean — else report the blocker (`higgsfield auth login` is a user action). Never install automatically.

## UX Rules

1. Be concise. Deliver image URLs only for actual successful outputs; blocked, failed, partial, or narrower-scope work must state its status and limitations instead.
2. Detect language, respond in it. Mode names and CLI flags stay English.
3. Ask at most 4 short questions before submitting — and only for materially unresolved choices. Supplied mode/count/style/use answers are reused, never re-asked.
4. Skip questions whose answer is obvious from context (uploaded image, prior turn, brand memory, delegated brief).
5. Preserve backend prompt assembly only as a historical, unverified recipe; do not claim a verified `gpt_image_2` backend or reproduce its private prompt.
6. Polling is silent. Wait until URLs are ready, then deliver.

## Modes and interview

Load `references/modes.md` before submitting: the ten modes (`product_shot`, `lifestyle_scene`, `closeup_product_with_person`, `moodboard_pin`, `hero_banner`, `social_carousel`, `ad_creative_pack`, `virtual_model_tryout`, `conceptual_product`, `restyle`), selection tie-breakers, and the Type A–F interview scripts. Pick by intent, not surface keyword; reuse every answer already supplied.

## Generation

Historical, unverified backend recipe: one command assembles a prompt, submits to `gpt_image_2`, and prints URLs. Installed help verifies command inputs, not those backend guarantees. Inspect a current official contract before relying on them; submission remains ineligible inside this package.

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

The preserved recipe requests variation across `--count` outputs. Distinctness, product fidelity, and cross-slide consistency require inspection of the actual results; an enhancer description is not proof that they hold.

For `social_carousel` and `ad_creative_pack`, count denotes slides / variants in the pack. Report any missing or inconsistent slide individually; do not claim an automatically locked visual system without inspecting it.

## Aspect ratio

Historical recipe: mode-specific aspect default with override, and values `1:1`, `4:5`, `5:4`, `3:4`, `4:3`, `2:3`, `3:2`, `9:16`, `16:9`. Help verifies only an override string, not these enums/defaults. Verify the current contract and actual brief; do not invent a backend default.

## Resolution

The preserved recipe targets `2k`; the inspected CLI 1.1.26 dedicated command exposes no resolution flag. Do not invent one or claim this resolution was requested or returned; verify any backend resolution contract separately.

## Delivering results

Print the image URLs as a short bulleted list. No JSON, no IDs, no internal model names, no enhanced prompt text. If a job failed, mention it briefly with the failure status.

```
3 lifestyle shots ready:
- https://cdn.higgsfield.ai/.../job_abc.jpg
- https://cdn.higgsfield.ai/.../job_def.jpg
- https://cdn.higgsfield.ai/.../job_ghi.jpg
```

## What this skill does NOT do

- Does not claim to reproduce the historical backend's private prompt assembly.
- Does not auto-pick a replacement model or assert “always `gpt_image_2`”: that historical backend choice is unverified and requires a current official contract. The package image gate still blocks submission.
- Does not replace `higgsfield-generate` Marketing Studio for branded video / avatar workflows.
- Does not replace `higgsfield-generate` for raw text-to-image without a product or brand context.

## Common mistakes to avoid

- Asking more than 4 interview questions in a single message.
- Picking the wrong mode (e.g. `product_shot` when the user wants a Pinterest pin).
- Bypassing the documented enhancer and claiming equivalent output. No comparative quality guarantee has been established by this skill.
- Pasting the assembled prompt back to the user — they want the URLs.
- Using a `--mode` value not in the table in `references/modes.md`.

## Acceptance

The requested set is complete only when the selected mode and count match the user’s brief, product identity and visible attributes are supported by supplied references, and every requested output is delivered or individually marked failed. Provider image submission is ineligible in this package; a narrower authorized image-executor route must disclose that it does not reproduce the private enhancer or locked provider templates. Never invent product specifications or treat an unverified image as a faithful product depiction.
