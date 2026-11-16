# 설계서 R1 보완·재QA

## 최종 판정: 설계 재QA PASSED — 직접 문서 재QA PASS / 새 독립 gate review APPROVE

- 사용자 요청: 설계 QA에서 발견한 F01–F04를 “보완해”.
- 범위: 설계서 수정 및 문서 재검토. 영상 분석·생성, ASR, 실제 행동 테스트, 스킬 본문 수정은 수행하지 않았다.
- 대상: [설계서 R1](../../docs/superpowers/specs/2026-11-16-ad-rofan-archive-skill-upgrade-design.md).
- 검토 snapshot SHA-256: `dbcc3dd61fe7360abcc875db42b2b28daafb61f5614213e212df9ddc16132875`.
- 최초 FAILED QA와 원본 근거는 [이전 보고서](design-qa-report.md)에 그대로 보존했다. 이번 결과로 이전 결과를 재채점하지 않는다.

| 레인 | 결과 | 한계 |
|---|---|---|
| 부모 세션의 직접 문서·환경 재QA | PASS, 16개 시나리오 | 문서 경로 추적과 로컬 메타데이터 확인이며 실제 미디어/평가 실행의 성공 증거가 아님 |
| fresh-context gate reviewer 1명 | APPROVE, 문서 적합성 신뢰 HIGH | 현재 설계 해시·원문·F01–F04·직접 QA 16개 경로·근거 artifact를 독립 대조; 미디어 실행 준비의 승인은 아님 |

## 변경 대조

| 이전 QA | 실제 보완 | R1 위치 |
|---|---|---|
| F01: 상태 행 작성으로 C 종료 가능 | INVENTORY_COMPLETE / C_CONTENT_REVIEW_COMPLETE / C_PARTIAL·C_BLOCKED 분리, source-time·영역·모드·crosswalk gate, 모드별 GO/STOP와 재개 증거, D_PARTIAL/E_PARTIAL의 독립 근거 조건 | 19–21, 111–113, 134–160행 |
| F02: 불공정 비교·채점/승격 계약 부재 | baseline 전 prompt/rubric 동결, 동일 입력·모델·권한/버전·해시 기록, 실행/채점 격리, 필수 assertion 전부 및 안전 실패0·negative control 통과, 오류/재시험/회귀 처리 | 223–229행 |
| F03: Whisper 부재 오기 | 실행 파일·모듈 발견을 사실대로 정정, CLI/import·가중치·장치·실행·정확성은 미검증, ASR≠청취 유지 | 175–179행 |
| F04: 장편 분기 부재 | 2+2 의미 파일럿 유지 + 3,406초 몰아보기 최대300초 stress 검사; 앞/중간/끝·실제 접합·source/chunk 시간·중단/재개·재실행 중복 검사 | 128–142행 |

설계 승인은 계획·사전점검의 승인과 전량 실행 준비를 분리한다. 연속 동작·음향 청취 수단의 미검증은 해결된 것이 아니며, 현재 그 모드의 확장은 STOP이라는 상태를 유지한다.

## 직접 QA 매트릭스

실제 액션: 수정 설계 전체를 직접 읽고 아래 가정 상태를 해당 조항에 대입해 다음 경로가 유일하게 결정되는지 추적했다. 문서에 대한 QA이며 가정 상태를 처리하는 구현 코드를 실행한 것이 아니다. 줄번호 근거는 [R1 발췌](design-qa-r1-excerpts.txt); 도구 현황은 [직접 조회](design-qa-r1-runtime.txt); [문자열/형식 smoke](design-qa-r1-structure.json)는 보조 검사일 뿐 의미 정확성을 입증하지 않는다.

| # | 문서에 대입한 시나리오 / 실제 확인 | 기대 | 관찰한 결정 | 결과 | 근거 |
|---|---|---|---|---|---|
| R01 | 정상: A등록 완료 후 B의 실제 검사 전 | 인벤토리만 완료 | INVENTORY_COMPLETE 다음은 B; 내용 완료로 승격 불가 | PASS | R1 111–113, 152행 / excerpts |
| R02 | 정상: 92개 전체 시간·해당 영역·필수 모드·필수 crosswalk gate 검사 완료라는 가정 | 전량 내용 완료 후 D→E 가능 | C_CONTENT_REVIEW_COMPLETE의 필요 조건과 전량 후속 경로 명시 | PASS | R1 153–158행 / excerpts |
| R03 | 4개만 검사+88개 NOT REVIEWED, 또는 probe만92 | 전량 내용 완료 불가 | C_PARTIAL/C_BLOCKED로 명시 분기 | PASS | R1 158행 / excerpts |
| R04 | 정적 근거 존재, 음향·연속 동작 능력 UNKNOWN | 관련 전량 확장 STOP | 미확인도 STOP; GO인 독립 정적 작업만 부분 경로 | PASS | R1 134–142, 160, 179행 / excerpts |
| R05 | 후반 locator/재개 stress 실패 | 대량 확장 금지 | 모든 모드 전량 확장 중단; 경로·권한·실제 재파일럿 없이는 재개 불가 | PASS | R1 130–142행 / excerpts |
| R06 | 입력 근거 또는 모델/설정이 baseline/green 사이에 다름 | 같은 개선 실험으로 승격 불가 | 동일 비교로 합치지 않음; 고정 불가/UNKNOWN은 INCONCLUSIVE | PASS | R1 224행 / excerpts |
| R07 | 평가 rubric/이전 정답이 실행자에게 노출 | 결과 무효, 격리 후 재실행 | INVALID 및 실행/채점 context 분리 | PASS | R1 225행 / excerpts |
| R08 | 대부분 양호하나 권한/안전 실패 1건 또는 negative control 회귀 | 평균으로 상쇄하지 않고 NOT PASS | 안전 실패0 및 필수/negative 모두 통과 조건 | PASS | R1 227행 / excerpts |
| R09 | 예정5개 중 일부 tool 오류, 한 번의 동일조건 재실행도 실패 | 성공 분모 축소·은폐 금지 | INCOMPLETE 원본/대체 보존, 비교 INCONCLUSIVE, 승격 금지 | PASS | R1 228행 / excerpts |
| R10 | 내용 실패를 좋은 재응답으로 교체하거나 rubric 사후 완화 | 기존 실패 보존 및 새 variant/실험 필요 | 불리한 표본 삭제 불가, 기준 동결·새 variant 전체 재시험 | PASS | R1 223, 226–228행 / excerpts |
| R11 | Whisper executable/module 존재 | 발견은 인정, 사용 가능성은 미확인 | command -v와 find_spec 실제 일치; ASR/정확성/청취로 승격하지 않음 | PASS | R1 177–179행; runtime WHISPER DISCOVERY ONLY |
| R12 | 약57분 몰아보기의 늦은 경계·반복 구간·chunk 재실행 | 확장 전에 장편 분기 검사 | 앞/중간/끝+실제 접합·누락/중복·source PTS 대조 필수; 표본 합집합 최대300초 | PASS | R1 128–142행; runtime LONG SOURCE |
| R13 | 장편 최대300초만 검사 | 해당 전편 의미 분석 완료 아님 | 남은 구간은 C에서 미검토, 분모92 유지 | PASS | R1 132, 148행 / excerpts |
| R14 | 원본 외부 업로드·설치 필요, 또는 사용자 관찰만 제공 | 기존 권한 확대/직접 검사로 오인 금지 | 별도 동의·재검증; user observation은 bounded evidence만 | PASS | R1 185, 189행 / 설계 전체 직접 읽기 |
| R15 | 무관한 비영상 브리프·일반 단일 레퍼런스 | casebank/전량 감사 강요 방지 | 두 negative control 유지, 회귀는 NOT PASS | PASS | R1 227, 233행 / excerpts |
| R16 | 기존 QA 실패·과거 미디어 분석과 R1 결과 혼동 | 과거 결과·검토 모드 보존 | 최초 실패 보존, 과거검토 prior_record, 새 문서 QA≠실제 미디어 검사 | PASS | R1 4–6, 47–57행; 이 보고서와 이전 보고서 |

## 확인 명령과 산출물

- `command -v whisper`와 `/usr/bin/python3`의 `importlib.util.find_spec('whisper')`: 파일·모듈 발견만 재확인. import/CLI/모델 실행 안 함.
- 장편 원본에 `ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1`: `duration=3406.390567`.
- `git diff --check` 및 문서 문자열/후행 공백 검사. 문서는 untracked이므로 tracked diff 검사만으로 문서 공백 검사를 대신하지 않았고 별도 문자열 검사를 수행했다.
- `design-qa-r1-runtime.txt`의 `48960d...`는 본문 수정 후 첫 검사의 hash다. 이 세션의 편집 기록상 이후 상태 header 한 줄을 결과 보고서 링크로 바꿨다. 다만 이전 완전 문서를 별도 snapshot으로 보존하지 않아 그 delta 전체를 근거 파일만으로 독립 복원할 수는 없다. 최종 reviewer는 현재 `dbcc3d...` 전체 문서를 새로 읽고, R1 발췌의 번호 있는 93개 행이 현재 문서와 정확히 일치함을 독립 확인했다. 현재 설계 검토의 근거와 과거 runtime snapshot의 이 제한을 구분한다.
- 설계 문서만 수정했으므로 저장소 전체 pytest나 새 행동 테스트는 실행하지 않았다. 통과했다고 주장하지 않는다.

## 독립 검토 및 최종 인계

- 독립 검토: **APPROVE**, 현재 R1을 사용자 승인 요청 및 실행 계획 작성에 적합한 설계로 판정했다. F01–F04의 설계 계약상 보완을 모두 확인했고 새 blocking issue는 없었다. 이는 실제 파이프라인 실행, 검사 능력, 사용자 승인을 뜻하지 않는다.
- 원본 검토 결과: `/home/declan/.pi/agent/sessions/--home-declan--/subagent-artifacts/outputs/fb494f2f-70d3-4590-a163-468e933c2cbf/design-r1-gate-review.md`.
- reviewer run: `fb494f2f-70d3-4590-a163-468e933c2cbf`, fresh-context, 읽기 전용. 현재 설계 SHA-256 `dbcc3dd61fe7360abcc875db42b2b28daafb61f5614213e212df9ddc16132875`를 독립 확인했다. 설계 본문은 검토 이후 변경하지 않았다.
- 새 reviewer가 REJECT하면 문제를 보완하고 영향받는 직접 QA를 반복한 뒤 새 reviewer로 검사한다.
- 사용자 설계 승인, 미디어 검사 경로 검증, 파일럿/장편 stress 실행, 92개 내용 분석, 스킬 수정·행동 테스트는 아직 완료되지 않았다.
