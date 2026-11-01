# 컷·전환·음향 표현 선택표

편집·소리 선택이 필요한 요청에만 읽는다. [09 편집·사운드](09-edit.md)의 시간·소스·오디오 모드·권리·청취 절차가 정본이다. 카메라 카탈로그의 B17–24 ID/정의는 유지하며 이 문서는 실제 편집 인계 조건을 보완한다. X의 작성자 설명과 Eyecandy 분류는 탐색 자료이고 클립 전체 분석/효과 검증이 아니다. [참조 색인](production-reference-index.md)의 검사 범위와 권리 기록을 적용한다.

| 표현 | 선택 조건 / 필요한 자료 | 실패 조건·실제 검수 | 기존 09 인계 칸 |
|---|---|---|---|
| Match cut | 두 화면의 형태·방향·위치 또는 행동 단계 대응 | 컷아웃/컷인 대응이 읽히지 않음; 실제 전환 양쪽 프레임과 재생 확인 | 행동·카메라 변화 / 컷아웃→컷인 phase·state + cue time, transition/duration_s |
| Jump cut | 의도된 시간 생략·불연속을 드러냄 | 원치 않는 순간이동·소품 상태 리셋; 생략 전후와 후속 유지 확인 | 컷 이유, 시간 압축·생략 표 |
| Cross-cutting / parallel editing | 다른 공간/행동의 관계를 교대로 공개 | 동시성이 미확정인데 동시 사건으로 단정하거나 기능 없는 교대 | 컷 이유, final_start_s/final_end_s |
| Montage | 선택 단계·대비·시간 압축으로 관계를 전달 | 생략 단계·실제 경과시간을 발명, 필수 원인 제거 | 시간 압축·생략, source_in_s/source_out_s |
| Smash cut | 앞뒤 화면·소리 대비가 선택된 강조 | 대비 의도 없이 단순 hard cut을 효과로 과장 | 컷 이유, transition/duration_s, sound_id·sync anchor |
| Shot / reverse shot | 발화·듣기·관계·시선을 필요한 시점에서 읽힘 | 기계적 1대사=2컷; 축·시선·반응 계기 불일치 | 컷 이유, reaction/settle hold, 06의 시선/축 |
| J-cut / L-cut | 다음 소리의 선행 / 이전 소리의 잔류 | 시각 컷과 음향 경계 혼동·잘린 말·공간 점프 | sound_id·sync anchor, final time, sound-cues start/end |
| Dissolve / wipe / whip-pan transition | 시간/공간 연결 방식이 브리프에 필요 | 전환 중첩으로 총길이·읽기 시간 소실; whip은 촬영 무빙과 편집을 구분 | transition/duration_s, source handles, final time |
| Foley / material detail | 보이는 접촉·재질·힘을 소리로 구체화 | 다른 재질·주체·시점·접촉보다 빠른/늦은 사건 | layer, function, sync_anchor/sync_offset_s |
| Ambience / room tone | 공간과 컷 간 이어지는 청취 관점 | 역방향마다 채널 뒤집기·잔향/배경음 단절 | mix_note의 관점·위치·거리/잔향, fade |
| Music / silence | 선택된 감정·리듬·공개 기준 | 무음 요청에 음악 삽입, 단순 음악 존재로 기능 주장 | audio_mode·레이어, function, gain_db, mix_note |

## 예시를 실행 명세로 옮기기

기존 09 표의 `소싱 후보`, `출처/파일 ID·버전`, `기능·감정·길이·동기 기준점`, `권리 근거/확인 시점·제한`, `청취 결과`, `선택`을 채운다. 실제 없는 파일/ID/in-out은 미선택·미확인이다. 공급자 혼합 오디오에 없는 stem을 발명하지 않는다.

J컷을 제안하는 경우 시각 컷 시각과 다음 소리 시작을 별도로 적는다. 제안 오프셋은 측정값이 아니며 허용 오차는 브리프/합의 기준을 따른다. source time, final time, shot-local/generation-local time은 기존 시간 계약대로 변환한다. 네이티브 오디오는 지원된 같은 요청의 AUDIO 구획을 쓸 수 있고, 별도 파라미터가 없다는 이유로 외부 TTS를 자동 추가하지 않는다.

실제 전체 시퀀스를 소리와 함께 재생하고 필요한 무음/오디오 단독/경계 프레임 검사를 추가한다. 표본 프레임·오디오 스트림 메타데이터·자동 전사만으로 리듬·발음·공간음·믹스 통과를 주장하지 않는다. 권리 미확인은 해당 사용/업로드/게시 행위를 막고 자료 없는 설계는 진행한다. 소리의 서사 효과는 창작 의도이며 관객 반응 측정이 아니다.
