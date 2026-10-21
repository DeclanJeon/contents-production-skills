# P1 — structured JSONL parser handoff

## Changed files

- `qa/skill-completeness-95/event_trace.py`: new dependency-free `parse_trace(wire_stdout: str, root: Path) -> dict` implementing the shared API.
- `qa/skill-completeness-95/test_event_trace.py`: deferred synthetic protocol safety tests.
- `qa/skill-completeness-95/report-P1.md`: this handoff.

No other files edited; no commits, model calls, uploads, external generation or configuration changes.

## Defects addressed

- Requested read paths come exclusively from correlated `tool_execution_start.args`; args-only reads never become source-confirmed or root-local evidence.
- Reported `result.details.meta.source.value` is preserved, root-local reported paths become root-relative POSIX paths, successful outside/global reads remain explicit in `external_reads`.
- Actual `isError` events generate call/name-associated tool errors. Quoted failure prose in final text does not become an execution failure.
- Result fingerprints are SHA256 of UTF-8 `json.dumps(result, sort_keys=True, separators=(',', ':'), ensure_ascii=False)`.
- Final text comes from the last nonblank completed assistant `message_end` with `stopReason=stop`, excluding tool-use content; deltas and duplicated `agent_end.messages` cannot supply a final.
- Missing final/agent end, malformed JSON, invalid relevant shapes, duplicate/orphan/mismatched calls, unfinished calls, and relevant events after agent end produce protocol errors. Callers must reject traces with protocol errors, even when some valid evidence was extracted.

## Direct evidence read

- `structured-event-contract.md`, lines 1–28: exact shared API and leader-provided observed event excerpt.
- Approved work-order execution addendum, lines 178–288: scope, ownership and deferred-test policy.
- Fixed `rubric-definition.md`, lines 1–34.
- Existing `test_run_cases.py`, lines 1–113: unittest conventions.

No original model stdout artifact was available through the assigned file contract, and no original book passages were needed for this parser-only change. The protocol excerpt was read directly; its provenance is the leader's observation, not a model call performed by P1. No claim slice or skill score is issued.

## Executed non-test smoke

Two direct `python -B -c` API invocations (full commands retained in this worker's tool transcript) imported `event_trace` through `sys.path.insert(0, 'qa/skill-completeness-95')` and printed returned JSON. They did not execute unittest or call a model.

1. Synthetic actual-shaped read start/end with an absolute host-local source, completed assistant answer quoting `file not found`, then agent end: observed `local_path=manifest.json`, `source_confirmed=true`, `success=true`, empty protocol/tool errors, preserved final text, `agent_completed=true`; result hash `132f0e54b858df813aea226a6b63c7f7d0753331f177119602058cce7219cc27`.
2. Synthetic failed read with no source metadata followed by malformed `{`: observed unsuccessful unconfirmed read, associated `bad-read` error, and exactly malformed-JSON/missing-agent-end/missing-final protocol errors; `agent_completed=false`.

These are parser execution evidence only, not real read/model evidence. Neither smoke opened `manifest.json`; the source metadata was synthetic input.

## Deferred integration commands

Run after the shared edit wave, from repository root:

```text
python -B -m unittest discover -s qa/skill-completeness-95 -p test_event_trace.py
python -B -m unittest discover -s qa/skill-completeness-95 -p test_run_cases.py
```

The parent must also run the runner's real explicit-model JSON-mode smoke and retain raw JSONL; confirm a required file has a successful source-confirmed local read and the final answer is extracted. No actual-model execution command is prescribed here because runner/profile ownership belongs to the colleague. Parent owns combined tests and documentation/changelog integration.

## Limits / review points

- Tests were written but not run, per worker contract. No passing-test or independent-score claim.
- External paths and URIs are recorded, not adjudicated as allowed/disallowed by this parser.
- Hashing covers the structured result, not original source-file bytes. Range/display metadata remains in raw stdout, which the runner must retain.
- Protocol error presence is the rejection signal; `agent_completed` means only an actual agent-end event was observed.
