# CINEMATIC_DIRECTING_BIBLE v1.0 반영 설계

상태: 구현 완료 2026-11-18 (package 2.56) · 결정: 음향 표는 `edit-sound-language-catalog.md`에 합침 · P0–P4 한 번에 진행

## 1. 대상과 성격

입력 문서: `/home/declan/Downloads/CINEMATIC_DIRECTING_BIBLE_v1.md`, v1.0, 2026-11-18, 39,052 bytes, SHA-256 `b2eceb86088ec17d4b65361a55d00c7ad5b39db3294de367d132690efb95e91b`, 459줄.

성격 판정: **사용자 작성 프로젝트 분류 체계**(문서 스스로 "공인된 30대 분류를 주장하지 않는다"고 밝힘). 영화사·기법 효과에 대한 외부 검증 자료가 아니므로 `sources.md`의 서적 근거로 승격하지 않는다. 판정 근거는 이 문서의 자기 진술과, 각 항목이 이미 패키지 정본에 더 엄격한 형태로 존재하는지의 대조다.

## 2. 적용 원칙

1. **정본 소유자 유지.** 기법 정의는 이미 소유 문서가 있다(카메라=`camera-language-catalog`, 편집·음향=`edit-sound-language-catalog`, 애니메이션=`08-animation`, 후반=`23-finishing-platform`, QA=`12`/`21`/`27`). 문서를 통째로 새 스킬로 옮기면 같은 의미가 두 곳에 생긴다. **새 정의는 만들지 않고, 없는 분기만 소유 문서에 넣는다.**
2. **부르는 이름만 이관.** 사용자가 `ST-01`, "impact frame", "leitmotif"처럼 문서 용어로 요청할 때 정본을 찾을 수 있어야 한다. 이를 위해 ID 범위→소유 파일/앵커를 잇는 **크로스워크 한 장**만 추가한다(§5).
3. **수치는 후보로만.** 문서의 "1~3프레임", "0.25초=6프레임" 같은 값은 검증된 권장치가 아니다. 예시로 옮길 때 예시 라벨·계산 근거·미검증 표시를 붙인다.
4. **이미 있는 것은 옮기지 않는다.** 중복 서술은 유지비와 prominence를 동시에 올린다. 이미 더 엄격한 문서가 있으면 크로스워크에 포인터만 둔다.

## 3. 30범주 갭 판정

판정: **충족**(기존 정본이 동등 이상) / **용어 신규**(개념은 있으나 선택 가능한 이름·인계 조건이 없음) / **신규** / **거부**(중복·스키마 충돌).

| # | 범주 | 기존 정본(파일·절) | 판정 |
|---|---|---|---|
| 01 | Narrative Pacing | `09-edit` 시퀀스 리듬 계약 + 속도 대비 곡선 | 충족(NP-04는 이번에 추가됨) |
| 02 | Rhythmic Editing | `edit-sound-language-catalog`, `09-edit` 비트 기준 | 충족(RE-03은 이번에 추가됨) |
| 03 | Speed & Time | `camera-language-catalog` B13–16 + 이번 속도·타격 표(편집 인계) | 충족(ST-06→`08`) |
| 04 | Timing & Spacing | `08-animation` 실행 절차 + 모션 속도·타격 기법 | 충족(AT-04/06 이번에 추가됨) |
| 05 | Camera Movement | `camera-language-catalog` A/B | 충족(CM-04=줌 인 B04) |
| 06 | Action Choreography | `21` §1, `26-state-causality-continuity`, `storyboard-contract` | 충족 |
| 07 | Visual Effects | `21` §2 레이어 스택, `23` Texture, `12`/`21` QA | 충족(VX-05→`07`, VX-06→`23` 할레이션/블룸) |
| 08 | Sound Design | `edit-sound-language-catalog` Foley/앰비언스/음악 행 | **용어 신규 5** — layered impact, whoosh, riser, sound bridge, transient |
| 09 | Composition & Continuity | `camera-language-catalog` A, `06-shots`, `26` | 충족 |
| 10 | AI Animatic | I2V 체이닝·`ai-camera-control`·`21` §2 | **신규 3** — 2.5D parallax, Ken Burns, interpolation 아티팩트 |
| 11 | Acting & Performance | `04-performance`, `expression_pose`, 반응 지연 | 충족 |
| 12 | Mise-en-scène | `camera-language-catalog` A24 여백·A23 중앙·A08 인서트, `visual-scene-communication` | **부분 신규 1** — 전경 프레이밍(문틈·난간 너머) |
| 13 | Cinematography & Optics | `camera-language-catalog`, `05-visual`, `21` §2 매칭 | 충족 |
| 14 | Lighting | `lighting-language-catalog`, `07-lighting` | 충족 |
| 15 | Color Grading | `23` §1 의존 순서·노드 역할 | 충족(문서보다 엄격) |
| 16 | Physical Realism | `08`, `21` §1, `26`, QC-05 | 충족 |
| 17 | Emotional Direction | `16-concept-emotion-retention`, `04`, `09` release | 충족 |
| 18 | Advanced Film Grammar | `06`/`09`/`26`, `storyboard-contract` 정보 공개 | 충족 |
| 19 | Temporal Consistency | `26`, `21` 정체성/시간 패스, `character-ssot` | 충족 |
| 20 | Post Pipeline | `23`, `28`, `09` 후반 단계 추적 | 충족 |
| 21 | Shot Coverage | `06-shots` 커버리지, `camera-language-catalog` A | 충족 |
| 22 | Eye Trace & Perception | `storyboarding-video` narrative-panels eye trace, `21` 판독 | 충족 |
| 23 | Visual Storytelling | `visual-scene-communication`, `silent-visual-storytelling` | 충족 |
| 24 | Production Design | `05` 장소 마스터, `26` 연속성 원장, 소품 SSOT | 충족 |
| 25 | Music Dramaturgy | `09` 음악 기준점(힛포인트 일부) | **용어 신규 4** — leitmotif, ostinato, 대조 음악, 음악적 침묵 배치 |
| 26 | Spatial Audio | `09` mix_note 청취 관점·좌우/거리/잔향 | **용어 신규 4** — 거리 감쇠, 초기 반사, 차폐, 주관 먹먹함 |
| 27 | Editorial Transitions | `camera-language-catalog` B17–24 + 편집 카탈로그 | 충족 |
| 28 | Scene Objectives | `02-story` 욕망/결핍/아크, `16` | 충족 |
| 29 | Visual Quality Control | `12`, `21` §3 검사 패스, `27` | 충족 |
| 30 | Distribution & Accessibility | `15-delivery` WCAG·자막·안전영역, `23` §1 | **부분 신규 1** — 광과민·흔들림 편안함 검사 |

합계: 충족 23, 용어·부분 신규 6, 신규 1(IA), 거부 3(§6).

## 4. 반영 설계 (파일 단위)

### 4.1 음향·음악 용어 — `video-production-assets/references/edit-sound-language-catalog.md`

이미 "컷·전환·음향 표현 선택표" 소유자다. 세 표를 추가하고, 열 구조는 기존 표와 동일하게 `표현 | 선택 조건/필요 자료 | 실패 조건·실제 검수 | 기존 인계 칸`을 쓴다. 인계 칸은 `sound-cues.csv`의 실제 열(`layer`, `function`, `sync_anchor`, `sync_offset_s`, `gain_db`, `mix_note`, `rights_status`)만 가리킨다.

- **효과음 설계**: Layered impact(저음+접촉+파편의 층 분리), Whoosh(이동 방향·근접도), Riser(공개 직전 상승), Pre-impact silence(정점 직전 무음과 앰비언스 최소화 구분), Sound bridge(다음 장면 소리 선행 = J컷과 소유 구분), Transient design(어택 선명도와 피로 한계).
- **음악 설계**: Leitmotif, Ostinato, Musical hit point(기존 09 기준점 사용), Musical counterpoint. `09`의 "음악·효과음 소싱과 권리"와 "비트 기반 편집" 절이 정본임을 명시하고 여기서는 선택 조건만 다룬다.
- **공간 음향**: Distance attenuation, Early reflection, Occlusion, Pan automation, Subjective muffle. `09`의 청취 관점·좌우 유지 규칙이 정본이며, 실제 채널 청취 없이는 미검증임을 표 머리에서 반복한다.

합계 약 15행. 행마다 "이 목록 자체가 검증된 recipe가 아니다"를 표 머리에 1회만 적는다(행마다 반복 금지).

### 4.2 스틸 모션 — `storytelling-with-still-images/SKILL.md`

IA-01/02/06의 소유자가 지금 없다. 정지 이미지 조립을 소유한 이 스킬에 compact 절을 추가한다.

- 2.5D parallax: 레이어 분리·가장자리 채움 필요, 실패=분리 경계 틈·잘린 팔.
- Ken Burns: 같은 줌·이동 반복 금지, 실패=모든 컷 동일 방향·과도한 크롭으로 정보 손실.
- Interpolation: 보간 아티팩트가 손·머리카락·가림에서 생김, 실패=보간 결과를 원본 모션으로 표기.
- 공통: 스틸 모션은 **계획·검수 대상이며 이동 속도 측정이 아니다**. 타이밍은 `animatic-direction` 소유.

### 4.3 전경 프레이밍 — `camera-spatial-design/references/camera-language-catalog.md`

A13–18 인접에 "전경 오버레이/문틈 프레이밍" 1행 추가(형태·은폐/감시 기능·주인공 행동 가림 금지·전경 초점/노출 분리). 새 ID를 만들지 않고 기존 A 절 서술 규칙을 따른다. ID 체계를 늘리면 카탈로그 참조가 깨진다(§6).

### 4.4 광과민·편안함 — `video-production-assets/references/15-delivery.md`

DA-06/VX-05를 납품 검사 항목 1줄로 넣는다: 섬광·연속 플래시·지속 흔들림·급격 줌이 포함되면 실제 출력에서 빈도·지속을 확인하고, 의도된 연출과 편안함 위험을 분리해 기록. 임계 수치·보편 기준은 발명하지 않고 목적지 규격/승인 기준이 있을 때만 적용. `21` §3 시간 패스에는 "플리커"가 이미 있으므로 중복 서술하지 않고 15에서 21로 포인터.

### 4.5 숨기지 않기 가드레일 — `edit-sound-language-catalog.md` 속도·타격 표 머리

`23`이 그레인·블룸·암부로 결함을 가리는 것을 이미 금지한다. 같은 규칙의 속도 버전을 1문장 추가: **공간·해부·접촉 결함은 속도 램프·모션 블러·충격 프레임·카메라 흔들림으로 가리지 않는다. 가려야 할 결함이면 소스를 수리하거나 컷을 바꾼다.**

### 4.6 타이밍 검산 예시 — `08-animation.md` (선택)

문서의 1차원 슬라이드 예(0.25초·24fps·6노출프레임, `x=90(3u²-2u³)`, 끝 경계 f=6은 추가 노출 아님)를 **선택 예시**로 3–5줄 추가한다. 목적: "계산으로 스페이싱을 검산하되 물리·무게·영상 생성은 NOT_RUN"이라는 기존 태도를 구체화. 고정 24fps 권장으로 읽히지 않도록 예시 라벨을 붙인다.

## 5. 크로스워크 파일

신규: `video-production-assets/references/directing-vocabulary-crosswalk.md` (범주 30행 + 장르 레시피 6행 + 거부 5행).

- 머리: 입력 문서 identity(경로·버전·해시·성격), "정의를 복제하지 않는다", "ID는 조회용이며 패키지 스키마가 아니다".
- 표 열: `문서 ID 범위 | 문서 용어 | 정본 파일·앵커 | 이 패키지에서의 상태(충족/신규 이관/거부) | 주의`.
- 30행 + 장르 레시피 6행(§6) + 템플릿 1행(§6).
- 배치 근거: 사용자가 문서 용어로 요청할 때 검색 비용을 줄이는 **포인터 전용** 문서다. 정의·수치·검수 기준을 담지 않으므로 정본과 충돌하지 않는다.
- `production-reference-index.md`의 "선택 → 인계 → 검수" 절에 이 파일을 1회 연결한다(진입점 1개).

## 6. 거부 목록과 이유

| 문서 요소 | 판정 | 이유/대체 |
|---|---|---|
| 30범주 ID 체계 자체 | 거부(스키마) | 새 분류 스키마는 기존 owner·필드와 이중 체계를 만든다. 크로스워크 조회용으로만 유지 |
| 샷 지시서 YAML | 거부(중복) | `06`/`08` 템플릿, `project.json`, `11` 핸드오프가 이미 정본. 다른 스키마를 추가하면 필드 의미가 갈린다 |
| 장르 조합 레시피 6종 | 거부(중복) | 구성 ID는 `camera-language-catalog`(액션·추격·충격), `performance-and-style-recipes`, `silent-satire-animatic`에 이미 있음. 크로스워크에서 대응만 표기 |
| 고정 프레임·초 수치 | 후보로만 | 검증된 권장치 아님. 예시 라벨·계산 근거 필수 |
| "G1–G7 승인 게이트" | 거부(중복) | `12-qa`·`asset_gate`·`21` 검사 순서가 더 엄격. 게이트 이름만 크로스워크 주의 열에 병기 |
| 그레이딩·납품·후반 규칙 | 거부(중복) | `23`/`15`/`28`이 이미 상세·검증 절차 보유 |

## 7. 실행 순서와 검증

1. **P0** 크로스워크 골격 + 머리(provenance) — 먼저 넣어 이후 편집의 색인을 만든다.
2. **P1** 음향·음악·공간음향 표(4.1), 가드레일 문장(4.5).
3. **P2** 스틸 모션(4.2), 전경 프레이밍(4.3).
4. **P3** 광과민 검사(4.4), 타이밍 검산 예시(4.6).
5. **P4** 버전·이력: `manifest` 2.56, `CHANGELOG` 항목, `video-production-assets`·`storytelling-with-still-images`·`camera-spatial-design`·`animatic-direction` 중 실제 수정된 스킬만 minor bump.

검증:

- 크로스워크의 모든 `파일#앵커`가 실제로 해석되는지 검사하는 테스트 추가(`scripts/test_crosswalk_navigation.py`, `test_visual_recipe_navigation.py` 패턴: 파일 존재 + 헤딩 slug 대조 + 깨진 사본 검출).
- `python3 -m pytest -q` 전체, `python3 scripts/check_versions.py`.
- 단일 출처 확인: 새로 넣은 용어가 정본 1곳에만 정의되고 크로스워크에는 포인터만 있는지 grep으로 확인.
- 없는 필드·수치 부재 확인: 새 표가 `sound-cues.csv`/`06`/`08`/`09` 기존 열 이름만 참조하는지 육안+테스트.

## 8. 비용·위험

- 분량: 표 약 15행 + 문장 6개 + 문서 1장. 기존 참조 문서 증가폭은 작고, SKILL.md 본문은 늘리지 않는다(컨텍스트 부하 최소화).
- 위험 1: 음향 표가 `09`의 권리·믹스 절차를 다시 쓰는 방향으로 비대해질 수 있음 → 표는 선택 조건/실패 조건/인계 칸만, 절차는 포인터.
- 위험 2: 스틸 모션이 `animatic-direction`과 소유권이 겹칠 수 있음 → 모션 메커니즘은 10(스틸), 시간 배분은 `animatic-direction`으로 명시 분리.
- 위험 3: 크로스워크가 낡으면 잘못된 포인터가 된다 → 테스트로 앵커 소실을 CI에서 잡는다.

## 9. 결정 결과

1. 음향·음악·공간음향 표는 **`edit-sound-language-catalog.md`에 합쳤다**(오너 1곳 유지).
2. P0–P4를 **한 번에** 실행했다.

구현 결과와 검증은 2.56 `CHANGELOG.md` 항목과 `scripts/test_crosswalk_navigation.py`(30범주 행 수·모든 파일+앵커 해석·손상 사본 검출)에 있다. 설계에서 벗어난 점은 없다. 다만 크로스워크 작성 중 경로가 `../references/`로 잘못 적힌 9곳을 발견해 상대 경로로 고쳤고, 이 검사가 그런 종류의 오류를 잡는 테스트다.
