# C2 첫 묶음 중단과 미실행 과제의 계속

**아래는 첫 묶음 종료 당시 이력이다.** 현재는 원래8건을 모두 시도해6 PASS/2시간초과 INCONCLUSIVE로 인계했고, 총32회 소진/추가실행없음이다. 두 번째 중단SD09와 최종 결과는 [C2 최종 요약](c2-final-summary.md)에 기록한다.

- C2 동결 소스/입력·모델/high/fresh/600000ms는 그대로다.
- workflow `d5aa7ffc-13b5-466e-a482-19bc7dcc3af6`은 두 과제 뒤 **BLOCKED**로 종료했다. 실패 뒤 멈추고 사용자에게 보고했으며 원시 기록/해시를 보존·확인했다.

| 사례 | 실제 실행 | 부모의 내용 판정 |
|---|---|---|
| SD13 | 완료, 172510ms, read12회 | 잠긴 콘티 인계 통제: 원래6관찰 PASS, 별도X1 범위 보호 PASS. 독립 리뷰/전체 확대 보드 검증이 아님 |
| SD14 | 600000ms 제한으로 시간초과, read35회, 부분452행 보존 | 원래6관찰 및 X1 INCONCLUSIVE. 스트림 중단을 창작 FAIL이나 완료 PASS로 치환하지 않음 |
| SD12/11/10/09/08/03 | 첫 workflow에서는 **미실행** | 아직 UNREVIEWED |

Native SD14는 `Subagent timed out after 600000ms.`, 최종 assistant 이벤트는 `stopReason=aborted`이다. 부분 본문에는 네 샷의 확대 보기와 실제 VISUAL/AUDIO가 보이나 마지막 QA 행에서 잘렸다. **확인된 직접 원인은 실행 deadline의 중단이며**, 특정 공급자 장애/출력 토큰 상한/템플릿 길이가 원인이라는 인과까지 확인한 것은 아니다. 로그에 없는 API 상한·청구액을 추정하지 않는다.

215개 동결/작업 소스의 해시가 일치한다. 두 과제 모두 고정 소스 안의 read만 사용했고, 다른 모델·CLI/외부 조회·파일/미디어 생성·추가 리뷰는 없다. 런타임 보고 비용은 합계 USD0.6881708이며, 실패 스트림의 사용량은 불완전할 수 있고 청구서 대조값이 아니다.

## 계속할 범위

현재 **26회 시도 = 25회 응답 완료 + 1회 시간초과**, 승인 한도32에서6회가 남았다.

- 실패한 SD14와 완료한 SD13은 **재실행하지 않는다**.
- 부모가 중단/보존/범위·프로필/해시를 확인한 뒤, 원래 승인된 **아직 한 번도 실행하지 않은 여섯 과제만** 같은 동결 입력/소스·600000ms에서 이어간다. 새 예산·프로필/소스 변경·실패 표본 대체가 아니다.
- 추가 workflow도 실패 시 멈추고, 자동 재시도/CLI 대체는 하지 않는다.
- SD14의 실패 기록과 미확인 판정은 최종 요약에도 남는다. 시간초과를 없었던 것으로 만드는 추가 호출·시간제한 변경은 별도 승인이 필요하다.
- 원래43관찰과 별도X1 여덟 개는 분리한다. 첫 묶음 현재 원래6 PASS/6 INCONCLUSIVE/31 UNREVIEWED, X1은1 PASS/1 INCONCLUSIVE/6 UNREVIEWED다.

소스 구현/정적 호환성 검사와 전체 새 동작 통과는 별개이며, **현재 전체 B 검증 완료/배포 가능으로 보고하지 않는다**.

보존 위치: `<worktree>/.superpowers/sdd/2026-11-14-scene-direction-integration/epoch-e2/final-c2-outputs/`, `final-c2-first-batch-audit.json`, `final-c2-status.json`, `final-c2-workflow-receipt.json`, `case-run-accounting-c2-first-batch.json`. 이 로컬 원시 증거는 gitignored이며 삭제·업로드하지 않았다.
