# Rofan 제작 원리의 기존 스킬 이전 설계

## 상태와 목적

- 역사적 T12 상태: **기존 casebank 적용; copied-package reader 결과 부분 미충족**. 저장 관찰 57개, worked proposal 4개, 지원 cue 4개를 적용했으며, frozen suite는 case retrieval/output handoff만 평가했다. Active-owner T12는 15 PASS / 1 PASS_WITH_CONTEXT_LIMIT / 2 PARTIAL_NOT_MET, guard failure 0이며 all-pass가 아니다. 이는 archive-wide craft extraction/owner skillification의 완료 증거가 아니다. 이후 범위 수정과 현재 접근 한계는 아래 `승인된 범위 수정`에 기록한다. 상세 historical evidence: [적용 계획](../plans/2026-10-12-rofan-craft-skill-application.md), [테스트 계획](../../implementation/2026-10-12-rofan-craft-skill-test-plan.md).
- 목표: 분석 가능한 영상 아카이브의 관찰·교차 영상 패턴을 기존 content-production owner 절차와 대조하고, 사용자가 명시적으로 요청한 경우 증거로 확인된 일반 제작 절차/QA 공백만 해당 실제 owner에 이전한다. 57개 saved cases는 보존된 provenance/evidence이며 정책·필수 조회 경로가 아니다. 관찰·해석·새 brief 제안을 분리한다.
- 적용 길이: 길이 제한 없음. 특정 30초 드라마에 한정하지 않고, 요청된 컷신·장면·콘텐츠의 실제 길이와 매체에 맞춘다.
- 권한 경계: 승인 범위는 지정된 skill/reference와 계획·설계·README·CHANGELOG 문서 변경이다. 패키지 버전·스키마·manifest, 미디어·생성·역사 실행 및 무관한 파일은 변경하지 않았다.


## 결정 요약

| 결정 | 설계와 이유 |
|---|---|
| 단일 목록 | 아래 57개 항목이 canonical craft inventory의 유일한 정본이다. 57은 inventory coverage의 최소 기준이지 향후 supporting example 수의 상한이 아니다. 향후 예시는 목록 전체를 복사하지 않고 각 항목을 참조한다. |
| 기존 소유권·진입 | `25-reference-video-analysis.md`가 evidence→mechanism→new brief→QA와 A01–A12 owner routing을 제공하므로 분석 경로로 유지한다. 명시적 skillification에서는 교차 패턴→각 관련 owner/template/QA 비교→증거 기반 실제 공백만 기존 owner 수정 순서를 따른다. 사례집은 provenance/evidence이지 policy가 아니다. |
| 사례집의 역할 | `video-production-assets/references/rofan-craft-examples.md`는 57개 저장 관찰과 4개 보조 관찰을 담는 선택적 provenance/evidence index다. 작업지시서와 QA/출력 절차는 포함하지 않는다. 실행 policy나 prompt lookup이 아니며 일반 owner 절차를 대신하지 않는다. |
| 근거 계층 | 저장된 분석 관찰, 해석/인과 가설, 새 brief용 설계 제안, 실제 생성 결과 검수는 별도 상태다. 영상은 이 작업에서 새로 열거나 검사하지 않았다. |
| 실제 검수 | 사례는 미디어 생성 승인이나 실제 QA를 대신하지 않는다. 생성 후 검수는 기존 실제 결과 QA 소유자가 수행한다. |

## 범위와 비목표

**포함:** 분석 가능한 archive의 source-grounded camera/action/timing/edit/performance craft pattern 종합; 5개 군 57 saved observations의 provenance/coverage 기록; 각 transferable pattern을 실제 관련 owner procedure/template/QA와 비교; 명시적 skillification 요청에 한해 증거로 확인된 일반 절차/QA 공백만 그 owner에 최소 이전; 보호 표현/미확인 범위 분리; 적용 후 문서 검증.

**비목표:** 줄거리/사건·인물/관계·장소/세트·소품·의상·고유 디자인/샷 배열·안무·원본 절대 타이밍의 모방, 근거 없는 source-wide/상시 적용 규칙, 요청 없는 skill mutation, 자동 승격, 생성·편집·렌더/Blender 실행, 신규 project schema/DB/조정자/ID 체계, 생성 자연스러움/프롬프트 제어 성능 입증, 유사도 점수·성과 보장. 사용자가 명시한 skillification 요청의 evidence-backed, source-neutral procedure/QA gap synthesis는 비목표가 아니다.

## 근거, 출처 및 신뢰 범위

관찰·상세 근거는 기록된 분석 및 F: `AI-Rofan-Drama-2026-10-11`의 직접 확인된 source ledgers에서 온다. root와 일부 JSON metadata 안의 오래된 C: 경로는 동일 자료의 현재 F: 위치와 함께 보존된 legacy locator이며 현재 접근 불가를 뜻하지 않는다. 이번 점검에서 원본 미디어 playback/full decode는 하지 않았다. source 접두사는 locator이지 전체 ID·제목·정확한 숏/렌즈/장비 정보가 아니다. 일부 source rows와 global gates는 미완료이므로 ledger 접근을 전체 source의 의미상 종결로 취급하지 않는다.

**Historical casebank-body recovery snapshot (not the current F: ledger-access status):** At that earlier recovery point, 44 sources had been routed but were not all semantically closed. Sixteen saved B casebank IDs were confirmed; this did not mean every body was recovered or verified. Public saved logs restored C7/D8 source IDs. The read-only paired successful evals were C840/D942; D797 had 95 shot rows but only its opening excerpt was then recoverable. D8fba recorded 3.4/5.08MB and dense 310/686 events, while its full body was then unavailable; the fde1 dynamic ledger body was not then accessible; C9e26 and Db834 bodies were not then recovered. These are historical casebank-body recovery limits, not a claim that the current F: root or semantic ledgers are inaccessible. Counts do not reconstruct missing observations.

접근을 시도한 경로는 Windows/home/runtime aliases, 성공적으로 읽은 공개 read/write/edit 결과, 공개 eval AST literals다. 비공개 데이터나 오래된 코드를 실행하지 않았다. 증거 상태를 섞지 않는다: **관찰**은 저장 분석의 명시적 시각 설명, **추론**은 의도·인과·기법 해석, **설계 제안**은 새 작업에 적용할 제안 시각/단계, **미검증**은 현 도구·실제 영상/생성 결과 검수가 없는 상태다. 영상 개별 타이밍은 기존 분석 메모로 기록된 관찰 locator일 뿐 새 정밀 프레임 판독이 아니다.
**과거 감사 범위 기록:** 선행 탐색의 audit inventory는 46개 entry/reference/template 파일이었다. 이 숫자는 역사적 scope count이며 46개 파일이 당시 작업에서 변경되거나 새로 감사되었다는 뜻이 아니다. 초기 T12 작업은 casebank 중심이었다; 이후 승인된 범위 수정은 기존 skill/owner 절차와 이 spec/plan/test 기록도 갱신했다. 어느 기록도 현재 접근 불가한 영상의 재검사나 archive-wide coverage를 주장하지 않는다.

저장된 작품의 분석 관찰은 캐릭터·장소·의상·소품·구체적 표현을 재사용하거나 재현할 권리/허가를 부여하지 않는다. 새 brief에서는 사용자가 승인한 자산·캐릭터·setting을 사용하고, 여기서 이전할 것은 권리 검토를 통과한 범용 제작 메커니즘뿐이다. 원본 미디어의 접근·인용·재사용은 기존 권리/permission gate를 별도로 따른다.
## 승인된 범위 수정 (historical T20 이후)

초기 설계는 작업을 57개 saved-case 검색성·예시로 좁히고 universal craft procedure 설치를 비목표로 두었다. 이는 original intent인 archive craft 분석 후 transferable filmmaking method를 기존 content-production skill에 이전한다는 범위를 충족하지 못했다. 수정된 접근은 아카이브 패턴 종합 → 각 관련 owner/reference/template/QA와 gap 비교 → 증거가 확인된 일반 절차/QA만 정본 owner에 최소 반영이다. 사례집은 선택적 provenance/evidence로만 유지하며 policy나 필수 prompt lookup으로 쓰지 않는다. 분석만 요청된 경우에는 계속 skill files를 수정하지 않는다. 이전 대상에서 줄거리·인물·장소·소품·고유 표현과 원본의 특정 shot/timing imitation은 명시적으로 제외한다.

**Historical T20-era coverage snapshot (retained as historical, not current):** Its 44-source/335-strip extraction, 6,002 detector candidates, then-reported `manual_review.json` access, semantic materialization counts, 1/44 full-source run, stale progress/lock, and unresolved semantic gates describe that snapshot only. They establish neither complete review nor prevalence and are superseded for current status by the later archive work order; T20 prompt/rubric/raw grades remain frozen.
**Current later audit:** The [2026-10-13 work order](../plans/2026-10-13-rofan-archive-craft-completion.md) and [QA register](../../../qa/rofan-archive-craft-completion-register.json) record 44/44 overview sheets, 335/335 sampled windows, one confirmed hard cut (ordinal 13), one unresolved native bracket (ordinal 41), zero continuous playback/audio listening, no complete source-to-shot/event crosswalk, and five OPEN gates. All 44 current F: filename/size/hash tuples match the identity inventory; URL-ID→filename mapping remains unresolved. The seven-family owner comparison reports already-covered owners and insufficient source-derived support for a new reusable gap. The archive crosswalk remains a generic requirement only for explicit exhaustive or cross-source extraction; the 04/07 cues are conditional general design guidance, not archive-proven gaps.

### 확인된 B casebank locator

다음 16개 canonical case ID는 확인된 저장 ID 그대로이며 source prefix 이상의 원본 식별을 주장하지 않는다. 각 항목은 목록의 관련 조건에 참고로 연결할 수 있다.

- `fee0-wide-onset-to-body-then-portrait`
- `7488-bed-two-shot-to-reverse-portrait`
- `0ad-carriage-threshold-foot-detail`
- `0ad-snowboot-pressure-without-full-gait`
- `0ad-seat-rise-insert-to-standing-state`
- `fb568-near-contact-hand-and-hair-hold`
- `fb568-dark-armour-to-horse-soft-reveal`
- `be746-dark-object-insert-and-reaction-hold`
- `be746-text-report-to-bedroom-attention`
- `fee0-whip-blur-one-within-shot-event`
- `7edf-opening-title-overlay-as-independent-information-layer`
- `fb568-time-card-fade-as-explicit-but-not-proven-chronology`
- `7488-bonus-scene-after-apparent-title-and-late-ending`
- `7edf-wide-to-ots-is-one-edit-not-two`
- `fee0-box-to-paper-prop-reveal`
- `fb568-saddle-pose-change-is-not-a-full-dismount`

추가 저장 locator 네 건: `0ad` seat-rise wide 201.067708 PTS 3088384에서 rise 시작, shoe insert 약 212.934, 이후 standing state; 이는 전체 연속 행동 아님. `be746` report caption은 corridor 64.6, pair attention 66.4, wide 77.534, door insert 81.467; caption 가독성은 관찰 가능하지만 실제 발화/문 조작자 증거는 아니다. `7edf` wide 15.5→OTS 15.542→15.584는 동일 OTS 상태이며 세 컷이 아니다. `797`은 illustrated opening title 약 0s에서 live bed image 약 0.2s로 이어지며 opening excerpt만 복구 가능하다; 뒤이은 내용은 추론하지 않는다. 이는 기존 분석 locator로서, 본 작업의 새 미디어 검수나 전체 source 복구를 뜻하지 않는다.

## 현재 역량과 실제 보강 격차

| 구분 | 이미 존재/증거 | 설계상 처리 |
|---|---|---|
| 기본 craft | 기존 스킬은 walk/decelerate/plant/stop/settle/reaction, 동일 시간축 actor/camera phase, 접촉·paired response, spatial axis/anchor, prop/wardrobe persistence, time elision, 관찰/추론/미확인 구분, tool support, 실제 generated-output QA를 이미 다룬다. | 이를 새 기능으로 다시 쓰지 않는다. 아래 사례는 기존 계약의 예시 선택성·검색성을 보완한다. |
| reference-video bridge | `25-reference-video-analysis.md`는 이미 evidence→mechanism→new brief→QA 이전 절차와 A01–A12 owner routing을 갖는다. | “일반 bridge가 없다”는 갭 주장을 철회한다. 해당 경로를 재사용하고 구체 사례 발견성을 높인다. |

### 7개 보강 범주

이전 분석이 식별한 개선 필요는 기본 craft capability의 부재가 아니라 사례·근거 범위의 보완이다.

1. **범위와 source-example breadth:** 57개 recovered observations를 조건별로 연결해 craft variation을 넓힌다. 이는 44개 source 전체의 완전 분석이 아니다.
2. **문제→예시 retrieval:** brief의 관찰 가능한 문제 cue로 적절한 saved case를 찾을 수 있도록 indexed retrieval을 둔다.
3. **Paired counterexamples:** 예가 적용되지 않는 opener/가림/컷/미확인 상태를 함께 표시한다.
4. **Multi-owner complete examples:** 하나의 scene proposal을 기존 owner/template fields를 따라 끝까지 펼쳐 보인다.
5. **Per-case observable failure criteria:** 각 case에서 결과가 읽히는지, 연속성/소유/접촉/컷 경계가 유지되는지의 실제 검수 질문을 둔다. 실제 실패 사례는 저장된 근거가 있는 경우만 기록한다.
6. **Data access/completion:** 원본 body가 현재 unavailable/incomplete인 상황과 이미 보존된 bounded observation을 분리하고, counts로 세부를 복원하지 않는다.
7. **Generated-quality empiricism:** naturalness, prompt controllability, tool support 및 품질 개선은 이 자료로 실증하지 않았다. 이를 입증하려면 별도 승인과 실제 generated-output evaluation이 필요하다.

### 적용 진입점과 사례 파일

`25-reference-video-analysis.md`는 이미 존재하는 transfer procedure와 A01–A12 owner routing이며 유지한다. 저장 사례 재사용은 원본 미디어의 fresh analysis를 요구하지 않는다. `video-production-assets/SKILL.md` on-demand table의 기존 25 row에는 저장 사례 재사용 요청 또는 현재 brief의 구체적 문제 cue가 사례와 일치할 때만 25를 열도록 조건을 두었다. 기존 06 scene-planning step 3와 25의 기존 analysis/transfer route에는 선택형 사례집으로 가는 한 문장 pointer가 있다. 현재 경로 `video-production-assets/references/rofan-craft-examples.md`에는 57 ID의 self-contained problem index와 네 worked proposal이 있으며 canonical 57-row source table을 복제하지 않는다. 일반 브리프에는 조회를 강제하지 않는다.

불적용 조건도 보여준다. 이미 접촉 중인 opener에 first-touch를 발명하지 않고, 가려진 발/부분 동작으로 full gait를 주장하지 않으며, overlay/blur/flare를 컷으로 세지 않고, source에 없는 소품 정체·행위·경과시간을 추정하지 않는다. 원본 상세가 접근 불가해도 기록된 한정 관찰은 적절한 범위에서 쓸 수 있으나 미복구 내용은 unknown이다.

## 저장된 분석에서 복구된 57개 관찰의 정본 목록

이 목록은 제공된 이전 분석 요약에서 복구 가능한 57개 항목을 완전히 보존한다. 이는 전체 44 source의 의미상 모든 기법이 완전하게 조사/종결되었다는 주장이 아니다. 아래 각 행은 **관찰/범위 → 적용 조건 및 요구 → 오검증 방지(QA)** 순으로 기록한다. source 이름은 locator prefix뿐이다. 목록의 “요구”는 미래 브리프에 대한 설계이며 저장 영상의 원인/의도를 사실로 확정하지 않는다.

### 카메라와 공간 (C01–C12, 12)

| ID | 관찰·source locator | 조건부 적용 및 QA 경계 |
|---|---|---|
| C01 | `fee0`: 빈 초원 약 5.005/7.408s에서 실루엣 첫 출현 약 7.608, 두 인물 약 9.043, carry pose 약 12.947, medium 약 12.980, face 약 15.382. | 공간→실루엣→두 인물/관계→얼굴 순서가 brief의 공개 목적에 맞을 때만 단계화한다. 크기 변화 원인은 미확인; 원인을 렌즈/카메라로 단정하지 않는다. |
| C02 | `7488`: bed two-shot 0–2.7, woman close 약 2.733, man reverse 약 4.933; 상대 edge/window 유지. | 공간 관계나 접촉이 중요한 경우 shared frame을 고려한다. wide-first는 보편 규칙이 아니다. |
| C03 | `7edd`, `9e0`, `d31`: wide/reset composition observed after face/hand/object details. | Wide restore may re-establish partner/geography when the new brief needs that information; the claim that a viewer “lost” geography is an interpretation, not an observed viewer state. Do not force a wide after every detail. |
| C04 | 별도 pilot `e8c1`: bed wide high/top view 35.035–37.6378 (`7edd`와 별도 locator). | 상부/높은 시점이 공간 reset에 필요할 때 선택. `9e0`와 합치거나 출처 동일성을 주장하지 않는다. |
| C05 | `7488`, `7edf`, `d31`: reverse에서 partner의 머리카락/귀/어깨 edge anchor. | reverse에 관계 anchor가 도움이 될 때 배치한다. 실제 OTS에서 partner anchor가 얼굴/눈을 가리지 않고 상대 방향을 안정적으로 알려주는지 확인한다. 모든 reverse의 의무 요소가 아니다. |
| C06 | `a600` 834–843s: foreground shoulders frame reaction face. | 전경 어깨가 얼굴을 감싸는 반응 구도를 원할 때 사용; final frame에서 foreground edge가 얼굴/시선을 가리지 않고 reaction face remains readable인지 확인한다. |
| C07 | `c749` 37.0667–65.1: woman left FG, old man right FG, young man central BG의 세 깊이. | 세 깊이 blocking이 관계/위계를 읽히게 할 때 사용. 최종 frame에서 FG 두 인물과 BG 인물의 depth/sightline이 구분되고, actor overlap이 관계 정보를 훼손하지 않는지 확인한다. 신분/시선 의도는 brief 자료로 확정한다. |
| C08 | `c749` 21.033–37.067: 낮은 위치의 woman이 약 29.3부터 일어나 약 30에 대면; 시작 kneel/sit 불명. `2464` royal wide 70.07s에서 전경 woman과 raised queen/crowned man. | 상대 높이 변화나 raised dais가 권력/거리 정보에 필요할 때만 명시한다. 불명 시작 자세를 만들지 않는다. |
| C09 | `a600` 120.22–135.803: 한 actor FG 유지, 다른 actor가 BG로 이동/정지, 남은 actor를 통해 attention. | attention handoff가 필요할 때 사용. 최종 구도에서 stayer가 읽히고 이동 actor의 BG arrival/stop과 stayer attention이 구분되는지 확인한다. |
| C10 | `81d7` partition watcher 129.5–143.333; `d31` gate face 2097.387: 부분 가림 후 정보 공개. | 가림/공개가 장면 정보에 필요한 경우. 가려진 영역을 이미 보인 사실로 취급하지 않는다. |
| C11 | `2464` 약 18s: garment/torso에서 얼굴로 같은 shot 안 상향 reveal. | 인물 식별/반응 공개가 목적이면 한 shot 내 동작으로 계획한다. 실제 cut과 혼동하지 않는다. |
| C12 | `fee0` 607.373–607.740: rapid blur, clear origin→blur→clear arrival; physical whip/path/lens는 미확인. 후보 198–200은 하나의 event. | 방향 전환/주의 handoff에서 origin과 arrival을 명확히 둔다. 후보 프레임을 여러 컷으로 세지 않고 광학/물리 기법을 확정하지 않는다. |

### 연기와 움직임 (P01–P17, 17)

| ID | 관찰·source locator | 조건부 적용 및 QA 경계 |
|---|---|---|
| P01 | `03ab` 59.6–67.6s: approach→spacing narrows (about 64.4)→stop; full feet/gait evidence absent. | If approach and arrival matter, carry approach, deceleration and stop as distinct phases. A following reaction is a possible new brief proposal, not part of the recorded observation. Do not infer gait/foot plant from cropped feet. |
| P02 | `03ab` 107.5–114s: lean→rise→stand hold; table/candelabra/windows가 anchor. | 일어남/정착이 중요한 경우 landmark와 상태 변화를 기록한다. |
| P03 | `0ad` 86.6–90.8: threshold/boarding foot detail. | 발 디테일은 국소 행동 증거다. 전체 신체 균형/완전한 boarding cycle로 확대하지 않는다. |
| P04 | `0ad` 98.4–104.8667: 눈 위 boot pressure/imprint. | 표면 접촉/자국이 정보일 때 국소 결과를 기록한다. 전체 보행 주기·힘 크기를 추정하지 않는다. |
| P05 | `fb568` 251.6667 astride→253.1 leg cross→254.3667 beside; support phase 누락. | 관찰된 pose progression을 상태 변화로 계획할 수 있다. 완전한 dismount 연속동작으로 서술하지 않는다. |
| P06 | `81d7` 40–60.967: walk→turn/lookback→paired attention; 하체 crop. | 회고/상대 주의 전환이 필요할 때 상체와 시선을 계획한다. 완전한 하체 gait가 보였다고 하지 않는다. |
| P07 | `f7af` 0–42.233: obstacle avoidance, foreground crossing, duck/pass; 약 37.9초에 와이드 정면 달리기 화면으로 컷/스케일 리셋된다. 연속 tracking/gait 아님. | Use obstacle/foreground crossing only when it serves the brief. Preserve the cut/scale reset rather than describing continuous camera tracking. |
| P08 | `d551` EP9: 213.450/213.466667/213.516667/~213.8s (TB1/15360; PTS 3278592/3278848/3279616/3283968): separation→touch→second hand→settled clasp. | 첫 접촉이 서사상 요구될 때 접촉·두 번째 손·정착을 분리한다. 힘/의도/동의는 알 수 없다. |
| P09 | `fb568` 108.6667–114.2333: hand/head-hair near-contact anticipation; hand rises 약 111.4; positive touch 입증 아님. | 기대/망설임이 목적이면 proximity를 표현하되 touch 여부를 별도 둔다. |
| P10 | `fd2` 0–3.167: candle-lit close pair에 이미 mouth contact; first touch 없음. | 장면이 이미 contact 상태로 시작할 수 있다. 매번 approach/anticipation/first touch를 추가하지 않는다. |
| P11 | `a600` 152–154: contact 뒤 receiver response/recoil/pivot. | 상대 반응이 brief의 인과 목표일 때 response를 contact과 구분한다. 힘/의도 미확인. |
| P12 | `a600` 257–263: hand contact 유지, free hand gesture. | 접촉 유지와 자유손 동작이 동시에 필요한 장면에서 지속 상태를 명시한다. |
| P13 | `a600` 263–270: release→exit→extended arm/empty space→remaining actor reaction; `81d7` 89.767–94.167 isolated woman after departure. | 이탈 뒤 남은 actor/빈 공간이 이야기 정보일 때 반응 hold를 계획한다. |
| P14 | `a600` 160–177/813–834: held shot with micro eye/mouth/head/hand changes; audio was not listened to, so actual dialogue is unverified. | When a hold matters, distinguish micro-change from a frozen still. Do not infer speech or silence from the image. |
| P15 | `a600` 190–198: third-party/animal reaction ladder. 입 움직임은 audio 증거 아니며 동물 자연스러움 미검증. | 연쇄 반응을 의도할 때 actor 순서를 구분한다. 입모양만으로 말이나 자연스러운 동물 연기를 통과시키지 않는다. |
| P16 | `3090` 약 1210–1290: offer→receiver look→hand touch→shared bed return; 시간은 근사 메모, native first-touch 근거 아님. | 제안/응시/접촉/복귀가 실제 brief에 필요할 때 순서를 디자인한다. 근사 메모를 frame-accurate timing이라 하지 않는다. |
| P17 | `03ab` 127–135.5: supporting attendants lean in→work→withdraw→reposition alongside main actor. | 조력자의 동시 작업이 장면 기능에 있을 때 각 actor의 위치·작업·withdraw/reposition을 계획한다. |

### 소품·의상·정보 공개 (O01–O10, 10)

| ID | 관찰·source locator | 조건부 적용 및 QA 경계 |
|---|---|---|
| O01 | `fee0` 157.057 box, 178.278 pair, 248.782 paper; 긴 장면이며 하나의 연속 handoff 아님, text unreadable. | 상자→내용물/종이→반응이 의미 있을 때만 분리한다. 읽혀야 하는 글은 실제로 readable해야 하며 continuity를 과장하지 않는다. |
| O02 | `be746` 1.5 hold dark rectangle, 3.3 turn, 5.267 floor object, 7.833 face, 9.166 held gaze. | object question→reaction hold를 쓸 수 있다. 낙하, 동일 소품, 원인 관계는 입증되지 않았다. |
| O03 | `81d7` 94.167–109.8: map/table establish, point insert, response. | 지시/반응을 읽히게 할 때 표면/지도 관계를 먼저 establish한다. |
| O04 | `81d7` 129.5–143.333: paper transfer source/destination hands. | 실제 소품 전달에서 source hand→destination hand의 ownership/carry 연속성과 최종 after-holder를 추적한다. 각 손의 가림/교대가 읽히는지, hand/object fusion이나 cut 사이 소품 점프가 없는지 실제 결과에서 확인한다. 소유 의도는 미확인. |
| O05 | `a600` 16.7–19.92: cup raise→mouth→lower, stable composition. | 마시기가 정보일 때 composition 안의 시작/끝 상태를 계획한다. |
| O06 | `9e0` 약 130–133 pour, 약 136 food: tea/food insert가 face repetition을 끊음. | 장면 관련 차/음식/도구를 정보/리듬 기능으로 쓸 때. 자동으로 장식 insert라 분류하지 않는다. |
| O07 | `9e0` 약 156.7 eye detail. | eye detail과 full-face reaction이 서로 다른 정보를 줄 때 shot 목적을 구분한다. |
| O08 | `03ab` 24.1–33.6 preparation/lacing→finished look→reaction; grooming/shoes/skirt 약 33.8–48.2, 전체 dressing 연속 아님. | 준비/결과/반응이 중요할 때 생략된 구간과 상태를 둔다. 전부 연속 착장 장면이라 하지 않는다. |
| O09 | `03ab` 290.1–295.9 hem→mirror/reflection whole-gown reveal; 정확 인물 정체 미확인. | 거울/반사를 통한 의상 공개가 brief에 적절할 때. 실제 인물과 반영 인물이 읽히고 의도한 identity correspondence가 확인되는지 검수한다. source의 반영 인물 정체는 확정하지 않는다. |
| O10 | `2464` pale at 60.06→blue gown 70.07; `9e0` 약 145 different jacket/tie; dressing 행위는 보이지 않음. | 변화한 appearance state와 dressing action을 나눈다. 후속 장면에서 필요한 상태 유지/리셋을 검수한다. |

### 조명·초점·효과 (L01–L09, 9)

| ID | 관찰·source locator | 조건부 적용 및 QA 경계 |
|---|---|---|
| L01 | `9e0`: bright bed→dark warm dining/fire→cool courtyard; reverse continuity. | room-specific palette/contrast가 이야기 정보를 지원할 때 전환·reverse를 일관되게 설계한다. 색만으로 감정 원인을 단정하지 않는다. |
| L02 | `d31` opening: narrow blue gap silhouette/backlight, right warm torch, floor reflection. | threshold silhouette/backlight가 진입 공개에 맞을 때. 실내 광원 장비/물리 배치를 확정하지 않는다. |
| L03 | `430` 65.532–76.943: framed seat/windows held, progressive brightness/exposure; `d31` gate 2101.599/2101.683 rising flare, no cuts. | When gradual light change over fixed geometry serves the brief, describe it without asserting a cut/camera move or physical exposure mechanism. |
| L04 | `fb568` 244.5–249.533: dark/soft armour→horse muzzle/pink sleeve, 246.1–246.7 clearer; rig/focus mechanism unknown. | 어둠/부드러움에서 형상 공개를 설계할 수 있다. 초점/조명 장치 기법은 관찰만으로 모른다. |
| L05 | `9e0` about 266s: sharper profile, blurred woman BG. | Differential sharpness can establish visual hierarchy; it does not prove rack focus. |
| L06 | `a600` 70.17–75.61 gesture/glow; 74.108–75.81 insert; 75.81–77.478 cup separation; 77.478–79.613 trajectory past harp/statue/windows descending/break; candidates 15–28 are one within-shot action; 79.813–85.719 man/wolf reaction. | 효과의 gesture→glow→cup→trajectory→impact/fragments→witness response가 brief에서 필요할 때 인계한다. fictional causal function은 추론이며 물리적 magic/material 증거가 아니다. continuity/persistence를 실제 결과에서 QA한다. |
| L07 | `a600` 약 779–784 leg strikes table; dishes/linens shift, woman mouth/hands react. | impact→object response→witness가 필요할 때 각 결과를 확인한다. 힘·역학·충돌 원인은 입증되지 않는다. |
| L08 | `a600` 87.421–95.796: human/animal hands-cheeks/muzzle paired contact, head turn. | 접촉 상태/응답이 의미 있을 때 경계와 연속성을 디자인한다. 해부/힘의 자연스러움 미검증. |
| L09 | `d31` 약 2025s: campfire 지속 중 ghost-figure overlay. | 겹침이 의도된 정보 층일 때 배경 shot 지속과 overlay event를 구분한다. 회상/연대기는 추론이며 새 shot으로 세지 않는다. |

### 편집·시간·엔딩 (E01–E09, 9)

| ID | 관찰·source locator | 조건부 적용 및 QA 경계 |
|---|---|---|
| E01 | `3090` 약 1020–1050 rainy carry rearwide/recede→near-black→bright palace/title. | 출발→暗転→새 장소 establish는 실제로 필요한 시간/장소 압축일 때 선택한다. 연속 여행으로 입증된 것은 아니다. |
| E02 | `f7af` 42.233–71.9667 wedding faces/officiant→hand meet→rear aisle pair. | 접촉 detail 뒤 함께 떠나는 구도가 필요한 경우. 전체 연속 gait를 주장하지 않는다. |
| E03 | `b355` 265.557–289.246 sunset pair→hand→meltwater→shoot→garden→animated title. | 환경/계절 motif로 압축할 수 있으나 literal elapsed time은 확정되지 않는다. genre/relationship recap은 추론. |
| E04 | `fb568` card “3개월 전”. | 명시적 narrative timecard와 fade/edit를 각각 기록한다. 물리적 시간 경과 증명은 아니다. |
| E05 | `7edf` 약 2.5 same window/settee title overlay; `c749` 18–21.033 title/carriage candidates 1–4 are one overlay; `a600` 803–813 pink title over live image. | graphic/title layer와 underlying shot을 분리한다. overlay를 자동 컷으로 세지 않는다. |
| E06 | `7488`: apparent title→bonus label at 339s→table scene at 342.767s→actual late black/small-gold-star ending. `797`: illustrated opening title ~0→live bed ~0.2, opening body only recovered. `a600`: SODA 0–4.99→room 5.2. | Separate opener/interstitial/apparent ending from true EOS; do not infer the whole work structure from one recovered excerpt. |
| E07 | `81d7` 168.4–170.766 black, container 170.852426; `a600` last visible PTS 13488672 at 843.042, container 843.093. | picture black/EOS와 container tail을 각각 실제 파일에서 확인한다. container duration만으로 마지막 picture frame을 단정하지 않는다. |
| E08 | `fee0` whip blur, `d31` gate flare, `a600` cup motion은 blur/flare/continuous motion이지 여러 cut이라는 증거 아님. | 실제 편집 boundary만 cut으로 기록한다. blur, flare, effect phase를 가짜 frame cut으로 분해하지 않는다. |
| E09 | `d31` 약 2094.843 restrained three/gate frontal→profile angle: same place, angle coverage. | coverage angle change와 새 장소/시간 전환을 분리한다. |

## 기존 스킬 적용 설계

적용 계획은 아래 경계를 기준으로 작성하며, 구체적인 파일별 체크리스트/실행은 [별도 적용 계획](../plans/2026-10-12-rofan-craft-skill-application.md)이 소유한다. 이 섹션은 원리와 계약을 정하며 적용 완료를 주장하지 않는다.

### 아키텍처와 정보 계층

1. `25-reference-video-analysis.md`는 기존 transfer entry/router로 유지한다. 저장 사례 재사용은 fresh source analysis 없이 가능하고, 새 영상 분석 요청에 한해 기존 분석 절차를 따른다.
2. `video-production-assets/SKILL.md` on-demand table의 기존 25 row는 저장 사례 재사용 요청 또는 active brief의 구체적 문제 cue가 catalogued cue와 일치할 때만 25를 열도록 조건부 연결한다. 새 source 분석은 prerequisite가 아니다.
3. 기존 06 scene-planning step 3와 25의 brief-transfer section은 선택형 사례집으로 연결한다. 25의 기존 analysis/transfer procedure와 A01–A12 routing은 그대로 유지한다; 다른 owner에 default pointer를 만들지 않는다.
4. 사례 bank는 조건별 문제 검색, source locator, 접근성, 관찰/해석/제안 경계, 제한/반례, 기존 owner/template destination, 네 개 worked example 및 필요한 supporting cases를 둔다. canonical 57-row 목록을 bank나 모든 SKILL/owner에 복사하지 않는다.
5. 기존 owner reference/template만 실제 필요에 따라 연결한다. 04 performance는 상대 반응; 06 shots는 공간/camera/blocking; 08 animation은 동작; 09 edit는 cut/time/elision/title; 11 AI handoff는 prompt/end-state/preserve/tool support; 21 generated QA는 실제 생성물. 07 lighting 등은 활성 문제에 한해 해당 owner로 보낸다. 새 global SSOT/enum/schema, coordinator, micro-skill, 자동 promotion은 없다.
6. 문서 사례의 source timing, 미래 brief의 제안 timing, 실제 결과의 측정 timing은 서로 다른 근거 상태로 남긴다.
7. 사례 bank는 선택형 참조다. 일반적인 짧은 pointer 외의 상세 inventory는 요청/조건에 따라 progressive disclosure한다.

**설치 포터빌리티 경계:** installed skill-folder 복사본에는 `docs/superpowers/`나 원본 Windows corpus가 있다고 가정하지 않는다. 57개 runtime index entry는 bounded observation, generic mechanism, apply/skip, installed owner destination, QA를 자체 포함한다. 네 worked examples는 깊이 있는 exemplar이지 나머지 coverage를 대체하지 않는다. canonical 57-row source inventory는 이 historical design에만 남고 사례집에는 복사되지 않는다. Provenance는 optional이며 internal owner links는 installed skill folders 안에서 resolve한다.

### 조건부 적용 흐름

| 단계 | 작업 | 완료 관찰 기준 |
|---|---|---|
| 1. 문제 발견 | brief의 정보/행동 문제를 사례 검색어에 대응한다. | 문제 cue가 직접 서술되거나, 해당 사례를 쓰지 않는 이유가 명확하다. |
| 2. 근거 등급 | locator, 저장된 관찰, interpretation, unavailable detail, source time을 읽는다. | 새 브리프 제안과 source fact가 분리되고, unavailable은 unknown으로 유지된다. |
| 3. 조건 및 대안 | 적용 조건과 positive/negative pair를 비교한다. | contact-start 예제에 이미 접촉 중인 opener 반례가 있고, 가려진 발을 full gait 증거로 쓰지 않는다. |
| 4. 기존 owner로 번역 | 기존 canonical template fields에만 필요한 actor/camera/prop/light/edit state를 넘긴다. | 각각 책임 owner가 분리되며 별칭/추가 필드를 만들지 않는다. |
| 5. 제안/미디어 경계 | 새 proposed time과 실제 실행·검수 상태를 보고한다. | 미디어가 없으면 QA는 계획/미검증이며 생성 품질을 통과로 표현하지 않는다. |
| 6. 실제 산출물 검수 | 승인된 생성/미디어가 있으면 기존 generated QA owner가 실제 결과를 검토한다. | 관찰 위치와 실제 실패/통과 근거가 있고, 미검수 범위가 보인다. |

### 기존 필드 계약을 재사용

적용은 기존 owner field를 사용하고, 09의 canonical 열을 그대로 쓴다: `행동·카메라 변화 / 컷아웃→컷인 phase·state + cue time / 컷 이유`; `reaction/settle hold final start–end s·연속성/검수 상태`; elision의 `획득 방식: 연속배속/인터벌/몽타주/의도적 생략/미확인`, `실제 경과시간·촬영 구간·간격·공백(근거 위치)`, `생략 전 상태`, `생략 후 상태`, `후속 컷 유지/리셋 조건`. `before/after/keep`은 이 09 elision 계약의 별칭이 아니며 사용하지 않는다. Worked examples는 06 cue의 다섯 실제 열(Local time (shot seconds), Actor phase / contact / visibility, Camera phase, Reveal / hold, Cut-out → cut-in phase)을 각각 채운다. 추가 owner field는 현재 template에서 확인한 이름만 쓴다.

네 가지 예시는 새 브리프에서 실제 기존 field에 채워 넣는 완성된 illustrative payload다. 아래 timing은 모두 **새 브리프에 대한 상징적 제안**이며 저장 source 타임코드가 아니다. 생성/검수 결과도 아니다. 실제 프로젝트가 사용할 cue와 필드 값은 사용자가 승인한 브리프·기존 template에 맞춰 조정한다.


### 접촉 상태: mouth contact opener와 first touch를 구분

**조건/기준:** `fd2`의 관찰은 close pair가 이미 mouth contact 중인 상태다. 이 proposal은 그 보이는 mouth contact를 opener로 선택한다. 손은 가려져 있을 수 있으며 hand contact의 구체 상태는 불명일 수 있지만, 이는 보이는 mouth contact 자체를 무효화하지 않는다. first-touch를 원하는 별도 brief라면 `d551` 경로를 택하고, near-hair `fb568`는 접촉 증거로 쓰지 않는다.

**새 shot proposal:** shot-local duration 2.0s, 제안된 final timeline interval 12.0–14.0s. 두 인물을 관계가 읽히는 shared composition에 두되 kiss에 손이 필요하다고 가정하지 않는다.

| Local time (shot seconds) | Actor phase / contact / visibility | Camera phase | Reveal / hold | Cut-out → cut-in phase |
|---|---|---|---|---|
| 0.0 | Already in visible mouth contact; hands may be out of frame, hand-contact state unknown. | Steady two-person composition. | Reveal=established mouth contact. | N/A; shot-in already in contact. |
| 1.0 | Contact maintained; receiver gaze shifts if specified by the new brief. | Hold same axis/framing. | Hold response without changing contact type. | N/A; no cut planned. |
| 2.0 | End in same visible mouth-contact state; hand details remain unverified if occluded. | End frame holds pair. | Hold endpoint. | N/A. |

| Owner field | Filled proposal |
|---|---|
| 06 `인물 블로킹` / `시선/축` / `공개 정보` / `관점·감정/구도 의도` | Two actors remain in a shared frame on the established axis. Information = already-established mouth contact, not the first touch. |
| 09 `행동·카메라 변화 / 컷아웃→컷인 phase·state + cue time / 컷 이유` | Action=continuous hold of existing mouth contact; out/in=N/A (no cut); cut reason=N/A. |
| 09 `final_start_s` | `12.0` proposed final time; shot-local `0.0`. |
| 09 `final_end_s` | `14.0` proposed final time; shot-local `2.0`. |
| 09 `reaction/settle hold final start–end s·연속성/검수 상태` | Proposed hold final `13.0–14.0s`; verify mouth-contact visibility and pair continuity in actual output; not generated or verified. |
| QA expectation (not pass evidence) | Verify visible mouth contact is preserved, partner/axis anchors remain consistent, and no unintended hand/face fusion occurs. Hands out of frame mean their contact state is unknown, not that mouth contact is absent. Force, intent and consent are unknown. |

### 도착·정지와 남는 actor 반응

**조건/기준:** `03ab` records approach, spacing narrowing (about 64.4), then stop; its next reaction is not a recorded fact. A stayer response is a new proposal informed by `a600` departure/remaining-actor observations. Shot-local and final time are proposed, not source timing.

**새 shot proposal:** one shared shot, shot-local duration 3.0s; proposed final interval 24.0–27.0s.
| Local time (shot seconds) | Actor phase / contact / visibility | Camera phase | Reveal / hold | Cut-out → cut-in phase |
|---|---|---|---|---|
| 0.0–1.0 | Arriving actor approaches; feet cropped, foot plant unverified. Stayer holds established position. | Shared two-person frame at room anchor. | Approach begins. | N/A. |
| 1.0–1.2 | Arriving actor decelerates; stayer remains. | Hold; no tracking inferred. | Deceleration before stop. | N/A. |
| 1.2–1.3 | Arriving actor stops; stayer remains. | Hold. | Stop becomes legible. | N/A. |
| 1.3–1.5 | Arriving actor settles into final mark; stayer remains. | Preserve both actors and anchor. | Arrival settle. | N/A. |
| 1.8–2.0 | Arriving actor stays settled; stayer begins gaze response. | Maintain shared composition. | Reaction onset, not yet hold. | N/A. |
| 2.0–3.0 | Arriving actor stays settled; stayer holds gaze/reaction. | Maintain shared composition. | Separate stayer reaction hold. | N/A; no cut planned. |

| Owner field | Filled proposal |
|---|---|
| 06 `크기/카메라 위치` / `인물 블로킹` / `시선/축` / `공개 정보` | Medium-wide shared frame at a room anchor; arriving actor approaches from frame-left and stops near table; stayer remains frame-right; reveal arrival then stayer attention. |
| 09 `행동·카메라 변화 / 컷아웃→컷인 phase·state + cue time / 컷 이유` | Action=approach (0.0–1.0)→decelerate (1.0–1.2)→stop (1.2–1.3)→settle (1.3–1.5); stayer response starts at 1.8. Out/in=N/A (one continuous shot); reason=N/A. |
| 09 `final_start_s` | `24.0` proposed final time; shot-local `0.0`. |
| 09 `final_end_s` | `27.0` proposed final time; shot-local `3.0`. |
| 09 `reaction/settle hold final start–end s·연속성/검수 상태` | Arrival settle `25.3–25.5s`; stayer response onset `25.8s`, reaction hold `26.0–27.0s`; verify both remain readable and actor/camera share shot-local timebase after generation. |
| QA expectation (not pass evidence) | Verify arrival and distinct deceleration/stop/settle phases, stayer visibility/response, stable spatial anchor and no axis break. Do not claim full gait or foot plant from cropped feet. The source observation did not include the proposed stayer reaction. |

### Attendants·wardrobe elision·mirror reveal

**조건/기준:** source notes show partial grooming/lacing and attendant work; wardrobe state changes and mirror reveal do not prove complete continuous dressing. This proposal explicitly uses an edit gap between work and finished appearance, rather than presenting omitted preparation as continuous realtime. Shot-local cues, elapsed story time and final timeline values below are proposals.

**새 sequence proposal:** work shot local 0.0–2.0, final 40.0–42.0s; reveal shot local 0.0–2.0, final 42.0–44.0s; the two output shots are adjacent at the edit (work cut-out 42.0 = reveal cut-in 42.0). Actual story-time elapsed and any interval between captured performances remain unknown; no blank output gap is proposed.

| Local time (shot seconds) | Actor phase / contact / visibility | Camera phase | Reveal / hold | Cut-out → cut-in phase |
|---|---|---|---|---|
| Work 0.0–1.0 | Two attendants lean in and work at opposite shoulders; hands visible only where framed. | Medium shared composition; keep actor and both attendants readable. | Work in progress. | Cut out after work state; cut in to prepared appearance after intentional time elision. |
| Work 1.0–2.0 | Attendants withdraw/reposition; main actor stays seated. | Hold shared frame; end actor state=seated. | Work shot settles. | Out=attendants withdrawn/main seated; in=main seated before mirror, finished wardrobe. |
| Reveal 0.0–1.0 | Main actor remains seated; hem enters foreground; reflection begins. | Tilt/reframe only as specified by brief. | Reveal hem/reflection; reflection identity unverified unless anchored. | Cut-in state=finished wardrobe, seated. |
| Reveal 1.0–2.0 | Main actor remains seated, regards mirror; do not imply rising. | Hold mirror and actual actor in same readable composition. | Finished look/reaction. | Cut-out state=seated finished look; next state must preserve or explicitly change posture. |

| Owner field | Filled proposal |
|---|---|
| 06 `인물 블로킹` / `종료 프레임` / `공개 정보` | Work shot: main actor seated center; attendants at opposite shoulders, then withdraw. Reveal shot: same actor remains seated before mirror; hem and reflection enter; end frame maintains actor/mirror relation and seated state. |
| 09 `획득 방식: 연속배속/인터벌/몽타주/의도적 생략/미확인` | `의도적 생략` between the work and reveal shots. This is an edit gap, not continuous realtime. |
| 09 `실제 경과시간·촬영 구간·간격·공백(근거 위치)` | Actual story-time elapsed and capture gap=`unknown/not measured`; output shots are adjacent at final 42.0s. Saved locators: `03ab` grooming/lacing and mirror reveal; `2464`/`9e0` changed appearance states. |
| 09 `생략 전 상태` | Main actor seated; attendants withdrawn; work in progress/unfinished appearance as brief specifies. |
| 09 `생략 후 상태` | Same actor seated before mirror in finished, brief-approved wardrobe. |
| 09 `후속 컷 유지/리셋 조건` | Preserve actor identity, seated posture, approved wardrobe and prop ownership; any posture/prop change must be explicit in the next shot. |
| QA expectation (not pass evidence) | Check both main actor and reflection are readable; ground reflection identity from the new brief; check attendants do not fuse with actor/hands, wardrobe persists after adjacent cut, and mirror framing does not imply a posture change. |

**09 cut-row illustration:** `W1` and `W2` below are document-local example labels only, not production cut IDs. The rows show adjacent output cuts; they do not assign an elapsed story-time interval.

| cut_id | final_start_s | final_end_s | 행동·카메라 변화 / 컷아웃→컷인 phase·state + cue time / 컷 이유 | reaction/settle hold final start–end s·연속성/검수 상태 |
|---|---:|---:|---|---|
| W1 | 40.0 | 42.0 | Work/withdrawal; out at 42.0=attendants withdrawn, actor seated; reason=omit unshown preparation. | N/A; no reaction hold in this work shot. |
| W2 | 42.0 | 44.0 | Mirror/hem reveal; in at 42.0=same actor seated, finished wardrobe; reason=disclose finished look after intentional elision. | Proposed reveal hold 43.0–44.0s; verify finished wardrobe state, seated posture, mirror relation/reflection continuity and no unintended identity duplication. Not generated/verified. |

### Magic object·continuous effect와 witness response

**조건/기준:** `a600` records a within-shot action chain; candidates 15–28 are one event. This is a new brief proposal and does not assert physical magic, exact source technique or supported generation endpoint.

**새 shot proposal:** shot-local duration 3.0s; proposed final interval 70.0–73.0s; one continuous shot, with actor hand, cup, trajectory landmarks, impact area and witness readable.

| Local time (shot seconds) | Actor phase / contact / visibility | Camera phase | Reveal / hold | Cut-out → cut-in phase |
|---|---|---|---|---|
| 0.0–0.5 | Actor gestures; cup remains held; fingers/cup separation visible. | Locked three-quarter view; empty trajectory lane visible. | Gesture. | N/A. |
| 0.5–1.0 | Glow appears; cup still held. | Hold frame. | Glow reveal. | N/A. |
| 1.0–1.5 | Cup separates; hand remains visible, cup identity/count tracked. | No unmotivated pan. | Separation readable. | N/A. |
| 1.5–2.0 | Cup travels past harp/statue/window landmarks toward impact. | Keep origin, path and destination legible. | Trajectory reveal. | N/A. |
| 2.0–2.5 | Impact and fragments; witness begins response. | Maintain geography. | Impact/result. | N/A. |
| 2.5–3.0 | Fragments settle; witness reaction held. | Hold end composition. | Settle and reaction. | N/A; same shot ends after hold. |

| Owner field | Filled proposal |
|---|---|
| 06 `크기/카메라 위치` / `카메라 동작` / `종료 프레임` | Locked three-quarter view; no camera move; end frame shows resulting fragments and witness in same geography. |
| 06 `핸들` | Proposed 0.25s pre-roll and 0.5s post-roll around the 3.0s action for edit handles; values are brief proposals, not model guarantees. |
| 06 cue `Reveal / hold` | Gesture→glow→separation→trajectory→impact→fragments/witness; hold settled result from shot-local 2.5–3.0s. |
| 06 `Cut-out → cut-in phase` | `N/A; one continuous proposed event, not a cut sequence.` |
| 11 `도구 지원 확인` | `UNKNOWN` until the applicable endpoint is checked; this belongs to AI handoff, not a 06 shot field. |
| 09 `행동·카메라 변화 / 컷아웃→컷인 phase·state + cue time / 컷 이유` | Action=continuous effect phases; no cut inferred from glow/blur/travel; out/in=N/A (one continuous shot); reason=N/A. |
| 09 `final_start_s` | `70.0` proposed final time; shot-local `0.0`. |
| 09 `final_end_s` | `73.0` proposed final time; shot-local `3.0`. |
| 09 `reaction/settle hold final start–end s·연속성/검수 상태` | Witness/fragment hold `72.5–73.0s`; verify count, trajectory, impact result, persistence and witness response in actual output; not generated or verified. |
| QA expectation (not pass evidence) | Check cup count and separation, continuous origin-to-destination path, impact result/fragments persistence, readable witness response, and no spatial jump. Do not treat flare as focus pull or visual effect as physical material proof. |

## 적용 acceptance criteria 및 마일스톤

| 구간 | 산출물 | 완료 조건 |
|---|---|---|
| A. 기존 계약 확인 | 25 분석 진입점, owner references/templates의 최소 변경안 | owner와 canonical field가 실제 파일에서 확인되고, 25 entry/router 유지와 저장 사례 재사용 시 fresh inspection 불필요가 명시되며 대체 절차/스키마가 없음. |
| B. 조건별 사례 | `video-production-assets/references/rofan-craft-examples.md` 및 25 pointer | 구현됨: 57개 ID를 problem cue / bounded observation / generic mechanism / apply-skip / owner / QA로 검색하며 원문 57-row table은 복사하지 않음. |
| C. 실제 파일 적용 | 기존 skill entry, 06 step 3, 25 transfer pointer, 사례집 | 지정된 문서 적용 완료; 25 entry/router와 A01–A12 및 owner field ownership 유지. |
| D. 문서·copied-package 검증 | 변경 문서 구조/링크 및 frozen reader suite | [테스트 계획](../../implementation/2026-10-12-rofan-craft-skill-test-plan.md), [T12 원문](../../../qa/rofan-craft-green-final-t12-run.json), [package smoke](../../../qa/rofan-craft-package-smoke.json)에 actual results 기록. Version check passed (2.5/23); pytest exited 0 (258 passed, 1 skipped, 2 warnings, 217 subtests); isolated 23-skill package, 57 exact C12/P17/O10/L9/E9 IDs and 384/384 relative links checked. Reader grade: 15 PASS, 1 PASS_WITH_CONTEXT_LIMIT, 2 PARTIAL_NOT_MET, 0 guard failures; reader 07 lacks concrete bounded-excerpt transfer, and composite lacks canonical 09 elision row and explicit EOS/container-tail check. This is not all-pass. |

적용 후에도 “성능이 좋아졌다”는 수치 주장은 별도 승인된 평가·근거 없이는 하지 않는다. source 관찰 항목의 목록 완결성만으로 생성 결과의 자연스러움, 제어 가능성, 일반화가 증명되지 않는다.

## 위험과 대응

| 위험 | 대응 |
|---|---|
| local locator를 완전한 원본 식별자로 오인 | source prefix만 쓰고 full ID/title/rig/lens를 만들지 않음; locator는 plain code. |
| 분석 요약을 직접 미디어 검수로 오인 | 표제/문장에 saved historical analysis 및 no fresh inspection을 명시. |
| sample cutscene를 universal rule로 일반화 | 조건과 반례를 함께 둠; 30초 제한/first-touch/wide-first/gait 수치 금지. |
| 접근 불가 상세를 추론해 복원 | 정확한 접근성 제한 기록; counts로 본문을 재구성하지 않음. |
| 새로운 중복 시스템 도입 | 기존 owner, schema, SSOT, routing만 사용. |
| plan-only를 production QA pass로 오인 | 설계 제안과 실제 미디어 상태를 별도 보고; 실제 결과가 없으면 미검증. |

## 상태 보고 경계

이 문서와 적용 계획은 설계·구현 경계와 근거를 기록한다. 지정된 skill/reference 문서 적용은 끝났으며 copied-package test는 별도 test plan/operator evidence를 따른다. README와 CHANGELOG는 이를 가리킨다. 실제 생성/미디어 QA/생성 품질은 입증하거나 주장하지 않는다.