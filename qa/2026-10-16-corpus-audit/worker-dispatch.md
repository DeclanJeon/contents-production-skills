# Frozen-matrix parallel dispatch plan (baseline and post arms)

Direction: once `w1:pC` (tab `w1:tC`) reports `idle`/`done`, run the frozen read-only matrix across the existing idle worker panes in tab `w1:t12`, split into disjoint prompt-ID ranges. Reuse the same ranges and byte-identical prompts for the post-remediation arm. Neither arm may start while `w1:pC` is `working`.

## Preconditions (leader, before either arm)

1. `herdr agent list` shows `w1:pC` `agent_status` not `working`.
2. Pre-edit gate recorded: `git diff --numstat` + HEAD; `python scripts/check_versions.py`; `python -X utf8 -m pytest -q --basetemp='C:/Users/Declan/AppData/Local/Temp/pytest-omp-cps5'`.
3. `prompts.sha256` verified against on-disk `baseline-prompts-exact.md` (16869B, sha256 `36ebdab6506d18ed2086c5b9f364f3e77ce510cbec1c72a5070a1b8d963b84fa`). If it does not match, HALT: the frozen arm is invalid.

## Panes and disjoint ranges

All four panes are in tab `w1:t12` and were `idle` at plan time. Each worker owns a disjoint set; no ID is run by two workers.

| Worker pane | Range (exact `##` headings in `baseline-prompts-exact.md`) | Blocks |
|---|---|---|
| `w1:p15` | `M-01` .. `M-24` | 24 |
| `w1:p16` | `V-01` .. `V-14` | 14 |
| `w1:p17` | `V-15` .. `V-28` | 14 |
| `w1:p18` | `VC-1`,`VC-2`,`VC-3`,`VP-1`,`VP-2`,`VS-1`,`VO-1` | 7 |
| leader (this pane `w1:p12`) | `S1a` + `S1b` from `baseline-prompts.md` | 2 |

Sum: 24+14+14+7+2 = 61 prompts/IDs executed per arm. The denominator is the **prompt blocks**, not the `##` headings: `baseline-prompts-exact.md` holds **59** exact prompt blocks and `baseline-prompts.md` holds **2** exact blocks (`S1a`, `S1b`), so **59 + 2 = 61** prompts per arm. The remaining `##` headings (`Scoring`, `S1a, S1b`) are not prompt blocks and are not counted. Coverage is complete: every frozen prompt block is run exactly once per arm.

`S1a`/`S1b` stay with the leader because they need cross-file reading and the byte-exact copy in `baseline-prompts.md`; `baseline-prompts-exact.md` also carries an `S1a,` heading for traceability but the leader runs the `baseline-prompts.md` wording.

## Per-worker instruction (identical for each)

- Read ONLY `qa/2026-10-16-corpus-audit/baseline-prompts-exact.md`. Take the byte block under each assigned `## <ID>` heading exactly as written; do not paraphrase, retype, or trim.
- For each assigned ID: run one fresh single-turn session with that exact prompt, read-only, no file edits, no side effects, no provider/tool spend, no generation, no publish/deploy/upload.
- Return, per ID: `ID | PASS/FAIL | response excerpt (verbatim, trimmed to the decisive sentences) | file+section locators the response gave | the assertion it met or missed`.
- If the environment cannot run a session for an ID, report `UNRUN` with the reason; do not simulate a response.
- Do NOT edit any file. Report back only.

## Central collection

The leader writes `baseline-results.md` with, per ID: the exact prompt hash source, PASS/FAIL, and the response excerpt verbatim. Failures are preserved verbatim and reported as evidence, never smoothed. A boundary probe that fails identically at baseline and post is reported as a known limit, not a regression.

## Post arm

After remediation, re-run the SAME ranges with the SAME byte-identical prompts in fresh sessions, writing `post-results.md` in the same shape, for a per-ID baseline-vs-post comparison.
