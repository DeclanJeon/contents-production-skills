# Korean Script Postediting Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 기존 한국어 대사·내레이션 작성 흐름에 의미/인물성을 보존하는 후편집 지침과 읽기 전용 검증기를 연결한다.

**Architecture:** 기존 각본 오너가 완료 초안을 진단·국소 교정하고, 단일 표준 라이브러리 Python 모듈이 원문/후보/범위 패킷을 대조한다. 대사·내레이션별 규칙은 조건부 참조로 배포하며 제작 스키마와 설치 스킬 목록은 유지한다. 행동 평가가 완료되기 전에는 명시적 후편집·제안 전용으로만 열고, 새 초안의 자동 기본 적용은 보류한다.

**Tech Stack:** Python 3 표준 라이브러리, pytest(설치 확인: 9.1.1), Markdown, 기존 manifest 기반 installer. 신규 의존성·LLM SDK·네트워크 런타임 없음.

**Spec:** [승인된 설계](../specs/2026-11-11-korean-script-postediting-design.md), 사용자 승인일 2026-11-11.

## Global Constraints

- “새 총괄·설치 스킬·제작 원장·승인 체계를 만들지 않는다.”
- “대본 전체가 입력이어도 **자동 수정 범위는 대사와 내레이션**이다.”
- “원문 **100자 미만인 편집 단위**의 실제 수정은 별도 정밀 대조 대상으로 한다.”
- “**30% 이상 50% 미만**: 경고”, “**50% 이상**: 수정본 전체 자동 채택 중단.”
- “수정 루프는 작업당 최대 1회이며 재입력으로 한도를 우회하지 않는다.”
- “검증기는 수정하지 않는다.”
- “원문 파일은 바이트 그대로 보존한다.”
- “음성 실행은 기존 보이스 선택·권리·비용·실행 승인·실제 청취 절차를 따른다.”
- “`manifest.json`의 설치 스킬 목록, `project.json` 스키마, 각본 템플릿 heading/필드, 글로벌 설치본은 변경하지 않는다.”
- “한 건이라도 의미/인물성 악화가 남으면 기본 적용을 열지 않고 원인과 규칙을 보완한다.”
- 현재 HEAD `968b571` + 기존 미커밋 작업 트리를 기반으로 한다. 기존 변경을 정리·revert·stash·삭제하지 않는다. 실제 편집 직전에 파일을 다시 읽는다.
- 커밋·푸시·전역 설치·외부 모델 호출·과금·미디어 실행은 이 계획 실행의 자동 권한이 아니다. 아래 체크포인트에서 diff만 확인하고 커밋은 별도 요청 때 수행한다.

## Review Focus

1. 같은 숫자가 다른 화자로 이동한 원고: 문서 총합이 같아도 단위별 이동을 차단한다(Task 2).
2. 동일한 대사가 여러 번 등장하는 원고: 문자열 전역 replace 대신 원문 offset/hash로 구분하며 중복 locator·겹침을 거부한다(Task 1).
3. NFD 한글·CRLF·bidi가 있는 원고: 비교용 정규화 외 실제 원문 bytes와 범위 밖 bytes를 그대로 유지한다(Task 1/2).
4. 대사 속 실제 인용과 창작 대사의 혼합: 중첩 실제 인용은 보호하고 창작 발화 전체를 따옴표 때문에 잠그지 않는다(Task 2/3).
5. 새 입력처럼 위장한 재윤문과 오래된 파일: 최초 원문 hash·단위별 위치·누적 비교를 유지하고 버전 충돌을 판정 불가로 반환한다(Task 1/2/3).

---

## 파일 구조와 책임

신규 runtime 파일은 모두 `video-production-assets/` 안에 두어 기존 installer로 배포한다.

- `scripts/korean_script_postediting.py`: 데이터 계약·검증·집계·읽기 전용 CLI. 범용 마크다운 파서·원고 생성기·자동 패치 쓰기 기능 없음.
- `scripts/test_korean_script_postediting.py`: 단위/CLI 테스트. 같은 폴더의 기존 pytest 패턴을 따른다.
- `references/korean-script-postediting.md`: 절차·권한·검사 패킷 예시·반환·제약의 정본.
- `references/korean-script-postediting-patterns.md`: KP01–KP08 소수 패턴, 출처 ID와 발화 예외.
- `references/upstream/im-not-ai-provenance.md`, `im-not-ai-LICENSE.txt`: 고정 출처·수정점·MIT 고지.
- `scripts/test_korean_script_postediting_integration.py`(저장소 루트 scripts): 연결·배포 정적 계약과 임시 설치 시험.
- `qa/korean-script-postediting-cases.json`: 합성 행동 평가 입력/보존 루브릭. 모델 실행 결과가 아님.
- `qa/korean-script-postediting-validation.md`: 실제 실행한 구조/회귀/설치/모델 평가를 구분한 기록. 행동 미실행은 미실행이라고 적는다.

기존 파일 변경은 Task 4 목록만 대상으로 한다. 구현 중 파일이 과도하게 커질 때만 타입/파싱 분리를 검토하며 불필요한 범용 프레임워크를 추가하지 않는다.

## 고정 인터페이스

### 문서·패킷

`--source original.md --candidate candidate.md --packet packet.json`의 세 입력을 읽고 JSON 결과를 stdout에 출력한다. 파일 쓰기 인자와 자동 생성/복구 명령은 제공하지 않는다.

검사 패킷 형식 `korean-script-postediting/1`:

- `schema`: 위 문자열.
- `source_sha256`: 최초 원문의 UTF-8 bytes SHA-256. 재시도에서도 그대로 유지.
- `units`: 원문 순서의 배열. 각 항목은 `locator`(기존 ID 또는 문서 위치), `kind`(`dialogue|narration|direction`), `speaker`(공급값 또는 null), `start`, `end`(UTF-8 디코딩 원문 code point offset, 반개구간), `before`, `after`, `editable`(엄격한 bool), `reason`(수정 시 비어 있지 않은 문자열), `protected_spans`.
- `protected_spans`: 단위 안의 잠금 구간 배열. 각 항목은 `start`, `end`(before 기준), `after_start`, `after_end`(after 기준), `text`. 두 문자열의 해당 substring은 모두 text와 정확히 같아야 하며 같은 순서·서로 비겹침이어야 한다. 위치는 자동 보정하지 않는다.
- `direction` 단위는 사용자가 지문 표현 수정을 명시 허가한 경우에만 `editable=true`로 패킷에 넣는다. 권한 진위는 도구가 인증하지 않으며 실제 작업자가 요청 근거를 확인한다.

원문 안 units 밖의 모든 텍스트는 잠금이다. 후보 문서는 원문에 unit.after를 offset 기준으로 대입한 예상 문서와 바이트 단위로 같아야 한다. 따라서 header·ID·화자 표시를 범위 밖에 두면 변경이 차단된다. 화자를 보존하려면 그 표시를 before/after의 편집 가능 본문에 포함하지 않는다는 작성 예를 제공한다. units는 작업 범위의 목록이지 전체 원고의 의미적 완전성을 자동 증명하는 목록이 아니다.

검증기 내부 공개 타입/함수:

- `PacketError(ValueError)`: 스키마/원문 불일치/모호한 위치 등 판정 불가.
- `parse_packet(data: object, source: str) -> Packet`: 엄격한 내부 dataclass로 변환. `Packet`, `Unit`, `ProtectedSpan`은 위 필드의 snake_case 그대로 사용한다. 수치형 offset에 bool 허용 금지, 범위/중복/겹침/원문 일치 검증.
- `change_rate(before: str, after: str) -> float`: NFC 사본에 `1 - difflib.SequenceMatcher(None, before, after, autojunk=False).ratio()`. 빈 쌍=0, 한쪽만 빈 경우=1. whitespace·문장부호는 제거하지 않는다. 고정 원본 코드와 같은 문자 방식이며 영문 문서의 bigram 주장과 다름을 provenance에 명시한다.
- `rate_band(rate: float) -> int`: 유한한 [0,1] 입력에 `<0.30:0`, `<0.50:1`, 나머지 `2`. 반올림 전 비교.
- `analyze(source: bytes, candidate: bytes, packet_data: object) -> dict[str, object]`: 검증/집계. 파일 쓰기·LLM 호출 없음.
- `main(argv: list[str] | None = None) -> int`: CLI. argparse 오류 포함 판정 불가를 exit 3으로 일관되게 변환.

JSON 보고서 키: `schema`, `source_sha256`, `exit_code`, `scope`(검사 locator 목록), `change_rate`, `changed_units`, `review_required`, `blockers`, `warnings`, `units`, `limitations`. 항목별 문제는 code·locator·reason을 포함한다. `limitations`는 항상 의미·인물성·권한 진위·청취·사용자 승인 미검증을 밝힌다. 모델의 ‘의미 대조 통과’ 입력으로 코드 경고를 제거하는 API는 만들지 않는다.

집계는 각 editable 단위에서 명시 보호 span을 before/after 양쪽에서 제거한 문자열별로 rate를 계산하고, `max(len(NFC(before)), len(NFC(after)))` 가중 평균을 사용한다. 전부 잠겨 있으면 0. 단위 경계를 가로지르는 매칭을 하지 않고 비편집 영역·잠긴 인용 길이로 변경률을 희석하지 않는다. 별도 unit report에는 보호 span을 포함한 전체 rate도 제공한다.

우선순위: 판정 불가=3, 확인된 hard violation 또는 합산 rate≥0.50=2, 경고/수정한 100자 미만 단위/의미 위험=1, 그 외=0. `<100`은 NFC 전 원문 code point 길이, 변경 여부는 raw 문자열 비교. 강제 중단이 있는 경우에도 짧은 단위 경고 등 관찰 결과를 숨기지 않는다.

### 보호 탐지의 초기 범위

단위별 아라비아 숫자(부호·소수·자릿수 쉼표·백분율)와 바로 붙거나 공백으로 연결된 단위/화폐/날짜 표기의 순서 있는 토큰을 before/after로 비교한다. 예시 고정 목록: `%`, `원`, `만원`, `억원`, `년`, `월`, `일`, `시`, `분`, `초`, `명`, `개`, `회`, `배`, `kg`, `g`, `mg`, `km`, `m`, `cm`, `mm`, `ml`, `L`, `℃`, `°C`. 접두 외화 `$`, `₩`, `€`도 포함. 정확한 문자열 보존이며 임의 단위 환산은 허용하지 않는다. 한국어 수사·미등록 단위는 자동 탐지 보장 밖이므로 작업자가 명시 span으로 잠근다.

따옴표 자동 탐지는 인용 후보를 표시하는 경고만 생성한다. 실제 인용인지 판별/보호 span 설정은 작업자가 원자료에 따라 수행한다. 인용 후보가 있다고 창작 대사 자체를 일괄 잠그지 않는다. 부정(`안`, `못`, `않`, `없`)과 서법(`수 있다`, `수도`, `것 같다`, `보인다`, `해야`, `필요하다`)의 제거/추가/이동 가능성은 양방향 경고로만 보고한다. 이것은 문법 분석이나 의미 인증이 아니다.

## Task 1: 원문에 고정된 패킷과 변경률

**Files:** Create `video-production-assets/scripts/korean_script_postediting.py`, `video-production-assets/scripts/test_korean_script_postediting.py`.

**Interfaces:** 위 `PacketError`, dataclass, `parse_packet`, `change_rate`, `rate_band`를 생산한다. source는 newline 변환 없는 UTF-8 bytes에서 디코딩한 문자열이다.

- [x] **Step 1: 실패 테스트 작성.** 다음 이름과 assertions를 고정한다. `valid_packet()` 등 테스트 builder는 이 테스트 파일 안에 만들고 기존 제작 fixture를 가져오지 않는다.

```python
def test_rate_boundaries_and_empty():
    assert change_rate('', '') == 0
    assert change_rate('가', '') == 1
    assert change_rate('가', '가') == 0
    assert rate_band(0.299999) == 0
    assert rate_band(0.30) == 1
    assert rate_band(0.499999) == 1
    assert rate_band(0.50) == 2

def test_nfc_only_for_comparison():
    assert change_rate('가', '\u1100\u1161') == 0
```

추가 parameterized 테스트 `test_packet_rejects_invalid_shape`는 missing key, unknown schema, bool offset, 문자열 editable, 역전/범위 초과 offset, 중복 locator, 겹치는/순서 뒤집힌 unit, before 불일치에서 `pytest.raises(PacketError)`를 확인한다. `test_repeated_dialogue_has_distinct_offsets`는 똑같은 대사라도 두 offset/locator가 유효함을 확인한다.

- [x] **Step 2: RED 확인.** `python3 -m pytest -q video-production-assets/scripts/test_korean_script_postediting.py` → 신규 모듈/함수 미구현 실패. unrelated import failure는 RED 증거로 사용하지 않는다.
- [x] **Step 3: 최소 구현.** dataclass·엄격한 parse·metric만 구현한다. 원고 파싱·자동 patch 저장은 만들지 않는다.
- [x] **Step 4: GREEN 확인.** 같은 명령 → 모든 작성 테스트 통과. `NaN`, ±inf, -0.1, 1.1 rate 입력은 ValueError 테스트로 묶는다.
- [x] **Step 5: 체크포인트.** 신규 파일 diff 확인, 원본/후보 파일 쓰기가 없음을 확인. 커밋 보류.

## Task 2: 보호·구조 게이트와 읽기 전용 CLI

**Files:** Modify Task 1 두 파일.

**Interfaces:** Task 1 API 소비. `analyze`, `main`과 위 보고서/exit code 생산. 오직 stdout으로 보고한다.

- [x] **Step 1: 실패 테스트 추가.** 다음 사례별 assert를 작성한다.

```python
# 각각 독립 pytest 테스트의 핵심 판정
assert analyze(source, source, unchanged_packet)['exit_code'] == 0
assert analyze(source, changed_number_candidate, packet)['exit_code'] == 2
assert analyze(source, changed_locked_candidate, packet)['exit_code'] == 2
assert analyze(source, candidate, stale_hash_packet)['exit_code'] == 3
```

`test_numbers_cannot_move_between_speakers`(각 단위 10/20 교환), `test_units_currency_and_dates_are_preserved`(10kg→10g, 5만원→5원, 2026-11-11 변경), `test_nested_quote_span_is_locked`(창작 대사 내 인터뷰 인용), `test_protected_spans_do_not_dilute_rate`(긴 잠긴 인용 + 짧은 변경), `test_candidate_outside_units_is_rejected`(heading/화자/CRLF 변화), `test_modality_polarity_changes_require_review`, `test_short_changed_unit_requires_review_even_below_global_warn`, `test_retries_compare_to_initial_source`, `test_partition_overlap_or_missing_edit_fails`, `test_untrusted_instruction_is_only_text`를 포함한다. 숫자 이동은 전체 문서 토큰 총합이 같아도 exit 2여야 한다. raw NFD/제로폭/bidi 보존 및 유효한 미변경 문자열의 exit 0을 확인한다.

- [x] **Step 2: RED 확인.** 같은 pytest 명령 → analyze/게이트의 해당 미구현 실패 확인.
- [x] **Step 3: `analyze` 구현.** source hash → schema/ranges → 예상 candidate 재조립 대조 → 잠금/숫자 → rate/위험 경고 순서. 예상 문자열은 메모리에서만 구성한다. 보호 span 위치 오류/중복은 3, 확인된 텍스트 변조는 2. 필수 출력은 미검증 한계를 항상 포함한다. 빈 units와 source=candidate는 scope 빈 배열·rate 0이며 ‘전체 원고 검토’로 표시하지 않는다.
- [x] **Step 4: CLI 실패 테스트 추가.** `test_cli_read_only_exit_codes`는 tmp_path의 세 입력으로 subprocess를 실행해 0/1/2/3, parse 가능한 JSON, 입력 bytes 불변과 출력 파일 부재를 확인한다. 누락 파일·잘못된 JSON·invalid UTF-8·지원 안 하는 schema·인자 누락은 3. 후보와 packet에 의도치 않은 파일 경로가 있어도 읽거나 실행하지 않음을 확인한다.
- [x] **Step 5: RED 후 `main` 최소 구현.** `Path.read_bytes()` 사용, stdin·저장 옵션·외부 실행 없음. 예상된 오류만 구조화하고 예상치 못한 내부 오류를 pass로 숨기지 않는다.
- [x] **Step 6: GREEN/체크포인트.** Task 1/2 전체 pytest → 통과, `python3 video-production-assets/scripts/korean_script_postediting.py --help` → 사용법 출력. 입력/패킷 없이 미디어나 제작 파일 생성이 없는지 확인. 커밋 보류.

## Task 3: 발화용 절차·패턴·출처와 행동 평가 케이스

**Files:** Create 설계의 신규 reference 4개, `qa/korean-script-postediting-cases.json`, `scripts/test_korean_script_postediting_integration.py`.

**Interfaces:** Task 2 CLI/패킷 예시를 그대로 문서화한다. reference 정본의 explicit anchors는 `scope`, `workflow`, `dialogue`, `narration`, `packet`, `gates`, `handoff`. synthetic suite schema는 `{schema: 'korean-script-postediting-cases/1', cases: [...]}`이며 case 필드는 `id`, `kind`, `prompt`, `source`, `locked`, `must_preserve`, `should_improve`, `forbidden_actions`이다.

- [x] **Step 1: 정적 실패 테스트.** `test_references_and_anchors_exist`, `test_packet_example_runs_against_cli`, `test_patterns_have_upstream_mapping_and_genre_guards`, `test_behavior_suite_has_all_required_classes`, `test_provenance_is_pinned_and_notice_preserved`를 작성한다. 파일·anchor 존재뿐 아니라 무음/QA-only/승인본/기존 음성/독립 검토 부재/1회 재시도/미검증 보고 문구를 확인한다.
- [x] **Step 2: RED 확인.** `python3 -m pytest -q scripts/test_korean_script_postediting_integration.py` → 신규 참조/평가 입력 부재 실패.
- [x] **Step 3: 정본 절차 작성.** 설계 §§6–9를 간결한 실행 순서로 옮긴다. 권한 확인 → 단위/실제 인용 구분 → 경로 → 국소 편집 → 코드/의미 대조 → 반환. 검증기 0이 의미 pass가 아님, 읽기 전용과 저장 시 단일 기록자, 새 원고 버전/SSOT 변경 시 재검토, 외부 실행/음성 재생성 별도 승인, 자체 대조와 독립 검토 구분을 포함한다. 재시도 상태는 기존 operation/review 메모에 남기고 패킷을 새 제작 원장으로 쓰지 않는다.
- [x] **Step 4: 패턴 KP01–KP08 작성.** 번역투/피동(A), 명사화(F/I), 추상 연결(A/D), 상투 도입/결론(D), 접속/열거(C/H), 종결 리듬(E), 유보 중첩(G), 호흡·수식 길이(A/E). 각 항목에 원본 ID·발동 문맥·대사/내레이션 예외·보존 반례·동일 의미 교정 예시를 둔다. 적용 가능한 것만 고르고 원본의 ‘잔존 0’·장문 삽입·비유 일괄 삭제는 제외한다.
- [x] **Step 5: 고정 출처/라이선스 기록.** 고정 커밋에서 실제 이전하는 파일을 다시 읽고 bytes SHA-256을 기록한다. 승인된 GitHub 공개 URL의 read-only fetch만 사용한다. MIT 전문은 확인한 `Copyright (c) 2026 epoko77-ai`와 함께 보존한다. 영문 bigram 설명과 실제 SequenceMatcher 코드 차이, 자체 집계/발화 예외를 명시한다. 미열람 전체 taxonomy를 검토했다고 쓰지 않는다.
- [x] **Step 6: 합성 행동 suite 작성.** 설계 §10의 10종에 각 최소 1개, 두 인물 관계·인용/창작 혼합·짧은 부정·무수정·읽기 전용·의도 반복을 별도 case로 포함한다. source에 실제 사용자 원고를 넣지 않는다. 구조 테스트와 행동 평가의 차이를 문서화하고 suite 작성만으로 모델 통과로 보고하지 않는다.
- [x] **Step 7: GREEN/체크포인트.** Task 3 pytest → 통과. 문서의 complete packet 예시를 tmp_path에서 CLI에 넣어 예시의 보고서/exit가 맞는지 검증. 커밋 보류.

## Task 4: 기존 작성·음성 인계·QA 연결

**Files:** Modify `video-production-assets/SKILL.md`, `video-production-assets/references/03-screenplay.md`, `video-production-assets/references/22-dialogue-lipsync.md`, `video-production-assets/references/12-qa.md`, `creative-production/references/production-routing.md`, `integrations/skill-routing.md`, `integrations/package-provenance.md`, `README.md`, `USAGE_GUIDE.md`, `CHANGELOG.md`; Modify Task 3 integration test.

**Interfaces:** 오직 Task 3 reference anchors와 Task 2 CLI 사용. 새 stage·state·manifest entry·글로벌 스킬 호출 없음.

- [x] **Step 1: 연결 실패 테스트.** `test_each_owner_reaches_current_stage_reference`에 위 각본→workflow, 음성→handoff, QA→gates, 라우팅/skill→scope 포인터를 검사한다. `test_no_schema_template_manifest_expansion`은 실행 전 스냅샷과 manifest skills·project schema·각본 템플릿 headings 불변을 확인한다. 비교용 원본 hash는 실행 직전에 캡처한다.
- [x] **Step 2: RED 확인.** integration pytest → 현재 연결 부재만 실패하는지 확인.
- [x] **Step 3: 최소 포인터 추가.** 편집 직전에 기존 파일을 다시 읽고 짧은 정확 일치 edit를 사용한다. 기존 미커밋 집필·보드 변경을 포함한 현재 내용을 보존한다. 영상 패키지 범위 밖 스킬에 의존하지 않는다. ‘명시 후편집 또는 제안 전용; 행동 도입 게이트 통과 전 자동 기본 적용 보류’ 문구를 scope 정본에 두고 각 오너는 이를 참조한다.
- [x] **Step 4: 사용 예시/이력.** 새 초안 교정·검수만·이미 녹음된 원고·무수정 통과 예시를 작성한다. 실제 구조/행동 검증 상태를 구분하고 성과 보장을 넣지 않는다. 버전 변경이 필요하면 `scripts/check_versions.py` 현행 규칙과 기존 작업자의 버전 변경을 먼저 대조하고 자동 일괄 bump를 하지 않는다.
- [x] **Step 5: GREEN/체크포인트.** Task 1–4 pytest 통과, 변경 diff가 승인된 최소 연결 범위인지 검토한다. 커밋 보류.

## Task 5: 임시 설치·회귀·행동 도입 게이트와 인계

**Files:** Modify integration test; Create `qa/korean-script-postediting-validation.md`. 조건부로 모델 실행 증거 경로 `qa/korean-script-postediting-behavior/`를 사용하되 승인된 실제 실행이 있을 때만 결과 파일을 만든다.

**Interfaces:** 기존 `install_package.install(skills_root, repo_root=..., exclude_derived_support=True)`를 소비한다. 외부 SDK와 모델을 임의 선택하지 않는다.

- [x] **Step 1: 설치 회귀 테스트 작성/실행.** `test_installed_postediting_runs_without_repo_or_home_dependencies`는 tmp_path에 최소 package fixture(manifest: `video-production-assets`, `creative-production`, 필요한 examples/qa placeholder)를 만들고 **실제 runtime 파일**을 복사해 installer를 호출한다. 다른 cwd에서 설치된 checker를 실행하고 references/upstream license·포인터가 설치본 안에서 해결되는지 확인한다. docs/와 원본 repo를 참조하지 않아야 한다. global skill root가 불변임을 확인한다. 설치부 신규 코드가 필요 없다면 이 테스트는 바로 GREEN일 수 있으며 허위 RED를 만들지 않는다.
- [x] **Step 2: 집중 회귀.** 저장소 루트에서 `python3 -m pytest -q video-production-assets/scripts/test_korean_script_postediting.py scripts/test_korean_script_postediting_integration.py scripts/test_install_package.py scripts/test_guide_integration.py scripts/test_video_pack_boundary.py` → 전부 통과 또는 기존 실패를 출처별로 보고.
- [x] **Step 3: 전체 회귀/정적 검사.** `python3 -m pytest -q -rs`, `python3 scripts/check_versions.py`, `git diff --check` 실행. 기존 미커밋 코드의 실패·skips와 신규 기능 실패를 구분한다. 미설치 의존성 발견 시 자동 pip install하지 않고 필요한 승인/대안을 보고한다. 신규 문서의 상대 파일/anchor도 검사한다.
- [x] **Step 4: 행동 평가 가용성 확인.** 기존 `scripts/run_guide_behavior.py`의 suite 형식과 실제 Pi 비대화 실행/로그 캡처 계약을 전체 읽고 사용 가능 여부만 확인한다. 실제 외부/과금 호출 전 사용자에게 모델·실행 수·예산·저장 범위를 승인받는다. 호환되지 않으면 harness를 무단 개조하지 않고 별도 실행 방법을 제안한다. 현재 세션의 수작업 예문은 독립 모델 A/B 증거가 아니다.
- [ ] **Step 5 (미실행·도입 보류): 승인된 경우에만 행동 대조 실행.** 동일 모델/설정/입력의 무가이드/모듈 적용 결과와 실제 prompts를 보관하고 case별 보존/개선/악화를 판정한다. 미실행이면 validation에 `behavior: unverified`, `default_application: held`로 기록하고 기능을 명시 요청/제안 전용으로 인계한다. 모든 hard guard 통과·보존 사례 통과·의미/인물성 악화 없음이 실제 확인돼야 기본 적용 보류를 해제할 수 있다.
- [x] **Step 6: 리뷰/사용자 인계.** 제공되는 독립 리뷰 도구가 있으면 실행 방법 합의에 맞춰 리뷰한다. 없으면 독립 리뷰 미수행을 명시하고 사용자가 승인한 대체 자체 점검만 수행한다. 실제 검사 명령·결과·한계·변경 파일·설치 미실행·남은 도입 게이트를 보고한다. 커밋·푸시·전역 동기화는 별도 요청 없이는 수행하지 않는다.

## 실행 방식과 승인 체크포인트

현재 세션에는 독립 범용 subagent/reviewer 도구가 확인되지 않는다. 따라서 스킬의 정식 Subagent-driven과 Native(마지막 독립 reviewer 포함)를 완전하게 수행할 수 없다. 사용자에게 다음 지원 가능한 대안을 설명하고 **동의받은 뒤** 실행한다.

- 이 세션에서 Task 1–5를 순차 TDD로 구현하고 각 task의 증거와 자체 리뷰를 기록한다. 독립 리뷰·외부 행동 대조는 미완료 항목으로 남긴다.
- 독립 리뷰를 필수로 유지한다면 사용자가 사용 가능한 리뷰 실행 경로를 지정할 때까지 구현을 보류한다.

작업 트리 격리 선택은 실행 시 `using-git-worktrees`를 읽고 결정한다. HEAD worktree만 만들면 승인 설계가 읽은 기존 미커밋 원고/보드 변경이 빠지므로 이를 조용히 누락하지 않는다. 기존 작업 보존·복제 여부를 확인한 후 실행 방식에 기록한다. 이 계획은 worktree 생성·이동 자체를 실행하지 않는다.

## 계획 자체 검토

- 설계 §§1–4 목표/이전 경계/인접 구조: Task 3/4.
- §5 배포/포인터/라이선스: Task 3–5.
- §§6–7 권한/단위/범위/hash/분할: Task 1/2/3.
- §8 프로필/보호/수치/짧은 발화/경고/재시도: Task 1–3.
- §9 승인/저장/의존성/중복 실행 방지: Task 3/4.
- §§10–11 회귀/행동/도입: Task 3/5. 행동 실행은 별도 승인·도구 가용성 조건부이며 미완료 시 default held가 산출물이다.
- §12 독립 리뷰 부재: 실행 합의와 Task 5에서 명시.
- Review Focus 5개 모두 Task 1–3의 이름 있는 테스트/절차로 연결했다. task 간 API 이름·report 키·exit code를 공통 인터페이스와 맞췄다.
- 확인: 계획 문서 작성은 구현·독립 리뷰·행동 평가의 수행 증거가 아니다.
