---
name: creative-production
description: Use for content creation or adaptation, including articles, social posts, campaigns, scripts, storyboards, audio, images, and video planning, generation, editing, QA or delivery; also hybrid 3D/web creative productions. Applies to single artifacts and full productions, not ordinary UI styling or unrelated application development.
metadata:
  version: "1.2.0"
---

# Creative Production

Coordinate the requested content/video deliverable using one brief, relevant specialists, and version-bound approvals. Choose purpose and output before tools. Coordination does not enlarge the request.

## 1. Establish scope and the active brief

Read supplied material and existing project instructions first. Preserve requested language, output, exclusions, fixed facts, continuity anchors, selected tools, and existing approvals. Separate factual evidence, derived calculations, interpretation, and creative proposals. Ask only for a missing consequential choice that tools or sources cannot answer.

Use the host's available dialogue or structured question tool. Existing interview/plan skills may supply this interaction, but no particular framework is required. Reuse an active interview or approval flow rather than starting another. When several creative directions remain open, present distinct options and one recommendation; proceed with a direction only when supplied, accepted, or explicitly delegated. Silence is not approval. A locked brief or single artifact needs no new full-project interview.

## 2. Select the narrowest lane

Read [production-routing.md](references/production-routing.md) for the requested branch and dependency boundary.

- Articles, blog/social drafts and source-based text can be written directly from the brief and evidence. Marketing rules apply only to a marketing request.
- Text video planning uses [orchestrating-video-preproduction](../orchestrating-video-preproduction/SKILL.md) and the applicable synopsis, character or storyboard specialist. Omit characters when the project has none.
- Production assets use [video-production-assets](../video-production-assets/SKILL.md), loading only requested modules. It is not a renderer or publishing tool.
- Numeric camera/blocking uses [camera-spatial-design](../camera-spatial-design/SKILL.md). An actual Blender proxy/previs uses [blender-previsualization](../blender-previsualization/SKILL.md) and its real runtime.
- Story-commerce, screenplay, marketing strategy, platform operations and provider execution use their selected available external specialist. These specialists and runtimes are not bundled by this skill.
- Ordinary UI/brand implementation retains its existing design/development owner. For a hybrid production, coordinate media delivery while that owner supplies the visual/UI contract.

A standalone specialist consults this scope contract once, then performs its requested craft. A delegated specialist continues the assigned stage with the inherited brief and checkpoints; it does not call the coordinator back, reopen answered questions, or create a second approval ledger. Internal text-planning sequencing is not a competing project coordinator.

## 3. Use the existing artifact surface

A single draft, prompt, critique, synopsis, character sheet, or storyboard can be delivered in chat. No project folder, manifest, generated images/video, additional formats, CTA or publication is implied. Requested text-file saving does not change the work into image-backed preproduction.

For multi-stage video under the production-assets contract, use its existing [project contract](../video-production-assets/references/contract.md). Keep `project.json` canonical. Preserve a specialist's required story bible or lane-local manifest as an artifact, linking actual IDs, versions, dependencies and approval evidence rather than rewriting its schema or creating rival global state. An executor needing another input shape uses the [optional adapter](references/shot-manifest.md), not a second project database.

Carry the brief, sources/claim status, requested output and exclusions, stable IDs/versions, continuity, actual artifacts, approval evidence and blockers across stages. Maintain only fields needed by those stages. User data and generated project files remain in the selected project root, not the installed skill package.

## 4. Separate planning, review and execution

For a full topic-to-video or image-backed preproduction package, read [preproduction-review.md](../video-production-assets/references/preproduction-review.md) **before project writes or media calls**. It owns exact project-directory selection, existing-folder/resume rules, applicable artifacts, actual review stills through external `codex-imagen`, registration, inspection and user review. An exact supplied directory is reused; a parent root still requires a selected project subdirectory. Explicit text-only planning stays in the text lane instead.

Keep the video model unresolved through preproduction. Acceptance covers only reviewed artifact versions. A separate request to proceed opens a live-verified, bounded video execution plan; execute only after explicit approval of the plan and applicable spend. Free/local sample video, moving animatic and export also require this gate. Automated validators or judgments do not substitute for user approval.

Before requested external execution, verify the selected provider's current catalog, exact endpoint/input schema, reference/audio/edit support, limits, destination requirements, rights/terms and price. Unknown required support or price stops submission. Paid calls need explicit scope and spend approval; publishing or live platform changes need their separately requested scope. A rewrite-only request never changes a database or deploys a site.

Preserve approved shot/output count, time/storage bounds, concurrency, retry scope and spend cap in the owning plan. Do not infer extra retries or unbounded batches. Changed upstream inputs make affected dependent reviews/execution plans stale; unaffected approvals remain valid.

## 5. Execute only the selected surface

Text planning requires no renderer, GPU, media account or output folder. Check tools/auth only for the branch that needs them. External specialists are optional at installation but can be required for a chosen branch: report the precise missing skill/runtime/auth, complete reachable requested preparation, and stop before that step. Offer a materially different route as a proposal, not as a silent provider substitution or an equivalent completion.

For actual media, use the selected available executor and inspect outputs before scaling. Use deterministic geometry/cameras for exact spatial requirements, deterministic composition for critical text/logos/prices, and actual timeline/encoding tools for assembly. Do not treat a raw generated clip or mesh as production-ready. A representative result must fit the authorized scope; it is not permission to batch.

Check credential presence without exposing values. Keep secrets out of prompts, files, logs and commits. Use isolated requested output locations; inspect generated Blender/runtime scripts and preserve source assets. Parallel workers are optional host capabilities, not a required framework or a reason to run the same paid job twice.

## 6. Verify and deliver

Apply the relevant checks in [creative-qa.md](references/creative-qa.md): actual text/source fidelity for a draft, listening for audio, frames/timing/continuity/encoding for video, scene/render inspection for Blender, and the actual browser surface for web/3D. A schema or source-file pass is not visual verification or legal clearance.

Return the requested artifact itself or its actual file location and exercised checks. Distinguish draft/plan, actual generated output, inspection, user acceptance and publication. Partial generation registers only actual files and names the failed/missing outputs; API success or a predicted result is not complete delivery. State unverified conditions without claiming unavailable tools were used.
