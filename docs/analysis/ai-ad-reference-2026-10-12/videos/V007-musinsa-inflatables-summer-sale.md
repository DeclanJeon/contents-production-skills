# V007 — MUSINSA 「그냥 지나칠 수 없어, 무진장」 인플레이터블 캐릭터 세일 광고
[← 전체 영상 색인](../video-index.md)

## 확인 범위 / 출처
- 안정 ID `sha256:f71e79b9090c19a256fb5d48a0fa6d5c21016c65428b104ecf330d41fe8cf18d`; 원본 파일명 `[무진장 성공 기원 AI 광고제] 본선 진출작 ： 그냥 지나칠 수 없어, 무진장.mp4`. 파일명과 화면 표식에 광고제/플랫폼명이 보이지만, 공식 브랜드 캠페인인지 별도로 확인하지 않았다.
- 길이 28.445083초; 1920×1080, 24000/1001 fps; timebase 1/24000, 시작 PTS 0, duration_ts 682682; AV1/AAC stereo; 전체 영상 디코드 rc=0(기계 인벤토리).
- **FRAMES_REVIEWED:** `read(video)` 미리보기 격자, 0–28 정수초 PTS 표본, 기존 6개 grouped candidate sheet 및 raw 6-event supplement(18개 고유 네이티브 프레임/1 strip의 n−2/n/n+2)를 검토했다(`evidence/raw-review-V007/`, [원장](../raw-candidate-coverage-first24.json)). 실제 마지막 프레임 n=681/PTS28.403375 (`evidence/V007/native-terminal.jpg`)은 오렌지 바탕 중앙의 검정 `MUSINSA`다. 컷 수나 연속 재생을 주장하지 않는다. 표본 사이 카메라 움직임과 효과음/음성은 확인되지 않았다.
**오디오 한계:** AAC 스트림은 있으나 오디오를 청취하지 않았다. VO/음악/SFX/믹스는 UNKNOWN. 오프라인 ASR은 실행됐지만 반환된 구간은 0개(`NO_SEGMENTS_RETURNED`; 영어 언어 가설 confidence 0.3684)다. 이는 발화가 없다는 증거가 아니며, 대사·음악·음향 설계의 근거로 사용할 수 없다.

## 장면·샷·행동단계 원장
각 초표본은 nearest integer-second preview이며 PTS 경계가 아니다. 이벤트 후보 중심은 inventory/`candidate-neighborhoods.json`; 전후 샘플은 시트 001–003에 원본 PTS로 표기. 장면은 시각적 관계를 묶고, 컷과 튜브 캐릭터 동작·카피 reveal은 따로 기록한다.

| 그룹 / 대략 시간 | 화면에서 실제 보이는 구성 | 샷/행동 관찰과 후보 증거 | 기능 해석 및 대안 |
|---|---|---|---|
| G01 0–8.9초: sky-mascot + 질문 | 밝고 매끈한 푸른 하늘 아래 주황색 길쭉한 튜브형 인형이 팔을 들어 흔들고 몸통을 구부림; 눈 두 개·검은 동공과 흰 종이띠 같은 머리 장식. 화면 위 MUSINSA, 좌하단 오렌지 AI 광고제 수상 배지, 우하단 AI 생성 고지. 큰 갈색/주황 문장 `그냥 지나칠 거야?`가 6s 부근 대형으로 걸림. | 정수초 0–8은 같은 하늘과 같은 주황 마스코트가 이어지며 인형 팔/상체가 춤추는 action phase가 지속. 주위가 지나치게 단순한 sky-frame이라 캐릭터 실루엣·카피가 주의 중심. 1–5s 등에는 camera scale/자세 변화가 보이지만 연속 재생이 아니므로 pan/zoom 결론 금지. | 소리 없는(화면 기준) 독립적인 몸통춤과 말 거는 듯한 큰 질문으로 스크롤/보행자에게 멈추라는 암시. 제품 대신 세일 구경을 호소하는 캐릭터 커머스. 카피가 하늘 위에서 캐릭터 일부를 가리므로 글자/표정 동시 가독성 경쟁 가능. |
| G02 8.967–15.35초: 점포 앞 공중 응원인형 | 현대식 유리 쇼핑몰의 외부 MUSINSA 매장, 하늘·건물에 맞닿은 여러 키 큰 튜브 인형(주황/검정)이 구부러지고 팔을 흔듦. 흰 머리끈/검은 술 모양 장식, 원형 눈. t9 원경에서 storefront 전경으로 이동해 t10–12에 검정 두 캐릭터와 주황 캐릭터가 저각으로 매우 크게 프레임에 들어옴. | C01 pre PTS 8.842167 → candidate 8.967292 → post 9.092417: sky-body image에서 점포와 그룹이 있는 wide scene으로 전환. C01에서 sky 색·지평선이 없어지고 storefront/실재 보행환경이 드러나므로 높은 확신의 새 scene setup. t10–12 표본은 같은 정면/저각 그룹에서 인형이 춤추고 서로 겹치는 action phase. camera pan/tracking vs 바람/몸체 sway 불명. | 다수 인형 및 건물 facade 규모 대비가 거대한 프로모션/거리 스펙터클을 줌. 실제 wind-dancer 소재인지 CGI/AI인지 구분 불가. 검정은 주황과의 대비, 매장 외관은 할인 행동을 실매장·플랫폼에 연결할 수 있음. |
| G03 ~15.35–19.77초: 5주년/최대할인 시각 은유 + 쇼핑객 | 주황 인플레이터블 몸체의 근접 shot에 흰 `UP TO 80%`와 중앙/하단 `역대급 세일`, 작은 `무진장 블프 5주년 기념`. t17에는 MUSINSA 입구 앞 캐주얼 옷차림 쇼핑객 둘이 주황색 세일 쇼핑백을 들고 걷는다. `UP TO 80%`는 화면 copy이며 적용 대상/조건은 별도 검증되지 않았다. | C02 15.223542→15.348667→15.473792에서는 글자/몸체가 가득한 화면에서 건물 외부와 인형으로 돌아감. 두 쇼핑객의 걷기와 가방 흔들림은 행동 관찰이며, exact camera move/인물 연속성은 미확정. | 인플레이터블 몸체 자체를 할인 copy surface로 쓰고 실점포·쇼핑백을 뒤이어 보여 광고의 상업 맥락을 연결한다. 대안은 할인율을 독립된 큰 CTA 카드에 두는 것; 혜택 숫자의 노출만으로 약관/유효성을 입증하지 않는다. |
| G04 ~19.77–22.439초: 쇼핑백/마스코트 punchline | t19 큰 주황 쇼핑백/가방에 검정 붓글씨 무진장, 아래 `26 Summer Black Friday`; 이어 매장 유리와 판매점 맥락에서 흰 술 같은 머리가 달린 주황 캐릭터 정면, 왼쪽 카피 `미안해질 만큼 싸다`. C04 19.646425→19.769750→19.894875는 큰 orange bag graphic을 거쳐 캐릭터/미안해질 만큼 싸다로 넘어감. C05 22.313958→22.439083→22.564208에서 실제 매장 앞 마스코트가 전각 orange/black campaign endcard로 바뀜. | close-up bag graphic↔character portrait는 확실히 다른 구성. `미안해질 만큼 싸다`는 t20–22 눈/팔 동작 변동 속에서 화면에 고정돼 보이며 글자별 동작으로 오독 금지. C05는 배경/캐릭터에서 평면 full-frame orange endcard로 명백한 re-set. | 가격 혜택을 과장된 의인화 표현(너무 싸서 미안함)으로 귀엽게 만든다. 쇼핑백-캐릭터의 제품/브랜드 관계를 시각적으로 이어줌. 장바구니 전환 등의 실제 CTA는 직접 보이지 않음. |
| G05 약 22.439–28.445초: 세일 endcard + 재등장 mascot | Orange background, layered 빨강 brush-stroke shape, 큰 검정 한글 `무신사 무진장`, `26 Summer Black Friday`, `MUSINSA 역대급 할인 최대 80% \| 2026.06.14(일) - 06.24(수)`로 읽히는 정보가 t23–25. 실제 terminal frame n=681/PTS28.403375에는 중앙 검정 `MUSINSA` wordmark만 남는다 (`evidence/V007/native-terminal.jpg`). | C06 25.191833→25.316958→25.442083에서 세일 endcard pre-image 뒤 매장 내부 진열, 분홍 MUSINSA 캡·검정 선글라스·밝은 하와이안 셔츠·종이/술 머리 인플레이터블 portrait가 들어오며 배경/세트가 교체된다. 마지막 wordmark 전환 시각은 이 neighborhood에서 확정 불가. | CTA 숫자/기간을 판독 가능한 full-field에 제시한 뒤 캐릭터 착장 tag로 브랜드 개성을 남긴다. 이 마네킹형 mascot styling이 거대한 floating tube 캐릭터와 동일 개체/실제 상품 wearer임을 증명하지 않는다. |
### 후보 변화별 기능·대안 (R ≠ verified cut)

| 후보 / source PTS pre→center→post | OBSERVED 변화 | bounded WHY / alternative | QA·전이 기준 |
|---|---|---|---|
| R001 8.883875→8.967292→9.050708 | 하늘만 있던 주황 튜브형 캐릭터 구도에서 점포 façade와 여러 대형 캐릭터가 함께 보이는 거리 wide로 바뀐다. | 추상적 장난감을 실제 쇼핑 환경에 연결해 세일 맥락을 공개할 수 있다. 대안: 별도 공간으로의 ordinary cut이며 같은 캐릭터/장치 아님. | 캐릭터 수/방향/scale과 건물 사이 기준을 확인; morph면 얼굴·seam을 통해 몸체가 녹아들지 않게 한다. |
| R002 15.265250→15.348667→15.432083 | 주황 몸체의 `UP TO 80%` 글자와 건물 전경 사이에서 실외 storefront/캐릭터 장면으로 전환; pre에 읽히는 할인문구가 있다. | 혜택을 표면에 잠시 고정한 뒤 매장/행동으로 돌려 읽기와 상황을 분리할 수 있다. 대안: 인형/건물 사이 이미지교체. | discount eligibility/조건 증명은 외부 승인자료 필요; 화면에 보인 문자열을 본문에도 정확히 유지. |
| R003 16.975292→17.058708→17.142125 | 상점 앞 쇼핑객 두 명과 주황 가방이 전경; 얼굴·가방을 함께 보여주고 배경에 storefront가 있다. | offer 뒤에 사람/가방을 두어 소매 규모와 사용 맥락을 붙일 수 있다. 대안: 구매 후기나 실제 고객 증거가 아닌 staged/collage vignette. | testimonial로 사용하려면 실제 동의/증거 확보; 가방 mark/보행방향/인물 identity 과장 금지. |
| R004 19.686333→19.769750→19.853167 | 붉은 붓글씨가 있는 오렌지 쇼핑백/graphic에서 점포 앞 주황 마스코트와 `미안해질 만큼 싸다` 문구로 바뀐다. | 쇼핑백을 독립 상징에서 personified sale joke로 이어가며 가격 톤을 유머로 바꿀 수 있다. 대안: tag만 바뀌거나 동일 매장 내부 장면일 수 있다. | 글자 가독성과 캐릭터 표정/팔 동작이 충돌하지 않는지 확인; 실제 구매·저가를 입증하는 카피 아님. |
| R005 22.355667→22.439083→22.522500 | storefront의 mascot/문구에서 opaque 오렌지 full-field campaign graphic으로 장면 전체가 재설정된다. | 서사형 캐릭터/상품 정보를 끝내고 offer/date를 정지된 판독 공간으로 옮길 수 있다. 대안: 급한 style break로 전환. | 긴 날짜·조건과 최대할인을 읽을 hold/대비를 확인; 실제 법무 승인/현재 기간이 있어야 재사용 가능. |
| R006 25.233542→25.316958→25.400375 | endcard 이후 매장 내부처럼 보이는 장면에 분홍 캡·검은 선글라스·꽃무늬 셔츠를 입은 styled character portrait가 나온다. | 평면 offer 뒤에 마스코트를 다시 넣어 캐릭터 기억을 회수할 수 있다. 대안: 별개 진열 mannequin/product portrait, 이전 inflatables와 동일 개체 아님. | 캐릭터/의상/IP 권리 확인, 이전 inflated body와 동일 persona/상품을 암시하지 않는다; 종료 wordmark/native last frame을 별도 확인. |

G01 안의 팔·몸통 흔들림과 G02 안의 여러 balloon pose는 동일 연속 동작의 **action phase** 후보이지 frame당 컷이 아니다. 카메라와 캐릭터 motion을 분리해 판단할 continuous playback은 하지 않았다.


## 자산, 인물, 운동/카메라, 그래픽
- **캐릭터:** 주황·검정 inflatable/air-dancer-like 세로 원통 몸체, 짧고 분할된 팔, 흰 종이줄기/술 장식 머리, 종이 원형 눈과 검정 동공. 장면마다 torso seam, inflated softness, arms의 휘어짐·관성 흔들림이 보임. 정체/캐릭터명 없음. 후반에는 분홍 로고 캡·검은 sunglasses·blue flower shirt로 분장한 제품 진열형 캐릭터가 나온다. 표정 감정/의도는 색·팔동작에서 읽힌다는 해석으로만 둔다.
- **인물/관계:** t17 앞 쇼핑객 둘: 줄무늬 초록 티와 분홍 캡·베이지 바지 남성으로 보이는 사람; 민트색 티셔츠·비니 같은 회색 모자·데님을 입은 사람. 검정/주황 손잡이 쇼핑백 들고 상점 출입구에 서 있다. 정체·관계·나이·구매행동 확인 불가. 캐릭터가 손을 든 것은 인사처럼 보이나 방향만 관찰한다.
- **제품/혜택:** 특정 SKU hero shot은 없음. sale offer, Musinsa wordmark/점포 facade, 오렌지 shopping bag, `UP TO 80%`/endcard `최대 80%` type이 촉진 자산. 몸체의 `UP TO 80%`와 endcard `역대급 할인 최대 80%`가 모두 최대 80%로 읽히나 조건·품목 범위는 영상에 설명되지 않는다. 날짜는 2026.06.14–06.24로 읽힘. 실제 세일 유효성/범위 외부 검증 안 함.
- **구도:** sky-only character medium/close → 상점 외벽을 채우는 crowd-scale low angle → 숫자/text body macro → 실제 bag/쇼퍼 scale → 평면 오렌지 endcard → 스타일된 character portrait. 낮은 시점은 키 큰 인플레이터블 크기와 건물 facade를 과장할 수 있으며, t9–12에 하늘/유리창 평행선이 보인다. 실제 focal length, camera elevation, movement/rig 수치는 알 수 없다.
- **색·재질·광:** 하늘의 연한 파랑/밝은 회색, 흰 점포 facade·유리 반사, orange mascot/매장 bag/sale backgrounds; 검정 tubes·검정 handstyle로 값 대비. inflatable 표면의 세로 seam/주름/연질광택, 종이 술, 유리 facade, 아스팔트/점포 바닥이 보임. daylight 비교적 밝고 명료하며, graphic endcard는 opaque orange flat.
- **텍스트/고지/CTA:** 우상단 흰 `MUSINSA`; 좌하단 AI 광고제/수상 오렌지 badge; 우하단 `AI로 생성`; 큰 질문형 `그냥 지나칠 거야?`; 인형 몸체 `UP TO 80% / 역대급 세일` + `무진장 블프 5주년 기념`; 쇼핑백/세일 그래픽; 마스코트 옆 `미안해질 만큼 싸다`; endcard `26 Summer Black Friday / 역대급 할인 최대 80% / dates`; final centered MUSINSA wordmark. 할인 문구는 화면에 보이는 주장일 뿐 실제 조건/사실 인증이 아니다. 음성이나 음악이 이 질문/카피를 반복하는지는 미청취 상태.

## 컷과 액션 구분 / craft reasoning
- 시트 C02/03/04/05는 서로 다른 환경/스케일/재료로 교체되는 후보; 각 candidate time은 원본 프레임 PTS지만 candidate detector만으로 컷 프레임을 지정하지 않는다. 첫 0–8.9s 여러 포즈, 9–15s 여러 인플레이터블 집단 동작, 20–22s 마스코트 팔·머리 움직임은 action phase를 관찰한 것이고 프레임별 컷으로 계산하지 않았다.
- C01 (8.967s) 하늘 주황 단독 마스코트에서 점포·공동 마스코트로 공간을 넓혀 브랜드/place를 reveal. C02 숫자/torso close detail이 promo attribute/discount prominence를 키운 후 C03 shopper proof로 사회적 사용/스케일을 다시 붙인다. 이 구성은 혜택을 읽게 하지만 할인 조건을 대체하지 않는다.
- G01의 질문 텍스트는 캐릭터 팔 동작을 만나기 전에 브랜드/상황보다 시청자 선택에 직접 질문. G02의 건물 저각 컷은 추상 하늘 mascot을 매장과 연결. G03의 다수 배경/색상 mascot은 ‘놓치지 마라’라는 retail spectacle; C04 bag macro는 그 이벤트의 상품성/상징 소품. G05 final-sale typographic hierarchy는 카메라 영상에 비해 offer와 날짜를 독해하기 쉽도록 배치.
- 대안 읽기: 마스코트는 판매상품이 아니라 특가를 축하하는 매장 주변 설치/시각 효과일 수 있음. shopper shots는 구매 증언이 아닌 연출 이미지. 터무니없는 인플레이터블 춤은 브랜드 감정/관심환기 목적일 뿐 정확한 가격 신뢰를 생성하지 않는다.

## DESIGN_PROPOSAL — 무생물 매체/캐릭터를 할인 copy의 물리적 지지체로
조건: 적법하게 새로 제작·사용할 수 있는 mascots/brand art, 매장/상품 권한, 가격/기간 조건 검증이 필수. (1) 단순한 단색 sky/벽에서 캐릭터 silhouette+질문 한 줄 소개, (2) 인물·배경을 함께 보여 주는 넓은 store context로 스케일 드롭, (3) 제품 근거/offer 숫자를 캐릭터 몸이나 환경 표면에 ‘붙이는’ 은유 컷을 쓰되 정확한 수치는 승인자료에서 잠금, (4) shopper/제품 관계를 진실된 증거만으로 연결, (5) high-contrast endcard에서 행사·날짜·조건·다음 행동/URL·브랜드를 명확히 잠깐 고정. 상대시간 변수는 인형 pose/질문 순서, offer read-time, image-to-copy 전환, end-hold; %와 실매장 가격 자료는 창작 자유 변수 아님. 여기 나온 orange/black/wind-dancer/문구/브러시 로고/캐릭터 얼굴을 복제하지 않고 완전히 신규 시각시스템을 만든다.

## Observable QA
- 루프 가능한 mascot motion: 길쭉한 관절·팔/흰 술·눈 위치가 프레임 변화 중 유지되고 seam/공기압에 따른 변형이 관절 없는 몸의 종류와 일관한지 확인. 하늘에서 점포 facade로 cut할 때 인형 크기/방향은 새 shot으로 조정; portal/morph를 택한다면 눈·머리·몸체 continuity를 별도 평가.
- 숫자/copy: 인형 몸체와 endcard의 `UP TO 80%` / `최대 80%`를 정확히 분리·재확인하고, 실제 조건·대상 SKU·날짜를 독립 자료로 검증한다. Smartphone crop에서 숫자·브랜드·날짜 모두 읽히는 대비/안전영역/홀드를 시험.
- 인형 겹침이 모델/머리/핵심 세일 숫자나 쇼핑백을 덮지 않게 eye-trace 확인. `그냥 지나칠 거야?`가 질문하는 대상과 후속 action이 명확한지 사용성 QA.
- 실사 storefront, 화면 AI 생성 표식, 거대 inflation/날짜 claim, awards badge가 실제 계약/허가/할인 유효성을 보증하지 않음을 분리. 신청/구매 버튼·URL이 필요하면 실제 endpoint 제공.
- 미확인: 연속 playback, soundtrack/VO/SFX, 촬영/CGI 방법, 캐릭터의 이름/기능, 할인 조건·SKU, 공식 캠페인 인가/성과. 화면의 AI label은 사실 확인 대체물이 아니다.
