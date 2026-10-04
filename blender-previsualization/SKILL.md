---
name: blender-previsualization
version: 2.1
description: "Implement a camera-spatial specification as Blender proxy scenes with subject blocking, perspective cameras, camera and subject motion, shot previews, animated PNG sequences, .blend files and geometric inspection reports. Use for Blender previs, 3D camera tests, staging verification or animatics based on a script/camera brief. Exclude beauty rendering, full character rigging, physics simulation, photorealism guarantees and other-app rendering."
---

# 블렌더 프리비즈

`creative-production`이 프로젝트 수준 진입점·조정자다. 이 스킬은 Blender 프리비즈 산출물만 만든다. 단독 호출이면 `creative-production`으로 범위·경로를 한 번 확인한 뒤 요청된 프리비즈만 수행한다. 위임받아 실행 중이면 프로젝트 라우팅을 다시 하거나 두 번째 인터뷰·승인 원장을 열지 않고 인계된 명세만 진행한다. 실행·생성 라우팅은 `creative-production`에 맡긴다.

## 실행
1. [공통 공간 계약](../camera-spatial-design/references/spatial-contract.md)과 [Blender 실행 지침](references/blender-workflow.md)을 읽는다. 명세가 없으면 형제 스킬의 [카메라 예제](../camera-spatial-design/assets/camera-spec-example.json)를 작성용 기준으로 삼아 실제 배치를 채운다. 지정된 샷 ID와 잠긴 배치는 유지한다.
2. `blender --version` 또는 `import bpy; print(bpy.app.version_string)`으로 실행 환경을 확인한다. 실행 환경이 없으면 명세·수치 분석·실행 인계까지만 작성하고 .blend/렌더가 생성됐다고 말하지 않는다. 무단으로 다른 앱에 전환하지 않는다.
3. [공통 첨부·API 근거](../camera-spatial-design/references/sources.md)를 읽고 실제 Blender 버전에서 API·엔진 지원을 확인한다. 예제는 단순 대역이며 미감·연기·심도·제품 재현을 보장하지 않는다.
4. 형제 스킬의 `../camera-spatial-design/scripts/spatial_spec.py`로 명세를 검증하고 경고를 장면 의도와 대조한다. 스키마는 camera-spatial-1.0이며 Blender 어댑터도 이 단일 구현을 사용한다. 두 스킬은 같은 스킬 루트에 설치한다.
5. 먼저 독립 Blender 프로세스에서 저해상도 1프레임 smoke test를 수행한다. 동일 실행 명령의 `--mode smoke`를 사용한다. 새 장면 생성 스크립트는 현재 프로세스의 장면을 초기화하므로 사용자의 열린 프로젝트에 직접 실행하지 않는다. 출력 폴더가 존재하면 새 폴더를 사용한다.
6. `blender --background --factory-startup --python scripts/build_previs.py -- --spec camera_spec.json --output out-previs --mode stills`를 실행한다. 샷별 시작·중간·끝 PNG, 샷별 Blender scenes가 있는 previs.blend, Blender 가림·화면 검사 JSON과 인계 manifest를 생성한다.
7. 전체 프레임이 요청되면 `--mode sequence`를 사용한다. 파일은 `shot_id/frame_000001.png` 순서로 출력된다. 아직 인코딩된 영상이 아니므로 MP4 애니매틱이라고 보고하지 않는다. 편집/인코딩 도구가 있으면 샷 배열 순서와 fps로 조립하고 실제 길이를 확인한다.
8. PNG를 실제 열어 시작/중간/끝뿐 아니라 문제 프레임을 확인한다. 몸·손·얼굴의 가림, headroom, 시선, 공간 방향, 경로를 검수한다. ray cast는 주목점 검사이며 전체 실루엣 가시성을 보장하지 않는다.
9. 명세를 수정해 재생성하고 선택 결과를 기존 영상 제작 에셋 원장에 연결한다. `assets/previs-handoff-template.md`를 채워 generated/inspected와 미검증 항목을 분리한다.

## 실행 출력
previs.blend, 샷별 PNG(또는 전체 PNG 시퀀스), numerical-analysis.json, blender-inspection.json, manifest.json을 인계한다. 파일이 실제 존재하는 것만 generated로 기록한다. 기본 어댑터는 BBox 대역·카메라·간단한 조명을 만들며 실사 촬영의 최종 조명과 다른 기술 프리비즈다.
