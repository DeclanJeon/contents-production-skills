# 상태·인과 인계 보강 QA

## 범위와 결과

문서·템플릿만 보강했다. 기존 실행 코드·프로젝트 스키마·버전·공급자 라우팅은 변경하지 않았다. 새 26 가이드는 선택 조건과 최소 인계 슬롯, 09는 시간/획득, 25는 레퍼런스/역추정, 21은 실제 QA 판정을 소유한다.

**명세/품질 리뷰 APPROVE, 아키텍처 WATCH, 통합 권고 COMMENT.** 해결하지 않은 기능 결함은 없으며 WATCH는 하나의 공통 계약과 여러 실무 템플릿이 장기적으로 어긋날 수 있다는 비차단 유지보수 위험이다. 이것은 제작 영상 승인이나 모델 생성 품질 개선을 뜻하지 않는다.

## 실제 수행한 검증

| 검사 | 관측 결과 | 범위/제한 |
|---|---|---|
| 업데이트 전 fresh-context 적용 5회 | 기존 상태·접촉 인과·가림·불명 시간·인터뷰 N/A를 처리 | `qa/state-causality-baseline.json`. 핵심 기존 기능 실패를 재현하지 않았으므로 개선율을 만들지 않음 |
| 첫 통합 적용 5회 + held-out 4개 | 변화/보존·후속 상태, 수선의 가림, 미상 렌즈/획득 시간, 텍스트 인터뷰, 관찰된 결합 실패 vs 미검사 응답을 구분 | `qa/state-causality-post.json`. 실제 매체가 없는 지시 적용 평가 |
| 리뷰 수정 후 동일 적용 5회 | 기존 핵심 동작과 비적용·미검증 경계 유지 | `qa/state-causality-final.json`. 응답과 컨텍스트 SHA-256 보관 |
| 표적 회귀 2개 | 정지/가림 후속 컷의 상속 의무를 유지하고 SH05의 보고된 리셋 오류를 needs_revision으로 인계; 의도적 생략으로 필수 방울 시연 누락을 통과시키지 않음 | 동일 final JSON. 실제 검사자의 제공 관찰과 모델의 직접 검사 없음 구분 |
| 기존 전체 pytest | **118 passed, 156 subtests passed, 2 warnings**, 3.78초 | 명령 `python -m pytest -q`, 출력 `artifact://62`. 두 Windows subprocess UTF-8 디코딩 thread 경고는 기존 설치 테스트 경로에서 발생; 숨기거나 범위 밖 수정하지 않음 |
| 버전 pre-commit hook | working package 2.4, 17 skills consistent | 설계 커밋 a3cb49e의 실제 hook 출력. 사용자 기존 release 변경은 본 작업 커밋 대상 아님 |
| 로컬 Markdown 파일 링크 | 62개 target 존재, 누락 0 | `qa/state-causality-static.json`. anchor·외부 URL·영상 품질 검증이 아님 |
| 설치 surface smoke | Codex/Claude/Agents의 video-production-assets 모두 이 저장소로 resolve; 새 26 guide 존재·해시 동일 | static JSON. 재복사 없이 junction을 통해 현재 내용을 읽음 |

모델 응답은 합성 시나리오의 **지시 적용 근거**다. 실제 영상 생성·동작 성공·시청·청취·성과 검증으로 승격하지 않는다. baseline 원문은 tool artifact에서 복구했으며 kernel 소실로 pre-edit 컨텍스트 해시는 보존하지 못했다. 재구성한 해시나 별도 원시 프로토콜 완전성을 주장하지 않는다.

## 독립 리뷰와 해결

- `CodeReviewLane`: 최초 REQUEST CHANGES, MEDIUM 2개. 26의 무조건 N/A가 이전 변화의 유지 범위를 끊을 수 있었고, 21의 생략 허용 문구가 필수 시연을 면제하는 것으로 읽힐 수 있었다.
- 수정: 26/11/21의 활성 조건에 **상속된 유지 의무**, 문서화된 리셋까지 모든 해당 후속 경계·재등장 대조를 추가. 승인된 생략도 브리프/관객 인과를 충족해야 하며 필수 행동 누락은 needs_revision, 보이지 않은 동작 자체는 unverified.
- 같은 독립 품질 lane 재검수: **APPROVE**, 남은 actionable defect 없음. 근거: 26:7/18/28, 11:17, 21:80–87, 선택 템플릿:3–15.
- `ArchitectureLane`: 재검수 **WATCH**, 필수 수정 없음. 상세 실행 절차 복제·새 스키마/ID 네임스페이스 없음. baseline 텍스트가 잘렸다는 초기 우려는 read 도구의 축약 표시에 따른 것으로 철회했다.

리뷰 결과 원본: `agent://CodeReviewLane`, `agent://ArchitectureLane`; 영구 근거는 `qa/state-causality-reviews.json`에 저장한다. 두 lane 모두 작성 lane과 별개이며 검사·테스트·편집을 수행했다고 주장하지 않았다.

## AI SLOP CLEANUP REPORT

- Scope: 이번 새 가이드/템플릿과 기존 가이드 추가 구획만. 사용자 이전 편집 제외.
- Behavior Lock: baseline 5회, 첫 통합 5회+대조 4개; 리뷰 지적은 그대로 수용하고 수정 후 5회+표적 회귀 2개 확인.
- Cleanup Plan: 독립 CodeReviewLane 제안 → masking pass 해소 → 불필요 ID 제거 → 필드/소유 경계 정리 → 지시 smoke 재검증.
- Fallback Findings: 의도적 생략을 pass 근거로 삼는 문구 = masking fallback, 제거. 실제 응답 미검사/가림/미상 촬영 근거 = 정당한 증거 경계, 유지.
- Passes: 불필요 `state_contract_id` 삭제; 기존 artifact/shot ID 재사용 및 no-new-project.json-fields 명시; 누락된 허용 변화 슬롯 추가; 무조건 N/A/생략 허용 수정. 실무 템플릿의 같은 필드는 사용 인터페이스라 유지하고 새 전역 원장/실행 abstraction은 만들지 않음.
- Quality Gates: 기존 pytest PASS; 실제 지시 적용 및 파일 링크/설치 smoke PASS. 코드 lint/typecheck/build/security scan N/A(실행 코드 변경 없음). UI/design N/A(이번 스킬 문서 변경).
- Remaining Risks: 26과 09/11/21/25 및 템플릿의 장기 drift WATCH. 실제 132 광고의 QA는 별도 제작 보고에서 판정하며 여기서는 승인하지 않음.

## 커밋 경계

설계·지시서·baseline은 a3cb49e에 기록했다. 스킬 구현 커밋은 원래 clean이던 이번 범위 파일과 신규 파일만 전체 stage하고, 처음부터 dirty였던 SKILL.md/CHANGELOG.md는 **HEAD 위에 이번 추가분만** index patch로 올린다. 사용자 기존 수정 49개/미추적 18개는 본 작업에 포함하거나 되돌리지 않는다. git hook을 우회하지 않는다.

## Ultragoal 제한

`.omx/ultragoal/brief.md`, `goals.json`, `ledger.jsonl`을 공식 CLI로 만들고 목표 G001–G005를 기록했다. 현재 tool inventory에 get_goal/create_goal/update_goal이 없어 fresh Codex goal snapshot 및 서버 완료 게이트는 수행할 수 없다. CLI ledger의 annotate 기록으로 실제 수행 근거를 남기며 **formal aggregate goal complete를 주장하지 않는다**. 이 상태 경계는 실제 스킬/제작 작업을 중단하거나 다른 영상 모델로 바꾸는 사유가 아니다.
