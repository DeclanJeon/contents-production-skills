# Matt Pocock Writing Craft Integration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 기존 콘텐츠 제작 계약을 보존하며 평가 준비, 관찰된 집필 결함의 최소 보강, 패키지 회귀 검증을 순차적으로 수행한다.

**Architecture:** 기존 읽기 전용 Pi 평가 실행기는 유지하고, 고정 사례·반복 실행·다회차·파일 경합 검증을 분리한다. 집필 원리는 실제 baseline 실패가 확인된 경우에만 `video-production-assets`의 공용 참조와 기존 오너 포인터에 통합한다. 평가 도구 완료와 콘텐츠 통합 완료, 모델 평가 완료와 독립 리뷰 완료를 각각 별도 상태로 보고한다.

**Tech Stack:** 기존 Python/pytest, 이미 설치된 Pi CLI의 JSON/RPC, T09에 필요한 Pi SDK·Node.js와 Linux 격리 기능. 새 패키지는 자동 설치하지 않는다.

**Spec:** [QA 보완 설계 v0.2](../specs/2026-11-11-matt-pocock-writing-craft-integration-design.md)

## Global Constraints

- 원본 저장소는 `/home/declan/Documents/Projects/Products/04_Skills/Skills-and-Automation/contents-production-skills`이며 현재 미커밋 변경이 많다. HEAD만으로 baseline을 만들거나 사용자의 변경을 되돌리지 않는다.
- 신규 `SKILL.md`, 총괄, production JSON 필드/상태/CSV 열을 만들지 않는다. 기존 beat/artifact ID·버전·단일 기록자와 사용자 수정·잠금값을 보존한다.
- 글쓰기 원본은 `4ae2317ddb22b046e26455e4f9c9b3aaaf62212d`로 고정한다. 외부 matt 스킬이나 repo `docs/`를 설치본의 필수 런타임 의존성으로 만들지 않는다.
- 단일 응답은 read-only, 다회차는 같은 실제 대화의 연속, T09만 격리 fixture의 쓰기를 허용한다. capability 미확보는 `INCONCLUSIVE`이며 자체 독해로 대체하지 않는다.
- 각 입력/조건 5회, 총 14개 입력·140회 사례·170회 사용자 메시지 응답 단계. 도구 처리로 provider 호출이 더 늘 수 있다. 모델/provider/비용·재시도 상한은 실제 호출 전 별도 확정한다.
- `completed`는 실행 완료이지 PASS가 아니다. 평가표·기대 답은 모델 입력과 분리한다. 실제 평가 실패 전에는 스킬 지침을 작성하지 않는다.
- 최종 통과는 각 사례 5/5 PASS, 차단 위반 0, INCONCLUSIVE/SKIPPED 0이다. 구조 검사와 독립 리뷰·실제 관객 이해·음성/영상 QA를 혼동하지 않는다.
- 설치본 동기화·미디어 생성·게시·패키지 설치·Git 커밋/푸시는 이번 실행에 자동 포함하지 않는다.

## Review Focus

1. 기존 G/F suite가 T 사례 추가 후에도 동일 명령·권한·증거 형식을 유지하는가? → Task 1의 legacy fixture 검사.
2. 다회차가 실제로 대화를 보존하며 accepted/agent_end를 최종 완료로 오판하지 않는가? → Task 2의 RPC 가짜 프로세스 검사.
3. T09에서 사용자 수정 삽입이 실제 원고 읽기 뒤에 일어나며 symlink/상위 경로로 쓰기가 탈출하지 않는가? → Task 3의 경로·이벤트 검사.
4. 이미 dirty인 현재 소스와 도구/기대 답 유출 때문에 대조 실험이 오염되지 않는가? → Task 4의 스냅샷·읽기 추적 검사.
5. 공용 참조가 전문가/미스터리/국소 수정/One pass에 불필요한 설명·질문·파일을 추가하지 않는가? → Task 5–6의 T03/T04/T05/T06/T10/T11/T12/T13 및 설치본 검사.

---

## Execution Gates and Workspace

**현재 상태:** 구현 요청을 받았으며 계획 검토·실행 방식 선택을 기다린다. 설계문서의 ‘미구현’은 아직 사실이다. 계획 승인 후 해당 문서의 수락 근거만 갱신하고 구현 완료로 바꾸지 않는다.

- **G0 — 실행 방식·격리 동의:** 현재 세션에서 직접 구현하는 Native 방식을 권장한다. 표준 subagent/독립 리뷰 도구는 현재 제공되지 않는다. 독립 최종 리뷰를 생략한 전체 완료 판정은 하지 않으며, 그 기능을 확보하거나 검토 방식 변경에 대한 사용자 동의를 받는다.
- **G1 — 오프라인 준비:** Task 1–3과 mock 기반 검증은 모델 호출 없이 진행할 수 있다. worktree 생성은 사용자 동의 후 한다. 독립 리뷰 capability의 부재는 기록하고 도구 구현과 혼동하지 않는다.
- **G2 — 실제 baseline:** provider/model, 호출·토큰/비용 상한, timeout·재시도 상한, T09 격리 capability를 명시적으로 확정해야 Task 4의 모델 호출을 시작한다. 기존 계정 인증을 사용하고 자격 증명을 추출/복사하지 않는다.
- **G3 — 스킬 편집:** 실제 baseline FAIL과 해당 원문 증거가 있어야 Task 5를 시작한다. 전부 통과한 원리에는 불필요한 지침을 추가하지 않는다.
- **G4 — 수락:** Task 6의 평가·회귀·독립 리뷰 근거가 모두 있어야 전체 완료다. 미확보 단계는 BLOCKED/INCONCLUSIVE로 보고한다.

동의받은 격리 작업공간은 `.worktrees/matt-writing-craft`를 우선한다. `.gitignore` 변경이나 commit이 필요하면 자동 실행하지 않고 확인한다. worktree 생성 직후 기존 작업 트리의 tracked 변경·필요한 untracked 파일을 복사해 출발점을 맞추되 `.git`, 다른 worktree, 캐시, derived support는 복사하지 않는다. symlink로 원본을 가리키는 쓰기 공유를 만들지 않는다. 복사 전후 파일 해시·포함/제외 목록을 저장하고 baseline에 포함된 기존 변경과 이번 작업 delta를 구분한다. 기존 변경을 commit/stash/reset하지 않는다.

실행 시작 시 `python scripts/check_versions.py`와 `python -X utf8 -m pytest -q`를 격리 작업공간에서 수행한다. 기존 실패가 있으면 결과를 보고하고 계속할지 확인한다. pytest/Pillow/pydantic은 현재 발견됐지만 설치됐다는 사실만으로 테스트 통과를 가정하지 않는다.

## File Responsibilities

| 파일 | 책임 |
|---|---|
| `qa/matt-writing-inputs.json` (신규) | 설계 §10.1.2의 고정 사용자 메시지·오너·실행 유형만 보관; 기대 답 없음 |
| `qa/matt-writing-rubric.json` (신규) | 모델에 노출하지 않는 사례별 보존/수정/판정 기준 |
| `scripts/writing_eval_cases.py` (신규) | suite 검증·오너 선택·공통 접두사·스냅샷/입력 해시 |
| `scripts/run_guide_behavior.py` (수정) | 단일 응답의 T 사례 지원; G/F 동작 보존 |
| `scripts/writing_eval_rpc.py` (신규) | T11/T12의 지속 RPC 대화·회차별 증거·종료 처리 |
| `scripts/writing_eval_fixture.mjs` (신규) | T09의 제한된 SDK 도구와 읽기→사용자 수정→편집 이벤트 |
| `scripts/run_writing_evaluation.py` (신규) | 유형별 어댑터 배정·두 조건/반복·dry-run manifest·결과 집계 |
| `scripts/test_writing_eval_cases.py`, `scripts/test_writing_eval_rpc.py`, `scripts/test_writing_evaluation.py` (신규) | Python 오프라인 회귀·가짜 모델 프로세스 테스트 |
| `scripts/test_writing_eval_fixture.mjs` (신규) | Node 내장 test 기반 파일 경계·가짜 SDK 테스트 |
| `video-production-assets/references/writing-craft.md` (조건부 신규) | baseline에서 확인한 원리만 모은 제작용 참조 |
| `video-production-assets/references/upstream/matt-pocock-writing-provenance.md`, `matt-pocock-LICENSE.txt` (조건부 신규) | 원리별 원문/해시/각색 경계·MIT 고지 |
| 설계 §5.2의 기존 오너 파일, README/USAGE_GUIDE/CHANGELOG | 조건부 연결·실제 검증 결과만 기록 |
| `scripts/test_writing_craft_integration.py` (조건부 신규) | 설치본 포함/링크/manifest 불변·upstream 고지 검사 |

평가 파일은 개발/QA 도구이며 runtime skill manifest에 추가하지 않는다. 임시 모델 실행 루트는 설치된 skill payload만 포함하고 `qa/`, scripts의 테스트·루브릭은 포함하지 않는다.

### Task 1: 고정 사례와 단일 응답 실행 경로

**Files:** Create `qa/matt-writing-inputs.json`, `qa/matt-writing-rubric.json`, `scripts/writing_eval_cases.py`, `scripts/test_writing_eval_cases.py`; Modify `scripts/run_guide_behavior.py`, `scripts/test_run_guide_behavior.py`.

**Interfaces:** `load_cases(path: Path) -> list[dict]`, `resolve_owner(case_id: str) -> str`, `single_turn_case(case: dict) -> dict` in `writing_eval_cases.py`. `load_cases` validates id, kind (`single`/`conversation`/`fixture`), owner and nonempty `turns: list[str]`; rubric stays in a separate file. Existing `execute(case, root, out, profile, before)` keeps its signature.

- [ ] Write `test_case_roster_and_messages_match_spec`: exactly T01–T09/T10a/T10b/T11/T12/T13, T11 has 2 turns, T12 has 3, all other cases 1; compare full user messages and prefix against the approved design, not merely keywords. Test duplicate/unknown ID, empty turns and rubric keys rejected in inputs.
- [ ] Write `test_legacy_routes_and_permissions_unchanged` using existing F04 fake `Popen`; assert argv/system/prompt/UNREVIEWED unchanged. Add `test_conversation_not_sent_to_single_execute` and T05 exact prompt/hash assertions.
- [ ] Run `python -m pytest -q scripts/test_writing_eval_cases.py scripts/test_run_guide_behavior.py`; observe missing-module/routing failures before implementing.
- [ ] Implement validation and T owner routing; `single_turn_case` rejects multi-turn/fixture types instead of flattening them. Update only owner resolution at existing execute/main call sites; keep G/F lookup compatible. Map exact T10a/T10b IDs without stripping their suffix.
- [ ] Re-run both test files; record real exit/status. Commit only if separately requested, with just this task's delta.

### Task 2: T11/T12의 지속 RPC 대화

**Files:** Create `scripts/writing_eval_rpc.py`, `scripts/test_writing_eval_rpc.py`.

**Interfaces:** `run_conversation(case: dict, root: Path, out: Path, profile: dict) -> dict`; consumes validated cases and existing `parse_events`. Profile requires executable/provider/model/thinking/timeout; no implicit model. Produces per-turn raw stdin/stdout/stderr and result records with execution status, never automatic PASS.

- [ ] Write `test_same_child_receives_all_turns_in_order`, `test_new_repeat_starts_new_child`, `test_ack_or_agent_end_is_not_settled`, `test_handled_prompt_is_inconclusive`, `test_unicode_separator_is_not_jsonl_boundary`, and `test_timeout_terminates_child`. Use a stdlib fake JSONL child, not a model call.
- [ ] Run `python -m pytest -q scripts/test_writing_eval_rpc.py`; observe missing implementation failures.
- [ ] Implement one `pi --mode rpc --no-session` child per case/repetition, explicit read-only tools/no extensions/MCP/skills/context files, prompt command IDs and LF framing. Subscribe/read before sending; wait for successful final assistant message and `agent_settled` before next user message. Record accepted/queued/handled and fail closed on unsupported lifecycle. Close stdin, wait, then bounded termination on timeout; preserve all outputs.
- [ ] Re-run tests and record evidence. Before real execution, read installed `docs/rpc.md`, `rpc-commands.md`, `json.md`, `cli.md` and verify local CLI options; provider retry policy must respect G2. Do not mark a fake-child test as real model validation.

### Task 3: T09의 격리 fixture·이벤트 계약

**Files:** Create `scripts/writing_eval_fixture.mjs`, `scripts/test_writing_eval_fixture.mjs`; consume no production schema changes.

**Interfaces:** export `resolveFixturePath(root, requested) -> string`, `runFixtureCase(config, sessionFactory) -> Promise<object>`. Config requires snapshotRoot, fixtureRoot, outputRoot, explicit Pi package location/provider/model and deadline; sessionFactory injection permits model-free tests. Only `fixture/draft.md` is writable.

- [ ] Write Node tests for `../`/absolute escape/symlink escape, non-draft writes, initial full-read detection, injection-before-first-edit, required re-read, final exact bytes, aborted run, missing event and untouched adjacent files. Use design §10.1.2's literal initial/injected/final strings.
- [ ] Run `node --test scripts/test_writing_eval_fixture.mjs`; observe missing exports/module failures.
- [ ] Implement fail-closed SDK adapter using `createAgentSession`, `SessionManager.inMemory` and explicit resource/tool configuration. Use read-only package access and custom read/edit/write tools confined by realpath allowlists; no shell/MCP/provider tools. Barrier the first edit until the first complete draft read and evaluator insertion are logged, and require a subsequent re-read. Reject paths outside allowed fixture before opening them. Reuse existing auth transport without outputting secrets.
- [ ] Probe bwrap/user-namespace capability with an offline harmless child and verify a real external sentinel cannot be written; binary presence alone is insufficient. For real model execution, mount source/runtime/home read-only and only fixture/output paths writable. If permissions, compatible SDK, auth transport or deterministic event barrier are unavailable, return INCONCLUSIVE before any model submission. Do not silently fall back to unrestricted tools.
- [ ] Run Node tests with fake sessionFactory; record separately from live sandbox capability. Read installed SDK/tools/extensions declarations and examples fully before selecting exact custom-tool API; unsupported installed API is a blocker, not an invented method.

### Task 4: 재현 가능한 baseline과 판정 증거

**Files:** Create `scripts/run_writing_evaluation.py`, `scripts/test_writing_evaluation.py`; use Task 1–3 adapters. Evidence goes to new `qa/runs/matt-writing/<run-id>/` report paths outside each model-readable snapshot.

**Interfaces:** `build_run_manifest(cases: list[dict], profile: dict) -> dict`, `run_case(case: dict, root: Path, out: Path, profile: dict) -> dict`, `aggregate_results(records: list[dict]) -> dict`. The manifest describes exactly 140 runs and 170 user-response stages across baseline/candidate, input/snapshot/runner hashes, adapter kind and capabilities. `aggregate_results` consumes manual verdict records (`PASS`/`FAIL`/`INCONCLUSIVE`/`SKIPPED`) with evidence pointers; missing verdict/evidence never becomes PASS.

- [ ] Write tests for 14×2×5 run count, 170 response stages, T09 write gate, repeated output collision, missing provider/budget, snapshot mutation, missing read/owner evidence, unchanged baseline PASS not counted as improvement, all-5-PASS and one-blocker failure, timeout retained not resampled. Add dry-run assertions that no subprocess/model is invoked.
- [ ] Run `python -m pytest -q scripts/test_writing_evaluation.py`; observe failures. Implement dry-run first; actual run requires G2 approval. Store source/input/system/runner hashes and attempt artifacts using existing evidence naming conventions. Default concurrency 1; no hidden resampling or automatic retry.
- [ ] Create immutable baseline snapshot from the current dirty runtime payload, not HEAD. Capture existing worktree hashes, CLI version, adapter capability and run-manifest into evidence. Candidate will be derived from that baseline plus only the later approved runtime edits; evaluation scripts/settings stay identical across conditions.
- [ ] Stop at G2 to obtain the exact provider/model and budget limits. Once authorized, run baseline's 70 cases (85 user-response stages plus tool/provider turns) and manually classify every case with input/response/trace locations. T09/T11/T12 missing capability remains INCONCLUSIVE and blocks full-suite completion. No content skill edit occurs before baseline evidence.
- [ ] Save `baseline-review.md` listing observed failures, protected regressions and which proposed rules have no demonstrated need. If baseline reveals no applicable failure, report no-op and do not force Task 5's content changes.

### Task 5: 관찰된 집필 결함만 기존 오너에 통합

**Files:** Conditionally Create the three production reference/provenance/license files in File Responsibilities and `scripts/test_writing_craft_integration.py`. Modify only affected rows/files from design §5.2: `video-production-assets/SKILL.md`, `references/01-brief.md`, `02-story.md`, `03-screenplay.md`, `12-qa.md`, `developing-video-synopses/references/synopsis-craft.md`, `orchestrating-video-preproduction/references/video-direction.md`.

**Interfaces:** `writing-craft.md` anchors `explore`, `grounding`, `shape`, `interaction-and-handoff`; existing owner fields and routing stay authoritative. The provenance file maps each included principle to exact upstream path/hash and deviations; license bytes match the pinned LICENSE. No external matt runtime calls.

- [ ] Read `writing-skills` and `test-driven-development` before editing. Link each selected instruction to a real baseline FAIL; preserve failing response/trace. Write structural tests for installed reference/license/provenance, relative links, unchanged manifest skills/production schemas and no `/home/declan` runtime pointers; run them and observe expected missing-file failures. Structural failures alone do not satisfy behavioral RED.
- [ ] Write only rules supported by baseline failure: explore vs fixed-pile, audience prerequisites vs introduced concepts, block function/transition, source gaps, user edits, interaction modes and versioned handoff. Keep factual evidence separate from conceptual grounding; preserve expert/abstract/mystery/no-CTA exceptions. Detailed guidance lives in the shared reference once.
- [ ] Add one conditional entry-row pointer and affected owner pointers; exact anchor paths must work in copied installed skills. Do not alter `creative-production`, JSON updater, field names or unrelated user edits. Record each affected file in the task delta manifest.
- [ ] Run `python -m pytest -q scripts/test_writing_craft_integration.py scripts/test_video_pack_boundary.py`; then assemble candidate snapshot and run the affected post-change microcases under G2. If variance or new regression appears, minimally revise wording and rerun with preserved attempt history; no claims from cherry-picked outputs.

### Task 6: 전체 사례 재평가·패키지 회귀·인계

**Files:** Modify `README.md`, `USAGE_GUIDE.md`, `CHANGELOG.md` only to describe actual implementation/evidence; Create `qa/matt-writing-integration-review.md`. The manifest skill list is unchanged; no release/version bump is needed for an unreleased implementation. Check current version policy again if release is separately requested.

**Interfaces:** Uses Task 4 manifest/verdict artifacts and Task 5 copied-package outputs. Deliverable reports scope, files, unit/installation/behavioral results, independent reviewer verdict and unresolved capability separately.

- [ ] Run remaining candidate cases so each of all 14 inputs has 5 reviewed results. Confirm model/settings/runner/inputs match baseline and only approved runtime changes differ; any INCONCLUSIVE/SKIPPED or blocker leaves the behavioral gate incomplete.
- [ ] Run `python scripts/check_versions.py`, `python -X utf8 -m pytest -q`, and `node --test scripts/test_writing_eval_fixture.mjs` from the isolated workspace. Preserve commands/full logs/exits and distinguish pre-existing failures from task regressions. Verify temporary install contains reference/provenance/license and needs no external matt skills.
- [ ] Update usage examples for exploration, explanation-order repair, existing-draft editing, One pass and explicit beat-wise collaboration. Record the existing runtime owner and skip conditions. Keep docs honest if only evaluation tooling is finished or behavioral gates are blocked; do not present a draft as released/verified craft.
- [ ] Obtain one independent whole-change review when the capability is available, passing the approved spec, task delta, original dirty baseline, commands/results and behavior evidence. If unavailable, report review BLOCKED and ask for an approved review route; self-review is not independent approval.
- [ ] Return actual workspace paths, task delta, complete/incomplete gates and evidence paths. Do not synchronize global installed skills, publish, push or merge. Commit only if explicitly requested, staging this task's changes without bundling the inherited dirty baseline.

## Plan Self-Review

- [x] Spec §1–5: scope/owner/provenance/conditional file mapping → Task 5–6.
- [x] Spec §6–8: interactions, grounding, source/ID/edits and illustrative example → Task 1 fixtures, Task 2–3 adapters, Task 5 reference.
- [x] Spec §9: exact upstream source hashes and MIT → Task 5 provenance/license test.
- [x] Spec §10–11: runner reuse, fixed inputs, multi-turn/file collision, 140/170 counts, snapshots and review gates → Task 1–4/6.
- [x] Interfaces share validated case dicts/explicit profiles; adapters never manufacture verdicts. Existing `execute` signature is preserved.
- [x] All five Review Focus risks have named tests and an owning task. Structural tests are not substituted for behavior baselines.
- [x] No plan step authorizes paid calls, unsupported tooling, independent-review substitution or overwriting unrelated work by implication.

## Status

The statement that this was plan-only describes the original planning checkpoint. Subsequent user authorization selected isolated inline execution, native Codex/gpt-6-luna and no total monetary ceiling. Tasks 1–4 were implemented; Task 5/6 behavioral acceptance remains incomplete. User subsequently approved the contained document-relative/reference-reading architecture. New adapter epochs v4–v8 retain their errors and unstarted rows; v9 declared high reasoning equally for fresh baseline/candidate controls, same source/input/rubric and one archived adapter. All 140 runs / 170 stages completed with valid evidence and all 10 physical fixture checks. Reviewed result: baseline 55 PASS / 15 FAIL; candidate 69 PASS / 1 FAIL. A missing word in the fixed T05 ending is blocking, so final-aggregate remains FAIL (missing0/invalid0/blocker1). Current source CODE review found no actionable defect; 701 Python tests/518 subtests, Node11, type0/0 do not certify writing. No release/global install/merge/commit occurred at that evaluation checkpoint. A subsequent explicit user request authorizes committing, merging into main and pushing the source, not lifting the behavioral FAIL or making a release. See [current evaluation and retained history](../../../qa/matt-writing-integration-review.md) and this plan's evidence ledger. Do not silently start another wording-only epoch or overwrite old attempts.
