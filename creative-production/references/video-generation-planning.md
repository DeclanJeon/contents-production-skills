# Video generation planning, prompting and critique

On-demand reference for the video execution lane. Load this only when the request involves AI video model selection, prompt composition, shot decomposition for generation, hybrid pipeline design, or critiquing a generated clip. A planning artifact — requirements matrix, dialect-correct prompt, shot plan, or QA verdict — is a deliverable; it never authorizes a paid job, media submission, or publication.

Nothing here requires a specific provider, catalog file, or runtime. [video-prompt-dialects.json](video-prompt-dialects.json) contains provider-independent serialization examples, not model capabilities. Verify the selected endpoint's current syntax, availability, limits and price; a generic grammar example is not proof that a named model accepts it.

## 1. Shot requirements matrix

Use the canonical [production-execution reference](../../video-production-assets/references/24-production-execution.md) §3 to build per-shot hard requirements and preferences. A single prompt with a supplied verified input contract does not need a model comparison.

## 2. Model routing — live verification workflow

Read the same canonical reference §1–3 for cost eligibility, image discovery, live endpoint verification and per-shot routing. It owns the requirement matrix and cost policy; this coordinator reference owns prompt serialization (§3) and hybrid decomposition (§4), not another model catalog or budget ledger.

Carry the verified route/input contract into the prompt. Missing required live evidence blocks submission, not ordinary text preparation. Reuse supplied decisions and preserve the named provider; recommendations and fallback proposals never substitute for current-version execution/spend approval. Actual submission, async job handling and targeted revision follow §6.

## 3. Prompt composition — slots and dialects

Fill only the slots that serve the requested shot, then serialize using the verified input contract.

| Slot | Purpose |
|---|---|
| shot_type / subject | Framing and identifiable subject anchors |
| start_state / action / end_state | Observable change and edit-ready boundary states |
| setting / camera / lighting / style | Supported staging, movement and look |
| audio / dialogue | Only when requested and supported by the selected endpoint |
| duration / aspect / resolution / seed | Separate supported API controls from prompt text |
| negative | Targeted known failure only, using supported syntax |

Read [video-prompt-dialects.json](video-prompt-dialects.json) for narrative, production-spec, edit-command and interactive patterns. Natural-language instructions, reference labels, timestamps and sound markers are examples, not universal API syntax. Preserve the user's requested language. Do not infer current model support, quality, length caps or resolution from a static table.

Composition rules:

1. Never emit a prompt for a feature the model lacks (dialogue on a silent model, 30s on an 8s cap).
2. Prefer one coherent primary camera action per shot; split incompatible moves or unmanageable beats while preserving the requested sequence. This is a planning default, not a universal one-move model limit.
3. Use concrete physical action rather than abstract intent when the endpoint's guide recommends it (e.g. "the woman smiles and waves", not "embodies joyful greeting").
4. For image-to-video endpoints with a motion-focused guide, let the input image carry its static appearance and describe motion/change in text. Do not generalize this to endpoints that require identity or scene restatement.
5. Use negative instructions only for a known failure and only where supported. Runway Gen-4's guide explicitly rejects negative phrasing; use a positive target such as "locked camera" there, not a minimal negative list.
6. API-level controls (seed, aspect, duration, motion strength, structured camera params) belong in parameters when the endpoint exposes them, not prompt text.

When a local prompt corpus is configured, inspect its real layout before lookup. `VIDEO_PROMPT_CORPUS` may identify the corpus root; record actual example paths and reuse structure, not source content. An absent corpus does not block a normal prompt, and historical inventory totals, frequency statistics or host paths are not bundled evidence.

## 4. Shot decomposition and hybrid pipelines

Use the selected endpoint's verified duration limit and controllable action complexity to decompose the sequence. A **production storyboard** already includes the [complete contract](../../video-production-assets/references/storyboard-contract.md)'s integrated shot/camera/spatial/VFX/speech/audio specifications and clean-panel mapping; narrative panels still are not timed model clips. Preserve their order, IDs, reveal timing and continuity anchors.

For each clip inherit shot/scene/beat IDs and source synopsis locator, approved board version, start/peak/end panel IDs and actual image file/asset/hash, local-to-global action intervals, canonical subject/prop states, camera/spatial versions, VFX, literal speech/voice/lipsync and audio-cue IDs. Missing required cuts or unresolved image-only story blockers stop a production-board handoff. A text-only plan may state missing files honestly; it is not a visually approved board. Verify the selected endpoint's actual support before translating timestamps, first/last-frame inputs, audio or camera controls.

Repeat stable subject descriptors and supply approved references using documented input roles. Time-addressed beats and first/last-frame chaining are conditional techniques, not universal model features. A chained last frame must be inspected before it becomes the next reference, since it can carry an identity/contact defect forward. Return `Shot ID [start–end] — source beat/panel IDs, framing, local action intervals, camera, continuity anchors, prompt and applicable VFX/audio/speech/lipsync`, omitting unrequested detail for a single-prompt response. Technical shot ownership remains with the production-assets shot module; model splitting must not silently drop the intermediate contact/reveal states.

**Hybrid pipeline recipes**:

- **Blender plate + conditional reference input**: use Blender to specify the reference camera path, lighting and composition, then render the approved plate. Before assigning an image/video route, inspect the selected endpoint's current schema for accepted media roles and any first/last-frame fields. An uninspected or absent field is not an available route. Never promise that a generated continuation preserves Blender camera, geometry or lighting; inspect actual output.
- **Image → video two-stage**: establish approved art direction in the image stage. Use image references only when the selected endpoint's current schema declares the required role; follow that endpoint's documented prompting guidance. This is a handoff pattern, not a cross-model quality ranking.
- **ComfyUI**: use only an identified, installed workflow after inspecting its actual graph, model files, dependencies, resource requirements and input/output contract. Do not infer a usable workflow from the ComfyUI name. Duration/resolution are controls only when the inspected nodes expose them. Local computation does not bypass execution approval or imply zero cost.
- **Video edits**: select an edit route only when the chosen endpoint's current schema accepts the source video and declares the requested operation. List only documented operations; words such as extend, replace, restyle, remove or relight describe intent, not provider support. If the exact field is absent or uninspected, mark the route unresolved.
- **Conditional code/motion-graphics composite**: use when the brief requires exact, repeatable or editable typography, interface graphics or beat timing. This assigns controllable layers; it is not a quality guarantee or proof that a generated layer cannot meet the brief. For mixed work, assign layer ownership and define the plate, matte/alpha or other separation, occlusion order, timing source and final compositor before generating inputs. A generated-video-only or live-action route remains valid when appropriate. Do not require a chroma color, application or rendering framework; choose separation from subject colors, edges, motion blur and actual executor support. Inspect temporal edges and the composite over the intended background.

| Goal | Conditional plan |
|---|---|
| Camera/composition reference to preserve and verify | Blender plate; use a reference input only if the selected endpoint's current schema declares it |
| Character-reference continuity to inspect across clips | Use identity/reference inputs only when declared in the current schema; inspect actual outputs and make no consistency guarantee |
| Long sequence with inspected joins | Shot decomposition; frame chaining only when the exact current schema supports it and joins can be inspected; otherwise plan separate shots |
| Fix/restyle existing footage | Use only a current, schema-declared video input and edit operation; otherwise report the route unresolved |
| Authorized local execution | Use an identified installed ComfyUI workflow only after runtime, dependencies and its input/output contract are inspected |

For outputs collected from concurrent jobs, bind each file to its actual request/job/result identifiers before registering it as an asset. Never associate results by newest-file timestamps or shared-directory scan order. If the executor exposes no reliable result binding, isolate outputs per job or serialize collection; inspect content against the requested shot before marking the existing canonical asset verified. Do not add a parallel ledger.

## 5. Generated-clip critique and iteration

For actual inspection passes, failure evidence, severity, routing verdicts and bounded retries, read [the canonical generation QA/retry reference](../../video-production-assets/references/21-generated-video-qa-retry.md). It owns the production-side QA procedure; this coordinator does not maintain another scoring rubric or attempt ledger.

A critique requires actual media or explicitly supplied observations. Separate supplied observations from your own viewing/listening and causal hypotheses. Return the requested findings and correction; unavailable checks remain unverified. Critique or a corrected prompt is not approval to regenerate, reroute, spend or publish. Carry its shot/input version, problem timecode and repair criterion to the owning project artifact.

## 6. Submission and job lifecycle

Applies only to authorized actual media submission; text-only prompt/plan work ends at the artifact.

- Submit the approved scope through the selected executor's real interface — direct API, CLI, or a connected tool protocol, whichever it actually exposes; none is mandatory. Before submitting, confirm the approved N (shot/output count) and its total-estimate summary are recorded in the execution artifact; [production execution §1](../../video-production-assets/references/24-production-execution.md#1-비용-정책-free-first--no-paid-by-default) owns that estimate gate, and a missing or stale summary stops submission. Unsupported settings or an unverified price stop submission; a prompt or critique is not execution permission.
- Async jobs follow that tool's own wait/poll rule. Track the actual request/job/result IDs and pending status in the linked execution artifact; when an attempt is resolved, retain these details in `generation_attempts.notes` with its actual result. Unknown submit status is resolved through the tool's status check — never by resubmitting, which risks duplicate spend. Report failures and partial successes as they are.
- Inspect actual output before reporting success. Distinguish your own viewing/listening from user-reported observations.
- Targeted revision changes one primary variable at a time and names the preserved successful attributes (`generation_attempts.changes`, `preserve`), staying inside the approved retry/spend caps — see [QA/retry §5](../../video-production-assets/references/21-generated-video-qa-retry.md). Preserve historical attempt records; changed inputs make only affected dependent artifacts and approvals stale, not a new status field on attempts.

## 7. Evidence scope at this consumer

- **Prompt rules 2–5 and the motion-focused branch of §4:** [Runway, Gen-4 Video Prompting Guide](https://help.runwayml.com/hc/en-us/articles/39789879462419-Gen-4-Video-Prompting-Guide), read 2026-10-17, READ-PARTIAL: “Prompting for Iteration”, “Best Practices” (positive phrasing, direct/simple prompts, motion rather than input image, avoiding complexity), “Image prompts”, and “Subject Motion”. These sections support simple physical action, incremental detail and motion-focused i2v for **Gen-4**. They explicitly do not support negatives there. This is a live HTML article, not a local book rendition; URL and section headings are its locator, and no immutable byte/hash identity or generated-result validation is claimed. Recheck the selected endpoint rather than exporting these recommendations to every model.
- **Slots, four dialect patterns and hybrid handoff structure:** authored planning/serialization design. `video-prompt-dialects.json` examples demonstrate document shape only, not syntax accepted by any provider. The JSON conditions are prerequisites to verify, not verified endpoint capabilities. No book is being credited with model syntax, FLF2V, interactive steering, ComfyUI nodes or edit support.
- **Hybrid limits:** §4 proposes division of work, not measured superiority, guaranteed identity preservation or hard AI camera control. Blender's exact reference does not establish exact generated output. First/last-frame, reference-to-video, V2V verbs and time-addressed beats remain unsupported for an actual endpoint until its current documented contract is supplied or checked. The conditional code/composite route is an engineering choice for inspectable layers, not a claim that every generated clip fails typography or that every matte works.
- **Inherited gates:** canonical requirement, storyboard, execution and retry references retain their owners. This citation covers prompting only; it does not prove their craft claims, prices, rights or executor availability. Planning permission never becomes submission permission.
