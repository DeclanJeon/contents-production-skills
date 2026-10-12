# Archive crosswalk known-model skill-output run

**Overall:** NOT PASS against frozen assertions. The bounded crosswalk row, candidate distinctions, story-neutral transfer, and 06/Shot-DNA field handoff meet their criteria. Coverage status is incomplete: the response omits the selected source's explicit `visual_semantic_craft_closed` status and the named open archive-wide gates. This does not establish all acceptance passed.

## Run metadata

- Run: one fresh stateless `functions.task` call (`CrosswalkSkillOutputV2`), behavioral skill-output task; one response, no retries.
- Model metadata: runtime-advertised identity `openai-codex/gpt-6-luna`; the task interface did not expose an additional tier/effort suffix or per-call model string. The run was not sent to a separate `vibe` endpoint; this report records the actual route and available model metadata rather than inventing a suffix.
- Context: current working-tree package instructions/references/templates and bounded current semantic evidence for the specified source. No test plan, rubric, previous output, diagnosis, or result artifact was included in the model context. No original media/images/playback, F: writes, or all-44 analysis.
- Requested output: one filled bounded crosswalk row and the two candidate disposition records; actual output is preserved below.
- Package context SHA-256:
  - `video-production-assets/SKILL.md`: `c400ac9192be3b9783b131a1e4f1574e4aa9c8027cdfe160fa350cd35aafdcca`
  - `video-production-assets/references/25-reference-video-analysis.md`: `da4ebf6f976fd4c5e548777399c53331dd84fa3efbbd50291895570c2f9512f3`
  - `video-production-assets/assets/archive-craft-crosswalk-template.md`: `43079fcd460b92da2f58e415f76721ea2200e4ab492cb0ef114c7051a9da7b43`
  - `video-production-assets/assets/archive-audit-template.md`: `333e6f844ac79878b7a948761abc19c50dc57d0ee38d105bc3a50f5b1c15e487`
  - `video-production-assets/assets/shot-dna-template.md`: `5dbc0b305ad97da240baf19cf92db5962fd1824b48448a73f57fc0600f9ab3fa`
  - `video-production-assets/references/06-shots.md`: `ee493732d45b82fc5f640a9af8041fca3e78e363da6183de14d59115e5de6b5e`
  - `video-production-assets/assets/06-shots-template.md`: `506c83f3814c04ed1ebb429301d0f92ee9644e30207de74d03a4d032e18ae860`
- Bounded evidence files (F: paths, SHA-256):
  - `videos/rofan-temporal-analysis/exhaustive/semantic/archive-normalized-master-in-progress.json` — `f62effd762239c581992213ad4e371b79aa6c22f0682c50b921a43d563135a6e`
  - `videos/rofan-temporal-analysis/exhaustive/semantic/cross-source-craft-catalog-provisional-v1.json` — `63984d67816a38d40c33f55120b5e30702f607981eeadab0b4feebe64adadb6f`
  - `videos/rofan-temporal-analysis/exhaustive/semantic/reviewer-F/ea6a017b14fc647205b30ea896553c8e36e3abbc2983b73757a9c7cb282a8257-canonical-shot-scene-event-ledger.json` — `2226407c876bd979cc236e55ddb17db6276f2059893d55e9ced81a6c8a134d8a`
  - `videos/rofan-temporal-analysis/exhaustive/semantic/reviewer-F/ea6a-native-union/candidate-dispositions.json` — `a986c48e1ce3f007ea07bff44efbde2afabee004854a480c2db5ae9c4ebb52e2`

## Frozen criteria and behavioral transfer grade

| Criterion | Grade | Evidence |
|---|---|---|
| One bounded row traceable to the predeclared occurrence, scene, shot, event, and locators | PASS | Full `source_position_id`, `archive_id`, scene, shot, and event IDs; filename, source PTS timebase, bounded interval and locators stated. |
| Preserve `[0,77824)` and supported candidate outcomes; do not invent cuts | PASS | Gives full candidate IDs and PTS; 77824 is `observed_hard_view_change` with neighbor triplet; 78848 is `continuous_within_shot` with its triplet. No extra cut is claimed. |
| Story-neutral mechanism, inference/alternative, applicability and avoid conditions | PASS | Mechanism is generic and timing-free; `[INFERENCE]`, alternative, transfer predicate and avoidance conditions are explicit. |
| Exact receiving owner/QA fields and all five existing Shot-DNA `이전 체인` fields | PASS | Names all required 06 identity/time fields, the applicable approach/response/contact fields, other applicable existing 06 fields, and the exact `06-shots.md` `완료 조건` QA slot. Separately maps `레퍼런스 증거(관찰+위치)`, `메커니즘`, `의도 효과(해석)`, `새 브리프 제작 요구`, and `정성 검증 기준`. |
| Selected-source and archive-global coverage status | FAIL | Correctly gives 34/44 materialized and ten unmaterialized and makes no completion claim, but omits the selected row's explicit `visual_semantic_craft_closed` status and does not name the required open archive gates (crosswalk, native-image, candidate-free transitions/first-last, scene bounds, occurrence-vs-case reconciliation). |
| Behavioral transfer clarification: 06 handoff carries target identity/time plus applicable exact creative/QA fields | PASS | Includes `shot_id`, `scene_id`, `beat_id`, `shot-local time (s or frames; FPS if frames)`, and the applicable listed 06 fields, with no new schema fields. |

The frozen acceptance is **not fully met** because the coverage-status criterion failed. The fix's target owner-field behavior is observed in this run; archive/source-status reporting remains incomplete. No claim is made about other prompts or statistical reliability.

## Raw response

```text
## 범위와 한계
- 요청 범위: CF-13에 한정한 단일 source occurrence·scene·shot·event crosswalk이며, exhaustive all-source/all-shot 분석이 아니다.
- 검토한 범위: 아래 source의 shot p0, PTS [0,77824), 1/15360 timebase; 두 개의 지정 후보 disposition. 근거는 제공된 의미 ledger/catalog의 텍스트만 읽었다. 원본 미디어·이미지 열람/재생은 하지 않았다.
- 현재 선택 source: `source_position_id=ea6a017b14fc647205b30ea896553c8e36e3abbc2983b73757a9c7cb282a8257`, `archive_id=sha256:4831e753f691064aaa92b4b3748045b3fbef7d6dc76e0cfb21e37f1b7c4db195`, filename `AI 로판 드라마 ｜ 몰아보기 EP.1~9 ｜ 버려진 약혼녀에게 집착이 시작됐다 🗝️.mp4`. Ledger records sampled/dense and native-neighbor review; this response does not claim direct media review or continuous playback. Audio is not human-listened.
- Archive-wide: master/catalog state 34/44 materialized, 10 unmaterialized; no archive-wide completeness, recurrence, prevalence, or zero-findings claim. This row is one bounded case only.

## Filled crosswalk row (1)

| finding_id | linked occurrence / sequence / scene / shot / event IDs | directly observed evidence + exact source PTS/timebase and locator | `[INFERENCE]` function + plausible alternative | story-neutral mechanism | transfer conditions | avoid / counterconditions | existing owner procedure + exact existing QA slot/field | target-specific observable acceptance check | evidence gaps / status |
|---|---|---|---|---|---|---|---|---|---|
| CF-13 | source_position_id `ea6a017b14fc647205b30ea896553c8e36e3abbc2983b73757a9c7cb282a8257`; archive_id `sha256:4831e753f691064aaa92b4b3748045b3fbef7d6dc76e0cfb21e37f1b7c4db195`; scene `F-EA-SC01` (scene span 0–5.033333333333333s, membership bounded by shot); shot `archive-shot:ea6a017b14fc647205b30ea896553c8e36e3abbc2983b73757a9c7cb282a8257:p0` ([0,77824), TB 1/15360; visible last frame PTS 77312); event `archive-event:ea6a017b14fc647205b30ea896553c8e36e3abbc2983b73757a9c7cb282a8257:p0:F01`; candidate IDs `archive-event:ea6a017b14fc647205b30ea896553c8e36e3abbc2983b73757a9c7cb282a8257:77824` and `archive-event:ea6a017b14fc647205b30ea896553c8e36e3abbc2983b73757a9c7cb282a8257:78848` | At PTS 0, 39424, and 77312, ledger’s shot-local notes record an initial single figure in profile, a second figure joining the frame and proximity developing, then visible face/hand contact held at the outgoing edge. These are source-PTS observations in `...canonical-shot-scene-event-ledger.json#/shots/0/within_shot` (`manual_visual_review_ref` and `sidecar_ref` named in that row); dense-state note describes sampling, not continuous playback. PTS 77312→77824 is the exact outgoing/incoming neighbor pair for the hard cut; candidate 77824 is `observed_hard_view_change`. The scene row `#/scenes/0` bounds F-EA-SC01 to 0–5.033333333333333s and links the p0 shot and F01 event. | `[INFERENCE]` A shared frame that keeps initiating action and partner response legible, with enough hold for the contact/state to register, may make a relational beat readable before an editorial reset. Alternative: conventional coverage, an assembled/generated pose progression, or transition/continuity mechanics rather than deliberate emotional emphasis; intent is not observed. | Keep the initiating action and receiving partner’s visible response in a shared readable frame; allow the resulting state to register before cutting or otherwise resetting the relation. No prescribed camera move, gait, gesture, or duration. | Transfer only when the beat’s meaning depends on who acts toward whom and the audience must read the response/contact. In a new brief, choose new actors, action, environment, framing, and timing; establish only the visibility/response requirement needed for that brief. | Avoid when shared framing obscures the action, separate viewpoints convey necessary information better, contact/consent/force is not established or should not be implied, or beat does not require contact. Do not claim a completed walk, natural gait, physical camera path, creator intent, emotional state, consent, or copy any source narrative/assets/order/timing. | Receiving owner: `video-production-assets/references/06-shots.md`; existing template `video-production-assets/assets/06-shots-template.md`. Applicable exact fields: `shot_id`, `scene_id`, `beat_id`, `shot-local time (s or frames; FPS if frames)`, `크기/카메라 위치`, `인물 블로킹`, `시선/축`, `공개 정보`, `관점·감정/구도 의도`, `대안·채택/승인 상태`, `카메라 동작`, `종료 프레임`. QA slot: `references/06-shots.md` §완료 조건 — “각 샷의 관점·구도 선택이 의도한 정보와 감정을 전달하는가? 실제 이미지가 있으면 필수 행동과 주목점이 읽히는가?” | For the new brief’s assigned `shot_id`/`scene_id`/`beat_id` and shot-local time, inspect its storyboard/render at delivery size: action source and partner response/contact state must both be visibly identifiable in the intended frame(s), the response must be readable before any planned cut/reset, and selected viewpoint/axis must not hide the needed information. Text-only plan can specify this check but cannot pass actual-image QA. | Bounded finding only; low-confidence interpretive function. No audio listening, continuous playback, physical camera cause, or natural-motion/gait verification. Archive-wide coverage remains incomplete as stated above. |

### Shot-DNA `이전 체인` (all five existing fields)
1. **레퍼런스 증거(관찰+위치):** p0, TB 1/15360, PTS 0 / 39424 / 77312; shot-local observations and boundary information at ledger `#/shots/0/within_shot` and `#/shots/0/exit`; candidate 77824 confirms the hard view change. Source facts are cited above; no original media was opened here.
2. **메커니즘:** Shared framing keeps action and partner response readable; hold on the resulting state until it registers, then reset/cut if the new beat requires it.
3. **의도 효과(해석):** `[INFERENCE]` May clarify relational proximity/contact. Alternative: routine coverage or generated pose continuity; intent unknown.
4. **새 브리프 제작 요구:** If the new brief’s action needs a partner response to be understood, stage both action and response visibly in the chosen shot; choose new story content and locally designed timing.
5. **정성 검증 기준:** At the target output size, action and response/contact read in the planned frame(s); intended state registers before cut/reset; no hidden needed action or unsupported inference. Actual image review required to mark image-level pass.

### 06 handoff mapping (proposal only; no project IDs invented)
- `shot_id`: assigned downstream for the new production; not assigned in this analysis.
- `scene_id`: assigned downstream; not assigned in this analysis.
- `beat_id`: assigned downstream; not assigned in this analysis.
- `shot-local time (s or frames; FPS if frames)`: set by the new brief/shot plan; no source timing transferred.
- `크기/카메라 위치`: choose framing that keeps the needed action and response observable.
- `인물 블로킹`: identify initiating action and receiving response, with visible positions and contact/state only as required by new brief.
- `시선/축`: preserve readable relation and screen direction; do not infer source eyeline beyond ledger.
- `공개 정보`: state what action/response becomes legible and when.
- `관점·감정/구도 의도`: state the new brief’s audience-information purpose, not source emotion.
- `대안·채택/승인 상태`: record viable alternatives and actual adoption/approval state; no approval inferred.
- `카메라 동작`: only if motivated/selected for the new brief; no source move asserted.
- `종료 프레임`: define visible target state before cut/reset.
- Exact 06 QA slot and observable check: as listed in the crosswalk row; actual rendered/storyboard image inspection remains a downstream gate.

## Candidate disposition records (exactly two)
1. **Candidate** `archive-event:ea6a017b14fc647205b30ea896553c8e36e3abbc2983b73757a9c7cb282a8257:77824` — source `ea6a017b14fc647205b30ea896553c8e36e3abbc2983b73757a9c7cb282a8257`; PTS 77824 / TB 1/15360 / 5.066666666666666s; status `reviewed`; disposition `observed_hard_view_change`. Neighbor frames PTS 77312, 77824, 78336. Record observation: “Abrupt transition from close intimate face-to-face wall shot (red-haired man cups blonde’s face) at 5.033s to bright corridor medium two-shot at 5.067s; candidate and next frames persist hallway. Cut confirmed visually; production cause unknown.” Locator `candidate-dispositions.json` item at candidate_order 1; image refs `chunk_0_00001.jpg`, `chunk_0_00002.jpg`, `chunk_0_00003.jpg`.
2. **Candidate** `archive-event:ea6a017b14fc647205b30ea896553c8e36e3abbc2983b73757a9c7cb282a8257:78848` — source `ea6a017b14fc647205b30ea896553c8e36e3abbc2983b73757a9c7cb282a8257`; PTS 78848 / TB 1/15360 / 5.133333333333334s; status `reviewed`; disposition `continuous_within_shot`. Neighbor frames PTS 78336, 78848, 79360. Record observation: “Same bright corridor medium two-shot and eyeline; no composition discontinuity across 5.100–5.167s.” Locator `candidate-dispositions.json` item at candidate_order 2; image refs `chunk_0_00003.jpg`, `chunk_0_00004.jpg`, `chunk_0_00005.jpg`.

## Exact package and evidence paths consulted
- `video-production-assets/SKILL.md`
- `video-production-assets/references/25-reference-video-analysis.md`
- `video-production-assets/references/contract.md`
- `video-production-assets/assets/archive-craft-crosswalk-template.md`
- `video-production-assets/assets/archive-audit-template.md`
- `video-production-assets/assets/shot-dna-template.md`
- `video-production-assets/references/06-shots.md`
- `video-production-assets/assets/06-shots-template.md`
- `F:\Resources\AI-Rofan-Drama-2026-10-11\videos\rofan-temporal-analysis\exhaustive\semantic\archive-normalized-master-in-progress.json`
- `F:\Resources\AI-Rofan-Drama-2026-10-11\videos\rofan-temporal-analysis\exhaustive\semantic\cross-source-craft-catalog-provisional-v1.json`
- `F:\Resources\AI-Rofan-Drama-2026-10-11\videos\rofan-temporal-analysis\exhaustive\semantic\reviewer-F\ea6a017b14fc647205b30ea896553c8e36e3abbc2983b73757a9c7cb282a8257-canonical-shot-scene-event-ledger.json`
- `F:\Resources\AI-Rofan-Drama-2026-10-11\videos\rofan-temporal-analysis\exhaustive\semantic\reviewer-F\ea6a-native-union\candidate-dispositions.json`
```