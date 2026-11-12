# Matt writing integration — offline tooling milestone (G1)

상태: **Task 1–3 오프라인 구현/테스트 완료; 전체 통합은 미완료**. 실제 provider 호출, 140회 모델 평가, 콘텐츠 스킬 편집, 설치본 동기화, 커밋/배포는 하지 않았다. Task 4의 실행 오케스트레이터도 아직 구현하지 않았다.

## 작업 위치와 원본 경계

- Worktree: `../contents-production-skills-matt-writing-craft`, branch `feat/matt-writing-craft`.
- 계획: [implementation plan](../superpowers/plans/2026-11-11-matt-pocock-writing-craft-integration.md).
- 설계: [design v0.2](../superpowers/specs/2026-11-11-matt-pocock-writing-craft-integration-design.md).
- 출발점: HEAD `968b571`에 원본의 현재 tracked/untracked 파일 1178개를 복사한 dirty snapshot. `.git`, 캐시, `.omo/.omx`, derived support는 제외했다.
- 이번 구현에서 기존 파일을 바꾼 것은 `scripts/run_guide_behavior.py` 하나다. 다른 기존 runtime skill 파일은 복사 당시와 같다. 신규 QA/도구 파일과 이 보고서는 worktree에만 있다.
- 작업 말미 원본의 다음 10개 파일이 복사 기준과 달라졌음을 관찰했다. 변경 주체는 확인하지 않았으며 자동 병합/되돌리기를 수행하지 않았다: CHANGELOG.md, README.md, USAGE_GUIDE.md, creative-production/references/production-routing.md, integrations/package-provenance.md, integrations/skill-routing.md, video-production-assets/SKILL.md, video-production-assets/references/03-screenplay.md, video-production-assets/references/12-qa.md, video-production-assets/references/22-dialogue-lipsync.md.
- 이 테스트 결과는 **격리 worktree의 출발점+이번 delta**에 대한 것이다. 원본 최신 트리에 대한 통과 판정이 아니다. 후속 통합/평가 전에 이 차이를 다시 대조한다.

## 구현한 기능

1. `qa/matt-writing-inputs.json`: 설계에서 추출한 고정 입력 14개. `matt-writing-rubric.json`은 별도 평가자 자료이며 입력 파서가 rubric/expected 필드를 거부한다.
2. `writing_eval_cases.py`: frozen Pydantic 입력 검증, 정확한 T ID/오너/회차 수, 단일 응답 변환. 기존 실행기의 G/F 경로·도구 권한은 유지하고 T09/T11/T12의 잘못된 단일 실행을 차단했다. legacy 오너 데이터는 `guide_eval_routes.py`로 옮기되 기존 `runner.OWNER` 접근은 유지했다.
3. `writing_eval_transport.py`, `writing_eval_rpc.py`: 같은 RPC 자식 프로세스에 후속 메시지 전달, 응답 ID 상관관계, LF framing, accepted/agent_end와 settled 구별, 자동 retry/compaction 비활성화, bounded process cleanup, 회차별 raw/응답/입력 해시/소스 지문. malformed/handled/aborted/timeout은 INCONCLUSIVE이고 실행 성공도 UNREVIEWED다.
4. `writing_eval_fixture.mjs`: 실제 초기 전체 읽기 완료 뒤 사용자 수정 삽입, 재읽기 전 쓰기 차단, 한 파일만 수정, 경로/symlink 탈출 거부, 사용자 수정·인접 파일 보존, 초기 세션 생성까지 포함한 deadline와 늦게 생성된 세션 폐기.
5. `writing_eval_sandbox.mjs`, `writing_eval_sdk.mjs`: Linux bwrap 명령·실제 외부 sentinel 쓰기 거부 probe, readonly mount와 명시 승인 없이는 SDK 제출 거부, 정확 provider/model·제한된 custom tools·in-memory session/resource/settings 구성을 사용하는 SDK 연결 코드. **실제 모델/SDK 세션의 end-to-end 동작은 실행하지 않았으므로 미검증**이다.

## 실제 검증 결과

| 검사 | 관찰 결과 | 증거 |
|---|---|---|
| 복사 직후 버전/전체 회귀 | package 2.33 / 22 skills, 415 passed / 518 subtests passed | 아래 workspace의 version-baseline.log, pytest-baseline.log |
| Task 1 RED→GREEN | 새 사례 모듈 미존재 및 잘못된 직접 단일 실행으로 실패를 확인한 뒤 통과 | task-1-red.log, task-1-direct-red.log, task-1-tests.log |
| RPC RED→GREEN | 새 어댑터 미존재 실패 후 실제 가짜 subprocess로 history/프레이밍/종료 검사 통과 | task-2-red.log, task-2-tests.log |
| malformed RPC 회귀 | int text로 legacy parser가 TypeError를 내는 실패 재현 후 INCONCLUSIVE·raw 보존으로 수리 | task-2-malformed-red.log, 최종 Python suite |
| fixture RED→GREEN | 새 모듈/bridge 미존재 실패 후 경로·이벤트·사용자 편집·누락/abort/timeout 검사 통과 | task-3-red.log, task-3-bridge-red.log, task-3-green.log |
| deadline 회귀 | 세션 생성 시간이 deadline에서 누락되는 실패 재현 후 늦은 prompt 차단·dispose 확인 | task-3-deadline-red.log, task-3-green.log |
| 최종 전체 Python 회귀 | **436 passed / 518 subtests passed** | final-python-tests.log (registry 분리 후) |
| 최종 Node suite | **11 passed, 0 failed** | final-node-tests.log |
| bwrap capability | harmless namespace probe 성공; 별도 sentinel 쓰기가 거부되고 원문 보존됨 | Node suite의 sandbox probe; live provider 검증은 아님 |
| Python 규칙 감사 | 신규·수정 Python 7개 파일에서 no violations | python-audit.log |
| basedpyright | **0 errors, 24 warnings, exit 1**. 경고가 있으므로 타입 검사 전체 통과로 보고하지 않음 | python-types.log, pyrightconfig.json |
| 독립 리뷰 | 도구 미제공으로 BLOCKED. 저자의 검사·테스트를 독립 승인으로 바꾸지 않음 | progress.md |

위의 실제 기록 폴더는 [plan workspace](../../.superpowers/sdd/2026-11-11-matt-pocock-writing-craft-integration/)다. Git에 포함되지 않는 로컬 증거이므로 이 worktree를 삭제하지 않는다. 커밋 범위가 비어 있는 것은 요청하지 않은 Git 커밋을 하지 않았기 때문이며 ledger의 `968b571..968b571`이 코드 변경 없음이라는 뜻은 아니다.

## 구조·타입 자체 점검과 남은 사항

입력 검증, RPC IO, 대화 생명주기, 통제 fixture, sandbox, SDK bridge의 책임을 분리했다. 새 입력은 타입 경계에서 파싱하고 기존 legacy trace는 소비 전에 Pydantic 모델로 검증한다. 새 코드에 Any/cast/type-ignore 우회는 추가하지 않았다. 타입 경고에는 legacy 함수의 미지정 타입, 새 클래스 속성 타입 표기와 미사용 반환값 경고가 포함돼 있다. 코드 크기는 모두 250 pure LOC 이내이며 기존 실행기는 243줄로 경고 구간(200–250)에 있다. 다음 증분에서 커지면 추가 분리를 검토해야 한다. ruff 실행 파일은 발견되지 않았으며 자동 설치하지 않았다.

다음은 Task 4의 dry-run/반복 집계·루브릭 증거 검증 준비, 모델/provider·예산·재시도 상한 확인, 실제 baseline이다. 실제 FAIL이 확인되지 않았으므로 `writing-craft.md`나 기존 콘텐츠 지침을 앞서 작성하지 않았다. 전체 완료에는 candidate 비교·설치 회귀·독립 리뷰가 더 필요하다.

## 기록한 판단

- `.worktrees`가 ignored가 아니어서 외부 sibling worktree 사용. 비용/위험: 경로가 선호값과 다를 뿐 원본 .gitignore/커밋은 변경하지 않음.
- `python` 부재로 `python3` 사용. 비용/위험: 인터프리터 차이; 해당 인터프리터에서 실제 전체 baseline/회귀를 검증함.
- 계획의 raw dict 입력 대신 frozen Pydantic/dataclass/TypedDict 경계 사용. 비용/위험: 어댑터 변환 유지보수; wire JSON 계약은 동일함.
- transport·sandbox·SDK bridge를 작은 추가 모듈로 분리. 비용/위험: import/패키징 경계가 늘어남; 오프라인 테스트로 연결을 검사함.
- 기존 실행기가 크기 제한을 넘어 legacy 오너 데이터를 `guide_eval_routes.py`로 분리하고 기존 import 접근을 보존. 비용/위험: stdlib-only import 한 곳 추가; 분리 전 집중 테스트 33개와 분리 후 전체 회귀가 통과함. 독립 Plan-agent/LSP 도구는 없어 해당 도구의 검증을 수행했다고 주장하지 않음.
- entrypoint-style 스크립트의 타입 검사 root를 scripts/로 지정. 비용/위험: 다른 import 문맥은 명시적 runner/PYTHONPATH가 필요함; source 진단을 숨기는 옵션은 넣지 않음.
