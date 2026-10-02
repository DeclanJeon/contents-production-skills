# Video-production skill routing

This guide integrates the three skills in this repository with an agent's existing specialist skills. It is a routing reference, not another skill or production-state machine. Keep the agent's existing `creative-production` skill as the single cross-domain coordinator. The named external skills below are optional local dependencies; this repository does not copy or install their contents.

## Classify intent first

Select the narrowest owner that completes the request. Content format, audience, source material, and delivery goal determine the craft path; the chosen model does not.

| User intent | Primary route | Add only when needed |
|---|---|---|
| Complete multi-stage video production, hybrid campaign, or work spanning writing, generation, 3D, editing, and delivery | Existing `creative-production` coordinator | `video-production-assets` for the requested preproduction package; `camera-spatial-design` for quantified camera/space design; `blender-previsualization` for a Blender proxy or previs artifact. |
| One explicit production asset, such as a brief, claim ledger, lighting plan, or shot list | `video-production-assets`, loading only the relevant module | `camera-spatial-design` for actual spatial/camera calculations; `blender-previsualization` only when an executable Blender previs is requested. |
| Factual or educational video | Claim/evidence and delivery modules in `video-production-assets` when those assets are requested | `content-production-marketing` only for audience, channel, campaign, or source-derived social strategy. Do not invent a protagonist, conflict, dramatic reenactment, product pitch, or unsupported claim. |
| Original narrative, screenplay, character, or scene work | Existing screenplay/story specialists (`synopsis-craft`, `script-craft`, `sw-*`, `char-design`) for the exact requested stage | `video-production-assets` only for requested video-production artifacts. `story-pipeline` only when the user explicitly requests its story-commerce workflow. |
| Storyboard within the existing story-commerce pipeline | `storyboard-craft` only in that pipeline and within its defined schema | For a general storyboard or shot list, use `video-production-assets` or `video-shotlist`; do not impose the story-commerce scene count, runtime, or character-sheet contract. |
| Campaign, paid ad, product promo, UGC, or conversion-led social video | `content-production-marketing` when campaign strategy, claim research, or performance-specific content is requested | `video-production-assets` for explicit production assets; `creative-production` for the multi-stage render/edit route; `fal-video-production` only when Fal is the chosen execution provider. An ad may use hook → demonstration/proof → payoff → CTA when the brief supports it; none of those beats, product wording, or a CTA is universal. |
| Source-derived YouTube/interview/podcast shortform | `youtube-content` for YouTube transcript-derived content; `content-production-marketing` for campaign or performance requirements | `video-production-assets` for a requested source/claim/shot handoff; `video-pipeline` or `fal-video-production` only for the selected executor. Preserve source facts and inspect the actual source media when required. |
| Abstract, music-led, or visual-concept clip | `video-prompt` or `video-shotlist` for a prompt/shotlist request | `creative-production` for multi-stage generation, controlled 3D, assembly, or delivery; use the relevant media executor only after confirming live capabilities. Do not add a story or ad structure without a brief reason. |
| Single prompt, model comparison, or prompt rewrite | `video-prompt`; `video-model-router` only if model choice is unresolved | Query a current model catalog, exact input schema, limits, and pricing. Do not choose from a remembered/static model table. A prompt or model recommendation is not a generation request. |
| Edit or critique of existing footage | `video-critique` or the requested editing workflow | `video-pipeline` or the selected provider's edit executor only when editing is requested. Keep one-asset edits narrow; do not create a new project manifest unless the work becomes multi-stage. |
| Controlled camera-space specification or proxy scene | `camera-spatial-design` for camera and blocking mathematics; `blender-previsualization` for implementation and rendered geometric checks | Preserve shot IDs and spatial-contract versions across the handoff. A projection or proxy render is not a finished video or an aesthetic guarantee. |

## Execution and approval gates

- **Preproduction versus execution:** `video-production-assets` prepares assets and validates structured plans; it does not render or publish footage. Route a real render, edit, or upload request to an available executor and verify that executor before relying on it.
- **Multi-stage state:** Use `project.json` for a multi-stage production contract, with stable asset IDs, claims/provenance, versions, approvals, and output status. Do not create a manifest/database for a single prompt or edit.
- **Dynamic capability:** Before selecting or calling a provider, inspect the live catalog and the exact schema for the selected endpoint and input mode. Verify duration, aspect, resolution, reference/audio/edit support, destination constraints, rights/terms, and current pricing from current authoritative sources. Unknown support means stop before submission; do not substitute a guessed model.
- **Spend:** Show the live price and bounded scope, then obtain explicit approval before any paid submission. Creative approval, batch mode, or “handle it” alone is not spend approval. Do not expand retries beyond an approved scope.
- **Delivery:** A storyboard, prompt, API success, or predicted result is not a generated-video deliverable. Confirm the actual output exists, inspect it with available technical and visual checks, and record unverified checks honestly.
- **Publishing:** Do not post or publish an output unless the user separately requests publication and the destination's requirements are verified.
- **Single-owner handoffs:** The coordinator owns cross-domain lane selection and shared campaign manifests. A specialist owns only its named subtask; do not run a second coordinator, duplicate the same paid shot through two executors, or load unrelated specialist skills in parallel by default.

## Existing specialist IDs

These names describe optional skills that may be present in the agent's local skill root; none of their skill bodies are included here:

- Creative/story stages: `synopsis-craft`, `script-craft`, `sw-premise-theme`, `sw-story-structure`, `sw-character-conflict`, `sw-dialogue`, `sw-scene-craft`, `sw-format-adaptation`, `char-design`.
- Focused content/story-commerce: `story-pipeline`, `storyboard-craft`, `content-production-marketing`, `youtube-content`.
- Prompt/model/edit/execution: `video-prompt`, `video-shotlist`, `video-model-router`, `video-critique`, `video-pipeline`, `fal-video-production`.
- Other rendering surfaces, when directly relevant: `comfyui`, `remotion-create`, and `remotion-render`.

If a named skill is absent, continue only with a supported route and state the limitation; do not fabricate its behavior.

## Routing smoke examples

Use these as route checks when integrating the guide into a local skill set; none of the examples authorizes generation, spend, or publication by itself.

| Request | Expected route | Boundary to preserve |
|---|---|---|
| “Prepare a source-backed 15-second factual explainer about urban heat islands; no characters, ad, or render.” | `video-production-assets` for the requested evidence/shot assets; `creative-production` only if coordinating additional production stages. | No fictional conflict or commercial beat; claims need real sources. |
| “Write one 8-second prompt for a macro flower shot using my selected model; return text only.” | `video-prompt`; use `video-model-router` only if the named model's live schema needs verification. | No full preproduction package, job submission, or spend. |
| “Give me a shot list for a general educational clip.” | `video-production-assets`' relevant shot module or `video-shotlist`. | Do not activate the story-commerce storyboard schema; a shot list is not a rendered clip. |
| “Use the story-commerce format to write a product-conversion story.” | `story-pipeline`, plus only the exact screenplay/character/storyboard stage requested. | Product-conversion constraints apply because the user named that format; do not generalize them. |
| “Turn this YouTube interview into Shorts and preserve the interview's claims.” | `youtube-content`; add `content-production-marketing` only if audience/channel/performance strategy is part of the brief. | Keep source fidelity; use a render executor only if rendering is requested. |
| “Render the approved shots through Fal; I approved the live quote for these exact shots and settings.” | `fal-video-production`, after rechecking current endpoint schema and actual price for that scope. | Preserve the approved shots; no endpoint changes, extra retries, or publication beyond the approved request. |
| “Post the finished video to my selected channel.” | The named publishing integration only after its destination/account requirements are checked. | Publication is explicit here; it is still distinct from generation and must not be inferred from a completed render. |
