# Structured checkout-read runner v3

Series: `omp-readonly-local-owner-v3`. Historical v2 run directories remain untouched; the v2 full arm was cancelled after review and is not a completed baseline.

## Execution contract

- Sequential, explicit `openai-codex/gpt-6.1-sol`, OMP `--mode json`, `--max-time 180`; host communication deadline 195 seconds. Timeout retains partial raw bytes and terminates the process (Windows process tree).
- Tools remain `read,grep,glob`; no LSP, extensions, session persistence, source-content injection or provider actions. The reviewed append-system owner directive remains intact. Parent integration adds verified OMP `--no-skills`: automatic host/global skill discovery/loading is disabled, while the model must manually read the applicable checkout skill/module. This measures explicitly owner-assisted package application, not automatic skill discovery; no rules or safety permissions are disabled.
- Raw `.stdout` is full original JSONL bytes, not extracted prose. Raw `.stderr` is retained separately. Attempt JSON `stdout` is the parser's final assistant text.
- `event_trace.parse_trace(wire_stdout, root)` supplies `structured_evidence`, `tool_reads`, `tool_errors`, `protocol_errors`, `external_reads`. Source-confirmed successful root-relative local reads are required. External/global reads are recorded for independent scope adjudication, not silently accepted as checkout reads.
- S1a requires modules 16 and 12; M-03 requires 16, 12, 10 and 17; S1b requires 16. Every other case requires the frozen assertion's owner `SKILL.md` or named module.
- Missing reads produce noncacheable `checkout-read-missing`; actual tool errors produce `tool-error`; malformed/incomplete protocol produces `protocol-error`. These receive `ERROR`, never PASS. Clean execution remains `UNREVIEWED` pending independent assertion evaluation.
- Final prose quoting `cannot read`, `file not found` or `usage limit` is not an infrastructure failure. Process return code, deadline, stderr and structured trace control execution status. Tree mutation overrides execution success.

## Identity and preservation

Identity binds frozen prompt, tree, model/profile, exact owner context, required read set, JSON output mode and parser SHA256. Profile additionally binds runner SHA256, executable/version and environment selectors. Plain v2 attempts cannot be reused. Completed cache entries must carry final text, completed protocol, no tool/protocol errors and confirmed required reads.

Instruction/code/skill assets remain fingerprinted. Only raster images under `docs/` are excluded as archival screenshots; assets elsewhere remain covered. QA/cache exclusions are unchanged.

`case-manifest-v2.raw.b64` preserves original manifest bytes (decoded SHA256 `c1e6205841a4df33a3dea169a0fa1e01416519ced66c4fb62db853bc8e5e3cbd`). Current manifest changes only `series` metadata semantically; all 61 cases, prompts, assertions and four frozen source descriptors remain unchanged.

## Parent integration commands

After P1/P2 shared wave ends:

```text
python -m unittest discover -s qa/skill-completeness-95 -p test_event_trace.py
python -m unittest discover -s qa/skill-completeness-95 -p test_run_cases.py
python qa/skill-completeness-95/run_cases.py --manifest qa/skill-completeness-95/case-manifest.json --run-dir qa/skill-completeness-95/runs/omp-readonly-local-owner-v3-smoke --case S1a
python qa/skill-completeness-95/run_cases.py --manifest qa/skill-completeness-95/case-manifest.json --run-dir qa/skill-completeness-95/runs/omp-readonly-local-owner-v3-final
```

Use fresh run directories if tree/profile/parser changes. Before the full arm, inspect smoke raw JSONL and attempt evidence for both required resolved local paths; success status alone is not assertion PASS. No formal v3 model arm or tests were run by P2 during the shared edit wave.
