# 후반작업 단계 기록 (영화 라이프사이클)

project_id: {프로젝트}
artifact_id: {이 기록의 artifact ID}
version: {버전}
status: draft
lifecycle_stage: 05 Post-production
dependencies: {입력 artifact ID와 버전 — 선택 테이크 기록, generation_attempts accept 결과, 승인된 씬/샷 버전}
live_action: {적용 / N/A — 애니메이션·AI 작업은 촬영 로그 대신 generation_attempts와 생성 QA가 입력}

이 문서는 버전이 붙은 인계 artifact이며 `project.json`의 artifact/dependency/version/approval과 `asset_registry`를 대체하는 정본이 아니다. 계획만으로 렌더·믹스·마스터 완료를 주장하지 않는다 — 실제 출력 파일·검사 근거가 있을 때만 generated/verified를 기록한다. 미적용 단계는 N/A와 이유를 적고 만들어내지 않는다.

## 후반 단계 표 — 선택된 단계만 추적

상태는 `project.json` artifact 상태(draft/reviewed/approved/generated/verified/stale)를 그대로 쓴다. 계획·설계 단계는 draft/reviewed에 두고, 실제 출력이 생기기 전에 generated/verified로 올리지 않는다.

| 단계 | 단계 artifact ID·버전 | 입력 테이크/미디어 (ID·버전) | 상태 | 실제 출력 locator | dependencies | 검수 evidence | 미해결 이슈 | 미검증 범위 |
|---|---|---|---|---|---|---|---|---|
| 인제스트/싱크 | | | | | | | | |
| 어셈블리 컷 | | | | | | | | |
| 러프 컷 | | | | | | | | |
| 파인 컷 | | | | | | | | |
| 픽처 락 | | | | | | | | |
| VFX | | | | | | | | |
| ADR | | | | | | | | |
| Foley | | | | | | | | |
| 사운드 디자인 | | | | | | | | |
| 스코어/음악 편집 | | | | | | | | |
| 사운드 믹스 | | | | | | | | |
| 컬러 그레이드 | | | | | | | | |
| 자막/크레딧 | | | | | | | | |
| 마스터링 | | | | | | | | |
| 최종 QC | | | | | | | | |

- 순서·종속 기준은 `references/23-finishing-platform.md`의 의존 순서를 따른다: 컷 잠금 이후 그레이드·최종 믹스, 이후 마스터링. 겹쳐 진행해도 입력 버전을 기록한다.
- 인제스트/싱크 입력은 실제 관찰·확정된 테이크만이다 — 선택/보류/재촬영 상태는 `film-production-day-template.md`나 generation_attempts의 기록에서 참조한다. 싱크를 확인하지 않은 클립은 unverified다.
- 픽처 락은 승인된 컷의 artifact 버전과 approval 근거로만 기록한다. 계획된 잠금 일정을 잠금으로 취급하지 않는다.
- VFX는 `references/21-generated-video-qa-retry.md`, ADR/립싱크는 `references/22-dialogue-lipsync.md`, Foley·스코어·믹스 큐는 `09-edit`의 sound-cues/오디오 의도 절차, 자막·마스터·QC는 `15-delivery`/`23-finishing-platform`과 `12-qa` 절차를 따른다. 이 표는 그 절차를 대체하지 않고 각 단계의 입력·출력·상태만 잇는다.

## 컷 버전 표 (컷 단계별 실제 버전)

| cut 버전 ID | 단계 (어셈블리/러프/파인/락) | 버전 | 입력 테이크·이전 컷 버전 | 실제 타임라인/출력 locator | 변경 요약·의존 | 검수 결과 | 상태 |
|---|---|---|---|---|---|---|---|
| | | | | | | | |

- 상위 입력(각본·테이크 선택·각 샷 에셋)이 바뀌면 실제 의존하는 컷만 stale로 표시하고, 독립 승인 이력은 보존한다.
- 재생·청취 없이 리듬·타이밍 통과를 기록하지 않는다. 가상 타임라인 배분은 `proposal / 비실행용`으로 표시한다.

## 인제스트·싱크 확인 (실제 파일만)

| 테이크/미디어 ID | 원본 파일 locator | asset_registry ID | 선택 상태 (선택/보류/재촬영) | 싱크 방법·오프셋 | 싱크 확인 결과 (확인/unverified) |
|---|---|---|---|---|---|
| | | | | | |

## 후반 QC — 체크리스트와 결과 분리

체크리스트는 계획 단계에서도 만들 수 있다. pass/fail은 해당 실제 파일이 존재하고 검사된 뒤에만 기록한다.

| 검사 | 실제 검사 방법 | 근거 파일/위치 | pass/fail/unverified/N/A |
|---|---|---|---|
| 전체 재생·타이밍·길이 | | | |
| 오디오·믹스 청취 | | | |
| 화면·그레이드·자막 | | | |
| 연속성·주장 대조 | | | |
| 목적지 규격·파일 구조 | | | |

미해결 이슈: {issue ID 목록 — project.json issues와 연결}
가정·미확인 항목: {목록}
다음 인계: {배급/납품 단계 artifact ID·버전}
