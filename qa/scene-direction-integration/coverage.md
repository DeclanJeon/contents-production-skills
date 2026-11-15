# V1 커버리지 / 진행 상태

**E1 보존 결과:** 기준판 8종은 7 PASS / 1 INCONCLUSIVE, 관찰 35 PASS / 1 INCONCLUSIVE / 0 FAIL로 유지한다. 당시 생산 본문 변경은 0이었다. 이후 승인된 E2에서 확정 누락을 발견해 3문서 C1 후보와 형성 2건·최종 8건을 실행했다. 아래 E1 최종 후보는 SD03/08 보호 대조군만 해당한다. 전체 현재 범위는 [E2 coverage](open-brief-coverage.md)와 [최종 검증 보고](../2026-11-14-scene-direction-integration-validation.md)를 본다. 구조/내용/실제 준비/결과/수락 모두 별도다.

| Case | 지키는 대표 요구 / 긍정·부정 대조 | 기준선 | 형성 후보 | 최종 후보 | 담당 작업 |
|---|---|---|---|---|---|
| SD01 | 세계 법칙·관계 선택/비용→대본→3샷·원문/왼손·요청문 | PASS (6/6 관찰, 작성자 검토) | NOT_RUN | NOT_RUN | 3/4/7/9 |
| SD02 | 같은 첫끝 속 전달/복귀·손/점유·접촉 중간 단계 | PASS (4/4) | NOT_RUN | NOT_RUN | 4/6/9 |
| SD03 | 정적/동일 hold·원테이크·완전 no_audio의 유효성 | PASS (4/4) | NOT_RUN | C1 PASS (4/4, 작성자) | 4/8/9 |
| SD04 | 비인간 지지·FX 원인/단계/차폐/환경·다음 샷 비용 | PASS (5/5) | NOT_RUN | NOT_RUN | 6/9 |
| SD05 | offscreen 화자/입 비가시 청자·공개 유보·stale/범위 | PASS (5/5) | NOT_RUN | NOT_RUN | 5/8/9 |
| SD06 | 원문/보이스/12행·4길이 묶음·3시간 basis·실제 요청문 | INCONCLUSIVE (4 PASS / 1 기준 입력 부족) | NOT_RUN | NOT_RUN | 5/7/9 |
| SD07 | 음악/효과 기능·발화 우선·청점/거리·미측정 정직성 | PASS (4/4) | NOT_RUN | NOT_RUN | 5/9 |
| SD08 | 무인 설명 QA-only·generic 칸의 내용 부족·구조≠품질 | PASS (3/3) | NOT_RUN | C1 PASS (3/3, 작성자) | 3/8/9 |

모든 baseline의 실제 응답·도구 audit·검토 카드를 계획 전용 evidence root에 보존했다. SD06의 대사별 보컬 연기 보존은 원본 큐가 공급되지 않아 판정 불가다. 관찰되지 않은 실패/개선을 꾸미지 않는다. E1의 나머지 6종은 승인된 E2 배분상 최종 후보에서 재호출하지 않았으며, 이를 후보에서도 통과한 것으로 계수하지 않는다. 독립 최종 리뷰 1회는 완료했고, 실제 미디어는 미수행이다. 전체 B는 미완료/HOLD이며 최종 채택 판정은 보고서에서 구분한다. 기존 감사의 validator 반례는 구조 범위의 근거일 뿐 이 사례들의 실제 baseline 응답이 아니다.

## 현재 확인한 것
- 격리 branch feat/scene-direction-integration-20261114, BASE 0e1d9f343fa2bec0d00421ed2cf4488abd41888c.
- 초기 package 2.34/22 skill 버전 일관성 검사 성공.
- 초기 전체 pytest: 737 passed, 4 skipped, 525 subtests passed. 4 skip은 실행/플랫폼 검증 성공으로 계수하지 않는다.
- 위 회귀는 과제 입력/스킬의 연출 품질 검사가 아니다.
- SD06 공급 표는 creative-production/references/storyboard-timing-to-prompt.md §4의 첫 12행 표와 서문을 그대로 고정한다. 묶음 정답 표/실제 제출문 예시는 사용자 입력에 덧붙이지 않는다. baseline의 기존 전문 문서는 정상적인 지침이므로 숨기거나 제거하지 않는다.

## 입력/자료 무결성 검사
확인한 것: 고정 8개 ID/필수 관찰 36개·rubric 연결/입력 locator와 owner_paths 실재, JSON parse, SD06 12행·D01–D06 및 BASE 원문 excerpt의 정확 일치, 빈 검토 카드의 NOT_RUN/UNREVIEWED. 계획 전용 verify-task-1.sh의 실제 출력으로 확인했다. 이는 행동 판정이 아니다.

실제 baseline 8건의 프로필/범위·출력 해시·관찰/보호 대조군과 미검사 이유를 확인했다. 후보/회귀 비교는 E2 최종 8쌍과 구분해 보고한다. 독립 리뷰의 최종 7 PASS/1 FAIL을 채택했으며, E1 SD03/08 보호 대조군은 PASS를 유지한다. source/input 동결·기계 검사를 실제 모델 응답/의미 검사나 미디어 검증의 대체물로 쓰지 않는다.
