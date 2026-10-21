# w2 bounded follow-up read (read-only, pre-gate)

Purpose: p16's craft slice reported only 9/16 works with substantive body reads, leaving 7 UNREAD (two preface-only). The 16 `문학·영화`/storyboard works are all legible and substantial (measured: 47 KB to 2.6 MB, all decodable UTF-8 with film/craft keyword density from 39 to 4357 hits). A bounded section read is therefore practicable. This pass reads the highest craft value works by named section and records line anchors.

## Hard rules

- READ-ONLY. Do not open or edit any SKILL.md, reference, CHANGELOG, manifest, or template file.
- Write only `qa/2026-10-16-corpus-audit/extracts/w2-craft-leader.md`.
- Every row carries the exact path, the named section, and the resolved 1-based line number `#L<n>` in that `.md` rendition. No anchor may be invented; if no heading resolves, say so and mark the row `UNVERIFIED (no resolvable section)`.
- A book read only by section is `READ-PARTIAL`, never `READ-FULL`. A preface-only or illegible book is `UNVERIFIED`, not `READ-PARTIAL`.
- No principle may bear score unless its governing section is cited with a line anchor here. Do not map any line to a craft rule the book does not itself state.

## Works (priority order: film-craft-dense first)

1. `originals/콘티_스토리보드/Film Directing Shot by Shot Visualizing from Concept to Screen (Steven D. Katz) …md` (8,502 L, kw 4357). Sections: framing/shots, staging, storyboard use. NOTE cross-slice: also read in w1; count once.
2. `originals/문학·영화/Room to Dream (David Lynch, Kristine McKenna) …md` (18,549 L, kw 2268). Sections: film-making process, idea capture, collaboration.
3. `originals/문학·영화/Starting Point 1979-1996 (Hayao Miyazakis Memoir 1) …md` (14,073 L, kw 2451). Sections: production essays, image boards, direction.
4. `originals/문학·영화/Something Like an Autobiography (Akira Kurosawa) …md` (8,513 L, kw 1258). Sections: directing, rehearsal, weather/light waiting.
5. `originals/콘티_스토리보드/Professional storyboarding rules of thumb (Paez, Sergio, Jew, Anson) …md` (8,532 L, kw 4050).
6. `originals/콘티_스토리보드/Storyboard design course … (Cristiano, Giuseppe) …md` (12,213 L, kw 2415).
7. `originals/콘티_스토리보드/The storyboard artist - A guide to freelancing in film tv and advertising (Giuseppe Cristiano) …md` (4,805 L, kw 1690).
8. `originals/콘티_스토리보드/Mastering Storyboarding Professional Techniques for Visual Storytelling (Caroline Hu) …md` (1,030 L, kw 542).
9. `originals/애니메이션/Sketching for Animation … (Peter Parr) …md` (4,837 L, kw 197).
10. `originals/문학·영화/On Writing A Memoir Of The Craft (Stephen King) …md` (7,684 L, kw 85).
11. `originals/문학·영화/I Know Why the Caged Bird Sings (Maya Angelou) …md` (7,166 L, kw 97).
12. `originals/문학·영화/Agatha Christie An Autobiography …md` (20,181 L, kw 467).
13. `originals/문학·영화/Capote A Biography (Gerald Clarke) …md` (23,350 L, kw 787).
14. `originals/문학·영화/Ernest Hemingway a life story (Baker, Carlos) …md` (60,526 L, kw 1336).
15. `originals/문학·영화/Mr. Clemens and Mark Twain (JUSTIN KAPLAN) …md` (18,527 L, kw 616).
16. `originals/콘티_스토리보드/Essentials of Creativity and Creative Behavior (Stephen P. Ramocki) …md` (4,721 L, kw 39).

If a work's body turns out to be index/OCR-fragment-only on opening, record it `UNVERIFIED (illegible body)` with the observed byte size and line count, and move on. Do not spend budget re-deriving p16's rows; this pass fills the gaps.

## Output format

`extracts/w2-craft-leader.md`:

```
# w2 bounded follow-up read (leader pass)
## Read states
| Exact path | State | Sections read (#L anchors) |
## Principles
| PRINCIPLE | EVIDENCE (path + section + #L) | OWNER | already covered? |
```

Then a short note naming which of the 16 remain UNREAD/UNVERIFIED after this pass, so the final report can carry them as explicit blockers.

---

## Execution status (leader)

`w1:p16` (the w2 worker) reported its file writer failing on both full and minimal writes and its shell runner failing before launch (`helper_unknown_error: setup refresh had errors`). It produced no saved evidence file; per the no-unsaved-claims rule its principles are NOT integrated. `w1:p15` was dispatched this spec but stayed idle without producing a file.

The leader therefore executed this read directly with the leader's own read/python tools on the exact worklist paths. Result: `extracts/w2-craft-extract.md` (0 FULL, 7 READ-PARTIAL, every row opened and anchored). The 7 works are the direct craft set (Katz, Paez, Hu, Cristiano *Design Course*, Cristiano *Storyboard Artist*, Parr, Ramocki); the 9 w2 memoirs remain READ-PARTIAL. No w2 craft work is left wholly UNREAD.

Blocker record: w2 has no worker-produced evidence file; recovery was by the leader. Any w2 principle used for scoring must appear in `w2-craft-extract.md` with a resolvable anchor, else its row stays unverified.
