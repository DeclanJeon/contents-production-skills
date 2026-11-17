---
name: orchestrating-video-preproduction
version: 2.27
description: Use for text-only video preproduction that spans multiple artifacts — a complete planning package or one idea carried from concept through synopsis, characters, and storyboard. Delegated planning lane under creative-production; returns text and generic image prompts, never media.
---

# Orchestrating Video Preproduction

This lane moves a single brief through whichever planning stages were requested while holding one premise steady across all of them. Answer in Korean unless told otherwise. Deliverables are structured text plus reusable image prompts; nothing here produces or claims images or video.

`creative-production` alone coordinates content and video projects, and
`creative-production/references/policy.md` is the canon for authority, scope,
read-only probes, single writer, evidence and the execution gate. This skill is
its delegated text-planning lane — on a standalone call, consult
`creative-production` once to confirm scope and route, then perform only the
requested planning. When work arrives already delegated, inherit the
coordinator's brief, IDs, versions, and approvals: no call-backs, no re-routing,
no second interview or approval ledger — with stage packet intake and worker
return per the canonical [worker handoff and single writer](../video-production-assets/references/contract.md#worker-handoff-and-single-writer). Text planning alone never creates a project folder, `project.json`, stills, or a sample video. Anything beyond text — image-backed packages, generation, editing, delivery, publication — goes back to `creative-production` as a plan and handoff; this lane never executes or picks an executor.

Text-only forbids media, files, and spend — not technical planning: a storyboard requested here defaults to the complete production plan under [`../video-production-assets/references/storyboard-contract.md`](../video-production-assets/references/storyboard-contract.md). Rough narrative panels or prompt-only thumbnails apply only on an explicit request for that narrow exercise.

If a text-only/read-only request also says “render the storyboard later,” return the requested text plan, generic prompts and downstream render requirements only. “Later” is a handoff requirement, not authorization to render now (policy §3): do not call an image/video generator, Blender, a provider submit tool, or a file-writing production tool from this lane. This boundary applies even when `creative-production` is not loaded; loading or consulting a coordinator cannot widen the current request's permission.

## Choosing the stages

- **Package request:** follow the coordinator's assigned text stages in order, using the matching text specialists from the [canonical routing table](../creative-production/references/routing.csv). A full text package ends with the assigned text artifacts and, only when dependencies are missing, one indexed missing-input packet; a full image-backed package returns the same bounded handoff so the coordinator can resume downstream specialists/media. If a matching text skill is not loaded, follow its `SKILL.md` in the same-named sibling directory; read only the current-stage guide, never every downstream guide.
- **Single-artifact request:** invoke only the matching specialist and return only that artifact. Never build the full package, never ask permission to skip unrequested stages, never treat an omitted stage as an open question.
- The canonical route owns specialist selection; this lane invokes only matching text specialists within its assignment. A character-sheet assignment retains the required `designing-character-personas` design. Preserve supplied synopsis and character/persona decisions rather than inventing unassigned upstream artifacts.
- For assigned visual directing in dialogue-led or wordless work, use only the current owner's relevant parts of [common visual scene communication](../video-production-assets/references/visual-scene-communication.md). Preserve language/sound roles and approved facts, and return the actual shot/performance/look/edit choices with observable checks in existing fields; this is not a new specialist, research stage or silent-story prerequisite.
- For assigned no-dialogue story work, invoke `silent-visual-storytelling`; for assigned timing/cut/hold or timed-board test planning on an approved story/board, invoke `animatic-direction`. Follow the coordinator's [silent/animatic assignment](../creative-production/references/production-routing.md#silent-and-animatic-assignment) packet and stage precedence; both are not mandatory for ordinary boards/animation. Preserve approved story, IDs, independent audio/text constraints and the existing06/08/09 handoff fields. Return text/proposed timing/unverified playback only: no source reanalysis, second interview, renderer or automatic next stage.
- Applicability is mode-dependent: omit inapplicable characters and fictional plot elements, not explicitly requested planning artifacts. Character-free, factual and abstract briefs retain their requested concept, informational/visual synopsis, beat planning and board without fabricating a cast or conflict.

When a film/short/animation/AI-film request is assigned through the lifecycle route, inherit its current preproduction stage, IDs, versions and approvals. This lane owns only the assigned preproduction text artifacts; shooting, postproduction and distribution remain downstream stages and are not inferred.

## Detailed guides

- **Multi-stage or package request:** read [`references/video-direction.md`](references/video-direction.md) for the interaction modes, direction decision, discovery flow, choice statuses and checkpoints, and [`references/stage-execution.md`](references/stage-execution.md) for the canonical spine fields, per-stage craft requirements, integrity standards, package assembly, and the final consistency pass. These are the two lane guides; a single-artifact call opens neither.

## Missing technical inputs

A production storyboard retains every applicable camera/spatial, VFX, speech/lipsync and audio slot from its contract; a slot alone does not activate every specialist or Blender. When the inherited packet lacks required specialist input, return **one indexed requirement packet** to `creative-production` listing each blocked slot by scene/shot/beat index, the required input and blocker. Continue independent assigned text work. The coordinator selects and assigns each missing-input owner once using the canonical route, integrates its return, and supplies the resolved input for board assembly without repeating intake or routing. This lane never selects a technical executor, calls back to reroute itself, or opens a second interview/ledger. Unresolved requirements remain explicitly blocking; the board never silently shrinks to rough panels.

## Package return

A full text-package assignment returns the applicable assigned sections defined in `references/stage-execution.md` — shared spine, concept/synopsis with stable beat IDs, character sheets, Visual Bible, screenplay when assigned, the storyboard, and the consistency/unresolved/review status — plus the indexed missing-input packet, if any. Do not add unassigned artifacts. Delegated returns additionally carry the assigned artifact/entity IDs and output versions, a dependency/dependency_versions proposal naming each input artifact version used, assumptions, checks performed, and remaining blockers, per the canonical [worker handoff and single writer](../video-production-assets/references/contract.md#worker-handoff-and-single-writer). Standalone chat work allocates no project or artifact IDs.

## Multi-artifact plan response shape

For a **plan-depth** multi-artifact request, preserve all six requested sections and the full storyboard contract, but keep the response compact: target **≤2,000 words** unless the user asks for exhaustive detail. Put shared assumptions, IDs, continuity and status in one spine/table; reuse them by ID instead of repeating them in every artifact. Use one concise row per beat, shot and required panel; populate each mandatory slot once in the shot table and mark unresolved values with indexed blockers. Keep rationale to decision-changing facts, cite sources inline, and omit repeated explanations, duplicate source-basis sections and unrequested prompt variants. The word target never authorizes omitting a requested artifact, panel, or mandatory slot: compress field values, not coverage. Finished drafts or explicitly exhaustive boards follow the requested detail instead of this plan-depth target.

## Acceptance

Done means the requested stages — no more, no fewer — returned as actual artifacts consistent with the spine, every supplied choice and approval reused verbatim, each claim carrying its fact status, the board's technical slots integrated or explicitly carried as the indexed requirement packet, and nothing implying generated media, files, or spend. When the coordinator continues into an image-backed package, this lane's handoff requires (downstream of it): the paginated storyboard sheet set (≤8 panels per sheet, `<stem>_sNN.png` when the board paginates), mandatory `split_storyboard.py --sheet` extraction of clean panels plus per-scene overview images with `split-manifest.json`, visual inspection of the actual extracted pixels, and operation recording via `recording-production-history` (`production_history.py init/record`) per the shared storage contract — all registered back to the coordinator's ledger, never to a parallel ledger.

## Handoff

Beyond the package, the lane hands off the direction decision, interaction mode, choice statuses, stable beat/panel IDs, Visual Bible, and continuity ledger so the receiving stage inherits them as-is rather than re-interviewing. Shot-level production specifications inside the board contract are this lane's own text deliverable; model-specific clip decomposition and execution are handed to `creative-production`, which selects the downstream owner and provider. Planning approval is never spend approval.

### 창작 연출 집중 모드 (Creative Staging Focus vs. Full Audit Mode)

다중 산출물 계획 응답의 `≤2,000 words` 예산 안에서 행정 메타데이터(도서 `SHA-256` 해시 반복, 중복 ID 나열, 빈 형식 표)가 정작 중요한 **장면 연출·인물 표정·동세·컷별 프롬프트**를 한 줄짜리 단답형으로 압축시키지 않도록 응답 밀도를 관리한다:

- **토큰 배분 우선순위**: 전체 응답 분량의 **80% 이상**을 ① 씬별 카메라/리듬 설계, ② 패널별 적용 가능한 **상황 위계(`focal_hierarchy`)·표정/대체 연기(`expression_pose`)·물리/동세 단서(`kinetic_cues`)**, ③ 요청된 **한·영 이중 이미지 프롬프트(`image_prompt`)**에 할애한다. 정본 스토리보드 계약의 적용성을 따른다: 비인간/얼굴 유보/정적·평면 장면에는 목적에 맞는 대체 단서 또는 이유 있는 N/A를 사용하며 인체·3단 깊이·역동성을 일률 강제하지 않는다. 명시적으로 승인된 적용 가능한 strict 제약은 유지한다.
- **기계적 메타데이터 압축**: 공통 가정·출처 지문·버전 핀은 문서 상단 스파인에 1회만 선언하고, 개별 패널 행에서는 생생한 시각·연기·구도 묘사를 절대 축약하지 않는다.
