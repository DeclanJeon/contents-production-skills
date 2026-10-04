# 범용 인계 보강 및 132 가을 광고 작업지시서

설계: `../specs/2026-10-05-state-causality-reinforcement-design.md`. 설계·실행 선택은 사용자가 위임했다. 요청한 도구·모델과 전체 산출물 범위를 축소하지 않는다.

## 1. 근거와 변경 경계 고정

- 기존 5회 fresh-context 적용 응답을 원문 저장한다. 주요 기존 검수는 정상 작동했으므로 실패했다고 주장하지 않는다.
- 본 작업 전 사용자 변경 49개/미추적 18개를 보존한다. 기존 변경 내용에 손대거나 전체 git add를 하지 않는다.
- 설계/작업지시서와 CLI ultragoal brief/goal ledger를 남긴다. mounted Codex goal API 없음은 명시한다.

## 2. 인계·QA 계약 구현

담당 A: 새 `26-state-causality-continuity.md`, `assets/state-transition-template.md`; 기존 `11-ai-handoff.md`, `21-generated-video-qa-retry.md`, `11-ai-handoff-template.md`, `motion-beat-template.md`, `generated-qa-report-template.md`.

- 새 가이드는 선택 조건과 변화/보존·잔류 결과·시점 대응·결합·시간 생략의 최소 슬롯을 소유한다. 기존 실행 절차를 복제하지 않는다.
- 기존 ID·artifact 버전, 실제 근거 위치, 미확인과 수정 경로를 이어받는다. 프로젝트 JSON 필드를 늘리지 않는다.
- 변화 없는 인터뷰 비적용, 가림 불확실성, 단일 행동, 반복 변환의 후속 상태를 예제로 검사한다.
- 기존 판정과 evidence 개념을 유지한다. 실제 매체 없는 예시에 pass 금지.

담당 B: 기존 `09-edit.md`, `assets/09-edit-template.md`, `25-reference-video-analysis.md`, `assets/shot-dna-template.md`.

- 연속 소스 배속/인터벌 획득/단계 몽타주/생략을 구분한다. 실제 경과시간·촬영 구간·간격·중단 근거, 생략 전후 상태와 출력 시간의 연결을 기록한다. 4시간/8초만으로 실제 playback_rate나 간격을 확정하지 않는다.
- 같은 특징의 시점 대응과 화면 정규화 기준점을 기록한다. 렌즈·거리·센서 역추정은 단일 해가 아닐 수 있으며 관찰/가설/미확인을 분리한다. 확정 측정값을 만들지 않는다.
- 시간/측정 상세 절차는 각각 09/25에 남기며 26에는 링크한다. 건축 전용 기본값이나 provider/model 강제 금지.

두 담당 모두 범위 파일만 편집하고 중간 build/lint/test/formatter를 돌리지 않는다. 통합 담당이 완료 후 한 번 수행한다. 공유 filename은 `26-state-causality-continuity.md`로 고정한다.

통합 담당: dirty SKILL.md의 짧은 선택 라우팅 및 CHANGELOG.md unreleased 추가, 설계·QA 산출물, staging/commit, 설치 확인, 광고 실행. 사용자 기존 dirty 내용이 commit에 포함되지 않도록 HEAD 기준 본 작업 추가분만 index에 적용한다.

## 3. 통합 QA 및 커밋

- 같은 시나리오 fresh-context 5회, held-out 요리/수선/뷰티/정적 인터뷰/불확실 렌즈/권리·청취 대조. baseline을 통과한 기능은 regression-free로 보고하고 개선으로 부풀리지 않는다.
- 링크와 기존 버전/구조 검증; 기존 전체 pytest. 미디어 생성/추론 API를 pytest의 영구 테스트에 넣지 않는다.
- 독립 reviewer 두 lane: 품질/명세와 아키텍처/반론. 새 절차 중복, N/A 손실, 가짜 측정·QA 통과가 있으면 수정한다.
- bounded ai-slop-cleaner: 중복·불필요 추상화·fallback·dead weight를 본 변경에서만 검토한다. 코드 변경이 없으면 해당 코드 게이트는 N/A로 남긴다.
- 설계/실행 계약과 구현/QA를 의미별 커밋한다. hook을 우회하지 않는다. 설치 junction이 정확한 저장소를 가리키면 중복 복사 없이 새 가이드를 사용한다.

## 4. 132 광고 실제 제작

- 홈페이지 브랜드/제품 근거를 기록하고 제공 4오브젝트와 일치하는 실제 파일을 확보한다. 상자 전면·측면의 특징을 대응시킨다.
- 기존 preproduction artifact와 SSOT 계약을 적용한다. 성인 여성 한 명, 허구 인물, 가을 저녁, 제품 정확도와 실제 동작 우선. 효능 전후 변화·검증되지 않은 임상 수치를 배제한다.
- codex-imagen으로 5개 샷의 참조 프레임을 생성; 모델 identity와 병/스포이드/상자 참조 재사용. prompt/입력/출력/실패/수정 이력을 보관한다.
- Flow 새 전용 프로젝트에서 Omni 1.1 Flash 선택을 확인하고 720p/9:16/6초/x1으로 최대 5개+표적 재시도 2개, 70크레딧 이내. UI 확인 없이 제출하지 않는다. 업로드 확인, 실제 원본 다운로드, 생성 상태와 결과 검수.
- 실제 원본 구간을 선택해 25초로 조립한다. 업스케일 해상도는 네이티브 생성 해상도와 구분한다. 로고/제품 글자는 결정적 후반 합성으로 보존 가능. 카메라 zoom만을 제품/인물 행동 성립으로 판단하지 않는다.

## 5. 완성 QA와 기록

- ffprobe 실제 길이·해상도·FPS·오디오, 디코드, 컷 양쪽과 상호작용 구간 관찰, 전체 실시간 재생. 가능 범위에서 실제 청취도 별도 수행한다.
- 여성 identity, 금속 칼라/라벨/스포이드/상자 구조, 손·액체 원인→결과, 상태 지속, 가을 룩, 엔드카드 가독성 확인. 실패한 시연을 효과음·빠른 컷으로 숨기지 않는다.
- QA 보고에 관찰 범위, 미검증, 실제 제한과 수정 이력을 적는다. 생성 상태 completed만으로 QA pass를 적지 않는다.
- 산출물 경로·프로젝트 URL·commit ID·검증 결과·남은 제한을 보고한다. 게시하지 않는다. 실제 제작 기록/QA 문서도 별도 커밋한다.
