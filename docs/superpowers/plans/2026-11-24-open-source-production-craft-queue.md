# Open-source production craft — implementation queue

> **For agentic workers:** Use `superpowers:executing-plans` for inline execution and record the evidence before checking off each item.

**Goal:** Apply the five production-craft gaps identified in the preceding repository audit, keeping existing routing and approvals.
**Design:** Extend the existing on-demand references. No new skill, development dependency, executable adapter, production artifact, or project record. Link to upstream primary sources rather than vendoring their files. Fallbacks never auto-install or silently substitute for a required engine. Fountain stays a separate optional follow-up.
**Verification:** Add failing document-contract tests first; run the matching case before closing each item. Final gate: whole-suite regression, version consistency, diff/links, and fresh-context review. The 100% gate covers this documentation queue, not a production render or real Korean-media validation. Preserve pre-existing changes; no commit, install, or release in this queue.

## Queue

- [x] Q1 — Conditional local subtitle timing in `creative-production/references/narration-subtitle-handoff.md`: approved local speech source; raw ASR separate from display text; aligned word timing only if needed and supported; timing/review gate. Test `test_local_caption_timing`.
- [x] Q2 — Talking-head cleanup in `video-production-assets/references/09a-short-form-edit-recipes.md`: distinguish flubs from intent, keep source/output cut times, rerun transcript and listen. Test `test_talking_head_cleanup`.
- [x] Q3 — Editable timeline delivery in `video-production-assets/references/15-delivery.md`: explicit destination, adapter limitations, reopen and verify media, cuts and audio; no verification claim without target app. Test `test_editable_timeline_delivery`.
- [x] Q4 — Hand-drawn 2D handoff in `video-production-assets/references/08-animation.md`: exposure, layers, and frame-sequence handoff with playback/import check. Test `test_hand_drawn_handoff`.
- [x] Q5 — Cut-only option in `video-production-assets/references/31-external-video-decomposition.md`: installed-only PySceneDetect, detector result stays candidate, no silent downgrade from full decomposition; manual fallback. Test `test_cut_only_candidate`.
- [x] Q6 — Regression and final review: `python3 -m pytest -q`, `python3 scripts/check_versions.py`, `git diff --check`, fresh-context review. Confirm no out-of-scope edits.

**Progress: 6/6 (100%). Queue empty.**

Q1–Q5 evidence: the five new document-contract cases failed for missing sections before the edits and passed afterward. Version check and `git diff --check` passed. The existing checkout is shared, so edits were confined to untouched target references and these new queue/test files.

Q6 evidence: fresh-context review found two blockers. Added failing regression assertions, then documented source playback when no word timings are available and separated the cut-only branch from the full-decomposition prerequisite. The reviewer session could not be resumed; the two fixes were checked locally against the findings. Final suite: 1,370 passed, 5 skipped, 534 subtests passed. Package 2.63 and 27 skill versions match. `git diff --check` passed. No ASR, editing app, or real-media test was run.
