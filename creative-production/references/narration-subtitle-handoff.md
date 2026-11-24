# Narration and subtitle handoff

`creative-production` remains the sole coordinator and project writer. This is a conditional craft assignment, not a new route, ledger, or authorization.

## Select by request

- **Narration direction:** map information and emotional beats into a performance brief. Keep spoken words, display captions, pronunciation, breathing, pace, emphasis and emotional turn separate. Preserve the approved speaker and wording. For explicitly narration-first shorts use `narration-first-viral-shorts` when available; its specialist format does not apply to every video. Use the [audio cue handoff](audio-production-routing.md) only when a separate audio asset is needed.
- **Basic captions, lower thirds, placement or supplied SRT:** retain [caption layout](../../video-production-assets/references/23a-captions-layout.md) and existing delivery rules. Do not open the advanced engine just because a caption slot exists.
- **Analysis-led subtitle redesign, typography/color/motion direction, or requested specialist render:** resolve the optional `shortform-subtitle-direction` by exact installed skill name or a known authorized source checkout. In the local sibling project the entry is `subtitle-direction-skill/03_스킬/SKILL.md`; resolve from the package checkout, not a presumed user home. Preserve that entry's relative references and read its session contract. Do not automatically install or copy its engine, fonts or recovery tree. If missing, give the basic text/layout proposal and flag specialist work unresolved; no silent downgrade of mandatory motion or render.
- Respect no-caption and no-audio independently. Do not add unrequested speech, transcription or captions.

## Packet and timing lock

Carry the current script/edit versions, cue/shot/beat IDs, target canvas/platform and safe zones, purpose and language, spoken/display text pair, pronunciation exceptions, and any required expression or typography constraints. Attach the chosen authorized take's identifier/hash and actual duration if available. Mark every timing set as estimated or aligned to the actual take and edit version. Never present ASR guesses, frame samples or planned durations as verified timing or listening. A new take/edit invalidates only its dependent timecodes, previews and render approval. Preproduction returns proposed text and requirements only.

## Local timing draft

Open this path only when authorized local speech media is available, captions were requested, and usable timing for the current edit is missing. Use supplied verified cues if they already match. If there is no actual take, label the timing provisional and do not infer word times from script length.

1. Keep the actual take and edit version fixed. For Korean speech, use an already available local [faster-whisper](https://github.com/SYSTRAN/faster-whisper) runtime and model with Korean selected when known. Keep the raw ASR transcript and its time basis separate from the approved display text. Do not install, download models or upload the take as an implicit fallback.
2. Use an installed [WhisperX](https://github.com/m-bain/whisperX) alignment path only when the deliverable needs word-level timing and the language model and dependencies are already available and compatible. Mark unaligned spans unverified; keep phrase-level cues if the requested format allows them, otherwise report the gap. Do not invent word-level timing.
3. Reconcile names, particles, numerals and line breaks against the approved text and what was actually said. Compare the cue boundaries with actual playback of the locked edit and check that speech is not clipped and the cues do not drift. Keep unresolved or unchecked cues provisional. Pass the reviewed cues into the existing delivery or specialist-render path; ASR does not replace it or authorize rendering.

## Execute and check

For the advanced engine, check the source, actual CLI, FFmpeg/backend, target renderer compatibility and fonts when needed. Keep source video unchanged. Compile, preview and export require that engine's current plan-hash approval; the scope of the production request does not replace it. Report whether frames were actually rendered and inspected separately from CLI/test success. Verify actual playback for wording, pronunciation, readable line breaks, type/contrast, safe area, face/UI overlap, cut timing and speech intelligibility under music. Keep unresolved items in the existing production record; only the coordinator adopts the output.
