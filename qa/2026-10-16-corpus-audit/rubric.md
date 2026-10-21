# Skill scorecard: 24 installed skills, 0-5

Method: `SKILL.md` plus every bundled reference a trigger would load, read directly this session; scored per the fixed anchors in `rubric-definition.md`. Behavioral rows back onto the completed baseline arm (`baseline-results.md`, 61 frozen prompts). Structural facts (bytes, ref counts, heading presence) come from the direct scan in the transcript.

> **Superseded:** this historical scorecard predates the fixed acceptance rule and post-audit evidence. Its global-ceiling assertions and scores below are not authoritative. Apply `rubric-definition.md` and the current `qa/skill-completeness-95/` records; `READ-PARTIAL` may qualify when the exact scope and exercised verification are recorded.

Gate note: scored after `w1:pC` flipped to `idle` (seq 835), so `SKILL.md` and `reference/` bytes here are the post-remediation state (`check_versions.py` OK; pytest 254 passed / 8 skipped both sides).

## Global ceilings that apply to every row

- **No row scores 5.** Anchors 5 requires every craft claim traceable to a cited source with read-scope stated **and** an exercised verification record. Across the package only **19 of 154** reference files carry a provenance-style heading, so a claimed "every craft claim" is false for 23 of 24 skills. Score 5 is therefore unreachable this audit, not merely unearned.
- **Read state everywhere is `READ-PARTIAL`** (`발췌 탐색`, excerpt scan). Zero works are READ-FULL. A `READ-FULL` citation does not exist anywhere in the package, so no citation can satisfy the score-5 evidence rule.
- `unverified` is used **only** where the skill's load-bearing craft maps by crosswalk onto a book this audit could not open at all (the 11 extraction-failure stubs, chiefly Malkiewicz, *Film Lighting Talks*). A partially-read book (`READ-PARTIAL`) is read, so it does not trigger the cap.
- `token:<bytes>` = the `SKILL.md` bytes a consumer loads before any reference.

## Scorecard

| # | Skill | ver | token B | refs | score | modifiers | decisive evidence |
|---|---|---|---|---|---|---|---|
| 1 | creative-production | 1.3 | 16738 | 7 | **4** | `dup:video-production-assets` (SSOT/single-writer) | Coordinator only. Scope + "Select one current stage" + Planning/review/execution separate review acceptance from user acceptance and media permission; states `.history` return contract. No `## Acceptance` heading, so the criterion is prose-level but reviewer-failable. Boundary explicit. |
| 2 | topic-demand-selection | 1.0 | 6016 | 0 | **3** | none | `When to Use` / `Decision Procedure` / `Evidence Labels` / `Common Mistakes`. Output named, no acceptance criterion and no exclusion boundary. |
| 3 | video-production-assets | 1.2 | 22261 | 35 | **4** | `dup:creative-production`; token-burden row | Strongest boundary in the package (실행 원칙 + 요청 범위와 완료 판정 + separate 프리프로덕션 수락 / 영상 실행 승인 / 게시 승인), explicit `pass / pass_with_notes / needs_revision` + `unverified` reporting. Post-remediation refs 07/12/16 now carry stated read scope. Not 5: 13 of 35 refs still lack a provenance heading. |
| 4 | camera-spatial-design | 1.0 | 7080 | 6 | **3** | `dup:blender-previsualization` (3D spatial) | `장소 공간 계약 (v5.1)` + 산출물 named; no acceptance criterion; boundary implicit. |
| 5 | camera-motion-reference-analysis | 1.0 | 3446 | 2 | **2** | none | 26 lines; `완료와 저장` only. No exclusion boundary, no acceptance, no blocker list. |
| 6 | ai-camera-control | 1.0 | 3237 | 2 | **3** | none | `인계와 실행 경계` = explicit handoff boundary; output named; acceptance absent. |
| 7 | blender-previsualization | 2.4 | 6021 | 1 | **2** | `dup:camera-spatial-design` | `실행` / `실행 출력`; no boundary, no acceptance, no blocker naming. |
| 8 | orchestrating-video-preproduction | 2.6 | 6988 | 2 | **4** | none | Has `## Acceptance` (stages no more/no fewer, artifacts not reports, nothing implying media or spend) **and** `Missing technical inputs` = named blockers instead of silent substitution. |
| 9 | developing-video-synopses | 2.4 | 5369 | 1 | **4** | `[INFERENCE]` book crosswalk | Has `## Acceptance` (artifact present not a report, beat-map QA passed, fact status per claim, repairs proposed not applied). Its one craft ref carries no provenance heading; the w1-story crosswalk is `[INFERENCE]` (`book-coverage.md` §8). |
| 10 | designing-video-character-sheets | 2.6 | 11145 | 2 | **4** | `[INFERENCE]` book crosswalk | Has `## Acceptance` (each sheet returned, 확정/제안/관찰/미정 separable, voice axes separated, no invented real-person facts). Both refs carry provenance headings. |
| 11 | designing-character-personas | 1.0 | 8190 | 4 | **4** | none | `Return contract` + `Quality gate` + `Voice boundaries` = reviewer-failable gate and an exclusion boundary; 1 of 4 refs carries provenance. |
| 12 | storyboarding-video | 2.5 | 7287 | 1 | **4** | `dup:higgsfield-video-replicate` (board contract) | Has `## Acceptance` with a real blocker rule: indexed unresolved requirements block completion of the stage they serve. |
| 13 | storytelling-with-still-images | 1.0 | 3491 | 0 | **3** | none | `Principle` / `Activate when` / `Workflow` / `Cue-table contract`. Output contract present; no acceptance, no boundary. |
| 14 | recording-production-history | 1.0 | 8646 | 0 | **3** | none | `이 스킬이 하는 일` + `언제 쓰지 않나` (explicit exclusion) + CLI 계약. No acceptance criterion. |
| 15 | higgsfield-brandkit | 0.17.0 | 14931 | 24 | **4** | provider; token-burden row | `Consistency invariants` + `Failure policy` + `Deterministic scripts` + `Delivery`: invariants are reviewer-failable, failure policy names blockers. Provider docs, not books, so no book cap. |
| 16 | higgsfield-generate | 0.17.0 | 18479 | 15 | **3** | provider | `Scope` + `Package gate` + `Errors` + `Discovery guardrail`. Boundary present; no acceptance criterion. |
| 17 | higgsfield-marketplace-cards | 0.17.0 | 5969 | 0 | **3** | provider | `Package gate and eligibility` + `Delivery`; boundary present, acceptance absent. |
| 18 | higgsfield-product-photoshoot | 0.17.0 | 7385 | 1 | **3** | provider | Has `What this skill does NOT do` (strong exclusion) + `Common mistakes`; no acceptance criterion. |
| 19 | higgsfield-soul-id | 0.17.0 | 5014 | 2 | **3** | provider | `Scope and package gate` + downstream contract + `Errors`; acceptance absent. |
| 20 | higgsfield-video-explainer | 0.18.0 | 17106 | 1 | **3** | provider; peer-edited | `Hard rules` + phased pipeline + `Phase 0 ask first`; boundary and blocker behavior strong, no acceptance criterion. |
| 21 | higgsfield-video-replicate | 0.17.0 | 14527 | 4 | **3** | provider; `dup:storyboarding-video` | `Hard rules` + `Ask first model selection` + REQUIRED board contract pointer; acceptance absent. |
| 22 | higgsfield-websites | 0.17.0 | 16929 | 37 | **3** | provider; largest token burden (refB 652849) | `Package gate and scope` + UX rules + turn economy; acceptance absent. Highest consumer-load row in the package. |
| 23 | higgsfield-youtube-thumbnail | 0.17.0 | 9404 | 3 | **4** | provider | `Intake gates` + `Concept gate` + `Post-render gate` = a reviewer-failable acceptance chain with named blocks. |
| 24 | community-shorts-stills-pipeline | 1.2 | 3957 | 4 | **3** | provider; peer-edited | `불변 규칙` + `적용 순서` + scripts; boundary present, acceptance absent. |

## Distribution

| Score | Count | Skills |
|---|---|---|
| 5 | 0 | none (evidence-bound anchor unreachable: 19/154 refs carry provenance; zero READ-FULL) |
| 4 | 9 | creative-production, video-production-assets, orchestrating-video-preproduction, developing-video-synopses, designing-video-character-sheets, designing-character-personas, storyboarding-video, higgsfield-brandkit, higgsfield-youtube-thumbnail |
| 3 | 13 | topic-demand-selection, camera-spatial-design, ai-camera-control, storytelling-with-still-images, recording-production-history, higgsfield-generate, higgsfield-marketplace-cards, higgsfield-product-photoshoot, higgsfield-soul-id, higgsfield-video-explainer, higgsfield-video-replicate, higgsfield-websites, community-shorts-stills-pipeline |
| 2 | 2 | camera-motion-reference-analysis, blender-previsualization |
| 1 | 0 | none |
| 0 | 0 | none |

## `dup:` pairs (one principle, two owners; flagged once)

| Principle | Owners |
|---|---|
| SSOT / single-writer / approval boundaries | creative-production, video-production-assets |
| 3D spatial spec then Blender previsualization | camera-spatial-design, blender-previsualization |
| Storyboard board contract | storyboarding-video, higgsfield-video-replicate |

## Token-burden rows (consumer bytes before any reference)

| Skill | token B | full-load ref B | note |
|---|---|---|---|
| video-production-assets | 22261 | 382873 | 35 refs; largest craft payload |
| higgsfield-generate | 18479 | 75672 | |
| higgsfield-video-explainer | 17106 | 5572 | |
| higgsfield-websites | 16929 | 652849 | largest total payload by far |
| creative-production | 16738 | 55778 | |

## Honest limits on this scorecard

- Scores 4 are gated-level only: acceptance + named blockers, verified behaviorally by the corresponding baseline row. They are **not** evidence-bound, so they are not 5.
- Two rows (`developing-video-synopses`, `designing-video-character-sheets`) carry `[INFERENCE]` on the book-to-owner crosswalk (`book-coverage.md` §8); the mapped works were read `READ-PARTIAL`, so the inference is about ownership, not the craft claim.
- No row is capped by `unverified`, because the 28 craft-core works were read at excerpt level; the cap would apply only if a skill's load-bearing craft resolved solely onto one of the 11 extraction-failure stubs, and none does.
- The two `2` rows are structural, not craft, judgements: `SKILL.md` too thin to gate.
