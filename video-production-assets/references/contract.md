# 공통 제작 계약 v1.1

## ID와 단위
- project_id는 프로젝트 내 고유값으로 정한다. scene_id S01, beat_id B01, shot_id SH01, character_id CH01, claim_id CL01, sound_id AU01, artifact_id A01 형식을 권장하되 기존 체계를 우선한다.
- 시간은 초 단위 숫자로 기록한다. 최종 타임라인은 start_s 포함 / end_s 미포함이다. fps는 초당 프레임 수다. 프레임 범위는 시작 포함 / 끝 미포함이며 길이는 (end-start)/fps다.
- 생성/촬영 원본 길이 source_duration_s와 최종 편집 구간 길이를 구분한다. final 구간은 겹치지 않는다. 전환과 오디오 중첩은 별도 레이어 큐로 표현한다.
- 기본 계약의 최종 영상 구간은 0초부터 target_duration_s까지 연속으로 덮는다. 블랙·정지·타이틀도 하나의 shot으로 기록한다.

## 상태와 버전
- artifact 상태: draft / reviewed / approved / generated / verified / stale.
- approved는 실제 사용자 또는 위임된 승인 사실이 있을 때만 기록한다. generated는 실제 파일이 생성됐을 때, verified는 해당 파일을 검사했을 때만 기록한다.
- 버전과 dependency를 기록한다. 상위 각본이 바뀌면 영향을 받는 샷과 계획을 stale로 표시한다.
- `assets/project-template.json`의 빈 배열과 null은 작성 시작 상태다. 검사 통과 예제가 아니다.

## JSON 구조
필수: project_id, version, target_duration_s, fps, aspect_ratio, scenes, characters, shots, claims, artifacts.
scenes: id, purpose. characters: id, locked_traits.
shots: id, scene_id, character_ids, start_s, end_s, source_duration_s, purpose, start_state, end_state.
claims: id, statement, kind(fact/inference/fiction), source(실제 문서/데이터 위치), status(unverified/verified/fiction).
artifacts: id, type, version, status, dependencies(artifact id 배열), evidence(검수 위치; verified 상태 필수).

## 인계 최소값
각 산출물에 입력 ID와 버전, 생성한 항목 ID, 가정, 실제 검증 결과, 다음 단계 미해결 사항을 붙인다. 재생성에는 바뀐 변수와 실패 타임코드를 남긴다. 같은 정보를 복사해 여러 문서에서 따로 변경하지 말고 공통 원장을 기준으로 조회한다.

## v1.1 구조와 검사 프로필
`schema_version`은 `1.1`을 사용한다. 이전 `1.0` 입력도 일부 호환되지만 새로운 프로젝트는 v1.1 필드를 작성한다.

- plan: 필수 제작 정보·시간·참조·상태 기록을 검사한다. 생성 전 자료와 source_duration_status=estimated를 허용한다.
- delivery: plan 검사에 실제 파일 존재·해시·측정 시간·열린 blocker·납품 검사 기록을 추가한다. `--base-dir`을 프로젝트 폴더로 지정한다. 파일 재생, 디코딩, 음량 측정, 사실의 진위나 동의의 진위는 이 코드가 확인하지 않는다.
- 필수 테이블 scenes/shots/artifacts는 비어 있으면 안 된다. 등장인물이 없는 영상은 characters=[]를 허용한다.
- scene.purpose는 장면 기능, character.locked_traits는 문자열 또는 비어 있지 않은 목록/객체로 기록한다.
- target_duration_s와 shot.start_s/end_s는 fps 기준 프레임 경계에 맞춘다. 초는 실수로 허용하고 반올림 오차를 제한한다.
- shot.source_duration_status: estimated/measured. 계획의 원본 길이는 추정이며 실제 생성/촬영 후 측정한다.
- shot.source_in_s는 선택 테이크의 소스 시작 초, playback_rate는 소스 초/최종 초(기본 1). 배속·슬로모션에서 필요한 소스 길이는 source_in_s+(end_s-start_s)*playback_rate다.
- shot.asset_ids는 asset_registry의 선택된 참조 ID 목록이다. 프롬프트의 경로·룩·의상·소품은 CSV 연속성 원장과 맞춘다.
- artifact.dependencies는 ID 목록이고 dependency_versions는 {artifact_id: 입력 버전} 객체다. 상위 버전 변경은 재검토를 요구한다.
- approved artifact는 approval={by, at, evidence}를 기록한다. 승인자·시간·근거는 실제 기록을 사용한다. 생성/검증 산출물에는 asset_ids, verified에는 evidence가 필요하다.

## 실제 파일과 부가 시간표
- asset_registry: {id, kind, version, path, status, sha256}. path는 실제 파일이 있으면 프로젝트 폴더 기준 상대 경로를 권장한다. planned는 path=null을 허용한다. available/verified는 실제 경로를 갖고, 검사 명령에 base-dir가 있으면 파일 존재와 제공된 해시를 확인한다. 최종 파일에는 verified와 SHA-256이 필요하다.
- asset_registry 선택 provenance 필드(있을 때만 채운다): entity_type(character/product/prop/location/wardrobe/look/lighting/graphic/environment), entity_id, authority(authoritative/inferred/derived), source_asset_ids, prompt, provider, model, workflow, result_asset_id. 사용자가 준 SSOT·바이블은 authoritative로 기록하고 임의로 변경하지 않는다. 확인되지 않은 provider/model을 기록하지 않는다.
- shot.retry_budget: 최초 생성 이후 허용된 최대 재시도 수(선택, 0 이상 정수). 승인된 video_execution_plan의 상한에서 온다. 0이면 최초 1회만 허용하고 attempt의 최대값은 1+retry_budget이다. 필드 부재는 무제한 실행 허가가 아니다.
- generation_attempts: {id, shot_id, attempt(최초=1, 이후 샷별 중복 없는 양의 정수), route, model?, changes?, observed_failures?, preserve?, result(accept/reject/conditional), result_asset_id?, failure_class?, notes?}. 실제 시도만 기록한다. accept는 available/verified인 실제 결과 에셋 ID를 참조해야 하며 planned 에셋을 성공 결과로 기록하지 않는다. 기록/구조 검사 자체가 실행 승인이나 미디어 품질 검사는 아니다.
- audio_mode: no_audio / no_dialogue / dialogue. audio_cues: {id, start_s, end_s, layer, shot_id?, asset_id?}. 소리는 겹칠 수 있지만 전체 영상 구간을 벗어나지 않는다.
- captions: {id, start_s, end_s, text, shot_id?}. 오디오 음소나 자막 타이밍의 의미 적합성은 실제 재생으로 검사한다.
- issues: {id, severity: blocker/major/minor, status: open/resolved, evidence?, fix?}.
- delivery_spec: {destination, width, height, container, video_codec, caption_mode: none/sidecar/burned_in, final_asset_id, caption_asset_id?}. 기존 소스에서 현재 목적지 규격을 추정하지 않는다.
- delivery_checks: {id, category: playback/timing/visual/audio/captions/continuity/claims, status: pass/fail/unverified/not_applicable, evidence?, reason?}. pass는 실제 검사 위치, N/A는 비적용 이유를 갖는다. 실제 확인하지 않고 pass를 적지 않는다.

## 버전 변경과 범위
변경된 산출물과 그 하위 인계를 stale로 표시하고 입력 버전을 갱신한 뒤 관련 항목만 재검수한다. 계획 패키지가 완성됐어도 실제 영상이 완성된 것은 아니다. 참고 후보·예산·도구 기능이 미정이면 계획에서 가정으로 남기고 실제 실행 직전에 확인한다.

## 프리프로덕션 검토와 영상 실행 승인
[프리프로덕션·검토 절차](preproduction-review.md)의 `review.md`는 `type=preproduction_review` artifact로 등록하고 검토 대상의 ID·버전을 dependencies/dependency_versions로 연결한다. 실제 사용자 수락 때만 approved와 approval 근거를 기록한다. 문서·이미지의 generated/verified 상태는 사용자 수락을 뜻하지 않는다.

별도 `type=video_execution_plan` artifact는 승인된 검토 패키지 버전과 명시적 샷·모델/endpoint·실행/재시도/비용 상한을 참조한다. 실제 사용자 실행 승인 뒤에만 approved로 기록한다. 프리프로덕션 중 모델/가격 미정은 허용하지만 실행자 기본값으로 보충하지 않는다. 변경된 에셋의 종속 검토/실행 계획은 stale로 표시하고 새 버전에 이전 승인을 재사용하지 않는다. 사용자 승인과 파일 존재/구조 검사는 별개의 증거다.

프리뷰와 최종은 별도 허가다. `video_execution_plan`의 승인 범위에 프리뷰 단계가 포함되면 승인된 프리뷰 입력 버전·설정·샷/출력 수·상한을 그대로 기록하고, 프리뷰 승인만으로 최종 생성·추가 과금을 허가하지 않는다. 프리뷰 실제 출력·검수 결과·수락 근거는 연결된 artifact(result_asset_id, generated/verified, evidence)로 남기고, 승인된 최종 계획은 프리뷰 판정과 최종 승격 경로를 dependencies로 참조한다. 프리뷰와 최종 범위를 하나의 plan 버전으로 함께 승인한 경우에만 최종이 같은 승인 안에서 현재 입력 버전·조건·상한으로 진행되며, 그렇지 않으면 현재 버전의 별도 최종 승인이 필요하다. 같은 seed·입력의 재생성은 같은 동작·정체성을 보장하지 않으므로 최종본은 다시 검수한다.

## 선택적 상세 스토리보드 확장
제작용/상세 콘티와 전체 보드 시트에는 [완전한 스토리보드 계약](storyboard-contract.md) §8의 `storyboard` 객체와 shot 기술 필드를 정본 `project.json`에 추가한다. 기존 schema_version=1.1 및 일반 plan/delivery 프로필은 유지한다. 별도 `validate_storyboard.py`는 전체 비트/씬/샷/패널 연결과 제작 슬롯을 검사하며 실제 이미지에는 `--require-images --base-dir`를 적용한다. 합본 crop/clean 컷은 `split_storyboard.py`의 파생 결과를 asset_registry에 등록하고 같은 ID로 연결한다. CSV/시트/분할 manifest는 조회·등록용 투영이며 별도 원장이 아니다. 의미 검수·권리·사용자 수락을 파일 검사로 대체하지 않는다.

