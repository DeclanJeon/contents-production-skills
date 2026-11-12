# Writing evaluation — contained reference reading

## Scope

User-approved evaluation-tool improvement, not a new production skill or global MCP installation. Existing 22 owners, project fields, versions and fixture permissions stay unchanged. Candidate-3 runtime source remains frozen; tool/source behavior and writing quality have separate gates.

## Address contract

The existing `read` tool accepts:

1. A package-root source filename.
2. A literal local document href with explicit `relative_to` equal to the full package-root **containing document**, not a directory.
3. A source-derived `ref_` address copied from the `read_arguments` supplied with an actual returned source page.

Example of explicit document-relative reading:

```text
read(path="../../video-production-assets/references/writing-craft.md#grounding",
     relative_to="developing-video-synopses/references/synopsis-craft.md")
```

Original source bytes remain the primary content. Bounded companion reference metadata supplies copyable read arguments; the model need not calculate paths. Document hrefs and skill-relative inline `references/`, `assets/`, `scripts/` addresses use distinct deterministic rules. Unknown addresses do not trigger an existence-based fallback.

`find(query="A01", path="video-production-assets")` searches only the contained source scope. Legacy `find(path="A01")` retains its original query meaning. This does not promise the hypothetical A01 artifact exists, perform external search or register an artifact dependency.

## Boundaries and proof

- Shared resolver rejects external URLs, malformed percent escapes, root escapes, symlink components, excluded/non-runtime files and source/fixture confusion. URI decoding occurs once; fragments are local anchors, not permission to escape.
- Receipt verification correlates successful physical page delivery, immutable content hash, source-recomputed offered addresses, selection, controlled read and completion. A forged or unreturned-page offer is not evidence.
- References survive MCP process restart only from the same case's actually delivered successful pages after source/page/hash revalidation. Incomplete reads and changed sources cannot restore offers.
- A later correct call does not erase a prior failed call. Fixture writes still require explicit approval, ordered initial read → user insertion → fresh read → write, and exact final bytes.
- Historical frozen adapters/receipts stay unchanged. Legacy fixture normalization is explicitly projected; historical prototype handle evidence is not silently upgraded to newer proof.

Implementation: `scripts/writing_eval_source_paths.py`, `writing_eval_references.py`, `writing_eval_wire.py`, `writing_eval_codex_tools.py`, `writing_eval_codex_mcp.py`, `writing_eval_review.py` and native/batch integration.

## Observed verification

Current full host checks: **701 Python tests / 518 subtests**, **11 Node tests**, basedpyright **0 errors / 0 warnings**, package **2.33 / 22 skills**. Regression records preserve observed RED→GREEN for containment, page-proof/call correlation, forged offers, restart restoration and scoped-find ABI. Native probes preserve failures as well as actual successful reads; the restart probe's separator whitespace is disclosed rather than claimed as exact-format PASS.

V4–v8 were stopped, retained low-reasoning adapter epochs, not replaced samples. V9 separately declared matched high reasoning in both conditions, fresh controls, unchanged source/input/rubric and one archived 17-file adapter. All **140 runs / 170 stages** completed with valid evidence; all **10 fixtures** passed physical order/hash/final-byte checks. This demonstrates the observed evaluation tool contract under that profile, not general model reliability.

Writing verdict remains **FAIL**: baseline **55 PASS / 15 FAIL**, candidate **69 PASS / 1 FAIL**. Candidate/T05/r1 drops `이제` from a user-locked sentence. No adoption, release, global sync or Git integration follows from the tool checks. See [complete review and retained epochs](../../qa/matt-writing-integration-review.md).

Operational evidence (ignored, worktree-local): `.superpowers/sdd/2026-11-11-matt-pocock-writing-craft-integration/`, especially `codex-comparison-v9/final-host-evidence.json`, `final-reviewed-runs.json`, `final-aggregate.json`, `final-review-rulings.json`, independent review inputs/results and `v9-final-*` host logs. Reviewer judgments were checked against actual text; original mistakes and adjudications remain auditable.
