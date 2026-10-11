# Character Persona and Voice SSOT Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make character-sheet generation consume a behavior-based persona and, for speaking roles, a version-aware Voice Identity/Speech Style/Performance design.

**Architecture:** Add `designing-character-personas` as a text specialist, automatically read by the existing character-sheet owner. Preserve one coordinator and existing character_sheet/voice_profile artifact types; integrate the persona packet into the character SSOT, never maintain a competing bible. Keep typology conditional and real audio execution separately authorized.

**Tech Stack:** Markdown agent skills/templates, JSON manifest and instruction evals, existing Python installer/version checker, fresh-context model completions for behavior smokes.

**Spec:** `docs/superpowers/specs/2026-10-10-character-persona-voice-design.md`

## Global Constraints

- Preserve canonical sections 0–33, assigned IDs, `characters[].persona` four-string summary, project schema 1.1 and single-writer ownership.
- User-supplied/approved identity, behavior and voice win over typology proposals. Fictional-design gaps are labeled proposals; unsupported real-person facts remain undecided.
- Typology modes are `none | mbti | enneagram | both`; explicit supplied/requested modes win. New fictional full design may propose lenses within its delegated scope; no automatic typing of existing or real people.
- Voice design applies only to speaking roles and separates fixed identity, speech style and scene performance. Text planning never authorizes voice selection, audition, cloning or spend.
- No unrelated edits, runtime changes, commits or remote pushes. Keep this working checkout and existing user changes; sync only the selected Codex installation root with the existing package tool.
- Workers own disjoint files and skip tests/build/lint/formatters during edits. Parent runs integrated checks once changes settle.

## Review Focus

- Ordinary character-sheet request without an explicit persona/voice request: produce the persona/voice design, not merely mention an optional specialist.
- Same supplied MBTI/Enneagram for two fictional characters: distinguish personal motives, decisions, exceptions and speech without a type→face/pitch mapping.
- Silent or real-person roles: no invented narrator, personality type, biography or voice; respect supplied scope.
- Existing approved behavior/voice conflicting with a type proposal: preserve the supplied setting and name the gap without a silent substitution.
- Unsupported voice controls or stale SSOT inputs: return precise requirements/old pins, no fabricated application or selective invalidation beyond the real dependency graph.

---

## Task 1: Baseline and persona specialist

**Files:** Create `designing-character-personas/{SKILL.md,references/mbti-lens.md,references/enneagram-lens.md,references/expression-voice-bridge.md,references/sources.md,assets/persona-template.md,evals/evals.json}`. Record comparison evidence under `qa/`.

**Interfaces:** Consumes the existing brief/synopsis, character IDs, approved facts and optional typology mode/voice notes. Returns provenance, persona_core, typology_lens, behavior_rules, expression_bridge, voice_identity/speech_style/performance, validation and unresolved requirements. Content slots are text-packet fields, not new canonical project JSON fields.

- [x] Run five fresh-context current-skill applications before editing. Identify a concrete missing required output rather than assuming a regression.
- [x] Implement the narrow text skill and on-demand references, one reusable persona/voice template, and realistic evaluation prompts. Reuse researched primary links and distinguish theory from empirical evidence and creative design.
- [x] Include one fictional worked example with neutral/pressure/trust states and preserved voice identity; type labels are not voice prompts.
- [x] Later run the same requests using the new skill and compare actual outputs, plus real-person/silent/approved-voice/stale-input/unsupported-control scenarios.

## Task 2: Character SSOT and voice handoff

**Files:** Modify `designing-video-character-sheets/SKILL.md`, its `references/character-craft.md` and `references/character-ssot-master-prompt.md`; `video-production-assets/assets/character-ssot-template.md`, `references/22-dialogue-lipsync.md`, `assets/performance-cue-template.md`.

**Interfaces:** Read the persona specialist's documented packet; map it into existing SSOT sections and `voice_profile`. Preserve `voice_artifact_id`, `performance`, existing dependency/approval states and no-generation scope.

- [x] Require the persona specialist whenever drafting/deepening a character sheet; if an existing sheet is complete, reuse and check its applicable content rather than redesigning it.
- [x] Expand §12 into Voice Identity, Speech Style, Persona-to-Voice, State Variations, reusable direction and realization reference. Map core/lenses/rules into §13–20 and expression bridge into §10–11.
- [x] Keep rules authoritative in the specialist/master reference; template carries structural output slots. Extend allowed-state/anti-drift/lock summary and cast comparison to voice.
- [x] Update voice execution handoff to consume current persona/voice design and supported controls; keep actual voice selection/listening/rights gates unchanged.

## Task 3: Routing, registration and user installation

**Files:** Modify `manifest.json`, `creative-production/references/production-routing.md`, `orchestrating-video-preproduction/{SKILL.md,references/stage-execution.md}`, `integrations/skill-routing.md`, `README.md`, `USAGE_GUIDE.md`, `CHANGELOG.md`; version only affected skill headers where their package content changed.

- [x] Register the new specialist and direct persona request route; retain character sheets as owner of the integrated SSOT and no second coordinator.
- [x] Advance package 2.4→2.5, character-sheet 2.5→2.6, preproduction 2.5→2.6, creative-production and video-production-assets 1.0→1.1; new specialist starts at 1.0. Preserve unrelated unreleased entries.
- [x] Document when automatic persona/voice design applies, conditional type use, reuse of supplied identities and no automatic audio generation.
- [x] Run `python scripts/check_versions.py` and `python -X utf8 -m pytest -q` after all edits settle. Do not rerun the known default cp949 invocation.
- [x] Exercise real fresh package installation in a temporary root and inspect installed references/template access. Run `python scripts/sync_installed.py --root C:/Users/Declan/.codex/skills` after verification, then confirm source/installed paths and new skill visibility.
- [x] Obtain independent contract review and fix actionable issues. Record model-output evidence and limits; do not claim image/audio quality or human acceptance.

## Verification evidence and limits

- Version check: package 2.5, 23 skills. UTF-8 suite: 258 tests and 217 subtests passed; two existing Windows subprocess decoding warnings.
- Fresh isolated installation and final Codex synchronization were both executed. Final local install created one new link and repointed 22; all 34 checked skill/resource hashes match source. The installed new `SKILL.md` is readable. The current process's `skill://` list is cached and did not rediscover it; restart/refresh is still required for name-based discovery in a new session.
- Text proof: canonical headings 0–33 in order, ordinary automatic persona/voice, ten persona cases and separate MBTI-only/standalone-dialogue/version-pinned voice cases. Compact final comparisons went through measured length and semantic checks; first drafts were not universally compliant. Keep intermediate failures as evidence, not a passing benchmark.
- Independent reviewers closed the MBTI-only rationale/limits and standalone dialogue overreach findings. Later text smokes exercised cue completeness, silent vocal N/A, existing reference retention, and authored rule/sample consistency.
- Evidence: [static review](../../../qa/character-persona-voice-review.html), [final compact outputs](../../../qa/character-persona-voice-final-compact.json), [grading](../../../qa/character-persona-voice-final-grading.json), [local installation](../../../qa/character-persona-voice-local-installation.json).
- No provider execution, audio listening/selection/cloning, image-quality or human acceptance proof; no commit, push or published release.
