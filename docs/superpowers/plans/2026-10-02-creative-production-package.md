# Creative Production Package Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use subagent-driven-development or executing-plans to implement this plan task-by-task. Native task tools are the execution surface; do not introduce an additional runtime.

**Goal:** Ship the approved eight-skill content/video planning package, with explicit optional execution dependencies and safe manifest-driven installation.

**Architecture:** Preserve sibling skill directories and existing production/spatial contracts. `creative-production` is the project coordinator; the four text-planning skills form one internal lane. A small Python installer consumes the one package manifest, preflights sources and collisions, and supports explicit backed-up replacement/migration.

**Tech Stack:** Markdown/YAML skills, JSON manifest, Python 3 standard library installer/unittest, PowerShell invocation on Windows.

**Spec:** [Approved package design](../specs/2026-10-02-creative-production-package-design.md).

## Global Constraints

- Core IDs: creative-production, video-production-assets, camera-spatial-design, blender-previsualization, orchestrating-video-preproduction, developing-video-synopses, designing-video-character-sheets, storyboarding-video.
- Keep root-level skill directories, production schema 1.1, camera-spatial-1.0 and video-production-assets/support installation convention.
- Text-only work has no required provider, image, folder, GPU, Blender or OMX framework. Optional execution dependencies become required only in their selected branch.
- Preserve separate version-bound preproduction, execution/spend and publication gates; no paid media or publication smoke without authorization.
- No new package reuse license. Exclude newly imported book summaries, external Notion adaptation and private references; write independent operational guidance from this approved brief instead. Do not imply legal clearance of historical bibliography or package contents.
- Never merge/overwrite existing installed skill folders silently. Replacement/migration requires explicit flags and a backup location. Preserve unrelated skills.
- Initial validated installation surface: Windows + Codex user skill root; arbitrary root accepted without claiming every agent/platform was tested.

## Review Focus

- A late source/support omission must fail before any installation write: Task 3 preflight test.
- An existing skill near the end of the list must prevent all copies: Task 3 collision test.
- Installation into a package source/backup root or an unsafe manifest ID must not mutate sources: Task 3 boundary test.
- Duplicate IDs in the explicitly supplied alias root must either block or be backed up and migrated: Task 3 migration test.
- A missing framework must not stop a locked text request; approving stills must not generate video: Task 4 actual fresh-model artifact/action probes.

---

## Task 1: Portable coordinator and provenance

**Files:**
- Create: creative-production/SKILL.md, creative-production/references/production-routing.md, creative-production/references/shot-manifest.md, creative-production/references/creative-qa.md, creative-production/agents/openai.yaml.
- Create: integrations/package-provenance.md.
- Modify: README.md, integrations/skill-routing.md, approved spec status.

**Interfaces:** Consume existing production/spatial/review contracts; expose one coordinator entry point and scoped specialist handoffs. Relative references must resolve from an installed skill directory, not the repo working directory.

- [x] Inspect current coordinator and owned references; retain useful contracts, replace framework-only requirements with host dialogue/tools, and treat external skills as branch-scoped dependencies.
- [x] Write the coordinator and its needed reference files; do not copy third-party media, credentials or external tool helper code.
- [x] Record exclusions and source/rights limits honestly, including no package license grant and no third-party book/Notion text in the new planning lane.
- [x] Update README/routing to describe actual eight-skill package and entry point once Tasks 2/3 are integrated.

## Task 2: Closed text-planning lane

**Files:**
- Create: orchestrating-video-preproduction/SKILL.md and references/video-direction.md.
- Create: developing-video-synopses/SKILL.md, designing-video-character-sheets/SKILL.md, storyboarding-video/SKILL.md.
- Create: agents/openai.yaml and evals/evals.json for the four new planning skills where useful.

**Interfaces:** Core siblings in one skill root; share operational video-direction.md and one brief/continuity context. Independent artifacts need no project.json. Expose actual concept/synopsis, character sheet or storyboard text, not a completion report.

- [x] Inspect installed specialist contracts and inheritance/checkpoint behavior. Do not import book-synthesis.md or the Notion-adapted reference.
- [x] Author independent concise workflows from the approved brief and existing in-repo contract, retaining mode-specific factual/narrative/abstract handling and narrow requests.
- [x] Ensure checkpoints reuse supplied direction/explicit delegated creative choices; text prompts never claim media generation or authorize external spend.
- [x] Define synthetic eval prompts with consumer-visible expected boundaries; no source-wording tests.

## Task 3: Manifest-driven safe installation

**Files:**
- Modify: manifest.json (package 1.3, entry_skill and eight skills; existing fields retained; conditional external dependency records).
- Create: scripts/install_package.py, scripts/test_install_package.py, .gitignore.

**Interfaces:** CLI `python scripts/install_package.py [--skills-root PATH] [--replace --backup-dir PATH] [--alias-root PATH]`. Default CODEX_HOME/skills else user-home/.codex/skills. Source root is the script's repo parent. Alias root is an explicitly supplied second scan location, never inferred/mutated secretly. Exit 0 means installation complete; nonzero explains preflight or I/O failure. External dependencies are never auto-installed.

- [x] Write focused unittest scenarios through the public installer interface: fresh install/full resource preservation, late collision/no partial writes, source/support omission/no partial writes, explicit replacement preserves old bytes in backup, alias migration preserves old bytes and unrelated skills, manifest path traversal/duplicate IDs rejected, source-target/backup overlap rejected.
- [x] Before production code, execute one isolated missing-installer scenario and record the observed failure. Other tests are run centrally after integration; workers skip mid-flight suites.
- [x] Implement stdlib CLI and complete preflight before filesystem writes. Exclude __pycache__ and .pyc from copied resources. Use full-folder backup rather than merge on explicit replacement; on failure report actual applied paths and retained backups.
- [x] Set manifest single source of installation IDs and preserve support manifest/examples/qa.
- [x] Add narrow ignore rules for Python caches; do not delete unrelated existing files.

## Task 4: Integrated verification, docs and release

**Files:**
- Create: qa/package-validation.json, CHANGELOG.md.
- Modify: README.md installation/check instructions and design/plan completion evidence.

**Interfaces:** New installer + core directory resources + unchanged validators. Install into a fresh temporary root, then apply the same skills in fresh model contexts. Test output is evidence, not an authorization record.

- [x] Run `python scripts/test_install_package.py`, `python video-production-assets/scripts/test_validate_project.py`, `python camera-spatial-design/scripts/test_spatial_spec.py` after integration and after correcting observed/reviewed defects.
- [x] Execute the actual installer into an empty root; run its duplicate/collision path and observe nonzero exit with original bytes unchanged.
- [x] Validate every Markdown local resource link and YAML ID/description; exercise educational project validator and camera example analysis.
- [x] Apply only installed core instructions to independent content draft, factual 15-second/3-panel plan, standalone character artifact, inherited checkpoint, missing image prerequisites, preproduction acceptance, stale input, chosen provider/partial success, rewrite-only and UI exclusion scenarios. Report actual outputs; no tool-enabled execution or paid-provider verification inferred from model probes.
- [x] Record QA/provenance/changelog; describe real package behavior without claiming external runtimes or provider calls tested.
- [x] Back up and explicitly replace core Codex folders; migrate matching .agents planning IDs using the explicit alias-root contract. Verify no duplicate managed IDs and existing unrelated skills remain.
- [ ] Stage only scoped package files, commit `feat: package creative-production and portable planning skills`, push the implementation branch and verify its remote SHA. Integrate main only by the approved normal fast-forward workflow if main still points to the original base; do not force-push or include unrelated changes.

## Execution decisions

- User's request to continue after design is treated as approval to implement the described package and its normal commit/push handoff; no media generation or platform publication is implied.
- Work on a dedicated local implementation branch in the current checkout, carrying only the prior design/README changes. Do not introduce a worktree or disturb the current installed environment mid-flight.
- Two independent worker ownership slices: Task 2 planning folders; Task 3 installer/manifest/ignore files. Parent owns Task 1 and Task 4, final verification and Git operations. Workers skip build/lint/tests/formatters and do not commit.
- Public source hygiene uses independent replacement guidance for new book/Notion-dependent planning resources; it does not assert a new legal license or copyright clearance.

## Exercised completion evidence

- Initial package lacked five core directories and installer CLI returned exit 2 (missing file). This was the package-closure baseline, not a failed text-drafting claim; the old coordinator's direct-draft control already behaved correctly.
- Final integrated suites: installer 21, production contract 8, spatial 6, all pass. Observed pre-fix safety failures have retained regressions, including malformed/empty manifest, wrong root/support type, linked roots, partial-copy reporting and source-support collisions.
- Actual CLI fresh install, collision byte preservation, full-folder backed-up upgrade and alias migration pass. Core-only fresh-context probes produced 13 actual artifacts/checkpoint responses; probabilistic low-confidence judgments were resolved by reasoned artifact review.
- Two independent static reviews reported and re-reviewed two defects: source-support collision and non-narrative requested-stage omission. Scoped re-reviews have no findings.
- Actual local synchronization backed up four existing Codex core folders and four planning aliases; installed all eight into one Codex root; removed the four backed-up duplicate aliases. All 364 unrelated skill entrypoints remained unchanged. Full prior managed-folder snapshots match their backups.
- Detailed public-safe observations and unexercised provider/media/legal surfaces: [QA record](../../../qa/package-validation.json).
