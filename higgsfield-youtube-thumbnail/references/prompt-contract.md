# Thumbnail prompt contract and render recipes

Load before composing any render prompt. The doctrine below is craft — executor-agnostic.
In this package Higgsfield image jobs are ineligible (see SKILL "Package gate"): apply the
same prompt contract through the explicitly authorized eligible image executor (`codex-imagen`
default), and keep the preserved CLI shapes as reference for contexts where they are
permitted. A "retry" inside the preserved CLI notes is a workflow limit only — the approved
bounded retry/cost scope governs.

## Prompt contract

Assemble every main-render prompt in this order:

1. **Frame:** `Bold, punchy YouTube-thumbnail composite — poster-grade, photoreal and high-impact, NOT a muted cinematic movie still, <ratio>, single unified frame — no split-screen, no diagonal divide, everything blends smoothly and organically across the same continuous shot.` For `9:16`, add `faces in the upper two-thirds`. A requested graphical representation replaces photoreal language with a clean diagram/graphic brief.
2. **Scene brief:** depict the user's exact content.
3. **Text:** default `No text, no readable UI labels, no watermark.` For explicit baked headline: `TEXT: bold thumbnail headline text baked into the image, reading exactly "<TEXT>" — massive, ultra-legible sans-serif with a clean outline/glow treatment, placed where it never covers the subject's face. No other text, no watermark.`
4. **Subjects:** large, foreground-dominant, chest-up or medium-close, filling about 40–60% of the frame. End with `All faces crisply sharp as the anchors of the shot.`
5. **Key elements:** only signature props/effects that explain the information gap.
6. **Logo:** preserve exact shapes, colors, proportions, and letterforms; keep it away from faces.
7. **Location:** place, time, weather, and atmosphere when relevant.
8. **Composition:** one power-third hero, clear scale hierarchy, depth, and strong subject/background separation.
9. **Background:** vivid high-contrast color field or environment, soft vignette and edge falloff; do not divide it unless a split layout was explicitly requested.
10. **Lighting on people:** `signature YouTube thumbnail lighting rig — strong key light sculpting the face, soft dreamy fill lifting shadows, and defined back light plus hair light tracing a clean bright rim around hair, shoulders and silhouette.` Only the rim may use a colored accent.
11. **Grade:** vivid, bright, glossy, poster-punchy, deep blacks, crisp highlights, rich saturated colors, cohesive as one image. Restrain it only for an explicit calm/premium/muted brief.

For each photo-referenced person, include:

```text
CHARACTER N: the person from attached face reference #K — IDENTITY LOCK: reproduce
this exact person with a photographic identity match — same bone structure, eye shape,
nose, lips, jawline, skin tone, hairline and hair texture. Do not beautify, average,
or restyle the face. Expression: <emotion phrase>.
```

### Split layouts

Use a split only when the user asks for `split`, `before/after`, `versus`, `side by side`, or the analyzed reference is split. A topical phrase such as `X vs Y` does not itself require a split. Replace the normal frame block with a clear halves/panels contract and keep all labels out unless short, truthful baked UI was explicitly requested.

## Optional 3D logo

First create a 1:1 4K logo render, then use its completed job ID as the last `--image` on every thumbnail call:

```bash
higgsfield generate create gpt_image_2 \
  --prompt "Transform the attached 2D logo into a premium 3D logo render: extrude the exact logo shapes into glossy dimensional volumes; preserve every letterform, proportion and brand color; soft studio reflections, subtle bevels, crisp edges, clean dark neutral background, soft contact shadow, centered, generous margins, no extra text, no watermark." \
  --image ./logo.png \
  --aspect_ratio 1:1 \
  --quality high \
  --resolution 4k \
  --wait --json
```

## Main render

Use Nano Banana Pro at explicit 4K. Write the final prompt to a temporary text file and pipe it on stdin so punctuation and multiline blocks are preserved safely:

```bash
higgsfield generate create nano_banana_pro \
  --aspect_ratio 16:9 \
  --resolution 4k \
  --image ./face-1.png \
  --image ./logo.png \
  --wait --json < thumbnail-prompt.txt
```

Omit all `--image` flags when there are no references. For a variant set, make one call per distinct prompt. Keep the same references and settings; vary only the selected concept, expression, or camera-take line.

The completed JSON result contains `id` and `result_url`. Preserve both privately: the URL is delivered; the ID is the source for later edits.
## Surgical tweaks

Use the picked completed job ID as the only image input. Keep the edit prompt narrowly scoped and state that every other pixel-level property remains unchanged.

```bash
higgsfield generate create seedream_v5_pro \
  --prompt "Change ONLY the person's facial expression to: <phrase>. Keep identity, face structure, hair, pose, body, clothing, logo, background, lighting and composition EXACTLY unchanged, pixel-faithful. Keep the YouTube thumbnail lighting rig intact." \
  --image <picked_job_id> \
  --aspect_ratio 16:9 \
  --resolution 2k \
  --wait --json
```

If `seedream_v5_pro` is absent or rejects the submit, retry once with `seedream_v4_5 --quality high`. For a `4:5` main render, Seedream has no `4:5`; ask before changing the edit to `3:4`, and disclose the crop/ratio change. Each accepted edit becomes the source ID for the next tweak.

CLI compatibility: versions through `1.1.20` can mislabel a `nano_banana_pro` job reference as `nano_banana_pro_job`. If the edit is rejected with a `medias.0...data.type` error, download the picked `result_url` to a local image and retry the same edit with `--image ./picked-thumbnail.png`. A local path is auto-uploaded as `media_input`; do not retry the invalid job-id payload.

Allowed tweak scopes: expression only, background replacement only, background recolor only, or rim-light recolor only. Never silently regenerate the full composition for a surgical request.
