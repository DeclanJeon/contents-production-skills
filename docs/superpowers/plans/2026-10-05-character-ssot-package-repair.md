# Character SSOT and Image-Backed Preproduction Repair

> **For agentic workers:** REQUIRED SUB-SKILL: Use subagent-driven-development or executing-plans for the assigned slices; the coordinator owns integration and runs verification once after all edits.

**Goal:** Make a full image-backed production return synopsis MD, per-character persona/SSOT MD and one identity image sheet, an indexed technical storyboard, and one actual combined storyboard image before review or video execution.

**Architecture:** Extend the existing project.json, artifact dependency graph and validators; do not introduce another manifest or approval database. Keep standalone text-only work narrow. The supplied Character SSOT Master Prompt becomes a detailed character reference; explicit fictional design delegation permits labeled creative choices, while real-person facts remain sourced or unknown.

**Tech Stack:** Python, existing unittest/pytest conventions, Pillow for deterministic PNG assembly, Markdown skills and junction-based installation.

**Spec:** User-approved repair scope in the current conversation and the supplied Character SSOT Master Prompt; canonical field definitions below.

## Global Constraints

- No production media generation, provider submissions, new spend or fabricated artwork/approvals in this repair.
- Preserve the existing dirty worktree and source assets. Commit only changes attributable to this repair; if isolation is unsafe, report and leave the changes uncommitted rather than include unrelated work.
- Preserve schema_version=1.1. Minimal standalone plans need no package declaration. Full package completeness is a distinct preproduction validation profile and is mandatory for any reviewed/approved preproduction_review or approved video_execution_plan.
- Canonical `preproduction`: `{mode: text|image_backed, synopsis_artifact_id, storyboard_artifact_id, storyboard_sheet_artifact_id?}`. Text mode has no actual-image requirement; a full image-backed review or video execution cannot use text mode to bypass image requirements.
- Every requested `characters[]` entry in a full package: `persona={role,personality,observable_behavior,speech}` (nonempty strings; silent/not-applicable explained), `ssot_artifact_id` (type character_sheet), `identity_sheet_asset_id` (image-backed only, kind character_identity_sheet, matching entity_type=character/entity_id).
- The synopsis is a type synopsis artifact linked to an actual Markdown asset. Character SSOT artifacts depend on that synopsis/version and carry their Markdown asset; the storyboard artifact depends on the synopsis and all character SSOT artifacts. Every shot naming a character consumes that character's identity image asset in image-backed mode.
- Combined sheet artifact type storyboard_sheet depends on the current storyboard; exactly one kind storyboard_sheet image asset records the entire ordered `panel_ids` and corresponding `source_asset_ids`. A sheet containing a subset, stale sources, incorrect ordering or wrong provenance is incomplete.
- Actual-image completeness needs --base-dir, real decodable images, hashes, current dependency versions and no unresolved blocker. Structural/identity/artistic review and user acceptance are separate; code never certifies a face or creative quality from declarations.

## Review Focus

- A plan validator returning valid must not allow reviewed/approved incomplete packages or video execution approval.
- Text-only/standalone/characterless scope must not invent images, characters or spend.
- Persona, actual SSOT image and combined sheet pointers must resolve to the right artifact/asset roles and versions, not merely existing IDs.
- Combined sheets must include every canonical panel once, in story order, with the same source mapping, metadata and unmodified clean panel images.
- Rejection of existing creative treatment must invalidate related review/execution/delivery readiness without deleting actual sources or treating the rejected preview as approved.

## Tasks

### 1. Character design and SSOT handoff

**Files:** designing-video-character-sheets/SKILL.md; references/character-craft.md; new references/character-ssot-master-prompt.md; video-production-assets/assets/character-ssot-template.md; references/20-visual-mode-ssot.md.

- [ ] Preserve the user prompt's 0–33 output sections, visual/face/hair/body locks, anchors/priority, persona/behavior, turnaround, ratios, anti-drift, prompt lengths, A/B/C/D prompt specs, audit, nonhuman adaptation and multi-cast contrast.
- [ ] Fix unconditional no-invention rules: delegated fictional design is a labeled proposal; real-person unknowns are not invented. Irrelevant exact numbers remain unspecified.
- [ ] Make one per-character Identity Sheet A the mandatory actual SSOT image of the full image-backed package. B/C/D are specifications, not automatic extra image submissions. Standalone text outputs remain text.

### 2. Complete board and deterministic sheet

**Files:** storyboard-contract.md; storyboarding-video/SKILL.md and its current-stage guide; new scripts/render_storyboard_sheet.py and test_render_storyboard_sheet.py.

**Interface:** `render_sheet(project, base_dir, output, *, font_path=None) -> dict` returns actual file/hash and ordered panel/source references; no project.json mutation. CLI `project --base-dir ROOT --output RELATIVE.png [--font FONT.ttf]`. One PNG includes all panels with readable external shot/scene/beat/character/SSOT/camera/time/source captions. Reject overwrite, outside-root paths, absent/invalid inputs and label/font limitations rather than silently omit captions. Parent integrates returned provenance into existing asset/artifact tables.

- [ ] Retain the six-section board contract and clean panel boundaries; require the actual assembled sheet for image-backed full packages or explicit image-sheet requests.
- [ ] Add consumer-visible boundary/order/provenance/overwrite tests without source-text assertions.

### 3. Package validator and coordinator cutover

**Files:** validate_project.py; validate_storyboard.py (internal shared-validation option to avoid recursion); new validate_preproduction.py and test_validate_preproduction.py; affected approval/handoff fixtures; contract.md; preproduction-review.md; creative-production routing and SKILL.md; orchestrating-video-preproduction handoff references; usage/changelog.

**Interface:** `validate_preproduction(project, base_dir=None, *, image_backed_required=False) -> list[str]`, used by new `--profile preproduction` and automatically for reviewed/approved package review or approved execution. `validate_storyboard(..., check_project=True)` permits the package validator to reuse board checks without recursive plan validation. Do not duplicate complete-board semantics.

- [ ] Run one regression against the existing ready-review omission before implementing; preserve the observed failing result.
- [ ] Validate every required artifact, persona, image, dependency/version, source mapping and coverage. Use current files; do not infer acceptance from hashes or metadata.
- [ ] Cut the full image-backed coordinator path over to explicit synopsis → character SSOT → reference image → integrated board → combined sheet → complete-package/visual checks → review. No callbacks to a rival coordinator.
- [ ] Keep draft/stale incomplete ledgers recordable; readiness/approval and the strict preproduction profile reject incomplete deliverables.

### 4. Reconcile the rejected production

**Files:** productions/132-autumn-25s/project.json and only affected brief/visual/storyboard/review/execution/edit/QA/delivery documents.

- [ ] Remove the misleading 'character sheet not requested' decision, record the actual missing persona/SSOT/sheet as blockers, mark affected dependent approvals stale, and preserve the rejected composite and good sources as history.
- [ ] Do not write fake persona completion, generated SSOT files, replacement imagery or accepted final video. Report that new generation and creative reapproval remain blocked/outside this repair.

### 5. Verify and deploy

- [ ] Run the full existing pytest suite after integration; report all failures/warnings rather than hide them.
- [ ] Run actual valid and invalid package CLI scenarios and deterministic PNG assembly; open the resulting sheet and exercise confinement/overwrite failure paths.
- [ ] Compare five fresh-context baseline/updated instruction applications plus scope controls. Retain exact responses and reviewed limitations; this is not rendered-character quality evidence.
- [ ] Independently review code/contracts, fix actionable findings, update changelog/docs and check package versions. Verify junction installation/provenance without overwriting unrelated skills.
- [ ] Commit only attributable changes if safe; report installation, exercised proof, remaining production blockers and any uncommitted user-worktree constraint.
