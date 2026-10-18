# Camera-Specific Storyboards, Blender Gates, and Orchestration

**Status:** Approved execution design for this workstream.
**Scope:** Existing `contents-production-skills` instructions only. This document defines how three bounded workers will update the existing camera/storyboard and coordinator contracts.
**Authority:** Existing project/user approvals, `project.json`, storyboard contract, camera-space contract, and provider/runtime gates remain authoritative. This design adds no runtime permission.

## 1. Decision summary

The skill set already covers the core camera-planning vocabulary and specialist handoffs. The durable gap is proof of scene-specific intent: each shot has a camera field and rationale, but the board does not require a scene-level camera treatment or compare that treatment with adjacent scenes. Add that comparison without demanding arbitrary visual novelty.

Standardize Blender use around **3D spatial verification**, not the mere presence of a camera field or a storyboard. Keep `creative-production` as the sole project coordinator and `orchestrating-video-preproduction` as a text-only worker. The coordinator selects specialists from the canonical routing map, assigns one scoped output at a time, and resumes after indexed dependency packets return.

## 2. Scene-specific camera design

### 2.1 Design unit and decision order

Design from scene intent down to shots; do not choose a move first and invent a reason afterward.

1. Resolve the scene's dramatic/informational purpose, audience knowledge at entry and exit, emotional change, blocking, and constraints.
2. State the scene's camera treatment: audience POV, screen/action axis, framing or scale progression, composition/focal hierarchy, and whether the camera is static or moves.
3. For every shot, select the view and camera behavior that serves its assigned beat, reveal, reaction, contact, or hold. Record the start/end framing and the action/reveal timing when movement matters.
4. Compare the treatment with the preceding and following scenes. State the intended contrast, continuity, or deliberate reuse and why it serves the story.
5. Review the ordered board for coverage, screen direction, axis, reveal timing, readable action, and continuity. Keep alternatives selective: compare them when a consequential choice remains unresolved, not for every shot by default.

### 2.2 Required scene-camera intent record

For a complete production storyboard, provide one row per scene, linked to existing `scene_id` and shot IDs. Use the existing board/project artifacts; do not create a second ledger or a new required `project.json` schema.

| Field | Required decision |
|---|---|
| Scene purpose | Story, information, or emotional change the scene must deliver |
| Entry → exit knowledge/state | What the audience and visible subjects know or feel before and after |
| POV and axis | Audience viewpoint, subject/action axis, and any planned reorientation |
| Camera grammar | Framing/scale progression, focal hierarchy, composition, and static/moving choice |
| Motivated move | For a move: what triggers it, what it reveals/follows, shot-local timing, and settle/cut; otherwise why static is stronger |
| Adjacent-scene relation | Intended change from/to neighboring scene treatments, or continuity reason |
| Reuse rationale | Required only when a setup/treatment is intentionally repeated across scenes |
| Status/evidence | Planned, inspected, or unverified; link actual visual evidence only when it exists |

The board's existing per-shot camera/spatial slots remain required. The scene row summarizes and compares intent; it never replaces shot IDs, local camera/action timing, numeric spatial specs when applicable, or actual image/previs QA.

### 2.3 Uniqueness means motivated distinction, not forced novelty

- Do **not** require every scene to have a numerically different lens, angle, or move.
- Do require a stated, scene-specific reason for each treatment and an explicit relation to adjacent scenes.
- Reuse is valid when it preserves an intentional axis, visual motif, POV, rhythm, or contrast. Record that purpose; do not let reuse pass merely because the values are populated.
- Detect generic duplication through review of purpose, knowledge change, POV, framing progression, and move rationale—not a numeric uniqueness score or an arbitrary move quota.
- Static shots remain first-class choices. A move that is decorative or weakens legibility should be removed or motivated.
- A consequential unresolved choice may receive a small number of alternatives. A locked direction is reused, not reopened.

### 2.4 Acceptance

A production board is scene-camera complete when:

1. Every scene has an intent row and links to the shots it governs.
2. Every shot has a camera choice that serves its beat/scene and satisfies the existing technical slots or has a reasoned N/A/deferred/blocker status.
3. Every adjacent-scene transition has an intentional contrast/continuity decision; intentional repeated treatments have a reason.
4. Axis, screen direction, reveal/contact timing, and required action readability are checked against the ordered board.
5. Unverified image or 3D claims remain unverified; a populated field or validator pass is not creative or visual evidence.

No new machine-readable schema or prose-pinning test is justified for this instruction update. Existing validators retain their structural remit; visual/meaning review stays human and evidence-scoped.

## 3. Blender decision gate

### 3.1 Three work classes

| Class | Example | Required route |
|---|---|---|
| Narrative camera planning | POV, shot size, composition, motivated pan/push/static choice in a text or ordinary 2D storyboard | `storyboarding-video` / `06-shots`; no Blender invocation |
| Numeric camera design without a geometry-verification deliverable | Proposed lens, coordinates, or path as a design artifact, with no requested 3D scene feasibility claim | `camera-spatial-design`; numeric/schema analysis as applicable; label unrendered geometry `UNVERIFIED`; Blender only if a trigger below applies |
| Scene-specific 3D spatial verification/previs | Actual 3D blocking, camera path/clearance, occlusion, contact/visibility feasibility, explicit Blender/previs request, or a delivery that claims the 3D arrangement was checked | `camera-spatial-design` owns the spec; `blender-previsualization` is mandatory for implementation and visual inspection |

**Blender trigger:** explicit Blender/previs request, or the requested result depends on validating an actual scene-specific 3D arrangement (camera path, geometry, blocking, occlusion, clearance, or contact), or a 3D-verified result is part of the requested deliverable. A camera field, camera move, storyboard, or scene ID alone is not a Blender trigger.

The canonical meaning of “scene-specific 3D camera/spatial design” is the third row. A storyboard's numeric/N/A branch is consistent with this gate: simple graphics and narrative-only planning do not become 3D tasks just because they contain camera descriptions.

### 3.2 Execution boundary and evidence

- Text-only/read-only work may design a later previs, but must not execute Blender. Mark the unperformed 3D check `PLANNED`/`UNVERIFIED` or `BLOCKED` according to the existing contract.
- If Blender is required but unavailable, continue independent text work, return the exact missing evidence/runtime, and block only dependent 3D completion. Do not substitute another renderer or claim FINAL.
- A smoke render is a pipeline preflight only. It does not satisfy full-scene, all-requested-frame, contact, or final visual inspection.
- For a completed requested previs, preserve the existing camera spec/version and shot/scene/panel IDs; record actual Blender version and mode; produce the requested `.blend`, frames, numerical analysis, inspection and manifest artifacts; reopen the requested outputs and inspect the relevant frames.
- Bounding-box, center-point, ray-cast, or schema checks are proxies. They do not prove full articulated visibility, hand/object contact, performance, aesthetics, or final generated-video quality. Keep such claims `UNVERIFIED` unless the required actual evidence is inspected.

## 4. Orchestration and specialist ownership

`creative-production` remains the sole coordinator and state writer. `orchestrating-video-preproduction` handles only assigned text planning; it never invokes media/runtime tools or creates a rival ledger. Single-artifact requests stay narrow.

| User request/current deliverable | Owner route |
|---|---|
| One ordinary or complete storyboard | `storyboarding-video` and the canonical storyboard contract |
| Multi-artifact text planning | `creative-production` assigns requested stages to `orchestrating-video-preproduction`, which invokes only matching text specialists |
| Camera movement observed in supplied reference media | `camera-motion-reference-analysis` |
| Camera design from a scene/brief, especially numeric spatial path | `camera-spatial-design` |
| Convert an approved camera design to AI video controls | `ai-camera-control` |
| Triggered 3D scene feasibility or explicit previs | `camera-spatial-design` → `blender-previsualization` |
| Actual generated-camera movement/lens/reveal QA | Existing `video-production-assets` camera-motion QA reference |

### Handoff protocol

1. The coordinator resolves the requested scope and current stage once, selects the narrowest owner, and sends the required brief, IDs/versions, constraints, and acceptance checks.
2. A worker returns only its assigned artifact/proposal, observed evidence, actual checks, and indexed missing inputs. It does not reroute itself, ask a second interview, edit canonical state, or reopen approval.
3. Missing specialist inputs return as one indexed requirement packet to the coordinator. The coordinator assigns the named specialist and resumes integration after the packet returns.
4. The coordinator alone integrates outputs, reconciles versions, persists authorized state, performs cross-artifact QA, and chooses the next stage.
5. The coordinator stops at the requested deliverable. Review acceptance, media execution/spend authorization, and publication remain separate.

Keep the decision table canonical in `creative-production/references/production-routing.md`; specialist documents should state their owner boundary and link to the canonical route rather than reproduce a competing routing table.

## 5. Worktree protection and work decomposition

This checkout contains pre-existing changes. The README has substantive user changes and is excluded from all worker write scopes; do not touch `README.md`, `manifest.json`, unrelated QA/examples, other skills, installed copies, or user production directories. Several assigned skill files currently show tracked line-ending-only diffs; preserve their existing encoding/line endings and avoid whole-file rewrites. Work orders own disjoint file sets and use this design as their acceptance contract.

Three independent work orders implement the design:

1. Storyboard scene-camera intent and comparative acceptance.
2. One canonical Blender trigger, outputs, and verification boundary.
3. Coordinator/text-worker routing and non-looping handoff.

The main session owns integration review, cross-document consistency, local links and relevant non-destructive verification. No commit is authorized.

## 6. Evidence limits

This design governs written routing and output contracts. It does not claim every model invocation will obey them. Existing Flucto craft directories are analysis-run bundles, not actual storyboard/Blender executions; they cannot prove camera-treatments are scene-specific. Behavioral verification requires future observed storyboard outputs and, where the trigger applies, opened Blender outputs tied to actual shot/panel IDs.
