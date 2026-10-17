# Avatars

Contract read 2026-10-17: CLI 1.1.26 `marketing-studio avatars create --help` documents required name plus optional image/image-url/pinned flags. [Official MODELS.md](https://github.com/higgsfield-ai/cli/blob/main/MODELS.md#marketing_studio_video--marketing-studio-video) documents an avatars array, not all entity response fields. Costs, diversity, mandatory image-url, and automatic Soul synthesis below are historical/unverified, not guarantees; inspect live entity/model contracts. Custom creation is a mutation requiring reference authority and consent.

## Preset vs Custom

| | Preset | Custom |
|---|---|---|
| Source | Curated by Higgsfield | User-uploaded |
| Cost | Verify current selection/use cost | Verify upload/create/use cost; no fixed fee established |
| Diversity | Inspect actual catalog | Inspect supplied/authorized references; not “unlimited” |
| Use when | Generic ad, fast turnaround | Brand-specific face, founder, employee |

## Listing presets

```bash
higgsfield marketing-studio avatars list
higgsfield marketing-studio avatars list --json | jq '.[] | select(.gender=="female")'
```

Filter by `name`, `gender`, etc. on the JSON output.

## Creating a custom avatar

```bash
# Upload once only after authorization; reuse the returned ID and URL from that one response.
# <upload_id> and <upload_url> must identify the same confirmed upload.
higgsfield marketing-studio avatars create --name "Founder" --image <upload_id> --image-url <upload_url>
```

`--image-url` is documented as an uploaded image URL flag; inspected help does not mark it required. Verify the current API requirements instead of assuming it is mandatory.

## Passing to video

```bash
AVATARS_JSON=$(mktemp)
printf '[{"id":"<avatar_id>","type":"preset"}]' > "$AVATARS_JSON"

higgsfield generate create marketing_studio_video \
  --avatars @"$AVATARS_JSON" \
  ... \
  --wait
```

`type` is `preset` for curated, `custom` for user-created.
`--avatars` expects a JSON array, so pass it via `@/path/to/file.json`.

Historical recipe describes automatic presenter synthesis when an avatar is omitted; current behavior is unverified. Preserve a specifically chosen presenter and resolve identity/consent before any operation that could create or train a reusable identity.
