# Continuity Entrypoint Release Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Close standalone continuity-entrypoint gaps and release related sequence/AV implementation to Git and installed agents.
**Architecture:** Keep the existing storyline gate and fail-closed sequence/AV request preparation. Repair entrypoint navigation and the optional-detail wording rather than adding a new global interceptor.
**Tech Stack:** Markdown, Python, pytest, Git, existing sync_installed.py.
**Spec:** ../specs/2026-11-17-continuity-entrypoint-release-design.md

## Global Constraints
- Preserve unrelated routing edits and analysis material; stage explicit owned paths only.
- No new media jobs, uploads, purchases, publications or dependency installs.
- Structural readiness never proves real viewing/listening or model conditioning.
- First shot, first voice, explicit silence and intentional transitions retain scoped exceptions.

## Review Focus
- Standalone video executor skips coordinator: test mandatory predecessor gate pointers.
- Optional detail wording disables basic gate: test separate mandatory/basic and conditional/detail sections.
- Reference listed but not selected natively: run existing transport/request regressions.
- New angle, silence, first voice: run existing handoff positive/negative cases.
- Deployment omits Pi or ships missing helpers: verify tracked dependency files and installed realpaths/hashes.

### Task 1: Entrypoint contracts
Files: scripts/test_storyline_continuity_gate.py; creative-production/SKILL.md; video-production-assets/SKILL.md; higgsfield-generate/SKILL.md; higgsfield-video-replicate/SKILL.md; other video executor entrypoints only if inspection finds the same dependency gap.
Interfaces: existing whole-storyline gate and sequence-execution.md remain canonical.
- [x] Inspect current tests, executor routing and related dirty dependencies; snapshot the initial state.
- [x] Add tests requiring standalone dependent generation to read the gate, inspect accepted predecessor/history references and block missing/unsupported handoff.
- [x] Run the focused tests and record baseline failures.
- [x] Add minimal entrypoint guidance and separate basic mandatory continuity from conditional detail slots.
- [x] Re-run focused regression tests; record behavioral verification limitations honestly.

### Task 2: Adopt and verify related execution implementation
Files: existing sequence/AV scripts, fixtures, tests, sequence reference/example, and related dirty integration changes in creative-production and video-production-assets. No unrelated routing changes.
Interfaces: validate_sequence(...), prepare_request(...), audit_call(...) and existing artifact/version contracts.
- [x] Review sequence/AV implementation dependency closure and diffs, including update_project.py and contract.md.
- [x] Run existing positive/negative sequence and AV tests; fix only demonstrated in-scope failures test-first.
- [x] Run full pytest suite and git diff --check; distinguish pre-existing or unrelated failures.
- [ ] Review exact staged files and diff; commit required implementation and entrypoint changes in coherent units, including this approved spec/plan.

### Task 3: Push and local agent deployment
Files: no application changes expected; existing scripts/sync_installed.py is the deployment interface.
- [ ] Verify current branch, remote URL, upstream and live remote relation before a non-force push; existing local commits are included in a current-branch push and must be reported.
- [ ] Push the requested branch and compare live remote HEAD with local HEAD.
- [ ] Dry-run synchronization for existing Codex/Claude/shared/Pi roots, inspect proposed actions, then apply with backup behavior preserved.
- [ ] Verify installed updated skills resolve to the intended source and required helper paths exist; record tests, commit hashes, push and sync results and excluded dirty paths.

## Execution method
Recommended: native execution in this session plus one independent final reviewer. Worktree isolation is optional pending user consent because the requested release includes selected existing dirty work in the installed source checkout.
