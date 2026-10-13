# Cross-domain craft-transfer smoke results

Append-only note: the original five-call scenario set and its grades/raw outputs are retained as recorded below. The matrix now includes one additional unrelated lighting scenario, recorded in the separate extension section at the end.
This is a separate, descriptive five-call smoke. It does not replace or regrade frozen T13–T20. The four positive prompts use unrelated fictional briefs and omit the casebank; the negative control includes it. No archive-derived claim is tested or made.

- **Calls:** 5 planned / 5 completed; one fresh stateless `completion(prompt, model="default", system=package_context).wait()` per scenario; no retry/error recorded.
- **Model:** selection `default`; resolved model `UNKNOWN` (not exposed in the saved result).
- **Predeclared matrix result:** 5/5 scenario criteria passed; no safety/provenance guard failures. One owner-format deviation is separately noted below.
- **Important secondary observation:** the edit/elision response satisfies the matrix's state/elision/time criteria but returns a full 11-column 09 cut table for a concise scoped handoff. This is broader than the current 09 scoped-projection contract; count the response as semantic PASS with a field-projection note, not as proof of perfect owner formatting. Camera plan outputs also supplied proposed local labels (`S01`/`SH01`); these are not source IDs or archive claims.
- **Interpretation:** this demonstrates useful cross-domain application of existing owner guidance, not extraction of new universal methods from the unavailable Rofan archive, reliability, causality, or archive-wide coverage.

| Scenario | Grade | Observed evidence |
|---|---|---|
| `camera_action_timing` | PASS | 0–9s shot-local cue sequence aligns crank/grounds/camera phases; camera push-in starts with visible grounds, slows with hand stop, then holds; explicitly no lens or 3D verification. |
| `approach_stop_gait` | PASS | Separates 0–5 approach, 5–7 deceleration, 7–8 stop/settle, 8–10 prop placement; cropped foot plants remain hidden/unverified; no fixed gait cadence. |
| `nonverbal_hold_reaction` | PASS | Orders eye shift, head follow, visible breathing, then one small jaw/shoulder/finger change; no dialogue or invented cause/interiority; includes a playback QA check. |
| `edit_elision` | PASS with projection note | Marks kiln/wait as intentional elision, preserves before/after state, leaves elapsed time unknown, totals 45s. Uses existing fields but includes inactive full-template columns despite scoped request. |
| `negative_no_reference_or_skillification` | PASS | Gives an ordinary cracker handoff/continuity plan; no case retrieval, Rofan reference, archive analysis, or skill-update suggestion. |

## Exact prompts, context hashes, and raw outputs

### camera_action_timing

- Prompt SHA-256: `5d42a22d26da33ab2cf54f366f497f9ec057488b7d50757ca1615bf43137d625`
- System SHA-256: `3bd73ca730b6f3dd5f9fee245b684c39cd4f749161c81b5807b21677a71cdf96`
- Response SHA-256: `31e6140748a7d83b3ff3b8b1aac6b60480f6d4c7646d956af32f635c096c0b1b`
- Context: `video-production-assets/SKILL.md`, `references/contract.md`, `references/06-shots.md`, `assets/06-shots-template.md`, `references/27-camera-motion-qa.md`.
- Prompt: Plan a 9-second text-only 2D product film for a small hand-cranked coffee grinder: an adult turns the crank, the grounds fall into a cup, and the hand stops. Use a concise shot-local time basis to align the subject action and any motivated camera move; show when the camera begins/changes/settles only where useful. Keep the cup and grinder readable. This is a new proposal, not reference-footage analysis; do not invent lens measurements or 3D validation.

```text
## 블로킹·촬영·스토리보드 계획

- **목적:** 9초 텍스트 전용 2D 제품 필름 제안
- **가정:** 한 장면, 성인 한 명, 손크랭크식 그라인더와 컵이 한 프레임에 함께 보임. 카메라 동작은 제품과 분쇄물이 잘 읽히는 범위의 완만한 푸시인으로 제안하며, 렌즈·거리 수치는 지정하지 않음.
- **이미지·3D 검증:** 미제작. 실제 프레임 및 공간 검증 없음.

| shot_id | scene_id | beat_id | shot-local time (s or frames; FPS if frames) | 크기/카메라 위치 | 인물 블로킹 | 시선/축 | 공개 정보 | 관점·감정/구도 의도 | 대안·채택/승인 상태 | 카메라 동작 | 종료 프레임 | 핸들 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| SH01 | S01 | B01 | 0.00–9.00 s | 중간 와이드 제품 구도. 성인의 손·크랭크, 그라인더, 아래의 컵이 모두 계속 읽히도록 배치 | 성인이 크랭크를 돌린다. 분쇄물이 컵으로 떨어지는 동안 회전을 이어가고, 마지막에 손과 크랭크를 멈춘다. 컵은 그라인더 아래 위치를 유지한다. | 제품과 손 동작이 주 관찰 대상. 컵 입구와 분쇄물의 낙하 경로를 가리지 않음 | 크랭크 회전 → 분쇄물이 컵에 떨어짐 → 손이 멈추고 제품 구도가 안정됨 | 한 프레임에서 제품·행동·결과를 함께 읽히게 한다. 낙하가 시작될 때만 시선을 살짝 모으고, 멈춤 뒤에는 결과를 확인할 시간을 둔다. | 채택: 단일 연속 구도. 미승인 제안 | 시작은 고정. 분쇄물 낙하가 시작될 때 완만한 푸시인 시작; 낙하 중 유지; 손이 멈출 때 감속해 정지. 컵과 그라인더가 프레임에 계속 남도록 함 | 손이 멈춘 상태. 크랭크·그라인더·컵이 모두 읽히는 안정된 구도 | 시작 전 추가 편집 핸들은 미정 |

### Consequential moving-shot cue timeline — 제안

| Local time (shot seconds) | Actor phase / contact / visibility | Camera phase | Reveal / hold | Cut-out → cut-in phase |
|---|---|---|---|---|
| 0.00 | 손은 크랭크에 닿아 있음. 손과 크랭크의 접점이 보임 | 고정 구도 | 그라인더와 컵의 관계를 먼저 읽힘 | — |
| 0.50–2.00 | 성인이 크랭크를 돌리기 시작함. 회전 동작이 손과 함께 보임 | 고정 유지 | 동작 시작을 명확히 보여 줌 | — |
| 2.00–2.50 | 크랭크 회전 지속. 분쇄물이 떨어지기 시작함 | 분쇄물 공개에 맞춰 완만한 푸시인 시작 | 낙하와 컵 입구를 함께 보이게 함 | — |
| 2.50–6.60 | 회전 지속, 분쇄물이 컵으로 떨어짐 | 푸시인 지속하되 컵과 그라인더를 모두 프레임 안에 유지 | 낙하 결과가 읽히도록 유지 | — |
| 6.60–7.10 | 손이 회전을 늦추고 멈춤. 손과 크랭크의 정지 상태가 보임 | 푸시인 감속 후 정지 | 손이 멈추는 순간을 드러냄 | — |
| 7.10–9.00 | 손·크랭크 정지. 컵 안의 결과를 확인할 수 있음 | 고정 | 안정된 결과 구도 유지 | — |

**미확인 사항:** 제품의 실제 크기·형태와 분쇄물의 양·속도는 미제공이므로 미정.  
**다음 단계 인계:** 실행 전 제품 외형과 낙하 동작을 확인하고, 실제 제작 시 프레임에서 컵·그라인더·손의 가독성을 검수.
```

### approach_stop_gait

- Prompt SHA-256: `cb41c35a35493cafa3958e18cc21505243f230106f3daa5dc131135114061801`
- System SHA-256: `dd6569f5728b2330d9d6a9084a5a1b50c9306000a57768329eb2d1ed899592a8`
- Response SHA-256: `b3071b060bf336a9f3a5059a08b65243983ea3706af0302fc9f631f2b87a3d6b`
- Context: `video-production-assets/SKILL.md`, `references/contract.md`, `references/06-shots.md`, `assets/06-shots-template.md`, `references/08-animation.md`, `assets/08-animation-template.md`.
- Prompt: Plan a 10-second text-only documentary shot of a park maintenance worker carrying a watering can along a greenhouse aisle, slowing to a stop at a plant bench and setting the can down. The lower legs are outside the frame for the first half; no source footage is supplied. Give concise 06/08 movement cues that distinguish approach, deceleration, stop, settle, and the prop-placement action. Do not claim unseen foot plants or prescribe universal gait timing.

```text
## 06 — Blocking / Camera Plan

**Purpose:** Text-only documentary shot plan  
**Duration:** 10 s · **Assumption:** One continuous shot; exact greenhouse layout and worker/can details are unspecified. Lower legs remain out of frame from 0–5 s. No source footage supplied; all cues below are proposed, not observations.

| shot_id | scene_id | beat_id | shot-local time (s or frames; FPS if frames) | 크기/카메라 위치 | 인물 블로킹 | 시선/축 | 공개 정보 | 관점·감정/구도 의도 | 대안·채택/승인 상태 | 카메라 동작 | 종료 프레임 | 핸들 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| SH01 | S01 | B01 | 0–10 s | Medium-wide, aisle-level, framing worker, watering can, and plant bench; lower legs excluded until 5 s | Worker approaches along aisle carrying the can; slows beside bench, stops, settles, then places can on bench | Maintain aisle direction and readable relation between worker, can, and bench | Approach and carried can; then stopping and deliberate placement | Observational, unobtrusive coverage; keep the hand–can–bench interaction visible | Single continuous take — proposed, unapproved | Gentle tracking during approach; decelerate and settle to locked frame | Can rests on bench; worker’s hand releases it | Preserve a brief post-placement handle |

**Consequential moving-shot cue timeline — proposed**

| Local time (shot seconds) | Actor phase / contact / visibility | Camera phase | Reveal / hold | Cut-out → cut-in phase |
|---|---|---|---|---|
| 0–5 | Approach carrying can; lower legs out of frame. Foot plants/contact are hidden and unverified. | Track with worker at a steady, unobtrusive pace. | Keep worker and can readable. | — |
| 5–7 | Approach continues into deceleration beside the bench; do not infer unseen foot plants. | Ease tracking to a stop. | Bench and intended placement area remain visible. | — |
| 7–8 | Stop, then body and can settle before placement. Lower-body contact remains unverified if still obscured. | Camera settles and holds. | Allow the stop to read before the next action. | — |
| 8–10 | Prop placement: worker lowers can onto bench, releases it, and withdraws hand. | Locked. | Keep contact, release, and can’s resting position in frame. | — |

## 08 — Animation / Movement Cues

**FPS:** Not specified; cues are in shot-local seconds. No source footage is supplied.

| shot_id | 포즈/행동 | 시작 프레임 | 끝 프레임(미포함) | 행동선/무게 | 스페이싱 | 보조 동작 | 접촉 잠금 / 필요한 발 접촉의 가시 구간 또는 hidden·미확인 제한 |
|---|---|---:|---:|---|---|---|---|
| SH01 | Approach, carrying can | 0 s | 5 s | Forward travel; can supported in carry | Natural continuous movement; no fixed gait cadence prescribed | Can may respond subtly to movement | Lower legs outside frame; foot plants hidden/unverified |
| SH01 | Deceleration toward bench | 5 s | 7 s | Forward movement reduces before stopping | Gradually shorter travel; do not imply specific steps | Keep can controlled | Foot contact unverified while legs are obscured |
| SH01 | Stop and settle | 7 s | 8 s | Travel ends; body and carried can settle | Minimal residual motion, then stillness | Small balance adjustment only if visible | No unseen plant or weight transfer claimed |
| SH01 | Set can down and release | 8 s | 10 s | Hands lower can to bench; can’s weight transfers to surface | Controlled lowering; brief contact before release | Hand withdraws after release | Can–bench contact should be visible; exact hand placement unspecified |

**Unverified:** Actual worker gait, foot contacts, can weight/handle configuration, bench height, and precise timing are not established by footage. These are planning cues, not measured performance.
```

### nonverbal_hold_reaction

- Prompt SHA-256: `190c5ee98da47bf5d326e8d74998f6ab5fb1dd83ec829497550ea724659025ac`
- System SHA-256: `db36292086ee3c7bb15557e06e474cf65738d1d20b63982f46b60e8d7a59f30f`
- Response SHA-256: `8e16f0210803aca8338ba65b9f0df2419f80a22869cc6baadd82f89df4dcca8a`
- Context: `video-production-assets/SKILL.md`, `references/contract.md`, `references/04-performance.md`, `assets/04-performance-template.md`.
- Prompt: For a 6-second silent close shot in a coastal field station, a marine researcher notices a cracked sample vial on the desk. Direct a restrained nonverbal held beat that progresses through observable small changes instead of a frozen expression. No dialogue, internal thought, cause, or source footage is supplied. Give usable 04 performance cues and one observable QA check; label any interpretation as a proposal.

```text
## 04 연기·서브텍스트 디렉팅

**장면:** 해안 현장 연구소, 책상 위 금 간 샘플 바이알을 알아차리는 해양 연구자  
**길이:** 6초  
**오디오:** 무음 — 대사 없음 및 기타 오디오 없음으로 해석  
**가정:** 바이알과 연구자의 시선이 샷 안에 보인다.  
**해석 제안:** 이 비트는 바이알을 확인하려는 순간으로 연기할 수 있다. 이는 제안일 뿐이며, 파손 원인·감정·내면 생각은 설정하지 않는다.

| 구간 | 목표 / 행동 | 관찰 가능한 연기 큐 |
|---|---|---|
| 0–1.5초 | 하던 시선이나 자세를 유지한다. | 눈과 머리는 움직이지 않는다. 이미 진행 중인 동작이 있다면 작게 마무리한다. |
| 1.5–2.5초 | 바이알 쪽으로 주의를 옮긴다. | 눈이 먼저 바이알로 이동하고, 짧은 간격 뒤 머리가 소폭 따라간다. |
| 2.5–4초 | 금을 확인한다. | 시선을 바이알의 금 간 부분에 둔다. 보이는 호흡은 자연스럽게 이어가고, 손은 아직 뻗지 않는다. |
| 4–6초 | 반응을 보류한 채 관찰을 이어간다. | 턱이나 어깨에 작은 긴장이 생겼다가 유지되거나 풀린다. 손가락 하나가 책상 위에서 미세하게 멈추는 등 한 가지 작은 변화를 택한다. 마지막에는 시선이 바이알에 남는다. |

**배우 디렉션:** 감정을 표정으로 보여주려 하지 말고, “발견한 물체를 시선으로 확인하고, 손을 뻗을지 보류한다”를 수행한다. 미세 변화는 한 번에 하나씩만 더한다. 바이알에 손대거나 옮기지는 않는다.

**관찰 가능한 QA 체크:** 6초 재생에서 바이알을 향한 눈의 이동과 뒤따르는 작은 변화가 순서대로 읽히고, 그 사이 표정이 고정된 채 유지되지 않는가?

**미확인 사항:** 인물의 직전 동작, 바이알의 정확한 화면 위치, 샷 내 손의 가시성.
```

### edit_elision

- Prompt SHA-256: `75856fe31ab4daea48c8940ff430c4a146cabc35a16b323aa69ce442029b26fa`
- System SHA-256: `1e2ad74086d3dba6d90e8bd2579f5a6b91947db78c8c0c742cd25e804b98f5a6`
- Response SHA-256: `7e9a59af8b9376625c4d2b73361259c415c05ca0f9da935a7e06c56d1301f241`
- Context: `video-production-assets/SKILL.md`, `references/contract.md`, `references/09-edit.md`, `assets/09-edit-template.md`.
- Prompt: Create a 45-second text-only 2D short about a ceramic artist testing a glazed tile: show the tile before the kiln, then cut to a later cooled result; the actual overnight wait and firing are not shown and no elapsed-time figure is supplied. Give a concise cut/elision plan in existing 09 fields that distinguishes an intentional omission from continuous action, preserves before/after state, and keeps unprovided elapsed time unknown. Do not use or imitate a reference film.

```text
### 09 편집·리듬·사운드 — 컷/생략 제안

**상태:** 비실행용 타이밍 제안. 총 길이 45초. 샷·에셋 및 오디오 정보는 제공되지 않아 비워 둠.  
**오디오 의도:** 미지정. “text-only”는 텍스트 계획으로 해석했으며, 무음으로 가정하지 않음.

| cut_id | shot_id/asset_id | source_in_s | source_out_s | playback_rate | final_start_s | final_end_s | 행동·카메라 변화 / 컷아웃→컷인 phase·state + cue time | transition/duration_s | sound_id·sync anchor | reaction/settle hold final start–end s·연속성/검수 상태 |
|---|---|---:|---:|---:|---:|---:|---|---:|---|---|
| C01 — 타일 시험 전 | 미배정 | — | — | — | 0 | 20 | 작가가 유약을 바른 타일을 가마에 넣기 전 살펴본다. **컷아웃 상태:** 타일은 아직 가마 전이며 결과는 미확인. | hard cut / 0 | 미지정 | 18–20초: 시험 전 타일 상태를 읽히게 둠. 제안 |
| C02 — 냉각 후 결과 | 미배정 | — | — | — | 20 | 45 | **의도적 생략:** 가마 작업과 실제 대기 시간은 보여주지 않는다. 컷인에서 타일은 가마 작업 후 냉각된 결과로 제시한다. 작가가 결과를 살펴본다. | hard cut / 0 | 미지정 | 20–23초: 결과를 먼저 읽히게 둠. 23–45초: 작가의 반응·검토. 세부 동작 미지정 |

### 시간 압축·생략

| cut_id | 획득 방식: 연속배속/인터벌/몽타주/의도적 생략/미확인 | 실제 경과시간·촬영 구간·간격·공백(근거 위치) | 생략 전 상태 | 생략 후 상태 | 후속 컷 유지/리셋 조건 |
|---|---|---|---|---|---|
| C02 — 냉각 후 결과 | 의도적 생략(elision). 연속 액션이나 타임랩스로 표현하지 않음. | 미확인. 실제 대기 시간·가마 가열 및 냉각 과정은 제시된 정보가 없으며 화면에 표시하지 않음. | 가마에 넣기 전, 유약 타일의 결과 미확인. | 가마 작업 후 냉각된 타일. | 결과 컷에서는 냉각된 타일 상태를 유지. 추가 변화나 경과시간 표시는 제안하지 않음. |

**범위 메모:** 컷 시점과 구간은 45초 안의 제안 배분이지 측정된 편집 타임라인이 아니다. 실제 경과시간을 수치로 표기하거나 유추하지 않는다.
```

### negative_no_reference_or_skillification

- Prompt SHA-256: `f4241d8afc552baecef3b682ac00c0cc028e9e13a16efc444492934c7bddc17e`
- System SHA-256: `0fb3aa0e6b28c041f058a5ac4a619a6620a0736257875dc02984f0518c6c2986`
- Response SHA-256: `0c71d9410fe4ae73cce4f10dd8f27786654547797dd9bd5e3ad215334e62c92a`
- Context: `video-production-assets/SKILL.md`, `references/contract.md`, `references/25-reference-video-analysis.md`, `references/06-shots.md`, `references/rofan-craft-examples.md`.
- Prompt: Plan a 7-second text-only 2D scene of a baker placing sesame crackers on a cooling rack, brushing crumbs aside, and handing one cracker to a customer. There is no reference footage, no archive request, no saved-case reuse request, and no request to edit or improve any skill. Give a concise ordinary shot/continuity plan only.

```text
### 7-second shot plan

**Format:** Text-only, 2D; no reference footage. Times are proposed, not measured.  
**Continuity:** Baker works behind the counter; cooling rack stays between baker and customer. Cracker moves from rack to baker’s hand to customer’s hand.

| Time | Shot / action | Continuity notes |
|---|---|---|
| 0.0–2.5s | **Medium-wide, locked.** Baker places several sesame crackers on the cooling rack. | Keep the rack and both hands visible; crackers land flat without overlapping. |
| 2.5–4.0s | **Same shot.** Baker brushes crumbs off the counter beside the rack. | Brush crumbs away from the crackers; leave the rack in place. |
| 4.0–7.0s | **Same shot.** Baker picks up one cracker and offers it across the counter. Customer takes it; hold briefly on the completed handoff. | Track one cracker only. Baker releases after the customer has a secure hold; end with the cracker in the customer’s hand and the rack still visible. |

**Audio:** Not specified.
```
## Sixth-scenario extension — conditional 07 lighting reveal

This one-call extension adds an unrelated positive lighting brief to the existing smoke matrix; it does not replace or regrade the original five scenarios or any T13–T20 artifact. The source evidence motivating the owner gap is limited to casebank L03: two bounded observations (`430` ~65.532–76.943s and `d31` 2101.599/2101.683s) note gradual brightness/flare over held geometry; neither establishes a cut. This supports conditional planning only, not prevalence.

- **Calls:** 1 planned / 1 completed; fresh stateless `completion(prompt, model="default", system=package_context).wait()`; no retry/error.
- **Model:** selection `default`; resolved model `UNKNOWN` (not exposed).
- **Grade:** PASS, 4/4 predeclared scenario criteria; no source/equipment/exposure/focus claim.
- **Prompt SHA-256:** `9f8e7e5fadc66e0856e5683b9ed05d9661b55f7298b515eaa9494a0f9966fcdb`
- **System SHA-256:** `0a377b7da8894d849d19723c9b2deceb7428da68d1beaa417e5e1bc40628d261`
- **Response SHA-256:** `63c9f756f26fe1d3d330b8ed2e8a5ccb75f6f7336d3f692a92649d4ae7cebb00`
- **Context files and SHA-256:**
  - `video-production-assets/SKILL.md` — `e8a142dce547f07fb9a7539d90ff257d99b5871fa419dab6b6e470ae898432f3`
  - `video-production-assets/references/contract.md` — `7a7c0f2454e788d8ccd01f243a0ea5b30b8e64b0e970179b70e75376c18cd5ce`
  - `video-production-assets/references/07-lighting.md` — `210d6c3366437cbb4f6046f2207d851a2fc251464891d828ae7175d35d4553ff`
  - `video-production-assets/assets/07-lighting-template.md` — `d311833f2b41b026fa1d7f20a232b24e11b3522b7481f988751b53f9192adea7`
- **Prompt:** Plan an 8-second text-only 2D museum conservation shot: a restorer examines a translucent amber glass sample on a fixed dark slate board. In one held shot, a gradual brightness/flare change should make fine etched ridges become readable while the sample, board edge, framing, and geometric anchors stay held. No source footage is supplied, and no camera move or edit is requested. Give proposed shot-local start/change/settle/hold cues and use existing 07 lighting fields (such as matching notes/shadow rule). Do not infer a fixture, exposure, focus, or equipment from appearance; add no fields or universal timing.

**Manual grade against the matrix acceptance criteria:**

| Criterion | Grade | Evidence in response |
|---|---|---|
| Shot-local start/change/settle/hold phases; held framing/geometric anchors | PASS | Proposes start 0s, change 0–4s, settle 4–5s, hold 5–8s; says sample, board edge, framing and anchors remain fixed. |
| Information becomes readable; lighting remains within-shot, not camera/edit | PASS | Names the etched ridges becoming legible through gradual brightness/flare; keeps a fixed single shot and asks for no camera movement or edit. |
| Existing 07 fields; no new schema or universal timing | PASS | Fills the existing lighting-table columns, including shadow rule and matching notes; timing is labelled proposed and adjustable. |
| No unsupported fixture/equipment, exposure, or focus inference | PASS | Marks light direction, height, fixture, diffusion, key/fill, and exposure values unknown/unmeasured; makes no focus-mechanism claim. |

```text
| scene/shot | 광원 동기 | 방향/높이 | 경도/확산 | 색 의도 | 키/필 관계 | 배경 분리 | 그림자 규칙 | 노출 상태 | 매칭 주의 |
|---|---|---|---|---|---|---|---|---|---|
| S01/SH01 · 0–8초, 고정된 단일 샷 | 제안: 유리 표면의 점진적인 밝기/플레어 변화로 에칭된 미세 능선이 읽히게 한다. **start (0초):** 능선이 아직 뚜렷하지 않은 상태에서 시작. **change (0–4초):** 표면의 밝기/플레어를 서서히 변화시켜 능선의 가독성을 드러낸다. **settle (4–5초):** 밝기 변화를 안정시킨다. **hold (5–8초):** 능선이 읽히는 상태를 유지한다. 구간은 제안이며 테스트로 조정한다. | 미확인. 광원 방향·높이 또는 기구는 추정하지 않음. | 미확인. 광원 경도·확산은 추정하지 않음. | 어두운 슬레이트 보드 위 반투명 앰버 유리의 색을 보존한다. | 키/필 관계는 미확인. 외관만으로 추정하지 않음. | 유리 샘플이 어두운 보드에서 분리되어 보이되, 보드의 어두운 톤은 유지한다. | 보드와 샘플의 그림자·접촉 상태가 샷 동안 일관되게 유지된다. 변화가 새로운 그림자를 만들거나 고정된 기하 앵커를 흐리지 않도록 테스트한다. | 미측정 목표. 실제 노출값이나 조작 방식은 지정하지 않음. | 샘플, 보드 가장자리, 프레이밍 및 기하 앵커를 전체 8초 동안 고정한다. 조명 변화만으로 능선 가독성이 개선되는지 연속 프레임에서 확인한다. 변화 경계가 확인되지 않으면 광원 기구·노출·초점 메커니즘을 추론하지 않는다. |

**미확인 사항:** 시작/종료 밝기와 플레어의 구체적 모양·세기, 광원 특성, 실제 조명/노출 설정. 제안 큐는 영상 생성·촬영 결과가 아니라 계획.  
**다음 단계 인계:** 8초, 고정 구도, 단일 홀드 샷, 샘플·보드·기하 앵커 유지. 사용자 요청 외 카메라 이동이나 편집은 제안하지 않음.
```
