# Korean Postediting Evaluation Adapter Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 승인된 후편집 설계의 남은 행동 평가 준비를 연결하되 이번 작업에서는 모델 호출 없이 13쌍/26건의 동결 실행 계획과 캡처 수집 어댑터를 제공한다.

**Architecture:** 기존 G/F runner를 변경하지 않고 digest/JSONL 해석을 재사용한다. 별도 어댑터가 공통 입력·조건별 system·hash·검토 양식을 만들고, 나중에 승인된 외부 실행의 JSONL 캡처를 검증해 UNREVIEWED 결과로 수집한다. 모델/가격/실행은 정하지 않고 자동 기본 적용은 held로 유지한다.

**Tech Stack:** Python 3.11+ 표준 라이브러리, 기존 pytest, Pi 1.5.2 CLI/JSON 계약. 새 라이브러리 없음.

**Spec:** [승인된 후편집 설계](../specs/2026-11-11-korean-script-postediting-design.md) §10–11, [원래 계획](2026-11-11-korean-script-postediting.md) Task 5의 미실행 행동 평가 준비. 사용자는 ‘평가 실행기 연결’을 다음 작업으로 선택하고 진행을 요청했다. 같은 폴더·순차 TDD·자체 리뷰·미커밋 보존 방식 유지.

## Global Constraints

- 이번 단계는 준비/수집만 구현·오프라인 검증한다. 실제 모델·음성·영상 호출, 과금, 설치, 전역 설정 변경, 커밋/푸시 없음.
- 기존 G/F 평가기와 제작 schema/manifest/각본 모듈은 변경하지 않는다.
- baseline에는 후편집 지침을 제공하지 않는다. 양쪽 user prompt는 동일하고 rubric은 입력에 노출하지 않는다. 명시적 locked 문구는 실제 사용자 제약으로 양쪽에 제공한다.
- 양쪽 모두 --no-tools/--no-extensions/--no-mcp/--no-skills/--no-context-files/--no-prompt-templates/--no-approve/--no-session/--offline를 사용한다. offline은 startup network 억제이지 모델 호출 무료/차단 옵션이 아니다.
- CLI에 실제 실행 옵션을 만들지 않는다. provider/model 둘 다 지정해야 실행 명령을 생성하며, 미지정이면 명령은 null·선택 대기다. 26은 과정 수이지 비용/토큰 상한이 아니다. 승인 뒤에도 provider 측 실제 비용 통제가 별도로 필요하다.
- 새 결과 폴더만 생성한다. 기존 파일 덮어쓰기·symlink 경유 쓰기·case ID 경로 탈출을 거부한다.
- 캡처 성공은 품질 PASS가 아니다. 항상 UNREVIEWED, default_application=held. 수집은 제출한 로그에 대한 검증이며 명령 실제 실행/위변조 불가를 인증하지 않는다.

## Review Focus

1. treatment 원고가 누락되거나 rubric이 baseline에 새는 경우: 같은 user payload/source hash와 rubric 비노출을 검사한다(Task 1).
2. 잘못된 모델/다른 user prompt의 로그 재사용: 캡처 실제 model/provider/user message를 job과 대조한다(Task 2).
3. malformed JSONL·toolCall·length/error·미정착·자동 재시도: completed가 아니라 실행 실패로 기록한다(Task 2).
4. 기존 output·symlink·unsafe ID·변조된 run snapshot: 어떤 덮어쓰기나 외부 호출 없이 거부한다(Task 1/2/3).
5. 실제 호출로 오해되는 준비 작업: subprocess/network가 없는 CLI, 실제 모델 테스트 0건, 명령 선택 대기와 승인 필요를 명시한다(Task 3).

## 파일 구조와 인터페이스

- Create `scripts/korean_postediting_eval.py`: suite 파싱·동결 plan/render. `EvalError(ValueError)`, frozen `Case`, `Profile(provider: str|None, model: str|None, thinking: str)`, `Job`와 `Batch`.
- Create `scripts/korean_postediting_capture.py`: 기존 `run_guide_behavior.parse_events` 재사용 전 JSONL shape 검사·capture 판정/파일 렌더링.
- Create `scripts/run_korean_postediting_eval.py`: `prepare`/`collect` argparse CLI. 선택된 output만 create-only 저장. 외부 프로세스 실행 기능 없음.
- Create `scripts/test_korean_postediting_eval.py`, `scripts/test_korean_postediting_capture.py`: 실제 filesystem·합성 JSONL의 오프라인 테스트.
- Create `qa/korean-postediting-eval-adapter.md`: 사용법·실제 검증·한계. Modify `qa/korean-script-postediting-validation.md`, `USAGE_GUIDE.md`, `CHANGELOG.md`에 현재 준비 상태만 기록.

API:

- `load_cases(raw: bytes) -> tuple[Case,...]`: schema=기존 korean-script-postediting-cases/1, 고유 KPCASE[0-9]{2,} ID, 모든 원문/목록 타입과 비어 있지 않은 필수 제약 검사.
- `build_batch(cases: tuple[Case,...], guides: tuple[str,str], profile: Profile) -> Batch`: case별 baseline/postediting job. 짝수/홀수 case는 실행 순서를 교대한다. prompt는 JSON data(source/request/locked), 두 조건에 동일.
- `render_batch(batch: Batch) -> dict[str,str]`: plan.json, suite.json, system-baseline.txt, system-postediting.txt, prompts/<id>.txt, review.md. 파일 경로/내용·SHA-256은 plan에 고정한다. review의 의미·말투·인용·수치·자연스러움 칸은 UNREVIEWED.
- `collect_capture(run_dir: Path, capture: CaptureInput) -> dict[str,str]`: job_id/wire bytes/stderr bytes/제공된 process exit_code를 담은 frozen CaptureInput. 입력 snapshot hash 확인 뒤 raw stdout/stderr·response.md·attempt.json 렌더. model/provider와 user prompt 불일치·도구·retry·프로토콜 오류는 failed, 정상은 completed/UNREVIEWED. 부분 실패도 raw 증거는 보존.
- `save_new_bundle(output: Path, files: dict[str,str]) -> None`: 사전 경로/symlink/충돌 검사 후 새 폴더에 create-only. 수집 raw 파일은 bytes를 그대로 보존할 수 있도록 렌더 반환에 bytes도 허용한다.
- `main(argv: list[str]|None=None) -> int`: prepare 성공=0, collect 정상 수집=0/실행 실패 캡처=1, 입력/경로 오류=2. 어떤 명령도 subprocess를 호출하지 않는다.

## Task 1: A/B 동결 계획

**Files:** Create model module and tests.

- [x] RED: `test_real_suite_builds_26_jobs`(13 cases/26 jobs), `test_same_user_prompt_and_rubric_withheld`, `test_treatment_only_receives_guides`, `test_unselected_profile_has_no_command`, `test_selected_commands_disable_all_tools`, `test_suite_rejects_unsafe_duplicate_or_malformed_case`.
- [x] Run `python3 -m pytest -q scripts/test_korean_postediting_eval.py` → 신규 기능 부재 실패 확인.
- [x] Implement typed input/model/render. case.source를 반드시 prompt에 포함하고, 원문/지침/설정/명령의 실제 제출 예정 bytes를 hash로 묶는다. reviewer rubric은 suite/review 파일에만 둔다.
- [x] GREEN: 같은 테스트 통과, 동일 입력 render가 결정적임을 확인. 커밋 보류.

## Task 2: 결과 캡처 연결

**Files:** Create capture module/tests.

- [x] RED: `test_collect_complete_keeps_unreviewed`, `test_rejects_wrong_model_provider_or_prompt`, `test_tool_retry_error_and_unsettled_are_not_complete`, `test_malformed_json_shapes_fail_closed`, `test_snapshot_tamper_is_rejected`, `test_unicode_lf_framing_and_raw_bytes_survive`.
- [x] Run `python3 -m pytest -q scripts/test_korean_postediting_capture.py` → 신규 기능 부재 실패 확인.
- [x] Implement snapshot preflight, minimal shape validation then existing parse_events. final authoritative response·종료 상태·실제 모델·사용량을 기록하고 tool-call content도 거부한다. provider/model 정보가 빠져도 실패/미확인으로 남긴다. source/rubric 변조와 case/path 일치를 검사한다.
- [x] GREEN: 같은 테스트 통과. 캡처/리뷰 결과가 default gate를 승격시키는 코드가 없는지 확인. 커밋 보류.

## Task 3: 준비/수집 CLI와 사용 증거

**Files:** Create CLI; Modify tests and QA/docs above.

- [x] RED: `test_prepare_cli_creates_only_new_output`, `test_output_symlink_and_collision_are_zero_write`, `test_cli_has_no_execution_option`, `test_collect_cli_records_synthetic_trace_without_model_calls`.
- [x] Run model/capture 테스트 → CLI 부재 실패 확인.
- [x] Implement prepare/collect only. 전체 입력/경로 preflight 뒤 저장한다. `--execute`는 unknown option으로 거부한다. 준비/수집 API의 비용/실행/로그 진위 한계를 사용법에 넣는다.
- [x] GREEN: 집중 테스트, 기존 `scripts/test_run_guide_behavior.py`, 전체 `python3 -m pytest -q -rs`, basedpyright standard/스크립트 audit, `check_versions.py`, `git diff --check`.
- [x] 실제 default 13쌍 prepare만 ignored workspace에 실행해 26건 planned/선택대기·실제 모델 0회임을 확인한다. 합성 capture는 synthetic 표시를 남긴다.
- [x] 자체 리뷰·한계·검증 결과 기록. 기존 기본 적용 held 유지. 커밋/설치/실제 모델 실행 없음.

## 자체 검토와 실행 메모

세 task는 공통 typed model·plan hash→capture→CLI 순서로 의존한다. 기존 parse_events의 JSON object 가정을 adapter가 검사하므로 기존 G/F runner를 바꿀 필요가 없다. 출력 폴더와 raw 입력은 create-only로 분리한다. 기존 동의대로 바로 순차 실행하며 새 모델 선택/예산 결정은 미실행 범위로 남긴다.
