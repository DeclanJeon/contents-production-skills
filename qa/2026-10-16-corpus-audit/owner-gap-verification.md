# Owner-gap verification (leader, 2026-10-16)

Converts the provisional "no owner" cells from the extracts into definitive verdicts, each backed by the owner file's actual text (line numbers 1-based in the owner file, which I opened).

## w1 provisional gaps

| Principle (book) | Named owner | Verdict | Owner evidence |
|---|---|---|---|
| Hooks: give the character a provable objective + obstacle | `04-performance.md` | **partly covered** | L9 "상대에게 무엇을 얻으려는지 목표를 정한다" covers the objective; the obstacle half is not stated explicitly |
| Weston: a concrete sensory image produces more playable choices than an abstract label | `04-performance.md` | **covered** | L12 "사실·이미지·물리적 과제·질문으로 대안을 제시하고 한 번에 한 변수만 바꿔 리허설한다" |
| Hahn: gesture follows the character's impulse, not one illustration per phrase | `08-animation.md`, `22-dialogue-lipsync.md` | **partly covered** | 08 L13-14 handle contact/gesture QA; no explicit "one impulse not one illustration" rule |
| Alton: bar-shaped shadows establish confinement before the cell | `07-lighting.md` | **absent** | L10 "그림자로 무엇을 감추고 언제 드러낼지 정한다" covers shadow as information control, but no rule that a shadow motif prefigures a later literal state, nor the "if viewers do not read it, the motif failed" check |
| Williams: key poses need specified spacing of the intervening frames | `08-animation.md` | **covered** | L12 "타이밍은 포즈 사이 프레임 수, 스페이싱은 프레임마다 위치 변화로 구분한다" states exactly the spacing rule |
| Habermas: narrator vocal emotion conflicting with the words lowers perceived authenticity | `22-dialogue-lipsync.md` | **absent** | L14 fixes `voice_identity_direction` (auditory anchor, rhythm) but has no rule for word/emotion mismatch as an authenticity signal |
| Mason: specific character-bound sensory detail over generic emotion labels | `16-concept-emotion-retention.md` | **covered** | §2 "핵심 감정에 감각적·시각적 앵커 하나를 배정" and "대사·내레이션으로 감정 이름을 붙이는 것으로 대신하지 않는다" |
| Ursin: an educational metaphor works only if both concept and familiar activity are identifiable | `16-concept-emotion-retention.md` | **partly covered** | §1 "은유의 문자화" and the copy-metaphor subsection cover metaphor realization, but not the two-part comprehension check |
| Do Rocha: a data narrative needs a traceable central subject + desired outcome + opposing condition | none found | **absent** | no owner states a data-throughline triple; `10-evidence.md` covers claim traceability, not narrative throughline |

**Net w1:** 3 covered, 3 partly covered, 3 absent. All named owners inspected.

## w3 provisional gaps

Owners inspected: `13-ideation-brand.md` (23 L), `creative-production/references/marketing-source-adaptation.md`, `creative-production/references/creative-qa.md`. Repo-wide term counts (excluding this audit dir): `포지셔닝` 1 file (an unrelated analysis doc), `세그먼트` 2 files (blender/QA, unrelated), `프리런치` 0.

| Principle (book) | Owner | Verdict |
|---|---|---|
| P12 idea-generation (James Webb Young): idea = collected material recombined + a maturation stage | `13-ideation-brand.md` | **covered** | L3-4 "관객 문제×제품 증거×뜻밖의 상황을 조합" and "숙성은 사람의 발상 과정에 대한 설명으로 다룬다"; 근거와 한계 names 자료 37 |
| P26/P59 positioning against the alternatives buyers actually consider (Dunford) | none | **absent** |
| P07/P08 attaching a message to an everyday cue (Berger *Contagious*) | none | **absent** |
| P31 audience segmentation by behavior (Kotler) | none | **absent** |
| P02 prelaunch selling what they want before the launch (Walker *Launch*) | none | **absent** |
| P27 marketing→page/source adaptation | `marketing-source-adaptation.md` | **partly covered** | §1, §4, §6 exist; the specific principle's wording not matched |

## w4 provisional gaps (verified this phase)

Owner search performed with the leader's read/grep tools over `video-production-assets/references/*.md` and `creative-production/references/*.md`: `appraisal` 0 files, `재평가` 0, `억제` 0, `다중채널` 0; `규제` 2 files but both in a compliance sense (`10-evidence.md:18`, `24-production-execution.md:159`), not emotion regulation.

| w4 principle (book) | Owner | Verdict |
|---|---|---|
| Emotion follows subjective appraisal (goal relevance, agency, coping, standards); reappraisal revises it | `16-concept-emotion-retention.md` §2 (only after P2b lands) | **absent pre-patch -> partly covered post-patch.** The bounded P2b check (`### 감정 전환의 평가 점검`) adds triggering event, goal/relationship significance, agency/coping, and observable response, and labels inferred appraisals. The broader appraisal apparatus (reappraisal mechanics, full secondary-appraisal taxonomy) stays **absent/deferred**. Before P2b is applied this row is `absent`; the grep below is the pre-patch state and stays valid as evidence for why the owner was empty. |
| Emotion-regulation strategies change the response after appraisal | none | **absent** |
| Coordinate face+voice+body with the triggering event; conflicting channels change the inferred emotion | `16-concept-emotion-retention.md` §2 (sensory anchor, no emotion labeling) | **partly covered** |
| A shared emotion category does not guarantee a shared display; social/cultural display rules shape it | none | **absent** |
| Orienting information / identification / psychological distance alter audience distress | none | **absent** |

All 12 w4 works are READ-PARTIAL (`extracts/w4-emotion.md`); the extract's OWNER/COVERAGE cells say `unverified`, which this section resolves for the mechanisms checked above.

**Post-patch reconciliation (appraisal):** once the bounded P2b check lands in `16-concept-emotion-retention.md` §2, the first row (appraisal / goal relevance / agency / coping / standards) is **partly covered by that bounded check only**. The check names the triggering event, the goal/relationship significance, agency/coping, and the observable response, and labels its inferred appraisals. It does **not** add reappraisal mechanics or the full secondary-appraisal taxonomy, so those stay `absent/deferred`. The other four rows are unchanged: regulation strategies, display rules, and identification/psychological-distance stay **absent**. Rubric/report wording must not state "appraisal wholly absent for ref 16" after P2b applies; it must state "bounded appraisal check present; broader appraisal and the other w4 mechanisms absent/deferred."

## Catmull rows vs owners

| Catmull principle | Owner | Verdict |
|---|---|---|
| Reviewers have no authority to mandate; the director decides | `creative-qa.md` | **partly covered** | creative-qa states "a validator/model judgment is not user approval" (draft ≠ acceptance ≠ publication) but has no craft rule on authority-less peer review |
| Crisis review must represent the audience | `creative-qa.md` | **absent** |
| Show unfinished work early so critique is cheap | `12-qa.md` | **partly covered** | 12-qa L1 lists 애니매틱·러프컷 as review targets but does not state the early-unfinished timing rule |
| Candor with safety (blunt but not personal) | `creative-qa.md` | **absent** |
| Postmortem / retrospective after shipping | `12-qa.md` | **partly covered** | 12-qa has a "요청 기반 제작 회고" section only when requested; not the Catmull institutionalized-postmortem rule |

**All verdicts above were made by opening the named owner file.** Ones still marked unverified name an owner not yet inspected. Absences are candidate evidence-proven gaps for the minimal-patch stage.
