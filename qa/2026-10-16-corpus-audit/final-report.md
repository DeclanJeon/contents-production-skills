# Corpus audit, QA and remediation: final report

Date 2026-10-16. Repo `C:/Users/Declan/Documents/Projects/Skills-and-Automation/contents-production-skills`, HEAD `fed9275`. Nothing was committed, pushed, or installed globally.

## 1. Files produced (all in `qa/2026-10-16-corpus-audit/`)

| File | Role |
|---|---|
| `CONTRACT.md` | frozen scope, definitions, metrics |
| `worklists/` | per-slice worklists |
| `extracts/` (7) | first-hand book extracts with `#L` anchors |
| `extract-reconciliation.md` | Axis 1 and Axis 2 reconciliation |
| `inventory.md` | skill inventory, bytes, ref counts |
| `corpus-ledger.tsv` | all 1086 book-file rows with read state |
| `coverage-ledger.md` | book-to-skill coverage, crosswalk |
| `book-coverage.md` | denominator chain, §8 crosswalk |
| `owner-gap-verification.md` | named-owner gap audit |
| `unassigned-triage.md` | unassigned-row disposition |
| `planned-patches.md` | P1-P7 patch plan with corrected anchors |
| `baseline-prompts.md`, `baseline-prompts-exact.md` | frozen prompt bytes |
| `baseline-matrix.md`, `baseline-matrix-vpa.md` | per-ID assertions |
| `prompts.sha256` | frozen-byte manifest (verified MATCH) |
| `baseline-results.md` | 61 scored baseline rows |
| `post-results.md` | 61 post-change rows, same bytes |
| `rubric-definition.md`, `rubric-skeleton.md`, `rubric.md` | fixed 0-5 rubric and the 24-skill scorecard |
| `peer-remediation-verification.md` | anchor-by-anchor verification of the peer edits |
| `optimization-candidates.md` | reduction candidates with byte impact |
| `gate-status.md` | gate/sequence record |
| `concurrent-tree-state.txt` | tree-freeze evidence |

## 2. Book coverage

| Metric | Value |
|---|---|
| (A) all `.md` under `E:\Book\06_Book` | **1559** |
| (B) actual book-text `.md` | **1086** |
| Exact-byte duplicate groups / files | 326 / 652 |
| Unique by hash | 760 |
| Folder candidates content-verified | 217 = 202 BOOK / 11 SUSPECT / 4 STUB |
| Worklist paths | 213 |
| Title-keys | 135 |
| Slice-work incidences | 120 |
| **Globally distinct works (denominator)** | **118** |
| w3 slice | 55 works, 63 principles, 64 entries |
| Unassigned rows | 873 -> 749 -> ~547 |
| Read state | READ-PARTIAL **377** / UNREAD **709** (zero READ-FULL) |
| Body scan of all 1086 | 1077 BODY / 9 HEADERONLY (+2 in the Pyramid Principle pair) |
| Craft-keyword density screen (706 unread) | median 0.114/1k, p90 0.668/1k, max 8.384/1k; no hidden unread craft book |
| Provenance census | 19 of 154 reference files carry a provenance heading |

Every unread row is explicitly UNREAD in `corpus-ledger.tsv`. Never report 213 as works; the work count is 118.

## 3. Herdr agents

| Pane | Role | End state |
|---|---|---|
| `w1:p12` | audit leader (this session), tab `w1:t12` | self, 816 |
| `w1:pC` | single remediation writer | `working` 705 -> **`idle` 835** (gate opened) |
| `w1:p15`..`w1:p18` | dispatch panes (labeled for the arm) | idle, cwd = repo |
| others | `w1:p8` blocked, `w1:p0` opencode, etc. | idle/blocked, untouched |

## 4. Skill scorecard (24 skills)

Full detail in `rubric.md`. Distribution: **0 x 5, 9 x 4, 13 x 3, 2 x 2, 0 x 1, 0 x 0.**

- No 5 is reachable: anchors 5 needs every craft claim source-cited with read scope **and** an exercised verification record; only 19/154 refs carry provenance and no work is READ-FULL.
- 4 (gated): creative-production, video-production-assets, orchestrating-video-preproduction, developing-video-synopses, designing-video-character-sheets, designing-character-personas, storyboarding-video, higgsfield-brandkit, higgsfield-youtube-thumbnail.
- 2 (too thin to gate): camera-motion-reference-analysis, blender-previsualization.
- `dup:` pairs flagged once: SSOT/single-writer (creative-production, video-production-assets); 3D spec + Blender (camera-spatial-design, blender-previsualization); board contract (storyboarding-video, higgsfield-video-replicate).

## 5. Change list (`w1:pC`, 43 tracked files, all verified)

`git status --porcelain` = 43 modified/deleted tracked files plus the untracked audit dir. Forward additions and one deletion; `git diff --numstat` recorded. Every corrected anchor is used (`peer-remediation-verification.md`):

- `video-production-assets/references/12-qa.md`: excerpt-level scope replaces the "전체 읽기 가능한 자료의 통합" overstatement.
- `video-production-assets/references/16-concept-emotion-retention.md`: adds `## 근거와 적용 범위` and the Lazarus evaluation spot-check (자료 42).
- `video-production-assets/references/07-lighting.md`: Alton indicator-only wording (자료 02, L187-189), "prefigure" dropped.
- `video-production-assets/references/22-dialogue-lipsync.md`: Habermas congruence as context-sensitive, not a universal rule (자료 24, L351-359).
- `video-production-assets/references/10-evidence.md`, `08-animation.md`, `23-finishing-platform.md`: data-story subject/goal/opposition, motion-graphics surface, finishing/grading additions.
- `video-production-assets/references/13-ideation-brand.md`: states the segmentation-method gap (자료 44, Kotler L16831-16839).
- `video-production-assets/references/sources.md`: IDs 41-44 with corrected OCR lines, Alton/Habermas/Lo Duca rows corrected, SHA-256 per rendition.
- `creative-production/references/marketing-source-adaptation.md`, `production-routing-optional.md`: Dunford positioning relative to buyer alternatives (source 43, L1135-1140) plus the structured ad-variation section and the Higgsfield MCP preset inventory.
- `creative-production/references/creative-qa.md`, `community-shorts-stills-pipeline/{SKILL.md,references/pipeline-stages.md,references/server-operation.md}`, `higgsfield-video-explainer/{SKILL.md,references/prompts.md}`: the remaining forward additions.
- **Boundary patch 2.9** (`creative-production/SKILL.md` 1.4, `video-production-assets/SKILL.md` 1.3): the read-only/no-generation clause.
- Plus all 24 `SKILL.md` version fields in lockstep, `CHANGELOG.md`, `README.md`, `manifest.json`.
- **Deleted by this audit:** `creative-production/references/shot-manifest.md` (-2137 B).

## 6. Executed QA evidence

| Check | Result |
|---|---|
| `prompts.sha256` re-verified after the peer edits | **MATCH** (4/4) |
| `scripts/check_versions.py` | `version check OK: package 2.8, 24 skill(s) consistent` |
| pytest pre-gate (`pytest-omp-cps5`) | 254 passed, 8 skipped, 214 subtests passed |
| pytest post-gate (`pytest-omp-cps6`) | 254 passed, 8 skipped, 214 subtests passed (no regression) |
| Relative links (all skills, 366 links) | **0 broken** |
| Baseline arm (61 frozen prompts, `codex exec --sandbox read-only`) | PASS 44, PASS* 12, FAIL 4, UNSCORED 1 |
| Post arm (same 61 bytes, fresh sessions) | **PARTIAL: 25/61 executed.** PASS 17, PASS* 5, FAIL 2, UNSCORED 1; remaining 36 blocked by the provider usage limit (reset 10:16) |
| Boundary patch 2.9 applied by `w1:pC` (boundary clause in `creative-production` 1.4 and `video-production-assets` 1.3, all 24 skills lockstep) | `check_versions.py` OK at 2.9; `prompts.sha256` still MATCH (4/4, bytes frozen). Fresh `M-04`/`M-09` replays scheduled with the 36 blocked rows |
| Post-gate pytest, after the shot-manifest deletion (`pytest-omp-cps7`) | 254 passed, 8 skipped, 214 subtests passed |
| Pytest at package 2.9, after the boundary patch (`pytest-omp-cps8`) | 254 passed, 8 skipped, 214 subtests passed |

Baseline arm scores (`baseline-results.md`); sources of the FAILs:

| ID | Behavior |
|---|---|
| M-04, M-09 | generated a still image inside a read-only probe (image-route ambiguity) |
| S1a | provenance probe returned a two-line summary, not the asked-for table with a quoted separating sentence |
| S1b | emotion/retention probe carried no file+section locator and zero `[BASIS-UNSTATED]` marks |
| M-03 | session could not read the tree; no basis invented (UNSCORED) |
| M-08, M-15, V-05, V-06, V-10, V-12, V-16, V-21, V-23, VP-1, VP-2, VS-1 | boundary behavior correct, but the read-only shell setup failed so locators could not be exercised (PASS*) |

## 7. Optimization candidates

| Candidate | Verdict | Byte impact |
|---|---|---|
| `creative-production/references/shot-manifest.md` | **DELETED** (applied after the baseline arm and before the post arm): 2137 B, 0 live inbound links; only self-reference, an internal plan doc, and a generated analysis json mention it; its own body says it is not a file to maintain | -2137 B |
| `workspace-integration.md` triplication | **REJECTED**: install copies each skill as its own tree, so each copy is needed | 0 |
| `support/` duplication | **REJECTED**: git-ignored generated build output | 0 |
| large `SKILL.md` token burden | measure only: video-production-assets 22261 B, higgsfield-websites 16929 B + 652849 B refs | 0 |
| **read-only arm not defended against a later clause** | **APPLIED by `w1:pC` (2.9)**: clause landed in `creative-production/SKILL.md` (1.4, 200 B) and `video-production-assets/SKILL.md` (1.3, 202 B); replay verification of `M-04`/`M-09` pending with the 36 blocked rows | +402 B |

## 8b. Unfinished work and why

- The post arm ran 25 of 61 rows. The other 36 (`V-02`..`V-28`, `VC-1`..`VC-3`, `VP-1`, `VP-2`, `VS-1`, `VO-1`, `S1a`, `S1b`) were blocked by an external account quota: `ERROR: You've hit your usage limit ... try again at 10:16 AM` (post arm reached that at roughly 06:36 KST; a single immediate retry of `V-02` reproduced the same `rc 1` with empty stdout, so it is not transient). No amount of in-package work can clear it.
- The unmeasured result that matters most is the post-change delta on the provenance probes `S1a`/`S1b`. Re-run those and the other 35 after the reset with the same harness and score against `baseline-results.md`.
- **Boundary replay required:** the 25 pre-patch post rows predate the 2.9 clause and cannot verify it. `M-04` and `M-09` were cleared and are re-run fresh against 2.9 with the 36 blocked rows at the 10:20 reset (`_finish_post_arm.py`, PID 20328). Their verdicts, together with the `S1a`/`S1b` provenance delta, are the last two open results; both arrive automatically.
- Candidate 5 is applied by `w1:pC` (2.9), not by this audit; this audit applied only the verified-safe deletion.

## 8. Unverified limits

- Zero works are READ-FULL; all citations are READ-PARTIAL (excerpt scan).
- Eleven extraction-failure stubs remain UNREAD (Malkiewicz *Film Lighting* is the only craft-relevant one).
- C 18 KEEP-READ rows are contextual only; memoir-derived findings are marked contextual unless the book states direct film/video applicability.
- Subagent delegation (task/orchestrator/scout/worker) is blocked by `[openai-codex/gpt-6-luna] getaddrinfo ENOTFOUND chatgpt.com`; all reads were done with the leader's own tools.
- `codex exec`'s in-session shell is unavailable, which limits 12 IDs to PASS* (boundary correct, locator not exercisable).
- Provenance census is 19/154 reference files.
- Book-to-owner crosswalks for three skills remain `[INFERENCE]`.
