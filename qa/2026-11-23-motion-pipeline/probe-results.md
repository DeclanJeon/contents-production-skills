# 행동 프로브 결과 (2026-11-23, anthropic/claude-sonnet-5-5, 텍스트만 답하라는 접미사)

판정은 두 층이다. **전체 판정**은 프로브 하니스 그대로(읽은 파일 + 답 키워드 + 마감 줄 계약). **모션 판정**은 마감 줄 실패를 빼고 읽은 파일·금지 파일·답 키워드만 본다. 마감 줄 실패는 2026-11-20부터 남아 있는 F1 잔여 결함이며 이번 변경 범위가 아니다.

| 회차 | 케이스 | 전체 | 모션 | 사유 |
|---|---|---|---|---|
| run1 | pm1 | PASS | PASS | opened ['creative-production/references/motion-pipeline.md'] |
| run1 | pm2 | FAIL | PASS | closing line is not an exact pattern: '다음: 박자표 확정과 C04–C06 스파이크 — 렌더·지출·음원 승인 전까지 대기 (필요: 렌더 실행 승인, 음원/내레이션 선택 |
| run1 | pm3 | PASS | PASS | opened ['creative-production/references/motion-pipeline.md'] |
| run1 | pm4 | PASS | PASS | opened ['creative-production/SKILL.md'] |
| run2 | pm1 | PASS | PASS | opened ['creative-production/references/motion-pipeline.md'] |
| run2 | pm2 | FAIL | PASS | closing line is not an exact pattern: '다음: 박자표 확정 후 컷 1개 스파이크(정지 프레임 3장) — 자동 진행' |
| run2 | pm3 | FAIL | FAIL | none of ['creative-production/references/motion-pipeline.md'] opened |
| run2 | pm4 | PASS | PASS | opened ['creative-production/SKILL.md'] |
| run3 | pm1 | FAIL | PASS | optional offer ending: '대기: 렌더 진행 여부 확인 — 필요: 실제 앱 기능 3가지 확정, `[모아 로고]`와 브랜드 컬러 제공, 렌더 실행 승인(텍스트 설계만 원하면 불필요). |
| run3 | pm2 | FAIL | PASS | mixed 다음:/대기: forms in one line: '다음: 스토리보드와 TTS·BGM 선택 — 대기: 렌더·유료 생성은 승인 필요 — 필요: 영상 제작 진행 여부와 실행 승인' |
| run3 | pm3 | PASS | PASS | opened ['creative-production/references/motion-pipeline.md'] |
| run3 | pm4 | PASS | PASS | opened ['creative-production/SKILL.md'] |

| 케이스 | 전체 | 모션 | 기준선(1회) |
|---|---|---|---|
| pm1 | 2/3 | 3/3 | FAIL |
| pm2 | 0/3 | 3/3 | FAIL |
| pm3 | 2/3 | 2/3 | FAIL |
| pm4 | 3/3 | 3/3 | PASS |

- 기준선(문서 수정 전): pm1~pm3 모두 motion-pipeline 미사용, 분석표·연출안 비교·구현 경로 없음.
- `iter1/`: 첫 수정 직후 1회. pm1이 구현 브리프를 생략하고 pm3이 파이프라인을 열지 않아, M4에 "텍스트 답에도 브리프 6칸" 규칙을, Step 1 트리거에 예시(price tag, chart, logo)를 추가한 뒤 run1~3을 다시 돌렸다.
- 설계의 통과 기준(양성 각 3/3, 부정 대조 3/3)에 대해: 모션 판정은 pm1 3/3, pm2 3/3, pm3 2/3, pm4 3/3이다. pm3 미달. 전체 판정은 마감 줄 계약 실패 때문에 더 낮다.
- 회귀(`regression/`, 1회): p2~p5·n1~n3 PASS, p1은 마감 줄 형식만 FAIL(읽기 정상). p2(모션 스타일)는 여전히 33번 스타일 사전을 연다.
