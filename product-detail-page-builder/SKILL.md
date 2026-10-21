---
name: product-detail-page-builder
version: 1.1.0
description: Build truthful Korean marketplace product-detail pages from real product photos and supplied facts. Use for 상세페이지, 상품상세, 상품 상세 이미지, 스마트스토어 상세페이지, 쿠팡 상세페이지, product detail page, PDP module images, or a request to turn product photos into reviewed marketplace modules. Do not use for ordinary storefront UI, checkout, listing thumbnails, or publishing.
---

# Product Detail Page Builder

Create a reviewable, platform-aware product story from real product photos and evidence-backed facts. This is a specialist skill. `creative-production` remains the only coordinator and owns scope, execution permission, storage, history, and user-approval interpretation.

## Scope

- Produce a factual Korean product brief, copy draft, ordered module plan, and image-generation prompts.
- Compose approved text deterministically into independent module images and a stitched review preview. A compact, vertically balanced, fact-backed `text-only` module is valid and does not require a repeated product photo. Create long-page slices only when the selected platform profile requires them.
- Validate fact references, image files, text fit, dimensions, file sizes, and unresolved platform requirements.
- Keep product-page assets separate from a storefront's product UI, cart, checkout, catalog, or backend.

Do not upload or publish. A generated preview is not a platform-approved listing and does not guarantee conversion or sales.

## Required inputs

Require:

1. Target platform and country/site.
2. Product name or category.
3. At least one real image that identifies the actual product.

Brand guidance, confirmed specifications, intended audience, and a seller-center-confirmed export profile are optional. If a required input is missing, ask for the single most important missing item and stop before generating images or composing a deliverable.

For one image, treat only visible pixels as visual evidence. Do not invent a back, underside, hidden component, package contents, logo, color variant, or use outcome. Ask for another view or omit that module when the required detail is not visible.

## Fact and evidence contract

Classify each fact as one of:

- `user`: explicitly supplied by the user.
- `visible`: directly visible in a named input image and region.
- `official_source`: supported by a URL and a specific document/field locator.
- `unconfirmed`: unverified or inferred.

Every published claim must reference one or more publishable fact IDs. Never publish `unconfirmed` facts or turn visual appearance into a hidden specification such as material, capacity, performance, certification, compatibility, origin, warranty, or included accessories. Preserve units and wording; ask when a measurement's orientation or meaning is ambiguous.

For regulated, safety-sensitive, health, children, food, cosmetics, or efficacy claims, omit unsupported claims and preserve unresolved review warnings. This skill does not certify advertising-law compliance.

## Workflow

1. Read `references/platform-profiles.json` and `references/category-playbooks.md`.
2. Build a fact ledger and product visual lock from the supplied images. Record asset IDs and evidence locators.
3. Choose only modules that answer buyer questions supported by the facts. Use a real image only when it adds evidence or useful visual context; compact fact-backed `text-only` modules are valid. The count is product-dependent; do not force a fixed 6–10 modules or repeat the same photo merely to fill sections.
4. Draft the module order, exact Korean copy, fact IDs, image source/generation approach, and export profile in `page-spec.json`.
5. Show the plan and copy for review. Do not generate images until the user has reviewed the page-spec and the existing `creative-production` execution boundary is satisfied. A text-only request stops at the plan.
6. For approved image work, use the current `creative-production` image-execution contract and its required `codex-imagen` route. Generate one text-free visual base per needed module. Keep the submitted prompt and reference assets traceable through the existing production history; do not add a separate approval or execution ledger.
7. Use the supplied real photos for exact product details. A generated background must not change product geometry, color, logo, controls, visible material, or included parts. Keep exact packaging pixels out of generative redraws; if identity cannot be preserved, mark that module concept-only and do not include it in upload-configured exports.
8. Run `scripts/compose_detail_page.py`, then `scripts/export_slices.py`, then `scripts/validate_output.py`. The composer writes one independent image per module and a stitched `detail-page-preview.jpg` for review. `module_images` profiles create no slices; `long_page_slices` profiles require an explicit slice height. Open and inspect every module and the preview, plus any profile-generated slices. Structural validation does not replace product-identity, copy, or visual review.
9. Report actual file paths, source profile, warnings, seller-center confirmations, and review status. Leave upload readiness unresolved until platform and human-review gates are actually satisfied.

## Platform routing

- `smartstore`: deliver individual ordered module images plus a stitched review preview, not one long upload raster. Use the 860 px recommended working width as a draft default, surface the documented 848/860 px discrepancy, and require seller-center confirmation. Respect the per-image file limit, warn when total page content exceeds the documented 4,000 px fold behavior, and verify actual image order in the seller editor.
- `coupang`: the public guide documents multiple detail-description images and preview, but does not publish a definitive detail-image width. Require a seller-center-confirmed width for upload-configured export. Do not reuse Coupang main-thumbnail dimensions as detail-image dimensions.
- `custom`: require an explicit width, image format, per-file limit, and confirmation source from the user or target platform before marking the profile upload-configured.

Platform rules live in `references/platform-profiles.json` with source URL, retrieval date, evidence level, and caveats. Seller-center-only limits remain warnings, not inferred hard rules.

## Page spec and output

`references/page-spec.schema.json` defines the machine-consumed render contract. Keep product facts and module fact references in the spec. The spec is an artifact for one page, not a production project ledger or approval database.

Expected output:

```text
<existing production root>/<product-slug>/
├── brief.json
├── page-spec.json
├── copy.md
├── modules/                 # independent ordered platform assets
├── detail-page-preview.jpg
└── manifest.json
```

`slices/` is added only for a profile whose `output_mode` is `long_page_slices`. A stitched preview is for review and must not be treated as an upload asset when the profile says `module_images`.

Use the existing `creative-production` and `recording-production-history` storage contract before writing production assets. Tests and sample images stay synthetic and inside temporary directories.

## Quality gates

- Every copy claim has valid, publishable fact IDs.
- Every visible fact points to a source image and a reviewable region.
- A `text-only` module cites publishable fact IDs and has no background image reference.
- Unknown product surfaces and unsupported claims are omitted.
- Exact text is composed by code, not rasterized by the image model.
- No text overflow, missing file, invalid profile reference, excessive configured file size, or silent format conversion.
- Every module is a separate image file in the exact `page-spec.modules`/manifest order; module-mode output has no slice files.
- Compare every output to the actual product images; inspect mobile-scale readability and module continuity.
- Report `plan_review`, `platform_profile`, `asset_visual_review`, and `upload_readiness` as separate observed states. Never infer user acceptance or seller approval from a validator pass.

## References and scripts

- `references/page-spec.schema.json`: page input contract.
- `references/platform-profiles.json`: Korean marketplace working profiles and evidence.
- `references/platform-source-policy.md`: policy verification and source-record rules.
- `references/category-playbooks.md`: buyer-question-oriented module choices.
- `references/production-workflow.md`: intake-to-delivery work instructions and profile-driven output contracts.
- `references/codex-imagen-prompt-pipeline.md`: per-module Codex Imagen prompt structure, provenance, and image-review pipeline.
- `references/prompt-recipes.md`: product-safe, text-free visual prompt recipes.
- `scripts/compose_detail_page.py`: deterministic text composition and preview rendering.
- `scripts/export_slices.py`: configured image slicing.
- `scripts/validate_output.py`: fact, file, platform-profile, and render validation.
- `scripts/test_page_builder.py`: synthetic regression fixtures.

Each executable script declares its Python/Pillow/Pydantic requirements in PEP 723 metadata and can run with `uv run`. The package installer does not install runtimes or dependencies. The target host must provide a Korean-capable font; specify its path in `style.font_path` when automatic system-font discovery cannot find one.
