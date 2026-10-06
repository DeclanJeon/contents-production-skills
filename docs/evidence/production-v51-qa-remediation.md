# Production v5.1 QA remediation — implementation evidence

## Status

The authorized Q01–Q23 implementation, native acceptance corpus, and post-review repros are complete. ReviewGatePublication and ReviewHistoryHandoff both returned final **APPROVE**. Follow-up probes now reject stale/replaced extraction bytes, cross-panel aliases, alpha-only pixel changes, overlapping panel/scene bounds, and case-folded report collisions; positive controls include single-sheet legacy FINAL18, repeated S01→S02→S01 FINAL26, and 10-panel/two-sheet FINAL30.

The default-locale `python -m pytest -q` invocation exited 1 (30 failed, 240 passed, 205 subtests passed): 27 Windows cp949 decode failures in out-of-scope UTF-8 fixture readers and 3 checker assertion expectations fixed semantically. The updated focused regressions passed; a complete `python -X utf8 -m pytest -q` run then passed (258 passed, 217 subtests). The UTF-8 mode changes decoding configuration only and does not skip/suppress tests. Version check and isolated 18-skill install/runtime/package smoke also passed. Complete exact output is in [final verification evidence](production-v51-final-verification.json).

Implementation, native QA and both independent code reviews are complete. Deployment remains **BLOCK** because no deployment was requested or authorized; this is not an unresolved code-review finding. The original QA fixture and support cache remain unmodified. The native acceptance record reports source-ledger SHA-256 `584405823dbb544fb380c347d1ab9b5b3373c14b58d780ded890af9c65b3fd7f`, `source_qa_ledger_unchanged: true`, and 18 checked source assets with no changed IDs.

## Resolved independent review findings

- **Q02:** Shared readiness now checks current sheet registration/hash/order, each split entry path, actual panel/scene output hashes and RGBA pixels, and rejects aliases. Original single-sheet registry rows may omit `sheet_index`; PNG metadata must still identify index 1. Native probes rejected stale sheet/hash, P02→P01 alias, alpha-only mismatch, and panel/scene overlap; real FINAL outputs were absent on rejection.
- **Q04:** FINAL preserves repeated chronological scene bands, including S01→S02→S01 on one sheet, while rejecting overlapping panel or scene rectangles. A six-panel FINAL26 positive control passed.
- **Q05:** Case-folded reserved report-path collisions reject for directory and ZIP publication before replacing source bytes or publishing an archive.
- **Q09:** Escaped quotes inside credential values no longer leak the secret suffix into events or prompt snapshots; original prompt bytes/digest and creative fields remain unchanged.
- **Q10:** The chronologically current explicit attempt governs completion outputs, even when its ID is lower than an older attempt. Missing current output blocks completion; missing superseded output does not block a successful retry.
- **Q14:** Panel-pin drift invalidates only the selected canonical storyboard and its actual downstream branch. Unrelated ALT/ALT_CHILD/AUDIO remain reviewed, and historical pins remain unchanged.
- **Q15:** Canonical panel pins and master/LOOK ancestry are collected when BOARD is reached transitively through SHEET/GEN artifact focus. Unrelated ALT and shot-focused SH01 controls remain narrow.

The corrected physical-root evidence is under `C:\Users\Declan\Documents\03_studio_production\production-v51-remediation-parent-verification-20261006-233729\`. The follow-up summary records the reviewer-resolved cases; raw evidence retains initial failed probes and invalid-fixture/external-alias rows accurately rather than treating every historical probe as green.

## Final verification commands and observed results

The default-locale full-suite command was executed once, and the corrected UTF-8 full suite was run after the final test changes. An earlier UTF-8 run is retained as a pre-final intermediate result:

```text
python -m pytest -q
exit 1: 30 failed, 240 passed, 205 subtests passed in 26.22s

python -X utf8 -m pytest -q video-production-assets/scripts/test_render_storyboard_sheet.py::StoryboardRenderTests::test_crop_source_hashes_register_as_actual_inputs video-production-assets/scripts/test_validate_preproduction.py::PreproductionGateTests::test_missing_wrong_stale_or_incomplete_deliverables_block_review
exit 0: 2 passed, 15 subtests passed in 6.06s

python -X utf8 -m pytest -q
pre-final intermediate: 258 passed, 217 subtests passed in 30.80s
final after CLI-test edits: 258 passed, 217 subtests passed in 47.18s

python scripts/check_versions.py
exit 0: version check OK: package 2.4, 18 skill(s) consistent
```

The default run's 27 external failures were Windows `cp949` `UnicodeDecodeError` exceptions while unrelated Blender/camera tests read the UTF-8 `camera-spatial-design/assets/camera-spec-example.json`. The 3 initial production test failures were assertion-only: they were replaced by actual `validate_project.py --profile preproduction` consumer CLI checks. The valid fixture exits 0 with `valid:true`; each of 15 mutated readiness fixtures exits 1 with `valid:false`; crop-source hash corruption is also rejected by the CLI. No Blender or camera files were edited, and UTF-8 mode does not skip or suppress tests. Exact commands, exit codes, stdout, and stderr are in [the raw final verification record](production-v51-final-verification.json).

### Clean isolated staging install and runtime

The original source `video-production-assets/support` cache remains untouched. A fresh temporary checkout was built from the manifest-listed 18 skills plus root support sources, excluding that cache only in the staging copy.

Temporary stage: `C:\Users\Declan\AppData\Local\Temp\production-v51-final-stage-1791307658711-e7eda3`

Installer exit 0 installed all 18 skills (package 2.4); installed history CLI `init` and `status` both exited 0; installed `package_production.py` successfully packaged `runtime-package-final\staging-smoke-final_v0.1` from a valid schema 1.1 synthetic smoke ledger with 0 assets/history entries and a clear asset gate. This stage was created after the final test edits. An earlier attempt using init's unmodified incomplete ledger exited 1 without creating a package; the valid synthetic ledger then passed. No global installation occurred.

In addition, the parent exercised significant paths from an independently installed package—not only the empty-ledger smoke above. Six implementation files in the installed stage matched the live repository. In stage `C:\Users\Declan\AppData\Local\Temp\production-v51-final-stage-1791306997051-3f81f5`, installed package CLI accepted real image-backed FINAL18 assets and rejected a transparent P02 pixel mismatch with no target package. Installed history CLI covered attempt 7 failure, attempt 3 completion, deletion refusal/restored-file completion, prompt/digest preservation and event/snapshot secret redaction; final status was completed with two attempts, `current_attempt=3`, no in-flight operations and five events. Exact parent command/result cases use prefix `final-installed-` in [the physical-root follow-up raw evidence](file:///C:/Users/Declan/Documents/03_studio_production/production-v51-remediation-parent-verification-20261006-233729/independent-review-followup-evidence.json).

The latest stage above was independently checked as well: all six changed implementation-file hashes matched the live repository; its installed package CLI accepted the actual image-backed FINAL18 control and rejected transparent P02 without publishing a target. Its installed history CLI read the real completed 7→3 lifecycle with two attempts, `current_attempt=3`, five events and no in-flight operations from the earlier owned runtime root. These exact commands/results are the `latest-installed-*` cases in the same raw follow-up evidence.


## Independent Windows CLI/API acceptance

The parent acceptance run reports all 23 findings passed, including positive controls for FINAL refusal/acceptance, PRELIMINARY and text-only scope, source provenance, scene assembly, relocation/repackage, lifecycle attempts, explicit-root initialization, and stale propagation. Q15 was rerun after retaining the active `look_asset_id` in focused project metadata. Q14 exercised an actual guarded update: `ANIMATIC`, `BOARD`, `GEN`, and `SHEET` became stale; unrelated `AUDIO` stayed reviewed; the historical panel pin remained at version 1 and FINAL readiness rejected stale history.

- Final Q01–Q23 case mapping: `C:\Users\Declan\Documents\03_studio_production\production-v51-remediation-parent-verification-20261006-233729\independent-final-acceptance-summary.json` (`all_23_passed: true`).
- Raw CLI/API transcript, including initial failed probes and their corrected fixtures: `C:\Users\Declan\Documents\03_studio_production\production-v51-remediation-parent-verification-20261006-233729\independent-acceptance-evidence.json`.
- Q02/Q04/Q05 resolved after-probes and reviewer finding summary: `C:\Users\Declan\Documents\03_studio_production\production-v51-remediation-parent-verification-20261006-233729\independent-review-followup-summary.json`; raw follow-up evidence: `C:\Users\Declan\Documents\03_studio_production\production-v51-remediation-parent-verification-20261006-233729\independent-review-followup-evidence.json`.
- Independent final reviewers: ReviewGatePublication and ReviewHistoryHandoff both APPROVE; the co-located follow-up summary documents resolved issues and confidence.
- Q15 post-fix CLI invocation: `python video-production-assets/scripts/project_index.py "C:/Users/Declan/Documents/03_studio_production/production-v51-remediation-parent-verification-20261006-233729/Q15-focused-ancestry/project.json" --shot SH01` exited 0 and returned `project.look_asset_id: LOOK_ACTIVE`, the active LOOK/master ancestry and pins, while excluding unrelated SH02.
- Independent read-only-status review case: `review-history-status-readonly-regression-fixed` in the parent acceptance transcript. A no-history project returned `event_count=0` with its directory/file tree unchanged; `status` created no `.history` directories.

## Real synthetic FINAL package and visual inspection

The positive FINAL exercise generated a ZIP, extracted it in a fresh root, checked portable snapshot paths and file hashes, and successfully FINAL-repackaged it. The 10-panel storyboard was rendered across two sheets and scene overviews were assembled across the sheet boundary. I opened both generated sheets:

- `.../positive-cross-sheet-final/04_STORYBOARDS/sheets/parent-final_s01.png` — 2320×2650, FINAL sheet 1/2, panels P01–P08.
- `.../positive-cross-sheet-final/04_STORYBOARDS/sheets/parent-final_s02.png` — FINAL sheet 2/2, panels P09–P10.

These are synthetic flat-color source fixtures and establish mechanical layout, panel labeling, and extraction flow only. They do **not** establish artistic quality, character identity, rights, or human approval. The full paths are under `C:\Users\Declan\Documents\03_studio_production\production-v51-remediation-parent-verification-20261006-233729\positive-cross-sheet-final\04_STORYBOARDS\sheets\`.

## Q01–Q23 implementation/test coverage

The plan’s Q01–Q23 table is the source-of-truth acceptance description; the independent summary above records the native CLI/API case result for every row.

| QA | Implementation and regression coverage |
|---|---|
| Q01 | `video-production-assets/scripts/asset_gate.py`; `test_asset_gate.py` master-ancestor/direct-master cases |
| Q02 | `asset_gate.py`, `validate_preproduction.py`; `test_validate_preproduction.py` extraction freshness, aliases, pixel/alpha and overlap; actual CLI valid/invalid matrix |
| Q03 | `split_storyboard.py`; `test_split_storyboard.py` forged/missing source provenance |
| Q04 | `package_production.py`; `test_asset_gate.py` panel alias, actual pixels/scene reconstruction, repeated chronological bands |
| Q05 | `package_production.py`; `test_asset_gate.py` case-folded reserved report-path collisions |
| Q06 | `render_storyboard_sheet.py`; `test_render_storyboard_sheet.py` paginated dangling-link/no-partial-write case |
| Q07 | `package_production.py`; `test_asset_gate.py` history-link export confinement |
| Q08 | `recording-production-history/scripts/production_history.py`; `test_production_history.py` events/prompts/lock link confinement |
| Q09 | `production_history.py`; prompt/event/snapshot redaction behavior tests |
| Q10 | `production_history.py`; current output existence and failed/interrupted completion tests |
| Q11 | `production_history.py`; stale terminal attempt cannot close current attempt tests |
| Q12 | `package_production.py`; `test_asset_gate.py` fresh-root ZIP relocation/repackage round-trip |
| Q13 | `package_production.py`; `test_asset_gate.py` injected copy-time source mutation tests for ZIP and directory publication |
| Q14 | `update_project.py`; `test_project_handoff.py` panel-only stale propagation and unrelated branch preservation |
| Q15 | `project_index.py`; `test_project_handoff.py` focused active LOOK/master ancestry; `look_asset_id` also appears in project metadata |
| Q16 | `split_storyboard.py`; `test_split_storyboard.py` panel overlap and scene-band containment tests |
| Q17 | `production_history.py`; `test_production_history.py` exact selected-root/reinit/foreign-ledger preservation |
| Q18 | `production_history.py`; `test_production_history.py` original raw-byte prompt hash and CRLF/LF behavior |
| Q19 | `production_history.py`; `test_production_history.py` child-exit atomic initialization/retry and corrupt-ledger preservation |
| Q20 | `production_history.py`; `test_production_history.py` explicit attempt retention across resume/terminal |
| Q21 | `production_history.py`; `test_production_history.py` project-scope events excluded from operation attempt count |
| Q22 | `production_history.py`; `test_production_history.py` quoted/newline operation description round-trip |
| Q23 | `validate_storyboard.py`; `test_validate_storyboard.py` structured list/object selector diagnostics and standalone omission |

## Limits and open gates

- Verification was performed on Windows 10 / Python 3.12. Native macOS and Linux behavior was not run. Redirected/OneDrive Documents, sustained concurrent writers, actual disk-full behavior, provider integrations, Blender, and real media generation were not exercised.
- Default-locale full-suite errors are retained as environmental evidence; the complete suite passed under explicit Python UTF-8 mode. The source support-cache collision is preserved and documented; staging used a clean temporary copy with that cache excluded.
- Mechanical Q01–Q23 acceptance and both final code reviews passed. Deployment remains **BLOCK** until an explicit release authorization is given.
