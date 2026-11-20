# open-design video craft absorption — validation record (package 2.63)

Branch `feat/open-design-absorption` (from main `1f4f9dd`). Local commit only; nothing pushed or published.

## Ledger (final, read from the CSV)

`docs/superpowers/specs/2026-11-20-open-design-absorption-ledger.csv`: 407 rows = **125 absorb (all `status=absorbed`, 0 `planned`)**, 58 exclude, 224 out_of_scope. Absorbed licenses: Apache-2.0 108, MIT 17 (15 repositories). Excluded (58): 7 `source unavailable` (hyperframes, 404), 9 already external lanes in `manifest.json`, engine/runtime/service-bound skills, and sources whose license was not confirmed as MIT/Apache-2.0 (unconfirmed, Figma terms, AGPL-3.0, non-commercial, conflicting terms, LicenseRef, CC-BY) — see the `reason` column per row.

Absorbed rows by target (spec section 6 counts changed during Task 1; these are the actual numbers): 33-motion-style-library 76, 19-brand-product-integration (19a) 13, 08-animation (08a) 7, 09-edit (09a) 6, 23-finishing-platform (23a) 6, 11-ai-handoff (11a) 4, 29-reference-driven-production (29a) 3, storytelling-with-still-images 2, 30-marketing-story-craft 2, 03-screenplay 2, 10-evidence 1, 06-shots 1, 25-reference-video-analysis 1, 13-ideation-brand 1.

New files under `video-production-assets/references/`: `08a-motion-craft.md`, `09a-short-form-edit-recipes.md`, `19a-product-promo-formulas.md`, `23a-captions-layout.md`, `11a-ai-video-prompting.md`, `29a-template-recreation.md`, `33-motion-style-library.md`, `motion-styles/` (8 family files), `upstream/open-design-provenance.md` and the LICENSE copies; plus `storytelling-with-still-images/references/still-motion-recipes.md`.

## Commands and results

| Command | Result |
|---|---|
| `python3 -m pytest -q scripts` | 505 passed, 1 skipped, 244 subtests passed (baseline 476 passed + tests added across Tasks 1–10) |
| `python3 -m pytest -q scripts/test_open_design_absorption.py` | 11 passed, including the two Task 10 tests |
| RED check for the new tests | Moving `nexu-io-openmotion-LICENSE.txt` away made `test_installed_pack_contains_absorbed_refs` (and the provenance test) fail; asserting `status == "absorbed"` instead of `"planned"` made `test_no_planned_rows_remain` fail. Both reverted. |
| `git diff --stat main -- creative-production/SKILL.md creative-production/references/routing.csv` | empty (routing unchanged) |
| `python3 scripts/routing_regression.py` | rc 0; 33 routes, 79 cases, 0 failing; layered frontier 3 files / 2,820 words / 25,636 bytes (includes the pair table); legacy 4,000 words; saved 30%. Output is **byte-identical** to the same command run on a clean `main` checkout. The spec cites about 1,410 frontier words; the script reports its own layered count (2,820, including the pair table), so the unchanged-vs-main comparison is what is recorded here. |
| `python3 scripts/check_versions.py` | version check OK: package 2.63, 26 skills consistent (after `bump_version.py 2.63`) |
| `python3 scripts/routing_eval.py --limit 3 --out /tmp/routing-eval-od` | **BLOCKED** (see below) |

## Behavioral eval — BLOCKED, not passed

One attempt, `--limit 3` smoke (a single attempt as directed; the 65-case run and the ad-script `--stage handoff` check were therefore not run). The `codex` dispatcher exists on PATH but every dispatch failed: 3/3 cases `dispatch_error` after 2 retries each, accuracy 0/0 scored attempts. Exact error recorded in `summary.json`: `codex exit 1: ... {"type":"item.completed","item":{"id":"item_0","type":"error","message":"Codex is ignoring 1 unrecognized configuration setting. ... session-flags: `skills.search_dirs` is ignored."}}` followed by a second error item (truncated in the harness). The controller had reported the Codex usage limit was hit just before this run, which is the likely cause, but the captured error text does not name it. No routing-accuracy or `30-marketing-story-craft.md` read-through claim is made.

## Limits

- Fidelity of each adapted section to the cached original (no invented numbers or rules) was checked by reviewers per task (`.superpowers/sdd/.../task-N-findings-*.md`), not by tests. Tests only check structure: source lines, provenance and license copies, engine-string absence, link/anchor resolution, style-index coverage, ledger state, and installed-pack contents.
- No behavioral measurement of whether an agent reads the new references; routing is unchanged by construction.
- Upstream content was read from public raw files at the pinned commits; nothing from upstream was executed.
- Not pushed; local commit only.
