# W0 — review handoff

## Changed files

- `run_cases.py`: new sequential explicit-model OMP runner and frozen manifest builder.
- `test_run_cases.py`: deferred consumer-visible boundary tests.
- `case-manifest.json`: generated 61 exact fenced prompts, hashes, byte sizes, source line ranges, assertion rows; evaluator initially null.
- `environment.md`: observed runtime evidence, inherited evidence, identity/safety limits.
- `report-W0.md`: this handoff.
- `claims-W0.tsv`: authored-design claim slice; no book-derived claims.

All paths above are under `qa/skill-completeness-95/`. Historical runners, frozen sources, shared manifest/version/docs/ledger and other workers' skills unchanged by W0.

## Defects addressed

1. Extracts 59 actual `text` fences plus S1a/S1b, rejects missing/duplicate/unexpected IDs, excludes Scoring. Preserves bytes between opening and closing fences, including terminal newline and original line endings.
2. Verifies all four original frozen hashes AND sizes before extraction/execution; matrix assertions are attached by actual line, including supplementary scoring lines 32/33. Execution re-derives the manifest and refuses modified prompt/source/assertion data.
3. Cache identity binds prompt hash, tree hash, explicit model, executable/version, series, tool configuration and runner hash. A run-directory identity change is rejected, not silently merged into historical evidence.
4. Failure attempts remain immutable, numbered artifacts; raw stdout/stderr bytes, decoded output, exact argv, exit code, start/end timestamps and duration recorded. Timeout/nonzero/blank/read failures are not completed cache entries. Successful execution is UNREVIEWED, not PASS.
5. Tree fingerprint includes skill code/assets/references and repository config; excludes growing QA/VCS/cache data. Pre-case mutation stops; in-case mutation invalidates response and stops arm.
6. Default concurrency 1; explicit tools `read,grep,glob`, no LSP/extension discovery. No Codex fallback or security/rules-disable switches.

## Original evidence directly read

- `docs/superpowers/plans/2026-10-16-skill-completeness-95-work-order.md:178-339`, particularly T0/T1.
- `qa/2026-10-16-corpus-audit/rubric-definition.md:1-34`.
- Entire original `baseline-prompts-exact.md` prompt regions (lines 1-372 in two reads), `baseline-prompts.md:1-34`, `baseline-matrix.md:1-48`, `baseline-matrix-vpa.md:1-58`, `prompts.sha256:1-14`.
- Repository `manifest.json:1-85`: current owner names/version for scope only.
- Actual `omp --help`: v18.11.1 and supported flags. No book originals used or craft evidence claimed.

## Exercised local verification

1. `omp --help` — exit 0, actual supported flags observed.
2. `python -X utf8 qa/skill-completeness-95/run_cases.py --manifest qa/skill-completeness-95/case-manifest.json --build-manifest` — exit 0; all four hashes/sizes matched; 61 unique cases generated.
3. `python -X utf8 qa/skill-completeness-95/run_cases.py --help` — exit 0 after final runner edit; advertised exact CLI and allowed IDs observed.

No unit tests/linters/formatters or model-case arm executed mid-wave. An intermediate line-number edit introduced syntax errors, immediately corrected using fresh displayed lines; final CLI smoke passed. No skill score assigned.

## Parent integration commands (not yet run)

After shared edit wave, first:

```text
python -X utf8 -m unittest discover -s qa/skill-completeness-95 -p test_run_cases.py
python -X utf8 qa/skill-completeness-95/run_cases.py --manifest qa/skill-completeness-95/case-manifest.json --run-dir qa/skill-completeness-95/runs/omp-readonly-final-01 --case M-03
python -X utf8 qa/skill-completeness-95/run_cases.py --manifest qa/skill-completeness-95/case-manifest.json --run-dir qa/skill-completeness-95/runs/omp-readonly-final-01 --case M-04
python -X utf8 qa/skill-completeness-95/run_cases.py --manifest qa/skill-completeness-95/case-manifest.json --run-dir qa/skill-completeness-95/runs/omp-readonly-final-01 --case S1a
```

Inspect actual tool/output evidence and confirm read-only boundary for this tightened profile. Then execute all remaining cases in the same stable tree/profile (completed probes cache-reused):

```text
python -X utf8 qa/skill-completeness-95/run_cases.py --manifest qa/skill-completeness-95/case-manifest.json --run-dir qa/skill-completeness-95/runs/omp-readonly-final-01
```

Independent reviewer must adjudicate all 61 UNREVIEWED responses against attached assertions and inspect errors; runner never supplies automatic PASS. If skills/config/model/runner change, use a NEW run directory. Failed attempts retry on same identity while preserving earlier files. Rebuilding manifest requires a new output filename because builder is exclusive-create, by design.

## Unresolved limits / cross-owner requests

- T1 fresh-session M-03/M-04/S1a and full 61-case arm remain parent integration work, explicitly deferred during skill changes. Parent-reported working prior OMP probe is not a substitute for this exact profile.
- No filesystem sandbox or global-provider/config-content fingerprint claimed; inherited runtime settings require operator disclosure if changed. Tool selection is the primary side-effect constraint; persistent tree mutation detection is secondary. Read tools may access permitted outside paths/network reads. Neither paid-provider actions nor write tools are enabled by this runner.
- Text-mode output cannot automatically prove every tool invocation or semantic completeness; stdout/stderr are raw available evidence. Conservative error-string screening may flag a response discussing a read failure; review and retry rather than turning it into PASS. Explicit evaluator and evidence slots remain null/empty until independent review.
- Leader owns current 24-owner integration inventory, workspace snapshot, aggregate run/state/ledger/scorecard, package docs/changelog/version. Record this new series separately from historical Codex/alternate results.
