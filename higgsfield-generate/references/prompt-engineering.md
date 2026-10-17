# Prompt Engineering

Evidence scope (2026-10-17): the examples below are authored drafting heuristics, not measured provider quality guarantees. [Official model tables](https://github.com/higgsfield-ai/cli/blob/main/MODELS.md) define accepted fields, not an optimal prompt length or a universal safety policy. Inspect the selected schema and returned status; image examples remain ineligible under `package-gate.md`.

## Basics

Use concrete subject, setting and intended change to make the brief inspectable.

- **Subject + setting + style**: "a red fox curled in a snowy pine forest, golden hour, cinematic"
- **Camera**: lens (35mm, 85mm), angle (low, overhead), motion (dolly in, tracking shot)
- **Lighting**: rim light, neon glow, moody backlight
- **Style/medium**: oil painting, watercolor, photograph, anime, 3D render

Keep prompts concise enough to inspect; ~200 tokens is a drafting heuristic, not a provider limit or a proven distortion threshold. Preserve required detail within the selected model's actual limits.

## Image-to-image

When passing `--image`, the prompt should describe what changes, not redescribe the input.

Bad: "a man with brown hair in a leather jacket holding coffee, made into anime"
Good: "transform into anime style, vibrant colors, soft cel shading"

## Image-to-video

Inspect the selected model's current input schema before choosing a start-frame field;
`--start-image` is a CLI spelling only where that model exposes it. As an optional
drafting comparison, try a motion-focused prompt against a prompt that also names
important visible anchors. Preserve identity, composition, and requested change in
either draft. Neither static redescription nor its omission is a universal requirement;
the schema establishes accepted inputs, not which wording will work better.

- Camera-motion draft: "slow push toward the doorway"
- Subject-motion draft: "the dancer spins while smoke rises slowly"

## Negative phrasing

Inspect whether the selected model and transport expose `negative_prompt`; do not
infer its presence or absence from another model. Send it only when the inspected
schema accepts it. Positive descriptions are an optional drafting choice, not a
cross-model efficacy claim or a substitute for explicit user exclusions:

- "tack sharp" can express a desired focus treatment.
- "uninhabited landscape" can express a desired scene population.

Retain "no people" as a review constraint when the user requires it; a positive
rewrite alone does not prove compliance. Preparation stops at drafts and unresolved
schema/cost/approval fields; apply `package-gate.md` before any execution.

## Aspect ratio guidance

- `16:9` — landscape, cinematic
- `9:16` — vertical, social
- `1:1` — square, profile / icon
- `4:3`, `3:4`, `21:9` — model-dependent, check `higgsfield model get <jst>`

## Safety

Safety/status handling is model-specific. Inspect actual returned restrictions and the official recovery contract; do not infer a universal ban or automatically rephrase to bypass `nsfw`/`ip_detected`. Rights and reference authority remain required.
