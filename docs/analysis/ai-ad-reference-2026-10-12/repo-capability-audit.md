# 광고 레퍼런스 개선: 저장소 역량 근거 감사

## 범위·판정

설계 전용이다. 기존 스킬·코드·manifest를 변경하지 않았다. 정본은 저장소 manifest v2.5의 23개 bundled skills(`manifest.json:3-30`)다. 설치 `.codex` 스킬은 기준선이 아니다. reference-intake는 조사 절차용 외부 가이드이며 번들 기능으로 세지 않는다. 외부 story-commerce/audio 실행기 역시 `manifest.json:65-87,149-163`의 선택 의존성이지 구현 완료 증거가 아니다.

295개 SKILL.md/references/assets/evals/support 파일을 경로·바이트·SHA-256·mtime_ns·줄 수로 인벤토리화했다. 인벤토리 전수와 본문 전권 정독은 다르다. 아래 판정은 정확히 읽은 핵심 계약과 저장소 범위 키워드 탐색을 근거로 한다. JSON에는 실제 파일 인벤토리와 판정마다 탐색 범위·근거 줄을 보관한다.

PRESENT는 요청 축에 실행절차/인계/검수 조항이 있다는 뜻이지 영상 생성 또는 성과 검증을 뜻하지 않는다. PARTIAL은 일반 계약은 있으나 특정 광고의 재사용 가능한 상세 레시피 후보를 비교할 여지가 있다는 뜻이다. NOT_FOUND는 범위 내 특정 조항의 미발견이지 해당 분야 전체가 없는 뜻이 아니다. 영상 노동자가 제공할 실제 scene/cut 증거 전에는 갭 후보를 확정 개선안으로 승격하지 않는다.

집계: PRESENT 19 / PARTIAL 5 / NOT_FOUND 1 (총25).

## 분야별 근거 지도

|ID|축|상태|직접 관찰 및 정확한 근거|조건부 확장 경계|
|---|---|---|---|---|
|C01|감독·스토리·광고 약속|PRESENT|관점·정보 공개·힘 관계·제품증거와 관객 문제·한 문장 약속을 연결한다. `video-production-assets/references/06-shots.md:10-19`; `video-production-assets/references/13-ideation-brand.md:4-11`|없음 |
|C02|소비자 설득·브랜드|PRESENT|품질 시연·조건·한계·고지·CTA 다음 경험·강압 금지 포함. `video-production-assets/references/13-ideation-brand.md:8-11`; `creative-production/references/marketing-source-adaptation.md:7-15`; `video-production-assets/references/19-brand-product-integration.md:9-22`|없음 |
|C03|페르소나·음성 정체성|PRESENT|행동·선택·비용과 voice identity/speech/per-line performance를 분리한다. `designing-character-personas/SKILL.md:36-58`|없음 |
|C04|배우 연기·듣기|PRESENT|행동동사·자극 반응·전술 전환·생각→목표→행동→결과. `video-production-assets/references/04-performance.md:9-16`|없음 |
|C05|블로킹·시선·접촉|PRESENT|축·소유·행동정점·지지/중력/주접촉 우선. `video-production-assets/references/06-shots.md:11-19`; `video-production-assets/references/21-generated-video-qa-retry.md:7-28`|없음 |
|C06|촬영·렌즈·카메라 타이밍|PRESENT|공통 시간 기준·병진/회전/줌/초점 구분·렌즈와 거리·미지원 경계. `camera-spatial-design/references/motion-timing-lens.md:4-18`|없음 |
|C07|광학 역추정 불확실성|PRESENT|정규화 기준점·여러 후보 해·크롭 제약·반증 증거까지 있음. `video-production-assets/references/25-reference-video-analysis.md:34-44`|없음 |
|C08|조명·빛 크기·연속성|PRESENT|동기·키필 분리·상대 크기/거리·그림자 경도·역방향 연속성. `video-production-assets/references/07-lighting.md:9-17`|없음 |
|C09|색·시각 구조|PRESENT|7시각요소·대비/유사성·비보편적 색 의미·샷 매칭과 제품 보호. `video-production-assets/references/05-visual.md:9-17`; `video-production-assets/references/23-finishing-platform.md:11-23`|없음 |
|C10|제품·재질·팩샷|PRESENT|SSOT·유광/반투명/크림액체/금속/피부 조명·히어로/매크로/팩샷·합성 공간통합. `video-production-assets/references/19-brand-product-integration.md:39-55`|없음 |
|C11|반사 형상 정밀 레시피|PARTIAL|반사환경·길게 통제된 하이라이트·환경 반사 검수는 있음. `video-production-assets/references/19-brand-product-integration.md:46-52`; `video-production-assets/references/21-generated-video-qa-retry.md:35-46`|반사 카드/광원 형상→표면 하이라이트 궤적→카메라각 변화별 보존을 연결한 광고별 레시피는 현재 읽은 일반 조항보다 상세하다. 관련 광고의 실제 프레임/움직임에서 이 문제가 확인될 때 19/07/21 심화; 새 조명 스킬 불필요.|
|C12|식품·액체 누적 상태|PRESENT|익음·변색·붓기·접촉·잔류결과·유체 합성 포함. `video-production-assets/references/26-state-causality-continuity.md:11-19`; `video-production-assets/references/26-state-causality-continuity.md:39-43`; `video-production-assets/references/21-generated-video-qa-retry.md:7-20`|없음 |
|C13|식품 미감·상태별 시연 레시피|PARTIAL|재질/상태/후속유지 일반계약은 충분히 있다. `video-production-assets/references/19-brand-product-integration.md:43-54`; `video-production-assets/references/26-state-causality-continuity.md:26-32`|먹을 수 있는 단면·표면·김/응결·중량/점성/충격의 광고별 공개 시퀀스와 반례를 묶은 재사용 사례는 별도 후보. 실제 식품 영상 증거가 있을 때 19/26/21의 사례 확장; 물리값 역추정 금지.|
|C14|차량 광고 전용 운행 안전·바퀴 위상 레시피|NOT_FOUND|일반 관성·접촉·추적카메라 계약은 있음. 차량 전용 노면/바퀴회전/차체반사/운행안전 인계 조항은 scoped text 검색에서 발견하지 못함. 20에는 군중 공간의 차량 안전 논리·관통·규모단서도 이미 있다; 본 판정은 차량 광고 전용 바퀴/노면 위상 계약에 한정. `video-production-assets/references/21-generated-video-qa-retry.md:7-28`; `camera-spatial-design/references/motion-timing-lens.md:7-15`; `video-production-assets/references/20-visual-mode-ssot.md:112-121`|차량 전용 조항의 부재이지 차량 영상을 만들 기능 전체의 부재 아님. 차량 장면이 실제 포함되고 일반 모션/제품 계약으로 설명 못하는 실패가 확인되면 심화; 독립 전문 스킬은 별도 소유 계약이 필요할 때만.|
|C15|건축·장소 지리|PRESENT|4공간뷰·출입/창/장애물/광원 앵커·마스터/파생 계보. `camera-spatial-design/SKILL.md:32-37`; `video-production-assets/references/contract.md:111-118`|없음 |
|C16|건축 공개 시퀀스·공간 전환 레시피|PARTIAL|관점·주목점·깊이·동일 특징 대응은 있음. `video-production-assets/references/06-shots.md:11-19`; `video-production-assets/references/25-reference-video-analysis.md:38-44`|외관→문턱→실내→시설의 공간지리 읽힘과 비가능 공간 점프 반례를 묶은 장르별 레시피는 조건부 후보. 관련 건축 영상의 실제 공개 순서가 증명될 때 06/25 또는 camera-design 사례를 확장.|
|C17|세계·에셋 연속성|PRESENT|활성 LOOK 하나·정확 버전핀·후속 재등장/리셋/가림 구분. `video-production-assets/references/contract.md:111-130`; `video-production-assets/references/26-state-causality-continuity.md:18-33`|없음 |
|C18|편집·전환·시간 압축|PRESENT|J/L컷·감정/신체/사건 리듬·배속/인터벌/몽타주/생략 구분. `video-production-assets/references/09-edit.md:9-17`; `video-production-assets/references/09-edit.md:28-42`|없음 |
|C19|매치컷 지각 대응 레시피|PARTIAL|시선유도·action phase 컷 경계·전환 길이 기록은 있음. `video-production-assets/references/09-edit.md:10-17`; `video-production-assets/references/25-reference-video-analysis.md:18-22`|형상/색/화면위치/벡터/재질/소리 가운데 무엇을 맞추고 무엇을 의도적으로 바꾸는지 분리한 레시피 카드 후보. 실제 경계 양쪽 프레임·재생 증거 있을 때 09/25 심화. 키워드 부재만으로 매치컷 기능 부재 판정 금지.|
|C20|음악·VO·Foley·싱크·권리|PRESENT|큐 레이어·소스/최종구간·gain/fade·sync offset·청취·권리 근거·침묵 포함. `video-production-assets/references/09-edit.md:45-83`; `video-production-assets/references/09-edit.md:111-124`|없음 |
|C21|타이포·엔드카드·CTA|PARTIAL|철자/로고/안전영역·요청된 CTA 문구/길이·실제 읽기 QA 있음. `video-production-assets/references/23-finishing-platform.md:19-20`; `creative-production/references/marketing-source-adaptation.md:34-58`; `video-production-assets/references/19-brand-product-integration.md:9-9`; `video-production-assets/references/19-brand-product-integration.md:45-52`|광고별 타이포 motion onset/settle/읽기 hold/팩샷/음성 약속 일치의 재사용 레시피를 체계화할 여지. 실제 텍스트·최종 크기·타이밍 증거로 필요 확인; CTA 없는 브리프에 강제하지 않음.|
|C22|아카이브 전수 분석·coverage ledger|PRESENT|stable archive_id·6모드·추출≠검토·연속재생≠청취·cross-video gap 분류 이미 있음. `video-production-assets/references/25-reference-video-analysis.md:47-68`; `video-production-assets/assets/archive-audit-template.md:14-27`|없음 |
|C23|재사용 메커니즘 이전 체인|PRESENT|증거→메커니즘→해석 효과→새브리프 요구→정성 QA 이미 있음. `video-production-assets/references/25-reference-video-analysis.md:58-64`; `video-production-assets/assets/shot-dna-template.md:50-55`|없음 |
|C24|QA·실패 반례·최소 수리|PRESENT|실패 클래스·원인/수리/보존/재검수·예산·실제 전체 재생 게이트. `video-production-assets/references/21-generated-video-qa-retry.md:48-158`; `video-production-assets/references/12-qa.md:9-16`|없음 |
|C25|구조 검사와 작품/권리 판정 경계|PRESENT|구조 pass는 예술/권리/수락 인증 아님. 점수 평균으로 blocker 숨기지 않음. `video-production-assets/references/contract.md:47-52`; `video-production-assets/references/12-qa.md:36-51`|없음 |

## 이미 구현된 것을 결손으로 다시 만들지 말 것

- reference25:47–64와 archive-audit-template:14–27에는 전수 인벤토리·stable archive_id·모드별 커버리지·교차영상 대조·이전 체인이 이미 있다. “아카이브 감사 스킬 없음”은 오판이다.
- reference19:39–55에는 제품 SSOT·재질별 광원·액체 레이어·팩샷·손 접촉·승인 아트워크 합성의 원근/반사/그림자 통합이 있다. “제품/재질/조명 스킬 없음”은 오판이다.
- reference04:9–16의 행동동사·듣기·자극 반응과 reference08:9–17의 포즈/무게/timing/spacing은 연기·애니메이션 기본 계약이다. 새 이름으로 중복 분리하지 않는다.
- reference09:45–83의 음원 계층/싱크/권리와 reference21:93–104의 전체 시퀀스 재생은 표본 이미지나 파형만으로 충족되지 않는다.

## 평가·계약 현황과 구체적 QA 위험

7개 eval JSON이 실제 존재한다(전체 경로·파일 지문은 repo-capabilities.json). 읽은 핵심 사례: creative-production/evals/evals.json:41–58(광고 혼합오디오/전체재생 경계),96–99(권리),114–117(아카이브); designing-character-personas/evals/evals.json:87–105(비지원 제어·stale 핀); storyboarding-video/evals/evals.json:41–62(전체보드·접촉누락 수리); developing-video-synopses/evals/evals.json:29–36(비서사/noCTA); orchestrating-video-preproduction/evals/evals.json:28–35(제품/noCTA/미실행); designing-video-character-sheets/evals/evals.json:17–25(고객 주인공·주장 금지); storytelling-with-still-images/evals/evals.json:19–28(음성 길이와 스틸 hold). 파일 존재와 기대조건은 확인했지만 평가를 실행하지 않았으며 합격률을 주장하지 않는다.

**관찰된 불일치:** creative-production/evals/evals.json:117의 archive 기대조건은 ‘archive-wide inventory/cross-video synthesis가 uncovered일 때만’이라는 과거 갭 가정을 남긴다. 현재 reference25:47–56 및 archive-audit-template:14–48과 대조하면 신규 결과가 이것을 미구현으로 오판할 위험이 있다. 기존 파일은 수정하지 않고 다음 설계 QA의 회귀 반례로 기록한다. 실제 테스트 결과를 본 것은 아니다.

공통 계약 reference contract:47–52는 plan/preproduction/delivery 검사와 실제 재생·음량·권리·수락 인증을 명시적으로 구분한다. 111–130의 LOOK·계보·정확버전·FINAL gate를 재사용하고 병렬 SSOT/새 전역 JSON을 제안하지 않는다.

## 후속 설계자의 채택 조건

각 PARTIAL은 영상 ID+정확 경계/프레임+실제 검사 모드→구체 메커니즘→현재 supporting/restricting clause→충족되지 않는 최소 작업→수리/보존/반례→검증 기준을 연결해야 한다. 우선 기존 05/06/07/09/19/21/25/26 또는 camera-design 참조를 깊게 한다. 새 specialist는 독립 입력/출력·소유권·라우팅이 실제로 필요하고 기존 담당에서 해결하지 못함이 입증될 때만 정당화한다. 이 문서는 reusable skill contract 자체를 새로 구현하지 않는다.

## 수행한 증거 QA

Python 인메모리 점검으로 manifest 23개·인벤토리295개·capability25개 상태합계와 인용 경로/줄 범위를 확인했다. 인벤토리 기준 지문을 최종 후보 작성 직전에 다시 비교한 결과 변경 파일 0이었다. 이후 동시 변경 가능성은 남으므로 설계 병합 시 JSON 지문/mtime와 현재 파일을 비교해야 한다. 프로덕션 빌드/평가/렌더는 실행하지 않았다.
