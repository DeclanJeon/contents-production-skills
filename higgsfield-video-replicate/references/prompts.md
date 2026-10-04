# Shot Prompts

One prompt per shot. STYLE and CHARACTER are byte-identical across every shot; only SCENE/MOTION change.

## Template

```text
CHARACTER: <locked descriptor — identical every shot; omit when no recurring character>
STYLE: <locked descriptor from the style bible — identical every shot>
SCENE: <setting + subject + the ONE action of this shot>
CAMERA: <shot size, angle, movement, lens feel, depth of field>
MOTION: <how the action unfolds over the shot's duration>
AUDIO: <clip-local sound, or "ambient only" when --generate-audio false>
NEGATIVE: <bans — see below>
```

## Rules

1. **Verbatim blocks:** STYLE and CHARACTER strings are copy-pasted, never reworded.
2. **Video reference changes the prompt's job:** with `--video-references` attached, the model already has the look — the prompt carries the NEW scene, subject, and camera intent. Do not re-describe the reference's grade or lens (same principle as image-to-image in `higgsfield-generate`).
3. One clear action per shot, completable within its 4–30s duration.
4. Under ~200 tokens. Long prompts distort.
5. English prompts always.
6. Positive phrasing for attributes (`tack sharp`, `locked-off tripod`); style bans live only in NEGATIVE.
7. Standard NEGATIVE tail: `no on-screen text, no captions, no watermark, no logos, no style drift, no documentary shakiness` — adjust only when the beat sheet calls for text/logos (then generate them as assets, don't ask the video model to spell).

## Worked examples

Reference: 43.5s photoreal "emotional chicken ad", 16:9, 24fps, park daylight.

```text
STYLE: photorealistic cinematic live-action, film emulation with gentle halation, shallow depth of field, teal-green shadows and warm skin tones, natural sunlight, subtle grain, 16:9
CHARACTER: young woman, long wavy bright red hair, round red-framed glasses, shiny red vinyl jacket
NEGATIVE: no on-screen text, no captions, no watermark, no logos, no style drift
```

**Shot 1 (0–7s) — hook**

```text
CHARACTER: <as locked>
STYLE: <as locked>
SCENE: A young woman stands alone on a sunlit park lawn, seen in profile, looking off-frame as blurred picnic-goers rest in the background.
CAMERA: medium close-up profile, static tripod, 85mm feel, very shallow focus with soft bokeh.
MOTION: she holds still and breathes slowly; a faint breeze moves her hair.
AUDIO: ambient only
NEGATIVE: <standard tail>
```

**Shot 3 (14–21s) — picnic beat**

```text
CHARACTER: <as locked>
STYLE: <as locked>
SCENE: An older woman and an older man sit at a park picnic table, each biting into a sauced fried chicken drumstick beside an open cardboard chicken box and small side dishes.
CAMERA: two-shot at table height, static, 50mm feel, shallow focus on the pair.
MOTION: they take a bite, glance at each other, and chew with small satisfied nods.
AUDIO: ambient only
NEGATIVE: <standard tail — plus: no readable brand text on the box>
```

**Shot 5 (28–35s) — payoff**

```text
CHARACTER: <as locked>
STYLE: <as locked>
SCENE: On a grassy hill overlooking a hazy city, a golden-haired man in an ornate gold feathered costume embraces the red-haired woman; a lone figure crouches in the far background.
CAMERA: medium two-shot, slow subtle push-in, 35mm feel, shallow focus.
MOTION: he pulls her into a hug; she settles against his shoulder and looks toward camera.
AUDIO: ambient only
NEGATIVE: <standard tail>
```

Repeating beats (same scene type) vary only SCENE and MOTION — never STYLE/CHARACTER/CAMERA language that defines the film's look.

## Prompt → CLI

Each prompt feeds one Phase 3 invocation (`--prompt "<prompt>"` in the gate-chosen model's command shown in SKILL.md — example there uses `seedance_2_5 --mode omni_reference`). Keep a numbered `prompts.md` scratch file with `Shot 1..N` labels so job UUIDs map 1:1 to shots.
