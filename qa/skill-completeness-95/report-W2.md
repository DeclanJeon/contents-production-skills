# W2 카메라·공간 인계 — 독립 검토 대기

점수 부여 없음. 기존 dirty 변경 보존, 커밋/설치/설정 변경/원격 업로드/유료 생성/훈련/배포/게시 없음. 사용자 계약에 따라 테스트·빌드·formatter·linter 및 fresh-agent 행동 평가는 실행하지 않았다. 아래 로컬 명령은 실제 실행한 비테스트 smoke다.

## 변경 파일과 결함

- `camera-spatial-design/SKILL.md`: M-04의 read-only/text-only 요청 다음에 렌더 스틸을 요구해도 standalone camera owner가 생성/Blender/파일 쓰기를 실행하지 않도록 명시. 기존 무조건적 Blender 절차와 text-only 범위 충돌을 해소하고 계획/렌더 검증을 구별.
- `camera-spatial-design/references/camera-design.md`: 실제 읽은 Katz/Block의 주장별 범위와 미검사 도판 명시.
- `camera-spatial-design/references/sources.md`: 과거 런타임 부재를 현재 사실처럼 쓰던 문장 교정. 실제 smoke 범위와 원문 rendition/줄/read-state 추가. 다른 책의 과거 읽기 기록을 이번 직접 읽기로 승격하지 않음.
- `camera-motion-reference-analysis/SKILL.md`, `ai-camera-control/SKILL.md`: Windows 등에서도 쓰는 독립 스킬에 고정 Linux 경로를 요구하던 문장을 현재 설치 루트/frontmatter name 탐색으로 교정.
- `camera-motion-reference-analysis/references/motion-analysis.md`, `assets/motion-analysis-template.md`: 추정별 qualitative confidence/근거/대안 및 읽기 실패 구간을 구조화. USER_REPORTED와 OBSERVED 구별. Block 원문 읽기 범위 추가.
- `ai-camera-control/references/control-contract.md`, `assets/camera-control-template.md`: source locator, 실제 version 또는 unversioned 상태, lens/gate/시간 누락 슬롯을 명시. push-in만으로 수치 렌즈·거리·길이를 만들지 않으며 provider field로 넘기지 않음.
- `blender-previsualization/references/blender-workflow.md`: 역사적 17개 경로/테스트 통과 기록과 이번 독립 smoke를 구분. 실제 deprecation 경고와 6.0 미검증 명시. 어댑터 코드는 수정하지 않음.
- `orchestrating-video-preproduction/SKILL.md`: later-render 문구가 독립 text-only lane의 생성 권한이 되지 않는다는 실행 경계 추가.
- `orchestrating-video-preproduction/references/video-direction.md`: shared spine 필드가 SKILL.md에 있다는 잘못된 포인터를 실제 `stage-execution.md`로 수정.
- QA: `claims-W2.tsv`, 이 보고서, `W2-numerical-analysis.json`, `W2-previs-smoke/` 실제 출력, `W2-subject-motion.mp4` 최소 합성 증거. 재현에 필요한 최소 fixture/출력으로 보존하며 제품 산출물이 아니다.

기존 Acceptance를 중복 추가하지 않았다. manifest/README/CHANGELOG/통합 원장/정본 sources.md는 수정하지 않았다.

## 직접 읽은 원문

1. `E:/Book/06_Book/originals/콘텐츠_제작/md/The Visual Story Creating the Visual Structure of Film, TV, and Digital Media Third Edition (Bruce Block) (z-library.sk, 1lib.sk, z-lib.sk).md`
   - SHA256 `403172711929152d7019ccbab9043fc0ba8c512606fc14375ef6e78cc410392c`, 368221 bytes.
   - READ-PARTIAL: L103–117, L161–173, L529–537. 본문 페이지 표지 51–58, 80–86, 264–268.
   - 지지: 상대 움직임/깊이 단서, subject와 camera 운동 구분, 줌/돌리 차이, matched framing에서 거리의 역할. 정확한 meter solve·렌즈 캘리브레이션·모든 회전의 균일 pixel velocity를 입증하지 않는다.
2. `E:/Book/06_Book/originals/콘텐츠_제작/md/Film Directing Shot by Shot Visualizing from Concept to Screen (Steven D. Katz) (z-library.sk, 1lib.sk, z-lib.sk).md`
   - SHA256 `e8ad5bf5ecc3659fb9b936dd081147a465b03ca09f53e6d690ca286fa4706e9a`, 535607 bytes.
   - READ-PARTIAL: L333–355, Chapter 6 Line of Action / Moving the Camera Over the Line; L595–597, Chapter 14 Camera Angles. 안정적인 원서 페이지 표지가 없어 chapter/section/줄을 locator로 사용.
   - 지지: screen direction/축/재정위, 앵글 의미의 맥락 의존성. 참조 도판은 열지 않았다.

추출/index를 직접 원문 읽기의 대체 근거로 쓰지 않았다. 위 파일 byte/hash는 PowerShell `Get-Item`/`Get-FileHash -Algorithm SHA256 -LiteralPath`로 확인했다. canonical source ID와의 대응은 W4가 통합해야 한다.

## 실제 실행 증거

### W2-NUMERIC

실행(종료 0):

```sh
python camera-spatial-design/scripts/spatial_spec.py camera-spatial-design/assets/camera-spec-example.json --out qa/skill-completeness-95/W2-numerical-analysis.json
```

관찰: `valid=true`, 24fps 두 샷 각 48프레임/2초, 전체 4초, warnings 각 빈 목록. SH01 카메라 속도 0; SH02 최대 유한차분 속도 0.9190102385791192m/s. SH02 camera Y=-5→-3.8m, CH01 X=-0.8→-0.4m, pair distance 1.6→1.2m, lens 35mm, horizontal FOV 54.43222311461495°. 단순 BBox의 이상적 핀홀 수치 검사이며 가림/실루엣/미감/물리 리그 증명이 아니다.

### W2-BLENDER

PATH 부재 보고를 재확인하지 않고 설치 경로를 glob으로 탐색해 `C:/Program Files/Blender Foundation/Blender 5.2/blender.exe`를 발견했다.

실행(모두 종료 0):

```sh
"C:/Program Files/Blender Foundation/Blender 5.2/blender.exe" --version
"C:/Program Files/Blender Foundation/Blender 5.2/blender.exe" --background --factory-startup --python blender-previsualization/scripts/build_previs.py -- --spec camera-spatial-design/assets/camera-spec-example.json --output qa/skill-completeness-95/W2-previs-smoke --mode smoke
"C:/Program Files/Blender Foundation/Blender 5.2/blender.exe" --background qa/skill-completeness-95/W2-previs-smoke/previs.blend --python-expr "import bpy; s=bpy.data.scenes['SH01']; print('W2_REOPEN', bpy.app.version_string, s.camera.name, s.frame_start, s.frame_end, s.render.resolution_x, s.render.resolution_y)"
```

실제 버전 5.2.2 LTS, build hash d13f752e3b9c, Cycles CPU. manifest status generated, SH01 local frame 0→Blender frame 1, 320×180 PNG. spec SHA256 `90345bf845c5876e5b684bc0b67baa333c8751b14e394c84ef2d193344b380a3`. 생성물: `previs.blend`, `SH01/frame_000001.png`, `manifest.json`, `blender-inspection.json`, `numerical-analysis.json`.

PNG를 read 도구로 실제 열었다: 청색 대역 왼쪽, 주황 대역 오른쪽, 둘의 전신과 바닥 접촉이 프레임 안에 있고 서로 겹치지 않으며 머리 위 여백이 보인다. 얼굴/손/연기는 없는 직육면체다. ray cast는 두 대역의 center/head 네 점 모두 visible=true. 재열기 stdout: `W2_REOPEN 5.2.2 LTS SH01_camera 1 1 320 180`. 새 process에서 `.blend`가 실제 열리는 것을 확인했다. 재열기 시 기존 BlenderMCP addon의 register/unregister 메시지가 보였지만 MCP 호출이나 설정 변경은 하지 않았다.

경고: World.use_nodes, Material.use_nodes의 Blender 6.0 제거 예정 DeprecationWarning. 현재 smoke는 성공했지만 6.0 호환성은 미검증. SH02와 움직이는 전 구간을 렌더했다고 주장하지 않는다. smoke의 numerical-analysis는 full analysis not-run/unverified이고 별도의 W2-NUMERIC만 전체 수치 경로를 계산했다.

### W2-MOTION

실행(종료 0):

```sh
ffmpeg -version
ffmpeg -n -f lavfi -i "color=c=gray:s=320x180:r=12:d=4,drawgrid=w=40:h=30:t=1:c=white" -f lavfi -i "color=c=red:s=24x40:r=12:d=4" -filter_complex "[0:v][1:v]overlay=x='40+40*t':y=90:shortest=1" -c:v libx264 -pix_fmt yuv420p qa/skill-completeness-95/W2-subject-motion.mp4
ffprobe -v error -select_streams v:0 -show_entries stream=width,height,r_frame_rate,avg_frame_rate,time_base,nb_frames,duration -show_entries format=duration -of json qa/skill-completeness-95/W2-subject-motion.mp4
```

FFmpeg 8.1.2 essentials, ffprobe 관찰: 320×180, 12/1 fps, 48프레임, 4초, time_base=1/12288, 무음. read 도구의 6프레임 preview grid 및 0s/3s 프레임을 실제 열었다.

채워진 관찰 brief:

| 범위 | 카메라 후보 | 피사체 | 렌즈 후보 | 근거/상태 | confidence/한계 |
|---|---|---|---|---|---|
| 샘플 0–3s와 4초 clip preview grid | 고정 배경에 대해 카메라 이동 증거 없음 | 빨간 사각형이 screen-right로 이동; 크기 유지 | 줌/초점 변화 증거 없음 | OBSERVED: 격자 위치 유지, 빨간 대역만 위치 변화 | 샘플 간 subject-only 설명 high; 실사 카메라의 정확한 정지/리그는 이 합성 raster fixture로 입증하지 않음 |

생성 명령의 ground truth는 static grid와 x=40+40t pixel overlay이며 3s에 nominal x=160이다. 이 값은 직접 측정 속도가 아니라 fixture 설계값이다. meters/degrees/lens를 역추정하지 않았다. 비디오 전체 재생은 수행하지 않았으므로 easing/진동/속도 일관성 등 동적 품질은 UNVERIFIED; frame-only smoke를 playback review라 부르지 않는다. 읽기 실패 구간은 없었지만 전 프레임을 시각 검사하지 않았다. 원본 영상이 없는 경계에서는 이 fixture를 사용자 참조처럼 대체하지 않고 `reference video/access missing`을 반환해야 한다.

## 실제 텍스트 산출물 — 자체 작성 사례, fresh-agent 평가 아님

### W2-TEXT-M04: kitchen plan / rendered-still 경계

가상의 두 인물 대화, 모든 공간 수치는 DESIGN_PROPOSAL/ESTIMATED. 오른손계 X=방 동쪽, Y=북쪽, Z=위, m. 방 4×3×2.6m, 남서 바닥 origin=(0,0,0). 북쪽 조리대 bottom center=(2,2.7,0), size=(3,0.6,0.9); 서남 출입문 x=0,y=0.4–1.2. A 발=(1.4,1.5,0), B 발=(2.6,1.5,0), 두 인물 시선 A↔B. 대화 축은 A→B, 카메라는 남쪽 negative side 유지.

- 후보 K1: position=(2,-2.0,1.55), target=(2,1.5,1.0), lens=35mm/gate=36mm, 16:9. 남쪽 벽 밖 위치이므로 **벽 제거/촬영 구역 승인 없이는 불가능한 후보**; 실제 방 안 카메라로 속이지 않는다.
- 후보 K2 선택안: position=(2,0.2,1.45), target=(2,1.5,1.15), lens=24mm/gate=36mm, 16:9. 반응 투샷 계획. 좁은 공간의 얼굴 원근·머리/팔 크롭·조리대 가림은 미검증이고 실제 spec/Blender 결과 전까지 최종 채택 아님.
- blocking: B는 (2.6,1.5,0)에 머물고 A가 말끝에 (1.6,1.5,0)으로 접근하는 제안. 손/서랍 접촉은 없음.
- 움직임 후보: 정지 투샷 우선. 접근에 맞춘 작은 push-in은 position=(2,0.2,1.45)→(2,0.4,1.45), target 유지라는 제안만 기록. 길이/FPS/시작·정지 cue가 없으므로 실행 명세는 BLOCKED; 임의 초 수를 확정하지 않는다.
- 가림/안전: 문 진입 동선과 리그 radius, 두 피사체의 머리/중심·팔, 북쪽 조리대와 대상의 겹침, 실제 방 치수와 camera clearance 확인 필요. 현재는 텍스트 계획만이며 숫자 example 결과를 이 kitchen의 검증으로 재사용하지 않는다.
- 렌더 스틸 후속 요구 답: 이 호출은 read-only/no-generation이고 camera-spatial-design은 이미지 출력 owner가 아니다. 지금 렌더/파일 생성은 하지 않는다. 위 제안·미정·축·참조를 storyboard/image 실행 owner에 handoff하되 현재 no-generation 조건을 그대로 전달한다. coordinator 미로드 상태에서도 같다.

### W2-CONTROL: 검증 예제와 누락 입력

source=`camera-spatial-design/assets/camera-spec-example.json` / shots[1], CAM01 v1.0, SH02/S01, project dialogue-distance-previs. 모델 중립, provider_inputs={}. local frames 0–47 at 24fps, duration=2s, 640:360, RH X/Y floor Z-up meters. camera (0,-5,1.6)→(0,-3.8,1.6), target (0,0,0.85)→(0.15,0,0.85), 35mm/36mm gate, smoothstep. CH01 (-0.8,0,0)→(-0.4,0,0), CH02 stationary (0.8,0,0). 전부 SOFT_PROMPT, 실제 모델의 path/lens 강제력은 UNVERIFIED. prompt: 두 대역의 간격을 보이며 CH01의 작은 접근에 맞춰 카메라도 천천히 전진하고, 고정 초점거리와 화면 좌우 관계를 유지한다. 두 대상이 끝 프레임에도 보이고 축 negative side를 유지해야 한다. onset/settle은 해당 smoothstep의 endpoint 설계이며 공개/접촉 cue는 이 소스에 없다. 생성 결과를 관찰했다고 하지 않는다.

경계 source=`supplied text: push in`, unversioned, shot ID 미제공. lens/gate/duration/FPS/onset-stop/path=UNRESOLVED. qualitative SOFT_PROMPT 초안은 가능하지만 실제 수치 directive와 provider_inputs는 비워 두고 camera-spatial-design에 누락 슬롯을 반환. 35mm/2m/4s를 예제에서 복사하지 않는다.

### W2-PACKAGE: 단일 합성 소재의 stage handoff

입력: 허구의 무성 12초 16:9 단편, 한 번에 텍스트 package, 소재/결말/창작 선택은 이 사례에서 제안으로 위임. 현관 앞 택배 기사가 비 맞는 종이상자를 보고 비를 피할 위치로 옮긴 뒤 떠난다. 실존 배송 서비스 능력 주장 없음. 이하 모든 창작 설정 DESIGN_PROPOSAL, 승인 상태 proposed, 미디어 생성 없음.

1. 공유 spine: 목적=작은 배려의 선택, 관객=미정, 감정=걱정→안도, tone=절제, dialogue=없음, 엔딩=기사는 떠나고 상자는 처마 밑. prop=테이프 봉인 갈색 상자, 인물=허구 기사 1명. 방향/색/시간은 아래와 공유.
2. Concept/logline: 서두르던 기사가 젖는 상자를 발견해 발걸음을 멈추고, 마지막 순간 상자를 처마 안으로 옮긴다.
3. Synopsis: 빗물이 상자 모서리로 떨어진다. 떠나려던 기사는 이를 보고 돌아선다. 양손으로 같은 상자를 들고 처마 밑에 놓은 뒤 떠난다. 봉인 상태는 유지된다.
4. Beats: B01 0–3s 발견; B02 3–8s 선택/이동; B03 8–12s 결과/이탈. scene S01 하나. 합계 12s는 authored timing proposal이지 촬영 관찰값이 아니다.
5. Persona/sheet text: C01 허구 기사; 목표=배송 마치기, 마찰=서두름/상자 젖음, 선택 규칙=상자를 손상 없이 둘 수 있으면 잠시 돌아와 보호. identity proposal=회색 방수 재킷·짙은 바지·짧은 머리; invariant=같은 재킷/상자; variant=이동 중 젖음. 표정=상자 확인→짧은 결심→중립; 실존 인물 진단/유형 없음. 무성 역할 voice N/A. sheet prompt=중립 배경, 동일 인물 정면/측면/후면과 재킷 세부를 보여주는 참조시트 설계. 실제 identity image 없음.
6. Visual Bible: 빗물/갈색 상자/회색 재킷/처마라는 anchor. 화면상 젖는 곳은 왼쪽, 안전한 처마는 오른쪽이라는 제안. 상자 봉인/모양 동일; B02에서 양손 소유, B03에서 바닥 소유. 실제 장소 치수/빛/카메라/참조 파일은 미정.
7. Indexed board text:
   - P01/S01/SH01/B01, 0–3s: 상자에 빗물, 떠나던 기사가 돌아봄. intended camera=둘의 관계가 읽히는 wide 제안; audio=비 제안; prompt=처마 경계 밖 갈색 상자와 돌아보는 기사. 렌즈/좌표는 미정.
   - P02/S01/SH02/B02, 3–8s: 양손으로 상자를 들어 오른쪽 처마 밑에 놓음; camera=손 접촉과 착지가 보이는 framing 제안; audio=옷/상자 접촉 제안; prompt=같은 상자와 양손, 오른쪽 안전구역으로 이어지는 동작. 실제 contact frame/가림은 미정.
   - P03/S01/SH03/B03, 8–12s: 상자는 처마 밑에 정지, 기사는 화면 밖 이탈; camera=결과 hold 제안; audio=빗소리 유지 제안; prompt=마른 구역의 같은 봉인 상자와 떠나는 기사.
8. 단일 requirement packet: SH01–03 camera_spec 좌표/렌즈/게이트/FPS/version 및 장소 치수·처마 경계→camera owner 입력 필요; SH02 접촉/착지 frame과 실제 가림→spatial/board 입력 필요; 전 샷 rain VFX 방식·안전 제약, ambience source/권리/음량→담당 owner 입력 필요; speech/lipsync=N/A(무성); identity image/실제 board render=후속, 현재 생성 금지. 이 packet은 creative-production에 반환하며 새 coordinator/승인 원장을 만들지 않는다.
9. Consistency: B01→B02→B03, 모든 panel source mapping, prop possession 변화와 12초 합계 일치. 기술 입력이 없으므로 **완성 production board는 BLOCKED**이고 rough board를 완성품으로 재명명하지 않는다. 텍스트 package의 기술 미정은 위 packet으로 납품한다. 검토/수락/지출/생성 권한은 부여되지 않는다.

## 미해결 근거와 cross-owner 요청

- W4 요청: 위 Block/Katz의 exact rendition/hash/bytes/read-scope를 canonical `video-production-assets/references/sources.md`와 대응해 달라. 이 보고/원장은 정본 규칙 파일이 아니다.
- Kenworthy/Master Shots, Lumet, Stanchfield, Williams 원문은 이번 작업자가 직접 읽지 않았다. 특히 timing/spacing/gesture/초점 연출 등 Block/Katz의 읽은 구간이 지지하지 않는 load-bearing craft는 claims의 unsupported/unverified로 남겼다. 기존 표의 제목을 읽음 증거로 쓰지 말 것. 독립 reviewer는 관련 주장별 직접 근거가 추가되기 전 rubric modifier/cap을 적용해야 한다. 외부 자료가 불가능하다고 진단한 것은 아니므로 U3 사용자 요청은 아직 하지 않는다.
- model-neutral packet만 작성했고 provider 공식 schema 조회/실제 control 지원/영상 생성 성공은 검증하지 않았다. provider-specific HARD_CONTROL을 주장하지 않는다.
- 원문 도판, 실제 kitchen 치수, 전체 동영상 playback, SH02 전체 렌더, 독립 행동 평가 미실행. 보유 자료로 후속 검증할 수 있는 항목이며 사용자에게 재조사를 요구하지 않는다.
- 리더 요청: 공유 changelog/version 정책에 따라 위 실제 변경을 기록하고 최종 상대 링크/독립 설치 접근성을 검사해 달라. 스킬 본문의 QA report 경로 표기는 checkout 기준 증거 locator이며 독립 설치의 필수 runtime resource가 아니다.

## 통합 후 정확한 smoke/test 명령 — 아직 실행하지 않음

아래는 부모의 공유 편집 완료 후 실행할 명령이다. output 디렉터리가 이미 존재하면 새 이름을 사용해야 하며 덮어쓰지 않는다.

```sh
python camera-spatial-design/scripts/test_spatial_spec.py
python blender-previsualization/scripts/test_build_previs.py
powershell -NoProfile -Command "$env:BLENDER_EXECUTABLE='C:/Program Files/Blender Foundation/Blender 5.2/blender.exe'; python blender-previsualization/scripts/test_camera_orientation_in_blender.py"
"C:/Program Files/Blender Foundation/Blender 5.2/blender.exe" --background --factory-startup --python blender-previsualization/scripts/build_previs.py -- --spec camera-spatial-design/assets/camera-spec-example.json --output qa/skill-completeness-95/W2-integration-stills --mode stills
python scripts/check_versions.py
```

stills 출력의 SH01/SH02 시작·중간·끝 PNG를 실제 열어 수치 분석/ID와 대조해야 한다. read-only M-04 fresh session은 `camera-spatial-design`만 로드하고 기존 frozen prompt를 사용해 생성·파일·Blender 호출이 없는지 도구 기록으로 판정할 것. camera-motion은 missing video와 USER_REPORTED-only 경계, ai-camera는 lens/timing 없는 push-in, orchestrating lane은 text-only later-render와 단일 artifact/다중 stage를 각각 fresh session에서 판정할 것. 해당 runner의 manifest/run-dir은 리더/W0가 소유하므로 임의 파일명/ID를 발명하지 않았다. 이 명령 목록은 실행 성공 증거가 아니다.
