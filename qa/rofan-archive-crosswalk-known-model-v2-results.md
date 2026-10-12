# Archive crosswalk known-model v2 skill-output run

**Overall: NOT PASS.** The output states the selected source's exact status and counts, and includes a concrete owner handoff, but misses required source identity/chain details and does not enumerate the current global open gates completely. Do not mark the status-contract change complete.

## Run metadata

- One fresh stateless `functions.task` task-agent call, run label `CrosswalkKnownModelV2`; not an `eval`-default completion call. No retry.
- Runtime-advertised model identity: `openai-codex/gpt-6-luna`. The task interface exposed no tier/effort suffix or separate per-call model string; none is invented.
- The model context contained the current package instructions/references/templates and only the bounded current F: semantic master, catalog, selected source ledger, and candidate dispositions. It did not contain the test plan, rubric, previous output, previous QA artifacts, or diagnosis. No source media/images/playback or F: writes.
- Package evidence version (SHA-256): `video-production-assets/references/25-reference-video-analysis.md` `1c2c9f2fd9aa532600ea96fb8710de679d4f4e4550cac77ba2651b1273840ad2`; `video-production-assets/assets/archive-craft-crosswalk-template.md` `6e2fe18678d40f5ea519bb772e8a42c4004da3e5bacccdd0c4246ab93369e436`.
- The bounded F: evidence sources are the current master, provisional CF-13 craft catalog, selected `ea6a…` source semantic ledger, and its candidate-dispositions ledger. No original media was inspected.

## Per-criterion grade against frozen assertions and behavioral transfer

| Criterion | Grade | Exact reason |
|---|---|---|
| C1 — One bounded, traceable crosswalk row (including source occurrence and exact filename) | **FAIL** | Row has full source-position/archive, scene, shot, and event IDs and explicitly marks sequence `UNKNOWN`, but omits the exact source filename required by the frozen source-row assertion. |
| C2 — Half-open shot bounds and supported candidate outcomes | **PASS** | Gives `[0,77824)` at 1/15360 and full candidate IDs/PTS, outcomes and native-neighbor triplets; no unsupported cut is claimed. |
| C3 — Story-neutral mechanism, inference alternative, applicability and avoid conditions | **PASS** | Transfer rule is generic, has an alternative, applies conditionally, and avoids importing source staging or timings. |
| C4 — Exact 06 receiving owner/QA fields and all five existing Shot-DNA `이전 체인` fields | **FAIL** | The 06 mapping names required target identity/time, applicable creative fields, cue-table QA and `완료 조건`. However, the response does not explicitly map to all five `이전 체인` fields: `레퍼런스 증거(관찰+위치)`, `메커니즘`, `의도 효과(해석)`, `새 브리프 제작 요구`, and `정성 검증 기준`. |
| C5 — Selected-source and archive-global status contract | **FAIL** | Correctly states selected `visual_semantic_craft_closed`, 34/44 materialized and 10 unmaterialized. It gives examples of open source-specific gates but not an exhaustive named list of the current archive-global gates; it uses “e.g.” and “other status rows” rather than naming each gate. Required gate inventory includes the archive crosswalk, native-image checks, candidate-free transitions/first-last images, scene membership bounds, and occurrence-vs-independent-case reconciliation. |
| Behavioral transfer clarification: 06 handoff carries target identity/time plus applicable exact creative/QA fields | **PASS** | Lists all required 06 identity/time and applicable creative/QA fields, plus additional relevant existing cue-table fields, with no new schema. |

The status contract elicited the exact selected-source status and counts, but the row still fails the frozen completeness assertions; the global gate list is not complete, and the explicit Shot-DNA chain and exact filename are omitted. No overall pass claim.

## Raw skill-output response

```json
{
  "crosswalk_row": {
    "finding_id": "CF-13",
    "linked occurrence / sequence / scene / shot / event IDs": "source_position_id=ea6a017b14fc647205b30ea896553c8e36e3abbc2983b73757a9c7cb282a8257; sequence_id=UNKNOWN (no sequence ID established in the supplied bounded evidence); scene_id=F-EA-SC01; shot_id=archive-shot:ea6a017b14fc647205b30ea896553c8e36e3abbc2983b73757a9c7cb282a8257:p0; event_id=archive-event:ea6a017b14fc647205b30ea896553c8e36e3abbc2983b73757a9c7cb282a8257:p0:F01",
    "directly observed evidence + exact source PTS/timebase and locator": "Semantic master raw shot record: shot visible from PTS 0 through 77312 inclusive, half-open shot interval [0,77824), timebase 1/15360; within-shot observation reports a second figure entering by 3072, shared framing, an arm rising, a hand reaching the cheek, and close contact persisting through PTS77312. Entry and within-shot evidence are native images in the source record, with dense chronology and manual visual-review refs; cited locator is canonical-shot-scene-event-ledger.json#/shots/0, corroborated by archive-normalized-master-in-progress.json source row. Crosswalk source range in the provisional catalog: 0–5.033333s / PTS0–77312, TB1/15360. At PTS77824 (5.066667s), a visually confirmed hard view change begins; candidate record supplies neighboring native PTS77312,77824,78336. At PTS78848 (5.133333s), the candidate is continuous within the new shot, not a cut.",
    "[INFERENCE] function + plausible alternative": "[INFERENCE, low confidence] Keeping an initiating action and partner response together may make changing proximity/contact legible before an editorial reset. Alternative: conventional coverage, generated-image/pose continuity, or editorial transition mechanics rather than intentional emotional timing.",
    "story-neutral mechanism (no source narrative/assets)": "In a stable shared frame, let an approach and visible partner response accumulate, then allow the consequential contact/state to register before cutting to a genuinely distinct relation or space. No literal path, footfall count, particular gesture, measured camera move, or fixed duration is specified.",
    "transfer conditions (new brief predicate)": "Use only when a target action's meaning depends on who approaches or makes contact with whom and both initiating action and receiving response can be kept legible together. Determine timing from the new brief and shot-local action; use separate reaction coverage only when it adds information.",
    "avoid / counterconditions": "Avoid treating this as a universal romance/intimacy rule or prescribing duration, gait, force, consent, intent, physical camera motion, or a particular edit. Do not use a shared frame if it obscures required information, consent/safety, or meaningful reactions; do not assert continuous gait from sparse frames. Do not import source narrative, characters, place, props, wardrobe, choreography, exact shot sequence, or original timing.",
    "existing owner procedure + exact existing QA slot/field": "Primary receiving owner: video-production-assets/references/06-shots.md; existing template video-production-assets/assets/06-shots-template.md. Identity/time fields: `shot_id`, `scene_id`, `beat_id`, `shot-local time (s or frames; FPS if frames)`. Applicable creative fields: `인물 블로킹`, `시선/축`, `공개 정보`, `관점·감정/구도 의도`, `대안·채택/승인 상태`, `종료 프레임`. Applicable consequential-motion QA cue-table fields: `Local time (shot seconds)`, `Actor phase / contact / visibility`, `Camera phase`, `Reveal / hold`, `Cut-out → cut-in phase`. Exact QA slot: 06-shots.md §완료 조건, plus template cue table's contact visibility / reveal-hold / cut cue checks (and shot-plan field `종료 프레임`). Do not prescribe/give a camera move unsupported by evidence.",
    "target-specific observable acceptance check": "In the new target plan, verify both initiating action and response are readable in the stated shot/frame; the contact or resulting state is explicitly visible and given a distinct register/hold only if the brief warrants it; shot-local cues fit the owning shot; any cut is linked to an observable distinct information/space state. Text-plan checks establish planning only, not actual-media quality.",
    "evidence gaps / status": "Provisional finding is retrievable as a bounded case, not archive-wide prevalence/general law. Selected source exact current master status: source_quality_gate.status=visual_semantic_craft_closed; review_status=complete; 468-shot visual-semantic audit closed, with no open visual-semantic items. This is not audio/listening or playback closure. Archive global: 34/44 source occurrences materialized; 10 unmaterialized. Open global gates include those 10 unmaterialized occurrences and unresolved source-specific owner gates: e.g. 430 source shot-phase/function craft open, 1c625 source candidate-miss/reciprocal coverage gates open, 3090 all438 shot-local craft open, d31 unique transition grouping/possible-miss/semantic partition open, and other status rows explicitly marked open/not explicitly closed. Overall status remains IN_PROGRESS_ACTIVE_PARTITION_V5; archive completion NOT ESTABLISHED. Evidence is semantic ledger and sampled/native-frame review metadata only; no original media/images opened here, no continuous/full-rate playback, no human audio listening, and no physical capture-cause finding."
  },
  "candidate_disposition_records": [
    {
      "candidate_id": "archive-event:ea6a017b14fc647205b30ea896553c8e36e3abbc2983b73757a9c7cb282a8257:77824",
      "source_position_id": "ea6a017b14fc647205b30ea896553c8e36e3abbc2983b73757a9c7cb282a8257",
      "sequence_id": "UNKNOWN",
      "scene_id": "F-EA-SC01 (outgoing); incoming shot scene F-EA-SC02",
      "candidate_pts": 77824,
      "timebase": "1/15360",
      "time_seconds": 5.066666666666666,
      "outcome": "BOUNDARY_SUPPORTED / observed_hard_view_change; hard cut visually confirmed by current semantic shot record",
      "native_neighbor_pts": [77312, 77824, 78336],
      "evidence_locator": "candidate-dispositions.json item candidate_order 1; canonical shot record exit and following shot entry",
      "direct_observation": "Abrupt switch from outgoing close wall composition at PTS77312 to bright corridor medium two-shot at PTS77824; candidate and next frame persist in corridor.",
      "uncertainty": "Visual boundary supported; production/capture cause unknown. Do not treat provisional 4.9s dense-window change cue as cut evidence; native neighbors supersede it."
    },
    {
      "candidate_id": "archive-event:ea6a017b14fc647205b30ea896553c8e36e3abbc2983b73757a9c7cb282a8257:78848",
      "source_position_id": "ea6a017b14fc647205b30ea896553c8e36e3abbc2983b73757a9c7cb282a8257",
      "sequence_id": "UNKNOWN",
      "scene_id": "F-EA-SC02",
      "candidate_pts": 78848,
      "timebase": "1/15360",
      "time_seconds": 5.133333333333334,
      "outcome": "REJECTED as cut / continuous_within_shot",
      "native_neighbor_pts": [78336, 78848, 79360],
      "evidence_locator": "candidate-dispositions.json item candidate_order 2",
      "direct_observation": "Same corridor medium two-shot and eyeline continue across 5.100–5.167s; no composition discontinuity.",
      "uncertainty": "Candidate is a no-cut locator within the continuing shot; the disposition does not establish motion naturalness or full-rate continuity."
    }
  ],
  "paths_consulted": [
    "video-production-assets/SKILL.md",
    "video-production-assets/references/25-reference-video-analysis.md",
    "video-production-assets/assets/archive-craft-crosswalk-template.md",
    "video-production-assets/assets/archive-audit-template.md",
    "video-production-assets/assets/shot-dna-template.md",
    "video-production-assets/references/06-shots.md",
    "video-production-assets/assets/06-shots-template.md",
    "F:\\Resources\\AI-Rofan-Drama-2026-10-11\\videos\\rofan-temporal-analysis\\exhaustive\\semantic\\archive-normalized-master-in-progress.json",
    "F:\\Resources\\AI-Rofan-Drama-2026-10-11\\videos\\rofan-temporal-analysis\\exhaustive\\semantic\\cross-source-craft-catalog-provisional-v1.json",
    "F:\\Resources\\AI-Rofan-Drama-2026-10-11\\videos\\rofan-temporal-analysis\\exhaustive\\semantic\\reviewer-F\\ea6a017b14fc647205b30ea896553c8e36e3abbc2983b73757a9c7cb282a8257-canonical-shot-scene-event-ledger.json",
    "F:\\Resources\\AI-Rofan-Drama-2026-10-11\\videos\\rofan-temporal-analysis\\exhaustive\\semantic\\reviewer-F\\ea6a-native-union\\candidate-dispositions.json"
  ]
}
```
