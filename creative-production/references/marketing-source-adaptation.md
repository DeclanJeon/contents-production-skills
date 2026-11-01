# Video source adaptation and ad variants

Load only for requested video adaptation or video-ad variants. Standalone articles, social copy and campaign strategy are outside this video pack. Preserve source facts, requested voice/count, rights and the difference between a prepared file and publication.

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


## Video critique

Use [12 QA](../../video-production-assets/references/12-qa.md) for requested video concepts/scripts/results. Claims of retention or conversion need actual data.

## 6. Structured ad variation and campaign review

Applies only to requested video-ad variants; standalone still-ad/campaign operations belong to their non-video owner. The Higgsfield Paid-Ads presets map onto these operations; a preset name alone does not authorize spend, submission, or publication.

**Distinct-angle ad sets.** One set = several ads differing in a *named* angle (audience question, demonstrable contrast, practical benefit, curiosity, personal perspective), not in incidental wording. Record the angle per ad in the ledger. Claims, prices, features and evidence must trace to the supplied brief or checked sources; competitor figures need checked sources with URLs. Meta/placement formats are requested output specs, not defaults to invent.

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

