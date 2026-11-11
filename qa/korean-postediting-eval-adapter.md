# 한국어 후편집 A/B 평가 어댑터

- 구현일: 2026-11-11
- 단계: **준비·캡처 수집 연결**. 실제 모델 A/B 실행·품질 판정·설치가 아니다.
- 이 prepare/collect 도구 자체의 실제 호출은 0회다. 후속 사용자 지정 [Codex CLI 실제 26건 시험](korean-postediting-codex-2026-11-11/README.md)은 별도 native 로그/프로필로 보관했다.
- 현재 `behavior: codex_single_sample_reviewed_with_notes`, `default_application: held`. 아래 오프라인 검사 수치는 어댑터 개발 당시의 기록이다.
- 기존 G/F runner는 변경하지 않는다. digest와 JSONL 해석만 재사용한다.

## 1. 실행 계획 준비 — 모델 호출 없음

저장소 루트에서 새 출력 경로를 지정한다.

```bash
python3 scripts/run_korean_postediting_eval.py prepare --output /tmp/korean-postediting-batch-new
```

기본 [13개 합성 사례](korean-script-postediting-cases.json)에 대해 baseline/postediting **26개 실행 예정 job**을 만든다. 현재 명령은 선택 대기(null)이며 실행 횟수·모델 호출은 0이다. `--case KPCASE01`을 반복 지정하면 일부 사례만 준비할 수 있다. 잘못된/중복 case ID와 부분적인 모델 선택은 거부한다.

실행 예정 argv까지 생성하려면 선택한 provider와 **정확한 model ID**를 함께 제공해 새 폴더를 만든다.

```text
python3 scripts/run_korean_postediting_eval.py prepare --output <새폴더> \
  --provider <선택한-provider> --model <정확한-model-id> --thinking low
```

이 작업도 모델을 호출하지 않는다. 실제 호출 전 모델·실행 수·예산·저장 범위를 별도로 승인받아야 한다. **26건은 Pi invocation 수이지 토큰/금액 상한이 아니다.** Pi 내부 자동 재시도 때문에 실제 provider 요청 수는 더 많을 수 있다. 어댑터에는 실행/비용 제한 기능이 없으며, 재시도 캡처는 정상 단일 시행으로 채택하지 않는다.

### 동결 폴더

- `plan.json`: 선택 상태·job별 argv·prompt/system hash·artifact hash·호출 미실행 상태.
- `suite.json`: 원고·제약·검토 루브릭의 동결 사본. 모델에는 평가 루브릭을 주지 않는다.
- `system-baseline.txt`: 공통 한국어 편집 과제·도구 금지 지시만.
- `system-postediting.txt`: 같은 공통 지시 + 실제 후편집 절차/패턴 스냅샷.
- `prompts/KPCASE01-baseline.txt` 등: 각 조건에 동일한 request/source/locked JSON.
- `review.md`: 의미·인물 말투·인용/수치·자연스러움·판정 모두 UNREVIEWED인 템플릿. 복사해서 별도 경로에서 검토하고 동결본은 변경하지 않는다.

두 조건은 같은 원고·provider/model/thinking을 쓰며 **후편집 지침만 다르다**. 사례별 baseline-first/postediting-first를 교대한다. 단일 샘플/조건이므로 통계적 우수성·일반화를 주장하지 않는다. 원고는 실제 prompt에 포함하고, should_improve/must_preserve/forbidden_actions는 reviewer용 suite에만 남긴다. locked는 사용자 제약이므로 양쪽 prompt에 제공한다.

## 2. 나중의 승인된 실행과 격리

`plan.json`의 command는 shell 문자열이 아닌 **argv 배열**이다. 동결 폴더를 cwd로 삼아 승인된 실행자가 그대로 사용해야 한다. 마지막 인자는 원고 JSON 자체다. `@file` 첨부의 추가 framing에 기대지 않는다. system-prompt는 동결된 조건별 파일을 참조한다. 기존 세션을 재개하거나 명령에 다른 옵션을 추가하면 동일 조건 비교가 아니다.

두 조건 모두 `--no-tools --no-extensions --no-mcp --no-skills --no-prompt-templates --no-context-files --no-approve --no-session --offline`를 사용한다. 이로써 모델이 QA 루브릭·전역 스킬·다른 조건을 도구로 읽는 경로를 열지 않는다. **`--offline`은 startup network를 억제하는 옵션이며 모델 API 호출을 차단하거나 무료로 만드는 옵션이 아니다.**

Pi 1.5.2의 실제 `--help`, 설치 문서 `docs/cli.md`·`docs/json.md`를 확인했다. 사용자가 승인한 실제 모델 호출은 아직 하지 않았으므로 flags 확인을 실행 성공 증거로 보고하지 않는다. 모델이 지침을 읽고 적용했는지의 의미적 증명도 아니며, runtime checker·자동 라우팅의 실효성을 이 no-tools 실험으로 검증하지 않는다.

## 3. 캡처 수집 — 모델 호출 없음

승인된 외부 실행자가 보관한 실제 JSONL/stderr/프로세스 종료 코드를 수집한다.

```text
python3 scripts/run_korean_postediting_eval.py collect \
  --run-dir <동결폴더> --job KPCASE01-baseline \
  --wire <stdout.jsonl> --stderr <stderr.txt> --exit-code 0 \
  --output <새수집폴더>
```

`collect`는 모델을 호출하지 않는다. raw stdout/stderr bytes, authoritative response, 사용량/실제 model/provider, 제출된 exit code, plan/prompt/system/raw hash, 문제 목록을 새 폴더에 보존한다.

- 동결 artifact가 바뀌거나 job·경로·입력이 잘못됐으면 **입력 오류(2)**, 쓰기 전에 거부한다.
- 정상 캡처는 **completed/UNREVIEWED(0)**. 코드/프로토콜/모델/원문 문제 캡처는 **execution_error/UNREVIEWED(1)**이며 실패 raw 증거도 보존한다.
- 실제 user message와 예정 원고 JSON, 관측 model/provider를 대조한다. 잘못된 모델·원고, 도구 실행/요청, 재시도·compaction, error/length/abort, 최종 agent_settled 부재, 비정상 JSONL은 정상으로 채택하지 않는다.
- JSONL은 LF로만 분리한다. 한국어·U+2028 같은 문자열 내용과 원본 bytes를 보존한다.
- 준비/수집 폴더는 create-only다. 기존 폴더, symlink 경유, unsafe ID/상대 경로를 거부한다. 쓰기 중 디스크 오류는 일부 새 폴더를 남길 수 있으나 기존 파일을 덮어쓰지 않는다. 부분 폴더는 완료 증거가 아니다.

**한계:** 로그/exit code는 외부에서 제공된 증거다. hash는 일관성 검사이지 서명/실제 명령 실행 인증이 아니다. JSONL은 system prompt의 실제 의미적 소비나 로그 위조 불가를 입증하지 못한다. 완료 수집을 품질 PASS나 사용자 승인으로 자동 바꾸지 않는다. 기본 적용을 여는 코드가 없다.

## 4. 검증 기록

실제 모델 호출은 **0회**다. 오프라인 테스트는 filesystem과 **합성 JSONL**만 사용하며 외부 프로세스 실행을 금지한 테스트도 포함한다. Pi CLI의 help/version만 조회했고 인증·키 조회·설정 변경은 하지 않았다.

- Task 1: 신규 모듈 부재 RED → 15 passed.
- Task 2: 신규 capture 모듈 부재 RED → 19 passed.
- CLI/원문 전달: CLI 부재 및 @file 대신 정확 user payload 필요성 RED → 기존 runner 회귀 포함 51 passed, 3 subtests passed.
- Runtime 3모듈 basedpyright standard: 0 errors, 0 warnings. 초기 JSON container 불변성/provider 타입 오류 3개는 타입을 명시해 해결했으며 type-ignore를 넣지 않았다.
- Runtime/테스트 5개 파일 no-excuse audit: no violations. 모두 250 pure LOC 미만.
- 최종 자체 리뷰에서 불완전한 agent_settled, 재시도 예정 agent_end, 도구 결과/추가 이미지 문맥, 누락된 hash/짝 job, 잘못된 system 조건/명령을 각각 RED 9건으로 재현했다. 동결 suite/profile/system에서 plan을 재구성해 일관성을 확인하고 trace 문맥·종료 검사를 강화한 뒤 기존 runner 회귀 포함 **60 passed, 3 subtests passed**를 확인했다.
- 기존 G/F runner와 테스트는 수정하지 않았다. 독립 리뷰는 미수행이며 사용자 동의한 작성자 자체 리뷰만 수행했다.
- 실제 기본 13쌍 prepare를 ignored workspace에서 실행해 26 planned·명령 선택 대기(null)·execution=not_run을 확인했다. 실제 모델 호출은 0회다.
- 최종 전체 `python3 -m pytest -q -rs`: **535 passed / 518 subtests passed** (55.76s). 버전 검사 package 2.33/22 skills consistent, `git diff --check`, 신규 QA/계획 상대 링크 통과. Runtime 3모듈 타입 검사 0 errors/0 warnings, 신규 runtime/테스트 5개 파일 audit no violations.
- 구현 판단: prepare/collect만 제공하므로 실제 호출은 별도 승인·실행 단계가 필요하다. no-tools 스냅샷은 baseline 오염을 막지만 자동 라우팅/코드 검사 실행을 평가하지 못한다. 원고 JSON을 argv에 직접 넣어 정확히 대조하므로 향후 매우 긴 원고는 stdin 전달 방식이 필요할 수 있다. 이번 13개 짧은 사례에서는 문제없다.

## 다음 게이트

실제 A/B 실행에는 선택한 모델/provider·최소 실행 수(전체 26 invocation)·비용 통제 방법·저장 범위의 별도 승인이 필요하다. 이후 실제 결과를 원문과 함께 검토해 의미/인물성 훼손 없이 hard guard와 보존 사례가 통과했는지 판단한다. 자동 기본 적용·전역 설치는 그다음 별도 단계다.
