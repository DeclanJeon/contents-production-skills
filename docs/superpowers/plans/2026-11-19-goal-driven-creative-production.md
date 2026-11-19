# Goal-driven Creative Production Implementation Plan

> **For agentic workers:** Use superpowers:executing-plans for inline work; the authorized independent reviewer is read-only.

**Goal:** Continue from the user's approved production goal through applicable stages, with bounded repair and one final full-film review.

**Architecture:** The existing coordinator owns progression; route rows still select one current-stage owner. Existing assets/QA modules own media checks; the worker is never a second ledger or scheduler.

**Tech Stack:** Markdown skills, existing Python/FFmpeg media tools and pytest.

**Spec:** `docs/superpowers/specs/2026-11-19-goal-driven-creative-production-design.md`.

## Global Constraints

Preserve existing approvals, material limits, source IDs, asset/continuity gates and selected-provider boundaries. Do not install or execute external media jobs. Worktree is based on `6b2444d`; no unrelated main edits, commit, merge or publish.

## Review Focus

- A video goal is not permission to submit a job.
- A worker return, first successful take or explicit progress preview is not a stop.
- A directly requested text-only plan/material-limited edit retains its scope.
- Provider capability gaps and a single missing mandatory cut cannot become PASS.
- Valid media files are not proof of perceptual QA or user acceptance.

## Tasks

- [ ] Capture fresh-context baseline and preserve the structural routing test (`python3 scripts/routing_regression.py`). Patch `creative-production/SKILL.md`, `references/production-routing.md`, and text-lane references. Preserve current route identifiers; exercise continuation and stop cases with the same prompts.
- [ ] Copy attributed FrameAtlas sources to `creative-production/references/frameatlas/`; introduce a compact craft selector that references existing story/scene/shot owners. Use local panel fixture, existing sheet assembly/extraction, and a deliberate continuity defect; inspect all panels.
- [ ] Add one `video-production-assets/references/take-repair.md` reference and reachability from actual QA/edit/delivery work. Verify with 10–15-second local fixtures (noise repair and pre-existing phrase replacement) and blocked-provider cases. No live generation claim.
- [ ] Verify required coverage and whole-film QA against existing sequence tools. Run route and media regression suites, actual multi-cut local output plus missing-cut negative case, then independent fresh-context review in the isolated worktree. Journal the evidence and unchecked requirements in Ultragoal.
