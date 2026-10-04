# Complete Storyboard Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development or superpowers:executing-plans. Steps use checkbox tracking. User explicitly requests design, work order and immediate implementation; no additional design approval pause. Parent integrates and runs checks once after edits; workers do not run tests/lint/build/formatters mid-flight.

**Goal:** Every production storyboard includes all shot specifications and traceable visual story coverage, with an image-only review gate before video handoff.

**Architecture:** Keep creative-production as coordinator and project.json as production authority. One shared storyboard contract links existing craft/runtime specialists; a selective structural validator and indexed image splitter enforce mechanical coverage, not artistic quality.

**Tech Stack:** Markdown skills, existing Python 3 standard-library validation, Pillow only for image extraction.

**Spec:** `docs/superpowers/specs/2026-10-04-complete-storyboard-design.md`

## Global Constraints

- Preserve schema_version=1.1 and existing plan/delivery profiles; detailed storyboard extension is optional for ordinary projects.
- Canonical new fields, semantics and requirements are exactly those in the Spec; no new skill IDs, global state, model catalog or spend authority.
- Reuse supplied assets/IDs/versions. Text-only output remains text. Only actual viewed/listened/generated output gets that status.
- Missing Blender or requested media executor blocks that execution, not reachable planning. Never substitute a numerical preview for Blender evidence.
- No git commit/push, installation, paid media or publication as an implied task. Package version uses existing bump/check/sync tooling.

## Review Focus

1. Uploaded synopsis/board stays locked; repair within staging scope, escalate story-changing repairs rather than inventing story.
2. Character-free/data/no-audio requests still get full coverage without fictional cast or forced narrator/music.
3. Camera movement and contact/reveal require intermediate panels where one still cannot show causality; no fixed three-images-per-shot policy.
4. Existing validated projects are not forced into the storyboard extension; complete storyboards cannot hide a missing scene/beat behind valid timeline.
5. Extraction preserves ID/order/crop and rejects unsafe paths, overlapping/out-of-bounds crops and overwrite before writing output.

## File Ownership and Tasks

### Task 1: Planning/character routing

**Files:** creative-production/SKILL.md, creative-production/references/production-routing.md, orchestrating-video-preproduction/SKILL.md, orchestrating-video-preproduction/references/video-direction.md, developing-video-synopses/SKILL.md, designing-video-character-sheets/SKILL.md, video-production-assets/references/22-dialogue-lipsync.md.

**Consumes:** supplied choices and canonical `storyboard-contract.md` trigger, not a second coordinator.
**Produces:** routed upstream decisions, versioned synopsis beat map, voice/persona/speech handoff.

- [x] Read exact source sections and current craft contracts; baseline probes in qa/storyboard-baseline.json show variable panel counts, informal linkages and unsupported labor estimates under current guidance.
- [x] Add runtime/chapter/series decision, reference intake, emotion and synopsis QA/revision checkpoints for complete production; preserve single-artifact scope.
- [x] Add supplied sheet/voice inspection and persona-to-dialogue/narration timing handoff; silence is not a demand for narration.
- [x] Add strong conditional pointers for production storyboard integration and image-only gate, removing contradictory blanket downstream-only technical-planning boundaries.

### Task 2: Canonical storyboard contract and visual gate

**Files:** new video-production-assets/references/storyboard-contract.md; modify storyboarding-video/SKILL.md, video-production-assets/SKILL.md, references/06-shots.md, references/preproduction-review.md, references/12-qa.md, references/contract.md, assets/storyboard-panels.csv, creative-production/references/video-generation-planning.md.
Integration ownership also includes camera-spatial-design/SKILL.md, blender-previsualization/SKILL.md and the condition-scoped preproduction handoff pointers in higgsfield-video-explainer/SKILL.md and higgsfield-video-replicate/SKILL.md. These preserve the same board IDs and gate without changing executor formats or creating unrequested packages.

**Consumes:** Task 1 decisions, existing project/camera contracts.
**Produces:** required cut specification and canonical extension consumed by Tasks 3/4.

- [x] Publish required fields and complete flow from Spec once in the shared contract; references use condition-keyed pointers.
- [x] Integrate camera-spatial/Blender and per-cut VFX/speech/audio metadata before panel generation.
- [x] Require exact image-slot accounting, clean images plus external labels, full beat/scene/shot coverage and image-only chronological review.
- [x] Add KEEP/FIX/unverified, why/how/preserve/prerequisites/grounded-time/owner/recheck and bounded correction loop.
- [x] Connect extracted clean cuts and first/peak/end states to timed prompts without selecting model/spend prematurely.

### Task 3: Structural coverage validator

**Files:** new video-production-assets/scripts/validate_storyboard.py, test_validate_storyboard.py.
**Interface:** `validate_storyboard(project: dict, base_dir=None, require_images=False) -> list[str]`; CLI accepts project path, --base-dir, --require-images. Reuses validate_project.validate(profile='plan') and documented optional extension.

- [x] Write behavior regressions for omitted/reordered beats, orphan scene, missing shot panels/endpoint roles, invalid technical/voice/audio references and real image absence. Show baseline missing-story coverage accepted by existing plan validation before update.
- [x] Implement exact Spec fields, robust malformed-object errors and scope-limited checks. No media-semantic/approval attestation from text fields.
- [x] Parent runs full regression suite and actual valid/invalid CLI examples after integration.

### Task 4: Indexed cut extraction

**Files:** new video-production-assets/scripts/split_storyboard.py, test_split_storyboard.py.
**Interface:** `split_storyboard(project: dict, base_dir, output_dir) -> dict`; CLI project path --base-dir ROOT --output NEW_DIR. Pillow dependency explicit; no network/media generation.

- [x] Write regressions checking actual pixels/order, preserved associations, invalid crop/overlap/path/overwrite and whole-input preflight.
- [x] Implement deterministic extraction from registered source sheet crops or clean image paths; output files + derived split-manifest.json. Manifest links canonical IDs and hashes; no project mutation or competing database.
- [x] Parent exercises synthetic sheet extraction, pixel order and repeated-run refusal after integration.

### Task 5: Verification and release documentation

**Files:** qa/storyboard-baseline.json, qa/storyboard-flow-validation.json, storyboarding-video/evals/evals.json, USAGE_GUIDE.md, integrations/skill-routing.md, CHANGELOG.md; package/frontmatter versions through existing tools.

- [x] Run same 5 fresh-context scenarios against updated guidance; review indexed state/review tables across all traces and report text-only limitations. Add consumer-facing eval cases for complete and uploaded/defective boards, silent data, default routing and blocked Blender.
- [x] Run actual structural valid/invalid CLI and synthetic sheet extraction; no claim of rendered artwork or Blender validation.
- [x] Run complete `python -m pytest -q`, existing version checker and managed sync check; sync only package-managed skills by existing non-destructive policy.
- [x] Add usage and changelog instructions matching actual commands/output. Record observed checks and any unavailable runtimes; do not commit/push.

## Acceptance

Every user requirement 2~13 has a named owner and exit condition. Production storyboard cannot be reported complete with missing beat/scene/shot/panel/audio/character links, required unverified spatial inputs, or uninspected images. Image-only narrative quality remains an actual visual review, not a JSON/model-text success claim.

## Observed Completion Evidence

- Package 2.3; version checker confirms 17 consistent skills.
- Full suite: 86 tests / 136 subtests pass. Two existing Windows junction tests emit subprocess decoding warnings; no new Pillow deprecation warnings.
- Actual validator CLI: valid plan and registered images pass; uncovered beat, changed-state hold, missing images, zero/overflowing fps and missing image base return validation errors.
- Actual extraction CLI: five synthetic sheet/JPEG inputs yield ordered PNGs with checked pixels/format/size/hash/ID associations; overwrite, invalid crop and escaping paths are refused before output.
- Local documentation links: 165 checked, zero missing. Managed sync: 51 existing links retained, no replacement/backups; payload refreshed.
- Baseline and application traces plus detailed runtime evidence: `qa/storyboard-flow-validation.json`. Model text is not perfect executable JSON or artistic approval.
- No actual artwork, Blender/voice/video/provider execution, paid generation, publication, commit or push. Blender was unavailable in the initial runtime probe; actual image-only story quality remains a blocking production gate.

