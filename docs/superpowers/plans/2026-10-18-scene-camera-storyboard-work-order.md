# Work Order 1: Scene-Specific Camera Treatment in Storyboards

**Design:** `docs/superpowers/specs/2026-10-18-camera-storyboard-blender-orchestration-design.md`
**Owner:** One OMO worker session
**Mode:** Documentation/skill-contract implementation only; no media generation or runtime execution.

## Goal

Make complete production storyboards explicitly design and compare a motivated camera treatment per scene while preserving shot-level camera fields and allowing intentional repeated setups.

## Owned files — edit only these

- `video-production-assets/references/storyboard-contract.md`
- `video-production-assets/references/06-shots.md`
- `storyboarding-video/SKILL.md`

Do not edit the design document, other work orders, `README.md`, `manifest.json`, camera/Blender specialist files, validators, examples, QA artifacts, installed copies, or production outputs.

## Required changes

1. Add the design's scene-camera intent record to complete production-storyboard output. Link it to existing `scene_id` and shot IDs; do not create another ledger or new required project schema.
2. Require the board to compare adjacent scenes by purpose, audience-knowledge change, POV/axis, framing progression, static/moving choice, and reveal/action timing.
3. Require a reason for intentional repeated camera treatments. Do not force numeric novelty, a camera move in every scene, or alternatives for every shot.
4. Preserve all current beat→scene→shot→panel coverage, technical slots, focus/camera ownership, blockers, and image/text-only boundaries.
5. Define fail-able storyboard acceptance checks as in design §2.4; distinguish planned text from inspected image/previs evidence.
6. Keep scene intent as a compact section/table in the existing board artifact. Do not add machine-readable schema fields unless the current contract already requires them.

## Forbidden scope

- No new skills, global ledgers, schema/version changes, invented cinematography rules, numeric camera uniqueness scores, or forced one-move-per-scene rule.
- No image generation, Blender execution, render, filesystem writes outside the three owned docs, README/manifest edits, or commits.
- Do not normalize/convert line endings or rewrite whole files. Preserve unrelated existing edits.

## Acceptance evidence

- Every complete production scene has a linked camera-intent row.
- Shot-level camera requirements remain intact and are not replaced by the summary row.
- Adjacent scene relation and intentional reuse are reviewable; camera novelty is motivated, not mechanically enforced.
- Narrow rough-panel/prompt-only requests and simple N/A cases remain narrow.
- Links/headings resolve and no existing owner or approval boundary is contradicted.

## Return

Report exact changed files, a concise change summary, any unresolved conflict with design §3 Blender wording, and checks actually run with observed results. If a conflict appears, stop before changing another owner's files and message the coordinator.
