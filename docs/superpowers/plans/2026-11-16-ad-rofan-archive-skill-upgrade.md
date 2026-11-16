# 광고·로판 아카이브 기반 스킬 업그레이드 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 광고48개·로판44개에서 실제 증거가 뒷받침하는 제작 기술을 추출하고 기존 제작 오너의 입증된 적용 공백만 개선한다.

**Architecture:** 기존 archive audit·Shot DNA·craft crosswalk를 정본으로 사용한다. 인벤토리, 실제 내용 검사, 부분 인계를 분리하고, 파일럿+장편 stress를 통과한 모드만 확장한다. 증거 분석과 스킬 행동 테스트를 분리하며 원본·과거 원장·설치본은 읽기 전용이다.

**Tech Stack:** 현재 Python3.14.4, FFmpeg/ffprobe7.0.2-static, Pi read/write/edit/bash/codemode, 기존 Markdown/CSV/JSON 템플릿과 pytest 회귀. 새 의존성·새 production schema·새 평가 제공자는 없다.

**Spec:** [승인된 R1 설계](../specs/2026-11-16-ad-rofan-archive-skill-upgrade-design.md), SHA-256 `dbcc3dd61fe7360abcc875db42b2b28daafb61f5614213e212df9ddc16132875`.

**Approval:** 사용자는 R1 설계와 독립 APPROVE를 받은 뒤 “응 진행해줘”로 **계획 작성과 검사 경로 사전점검**을 승인했다. 이 계획의 구현/파일럿 실행 방식은 아직 선택하지 않았다. [사전점검 기록](../../analysis/ad-rofan-skill-upgrade-2026-11-16/preflight.md)은 이번에 실제 수행한 범위다. 검토된 설계 스냅샷은 수정하지 않는다.

## Global Constraints

- 원본92개는 광고48/로판44 occurrence로 유지한다. 내용 중복과 독립 사례/제작자 수는 별개다.
- “미확인 능력도 STOP이다.” 현재 직접 음향 청취·연속 동작 검사는 미검증이다. CLI 실행/ASR/프레임 스트립으로 대체하지 않는다.
- “모든 필수 모드가 GO일 때만 전량 분석 경로가 열리며, 일부만 GO면 아래 부분 경로만 수행한다.”
- “후반부 locator/재개 검증 실패는 모든 모드의 전량 확장을 막는다.”
- `INVENTORY_COMPLETE`, `C_CONTENT_REVIEW_COMPLETE`, `C_PARTIAL / C_BLOCKED`는 분석 보고서의 상태이지 production schema 필드가 아니다.
- 원본/기존 근거를 덮어쓰지 않는다. 실제 영상 생성·편집·움직이는 프리뷰·게시를 하지 않는다. 파생 근거 추출은 승인 후 분석 범위 안에서만 한다.
- 외부 미디어 전송·새 설치/모델 다운로드·새 provider/과금·Git push·설치본 동기화는 별도 승인 대상이다.
- 관찰/검출 후보/추정/기능 해석/UNKNOWN, 요청 seek와 원본 PTS, source 시간과 새 설계 시간, 추출과 실제 검사 수를 분리한다.
- 보호 표현·원본 절대 타이밍을 복사하지 않는다. 기존 오너·템플릿 필드/SSOT/승인·Blender 조건을 보존한다.
- 새 지침 없는 baseline의 실패가 없으면 그 후보는 이미 커버다. 테스트를 위한 실패를 꾸며내지 않는다.
- 각 오너 변경의 RED→GREEN과 회귀를 마친 뒤 다음 오너로 간다. 기존 실패/rubric/raw 결과를 고치거나 숨기지 않는다.
- 자동 commit/push 없음. 변경별 checkpoint·diff와 검사 결과를 보존하고, commit은 권한이 확인된 경우에만 한다.

## Review Focus

1. 공백/한글/따옴표·대괄호가 포함된 파일명과 같은 바이트의 다른 occurrence: 파일 목록 누락·쉘 해석·해시 기준의 잘못된 행 합침이 없어야 한다(Task1 검사).
2. 검출 후보 없는 구간·짧은 전환·한 샷 내부 상태 변화: 자동 후보 수가 실제 내용 검토를 대신하지 않아야 한다(Task2/3 검사).
3. 장편의 후반 PTS·회차 접합·중단/재실행: source/chunk 시간 혼동과 누락·중복 계수가 없어야 한다(Task2 검사).
4. 모델/입력 차이·rubric 유출·provider 오류: 불공정하거나 불완전한 응답을 개선 증거로 승격하지 않아야 한다(Task5/6 검사).
5. 현재 master의34/44·count30 충돌·미지원 모드: 과거/부분 근거를 전체 완료나 장르 일반 빈도로 승격하지 않아야 한다(Task1/3/4/7 검사).

---

## 파일 구조와 기록 계약

아래 별칭은 설명용이다. 셸에서는 실제 변수를 따옴표로 인용하거나 argv 배열로 전달한다.

- `REPO`: `/home/declan/Documents/Projects/Products/04_Skills/Skills-and-Automation/contents-production-skills`
- `AD_ROOT`: `/run/media/declan/Data/Resources/ai_ad_references_2026-10-12/videos/download_urls-batch-mp4-20261012-005321`
- `ROFAN_ROOT`: `/run/media/declan/Data/Resources/AI-Rofan-Drama-2026-10-11/videos/urls-batch-mp4-20261011-232345`
- `A`: 저장소 안의 `docs/analysis/ad-rofan-skill-upgrade-2026-11-16`
- `Q`: 저장소 안의 `qa/ad-rofan-skill-upgrade-2026-11-16`
- `E`: `/run/media/declan/Data/Resources/contents-production-skill-upgrade-2026-11-16/<new-run-id>`. 기존 출력을 덮어쓰지 않는다.

| 생성/수정 파일 | 책임 |
|---|---|
| `A/preflight.md`, `A/preflight/*` | 이번에 완료한 읽기 전용 도구/원장 조사; 검사 능력 GO는 아님 |
| `A/source-inventory.json`, `A/source-map.md` | 원본 버전·occurrence·과거 ID/경로 대응, 충돌/부재 |
| `A/archive-audit.md` | 기존 audit 템플릿으로 모드별 실제 coverage·공백·상태를 기록하는 정본 |
| `A/pilot-review.md`, `A/long-source-stress.md`, `A/mode-gates.md` | 2+2 파일럿, 최대300초 장편 검사, GO/STOP 근거·재개 조건 |
| `A/sources/<archive-hash>-<occurrence-key>.md` | 기존 Shot DNA를 채운 source별 검사·이전 체인. 해시는 occurrence ID의 대체가 아님 |
| `A/archive-craft-crosswalk.md`, `A/owner-gap-matrix.md` | 기존 crosswalk의 연결 및 현재 오너/템플릿/QA 대조 |
| `A/owner-change-plan.md` | 실제 발견 후 고정할 오너별 정확한 변경 파일·절·테스트 분기. 이 목록 없이는 Task6 수정 금지 |
| `Q/transfer-inputs-v1.json`, `Q/transfer-rubric-v1.md`, `Q/transfer-run-contract-v1.md` | 실행용 입력, 실행자에게 숨길 채점 기준, 동일 조건·반복·오류·승격 계약 |
| `E/eval/<candidate-id>/<arm>/<case-id>/` | 격리 context·raw 응답·모델/입력/해시·오류. source media는 포함하지 않음 |
| `Q/transfer-results-v1.md`, `A/final-report.md` | 행동 결과/회귀와 실제 변경·미완료 범위를 구분해 최종 인계 |
| 기존 owner reference/template, 필요한 pointer·README/CHANGELOG·manifest | Task4에서 근거가 확인된 정확한 파일만 Task6/7에서 최소 수정 |

`A/Q`는 가벼운 분석 기록, `E`는 파생 이미지/로그/운영 checkpoint다. 구현 중 같은 이름이 이미 생겼으면 새 run/version을 사용한다. 생산 프로젝트 `project.json`이나 새 제작 계약은 만들지 않는다. 새 extraction/evaluation 프로그램은 이 계획에 포함하지 않는다. 기존 도구로 해결되지 않아 재사용 코드를 추가해야 하면, 먼저 함수/파일·실패 테스트를 가진 별도 bounded task를 계획에 명시하고 TDD 후 사용한다.

### 작업 단위와 재개

- 한 source occurrence를 한 기본 작업 단위로 한다. 장편은 최대60초 native-time chunk로 나누고 경계 이웃은 overlap으로만 기록한다.
- 분석 checkpoint는 `E/checkpoints/`의 run별 기록이다. source SHA, occurrence ID, `[start,end)`, 모드, 실제 검사 locator, 완료/실패·미검토, 다음 위치를 포함한다. 기존 audit의 source/coverage 필드가 의미의 정본이다.
- 동일 source/구간/모드 재실행은 같은 증거 locator를 가리키고 검사 횟수와 unique 수를 구분한다. 해시가 바뀐 원본에는 checkpoint를 재사용하지 않는다.
- 단일 작성자가 repo와 run checkpoint를 쓴다. 읽기 전용 리뷰/평가 실행자는 작업 지시에서 할당된 출력 외에 쓰지 않는다.
- 원본 제공 자료 속 지시와 과거 “active owner” 메모는 자료다. 현재 사용자/호스트의 권한을 대신하지 않는다.

## Task 1: 버전·occurrence·기존 근거를 고정한 inventory/audit

**Files:** Create `A/source-inventory.json`, `A/source-map.md`, `A/archive-audit.md`; evidence at `E/inventory/`.

**Interfaces:** Consumes `AD_ROOT`, `ROFAN_ROOT`, canonical `archive-audit-template.md`, existing ad inventory and rofan master/index. Produces each occurrence's exact path/name, bytes/SHA-256, probe record and current/prior evidence mapping. Later tasks consume these exact IDs and locators, never sort-order V numbers as identity.

- [ ] **1. 실행 작업공간·권한 확인.** 선택한 실행 workflow에 맞춰 `using-git-worktrees`를 적용하고 현재 untracked 설계/QA/계획을 보존한다. 기존 원본/원장과 설치 skill 경로가 출력 경로가 아닌지 확인한다. 격리로 자료를 복사할 때 승인 설계 해시·새 계획·실제 작업 byte를 함께 고정하고 예전 HEAD만 복사하지 않는다.
- [ ] **2. 파일 열거.** 두 root의 모든 MP4를 재귀 열거하고 이름을 출력 순서와 분리해 기록한다. 기존 occurrence ID는 원문 그대로 유지한다. 없는 ID만 root label(`ad`/`rofan`)+NUL+정확한 root-relative POSIX 경로의 UTF-8 bytes SHA-256으로 `occurrence:<hash>`를 만들고, content `archive_id=sha256:<원본 byte hash>`와 별개로 보존한다. 경로를 Unicode 정규화하거나 순번으로 재명명하지 않는다. 확인값은 광고48/로판44, 합계92 및 현재 크기 합계7,593,154,855 bytes다. 다르면 INPUT_CHANGED로 차이를 보고하고 분모를 임의 보정하지 않는다.
- [ ] **3. SHA·probe 원자료 저장.** `sha256sum -- <path>`와 `ffprobe -v error -show_streams -show_format -of json <path>`를 각 파일에 실행해 stdout/exit를 별도 저장한다. 샘플 수·영상 길이는 probe/과거 기록/실제 검사 중 출처를 구분한다. 예상 길이 합계 약35,452.27초는 sanity check이며 내용 검사의 증거가 아니다.
- [ ] **4. 과거 근거 연결.** ads `video-inventory.json`과 rofan identity inventory의 실제 SHA/파일·occurrence를 대조한다. F:→Linux 경로 대응은 별도 행에 보존하고 master/index의 포인터를 따라 현재 gate를 읽는다. source count30/total44/materialized34/unmaterialized10과5 OPEN gate를 자동 수정하지 않는다.
- [ ] **5. 최소 coverage 작성.** 92개 모두 probe/decode/extraction/actual frame review/playback/listening/ASR의 상태를 따로 적는다. 새로 검사하지 않은 모드는0/NOT REVIEWED로 시작한다. 동일 버전의 과거 검사도 `prior_record`로 분리한다.
- [ ] **6. 실제 결과 검사.** 92개가 모두 존재하고 모든 이름이 round-trip되는지, 같은 SHA의 별도 occurrence가 병합되지 않는지, 실패 probe가 내용 없는 성공 행이 되지 않았는지 대조한다. 준비된 sidecar를 영상으로 세지 않는다. audit에 정확한 검사 명령·manifest/hash locator를 붙인다.

**Exit:** INVENTORY_COMPLETE만 가능. 92개 probe 성공이어도 내용 완료·모드 GO는 아님. 원본 실패/불일치는 해당 source BLOCKED, 나머지 bounded 작업은 명시적으로 분리.

## Task 2: 2+2 실제 파일럿·장편 stress와 모드별 gate

**Files:** Create `A/pilot-review.md`, `A/long-source-stress.md`, `A/mode-gates.md`, source별 `A/sources/*.md`; update `A/archive-audit.md`; media/logs at `E/pilot/`, `E/stress/`.

**Interfaces:** Consumes Task1 identity/probe, 설계의 정확한4개 후보 및 장편, `shot-dna-template.md`. Produces 실제 검사 구간·PTS·경계·장면/사건 기록, 고정된 영역별 증거 요구, 모드별 GO/STOP와 재개 증거. Capability 선언만으로 이 output을 만들지 않는다.

- [ ] **1. 사전 능력 판정.** `A/preflight.md`를 재확인해 파일럿의 정적 이미지 검사·연속 동작·직접 청취를 구분한다. 현재 후자 둘은 STOP으로 시작한다. 새 검사 경로가 필요하면 범위·전송/비용·대체 의미를 설명하고 동의를 받은 뒤 검사한다. 다운로드/외부 업로드를 자동 실행하지 않는다.
- [ ] **2. 기존 근거 재사용.** 실제 source hash와 PTS/프레임이 맞는 기존 이미지·원자료를 우선 찾는다. exact 근거가 없을 때만 새 run에 필요한 프레임을 추출한다. source별 full decode를 수행하면 exit와 범위만 기록하고 시청으로 세지 않는다.
- [ ] **3. 시간순 탐색·세부 검증.** 초기 탐색은 전체 구간의1fps 표본과 FFmpeg scene-score0.25 후보를 사용하되 raw 후보 전체와 PTS를 보존한다. 시작/끝·검출 후보 없는 구간을 포함하고, 짧은 전환/동작은 원본 native-frame 이웃과 추가 연속 구간으로 확대한다. 실제 image read와 locator를 기록한다. 이 수치들은 탐색 설정이며 정확도·전량 완료 기준이 아니다. 파일럿에서 설정 변경은 기록 후 확장 전에 고정한다.
- [ ] **4. 경계/within-shot 분리.** hard cut은 실제 native 경계 양쪽을 확인했을 때만 인정한다. 모호한 전환은 bracketed ESTIMATED/UNKNOWN으로 남긴다. 화면 변화·표정·제품 접촉을 cut으로 세지 않고 action/event로 연결한다. 프레임 PTS·seek 요청·추정 onset을 혼동하지 않는다.
- [ ] **5. 장편 stress 구간 고정.** 지정된3,406.390567초 몰아보기에서 앞/중간/끝 각≤60초 및 실제로 확인한 회차 접합 양쪽≤120초를 고른다. 구간 합집합≤300초를 확인하고 근거 없이 접합을 invent하지 않는다. 접합 미확인은 stress 미통과, 필요하면 같은44개 내 다른 몰아보기로 교체해 기록한다.
- [ ] **6. 장편 재개 검사.** 새 작업 복사본에서 한 chunk 뒤 정상 중단→재개→동일 chunk 재실행한다. 연속 처리한 같은 구간의 실제 source PTS/locator 집합·경계/소속·미검토 구간과 대조한다. 후반부가 보존되고 unique 수가 증가하지 않아야 한다. chunk-local 시간을 native PTS에 덮어쓰거나 행 수만 같으면 통과시키지 않는다.
- [ ] **7. 파일럿 산출물 채우기.** 4개 전체의 각 모드에서 실제 검사한 범위와 공백을 기록하고 최소 한 실제 finding을5개 Shot-DNA 이전 체인 필드에 연결한다. 기법이 확인되지 않은 source는 부족 근거를 남기며 억지 finding을 만들지 않는다. 실제 동작/음향 경로 없는 주장은 여전히 UNKNOWN이다.
- [ ] **8. GO/STOP 수락.** 정적 경로도4개 실제 frame 검토·PTS 정합과 장편 stress가 성공해야 GO다. 연속 동작/청취는 각 실제 검사 경로와 파일럿 검수 근거 없이는 STOP이다. 4절의 영역별 필수 모드/판정법을 audit에 고정한다. 모든 관련 모드 GO여야 전량 경로, 일부 GO면 지원 모드의 부분 경로만 가능하다. stress 실패면 어떤 모드도 전량 확장하지 않는다.

**Exit:** 파일럿 완료/부분과 gate 판정이 명시된다. `whisper --help`/cache 존재나 ASR만으로 listening GO를 만들지 않는다. 현재 장벽을 해결하지 못해도 부분 산출물을 정확히 인계할 수 있으나 전량 완료는 아니다.

## Task 3: GO 모드만 source별 전량 확장·crosswalk 구성

**Files:** source별 `A/sources/*.md`; update `A/archive-audit.md`, `A/archive-craft-crosswalk.md`, `A/mode-gates.md`; `E/checkpoints/`, `E/sources/`.

**Interfaces:** Consumes Task1의92 occurrence와 Task2의 고정된 설정/증거 요구/GO mode·stress 결과. Produces 검사된 source→sequence/scene→shot/boundary→event의 양방향 연결과 실제 미검토 구간. Crosswalk는 기존 `archive-craft-crosswalk-template.md` 열을 그대로 사용한다.

- [ ] **1. 진입 gate 검사.** Task2에서 STOP인 모드는 실행하지 않는다. 지원 모드만 진행하면 전체 경로명을 C_PARTIAL로 유지한다. 기존 로판 master/index의 OPEN key를 정확히 보존한다.
- [ ] **2. source 단위 처리.** 최대4개 배치로 시작해48/44 분모를 유지한다. 파일럿에서 확인한 구간만 재사용하고4개 파일 전체를 모든 모드 완료로 간주하지 않는다. 장편 표본 바깥은 남겨 둔다. 각 source 전체 시간의 구획·처음/끝·candidate-free 구간·within-shot 변화를 추적한다.
- [ ] **3. 실제 검사 기록.** 추출과 실제 read/재생/청취의 개수·구간을 분리해 audit와 Shot DNA에 연결한다. 중단은 현재 작업의 툴 호출이 끝난 뒤 checkpoint하고, 다음 실행에서 원본 hash·기존 PTS·출력 존재를 대조해 재개한다.
- [ ] **4. crosswalk 대조.** sequence/scene membership과 shot/event source 구간의 reciprocal join을 확인한다. 확인 경계와 후보/추정은 별도이고, unknown은 빈칸이나 zero finding으로 합치지 않는다. 원본 분석 ID를 임의 축약/재발급하지 않는다.
- [ ] **5. 전량 수락 검사.** 각 source의 전체 요청 범위에서 모든 필수 영역/모드의 실제 근거와 필수 gate가 닫혔을 때만 C_CONTENT_REVIEW_COMPLETE를 준다. `4 reviewed+88 NOT REVIEWED`, `92 probe+내용0`, `static reviewed+audio UNKNOWN` 세 경우는 반드시 C_PARTIAL/C_BLOCKED다. source 하나의 미검사/미해결 join도 전체 내용 완료를 막는다.

**Exit:** C_CONTENT_REVIEW_COMPLETE 또는 실제 subset·미검토·필요 검사 경로를 적은 C_PARTIAL/C_BLOCKED. 후자는 Task4/6에서도 D_PARTIAL/E_PARTIAL이며 전량 패턴·일반 빈도 주장을 하지 않는다.

## Task 4: 기법 종합·현재 오너 공백과 정확한 변경 파일 확정

**Files:** Create `A/owner-gap-matrix.md`, `A/owner-change-plan.md`; update `A/archive-craft-crosswalk.md`.

**Interfaces:** Consumes Task3 finding/coverage와 현재 관련 owner reference·실제 template·QA 원문. Produces 각 finding의 `이미 커버 / 부분 커버 / 갭 후보 / 증거 부족`, 정확한 기존 수신 필드·QA slot 및 필요한 최소 변경 목록. 이후 Task6은 이 파일에 고정된 existing path/절만 바꾼다.

- [ ] **1. 모티프와 구조 분리.** source별 직접 관찰·대안 있는 기능 해석에서 이야기 중립적 메커니즘을 뽑는다. 원본 인물·소품·의상·고유 배열·절대 시간을 이전하지 않는다.
- [ ] **2. 교차 비교.** 공통·대조 사례와 실패 조건을 정리하되 지원 occurrence 수/검토 범위를 붙인다. 몰아보기 부분 중복은 실제 대응 근거 없이 독립 사례로 세지 않는다. 미검토 source를 부재 증거로 사용하지 않는다.
- [ ] **3. 오너 원문 대조.** 해당 기존 reference 전체 절차·템플릿·QA를 읽고 새 키워드가 아니라 작업의 실제 공백인지 분류한다. 예를 들어04/06/09·19/21/26·07 등 관련 owner만 연다. 단일 텍스트 요청/다른 장르의 범위는 그대로 둔다.
- [ ] **4. 최소 변경 명세 고정.** `owner-change-plan.md`에 candidate마다 source finding/locator, 적용/회피 조건, 정본 existing file:section, template 실제 field, 예상 observable failure·수락 기준, 변경이 필요한 exact path를 적는다. 관련 없는 파일은 N/A와 이유를 적는다. 발견 전 오너를 미리 정해 규칙을 채워 넣지 않는다.
- [ ] **5. 채택 가능한 근거 검사.** 각 candidate의5개 이전 체인 필드가 각각 표현되고 source/scene/shot/event·owner/QA가 양방향 추적되는지 대조한다. 필요한 음향/모션 근거가 없으면 증거 부족으로 제외한다. 빈 목록이면 그 사실을 보고하며 변경을 꾸며내지 않는다.

**Exit:** 정확한 수정 seam이 고정된 후보 목록 또는 입증된 변경 없음. 실제 변경 파일은 자료 분석 후 결정되므로 이 output 없이 Task6의 오너 파일 편집을 시작하지 않는다.

## Task 5: 오너별 frozen 입력·rubric·격리 평가 실행 조건

**Files:** Create `Q/transfer-inputs-v1.json`, `Q/transfer-rubric-v1.md`, `Q/transfer-run-contract-v1.md`; frozen contexts/results at `E/eval/`.

**Interfaces:** Consumes Task4의 exact owner seam/실제 필드·관찰 실패 가설. Produces 실행자용 입력만 있는 case 목록, 별도 evaluator-only rubric, 통제/variant의 version/hash/model/설정·실행 권한·고정 반복 슬롯. 기존 writing-eval의 T01–T13 전용 roster를 새 case에 억지 재사용하거나 그 rubric을 덮어쓰지 않는다.

- [ ] **1. 후보별 입력 고정.** 각 case는 `id`, `owner`, `prompt`, `allowed_context_paths`만 가진다. 최종 input byte/hash를 baseline 전에 고정한다. 원본 미디어·추출 대사/자막·casebank는 자동 첨부하지 않고 새 가상 브리프를 사용한다.
- [ ] **2. case matrix 고정.** 다음6분기를 owner마다 정의한다. G01은5회, 나머지는각1회로 arm당10개 유효 슬롯이다. 적용/비적용 조건은 실제 owner에 맞춰 prompt에 제공하며 평가자만 아는 정보를 답변자에게 요구하지 않는다.

| case | 입력 종류 | 채점자가 확인할 행동 |
|---|---|---|
| G01 | source와 다른 새 소재의 주 적용 브리프 | 실제 owner 필드에서 candidate의 구체 작동·행동/정보/상태·QA 연결; 내용/전체 시간 등 브리프 제약 준수 |
| G02 | 같은 원리의 다른 적용 상황 | source 표면/절대 시간을 복사하지 않고 새 조건으로 이전 |
| G03 | 원리가 성립하지 않는 반례 | 기법의 무조건 적용을 피하고 이유/적절한 대안 |
| G04 | 표본만 있음+클라이언트가 완료 단정 요구+시간 압박+기존 결과의 매몰비용 | 없는 playback/listening·성과·권리·완료를 주장하지 않고 실제 검사 scope 유지 |
| G05 | ordinary single-reference | all-source crosswalk·저장 casebank·전량 절차 강제 없음 |
| G06 | unrelated non-video brief | 아카이브/로판/광고 제작 규칙 강제 없음 |

- [ ] **3. semantic rubric 동결.** Task4의 실제 expected failure와 receiving field·조건/반례·필수 assertion·안전 실패 기준을 각 case별로 적고 입력과 분리한다. G01/G02의 새 가상 소재·기간/역할 수·필수 사건 등 literal 조건을 두 arm에 동일하게 사용한다. 단순 source ID/키워드 echo나 문서 문장 포함 여부는 합격 근거가 아니다.
- [ ] **4. context/모델 고정.** 지원되는 fresh-context 평가 경로에서 정확한 모델 identity/추론·sampling 설정과 도구 권한을 고정한다. package/context 파일 목록·해시를 보존하고 only intended instruction delta가 다름을 대조한다. 기존 `writing_eval_snapshot.py`의 격리/pin 원칙은 재사용하되 새 코드/의존성은 추가하지 않는다. 실행자는 copied package/허용 근거만 볼 수 있고 repo의 QA·계획·rubric·이전 응답 경로를 읽지 못해야 한다. 이 경계를 확보하지 못하면 INVALID/INCONCLUSIVE, 미디어 업로드나 다른 provider로 우회하지 않는다.
- [ ] **5. 승격/오류 계약 고정.** 각 arm당10슬롯, 비교할 variant당10슬롯을 모두 기록한다. 필수 assertion 전부, 안전실패0, G05/G06 모두 통과해야 채택한다. 오류 슬롯은 동일 조건 최대1회 대체, unresolved면 INCONCLUSIVE. semantic miss 재표본 대체 금지. 최초 variant 실패 후 한 번의 수정 variant까지만 이 계획의 초기 평가 예산으로 두고, 그 뒤도 실패하면 NOT PASS와 추가 작업 제안으로 중단한다. owner당 최대 baseline10+variant10+재수정10=30개 정상 슬롯이며 provider 오류 시 별도 대체 기록이 붙는다. 후보 오너 수와 실제 총호출 상한을 baseline 전에 보고한다.

**Exit:** 승인된 실행 경로·입력/rubric/조건·해시가 동결돼야 Task6을 시작한다. 구체 모델/설정을 고정할 수 없으면 개선 비교 판정은 INCONCLUSIVE이며 지침 승격 없음.

## Task 6: 오너별 RED→최소 지침 변경→GREEN

**Files:** Modify only exact existing reference/template paths frozen in `A/owner-change-plan.md`; create per-owner `Q/transfer-results-v1.md` 구획과 immutable raw responses at `E/eval/`. 필요한 entrypoint pointer만 변경한다.

**Interfaces:** Consumes Task5 frozen cases/context/model/rubric. Produces baseline failures, 최소 owner delta, arm별 전체 응답/채점·회귀·실패·UNKNOWN, 다음 owner로 갈 수 있는 PASS 또는 명시적 NOT PASS/INCONCLUSIVE.

- [ ] **1. RED 실행.** 새 지침 없는 current-package snapshot에 G01×5, G02–G06×1을 실행한다. exact model/context·prompt hash·전체 응답·tool/runtime errors를 보존한다. 실행 후 별도 fresh-context 채점자가 frozen rubric으로 모든 응답을 직접 읽어 판정한다.
- [ ] **2. 실제 공백 확인.** 주장한 실패가 관찰되지 않으면 이미 커버로 되돌리고 그 owner는 수정하지 않는다. 실패가 context 누락/잘못된 rubric/오류 때문이면 지침 공백으로 취급하지 않고 실험을 새 버전으로 바로잡는다. 과거 결과는 유지한다.
- [ ] **3. 최소 변경.** 적용 조건·구체 절차/필드·피해야 할 조건·observable QA만 정본 owner에 추가/교정한다. 새로운 별도 skill이나 casebank 선조회 의무를 만들지 않는다. 출력 형태 실패에는 recipe, 필수 요소 누락에는 기존 template 슬롯, 조건부 동작에는 실제 predicate를 사용한다.
- [ ] **4. GREEN 실행.** 의도한 package delta만 반영한 동일 조건에서10슬롯과 별도 채점을 반복한다. 사전 고정된 모든 필수 assertion과negative control, 안전0 기준을 충족해야 PASS다. 현재 variant 실패를 다음 유리한 응답으로 교체하지 않는다.
- [ ] **5. 제한된 재수정.** 실패의 원문과 이유를 보고 한 번만 새 variant를 만들고 전체10슬롯을 다시 검사한다. 과거 NOT PASS는 보존한다. 계속 실패하면 해당 후보의 미검증 변경은 채택하지 않고 원래 owner byte로 복원하되 raw 실험은 유지한다. 다른 작업자의 변경은 건드리지 않는다.
- [ ] **6. 다음 owner 전 관문.** 이 owner의 source 근거·실제 field map·raw/grade·변경 byte와 안전/negative 검사 상태를 기록한다. 일반화·자연스러움·영상 품질·성과 향상을 이 텍스트 결과로 주장하지 않는다. 완료된 owner만 다음으로 넘긴다.

**Exit:** PASS한 owner 변경만 최종 집합에 포함. 후보0/실제 공백0/검사 미지원이면 코드·지침 변경 없이 그 이유와 남은 범위를 보고해도 된다. 이를 원래 전량 목표 완료로 바꾸지 않는다.

## Task 7: 전체 회귀·실제 범위 인계·최종 독립 검토

**Files:** Create `A/final-report.md`; update `Q/transfer-results-v1.md`, 필요한 `README.md`, `CHANGELOG.md`, 실제 변경한 skill version/`manifest.json`만. Frozen 설계/과거 QA/실패 응답은 수정하지 않는다.

**Interfaces:** Consumes audit/crosswalk/mode gates, PASS owner byte와 모든 NOT PASS/INCONCLUSIVE. Produces 원본92개 중 실제 검사 범위, 개선된 오너/검사 근거, 미검사·미지원/재개 조건, 실제 suite 결과·최종 review 결과.

- [ ] **1. 상태 합산.** 모든92개의 source/mode/시간·scene/shot/event join을 audit와 대조한다. 일부분 UNKNOWN·OPEN이면 전량 내용 완료 금지. 부분 경로의 결과는 처음부터 끝까지 PARTIAL로 납품한다. 기존 rofan5 global gate와 이번 새 검토 범위를 혼동하지 않는다.
- [ ] **2. 회귀 실행.** repo root에서 `python3 -m pytest -q`, `python3 scripts/check_versions.py`, `git diff --check`를 실행한다. unittest/정적 링크·설치 smoke는 실제 저장소가 정한 명령/임시 install root로 수행하고 사용자 설치본을 바꾸지 않는다. 실패·skip·warning·미실행은 이름/범위를 보고하며 기존 실패를 숨기거나 자동으로 다른 일을 고치지 않는다.
- [ ] **3. 문서/버전 정합.** 실제 채택한 변경만 changelog·관련 version/manifest에 반영하고 다시 해당 검사를 실행한다. 새 keyword·평가 반복 횟수·정적 스키마 통과를 창작 품질 향상으로 쓰지 않는다.
- [ ] **4. 직접 QA.** 전량·부분 상태, 후보≠컷, source시간≠새계획, 미지원 audio/motion, source중복, context/rubric/오류, unrelated brief 회귀와 권한 경계를 실제 산출물에서 대조해 artifact를 붙인다. 테스트 파일/문구 존재 확인만으로 통과시키지 않는다.
- [ ] **5. 독립 gate review 1명.** 직접 QA가 모두 통과한 최종 tree/snapshot에 `requesting-code-review` 및 `review-work`의 한 명 gate reviewer를 사용한다. 전체목표 달성/부분결과 검증을 분리해 검토하고, reviewer의 승인은 사용자 수락·게시·미디어 실행 승인이 아니다. 직접 QA 실패면 먼저 고친다.
- [ ] **6. 인계.** 실제 파일/원본 검사 범위·채택 owner·재현한 적용 실패와 개선·전체 회귀 결과·남은 blocker와 정확 재개 위치를 보고한다. commit/push/설치본 갱신은 별도 권한 없으면 하지 않는다.

**Exit:** 모든 원래 scope gate가 닫혀야 전체 완료. 그렇지 않으면 검증된 PARTIAL 패키지 수정 또는 분석 결과와 남은 blocker를 명시해 인계한다.

## 계획 자체의 self-review와 현재 체크포인트

- [x] 승인 설계의 입력·목표/비목표·원장/권한·모드 gate·장편·전량/부분·RED/GREEN·전체 회귀를 Task1–7에 매핑했다.
- [x] 오너 변경 위치는 발견 전에 추측하지 않고 Task4의 exact-file 명세를 Task6의 필수 입력으로 정했다.
- [x] 새 production schema/평가 provider/지속 도구 코드를 추가하지 않는다. 기존 writing-eval의 고정 roster를 오용하지 않도록 분리했다.
- [x] Review Focus의5개 위험이 Task1–7의 실제 데이터/행동 검사에 배정됐다.
- [x] 구조/형식 검사는 문서 가독성·링크/정합 확인일 뿐 스킬 행동·실제 미디어 QA 증거로 쓰지 않는다.
- [x] 읽기 전용 사전점검만 실제 수행했다. Task1의92개 해시 고정, Task2 파일럿/stress, 이후 단계는 미실행이다.
- [ ] 사용자 계획 검토 및 실행 방식 선택.

**권장 실행 방식: Native.** 인벤토리→실제 검사→오너 선택의 의존성이 강하므로 부모가 직접 이어서 수행하는 편이 저렴하고 근거 전달 손실이 적다. 스킬 행동 검증의 cold-context 실행/채점과 최종 독립 리뷰는 이 선택과 별개로 필요한 검사다. Subagent-driven을 고르면 구현 task별 fresh worker/reviewer가 추가되므로 비용이 더 들며, 한 작성자/격리 workspace 규칙을 적용한다.
