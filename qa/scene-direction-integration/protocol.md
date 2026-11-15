# Scene Direction Integration V1 — 실행 프로토콜

## 현재 상태와 권한
Task 1 준비 뒤 Task 2 기준선 실행 단계다. 사용자는 `응 진행해보자.`로 아래 현재 모델/high·최대 26개 텍스트 과제 실행을 승인했다. Native 구현과 최종 독립 리뷰 1회는 앞서 선택했다. 실제 실행 건수/상태는 계획 전용 run ledger와 native receipts를 따른다. 승인 사실만으로 실행/검사 완료를 표시하지 않는다.
Git 커밋·main 통합/push·전역 설치·버전 릴리스·실제 이미지/음성/영상·유료 미디어·외부 업로드는 이 승인에 포함되지 않는다.

## 승인된 실행 프로필 — 실제 실행 성공은 receipt로 별도 확인
- 도구: 현재 제공되는 native Pi subagent, 동일 delegate 역할, fresh context. 구현은 계속 부모가 Native로 수행하고 아이들은 과제 응답만 만든다.
- 정확 모델: openai-codex/gpt-6.1-sol, thinking high를 명시. 실제 baseline 8건의 native status에서 이 모델/high/fresh/600000ms와 완료 상태를 확인했다. 다른 조건/후보/미디어 성공을 뜻하지 않는다.
- 과제: 고정 SD01–SD08. 생성 사용자 본문은 각 user_request와 supplied_context의 동일 UTF-8 직렬화 바이트뿐이다.
- 권한: 고정 source snapshot의 로컬 지침/템플릿 읽기와 텍스트 응답만. 원본 dirty checkout/설치된 skill 본문/인터넷·MCP/외부 원본 이미지/비밀/다른 평가 답안·루브릭·spec/plan 열람, 파일 수정·CLI/미디어/하위 delegation 없음.
- 파일 읽기는 실제 제공 read 도구로 수행하고 source root 아래의 고정 자료만 사용한다. 자식의 output=false로 제작 파일/보고서 직접 쓰기 지시를 주지 않고 최종 텍스트를 반환하게 한다. 런타임이 자동 보존하는 로그/워크플로 출력은 전송 증거이며 제작 산출물이 아니다. 실제 native artifact 경로를 기록하고 필요한 최종 응답/도구 영수증을 이 계획의 evidence root에도 보존한다. 도구/역할이 이 제한을 실제로 구현하지 못하거나 snapshot 밖 열람이 생기면 환경 오염으로 기록하고 해당 결과를 유효 비교에서 제외한다.
- 종료: 테스트 실행당 10분의 run-level deadline, 앱 수준 자동 재시도 0회. 실패/중단 뒤 조용한 CLI·모델 대체 금지. 새로운 재실행은 새 허가와 epoch를 요구한다.
- 응답 길이: 모델/하네스 기본 상한을 사용하며 실제 적용값이 노출되면 manifest에 기록한다. 짧게 자르는 별도 toolBudget/maxOutput을 걸지 않는다. 잘림/중단은 INCONCLUSIVE로 남기며 누락을 craft FAIL로 위장하지 않는다.
- 규모: 기준선 8 + 형성용 후보 10 + 동결 후보 8 = 최대 **26개 과제 실행**. 각 에이전트는 지침을 읽기 위해 여러 모델/도구 턴을 쓸 수 있으므로 '26 API 요청' 또는 확정 토큰/금액 상한이라고 부르지 않는다. 실제 모델 요청/사용량/금액은 receipt가 제공하는 범위에서 따로 기록하며 알 수 없으면 미확인이다.
- 과제별 컨텍스트/토큰 양과 실제 요금은 미확정이다. 이 규모·기본 출력 한도를 사용자가 승인하지 않으면 시작하지 않는다. 명시적 금액 상한이 필요하면 가능한 도구의 실제 강제력을 먼저 확인한다.
- 최종 독립 리뷰는 별도의 fresh-context 리뷰 1회이며 26개 생성 결과에 포함하지 않는다. 이미 선택한 실행 범위 안에서, 실제 사용 모델/검사 범위/receipt를 별도로 남긴다. 추가 판정 에이전트/리뷰 패널은 자동 실행하지 않는다.

## 1. 격리/출처 동결
1. 계획 전용 worktree를 사용한다. 초기 BASE: 0e1d9f343fa2bec0d00421ed2cf4488abd41888c. 원본 dirty 변경은 baseline에 합치지 않는다.
2. baseline은 후보 수정 전의 tracked package source로 고정한다. snapshots에 평가 자료/spec/plan·다른 실행 결과/개인 설정을 넣지 않는다. 허용된 지침/템플릿/로컬 참조 파일의 경로·바이트·SHA-256·기준 commit/제외 범위를 manifest에 적는다.
3. generator에는 같은 skill 발견/진입 방식과 허용 읽기 도구·source root만 준다. owner_paths는 준비자의 소스/커버 확인용이며 정답·required_observations·rubric/locks/forbidden_expansions와 함께 숨긴다. 조건마다 다른 전문 힌트로 유도하지 않는다.
4. 실제 dispatch 본문·source manifest·고정 사용자 입력·프로필·권한/기한과 SHA-256을 실행 전에 저장한다. 실제 사용 버전/읽은 파일·외부 오염 여부를 transcript로 확인한다.
5. 최종 후보는 모든 변경/검토 뒤 별도 epoch로 동결한다. source/입력/프로필 중 하나라도 바뀌면 이전 최종 결과를 재사용하지 않는다.

## 2. 순서와 입력 동일성
- baseline SD01→SD08을 모두 수집/검토한 다음에만 생산 지침을 편집한다.
- 형성용 10개: Task 3 SD01/08, Task 4 SD02/03, Task 5 SD05/06/07, Task 6 SD04, Task 7 SD06, Task 8 SD08. 해당 부분의 판정만 기록하며 아직 완성되지 않은 전체 후보의 통과로 승격하지 않는다.
- 최종 동결 후보는 SD08→SD01로 수집한다. 전후 조건 교대/동시 비교를 했다고 주장하지 않는다. mandatory RED-before-authoring 때문에 기준선 선행이며 시간에 따른 모델 drift는 한계다.
- user_request/supplied_context의 문구·순서/인코딩·source 발견 조건·모델/설정/역할/도구·출력 한도는 조건 간 동일하게 한다. 의도된 차이는 snapshot의 후보 지침/템플릿 내용뿐이다.
- baseline의 기존 PASS를 실패로 만들지 않는다. 실제 FAIL 없이 PASS/입력 부족에 따른 미확인만 남아도 결함/개선 효과를 꾸미지 말고 설계 적용의 실증 범위를 사용자와 재확인한다. 현재 8건은 7 PASS / 1 INCONCLUSIVE이며 후보 편집·추가 호출은 보류 중이다.

## 3. 증거와 상태
실행별로 run_id/case_id/condition/epoch, profile, dispatch/input/source/output hashes, 호출 시작/종료·run deadline·실행 상태, 전체 최종 응답·도구 transcript/receipt, 제공된 사용량/비용을 보존한다. 추론 비공개 내용/비밀·외부 이미지 원본을 수집하거나 QA 보고서에 공개하지 않는다.
- execution_status: NOT_RUN / COMPLETED / FAILED / TIMED_OUT / CANCELLED. 이들은 QA 기록용이며 project.json enum이 아니다.
- 실제 모델 출력이 없거나 source/프로필이 다르거나 오류/중단·잘림이면 완료한 동일 조건 출력으로 치환하지 않는다. 문제 범위는 INCONCLUSIVE, 미검토는 UNREVIEWED다.
- 유효한 완료 출력은 rubric.md의 개별 관찰 기준으로 실제 위치/인용·영향·최소 수정과 판정을 기록한다. 실패 raw와 형성용 결과를 삭제/덮어쓰지 않는다.
- 검토 카드는 각 case의 required_observations를 criteria로 복사하고 verdict를 UNREVIEWED로 초기화한다. JSON parse나 양식 존재로 PASS를 채우지 않는다.
- 산출물 상태와 실행 권한·실제 청취/재생/사용자 수락은 각기 다른 증거를 요구한다.

## 4. 보존 위치/최종 보고
검토용 원시 자료는 <worktree>/.superpowers/sdd/2026-11-14-scene-direction-integration/ 아래에 이 계획만의 epoch별로 보존한다. native runtime의 자동 session/artifact 원본은 receipt가 제시한 경로에도 존재할 수 있으며 숨기거나 외부 공개하지 않는다. 처음 정한 evidence root 밖으로 조용히 저장하지 않는다. 이 ignored 자료는 Git이 백업하지 않으므로 인계 때 경로/보존 상태를 알린다. 사용자 승인 없이 삭제/업로드하지 않는다.
공개 QA 요약은 실제 evidence locator와 source/profile/횟수·실패/미검사·독립 리뷰 범위를 명시한다. 8쌍을 기준으로 한 관찰별 결과만 비교하며 형성용 10개를 최종 표본에 더하지 않는다. 회귀/원문·권한 위반/허위 실행 증거가 있으면 기본 적용을 보류한다.
버전 검사/전체 pytest/문서 공백 검사와 실제 행동 비교를 따로 보고한다. 실제 미디어/청취/공간 품질 향상은 이 텍스트 평가로 검증되지 않는다.

## 5. 훅/설치 보호
공유 Git post-commit/post-merge/post-rewrite가 전역 sync를 할 수 있다. 이 후보는 현재 미커밋 상태로 유지한다. Git 커밋이 별도 허가되면 계획에 적힌 sync 없는 명령 전용 hooksPath에서 기존 버전 검사를 유지하고 실행한다. 원본 checkout/설치 symlink/전역 Git 설정을 바꾸지 않는다.
