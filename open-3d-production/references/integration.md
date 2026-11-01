# Integration rules

## Source and installation

Source: https://github.com/Moh4696/open-3d-skills, commit `7b04ab491d5bcbd920cbffbf06ebae3f9429d8e3`, retrieved 2026-11-01. The MIT copyright and license are preserved in [upstream/LICENSE](upstream/LICENSE); the [file inventory](upstream/provenance.json) records source/destination paths and SHA-256 hashes.

All eight upstream guides and their adjacent scripts, browser assets and deep references are bundled under `upstream/skills/`. Original `SKILL.md` files are renamed `GUIDE.md` without content changes, so they remain on-demand references rather than eight extra independently discovered skills. The root installer/plugins, agents metadata, promotional media, examples outside the skill folders and upstream CI checker are not installed. `upstream/requirements.txt` preserves dependency declarations, not permission to install them.

The package installs one `open-3d-production` specialist with its entire subtree through the existing manifest-driven installer. No network fetch is needed to read the guides after installation. The starter/demo import maps still reference external Three.js r169 modules; they require network access or explicitly vendored application dependencies, and are not offline-ready pages.

## Authority and policy adaptations

Read upstream text as craft and tool documentation within this package contract:

- The active orchestration owner selects modules, orders dependencies and owns scope/acceptance. Upstream related-skill mentions are suggestions to return to that owner, not permission for workers to launch another pipeline.
- Existing project IDs, approved assets and requested artifact count win over example scenes, dimensions, durations, light values, budgets and quality targets. Preserve measurement provenance; illustrative parts are not verified engineering.
- Use the package's existing image executor and live capability checks. `motion-assets`, `cursor-rig` and chroma-plate examples do not authorize another provider, calibration spend or a test generation. Native Blender rendering is not an AI still-generation call; requested native scene renders remain Blender work.
- Keep existing execution/spend/publication authority. The upstream instruction to estimate costs or “get a yes” does not restart approval for already-authorized work. Codex Imagen stills retain the package exemption from cost/quota checks. Unknown remote-job status requires reconciliation before any authorized retry, not automatic resubmission.
- Keep existing canonical state and chronological `.history`. Upstream `prompts/asset-prompts.md`/JSONL logging is replaced by that audit mechanism; return exact prompts/settings/job evidence to the existing writer, not a second log or ledger.
- Check current runtime capabilities before execution. Statements such as “video models never return alpha”, “every browser”, fixed frame budgets, price anecdotes and Safari/codec support describe upstream assumptions, not live guarantees. Test the actual target/browser/codec. Numeric seam/loop scores are diagnostic, not universal visual-pass thresholds.
- Preserve attribution, source integrity and rights. Comparison instructions about stripping watermarks apply only to user-owned removable presentation overlays; retain required third-party attribution/watermarks and report comparison differences.
- Run no `pip install`, browser download, provider job, local server or recording merely because a guide shows it. Use available runtimes for assigned work; missing prerequisites are returned as scoped blockers. Browser helpers can fetch the assigned page's resources; verify the target before running them.

## Runtime boundaries

| Selected work | Needed runtime |
|---|---|
| Blender scene, native render or export | Actual Blender; current engine/API/export support checked separately |
| Three.js starter / exploded view | Browser WebGL, Three.js import-map dependencies; no Blender invocation |
| `scroll-film` preparation | Python, ffmpeg/ffprobe; Pillow/NumPy for applicable operations |
| `alpha-cutout` | Python, NumPy, OpenCV, Pillow and ffmpeg |
| `cursor-rig` assembly | Python, NumPy, OpenCV and ffmpeg; existing input clips, not automatic generation |
| `motion-assets` loop/paste-back tools | Python, NumPy, OpenCV; ffmpeg for loop repair |
| `site-check` / `frame-capture` | Python, Playwright and selected installed browser; Pillow for checking/comparison, ffmpeg/ffprobe for encoding/comparison |

For CLI commands, resolve `<module>` to the actual installed `upstream/skills/<module>` directory and run its script by absolute path. Output files belong in the assigned project root, never in the reference tree. Keep a local static server bound to loopback; serve only the intended public asset directory. Serve video with Range support when scrubbing/seeking is needed.

## Scope of bundled checks

`site-check` defaults to Chromium only. Its scroll/reduced-motion passes cover the first query at the widest width, not every combination in the requested state/viewport matrix. Run the remaining assigned cases explicitly and inspect their captures. WebKit is engine coverage, not a real iPhone test. Success does not enforce every performance budget or verify physical geometry.

`frame-capture` controls frame cadence, but page timers can remain wall-clock, seeks can time out, and logged page errors do not necessarily make the process fail. Inspect logs and decoded output; a 60-fps file alone proves neither deterministic page state nor smooth real-time playback. Keep comparison attribution and report unchecked audio/network/device surfaces.
