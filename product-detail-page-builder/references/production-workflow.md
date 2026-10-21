# Product Detail Page Production Workflow

Use this checklist for one requested product page. `creative-production` remains the coordinator and canonical writer; this workflow does not create a second approval database or project ledger.

## 1. Inspect the selected project and inputs

1. Read the actual user request and exact source files. Confirm file type, dimensions, views, and that each image opens.
2. Resolve the active production root. Reuse it only when it is the selected, relevant project; otherwise initialize the documented `Documents/studio_production/<project-id>` root.
3. Read `project.json`, actual outputs, approvals, and `.history` status before reusing a root. Do not overwrite existing versions.
4. Record the actual production prompt/method in existing `.history` before the first content output write.
5. Do not treat a filename, prior page, or another SKU's photo as evidence for the selected product.

## 2. Build the fact ledger and visual lock

For every possible copy claim, record:

- stable fact ID and exact value/units;
- `user`, `visible`, `official_source`, or `unconfirmed` source;
- a locator: intake field, visible image region, or official URL plus document/field and check date;
- whether it may be published.

Visible text proves what the supplied image displays, not necessarily the truth or substantiation of an advertising claim. Keep visible-but-unpublished claims in the fact ledger and never cite them from a module. For food, request the full label or official supplier data for ingredients/percentages, allergens, nutrition, food type, origin/manufacturer, storage, expiry, and regulated claims. Do not infer missing fields.

Create a product visual lock from the actual images: asset IDs, observed views, color/geometry/logo/label details, and explicitly unseen views. Do not generate a back, opened package, loose product, scale comparison, or use result without suitable evidence.

## 3. Decompose the page into modules

Read the selected platform and category playbooks. For every proposed module, specify:

| Field | Required decision |
|---|---|
| `id` | Stable ordered ID; prefer a zero-padded prefix such as `01-hero`. |
| `type` | Existing supported module type. |
| Buyer question | One decision the module answers. |
| Exact copy | Short approved Korean copy, if supported; otherwise no text. |
| `fact_ids` | Every factual statement used by the module. |
| Source assets | Exact product-image IDs and any authorized generated asset. |
| Image approach | Original photo, text-only fact panel, background plate, or a concept-only visual. |
| Layout/height | One image module's composition and content-dependent height. |
| Export profile | Width, format, per-file size, and confirmation state. |

Order sections from product recognition to product proof, experience, package details, required facts, and a useful close. Omit empty or unsupported sections instead of padding the page to a target module count. Keep price, discount, availability, shipping estimates, review counts, and purchase controls in the marketplace UI unless the user explicitly requests a static campaign asset.

## 4. Review before media execution

Show the ordered module plan, exact copy, fact references, image source/generation approach, and export profile. Record the user's actual response through the existing coordinator workflow; do not infer approval from silence or a validator pass. Text-only requests stop here.

## 5. Create module visuals

For each needed module:

1. Prefer an actual product photo for exact package, food texture, scale, or product details.
2. Use Codex Imagen only through the exact current helper contract selected by `creative-production`. Resolve its actual installed instructions at execution time. Do not infer command flags, model names, edit modes, reference weighting, or output paths.
3. Submit one module-specific, text-free visual brief at a time. Keep exact copy, prices, legal statements, labels, logos, and nutrition tables for deterministic composition.
4. For an exact package front, preserve the supplied pixels or make a verified cutout/composite; do not ask the image model to redraw small package text. If a generated image includes a product whose identity cannot be confirmed, mark it concept-only and exclude it from upload-configured assets.
5. Before generation, record the actual submitted prompt and reference asset IDs/hashes in the existing production history. After generation, record actual output paths and observed metadata.

If Codex Imagen or its current helper/authentication is unavailable, keep copy, module plan, deterministic layout, and other reachable work; report the exact image-generation blocker. Do not silently substitute another provider.

## 6. Compose and export

1. Create one independently reviewable file per module. Each file uses the selected profile width and its own content-driven height. A `text-only` module is rendered from the configured surface/accent/text style and verified facts; vertically balance its compact copy, omit its background image, and do not trigger an image-generation call.
2. Compose all approved copy deterministically from the `page-spec`; the image model never renders final text.
3. Create `detail-page-preview.jpg` by stacking modules in `PageSpec.modules` order. This stitched preview is for sequence, seam, and mobile-readability review.
4. For `module_images` profiles, deliver the individual `modules/` files as the platform assets. `export_slices.py` should emit no slices.
5. For a `long_page_slices` profile only, require an explicit slice height and create bounded slices from the preview. Never turn this into the default for a marketplace that accepts independent modules.
6. The SmartStore editor may remove gaps and may not preserve selection order. Manually arrange the images in the editor's vertical slice/group layout and inspect its preview before upload.

Expected bundle:

```text
<production-root>/<product-slug>/
├── brief.json
├── page-spec.json
├── copy.md
├── modules/
│   ├── 01-hero.jpg
│   └── ...
├── detail-page-preview.jpg
├── manifest.json
└── slices/                 # only for long_page_slices profiles
```

## 7. Validate and inspect

Run compose, profile-driven export, and bundle validation. Require:

- every module has valid fact and source-image references;
- module file order matches the spec and manifest;
- dimensions and byte limits match the confirmed/working profile;
- the stitched preview height equals the sum of module heights;
- module-image profiles have no declared slices; long-page profiles have complete, ordered slices;
- copy fits and is legible at mobile scale;
- every module, the stitched preview, and any slices have been opened and visually compared with the real input.

Report validator errors separately from warnings. Report `plan_review`, `platform_profile`, `asset_visual_review`, and `upload_readiness` independently. Seller confirmation, food-label substantiation, and user acceptance remain unresolved until actually supplied or performed.
