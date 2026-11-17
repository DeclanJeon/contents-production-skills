# 공통 제작 계약 — 파일 납품과 패키징

실제 파일 패키징/납품 때 적용한다. 원장 필드는 [project](contract-project.md), 이미지 기반 전체/FINAL의 선행 조건은 [package](contract-package.md)가 소유한다. 파일 검사 통과는 실행 승인이나 실제 미디어 품질 인증이 아니다.

## 패키지 도구 인터페이스

- `python scripts/package_production.py <project-root>/project.json --base-dir <project-root> --output <새-출력> [--zip] [--require-final]`: 원장과 실제 파일에서 v5.1 패키지 트리/ZIP를 조립하는 **파생 출력 도구**. 원장을 쓰지 않고 출력 경로를 덮어쓰지 않으며, 매니페스트는 정본에서 재생성한다.


## 전체 프리프로덕션 납품

- `package_production.py --require-final`은 명시적인 현재 FINAL 보드, 완료된 이미지 기반 패키지, 정렬된 현재 시트/hash와 일치하는 split manifest, 전체 scene/panel 이미지의 실제 등록을 요구한다. ZIP의 root `project.json`은 휴대 가능한 파생 스냅샷이며 registry 경로가 실제 패키지 파일을 가리킨다. 표준 폴더 경로는 유지하고, 구형 평면 경로는 asset ID를 포함해 충돌 없이 배치한다. CSV manifest는 정본의 파생물이고 모든 실제 패키지 파일을 열거한다.
- ZIP 재개봉은 asset registry 경로와 split 내부 `file`/`sheet_path`/overview source 참조를 같은 relocation map으로 재투영하고 파생 snapshot hash를 갱신한다. 원본 정본은 변경하지 않으며, 실제 복사 byte stream이 등록 지문과 다르면 게시를 중단한다.


## 납품 필드와 실제 검사

- delivery_spec: {destination, width, height, container, video_codec, caption_mode: none/sidecar/burned_in, final_asset_id, caption_asset_id?}. 기존 소스에서 현재 목적지 규격을 추정하지 않는다.
- delivery_checks: {id, category: playback/timing/visual/audio/captions/continuity/claims, status: pass/fail/unverified/not_applicable, evidence?, reason?}. pass는 실제 검사 위치, N/A는 비적용 이유를 갖는다. 실제 확인하지 않고 pass를 적지 않는다.


### 패키지 출력과 이력 저장
- 제작 프로젝트 루트는 실제 사용자의 `Documents/Media_Studio/<project>` 아래를 기본으로 한다. 저장 경로 초기화·중간/최종 결과 등록·중단/재개 기록은 [프리프로덕션 저장 계약](preproduction-review.md#1a-실제-파일-저장-초기화와-제작-이력)과 `recording-production-history`의 `production_history.py` CLI를 따른다. `.history/`는 시간순 감사 흔적이며 승인 원장이 아니고 project.json과 경쟁하지 않는다.
- `python scripts/package_production.py <project.json> --base-dir <root> --output <새-출력>`는 정본 원장에서 v5.1 패키지 트리(00_MANIFEST…10_DELIVERY)를 만든다. `--zip`은 `<root_name>.zip` 한 개를 만든다. 실제 available/verified 파일만 복사하고, `package_manifest.csv`·`asset_gate.csv`·`asset_registry.csv`·`asset_provenance.csv`·`scene/shot/storyboard_panel manifest`·`dependency_graph.csv`·`generation_status.csv`·`prompt_ledger.csv`·`qa_report.md`를 원장에서 **파생**해 쓴다 — 존재하는 데이터에만 해당 매니페스트를 만들고 빈 파일을 산출물로 위장하지 않는다. 기존 출력 경로는 덮어쓰지 않는다. `.history/`가 있으면 감사 사본으로 포함한다(`--no-history`로 제외 가능). `--require-final`은 에셋 게이트가 열려 있으면 패키징을 거부한다.
- 패키지는 이미지가 있다고 완료가 아니다: 게이트 blocker 0, 핵심 에셋 버전·provenance 추적 가능, 패널 매니페스트가 사용 에셋을 특정 버전으로 참조해야 완료다.
