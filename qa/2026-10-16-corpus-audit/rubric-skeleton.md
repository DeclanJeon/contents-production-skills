# Scorecard scaffold (structure only, no scores yet)

Scoring is **gated on `w1:pC`**. This file fixes the probe set and the evidence each row must carry, so scoring after the gate is mechanical. No score is assigned here.

Method: run the frozen S1a/S1b scenarios from `baseline-prompts.md` against each skill's own files, then read the skill's `SKILL.md` plus every bundled reference that the trigger would load. Score per `rubric-definition.md` anchors 0-5, with mandatory modifiers reported separately (`unverified`, `[INFERENCE]`, `dup:<other>`, `token:<bytes>`).

`token:<bytes>` = `SKILL.md` bytes a consumer loads before any reference. Full-load bytes (SKILL + all refs) noted in `inventory.md` §A.

| # | Skill | ver | token (SKILL B) | bundled refs | acceptance in SKILL.md | provenance form | probe required at score time | score |
|---|---|---|---|---|---|---|---|---|
| 1 | creative-production | 1.3 | 16657 | 7 | yes | n/a (coordinator) | read SKILL + 7 refs; verify single-writer contract, approval boundaries, no second coordinator | (pending) |
| 2 | topic-demand-selection | 1.0 | 6002 | 0 | no | n/a | no bundled ref; craft claims must be checked in text alone | (pending) |
| 3 | video-production-assets | 1.2 | 13205 | 35 | no | mixed (ref 16 no section; ref 12 overstated) | read all 35 refs; apply P1+P2; count refs lacking provenance | (pending) |
| 4 | camera-spatial-design | 1.0 | 4093 | 6 | no | n/a | read SKILL + 6 refs | (pending) |
| 5 | camera-motion-reference-analysis | 1.0 | 1904 | 2 | no | n/a | read SKILL + 2 refs | (pending) |
| 6 | ai-camera-control | 1.0 | 1822 | 2 | yes | n/a | read SKILL + 2 refs | (pending) |
| 7 | blender-previsualization | 2.4 | 3532 | 1 | no | n/a | read SKILL + 1 ref | (pending) |
| 8 | orchestrating-video-preproduction | 2.6 | 6952 | 2 | yes | n/a | read SKILL + 2 refs | (pending) |
| 9 | developing-video-synopses | 2.4 | 5319 | 1 | yes | n/a | read SKILL + 1 ref; check book→owner (ref 02) since corpus crosswalk maps w1 story here | (pending) |
| 10 | designing-video-character-sheets | 2.6 | 11025 | 2 | yes | n/a | read SKILL + 2 refs; corpus maps w1 performance here (Weston, Hogan character types) | (pending) |
| 11 | designing-character-personas | 1.0 | 8142 | 4 | no | n/a | read SKILL + 4 refs | (pending) |
| 12 | storyboarding-video | 2.5 | 7245 | 1 | yes | n/a | read SKILL + 1 ref; corpus maps w1 animation + Habermas pacing here | (pending) |
| 13 | storytelling-with-still-images | 1.0 | 3459 | 0 | no | n/a | no bundled ref; craft claims checked in text alone | (pending) |
| 14 | recording-production-history | 1.0 | 5498 | 0 | no | n/a | no bundled ref | (pending) |
| 15 | higgsfield-brandkit | 0.17.0 | 14871 | 24 | no | provider | provider skill; verify no image submission (ineligible in-package) | (pending) |
| 16 | higgsfield-generate | 0.17.0 | 18367 | 15 | no | provider | provider skill; verify image submission route | (pending) |
| 17 | higgsfield-marketplace-cards | 0.17.0 | 5953 | 0 | no | provider | no bundled ref | (pending) |
| 18 | higgsfield-product-photoshoot | 0.17.0 | 7363 | 1 | no | provider | provider skill | (pending) |
| 19 | higgsfield-soul-id | 0.17.0 | 4974 | 2 | no | provider | provider skill | (pending) |
| 20 | higgsfield-video-explainer | 0.18.0 | 17036 | 1 | no | provider | edited concurrently by `w1:pC`; read final state after gate | (pending) |
| 21 | higgsfield-video-replicate | 0.17.0 | 14371 | 4 | yes | provider | provider skill | (pending) |
| 22 | higgsfield-websites | 0.17.0 | 16747 | 37 | no | provider | largest ref payload (652849 B): token-burden row | (pending) |
| 23 | higgsfield-youtube-thumbnail | 0.17.0 | 9376 | 3 | no | provider | provider skill | (pending) |
| 24 | community-shorts-stills-pipeline | 1.2 | 2581 | 4 | no | provider | edited concurrently by `w1:pC`; read final state after gate | (pending) |

## Rows with a known load-bearing gap

| Skill | Gap | Evidence |
|---|---|---|
| video-production-assets (ref 12) | provenance overstatement | `sources.md` excerpt-only pass; 업로드/체크리스트/QA/통합 = 0 occurrences (verified this phase) |
| video-production-assets (ref 16) | craft with no stated basis | no `## 근거` section; three covering works (Habermas/Hogan/Lazarus) uncited (`extracts/leader-emotion-evidence.md`) |
| developing-video-synopses, storyboarding-video, designing-video-character-sheets | book→owner crosswalk `[INFERENCE]` | `book-coverage.md` §8; needs w1/w2 extracts to confirm |

## Scoring rule reminder
- Any row whose load-bearing craft rests on an unread book stays `unverified` and **may not exceed 3**.
- A row is scored once per *principle*; if two skills state the same principle, use `dup:` and do not double-count it as two strengths.
