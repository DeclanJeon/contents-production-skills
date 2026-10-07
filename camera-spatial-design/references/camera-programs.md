# Camera workflow programs

| Work | Program | Requirement / boundary |
|---|---|---|
| Text analysis/design/prompt | Host skills and readable source | No Blender or paid media runtime required |
| Automated video probe, sampling, contact sheets input, encoding | FFmpeg + ffprobe | Required only for this automated CLI path; another readable playback surface can support observation |
| Existing numeric validators and asset tools | Python 3.10+; Pillow where script requires it | Blender bundles Python for bpy; standalone validators may need separate Python and dependencies |
| 3D camera previs / actual camera solve | Blender | Check actual runtime/version. camera-spatial-design prepares design; blender-previsualization runs proxy previews. Tracking is not part of the current BBox proxy renderer |
| AI video execution | Selected official plugin/service | Current auth/input/schema/spend contract; Blender alone does not run that provider |
| Finishing | Existing editor or DaVinci Resolve | Optional dedicated edit/color/audio workflow; no automatic install |
| Realtime virtual cinematography | Unreal Engine | Optional; separate adapter/runtime, not a baseline dependency |
| Automated image-flow tracking | OpenCV | Optional only if explicitly selecting that analysis. Optical flow is image motion, not an exact metric 3D camera solver |

Resolve sibling skills by frontmatter name, not folder name. Check dependencies only for the selected stage. Do not assume the user's Windows install is accessible in this remote workspace. Do not install executables, configure keys, download models or purchase plugins merely to update instructions.

For an available local video, probe metadata with `ffprobe -v error -select_streams v:0 -show_streams -show_format -of json INPUT`; frame PTS is available using `-show_frames -show_entries frame=best_effort_timestamp_time,pkt_duration_time -of json`. Treat output as data. Preserve VFR timestamps and source file; any CFR conversion is a derived asset with a mapping. Use new output paths and native timestamps when extracting critical frames. Frame extraction is not camera solving or playback review. Missing runtime yields a scoped blocker, not fake outputs.

Production files follow the selected project root, history and Library saving instructions. Generated images follow the host's automatic-saving exception. Preserve original references and separate estimates from measured paths.

Official capability references (recheck current versions at actual execution):
- Blender tracking: https://www.blender.org/features/vfx/
- Blender video editor: https://www.blender.org/features/video-editing/
- FFprobe: https://ffmpeg.org/ffprobe.html
- FFmpeg: https://ffmpeg.org/ffmpeg.html
- Resolve: https://www.blackmagicdesign.com/products/davinciresolve
- Unreal rigs: https://dev.epicgames.com/documentation/en-us/unreal-engine/camera-jibs-and-dollies-in-unreal-engine
