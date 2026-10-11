# Expression–voice bridge: behavior → acting, speech, vocal direction

Read for any expression or voice handoff. Converts each persona rule into observable/audible instructions the next executor (sheet, prompt, voice selection) can use. Text only — no generation or spend authorized.

## Bridge table

For each core rule, fill the columns the assignment needs:

| Ground/rule | Behavior | Expression · posture · gesture | Speech style | Per-scene vocal direction | Keep · exclude |
|---|---|---|---|---|---|
| This character's value/intent | Observable reaction | Executable visual performance | Lexicon, sentence shape, silence use | Stress, pace, attack, breath | Identity locks and forbidden readings |

Rules:

- Derive **nothing** about eyes, jaw, body, skin, gender, nationality, pitch, or timbre from a type label. Persona expresses through expression, gesture, prop handling, and acting. Locked appearance stays locked; new appearance proposals need their own grounds and delegation.
- Every visual cue must be filmable — a posture, a handling of an object, an eye-line choice — not an internal state label.

## Voice Identity (fixed layer)

The design by which this voice is recognized, stable across scenes:

- baseline register; timbre/roughness/breathiness; resonance *impression* (acting shorthand, not measurement); articulation and sentence-end habits; baseline rhythm;
- **auditory anchors** — the two-or-three cues a listener uses to know it is them;
- **allowed variation range** — what may bend under state changes and what must not.

Timbre is never selected from type. Ground it in the brief, supplied audio, cast differentiation, or an explicit labeled proposal. Contrast is allowed (a bright voice hiding unease) as a design choice, never as a type's inevitable trait. Invent no precise Hz/rate/resonance figures.

## Speech Style (habit layer)

Sentence length, lexicon, question/command/indirection preferences, honorifics, humor, use of silence, and per-relationship register shifts. Supplied-only language/dialect contract applies.

## Performance (per-line layer)

For each delivered line: exact text, intent, subtext, emotional pressure, stressed words, pauses/breath/pace shifts. Pressure is **not a new voice** — state which timbre/articulation anchors hold and which performance variables move. Reusable `voice_identity_direction` and per-line `performance_cue` stay separate; executors get speaking rules, not type names or backstory dumps.

## Realization boundary

At execution time, confirm the actual tool's voice list, supported languages, reference-voice support, instruction/emotion-tag/rate controls, rights/consent, and cost. Unsupported controls come back as named gaps — never claimed as applied. `voice_profile` handoffs must reference the exact SSOT artifact version; a stale pin is refused for current execution, with downstream assets restaled only along the real dependency graph. Text direction, seed, or a repeated voice_id alone do not guarantee identical output — continuity is verified by the approved listening procedure, which lives outside this skill.
