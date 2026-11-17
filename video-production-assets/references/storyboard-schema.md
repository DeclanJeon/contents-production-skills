# 스토리보드 — 정본 JSON·리듬 스키마

상세 보드/rhythm JSON 작성·수정·관련 구조 오류 해결 단계의 정본이다. 일반 텍스트 보드의 필수 설계는 [core](storyboard-contract.md)+[direction](storyboard-direction.md)가 소유한다. 번호 §n은 core의 기존 절 번호다. 실제 이미지/납품은 각각 [media](storyboard-media.md)/[delivery](storyboard-delivery.md)를 적용한다.


## 8. 선택적 project.json 상세 보드 확장

schema_version=1.1을 유지한다. 상세 보드에서는 아래 필드를 작성하고 일반 프로젝트는 기존 plan/delivery 계약을 유지한다. 기존 상세 보드도 누락된 패널별 ID 연결을 채우기 전에는 새 validator/renderer를 통과하지 못한다. CSV/시트는 이 원장의 투영이며 서로 별도 수정하지 않는다.

- `storyboard`: `{synopsis_artifact_id, beats, panels, rhythm?}`. synopsis_artifact_id는 현재 시놉 artifact, `rhythm`은 선택 리듬 곡선(아래 [리듬 곡선 절](#리듬-곡선-storyboardrhythm-선택)).
- `beats`: 이야기 순서의 `{id, synopsis_locator, event, emotion}`. 전부 비지 않은 문자열. 제작용 연결 비트도 승인 시놉의 어느 행동을 시각화하는지 적는다.
- 기존 `shots[]` 추가 필드: `beat_ids`(비지 않은 유효 beat 배열), `camera={shot_size,angle,framing,movement,start,end}`(비지 않은 문자열), `spatial={mode:numeric|not_applicable,artifact_id?,reason?}`, `vfx={enabled:bool,description}`, `speech=[]`, `audio_cue_ids=[]`. numeric은 실제/예정 수치 artifact 참조, N/A는 사유 필수. 모든 씬/비트/샷을 사용하며 처음 등장하는 beat의 순서는 시놉 순서다. 여러 샷의 같은 비트와 정당한 여러 비트 연결은 허용한다.
- `speech[]`: `{id,kind:dialogue|narration,character_id,text,start_s,end_s,voice_artifact_id,lip_sync:required|not_applicable,performance}`. 대사 화자는 shot의 캐릭터; narration에만 null 가능. voice_artifact는 profile/선택/실제 음성의 구분된 상태다. dialogue는 required 또는 화면 밖 등 N/A 사유를 performance에 명시; narration은 N/A. 발화 시간은 해당 shot 안이고 no_audio/no_dialogue에서는 배열이 빈다. 정확 립싱크는 실제 음성과 영상 검수로 확인한다.
- 시놉 pointer는 synopsis/script/beat_map artifact, 음성 pointer는 voice_profile/voice/voice_recording/voiceover artifact, numeric 공간 pointer는 camera_spec/spatial_spec artifact여야 한다. 존재하는 다른 종류의 ID만 연결해서는 통과하지 않는다.
- 등록된 camera JSON을 `--base-dir`에서 얻으면 프로젝트/내용 버전, scene/shot, fps·local frame 길이와 subject 연결을 함께 검사한다. 샷 일부만 포함한 spec은 허용하지만 그 artifact를 참조하는 numeric 샷은 빠질 수 없다. 실제 이미지 인계의 numeric 공간은 등록된 JSON 파일이 필요하며, 계획의 미생성 파일/렌더링/의미 검수는 별도 미검증이다.
- `panels[]`: 이야기/시간 순서의 `{id,shot_id,beat_ids,visible_character_ids,audio_cue_ids,speech_ids,frame_time_s,role:start|action_peak|end|hold,visual_action,reveals,withholds,continuity,image_asset_id}`. 네 ID 필드는 모두 배열이며 생략할 수 없다. `beat_ids`는 비어 있지 않아야 하고 연결된 shot의 `beat_ids` 부분집합이다. `visible_character_ids`는 실제 그 패널에 보이는 characters이며 연결된 shot의 `character_ids` 부분집합이다. `audio_cue_ids`는 해당 패널의 음향 맥락, `speech_ids`는 해당 패널과 연결된 발화를 가리키며 각각 연결된 shot의 ID 부분집합이다. `frame_time_s`는 샘플 프레임이며 음향·발화의 기준 시각이다. 각 shot의 모든 `beat_ids`, `audio_cue_ids`, `speech[].id`는 해당 구간과 시간상 겹치는 그 샷의 패널 중 하나 이상에 직접 연결돼야 한다. 캐릭터 없는 패널/작품은 `visible_character_ids: []`를 쓴다. 설명 문자열은 비지 않아야 한다(N/A도 명시). 첫 프레임은 shot.start_s, 끝은 shot.end_s-1/fps. 변화 샷에는 start/end, 동일 상태 정지 샷에는 hold 또는 start/end. action_peak 추가 필요성은 의미 검수로 판단한다.
- `image_asset_id`는 planned/actual asset ID. 실제 인계에는 available/verified 파일이 필요하다. 시트 crop 패널은 추가로 `source_sheet_asset_id`, `crop_box=[left,top,right,bottom]`(정수 pixel, 우/하 제외)을 둔다. crop은 해당 source의 실제 범위 안이고 서로 겹치지 않는다.
- `panels[]` 선택 필드 `asset_version_refs: {asset_id: version}`은 패널이 사용하는 잠긴 에셋의 정확한 버전을 핀한다. board가 `finality: final`이면 모든 패널에 필수이며 그 샷의 `asset_ids` 전부와 활성 `look_asset_id`를 포함해야 하고, 버전 드리프트·stale 참조는 구조 검사가 거절한다. stale 보드의 패널은 이전 핀 버전을 보존할 수 있다.
- `panels[]` 선택 필드 `expression_pose`, `focal_hierarchy`, `kinetic_cues`, `image_prompt`는 정지 이미지의 단일 프레임 가독성·동세·표정·이중 프롬프트를 담는다. 넷 다 비지 않은 문자열이며, 존재할 때만 형식 검사하고 **없어도 통과하는 하위 호환 필드**다. `--strict-staging`에서는 넷 다 필수이고 비공백이어야 한다. 형식과 서술 규칙의 정본은 §3의 [동작 중심 패널의 장면 통합](storyboard-direction.md#동작-중심-패널의-장면-통합)이고, 이 항목은 그 필드들이 `panels[]` 스키마에 속함을 선언할 뿐 규칙을 다시 쓰지 않는다. `storyboard-panels.csv`와 `06-shots-template.md`는 이 스키마의 투영이다.
- 합본 시트 에셋(`kind=storyboard_sheet`)은 `panel_ids`(이야기 순서)와 `sheet_index`/`sheet_count`를 가지며 한 시트 최대 8패널이다. 렌더러 `--panels-per-sheet 1..8`로 정보 밀도에 맞춰 줄인다. 등록된 시트가 전체 패널을 빠짐없이 순서대로 덮어야 한다. 전체 패키지는 `preproduction.storyboard_sheet_artifact_ids` 배열로 연결하며, 한 장도 배열로 기록한다. 생성 직후 실제 시트에서 장면·패널 이미지를 분리하고 등록된 `storyboard_split_asset_id`로 추적한다.


### 리듬 곡선 `storyboard.rhythm` (선택)

`storyboard.rhythm` 선택 필드: 시퀀스 리듬 곡선 `{intent, curve}`.

- `intent`: 비지 않은 문자열. 곡선 전체의 한 줄 의도.
- `curve[]`: 비지 않은 배열. 각 항목은 `{id, beat_ids, shot_ids, energy, cadence, planned_duration_s, cut_out_phase, exit_handle_frames, reason}`이고 **샷 1개가 아니라 리듬 구간 1개**를 나타낸다.
- `id` 고유 비지 않은 문자열, `beat_ids`/`shot_ids` 비지 않은 배열(`storyboard.beats`·`shots` 실존 ID), `energy` **1–5 정수**(이 프로젝트 안의 상대값이며 절대 척도가 아니다), `cadence` ∈ `steady|accelerando|ritardando|brake|peak|release`, `planned_duration_s` 양수, `cut_out_phase` ∈ `pre_action|mid_action|impact|reaction|settle`, `exit_handle_frames` 0 이상 정수, `reason` 비지 않은 문자열.
- 커버리지: 모든 shot은 **정확히 1회**, 모든 beat는 **1회 이상** 덮는다. 한 beat가 여러 샷·여러 구간에 걸치는 것은 허용한다. 각 항목의 `beat_ids`는 자기 `shot_ids`의 beat 합집합의 부분집합이다.
- 순서: 각 항목의 커버 샷은 타임라인(`start_s`) 오름차순이고 항목 간 구간은 겹치지 않는다. 합계: `abs(planned_duration_s - Σ(end_s - start_s)) <= max(1/fps, 0.05)`.
- 핸들 선언 하한: `cut_out_phase`가 `mid_action`/`impact`이면 `exit_handle_frames >= 2`이고, 이 하한은 그 항목 `shot_ids`의 **마지막 샷**(실제로 컷이 나가는 샷)에 적용된다.
- 존재할 때만 위 구조·커버리지·합계·순서·핸들 선언을 검사하는 **하위 호환 필드**다. `--strict-rhythm`에서는 존재 자체가 필수다. 검사기가 **에너지 곡선의 단조·다양성·품질을 판정하지 않는다**.


#### 리듬 필드의 소유 경계와 우선순위

- **사실값**(실측 시각, 실제 핸들 용량, 실제 클립 상태)은 `09` 컷 표·`asset_registry`·클립이 정본이다. 곡선은 사실을 주장하지 않는다.
- **계획 의도**(에너지·케이던스·계획 길이·컷 이탈 국면)는 `storyboard.rhythm`이 정본이다.
- `09`의 `컷아웃→컷인 phase·state + cue time`은 **컷별 실행 기록**, 곡선의 `cut_out_phase`는 **구간 요약 의도**이며 구조 검사는 둘을 대조하지 않는다. 문서 간 같은 숫자를 두 번 입력하지 않는다.

| 문서 | 소유 범위 | `rhythm` 취급 |
|---|---|---|
| 이 문서 §8 | 스키마 선언 | 정본 — 필드 소속·필수 여부 |
| [direction: 장면 리듬·수락 검사](storyboard-direction.md#장면-리듬과-감정-가독성) | 해석 원칙 | 정본 |
| [`assets/06-shots-template.md`](../assets/06-shots-template.md) | 설계 출력 양식 | 정본 — 곡선 표 |
| [`assets/09-edit-template.md`](../assets/09-edit-template.md) | 검증 출력 양식 | 정본 — 계획 vs 실측 대조 표 |
| [`09-edit.md`](09-edit.md#시퀀스-리듬-계약) | 실행 절차·기본값·측정 경로 | 정본 |
| [`06-shots.md`](06-shots.md) | 컷 설계 원칙 | 비소유 — 에너지 배분 cross-ref만 |
| `scripts/validate_storyboard.py` | 구조 검증 | 구조·커버리지·합계·순서·핸들 선언만 |
| `scripts/measure_cut_rhythm.py` | 실측·대조 | 측정·차이·관찰만, 판정 금지 |

> 검증 시 주의: `06-shots.md`에 `rhythm` 필드가 없다는 사실을 결함으로 보고하지 않는다. 스키마 완결성은 이 절과 템플릿 2종·검증기의 정합으로만 판정한다.


### 연결 예시 — 실제 이미지가 아니라 계획 표

| 원문/beat | scene/shot | panel/순간 | 눈으로 보일 증거 | 캐릭터/음향/VFX |
|---|---|---|---|---|
| 문단1 문장1/B01 장갑 발견 | S01/SH01 | P01/start | 창가에 놓인 빨간 장갑, CH01의 빈손 | CH01 / AU01 환경 / VFX 미사용 |
| 같은 원문/B01 | S01/SH01 | P02/end | CH01 시선이 같은 장갑에 멈춤 | 위 연결 유지 |
| 문단1 문장3/B03 반환 | S02/SH03 | P07/start, P08/action_peak, P09/end | CH01만 점유→두 손 접촉→CH02만 점유 | CH01·CH02 / AU02 천마찰 / 발화 N/A |

실제 프로젝트에는 중간 B02 등 **전체 비트 행**도 작성한다. 일부 행 예시는 전체 스토리보드로 인계하지 않는다.
