# 영화 제작 라이프사이클 스킬 확장 설계

## 상태와 목적

- 상태: **구현 완료 — README 및 총괄/전문 스킬 진입점 반영; 검증 통과, 형식 리뷰·Ultragoal 체크포인트 대기**. `python -X utf8 -m pytest -q` 258 tests +217 subtests (2 Windows subprocess UTF-8 warnings), targeted validators 57 tests +145 subtests, 14개 텍스트/인스트럭션 시나리오와 변경 Markdown의 247개 상대 링크 및 9개 템플릿 표 폭 검사를 통과했다. 검증은 텍스트/저장소 기준이며 미디어/프로바이더 실행이나 형식 코드 리뷰 승인을 의미하지 않는다.
- 목적: 기존 영상 제작 스킬을 영화 제작의 기획부터 배급까지 이어지는 선택형 라이프사이클로 보완한다. 첨부에서 확인된 갭을 기존 스킬 소유권·프로젝트 계약에 맞춰 구체화한다.
- 대상: `video-production-assets` 및 `creative-production`의 영화/단편/애니메이션/AI 영화 제작 흐름. 광고·설명 영상 등 비영화 작업은 현재 동작을 유지한다.
- 근거: `video-production-assets/SKILL.md`, 해당 `references/01-brief.md`, `02-story.md`, `03-screenplay.md`, `06-shots.md`, `09-edit.md`, `11-ai-handoff.md`, `14-production-ops.md`, `15-delivery.md`, `references/contract.md`, `creative-production/references/production-routing.md` 및 2026-10-11 사용자 첨부.

## 문제 정의

현재 스킬은 브리프·서사·각본·스토리보드·샷·생성형 영상 연속성·일정/예산·편집/사운드·자막/납품에 강하다. 하지만 영화의 6단계를 연결하는 공통 경로가 없고, 개발 문서(프레미스/테마/스토리/플롯/시놉시스/트리트먼트/피치), 촬영 현장 운영, 전체 후반작업 상태, 배급 패키지의 계약과 완료 기준이 흩어져 있거나 빠져 있다.

설계가 해결할 문제는 모듈 수를 늘리는 것이 아니라, 해당 작업에 필요한 문서와 단계 간 인계를 선택하게 하고, 계획·실제 제작·승인·최종 납품의 상태를 기존 원장으로 추적하게 하는 것이다.

## 결정 요약

| 결정 | 설계 |
|---|---|
| 소유권 | 기존 `video-production-assets` 안에 영화 라이프사이클 참조를 추가한다. 새 영화 전용 조정자/스킬이나 경쟁 파이프라인은 만들지 않는다. |
| 진입점 | `creative-production`은 명시적 영화/단편 요청에 한해 라이프사이클 경로를 선택하고, 현재 단계와 요청 산출물만 담당 모듈에 위임한다. 기존 단일 산출물/비영화 라우팅은 유지한다. |
| 단계 구조 | Development, Screenwriting, Pre-production, Production, Post-production, Distribution의 6단계를 상위 탐색 구조로 둔다. 단계는 겹칠 수 있고, 매체·길이·제작 방식·요청에 따라 N/A 또는 통합할 수 있다. |
| 정본 | `project.json`, artifact/dependency/version/approval/asset_registry 및 기존 이력 규칙을 재사용한다. 새 DB, 전역 승인 원장, 필수 스키마 확장은 만들지 않는다. |
| 문서 정책 | 산출물은 전부 생성하지 않는다. 간단한 단편은 최소 패키지를 선택하고, 미적용 항목은 N/A와 이유, 미확인 항목은 unverified로 둔다. |
| 실행 경계 | 계획·스토리보드·타임라인은 촬영·렌더·편집·배급 실행이 아니다. 실제 미디어 작업, 권리 승인, 비용, 게시에는 기존의 별도 승인 게이트를 유지한다. |

## 범위 및 비목표

**포함**
- 6단계 흐름과 단계별 목적, 입력/출력, 의존관계, 종료/인계 기준.
- 영화 개발 및 각본 산출물의 구분과 선택 규칙.
- 현장 기록·후반작업·배급 산출물의 최소 추적 필드 및 검수 기준.
- 기존 스킬·참조·템플릿·라우팅에 적용할 파일 단위 구현 경계와 수락 시나리오.
- AI 영화에서 기존 SSOT/상태/샷 프롬프트/생성 QA 규칙을 라이프사이클 단계에 연결.

**비목표**
- 영화 제작 전용 데이터베이스, 새로운 상태 머신/프로젝트 스키마, 자동화 엔진 또는 새 조정자.
- 촬영, 편집, 믹싱, VFX, DCP 생성, 영화제 출품, 유통 계약, 공개 게시를 자동 수행.
- 모든 프로젝트에 장편 영화식 문서·구조를 강제하거나 모든 이야기에 3막/5막을 강제.
- 법률 판단, 저작권 허가 인증, 예산·일정·관객 성과의 사실이 아닌 추정치.
- 기존 `storyboarding`/카메라/Blender/생성 실행 전문 스킬의 소유권을 가져오는 것.

## 라이프사이클과 계약

| 단계 | 핵심 질문 | 선택 가능한 산출물 | 다음 단계로 넘어갈 최소 조건 |
|---|---|---|---|
| 01 Development | 무엇을 누구에게 왜 제안하는가? | 아이디어, 콘셉트, 프레미스, 테마, 장르/톤, 세계관, 스토리, 플롯 아웃라인, 제작용 시놉시스, 캐릭터/관계, 리서치, 트리트먼트, 피치덱 | 사용자가 승인/위임한 핵심 이야기 방향, 범위와 미확인 전제 표시. 기획 전부를 채울 필요 없음. |
| 02 Screenwriting | 이야기를 어떤 장면·행동·대사로 구현하는가? | 스토리/캐릭터 아크, 비트시트, 시퀀스 아웃라인, 씬 아웃라인, 시나리오, 서브텍스트/연기 메모, 리라이트 노트 | 선택된 각본 버전이 식별되고 씬/캐릭터/비트 ID가 필요한 하위 산출물과 연결됨. |
| 03 Pre-production | 각본을 제작 가능한 시청각 계획으로 바꾸었는가? | 감독 트리트먼트, 비주얼 바이블/룩, 콘셉트 아트, 스토리보드, 샷리스트, 애니매틱/프리비즈, 블로킹/카메라/조명/사운드 플랜, 브레이크다운, 캐스팅/로케이션, 예산/일정, 허가·안전·연속성 계획 | 실행에 필요한 버전·자원·권리/안전 blocker가 확인되고, 실제 제작 계획과 미정 항목이 구분됨. |
| 04 Production | 계획된 장면을 실제로 기록했는가? | 촬영/생성일지, 씬·샷·테이크 로그, 스크립트 슈퍼비전/연속성 기록, 데일리 리뷰, 미디어 백업·무결성 기록 | 관찰된 실제 촬영/생성 결과만 등록, 선택 테이크·미완료/재촬영 항목을 식별하고 원본 보존 상태를 기록. |
| 05 Post-production | 촬영물을 의도된 최종 시청각 경험으로 완성했는가? | 인제스트/싱크, 어셈블리·러프·파인 컷, 픽처 락, VFX, ADR/Foley, 사운드·음악, 믹스, 그레이딩, 자막/크레딧, 마스터·QC | 최종 타임라인/사운드/그레이드/자막 버전과 검사 증거가 실제 파일에 연결되고 열린 blocker가 표시됨. |
| 06 Distribution | 승인된 최종본을 지정 관객/플랫폼에 전달할 준비가 되었는가? | 키아트/포스터, 티저/트레일러, EPK, 영화제 제출 기록, 배급·권리 범위, 목적별 마스터/자막/음향 납품, 공개 후 관객 피드백 | 목적지별 납품 규격·파일·권리 상태·검수 및 실제 제출/공개 상태를 구분. 계획은 제출/배급 완료로 간주하지 않음. |

단계 간 동시 진행은 허용하되 산출물의 dependency/version을 기록한다. 상위 입력 변경 시 실제 의존 artifact만 stale 처리한다. 촬영 순서는 스토리 순서와 분리해 별도 촬영 순서로 기록한다.

## 첨부 항목 전수 대조표

아래 표는 첨부의 항목을 설계에서 다루는 위치와 기존 소유 모듈에 연결한다. “기존 계약 재사용”은 현재 스킬에 해당 절차가 이미 있음을 뜻하고, “보강”은 영화 라이프사이클에서 다시 연결하거나 빠진 추적 기준을 설계한다는 뜻이다.

| 단계/항목 | 대조 결과 및 소유 위치 |
|---|---|
| Development: idea, concept, premise, theme, logline | 보강 — 01 brief + 28 lifecycle. 요청에 맞춰 선택. |
| Development: genre, tone/mood, worldbuilding, story, plot | 보강 — 01/02 + 스타일·세계관 바이블. story와 plot은 별개 문서 의미로 유지. |
| Development: synopsis, character, relationship map, research, pitch deck | 보강 — 01/02/03에서 해당 산출물과 출처·버전 인계 규칙 연결. 피치덱은 요청 시 기획 패키지로 선택. |
| Research requirements | 질문/주장, 자료 locator·출처와 확인 시점, 검증된 관찰과 해석의 구분, 라이선스/사용 제한을 연결한다. 출처가 있다는 사실만으로 검증 완료나 재사용 허가로 보지 않는다. |
| Screenwriting: story/character arc, 3-act/5-act, beat/beat sheet, sequence, scene | 보강 — 02/03. 3막·5막은 선택 구조이며 모든 작품에 강제하지 않음. 샷은 서사 단위와 별개. |
| Screenwriting: scene outline, script, subtext, rewrite | 보강 — 03 + 기존 performance/scene craft 경로. 씬별 목표·갈등·전환·감정 이동·정보 공개는 검토 질문으로 사용하고 자동 필수 필드는 아님. |
| Beat / act / sequence distinction | 비트는 행동·감정·상황의 의미 있는 변화, 비트시트는 주요 비트의 순서와 인과를 기록한다. 막/시퀀스는 하위 씬을 묶으며 샷은 촬영·편집 단위다. 비선형/실험 작업은 해당 구조가 유용할 때만 적용한다. |
| Preproduction A: director's treatment, visual bible, moodboard, concept art | 보강 — 01/05와 라이프사이클. 감독의 해석과 프로젝트 시각 기준을 구별. |
| Preproduction A: storyboard, shot list, animatic, previs, blocking, camera plan | 기존 계약 재사용 + 보강 — 06, storyboard contract, 08, 27 및 camera-spatial-design/Blender 연결. 스토리보드(시각 설명), 실행 샷리스트(기술/촬영 지시), 애니매틱(시간축/임시 소리), 3D 프리비즈(공간 검증)의 목적을 혼동하지 않음. |
| Preproduction B: script breakdown, casting/auditions, location scouting, production design, wardrobe/makeup | 보강 — 14의 역할/장소/자원 계획에 항목별 준비·상태·담당·근거 연결. 기존 스킬에 없는 전문 평가/캐스팅 실행을 완료했다고 주장하지 않음. |
| Preproduction B: lighting, sound design plan, budget, shooting schedule, continuity log | 기존 계약 재사용 + 보강 — 07/09/14, continuity ledger. 이야기 순서와 장소·배우·조명 세팅 기준 촬영순서를 분리. |
| Preproduction additional: crew, contracts, likeness/music/location rights, insurance, risk assessment, equipment tests | 보강 — 14의 준비 blocker/checklist 및 권리 provenance. 책임자 확인·외부 법률 검토가 필요한 상태를 표시; 스킬이 허가나 보험을 승인하지 않음. |
| Production preparation checks | crew/role, 계약/동의, 촬영 허가·음악/초상권, 보험, 위험평가, 장비/워크플로 테스트를 프로젝트별 적용/비적용/미확인으로 기록한다. 책임자, 근거 locator, 범위/만료, blocker를 표시하며 체크만으로 법적·안전 승인을 선언하지 않는다. |
| Production: acting direction, mise-en-scène, framing, camera work, focus/DOF, lighting operation | 기존 전문 설계 재사용 — 04/05/06/07/08 및 camera-spatial-design. 실제 현장 운용/포커스·조명 상태는 촬영 로그에 관찰 결과로 기록하며 설계 문서만으로 실행 완료 판정하지 않음. |
| Production: sync sound, takes, script supervision, dailies, media backup/integrity | 보강 — 14와 신규 현장 기록 양식 검토 대상. take별 원본/선택·연속성·검토·백업을 실제 확인 근거와 연결. |
| Continuity checks | 인물의 동작/시선·화면 방향, 소품의 손/위치/상태, 의상·분장, 조명/공간 상태를 씬·샷·테이크 간 비교한다. 의도적 변화는 원인/승인된 연출 의도로 기록하고 설명 없는 불일치는 수정/재촬영 대상으로 남긴다. 이야기 순서와 실제 촬영 순서는 분리한다. |
| Post: ingest/sync, assembly/rough/fine cut, picture lock | 보강 — 09/23 및 신규 후반 단계 추적. 각 컷 버전의 입력/승인 의존성 기록. |
| Post: VFX, ADR, Foley, sound design, score, mix, grade | 기존/조건부 전문 작업 + 보강 — 09/22/23, 요청된 실제 도구·스킬로 인계. 선택된 항목만 작업하고 계획과 실제 결과를 구분. |
| Post: captions/credits, mastering/QC | 기존 delivery/QC 재사용 + 보강 — 12/15/23. 실제 파일 재생·청취·규격 검사를 통과 증거로 남김. |
| Distribution: key art/poster, teaser/trailer, EPK | 조건부 보강 — 실제 asset/file이 있으면 delivery package에 등록. 제작 계획과 미디어 완성본을 구분. |
| Distribution: festival eligibility/deadlines, distribution strategy, rights, final deliverables, audience response | 보강 — 목적지별 체크리스트/기록을 15와 연결. 자격·마감·계약은 공식/사용자 제공 근거를 확인하고 실제 제출·공개·피드백과 계획을 분리. |
| Project folder structure | 선택형 논리 구획으로 지원하되 기존 `package_production.py`의 `00_MANIFEST`–`10_DELIVERY` 패키지 레이아웃을 대체하지 않음. 아래 폴더 대응 규칙 참조. |
| AI production additions | 기존 11/20/21/26 및 v5.1 계약 재사용 — 캐릭터 아이덴티티/SSOT, scene state, reference assets, shot prompt, start/end frame, model/version, result QA, retries, rights provenance. 연속성 검수는 shot 단독이 아니라 연결된 씬/시퀀스 단위도 포함. |
| 30-second short deliverables | 프로필 표에 명시한 추천 최소 12개를 적용. 애니매틱은 필요 시, 캐릭터 시트는 등장인물이 있을 때, QC는 실물 납품 시 실제 파일에 적용. |

전역 완료 검토는 세 축을 각각 분리해 기록한다: **내러티브 일관성**(인과·인물·감정), **시청각 일관성**(정체성·공간·동작·소리), **제작 추적성**(버전·승인·출처·산출물·실제 검사). 한 축의 통과로 다른 축의 통과를 추론하지 않는다.

### 선택형 프로젝트 폴더 대응

프로젝트 폴더는 정본 원장·artifact/asset ID를 소유하고 아래는 파일을 찾기 위한 선택형 논리 구획으로만 쓴다. 기존 표준 패키지 트리와 중복 복사하지 않는다.

| 논리 단계 폴더 | 기존 패키지 경로 대응 |
|---|---|
| `01_DEVELOPMENT/` | `01_SOURCE/` 및 `02_BIBLE/` |
| `02_SCREENWRITING/` | `01_SOURCE/` |
| `03_PREPRODUCTION/` | `02_BIBLE/`, `04_STORYBOARDS/`, `05_SHOT_CARDS/`, `06_GENERATION_SPECS/`, `08_ANIMATIC_EDIT/` |
| `04_PRODUCTION/` | 원본 미디어는 실제 등록 위치를 유지하고, 촬영/테이크/연속성 기록은 `00_MANIFEST/`의 artifact로 연결 |
| `05_POSTPRODUCTION/` | 컷/사운드/애니매틱은 `07_AUDIO/`, `08_ANIMATIC_EDIT/`; QA는 `09_QA/` |
| `06_DISTRIBUTION/` | `10_DELIVERY/` |

이 대응은 기존 패키지 생성기의 현재 artifact 분류에 맞춘다. 새로운 flat 폴더를 추가하거나 같은 에셋을 단계별 폴더에 복제하지 않는다. 구현에서 경로 충돌이 확인되면 정본 manifest/asset registry를 우선한다.

첨부에서 제안한 30초 단편의 12개 항목은 전부 고려했으며, **애니매틱은 조건부**다. 영화 제작 전반의 산출물을 한꺼번에 생성하지 않는 선택 규칙과 촬영/배급의 법률·권리 확인 한계도 적용 범위에 포함했다.


## 문서 의미 및 최소 필드

### Development와 Screenwriting

- **Story**: 이야기 세계에서 일어난 사건의 전체 내용/시간 순서.
- **Plot**: 관객에게 사건을 배열·공개하는 구조. story의 동의어로 쓰지 않는다.
- **Synopsis**: 시작부터 결말까지의 압축 요약. 제작용이면 반전/결말을 포함하며, 홍보용 블러브와 목적을 표시해 구분한다.
- **Treatment**: 각본보다 앞선 산문형 전개 문서. 사건, 주요 장면, 인물 행동과 감정 변화의 수준을 밝힌다.
- **Screenplay**: 장면별 장소/시간, 화면 행동, 대사 중심의 제작용 각본.
- **Premise, theme, concept, logline**: 각각 전제, 탐구 질문, 차별화된 핵심 발상, 인물·목표·장애/위험의 압축으로 구분한다. 사용자가 제공하지 않은 방향은 제안으로 표시한다.
- 비트→씬→시퀀스→막을 연결할 수 있으나 샷은 제작/편집 단위로 별도 유지한다. 각 씬에서 목표·갈등·전환·감정 변화·정보 공개 슬롯은 필요한 장면에 사용하며, 전부 필수화하지 않는다.
- 리라이트는 기존 artifact 버전과 변경 요약으로 추적한다. 새 중복 원장이나 승인 상태를 만들지 않는다.

### Production, Post-production, Distribution 기록

`project.json`의 정본 ID/버전/의존/상태/승인/에셋 계약을 재사용한다. 구현 시 필요할 경우 도메인별 CSV/Markdown은 조회·인계용 파생 문서로 둔다. 새 스키마 필드는 필요성 검토와 기존 validator/consumer 영향 확인 전에는 추가하지 않는다.

- 현장 기록: `scene_id`, `shot_id`, `take_id`(기존 원장에 대응하는 artifact/asset locator), 날짜/촬영순서, 상태(계획/촬영/선택/보류/재촬영), 실제 원본 파일·버전, 선택 사유/검토 근거, 연속성 차이, 백업/무결성 검사 결과. 측정하지 않은 카메라/오디오 메타데이터는 추정하지 않는다.
- 후반작업: 컷/믹스/그레이드 등 단계별 artifact version, 입력 테이크/에셋 버전, 실제 타임라인 또는 출력 파일, 변경/수정 의존성, 검수 유형(playback/audio/visual/captions/continuity 등), evidence 및 미검증 범위. 편집 계획만으로 렌더 완료를 주장하지 않는다.
- 배급: 목적지·포맷·버전이 있는 delivery_spec을 재사용하고, 자막/크레딧/키아트/EPK/예고편 파일은 실제 있으면 asset_registry에 연결한다. 권리 항목은 출처·확인 상태·사용 범위·제한·근거를 기록하고, 기록 자체를 허가로 해석하지 않는다. 영화제/플랫폼 submission 상태는 실제 확인 결과와 계획을 구분한다.
- 촬영 계약/허가/보험/동의는 책임자 확인이 필요한 blocker 또는 근거 locator로 기록한다. 스킬의 체크리스트가 법률·보험 자문을 대체하지 않는다.

## 30초 단편 프로필

전체 프로젝트에 장편 패키지를 강제하지 않는다. 사용자가 30초 단편 또는 비슷한 소규모 작품을 요청하면 아래를 **추천 최소 세트**로 제안하고 해당 없는 요소를 표시한다: 로그라인, 결말 포함 시놉시스, 캐릭터 시트(등장인물 있을 때), 시간/감정 비트시트, 시나리오, 씬 리스트, 비주얼 바이블/룩, 스토리보드, 샷리스트, 필요 시 애니매틱, 사운드 플랜, 최종 QC 체크리스트.

타임라인은 실제 측정이 아닌 경우 `proposal / 비실행용`으로 표시한다. 전체 타임라인의 샷 합계·타이밍 검증은 기존 계약/검증기를 쓰고, 검증 통과가 이야기 품질이나 실제 재생의 증거라고 주장하지 않는다.

## AI 영화 프로필

기존 AI 영상 인계 및 v5.1 무결성 계약을 그대로 라이프사이클에 매핑한다. 필요한 경우 캐릭터 정체성/SSOT, LOOK, 장면 상태/변화·보존, 레퍼런스 asset registry, 샷별 프롬프트, 시작/끝 상태, 모델·버전 provenance, 시도 로그/재시도 상한, 생성 결과 QA, 권리 출처를 등록한다. 변화 없는 씬에 상태 ledger를 강제하지 않는다. 샷 단위 결과만 통과해도 씬/작품 연속성이 통과한 것으로 보지 않으며, 실제 순서대로 이어진 결과물을 검사한다. 실제 모델·파라미터는 사용 시점의 실행기 계약에서 확인한다.

## 설계된 파일 변경 표면

| 파일 | 설계상 변경 |
|---|---|
| `video-production-assets/SKILL.md` | 새 라이프사이클 참조를 모듈 표/온디맨드 목록에 추가하고, 명시적 전체 영화 패키지와 단일 산출물 경계를 라우팅한다. 기존 모듈 15개 계약은 유지한다. |
| `video-production-assets/references/28-film-production-lifecycle.md` (신규) | 6단계 흐름, 적응 규칙, 단계 산출물/입출력/승인 경계, 단계별 기존 모듈 라우팅, 단편/AI 프로필 연결의 단일 안내서. |
| `video-production-assets/references/01-brief.md`, `02-story.md`, `03-screenplay.md` | 개발 문서 의미 차이, 제작용 시놉시스/트리트먼트/각본과 beat→scene→sequence→act 매핑을 필요한 모듈에서 명확히 한다. 기존 템플릿과 겹치지 않도록 변경 범위를 좁힌다. |
| `video-production-assets/references/06-shots.md`, `09-edit.md`, `14-production-ops.md`, `15-delivery.md` | 스토리보드/샷리스트/애니매틱 경계, 촬영순서·실제 현장 기록, 후반작업·최종 QC, 배급/납품 기록을 각 소유 모듈에서 보강한다. 전문 참조 23·기존 계약과 중복 절차를 만들지 않고 링크한다. |
| `video-production-assets/assets/` | 갭 검증 후 현장일지, 후반 QC/픽처락, 배급 패키지 템플릿을 추가한다. 각 템플릿은 기존 ID/상태/원장 필드를 참조하며 중복 원장을 정의하지 않는다. 기존 양식 재사용이 가능하면 신규 템플릿을 만들지 않는다. |
| `creative-production/references/production-routing.md` | 명시적 영화 전체 파이프라인/현재 단계 요청을 위 lifecycle guide로 연결한다. 단일 synopsis/script/shot/delivery 요청은 현행 최소 라우팅을 유지한다. |
| `README.md`, `creative-production/SKILL.md`, `orchestrating-video-preproduction/SKILL.md`, `developing-video-synopses/SKILL.md`, `storyboarding-video/SKILL.md`, `designing-video-character-sheets/SKILL.md`, `integrations/skill-routing.md` | 패키지 탐색과 위임된 에이전트 진입점에서 선택형 영화 라이프사이클을 해당 전체 제작/단계 인계 요청에만 노출한다. 단일 단계 안내는 공통 가이드 링크만 두며 각 전문 스킬의 기존 소유 범위를 유지한다. |
| `video-production-assets/scripts/`, `references/contract.md`, `project.json` | 초기 설계 범위에서는 변경하지 않는다. 기존 validator가 표현할 수 없는 필수 추적 요구가 발견된 경우에만 별도 호환성 설계 및 회귀 검증을 제안한다. |

저장소에 추가되는 파일·참조의 출처/권리 검토를 기존 패키지 원칙대로 한다. 첨부 자료를 통째로 복사하지 않고 독립적 운영 규칙으로 요약·구현한다.

## 구현 순서 및 수락 기준

| 순서 | 작업 | 완료 증거 |
|---|---|---|
| 1 | 현재 소유 모듈·템플릿/검증기 필드와 영화 단계 요구를 대조해 실제 추가 템플릿 목록 확정 | 모든 첨부 항목이 기존/추가/조건부/N/A로 매핑되고 중복 원장·불필요 스키마가 없음. |
| 2 | `28-film-production-lifecycle.md` 작성 및 `video-production-assets/SKILL.md`에 발견/라우팅 연결 | 6단계 모두 입력·산출물·종료/인계 기준, 선택/N/A, 승인 경계가 명시됨. 기존 단일 산출물 요청은 전체 패키지로 확대되지 않음. |
| 3 | 01/02/03/06/09/14/15 참조의 소유 범위만 업데이트하고 필요한 템플릿 구현 | 정의 충돌 없이 첨부의 주요 누락(개발 문서, 현장 추적, 후반작업, 배급)이 사용 가능한 양식/지침으로 표현됨. |
| 4 | creative-production 영화 라우팅 연결 | 영화 전체 요청은 통합 흐름으로, 단계별/단일 산출물 요청은 가장 좁은 소유 모듈로 라우팅됨. |
| 5 | 문서·경로·프로젝트 검사와 실제 스모크 | 아래 시나리오 통과. 기존 광고/교육/비디오 스토리보드·delivery 예제 검사 회귀 없음. |

### 검증 시나리오

1. **단일 로그라인 요청:** 로그라인만 반환. 영화 전체 파일 구조·폴더·프로젝트 원장·후속 단계 생성 없음.
2. **영화 전체 개발 요청:** story와 plot, 제작용 synopsis, treatment, screenplay의 차이를 설명하고 요청·승인 범위에 맞는 문서만 실제 작성/계획. 미정 창작 방향은 제안으로 표시.
3. **막/시퀀스/씬/비트 예제:** ID 연결이 보존되고 shot이 story unit으로 잘못 혼합되지 않음.
4. **30초 단편 요청:** 최소 산출물 세트를 제안/작성하되 불필요한 캐스팅·보험·DCP 등은 강제하지 않음. 가상 타임라인은 측정값으로 표시하지 않음.
5. **실사 촬영 재개:** 이야기 순서와 다른 실제 촬영 순서를 보존하고 take/연속성/파일 무결성 상태를 실제 관찰과 분리. 누락된 현장 자료를 만들어내지 않음.
6. **AI 단편:** 활성 LOOK/캐릭터 SSOT/샷 상태·생성 provenance를 적용하며 변화 없는 상태 ledger를 강제하지 않음. 각 샷 평가와 전체 씬 연결 재생 검사를 구분.
7. **후반작업/배급 계획만 요청:** 픽처 락·믹스·그레이드·납품/출품은 계획과 실행 상태를 분리. 실제 렌더·업로드·출품·게시 없음.
8. **권리 근거 미확인:** 권리 상태를 unknown/unverified로 유지하고 사용 승인·배급 가능을 주장하지 않음.
9. **상위 각본 버전 변경:** 실제 dependency가 있는 하위 아티팩트만 stale. 독립 아티팩트와 기존 승인 이력은 보존.
10. **비영화 광고/설명 영상 요청:** 현행 좁은 모듈 흐름 유지, 6단계 문서/영화 구조를 강제하지 않음.
11. 기존 project/스토리보드/납품 검증 예제를 다시 실행하고 기존 검사 의미를 유지한다. 실제 재생/권리/사용자 승인 판정은 별도 증거로 남긴다.
12. **연속성 경계 사례:** 컵이 한 테이크에서 오른손에 있고 연결 샷에서 왼손으로 바뀌면 명시적 의도/행동 원인이 없을 경우 미해결 이슈로 남긴다. 의도된 변화는 근거와 상태 전이를 기록해 자동 오류로 취급하지 않는다.
13. **리서치·권리 경계:** 출처 링크만 있고 실제 근거/사용 범위가 확인되지 않은 자료는 미검증/권리 미확인 상태로 유지한다.
14. **단계 겹침·비적용:** 예를 들어 개발 중 선행 비주얼 테스트를 허용하되 입력 버전을 기록하고, 촬영 없는 애니메이션/AI 작업은 실사 현장 양식을 N/A 처리해 존재하지 않는 현장 데이터를 요구하지 않는다.
15. **최종 QC 체크리스트와 결과 구분:** 계획 단계에서도 QC 체크리스트 산출물은 만들 수 있다. 실제 playback/audio/visual/QC 결과는 해당 파일이 생기고 검사된 뒤에만 pass로 기록한다.


## 구현 전 검토가 필요한 선택

현재 설계는 보수적 기본값으로 **기존 스킬을 확장하고, 전체 영화 흐름은 선택 경로로 제공**하도록 정했다. 다음 피드백이 있으면 구현 전에 이 문서를 수정한다:

- 6단계 전체 경로를 모든 영상 요청에 기본 적용할지 여부 (기본: 명시적 영화/전체 파이프라인 요청에만 적용).
- 템플릿을 우선 추가할 단계 (기본 우선순위: development 문서 분화 → production 현장 기록 → postproduction/distribution 패키지).
- 새 project.json 필드/validator가 실제로 필요한지 (기본: 기존 스키마와 artifact/asset 연결로 해결하고 필요성이 입증될 때만 별도 설계).
