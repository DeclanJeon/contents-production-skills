---
name: storyboarding-video
version: 2.30
description: Use to turn a synopsis, scene, visual sequence, or story beat into ordered storyboard panels, a storyboard sheet, or per-panel image prompts.
---

# Storyboarding Video

Return Korean text boards/prompts, never claimed images. Preserve supplied/approved story, exact dialogue/panel count, language and exclusions.

## Read the current stage, not every stage
| Request/stage | Required owners |
|---|---|
| Ordinary storyboard/콘티, detailed production board, supplied-board QA | [complete core](../video-production-assets/references/storyboard-contract.md) **and** [direction](../video-production-assets/references/storyboard-direction.md) |
| Explicit standalone rough narrative beats/thumbnails, panel exercise or prompt-only scope without a production board | [narrative-panels](references/narrative-panels.md) instead; never silently narrow an ordinary board |
| Actual image generation/sheets/extraction/clean-pixel QA | Full-board owners + [media](../video-production-assets/references/storyboard-media.md); full image package also [package](../video-production-assets/references/contract-package.md) |
| Requested PDF/file-board delivery/conversion | [delivery](../video-production-assets/references/storyboard-delivery.md) at that stage |
| project.json detailed board/rhythm authoring/update or structure error | [schema](../video-production-assets/references/storyboard-schema.md) at that stage |

Text-only still returns **all six sections and every mandatory technical slot**. It forbids new media, not explicit MD/PDF saving. No-save/read-only/chat-only independently prohibit writes; absent a file request, answer in chat. Unperformed image/clean/Blender/playback checks remain planned/unverified/blocking.

Complete boards integrate scene-camera intent, every per-shot camera/spatial/VFX/speech/lipsync/audio slot, full beat→scene→shot→panel coverage, and panel-level visible characters/cue/speech/state links **before the final board**. Direction owns speaker/listener reaction choices, neighboring-scene comparison, static/move reasons, emotional/rhythm readability, contact/ownership states, optional kinetic still recipes and readability-first independent pagination. Scene, shot, panel and sheet are different decisions; the four-panel default/eight-panel support ceiling never changes the canonical story count.

`creative-production` is the sole coordinator/writer. A standalone call confirms scope/route once and returns only the requested board. Delegated work inherits the spine, IDs/versions/approvals without a callback, second intake or approval ledger. Delegated packet intake/return reads [minimal handoff/single writer](../video-production-assets/references/contract-core.md#worker-handoff-and-single-writer). Explicit film-lifecycle work adds phase placement only, not unrelated production/distribution.

When Three.js previs is requested and authorized, use [R30 proxy frames](../open-3d-production/references/storyboard-previs.md) for the visual board before final stills. Carry the same shot/panel IDs; proxy renders never close the contact gate.

## Missing specialist inputs
Return one indexed missing-input packet to the coordinator for blocked camera/spatial, VFX, voice/lipsync or audio slots; do not reroute or reopen intake. Resume assembly from the returned owner packets. Legitimate N/A has reasons, deferred execution slots remain stage-labeled, and unresolved requirements stay blocking.

For required contact without articulated body/contact-surface evidence, use the exact [indexed missing-evidence packet](../video-production-assets/references/storyboard-direction.md#카메라공간blender-분기) and hold dependent still generation. Overlap/visibility/static BBox/raycast is not anatomical feasibility. A camera field, scene ID, move or numeric proposal alone does not trigger Blender; actual requested/necessary scene-specific 3D verification does, and unperformed verification remains UNVERIFIED.

## Files, images and return
Full image packages require synopsis/persona/SSOT MD + actual seven-view Sheet A before panels; ordered registered/hashed sheets, mandatory `split_storyboard.py --sheet` scene panels/overviews and every extracted image reopened under media/package. Prompts/portraits/copied panels never substitute.

File-image boards default to PDF + original PNG sheets/clean cuts/split manifest; user format wins. Read delivery at that stage. Text MD/PDF generates no pictures. Missing tools/inspection block corresponding claims. Authorized writes/render/extract use `recording-production-history`; chat-only never initializes history.

Return the usable board, stable content beat/scene/shot/panel IDs, assigned artifact/output version (only when allocated), consumed artifact dependency_versions proposal, assumptions, actual checks and indexed unresolved inputs. Standalone text allocates no project/artifact ID. Registered files and provider locators are distinct.

Model-specific regrouping/prompts inherit `creative-production` generation planning and [timeline→actual request](../creative-production/references/storyboard-timing-to-prompt.md): preserve cut/reaction/state order and exact speech when duration grouping changes. Image review, content acceptance and execution approval remain separate.

## Acceptance
Apply core + direction's indexed KEEP/FIX/unverified corrections, scene intent/neighbor/reuse checks, full coverage, and optional/strict staging/rhythm distinctions. Purposeful static or repeated framing may pass; do not add movement/cuts mechanically. A declared even cadence with reason is valid. Design review, actual image readability and timed playback have distinct evidence scopes.

Full production text is complete only with all six return sections and mandatory technical slots filled or reasoned N/A. An explicitly requested concept pitch may defer execution-only slots as `deferred (승인 후)` and is never a completed shooting board. Missing required checks remain unverified/blocking. Image-backed completion additionally needs every required real artifact, strict validation and actual clean-pixel QA; none grants user acceptance or video spend. Narrow boards keep exact count and visible before/action/after changes; impossible count/story coverage returns an indexed conflict rather than omitted events.

For consequential composition/performance, apply [visual scene communication](../video-production-assets/references/visual-scene-communication.md) within this owner: no twelve-axis form or forced silent-story route. Craft is neither factual evidence nor guaranteed audience response.
