# 첨부 자료와 구현 근거

아래 직접 읽기 항목만 읽음 증거다. 선별 본문 검토는 전권 정독·도판 복구를 뜻하지 않으며 원문을 재배포하지 않는다. 좌표 계약·검증기·Blender 어댑터는 원리를 실행으로 연결하기 위한 독자 구현이다.

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

이전 환경에서는 공식 검색 표지만 확인했고 문서 본문 fetch가 실패했다. 그 기록은 현재 런타임 부재의 근거가 아니다. 2026-10-16 W2는 설치 경로의 Blender 5.2.2 LTS를 직접 실행하고 기존 예제의 Cycles CPU smoke 프레임을 생성했다(`qa/skill-completeness-95/report-W2.md`); 이는 첫 샷·첫 프레임에 한정된다. API 버전 전체 호환성이나 전체 장면 검수를 뜻하지 않으며 실행마다 실제 버전·모드·열어 본 출력을 기록한다.

## 이번 직접 읽기 범위

- Bruce Block, *The Visual Story*, third edition: `E:/Book/06_Book/originals/콘텐츠_제작/md/The Visual Story Creating the Visual Structure of Film, TV, and Digital Media Third Edition (Bruce Block) (z-library.sk, 1lib.sk, z-lib.sk).md` lines 103–117, 161–173, 529–537, `READ-PARTIAL` (본문 페이지 표지 51–58, 80–86, 264–268). 상대 움직임·깊이 단서·줌/돌리 구별만 지원한다. 도판을 직접 열었다거나 렌즈 캘리브레이션·정확한 3D 복원을 검증했다는 뜻이 아니다.
  - 정확 rendition: 368221 bytes, SHA256 `403172711929152d7019ccbab9043fc0ba8c512606fc14375ef6e78cc410392c`. 읽기 주체 W2; E2는 파일 식별만 재확인했다.
- Steven D. Katz, *Film Directing Shot by Shot*: `E:/Book/06_Book/originals/콘텐츠_제작/md/Film Directing Shot by Shot Visualizing from Concept to Screen (Steven D. Katz) (z-library.sk, 1lib.sk, z-lib.sk).md` lines 333–355 (Chapter 6, Line of Action), 595–597 (Chapter 14, Camera Angles), `READ-PARTIAL`. 축의 연속성·관객 재정위와 앵글 의미의 맥락 의존성만 지원한다. 텍스트 rendition에서 안정된 페이지 표지는 없어 chapter/section·줄 위치로 특정하며 도판은 미검사다.
  - 정확 rendition: 535607 bytes, SHA256 `e8ad5bf5ecc3659fb9b936dd081147a465b03ca09f53e6d690ca286fa4706e9a`. 읽기 주체 W2; E2는 파일 식별만 재확인했다.
- E2 직접 읽기(아래 각 인용은 `READ-PARTIAL`; 공통 루트 `E:/Book/06_Book/originals/콘텐츠_제작/md/`, 파일명은 생략 없이 표기). 해시/바이트는 실제 읽은 Markdown rendition 기준이다. 원문 도판은 열지 않았다.
  - **E2-WILLIAMS** — `The Animators Survival Kit, Expanded Edition A Manual of Methods, Principles and Formulas for Classical, Computer, Games,… (Richard Williams) (z-library.sk, 1lib.sk, z-lib.sk).md`, 390099 bytes, SHA256 `dd1d17e5d57695a274c531287cdf1dce76785229280b0ae68bf850a51e4ca9ef`, L95–97, “It's All in the Timing and the Spacing”, p.36 및 다음 본문. 사건/접촉의 발생 시각과 프레임 간 위치 간격을 구별하고 움직임으로 확인한다는 원리만 지원한다. 카메라 easing 공식이나 물리 리그 한계의 근거가 아니다.
  - **E2-PEARLMAN** — `Cutting Rhythms Shaping the Film Edit (Karen Pearlman) (z-library.sk, 1lib.sk, z-lib.sk).md`, 547079 bytes, SHA256 `e09d86df3f28ef5e4351e16296a0e26528dfc1ca78aff9abc2c4a7962744e49e`, L119–121, Chapter 2, pp.29–30, Pulse / Movement Phrases. 강조점·움직임 구절 및 카메라/배우/대사/음향의 리허설 조율을 지원한다. 정해진 hold 초 수나 관객 반응의 보장은 지원하지 않는다.
  - **E2-LUMET** — `Making Movies (Sidney Lumet) (z-library.sk, 1lib.sk, z-lib.sk).md`, 387668 bytes, SHA256 `d659269b667d5e48c3669c2aade7c20069a28429715513dfc230ef3cd1ff977f`, L103, p.51. 읽기→블로킹→촬영 선택, 배우 동선 후 촬영감독 run-through, 예산/장소/스케줄 제약의 사례를 지원한다. 모든 제작에 고정 리허설 기간을 요구하지 않는다.
  - **E2-STANCHFIELD** — `Drawn to Life 20 Golden Years of Disney Master Classes Volume 1 (Hahn, DonStanchfield, Walt) (z-library.sk, 1lib.sk, z-lib.sk).md`, 652080 bytes, SHA256 `a765d6b75e1945ae217ed121a33ff6bbfd7acc40362bd55d8ba7210763bd586c`, L67–69, pp.15–16, Line and Silhouette / Basic Shapes versus Details; L223, p.93, Silhouette. 디테일보다 행동·포즈의 실루엣 가독성을 먼저 검사한다는 원리만 지원한다. BBox가 손·표정·연기를 검증한다는 근거가 아니다.
  - **E2-KENWORTHY1** — `Master shots 100 advanced camera techniques to get an expensive look on your low-budget movie (Christopher Kenworthy) (z-library.sk, 1lib.sk, z-lib.sk).md`, 530649 bytes, SHA256 `fcfc5a01f7b6231ce1cbaf4bad37f390cea882e4e4fb4b6d9b69e83a3626e618`, L175 (5.1 Focus In, p.80), L183 (5.3 Pan and Slide, p.84), L301 (8.4 Reflections, p.146). OCR는 글자 사이 공백이 크지만 해당 문장을 직접 읽었다. 반응에 맞춘 push-in, 별도 배우 회전/카메라 병진·팬 조율, 전경/반사상 초점 선택으로 주의를 유도하는 사례를 지원한다. 효과를 보편 법칙으로 쓰거나 도판 배치를 복원하지 않는다.
  - **E2-KENWORTHY2** — `Master Shots Volume 2 Shooting Great Dialogue Scenes (Christopher Kenworthy) (z-library.sk, 1lib.sk, z-lib.sk).md`, 204606 bytes, SHA256 `86512c9fea5c50550832c5b5fae45ff9906dfb3763066d3560f918557cfcf97b`, L47 (1.5 Barrier), L57 (1.8 Swing to Cut의 끝), L83 (2.7 Focus on One), L103 (3.4 Threshold). 장벽/문턱의 관계 표현, 특정 컷 전 settle, push-in 중 초점 유지의 사례만 지원한다. 페이지 표지는 없으므로 section/line으로 특정한다. 모든 컷에 정지/긴 렌즈를 강제하지 않는다.

좌표/단위/스키마·원장 연결·검사 상태는 자체 구현 계약이며 책의 권위로 API 동작을 입증하지 않는다. 광학 호흡·왜곡·정량 심도·모션블러, 실제 focus pull 결과, 리그 가능성은 위 읽기로 검증되지 않는다.
