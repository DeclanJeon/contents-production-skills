# 블로킹·촬영·스토리보드

## 입력과 산출물
입력: 각본, 룩, 장소, 인원·장비

산출물: 샷 리스트, 블로킹, 스토리보드 설명, 커버리지
제작용/상세 콘티, 전체 스토리보드 시트, 업로드한 제작 콘티의 보완이면 [완전한 스토리보드 계약](storyboard-contract.md)을 필수 적용한다. narrative panel과 shot은 다른 단위지만 카메라/공간/발화/음향/VFX를 최종 보드 인덱스에 함께 연결한다.

## 실행 절차
1. 보드의 목적·수신자·현재 사용 단계를 정한다. 콘셉트 피치와 촬영 실행 보드를 구분하고, 촬영 순서와 이야기 순서를 혼동하지 않는다.
2. 장면의 목적·진입→종료 지식/감정 변화·정보 공개 순서와 인물의 힘 관계를 먼저 정한다. 인물 위치·이동·시선·행동 축·제약을 기록한 뒤 카메라 처리를 설계한다. 완전한 제작용 보드는 [씬별 카메라 의도와 인접 씬 비교](storyboard-contract.md#씬별-카메라-의도와-인접-씬-비교)에 따라 기존 scene_id/shot_id에 연결한 씬당 한 행을 같은 보드 안에 반환한다.
3. 각 샷에 보는 대상과 관객이 새로 알 정보, 감정 목적을 붙인다. 관객의 관점, 화면에 담거나 제외할 정보, 구도·주목점의 선택 이유를 적는다. 씬 의도에서 샷별 시작/끝 프레이밍과 static/무빙 선택을 도출하고, 이동이 중요하면 행동/공개 타이밍과 시작 계기·대상·정착/컷을 연결한다. 멋진 움직임만 있는 샷은 삭제하거나 동기를 부여하고 static이 더 적합하면 그 이유를 적는다.
4. 시각 선택이 중요한 씬만 썸네일 수준 대안을 비교해 샷 흐름·구도·스테이징·공개 순서를 시험한다. 대안은 고정된 사건 순서를 지키며, 채택안과 미승인 제안을 구분한다. 확정된 방향만으로 충분하면 대안을 억지로 만들지 않는다.
5. 와이드·싱글·투샷·리액션·인서트 중 장면에 필요한 커버리지만 선택한다. 대사를 전부 정면 교차 편집으로 해결하지 않는다.
6. 이동의 시작·끝·속도·동기·종료 프레임을 정한다. **걷기/정지 또는 카메라 무빙이 핵심이면 `assets/06-shots-template.md`의 canonical cue table을 채워 shot plan에 반환한다.** 컷 phase/hold은 기존 09 편집 슬롯에, 채택 카메라 지시와 지원 상태는 기존 11 인계 슬롯에 기록한다(`UNKNOWN` until endpoint support is checked). 보편적 gait timing은 정하지 않는다. 상세 곡선은 [카메라 무빙 타이밍](../../camera-spatial-design/references/motion-timing-lens.md)을 따른다.
7. 시선·화면 방향·180도 축·행동 축을 검수한다. 축을 넘으면 중립 샷·연속 이동·새 공간 설명 등 관객을 재정위시키는 수단을 명시한다. 앞/뒤 씬의 목적·관객 지식 변화·POV/축·프레이밍 진행·static/무빙·공개/행동 타이밍을 비교해 대비/연속성을 기록한다. 의도적 반복은 유지할 이유를 적되 씬마다 다른 수치·무빙이나 샷마다 대안을 강제하지 않는다.
8. 편집 핸들, 룸톤, 소품 인서트와 반응 샷을 확보한다. 장소·광원·세팅으로 촬영 순서를 묶고 이야기 순서와 구분한다.
9. 패널에서 핵심 행동의 실루엣, 인물·소품 겹침, 주목점·시선 유도, 필요한 깊이·대비 및 최종 출력 크기에서의 판독성을 확인한다. 필수 정보가 읽히지 않으면 구도·스테이징·시점 또는 패널 분할을 고친다.
10. 동작 중심 비트의 start/action_peak/end 이미지는 실제 시간 상태 차이를 보여야 한다. 인접 패널에 자세·행동·손-제품 접촉·시선·공간 관계의 변화가 없으면 키프레임을 다시 스테이징한다. 제공된 인물/제품 reference를 완성된 컷아웃으로 붙이지 않고, 제품이 장면의 원근·광원·접촉 안에서 읽히는지 확인한다.
11. 스토리보드가 텍스트 설명뿐이면 이미지가 완성됐다고 말하지 않는다. 실제 그림/프리비즈가 있으면 카메라와 블로킹을 비교한다.

### 정보 단위와 POV/반응 인계

하나의 scene에 여러 shot이 있을 수 있고, 한 shot도 여러 action-phase를 포함할 수 있다. 장면에서 actor/camera/action 변화가 없다면 event detector나 시각 grain마다 새 shot을 만들지 않는다. 반대로 POV 이동과 상대의 reaction은 서로 다른 정보/관점을 전달할 때 각각 목적·진입/종료 상태가 보이는 shot으로 분리한다. 같은 continuous shot에서 양쪽을 실제로 볼 수 있으면 한 shot 안의 phase로 적고, 관찰되지 않은 reverse/cut을 가정하지 않는다.

특히 상대의 표정을 보여 주는 host/reverse shot에서 guest의 POV 전환·후속 이동을 같은 shot에 연속 서술하지 않는다. host reaction은 그 shot에 보이는 host/구도에 한정한다. guest의 시선·POV·복귀 동작은 별도의 shot 또는 같은 프레임에서 양쪽을 실제로 볼 수 있도록 의도한 구도로 계획하고, 그 연결이 불명확하면 06의 shot ID/time/blocking/관점·공개 필드를 분리해 09의 컷 순서와 잇는다. shot 한 행/ID에 여러 관점이 들어가도 관객에게 실제로 함께 보이는 근거가 있어야 한다.

각 shot에는 초점 대상, 새 정보, 행동의 주체·상대, reaction cue, 종료 상태를 기존 shot/beat/cue 필드에 기록한다. 핵심 반응이나 product handoff가 앞 shot의 자극에 의존하면 cut order와 cue를 [09-edit](09-edit.md)에 연결한다. 캐릭터 목표/실행 가능한 action은 [04-performance](04-performance.md), 지속 상태와 가림 뒤 재등장은 해당할 때만 [26-state-causality-continuity](26-state-causality-continuity.md)로 넘긴다. Copy가 행동을 약속하면 텍스트 상태와 행동을 맞추되 shot count나 endcard/CTA를 새로 의무화하지 않는다.

소품의 소유/위치가 다음 행동·복귀에 영향을 주면 이 상태를 sequence 끝까지 계획한다. 기존 `인물 블로킹`, `종료 프레임`, 필요 시 26의 `끝 상태와 근거`/`후속 유지 범위 / 리셋 조건`을 연결하고, 사용자가 이동·복귀만 지정했어도 소품을 들고 갈지 목적지에서 내려놓을지 시각적으로 일관된 선택을 한다. 실행 가능 정보가 있는데 컷에서 처리를 생략하거나 `미정`으로 두지 않는다; 실제 제공 자료/제품 물성 없이는 결정 불가한 사실만 미확인으로 남긴다.

위계/스케일 농담에서 아동과 성인의 대상/역할을 마주 놓을 때, 두 인물·시간·관계가 같은지 브리프에서 정하고 storyboard의 기존 character/shot identity를 맞춘다. 명시된 허구가 아니면 아동이 실제 차량을 운전하거나 위험한 행동을 하는 것처럼 staging하지 않는다. copy가 한 뜻에서 다른 뜻으로 바뀌면 두 화면 상태와 각각의 대상/행동을 별도로 적는다; 연결점이 불분명하면 단순 cut 또는 copy 변경을 비교한다.

필요한 경우에만 쓰는 사건→개별 시선→집단 반응→원인 대상/역방향 정보→문구 순서는 package-authored sequencing heuristic이다(`[BASIS-UNSTATED]` as an external efficacy claim). Katz의 특정 반응 coverage 사례는 해당 sequence가 보편적이거나 관객 주의를 개선한다는 근거가 아니다. 각 반응을 독립 cut으로 강제하지 않고 같은 scene의 phase일 수 있는지 검토한다. 확인 가능한 eyeline과 공간 관계를 맞추고 표정만으로 목격, 말, 동의, 동일 사건을 추정하지 않는다. 관련 장르 기대/closure는 실제 comedy brief일 때만 [17-genre-comedy](17-genre-comedy.md)에서 판단한다.

숙박/서비스/장소를 따라가는 브리프에는 입구→경로→문턱→기준 landmark→목적지와 복귀를 scene/shot fields의 공간 기준으로 선언할 수 있다. 이 경로/miniature/portal staging은 package-authored continuity proposal이지, 관객이 실제 floorplan·이동 거리·스케일 전환을 이해한다는 근거가 아니다(`[BASIS-UNSTATED]` as an external effect claim). 프레임/POV가 바뀌어도 landmark·방향·소품 소유 관계를 유지하고, 가림·wipe만으로 실제 floorplan이나 이동 거리를 증명하지 않는다. 수치 spatial/camera 요청은 기존 `$camera-spatial-design` handoff를 사용한다.

화면 안 화면·인셋이 선택된 경우 main/secondary 정보, 공개 순서, 기준 anchor, 각 창의 시간·공간·출처가 같은지/다른지를 package-authored layout/QA fields로 기록한다. 이는 시선을 더 잘 유도하거나 관객 이해를 보장한다는 근거가 아니다(`[BASIS-UNSTATED]` as an external effect claim). 동시 inset이면 동시 동작을 실제로 보이는지, 과거/별도 세계의 insert면 그 시간·공간 전환이 읽히는지 계획하고 실제 출력 크기와 크롭에서 각 창의 대상·행동·타이포를 검사한다; flash나 detector event 수만으로 리듬/beat를 만들거나 동시성을 주장하지 않는다.

## 참조 자료에서 샷으로 인계 (해당 시)

시트·배치도·직전 클립·프리비즈를 보드/샷으로 옮기면 [실무 인계 R1/R3](29-reference-driven-production.md#space-performance)를 적용한다(GUIDE-01 pp60–64, 74–84). 시작 실제 상태/정체성/소품 배치/카메라의 속성별 우선 기준을 기존 `인물 블로킹`, `시선/축`, `공개 정보`, `카메라 동작`, `종료 프레임`, `핸들`에 연결하고 상세 역할표는 11 인계 템플릿을 참조한다. 대역과 실제 인물을 매핑하며 대역 외형/임시 소리를 전사하지 않는다. 한 출력 클립 안의 여러 샷을 파일 수에 맞춰 합치지 않는다. 샷/클립/테이크 단위만 묻는 요청에서 실제 원장/샷 ID가 제공되지 않았으면 역할명(와이드/인서트/반응)과 `ID 미배정`으로 설명한다. 새 SH01 등의 ID를 실제 배정/조회한 값처럼 제시하지 않는다. 예시 ID가 꼭 필요하면 비정본 예시라고 명시하고 실제 asset·타임코드도 미확인으로 남긴다. 샷 목적·핸들·필수 사건 커버리지를 유지하고, 정지 프리비즈 검사로 연속 동작/음성 검수를 완료 처리하지 않는다. 기존 공간 게이트/실행 승인은 바꾸지 않는다.

## 산출물 목적 구분 — 스토리보드·샷리스트·애니매틱·프리비즈

같은 샷 ID를 공유해도 네 산출물은 목적이 다르며 하나가 다른 하나를 대체하지 않는다. 영화 라이프사이클에서는 [영화 제작 라이프사이클](28-film-production-lifecycle.md)의 03 Pre-production 라우팅을 따른다.

- **스토리보드**: 이야기·정보 공개를 설명하는 시각 설명물. [완전한 스토리보드 계약](storyboard-contract.md)이 panel→shot→scene 연결과 이미지 검수를 소유한다.
- **실행 샷리스트**: 촬영/생성 지시용 기술 목록(`assets/shot-list.csv`, `06-shots-template.md`). 계획된 촬영 순서는 장소·광원·세팅·배우 가용 기준으로 묶고 **이야기 순서와 별도 열**로 기록한다.
- **애니매틱**: 시간축 위의 순서 검증용 임시 편집물(타이밍·임시 소리). 완성 영상이나 실제 녹음이 아니다.
- **3D 프리비즈**: 공간·카메라 경로의 수치 검증(→ `camera-spatial-design`, `blender-previsualization` 인계). 미감·연기를 보장하지 않는다.

**이야기 순서 ≠ 촬영 순서.** 이야기 순서는 스토리보드 패널 배열과 최종 타임라인 순서다. 촬영 순서는 세팅·자원 기준 실행 순서로서 이 템플릿의 계획 열에 두고, 실제로 촬영된 순서는 실사에 한해 `assets/film-production-day-template.md`의 촬영 순번에 별도 기록한다. 둘을 한 필드로 섞거나 촬영 순서로 이야기 순서를 덮어쓰지 않는다.

## 완료 조건
보드의 목적에 맞는 촬영 가능한 커버리지와 방향성이 확보됐는가? 각 샷의 관점·구도 선택이 의도한 정보와 감정을 전달하는가? 실제 이미지가 있으면 필수 행동과 주목점이 읽히는가? 동작 중심 panel은 인접 keyframe에서 자세·행동·제품 접촉/위치가 실제로 달라지는가?

완전한 제작용 보드는 [씬 카메라 수락 검사](storyboard-contract.md#씬-카메라-수락-검사)를 적용한다. 씬 의도/shot 연결 누락, 비트와 맞지 않거나 빠진 샷 카메라 슬롯, 근거 없는 인접 씬 관계/반복, 순서상 축·화면 방향·공개/접촉 타이밍·행동 가독성의 모순은 해당 ID로 FIX를 반환한다. N/A·deferred·blocker는 사유/단계와 함께 유지하고 증거가 없으면 미검증으로 둔다. 텍스트 의도 검토와 실제 이미지/프리비즈 검사를 분리하며 필드 채움·구조 검사 통과를 시각 검증으로 보고하지 않는다.

## 근거와 적용 범위
자료 ID: 04,05,06,07,08. `sources.md`에서 파일 상태와 탐색 위치를 확인한다. 절차와 템플릿은 여러 자료의 개념을 결합한 독자 설계다. 저자의 규칙을 그대로 재현한 요약이나 공식 인증된 방법론으로 표현하지 않는다.
04 L37은 동기 있는 카메라 이동의 배경이고, 05 L333–355는 축·화면 방향·재정위, L595–597은 앵글 의미의 맥락 의존성을 직접 지원한다(READ-PARTIAL, [직접 대조 구간](sources.md#직접-대조-구간--2026-10-16-w4)). 05 L75는 시각화 모델 소개에 한정하므로 축의 locator로 쓰지 않는다. 도판·전체 커버리지·키패널 체계의 지원은 별도 확인하며 ID·cue·보드 슬롯·수치 인계는 패키지 규격이다.

E5 직접 읽기(READ-PARTIAL): `E:/Book/06_Book/originals/콘텐츠_제작/md/Film Directing Shot by Shot Visualizing from Concept to Screen (Steven D. Katz) (z-library.sk, 1lib.sk, z-lib.sk).md`, SHA-256 `e8ad5bf5ecc3659fb9b936dd081147a465b03ca09f53e6d690ca286fa4706e9a`, 535607 bytes, L389–393 `Camera Cutting vs. Coverage`(이 구간의 인쇄 페이지 표기 없음). 정밀한 camera cutting과 여분 coverage의 장단점, 전체 행동을 확보하는 이유, 말하는 아버지만이 아니라 듣는 아이들의 반응을 확보하는 예를 지원한다. 모든 장면에 고정 샷 수를 부과하거나 모든 coverage를 보장하지 않는다. 썸네일→핵심 상태→접촉 상태를 계획하는 근거는 [08의 Williams L137–155](08-animation.md#근거와-적용-범위), 행동 판독은 [05의 L525](05-visual.md#근거와-적용-범위)로 한정한다. start/action_peak/end라는 슬롯 이름·패널 수·ID·순서 원장은 패키지 규격이며 책의 그대로인 키패널 분류가 아니다. 도판은 미확인이다.
추가 직접 읽기(READ-PARTIAL): Katz 동일 535607-byte rendition, SHA-256 `e8ad5bf5ecc3659fb9b936dd081147a465b03ca09f53e6d690ca286fa4706e9a`, L333–355(printed p130 onward)는 screen direction과 visible reorientation/camera crossing을 지원하고, L393–395는 action 중 cut의 편집 선택을 설명한다. 이 구간들은 축/행동 연속성의 planning 근거이지 모든 장면의 고정 coverage, 정확한 key-pose 세트, inset·portal 배치나 특정 reaction ladder의 효능 근거가 아니다.

## 출력 템플릿
`assets/06-shots-template.md`를 복사해 채운다.

스토리보드가 요청되면 `assets/storyboard-panels.csv`를 정본 project.json의 투영으로 작성해 panel_id→shot_id→scene_id와 패널별 `beat_ids`/원문 위치·`visible_character_ids`·`audio_cue_ids`·`speech_ids`를 연결한다. 샷 단위 목록을 패널 목록으로 대신하지 않는다. `frame_time_s`는 패널의 기준 시각이며 연결한 음향 큐와 발화의 시간 구간에 포함돼야 한다. 실제 image_asset_id를 등록하고 텍스트 계획만 있으면 planned/drawing_pending으로 구분한다. 상세 보드는 모든 씬/샷의 시작·필요 정점·끝 패널 또는 정지 hold를 포함하고 이미지 수를 사전 계산한다. 필수 행동이 가려지거나 설명 없이 인과가 끊기면 해당 인덱스를 수정한다.

## 전문 스킬 인계
`$camera-spatial-design`으로 위치·거리·렌즈·각도·구도·전 프레임 경로를 수치화하고, 장면별 3D 카메라/공간 작업은 `$blender-previsualization`으로 실제 구현·시각 검수를 반드시 수행한다. `camera_spec.json`의 로컬 프레임을 기존 샷의 start_s/end_s와 연결하고 total duration을 대조한다. Blender 미실행 시 3D 화면 검증은 BLOCKED/UNVERIFIED다.

## 심화 참조
복잡 접촉·동작 분할은 [생성 영상 QA·재시도](21-generated-video-qa-retry.md)의 모션 절차(`../assets/motion-beat-template.md`), 군중·스펙터클은 [비주얼 모드·SSOT](20-visual-mode-ssot.md) §4(`../assets/crowd-map-template.md`).
