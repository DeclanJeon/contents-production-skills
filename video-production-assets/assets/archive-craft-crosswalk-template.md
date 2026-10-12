# Archive craft crosswalk

> Archive-level relational evidence artifact. Use only when the request explicitly asks for exhaustive all-source/all-shot or cross-source craft extraction. Pair with [`archive-audit-template.md`](archive-audit-template.md) for source inventory/coverage; keep individual shot observations in [`shot-dna-template.md`](shot-dna-template.md). This template does not certify archive completion. For a single reference or ordinary analysis, do not create this crosswalk unless requested.

## Scope and completeness

- Archive / supplied root: {as supplied; do not imply access beyond evidence}
- Requested scope: {all-source/all-shot / cross-source extraction; exact request}
- Actual inspected scope: {sources, time ranges, evidence modalities actually read/reviewed}
- Status: {complete for declared scope / partial / blocked / not assessed}
- Coverage ledger: {link to archive-audit-template output}
- Semantic catalog/master version and exact locator: {if used}
- Known identity conflicts / stale snapshots: {record; do not reconcile silently}
For every bounded single-source crosswalk, use the existing status/coverage/gate slots to state (1) the selected source's exact status value and locator from the current master, (2) its exact filename in the source-provenance row (never in the reusable mechanism), and (3) archive-global materialized/total and unmaterialized occurrence counts plus each currently OPEN global gate by its exact key and status. Resolve the current semantic index through the master's current index pointer (`source_index_ref` in the current master; follow `current_index_ref` where present), then inspect that index's `global_merge_gates`. A count or selected-source closure alone is insufficient; 44/44 identities indexed is not gate closure. If a status, filename, count, pointer, or gate cannot be verified, state `UNKNOWN`/`OPEN`; never infer it or silently treat it as closed.

| Status category | Count / IDs | Evidence locator | Limitation / next gate |
|---|---|---|---|
| Requested source occurrences | | | |
| Materialized source occurrences | | | |
| Partial / unmaterialized source occurrences | | | |
| Unresolved joins / open global gates | | | |

Never convert a missing source row, missing evidence, or unresolved gate into “zero findings.” Write `NOT MATERIALIZED`, `UNKNOWN`, `NOT REVIEWED`, or `OPEN` as appropriate; no blank means complete. Counts must state whether they count source occurrences, unique source identities, or independent cases/creators.

## Source occurrence ↔ sequence/scene membership

Keep each occurrence distinct even when contents may duplicate. `source_position_id` is a stable occurrence identifier, not a row number. Preserve the supplied SHA value and `archive_id` verbatim in separate fields; never use a hash as occurrence identity or invent/silently substitute identifiers. Store exact filename including extension and path as available. Every cited occurrence, sequence, scene, shot, event, and candidate ID MUST be reproduced verbatim and in full; never use `…`, other truncation, or regenerated aliases.

| source_position_id (stable occurrence) | SHA (algorithm/value verbatim or UNKNOWN) | archive_id (verbatim or UNKNOWN) | exact filename / path | source status | source-local sequence_id | scene_id | scene membership bounds (source PTS; start inclusive, end exclusive) | membership evidence locator | reciprocal scene→source membership checked? | status / unknowns |
|---|---|---|---|---|---|---|---|---|---|---|
| | | | | | | | | | |

Sequence/scene membership is reciprocal: source rows identify their sequence and scene; each sequence/scene record below enumerates its member source occurrence IDs and bounds. Bounds must be supported by evidence; unknown bounds remain `UNKNOWN`, not inferred from sequence numbering.

| sequence_id / scene_id (source-local) | member source_position_id(s) | source PTS timebase | membership start PTS (inclusive) | membership end PTS (exclusive) | evidence locator(s) | reciprocal membership/status / open bounds |
|---|---|---|---:|---:|---|---|
| | | | | | | |

## Shot boundaries and candidate outcomes

Use the source's actual PTS/timebase. A shot interval is half-open `[start_pts, end_pts)`; retain source timebase and do not imply a frame-accurate boundary from sampled evidence. Candidate detections and confirmed boundaries are separate records. A `DETECTOR_CANDIDATE` is not a cut. A transition can be soft/uncertain without being certified as a hard cut. Shot boundary claims require evidence on both sides; otherwise preserve `ESTIMATED` or `UNKNOWN` and evidence bracket.

### Detector candidate disposition

| candidate_id | source_position_id | sequence_id / scene_id | candidate PTS / timebase | detector/source locator | outcome (`UNASSESSED` / `REJECTED` / `BOUNDARY_SUPPORTED` / `TRANSITION_CANDIDATE`) | supporting evidence on each side / locator | rationale and remaining uncertainty | linked boundary_id (if confirmed separately) |
|---|---|---|---|---|---|---|---|---|
| | | | | | | | | |

### Confirmed or unresolved shot intervals

| shot_id (source-local) | source_position_id | sequence_id / scene_id | start PTS inclusive | end PTS exclusive | PTS timebase | boundary status (`CONFIRMED_HARD_CUT` / `CONFIRMED_SOURCE_ENDPOINT` / `SOFT_TRANSITION` / `ESTIMATED` / `UNKNOWN`) | start/end evidence locators (both sides where boundary) | linked candidate_id(s), if any | uncertainty / limits |
|---|---|---|---:|---:|---|---|---|---|---|
| | | | | | | | | | |

Do not require a detector candidate to establish a boundary: candidate-free transitions and first/last source images remain explicit review gates. Do not classify overlays, blur, flare, or within-shot motion as a cut without boundary evidence. Do not infer motion from sparse stills.

## Within-shot events

Events remain distinct from cuts and transitions. Each event belongs to a shot interval or has an explicitly unresolved shot association.

| event_id | source_position_id | sequence_id / scene_id | shot_id or unresolved | event type | event PTS / timebase (or bounded interval) | direct observation | exact locator/evidence | event vs boundary distinction / uncertainty |
|---|---|---|---|---|---|---|---|---|
| | | | | | | | | |

## Transferable craft findings and owner handoff

One row per finding, with one or more evidence locators joined to the source/scene/shot/event rows above. Existing owner procedures are the destination; this is not permission to duplicate existing generic craft guidance or invent new universal camera/gait rules. Use only the existing columns below: map the finding through the `shot-dna-template.md` `이전 체인` fields `레퍼런스 증거(관찰+위치)` → `메커니즘` → `의도 효과(해석)` (including a plausible alternative) → `새 브리프 제작 요구` → `정성 검증 기준`; then name the applicable existing receiving-owner template field(s) verbatim and its exact QA check slot. Include only relevant owner columns; add no field, alias, or schema.
For a completed handoff into 06 shot planning, always name the existing target identity/time fields `shot_id`, `scene_id`, `beat_id`, and `shot-local time (s or frames; FPS if frames)`, plus every applicable existing 06 creative/QA field. For an approach/response/contact-state finding, applicable fields include `크기/카메라 위치`, `인물 블로킹`, `시선/축`, `공개 정보`, `관점·감정/구도 의도`, `대안·채택/승인 상태`, and `종료 프레임`; keep other owner mappings limited to their own applicable existing fields.

| finding_id | linked occurrence / sequence / scene / shot / event IDs | directly observed evidence + exact source PTS/timebase and locator | `[INFERENCE]` function + plausible alternative | story-neutral mechanism (no source narrative/assets) | transfer conditions (new brief predicate) | avoid / counterconditions | existing owner procedure + exact existing QA slot/field | target-specific observable acceptance check | evidence gaps / status |
|---|---|---|---|---|---|---|---|---|---|
| | | | | | | | | | |

Transfer chain completeness check for each finding:

- [ ] Observed evidence and exact locator are explicit; interpretation is labelled `[INFERENCE]` and includes an alternative explanation.
- [ ] The mechanism is stated without story, character, prop, wardrobe, distinctive design, choreography, exact shot sequence, or source absolute timing.
- [ ] Conditions for transfer and conditions for avoidance are both stated.
- [ ] The destination is an existing owner procedure and existing QA field/slot; no duplicate policy or schema field is introduced.
- [ ] Acceptance is a target-specific observable check, not a claim that a plan or text proves actual media quality.
- [ ] Every cited source occurrence, sequence, scene, shot, event, and candidate ID is verbatim and full; no `…`, truncation, or regenerated alias.
- [ ] Each completed finding maps to every applicable existing `shot-dna-template.md` `이전 체인` field and to the exact relevant receiving-owner template field(s) and QA check slot, with names copied verbatim; no invented fields.
- [ ] Every existing Shot-DNA `이전 체인` field is separately named and represented in the completed handoff: `레퍼런스 증거(관찰+위치)`, `메커니즘`, `의도 효과(해석)`, `새 브리프 제작 요구`, `정성 검증 기준`. Do not leave any field implicit in a combined explanation or add schema columns.

A finding is `RETRIEVABLE` only after this row-by-row check passes; otherwise keep its existing status unresolved/partial and state what is missing.

## Open gates and unresolved rows

List each outstanding item even when no finding can yet be made. Link the affected source occurrence/record IDs and evidence sought. Keep this section present when all findings are empty.

| gate_id | affected occurrence / record IDs | unresolved question or missing row | evidence modality required | current status | consequence for claims / transfer | closure evidence locator |
|---|---|---|---|---|---|---|
| | | | | OPEN / NOT MATERIALIZED / UNKNOWN | | |

Required gate review (mark status and provide locator or reason):

- [ ] Complete source-occurrence ↔ sequence/scene ↔ shot ↔ event crosswalk.
- [ ] Native-image/content checks where necessary; extraction success is not visual review.
- [ ] Candidate-free transitions plus source first/last images checked where scope requires them.
- [ ] Source scene membership bounds supported and reciprocal.
- [ ] Occurrence-vs-independent-case identity reconciliation resolved or explicitly OPEN.
- [ ] Extraction, actual strip/image review, continuous playback, full-source decode, motion evidence, and audio listening reported as separate modalities; no one substitutes for another.
- [ ] Findings/absence language respects every unresolved source and gate; no archive-wide completion or prevalence claim from incomplete coverage.

## Summary for the requested task

- Transferable findings supported: {finding IDs, or `NOT ASSESSED`—never infer zero from missing coverage}
- Existing owners receiving findings: {owner and linked finding IDs}
- Explicit exclusions preserved: story/events, characters/relationships, props, wardrobe, distinctive designs, original choreography/shot order, original absolute timings.
- Archive completion claim: {must remain `NOT ESTABLISHED` unless all required scope gates actually close}
