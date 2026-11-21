# Suno inputs by branch

These are writing patterns, not guaranteed syntax for musical timing. Check the live MCP tool schema and account grants before submission. The examples are drafts, not auditioned renders.

## Narration BGM — Custom instrumental

- **Style / `style`:** Minimal cinematic suspense underscore for spoken narration, around 82 BPM. Sparse muted piano over a low synth pulse. Keep the texture thin under the voice. Move from quiet curiosity to unease, then end cleanly with a short tail.
- **Instrumental / `instrumental`:** on / true. Omit lyrics and voice ID.
- **Exclude / `negative_style` (optional if supported):** whispering, choir, trailer brass.
- **Outside Suno:** Aim for a 30-second edit. Align the final accent with the reveal in the edit. Listen against the actual voice for intelligibility, unintended vocals, and a usable ending.

## Vocal song — Simple or Custom

**Simple / `description`** when the user wants Suno to propose the song: “Warm mid-tempo Korean indie pop about walking home after the last train, soft guitar in the verses and a brighter, singable chorus.” Do not also send `style` or `lyrics`.

**Custom** with fixed lyrics: put the supplied words verbatim in **Lyrics / `lyrics`**. Put “Close, restrained lead vocal, muted acoustic guitar in the verses, wider harmony in the chorus” in **Style / `style`**. Keep the story beat notes out of the sung text. Audition actual wording, pronunciation and chorus contrast.

## Sting or loop — Sounds

- **Sting:** `description` “Soft reverse swell into one muted tonal hit, short dry decay”; `loop: false`. Align the hit in the edit.
- **Loop:** `description` “Sparse brushed drum and muted bass bed, even dynamics, continuous unaccented texture”; `loop: true`. Supply tempo/key only if needed to fit existing music. Listen across consecutive repeats.
- The checked `sounds_create` declaration has `description`, `loop`, optional `tempo`, `key` and `title`; it does not expose duration. Length is model-chosen. Verify live account eligibility; if unavailable, return a Sounds prompt, not an automatic song substitution.

## MCP guardrails

- For songs, inspect `audio_create`. Its `description` and `style` are incompatible. For this workflow use separate clean Simple and Custom payloads. `negative_style` is conditional on caller-supplied style and permitted account controls; if unavailable, explain the gap and emphasize the wanted texture in the positive Style. A `voice_id` overrides instrumental.
- When present in the live schema, `duration` is a target (15–360 seconds at the time checked); strict mode caps rather than guaranteeing exact timing or a musical ending. Keep cut timing in the edit brief. Do not enable Max Mode by default.
- Snapshot (2026-11-21): current signed-in MCP declarations indicate two song outputs per call and two Sounds outputs per call. Verify the applicable cost and access before seeking execution approval; do not infer credit authorization from a production brief.

Official sources: [Simple](https://help.suno.com/en/articles/2462273), [Custom lyrics](https://help.suno.com/en/articles/2415873), [Exclude](https://help.suno.com/en/articles/3161921), [musical terms](https://help.suno.com/en/articles/9010177), [v6 controls](https://help.suno.com/en/articles/13924481), [MCP](https://help.suno.com/en/articles/14551361), [Song Editor](https://help.suno.com/en/articles/6141505).
