# Kinetic Still Staging, Facial Mechanics, Single-Frame Causal Readability, and Pipeline Upgrade Design

**Date:** 2026-11-15
**Status:** Approved Execution Design (v2.36 Upgrade)
**Scope:** `contents-production-skills` 코어 스킬 계약(`storyboarding-video`, `video-production-assets`, `camera-spatial-design`, `designing-video-character-sheets`, `orchestrating-video-preproduction`, `creative-production`), 검증/렌더러 스크립트(`validate_storyboard.py`, `render_storyboard_sheet.py`), 템플릿·CSV 스키마 및 레포지토리 패키징 구조.

## 1. 배경 및 핵심 문제 진단 (Executive Summary)

현재 `contents-production-skills` (v2.35) 패키지는 프로젝트 원장(`project.json`)의 ID 추적성, 에셋 버전 핀(`asset_version_refs`), 사후 구조/시각 검수(QA 게이트) 측면에서 매우 견고하게 설계되어 있다. 그러나 실제 제작 공정에서 **컷별 정지 이미지(Key Panel Stills)를 먼저 생성해 씬을 구성할 때** 다음과 같은 구조적 병목이 발생한다.

1. **패널(`panel`) 단위의 연출·표정·프롬프트 스키마 부재**: `validate_storyboard.py`의 `PANEL_TEXT_KEYS`가 `visual_action`, `reveals`, `withholds`, `continuity` 4개만 다루며, 개별 컷 프롬프트(`image_prompt`), 안면 표정·동세(`expression_pose`), 시선 유도 위계(`focal_hierarchy`), 정지화 역동성 단서(`kinetic_cues`)가 스키마에서 누락되어 있다.
2. **정지 이미지 내 역동성·스피드 표현의 과도한 억제**: `storyboard-contract.md` §3–4의 *"그 순간 보이는 상태만 묘사한다"*, *"모션 블러만으로 동작 장면이라고 간주하지 않는다"*라는 방어 규정이 AI가 동세선(Line of Action), 포어쇼트닝(Foreshortening), 2차 물리 관성(휘날리는 의상·머리카락·먼지·스파크·방향성 블러)을 프롬프트에서 제거하도록 유도해 마네킹 같은 정적 이미지를 만든다.
3. **카메라 카탈로그의 정적 구도 편향**: `camera-language-catalog.md` §C의 예시 비율(아이레벨 70%, 고정 카메라 60%, MS/MCU 50%)이 기본값처럼 작동하여 액션·추격·위기 씬에서도 광각(14–24mm)·로우/더치 앵글·WS↔ECU 스케일 점프가 생략된다.
4. **연기 동사(`04-performance.md`)와 이미지 생성기 간의 해부학적 단절**: `"설득한다"`, `"주의를 얻는다"` 같은 타동사 지시는 정지 이미지 생성기(`codex-imagen`)가 시각화할 수 없으며, 캐릭터 SSOT §10(`Expression DNA`)의 안면 근육·시선 규칙을 패널 프롬프트로 끌어오는 브릿지가 없다.
5. **단일 프레임 상황 직관성(Single-Frame Causal Readability) 공식 부재**: `narrative-panels.md`의 1패널 1행동 원칙이 전경(원인·위협)·중경(주체 행동·표정)·배경(환경 맥락·결과 흔적)의 3단 레이어 압축을 생략하게 만들어 이미지 한 장만으로 전후 맥락을 이해하기 어렵다.
6. **파이프라인 연쇄 병목 (6대 추가 과제)**:
   - **I2V 키프레임 체이닝 불일치**: `validate_storyboard.py`가 모든 변화 샷에 `start`+`end` 2장 이상을 강제하여 1~2초 단발 액션 컷의 단일 키프레임(`start` 또는 `action_peak`) 구성을 막고, 복합 액션 컷의 `start→peak` / `peak→end` FLF2V 분할 규칙이 없다.
   - **시트 렌더러(`render_storyboard_sheet.py`)의 `560×560` 정방형 고정**: 9:16 쇼츠나 16:9 와이드 프로젝트에서도 정방형 셀을 강제해 여백 낭비와 디테일 축소가 발생하며, `CAPTION_MAX_LINES = 40` 제한으로 상세 연출 캡션 작성 시 렌더링이 실패한다.
   - **행정 메타데이터 과부하(Context Bloat)**: 2,000단어 제한 안에 6개 대형 관리 표를 강제해 정작 창작 연출·프롬프트 문장이 단답형으로 축약된다.
   - **한·영 프롬프트 정책 충돌**: 한국어 전용 규칙(`narrative-panels.md`)과 영어 전용 규칙(`higgsfield-video-replicate`)이 충돌하며 시네마틱 촬영·렌즈·표정 토큰이 손실된다.
   - **물리 재질 기반 SFX 및 타격점 동기화 부재**: 추상적 효과음 서술로 인해 과장된 폭발음 오생성이 발생하며, `action_peak` 패널과 오디오 타격점(`sync_anchor`)의 1:1 시각-청각 동기화가 약하다.
   - **배포 패키지 용량 비대화**: `manifest.json`에서 제외된 비영상 스킬 폴더 4종과 대규모 과거 QA/픽스처 로그가 패키지에 잔존한다.

## 2. 아키텍처 및 상세 설계 (Target Architecture)

### 2.1 단일 프레임 3단 상황 압축 및 정지화 역동성 변환 (Kinetic Still Translation)

정지 이미지 한 장만으로 전후 인과관계와 속도감·박진감이 직관적으로 읽히도록 `storyboard-contract.md` §3–4와 `narrative-panels.md`, `08-animation.md`에 다음 설계 공식을 도입한다.

| 설계 축 | 필수 구성 요소 | 프롬프트 및 패널 명세 반영 규칙 |
|---|---|---|
| **3단 레이어 상황 압축 (`focal_hierarchy`)** | **1순위(전경/주점)** + **2순위(중경/상호작용)** + **3순위(배경/맥락)** | 단일 프레임 안에 ① **원인/위협/목표물**(전경 가림·실루엣·포어쇼트닝 소품), ② **주체의 핵심 행동·표정·접촉**(중경 초점), ③ **장소 상태·시간·직전 행동의 잔류 흔적**(배경 맥락)을 함께 배치해 대사 없이 상황을 직관화 |
| **정지화 역동성 단서 (`kinetic_cues`)** | **동세선(Line of Action)** + **포어쇼트닝** + **2차 물리 관성** | 수직 기립 정자세 금지; 추진/충돌 방향으로 기울어진 C/S자 척추 동세선, 렌즈 코앞까지 뻗는 원근 과장(14–24mm 광각), 관성으로 뒤집히는 옷자락·머리카락·지면 먼지·파편·방향성 스피드 블러 명시 |
| **안면 해부학·신체 긴장 (`expression_pose`)** | **눈·시선 벡터** + **눈썹·미간** + **입·턱** + **목·어깨 텐션** | `"긴장한"`, `"설득한다"` 등 추상어 단독 사용 금지; 캐릭터 SSOT §10(`Expression DNA`)과 연동해 동공/흰자위 노출, 비대칭 미간 주름, 악문 턱/벌어진 입술, 승모근·손끝 경직도를 구체적 시각 단어로 변환 |
| **컷 간 시선·스케일 흐름 (`cut_to_next`)** | **스케일 점프(Scale Contrast)** + **아이트레이스(Eye-Trace)** | 동일 샷 크기 연속 나열 지양(`WS → ECU → Low-Angle FS → CU`); 앞 컷의 시선·운동 벡터가 도달한 화면 구역에서 다음 컷의 핵심 피사체/반응이 시작되도록 연결 |

### 2.2 한·영 이중 프롬프트(Dual-Layer Prompt) 표준

모든 패널(`storyboard.panels[]`)과 샷 인계(`11-ai-handoff-template.md`)의 프롬프트는 사용자 직관 검수와 생성 엔진의 시네마틱 재현력을 동시에 확보하기 위해 다음 이중 구조를 사용한다.

- **`[KO 연출 직관 요약]`**: 한국어 사용자가 1초 만에 컷의 상황·감정·동세·인물 관계를 이해할 수 있는 직관적 연출 묘사(1~2문장).
- **`[EN 시네마틱 생성 프롬프트]`**: 이미지/영상 생성 엔진(`codex-imagen`, Seedance, Kling 등)의 광학·해부학·물리 토큰 이해도를 극대화하는 구조화 영문 프롬프트(`Shot Scale/Angle + Lens/Depth + Subject/Anatomical Expression/Line of Action + Foreground/Midground/Background Causal Layers + Kinetic Secondary Physics + Lighting/Palette`).

### 2.3 I2V 키프레임 체이닝 브릿지 및 검증기(`validate_storyboard.py`) 확장

1. **단발 액션·급전환 샷의 1패널(`start` 또는 `action_peak`) 허용**:
   - 기존 `validate_storyboard.py`는 변화 샷에 반드시 `start`와 `end` 패널이 모두 존재해야 통과시켰으나, 2초 이하의 빠른 액션 컷이나 타격 순간으로 바로 컷인(Cut-on-Action)하는 샷은 단일 `start` 패널(프레임 `start_s`) 또는 단일 `action_peak` 패널만으로도 구조 검증을 통과하도록 허용한다.
2. **복합 액션 샷의 FLF2V(`--start-image` / `--end-image`) 서브클립 분할 매핑**:
   - `start → action_peak → end` 3패널로 구성된 복합 궤적 샷을 I2V 모델로 넘길 때는 ① `start → action_peak`(전반부 가속/접촉 서브클립)와 ② `action_peak → end`(후반부 반동/정착 서브클립)로 분할 체이닝하거나, `action_peak`를 히어로 `--start-image`로 고정하는 의사결정 규칙을 `11-ai-handoff.md`와 `storyboard-timing-to-prompt.md`에 명문화한다.
3. **패널 스키마 확장 (하위 호환 유지)**:
   - `storyboard-panels.csv` 및 `storyboard-contract.md` §8의 패널 필드에 `expression_pose`, `focal_hierarchy`, `kinetic_cues`, `image_prompt`를 정식 지원하며, `validate_storyboard.py`에서 이 확장 필드들이 존재할 경우 빈 문자열이 아닌지 검증(기존 최소 픽스처와의 하위 호환성을 위해 선택적 비공백 검증 `OPTIONAL_PANEL_TEXT_KEYS` + `--strict-staging` 옵션 제공)한다.

### 2.4 화면비 연동 스토리보드 시트 렌더러(`render_storyboard_sheet.py`) 개선

1. **프로젝트 화면비(`aspect_ratio`) 기반 가변 셀 크기 계산**:
   - `project.json`의 `aspect_ratio`(또는 `format.delivery_resolution`)를 읽어 셀 크기를 동적으로 설정한다:
     - `9:16` (세로형 쇼츠): `405 × 720` (세로 구도와 상하 공간감 보존, 좌우 불필요 여백 제거)
     - `16:9` (가로형 표준): `640 × 360` (가로 시네마틱 구도 보존 및 시트 가로 밀도 최적화)
     - `4:5` / `3:4`: `480 × 600`
     - `1:1` 또는 미지정 폴백: 기존 `560 × 560` 유지 (기존 단위 테스트와 100% 호환)
2. **캡션에 확장 연출 필드(`expression_pose`, `focal_hierarchy`, `kinetic_cues`, `image_prompt`) 표시 및 `CAPTION_MAX_LINES` 상향**:
   - `CAPTION_MAX_LINES`를 기존 `40`에서 `64`로 상향하여 상세한 액션·표정·이중 프롬프트 캡션이 잘리거나 에러를 일으키지 않도록 개선한다.

### 2.5 창작 컨텍스트 경량화(Creative Staging Mode) 및 물리 재질 SFX 동기화

1. **창작 집중 모드(`Creative Staging Mode`) 분기 (`orchestrating-video-preproduction/SKILL.md`, `storyboard-contract.md`)**:
   - 사용자가 컷별 이미지 구상·액션 연출·콘티 초안을 요청할 때는 행정적인 6개 대형 표와 도서 출처 해시 나열을 생략하고, **토큰의 80% 이상을 컷별 3단 구도·동세·안면 표정·한/영 프롬프트에 집중**하도록 응답 밀도 규칙을 개편한다.
2. **물리 재질 기반 SFX 프롬프트 공식 (`09-edit.md`, `edit-sound-language-catalog.md`)**:
   - 효과음 설계 시 `"강렬한 충돌음"`, `"SF 폭발음"` 같은 추상적 장르어를 금지하고, 반드시 **`[접촉 주체 재질] + [대상 표면 재질] + [접촉 방식(마찰/압착/타격/미끄러짐)] + [질량감·잔향(Decay)]`** 공식으로 기술하며 `action_peak` 패널의 시각적 접촉 부위와 1:1로 동기화한다.

## 3. 검증 및 완료 기준 (Acceptance Criteria)

1. 코어 스킬 마크다운 문서 12종 및 템플릿/CSV가 상호 모순 없이 업데이트되고 내부 상대 경로 링크가 100% 유효해야 한다.
2. `validate_storyboard.py`와 `render_storyboard_sheet.py`의 기존 단위 테스트(`test_validate_storyboard.py`, `test_render_storyboard_sheet.py`, `test_split_storyboard.py`, `test_validate_project.py`)가 모두 통과하고, 신규 기능(단발 액션 1패널 허용, 확장 스테이징 필드 검증, 화면비 연동 셀 크기 계산) 테스트가 통과해야 한다.
3. 패키지 버전(`manifest.json` 및 수정 스킬 버전)이 `check_versions.py`와 `test_video_pack_boundary.py`를 통과해야 한다.
