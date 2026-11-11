# Primary-source register: reusable Blender production workflows

Research and access date: **2026-11-03**.

Scope: reusable content-production methods across product lighting/rendering, procedural geometry, camera tracking/projection, Grease Pencil, Geometry Nodes motion graphics, compositing/passes/alpha, animation/loops, and asset/export pipelines.

**Evidence inventory: 25 inspected substantive primary sources: 19 Blender Manual pages, one Blender Python API page, and five first-party creator/production pages.** One additional access-limited article is recorded separately and is not included in that count. No video playback, media download, Blender execution, rendered output, or runtime compatibility test was performed. The parent-owned video `lyNzEk8H9AM` was not accessed or analyzed.

## Reading contract and provenance

- **D - inspected documentation:** text returned from an opened official Manual/API page. It establishes a documented contract for the pinned version, not a successful local execution.
- **T - inspected creator text:** the creator/publisher's article, course description, lesson notes, or identified author reply was read. It does not establish that an embedded video was watched.
- **C - candidate only:** a landing page or access barrier was inspected; substantive tutorial content was unavailable. It cannot substantiate implementation steps.
- **Adaptation:** a proposed production application inferred from the sources. These are recommendations for future skill authoring, not claims that the source demonstrates the exact proposed shot.
- Source dates below are publication dates only where exposed. Unknown dates remain unknown; search-engine crawl dates and comment dates are not silently treated as publication dates.

Official documentation is pinned to **Blender 4.5** as a coherent reference baseline, not asserted to be the newest Blender release. Search results also exposed rolling `latest` documentation labeled 5.2; those results were not used to import newer behavior into 4.5 instructions. Creator lessons may predate this baseline, so explicit compatibility notes take precedence over remembered UI steps.

Retrieval: web searches discovered sources; actual pages were then opened through web retrieval or direct HTTP Markdown extraction. Several `web.open` requests for Blender documentation returned a retrieval-layer 402 error; direct `webfetch` of the same pinned pages succeeded. That retrieval error is not evidence that the public Manual requires payment. CG Cookie's course page was inspected through `web.open`, because direct extraction returned no useful text.

Local context: no `AGENTS.md` was found inside this repository; direct checks of the Documents, Projects, and Skills-and-Automation ancestor paths also found no `AGENTS.md`. No `CLAUDE.md` or `CONTRIBUTING.md` was found in the repository search. The repository README and an existing research memo were inspected. The README places Blender craft under `open-3d-production` and spatial implementation/verification under `blender-previsualization`; this memo proposes reusable craft without changing those owners or claiming spatial verification.

## Coverage map

| Requested area | Grounding | Reusable output to develop |
| --- | --- | --- |
| Product lighting/rendering | S01, S02, S13, S21 | A named-light studio rig with receiver collections and optional light-group outputs |
| Procedural geometry | S03, S04, S05, S24 | Parameterized reusable generators, with late and selective realization |
| Camera tracking/projection | S08, S09, S10 | A solved-camera plate workflow or a bounded camera-projection setup, selected separately |
| Grease Pencil | S11, S12, S22 | Hybrid 2D/3D boards and camera-aware line-art overlays |
| Geometry Nodes motion graphics | S03, S05, S06, S07, S25 | Time-driven instanced motion; stateful simulations only when necessary |
| Compositing/passes/alpha | S13, S14, S15, S16 | Isolated elements, masks, intermediate sequences, and a stated alpha convention |
| Animation/loops | S06, S07, S17, S25 | Periodic analytic motion or cyclic F-curves, with explicit seam checks |
| Asset/export pipeline | S18, S19, S20, S23 | Curated source assets, explicit publication, and destination-specific export validation |

## Strongest eight workflow findings

Each workflow below is a proposed production adaptation. Source references establish its building blocks; the acceptance checks describe work a future implementation must perform, not tests executed during this research.

### W01 - Reusable product-lighting rig with independent controls

**Grounding:** S01, S02, S13; supporting curriculum text S21.

Build a product collection, a backdrop collection, and named key/fill/rim lights. Choose area-light shapes and dimensions to control the lighting pattern; make Normalize state explicit when adjusting size. Create dedicated receiver/blocker collections rather than coupling light-link membership to general scene organization. If post-production needs intensity/color alternatives, use Cycles Light Groups to output separate contributions.

Inputs: product scale/materials, hero camera, background intent, engine/version, light roles, receiver membership, delivery exposure/color settings. Outputs: reusable `.blend` setup, a light-role manifest, and optional light-group sequences.

Acceptance: inspect highlights and silhouette on the actual product; confirm the rim affects only intended receivers; compare the sum of the light groups to the baseline render. Light groups permit changing recorded contributions, not relocating lights or inventing new shadow directions. Light linking and light groups are different controls. Emissive-mesh linking is Cycles-only in S02; Grease Pencil is unsupported there.

### W02 - Procedural generators that stay instanced until necessary

**Grounding:** S03, S04, S05, S24.

Create points from the chosen distribution or curve, instance the source object/collection on them, expose count/spacing/scale/rotation and selection controls, and use a Repeat Zone only for iterative construction within one evaluation. Keep geometry instanced while changing transforms. Realize selected levels only when downstream operations require actual geometry or a destination contract demands it.

Adaptations include modular product arrays, ingredient layouts, repeating packages, branching decoration, and configurable set dressing. Retain editable parameters rather than only a flattened mesh.

Acceptance: confirm instances reference the intended source, check nesting transforms, compare realized and instanced appearance, and inspect the exported result separately. S04 documents potentially severe realization cost and attribute precedence, so no blanket speed or memory budget is asserted. S24 gives a concrete reason to carry version notes: its older curve-radius behavior must be adapted for 4.5.

### W03 - Prefer analytic time-driven motion for repeatable motion graphics

**Grounding:** S03, S06, S07, S17, S25.

For a design that does not need previous-frame state, drive instance transforms from Scene Time. A proposed periodic phase is `phase = 2*pi*(seconds - start_seconds)/period_seconds`; use periodic functions for the intended channels and add per-instance phase offsets for staggered waves. This formula is an adaptation, not a quoted node recipe. Use seconds for duration-based controls; reserve frame-based controls for deliberately frame-locked timing.

A Simulation Zone is for state carried between frames, not simply any animation. If needed, use Delta Time for rate-based updates, retain required state attributes, and bake before non-sequential rendering. A Repeat Zone is not a simulation or a timeline loop.

Acceptance: compare identical times requested in different frame orders; verify subframes where motion blur matters; inspect a wrap across the delivery boundary. Trigonometric periodicity alone does not prove that every material, noise field, camera, or particle state also loops.

### W04 - Separate camera solving from texture projection

**Grounding:** S08, S09, S10.

Choose the task first. To attach CG to a filmed plate, track and solve the camera, clean bad tracks, establish orientation/scale, then attach the reconstructed motion using Camera Solver or baked transforms. For a static image mapped onto geometry, use UV Project with a distinct projector camera and a named UV map. Do not present texture projection as reconstruction of real camera motion.

Camera solves require appropriate tracking evidence; S08's minimum marker count is a prerequisite, not a quality guarantee. S09 distinguishes tripod rotation from general translation and warns that refinement still needs reasonable initial intrinsics. UV Project follows the projector's perspective/orthographic mode and negative Z direction.

Acceptance: inspect plate registration throughout the intended interval, including frame edges; verify geometry does not cross behind the projector; evaluate parallax limits for the proposed camera move. Projection does not create unseen surfaces. The detailed matte-painting creator article in C01 was inaccessible and contributes no hidden implementation steps.

### W05 - Hybrid Grease Pencil boards and baked line-art overlays

**Grounding:** S11, S12, S13, S22.

Use a 3D environment for spatial layout and Grease Pencil for drawings, expressions, callouts, or board characters; organize shot timing with the sequencer when useful. For derived contours, use Line Art on a deliberate scene/collection/object scope with an active or specified custom camera. Set overscan where lines otherwise terminate at the image edge, then bake only after camera and geometry are sufficiently stable.

Outputs can be an animatic, an explanatory outline layer, or a stylized product overlay. Use the Grease Pencil render pass when separate finishing is required.

Acceptance: inspect near/far clipping and occlusion, check line continuity at image boundaries, and compare separate-pass compositing to Combined. S13 warns that some Grease Pencil blend modes can produce a different result when composited separately. S12 warns that clearing baked Line Art can also remove manually drawn strokes in that frame range; separate hand-drawn work before adopting a rebake procedure.

### W06 - Treat passes and alpha as a delivery contract

**Grounding:** S13, S14, S15, S16, S20.

Select required passes before rendering: Combined, suitable object/material Cryptomatte masks, specific lighting contributions, or Grease Pencil isolation. Enable Film Transparent for background replacement. Use compositor File Output nodes for named intermediate and final frame sequences. Record whether each handoff is premultiplied or straight alpha instead of relying on a filename alone.

Blender render layers are premultiplied according to S15. If an operation needs straight RGB, convert deliberately and return to premultiplied before Composite Output. Transparent background and transparent/refractive glass are separate settings.

Acceptance: composite over contrasting backgrounds, inspect soft edges, hair/lines, glass and motion blur, and compare pass reconstruction to Combined. S13 documents non-antialiased index/depth passes and EEVEE-specific pass limitations. Do not promise that Cycles and EEVEE deliver interchangeable pass sets. A future output-format choice must preserve the required channels; no specific encoder was tested here.

### W07 - Design loop boundaries, not just repeated playback

**Grounding:** S06, S07, S17, S25.

Use an F-curve Cycles modifier for existing keyed repeating motion, selecting Repeat Motion, Repeat with Offset, or Repeat Mirrored intentionally. Keep it first in the modifier stack. For procedural motion, use W03's periodic phase. For stateful effects, distinguish warm-up from the deliverable interval and design particle lifecycle/state recurrence explicitly.

A proposed sampling convention for `N` unique frames is to render one period without duplicating its equal endpoint. The appropriate frame numbering depends on the scene; this is a handoff convention, not a documented universal Blender requirement.

Acceptance: review last-to-first motion, position and velocity; include camera, lighting, texture phase, shadows, and emission. Repeat with Offset may be correct for traveling motion but is not automatically a stationary seamless loop. The creator reply in S25 explicitly cautions that simulations depend on prior frames; changing time units does not by itself make a simulation periodic.

### W08 - Publish reusable assets explicitly and validate the destination

**Grounding:** S18, S19, S20, S23.

Curate source objects/materials/worlds in saved library `.blend` files with useful descriptions and catalogs. Keep the editable source distinct from the published export. Use collection-level export scope to exclude reference objects and work-in-progress data. Choose GLB for a packaged transfer or separate glTF when an editable external file layout is needed.

Define exportable geometry, materials, animations, naming, paths, and target viewer expectations. S19 supports transform/bone/shape-key animation, not arbitrary animated material/light/physics properties. Its Geometry Nodes instance export is labeled experimental.

Acceptance: open the published artifact in the intended destination and inspect material appearance, hierarchy, scale, animation names/ranges, missing textures and supported extensions. S23 is evidence for explicit publication and reusable export settings, not a recommendation to copy the Studio's entire custom pipeline. Its author reports duplicate-ID, shared-index, and material-import-order problems.

## Inspected source register

All sources below were accessed **2026-11-03**. Manual/API publishers are the Blender documentation project / Blender Foundation. Unless explicitly stated, those pages expose no per-page publication date. Section locators identify inspected evidence rather than relying on search snippets.

### S01 - Light Objects

- URL: https://docs.blender.org/manual/en/4.5/render/lights/light_object.html
- Publisher/date/version: Blender Manual; publication date unknown; 4.5. Evidence **D**.
- Inspected evidence: **Common Settings**, **Area Light**, **Power of Lights**. Documents Temperature, Exposure, Normalize, emitter shapes/dimensions, and the distinction between radiant power and consumer electrical wattage.
- Supported method: shape and size lights deliberately while controlling intensity/exposure.
- Production adaptation: a reusable product-light rig with explicit Normalize state and named light roles.
- Limits: physical bulb wattage is not a direct scene-power prescription; changing size with normalization disabled changes emitted power. No lighting setup was rendered.

### S02 - Light Linking

- URL: https://docs.blender.org/manual/en/4.5/render/lights/light_linking.html
- Publisher/date/version: Blender Manual; date unknown; 4.5. Evidence **D**.
- Inspected evidence: **Setup**, **Include & Exclude**, **Performance**. Receiver and blocker collections can control illumination and shadow participation separately.
- Supported method: dedicated linking collections, reusable across lights.
- Production adaptation: highlight the hero product without relighting the backdrop; isolate a rim-light receiver set.
- Limits: Grease Pencil objects do not support linking; emissive-mesh linking requires Cycles. Shadow linking may add rendering cost. This is artistic control, not physically faithful isolation.

### S03 - Instance on Points Node

- URL: https://docs.blender.org/manual/en/4.5/modeling/geometry_nodes/instances/instance_on_points.html
- Publisher/date/version: Blender Manual; date unknown; 4.5. Evidence **D**.
- Inspected evidence: introduction and **Inputs**. Reuses geometry references on point-domain geometry; supports selection, per-instance rotation/scale and choosing instances from a list.
- Supported method: distribute repeated elements without duplicating their underlying geometry.
- Production adaptation: product grids, particles-as-design-elements, curved arrays and modular scenery.
- Limits: nested instances inherit parent transforms; selection/index/ID behavior matters when choosing assets. Not every Blender object type supports instancing through this node.

### S04 - Realize Instances Node

- URL: https://docs.blender.org/manual/en/4.5/modeling/geometry_nodes/instances/realize_instances.html
- Publisher/date/version: Blender Manual; date unknown; 4.5. Evidence **D**.
- Inspected evidence: introduction, **Attributes**, **Inputs**. Converts instances into geometry; selection and depth control the realization scope.
- Supported method: enable downstream geometry-level edits while understanding attribute propagation.
- Production adaptation: keep layout instanced, then realize only branches needing deformation or mesh delivery.
- Limits: complex high-count inputs can perform much worse; base-geometry attributes take precedence over same-named instance attributes. Only the first volume component is moved to output when multiple volume instances are present.

### S05 - Repeat Zone

- URL: https://docs.blender.org/manual/en/4.5/modeling/geometry_nodes/utilities/repeat_zone.html
- Publisher/date/version: Blender Manual; date unknown; 4.5. Evidence **D**.
- Inspected evidence: introduction, **Inputs**, **Properties**. Repeats a node region, feeding results between iterations; outside inputs remain constant during those iterations for the current frame.
- Supported method: parameterized iterative geometry construction without duplicating an arbitrary number of nodes.
- Production adaptation: stacked tiers, modular towers, repeated construction or bounded recursive-looking structures.
- Limits: zone outputs pass through Repeat Output. Iteration is within evaluation, not frame-to-frame simulation and not seamless animation.

### S06 - Scene Time Node

- URL: https://docs.blender.org/manual/en/4.5/modeling/geometry_nodes/input/scene/scene_time.html
- Publisher/date/version: Blender Manual; date unknown; 4.5. Evidence **D**.
- Inspected evidence: **Outputs**. Provides seconds and frames; Frames can return non-integer values for motion-blur evaluation.
- Supported method: derive procedural animation from evaluated scene time.
- Production adaptation: shared phase controls for waves, orbiting instances, reveals and repeating product arrangements.
- Limits: integer rounding may defeat intended subframe behavior; a time source alone does not create a loop, stable random identity, or simulation recurrence.

### S07 - Simulation Zone

- URL: https://docs.blender.org/manual/en/4.5/modeling/geometry_nodes/simulation/simulation_zone.html
- Publisher/date/version: Blender Manual; date unknown; 4.5. Evidence **D**.
- Inspected evidence: introduction, **Clock**, **Inputs**, **Baking**. Carries state across frames, offers Delta Time and caches playback; disk baking permits non-sequential rendering.
- Supported method: stateful Geometry Nodes effects with an explicit cache/bake boundary.
- Production adaptation: accumulating trails, growth or particle systems whose history matters.
- Limits: modifier context only, not Tool context. Required anonymous attributes must be explicitly retained in state. Baking affects all simulations in all modifiers of selected objects; cache behavior is not a seamless-loop guarantee.

### S08 - Camera Solver Constraint

- URL: https://docs.blender.org/manual/en/4.5/animation/constraints/motion_tracking/camera_solver.html
- Publisher/date/version: Blender Manual; date unknown; 4.5. Evidence **D**.
- Inspected evidence: introduction, prerequisite note and **Options**. Uses reconstructed camera location/rotation; can use the active clip and convert constrained motion to F-curves.
- Supported method: connect a solved footage camera to a Blender object/camera.
- Production adaptation: place explanatory CG or a product insert into a tracked shot.
- Limits: the documented minimum of eight markers and a completed solve is only a prerequisite. This page alone does not establish track quality, intrinsics, scene scale or a reliable reconstruction.

### S09 - Solve

- URL: https://docs.blender.org/manual/en/4.5/movie_clip/tracking/clip/toolbar/solve.html
- Publisher/date/version: Blender Manual; date unknown; 4.5. Evidence **D**.
- Inspected evidence: **Solve**, **Cleanup**, **Orientation**, **Scene Setup**. Describes tripod solving, initial keyframe selection, refinement controls, track cleanup and scale/orientation tools.
- Supported method: clean and orient a solve rather than treating the solve button as the whole workflow.
- Production adaptation: separate static-rotation plates from translation/parallax plates and document camera assumptions.
- Limits: tripod mode cannot recover actual feature depth; intrinsics refinement requires reasonable initial values. Some orientation cross-reference labels in the retrieved page are inconsistent, so follow named operators rather than deriving an exact click sequence from those labels.

### S10 - UV Project Modifier

- URL: https://docs.blender.org/manual/en/4.5/modeling/modifiers/modify/uv_project.html
- Publisher/date/version: Blender Manual; date unknown; 4.5. Evidence **D**.
- Inspected evidence: introduction, **Options**, **Usage**, **Known Limitations**. Projects UVs along negative Z, supports up to ten projectors, and respects camera projection mode.
- Supported method: map an image through a controller/camera onto geometry using a specified UV map.
- Production adaptation: camera-projected illustration, bounded matte projection, or decals on set geometry.
- Limits: vertices behind a perspective projector are not mapped properly. The inspected 4.5 page does not contain all the additional low-poly caveats visible in rolling newer documentation; do not silently attribute those newer notes to it.

### S11 - Grease Pencil: Introduction

- URL: https://docs.blender.org/manual/en/4.5/grease_pencil/introduction.html
- Publisher/date/version: Blender Manual; date unknown; 4.5. Evidence **D**.
- Inspected evidence: introduction, **Quick Start**, **2D Animation Template**. Strokes are points in 3D space; the object supports 2D/cutout animation, motion graphics and storyboarding.
- Supported method: create keyed drawings and edit/sculpt strokes with materials/modifiers.
- Production adaptation: combine 3D proxy space with expressive 2D subjects or explanatory callouts.
- Limits: the 2D template has preconfigured drawing-plane, layer and view settings. Do not assume these are the same as an ordinary new 3D scene or copy old Grease Pencil APIs without checking them.

### S12 - Line Art Modifier

- URL: https://docs.blender.org/manual/en/4.5/grease_pencil/modifiers/generate/line_art.html
- Publisher/date/version: Blender Manual; date unknown; 4.5. Evidence **D**.
- Inspected evidence: introduction, **Geometry Processing**, **Composition**, **Bake**. Generates camera-dependent lines from geometry; supports custom camera, overscan, source selection and baking.
- Supported method: derive editable/baked stylized outlines from 3D layout.
- Production adaptation: product diagrams, line-art overlays and outlined animatics.
- Limits: active camera required; additional modifiers can repeat expensive occlusion work. Cache reuse has settings restrictions. Clearing baked Line Art can erase manual strokes within the affected range.

### S13 - Passes

- URL: https://docs.blender.org/manual/en/4.5/render/layers/passes.html
- Publisher/date/version: Blender Manual; date unknown; 4.5. Evidence **D**.
- Inspected evidence: **Data**, **Cryptomatte**, **Shader AOV**, **Light Groups**, **EEVEE Limitations**. Defines isolated data/images, masks, custom shader outputs and Cycles light-group contributions.
- Supported method: separate render information for targeted compositing.
- Production adaptation: product/material masks, per-light finishing and isolated Grease Pencil effects.
- Limits: Z/Position/index passes are not antialiased; Cryptomatte's Cycles behavior includes transparency, motion blur and depth of field. EEVEE differs for blur, blended surfaces and AOVs. Grease Pencil blend modes can prevent exact reconstruction from a simple separate Alpha Over.

### S14 - Film

- URL: https://docs.blender.org/manual/en/4.5/render/cycles/render_settings/film.html
- Publisher/date/version: Blender Manual; date unknown; 4.5/Cycles. Evidence **D**.
- Inspected evidence: **Transparent**, **Pixel Filter**, opening Exposure description. Transparent removes the world background for compositing; Transparent Glass and its roughness threshold are separate controls.
- Supported method: produce an element intended to be placed over another background.
- Production adaptation: product cutouts, graphic overlays and reusable 3D elements.
- Limits: Film exposure acts on data, whereas Color Management exposure acts on the view transform. A transparent world is not proof of correct glass or edge behavior in another compositor.

### S15 - Alpha Convert Node

- URL: https://docs.blender.org/manual/en/4.5/compositing/types/converter/alpha_convert.html
- Publisher/date/version: Blender Manual; date unknown; 4.5. Evidence **D**. The retrieved edit link points to the `types/color/alpha_convert.rst` source; the requested URL resolves successfully.
- Inspected evidence: introduction and **Mapping**. Blender render layers are premultiplied; the node converts between straight and premultiplied alpha.
- Supported method: perform alpha representation changes deliberately around operations that need them.
- Production adaptation: a finishing handoff that names alpha mode and validates edges.
- Limits: convert back to premultiplied before Composite Output after straight-alpha operations; otherwise artifacts may occur. Conversion is not a substitute for fixing the source matte.

### S16 - File Output Node

- URL: https://docs.blender.org/manual/en/4.5/compositing/types/output/file_output.html
- Publisher/date/version: Blender Manual; date unknown; 4.5. Evidence **D**.
- Inspected evidence: introduction, **Inputs**, **Properties**. Writes image sequences during rendering and can save intermediate node-tree outputs. Names combine a base path, image name, frame number and extension.
- Supported method: save planned intermediate and final outputs automatically.
- Production adaptation: parallel beauty/mask/element sequences with explicit directory and naming conventions.
- Limits: the node has no output sockets; connection alone is not proof that a render ran or files were produced. File format and channel preservation need separate delivery choices.

### S17 - F-Curve Modifiers

- URL: https://docs.blender.org/manual/en/4.5/editors/graph_editor/fcurves/modifiers.html
- Publisher/date/version: Blender Manual; date unknown; 4.5. Evidence **D**.
- Inspected evidence: **Cycles Modifier**, **Trivially Cyclic Curves**, **Stepped Interpolation Modifier**. Supports repeated, offset and mirrored cycles; trivial cycles receive cycle-aware handle/keying support.
- Supported method: repeat keyed motion non-destructively or deliberately step animation sampling.
- Production adaptation: turntable channels, bobbing objects, repeated mechanical movement or stylized low-frequency motion.
- Limits: Cycles must be the first modifier. Repeating values is not proof of a visually seamless scene; offset cycles intentionally change values between repetitions.

### S18 - Asset Libraries: Introduction

- URL: https://docs.blender.org/manual/en/4.5/files/asset_libraries/introduction.html
- Publisher/date/version: Blender Manual; date unknown; 4.5. Evidence **D**.
- Inspected evidence: **What is an Asset Library?**, **Life Cycle of an Asset**, **Design Limitations**. Libraries scan saved blend-files; assets are curated data-blocks with metadata and catalogs.
- Supported method: mark reusable data, save its source in a registered library, and share source files plus catalog definitions.
- Production adaptation: reusable lighting worlds, props, materials and controlled generator assets.
- Limits: Mark as Asset does not copy the file into a library. Ordinary image/audio files are not supported asset types here. Editing usually requires opening the asset's source blend-file; special managed brush files have different rules.

### S19 - glTF 2.0

- URL: https://docs.blender.org/manual/en/4.5/addons/import_export/scene_gltf2.html
- Publisher/date/version: Blender Manual / bundled glTF importer-exporter documentation; date unknown; 4.5. Evidence **D**.
- Inspected evidence: **Meshes**, **Exported Materials**, **Animations**, **File Format Variations**, **Collection Exporters** and export options.
- Supported method: export recognized materials, mesh data and supported animation through explicit scope/settings.
- Production adaptation: publish GLB/web assets separately from editable sources; validate animations and textures in the destination.
- Limits: curves require conversion; triangulation and UV/normal discontinuities can change counts. Arbitrary animated light/material/physics properties are ignored. Action merging changed with 4.4 slotted actions. Geometry Nodes instance export is experimental; viewer extension support varies. The text contains conflicting legacy/new action guidance, so use a version-specific export check rather than quoting one old naming rule as universal.

### S20 - RenderSettings

- URL: https://docs.blender.org/api/4.5/bpy.types.RenderSettings.html
- Publisher/date/version: Blender Python API; date unknown; 4.5. Evidence **D**.
- Inspected evidence: entries `filepath`, `film_transparent`, `fps`, `fps_base`, `resolution_x`, `resolution_y`, `resolution_percentage`.
- Supported method: address explicit scene-render properties rather than driving setup by fragile remembered UI locations. `filepath` supports blend-relative paths and frame-number padding.
- Production adaptation: a future automation contract records those fields alongside engine, version, frame range and output format.
- Limits: API property documentation does not validate a complete render script, active scene, compositor destinations, color transform or encoder compatibility. No Python code was executed.

### S21 - Fundamentals of Digital Lighting in Blender

- URL: https://www.cgcookie.com/courses/fundamentals-of-digital-lighting-in-blender
- Publisher/author: CG Cookie / Jonathan Lampel. Publication date unknown; exact course Blender version not established. Evidence **T**, course-description/curriculum text only.
- Inspected evidence: **What You'll Learn**, **Curriculum**, instructor identification. Lists realistic light values, exposure/scopes, HDRI/volumetrics, three-point lighting, key styles and separate Cycles/EEVEE topics.
- Supported method: the publisher explicitly teaches lighting roles and technical control together.
- Production adaptation: organize a reusable lighting recipe around purpose, source size/color and exposure before prescribing numbers.
- Limits: videos and downloadable resources were not viewed. Curriculum includes Filmic and older EEVEE shadow/probe terminology; do not transplant its engine-specific instructions to 4.5 without documentation checks. Promotional descriptions do not establish observed image quality.

### S22 - Story Tools

- URL: https://studio.blender.org/training/story-tools/
- Publisher: Blender Studio; individual course author and publication date not established in the extracted introduction. Evidence **T**, inspected overview text; lesson videos unviewed.
- Inspected evidence: introduction describes Grease Pencil, 3D environments, camera blocking and the Video Sequence Editor in one workflow.
- Supported method: combine 2D drawings over spatial layouts with sequence timing.
- Production adaptation: reusable hybrid storyboard/animatic scenes rather than isolated drawing files.
- Limits: no exact shortcut, installed tool version, shot execution or timing improvement was verified. The overview supports the workflow concept; detailed implementation must come from current docs or separately inspected lessons.

### S23 - Our Workflow with Blender and Godot

- URL: https://studio.blender.org/blog/our-workflow-with-blender-and-godot/
- Publisher/author/date: Blender Studio / Simon Thommes; **2025-07-11**. Evidence **T**, substantial article text inspected; embedded clips unviewed.
- Inspected evidence: **glTF as the Vessel**, **Collection Exports**, **Asset Separation**, **Workflow**, **Caveats and Lessons Learned**, **Get the code**.
- Supported method: explicit glTF publication, reusable collection export settings and separation of working files from destination assets. The production used custom export/import code for nested references and metadata.
- Production adaptation: adopt the source/published split and per-asset export scopes before adding custom pipeline machinery.
- Limits: author labels shared code a prototype, not a supported product. Reports central-index merge friction, duplicated IDs and material-import-order ambiguity. Those are lessons to avoid, not features to copy. Embedded assets showed login barriers; no code bundle was downloaded.

### S24 - Example - Tree Generator

- URL: https://studio.blender.org/training/geometry-nodes-from-scratch/example-tree-generator/
- Publisher/author: Blender Studio / Simon Thommes. Publication date unknown; page explicitly supplies **Blender 4.5 compatibility notes**. Evidence **T**, inspected author lesson notes; video and `.blend` file unviewed.
- Inspected evidence: compatibility notes identify the Curve to Mesh Scale input and Mesh Boolean Exact/Hole Tolerant settings.
- Supported method: update older procedural curve/boolean recipes using specific, source-owned migration notes.
- Production adaptation: branch/curve generators must expose profile scale explicitly and record Boolean assumptions instead of copying an old screenshot.
- Limits: the page's approximately 6:00 and 16:00 references are the author's locators, not timestamps independently observed here. Do not infer the full tree generator graph or claim its downloadable file was tested.

### S25 - Simulation Nodes in Blender 3.6 LTS

- URL: https://studio.blender.org/training/geometry-nodes-from-scratch/how-to-use-the-new-simulation-nodes-in-blender-36/
- Publisher/author: Blender Studio / Simon Thommes. Tutorial publication date unknown; **author reply dated 2025-08-29** inspected. Evidence **T**, author reply and lesson metadata only; video unviewed.
- Inspected evidence: Simon Thommes's reply distinguishes frame-rate-independent physics in seconds with Delta Time from frame-based choices; explains that simulation looping is difficult because frames depend on previous states.
- Supported method: initialize particle state deliberately and account for time between simulation steps; use designed lifecycle repetition where appropriate.
- Production adaptation: choose analytic loops when history is unnecessary; treat respawn/reset schemes as intentional design, not automatic physical recurrence.
- Limits: a viewer's claimed successful loop is not accepted as verified behavior. The author's example suggestion is not a universal loop construction. Use S07 for the 4.5 simulation contract.

## Access-limited and unviewed candidate

### C01 - Projecting Matte Paintings in 3D

- URL: https://studio.blender.org/blog/projection-matte-painting/
- Publisher/author/date: Blender Studio / Julien Kaspar; **2025-02-04**. Accessed 2026-11-03.
- Evidence **C**: actual page opened; title, author, date and short purpose statement inspected, followed by a login barrier. Article body and embedded video were not inspected.
- Potential use: first-party production examples for camera-projected matte paintings.
- Supported claim: the creator published an article on that subject. No detailed node setup, camera path, color-management method or demonstrated result is established here.
- Excluded from the 25 substantive-source count. No authentication bypass or download attempted.

The videos associated with S21, S22, S24 and S25 are likewise **unviewed**. Their inspected text is useful evidence at the stated level; it must not be relabeled as video observation by downstream skill authors.

## Authoring handoff and unresolved verification

The eight research findings ground the ten conditional recipes in [native Blender workflows](native-blender-workflows.md). Recipe fields:

1. Trigger and exclusions: the production need; analytic motion versus simulation; solve versus projection.
2. Required inputs: source assets/plate, camera, scale, engine/version, timing, destination and rights/provenance.
3. Editable controls: lighting roles/link sets, geometry parameters, phase/period, line styles, pass names and alpha convention.
4. Execution contract: source file, node/modifier dependencies, bake state, export scope and output naming.
5. Inspection contract: actual render or destination view, requested angles/frames, seam or edge checks and acceptance criteria.
6. Evidence and limitations: source IDs, exact version notes, what was tested and what remains documentary.

Do not create a new orchestrator, replace the spatial-verification owner, or promote documentation research into an executed render claim. This memo does not establish local Blender availability, performance, visual quality, actual alpha encoder behavior, export fidelity or successful video reconstruction.

Before shipping executable recipes, the parent should validate the selected version and actual surface: light-group reconstruction, line-art rebaking boundaries, state/cache invalidation, first/last-frame continuity, pass/alpha import, and glTF material/animation appearance in the chosen destination. These are explicit future implementation checks, not deferred research requirements: the present deliverable is the source-grounded method map.
