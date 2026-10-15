# Updated application assessment — 30-second romantic-fantasy drama

This assessment is separate from the verbatim responses in `qa/30s-romantic-fantasy-updated-application.json`. It compares those outputs with the baseline evidence in `qa/30s-romantic-fantasy-baseline-assessment.md`. It does not include archive conclusions or observations from reference footage; the prompts supplied no footage or named generator.

## Method

Three fresh, independent stateless `completion(default)` calls reused the same scenario prompts as the baseline: approach→stop→eye contact→reaction; offscreen entrance/reveal; moving walk→dialogue. The current changed planning references and templates were provided in model context. Outputs are planning proposals, not rendered or tool-feasibility results.

## Scenario findings

| Baseline issue | Updated output evidence | Outcome |
|---|---|---|
| Actor/camera co-timing | Romance plan now labels its shot ranges as proposed shot-local seconds and describes a track easing as the actor stops. Entrance plan says actor and camera timing should share a local basis once production timing is set. Walk plan uses shot-local seconds and couples tracking settle with actor stop. None lays down matched cue times for camera phase and actor phase within a shot; no output gives FPS/frame basis. | **Improved but still partial.** The outputs explicitly carry the shared-basis principle, but did not consistently instantiate the paired onset/change/reveal/contact/settle/hold/cut cues needed for a timed path. Keep the field conditional and make it an actionable cue annotation, not an arbitrary curve requirement. |
| Consequential walking contact / hidden feet | Walk plan says feet should remain visible through the stop if gait/contact is important; later states hidden/out-of-frame feet make contact unverified. It still gives no foot-plant or weight-transfer interval. | **Improved limitation handling; timing not demonstrated.** The outputs now distinguish contact evidence from unverified contact, but do not provide a timed gait/contact cue. Do not force feet into all frames. |
| Action-phase continuity at moving cuts | Outputs explicitly match Shot 1's continued walk into Shot 2, Shot 2's stop into Shot 3, preserve actor eyelines and positions, and ask to match Shot 3 listener pose/eyeline into Shot 4. No plan names an outgoing action phase and matching incoming phase/state in the edit entry. | **Partially improved.** State/pose continuity appears, but phase-paired cut notation did not reliably appear in the plans. Existing edit cue remains justified. |
| Reaction/settle allocation | Reactions and final holds are assigned to shot ranges (e.g. 18–24s and 24–30s; final 21–30s), and outputs say adjust after animatic/take review. They do not identify a distinct sub-interval for the reaction onset or settled hold within those ranges. | **Improved at shot-level, incomplete within shots.** The overall 30-second allocation can be reviewed, but short holds are not separately budgeted inside a shot. Keep that allocation optional and avoid prescribing a universal duration. |
| Prompt camera choice / feasibility | Outputs state camera moves are proposals and tool controls are unverified. The entrance plan explicitly labels pan/reframe and push-in/still choices as unresolved alternatives. The other outputs use one main proposed direction in several rows but still hedge with “if supported” or alternative framing. | **Feasibility boundary improved; execution choice remains unresolved where tool support is unknown.** This is correct for an unspecified tool; candidates must stay marked design-only until a real supported control is selected. No provider capability was tested. |

## What the updated probes support

- The prompts now elicit shot-local proposed time ranges rather than undifferentiated “seconds,” and explicitly distinguish proposals from reference observations or verified camera behavior.
- Walk-to-stop prompts surfaced the hidden-feet limitation as an unverified-contact status rather than treating occluded contact as proven.
- Shot-to-shot position, gaze, screen direction, action starts/ends, and reaction holds were stated more consistently.
- AI instructions remained conditional on actual tool support; the entrance result kept competing camera candidates separate from any claim of a final executable setting.

## Minimal next refinements, if desired after archive analysis

1. If full timed camera/action paths are required, ask the shot plan to write actual applicable shared-basis cue pairs (e.g. `subject stop` and `camera settle` on shot-local seconds or frames/FPS), not only to repeat that the basis is shared. Use a small selected set of relevant cues, not a mandatory phase checklist.
2. For an important walk/stop, give the required foot plant/weight-shift cue a local time or frame interval; otherwise state hidden/out-of-frame and leave contact unverified. The current visible/hidden distinction works but timing did not emerge.
3. Carry cut-out phase/end state → cut-in matching phase/start state into the edit plan itself. Current prose continuity descriptions do not instantiate the dedicated edit slot.
4. For reaction holds that materially consume runtime, budget onset/hold/settle as sub-intervals within the shot. Shot-level duration alone leaves actual hold time ambiguous.
5. When no tool has been selected, keep camera alternatives in the DESIGN_PROPOSAL area and make prompt camera instruction unresolved; after a tool is selected, the prompt should state one supported camera choice. No generator capability can be inferred from these text probes.

## Limits

Three single samples per scenario indicate observed behavior in this run, not a measured reliability rate or causal proof. Reuse of the same prompts and stateless calls makes this an application comparison, not proof of provider quality. No reference video or archive analysis informed these proposals, and no 3D/blocking visual inspection or AI generation was performed.