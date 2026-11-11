# Product-photoshoot modes and interview taxonomies

Load this before mode selection or the pre-generation interview. These taxonomies are craft
knowledge — they serve the authorized executor path truthfully-scoped work and preserved
backend contracts; they do not make an ineligible submission eligible.

Contract scope (2026-10-17): CLI 1.1.26 `product-photoshoot create --help` directly read;
it requires a mode string but does not enumerate these ten slugs or verify their aspect,
slide-count or private template semantics. Preserve this historical taxonomy for brief
classification; verify selected slugs/limits against a current official contract before
depending on them. Interview tie-breakers are authored routing rules, not provider validation.

## Modes

| Mode | When user wants… |
|---|---|
| `product_shot` | Product on neutral / studio / catalog background |
| `lifestyle_scene` | Product in real-world environment, hands, action, atmosphere |
| `closeup_product_with_person` | Tight crop with hands / partial face — beauty application, holding, demonstrating |
| `moodboard_pin` | Vertical 2:3 Pinterest-native aesthetic, moodboard feel |
| `hero_banner` | Wide-format website / email / campaign header |
| `social_carousel` | 3–10 connected slides for IG / LinkedIn / Facebook |
| `ad_creative_pack` | Coordinated pack of static ad variants for Meta / TikTok / Pinterest / Google Ads |
| `virtual_model_tryout` | Product worn or used by an AI-rendered model |
| `conceptual_product` | Surreal / CGI-style / levitating / splash / sculptural product |
| `restyle` | Transform an existing image's aesthetic, mood, or seasonal context |

## Mode selection

Pick by intent, not surface keyword. When two modes could apply, prefer the more specific one.

An object name or count does not determine mode. “Three photos of this mug” leaves
`mode` unresolved: reuse count=3 and ask for the intended setting/use. Do not silently
choose `product_shot`. A supplied mode or a current inspected contract that explicitly
determines it resolves the field; historical defaults and the product category do not.

- product + neutral / clean / white / studio / catalog / Shopify → `product_shot`
- product + scene / in use / kitchen / outdoor / cafe / gym → `lifestyle_scene`
- hands holding / face with product / beauty application / demonstrating → `closeup_product_with_person`
- Pinterest, pin, vertical pin → `moodboard_pin`
- hero, banner, website header, landing page, email header, wide format → `hero_banner`
- carousel, slide post, multi-slide, swipeable → `social_carousel`
- ads, ad pack, paid social, Meta / TikTok / Pinterest ads → `ad_creative_pack`
- model wearing, virtual try-on, on body, fashion shoot, lookbook → `virtual_model_tryout`
- levitating, floating, splash, frozen motion, surreal, CGI, sculptural → `conceptual_product`
- modify EXISTING image's aesthetic, mood, season — without changing subject → `restyle`

Tie-breakers:
- "Pinterest pin of my product on a kitchen counter" → `moodboard_pin` (Pinterest is the platform)
- "Hero banner showing my product in use" → `hero_banner` (banner format wins)
- "Carousel of my product in different scenes" → `social_carousel` (multi-slide wins)
- "Closeup of person applying my serum" → `closeup_product_with_person` (specific genre wins)

## Pre-generation interview

Ask only materially unresolved questions, at most 4 short questions; zero is valid when the brief is complete. Use labeled options when helpful; the scripts below are menus, not a fixed minimum. Reuse supplied answers.

### Type A — uploaded a product photo, "make me images / photoshoots"

1. How many? `[1 / 3 / 5]`
2. What style/mood? `[Clean studio / Lifestyle / Conceptual / With a model / Other]`
3. Where will you use them? `[Shopify / Instagram / Pinterest / Paid ads / Website hero]`
4. Brand colors to match? (skip if obvious)

### Type B — uploaded a product photo, named a use case

E.g. "make ads for my product", "make a Pinterest pin", "make a hero banner". Mode is obvious. Ask only the gaps:

1. How many? (if multi-output mode)
2. What's the offer / mood / hook?
3. Anything in particular to emphasize?

### Type C — text only, no product photo

1. Can you supply a product photo? It provides visible attributes (shape, color, packaging, markings) to preserve; inspect actual outputs against those attributes rather than assuming higher fidelity.
2. If not, describe the product — category, packaging, color, distinctive features.
3. What style? (same options as Type A)
4. Where will you use it?

### Type D — uploaded existing image, "redo / change vibe / different version"

→ `restyle`

1. What aesthetic? `[Clean girl / Cottagecore / Quiet luxury / Dark academia / Y2K / Other]`
2. Seasonal context? `[Christmas / Valentine's / Halloween / Black Friday / None]`
3. What to preserve, what to change? (only if ambiguous)

### Type E — model wearing a product (fashion, accessories)

→ `virtual_model_tryout`

1. Model archetype? (suggest 2–3 based on brand audience)
2. Environment? `[Studio clean / Outdoor natural / Street style / Editorial / Home cozy]`
3. Framing? `[Full body / Three-quarter / Waist up / Closeup on product area]`

### Type F — vague request, unclear subject

E.g. "make me something cool for my brand".

1. What product or topic?
2. Goal? `[Sell on a marketplace / Build awareness / Run paid ads / Update website]`
3. Upload a reference image?

After answers → return to the relevant Type A–E.
