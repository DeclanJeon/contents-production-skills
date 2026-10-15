# V045 — Zara AI Spec Ad.mp4

[영상 색인으로 돌아가기](../video-index.md)

## 근거와 관찰 모드

archive_id `sha256:06d7c4dd6452e65e2576d1655256f3ea4b8ae69c539adab901806818318e8da1` / 43.125000s. [native PTS ledger](../evidence/fast-V045/extraction-manifest.json). fps 필터 없이 원본 ffprobe 의 frame n/PTS 를 사용했다. 전체 .5s nearest-after + scene>.30 후보 ±2 native frame + 후보 간 midpoint + first/last. 5개 strip 의 193개 frame 실제 판독. FRAMES_REVIEWED 이며 연속 재생/청취 아님. 후보 20개는 컷 수가 아니다. 아래 B 는 관찰 블록: scene/shot/phase 가 섞이므로 verified shot count 로 합산하지 않는다. 구간 경계는 인접 표본 사이 근사, source cut PTS 인증 아님. 표본 사이 미검출 짧은 컷 가능.

## 블록별 관찰과 기능

|블록 / 근사 s|실제 화면 관찰|WHY [INFERENCE], 대안·실패·이전|native frame locator|
|---|---|---|---|
|B01 0.000–3.583|청록색 하늘과 모래 사막, 빈 의자 위 분홍색 구름, 작은 자막|비어 있는 자리와 비현실적인 색으로 세계에 대한 기대 형성. 빈 의자의 인물상은 확정되지 않음|[n0 PTS0.000000 cell1](../evidence/fast-V045/strip-01.jpg) → [n86 PTS3.583333 cell11](../evidence/fast-V045/strip-01.jpg)|
|B02 3.583–5.042|사구에서 오토바이를 탄 인물이 측면으로 이동, 뒤로 먼지가 일어남|정지한 의자에서 이동 행동으로 전환. 바퀴와 지면의 접지 검사|[n86 PTS3.583333 cell11](../evidence/fast-V045/strip-01.jpg) → [n121 PTS5.041667 cell19](../evidence/fast-V045/strip-01.jpg)|
|B03 5.042–6.875|금발 인물이 팔을 벌림. 흰 셔츠와 검정 바지, 바람에 움직이는 옷|목표 행동을 자세로 읽기. '자유'는 연출 가설|[n121 PTS5.041667 cell19](../evidence/fast-V045/strip-01.jpg) → [n165 PTS6.875000 cell27](../evidence/fast-V045/strip-01.jpg)|
|B04 6.875–8.458|단발머리에 검정 상의를 입은 인물의 손 위에서 분홍색 구름이 커져 얼굴을 가림|손과 구름의 접촉 비유, 부분 가림과 얼굴의 동일성|[n165 PTS6.875000 cell27](../evidence/fast-V045/strip-01.jpg) → [n203 PTS8.458333 cell36](../evidence/fast-V045/strip-01.jpg)|
|B05 8.458–9.208|베이지색 소매의 ZARA 소맷단과 손을 가까이 보여 줌. 작은 황금빛|세계보다 상품의 세부로 회수. 소맷단 문자는 실제 관찰|[n203 PTS8.458333 cell36](../evidence/fast-V045/strip-01.jpg) → [n221 PTS9.208333 cell43](../evidence/fast-V045/strip-01.jpg)|
|B06 9.208–12.000|금발 머리와 옆얼굴이 뒤로 젖혀짐. 머리카락이 바람에 좌우로 움직임|옷과 머리카락의 움직임, 얼굴 자세. 실제 원인이 바람인지 렌즈인지는 불명|[n221 PTS9.208333 cell43](../evidence/fast-V045/strip-01.jpg) → [n288 PTS12.000000 cell4](../evidence/fast-V045/strip-02.jpg)|
|B07 12.000–14.083|해안 절벽 옆 공중에 떠 있는 인물, 바다와 일몰|사막에서 물의 세계로 도약하는 연상. 착지나 장소의 연속성을 뒷받침하는 증거 없음|[n288 PTS12.000000 cell4](../evidence/fast-V045/strip-02.jpg) → [n338 PTS14.083333 cell10](../evidence/fast-V045/strip-02.jpg)|
|B08 14.083–14.917|모래 위 작은 분홍색 나무|구름의 색을 뿌리내린 요소로 변환. 실제 식생은 아님|[n338 PTS14.083333 cell10](../evidence/fast-V045/strip-02.jpg) → [n358 PTS14.916667 cell16](../evidence/fast-V045/strip-02.jpg)|
|B09 14.917–16.708|베이지색 바지를 입고 맨발로 걷는 하반신, 모래 위 그림자|패션의 접촉과 무게감 읽기. 발자국 형성 단계의 표본은 제한적|[n358 PTS14.916667 cell16](../evidence/fast-V045/strip-02.jpg) → [n401 PTS16.708333 cell25](../evidence/fast-V045/strip-02.jpg)|
|B10 16.708–19.000|따뜻한 색감의 피부와 눈을 가까이 보여 줌. 눈을 감았다가 뜸, That you/are the journey|외부 여행을 인물 초상과 카피로 회수. 심리 효과는 불명|[n401 PTS16.708333 cell25](../evidence/fast-V045/strip-02.jpg) → [n456 PTS19.000000 cell35](../evidence/fast-V045/strip-02.jpg)|
|B11 19.000–19.750|베이지색 짧은 소매 상의와 바지를 입은 몸통|옷의 핏과 허리 주름 읽기. SKU 동일성의 연속성 검사|[n456 PTS19.000000 cell35](../evidence/fast-V045/strip-02.jpg) → [n474 PTS19.750000 cell42](../evidence/fast-V045/strip-02.jpg)|
|B12 19.750–20.583|사구와 분홍색 나무를 넓게 보여 줌. 작게 보이는 인물|상품 규모 뒤에 세계 규모를 제시, 모티프 고정|[n474 PTS19.750000 cell42](../evidence/fast-V045/strip-02.jpg) → [n494 PTS20.583333 cell1](../evidence/fast-V045/strip-03.jpg)|
|B13 20.583–21.750|금빛 원과 모래 소용돌이를 추상적으로 가까이 보여 줌|색과 입자로 전환. 카메라 회전 또는 질감 합성이 대안|[n494 PTS20.583333 cell1](../evidence/fast-V045/strip-03.jpg) → [n522 PTS21.750000 cell9](../evidence/fast-V045/strip-03.jpg)|
|B14 21.750–24.500|검정 재킷을 입은 금발 인물이 팔을 벌림. 머리카락이 흩날림|초반 자세의 반복과 의상 변화. 같은 인물인지 외형 검사|[n522 PTS21.750000 cell9](../evidence/fast-V045/strip-03.jpg) → [n588 PTS24.500000 cell20](../evidence/fast-V045/strip-03.jpg)|
|B15 24.500–26.167|오토바이 옆 흰 상의를 입은 단발머리 인물이 뒤돌아봄 → 25.5 넓은 화면|행동에서 전체 착장을 안정적으로 유지하는 화면으로 전환. 오토바이는 패션 소품|[n588 PTS24.500000 cell20](../evidence/fast-V045/strip-03.jpg) → [n628 PTS26.166667 cell33](../evidence/fast-V045/strip-03.jpg)|
|B16 26.167–28.917|베이지색 바지를 입고 걷는 몸통과 엉덩이 부분을 가까이 보여 줌|옷감의 주름과 무게감이 드러나는 행동. 다리와 손의 수 오류 검사|[n628 PTS26.166667 cell33](../evidence/fast-V045/strip-03.jpg) → [n694 PTS28.916667 cell44](../evidence/fast-V045/strip-03.jpg)|
|B17 28.917–30.458|작은 초록색 나무 옆 인물의 팔 끝, 손이 나무 쪽으로 접근|분홍색 구름에서 나무로 변주. 손의 접촉과 나무의 크기에서 실패 가능성을 대안으로 검토|[n694 PTS28.916667 cell44](../evidence/fast-V045/strip-03.jpg) → [n731 PTS30.458333 cell4](../evidence/fast-V045/strip-04.jpg)|
|B18 30.458–31.750|검게 광택 나는 얼굴의 정면, 입을 벌림. 얼굴 위 붉은 주황색 입자|피부와 재질의 극단적 대비. 실제 피부나 인종의 변환이라고 주장할 수 없음|[n731 PTS30.458333 cell4](../evidence/fast-V045/strip-04.jpg) → [n762 PTS31.750000 cell12](../evidence/fast-V045/strip-04.jpg)|
|B19 31.750–35.042|모래, 검정 입자, 분홍색 꽃 위에 베이지색 바지를 펼쳐 놓음|인물이 착용한 패션에서 상품 형태를 분리. 꽃과 모래로 세계의 모티프를 묶음|[n762 PTS31.750000 cell12](../evidence/fast-V045/strip-04.jpg) → [n841 PTS35.041667 cell24](../evidence/fast-V045/strip-04.jpg)|
|B20 35.042–39.000|처음의 사막 의자에 인물이 앉음. 큰 ZARA 문자와 이동하는 분홍색 구름|빈자리에서 앉은 상태의 결과로 전환하고 브랜드 읽기. 의자와 의상의 연속성|[n841 PTS35.041667 cell24](../evidence/fast-V045/strip-04.jpg) → [n936 PTS39.000000 cell37](../evidence/fast-V045/strip-04.jpg)|
|B21 39.000–43.125|검정 화면 → 40.5 DIRECTED BY THE DOR BROTHERS → 서서히 사라짐|제작 크레디트 층위. 문자 관찰일 뿐, 제작자나 진위에 대한 인증은 없음|[n936 PTS39.000000 cell37](../evidence/fast-V045/strip-04.jpg) → [n1034 PTS43.083333 cell1](../evidence/fast-V045/strip-05.jpg)|

## 연출과 이전 판단

패션 상품은 셔츠, 바지, 소맷단, 펼쳐 놓은 상품 형태로 보이지만 실제 SKU나 공식 캠페인은 확인하지 않았다. 구름, 나무, 먼지, 머리카락, 피부의 재질 변주가 서사의 여행 카피와 결합한다. 얼굴과 의상의 변화를 캐릭터의 실제 성장으로 단정하지 않는다.

### 재사용 메커니즘·절차의 실마리 [INFERENCE]

세계의 모티프 → 신체 동작 → 옷감의 세부 → 재질 대비 → 펼쳐 놓은 상품 → 브랜드 화면. 04의 연기 / 08의 색 / 19의 의상 SSOT / 25의 지각적 대응 심화. 피부와 재질 변환의 동일성 및 권리 검사.

## 미확인과 반례

WHY는 제작자 의도나 효과의 검증이 아니다. 관찰한 색·형상·배치의 확실성은 높음, 미세 접촉과 작은 문자는 중간~낮음. 렌즈 mm, 원본 촬영 fps, 장비·CG·합성 여부, 심리·효능은 UNKNOWN. 화면 변화가 카메라 이동인지 피사체 회전·크롭·합성인지는 상대적인 배경 변화의 근거가 있을 때만 후보를 구분한다. 파일 제목의 공식·viral·실명·모델 표기는 인증하지 않는다. 오디오 디코딩 및 ASR 결과는 별도 기계 모드이며, 음악 질감·효과음·박자 동기화는 청취 없이 판정하지 않는다.

## 도달 가능한 오디오 증거

전체 AAC 디코딩과 astats/silencedetect 측정 실행 rc0, 캐시된 faster-whisper small 로컬 ASR 1개 기계 가설. [ASR 원문](../evidence/fast-V045/offline-asr.json) · [측정 로그](../evidence/fast-V045/audio-decode-astats-silence.txt) · [런타임/해석 한계](../evidence/repo-worker-audio-evidence.json). 음악·질감·foley·lip sync는 실청취하지 않아 UNKNOWN이다. 단어 가설은 대사·음악·성능 약속의 사실 확인이 아니다.

## 도달 가능한 원본 텍스트 출처

[The Dor Brothers의 원본 URL](https://www.youtube.com/watch?v=a4SbLFW-UzI)을 실제 원문 reader로 확인했다. 결과: `CAPTION_UNAVAILABLE_READER`. [실제 응답](../evidence/provenance-original-V045.txt) · [제작자 주장과 캐시 위치](../creator-provenance.json). 이번 reader에 자막이 없다는 결과만 기록한다. 캐시 설명의 제작·음악 credit가 없는 것으로 확대 해석하지 않는다.
