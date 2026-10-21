# Module-First Product Detail Page Design

## Status

This design supersedes the SmartStore long-page-slice delivery default described in the 2026-10-18 builder design. It keeps the original page-spec, fact-evidence, Pillow composition, production-history, and single-coordinator boundaries. SmartStore and Coupang deliver ordered module images; a stitched image is a QA preview. Long-page slices remain available only for a target profile that explicitly requires them.

## Problem

The first Beef99 builder preview repeated one front-package photo in three panels, used tall text-only areas, and exported one 2,220 px image. It demonstrated fact tracking and deterministic composition, but it did not form a convincing product story or match the requested one-image-per-section workflow. The existing `long-detail-v2` page is a different product-photo source and remains historical; it is not the design baseline for the supplied front-package image.

The new output contract must keep these distinct:

1. An **image module** is an independently reviewable and replaceable page section.
2. The **stitched preview** shows vertical flow and transitions for review; it is not the default upload asset.
3. **Long-page slices** are a separate platform mode, used only when the selected seller profile requires a continuous raster.

## Structural review of real storefronts

These observations describe public page structure, not measured conversion performance.

| Public page | Observed order and content | Design implication |
|---|---|---|
| [Carnivore Crisps Beef Brisket](https://carnivorecrisps.com/products/carnivore-crisps-beef-brisket) | Nine-image product gallery; title, price, size options, purchase/subscription controls; short product description and feature list; reviews below. | Keep purchase controls and changing commerce values in the storefront UI. Give the image sequence product views, evidence-backed claims, and use context instead of reproducing price/cart UI inside images. |
| [Korean Butchery Beef Jerky](https://koreanbutchery.com/products/beef-jerky) | Flavor selection, purchase controls, Korean description, weight, delivery support, and product images. | Resolve variant and package facts clearly; keep the story concise and flavor-specific. |
| [Costco Korea Koong Beef Jerky](https://www.costco.co.kr/Foods/Dried-Products/Jerky/Koong-Beef-Jerky-100g-x-5/p/622041) | Product introduction, pack composition, features and serving ideas, followed by a compact specification area for food type, producer, expiry, weight, ingredients/allergens, nutrition, storage and safety. | A food page needs a distinct, legible evidence-backed information section; mood photography cannot replace the food label. |
| [SmartStore SmartEditorONE guidance](https://help.sell.smartstore.naver.com/faq/content.help?faqId=5450) | Multiple selected images can be grouped with collage/slice layouts. Uploaded images may have gaps removed; their order is not guaranteed and must be adjusted in the editor. | Export separate files, use the vertical slice/group layout rather than collage for page sections, manually set the order, and inspect the seller preview. |

## Design decisions

### Independent module assets

- One module answers one buyer question and maps to its own `PageModule`, `modules/<id>.jpg`, fact IDs, source image IDs, and visual-review result.
- A `text-only` module is appropriate for a compact fact/table card when another photo would only repeat the hero. It uses the page surface/accent style, cites publishable facts, and has no image-generation/background reference.
- The `PageSpec.modules` array and `manifest.modules` array are the canonical order. Use stable IDs with zero-padded ordinal prefixes such as `01-hero` and `02-product-form` to make manual editor ordering easier; never depend on filenames alone.
- All modules use the seller-confirmed width and per-image file limit. Heights vary by content; do not pad every section to the same height.
- Generate `detail-page-preview.jpg` by stacking the ordered module files without resizing them. This image is for visual QA and continuity review.
- For `module_images`, no `slices/` directory is generated. A `long_page_slices` profile may create slices only when its verified platform contract explicitly asks for a continuous image.

### Page sequence

Choose only sections supported by evidence. The Beef99 candidate flow is:

1. **Hero / identity** — front package, exact brand and product name.
2. **Product form** — actual unpackaged beef-chip photo and scale, not a picture of chips printed on the pouch.
3. **Composition / differentiation** — exact product-label facts, only after the full label substantiates them.
4. **Texture / serving context** — real product photography and an approved serving suggestion; no invented texture or result.
5. **Pack size** — verified 30 g and package configuration.
6. **Food facts** — food type, ingredients, allergens, nutrition, origin/manufacturer, storage, expiry, and other required label fields from official data.
7. **Brand close** — only if supplied brand material adds useful information; otherwise end with a clean packshot.

The order may change when the actual product, buyer question, or available evidence differs. Do not force a seven-module count or create a generic closing section merely to lengthen the page.

### Visual system

- Derive the palette from the actual pack: package red as an accent, ivory as the main canvas, and dark brown/burgundy for text. Avoid large repeated red slabs that compete with the package.
- Keep one shared horizontal grid, consistent safe margins, baseline alignment, and edge-to-edge module joins. Use full-width product photos, compact factual panels with vertically balanced text-only cards, and varied image scale; avoid repeating the same split-card layout.
- Use the actual package image for exact logos and label text. Use actual loose-product photographs for product texture. Do not ask the image model to recreate a logo, package label, price, ingredients, badge, or nutrition panel.
- Keep headings short and body copy to one evidence-backed point per module. Do not rasterize price, discount, delivery estimate, options, review count, or other values already owned by the live storefront.
- Inspect both each standalone module and the stitched mobile-width preview. Fix clipped text, accidental blank panels, visual seams, repeated photography, and ambiguous fact presentation before delivery.

## Beef99 evidence and unresolved inputs

The supplied image is a front-package photo. It shows the brand/product lettering, a `BEEF 99% / SALT / VINEGAR` text row, 30 g, and the printed phrases “High-protein chips” and “100% Natural.” The latter claims remain visible inside the authentic package photograph even when omitted from new copy. Until substantiation is supplied, the manifest must warn and upload readiness must stay blocked.

Before a final food-detail page is considered complete, obtain:

- the back/side Korean label or supplier-approved source for full ingredients and percentages, allergens, nutrition, food type, origin, manufacturer, storage, and expiry;
- an actual open-pack/loose-chip image and, if size/portion comparison matters, a real scale reference;
- evidence supporting “High-protein” and “100% Natural,” or an approved current package image without those claims.

Never retouch or erase text from the supplied package to make the claims disappear. The existing three-module draft is a visual prototype only and should not be treated as a final product story.

## Codex Imagen boundary

Codex Imagen remains the default requested still-image executor under `creative-production`. The module prompt pipeline is specified in [codex-imagen-prompt-pipeline.md](../../../product-detail-page-builder/references/codex-imagen-prompt-pipeline.md). At execution time, resolve and read the exact installed helper contract; do not infer its CLI flags, model, supported references, or output behavior. No matching Codex Imagen skill/tool was available in the design session, so the prompt schema below is an authored content contract, not a verified invocation syntax.

## Output and acceptance

```text
<production-root>/<product-slug>/
├── brief.json
├── page-spec.json
├── copy.md
├── modules/
│   ├── 01-hero.jpg
│   ├── 02-product-form.jpg
│   └── ...
├── detail-page-preview.jpg      # review only
├── manifest.json
└── slices/                      # only for long_page_slices profiles
```

Acceptance:

- Each module is independently deliverable and has an explicit order, purpose, fact IDs, and source asset references.
- SmartStore module mode exports the module files and stitched preview without claiming that the preview is the upload file.
- The actual seller editor order is manually checked; the preview matches that order.
- Unsupported food claims and missing label fields remain visibly unresolved, never transformed into marketing copy.
- Automated validation passes; every module and the mobile-width preview receive direct visual inspection.
- `manifest.readiness.platform_profile`, `asset_visual_review`, and `upload_readiness` retain their true status; no upload/publish claim follows from render success.
