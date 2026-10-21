# Observed OMP JSONL protocol and integration API

Source: leader actually ran explicit-model OMP `--mode json --tools read,grep,glob --no-lsp --no-extensions --no-session` and observed real manifest read; full untruncated output retained in parent artifact118. This schema excerpt is for parser implementation/tests, not a substitute formal-case result.

Observed events (other delta/session/turn events may appear between):

```json
{"type":"tool_execution_start","toolCallId":"call1","toolName":"read","args":{"path":"manifest.json"}}
{"type":"tool_execution_end","toolCallId":"call1","toolName":"read","result":{"content":[{"type":"text","text":"{...actual manifest display...}"}],"details":{"meta":{"source":{"type":"path","value":"C:\\Users\\Declan\\Documents\\Projects\\Skills-and-Automation\\contents-production-skills\\manifest.json"}}}},"isError":false}
{"type":"message_end","message":{"role":"assistant","content":[{"type":"text","text":"Package version: 2.10\nSkill count: 24"}],"stopReason":"stop"}}
{"type":"agent_end","messages":[]}
```

`tool_execution_start.args` is the authoritative requested argument object. `tool_execution_end.result.details.meta.source` supplies the host-resolved path; do not certify an inferred requested path as an observed read. `isError` is on the event. Actual events may carry result display metadata, truncated-display markers and other fields; raw structured stdout must be retained for independent range/scope review. Assistant message starts/deltas and `agent_end.messages` duplicate content; extract final text from last completed assistant `message_end` text before agent_end, excluding toolUse messages. No agent_end or no final answer means incomplete protocol, not successful execution.

## Shared API — fixed for parallel implementation

`event_trace.py` exports `parse_trace(wire_stdout: str, root: pathlib.Path) -> dict` returning:
- `final_text: str`
- `reads: list[dict]`: each record has `tool_call_id`, `requested_path`, `resolved_path` (reported value or null), `local_path` (root-relative POSIX when actually reported/resolved under root, else null), `success: bool`, `source_confirmed: bool`, and `result_sha256` (SHA256 of canonical JSON result). Keep local/outside paths explicit; do not claim source-confirmed from args fallback. Include result display/range metadata if useful, not a copied book corpus.
- `tool_errors: list[dict]` from actual isError events; fields enough to associate name/id/message.
- `protocol_errors: list[str]` for malformed JSONL, missing final/agent_end or relevant invalid shapes. Ignore recognized irrelevant event types; never treat natural answer text as protocol error.
- `external_reads: list[dict]` for successful reported reads outside root or nonlocal URI reads. Record them; final scope adjudication is separate.
- `agent_completed: bool` (actual agent_end observed).

Runner v3 will pass raw JSONL, retain raw stdout/stderr, store extracted final text in `stdout` for downstream graders and structured evidence in `tool_reads`/`tool_errors`/`protocol_errors`/`external_reads`. Required local files must have successful source-confirmed read events. Plain text claiming a source is not equivalent. Actual observed metadata may be absent for URI lookups; record as unconfirmed, do not fabricate resolution.

No source prompt bytes change. New series/profile identity must include parser code hash and JSON output mode. Infrastructure status comes from process/deadline/stderr and structured errors; merely quoting 'cannot read'/'file not found'/'usage limit' in a legitimate final answer is an adjudication flag, not definitive execution ERROR.
