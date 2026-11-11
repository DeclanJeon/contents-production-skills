# 한국어 대본 후편집 검증 기록

- 일자: 2026-11-11
- 범위: 승인된 설계의 소스 저장소 구현. 기존 main 미커밋 변경을 유지하며 직접 작업하는 방식에 사용자 동의를 받았다.
- `behavior: codex_single_model_single_sample_author_reviewed_with_notes`
- 후속 실제 시험: [Codex CLI 13쌍/26건 결과](korean-postediting-codex-2026-11-11/README.md). 보존 루브릭의 뚜렷한 위반은 관측하지 않았으나 표현 개선/패턴 ID/보고량 보완이 있어 기본 적용은 보류한다.
- `default_application: held` — 현재 명시적인 후편집 요청 또는 제안 전용이다.
- 독립 리뷰 도구가 없어 사용자가 동의한 작성자 자체 리뷰를 수행했다. 후속으로 사용자 지정 Codex CLI의 실제 행동 대조를 수행했다. 독립·블라인드 리뷰와 실제 음성 청취는 수행하지 않았다.

## 실제 실행한 검사

| 검사 | 결과 |
|---|---|
| 구현 전 전체 `python3 -m pytest -q -rs` | 415 passed, 518 subtests passed (46.75s) |
| Task 1 패킷·변경률 RED → GREEN | 신규 모듈 부재 → 22 passed |
| Task 2 게이트 RED → GREEN | analyze 부재의 26 failed → 게이트/패킷 48 passed |
| Task 2 실제 CLI RED → GREEN | CLI 부재의 10 failed → 총 58 passed |
| Task 3 참조·예시·출처 RED → GREEN | 신규 파일 부재의 5 failed → 5 passed |
| Task 4 연결 RED → GREEN | 기존 오너 포인터 부재의 1 failed → 집중 65 passed |
| Task 5 임시 설치 | 새 checker·parser·참조·MIT 고지를 임시 fixture로 설치하여 다른 cwd에서 실행. docs/·전역 설치본 의존 없음 |
| Task 5 설치 링크 테스트 자체 오류 | `#packet`을 폴더로 검사하던 테스트 경로 해석 오류를 재현, 기존 정적 검사와 같은 현재 파일 해석으로 수정 |
| 최종 전 집중 회귀 | 112 passed, 239 subtests passed (2.57s) |
| 최종 전 전체 회귀 | 481 passed, 518 subtests passed (52.63s) |
| `python3 scripts/check_versions.py` | package 2.33, 22 skills consistent |
| `git diff --check` | 통과 |

최종 자체 리뷰·테스트 타입 정리 후 **전체 487 passed / 518 subtests passed** (최신 51.31s), 기능 집중 **72 passed**를 확인했다. 신규 설계/계획/참조/검증 기록의 상대 링크·명시 runtime anchor 25개도 통과했다. 위 수치는 텍스트 지침의 실제 모델 효과나 청취 품질 점수가 아니다.

## 계약 보존 확인

구현 전후 실제 SHA-256이 같았다:

- manifest.json: `45c9949ff6e65850f073e0759ec0dd228d66d0cf723ba35ec944328250fcd307`
- 각본 템플릿: `7f5c68e7c44f6072afadcece04e1f1be2b7aeec9335010ba2647c7b29a3b1ad6`
- contract.md: `d7be20620a61a12e11e534f1bec1d7f88ed0b44fc8c264cfc6781ae2657c89ad`

Python runtime은 범위 파서와 읽기 전용 checker로 나눴다. 기존 interpreter/pytest/installer만 사용하고 신규 의존성을 설치하지 않았다. 위 소스 구현 단계에서는 전역 설치·커밋·푸시·영상/음성 생성·외부 모델 호출을 하지 않았다. 후속 사용자가 Codex CLI 테스트를 지정해 기존 ChatGPT 로그인으로 26개 turn을 실행했다. API 키 환경 변수는 child에서 제거했으며 실제 금액/남은 구독 한도는 CLI가 제공하지 않아 추정하지 않는다.

## 행동 평가 준비와 제한

[합성 케이스](korean-script-postediting-cases.json)는 13종 입력·보존/금지 루브릭이며 실제 모델 출력이 아니다. 기존 `scripts/run_guide_behavior.py` 전체를 읽어 확인했다. 기존 runner는 G/F case ID→owner 고정 맵과 단일 owner-read/반응 기록 구조여서 KP case/무가이드 A/B를 직접 지원하지 않는다. 후속 승인 범위에서 [별도 prepare/collect 어댑터](korean-postediting-eval-adapter.md)를 연결했다. 13쌍/26건의 동일 원고·후편집 지침 차등 스냅샷을 만들고, 나중의 승인된 JSONL 캡처만 수집한다. 실제 모델 실행 옵션은 제공하지 않으며 이번에도 모델 호출은 0회다. Pi executable은 있으나 이것만으로 평가 도구/실행/예산이 준비됐다고 주장하지 않는다.

후속 사용자 지정에 따라 Codex CLI 0.167.0 / 기존 설정 모델 gpt-6.1-sol / low로 실제 13쌍을 시험했다. 동일 원고·설정과 조건별 지침의 동결 사본, 실제 argv·Codex native JSONL·응답·usage·작성자 판정을 별도 폴더에 보관했다. Pi collector는 사용하지 않았다. 1회 설정 사전 실패와 매 turn의 격리 경고 2개도 보존했다. 단일 모델/샘플·자체 검토의 한계와 발견된 보완점 때문에 자동 기본 적용을 계속 보류한다.

## 자체 리뷰

- 독립 리뷰: 미수행, 사용자 합의된 자체 리뷰만 사용.
- 의미 판별·권한 진위·범위/잠금 목록의 완전성은 checker가 인증하지 않는다.
- 원문 hash는 주어진 최초 원문과의 일치만 증명한다. 실행 간 원문/잠금 재설정 우회는 기존 작업 기록과 조정자가 관리한다.
- 최종 리뷰는 읽기 전용으로 현재 신규 파일과 이번 변경을 기준으로 수행했다. 커밋이 없으므로 commit-range review helper는 빈 범위로 종료했고, 기존 변경이 섞인 HEAD diff를 이번 구현 전체라고 오인하지 않았다.
- 보완: 긴 단위 안 부정어 이동, .5kg 같은 소수의 값 변화, JSON 중복 키/NaN/고립 surrogate, ASCII stdout 인코딩 오류를 각각 실패 테스트로 재현 후 수정했다. 부정어 위치 변화는 무해한 선행 편집에도 보수적으로 경고할 수 있으며 의미 판정은 사람이/모델이 문맥 대조한다.
- parser/CLI와 테스트 총 6개 Python 파일의 no-excuse audit: no violations. 각 파일 250 pure LOC 미만. Runtime 두 모듈 basedpyright standard 검사(Python 3.10, scripts 루트 execution environment): 0 errors, 0 warnings, 0 notes. 프로젝트 전체 strict 타입/ruff 검사를 수행했다는 뜻은 아니다.
- 타입 검사 초기 전체 프로젝트 기준 실행에서는 standalone sibling import 진단과 CLI Namespace 경고가 있었다. 실제 script-root 실행 환경으로 설정하고 Namespace를 명시 타입으로 바꿔 확인했다. 타입 무시 주석은 넣지 않았다.
- 단일 책임: 범위 파서는 불변 범위 계약, checker는 판정/CLI만 담당한다. 비신뢰 입력은 recursive JSON union에서 dataclass로 파싱하고 보고서는 TypedDict다. 신규 외부 런타임·동적 실행·광범위 예외·저장 기능은 없다.
- 자체 판단: 표준 라이브러리/argparse와 수작업 파싱은 승인된 무의존성 설계를 따랐다(일반 스킬의 Typer/Pydantic 기본값보다 우선). 파일/테스트 분리는 250 LOC 제한을 위한 것으로 설치할 파일 수가 조금 늘었다. exact 계약 보존은 당시 hash 증거로 남기고 영구 테스트는 다른 기능의 정당한 계약 개정을 동결하지 않는다.
- 남은 항목: Codex 시험에서 드러난 분류/표현/보고량 보완과 추가 표본, 독립 리뷰, 실제 음성 청취, 사용자 설치본 업데이트. Codex A/B 26건은 수행했지만 일반화된 품질 향상을 입증하지 않았으므로 자동 기본 적용은 계속 held다.
