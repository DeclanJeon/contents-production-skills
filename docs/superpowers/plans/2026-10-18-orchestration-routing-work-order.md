# Work Order 3: Coordinator and Text-Worker Routing

**Design:** `docs/superpowers/specs/2026-10-18-camera-storyboard-blender-orchestration-design.md`
**Owner:** One OMO worker session
**Mode:** Documentation/skill-contract implementation only; no media or project execution.

## Goal

Make the coordinator's stage selection and specialist handoffs discoverable, non-looping, and consistent with the canonical routing table without duplicating domain rules.

## Owned files — edit only these

- `creative-production/SKILL.md`
- `orchestrating-video-preproduction/SKILL.md`

Do not edit `creative-production/references/production-routing.md` (Work Order 2 owns it), storyboard/camera specialist files (Work Orders 1 and 2 own them), `README.md`, `manifest.json`, other skills, QA/examples, installed copies, or production outputs.

## Required changes

1. State once that `creative-production` is the sole coordinator and state writer; it selects the narrowest current owner from `creative-production/references/production-routing.md`.
2. Keep `orchestrating-video-preproduction` text-only and limited to assigned planning stages. For a full package, it returns its assigned text artifacts and indexed missing-input packet; the coordinator resumes downstream specialist/media work.
3. Preserve single-artifact narrow routing, inherited IDs/versions/approvals, and the no-callback/no-second-interview/no-second-ledger boundary.
4. Make specialist selection conditional on the requested output and design §4: reference observation, numeric camera design, AI-control translation, Blender spatial verification, and actual camera QA are distinct owners/stages.
5. Require one indexed dependency packet when a specialist input is missing; coordinator assigns the owner once, integrates the return, and continues without a routing loop.
6. Keep planning/review acceptance, actual media execution/spend, and publication as separate gates. Do not imply automatic worker execution from a text instruction.
7. Reduce only contradictory/duplicated normative text in the two owned files; retain useful local handoff detail and link to the canonical routing file.

## Forbidden scope

- No changes to the routing map or camera/storyboard/Blender owner files.
- No new scheduler, skill, agent API, ledger, approval gate, test fixture for prose, provider call, media generation, README/manifest change, or commit.
- Do not normalize line endings or rewrite whole files. Preserve unrelated existing edits.

## Acceptance evidence

- Each request class resolves to one primary owner and only applicable specialists.
- Full text package and full image-backed package have a clear coordinator/worker boundary.
- A single missing technical input returns to the coordinator once and does not recurse.
- Single-artifact requests do not trigger a full package.
- Route links resolve and existing scope/authorization rules remain unchanged.

## Return

Report exact changed files, the simplified routing/handoff rule, checks actually run with observed results, and any needed coordination with the other workers. Message the coordinator before touching an unowned file.
