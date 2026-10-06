---
version: 0.17.0
name: higgsfield-soul-id
description: |
  Train a Soul Character — a personalized model on a person's face that
  Higgsfield uses for identity-faithful image and video generation.
  Use when: "create my Soul", "train my face", "make my digital twin",
  "build me an avatar", "learn my appearance", "create a character of me",
  "set up identity for video", "I want my face in generated images".
  Chain: train Soul (one-time, returns reference_id) → use in
  higgsfield-generate via `--soul-id <id>` with models like
  `text2image_soul_v2` or `soul_cinematic`.
  NOT for: one-shot face swaps (use higgsfield-generate with --image),
  named-character / non-photo avatars (use higgsfield-generate with prompt).
argument-hint: "[name] [photo paths...]"
allowed-tools: Bash
---

# Higgsfield Soul Character

Train a face-faithful identity model. Reusable across all Soul-powered generations.

## Scope and package gate

`creative-production` is the project-level coordinator when one exists; this skill owns the Soul training lifecycle only — not image generation, character sheets, or ordinary boards (those never load this skill). Delegated work follows `../higgsfield-generate/references/package-gate.md`: reuse the supplied name/photos/variant, return the trained `reference_id` as a **provider locator mapped to the canonical character/asset ID** it serves — a `reference_id` is an identity-model locator, not an image result and not a canonical `result_asset_id`.

Apply the shared gate before submitting: training is a paid-plan operation — verified cost status and bounded approval are required, and the user must own or control rights to the faces being trained. Auxiliary still renders that would consume a Soul (e.g. `--soul-id` image calls shown below) are image jobs and are ineligible in this package; they are documented for downstream use only.

## Step 0 — Runtime check

Before any other command:

1. Verify `higgsfield` on `$PATH` and `higgsfield account status`. Missing CLI or failed auth (`Session expired` / `Not authenticated`) is a reported blocker — ask the user to run `higgsfield auth login` (interactive) and wait. Never auto-install; installation happens only as a separate explicit user request.
2. Soul training requires a paid plan (Basic+). If `higgsfield account status` shows free plan, tell the user before submitting.

## UX Rules

1. Be concise. No raw JSON dumps or unrelated IDs in chat — the returned reference ID itself is delivered as the `--soul-id` value the user needs.
2. Detect language and respond in it. CLI flags stay English.
3. Ask for the smallest set of inputs: name + photos. Reuse a supplied variant; ask only when the downstream use is unresolved.
4. Polling is silent — training takes minutes. Don't repeat status updates.

## Workflow

1. **Get name.** One word, used for later reference. Ask if missing.
2. **Get photos.** 5–20 face photos, varied angles and lighting. Local paths or already-uploaded IDs both work — `--image` accepts either.
3. **Pick variant.**
   - `--soul-2` — for image generation (default)
   - `--soul-cinematic` — for cinematic / video work
   Choose based on user's stated downstream use. Default to `--soul-2`.
4. **Submit.**
   ```bash
   higgsfield soul-id create --name "<name>" --soul-2 --image ./photo1.png --image ./photo2.png ...
   higgsfield soul-id create --name "<name>" --soul-2 --image <upload_id> --image <upload_id> ...
   ```
   CLI auto-uploads paths. Captures returned reference id.
5. **Wait.** `higgsfield soul-id wait <id>`. Silent. Default timeout 30m.
6. **Deliver.** "Soul `<name>` ready. Use in generate with `--soul-id <id>`."

## Use the Soul — downstream contract (image renders ineligible in this package)

The returned `reference_id` passes to image models via `--soul-id` (sent as the model's `custom_reference_id`):

```bash
higgsfield generate create text2image_soul_v2 --prompt "..." --soul-id <ref_id> --quality 2k --wait
higgsfield generate create soul_cinematic --prompt "..." --soul-id <ref_id> --quality 2k --wait
```

These are image-generation calls — craft/reference documentation only in this package (see Scope and package gate). Do not assume video-model compatibility: `seedance_*` has no soul parameter; video identity travels as reference images. For a curated Soul style, list styles with `higgsfield preset list soul-v2` and pass the chosen id as `--style_id` on `text2image_soul_v2`. `--style_id` cannot be combined with `--image`.

## Listing existing Souls

```bash
higgsfield soul-id list                   # all references
higgsfield soul-id get <id>               # one by id
```

## Errors

- `Minimum Basic plan required` — user is on free plan; tell them.
- `Training failed` — check photos quality (5+ unique faces, well-lit).
- `Session expired` → `higgsfield auth login`.

## Reference docs

- `references/photo-guide.md` — what photos work best
- `references/troubleshooting.md` — common training failures
