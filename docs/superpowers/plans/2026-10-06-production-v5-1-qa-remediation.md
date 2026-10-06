# Production v5.1 QA 보완 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use executing-plans for the integrated remediation. The user authorizes implementation despite the previous work-order-only status. This authorization does not permit commits, pushes, media generation, or global installation.

**Goal:** QA에서 확인한 23개 결함을 수정하여 잘못된 FINAL 승인, 파일 누락·변조, 작업 폴더 밖 자동 접근, 부정확한 이력을 막는다.

**Architecture:** 기존 `project.json`을 유일한 제작 상태 정본으로 유지한다. 기존 자산 게이트, 준비 검사, 추출기, 패키저, 변경 전파 및 history 도구를 보완하고 모든 소비 경계에 같은 검증을 적용한다. CSV·ZIP·작업자 전달 패킷은 정본에서 파생하며 별도 승인 원장을 만들지 않는다.

**Tech Stack:** Python, Pillow, 기존 pytest/unittest, Markdown, Windows junction/symlink 및 POSIX 파일 경로 처리. QA 환경은 Windows 10 build 26200 / Python 3.12.10이다.

**Spec:** [v5.1 기존 설계](../../PRODUCTION_V5_1_UPGRADE.md), [원본 패키지 아키텍처](file:///C:/Users/Declan/Downloads/Production_Package_v5.1_Architecture.md), [원본 스토리보드 프롬프트](file:///C:/Users/Declan/Downloads/Universal_Production_Storyboard_Master_Prompt_v5.1.md), [전체 QA 보고서](file:///C:/Users/Declan/Documents/03_studio_production/production-v51-overall-qa-20261006-214733/09_QA/overall-qa-report.json).

이 문서는 구현 추적 기준이다. 사용자 승인에 따라 Q01~Q23 구현과 native acceptance를 완료했고, 독립 검토에서 발견한 후속 경계 사례도 수정·재검증했다. ReviewGatePublication 및 ReviewHistoryHandoff는 각각 최종 APPROVE다. 기본 Windows locale의 `python -m pytest -q`는 cp949 디코딩 오류와 수정 전 회귀 assertion으로 실패했으나, assertion을 동작 중심으로 수정한 뒤 `python -X utf8 -m pytest -q` 전체 suite가 통과했다. 구현·기계 검증은 완료다. 배포는 별도 승인 대상이므로 현재 `BLOCK`이며, 미해결 코드 리뷰 finding을 의미하지 않는다.

## Global Constraints

다음 조건은 모든 작업에 적용한다.

- QA ID `Q01`~`Q23`을 그대로 유지한다. HIGH 11건, MEDIUM 12건을 누락하거나 다른 결함으로 대체하지 않는다
- `schema_version=1.1`과 기존 제작 정본을 유지한다. 현재 패키지는 2.4, 설치 스킬은 18개다. 이 보완만을 위해 스킬·원장·승인 체계를 추가하지 않는다
- 실제 제작 결과는 선택된 제작 프로젝트에 저장한다. 저장소에는 재사용 코드·템플릿·문서를 유지한다
- 기본 위치는 실제 Documents의 `studio_production/<project_id>`다. 명시적으로 선택한 root는 그대로 사용한다. 사용자명을 코드에 고정하지 않는다
- FINAL은 활성 LOOK과 관련 마스터 계보의 검증·정확한 버전, 현재 시트와 실제 패널·씬 추출을 요구한다. PRELIMINARY와 좁은 텍스트 작업의 기존 합법적 범위는 유지한다
- 시트당 패널은 최대 8개다. 전체 패널 순서, 장면 연결, 실제 이미지 픽셀과 출처를 보존한다
- 변경 시 실제 종속 분기만 `stale`로 표시한다. 과거 버전 핀을 최신 버전으로 몰래 바꾸지 않는다
- 기존 사용자 변경, 원본 미디어, 기존 이력, 저장소의 `video-production-assets/support` 캐시와 전역 설치를 보존한다
- 외부 생성 서비스 호출, 지출, 새 작품 생성, 가짜 승인·산출물 작성은 범위 밖이다
- 공개 인터페이스를 변경하기 전 참조를 조사하고 실제 호출자·테스트·계약 문서를 함께 갱신한다
- 테스트는 사용자에게 보이는 동작·경계·오류·상태 전이를 검증한다. 소스 문자열, 함수 전달 여부, 목 객체의 응답 복사만 검사하는 테스트는 만들지 않는다

## Review Focus

다음 다섯 입력·전이는 해당 작업의 회귀 테스트에 포함한다.

1. 프로젝트 내부 이름이 외부 파일을 가리키는 dangling symlink 또는 junction이면 쓰기·자동 수집 전에 차단한다: 작업 1, Q06~Q08
2. 창작 문장에 JSON 비밀값과 Windows 줄바꿈이 섞이면 비밀값만 가리고 원본 파일 지문은 보존한다: 작업 2, Q09·Q18·Q22
3. 파일이 존재해도 마스터가 미검증이거나 패널 출처·추출 영역이 잘못 연결되면 FINAL을 거부한다: 작업 3~4, Q01~Q04·Q16
4. 내보내는 도중 원본이 바뀌거나 등록 파일명이 자동 보고서와 충돌하면 원본을 보존하고 잘못된 ZIP을 게시하지 않는다: 작업 5, Q05·Q12·Q13
5. 재개·늦은 완료·원본 버전 변경은 해당 작업 번호와 종속 분기만 갱신한다. 이미 없어진 결과물을 완료로 인정하지 않는다: 작업 6~7, Q10·Q11·Q14·Q15·Q19~Q21

## 경로·폴더 경계·마스킹의 의미

여기서 보완하는 대상은 폴더 주소 자체가 아니라 자동 파일 접근과 로그 저장 동작이다.

| 용어 | 의미 | 이번에 확인한 문제 | 기대 동작 |
|---|---|---|---|
| 경로 | 폴더·파일의 주소. 예: `Documents/studio_production/film_a/04_STORYBOARDS/board.png` | 새 사용자 지정 폴더를 초기화할 때 원하지 않는 하위 폴더가 추가됨: Q17 | 선택한 주소를 그대로 사용 |
| 폴더 경계 | 결과물·이력·ZIP 자동 수집을 선택한 작업 폴더 안으로 제한하는 규칙 | 안쪽 파일명·폴더가 외부를 가리키면 결과물이 밖에 생성되거나 외부 파일이 ZIP에 포함됨: Q06~Q08 | 실제 연결 목적지까지 확인하고 외부 접근을 거부 |
| 링크 | 다른 위치를 가리키는 파일시스템 연결. Windows junction과 symlink가 이에 해당하며 일반 `.lnk` 바로가기와는 다름 | 문자열 주소는 안쪽인데 실제 읽기·쓰기 위치는 바깥인 경우 | 링크 대상이 없더라도 안전한 새 출력 파일로 취급하지 않음 |
| 마스킹 | 저장하는 로그 복사본에서 API 키·비밀번호·접근 토큰 값을 `[REDACTED]`로 치환 | JSON이나 공백 포함 설정에서 비밀값이 평문으로 저장됨: Q09 | 비밀값만 숨기고 창작 내용은 유지 |
| 파일 지문 | 파일 원본 bytes의 SHA-256. 내용이 달라지면 값도 바뀜 | Windows 줄바꿈을 바꾼 뒤 계산하여 원본 지문과 달라짐: Q18 | 원본 bytes로 먼저 계산 |
| `stale` | 이전 입력 버전으로 만들어 다시 검토·생성해야 하는 상태 | 패널에만 적힌 마스터 버전 변경은 이 상태가 전파되지 않음: Q14 | 실제 종속 결과만 재작업 대상으로 표시 |

폴더 경계 예시는 다음과 같다. `film_a/.history`가 `other_folder`를 가리키면, `film_a`를 묶는 ZIP에 `other_folder`의 파일이 들어가면 안 된다. 이번 QA는 직접 만든 무해한 시험 파일로 이를 재현했다. 실제 개인정보 유출이 확인됐다는 뜻은 아니다.

마스킹은 이미지에 마스크를 씌우는 작업이 아니다. 원본 프롬프트를 지우거나 창작 지시를 바꾸는 작업도 아니다. 아래 값은 설명용 가짜 자격증명이다.

```json
{"api_key": "fake_key_1234567890", "scene": "폭우 속 골목"}
```

history에 저장하는 복사본은 다음과 같아야 한다.

```json
{"api_key": "[REDACTED]", "scene": "폭우 속 골목"}
```

작업 폴더 밖 자동 접근과 명시적 입력은 구분한다. 직접 지정한 `--prompt-file` 같은 외부 원본 입력의 기존 읽기 범위를 무조건 금지하지 않는다. 이 작업은 관리 대상 산출물·이력의 쓰기와 ZIP 자동 수집 경계를 보완한다.

## 우선순위별 실행 묶음

같은 파일을 여러 작업이 수정하므로 아래 순서로 통합한다. 파일을 공유하는 작업을 동시에 편집하지 않는다.

| 순서 | 작업 | QA ID | 건수 | 중요도 | 권장 책임 |
|---|---|---|---:|---|---|
| 1 | 작업 폴더 밖 접근 차단 | Q06, Q07, Q08 | 3 | HIGH 3 | 파일 입출력 담당 |
| 2 | 비밀값 마스킹·원본 기록 보존 | Q09, Q18, Q22 | 3 | HIGH 1 / MEDIUM 2 | history 담당 |
| 3 | FINAL·제작 준비 게이트 통합 | Q01, Q02, Q23 | 3 | HIGH 2 / MEDIUM 1 | 자산·준비 검사 담당 |
| 4 | 패널 출처·실제 추출 연결 검증 | Q03, Q04, Q16 | 3 | HIGH 2 / MEDIUM 1 | 스토리보드 추출 담당 |
| 5 | ZIP 무결성·재개봉 보장 | Q05, Q12, Q13 | 3 | HIGH 1 / MEDIUM 2 | 패키징 담당 |
| 6 | 완료·재개·선택 폴더 초기화 보완 | Q10, Q11, Q17, Q19, Q20, Q21 | 6 | HIGH 2 / MEDIUM 4 | history·저장 담당 |
| 7 | 변경 전파·작업자 입력 연결 보완 | Q14, Q15 | 2 | MEDIUM 2 | 정본 인계 담당 |
| 합계 | 전체 수정 및 재검증 | Q01~Q23 | 23 | HIGH 11 / MEDIUM 12 | 총괄 통합·QA |

## QA 23건 수정 지시 및 완료 판정표

아래 표가 보완 범위의 추적 기준이다. 각 행은 구현 후 실제 검증 증거를 확보했을 때만 완료로 바꾼다. 파일 위치는 QA 당시 기준이다. 구현 전 현재 심벌과 호출자를 다시 확인한다.

| ID | 중요도 | QA 당시 위치 | 수정 지시 | 완료 판정 | 상태 |
|---|---|---|---|---|---|
| Q01 | HIGH | `asset_gate.py:40–47` | 필요한 에셋부터 `master_asset_ref` 전체 계보의 verified 상태·정확한 버전을 검사 | 검증된 derivative라도 상위 마스터가 planned·미생산이면 FINAL 거부, 정상 계보는 허용 | 완료 |
| Q02 | HIGH | `validate_preproduction.py:193–195` | 필수 split 포인터, ordered sheets/hash, 전체 패널·씬과 등록된 실제 추출 파일을 공통 준비 검사에 포함 | 오래된 split/hash/order 및 P02→P01 alias를 준비·review·execution에서 거부 | 완료 — native 재현 및 독립 APPROVE |
| Q03 | HIGH | `split_storyboard.py:499–506` | PNG 출처 ID/version/hash와 scene/shot/asset pins를 정본 패널과 대조, 필수 출처 누락을 거부 | P01의 출처를 IM02로 바꾸면 추출 실패, 정상 출처는 원본 픽셀 유지 | 완료 |
| Q04 | HIGH | `package_production.py:151–157` | panel/scene별 등록 에셋의 실제 대응과 출처·기하를 검증 | P02를 P01 파일에 연결한 split은 거부하고, 합법적인 S01→S02→S01 scene band 순서는 허용하며 중첩 bounds는 거부 | 완료 — native 재현 및 독립 APPROVE |
| Q05 | HIGH | `package_production.py:194–195` | 자동 생성 경로를 예약하고 등록 파일·파생 파일 경로 충돌을 거부 | 등록된 QA 파일 및 Windows 대소문자 alias를 덮지 않고 충돌 시 새 FINAL ZIP을 만들지 않음 | 완료 — native 재현 및 독립 APPROVE |
| Q06 | HIGH | `render_storyboard_sheet.py:521–527` | `_sNN.png` 출력 각각을 생성 전에 실제 경로·기존 링크까지 검사 | dangling symlink가 외부를 가리켜도 외부 PNG 및 부분 결과를 생성하지 않음 | 완료 |
| Q07 | HIGH | `package_production.py:231–235` | `.history` 및 하위 파일의 실제 목적지를 root 안으로 제한 | 외부 시험 파일이 ZIP에 포함되지 않으며 경계 위반을 명시적으로 거부 | 완료 |
| Q08 | HIGH | `production_history.py:335–342` | `.history`, events, prompts, lock의 조상·실제 목적지를 쓰기 전에 검사 | 외부 junction 대상에 이벤트·스냅샷·lock 파일이 생성되지 않음 | 완료 |
| Q09 | HIGH | `production_history.py:121–123` | quoted key 및 `=`/`:` 주변 공백이 있는 자격증명을 마스킹 | event·prompt snapshot 모두 비밀값 없이 저장, 창작 문장 보존 | 완료 |
| Q10 | HIGH | `production_history.py:650–657` | 완료된 작업도 현재 산출물 존재 여부 재검사, 미해결 중단·실패 완료 정책 일치 | 완료 파일 삭제 또는 현재 attempt 중단·실패 상태에서는 프로젝트 완료 거부, 성공적 재시도 후에는 허용 | 완료 |
| Q11 | HIGH | `production_history.py:639–644` | terminal 이벤트를 현재 pending start의 실제 attempt ID와 대조 | attempt 2 진행 중 늦은 attempt 1 완료가 상태를 바꾸지 않음 | 완료 |
| Q12 | MEDIUM | `package_production.py:237–241` | 이동한 registry 경로와 split 내부 경로를 함께 재투영하고 파생 snapshot hash 갱신 | 비표준 경로 입력으로 만든 ZIP을 새 폴더에 풀어 검증·FINAL 재패키징 성공 | 완료 |
| Q13 | MEDIUM | `package_production.py:383–389` | 실제 복사 byte stream의 SHA-256을 검사하고 불일치 시 게시 중단 | 복사 직전 원본 변경 주입 시 잘못된 FINAL ZIP이 생성되지 않음 | 완료 |
| Q14 | MEDIUM | `update_project.py:151–160` | panel-only `asset_version_refs`를 보드의 종속 관계에 반영 | 마스터 변경이 정상 반영되고 BOARD와 관련 downstream만 stale, 과거 핀과 무관한 분기 보존 | 완료 |
| Q15 | MEDIUM | `project_index.py:81–93` | master/required/panel pins를 전이 수집, 활성 LOOK pointer 및 asset 포함 | focused 패킷에 필요한 마스터·LOOK·핀 정보가 모두 있고 무관한 샷은 제외 | 완료 |
| Q16 | MEDIUM | `split_storyboard.py:351–355` | clean panel bounds와 scene band의 중첩·잘못된 배치를 사전 검사 | P02 bounds를 P01 bounds로 바꾸면 실패, 정상 장면 경계 추출은 유지 | 완료 |
| Q17 | MEDIUM | `production_history.py:264–272` | init API/CLI에 선택 root 직접 초기화 기능을 추가하고 coordinator와 연결 | 선택 폴더에 그대로 초기화, 불필요한 `studio_production/selected` 중첩 없음, 기존 원장 보존 | 완료 |
| Q18 | MEDIUM | `production_history.py:688–696` | 원본 bytes로 hash 후 UTF-8 decode·마스킹 분리 | CRLF·LF 각각 실제 원본 bytes의 SHA-256과 기록값이 일치 | 완료 |
| Q19 | MEDIUM | `production_history.py:309–313` | 초기 `project.json`을 동일 디렉터리에서 staging 후 기존 파일을 덮지 않고 원자적으로 게시 | 첫 JSON byte 쓰기 뒤 종료돼도 깨진 정본이 남지 않고 정상 init 재시도 성공 | 완료 |
| Q20 | MEDIUM | `production_history.py:778–784` | 실제 pending attempt ID를 자동 terminal/resume에 사용 | 명시적 start 7에 대한 interruption·기본 terminal도 7로 기록 | 완료 |
| Q21 | MEDIUM | `production_history.py:407–409` | operation-scope started만 attempt 개수 계산에 포함 | project lifecycle과 같은 ID를 사용해도 첫 operation 번호·개수 계산이 섞이지 않음 | 완료 |
| Q22 | MEDIUM | `production_history.py:380–384` | JSON string metadata를 decode하고 raw scalar와 구분 | 따옴표·개행 포함 작업 설명이 status·resume 후에도 원문과 동일 | 완료 |
| Q23 | MEDIUM | `validate_storyboard.py:88–91` | dictionary membership 전에 selector가 유효한 문자열인지 검사 | 배열·객체 입력에 traceback 대신 해당 필드의 구조화 진단 반환 | 완료 |

위 표의 Python 파일은 `video-production-assets/scripts/` 아래에 있다. `production_history.py`만 `recording-production-history/scripts/` 아래에 있다. 각 ID의 재현 입력과 실제 결과는 [27개 CLI/API 시나리오 증거](file:///C:/Users/Declan/Documents/03_studio_production/production-v51-overall-qa-20261006-214733/09_QA/parent-cases/captured-parent-reproductions.json)에 있다.

## 구현자용 작업별 인터페이스와 검증

기존 재현 증거를 덮어쓰지 않는다. 각 회귀 테스트는 새 임시 프로젝트와 직접 만든 무해한 외부 시험 파일을 사용한다. 기존 증거의 junction을 그대로 실행하여 원래 목적지에 쓰지 않는다.

공통 진행 방식은 다음과 같다.

- 회귀 테스트는 격리된 합성 fixture로 사용자 관찰 동작·경계·상태 전이를 확인한다. 원본 QA fixture는 보존한다.
- 병렬 통합 중에는 중간 suite를 실행하지 않았다. 최종 통합 suite 결과와 실제 CLI/API acceptance는 [구현 검증 기록](../../evidence/production-v51-qa-remediation.md)에 남겼다.
- 지정된 파일과 실제 호출자만 수정하고, 우회·예외 삼키기·불필요한 재설계를 피한다.
- 선택 테스트·실제 CLI/API smoke·전체 검증은 통합 후 수행하고 실제 출력만 기록한다.
- 공유 파일의 편집 소유자를 명확히 하고, 통합 뒤에는 총괄이 최종 검증한다.

### 작업 1: 결과물과 이력의 실제 저장 경계를 지킨다

**Files:** `video-production-assets/scripts/render_storyboard_sheet.py`, `video-production-assets/scripts/package_production.py`, `recording-production-history/scripts/production_history.py`.

**Tests:** `video-production-assets/scripts/test_render_storyboard_sheet.py`, `video-production-assets/scripts/test_asset_gate.py`, `recording-production-history/scripts/test_production_history.py`.

**Interfaces:** 기존 `render_sheets(project, base_dir, output, *, font_path=None, panels_per_sheet=MAX_PANELS_PER_SHEET)`, `build_package(project, base, dest_root, zip_path=None, require_final=False, include_history=True)` 및 history CLI의 정상 호출을 유지한다. 관리 대상 출력·이력·수집 파일의 실제 목적지를 승인한 root 안으로 제한한다. 기존 링크를 새 빈 파일처럼 취급하지 않는다.

- [x] Q06 회귀 `test_paginated_dangling_link_writes_nothing_outside`: 10패널 입력과 `_s01.png` dangling symlink에서 명령 실패, 외부 파일 없음, 남은 부분 시트 없음
- [x] Q07 회귀 `test_history_junction_export_rejected`: 외부 sentinel을 가리키는 `.history`에서 export 실패, 새 ZIP 없음, sentinel 원본 유지
- [x] Q08 회귀 `test_history_junction_write_rejected`: events/prompts/lock 대상의 외부 연결에서 작업을 거부하고 외부 디렉터리 내용 불변
- [x] 새 10패널 프로젝트의 실제 renderer 및 내부 history CLI를 실행한다. 정상 2시트와 내부 이벤트 파일 생성은 계속 성공해야 한다

### 작업 2: 비밀값을 숨기되 원본 창작 지시와 지문을 보존한다

**Files:** `recording-production-history/scripts/production_history.py`, `recording-production-history/SKILL.md`.

**Tests:** `recording-production-history/scripts/test_production_history.py`.

**Interfaces:** `record`의 `prompt_sha256`은 마스킹 전 원본 파일 bytes의 SHA-256이다. event와 prompt snapshot에는 같은 마스킹 결과를 저장한다. operation 문자열은 writer의 JSON serialization과 reader의 decoding을 왕복해도 동일해야 한다.

- [x] Q09 회귀 `test_quoted_and_spaced_credentials_redacted`: JSON API key/password, 공백 포함 token과 창작 문장을 함께 넣어 두 저장본에서 비밀값 제거·창작 문장 보존을 검증
- [x] Q18 회귀 `test_original_prompt_byte_digest_preserved`: 실제 CRLF·LF bytes 각각의 hash와 기록값 일치, 원본 프롬프트 파일 bytes 불변
- [x] Q22 회귀 `test_operation_description_round_trip`: 따옴표·개행 포함 operation에 대해 start → status → resume → status의 설명값이 원문과 일치
- [x] 실제 CLI 생성 event와 snapshot을 열어 확인한다. 허위 토큰만 사용하고 실제 계정 비밀값은 시험에 사용하지 않는다

### 작업 3: FINAL과 준비 판정을 같은 실제 입력에 적용한다

**Files:** `video-production-assets/scripts/asset_gate.py`, `video-production-assets/scripts/validate_preproduction.py`, `video-production-assets/scripts/validate_project.py`, `video-production-assets/scripts/validate_storyboard.py`, `video-production-assets/scripts/package_production.py`.

**Tests:** `video-production-assets/scripts/test_asset_gate.py`, `video-production-assets/scripts/test_validate_preproduction.py`, `video-production-assets/scripts/test_validate_project.py`, `video-production-assets/scripts/test_validate_storyboard.py`.

**Interfaces:** 기존 `check_asset_gate(project, artifact_ids=None)`과 `validate_preproduction(project, base_dir=None, *, image_backed_required=False, panels_per_sheet=8)`의 결과 형식을 유지한다. 준비 검사 내부에 실제 sheet-derived extraction 검사를 한 번 정의하고 FINAL 패키징에서도 이를 사용한다. 파일 누락·버전 불일치는 승인 근거가 될 수 없다.

- [x] Q01 회귀 `test_final_rejects_unverified_master_ancestor`: 직접·다단계 마스터 계보를 검사한다. planned/missing/stale/버전 불일치는 FINAL에서 거부하고 정상 verified 계보는 통과
- [x] Q02 회귀 `test_split_entry_sheet_path_must_match_current_registered_sheet`, `test_split_manifest_bytes_must_match_registered_sha`, `test_replaced_registered_sheet_invalidates_existing_split`, `test_split_panel_outputs_cannot_alias_another_panel`, `test_transparent_panel_output_does_not_match_opaque_sheet_crop`, `test_transparent_scene_output_does_not_match_opaque_sheet_bands`, `test_overlapping_produced_sheet_bounds_are_rejected`: stale registration/hash/order, aliases, RGBA alpha mismatch와 panel/scene overlap을 공통 readiness에서 거부한다. `test_missing_wrong_stale_or_incomplete_deliverables_block_review`는 실제 CLI의 valid 0/true 및 15개 변형의 exit1/false를 검증한다. 독립 native after-probes는 실제 FINAL 거부·대상 미생성과 single-sheet no-index FINAL18, repeated scene FINAL26, 10-panel/two-sheet FINAL30 positive control을 확인했다
- [x] Q23 회귀 `test_invalid_storyboard_selector_returns_diagnostics`: 배열·객체로 잘못 선언한 selector에 구조화 오류를 반환하고 CLI traceback 없음. 선택값 생략을 허용하는 기존 standalone 범위는 유지
- [x] 실제 `validate_project.py --profile preproduction`와 FINAL renderer/package 명령을 정상·불완전 fixture 각각에 실행한다. 단순 plan 저장과 합법적인 PRELIMINARY는 준비 승인과 구분한다

### 작업 4: 패널별 출처·픽셀·장면을 정본과 일치시킨다

**Files:** `video-production-assets/scripts/split_storyboard.py`, 작업 3의 공통 extraction 검사, `video-production-assets/scripts/package_production.py`의 소비 경계.

**Tests:** `video-production-assets/scripts/test_split_storyboard.py`, `video-production-assets/scripts/test_asset_gate.py`, 필요 시 기존 `test_validate_preproduction.py`.

**Interfaces:** 기존 `split_storyboard(project, base_dir, output_dir, sheets=None)` 반환 manifest와 등록 구조를 유지한다. 각 canonical panel은 정확한 출처와 clean bounds를 가진다. 패키저는 파일 존재·hash뿐 아니라 해당 panel/scene의 대응을 검사한다. 서로 다른 패널이 같은 원본 이미지를 사용하는 정상 경우와 잘못된 추출 파일 alias를 구분한다.

- [x] Q03 회귀 `test_split_rejects_wrong_canonical_source`: PNG의 P01 출처를 현재의 다른 IM02로 바꿔도 거부한다. provenance 누락·잘못된 shot/scene/version pins도 진단한다
- [x] Q04 회귀 `test_final_package_rejects_panel_alias_even_with_current_hashes` 및 `test_final_package_accepts_repeated_scene_bands_in_chronological_order`: P02 alias는 FINAL에서 거부되고, 합법적인 S01→S02→S01 chronological bands 허용된다. 겹치는 panel/scene bounds는 거부된다 (독립 native 재현 및 final review APPROVE)
- [x] Q16 회귀 `test_split_rejects_overlapping_panel_geometry`: P02 bounds를 P01로 교체하면 쓰기 전 실패한다. 이미지가 비슷하다는 이유만으로 정상 비중첩 패널을 거부하지 않는다
- [x] 실제 10패널·2시트 추출 후 모든 canonical ID와 원본 RGB bytes를 대조한다. 반복·교차 scene bands를 검증하고 생성 PNG를 연다. 독립 after-probes는 10-panel/two-sheet FINAL30과 반복 scene FINAL26도 확인했다

### 작업 5: ZIP 안의 실제 파일과 정본 경로·지문을 일치시킨다

**Files:** `video-production-assets/scripts/package_production.py`.

**Tests:** 기존 `video-production-assets/scripts/test_asset_gate.py`의 PackagingTests를 확장한다.

**Interfaces:** 기존 `build_package` 인터페이스와 versioned ZIP을 유지한다. exporter의 경로 대응표를 registry와 split 내부 참조에 같은 방식으로 적용한다. 원본 정본을 수정하지 않으며 ZIP의 파생 snapshot만 재투영한다. 실제 게시 byte stream의 hash는 파생 snapshot과 일치해야 한다.

- [x] Q05 회귀 `test_casefolded_report_path_collision_preserves_source_and_publishes_nothing`: registered `00_MANIFEST/qa_report.md`와 자동 보고서의 Windows 대소문자 alias를 directory·ZIP에서 거부하고 source bytes를 보존하며 archive를 게시하지 않는다 (native after-probes 및 final review APPROVE)
- [x] Q12 회귀 `test_relocated_split_round_trip`: 비표준 sheet/split/panel/scene 경로를 사용한다. ZIP을 새 root에 풀고 내부 참조·hash 검증 및 FINAL 재패키징 성공, 원본 `project.json` bytes 불변
- [x] Q13 회귀 `test_mutation_during_copy_prevents_publication`: 실제 복사 시점에 원본 변경을 주입하여 hash 불일치 시 게시 중단을 확인한다. OS에서 우연히 race가 발생했다고 표현하지 않는다
- [x] 실제 정상 FINAL ZIP을 생성·해제한 뒤 snapshot 기준으로 모든 등록 파일의 bytes/hash를 확인한다. 기존 목적지 파일을 덮어쓰지 않는다

### 작업 6: 완료·재개 번호와 선택한 저장 폴더를 보존한다

**Files:** `recording-production-history/scripts/production_history.py`, `recording-production-history/SKILL.md`, `creative-production/SKILL.md`, `video-production-assets/references/preproduction-review.md`, `README.md`, `USAGE_GUIDE.md`의 해당 호출 예시.

**Tests:** `recording-production-history/scripts/test_production_history.py`.

**Interfaces:** `status.operations[operation_id].attempts`는 operation-scope start 개수다. 실제 마지막 start 번호는 `current_attempt` 정수로 구분하고 `_record`·`_resume`이 사용한다. `initialize_project(project_id, documents=None, *, project_root=None)` 및 `init --project-root ROOT`를 추가한다. `--documents`와 `--project-root`는 동시에 지정하지 못하며, 둘 다 없으면 기존 실제 Documents 기본값을 유지한다.

- [x] Q10 회귀 `test_project_completion_rechecks_latest_outputs`: 완료 파일 삭제 시 project 완료 거부. 현재 attempt가 failed/interrupted여도 완료 거부. 성공한 새 attempt의 실제 산출물이 있으면 허용. 과거 실패 기록을 삭제하거나 취소된 이전 attempt의 미생산 파일을 가짜로 만들지 않음
- [x] Q11 회귀 `test_late_terminal_cannot_close_new_attempt`: 1 중단 → 2 시작 → 늦은 1 완료 거부 → 실제 2 완료 성공, 각 상태·번호 대조
- [x] Q17 회귀 `test_explicit_root_init_preserves_selection`: exact root 직접 초기화와 기존 동일 프로젝트의 재사용 성공, 다른 프로젝트 원장·원본 파일을 덮지 않음
- [x] Q19 회귀 `test_interrupted_initial_ledger_is_retryable`: staging의 첫 byte 후 child 종료를 주입한다. 깨진 canonical ledger를 게시하지 않고 정상 init 재시도 성공. 기존 사용자 손상 원장은 자동 삭제·수리하지 않음
- [x] Q20 회귀 `test_explicit_attempt_retained_on_resume_and_terminal`: start 7의 resume 및 기본 terminal이 각각 7을 사용
- [x] Q21 회귀 `test_project_events_excluded_from_attempt_count`: 같은 ID의 project start와 operation start가 섞여도 operation count와 자동 attempt 계산이 일치
- [x] 실제 history CLI로 start → resume → retry → operation completion → project completion을 실행한다. 마지막 in_flight가 비고 완료 파일이 실제 존재하는지 확인한다

project 완료 시 최신 attempt의 start·terminal에 선언된 산출물을 현재 디스크에서 확인한다. 이전 attempt는 불변 이력으로 남기되 성공한 재시도를 영구 차단하는 다른 완료 원장을 만들지 않는다. 이력 완료는 QA·예술성·사용자 승인 완료를 대신하지 않는다.

### 작업 7: 변경된 입력이 영향을 주는 결과에만 전파되게 한다

**Files:** `video-production-assets/scripts/update_project.py`, `video-production-assets/scripts/project_index.py`, `video-production-assets/scripts/validate_storyboard.py`와 관련 validation 경계, `video-production-assets/references/contract.md`.

**Tests:** `video-production-assets/scripts/test_project_handoff.py`, `video-production-assets/scripts/test_asset_gate.py`, `video-production-assets/scripts/test_validate_storyboard.py`.

**Interfaces:** 기존 `prepare_update(current, delta)`와 guarded `apply_update(project_path, delta)`를 유지한다. panel pins는 현재 storyboard 소유 artifact의 종속 입력이다. `build_index(project, shot_ids=(), artifact_ids=())`는 필요한 master 계보와 required/panel pins, 활성 `look_asset_id` 및 해당 asset을 전달한다. 전체 프로젝트를 무조건 보내 focused 범위를 없애지 않는다.

- [x] Q14 회귀 `test_panel_only_pin_stales_dependent_branch`: LOOK만 required map에 있고 IDENTITY는 panel에만 핀한 유효한 입력에서 IDENTITY 버전을 올린다. 실제 guarded update 성공, BOARD와 SHEET·GEN·ANIMATIC 같은 종속 분기 stale, 무관한 AUDIO 유지
- [x] stale 보드의 과거 version refs는 역사적 입력으로 보존하여 정본 업데이트를 막지 않는다. stale 결과의 준비 승인·FINAL 생산은 계속 거부한다
- [x] Q15 회귀 `test_focused_packet_contains_master_and_active_look`: SH01 패킷에 derivative·상위 master·LOOK·정확한 pins가 포함되고 무관한 shot/artifact는 빠짐
- [x] 실제 update CLI의 반환 stale ID와 저장된 정본 상태를 대조한다. 이후 index CLI를 실행하여 전달 패킷에 dangling master 참조가 없는지 확인한다

## 통합 검증과 배포 판정

표의 각 완료 판정과 실제 실행 증거를 충족해야 수정 완료로 기록한다. 과거의 테스트 통과 기록을 이번 수정의 증거로 재사용하지 않는다.

- [x] Q01~Q23 각각의 구현, regression, native CLI/API 수용 사례, 남은 제한은 [구현 검증 기록](../../evidence/production-v51-qa-remediation.md)에 연결했다. Q02/Q04/Q05 후속 독립 finding은 해결되었고, 두 reviewer 모두 최종 APPROVE했다.
- [x] 기본 locale 전체 suite 실패와 수정 후 UTF-8 전체 suite 통과, version check 및 staging/runtime 원본 출력을 새 [최종 verification 증거](../../evidence/production-v51-final-verification.json)에 기록했다. 기본 locale 실패는 27개 Windows cp949 fixture decode 오류와 수정 전 3개 checker assertion이며, 올바른 UTF-8 mode 전체 suite는 통과했다.

```powershell
python -m pytest -q
python -X utf8 -m pytest -q
python scripts/check_versions.py
```

명령은 저장소 root에서 실행했다. 기본 Windows locale 실행은 `30 failed, 240 passed, 205 subtests passed`였고, final UTF-8 mode 전체 suite는 `258 passed, 217 subtests passed`였다. 기본 `python -m pytest -q` invocation은 재실행하지 않았다; 한 UTF-8 full-suite run은 CLI test method refinement 전 intermediate였고, 마지막 run은 최종 CLI behavior tests 뒤 실행됐다. UTF-8 mode는 인코딩 환경만 명시한다.

- [x] 정상 FINAL ZIP, 10패널·2시트 결과, 반복 scene-band 조립을 실제로 실행하고 합성 결과 이미지를 열었다
- [x] Source support cache remains untouched; a clean isolated copy installed all 18 skills and ran history init/status plus installed package CLI smoke. Independent installed-runtime proof also exercised actual FINAL18 acceptance, transparent-P02 pixel rejection/no target, history completion after attempt 7→3/current-output deletion/restoration, final status, and prompt/secret handling (`final-installed-*` cases in the [physical-root raw follow-up evidence](file:///C:/Users/Declan/Documents/03_studio_production/production-v51-remediation-parent-verification-20261006-233729/independent-review-followup-evidence.json)).
- [x] Windows 기본 locale의 cp949 실패와 source support 충돌 원인·범위·결과를 별도 운영 확인으로 보고한다. 새 QA 결함으로 위장하거나 자동 정리하지 않았다
- [x] macOS/Linux 실제 결과가 없으면 Windows 검증과 교차 OS 미검증을 구분한다. redirect/OneDrive, 지속 동시 실행, 실제 disk-full, provider·Blender 역시 관찰한 범위만 보고한다
- [x] 소스·계약이 실제로 변경된 시점에 관련 usage/skill 문서와 CHANGELOG를 갱신한다. 이 작업지시서 작성만으로 수정 완료 changelog를 쓰지 않는다
- [ ] 총괄은 배포 권한을 별도로 확인한 뒤 배포 차단 해제 여부를 판정한다. 구현 승인과 독립 code-review APPROVE는 배포 승인을 대신하지 않으므로 현재 배포는 `BLOCK` 유지한다

## 재현 근거와 인계 상태

근거 파일은 확인 당시 결과를 보존한다. 이번 구현 통합 검증은 기존 QA fixture 바깥의 [구현 검증 기록](../../evidence/production-v51-qa-remediation.md)과 [명령 출력 증거](../../evidence/production-v51-qa-remediation-commands.txt)에 저장했다.

- [전체 QA 23건 보고서](file:///C:/Users/Declan/Documents/03_studio_production/production-v51-overall-qa-20261006-214733/09_QA/overall-qa-report.json)
- [27개 부모 CLI/API 시나리오](file:///C:/Users/Declan/Documents/03_studio_production/production-v51-overall-qa-20261006-214733/09_QA/parent-cases/captured-parent-reproductions.json)
- [전체 테스트 원본 출력](file:///C:/Users/Declan/Documents/03_studio_production/production-v51-overall-qa-20261006-214733/09_QA/full-suite-output.txt)
- [코드 무결성 독립 리뷰](file:///C:/Users/Declan/Documents/03_studio_production/production-v51-overall-qa-20261006-214733/09_QA/integrity-review.json)
- [이력 독립 리뷰](file:///C:/Users/Declan/Documents/03_studio_production/production-v51-overall-qa-20261006-214733/09_QA/history-review.json)
- [아키텍처 독립 리뷰](file:///C:/Users/Declan/Documents/03_studio_production/production-v51-overall-qa-20261006-214733/09_QA/architecture-review.json)
- [Windows Q01~Q23 최종 acceptance 요약](file:///C:/Users/Declan/Documents/03_studio_production/production-v51-remediation-parent-verification-20261006-233729/independent-final-acceptance-summary.json)
- [Windows Q01~Q23 raw CLI/API transcript](file:///C:/Users/Declan/Documents/03_studio_production/production-v51-remediation-parent-verification-20261006-233729/independent-acceptance-evidence.json)
- [Q02/Q04/Q05 후속 재현 및 수정 요약](file:///C:/Users/Declan/Documents/03_studio_production/production-v51-remediation-parent-verification-20261006-233729/independent-review-followup-summary.json)
- [Q02/Q04/Q05 후속 raw 재현](file:///C:/Users/Declan/Documents/03_studio_production/production-v51-remediation-parent-verification-20261006-233729/independent-review-followup-evidence.json)
- [최종 suite/version/staging raw output](../../evidence/production-v51-final-verification.json)

**문서 상태:** 갱신 완료. **구현 상태:** Q01~Q23 native acceptance 및 두 독립 review APPROVE 완료; default locale 실패와 UTF-8 mode full-suite pass를 별도로 기록했다. **배포 상태:** BLOCK 유지. 사용자 승인은 구현을 허가했으나 배포 승인을 포함하지 않는다.
