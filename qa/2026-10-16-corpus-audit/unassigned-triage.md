# Unassigned-work triage (leader, 2026-10-16, evidence-based)

Supersedes the "not assigned | 860" line in `CONTRACT.md` §4, which was an unauthorized reduction. This document inventories every unassigned book work and records an evidence-based verdict per domain. Craft-relevant or adjacent-uncertain works are **kept for reading**; only works with a stated, checkable reason are excluded.

## Method
- Source: `bookset.json` `book_files` (1086 book-text `.md`), minus the 213 worklist paths = **873 unassigned book files**.
- Byte-duplicate groups (`exact_dup_groups`, 326 groups) were used to remove unassigned files that are byte-identical to an already-assigned work.
- Folder names are NOT used as evidence; a domain verdict requires a body-level reason. Representative bodies were opened (see `leader-video-craft-evidence.md`).

## Corrected counts (replacing the single "860" figure)

| Step | Files |
|---|---|
| Book-text `.md` (B) | 1086 |
| minus assigned worklists (213 paths) | **873 unassigned** |
| minus byte-identical dups of an assigned work (124) | 749 |
| distinct works after group dedup (`[INFERENCE]` upper bound; OCR-whitespace renditions inflate it) | ~547 |
| of which fiction corpus (`소설/`) | 294 |
| of which non-fiction (`[INFERENCE]`) | ~253 |

The earlier "860" and "294 novel-corpus + 231 excluded + 음악·방송/예술·문화 low tier + remaining" combined file counts with work counts and treated two whole folders as "low tier" without a body check. Both errors are corrected here.

## Verdict table (non-novel, by domain)

Verdicts: **KEEP-READ** (craft-relevant, must be read before any score that depends on it), **ADJACENT** (specialized subject-matter that can feed content research; relevant to `creative-production` sourcing, not to film craft), **EXCLUDE** (stated reason).

| Domain (files unassigned) | Verdict | Evidence / reason |
|---|---|---|
| 문학·영화 (9) | KEEP-READ | Filmmaker/writer memoirs (Kurosawa, Miyazaki, Lynch, King, Christie, Hemingway, Angelou, Capote, Twain). Assigned to `w2-craft`; same class the user named. |
| 음악·방송 (9) | KEEP-READ | Springsteen, Elton John, Keith Richards, Miles Davis, Quincy Jones, Dave Grohl, Kiedis, Bourdain, Trevor Noah. Performer/artist-craft memoirs; sound/music and on-camera performance are **named package domains** and `storyboarding-video`/`16` own rhythm and emotion. Was wrongly tiered `LOW`; bodies confirmed real books. |
| 예술·문화 (9) | KEEP-READ | Kahlo, da Vinci, Michelangelo, Picasso, Van Gogh, Dali, Warhol, Abramović, Patti Smith. Visual-art memoirs and biographies giving visual-craft and art-process evidence. Was wrongly tiered `LOW`. |
| 콘티_스토리보드 (7) | KEEP-READ | `Framed Ink` (Mateu-Mestre) is an **extraction-failure stub (254 B, 0 nonblank lines)** and stays UNREAD; `Film Directing Shot by Shot` assigned to w2; storyboarding is a core owner (`storyboarding-video`). The remaining 5 (Ramocki, Hu, Paez, Cristiano x2) are READ-PARTIAL with `#L` anchors in `extracts/leader-video-craft-evidence.md` §E. |
| 콘텐츠_제작 (37) | KEEP-READ | Remaining includes `Film Lighting Talks with Hollywood's Cinematographers` (Malkiewicz): cinematography craft, and a participant in the package's own 40-book pass; assign to a craft owner. |
| 시놉시스 (4) | KEEP-READ | Screenwriting (McKee, Truby, Vogler, Save the Cat TV); assigned to w1. |
| 디자인 (1), 애니메이션 (1) | KEEP-READ | `The Design of Everyday Things` (Norman) and `Animation Sketch` (Peter Parr); assigned. |
| 마케팅 (50), SNS (20), 광고_상세페이지 (11), 마케팅 (12) | KEEP-READ (mostly dup) | Largely KO renditions of the EN works already read by `w3-market` (translation pairs, e.g. `Made to Stick`↔`스틱!`, `Obviously Awesome`↔`오비어슬리 어썸`). Counted once per work; do not double-read. |
| 비즈니스·기업가 (58) | ADJACENT + subset KEEP-READ | Mostly business biographies. Media-industry items are craft-adjacent: `Walt Disney` (Gabler), `The Ride of a Lifetime` (Iger), `Creativity, Inc.` (Catmull), `Steve Jobs` (Isaacson). The rest are business-memoir subject matter, not film craft. |
| 과학·기술 (24) | ADJACENT | Scientist biographies (Oppenheimer, Feynman, Einstein, Tesla, Darwin, Goodall). Subject matter for documentary content; not film craft. |
| 역사·정치 (18) | ADJACENT | Statesperson biographies. Documentary/longform subject matter. |
| 스포츠 (18) | ADJACENT | Athlete memoirs (Ali, Kobe, Zlatan, Ferguson, Agassi, Pelé). Sport-story subject matter; performance-discipline principles. |
| 인간관계·커뮤니케이션 (50) | ADJACENT | Conversation/negotiation/charisma/EQ. Directly relevant to testimonial and interview content, dialogue craft, on-camera performance. |
| 비즈니스 (2), 판단 (4), 협상 (2), 조직·리더십 (4), 제품개발 (4), 집중·생산성 (4), 전략 (2), 커뮤니케이션 (2), 스타트업 (2), 사고·글쓰기 (2), 가격전략 (2), 고객검증 (3) | ADJACENT | Business-thinking and writing-craft. `The Pyramid Principle` is an **extraction-failure stub (256 B, 2 nonblank = header only)** in both the EN and KO renditions, so it stays UNREAD; it was to be the writing-craft owner candidate. |
| 애착·연애·부부 (60), 갈등·경계·가족 (50), 우정·상대선택 (40) | EXCLUDE | Relationship psychology self-help. **Reason:** an interpersonal-therapy domain with no owner and no bearing on content/film/video production. Excluded by content, with bodies sampled (e.g. `Hold Me Tight`, Sue Johnson). |
| 애착·연애·부부 (60), 갈등·경계·가족 (50), 우정·상대선택 (40) | EXCLUDE | Relationship psychology self-help. **Reason:** an interpersonal-therapy domain with no owner and no bearing on content/film/video production. Excluded by content, with bodies sampled (e.g. `Hold Me Tight`, Sue Johnson). |
| 엔지니어 성장 (6), WebRTC (2), 분산시스템 (2), 아키텍처 (2), 시스템설계 (2), 네트워크 (2), 기술전략 (2) | EXCLUDE | Software-engineering career/architecture. No craft relevance. |
| 소설 (294) | EXCLUDE (per CONTRACT) | Fiction corpus: source stories, not craft. Retained as narrative material only. |
| Whole-corpus extraction failures (11 files, all domains) | UNVERIFIED stubs | A full body scan found 11 files whose Markdown contains only a title + `> Source:` line (0 body lines): `Framed Ink` (254 B), `영화 조명` KO + `Film Lighting Talks` EN (406 B each), `The Pyramid Principle` EN+KO (256 B each), `How Brands Grow Part 2` EN+KO (508 B each), `Gifts Differing` (1024 B), `Please Understand Me` (860 B), `Personality Plus` (804 B), `The Enneagram Made Easy` (700 B). All 11 stay UNREAD; each is an extraction/conversion failure, not a reading gap. The only craft-relevant one is `Film Lighting` (Malkiewicz). |


## Items needing a reading decision (resolved this phase)
The KEEP-READ items that were flagged unread have now been given a real bounded body read, each anchored in `extracts/leader-video-craft-evidence.md`:
- **비즈니스·기업가 media subset 4** (the specific items this list named): Catmull *Creativity, Inc.* `READ-PARTIAL` (Braintrust L2544-3647, dailies L6412-6503, postmortem L10359, candor L3482-3535); Gabler *Walt Disney* `READ-PARTIAL` (story-department/storyboard chapter L7219-7265); Iger *The Ride of a Lifetime* `READ-PARTIAL` (Imagineering review L3060-3120); Isaacson *Steve Jobs* `READ-PARTIAL` (Toy Story chapter L9645-9720). All four carry book-supported craft rows; none is left unread.
- 음악·방송 9 (bodies confirmed): Grohl *The Storyteller* `READ-PARTIAL` and **CONTEXTUAL ONLY** (music memoir, no film/video applicability); the remaining 8 are now `READ-PARTIAL` with second-window craft anchors (see `extracts/leader-sectionC-reads.md` section D3: Springsteen performance-story framing, Elton John's film analogy, Miles' improvisation stance, Bourdain's line-kitchen observation, Noah's comic-timing, Quincy's arranging-as-layering and LA-film-scoring ambition, Richards' recorded variation, Kiedis' music-video account). All 9 stay **CONTEXTUAL**; the three rows with no package owner (Richards, Kiedis, Quincy film-scoring) stay `unverified`.
- 예술·문화 9 (bodies confirmed): da Vinci (Isaacson) `READ-PARTIAL`; the other 8 also now `READ-PARTIAL` with second-window craft anchors (section D2: Michelangelo grid enlargement and cartoon transfer, Warhol short-roll compensation, Van Gogh complementary color, Picasso sketchbook, Just Kids maker's-process, Dali working-feedback, Frida, Abramović). All stay **CONTEXTUAL**.
- 문학·영화 9: `READ-PARTIAL` by this leader (section D1: Christie, Capote, Hemingway, Angelou, Clemens, King, Lynch, Kurosawa, Miyazaki), each with a real `#L` anchor; all stay **CONTEXTUAL** unless a future authorized pass expands an owner.
No KEEP-READ item is left silently unassigned. Every row above is either `READ-PARTIAL` with an anchor or explicitly `UNREAD`/`unverified`.

## Exclusions are reversible
Every EXCLUDE row states its reason and can be reversed by an explicit scope decision. Nothing is deleted.