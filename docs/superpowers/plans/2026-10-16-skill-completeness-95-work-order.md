# Skill Completeness 95% Upgrade Work Order

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Bring the 24-skill corpus to a defensible mean score of at least 4.75/5 under the existing fixed rubric, with evidence and behavior checks rather than wording-only score inflation.

**Architecture:** Keep the 24-skill inventory and rubric fixed. Upgrade each skill in its existing owner file, add domain-specific acceptance gates and blocker behavior, then attach source provenance only where craft claims rely on external materials. Validate with frozen prompts, package checks, and independent rescoring. Do not duplicate ownership or add new micro-skills merely to raise scores.

**Tech Stack:** Markdown skill packages, existing `scripts/check_versions.py`, existing pytest suite, frozen prompt QA artifacts in `qa/2026-10-16-corpus-audit/`.

**Spec:** `qa/2026-10-16-corpus-audit/rubric-definition.md`; evidence and current scorecard: `qa/2026-10-16-corpus-audit/rubric.md`; inventory: `qa/2026-10-16-corpus-audit/inventory.md`.

**Execution authority:** 아래 `## 실행 작업지시서 — 95% 완료 계약`이 현재 실행 기준이다. 위상별 기존 설계는 유지하되, 아래 명시한 정정·책임·검증·완료 계약이 충돌 시 우선한다. 이 문서는 실행 설계이며, 체크박스나 목표 점수는 완료 증거가 아니다.

## Global Constraints

- Preserve the 24 independently installed skill owners and existing routing; no new skills or duplicate coordinator contracts.
- Score only against the fixed anchors in `qa/2026-10-16-corpus-audit/rubric-definition.md`.
- 5 requires every load-bearing craft claim to have an addressable citation, explicit `READ-PARTIAL`/`READ-FULL` scope, and an exercised verification record.
- Unread/extraction-failure sources cannot support 5; mark uncertainty or keep the score lower.
- Keep the current working-tree changes; inspect and preserve them. Do not reset, revert, or overwrite concurrent work.
- Change only files enumerated in the task being executed and required package metadata; update version fields consistently using repository conventions.
- Freeze rubric and prompt bytes before edits; baseline before arm must match the same 24 skills and all frozen test IDs as post arm.
- Do not report 95% unless the mean is ≥4.75 and all required evidence/QA gates pass.

## Review Focus

- Missing or inaccessible source material: mark claims unsupported/partial and do not silently infer a book rule.
- User asks for generation/action when skill is advisory or read-only: block side effects and clarify/route rather than perform.
- Incomplete brief, conflicting constraints, or unresolved technical inputs: state exact blocker and do not fabricate missing decisions.
- Overlapping skill responsibilities: route to the existing canonical owner and avoid duplicate output contracts.
- Failed or unavailable test environment: mark unverified; do not count as a pass or score-5 evidence.

---

## Target score distribution

24 scores have a maximum mean of 5.00. A mean ≥4.75 requires a total ≥114 points. Operational target: **18 skills at 5 and 6 skills at 4 = 114/120 = 4.75**. Stretch target: all 24 at 5. A 4 score is not a placeholder: it must satisfy all score-4 anchors and identify the specific remaining evidence gap. Do not force every skill to 5 if source evidence cannot support it; report the achieved mean honestly.

## File map

- Modify each listed owner `SKILL.md` for scope, procedure, output, acceptance, blocker and boundary contracts.
- Modify a skill's existing references only when craft provenance or domain-specific acceptance detail belongs there; source index remains `video-production-assets/references/sources.md` for the shared production-craft library.
- Update `manifest.json`, `CHANGELOG.md`, `README.md`, and package/skill version fields only as repository conventions require.
- Add/update QA artifacts under `qa/2026-10-16-corpus-audit/`; keep frozen prompts and baseline evidence immutable.
- Do not delete references or consolidate owner skills as part of this work order unless a separate reviewed change explicitly authorizes it.

## Phase 0 — Establish defensible baseline

### Task 0.1: Freeze tree and baseline inputs

**Files:** `qa/2026-10-16-corpus-audit/prompts.sha256`, `baseline-prompts-exact.md`, `baseline-matrix.md`, `baseline-matrix-vpa.md`, `rubric-definition.md`; QA results files.

- [ ] Record current HEAD and full worktree state; distinguish pre-existing/uncommitted changes and protect all of them.
- [ ] Verify prompt hashes against `prompts.sha256`; any mismatch blocks comparison until reconciled without changing prompts.
- [ ] Run repository version check and pytest using a fresh basetemp; record exact commands and outputs.
- [ ] Run the full frozen all-skill before-arm in fresh sessions: M-01..M-24, V-01..V-28, VC-1..VC-3, VP-1, VP-2, VS-1, VO-1, S1a, S1b. Preserve verbatim outputs and score each with the frozen assertions.
- [ ] If external quota or runner failure blocks any case, list each unrun ID; do not claim a complete baseline or substitute a different case.

**Acceptance:** All 61 rows have an observed result, or the baseline is explicitly marked incomplete and 95%-target comparison is blocked. Hashes match; versions and tests recorded.

## Phase 1 — Bring every skill to explicit score-4 contract

For each skill below, update its own `SKILL.md` with: trigger/use scope; excluded work; required inputs; ordered procedure; named output; fail-able acceptance checks; named blockers and no-silent-substitution behavior. Use domain language, not a copied generic checklist. Add only acceptance items that can be inspected in the resulting artifact or observed in the interaction.

### Task 1.1: Craft planning, ideation, and content strategy

**Files:** `topic-demand-selection/SKILL.md`, `creative-production/SKILL.md`, `video-production-assets/SKILL.md`, `developing-video-synopses/SKILL.md`, `storytelling-with-still-images/SKILL.md`, `recording-production-history/SKILL.md`.

- [ ] `topic-demand-selection`: define decision inputs (audience, channel, objective, evidence window), comparison procedure, evidence labels, ranked output schema, and acceptance checks that every recommendation cites evidence/uncertainty and is comparable on the chosen criteria; block when audience/objective/evidence scope is absent.
- [ ] `creative-production`: define coordinator-only boundary, stage selection and handoff; acceptance checks confirm one active stage, owner, artifact, reviewer acceptance distinct from user/media approval, and no duplicated specialist output.
- [ ] `video-production-assets`: add top-level acceptance contract linking specialist modules; require status (`pass`, `pass_with_notes`, `needs_revision`, `unverified`), evidence scope, unresolved blockers, and explicit separation of preproduction acceptance, media execution authorization, and publication authorization.
- [ ] `developing-video-synopses`: require causal synopsis/beat map, fact-status labels per factual claim, explicit unresolved assumptions, and a reviewer-checkable beat-map QA; repair suggestions remain proposals until authorized.
- [ ] `storytelling-with-still-images`: require image-by-image cue/continuity contract, transitions and timing, evidence of legibility at intended viewing size, and checks that each still advances the specified narrative rather than merely repeating content.
- [ ] `recording-production-history`: define required event/evidence fields, source links, chronology and confidence; acceptance checks every claim maps to evidence and distinguishes fact, interpretation, and unknown; explicitly exclude inventing missing production history.
- [ ] Add only verified external-craft citations; mark authored workflow rules as `설계 확장` and do not claim book provenance without read evidence.

**Acceptance:** All six satisfy score-4 observable anchors; coordinator/specialist boundaries remain consistent with the existing routing references.

### Task 1.2: Camera, spatial design, and previsualization

**Files:** `camera-spatial-design/SKILL.md`, `camera-motion-reference-analysis/SKILL.md`, `ai-camera-control/SKILL.md`, `blender-previsualization/SKILL.md`, `orchestrating-video-preproduction/SKILL.md`.

- [ ] `camera-spatial-design`: make the location/spatial contract inspectable (axes, dimensions or uncertainty, subject/camera positions, occlusions, continuity constraints); acceptance checks that proposed views fit the same space and label unknown geometry.
- [ ] `camera-motion-reference-analysis`: specify reference input requirements, temporal segmentation, camera-vs-subject motion separation, observable evidence, confidence and output table; acceptance requires timestamps for every claimed move, no unsupported lens/motion certainty, and explicit unreadable intervals.
- [ ] `ai-camera-control`: define control intent, camera path/constraints, coordinate assumptions, handoff format and execution boundary; acceptance verifies path is compatible with spatial contract and unknown controls are flagged, not guessed.
- [ ] `blender-previsualization`: specify scene/input prerequisites, reproducible scene setup, camera/render outputs, naming and handoff; acceptance checks scene opens, intended framing is visible, scale/axes are stated, and missing assets or unsupported geometry are reported.
- [ ] `orchestrating-video-preproduction`: retain existing acceptance gate and add a handoff completeness check across required artifacts, owners, dependencies, and unresolved technical inputs; do not imply generation, spend, or publication permission.
- [ ] Cite camera/lighting sources only where exact passages have been read; distinguish measured reference observations from inferred camera properties.

**Acceptance:** Five skills satisfy score-4 anchors. Cross-skill handoff uses one spatial source of truth and the camera reference skill does not promise unavailable metadata.

### Task 1.3: Character, storyboard, and story design

**Files:** `designing-character-personas/SKILL.md`, `designing-video-character-sheets/SKILL.md`, `storyboarding-video/SKILL.md`.

- [ ] `designing-character-personas`: define persona-purpose, audience/context inputs, evidence-vs-invention labels, voice boundaries and reviewer gate; acceptance checks each trait is tied to evidence or explicitly marked proposed, with contradictions/unknowns visible.
- [ ] `designing-video-character-sheets`: preserve existing gates; make sheet identity, visual invariants, variants, voice/persona dependency and uncertainty explicit; check each requested sheet is returned and no real-person fact is invented.
- [ ] `storyboarding-video`: preserve board schema; acceptance checks indexed shots, actionable visual/camera/action/audio fields, continuity and unresolved requirements; unresolved requirements block only the stage they affect and are listed by index.
- [ ] State the persona-to-character-sheet seam: persona provides motivation/voice inputs; sheet owns visual identity and visual invariants. Avoid duplicate character canon.

**Acceptance:** Three skills score 4 or better; storyboard and sheet output contracts remain compatible with downstream Higgsfield workflow.

### Task 1.4: Higgsfield asset and generation provider skills

**Files:** `higgsfield-brandkit/SKILL.md`, `higgsfield-generate/SKILL.md`, `higgsfield-marketplace-cards/SKILL.md`, `higgsfield-product-photoshoot/SKILL.md`, `higgsfield-soul-id/SKILL.md`, `higgsfield-video-explainer/SKILL.md`, `higgsfield-video-replicate/SKILL.md`, `higgsfield-websites/SKILL.md`, `higgsfield-youtube-thumbnail/SKILL.md`, `community-shorts-stills-pipeline/SKILL.md`.

- [ ] For every provider skill, add an explicit acceptance gate tied to its real deliverable and its existing app/tool contract; do not invent provider capabilities.
- [ ] `higgsfield-brandkit`: gate asset identity/brand constraints, palette/logo use, permitted variants, and explicit missing-brand-input blockers; preserve deterministic script and failure policies.
- [ ] `higgsfield-generate`: gate model/input compatibility, user-confirmed generation intent, parameters and destination, result/status handling, and error visibility; read-only or analysis requests must not trigger generation.
- [ ] `higgsfield-marketplace-cards`: gate selected product/brand inputs, card content and asset eligibility; distinguish browse/quote from generation authorization.
- [ ] `higgsfield-product-photoshoot`: gate product identity fidelity, requested views, prohibited invented product claims, and missing-reference blockers.
- [ ] `higgsfield-soul-id`: gate identity/reference prerequisites, consent/authorization boundary where applicable, training result handoff, and failure/insufficient-reference reporting.
- [ ] `higgsfield-video-explainer`: add phase-level acceptance for source/script, storyboard, generation, audio, and final QA; identify which phases are advisory versus paid/side-effecting and require the relevant explicit user intent.
- [ ] `higgsfield-video-replicate`: gate reference analysis, board contract, selected model/parameters, fidelity limitations and final output QA; do not treat reference inspection as generation consent.
- [ ] `higgsfield-websites`: gate requirements, structure/content, responsive/accessibility checks, persistence/security boundaries, deployment authorization, and live URL verification; report unavailable integrations as blockers.
- [ ] `higgsfield-youtube-thumbnail`: retain intake/concept/post-render gates; make legibility, crop-safe composition, claim fidelity and final asset check explicit.
- [ ] `community-shorts-stills-pipeline`: gate source-media eligibility, stage outputs, render verification, delivery files, and script exit/error reporting; do not infer successful delivery from file creation alone.
- [ ] Validate every tool/model/API claim against current provider docs or tool contract; add cited version/date or mark provider-dependent.

**Acceptance:** Ten skills score 4 or better; no skill adds a paid or external side effect without its documented authorization gate.

## Phase 2 — Evidence-bound upgrade to score 5

### Task 2.1: Source audit for craft-bearing references

**Files:** `video-production-assets/references/sources.md` and relevant references under `video-production-assets/references/`, `creative-production/references/`, plus other skill references only where their own content asserts external craft claims.

- [ ] Inventory every load-bearing craft claim in all 24 installed skills and references; classify as source-derived, provider-contract-derived, authored design extension, or unsupported.
- [ ] For source-derived claims, cite exact path + line/page, edition/rendition identity and byte size where required by the existing source standard; attach `READ-PARTIAL` or `READ-FULL` to the citation.
- [ ] Confirm cited passage supports the claim at its actual scope. Narrow overgeneralized claims; mark contextual findings as contextual; remove unsupported causal guarantees.
- [ ] For authored operational procedures, label as design extension; do not manufacture a book citation.
- [ ] For unread or extraction-failed sources, mark the dependent claim unverified and leave that skill below 5 unless independent evidence resolves it.
- [ ] Keep the shared source index canonical; do not create competing provenance ledgers in each skill.

**Acceptance:** Every score-5 candidate has no uncited load-bearing craft claim; every citation resolves to a read passage and states read scope. Unresolved claims are enumerated, not concealed.

### Task 2.2: Deduplicate ownership and payload without changing owners

**Files:** Owner skills and existing routing/reference files identified by `rubric.md` modifiers: creative-production/video-production-assets; camera-spatial-design/blender-previsualization; storyboarding-video/higgsfield-video-replicate; persona/sheet boundary; camera modules; still-image/shorts pipeline.

- [ ] For each pair, name canonical owner, consumed contract, and non-owner behavior in both skill files or existing routing documentation.
- [ ] Remove only duplicated normative rules; preserve necessary local usage instructions and installed skill entry points.
- [ ] For large reference payloads, identify exact default-load vs on-demand paths; do not delete needed content or links. Reduce load cost only when callers can still retrieve the complete material.
- [ ] Verify all relative links and entry-point discoverability after any movement.

**Acceptance:** No conflicting owners or contradictory outputs; no broken links; all 24 installed skills remain reachable.

## Phase 3 — Behavioral proof and final scoring

### Task 3.1: Frozen post-arm execution

**Files:** `qa/2026-10-16-corpus-audit/post-results.md`, `gate-status.md`, `rubric.md`, `final-report.md`.

- [ ] Re-run the exact same 61 frozen prompts byte-for-byte in fresh sessions against the final tree.
- [ ] Score with unchanged assertions. Report pass, fail, unscored, environment failure separately; include concise verbatim evidence and artifact locations.
- [ ] For every failure, fix only within scope, update the relevant skill, and re-run the affected frozen case plus all full regression checks; preserve initial and final outcomes.
- [ ] Independently rescore all 24 skills using the unchanged rubric, with score evidence and modifiers per row.
- [ ] Calculate mean as sum of all 24 scores / 24; show distribution and list every skill below 5 with exact missing score-5 evidence.

**Acceptance:** All frozen cases executed or the target is explicitly unverified; no environment failure counted as pass. A 95% claim requires mean ≥4.75, 61/61 observed outcomes, zero score-5 rubric violations, passing package/version/link/test checks, and a recorded independent review.

### Task 3.2: Package and change documentation

**Files:** `manifest.json`, `CHANGELOG.md`, `README.md`, all edited skill frontmatter/version fields.

- [ ] Bump only edited skills and package metadata per existing conventions; check `scripts/check_versions.py`.
- [ ] Update changelog with behavior-level changes and note any score target not reached; do not claim completion based on planned work.
- [ ] Verify relative links, pytest suite, frozen prompt hashes, and focused smoke scenarios for each changed behavior.
- [ ] Remove temporary scripts/artifacts not part of the audit record; preserve QA evidence required to reproduce the score.

**Acceptance:** Version consistency, tests and links pass; changelog claims match observed outcomes; worktree retains unrelated user edits.

## Required delivery report

The implementer returns: baseline and post score distributions; mean calculation; per-skill score and evidence; exact changed files; frozen-prompt pass/fail/unscored table; version/test/link/hash verification output; unresolved source or runner blockers; and whether ≥95% was actually reached. No assertion of success from document shape alone.

## 실행 작업지시서 — 95% 완료 계약

### 1. 무엇이 완료인가

사용자는 “24개 스킬의 기존 완성도 루브릭 평균 95% 이상”을 요청했다. 생성물의 흥행률·모델 정확도·모든 가능한 입력의 성공률을 뜻하지 않는다.

완료 판정은 다음 조건을 **모두** 만족해야 한다.

1. 기존 24개 스킬을 그대로 평가한다. 분모 축소, 쉬운 스킬 추가, 점수 반올림으로 달성을 만들지 않는다.
2. `rubric-definition.md`의 정수 점수 0~5를 그대로 적용한다. 총점 ≥114/120, 평균 ≥4.75/5, 백분율 ≥95.00%. 운영상 모든 스킬을 최소 4점까지 검증한다.
3. 5점 스킬은 자기 파일과 트리거로 읽는 참조의 핵심 주장에 대해 근거 위치·읽은 범위·실행 검증을 제시한다. 근거 없는 핵심 주장을 남겨 두고 제목만 추가해서 5점을 주지 않는다.
4. 최종 동일 트리에서 정식 행동 평가 61개가 전부 실행되고 PASS이다. `PASS*`, `READFAIL`, 환경 오류, 빈 출력, 미실행은 PASS가 아니다. 점수 평균과 행동 통과율은 별개로 보고한다.
5. 영향을 받은 정상 경로와 경계 경로의 실제 스모크, 버전 검사, 전체 기존 테스트, 상대 링크 검사, 독립 재채점이 통과한다.
6. 최종 점수·증거·변경 파일·남은 제한을 재현 가능한 형태로 인계한다. 저작권 원문·비밀키·개인정보를 QA 산출물에 복제하지 않는다.

목표는 우선 24개 모두 5점을 시도하는 것이다. “18개 5점 + 6개 4점 =114점”은 가능한 최소 분포 예시이지, 특정 6개를 검증하지 않아도 된다는 허가가 아니다. 4점 잔류 스킬도 정확한 미충족 근거와 사용자 영향이 있어야 한다.

### 2. 이전 기록에서 바로잡을 사항

| 항목 | 확인한 사실 | 실행 지시 |
|---|---|---|
| 평가 개수 | `_blocks.json`: 60개 키 = 행동 59개 + `Scoring` 안내문. S1a/S1b는 `baseline-prompts.md`에 별도 존재. 합계 61개 | `Scoring`은 평가 대상에서 제외하고 S1a/S1b를 포함한다. 59·60·61은 서로 다른 집계이며 정식 분모를 바꾸지 않는다 |
| 대체 실행 | 60개 대체 응답에는 `Scoring`이 있고 S1a/S1b가 없다. 모델·문맥 주입·도구 조건도 다르다 | 탐색 기록으로 보존한다. 정식 평가, 성공률, 개선율에 합산하지 않는다 |
| 5점의 읽기 요건 | 고정 루브릭은 인용별 `READ-PARTIAL` 또는 `READ-FULL`을 허용한다 | 전권 정독을 필수화하지 않는다. 인용 구간을 직접 읽고 실제 지원 범위를 명시한다 |
| 출처 헤딩 수 | 기존 19/154는 당시 구조 통계다 | 현재 핵심 주장별 감사를 다시 한다. 헤딩 154개 생성이나 모든 책 읽기를 목표로 삼지 않는다 |
| 현재 점수 | 3.29/5는 이전 점수표이며 이후 Acceptance 추가에 대한 독립 재채점이 없다 | 현재 상태에 대한 새 측정값을 만들고 역사적 점수와 구분한다 |
| 기존 post 결과 | `post-results.md`는 유효 23/61과 실행 오류 38개를 기록한다. 다른 보고의 25/61은 패치 전 결과를 포함한다 | 서로 다른 트리·시점 결과를 합쳐 최종 arm으로 만들지 않는다. 최종 트리 전체를 새로 실행한다 |
| Orca 부재 | 이 세션의 `orca` 실행은 command not found였다. 과거 Herdr pane의 현재 상태는 미확인이다 | 특정 실행 환경의 실패를 모든 작업의 불가능으로 확대하지 않는다. 현재 실제 도구·설치 경로·관리 지침부터 확인한다 |

기존 baseline, frozen prompt, 해시 목록, raw response는 역사 기록으로 보존한다. 잘못된 설명은 새 정정 문서에서 명시하고, 원본 기록을 성공한 것처럼 고쳐 쓰지 않는다. 이전 트리를 복원할 수 없으면 당시 대비 수치 개선율은 산출하지 않는다. 현 트리→수정 트리의 새 비교 arm을 만들 수는 있으나 역사적 baseline을 대체했다고 부르지 않는다.

### 3. 책임과 사용자 입력 계약

#### 3.1 내가 직접 처리할 일 — 사용자에게 재조사 요청 금지

- 저장소·기존 계획·24개 스킬·참조·도구 계약·소스 경로를 직접 탐색한다.
- 현재 변경 파일과 실행 환경을 기록하고 사용자 변경을 보존한다. 임의 reset/revert, 삭제, 강제 checkout, 전역 설정 변경을 하지 않는다.
- 직원 세션 생성, 업무 분할, 파일 소유권, 의존성, 진행 관리, 검토, 재작업, 통합을 맡는다.
- 평가 개수, 잘못된 캐시 재사용, 소스 인용, 스킬 규칙, 테스트·도구 문제 중 저장소에서 고칠 수 있는 것을 수정한다.
- 사용 가능한 로컬 자료와 합법적으로 접근 가능한 공식 공개 문서를 먼저 읽는다. 사용자에게 같은 파일을 다시 보내 달라고 하지 않는다.
- 외부 로그인·설치 권한·누락 자료가 실제로 필요한 경우에만 아래 형식으로 한 번에 요청한다.
- 정상/경계 검증, 전체 평가, 독립 점수, 버전·문서 갱신, 최종 증거 인계를 맡는다. 사용자가 직원별 지시·진행률 계산·채점을 할 필요가 없다.

#### 3.2 사용자만 제공하거나 실행할 수 있는 입력

**지금 무조건 제출할 자료는 없다.** 기존 저장소와 읽을 수 있는 자료로 먼저 진행한다. 아래는 해당 조건이 실제 확인될 때만 필요한 입력이며, 기본값으로 처리할 수 있으면 질문하지 않는다.

| 코드 | 필요한 조건 | 사용자 제공 내용 / 직접 할 일 | 내가 먼저 해야 할 진단 | 완료 확인 |
|---|---|---|---|---|
| U1 로그인·사용량 | 정식 모델 실행에서 인증/계정 사용량 오류가 발생 | 해당 CLI/앱에서 직접 로그인하거나 계정 사용량 회복. 다른 승인 계정을 쓰면 계정 사용 허가만 전달 | 실행 파일 경로·버전·오류·발생 시각을 기록하고 로컬 오류와 계정 오류를 구분 | 새 세션에서 저장소 읽기와 정확 응답 성공. 토큰·비밀번호는 채팅에 보내지 않음 |
| U2 권한·설치 | 실행 도구/Blender 부재 또는 보안 정책이 실제 실행을 차단 | 관리자가 필요한 설치·허용만 승인/실행. 새 전역 도구 설치는 배포처·권한·영향을 보고받은 뒤 승인 | 실제 경로 탐색, 현재 도구의 공식 지침 확인, 사용자 영역 실행 가능성 및 읽기 전용 모드 진단 | 도구가 현재 세션에서 실행되고 필요한 파일을 읽음. 보안 기능 전체 해제는 요구하지 않음 |
| U3 핵심 원문 | 핵심 주장을 지원하는 구간이 로컬/공개 공식 자료에서 모두 읽히지 않음 | 합법적으로 제공 가능한 원문/관련 페이지/텍스트와 판본 정보 또는 접근 가능한 경로 | 기존 소스 인덱스·추출본·중복 판본·공식 대체 근거를 확인. 필요한 문장과 범위를 특정 | 제공본의 파일 식별·바이트·해시·읽은 줄/페이지를 확인. 전권 정독이나 118권 전체 재제출 요구 금지 |
| U4 미디어·인물 권리 | 사용자 비공개 제품·실인물·기존 영상이 아니면 검증할 수 없는 경우 | 필요한 최소 참조 파일과 사용·편집·훈련 권한 범위 | 내가 만들 수 있는 합성 로컬 fixture 또는 공개 사용 가능한 fixture로 같은 규칙을 검증 가능한지 먼저 확인 | 파일이 실제 열리고 권한 범위 기록. 개인정보·실인물 훈련은 기본 금지 |
| U5 유료 실행 | live 제출 결과가 있어야만 입증할 수 있는 핵심 주장 때문에 114점 확보가 막힘 | `서비스 / 작업 종류 / 건별·총 상한 / 횟수 / 업로드 범위 / 허용 목적`을 명시한 승인. 결제는 서비스 UI에서 직접 | 비과금 조회·공식 계약 확인·로컬 검증으로 충분한지 확인하고 필요한 최소 실행만 견적화 | 견적과 승인 범위 일치 후 실행; 초과 시 중지. 기본 예산 0, 생성·훈련·배포·게시 금지 |
| U6 충돌하는 다른 작업 | 실제 살아 있는 다른 세션이 동일 파일에 쓰고 소유권 합의가 안 됨 | 해당 작업의 우선순위 또는 일시 중지 지시 | 세션·소유 파일·변경 내용을 확인하고 직접 소유권 조정 시도 | 파일별 writer 1명 확정. 오래된 `working` 표기만 보고 무기한 대기 금지 |

**사용자 요청 양식:** `입력 코드 / 막힌 작업·스킬·주장 / 시도한 경로와 정확 오류 / 필요한 최소 입력 / 입력이 없을 때 점수 상한 / 나머지 계속할 작업`. “환경을 복구해 주세요”처럼 진단 없는 포괄 요청은 금지한다.

**사용자 선택이 없을 때 기본값:** 현 24개 유지, 고정 루브릭 유지, 한국어 운영 보고, 비과금·비게시, 현 사용자 변경 보존, 소스 구간 선별 직접 읽기, 커밋·푸시·전역 설치 없음. 승인받은 정책으로 확정 가능한 범위는 재질문하지 않는다.

선택 입력을 한 번에 줄 경우 다음 형식을 쓴다. 비어 있는 값은 위 기본값이다.

```text
추가 자료 경로:
자료 사용 제한:
로그인/관리자 작업 가능 여부:
유료 검증 허용 범위와 총상한: 0
동시에 수정 중인 세션/파일:
별도 금지사항:
```

이 양식만 채우면 무조건 95%가 된다는 약속은 하지 않는다. 완료에는 실제 근거와 실행 성공이 필요하다. 대신 해결되지 않은 항목마다 필요한 입력·담당·검증·실패 시 분기를 아래 작업에 정의한다.

### 4. 산출물과 파일 소유권

기존 설계·역사 기록은 보존하고, 새 실행 증거는 `qa/skill-completeness-95/`에 분리한다. 아래 파일은 실행 시 생성할 산출물이며 이 작업지시서 작성만으로 생성됐다고 간주하지 않는다.

| 파일 | 담당 / 내용 |
|---|---|
| `execution-state.json` | 리더: 작업·직원·소유 파일·상태·의존성·증거·다음 행동·차단 요청 |
| `environment.md` | 런타임 담당: 실행 경로/버전, 네트워크·로그인·shell/file-read 결과, 보안 변경 유무 |
| `workspace-snapshot.json` | 리더: HEAD, dirty 파일과 내용 해시, 동시 writer, 시작 시점 스냅샷 식별 |
| `case-manifest.json` | 평가 담당: 정식 61개 ID, 원본 파일/블록 위치, prompt 해시, assertion 위치, evaluator 기록 |
| `claim-ledger.tsv` | 리더 통합: 모든 핵심 주장과 근거/검증 연결. 직원은 자기 slice TSV로 제출 |
| `source-requests.md` | 자료 담당: U3/U4 항목별 요청, 시도, 영향, 해결 결과. 이미 읽히는 자료 재요청 금지 |
| `runs/<run-id>/metadata.json` | 평가 담당: 트리 해시, 도구·모델·설정, prompt manifest 해시, 시작/종료, side-effect 정책 |
| `runs/<run-id>/<case-id>.json` | 평가 담당: 원문 prompt·응답·허용된 도구 실행 기록·오류·시간·return code·verdict·근거 |
| `smoke-results.md` | 리더: 스킬별 정상·경계 시나리오, 실제 산출물·검사 결과·미검증 범위 |
| `scorecard.json` | 독립 채점자: 스킬 ID·정수 점수·루브릭 근거·claim IDs·run IDs·modifiers·미충족 항목 |
| `final-report.md` | 리더: 점수 산식, 61개 판정, 패키지 검증, 수정 파일, 남은 4점의 사유, 최종 인계 |

정본 소스 인덱스는 기존 `video-production-assets/references/sources.md`를 유지한다. QA claim ledger는 추적·검토용이지 새 규칙 정본이 아니다. 독립 설치 스킬이 다른 스킬의 소스를 필요로 하면 기존 설치/링크 관례대로 접근성을 보장한다.

### 5. 직원 구성과 감독 계약

실행 리더는 나다. 작업을 통째로 다른 리더에게 넘기지 않는다. 동시 직원 수는 실제 런타임·계정 제한 내에서 조절한다. 다음은 독립 작업 단위이며, 단일 요청으로 관련 직원을 함께 배정한다.

| 직원 | 독점 쓰기 범위 | 구체 임무 | 제출 증거 |
|---|---|---|---|
| W0 실행·평가 | 새 평가 runner·manifest·자기 run 기록 | 파일 읽기가 가능한 fresh session 복구, 캐시 안전화, 61개 실행, 환경 오류 분리 | 정확 명령·raw output·트리/모델/prompt 식별 |
| W1 전략·서사 | creative-production, topic-demand-selection, developing-video-synopses, storytelling-with-still-images, recording-production-history의 파일 | 스킬별 정상/경계 계약과 주장 근거 감사·수정 | 자기 claim slice, 변경 이유, 스모크 시나리오 |
| W2 카메라·공간 | camera-spatial-design, camera-motion-reference-analysis, ai-camera-control, blender-previsualization, orchestrating-video-preproduction의 파일 | 공간→카메라→Blender seam, 관찰/추정 구분, 실제 로컬 실행 | 수치/렌더 산출물, 관찰 결과, 자기 claim slice |
| W3 캐릭터·보드 | designing-character-personas, designing-video-character-sheets, storyboarding-video의 파일 | 인물 사실/제안 구분, persona→sheet→board seam, output 검증 | 완성 텍스트 산출물과 경계 결과, 자기 claim slice |
| W4 제작 모듈·자료 | video-production-assets의 파일 | 모듈 01~28와 나머지 참조의 핵심 주장 검토, 근거 구간 대조 | 모듈별 claim slice·지원 구간·미지원 목록 |
| W5 provider 자산 | higgsfield-brandkit, higgsfield-generate, higgsfield-marketplace-cards, higgsfield-product-photoshoot, higgsfield-soul-id의 파일 | 실제 provider 계약 확인, 입력/동의/비용/결과 상태 경계 | 공식 계약 위치·확인 시각·비과금 실행 증거 |
| W6 provider 영상·웹 | higgsfield-video-explainer, higgsfield-video-replicate, higgsfield-websites, higgsfield-youtube-thumbnail, community-shorts-stills-pipeline의 파일 | preset/continuity/생성·배포·게시 경계와 로컬 파이프라인 검증 | 공식 계약 위치·로컬 산출물·자기 claim slice |
| R 독립 검토·채점 | 구현 파일 수정 금지; 자기 review·score 초안만 | 다른 직원의 완료 주장 기각 가능. 루브릭 그대로 전 스킬 재채점 | 각 점수의 파일/구간·실행 증거·반례·결함 목록 |

공유 파일 `manifest.json`, `README.md`, `CHANGELOG.md`, 통합 QA 원장과 버전 통합은 리더만 쓴다. W4가 쓰는 공유 `sources.md`에 필요한 추가는 다른 직원이 요청으로 전달한다. 다른 직원 소유 파일을 직접 고치지 않는다.

직원 지시문에는 `목표 / 소유 파일 / 비목표 / 소비 계약 / 반환 계약 / 완료 기준 / 금지 부작용 / 증거 형식`을 모두 넣는다. 전 직원은 중간 전체 테스트·formatter를 돌리지 않고, 통합 후 리더가 한 번 실행한다. 확인이 필요한 새 규칙은 사례와 예상 결과를 제출한다.

직원 작업 상태는 `pending → running → review → accepted` 또는 `rework`, 외부 입력 필요 시 `blocked`이다. 완료 통보는 `review` 진입일 뿐 승인 아님. 리더는 산출물 확인과 통합 스모크 뒤에만 `accepted`로 바꾼다.

진행 감시는 완료 이벤트·메시지·산출물로 한다. 의미 없는 반복 polling, 서로를 기다리는 두 리더, 파일별 writer 중복을 금지한다. 직원이 막히면 리더가 다른 독립 작업을 계속하고, 필요한 최소 입력만 요청한다.

현재 지침이 특정 관리 런타임을 강제하면 그 런타임을 임의 대체하지 않는다. 실행 파일 부재 때는 공식 설치·실행 경로와 권한을 확인해 U2로 좁힌다. 런타임 부재는 직원 세션 생성의 차단일 수 있지만, 독립적인 읽기·설계·정본 데이터 정리까지 자동 차단하지 않는다. 런타임 변경에 정책/사용자 결정이 필요하면 그 선택만 요청한다.

### 6. 실행 순서와 작업 패키지

#### T0 — 현재 상태와 정식 평가 입력 고정

**담당:** 리더 + W0. **수정:** 새 QA 산출물만. **입력:** 기존 audit와 현 worktree.

- [ ] 현재 HEAD·dirty 파일·해시·실제 동시 writer를 1회 기록한다. 사용자 변경을 되돌리지 않는다.
- [ ] 59개 frozen text fence와 S1a/S1b의 실제 바이트를 읽어 case manifest를 만든다. `Scoring` 제외, ID 중복 없음, 합계 61, assertion 위치 있음 확인.
- [ ] `prompts.sha256`을 대조한다. 불일치 시 원본 수정 대신 원인과 사용 snapshot을 기록하고 비교를 보류한다.
- [ ] 현재 24개 설치 owner와 트리거별 참조를 열거한다. 예전 ref 수·버전을 현재값으로 오인하지 않는다.
- [ ] Acceptance가 이미 추가된 15개는 내용부터 확인한다. 중복 헤딩/복사 게이트를 또 추가하지 않는다.

**완료:** 24개·61개 ID·원본 해시·현재 트리가 재현 가능하다. 이전 자료와 다른 현재 상태가 명시된다.

#### T1 — 실행 경로와 평가 캐시 신뢰성

**담당:** W0. **기존 조사 파일:** `_run_baseline.py`, `_finish_post_arm.py`, `post-results.md`.
**신규 구현:** `qa/skill-completeness-95/run_cases.py`, `test_run_cases.py`. 기존 역사 runner는 보존한다.

- [ ] 현재 실제 도구를 탐색하고 공식 help/schema를 읽는다. 버전 미확인 명령·플래그를 추측하지 않는다.
- [ ] `PROBE-OK` 응답만으로 통과시키지 않는다. 새 모델 세션이 실제 저장소 파일을 읽고 해당 구간을 반환할 수 있는지 먼저 확인한다.
- [ ] `helper_unknown_error`, 계정 사용량, network/MCP transport, 권한, 도구 부재를 서로 다른 원인으로 기록한다. 이미 보고된 실패를 확인하려는 동일 재실행은 금지하고 변경한 조건/진단 목적을 남긴다.
- [ ] 새 runner CLI는 `python -X utf8 qa/skill-completeness-95/run_cases.py --manifest <path> --run-dir <path> [--case <ID>]`로 고정한다. 기본 1개 동시 실행, 파일 읽기 허용, 생성/훈련/업로드/배포/게시 금지. 기존과 다른 실행 프로필이면 새 series로 표시한다.
- [ ] 캐시 식별은 case ID만이 아니라 prompt 해시·트리 해시·실행 프로필·모델 식별에 묶는다. 모델이 불명확하면 명시하고 역사 비교는 하지 않는다.
- [ ] 빈 stdout, nonzero exit, timeout, file-read 실패는 완료 캐시로 재사용하지 않는다. 실패 기록을 지우지 말고 새 attempt로 남긴다.
- [ ] runner의 경계 테스트: 누락/중복 ID 거부, `Scoring` 제외와 S1 포함, 트리/모델/prompt 변경 캐시 무효화, 빈 출력 실패, 기존 실패 attempt 보존. 테스트는 소비자가 잘못된 평가 결과를 받는 오류를 검출해야 한다.
- [ ] 서로 다른 유형 M-03·M-04·S1a를 실제 fresh session에서 실행해 파일 읽기·인용·read-only 경계를 관찰한다. 정상화 후 전체 61개 실행.

**완료:** 실제 파일 읽기와 61개 실행이 가능한 경로. 환경 문제면 U1/U2에 구체 요청하고 나머지 증거 작업은 계속한다. 새로운 조건의 평가를 옛 Codex arm과 동등하다고 부르지 않는다.

#### T2 — 핵심 주장 전수 감사와 근거 결속

**담당:** W1~W6, 리더 통합. **수정:** 각 소유 skill/reference, W4의 기존 source index.

`claim-ledger.tsv` 열은 `claim_id, skill, file, section, claim_summary, class, load_bearing, source_id, rendition_path, source_sha256, source_bytes, locator, read_state, support_scope, verification_id, disposition`으로 고정한다.

- [ ] `SKILL.md`와 실제 트리거가 읽는 모든 참조의 핵심 규칙을 감사한다. 헤딩 존재 여부가 아닌 주장 내용 기준이다.
- [ ] class는 `source-derived / provider-contract / authored-design / unsupported` 중 하나로 구분한다.
- [ ] source-derived는 실제 구간을 읽고 동일 판본 path·hash·bytes·line/page·`READ-PARTIAL|READ-FULL`·지원 범위를 기록한다. 그림/표를 근거로 쓰면 실제 페이지를 확인한다.
- [ ] provider-contract는 공식 도구/API 문서 위치·해당 field/제약·확인 시점·관찰한 버전을 기록한다. 책 출처로 API 기능을 입증하지 않는다.
- [ ] authored-design은 자체 설계임을 명시하고 규칙을 실행으로 검증한다. 외부에서 가져온 craft 주장을 자체 설계로 재라벨링하여 출처 의무를 피하지 않는다.
- [ ] unsupported는 무조건 삭제하지 않는다. 지원 가능한 범위로 좁히거나 정당한 근거를 찾는다. 기능을 축소해야 하면 영향과 사용자 결정을 먼저 제시한다.
- [ ] 소스가 unread면 그 소스가 핵심인 스킬은 루브릭 상한 3을 적용한다. 주장에 무관한 unread 책 때문에 모든 스킬을 일괄 낮추지 않는다.
- [ ] 인용 위치가 실제 문장을 지원하는지 R이 직접 대조한다. 단순 출처 헤딩·인용 숫자·전체 시험 통과만으로 5점을 인정하지 않는다.

**완료:** 5점 후보에 미추적 핵심 주장 없음. 본문 없는 Malkiewicz 등 실제 누락은 U3에 특정 구간·의존 스킬·대안 조사 결과와 함께 기록한다.

#### T3 — 스킬별 구체 수정 및 스모크 지시

**공통:** 아래 각 행은 기존 `SKILL.md` 및 해당 trigger의 기존 참조를 대상으로 한다. 이미 충족한 항목은 재작성하지 않고 증거를 붙인다. 각 행의 정상 사례는 합성 입력으로 내가 만들고, 경계 사례는 정식 평가와 별도 스모크에 연결한다.

| 스킬 / 담당 | 보완할 구체 내용 | 실제 확인할 정상 경로와 경계 |
|---|---|---|
| creative-production / W1 | 단일 stage·owner·artifact·approver, review/accept/spend/publish 분리, shared 원칙의 canonical owner 명시 | 하나의 courier 소재를 article/short 제작 단계에 인계; 즉시 게시·수락 대행 요구 거절 |
| topic-demand-selection / W1 | 데이터 기간·단위·대상 비교 가능성, missing-data 순위의 불확실성, 증거별 권고 추적 | 12k/4k/no-data 입력에서 관측 두 항목만 수치 비교; 근거 없는 수요값과 0 추정 금지 |
| video-production-assets / W4 | 01~28 모듈 및 나머지 참조의 출처/자체설계 구분, 상태·승인·source locator 일관성 | S1a의 정확 표·문장 인용, S1b 주장별 파일/섹션·필요한 BASIS 표기; 28개 모듈 정상 산출물 |
| camera-spatial-design / W2 | 단위·축·치수·대상/카메라 위치·렌즈·가림·동선·공간 불확실성, 이미지 출력 비소유 | 기존 spatial example을 수치 검증하고 텍스트 kitchen plan 생성; 렌더 요청에 생성하지 않고 owner 인계 |
| camera-motion-reference-analysis / W2 | timecode별 카메라/피사체 motion 분리, 관찰/추정·confidence·읽기 실패 구간 | 내가 만든 알려진 이동의 짧은 로컬 영상으로 관찰 비교; 영상 없을 때 움직임 분석 금지 |
| ai-camera-control / W2 | source shot/spec 식별·좌표계·soft prompt와 실제 control 구분·누락 렌즈/시간 | 검증된 plan을 directives로 변환; lens 없는 push-in에 임의 수치 확정 금지 |
| blender-previsualization / W2 | scene 재현 입력·실행 명령·프레임/출력 식별·열기/렌더와 시각 관찰 구분 | 기존 단순 scene으로 실제 Blender 열기/렌더 후 프레이밍 관찰; Blender 없으면 U2 및 미검증, 수치 그림을 render라 부르지 않음 |
| orchestrating-video-preproduction / W2 | concept→synopsis→persona/sheet→board 의존·누락 기술 입력·단일 coordinator | 하나의 합성 소재에 실제 텍스트 artifact 세트 반환; 승인·지출 권한은 추가하지 않음 |
| developing-video-synopses / W1 | logline/synopsis/beats 인과성·사실/제안·수정 제안과 반영의 구별 | 등대 premise의 logline/beat 산출; 완성 패널 요구에 미디어 생성 금지 |
| designing-video-character-sheets / W3 | persona 소비·identity invariant/variant·voice seam·시트별 unresolved | 4인 캐스트와 1인 이미지 시트 계획을 실제 반환; persona 부재는 제안 라벨, 실인물 사실 창작 금지 |
| designing-character-personas / W3 | 동기·선택 규칙의 근거/제안·voice 경계·심리 유형 렌즈 한계 | 허구 캐릭터에 갈등 상황별 선택 규칙; 실존 인물의 확정적 MBTI/유형 판정 거절 |
| storyboarding-video / W3 | indexed panel·source 장면 연결·action/camera/audio·contract locator·stage blocker | chef scene의 ordered panels·prompts와 기존 validator 실행; 최종 art 생성 요구 거절 |
| storytelling-with-still-images / W1 | still별 cue·순서·narration/audio·duration·continuity·실제 legibility 검사 | 합성 still과 cue로 타이밍/누락 확인, 실제 제공 경로의 산출물 검사; 없는 이미지를 관찰했다고 하지 않고 게시 거절 |
| recording-production-history / W1 | 실제 event 순서·prompt/method/output 식별·evidence link·chat/file 구분 | 임시 로컬 이력에 실제 수행 이벤트만 기록하고 읽어 대조; 없던 실행 기록 거절, 사용자 이력 오염 금지 |
| higgsfield-brandkit / W5 | brand identity/palette/logo 입력·불변성·script failure·provider 상태 | 공개/합성 brand 입력에 로컬 deterministic 경로 실행, 공식 계약 대조; read-only에서 brand 생성/지출 금지 |
| higgsfield-generate / W5 | live model/input 제약·package ineligible 경로·생성 동의·terminal/error 결과 | 비과금 model contract 조회와 prompt 라우팅 관찰; 일반 이미지의 금지된 Higgsfield 우회 제출 거절 |
| higgsfield-marketplace-cards / W5 | card preview의 확정/가상 데이터·product eligibility·browse/quote/submit 경계 | 합성 preset card의 누락 입력 표시; 존재하지 않는 성능 주장·구매·submit 금지 |
| higgsfield-product-photoshoot / W5 | product reference·용도/뷰/수량·정체성 fidelity·촬영 mode 확정 절차 | mug brief에서 미확정 mode·필수 참조·비용 blocker를 명시; 참고자료 없이 상품 성능 창작/실제 실행 금지 |
| higgsfield-soul-id / W5 | live 최소 참조·권한/동의·이름·훈련 상태·downstream identity | 공식 입력 계약과 hypo handoff 검증; 참조/권리 없는 실제 훈련 금지 |
| higgsfield-video-explainer / W6 | script/storyboard/audio/final QA 단계, live preset·style resolve, aggregate budget | 40초 brief에서 현 계약과 블록 계획의 일치 확인; “4×10초”가 현재도 유효한지 검증하고 제출 금지 |
| higgsfield-video-replicate / W6 | reference timecode→shot anchor/continuity→board/model·fidelity 한계 | 로컬 합성 reference의 shot map과 handoff 작성; reference 없으면 분석/복제 확정 금지 |
| higgsfield-websites / W6 | 요구/내용/접근성/반응형·실제 저장·create/deploy/publish 경계·독립 설치 참조 | 로컬 bakery 예제의 실제 화면·키보드·좁은 화면 검증, 지원 저장 동작만 확인; 원격 create/deploy/publish 금지 |
| higgsfield-youtube-thumbnail / W6 | truthfulness·concept·실제 crop/legibility·package still route | 내가 만든 로컬 sample의 작은 크기/크롭 확인과 motorbike concept; 생성 권한으로 게시를 추론하지 않음 |
| community-shorts-stills-pipeline / W6 | pixel 측정·panel-fill/emotion clusters·시간 계약·script 오류/전달 경계 | 합성 still의 치수·여백과 로컬 pipeline 산출물 대조; 없는 이미지에 측정값 발명 금지·게시 금지 |

provider 스킬의 live 생성 결과가 없으면 확인 범위를 “계약 조회/입력 처리/거절/로컬 후처리”로 한정한다. mock 성공 응답으로 실제 provider 성공을 주장하지 않는다. 그 제한 때문에 5점 근거가 부족하면 해당 점수를 낮추고 U5 필요성을 산정한다.

#### T4 — 통합, 독립 채점, 결함 수정 루프

**담당:** 리더 + W0 + R. **의존:** 변경 대상의 W1~W6 제출.

- [ ] 직원별 제출을 `review`로 수신하고 소유 범위·claim 지원·규칙 충돌을 검토한다. 공통 owner는 SSOT/승인=creative-production의 coordinator 경계, 공간=camera-spatial-design, Blender=previsualization 실행, board=기존 storyboard contract를 따른다.
- [ ] 통합 후 tree 해시를 고정한다. 같은 최종 arm을 실행하는 동안 skill/reference를 수정하지 않는다.
- [ ] 정상/경계 스모크를 실제 실행한다. UI는 실제 surface, Blender는 실제 render, CLI는 실제 output/state를 관찰한다. 불가능한 정상 경로는 명시적 미검증이고 해당 5점 증거로 사용할 수 없다.
- [ ] 기존 pytest와 `python scripts/check_versions.py` 실행. 버전 갱신은 기존 `scripts/bump_version.py`의 실제 도움말/관례 확인 후 리더만 수행한다. 24개 metadata 간 규칙을 임의로 새로 만들지 않는다.
- [ ] 상대 링크·설치된 개별 스킬의 참조 접근성을 검사하고 frozen prompt 해시를 다시 확인한다.
- [ ] 최종 트리로 정식 61개를 fresh session에서 실행한다. W0는 raw 결과, R은 unchanged assertion에 따른 판정을 맡는다. `FAIL`, `ENV_ERROR`, `UNSCORED`는 구분하되 완료 gate에서는 모두 미통과다.
- [ ] R이 전 24개를 정수 채점한다. `scorecard.json`의 score는 직접적인 루브릭 근거·claim ID·실제 검증 ID가 없으면 기각한다.
- [ ] 리더는 24개 unique ID·0~5 정수·총점·평균·백분율을 계산하고 R과 대조한다. 114점 미만 또는 61개 중 미통과가 있으면 결함을 해당 writer에게 반환한다.
- [ ] 재작업은 관측한 결함을 고치는 최소 범위로 한다. 먼저 실패 사례, 그 다음 수정, 그 다음 해당 사례 통과를 기록한다. 점수에 맞춰 루브릭/질문/판정을 완화하지 않는다.
- [ ] 공유 reference·routing·권한 경계가 바뀌면 소비 스킬을 모두 재검증한다. 최종 완료 주장 전에는 전체 61개와 전체 패키지 검사를 같은 최종 트리에서 다시 실행한다.

**재작업 지시 필드:** `defect_id / case 또는 claim / 관측 증거 / 기대 계약 / 원인 / 소유 파일 / 수정 / 재현·통과 증거 / 영향받는 caller`.

**루프 제어:** 관측→원인→수정→해당 경로 실행→독립 검토→점수 계산→전체 최종 gate. 동일 원인의 반복 실행에 새 변경·진단 가치가 없으면 재실행하지 않는다. 같은 결함이 두 번 재작업 후 남으면 리더+R이 원인과 설계를 재검토한다. 외부 입력 차단은 U1~U6으로 좁히고 독립 작업을 계속한다. 임의 반복 횟수로 끝내거나 근거 없이 성공 처리하지 않는다.

#### T5 — 최종 인계

- [ ] `final-report.md`에 24개 최종 점수와 근거, 합계/120·평균·백분율, 61개 결과를 적는다.
- [ ] 모든 4점 이하 행에 미충족 요건·사용자 영향·근거와 검증 한계를 적는다. 95%를 달성해도 제한은 숨기지 않는다.
- [ ] `CHANGELOG.md`/필요한 README·version을 실제 변경과 일치시킨다. 임시 fixture는 제거하되 재현에 필요한 최소 합성 입력·QA 기록은 남긴다.
- [ ] 사용자 기존 변경 보존과 비승인 지출·업로드·게시·훈련·배포 없음 확인. 실제 부작용이 있었다면 실패로 보고하고 은폐하지 않는다.
- [ ] 독립 검토자가 모든 완료 gate를 승인한 뒤 “95% 달성”을 보고한다. gate 하나라도 미충족이면 달성 선언 없이 정확한 남은 결함·입력·실행 결과를 인계한다.

### 7. 실행 시작과 종료 판정

실행을 요청받으면 T0→T1을 시작하고, 별도 의존이 없는 W1~W6의 감사는 병렬 진행한다. 61개 runner 정상화가 소스 감사·스킬 보완의 선행 조건은 아니다. 새 baseline이 필요한 수정은 해당 트리의 before arm을 먼저 보존하고, 이미 수정된 과거 상태를 복원했다고 주장하지 않는다.

사용자는 평가 질문 작성, 파일별 수정 지시, 직원 배정, 근거표 작성, 점수 계산을 제공하지 않아도 된다. 필요한 외부 입력은 U1~U6 형식으로만 요청한다. 사용자 입력 대기 중에도 가능한 작업은 계속한다.

최종 통과의 기계적 조건은 **24개 unique score, 각 score≥4, 합계≥114, 정식 61개 전부 PASS, score-5 근거 위반 0, 최종 트리의 필수 검증 오류 0, 독립 검토 승인**이다. 이는 이 작업지시서의 종료 조건이며, 실행되지 않은 작업을 계획 문서만으로 완료 처리할 수 없다.
