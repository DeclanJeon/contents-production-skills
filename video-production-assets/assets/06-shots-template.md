# 블로킹·촬영·스토리보드

project_id: {프로젝트}
version: {버전}
status: draft
assumptions: {가정}
board_purpose: {콘셉트 피치 / 촬영 실행 / 애니매틱 계획}
audience: {클라이언트·승인자 / 감독·촬영팀 / 기타}
approval_status: {제안 / 피치 승인 / 촬영 보드 승인}
deferred_execution_slots: {승인 후 결정할 샷 슬롯 ID 또는 없음}

| shot_id | scene_id | beat_id | 초 | 크기/카메라 위치 | 인물 블로킹 | 시선/축 | 공개 정보 | 관점·감정/구도 의도 | 대안·채택/승인 상태 | 카메라 동작 | 종료 프레임 | 핸들 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| SH01 | S01 | B01 | | | | | | | | | | |

## 패널별 ID 매핑 — project.json `storyboard.panels[]`의 투영

| panel_id | shot_id | beat_ids | visible_character_ids | audio_cue_ids | speech_ids | frame/time | 공개·유보·연속성 | image_asset_id |
|---|---|---|---|---|---|---|---|---|
| P01 | SH01 | B01 | CH01 | AU01 | SP01 | | | IM01 |

`beat_ids`는 해당 패널이 시각화하는 beat, `visible_character_ids`는 실제 화면에 보이는 인물만 쓴다. 패널 연결은 각 참조 shot의 관련 ID 부분집합이어야 한다. `frame/time`은 패널의 기준 시각이며 연결한 audio cue 및 speech의 시간 구간에 포함되어야 한다. 각 shot의 beat/audio/speech 참조는 해당 shot의 하나 이상의 패널에 직접 연결됐는지 확인한다.

미확인 사항: {목록}
다음 단계 인계: {입력 ID와 버전}
