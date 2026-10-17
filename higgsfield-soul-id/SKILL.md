---
version: 0.35.0
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

Apply the shared gate before submitting: verify that the current account and requested operation are eligible under the inspected provider contract, verify the operation cost, and obtain bounded approval. The user must own or control rights to the faces being trained. Auxiliary still renders that would consume a Soul (e.g. `--soul-id` image calls shown below) are image jobs and are ineligible in this package; they are documented for downstream use only.

Before any photo upload or training, require explicit authorization to train a reusable
identity model and consent/authority for the one depicted person. Photo possession, an
avatar request, or five attachments alone is not consent. Multiple identities, non-person
subjects, a single photo, instant-result requests, or a non-Soul target do not satisfy this
training contract: clarify the intended non-training route without creating an Element
or uploading anything automatically.

Transport contracts differ: CLI `--image` paths auto-upload; mounted MCP `show_characters`
accepts confirmed media IDs, completed image-job IDs, or HTTPS references, never local paths.
Inspect the selected transport before use. Its documented `ready` state is the Soul
success boundary; generic generation-job states are not a substitute. Soul compatibility
is limited to Soul V2 / Cinema, one Soul per generation; inspect exact model IDs at runtime.

Direct evidence read (2026-10-17): mounted `xd://mcp__higgsfield_show_characters`
documents name + 5–20 references, allowed reference transports, `ready/training/failed`
filters and one-Soul/Soul V2-or-Cinema compatibility. CLI 1.1.26 `soul-id create --help`
documents name/images and two variant flags; [official MODELS.md Soul tables](https://github.com/higgsfield-ai/cli/blob/main/MODELS.md)
document CLI `--soul-id` and quality tiers. These reads do not prove successful training,
identity fidelity, plan tier/pricing, wait timeout, quality-to-pixel mapping or style/image
exclusion. Treat those cached details below and in troubleshooting as historical/unverified
until the actual current account/model/preset/wait contract is inspected. The explicit
training-consent rule is this package's stricter authorization policy.

## Step 0 — Runtime check

Before any other command:

1. Verify `higgsfield` on `$PATH` and `higgsfield account status`. Missing CLI or failed auth (`Session expired` / `Not authenticated`) is a reported blocker — ask the user to run `higgsfield auth login` (interactive) and wait. Never auto-install; installation happens only as a separate explicit user request.
2. Historical recipe requires a paid plan (Basic+), but the inspected create help/MCP schema does not establish that tier. Verify the current account/plan and quoted operation cost; do not promise training eligibility from a cached plan label.

## UX Rules

1. Be concise. No raw JSON dumps or unrelated IDs in chat — the returned reference ID itself is delivered as the `--soul-id` value the user needs.
2. Detect language and respond in it. CLI flags stay English.
3. Ask for the smallest set of inputs: name + photos. Reuse a supplied variant; ask only when the downstream use is unresolved.
4. Polling is silent — training takes minutes. Don't repeat status updates.

## Workflow

1. **Get name.** One word, used for later reference. Ask if missing.
2. **Get photos.** 5–20 face photos, varied angles and lighting. Local paths or already-uploaded IDs both work — `--image` accepts either.
3. **Pick variant.**
   - `--soul-2` and `--soul-cinematic` are explicit variant flags in the inspected create help; that help establishes no default or downstream-use mapping.
   - Before selecting, inspect the current training/model contract for the requested downstream use. Reuse a supplied compatible variant; otherwise resolve it with the user. Pass the selected flag explicitly; do not rely on an unverified default.
4. **Submit.**
   ```bash
   higgsfield soul-id create --name "<name>" --soul-2 --image ./photo1.png --image ./photo2.png ...
   higgsfield soul-id create --name "<name>" --soul-2 --image <upload_id> --image <upload_id> ...
   ```
   CLI auto-uploads paths. Captures returned reference id.
5. **Wait.** Immediately before use, inspect `higgsfield soul-id wait --help` and select an explicit bounded timeout/interval. The directly read help (2026-10-17) documents `--timeout` default 30m0s, `--interval` default 10s, and `--quiet`. Use `higgsfield soul-id wait <id> --timeout <approved-duration> --interval <selected-duration> --quiet`. Timeout leaves outcome pending/unknown: inspect the same ID and reconcile `ready/training/failed` before delivery or another attempt.
6. **Deliver.** "Soul `<name>` ready. Use in generate with `--soul-id <id>`."

## Use the Soul — downstream contract (image renders ineligible in this package)

The returned `reference_id` passes to image models via `--soul-id` (sent as the model's `custom_reference_id`):

```bash
higgsfield generate create text2image_soul_v2 --prompt "..." --soul-id <ref_id> --quality 2k --wait
higgsfield generate create soul_cinematic --prompt "..." --soul-id <ref_id> --quality 2k --wait
```

These are image-generation calls — craft/reference documentation only in this package (see Scope and package gate). Before any downstream handoff, inspect the exact selected model schema for Soul compatibility, style listing/selection syntax, and whether style and image references may coexist. The earlier evidence does not establish `--style_id`/`--image` exclusion or a universal video-model restriction; do not execute those cached assumptions. If the selected contract is unavailable, return that unresolved compatibility field as a blocker rather than issuing an example call.

## Listing existing Souls

```bash
higgsfield soul-id list                   # all references
higgsfield soul-id get <id>               # one by id
```

## Errors

- `Minimum Basic plan required` — if actually returned, report that error and inspect current eligibility; do not infer a plan threshold from this historical example.
- `Training failed` — inspect the recorded failure and photo quality (5–20 usable images of the same consenting person, not five different faces). Retraining is a new attempt requiring remaining approved count/cost scope.
- `Session expired` → `higgsfield auth login`.

## Reference docs

- `references/photo-guide.md` — what photos work best
- `references/troubleshooting.md` — common training failures

## Acceptance

Training may be submitted only when the requested name and 5–20 usable reference photos are present, the user has rights to the depicted faces, the current provider contract confirms account and operation eligibility, and the verified bounded cost is approved. Completion requires a terminal successful training result and the returned `reference_id` mapped to its canonical character/asset; failed or incomplete training is reported as such. Provider image-generation examples remain documentation only under this package’s eligibility rule.
