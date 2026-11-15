# Blender 프리비즈 동선·가림 보완 설계

**Date:** 2026-11-16
**Status:** Approved (사용자 승인: 4개 항목 전부 진행)
**Scope:** `blender-previsualization`의 어댑터(`scripts/build_previs.py`), 신규 `scripts/path_map.py`, 테스트, 스킬 문서, 패키지 버전.
**비범위:** three.js/브라우저 프리비즈 표면, Blender 대체 렌더러, 관절·연기·접촉 검증, 유료 생성·배포.

## 1. 배경

프리비즈의 목적은 동선·블로킹 판단이다. 현재 `blender-previsualization` v2.26은 이를 **샷별 PNG + numerical-analysis.json + blender-inspection.json**으로 제공하지만, 그 목적에 직접 필요한 네 가지가 비어 있다.

| # | 확인된 결손 | 근거 |
|---|---|---|
| 1 | 평면 동선도가 없다 | `blender-previsualization/` 전체에 top-down/경로도 산출물 0건. 사람은 프레임 여러 장을 눈으로 이어 붙여야 함 |
| 2 | 가림 검사가 점 2개뿐 | `build_previs.py`의 `[('center',height/2),('head',height*.95)]` — 실루엣 절반이 가려져도 "보임" |
| 3 | figure 프록시에 방향 표식 없음 | `figure_proxy_parts()`는 torso/neck/head 구 3개. `camera-spatial-1.0`에 facing 필드가 없어 시선 방향을 화면에서 읽을 수 없음 |
| 4 | 시퀀스 모드가 MP4를 만들지 않음 | `--mode sequence`는 PNG만 생성. 애니매틱 확인은 수동 조립 |

## 2. 목표 / 비목표

**목표**
- 같은 spec에서 **사람이 한 장으로 동선을 읽는 평면도**를 만든다.
- 가림 판정을 점 1~2개에서 **실루엣 9점**으로 확장하고 샷 단위 요약을 남긴다.
- figure 프록시에서 **인물이 향하는 방향**을 읽게 한다.
- 시퀀스 산출물을 **ffmpeg로 애니매틱 MP4로 조립**하고 실제 길이를 기록한다.

**비목표(안티골)**
- 새 렌더러·새 증거 등급을 만들지 않는다. Blender 산출물 계약(`previs.blend`·PNG·inspection·manifest)은 그대로다.
- 평면도를 "3D 검증"으로 승격하지 않는다. 평면도는 **spec 파생 도해**이며 가림·접촉을 증명하지 않는다.
- 9점 가림을 "실루엣 전체 가시성"으로 표현하지 않는다.
- 유료 생성·자동 설치·자동 배포를 추가하지 않는다.

## 3. 설계

### 3.1 동선 평면도 (`scripts/path_map.py`, 신규)

bpy를 쓰지 않는 순수 모듈. `camera-spatial-1.0` spec만으로 샷별 SVG 1장을 만든다.

- 출력: `<output>/<shot_id>/path-map.svg`
- 내용: 1m 격자·스케일 바, 장애물 사각형, 피사체 시작(점선)/종료(실선) 발자국 + 이동 폴리라인 + 프레임 틱, 피사체 facing 화살표, 카메라 경로 폴리라인 + 진행 방향 화살표, 샘플 프레임의 화각 쐐기(±fov_x/2, 길이 = 가장 가까운 피사체까지 거리 상한), 샷 메타(길이·fps·렌즈 범위·scene/beat ID)
- 결정론: 좌표 반올림 3자리, 정렬된 키 → 동일 spec은 동일 바이트.
- **`--mode path-maps` 신설**: Blender 없이 `python3 build_previs.py --mode path-maps`로 전 샷 도해만 생성. bpy import 이전에 분기하므로 Blender 미설치에서도 동작한다. 이 모드의 manifest는 `blender_version: null`, `status: generated`, `scope`에 "diagram only, no render/occlusion verification"을 기록한다.

### 3.2 실루엣 9점 가림 (`silhouette_points()`)

`(high|mid|low) × (left|center|right)` 9점.

- box 프록시: z = 0.88h / 0.55h / 0.25h, 측면 반폭 = AABB를 카메라 right 축에 투영한 값의 ±0.9배
- figure 프록시: z = head 중심 / torso 중심 / torso 하단부, 측면 반폭 = torso 반지름의 ±0.9배 (구 밖으로 나가 헛가시가 되지 않게)
- right 축은 `normalize(cross(forward, +Z))`, 각 프레임의 실제 카메라 방향에서 계산
- 판정 규칙은 기존과 동일: 첫 hit이 자기 대역(또는 부품)이면 보임
- 추가 산출: 샷별 `occlusion_summary` — 피사체별 보임 비율, 최초 가려진 프레임·지점

### 3.3 figure 방향 표식

- 신규 순수 헬퍼 `cone_mesh()`(닫힌 원뿔, `signed_volume`으로 법선 검증) + `facing_marker_parts()`(반지름·길이·높이)
- 방향 결정 우선순위: `--facing-map` 지정값 → 이동 벡터(`subject_tracks`의 전후 프레임 차이, 1cm 미만은 미정) → 없음
- 미정이면 마커를 숨기고 `facing_source: "none"`으로 기록한다. 임의 방향을 만들지 않는다.
- `--facing-map facing.json` = `{"SH01": {"CH01": [0.0, 1.0]}}` (월드 XY 단위 벡터, 샷 단위 상수). **어댑터 전용 입력**이며 `camera-spatial-1.0` 스키마를 넓히지 않는다(`--focus-map`·`--look-cards`와 동일 규칙).
- 평면도에도 같은 벡터로 화살표를 그린다(단일 구현 공유).

### 3.4 애니매틱 조립 (`--encode-mp4`)

- 사전 검사: `--mode sequence`에서만 허용, 시작 시 ffmpeg 존재를 확인하고 없으면 렌더 전에 실패(자동 설치 없음)
- 구현: concat demuxer 목록(이미지당 1/fps duration, 마지막 프레임 반복) → `animatic.mp4`
- 기록: `manifest.encode = {ffmpeg, command, output, frames, expected_s, measured_s, scope}`. 측정은 ffprobe가 있을 때만, 없으면 `measured_s: null`
- 주장 범위: "무음·무전환 스틸 조립본". 최종 편집본·모션블러·오디오 없음. 기존 문서 문구("MP4 애니매틱이라고 보고하지 않는다")는 **조립 사실과 미보장 범위를 분리 기록**하는 방향으로 갱신한다.

## 4. 계약·문서 변경

| 문서 | 변경 |
|---|---|
| `SKILL.md` | 실행 6·7단계에 path map/9점 가림/`--facing-map`/`--encode-mp4`/`--mode path-maps` 반영, 실행 출력 목록 갱신, 버전 범프 |
| `references/blender-workflow.md` | 범위·모드·대역·어댑터 전용 입력 절에 신규 동작과 한계 추가 |
| `assets/previs-handoff-template.md` | 평면도·가림 요약·facing·encode 기록 슬롯 추가 |
| `USAGE_GUIDE.md` | 프리비즈 산출물 설명에 평면도·애니매틱 추가 |
| `CHANGELOG.md` | Unreleased 항목 |
| `mcp/blender_mcp_server.py` | `--facing-map`, `--encode-mp4` 전달 |
| 테스트 | `silhouette_points`, `cone_mesh`, `parse_facing_map`, facing 결정, SVG 결정론, encode 명령, CLI 파싱 |

## 5. 검증 (실제 실행 결과, 2026-11-16)

| 검증 | 결과 |
|---|---|
| 전체 테스트 | `python3 -m pytest -q` → **766 passed, 4 skipped**, 532 subtests. 신규 `test_path_map.py` 19건 포함 |
| 버전 정합 | `python3 scripts/check_versions.py` → `package 2.40, 23 skill(s) consistent` |
| `--mode path-maps` (Blender 없이) | 2샷 SVG 생성, `blender_version: null`, scope에 렌더·가림 미검증 명시. `--facing-map` 지정 시 manifest에 벡터 기록. 기존 출력 폴더는 거부 |
| `--proxy figure --facing-map` stills | Cycles 8 samples·eevee 각각 실행. 방향 마커가 실제 렌더에 나타남(육안 확인). 지정 없는 정지 피사체는 `facing.source: none`, 마커 미표시 |
| 9점 가림 (무릎 높이 장애물) | CH01 **6/9**, 가려진 점 `low_left/low_center/low_right`, `first_hit=SH01_LOWWALL`. 기존 2점(0.5h·0.95h)은 이 행을 표본하지 않음 |
| 9점 가림 (전신 차폐 장애물) | CH01 144/432(0.333), CH02 432/432. 전 샷 프레임 검사 |
| `--mode sequence --encode-mp4` | 8프레임·fps 24 → expected 0.333s, measured **0.333s**, `nb_read_frames=8`로 일치 |
| 가드 | `--encode-mp4`를 path-maps/stills와 함께 쓰면 명시적 오류. 잘못된 facing 맵은 unknown shot/subject로 거부 |
| box 프록시 회귀 | 마커 없음·기존 렌더 형태 유지 확인 |

**미검증(문서에도 남김)**: `path-map.svg`의 육안 확인. 이 호스트에 SVG 래스터라이저(rsvg·inkscape·cairosvg·Chromium)가 없어 PNG로 변환하지 못했다. 대신 좌표 매핑·1m 스케일 바·결정론·요소 존재를 테스트로 고정했고, 실제 보기 확인은 사람이 파일을 여는 것으로 남긴다.

## 6. 남은 한계 (문서에 그대로 남긴다)

- 평면도는 spec 파생 도해다. 실제 장면의 가림·접촉·조명을 증명하지 않는다.
- 9점 가림은 여전히 점 샘플이다. 실루엣 전체·관절·손 접촉은 미검증.
- facing은 이동 벡터 또는 사용자 지정 상수이며, 얼굴 방향·시선 목표를 검증하지 않는다.
- 애니매틱 MP4는 무음·무전환 스틸 조립본이다.
