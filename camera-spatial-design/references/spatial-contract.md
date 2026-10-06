# 카메라 공간 계약 1.0

## 좌표·렌즈·시간
월드 좌표는 오른손계, X/Y=수평 바닥, Z=위, 단위 m다. 피사체 position은 발/밑면 중심이다. 카메라 position은 광학 중심이며 target은 실제 월드의 바라보는 점이다. 방향 벡터는 target-position이다. 화면의 오른쪽은 월드 X와 항상 같지 않다.

출력은 정사각 픽셀, HORIZONTAL 센서 fit, shift=0인 원근 카메라만 지원한다. sensor_width_mm은 가로 게이트이며 유효 세로 게이트는 sensor_width_mm*height/width다. 실제 센서 전체 높이·아나모픽·왜곡·렌즈 시프트·정사영은 이 명세 밖이다. fov_x=2*atan(sensor_width_mm/(2*lens_mm)); fov_y는 유효 세로 게이트로 계산한다. 이 값은 이상적인 핀홀 화각이며 실제 렌즈 캘리브레이션을 대신하지 않는다.

fps는 양의 정수다. 샷은 독립적인 로컬 frame 0..duration_frames-1, JSON 키프레임은 처음과 마지막 프레임을 포함한다. Blender에서는 프레임 +1로 변환한다. 전체 편집 타임라인은 샷 배열 순서로 이어 붙인다. 카메라 좌표·바라보는 점·렌즈·피사체 위치는 매 프레임 샘플링한다. `interpolation`은 linear 또는 smoothstep이고 smoothstep은 각 구간의 가감속이지 전체 속도 연속을 보장하지 않는다. 급변하는 구간은 더 많은 점을 추가하거나 선형 속도 구간으로 설계한다.

## JSON
필수: schema_version=camera-spatial-1.0, project_id, fps, resolution=[width,height], subjects, obstacles, shots. 선택: version(명세 내용 버전, schema_version과 별개), artifact_id(이 명세가 내용 버전을 제공하는 원장 artifact ID).
subjects: id, size_m=[가로,깊이,높이], position=[x,y,z], color_rgba(선택). 대역은 직육면체이며 실제 인체·실루엣이 아니다.
obstacles: id, size_m, position(밑면 중심). 단순 장애물만 사용한다.
shot id는 파일 경로에도 사용하므로 ASCII 영문·숫자·밑줄·하이픈만 허용한다. 기존 ID가 다른 형식이면 원장에 대응표를 두고 안전한 파일용 ID를 사용한다.

shots: id, scene_id, purpose, duration_frames, subject_ids, motion_reason, camera, subject_tracks, axis.
camera: sensor_width_mm, lens_mm, clip_start_m, clip_end_m, roll_deg, clearance_radius_m, interpolation, keyframes=[{frame,position,target,lens_mm?}]. 키프레임 렌즈 생략 시 camera.lens_mm이다. roll은 카메라 로컬 +Z축 회전이며 실제 리그 회전 제약과 별개다.
subject_tracks: [{subject_id, interpolation, keyframes:[{frame,position}]}]. 없는 트랙은 기본 위치를 유지한다.
axis: null 또는 {a_subject_id,b_subject_id,allowed_side: positive/negative/either,exception_reason}. 바닥면 A→B 벡터와 A→카메라 벡터의 2D 외적 부호로 측면을 판정한다. 이는 180도 룰의 기하 보조값이며 시선·이동 축·중립 샷은 사람이 확인한다. 의도적으로 넘으면 exception_reason에 관객 재정위 방법을 기록한다.

## 검사 범위
validator는 자료형·고유 ID·유효 참조·프레임·양의 렌즈·위치/타겟 퇴화 등을 검사한다. analyze는 모든 프레임의 거리·화각·카메라 속도·직육면체 화면 경계·축·대역 장애물과의 충돌 가능성을 계산한다. 후면·프레임 외 대역은 경고이며, 인서트/클로즈업에서 의도된 크롭이면 설계 노트로 설명한다. clearance_radius_m은 구형 카메라 리그 대역이다. 충돌 검사는 이를 둘러싼 AABB의 보수적 중첩이고 움직이는 대역도 고려한다. 실제 리그·운영자·케이블의 이동 가능성을 증명하지 않는다.

가림은 실제 Blender 장면의 ray cast로 주목 점(머리/중심)만 검사한다. 점이 보인다고 몸 전체가 보이는 것은 아니다. 렌더의 머리 여백·손·접촉·표정·구도·서사 의도는 실제 미리보기에서 확인한다.

## 인계
샷 ID와 scene_id는 기존 video-production-assets의 원장을 그대로 사용한다. 시간은 duration_frames/fps이며 shot start/end 초를 원장에 기록한다. 좌표 명세 버전을 바꾸면 프리비즈·샷 설명·AI 프롬프트를 stale로 표시한다. camera_spec.json은 좌표의 단일 원장이다. `.blend`의 수동 수정은 명세에 되돌려 반영하고 다시 생성한다.

## 원장 등록·정합
프로젝트에 등록된 명세는 원장 artifact(type camera_spec 또는 spatial_spec)에 version으로 연결한다: spec.version==artifact.version, spec.artifact_id는 그 artifact ID다. 등록 가능 여부는 `spatial_spec.reconcile_project(project, spec, artifact_id)`가 검사하며 빈 오류 목록이면 통과다. 프로젝트 ID·fps·scene_id·샷 duration_frames(≈(end_s-start_s)*fps)·subject↔character/asset 참조와 역방향(이 artifact를 참조하는 numeric 샷이 명세에 있는지)을 확인한다. 명세는 샷 부분집합이어도 되지만 이 artifact를 가리키는 프로젝트 샷은 모두 명세에 있어야 한다. 단독 명세는 version 없이 유효하지만 프로젝트에 첨부하려면 version/artifact_id가 필요하다.
