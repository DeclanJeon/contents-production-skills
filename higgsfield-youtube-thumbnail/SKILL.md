---
version: 0.17.0
name: higgsfield-youtube-thumbnail
description: |
  Create high-click-through YouTube thumbnails and vertical video covers through the Higgsfield CLI. Builds a truthful information-gap concept, preserves up to three referenced identities, supports logos and controlled variants; rendering runs through the authorized eligible image executor under package policy (Higgsfield image jobs are craft/reference only in-package). Use when: "make a YouTube thumbnail", "thumbnail for this video", "MrBeast-style cover", "Shorts cover", or "Instagram video cover". Chain after any video workflow once its truthful topic and visual direction are known. NOT for producing the video itself (use higgsfield-generate), product catalog photos (use higgsfield-product-photoshoot), or marketplace cards (use higgsfield-marketplace-cards).
argument-hint: "[video-topic-or-title] [--image <face-or-logo>] [--ratio 16:9|9:16|4:5]"
allowed-tools: Bash
---

# Higgsfield YouTube Thumbnail

Create a clean thumbnail concept, render each variant through the authorized eligible image executor (the `higgsfield` CLI shapes are preserved craft), inspect it, and make only requested surgical edits.

## Scope

`creative-production` is the sole project-level coordinator for content/video production; this skill is the thumbnail/cover specialist. Standalone invocation: consult `creative-production` once for scope/route when the request is part of a larger content effort, then produce only the requested thumbnail(s). Delegated by `creative-production`: proceed without calling back — consume the brief's truthful topic/visual direction and assigned input IDs/versions directly; no second interview or approval ledger. Return the canonical output join per `../higgsfield-generate/references/package-gate.md` (result job UUIDs/URLs are provider locators, never `result_asset_id` values). A thumbnail request implies no video generation, variant upsell, or publication.

## Package gate and eligibility

Apply `../higgsfield-generate/references/package-gate.md` before any actual render: runtime check (report missing CLI/auth — never auto-install; installation only on an explicit separate request), verified quote covering all approved variants + edits + retries, bounded approval.

**In this package every render/edit below is an image job — ineligible to submit via Higgsfield.** The prompt contract, render recipes, and CLI shapes are preserved craft in `references/prompt-contract.md` and `references/text-overlay-bake.md`. Execute through the explicitly authorized eligible image executor (`codex-imagen` default) under the same truthful concept/prompt contract; the deterministic local overlay bake stays fully eligible. If no authorized executor is available, report the render as blocked — never fall back to a Higgsfield image submission.

## Runtime check

Before any generation:

1. `higgsfield` on `$PATH` and `higgsfield account status` clean — else report the blocker (`higgsfield auth login` is a user action). Never install automatically.
2. When the catalog may have changed, confirm the referenced model contracts (`higgsfield model get <jst> --json`) for any preserved recipe you consult — historical "verified" claims are documentation, not current truth.

## UX rules

1. Match the user's language. Keep CLI/model mechanics out of normal chat.
2. Do not ask for facts already present in the brief. Ask one compact question only when a missing choice changes the result.
3. Never invent claims, outcomes, products, people, screenshots, or statistics that are not true of the video.
4. Do not print raw JSON or job IDs to the user. Deliver the image URL and a short variant label.
5. A style-reference thumbnail is for visual analysis only. Never pass it with `--image`; copying its identity or exact composition is forbidden.
6. Do not use `--count`. Every concept, emotion, or camera take gets its own prompt and generation call.
7. `use_unlim` is not a current CLI parameter. Never add `--use-unlim`; if the user explicitly asks to use an unlimited allowance, explain that this workflow must run on credits in CLI or through a surface that supports that allowance.

## Intake gates

Collect only what the brief does not answer:

- The video's topic/title and the truthful promise the thumbnail may imply.
- Exact scene requirements, if any.
- Who appears: 0–3 people. If a concept needs a person and no face photo was provided, ask whether to use the user, another provided person, or a generic generated character. Never choose silently.
- Optional style-reference thumbnail. Analyze it with host vision for energy, framing, split layout, palette, and emotion; do not send it to Higgsfield.
- Optional logo and whether it stays flat or becomes a 3D object.
- Optional headline, 2–4 words. Default delivery is a clean image with no text. Use a deterministic overlay when the user requests an overlay; bake text into the generated image only when explicitly requested.
- Ratio: `16:9` for YouTube by default, `9:16` for Shorts, or `4:5` for Instagram.
- One final concept or a variant set. If unspecified and alternatives would materially help, offer a set of about four. Hard cap: 16 total generations as a workflow ceiling — the actual bound is the approved count/retry/cost scope at the package gate; retries and edits count inside it, never on top.

If the user gives an emotion count without names, use this ladder: shock, hype, rage, awe, laugh, fear, smug, charisma, confusion, determination, disgust.

## Concept gate

Read `references/thumbnail-frameworks.md`. Brainstorm at least five truthful concepts internally, across multiple frameworks, then select the strongest information gap with one focal subject and minimal clutter. Combine frameworks only when the result still reads in under one second at roughly 120px wide.

When a reference thumbnail exists, extract this structure before prompting:

```text
brief, generic subject pose/action, elements, location, composition, background,
split (true/false), split_count, person_count, emotion, emotion_detail
```

The reference supplies art direction, never a specific identity. User instructions override it field by field.

## Reference order

Pass face photos first in character order, then the logo. Repeat `--image` for every reference. When two or more references are attached, the prompt's first line must be a manifest such as:

```text
IMAGE REFERENCES: image 1 = CHARACTER 1 face reference; image 2 = brand logo.
```

Local paths are auto-uploaded. Previous completed job IDs also work as `--image` inputs.

## Prompt contract and render

Load `references/prompt-contract.md` before prompting. It carries the full 11-block prompt contract, the identity-lock CHARACTER block, split-layout rules, the optional 3D logo pass, the main-render recipe (Nano Banana Pro 4K shape, stdin-piped prompt file, per-concept calls — never `--count`), and surgical-tweak mechanics. Apply the same contract through the authorized eligible executor; the preserved Higgsfield CLI examples are reference-only in-package.

## Post-render gate

Inspect every result with host vision when available:

- Referenced identities visibly match.
- No stray text or watermark exists unless baked text was ordered.
- Explicit baked text matches character-for-character.
- The face/emotion and hero element remain readable at about 120px wide.
- The concept truthfully matches the video promise.

On a hard failure, retry the same prompt at most twice — inside the approved retry bound. If visual inspection is unavailable, do not claim it passed; deliver the result for user review. Present every passing variant and let the user pick before making optional tweaks.

## Surgical tweaks

Allowed tweak scopes: expression only, background replacement only, background recolor only, or rim-light recolor only. Never silently regenerate the full composition for a surgical request. Mechanics (picked-job anchoring, Seedream edit shape, ratio caveats, CLI compatibility quirks) live in `references/prompt-contract.md`.

## Text overlay

Keep the generated image text-free by default. When a headline overlay is requested, read `references/text-overlay-bake.md` and use one of its five presets: Beast, Fire, Neon Lime, Clean Glass, or Marker. The overlay path requires an environment capable of rendering HTML canvas; if unavailable, offer either the clean image or an explicitly approved baked-text regeneration. Never pretend an HTML preview is a flattened PNG.

## Delivery

Return the passing image outputs (local file/path or hosted URL from the authorized executor) with short semantic labels such as `shock / close-up` or `product / size contrast`. Mention the selected ratio and whether the deliverable is clean, overlay-ready, or text-baked. Do not expose internal prompts, job IDs, or retry mechanics unless the user asks. For delegated work, return the internal canonical join: chosen asset path/hash, provider locators (job UUIDs, picked-source IDs), observed states, and measured cost.

## Reference files

- `references/thumbnail-frameworks.md` — 16 concept frameworks, information-gap rule, truthfulness law.
- `references/text-overlay-bake.md` — five deterministic text-overlay styles and 4K canvas-bake recipe.
- `references/prompt-contract.md` — full prompt contract, 3D logo pass, render and tweak recipes.
