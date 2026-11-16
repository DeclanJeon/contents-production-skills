# Visual Craft Reinforcement Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans for the recommended native implementation; use superpowers:subagent-driven-development only if the operator selects that execution mode. Execute task-by-task and track checkbox steps. This draft is not authorization to bypass design approval.

**Goal:** 기존 시각 연출21항목의 중복/수신처를 확인하고,8개 상세 묶음과 근거 확인 조건부3후보를 기존 에이전트 스킬의 실제 선택법·예시·검수로 연결한다.

**Architecture:** 새 독립 스킬/제작 스키마 없이 기존 오너를 유지한다. 공통 가이드는 짧은 분기만 갖고, 연기/표현과 세계규칙/정보의 두 상세 참조에 선택적 예시를 둔다. 현재 설치본이 정본 링크이므로 격리본에서 검수한 변경만 충돌 확인 후 반영한다.

**Tech Stack:** Markdown 참조/기존 템플릿, 현행 Python 설치·동기화·버전 검사/pytest, Pi native fresh-context 적용·검토. 신규 의존성 없음.

**Spec:** `docs/superpowers/specs/2026-11-16-visual-craft-reinforcement-design.md`

**Status:** completed — 2026-11-16 사용자 승인 범위의 보강·독립 검수·정본/에이전트 반영 완료. package2.45/25skills.

## Global Constraints

- 사용자 설계 승인 후 구현한다. 이번 문서 작성 단계에서는 제품·설치본을 변경하지 않는다.
- 신규 스킬 수25 유지. 새 project.json/CSV/연구 필드·경쟁 SSOT·필수 전수 분석을 만들지 않는다.
- 원본은 읽기 전용. V1–V3 새 검사 합계 최대24파일; 미확정은 deferred-source-evidence.
- 대사/언어 역할·승인 사실·의도적 모호함·고요/비서사/비인간 형식을 보존한다. 컷/초수/인체 큐 수 강제 없음.
- 실제 관찰·상속 분석·해석·제안을 구별한다. 정지 자료를 실제 시간/음향/3D/관객 효과로 확정하지 않는다.
- 기존 미커밋 변경과09-edit-template/26-state-causality-continuity/storyboard-contract,ad-rofan/continuity 작업을 보존한다.
- 유료/외부 호출·생성·업로드·게시·신규 의존성 설치·Git commit/merge/push/파괴 작업은 범위 밖이다.
- 기준선2.44를 실행 시 재확인한다. 예정 완료 버전2.45/25skills, 외부 버전 충돌은 먼저 해결한다.

## Review Focus

1. 비인간 형태/부상 제약과 행동 중단이 겹칠 때 인간 얼굴/팔을 추가하거나 접지 상태를 초기화하는 문제 → Task2/3 caseA.
2. 코믹 표현 변경을 정체성 교체·피해 소거·무조건 변형으로 처리하는 문제 → Task2/3 caseB.
3. 인물 추측·거짓말·독백을 세계 규칙으로 승격하거나 명시된 대사를 바꾸는 문제 → Task2/3 caseC.
4. 포털/효과의2D설계에서 실제3D/시간 검증을 주장하거나 이미 있는20/21/26 절차를 복제하는 문제 → Task2/3 caseD.
5. 무관한 정적 교육 영상에 서사·인물·코미디·새 필드/단계를 강제하는 문제 → Task2/3 caseE.

---

## 작업 파일·책임

- Create: `video-production-assets/references/performance-and-style-recipes.md` — R1/R2/R8, 증거 확보된V2/V3 적용 사례.
- Create: `video-production-assets/references/world-rules-and-information-recipes.md` — R3–R7, 증거 확보된V1 적용 사례.
- Modify conditionally: `video-production-assets/references/visual-scene-communication.md`의 필요한 분기; 기존02/03/04/05/06/08/12와17/20/21의 해당 오너 연결.
- Modify conditionally: `designing-character-personas/references/expression-voice-bridge.md`, `designing-video-character-sheets/references/character-craft.md`, `storyboarding-video/references/narrative-panels.md`의 실제 수신처 연결만.
- Release metadata: `manifest.json`, `CHANGELOG.md`, `README.md`, `USAGE_GUIDE.md`. SKILL 본문을 실제 바꾼 경우에만 해당 frontmatter/manifest version 동기화.
- QA root: `qa/visual-craft-reinforcement-2026-11-16/`. 출처표·실제 답안·판정·로그·배포 영수증만 저장하며 제품 지침을 QA에 숨기지 않는다.
- Existing tests: `scripts/test_video_pack_boundary.py`, `scripts/test_install_package.py`, `scripts/test_sync_installed.py`. 단순 문장 매칭을 창작 품질 시험으로 새로 만들지 않는다.

### Task 1: 승인·작업 격리와 변경 보호

**Consumes:** 승인된 spec/plan, 현재 사용자 정본과 네 설치 루트.
**Produces:** QA `source-snapshot.json`(경로/해시/버전/상태의 작업 증거), `workspace.md`(격리 경로/복구·전송 조건). 제작 스키마가 아니다.

- [x] 설계 승인 여부를 확인한다. 승인 전이면 문서만 수정하고 제품 작업을 시작하지 않는다.
- [x] `using-git-worktrees`를 읽고 현재 `git status --short`,manifest/모든 변경 대상 파일의SHA-256, 설치 링크 목표를 기록한다.
- [x] 기존 경로를 재사용/삭제하지 않는 고유 격리 작업공간을 만든다. native worktree를 쓰면 현HEAD만으로는 현재 미커밋2.44를 얻지 못함에 주의한다. 현재 tracked＋nonignored untracked 제품 파일을 읽기 전용 원본에서 overlay하고 모든 계획 대상의 원본/격리본 해시가 같은지 확인한다. `.git`·거대 연구 원본·파생support를 덮거나 외부 symlink를 따라가지 않는다. 지원되는 격리를 만들 수 없으면 중단·보고한다.
- [x] 격리본에서 `python3 -B scripts/check_versions.py`와 기존 설치/file-link 시험을 실행해 실제 초기 상태를 기록한다. 기존 실패는 새 보강 탓으로 취급하지 않는다.
- [x] 아래 Task2–4의 모든 제품 편집·baseline/loaded 적용은 격리본에서 수행한다. 실제 사용자 정본/설치 루트는 Task5까지 유지한다.

### Task 2: 출처·실제 참조 갭·편집 전 적용 기준선

**Consumes:** Task1의 동일 내용 격리본, spec의R1–R8/V1–V3, 이전 QA5개 근거 문서.
**Produces:** `source-crosswalk.md`, `cases.md`, `baseline/a.md`~`e.md`, `baseline-review.md`.

- [x] 앞21개를 실제 현재 파일/heading/기존 필드에 연결하고 `충분/접근 개선/사례 필요/보류`를 기록한다. 앞서 통과한 내용을 누락/실패로 재분류하지 않는다.
- [x] R1–R8마다 현재 참조의 실제 선택법/예시/검수 질문을 찾는다. 조회한 경로·찾은 내용/부족한 내용을 기록한다. 참조 부재와 실제 창작 출력 실패는 다른 열/서술로 구분한다.
- [x] V1–V3의 후보 위치를 기존 기록/메타데이터로 좁힌 뒤 합계24원본 이내의 연속 구간을 직접 연다. 정확 경로/영역·관찰·한계·독립 읽기 여부를 남긴다. 제목/워터마크/패널 파일 경계를 사건으로 세지 않는다.
- [x] 각 V를 `evidence-backed/추가 맥락 필요/deferred-source-evidence`로 결정한다. 전/중/후가 없으면 변신/시간층/분업을 확정하지 않는다. 한도에서 못 찾으면 그대로 보류한다.
- [x] `cases.md`에 spec A–E를 원작과 다른 새 브리프로 고정한다. A는 얼굴/별도 팔 없는 승인 형태와 지지 과제, B는 유지할 상처/물체·허용 변형, C는 명시된 허구 규칙/고정 대사/추측, D는2D전용 경계/효과 조건, E는 승인 내레이션·도표·단일 정적 화면을 명시한다. 출력은 요청한 러프/단일 모듈 범위로 제한한다.
- [x] fresh context 한 호출당 한 사례로 편집 전A–E 답안을 저장한다. 현재 오너/관련 참조만 읽게 하며 새 설계·평가표·원본 QA를 답안에 미리 주입하지 않는다. 병렬 실행은 읽기 전용, 동시 최대2개로 제한한다.
- [x] 실제5개 본문을 읽고 구체적 선택·누락·실패/이미 좋은 부분을 기록한다. 실패가 없으면 새 금지/강제 문구를 만들지 않고 실제 참조 갭/선택적 예시 보강만 한다. 참조/예시 조회 실패를 행동 RED로 보고하지 않는다.

### Task 3: 조건부 레시피와 기존 수신처 구현

**Consumes:** Task2 실제 갭/원본 상태/고정 사례. **Produces:** 새 참조 두 개와 필요한 최소 오너 포인터, `change-map.md`.

- [x] 편집 전 각 변경을 `현재 부재한 reference/technique 예시 / 접근성 / 실제 행동 결함`으로 명명하고 대응 증거를 고른다. 기계적 검사/코드를 정말 변경할 때는 해당 테스트의 실제 RED부터 확인한다. 새 강제 행동을 제안하면 spec의 별도 microtest 조건을 충족한 뒤에만 채택한다.
- [x] R1/R2/R8의 상세 참조를 작성한다. 각 레시피는 조건·독립 창작 전후 예시·대안/득실·기존 수신 필드·오독과 최소 수정·미검증 범위를 함께 둔다. R1은 몸 구조/부상 제한, R2는 정체성/피해 및 필요한 복귀, R8은 기존 지지/과제 상태가 핵심이다.
- [x] R3–R7의 상세 참조를 같은 구조로 작성한다. 세계 규칙/관찰/믿음을 구별하고, 포털20·효과21·유지26 절차는 복제하지 않고 정확 heading에 연결한다. 원작의 고유 규칙/인물/구도를 새 예시에 복사하지 않는다.
- [x] 증거가 확보된V1–V3만 해당 상세 참조의 사례로 통합한다. 원작에서 확인하지 못했지만 독립적 일반 제안으로 유용한 내용은 ‘source-derived’로 승격하지 말고 이번 채택에서 보류한다.
- [x] 공통 가이드와 실제 필요한 오너 수신처에 상황별 포인터를 추가한다. 기존 동등 포인터가 있으면 유지하며 상위 조정자에 새 기본 연구/제작 단계를 만들지 않는다. 표정/룩/행동 예외는 기존 SSOT/필드로 받는다.
- [x] 템플릿을 실제 읽고 필드명을 그대로 인용했는지 확인한다. 가짜 신규 field/별도 원장/음성 없는 역할의 보이스 요구를 제거한다. 변경 이유와 정확한 수신 경로를 `change-map.md`에 남긴다.
- [x] 같은 A–E를 fresh context로 실행해 `loaded/a.md`~`e.md`에 실제 답안을 저장한다. 단일 Markdown bound output에는 구조화 JSON만 덮어쓰는 outputSchema를 결합하지 않는다.
- [x] 실제10개 본문을 전부 읽어 사례별 적합성/차이/수정 필요를 `application-review.md`에 기록한다. 기존과 신규가 모두 좋으면 그대로 보고하고 우월성/인과적 개선을 주장하지 않는다. 각 적용 가능 R은 구체적인 새 화면/행동 선택이 있고 E는 비적용 범위를 보존해야 한다.

### Task 4: 패키징·회귀·독립 최종 검수

**Consumes:** Task3 구현·실제 답안·V상태. **Produces:** 로그·단일 독립 검수 보고와 수정/재검수 증거.

- [x] README/USAGE_GUIDE에 필요한 경우의 사용법과 계획/스틸/재생 검사 구분을 갱신한다. CHANGELOG에는 실제 채택된 R/V만 기록한다.
- [x] 기준선2.44가 유지된 경우 `python3 -B scripts/bump_version.py 2.45`로 패키지 버전을 올린다. `--bump-skills`로 전 스킬을 무차별 범프하지 않는다. 실제 SKILL 본문 변경이 있으면 그 스킬의 version/manifest만 동기화한다.
- [x] `python3 -B scripts/check_versions.py` 실행, 실제2.45/25skills 일치 확인.
- [x] `pytest -q scripts/test_video_pack_boundary.py scripts/test_install_package.py scripts/test_sync_installed.py` 실행. 새 참조가 실제 임시 설치에 포함되고 상대 링크가 설치 루트 안에서 해소돼야 한다. 출력/exit code 저장.
- [x] `pytest -q` 전체와 `git diff --check` 실행, 실제 수치·skip·실패/기존 실패를 기록한다.812개라는 과거 수치를 결과처럼 복사하지 않는다.
- [x] fresh 검토자1명에게 spec/plan·변경 파일·실제10개 답안·V결정·소스/해시/로그를 제공한다. 요구/품질/중복/범위/관객 효과 주장/실제 필드·설치 경로를 검수하고 구체 Important/Critical을 보고하게 한다. 원본을 직접 보지 않았다면 그 한계를 명시한다.
- [x] 실제 중요 결함만 국소 수정하고 영향받는 사례·검사를 재실행한다. 독립 scoped 재검수에서 미해결 Important/Critical0을 확인한다. 끝없는 새 연구/패널·지표 추가를 검수 조건으로 수용하지 않는다.

### Task 5: 사용자 정본과 에이전트 설치 경로 반영

**Consumes:** 승인된 Task4 결과, Task1 원본 해시. **Produces:** `deployment-receipt.md`, 갱신된 사용자 정본/파생support와 일치하는 설치 링크.

- [x] 전송할 **이번 작업 소유 변경 파일 목록만** 확정한다. 각 기존 파일의 사용자 정본이 Task1 해시와 같은지 확인한다. 기존 보호 파일은 수정하지 않았으면 해시가 같아야 한다.
- [x] 달라진 원본이 있으면 해당 파일 전송을 중단하고 diff를 보존해 충돌 결정을 받는다. 다른 작업자의 수정이나 전체 디렉터리를 덮어쓰지 않는다.
- [x] 확인된 파일만 정본에 정밀 반영한다. 실제 정본에서 version/file-link 및 diff 검사를 실행해 격리본과 다른 위치에서도 유효함을 확인한다. 전체 파일 내용/변경 목록과 동일성을 영수증에 남긴다.
- [x] 다음 dry-run을 실행해 예상 밖 repoint/displace가 없는지 확인한다.
  `python3 -B scripts/sync_installed.py --dry-run --root /home/declan/.codex/skills --root /home/declan/.claude/skills --root /home/declan/.agents/skills --root /home/declan/.pi/agent/skills`
- [x] 예상대로 현재 정본 링크를 유지할 때만 같은 명령에서 `--dry-run`을 빼서 파생support를 갱신한다. 예상 밖 실체 폴더/링크 변경이면 승인 없이 교체하지 않는다.
- [x] 네 루트의25스킬 링크 목표·신규 참조 SHA-256·파생 manifest 일치를 실제 확인한다. Git commit/merge/push는 하지 않는다.
- [x] 완료 보고에 채택된8묶음별 결과와V1–V3의 채택/보류, 실제 테스트·검수 범위·잔여 미검증을 적는다. 실행 중 Pi는 `/reload`/새 세션이 필요하며 파일 배포와 스킬 목록 재로드를 분리해 설명한다.

## 문서 자기 검토 / 구현 시작 조건

- [x] spec의 기존21·R1–R8·V1–V3·후보 한계·보존·배포·검수 각각에 담당 Task가 있는지 확인했다: Task2/3 출처·선택·적용, Task1/5 보존·배포, Task4 독립 검수.
- [x] 경로/recipe ID/오너 이름·case A–E·예정 버전과 spec의 일치를 자기 검토했다. 문서 대조이며 구현·실제 적용 통과를 뜻하지 않는다.
- [x] 사용자 ‘진행하자.’로 설계/작업지시서와 순차 직접 구현＋단일 독립 최종검수 방식을 승인받았다.

Task1–5 완료. 실제 진행/판정·보존·설치 결과는 [완료 영수증](../../../qa/visual-craft-reinforcement-2026-11-16/deployment-receipt.md)과 이 계획의 작업공간 ledger에 기록했다. 실제 생성 매체/재생·관객 효과의 검증은 아니다.
