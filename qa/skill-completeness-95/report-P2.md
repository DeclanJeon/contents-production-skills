# P2 structured evidence correction

Status: implementation delivered for parent integration, not independently accepted. No score or behavioral PASS claim.

## Changed files

- `run_cases.py`: v3 JSON-mode command; parser API integration; raw bytes retained and final text extracted; explicit tool/protocol/external read evidence; confirmed local required-read gate; noncacheable missing-read status; infrastructure classifier no longer scans final prose; identity binds parser/output/context/read requirements and existing full profile/tree inputs.
- `test_run_cases.py`: successful execute/cache scenarios now simulate observed structured read/message/agent events; quoted-error-prose success and missing-read regressions; plain-text cache rejection; failed/timeout raw output preservation and mutation invariants retained.
- `case-manifest.json`: series metadata migrated to v3 only; frozen case content unchanged.
- New `case-manifest-v2.raw.b64`: original manifest raw bytes preserved before migration.
- New `runner-profile-v3.md`: exact execution/evidence/cache contract and parent commands.
- `report-P2.md`: this handoff.

P1 files `event_trace.py` and `test_event_trace.py` were not edited. No historical runs, frozen sources, root documents, combined ledgers or scorecards were edited.

## Defects addressed

Previously, natural-language answer tokens could trigger infrastructure ERROR, and plain successful answers could be cached without proof of checkout reads. v3 requires successful source-confirmed local tool read events for the frozen owner/module, including S1a two files, M-03 four modules and S1b emotion module. Actual tool/protocol errors remain ERROR. External/global reads are explicit evidence for independent scope review; they cannot satisfy required local paths.

No source text was added to prompts. Reviewed system owner directive, safe-tool restriction, sequential 180-second execution and docs-raster-only hash exclusion remain.

## Evidence directly read

- Execution addendum lines 178–290 of the approved work order.
- Fixed `qa/2026-10-16-corpus-audit/rubric-definition.md`.
- `structured-event-contract.md` including observed tool start/end source metadata and the agreed `parse_trace` API. This is a contract read, not a claim that P2 observed the leader's original runtime stream.
- Existing runner, relevant complete tests, manifest metadata and frozen prompt discovery for exceptional required paths.

No original book passages were needed or claimed: this worker changes evidence transport, not craft claims. No claims slice was created because ownership is limited to the six assigned files.

## Executed local non-test checks

1. `python qa/skill-completeness-95/run_cases.py --help` exited 0 and displayed all 61 selectable case IDs and execution arguments.
2. Local manifest/archive computation decoded the base64 archive and compared JSON with only series normalized; independently rebuilt the manifest from frozen sources using `build_manifest`.

Observed output:

```text
archive_sha256=c1e6205841a4df33a3dea169a0fa1e01416519ced66c4fb62db853bc8e5e3cbd
series_only_migration=True
frozen_manifest_match=True
case_count=61
required_read_counts={'M-03': 4, 'S1a': 2, 'S1b': 1}
```

The first two shell attempts to encode the byte archive failed due to nested PowerShell quoting/shell syntax; the subsequent single-quoted PowerShell byte-to-base64 command succeeded. No manifest edit occurred until that archive existed. Decoding/comparison above verifies the resulting archive.

## Limits and exact integration commands

All tests/builds/linters/formatters and formal model runs are deferred by the approved shared-wave contract. CLI help and manifest computation do not prove parser integration or live source reads. No v3 behavioral result, final score or 61-case success is claimed. The parent must integrate P1 and execute:

```text
python -m unittest discover -s qa/skill-completeness-95 -p test_event_trace.py
python -m unittest discover -s qa/skill-completeness-95 -p test_run_cases.py
python qa/skill-completeness-95/run_cases.py --manifest qa/skill-completeness-95/case-manifest.json --run-dir qa/skill-completeness-95/runs/omp-readonly-local-owner-v3-smoke --case S1a
python qa/skill-completeness-95/run_cases.py --manifest qa/skill-completeness-95/case-manifest.json --run-dir qa/skill-completeness-95/runs/omp-readonly-local-owner-v3-final
```

Inspect actual raw stdout and required-read evidence after the smoke, then independently adjudicate assertions and external/global reads. Frozen root sources remain unchanged; v2 cancelled-arm records are preserved, not combined into v3.
