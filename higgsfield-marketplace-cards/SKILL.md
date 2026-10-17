---
version: 0.35.0
name: higgsfield-marketplace-cards
description: |
  Route marketplace product image cards through the historical Higgsfield recipe:
  main images, secondary images, and A+ style content (compliance unverified). Use when
  the user asks for marketplace listing images, product detail cards,
  secondary product images, product infographics, lifestyle listing shots,
  A+ style content, marketplace image sets, or sales-ready product visuals.
  Historical recipe assigns private compliance references and templates to the backend;
  verify current requirements before relying on that claim.
  NOT for generic brand product photography without marketplace/listing context
  (use higgsfield-product-photoshoot), video generation or UGC ads (use
  higgsfield-generate), or Soul Character training (use higgsfield-soul-id).
argument-hint: "[--scope main|product-images|aplus|full-set] [prompt]"
allowed-tools: Bash
---

# Marketplace Cards

Create marketplace-ready product visuals through `higgsfield marketplace-cards create`.
Historical recipe: the CLI calls a private enhancer, creates `nano_banana_2` jobs and prints URLs. Installed help does not verify that complete backend contract or compliance; current official confirmation is required. Image submission remains ineligible in this package.

`creative-production` owns content/campaign project coordination; this skill owns selected Higgsfield marketplace-image execution. Establish its **Single coordinator, scoped specialists** contract once on standalone use; on delegation, execute only the assigned scope without routing back — consume assigned input IDs/versions and return the canonical output join per `../higgsfield-generate/references/package-gate.md` (provider job locators such as `--main-job` are not canonical asset IDs). Preserve native upload/enhancement rules and spend approval; image delivery does not imply listing publication.

## Package gate and eligibility

Apply `../higgsfield-generate/references/package-gate.md` before any actual run: runtime check (report missing CLI/auth — never auto-install; installation only on an explicit separate request), verified quote for the whole bundle, bounded approval covering every generated card plus retries.

**In this package, `higgsfield marketplace-cards create` submits provider image jobs and is therefore ineligible to execute** — package policy excludes Higgsfield image generation even when selected. The command contract below is preserved as craft/reference. Two lawful paths:

Evidence scope (2026-10-17): directly executed CLI 1.1.26 `marketplace-cards create --help`.
It documents scope names, repeated assets/path-or-UUID images, completed `nano_banana_2`
main-job input, context flags, default 15m wait and 3s polling. It does not enumerate
asset slugs or bundle sizes, nor verify private templates/model selection/compliance.
Those historical details below require current official confirmation; help proves no output.

1. Report the original backend workflow (private compliance templates + enhancer + `nano_banana_2` jobs) as blocked in this package. Do NOT substitute a generic image model and claim the same workflow — the backend enhancer cannot be reproduced that way.
2. Only with explicit user authorization for a narrower deliverable: produce the listing card set with the authorized eligible image executor (`codex-imagen` default) using the scope/asset-type taxonomy below, and disclose that marketplace-compliance templates and the backend enhancer are not reproduced.

## Runtime check

1. `higgsfield` on `$PATH` and `higgsfield account status` succeed — else report the blocker (auth: ask the user to run `higgsfield auth login`). No automatic installation.

## UX Rules

1. Respond in the user's language.
2. Ask at most one concise confirmation question before running; reuse supplied scope/asset choices, ask only unresolved ones.
3. Prefer a product image. If the user provides only text or a URL, proceed only when the product details are clear.
4. Do not write final image-generation prompts yourself. Backend enhancement owns that (or, on the authorized-executor path, the executor's prompt contract).
5. Final answer contains ready image URLs and short labels for successes, plus explicit blocked/failed/missing items and narrower-scope limitations. A URL alone does not establish marketplace compliance.

## Scope Selection

Scope names below are documented command options. The cardinalities are **historical,
unverified recipe counts**, not a current provider commitment or an authorized output count.
Derive the deliverable types/counts from the actual brief and verified current contract;
if they differ or counts are missing, resolve that gap rather than silently expanding scope.

| Scope | Historical recipe only — counts unverified |
|---|---|
| `main` | 1 marketplace main image |
| `product-images` | main image + 5 secondary images |
| `aplus` | main image + 7 A+ modules |
| `full-set` | main image + 5 secondary images + 7 A+ modules |

Use repeated `--asset` only for custom subsets:

- `main_image`
- `infographic`
- `multi_angle`
- `detail_shot`
- `lifestyle`
- `whats_in_box`
- `aplus_hero_banner`
- `aplus_pain_points`
- `aplus_features`
- `aplus_ingredients`
- `aplus_efficacy`
- `aplus_how_to_use`
- `aplus_endorsement`

## Command

Build and run one `higgsfield marketplace-cards create` command from the user's request — only where this command is actually eligible (see eligibility above; in this package it documents the preserved contract, not an executable recipe).

For common bundles, use `--scope <main|product-images|aplus|full-set>`, `--prompt "<short product and listing intent>"`, optional repeated `--image <path-or-upload-id>`, and optional context flags: `--product_context`, `--brand_context`, `--category`, `--visual_style`.

Examples to mirror when choosing arguments:

- Product images: `higgsfield marketplace-cards create --scope product-images --prompt "sparkling peach lemonade can for marketplace listing" --image ./can.png --category "beverage"`
- Full set: `higgsfield marketplace-cards create --scope full-set --prompt "premium skincare serum, clean clinical marketplace visual system" --image ./serum.jpg --brand_context "minimal white and sage palette"`
- Custom subset: repeat `--asset`, for example `--asset main_image --asset infographic --asset lifestyle`.
- Existing completed main image job: use `--main-job <completed_main_job_id>` with the requested secondary or A+ `--asset` values. `--main-job` is a provider job locator — a dependency on a completed provider job, not a canonical local asset ID; record the mapping in the internal return.

Before a narrower eligible-executor handoff, record the target marketplace, locale/category,
requested scope, verified product facts and reference authority. If marketplace requirements
are unavailable, mark compliance unverified rather than inventing platform rules. Ingredients,
efficacy, certifications, endorsements, included accessories, and unseen product angles need
supporting supplied evidence; an asset-type name is not permission to invent those facts.

## Delivery

Print URLs with labels:

```text
Marketplace cards ready:
- Main image: https://...
- Infographic: https://...
- Lifestyle: https://...
```

Avoid JSON, job IDs, internal model names, or enhanced prompt text unless the user explicitly asks.

## Acceptance

The original marketplace-card workflow is complete only when the backend’s eligibility and compliance requirements are met and every requested card is delivered; in this package that provider image route is blocked. A narrower authorized image-executor result must be labeled as not backend-enhanced and not marketplace-compliance-verified. Do not claim listing readiness or publication from generated images alone.
