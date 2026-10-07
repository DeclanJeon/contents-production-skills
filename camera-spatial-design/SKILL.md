---
name: camera-spatial-design
version: 1.0
description: Design shot sizes, camera positions and angles, composition, subject-to-subject
  and camera-to-subject distances, lens field of view, blocking and motivated camera
  paths for film, animation or AI video. Use for camera movement, shot coverage, spatial
  staging, angle/placement design or numerical camera specifications. Exclude camera
  shopping, generic book recommendations and actual Blender rendering, which belongs
  to blender-previsualization.
---

# 카메라·공간 설계

## Workspace integration

Read [workspace integration](references/workspace-integration.md) before applying local storage, sibling paths, image execution, Higgsfield CLI or approval instructions below. These adaptations govern this installed copy.

`creative-production`이 프로젝트 수준 진입점·조정자다. 이 스킬은 카메라·공간 수치 설계라는 직접 요청 산출물만 만든다. 단독 호출이면 `creative-production`으로 범위·경로를 한 번 확인한 뒤 요청된 설계만 수행한다. 위임받아 실행 중이면 프로젝트 라우팅을 다시 하거나 두 번째 인터뷰·승인 원장을 열지 않고 지정된 샷과 명세만 진행한다.

## 실행
1. [공통 공간 계약](references/spatial-contract.md)을 읽는다. 장면 목적, 관객이 알 정보, 인물 관계, 화면비, 장소·리그 제약을 확인한다. 도서 근거가 필요하면 [자료 지도](references/sources.md)를 읽는다.
2. 피사체·장벽·동선을 미터 좌표로 배치한다. 인물간 거리를 실제 이야기 관계와 연결하되 가까움=친밀함 같은 보편 공식을 강제하지 않는다. 주목할 대상과 가림을 명시한다.
3. 설계가 미확정이면 최소 두 카메라 후보를 비교한다. 각 후보에 크기·시점·높이·좌표·target·피사체 거리·렌즈/유효 게이트·구도를 기록한다. `assets/camera-comparison.csv`를 채운다. 창작 취향을 계산된 성과로 표현하지 않는다. 잠긴 카메라 명세를 위임받았으면 새 후보를 만들지 않고 검증·재사용하며, 승인된 설계가 깨진 것이 발견될 때만 변경 이유와 함께 부모에 돌려보낸다.
4. 원근은 시점·거리, 프레이밍은 시점·렌즈·출력 게이트의 결합으로 설계한다. 줌과 돌리를 구분하고, 카메라 이동이 꼭 필요한지 정지 샷/컷 대안과 비교한다.
5. 팬/틸트=위치 고정·바라보는 점 변화, 돌리/트럭/페데스털=위치 변화, 아크=대상 주변 경로로 기록한다. 추적은 대상 움직임과 카메라 경로를 함께 설계한다. 초점 이동은 초점 설계이며 카메라 위치 이동과 구분한다.
6. 화면 여백·눈높이·전경/중경/배경·가림·시선·180도 축을 확인한다. 축 변경의 관객 재정위 방법과 주목 대상 전환을 적는다.
7. `assets/camera-spec-example.json`을 복사해 실제 장면 명세를 작성한다. 예제 좌표를 아무 장면에 그대로 적용하지 않는다. 처음/중간/끝만 보지 말고 모든 프레임에서 대상 위치와 경로를 계산한다.
8. `python scripts/spatial_spec.py camera_spec.json --out analysis.json`으로 검사한다. warnings를 실제 샷 목적과 대조하고 의도된 크롭/축 변경은 이유를 기록한다. 경고 수를 작품의 품질 점수로 해석하지 않는다.
9. [설계·구도 판단](references/camera-design.md)을 적용하고 실제 프리비즈가 필요하면 `$blender-previsualization`에 같은 명세를 인계한다. 실제 화면 확인 전에는 수치 설계 완료로만 보고한다.

## 산출물
채워진 camera_spec.json, 후보 비교표, 분석 JSON, 샷별 선택 이유·미검증 항목을 인계한다. 기존 영상 제작 원장과 ID·시간·버전을 맞춘다. 프리비즈 실행 요청에는 `blender-previsualization`으로 인계하고, 그 밖의 실행·생성 라우팅은 `creative-production`에 맡긴다. 실제 촬영 가능한 리그·운영자 동선은 현장에서 재확인한다.

## 장소 공간 계약 (v5.1)

생산상 중요한 장소는 한 장의 establishing으로 잠기지 않는다. 위임된 경우 장소 마스터에 최소 4공간뷰(A establishing/master wide · B reverse master · C lateral/3-quarter · D top-down/isometric/floorplan-like)와 공간 앵커를 정의한다: origin, 방/거리 치수, 출입구·창 위치, 주요 가구/장애물, 광원 앵커, 인물 진입/이탈 지점, 필요 시 카메라 접근 구역. 복잡 공간은 뷰를 추가한다. 수치는 right-handed, X/Y 지면·Z 수직, 미터 단위를 권장하고 **추정값은 반드시 `ESTIMATED`로 표시**한다 — 꾸민 top-down 그림을 측정 평면도와 혼동하지 않는다. 장소 마스터는 `asset_registry`의 `role=master` 에셋이고, 씬별 조명/배치 상태는 `master_asset_ref` 버전 핀의 derivative로 인계한다(기록은 coordinator가 한다).

프로젝트에 등록할 명세는 `{id, type: camera_spec|spatial_spec, version, status, dependencies, dependency_versions, asset_ids}` 형태의 등록 제안으로 부모 coordinator에 반환한다(기록은 coordinator만 한다). 명세는 version과 artifact_id를 넣고, `spatial_spec.reconcile_project(project, spec, artifact_id)` 결과가 빈 목록일 때만 첨부 가능하다고 본다.
상세 제작 보드에서 호출되면 [완전한 스토리보드 계약](../video-production-assets/references/storyboard-contract.md)의 shot/scene/beat/panel 연결을 보존하고 선택 카메라의 크기·앵글·구도·무빙과 수치 artifact를 최종 보드에 인계한다. 시작·정점·끝 패널의 실제 프레임 위치를 camera_spec의 로컬 프레임과 대조한다. 필수 손 접촉/정보 공개가 가려지면 구도·패널 분할을 수정하도록 해당 ID로 보고한다. 수치 분석은 이미지 단독 스토리텔링 검수를 대신하지 않는다.

## 선택적 수치 미리보기
Pillow가 있으면 `python scripts/render_projection.py camera_spec.json wireframe.png`로 수학적 핀홀 와이어프레임 패널을 만들 수 있다. 실제 Blender 렌더가 아니며 가림·조명·연기는 시뮬레이션하지 않는다.

## 무빙 타이밍·렌즈 보완
카메라 무빙/초점/렌즈 또는 레퍼런스 기반 촬영 설계 요청에는 [무빙 타이밍·렌즈](references/motion-timing-lens.md)를 읽고 [시간표](assets/motion-timing-template.md)를 적용한다. 타이밍을 현재 camera_spec·피사체 행동·정보 공개 시점과 연결하고 스키마를 무단 확장하지 않는다. 레퍼런스 관찰은 camera-motion-reference-analysis, 생성 입력 변환은 ai-camera-control로 인계한다. 형제 스킬은 정확한 frontmatter name으로 찾는다. 프로그램은 [실행 환경](references/camera-programs.md)을 읽는다.
