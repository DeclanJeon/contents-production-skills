# Changelog

## Unreleased

## 2.3 2026-10-04

- Default an unqualified storyboard request to a complete production plan; keep explicitly rough narrative panels narrow and preserve text-only/media/spend boundaries.
- Add one shared storyboard contract linking approved synopsis/source beats, scenes, shots, characters, camera/space/Blender, VFX, dialogue/voice/lipsync, sound cues and every required panel. Return integrated specifications, exact image/sheet counts and versioned handoffs.
- Require actual clean-image chronological review against the approved story before completion; administrative labels and audio cannot hide missing causal, ownership or emotional transitions. Structural validation and model text are not visual approval.
- Add indexed KEEP/FIX/unverified repair with preserved normal cuts, prerequisites, grounded time estimates and reinspection. Extend source/character/voice intake, synopsis QA, technical preproduction and first/peak/end-frame handoffs in existing owners.
- Add `validate_storyboard.py` for optional detailed-board coverage/references/timing and `split_storyboard.py` for preflighted indexed PNG extraction with ID/hash provenance. Reject missing beats/panels, invalid audio/speech links, unsafe paths/crops, duplicate file IDs and overwrite; preserve existing project schema and validation profiles.
- Add design/work-order documents, usage/routes, behavior scenarios and QA evidence. Verification: 86 tests and 136 subtests pass; existing Windows junction tests emit two decoding warnings. Actual valid/invalid validator CLI and five-cut synthetic PNG/JPEG extraction smokes pass. No rendered-artwork, Blender or provider execution validation is claimed.

## 2.2 2026-10-04

- Align the text-planning lane with a 15-step agent production flow: add an Emotion field to the shared spine, an emotion checkpoint after topic selection, and an optional link to the concept/emotion/retention deepening before the synopsis locks.
- Add a Voice profile section to character sheets with a three-route procurement table (user-supplied recording, synthesis, closest available match), demographic-label rules for voice, and handoff to the dialogue/lipsync voice selection procedure.
- Require a total-estimate summary (N × current unit price) in paid-path approval requests under production execution §1, bound to the approved count; generation planning §6 stops submission when that summary is missing or stale.
- Document the post-completion chain (generation QA/retry → edit/captions → finishing/platform → distribution metadata) as step D of the usage guide, placing title/keyword/thumbnail design after the content is finalized rather than at the start.
- Add the 15-step flow-alignment implementation plan under docs/superpowers/plans.

## 2.1 2026-10-04

- Add selective reference discovery/selection, evidence-scoped five-axis analysis and traceable mechanism-to-production handoffs without copied protected expression or fabricated project state.
- Add fit-first video topic/synopsis discovery checkpoints with scoped five-option defaults, explicit-count overrides and supplied/locked-input skips; preserve text-only and media approval boundaries.
- Add project-local style brief fields, qualitative reference-intent QA and requested retrospectives; exclude autonomous skill/profile improvement and numeric similarity pass/retry gates.
- Extend creative-production behavior cases for discovery, reference selection, style handoff, qualitative QA/retrospective and locked single-prompt scope.

- Default content/review image generation to Codex Imagen; exclude Higgsfield image submissions and fallback. Missing helper/auth/usage readiness blocks that image step without expanding text-only work or changing video/audio routing.
- Add a minimum-sufficient preview-to-final workflow with approved version/count/cost caps, output inspection, promotion choices and separate-or-combined version-bound authorization.
- Connect provider-neutral job reconciliation and targeted edits; unknown async status is checked before any retry to avoid duplicate submission.
- Add SFX-only/music-exclusion, voice selection/listening, measured translated-caption timing and source-level music/effects rights procedures without fixed vendor or audio-mode enums.
- Make creative candidate counts responsive to the brief and tighten unsupported product-benefit/offer-causality claims.

- Extend reference-video analysis into a measured/estimated beat map of subject and camera motion, edit transitions, product/action peaks and audio sync anchors.
- Make edit and sound-cue templates executable as timeline handoffs, including source ranges, gain/fades, sync offsets, source-rights status and review scope.
- Add sequence-level dynamic-edit QA; distinguish full playback/listening from sparse frame and waveform checks, and prohibit treating cut speed/effects as observed motion.
- Add creative-production behavior cases for mixed-reference audio, static source clips and incomplete sequence audition.
- Require media-backed edit timing; without source access, return beat order instead of fabricated cut points, IDs or executable JSON.
- Require QA findings to distinguish direct inspection, user-supplied observations, tool output and inference.
- Add read-only archive-wide video audits with per-file evidence coverage and a dedicated comparison template; add per-episode/monthly feasibility checks for dialogue-heavy AI series that separate measured workload from assumptions and unknowns.

## 2.0 — 2026-10-02

- Rename the project and GitHub repository to `contents-production-skills`; retain eight installable skill IDs and `creative-production` as the only content/video coordinator.
- Integrate active generic marketing/source adaptation, video prompt composition, shot decomposition, model-routing and hybrid-pipeline planning as selective coordinator references. Replace stale per-model capability tables and unverified corpus statistics with provider-independent patterns and live endpoint verification.
- Consolidate all 28 supplied memorable-video v6 skills into existing production owners: 10 on-demand deep-dive references and 10 reusable templates for concept/emotion/retention, genre/comedy, series, brand/product, visual identity/SSOT/crowd, physics/VFX/QA/retry, dialogue/lipsync, sound/finishing/platform, execution and reference analysis.
- Retire the nested v6 installation, old archive and duplicated usage guide. Merge global state/budget/asset/attempt semantics into canonical project.json; preserve supplied identities, version dependencies and separate review/execution-spend/publication approvals.
- Keep actual image/audio/video/assembly/publishing executors conditional. Add explicit selected image-craft and runtime dependency lanes without vendoring auth, private server paths, model weights, book/Notion material or provider helpers.
- Extend schema 1.1 with optional asset provenance, generation_attempts and shot.retry_budget. Fix retry counting (zero retries permits the initial attempt), malformed attempt-reference crashes and accepted attempts referencing only planned results. New regression cases observed failing before their fixes.
- Fix locale-dependent JSON decoding in production and spatial CLIs; use UTF-8 for projection/Blender JSON boundaries. Remove Blender's duplicate spatial implementation, contract, source bibliography and fixture; use the canonical camera-spatial-design resources from the same installed skill root.
- Verification: 21 installer, 15 production-contract and 7 spatial regression tests pass. Actual disposable install/collision/backup/alias-migration CLIs, educational/animation plans, spatial/product calculations, numerical projection and zero-retry boundary CLIs exercised. Blender adapter import/help exercised; bpy runtime unavailable, so no Blender render is claimed. Text-behavior evaluation and rename evidence are recorded separately in qa/consolidation-validation.json.

## 1.3 — 2026-10-02

- Package `creative-production` as the single content/video coordinator alongside the three existing production/camera/Blender specialists and four text-planning skills: eight core skills total.
- Make locked text drafting and text-only planning independent of provider accounts, GPUs, Blender and particular agent frameworks. Preserve inherited briefs/checkpoints, requested artifact scope and separate review, execution/spend and publication authorization.
- Add complete planning resources, host discovery metadata and synthetic behavior evals. Exclude newly imported book-summary/Notion references; preserve existing source and reuse limitations without granting a new license.
- Extend the one package manifest with the entry skill, support host and conditional external dependencies. No external skills, auth setup, models or tools are installed automatically.
- Add `scripts/install_package.py`: complete source/support/collision preflight, refusal to overwrite/merge by default, explicit backed-up replacement and optional second-root duplicate migration. Unrelated skills remain outside managed scope. Partial I/O failures report affected destinations and retained backups; installation is not atomic.
- Keep existing production schema 1.1 and camera-spatial-1.0 contracts and validators unchanged.
- Verification: 21 installer tests, 8 production-contract tests and 6 spatial tests pass; actual fresh-install, collision, backup-upgrade and alias-migration CLI smokes; installed resource checks; educational/spatial validator smokes; 13 core-only model artifact/action probes. The latter are not tool-enabled provider/media or platform execution tests. Repository QA retains the detailed verification record.
