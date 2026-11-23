# 모션그래픽 파이프라인 M1~M6

요청에 모션그래픽 요구가 있으면 이 파일을 따른다. 요구는 영상 전체일 수도 있고 컷 하나일 수도 있다. 순서는 **감지 → 분석 → 연출 판단 → 설계 → 구현 → 검수**다. 승인·비중단·마감 규칙은 [policy.md](policy.md)가 정본이고, 이 파일은 모션에 필요한 판단만 더한다. 텍스트만 요청했으면 M4까지 하고 멈춘다. 렌더된 영상을 요청했으면 M6까지 진행한다.

판단 근거는 Prompt Motion 공개 코퍼스(2026-11-23 스냅샷, 450행)를 분류한 흡수 원장(패키지 저장소의 `docs/research/prompt-motion-absorption-ledger.csv`, 설치본에는 없음)이다. 원문과 예제 미디어는 패키지에 넣지 않았다.

## M1 감지 {#m1-detect}

다음 중 하나라도 해당하면 모션 파이프라인을 켠다.

- **명시적 요구:** 모션그래픽, 키네틱 타이포, 인포그래픽·차트·숫자 애니메이션, 로고 애니메이션, 앱·제품 데모·출시 영상, 쇼릴, 애니메이션 설명 영상, 3D 회전·스크롤 영상, 가격표·자막 그래픽처럼 화면 위에서 움직이는 그래픽
- **묵시적 요구:** 촬영할 대상이 없는 정보(문구·수치·절차·관계·UI 상태)를 영상으로 보여 달라는 요청

실사 중심 요청 안에 그래픽 컷이 섞여 있으면 **그 컷만** 파이프라인을 타고, 나머지 컷은 기존 실사 경로를 유지한다. 자막·하단 이름 자막만 필요한 편집은 [23a](../../video-production-assets/references/23a-captions-layout.md) 경로를 쓰고 이 파일을 열지 않는다. 그래픽이 필요 없다고 판단하면 `모션 불필요: 이유` 한 줄을 남기고 기존 경로로 간다.

## M2 요구사항 분석표 {#m2-analysis}

아래 11칸을 모두 채운다. 요청이나 자료에서 알 수 없는 칸은 되돌릴 수 있는 값으로 채우고 `inferred`로 표시한 뒤 계속 진행한다. 질문은 핵심 축(주제·목적)을 추론할 수 없을 때만 한다.

| 칸 | 내용 | 비어 있을 때 |
|---|---|---|
| `audience_task` | 관객이 이해하거나 느껴야 할 것 한 문장 | 요청에서 추론. 추론할 수 없을 때만 질문 |
| `message_units` | 꼭 전달할 단위(문구·수치·단계·기능) 목록 | 요청·자료에서 추출. 지어내지 않음 |
| `format_hint` | 아래 형식 표의 후보 ID | 추론 |
| `platform` | 플랫폼·화면비·안전 영역 | `inferred` |
| `duration` | 총 길이와 컷당 읽기 시간 | `inferred` |
| `assets` | 승인 자산(로고·화면·사진·음원)과 권리 상태 | 플레이스홀더 `[로고]`로 표시하고 계속 진행 |
| `data_sources` | 수치의 출처 | 출처가 없으면 수치 차트를 쓰지 않음([10](../../video-production-assets/references/10-evidence.md)) |
| `audio` | 음원·내레이션 유무, BPM 확정 여부 | 무음 박자표를 시작값으로 |
| `brand` | 색·서체·금지 사항 | 중립 토큰을 `inferred`로 |
| `constraints` | 마감·납품 규격·금지 표현 | 기록 |
| `delivery` | 텍스트 설계까지인지, 렌더 영상까지인지 | 요청 문장으로 판정 |

### 형식 표

| 형식 | 맞는 요청 | 기본 레시피 | 구조 |
|---|---|---|---|
| `showreel` | 쇼릴·브랜드 무드·키네틱 타이포 영상 | `kinetic_type` / `shape_morph` | 모티프 하나 → 크기·속도·매체 변주 → 모티프 회수. 박자마다 변화 하나 |
| `product_film` | 앱·SaaS·제품 출시·프로모·데모 | `ui_state` → `brand_product` | 첫 마디 훅 → 제품의 대표 순간 3~4개 → 가장 큰 박에 결말 → 로고와 CTA |
| `explainer` | 개념·절차·데이터 설명 | `diagram_data` | 질문 → 직관 → 쉬운 예에서 어려운 예 → 정리. 레이아웃 고정 |
| `character_short` | 캐릭터가 있는 짧은 이야기 | `character_photo` / `pose_swap` | 자극 → 반응 → 결과. 한 샷에 동작 하나 |
| `realtime_3d` | 깊이·시점·조작이 정보 자체인 경우 | `realtime_3d` | 대표 샷부터 거꾸로 설계 |
| `logo_bumper` | 로고 공개·인트로·범퍼 | `brand_product` + 루프 | 조각 → 식별 시점 → 홀드. 루프 경계 확인 |
| `edit_assist` | 기존 영상 위 그래픽 | 편집 레인([09a](../../video-production-assets/references/09a-short-form-edit-recipes.md), [23a](../../video-production-assets/references/23a-captions-layout.md)) | 발화 타이밍에 그래픽 배치 |

## M3 연출안 비교와 선택 {#m3-direction}

1. 형식 하나와 레시피 하나로 이루어진 **후보 2~3개**를 만든다. 정보가 명백히 한 가지 표현에만 맞을 때만 후보 1개와 탈락 이유 한 줄을 허용한다.
2. 후보마다 네 기준을 `상/중/하`와 한 줄 이유로 평가한다.
   - **전달력:** `message_units`가 읽기 시간 안에 읽히는가
   - **자산 적합성:** 승인된 자산과 출처 있는 데이터만으로 만들 수 있는가
   - **구현 가능성:** M5 매트릭스에서 `local` 또는 `code`로 구현되는가
   - **길이 적합성:** `duration` 안에서 컷마다 읽기 홀드를 확보하는가
3. 선택을 `recipe + format + reason`으로 기록하고 `inferred`로 표시한 뒤 계속 진행한다. 사용자가 직접 고르겠다고 했을 때만 멈춘다.

| 레시피 | 맞는 전달 과제 | 최소 장면 구조 | 피하거나 바꿀 때 |
|---|---|---|---|
| `kinetic_type` | 문구 자체의 대비·반전 | 설정 → 대조 카피 → 회수, 분명한 읽기 홀드 | 인물의 미세 반응이 핵심이면 `character_photo` |
| `ui_state` | 선택에 따른 상태 차이 | 초기 화면 → 행동 → 결과 | 실제 UI가 없으면 가상 UI라고 명시하거나 타이포 |
| `diagram_data` | 관계·순서·비교 | 기준 → 한 번에 하나씩 변화 → 읽는 시간 | 통계가 미확인이면 수치 차트 대신 개념도 |
| `shape_morph` | 한 대상이 다른 의미·상태로 바뀜 | 변하지 않는 앵커 → 변형 → 알아볼 수 있는 끝 상태 | 효과만 눈에 띄면 컷이나 디졸브 |
| `card_sequence` | 나란히 비교하거나 한 항목씩 읽는 목록 | 항목 공개 → 같은 기준으로 비교 | 실제 UI 행동이 핵심이면 `ui_state` |
| `character_photo` | 반응·표정 또는 사진이 근거 | 자극 → 반응 → 결과 | 초상·자산 권리가 불명하면 추상 모션 |
| `brand_product` | 브랜드 인지·기능 공개 | 사용자 과제 → 증거·기능 → 승인 마크 공개 | 로고·기능·효능을 지어내지 않음 |
| `realtime_3d` | 깊이·시점·실시간 조작이 설명에 필요 | 대표 샷 → 시점·정보 변화 → 가독 상태 | 평면으로 같은 정보를 전달할 수 있으면 2D |

CineForge 프로젝트에서는 분석표·후보·선택·컷별 경로를 `production_spec.motion_brief = {analysis, candidates, choice, route_by_cut}`(`route_by_cut`은 `[{cut, route}]` 목록)에, 선택한 레시피를 기존 `production_spec.motion_recipe = {recipe, reason}`에 기록한다.

## M4 설계와 구현 브리프 {#m4-design}

- 컷 표: 컷 ID, 시작 상태 → 행동·시간 → 끝 상태, 보여 줄 것·숨길 것, 박자나 큐, 읽기 홀드, 적용 기법 ID
- 형식 구조는 위 형식 표를 따르고, 기법은 [코드 기반 모션 제작](../../video-production-assets/references/08b-code-motion-production.md#prompt-motion-techniques)과 [모션 크래프트](../../video-production-assets/references/08a-motion-craft.md#prompt-motion-craft)에서 고른다.
- [구현 브리프 템플릿](../../video-production-assets/assets/code-motion-brief-template.md)의 6칸을 모두 채운다. 해당 없음은 `N/A — 이유`로 쓴다. 텍스트 답으로 끝나는 요청에서도 `구현 브리프` 제목 아래에 6칸(입력·방향·구조·빌드·주의·시작·납품)을 그대로 쓴다. M2 분석표와 M3 비교만으로 M4를 대신하지 않는다.

## M5 구현 경로 판정과 실행 {#m5-route}

컷마다 경로를 정한다.

| 경로 | 조건 | 실행 |
|---|---|---|
| `local` | 아래 매트릭스에서 `local`이 `지원`이고, 720×1280(9:16)·30fps·무음으로 충분할 때 | `cineforge motion <project> --font …` → 미리보기 검수 → `cineforge motion <project> --deliver <sha256>` |
| `code` | 그 밖의 2D 모션그래픽 | HTML 작품 → `node video-production-assets/scripts/render_html_motion.mjs` ([코드 렌더 경로](../../video-production-assets/references/08b-code-motion-production.md#code-render-path)) |
| `realtime_3d` | 깊이·시점·실시간 조작이 정보 자체일 때 | [open-3d-production](../../open-3d-production/SKILL.md)과 [실시간 모션 연출](../../open-3d-production/references/realtime-motion-direction.md) |
| `downgrade` | 위 경로로 구현할 수 없을 때 | 가장 가까운 지원 기법으로 대체하고 분석표와 최종 보고에 `downgrade: 원래 기법 → 대체 기법, 이유`를 남긴다 |

경로가 섞인 작품은 컷 단위로 렌더한 뒤 `cineforge render`(FFmpeg 조립)로 합친다. 로컬 코드 렌더는 유료·외부 실행이 아니어서 지출 승인 대상이 아니다. 하지만 G2 검수와 재생 검수 해시 납품은 그대로 적용한다. CineForge 프로젝트에서는 실행 계획 레인 `{kind: video_cut, provider: code-motion}`으로 봉투를 만든다. 직접 `cineforge results`를 호출하지 말고 스킬팩의 [제출 검사](../../video-production-assets/references/08b-code-motion-production.md#code-motion-submit)로 컷 명세가 맞는 MP4만 제출한다.

### 구현 가능성 매트릭스

| 레시피·기법 | local | code | realtime_3d |
|---|---|---|---|
| `ui_state` | 지원 | 지원 | 불가 |
| `kinetic_type` | 지원 | 지원 | 불가 |
| `echo_type` | 지원 | 지원 | 불가 |
| `diagram_data` | 지원 | 지원 | 부분(3D 구조도) |
| `shape_morph` | 지원 | 지원 | 부분 |
| `card_sequence` | 지원 | 지원 | 불가 |
| `image_reveal` | 지원 | 지원 | 불가 |
| `chart_bars` | 지원 | 지원 | 불가 |
| `paper_layers` | 지원 | 지원 | 불가 |
| `map_route` | 지원 | 지원 | 부분(공간 검증은 Blender) |
| `pose_swap` | 지원 | 지원 | 불가 |
| `character_photo` | 불가 | 부분(승인 사진·포즈만) | 불가 |
| `brand_product` | 불가 | 지원(승인 마크만) | 부분 |
| `realtime_3d` | 불가 | 불가 | 지원 |
| 주인공 객체 변형 `T-throughline` | 불가 | 지원 | 부분 |
| 실제 UI 레이어 재구성 `T-vector-ui` | 불가 | 지원 | 불가 |
| 박자표 `T-beatgrid` | 부분(무음 프레임 큐) | 지원(승인 음원 합성) | 지원 |
| 가로 16:9·임의 해상도 | 불가 | 지원 | 지원 |

`local` 열의 `지원` 행은 CineForge `local_motion.RECIPES`와 같아야 한다. 테스트가 둘을 대조한다.

## M6 검수 {#m6-review}

- 실제 출력본에서 첫 프레임, 각 컷 경계, 박자 지점, 마지막 홀드 프레임을 뽑아 본다. `code` 경로는 렌더 리포트의 결정성 결과와 컨택트 시트를 함께 확인한다.
- 사용한 기법의 탈락 조건을 체크리스트로 판정한다. 결과는 PASS/FAIL과 해당 프레임 번호로 남긴다.
- 수정은 실패한 컷만 다시 렌더한다(`--frames A:B`). 실제 영상 요청 검수는 최대 2회이며 [phase-review](phase-review.md) 계약을 따른다.
- 납품은 해시를 고정한 뒤 진행한다. `local`은 `cineforge motion --deliver <sha256>`, `code`는 영수증 기록과 사람 재생 검수(`cineforge qa-playback`)를 거친 해시로만 납품한다. 공개 업로드는 별도 승인 없이 하지 않는다.
- 최종 보고에는 분석표 요약, 선택한 연출과 이유, 컷별 경로, `downgrade` 기록, 출력 파일 경로와 sha256, 검수 판정을 넣는다.
