# Preproduction Review Gate Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make topic-to-video requests produce a directory-scoped, image-backed preproduction review package and stop before separately approved video execution.

**Architecture:** Extend the existing coordinator and production-assets skill. Keep one canonical `project.json`; put the detailed branch contract in a disclosed production-assets reference. Reuse artifact versions, dependencies and approval records rather than introducing a new runtime or approval engine.

**Tech Stack:** Markdown skills and references, existing Python validators, Node-based external `codex-imagen` skill, Git/GitHub CLI. No new package dependencies.

**Spec:** `docs/superpowers/specs/2026-10-02-preproduction-review-gate-design.md`

## Global Constraints

- All project artifacts stay under one user-selected project directory with registry paths relative to that directory.
- Ask for the exact project directory before creating files or submitting media requests; reuse an exact directory already supplied for the current project.
- Topic-only requests use applicable modules; source site, judgment model, genre, runtime and aspect ratio remain project-specific.
- Images are delegated to `codex-imagen` after reading its instructions and checking actual availability/auth and applicable usage/spend approval.
- A production-assets package is not footage. No representative video shot, animation render or edited video export before explicit video authorization.
- Preproduction acceptance is version-bound and is not video execution or spending permission. Changed dependencies require affected approvals to be reviewed again.
- Publishing remains separately requested. Public repository changes exclude actual project data, credential values and personal save paths.
- Preserve narrow single-artifact, UI and 3D paths outside the topic-to-video branch.
- This session's first-project execution remains paused until its separately requested judgment tool is ready. That prerequisite does not block these skill updates.

## Review Focus

- A selected parent root is not an exact project directory: propose a non-colliding child and obtain the user's choice before writing.
- Existing content must not be overwritten by a fresh topic request; explicit resume uses the existing registry.
- The coordinator's existing representative-shot instruction must not bypass the preproduction stop.
- A generated/verified image or positive automated judgment must not manufacture user acceptance or video authorization.
- A modified reviewed asset must not carry its previous approval into the changed version; missing image auth must not silently switch providers.

---

### Task 1: Establish the folder-scoped preproduction contract

**Files:**
- Create: `video-production-assets/references/preproduction-review.md`
- Modify: `video-production-assets/SKILL.md` — execution principles, full-package sequence, handoff, completion and image-executor boundary.
- Modify: `video-production-assets/references/contract.md` — version-bound review/authorization mapping using existing fields.

**Interfaces:**
- Consumes: existing artifact IDs, states, `approval={by, at, evidence}`, dependencies and `dependency_versions`; current `codex-imagen` instructions.
- Produces: the authoritative reference at `video-production-assets/references/preproduction-review.md`, used by both the asset skill and local coordinator; no schema or exported-code changes.

- [x] Write the reference's ordered procedure and completion criteria: exact folder selection/collision/resume, topic-specific brief, applicable assets, explicit image outputs, actual inspections, review report, version-bound acceptance, deferred video model and separate bounded execution approval.
- [x] Update the skill's full-package branch to reach that reference before files or media requests. Keep single requested text artifacts narrow. Apply story/performance/character modules only when relevant.
- [x] Explain the `review.md` artifact and optional later video execution plan using existing approval/dependency fields. Leave unknown video model/price unresolved in valid preproduction packages; distinguish generated/verified from accepted.
- [x] Record each Review Focus input in a temporary decision table with expected next action and forbidden side effects. This is a dry-run interpretation check, not proof of generated images or executed videos.

### Task 2: Wire coordinator, installation and public guidance

**Files:**
- Modify local: user skill root `creative-production/SKILL.md` — video request routing and representative slice precedence.
- Modify local: user skill root `creative-production/references/production-routing.md` — image-backed package and approval handoff.
- Synchronize local: user skill root `video-production-assets/SKILL.md`, `references/contract.md`, and new `references/preproduction-review.md` from the repository.
- Modify public: `README.md`, `integrations/skill-routing.md`.

**Interfaces:**
- Consumes: Task 1's reference and existing `project.json` contract.
- Produces: one discoverable topic-to-preproduction branch; one shared contract; consistent public/install guidance.

- [x] Link the local coordinator to the installed production-assets reference. Define topic-to-video entry as preproduction-first; prompt/edit-only requests retain their existing narrow owners.
- [x] Make the preproduction branch explicitly override representative video-shot generation. A representative still/storyboard image is appropriate before video approval; unrelated UI/3D workflows retain their original representative slices.
- [x] Update public guidance to explain exact directory selection, external `codex-imagen` dependency, review package and distinct video approval. Do not bundle external skill bodies or first-project details.
- [x] Apply the same production-assets text to the installed copies. Compare SHA-256 for the three synchronized files; all pairs must match.

### Task 3: Verify and publish the skill change

**Files:** Only Task 1–2 files and the approved spec/plan are in scope for the release. No first-project assets are created in this task.

- [x] Run the existing suite once after the edits:
  - `python -B video-production-assets/scripts/test_validate_project.py` from repository root: 8 tests pass.
  - `python -B camera-spatial-design/scripts/test_spatial_spec.py` from repository root: 6 tests pass.
  - `python -B video-production-assets/scripts/validate_project.py examples/20-second-animation/project.json --profile plan`: valid example, exit 0.
- [x] Smoke the actual installed image helper with `node <installed-codex-imagen>/scripts/codex-imagen.mjs --smoke`; report actual readiness or a concrete blocker without exposing auth values. No image generation is authorized by this command.
- [x] Run a disposable dry-run workflow exercise over: topic only/no path; exact supplied path; parent root only; colliding folder; explicit resume; single text artifact; unavailable image auth; model not selected; preproduction accepted but no video authorization; positive model judgment without user acceptance; and a changed accepted dependency. Observe planned next actions against the decision table. Do not substitute these checks for actual end-to-end media execution.
- [x] Exercise existing validator behavior using a disposable in-memory copy of `examples/20-second-animation/project.json`: an approved artifact without approval evidence must fail; a stale artifact carrying an old dependency version must fail. Use existing schema, not new permanent tests for instructions or wording.
- [x] Obtain a read-only final review of the changed skills and docs. Address concrete Important/Critical defects before publishing. Remove any disposable smoke artifacts.
- [ ] Verify public changes contain no personal project path or source/judgment-specific project defaults. Commit and push the scoped skill/docs files; read back the public commit and changed skill/reference files.
- [ ] Report exactly what was updated and verified. First-project assets, image QA and video generation remain unexecuted while that project's prerequisite is unresolved; do not claim the first package exists.

### Observed verification

- Before the change, all five fresh-context baseline samples proposed a representative video before review and did not require a selected output directory. After the change, all five required a folder before writes and limited generation to review stills.
- Eleven additional dry-run scenarios preserved the folder, narrow-request, missing-auth, model-deferral, review and changed-dependency boundaries. One further scenario correctly rejected an unlisted representative shot outside an approved execution plan. These are model-interpreted workflow smoke checks, not real end-to-end media runs.
- Production validator suite: 8 passed. Camera suite: 6 passed. Existing animation plan: valid. In-memory probes rejected missing approval evidence and dependency-version mismatch.
- Installed production skill, contract, and review reference: all three SHA-256 pairs matched the source. Actual image helper smoke found a local auth profile; no image-generation request was made.
- Independent fresh-context review identified a representative-shot scope ambiguity. The coordinator now requires that shot to be included in the approved execution plan and caps; targeted review confirmed the fix. No other Important/Critical issue was reported.


## Execution Handoff

Preserve the previously selected Native execution style: implement these tasks inline, with one final independent reviewer. Obtain user review of this plan before editing the skills. After the skill update, resolve the first project's judgment-tool prerequisite separately; do not encode that prerequisite as a global skill rule.
