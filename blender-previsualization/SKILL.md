---
name: blender-previsualization
version: 2.24
description: "Required Blender implementation/visual inspection for actual scene-specific 3D geometry/placement/feasibility design or explicit Blender/previs requests; also animatics. Camera fields, moves and storyboards alone do not trigger Blender. Exclude beauty rendering, full character rigging, physics simulation and other-app rendering."
---

# 블렌더 프리비즈

`creative-production`이 프로젝트 수준 진입점·조정자다. 이 스킬은 장면별 3D 카메라/공간 작업의 Blender 구현·시각 검수를 소유한다. `camera-spatial-design`의 수치 명세가 정본 입력이며 실제 장면과 화면을 생성·검사한다. 단독 호출이면 `creative-production`으로 범위·경로를 한 번 확인한 뒤 요청된 프리비즈만 수행한다. 위임받아 실행 중이면 프로젝트 라우팅을 다시 하거나 두 번째 인터뷰·승인 원장을 열지 않고 인계된 명세만 진행한다. 실행·생성 라우팅은 `creative-production`에 맡긴다.

## Blender decision boundary

Use the [canonical production routing and Blender gate](../creative-production/references/production-routing.md#blender-decision-gate). Narrative camera planning in text/ordinary 2D storyboards and simple 2D/flat graphics do not invoke Blender. Numeric lens/coordinate/path proposals without a geometry-verification deliverable remain with `camera-spatial-design`, with numeric/schema analysis as applicable and unrendered geometry `UNVERIFIED`.

**Blender trigger:** explicit Blender/previs request, or the requested result depends on validating an actual scene-specific 3D arrangement (camera path, geometry, blocking, occlusion, clearance, or contact), or a 3D-verified result is part of the requested deliverable. A camera field, camera move, storyboard, or scene ID alone is not a Blender trigger.

“Scene-specific 3D camera/spatial design” means actual scene-specific 3D geometry/placement/feasibility design under this trigger. `camera-spatial-design` owns the spec; this skill implements and visually inspects triggered work. Text-only/read-only work may plan later previs but must not execute Blender, including runtime probes or smoke; mark unperformed checks `PLANNED`/`UNVERIFIED` or `BLOCKED`. If required Blender is unavailable, return the exact missing runtime/evidence, continue independent text work, and mark only dependent spatial deliverables `BLOCKED`/`UNVERIFIED`; no alternate-renderer substitution or FINAL claim. The execution steps below apply only to authorized runtime work.

## 실행
1. [공통 공간 계약](../camera-spatial-design/references/spatial-contract.md)과 [Blender 실행 지침](references/blender-workflow.md)을 읽는다. 인계된 카메라 기법이 카탈로그 어휘를 쓰면 [기법별 Blender 구현표](references/camera-technique-implementation.md)도 읽고 현재 구현·추가 구현·외부 편집·미지원 상태를 정한다. 위임된 유효 명세는 그대로 구현하고 지정된 샷 ID와 잠긴 배치는 유지한다. 수치 카메라 명세가 없거나 불완전하면 카메라 설계는 이 스킬의 권한이 아니므로 예제로 채워 실행하지 말고 정확히 비는 항목을 scoped gap으로 부모에 돌려보낸다. 예제 spec은 사용자가 시도용으로 명시할 때만 쓰고 제작 카메라 근거로 보고하지 않는다.
2. `blender --version` 또는 `import bpy; print(bpy.app.version_string)`으로 실행 환경을 확인한다. 실행 환경이 없으면 명세·수치 분석만 계획 산출물로 반환하고 해당 3D 작업을 BLOCKED/UNVERIFIED로 표시한다. `.blend`/렌더가 생성됐다고 말하거나 다른 렌더러로 대체하지 않는다. 이 스킬의 기준 경로는 Blender CLI(`blender --background --python`)다. 호스트에 MCP 서버가 등록되어 있으면(전역 명령 `blender-mcp-server`) 동일 어댑터의 `blender_version`·`blender_previs`·`blender_previs_inspect` 도구로 같은 산출물(`previs.blend`·샷별 PNG·numerical-analysis·blender-inspection·manifest)을 만들 수 있다. MCP 경로는 보조 표면일 뿐이며, 산출물·evidence 계약이 같지 않으면 CLI 경로로 되돌아간다. 어느 표면이든 설치는 자동 수행하지 않고, 없으면 그 사실을 보고한다.
3. [공통 첨부·API 근거](../camera-spatial-design/references/sources.md)를 읽고 실제 Blender 버전에서 API·엔진 지원을 확인한다. 예제는 단순 대역이며 미감·연기·심도·제품 재현을 보장하지 않는다.
4. 형제 스킬의 `../camera-spatial-design/scripts/spatial_spec.py`로 명세를 검증하고 경고를 장면 의도와 대조한다. 스키마는 camera-spatial-1.0이며 Blender 어댑터도 이 단일 구현을 사용한다. 두 스킬은 같은 스킬 루트에 설치한다.
5. 먼저 독립 Blender 프로세스에서 저해상도 1프레임 smoke test를 수행한다. `--mode smoke`는 첫 샷·첫 프레임만 베이크/검사/렌더하며 긴 변 320px 이하, 업스케일 없음으로 제한한다. 전체 수치 분석은 생략한 미검증 상태로 남기며 전체 명세 렌더 검수라고 보고하지 않는다. 새 장면 생성 스크립트는 현재 프로세스의 장면을 초기화하므로 사용자의 열린 프로젝트에 직접 실행하지 않는다. 출력 폴더가 존재하면 새 폴더를 사용한다.
6. `blender --background --factory-startup --python scripts/build_previs.py -- --spec camera_spec.json --output out-previs --mode stills`를 실행한다. 샷별 시작·중간·끝 PNG, 샷별 Blender scenes가 있는 previs.blend, Blender 가림·화면 검사 JSON과 인계 manifest를 생성한다. 명시된 패널/프레임을 렌더하려면 `--mode stills --render-map '{"SH01":{"P04":17}}'`(또는 JSON 파일 경로를 붙인 `@file`, `{"shot":[frame]}`·`[{shot_id,frame,panel}]` 형태도 가능)를 쓴다. 지도에 없는 샷은 렌더하지 않고 로컬 0기준 프레임만 허용한다. 피사체 대역은 `--proxy box`(기본, 추상 박스)와 `--proxy figure`(토르스·목·머리 구체로 만든 점토 스타일 인물 대역) 중 하나를 고른다. figure 모드는 프레이밍·헤드룸·눈높이·실루엣 겹침·가림을 사람 몸 형태로 읽게 하는 것이 목적이며, 얼굴 방향·자세·관절·손 접촉·연기·최종 조명을 검증하지 않는다. 사용한 모드는 manifest의 `proxy_mode`와 `scope`에 남고 렌더 결과와 함께 인계한다. 선택 입력은 세 가지다: `--engine cycles|eevee`(렌더 엔진, cycles가 기준 look이고 eevee는 빠른 미리보기이며 품질 주장 아님), `--focus-map focus.json`(샷별 초점 거리 키프레임·f-number. 스키마에 없는 어댑터 전용 입력이며 랙 포커스 미리보기에만 쓴다), `--look-cards cards.json`(주목 대상 ID → 승인 이미지 경로. 카메라를 향하는 평면 카드로 프레이밍 안에 승인된 룩을 보여 주며, 깊이·가림 순서·자세·접촉은 증명하지 않는다).
7. 전체 프레임이 요청되면 `--mode sequence`를 사용한다. 파일은 `shot_id/frame_000001.png` 순서로 출력된다. 아직 인코딩된 영상이 아니므로 MP4 애니매틱이라고 보고하지 않는다. 편집/인코딩 도구가 있으면 샷 배열 순서와 fps로 조립하고 실제 길이를 확인한다.
8. 요청된 .blend와 PNG 출력을 다시 열어 요청된 프레임 및 시작/중간/끝뿐 아니라 문제 프레임을 확인한다. 몸·손·얼굴의 가림, headroom, 시선, 공간 방향, 경로를 검수한다. ray cast는 주목점 검사이며 전체 실루엣 가시성을 보장하지 않는다.
9. 명세를 수정해 재생성하고 선택 결과를 기존 영상 제작 에셋 원장에 연결한다. `assets/previs-handoff-template.md`를 채워 generated/inspected와 미검증 항목을 분리한다.
10. 어댑터·카메라 회전 코드를 변경하면 `python camera-spatial-design/scripts/test_spatial_spec.py`와 `python blender-previsualization/scripts/test_build_previs.py`를 실행한다. 실제 Blender가 있으면 `BLENDER_EXECUTABLE=<blender 실행 파일> python blender-previsualization/scripts/test_camera_orientation_in_blender.py` 통합 검사도 실행한다. MCP 서버를 건드렸으면 `python blender-previsualization/mcp/test_blender_mcp_server.py`도 실행한다. 이는 smoke 장면의 인물 중심·머리 가시성을 확인하며 전체 프레임의 미감 검수를 대체하지 않는다.

## 실행 출력
previs.blend, 샷별 PNG(또는 전체 PNG 시퀀스), numerical-analysis.json, blender-inspection.json, manifest.json을 인계한다. 기존 camera spec/version과 shot/scene/panel ID를 보존하고 실제 Blender version/mode 및 검사 프레임을 연결한다. 사용한 대역 모드(`proxy_mode`)·엔진·포커스 맵·룩 카드도 기록한다. 파일이 실제 존재하는 것만 generated로 기록한다. smoke에서 생략한 분석/프레임은 생성·검사 완료로 기록하지 않는다. 기본 어댑터는 대역·카메라·간단한 조명을 만들며 실사 촬영의 최종 조명과 다른 기술 프리비즈다.


## Acceptance

A previs is complete only when the requested scene spec passes its schema check, the actual Blender version and run mode are recorded, requested `.blend`/image artifacts exist and can be reopened, and the inspected frames are tied to shot/panel IDs. Report smoke-only checks as smoke-only; list occlusion, framing, missing-asset, and unsupported-geometry failures with the affected IDs. If Blender was unavailable or any requested render was not produced and opened, mark that deliverable `BLOCKED` or `UNVERIFIED`; never infer completion from a script exit code alone.

Numeric/schema checks and smoke runs do not prove actual 3D scene feasibility or full requested visual inspection. Smoke is pipeline preflight only, not full-scene/all-requested-frame/contact acceptance. Bounding-box, center-point and ray-cast proxies do not prove full articulated visibility, hand/object contact, performance, aesthetics or final generated-video quality; claims without the required actual inspected evidence remain `UNVERIFIED`.


