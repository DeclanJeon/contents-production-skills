# 비주얼 모드·SSOT 티어·연속성 (온디맨드 심화)

모듈 05(시각 구조), 11(AI 인계), 14(에셋 운영)의 심화. 반복 인물/제품/세계가 여러 샷·회차·생성에 걸쳐 정체성을 유지해야 할 때 연다. 사용자가 제공한 SSOT·바이블은 authoritative로 보존하고, 빈 필드는 명시적 창작 위임이 있을 때만 `proposal` 라벨로 채운다 — 실존 인물의 문서화되지 않은 사실은 추론으로 만들지 않는다.

## 1. 비주얼 모드 선택

캐릭터 시트·제작 이미지 생성 전에 표현 체계를 정한다. 스타일은 장식이 아니라 SSOT 요구·모션 기대·조명·질감·카메라 언어·모델 라우팅을 바꾼다.

1. 브리프·레퍼런스·플랫폼·장르·반복/예산 여유·정체성 연속성 요구를 읽는다.
2. 사용자의 명시 선택은 authoritative다.
3. 미지정이면 브리프에 맞는 서로 다른 표현 방향과 추천 이유를 제시한다. 후보 수는 요청과 필요한 비교 폭으로 정한다. 중요한 방향은 사용자 수락 또는 명시적 창작 위임 뒤에 잠그며, 위임받은 경우 선택 이유를 기록해 계속한다. 정지/영상 생성 승인은 별도다.
4. 비주얼 모드 ID를 잠그고 시각 규칙(룩 바이블)에 기록한다.
5. 렌더링 차원을 정의한다: 표현(실사/스타일라이즈드 실사/2D/3D/스톱모션/일러스트/혼합)·리얼리즘 수준·인물 비율·재질/질감 논리·조명 논리·렌즈/카메라 리얼리즘·모션 리얼리즘·색 체계·선/렌더 처리.
6. 이미지 생성·영상 생성·피니싱 전 구간에서 유지해야 할 것을 정한다.
7. 모드별 SSOT 요구는 아래 참조 팩 표, 생성 요구는 [프로덕션 실행·비용 라우팅](24-production-execution.md)으로 보낸다.

### 선택 메뉴 (선택이 유용할 때)

- A. 실사 — 믿을 수 있는 피부·광학·재질·물리 조명.
- B. 스타일라이즈드 실사 — 사실적 해부 + 의도적 아트 디렉션.
- C. 2D 애니메이션 — 그래픽 형태·선/색 일관성·포즈 가독성.
- D. 3D 애니메이션 — 안정된 볼륨·재질·모델 시트 턴어라운드·통제 조명.
- E. 스톱모션/미니어처 — 촉각 재질·수제 불완전성·연출 조명.
- F. 일러스트/그림책 — 회화적·그래픽적 정지 이미지 우선 서사.
- G. 하이브리드 — 어떤 레이어가 어떤 표현을 쓰는지 명시 정의.
- AUTO — 레퍼런스와 콘텐츠 목표에서 추론.

### 모드별 고정 후보 (브리프에서 채택한 속성만 잠금)

- 실사: 정체성 충실도·피부/머리카락·의상 재질·렌즈 거동·물리적 조명·표정 참조. 중립 정체성 참조에 극단적 그레이딩을 입히지 않는다.
- 스타일라이즈드 실사: 해부 과장·얼굴 비율·질감 선명도·팔레트·스타일화 강도를 잠근다. 샷마다 일반 실사나 카툰으로 표류하지 않게 한다.
- 2D: 모델 시트 비율·실루엣·선 굵기·팔레트·명암 단순화·눈/입 구조·포즈 언어를 검토한다. 필요한 시점/포즈 재현에는 턴어라운드와 표정 참조를 사용할 수 있다(아래 Culhane). 실사 질감과의 보편 우위는 없으며 질감이 핵심인 2D 브리프도 보존한다.
- 3D: 볼륨·재질 반응·표면 거칠기/반사·헤어/털 처리·리그 친화 비율·중립 스튜디오 조명. 앞/옆/뒤/3/4 뷰가 중요하다.
- 스톱모션/미니어처: 재질 스케일 단서·수제 표면·미니어처 심도 논리·실물 조명 느낌·프레임 간 촉각 일관성.
- 일러스트: 붓/선 처리·형태 언어·팔레트·원근 단순화·반복 모티프 처리. 모션 생성은 통제된 image-first 워크플로가 필요할 수 있다.
- 하이브리드: 레이어/시퀀스마다 표현 모드와 전환 규칙을 선언한다. 모델 표류로 우발적 혼합을 만들지 않는다.

규칙: 생존 작가 이름만으로 스타일을 지정하지 말고 시각 속성으로 기술한다. 레퍼런스 영상은 페이싱·카메라 문법만 제공하고 같은 렌더링 스타일을 강제하지 않는다.

## 2. 캐릭터 SSOT 티어

연속성을 지킬 만큼만 SSOT를 만들고 그 이상은 만들지 않는다.

- Tier A — Full SSOT: 주인공·반복 리드·반복 적대자·반복 연애 상대·시그니처 마스코트·여러 씬/회차의 정체성 핵심 인물.
- Tier B — Lite SSOT: 여러 샷에 정체성이 필요한 명명된 조연·단일 회차 인물.
- Tier C — 아키타입 엑스트라: 고유 SSOT 대신 재사용 캐스팅 카드(궁중 시녀·직장인·마을 사람·파티 손님).
- Tier D — 군중 규칙: 개인 시트 없이 인구 구성·의상 범위·행동 군집·팔레트·배제 규칙을 정의한다.
- Tier별 텍스트 깊이는 같이 간다: `designing-video-character-sheets`의 전체 canonical `CHARACTER SSOT`(섹션 0–33, [`designing-video-character-sheets/references/character-ssot-master-prompt.md`](../../designing-video-character-sheets/references/character-ssot-master-prompt.md))는 Tier A와 명시적 전체 SSOT 요청에 쓰고, Tier B/C는 `assets/character-ssot-template.md`의 필요 필드만 채운다.
- **이미지 기반 전체 패키지의 필수 이미지:** 정의된 인물마다 Sheet A — 한 장의 중립 스튜디오 정체성 시트(전신 정면·3/4 전면·측면·후면 + 얼굴 정면·3/4·측면, 7뷰, 동일 인물, 중립 표정·조명, 장면 서사 없음)가 실제 파일로 필요하다. B/C/D(표정·의상·액션)는 프롬프트 스펙일 뿐 추가 생성·과금을 승인하지 않는다. 텍스트 전용/독립 작업은 파일·이미지 없이 끝난다. 글래머 초상은 실제 시트 대체가 안 된다.

### 승격 기준과 절차

1. 이야기/회차/시리즈의 캐스트 목록을 파싱한다.
2. 정체성 핵심 반복 인물을 먼저 센다.
3. 하나 이상 해당하면 Full로 승격: 회차 반복·감정 중심·즉시 재인식 필요·시그니처 의상/소품/제품 상호작용·여러 샷이 정확한 얼굴/신체 연속성에 의존.
4. 짧지만 여러 샷의 명명 역은 Lite.
5. 교환 가능한 배경 역은 아키타입/군중 규칙으로 묶는다.
6. 티어별 정확한 수와 이유를 보고한 뒤에 참조 이미지를 만든다.
7. 시리즈는 영속 레지스트리를 유지하고 새 반복 정체성이 생길 때만 SSOT를 추가한다 — `project.json`의 characters와 asset_registry를 쓰고 별도 DB를 만들지 않는다.

### 참조 팩 (샷 필요에 맞게 조정)

- Full SSOT — 실사/스타일라이즈드: 정면 중립 · 3/4 중립 · 측면(옆 샷이 있으면) · 전신 중립 · 주 의상 전신 · 서사 핵심 표정열 · 반복 소품 상호작용 · 후면(뒷모습 샷이 있으면).
- Lite SSOT — 실사/스타일라이즈드: 정면 또는 3/4 정체성 · 전신/의상 · 필요시 표정/행동 참조 1종.
- Full SSOT — 2D: 필요한 턴어라운드(앞/3/4/옆/뒤) · 전신 모델 시트 · 표정 시트 · 플롯상 중요한 손/소품 디테일 · 팔레트와 선/명암 규칙.
- Full SSOT — 3D: 앞/옆/뒤/3/4 · 전신 중립 · 재질 노트 · 표정 목표 · 중요 시 헤어/털/재질 클로즈업.
- 스톱모션/미니어처: 앞/옆/뒤 물리 형태 · 재질/질감 매크로 · 의상/소품 스케일 참조.
- 크리처/비인간: 해부도·이동 논리·스케일 참조·실루엣 불변을 추가.
- 엑스트라/군중: 개별 SSOT 대신 아키타입 보드나 군중 규칙 — 배경 인물이 서사상 중요해지면 그때 승격.

규칙: 배경 엑스트라마다 Full SSOT를 만들지 않는다. 반복 인물을 글래머 초상 하나에 의존하지 않는다. 정체성 앵커와 샷별 조명/포즈/스타일 참조를 분리한다. 실존 인물의 용모가 필요한데 쓸 이미지가 없으면 정체성 정확도를 주장하기 전에 필요한 입력을 요청한다.

### 정본 레코드 매핑 (이미지 기반 전체 패키지)

캐릭터 SSOT 출력은 정본 `project.json`에 이렇게 연결된다(조정자가 기록, 워커는 패킷으로 제안):

| 정본 필드 | 내용 |
|---|---|
| `characters[].persona` | `{role, personality, observable_behavior, speech}` — 모두 비어 있지 않은 문자열; 무언·해당 없음은 이유가 적힌 `N/A` |
| `characters[].ssot_artifact_id` | `type=character_sheet` artifact — 실제 SSOT Markdown 에셋, synopsis artifact·버전에 의존 |
| `characters[].identity_sheet_asset_id` | `mode=image_backed` 전용 — `kind=character_identity_sheet`, `entity_type=character`, `entity_id`=character_id; 인물당 실제 Sheet A 이미지 1장 |
| `preproduction` | `{mode: text|image_backed, synopsis_artifact_id, storyboard_artifact_id, storyboard_sheet_artifact_ids, storyboard_split_asset_id}` — 시트 artifact ID는 한 장도 이야기 순서 배열(시트당 최대 8패널), split pointer는 실제 장면/패널 추출 manifest asset. text는 이미지 요구가 없고 image_backed 검토·실행은 text로 우회하지 않는다 |

추적 체인은 synopsis artifact·버전·소스 locator → `character_sheet` artifact·버전 → 단일 `character_identity_sheet` 에셋 → 샷/패널 참조 입력이다. `mode=image_backed`에서 캐릭터를 이름으로 호출하는 샷은 그 인물의 정체성 이미지 에셋을 소비한다. 실제 이미지 검수는 시트의 각 뷰와 선언 앵커를 직접 비교한다 — 프롬프트가 생성된 시트를 뜻하지 않고, 공급자 성공은 정체성 QA가 아니다.

## 3. 캐릭터 연속성 운용

연속성은 프롬프트 형용사가 아니라 에셋 관리 문제다.

1. 반복 인물마다 안정된 `character_id`(CH01 형식)를 부여한다.
2. 많은 샷 생성 전에 SSOT를 만든다: `assets/character-ssot-template.md`. 불변 정체성과 씬 가변 상태를 분리한다.
   - 불변: 얼굴 비율·눈 위치·코/입 형태·피부/털 무늬·연령대·신체 비율·키 관계·머리/털 실루엣·식별 표지·시그니처 액세서리·기준 의상 형상·관련 시 목소리 정체성.
   - 가변: 표정·포즈·임시 머리 상태·먼지·땀·젖음·멍·피·의상 여밈·탈착 레이어·소지품·손상·조명 반응.
3. 승인된 참조 뷰를 정의한다(위 참조 팩).
4. 씬 상태는 별도로 기록한다: 오염·젖음·부상·머리 변화·소지물·의상 손상·분장·감정 상태.
5. 샷마다 SSOT를 상속하고 명시된 상태 델타만 바꾼다. 샷마다 전체 정체성을 다르게 다시 쓰지 않는다.
6. 연속성 앵커: 얼굴 형상·머리 실루엣·신체 비율·시그니처 액세서리·의상 형상·색/재질·소품 손.
7. 인접 샷을 비교한다: 정체성 표류·의상 표류·연령 표류·좌우 반전·빠진 액세서리·설명 없는 상태 리셋.
8. 생성기가 참조/캐릭터 컨디셔닝을 지원하면 승인된 참조를 쓴다. seed만으로 정체성이 보장된다고 주장하지 않는다.
9. 표류가 생기면 가장 작은 영향 단위를 재생성하고 한 번에 한 변수만 바꾼다 — 재시도 절차는 [생성 영상 QA·재시도](21-generated-video-qa-retry.md).

### 연속성 함정

손 개수/형태 변화, 액세서리가 쪽을 옮김, 머리 길이 표류, 신체 스케일 표류, 얼굴 연령 변화, 의상 무늬 변이, 눈 색 표류, 소품 손 바뀜, 설명 없는 깨끗/더러움 리셋, 비대칭 표지의 거울 반전.

연속성 검사는 `assets/continuity-ledger.csv`(shot_id·character_id·의상·소품/손·시선·화면 방향·광원 방향·진입/이탈 상태·예외 이유)로 기록한다. 생성 전에는 텍스트 원장, 생성 후에는 실제 매체와 대조한다.

## 4. 군중·스펙터클

지각된 규모를 설계할 때 인원수 문구뿐 아니라 화면의 깊이·크기·세부 차이를 함께 계획한다. 특정 군중 수나 이 절의 컷 배열이 규모감을 보장하지는 않는다.

1. 히어로 이벤트와 규모 이야기를 정한다: 무엇이 무엇에 비해 커 보여야 하는가.
2. 깊이 밴드를 만든다: 전경 앵커 · 중경 군집 · 배경 질량 · 환경 규모 단서 · 하늘/건축/지형.
3. 군중 행동의 비교안: 보기·촬영·대화·걷기·환호·대기·뒤돌기·앉기·보안/스태프·고립된 이질 존재. 군집 공유 행동·개별 변주·동기화 가운데 브리프에 맞는 것을 선택한다. 군집이나 비동기화 자체를 의무 품질 규칙으로 쓰지 않는다.
4. 구도·빛·동작 대비·고도·깊이로 히어로 대상이 질량 위에서 읽히게 한다.
5. 군중 흐름과 안전한 공간 논리를 설계한다: 출입구·동선·무대·장벽·차량·항공기·시선 방향.
6. 규모 공개의 선택적 컷 비교안: 디테일/반응 → 중간 군집 → 극와이드 → 히어로 반응. 단일 마스터와 비교해 브리프의 정보 공개를 선택하며 이 배열을 강제하지 않는다.
7. 큰 수를 다룰 때 생성 플레이트·복제/절차적 레이어·대기 효과·합성을 선택 실행자의 지원/예산과 비교한다. 단일 생성의 불가능이나 합성의 우위를 가정하지 않는다. `assets/crowd-map-template.md` 사용.
8. QA: 반복 얼굴·복제 포즈·불가능한 밀도·떠 있는 사람·스케일 점프·차량 관통·일률적 시선·전경 깊이 부재.

규모 단서: 알려진 크기의 사람/차량·겹침 깊이·대기 원근·변주된 반복 구조·시차·고각 공개·소리 밀도·지연 공개·전경 가림.

## 5. 장면 공간 앵커와 선언된 세계 변형

여러 샷이 같은 공간을 이어받거나 portal/불가능한 스케일을 사용할 때만 적용한다. 기존 location/world SSOT에 입구·문턱·landmark·방위·가구/소품 관계와 카메라 쪽 이동을 고정하고, 이동 전후 관객이 재정위할 화면 anchor를 지정한다. 컷/POV 변경·가림은 공간 이동이나 reset이 아니다. 유지되는 위치/소품은 [26 상태 인계](26-state-causality-continuity.md)에서 후속 상태로 잇는다.

세계 규칙을 의도적으로 깨면 어느 shot/layer에서 바뀌고 ordinary space로 어떻게 돌아오는지 brief에 표시한다. portal 전후의 frame/eyeline, 방향, scale 단계와 복귀 view를 정한다. cut/dissolve/graphic wipe/composite를 비교하고 단순 cut이 더 명확하면 억지 morph를 하지 않는다. 경계 전 anchor→fantasy insert→회복 anchor를 storyboard/shot cue에 보이고, scale/방위 변화가 실제 평면도·서비스·장소 claim처럼 읽히지 않는지 inspect한다.

수치 카메라·경로·3D geometry가 필요하면 `$camera-spatial-design`으로 넘긴다; 실제 장면 geometry가 필요할 때만 해당 3D review/runtime 절차를 따른다. 단일 reference frame에서 주소·지리·실제 건축·camera solve를 역산하지 않는다. 실행 가능한 공간/카메라 근거는 계획 텍스트와 구분한다.

## 근거와 적용 범위

SSOT 티어·뷰 수·승격·ID·버전 핀·파생 상태는 패키지 운영 규격이며 책/모델의 보장 수치가 아니다. 모드 메뉴·참조 팩·군중 행동/컷 배열은 브리프별 선택지다. 2D 참조의 실사 질감 대비 우위와 군중 군집/컷 배열의 효과는 `[BASIS-UNSTATED]`이며 필수 품질 조건으로 쓰지 않는다.

자료 08 원문을 E7이 직접 읽었다(READ-PARTIAL): `E:/Book/06_Book/originals/콘텐츠_제작/md/The Visual Story Creating the Visual Structure of Film, TV, and Digital Media Third Edition (Bruce Block) (z-library.sk, 1lib.sk, z-lib.sk).md` L95–99(인쇄 pp47–49), L103–117(pp51–58). SHA-256 `403172711929152d7019ccbab9043fc0ba8c512606fc14375ef6e78cc410392c`, 368221 bytes. 알려진 크기·전중후경의 크기/질감 차이·상대 운동을 깊이 단서로 쓰는 좁은 범위만 §4에 연결한다. 군중의 전경 세부와 배경의 작은 점 대비는 원문의 예지만, 이 패키지의 군중 시트/계층/모드 추천 전체나 생성 정체성 성공률의 근거는 아니다. 도판은 미검사. 정본 인덱스 통합은 [sources.md](sources.md) 소유자에게 요청한다.

**F1 직접 대조 / §1 2D 참조:** `E:/Book/06_Book/originals/콘텐츠_제작/md/Animation  from script to screen (Culhane, Shamus) (z-library.sk, 1lib.sk, z-lib.sk).md`; 668243 bytes; SHA-256 `be4240f517b982d1d78c1417edf0affed31c999cd82ba399be51f85d4d393ca8`; **READ-PARTIAL L447–449 전체, 인쇄 pp200–201, Exercise: Animals**. 앞/옆/뒤 시점에서 그릴 정보, 중립 기본 모델과 얼굴/전신 감정 포즈 참조를 구별한 애니메이션 연습을 지원한다. 7뷰 수·모든 2D의 필수 팩·실사 질감 대비 우위·생성 성공률은 지원하지 않는다. OCR 텍스트만 읽고 도판은 미검사다.
**E7 직접 읽기 / §4 군중·공간 연출(READ-PARTIAL; 도판 미검사):** Katz, `E:/Book/06_Book/originals/콘텐츠_제작/md/Film Directing Shot by Shot Visualizing from Concept to Screen (Steven D. Katz) (z-library.sk, 1lib.sk, z-lib.sk).md`, 535607 bytes, SHA-256 `e8ad5bf5ecc3659fb9b936dd081147a465b03ca09f53e6d690ca286fa4706e9a`, L521–523/L539–543: principal players and foreground/background crowd staging. Culhane, `E:/Book/06_Book/originals/콘텐츠_제작/md/Animation  from script to screen (Culhane, Shamus) (z-library.sk, 1lib.sk, z-lib.sk).md`, 668243 bytes, SHA-256 `be4240f517b982d1d78c1417edf0affed31c999cd82ba399be51f85d4d393ca8`, L411–413: subordinate reaction examples. Block L95–117 (same 368221-byte rendition above) supports qualitative depth cues only. These passages do not validate a universal crowd behavior, cut ladder, portal return recipe, safety plan, sound-scale effect, or generator result; the techniques remain brief-dependent proposals.
