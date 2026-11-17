# 단계별 스킬 로딩·포커스 조회 최적화 설계

상태: 사용자 상세 설계 승인 완료(2026-11-18, “승인할게 작업 진행해”). 구현 계획 작성 단계. 구현 방법·평가 호출 예산·Git/설치 실행 범위는 계획 인계에서 확정하며, 이 승인만으로 원격 푸시/배포를 실행하지 않는다.

## 1. 목적과 결정

사용자가 선택한 방식은 **단계별 로딩 + 포커스 조회**다. 기능과 제작 품질·연속성·승인·검수의 요구 수준을 낮추지 않고, 현재 작업에 불필요한 문서·데이터를 읽는 양을 줄인다.

근거: `docs/analysis/2026-11-18-skills-weight-audit/REPORT.md`, 기준 소스 `bd5fb689dced7d09d966bff8f1897c06bac6082f`.

- 관리 25개 SKILL 본문 합 61,031 reference tokens. 발견용 메타데이터와 작업당 읽기량은 별개다.
- 조명 계획 문서 프로필 22,538 tokens, 일반 텍스트 콘티 선언 파일 프로필 25,058 tokens.
- 합성 100샷 계획 뼈대에서 한 샷 포커스 조회도 전체 출력 45,039 tokens. 포커스 context는 3샷이나 최상위 전체 cuts/links/requirements가 유지된다.
- 수치는 `o200k_base`의 정규화 텍스트 기준이며 실제 모델 청구량·응답 시간이나 완성 제작 프로젝트의 성능을 뜻하지 않는다.

### 선택한 접근과 비교

| 방식 | 장단점 | 결정 |
|---|---|---|
| 1. 문서 문장만 축약 | 변경은 작지만 전체 JSON 출력·거대한 공통 계약은 그대로 | 단독 해법으로 사용하지 않음 |
| **2. 단계별 로딩 + 포커스 조회** | 기존 라우팅/검증기/원장은 유지하고 읽기 인터페이스를 개선 | **사용자 선택** |
| 3. 중앙 로딩 엔진 재구축 | 자동 조립 가능하지만 새로운 실행·설정 계층과 마이그레이션 부담 | 이번 범위에서 제외 |

이 문서의 구체적인 파일 분해, 호환 정책, 측정 목표는 감사 결과를 바탕으로 한 **설계 제안**이며, 사용자가 개별 구현 결정을 모두 승인했다고 기록하지 않는다.

## 2. 범위와 비목표

### 포함

1. manifest의 **25개 관리 스킬**을 대상으로 현행 필수/조건부 읽기 경로를 정리한다. 모든 스킬을 억지로 수정하지 않고, 동등한 기능을 더 작은 읽기 단위로 제공할 수 있는 곳을 변경한다.
2. 시퀀스 조회에 읽기 전용 포커스 뷰를 추가한다.
3. 공통 제작 계약과 스토리보드 계약을 단계별 정본으로 분해하고 기존 링크를 호환시킨다.
4. 무거운 진입점의 현재 실행 규칙과 역사적/선택적 예제를 분리한다.
5. 대체 이미지 실행자 전제, text-only/no-save 용어, 조건부 appearance 읽기의 정합성을 바로잡는다.
6. 실제 읽기량·출력량·도구 호출과 계약 준수를 함께 비교하는 검증 기준을 둔다.

### 제외

- manifest 비목록인 brandkit/marketplace-cards/product-photoshoot/websites **4개는 후속 별도 범위**다. 기존 링크를 삭제하거나 비디오팩에 편입하지 않는다.
- 새 스케줄러, 중앙 로딩 엔진, project.json 대체 DB, 승인 원장, 자동 에이전트 팬아웃을 만들지 않는다.
- 실제 공급자 생성·업로드·비용 지출·모델 변경·외부 게시·사용자 미디어 수정은 하지 않는다.
- MBTI/Enneagram 기본값, 실제 7뷰 Sheet A, 보드 필수 슬롯, 원본/파생 계보, 이미지 전수 QA, PDF 납품 요구를 성능 핑계로 삭제하지 않는다.
- 이번 최적화에 FFprobe/해시 캐시를 넣지 않는다. 측정과 실패·변경 탐지 의미를 별도 설계해야 하므로 후속으로 미룬다.
- 기존 미커밋 `scripts/routing_eval.py`, `scripts/test_routing_eval_harness.py`와 무관한 분석 자료는 보존한다. 새 측정을 위해 이 두 파일의 미완성 변경을 무단 채택하지 않는다.

## 3. 보존해야 할 불변 조건

| 영역 | 최적화 후에도 반드시 유지 |
|---|---|
| 작업 범위 | 요청된 산출물·패널 수·언어·제외 조건 유지. 일반 콘티를 러프 콘티로 몰래 낮추지 않음 |
| 상태/버전 | 기존 ID·schema_version·artifact/asset 버전·dependency_versions·stale 전파 의미 유지 |
| 연속성 | 실제 채택 source in/out와 out−1, 선행 컷·비인접 재등장 이력·소품/손/위치/음성 상태를 유지 |
| 생성 입력 | 필요한 native selected references·역할·실제 제출문·실제 호출 대조 유지. 문서에만 있는 참조는 불충분 |
| 차단 | 필수 missing/unverified·미지원 transport·현재 입력 불일치·미승인 실행을 허용으로 바꾸지 않음 |
| 권한 | 콘텐츠 수락·검토 준비·실행/비용·공개를 분리하고 이미 승인된 범위는 재질문하지 않음 |
| 매체 | no_dialogue/no_audio/화면 글자 금지를 분리. 무음에 음향을 새로 추가하지 않음 |
| 증거 | 구조/파일/해시/조회 성공은 실제 시각·청취·품질·동의·사용자 수락 증거가 아님 |
| 저장 | 기존 project.json 단일 기록자와 .history 감사 유지. 조회/라우팅은 저장·초기화를 일으키지 않음 |
| 경합/무결성 | 덮어쓰기·stale write·루트 이탈 거부 및 실제 호출 직전 확인을 약화하지 않음 |

## 4. 읽기 전용 포커스 뷰

### 4.1 인터페이스와 호환

기존 `build_sequence_context(project, shot_ids, projection=None)`의 전체 `sequence-execution/1` 반환과 기존 CLI 기본 동작은 유지한다. 기존 full projection을 사용하는 prepare/validate/inspect/render는 그대로 전체 입력을 소비한다.

새 인터페이스:

- `sequence_view.build_sequence_focus_view(project, shot_ids, projection=None) -> Document`: 순수 읽기·파생 조회. 파일 저장/해시 검수/생성/승인 추론 없이 현재 문맥을 고른다.
- `sequence_context.py ... --view full|focus`: **기본값 full**로 호환 유지. 새 에이전트 지침에서는 포커스 읽기에 명시적으로 `--view focus`를 쓴다.
- `--view focus`는 하나 이상의 `--shot`을 요구한다. `--all --view focus` 조합은 오류로 거부한다. 전체 열람은 기존 `--all --view full`을 쓴다.
- 새 뷰 형식은 `sequence-focus-view/1`, `read_only: true`, `executable: false`, `validation: not_run`이다. 실행 투영·정본 프로젝트가 아닌 **표시용 형식**이다.
- `read_projection`은 새 표시용 형식을 거부한다. prepare_generation_request/validate_sequence/render/inspection에 잘못 넘겨도 실행되거나 ready가 되지 않아야 한다.

새 조회 예:

```bash
# 전체 실행 투영은 기존 파일에 그대로 둔다.
python3 scripts/sequence_context.py <root>/project.json \
  --shot SH42 --projection <root>/source/sequence-v01.json --view focus

# 실행 준비와 검증은 원래의 전체 파일로 수행한다.
python3 scripts/prepare_generation_request.py \
  <root>/project.json <root>/source/sequence-v01.json
```

단계별 문서에는 첫 bootstrap에서 full 투영을 파일로 만드는 명령과 이후 포커스 읽기 명령을 구분해 적는다. 표시용 뷰를 full 파일 위로 리다이렉트하지 않도록 예제 파일명/형식을 분명히 한다. 출력 경로 옵션을 새로 만들 필요는 없고 조회 CLI는 기본 stdout 읽기만 수행한다.

### 4.2 포함 집합

선택 대상은 임의 토큰 상한이 아니라 **현재 컷과 실제 참조 의존성**으로 정한다.

1. 요청한 focus shot에 속한 모든 cut을 포함한다. 같은 shot이 여러 cut에 나타나면 하나만 고르지 않는다.
2. 각 focus cut의 실제 편집상 선행 cut과 후행 cut을 포함한다. 시작/끝에는 존재하는 쪽만 포함한다.
3. focus로 들어오는 link의 `history_shot_ids`를 모두 해석하고, 해당 shot의 모든 관련 cut과 선택된 소스 상태를 포함한다. 기존 `predecessor_cuts`의 이력 해석/거부 의미와 맞춘다. 서사 시간선과 편집 이웃을 같다고 추정하지 않는다.
4. 이력으로 포함한 항목에 별도의 명시적 상태 의존 이력이 연결되어 있으면 그 명시적 연결을 닫을 때까지 포함한다. 방문 집합으로 반복을 끝내고, 알 수 없는 ID·연결 불일치는 조용히 생략하지 않고 오류 또는 조회 이슈로 반환한다. **단순히 앞 컷이라는 이유만으로 첫 컷까지 계속 확장하지 않는다.**
5. 각 포함 항목의 선택 이유를 `focus | predecessor | successor | history | referenced_dependency`로 표시한다. 오래전 이력이 많으면 뷰도 커질 수 있다. 필요한 이력을 자르는 토큰 상한은 두지 않는다.
6. 프로젝트의 임의 전체 registry 대신 위 항목에서 소비하는 입력을 닫는다: 캐릭터/장소/소품/LOOK, 관련 패널/비트, 명시적 source/derivative/master 계보와 버전 핀, 해당 voice profile/anchor, 현재 실행 인계가 요구하는 입력·증거 locator.

이는 기존 ID/계보 의미와 `predecessor_cuts`의 해석을 재사용하는 작은 조회 모듈이다. 새 스케줄러나 창작 의미 추론기는 아니다. 다만 **`project_index.build_index`의 출력 전체를 그대로 넣는 구현은 사용하지 않는다.** 그 함수는 storyboard 소유 artifact를 만나면 정당하게 전체 panel/asset 커버리지로 확장하므로, 표시 최적화와 목적이 다르다. 기존 project_index/validator의 그 동작은 변경하지 않고 새 뷰에서 별도로 표시 범위를 고른다.

프로젝트 전체 보드/실행 계획처럼 전역 범위인 artifact는 ID/type/version/status 및 원본 locator·스냅샷 식별자로 표시한다. 전역 artifact를 참조했다는 이유만으로 그 모든 패널·자산·required_asset_versions/dependency_versions 전체 맵을 다시 펼치지 않는다. 현재 컷/선행/선언 이력/실제 handoff가 소비하는 레코드와 핀만 상세 표시하고, 생략한 전역 맵은 원래 전체 파일에 유지한다. 이는 실행 검사 축소가 아니라 표시 축소다. 실제로 범위가 넓은 명시적 handoff 참조는 필요한 만큼 포함하며, 이 경우 뷰가 커지는 것을 숨기지 않는다.

### 4.3 출력 구조와 누락 처리

표시용 뷰에는 다음만 넣는다.

| 필드 | 내용 |
|---|---|
| source | project ID/version, 입력 projection의 owner/version, origin=provided 또는 bootstrap. CLI에서 읽은 파일 경로/스냅샷 식별자 |
| focus | 요청 shot/cut ID, 포함 ID와 선택 이유 |
| time_basis | 해석에 필요한 FPS·프레임 기준 |
| context | 포함 대상의 정본 샷·패널·인물·asset/artifact 레코드와 필요한 계보 |
| cuts | 포함한 cut의 실제/계획 source 선택, in/out, FPS/count, 상태. 없는 실제 결과는 null/planned 그대로 |
| links | focus 경계 및 포함된 명시적 이력의 상태 인계/허용 변화와 locator |
| requirements | focus 산출물의 요구 행. 이웃/이력은 상태·의존성 정보를 주되 무관한 전체 대본을 복제하지 않음 |
| checks | 포함 대상/참조를 직접 검사한 관련 기록, scope 검사 결과의 locator와 선언된 범위. 전역 PASS를 현재 컷의 검사로 재해석하지 않음 |
| inputs | 실제 이 뷰에서 참조하는 artifact/asset 핀. 전체 실행 투영의 핀은 원래 파일에 그대로 남음 |
| handoff | **현재 요청에 해당할 때만** binding의 source/voice/composition ID·역할·imports/excludes·실제 request_clause와 원본 submission locator. 원본 native request와 reference 목록은 수정하지 않음 |
| issues | 명시적 source 불일치·stale pin·알 수 없는 연결 등 조회에서 확인한 문제. 실제 validator의 대체 판정이 아님 |
| omissions | 전체/표시/제외 개수, 전체 투영 locator와 추가 조회 방법. 제외된 모든 ID를 나열해 다시 O(N) 출력하지 않음 |
| limits | 표시용·실행 금지·검증 미수행. source 식별자가 품질/관측 진위를 인증하지 않음 |

전체 native request JSON과 세션/업로드 snapshot 원문은 대량 재출력하지 않고 등록된 locator/핀으로 연결한다. 현재 binding의 보존/제외 지시는 의미를 임의 요약하거나 잘라내지 않는다. 원문이 필요하면 해당 등록 문서를 명시적으로 조회한다.

입력 projection의 focus가 다른 요청의 제출문/bindings를 가리키면 그 패킷을 현재 요청의 것으로 표시하지 않는다. `handoff_applicability: mismatch`와 원래 scope/locator를 남기고 현재 native handoff 준비가 안 됐다고 표시한다. 조회가 잘 됐다고 submission을 바꾸거나 재준비하지 않는다.

입력 소스 식별자는 조회에 실제 사용한 스냅샷을 가리킨다. CLI는 파일 경로와 해당 **같은 읽기 스냅샷**의 raw-byte digest를 제공한다. 순수 함수 호출에 파일 locator가 없으면 이를 null/unavailable로 표시하고 실제 파일 hash처럼 꾸미지 않는다. bootstrap은 `origin: bootstrap`, 저장 projection locator 없음으로 표시한다. source 식별자 자체는 새 실행 권한이 아니다.

**안전 실패 방향:** 알 수 없는 focus/잘못된 projection/필수 의존성 해석 오류는 구조화 오류로 거부한다. 정상적인 planned/null과 incomplete owner는 미완성 계획으로 보여 줄 수 있으나 준비 완료로 승격하지 않는다. 어떤 경우에도 실행자는 기존 전체 파일을 다시 읽고 현재 게이트를 통과해야 한다.

## 5. 문서 로딩 구조

### 5.1 정본 소유 원칙

- 규칙 본문은 한 정본에만 둔다. 진입점에는 발동 조건·정확한 경로·중요 차단 조건을 짧게 둔다.
- 단독 실행에서 꼭 알아야 할 연속성/권한 포인터는 각 실행 진입점에 남긴다. 문장 중복 제거를 이유로 단독 경로 안전장치를 없애지 않는다.
- 파일을 나눈 뒤 한 작업이 결국 전부 읽게 하면 실패다. 선택은 현재 산출물·단계·매체·저장/실행 범위로 결정한다.
- 기존 명시적 `routing.csv` 27 route ID, owner와 3축 판단, `routing-disambiguation.csv`의 필수 사용은 유지한다. 새 중앙 resolver를 만들지 않는다.
- `required_read`에는 지금 반드시 읽어야 하는 실제 파일 경로만 둔다. 조건식/모호한 설명문을 CSV 경로 칸에 넣지 않는다. 조건부 읽기는 소유 SKILL의 구체적인 분기표로 지정한다.

### 5.2 공통 제작 계약

| 파일 | 정본 책임 | 읽는 조건 |
|---|---|---|
| `references/contract-core.md` 신규 | ID/시간/상태의 기본 의미, standalone vs 프로젝트 ID, 최소 입력/반환, 단일 기록자 | 해당 전문 산출물의 기본 인계 |
| `references/contract-project.md` 신규 | project.json 필드, 버전/의존성·stale, index/update 사용법, 실행 승인·timing 메타데이터 | 기존 원장 등록/수정·스키마 작성·관련 오류 해결 |
| `references/contract-package.md` 신규 | 전체 image-backed 산출물, 캐릭터 Sheet A, LOOK·master/derivative·FINAL·panel pins | 실제 전체 이미지 패키지 및 해당 downstream FINAL |
| `references/contract-delivery.md` 신규 | 실제 납품 검사, ZIP/relocation/manifest·감사 사본 | 파일 패키징/납품 |
| `references/contract.md` 기존 | 이전 절 anchor와 새 정본으로 가는 호환 색인 | 오래된 링크 진입/전체 계약 탐색 |

기존 contract의 sequence timing/authority 정의는 project 문서로 옮기고, 실제 실행 절차는 기존 `sequence-execution.md`가 계속 소유한다. 새 의미의 상태/승인 스키마를 만들지 않는다.

`contract.md`의 기존 fragment는 explicit anchor로 보존한다. 각 절은 새 정확한 정본으로 연결하고 동일 규칙 본문은 중복 저장하지 않는다. 기존 클라이언트가 전체 계약을 요청했으면 색인의 전체 정본 목록을 따라 읽을 수 있다. 최적화된 경로는 필요한 새 파일을 직접 지정한다.

### 5.3 스토리보드 계약

| 파일 | 정본 책임 | 읽는 조건 |
|---|---|---|
| `storyboard-contract.md` 기존, 코어로 정리 | 6개 반환 구획, 모든 필수 샷/패널 슬롯, 범위/N/A/deferred/blocker, 커버리지·기본 연속성·수락, 단계별 읽기표 | 완전 제작용 보드; 러프/프롬프트-only의 기존 좁은 분기는 유지 |
| `storyboard-direction.md` 신규 | 씬 카메라 의도/이웃 비교, 리듬·감정·공간 가독성, 적용 가능한 staging·동작/상태 패널 설계 | 완전 보드의 실제 텍스트/연출 설계·수정·검토 |
| `storyboard-media.md` 신규 | 실제 이미지 생성/정본 입력·시트 조립/추출·등록·clean 이미지 전수 QA | 실제 이미지 보드 생성/시트·추출·검사 |
| `storyboard-delivery.md` 신규 | 이미지/텍스트 PDF, 도구·폰트·페이지/텍스트/시각 검수 | 파일 보드 납품/변환 |
| `storyboard-schema.md` 신규 | project.json 상세 보드/rhythm 스키마와 validator 매핑 | 스키마 작성/수정/해당 구조 오류 해결 |

기존 contract의 모든 fragment는 원위치에 유지된 코어 내용 또는 명시적 호환 anchor→새 소유 문서로 이어진다. 기존 field heading/enum/시간/패널 수/표현력의 적용성은 유지한다. 원전 근거는 기존 sources의 ID/locator로 연결하며 촬영 의무처럼 확장하지 않는다.

텍스트 콘티는 core+direction을 읽고 모든 필수 설계 슬롯을 채운다. 실제 PDF 도구/PNG metadata/분할 알고리즘/전체 JSON 작성법은 지금 그 실행/편집을 하지 않으면 미리 읽지 않는다. image-backed 전체 패키지는 해당 단계에 도달하면 package/media/schema 등 필요한 규격을 모두 적용한다.

### 5.4 무거운 진입점 정리

- `video-production-assets/SKILL.md`: 최소 실행 원칙 + 현재 모듈/단계 선택표 + 필수 안전 포인터만 남긴다. 전체 패키지 진행은 기존 `preproduction-review.md`/production-routing와 새 package 계약으로 이동한다. 심화 목록은 선택용 색인으로 분리할 수 있으나 조건별 정확한 조회 경로를 유지한다.
- `storyboarding-video`: 텍스트/이미지/파일 납품/스키마 단계를 읽기표로 연결한다. 일반 보드의 완전성 기본값은 그대로다.
- `designing-video-character-sheets`: compact/full SSOT와 persona 소비는 유지한다. R03의 appearance 표는 unconditional required_read에서 빼고, 실제 헤어/메이크업/의상 선택·변형 분기에서 필수로 연다. 새 캐릭터의 기존 typology/voice 계약을 바꾸지 않는다.
- `higgsfield-generate`, replicate, explainer: 적격성·현재 입력·타임아웃/재시도·연속성 필수 포인터는 본문에 둔다. 역사적 모델표/사용 금지 이미지 명령/상세 단계 예제는 기존 해당 references 또는 전용 실행 가이드로 이동한다. 현재 가용성·가격을 이 설계에서 새로 확정하지 않는다.
- Blender: 모드/CLI 세부를 기존 `blender-workflow.md`로 모은다. 실제 scene-specific geometry 검증 trigger와 inspection 의무는 코어에 남긴다.
- history: 시작/상태/재개/기록의 짧은 사용 인터페이스를 본문에, 전체 CLI·원자성/보안 상세를 `references/cli-contract.md`로 둔다. 상태 전이와 실제 output 존재 검사는 코드에서 유지한다.
- 나머지 스킬은 직접 이득이 확인될 때만 바꾼다. 25개를 모두 동일 분량으로 강제하지 않는다.

## 6. 정합성 수정

### 6.1 media_axis와 저장은 별개

`text_only`는 새 이미지/음성/영상 생성이 없다는 뜻으로 통일한다. `no-save`/`read-only`/`chat-only`는 별도 명시된 제약이며 서로 자동 추론하지 않는다.

- '채팅으로만 콘티': 파일/프로젝트 초기화/미디어 없음.
- '이미지 없이 콘티를 MD로 저장': 요청된 텍스트 파일과 기존 범위의 history 저장은 허용. 새 이미지/음성/영상은 금지.
- '텍스트 계획 후 나중에 렌더': 현재 렌더 승인 아님.
- 명시적 read-only/no-save와 파일 요청이 충돌하면 임의로 제약을 해제하지 않고 확인한다.

이는 새 root schema/권한 필드를 만들자는 제안이 아니라 기존 요청 범위를 읽는 용어 정리다. 첫 저장 위치 선택·기존 프로젝트 재사용·불필요한 초기화 금지·단일 기록자는 유지한다. 명시적으로 파일을 요청하지 않은 text_only 요청을 자동 저장하지 않는다.

### 6.2 선택된 실행자만 preflight

Codex Imagen 썸네일은 해당 실행자의 runtime/auth/입력/목적지/권리를 확인한다. 비사용 Higgsfield 인증/모델표/quote는 요구하지 않는다. Codex Imagen의 기존 usage/price/quota/quote 예외를 보존한다. 실제 Higgsfield 적격 작업과 그 spend gate는 그대로다. Higgsfield 이미지 금지와 private enhancer 동등성 주장 금지는 유지한다.

### 6.3 외부 의존성

`ai-delegation-loop`는 현재 네 설치 루트에서 찾지 못했지만 외부 의존성으로 선언돼 있다. 이번 최적화는 이를 임의 삭제/대체/자동 설치하지 않는다. 한 세션의 동일 소스 탐색 실패는 정확한 경로/범위와 함께 한 번 기록하고, 설치/설정이 바뀌기 전 반복 탐색하지 않는다. 의존 단계만 unresolved로 남기고 독립 작업은 계속한다. 누락 상태를 '이미 모두 최적화되어 무의존'으로 보고하지 않는다.

## 7. 읽기 재사용과 실제 관측

- 같은 세션에서 **실제로 열어 읽은** 동일 버전/hash 문서의 같은 적용 절은 다시 읽지 않아도 된다. 부모의 '읽었다'는 말, 파일이 있다는 사실, 평가 harness가 경로를 알려 준 사실은 소비 증거가 아니다.
- 새 워커/새 세션에는 이 읽기 상태를 자동 승계하지 않는다. 해당 단계의 필수 정본을 읽는다.
- 현재 입력/계정/모델/참조 역할/서버 revision이 바뀌면 실제 실행자 게이트대로 재검사한다. 영구 전역 capability 캐시는 만들지 않는다.
- 목록/로그/계약이 길다는 이유로 필수 원문·정확한 대사·상태·실제 참조 역할을 잘라내지 않는다. 무관한 내용과 locator로 충분한 대량 부록을 줄인다.

## 8. 검증과 수락 기준

### 8.1 고정 baseline과 변경 격리

구현 시작 시 clean committed baseline을 고정한다. 감사의 synthetic context/profiles와 문서 hash를 고정된 입력 자료로 보존한다. 미완성 routing_eval 변경과 artifact QA 자료를 평가기의 진실로 무단 채택하지 않는다.

기존 회귀는 유지하고 새 집중 테스트/측정을 별도 파일로 추가한다. 기존 `scripts/run_guide_behavior.py`의 관측 접근은 참조할 수 있지만 현재 dirty harness를 수정해야만 비교할 수 있는 설계는 피한다. 실제 LLM 호출/추가 에이전트 실행은 구현 단계의 명시된 실행 방식·권한 안에서만 수행한다.

### 8.2 포커스 뷰의 기능 시험

- 기존 default/full CLI와 Python 인터페이스 결과·full 파일은 변경 없음.
- focus는 원장/전체 projection/기존 파일을 수정하지 않는다. invalid focus/shape/`--all` 조합은 실패한다.
- 첫/마지막/복수 focus, 한 shot의 복수 cut, 인접 선행/후행, 인서트 뒤 재등장, cross-cut/flashback의 선언 이력, master→derivative/LOOK/voice anchor가 필요한 범위에 남는다.
- 알려진 이력 순환은 중복 없이 끝나며, self/unknown/충돌은 기존 거부 의미를 유지한다. 이력을 토큰 상한으로 자르지 않는다.
- 다른 focus의 handoff가 현재 패킷으로 오인되지 않는다. missing/stale/planned/null의 구별을 보존한다.
- 실제 image-backed fixture에서 전역 storyboard owner 또는 execution artifact가 dependency에 들어가도 무관한 전체 panel/asset 맵이 뷰로 다시 유입되지 않는다. 현재 소비 핀과 원본 전체 맵 locator는 유지한다.
- 새 표시 형식은 validate/prepare/render/inspect 경로에 실행 투영으로 수락되지 않는다.
- 전체 투영을 사용한 기존 missing-history/native ref/audio/어댑터/권한/파일 무결성 실패 사례가 계속 차단된다.

### 8.3 문서/행동 회귀

대표 요청은 로그라인, 단일 조명, compact 캐릭터·full SSOT, appearance-only, typology none/both, 일반/러프 콘티, 채팅-only/MD/PDF 저장, image-backed 전체, 수치 카메라/실제 Blender, 무음, 새 앵글 후속 생성, 인서트 뒤 재등장, 미지원 참조, 타임아웃 복구를 포함한다.

각 경우에 다음을 비교한다.

1. 요청 산출물/전체 슬롯·수량·잠근 원문·N/A/deferred/blocker의 일치.
2. 실제 도구 기록에서 필수 파일 소비 및 무관한 단계 읽기 유무. 파일 이름을 답한 것만으로 읽었다고 판정하지 않음.
3. 본문 축소 후 참조를 더 많이 열어 **총 읽기량이 증가하지 않는지**. 같은 데이터 중복 읽기도 포함한 returned-text tokens와 unique-read tokens를 구분한다.
4. 불필요한 인증·견적·프로젝트 생성·재질문·금지된 제출이 생기지 않는지.
5. 구조 테스트와 fresh-context 행동 확인을 별도로 보고. static 문자열 일치만으로 실제 준수를 인증하지 않음.

### 8.4 성능 예산

다음은 **설계 목표**이며 현재 달성 결과가 아니다. reference encoding, 고정 fixture와 측정 방식을 함께 기록한다.

| 대상 | 목표 |
|---|---|
| 100샷 합성 뼈대의 단일 focus 뷰 | 같은 기준 encoder에서 6,000 tokens 이하. 필요한 이력/참조 수가 같은 10→100샷의 unrelated 확장 시 출력 증가 256 tokens 이하 |
| 단일 조명 계획 문서 프로필 | 현재 22,538 대비 전체 선택 파일 합집합 35% 이상 감소 |
| 일반 텍스트 콘티 문서 프로필 | 현재 25,058 대비 25% 이상 감소, 모든 기존 필수 슬롯 유지 |
| 무거운 진입점 | assets/storyboard/generate 계열은 각각 약 1,800 tokens를 목표로 하되 안전·기능 시험이 우선 |
| 영향 없는 스킬/요청 | 불필요한 새 문서·전제·도구 호출을 추가하지 않음 |

문서 프로필 합계와 실제 작업 읽기량은 다른 지표다. 둘 다 기록한다. host tokenizer가 없으면 reference encoder라고 표기하고 실제 청구/속도 개선률로 확대하지 않는다. 예산을 맞추려면 필수 정보를 버려야 하는 경우 축약하지 않고 설계 재검토/목표 미달로 보고한다.

순수 함수/CLI 계약·기존 전체 suite·문서 경로/anchor 검사·대표 행동 회귀가 모두 통과해야 구현 완료다. 실제 공급자/미디어 품질 검증은 별도 허가 없이는 수행하지 않으며 미실시를 기록한다.

## 9. 변경 순서와 출시

구현 계획은 상세 설계 승인 후 별도로 만든다. 의존 순서는 다음과 같다.

1. baseline/대표 요청/파일 hash·read trace 측정과 불변 조건을 고정한다.
2. 포커스 표시 모듈+CLI를 추가하고 기존 full 소비자는 유지한다.
3. 공통 계약·스토리보드 계약의 정본 이동과 호환 anchor를 함께 바꾼다. dangling pointer 상태로 출시하지 않는다.
4. 라우팅 required_read/전문 진입점/예제를 새 단계별 경로로 동시에 연결하고 전제 충돌을 수정한다.
5. 전체 계약/행동/성능 비교 후 독립 최종 검토, 현재 원격·로컬 상태 확인, 명시적으로 승인된 Git/설치 절차를 수행한다.

특정 스킬의 소유권·형식이 바뀌지 않았으므로 기존 프로젝트 데이터 마이그레이션은 없다. 새 표시 뷰는 재생성 가능하고 canonical project/projection에 저장하지 않는다. 이후 롤백은 최적화 커밋과 문서 포인터를 함께 되돌리고 설치 링크/파일을 확인하는 방식이며 제작 데이터·원본 미디어를 되돌리지 않는다.

이 설계 승인 자체로 main push, 패키지 버전 변경, 다른 에이전트의 미커밋 작업 채택, 기존 설치 링크 변경이 허용되는 것은 아니다. 실제 구현/출시 단계에서 범위와 실행 방법을 확정한다.

## 10. 설계 상태

- [x] 사용자 방식 선택: 2번, 단계별 로딩 + 포커스 조회.
- [x] 감사 결과·기존 인터페이스/테스트/라우팅 소비자 대조.
- [x] 호환성·불변 조건·단계별 정본·성능/행동 수락 기준 작성.
- [x] 구현자 관점의 독립 설계 검토 및 필요한 보완.
- [x] 사용자 상세 설계 승인.
- [x] 승인 후 구현 계획 작성: `../plans/2026-11-18-staged-skill-loading-focus-view.md`. 현재 문서는 구현 작업표가 아니다.

### 검토 기록

- fresh-context 구현자 검토 1회: `openai-codex/gpt-6.1-sol`, run `0f7c5ca9-1ac4-41ee-ba59-bc9851d66959`.
- 설계와 실제 sequence_context/predecessor_cuts/project_index/routing.csv를 읽고 남은 중요한 구현 계획 질문을 검토했다. 반환: **`nothing important left`**. 파일 수정/명령/공급자 실행/하위 에이전트 호출은 없었다.
- 작성자 대조에서 `project_index`의 전역 storyboard 커버리지 확장이 새 표시 뷰로 다시 유입되지 않도록 §4.2와 §8.2에 명시했다. 기존 index/validator의 전역 검사 동작은 유지하는 구체화이며, 별도의 재검토나 성능 통과를 주장하지 않는다.
- 이 검토는 설계의 계획 가능성 점검이다. 구현 정확성·에이전트 실제 준수·토큰 목표 달성의 증거가 아니다.
