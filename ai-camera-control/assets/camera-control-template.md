# AI camera control packet

- Shot / scene / beat / panels:
- Camera-language catalog IDs / camera-intent artifact ID and version:
- Input camera specification and asset IDs/versions / file-section or supplied-text locator:
- Duration / FPS basis / aspect / coordinate convention / units:
- Approved scope / provider or model-neutral:
- Lens / effective gate / move onset-stop / unresolved design slots and owner:

## Prompt
Scene; subject action; camera action; timing/reveal; lens/focus; continuity.

| Requirement | Intended value | Verified tool field | HARD_CONTROL / SOFT_PROMPT / UNSUPPORTED / UNVERIFIED | Evidence / limitation |
|---|---|---|---|---|

## Reference roles
One row per attached slot (e.g. `@image1`, `@video1`, `@audio1`), the slot tag actually sent, and the source file/asset ID + version. Import the attribute this slot owns, exclude the attributes it must not contribute, and name the priority rule for conflicts. A character sheet slot owns face/body/costume but not pose or background; a previs slot owns camera, cut and blocking but not proxy face, body shape or plastic look; a previous clip slot owns the real end state, held prop, costume and travel direction but not a replayed action or its original sound. If no file is attached, the slot does not exist and no tag is written.

| Slot tag actually sent | Source asset ID/version/file | Attributes to import | Attributes to exclude | Priority on conflict |
|---|---|---|---|---|

## Action beats (shot-local time segments)
Split the shot into the time segments the story actually changes in (e.g. 0–2s, 2–5s, 5–7s, 7–8s) and record, per segment, the subject action, the camera state, the new information or emotion, and the cut/settle point. Time segments use the shot-local basis of the spec (frames or seconds with the FPS stated), never the final edit timeline. A camera that must stay fixed for the whole clip is written once as fixed, not re-described per segment.

| Segment (local time basis) | Subject action | Camera state | New information / emotion | Cut or settle |
|---|---|---|---|---|

### Camera schedule carried into the final prompt

One take means one continuous shot, not one locked framing. Link required medium/close/reaction compositions and motivated moves to the actual final request. Brief purposeful settles are allowed; an all-wide/static replacement requires explicit approval when it removes required coverage. A generation job, scene, shot and framing segment are not interchangeable.

| Source shot/panel ID + version | Local interval / time basis | Start framing + visible subject | Trigger -> move -> target | Deceleration / settle -> end framing | Exact final-provider-request clause | Control status / limitation |
|---|---|---|---|---|---|---|

Missing required rows or clauses, reveal-order changes, contradictory global locked-wide instructions, or a cut disguised as a no-cut transition are FIX / submission blocked. Distinguish physical dolly/truck/arc, pan/tilt, optical zoom and focus pull. A SOFT_PROMPT must remain explicit, not be deleted for lack of hard control. Do not claim unrendered geometry or generated motion is verified.

## Preservation constraints (do-not-change)
List what must survive the generation: identity and costume, prop state and hand ownership, an already-established room or set layout, light direction, the screen-direction/axis anchor, and a motion that must continue instead of restarting. Every entry names the constant, its source (shot/beat/panel ID or approved reference), and how it is checked against the approved frame. A negative instruction never replaces a positive plan: if a thing must not change, the thing that does change in that segment is stated in the beat table above.

| Constraint (what stays constant) | Source ID | How it is verified after generation |
|---|---|---|

## Audio and dialogue (separate channel)
Dialogue, SFX, ambience and music are edit-timeline items with their own cue IDs and timing. Record them here only as an execution constraint, not as visual action: a sound cue does not describe a visible move, and "on the beat" is not a visual instruction. If the selected provider exposes an audio field, list it in the provider table with its verified field name; otherwise mark it `UNSUPPORTED` and hand it to the edit owner. Generated sound is not evidence that the visual action happened at that time.

For a verified native-audio model, this separate AUDIO section travels inside the same provider request. Do not infer an extra dubbing job or invent an audio toggle/reference field the current transport does not expose.

## Actual provider inputs
Include only supported fields; leave empty for model-neutral work.
For every selected catalog directive, map the intended result to a verified provider field or mark it `SOFT_PROMPT`, `UNSUPPORTED`, or `UNVERIFIED`. Do not translate a catalog label into invented numeric motion, duration, lens, or path values.

## Acceptance and revision
Start/end framing; reveal/contact timing and supplied/proposed tolerance; motion/spatial continuity; actual clip version/evidence time; minimum revision/affected dependents/scope change. Every reference slot is bound to a real file/version with import/exclude attributes, every preservation constraint names a constant and its verification, and every action beat carries the local time basis it was written on.
