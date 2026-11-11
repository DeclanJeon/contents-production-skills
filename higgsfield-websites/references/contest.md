# App contest — how to enter, and how it shapes the build

Higgsfield runs an app contest with a **$100,000 total prize pool**. If the
user wants to enter (or asks what the contest is), this is the reference.
`higgsfield website contest <website_id>` is the command that submits an app.

> Prizes, dates, and rules below are the **current** contest as of 2026-07-08.
> The contest is admin-curated and recurs — treat specifics (amounts, dates) as
> this round's, and the live details are on
> `https://higgsfield.ai/supercomputer/apps?tab=prizes`. The mechanics
> (auto-publish on entry, social-link submission, judging on real usage) are
> stable.

## What it is

- **$100,000 total.** 1st **$25,000**, 2nd **$15,000**, 3rd **$10,000**, plus
  **10 honorable mentions at $5,000 each**.
- **Timeline (this round):** submissions open **Jul 8, 2026**, close **Jul 22,
  2026 (8:00 AM PT)**; judging Jul 22–29; winners announced **Jul 29, 2026**.
  Rankings refresh every 24h during the contest.
- **No fixed theme** — build anything that gives people a reason to *create* on
  Higgsfield (productivity tools, games, image/video generators, novelty apps).

## How entering shapes what you build (bake this in from the start)

Even before the user mentions the contest, these are just good `type: "app"`
practice — and they're the eligibility bar and the scoring rubric:

- **Must use Higgsfield image and/or video generation.** An app that routes
  generation through a third-party API instead of Higgsfield is DISQUALIFIED.
  (This is already the app rule — generation runs on Higgsfield via the fnf
  SDK; never offer a bring-your-own-API path.)
- **Original work, no third-party IP.** No protected characters, films, music,
  celebrities, or brands — in the app's concept, assets, or generated output
  framing. (Also the platform content rule.)
- **Must be freshly published** on Higgsfield on/after the contest open date —
  a brand-new listing, not a pre-existing app.
- **Judging is mostly real usage.** Weights: **Usage generated 40%** (the
  primary metric — total Higgsfield generation by users inside the app),
  **Creativity & concept 30%**, **social engagement 15%**, **in-app gallery
  engagement 15%**. So design for repeat generation: a fast path to a first
  result, an obvious reason to generate again, shareable output. Artificially
  inflated usage is discounted at Higgsfield's discretion.

## Entering — `higgsfield website contest` (may auto-publish the app)

Contest entry is a separate public action and can list the app on the community
feed. Require the user's explicit contest-entry authorization, including that
public effect, before running the command. It does not authorize remote project
creation, asset generation/upload, pushing, or live deployment.

When contest entry is authorized:

1. **Check listability.** Use an already live deployment with complete, approved
   cover/metadata. If the app is not live, or required metadata must change, a
   separately authorized deployment is needed. A contest request alone does not
   authorize `higgsfield website deploy`; stop and request that permission when
   absent. Never run the contest command against an incomplete or undeployed app.
2. **Get the social link(s).** The contest requires the app posted to at least
   one **public** social platform (Instagram, TikTok, YouTube, or X) with a link
   back to the Higgsfield app and the **`#HiggsfieldApp`** hashtag. Pass one or
   more `--url` flags, each linking to that public post. The user posts it
   themselves; request the URL(s) if missing and remind them about the app link
   and hashtag.
3. **Submit.** Run `higgsfield website contest <website_id>` with the `--url`
   flag(s) only after explicit contest-entry authorization, listability, and
   user-provided public post URLs are verified. There is a single active contest,
   so no contest id. One entry per app — re-running overwrites the URLs; use it
   to fix or add links, not to create a second entry.

```bash
# Only after all three gates above pass:
higgsfield website contest <website_id> \
  --url https://x.com/<user>/status/…   # public post, #HiggsfieldApp
```

If the user authorizes entry but has not posted yet, do not submit. If an
authorized live deploy already exists, give them the link and request their
public post URL; if it does not, first request any missing deployment permission.

## Eligibility (relay if asked)

18+, a Higgsfield account, free to enter. No third-party IP. Prizes paid within
30 days of the announcement after eligibility verification; winners cover their
own taxes. Void where prohibited. Jury decisions are final. Full official rules
are on the prizes page.
