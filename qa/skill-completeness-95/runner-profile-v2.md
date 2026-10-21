# Local-owner evaluation profile v2

## Observed defect

The first narrowed OMP series successfully executed M-03, M-04 and S1a but the M-04 answer gave no package file/section locators and routed a later render via global `/3d-jutsu` rather than the package owners. The v1 caller passed only the frozen user block; it did not explicitly route the request to this checkout's owner. Successful process execution was therefore insufficient proof of local skill consumption. V1 artifacts remain preserved and UNREVIEWED; they are not reused in v2.

## Correction

- Frozen user prompts and four original frozen hash inputs are unchanged. `-p` still receives the exact manifest prompt bytes.
- New series `omp-readonly-local-owner-v2` supplies an **execution-profile system directive**, not source-file contents: the common read-only/hypothetical/one-turn/file+section rules already defined by the frozen corpus, plus the exact local owner/module path derived from its frozen assertion row.
- S1a/M-03 retain their expressly named file-only source scope; no extra skill is required by the harness for them. S1b starts at the package emotion/retention module. Other M cases load their local owner SKILL; module/group cases load their named reference.
- Profile is explicit-model, read/grep/glob only, no LSP/extensions/session persistence; no write/bash/provider executor tools. Raw argv includes the directive, and runner hash/profile/manifest/prompt/tree bind cache identity.
- Per-case model deadline is 180 seconds with process timeout 195 seconds. No automatic semantic PASS; independent assessment is still required.
- This changes execution context and is explicitly a new series, not a byte-equivalent historical Codex arm or evidence of a causal skill improvement over v1.

## Fingerprint scope correction

Observed full-root inventory: docs contained 10135 files / 2693401780 bytes, dominated by 2345 PNGs (2299457999 bytes) and 7354 JPGs (372797632 bytes). These historical screenshots are not media inputs to the 61 frozen text-only scenarios. The v1 full-root hasher reread them before/after each case.

V2 excludes only archival docs PNG/JPG/JPEG/GIF/WebP from instruction identity; code, root config, instructional docs text/JSON, all skill code/references/assets and example assets remain covered. QA evidence and VCS/cache exclusions remain. This is not a claim that archival media integrity was verified.

A new consumer-visible cache-boundary test failed before the correction: an unrelated archived frame changed the instruction fingerprint. It also asserts that changing docs/instructions.md changes the fingerprint. The existing test preserves mandatory skill-asset/root-config invalidation. Final suite and v2 critical-case outputs are recorded separately, not assumed here.
