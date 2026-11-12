# Matt writing craft — native Codex discovery baseline

Historical discovery checkpoint only. Later candidates, contained-reader changes and the complete matched-high v9 result are recorded in the [current integration review](../../qa/matt-writing-integration-review.md); do not treat the historical absence of a candidate/reviewer below as current status.

## Scope and authorization

User selected **Codex CLI / `gpt-6-luna`**, no total monetary ceiling, and delegated baseline-source choice. The isolated worktree imported 31 conflict-free latest-source files, including Korean postediting dependencies. Original repository, installed skills, publishing and Git integration were not changed.

- CLI: `codex-cli 0.167.0`, existing ChatGPT login, reasoning `low`.
- Baseline package: 2.33, 22 skills; **285 runtime files**.
- SHA-256: `85ac6bb7ad60abed38614774f0394322ab739f8ab17ef149e262c7d95a23fc7c`.
- Whole-case deadline 240 seconds, concurrency 1, application resampling/retries **0**.
- Native provider request count, billed USD and provider finish reason are not exposed. Explicit unlimited provider/token/cost fields are not hard spending controls. Native transport retries use CLI defaults; no claim that they were disabled.

## Execution evidence

Evidence is under `.superpowers/sdd/2026-11-11-matt-pocock-writing-craft-integration/`:

- `latest-import.json`, `pre-latest-import/`: source-import hashes and original worktree bytes.
- `codex-evaluation-v2/run-manifest.json`, `adapter-pin.json`, `adapter-source/`: exact source, input, rubric and adapter bytes/hashes.
- `codex-evaluation-v2/runs/baseline/<case>/r<repeat>/`: inputs, native stdout/stderr, command, final response, controlled tool events, native observation and receipt.
- `baseline-reviewed-runs.json`: 70 implementing-assistant review cards pinned to receipt SHA-256s.
- `baseline-r*-review-notes.json`, `baseline-reviewed-counts.json`: direct inspection reasons and quality caveats.

The earlier v1 epoch and capability probes remain separate and retained. v1 stopped on a source-only fixture-disclosure harness error; it was not mixed into v2. Native same-thread memory and exact T09 byte-preservation probes succeeded before v2.

The v2 batch dispatcher stopped on a model pagination-argument error. The existing `run_case` API then submitted **only unstarted slots** with unchanged adapter, inputs and rubric. Existing successes and inconclusive records were retained, not replaced. `continue-unstarted.py` and `continuation-metadata.json` record that operational invocation.

## Results — discovery, not acceptance

All **70 baseline slots** were attempted and directly reviewed: **49 PASS / 15 FAIL / 6 INCONCLUSIVE**. The snapshot remained unchanged. Valid completed receipts passed owner-read, final/settled and stage-count checks. Valid T09 samples preserved the expected bytes. This is author evaluation, **not independent review**.

| Case | PASS | FAIL | INCONCLUSIVE | Observed issue |
|---|---:|---:|---:|---|
| T01 | 5 | 0 | 0 | No demonstrated missing exploration rule |
| T02 | 2 | 3 | 0 | r3 retains use-before-definition; r4/r5 move the comparison function away from B03 while retaining labels |
| T03 | 4 | 0 | 1 | One guessed nonexistent reference path |
| T04 | 5 | 0 | 0 | Intentional reveal timing preserved |
| T05 | 5 | 0 | 0 | One-pass completion preserved; repetition is a quality caveat, not a new criterion |
| T06 | 5 | 0 | 0 | Narrow response scope preserved; semantic/naturalness caveats remain |
| T07 | 5 | 0 | 0 | No fabricated efficacy/source or execution of embedded instructions |
| T08 | 0 | 2 | 3 | Valid r1/r4 provide advice/deferral, not actual replacement wording; other runs have tool errors |
| T09 | 3 | 0 | 2 | Two edits attempted before required post-insertion re-read; guard refused them |
| T10a | 5 | 0 | 0 | Abstract, non-character beats preserved |
| T10b | 5 | 0 | 0 | Single logline artifact preserved; unnecessary inline source annotations noted separately |
| T11 | 0 | 5 | 0 | R1 drafts a script instead of first asking the explicitly unresolved audience decision |
| T12 | 5 | 0 | 0 | Two-option waits, actual prior choices and user-revised B01 preserved |
| T13 | 0 | 5 | 0 | Incompatibility is explained, but the required constraint-waiver question is omitted |

### Admissible minimal integration

Only four observed failure classes justify runtime craft guidance:

1. **T02:** prerequisites before use while preserving stable beat identities/functions; distinguish existing knowledge and intentional reveal withholding.
2. **T08:** a requested text repair ends with usable replacement/reordered text inside the existing assigned return scope, not advice alone or a renewed interview.
3. **T11:** in collaborative drafting, first resolve an explicitly undecided essential choice; reuse supplied purpose/material/ending.
4. **T13:** undelegated hard-constraint conflicts require a minimal user decision question, not unilateral waiver or unexplained dead end.

Passing baseline behaviors protect regressions; they are not improvement claims or grounds to add unrelated rules. No new skill, owner, production field, mandatory general interview or external Matt runtime dependency is justified.

### Inconclusive records and limits

The six inconclusive samples are **not craft failures** and cannot be silently replaced: T03/r4, T08/r2/r3/r5, T09/r2/r4. Causes include guessed missing path, 0-based/large pagination arguments, 50KB read behavior, and a refused edit before re-read. Tool-interface work must preserve these historical records and keep actual read/write safety checks.

The fixed rubric is narrower than overall writing quality. Awkward wording, repeated endings and unnecessary citations are retained as notes, not newly invented success criteria. No audience-comprehension, voice, visual, retention or general reliability claim follows from these results.

**Full evaluation acceptance remains INCONCLUSIVE**: a candidate, complete comparable regression data and independent review are still absent. No global installation, merge, commit/push or publication is authorized by this report.

## Offline verification checkpoint

Full Python: **611 passed / 518 subtests**. Node fixture regressions: **11 passed**. Versions: **2.33 / 22 skills consistent**. Before the final conditional capability wording refactor, type checking was clean; the frozen v2 adapter currently has **0 errors / 2 implicit-string-concatenation warnings**, recorded in `codex-types-v2.log`. Its exact old bytes are archived; do not silently rewrite its identity while evaluating.
