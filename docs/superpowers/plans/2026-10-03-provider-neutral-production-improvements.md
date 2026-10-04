# Provider-neutral Production Improvements Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement the checked tasks. Shared-file integration and verification belong to the coordinator; independent execution/audio reference edits may run concurrently. Skip build/lint/tests/formatters during delegated edits; verify the integrated result once afterward.

**Goal:** 현재 제작 스킬의 프리뷰·대화형 수정·음성·자막·음원 소싱 공백을 메우되 모델·공급자·수량·품질 설정을 공통 기본값으로 고정하지 않는다.

**Architecture:** 기존 creative-production 총괄, production-assets의 온디맨드 참조, project.json 정본을 유지한다. 도구 발견·현재 계약 확인·버전별 승인·실제 출력 검수를 연결하고 상세 호출은 선택된 외부 실행자가 소유한다. 새로운 공급자 SDK, 상태 원장, 자동 승인 엔진을 추가하지 않는다.

**Tech Stack:** Markdown skills/references/templates, JSON behavior evals, 기존 Python installer/production/spatial 검증 CLI, 도구 없는 fresh-context 모델 시나리오 평가.

**Spec:** 이 문서의 Global Constraints와 작업별 완료 기준이 사용자가 승인한 대화상의 보완 요구사항을 기록한다. 사용자 요청: 작업지시서를 저장하고 체크하면서 보완한다; 모델 추천은 가능하나 스킬에 모델·공급자·숫자를 하드코딩하지 않는다.

## Global Constraints

- 기존 작업 디렉터리의 미커밋 변경을 보존한다. 무관한 변경을 되돌리거나 커밋·푸시·전역 설치하지 않는다.
- 사용자가 지정한 공급자/모델/출력 규격은 보존한다. 미지정 경로는 현재 사용 가능성과 요구사항으로 고르고, 지정 경로 변경은 승인된 변경 범위로 처리한다.
- 특정 모델명·버전·가격·성능 순위·프리뷰/최종 해상도·길이·아이디어 수를 기본 정책으로 넣지 않는다. 프로젝트별 실제 선택과 도구 계약은 근거/확인 시점과 함께 기록한다.
- 특정 이미지 helper를 필수로 강제하는 기존 검토 계약을 현재 발견/선택된 이미지 실행자 계약으로 바꾼다. 실제 도구명·명시적 통합 매핑과 과거 릴리스 증거는 삭제 대상이 아니다.
- project.json, artifact.dependencies/dependency_versions/approval, asset_registry, shot.asset_ids, generation_attempts와 retry_budget을 재사용한다. 추가 상세 계획은 연결된 artifact로 관리한다; JSON 스키마를 불필요하게 확장하지 않는다.
- 실제 영상 프리뷰도 실행 승인 대상이다. 프리뷰 승인/QA는 최종 제작·과금·게시 허가를 대신하지 않는다. 프리뷰와 최종 범위를 하나의 계획에서 승인한 경우 이미 승인된 범위를 재질문하지 않되 현재 입력 버전/조건/상한을 지킨다.
- 문서 스킬 보완이지 외부 서비스/미디어 제작 요청이 아니다. 실제 생성·과금·게시 없이 도구 없는 시나리오와 기존 CLI로 검증한다. 실제 미디어 품질·현재 공급자 기능·권리의 진위를 이 검증으로 보증하지 않는다.

## Review Focus

- 지원되지 않는 저해상도/짧은 길이를 비용 절감 기본값으로 발명하는 입력: 검증된 지원 설정과 판단할 동작을 기준으로 프리뷰를 설계한다.
- 프리뷰만 승인됐거나 프리뷰 입력이 변경된 경우: 최종 실행과 이전 버전 승인을 자동 승계하지 않는다.
- 정지 프레임만 보고 음향/모션 pass를 요구하는 입력: 실제 재생/청취 범위를 분리한다.
- 음악 제외 기능이 없는 도구와 단일 혼합 트랙: 가짜 파라미터나 존재하지 않는 stem을 만들지 않는다.
- 최종 음성 없는 운문 번역/SRT와 라이선스 불명 음원: 편집/번역 계획과 측정된 동기화·권리 확인을 구분한다.

---

## 체크리스트

각 작업의 문서 반영 후 항목을 체크하고 변경 위치를 남긴다. 마지막 시나리오 검증이 통과하기 전 전체 완료로 보고하지 않는다.

### 1. 모델·공급자·설정의 하드코딩 제거

- [x] 공통 검토 이미지 경로의 필수 helper/명령 고정을 제거한다. 실제 선택 실행자의 발견·인증·지원 기능·가격·권리·출력 저장 계약으로 대체한다.
- [x] 총괄 SKILL, production-routing, production-assets SKILL, README, USAGE_GUIDE, integrations/skill-routing의 활성 설명을 같은 계약으로 맞춘다.
- [x] video-model-routing-template에 실제 endpoint/스키마 근거·확인 시점·설정별 견적·한계·승인 범위 기록란을 보완한다.

**Files:** creative-production/SKILL.md, creative-production/references/production-routing.md; video-production-assets/SKILL.md, references/preproduction-review.md, references/24-production-execution.md, assets/video-model-routing-template.md; manifest.json, README.md, USAGE_GUIDE.md, integrations/skill-routing.md; docs/superpowers/specs/2026-10-02-creative-production-package-design.md, specs/2026-10-02-preproduction-review-gate-design.md and the supersession note in plans/2026-10-02-preproduction-review-gate.md.
**완료 기준:** 공급자를 지정하지 않은 검토 이미지 작업이 특정 helper 부재만으로 차단되지 않는다. 지정된 공급자는 조용히 대체하지 않는다. 가격/필수 기능이 미확인이면 제출하지 않는다.
**결과·근거:** 문서 반영 완료. preproduction-review §3과 manifest image dependency를 선택 실행자 계약으로 전환하고 활성 호출 경로와 이전 설계 참조를 맞췄다. Codex Imagen 관련 명칭은 조건부 통합 예시/과거 provenance에만 남긴다. 모델 순위·공급자별 가격·프리뷰 숫자 기본값을 추가하지 않았다.

### 2. 프리뷰·에셋 잠금·최종 제작 게이트

- [x] 승인 참조 ID/버전과 판단할 동작·구도·접촉을 연결해 최소 충분 프리뷰 계획을 만든다.
- [x] 실제 지원 설정으로 프리뷰 샷/출력 수·시간·비용·재시도 상한을 명시하고 영상 실행 승인을 유지한다.
- [x] 프리뷰 실제 출력/검토/수락과 최종 실행 허가를 구분한다. 업스케일/재생성/편집 경로를 비교하고 최종본의 정체성·동작·구도·오디오·기술 규격을 재검수한다.

**Files:** references/preproduction-review.md, references/24-production-execution.md, references/contract.md, references/21-generated-video-qa-retry.md, assets/video-model-routing-template.md.
**완료 기준:** 프리뷰만 승인된 입력은 최종 생성으로 넘어가지 않는다. 프리뷰에 없는 접촉/동작을 통과 처리하지 않는다. 에셋 변경은 영향받는 단계만 stale로 만든다. 동일 seed/재생성의 동일 동작을 보장하지 않는다.
**결과·근거:** 문서 반영 완료. 24-production-execution §5, contract의 프리뷰/최종 artifact 연결, 21-generated-video-qa-retry의 프리뷰 판정과 라우팅 템플릿에 반영했다. 이미 승인된 조건부 최종 단계는 재승인을 강제하지 않으며, 프리뷰 밖의 동작을 통과 처리하지 않는다.

### 3. 도구 중립 대화형 생성·검토·수정 루프

- [x] 요청/계획 → 현재 도구 계약 확인 → 승인된 제출 → 실제 job/파일 기록 → 관찰 → 타깃 수정 → 허가 범위 내 재시도 순서를 연결한다.
- [x] MCP는 연결 방식으로만 취급한다. async 상태는 실제 선택 도구의 대기 규칙을 따르고, 결과 ID/실패/일부 성공을 보존하며 중복 제출하지 않는다.
- [x] 수정 프롬프트·비평 자체는 실행 허가가 아님을 유지한다. 입력 변경의 영향과 남은 상한을 확인한다.

**Files:** creative-production/references/video-generation-planning.md, video-production-assets/references/21-generated-video-qa-retry.md.
**완료 기준:** 사용자 관찰과 직접 검사 구분, 문제 위치·보존 속성·한 주요 변수 수정·재검수 기준을 반환한다. 결과 확인 불가를 성공으로 보고하거나 재호출로 해결하지 않는다.
**결과·근거:** 문서 반영 완료. video-generation-planning §6 및 21-generated-video-qa-retry에 연결했다. 대기 job 상태/ID는 실행 artifact, 확정 시도 상세는 generation_attempts.notes에 기록한다. 과거 시도는 보존하고 영향받는 artifact/승인만 stale로 만든다.

### 4. 효과음 전용·음악 제외 오디오 경로

- [x] 무음/대사 없음/효과음만/음악 제외/혼합 참조를 분리하고, endpoint의 실제 제어 지원으로 생성 경로를 결정한다.
- [x] 미지원 시 영상과 음향을 분리하는 제안을 하되 승인 없이 새 음향 작업·분리·과금하지 않는다.
- [x] 실제 오디오 큐·파일·청취 범위로 요청을 검수한다. 원장 enum과 layer를 재사용한다.

**Files:** video-production-assets/references/09-edit.md, references/15-delivery.md, assets/09-edit-template.md, assets/15-delivery-template.md.
**완료 기준:** no_dialogue를 no_audio나 no_music으로 해석하지 않는다. 음악 제외 미지원 도구에 가짜 필드를 추가하지 않는다. 단일 혼합 트랙을 분리 stem으로 보고하지 않는다.
**결과·근거:** 문서 반영 완료. 09-edit의 오디오 의도/실행 경로와 15-delivery에 SFX-only/no-music을 기존 enum 및 큐 layer로 표현했다. 미지원 제어는 별도 승인된 조립 제안으로 처리하고 실제 청취 없이는 pass를 기록하지 않는다.

### 5. 보이스 선택·생성·번역 자막·SRT

- [x] 현재 음성 도구/보이스 목록·언어·발음·톤·속도·권리/동의·비용을 확인하고 승인된 음성 정체성을 버전 연결한다.
- [x] 음성 결과를 실제로 청취하고 텍스트·발음·호흡·속도·일관성을 검수한 뒤 편집/립싱크에 연결한다.
- [x] 운문 번역의 의미·리듬·행 구분·고유명사·승인된 각색을 구분하고, 최종 음성 후 측정 타이밍으로 요청된 SRT/자막 형식을 제작·검수한다.

**Files:** video-production-assets/references/22-dialogue-lipsync.md, references/15-delivery.md, assets/performance-cue-template.md, assets/15-delivery-template.md.
**완료 기준:** 음성 없는 원고에서 frame-accurate SRT를 발명하지 않는다. 실제 음성 교체가 종속 자막/립싱크 승인에 미치는 영향을 반영한다. 지정 음성 도구를 무단 대체하지 않는다.
**결과·근거:** 문서 반영 완료. 22-dialogue-lipsync의 보이스 선택/청취 및 15-delivery의 자막 파일/타이밍을 보완하고 performance/delivery 템플릿에 근거·버전·번역 검수란을 추가했다. 최종 음성 없는 타이밍은 provisional/unverified이며 특정 음성 공급자를 강제하지 않는다.

### 6. 음악·효과음 소싱·권리 확인

- [x] 요청 목적·길이·감정·동기 기준점을 바탕으로 현재 가능한 카탈로그/제공 파일에서 후보를 비교한다.
- [x] 선택 항목의 출처/ID·권리 근거·확인 시점·플랜/프로젝트/지역/기간/게시 제한과 파일 버전을 연결한다. 구독/다운로드를 허가로 단정하지 않는다.
- [x] 실제 source/final 구간·fade/gain·동기 기준점·청취 결과를 기존 sound-cues와 편집 artifact에 연결한다.

**Files:** video-production-assets/references/09-edit.md, assets/09-edit-template.md.
**완료 기준:** 출처 URL만으로 상업적 사용을 통과 처리하지 않는다. 가격/권리 불명은 차단 범위와 준비 가능 범위를 구분한다. 자동 구매/게시하지 않는다.
**결과·근거:** 문서 반영 완료. 09-edit의 음악/효과음 소싱·권리 절차와 편집 템플릿의 후보/근거/청취 표에 기록했다. 기존 sound-cues.csv 스키마는 유지하며 상세 권리 조건은 mix_note/연결 artifact에 둔다. 실제 라이선스 적합성과 청취는 별도 미디어 실행에서 확인해야 한다.

### 7. 콘셉트 탐색 수량의 프로젝트별 결정

- [x] 요청한 정확한 후보 수는 보존한다. 미지정 수량은 차별성·판단 가능한 탐색 폭과 제작 제약으로 결정한다.
- [x] 텍스트 후보 수와 실제 정지/영상 프리뷰 출력 수·승인을 분리한다. 공통 아이디어/앵글 고정 수량을 추가하지 않는다.

**Files:** video-production-assets/references/13-ideation-brand.md, references/16-concept-emotion-retention.md, references/20-visual-mode-ssot.md, references/05-visual.md, references/24-production-execution.md (실제로 발견된 고정 후보/전환 수와 승인 충돌만).
**완료 기준:** 불필요한 후보 수 강제나 미승인 영상 batch로 확대되지 않는다. 창작 방향 수락/위임과 실제 생성 승인을 구분한다.
**결과·근거:** 문서 반영 완료. 13-ideation-brand, 16-concept-emotion-retention, 20-visual-mode-ssot 및 24의 후보 수 고정과 방향 수락 충돌을 제거했다. 05-visual의 핵심 요소 수도 제작 요구로 결정한다. 임의 신기함 경고 개수로 자동 탈락시키지 않고 실제 관객 영향으로 판단한다.

### 8. 동작 검증·배포 문서·완료 기록

- [x] creative-production/evals/evals.json에 consumer-visible 경계 시나리오를 추가하고, 문구/링크 존재를 permanent test로 검사하지 않는다.
- [x] 변경 전 대표 경로를 실행했으나 첫 baseline 2회 시나리오 수집이 eval 셀 deadline을 초과했다. 비교 출력은 없다고 기록하고 변경 후 17개 scenario 실제 출력과 probabilistic rubric 결과를 qa/provider-neutral-production-validation.json에 기록했다.
- [x] 기존 전체 suite를 실행했다: python -B scripts/test_install_package.py (21), python -B video-production-assets/scripts/test_validate_project.py (15), python -B camera-spatial-design/scripts/test_spatial_spec.py (7) — 전부 OK.
- [x] 기존 교육/애니메이션 project.json 두 개를 실제 plan validator CLI로 검증해 valid를 확인했다. eval/QA JSON을 읽고, 변경 Markdown 28개에서 상대 링크 161개를 검사해 누락 0건을 확인했다. 설치 스모크에서 임시 경로에 8개 스킬과 production reference를 설치하고 대상 경로를 삭제했다.
- [x] read-only 검토에서 Critical/Important 결함은 보고되지 않았다. 평가와 수동 판독으로 실행자/가격/승인 범위를 확인했다. rubric 확률은 binary proof가 아니며 결과 기록에 보존했다.
- [x] CHANGELOG와 README/USAGE_GUIDE를 갱신하고 외부 미디어/provider/license verification 한계를 기록했다.

**완료 기준:** 신규/기존 시나리오의 실제 출력과 rubric 결과가 남고, 구조/회귀 CLI 결과와 실패를 모두 보고한다. 생성/청취/공급자 통합/권리 진위 검증으로 과장하지 않는다. 전역 설치/커밋/푸시는 별도 요청 전 수행하지 않는다.
**결과·근거:** 완료. eval 17개 fresh-context 실제 출력과 판정, suite 21+15+7, plan validator 2개, disposable install 및 markdown 상대 링크 결과를 QA에 남겼다. 변경 전 출력은 수집 deadline으로 확보하지 못해 비교 주장을 하지 않는다. 실제 미디어 생성·공급자 기능·음원 라이선스·최종 음성 타이밍은 검증하지 않았다.


### 9. 기존 평가에서 발견된 무근거 제품 효익 주장

- [x] 제품 기능명만 주어지고 구체적 효익 근거가 없으면 편의성·속도·품질 개선을 사실처럼 보태지 않도록 카피 지침을 명시한다.
- [x] 기존 eval 3을 다시 실행해 요청한 할인/기간만 전달하는지 확인하고, 실제 출력과 판단 근거를 검증 기록에 남긴다.

**Files:** creative-production/references/marketing-source-adaptation.md, creative-production/evals/evals.json (기존 시나리오 사용), qa/provider-neutral-production-validation.json.
**완료 기준:** 지원 자료가 없는 제품 효익 주장을 만들지 않는다. 필요한 사실이 비어 있으면 중립적으로 제안하거나 근거를 요청하며, 마케팅 전체 경로를 임의로 늘리지 않는다.
**결과·근거:** 완료. 참조 지침은 기능명에서 편의성/속도/품질 우위를 추론하지 않고, 프로모션 기간을 출시 이유로 바꾸지 않도록 한다. eval 3 fresh-context 출력은 정확히 3개 카피를 제공하고, 미제공 효익·원인·게시 지시를 추가하지 않았다. 출력과 probabilistic judgment를 QA에 기록했다.

## Execution Handoff

사용자가 이 대화에서 작업지시서 기록과 이어지는 실행을 요청했다. 기존 미커밋 작업을 보존하며 현재 디렉터리에서 진행한다. 문서/평가 결과만 변경하고 실제 외부 미디어 작업이나 지출은 하지 않는다.
