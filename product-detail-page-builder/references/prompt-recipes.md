# Module Image Prompt Recipes

Follow [`codex-imagen-prompt-pipeline.md`](codex-imagen-prompt-pipeline.md) for the full prompt contract, helper resolution, provenance, and post-generation gates. The image model produces a separate text-free visual base only for image-led modules. It does not compose the page or write customer-facing copy; text-only fact modules skip generation.

## Product lock

Repeat the relevant, source-backed constraints in every module prompt:

- Identify the exact supplied reference asset IDs and views actually submitted.
- Preserve only the product appearance visible in those references.
- Never invent hidden surfaces, dimensions, contents, ingredients, certification, compatibility, efficacy, or use outcomes.
- Do not redraw logos, package copy, nutrition panels, prices, claims, numbers, labels, badges, or watermarks.
- If exact packaging or readable label text is required, use the original source pixels or a reviewed deterministic composite; do not ask the image model to reproduce it.
- If product identity cannot be checked and preserved, return a concept-only asset and exclude it from upload-configured modules.

## Background plate

Use when the source product photo should remain exact and the module needs a different environment:

```text
Create one text-free background plate for module {{module_id}}.
Module purpose: {{one buyer question}}
Composition: {{empty placement area for the original product cutout}}
Background, lighting, and palette: {{approved visual direction}}
Do not draw a product, package, food item, logo, text, badge, number, or claim.
Return one standalone background image only.
```

The plate can be combined with a real product photo only when the chosen compositor supports that composition and the user-approved plan allows it. Do not use a background plate that changes the product or implies an unsupported use setting.

## Real-product visual base

Use only when the selected Codex Imagen helper supports the actual reference inputs and the source is sufficient for the requested view:

```text
Create one text-free visual base for module {{module_id}}.
Buyer question: {{one approved question}}
Reference assets: {{IDs, observed views, and supplied image regions}}
Product lock: {{shape, color, visible material, packaging, and included items}}
View and composition: {{camera angle, crop, scale, and focus}}
Negative space for later code-composed copy: {{location and amount}}
Visual direction: {{approved palette, lighting, and photographic treatment}}
Do not add text, redraw labels/logos, add claims or accessories, or reveal unseen details.
Return one standalone image for this module only.
```

Generated product scenes remain concept-only until direct review confirms identity and fact consistency. For food, use real product photographs for exact texture, serving size, and contents; generated-looking food is not evidence of the actual product.

## Deterministic composition

Compose reviewed Korean copy, numerical values, ingredient/nutrition tables, and legal or seller information with code after image review. Use the source-linked page-spec facts. Never pass copy to the image model as text to render, and never promote an unpublished fact into module copy.
