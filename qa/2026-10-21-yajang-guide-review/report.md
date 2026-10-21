# '야장시단' 제작 가이드북 대조 검토 + Blender 실행 검증 (2026-10-21)

## 1. 범위와 입력

| 입력 | 실제 확인 방식 | 확인 범위 |
|---|---|---|
| `~/Documents/AI 숏드라마 '야장시단' 제작 가이드북_20261020.pdf` (101p, 텍스트 레이어 없음) | `pdftoppm`로 페이지 이미지 렌더 후 육안 판독 | 표지·목차(2p), 3·5·9–16·22–25·56–64·72–83p. 나머지 장은 제목·소제목만 스캔 |
| `KakaoTalk_20261018_192654918*.jpg` (3p) | 육안 판독 | 카메라 연출 비율·구도 24·움직임/전환 24 카드 |
| 스킬 패키지(26 skills) | 파일 읽기 + 실행 | `camera-spatial-design`, `blender-previsualization`, `ai-camera-control`, `camera-motion-reference-analysis`, `video-production-assets`(스토리보드 계약·참조 R1·상태 인계), `higgsfield-generate` |

가이드북은 텍스트 추출이 불가해 이미지 판독으로만 읽었다. 인용은 **장/쪽 단위**로만 적었고, 판독이 불확실한 항목은 그렇게 표시했다.

## 2. Blender 실행 검증 (실제 수행)

가이드북 14화(60–62p)는 이 패키지의 `blender-previsualization` 산출물(실제 Blender 프리비즈 프레임)을 그대로 인용하고 있어, 어댑터가 지금도 재현되는지 확인했다.

| 실행 | 명령 | 결과 |
|---|---|---|
| 런타임 | `blender --version` | Blender 5.2.2 LTS (`/home/declan/.local/bin/blender`, build 2026-09-15) |
| 수치 검사 | `python3 camera-spatial-design/scripts/spatial_spec.py <spec> --out analysis.json` | `valid: true`, SH01/SH02 분석 산출 |
| 단위 테스트 | `test_spatial_spec.py` / `test_build_previs.py` | 14 OK / 13 OK (figure proxy 테스트 4건 추가) |
| 실제 Blender 통합 | `BLENDER_EXECUTABLE=<blender> python3 blender-previsualization/scripts/test_camera_orientation_in_blender.py` | 1 OK (실제 Blender 실행) |
| smoke | `blender --background --factory-startup --python build_previs.py -- --spec … --mode smoke` | 320×180 1프레임, 약 2초, `status: generated` |
| stills | 동일 `--mode stills` | 2샷 × 시작/중간/끝 6PNG + `previs.blend` + `numerical-analysis.json` + `blender-inspection.json` + `manifest.json`, 약 12초 |
| figure proxy | 동일 `--mode stills --proxy figure` | 6PNG, 약 20초, `manifest.proxy_mode: figure` |
| 렌더 맵 | `--render-map '{"SH01":[0,24,47]}'` | 지정 샷·로컬 프레임만 렌더, 지도 밖 샷 거부 확인 |
| 육안 검수 | 생성 PNG 4장 직접 열어 확인 | box 모드: 2인물 배치·SH02 돌리인 프레이밍 정상. figure 모드: 머리·눈높이·실루엣이 사람 형태로 읽힘 |

**MCP 관련 확인:** 이 호스트의 Pi(`~/.pi/agent/mcp.json`)는 `higgsfield`, `momcalendar`만 등록되어 있고, Codex(`~/.codex/config.toml`)에도 Blender MCP 서버가 없다. 파일시스템 전체를 `*blender*mcp*`로 검색해도 설치본이 없다. 즉 **사용자가 말씀하신 "블렌더 MCP"는 이 시스템에 설치되어 있지 않다.** 이 스킬은 애초에 MCP가 필요 없으며 `blender --background --python` CLI로 구동된다. MCP 표면을 쓰려면 같은 명세로 `.blend`·샷별 PNG·`numerical-analysis.json`·`blender-inspection.json`·`manifest.json`을 만들 수 있어야 인정된다(스킬 SKILL.md 2단계에 명시).

## 3. 가이드북 ↔ 스킬 대조 결과

### 3.1 이미 일치하는 것 (수정 불필요)

| 가이드북 관찰 | 대응 스킬 위치 |
|---|---|
| 3장 90초 3구간(소개/시도/변화), "컷마다 새 정보가 있어야" | `camera-language-catalog` 공통 설계 원칙 + C2(추가) |
| 14장 "카메라 이동을 먼저 고르고 이유를 나중에 붙이지 않는다" | `camera-spatial-design/SKILL.md` 실행 3·6, `storyboard-contract.md` 씬별 카메라 의도 |
| 17장 참조 역할(외형/환경/효과 분리) | `video-production-assets/references/29-reference-driven-production.md` R1 + `ai-camera-control` control-contract |
| 17·18장 상태 변화·보존·인계 | `26-state-causality-continuity.md` (변화/보존/결합/생략 슬롯) |
| 14장 "프리비즈는 최종 영상이 아니다" | `blender-previsualization` Acceptance(UNVERIFIED 유지) |
| 18장 "프리비즈의 조형물은 원본 의식 소질이 아니다" | 어댑터 `scope` 문구와 동일 취지 |

### 3.2 이번에 반영한 공백 (구현 완료)

| # | 공백 | 근거 | 반영 |
|---|---|---|---|
| F1 | 어댑터 대역이 추상 박스뿐 → 가이드북 14·18장이 쓰는 점토 인물 프리비즈(머리·몸 실루엣)를 재현하지 못함 | 62p 실물 프리비즈 이미지 vs 실제 렌더 비교 | `build_previs.py`에 `--proxy box\|figure` 추가(figure = 토르스·목·머리 구체). `figure_proxy_parts`/`sphere_mesh` 순수 함수 + 단위 테스트 4건. manifest에 `proxy_mode`/`scope` 기록. 스키마 `camera-spatial-1.0`은 불변 |
| F2 | AI 제어 패킷에 **참조 슬롯 역할표 / shot-local 구간 행동표 / 보존 제약 / 오디오 분리** 칸이 없음. 가이드북 17·18장의 모든 생성 카드는 "보존-금지"를 씀 | 73·75·81–82p 카드 | `ai-camera-control/assets/camera-control-template.md` 4개 표 추가, `control-contract.md`에 "시간 구간 행동·보존 제약·오디오 분리" 절 추가, SKILL 4단계·Acceptance 갱신 |
| F3 | 카메라 설계 인텐트에 "무엇이 변하면 안 되는지" 칸이 없음 | 가이드북 카드 공통 구조 | `camera-intent-template.md`에 보존 제약 행(근거 ID·검증 방법) 추가 |
| F4 | 리듬·감정 예시 수치(90초 3구간, 4초 컷, 12–18초 감정 지속, 감정→몸짓→키 비주얼)가 없음 | 9–11p(3장), 56–58p(13장) | `camera-language-catalog.md`에 **C2. 예시 리듬·감정 프로필(선택)** 추가. 다른 프로젝트 규칙이 아님을 명시 |
| F5 | 런타임 기록이 Windows 10 과거 실행 기준 | 62p(현재 작업 환경) | `blender-workflow.md` 런타임 상태를 2026-10-21 Linux 실측(24개 테스트·렌더 시간 포함)으로 갱신, "MCP 불필요" 명시 |

### 3.3 이번에 반영하지 않은 권고 (사용자 결정 필요)

| # | 권고 | 이유 |
|---|---|---|
| R1 | 90초/4초/12–18초를 **기본 강제값**으로 승격 | 스킬의 원칙("교육용 비율은 강제 배분이 아니다")과 충돌. C2는 선택 프로필로만 추가 → **§3.5에서 기본 강제값 승격으로 확정하지 않음** |

### 3.5 범용화 마감 (R1 결정 반영)

사용자 결정: **R1은 기본 강제값으로 승격하지 않는다.** 스킬은 여러 작품에 적용되어야 하므로, 출처의 수치가 아니라 *방법*을 일반화하고 수치는 예시로만 남긴다. 패키지가 이미 같은 출처를 `GUIDE-01`로 통합한 기록과 "작품 고유 요소는 범용 지침으로 옮기지 않는다" 규칙(29-reference-driven-production.md·guide-01-extraction.md의 충돌 해결 절)에 맞춰 다음과 같이 정리했다.

| 항목 | 조치 |
|---|---|
| 카메라 카탈로그 C2 | 작품명을 빼고 `GUIDE-01` 출처 ID + 장/쪽(3장 pp9–12·11장 pp48–50·13장 pp56–60)으로 인용. "고정 90초·구간 배분·인물/장소 수를 강제 규격으로 채택하지 않는다" 문구를 house 문구와 일치시킴. 예시 수치는 유지하되 유지 길이의 판정 기준을 "그 안에 카메라가 보낼 정보/행동이 남아 있는가"로 일반화 |
| 런타임 가이드 R3 | 컷 전환은 새 정보·행동·반응·감정·시선 중 하나의 실제 변화를 근거로 하고, 컷 수/길이 목표값을 먼저 정하지 않는다는 일반 규칙 추가. 감정 구간 카메라의 세 선택(밀어붙이기·근거 따라가기·관점 바꾸기) 추가 |
| 런타임 가이드 R8 | 편을 "관객이 알게 되는 정보가 바뀌는 지점"으로 구간화하고, 참고한 길이 예시는 채택하지 않는다는 일반 규칙 추가 |
| higgsfield 이미지 craft | 작품명 제거, `GUIDE-01` + 출처 등록 링크로 대체, "서비스·모델 기본값을 채택하지 않는다" 명시 |
| Blender 기법 구현표 | GUIDE-01 R3 앵커·쪽수 인용 추가(프리비즈 카드·컷 리듬 근거) |
| 통합 기록 | guide-01-extraction.md에 2026-10-21 보충 절 추가(추가 소비처 5곳과 제외 원칙). K-item 표와 44항목 연결표는 건드리지 않음 |

검증: `scripts/test_guide_integration.py` 14 OK(드라마 고유어·고정 제공자 레시피 금지 검사 포함), 런타임 스킬 전역에서 작품 고유 표현 0건(잔존 1건은 금지어 목록을 가진 검사 스크립트 자체), `pytest` 398 passed / 516 subtests / 0 skipped.
| R2 | 프리비즈에 실제 캐릭터 에셋(스케치·시트) 연결 | `camera-spatial-1.0`에 에셋 필드가 없고, 이미지 실행은 `codex-imagen` 승인 게이트를 따른다. 스키마 확장 필요 |
| R3 | 초점거리/조리개 키프레임(랙 포커스) 구현 | 현재 `UNSUPPORTED/UNVERIFIED`로 명시됨. 동일 스키마에 안전하게 추가 가능하나 렌더 검증이 필요 |
| R4 | EEVEE 기본 전환(속도) | Cycles CPU가 미감·그림자 기준선. 기본 엔진 변경은 렌더 판정 기준 변경이므로 별도 검토 필요 |
| R5 | 가이드북의 모델 표(Flare/Sunburst, WAN 2.7 Image Pro, Seedream 5 Pro, Nano Banana Pro 역할)를 `higgsfield-generate` craft 참조로 등재 | 이미지 모델은 패키지 정책상 craft/reference 전용이며, 힌지스필드 이미지 실행은 제외됨. 라우팅 문서 반영은 정책 확인 후 |
| R6 | Blender MCP 서버를 실제로 Pi에 등록 | 현재 스킬은 CLI 경로로 완결. MCP는 선택 실행 표면이며 서버 설치·인증이 별도 과제 |

### 3.4 2차 라운드에서 구현한 권고 (R2–R6)

사용자 승인 후 위 권고를 모두 구현했다. **스키마(`camera-spatial-1.0`)는 끝까지 건드리지 않았고**, 새 입력은 어댑터/문서 계층에만 넣었다.

| # | 구현 내용 | 위치·검증 |
|---|---|---|
| R2 | `--look-cards cards.json`: `{"CH01": {"image": "/abs/path.png"}}` → subject box 크기의 카메라 정면 평면 카드에 승인 이미지 텍스처. 프레이밍 안에 승인된 룩을 보여 주되 깊이·가림 순서·자세·접촉은 증명하지 않음 | `build_previs.py` `look_card()` + `parse_look_cards()`. 실제 렌더로 카드 표시 확인, 단위 테스트 포함 |
| R3 | `--focus-map focus.json`: 샷별 `focus_distance_m` 키프레임 + `f_number` → Blender DoF 베이크. 랙 포커스 미리보기가 실제로 동작(프레임 0 카드 선명 / 프레임 47 인물 선명) | `parse_focus_map()`·`focus_distance_at()`. 렌더 육안 확인, 단위 테스트 포함 |
| R4 | `--engine cycles|eevee`: 후보 id를 순차 시도해 이 빌드에서 실제 사용 가능한 엔진을 선택(Cycles는 add-on이라 enum에 없을 수 있음) | `engine_candidates()`. eevee 렌더 10초 확인. 기본값은 cycles 유지 |
| R5 | 가이드북의 작업별 이미지 모델 선택(캐릭터 시트·실감 조명·강한 감정 키 비주얼)을 craft 참고로 등재 + 모델명 혼동(Flare/Sunburst)·모델 교체 시 정체성 드리프트 경고 | `higgsfield-generate/references/image-branches.md`. capability/품질 주장 없음, 패키지 정책(이미지 제외) 명시 |
| R6 | Blender MCP 서버 구현·등록: `blender_version`·`blender_previs`·`blender_previs_inspect`. 사용자 명령 실행 금지, 자동 설치 금지, 기존 출력 폴더 덮어쓰기 거부, 절대 경로 요구 | `blender-previsualization/mcp/blender_mcp_server.py` + `test_blender_mcp_server.py`(8 테스트). **전역 실행 명령** `~/.local/bin/blender-mcp-server`로 Pi/Codex 등록(호스트 재시작 필요) |

R2–R4는 모두 `camera-spatial-1.0` **밖의 선택 입력**이므로 스키마·정본은 그대로다. `spatial-contract.md`·`motion-timing-lens.md`·`camera-technique-implementation.md`에 이 경계를 명시했다.

## 4. 변경 파일

- `blender-previsualization/scripts/build_previs.py` — `--proxy figure`, `--focus-map`, `--look-cards`, `--engine`; `figure_proxy_parts`, `sphere_mesh`, `signed_volume`, `parse_focus_map`, `focus_distance_at`, `parse_look_cards`, `engine_candidates`; 매니페스트 `proxy_mode`/`engine`/`focus_map`/`look_cards`
- `blender-previsualization/scripts/test_build_previs.py` — 프록시/메시/CLI/포커스/룩카드/엔진 테스트 (17 OK)
- `blender-previsualization/mcp/blender_mcp_server.py`, `blender-previsualization/mcp/blender_mcp_server_launcher.py`, `blender-previsualization/mcp/install_global_launcher.py`, `blender-previsualization/mcp/test_blender_mcp_server.py` — MCP 서버·전역 실행 명령·설치 스크립트와 자체 테스트 (8 OK)
- `blender-previsualization/SKILL.md` (2.23→2.24) — 프록시 모드, 선택 입력, MCP 표면
- `blender-previsualization/references/blender-workflow.md` — 대역 모드·선택 입력·MCP 표면 절, 런타임 상태 갱신
- `blender-previsualization/references/camera-technique-implementation.md` — 프록시 모드, 랙 포커스 경계 갱신
- `ai-camera-control/SKILL.md` (1.18→1.19), `references/control-contract.md`, `assets/camera-control-template.md`
- `camera-spatial-design/SKILL.md` (1.18→1.19), `references/camera-language-catalog.md`(C2), `references/spatial-contract.md`(스키마 밖 입력 명시), `references/motion-timing-lens.md`, `assets/camera-intent-template.md`
- `higgsfield-generate/references/image-branches.md` — 작업별 모델 선택 craft 참고
- `pytest.ini` — 파생 `video-production-assets/support/` 빌드 산출물만 제외해 로컬과 CI 수집을 일치
- `README.md`, `CHANGELOG.md`

## 4.1 환경 정리 (2차 라운드 종료 시점)

| 항목 | 조치 | 결과 |
|---|---|---|
| pytest 미설치 | 이 호스트에 `pip`/`ensurepip`/`sudo`가 없어 `get-pip.py`를 **사용자 사이트**(`~/.local`)에만 부트스트랩(`--user --break-system-packages`)하고 `pytest 9.1.1`, `Pillow 12.1.1`, `pydantic 2.14.1`을 CI와 같은 세트로 설치 | `python3 -m pytest -q`가 이 호스트에서 동작 |
| pytest 기반 테스트 미실행(6개 파일) | 위 설치로 즉시 해소. 추가로 `ffprobe`가 없어 건너뛰던 실제 딜리버리 회귀 13건도 해소 | **396 passed, 515 subtests passed, 0 skipped** |
| `ffprobe` 부재 | 기존 `ffmpeg`(johnvansickle static 7.0.2, `~/.local/opt/flucto-cli/bin`)와 **동일 버전** 7.0.2 정적 배포의 `ffprobe`만 `~/.local/bin`에 설치(GPLv3 문서 동봉). 기존 `ffmpeg` 해석은 그대로 유지 | `which ffmpeg` 불변, `ffprobe` 7.0.2 사용 가능 |
| 로컬/CI 수집 차이 | `video-production-assets/support/`(git-ignored 생성물)이 커밋된 `qa/` 페이로드와 동일 basename을 가져 로컬 수집이 충돌했음 | `pytest.ini`에 `norecursedirs`로 해당 생성물만 제외 → 로컬과 CI 수집이 동일해짐 |
| MCP 반영 | Pi `~/.pi/agent/mcp.json`, Codex `~/.codex/config.toml`에 **전역 실행 명령** `blender-mcp-server`로 등록(TOML/JSON 파싱 검증). `install_global_launcher.py --update-pi`가 실행 명령 설치·스킬 루트 기록·Pi 설정 갱신을 수행. 임의 cwd에서 전역 명령으로 기동해 `blender_version`·`blender_previs`·`blender_previs_inspect`와 산출물 5종 확인 | **호스트 재시작 후** 두 호스트 모두 `blender` 서버가 노출됨 |
| MCP 인세션 실전 확인 | 사용자 `/reload` 후 이 세션에서 실제 `mcp__blender__blender_version`·`mcp__blender__blender_previs`·`mcp__blender__blender_previs_inspect` 호출로 프리비즈 실행(figure proxy·cycles, 2샷×3프레임, 12.4초) → 산출물 9개·`status: generated` 확인, SH02 mid 프레임 육안 검수(돌리인 접근 프레이밍 정상) | 세션 내 MCP 경로 완전 동작 |

## 4.2 잔여/주의 사항

- `pytest.ini`는 `video-production-assets/support/`(동기화 스크립트가 만드는 파생 빌드 산출물)만 제외한다. 커밋된 `qa/` 페이로드는 그대로 수집된다.
- 리포지터리 루트의 `%TEMP%pytest-skill-final/`은 이전 세션이 남긴 pytest 임시 산출물(untracked)이었으며 **삭제**했다(내용은 전부 재생성 가능한 테스트 픽스처). 같은 이름이 다시 생기지 않도록 `.gitignore`에 패턴을 추가했다.
- MCP는 **전역 실행 명령**(`~/.local/bin/blender-mcp-server`)으로 등록해 체크아웃 절대경로를 더 이상 쓰지 않는다. 서버는 `BLENDER_PREVIS_ADAPTER` → `BLENDER_PREVIS_SKILL_ROOT` → `~/.config/blender-mcp/skill_root` → 설치된 스킬 루트 순으로 어댑터를 찾는다. 스킬이 옮겨지면 `~/.config/blender-mcp/skill_root`를 갱신하거나 `BLENDER_PREVIS_SKILL_ROOT`를 지정한다.
- 세션 재시작은 불필요하다. Pi 문서대로 MCP 설정을 세션 밖에서 바꾼 뒤 `/reload` 한 줄이면 서버만 재연결된다(2026-10-21 실제로 그렇게 확인).

## 5. 재현 명령

```bash
cd /home/declan/Documents/Projects/Skills-and-Automation/contents-production-skills
python3 camera-spatial-design/scripts/test_spatial_spec.py
python3 blender-previsualization/scripts/test_build_previs.py
BLENDER_EXECUTABLE=/home/declan/.local/bin/blender python3 blender-previsualization/scripts/test_camera_orientation_in_blender.py
/home/declan/.local/bin/blender --background --factory-startup \
  --python blender-previsualization/scripts/build_previs.py -- \
  --spec camera-spatial-design/assets/camera-spec-example.json \
  --output /tmp/previs-figure --mode stills --proxy figure
```
