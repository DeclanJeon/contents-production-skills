---
name: open-3d-production
version: 1.0
description: "Delegated 3D craft for Blender modeling, lighting, staged exploded views and rendered web assets, plus Three.js scenes, scroll films, alpha cutouts, cursor rigs, browser QA and frame capture. The active orchestration owner selects modules and execution; this specialist returns only its assigned artifact. Spatial verification remains blender-previsualization."
---

# Open 3D Production

`creative-production` retains production orchestration: scope, current owner, module selection, sequencing, approvals and canonical project/history writes. This is a specialist, not another coordinator. For a standalone non-video Blender or web task, keep the active host/design owner and the requested artifact; do not activate video production merely to use these techniques. A delegated worker consumes its packet without another intake, coordinator callback or approval ledger.

## Assigned work

1. Read the assignment: Blender or browser target, exact output, source assets/dimensions, locked camera/IDs, selected modules, execution authority and destination. If the target is consequentially ambiguous, return that gap to the owner. A `.blend` deliverable requires Blender, not a Three.js scene or a recorded browser page.
2. Read [integration rules](references/integration.md) before any upstream guide. For Blender work also read [Blender adaptation](references/blender-adaptation.md). The orchestration owner chooses only the matching modules from the canonical [routing table](../creative-production/references/production-routing.md#open-3d-module-selection); consume that selection rather than starting the upstream Plan → Make → Check → Show pipeline.
3. Use the assigned guide and its adjacent scripts/assets only. Guide-relative `scripts/`, `assets/` and `references/` paths resolve from `references/upstream/skills/<module>/`, not this skill's root or the production output directory. Bare sibling names refer to those bundled module folders, not independently installed skills.
4. Check only the runtime needed for authorized execution. The upstream Python/JavaScript tools are real bundled tools, but not Blender add-ons. Work from copies in the assigned output root; use absolute input/output paths and a fresh output location, since several tools overwrite outputs. Keep source files and installed reference folders unchanged.
5. Return the actual artifacts and evidence to the owner: source versions, runtime/engine, exact commands/settings, inspected views/frames, limitations, and indexed missing inputs. Only the coordinator persists project state/history. Text-only work returns a plan without runtime probes, media generation or output folders.

## Completion

Blender work needs a reopenable `.blend` and the requested renders/exports, actual Blender version, engine/color settings and visual inspection of the assigned views/frames. Spatial verification uses the existing `blender-previsualization` acceptance contract, not a beauty frame as proof. Web work needs the requested page/assets and actual selected browser/state/viewport evidence. Browser frame capture proves encoded output timing, not real-time GPU throughput or Blender rendering.

Report missing runtimes, skipped surfaces and unsupported mappings as `BLOCKED`/`UNVERIFIED`; file existence, numeric similarity and a script exit code alone are not visual acceptance. Do not attach browser QA, a demo reel, regeneration, installation or publication unless assigned.
