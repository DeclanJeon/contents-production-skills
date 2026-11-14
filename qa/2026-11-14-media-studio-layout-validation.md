# Media Studio layout — verification (2026-11-14)

## Release preparation — scoped staged snapshot

After the operator requested commit/push and installed-skill update, Media Studio changes were staged separately from unrelated stickman/creator/research work. An index-only snapshot exported with `git checkout-index` passed **736 tests, 4 Windows-only skips, 524 subtests** (60.84 s), plus the package 2.34 / 22-skill version check. This clean-snapshot count differs from the larger dirty-worktree suite below because unrelated uncommitted tests were deliberately excluded. Neither result is a macOS/Windows execution claim.

## Latest — independent review and fix pass

One fresh-context reviewer completed a read-only inspection. Its original **BLOCK** report is retained in [independent review](2026-11-14-media-studio-layout-independent-review.md); it was not overwritten with an author-generated approval. The reviewer ran no commands and did not independently inspect historical commit ranges. The implementer reproduced and fixed all six actionable findings in one fix pass; no second reviewer was dispatched.

Latest observed Linux verification:
- Full suite: **806 passed, 4 skipped, 524 subtests passed** (50.69 s).
- Storage/audit suite: **83 passed, 4 skipped, 11 subtests passed**.
- The four skips are Windows-only junction subcases, not hidden failures.
- Version check: package **2.34**, **22 skills consistent**.
- All code findings below have observed failing regression tests followed by passing tests.

| Finding | Fix and regression evidence |
|---|---|
| P1: linked slug escapes selected studio | Shared `project_root_in_studio` validates the unresolved child before canonicalizing it. Explicit/default/environment/config routes reject real external symlinks without writes. Windows junction cases are added but not executed here. |
| P1: tests inherit real saved-root settings | Module-scoped temporary home/config/Documents environment clears ambient studio overrides. A subprocess runs an existing storage test under hostile saved/environment choices and proves the external production directory stays empty. |
| P2: repeat init rejects an unused linked work folder | Preset paths are checked only for new-project creation. Existing ledger/audit boundaries remain checked; a linked internal work folder survives repeat full init unchanged. |
| P2: ensure-dir creates orphan roots | CLI now calls the existing initialized-project guard before creating a work folder. A typo path is rejected with JSON/exit 2 and remains nonexistent. |
| P2: undecodable config/ledger tracebacks | Non-UTF-8 config falls back to default; non-UTF-8 ledger becomes a structured preflight error without writes. |
| P2: delivery PDF examples target work folders | Delivered PDFs now use `final/`; intermediate PNG sheets and extraction remain under `storyboards/`. Documentation-only correction, not an independently observed agent action. |

The first full fix-pass run exposed a test-harness cleanup mismatch: pytest does not drain unittest's module cleanup stack automatically. A new subprocess regression observed the leaked environment, then explicit module teardown restored it. The final complete suite is green after that correction.

### Current limits and rulings

- Actual macOS/Windows execution remains unobserved. Six CI jobs are configured, not submitted; native redirected Documents, junction behavior and case-insensitive filesystem behavior must still be confirmed there.
- Real agent-behavior pressure tests remain unperformed. The reviewer statically checked fresh/default/custom/environment/resume/chat-only routing and found it substantially clear; this is not behavioral acceptance.
- No automatic legacy migration, project.json schema change or delivery ZIP projection change. Existing projects are reused only by their selected root; no project-tree cleanup or data movement was performed.
- Existing atomic-hardlink publication remains a filesystem requirement; this is not a claim of compatibility with every network/removable filesystem.
- Historical committed-range review was not possible for the reviewer. Its findings are based on current files; the author does not represent this as a separate history audit.
- No extra review fanout, new dependency installation, additional Git commits, push, merge or publication in the resumed/fix sessions. Shared dirty user edits remain in place.
- Release metadata was generated in an isolated fixture to preserve unrelated Unreleased notes.
- Parent disposition: all six actionable review findings addressed with regression evidence; cross-platform runtime and agent-behavior acceptance remain pending. The independent review itself was not rerun.

The sections below retain the earlier pre-review evidence for chronology.

## Scope and current state

Package working-tree version: **2.34**, 22 bundled skill versions bumped with the existing bump tool in an isolated temporary release fixture. Only the Media Studio release note was inserted; pre-existing Unreleased notes and unrelated dirty source files were preserved. No publishing, migration, merge, push, new dependency installation or additional Git commit was performed in the resumed session.

Default: actual Documents/Media_Studio/<slug>. Explicit project roots are used directly. Studio override: call-level --media-studio-root, MEDIA_STUDIO_ROOT, saved set-root config, then Documents fallback. Default text init creates source/, project.json and .history/{events,prompts}; other work folders are on demand. final/ holds deliverables. Existing ledgers and legacy project folders remain unchanged.

The coordinator asks once for a preferred directory before the first save, unless an active explicit path, environment/config choice or existing default studio root resolves it. The CLI is intentionally non-interactive.

## Observed Linux verification

- `python3 -m pytest recording-production-history/scripts -q`: **76 passed, 5 subtests passed**.
- Final `python3 -m pytest -q`: **786 passed, 518 subtests passed** (58.67 s).
- `python3 scripts/check_versions.py`: **package 2.34, 22 skill(s) consistent**.
- `git -c core.whitespace=cr-at-eol diff --check`: passed. Existing CRLF skill files retain their line endings.
- Real subprocess CLI smoke in a temporary directory: Unicode project slug, minimal init, repeat init with full preset preserving exact ledger bytes, lazy final directory, read-only list, set-root and subsequent cached-root init all passed. It did not touch the actual Documents tree or actual saved root configuration.
- Four boundary tests were observed failing first, then passing: relative MEDIA_STUDIO_ROOT rejection; ignore relative cached studio root; reject non-object project JSON without writes; reject unsafe audit symlink before creating work directories.
- Existing project.json schema and package_production.py delivery ZIP projection are unchanged.

## Cross-platform verification boundary

.github/workflows/ci.yml now includes Ubuntu/macOS/Windows × Python 3.10/3.12 storage/audit tests. macOS canonical-path comparisons account for /var and /private/var. Windows known-folder/registry discovery and platform locks remain in use.

**Only Linux was executed here.** The six CI jobs have not been submitted or observed. This report does not claim macOS/Windows runtime success, nor support for filesystems that lack the existing atomic-hardlink publication requirement.

## Gates at the pre-review checkpoint (superseded above)

Independent review was initially awaiting operator authorization. Authorization was later given and one reviewer completed the inspection described above. Agent-behavior pressure tests and actual macOS/Windows runtime results remain unobserved. No additional commits/publication were performed.
