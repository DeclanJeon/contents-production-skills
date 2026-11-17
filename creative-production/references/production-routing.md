# Current-stage routing

**Canonical route table: [routing.csv](routing.csv).** It is machine-readable,
covered by `scripts/routing_regression.py`, and frozen against
`creative-production/evals/routing-cases.json`. Edit the CSV, not a copy of it.

This file no longer restates the route table (that duplication was the drift
source). It keeps only the prose that does not fit a CSV cell:

- the **step sequence** for a full image-backed package under `R24`
- the **silent/animatic assignment** precedence
- the **Blender decision gate** trigger definition
- the **Open 3D module selection** table
- the **selected runtime gate**
- **state and handoff** rules

Select the narrowest requested output. The coordinator reads this file once
after `routing.csv`; workers consume their assigned packet and never reroute.
No automatically running agent engine is supplied.

Standalone writing, social/campaign operations, brand identity, product pages, product photography and website requests stay with their non-video owner; they do not activate this coordinator. The separated pack is discovered by exact skill name only when the user requests that independent work.

한국어 영상 대사·내레이션 후편집은 기존 각본 오너의 [선택 지원 참조](../../video-production-assets/references/korean-script-postediting.md#scope)를 사용한다. 일반 글쓰기까지 총괄 활성화를 확장하거나 별도 stage·worker·원장을 만들지 않는다.

<a id="full-package-sequence"></a>
## Full image-backed package sequence (R24)

`creative-production` is the sole coordinator for an explicit image-backed full
preproduction package. It sequences the existing owners in this order:

1. source/brief and synopsis (`developing-video-synopses`)
2. screenplay using `video-production-assets/references/03-screenplay.md`
3. applicable character SSOT and active LOOK/style-world bible
4. required locked character/location/prop/product masters and scene derivatives
5. indexed technical storyboard (`storyboarding-video` + storyboard contract)
6. cross-stage content/cause/coverage/continuity/timing QA and minimum
   correction loop
7. still-image generation and ordered storyboard sheets
8. mandatory per-scene/per-panel extraction
9. structural and visual QA/correction
10. versioned handoff

`orchestrating-video-preproduction` handles only the text stages assigned to it
and returns text plus indexed gaps; the coordinator then resumes the remaining
owners.

Do not silently omit the requested screenplay. Resolve every synopsis
event/beat through the script and board; check every fact/event, causal
transition, continuity state, required dialogue/caption/audio, scene, shot and
panel for omission or contradiction, and verify that allocated time sums to the
requested total. Correct in-scope mismatches and repeat affected checks before
proceeding; changed inputs stale only their true dependents. Structural
validation is not meaning or visual QA.

Each storyboard sheet has at most eight panels; use fewer for readable dense
cards. Package complete eligible output with the existing versioned ZIP and
`--require-final` contract; never package a blocked PRELIMINARY state as FINAL.
A portrait or prompt cannot substitute for a master pack, and text or individual
panels cannot substitute for actual sheets plus all extracted scene/panel images.

**Finality gate (v5.1).** Lock the active LOOK via `look_asset_id`; register
masters once and make scene states version-pinned derivatives through
`master_asset_ref`. A final artifact needs `finality: final` plus
`required_asset_versions`, valid only when every referenced asset is a `verified`
lock at matching version (`available` files are not locks). Unlocked inputs may
generate `finality: preliminary`, which is not a continuity-locked deliverable.
`asset_gate.check_asset_gate` must be empty before final generation or delivery.
Record only observed provenance; else `UNKNOWN`/`NOT_EXPOSED`.

<a id="silent-and-animatic-assignment"></a>
## Silent and animatic assignment

Select the requested **artifact and current stage**, not the word “silent” alone:

- Existing-still assembly/edit stays with `storytelling-with-still-images`, including dialogue-free and fully muted versions. Add silent story craft only for requested new/revised storytelling, not merely because the soundtrack is absent.
- Explicit local repeated-gag satire uses `silent-satire-animatic`. Generic drama, grief, action or long-form does not inherit its 85–120s / notice→land constraints. A conflict between a locked brief and that local contract is surfaced, not resolved by silently changing the brief.
- An approved story/board that needs only shot timing, cut/hold revision or a timed-board test plan uses `animatic-direction`. Preserve approved story content; do not reopen synopsis/characters or require a new silent screenplay.
- New/revised no-dialogue visual storytelling uses `silent-visual-storytelling`. Ordinary narrated scripts and ordinary production boards keep their existing owners. A no-audio flag on an otherwise locked project does not create a new story stage.
- When story and temporalization are both requested, assign the story work first; pass the accepted/clearly proposed story version and stable beat/state references into the requested animatic stage. For a larger package, these specialists support only the applicable assigned text stages; `creative-production` remains the sole coordinator, and the current board owner retains the complete technical contract. Do not load both skills for every animation or add an unrequested animatic/render step.

**Silent story packet:** assign only the requested scenes/beats; carry source/brief/approved story versions, desired information and emotional changes, locked facts, genre/runtime if supplied, continuity and separate dialogue/narration/nonverbal vocal/audio/caption constraints. Request visible cause→choice→result, specific performance/composition/environment cues, disclosure/withholding, retained end state, alternative reading and unverified checks. The worker uses existing story/04/06/12 owners and returns indexed artifact changes, not a new research ledger or mandatory source reanalysis.

**Animatic packet:** carry the approved story/board and its IDs/versions, required action/reveal/state sequence, fixed or flexible runtime, supplied/proposed/unknown FPS, audio intent and actual media availability. Request existing06 shot-local cues,08 poses/contact/spacing and09 final cut/hold/reaction timing, duration conflicts, continuity and scoped playback-test status. Missing actual media means playback `UNVERIFIED`, not failed story drafting; time plans never authorize image/video/audio generation. The coordinator reconciles returns and persists only authorized state updates under the existing single-writer contract. Specialist outputs do not constitute user acceptance or execution approval.

## Blender decision gate

For requested native Blender modeling, materials/lighting, staged exploded views or rendered web assets beyond proxy previs, assign `open-3d-production` with the relevant modules below. `blender-previsualization` retains its camera/spatial verification owner and existing proxy adapter limits. A native beauty/asset request does not make that adapter a production renderer; a web-only request does not turn Three.js evidence into Blender verification.

**Blender trigger:** explicit Blender/previs request, or the requested result depends on validating an actual scene-specific 3D arrangement (camera path, geometry, blocking, occlusion, clearance, or contact), or a 3D-verified result is part of the requested deliverable. A camera field, camera move, storyboard, or scene ID alone is not a Blender trigger.

“Scene-specific 3D camera/spatial design” means actual scene-specific 3D geometry/placement/feasibility design under this trigger, not narrative camera descriptions or numeric proposals alone. This is the canonical routing table; specialists use this gate without creating another route table.

Text-only/read-only work may plan later previs but must not execute Blender; mark unperformed checks PLANNED/UNVERIFIED or BLOCKED. If required Blender is absent, report the exact missing runtime/evidence, continue independent work, and mark only dependent spatial deliverables BLOCKED/UNVERIFIED; no alternate-renderer substitution or FINAL claim. Numeric/schema checks and smoke runs do not prove actual 3D scene feasibility or full requested visual inspection. Smoke is pipeline preflight only, not full-scene/all-requested-frame/contact acceptance. Completed previs records actual Blender version/mode, preserves camera spec/version and shot/scene/panel IDs, and requires reopening requested .blend/image outputs and inspecting relevant frames. Bounding-box, center-point and ray-cast proxies do not prove articulated visibility, contact, performance, aesthetics or final generated-video quality; unsupported claims stay UNVERIFIED.

## Open 3D module selection

The active orchestration owner selects modules and order here, then hands off one bounded artifact to `open-3d-production`. For in-boundary video/storyboard work, that owner is `creative-production`; standalone non-video Blender/web work keeps its existing host/design owner and does not activate video production. Read the specialist's [integration rules](../../open-3d-production/references/integration.md) before using upstream text. Select by output, not every related-skill mention.

For a native Blender deliverable, select the matching native recipe first. The overlapping upstream rows supply only explicitly needed supplemental craft; they do not redirect native authoring into Three.js. Choose an upstream browser module as the implementation owner only for a requested browser-native output. The native worker may write a new Blender script in the assigned project root under the existing execution and inspection contract.

| Assigned need | Conditional module / required read | Evidence and stop boundary |
|---|---|---|
| Reference-to-generation semantic proxy, replacement colors, stateful prop revision | `blender-previsualization` [semantic proxy handoff](../../blender-previsualization/references/semantic-proxy-handoff.md); native articulated/hinged work also assigns `open-3d-production` | Preserve camera spec/IDs, state-specific dimensions, identity mapping and actual reference slots; basic proxy adapter does not solve articulated contact |
| Native product lighting, Geometry Nodes repetition or timed procedural motion graphics | `open-3d-production` [native workflows B01–B03](../../open-3d-production/references/native-blender-workflows.md) and native adaptation | Actual version/engine, named controls/seeds and inspected timeline; no required paid rig or Three.js substitution |
| Camera tracking, plate projection or footage/3D integration | `open-3d-production` [native workflows B04–B05](../../open-3d-production/references/native-blender-workflows.md); camera/spatial owner when verification is requested | Distinguish observed motion from solved camera, mark estimated scale, inspect parallax/sliding/occlusion; not a feature of the proxy adapter |
| Grease Pencil, render passes/compositing, native loops, asset variants or GLB handoff | `open-3d-production` [native workflows B06–B10](../../open-3d-production/references/native-blender-workflows.md); only the matching section | Native `.blend`/requested exports and actual inspection; no automatic web, audio, simulation or generated-video job |
| Blender procedural modeling, materials/lighting or render craft; browser Three.js scene | [threejs-scene](../../open-3d-production/references/upstream/skills/threejs-scene/GUIDE.md); Blender target also reads [native adaptation](../../open-3d-production/references/blender-adaptation.md) | Native implementation uses actual Blender; browser starter uses Three.js. Preserve dimensions/seed/camera and inspect relevant views; no renderer substitution |
| Product parts, staged disassembly, x-ray or section presentation | [exploded-view](../../open-3d-production/references/upstream/skills/exploded-view/GUIDE.md); native adaptation for Blender | Named parts/assembled transforms, ordered motion and readable labels; illustrative internals labeled; geometry/contact acceptance still uses existing Blender verification |
| Scroll-driven presentation of approved rendered/generated clips | [scroll-film](../../open-3d-production/references/upstream/skills/scroll-film/GUIDE.md) | Assigned sequence/video, holds, crop and seam inspection; no automatic clip generation, portrait variant or website build |
| Transparent subject/plate keying or alpha web delivery | [alpha-cutout](../../open-3d-production/references/upstream/skills/alpha-cutout/GUIDE.md) | Actual alpha/edge composites on target backgrounds; native Blender RGBA preferred for native scenes; new plate generation remains separately assigned |
| Cursor-following illustrated pose playback | [cursor-rig](../../open-3d-production/references/upstream/skills/cursor-rig/GUIDE.md) | Fixed-body pose grid and browser player; not a Blender skeletal rig; missing clips return an input gap, not generation permission |
| Loop/chain repair, outpaint source restoration or generated-asset handoff | [motion-assets](../../open-3d-production/references/upstream/skills/motion-assets/GUIDE.md) | Existing approved inputs and package generation/history owners; diagnostics plus actual wrap inspection; no second intake, approval or prompt ledger |
| Browser/WebGL presentation QA | [site-check](../../open-3d-production/references/upstream/skills/site-check/GUIDE.md) | Requested browser/state/viewport matrix, screenshots and observed failures; no physical feasibility or automatic publish claim |
| Requested browser presentation recording or clip comparison | [frame-capture](../../open-3d-production/references/upstream/skills/frame-capture/GUIDE.md) | Exact assigned timing/viewport, inspected encoded output; not native Blender rendering or proof of real-time performance |

Do not load all eight guides or chain production → checking → recording by default. The coordinator assigns dependencies only when the artifact needs them, preserves locked facts/IDs and execution authority, and integrates the worker's evidence into the existing project/history. A missing browser tool blocks browser work, not independent Blender work; missing Blender blocks native output/verification, not an independently requested web presentation.

## Selected runtime gate

Apply this gate only before an actual requested runtime/provider operation, not text planning:

1. Verify the selected runtime/auth, actual live schema/capabilities, destination and rights/consent. Report missing prerequisites; installation is separate explicit scope, never automatic.
2. Apply [production execution](../../video-production-assets/references/24-production-execution.md): `codex-imagen` is the default still-image executor; no Higgsfield image submission/edit fallback. For Codex Imagen stills, do not check price, usage, quota, or block on unknown cost; verify only runtime/auth, supported inputs/outputs, destination, and rights.
3. Bind image calls to current input versions, exact requested outputs/settings, and practical retry/concurrency/time/storage limits. No Codex Imagen quote, free-allowance lookup, or cost cap is required. Keep separate video-generation and other-provider approval gates.
4. Preproduction acceptance, preview permission, final production and publication are distinct. No extra retries/batches/covers/training/analysis or live deploy inferred. Independent work may run concurrently; prior-frame dependencies and uncertain async jobs may not.
5. Preserve secrets/source files, inspect actual outputs, register only observed results. A private backend enhancer cannot be replaced by generic generation and claimed equivalent.

## State and handoff

For an existing project, [common handoff/single writer](../../video-production-assets/references/contract.md#worker-handoff-and-single-writer) owns ID/version lookup, worker return and authorized persistence. Domain bibles/provider adapters are linked artifacts. Text-only/no-save proposals do not write a ledger; a standalone artifact does not create one.

Actual saved content work uses `recording-production-history` before writes and after every observed output. Topic-to-video/image-backed work also reads preproduction-review. Use the history skill's path precedence, defaulting to the actual user's Documents/Media_Studio; preserve an explicit active project destination. Before the first save, ask once for a preferred project directory unless an active path, environment/config choice or existing default studio root resolves it. Create only used work folders; collect deliverables in `final/` and keep audit in `.history/`. Report absolute saved paths and history paths. Tools and interview frameworks are checked only when selected, never universal prerequisites.
