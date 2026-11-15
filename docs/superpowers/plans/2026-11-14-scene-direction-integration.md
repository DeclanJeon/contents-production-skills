# Scene Direction Integration — B안 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 기존 전문 오너와 정본을 유지하면서 세계·인물·각본에서 컷별 시작/중간/끝·에셋·카메라·음성/음향·VFX·실제 제출문·수락까지 끊기지 않는 제작용 보드를 만든다.

**Architecture:** 기존 storyboard-contract의 여섯 반환 부분을 유지하고, 전체 샷 명세 안에 원래 오너의 내용/ID/버전을 소비한 컷별 확대 보기를 추가한다. 기존 02/03/04/06/08/09/11/12/14/21/22/26과 캐릭터 오너의 정본을 보강하고, 구조 검사와 내용 수락을 분리한다. V1은 지침·템플릿·인계·행동 평가이며 새 자동 컴파일러·생성 엔진·생산 JSON 스키마가 아니다.

**Tech Stack:** 기존 Markdown/CSV 템플릿, JSON 평가 자료, 기존 Python/pytest 검증 도구. 새 런타임 의존성 없음. 운영 Python 3.10+ 계약 유지; 기존 평가 도구의 더 높은 버전/외부 의존성을 이 기능에 전이하지 않는다.

**Execution:** 사용자 `응 진행해라.`로 Native 구현 및 최종 독립 리뷰 1회를 선택함. Task 2의 실제 모델/26개 테스트 실행 승인과 Git 통합/설치 권한은 별도.

**Spec:** `docs/superpowers/specs/2026-11-14-scene-direction-integration-design.md` — 사용자 상세 설계 승인(2026-11-14). 독립 builder check 원문은 `qa/2026-11-14-scene-direction-integration-builder-check.md`; 회신은 `No issues found.`이며 행동/미디어 검증이 아니다.

## 실행 중 승인된 평가 보완 — E2

기준판 SD01–08은 7 PASS / 1 입력 부족 INCONCLUSIVE, 실제 FAIL 0이었다. 사용자 `응 진행해`로 [아이디어 출발 보완 평가](../../../qa/scene-direction-integration/open-brief-protocol.md)를 남은 18건 안에서 승인했다. 원래 설계/오너 경계는 유지하며, 기존 평가를 지우지 않는다.

- 새 SD09–SD14 6개 입력/36개 기준을 후보 편집 전에 고정한다. 5개는 아이디어만 제공하고 창작을 위임, SD13은 독립된 발화별 Performance 패킷 인계를 검사한다.
- 예산: 이미 쓴 8 + 새 기준판 6 + 형성 최대 4 + 최종 8 = 최대 26. 최종은 새 6종과 기존 SD03/08의 보호 대조군이다. 자동 재시도/추가 공급자/미디어/설치/Git 권한은 늘리지 않는다.
- Tasks 3–8의 파일/목표는 요구 커버 지도다. 실제 실패 없는 영역을 중복 수정하지 않는다. 실제 실패를 발견하면 관련 오너 변경을 의존 묶음으로 진행하고 4건 이내 형성 점검·최종 8건으로 검증한다. 이 배분 때문에 각 문서 미세 변경마다 새 모델 테스트를 할 수는 없으며, 검증 전 중간 작업을 행동 GREEN으로 부르지 않는다.
- 새로운 허구 이름/줄거리 자체를 고정 정답으로 만들지 않고 사용자 잠금과 응답 내부 정본→샷/요청문의 소비·인과/시간·구체성을 판정한다. 실제 FAIL이 없으면 제작 지침을 임의 수정하지 않는다.
- 이 절은 아래 원래 8+10+8의 실행 배분을 대체한다. 미디어/일반 창작 역량이나 통계적 우열을 검증했다고 해석하지 않는다.

## Global Constraints

- `project.json schema_version=1.1`, 카메라 스키마, 기존 ID/상태/승인/파일 저장·배포 규격을 유지한다.
- 새 스킬/의무 JSON 테이블·필드·enum·새 기본 validator profile을 추가하지 않는다.
- V1에서 임의 Markdown을 자동 해석·합성하는 의미 컴파일러나 새 `--direction` CLI는 만들지 않는다.
- 구조 검사, 설계 내용, 실제 입력 준비, 실행 권한, 실제 결과, 사용자 수락을 각각 보고한다.
- 기존 필드명/여섯 반환 부분/마스터·파생 계보·artifact dependency/version을 유지한다. 추가 Markdown 구획은 기존 정보의 통합/조회이고 별도 정본이 아니다.
- 세계/인물/음악/효과/무빙/새 컷을 모든 요청에 강제하지 않는다. 단일·비서사·무언·정적·원테이크·피치·chat-only 경계를 보존한다.
- 실제 없는 파일·보이스·가격·Hz/BPM·타이밍 실측·검수·권한을 발명하지 않는다. 모델 미정은 유효한 설계 상태다.
- 제공 웹툰에서 일반 메커니즘만 이전한다. 원본 픽셀·대사·캐릭터·줄거리·특정 배열을 평가/제작 자산에 복제하지 않는다. 113개 표본 열람을 전수 분석으로 승격하지 않는다.
- 수정은 격리된 후보 작업 공간에서 진행한다. 현재 전역 skill symlink가 가리키는 dirty checkout을 실험 작업 공간으로 사용하지 않는다.
- 기존 사용자/다른 작업의 미커밋 파일과 프롬프트·실패 이력을 보존한다. 승인되지 않은 stash/reset/merge/push/설치·릴리스 없음. 아래의 모든 커밋 단계도 이 새 작업의 Git 쓰기가 명시적으로 승인된 경우에만 수행하며, 승인 없으면 변경/검증 기록만 남긴다.
- 작성 승인과 실제 평가 호출/비용/미디어/게시 승인은 다르다. 실행 도구/모델·횟수 권한이 없으면 필요한 단계만 명시적으로 보류한다.
- 새 프로덕션/평가 런너를 만들지 않는다. 기존 전용 writing/postediting 런너의 입력 형식을 이 과제에 억지로 맞추거나 수정하지 않는다.
- 문서 행동 테스트는 실제 입력→실제 에이전트 출력의 내용 대조다. 키워드 grep/문자 수·JSON parse·자체 점수는 대체물이 아니다.

## Review Focus

1. **평범한 정지/무음/화면 밖 발화/원테이크:** 정당한 N/A와 동일 상태 hold를 인정하고 새 대사·음악·얼굴 컷을 강제하지 않아야 한다. SD03/SD05/SD08, Tasks 4·5·8에서 검사한다.
2. **첫끝은 같지만 전달/복귀가 필요한 행동:** 두 장만으로 중간 사건을 삭제하지 않고 손·점유·접촉·후속 유지까지 보여야 한다. SD02, Tasks 4·6에서 검사한다.
3. **잘못된 입력 핀/아직 없는 음성·에셋:** 문서가 채워졌다는 이유로 현재 실행 준비나 실제 voice 선택/청취로 승격하지 않아야 한다. SD05/SD06, Tasks 5·7·8에서 검사한다.
4. **생성 길이 변경/네이티브 오디오 경로:** 컷·반응·원문·보이스·소리를 유지하고 시간 주소만 변환하며 중복 TTS·가짜 제어를 만들지 않아야 한다. SD06/SD07, Tasks 5·7에서 검사한다.
5. **통합 보드의 오래된 요약/상위 정본 수정:** 세계/인물/대사 사실을 보드에서 독립 변경하지 않고 실제 입력 버전과 바뀐 의존만 재검토해야 한다. SD01/SD05/SD08, Tasks 3·4·8에서 검사한다.

## 사전 결정과 승인 경계

### 작업 공간/스냅샷

- 실행 시작에 `using-git-worktrees`로 격리 공간을 준비하고 기준 커밋/작업 트리 변경 목록을 기록한다. 계획 작성 시 HEAD는 `0e1d9f3`였다. 실행 때 HEAD를 새로 확인하고 바뀐 오너 지침은 보존/재조정한다.
- 원본 dirty tree의 관련 수정이 필요하면 출처/범위를 먼저 확인해 선택적으로 반영한다. 전체 dirty tree 복사나 무관한 작업 커밋 금지.
- **커밋 훅 주의:** 조사한 `.git/hooks/post-commit`은 `sync_installed.py`를 자동 실행한다. 같은 Git 공통 디렉터리의 worktree도 이 훅을 공유할 수 있으므로 격리 worktree만 만들었다고 전역 설치가 안전한 것은 아니다. 실행 시 활성 hooksPath와 post-commit/post-merge/post-rewrite를 확인한다. 후보 검증 중 커밋이 명시적으로 허가된 경우에는 버전 검사를 유지하고 sync를 하지 않는 계획 전용 임시 훅 디렉터리를 만들어, 해당 Git 명령에만 `-c core.hooksPath=<그 디렉터리>`로 적용한다. 실제 pre-commit 검사/명령 성공을 확인하고 전역 Git 설정·기존 훅·설치 링크는 바꾸지 않는다. 이 분리가 불가능하면 후보 커밋을 보류한다.
- 기준선은 후보 수정 전 읽기 전용 source snapshot으로 고정하고, 후보는 변경 epoch별로 새 snapshot을 만든다. 파일/해시·입력·프로필·원시 출력은 지우거나 덮어쓰지 않는다.
- 원시 평가 자료는 이 계획 전용 gitignored 작업 공간 또는 사용자 승인 외부 위치에 둔다. `qa/scene-direction-integration/`에는 새로 쓴 과제/프로토콜/검토 양식, 최종 요약에는 실제 근거 locator를 둔다. 원본 웹툰 파일은 복사하지 않는다.

### 실제 평가 실행 승인

Task 1의 자료 작성/준비는 모델 호출 0회다. Task 2 이전에 현재 하네스의 **실제로 있는 도구**로 읽기 전용/텍스트 평가를 할 수 있는지 확인하고 다음을 한 번에 승인받는다:
- 동일한 정확 provider/model ID, reasoning 설정, 응답 한도와 대기/중단 정책.
- 첫 V1 epoch 계획: 기준선 8회 + 단계별 후보 점검 10회 + 최종 동결 후보 8회 = **최대 26회 생성**, 앱 수준 재시도 0회. 최종 독립 리뷰/판정 호출은 이 26회에 포함하지 않으며 실행 방법 선택/별도 승인 범위를 기록한다.
- 단계별 10회: Task 3 SD01/SD08(2), Task 4 SD02/SD03(2), Task 5 SD05/SD06/SD07(3), Task 6 SD04(1), Task 7 SD06(1), Task 8 SD08(1).
- 실제 고정 입력과 읽을 source snapshot, 허용 도구, 출력 위치, 비용/호출 상한, 승인 근거.

한도/모델이 미정이면 실행하지 않는다. 도구가 없으면 없는 기능을 발명하거나 다른 CLI/공급자를 조용히 대신 쓰지 않는다. 추가 수집/반복·실패 수정 epoch는 새 한도/권한 확인 후 별도 기록한다. 형성용 단계별 출력과 최종 동결 비교를 합산하지 않는다.

### 평가 자료 형식 — 프로덕션 스키마 아님

`cases.json`은 `suite_id`, `cases[]`를 가진 QA 입력이다. 각 case는 `id`, `category`, `user_request`, `supplied_context`, `locks`, `required_observations`, `forbidden_expansions`, `owner_paths`, `rubric_ids`를 가진다. 사용자에게 보여줄 입력은 `user_request`와 `supplied_context`뿐이며 정답/rubric은 생성 에이전트에 주지 않는다.

검토 카드에는 `case_id`, `condition`, `source_snapshot`, `input_sha256`, `output_locator`, `output_sha256`, `execution_status`, `criteria[]`, `verdict`, `limitations`를 둔다. 각 criterion은 `id`, `expected`, `input_locator`, `output_locator`, `observation`, `verdict`를 기록한다. QA 판정은 기존 관례의 PASS/FAIL/INCONCLUSIVE, 미판정은 UNREVIEWED다. 실제 출력/직접 검사 근거가 없으면 PASS 금지. 이 자료를 `project.json` 상태/승인 enum으로 넣지 않는다.

실제 평가 호출은 source snapshot만 읽는 fresh context, 동일 role/tools/profile, 조건별 같은 과제 본문을 사용한다. baseline/candidate 순서는 case별 교대로 고정한다. 실패 결과·중단/미검사·도구 오류를 보존하고 유효한 PASS 표본으로 대체하지 않는다.

## 파일 구조와 책임

- **신규 평가 자료만:** `qa/scene-direction-integration/cases.json`, `rubric.md`, `protocol.md`, `review-template.json`, `coverage.md`.
- **신규 최종 보고:** `qa/2026-11-14-scene-direction-integration-validation.md`.
- **이야기 기반:** 기존 `02-story`, `03-screenplay`, `04-performance`, 해당 템플릿·캐릭터/페르소나 입력 연결.
- **통합 소유자:** 기존 `storyboard-contract.md`와 `06-shots-template.md`; 하나의 shot 상세 블록은 기존 storyboard artifact 안에 둔다.
- **자원 준비:** 기존 `14-production-ops` 문서/템플릿과 기존 registry/pins의 조회.
- **전문 내용:** 기존 음성/편집/동작/VFX/상태/AI 인계 오너. 한 곳의 규칙을 다른 오너 본문에 복사하지 않고 현재 입력·소유자 포인터만 연결한다.
- **QA/라우팅:** 기존 12/공통 계약/프리프로덕션 절차와 진입 스킬의 조건부 포인터.

기존 Python 검증기·생산 JSON/CSV 열·모델 실행기 코드는 이 계획의 변경 파일이 아니다. 결함이 확인되면 별도 재현/설계 판단으로 분리한다.

---

### Task 1: 고정 과제·루브릭·평가 프로토콜 준비

**Files:**
- Create: `qa/scene-direction-integration/cases.json`
- Create: `qa/scene-direction-integration/rubric.md`
- Create: `qa/scene-direction-integration/protocol.md`
- Create: `qa/scene-direction-integration/review-template.json`
- Create: `qa/scene-direction-integration/coverage.md`

**Interfaces:**
- Consumes: 승인 spec §§5–17, 감사의 범위/구조 검사 한계.
- Produces: SD01–SD08 고정 입력, 아래 판정 기준·불변값, 조건 동일성/증거 보존 규칙. 후속 모든 task는 이 ID/입력을 재사용한다.

**고정 과제:**

| ID | 공급할 상황/잠금 | 필수 관찰과 보호할 예외 |
|---|---|---|
| SD01 | spec §14의 신호소 설정·두 인물·레버는 CH02 왼손·경고 원문 `놓지 마.`·8초/24fps를 공급; 전체 텍스트 제작 보드 요청 | 세계 규칙이 행동·비용/후속 상태에 소비됨, 인물 선택/경고 전술, 고정 원문/손·시간, 새 원장/실행 없음 |
| SD02 | 무언 6초 행동: CH01 오른손의 열쇠를 CH02 왼손에 넘겼다가 같은 샷에서 돌려받음. 시작/끝 점유는 CH01 오른손, 필수 중간 전달을 고정 | 전달/접촉 정점·상대 반응/되돌림과 현재 점유를 별도로 보여줌; 같은 첫끝을 이유로 hold/중간 삭제 금지 |
| SD03 | 6초 고정 원테이크·완전 무음·두 인물이 서로의 선택을 기다리는 동일 상태 hold, 새 사건/카메라/컷/오디오 추가 금지 | 의도적 정지/N/A 인정, 시간/시선·끝 연결 설명, 가짜 '역동성 보완' 금지 |
| SD04 | 새 허구 생물: 보호막 발동은 앞발 지지 시에만 가능, 발동 후 왼쪽 앞발의 떨림이 다음 샷에도 남음. 능력 대가·두 샷 순서 잠금 | 몸통/지지·경로/차폐·준비/충격/소멸·환경 반응·잔류를 연결; 외형 시트로 물리 검증/실제 FX 성공 주장 금지 |
| SD05 | CH01 화면 밖 경고, CH02의 얼굴 반응 유지·입은 보이지 않음, CH03의 정체 공개는 다음 샷. CH02 시트 v2와 그 v1을 핀한 voice_profile 공급 | 화자/청자·정보 유보·부분 lip-sync N/A 보존; stale 핀 반환, 새 voice/정면 컷/조기 CH03 공개 금지 |
| SD06 | 기존 `storyboard-timing-to-prompt.md` §4의 30초/12샷 예시를 정확한 공급 콘티로 동결; 5/10/20/30초 묶음의 모델 중립 인계 요청. voice_id/모델 미선정, 기존 발화/반응·순서 고정 | global/shot-local/generation-local·핸들 구분, 실제 원문·반응/정착·카메라·음성 정체성 보존, 가짜 API/중복 TTS/비례 압축 금지 |
| SD07 | 음악/SFX가 필요한 8초 추격 텍스트 계획; 실제 음원 없음, 공급된 발화창 [2,4), 공개 시점 5초는 계획값 | BGM 진입/유보/전환/끝, SFX 원인·거리/청점·잔향·음성 우선·싱크가 읽힘; 실제 BPM/박/게인 측정·음원/권리/청취 성공 발명 금지 |
| SD08 | 캐릭터 없는 설명 보드의 QA-only, no_audio·새 파일/이미지/원문 수정 금지. 공급 보드는 세부 설명이 `적절하게`뿐이고 'validator 통과'는 사용자 제공 주장 | 내용 부족을 위치/영향/최소 수정으로 반환, 구조/내용/실제 검수 구분; 세계관/인물/보이스/프로젝트 생성·직접 validator 실행/이미지 열람 주장 금지 |

- [x] **Step 1:** 8개 `user_request`/`supplied_context`를 실제 재사용 가능한 완전한 문장/표로 작성하고 잠금/판정 기준을 별도 열로 고정한다. SD06은 현재 파일의 예시 원문·버전을 기록하고 예시 타이밍을 보편 공식으로 쓰지 않는다.
- [x] **Step 2:** 루브릭을 원문 보존, 세계/인물 소비, 첫중간끝·시간/연결, 전문 자원/소리/FX, 최종 요청문 대응, 범위/증거 정직성으로 나눈다. 각 항목은 입력/출력 locator와 관찰 이유를 요구하고 평균으로 blocker 상쇄 금지.
- [x] **Step 3:** protocol에 위 승인/26회 계획·동일 프로필·읽기 범위·원시 증거·미검사 처리·snapshot/epoch 보존을 적고 review template은 UNREVIEWED로 만든다.
- [x] **Step 4:** `python3 -m json.tool qa/scene-direction-integration/cases.json > /dev/null` 및 `python3 -m json.tool qa/scene-direction-integration/review-template.json > /dev/null`. 기대: parse 성공. 이어 직접 8개 ID/잠금/원문·예시 시간·rubric 연결을 대조한다. JSON parse는 행동 테스트가 아님을 기록한다.
- [x] **Step 5:** 조건 확인 완료 — 이 새 작업의 커밋은 명시적으로 승인되지 않아 미커밋으로 보존한다(ledger Ruling). 승인 후 해당 신규 QA 자료만 커밋하며 예시 메시지는 `test: define scene direction behavior cases and evidence protocol`.

### Task 2: 기준선 고정과 실제 RED 관찰

**Files:**
- Modify: `qa/scene-direction-integration/protocol.md`, `coverage.md`
- Create (계획 전용 ignored evidence root): source/input/profile manifests, SD01–SD08 baseline raw outputs/receipts/review cards.

**Interfaces:**
- Consumes: Task 1의 고정 과제·프로토콜.
- Produces: 변경 전 source hash와 실제 baseline 출력/각 criterion의 PASS/FAIL/INCONCLUSIVE. 이후 task의 RED 근거.

- [x] **Step 1:** 격리 worktree/기준선 snapshot과 source 파일 해시를 고정한다. dirty 수정/설치 링크를 기준선에 몰래 가져오지 않는다. 관련 충돌/미반영 변경을 ledger에 기록한다.
- [ ] **Step 2:** 실제 평가 도구/모델/상한·권한을 확인한다. 미승인이면 정확한 요청을 한 번에 반환하고 이 단계 및 스킬 수정은 보류한다. 도구/모델 변경으로 평가를 대신 수행하지 않는다.
- [ ] **Step 3:** 승인된 동일 read-only fresh-context 조건으로 baseline 8개를 각 1회 실행한다. 주입 prompt에서 루브릭/정답/후보 전용 절차를 빼고 source 읽기 증거·전체 출력·프로필/시간·실행 상태를 보존한다.
- [ ] **Step 4:** 실제 출력을 Task 1 기준으로 검토하고 입력/출력 locator별 실패를 기록한다. 기존 PASS는 보호 대조군이며 실패를 억지로 만들지 않는다. 모든 baseline이 충분하면 개선 효과를 꾸미지 말고, 강화가 필요한 실증 범위를 사용자와 재확인한다.
- [ ] **Step 5:** coverage에 각 요구의 기존 커버/관찰된 실패/미확인을 구분한다. 권한·실행·입력 동일성 오류는 craft FAIL/PASS 대신 INCONCLUSIVE로 남긴다. 이 task의 완료는 실제 baseline과 검토가 있을 때뿐이다.

### Task 3: 세계·인물·각본의 장면 소비 강화

**Files:**
- Modify: `video-production-assets/references/02-story.md`, `assets/02-story-template.md`
- Modify: `video-production-assets/references/03-screenplay.md`, `assets/03-screenplay-template.md`
- Modify: `video-production-assets/references/04-performance.md`, `assets/04-performance-template.md`
- Modify: `designing-video-character-sheets/SKILL.md`, `designing-character-personas/references/expression-voice-bridge.md`

**Interfaces:**
- Consumes: SD01/SD08 baseline과 spec §§6–8.
- Produces: 기존 `세계관 규칙`·비트·각본/연기 표에 연결된 규칙→상황/판단→행동/발화→비용/잔류. persona/character_sheet/voice_profile 원래 소유/필드 유지.

- [ ] **Step 1 (RED):** baseline SD01의 미소비 세계 규칙/인물 전술·빈 동작, SD08의 과잉 확장을 실제 locator로 확인한다. 이미 충족한 축은 새 결함처럼 쓰지 않는다.
- [ ] **Step 2:** 02 템플릿의 기존 `세계관 규칙` 아래 필요한 법칙·조건/한계·대가·인물별 지식·관련 beat/scene·가시 결과/필요 자원 구획을 추가한다. LOOK과 분리하고 서사형 범위에만 적용한다.
- [ ] **Step 3:** 03/04의 기존 행동/의도/반응/물리 과제·상태 대조에 인물의 목표/관계·자극/인지·선택/비용과 공급 원문 검산을 연결한다. 새 플롯/대사를 보드에서 몰래 만들지 않는다.
- [ ] **Step 4:** 캐릭터/표현 브리지에 이번 장면이 소비한 SSOT/version·행동/말투/고정 음성 앵커를 설명하게 한다. 0–33 사본·필수 유형·보이스 생성은 추가하지 않는다.
- [ ] **Step 5 (GREEN):** 후보 SD01/SD08 각 1회. SD01 원문 `놓지 마.`, CH02 왼손, 설정의 행동 비용, 8초/24fps와 미생성 상태를 대조한다. SD08은 인물/세계/오디오·파일 생성 없이 QA 범위 유지. 결과를 실제 카드로 기록한다.
- [ ] **Step 6:** 관련 파일만 기능 단위 커밋. 예: `feat(story): connect world and persona rules to scene choices`.

### Task 4: 컷별 통합 확대 보기와 자원 준비 연결

**Files:**
- Modify: `video-production-assets/references/storyboard-contract.md`, `references/06-shots.md`, `assets/06-shots-template.md`
- Modify: `storyboarding-video/SKILL.md`
- Modify: `video-production-assets/references/14-production-ops.md`, `assets/14-production-ops-template.md`

**Interfaces:**
- Consumes: Task 3의 정본 소비, 기존 scene/shot/beat/panel·자원 핀·06 shot-local cue·09 컷 표.
- Produces: 기존 여섯 반환 부분의 §3 안에 `컷별 통합 제작 명세`, 다음 열 가지 상세 구획과 source/version/구간 연결. 별도 JSON/원장 없음.

**상세 구획:** `입력과 목적`, `첫 프레임`, `내부 사건`, `마지막 프레임과 연결`, `화면/카메라/공간`, `발화/연기`, `사운드`, `VFX/조명`, `필요한 자원`, `프롬프트/검수`.

- [ ] **Step 1 (RED):** SD02 중간 전달/반환/손 점유 누락, SD03 정지/원테이크를 깨는 과잉 설계를 baseline에서 확인한다.
- [ ] **Step 2:** 통합 규칙은 storyboard-contract에 한 번 정의하고 06/진입 스킬은 그 절을 조건부 참조한다. 상위의 실제 내용을 버전/locator와 함께 가져오며 링크 목록으로 대체하지 않는다. 보드의 자체 샷 연출과 상위 정본을 구별한다.
- [ ] **Step 3:** 06 템플릿은 기존 요약표/필드명을 유지하고 샷별 확대 블록을 추가한다. 첫끝·필수 중간·오프스크린/의도적 hold·원테이크를 구분한다. 컷 경계에서 상태/시선·소유/방향·광원과 다음 연결을 확인한다.
- [ ] **Step 4:** 14의 기존 각본 브레이크다운/준비 표에 실제 사용 샷, 기능/뷰/상태·마스터/파생, 현재 입력 버전·준비/권리·담당/미해결을 연결한다. JSON registry/CSV 열은 바꾸지 않고 미래 자원의 선제 생성을 요구하지 않는다.
- [ ] **Step 5 (GREEN):** SD02/SD03 후보 각 1회. SD02는 같은 첫끝 안의 필수 두 전달 단계와 현재 손·점유를 찾을 수 있어야 한다. SD03은 6초 고정·무음·원테이크·N/A와 같은 상태를 유지해야 한다. 파일/에셋 준비·공간 실행은 계획과 구별한다.
- [ ] **Step 6:** 해당 블록에 spec §14의 신호소 예시를 새로 만든 비정본 작성 예로 축약 연결한다. 원본 작품/실제 미디어/승인 샘플로 표시하지 않는다. 기능 단위 커밋.

### Task 5: 고정 보이스·대사별 연기·씬 음향의 연결

**Files:**
- Modify: `video-production-assets/references/09-edit.md`, `assets/09-edit-template.md`
- Modify: `video-production-assets/references/22-dialogue-lipsync.md`, `assets/performance-cue-template.md`

**Interfaces:**
- Consumes: Tasks 3·4의 SSOT/version·통합 shot/cue 참조, 기존 sound-cues/audio_cues·voice 선택/청취 기록.
- Produces: 같은 컷의 고정 음성/말투/이번 연기·실제 화자/청자/가시성, 음악/효과/환경/침묵의 기능·시간/청점·믹스와 실제 준비 상태.

- [ ] **Step 1 (RED):** SD05 stale 핀/화자·청자 혼동/강제 입 노출, SD06 음성 정체성 또는 반응 손실, SD07 음악 이름뿐인 큐/가짜 청취·측정을 baseline에서 특정한다.
- [ ] **Step 2:** 22/performance 기존 칸에 source character_sheet/voice_profile의 정확한 버전, 재사용 voice_identity_direction, 실제 대사의 의도/서브텍스트·강조/쉼/숨·속도/압력과 청자 반응을 대조하게 한다. 무언/가시 입 N/A와 실제 보이스 선정·권리/청취 경계를 유지한다.
- [ ] **Step 3:** 09의 기존 source/cut/sync/mix_note에 음악의 진입·유보·전환/종료, 필요 모티프/밀도·발화 우선순위를 연결한다. SFX/Foley/앰비언스는 원인·재질/거리·청점·꼬리·동기/중첩을 구체화한다. 새 CSV 열/음향 enum·보편 BPM/게인을 만들지 않는다.
- [ ] **Step 4 (GREEN):** SD05/SD06/SD07 후보 각 1회. 실제 voice_id/음원 없는 상태 유지, stale 핀을 현재 실행 입력으로 쓰지 않음, 화면 밖 화자·다음 샷 공개 보존, 정확 원문/음성 앵커/시간·사운드 기능/청점 대조. 네이티브 음성 지원 미확인 상태에 별도 TTS/가짜 파라미터를 추가하지 않음.
- [ ] **Step 5:** 음성/편집·청취 결과와 제안 상태를 분리한 증거를 남기고 기능 단위 커밋.

### Task 6: 동작·VFX를 같은 시간의 원인/반응/잔류로 연결

**Files:**
- Modify: `video-production-assets/references/08-animation.md`, `references/21-generated-video-qa-retry.md`, `references/26-state-causality-continuity.md`
- Modify: `video-production-assets/assets/motion-beat-template.md`, `assets/vfx-layer-stack-template.md`, `assets/state-transition-template.md`

**Interfaces:**
- Consumes: Task 4의 shot 내부 사건/자원, Task 5의 cue/음향 동기, 기존 08/21/26 선택 슬롯.
- Produces: 준비→발동→진행/차폐→접촉/충격→소멸·잔류와 배우/환경 반응, 보존/변화·상속 상태의 명시적 shot-local 연결.

- [ ] **Step 1 (RED):** SD04 baseline에서 지지 조건/발동 경로·차폐/잔류 떨림·환경 반응이 어디서 빠졌는지 기록한다.
- [ ] **Step 2:** 필요한 동작·효과만 기존 motion/VFX/state 칸에서 시간 관계를 설명하고 06 cue/09 동기와 연결한다. 외형/Bounding box를 관절·지지·접촉/동적 검증으로 쓰지 않는다.
- [ ] **Step 3:** 효과의 규모·빛/그림자·반사/깊이·필수 행동 가독성과 후속 손상을 연결한다. 실제 조명과 독립 VFX를 구별하고 미사용은 사유 있는 N/A로 둔다. 새 event ID/물리 수치/실제 시뮬레이션 성공 주장 없음.
- [ ] **Step 4 (GREEN):** SD04 후보 1회. 보호막의 지지 전제, 단계/상호작용, 왼쪽 앞발 떨림의 다음 샷 유지, 미실행 공간/FX 검증을 대조한다. SD02의 반환/접촉 수락 기준도 텍스트 대조로 다시 확인하되 새 평가 실행처럼 계수하지 않는다.
- [ ] **Step 5:** 관련 파일만 기능 단위 커밋.

### Task 7: 전체 설계를 최종 요청문에 보존

**Files:**
- Modify: `video-production-assets/references/11-ai-handoff.md`, `assets/11-ai-handoff-template.md`
- Modify: `creative-production/references/storyboard-timing-to-prompt.md`
- Modify: `ai-camera-control/SKILL.md` (기존 오디오/시각 역할·인계 경계의 필요한 포인터만)

**Interfaces:**
- Consumes: Tasks 3–6의 통합 제작 명세와 각 오너 버전·기존 세 시간 basis/11 참조 역할표.
- Produces: 각 필수 요구→실제 VISUAL/AUDIO 문장·첨부/파라미터·지원 등급의 같은 버전 역대조. 새 provider payload/CLI 없음.

- [ ] **Step 1 (RED):** SD06 baseline에서 5/10/20/30초 묶음으로 옮기며 사라진 컷/발화/반응·보이스·음향/상태와 주소 혼동을 해당 ID/구간으로 기록한다.
- [ ] **Step 2:** 기존 11 시간/카메라/참조 대응표를 활용해 세계/인물 선택의 가시 결과, 첫중간끝·반응, 음성 정체성/연기·소리·VFX도 실제 최종 요청의 문장/입력에 대응한다. 또 하나의 경쟁 시간 원장을 만들지 않는다.
- [ ] **Step 3:** 실제 지원 자연어/하드 제어·미지원/미확인을 구분하고, 네이티브 오디오면 AUDIO가 같은 요청에, 별도 트랙이면 승인된 편집 경로에 들어감을 명시한다. AI 카메라 오너가 TTS/믹스를 별도 실행하거나 줄거리 한 문장으로 모든 내부 컷을 합치지 않는다.
- [ ] **Step 4 (GREEN):** SD06 후보 1회. 공급된 30초/12샷·모든 발화·중요 반응을 각 묶음에 대응하고, 예시 global 82–85초의 shot-local [0,3), 30초 작업 generation-local [22,25)를 보존한다. 5/10초 작업에서는 해당 작업 local [2,5)이며 다른 basis와 혼동하지 않는다. 모델 미선정/실제 음성 미생성 상태와 의미 검수의 범위를 기록한다.
- [ ] **Step 5:** 전후 제출문 보존 근거를 남기고 기능 단위 커밋.

### Task 8: 내용 수락·준비도·진입 라우팅을 한 계약으로 연결

**Files:**
- Modify: `video-production-assets/references/12-qa.md`, `assets/12-qa-template.md`
- Modify: `video-production-assets/references/storyboard-contract.md`, `references/preproduction-review.md`, `references/contract.md`
- Modify: `creative-production/SKILL.md`, `creative-production/references/production-routing.md`
- Modify: `video-production-assets/SKILL.md`, `storyboarding-video/SKILL.md` (필요한 조건부 포인터/완료 경계만)

**Interfaces:**
- Consumes: Tasks 3–7의 현재 입력/샷/실제 요청문 연결과 기존 QA 판정/수정표.
- Produces: 구조/내용/실제 입력 준비/결과/사용자 수락의 분리와 단일 indexed FIX 반환. 기존 상태·권한 규칙은 유지.

- [ ] **Step 1 (RED):** SD08 baseline의 구조 PASS→내용/실제 검수 승격 또는 QA-only 범위 확대를 확인한다. 품질을 증명하지 않는 현재 validator의 고의적 범위를 '고칠 버그'로 바꾸지 않는다.
- [ ] **Step 2:** 기존 12/보드 QA에 입력 locator·출력 위치·관찰/해석·영향·최소 수정·필요 오너·검사 범위를 연결한다. 문서 수/가중 평균·키워드만으로 통과시키지 않는다. 미검증과 관찰된 불충족을 구분한다.
- [ ] **Step 3:** 준비도 세 질문(설계 충분성/해당 배치의 실제 필수 입력/실행 권한)과 전체 다섯 판정 층을 기존 검토 문서에 보고하게 한다. missing/stale·지원 미확인·해당 단계 차단은 이유와 ID로 남기되 새 production enum/profile 없음.
- [ ] **Step 4:** 기존 entry/라우팅은 현재 요청에 필요한 통합/전문 절만 연결한다. 원장/저장/Blender·이미지/음성/유료 실행 승인 경계는 유지하고 단순 내러티브 카메라로 공간 실행을 강제하지 않는다.
- [ ] **Step 5 (GREEN):** SD08 후보 1회. 실제 generic 텍스트 부족을 위치/최소 수정으로 지적하되 원문 수정·파일·세계/인물·오디오·가짜 검증 실행 없이 종료해야 한다. SD03/SD05의 정지·화면 밖 발화·N/A 기준도 기존 증거에 대조한다.
- [ ] **Step 6:** 통합/QA 포인터만 묶어 기능 단위 커밋.

### Task 9: 동결 비교·전체 회귀·범위 있는 최종 보고

**Files:**
- Modify: `qa/scene-direction-integration/protocol.md`, `coverage.md`
- Create: `qa/2026-11-14-scene-direction-integration-validation.md`
- Create (ignored evidence root): final candidate source manifest, SD01–SD08 candidate raw outputs/receipts, baseline/candidate criterion reviews and final comparison summary.

**Interfaces:**
- Consumes: 고정 과제/동일 프로필 baseline 8개와 Tasks 3–8의 후보 최종 snapshot.
- Produces: 8개 최종 비교의 실제 범위·성공/실패/미검사, 호환성 회귀/독립 리뷰 근거, 기본 적용/보류의 정확한 경계.

- [ ] **Step 1:** 최종 candidate source와 baseline의 의도한 diff/file/hash를 고정한다. source를 더 바꾸면 별도 epoch로 남기고 이 후보의 최종 증거를 재사용하지 않는다.
- [ ] **Step 2:** 승인 범위 안에서 동결 후보 SD01–SD08 각 1회 실행한다. 단계별 10개 출력은 형성용이며 최종 16개 baseline/candidate 쌍과 합산하지 않는다.
- [ ] **Step 3:** 같은 rubric으로 8쌍을 실제 입력/출력 locator별로 대조한다. baseline FAIL→candidate PASS만 해당 축의 관찰된 개선, 양쪽 PASS는 보존, 새 실패는 회귀, 오류/미검사는 INCONCLUSIVE다. 1회 표본을 일반 연출력·미디어 품질·통계 효과로 소개하지 않는다.
- [ ] **Step 4:** `python3 scripts/check_versions.py`, `python3 -m pytest -q`, `git -c core.whitespace=cr-at-eol diff --check`. 기대: 버전 일관성/전체 기존 회귀/공백 검사가 성공. 실패는 이름/출력과 함께 보고하고 무관한 dirty 테스트를 몰래 제거하지 않는다. 필요하면 커밋 대상 snapshot을 따로 검사해 차이를 명시한다.
- [ ] **Step 5:** 실제 일괄 모델 호출과 별도로, 선택한 실행 방식/권한에 맞는 fresh-context 최종 리뷰 1회에 spec/plan·diff·원시 출력/판정·실패/미검사 범위를 전달한다. 독립 리뷰를 못 하면 스스로 했다고 대체하지 말고 그 gate를 보류한다.
- [ ] **Step 6:** QA 보고서에 정확한 오너 변경/보존, source·프로필·횟수·판정, 구조/내용/미디어 경계, reviewer가 검사한 범위/지적 처리, 남은 권한/검증을 적는다. 중요한 신규 결함·원문/권한 위반·허위 실행 증거가 남으면 기본 적용 보류.
- [ ] **Step 7:** 후보 수정/검증 완료와 배포를 분리한다. 버전 bump·main 통합·push·전역 skill sync·실제 미디어/추가 반복 평가는 현재 사용자의 명시적 범위가 있을 때만 수행한다. 없으면 격리 후보와 보고서를 인계한다. 예: `test: record scene direction comparison and compatibility evidence`.

## 실행 체크포인트 — C2 인계

원래 step/평가 배분을 지우거나 관찰하지 않은 RED/GREEN을 채우지 않는다. 사용자 `남은 작업들을 진행해`로 원래 B 보완과 총 사례32건(기존26에서추가6)을 진행했다. Native의 추가 독립리뷰/설치·Git·미디어 권한으로 확대하지 않았다.

| 작업 | 실제 처리와 현재 경계 |
|---|---|
| 1–2 | 격리/동결·기준판/보완평가와 원본/실패/프로필 증거 보존. 과거 결과를 C2에 재사용하지 않음 |
| 3 | 기존02/03·캐릭터/04 오너 보존. C2의 공통 입력/확대 보기가 실제 세계 규칙·지식·인물 선택과 각본 발췌를 소비하도록 연결. 전문 몸통을 새로 개편했다고 주장하지 않음 |
| 4 | 보드 계약/06템플릿·비정본 예시·기존14 작업행에 열구획/상태 역대조/자원 준비 연결 구현. C1 인터페이스 RED와 실제SD09 모순을 근거로 삼음. C2 전체 보드5종 중 완료3종에서 X1 PASS, SD09/14는 시간초과로 미검증 |
| 5 | C1의 고정 음성/이번 연기→실제 AUDIO 수리 및 독립 확인 보존. C2 SD11/13·무발화/N/A 통제 PASS, 중단09/14로 새 전체 효과를 인증하지 않음 |
| 6 | 기존08/21/26 보존·통합 소비. C2 SD10에서 접촉 조건/단계·비용/환경·잔류와 실제 요청문 보존을 텍스트로 확인. 실제 동작/공간/FX 검사 아님 |
| 7 | 11에 확대 보기 소비/상태 역대조 추가. SD13의12샷/6발화·독립PERF_PACKET이3작업에 보존됨. C1 SD09 결함의 새 수정 검증은 완료 못 함 |
| 8 | 보드/12 QA 및 entry/06·14 포인터 연결. QA-only/완전 무음·정지/인계-only를 C2 SD08/03/13에서 확인. 새 validator/profile/원장 없음 |
| 9 | C2 215파일 동결·동일8입력 각1회 시도.6완료 PASS/2시간초과 INCONCLUSIVE, 원래31P/12I와 별도X1 6P/2I 분리. 최신pytest737P/4skip/525subtests·버전/공백·기존149해시 보존 확인. 독립리뷰1회는C1에서 소진, C2는Native수정패스/부모판정. 전체 수락HOLD |

총32회 시도=30응답완료+2시간초과, 허가잔여0/자동재시도0. 미완결 표본을 고쳐 성공으로 치환하지 않았다. 커밋·main통합·릴리스·설치/동기화·미디어 실행·추가 반복 평가를 하지 않는다. 현재 구현/검증/권한/수락을 분리한 인계는 `qa/scene-direction-integration/c2-final-summary.md`를 따른다. 원래 계획과 C1 리뷰 당시 버전은 보존했다.

## 계획 자체 점검

- **Spec coverage:** §§1–5 목표/범위/예외→Global Constraints·Tasks 1/4/8; §§6–8 정본·이야기/인물/각본→Tasks 2/3/8; §9 통합 상세→Task 4; §10 시간→Tasks 4/5/7; §11 에셋→Task 4; §12 보이스/음향/FX→Tasks 5/6; §13 실제 요청문→Task 7; §14 가상 예시→SD01/Task 4; §§15–16 수락/변경 영향→Tasks 7/8; §17 검증→Tasks 1/2/9; §§18–19 파일 책임/경계→각 Files/Interfaces와 최종 gate.
- **Step scan:** 문서 작업의 RED/GREEN은 실제 승인된 사례 출력/의미 대조다. 존재하지 않는 eval 명령·semantic parser를 호출하지 않고, JSON parse를 내용 검사라고 쓰지 않는다.
- **Interface consistency:** SD01–SD08/동일 입력·source version과 ten-block 명칭, 기존 project/voice/audio/state 필드를 모든 task에서 동일하게 사용한다. 새 production key 없음.
- **Review Focus coverage:** 정지/무음/오프스크린→SD03/05/08, 같은 첫끝의 중간 사건→SD02, stale/미생성→SD05/06, 시간/오디오 route→SD06/07, 정본/범위→SD01/05/08. 담당 task의 실제 관찰 기준으로 연결했다.
- **Proportion:** 이 계획은 오너별 문서 변경/평가 증거에 필요한 결정을 기록한다. 모델 런너/컴파일러 구현, 예제 프로그램 본문 또는 새 제작 엔진을 쓰지 않는다.
- **Execution handoff:** 계획 검토와 Native/Subagent-driven 선택 전 구현하지 않는다. 본 계획은 공유 템플릿/인계 계약에 순차 의존하는 9개 작업이므로 **Native + 마지막 독립 리뷰 1회**를 권장한다. 실제 평가 프로필·26회 한도/실행 권한은 Task 2의 별도 gate이며 설계 승인으로 채워졌다고 추정하지 않는다.
