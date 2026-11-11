# Architecture reference: actual native Blender execution

## Result

An actual 30-second native Blender reconstruction was produced from 신비한 건축사전 source `35lHzyVx_qM`, interval 207–237 seconds, retrieved with Flucto CLI 1.19.0. Exact-reference fidelity **did not pass**. This execution establishes usable native authoring/rendering, not identical replication.

External production root: `/home/declan/Documents/studio_production/architecture-reference-2026-11-03`.

Authoritative delivery details and remaining discrepancies: `DELIVERY.md` in that root. Actual outputs: `delivery-v002/architecture-reproduction-30s.mp4`, `delivery-v002/reference-comparison-30s.mp4`, and `authoring/architecture_native_v003.blend`.

## Skill-to-execution evidence

The native worker used open-3d-production's native workflow and reproduction guidance, source-detail sheets and the parent's shot brief. The parent corrected geometry, deformation, camera evaluation and final editing, and inspected the output. One worker authored the scene; this was not a multi-agent team validation.

The exercised technique is native bpy meshes, materials, shape keys, F-curves and cameras. It is not a verified Geometry Nodes graph or fluid/acoustic simulation. The scene has 843 editable objects and no source-image texture nodes.

Blender 5.2.2 LTS executed the scripts. Runtime API probes resolved engine/compositor differences. Embedded Python lacked the host's Pydantic, so render job validation used standard-library dataclasses. Host LSP cannot resolve Blender's embedded bpy/mathutils; real Blender execution, rather than a suppressed diagnostic, verified those imports.

Commands and provenance are retained in the external scripts and production events. Full native rendering completed 900 frames in 2854.864 seconds. The corrected close-up rendered 149 frames in 470.797 seconds. Explicit versioned edit provenance combines those runs rather than pretending a changed scene can reuse another scene's cache.

## Observed corrections and checks

The parent inspected native previews, three actual geometry camera views and all nine final contact sheets (25 paired source/output times). Corrections removed intersecting floor/cushion geometry, shared their deformation field, corrected actual-camera selection and moved the compression peak to the observed source timing.

All delivered videos passed 900-frame, 30-fps, 30-second and full-decode checks. Audio is borrowed original audio, not a newly generated performance. Continuous playback and listening were not performed.

Remaining failures include construction cut timing, missing complete-system cutaway/arrows, differing wave trajectories/camera, material detail and some subtitle transitions. These prevent an identical-remake acceptance. The comparison is the review artifact, not a similarity percentage.

## Package improvements

Native Blender authority now overrides overlapping browser recipes for native deliverables. Reproduction guidance requires an acquired source, locked interval, actual previews, contact deformation checks, runtime-specific API verification, immutable render fingerprints, explicit borrowed-media ownership and an honest discrepancy verdict. B03 allows illustrative bpy deformation without falsely claiming Geometry Nodes execution.

This case validates only the exercised workflow. No blanket claim is made for all ten native recipes or unrelated exports.

Final repository checks passed: version consistency (package 2.33, 22 skills), pytest (400 tests and 518 subtests, 43.98 seconds), installed-link dry run, and `git diff --check`. The external project passed the plan contract validator. The QA JSON parsed successfully; JSON LSP was unavailable because Biome is not installed. No dependency was added solely for prose/JSON evidence.
