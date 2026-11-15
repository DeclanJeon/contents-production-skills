# Work Order: Kinetic Still Staging, Facial Mechanics, Single-Frame Readability & Pipeline Upgrade (v2.36)

**Design Spec:** `docs/superpowers/specs/2026-11-15-kinetic-staging-and-pipeline-upgrade-design.md`
**Target Package:** `contents-production-skills` (v2.35 → v2.36)
**Execution Mode:** 단계별 진행률(%) 추적 기반 전수 패치 및 자동 검증

## 1. 작업 목표 (Objective)

컷별 정지 이미지 생성 단계에서 액션·박진감·스피드·인물 표정·단일 프레임 상황 직관성이 떨어지는 문제를 근본적으로 해결하고, I2V 키프레임 브릿지·화면비 연동 시트 렌더러·한/영 이중 프롬프트·물리 재질 SFX 동기화·패키지 슬림화를 일괄 구현한다.

## 2. 단계별 작업 지시 및 진행률 배분 (Work Breakdown & Progress Weights)

| 단계 | 작업 묶음 (Work Package) | 대상 파일 | 진행률 가중치 | 누적 진행률 |
|---|---|---|---|---|
| **WP-01** | 설계문서 및 작업지시서 수립·고정 | `docs/superpowers/specs/2026-11-15-...-design.md`, `docs/superpowers/plans/2026-11-15-...-work-order.md` | 15% | **15%** |
| **WP-02** | 스토리보드 코어 계약 및 단일 프레임 3단 직관화·역동성 변환 패치 | `video-production-assets/references/storyboard-contract.md`, `storyboarding-video/SKILL.md`, `storyboarding-video/references/narrative-panels.md` | 20% | **35%** |
| **WP-03** | 안면 해부학 표정 브릿지 및 동세·카메라 스케일 점프 레시피 패치 | `video-production-assets/references/04-performance.md`, `06-shots.md`, `08-animation.md`, `camera-spatial-design/references/camera-language-catalog.md` | 20% | **55%** |
| **WP-04** | I2V 키프레임 체이닝·한/영 이중 프롬프트·경량 연출 모드·물리 SFX 패치 | `video-production-assets/references/09-edit.md`, `11-ai-handoff.md`, `edit-sound-language-catalog.md`, `creative-production/references/storyboard-timing-to-prompt.md`, `orchestrating-video-preproduction/SKILL.md` | 15% | **70%** |
| **WP-05** | 템플릿·CSV 스키마 및 예제 프로젝트(`20-second-animation`) 고도화 | `video-production-assets/assets/storyboard-panels.csv`, `06-shots-template.md`, `11-ai-handoff-template.md`, `examples/20-second-animation/project.json` | 10% | **80%** |
| **WP-06** | 파이썬 검증기(`validate_storyboard.py`) 및 시트 렌더러(`render_storyboard_sheet.py`) 코드 업그레이드 | `video-production-assets/scripts/validate_storyboard.py`, `render_storyboard_sheet.py`, 관련 단위 테스트 | 10% | **90%** |
| **WP-07** | 레거시 비영상 폴더·대용량 QA 로그 정리, 전체 테스트 검증 및 클린 패키징 | `manifest.json`, `CHANGELOG.md`, 전체 `unittest` 실행 및 최종 `.zip` 아카이브 생성 | 10% | **100%** |

> **WP-07 범위 조정 (2026-11-15)**: ZIP 아카이브 생성과 저장소 내 비영상 폴더 삭제는 **하지 않는다**. 근거: (1) Git 저장소 자체가 배포 채널이므로 중복 아카이브는 드리프트 원인이다. (2) `higgsfield-brandkit`/`higgsfield-websites` 등 4종은 여전히 유효한 스킬이며 추적 중인 파일을 지우면 이력 손실이다. (3) 비영상 형제 스킬의 미설치 처리는 이미 `scripts/sync_installed.py`가 담당한다. 대신 전체 테스트 통과와 버전·매니페스트 정합으로 패키징을 완료 판정한다.

## 3. 작업 묶음별 상세 지시사항 (Detailed Instructions per Work Package)

### WP-02: 스토리보드 코어 계약 및 단일 프레임 직관화 (`15% → 35%`)
- **`video-production-assets/references/storyboard-contract.md`**:
  - §3 `동작 중심 패널의 장면 통합`에 **[단일 프레임 3단 상황 압축(Fore/Mid/Background Causal Framing)]**과 **[정지화 역동성 변환(Kinetic Still Translation: C/S자 동세선, 광각 포어쇼트닝, 2차 물리 관성)]** 규칙을 추가한다.
  - §4의 *"이미지 프롬프트는 그 순간 보이는 상태만 묘사한다"*를 **"그 순간의 물리적 상태와 함께 운동 에너지·속도 벡터·안면 근육 긴장·3단 공간 인과가 정지 픽셀 안에서 즉각 읽히도록 묘사한다"**로 개편한다.
  - §8 `panels[]` 스키마에 선택적 고도화 필드 `expression_pose`(안면 해부학 표정 및 전신 동세), `focal_hierarchy`(1순위 초점 → 2순위 상호작용 → 3순위 배경 맥락), `kinetic_cues`(속도감·물리 관성 단서), `image_prompt`(한·영 이중 프롬프트)를 정의한다.
- **`storyboarding-video/SKILL.md` & `references/narrative-panels.md`**:
  - `Composing each panel`에 1패널 1행동이 '배경·원인 삭제'가 되지 않도록 **시각적 인과 앵커(원인 흔적 + 주 행동 + 상대/목표물 반응)** 규칙과 **컷 간 아이트레이스(Eye-Trace) 및 샷 스케일 점프** 규칙을 추가한다.
  - 패널 표 출력 양식에 `표정·동세(expression_pose)`, `시선 위계·3단 레이어(focal_hierarchy)`, `한·영 이중 이미지 프롬프트(image_prompt)`를 반영한다.

### WP-03: 안면 해부학 표정 브릿지 및 카메라 액션 레시피 (`35% → 55%`)
- **`video-production-assets/references/04-performance.md`**:
  - 배우용 타동사 지시(`설득한다`, `주의를 얻는다`)를 이미지/영상 생성용 **안면 해부학(눈동자/흰자위 노출·시선 각도, 미간/눈썹 비대칭 수축, 입꼬리/턱 근육 긴장) + 신체 텐션(목·승모근·어깨·손끝)**으로 변환하는 `정지 이미지·AI 생성용 표정·신체 변환 브릿지` 절을 신설한다.
- **`video-production-assets/references/06-shots.md` & `08-animation.md`**:
  - 액션·추격·위기 씬에서 평면적 구도 반복을 막는 **샷 스케일 낙차(WS↔ECU, Low/Dutch Angle)** 규칙과 C/S자 동세선·무게중심 붕괴(Off-balance forward lean)·오버슈트 정착 규칙을 보강한다.
  - **범위 제한**: 두 문서는 **컷 설계 원칙** 문서이며 패널 스키마 문서가 아니다. `kinetic_cues`, `expression_pose`, `image_prompt` 슬롯의 정의·양식·검증은 WP-02(`storyboard-contract.md` §8)·WP-05(템플릿·CSV)·WP-06(`validate_storyboard.py`)이 소유한다. 따라서 이 두 문서에 세 필드가 없는 것은 미완료가 아니다. 근거는 설계문서 §2.1.1(소유 문서 경계)을 따른다.
- **`camera-spatial-design/references/camera-language-catalog.md`**:
  - §C의 예시 배분(아이레벨 70%, 고정 60%)이 액션·박진감 씬의 기본값으로 오용되지 않도록 경고문을 강화하고, §D에 **액션·추격·타격·서스펜스 전용 컷 연결 레시피 4종**(추격 속도감, 근접 타격 임팩트, 급박한 위기/발견, 고속 전환 휩팬/스매시컷)을 추가한다.

### WP-04: I2V 브릿지·한/영 이중 프롬프트·경량 모드·물리 SFX (`55% → 70%`)
- **`video-production-assets/references/11-ai-handoff.md` & `creative-production/references/storyboard-timing-to-prompt.md`**:
  - `start / action_peak / end` 패널을 I2V 모델(`--start-image`, `--end-image`)로 넘길 때 단발 컷(1~2초)의 단일 프레임 앵커링과 복합 궤적 컷의 `start→peak` / `peak→end` 서브클립 분할 체이닝 규칙을 추가한다.
- **`orchestrating-video-preproduction/SKILL.md`**:
  - `Multi-artifact plan response shape`에 **창작 연출 집중 모드(Creative Staging Mode)** 분기를 추가하여, 초기 콘티·컷별 이미지 기획 시 관리용 중복 표를 줄이고 시각 묘사·표정·프롬프트에 토큰의 80% 이상을 배정하도록 개선한다.
- **`video-production-assets/references/09-edit.md` & `edit-sound-language-catalog.md`**:
  - 추상적 효과음 명칭 대신 **`[주체 재질] + [대상 재질] + [접촉/마찰 방식] + [무게·잔향]`**으로 SFX를 설계하는 물리 재질 규칙과 `action_peak` 시각 타격점 동기화 규칙을 추가한다.

### WP-05: 템플릿·CSV 및 예제 프로젝트 업그레이드 (`70% → 80%`)
- `video-production-assets/assets/storyboard-panels.csv`, `06-shots-template.md`, `11-ai-handoff-template.md`에 확장 필드(`expression_pose`, `focal_hierarchy`, `kinetic_cues`, `image_prompt`)와 한·영 이중 프롬프트 양식을 반영한다.
- `examples/20-second-animation/project.json` 및 `production-plan.ko.md`의 추격/발견 샷(`SH01`, `SH03`, `SH04`)에 광각·로우앵글·동세선·표정 디테일 주석을 보강한다.

### WP-06: 검증기 및 시트 렌더러 파이썬 스크립트 업그레이드 (`80% → 90%`)
- **`video-production-assets/scripts/validate_storyboard.py`**:
  - `OPTIONAL_PANEL_TEXT_KEYS = ('expression_pose', 'focal_hierarchy', 'kinetic_cues', 'image_prompt')`를 추가해 필드가 존재할 경우 비어 있지 않은 문자열인지 검증하고, `--strict-staging` 플래그 사용 시 해당 필드들을 필수로 검사한다.
  - 변화 샷에서 `len(rows) == 1`이고 `role in ('start', 'action_peak')`인 단발 액션 키프레임 구성을 허용하도록 검증 로직을 확장한다.
- **`video-production-assets/scripts/render_storyboard_sheet.py`**:
  - `_cell_dimensions(project)` 헬퍼를 추가해 `project.aspect_ratio`가 `9:16`일 때 `405×720`, `16:9`일 때 `640×360`, `4:5`일 때 `480×600`, 기본/미지정(`1:1` 등)일 때 `560×560`을 반환하도록 구현한다.
  - `CAPTION_MAX_LINES`를 `64`로 확장하고, 패널에 `expression_pose`, `focal_hierarchy`, `kinetic_cues`, `image_prompt`가 있으면 캡션과 traceability 메타데이터에 포함시킨다.

### WP-07: 레거시 정리·전체 검증 및 패키징 (`90% → 100%`)
- `test_validate_storyboard.py`와 `test_render_storyboard_sheet.py`에 신규 기능 단위 테스트를 추가하고 전체 테스트를 실행한다.
- 패키징은 **버전·매니페스트 정합 + 전체 테스트 통과**로 판정한다. 배포용 ZIP 생성과 비영상 폴더 삭제는 위 범위 조정에 따라 제외한다.
