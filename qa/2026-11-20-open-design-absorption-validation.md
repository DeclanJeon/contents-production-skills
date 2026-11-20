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

## Post-release QA (2026-11-20): reachability probes

Real agent probes replaced the BLOCKED Codex eval: `pi --print --mode json --no-skills --skill <isolated install> --tools read,ls,find,grep --model anthropic/claude-sonnet-5-5`, one run per prompt, text only. Tool-call logs are summarized in `qa/2026-11-20-open-design-reachability-probes/` (read/grep paths only; one repeat, one model — stability is not measured).

**Defect found and fixed.** Before `16edb76`, 0 of 5 probes opened any absorbed reference. The spec (section 6) required a conditional link in each host module; the plan replaced that with `module-index.md` rows only, which agents did not open. `16edb76` adds one conditional link per host module (03, 05, 08, 09, 10, 11, 15, 19, 23, 29) and in `video-production-assets/SKILL.md` (+58 words), plus `test_new_references_linked_from_host_and_skill` with a corruption check.

| Probe | Before | After `16edb76` |
|---|---|---|
| p1 product ad script (no destination) | 03 only | grep `30#od-openmotion-ad-script`; output: 0–1.5 s hook, 3 angles offered, no CTA |
| p2 motion style, kinetic type | 08 only | 33 index → 08a → `motion-styles/kinetic-type.md` only |
| p3 podcast → shorts | no skill read | no skill read (same on 2.62 main: SKILL.md only) — skill discovery, not this change; p3b naming the skill: 09 → 09a |
| p4 tumbler sale promo with photos | creative-production → storytelling-with-still-images | same; identical on 2.62 main (stills route chosen because photos exist). 19a is not reached from the stills lane — open follow-up |
| p5 bilingual captions + lower thirds | 15 only | `23a-captions-layout.md` |

Checks re-run after the fix: `pytest scripts` 507 passed / 1 skipped; `routing_regression.py` 79 cases, 0 failing; `creative-production/` diff vs main empty; isolated install 248 links / 78 `#od-` anchors, 0 broken. Probe outputs are model text, not package facts or creative-quality acceptance.

## Craft bridge probes (2026-11-21)

Same method as above, driven by `scripts/agent_read_probe.py` over `creative-production/evals/agent-read-probes.json` (model `anthropic/claude-sonnet-5-5`, install with `--exclude-derived-support`, read-only tools, one run per case, no reruns). Reads, final answers and `summary.json` are in `qa/2026-11-20-craft-bridge-probes/`; raw JSONL is not kept. One run, one model: stability is not measured, and a read is not evidence of correct use.

| Case | Kind | Opened key files | Verdict |
|---|---|---|---|
| p1 ad script | positive | creative-production/SKILL.md → video-production-assets 03 → `30-marketing-story-craft.md` | pass |
| p2 motion style | positive | SKILL.md → `33-motion-style-library.md` → `motion-styles/kinetic-type.md` | pass |
| p3 podcast → shorts (no skill named) | positive | SKILL.md → 09-edit → `09a-short-form-edit-recipes.md` | pass |
| p4 tumbler sale promo, photos exist | positive | SKILL.md, routing.csv, routing-disambiguation.csv only; no `19a`, no module opened | **fail** |
| p5 bilingual captions + lower thirds | positive | SKILL.md → `23a-captions-layout.md` | pass |
| n1 Instagram caption | negative | none | pass |
| n2 logo image | negative | none | pass |
| n3 video summary → blog | negative | none | pass |
| s1 30 s cafe brand video | nonstop | SKILL.md, routing, policy, orchestrating-video-preproduction stage-execution | controller review pending |

- **p4 fails and is recorded as a failure.** The agent read the entry and routing tables, then answered from its own knowledge without opening any craft reference. The earlier probe (p4 above) at least reached `storytelling-with-still-images`. The brief's widened description opened the entry, but the bridge did not make the agent open `19a`. Not rerun to obtain a pass; the follow-up is open.
- No run opened `creative-production/references/craft-bridge.csv`. p1, p2, p3 and p5 reached their reference through the routing tables or module links, not through the bridge, so these results do not show that the bridge itself is read at S0x handoffs.
- The tool's keyword hints for s1 (`기획`, `대본` missing, approval request present, no completion claim) are candidates only; the answer has a spine, synopsis and storyboard with image prompts but no section titled script. The decision stays with the controller.
- The `opened` lists in `summary.json` include `.` for `grep` calls without a file path; these are not file reads.

### Craft bridge placement fix (2026-11-21)

After the first run, `creative-production/SKILL.md` moved the bridge read from Step 4 ("Hand off") to right after route selection in Step 1 (commit `d1e11e2`; Step 4 keeps a `craft_refs` pointer). Same tool, cases and model, one run per case, no reruns: `qa/2026-11-20-craft-bridge-probes/after-placement/` (earlier results kept in the parent directory). One run, one model: a read is not evidence of correct use, and the 2/9 vs 0/9 difference is not a stability measurement.

| Case | `craft-bridge.csv` opened before → after | Expected ref opened before → after | Verdict before → after |
|---|---|---|---|
| p1 ad script | no → **yes** (read) | yes → yes (`30-marketing-story-craft.md`) | pass → pass |
| p2 motion style | no → **yes** (grep) | yes → yes (`33-motion-style-library.md`) | pass → pass |
| p3 podcast → shorts | no → no | yes → yes (`09a-short-form-edit-recipes.md`) | pass → pass |
| p4 tumbler sale promo | no → no | no → no (`19a` unopened) | **fail → fail** |
| p5 captions + lower thirds | no → no | yes → yes (`23a-captions-layout.md`) | pass → pass |
| n1 Instagram caption | no → no | n/a (SKILL.md not opened) | pass → pass |
| n2 logo image | no → no | n/a | pass → pass |
| n3 video summary → blog | no → no | n/a | pass → pass |
| s1 30 s cafe brand video | no → no | n/a | controller verdict (unchanged by this run) |

- The bridge was opened in 2 of 9 runs (p1, p2), up from 0 of 9. Both are opened through the Step 1 instruction; p2 only grepped it.
- **p4 still fails.** The agent read only `SKILL.md` and `routing.csv` (not even `routing-disambiguation.csv`), then answered from its own knowledge with an R10 text storyboard. The Step 1 instruction did not make it open the bridge. Not rerun; the follow-up is open.
- p3 and p5 reached their reference through routing/module paths and still skipped the bridge, so those passes do not show bridge use.
- s1 read `SKILL.md`, `routing.csv` and `concept-intake-design/SKILL.md` and stopped there in this run (earlier run read more); the tool's keyword hints are candidates only and the verdict stays with the controller.

## 3-run results (2026-11-21)

After the single-run results above (p4 still failing), three more stages were each run three times with the same tool, the same nine cases and the same model (`anthropic/claude-sonnet-5-5`). Summaries, the install-relative read lists and the final answers (no raw JSONL) are committed under `qa/2026-11-20-craft-bridge-probes/`:

| Stage | Directory | Package state |
|---|---|---|
| before triggers | `3x-before-triggers/r1..r3` | Step 1 bridge read, infer-and-propose nonstop (`0e2bb6e`); no inline craft triggers yet |
| after nonstop fix | `3x-after-nonstop/r1..r3` | inline craft triggers and the first review round (`1958ed1`, `e6b8e97`) |
| final | `3x-final/r1..r3` | G1 checkpoint continues, gate-only closing (`428eb52`) |

| Stage | Positives (p1–p5, 3 runs = 15) | Negatives (n1–n3, 3 runs = 9) | s1 (30 s cafe brand video) |
|---|---|---|---|
| before triggers | 15/15 | 9/9 | no upfront question 3/3; **stopped at the concept packet with an optional next-step offer 2/3** (r1, r2); r3 went on to storyboard |
| after nonstop fix | 15/15 | 9/9 | continued past the concept packet to storyboard/shot list 3/3; ended with the facts that cannot be inferred (brand name etc.) and the execution approval; r1 and r2 still end with an optional "원하시면 … 이어서" offer, r3 with an option menu ("고르시면 이어서 진행합니다") |
| final | 15/15 | 9/9 | continued past the concept packet to storyboard/shot list 3/3; ended with non-inferable facts (brand name, slogan, logo, production method) and the execution/spend approval |

- **Known residual, not a pass:** in `3x-final` a soft optional continuation offer still appears 3/3 despite the gate-only closing rule (r1 and r2: "원하시면 … 이어서"; r3: "이 정보를 주시면 … 이어서 작성하겠습니다"). The rule is written but the model does not fully follow it; no further fix was made.
- The positive passes in all three stages are auto-judged by the expected reference being opened. `craft-bridge.csv` itself was opened in 1 of 15 positive runs before triggers and 0 of 15 afterwards, so the passes reflect the inline triggers in `creative-production/SKILL.md`, not reads of the bridge table; p4, which failed in every earlier run, passed 3/3 at every stage here.
- Limits: one model, three runs per stage, so this shows stability over three samples, not a rate. A read is not evidence of correct use. The probe prompt is text-only, so image-sheet execution was never in scope. The s1 judgement (continued, ended at gates) is by reading the final answers, not by the tool, whose keyword hints are candidates only. The codex `routing_eval` remains BLOCKED (Codex dispatch failed), so the behavioral routing eval has still not run.
