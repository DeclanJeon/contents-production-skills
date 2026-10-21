# F3 evidence closure

Scope: review-source-1.md camera findings L107–167. Local only; no tests/builds/lint/formatters, paid operations, uploads, remote create/deploy/publish, identity training, commits or global configuration changes.

| Defect ID | Action and evidence | Remaining limit |
|---|---|---|
| F3-D01 (review L115) | Changed `camera-spatial-design/references/camera-design.md:10,26`: retained headroom/leadroom, balance and tonal checks; bound them to directly read text with context and intentional departures preserved. | No fixed spacing ratios, exposure prescription, optical calibration, focus or DOF guarantee. |
| F3-D02 (review L129–133) | Actual two-depth-plus-middle synthetic camera A/B rendering, encoding, sampled image/video inspection and projection measurements below. | Fresh-model discrimination replay pending parent freeze; no full-rate playback claim. |
| F3-D03 (review L145–149) | Supplied separate CAM01 preservation and missing-number prompts using the actual existing example. | No independent transformation response claimed; parent replay required. |
| F3-D04 (review L117) | Timed 24-frame sequences with timing.json, exact sampled frames and encoded duration checks. | Does not extend prior CAM01 six-still evidence into full timed CAM01 playback or focus verification. |

Only production file changed: camera-design.md above. Other three owners intentionally unchanged: their existing observation, conversion and local execution boundaries already state the required behavior. New QA deliverables are under this directory. Package metadata unchanged; shared documentation/changelog integration belongs to parent.

## Direct source reads and entailment

F3 read Katz L317–333 through the reader, then reread the complete untruncated L319 with `:319-319:raw`. Load-bearing scope is only L319, Chapter 6 / The Close-up / Figure 6.2 explanatory prose. Exact printed page unresolved; the nearby L327 refers to Figure 6.4 p128, not proof of L319's page. This text supports customary gaze-side space, relative top/bottom space, comparing balance across neighboring shots, and departing from those conventions. It does not prescribe numeric headroom or mandatory off-center framing. No diagrams inspected.

Exact rendition: `E:/Book/06_Book/originals/콘텐츠_제작/md/Film Directing Shot by Shot Visualizing from Concept to Screen (Steven D. Katz) (z-library.sk, 1lib.sk, z-lib.sk).md`; 535607 bytes; SHA256 `e8ad5bf5ecc3659fb9b936dd081147a465b03ca09f53e6d690ca286fa4706e9a`; READ-PARTIAL.

F3 directly read Block L123–125 (pp61–62, Tonal Separation) and L183–185 (pp91–92, Reversing the Depth Cues). Supports qualitative brightness/depth cues and deliberately reducing/reversing them for flat space. Does not establish lighting ratios, calibrated optics or focus quality. No diagrams inspected.

Exact rendition: `E:/Book/06_Book/originals/콘텐츠_제작/md/The Visual Story Creating the Visual Structure of Film, TV, and Digital Media Third Edition (Bruce Block) (z-library.sk, 1lib.sk, z-lib.sk).md`; 368221 bytes; SHA256 `403172711929152d7019ccbab9043fc0ba8c512606fc14375ef6e78cc410392c`; READ-PARTIAL.

`package_evidence.py` actually computed both byte counts and hashes; output matched the installed identities. `source-identities.json` retains identities, not book passages. Canonical sources.md untouched.

## Actual local execution

Reproducible retained fixture source: `build_fixture.py`; separate ground truth: `ground-truth.json`. Analysis-facing media names and contact-sheet labels identify only A/B, frame and time; no motion identity labels. All shapes are synthetic static boxes, floor and background bars; no people/private assets. Scene uses Workbench, 320×180, 12fps, 24 frames per clip, fixed orientation, three depth planes. DOF disabled.

Commands run from checkout:

```text
"C:/Program Files/Blender Foundation/Blender 5.2/blender.exe" --background --factory-startup --python qa/skill-completeness-95/closure-F3/build_fixture.py
ffmpeg -version
python qa/skill-completeness-95/closure-F3/package_evidence.py
"C:/Program Files/Blender Foundation/Blender 5.2/blender.exe" --background qa/skill-completeness-95/closure-F3/fixture.blend --python-expr "import bpy; print('F3_REOPEN', bpy.app.version_string, len(bpy.data.objects), bpy.context.scene.render.fps, bpy.context.scene.frame_end)"
```

An initial PowerShell-style `&` command was rejected by the command parser before Blender started (exit2). Correct quoted executable invocation succeeded (exit0): `F3_FIXTURE_COMPLETE 5.2.2 LTS 48`; 48 PNG save messages and fixture.blend save. FFmpeg reported 8.1.2. Packaging exit0 encoded both H264/yuv420p MP4s, probed frame counts and wrote contact sheets, timing and measurements. Fresh-process reopen exit0: `F3_REOPEN 5.2.2 LTS 12 12 24`. Reopen loaded the installed BlenderMCP addon (registered/unregistered messages); no addon operation or configuration change requested.

Both ffprobe companions record 320×180, 12/1fps, 24 decoded frames, 2.000000s. Each encoded frame lasts 1/12s; final image PTS is 23/12 = 1.916667s, not 2s. Contact sheets show frames 0,4,9,14,19,23 at 0,.333333,.75,1.166667,1.583333,1.916667s. `media/timing.json` is the non-identity timing companion.

F3 actually opened both contact sheets and both MP4s with read. MP4 read returned six-frame preview grids and metadata, **not continuous playback**. No judgment of smoothness, shake, full timed playback or focus quality follows. Intervening images were rendered but not individually visually inspected.

Observed sampled images: orange left foreground box grows visibly more relative to the green middle and blue background boxes in A; their relative sizes change. B enlarges all three boxes and background bars together; apparent size ratios remain substantially stable. Both show foreground, middle and background throughout inspected samples, with left/right order retained. This is stronger than subject-only motion on a static grid, but sampled pictures alone do not exclude contrived independent object motion or post-crop.

Ground truth separately establishes A: camera world-Y translation from -8 to -5m, constant 32mm lens and orientation; B: constant camera position/orientation, 32→51.2mm lens. All subjects static. Projection center-height growth from first to last rendered configuration:

| Clip | Foreground | Middle | Background |
|---|---:|---:|---:|
| A | 1.557462 | 1.319868 | 1.208658 |
| B | 1.600000 | 1.600000 | 1.600000 |

These are computed projection measurements, not pixel metrology or a blind camera solve. Known fixture geometry permits attributing A's relative-depth change to translation and B's uniform magnification to lens change; an analysis model must state its own observed basis and alternatives without reading ground truth.

## Parent replay handoff

`smoke-prompts.json` contains five NEW supplemental scenarios: A/B discrimination, CAM01 exact source transformation, separate underspecified push-in, kitchen text plan and standalone no-generation boundary. These do not alter the frozen61. Prompts include only synthetic facts/requests; observable expected checks are separate. No original-book access is needed or permitted in replay; checkout camera-design.md contains bounded source bindings.

Parent should allow only relevant owner/ref and analysis-facing media reads for F3-MOTION-AB; exclude this report, fixture scripts, measurements and ground truth from blind inference. Required media reads must appear in the actual trace. A model that only sees grids must report sampled scope. Preserve actual final response and trace; tool errors, missing reads and empty finals are not PASS. No fresh-model invocation occurred in this employee lane.

Remaining exact gates: independent post-freeze replay and adjudication of all five scenarios; parent final-tree package checks/formal61 and source review. No score, 95% declaration, paid-success claim, calibrated optical claim or complete CAM01 timed-playback claim is made here.
