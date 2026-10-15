# V043 — Travis Scott Video Ads Made with AI for Nike.mp4

[영상 색인으로 돌아가기](../video-index.md)

## 근거와 관찰 모드

archive_id `sha256:428e66d8b88db87fc813ba1d0278185bacc8712702d380c42f1d6e2594a723e3` / 99.750000s. [native PTS ledger](../evidence/fast-V043/extraction-manifest.json). fps 필터 없이 원본 ffprobe 의 frame n/PTS 를 사용했다. 전체 .5s nearest-after + scene>.30 후보 ±2 native frame + 후보 간 midpoint + first/last. 5개 strip 의 213개 frame 실제 판독. FRAMES_REVIEWED 이며 연속 재생/청취 아님. 후보 2개는 컷 수가 아니다. 아래 B 는 관찰 블록: scene/shot/phase 가 섞이므로 verified shot count 로 합산하지 않는다. 구간 경계는 인접 표본 사이 근사, source cut PTS 인증 아님. 표본 사이 미검출 짧은 컷 가능.

## 블록별 관찰과 기능

|블록 / 근사 s|실제 화면 관찰|WHY [INFERENCE], 대안·실패·이전|native frame locator|
|---|---|---|---|
|B01 0.000–1.500|청흑색 안개가 낀 풍경, 작은 사람들의 줄과 먼 차량|줄의 크기로 제품에 대한 기대와 접근 방향을 나타냄. 실제 군중 수는 불명|[n0 PTS0.000000 cell1](../evidence/fast-V043/strip-01.jpg) → [n36 PTS1.500000 cell4](../evidence/fast-V043/strip-01.jpg)|
|B02 1.500–3.500|찢어진 큰 AIR JORDAN 표지, 구멍으로 보이는 풍경|종이/포장의 구멍을 세계를 드러내는 창으로 사용. 찢김 형상의 연속성|[n36 PTS1.500000 cell4](../evidence/fast-V043/strip-01.jpg) → [n84 PTS3.500000 cell8](../evidence/fast-V043/strip-01.jpg)|
|B03 3.500–7.500|공중 시점이 줄 둘레를 이동→6s 거대한 검정 신발이 위에 부유|대기 줄→거대한 제품 크기의 대비. 실제 렌즈/카메라 원인은 미확정|[n84 PTS3.500000 cell8](../evidence/fast-V043/strip-01.jpg) → [n180 PTS7.500000 cell16](../evidence/fast-V043/strip-01.jpg)|
|B04 7.500–8.000|두 팔/손이 밝은 수직 막대를 잡음, 공간이 암전됨|외부 공중 시점→1인칭 신체 기준점. 동일 인물로 연결된다는 가설|[n180 PTS7.500000 cell16](../evidence/fast-V043/strip-01.jpg) → [n192 PTS8.000000 cell17](../evidence/fast-V043/strip-01.jpg)|
|B05 8.000–11.500|작은 밝은 덩어리→9.5 앞쪽의 수많은 종이/물체 더미|점→장애물 전체가 드러남. 그림 형상의 생성인지 이동인지는 불명|[n192 PTS8.000000 cell17](../evidence/fast-V043/strip-01.jpg) → [n276 PTS11.500000 cell25](../evidence/fast-V043/strip-01.jpg)|
|B06 11.500–14.000|앞의 인물들이 더미 사이로 달림, 종이가 주변에서 흐름|주행 경로를 사람의 실루엣으로 읽음. 개별 움직임의 접촉은 미검증|[n276 PTS11.500000 cell25](../evidence/fast-V043/strip-01.jpg) → [n336 PTS14.000000 cell30](../evidence/fast-V043/strip-01.jpg)|
|B07 14.000–15.000|손 앞의 탁자/짙은 색의 방, 벽난로와 상자에 담긴 소품|질주→개인적인 개봉 작업 공간. 따뜻한 색으로 세계 전환|[n336 PTS14.000000 cell30](../evidence/fast-V043/strip-01.jpg) → [n360 PTS15.000000 cell32](../evidence/fast-V043/strip-01.jpg)|
|B08 15.000–17.500|손이 덮개를 열고 물체를 들었다 놓음|개봉의 접촉/들어 올리기 단계. 손/포장 경첩 검사가 필요|[n360 PTS15.000000 cell32](../evidence/fast-V043/strip-01.jpg) → [n420 PTS17.500000 cell37](../evidence/fast-V043/strip-01.jpg)|
|B09 17.500–21.458|검정 신발 형태의 물체를 손에서 돌리고, 19.5 카드 같은 CONGRATULATIONS 표시|포장/신체/인증 문자의 순서. 실제 구매/보상 사실은 아님|[n420 PTS17.500000 cell37](../evidence/fast-V043/strip-01.jpg) → [n515 PTS21.458333 cell47](../evidence/fast-V043/strip-01.jpg)|
|B10 21.458–23.000|1인칭 손의 CONGRATULATIONS 카드, 밝고 차가운 지면과 원형 맨홀|손/소품을 기준점으로 따뜻한 방→야외를 연결. '연속 숏'으로 확정 불가|[n515 PTS21.458333 cell47](../evidence/fast-V043/strip-01.jpg) → [n552 PTS23.000000 cell4](../evidence/fast-V043/strip-02.jpg)|
|B11 23.000–25.500|손/카드가 화면 밖으로 나감, 지면에서 거대한 실내 산업 공간 위로 틸트하듯 변함|소품 관찰→세계의 지리 공개. 카메라 틸트/합성 변환이라는 대안|[n552 PTS23.000000 cell4](../evidence/fast-V043/strip-02.jpg) → [n612 PTS25.500000 cell9](../evidence/fast-V043/strip-02.jpg)|
|B12 25.500–28.500|위 구조의 자루 같은 기계→27.5 원형의 밝은 구멍에 접근|시선 높이/광원 형상이 탑승 이동의 출발 기호. 실제 장비는 불명|[n612 PTS25.500000 cell9](../evidence/fast-V043/strip-02.jpg) → [n684 PTS28.500000 cell15](../evidence/fast-V043/strip-02.jpg)|
|B13 28.500–30.500|적색 등이 있는 터널, 양손의 안전바와 앞쪽 레일|1인칭 시점의 장기 기준점. 상하/좌우 기울기와 속도 체감은 화면 벡터에 관한 가설|[n684 PTS28.500000 cell15](../evidence/fast-V043/strip-02.jpg) → [n732 PTS30.500000 cell19](../evidence/fast-V043/strip-02.jpg)|
|B14 30.500–33.500|옆으로 기울어진 시야→31s 흰 코트/고글을 착용한 인물이 옆 좌석에 있음|빠른 경로 이동 사이에 동반자를 선명한 프레임으로 제시. 인물의 실명은 인증하지 않음|[n732 PTS30.500000 cell19](../evidence/fast-V043/strip-02.jpg) → [n804 PTS33.500000 cell25](../evidence/fast-V043/strip-02.jpg)|
|B15 33.500–37.500|앞쪽 레일로 복귀, 터널의 밝기 변화/적색 등 통과|옆쪽 반응→경로상의 행동으로 복귀. 터널 구조 변형 검사|[n804 PTS33.500000 cell25](../evidence/fast-V043/strip-02.jpg) → [n900 PTS37.500000 cell33](../evidence/fast-V043/strip-02.jpg)|
|B16 37.500–39.000|기계/SHOEBOX와 비슷한 큰 표지 아래를 통과|탑승 이동 환경에 제품 세계의 문자. 작은 문자는 원본 판독이 필요|[n900 PTS37.500000 cell33](../evidence/fast-V043/strip-02.jpg) → [n936 PTS39.000000 cell36](../evidence/fast-V043/strip-02.jpg)|
|B17 39.000–43.000|레일 분기/굴곡과 호박색 통로, 앞쪽 불빛/광원이 확대됨|경로의 곡선으로 방향 변화. 속도 변화 효과/실제 속도는 불명|[n936 PTS39.000000 cell36](../evidence/fast-V043/strip-02.jpg) → [n1032 PTS43.000000 cell44](../evidence/fast-V043/strip-02.jpg)|
|B18 43.000–48.000|좌우의 녹색 기계 창, 45.5 한 기계가 전경을 크게 지나감|가까운/먼 구조물의 상대적인 화면 흐름이 이동 단서. CG임은 단정하지 않음|[n1032 PTS43.000000 cell44](../evidence/fast-V043/strip-02.jpg) → [n1152 PTS48.000000 cell6](../evidence/fast-V043/strip-03.jpg)|
|B19 48.000–55.500|동반자 옆모습의 중간 크기 숏, 50.5 손을 펼침→54.5 신발 형태의 물체를 들고 보여줌|탑승 이동 중 제품 공개를 배우의 행동으로 안정시킴. 신발의 동일성은 지속 검사|[n1152 PTS48.000000 cell6](../evidence/fast-V043/strip-03.jpg) → [n1332 PTS55.500000 cell21](../evidence/fast-V043/strip-03.jpg)|
|B20 55.500–57.500|앞쪽 레일의 CAUTION INTENSE HEAT와 매우 밝은 출입구|경고문이 행동을 예고함. 실제 안전성 소재로 이전 금지|[n1332 PTS55.500000 cell21](../evidence/fast-V043/strip-03.jpg) → [n1380 PTS57.500000 cell25](../evidence/fast-V043/strip-03.jpg)|
|B21 57.500–61.000|흰색/주황색 섬광, 손을 위로 올림→58.5 차가운 동굴의 레일|열기→차가움의 전환과 신체 반응. 섬광이 편집인지 빛인지는 불명|[n1380 PTS57.500000 cell25](../evidence/fast-V043/strip-03.jpg) → [n1464 PTS61.000000 cell33](../evidence/fast-V043/strip-03.jpg)|
|B22 61.000–65.500|동반자가 손을 들고, 뒤쪽 세계에는 거대한 선인장/기계들이 있음|인물의 지시 몸짓을 환경 공개의 동기로 사용. 의미와 심리는 불명|[n1464 PTS61.000000 cell33](../evidence/fast-V043/strip-03.jpg) → [n1572 PTS65.500000 cell42](../evidence/fast-V043/strip-03.jpg)|
|B23 65.500–68.500|동반자가 아래쪽에서 신발을 돌려 보여줌→67s 옆 아래쪽의 선인장 플랫폼과 레일|제품 세부와 세계의 거시적 규모를 왕복. 실제 공장은 아님|[n1572 PTS65.500000 cell42](../evidence/fast-V043/strip-03.jpg) → [n1644 PTS68.500000 cell48](../evidence/fast-V043/strip-03.jpg)|
|B24 68.500–72.500|커다란 검정 선인장 형태의 구조 옆으로/위로 시야가 기울어짐|좌우 기울기/경로 감각과 근거리/원거리 시차 후보. 크롭 합성이라는 대안|[n1644 PTS68.500000 cell48](../evidence/fast-V043/strip-03.jpg) → [n1740 PTS72.500000 cell8](../evidence/fast-V043/strip-04.jpg)|
|B25 72.500–75.500|레일 정면→73 동반자가 손을 뻗음→74 어두운 터널 정면|짧은 반응/행동의 교대. 경계는 .5s 사이의 근사값|[n1740 PTS72.500000 cell8](../evidence/fast-V043/strip-04.jpg) → [n1812 PTS75.500000 cell14](../evidence/fast-V043/strip-04.jpg)|
|B26 75.500–78.500|붉은 수평 광선/표지 통과→76.5 동반자가 몸을 뒤로 젖힘|빠른 이동과 대비되는 앉은 신체의 기준점. 접촉 없는 배경 흐름|[n1812 PTS75.500000 cell14](../evidence/fast-V043/strip-04.jpg) → [n1884 PTS78.500000 cell20](../evidence/fast-V043/strip-04.jpg)|
|B27 78.500–82.500|동반자 옆에서 앞쪽 레일로 복귀, 광원/표지가 길게 늘어짐|경로 방향을 다시 확보. 광학적 흐름/느린 속도의 직접 증거는 없음|[n1884 PTS78.500000 cell20](../evidence/fast-V043/strip-04.jpg) → [n1980 PTS82.500000 cell28](../evidence/fast-V043/strip-04.jpg)|
|B28 82.500–85.500|밝고 좁은 레일→83.5 어두움→84 불꽃과 새 방|출입구 통과의 가림/섬광 전환. 짧은 하드 컷이 누락되었을 가능성|[n1980 PTS82.500000 cell28](../evidence/fast-V043/strip-04.jpg) → [n2052 PTS85.500000 cell34](../evidence/fast-V043/strip-04.jpg)|
|B29 85.500–88.000|거대한 작업장 안, 앞 좌석의 붉은 머리 받침대, 레일과 금빛 전광|이동→목적지 공개. 실제 공간 지리는 없음|[n2052 PTS85.500000 cell34](../evidence/fast-V043/strip-04.jpg) → [n2112 PTS88.000000 cell39](../evidence/fast-V043/strip-04.jpg)|
|B30 88.000–91.500|새로운 앞/옆 좌석 인물이 보임→90s 흰 코트 동반자의 옆얼굴|동반자의 동일성/좌석 수 변화 가능. 여러 배우/연속성 오류라는 대안|[n2112 PTS88.000000 cell39](../evidence/fast-V043/strip-04.jpg) → [n2196 PTS91.500000 cell46](../evidence/fast-V043/strip-04.jpg)|
|B31 91.500–93.500|카메라 같은 시야가 앞쪽으로 흐려지며 회전→92s 정면에 앉은 인물|대화/반응 방향을 재설정. 180축은 가상 탑승 이동 기준으로 따로 정의|[n2196 PTS91.500000 cell46](../evidence/fast-V043/strip-04.jpg) → [n2244 PTS93.500000 cell2](../evidence/fast-V043/strip-05.jpg)|
|B32 93.500–97.625|정면 인물이 팔을 올림, 앞쪽 팔이 손을 뻗음→96 둘 다 앉음|몸짓의 접근/접촉/결과 후보. 접촉 순간의 전체 프레임을 검증한 것은 아님|[n2244 PTS93.500000 cell2](../evidence/fast-V043/strip-05.jpg) → [n2343 PTS97.625000 cell13](../evidence/fast-V043/strip-05.jpg)|
|B33 97.625–99.750|검정/붉은 Jumpman 형태의 표식→99 어두운 잔상|긴 세계 속 탑승 이동 뒤 단일 브랜드 표식을 유지. 신발 구매 유도 문구는 없음|[n2343 PTS97.625000 cell13](../evidence/fast-V043/strip-05.jpg) → [n2393 PTS99.708333 cell21](../evidence/fast-V043/strip-05.jpg)|

## 연출과 이전 판단

후보 2개만으로는 대부분의 세계/배우/소품 전환을 잡지 못한다. 전체 213개 원본 표본에서 다수의 단계/숨은 경계 후보를 수동으로 기록했다. 0–7초는 외부의 거대한 신발/대기 줄, 7.5–23초는 개봉/소품의 1인칭 시점, 23–97.6초는 탑승 이동과 동반자, 97.6초 이후는 표식으로 상위 장면을 대응시킨다. 각 B를 독립 컷으로 합산하지 않는다.

### 재사용 작동 원리·구성 절차의 단서 [INFERENCE]

1인칭 시점의 신체 기준점→경로 예측→가림/섬광→세계 공개→동반자 반응→제품으로 복귀. 06/20/25에서 경로의 연결 구조와 전경 가림/소품 동일성/숨은 컷의 증거 범위를 심화. 신발/인물의 브랜드 권리와 실명은 출처 확인이 필요.

## 미확인과 반례

WHY는 제작자 의도/효과 검증이 아니다. 관찰한 색·형상·배치=높음, 미세 접촉/작은 문자=중낮음. 렌즈 mm, 원본 촬영 fps, 장비/CG/합성 여부, 심리/효능=UNKNOWN. 화면 변화가 카메라 이동인지 피사체 회전/크롭/합성인지는 상대적인 배경 변화의 근거가 있을 때만 후보를 구분한다. 파일 제목의 공식/바이럴/실명/모델은 인증하지 않는다. 오디오 디코딩/자동 음성 인식 결과는 별도 기계 모드이며, 음악 질감/효과음/박자 동기화는 청취 없이 판정하지 않는다.

## 도달 가능한 오디오 증거

전체 AAC 디코딩과 astats/silencedetect 측정 실행 rc0, 캐시된 faster-whisper small 로컬 ASR 6개 기계 가설. [ASR 원문](../evidence/fast-V043/offline-asr.json) · [측정 로그](../evidence/fast-V043/audio-decode-astats-silence.txt) · [런타임/해석 한계](../evidence/repo-worker-audio-evidence.json). 음악·질감·foley·lip sync는 실청취하지 않아 UNKNOWN이다. 단어 가설은 대사·음악·성능 약속의 사실 확인이 아니다.

## 도달 가능한 원본 텍스트 출처

[Mejor llama a Javier의 원본 URL](https://www.youtube.com/watch?v=xLnrdf_SKdA)을 실제 원문 reader로 확인했다. 결과: `CAPTION_TEXT_AUTO_UNTIMED`. [실제 응답](../evidence/provenance-original-V043.txt) · [제작자 주장과 캐시 위치](../creator-provenance.json). 자동 자막 원문은 시간 정보가 없으며 ASR와 마찬가지로 실청취·음악 식별·VO onset·동의·성능 입증이 아니다.
