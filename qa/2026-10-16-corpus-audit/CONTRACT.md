# Corpus classification contract (2026-10-16)

Authority for every worker in this audit. Do not re-derive; read and apply.

## 1. Two separate metrics (never conflated)

- **(A) ALL `.md` files under `E:\Book\06_Book` = 1559**, measured `2026-10-16` by `find E:\Book\06_Book -type f -name '*.md' | wc -l`.
- **(B) BOOK-TEXT `.md` files = 1086**, i.e. (A) minus material that is not book text:

| Excluded from (B) | Count |
|---|---|
| `node_modules/**`, dependency docs (READMEs, package docs) | 452 |
| `_projects/**` + `**/.worktrees/**`, generated repositories | 16 |
| `.omx/**`, hidden cache state | 3 |
| `소설/md/무직전생/실행계획.md`, `작업지시서.md`, work orders | 2 |
| `스토리텔링/md/영상_프롬프트_제조_웹사이트_설계서.md`, design doc | 1 |

**The 1559 and the intermediate 1213 are NOT book counts.** They include generated repos and dependency docs. Only (B)=1086 is the book-text denominator.

## 2. Verification before relevance (bodies, not folder names)

Every candidate was opened and measured (bytes, line count, heading count, word count). 217 candidates → **202 BOOK / 11 SUSPECT / 4 STUB-NOT-BOOK**.
* **4 stub/empty files excluded** (0-29 words): `originals/콘텐츠_제작/md/Film Lighting Talks…`, `콘티_스토리보드/md/프레임드 잉크…`, `originals/마케팅/md/How Brands Grow Part 2…`, `originals/사고·글쓰기/The Pyramid Principle…` (truncated, 29 words).
* An empty/stub file is **not a book** and never counts as corpus evidence.

A library-folder name is not evidence of relevance. Candidate relevance was decided by (i) category directory, (ii) title keyword screen across all 792 non-novel books, and (iii) body verification. 506 of 792 non-novel books carried no craft keyword in title; those were reviewed by category before exclusion (e.g. 60 애착·연애·부부, 58 비즈니스·기업가, 50 갈등·경계·가족, 50 인간관계, 40 우정, relationship/psychology titles, no production craft).

## 3. Duplicate handling (recorded separately, never counted as works)

- `originals/<X>/…` mirrors `<X>/…`: **13 titles** (mirror duplicates).
- Exact-content duplicate groups over full bytes: **326 groups / 652 files**.
- `epub/` + `md/` + `pdf/` copies of one book are editions of one work.
- **Unique book works after content-hash dedup: 1073.**

## 4. Assigned reading set (213 paths/entries; not 213 works)

Worklists are the authoritative file lists: `worklists/w{1,2,3,4}.txt`. Every path in them was confirmed to exist on disk. The 213 figure is **assigned paths (worklist entries)**, NOT distinct works; rendition pairs and 2 cross-slice overlaps are present inside it. The verified distinct-work denominator is derived separately in §4b from the work-identity tables.

| Worker | Assigned paths | Domains |
|---|---|---|
| `w1-story` | 53 | `콘텐츠_제작`, `스토리텔링`, `시놉시스` |
| `w2-craft` | 16 | `콘티_스토리보드`, `애니메이션`, `문학·영화` |
| `w3-market` | 132 | `마케팅`, `광고_상세페이지`, `SNS`, `디자인`, `사고·글쓰기` |
| `w4-emotion` | 12 | `감정구조` (affective science) |
| not assigned (see `unassigned-triage.md`) | 873 files → ~253 distinct non-fiction works + 294 novel-corpus | Inventory, not an exclusion. Every unassigned work carries a verdict: **KEEP-READ** (craft works wrongly dropped, incl. `음악·방송`/`예술·문화`/`문학·영화` memoirs and `콘텐츠_제작`/`콘티`/`시놉시스` craft), **ADJACENT** (subject matter for content research, not film craft), or **EXCLUDE** (stated reason, reversible) |

**Scope correction (2026-10-16):** the earlier row "not assigned | 860" was an unauthorized reduction that folded two whole folders into a "low tier" without a body check and mixed file counts with work counts. It is replaced by `unassigned-triage.md`, which inventories all 873 unassigned files, records a body-level verdict per domain, and keeps every craft-relevant or adjacent-uncertain work for reading. Nothing is dropped silently; exclusions are listed with their reason.

An earlier draft worklist included personality-type titles (`MBTI*`, `애니어그램*`) because a title keyword matched "personality". Those are not production-craft books and are **excluded**; the worklists were rebuilt from the verified DIRECT+ADJACENT category sets and the stale files deleted.

**Filename rule:** workers must read paths exactly as written in the worklist. An ENOENT is reported for that canonical line only; a guessed or abbreviated filename failing is a worker error, not a corpus-access failure.

## 5. Read-completion states (recorded per book, never conflated)

- `READ-FULL`, entire body traversed.
- `READ-PARTIAL`, named chapters/sections only; ranges listed.
- `UNREAD`, no body read. **Any rubric influence of an unread book MUST be reported as `unverified`.**
- An unread/extract-only book MUST NOT be cited as support for a change. Inference from it is marked `[INFERENCE]`.
- Reading 233 works of ~500 MB cannot be done exhaustively; workers MUST record which titles they opened and which they did not, and the scorecard must keep unread ones `unverified`.

## 6. Extraction rules

- Generalized principles only, each with `file path + chapter/section` evidence. Never copy whole books, long verbatim passages, or licensed content into a skill.
- One principle = one falsifiable statement + its source + which existing skill reference already covers it (or `none`).
- Report a *coverage gap* only when the principle is absent from all existing references; report *duplication* when two owners state it.

## 7. Worker boundaries (single writer per path)

| Worker | Role | Owns (write) | Must not touch |
|---|---|---|---|
| `w1-story` | story/screenwriting/authorship reading | `extracts/w1-*.md` | any `*/SKILL.md`, any skill reference |
| `w2-craft` | storyboard/animation/memoir reading | `extracts/w2-*.md` | same |
| `w3-market` | marketing/ads/audience reading | `extracts/w3-*.md` | same |
| `w4-emotion` | affective-science reading | `extracts/w4-*.md` | same |
| leader (this agent) | skill inventory, rubric scorecard, book-coverage ledger, all remediation | `inventory.md`, `rubric.md`, `book-coverage.md`, skill files | `extracts/*` while workers run |

Workers run from this tab's shell panes with `--no-focus`; the leader reviews, integrates, verifies, and never edits a file a worker owns.

## 4b. Correction, 213 paths ≠ 213 works (2026-10-16, recomputed 2026-10-16)

The 213 worklist entries are **assigned paths**, not works. Two distinct mechanisms reduce them, measured on the byte-identical worklists with title-key normalization (strip `.md`, strip `(z-library…)`, strip `(author|etc|edition)` suffix, collapse whitespace, lowercase):

1. **Title-key collapse** (same filename, different bytes): the same work stored as top-level and `originals/<X>/`, or `epub/`+`md/` copies. These share a normalized filename and collapse at the title-key step.
2. **Work-identity collapse** (different filename, same underlying work): cross-language translations and edition pairs, which title-key cannot see. Verified one-by-one in `extract-reconciliation.md` Axis 1 (exact author/title/edition in the file's own front matter), NOT by principle text.

| slice | paths | title-keys | same-filename rendition groups | work-identity groups (Axis 1) | slice-unique works |
|---|---|---|---|---|---|
| w1 | 53 | 37 | 16 | (none checked) | 37 |
| w2 | 16 | 16 | 0 | 0 | 16 |
| w3 | 132 | 72 | 51 | **17** (one is a 3-path group) | **55** |
| w4 | 12 | 12 | 0 | 0 | 12 |
| **sum (incidences)** | **213** | **137** | 67 | 17 | **120 slice-work incidences** |

The 120 is a **sum of per-slice work incidences**, not a global work count. Sum of per-slice title-keys is 137; the **union is 135** because **2 works** are verified to sit in two slices at once (`Film Directing Shot by Shot` / Katz in w1+w2; `쇼 유어 워크` / Kleon in w1+w3, both listed in `extract-reconciliation.md` §Cross-slice). Those 2 are counted twice in the 120 sum, so subtracting them gives the globally unique count:

**213 assigned paths → 135 union title-keys → 120 slice-work incidences → 118 globally distinct works** (37 + 16 + 55 + 12 − 2 overlaps). The coverage denominator is the **118 globally distinct works**, never the 120 incidences and never the 213 paths.

The earlier "136 title-keys → 16 pairs → ≈119 works" wording **is withdrawn**: it used a 16-row pair table that omitted the Cialdini *Influence* edition pair, so w3 has **17** work-identity groups, not 16; and it described path counts with an implicit "minus pairs" subtraction (`136−17=119`) that mixed path and work units. The corrected denominator is derived from the work-identity tables, never from principle dedup. w3's 55 works == w3's title-keys (72) minus the 17 work-identity groups collapsed, which reconciles exactly with Axis 1's `73 paths → 18 collapsed → 55 works` (the 73 includes the two `컨테이저스` renditions that share one title-key).

Consequences:
- The reading set is **118 distinct works** over 213 assigned paths, and the coverage figure is reported as this derived count (range if any group stays `[UNCERTAIN]`), never as 213 or as the raw title-key total.
- Deduped lists: `worklists/w{1,2,3,4}-dedup.txt`; skipped paths: `worklists/w{N}-skipped-duplicates.txt`.
- Workers read one rendition per title; multiple renditions are counted **once** in coverage. **Distinct works, not paths, is the coverage denominator.**
