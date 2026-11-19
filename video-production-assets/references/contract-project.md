# 공통 제작 계약 — 정본 프로젝트

기존 원장 등록/수정·스키마 작성·관련 오류 해결 때 적용한다. 최소 인계는 [core](contract-core.md), 실제 전체 이미지 패키지는 [package](contract-package.md), 파일 패키징/납품은 [delivery](contract-delivery.md)를 적용한다. 실행 절차의 정본은 [sequence-execution](sequence-execution.md)이다.

## JSON 구조
필수: project_id, version, target_duration_s, fps, aspect_ratio, scenes, characters, shots, claims, artifacts.
scenes: id, purpose. characters: id, locked_traits.
shots: id, scene_id, character_ids, start_s, end_s, source_duration_s, purpose, start_state, end_state.
claims: id, statement, kind(fact/inference/fiction), source(실제 문서/데이터 위치), status(unverified/verified/fiction).
artifacts: id, type, version, status, dependencies(artifact id 배열), evidence(검수 위치; verified 상태 필수).


## Worker 조회와 원장 갱신

- `python scripts/project_index.py <project-root>/project.json --shot SH06` 또는 `--artifact A01`: 정본에서 현재 샷의 scene/character/beat/panel/voice/audio/claim/asset와 provenance·artifact dependency를 읽는 **읽기 전용 조회**. 샷/산출물을 지정하지 않으면 전체 원장을 자동 로드하지 않는다. 결과는 전체 브리프나 실행 승인 대신 사용할 수 없다.
- focused `project_index.py` 전달에는 panel pins, `required_asset_versions`, `master_asset_ref` 전체 계보, 활성 `look_asset_id`와 해당 에셋을 포함하고 무관한 샷/산출물은 제외한다.
- `python scripts/update_project.py <project-root>/project.json --update update.json`: **총괄 전용**, 구조가 유효한 기존 원장의 upsert 도구. 입력은 `{project_id, base_version, version, input_versions, owner_artifact_ids?, changes, storyboard?, preproduction?}`. changes는 기존 테이블 이름→부분 레코드 배열이며 기존 ID의 미변경 필드는 보존한다. storyboard는 synopsis_artifact_id와 beats/panels upsert, preproduction은 아래 패키지 포인터의 부분 갱신만 지원한다. 생성/삭제·프로젝트 선택·임의 헤더 변경·승인 추론은 하지 않는다. `project.target_duration_s`는 현재 승인된 edit_plan의 timing_policy와 입력 버전을 소비하는 유연 편집에서만 갱신하며, shots·관련 패널/rhythm·cue/자막·소유 버전을 같은 후보로 검사한다.
- 내용 레코드(씬/인물/샷/주장/에셋/오디오/자막/보드)를 바꾸면 패킷에서 배정한 `owner_artifact_ids`와 신규/증가한 소유 artifact 버전을 함께 준다. 상태·증거만 갱신할 때 내용 버전을 억지로 바꾸지 않는다. 소유 관계와 사용자 권한은 총괄이 실제 문맥에서 판단한다; 도구가 진위를 인증하지 않는다.
- 업데이트 도구는 base/input 버전, 레코드 참조/시간, 파일 루트, 후보 전체 구조를 확인한 뒤 같은 폴더 임시 파일→원자 교체한다. 협력 작성자 lock과 교체 전 원본 재확인으로 오래된 결과·중복 작성·관찰된 외부 수정을 거부한다. 기존 lock을 자동 제거하거나 재시도하지 않는다. 비협력 편집기의 마지막 순간 경합/정전 내구성까지 보장하는 DB는 아니다.
- 상위 버전 변경은 실제 dependency 그래프를 따라 stale을 전파한다. stale artifact는 **이전 입력 버전**을 보존할 수 있으나 현재 승인/실행에 쓰지 않는다. 현재 버전으로 다시 만든 레코드는 명시적으로 등록하고 재검수한다. 독립 승인과 정상 컷은 보존한다.
- `storyboard.panels[].asset_version_refs`의 버전 변경은 해당 에셋이 `required_asset_versions`에 없어도 보드 artifact의 입력 변경이다. 그 보드와 실제 종속 downstream만 stale 처리하고 과거 핀은 그대로 보존한다. 무관한 분기는 현재 상태를 유지한다.

공급자 upload/job/Soul/site/folder ID와 URL은 외부 locator이며 canonical asset ID가 아니다. 실제 파일을 얻고 등록한 available/verified asset만 result_asset_id로 쓴다. Brandkit 상태·blocks.json·camera_spec.json·분할 manifest는 각각 domain authority/파생 adapter로 연결하고 project.json과 경쟁하는 전역 원장을 만들지 않는다.


## v1.1 구조와 검사 프로필
`schema_version`은 `1.1`을 사용한다. 이전 `1.0` 입력도 일부 호환되지만 새로운 프로젝트는 v1.1 필드를 작성한다.

카메라·공간 명세를 연결할 때는 [카메라 공간 계약](../../camera-spatial-design/references/spatial-contract.md#json)의 별도 `schema_version=camera-spatial-1.0`을 사용한다. `camera-spatial-design/scripts/spatial_spec.py`가 이 문자열을 검사한다. 프로젝트 schema `1.1`, 카메라 schema `camera-spatial-1.0`, 각 artifact의 내용 `version`은 서로 다른 필드다. 카메라 schema `0.9`를 임의 수락하지 않으며, 프로젝트 `1.0`의 기존 호환 입력 허용을 새 프로젝트의 `1.1` 계약 충족으로 보고하지 않는다.

- plan: 필수 제작 정보·시간·참조·상태 기록을 검사한다. 생성 전 자료와 source_duration_status=estimated를 허용한다.
- preproduction: 저장한 전체 패키지의 필수 산출물·실제 Markdown/이미지·전체 보드·인물 페르소나/SSOT·참조와 해시를 검사한다. `--base-dir` 필수, 이미지 모드에는 Pillow 필요. 예술성·동일 얼굴·권리·사용자 승인 진위를 인증하지 않는다. plan 성공은 이 준비 완료 판정을 대신하지 않는다.
- delivery: plan 검사에 실제 파일 존재·해시·측정 시간·열린 blocker·납품 검사 기록을 추가한다. `--base-dir`을 프로젝트 폴더로 지정한다. 파일 재생, 디코딩, 음량 측정, 사실의 진위나 동의의 진위는 이 코드가 확인하지 않는다.
- 필수 테이블 scenes/shots/artifacts는 비어 있으면 안 된다. 등장인물이 없는 영상은 characters=[]를 허용한다.
- scene.purpose는 장면 기능, character.locked_traits는 문자열 또는 비어 있지 않은 목록/객체로 기록한다.
- target_duration_s와 shot.start_s/end_s는 fps 기준 프레임 경계에 맞춘다. 초는 실수로 허용하고 반올림 오차를 제한한다.
- shot.source_duration_status: estimated/measured. 계획의 원본 길이는 추정이며 실제 생성/촬영 후 측정한다.
- shot.source_in_s는 선택 테이크의 소스 시작 초, playback_rate는 소스 초/최종 초(기본 1). 배속·슬로모션에서 필요한 소스 길이는 source_in_s+(end_s-start_s)*playback_rate다.
- `playback_rate`는 **샷당 스칼라 하나**다. 한 샷 안에서 속도를 바꾸는 램프·리매핑은 같은 동작을 인접 shot(또는 09의 연속 cut 행)으로 분해하고 각 행에 상수 rate를 적는다. 배열·곡선·키프레임 목록을 이 필드에 넣지 않으며 검증기가 거부한다. 편집기에서 실제 램프를 적용했다면 그것은 출력 검수 항목이지 계획 JSON의 값이 아니다.
- shot.asset_ids는 asset_registry의 선택된 참조 ID 목록이다. 프롬프트의 경로·룩·의상·소품은 CSV 연속성 원장과 맞춘다.
- artifact.dependencies는 ID 목록이고 dependency_versions는 **정확히 그 ID들**의 {artifact_id: 입력 버전} 객체다. 선언되지 않은 키는 오류다. 현재 산출물은 상위 버전과 일치해야 하고, stale 산출물만 과거 입력 버전을 보존할 수 있다.
- approved artifact는 approval={by, at, evidence}를 기록한다. 승인자·시간·근거는 실제 기록을 사용한다. 생성/검증 산출물에는 asset_ids, verified에는 evidence가 필요하다.


## 시퀀스 실행 투영과 편집 시간 권한

[시퀀스 실행](sequence-execution.md)은 기존 generation_spec/edit_plan/qa_review의 `sequence-execution/1` 파생 문맥을 사용한다. 새 root 원장이나 프로젝트 상태 enum이 아니다. owner·입력 버전/해시·원문 요구·프레임 구간·연결·실제 검사 근거를 묶고 실제 다음 입력과 편집 실행기가 소비한다. `ready`는 기록·구조 준비이지 미감 인증·실행 허가가 아니다.

승인된 실행/편집 artifact의 선택 메타데이터 `execution_scope={shot_ids:[...],operations:[generation|edit|export]}`는 실제 승인 범위를 구조화한다. `edit_plan.timing_policy={duration:fixed|flexible,anchors:[{table,id,field,frame}]}`는 원래 승인된 시간 제약이며 새 delta가 자기 권한을 만들 수 없다. `update_project.py`는 target_duration_s 및 필요한 storyboard.rhythm 교체를 제한적으로 지원하고, 고정 anchor·후속 시간/참조·owner 버전·원자 저장 검사를 유지한다. 실제 사용자 승인과 검수 진위는 코디네이터 책임이다.

일부 샷만 별도 납품하는 현재 승인된 편집 계획은 `execution_scope.deliverable: shot_subset`으로 명시한다. 누락된 전체 영화 컷을 면제하지 않는다.


## 실제 파일과 부가 시간표
- asset_registry: {id, kind, version, path, status, sha256}. 실제 path는 프로젝트 폴더 기준 상대 경로를 권장하며 `--base-dir` 검사에서 resolve한 결과가 그 폴더 밖이면 거부한다(절대 경로/..//symlink 포함). planned는 path=null을 허용한다. available/verified는 실제 경로를 갖고 base-dir가 있으면 파일 존재와 제공된 해시를 확인한다. 최종 파일에는 verified와 SHA-256이 필요하다.
- asset_registry 선택 provenance 필드(있을 때만 채운다): entity_type(character/product/prop/location/wardrobe/look/lighting/graphic/environment), entity_id, authority(authoritative/inferred/derived), source_asset_ids, prompt, provider, model, workflow, result_asset_id. 사용자가 준 SSOT·바이블은 authoritative로 기록하고 임의로 변경하지 않는다. 확인되지 않은 provider/model을 기록하지 않는다.
- source_asset_ids/result_asset_id는 실제 asset_registry ID를 참조한다. entity_id가 있으면 비어 있지 않은 문자열이어야 하고 entity_type=character는 characters의 ID와 일치한다. 캐릭터 Identity Sheet A의 source_asset_ids에는 해당 캐릭터 SSOT artifact의 유일한 Markdown asset ID가 반드시 포함된다. 다른 entity_id는 해당 전문 바이블 locator로서 실제 소스를 인계하며 새 임의 테이블을 강제하지 않는다. shot.claim_ids가 있으면 claims의 실제 ID를 참조한다.
- shot.retry_budget: 최초 생성 이후 허용된 최대 재시도 수(선택, 0 이상 정수). 승인된 video_execution_plan의 상한에서 온다. 0이면 최초 1회만 허용하고 attempt의 최대값은 1+retry_budget이다. 필드 부재는 무제한 실행 허가가 아니다.
- generation_attempts: {id, shot_id, attempt(최초=1, 이후 샷별 중복 없는 양의 정수), route, model?, changes?, observed_failures?, preserve?, result(accept/reject/conditional), result_asset_id?, failure_class?, notes?}. 실제 시도만 기록한다. accept는 available/verified인 실제 결과 에셋 ID를 참조해야 하며 planned 에셋을 성공 결과로 기록하지 않는다. 기록/구조 검사 자체가 실행 승인이나 미디어 품질 검사는 아니다.
- audio_mode: no_audio / no_dialogue / dialogue. audio_cues: {id, start_s, end_s, layer, shot_id?, asset_id?}. 소리는 겹칠 수 있지만 전체 영상 구간을 벗어나지 않는다.
- captions: {id, start_s, end_s, text, shot_id?}. 오디오 음소나 자막 타이밍의 의미 적합성은 실제 재생으로 검사한다.
- issues: {id, severity: blocker/major/minor, status: open/resolved, evidence?, fix?}.



## 프리프로덕션 검토와 영상 실행 승인
[프리프로덕션·검토 절차](preproduction-review.md)의 `review.md`는 `type=preproduction_review` artifact로 등록하고 검토 대상의 ID·버전을 dependencies/dependency_versions로 연결한다. 실제 사용자 수락 때만 approved와 approval 근거를 기록한다. 문서·이미지의 generated/verified 상태는 사용자 수락을 뜻하지 않는다.

별도 `type=video_execution_plan` artifact는 승인된 검토 패키지 버전과 명시적 샷·모델/endpoint·실행/재시도/비용 상한을 참조한다. 실제 사용자 실행 승인 뒤에만 approved로 기록한다. 프리프로덕션 중 모델/가격 미정은 허용하지만 실행자 기본값으로 보충하지 않는다. 변경된 에셋의 종속 검토/실행 계획은 stale로 표시하고 새 버전에 이전 승인을 재사용하지 않는다. 사용자 승인과 파일 존재/구조 검사는 별개의 증거다.
approved 영상 실행 계획은 dependency 그래프에 현재 approved인 preproduction_review를 반드시 포함한다. 이 구조 검사는 실제 사용자 권한·비용·음성/이미지의 품질을 인증하지 않는다.

프리뷰와 최종은 별도 허가다. `video_execution_plan`의 승인 범위에 프리뷰 단계가 포함되면 승인된 프리뷰 입력 버전·설정·샷/출력 수·상한을 그대로 기록하고, 프리뷰 승인만으로 최종 생성·추가 과금을 허가하지 않는다. 프리뷰 실제 출력·검수 결과·수락 근거는 연결된 artifact(result_asset_id, generated/verified, evidence)로 남기고, 승인된 최종 계획은 프리뷰 판정과 최종 승격 경로를 dependencies로 참조한다. 프리뷰와 최종 범위를 하나의 plan 버전으로 함께 승인한 경우에만 최종이 같은 승인 안에서 현재 입력 버전·조건·상한으로 진행되며, 그렇지 않으면 현재 버전의 별도 최종 승인이 필요하다. 같은 seed·입력의 재생성은 같은 동작·정체성을 보장하지 않으므로 최종본은 다시 검수한다.


## 선택적 상세 스토리보드 확장
제작용/상세 콘티와 전체 보드 시트에는 [완전한 스토리보드 계약](storyboard-contract.md) §8의 `storyboard` 객체와 shot 기술 필드를 정본 `project.json`에 추가한다. 기존 schema_version=1.1 및 일반 plan/delivery 프로필은 유지한다. 별도 `validate_storyboard.py`는 전체 비트/씬/샷/패널 연결과 제작 슬롯을 검사하며 실제 이미지에는 `--require-images --base-dir`를 적용한다. 합본 crop/clean 컷은 `split_storyboard.py`의 파생 결과를 asset_registry에 등록하고 같은 ID로 연결한다. CSV/시트/분할 manifest는 조회·등록용 투영이며 별도 원장이 아니다. 의미 검수·권리·사용자 수락을 파일 검사로 대체하지 않는다.
