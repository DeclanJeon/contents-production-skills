# 첨부 자료와 구현 근거

첨부 정상 본문을 선별 검토했으며 전권 정독·도판 복구를 뜻하지 않는다. 원문을 재배포하지 않는다. 좌표 계약·검증기·Blender 어댑터는 원리를 실행으로 연결하기 위한 독자 구현이다.

| 자료 | 탐색 표지 | 적용 |
|---|---|---|
| 05 Steven D. Katz, Film Directing Shot by Shot | Line of Action; Shot Plan; camera movement | 샷의 서사적 목적, 축·카메라 위치·거리·시점, 커버리지 |
| 06 Christopher Kenworthy, Master Shots | Pan and Slide; Dolly; Dramatic Shift | 카메라와 피사체의 상대 이동, 이동의 동기와 종결 |
| 07 Christopher Kenworthy, Master Shots Vol. 2 | Thresholds; Power; Claustrophobic Space | 인물 사이 거리·장벽·시선·프레임 분리와 관계 |
| 08 Bruce Block, The Visual Story | Depth Cues; Flat Space; Telephoto Lenses | 깊이 단서, 공간 대비, 위치/거리와 화각의 구분 |
| 04 Sidney Lumet, Making Movies | rehearsal; camera; theme | 제약 안에서 리허설과 부서 간 선택을 조율 |
| 15 Walt Stanchfield, Drawn to Life | gesture; pose | 대역의 실루엣과 포즈 가독성 검사 필요 |
| 16 Richard Williams, The Animator’s Survival Kit | timing; spacing | 카메라/인물 타이밍과 위치 변화의 구분 |

01 Film Lighting는 공백뿐이라 제외했다. 03/06은 글자 간 과도한 OCR 공백이 있으며 06의 표지를 공백 제거해 정상 의미가 확인되는 구간만 활용했다. 탐색 표지는 첨부 텍스트의 구간명이며 원서 페이지 번호가 아니다.

## Blender 공식 기술 참고
- Camera: https://docs.blender.org/api/4.5/bpy.types.Camera.html (lens, sensor fit)
- Projection: https://docs.blender.org/api/4.4/bpy_extras.object_utils.html (world_to_camera_view)
- Orientation: https://docs.blender.org/api/main/mathutils.html (to_track_quat)
- Save: https://docs.blender.org/api/4.5/bpy.ops.wm.html (save_as_mainfile)

공식 검색 결과로 API 표지를 확인했다. 문서 본문 fetch는 접근 오류가 있어 통독하지 못했다. 현재 제작 환경에는 Blender/bpy가 없고 설치 탐색도 실패했다. 스크립트는 Python 구문·명세 계산을 검사했지만 Blender 런타임 렌더는 미검증이다. 실제 환경에서 smoke test 후 버전·엔진·출력을 기록한다. 특정 최신 버전에서 정상 동작한다고 확정하지 않는다.
