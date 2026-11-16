# 편집·리듬·사운드

project_id: {프로젝트}
version: {버전}
status: draft
라이프사이클 후반 단계 추적: {영화·단편 요청이면 `film-postproduction-template.md`의 단계/컷 버전 표에 artifact ID·버전으로 연결, 아니면 N/A}
assumptions: {가정}
오디오 의도(audio_mode·레이어)/실행자 지원 확인: {no_audio/no_dialogue/dialogue + SFX-only·음악제외·혼합참조 여부, 실제 지원 제어/확인 시점, 미지원 시 별도 제안 상태}

| 소싱 후보 | 출처/파일 ID·버전 | 기능·감정·길이·동기 기준점 | 권리 근거/확인 시점·제한 | 청취 결과 | 선택 |
|---|---|---|---|---|---|
| | | | | | |

| cut_id | shot_id/asset_id | source_in_s | source_out_s | playback_rate | final_start_s | final_end_s | 행동·카메라 변화 / 컷아웃→컷인 phase·state + cue time / 컷 이유 | transition/duration_s | sound_id·sync anchor | reaction/settle hold final start–end s·연속성/검수 상태 |
|---|---|---:|---:|---:|---:|---:|---|---|---|---|
| C01 | SH01 | | | 1.0 | | | | hard_cut/0 | | |

**필수:** 각 `cut_id`에 [전체 스토리라인 참조·연속성 게이트](../references/26-state-causality-continuity.md#storyline-continuity-gate)를 적용한다. 기존 `행동·카메라 변화 / 컷아웃→컷인 phase·state + cue time / 컷 이유` 셀에 선행 shot/artifact ID·버전과 관련 이력, planned/accepted 구분, 출구 상태 → 다음 입력 참조·시작 상태, 서사 관계·허용 델타/리셋을 연결한다(최초 컷은 정본 초기 상태). 실제 accepted 원본 ID·버전과 `source_in_s`/`source_out_s`·시간 basis·FPS/PTS를 연결하고, 기존 `reaction/settle hold final start–end s·연속성/검수 상태` 셀에 실제 out/in 프레임·인접 모션 검사 위치/관찰·판정·blocker를 기록한다. 실제 매체가 없으면 계획 참조와 `not produced`/unverified를 표시한다. `sound_id·sync anchor`에는 해당 오디오 연결을 유지한다. 전체 경계·재등장 검수와 최종 조립본 전체 정속/오디오 재생 증거는 기존 `검수 범위` 및 `delivery_checks`에 연결한다; 자세한 기록은 기존 QA artifact ID·버전으로 참조하고 새 열·스키마를 만들지 않는다.

스토리보드의 [장면 리듬과 감정 가독성](../references/storyboard-contract.md#장면-리듬과-감정-가독성)을 위 기존 컷 표에 연결한다. `컷 이유`에는 자극·공개·반응·선택과 진입/종료 계기, 동일 프레이밍 유지/반복의 기능을 적고, `reaction/settle hold final start–end s·연속성/검수 상태`에는 필요한 여운과 너무 이른/늦은 컷의 관찰 위치를 적는다. 씬별 요약은 06의 의도 표를 참조한다.

검수 범위: {텍스트 설계 / 실제 이미지 가독성 / 시간 재생 각각의 대상 버전·위치·관찰·미검증}. 시간 재생을 수행했다면 장면 전체를 따라 공개·반응 지연·hold·컷과 해당 음향을 대조한다. 계획만 있으면 제안 시간이며 재생 통과가 아니다.

카피와 행동/세계 변화의 연결을 검수할 때 새 pseudo-field를 만들지 않는다. `cut_id`마다 별도 행을 만들고 `final_start_s`/`final_end_s`에 해당 컷의 최종 타임라인 시작·끝 초를 각각 숫자로 기록한다; 여러 컷을 `C01–C02` 하나로 합치거나 값을 `0→3.5`처럼 두 시간 범위로 바꾸지 않는다. 실제 `행동·카메라 변화 / 컷아웃→컷인 phase·state + cue time`에 화면 사건·컷을 기록하고, 발화/음향 sync가 있으면 `sound_id·sync anchor`에 실제 근거를 연결한다. 컷·행동·카피 상태가 달라질 때만 기존 행을 나눈다; 카피나 audio cue를 브리프/제공 자료 없이 발명하지 않는다.

생성/수정/확장 클립을 편집할 때 기존 `source_in_s`/`source_out_s` 행과 QA 보고의 원본 ID·버전·시간 basis 및 클립 전체/선택 구간/편집 후 판정을 연결한다. 필수 사건 누락과 대체 커버리지를 명시하고, 원본 포함 확장 결과의 중복을 제거한다. 음성 국소 교정은 별도 트랙의 기존 sound_id 및 `performance-cue-template.md` 교정 기록을 연결하고 문장/장면/입/감정을 재검수한다. [실무 인계 R6/R7](../references/29-reference-driven-production.md#usable-ranges)의 해당 절만 적용하며 새 컷/오디오 스키마를 만들지 않는다.

### 시퀀스 리듬 대조 (곡선 선언 시)

[시퀀스 리듬 계약](../references/09-edit.md#시퀀스-리듬-계약)의 곡선을 실제 컷과 대조한다. 측정은 `scripts/measure_cut_rhythm.py`로 수행한다.

| rhythm_id | 계획 energy / cadence | 계획 길이 | 실측 길이(근거) | 차이 | 판정(재생 근거 필요) | 최소 수정 |
|---|---|---|---|---|---|---|
| RB01 | 2 / steady | 4.25 | 4.10 (ffmpeg scene 12컷) | −0.15 | UNVERIFIED → 재생 후 PASS_WITH_NOTES | 컷 OUT 2f 앞당김 |

숫자만으로 판정하지 않는다. `판정` 칸은 완성 시퀀스를 실제 재생한 근거가 있을 때만 `PASS`/`PASS_WITH_NOTES`/`NEEDS_REVISION` 중 하나로 채우고, 재생 전에는 `UNVERIFIED`로 둔다. 측정값은 판정의 근거가 아니라 수정 지점을 찾는 도구다. 리듬 곡선이 없으면 이 표는 `N/A`로 적는다.

### 시간 압축·생략 (해당 컷만)
| cut_id | 획득 방식: 연속배속/인터벌/몽타주/의도적 생략/미확인 | 실제 경과시간·촬영 구간·간격·공백(근거 위치) | 생략 전 상태 | 생략 후 상태 | 후속 컷 유지/리셋 조건 |
|---|---|---|---|---|---|
| | | | | | |

원본/출력 길이 비율만으로 playback_rate·촬영 간격·획득 방식을 확정하지 않는다. 근거 없는 항목은 `미확인`으로 둔다.


선택 큐는 `sound-cues.csv` 필드에 맞춰 기록; 권리·제한 상세는 mix_note/연결 artifact에 둔다.
미확인·권리 상태·재생/청취 범위: {목록}
다음 단계 인계: {입력 ID와 버전, 선택 실행기, 승인 상태}

행위별 권리 상세(실제 외부 파일 사용 시): {참조 색인의 표를 기존 `권리 근거/확인 시점·제한`/`mix_note` 또는 연결된 버전 문서에 기록; 열람·상업 작품·원본 재배포·생성기 업로드·AI 학습 각각의 근거/미확인. 기존 rights_status enum 유지}
