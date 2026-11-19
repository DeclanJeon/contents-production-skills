# 모듈 심화·표 형식 인계 색인

해당 요청의 심화 가이드/추가 템플릿을 찾을 때만 연다. 단일 조명 등 기본 모듈 요청은 SKILL의 직접 모듈 행을 쓰며 이 전체 색인을 미리 읽지 않는다. 패키지 진행은 [preproduction-review](preproduction-review.md)가 소유한다.

## 온디맨드 심화 참조

대사 유무와 무관하게 중요한 스틸·샷·앵글·구도·인물 묘사·표정·액션·분위기의 전달 의도를 설계하거나 검수하면 [공통 시각 연출·장면 전달](visual-scene-communication.md)의 필요한 절을 현재02/03/04/05/06/07/08/09/12 오너 안에서 사용한다. 기존 템플릿과 승인된 이야기·언어 역할을 유지하며 모든 작업을 무성 서사 스킬로 보내거나 전수 원본 분석/새 필드를 요구하지 않는다.

요청에 해당할 때만 연다. 각 파일은 기존 모듈의 절차를 확장하는 심화 가이드다.

한국어 영상 대사·내레이션의 번역투/자연스러움 후편집 또는 해당 원고 QA 요청에는 [한국어 발화 후편집](korean-script-postediting.md#scope)을 읽는다. 기존 각본 오너의 지원 참조이며 별도 스킬·제작 단계를 만들지 않는다.

| 요청 | 심화 참조 | 보조 템플릿 |
|---|---|---|
| 콘셉트 후보·감정 여정·시청 유지 설계 | [콘셉트·감정·유지](16-concept-emotion-retention.md) | 13 템플릿 |
| 장르 긴장·코미디 구조·에스컬레이션 | [장르·코미디](17-genre-comedy.md) | — |
| 시리즈 바이블·회차·콜백·상태 델타·대사 중심 연작의 제작량/연재 페이스 | [시리즈·에피소드](18-episodic-series.md) | `assets/series-bible-template.md`, `assets/continuity-ledger.csv`, 반복 작업량에는 `assets/14-production-ops-template.md` |
| 스폰서 통합·정확한 제품 샷 | [스폰서·제품 통합](19-brand-product-integration.md) | `assets/product-ssot-template.md` |
| 비주얼 모드 선택·SSOT 티어·연속성·군중 | [비주얼 모드·SSOT](20-visual-mode-ssot.md) | `assets/character-ssot-template.md`, `assets/crowd-map-template.md` |
| 복잡 모션·합성 레이어·생성 매체 검수·재시도 | [생성 영상 QA·재시도](21-generated-video-qa-retry.md) | `assets/motion-beat-template.md`, `assets/vfx-layer-stack-template.md`, `assets/generated-qa-report-template.md` |
| 대사 연기·보이스 선택/생성·립싱크·청자 디렉팅 | [대사·립싱크](22-dialogue-lipsync.md) | `assets/performance-cue-template.md` |
| 실제 테이크의 음질·연기·보이스·효과음·립싱크 결함 | [최소 테이크 보정](take-repair.md) | 기존 컷/테이크·오디오 인계와 QA 기록 |
| 피니싱 룩·그레이드 노드 구조·믹스·마스터 QC·플랫폼 적응 | [피니싱·플랫폼](23-finishing-platform.md) | — |
| 속도·타격·컷 전환·효과음·음악·공간음향 중 무엇을 이름으로 고르거나 바꿈 | [편집·음향 표현 선택표](edit-sound-language-catalog.md) | 편집은 09 템플릿, 음향은 `assets/sound-cues.csv` |
| 이미지/영상 생성 경로·최소 충분 프리뷰·최종 제작·비용·에셋 출처 | [생성 경로·비용 라우팅](24-production-execution.md) | `assets/video-model-routing-template.md` |
| 사용자가 요청한 단일/아카이브 레퍼런스 분석·교차 영상 패턴/오너 갭 비교·기존 스킬로의 명시적 skillification | [레퍼런스 영상 분해](25-reference-video-analysis.md) | 단일 영상은 `assets/shot-dna-template.md`, 아카이브는 `assets/archive-audit-template.md`; 명시적 exhaustive all-source/all-shot 또는 cross-source craft extraction에서만 [`assets/archive-craft-crosswalk-template.md`](../assets/archive-craft-crosswalk-template.md)를 조건부 필수 사용. 일반/단일 레퍼런스에는 강제하지 않음. 기존 오너 반영은 명시적 skillification에서만; Rofan 사례집은 선택적 출처 근거이며 필수 조회가 아님. 로컬 영상의 컷·제작방식·자막·음원 측정이 필요하고 설치된 rea-video가 있으면 조건부로 [외부 분해 백엔드 어댑터](31-external-video-decomposition.md)를 적용하고, 없으면 25 수작업 경로로 폴백 |
| 한 번에 시놉시스부터 전체 스토리보드 시트까지 요청·프롬프트 작성 | [스토리보드 시트 사용자 가이드](storyboard-sheet-user-guide.md) | 범용 복사용 프롬프트 |
| 활성 LOOK·에셋 게이트·마스터/파생 계보·패널 버전 참조·provenance·v5.1 패키지 출력 | [v5.1 프로덕션 무결성](contract.md#v51-프로덕션-무결성-look에셋-게이트계보provenance패키지) | `assets/style-world-bible-template.md`, `assets/adaptation-map-template.md`, `assets/asset-gate.csv`, `assets/asset-provenance.csv`, `assets/prompt-ledger.csv`, `assets/dependency-graph.csv`, `assets/storyboard-panel-manifest.csv` |
| 복합 참조의 속성/우선순위·시트 입력 뷰·다국어 제출 검수·새 생성/부분 수정/실제 확장·국소 발음 교정·채택 구간/비용 | [참조 기반 실무 인계](29-reference-driven-production.md) — 현재 모듈의 해당 절만 적용; 기존 승인·Sheet A·단일 원장 유지 | 기존 11·14·연기 큐·생성 QA·시리즈 바이블 템플릿 |
| 명시적 영화/단편/애니메이션/AI 영화의 기획→배급 전체 라이프사이클·단계 인계 요청 | [영화 제작 라이프사이클](28-film-production-lifecycle.md) | — |

레퍼런스 영상 분해를 요청하면 영상/링크가 첨부되지 않았더라도 `references/25-reference-video-analysis.md`를 읽는다. 소스가 없으면 필요한 입력만 안내하고 프레임 분석·아카이브 주장·파일 쓰기·업로드·생성을 시작하지 않는다. 장면 내용을 추론하지 않는다.

## 표 형식 인계
대량 샷은 `assets/shot-list.csv`, 사운드 레이어는 `assets/sound-cues.csv`, 사실 주장은 `assets/claim-ledger.csv`, v5.1 매니페스트는 `assets/asset-gate.csv`·`assets/asset-provenance.csv`·`assets/prompt-ledger.csv`·`assets/dependency-graph.csv`·`assets/storyboard-panel-manifest.csv`의 열 구조를 사용한다. CSV는 비어 있는 작성용 헤더이며 JSON 원장과 ID를 맞춘다. 패키지 매니페스트는 `package_production.py`가 정본에서 파생하므로 수동으로 따로 수정하지 않는다.

## 요청 범위와 완료 판정
이 패키지는 하나의 통합 스킬 안에 15개 작업 모듈이 있다. 각 모듈이 별도로 설치되는 스킬은 아니다. 단일 산출물 요청에는 필요한 모듈과 공통 계약만 읽는다.

계획/각본/프롬프트 요청은 내용과 인계가 완성되면 완료한다. 전체 프리프로덕션 패키지는 실제 문서·요청된 정지 이미지·검수 보고를 갖춰 검토 대기로 인계한다. 영상 파일 요청은 별도 실행 승인 뒤 실제 생성·편집 결과와 해당 검사를 갖춰야 완료한다. 프리프로덕션 수락은 영상 생성·과금·게시 승인이 아니다.

검수 결과는 pass / pass_with_notes / needs_revision과 검사 범위를 함께 기록한다. 해당 없는 항목은 N/A와 이유, 확인할 수 없는 항목은 unverified로 남긴다. 원본 도서의 전권 핵심을 추출한 패키지라고 소개하지 않는다.

추가 에셋: `assets/asset-registry.csv`, `assets/continuity-ledger.csv`, `assets/storyboard-panels.csv`, `assets/production-budget.csv`와 심화 템플릿 `assets/series-bible-template.md`, `assets/character-ssot-template.md`, `assets/product-ssot-template.md`, `assets/shot-dna-template.md`, `assets/motion-beat-template.md`, `assets/vfx-layer-stack-template.md`, `assets/crowd-map-template.md`, `assets/performance-cue-template.md`, `assets/video-model-routing-template.md`, `assets/generated-qa-report-template.md`. 생성 시도 로그와 재시도 상한은 별도 파일이 아니라 `project.json`의 `generation_attempts`와 `shot.retry_budget`에 기록한다.
v5.1 패키지 추가 에셋: `assets/style-world-bible-template.md`, `assets/adaptation-map-template.md`, `assets/asset-gate.csv`, `assets/asset-provenance.csv`, `assets/prompt-ledger.csv`, `assets/dependency-graph.csv`, `assets/storyboard-panel-manifest.csv`.

