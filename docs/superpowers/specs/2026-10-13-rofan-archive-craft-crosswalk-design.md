# Archive-wide transferable craft crosswalk design

## Status and purpose

**Status:** Implementation is complete; one fresh V4 known-model skill-output call passes the bounded acceptance (`openai-codex/gpt-6-luna`; [raw response and grade](../../../qa/rofan-archive-crosswalk-known-model-v4-results.md)). Earlier non-pass/incomplete outcomes remain preserved without regrading: the initial five-call smoke, follow-up v1/v2, and known-model v1/v2/v3 (see the [test-plan history](../../implementation/2026-10-12-rofan-craft-skill-test-plan.md) and linked result artifacts). The separate baker baseline/with-skill comparison is [one descriptive sample per arm](../../../qa/rofan-unrelated-brief-baseline-with-skill.md), not causal or statistical evidence.

This record defines a bounded way to transfer reusable, source-derived filmmaking craft into existing video-production owner procedures. It is based on source-ledger evidence, not a claim that all 44 videos were decoded or watched. It does not authorize copying story, characters, props, wardrobe, specific shot sequence, or original timings.

## Problem and decision

The repository already contains owner procedures for shot/reaction/information order (04/06/09), action phases/foot support/contact/settling (06/08/21), image-plane versus physical camera cause (camera-motion-reference-analysis, 27, 25), and look/light/props/graphics (05/07/20). Existing bounded owner additions P14 and L03 remain. Do not restate these as new universal rules.

The actual gap is an archive-wide relational retrieval and transfer chain: source occurrence → source-local sequence/scene → shot/boundaries → within-shot event → craft finding → existing owner → target-specific QA. `archive-audit-template.md` owns inventory/coverage; `shot-dna-template.md` owns per-shot notes. Neither represents this archive-wide join, and procedure 25 calls for audit and shot DNA without requiring the join in exhaustive mode.

**Decision:** Add an optional `video-production-assets/assets/archive-craft-crosswalk-template.md`; link it from `archive-audit-template.md`; require it only for an explicit exhaustive all-source/all-shot or cross-source craft extraction in reference module 25. Keep regular/single-reference analysis light. Do not change `project.json` or production schemas, make the casebank mandatory, or copy source narrative into rules.

## Files and responsibilities

| File | Proposed change | Responsibility |
|---|---|---|
| `video-production-assets/assets/archive-craft-crosswalk-template.md` | Add | Relational evidence and transfer record, including explicit missing rows/gates. |
| `video-production-assets/assets/archive-audit-template.md` | Link to new template | Existing source inventory and coverage; no duplicate crosswalk. |
| `video-production-assets/references/25-reference-video-analysis.md` | Add exhaustive-mode conditional requirement | Trigger and use the crosswalk only when scope is exhaustive all-source/all-shot or cross-source craft extraction. |
| `video-production-assets/assets/shot-dna-template.md` | No change | Continues to own per-shot notes. |
| `video-production-assets/references/rofan-craft-examples.md` and owner files | No change in this design | Optional provenance and existing owner knowledge; no casebank requirement or duplicate craft rules. |
| `project.json`, production schemas | No change | No schema or production-payload expansion. |

## Crosswalk contract

The template is an archive-level relational join, not another inventory or shot-DNA form. Retain one source occurrence per row/group and preserve identifiers verbatim. Required links and fields:

1. **Source occurrence:** stable `source_position_id`, separately preserved SHA (algorithm/value) and `archive_id`, exact filename, and source status. Occurrence identity is not an independent creator/case identity.
2. **Source-local structure:** sequence/scene IDs and membership bounds, with evidence and explicit unknowns.
3. **Shot and boundaries:** shot ID; source PTS and timebase; start and end-exclusive values; boundary evidence and status. Distinguish detector candidate, confirmed hard cut, soft transition, and shot boundary; do not collapse these labels.
4. **Within-shot event:** event ID/type, source PTS/timebase, locator/evidence, and relation to shot. Do not treat overlays, blur, or within-shot events as cuts absent boundary evidence.
5. **Craft finding:** directly observed evidence plus exact locator; `[INFERENCE]` function with at least one alternative; story-neutral mechanism; transfer conditions and avoid conditions; existing owner procedure; target-specific, observable QA acceptance.
6. **Completeness gates:** explicit source rows not materialized, unresolved joins, missing evidence, and open global gates. Missing source rows/gates must be stated; never report zero findings as a proxy for missing coverage.

The chain must be traceable in both directions: each craft finding points to evidence/locator and the relevant source/scene/shot/event records; each record can be joined without relying on narrative paraphrase or ambiguous aliases.

## Owner-routing matrix

| Finding domain | Existing owner route | Design rule |
|---|---|---|
| Shot/reaction/information order | 04 / 06 / 09 | Reuse existing procedure; only transfer a demonstrated missing, generic QA or decision step. |
| Action phases, foot support, contact, settling | 06 / 08 / 21 | No universal gait or contact claim from sparse strips; route bounded evidence to existing action owner. |
| Camera image-plane change versus physical camera cause | camera-motion-reference-analysis / 27 / 25 | Describe observable frame change separately from inferred camera cause; include alternatives. |
| Look, lighting, props, graphics | 05 / 07 / 20 | Do not transfer source-specific assets or narrative; route only generic, evidence-backed mechanism/QA. |
| Existing additions | P14 in 04; L03 in 07 | Preserve; do not duplicate or broaden beyond their bounded evidence. |

## Scope gates

- **Exhaustive all-source/all-shot or cross-source craft extraction:** module 25 MUST use the archive audit and crosswalk; state requested and actual coverage, unresolved rows, and gates. “Exhaustive” is a requested scope label, not evidence of completion.
- **Regular or single-reference analysis:** use existing audit/shot-DNA paths as appropriate; crosswalk is not required and casebank lookup is not forced.
- **Owner transfer:** only when explicitly requested; require a traceable finding, generic mechanism, existing owner, conditions/avoidance, and target-specific QA. Existing rules are not recopied as new craft.
- **Incomplete evidence:** retain unknowns and incomplete status. No inference from absent rows, candidate counts, or saved examples to archive-wide prevalence or full source behavior.

## Evidence snapshot and open gates

Evidence below was directly checked in F: root and the current source ledgers; the baseline runner also read manifests/ledgers. Neither baseline nor this design work performed original-video playback/full decode. The snapshot is not a claim that all 44 videos were decoded or watched.

- **Inventory:** 44 MP4 occurrences; manifest 50 URLs, 44 downloads, six YouTube HTTP 403s; 7,095,987,672 bytes (about 7.095 GB) and 33,419.9 seconds. Occurrences are not independent creators.
- **Dense strip extraction:** `dense-review/progress.json` records 44/44 files, 335/335 intervals, and zero extraction failures. Each interval is 1.2 seconds sampled at 5 fps (six frames). `manual_review.json` says these are around only the first eight retained locator PTS per source; full-video coverage is false. Extraction is not itself human review or continuous playback and cannot prove full-rate gait or camera cause.
- **Separate mechanical full-source run:** `full_archive_summary.json` reports 44 expected/observed/unique source identities, one complete and 43 failed, and false full-source PTS coverage. The separate scene scan found 6,002 detector candidates and retained only the first eight locator PTS/source; none are boundary-certified, and no motion is inferred. This is distinct from the 335 dense strips.
- **Persisted process state:** `full-archive/progress.json` still says running at 6/44, file_07, and `run.lock` lists PID 17736. Prior process/service inspection found no matching active process; treat these as stale persisted state, not active work.
- **Current semantic master:** 44 source status rows; 34/44 materialized (24 complete source ingests, one bounded augmentation, six partial actual, two craft-only partial, one endpoint-only); ten unmaterialized. `source_occurrence_count=30` conflicts with the 44 rows/34 materialized. The current index says 44/44 occurrence identities align, which is not closure.
- **Global semantic-index gates:** `complete_scene_shot_event_crosswalk` OPEN; `all_visual_shot_content_checked_against_native_images` OPEN; `all_candidate_free transitions_and_first_last_images` OPEN; `all_source_scene_membership_bounds` OPEN; `occurrence_vs_independent_cases` OPEN. `creator_intent` remains inference; `camera_and_gait` remains unverified absent those modalities.
- **Selected EA6A source ledger:** 468 shots, 44 scenes, 39 events, 650 candidate dispositions; the master status is `visual_semantic_craft_closed`. Its 0.2-second dense sampling is not full-rate playback. Audio processing is machine inference only; `human_listened=false`. This selected-source closure does not close archive-global gates.
- **Version/snapshot conflicts:** partition manifest is file/status v5 while its embedded schema label says v4. Current in-progress master/catalog report 34/44; older design header reports 31/44 and `archive-normalized-actual-master-v1.json` reports 23/44. Preserve these as stale snapshots; do not reconcile silently. The catalog is provisional, and some JSON metadata retains old C: paths although current F: root resolves them.
- **Owner coverage:** general craft language described above already exists; P14 and L03 remain. The material gap is relational archive retrieval and the evidence→mechanism→owner→QA chain, not invention of universal camera/gait rules.
- **Baseline:** five fresh stateless calls on the exhaustive all-44 request produced no joinable source-occurrence→sequence/scene→shot→within-shot-event crosswalk and no operational evidence-locator→mechanism→owner→QA path (0/5). All five distinguished detector candidates from confirmed cuts and acknowledged incomplete sources, no audio listening, and no full-motion playback (5/5). The runner used manifests/ledgers but did not open original video media; available dense extraction was 335/335 intervals, not all-shot source review. Requested model `default`, resolved identity UNKNOWN. This is a bounded behavioral sample, not a statistical estimate.

## Transfer and anti-copy rules

Transfer only a source-grounded, story-neutral production mechanism, separated from what was observed and what is inferred. Every finding must retain locator, evidence, alternative explanation, applicability and avoid conditions, existing owner, and target-specific QA. Do not transplant plot, characters, relationships, locations/sets, props, wardrobe, distinctive design, choreography, exact shot sequence, or original absolute timing. Do not universalize prevalence, camera cause, gait, technique, or intent from incomplete evidence. Saved examples are optional provenance only; owner procedures remain the operational source of truth.

## Non-goals

The design does not authorize media re-review, claims of archive completion, schema or project-payload changes, required casebank behavior, new universal filmmaking doctrine, narrative/asset imitation, or claims of naturalness, generated-output quality, or statistical generalization.

## Validation plan for implementation

1. The initial post-edit five-call smoke remains a **failed, non-passing** result: C1 retrievable crosswalk 0/5, C2 evidence→mechanism→owner→QA 0/5 complete and 1/5 partial, C3 candidate-versus-confirmed outcome 1/5 pass, C4 source gates 5/5 pass, and C5 playback/audio claims 5/5 pass; all five overall results are NOT PASS. The prompt/context/rubric mismatch makes C1/C2/C3 insufficiently testable, not evidence the skill lacks source data. Preserve the [initial result](../../../qa/rofan-archive-crosswalk-smoke-results.md).
2. Preserve all one-row outcomes separately: follow-up v1 NOT PASS; follow-up v2 INCOMPLETE/UNGRADABLE; known-model v1 NOT PASS; known-model v2 NOT PASS; known-model v3 NOT PASS. Do not alter their grades or raw outputs. The [test plan](../../implementation/2026-10-12-rofan-craft-skill-test-plan.md) links each result.
3. The new V4 known-model run **PASSes** its separately predeclared one-row acceptance, including exact filename/full IDs, both candidate dispositions, current selected-source status and all OPEN gates, exact 06 field `크기/카메라 위치`, and all five Shot-DNA fields. Model: `openai-codex/gpt-6-luna`; see [V4 raw result and grade](../../../qa/rofan-archive-crosswalk-known-model-v4-results.md). This bounded pass is not archive completion.
4. Both original negative controls already PASS (single-reference and unrelated brief; [initial smoke results](../../../qa/rofan-archive-crosswalk-smoke-results.md)). A separate same-prompt baker baseline/with-current-skill comparison also passed the manual scope check in both arms; the current arm did not consult module 25, the crosswalk, or a casebank. It is one sample per arm, descriptive only ([comparison record](../../../qa/rofan-unrelated-brief-baseline-with-skill.md)).
5. No validation claims full-source content completion, full-rate playback, human audio listening, media naturalness, or all-44 analysis. Preserve all modality distinctions and open source gates.

## Completion criteria

The implementation satisfies the design contract: the optional template encodes the joins and gates; audit links it; procedure 25 requires it only for exhaustive/cross-source extraction and keeps ordinary single-reference use light; existing owners and P14/L03 are reused without duplication. The V4 output acceptance and both negative controls passed, but archive-wide coverage gates remain OPEN; no 44-source analysis/completion claim follows.
