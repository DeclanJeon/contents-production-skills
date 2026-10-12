# Archive crosswalk known-model v3 skill-output run

**Overall: NOT PASS.** C1, C2, C3 and C5 pass. C4 fails: the 06 owner mapping omits the applicable `크기/카메라 위치` field, despite otherwise listing the required identity/time and approach/response/contact fields and all five Shot-DNA chain fields. The current-status contract elicited the exact selected-source status and all five OPEN gates. Do not mark overall acceptance complete.

## Run metadata

- One fresh stateless task-agent skill-output call, run label `CrosswalkKnownModelV3`; not an eval-default completion call. No retry.
- Runtime-advertised model identity: `openai-codex/gpt-6-luna`. The task interface exposed no tier/effort suffix or separate per-call model string; none is invented.
- Model context: current working-tree skill/package instructions and relevant owner templates, plus bounded current evidence from the master, CF-13 catalog, selected source ledger, candidate dispositions, and current semantic index resolved from the master pointer. No test plan, rubric, prior output, or QA result in call context. No F: writes or original-media/images/playback.
- Updated skill context SHA-256: `video-production-assets/references/25-reference-video-analysis.md` `28b2ecb29fdd3271e75c594299fdd1fd367a15bfd7b1e85eb63ff7097f2a30f4`; `video-production-assets/assets/archive-craft-crosswalk-template.md` `f6ea8b914cc40d49b7d52ae0d23ad840936238b13ee056adbe03e973829c737e`.
- Other current package context SHA-256: `video-production-assets/SKILL.md` `c400ac9192be3b9783b131a1e4f1574e4aa9c8027cdfe160fa350cd35aafdcca`; `assets/archive-audit-template.md` `333e6f844ac79878b7a948761abc19c50dc57d0ee38d105bc3a50f5b1c15e487`; `assets/shot-dna-template.md` `5dbc0b305ad97da240baf19cf92db5962fd1824b48448a73f57fc0600f9ab3fa`; `references/06-shots.md` `ee493732d45b82fc5f640a9af8041fca3e78e363da6183de14d59115e5de6b5e`; `assets/06-shots-template.md` `506c83f3814c04ed1ebb429301d0f92ee9644e30207de74d03a4d032e18ae860`.
- Bounded F: source files (SHA-256): master `f62effd762239c581992213ad4e371b79aa6c22f0682c50b921a43d563135a6e`; craft catalog `63984d67816a38d40c33f55120b5e30702f607981eeadab0b4feebe64adadb6f`; selected ledger `2226407c876bd979cc236e55ddb17db6276f2059893d55e9ced81a6c8a134d8a`; candidate dispositions `a986c48e1ce3f007ea07bff44efbde2afabee004854a480c2db5ae9c4ebb52e2`; semantic index `93ec30254ccf99f53695629be4eb91aee50fa0497f813ac068ee76bd8b4952b2`.

## Per-criterion manual grade

| Criterion | Grade | Evidence |
|---|---|---|
| C1 — One bounded row traceable to full IDs and exact filename | **PASS** | Full source-position, archive, scene, shot, and event IDs; sequence is explicitly `UNKNOWN`; exact filename is carried in bounded provenance. |
| C2 — Half-open shot interval and supported candidate outcomes | **PASS** | `[0,77824)` at 1/15360; exact candidates 77824 and 78848 with dispositions and native neighbors; no unsupported cut. |
| C3 — Story-neutral mechanism, inference alternative, transfer and avoid conditions | **PASS** | Mechanism is generic, conditional, timing-free, and carries an alternative and counterconditions. |
| C4 — Full existing 06 owner/QA map and five Shot-DNA fields | **FAIL** | All four identity/time fields, the six required approach/response/contact fields, QA slot, and all five separately labeled Shot-DNA fields are present. However, `크기/카메라 위치` is applicable to selecting the shared-frame composition and is absent from the owner map. Thus the requested full 06 field mapping is incomplete. |
| C5 — Exact selected-source status, archive counts and current open gates | **PASS** | Reports `visual_semantic_craft_closed` with master locator, 34/44 materialized and 10 unmaterialized, all five exact OPEN `global_merge_gates` keys/statuses, and distinguishes 44/44 indexed identities from closure. |
| No media/coverage overclaim | **PASS** | Explicitly reports semantic-ledger evidence only; no media playback, human audio, full-rate motion, or archive completion claim. |

## Raw skill-output response

```json
{
  "crosswalk_row": {
    "finding_id": "CF-13",
    "linked_occurrence_sequence_scene_shot_event_ids": {
      "source_position_id": "ea6a017b14fc647205b30ea896553c8e36e3abbc2983b73757a9c7cb282a8257",
      "sequence_id": "UNKNOWN / not supplied in bounded ledger rows",
      "scene_id": "F-EA-SC01",
      "shot_id": "archive-shot:ea6a017b14fc647205b30ea896553c8e36e3abbc2983b73757a9c7cb282a8257:p0",
      "event_id": "archive-event:ea6a017b14fc647205b30ea896553c8e36e3abbc2983b73757a9c7cb282a8257:p0:F01"
    },
    "bounded_source_provenance": {
      "archive_id": "sha256:4831e753f691064aaa92b4b3748045b3fbef7d6dc76e0cfb21e37f1b7c4db195",
      "source_sha256": "4831e753f691064aaa92b4b3748045b3fbef7d6dc76e0cfb21e37f1b7c4db195",
      "exact_filename": "AI 로판 드라마 ｜ 몰아보기 EP.1~9 ｜ 버려진 약혼녀에게 집착이 시작됐다 🗝️.mp4",
      "source status": "visual_semantic_craft_closed; quality_status.review_status=complete; master locator semantic/reviewer-F/ea6a017b14fc647205b30ea896553c8e36e3abbc2983b73757a9c7cb282a8257-canonical-shot-scene-event-ledger.json#/shots/0",
      "selected shot interval": "[0,77824) source PTS, half-open, timebase 1/15360. Last visible PTS 77312; next/cut PTS 77824. The normalized master row itself has null source_pts_interval bounds; this bounded interval is supported by canonical ledger visible span and exit/next evidence, not by that null wrapper interval.",
      "selected scene span/quality": "Scene F-EA-SC01; bounded shot/event evidence only."
    },
    "directly_observed_evidence": "Ledger-reported reviewed sampled/native states within the selected shot: a second figure enters the shared composition; shared proximity is maintained; a visible arm rises; a hand reaches/cups the face; that contact/close shared state remains at last visible PTS 77312. Exact native boundary comparison: last visible PTS 77312 differs abruptly from PTS 77824; PTS 77824 and 78336 retain the incoming corridor composition. This is ledger-reported observation, not independent image inspection or playback. Relevant locators: canonical ledger #/shots/0/within_shot and #/shots/0/exit; dense_frames.jsonl positions mapped in that ledger; reviewer-F native-union candidate records at PTS 77824 and 78848.",
    "inference_and_alternative": "[INFERENCE, low confidence] A stable shared frame followed by a readable contact state may make approach/response/contact legible before an editorial reset. Alternative: conventional close coverage, generated-image/pose continuity, or routine dramatic staging; creator intent and causal/emotional purpose are not directly established.",
    "story_neutral_mechanism": "For a beat whose meaning depends on an approach or contact and the partner's response, compose both the initiating action and receiving response legibly in a shared frame; allow the resulting state to register before an edit that changes the relevant relation. This is a compositional option, not a mandatory formula or prescribed duration; it establishes no camera path, gait, or physical action mechanics.",
    "transfer_conditions": "Transfer only when the new brief's beat depends on who approaches/touches whom, and a shared composition can make initiator, response, and resulting state legible. Select new blocking, composition, and timing from that brief; add separate reaction coverage only if it conveys information unavailable in the shared frame.",
    "avoid_or_counterconditions": "Avoid when a shared frame obscures key action/response, the intended beat is not relational/contact-dependent, or separate viewpoints are required for comprehension. Do not infer consent, force, emotional intent, full gait, continuous natural motion, camera movement, exact timing, or scene continuity from these records. Do not carry forward source-specific story/assets, blocking or order.",
    "existing_owner_procedure_and_exact_template_fields": {
      "receiving_owner": "video-production-assets/references/06-shots.md; existing output template video-production-assets/assets/06-shots-template.md",
      "identity_time_fields": [
        "shot_id",
        "scene_id",
        "beat_id",
        "shot-local time (s or frames; FPS if frames)"
      ],
      "applicable_creative_fields": [
        "인물 블로킹",
        "시선/축",
        "공개 정보",
        "관점·감정/구도 의도",
        "대안·채택/승인 상태",
        "종료 프레임"
      ],
      "applicable_QA_slot": "06-shots.md §완료 조건: 보드 목적에 맞는 촬영 가능한 커버리지/방향성, 각 샷의 관점·구도 선택이 의도한 정보와 감정을 전달하는지, 실제 이미지가 있으면 필수 행동과 주목점이 읽히는지, 동작 중심 panel 인접 keyframe에서 자세·행동·접촉/위치가 실제로 달라지는지. For the receiving shot plan, inspect the listed existing 06 fields for visible initiating action, partner response, axis/readability, information, chosen-vs-unapproved alternative and explicit end state; text alone does not prove media quality."
    },
    "target_specific_observable_acceptance_check": "In the new planned frame/shot, verify from its actual board/render at intended viewing size that both the initiating action and receiving response are visible/readable, the relation is unambiguous, and the end state registers before the planned edit; confirm the selected axis and end frame. If actual media is not available, status remains planned/unverified, not passed.",
    "five_shot_dna_transfer_chain": {
      "레퍼런스 증거(관찰+위치)": "As bounded in directly_observed_evidence: selected source occurrence/scene/shot/event full IDs; canonical ledger #/shots/0; native last-visible PTS 77312 and candidate at 77824. Sampling/state notes and two native candidate dispositions; no independent media inspection.",
      "메커니즘": "As stated in story_neutral_mechanism: co-present action/response legibility, visible resulting state, then a relation-changing edit if the new brief calls for it.",
      "의도 효과(해석)": "[INFERENCE, low confidence] May clarify proximity/contact before reset; alternative is routine coverage or generated pose continuity, with no proven intent.",
      "새 브리프 제작 요구": "Only if a new brief needs legible approach/contact and partner response: use the actual 06 template identity/time fields and relevant creative fields listed above; invent no source-derived IDs or timing here. Proposed timing remains UNKNOWN until brief/owner design.",
      "정성 검증 기준": "Apply the target_specific_observable_acceptance_check and exact 06 completion/QA slot above; evaluate planned text separately from actual board/render evidence."
    },
    "evidence_gaps_status": "The source's visual-semantic craft status is closed at the exact master locator above; this does not close archive-global coverage or establish creator intent, audio, full-rate playback, physical camera cause, consent/force, or natural gait. Selected-source timeline sampling was reported as 0.2-second dense states plus native boundary triplets; candidate file says all 650 reviewed, not continuous playback."
  },
  "candidate_disposition_records": [
    {
      "candidate_id": "archive-event:ea6a017b14fc647205b30ea896553c8e36e3abbc2983b73757a9c7cb282a8257:77824",
      "source_position_id": "ea6a017b14fc647205b30ea896553c8e36e3abbc2983b73757a9c7cb282a8257",
      "sequence_id": "UNKNOWN / not supplied in bounded ledger rows",
      "scene_id": "F-EA-SC01 (outgoing); F-EA-SC02 (incoming)",
      "candidate_pts": 77824,
      "timebase": "1/15360",
      "disposition": "BOUNDARY_SUPPORTED (source disposition observed_hard_view_change; ledger hard_cut_start; distinct from detector candidate status)",
      "support": "Native neighbor PTS 77312 is outgoing shot; candidate PTS 77824 begins incoming view; PTS 78336 persists incoming view. Source evidence records abrupt composition change and confirms visually. Exact locator: candidate-dispositions.json#/items/0; canonical ledger #/shots/0/exit and #/shots/1/entry.",
      "rationale_uncertainty": "Supported hard boundary at 77824; production/capture cause unknown. Earlier 0–10s dense-window cue assigning change around 4.9s is superseded by native neighbor evidence; do not use it as shot fact.",
      "linked_boundary_id": "UNKNOWN / no separate boundary ID exposed"
    },
    {
      "candidate_id": "archive-event:ea6a017b14fc647205b30ea896553c8e36e3abbc2983b73757a9c7cb282a8257:78848",
      "source_position_id": "ea6a017b14fc647205b30ea896553c8e36e3abbc2983b73757a9c7cb282a8257",
      "sequence_id": "UNKNOWN / not supplied in bounded ledger rows",
      "scene_id": "F-EA-SC02 (incoming; same shot as PTS 77824)",
      "candidate_pts": 78848,
      "timebase": "1/15360",
      "disposition": "REJECTED as a shot boundary / continuous_within_shot",
      "support": "Adjacent native samples PTS 78336, 78848, 79360; candidate-dispositions.json#/items/1 reports same corridor medium two-shot and eyeline with no composition discontinuity across 5.100–5.167s.",
      "rationale_uncertainty": "Candidate is accounted for as continuous within shot, not another cut. Bounded record supports no composition discontinuity at these sampled neighboring frames; it does not certify full-rate natural motion or any unobserved interval.",
      "linked_boundary_id": "N/A — no boundary supported"
    }
  ],
  "archive_status_and_global_gates": {
    "current_index_resolution": "Current master source_index_ref=semantic/archive-semantic-index.json; index current_index_ref=semantic/archive-semantic-index.json.",
    "counts": "Master: 44 source occurrences total; 34 materialized; 10 unmaterialized. Index status: 44/44 occurrence identities indexed. 44/44 identities indexed is not source/crosswalk closure.",
    "currently_open_global_merge_gates": [
      {"key": "complete_scene_shot_event_crosswalk", "status": "OPEN: only sources with available reviewer records are linked; pending sources have no fabricated rows"},
      {"key": "all_visual_shot_content_checked_against_native_images", "status": "OPEN; per-review artifact gates differ and have not been globally merged"},
      {"key": "all_candidate_free transitions_and_first_last_images", "status": "OPEN: full capture exists, but source-level shot segmentation/transition review is incomplete for many sources"},
      {"key": "all_source_scene_membership_bounds", "status": "OPEN: no cross-source midpoint partitioning; the B source's prior midpoint grouping was rejected and its corrected 12-scene crosswalk is cited"},
      {"key": "occurrence_vs_independent_cases", "status": "OPEN: preserve 44 source occurrences; after all source ledgers are merged, verify exact visual/timing alignment before linking compilation/episode repeats. Keep possible dependence explicit when unverified. Report occurrence counts separately from verified independent-case counts and do not state genre-wide prevalence."}
    ],
    "always_inference_or_unverified_global_dimensions": [
      {"key": "creator_intent", "status": "always inference with plausible alternatives; not directly recoverable from footage"},
      {"key": "camera_and_gait", "status": "image-plane and sampled state evidence may be recorded; physical 3-D path/lens calibration, continuous naturalness, and human audio performance remain unverified absent those modalities"}
    ],
    "completion_claim": "Archive completion NOT ESTABLISHED; this bounded CF-13 row is not archive-wide recurrence/prevalence or closure."
  },
  "unknowns_and_evidence_limits": [
    "No original media/images opened or played; summaries and locators in semantic ledgers only. No F: writes.",
    "Sequence membership is not supplied for this bounded source row; left UNKNOWN rather than inferred.",
    "The master normalized selected shot interval fields are null; interval [0,77824) is supported by canonical ledger visible span and exact exit/next PTS evidence as specified in the task.",
    "Human audio not listened to; no full-rate continuous playback; camera capture path/physical cause and natural gait unverified.",
    "No claim about consent, force, creator intent, emotional truth, or independent-case identity from this sample.",
    "The cross-source catalog is provisional; this is one bounded source/one finding, not analysis of all 44."
  ],
  "paths_consulted": [
    "C:/Users/Declan/.agents/skills/video-production-assets/SKILL.md",
    "C:/Users/Declan/.agents/skills/video-production-assets/references/workspace-integration.md",
    "C:/Users/Declan/.agents/skills/video-production-assets/references/25-reference-video-analysis.md",
    "C:/Users/Declan/.agents/skills/video-production-assets/assets/archive-craft-crosswalk-template.md",
    "C:/Users/Declan/.agents/skills/video-production-assets/assets/archive-audit-template.md",
    "C:/Users/Declan/.agents/skills/video-production-assets/assets/shot-dna-template.md",
    "C:/Users/Declan/.agents/skills/video-production-assets/references/06-shots.md",
    "C:/Users/Declan/.agents/skills/video-production-assets/assets/06-shots-template.md",
    "F:/Resources/AI-Rofan-Drama-2026-10-11/videos/rofan-temporal-analysis/exhaustive/semantic/archive-normalized-master-in-progress.json",
    "F:/Resources/AI-Rofan-Drama-2026-10-11/videos/rofan-temporal-analysis/exhaustive/semantic/cross-source-craft-catalog-provisional-v1.json",
    "F:/Resources/AI-Rofan-Drama-2026-10-11/videos/rofan-temporal-analysis/exhaustive/semantic/reviewer-F/ea6a017b14fc647205b30ea896553c8e36e3abbc2983b73757a9c7cb282a8257-canonical-shot-scene-event-ledger.json",
    "F:/Resources/AI-Rofan-Drama-2026-10-11/videos/rofan-temporal-analysis/exhaustive/semantic/reviewer-F/ea6a-native-union/candidate-dispositions.json",
    "F:/Resources/AI-Rofan-Drama-2026-10-11/videos/rofan-temporal-analysis/exhaustive/semantic/archive-semantic-index.json"
  ]
}
```
