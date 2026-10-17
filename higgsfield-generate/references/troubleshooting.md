# Troubleshooting

Contract read 2026-10-17: [official CLI README](https://github.com/higgsfield-ai/cli#troubleshooting) supports auth/unknown-model lookup and workflow cost syntax; mounted `generate_video` documents unknown submission outcomes, and `job_status` documents `poll_after_seconds`. Error examples below are historical, not a current exhaustive status contract. Reconcile known jobs and follow the selected transport; no provider execution was observed.

## Authentication

- `Session expired.` → `higgsfield auth login`
- `Stored credentials are for ... but current environment ...` → `higgsfield auth login` for the current API URL.
- `Not authenticated.` → first `higgsfield auth login`.

## Validation

- `Missing required params: prompt` — user gave no prompt. Ask.
- `Missing required params: medias` on Virality Predictor (`brain_activity`) — pass exactly one video via `--video <path-or-id>`. Virality Predictor does not need `--prompt`.
- `Invalid values: <param>=<v> (allowed: ...)` — pick from allowed enum.
- `Unknown params: <name>` — schema doesn't accept this flag. Run `higgsfield model get <jst>` and check.

## Job lifecycle

- Terminal `failed` — report the recorded reason; do not infer a safety cause. A corrected submission needs remaining approval.
- `nsfw` / `ip_detected` — inspect the current status/recovery contract. Do not automatically rephrase/resubmit to bypass a restriction.
- Wait timeout — outcome may be unknown. Inspect the original ID before any retry; extend the wait with the actual transport's documented flag.

## Rate limits

`Higgsfield API error (HTTP 429)` — too many requests. Back off.

## CloudFlare / DataDome

An HTML/captcha response is a transport/access failure, not proof of failed submission. Report it and reconcile any original job before retrying within approved scope; do not bypass anti-bot protection.

## Cost

`higgsfield generate cost <jst> ...` returns credit estimate without submitting. Useful when the user asks "how much will this cost?".

For workflows, use `higgsfield generate cost workflow <workflow_name> ...`, for example `higgsfield generate cost workflow reframe --duration 7.1 --resolution 1080p`. Do not use `higgsfield generate workflow cost ...`.
