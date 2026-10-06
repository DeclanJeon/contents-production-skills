# Production v5.1 upgrade design

## Scope and authoritative inputs

User-provided `Production_Package_v5.1_Architecture.md` and `Universal_Production_Storyboard_Master_Prompt_v5.1.md` specify an asset-locked, traceable production package. This repository update does not generate a real content production, authorize provider calls, or migrate/deploy user projects automatically.

Additional user requirements: obligatory storyboard scene/panel image splitting; cross-platform user Documents/studio_production project storage; report every saved intermediate/final path; standalone chronological Markdown `.history` skill recording actual prompts, methods, results and interruption/completion, controlled by the existing coordinator.

## Baseline gaps

- `creative-production` required a single combined image, but the source caps sheets at eight panels and requires readability-based pagination.
- Existing `split_storyboard.py` extracted clean panels with safe recorded crops and provenance, but lacked scene-level image outputs and an obligatory post-render workflow.
- Existing full-package checks verified synopsis, character SSOT/sheet, technical board and combined image. They did not express an active LOOK, per-panel exact critical master versions, FINAL/PRELIMINARY asset lock, type-specific master packs or the full v5.1 deliverable gate.
- Existing `update_project.py` already owns canonical guarded updates and dependent stale propagation. Extend it rather than introduce another editable graph/approval database.
- No shared Documents/studio_production resolver or independently installable history owner existed.
- Five fresh-context baseline applications of the old coordinator all omitted the standard storage root, per-scene/panel splitting and chronological Markdown `.history` contract; all correctly avoided inventing the interrupted provider outcome. Preserve that safe reconciliation behavior.

## Ownership and optimization decision

Retain the eight existing core skills: coordinator, video asset craft, text lane, synopsis, character, storyboard, numeric camera and Blender runtime have distinct consumer-facing boundaries. Do not delete a specialist solely because its terminology overlaps the master prompt. Keep nine provider modules conditional; this update does not change provider availability or spend permission.

Add exactly one installable skill, `recording-production-history`, for storage and lifecycle audit mechanics. `creative-production` invokes it, determines scope, owns canonical writes and approvals, and sequences all specialists. History does not select a stage or grant approval. Canonical `project.json` remains the only production-state ledger; CSV package manifests are derived handoff views, not second writable sources of truth.

Common v5.1 doctrine lives in video-production-assets references/templates/validators; specialists refer to it instead of embedding competing gate definitions. Mandatory splitting reuses the existing renderer/splitter. Actual production files stay outside this repository; templates, reusable scripts and instruction docs remain inside.

## Storage and lifecycle

Resolve actual Windows Documents through known-folder APIs (including redirected/OneDrive paths), macOS Documents under home, Linux configured XDG Documents or home/Documents. Default root: Documents/studio_production/project_id. Preserve an explicit active project root and existing artifacts; never silently move or overwrite user files.

Separate v5.1 master assets, scene derivatives, storyboard sheets/extracts, shot cards, generation specs, audio, animatic/edit, QA and delivery. Keep root project.json canonical. Create `.history` only for real saved production, not ordinary chat-only planning.

Record started events before work, followed by observed terminal events. Every event contains time, operation correlation, actual prompt, method/tool/model or honestly unavailable metadata, output paths and status. Interrupted client execution is distinct from a failed provider job. Resume records interrupted local work, reconciles pending provider requests and never invents completion. Project completion is distinct from completing one operation.

## Asset-first gates and handoff

Lock source adaptation and IDs, active LOOK/style-world bible, relevant master character/location/prop/product/environment assets and scene states before FINAL storyboard generation. Critical missing/draft/stale references allow only PRELIMINARY work. Capture exact IDs, versions and package-relative paths; preserve UNKNOWN/NOT_EXPOSED rather than fabricate provenance. Masters are stored once; derivatives identify their master/version.

Use readable sheets of at most eight panels; retain all story coverage across sheets. Extract actual sheet pixels from recorded clean bounds into panel images organized by scene plus scene overview images. Inspect the real outputs and report saved paths. Export applicable shot/generation/capture/audio/animatic/continuity/QA/delivery handoffs and a versioned ZIP with registered real files; empty directories are not completion.

On master changes invalidate only transitively dependent state/sheets/specs/animatic and approvals. Unrelated artifacts remain current. Structural/file gates never claim artistic continuity, rights clearance or user acceptance.

## Verification evidence and limits

- Whole repository: `python -m pytest -q` → **205 tests +193 subtests passed**. Two existing Windows decoding warnings remain in `scripts/test_sync_installed.py`; they are not new production/history failures.
- Final asset/package boundary checks: **25 tests +9 subtests passed**, overlapping the whole suite. Version checker: package **2.4**, **18** manifest skills consistent.
- Actual Windows Documents resolver created `C:\Users\Declan\Documents\03_studio_production\production-v51-mechanics-20261006-203426`. History CLI exercised start → interruption → resume → second attempt → operation completion → project completion; no in-flight operations remain.
- Actual renderer/splitter CLIs produced ten panels over two scenes, paginated as **4/4/2** panels. All ten clean preliminary extracts matched source pixels. The actual scene overview PNG was opened. Unlocked LOOK refused FINAL rendering without a written output; a preliminary board refused FINAL packaging.
- Actual FINAL structural-fixture ZIP contained **47 registered assets** with matching hashes. Its extracted portable `project.json` passed preproduction validation. FINAL packaging additionally requires registered, current sheet-derived scene/panel outputs; the canonical sheet pointer is an ordered array even for one sheet.
- Actual guarded update CLI marked a changed master's derivative and the **BOARD → SHEET → GEN → ANIMATIC** chain stale, including the returned stale-ID list. Unrelated AUDIO approval remained current.
- Direct installer preflight refused existing source `video-production-assets/support` cache collisions with zero writes. A clean staged copy installed all **18** skills and required helper scripts into an isolated temporary destination. Existing cache/global installations were not changed.
- Five baseline and five updated fresh-context coordinator applications were exercised. A further fresh-context probe against the final universal guide confirmed ordered sheet/split pointers, preserved original panel sources, no FINAL claim without master locks, and no invented saved files or interrupted remote outcome. This is instruction-only evidence, not provider execution.
- Persistent smoke evidence: project `09_QA/mechanical-verification.md`; actual sheets/extracts under `04_STORYBOARDS`; ZIP under `10_DELIVERY`; chronological records under `.history/events`. The ZIP captures history as of packaging; the operation/project completion events are subsequently recorded in the source project.
- Synthetic fixtures prove mechanics, not artwork quality, rights or creative/user approval. macOS/Linux Documents rules are contract-tested but were not run on those native OSes. No actual provider, video, Blender or global install/commit/push was performed for this update.

## Post-implementation QA and corrective work order

Subsequent read-only overall QA identified **23 unique findings: 11 HIGH and 12 MEDIUM** across FINAL readiness, extraction provenance, file confinement, ZIP integrity, lifecycle correlation and focused handoffs. That historical QA returned **REQUEST_CHANGES / BLOCK**; the implementation and final verification below resolve those findings. Deployment remains separately unauthorized. The baseline verification records above do not certify artistic quality, rights or human approval.

The [QA corrective work order](superpowers/plans/2026-10-06-production-v5-1-qa-remediation.md) maps Q01–Q23 to seven implementation tasks, affected files, regression scenarios and completion criteria. It also explains project-path boundaries and credential masking without assuming development terminology.

The authorized Q01–Q23 implementation passed its native acceptance corpus. Independent follow-up resolved readiness freshness/alias and pixel/geometry checks, repeated scene-band assembly, case-insensitive reserved-path collisions, escaped credential masking, chronological attempt output checks, selected-owner invalidation and transitive focused handoffs. ReviewGatePublication and ReviewHistoryHandoff both returned final **APPROVE**. The default-locale full-suite run failed on 27 unrelated Windows cp949 decode errors and 3 now-corrected checker assertions; the final `python -X utf8 -m pytest -q` run passed **258 tests +217 subtests**, with version check and clean isolated staging/runtime/package smoke also passing. Independent installed-package follow-up exercised image-backed FINAL18 success/alpha-pixel refusal, output-deletion completion refusal, history attempt correlation and secret-safe prompt recording; exact cases are linked in the [implementation record](evidence/production-v51-qa-remediation.md). Exact final outputs are in [the final verification record](evidence/production-v51-final-verification.json). The original QA reports remain historical and unmodified. Implementation QA and code reviews are complete; deployment remains **BLOCK** until separately authorized.
