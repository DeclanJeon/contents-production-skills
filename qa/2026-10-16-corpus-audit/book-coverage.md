# Book corpus coverage (leader, 2026-10-16, read-only phase)

All numbers below are measured this audit on `E:\Book\06_Book`. No number is inherited from a prior session's claim without re-measurement.

## 1. Two metrics, kept separate

| Metric | Value | How measured |
|---|---|---|
| **A. all `.md` files under `E:\Book\06_Book`** | **1559** | `find /e/Book/06_Book -type f -name '*.md' \| wc -l` |
| Excluded: `node_modules/**` | 452 | generated dependency docs |
| Excluded: `_projects/**` + `.worktrees/**` | 16 | source repos |
| Excluded: `.omx/**` | 3 | generated |
| Excluded: non-book docs | 3 | `소설/md/무직전생/실행계획.md`, `소설/md/무직전생/작업지시서.md`, `스토리텔링/md/영상_프롬프트_제조_웹사이트_설계서.md` |
| **B. actual book-text `.md`** | **1086** | A minus exclusions |

(A) and (B) are **not** book counts of distinct works. (B) is a file count.

## 2. Distinct works

| Step | Value |
|---|---|
| (B) book-text `.md` files | 1086 |
| minus exact-content duplicates (byte-identical, blake2b-16) | −326 groups / −652 files |
| **unique works after byte-hash dedup** | **1073** |
| of which narrative corpus `소설/**` (evidence-only, not craft books) | 294 |
| of which other | 792 |
| non-novel with a production-relevant title keyword | 286 |

**Rendition caveat (new, measured this audit):** byte-hash dedup under-counts duplicates because the corpus stores the *same work* as several renditions (top-level vs `originals/<X>/`, plus `epub/`, `md/`, `pdf/` subfolders) whose OCR line-wrapping differs. The 1073 figure is therefore an **upper bound** on distinct works. The reading set alone shows the effect: 213 assigned paths → **118 distinct works** (see `CONTRACT.md` §4b).

## 3. Body verification (no title-only or folder-only classification)

| Check | Value |
|---|---|
| zero-byte book files | 0 |
| stub files `<2 KB` | 13 |
| folder-derived candidates opened and content-checked | 217 → 202 BOOK / 11 SUSPECT / **4 STUB/NOT-BOOK** |

The four not-a-book files, named explicitly (never silently dropped):
1. `originals/콘텐츠_제작/md/Film Lighting Talks with Hollywoods Cinematographers and Gaffers (Kris Malkiewicz) ….md`, 0-29 words. Note: `video-production-assets/references/sources.md` independently records this book as **"본문 없음" (no body) and excluded**, the two findings agree.
2. `콘티_스토리보드/md/프레임드 잉크 - 마르코스 마테우-메스트레.md`
3. `originals/마케팅/md/How Brands Grow Part 2 … (Jenni Romaniuk, Byron Sharp) ….md`
4. `originals/사고·글쓰기/The Pyramid Principle … (Barbara Minto) ….md`

## 4. Reading coverage

Priority reading set: **118 distinct works** (213 assigned paths), split w1 37 / w2 16 / w3 55 / w4 12, after collapsing 67 same-filename title-key groups and 17 w3 work-identity groups (see `CONTRACT.md` §4b).

This slice is driven by **craft relevance** (story, screenwriting, storyboard, editing, lighting, performance, animation, direction, camera, marketing/audience, emotion theory), not folder names. Personality-type titles (`MBTI*`, `애니어그램*`) are excluded as non-craft; `소설/**` is a narrative corpus usable only as extra evidence for a principle already established from a craft book.

**Read state vocabulary:** `READ-FULL` | `READ-PARTIAL` | `UNREAD`. **Any unread item is `unverified` and may not carry a rubric score.** Worker extracts live in `extracts/`.

### 4b. Whole-corpus read campaign (this phase, non-gated)
Beyond the 118-work priority set, the leader opened **every all-UNREAD DIRECT and ADJACENT group** in `corpus-ledger.tsv`:
- **DIRECT:** all 83 works now carry a bounded window; 81 `READ-PARTIAL` (group-level) with a first-hand `#L` anchor (`extracts/leader-video-craft-evidence.md` §E: Murch x2, Reisz/Millar, Alton, Block, Lumet, Williams, Field, Snyder, Campbell, Yorke, Ondaatje, Pearlman, Stanchfield, Weston, Kenworthy, Culhane, Katz, Hooks, Hu, Cristiano x2, Paez, Ramocki, Parr, McKee, Truby, Nash, Vogler and the earlier craft-core rows). 2 groups stay `UNREAD` (zero-body stubs).
- **ADJACENT:** 132 of 134 groups `READ-PARTIAL` (39 previously all-UNREAD groups opened; §F records the 4 craft-relevant ones and the header-level EXCLUDE categories for the rest). 2 groups stay `UNREAD` (zero-body stubs).
- **Read-state totals:** 377 `READ-PARTIAL` / 709 `UNREAD` across the 1086 file rows. The residual `UNREAD` set is exactly: 11 extraction-failure stubs, 294 CORPUS fiction files (source stories, no owner), and 408 EXCLUDED files (typology / relationship / software, no craft owner).

### 4c. Extraction failures (11 files)
A whole-corpus scan flagged 11 Markdown files that carry only a title plus a `> Source:` line and no body: `Framed Ink` 254 B; `영화 조명` KO + `Film Lighting Talks` EN 406 B; `The Pyramid Principle` EN + KO 256 B; `How Brands Grow Part 2` EN + KO 508 B; `Gifts Differing` 1024 B; `Please Understand Me` 860 B; `Personality Plus` 804 B; `The Enneagram Made Easy` 700 B. All stay `UNREAD`. `Film Lighting` (Malkiewicz) is the only craft-relevant one; the KO file is the one named in the earlier handoff.


### w2 resolution (this phase)
w2's direct craft set (the 7 works that were UNREAD: Katz *Shot by Shot*, Paez *Professional Storyboarding*, Hu *Mastering Storyboarding*, Cristiano *Storyboard Design Course*, Cristiano *The Storyboard Artist*, Parr *Sketching for Animation*, Ramocki *Essentials of Creativity*) is **now READ-PARTIAL**, recovered by the leader after `w1:p16` reported tooling failure (`helper_unknown_error`; no file written). Evidence: `extracts/w2-craft-extract.md` (0 FULL, 7 READ-PARTIAL, every row anchored). The 9 w2 memoirs stay READ-PARTIAL. **No w2 craft work is wholly UNREAD**, so no w2-backed row is blocked by absence of a read. w2 still has **0 READ-FULL**; all w2 rows are partial.

## 5. Package's own prior basis

`video-production-assets/references/sources.md` records a **40-book excerpt-level pass** (36 + 4 added), each mapped to a concept and an OCR line position, feeding references 01-11 and 13 only.

- That pass is **partial by its own statement** ("전권 정독…을 완료했다는 뜻이 아니다").
- 01 excluded (no body); 03, 06, 34 OCR-damaged with only clean spans used.
- References **14-28** carry no book provenance row at all (see `inventory.md` §B2).

## 6. What is claimed and what is not

**Claimed:** (A)=1559, (B)=1086, byte-dup 326 groups/652 files, 1073 upper bound, 213 assigned paths = 118 globally distinct works, 217 candidates → 202/11/4, the four stub paths, and that 40 books were previously used at excerpt level for refs 01-13.

**Not claimed:** that any of the 118 priority works were fully read this audit before its extract exists; that the package has absorbed the corpus; that the four stubs zero out the `Film Lighting` concept (the concept may exist in another rendition, not yet checked).

## 7. Translation / edition pairs: the verified work denominator

w3 holds both the English original and the Korean translation of the same book. Title-key dedup cannot see these (the parenthetical only carries the author), so the title-key total is an upper bound. The 17 same-work groups are verified in `extract-reconciliation.md` Axis 1 (author/title/edition from each file's own front matter), not by principle text:

| English original | Korean translation | note |
|---|---|---|
| Made to Stick (Chip Heath) | 스틱! - 칩 히스 | 4 renditions on disk |
| The 22 Immutable Laws of Branding (Ries) | 브랜딩 불변의 법칙 22 | |
| The Art of Profitability (Slywotzky) | 수익의 기술 | |
| The Conversion Code (Chris Smith) | 전환 코드 | |
| Subscribed (Tzuo) | 구독 경제 | |
| Why We Buy (Underhill) | 우리는 왜 사는가 | |
| Tribal Knowledge (John Moore) | 트라이벌 날리지 | |
| The Tipping Point (Gladwell) | 티핑 포인트 | |
| The Zero Marginal Cost Society (Rifkin) | 한계비용 제로 사회 | |
| Principles of Marketing (Kotler/Armstrong) | 마케팅 원론 | |
| SPIN Selling (Rackham) | SPIN 세일즈 | |
| Building a StoryBrand 2.0 (Miller) | 스토리브랜드 만들기 2.0 | |
| Obviously Awesome (Dunford) | 오비어슬리 어썸 | 3 renditions |
| The Black Swan (Taleb) | 블랙 스완 | also `黑天鹅` Chinese rendition |
| Contagious (Berger) | 컨테이저스 | two Korean renditions |
| The Design of Everyday Things (Norman) | (none; EN only) | two English renditions (Norman / Don Norman) |
| Influence (Cialdini) | (none; EN only) | original + "New and Expanded" edition = one work |

> 17 work-identity groups total; the earlier 16-row table omitted the Cialdini *Influence* edition pair. Axis 1 in `extract-reconciliation.md` carries the same 17 groups.

Same-author **different-book** collisions that must NOT be merged: Al Ries holds 3 distinct books (Positioning, 22 Laws, Fall of Advertising); Kotler holds 2 (Principles of Marketing, Marketing 3.0); April Dunford's two rows *are* one book.

**So, verified: 213 assigned paths → 135 union title-keys → 120 slice-work incidences → 118 globally distinct works** (37+16+55+12−2 cross-slice overlaps; see `CONTRACT.md` §4b for the per-slice table and `extract-reconciliation.md` for the 17 groups). The `136 titles / 16 pairs / ≈119 works` figures are **withdrawn**: 136 was the w3 dedup-list key count, not the reading-set work count; the pair table had 16 rows because it omitted the Cialdini *Influence* edition pair; and `119` mixed path and work units. The coverage denominator for scoring is **distinct works**, reported as the derived 118 (or a range if any group stays `[UNCERTAIN]`), never 213, never the raw title-key total.

## 8. Proposed book → owner crosswalk (`[INFERENCE]` until extracts cite a line)

Mapping every distinct work to the package owner that should consume it. **No row is evidence until `extracts/` records a read state + location.**

| Corpus slice (works) | Domain | Candidate owner | Prior basis? |
|---|---|---|---|
| w1 screenwriting (McKee, Truby, Vogler, Snyder, Snyder-TV, Field, Yorke, Campbell, Block) | story structure | `video-production-assets/references/02-story.md`, `developing-video-synopses` | yes, `sources.md` IDs 17-36 |
| w1 visual/camera (Katz, Kenworthy ×2, Alton, Block) | shot design, lighting | `camera-spatial-design`, `ai-camera-control`, `video-production-assets/references/05`, `06` | partial, `sources.md` 01-11 |
| w1 editing (Murch ×2, Pearlman, Reisz/Millar) | rhythm, cut logic, sound | `video-production-assets/references/09-edit.md` | **yes**: `09-edit.md` exists (19902 B) and cites 자료 ID 04,09,10,11,12 = Lumet *Making Movies*, Pearlman *Cutting Rhythms*, Murch *In the Blink of an Eye*, Reisz/Millar *Technique of Film Editing*, Ondaatje *The Conversations* (sources.md rows 14,19,20,21,22). Earlier "no editing owner" claim was WRONG; corrected after inspection |
| w1 performance (Weston, Hooks, Hahn/Drawn to Life, Williams) | performance, animation | `designing-video-character-sheets`, `designing-character-personas` | **no** |
| w1 animation (Culhane, Williams, Blair) | animation craft | `storyboarding-video`, `video-production-assets/references/08-animation.md` | **no** |
| w1 emotion/narrative (Harbach [Habermas], Hogan-adjacent) | emotion design | `video-production-assets/references/16-concept-emotion-retention.md` | **no, this is the ref-16 gap**; Habermas *Emotion and Narrative* now read L241-253 (six recipient emotions, suspense vs empathy, knowledge-advantage lever, artefact vs fiction emotions) |
| w1 storytelling-for-business (Mason, Gupta, Ericson, Ursin, Bardi, Wiseman, Blazer, Cron/Lazarus, Karia, Moshowitz, Kleon) | narrative persuasion | `creative-production/references/marketing-source-adaptation.md` | **no** |
| w2 filmmaker memoirs (King, Kurosawa, Miyazaki, Lynch, Christie, Capote, Hemingway, Angelou, Kaplan-Twain) | craft-by-example | no owner; evidence-only per CONTRACT | n/a |
| w2 storyboard (Katz, Hu, Paez/Jew, Cristiano ×2, Parr, Ramocki) | storyboard craft | `storyboarding-video` | **no** |
| w3 marketing (55 works, incl. 17 same-work rendition groups) | audience/market | `topic-demand-selection`, `creative-production/references/marketing-source-adaptation.md` | **no** |
| w4 emotion science (Picard, Scherer, Lazarus, Gross, Meiselman, Davidson, Liu, Hogan, Combei) | emotion theory | `16-concept-emotion-retention.md` | **no**; Hogan (L974/1006/1064/2406) and Lazarus (L2342/3843/4319/5193) now read, both uncited |

## 8b. w4 works read this phase (evidence in `extracts/leader-emotion-evidence.md` and `extracts/w4-emotion.md`)

**Corrected: w4 is 12/12 READ-PARTIAL, 0 UNREAD, 0 READ-FULL.** The earlier "2/12" figure was stale (`w1:p18` completed a full 12-work section read at 04:54, `extracts/w4-emotion.md`, 15287 B, 12 principles). All 12 `감정구조` works were opened at named sections; the extract marks every OWNER/COVERAGE cell `unverified`, which `owner-gap-verification.md` §w4 now resolves with grep evidence.

| Work | Read state | Uncited craft available |
|---|---|---|
| Picard, *Affective Computing* | READ-PARTIAL | appraisal change from new information; film/video audience performance; emotion for animated characters |
| Scherer et al., *Appraisal Processes in Emotion* | READ-PARTIAL | stimulus-evaluation checks, sequential check theory, reappraisal |
| Combei/Reggi, *Appraisal, Sentiment and Emotion Analysis in Political Discourse* | READ-PARTIAL | multimodal (verbal+visual) stance; framing/gaze/distance/color/typography |
| Meiselman, *Emotion Measurement* | READ-PARTIAL | coordinate face+voice+body with trigger; conflicting channels change inference |
| Lazarus, *Emotion and Adaptation* | READ-PARTIAL | appraisal; orienting info / identification / distance alter audience distress |
| Al-Rodhan, *Emotional Amoral Egoism* | READ-PARTIAL | shared category ≠ shared display; social/cultural display rules |
| Gross, *Handbook of Emotion Regulation* | READ-PARTIAL | emotion-regulation strategies after appraisal |
| *Handbook of Emotions* 4th ed. | READ-PARTIAL | emotion components and core features |
| Davidson/Scherer, *Handbook of Affective Sciences* | READ-PARTIAL | affective-science mechanisms |
| Liu, *Sentiment Analysis* | READ-PARTIAL | opinion/sentiment mining for audience reading |
| *Oxford Handbook of Affective Computing* | READ-PARTIAL | affective computing mechanisms |
| Hogan, *The Mind and Its Stories* | READ-PARTIAL | empathic rasa, emotion-prototype micronarratives, junctural vs outcome pacing, telic plot |

No rubric score may rest on a w4 work without the specific governing section cited here with a line anchor (the w4 extract carries lines).

## 8c. w1 works read this phase (evidence in `extracts/w1-story.md`)

| Slice | Works | Read state | Coverage note |
|---|---|---|---|
| w1 canonical worklist (`w1-dedup.txt`) | 37/37 distinct works | **READ-PARTIAL, section-level** | 0 READ-FULL, 0 UNREAD. Each path carries a `READ-PARTIAL` state at its citation; 40 generalized-principle rows pinned to path+section. |

**Credit is partial-section coverage, never full-book.** A `READ-PARTIAL` row means the cited sections were opened and quoted, not that the whole book was read. Any rubric score that depends on a w1 work must stay `unverified` unless the specific governing section is cited here with a line anchor. Top-10 no-owner gaps from the extract: Hooks acting-objective/obstacle, Weston concrete-image, Hahn gesture, Alton prison shadows, Williams spacing chart, Habermas narrator-vocal-congruence, Mason sensory detail, Ursin explanatory metaphor, Do Rocha data throughline.

**Two findings the crosswalk makes checkable:** (1) ref **16** is the only emotion owner and its entire candidate basis (w1 emotion + w4 emotion science, 14 works) is cited nowhere; (2) `video-production-assets/references/09-edit.md` **is** the editing owner for the w1 editing slice (Murch, Pearlman, Reisz/Millar, Ondaatje) and cites 자료 ID 04,09,10,11,12. The concurrent task extended `23-finishing-platform.md` with grading craft; no second editing owner is needed, and the earlier "no editing owner" claim is withdrawn.

**Provisional owner gaps after inspecting owners (not yet all):** the w3 top-10 and w4 emotion rows remain provisional until their owners are inspected. Inspected so far: `13-ideation-brand.md` (23 L) already covers w3 **P12** (idea = collected facts recombined + maturation, 자료 37) and the product/experience split, so P12 is covered, not a gap; `creative-qa.md` and `marketing-source-adaptation.md` headings show **no** positioning-vs-alternatives, no competitor-substitute framing, no triggering-cue, no audience-segment method, no interview technique (repo-wide grep for `포지셔닝`/`세그먼트` = 1/2 unrelated files, `프리런치` = 0). Those w3 rows (P26/P59, P07/P08, P31, P02) are candidate real gaps pending full owner-text check.