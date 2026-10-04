# 편집·리듬·사운드

project_id: {프로젝트}
version: {버전}
status: draft
assumptions: {가정}
오디오 의도(audio_mode·레이어)/실행자 지원 확인: {no_audio/no_dialogue/dialogue + SFX-only·음악제외·혼합참조 여부, 실제 지원 제어/확인 시점, 미지원 시 별도 제안 상태}

| 소싱 후보 | 출처/파일 ID·버전 | 기능·감정·길이·동기 기준점 | 권리 근거/확인 시점·제한 | 청취 결과 | 선택 |
|---|---|---|---|---|---|
| | | | | | |

| cut_id | shot_id/asset_id | source_in_s | source_out_s | playback_rate | final_start_s | final_end_s | 행동·카메라 변화/컷 이유 | transition/duration_s | sound_id·sync anchor | 연속성·검수 상태 |
|---|---|---:|---:|---:|---:|---:|---|---|---|---|
| C01 | SH01 | | | 1.0 | | | | hard_cut/0 | | |

### 시간 압축·생략 (해당 컷만)
| cut_id | 획득 방식: 연속배속/인터벌/몽타주/의도적 생략/미확인 | 실제 경과시간·촬영 구간·간격·공백(근거 위치) | 생략 전 상태 | 생략 후 상태 | 후속 컷 유지/리셋 조건 |
|---|---|---|---|---|---|
| | | | | | |

원본/출력 길이 비율만으로 playback_rate·촬영 간격·획득 방식을 확정하지 않는다. 근거 없는 항목은 `미확인`으로 둔다.


선택 큐는 `sound-cues.csv` 필드에 맞춰 기록; 권리·제한 상세는 mix_note/연결 artifact에 둔다.
미확인·권리 상태·재생/청취 범위: {목록}
다음 단계 인계: {입력 ID와 버전, 선택 실행기, 승인 상태}
