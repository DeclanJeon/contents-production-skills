---
name: storytelling-with-still-images
version: 1.0
description: Use when a user wants a video assembled from still photos, illustrations, storyboard panels, or evidence images with narration, dialogue, music, or sound—especially when they specify image-only visuals or no video-generation model.
---

# Storytelling with Still Images

## Principle

Stills are the only picture sources; order, hold time, reframing, transitions, and sound carry the story. “No video-generation model” bans generated footage, not assembling stills and audio into an MP4.

## Activate when

Use for new or existing still-image cuts, with or without audio. Use normal creative production for live-action or generated motion. If new stills are requested, use `codex-imagen`, not a video model.

## Workflow

1. **Lock the contract:** asset IDs/order, aspect ratio, runtime, dialogue to preserve, narration language/voice, subtitles, audio tracks/speakers, and exclusions.
2. **Bound the facts:** distinguish source-backed facts and speakers, interpretation, unknowns, and staged details. Keep suspicion separate from findings; do not invent why evidence differs. Keep provenance in notes unless requested on-screen. Never present reconstructed dialogue as a source quote.
3. **Inspect and map each still.** Missing or unclear image: use a generic ID, mark mapping “proposed—not inspected,” and do not describe unseen content. Possible evidence arc: discrepancy → context → act → consequence → testimony → investigation → outcome/reflection; adapt to the material. Give every hold a purpose. Repeat an evidence image at the end only as a meaningful callback.
4. **Write and time:** short lines, one idea each; remove source-meta wording and repetition. Preserve dialogue and approved wording. Assign recorded dialogue to a speaker only after confirming its track; otherwise narrate the fact without inventing a quote. Use one cue row per visual hold; match dialogue to the character image when possible and avoid overlap. Measure clip duration and pauses; mark estimates until audio exists. If a line exceeds its hold, extend/reallocate when runtime is flexible. If fixed, resolve the conflict instead of rushing speech or cutting preserved dialogue.
5. **Mix and assemble:** prioritize speech over BGM; keep narrator tone consistent, use sparse illustrative SFX, measure loudness/true peak. Assemble only approved stills and audio. Crops, pushes, cuts, and dissolves are allowed; generated footage is not. Honor the subtitle choice.
6. **Verify and deliver:** watch/listen when possible. Check facts, image order, speaker/timing, continuity, ending, runtime, dimensions, frame rate, codecs, audio, and subtitles. Encode/probe is not story QA; mark uninspected items unverified. For actual files, use `recording-production-history` and report path/checks. For planning only, return script and cue table.

## Cue-table contract

| Start–end | Still ID + observed content or “proposed—not inspected” | Exact speech | Sound / transition |
|---|---|---|---|
| Measured/estimated | Beat and purpose | Text/audio ID; silence | BGM/SFX, cut/dissolve/reframe |

One row per distinct hold; allocate the ending.

## Derived case pattern

In v7, five measured narration clips preserved existing dialogue. A 19.6-second ending extended the 49-second cut to 62 seconds; the evidence-comparison still returned beneath the closing question. Reuse the callback, not its durations or shot count.
