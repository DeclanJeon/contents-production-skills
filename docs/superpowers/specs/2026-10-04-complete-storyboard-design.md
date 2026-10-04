# 완전한 제작용 스토리보드 설계

## 목표와 범위

사용자 요구 2~13을 기존 콘텐츠 제작 스킬에 연결한다. 핵심 완료 기준은 **컷 이미지만 이야기 순서대로 보아도 승인된 시놉시스의 사건·인과·정보 공개·감정 변화가 읽히는가**다. 문서 필드 채움과 실제 이미지의 의미 검수를 분리한다. 이번 변경은 스킬·연결 계약·기계적 검증·이미지 컷 분할 도구이며 실제 작품 생성, Blender 설치, 음성 복제, 유료 제출, 게시가 아니다.

## 결정

- 총괄은 creative-production, 제작 원장은 project.json, 수치 좌표 원장은 camera_spec.json 그대로 유지한다. 새 스킬·전역 DB·공급자 기본값을 만들지 않는다.
- 일반 콘티/스토리보드 요청은 완전한 제작용 계획이 기본값이다. 명시적 서사 패널 연습·러프 비트 썸네일·이미지 프롬프트 단독 요청만 storyboarding-video의 좁은 텍스트 형식으로 처리한다. 전체 제작 메타데이터는 `video-production-assets/references/storyboard-contract.md`에 따라 포함한다. 텍스트 요청도 상세 항목을 채우되 실제 미디어·승인을 주장하지 않는다. 고정 패널 수가 필수 사건 가시화를 막으면 누락 대신 수량/스토리 충돌을 해결한다.
- 카메라/시간/음향은 전문 모듈이 작성하고 storyboard 담당자가 통합한다. narrative panel과 timed shot은 다른 단위지만 한 산출물에서 인덱스로 함께 조회할 수 있어야 한다.
- 완성된 이미지에는 인덱스를 이미지 바깥 결정론적 라벨로 붙인다. 생성 모델에 작은 글씨·정확한 ID를 그리도록 맡기지 않는다. clean cut은 라벨/테두리 없이 추출한다.

## 단계 계약

1. 제공된 주제·레퍼런스 URL·시놉·캐릭터 시트·음성·콘티를 재사용하고 버전/출처/검사 범위를 기록한다. 읽을 수 없는 자료는 미검증이며 재발명하지 않는다.
2. 주제/레퍼런스 선택 → 감정 여정 선택(유머/감동/교훈을 결과 감정과 구분하고 혼합 감정 허용) → 장르/목적/제작 방식. 알려진 선택은 재질문하지 않는다.
3. 길이 미정인 전체 제작에는 30초/1분/2분/5분/10분/30분/1시간 이내 또는 직접 길이를 제시한다. 챕터/단편/시리즈 여부도 확인한다. 일괄 위임이면 제안으로 표시한다. 장편을 짧은 블록 하나처럼 처리하지 않고 전체→챕터/회차→씬→샷으로 분해하며 전체 커버리지를 유지한다.
4. 시놉 전체 비트에 stable beat ID와 원문 위치를 부여한다. 인과/정보 순서, 목표 감정, 결말, 사실, 길이·제작 가능성을 QA하고 필요한 수정 후 재검수한다. 잠긴 시놉 변경은 승인/위임 범위로만 한다.
5. 캐릭터 외형·페르소나·행동·관계·보이스 프로필과 사용자 제공 시트의 적용 범위를 고정한다. 음성은 업로드/녹음, 합성, 가용 유사 음성 후보의 순서가 아니라 선택 분기다. 복제는 동의와 실제 기능 확인, 불가능하면 자동 대체하지 않고 후보 청취·승인을 받는다.
6. 대사/나레이션과 실제 또는 추정 시간, voice ID/연기, 립싱크 적용/비적용을 분리한다. 실제 음성 전의 시간은 추정이다. 무대사라고 반드시 나레이션을 추가하지 않는다.
7. 씬/샷마다 목적·비트·카메라 크기/앵글/프레이밍/무빙 시작끝·인물/소품 시작끝 상태·공간 배치·VFX 사용/미사용·발화·음향 큐·참조를 명시한다. 정확 좌표·거리·경로·다중 피사체 접촉/가림/축 문제 또는 Blender 요청이면 camera-spatial-design을 필수 적용한다. 실제 3D 검증 요청/필요 시 Blender로 동일 ID/명세를 인계한다. 런타임 부재는 미검증 blocker, 수치 분석은 Blender 검증이 아니다.
8. 전체 비트→씬→샷→필요 키패널(start/action_peak/end/hold) 매핑을 완료하고 슬롯 수·고유 이미지 수·시트 수를 계산한다. 사건/접촉/정보 변화의 정점이 필요하면 중간 패널을 추가한다. 정지 샷만 hold 하나를 허용하며 컷당 장수를 임의 고정하지 않는다.
9. SFX/BGM/환경/침묵을 타임라인 큐로 연결한다. 캐릭터·음향·VFX 미사용도 명시하며 미정과 비적용을 구분한다.
10. 실제 생성/권리/지출 승인을 확인한 뒤 필요한 이미지 전체를 생성·등록하고 이미지 외부의 stable index를 가진 시트와 clean cuts를 만든다. 텍스트만 요청하면 생성하지 않는다.
11. 모든 실제 이미지 컷을 설명/라벨/대사/음향 없이 순서대로 보아 사건·시선·점유 변화·정보 공개·감정이 읽히는지 검수하고 시놉 원문과 대조한다. 숫자 정보형은 승인된 숫자/그래픽 자체의 의미는 유지한다. 핵심이 읽히지 않으면 구도/행동/패널 분할을 수정하며 해설로 결함을 덮지 않는다.
12. KEEP/FIX/미검증을 panel/shot/beat ID로 분리한다. 수정 이유·최소 수정·보존 요소·추가 준비물·예상 시간 범위와 산정 근거(없으면 미정 및 필요한 측정)·담당·재검수 기준을 적는다. 승인된 범위 안에서 수정→재검수, 변경 영향만 stale. 모든 blocker 해결 전 complete/pass/영상 인계하지 않는다.
13. clean cuts를 빠짐없이 분할·재열기·순서 검수하고 첫/정점/끝 패널 ID, 실제 파일/해시와 shot local time을 후속 프롬프트에 인계한다. 모델의 입력 역할/길이/타임스탬프/오디오를 라이브 확인한다. Blender 경로/첫끝 프레임은 조건부이며 미지원 기능을 텍스트로 지원한다고 주장하지 않는다.

## 기계적 확장: 선택적 project.json storyboard 계약

기존 schema_version=1.1을 유지한다. 일반 plan/delivery는 변경하지 않고 상세 제작용 보드만 별도 `validate_storyboard.py`로 검사한다. 확장 필드는 project.json에만 정본으로 저장하며 CSV/시트는 투영본이다.

- `storyboard`: `{synopsis_artifact_id, beats, panels}`. synopsis_artifact_id는 현재 artifact ID다.
- beats: `{id, synopsis_locator, event, emotion}`. 배열 순서는 시놉의 이야기 순서다. 사건/정보/형식 비트 모두 가능하다.
- 기존 shot에 추가: `beat_ids`(비지 않은 배열), `camera` `{shot_size, angle, framing, movement, start, end}`(모두 비지 않은 문자열), `spatial` `{mode: numeric|not_applicable, artifact_id?, reason?}`, `vfx` `{enabled: bool, description}`, `speech` 배열, `audio_cue_ids` 배열. numeric은 수치 명세 artifact를 참조한다. 비적용은 이유 필수. VFX description은 미사용 이유도 기록한다.
- speech 항목: `{id, kind: dialogue|narration, character_id, text, start_s, end_s, voice_artifact_id, lip_sync: required|not_applicable, performance}`. character_id는 narration에만 null 허용, dialogue는 해당 shot 캐릭터 ID여야 한다. dialogue lip_sync는 required(화면 밖 발화는 not_applicable과 performance에 이유), narration은 not_applicable. voice_artifact_id는 실제/예정 텍스트 voice profile artifact를 참조하며 음성이 생성되었다는 뜻은 아니다. 시간은 shot 안에 있어야 한다. no_audio/no_dialogue는 speech=[]이다.
- panels: `{id, shot_id, frame_time_s, role: start|action_peak|end|hold, visual_action, reveals, withholds, continuity, image_asset_id}`. 문자열 설명은 비지 않아야 한다(해당 없음은 명시). 패널은 시간/이야기 순서로 배열한다. 변화 샷은 start/end, 정지 샷은 hold 또는 start/end. 첫/끝은 샷 시작과 마지막 실제 프레임이다. 모든 shot에 패널이 있으며 모든 beat/scene가 shot에 쓰인다. 비트 순서 역전은 승인된 시놉 배열 자체를 기준으로 검사한다.
- 이미지 계획은 planned asset의 ID로 기록, 실제 이미지는 available/verified, `--require-images --base-dir`에서는 파일/등록 상태를 검사한다. 승인·실제 시각 의미는 코드가 증명하지 못한다.
- 시트에서 추출할 panel에는 `source_sheet_asset_id`와 `crop_box=[left,top,right,bottom]`(정수 pixel, 오른쪽/아래 제외). clean image_asset_id는 planned 등록될 수 있으며 분할 도구의 실제 결과를 이후 등록한다.

## 컷 분할 도구

`split_storyboard.py project.json --base-dir ROOT --output NEW_DIR`는 Pillow를 사용한다. 각 panel의 source sheet 또는 기존 clean image를 읽고 매핑된 clean 파일을 순서대로 생성한다. 모든 입력/좌표/ID/경로/겹침을 출력 전에 검사하고 기존 output 디렉터리를 거부한다. source sheet별 crop 겹침, 이미지 밖/반전/비정수 crop, 누락 파일, unsafe panel ID를 거부한다. 파일명은 `0001_PANELID.png`; 결과 manifest는 조회·원장 등록용 파생 결과이며 새 원장이 아니다. 생성물은 실제 경로·hash·shot/beat/character/audio links를 포함하고 오류 시 성공으로 보고하지 않는다.

## 검증

- 기존 스킬 기반 5회 fresh-context 실행과 개선된 동일 요청 5회 실행을 보관한다. 서사 생성 결과는 실제 시각 검증이 아니다.
- permanent regression은 실제 누락 beat/scene/shot, 역전, 잘못된 참조/발화/시간, 없는 이미지, crop 범위/겹침/순서/overwrite 거부를 검증한다. 문서 문자열 확인 테스트는 만들지 않는다.
- CLI smoke로 valid 상세 보드와 deliberate missing beat를 검사하고 실제 합성 테스트 시트를 분할해 픽셀·순서·해시를 확인한다. 합성 픽셀은 작품 이미지의 스토리텔링 통과 근거가 아니다.
- 기존 전체 pytest, 패키지/스킬 버전 확인, 설치 동기화 가능 범위를 확인한다. Blender 및 실제 이미지 실행자의 부재/미실행을 명시한다.
