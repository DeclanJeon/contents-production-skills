# Staged Skill Loading and Focus View Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans for approved native execution, or superpowers:subagent-driven-development only if the user chooses that method. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 기존 제작/연속성/승인 기능을 보존하면서 시퀀스 표시와 단계별 문서 읽기의 불필요한 부피를 줄인다.
**Architecture:** 기존 full 실행 투영과 validator를 유지하고 별도 표시용 focus 모듈을 둔다. 기존 CSV 라우팅을 유지하면서 계약의 정본 책임을 단계별 파일로 이동한다. 테스트는 full/focus seam과 실제 문서 소비를 통해 수행한다.
**Tech Stack:** 기존 Python 표준 라이브러리·pytest·Markdown·CSV; 측정 시 기존 설치된 tiktoken o200k_base, 행동 검사는 명시적으로 허가된 host/model만 사용한다. 새 의존성 자동 설치 없음.
**Spec:** ../specs/2026-11-18-staged-skill-loading-focus-view-design.md (사용자 승인 완료).

## Global Constraints

- manifest의 **25개 관리 스킬**이 범위다. 비목록 brandkit/marketplace-cards/product-photoshoot/websites 4개는 수정/편입하지 않는다.
- 기존 build_sequence_context, CLI 기본 full, sequence-execution/1, project.json, read_projection/prepare/validate/inspect/render의 실행 의미를 보존한다.
- 표시 형식은 sequence-focus-view/1, read_only=true, executable=false, validation=not_run. 실행 투영으로 수락하지 않는다.
- 실제 채택 source range/out−1·관련 이력·native selected refs·voice/asset pins·missing/unverified 차단·사용자 승인 경계를 약화하지 않는다.
- 일반 보드를 러프 보드로 낮추지 않는다. 기존 typology 기본값/voice cue/7뷰/필수 기술 슬롯/이미지 QA/PDF 요구를 삭제하지 않는다.
- 캐시·새 스케줄러·중앙 로딩 엔진·DB·새 승인 원장·사용자 제작 데이터 마이그레이션을 만들지 않는다.
- scripts/routing_eval.py와 scripts/test_routing_eval_harness.py의 기존 dirty 변경, 다른 분석/QA/설계 파일은 무단 채택/수정하지 않는다.
- 새 미디어/provider 제출·업로드·계정 변경·비용 지출·외부 게시·의존성 설치 없음. 행동 평가의 LLM 호출은 별도 명시된 방법/모델/예산 승인 안에서만 한다.
- 작업 격리/로컬 커밋 범위는 실행 인계에서 확정한다. 원격 push와 설치 스킬 repoint/sync는 별도 승인 전 실행하지 않는다.

## Review Focus

- 전역 storyboard/실행 artifact가 보이면 focus가 다시 전체 패널/핀 맵으로 팽창하는 문제(T2).
- 이력 순환·여러 cut에 등장한 shot·cross-cut/flashback에서 필요한 비인접 상태가 사라지는 문제(T2).
- 표시 뷰나 다른 focus의 handoff가 실행 준비 입력으로 오인되는 문제(T2).
- 계약 이동 후 같은 anchor가 다른 의미를 가리키거나 core와 상세 정본이 서로 다른 필수 조건을 주장하는 문제(T3/T4).
- 읽기량 감소가 필수 슬롯 누락·이미지 실행자 auth/quote 오판·명시적 no-save 해제로 얻어진 허위 개선인 경우(T5/T6).

## 구현 구조

- `video-production-assets/scripts/sequence_view.py`: 표시 집합 선택/출력의 작은 공개 인터페이스.
- `video-production-assets/scripts/sequence_contract.py`: 기존 JSON 파싱·투영 shape 의미를 재사용하는 same-snapshot 읽기.
- `video-production-assets/scripts/sequence_context.py`: 새 --view 분기. 기존 builder/full 출력은 유지.
- 공통 계약 신규 4개: `contract-core.md`, `contract-project.md`, `contract-package.md`, `contract-delivery.md`.
- 보드 계약 신규 4개: `storyboard-direction.md`, `storyboard-media.md`, `storyboard-delivery.md`, `storyboard-schema.md`.
- 기존 `contract.md`는 호환 색인, `storyboard-contract.md`는 기본 완전성 코어/단계 선택표로 남긴다.
- `scripts/skill_loading_metrics.py`, `scripts/test_skill_loading_metrics.py`: baseline/candidate 파일 읽기량 비교. dirty routing evaluator와 분리한다.
- `scripts/test_staged_loading_contracts.py`, `qa/staged-loading/`: 이동 정본/anchor/대표 요청과 평가 증거. 토큰 수만으로 의미를 판정하지 않는다.

---

### Task 1: Baseline과 동등성/읽기량 측정 인터페이스

**Files:**
- Create: `scripts/skill_loading_metrics.py`, `scripts/test_skill_loading_metrics.py`.
- Create: `qa/staged-loading/cases.json`, `legacy-anchors.json`, `rule-ownership.csv`.
- Input: 감사 metrics/profiles/context-scaling 및 현재 committed source bd5fb68. 감사 파일은 아직 untracked이므로 소유 파일만 명시적으로 복사/핀한다.

**Interfaces:**
- `measure_files(root: Path, relative_paths: Sequence[str]) -> dict`: 파일별 raw SHA256, 정규화 문자 수, o200k_base reference tokens, unique-file 합계를 반환. 중복 요청 목록은 unique 합계와 returned/read 합계를 구분한다.
- `measure_read_events(events: Sequence[dict], root: Path) -> dict`: 성공한 실제 text tool-result의 반환량/반복 읽기를 계수. 결과 본문·일치하는 읽기 이벤트가 없거나 경로만 있으면 measured가 아니라 unverified다. billing tokens는 별도 값이다.
- rule ownership CSV 필드: rule_id, old_path, old_anchor, source_sha256, new_path, new_anchor, applies_when, equivalence_case_ids.

- [ ] **RED:** 동일 파일 반복 읽기, CRLF/LF, 잘린/실패한 read, root 이탈, 원문 없는 read trace를 입력하는 테스트를 작성한다. 읽지 않은 owner를 opened라고 판정하거나 unique 토큰만으로 총 읽기를 감추면 실패해야 한다.
- [ ] **Run:** `python3 -m pytest scripts/test_skill_loading_metrics.py -q`. 새 모듈/동작 부재로 실패하는지 확인한다.
- [ ] **Implement:** audit의 reference-token 기준을 재사용하되 raw-byte hash와 normalized 텍스트를 구분한다. 토크나이저가 없으면 자동 설치/다운로드하지 않고 측정 blocker를 반환한다. 새 평가기는 provider를 호출하지 않는다.
- [ ] baseline 경로/문서 hash, 기존 계약의 실제 heading/fragment, 아래 20개 대표 요청을 고정한다. 기존 평가기/질문에 정답 파일 목록을 주입하지 않는다.
- [ ] **GREEN:** 집중 테스트와 기존 version/routing-table/routing-regression/pack-boundary 검사를 실행한다. 결과와 source fingerprint를 보존한다.
- [ ] 승인된 로컬 커밋 범위 안에서 이 과업의 소유 파일만 체크포인트한다.

대표 case ID: logline, lighting, character-compact, character-full-ssot, appearance-only, typology-none, typology-both, board-full-text, board-rough, board-chat-only, board-save-md, board-save-pdf, package-image-backed, camera-numeric-only, blender-verification, no-audio, next-new-angle, return-after-insert, unsupported-native-ref, unknown-timeout.

모든 행동 case는 read-only/no-provider probe다. 실제 미디어 작업은 하지 않고 현재 범위의 텍스트 산출물/인계/필수 입력·차단 상태를 평가한다. cases.json의 각 행은 id, prompt, scope, inputs, expected_artifact_slots, expected_blockers, forbidden_actions, source_locators를 가진다. prompt/고정 입력/불변 슬롯과 사람이 채점할 근거를 보존한다. LLM 실행 전에는 두 snapshot에 동일 case를 공급할 수 있는지와 파일 이탈/변경 방지부터 확인한다.

### Task 2: 표시 전용 focus 모듈과 호환 CLI

**Files:**
- Create: `video-production-assets/scripts/sequence_view.py`, `test_sequence_view.py`.
- Modify: `sequence_contract.py`, `sequence_context.py`, `test_sequence_cli.py`, `test_sequence_contract.py`.
- Preserve: `project_index.py`, `validate_sequence.py`, `generation_handoff.py`, `prepare_generation_request.py`, 렌더/검사 실행 의미.

**Interfaces:**
- `build_sequence_focus_view(project: Mapping[str, Json], shot_ids: Sequence[str], projection: Mapping[str, Json] | None = None) -> Document`.
- `read_snapshot(path: Path, *, projection: bool = False) -> tuple[Document, Document]` in sequence_contract: JSON과 같은 raw 읽기에서 나온 `{path, sha256}`를 반환. 기존 finite JSON/투영 shape 검사를 공유하며 기존 read_document/read_projection의 반환/오류 의미를 보존한다.
- CLI `--view full|focus`, default full. focus는 --shot 필수, --all과 함께 쓰면 실패. focus 분기의 source metadata만 실제 snapshot 정보를 받는다.

- [ ] **RED:** 다음 공개 seam 테스트를 먼저 작성하고 실패를 본다: 기존 full 동일성/원본 불변, focus read-only 형식, 1·복수 focus, 첫/끝, 같은 shot의 복수 cut, 선행/후행·명시적 재등장·cross-cut/flashback·이력 순환/잘못된 ID.
- [ ] **RED:** 실제 image-backed fixture에 전역 BOARD/EXEC artifact를 연결해도 무관한 panel/asset/핀 전체 맵이 focus에 유입되지 않아야 한다. 필수 master/LOOK/voice/source 계보는 남아야 한다.
- [ ] **RED:** 다른 focus 제출문은 handoff_applicability=mismatch. 새 표시 뷰를 read_projection/prepare/validate/inspect/render로 넘기는 경우 ready/실행이 되지 않아야 한다. bootstrap/null/planned/stale를 성공으로 바꾸지 않는다.
- [ ] **Run:** `python3 -m pytest video-production-assets/scripts/test_sequence_view.py video-production-assets/scripts/test_sequence_cli.py -q`. 새 모듈/flag 부재 실패를 확인한다.
- [ ] **Implement:** spec §4의 inclusion/표시 필드/locator/omissions를 구현한다. 전역 owner는 compact identity/locator로 나타내고 원래 full pin 맵은 그대로 둔다. 명시적 이력만 닫고 모든 편집 선행을 재귀 확장하지 않는다. native request를 수정/부분 실행하지 않는다.
- [ ] same-snapshot 파싱/해시와 full default CLI 회귀를 추가한다. 순수 함수는 실제 파일 hash가 없으면 null/unavailable로 표시한다.
- [ ] **GREEN:** `python3 -m pytest video-production-assets/scripts/test_sequence*.py video-production-assets/scripts/test_validate_sequence.py video-production-assets/scripts/test_generation*.py video-production-assets/scripts/test_prepare_generation_request.py -q`로 기존 sequence/AV/transport/prepare/합성 media 회귀를 실행한다. 감사의 2/10/50/100 skeleton에서 focus 출력 100샷 ≤6000 tokens, 10→100 증가 ≤256 tokens를 실제 측정한다. 필수 이력이 많아진 별도 fixture에는 임의 cap을 적용하지 않는다.
- [ ] 승인된 로컬 체크포인트와 증거를 남긴다.

### Task 3: 공통 계약의 단계별 정본과 legacy anchor

**Files:**
- Create: `video-production-assets/references/contract-{core,project,package,delivery}.md`.
- Modify: `references/contract.md`, `scripts/test_staged_loading_contracts.py`, `qa/staged-loading/rule-ownership.csv`.
- Compare: 기존 공통 계약과 validate/update/asset_gate/package 도구. validator의 허용 조건은 수정하지 않는다.

**Interfaces:**
- contract-core: 기본 ID/시간/상태·단독 요청·입출력 최소·single writer.
- contract-project: project schema/정확한 dependency 버전·stale·index/update·authority/timing 메타데이터.
- contract-package: image-backed 전체 산출물·Sheet A·LOOK/master/derivative/FINAL/panel pins.
- contract-delivery: 납품 검사·ZIP/relocation/manifest·감사 사본.
- 기존 contract의 anchor는 explicit compatibility anchor와 정확한 새 정본 포인터로 유지한다.

- [ ] **RED:** legacy-anchors.json의 모든 실제 fragment가 해석되고, 각 이동 규칙에 소유 파일/적용 조건/동등성 case가 있으며 중복 정본이 없다는 구조 시험을 작성한다. 존재하지 않는 새 정본 때문에 실패하는지 확인한다.
- [ ] 규칙 본문을 spec §5.2 책임으로 이동한다. 기존 schema/field/state/단위/승인 의미를 보존하고 임의의 새로운 표준을 추가하지 않는다.
- [ ] 호환 색인과 ownership map을 함께 바꾼다. 소유 규칙을 짧게 바꾸는 경우 preserved invariant와 실제 출력/차단 case를 대조한다. 문장 이동만으로 의미 동등성이 증명됐다고 하지 않는다.
- [ ] **GREEN:** `python3 -m pytest scripts/test_staged_loading_contracts.py video-production-assets/scripts/test_reference_contract.py video-production-assets/scripts/test_project_handoff.py video-production-assets/scripts/test_validate_project.py video-production-assets/scripts/test_validate_preproduction.py video-production-assets/scripts/test_asset_gate.py -q`로 새 문서/anchor와 기존 원장·asset/package 회귀를 실행한다. 새로운 문서로 인해 실행 입력·해시·stale 거부가 달라지면 멈추고 진단한다.
- [ ] 이 과업 파일만 로컬 체크포인트한다.

### Task 4: 스토리보드 계약의 설계/매체/납품/스키마 분리

**Files:**
- Modify: `video-production-assets/references/storyboard-contract.md`.
- Create: `references/storyboard-{direction,media,delivery,schema}.md`.
- Modify: 문서 이동 시험/ownership map. 기존 storyboard validator/renderer/split/PDF 동작은 유지.

**Interfaces:**
- 기존 storyboard-contract = 6개 반환 구획·모든 필수 샷/패널 슬롯·완전성/N/A/deferred/blocker/기본 커버리지·단계별 읽기표.
- direction = 씬 의도·인접 비교·리듬/감정/공간·적용 가능한 staging/상태 패널 설계.
- media = 실제 이미지/시트/추출/등록·clean 이미지 전수 QA.
- delivery = 텍스트/이미지 PDF 도구·폰트·전체 페이지/텍스트/시각 검사.
- schema = 현재 상세 보드/rhythm JSON 규격과 validator 매핑.

- [ ] **RED:** 기존 fragment 전수 보존, core의 전체 필수 slot·6개 구획 보존, 기존 조명/발화/카메라/접촉/strict-staging/rhythm 조건이 새 정본으로 연결되는 시험을 작성한다.
- [ ] **Run:** `python3 -m pytest scripts/test_staged_loading_contracts.py scripts/test_storyline_continuity_gate.py -q`; 누락된 새 대상/필수 연결로 실패하는지 확인한다.
- [ ] 기존 내용의 정본을 위 책임대로 이동한다. text 보드는 core+direction을 반드시 적용하고 실제 이미지/PDF/스키마의 실행 단계만 늦춘다. 일반 보드의 필수 슬롯을 optional로 바꾸지 않는다.
- [ ] **GREEN:** `python3 -m pytest video-production-assets/scripts/test_validate_storyboard.py video-production-assets/scripts/test_validate_preproduction.py video-production-assets/scripts/test_render_storyboard_sheet.py video-production-assets/scripts/test_split_storyboard.py video-production-assets/scripts/test_storyboard_document.py video-production-assets/scripts/test_storyboard_pdf.py video-production-assets/scripts/test_measure_cut_rhythm.py video-production-assets/scripts/test_rhythm_review_regressions.py -q`로 보드·매체·PDF·리듬 회귀를 실행한다. 텍스트-only는 동일한 필수 설계를 반환하되 미디어 검사 완료를 주장하지 않아야 한다.
- [ ] 문서/ownership map을 원자적인 로컬 체크포인트로 남긴다.

### Task 5: 진입점·라우팅 연결과 잘못된 전제 수정

**Files:**
- Modify where applicable: `creative-production/SKILL.md`, `references/routing.csv`, `references/production-routing.md`, `references/policy.md`.
- Modify: `video-production-assets/SKILL.md`, `references/sequence-execution.md`, `references/preproduction-review.md`, `references/11-ai-handoff.md`, `references/24-production-execution.md`와 이동 규칙의 직접 소비자.
- Modify: `storyboarding-video/SKILL.md`, `designing-video-character-sheets/SKILL.md`, `orchestrating-video-preproduction/SKILL.md`, `recording-production-history/SKILL.md`.
- Modify for focused load only: `higgsfield-generate/SKILL.md`, `higgsfield-video-replicate/SKILL.md`, `higgsfield-video-explainer/SKILL.md`, `higgsfield-youtube-thumbnail/SKILL.md`, `blender-previsualization/SKILL.md`.
- Create: `recording-production-history/references/cli-contract.md`(기존 CLI 전체/저장·전이·원자성 상세), `higgsfield-video-replicate/references/clip-execution.md`(기존 모델별 모드/명령/clip·soundtrack·QC 세부), `higgsfield-video-explainer/references/block-execution.md`(기존 block·voice·clip·assembler 명령/회복 세부).
- Use existing model-catalog/image-branches/blender-workflow refs for historical/CLI material; do not create duplicate archives.

**Interfaces:**
- 27 route IDs/owner/3축 판단/disambiguation은 유지. required_read에는 unconditional 실제 경로만 둔다.
- R03 appearance는 진짜 외형 선택/변형 분기에서 필수. compact/full와 기존 persona/typology/voice 의미는 유지.
- dependent generation의 로컬 필수 포인터와 actual native binding/audit gate는 각 독립 실행 진입점에 남긴다.
- text_only와 no-save/read-only는 독립 제약. 명시적 MD/PDF 저장은 해당 단계만 열고 새 미디어를 허가하지 않는다.

- [ ] **RED:** 단독 조명에서 package/PDF 미리 읽기, 텍스트 보드의 media/schema 선행 로딩, appearance 무조건 로딩, Codex Imagen 썸네일의 Higgsfield auth/quote 강제, text-only 저장 금지 혼용을 각각 재현하는 계약/분기 시험을 추가한다.
- [ ] 실제 에이전트 baseline은 승인된 read-only 평가 방식·모델·예산 안에서 T6와 동일한 동결 prompt를 사용한다. 정적 테스트와 구분한다.
- [ ] 진입점을 짧은 trigger/정확한 파일/필수 차단 조건으로 정리하고 owner 출력 형태는 보존한다. 모든 코어 파일을 일괄 1800 tokens로 자르는 변경은 하지 않는다.
- [ ] 전체 투영 bootstrap은 파일로, 이후 읽기는 명시적 --view focus로 문서/예제를 바꾼다. prepare/render 명령에는 원래 full 파일을 유지한다.
- [ ] Codex Imagen에서는 비사용 Higgsfield runtime/quote를 요구하지 않게 정본 예외를 일치시킨다. Higgsfield 적격 영상/음향/3D 비용·동의 규칙은 유지한다.
- [ ] 외부 ai-delegation-loop는 삭제/대체/설치하지 않는다. 동일 세션의 설치 소스가 바뀌지 않은 반복 실패 조회만 줄이고 정확한 unresolved scope를 유지한다.
- [ ] **GREEN:** `python3 -m pytest scripts/test_staged_loading_contracts.py scripts/test_routing_table_lint.py scripts/test_routing_regression.py scripts/test_storyline_continuity_gate.py scripts/test_audio_default_policy.py scripts/test_guide_integration.py scripts/test_video_pack_boundary.py -q`로 실제 경로/참조·라우팅·연속성·오디오·패키지 회귀를 실행한다. 실제 단독 문서 로드도 native reference gate를 우회하지 못하게 한다.
- [ ] 동시 출시가 필요한 새 파일/포인터/테스트를 같은 로컬 체크포인트에 포함한다.

### Task 6: 총 읽기량·행동 동등성·최종 검토

**Files:**
- Create: `qa/staged-loading/{before-after.json,verification.md}` 및 실제 실행한 trace/선별 증거.
- Change only if required: T1 측정기/집중 테스트. 기존 dirty routing harness는 제외.

**Interfaces:**
- 동일 host/model/도구·동결된 case inputs로 baseline/candidate를 비교한다. source fingerprint와 사용한 버전/출력량/실행 상태를 기록한다.
- 평가자는 사용자가 요청한 산출물과 scope만 전달한다. 파일 목록/정답 owner/필수 참조 정답을 미리 알려 주지 않는다.
- 정적 file union, 실제 returned-text tokens, unique-read tokens, 모델 usage(노출될 때), 도구/불필요한 질문 수, 기능/차단 판정을 분리한다.

- [ ] 전체 `python3 -m pytest -q`, `python3 scripts/check_versions.py`, diff whitespace/전체 링크·legacy anchor/ownership coverage 검사를 실행한다. 모든 실패/skip/미실시를 이름과 이유로 보고한다.
- [ ] 고정 skeleton의 focus 100샷 ≤6000, 10→100 증가 ≤256 reference tokens를 확인한다. 전역 owner/필수 이력 확장 fixture도 별도로 검사한다.
- [ ] 파일 합집합 프로필의 조명 ≥35%, 일반 텍스트 콘티 ≥25% 감소를 확인한다. 실제 trace의 총 읽기 증가나 필수 슬롯 누락이 있으면 성능 목표 달성으로 세지 않는다.
- [ ] **승인된 행동 평가만 실행:** 20개 대표 case baseline/candidate 각 1회, lighting/board-full-text는 추가 각 4회씩 반복해 두 arm에 각 5회가 되게 한다. 총 최대 56개 fresh-context read-only probe. 원문 trace/코드 결과를 사람이 대조하며 single sample/구조 pass로 29개 실제 준수를 보장하지 않는다.
- [ ] 모델/예산 승인 없이 위 56개를 자동 실행하지 않는다. 제한된 probe만 허용되면 그 범위만 보고하고, 누락된 행동 수락 게이트는 blocked/unverified로 남겨 완료 주장을 하지 않는다.
- [ ] native 구현이면 구현과 분리된 fresh-context 최종 리뷰 1회를 수행한다. Important/Critical은 재현 RED→GREEN과 전체 suite로 한 번의 fix pass를 수행한다. 설계와 다른 임의 범위 확대는 하지 않는다.
- [ ] 설계 목표/불변 조건/잔여 blocker/로컬 커밋/남은 dirty 파일을 보고한다. 원격 push/실제 설치 sync는 별도 승인 전 실행하지 않는다.

## 실행 인계·승인 범위

현재 사용자는 상세 설계를 승인하고 작업 진행을 요청했다. 이 계획은 그 설계를 실행 단계로 구체화한 문서이며, 계획 인계 확인을 받기 전 생산 코드는 변경하지 않는다.

**추천 방식:** native — 이 세션에서 직접 task별 RED→GREEN으로 구현하고 마지막에 독립 리뷰 1회. 기존 dirty 작업 보호를 위해 새 격리 worktree가 적합하다. clean baseline의 Git 내용과 이번 소유 spec/plan/필요한 audit fixtures만 가져오고 원본 작업 폴더·설치 링크는 건드리지 않는다.

승인 시 구현/검증과 소유 파일의 로컬 체크포인트 커밋을 포함하는지 명확히 한다. 56개 행동 probe의 모델/예산은 별도 실행 gate로 유지한다. 원격 푸시/배포는 별도 요청 전 하지 않는다.

## Self-review

- Spec §4 인터페이스/호환/의존성/출력/실행 금지 → T2.
- Spec §5 공통·보드 정본/legacy anchor → T3/T4, 실제 소비 경로 → T5.
- Spec §6 매체/저장·실행자·의존성 정합 → T5.
- Spec §7 소비 재사용·source truth, §8 측정/행동/수락 → T1/T6.
- Spec §9 격리/범위/단계 출시·25/4 소유 경계 → Global Constraints와 T6.
- 모든 shared 인터페이스의 명칭/포맷은 T1/T2에서 정의하며 후속 task는 그것을 소비한다. 성능 수치는 목표이고 성공 판정은 필수 정보 보존과 실제 검증에 종속된다.
