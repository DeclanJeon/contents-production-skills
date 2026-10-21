# Codex Imagen Module Prompt Pipeline

This reference defines the prompt content and review contract for Codex Imagen still-image assets used by the product-detail builder. It does **not** define a CLI/API invocation. At execution time, `creative-production` must resolve and read the exact current `codex-imagen` helper instructions for supported references, edit modes, output destinations, and request syntax. If no matching helper is available, report the blocker; do not substitute `image_gen`, another provider, or guessed command flags.

## Pipeline

### A. Freeze the module brief

Before authoring a prompt, resolve these fields from the reviewed page-spec:

- ordered `module_id` and one buyer question;
- asset role: source-photo placement, background plate, actual product view, or concept-only scene;
- fact IDs the eventual module will communicate;
- exact input asset IDs, local paths, observed views, and hashes;
- product-lock anchors visible in each source image;
- output composition, requested negative space for later text, brand visual direction, and module aspect/height class;
- claims and visual elements explicitly forbidden.

Do not put unconfirmed claims or exact final page copy into the image prompt. The image model creates a visual base; Pillow/code composes approved words and numbers afterward.

### B. Select the image lane

| Module need | Preferred lane | Upload handling |
|---|---|---|
| Compact factual copy or a verified specification table | `text-only` module composed with code; no image prompt. | Use only publishable fact IDs; missing facts stay out of the card. |
| Exact package, logo, or readable label | Use the real supplied pixels or a reviewed deterministic cutout/composite; do not regenerate label text. | Upload-configured only after visual identity inspection. |
| Background/lighting plate behind an exact product photo | Generate a background plate without product or text, then composite the real product photo if the existing implementation supports the requested composition. | If the exact product cannot be assembled faithfully, omit the generated scene or mark it concept-only. |
| Real product texture, portion, or scale | Request a real product photo. | Do not present model-invented food form or dimensions as the actual product. |
| Editorial mood/concept scene | Generate only when the plan and execution scope allow it. | Mark concept-only until the depicted product identity and claims are visually verified. |
| Nutrition, ingredients, certification, price, or legal table | Never image-generate. Use verified source data and deterministic text composition. | Facts remain blocked when evidence is missing. |

### C. Compose one prompt per module

Use a shared visual anchor for continuity, then add only the module-specific scene. Skip image generation for `text-only` factual modules. For image-led modules, a prompt should name the module, scene purpose, exact references, product-lock anchors, composition, lighting/background, desired negative space, and exclusions. Request one independent visual base; never request the full stitched page in one image-generation call.

```text
Create one text-free visual base for product-detail module {{module_id}}.

Module purpose / buyer question:
{{one_question}}

Image role:
{{source_photo | background_plate | actual_product_view | concept_only}}

Reference assets actually supplied to this request:
{{asset_id, path, hash, observed_view for each reference}}

Product lock — preserve only what the references show:
{{verified shape, color, logo/package placement, visible material, and included parts}}
Do not infer hidden views, ingredients, size, performance, origin, certification, or use results.

Composition:
{{camera/view, crop, product placement, focus, and reserved negative space for later code-composed copy}}

Visual direction:
{{approved palette, background, light, contrast, and photographic treatment}}

Do not render any words, letters, numbers, logo redraws, badges, claims, nutrition panels,
watermarks, UI, or price. Do not add unseen product parts or extra package contents.
Return one standalone image for this module only.
```

The template is a semantic prompt packet, not a verbatim helper invocation. The active helper's instructions determine which fields are prompt text, reference inputs, edit instructions, or output settings. Do not claim a reference was consumed unless it was actually submitted through the helper's supported input mechanism.

### D. Submit and trace

1. Store the actual submitted prompt and actual reference asset IDs/hashes through the existing project `.history` workflow before the image call.
2. Make one request per module. Parallelize only if the helper contract supports it and each returned result can be mapped unambiguously to its module ID.
3. Record the actual helper, confirmed model/version, request/result identifier if provided, output path, and observed file metadata. Unknown values remain unknown.
4. Do not edit prompt provenance after the call to make it resemble an intended prompt; retries are new attempts with new actual prompts.

### E. Inspect and compose

Before composition, open every returned asset. Compare it to the product-lock anchors, verify there are no invented labels/text/parts, and check crop and visual intent. A drifted or unreadable package is rejected, revised, or kept concept-only; it is never silently placed in an upload-configured module.

After visual acceptance, the deterministic compositor adds exact reviewed copy. The module image is the upload unit; `detail-page-preview.jpg` only shows the ordered module sequence for QA. Upload order and visual spacing must be checked in the target seller editor.

## Beef99 prompt-planning example

For the current supplied front-package image, `01-hero` should use the real front photo as the exact package image. If a background plate is later requested, generate only an empty cream/red food-photography backdrop with safe space for the untouched source package to be composited; do not ask Codex Imagen to redraw “TERRA VERA,” “BEEF 99,” the ingredients, nutrition, or claim text. A loose-chip close-up requires an actual loose-chip reference photo; until supplied, omit that module or label any generated food image concept-only.

The front currently displays “High-protein chips” and “100% Natural.” Their visibility in a reference does not independently substantiate the claims. They remain unpublished facts and are excluded from generated prompt content unless official supporting data is supplied and reviewed.
