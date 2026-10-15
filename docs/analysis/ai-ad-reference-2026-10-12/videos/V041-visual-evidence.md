# V041 — This Liquid Death Commercial Was Made by AI—And It Slaps.mp4

[영상 색인으로 돌아가기](../video-index.md)

## 근거와 관찰 모드

archive_id `sha256:6c21cb4399bc8bc959028d387d566c7845bc226de30d94d84021042347b43c0a` / 61.700000s. [native PTS ledger](../evidence/fast-V041/extraction-manifest.json). fps 필터 없이 원본 ffprobe 의 frame n/PTS 를 사용했다. 전체 .5s nearest-after + scene>.30 후보 ±2 native frame + 후보 간 midpoint + first/last. 6개 strip 의 288개 frame 실제 판독. FRAMES_REVIEWED 이며 연속 재생/청취 아님. 후보 29개는 컷 수가 아니다. 아래 B 는 관찰 블록: scene/shot/phase 가 섞이므로 verified shot count 로 합산하지 않는다. 구간 경계는 인접 표본 사이 근사, source cut PTS 인증 아님. 표본 사이 미검출 짧은 컷 가능.

## 블록별 관찰과 기능

|블록 / 근사 s|실제 화면 관찰|WHY [INFERENCE], 대안·실패·이전|native frame locator|
|---|---|---|---|
|B01 0.000–1.933|눈밭의 긴 도로, 붉은 승용차와 경찰차, 그 사이에 서 있는 사람|먼 거리의 넓은 화면으로 교통 정지 상황과 두 차량의 관계를 설정함. 실제 사건은 아님|[n0 PTS0.000000 cell1](../evidence/fast-V041/strip-01.jpg) → [n58 PTS1.933333 cell8](../evidence/fast-V041/strip-01.jpg)|
|B02 1.933–4.200|경찰 배지, 파란 외투, 털모자를 착용한 중년 인물의 정면과 입 움직임|의상을 통해 권위 역할로 읽음. '경찰관'은 극중 역할이라는 가설|[n58 PTS1.933333 cell8](../evidence/fast-V041/strip-01.jpg) → [n126 PTS4.200000 cell18](../evidence/fast-V041/strip-01.jpg)|
|B03 4.200–4.767|붉은 차 창 안의 콧수염이 있는 젊은 인물, 전경의 경찰 어깨|서로 마주 보는 인물을 번갈아 보여 주는 화면의 역할과 시선 축. 대사를 청취·검증하지 않았으므로 위반 종류는 불명.|[n126 PTS4.200000 cell18](../evidence/fast-V041/strip-01.jpg) → [n143 PTS4.766667 cell24](../evidence/fast-V041/strip-01.jpg)|
|B04 4.767–6.033|조수석에 밝은 Liquid Death 캔 여러 개|차 안 소품의 공개가 제품과 이야기를 연결함. 캔 수의 연속성 검사|[n143 PTS4.766667 cell24](../evidence/fast-V041/strip-01.jpg) → [n181 PTS6.033333 cell32](../evidence/fast-V041/strip-01.jpg)|
|B05 6.033–7.500|손이 밝은 캔을 창밖에 들고 있으며 로고가 보임|권하는 몸짓과 읽을 수 있는 라벨이 동시에 나타남. 음료 효능의 증거는 아님|[n181 PTS6.033333 cell32](../evidence/fast-V041/strip-01.jpg) → [n225 PTS7.500000 cell40](../evidence/fast-V041/strip-01.jpg)|
|B06 7.500–9.533|경찰 인물이 캔을 입에 대고 내림|권하기→한 모금 마시기→반응 단계. 입과 캔의 접촉 및 양손의 일관성|[n225 PTS7.500000 cell40](../evidence/fast-V041/strip-01.jpg) → [n286 PTS9.533333 cell1](../evidence/fast-V041/strip-02.jpg)|
|B07 9.533–11.800|운전석 인물의 웃음→안정된 표정|음료를 마신 후 상대의 반응. 맛에 만족했다고 확정하지 않음|[n286 PTS9.533333 cell1](../evidence/fast-V041/strip-02.jpg) → [n354 PTS11.800000 cell11](../evidence/fast-V041/strip-02.jpg)|
|B08 11.800–15.833|경찰이 다시 한 모금 마심→캔을 내리고 입을 움직임|첫 모금의 반복으로 머무름과 대화 지연을 읽음. 정확한 대사의 ASR은 별도|[n354 PTS11.800000 cell11](../evidence/fast-V041/strip-02.jpg) → [n475 PTS15.833333 cell25](../evidence/fast-V041/strip-02.jpg)|
|B09 15.833–19.867|운전자가 아래를 봄→경찰 쪽으로 시선을 향하고 말함|다른 장면을 삽입하는 화면으로 넘어갈 이야기 제시 후보. 이 시선만으로 의도는 불명|[n475 PTS15.833333 cell25](../evidence/fast-V041/strip-02.jpg) → [n596 PTS19.866667 cell39](../evidence/fast-V041/strip-02.jpg)|
|B10 19.867–21.367|차량 앞 그릴과 번호판의 근접 화면, 21s에는 번호판 없이 붉은 패널|차량 식별 요소가 변했을 가능성. 의도적인 개그 또는 AI 연속성 실패라는 대안|[n596 PTS19.866667 cell39](../evidence/fast-V041/strip-02.jpg) → [n641 PTS21.366667 cell48](../evidence/fast-V041/strip-02.jpg)|
|B11 21.367–22.533|경찰의 근접 화면에서 고개를 돌리고 옆으로 시선을 향함|이상한 소품 이후 상대의 반응. 앞 화면과의 실제 인과는 미확인|[n641 PTS21.366667 cell48](../evidence/fast-V041/strip-02.jpg) → [n676 PTS22.533333 cell8](../evidence/fast-V041/strip-03.jpg)|
|B12 22.533–23.700|운전자가 웃고 말함|반복 대화의 기준점. 이야기의 현재 위치를 유지함|[n676 PTS22.533333 cell8](../evidence/fast-V041/strip-03.jpg) → [n711 PTS23.700000 cell16](../evidence/fast-V041/strip-03.jpg)|
|B13 23.700–25.100|붉은 차 트렁크 틈으로 손이 밖으로 늘어짐|대화 사이에 부조리한 장면을 공개함. 실제 피해나 범죄 사실은 아님|[n711 PTS23.700000 cell16](../evidence/fast-V041/strip-03.jpg) → [n753 PTS25.100000 cell25](../evidence/fast-V041/strip-03.jpg)|
|B14 25.100–26.200|운전자의 시선이 아래→상대로 향함|가방과 뒤칸의 개그 뒤 자연스러운 태도와의 대비. 인물의 무심함은 가설|[n753 PTS25.100000 cell25](../evidence/fast-V041/strip-03.jpg) → [n786 PTS26.200000 cell33](../evidence/fast-V041/strip-03.jpg)|
|B15 26.200–28.700|차 내부 뒷좌석의 사람과 아이처럼 작은 인물, 많은 짐과 새장|좁은 차를 다른 사회적 세계로 드러냄. 인원, 관계, 실명은 불명|[n786 PTS26.200000 cell33](../evidence/fast-V041/strip-03.jpg) → [n861 PTS28.700000 cell44](../evidence/fast-V041/strip-03.jpg)|
|B16 28.700–29.867|운전자가 눈을 감고 입을 움직임|화면의 위험과 평온한 표정의 대비. 대사를 청취·검증하지 않았으므로 거짓말 여부는 판단 불가.|[n861 PTS28.700000 cell44](../evidence/fast-V041/strip-03.jpg) → [n896 PTS29.866667 cell4](../evidence/fast-V041/strip-04.jpg)|
|B17 29.867–31.533|도로 옆에 뒤집힌 큰 트럭, 문 쪽의 불, 사람이 눈바닥으로 넘어짐|큰 피해 규모로 개그를 강화함. 실제 사고나 안전 시연은 아님|[n896 PTS29.866667 cell4](../evidence/fast-V041/strip-04.jpg) → [n946 PTS31.533333 cell13](../evidence/fast-V041/strip-04.jpg)|
|B18 31.533–32.500|운전자의 위쪽 시선→웃음|큰 사고의 삽입 화면 이후 태연한 반응과의 대비|[n946 PTS31.533333 cell13](../evidence/fast-V041/strip-04.jpg) → [n975 PTS32.500000 cell20](../evidence/fast-V041/strip-04.jpg)|
|B19 32.500–33.800|어질러진 점포 바닥의 두 인물, 붉은 원통 다발과 선|의심스러운 소품을 새 공간으로 확장함. 폭발물이나 범죄로 단정 금지|[n975 PTS32.500000 cell20](../evidence/fast-V041/strip-04.jpg) → [n1014 PTS33.800000 cell28](../evidence/fast-V041/strip-04.jpg)|
|B20 33.800–35.367|붉은 물체의 #Team Diddy 스티커 근접 화면|문자와 문화적 참조의 실제 화면 증거. 특정 인물의 실제 연루를 주장하는 것은 아님|[n1014 PTS33.800000 cell28](../evidence/fast-V041/strip-04.jpg) → [n1061 PTS35.366667 cell37](../evidence/fast-V041/strip-04.jpg)|
|B21 35.367–37.433|눈밭 도로 중앙의 큰 고래형 동물, 꼬리 움직임과 입김 같은 흰색 형상|규모의 불가능성으로 부조리를 확대함. 실제 고래 구조 장면은 아님|[n1061 PTS35.366667 cell37](../evidence/fast-V041/strip-04.jpg) → [n1123 PTS37.433333 cell47](../evidence/fast-V041/strip-04.jpg)|
|B22 37.433–39.000|수영장 물 위의 소품, 뒤쪽의 문들과 작은 인물 및 의자|추운 도로변과 다른 공간으로 전환함. 지리적 연결은 불명|[n1123 PTS37.433333 cell47](../evidence/fast-V041/strip-04.jpg) → [n1170 PTS39.000000 cell7](../evidence/fast-V041/strip-05.jpg)|
|B23 39.000–40.800|운전자 뒤의 붉은 좌석과 팔을 위로 든 자세, 40.8에 원래 좌석으로 복귀|동일 인물과 차 내부의 연속성 변화. 개그인지 인물 동일성 결함인지 비교 필요|[n1170 PTS39.000000 cell7](../evidence/fast-V041/strip-05.jpg) → [n1224 PTS40.800000 cell16](../evidence/fast-V041/strip-05.jpg)|
|B24 40.800–43.267|눈밭에서 붉은 후드를 쓴 인물들이 불 둘레에 원형으로 모여 있음, 작은 오두막|앞의 개그들보다 집단 규모가 큼. 원본 캐릭터의 실제 행위로 읽지 않음|[n1224 PTS40.800000 cell16](../evidence/fast-V041/strip-05.jpg) → [n1298 PTS43.266667 cell27](../evidence/fast-V041/strip-05.jpg)|
|B25 43.267–44.833|운전자가 다시 경찰 방향을 응시하고 입을 움직임|삽입 화면 뒤 현재 대화의 기준점으로 돌아옴|[n1298 PTS43.266667 cell27](../evidence/fast-V041/strip-05.jpg) → [n1345 PTS44.833333 cell36](../evidence/fast-V041/strip-05.jpg)|
|B26 44.833–48.167|경찰이 내려다봄→촛불이 꽂힌 케이크가 들림, 다시 말함|케이크라는 일상 소품과 권위 역할의 대비. 생일 행사라는 사실은 아님|[n1345 PTS44.833333 cell36](../evidence/fast-V041/strip-05.jpg) → [n1445 PTS48.166667 cell48](../evidence/fast-V041/strip-05.jpg)|
|B27 48.167–50.133|운전자의 웃음과 위쪽 시선→눈을 감음|이야기를 마무리하는 반응. 기쁨이나 승리라는 해석은 가설|[n1445 PTS48.166667 cell48](../evidence/fast-V041/strip-05.jpg) → [n1504 PTS50.133333 cell10](../evidence/fast-V041/strip-06.jpg)|
|B28 50.133–51.800|경찰이 입을 크게 벌리고 케이크 쪽으로 고개를 내림|강한 반응 후 소품 확인. 소리를 청취·검증하지 않았으므로 고함 여부는 불명.|[n1504 PTS50.133333 cell10](../evidence/fast-V041/strip-06.jpg) → [n1554 PTS51.800000 cell19](../evidence/fast-V041/strip-06.jpg)|
|B29 51.800–54.467|운전자가 웃고 말하는 화면을 유지함|대화의 결말. 정확한 마지막 웃음 유발 대사는 ASR 기계 모드와 분리|[n1554 PTS51.800000 cell19](../evidence/fast-V041/strip-06.jpg) → [n1634 PTS54.466667 cell30](../evidence/fast-V041/strip-06.jpg)|
|B30 54.467–59.500|밝은 배경에서 왼쪽의 캔이 회전함, 오른쪽에 Arrestingly Refreshing.|경찰 역할↔arrestingly 말장난을 회수함. 제품 정체성은 안정적|[n1634 PTS54.466667 cell30](../evidence/fast-V041/strip-06.jpg) → [n1785 PTS59.500000 cell43](../evidence/fast-V041/strip-06.jpg)|
|B31 59.500–61.700|같은 캔과 카피 아래에 Made With AI|제작 고지 층위. 실제 사용 모델이나 제작자의 권리를 입증하는 것은 아님|[n1785 PTS59.500000 cell43](../evidence/fast-V041/strip-06.jpg) → [n1850 PTS61.666667 cell48](../evidence/fast-V041/strip-06.jpg)|

## 연출과 이전 판단

대화의 고정된 기준점 사이에 불가능한 삽입 화면을 넣고, 경찰과 운전자의 태도 대비를 유지한다. 화면의 UNOFFICIAL SPEC AD는 고지에 대한 관찰이지 권리 승인이 아니다. 원본을 실제 인물, 범죄, 문화적 연루에 대한 주장으로 재서술하면 실패한다.

### 재사용 작동 원리·제작 절차의 출발점 [INFERENCE]

이야기의 기준점→점차 강화되는 삽입 화면→미약한 반응→제품 말장난 회수. 04 목표/행동/결과와 09 반응 편집, 19의 소품 SSOT, 25의 출처 검토 모드에서 심화한다. 이전 시 소재의 명예와 권리에 대한 품질 검증을 우선한다.

## 미확인과 반례

WHY는 제작자의 의도나 효과를 검증한 것이 아니다. 관찰한 색·형상·배치의 확실성은 높음, 미세 접촉과 작은 문자는 중간~낮음. 렌즈 mm, 원본 촬영 fps, 장비/CG/합성 여부, 심리/효능은 UNKNOWN. 화면 변화가 카메라 이동인지 피사체 회전/크롭/합성인지는 상대적인 배경 변화 근거가 있을 때만 후보를 구분한다. 파일 제목의 공식 여부, 입소문 확산, 실명, 모델은 인증하지 않는다. 오디오 디코딩과 ASR 결과는 별도 기계 모드이며, 음악 질감, 효과음, 박자 동기화는 청취 없이 판정하지 않는다.

## 도달 가능한 오디오 증거

전체 AAC 디코딩과 astats/silencedetect 측정 실행 rc0, 캐시된 faster-whisper small 로컬 ASR 10개 기계 가설. [ASR 원문](../evidence/fast-V041/offline-asr.json) · [측정 로그](../evidence/fast-V041/audio-decode-astats-silence.txt) · [런타임/해석 한계](../evidence/repo-worker-audio-evidence.json). 음악·질감·foley·lip sync는 실청취하지 않아 UNKNOWN이다. 단어 가설은 대사·음악·성능 약속의 사실 확인이 아니다.

## 도달 가능한 원본 텍스트 출처

[MeatingAI의 원본 URL](https://www.youtube.com/watch?v=FYFNJZMpaes)을 실제 원문 reader로 확인했다. 결과: `CAPTION_UNAVAILABLE_READER`. [실제 응답](../evidence/provenance-original-V041.txt) · [제작자 주장과 캐시 위치](../creator-provenance.json). 이번 reader에 자막이 없다는 결과만 기록한다. 캐시 설명의 제작·음악 credit가 없는 것으로 확대 해석하지 않는다.
