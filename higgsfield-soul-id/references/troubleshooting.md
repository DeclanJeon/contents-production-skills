# Soul Troubleshooting

Evidence scope (2026-10-17): directly read mounted `show_characters` documentation
(training/ready/failed filters, 5–20 references) and CLI `soul-id create --help`.
They do not establish the historical Basic-plan threshold, cause frequencies or wait
defaults below. Inspect current account/training/wait contracts; report actual errors.

## `Minimum Basic plan required`

If that actual error is returned, report it. The Basic-tier threshold is historical/unverified; inspect current eligibility instead of asserting that upgrading necessarily resolves it.

## `Training failed`

Possible input-review hypotheses, not diagnosed causes or documented failure frequencies:

- Too few photos (<5) or too uniform.
- Heavy occlusion (sunglasses, hats).
- Group photos confusing identity.
- Upload type mismatch (must be image uploads, not video).

Action: report the terminal failure and recorded reason. Propose corrected photos; upload or retrain only within explicit identity-training consent and remaining approved attempt/cost scope. A timeout is not a terminal failure: resume inspection of the same ID, never create a duplicate training automatically.

## `Session expired`

`higgsfield auth login`.

## Slow training

Historical wait recipe uses 30m then `higgsfield soul-id wait <id> --timeout 60m`; verify current wait help before using that flag/default. While pending, inspect the same identity ID; do not retrain merely because the wait expires.
