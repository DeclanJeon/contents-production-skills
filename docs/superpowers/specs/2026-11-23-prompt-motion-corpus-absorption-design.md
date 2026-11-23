# 모션그래픽 요구 분석·연출·구현 파이프라인 및 Prompt Motion 코퍼스 흡수 설계

상태: **승인됨**(2026-11-23 사용자: "좋아 설계문서에 넣고 작업지시서를 작성해서 …"). 추천안 A — 코드 렌더 경로를 기본으로 하고 CineForge가 지원하는 레시피는 CineForge로 보냄 · 작업지시서: [2026-11-23-motion-pipeline-work-order](../plans/2026-11-23-motion-pipeline-work-order.md)
작성: 2026-11-23 · 대체: [2026-11-21 통합 스펙](2026-11-21-prompt-motion-integration.md)의 범위 문단(원작 비복제 원칙은 유지)
관련 저장소: 이 저장소(contents-production-skills)와 CineForge(`~/Documents/Projects/Products/01_Persnal_Work/cineforge`)

## 1. 의도

요청에 모션그래픽과 관련된 요구가 있으면 에이전트가 다음 순서로 **실제 영상 파일까지** 만들게 한다.

1. **감지** — 요청 속 모션 요구를 찾는다. 요청 전체가 모션그래픽인 경우뿐 아니라 일부 장면에만 필요한 경우도 포함한다.
2. **분석** — 요구를 필수 항목 분석표로 나눈다.
3. **연출 판단** — 연출안 2~3개를 비교해 하나를 고르고 근거를 남긴다.
4. **설계** — 컷·박자·전환·자산·탈락 조건을 정하고 구현 브리프를 쓴다.
5. **구현** — 기법별로 실행 가능한 경로를 판정하고, 그 경로로 실제로 렌더한다.
6. **검수** — 실제 출력본으로 판정하고, 기존 2회 검수 한도와 납품 게이트를 지킨다.

판단 근거는 2026-11-23 Prompt Motion 전수 아카이브(공개 갤러리 237개 항목, CSV 450행, 예제 GIF 239개)에서 추출한다. 아카이브 자체는 저장소에 넣지 않는다.

## 2. 현재 상태와 부족한 부분

| 단계 | 현재 | 부족한 부분 |
|---|---|---|
| 감지 | `creative-production` Step 1이 위임된 주제에만 `motion-selection`을 연다 | 일반 영상 요청 안의 부분적 모션 요구를 찾지 못함 |
| 분석 | 관객이 이해할 것 한 문장 | 플랫폼·화면비·길이·자산·권리·데이터·음향·브랜드 분석표가 없음 |
| 연출 | 레시피 하나를 선택 | 대안 비교와 선택 근거가 없음 |
| 설계 | 08b의 컷 시작·행동·끝 표 | 형식별 구조(쇼릴·제품·설명·캐릭터·3D)와 코퍼스 기법이 없음 |
| 구현 | `cineforge motion`: ffmpeg 기반, 720×1280(9:16) 30fps 무음, 레시피 11종(`ui_state`, `kinetic_type`, `echo_type`, `diagram_data`, `shape_morph`, `card_sequence`, `image_reveal`, `chart_bars`, `pose_swap`, `paper_layers`, `map_route`) | 주인공 객체 변형, 실제 UI 레이어 재구성, 커서 연출, 박자 싱크, 16:9, 자유 구도는 구현할 수 없음. 그 밖의 코드 렌더 레인(Remotion 계열)은 manifest에 외부 레인으로만 있고, 이 머신에는 설치되어 있지 않음 |
| 검수 | 08b POST, 2회 검수, 해시 기반 납품 | 코드 렌더 산출물을 CineForge 영수증·납품에 연결할 경로가 없음 |

## 3. 목표 / 비목표 / 반목표

**목표**
- 모션 요구가 있는 요청은 위 6단계를 빠짐없이 거쳐 검수된 MP4로 끝난다(텍스트만 요청한 경우는 4단계까지).
- 코드 렌더 경로를 의존성 설치 없이 이 머신에서 실행할 수 있게 한다. 설치된 Google Chrome, Node 24, FFmpeg만 사용한다.
- 코퍼스 450행을 전부 분류하고, 흡수한 기법은 기존 오너 파일 한 곳에만 정본으로 둔다.

**비목표**
- CSV, GIF, 프롬프트 원문, 예제 영상은 저장소와 스킬에 넣지 않는다.
- 새 스킬과 새 라우트(`routing.csv`)를 만들지 않는다. 모든 내용은 기존 `creative-production`, `video-production-assets`, `open-3d-production`에 넣는다.
- Remotion·Playwright 등 npm 패키지 설치나 유료 생성 모델 호출은 하지 않는다.
- 3D 실시간 렌더 구현은 기존 `open-3d-production` 경로를 그대로 쓰고 새로 만들지 않는다.

**반목표(동작해도 실패로 본다)**
- 분석표 없이 레시피를 바로 고르는 것
- 지원되지 않는 기법을 조용히 다른 기법으로 바꾸는 것. 기법을 낮추면 반드시 명시해야 한다.
- 원문을 그대로 옮겨 패키지가 프롬프트 모음이 되는 것
- 원본의 고정값(120 BPM, 60fps, 1.0→1.04 푸시 등)이 기본 정책이 되는 것
- 원본의 "로고를 사이트에서 가져와라 / 묻지 말고 빌드하라"가 권리·승인 게이트를 우회하는 것
- 쇼릴 템플릿 반복(같은 본문 49회)을 49개의 근거로 세는 것

## 4. 접근 방식(결정됨)

| 방식 | 판정 |
|---|---|
| A. 저장소에 코드 렌더 경로를 새로 두고, CineForge 지원 레시피는 CineForge로 보냄 | **채택**. 코퍼스 기법 대부분을 바로 구현할 수 있음. CineForge 쪽 변경은 영수증 연결에 필요한 최소 범위로 제한 |
| B. CineForge 레시피만 확장 | 기각. 기법마다 렌더러를 개발해야 해서 느림 |
| C. 카탈로그나 새 스킬 | 기각(사용자가 원본 포함을 제외함, 오너 중복) |

## 5. 모션 파이프라인(M1~M6)

정본 위치: `creative-production/references/motion-pipeline.md`(신규 참조 파일. 스킬은 새로 만들지 않음). 기존 `motion-selection.md`는 M3의 레시피 표로 흡수되어, 이 파일의 한 절이 된다. 기존 링크는 앵커로 리다이렉트한다.

### M1 감지

다음 중 하나라도 해당하면 모션 파이프라인을 켠다.
- 명시적 표현: 모션그래픽, 키네틱 타이포, 인포그래픽 영상, 로고 애니메이션, 제품 데모 영상, 앱 홍보 영상, 쇼릴, 애니메이션 설명 영상, 차트·숫자 애니메이션, 3D 회전·스크롤 영상
- 묵시적 표현: 실제 촬영 대상이 없는 정보(숫자·절차·관계·UI 상태·문구)를 영상으로 보여 달라는 요구, 또는 실사 영상 안의 자막을 넘어서는 그래픽 삽입

`creative-production` Step 1의 기존 문장("For delegated topics, use motion selection if motion serves the audience task")은 "모션 요구가 감지되면 M1~M6을 따른다"로 바꾼다. 위임 여부와 상관없이 적용한다. 실사 중심 요청에 모션이 일부 섞여 있으면 해당 컷만 모션 파이프라인을 탄다.

### M2 요구사항 분석표(필수 칸)

| 칸 | 내용 | 비어 있을 때 |
|---|---|---|
| `audience_task` | 관객이 이해하거나 느껴야 하는 것 한 문장 | 핵심 축이므로 추론. 추론할 수 없을 때만 질문 |
| `message_units` | 꼭 전달할 단위(문구, 수치, 단계, 기능) 목록 | 요청과 자료에서 추출 |
| `format_hint` | §6.1의 형식 ID 후보 | 추론 |
| `platform` | 플랫폼, 화면비, 안전 영역 | `inferred`로 표시 |
| `duration` | 길이 | `inferred` |
| `assets` | 승인 자산(로고, 화면, 사진, 음원), 권리 상태 | 없으면 플레이스홀더로 표시하고 계속 진행 |
| `data_sources` | 수치의 출처 | 없으면 수치 차트 금지(기존 규칙) |
| `audio` | 음원이나 내레이션의 유무, BPM 확정 여부 | 없으면 무음 박자표를 시작값으로 |
| `brand` | 색·서체·금지 사항 | 없으면 중립 토큰을 `inferred`로 |
| `constraints` | 마감, 납품 규격, 금지 표현 | 기록 |
| `delivery` | 텍스트 설계까지인지, 렌더된 MP4까지인지 | 요청 문장으로 판정 |

`inferred` 처리와 질문 제한은 policy §1의 비중단 규칙을 그대로 따른다. 분석표는 CineForge 프로젝트에서는 `production_spec.motion_brief.analysis`에 기록한다(§9의 CineForge 변경 참고). CineForge 밖에서는 브리프 파일의 첫 블록에 넣는다.

### M3 연출안 비교와 선택

- 형식 ID 하나와 레시피 하나로 구성된 **후보 2~3개**를 만든다. 정보가 명백히 하나뿐일 때만 후보 1개와 탈락 이유 한 줄을 허용한다.
- 평가 기준은 네 가지다. 각각 `상/중/하`와 한 줄 이유를 쓴다.
  1. **전달력**: message_units가 읽히는가
  2. **자산 적합성**: 승인된 자산만으로 만들 수 있는가
  3. **구현 가능성**: §7 매트릭스에서 `local` 또는 `code`로 구현되는가
  4. **길이 적합성**: duration 안에 읽기 홀드를 확보할 수 있는가
- 고른 결과는 `recipe + format + reason`으로 기록한다. 되돌릴 수 있는 선택이므로 `inferred`로 표시하고 계속 진행한다. 사용자가 고르기를 요청했을 때만 멈춘다.

### M4 설계와 구현 브리프

- 컷 표: 컷 ID, 시작 상태 → 행동·시간 → 끝 상태, 보여 줄 것·숨길 것, 박자나 큐, 읽기 홀드, 적용 기법 ID(§6.2)
- 형식별 구조: §6.1의 구조 열을 따른다.
- 브리프 템플릿 `video-production-assets/assets/code-motion-brief-template.md`의 6칸(입력, 방향, 구조, 빌드, 주의, 시작·납품)을 모두 채운다. 해당 없음은 `N/A — 이유`로 쓴다. 구현 경로가 `code`이면 이 브리프가 코드 작성의 직접 입력이 된다. 구현 경로가 `local`이면 브리프의 컷 표를 CineForge `motion_recipe` 컷 필드로 옮긴다.

### M5 구현 경로 판정과 실행

컷마다 §7 매트릭스로 경로를 정한다.

| 경로 | 조건 | 실행 |
|---|---|---|
| `local` | 레시피와 필드가 모두 CineForge 로컬 지원 범위 안에 있고, 720×1280(9:16) 무음으로 충분할 때 | `cineforge motion <project> --font …` → 미리보기 → 검수 → `--deliver SHA` |
| `code` | 그 밖의 2D 모션그래픽 전부 | §8 코드 렌더 경로 |
| `realtime_3d` | 깊이·시점·실시간 조작이 정보 자체일 때 | `open-3d-production` 기존 경로 |
| `downgrade` | 위 경로로 구현할 수 없을 때 | 가장 가까운 지원 기법으로 대체하고, 분석표와 최종 보고에 `downgrade: 원래 기법 → 대체 기법, 이유`를 기록 |

한 작품 안에서 경로가 섞이면 컷 단위로 렌더한 뒤 기존 `cineforge render`(ffmpeg 조립)로 합친다.

### M6 검수

- 08b POST를 그대로 적용한다. 실제 출력본에서 첫 프레임, 각 컷 경계, 박자 지점, 마지막 홀드의 프레임을 추출해 확인한다.
- 기법별 탈락 조건(§6.2)을 체크리스트로 판정한다.
- 수정은 실패한 컷만 다시 렌더한다. 실제 영상 요청 검수는 최대 2회이며, 기존 `phase-review` 계약을 따른다.
- 납품은 해시를 고정한 뒤 진행한다. `local`은 `cineforge motion --deliver`, `code`는 §9의 영수증 경로를 쓴다. 공개 업로드는 별도 승인 없이 하지 않는다.

## 6. 코퍼스에서 추출할 판단 자료

### 6.1 형식(`format`)

| ID | 코퍼스 근거(개선본 기준) | 기본 레시피 | 구조 |
|---|---|---|---|
| `showreel` | motion design showreel 72(그중 49개는 같은 본문), showreel 21, intro·hype | `kinetic_type` / `shape_morph` | 하나의 모티프 → 크기·속도·매체 변주 → 모티프 회수. 박자마다 변화 하나 |
| `product_film` | launch 10, promo 10+, product film 5, demo·release·hero | `ui_state` → `brand_product` | 첫 마디 훅(문제 3~5단어) → 제품의 대표 순간 3~4개 → 가장 큰 박에 결말 → 로고와 CTA |
| `explainer` | explainer 17+, recipe·product explainer, recursion | `diagram_data` | 질문 → 직관 → 쉬운 예에서 어려운 예 → 정리. 레이아웃 고정 |
| `character_short` | animated short film 12, animated film | `character_photo` / `pose_swap` | 한 샷에 동작 하나, 자극 → 반응 → 결과, 개그마다 반응 박자 |
| `realtime_3d` | 3D 게임·공중전·스크롤 3D·3D 템플릿 | `realtime_3d` | 대표 샷부터 거꾸로 설계 |
| `logo_bumper` | logo reveal, teaser, intro, bumper | `brand_product` + 루프 | 조각 → 식별 시점 → 홀드. 루프 경계 확인 |
| `edit_assist` | talking-head 편집, 리메이크 비교 | 기존 편집 레인(09a, 23a) | 발화 타이밍에 그래픽 배치 |
| `other` | 위에 해당하지 않음 | 해당 없음 | `reason` 필수 |

### 6.2 기법(`techniques`) 초기 코드북

새 기법은 **서로 다른 본문 묶음(`dup_group`) 3개 이상**에서 확인될 때만 추가한다. 각 기법은 정본 위치 한 곳, 구현 경로, 탈락 조건을 가진다.

| ID | 기법 | 정본 | 경로 | 탈락 조건 |
|---|---|---|---|---|
| `T-throughline` | 제품 속 한 객체가 장면마다 변형되어 엔드카드 로고가 됨 | 08b | code | 어떤 장면에서 객체가 사라지거나, 로고 공개 전에 정체가 드러남 |
| `T-beatgrid` | 박자표를 먼저 작성하고 박자마다 변화 하나, 가장 큰 박에 결말 | 08b | code / local(무음) | 변화가 같은 박에 몰리거나, 읽을 시간이 없음 |
| `T-vector-ui` | 승인된 UI를 레이어로 재구성하고, 커서로 실제 클릭·드래그 | 08b | code | 클릭 전에 결과가 보이거나, 존재하지 않는 기능을 보여 줌 |
| `T-camera-handoff` | 카메라가 이전 장면의 끝 배율에서 이어서 시작 | 08a | code | 컷 경계에서 배율이 튐 |
| `T-measured-matchcut` | 매치컷 좌표를 실행 중 측정 | 08b PROD | code | 경계에서 앵커 위치가 어긋남 |
| `T-overscale-wipe` | 화면을 채우는 도형은 네 모서리 밖까지 확대 | 08b 와이프 | code / local | 채움 중에 모서리가 비어 보임 |
| `T-text-handoff` | 나가는 글자와 들어오는 글자의 타이밍을 분리 | 08b 타이포 | code / local | 두 문구가 겹쳐 보이는 프레임이 있음 |
| `T-no-pop-in` | 성장·펼침·마스크로 등장하고, 갑자기 튀어나오지 않음 | 08a | code | 0→1 투명도만으로 갑자기 나타남(의도된 하드컷은 예외로 표시) |
| `T-contact-sheet` | 전체 렌더 전에 박자당 한 프레임을 확인 | 08b PROD | code / local | 해당 없음(절차) |
| `T-deterministic` | 상태를 시간 함수로 계산하고 시드 고정 | 08b PROD(기존) | code | 같은 프레임을 다시 렌더했을 때 픽셀이 달라짐 |
| `T-banlist` | 작품별로 템플릿 같은 효과의 금지 목록을 명시 | 08a 아트 디렉션 | 전부 | 금지 목록에 있는 효과가 출력에 나옴 |
| `T-hook-bar` | 첫 마디에 문제를 3~5단어로 제시 | 08b 구조 | 전부 | 첫 2초 안에 주제가 없음 |
| `T-explainer-ladder` | 질문 → 직관 → 예시 → 정리, 레이아웃 고정 | 08b 설명형 | code / local(`diagram_data`) | 설명 중에 레이아웃이 재배치됨 |
| `T-style-as-concept` | 스타일 전환 자체가 개념 설명의 일부 | 08b 설명형 | code | 스타일 전환이 개념과 무관함 |
| `T-shot-per-action` | 한 샷에 동작 하나, 손발 고정, 비율 유지 | 08 캐릭터 | code / local(`pose_swap`) | 비율이 흔들리거나 발이 미끄러짐 |
| `T-3d-gotchas` | 그림자 바이어스, 좁은 near/far, 시드 고정 | realtime-motion-direction | realtime_3d | 그림자 줄무늬, 깊이 깜빡임 |
| `T-inputs-default` | 필요한 입력과 빠졌을 때의 기본값을 한 블록으로 묶음 | 브리프 템플릿 | 전부 | 미승인 자산을 기본값으로 씀 |

### 6.3 분류 원장 `docs/research/prompt-motion-absorption-ledger.csv`

기존 `docs/research/prompt-motion-gallery.tsv`를 **대체**한다(TSV는 삭제하고, 인벤토리 문서의 링크를 갱신).

열: `entry_id`, `variant`, `page_url`, `tags`, `prompt_sha256`, `dup_group`, `format`, `techniques`, `evidence`(`tested`/`original_example`/`template_tested`/`untested`/`skill`), `disposition`(`absorb`/`example`/`reference`/`exclude`), `target`, `reason`, `visual_check`(`pass`/`mismatch`/빈칸).

본문, 번역, GIF 경로는 넣지 않는다. 스냅샷 기준값은 인벤토리 문서에 기록한다: `prompts.csv` sha256 `1bc3b16e…f55e8e`, 450행(원문 234, 개선본 211, 템플릿 2, 스킬 3).

### 6.4 정책 변환표

| 원본 지시 | 패키지에 쓰는 형태 |
|---|---|
| 로고·화면을 사이트에서 가져오거나 직접 캡처 | 승인된 자산만 사용. 없으면 플레이스홀더를 두고 계속 진행 |
| 음악을 코드로 작곡 | 승인된 음원과 큐가 있어야 박자 확정. 없으면 무음 박자표를 시작값으로 |
| 화면·기능·수치를 지어내지 말 것 | 그대로 유지. 근거는 10-evidence로 대조 |
| 묻지 말고 끝까지 빌드 | 비중단 기본값과 마감 계약. 실행·권리·공개 게이트는 유지 |
| BPM·FPS·해상도·배율·홀드의 고정값 | 모두 시작값. 납품 규격은 분석표를 따름 |
| 특정 도구 지시(Playwright, tmix, Web Audio, `will-change`) | 렌더러 중립 문장으로 바꾸고, 실제 실행은 §8 경로로 |
| 설치 명령 | 쓰지 않음. 스킬 3행은 `reference`로 분류 |

### 6.5 문장·출처 규칙

- 원문의 연속 8단어(한국어는 연속 20자) 이상을 그대로 옮기지 않는다.
- 흡수한 절에는 `출처: Prompt Motion <대표 ID 최대 3개> · 근거 <evidence> · 확인 2026-11-23` 한 줄을 붙인다.
- 근거가 `untested`뿐인 기법은 "관찰된 프롬프트 패턴"이라고만 쓴다. "예제에서 확인"이라고 쓰려면 해당 원장 행의 `visual_check=pass`가 필요하다.
- 사이트의 `Content-Signal: ai-train=no, use=reference`를 존중해 링크와 참조로만 사용한다.

## 7. 구현 가능성 매트릭스

정본 위치: `creative-production/references/motion-pipeline.md` M5 절. 행은 레시피와 기법, 열은 `local`, `code`, `realtime_3d`이고 각 칸은 `지원`/`부분(조건)`/`불가`다. 초기값은 다음과 같다.
- **`local`**: CineForge `RECIPES` 목록과 필드 범위만 지원한다(720×1280 9:16, 30fps, 무음 — 데모 C 렌더에서 실측해 정정).
- **`code`**: 2D 기법 전부를 지원한다. 음원은 승인 파일을 다시 합성하는 방식으로만 다룬다.
- **`realtime_3d`**: `open-3d-production`의 범위를 따른다.

CineForge `RECIPES`가 바뀌면 매트릭스도 바뀌어야 한다. 오프라인 테스트가 CineForge 소스의 `RECIPES` 집합과 매트릭스의 `local` 지원 행을 대조한다(CineForge 경로가 없으면 테스트를 건너뜀).

## 8. 코드 렌더 경로

정본 위치: `video-production-assets/references/08b-code-motion-production.md`(신규 절 "코드 렌더 경로"). 도구는 `video-production-assets/scripts/`에 둔다.

### 8.1 작품 계약(코드 작성자가 지킬 것)

- 산출물은 단일 `index.html`과 같은 폴더의 승인 자산뿐이다. 외부 네트워크 요청, CDN, 웹폰트 URL은 허용하지 않는다. 폰트는 로컬 파일이나 시스템 폰트를 쓴다.
- `window.__motion = { width, height, fps, duration, seek(t) }`를 노출한다. `seek(t)`는 시간 `t`(초)만으로 화면 상태를 결정한다. CSS 애니메이션, 타이머, 프레임 간 상태 누적, 시드 없는 난수는 금지한다.
- 레이아웃 측정이 필요한 기법(`T-measured-matchcut`)은 `seek` 안에서 DOM을 측정한다.
- 음향은 HTML 안에서 만들지 않는다. 승인된 음원은 렌더한 뒤 ffmpeg로 합친다.

### 8.2 렌더 도구 `video-production-assets/scripts/render_html_motion.mjs`(의존성 0)

- 입력: `index.html` 경로, 출력 경로, 선택 옵션(`--frames a:b`, `--contact-sheet N`, `--audio approved.wav`, `--chrome PATH`)
- 동작: 설치된 Chrome을 `--headless=new --remote-debugging-port`로 실행하고, Node 24의 내장 WebSocket으로 CDP에 연결한다. 뷰포트를 `width×height`, `deviceScaleFactor=1`로 설정한다. `document.fonts.ready`를 기다린 뒤 프레임마다 `seek(i/fps)`를 호출하고, 다음 애니메이션 프레임 두 번을 기다린 다음 `Page.captureScreenshot`(PNG)으로 캡처한다. 캡처한 PNG를 ffmpeg stdin(`image2pipe`)으로 넘겨 H.264 yuv420p, `+faststart`로 인코딩한다. 음원이 있으면 `-shortest` 없이 길이를 확인한 뒤 합친다(길이가 다르면 실패).
- 결정성 검사: `--verify-frames K`를 주면 무작위가 아닌 고정 프레임 K개를 두 번 캡처해 PNG 해시를 비교한다. 다르면 실패한다.
- 컨택트 시트: `--contact-sheet N`은 균등 간격 N프레임을 하나의 PNG로 만든다(M4·M6 확인용).
- 출력: `render-report.json`(입력 HTML sha256, 프레임 수, fps, 해상도, Chrome 버전, ffmpeg 버전, 출력 sha256, 결정성 검사 결과, 소요 시간)
- 테스트: `video-production-assets/scripts/test_render_html_motion.py`. 작은 HTML 픽스처(0.5초, 12fps, 160×90)를 렌더해 프레임 수, 길이, 결정성, 리포트 필드를 확인한다. Chrome이 없으면 테스트를 건너뛴다.

### 8.3 작성 절차

M4 브리프 → 컷 1개 스파이크(정지 프레임 3장으로 확인) → 전체 `seek` 구현 → 컨택트 시트 확인 → 전체 렌더 → M6 검수. 한 컷의 코드 수정은 같은 HTML 안에서 해당 시간 구간만 고친다.

## 9. CineForge 연결(별도 저장소, 최소 변경)

1. **분석과 선택 기록**: `production_spec.motion_brief`(선택 필드)에 `{analysis, candidates, choice, route_by_cut}`를 둔다. 스키마 검증은 키 존재와 열거값만 확인한다. 기존 `motion_recipe`는 그대로 둔다.
2. **코드 경로 영수증**: `video_cut` 작업에 로컬 무과금 공급자 `code-motion`을 추가한다. 실행 계획에서 비용은 0이고, 외부 전송이 없으므로 유료 승인 대상이 아니다. 다만 G2(프롬프트·브리프 검수) 해시는 기존처럼 요구한다. `cineforge results --stage S08_video --runner code-motion`으로 렌더 결과를 기록하면 기존 영수증과 sha256 고정이 그대로 적용된다.
3. **미리보기 납품 규칙 일치**: 코드 경로 산출물도 사람이 재생 검수(`qa-playback`)를 한 해시로만 납품한다.
4. CineForge 테스트: 새 공급자 허용, 영수증 기록, 미승인 해시 거부, 기존 테스트 회귀

이 변경 없이 스킬만 반영하면, 코드 경로 산출물은 CineForge 밖의 단독 산출물로만 납품할 수 있다. 계획에서는 CineForge 변경을 스킬 반영과 같은 단계에 묶는다.

## 10. 저장소 반영 지도

| 파일 | 변경 |
|---|---|
| `creative-production/references/motion-pipeline.md` | **신규**. M1~M6, 분석표, 후보 비교, 구현 매트릭스, 다운그레이드 규칙. 기존 motion-selection의 레시피 표를 흡수 |
| `creative-production/references/motion-selection.md` | 한 줄 리다이렉트로 축소(기존 링크 보존) |
| `creative-production/SKILL.md` | Step 1의 모션 문장을 M1 트리거로 교체. frontier 단어 상한 2,900 유지(늘어나는 만큼 다른 문장을 policy로 이동) |
| `creative-production/references/craft-bridge.csv` | 08b 행의 비고에 브리프 템플릿과 렌더 도구를 추가. motion-pipeline 행 1개 추가 |
| `video-production-assets/references/08b-code-motion-production.md` | 형식별 구조, 코퍼스 기법 절, 코드 렌더 경로 절. +120줄을 넘으면 형식 절을 `08c-code-motion-formats.md`로 분리 |
| `video-production-assets/references/08a-motion-craft.md` | `T-camera-handoff`, `T-no-pop-in`, `T-banlist` |
| `video-production-assets/assets/code-motion-brief-template.md` | **신규** 6칸 템플릿 |
| `video-production-assets/scripts/render_html_motion.mjs`, `test_render_html_motion.py` | **신규** |
| `video-production-assets/SKILL.md`, `module-index.md` | 08b 행에 브리프·렌더 도구 포인터 |
| `open-3d-production/references/realtime-motion-direction.md` | `T-3d-gotchas` |
| `docs/research/prompt-motion-absorption-ledger.csv`, `scripts/prompt_motion_ledger.py` | **신규** 원장과 생성·대조 도구. `prompt-motion-gallery.tsv` 삭제 |
| `docs/research/prompt-motion-inventory.md` | 스냅샷, 드리프트, 원장 링크 |
| `scripts/test_prompt_motion_corpus.py`, `scripts/test_motion_pipeline.py` | **신규** 오프라인 테스트 |
| `creative-production/evals/agent-read-probes.json` | 프로브 4건 추가 |
| 버전·CHANGELOG | video-production-assets 1.34, creative-production 2.8, open-3d-production 1.2, 패키지 2.64 |

## 11. 작업 단계

1. **기준선(RED)**: §12의 프로브를 현재 패키지로 실행하고 결과를 `qa/2026-11-23-motion-pipeline/baseline/`에 기록한다.
2. **원장**: 생성 스크립트로 키·해시·묶음·근거를 채운다. 대표 행(원문 203, 개선본 158)에 형식과 기법을 수동으로 코딩하고 처분을 판정한다.
3. **시각 확인**: `absorb`의 근거 예제와 형식별 대표 2개씩의 GIF로 컨택트 시트를 만들어 `visual_check`를 기록한다.
4. **렌더 도구**: 테스트를 먼저 작성하고, `render_html_motion.mjs`를 구현한다.
5. **파이프라인 문서**: motion-pipeline, 브리프 템플릿, 08b·08a·realtime 반영. `creative-production` Step 1을 교체한다.
6. **CineForge**: `motion_brief` 필드와 `code-motion` 공급자를 테스트 먼저 방식으로 구현한다.
7. **실제 렌더 시연(GREEN)**: 형식 3개(`product_film` 16:9 30초, `explainer` 9:16 20초, `showreel` 9:16 15초)를 가상 브랜드와 플레이스홀더 자산으로 M1~M6 전 과정을 거쳐 MP4로 렌더한다. 결과는 `~/Documents/Media_Studio/motion-pipeline-demo-*/`에 두고 저장소에는 넣지 않는다. 그중 1개는 `local`과 `code` 혼합 컷으로 만든다.
8. **프로브 재실행과 회귀**: 전체 pytest(양쪽 저장소), `check_versions.py`, `routing_regression.py`
9. **마감**: 인벤토리, 버전, CHANGELOG, `sync_installed`. 커밋과 푸시는 사용자 확인 후 진행한다.

## 12. 검증

**오프라인 테스트(이 저장소)**
- 원장: 450행, 고유 키, 열거값 유효, 변형별 개수, `target` 앵커 존재, `reason` 필수, 기법 정본이 정확히 한 곳(중복 0), `untested`만 근거인 기법 절에 효과 주장 표현 없음
- 위생: 저장소에 `*.gif`, 프롬프트 CSV, `<direction>` 블록, 설치 명령 문자열이 없음
- 파이프라인 문서: M1~M6 절, 분석표 필수 칸 11개, 후보 평가 기준 4개, 다운그레이드 기록 규칙, 매트릭스의 `local` 행과 CineForge `RECIPES` 일치
- 브리프 템플릿 6칸, 렌더 도구 테스트

**선택적 원문 대조**: `scripts/prompt_motion_ledger.py --verify ARCHIVE`로 스냅샷 해시를 확인하고, 반영 문서에 원문의 연속 8단어 이상이 없는지 확인한다.

**실제 렌더 증거(§11-7)**: 산출물마다 `render-report.json`, 결정성 검사 pass, 컨택트 시트, M6 체크리스트 판정, 다운그레이드 기록이 있어야 한다. 이 증거가 없으면 완료로 보지 않는다.

**행동 프로브**(기존 9건 유지, 4건 추가)
- `pm1` "앱 출시 30초 모션그래픽 영상 만들어줘" → motion-pipeline을 열고, 분석표 11칸, 후보 2개 이상, 주인공 객체가 담긴 브리프, 컷별 경로 판정이 나옴
- `pm2` "재귀를 설명하는 모션 영상" → `explainer` 형식과 `diagram_data` 또는 code 경로, `T-explainer-ladder` 구조
- `pm3` "실사 카페 광고 30초, 마지막에 가격표 애니메이션" → 가격표 컷만 모션 파이프라인을 타고, 나머지는 실사 경로를 유지
- `pm4`(부정) "실사 인터뷰 영상 편집 계획" → motion-pipeline을 열지 않음

통과 기준: 양성 3건이 각각 3회 중 3회, 부정 1건이 3회 중 3회. 하니스가 동작하지 않으면 BLOCKED로 기록한다.

## 13. 위험과 대응

| 위험 | 대응 |
|---|---|
| `creative-production` frontier 단어 상한 초과 | 모션 문장은 한 줄 트리거와 링크만 남기고, 나머지는 motion-pipeline으로 이동 |
| 헤드리스 Chrome의 폰트·GPU 차이로 결정성이 깨짐 | `--disable-gpu`와 고정 DPR, 로컬 폰트만 사용. 결정성 검사를 필수로 |
| 긴 영상의 캡처 시간 | 컷 단위 렌더와 `--frames` 구간 재렌더. 소요 시간은 리포트에 기록 |
| CineForge 변경이 늦어짐 | 스킬 쪽 코드 경로는 단독으로도 동작함. 이 경우 CineForge 납품 연결을 미완료로 보고하고 완료라고 주장하지 않음 |
| 쇼릴 반복이 원장을 지배 | `dup_group` 단위로 집계 |
| 사이트 드리프트 | 스냅샷 해시를 고정하고, 재수집 시 차이를 보고 |

## 14. 구현자 재량

문장 표현, 표 순서, 앵커 이름, 대표 출처 ID, 08c 분리 시점(상한 안에서), 시연용 가상 브랜드와 문구는 구현자가 정한다.

## 15. 셀프 빌더 체크(서브에이전트 미승인으로 직접 확인)

- 반영함: 렌더 도구의 의존성(설치된 Chrome, Node 24, FFmpeg로 충분함을 확인), CineForge 연결 지점(`video_cut` 공급자 목록, `record_results` 영수증), local 레시피 목록(`local_motion.RECIPES`)
- 설계자가 정한 것: 코드 경로는 HTML + `seek(t)` 계약(Remotion 미설치 상태에서 설치 없이 실행할 수 있는 방식). 로컬 코드 렌더는 유료·외부 실행이 아니므로 지출 승인 대상이 아니지만, G2 검수와 재생 검수 해시 납품은 유지
- 사용자가 결정할 것: 없음
