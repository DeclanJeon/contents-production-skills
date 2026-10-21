# Product Detail Page Builder — 통합 설계

## 상태와 목적

**상태:** 구현 초안 완료. specialist와 compositor/validator를 source package에 추가했다. 전역 사용자 스킬 설치나 실제 상품 이미지 생성은 수행하지 않았다.

**후속 설계:** 2026-10-19의 [module-first PDP 설계](2026-10-19-module-first-product-detail-page-design.md)가 SmartStore의 단일 긴 이미지 기본 export를 대체한다. 이 문서는 초기 v1 설계·구현 이력으로 유지하며, 현재 upload asset 계약은 후속 설계를 따른다.

**목표:** 기존 `contents-production-skills`에 상품 상세페이지 전용 specialist를 추가해, 확인된 상품 정보와 이미지에서 플랫폼에 맞는 상세페이지 모듈·문구·조판 파일을 만들고 실제 산출물을 검증한다. 외부 프로젝트의 코드를 한데 복사하는 방식이 아니라, 검토한 제작 원칙을 이 저장소의 경계와 도구 계약에 맞춰 독립적으로 구현한다.

**목표가 아닌 것:** 새 총괄 에이전트, 독립 제작 원장, 범용 자사몰·체크아웃 구현, 플랫폼 자동 게시, 미확인 효능·인증·치수 생성, 사용자 승인 없는 이미지 생성 또는 외부 전송.

## 구현 및 검증 기록 — 2026-10-18

- `product-detail-page-builder`를 manifest의 25번째 skill로 등록하고 `creative-production`의 단일 총괄 라우팅을 연결했다.
- page-spec, Korean platform profiles, fact/source validation, Pillow compositor, slicing, output validator, synthetic regression tests를 추가했다. Python modules are split by responsibility and remain under 250 pure LOC.
- 상세페이지 전용 테스트 8/8 통과. 모든 추적 테스트 파일과 새 상세페이지 테스트를 지정해 실행한 저장소 회귀는 267 passed, 13 skipped, 217 subtests passed.
- JSON parse, Python compile, package version check, sync dry-run 통과. 실제 출력 미리보기는 합성 fixture이며 판매 상품 출력이 아니다.
- 현재 checkout의 일반 `pytest -q`는 Git-ignore된 `video-production-assets/support/qa/...` 복사본과 추적 원본 테스트가 같은 모듈명이라 collection에서 실패한다. `--import-mode=importlib`는 기존 테스트의 스크립트 경로 import와 맞지 않았다. 추적 테스트를 빠뜨리지 않은 명시적 file-list 실행으로 회귀를 확인했다.
- `install_package.py`의 임시 설치 preflight는 현재 checkout에 이미 존재하는 Git-ignore `video-production-assets/support/{manifest.json,examples,qa,CHANGELOG.md}`와 source collision을 보고 쓰기 전에 중단했다. 해당 경로를 제거하거나 수정하지 않았다. CI의 깨끗한 checkout에서 실제 설치는 별도로 확인해야 한다.
- 실제 상품 사진이 없으므로 제품 정체성·실제 상품별 copy·판매 적합성은 검증하지 않았다. SmartStore seller-center 확인, Coupang 상세 이미지 폭/제한 확인, 실제 asset visual review도 업로드 전 남아 있다.

## 결정 요약

1. 별도 저장소나 중복 총괄을 만들지 않는다. 저장소 루트의 기존 skill 구조에 `product-detail-page-builder/` specialist를 추가하고, `creative-production`이 요청 범위에 따라 라우팅한다.
2. 기존 24개 스킬을 대체하거나 24개 모두와 억지로 결합하지 않는다. 상품 상세페이지에 유효한 사실 추적, 모듈 계획, 상품 정체성 보존, 결정론적 조판, 출력 QA만 가져온다.
3. MVP는 한국어 이미지형 상품 상세페이지다. 스마트스토어·쿠팡 규격은 구현 전에 각 플랫폼의 공식 판매자 문서와 판매자센터에서 확인한다. 검증되지 않은 값을 고정 사양으로 내장하지 않는다.
4. 이미지 생성, 텍스트 조판, 플랫폼별 export와 검증은 별도 경계로 둔다. 생성 모델은 문구·숫자·인증 표시를 그리지 않고, 코드는 승인된 문구를 정확히 합성한다.
5. 현재 저장소의 “재사용 라이선스 없음” 정책을 따른다. 기본값은 외부 코드·프롬프트·긴 문구를 복사하지 않는 것이다. 외부 구현을 vendoring하려면 해당 revision·라이선스·고지·대상 배포 조건을 별도로 검토한다.

## 저장소 기준선과 조사 근거

설계 착수 당시 지정 저장소의 `manifest.json`에는 24개 스킬이 있었고 `product-detail-page-builder` 경로는 없었다. 이 구현에서 신규 specialist를 등록해 목록은 25개가 됐다. 기존 `higgsfield-product-photoshoot` 등 이미지 제작 스킬은 상품 사실 추적과 플랫폼별 상세페이지 구성·출력 검증을 소유하지 않았다.

루트 `README.md`와 `integrations/package-provenance.md`는 이 저장소에 재사용 라이선스가 없으며, 공개 접근성이나 출처 표기만으로 재배포 권한이 생기지 않는다고 명시한다. 따라서 본 설계의 외부 저장소 검토는 기능·구조 분석이며, 코드나 창작 표현의 복사 허가가 아니다.

| 조사한 저장소 | 확인한 강점 | 재사용 경계 |
|---|---|---|
| [xianyu110/ecommerce-image-skills](https://github.com/xianyu110/ecommerce-image-skills) (`f4566fd`) | 작은 이미지 작업별 스킬, 상품 정체성 잠금, 플랫폼 사이즈 지침, 스티칭·크롭·검사 스크립트 | 확인한 checkout은 MIT. 원칙과 기능을 독립적으로 재작성한다. 코드 vendoring은 고지·revision 검토 후 별도 결정한다. |
| [Gayaya999/ecommerce-detail-page-generator](https://github.com/Gayaya999/ecommerce-detail-page-generator) (`2348487`) | user/visible/unconfirmed 사실 원장, 구조화된 page spec, 모듈별 텍스트 없는 이미지, Pillow 조판, manifest와 검증기 | 확인한 checkout은 MIT. schema·프롬프트·코드를 그대로 복사하지 않고, 필요한 계약을 이 저장소 목적에 맞게 새로 설계한다. |
| [medusajs/medusa-agent-skills](https://github.com/medusajs/medusa-agent-skills) (`4b495d5`) | 웹 상품 페이지의 모바일·접근성·SEO·상품 상호작용 관행 | 확인한 checkout에서 LICENSE 파일을 찾지 못했다. 코드 재사용은 보류한다. 웹 storefront는 MVP 범위 밖이며 UI 확장 시 참고만 한다. |
| [Shopify/dawn](https://github.com/Shopify/dawn) (`258f00f`) | 서버 렌더링 중심의 실제 상품 페이지와 모듈식 테마 구조 | `LICENSE.md`의 허용 범위는 Shopify 소프트웨어/서비스와 연동되는 테마로 제한된다. marketplace 상세 이미지 생성기에 코드를 옮기지 않는다. |
| [morluto/rea](https://github.com/morluto/rea) | 실행 중인 앱·웹 경험의 동작을 역공학하는 데 검토할 수 있는 도구 | 현재 분석 환경에서 실행하지 않았다. 소스 코드 리뷰를 수행한 것으로 간주하지 않으며, 이 설계의 근거는 직접 읽은 저장소 파일과 계약이다. |

위 revision은 조사에 사용한 얕은 checkout의 식별자이며, 구현 착수 시 upstream의 최신 상태와 라이선스를 다시 확인해야 한다. 별 수·fork 수는 실매장 사용의 증거로 취급하지 않는다.

## 범위와 라우팅

### MVP 포함

- 상품 정보와 하나 이상의 실제 상품 사진을 받아 상품 브리프를 정리한다.
- 사실을 출처와 함께 기록하고, 공개 가능한 사실만 문구와 이미지 지시문에 사용한다.
- 카테고리와 목표 플랫폼에 맞게 페이지 모듈을 제안하고, 생성 전 검토 가능한 계획으로 만든다.
- 필요한 경우 승인된 이미지 생성 경로로 모듈별 텍스트 없는 시각 자산을 만든다.
- 정확한 한글 문구를 코드로 조판하고, 긴 이미지를 플랫폼별 규칙에 맞춰 분할·내보낸다.
- 실제 파일의 규격·문구·모듈 참조·사실 근거를 검사하고 미리보기와 검증 기록을 제공한다.

### MVP 제외

- Shopify/Medusa 등 자사몰의 상품 상세 웹 UI, 장바구니, 결제 또는 backend integration.
- 판매자센터 로그인, 상품 업로드, 광고 운영, 게시·가격 변경.
- 공급자/API 자동 선택, silent fallback, 새 비용 원장 또는 독립 승인 DB.
- 이미지에 모델이 직접 그린 가격·한글 카피·할인 배지·인증 마크를 업로드용 최종 문구로 사용.
- source repository나 운영 중인 웹사이트에 대한 REA 결과를 정적 코드 리뷰의 대체 증거로 사용.

### 소유권

`creative-production`은 단일 총괄로 scope, 현재 실행 권한과 승인 경계를 소유한다. `product-detail-page-builder`는 제공된 상품 정보에서 상세페이지 한 건을 설계·생산하는 specialist이며, 재귀 호출·두 번째 intake·별도 프로젝트 원장을 만들지 않는다. 설치 가능한 정식 스킬로 채택할 때는 `manifest.json`, `README.md`, `integrations/skill-routing.md`, `integrations/package-provenance.md`와 버전 검증 절차를 같은 구현 변경으로 갱신한다.

실제 산출물을 파일로 저장하는 흐름은 기존 저장소의 `recording-production-history`와 `creative-production`의 단일 writer·프로젝트 root 규칙을 따른다. 상세페이지용 `page-spec.json`은 한 작업의 렌더 계약이지 `project.json`을 대체하는 상태 원장이 아니다. 채팅 내 계획/문구 검토만 요청받으면 파일 저장·생성 단계를 자동으로 확장하지 않는다.

## 사용자 입력과 사실 보호

### 최소 입력

1. 목표 플랫폼과 국가/스토어.
2. 상품명 또는 카테고리.
3. 실제 상품을 식별할 수 있는 사진 한 장 이상.

브랜드 가이드·색상·폰트·목표 고객·확인된 사양은 선택 입력이다. 필요한 필수 입력이 빠졌으면 가장 중요한 하나만 요청하고, 이미지 생성은 시작하지 않는다.

### 사실 레코드

각 사실은 최소한 다음 필드를 가진다. `evidence`는 자유로운 설명 한 줄만 두는 대신, 어떤 입력/자산에서 무엇을 확인했는지 재검토할 수 있는 locator를 보존한다.

```json
{
  "id": "compartment-count",
  "value": 3,
  "source": "user",
  "evidence": {
    "kind": "user_statement",
    "locator": "intake.product_facts.compartment_count"
  },
  "publish": true
}
```

`source`는 `user`, `visible`, `official_source`, `unconfirmed` 중 하나다. `visible` 사실에는 입력 이미지 ID와 관찰 영역(locator), 관찰 자체를 기록한다. `official_source` 사실에는 URL, 문서/필드 locator, 확인일을 기록한다. 사용자 사실에는 intake 항목 또는 원문 제공 위치를 연결한다. 제품 사진으로 숨겨진 재질·용량·성능·인증·호환성·구성품을 추론하지 않는다. `unconfirmed`는 페이지 문구와 image prompt에서 사용하지 않는다. 플랫폼 정책에서 직접 확인한 정보에는 URL·확인일·근거 수준을 붙이고, 판매자센터 확인이 필요한 규격은 최종 업로드 사양처럼 단정하지 않는다.

페이지 모듈은 참조하는 사실 ID를 선언한다. validator는 존재하지 않는 사실 참조, 미확인 사실의 게시, 게시 불가 사실 사용을 오류로 처리한다. 효능·건강·안전·아동·식품·화장품 등 고위험 상품은 증빙을 확인하기 전 해당 주장을 생략하고 필요한 최소 질문 또는 명시적 차단 사유를 낸다.

## 제작 흐름

```text
Intake
  → 상품/브랜드 입력 정리
  → 사실 출처 분류와 미확인 주장 차단
  → 공식 자료로 플랫폼 프로필 확인
  → 카테고리별 module plan 제안
  → 사용자 확인된 page-spec
  → 모듈별 텍스트 없는 이미지 자산
  → 코드 조판·크롭·분할·export
  → 자동 구조 검사 + 실제 이미지 QA
  → preview, 출력 파일, manifest와 미해결 항목 전달
```

### 단계 계약

1. **Intake/브리프:** 상품 이미지와 사실의 출처를 기록하고, 관찰과 추론을 분리한다. 이미지 속 상품의 geometry·색·표면·로고·포함 부품을 시각 기준으로 잠근다.
2. **플랫폼 라우팅:** 플랫폼·국가별 프로필에서 export mode, 폭, 포맷, 분할 제한, 이미지 내 문구/합성 이미지 정책을 읽는다. 공식 판매자 자료 우선이며, 현재 규칙을 확인할 수 없으면 unknown으로 남긴다.
3. **모듈 계획:** 상품·카테고리·플랫폼·사용자 목표에 맞춰 순서와 목적을 정한다. 기본 시작안은 hero → 문제/사용 맥락 → 확인된 이점·디테일 → 사용법/규격 → 관리·구성품 → 마무리지만, 불필요한 모듈은 생략한다. 정해진 6–10개 개수를 모든 상품에 강제하지 않는다.
4. **계획 승인:** 모듈 순서, 실제 문구, 각 문구가 참조하는 사실, 사용할 원본/생성 이미지 방법을 사용자에게 보여 준다. 요청이 실제 이미지 생성을 포함하고 있더라도 이 page-spec 확인과 기존 `creative-production` 실행 권한 경계가 닫히기 전에는 이미지를 생성하지 않는다. 텍스트/계획만 요청한 경우 이 단계의 제안으로 종료한다.
5. **생성:** 승인된 사실을 사용하는 모듈별 텍스트 없는 시각 생성만 요청한다. 모든 호출에서 상품 동일성 조건을 유지하고, 보이지 않는 면·구성품·사용 결과는 만들지 않는다. 단일 사진에는 보이는 각도·영역만 근거로 삼는다. 다른 각도나 가려진 세부를 보여야 하는 모듈은 추가 원본 사진을 요청하거나 생략한다. 생성 모델이 상품의 형상·색상·로고·구성을 보존하지 못하면 업로드용 자산으로 사용하지 않고 재검토 상태로 둔다. 생성된 각 자산을 실제로 열어 확인하기 전에는 사용 가능으로 간주하지 않는다.
6. **조판/export:** Python/Pillow 같은 결정론적 도구로 확정 문구, 폰트, 줄바꿈, 여백, 크롭, 압축, 분할을 계산한다. 모델 출력의 문자를 최종 문구로 신뢰하지 않는다. 폰트가 없거나 문구가 영역에 맞지 않을 경우 조용히 잘라내지 말고 오류를 낸다.
7. **QA/납품:** 규격·파일·page spec을 자동 검증하고, 실제 미리보기/모듈 이미지에서 제품 정체성·글자 가독성·반복 레이아웃·사실 표현을 확인한다. 검증 경고·사람의 확인이 남은 항목·최종 파일 경로를 구분해 전달한다. 게시/업로드는 별도 요청과 권한이 없으면 하지 않는다.

## 설계 QA 워크스루 — 가상 상품

**검사 방식:** 문서 요구사항을 따라 한 가상 입력을 수동으로 통과시킨 설계 단계 워크스루다. 이미지 파일이 제공되지 않아 image generation, compositor, validator, actual visual QA는 실행하지 않았다. 이 결과는 동작하는 제품의 테스트나 실제 상품에 대한 판매용 상세페이지가 아니다.

**가상 입력:** 목표는 네이버 스마트스토어 모바일 상세페이지, 상품은 “모아 3칸 데스크 오거나이저”다. 사용자가 이름·상품 분류·분체도장 강철·외형 치수 `180 × 90 × 110 mm`·칸 수 3개를 제공한다고 가정한다. 실제 상품 사진은 제공되지 않는다. 스마트스토어 export profile도 이 워크스루에서는 공식 자료로 확인하지 않았다.

| 사실 ID | 입력값 | 근거/상태 | 처리 |
|---|---|---|---|
| F01 | 모아 3칸 데스크 오거나이저 | 사용자 제공 이름/분류 | 계획에 사용 가능 |
| F02 | 칸 수 3개 | 사용자 제공 사양 | 계획/문구에 사용 가능 |
| F03 | 분체도장 강철 | 사용자 제공 사양 | 문구에는 사용 가능; 실제 표면 이미지는 사진 확인 전 단정하지 않음 |
| F04 | 외형 180 × 90 × 110 mm | 사용자 제공 사양 | 승인된 치수 도식에 사용 가능 |
| F05 | 방청, 내스크래치, 하중, 제조국, 구성품, 보증 | 미제공 | unconfirmed로 남기고 문구/생성 지시에서 제외 |
| A01 | 상품의 실제 형상·색·칸 배치·로고 | 사진 없음 | 관찰 근거 없음; 이미지 생성/업로드 자산 구성 불가 |
| P01 | 스마트스토어 이미지 제한·분할 규칙 | 이 검사에서 공식 profile 미확인 | 플랫폼 규격 export 차단; 계획안 상태만 허용 |

**예상 모듈 계획**은 실제 사진·판매자 profile 확인과 문구 계획 승인이 뒤따를 때만 유효하다.

| 순서 | 목적/임시 제목 | 허용 근거 | 남은 게이트 |
|---|---|---|---|
| 1 | Hero — “책상 도구를 세 칸으로 나눠 담아요” | F01, F02 | 실제 사진으로 상품 외형·칸 배치 확인 |
| 2 | 세 칸 구성 소개 | F02 | 실제 사진 필요; 각 칸의 용도를 임의 지정하지 않음 |
| 3 | 소재 정보 | F03 | 사용자가 제공한 문구로만 표현; 부식/내구성 효능 금지 |
| 4 | 크기 안내 | F04 | 도식은 결정론적 조판; 치수 방향이 불명확하면 사용자 확인 |
| 5 | 책상 위 사용 맥락 | F01 | 실제 사용 사진 또는 승인된 연출 지시 필요; 수납량·안정성 주장 금지 |
| 6 | 마무리 제품 컷 | F01, F02 | 원본 사진 필요; 구성품·브랜드·보증 배지 추가 금지 |

**기대되는 올바른 실행 결과:** 현재 입력에서는 가장 중요한 누락인 실제 상품 사진을 요청하고 중단한다. 생성·조판·플랫폼 export를 실행하지 않는다. 사진이 추가되더라도 단일 정면 사진만 있으면 측면·바닥·후면·가려진 로고를 새로 만들어 표현하지 않는다. 플랫폼 profile과 승인된 page-spec 전에는 이 모듈 순서를 확정하거나 “업로드 준비 완료”라고 표시하지 않는다.

**판정:** 사실 출처 분류와 근거 없는 주장의 차단은 설계상 표현되어 있다. 이 시뮬레이션은 입력 게이트가 누락 사진에서 멈추도록 정의된 것을 확인하지만, 정확한 이미지 생성·상품 동일성·한글 렌더링은 구현과 실제 사진 없이 판정할 수 없다. “제대로 된 페이지”는 이 문서에서 사실 추적, 제품 동일성, 구매 결정에 필요한 질문의 답변, 모바일 가독성, 플랫폼 규격 및 사람의 실제 시각 확인으로 평가한다. 판매 전환율이나 매출 개선은 데이터 기반 실험 없이는 보장하거나 주장하지 않는다.

## 제안 파일 구조와 계약

구현 시 설치 가능한 스킬의 최소 구조를 제안한다.

```text
product-detail-page-builder/
├── SKILL.md
├── references/
│   ├── page-spec.schema.json
│   ├── platform-profiles.json
│   ├── platform-source-policy.md
│   ├── category-playbooks.md
│   └── prompt-recipes.md
├── scripts/
│   ├── compose_detail_page.py
│   ├── export_slices.py
│   └── validate_output.py
└── tests/
    ├── fixtures/
    └── test_validate_output.py
```

이 구조는 설계 제안이다. 기존 source code의 파일을 복사한 구조가 아니며, 테스트·명령은 아직 존재하지 않는다. 반복 가능한 data contract가 필요한 경우 다음 작업에서 schema를 먼저 구현하고 예제 fixture로 검증한다.

### `page-spec.json`의 책임

한 번의 생성 작업에 필요한 플랫폼 ID와 locale, 입력 이미지 참조, 사실 레코드, 색상/폰트/여백, 순서가 있는 module 목록, 모듈별 실제 배경 자산, 문구, 크기·export 설정, 경고를 기술한다. 각 모듈의 문구는 실제 게시 사실 ID에 연결한다. 버전 필드를 두되, production `project.json`, artifact registry 또는 approval state를 중복 정의하지 않는다.

### 산출 파일

```text
<existing production root>/<product-slug>/
├── brief.json
├── page-spec.json
├── copy.md
├── modules/
├── detail-page-preview.jpg
├── slices/
└── manifest.json
```

실제 root·폴더 생성·history 기록은 기존 coordinator 및 `recording-production-history` 계약에 따른다. 외부 경로에 쓴 모든 파일은 실제 관찰한 경로로 등록한다. 샘플/fixture 산출물은 검증용임을 표시하고 승인된 판매용 결과로 취급하지 않는다.

## 플랫폼 프로필과 한국 우선 구현

공식 문서 또는 판매자센터 확인을 받은 profile만 upload-ready 규칙으로 사용한다. 각 profile은 최소한 다음을 기록한다.

- platform/site ID, locale, 확인일, 재검증 시점, 출처 URL, 근거 수준.
- export mode, width, format, 품질, slice height/count, 파일 크기 한도.
- 이미지 내 텍스트 및 합성 이미지 정책.
- seller-backend에서만 확인할 수 있는 조건과 업로드 전 경고.

첫 타깃 후보는 한국어 스마트스토어·쿠팡이다. 다만 이 문서 작성 시점에 최신 플랫폼별 seller 제한을 조사·승인한 것은 아니다. 구현자는 각 플랫폼 공식 판매자 자료를 찾아 profile에 출처를 기록하고, 공개 규칙이 없으면 현재 seller backend에서 확인하도록 표시해야 한다. 앞선 외부 생성기에서 본 750 px 등의 수치를 국내 플랫폼의 공식 보장 규격으로 가져오지 않는다.

후속으로 Amazon A+ 등 다른 플랫폼을 추가할 수 있지만, profile과 자동 검사 fixture가 함께 추가될 때만 지원 플랫폼으로 표시한다. Medusa/Dawn에서 보이는 모바일 storefront 동작은 후속 **웹 미리보기 UI**가 명시적으로 채택될 때만 별도 설계한다.

## 이미지·폰트 실행 경계

- `creative-production`에 이미 정의된 현재 이미지 실행자/권한 계약을 적용한다. 실행 환경·인증이 준비되지 않으면 blocker로 보고하며, 다른 provider로 자동 대체하지 않는다.
- 각 이미지 호출 전 현재 실행 가능한 image helper의 입력·출력 contract를 따른다. 실제 제출 prompt와 참조 asset을 기존 production history로 추적할 수 있어야 한다.
- 모든 모듈은 실제 상품 참조를 유지해야 한다. 새로운 배경 연출이 실제 상품 형태·로고·색상·구성품을 바꾸어도 된다는 뜻이 아니다.
- 정확한 한글·숫자·로고·가격·규격은 결정론적 합성 단계에서 처리한다. 상표·폰트 파일은 사용 권한을 확인하고 저장소에 무단 포함하지 않는다.
- 이미지 생성 단계의 완료와 최종 페이지 승인·판매자 업로드 권한은 분리한다.

## 품질 게이트

| 게이트 | 자동 검사 | 실제 시각 확인 |
|---|---|---|
| 사실 무결성 | 각 문구·모듈의 fact ID 존재, 미확인/미게시 사실 차단 | 이미지가 문구가 암시하는 주장과 모순되지 않는지 |
| 상품 동일성 | asset 경로와 source image 연결, 파일 읽기 가능 여부 | 형상·색·로고·표면·버튼·포함 부품의 drift |
| 구매 정보 완결성 | 확인된 사용법·규격·구성품이 page spec에 반영됐는지 | 구매 판단에 필요한 질문이 답변됐고 같은 내용을 반복하지 않는지 |
| 페이지 사양 | profile 크기·포맷·slice/file limit·순서 | 휴대폰 폭에서 글자와 주요 제품이 읽히는지 |
| 조판 | 글자 overflow, 잘못된 파일/폰트, 빈 텍스트 영역 탐지 | 가독성·대비·줄바꿈·한글 깨짐 |
| 구조/납품 | module 수와 참조, 출력 파일·manifest 일치 | 모듈 간 스타일 연속성과 불필요한 반복 |
| 상태/권한 | warning 및 seller confirmation 항목 보존 | 결과의 승인/미승인·업로드 미실행 상태 명시 |

validator 성공은 상품 사실의 진위, 광고법 준수, 제품 identity 또는 미감 QA를 증명하지 않는다. layout/page plan 통과와 플랫폼 upload-ready를 분리하고, manifest에는 최소한 `plan_review`, `platform_profile`, `asset_visual_review`, `upload_readiness` 각각의 실제 상태와 blocker를 기록한다. 이는 산출물 검토 상태이지 별도 승인 원장이나 생산 `project.json`이 아니다. 사람이 확인하지 않은 시각 주장을 QA pass로 기록하지 않는다. 광고 성과/전환 효율은 실제 실험 결과가 없으면 미검증으로 둔다. 잘못된 테스트를 고치기 위해 기존 회귀 검사를 삭제하거나 약화하지 않는다.

## 구현 단계와 완료 기준

### Stage 0 — 정책 및 프로필 조사

- 공식 스마트스토어·쿠팡 판매자 규정과 이미지 export 조건을 조사한다.
- 모든 규칙에 출처·확인일·근거 수준을 붙인다.
- 조회 불가/로그인 전용 제약은 추정 대신 명시적으로 표시한다.
- 검토한 외부 upstream revision과 라이선스를 구현 착수 시 다시 기록한다.

**통과 조건:** 정확한 국내 MVP 범위와 프로필 근거가 승인되고, 미확인 규칙이 upload-ready 제한과 분리된다.

### Stage 1 — 사실 브리프와 page spec

- `SKILL.md`의 최소 입력, 사실 분류, 모듈 계획, 허위 주장 차단을 구현한다.
- page-spec schema와 실제 fixture를 설계하고 schema validation 테스트를 둔다.
- `creative-production`과 기존 production artifact/history 경계에 라우팅한다.

**통과 조건:** 공개 가능한 모든 문구가 승인된 fact에 연결되고, unconfirmed 사실이 있으면 관련 모듈이 거부된다.

### Stage 2 — 조판과 플랫폼 export

- 분리된 text/image module 입력으로 정확한 한글 합성을 구현한다.
- 정해진 크기/압축/분할 규칙, 폰트 검사, overflow 검사를 구현한다.
- 기존 프로젝트의 Python 버전·의존성 설치/테스트 계약에 맞춘다.

**통과 조건:** fixture의 문구가 문자 단위로 보존되고, 파일 규격과 분할 경계 검사가 deterministic하게 통과한다.

### Stage 3 — 이미지 생성과 시각 QA

- 현재 허용된 image executor를 사용하는 작업 절차와 실제 prompt provenance를 연결한다.
- 제품 참조·모듈별 text-free 생성·실제 파일 검사를 순서화한다.
- 실이미지를 사람이 보지 않은 상태를 완료/FINAL로 표시하지 않는다.

**통과 조건:** 각 모듈이 올바른 입력·사실·product lock으로 추적되고, 시각 검사 결과 및 blocker가 manifest와 납품 보고에 남는다.

### Stage 4 — 패키지 등록과 회귀

- 승인 후 manifest/README/routing/provenance/version을 갱신한다.
- 관련 skill install, version check와 Python 회귀를 기존 단일 명령 계약으로 실행한다.
- 플랫폼별 positive/negative fixture와 전체 제품 브리프 smoke를 실행한다.

**통과 조건:** 현 패키지 테스트 전체가 한 번의 실행으로 통과하고, 설치기가 새 specialist만 추가하며 기존 skill을 덮어쓰지 않는다.

## 권리·출처·개인정보 경계

이 저장소에는 reuse license가 없으므로, 초기 구현은 외부 스크립트·skill prose·prompt template·데모 이미지·생성 샘플을 복사하지 않고 독립적으로 작성한다. 참조 upstream의 저장소명·URL·조사 revision·라이선스 상태는 이 설계처럼 조사 evidence로 기록할 수 있다. 추후 vendoring이 필요하면 파일별 출처, 정확한 commit, license notice, 포함 파일, 수정 내역을 확인하고 package policy에 맞는지 별도 승인받는다.

사용자 상품 이미지·상표·판매 데이터는 요청 작업에 필요한 범위 외에 저장소 fixtures, 외부 도구, 공유 사례집으로 옮기지 않는다. fixture는 합성/허구 데이터를 사용하고 실제 생성 파일을 테스트에 넣지 않는다. 외부 서비스로 이미지를 전송할 때는 선택된 실행자와 실제 입력·권한 계약을 따른다.

## REA의 역할

REA는 GitHub의 오픈소스 역공학 프로젝트로 조사 대상 후보에 포함했다. 현재 세션에서는 설치하거나 실행하지 않았으므로, 이 설계는 REA 분석 결과라고 주장하지 않는다. 저장소의 skill markdown, Python 스크립트, JSON profile, Liquid theme 코드는 직접 읽어 비교했다. 후속 구현에서 REA를 사용할 경우 각 입력 유형에 대한 공식 지원 범위와 재현 가능한 실행 증거를 먼저 확인하고, 해당 결과를 소스·라이선스 검토나 실제 시각 QA와 혼동하지 않는다.

향후 브라우저 미리보기/웹 편집기가 구현되어 역공학 비교가 명시적으로 요청되면, REA가 지원하는 대상에 한해 관찰 가능한 UI·동작 비교를 별도 QA로 수행할 수 있다. 그 결과를 upstream 코드 구조·라이선스 분석, 실제 상품 정책 준수, 시각 QA, 사용자 승인으로 대체하지 않는다.

## 위험과 미해결 결정

| 항목 | 현재 상태 | 구현 전 처리 |
|---|---|---|
| 스마트스토어 폭 | 공식 FAQ에 860px 및 848px 권장이 각각 존재 | 860px는 작업 폭만 제공; 판매자센터에서 실제 폭 확인 전 upload-ready 차단 |
| 스마트스토어 총 길이/용량 | 공식 FAQ의 20MB/이미지, 4000px 접힘 안내를 profile에 기록 | 길이 초과 경고; 3000px slice는 운영상 기본값이지 공식 단일 이미지 높이 제한이 아님 |
| 쿠팡 상세 이미지 폭/제한 | 공개 가이드에서 상세설명 입력 방식만 확인; 정확한 폭/파일 제한 미공개 | WING에서 실제 상세 입력 규격 확인 전 upload-ready 차단 |
| 신규 specialist의 manifest/설치 영향 | 설계 결정만 존재 | 기존 설치 테스트와 버전 정책 검토 |
| Medusa source reuse | checkout에 명시 license 없음 | 코드 복사 금지, 필요하면 권리 확인 |
| Dawn 코드 reuse | Shopify 서비스 연동 테마로 조건 제한 | marketplace asset pipeline에 vendoring 금지 |
| 외부 MIT 코드 결합 | 권리상 가능한 경우가 있더라도 본 저장소 policy 미정 | 기본 미사용; 사용 요청 시 notice 및 provenance 검토 |
| CJK 폰트 배포/런타임 | 환경별 가용성 확인 필요 | 폰트를 무단 번들하지 않고 실제 선택·라이선스 상태 검사 |
| 이미지 내 제품 drift | 자동 검증만으로 닫히지 않음 | 실제 결과를 사람 눈으로 확인 |
| REA 적용 범위 | 이 리뷰에서 실행하지 않음 | 사용할 입력 유형에 대한 공식 지원 확인 후 별도 선택 |

## 설계 승인 acceptance

- [ ] specialist는 `creative-production` 단일 총괄 및 기존 project/history owner를 유지한다.
- [ ] 한글 플랫폼 MVP의 공식 규칙 출처와 seller-backend 불확실성이 문서화된다.
- [ ] 게시 문구는 user/visible/official-source 근거와 재검토 가능한 locator에 연결된다.
- [ ] 단일/가림 사진에서 관찰되지 않는 표면·각도·구성품을 만들지 않는 제약이 있다.
- [ ] page-plan/copy 확인과 실제 이미지 생성 권한이 생성 전 단계로 분리된다.
- [ ] 이미지 생성과 정확한 문구 조판이 분리된다.
- [ ] 자동 검증과 실제 시각 검수, plan readiness와 upload readiness, review와 upload 권한이 구분된다.
- [ ] 구매 정보 완결성을 점검하지만 전환율·매출 향상을 근거 없이 약속하지 않는다.
- [ ] 외부 프로젝트 코드를 기본으로 vendoring하지 않는다.
- [ ] 기존 package install/version/test 경계를 지킨다.
- [ ] 별도 production schema·승인 DB·provider router를 추가하지 않는다.
