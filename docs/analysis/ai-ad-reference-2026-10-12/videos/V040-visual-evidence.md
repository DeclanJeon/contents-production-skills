# V040 — The Future ｜ Tesla Cybertruck ｜ AI Spec Ad.mp4

[영상 색인으로 돌아가기](../video-index.md)

## 근거와 관찰 모드

archive_id `sha256:ab437ae5fad0bc413cfe16dc9fbd5d9428094f12228f7a654280b1285bb555d5` / 46.796750s. [native PTS ledger](../evidence/fast-V040/extraction-manifest.json). fps 필터 없이 원본 ffprobe 의 frame n/PTS 를 사용했다. 전체 .5s nearest-after + scene>.30 후보 ±2 native frame + 후보 간 midpoint + first/last. 6개 strip 의 261개 frame 실제 판독. FRAMES_REVIEWED 이며 연속 재생/청취 아님. 후보 37개는 컷 수가 아니다. 아래 B 는 관찰 블록: scene/shot/phase 가 섞이므로 verified shot count 로 합산하지 않는다. 구간 경계는 인접 표본 사이 근사, source cut PTS 인증 아님. 표본 사이 미검출 짧은 컷 가능.

## 블록별 관찰과 기능

|블록 / 근사 s|실제 화면 관찰|이유 [INFERENCE], 대안·실패·이전|native frame locator|
|---|---|---|---|
|B01 0.000–1.001|백색 가로 빛과 청흑색 차체, .125 부근 측면 차량→붉은 후미등의 흐림|극단적으로 짧게 제시되는 앞뒤 빛으로 차량의 정체성을 먼저 드러냄. 섬광은 컷과 동의어가 아님|[n0 PTS0.000000 cell1](../evidence/fast-V040/strip-01.jpg) → [n24 PTS1.001000 cell16](../evidence/fast-V040/strip-01.jpg)|
|B02 1.001–4.004|물 표면의 흰 삼각 윤곽 표식, 반사와 작은 파문|단단한 차체 선을 추상 표식으로 압축. 공식 로고 여부는 별도|[n24 PTS1.001000 cell16](../evidence/fast-V040/strip-01.jpg) → [n96 PTS4.004000 cell25](../evidence/fast-V040/strip-01.jpg)|
|B03 4.004–4.671|차륜 둘레의 푸른 전광 호→차체의 흐림|원의 형상과 빛을 전기적 비유로 대응. 충전 기능의 증거가 아님|[n96 PTS4.004000 cell25](../evidence/fast-V040/strip-01.jpg) → [n112 PTS4.671333 cell37](../evidence/fast-V040/strip-01.jpg)|
|B04 4.671–7.466|거대한 어두운 홀, 멀리 있는 정면 차량과 천장의 흰 직사각형. 7.382에서 백광 강화|작은 차량→등 점등으로 드러남. 빛이 차체를 가리는 실패도 점검|[n112 PTS4.671333 cell37](../evidence/fast-V040/strip-01.jpg) → [n179 PTS7.465792 cell47](../evidence/fast-V040/strip-01.jpg)|
|B05 7.466–10.844|전조등과 각진 보닛의 근접 화면, 반사 띠 이동|각진 면의 부피를 선형 반사로 읽음. 카메라와 조명 변화의 원인은 불명|[n179 PTS7.465792 cell47](../evidence/fast-V040/strip-01.jpg) → [n260 PTS10.844167 cell12](../evidence/fast-V040/strip-02.jpg)|
|B06 10.844–11.178|차륜의 푸른 호 재등장|홀의 정지 화면과 에너지 삽입 화면의 대비. 물리적 성능 주장이 아님|[n260 PTS10.844167 cell12](../evidence/fast-V040/strip-02.jpg) → [n268 PTS11.177833 cell20](../evidence/fast-V040/strip-02.jpg)|
|B07 11.178–14.223|붉은 후미등 띠의 사선, 원근 변화|앞의 백색과 뒤의 적색으로 방향 구분. 등 연속성 점검|[n268 PTS11.177833 cell20](../evidence/fast-V040/strip-02.jpg) → [n341 PTS14.222542 cell33](../evidence/fast-V040/strip-02.jpg)|
|B08 14.223–16.808|전면등의 흐림→14.431에서 지붕과 유리를 보는 높은 시점|운동의 맥동 후 지붕 형상 읽기. 속도 측정 불가|[n341 PTS14.222542 cell33](../evidence/fast-V040/strip-02.jpg) → [n403 PTS16.808458 cell48](../evidence/fast-V040/strip-02.jpg)|
|B09 16.808–17.684|홀에서 차량 측면을 담은 넓은 화면. 광원이 어둠→밝음으로 변화|전체 윤곽이 안정됨. 천장 직사각형과 반사의 관계|[n403 PTS16.808458 cell48](../evidence/fast-V040/strip-02.jpg) → [n424 PTS17.684333 cell9](../evidence/fast-V040/strip-03.jpg)|
|B10 17.684–19.811|도어 안쪽의 적색 간접 조명 선, 흑백 패널|실내 재질과 선형 정체성. 실제 조명 사양 미확인|[n424 PTS17.684333 cell9](../evidence/fast-V040/strip-03.jpg) → [n475 PTS19.811458 cell19](../evidence/fast-V040/strip-03.jpg)|
|B11 19.811–21.104|차륜과 타이어의 초근접 화면, 바닥 반사|주행 전 지면 접촉. 차륜 수와 굴림의 정합성 검사|[n475 PTS19.811458 cell19](../evidence/fast-V040/strip-03.jpg) → [n506 PTS21.104417 cell27](../evidence/fast-V040/strip-03.jpg)|
|B12 21.104–22.397|후면 3/4 시점의 붉은 후미등 띠, 홀의 원근|차체 앞뒤를 동일한 세계 안에서 다시 제시|[n506 PTS21.104417 cell27](../evidence/fast-V040/strip-03.jpg) → [n537 PTS22.397375 cell35](../evidence/fast-V040/strip-03.jpg)|
|B13 22.397–23.523|뒷좌석에서 본 화면과 앞유리, 화면의 흰 글자|운전석 공간의 지리적 배치. 작은 글자 판독은 별도|[n537 PTS22.397375 cell35](../evidence/fast-V040/strip-03.jpg) → [n564 PTS23.523500 cell40](../evidence/fast-V040/strip-03.jpg)|
|B14 23.523–24.483|화면의 삼각 그래픽→23.732에서 파편과 백광→와이어프레임 터널의 차량|물리적 실내→추상적인 속도의 세계. 실제 UI 기능이 아님|[n564 PTS23.523500 cell40](../evidence/fast-V040/strip-03.jpg) → [n587 PTS24.482792 cell4](../evidence/fast-V040/strip-04.jpg)|
|B15 24.483–25.359|손과 운전대의 근접 화면|추상 세계의 제어 주체를 다시 제시. 손 위치의 불연속은 반례|[n587 PTS24.482792 cell4](../evidence/fast-V040/strip-04.jpg) → [n608 PTS25.358667 cell11](../evidence/fast-V040/strip-04.jpg)|
|B16 25.359–28.779|와이어프레임 터널→26.026에서 운전자의 옆얼굴→26.526에서 젖은 도로 위 차량의 측면|주관적 그래픽과 도로를 분리. 같은 주행 위치라는 증거 없음|[n608 PTS25.358667 cell11](../evidence/fast-V040/strip-04.jpg) → [n690 PTS28.778750 cell24](../evidence/fast-V040/strip-04.jpg)|
|B17 28.779–29.655|정면에서 본 바위 경사를 오르는 차량, 차체 높낮이 변화|경사와 접지 상태. 실차 등판 성능의 증거가 아님|[n690 PTS28.778750 cell24](../evidence/fast-V040/strip-04.jpg) → [n711 PTS29.654625 cell32](../evidence/fast-V040/strip-04.jpg)|
|B18 29.655–31.365|눈밭의 넓은 화면에서 차량의 횡단과 눈 구름→30.5에서 어두운 패널 통과|지형 전환과 가림을 이용한 와이프 후보. 두 지형의 연결은 미확인|[n711 PTS29.654625 cell32](../evidence/fast-V040/strip-04.jpg) → [n752 PTS31.364667 cell40](../evidence/fast-V040/strip-04.jpg)|
|B19 31.365–32.241|후륜의 근접 화면, 눈과 파편이 뒤로 번짐|차륜과 도로의 충돌 단계. 굴림과 접지 미끄럼 검사|[n752 PTS31.364667 cell40](../evidence/fast-V040/strip-04.jpg) → [n773 PTS32.240542 cell48](../evidence/fast-V040/strip-04.jpg)|
|B20 32.241–32.658|젖은 도로 위 차량을 측면 앞 3/4 시점에서 본 화면|눈의 초근접 화면 후 차체 전체의 방향을 다시 제시|[n773 PTS32.240542 cell48](../evidence/fast-V040/strip-04.jpg) → [n783 PTS32.657625 cell7](../evidence/fast-V040/strip-05.jpg)|
|B21 32.658–32.991|화면 표시: 117→118KPH, 85%|원본 화면의 표시일 뿐 실제 속도 측정이 아님|[n783 PTS32.657625 cell7](../evidence/fast-V040/strip-05.jpg) → [n791 PTS32.991292 cell13](../evidence/fast-V040/strip-05.jpg)|
|B22 32.991–33.951|계곡에서 낮은 전면 시점으로 본 차량의 통과→33.493에서 뒤쪽 먼지와 함께 이탈|접근·통과·이탈 동작을 포괄하는 화면 구성. 주행 방향 연결|[n791 PTS32.991292 cell13](../evidence/fast-V040/strip-05.jpg) → [n814 PTS33.950583 cell20](../evidence/fast-V040/strip-05.jpg)|
|B23 33.951–34.785|높은 후방 추종 시점의 차량과 계곡 도로|주체의 축척과 경로의 지리적 배치. 앞뒤 위치 대응 검사|[n814 PTS33.950583 cell20](../evidence/fast-V040/strip-05.jpg) → [n834 PTS34.784750 cell27](../evidence/fast-V040/strip-05.jpg)|
|B24 34.785–36.536|도로에서 전면 추적 촬영→36.036에서 바위와 전면의 물 튀김→36.119에서 후면의 먼지|여러 지형의 짧은 삽입 화면. 연속 여행보다 성능 몽타주 후보|[n834 PTS34.784750 cell27](../evidence/fast-V040/strip-05.jpg) → [n876 PTS36.536500 cell34](../evidence/fast-V040/strip-05.jpg)|
|B25 36.536–37.454|교량 측면, 전경의 기둥 통과, 원경의 산과 얼음|차량·전경·원경의 상대적 변화. 추적 촬영과 합성이라는 대안|[n876 PTS36.536500 cell34](../evidence/fast-V040/strip-05.jpg) → [n898 PTS37.454083 cell38](../evidence/fast-V040/strip-05.jpg)|
|B26 37.454–38.538|차량을 바로 위에서 내려다본 화면의 원형 먼지 선회|선회의 기하를 넓은 화면으로 읽음. 실차 드리프트의 증거가 아님|[n898 PTS37.454083 cell38](../evidence/fast-V040/strip-05.jpg) → [n924 PTS38.538500 cell42](../evidence/fast-V040/strip-05.jpg)|
|B27 38.538–39.957|뒤쪽의 붉은 후미등과 먼지, 먼지가 엷어져 차체가 읽힘|충돌로 생긴 먼지 구름→가라앉으며 드러남. 먼지가 정체성을 지우는 실패|[n924 PTS38.538500 cell42](../evidence/fast-V040/strip-05.jpg) → [n958 PTS39.956583 cell48](../evidence/fast-V040/strip-05.jpg)|
|B28 39.957–43.085|호수와 얼음 배경에서 낮은 사선 시점의 전면→측면, 젖은 반사 바닥|최종 주역 차량의 부피감과 환경 비유. 궤도 이동·회전·합성 중 원인은 미확정|[n958 PTS39.956583 cell48](../evidence/fast-V040/strip-05.jpg) → [n1033 PTS43.084708 cell10](../evidence/fast-V040/strip-06.jpg)|
|B29 43.085–46.797|검정 바탕의 짧은 흰 빛→삼각 윤곽 표식 유지|움직이는 차량→추상적 정체성의 안정. 이름과 행동 유도 문구는 불명|[n1033 PTS43.084708 cell10](../evidence/fast-V040/strip-06.jpg) → [n1121 PTS46.755042 cell21](../evidence/fast-V040/strip-06.jpg)|

## 연출과 이전 판단

청흑색의 젖은 도로와 얼음 세계, 흰 전조등·적색 후미등·삼각 기하 형태의 반복. 광원 반사의 흐림과 실제 차체 접촉을 구분. 같은 차량이라는 가설은 외형 반복에 근거하며, 원본 제목에 제시된 실차 성능의 증명이 아니다.

### 재사용 작동 방식·구성법의 단서 [INFERENCE]

차량의 접근·통과·이탈 + 차륜과 도로의 접촉 + 파편의 충돌·걷힘 + 안정된 정체성을 특정 구성법으로 묶는다. 기존 19의 금속·재질·주역 표현과 20의 차량 공간을 심화. 기술적 주장 검증은 별도.

## 미확인과 반례

이유에 대한 판단은 제작자의 의도나 효과를 검증하는 것이 아니다. 관찰한 색·형상·배치의 확신도는 높음, 미세 접촉·작은 문자는 중간~낮음. 렌즈 mm, 원본 촬영 fps, 장비·CG·합성 여부, 심리·효능은 UNKNOWN. 화면 변화가 카메라 이동인지 피사체 회전·크롭·합성인지는 상대적인 배경 변화 근거가 있을 때만 후보를 구분한다. 파일 제목의 공식 여부·바이럴 여부·실명·모델은 인증하지 않는다. 오디오 디코딩·ASR 결과는 별도 기계 모드이며, 음악 질감·효과음·박자 동기화는 청취 없이 판정하지 않는다.

## 도달 가능한 오디오 증거

전체 AAC 디코딩과 astats/silencedetect 측정 실행 rc0, 캐시된 faster-whisper small 로컬 ASR 3개 기계 가설. [ASR 원문](../evidence/fast-V040/offline-asr.json) · [측정 로그](../evidence/fast-V040/audio-decode-astats-silence.txt) · [런타임/해석 한계](../evidence/repo-worker-audio-evidence.json). 음악·질감·foley·lip sync는 실청취하지 않아 UNKNOWN이다. 단어 가설은 대사·음악·성능 약속의 사실 확인이 아니다.

## 도달 가능한 원본 텍스트 출처

[Dime Labs의 원본 URL](https://www.youtube.com/watch?v=bWF2AnQtyBs)을 실제 원문 reader로 확인했다. 결과: `CAPTION_TEXT_AUTO_UNTIMED`. [실제 응답](../evidence/provenance-original-V040.txt) · [제작자 주장과 캐시 위치](../creator-provenance.json). 자동 자막 원문은 시간 정보가 없으며 ASR와 마찬가지로 실청취·음악 식별·VO onset·동의·성능 입증이 아니다.
