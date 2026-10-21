# Extract reconciliation and dedup (leader, 2026-10-16)

Work identity and principle identity are tracked as **two separate axes** and never merged into one count. Duplicate rendition paths (same underlying work, different language or edition) are retained with their own read state; principle rows collapse **only when their text is exactly identical**, never merely because two rows share a work. Cross-slice overlaps are reconciled. No owner-gap is called definitive until the named reference is inspected.

## w3-market: work identity and principle identity are TWO separate axes (recomputed 2026-10-16)

**Supersedes all earlier w3 dedup text** ("63 works / 9 pairs / 14-pair table", and the interim "64 works" figure). The earlier confusion came from collapsing the two axes into one count. They must be reported separately, and the collapse must be driven by **exact path + exact principle text**, not by pair-count arithmetic.

### Axis 1: work identity (paths → underlying works)

**Method: work identity is NEVER derived from principle text.** Each group below is confirmed by matching the exact author + title + edition in the file's own front matter (title page or source note), independent of any principle row. Two paths merge only when the front matter proves the same underlying work; an uncertain pair is marked `[UNCERTAIN]` and its paths are NOT collapsed.

| Step | Value |
|---|---|
| w3 worklist entries (paths) | 73 |
| rendition groups with >1 path | 17 |
| paths collapsed into an existing work | 18 |
| **distinct underlying works** | **55** |

The 17 rendition groups (exact paths, `E:/Book/06_Book/...`). `Class` = whether the merged paths carry identical or different principle rows (this class does NOT affect the work count):

| Underlying work (author, title) | Paths (count) | Author/title/edition evidence | Class |
|---|---|---|---|
| Donald Miller, *Building a StoryBrand 2.0* | SNS KO `스토리브랜드 만들기 2.0` + 광고_상세페이지 EN (2) | same title both renditions | identical claims (P04=P53) |
| April Dunford, *Obviously Awesome* | SNS KO `오비어슬리 어썸` + originals/마케팅 EN + 광고_상세페이지 EN (3) | same title, 3 renditions | mixed (P26=P59 identical; P06 differs) |
| Chip & Dan Heath, *Made to Stick* | SNS KO `스틱!` + originals/마케팅 EN (2) | same title | **different claims (P05 vs P21)** |
| Jonah Berger, *Contagious* | SNS KO `컨테이저스 - 왜 어떤 것은 퍼지는가` + SNS KO `컨테이저스` (2) | both English text (verified: both open "Contagious… Simon & Schuster"); two renditions of the EN work | identical claims (P07=P08) |
| Don Norman, *The Design of Everyday Things* | originals/디자인 EN + 광고_상세페이지 EN (2) | edition pair: the ad-page rendition's own note says the original edition was titled *The Psychology of Everyday Things* | **different claims (P11 vs P62)**, edition pair |
| Kotler & Armstrong, *Principles of Marketing* | originals/마케팅 EN (18th Global) + 마케팅/epub KO `마케팅 원론` (2) | same title/edition | **different claims (P31 vs P65)** |
| Neil Rackham, *SPIN Selling* | originals/마케팅 EN + 마케팅/epub KO `SPIN 세일즈` (2) | same title | identical claims (P33=P63) |
| Tien Tzuo, *Subscribed* | originals/마케팅 EN + 마케팅/epub KO `구독 경제` (2) | same title | identical claims (P37=P64) |
| Ries & Ries, *The 22 Immutable Laws of Branding* | originals/마케팅 EN + 마케팅/epub KO `브랜딩 불변의 법칙 22` (2) | same title | identical claims (P38=P66) |
| Adrian Slywotzky, *The Art of Profitability* | originals/마케팅 EN + 마케팅/epub KO `수익의 기술` (2) | same title | identical claims (P39=P68) |
| Chris Smith, *The Conversion Code* | originals/마케팅 EN (2nd ed.) + 마케팅/epub KO `전환 코드` (2) | same title | identical claims (P41=P70) |
| Malcolm Gladwell, *The Tipping Point* | originals/마케팅 EN + 마케팅/epub KO `티핑 포인트` (2) | same title | **different claims (P43 vs P72)** |
| Jeremy Rifkin, *The Zero Marginal Cost Society* | originals/마케팅 EN + 마케팅/epub KO `한계비용 제로 사회` (2) | same title | **different claims (P44 vs P73)** |
| John Moore, *Tribal Knowledge* | originals/마케팅 EN + 마케팅/epub KO `트라이벌 날리지` (2) | same title | **different claims (P48 vs P71)** |
| Paco Underhill, *Why We Buy* | originals/마케팅 EN + 마케팅/epub KO `우리는 왜 사는가` (2) | same title | **different claims (P51 vs P69)** |
| Nassim Taleb, *The Black Swan* | originals/마케팅/md `黑天鹅…` + 마케팅/epub `블랙 스완` (2) | **corrected:** both renditions carry the same Chinese text (bibliographic line of the epub is 黑天鹅 如何应对不可预知的未来 升级版…). There is **no Korean rendition**; the Korean filename mislabels a Chinese edition. | identical claims (P52=P67) |
| Robert Cialdini, *Influence* | 광고_상세페이지 original ed. + New and Expanded ed. (2) | edition pair: same work, two editions | **different claims (P56 vs P57)**, edition pair |

Marked uncertainty:
- **Edition pairs (not certain-identity problems, but flagged):** DoET/POET and Influence original/New-and-Expanded are the *same work* in two editions; kept as one work each.
- **Corrected mislabel:** the Black Swan group is two renditions of the *same Chinese edition*, not CN + KO. No uncertain pair remains after this check.

Independent cross-check (byte-text canonical groups, `ledger_full.json`): the same 73 canonical paths resolve to **71 groups**, because cross-language renditions carry different bytes; byte dedup is a lower bound. The **55** work-identity count is the coverage figure.

### Axis 2: principle identity (principle rows → distinct principles)

72 of the 73 entries carry a generalized principle row in `extracts/w3-market.md`; P49 (Nishiuchi, *統計学が最強の学問である*) is `UNREAD` and carries none.

| Step | Value |
|---|---|
| principle rows | 72 |
| **exact-text** duplicate pairs | 9 |
| **distinct principles** | **63** (+1 UNREAD entry = 64 entries accounted) |

The 9 exact-text duplicate pairs (verified by normalized text equality over `extracts/w3-market.md`, NEVER by work):

`P04=P53`, `P07=P08`, `P26=P59`, `P33=P63`, `P37=P64`, `P38=P66`, `P39=P68`, `P41=P70`, `P52=P67`.

**Nine works carry several NON-identical principle rows** and are retained as distinct claims under the same work. Principle-row equality does not merge them, and work identity does not merge them either: deriving the work count from these rows was the original error. Verified by exact text:

| Underlying work | Rows | Why retained |
|---|---|---|
| Chip & Dan Heath, *Made to Stick* | **P05** vs **P21** | P05 = one prioritized idea beats several equally weighted claims; P21 = one central idea + a few supporting details. Different mechanisms → retain both. |
| Malcolm Gladwell, *The Tipping Point* | **P43** vs **P72** | P43 = spread depends on reach/credibility of carriers; P72 = a message designed for recall and action changes behavior. Different mechanisms → retain both. |
| Jeremy Rifkin, *The Zero Marginal Cost Society* | **P44** vs **P73** | P44 = offers framed around shared access/participation fit prosumers; P73 = low delivery cost is not sustainable while infrastructure needs funding. Different mechanisms → retain both. |
| John Moore, *Tribal Knowledge* | **P48** vs **P71** | P48 = repeated experiences embodying stated values build association; P71 = promotion grounded in a valued experience beats a trend without a clear link. Different mechanisms → retain both. |
| Paco Underhill, *Why We Buy* | **P51** vs **P69** | P51 = direct observation reveals barriers assumptions miss; P69 = slowing after entry raises notice opportunity. Different mechanisms → retain both. |
| April Dunford, *Obviously Awesome* | **P06** vs P26/P59 | P06 = perceived differentiation changes with the comparison category (frame); P26=P59 = positioning against the alternatives incl. inaction. Retain P06, collapse only P26/P59. |
| Kotler & Armstrong, *Principles of Marketing* | **P31** vs **P65** | P31 = combining demographic/geographic/psychographic/behavioral signals; P65 = segmenting by need/behavior/benefits/local context. Different source sections → retain both. |
| Don Norman, *The Design of Everyday Things* | **P11** vs **P62** | P11 = a visible affordance-cue aids discoverability; P62 = timely feedback after an action aids understanding. Different mechanisms → retain both. |
| Robert Cialdini, *Influence* (orig. + New and Expanded) | **P56** vs **P57** | P56 = peer behavior helps judge an unfamiliar choice; P57 = shared identity raises affinity. Different editions, different mechanisms → retain both. |

**Corrected totals (axis-separate):** 73 worklist paths → **55 distinct underlying works** (author/title/edition evidence above); 72 principle rows carry **63 distinct principles**; entry-level accounting = 64 (63 principle-bearing entries + 1 UNREAD). The gap between 55 works and 63 principles is exactly the 9 works above carrying more than one distinct claim; it is **not** a second work count. The earlier "64 works" figure was a category error (principle-row equality read as work identity) and is withdrawn.

## Cross-slice overlaps (both slices keep both paths, count once)

| Work | Slices | Paths retained | Principle counted |
|---|---|---|---|
| Steven D. Katz, *Film Directing Shot by Shot* | w1 (콘텐츠_제작) + w2 (콘티_스토리보드) | both `originals/…` rendition and w2 rendition | once (w1 read its shot-review rule; w2's read state kept separately) |
| Austin Kleon, *Show Your Work* | w1 (콘텐츠_제작) + w3 (SNS) | `originals/콘텐츠_제작/md/쇼 유어 워크…` + `SNS/md/쇼 유어 워크…` | once (P03 in w3; the w1 "creator provenance" row is the same book, collapsed) |

## w2-craft: 7-craft-set gap CLOSED by leader recovery

`w1:p16` reported its file writer failing on both full/minimal writes and its shell runner failing before launch (`helper_unknown_error: setup refresh had errors`). It wrote no evidence file, so its principles were never integrated. The leader read the 7 unread craft works directly (Paez, Hu, Cristiano *Design Course*, Cristiano *Storyboard Artist*, Katz, Parr, Ramocki) with own tools, on the exact worklist paths. Evidence: `extracts/w2-craft-extract.md` (0 FULL, **7 READ-PARTIAL**, every row anchored with a resolvable `#L`).

- Grading rule that was pending: now satisfied for w2, since each craft work has an opened, cited section.
- The 9 w2 memoirs stay READ-PARTIAL (not the craft set) and are not score-bearing for craft.
- w2 remains **0 READ-FULL**; w2 rows are partial. Katz is a w1+w2 cross-slice duplicate, counted once.
- Any w2 principle used for scoring MUST appear in `w2-craft-extract.md` with a line anchor, else the row stays `unverified`.

## W1/W3 status is not full source coverage

w1 (37/37 READ-PARTIAL, 0 READ-FULL) and w3 (72 READ-PARTIAL, 1 UNREAD, 0 READ-FULL) are **partial-section** reads: cited sections were opened, not whole books. Partial coverage is credited as partial only. No slice is "done"; the coverage ledger keeps every unread/preface-only/section-only state verbatim.

## Line-anchor pass on w1/w3 extracts (2026-10-16)

w1-story.md and w3-market.md originally cited each row by work title + section heading only. Every row now additionally carries the resolved 1-based line number of its cited heading in the `.md` rendition, `#L<n>` (w1: 89 anchors across all 37 works; w3: 70 of 73 rows, the 3 exceptions being the one `UNREAD` row and the two *Black Swan* rows that already carried explicit `body lines 1-70` / `68-105` hints). Anchor resolution matched the row's section tokens against the file's own heading/text lines; a row is anchored only where a heading matched, so no anchor was invented.

## Owner gaps are provisional until references are inspected

The "no existing skill covers" lists from w1/w3/w4 are **provisional**. Before any gap is recorded as definitive in `rubric.md`, the named owner reference (`video-production-assets/references/13-ideation-brand.md`, `creative-production/references/marketing-source-adaptation.md`, `creative-production/references/creative-qa.md`, `16-concept-emotion-retention.md`, `12-qa.md`, etc.) must be opened and the principle checked against its actual text. w3's P12 and P27 already name owners; the inspection pass decides whether each is truly covered, partly covered, or absent.
