---
name: blender-previsualization
version: 2.27
description: "Required Blender implementation/visual inspection for actual scene-specific 3D geometry/placement/feasibility design or explicit Blender/previs requests; also animatics. Camera fields, moves and storyboards alone do not trigger Blender. Exclude beauty rendering, full character rigging, physics simulation and other-app rendering."
---

# 블렌더 프리비즈

`creative-production`이 프로젝트 수준 진입점·조정자다. 이 스킬은 장면별 3D 카메라/공간 작업의 Blender 구현·시각 검수를 소유한다. `camera-spatial-design`의 수치 명세가 정본 입력이며 실제 장면과 화면을 생성·검사한다. 단독 호출이면 `creative-production`으로 범위·경로를 한 번 확인한 뒤 요청된 프리비즈만 수행한다. 위임받아 실행 중이면 프로젝트 라우팅을 다시 하거나 두 번째 인터뷰·승인 원장을 열지 않고 인계된 명세만 진행한다. 실행·생성 라우팅은 `creative-production`에 맡긴다.

## Blender decision boundary

For reference-to-generation previs, proxy color/identity mapping, prop-state changes or motion-versus-appearance separation, read [semantic proxy handoff](references/semantic-proxy-handoff.md). It supplies the decomposition, revision and reference-slot procedure; it does not add articulated hands, hinges, tracking or rigging to the bundled box/figure adapter.

Two additions stay inside that adapter boundary. The top-down blocking diagram (`<shot_id>/path-map.svg`) is derived from the camera spec alone: it shows camera path, frustum bearings, subject travel and facing, and proves no occlusion, contact or lighting. Facing comes from an assigned world heading (`--facing-map`) or from the subject's own travel; it never claims face direction, eyeline target or acting. Occlusion samples nine silhouette points per subject per frame instead of a head/center pair, and still proves no whole-silhouette, articulated or hand/object visibility.

For assigned procedural geometry, materials/lighting, staged exploded views or alpha/loop/web handoff craft, consume the relevant `open-3d-production` module selected by the coordinator in the [canonical module table](../creative-production/references/production-routing.md#open-3d-module-selection), after reading its [Blender adaptation](../open-3d-production/references/blender-adaptation.md). It is an implementation reference, not another orchestrator or a Three.js replacement for Blender. Keep this skill's spatial spec, proxy adapter, execution gates and inspected-evidence acceptance unchanged; beauty rendering, full rigs and physics need a separately scoped native implementation, not claims about this adapter.

Use the [canonical production routing and Blender gate](../creative-production/references/production-routing.md#blender-decision-gate). Narrative camera planning in text/ordinary 2D storyboards and simple 2D/flat graphics do not invoke Blender. Numeric lens/coordinate/path proposals without a geometry-verification deliverable remain with `camera-spatial-design`, with numeric/schema analysis as applicable and unrendered geometry `UNVERIFIED`.

**Blender trigger:** explicit Blender/previs request, or the requested result depends on validating an actual scene-specific 3D arrangement (camera path, geometry, blocking, occlusion, clearance, or contact), or a 3D-verified result is part of the requested deliverable. A camera field, camera move, storyboard, or scene ID alone is not a Blender trigger.

“Scene-specific 3D camera/spatial design” means actual scene-specific 3D geometry/placement/feasibility design under this trigger. `camera-spatial-design` owns the spec; this skill implements and visually inspects triggered work. Text-only/read-only work may plan later previs but must not execute Blender, including runtime probes or smoke; mark unperformed checks `PLANNED`/`UNVERIFIED` or `BLOCKED`. If required Blender is unavailable, return the exact missing runtime/evidence, continue independent text work, and mark only dependent spatial deliverables `BLOCKED`/`UNVERIFIED`; no alternate-renderer substitution or FINAL claim. The execution steps below apply only to authorized runtime work.

## 실행 — 승인된 runtime 작업만
1. [공통 공간 계약](../camera-spatial-design/references/spatial-contract.md)과 [실행·CLI 정본](references/blender-workflow.md)을 읽는다. 기법 어휘가 있으면 [구현표](references/camera-technique-implementation.md)도 적용한다. 수치 spec 누락을 예제로 채우지 않고 정확한 scoped gap을 부모에 반환한다.
2. 실제 Blender/API/엔진 지원을 확인하고 `camera-spatial-1.0` 명세를 형제 `spatial_spec.py`로 검사한다. 기준 실행은 독립 Blender CLI 프로세스다; 같은 어댑터/산출물·evidence 계약을 만족하는 MCP만 보조 표면으로 쓴다. 설치/업데이트는 자동 수행하지 않는다.
3. 사용자의 열린 프로젝트에는 초기화 스크립트를 실행하지 않는다. 새 출력 폴더의 저해상도 1프레임 smoke는 파이프라인 preflight일 뿐이다. 이후 요청된 stills/render-map/전체 sequence를 실제 실행한다. 정확한 모드·프레임·proxy/engine/focus/look/facing 옵션과 회귀 검사 명령은 실행 정본이 소유한다.
4. 요청된 .blend/PNG와 문제 프레임을 다시 열어 경로·headroom·공간 방향·가림을 실제 검수한다. 필수 articulated contact/손·제품 점유 근거가 없으면 UNVERIFIED로 둔다. 명세 수정→재생성→관련 QA 후 [인계 양식](assets/previs-handoff-template.md)에 ID/버전·실제 검사 범위를 기록한다.

## 실행 출력
실제 `previs.blend`, 샷별 PNG/시퀀스, `path-map.svg`, `numerical-analysis.json`, `blender-inspection.json`, `manifest.json`을 인계한다. 선택 proxy/engine/focus/look/facing/occlusion/encode와 Blender 버전·모드·scene/shot/panel 연결은 실행 정본대로 남긴다. 생성된 실제 파일만 generated다. `--mode path-maps`는 Blender 없는 spec 도해이고 `--encode-mp4`는 무음 스틸 시퀀스이며 어느 쪽도 실제 3D/접촉/최종 편집 검증을 대신하지 않는다. 미실행 분석·요청 프레임은 미검증으로 남긴다.

## Acceptance

A previs is complete only when the requested scene spec passes its schema check, the actual Blender version and run mode are recorded, requested `.blend`/image artifacts exist and can be reopened, and the inspected frames are tied to shot/panel IDs. Report smoke-only checks as smoke-only; list occlusion, framing, missing-asset, and unsupported-geometry failures with the affected IDs. If Blender was unavailable or any requested render was not produced and opened, mark that deliverable `BLOCKED` or `UNVERIFIED`; never infer completion from a script exit code alone.

Numeric/schema checks and smoke runs do not prove actual 3D scene feasibility or full requested visual inspection. Smoke is pipeline preflight only, not full-scene/all-requested-frame/contact acceptance. Bounding-box, center-point, nine-point silhouette sampling and ray-cast proxies do not prove full articulated visibility, hand/object contact, performance, aesthetics or final generated-video quality; claims without the required actual inspected evidence remain `UNVERIFIED`. Top-down diagrams are spec-derived and the assembled animatic is a silent still sequence; neither upgrades those claims.
