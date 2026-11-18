# 공통 제작 계약 — 전체 이미지 패키지와 FINAL

전체 이미지 기반 패키지 및 해당 downstream FINAL에 적용한다. [최소 인계](contract-core.md)와 해당 원장 작업의 [project 계약](contract-project.md)을 함께 지킨다. 실제 파일 패키징 단계에 [delivery](contract-delivery.md)를 추가한다.

## 전체 프리프로덕션 패키지

단일 텍스트/프롬프트 요청은 이 확장을 요구하지 않는다. 전체 이미지 기반 제작은 **시놉 MD, 인물별 페르소나·SSOT MD와 실제 한 장짜리 Identity Sheet A, 통합 기술 콘티 MD, 모든 패널을 이야기 순서로 덮는 합본 스토리보드 이미지 세트(시트당 최대 8패널, 순서 있는 1장 이상)**를 인계한다. 캐릭터 없는 작품은 인물 산출물만 비적용이다. 텍스트 전용 전체 설계는 새 미디어/지출/자동 저장을 추가하지 않는다. 명시적으로 요청한 MD/PDF 저장은 그 파일·이력 단계만 허용하며 no-save/read-only를 임의 해제하지 않는다.

- `preproduction={mode:text|image_backed,synopsis_artifact_id,storyboard_artifact_id,storyboard_sheet_artifact_ids,storyboard_split_asset_id}`를 기존 project.json에 둔다. 이미지 모드에는 합본 시트 artifact ID의 **정렬된 배열**이 필수다. 한 장도 배열로 기록하며 기존 단수 선언은 같은 ID의 한 항목 배열로 이전한다. 시놉 type은 synopsis, 보드 type은 storyboard이며 각각 정확히 한 실제 `.md` 에셋을 연결한다.
- 전체 패키지의 각 `characters[]`에는 `persona={role,personality,observable_behavior,speech}`, `ssot_artifact_id`를 둔다. 네 페르소나 값은 구체적인 비지 않은 문자열이며 무대사에는 이유를 적는다. character_sheet artifact는 시놉 입력 ID/버전과 실제 SSOT MD 에셋 하나를 연결한다. 공급된 캐릭터는 원본을 보존하고 시놉 적용 범위의 인계 시트를 버전으로 연결한다.
- 이미지 모드의 `identity_sheet_asset_id`는 kind=character_identity_sheet, entity_type=character, 해당 entity_id의 실제 이미지다. 전신 정면/3·4/측면/후면 + 얼굴 정면/3·4/측면의 7뷰를 한 장에 구성하고 각 뷰의 고정 앵커를 실제 검사한다. 장면 초상 하나는 대체물이 아니다. 해당 에셋의 `source_asset_ids`에는 그 캐릭터 SSOT artifact가 가리키는 실제 Markdown asset ID가 포함돼야 하며, 검사기가 연결을 확인한다. 인물이 등장하는 모든 샷의 asset_ids에 이 정본을 연결한다.
- storyboard artifact는 현재 시놉과 모든 캐릭터 character_sheet의 정확한 버전에 의존한다. 각 샷/패널에 원문·beat/scene/shot/panel/캐릭터·페르소나/SSOT·카메라·시간·실제 이미지 참조를 통합한다. 각 패널은 해당 beat·가시 캐릭터·audio cue·speech ID를 직접 기록한다.
- 합본 `type=storyboard_sheet` artifact는 보드의 현재 버전에 의존하고 `kind=storyboard_sheet` 이미지 에셋 정확히 하나를 연결한다. PNG의 `storyboard_sheet.panel_traceability` metadata와 표시 캡션은 panel별 ID 매핑을 담는다. 입력 시트/crop은 합본 출력의 대체물이 아니다.
- 이미지 모드의 `storyboard_sheet_artifact_ids`는 이야기 순서로 정렬된 `type=storyboard_sheet` artifact 배열이다. **한 시트에는 최대 8개 패널**만 둔다 — 패널 수·정보 밀도·씬 경계로 장수를 정하고 한 장에 욱여넣지 않는다. 각 시트 artifact는 보드의 현재 버전에 의존하고 `kind=storyboard_sheet` 이미지 에셋 정확히 하나를 연결한다. 각 시트 에셋의 `panel_ids`는 자기 구간의 정본 panels 순서이며, 모든 시트를 순서대로 이어 붙이면 정본 전체 순서와 일치한다(누락·중복 없음). 시트가 두 장 이상이면 각 에셋에 `sheet_index`(1부터)·`sheet_count`를 기록한다. `source_asset_ids`는 그 시트 패널의 실제 픽셀 입력(source_sheet_asset_id가 있으면 그 ID, 없으면 image_asset_id)을 같은 순서로 담고 `source_sha256`는 해당 입력 ID→현재 해시 맵이다.
- `render_storyboard_sheet.py <project.json> --base-dir <root> --output storyboards/sheets/<새.png> [--font <font.ttf>] [--panels-per-sheet 1..8]`는 clean 패널과 외부 촬영 캡션을 순서 있는 PNG 세트로 조립한다. 각 시트의 실제 path/hash/패널·소스 매핑과 동일 traceability PNG metadata를 반환하며 원장을 쓰지 않는다. 총괄이 모든 시트를 등록하고 실제 합본을 연다.
- 합본을 만든 직후 `split_storyboard.py --sheet <프로젝트-relative 시트>`를 이야기 순서로 반복 지정해 장면 overview와 clean 패널을 추출한다. 실제 JSON manifest를 `kind=storyboard_split_manifest`로 등록하고 `preproduction.storyboard_split_asset_id`에 연결한다. 각 추출 이미지도 실제 경로·SHA-256으로 등록한다. manifest의 `file`은 manifest 폴더 기준, `sheet_path`·`sheets[].path`·`band_sources`는 프로젝트 root 기준 상대 경로다. 원본 패널 입력을 추출 이미지로 바꾸지 않는다.
- preproduction/FINAL은 manifest의 주장만 신뢰하지 않는다. 각 panel/scene의 실제 등록 파일·SHA-256, canonical scene/shot/panel, source asset/version/hash 및 asset pins가 서로 일치해야 하며 다른 패널 파일을 alias한 split은 거부한다.
- 모든 필수 실제 파일에는 SHA-256을 기록한다. 이미지 디코딩·현재 종속 버전·전체 커버리지·열린 blocker도 검사한다. reviewed/approved인 preproduction_review 또는 approved인 video_execution_plan에는 plan에서도 이 완결 게이트를 자동 적용하며 이미지 모드를 요구한다. 검토는 시놉·보드·합본을 dependency 그래프로 소비해야 한다.
- 누락 상태는 draft/stale로 보존하고 strict preproduction 검사에서는 준비 미완료로 반환한다. 프롬프트·가상 path·planned 에셋·검사 기록만으로 실제 산출물이라고 표시하지 않는다. 구조 통과 뒤에도 캐릭터 7뷰 정체성, 전체 clean 컷 읽힘, 합본 누락/가독성, 장면 내 제품·빛·그림자·반사 통합을 실제 검수하고 사용자 수락을 별도로 받는다.




## v5.1 프로덕션 무결성 (LOOK·에셋 게이트·계보·provenance·패키지)

선택 확장이 아니라 전체 이미지 기반 패키지와 그 다운스트림(씬 상태·보드·생성 명세·애니매틱)에 적용한다. 기존 schema_version=1.1을 유지하고 아래 필드는 모두 선택이지만, `final`을 선언하는 순간 해당 게이트는 강제다.

### 활성 LOOK과 스타일/월드 바이블
- `look_asset_id`는 루트 필드로, `entity_type=look`(또는 미분류)의 asset_registry 에셋을 가리킨다. LOOK은 **하나만 활성**으로 둔다 — 프로젝트 전체 시각 문법(매체·리얼리즘·비율·팔레트·조명 철학·카메라 문법·스타일 드리프트 금지)을 버전으로 잠근다. 바이블 문서에는 `assets/style-world-bible-template.md`를 쓴다.
- 모든 시각 생성 에셋은 활성 LOOK 버전을 참조한다. LOOK 에셋의 내용이 바뀌면 버전을 올리고 종속물을 stale 처리한다. 패널이 활성 바이블에 없는 새 시각 스타일을 발명하지 않는다.

### 마스터·파생 에셋 계보
- `asset_registry` 선택 필드 `role: master|derivative`와 `master_asset_ref: {asset_id, version}`을 둔다. 반복 정체성 에셋(캐릭터 마스터·장소 마스터·소품 마스터)은 한 번만 master로 등록하고, 씬별 상태(젖음·파손·의상·조명·배치)는 derivative로 등록해 마스터 ID와 **정확한 버전**을 핀한다. 여러 씬 폴더에 같은 마스터의 편집 가능한 사본을 두지 않는다.
- 마스터 버전이 올라가면 그것을 핀하는 derivative는 자동으로 stale가 되고(재핀하기 전까지), 이 계보를 따라 이어지는 derivative도 연쇄로 stale가 된다. 비stale 에셋이 옛 버전을 핀하거나 stale 마스터에서 파생되면 검사가 거부한다.
- 캐릭터 마스터는 7뷰 정체성 시트 외에 서사 관련 표정·의상(WD ID)·DO-NOT-CHANGE 락을 포함한다. 장소 마스터는 생산상 중요한 장소에 4공간뷰(establishing/reverse/lateral/top-down)와 출입·창·장애물·광원 앵커를 둔다 — 수치는 추정이면 `ESTIMATED`로 명시한다. 소품/도구/제품은 연속성이 문제가 될 때만 전/후/측/3/4·상태 변형·스케일 참조를 둔다. 장식 보드를 위해 에셋을 만들지 않는다.

### 에셋 게이트: preliminary vs final
- artifact 선택 필드 `finality: preliminary|final`과 `required_asset_versions: {asset_id: version}`을 둔다. finality를 생략하면 preliminary다.
- `final` 선언은 **생성 전 잠금 게이트**다: 참조 에셋이 전부 등록돼 있고 status가 **`verified`**(v5.1의 LOCKED/APPROVED/VERIFIED_REFERENCE에 해당 — `available`은 파일이 존재할 뿐 에셋 QA 잠금이 아니므로 final을 차단한다)이며 핀 버전이 현재와 같아야 한다. final 시각 산출물(type storyboard/storyboard_sheet)은 추가로 **활성 `look_asset_id`가 등록된 style_world_bible/look 에셋이고 verified이며 해당 board의 `required_asset_versions`에 현재 버전으로 핀**돼 있어야 한다. stale이거나 draft인 artifact는 final이 될 수 없고, final은 의존 체인 어디에도 누락/draft/stale/버전 드리프트를 가질 수 없다. 실행 시점 게이트는 `scripts/asset_gate.py`의 `check_asset_gate(project, artifact_ids=None)`다 — `artifact_ids`로 특정 final 범위만 검사할 수 있고, 반환 blocker 목록이 비어 있어야 최종 생성·납품으로 진행한다. `--profile preproduction|delivery`와 ready-package 검사는 전체 게이트를 적용한다.
- **PRELIMINARY는 언제나 허용된다** — DRAFT/planned/pending 에셋에 의존하는 보드·명세는 preliminary로 생성·검토할 수 있지만 연속성 잠금 산출물로 취급하지 않는다. 누락 에셋은 ASSET_PENDING으로 표시하고 스토리보드를 역설계 소스로 쓰지 않는다.
- `required_asset_versions`의 에셋 버전이 바뀌면 핀을 업데이트하지 않은 해당 artifact는 `update_project`가 자동으로 stale 처리한다. 무관한 다운스트림은 유지된다.

### 패널 자산 참조
- `storyboard.panels[]` 선택 필드 `asset_version_refs: {asset_id: version}`은 그 패널이 사용하는 잠긴 에셋의 정확한 버전을 기록한다(기계 판독 패널 매니페스트 계약). 보드가 `finality: final`이면 모든 패널에 필수이며, 그 샷의 `asset_ids` 전부와 활성 LOOK을 포함해야 한다. 보드가 stale면 패널 핀은 이전 버전을 보존할 수 있다.

### provenance·프롬프트 메타데이터
- asset_registry 선택 필드를 확장한다: `generation_mode`, `negative_prompt`, `model_version`, `seed`, `aspect_ratio`, `resolution`, `created`, `creator`, `license_status`, `checksum`. 기존 `provider`, `model`, `workflow`, `prompt`와 동일하게 **확인된 값만** 기록한다. 확인할 수 없는 값은 비워두지 말고 `UNKNOWN` 또는 `NOT_EXPOSED`로 적는다 — 없는 메타데이터를 발명하지 않는다.
- 프롬프트 원문 파일은 `prompts/`에 두고 asset의 `prompt` 필드나 별도 locator로 연결한다. 생성 이력 자체는 `.history` 감사에 기록한다(아래).
