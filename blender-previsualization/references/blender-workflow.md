# 실행·검수 절차

## 범위
지원: 원근 카메라, 수평 센서 fit, 정사각 픽셀, 카메라 look-at target와 roll, 렌즈 변화, 대역 위치 이동, 기본 장애물, 샷별 독립 scenes. 미지원: 기존 .blend의 비파괴 편집, 복잡한 리그/모션캡처/스킨, 줌렌즈 호흡, 왜곡/아나모픽, 물리 시뮬레이션, 최종 음성/자막, 자동 영상 인코딩.

## 어댑터
build_previs.py는 Blender Python(bpy)에서 실행한다. 수치 검사 정본은 형제 스킬의 `camera-spatial-design/scripts/spatial_spec.py`이며 두 스킬을 같은 루트에 설치한다. Blender Python 모듈 환경은 `python scripts/build_previs.py --spec ... --output ... --mode stills`도 사용할 수 있다. 처음에 새 파일을 초기화하고 실패/출력 파일을 덮어쓰지 않으므로 독립 프로세스와 새 출력 폴더를 사용한다. 출력 경로가 기존이면 실패한다. JSON 명세·분석·인계 파일은 UTF-8을 사용한다. `--mode stills --render-map`은 지정된 shot·로컬 0기준 프레임(또는 패널→프레임 대응표)만 정확히 렌더해 지도에 없는 샷·명세 밖 프레임을 거절한다; 검사(scene 구성·ray cast)는 전 샷·전 프레임을 유지한다. `--mode smoke`는 첫 샷만 구성하고 렌더는 1프레임·해상도 상한 320px로 묶인 좁은 파이프라인 검증이며 전체 명세 렌더 성공으로 보고하지 않는다.
smoke는 첫 샷·로컬 frame 0만 베이크/ray cast/렌더한다. 업스케일 없이 긴 변을 320px 이하로 줄이며 `smoke_resolution`에 실제 설정을 남긴다. numerical-analysis.json의 전체 프레임 분석은 unverified/not-run 범위로 기록하고, inspection scope도 첫 프레임만으로 제한한다. stills/sequence의 전 프레임 검사·전체 수치 분석은 유지한다. manifest.shot_links와 inspection은 전달된 scene/shot/beat ID, rendered 행은 panel ID와 로컬 frame을 보존한다.

## 카메라/타이밍
Blender 카메라는 로컬 -Z를 정면, +Y를 위로 사용하도록 to_track_quat로 배치한다. 피사체/카메라 위치·렌즈를 모든 프레임에 베이크하고 상수 세그먼트 사이도 LINEAR 키를 기록한다. Quaternion 부호를 연속하게 맞추되 실제 렌더는 정수 프레임에서 확인한다. fps와 로컬→Blender 프레임 변환은 계약을 따른다. roll은 로컬 +Z 회전이다.

## 화면 검사
world_to_camera_view로 머리와 몸 중심의 화면 좌표·광학 깊이를 기록하고 scene.ray_cast로 같은 점을 바라볼 때 먼저 만나는 대역을 확인한다. 각 샷에서 다른 피사체가 움직이는 동안 가림을 전 프레임 검사한다. 장애물 중첩과 프레임 외 상태는 계획된 연출일 수 있으므로 자동 실패가 아닌 근거 있는 수정 판단으로 처리한다.

## 런타임 상태
제작 시점 환경에는 Blender가 없어 어댑터 런타임은 미검증이다. spatial_spec.py의 실제 계산과 회귀 테스트, build_previs.py의 compile 검사만 통과했다. Blender 사용 가능 환경에서 버전·엔진을 기록하고 1프레임 smoke test, .blend 재열기, 프레임 수와 미리보기 확인을 수행해야 한다. 제어 가능한 API 버전 범위를 추측해 선언하지 않는다.
