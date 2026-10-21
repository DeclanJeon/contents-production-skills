# Alternate-context supplementary run

Date: 2026-10-16. The repository block file `_blocks.json` contains 60 request blocks; this run answered all 60 exactly once. Raw responses are in `alternate-post-arm-results.json`.

## Method

Each frozen request was sent to `completion(model="slow")` as a fresh call with the relevant current repository skill/module text injected as read-only context. No tools were available to the completion calls, so no repo/provider side effects were possible. Responses were retained verbatim with their block IDs.

## Interpretation

This is **not** the formal frozen Codex arm: model/runtime, tool availability, and context-loading method differ. Do not compare its outcomes numerically with `baseline-results.md`, treat it as a valid before/after score, or infer a 95% score. It is exploratory coverage only. The scoring block itself declined PASS/FAIL because the row responses it needed were absent from the supplied scoring context; that is not a score for the 60 responses.

There is also a corpus-count discrepancy to resolve before formal scoring: `baseline-matrix.md` says 59 exact prompt blocks, whereas `_blocks.json` contains 60 keys, including `VS-1`, `VO-1`, and `Scoring`. The project’s earlier status describes a 61-case arm. This alternate run therefore reports its observed count (60), not the claimed formal-arm count.

## Result artifact

- `alternate-post-arm-results.json`: 60 raw answers, keyed by exact `_blocks.json` IDs.
- No aggregate pass rate or skill score assigned. Formal scoring needs the frozen runner/session contract and reconciliation of the corpus count above.
