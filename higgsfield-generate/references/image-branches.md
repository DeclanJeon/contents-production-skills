# Image model branches — craft/reference only (ineligible in this package)

Package policy (see `package-gate.md`) excludes Higgsfield image generation and image edits:
in this package none of the recipes below may be submitted. They are preserved for model
selection knowledge and for contexts where this skill runs without the package constraint —
and so that a request can be routed to the right owner or an authorized eligible executor.
Do NOT treat a listed model as currently available or priced; check `higgsfield model get
<jst>` in any context where image generation is actually permitted.

## Routing first — specialized image owners

| Request | Owner |
|---|---|
| Complete brand identity, logo system, palette, typography, brandbook, packaging, signage, coordinated branded asset suite | `higgsfield-brandkit` |
| YouTube thumbnail, Shorts cover, Instagram video cover | `higgsfield-youtube-thumbnail` |
| Brand product visual (Pinterest pin, lifestyle, hero banner, ad pack, virtual try-on) | `higgsfield-product-photoshoot` |
| Marketplace listing main/secondary/A+ images | `higgsfield-marketplace-cards` |
| Branded ad image with avatar + product (Marketing Studio shape) | Marketing Studio Image (`marketing_studio_image`) |
| Train a real person's face for reuse | `higgsfield-soul-id` |

## Image model taxonomy (selection craft)

- Soul Character (reference id from `higgsfield-soul-id`) → Soul 2.0 (`text2image_soul_v2`) for stills, Soul Cinema (`soul_cinematic`) for cinematic.
- New original person — UGC, editorial, fashion, lifestyle → Soul 2.0.
- Cinematic still frame → Soul Cinema (`soul_cinematic`).
- Character sheet, one-shot face from reference photos, or face edit on a real photo → Seedream 5.0 Pro (`seedream_v5_pro`).
- Locations / environments / no-people scenes → Soul Location.
- Logo, icon, vector-like illustration, brand mark, controlled-palette graphic → Recraft V4.1 (`recraft_v4_1`, often with `--model_type vector`).
- Cartoon or illustrated characters, heavily textured photos → Nano Banana 2 (`nano_banana_flash`). The id `nano_banana_2` is an alias for Nano Banana Pro, not Nano Banana 2.
- Default for everything else → GPT Image 2.5: graphic design, UI, banners, typography, product concepts, editing, high-fidelity general generation.
- Cheaper or faster on user request → Nano Banana 2 Lite (`nano_banana_2_lite`) for reference edits, Z Image for drafts.

## CLI shapes (craft reference)

```bash
higgsfield generate create gpt_image_2_5 --prompt "neon city at dusk" --aspect_ratio 16:9 --resolution 2k --wait
higgsfield generate create nano_banana_flash --prompt "anime character concept, expressive pose" --image ./ref.png --wait
higgsfield generate create text2image_soul_v2 --prompt "..." --soul-id <soul_ref_id> --quality 2k --wait
higgsfield generate create marketing_studio_image --prompt "..." --aspect_ratio 1:1 --resolution 2k --wait
```

Soul image quality: for `text2image_soul_v2` and `soul_cinematic`, pass `--quality 1.5k` or
`--quality 2k`. These are UI-facing tiers; the backend maps them to `720p`/`1080p` and
model-specific dimensions from the selected `--aspect_ratio`. `soul_location` has no quality
selector; it uses fixed dimensions per aspect ratio.

Soul style presets: `text2image_soul_v2` accepts `--style_id <uuid>`; list curated styles
with `higgsfield preset list soul-v2` and pass the chosen id. `--style_id` combines with
`--soul-id` but not with an image reference. `soul_cinema_studio` also accepts `--style_id`.
