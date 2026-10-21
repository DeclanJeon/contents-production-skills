# w2 craft-set extract (leader pass, read-only)

Recovered by the leader after `w1:p16` reported its file writer and shell runner both failing (`helper_unknown_error`; setup refresh had errors). No `extracts/w2-craft.md` was ever written by p16, so its principles are NOT integrated. This extract was produced with the leader's own `read`/python tools against the exact worklist paths, and every row was opened.

## Read states (0 FULL, 7 READ-PARTIAL)

The 7 previously-unread works in `w2-dedup.txt` are the direct craft set. All were opened; each below is READ-PARTIAL with the named sections actually read. None is READ-FULL.

| Work (exact path under `E:/Book/06_Book/originals/`) | State | Sections read (#L anchors) |
|---|---|---|
| `콘티_스토리보드/Film Directing Shot by Shot Visualizing from Concept to Screen (Steven D. Katz) (z-library.sk, 1lib.sk, z-lib.sk).md` | READ-PARTIAL | TOC/continuity-style outline #L104-122; storyboard-as-tool #L766-778 |
| `콘티_스토리보드/Professional storyboarding  rules of thumb (Paez, Sergio, Jew, Anson) (z-library.sk, 1lib.sk, z-lib.sk).md` | READ-PARTIAL | staging/depth #L237-239; silhouette/simplify #L1421-1440; finished-panel rules #L3490-3500 |
| `콘티_스토리보드/Mastering Storyboarding Professional Techniques for Visual Storytelling (Caroline Hu) (z-library.sk, 1lib.sk, z-lib.sk).md` | READ-PARTIAL | clarity/composition #L235-245; depth/tonals #L249-253; balance/contrast #L259-264 |
| `콘티_스토리보드/Storyboard design course  principles, practice, and techniques  the ultimate guide for artists, directors, producers, and… (Cristiano, Giuseppe) (z-library.sk, 1lib.sk, z-lib.sk).md` | READ-PARTIAL | brief→thumbnail→revision cycle #L562, #L944-971, #L1913, #L2711-2716; client boards #L174 |
| `콘티_스토리보드/The storyboard artist - A guide to freelancing in film tv and advertising (Giuseppe Cristiano) (z-library.sk, 1lib.sk, z-lib.sk).md` | READ-PARTIAL | storyboard-as-budget #L157; client vs shooting boards #L161; rate formulas #L170; revision via layers #L1833, #L1955 |
| `애니메이션/Sketching for Animation Desenvolvendo ideias, personagens e layouts em seu Sketchbook (Peter Parr) (z-library.sk, 1lib.sk, z-lib.sk).md` | READ-PARTIAL | sketchbook as idea space #L99-112; storyboard framing in film production #L949; readable expression #L478 |
| `콘티_스토리보드/Essentials of Creativity and Creative Behavior (Stephen P. Ramocki) (z-library.sk, 1lib.sk, z-lib.sk).md` | READ-PARTIAL | problem/opportunity metacomponents #L463-472; idea box #L4094-4100; random word lists #L4205-4215 |

No w2 craft work remains wholly UNREAD after this pass; the 9 w2 memoirs stay READ-PARTIAL (not re-opened here) and are the non-craft remainder.

## Principles (each with a resolvable source anchor)

| # | Principle | Evidence (path + #L) | Package owner | already covered? |
|---|---|---|---|---|
| W2-01 | Communication, not illustration: a storyboard panel's job is to describe the story point and the emotional beat, not to be finished art | Paez #L3492-3494, #L1427-1429 | `storyboard-contract.md` (video-production-assets) | covered in intent; no explicit "not finished art" line found in owner (partly) |
| W2-02 | Silhouette carries most of the readable information; simplify bodies into primitive forms so an image reads instantly | Paez #L1424-1440 | `storyboard-contract.md`; `08-animation.md` | not stated with this specificity (absent) |
| W2-03 | A finished panel: solid poses with clear silhouette, 2-3 grey tones, limited color, limited arrows | Paez #L3496-3500 | `storyboard-contract.md` | partly |
| W2-04 | Depth supports staging: separate foreground/middle ground/background | Paez #L239; Hu #L249-251 | `07-lighting.md`; storyboard contract | partly |
| W2-05 | Clarity is a retention requirement: an unclear storyboard loses the audience | Hu #L238-239 | `02-story`/`08-animation` | not stated as a retention mechanism (absent) |
| W2-06 | Compose with rule of thirds / golden ratio; three tonal values (dark, medium, light) create dimensionality; contrast conveys emotion | Hu #L240-253, #L263-264 | `07-lighting.md` | tonal contrast present loosely; rule-of-thirds absent |
| W2-07 | Board production is a cycle: brief → thumbnails → client review → revisions, with layers enabling cheap rework | Cristiano *Design Course* #L562, #L1913, #L2711-2716; *Storyboard Artist* #L1833 | storyboard contract; `creative-qa.md` revision boundary | partly |
| W2-08 | A storyboard doubles as a budget/scope instrument; distinguish client boards from shooting boards | Cristiano *Storyboard Artist* #L157, #L161, #L170 | none in package (freelance/business) | absent (outside craft package; contextual) |
| W2-09 | A sketchbook is a low-cost personal space that trains observation, feeding project/animation ideas | Parr #L99-112 | `13-ideation-brand.md` (idea capture) | not stated (absent, supports 자료37 idea-maturation owner) |
| W2-10 | Idea generation runs divergent-thinking techniques (idea box, random word lists) once a problem/opportunity is recognized and worth concern | Ramocki #L4094-4100, #L4205-4215, #L463-472 | `13-ideation-brand.md` | partly; Ramocki directly supports the L3-4 "collected facts recombined + 숙성" owner |

Scenario key: absent = no owner line states the rule; partly = owner states a weaker/partial form.

## Cite-once note
Katz *Shot by Shot* is also in w1 (cross-slice); count once. It is the only w2 craft work with a cross-slice duplicate.

## Honest limits
- All rows are READ-PARTIAL; anchors resolve in the `.md` rendition. Katz and Ramocki reads are narrow (outline + a few passages), so their rows are the least complete.
- W2-08 (freelance/rate/budget) is real book content but belongs to no current craft owner; recorded contextual, not score-bearing.
- No score-bearing claim uses a w2 craft principle unless its owner line is confirmed in `owner-gap-verification.md`.
