# Planned evidence-proven patches (apply only after `w1:pC` is idle)

No skill file has been edited this phase. Every patch below was derived from reading the target file and the cited evidence; all reads are READ-PARTIAL unless stated. Each addition is written only where the owner line is confirmed absent (owner evidence in the right column). Gate: no patch may be written while `w1:pC` reports `working`.

## P1. `video-production-assets/references/12-qa.md`, `## 근거와 적용 범위`

Current line 22:
```
자료 ID: 전체 읽기 가능한 자료의 통합; 검수 규격은 설계 확장. `sources.md`에서 파일 상태와 탐색 위치를 확인한다. ...
```
Problem (verified): `sources.md` records a 40-book excerpt-level pass and states outright "전권 정독... 을 완료했다는 뜻이 아니다". It contains `업로드` 0, `편집 결정` 0, `체크리스트` 0, `QA` 0, `통합` 0, `설계 확장` 0; only `검수` 2 and `편집` 2. So "전체 읽기 가능한 자료의 통합" claims a basis broader than anything recorded; the QA-checklist spec is the author's own design, which is exactly `설계 확장` (the honest form used by ref 11 and ref 26).

Minimal change: drop the `전체 읽기 가능한 자료의 통합` half, keep `설계 확장`, name the excerpt limit.
```
자료 ID: 설계 확장(검수 규격·템플릿). `sources.md`는 첨부 자료를 발췌 탐색으로만 기록하며 전권 정독이 아니다; 파일 상태와 탐색 위치는 그곳에서 확인한다.
```

## P2. `video-production-assets/references/16-concept-emotion-retention.md`, add `## 근거와 적용 범위`

Problem (verified): the file has no provenance section at all (12230B, no `근거`-with-ID heading) and asserts detailed emotion/retention craft. Its opening sentence already disclaims guarantee ("작가의 직관을 돕는 설계 도구이며 성과를 보장하지 않는다"), but its basis is uncited. Three works covering that basis are real and were read this session:

| Work | Path | Read state (anchors) |
|---|---|---|
| Habermas, *Emotion and Narrative* | `originals/콘텐츠_제작/md/감정과 서사 - 틸만 하버마스.md` (ID 24) | READ-PARTIAL L241-253: six recipient-emotion categories, artefact vs fiction emotions, suspense as non-empathic, knowledge-advantage lever |
| Hogan, *The Mind and Its Stories* | `감정구조/md/The mind and its stories... (Patrick Colm Hogan).md` | READ-PARTIAL L974/L1006/L1064/L2406: empathic rasa, emotion-prototype micronarratives, junctural vs outcome pacing, telic plot |
| Lazarus, *Emotion and Adaptation* | `감정구조/md/Emotion and adaptation (Richard S. Lazarus).md` | READ-PARTIAL L1429/L2342/L3843/L4319/L5193: primary/secondary appraisal, core relational theme, per-emotion decision trees, aesthetic emotions |

Minimal change: add a provenance section in the package's established form, marking the boundary (author-designed procedure, excerpt-level sources, no performance guarantee), consistent with the file's own opening disclaimer.
```
## 근거와 적용 범위
자료 ID: 설계 확장(콘셉트 엔진·유지 아키텍처·감사 주기); 감정·서사 원리는 첨부 자료 발췌 탐색에 근거한다. 후보 자료: Habermas『Emotion and Narrative』, Hogan『The Mind and Its Stories』, Lazarus『Emotion and Adaptation』(각 발췌 탐색, 전권 정독 아님). 개념을 결합한 독자 설계이며, 성과나 유지율을 보장하지 않는다. `sources.md`에서 파일 상태를 확인한다.
```
This records only what was read; it does not claim the three works' full rules were reproduced verbatim.

## P2b. `video-production-assets/references/16-concept-emotion-retention.md` §2, add `### 감정 전환의 평가 점검`

Problem (verified): §2 (lines 58-91) designs an emotion sequence, target perspective, observable vulnerability, transitions, sensory anchors, contrast, disclosure timing, and an ending, but never asks **what appraisal makes an event emotional**. `owner-gap-verification.md` w4 records "emotion follows subjective appraisal (goal relevance, agency, coping, standards)" as **absent pre-patch** and no owner accepts it; once this bounded check lands, that row becomes **partly covered by this check only** (reappraisal mechanics and the full secondary-appraisal taxonomy stay absent). This is the high-value craft gap P2's provenance alone does not close.

Minimal change: one narrow, existing-owner check inserted between `### 감정 구조 패턴` (line 71) and `### 감정 정직성 점검` (line 83). No new skill, no new concept block.
```
### 감정 전환의 평가 점검

각 주요 감정 전환 전에 평가를 명명한다:
- 촉발 사건: 무엇이 일어났는가(관찰 가능한 사건).
- 목표·관계 의미: 그 사건이 누구의 어떤 목표·관계·기대와 맞물리는가.
- 행위성·대처: 책임 소재와 인물이 인식하는 대처 선택지.
- 관찰 가능한 반응: 앞 항목들에서 따라 나오는 행동·표정·선택.
평가가 브리프에 확립되지 않았으면 추론한 평가로 표시한다. 감정은 사건 자체가 아니라 그 평가에서 발생한다(평가 이론: Lazarus, 발췌 탐색).
```

Anchors (verified in the real file `감정구조/md/Emotion and Adaptation (Richard S. Lazarus)....md`, 1803443B, READ-PARTIAL): L1429 core relational theme = a primary+secondary appraisal pattern with an action tendency; L2342 primary appraisal = goal relevance, goal congruence/incongruence, ego-involvement; L3841-3843 secondary appraisal = blame/accountability and coping potential; L4319 no-blame -> sadness, external/internal blame -> anxiety/guilt/shame, favorable coping -> hope; L5193 aesthetic emotions. Broader emotion-regulation strategy claims (reappraisal, suppression effects) stay **deferred** until the skill owner is inspected and evidence supports them; only the appraisal check is added here.

## P3-P7. Authorized narrow additions (one rule each, existing owners only)

Each addition is one craft rule with a real `#L` anchor, added only where the owner line is confirmed absent. No new micro-skill, no second coordinator, no approval-ledger duplication.

| ID | Target owner | Rule (one line) | Anchor | Absence evidence (owner opened) |
|---|---|---|---|---|
| P3 | `video-production-assets/references/22-dialogue-lipsync.md` | Narrator/event emotional congruence is context-sensitive: when a narrator's vocal emotion conflicts with the line's emotion, listeners may read the narrator as less authentic or feel less empathy; align `voice_identity_direction` with the line's emotional intent. **Narrowed this session:** state as context-sensitive narrator/event congruence, not a universal voice-identity claim. | `originals/콘텐츠_제작/md/감정과 서사 - 틸만 하버마스.md#L351-359` (ID 24) | owner L14 fixes `voice_identity_direction` (auditory anchor, rhythm) but states no word/emotion-mismatch authenticity rule; vocal terms appear 3x but none is this rule (`owner-gap-verification.md`). |
| P4 | `video-production-assets/references/07-lighting.md` | Bar-shadow shapes on a wall suffice to indicate a prison/locked setting without a literal cell shown; the cue only works if viewers read it. **Corrected this session:** the source does NOT support "prefigure a later literal reveal", so the word "prefigure" is dropped and the rule states the indicator function only. | `originals/콘텐츠_제작/md/Painting With Light (John Alton) (z-library.sk, 1lib.sk, z-lib.sk).md#L187-189` (ID 02) | owner L10 covers shadow as information control, but states no bar-shadow-as-setting-indicator rule and no "if viewers do not read it, the cue failed" check (0 shadow-indicator hits). |
| P5 | `video-production-assets/references/10-evidence.md` | A data narrative has a traceable throughline when its central subject (hero), desired outcome (what the hero wants), and opposing condition (adversary/comparator) can each be identified. **Corrected this session:** the §6.2 anchor is L375-376; L25 is contents/front matter. | `originals/콘텐츠_제작/md/생성형 인공지능 데이터 스토리텔링 - 안젤리카 로 두카.md#L375-376` (ID 30) | owner covers claim traceability (step 1) but states no throughline triple (0 hits). |
| P6 | `video-production-assets/references/13-ideation-brand.md` | Segment by need, behavior, benefits, and local context; demographic labels alone may group dissimilar customers. **Corrected this session:** anchor is the segmentation block L16831-16839 / L16871-16895 / L17124-17165; L276 is not the segmentation passage. | `마케팅/epub/마케팅 원론 - 필립 코틀러, 게리 암스트롱.md#L16831-16839` (ID 44) | owner step 5 separates brand values from experience but states no segmentation rule (`세그먼트` 2 files, both unrelated). |
| P7 | `creative-production/references/marketing-source-adaptation.md` | Positioning is judged against the alternatives buyers actually consider, not against the product's own features. **Anchored this session:** `originals/광고_상세페이지` Dunford `Obviously Awesome` L1135-1140 (alternatives), features further L1167-1171. | `광고_상세페이지/md/Obviously Awesome (April Dunford) (z-library.sk, 1lib.sk, z-lib.sk).md#L1135-1140` (ID 43) | owner has 1 positioning hit, not this rule; §1/§4/§6 exist but the principle's wording is not matched. |

## Sources integration (part of the patch stage)

Add these works to `video-production-assets/references/sources.md` with path + anchors + read state + owner. Existing IDs reused: Alton 02, Habermas 24, Lo Duca 30. Verified: `sources.md` rows are IDs 01-40 and **none** is Kotler or Dunford (`Principles of Marketing`/`마케팅 원론`/`Kotler`/`Obviously Awesome` all 0 hits), so those need new IDs. New IDs for works absent from the 40-book crosswalk:

- **41** Hogan, *The Mind and Its Stories* (owner ref 16, ref 02, `developing-video-synopses`).
- **42** Lazarus, *Emotion and Adaptation* (owner ref 16, `creative-qa`).
- **43** Dunford, *Obviously Awesome* (owner `marketing-source-adaptation.md`) if P7 is applied.
- **44** Kotler/Armstrong, *Principles of Marketing* 18th global ed. / *마케팅 원론* (owner `13-ideation-brand.md`) if P6 is applied.
- Habermas ID 24 already exists (modules 02,04,10); its row gains the emotion anchors.

## Deferred: verified content gaps, documented not patched

`owner-gap-verification.md` proves further absent craft rules that are NOT patched this phase, because adding them would expand craft (scope growth beyond minimal remediation) and risk the coordinator/micro-skill-sprawl constraint:

- w3 triggering-cue attachment (Berger *Contagious* P07/P08) and prelaunch (Walker *Launch* P01/P02): no owner; a new message-cue and launch-phase concept each.
- Catmull: authority-less review, audience-representative review, candor-with-safety, institutionalized postmortem: only partly covered by `creative-qa.md`/`12-qa.md`; adding them would be a craft-module expansion.
- w4 **regulation strategies** (reappraisal/suppression effects), **display rules**, **identification/psychological-distance** mechanics, and the remaining unimplemented w4 mechanisms: absent, no existing owner line accepts them without a new concept block; deferred. **Appraisal is NOT deferred wholesale**: only the bounded P2b check (name triggering event, goal/relationship significance, agency/coping, observable response; label inferred appraisals) is added to `16-concept-emotion-retention.md` §2. The full appraisal-model apparatus (Scherer component-process checks, per-emotion decision trees) is not adopted.
- Section C's 18 works (9 art/culture + 9 music/broadcast): five candidate rows owner-checked and ALL stayed CONTEXTUAL; no score-bearing rule; NOT added.

A future authorized pass can promote the strongest (positioning P7, audience-representative review) into existing owners.

## Gate reminder
No patch may be written until `w1:pC` reports idle/done. After that, in this order, before ANY skill edit:

1. Record the pre-edit gate: `git diff --numstat` + HEAD; `python scripts/check_versions.py`; `python -X utf8 -m pytest -q --basetemp='C:/Users/Declan/AppData/Local/Temp/pytest-omp-cps5'`.
2. Run the **COMPLETE byte-frozen all-skill + video-module baseline** (not only S1a/S1b): `M-01`..`M-24`, `V-01`..`V-28`, `VC-1`..`VC-3`, `VP-1`,`VP-2`, `VS-1`, `VO-1`, plus `S1a`/`S1b`, verbatim from `baseline-prompts-exact.md`/`baseline-prompts.md`, in fresh single-turn read-only sessions. This all-skills before-arm is required for the user-requested all-skills before/after QA. Dispatch per `worker-dispatch.md` (disjoint ranges) to the idle panes; write `baseline-results.md` with PASS/FAIL and verbatim excerpts.

Then apply P1, P2, P2b, P3-P7, bump only the edited skills + package version in lockstep, re-run `check_versions.py` + pytest (fresh basetemp `pytest-omp-cps6`), re-run the SAME ranges with the SAME byte-identical prompts to `post-results.md`, and verify relative links.
