# 블로킹·촬영·스토리보드

project_id: {프로젝트}
version: {버전}
status: draft
assumptions: {가정}
board_purpose: {콘셉트 피치 / 촬영 실행 / 애니매틱 계획}
audience: {클라이언트·승인자 / 감독·촬영팀 / 기타}
approval_status: {제안 / 피치 승인 / 촬영 보드 승인}
deferred_execution_slots: {승인 후 결정할 샷 슬롯 ID 또는 없음}

## 씬별 카메라 의도와 리듬

완전한 제작용 보드는 [공통 계약 §2](../references/storyboard-contract.md#씬별-카메라-의도와-인접-씬-비교)의 씬당 한 행을 아래에 작성한다. 기존 scene/shot ID의 문서상 요약이며 새 원장/JSON 필드가 아니다. [장면 리듬과 감정 가독성](../references/storyboard-contract.md#장면-리듬과-감정-가독성)으로 설계·검수한다.

| scene_id / shot_id 목록 | 씬 목적 / 진입→종료 지식·감정 | 장면 리듬: 축적·변화·쉼과 shot/panel ID | 감정 가독성: 자극·변화·선택과 화면 거리 | 공간 관계: 시작→끝·의미 | POV·축 / 카메라 문법 | 무빙 동기 또는 static 이유 | 인접 씬 관계 / 재사용 이유 | 상태·증거 |
|---|---|---|---|---|---|---|---|---|
| S01 / SH01 | | | | | | | | |

## 샷 명세

| shot_id | scene_id | beat_id | shot-local time (s or frames; FPS if frames) | 크기/카메라 위치 | 인물 블로킹 | 시선/축 | 공개 정보 | 관점·감정/구도 의도 | 대안·채택/승인 상태 | 카메라 동작 | 종료 프레임 | 핸들 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| SH01 | S01 | B01 | | | | | | | | | | |

`인물 블로킹` / `카메라 동작`은 별도 기록한다. 둘 다 움직일 때만 같은 shot-local basis에 적용되는 move/change·reveal/contact·stop/settle·hold/cut 시각을 서로 맞춰 적는다; 미사용 큐는 생략한다. 결과·반응 hold가 필요하면 해당 샷 시간 안의 구간을 적는다. See `camera-spatial-design/references/motion-timing-lens.md`.

최종 handoff는 위 샷 표의 실제 열 이름을 그대로 사용한다: `shot_id`, `scene_id`, `beat_id`, `shot-local time (s or frames; FPS if frames)`, `크기/카메라 위치`, `인물 블로킹`, `시선/축`, `공개 정보`, `관점·감정/구도 의도`, `대안·채택/승인 상태`, `카메라 동작`, `종료 프레임`, `핸들`. 열을 새 pseudo-field나 paraphrase alias로 바꾸지 않는다. 하나의 연속 샷에 발화·반응을 담으면 실제 같은 프레임의 동시 연기 또는 시간에 따른 프레이밍/블로킹 변화로 어떻게 읽히는지 기록한다.

씬 리듬을 각 샷의 `관점·감정/구도 의도`, `공개 정보`, `종료 프레임`과 아래 cue로 구체화한다. 발화 ID별 화면 안/밖 화자와 필요한 반응의 근거/유보는 기존 행동·연기 설명에 연결한다. 컷 이유와 hold 구간은 `09-edit-template.md`의 기존 열로 인계한다.

제품-세계 형태 대응은 `공개 정보`, `관점·감정/구도 의도`, `카메라 동작`, `종료 프레임`에 실제 화면 anchor·크기·방향·가림·질감과 각 공개 시점을 적는다. inset/main-secondary 설계는 같은 기존 shot 행의 `공개 정보`와 `관점·감정/구도 의도`에 주/보조 시선·공개 순서를, 별도 shot이면 해당 shot IDs와 cue를 적고 09의 기존 cut/time 행에 연결한다. 한 shot의 시작/정점/끝에서 변화가 필요하면 아래 cue 표를 사용한다.

### Consequential moving-shot cue timeline (DESIGN_PROPOSAL example)

For every consequential walking/stop or camera-moving shot, return these cue rows populated as part of the shot plan. Use shot-local times within the owning shot's duration; actor and camera phases share that basis. Include applicable actor/camera onset, deceleration, stop and settle sub-intervals. In `Actor phase / contact / visibility`, state the visible foot-contact cue/window or mark it `hidden/out-of-frame` or `unverified`. In `Reveal / hold`, give reaction onset and a distinct hold start–end when used. For an action cut, pair out/in phases and their shot-local cue times here and in the existing 09 edit slot, keeping each cue within its owning final range. In the existing AI-handoff tool-support slot, write `UNKNOWN` until the actual endpoint control is checked; until then, camera direction remains a DESIGN_PROPOSAL. These are proposed values, not observations or universal gait timings.

| Local time (shot seconds) | Actor phase / contact / visibility | Camera phase | Reveal / hold | Cut-out → cut-in phase |
|---|---|---|---|---|
| 0.00 | Walk begins; feet visible, no contact claim yet | Track begins with actor | Path revealed; no hold | — |
| 0.00–1.20 | Approach; show foot plants/weight transfers only where visible in this frame | Track alongside; preserve spacing | Keep both actors readable | — |
| 1.20–1.50 | Decelerate; final plant and transfer to supporting foot visible | Track decelerates | — | — |
| 1.50–1.85 | Stop; planted feet remain visible, body settles | Track stops, camera settles | Hold begins after settle | — |
| 1.85–2.00 | Partner reaction begins after the stop | Locked | Reaction onset 1.85; hold not started | — |
| 2.00–2.55 | Settled mutual eyeline | Locked | Reaction hold 2.00–2.55 | SH01 out 2.55: settled look → SH02 in 0.00: reverse begins on matching eyeline |

## 패널별 ID 매핑 — project.json `storyboard.panels[]`의 투영

| panel_id | shot_id | beat_ids | visible_character_ids | audio_cue_ids | speech_ids | frame/time | 공개·유보·연속성 | image_asset_id |
|---|---|---|---|---|---|---|---|---|
| P01 | SH01 | B01 | CH01 | AU01 | SP01 | | | IM01 |

`beat_ids`는 해당 패널이 시각화하는 beat, `visible_character_ids`는 실제 화면에 보이는 인물만 쓴다. 패널 연결은 각 참조 shot의 관련 ID 부분집합이어야 한다. `frame/time`은 패널의 기준 시각이며 연결한 audio cue 및 speech의 시간 구간에 포함되어야 한다. 각 shot의 beat/audio/speech 참조는 해당 shot의 하나 이상의 패널에 직접 연결됐는지 확인한다.

미확인 사항: {목록}
다음 단계 인계: {입력 ID와 버전}
