# Marketing and source-adaptation lanes

On-demand reference for content where audience, channel, or performance matters: campaign copy, social posts, comparisons, marketing strategy documents, and shortform video adapted from source media. Marketing rules apply only to a marketing request — a generic video request is not one. Publish-ready means prepared; posting or live platform changes need a separately requested scope.

## 1. Campaign and social workflow

1. **Define audience, channel, success metric first.** Views, saves, clicks, replies, conversions, and publish-readiness require different outputs.
2. **Inspect relevant evidence before producing.** Read the supplied sources; add trend, competitor or platform research only when the brief needs it. Separate documented facts from creative framing.
3. **Use the requested format** — single post, thread, carousel, comparison table, vertical video, CTA card, or explicitly scoped variants.
4. **Produce variants only when requested or delegated.** For an authorized A/B set, explain the distinct angle rather than changing incidental wording.
5. **Validate claims and assets.** Prices, model names, benchmarks, capabilities, product features and benefits must trace to the brief or a checked source. A feature name such as “Pro” does not establish that it is easier, faster, better, or more convenient. Use neutral wording when a benefit or the relationship between an offer and a launch is unspecified; do not invent a causal link such as “launch celebration.” Treat operational instructions such as “I’ll post it” as scope, not audience-facing copy. Never guess current competitor prices or model names; use official or clearly labeled third-party sources and record the URLs.
6. **Run applicable quality gates** — for text: source fidelity, tone, purpose, requested CTA and length; for video: actual streams/timing, representative frames and caption overlap. Apply the ending-card check only when that card is part of the brief.
7. **Report tradeoffs plainly** — e.g. contain-blur chosen because full crop clipped captions; third-party benchmark used because no official figure exists.

When the brief calls for variants, vary a relevant audience question, demonstrable contrast, practical benefit, curiosity or personal perspective. Avoid fabricated urgency, anecdotes, numerical shock and social pressure. CTA choices such as save, follow, link or reply apply only to a requested call to action.

## 2. Korean-language social conventions

- Match the supplied voice, register, audience and exclusions; short social copy need not erase a requested formal or documentary tone.
- Put relevant, sourced price comparisons in the body only when comparison is the requested purpose.
- Emojis, hashtags and rivalry/personal angles follow the brief rather than a universal count or default.
- Keep the requested variant count and format exact.

## 3. Marketing strategy documents

For a requested full launch/strategy document, cover the sections its decision needs: positioning, supported audience segments, channel-specific copy, discoverability, content formats, measurement and release dependencies. Website copy, SEO/AEO/GEO, OG cards, visual identity and growth-channel plans are optional branches, not compulsory deliverables. Coordinate with the existing design/brand owner rather than inventing a parallel brand kit.

Keep the document evidence-bound: capabilities only with brief or source support; no invented social proof, guarantees, urgency, or contact details. When architecture or product facts change, re-audit the strategy sections that depend on them and flag gaps (e.g. implemented FAQ pairs vs defined pairs) rather than declaring completion.
When positioning a product or offer, identify the competitive alternatives buyers actually use as their comparison yardstick. A feature is a differentiator only relative to those alternatives; do not substitute a product-feature list for buyer context (Dunford, *Obviously Awesome*, source 43; directly read rendition: `E:/Book/06_Book/originals/마케팅/Obviously Awesome How to Nail Product Positioning so Customers Get It, Buy It, Love It (April Dunford) (z-library.sk, 1lib.sk, z-lib.sk).md#L983-L1038`, READ-PARTIAL).
This excerpt supports customer-relative alternatives and differentiation only, not audience-demand ranking or a guarantee of market performance. The directly read rendition is 201161 bytes, SHA-256 `8f010e119d1f0cb67c1b7b09349b8ca31f43a41524ee056cb5ac93530081ecd2`; this identity travels with the installed reference. Other source-43 renditions retain their own locators in the canonical source index.

## 4. Source-media adaptation (shortform/vertical)

Production decisions to settle first:

- Preserve original speech/audio, add narration, or use source captions only?
- Are source captions soft, hard-burned, both, or absent?
- Should hard captions be preserved, masked, translated, replaced, or avoided through cut selection?
- Is an ending CTA requested? If so, what exact text, assets and duration are authorized?

**Caption strategy options:**

- `native_source_captions_only` — source hard captions already readable and synced. Preserve them; disable generated subtitle layers entirely rather than masking.
- `clean_generated_captions` — no hard captions, or they are removed/hidden by the chosen framing.
- `translated_or_curated_captions` — captions rewritten or translated; verify timing and prevent stacking on remaining source text.

**Framing rules:**

- Never stack generated subtitles on readable source hard captions unless intentionally designing a bilingual layout.
- For hard-burned captions that a 9:16 full crop would clip, prefer contain-blur (blurred duplicate background behind the original frame) or candidate re-selection over opaque masks — a misaligned lower-third mask reads as unfinished.
- Contain-blur filter shape: split the stream, scale+crop+gblur the background, and scale the foreground to the shared output dimensions while preserving its display aspect ratio; set SAR to 1 on every concat input. In an FFmpeg 8.1.2 synthetic case, a 64×64 SAR 2:1 clip failed to concatenate with a 64×64 SAR 1:1 clip before normalization. Scaling the SAR 2:1 clip to 128×64 and concatenating it with a 128×64 SAR 1:1 card after setting SAR 1 on both inputs succeeded. This verifies one filter path only; inspect the actual output.
- Prefer FFmpeg filter solutions over neural inpainting for caption handling unless a GPU/cloud approach is explicitly acceptable.
- If immersion (full crop) vs caption integrity (contain-blur) conflict, prefer caption integrity unless the user explicitly values immersion.

**Adaptation QA checklist:**

- Final file exists, non-empty; `ffprobe` confirms duration, resolution, streams, file size; record a checksum for traceability.
- Generated-subtitle overlap count is zero, or the generated subtitle layer is explicitly disabled for native-caption variants.
- Visually review representative frames and, when present, the ending card. Contact sheets alone do not verify subtitle sync, reading time or glyph rendering.
- Subjective publish-readiness requests include a viewer-style review (naturalness, subtitle comfort, content flow, framing/caption clipping, unnecessary overlays, CTA readability), not only automated checks.

## 5. Content critique gate

For a requested concept/script/draft review, use the canonical [production content-quality gate](../../video-production-assets/references/12-qa.md) under “내용 품질 판정”. Apply its purpose-appropriate evidence and repair criteria to text, not its unrelated media-inspection modules. This reference does not keep a second scoring rubric.

Marketing critique can compare requested audience/channel variants, but claims of improved views, retention or conversion need actual measurements. User acceptance and execution/publication authorization remain separate.

## 6. Structured ad variation and campaign review

Applies when the request is an advertising set on a paid platform. The Higgsfield Paid-Ads presets map onto these operations; a preset name alone does not authorize spend, submission, or publication.

**Distinct-angle ad sets.** One set = several ads differing in a *named* angle (audience question, demonstrable contrast, practical benefit, curiosity, personal perspective), not in incidental wording. Record the angle per ad in the ledger. Claims, prices, features and evidence follow §1.5 exactly; competitor figures need checked sources with URLs. Meta/placement formats are requested output specs, not defaults to invent.

**VOC / evidence-driven ads.** Customer-review-derived ads may quote or paraphrase only supplied reviews or checked sources. A review is evidence for the claim it makes and nothing more — do not generalize one reviewer's experience into product-wide capability, and do not fabricate testimonials, ratings or counts.

**Single-variable variants.** Hold every other variable constant and change exactly the named one:

- Headline-only set: identical visual, layout, product framing, offer and branding; the headline text differs.
- Hook-only video set: identical body, order, demo, product and CTA; only the opening hook differs.
- Report the held-constant list, so a reviewer can confirm the set is genuinely single-variable.

**Placement resizing.** For 1:1 / 4:5 / 9:16 adaptations, re-check per aspect: copy legibility at actual viewing size, text not clipped or crowded by safe areas, product/branding intact and uncropped, hierarchy preserved (not a blind center-crop). A resized ad that loses the offer or brand mark is a failed adaptation, not a variant.

**Ad localization.** Translate the copy while preserving the offer, price, legal/claim meaning and brand voice. Re-check reading time, line breaks, glyph rendering and any culture-specific claim. Do not localize a claim into a stronger claim than the source supports. Policy/compliance wording follows the target market's requirement when supplied; never invent it.

**Reference-video persuasion-structure reuse.** Reproducing a reference video's *persuasion structure* (hook type → problem → proof → offer → CTA order, pacing, on-screen beat rhythm) is permitted; copying its footage, voice, script, performer likeness, music or branded assets is a rights violation unless the user holds or supplies those rights. Recreate structure and craft, not content.

**Campaign review from data.** Scale / pause / test recommendations require actual supplied campaign data (impressions, spend, CTR, CPA/ROAS, frequency, window). A recommendation without measured inputs is blocked, not assumed. State the metric, the window and the decision rule per recommendation (e.g. "CPA above target with volume → pause", "cheap CPA but low reach → scale"), and separate what the data shows from what to test next. Never present predicted lift as measured.

**Boundaries kept distinct:** producing ad *copy/design* (this lane) ≠ generating or spending on provider media (execution approval) ≠ publishing or changing a live campaign (publication approval). Package image policy applies unchanged: Higgsfield **image** submission is ineligible — still-ad assets come from the authorized image executor, and a Higgsfield image recipe stays craft/reference only.

