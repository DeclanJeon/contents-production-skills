# Archive crosswalk known-model v4 skill-output run

**Overall: PASS against the separately predeclared V4 acceptance.** This does not change or regrade v3; v3 remains NOT PASS with its original result and frozen rubric intact.

## Run metadata

- One fresh stateless task-agent skill-output call, label `CrosswalkKnownModelV4`; no retry.
- Runtime model identity available from the system context: `openai-codex/gpt-6-luna`. The task-agent result did not expose a separate per-call model string or tier/effort suffix; none is inferred.
- Call context contained the current package files and bounded semantic master/catalog/selected-source ledger/candidate dispositions/current semantic index only. No test plan, rubric, v1/v2/v3 output or result artifact was supplied to the call.
- No F: writes, original media/images opened, or video playback.
- Current package and bounded evidence paths/hashes read:
  - `video-production-assets/SKILL.md` — `c400ac9192be3b9783b131a1e4f1574e4aa9c8027cdfe160fa350cd35aafdcca`
  - `video-production-assets/references/25-reference-video-analysis.md` — `5c76f54369a210ab729221ce01d8906a63bb47379cd580c7c92467b39ecc180e`
  - `video-production-assets/assets/archive-craft-crosswalk-template.md` — `e5ba2456b9db0726fb2a420f62fbc51a472b96a3a58de5e9f4e5321df8064f58`
  - `video-production-assets/assets/archive-audit-template.md` — `333e6f844ac79878b7a948761abc19c50dc57d0ee38d105bc3a50f5b1c15e487`
  - `video-production-assets/assets/shot-dna-template.md` — `5dbc0b305ad97da240baf19cf92db5962fd1824b48448a73f57fc0600f9ab3fa`
  - `video-production-assets/references/06-shots.md` — `ee493732d45b82fc5f640a9af8041fca3e78e363da6183de14d59115e5de6b5e`
  - `video-production-assets/assets/06-shots-template.md` — `506c83f3814c04ed1ebb429301d0f92ee9644e30207de74d03a4d032e18ae860`
  - F: `videos/rofan-temporal-analysis/exhaustive/semantic/archive-normalized-master-in-progress.json` — `f62effd762239c581992213ad4e371b79aa6c22f0682c50b921a43d563135a6e`
  - F: `videos/rofan-temporal-analysis/exhaustive/semantic/cross-source-craft-catalog-provisional-v1.json` — `63984d67816a38d40c33f55120b5e30702f607981eeadab0b4feebe64adadb6f`
  - F: `videos/rofan-temporal-analysis/exhaustive/semantic/reviewer-F/ea6a017b14fc647205b30ea896553c8e36e3abbc2983b73757a9c7cb282a8257-canonical-shot-scene-event-ledger.json` — `2226407c876bd979cc236e55ddb17db6276f2059893d55e9ced81a6c8a134d8a`
  - F: `videos/rofan-temporal-analysis/exhaustive/semantic/reviewer-F/ea6a-native-union/candidate-dispositions.json` — `a986c48e1ce3f007ea07bff44efbde2afabee004854a480c2db5ae9c4ebb52e2`
  - F: `videos/rofan-temporal-analysis/exhaustive/semantic/archive-semantic-index.json` — `93ec30254ccf99f53695629be4eb91aee50fa0497f813ac068ee76bd8b4952b2`

## Manual grade

| V4 criterion | Result | Evidence in response |
|---|---|---|
| One actual bounded crosswalk finding with exact filename and full occurrence/scene/shot/event/candidate IDs | PASS | Names exact filename, full source/shot/event/candidate IDs; sequence remains not supplied. |
| Half-open source PTS interval and exactly two supported candidate outcomes | PASS | `[0,77824)` at `1/15360`; candidate 77824 supported as hard boundary; candidate 78848 rejected as a cut and continuous within the next shot. |
| Selected-source exact status/locator, materialized/unmaterialized counts, and every current OPEN gate | PASS | Reports `visual_semantic_craft_closed`, master/source ledger locator, 34/44 materialized and 10/44 unmaterialized, plus each of the five exact OPEN gates; no archive-completion claim. |
| Story-neutral mechanism, inference alternative, transfer/avoid conditions, and limits | PASS | Mechanism excludes source narrative/assets and timings; alternative, applicability, counterconditions, and evidence limits are explicit. |
| Exact 06 receiving-owner map and target-specific QA, including `크기/카메라 위치` | PASS | Includes identity/time fields, `크기/카메라 위치`, applicable creative fields, exact procedure/template references and observable QA. |
| All five Shot-DNA `이전 체인` fields separately represented | PASS | Each exact existing label is a separate item. |
| No all-44/media overclaim | PASS | Scope is one bounded finding; response says no media/image opened, playback/audio listening, or archive completion. |

## Raw skill-output response

```text
## Archive-craft crosswalk — one bounded finding

### Scope, status, and coverage
- **Requested scope:** one source occurrence, one scene, one shot, one event, and exactly two candidate dispositions; not an all-source/all-shot analysis.
- **Actual inspected scope:** bounded JSON semantic ledgers and current index only; sampled/native state evidence as cited below. No media/image opened, continuous playback or audio listening performed.
- **Selected source status (current master):** `visual_semantic_craft_closed`; `review_status: complete`. Quality-gate reason: owner source-review visual-semantic review is complete with no open visual-semantic items; this does not imply human-heard audio or full-rate playback.
- **Exact filename (master source row):** `AI 로판 드라마 ｜ 몰아보기 EP.1~9 ｜ 버려진 약혼녀에게 집착이 시작됐다 🗝️.mp4`
- **Source identity:** `source_position_id: ea6a017b14fc647205b30ea896553c8e36e3abbc2983b73757a9c7cb282a8257`; `archive_id: sha256:4831e753f691064aaa92b4b3748045b3fbef7d6dc76e0cfb21e37f1b7c4db195`.
- **Current master locator:** `semantic/archive-normalized-master-in-progress.json#/sources` → selected source row; its `source_row_ref` is `semantic/reviewer-F/ea6a017b14fc647205b30ea896553c8e36e3abbc2983b73757a9c7cb282a8257-canonical-shot-scene-event-ledger.json#/shots`. Master `source_index_ref: semantic/archive-semantic-index.json`; resolved current index `current_index_ref: semantic/archive-semantic-index.json`, with gates read from `semantic/archive-semantic-index.json#/global_merge_gates`.
- **Archive-wide occurrence coverage:** 34/44 source occurrences materialized; 10/44 unmaterialized. Counts are occurrences, not independent cases. This does not establish archive completion or all-44 analysis.
- **Current OPEN global gates (exact key/status):**
  - `complete_scene_shot_event_crosswalk` — `OPEN: only sources with available reviewer records are linked; pending sources have no fabricated rows`
  - `all_visual_shot_content_checked_against_native_images` — `OPEN; per-review artifact gates differ and have not been globally merged`
  - `all_candidate_free transitions_and_first_last_images` — `OPEN: full capture exists, but source-level shot segmentation/transition review is incomplete for many sources`
  - `all_source_scene_membership_bounds` — `OPEN: no cross-source midpoint partitioning; the B source's prior midpoint grouping was rejected and its corrected 12-scene crosswalk is cited`
  - `occurrence_vs_independent_cases` — `OPEN: preserve 44 source occurrences; after all source ledgers are merged, verify exact visual/timing alignment before linking compilation/episode repeats. Keep possible dependence explicit when unverified. Report occurrence counts separately from verified independent-case counts and do not state genre-wide prevalence.`
- `creator_intent` remains inference with plausible alternatives; `camera_and_gait` states sampled/image-plane evidence only and leaves physical path/lens calibration, continuous naturalness, and human audio performance unverified. These are not additional `OPEN`-status entries in the gate map.

### Source/scene/shot/event join
- `scene_id: F-EA-SC01`
- `shot_id: archive-shot:ea6a017b14fc647205b30ea896553c8e36e3abbc2983b73757a9c7cb282a8257:p0`
- `event_id: archive-event:ea6a017b14fc647205b30ea896553c8e36e3abbc2983b73757a9c7cb282a8257:p0:F01`
- **Source interval:** `[0,77824)` PTS at timebase `1/15360` (0 to 5.066667 s). Last visible source frame is PTS 77312 (5.033333 s); PTS 77824 is the first frame of the next shot. Half-open end is the supported hard boundary, not a claim that a visible source frame exists at the exclusive endpoint.
- **Observed sampled states:** at PTS 0, profile figure beside a gray wall and lit brazier at frame right; at PTS 39424 (2.566667 s), second figure is present at her right, leaning in as her chin tilts upward; at PTS 77312, a hand cups her cheek and their faces are nearly touching, with wall/brazier anchors retained. Dense states additionally record arm lifting, reach, and held contact. These are timestamped sample states, including the manually reviewed start/within/end native frames—not continuous motion proof. No physical camera move, unseen footwork, audio, or intent is asserted.
- **Evidence/limitation:** ledger `#/shots/0` and its `within_shot` / `exit` / `craft` fields; source-side `manual_visual_review_ref` `.../ea6a-shot-local-audit.json` (shot locator `#archive-shot:ea6a017b14fc647205b30ea896553c8e36e3abbc2983b73757a9c7cb282a8257:p0`); native neighbor sequence PTS 77312→77824→78336 recorded in candidate disposition and shot entry. Semantic source review is closed for this source, but the evidence is sampled frames/ledger descriptions rather than playback. Audio is unlistened. The earlier dense-window doorway cue at ~4.9 s is explicitly superseded by the native PTS evidence and is not used as a shot fact.

### Exactly two candidate disposition records
| candidate_id (verbatim) | PTS / timebase | outcome and evidence | disposition |
|---|---|---|---|
| `archive-event:ea6a017b14fc647205b30ea896553c8e36e3abbc2983b73757a9c7cb282a8257:77824` | 77824 / `1/15360` | Native neighboring frames: 77312 shows close wall two-shot with cheek contact; 77824 and 78336 show bright corridor medium two-shot. Abrupt persistent view change. | `BOUNDARY_SUPPORTED` — visually confirmed hard cut at PTS 77824; physical/production cause unknown. Ends the selected interval. |
| `archive-event:ea6a017b14fc647205b30ea896553c8e36e3abbc2983b73757a9c7cb282a8257:78848` | 78848 / `1/15360` | Native neighbors 78336, 78848, 79360 show the same bright corridor medium two-shot and eyeline, with no composition discontinuity across 5.100–5.167 s. | `REJECTED` as a cut candidate; continuous within the next shot, not a cut. |

### Finding `F-EA-P0-CONTACT-HOLD`
- **Linked occurrence / sequence / scene / shot / event:** `ea6a017b14fc647205b30ea896553c8e36e3abbc2983b73757a9c7cb282a8257` / sequence `NOT SUPPLIED` / `F-EA-SC01` / `archive-shot:ea6a017b14fc647205b30ea896553c8e36e3abbc2983b73757a9c7cb282a8257:p0` / `archive-event:ea6a017b14fc647205b30ea896553c8e36e3abbc2983b73757a9c7cb282a8257:p0:F01`.
- **Directly observed evidence + exact location:** within `[0,77824)` PTS, `1/15360`; start PTS 0; manually reviewed intermediate PTS 39424; last visible PTS 77312; next-shot hard boundary PTS 77824. Sampled description documents entry into a shared frame, approach/close spacing, raised arm, hand-to-cheek contact, and contact retained in the outgoing frame. Evidence is the shot ledger’s `within_shot.manually_read_inside_shot_native_states`, timestamped dense state list, `exit.boundary_observation`, and two candidate native-neighbor records. Sampling establishes visible states at those locations, not a continuous path or exact action onset between samples.
- **`[INFERENCE]` function + plausible alternative:** A shared tight frame that preserves both participants as distance closes and contact becomes visible may make approach → response → contact legible without requiring a reverse cut. Alternative: conventional close coverage or generated/animated pose progression and continuity, without intentional emphasis; production intent is not directly observable.
- **Story-neutral mechanism:** In a shared frame, stage the approach and response so their relative spacing changes visibly; keep the relevant contact point readable, then hold the resulting state long enough to register before ending the shot. Treat camera movement as unproven/unnecessary unless the new brief independently motivates it.
- **Transfer conditions:** Apply only when a new brief requires a legible approach/response/contact-state beat, both participants can plausibly share the frame, and the desired contact is safe, consent-appropriate, and narratively specified by that brief. Choose new actors, setting, props, timing, and camera treatment from the new brief; do not import source imagery or absolute timing.
- **Avoid / counterconditions:** Avoid if shared-frame staging obscures the response or contact, creates an unsafe/ambiguous interaction, compromises required POV/reaction information, or the brief calls for separate viewpoints. Do not infer a physical camera move, unseen footwork, motive, or continuous natural motion from sparse states; split viewpoints only when the target information cannot be shown together.
- **Existing receiving owner and exact QA slots:** `video-production-assets/references/06-shots.md`, shot/blocking procedure steps 2–3 and 6–10; receiving template `video-production-assets/assets/06-shots-template.md`, shot row and consequential moving-shot cue timeline only if the new shot makes a walk/stop or camera move consequential. Populate applicable existing fields verbatim: `shot_id`, `scene_id`, `beat_id`, `shot-local time (s or frames; FPS if frames)`, `크기/카메라 위치`, `인물 블로킹`, `시선/축`, `공개 정보`, `관점·감정/구도 의도`, `대안·채택/승인 상태`, `종료 프레임`. New-plan `beat_id` and planned time are not established by this source analysis and are assigned by the receiving plan; source-local reference time is 0–5.066667 s, not a proposed new brief duration. Exact target QA: 06 procedure completion checks—intended information/emotion readability and, where actual images exist, key action/attention readability and start/action-peak/end state differences; for the cue timeline, verify applicable actor/camera onset, deceleration/stop/settle/hold and visible contact or explicitly unverified/hidden contact. Text handoff cannot prove the rendered result.

### Shot-DNA `이전 체인` (separately represented)
- **레퍼런스 증거(관찰+위치):** At source `ea6a017b14fc647205b30ea896553c8e36e3abbc2983b73757a9c7cb282a8257`, scene `F-EA-SC01`, shot `archive-shot:ea6a017b14fc647205b30ea896553c8e36e3abbc2983b73757a9c7cb282a8257:p0`, event `archive-event:ea6a017b14fc647205b30ea896553c8e36e3abbc2983b73757a9c7cb282a8257:p0:F01`, sampled start/within/end states PTS 0/39424/77312, timebase `1/15360`; PTS 77824 is the supported hard-cut endpoint. Sampled state evidence only.
- **메커니즘:** Shared-frame approach/response, readable contact point, and a brief hold on the resulting state; no story/source specifics.
- **의도 효과(해석):** `[INFERENCE]` May clarify relational distance and contact without another viewpoint; alternative: ordinary coverage or generated/animated pose continuity rather than intentional emphasis.
- **새 브리프 제작 요구:** For a brief that needs this legibility and can stage both participants safely in one frame, specify framing/position, blocking, eyeline/axis, information reveal, desired emotional/compositional purpose, alternatives/approval state, and endpoint in the existing 06 shot row. New-plan shot/scene/beat IDs and shot-local duration are assigned there, not inferred from source IDs/time.
- **정성 검증 기준:** In the target shot’s actual planned/rendered evidence, confirm both participants and the relevant contact point remain readable through approach, response, contact, and endpoint; confirm intended eyelines/axis and endpoint state. If actual media is unavailable, leave media-quality verification unverified.

### Open status and exclusions
Selected-source visual-semantic craft status is closed as above, but global merge gates remain open. No source-wide or archive-wide completion claim follows. Finding is a bounded transfer proposal; target-specific rendered-media QA remains unperformed. No story/character/design/timing copying, external use, generation, or production approval implied.
```