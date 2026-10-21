# Platform Source Policy

## Evidence levels

- `official`: current public seller documentation gives the exact rule.
- `official_partial`: official material supports some fields, but other fields conflict or require the seller editor.
- `seller_backend_confirmation`: the exact rule is not publicly verified; check the live seller-center field before upload.
- `operational_baseline`: a working default only; never present it as a platform guarantee.

Every platform field records a source URL, publisher, retrieval date, and evidence level. Do not infer detail-description requirements from listing-thumbnail requirements.

## SmartStore

The official help center currently contains an 860 px recommended detail-description width, and another help page lists 848 px. Use 860 px as the preview working width only; warn that the seller editor is authoritative until the seller confirms. The help center also describes a 20 MB per-image limit and fold behavior when the detail description exceeds 4,000 px (initial 3,000 px shown before expansion). Warn on aggregate page height over 4,000 px rather than silently discarding content. A 3,000 px export slice is an operational choice, not an official maximum single-image height.

Sources:

- https://help.sell.smartstore.naver.com/faq/content.help?faqId=5767
- https://help.sell.smartstore.naver.com/faq/content.help?faqId=3923

## Coupang

The public marketplace guide says detail descriptions can be uploaded as multiple image files, authored in the editor, or supplied as HTML, and recommends previewing before saving. The guide's explicit size values describe listing images, not the detail-description image set. Do not reuse those listing-image dimensions, formats, or limits for this builder. Require the seller to confirm width, per-image file size, and other constraints in WING before marking an export upload-configured.

Source:

- https://marketplace.coupang.com/register?rf=MARKETPLACE

## Reverification

Recheck official sources when implementing a new platform, when the profile's verification window expires, or whenever a public help page and seller-center behavior differ. If public documents conflict, retain both sources and expose the conflict. Do not silently choose the stricter or more convenient number as authoritative.
