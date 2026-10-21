# 실행·검수 절차

## 범위
지원: 원근 카메라, 수평 센서 fit, 정사각 픽셀, 카메라 look-at target와 roll, 렌즈 변화, 대역 위치 이동, 기본 장애물, 샷별 독립 scenes. 미지원: 기존 .blend의 비파괴 편집, 복잡한 리그/모션캡처/스킨, 줌렌즈 호흡, 왜곡/아나모픽, 물리 시뮬레이션, 최종 음성/자막, 자동 영상 인코딩.

## 어댑터
build_previs.py는 Blender Python(bpy)에서 실행한다. 수치 검사 정본은 형제 스킬의 `camera-spatial-design/scripts/spatial_spec.py`이며 두 스킬을 같은 루트에 설치한다. Blender Python 모듈 환경은 `python scripts/build_previs.py --spec ... --output ... --mode stills`도 사용할 수 있다. 처음에 새 파일을 초기화하고 실패/출력 파일을 덮어쓰지 않으므로 독립 프로세스와 새 출력 폴더를 사용한다. 출력 경로가 기존이면 실패한다. JSON 명세·분석·인계 파일은 UTF-8을 사용한다. `--mode stills --render-map`은 지정된 shot·로컬 0기준 프레임(또는 패널→프레임 대응표)만 정확히 렌더해 지도에 없는 샷·명세 밖 프레임을 거절한다; 검사(scene 구성·ray cast)는 전 샷·전 프레임을 유지한다. `--mode smoke`는 첫 샷만 구성하고 렌더는 1프레임·해상도 상한 320px로 묶인 좁은 파이프라인 검증이며 전체 명세 렌더 성공으로 보고하지 않는다.
smoke는 첫 샷·로컬 frame 0만 베이크/ray cast/렌더한다. 업스케일 없이 긴 변을 320px 이하로 줄이며 `smoke_resolution`에 실제 설정을 남긴다. numerical-analysis.json의 전체 프레임 분석은 unverified/not-run 범위로 기록하고, inspection scope도 첫 프레임만으로 제한한다. stills/sequence의 전 프레임 검사·전체 수치 분석은 유지한다. manifest.shot_links와 inspection은 전달된 scene/shot/beat ID, rendered 행은 panel ID와 로컬 frame을 보존한다.

## 카메라/타이밍
Blender 카메라는 로컬 -Z를 정면, +Y를 위로 사용하도록 to_track_quat로 배치한다. 피사체/카메라 위치·렌즈를 모든 프레임에 베이크하고 상수 세그먼트 사이도 LINEAR 키를 기록한다. Quaternion 부호를 연속하게 맞추되 실제 렌더는 정수 프레임에서 확인한다. fps와 로컬→Blender 프레임 변환은 계약을 따른다. roll은 로컬 +Z 회전이다.

## 대역 모드 (--proxy)
`--proxy box`(기본)는 피사체를 추상 직육면체로, `--proxy figure`는 같은 `size_m`에서 파생한 토르스·목·머리 구체 대역으로 만든다. figure 모드의 목적은 프레이밍·헤드룸·눈높이·실루엣 겹침·가림을 몸 형태로 읽게 하는 것이며, 얼굴 방향·자세·관절·손/소품 접촉·연기·최종 조명을 재현하거나 검증하지 않는다. 두 모드 모두 `camera-spatial-1.0` 스키마를 바꾸지 않고 같은 spec에서 파생된다. 사용한 모드는 manifest의 `proxy_mode`와 `scope`에 기록하고 렌더와 함께 인계한다.

## 어댑터 전용 선택 입력 (--focus-map · --look-cards · --engine)
`camera-spatial-1.0` 명세는 초점·룩 카드·엔진 필드를 갖지 않으며, 이 입력들은 **명세 바깥의 어댑터 옵션**이다. 명세 파일에 필드를 추가하지 않고, CLI로만 넘긴다.

- `--focus-map focus.json`: `{"SH01": {"f_number": 2.8, "keyframes": [{"frame": 0, "focus_distance_m": 4.0}, {"frame": 47, "focus_distance_m": 1.0}]}}`. 로컬 프레임은 명세 프레임 범위를 벗어나면 거부한다. 선형 보간 후 Blender DoF(focus distance·aperture f-stop)에 베이크한다. **래크 포커스 미리보기**이며 실제 렌즈 캘리브레이션·초점 품질·모션블러를 증명하지 않는다. 이 map은 카메라 소유자의 lens companion(초점 대상·거리·pull 시작/완료)에서 **파생**한 입력이지 두 번째 정본이 아니다. companion이 바뀌면 map을 재생성하고, 둘이 어긋나면 companion이 우선한다([파생 규칙](../../camera-spatial-design/assets/motion-timing-template.md)).
- `--look-cards cards.json`: `{"CH01": {"image": "/abs/path/approved_sheet.png"}}`. 주어진 subject box 크기에 맞춘 카메라 정면 평면 카드에 승인 이미지를 텍스처로 붙여 프레이밍 안에 보여 준다. 표시되는 것은 승인된 룩이며, **깊이·가림 순서·자세·접촉·연기를 증명하지 않는다.** 생성 입력으로 넘길 때는 [참조 역할 규칙](../../video-production-assets/references/29-reference-driven-production.md#reference-roles)대로 속성 단위로 가져오고 제외한다.
- `--engine cycles|eevee`: cycles가 기준 look(무CPU 저사양)이고 eevee는 빠른 미리보기다. 속도 차이는 품질 주장이 아니며, 최종 판정용 렌더는 기준 엔진으로 다시 만든다.

## MCP 표면 (선택)

패키지는 `blender-previsualization/mcp/blender_mcp_server.py`에 MCP 서버를 포함한다. 이 서버는 **동일 어댑터를 호출하는 얇은 실행 표면**일 뿐, 새로운 렌더 능력을 만들지 않는다.

- 도구: `blender_version`(호스트 Blender 버전), `blender_previs`(spec → 프리비즈 실행 + manifest 요약), `blender_previs_inspect`(완료된 출력 폴더의 manifest·inspection 요약, 읽기 전용).
- 제한: 사용자 제공 명령을 실행하지 않는다. 패키지된 `build_previs.py`만 Blender CLI로 호출한다. 설치·업데이트를 자동 수행하지 않는다. 기존 출력 폴더를 덮어쓰지 않는다. 경로는 반드시 절대 경로여야 하고, 누락된 런타임·명세는 오류로 보고한다.
- 어댑터 위치 확인: 서버는 `BLENDER_PREVIS_ADAPTER` → `BLENDER_PREVIS_SKILL_ROOT` → `~/.config/blender-mcp/skill_root` → 설치된 스킬 루트(`~/.codex/skills`, `~/.pi/agent/skills`, `~/.claude/skills`, `~/.agents/skills`) → 서버 옆 스킬 순서로 어댑터를 찾는다. cwd에 의존하지 않는다.

### 전역 등록 (저장소 경로에 묶이지 않게)

`python3 blender-previsualization/mcp/install_global_launcher.py [--update-pi]`를 실행하면:

1. `~/.local/bin/blender-mcp-server` 실행 명령을 설치하고,
2. 해석된 스킬 루트를 `~/.config/blender-mcp/skill_root`에 기록하고,
3. `--update-pi`를 주면 `~/.pi/agent/mcp.json`의 `blender` 항목을 실행 명령으로 바꾸고,
4. Codex `~/.codex/config.toml`에 붙여 넣을 스니펫을 출력한다.

```toml
[mcp_servers.blender]
command = "/home/<user>/.local/bin/blender-mcp-server"
startup_timeout_sec = 60
```

MCP 등록에 체크아웃 절대경로를 넣지 않으므로 저장소를 옮겨도 등록이 깨지지 않는다. 스킬이 다른 경로로 옮겨졌다면 `~/.config/blender-mcp/skill_root`를 갱신하거나 `BLENDER_PREVIS_SKILL_ROOT`를 지정한다. 호스트를 재시작하면 새 서버가 로드된다.

### 기준 경로

기준 경로는 여전히 CLI다. MCP로 돌렸더라도 산출물 5종과 manifest 기록이 같아야 하며, 다르면 CLI 경로로 되돌아가 재실행한다.

## 화면 검사
world_to_camera_view로 머리와 몸 중심의 화면 좌표·광학 깊이를 기록하고 scene.ray_cast로 같은 점을 바라볼 때 먼저 만나는 대역을 확인한다. 각 샷에서 다른 피사체가 움직이는 동안 가림을 전 프레임 검사한다. 장애물 중첩과 프레임 외 상태는 계획된 연출일 수 있으므로 자동 실패가 아닌 근거 있는 수정 판단으로 처리한다.

## 런타임 상태
이 기록은 2026-10-21 Linux(x86_64) 워크스테이션에서 독립 실행한 결과다. 실제 `Blender 5.2.2 LTS`(`/home/declan/.local/bin/blender`, build 2026-09-15)로 예제 `camera-spec-example.json`에 대해 `python3 camera-spatial-design/scripts/test_spatial_spec.py`(14 OK), `python3 blender-previsualization/scripts/test_build_previs.py`(17 OK), `BLENDER_EXECUTABLE=<blender> python3 blender-previsualization/scripts/test_camera_orientation_in_blender.py`(1 OK, 실제 Blender 실행)를 수행했다. `--mode smoke`는 640x360 명세에서 320x180 1프레임을 약 2초에, `--mode stills`(2샷 × 시작/중간/끝 6프레임, Cycles CPU 8 samples)는 약 12초에 렌더했고, `--proxy figure` 동일 조건은 약 20초, `--engine eevee`는 약 10초였다. `--focus-map`과 `--look-cards`를 함께 준 figure 렌더도 실제로 실행해 랙 포커스(프레임 0에서 카드 선명, 프레임 47에서 인물 선명)와 룩 카드 표시를 육안 확인했다. 이 스킬은 Blender CLI로 구동되며 Blender MCP 서버는 필요하지 않다. 과거 기록의 Windows 10 실행은 따로 두고, 다른 버전·플랫폼에는 일반화하지 말고 실제 버전/모드를 기록한다. Blender proxy ray cast는 중심·머리 주목점만 검사하며 전체 실루엣·연출·최종 미감을 보장하지 않는다. Blender 5.2.2 실행에서는 `World.use_nodes`와 `Material.use_nodes`의 6.0 제거 예정 deprecation 경고가 관찰되었다; 6.0 호환성을 선언하지 않는다.
