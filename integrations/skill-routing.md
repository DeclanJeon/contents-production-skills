# Video-production skill routing

This guide integrates the three skills in this repository with an agent's existing specialist skills. It is a routing reference, not another skill or production-state machine. Keep the agent's existing `creative-production` skill as the single entry point and cross-domain coordinator. The named external skills below are optional local dependencies; this repository does not copy or install their contents.

## Classify intent first

`creative-production` coordinates every content/video request, including one artifact. Select the narrowest specialist below that completes it; the table names craft lanes, not alternative project coordinators. Content format, source material, and requested delivery determine the route before model choice.

| User intent | Primary route | Add only when needed |
|---|---|---|
| Text/blog/social draft or adaptation without media execution | `creative-production` → applicable writing/source/platform specialist or direct source-grounded drafting | No video package, folder selection, generated imagery, CTA, extra variants, or publication unless requested. |
| Complete multi-stage video production, hybrid campaign, or work spanning writing, generation, 3D, editing, and delivery | Existing `creative-production` coordinator | `video-production-assets` for the requested preproduction package; `camera-spatial-design` for quantified camera/space design; `blender-previsualization` for a Blender proxy or previs artifact. |
| One explicit production asset, such as a brief, claim ledger, lighting plan, or shot list | `video-production-assets`, loading only the relevant module | `camera-spatial-design` for actual spatial/camera calculations; `blender-previsualization` only when an executable Blender previs is requested. |
| Factual or educational video | Claim/evidence and delivery modules in `video-production-assets` when those assets are requested | `content-production-marketing` only for audience, channel, campaign, or source-derived social strategy. Do not invent a protagonist, conflict, dramatic reenactment, product pitch, or unsupported claim. |
| Original narrative, screenplay, character, or scene work | Applicable `sw-*` craft or general video-planning specialists under `creative-production` | `synopsis-craft`, `script-craft`, and `char-design` keep their explicit story-commerce lane contracts. Load `story-pipeline` only when that format is requested. |
| Text-only story planning: concept, synopsis, character sheets, storyboard | `creative-production` → `orchestrating-video-preproduction` and applicable `developing-video-synopses`, `designing-video-character-sheets`, `storyboarding-video` | Text and generic prompts only; no automatic project folder, `project.json`, stills, or sample video. An image-backed production package uses `video-production-assets` and its review contract. Saving a requested text document alone does not authorize that switch or image generation. |
| Campaign, paid ad, product promo, UGC, or conversion-led social video | `content-production-marketing` when campaign strategy, claim research, or performance-specific content is requested | `video-production-assets` for explicit production assets; `creative-production` for the multi-stage render/edit route; `fal-video-production` only when Fal is the chosen execution provider. An ad may use hook → demonstration/proof → payoff → CTA when the brief supports it; none of those beats, product wording, or a CTA is universal. |
| Source-derived YouTube/interview/podcast shortform | `youtube-content` for YouTube transcript-derived content; `content-production-marketing` for campaign or performance requirements | `video-production-assets` for a requested source/claim/shot handoff; `video-pipeline` or `fal-video-production` only for the selected executor. Preserve source facts and inspect the actual source media when required. |
| Abstract, music-led, or visual-concept clip | `video-prompt` or `video-shotlist` for a prompt/shotlist request | `creative-production` for multi-stage generation, controlled 3D, assembly, or delivery; use the relevant media executor only after confirming live capabilities. Do not add a story or ad structure without a brief reason. |
| Single prompt, model comparison, or prompt rewrite | `video-prompt`; `video-model-router` only if model choice is unresolved | Query a current model catalog, exact input schema, limits, and pricing. Do not choose from a remembered/static model table. A prompt or model recommendation is not a generation request. |
| Edit or critique of existing footage | `video-critique` or the requested editing workflow | `video-pipeline` or the selected provider's edit executor only when editing is requested. Keep one-asset edits narrow; do not create a new project manifest unless the work becomes multi-stage. |
| Controlled camera-space specification or proxy scene | `camera-spatial-design` for camera and blocking mathematics; `blender-previsualization` for implementation and rendered geometric checks | Preserve shot IDs and spatial-contract versions across the handoff. A projection or proxy render is not a finished video or an aesthetic guarantee. |

A standalone specialist call confirms scope/route with `creative-production` once, then performs only the requested specialty. A specialist already delegated by `creative-production` continues its assigned stage without calling back, re-routing, or opening a second interview or approval ledger.

## Execution and approval gates

- **Preproduction versus execution:** For topic-to-video production and image-backed preproduction requests, read [`preproduction-review.md`](../video-production-assets/references/preproduction-review.md) before project writes or media calls. It requires an exact project folder, applicable artifacts, required review stills through `codex-imagen`, inspection, and a review report. Explicit text-only/no-generation planning follows the text lane instead; single assets use only their requested modules. No sample video, moving animatic, or local/free video export bypasses the separate execution gate.
- **Multi-stage state:** Use `project.json` for a multi-stage production contract, with stable asset IDs, claims/provenance, versions, approvals, and output status. Do not create a manifest/database for a single prompt or edit.
- **Review versus video authorization:** Keep the video model unresolved during preproduction. User acceptance covers the reviewed artifact versions, not video production. Only a separate request to proceed opens live model/price planning; execute after explicit approval of that bounded plan. Modified inputs invalidate affected review/execution approvals. Automated judgments and successful validators do not authorize user actions.
- **Dynamic capability:** Before selecting or calling a provider, inspect the live catalog and the exact schema for the selected endpoint and input mode. Verify duration, aspect, resolution, reference/audio/edit support, destination constraints, rights/terms, and current pricing from current authoritative sources. Unknown support means stop before submission; do not substitute a guessed model.
- **Spend:** Show the live price and bounded scope, then obtain explicit approval before any paid submission. Creative approval, batch mode, or “handle it” alone is not spend approval. Do not expand retries beyond an approved scope.
- **Delivery:** A storyboard, prompt, API success, or predicted result is not a generated-video deliverable. Confirm the actual output exists, inspect it with available technical and visual checks, and record unverified checks honestly.
- **Publishing:** Do not post or publish an output unless the user separately requests publication and the destination's requirements are verified.
- **Single-owner handoffs:** `creative-production` owns content/video lane selection and shared project coordination. A specialist owns its subtask, preserving existing lane-local manifests/story bibles; delegated work continues without routing back or starting another interview/approval ledger. Do not duplicate a paid shot through executors.

## Existing specialist IDs

These names describe optional skills that may be present in the agent's local skill root; none of their skill bodies are included here:

- Creative/story stages: `synopsis-craft`, `script-craft`, `sw-premise-theme`, `sw-story-structure`, `sw-character-conflict`, `sw-dialogue`, `sw-scene-craft`, `sw-format-adaptation`, `char-design`.
- Focused content/story-commerce: `story-pipeline`, `storyboard-craft`, `content-production-marketing`, `youtube-content`.
- Text-planning lane: `orchestrating-video-preproduction`, `developing-video-synopses`, `designing-video-character-sheets`, `storyboarding-video` (text artifacts only; no media or file side effects).
- Prompt/model/edit/execution: `video-prompt`, `video-shotlist`, `video-model-router`, `video-critique`, `video-pipeline`, `fal-video-production`.
- Review-image generation: `codex-imagen` is required for the image-backed preproduction branch, but its helper and OAuth setup are not bundled. Report missing installation/auth or applicable spend approval rather than silently switching providers.
- Other rendering surfaces, when directly relevant: `comfyui`, `remotion-create`, and `remotion-render`.

If a named skill is absent, continue only with a supported route and state the limitation; do not fabricate its behavior.

## Routing smoke examples

Use these as route checks when integrating the guide into a local skill set; none of the examples authorizes generation, spend, or publication by itself.

| Request | Expected route | Boundary to preserve |
|---|---|---|
| “Prepare a source-backed 15-second factual explainer plan; no characters, ad, media generation, or files.” | `creative-production` → applicable text-planning/evidence specialist. | No fictional conflict, commercial beat, folder questionnaire, or images; claims need real sources. |
| “Write one 8-second prompt for a macro flower shot using my selected model; return text only.” | `creative-production` → `video-prompt`; `video-model-router` only for a needed capability check. | No full production package, job submission, or spend. |
| “Give me a shot list for a general educational clip.” | `creative-production` → relevant `video-production-assets` module or `video-shotlist`. | No story-commerce schema or media generation. |
| “Use the story-commerce format to write a product-conversion story.” | `creative-production` → `story-pipeline` and only the requested stages. | Its product-conversion contracts apply because that format was explicitly selected. |
| “Turn this YouTube interview into Shorts and preserve the interview's claims.” | `creative-production` → `youtube-content`; marketing specialty only if briefed. | Preserve source fidelity; render only requested media, no implied publication. |
| “Render the approved shots through Fal; I approved the live quote for these exact shots and settings.” | `creative-production` → `fal-video-production`, preserving the approved handoff. | Recheck schema/price; no endpoint changes, extra retries, or publication. |
| “Post the finished video to my selected channel.” | `creative-production` → named publishing integration. | Explicit publication still requires destination/account checks. |
| “Make a video about this topic; I have not chosen a folder.” | `creative-production` → `video-production-assets` preproduction branch. | Ask for an exact project folder before writes or media calls; source, runtime, framing, and judgment tool are project-specific. |
| “The preproduction package looks good.” | Record acceptance for the reviewed artifact versions. | Wait for a separate video-production request; no model selection, sample render, or spend from this acceptance alone. |
| “Only write a lighting plan in chat.” | `creative-production` → `video-production-assets` lighting module. | No folder questionnaire, images, or full-package expansion. |
