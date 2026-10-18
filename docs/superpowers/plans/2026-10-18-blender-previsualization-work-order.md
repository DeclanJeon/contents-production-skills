# Work Order 2: Canonical Blender Previsualization Gate

**Design:** `docs/superpowers/specs/2026-10-18-camera-storyboard-blender-orchestration-design.md`
**Owner:** One OMO worker session
**Mode:** Documentation/skill-contract implementation only; do not run Blender.

## Goal

Align Blender trigger language and its evidence contract so ordinary storyboard camera planning is not over-routed, while scene-specific 3D feasibility work cannot claim completion without actual Blender inspection.

## Owned files — edit only these

- `camera-spatial-design/SKILL.md`
- `camera-spatial-design/references/spatial-contract.md`
- `blender-previsualization/SKILL.md`
- `creative-production/references/production-routing.md`

Do not edit the storyboard contract, other work orders, `README.md`, `manifest.json`, tests/scripts, installed copies, examples, QA artifacts, or production outputs.

## Required changes

1. Implement the three work classes and explicit Blender trigger from design §3. A camera field/move/storyboard alone must not trigger Blender.
2. Define “scene-specific 3D camera/spatial design” consistently as actual scene-specific 3D geometry/placement/feasibility design, including when camera path, blocking, occlusion, clearance, contact, or requested 3D delivery depends on geometry.
3. Keep text-only/read-only work non-executing. When Blender is required but absent, mark the dependent spatial deliverable `BLOCKED`/`UNVERIFIED`, continue independent work, and prohibit alternate-renderer substitution or FINAL claims.
4. Preserve Blender's current scope, schema ownership, actual version/mode recording, smoke-versus-full distinction, expected outputs, reopen/inspection requirement, and proxy limitations.
5. Keep `production-routing.md` the canonical routing table; link specialists to it rather than adding another route table.
6. Explicitly state that numeric/schema checks and smoke runs do not prove actual 3D scene feasibility or full requested visual inspection.

## Forbidden scope

- No change to `video-production-assets/references/storyboard-contract.md`; Work Order 1 owns that file and will align to the exact design wording.
- No new schema, alternate renderer, new skill, runtime install, Blender execution, tests requiring Blender, README/manifest changes, or commits.
- Do not normalize line endings or rewrite whole files. Preserve unrelated existing edits.

## Acceptance evidence

- Trigger wording agrees across the four owned files and with design §3.
- Ordinary narrative storyboard, 2D/flat graphics, numeric design-only work, and actual 3D feasibility are distinguishable.
- Required outputs and acceptance remain tied to requested shot/scene/panel IDs and actual inspection.
- Missing runtime and partial smoke behavior are truthful and scoped.
- Links resolve; no scene-specific 3D verification path loses its Blender requirement.

## Return

Report exact changed files, trigger wording, checks actually run with observed results, and any dependency on Work Order 1. If ambiguity cannot be resolved from design §3, message the coordinator before broadening scope.
