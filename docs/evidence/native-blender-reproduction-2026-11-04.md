# Native Blender reproduction execution evidence

Project outside this repository:
`/home/declan/Documents/studio_production/architecture-reference-2026-11-03`.

This records observed execution, not a universal similarity claim or approval
of complete visual imitation. No source video frames were used as architectural
render planes or material textures. No commits, publication or paid calls were
performed in this continuation.

## Executed production

- Blender 5.2.2 LTS, native mesh/curve/material animation, EEVEE.
- 1280x720, 30 fps, 900 output frames; original excerpt seconds 207–237.
- Separate native unit scenes retain their own lighting/worlds in a packed
  scene-strip master. ASS captions and borrowed source narration are explicit
  external edit layers, not hidden source-footage substitutes.
- Body renders and transparent graphic passes use per-frame checksums,
  source-scene fingerprints and single-writer locks.
- The first shot reuses lift frames 1–31 and roll frames 32–242 rather than
  redoing completed work. Doorway frames 403–655 completed all 253 frames.
- Construction frames 243–402 completed 160 frames; vibration 656–900 completed
  245 frames. Subsequent material changes rerender only the affected unit.
- Measured annotation vectors are explicitly graphic reconstructions, not
  evidence of recovered engineering dimensions or physical force simulation.

## Actual verification

`matching-v004/full-review-v006/final-audit.json` records:

- Both delivered videos: exactly 30 seconds, 900 frames at 30 fps; complete
  decode without errors.
- Audio packet hash equals the borrowed reference audio exactly:
  `65b9845e919da8dd526c0a67198fa1b0d1ee5e9dc845fc9f54246cd982dfbef3`.
- Packed master v006 reopened with 26 native scene strips, no uncovered body
  frame, packed external fonts and zero image texture nodes.
- All 12 whole-timeline sample sheets and seven cut-boundary sheets were
  inspected. Later changed-frame comparisons were inspected separately.
- Weak-wave refinement: all 226 unmodified vibration frame fingerprints
  identical; 19 changed frames order-stable and unoccluded.
- Foil correction: restoring the one declared emission socket makes all 245
  evaluated geometry/camera/material fingerprints equal to the prior baseline.

The actual native master SHA-256 is
`2b6f04db2b76832baf99ff056189ad72beffccf1a76a3107f7e65f04ba54ed6d`.

## Corrections driven by visual inspection

- Fixed an inherited preview-resolution setting that centered construction
  at half-size inside the native scene-strip master.
- Fixed an outgoing dissolve hold whose camera was overridden by a timeline
  marker; the outgoing pose is now frozen before that marker.
- Removed a superseded ASS compression-arrow proxy that doubled the native
  force arrow.
- Restored the measured red joint trace without rerendering unchanged bodies.
- Replaced broad-bloom skeletonization with a local green-channel ridge in
  the weak-wave interval, reducing false branches.
- Removed artificial foil self-lighting that appeared as a bright foam strip.

## Runtime API observations

On the actual executable, compositor `ShaderNodeMath` is supported;
`CompositorNodeMath` is not. `CompositorNodeSetAlpha` uses its `Type` menu socket
(`Replace Alpha`), not a `.mode` property. These were verified by constructing
nodes and rendering, rather than inferred from an unrelated installed package.

## Limits and current status

Native project and audited v007 media exist. V007 changes only inspected title
hierarchy and measured dimension graphics. Its complete decode, 900-frame
timing, exact audio equality and actual encoded annotation frames were checked.
The local history contains a real started/completed operation for this assembly;
that does not close the ongoing strict visual-matching operation.
The current pointer is `matching-v004/CURRENT.json`; the current media hashes
are in `matching-v004/full-review-v007/final-audit.json`.

Wood/aggregate/mortar texture and some geometric detail remain approximations.
Source numeric glyphs are not independently validated dimensions.
Strict visual matching remains open; file integrity does not close it.
Wayland desktop capture reported no display/capture capability, so continuous
desktop playback was not observed. Decoded timeline samples are not mislabeled
as a fully watched playback.

Actual configuration, source measurements, scripts, rejected attempts and
resume evidence remain in the external project. Earlier missing history events
were not backfilled with invented timestamps.
