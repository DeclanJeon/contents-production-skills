# Staged loading / focus view verification

## State

**Behavioral acceptance remains unverified; no main merge.** The later user-authorized feature push/current-Pi installation is documented in [deployment-current-pi.md](deployment-current-pi.md). Native verification below records the pre-deployment checkpoint. Native implementation and local structural/regression checks are recorded below. The separate 56-probe host/model/budget gate is unapproved, so actual consumption, behavioral equivalence and end-to-end performance acceptance remain **blocked/unverified**. One authorized independent review found two P1 omissions. They and a structured-error issue regraded Important were corrected in one RED→GREEN fix pass. The reviewer was not re-run; behavioral acceptance remains blocked.

- Baseline: `bd5fb689dced7d09d966bff8f1897c06bac6082f`.
- Worktree: `/home/declan/.cache/pi-worktrees/contents-production-loading-20261118`.
- Branch: `feat/staged-skill-loading-20261118`.
- Source metrics: `before-after.json` contains the source commit and raw document fingerprints; metrics are not billing tokens.
- Scope: manifest's 25 skills; four non-manifest installed image/website specialists are untouched.
- At the native verification checkpoint, no push, merge or installation had been performed. A later explicit user request authorized the feature push/current-Pi installation linked above. No media-provider execution, upload, production media creation or publication was performed; tests use synthetic fixtures.

## Evidence

| Check | Observed result |
|---|---|
| Baseline complete suite | 1048 passed, 4 skipped, 533 subtests |
| Candidate suite before review | 1113 passed, 4 skipped, 533 subtests (68.64s) |
| Candidate full suite after review fixes | **1121 passed, 4 skipped, 533 subtests (64.68s)**; `PYTHONDONTWRITEBYTECODE=1`, home TMPDIR, pytest `-p no:cacheprovider` |
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
- [Independent final review](independent-review.md): read-only source review, not an agent behavioral probe or provider test. Fix commit `dad0670ea405f870db2a009af490346525a2c4dd` preserves selected link/requirement checks and evidence, explicit native-adapter/schema records/pins, and JSON errors for malformed stored scopes. Eight new regression cases failed before the corresponding fixes and passed afterward; the full suite passed. No second review was dispatched.
- **Deferred minor:** the copied `docs/analysis/2026-11-18-skills-weight-audit/REPORT.md` is only a partial frozen audit snapshot. Its original audit scripts and some linked results were not copied; those historical reproduction commands do not run from this branch. Current implementation evidence is this QA directory and `scripts/skill_loading_metrics.py`; do not treat the old audit report as a complete portable reproduction bundle.
- External `ai-delegation-loop` remains a declared, scoped unresolved dependency where needed; it was not installed, removed or substituted.
- The later explicit user request authorized feature-branch push and current Pi deployment only. Main merge and 56-probe model/budget approval remain absent.

## Decisions and retained limitations

- The home-cache worktree protects dirty main. Local checkpoints omit the auto-sync post-commit hook; the later explicit deployment repoints Pi only. Other agents remain on the original checkout.
- Native/static-first work follows the approved plan; behavioral probes await their own budget. Structural line preservation and explicit edit receipts do not establish semantic acceptance.
- Private view-record closure is separated into `sequence_view_records.py`; optional deep-reference discovery uses `module-index.md`. Tradeoff: an extra private module and potentially one niche index read, whose actual overhead is unmeasured.
- The reference encoder constructs from pinned verified local ranks/pattern, not a download registry. Tradeoff: maintaining that fixed reference definition; all eight old totals were reproduced. This is not host billing.
- Stored-scope traceback was regraded Important because it breaks machine-readable errors; fixed with eight total new review regressions across the three accepted issues.
- Reviewer declined actual behavior, live-provider validity, real media/contact/listening/PDF/approval, universal scaling/latency and deep-reference discoverability: these remain explicitly unverified, not silently accepted.
- Reported static regressions and >1800-token entries are retained rather than deleting required content. Alternate trace-host adapters, the four non-manifest skills, original dirty routing files, pre-existing execution/index limitations and new caching/scheduling architecture remain outside scope; no claim is made for them.
- Audit reproduction remains the one deferred minor above. Its original tool bundle is not included here.
- The worktree is retained as Pi's active skill source; do not remove it. Deployment is explicitly recorded separately, without asserting behavioral acceptance or all-gates completion.
