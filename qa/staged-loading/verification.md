# Staged loading / focus view verification

## State

**Isolated draft; not yet behaviorally accepted, merged or deployed.** Native implementation and local structural/regression checks are recorded below. The separate 56-probe host/model/budget gate is unapproved, so actual consumption, behavioral equivalence and end-to-end performance acceptance remain **blocked/unverified**. One authorized independent final code review is pending.

- Baseline: `bd5fb689dced7d09d966bff8f1897c06bac6082f`.
- Worktree: `/home/declan/.cache/pi-worktrees/contents-production-loading-20261118`.
- Branch: `feat/staged-skill-loading-20261118`.
- Source metrics: `before-after.json` contains the source commit and raw document fingerprints; metrics are not billing tokens.
- Scope: manifest's 25 skills; four non-manifest installed image/website specialists are untouched.
- No remote push, merge, installation, installed-skill sync/repoint, model/provider operation, upload, media production or publication was performed. Local tests create synthetic fixtures only.

## Evidence

| Check | Observed result |
|---|---|
| Baseline complete suite | 1048 passed, 4 skipped, 533 subtests |
| Candidate complete suite, before final review | 1113 passed, 4 skipped, 533 subtests (68.64s) |
| Skip reason | Four Windows junction cases in `recording-production-history/scripts/test_layout_review_regressions.py:77`; host is not Windows |
| Version check | package 2.54, 25 consistent skills; IDs/versions unchanged |
| Whitespace | `git diff --check` clean |
| Local Markdown links/fragments | 217 managed documents, 866 local links, 0 unresolved; baseline 205 documents/0 unresolved. External URLs were not fetched. See `link-check.json` |
| Migration | Legacy fragments resolve; source rule lines retained once across stage owners. Formatting separators and moved self-links are normalized; explicit cross-reference/save-axis edits are enumerated in `rule-edits.json` |
| Focus seam | Default/full equality, input immutability, first/last/multiple/repeated cuts, explicit history closure/cycle, broad global owners, master/LOOK/voice/native lineage, scope mismatch, same-read hashes and execution-consumer rejection tested |
| Large explicit history | All 83 selected/history/context cuts retained; no arbitrary token cap |
| Offline counter | Portable aggregation tests; real tokenizer reads one verified cached rank snapshot and never calls a download-capable registry. All 8 frozen baseline profile totals reproduced exactly |

Full suite command (existing tokenizer cache is **read only**):

```sh
TMPDIR=$HOME/.cache TIKTOKEN_CACHE_DIR=/tmp/data-gym-cache python3 -m pytest -q -rs
python3 scripts/check_versions.py
git diff --check
```

Task RED/GREEN outputs, the SHA-verified baseline snapshot, and the read-only local-link checker are retained in `.superpowers/sdd/2026-11-18-staged-skill-loading-focus-view/`. No substantial test output is written under `/tmp`.

## Static reference-token measurements

`o200k_base`, fixed named **non-recursive file unions**, not actual agent traces:

| Profile | Before | After | Change |
|---|---:|---:|---:|
| Single lighting | 22,538 | 11,598 | −48.540% |
| Ordinary full text board | 25,058 | 18,791 | −25.010% |
| Text board with common handoff | 33,087 | 19,948 | −39.710% |
| Logline | 8,896 | 9,166 | +3.035% |
| New fictional character, both lenses (appearance catalog still required) | 19,022 | 19,294 | +1.430% |

The two slight static regressions are explicitly reported, not hidden in an aggregate. Shared scope/evidence policy grew. Fixed-appearance compact work skips the appearance catalog; actual design/variation still loads it. Some entrypoints remain above the aspirational ~1800-token size; functionality/safety take precedence over blanket shrinking.

`focus-scaling.json` records the **incomplete synthetic skeleton**, not valid completed production footage: 100-shot full projection 44,322 → focus 2,288 tokens; unchanged focus output from 10→100 shots. A two-shot display has overhead: 1,776 full vs 1,817 focus. The actual image-backed native handoff fixture is tested separately; no production speed or billed-token reduction is claimed.

## Remaining gates

- **0/56 behavioral probes run.** Need separate host/model/budget approval before the frozen cases can measure actual returned text, duplicate reads, questions, output completeness and fail-closed behavior. No filenames/answer-owner expectations may be injected into probe prompts. Single structural passes do not establish behavior.
- Independent final review and one bounded RED→GREEN fix pass are pending; its result will be recorded here.
- External `ai-delegation-loop` remains a declared, scoped unresolved dependency where needed; it was not installed, removed or substituted.
- Merge/push and installed-skill deployment/repoint remain separately unapproved.
