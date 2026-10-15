# V003 — Vans / Off the Wall 스케이트보드 필름 (파일명 표기만으로 확인)
[← 전체 영상 색인](../video-index.md)

## 출처와 확인 범위
- 안정 ID `sha256:3d59ee745d61d24da66c10ae909b941750af1dcf5249ecf39f2d288f8d20efc1`; 원본 파일명 `@vans - Off the Wall ｜ #AI spec ad ｜ Google Veo 2.mp4`. 파일명 표현만으로 공식성/공급자 사용을 입증하지 않는다.
- 길이 53.875초; 1920×1080; 24fps; time_base 1/12288, 시작 PTS 0, duration_ts 662016; AV1; AAC 44.1kHz stereo.
- 전체 decode와 FFmpeg 점수 이벤트 추출 rc=0 (`evidence/V003/ffmpeg-decode-scene.log`). 묶인 45개 검출 주변을 원본 PTS 라벨이 있는 시트에서 검토했다(C01–C45; `candidate-neighborhoods.json`, `candidate-neighborhood-sheets/neighborhood-001.jpg`–`-023.jpg`). 이벤트에는 장면 교체, 동작 정점, 샷 내부 움직임이 섞여 있으며 C ID는 shot ID가 아니다.
- **FRAMES_REVIEWED:** 정수초 0–53 nearest source-PTS 프레임 54개와 45개 grouped neighborhood(135 frames)를 검토했다. raw 보충 pass에서 49 events의 native n−2/n/n+2 145 unique frames/7 strips를 추가 시각 확인했다(`evidence/raw-review-V003/`, [원장](../raw-candidate-coverage-first24.json)). 첫 표본 PTS0.000; 실제 마지막 n=1292/PTS53.833333 (`evidence/V003/native-terminal.jpg`)에서 발 위 흰 `Off the Wall` 글자가 움직임과 함께 남는다. 53.9초 요청이 아니라 native terminal을 확인했다. 연속재생 아님; 이웃 프레임 사이의 continuous speed/handheld/settling 및 검출기가 놓친 cuts는 미검증.
- ASR: 오프라인 faster-whisper small CPU int8/local-files-only 가설(`evidence/V003/asr-hypotheses.json`), 영어 7구간 약 1.94–53.61초. 실제 음성 청취는 하지 않았다. 기계 텍스트는 확인된 VO나 공식 copy가 아니다. AAC가 있어도 음악/SFX/환경음/레벨/mix는 UNKNOWN.

## 해석상 장면 그룹과 자산
**G01 (해석, 확신 높음):** 도시형 스케이트/lifestyle 몽타주다. Vans 표식이 있는 검정 캔버스화, 보드, 콘크리트 bowl, 그래피티 벽, 난간, 거리/지하철/상점 질감과 여러 라이더가 반복된다. 도시 brand opener→신발·보드 detail→라이딩 트릭→짧은 어둠/거리 삽입→crew 반응→hero shoe와 `Off the Wall` 순이다. 실제 위치들이 같은 지리공간인지는 확인되지 않았다.

**보이는 역할:** 보드를 든 젊은 여성, 그래픽 deck을 든 흑인 여성, 어두운/노란/흰 상의를 입은 여러 남성-presenting skater, 붉은 머리·어두운 상의·찢어진 청바지의 젊은 여성, 환호하는 친구 무리가 보인다. 실명 cast는 확인되지 않았다. “반항적/젊음/진정성” 같은 persona는 해석이지 사실/심리진단이 아니다.

**자산 연속성:** 여러 보드·바퀴·그래픽 deck과, 흰 고무 sidewall/끈/붉은 heel·side label의 검정 캔버스 high-top/low-top 신발이 반복된다. 끈 묶기 detail에서 Nike swoosh가 보이는 양말/신발도 있으므로 이를 Vans shoe logo로 오인하지 않는다. 모델·브랜드 tie-in은 확인되지 않았다. 난간, bowl, 지하철 창, 웅덩이, 그래피티는 movement surface로 재등장한다.

## 시간순 화면 증거 (candidate event; 컷 ID와 일대일 대응 아님)
각 candidate event의 실제 검토 source-frame PTS는 표에 bracket으로 적힌다. `pre → center → post`는 약 ±0.12초의 세 점이지 정확한 마지막/첫 cut-frame 쌍은 아니다. 이 neighborhood에서 구도가 다른 것은 관찰할 수 있으나 hard cut과 짧은 transition은 구분되지 않을 수 있다. detector가 놓친 경계도 가능하다.

| 후보 이벤트 | 실제 검토한 원본 PTS / 화면 변화 | 구도·화면 내 움직임·재료/자산 | 기능 해석·대안·경계 확신 |
|---|---|---|---|
| C01 ~2.125→2.250→2.375 | 햇빛 든 도심 skatepark의 흰 `VANS` 상표에서 콘크리트 bowl/펜스가 보이는 낮은 park 시점으로 바뀐다. | 높은 wide skyline/bowl에서 지면 높이 rail line으로 내려오는 시점 대비; 나무·건물·콘크리트. 카메라/피사체 원인은 미확정. | 사람 등장 전 상표와 장소를 설정할 수 있다. 대안은 단순 logo hold. 화면교체 후보는 강하나 정확 컷은 모름. |
| C02 ~3.458→3.583→3.708 | 빈 bowl 접근 장면에서 손이 검정 skate shoe 끈을 조인다/묶는다. 흰 swoosh처럼 보이는 양말과 작은 빨간 Vans label이 보인다. | 끈·손 close-up이 화면을 채우고 따뜻한 자연광/얕은 초점. | 제품 사용 전 의식처럼 생활방식과 연결할 수 있다. 대안은 촉감 B-roll. 이미지/설정 변화가 뚜렷하다. |
| C03 ~4.667→4.792→4.917 | 신발 디테일에서 콘크리트 park의 여성 보더 후면으로 바뀐다. 보드를 들고 있고 흐린 배경에서 다른 라이더가 움직인다. | 중간거리 rear 3/4, 보드는 오른쪽 세워 들고 인물은 왼쪽에 둔다; 낮빛/녹색 잎/콘크리트. | 제품에서 착용자/커뮤니티로 초점을 옮긴다. 대안은 일반 청년문화 분위기 montage. |
| C04 ~6.375→6.500→6.625 | park 라이더에서 짙은 satin처럼 보이는 재킷·귀걸이·초록/그래픽 보드를 든 흑인 여성의 초상 close로 교체. | 얼굴은 화면 오른쪽을 향하고, 흐린 낙서 실내 배경과 피부 하이라이트가 대비된다. | 다양한 cast/board 스타일과 반응 초상을 추가한다. persona·관계·상황은 알 수 없다. |
| C05 ~7.292→7.417→7.542 | 초상 뒤 밝은 흰 실내/warehouse형 curved ramp에서 보드를 든 보더 뒷모습. | 낮은 위치에서 다리·보드, 높은 key의 밝은 곡면 벽과 금속 표면. | 초상 뒤 스케일을 reset하고 다음 공간으로 넘어갈 수 있다. 같은 실제 장소/경로인지 미정. |
| C06 ~7.917→8.042→8.167 | 밝은 enclosure에서 지붕 있는 graffiti corridor를 따라 출구의 역광으로 미끄러지는 실루엣 보더. | 중앙 소실점이 깊은 low wide; 내부 암부와 밝은 끝, 화면 안 인물은 멀어진다. | 어둠→빛 통과가 공간 reveal을 만든다. camera track과 subject 이동은 stills로 계측할 수 없다. |
| C07 ~8.417→8.542→8.667 | 지붕 corridor에서 야외 bowl/큰 벽화로 바뀌며 보더가 몸을 낮춰 보드에 다가간다. | 높은 wide bowl, 왼쪽을 차지한 화려한 mural; 작은 인물/보드가 크기 기준을 준다. | street-art/활동 공간을 설정한다. 한 경로의 연속일 수도, 서로 다른 trick 사이 jump일 수도 있다. |
| C08 ~9.000→9.125→9.250 | mural/rider wide에서 지면 가까운 wheel/deck 극근접으로 바뀐다. | 데크 아래·트럭·바퀴가 햇빛 든 콘크리트 위에서 크게 보이고 초점이 얕다. | 인물에서 장비의 촉감·속도 세부로 시선을 좁힌다. |
| C09 ~9.542→9.667→9.792 | 보드/바퀴 close에서 보드 밑으로 이동하는 지면 시점; 포장면과 건축물이 옆으로 흐른다. | 낮고 중앙축에 맞춘 구도에서 바퀴가 화면을 둘러싸고 도로 질감이 streak된다. | 보드가 이동 POV/운동 bridge가 될 수 있다. 보드 장착 카메라와 별도 tracking rig 중 어느 것인지 결정 못 한다. |
| C10 ~10.250→10.375→10.500 | 보드 밑 시점에서 낙서/벽돌 골목의 역광 여성 보더로, 길을 따라 멀어진다. 1초 표본에서도 피사체가 뒤로 작아진다. | 긴 그림자·건물 수렴선의 low wide; 화면상 인물이 후퇴/전진하는 듯 보이나 카메라 원인 모름. | 장비 디테일에서 사람의 이동으로 돌아온다. 구도 교체는 지지되나 카메라/피사체 속도는 미측정. |
| C11 ~12.833→12.958→13.083 | 여성 라이더에서 mural 옆에 웅크려 균형을 잡는 노랑 재킷 남성 보더로 바뀐다. | medium side profile; 벽화가 옆으로 smear되고 인물도 따라 움직인다. pan/tracking/background streak/composite는 구분 불가. | 새 옷/라이더로 trick 전 단계를 열어준다. 정확한 take·인물관계는 미확인. |
| C12 ~13.375→13.500→13.625 | 노랑 재킷 보더 뒤 어두운 frame 안의 좁은 letterbox형 이미지: 차량 뒤에서 두 라이더의 신발이 보드 위에 서 있다. | 크롭 안에는 다리/데크/바퀴만 보이고 뒤 차량들이 지나간다. | 발-보드 접촉을 짝으로 보여준다. 별도 insert인지 작은 화면의 superimposition인지 불확실하다. |
| C13 ~13.958→14.083→14.208 | 보드 위 발 인서트에서 노랑 재킷 보더로 복귀; 몸을 돌리거나 한발 내딛는다. | 그래피티 벽을 옆으로 지나가는 중경, 인물은 오른쪽에 치우침. | 물체 인서트 뒤 인물/트릭 축을 복구할 수 있다. 대안: 다른 take에서 직접 이어붙인 편집. |
| C14 ~14.500→14.625→14.750 | 노랑 재킷 장면에서 밝은 공장형 골목을 따라 보드로 멀어지는 라이더. | 후면 wide, 밝은 하늘, 도로 경계선; 보드는 화면 안쪽으로 진행. | 움직임을 풀어 주는 단계일 수 있다. 실제 속도나 카메라 이동은 미측정. |
| C15 ~15.750→15.875→15.995 | 후면 라이더에서 얕은 웅덩이에 거꾸로 비친 스케이터로 교체. | 프레임 위쪽에 실제 도로 edge, 나머지는 뒤집힌 반사와 젖은 asphalt. | 방향을 잠시 무너뜨리는 reflection insert/shape rhyme일 수 있다. 대안: 별도 양식적 장면이지 실제 낙하 아님. |
| C16 ~16.542→16.667→16.792 | 웅덩이 반사에서 거의 검정. 보충 raw sequence는 R016/PTS16.500 검정→R017/16.708333 잠깐 반사 복귀→R018/16.791667 검정이다. | 0.125초 반사가 어두운 화면에 번쩍 끼어든다; 세 R은 한 짧은 transition/action event이지 자동으로 3컷/scene이 아니다. | 의도된 blink/잔상, 노출·검출 민감도, 생성/합성 flicker가 대안. 순간 화면상태를 temporal QA에 남기되 원인 미확정. |
| C17 ~17.042→17.167→17.287 | 어둠에서 기둥/유리 너머 따뜻한 가게 전면과 옆모습 스케이터. | 수직 foreground frame, 유리/가게 빛과 거리 반사가 겹침. | 창/가림이 도시의 관찰자 시점을 만들 수 있다. 대안: 우연히 겹친 실내/거리 이미지. |
| C18 ~17.625→17.750→17.875 | 가게 전면에서 concrete bowl 안 보드 trick/착지처럼 보이는 동작. | bowl edge의 medium-wide, 콘크리트와 빠른 움직임 blur. | 어두운 가게 비트 뒤 운동감으로 복귀할 수 있다. 대안은 독립 주행 장면; 정확한 trick/착지는 단정하지 않는다. |
| C19 ~18.667→18.792→18.917 | bowl에서 현대식 유리 건물 계단을 오르거나 타는 silhouette로 교체. | 수직 건물 격자와 밝은 하늘 앞의 어두운 옆모습. | 거리 지형을 bowl 밖으로 확장할 수 있다. 안전/허용된 위치인지는 입증되지 않는다. |
| C20 ~19.125→19.250→19.375 | 계단 뒤 흰 셔츠/헬멧의 앉은 남성이 보드 다루고 들어 올린다. | 역광 medium, 얼굴·보드가 낮은 프레임, 밝은 하늘. | trick 사이 준비/휴식의 짧은 인간 beat일 수 있다. 대안: 독립 gear insert. |
| C21 ~19.833→19.958→20.083 | 앉은 인물에서 검정 옷·붉은 신발의 웅크린 보더가 그래피티 옆을 주행; 인접 frame에서 구성 지속. | 낮은 측면 frame, 벽 배경의 수평 smear; 화면상 라이더 이동 보임, tracking/pan/편집 원인은 미확정. | 낮은 자세가 control/skill을 연상시킬 수 있다. detector peak마다 컷이라고 세지 않고 연속 shot 가능성을 보존. |
| C22 ~20.500→20.625→20.750 | 라이더 동작 속 vertical board가 들리고 공중에 뜨며 지면 그림자와 분리. | 낮은 close, board rotation과 발/보드 사이 간격이 바뀜. | 동작의 이륙/정점 action-phase일 수 있고 편집 컷일 필요 없다. trick 명칭·접촉 물리는 frame sample만으로 추정하지 않는다. |
| C23 ~20.958→21.083→21.208 | 공중 보드 close에서 옅은 콘크리트 위를 가로지르는 보더의 비스듬한 overhead view로 전환; 긴 그림자가 보인다. | 높은 각도/강한 햇빛, 넓은 빈 바닥 대비 작은 인물; 이후 보드/발 detail로 좁아진다. | scale contrast로 장소 크기를 읽히게 할 수 있다. camera path나 정확한 이동은 미확정. |
| C24 ~22.167→22.292→22.417 | 넓은 skate view에서 보드를 든 인물이 바깥 계단을 내려오는 정면 low shot. | 대칭 계단의 소실점, 중앙 다리, 어두운 젖은 바닥과 역광. | trick 동작 뒤 잠시 보행/신발 detail로 호흡을 바꿀 수 있다. 대안: 독립 계단 insert. |
| C25 ~22.583→22.708→22.833 | 계단의 신발/보드 detail이 검은 테두리 안 monitor-like inset으로 보인다. | 화면 안의 화면 crop, 흰 끈/신발이 크게 차지한다. | 행동을 작은 memory/screen frame처럼 재구성할 수 있다. 대안: 우발 crop/composite이며 full-screen shot으로 오해하지 않게 처리. |
| C26 ~23.083→23.208→23.333 | close 계단에서 수염 있는 승객/작은 개/보드가 보이는 어두운 지하철 interior. | 창/rail geometry와 얕은 초점, 차가운 fluorescent 색. | 도시 이동/통근 texture를 삽입할 수 있다. 인물·개·라이더의 관계는 미확인. |
| C27 ~23.792→23.917→24.037 | 열차 안/유리 반사에서 보드를 든 앉은 승객이 door/window 너머로 보임. | 안팎 반사와 유리층, 프레임 안 피사체. | 이전 보드 cue를 transit 공간에 반복해 motif를 잇는다. 대안: 같은 공간 연속/카메라 이동은 입증되지 않음. |
| C28 ~26.250→26.375→26.495 | 어두운 transit image에서 넓은 햇빛 든 bowl/벽화와 작은 단독 스케이터. | 매우 넓은/휘어진 가장자리 인상, 큰 벽·bowl과 작은 figure의 규모 대비. | 새 skate terrain을 크게 소개할 수 있다. 곡면 왜곡만으로 fisheye lens를 확정하지 않는다. |
| C29 ~27.125→27.250→27.375 | bowl view에서 원형 top-down/중앙에 작은 skater; 주변 검정 vignette. | 높은 각도의 원형 구성, 가운데 인물. | 원형 graphic eye-shape를 만들 수 있다. 실제 portal/드론 시점을 주장하지 않는다. |
| C30 ~27.984→28.083→28.224 | 원형 bowl에서 흑백 발/데크와 그래피티, 수평 split/echo가 보이는 frame으로 교체. | 강한 명암과 가로 strip들, 발/데크의 측방 movement. | movement/rhythm을 시각적으로 나눌 수 있다. 대안은 editing collage/multi-exposure; 제작방식은 미확인. |
| C31 ~28.417→28.542→28.667 | split monochrome image가 blur/fade하고 보드/다리 close에 연결; 뒤에 컬러 street image. | 흐림/가로줄 효과가 자연 공간 continuity를 끊는다. | 그래픽 bridge/afterimage일 수 있다. 대안은 transition glitch; 중간 blur를 독립 story scene으로 분류하지 않는다. |
| C32 ~30.083→30.208→30.333 | 흑백 board close에서 그래피티 앞 흑셔츠 라이더의 컬러 동작, 이어 흰 셔츠 인물/보드. | 후면 medium, 인물 주위 수평 움직임; 카메라 종류는 미확정. | 흑백 interruption 후 street/cast motif를 회수할 수 있다. 인물 identity/take 연속성은 알 수 없다. |
| C33 ~31.000→31.125→31.245 | 스케이트 장면에서 어두운 큰 헤드폰을 낀 젊은 남성 얼굴 close, 눈을 감은 모습. | 얼굴이 중앙을 채우고 차가운 확산광/어두운 배경. | 몰입/청취 장면으로 보일 수 있지만 헤드폰만 관찰됐고 소리는 듣지 않았다. 실제 음악 경험/브랜드 ethos 증거 아님. |
| C34 ~32.750→32.875→32.995 | 헤드폰 초상에서 햇빛 든 bowl의 웅크린 스케이터로 복귀. | 몸통/보드 low crop, 강한 햇빛과 긴 그림자. | inward portrait 뒤 실제 동작으로 돌아가 대비를 줄 수 있다. sound→ride 연결은 해석뿐. |
| C35 ~34.583→34.667→34.807 | 라이딩에서 다리 아래 공중 회전하는 보드, 이어 발이 데크 착지 위치로 다가옴. | 밝은 하늘/그림자 위 보드 실루엣. | 준비→공중→착지 시퀀스의 action phases일 수 있고 각 프레임이 컷은 아니다. sample rate로 실제 slow motion 여부 판단 불가. |
| C36 ~35.667→35.792→35.912 | 스케이터가 콘크리트에 앉거나 넘어진 듯 보이고 upright board; 이어 햇빛에 비친 shoe/wheel macro. | 지면 높이의 인물에서 강한 flare·휠/트럭 close로 scale을 좁힘. | 불완전한 동작/휴식 뒤 장비 detail을 보일 수 있다. 부상/실패/연출 의도는 미확정. |
| C37 ~37.667→37.792→37.912 | shoe/truck close에서 친구들이 중앙 라이더를 둘러싸고 손을 든 group. | foreground shoe에서 사람·팔이 모인 bowl medium. | 개인 trick 뒤 사회적 reaction payoff를 만들 수 있다. 동기/성공 원인은 해석이며 관계·동일 cast 확정 아님. |
| C38 ~39.167→39.292→39.412 | 환호 그룹에서 웃는 남성 스케이터 초상. | 사람들 사이의 medium portrait, backlight/얕은 초점. | 군중 반응을 한 얼굴의 가시적 reaction으로 좁힌다. 감정·이름을 추정하지 않는다. |
| C39 ~40.792→40.917→41.037 | group reaction에서 보라 후드 남성 주변, 왼쪽 붉은 머리 여성의 웃음. | 친구들 모임 medium, 일광과 비교적 안정된 배경. | 커뮤니티 cue를 확대할 수 있다. 동일한 이전 cast인지 관계인지 불명. |
| C40 ~41.583→41.708→41.833 | 표정 그룹에서 board underside/wheel macro, 발이 데크에 놓임. | wheel/truck 중앙의 낮은 equipment close, 콘크리트 위 강한 태양 그림자. | 인물 reaction 뒤 제품 접촉 세부로 돌아가 footwear/board identity를 회수할 수 있다. 정지 이미지에서 바퀴 회전방향을 결론내리지 않는다. |
| C41 ~42.583→42.708→42.828 | 보드 detail에서 붉은 머리 여성 보더가 그래피티 벽 옆 낮게 웅크린 동작. | 옆면 medium, 청록/노랑/초록 graffiti와 붉은 머리 대비; 신체에 motion blur. | cast/action variation을 제공할 수 있다. persona·성별·성격은 외모로 단정하지 않는다. |
| C42 ~44.547→44.667→44.787 | 여성 라이더에서 차 side mirror에 비친 스케이트 트릭. | 거울 타원이 프레임을 크게 차지하고 건물/주차 차량과 반사 안 인물이 겹침. | screen-within-screen으로 형태 놀라움/관찰 시점을 추가할 수 있다. 대안은 현장 거울의 우연한 frame; camera는 미확정. |
| C43 ~45.755→45.875→45.995 | mirror view에서 콘크리트 위 바퀴/데크 low view와 큰 그림자. | 좌우 대칭에 가까운 wheel close; 프레임 사이 사람/보드 위치가 변화한다. | mirror trick에서 직접 기어 view로 shape/행동을 잇는 선택일 수 있다. 회전방향/카메라 tracking은 단일 frame으로 확정하지 않는다. |
| C44 ~46.755→46.875→46.995 | 바퀴에서 데크 위 검정 Vans-like 신발 hero close: 흰 sidewall/끈, 붉은 patch. | 신발이 화면 대부분을 차지하고 배경은 부드럽다. | 최종 copy 전에 승인 제품 cue를 재확인할 수 있다. 모델명/공식성은 확인되지 않음. |
| C45 ~48.047→48.167→48.287 | 보드 위 신발에서 발이 내딛거나 굴러가는 low close로; 흰 script `Off the Wall`이 위에 들어옴. native terminal n=1292/PTS53.833333까지 문구가 남는다 (`evidence/V003/native-terminal.jpg`). | 낮은 발높이, 흐린 콘크리트/도시, 흰 script가 아래 중앙; 신발 뒤축 mark 일부 보임. | 행동 위 문구를 얹어 title card보다 shoe motion에 campaign line을 붙일 수 있다. 대안은 별도 endcard. 작은 화면에서 글자와 발/신발 모두 읽히는지 검수. |

## 세부 화면 관찰과 연출 메커니즘
- **관찰 구조:** 조용한 도시/스케이트파크 원경의 `VANS` opener 뒤 신발끈 묶기를 보여주고, 다양한 라이더 몽타주를 이어간다. 바퀴/트럭/데크 detail, POV·데크 아래 시점, 계단·물웅덩이·차량 미러 반사, 프레임 안 프레임, 짧은 흑백/슬릿 효과가 넓은 파크 행동을 끊어준다. 끝은 신발로 돌아와 `Off the Wall`을 움직이는 발 위에 얹는다. 후보 시각/프레임 locator가 순서를 뒷받침하며 1초 표본은 0–53초 전체 범위를 가리키지만 연속 재생은 아니다.
- **화면 이동과 카메라 원인 분리:** 사람/보드가 지면을 따라 이동하고 라이더가 웅크렸다 데크를 들며 보드가 공중 프레임에서 회전하고, 바퀴/트럭이 렌즈 가까이 온다. 일부 벽/배경은 수평으로 smear된다. 기록은 화면 공간 변화에 한정한다. 가능한 원인은 스케이터 움직임, dolly/tracking/handheld, 보드 장착 카메라, optical flow, shutter blur, AI/composite warping 등이며 어느 것이 원인인지 프레임만으로 판별 못한다.
- **렌즈/구도 어휘:** 도시 와이드 establishing, 끈/라벨/신발 macro, 인물·보드 후면 미디엄, 데크/바퀴의 극저각, overhead circle, 차량 미러 반사, 물웅덩이 반사, split/letterbox/monochrome interruption. 볼의 곡면 왜곡은 보이나 실제 렌즈 종류는 알 수 없다.
- **색/재료:** 차가운 slate concrete/청록 그늘과 graffiti, 검정 천/캔버스, 흰 끈/sidewall, 간헐적 노란 재킷/붉은 머리, 후반의 따뜻한 햇빛. 고무, 캔버스/천, 콘크리트, 금속 truck/wheel, 유리/거울, 젖은 포장면이 보이는 표면 재료다. 야외 구간에 길고 단단한 그림자가 반복된다.
- **글자/로고:** 시작 도시 overlay의 흰 `VANS`; 신발 표식과 붉은 heel patch; 마지막 신발 sequence에서 들어오는 손글씨 `Off the Wall`은 실제 terminal frame에도 보인다. 검토된 마지막 프레임에는 별도 법적 endcard/URL이 없다. 이 영상에서 `AInspire`는 확인되지 않았다. 전체 copy/transcript는 검증되지 않았다.
- **오디오 단서:** ASR이 “you, your board”, 거리/rhythm/wheels, friends/family, “not just a brand”, 끝의 “Vans Off the Wall” 같은 영어를 제안한다. 환각이나 합성된 가사형 발화일 수 있다. 청취되지 않았으므로 정확한 대사/VO/soundtrack이라고 인용하지 않는다. 음악 장르나 mix를 주장하지 않는다.

## 연출 해석·대안·확신도
- **높은 확신도의 화면 기술:** 도시/스케이트파크 위 VANS opener, 신발끈 묶기, 다양한 보더·보드 장면, 단체 반응, 신발 hero, 움직이는 발 위 마지막 문구의 순서가 보인다. 끝 글자는 빈 법률 카드가 아니라 행동 화면 안에 통합된다.
- **중간 확신도 해석:** 라이더보다 먼저 끈 묶기 detail을 두면 신체적 제품 접점을 만든다. 반복되는 신발/바퀴/데크 close-up은 스타일이 다른 보더 사이에서도 제품을 알아보게 할 수 있다. 대안은 단순한 편집 리듬이며 구매 설득이라고 입증되진 않았다.
- **중간 확신도 해석:** 트릭의 운동 단계와 웃음/환호 reaction을 교대하면 동작을 집단적 payoff로 바꿀 수 있다. 대안은 친구들이 단지 스케이트파크 배경을 구성한다는 것이다. 성과/행동 자료 없음.
- **중간 확신도 해석:** 거울·물웅덩이·원형 bowl·split-screen이 straight trick coverage 밖의 시각적 놀라움을 만든다. 대안은 생성 영상 artifact repair나 제작자의 편집 선택일 수 있으며 source generation method는 확인되지 않았다.
- **낮은 확신도:** 헤드폰 착용자가 음악/도시 rhythm과 스케이트 동작을 이을 수 있다. 청취한 소리는 없어 시각만으로 soundtrack 역할을 정할 수 없다.

## 재사용할 수 있는 기법 (새 자산, 보호 표현 복제 없이)
`DESIGN_PROPOSAL`: 장소를 설정하고 의미 있는 준비 동작을 읽을 수 있는 크기로 보여준 뒤, 퍼포머/기어/액션을 두 개 이상의 구도에서 교차한다. 동작의 정점 뒤 반응을 payoff로 두고 한 가지 명확한 제품표식과 문구로 돌아온다. 저각 바퀴·overhead terrain·반사 프레임은 방향성을 잃지 않을 때만 사용한다. cast·board·shoe·장소·그래피티·색·logo·문구는 새로 만들거나 사용권 있는 자산으로 대체하며 프레임·브랜드 identity·특정 cast·문구를 복제하지 않는다. 물리 fidelity가 중요한 스케이트 동작은 목적과 안전에 맞춰 통제된 실촬영, 실루엣 애니메이션, tabletop insert 또는 단순 그래픽 중 선택한다.

## 관찰 가능한 QA와 미확인 범위
1. 원본 PTS로 45개 grouped candidate의 앞/중앙/뒤 표본을 대조한다. bracket은 cut frame 확정이 아니다. C16 짧은 black/blink, C25/30/31 frame inset/split/blur, C35/36 trick/fall, C45 움직이는 문구를 특별히 유지한다.
2. 새 스케이트 sequence에서는 준비·접지/이륙·공중·착지·반응 단계에 보드 자세/발·trucks/wheels/그림자·반사 일관성을 검사한다. 단일 still에서 바퀴의 회전방향을 판정하지 않는다.
3. 마감 문구는 신발/발을 모두 읽을 수 있도록 진입·유지·퇴장 구간과 safe area를 확인하고, 실제 terminal frame 및 필요한 고지를 별도 검수한다.
4. continuous playback, 음악/SFX/VO 청취, ASR human verification, claims review, metric camera solve, source authorization은 수행하지 않았다. Full decode는 playback이 아니다.
