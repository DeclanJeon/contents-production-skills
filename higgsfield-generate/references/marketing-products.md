# Products

Contract read 2026-10-17: CLI 1.1.26 `marketing-studio products fetch --help` documents required URL, `--wait`, default timeout 90s. It does not prove extracted fields, App Store auto-routing, manual response shape or successful import; those cached details require current official entity contracts. Fetch/create mutates provider state and is not read-only preparation.

Two ways to register a product: URL fetch (auto-imports title, description, images) or manual (provide your own).

## URL fetch (default)

```bash
ID=$(higgsfield marketing-studio products fetch --url https://shop.example.com/sneakers --wait --json | jq -r .id)
```

`--wait` polls until `status` is `completed` or `failed`. Default timeout 90s.

If `failed`, check `fail_reason` — usually invalid URL or scrape blocked.

App Store URLs auto-route to `webproducts` (different endpoint). Use:

```bash
higgsfield marketing-studio webproducts fetch --url https://apps.apple.com/... --wait
```

## Manual

When the user has product photos and details:

```bash
A=$(higgsfield upload create shoe1.png)
B=$(higgsfield upload create shoe2.png)
higgsfield marketing-studio products create \
  --title "AeroRun Pro" \
  --description "Lightweight running shoe" \
  --image $A --image $B
```

Returns the product entity directly (no polling needed).

## Manual webproduct

For App Store / web pages without URL fetch:

```bash
higgsfield marketing-studio webproducts create \
  --url "https://example.com" \
  --title "MyApp" \
  --subtitle "Productivity for teams" \
  --description "..." \
  --favicon-url "https://example.com/favicon.png" \
  --desktop "https://cdn/screenshot1.png" \
  --mobile "https://cdn/mobile-screenshot.png"
```

## Listing

```bash
higgsfield marketing-studio products list
higgsfield marketing-studio products list --json
higgsfield marketing-studio webproducts list
```
