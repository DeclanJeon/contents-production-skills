# Baseline application assessment — 30-second romantic-fantasy drama

This assessment is separate from the verbatim model outputs in `qa/30s-romantic-fantasy-baseline-application.json`. It evaluates only those three outputs against the current guidance supplied to the model. No archive conclusions, reference-media observations, rendered-video results, or skill edits are included.

## Method and scope

Three stateless `completion(default)` calls were made with the current repository guidance and templates in the system context. Scenarios: (1) approach → stop → eye contact → reactions; (2) offscreen entrance/reveal; (3) moving walk → dialogue interaction. Each request asked for a 30-second shot plan and handoff. No reference video, approved designs, script/dialogue, target AI tool, or tool-control schema was supplied. These are planning-output application probes, not rendered feasibility tests or a statistical evaluation.

## Observed output strengths

- All three outputs marked timings and camera choices as design proposals, explicitly did not claim reference analysis, and disclosed missing tool capability / assets.
- All used bounded shot durations summing to 30 seconds and expressed action order, actor positions or screen direction, and at least some end states.
- The approach scenario explicitly separated approach, stops, eye contact, and reciprocal reactions; it included position, eyeline, and appearance continuity.
- The entrance scenario staged an offscreen eyeline, entry geography, threshold pause, direction of travel, axis, and reaction holds.
- The walk-to-dialogue scenario explicitly staged slow/stop/settle before speech, discussed visibility of feet and contact, maintained direction/spacing across cuts, and carried listener reaction into a final hold.
- Prompt handoffs used separate shot prompts, one primary action, start/end states and continuity. They correctly described tool support as unconfirmed and called for checking it before execution.

## Observed gaps / limitations

| Concern | Evidence in raw output | Assessment |
|---|---|---|
| Camera/actor time alignment | Across all three plans, shot-level camera directions and actor action phases are in adjacent prose/table cells, but none gives shared local timestamps/frames for camera move onset, speed change, subject movement, reveal/contact/stop, deceleration or settle. Examples: romance SH03 says ease camera as actors stop; walk scenario shot 3 says tracking eases to settle; entrance SH04 offers slow follow or static. | Current guidance enabled motivated co-planning, but outputs did not make the camera path and blocking executable on one time basis. This is the clearest gap for the requested movement coordination. |
| Walking gait/contact visibility | Walk scenario says silhouette in the wide and explicitly avoids detailed foot proof there; later says feet visibility is conditional. It does not identify a footfall/plant, weight transfer, or the exact interval where contact must read. Romance approach has no gait breakdown. | Existing 08-animation guidance mentions foot contact and weight shift, but the resulting plans did not consistently operationalize it for a moving walk or distinguish when gait evidence matters from when it can be omitted. Do not require visible feet in every shot; require a deliberate visibility/contact choice for a consequential walk/stop. |
| Action-phase cut continuity | All plans provide broad continuity rules. Cut triggers are qualitative (“after the stop is legible,” “after B is visible,” “cut while they continue,” “cut after A settles”) with no shared phase/frame marker or explicit phase carried across the cut. | Guidance supports continuity but did not yield an explicit action phase at cut-out and corresponding phase/state at cut-in. Minimal improvement is a cut continuity cue tied to action phase/state, not a new cut taxonomy. |
| Holds/reactions | The outputs include listening, recognition, eye contact, reaction and settle holds. None allocates a duration within a shot to each hold/reaction; the reaction is assigned a whole shot or left as “brief/quiet.” | Emotional holds are present but are not separately timed against the 30-second allocation. A concise hold/reaction time field or explicit allocation within each shot would help preserve the emotional beat in a short runtime. |
| Prompt feasibility | All outputs state camera/tool support is unconfirmed; romance labels camera directions as creative intent, and entrance offers mutually exclusive camera alternatives (“slow follow or static”). Walk output says separate clips if the chosen tool cannot sustain action/continuity, and directs checking tool controls. | The caution is appropriate, not a failure to claim execution. The actionable gap is conversion to a prompt-ready single choice per shot after tool constraints are known; until then alternatives should stay explicitly unresolved, not be treated as one final prompt. The probe cannot determine actual model feasibility. |

## Exact current guidance and minimal target paths

- `video-production-assets/references/25-reference-video-analysis.md:16-32,58-64` and `camera-motion-reference-analysis/SKILL.md:13-24` establish evidence, uncertainty, motion timing, and reference-analysis handoff; this baseline had no reference, so it tests proposed-planning application only.
- `camera-spatial-design/references/motion-timing-lens.md:3-10` establishes shared camera/subject timing; `video-production-assets/references/06-shots.md:10-20` and `video-production-assets/assets/06-shots-template.md:12-14` establish blocking and camera fields. Candidate timing/blocking addition belongs in these existing interfaces.
- `video-production-assets/references/08-animation.md:8-17` and `video-production-assets/assets/08-animation-template.md:8-10` establish pose timing, foot contact, weight shift, and contact locks. Candidate gait/contact visibility note belongs here.
- `video-production-assets/references/06-shots.md:15-20` and `video-production-assets/references/09-edit.md:9-18,43-57` establish movement definition, action continuity, and cut reasoning; `video-production-assets/assets/09-edit-template.md:14-16` holds action/camera change and cut data. Candidate outgoing/incoming action-phase cue belongs in these existing conventions.
- `video-production-assets/references/08-animation.md:11-14` and `video-production-assets/references/09-edit.md:10-12` address settle/timing and emotional reaction placement; neither template currently has a dedicated hold/reaction timing field. If later evaluation confirms this omission matters, the smallest structural place is `video-production-assets/assets/06-shots-template.md:12-14`, not a separate general template.
- `video-production-assets/references/11-ai-handoff.md:8-14` and `video-production-assets/assets/11-ai-handoff-template.md:8-18` require checking actual tool support and separating shot action/camera instruction from continuity; candidate prompt-feasibility clarification belongs there.

## Minimal additions justified by this baseline

1. In the shot/animation handoff, require a **shared shot-local seconds or frame basis** for subject action and camera phases when both move; include only relevant onset/change/reveal-or-contact/stop-settle/hold/cut points. This directly addresses the repeated prose-only synchronization.
2. For a consequential walk or walk-to-stop, record the **gait/contact visibility choice** (what contact/weight change must read, where/when; or why it need not be visible). Reuse existing foot-contact/weight-shift guidance; no universal step duration or mandatory foot-in-frame rule.
3. At a movement cut, identify the **outgoing action phase/end state and incoming matching phase/start state**, with eyeline/screen direction as applicable. Keep the existing continuity approach; no new schema is indicated by this small sample.
4. Within a short-form shot allocation, record **where the hold/reaction time sits** (or label it as part of the proposed shot duration). Do not prescribe universal hold lengths.
5. In AI handoff, retain the current feasibility caveat and require a **single chosen camera/action instruction only after checking the actual tool controls**; otherwise mark the alternative unresolved. No prompt-control claims can be validated without a specified tool.

## Limits

These three samples show what one model produced under these prompts and supplied context, not a stable failure rate or proof that the guidance causes the omissions. They justify narrow candidate changes for later consideration; archive analysis and any additional baselines may alter or reject them. No skill files were edited.