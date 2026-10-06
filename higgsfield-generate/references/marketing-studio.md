# Marketing Studio — branded ads (video eligible; image ineligible here)

Branded image/video generation: avatars + products + optional setup hooks/settings + ad-style
modes. Models: `marketing_studio_video` and `marketing_studio_image`.

Package eligibility (see `package-gate.md`): `marketing_studio_video` jobs are video output
and run through the normal gate; `marketing_studio_image` is an IMAGE job and is ineligible in
this package — its workflow below is craft/reference only. Entity management commands
(products/avatars/hooks/settings/ad-references/brand-kits fetch/list/create) are not media
generation; they still require the runtime check and serve only the user-authorized scope.

## Concepts

- **Avatar** — presenter face. Curated `preset` (browse `higgsfield marketing-studio avatars list`) or `custom` (uploaded photos via `higgsfield marketing-studio avatars create`). For UGC modes, an avatar is optional if the brief clearly mentions a person; the backend can create a Soul Character automatically. Pass an avatar when the user wants a specific presenter.
- **Product** — brand item with title + reference images. Imported from URL (`higgsfield marketing-studio products fetch --url ...`) or created from uploaded images (`higgsfield marketing-studio products create`).
- **Webproduct** — App Store / web page version. Auto-routes when fetching App Store URLs.
- **Hook** — reusable opening angle / ad hook. Browse with `higgsfield marketing-studio hooks list`. Hook text is prepended to the user's prompt; it does not replace `--prompt`.
- **Setting** — reusable environment / scene context. Browse with `higgsfield marketing-studio settings list`.
- **Ad reference** — reusable inspiration video that can be bound to an avatar and/or product. Created from an uploaded video (`--video-input <upload_id>`) or a previous generation job (`--job <job_id>`). Browse with `higgsfield marketing-studio ad-references list`. See `references/marketing-ad-references.md`.
- **Brand kit** — captures a brand's identity (name, logo, hero images, colours, fonts, tone) for reuse across image generations. Created by handing in a website URL (`higgsfield marketing-studio brand-kits fetch --url https://… --wait`). See `references/marketing-brand-kits.md`.
- **Ad format** — presets that drives the visual structure of a generated image (`headline`, `bullet-points`, etc.). Read-only, browse with `higgsfield marketing-studio ad-formats list`. Required input for `dtc-ads generate`.

## Discovery commands

Use these exact list commands when the user asks what already exists:

```bash
higgsfield marketing-studio avatars list --json
higgsfield marketing-studio products list --json
higgsfield marketing-studio hooks list --json
higgsfield marketing-studio settings list --json
higgsfield marketing-studio ad-references list --json
higgsfield marketing-studio brand-kits list --json
higgsfield marketing-studio ad-formats list --json
```

`--hook_id` and `--setting_id` are supported by `marketing_studio_video` only; do not pass them to `marketing_studio_image`.

## UX rules (additional)

- One question per phase. Don't ask product+avatar+mode upfront.
- **Two ad approaches are mutually exclusive.** Either the user gives an ad reference video (reference-driven) **or** picks hook/setting blocks (composed-from-blocks) — never both. If the user has an ad reference selected, do not offer hook/setting; if hook/setting are picked, do not offer to attach an ad reference.
- **Ad reference source.** The only valid inputs are a local video file (uploaded via `higgsfield upload create ... --video`) or a prior video job. If the user provides anything else, ask for a local file.
- **`dtc-ads` ad format is mandatory.** Always ask the user to pick from `ad-formats list`. There is no auto-default — both the CLI and server reject calls without `--format-id`.
- **`dtc-ads` optional inputs.** Suggest avatars, products, and reference media when the brief calls for them; only attach what the user picks.

## Workflow — quick ad video

1. **Get product.**
   - Existing product → `higgsfield marketing-studio products list --json`
   - URL → `higgsfield marketing-studio products fetch --url <url> --wait` (polls until import done)
   - Local images → `higgsfield upload create <photo>...` then `higgsfield marketing-studio products create --title "..." --image <id>...`
   Capture product id. When using `--hook_id`, strongly prefer passing `--product_ids`; hooks are designed to pivot into a product and work poorly without product context.
2. **Pick avatar if needed.**
   - Default: `higgsfield marketing-studio avatars list` and pick a preset matching the brand voice.
   - Custom: `higgsfield marketing-studio avatars create --name "..." --image <upload_id>`.
   For UGC modes, you may omit `--avatars` when no specific presenter is required and the brief mentions a person; the backend can synthesize a Soul Character.
3. **Optionally pick setup items.**
   - Hook: `higgsfield marketing-studio hooks list --json`
   - Setting: `higgsfield marketing-studio settings list --json`
   Pass selected IDs as `--hook_id <hook_id>` and `--setting_id <setting_id>` for `marketing_studio_video` only. Do not copy the hook's prompt into `--prompt` unless the user explicitly wants to reinforce the same wording.
4. **Pick mode if needed.** Default is `ugc`; `--mode` is not required just because `--hook_id` is present. Other current slugs: `ugc_how_to`, `ugc_unboxing`, `product_showcase`, `product_review`, `tv_spot`, `wild_card`, `ugc_virtual_try_on`, `virtual_try_on`. **Hook/setting are valid only for `ugc`, `ugc_how_to`, `ugc_unboxing`, `product_review`, `ugc_virtual_try_on`** — do not pass `--hook_id` / `--setting_id` with the other modes. See `references/marketing-modes.md`.
5. **Generate (one-shot).**
   ```bash
   PRODUCT_IDS_JSON=$(mktemp)
   AVATARS_JSON=$(mktemp)
   printf '["<product_id>"]' > "$PRODUCT_IDS_JSON"
   printf '[{"id":"<avatar_id>","type":"preset"}]' > "$AVATARS_JSON"

   higgsfield generate create marketing_studio_video \
     --prompt "..." \
     --avatars @"$AVATARS_JSON" \
     --product_ids @"$PRODUCT_IDS_JSON" \
     --mode ugc \
     --duration 15 \
     --resolution 720p \
     --aspect_ratio 9:16 \
     --wait
   ```
   Add `--hook_id <hook_id>` and/or `--setting_id <setting_id>` when a setup hook/setting was selected.
   `product_ids` and `avatars` are JSON arrays; pass them via `@/path/to/file.json`. Do not pass a bare UUID to `--product_ids`.
   Resolution is `480p`, `720p`, or `1080p`. Aspect ratio is one of `auto`/`21:9`/`16:9`/`4:3`/`1:1`/`3:4`/`9:16`. `--generate-audio true` is supported here (default `false`). `--wait` blocks until done; bump `--wait-timeout 30m` for longer ad runs.
6. **Deliver.** URL + one-line summary (mode, duration).

## Click-to-Ad shortcut (URL-driven)

When the user gives a product URL and wants a marketing video in one go:

```bash
# 1. Trigger fetch (returns the product id, import runs in the background)
higgsfield marketing-studio products fetch --url https://shop.example.com/sneakers --wait

# 2. Generate the marketing video against the same URL — backend reuses the entity
higgsfield generate create marketing_studio_video \
  --url https://shop.example.com/sneakers \
  --mode ugc \
  --duration 15 \
  --aspect_ratio 9:16 \
  --wait
```

Backend dedupes by URL, so repeated runs reuse the existing entity instead of re-fetching.

## Workflow — marketing image — craft/reference only (image job, ineligible in-package)

Same as above but use `marketing_studio_image` model:

```bash
higgsfield generate create marketing_studio_image \
  --prompt "..." \
  --aspect_ratio 1:1 \
  --resolution 2k \
  --wait
```
