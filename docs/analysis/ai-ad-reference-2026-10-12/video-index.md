# AI 광고 레퍼런스 — 전체 영상 근거 색인

## 먼저 읽기
- [분석 방법](analysis-method.md): OBSERVED / ESTIMATED / INTERPRETATION / DESIGN_PROPOSAL / UNKNOWN 및 frame-only, PTS, cut/scene/action-phase 경계.
- [기계 생성 원본 인벤토리](video-inventory.json): 48개 파일·stable `archive_id` SHA-256·파일명/크기·probe/full-decode·검출 후보 타임스탬프. `V###`는 정렬 순번 표시 ID일 뿐이다.
- [설계 제안](DESIGN.md): 저장소 조항에 근거한 48편 교차표, 다원인 craft recipes, 우선순위·제안된 handoff/QA; 기존 skill 변경 없음.
- [fast worker 30개 source gap evidence](gap-evidence-fast.md): 소스별 mechanism→실제 capability clause→classification→recipe controls/handoff/failure-QA 표.
- [첫 24개 raw-event pass](raw-candidate-review-findings.md), [event/frame/PTS JSON](raw-candidate-coverage-first24.json): V001–V024의 496 R-event 실제 native n−2/n/n+2 frame 리뷰.
- [독립 preflight findings](qa-findings-preflight.md): 수정·보류 이슈의 evidence locator.
- Provenance/책: [creator metadata/caption notes](creator-provenance-notes.md), [web citation ledger](web-citations-ledger.json), [book source notes](book-source-notes.md), [source register](source-register.json), [repo capability audit](repo-capability-audit.md).

## 기계·시각 coverage 상태
- 재귀 탐색으로 원본 MP4 48개 발견. ffprobe 48/48, full FFmpeg decode 48/48 rc=0. 전체 1,035 detector event는 raw candidate이지 verified cuts가 아니다.
- 모든 48개 source chapter는 FRAMES_REVIEWED 상태로 화면 관찰을 기록한다. raw-candidate neighborhoods를 native-frame 주변 시점으로 검토했지만 n±2는 연속 재생/중간 프레임 전수/모든 boundary를 입증하지 않는다. V001–V024 raw supplement는 496 events / 1,468 unique native frames / 71 strips; 여섯 source의 별도 보충 pass는 337 review-display / 58 source·candidate sheets이며 unique frame count에 더하지 않는다. V025–V048 second-half raw-event review 539건은 source별 chapter/evidence와 연결한다. 모든 수치는 coverage 단위이며 shots/scenes/cuts로 전용하지 않는다.
- Continuous playback: 0. Human audio listening: 0. AAC 존재만으로 VO/music/SFX를 쓰지 않는다. 실제 실행된 ASR는 unverified hypothesis, 자동 자막은 CAPTION_TEXT_AUTO_UNTIMED로 표시한다. 파일 description/source claim과 화면에서 직접 읽은 사실은 각각 분리한다.
- 모든 영상별 가시적 구간·시각·단위·불확실성·마지막 화면 범위는 각각 chapter에 기록하며, 해당 chapter의 SHA/PTS/evidence가 inventory stable ID에 연결된다. Full cut certification을 주장하지 않는다.

## V001–V048 영상별 evidence chapter

| 표시 ID | Chapter / analysis scope | 표기 |
|---|---|---|
| V001 | [수영장 리조트 패션 montage](videos/V001-summer-resort-gucci-style-ad.md) | FRAMES_REVIEWED |
| V002 | [IM8 surreal product / persuasion montage](videos/V002-im8-surreal-product-film.md) | FRAMES_REVIEWED |
| V003 | [Vans skatepark / trick / puddle / moving type](videos/V003-vans-skateboarding-film.md) | FRAMES_REVIEWED |
| V004 | [nested alcohol-media counter-ad / white end slate](videos/V004-after-work-beer-counter-ad.md) | FRAMES_REVIEWED |
| V005 | [FRUSH burger/brand visual evidence](videos/V005-visual-evidence.md) | FRAMES_REVIEWED |
| V006 | [rain-boot hidden-purchase reveal](videos/V006-musinsa-rain-boot-male-secret.md) | FRAMES_REVIEWED |
| V007 | [inflatable mascot / discount endcards](videos/V007-musinsa-inflatables-summer-sale.md) | FRAMES_REVIEWED |
| V008 | [summer Santa / gift / cockpit allegory / coda](videos/V008-santa-revolt.md) | FRAMES_REVIEWED |
| V009 | [blue shoreline running montage / logo](videos/V009-adidas-beyond-the-blue.md) | FRAMES_REVIEWED |
| V010 | [Dior perfume spec / model–bottle–rose cycles](videos/V010-dior-perfume-spec-ad.md) | FRAMES_REVIEWED |
| V011 | [AI burger ingredient / creator slate](videos/V011-ai-burger-commercial.md) | FRAMES_REVIEWED |
| V012 | [Ferrari forest / driver / animal / car](videos/V012-ferrari-spec-commercial.md) | FRAMES_REVIEWED |
| V013 | [cloud/vehicle spatial visual evidence](videos/V013-visual-evidence.md) | FRAMES_REVIEWED |
| V014 | [shoe / beam / weather visual evidence](videos/V014-visual-evidence.md) | FRAMES_REVIEWED |
| V015 | [firelit social scene / blue package reveal](videos/V015-ai-generated-beer-commercial.md) | FRAMES_REVIEWED |
| V016 | [Range Rover car / water / finish visual evidence](videos/V016-visual-evidence.md) | FRAMES_REVIEWED |
| V017 | [Lincoln dune burial and reveal](videos/V017-lincoln-dune-spec-ad.md) | FRAMES_REVIEWED |
| V018 | [Ferrari / surfer / wave / horsepower metaphor](videos/V018-ferrari-augmentables-spec.md) | FRAMES_REVIEWED |
| V019 | [Adidas coffee-break fashion / shoes](videos/V019-adidas-coffee-break-spec-ad.md) | FRAMES_REVIEWED |
| V020 | [웅진씽크빅 learning montage / AI thesis](videos/V020-woongjin-thinkbig-branding.md) | FRAMES_REVIEWED |
| V021 | [tomato journey / food-misdirection / adult punchline](videos/V021-tomato-unexpected-ai-commercial.md) | FRAMES_REVIEWED |
| V022 | [Audi toy-to-adult / portal / type reframe](videos/V022-audi-big-boy-fake-ad.md) | FRAMES_REVIEWED |
| V023 | [restaurant food assembly visual evidence](videos/V023-visual-evidence.md) | FRAMES_REVIEWED |
| V024 | [cola/burger / creator-disclosure tail](videos/V024-visual-evidence.md) | FRAMES_REVIEWED |
| V025 | [vehicle image repair / creator claim](videos/V025-visual-evidence.md) | FRAMES_REVIEWED |
| V026 | [Oreo brand visual evidence](videos/V026-visual-evidence.md) | FRAMES_REVIEWED |
| V027 | [fictional resort / luxury-hotel visual evidence](videos/V027-visual-evidence.md) | FRAMES_REVIEWED |
| V028 | [IKEA continuous room-build / disclaimer](videos/V028-ikea-open-it-live-it.md) | FRAMES_REVIEWED |
| V029 | [KFC visual evidence](videos/V029-visual-evidence.md) | FRAMES_REVIEWED |
| V030 | [Lamborghini visual evidence](videos/V030-visual-evidence.md) | FRAMES_REVIEWED |
| V031 | [Nike pool remaster / source distinction](videos/V031-visual-evidence.md) | FRAMES_REVIEWED |
| V032 | [oceanfront lifestyle proxy—not floorplan proof](videos/V032-visual-evidence.md) | FRAMES_REVIEWED |
| V033 | [fashion montage visual evidence](videos/V033-visual-evidence.md) | FRAMES_REVIEWED |
| V034 | [McDonald's visual evidence](videos/V034-visual-evidence.md) | FRAMES_REVIEWED |
| V035 | [Mountain Dew / declared voice and music credits](videos/V035-visual-evidence.md) | FRAMES_REVIEWED |
| V036 | [Plum Delight / blossom-to-bottle visual evidence](videos/V036-visual-evidence.md) | FRAMES_REVIEWED |
| V037 | [Porsche visual evidence](videos/V037-visual-evidence.md) | FRAMES_REVIEWED |
| V038 | [PURE EDGE Sephora spec / visual evidence](videos/V038-visual-evidence.md) | FRAMES_REVIEWED |
| V039 | [headphone product visual evidence](videos/V039-visual-evidence.md) | FRAMES_REVIEWED |
| V040 | [Tesla Cybertruck visual evidence](videos/V040-visual-evidence.md) | FRAMES_REVIEWED |
| V041 | [Liquid Death gag / visual evidence](videos/V041-visual-evidence.md) | FRAMES_REVIEWED |
| V042 | [Nike float-or-swim visual evidence](videos/V042-visual-evidence.md) | FRAMES_REVIEWED |
| V043 | [Nike portal / POV gaming-hand sequence](videos/V043-visual-evidence.md) | FRAMES_REVIEWED |
| V044 | [Volvo / declared post-edit workflow](videos/V044-visual-evidence.md) | FRAMES_REVIEWED |
| V045 | [Zara fashion visual evidence](videos/V045-visual-evidence.md) | FRAMES_REVIEWED |
| V046 | [wedding-platform AI visual evidence](videos/V046-visual-evidence.md) | FRAMES_REVIEWED |
| V047 | [Osulloc tea visual evidence](videos/V047-visual-evidence.md) | FRAMES_REVIEWED |
| V048 | [Adidas Floral visual evidence](videos/V048-visual-evidence.md) | FRAMES_REVIEWED |

## Reader handoff
먼저 [DESIGN.md](DESIGN.md)를 읽는다. V001–V024 장별 분석과 추가 30편의 근거표는 각각 기존 역량 조항, recipe 제어값, 불확실성, QA로 연결된다. [reader-transfer.md](reader-transfer.md)는 장의 source ID를 프로젝트 ID로 바꾸지 않고 기존 skill을 수정하지 않으면서 근거를 새 브리프에 적용하는 방법을 설명한다.
