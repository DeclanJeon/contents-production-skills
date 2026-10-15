# V048 — ＂Floral＂ by ADIDAS - AI Spec AD.mp4

[영상 색인으로 돌아가기](../video-index.md)

## 근거와 관찰 모드

archive_id `sha256:45d7ca847d384b532a9e5b0d2f3a0bd1fcc0a164d6bc155a630f44cd0592b348` / 28.403375s. [native PTS ledger](../evidence/fast-V048/extraction-manifest.json). fps 필터 없이 원본 ffprobe 의 frame n/PTS 를 사용했다. 전체 .5s nearest-after + scene>.30 후보 ±2 native frame + 후보 간 midpoint + first/last. 5개 strip 의 204개 frame 실제 판독. FRAMES_REVIEWED 이며 연속 재생/청취 아님. 후보 26개는 컷 수가 아니다. 아래 B 는 관찰 블록: scene/shot/phase 가 섞이므로 verified shot count 로 합산하지 않는다. 구간 경계는 인접 표본 사이 근사, source cut PTS 인증 아님. 표본 사이 미검출 짧은 컷 가능.

## 블록별 관찰과 기능

|블록 / 근사 s|실제 화면 관찰|WHY [INFERENCE], 대안·실패·이전|native frame locator|
|---|---|---|---|
|B01 0.000–1.502|짧은 검정 화면 → .083 파란 꽃무늬 의상의 인물이 자판기가 있는 홀 앞에서 걷기|의상 전체 / 앞으로 등장하기. 실제 장소와 실명은 불명|[n0 PTS0.000000 cell1](../evidence/fast-V048/strip-01.jpg) → [n36 PTS1.501500 cell11](../evidence/fast-V048/strip-01.jpg)|
|B02 1.502–2.336|좌측은 야외에서 쪼그린 주황색 의상의 인물, 우측은 빨간 모자 / 꽃무늬 셔츠 인물의 얼굴로 화면 분할|인물상 / 스타일 변주를 두 크기로 동시에 제시. 같은 인물이 아님|[n36 PTS1.501500 cell11](../evidence/fast-V048/strip-01.jpg) → [n56 PTS2.335667 cell18](../evidence/fast-V048/strip-01.jpg)|
|B03 2.336–3.170|넓은 모자 / 빨간 꽃무늬 수트의 인물이 소파에 팔을 벌리고 앉음. 뒤에는 트레포일 형태|자세 / 브랜드의 기하학적 형태 결합. 주체성 / 인물상의 심리를 단정하지 않음|[n56 PTS2.335667 cell18](../evidence/fast-V048/strip-01.jpg) → [n76 PTS3.169833 cell26](../evidence/fast-V048/strip-01.jpg)|
|B04 3.170–4.171|초록색 꽃무늬 의상의 여성 둘이 해 질 녘 거리에서 춤추고 웃음|함께하는 움직임이 원단과 옷의 맞음새를 드러냄. 성능상의 효능을 뜻하지 않음|[n76 PTS3.169833 cell26](../evidence/fast-V048/strip-01.jpg) → [n100 PTS4.170833 cell34](../evidence/fast-V048/strip-01.jpg)|
|B05 4.171–5.500|인물의 옆모습 실루엣, 꽃 벽 / 큰 트레포일 빛|의상 무늬를 환경으로 옮김|[n100 PTS4.170833 cell34](../evidence/fast-V048/strip-01.jpg) → [n132 PTS5.505500 cell40](../evidence/fast-V048/strip-01.jpg)|
|B06 5.500–6.089|산호색 3줄무늬 신발을 꽃밭에서 측면으로 강조한 삽입 화면|인물의 스타일 → 제품 형태. 삽입 화면의 합성 여부가 아니라, 명확히 보이는 배치만 판단|[n132 PTS5.505500 cell40](../evidence/fast-V048/strip-01.jpg) → [n146 PTS6.089417 cell43](../evidence/fast-V048/strip-01.jpg)|
|B07 6.089–6.799|문신이 있는 인물을 낮은 각도에서 봄. 양팔은 위로, 앞에는 민트색 신발 밑창|신발 밑창을 자세로 드러냄. 프레임 왜곡 / 수동 검사|[n146 PTS6.089417 cell43](../evidence/fast-V048/strip-01.jpg) → [n163 PTS6.798458 cell2](../evidence/fast-V048/strip-02.jpg)|
|B08 6.799–8.217|같은 낮은 각도의 발 / 바지, floral is here|동작 후 카피를 읽는 구간. 몸 / 신발의 잘림에 따른 절충|[n163 PTS6.798458 cell2](../evidence/fast-V048/strip-02.jpg) → [n197 PTS8.216542 cell10](../evidence/fast-V048/strip-02.jpg)|
|B09 8.217–9.134|3분할 화면의 인물 / 중앙의 트레포일 꽃 / 다른 빨간 셔츠 인물|컬렉션 / 브랜드 / 인물 초상을 분리. 형태 반복으로 정체성 제시|[n197 PTS8.216542 cell10](../evidence/fast-V048/strip-02.jpg) → [n219 PTS9.134125 cell18](../evidence/fast-V048/strip-02.jpg)|
|B10 9.134–10.511|수염 난 남성이 흰 꽃무늬 셔츠를 입고 정면에 있음. 작은 꽃잎이 떠다님|실제 원단의 꽃무늬 → 환경의 꽃잎으로 연결. 실명 인증 없음|[n219 PTS9.134125 cell18](../evidence/fast-V048/strip-02.jpg) → [n252 PTS10.510500 cell26](../evidence/fast-V048/strip-02.jpg)|
|B11 10.511–12.179|네온 홀에서 분홍색 의상의 인물이 춤춤, time to blossom|몸의 움직임과 카피. 정확한 박자 동기화는 청취 필요|[n252 PTS10.510500 cell26](../evidence/fast-V048/strip-02.jpg) → [n292 PTS12.178833 cell35](../evidence/fast-V048/strip-02.jpg)|
|B12 12.179–13.972|수영장 안에서 문신이 있는 등의 뒷모습. 수면에는 붉은 꽃|꽃의 물질적 상태를 물의 세계로 옮김. 같은 인물이라는 해석은 상징적 가설|[n292 PTS12.178833 cell35](../evidence/fast-V048/strip-02.jpg) → [n335 PTS13.972292 cell44](../evidence/fast-V048/strip-02.jpg)|
|B13 13.972–14.765|벚꽃 길에서 분홍색 트랙수트의 인물이 춤춤|실외의 넓은 화면에서 의상 / 실루엣 제시. 발 접촉 검사|[n335 PTS13.972292 cell44](../evidence/fast-V048/strip-02.jpg) → [n354 PTS14.764750 cell3](../evidence/fast-V048/strip-03.jpg)|
|B14 14.765–15.349|초록색 의상의 여성 둘이 거리에서 몸짓하며 재등장|앞서 나온 인물상을 다시 제시. 의상 / 사람의 동일성 검사|[n354 PTS14.764750 cell3](../evidence/fast-V048/strip-03.jpg) → [n368 PTS15.348667 cell10](../evidence/fast-V048/strip-03.jpg)|
|B15 15.349–16.141|주황색 꽃무늬 수트의 인물이 춤춤. 주황색 벽에는 트레포일 두 개|의상과 브랜드 벽의 색을 맞춤. 심리 효과 검증 없음|[n368 PTS15.348667 cell10](../evidence/fast-V048/strip-03.jpg) → [n387 PTS16.141125 cell18](../evidence/fast-V048/strip-03.jpg)|
|B16 16.141–16.725|보라색 의상의 여성 3인이 네온 거리에서 동작|집단 동선과 배치 / 의상 변주. 인원 증감 / 원단 SSOT|[n387 PTS16.141125 cell18](../evidence/fast-V048/strip-03.jpg) → [n401 PTS16.725042 cell25](../evidence/fast-V048/strip-03.jpg)|
|B17 16.725–17.768|흰 꽃무늬 의상 / 베이지색 바지의 인물이 공중에서 옆으로 자세를 취함. 주변에 꽃잎|움직임의 정점에서 원단 / 제품을 보여 줌. 실제 속도 / 착지는 불명|[n401 PTS16.725042 cell25](../evidence/fast-V048/strip-03.jpg) → [n426 PTS17.767750 cell33](../evidence/fast-V048/strip-03.jpg)|
|B18 17.768–19.102|노란 상의 / 꽃무늬 바지의 인물이 젖은 바닥에서 춤춤. 고양이 벽화|큰 그래픽 형태와 인물 자세의 대비. 환경 속 로고 권리는 별도|[n426 PTS17.767750 cell33](../evidence/fast-V048/strip-03.jpg) → [n458 PTS19.102417 cell41](../evidence/fast-V048/strip-03.jpg)|
|B19 19.102–20.229|빨간 트레포일 벽 앞의 인물이 점프 → 다리를 넓게 벌림|준비 동작 / 공중에서 확장하는 구간. 정확한 착지는 원본 표본에서 미검증|[n458 PTS19.102417 cell41](../evidence/fast-V048/strip-03.jpg) → [n485 PTS20.228542 cell1](../evidence/fast-V048/strip-04.jpg)|
|B20 20.229–20.771|흰 하이톱의 꽃무늬를 측면으로 강조한 화면, 꽃잎|움직임 속 신발을 정적인 제품으로 제시. 실제 SKU는 불명|[n485 PTS20.228542 cell1](../evidence/fast-V048/strip-04.jpg) → [n498 PTS20.770750 cell7](../evidence/fast-V048/strip-04.jpg)|
|B21 20.771–21.688|주황색 / 파란색 꽃무늬 러닝화를 꽃밭에서 강조한 화면|같은 브랜드 세계 속 서로 다른 형태. 신발 변형의 일관성은 별도|[n498 PTS20.770750 cell7](../evidence/fast-V048/strip-04.jpg) → [n520 PTS21.688333 cell15](../evidence/fast-V048/strip-04.jpg)|
|B22 21.688–22.273|물 위 꽃무늬 플립플롭의 측면, 주변에 꽃|제품군 / 물의 물질적 대비. 방수 주장 아님|[n520 PTS21.688333 cell15](../evidence/fast-V048/strip-04.jpg) → [n534 PTS22.272250 cell22](../evidence/fast-V048/strip-04.jpg)|
|B23 22.273–22.940|파란색 / 보라색 하이톱 아래 주황색 빛, 꽃잎|조명 / 재질의 환상적 변주. 실제 발광 기능 아님|[n534 PTS22.272250 cell22](../evidence/fast-V048/strip-04.jpg) → [n550 PTS22.939583 cell29](../evidence/fast-V048/strip-04.jpg)|
|B24 22.940–23.732|금색 배경에서 꽃무늬 수트의 인물이 한쪽 다리로 발차기. 흰 입자|신발 / 프레임 가장자리 / 동작의 정점. 물리적 자세의 안정성 검사|[n550 PTS22.939583 cell29](../evidence/fast-V048/strip-04.jpg) → [n569 PTS23.732042 cell36](../evidence/fast-V048/strip-04.jpg)|
|B25 23.732–25.150|빨간 셔츠 / 넓은 바지의 인물이 수평으로 점프. 뒤에는 검은 트레포일 벽|의상 실루엣 / 정체성의 일체화. 트램펄린 등 제작 방법은 불명|[n569 PTS23.732042 cell36](../evidence/fast-V048/strip-04.jpg) → [n603 PTS25.150125 cell45](../evidence/fast-V048/strip-04.jpg)|
|B26 25.150–27.903|다리를 넓게 벌려 웅크린 뒤 자세를 안정시킴 → 25.526 큰 붉은 꽃 / floral by trefoil|정점 → 안정 / 카피 유지. 꽃과 몸이 브랜드를 가리는 실패 가능성|[n603 PTS25.150125 cell45](../evidence/fast-V048/strip-04.jpg) → [n669 PTS27.902875 cell7](../evidence/fast-V048/strip-05.jpg)|
|B27 27.903–28.403|28.4까지 검정 후미 구간|원본의 검정 후미 구간 분리. 섬광 누락 / 작품 의도는 불명|[n669 PTS27.902875 cell7](../evidence/fast-V048/strip-05.jpg) → [n680 PTS28.361667 cell12](../evidence/fast-V048/strip-05.jpg)|

## 연출과 이전 판단

꽃무늬·꽃밭·꽃잎·물꽃·그래픽 마크가 컬렉션 세계를 연결하는 단서다. 여러 인물과 서로 다른 신발을 단일 여정이나 한 SKU의 변환으로 부르면 오류다. 검출 후보 26개와 관찰 블록 27개(B01–B27)는 서로 다른 집계이며, 어느 쪽도 실제 컷 수를 확정하지 않는다.

### 재사용 원리·구성 절차의 단서 [INFERENCE]

의상 무늬 → 환경의 은유 → 몸의 동작 / 접촉 → 신발 형태 강조 → 컬렉션 변주 → 카피. 04 동선과 배치 / 19 원단과 제품 / 20 세계 / 09 정점과 안정 / 25 대응 관계를 심화. 공중 자세만 보고 슬로모션 촬영 기법을 확정하지 않음.

## 미확인과 반례

WHY는 제작자 의도 / 효과 검증이 아니다. 관찰 색·형상·배치의 확신도는 높음, 미세 접촉 / 작은 문자는 중간~낮음. 렌즈 mm, 원본 촬영 fps, 장비 / CG / 합성 여부, 심리 / 효능은 UNKNOWN. 화면 변화가 카메라 이동인지 피사체 회전 / 크롭 / 합성인지는 상대적인 배경 변화 근거가 있을 때만 후보를 구분한다. 파일 제목의 공식 / 바이럴 / 실명 / 모델은 인증하지 않는다. 오디오 디코딩 / ASR 결과는 별도 기계 모드이며, 음악 질감 / 효과음 / 박자 동기화는 청취 없이 판정하지 않는다.

## 도달 가능한 오디오 증거

전체 AAC 디코딩과 astats/silencedetect 측정 실행 rc0, 캐시된 faster-whisper small 로컬 ASR 12개 기계 가설. [ASR 원문](../evidence/fast-V048/offline-asr.json) · [측정 로그](../evidence/fast-V048/audio-decode-astats-silence.txt) · [런타임/해석 한계](../evidence/repo-worker-audio-evidence.json). 음악·질감·foley·lip sync는 실청취하지 않아 UNKNOWN이다. 단어 가설은 대사·음악·성능 약속의 사실 확인이 아니다.

## 도달 가능한 원본 텍스트 출처

[RabbitHole의 원본 URL](https://www.youtube.com/watch?v=VfKDzZybjiA)을 실제 원문 reader로 확인했다. 결과: `CAPTION_UNAVAILABLE_READER`. [실제 응답](../evidence/provenance-original-V048.txt) · [제작자 주장과 캐시 위치](../creator-provenance.json). 이번 reader에 자막이 없다는 결과만 기록한다. 캐시 설명의 제작·음악 credit가 없는 것으로 확대 해석하지 않는다.
