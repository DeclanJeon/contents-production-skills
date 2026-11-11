# Website flow — `type: "website"` (independent brand, phased pipeline)

You are building ONE per-website Cloudflare Worker: a **React 19 + TanStack
Start** app that is **server-rendered (SSR)** and deploys as a single Worker
served at the website's own subdomain. A `type: "website"` product is a
STANDALONE brand — no Higgsfield integration, no Quanta, no fnf SDK; the
user's brand is the only brand on the page. If the product itself needs end users
to authenticate with Higgsfield or generate media inside the experience, use
`type: "app"` and `references/app-flow.md`. This does not change a standalone
website into an app merely because its separately authorized build process uses
approved media assets.

**Asset execution follows the package gate in `../SKILL.md`.** Design boards, cover and other stills use the authorized eligible image executor or supplied approved assets; preserved Higgsfield image commands in references are not in-package execution. Video/audio/3D remain separately budget/consent-gated. Internal asset use does not waive upload, generation or live-deployment authorization.

**Scope: build the real, full app.** This stack ships complete, production-grade
applications: real frontend AND backend, database (D1), file storage (R2), auth,
third-party API integrations, background work. When the user describes an app,
tool, site, or web product, BUILD IT with the website builder — it is the default
for any web target. Never ask the user to confirm the platform, never downgrade to
a "demo"/mockup as the safe option, and don't stall on scope questions beyond the
single intake round defined below. Take the fullest reasonable interpretation
and ship a working site.

**Repo layout.** The website project lives in **`app/`** — its own `package.json`,
`src/`, `packages/`, `migrations/`, build config, and the deploy inputs
(`app.manifest.json`, `wrangler.jsonc`). Run every `bun`/build command from there.

---

## THE PIPELINE — phases in order, artifacts + gates, no skipping

Every NEW build runs this machine. Each phase produces a named artifact the next
phase consumes. Do not reorder, merge, or skip phases — "simple" briefs are where
generic output happens. (Follow-up edits to an existing site do NOT restart the
pipeline — see "Small edits" at the bottom.)

### Before Phase 0 — creative intake (ONE batched round)

Ask the creative-discovery questions below together once; do not reopen answered
design questions in later phases. Authorization for remote project creation,
asset generation/upload, spending, push, deployment, or publication is
operation-specific and is requested separately at the relevant gate when not
already explicit. An earlier creative-intake answer never grants that consent.

1. **Animation — ask when unresolved.** Offer exactly two options:
   - **Animated (recommended)** → sets `Animation mode: animated-website` — the
     scroll-scrub camera journey (the product default; mark it Recommended).
   - **Non-animated** → sets `Animation mode: non-animated` — a well-crafted site
     with lighter/optional motion, no mandatory camera journey.

   Honor a choice the request already states without re-asking; point the
   Recommended marker at the implied option when the request leans one way.
   Record the picked value on the brief's `Animation mode` line (Phase 0).
   ONLY if the user is genuinely unreachable / never answers do you proceed on
   the default (**Animated**) and say so in one line — never as a shortcut to
   avoid asking.
2. **Brand constraints** — ask whether to honor an existing brand (including
   supplied/approved colors, fonts, logos, photos, and links) or receive free
   creative direction. Free direction authorizes the creative brief, not remote
   asset generation, upload, credit spend, or deployment. For missing assets,
   identify the proposed kit and stop at each operation gate until its required
   authorization exists. See `references/asset-system.md` for the kit scope.

Ask the Animation question only when unresolved; honor an explicit choice without asking again. Omit the brand question when the brief already answers it. An unreachable user permits only the stated design default, not authorization for paid assets, uploads or live deployment.

### Phase 0 — Concept (`app/design-brief.md`, committed, BEFORE any code)

Write the brief (~40 lines). Every section mandatory; a generic line ("modern and
clean", "Inter", "blue accent") means the brief is not done:

- **Design read** — one sentence: who is this for, what emotional register.
- **Concept spine** — a nameable narrative idea threading the whole page (e.g.
  "the site is a calibration instrument", "an archive dossier", "a stage").
  Pick from `references/reference-boards.md`'s spine list or invent better.
- **Delivery tier** — `cinema` (**default**: Lenis+GSAP, Tier-1 hero, scroll
  chapters — carries the animated website) · `spectacle` (briefs saying
  awwwards/webgl/3d/immersive: cinema + WebGL/3D/scrub + custom cursor + a
  second beat) · `editorial` (calm/minimal/B2B: typography + imagery + bespoke
  chrome, micro-motion only). The animated website is the default Tier-1
  experience regardless of tier, so cinema/spectacle is the normal home for it.
  `editorial` drops the scroll-scrub journey to micro-motion — treat choosing it
  as one of the "user explicitly asked for something other than an animated
  website" cases, not a default an ordinary B2B/minimal brief falls into on its
  own.
- **Locked palette** — exact hexes + a one-line defense. Hard bans (mechanical,
  gate-checked): (1) graphite/near-black + orange/amber/ember accent, (2)
  near-black + neon cyan/blue/green accent, (3) beige/cream + brass/clay/
  oxblood, (4) AI purple/violet glow, (5) the palette family of your previous
  build in this chat. Overridable only by the user's explicit brand colors.
  See `references/reference-boards.md` for what to reach for instead.
- **Locked type** — preserve supplied/approved brand typography and do not
  substitute a recipe font. A supplied family owns the hierarchy; use size,
  case, spacing, and its available styles. Use the recipe pairing only when no
  approved brand typography is supplied. Serif still needs written justification.
- **`Animation mode` — MANDATORY explicit state, set from the intake answer.
  HARD STOP.** Write `Animation mode: animated-website` or
  `Animation mode: non-animated` in the brief; an unreachable user may receive
  only the stated animation default and this does not authorize media operations.
  Animated is the product default. When animated, read
  `references/scroll-scrub.md` and record `Journey shape` separately:
  - **`single-shot` is the default.** One continuous ~15s film; map 3–6 semantic
    page chapters to moments in that film. Require a single storyboard and
    mobile framing. Do not require multiple scenes, seam direction, or A/B
    camera architecture.
  - **`multi-leg` requires informed, explicit user opt-in.** Before selection,
    disclose the 4–7 worlds, planned sequential operation count and time, and a
    verified aggregate cost. If a current quote is unavailable, state that and
    keep `single-shot`; a budget cap is not a verified quote. Only after the
    user opts in on the verified cost, plan exact-frame handoffs, seam direction,
    and A/B architecture as scoped by `scroll-scrub.md`. Authorize each
    operation separately before submission.
  For either shape, say how the scroll-driven film serves the concept and plan
  mobile-safe framing. Do not infer multi-leg from “animated” or “make it
  impressive”; choose single-shot when the brief fits one continuous move.
  Do NOT shop the wow catalog for animated mode — differ on the other design
  axes instead.
- **`non-animated`** (user picked it or the request clearly asked for it): a
  well-crafted site with lighter/optional motion and no mandatory camera
  journey. Record the user's exact choice/reason; the agent's taste or a “simple
  landing page” is not a reason to override the Animated default. Clear the
  `wow-maker.md` floor through a named lighter Tier-1 technique or editorial
  tier; do not ship a dead-flat page.

  Either way, a passive autoplay loop is never the Tier-1 mechanic.
- **Section plan** — ordered, one layout family per section, no consecutive
  repeats, ≥4 families for 6+ sections, eyebrow budget ceil(sections/3).
- **Asset plan** — list required and optional roles from
  `references/asset-system.md`, reuse approved supplied assets, and flag missing
  items for which operation authorization/capability is not yet available.
  Include scroll media only for selected `animated-website`; video loop and GLB
  remain optional, separately authorized treatments.
- **CTA inventory** — every CTA named with its OWN interaction identity (no
  shared button style — see bespoke-chrome in `references/image-to-code.md`).

The brief is a contract: later phases may not silently contradict it — edit the
brief first and say why.

### Phase 1 — Reference boards (design the page as IMAGES)

Read **`references/reference-boards.md`** and plan one landscape design reference
for each section. Reuse approved references first. Create only missing required
boards through the eligible image executor, after explicit authorization for
the model, board count, inputs, and total cost under the package gate. Do not
infer board-generation or re-roll permission from the website request; each
additional image operation requires scope and cost approval. Inspect every
returned board against the approved concept and section plan. If a required
reference is unavailable or unauthorized, record the blocker rather than
starting implementation against a fictitious board. Boards land in `refs/` in
the repo; they guide the design and do not replace the separate single-shot
film storyboard described in `references/scroll-scrub.md`.

### Phase 2 — Asset system (plan only authorized missing assets)

Read **`references/asset-system.md`** and use the Phase 0 asset plan as a
role checklist, not a batch-generation order. Reuse approved supplied assets
first. Mark each role required or optional for this design; plan only missing
required roles, and generate only after explicit authorization for that
operation, model, output count, and disclosed cost. The interaction pair, extra
section plates, custom icons, video loop, and GLB are optional unless this
specific design requires them. A logo/monogram is needed only if the user has no
approved brand mark. Do not use stock, picsum, or CSS-only substitutes as fake
content; when a truly required asset is unavailable or unauthorized, record the
blocker rather than pretending the kit is complete.

For animated websites, use the selected `Journey shape` from Phase 0 and
`references/scroll-scrub.md`. `single-shot` uses one storyboard and one
continuous video. Opt-in `multi-leg` uses its planned scenes and exact-frame
handoffs sequentially; do not parallelize dependent legs or trigger them without
separate asset-operation authorization. Compose and inspect only the assets
actually approved and returned.

### Phase 3 — Build to the boards, section by section

Read **`references/image-to-code.md`** and follow its discipline per section:
re-read the board at build time, extract text/type-scale/spacing/color/
component logic, implement faithfully, anti-drift (when your habit disagrees
with the board, the board wins). The craft floor in
**`references/design-recipe.md`** still applies everywhere (hero discipline,
layout bans, copy rules, zero em-dashes). Bespoke chrome: every CTA designed in
its own component with its own interaction identity; no site-wide button
utility classes. Registry components (`references/wow-maker.md` §5) remain
available as raw material — restyled to the boards, never default-skinned.
Build static-but-complete; motion is the next phase.

**HARD STOP for `Animation mode: animated-website` — build the selected
scroll-scrub journey as the spine, not an afterthought.** The selected shape in
Phase 0 controls the component and media data: `single-shot` is one continuous
film mapped to semantic chapters; opt-in `multi-leg` is a sequential, exact-frame
scene chain. Materialize `app/src/components/scroll-scrub/scroll-scrub.tsx` and
its CSS per `references/scroll-scrub.md`, and wire that real shape in this
phase. Use verified posters from approved assets. If required media is
unavailable, keep any development-only placeholder clearly isolated, mark the
site non-deployable, and remove it before delivery; do not claim the phase is
complete. Do not downgrade an animated request to a generic static page.

### Phase 4 — Motion pass (tier-mandated, one focused pass)

- **cinema/spectacle:** use one Lenis/GSAP scroll clock when those libraries are selected.
  The directly read [Lenis README](https://github.com/darkroomengineering/lenis#gsap-scrolltrigger), Setup → GSAP ScrollTrigger and Settings → autoRaf (`READ-PARTIAL`, 2026-10-16; README examples name Lenis 1.3.27), shows `lenis.on('scroll', ScrollTrigger.update)` and `gsap.ticker` driving `lenis.raf(time * 1000)`. Confirm the installed versions/API and avoid a second RAF driver. This is an integration pattern, not proof that every alternative stutters; inspect actual scroll/seam behavior in the selected runtime.
- The **Tier-1 hero mechanic** from the brief, fully executed — a half-wired
  version fails review. The hero is the wow carrier and it must respond to
  the USER'S INPUT (scroll plays the movie), never a passive autoplay loop.
  Passive motion the user can't influence does not count as the Tier-1 mechanic.
- **Animated website:** the selected shape from `references/scroll-scrub.md` is
  the Tier-1 hero mechanic; scroll controls playback, never passive autoplay.
  For `single-shot`, inspect the one continuous clip and chapter mapping; there
  are no inter-clip seams to validate and no A/B multi-leg architecture. For
  opt-in `multi-leg`, inspect every sequential exact-frame handoff, its selected
  A/B architecture, and seam direction. Let the chosen controller own
  scroll-to-video time; never drive the same media with a second ScrollTrigger
  timeline. A user-selected non-animated treatment instead wires its selected
  catalog mechanic.
- Scroll-chapter reveals: staggered headline builds (`split-type` + GSAP or
  registry text components), per-section distinct timing; work rows / cards
  with hover reveals; magnetic nav/CTA physics via `useMotionValue`, never
  `useState`.
- **Screenshot-safe reveals (hard rule):** nothing waits at `opacity: 0` for an
  IntersectionObserver. The safe recipe: headline/text builds fire ON MOUNT
  (not viewport-gated); scroll-linked effects animate transform/scale/clip
  ONLY, never opacity-to-zero; hover states may use opacity freely. Ignore
  any `whileInView` fade-in examples in the ingredient libraries — they fail
  this gate. A full-page headless screenshot must show every section.
- **Pin-spacer trap:** a GSAP pinned hero injects a spacer that reads as a
  large blank band in full-page screenshots (guaranteed review failure).
  Use `pinSpacing: false` with the following content sliding over the pinned
  layer, or otherwise verify the full-page shot has no dead band after the
  hero.
- EVERYTHING `prefers-reduced-motion`-gated with static fallbacks; `[C]`/`[W]`
  components behind the SSR pattern (wow-maker §6). A top-level `window`
  reference crashes SSR — the #1 recurring build failure.
- spectacle only: custom cursor + WebGL/3D/scrub second beat.

### Phase 5 — Mechanical gate (before first deploy; every item fixed)

Run the grep checklist in
**`references/review-rubric.md` §A**: placeholders; em/en-dashes; banned palette
families in tokens; eyebrow ration; unreferenced generated assets (every kit
file used); `h-screen`; SSR safety; reduced-motion coverage; **repeated CTA
classes** (bespoke-chrome violation); **opacity-0 + whileInView** combinations;
section plan honored; copy self-audit. This is a completion gate — do not
deploy with a failing item.

### Phase 6 — Deploy

0. Local type/build checks are not a default prerequisite: trusted platform CI
   performs the authoritative type + build on an explicitly authorized deploy.
   Use the optional local checks below only when their stated conditions apply.
   If CI fails, fix the reported issue before any separately authorized retry.
1. `higgsfield website deploy <website_id>` only with explicit live-deployment
   authorization; it ships the site immediately, with no preview stage.
2. Report “Your site is live: <url>” only after `higgsfield website status`
   confirms it is live. Otherwise report prepared/blocked status without
   implying deployment.
   product terms — no repo/commit/deploy jargon (see the SKILL.md "Talking to
   the user" rule).

Before deployment, complete the actual browser checks in
`references/review-rubric.md` §B for every selected branch using a local runtime
or another safely reachable preview with authorized access; source/grep checks
alone cannot prove rendered behavior. Do not deploy solely to enable QA. Remote
visits and live deployment remain separately authorized operations.
After an explicitly authorized deployment, report status-confirmed availability;
do not claim the live pixels or interactions were inspected unless they actually were.

3. **Publish.** If the user opted in at intake, publish automatically now that
   the site is deployed with its cover + metadata filled — run
   `higgsfield website publish <website_id>` (don't wait to be asked) and share
   the community-feed listing URL it reports. Otherwise publish only when the
   user asks. (The $100k contest is for `--type app` products — don't pitch it
   for a plain website.)

---

## Design references — read order

## Design references — read order

1. **`references/design-recipe.md`** — craft floor (ALWAYS read; short).
2. **`references/scroll-scrub.md`** — the **animated website**, which is the
   DEFAULT Tier-1 experience for every website: read it in Phase 0. It owns the
   specialized boards/assets/runtime sequence and bundled Markdown code
   references for that build. Only read **`references/wow-catalog.md`** (Tier-1
   technique menu + anti-convergence ledger + Phase 4 implementation contracts)
   when the user explicitly asked for something other than an animated website.
3. **`references/reference-boards.md`** — Phase 1: per-section design boards.
4. **`references/asset-system.md`** — Phase 2: the Higgsfield asset kit.
5. **`references/image-to-code.md`** — Phase 3: faithful implementation +
   bespoke chrome + the CTA garment catalog.
6. **`references/review-rubric.md`** — Phase 5: the mechanical gate.
7. `references/wow-maker.md` — ingredient directory: motion/3D libs (§4),
   component registries (§5), signature effect patterns (§2), SSR pattern (§6).
   Only listed free/permissive sources may be used.
8. `references/design-taste-frontend.md` — the full deep-dive playbook behind
   the recipe; consult for specific situations, not required start-to-end.
9. `references/app-cover.md` — the branded 3:2 launch cover + OG image
   (stadium-capsule mask via the inlined compose script; hosted style refs).
   REQUIRED before every publish (`og_image_url` + `marketplace_cover_url` are
   mandatory feed-card fields — never run `higgsfield website publish` while
   they are empty), and whenever the user asks for a cover/OG image directly.

Do NOT search the skill library for other design guidance — everything is here.

Then route to the FUNCTIONAL reference for the task:

| Task | Read |
|---|---|
| Any website (animated by default), scrollable world, continuous camera journey, diorama fly-through, browse-through-an-industry site | `references/scroll-scrub.md` — choose single-shot by default or an explicitly opted-in multi-leg chain; React/CSS implementation, mobile, and QA contract |
| TanStack Start routes, SSR, server functions, Cloudflare Worker runtime | `references/runtime-and-infra.md` |
| Cover / OG image ("cover", "обложка", "OG image", publish prep) | `references/app-cover.md` — branded 3:2 cover + capsule OG mask |
| SEO: meta tags, OG/Twitter cards, robots/sitemap, JSON-LD, entity, GEO, audit | `references/seo.md` |
| Security: Worker hardening, OWASP audit, threat modeling | `references/security.md` |

## Stack

- **TanStack Start** (file-based routing under `app/src/routes/`, SSR via
  `app/src/server.ts` → a Worker `export default { fetch }`). No Next/Remix/Astro
  conventions, no `app/src/pages`.
- **Vite 7 + bun**. Build emits `dist/server/server.js` (the Worker) +
  `dist/client` (hashed static assets). Tailwind v4 is wired in `app/src/styles.css`
  (it also imports Quanta's Tailwind entry for the template
  bundle — leave that wiring alone even though websites use neither). Legacy
  shadcn/ui files may exist from the scaffold. Websites use custom
  Tailwind/CSS only — never import `@higgsfield/quanta/*`.
- **No separate Hono/Express backend.** Server logic is TanStack **server
  functions** (`createServerFn`) and **server routes**. App-local API routes are
  allowed when a platform contract requires them (for example a webhook
  receiver or a JSON endpoint the site's own client fetches).


## Hard rules

### 0a. Vendored packages and template modules

The `app/packages/` directory contains managed snapshots vendored from the
upstream Higgsfield web app (`@higgsfield/fnf`, `@higgsfield/fnf-react`,
`@higgsfield/quanta`). Websites never use them, but do NOT edit or delete
them. Template-owned infrastructure lives in `app/src/module/**`.

### 0b. Supercomputer Design mode inspector

Generated websites support a Higgsfield design inspector bridge for editing in
Supercomputer Design mode. The split is strict:

- The Higgsfield editor (parent window) owns the iframe UI, hover overlay,
  edit popover, origin/session checks, and edit prompt submission.
- This template owns the child iframe runtime through
  `app/src/module/design-inspector`.
- Agents never manually implement inspector code, refs, source markers, or
  `data-hf-*` attributes.

Local scripts (LOCAL work only — the deploy build is owned by CI):

- `bun run build` is inspector-free by default: no inspector runtime and no
  source metadata. Setting `HF_DESIGN_INSPECTOR=1` in the env turns the same
  build into the inspector-enabled one (this is what platform CI does on
  every deploy).
- `bun run dev:design` is local dev with the inspector enabled.

The platform CI sets `HF_DESIGN_INSPECTOR=1` on every deploy build, so the live
deployed site always carries the inspector and IS the surface Supercomputer
Design mode opens. Exact source metadata is attached with inspector-only
callback refs and a `WeakMap`, not DOM attributes. Keep the guarded
dynamic install in `app/src/routes/__root.tsx` and the Vite integration in
`app/vite.config.ts` wired to `app/src/module/design-inspector/vite`.

For every Supercomputer website-builder task there is ONE deploy —
`higgsfield website deploy <website_id>` — and it ships the live public site
immediately; there is no preview stage or environment choice. Publishing/listing on
the community feed is separate: do NOT run `higgsfield website publish` unless
the user explicitly asks to publish, list, or share the site. Never hard-code
`HF_DESIGN_INSPECTOR=1` into the `build` script and never hand-edit the build
script to toggle it — the deploy build is CI-owned.
### 1. SSR-safe rendering
Every route renders on the server per request. NEVER touch browser-only globals
(`window`, `document`, `localStorage`, `navigator`) at module top level or during
render — only inside `useEffect`/event handlers, or guarded with
`typeof window !== "undefined"`. A top-level `window` reference crashes SSR.

### 2. Server-only code stays server-only
Put server logic in `createServerFn(...).handler(...)` or a `*.server.ts` module
(the `.server.ts` suffix keeps it out of the client bundle). Secrets and
bindings are read **server-side, per request** — never shipped to the browser.

### 3. No Higgsfield integration — but a REAL backend of the site's own
A `type: "website"` product never calls `https://fnf.internal/*`, never shows
"Sign in with Higgsfield", and never imports the fnf SDK. It still gets a real
backend wherever the product needs one: server functions (`createServerFn`),
app-local API routes, sessions, business logic, and real persistence (D1) —
never in-memory arrays, `localStorage`-as-database, or fixture data. In-app
auth for the site's OWN users (accounts, teams, dashboards) is built with the
website's own routes/storage. If the request needs generation or Higgsfield
accounts, it is a `type: "app"` — switch to `references/app-flow.md`.

### 4. Cloudflare bindings via `cloudflare:workers`
Any infra you opt into (D1 `DB`, R2 `STORAGE`, KV `KV`) is read server-side
through `app/src/lib/bindings.server.ts` (`import { env } from "cloudflare:workers"`).
Each binding is present ONLY if declared in `app/app.manifest.json`, so the typed
accessors are optional — guard before use. Do not thread `env` through React
props or read it at module top level.

### 5. Opted-in storage is LIVE — one deploy, one database
If you opt into D1, R2, or KV, each is a SINGLE instance backing the ONE live
deploy. There is no staging copy: every migration and data change hits **live
production data** directly.
- `env.HF_ENV` is always `"production"` on deployed builds; there is no
  separate database/bucket to test against.
- A destructive migration you run "just to test" destroys **production data**.
  Prefer additive migrations (`CREATE TABLE IF NOT EXISTS`, `ADD COLUMN`), and
  get explicit user approval before any destructive change.

### 6. `app/app.manifest.json` declares infra — NOTHING is provisioned by default
A new website gets **no D1, no R2, no KV, no Durable Object**. Opt in only when
the website actually needs it:
- `"db": true` → a D1 database, bound `env.DB`
- `"r2": true` → an R2 bucket, bound `env.STORAGE`
- `"kv": true` → a KV namespace, bound `env.KV`
- `"durableObject": "ClassName"` → a Durable Object, bound `env.ROOMS`
- `"container": true` (or `{ "instanceType", "port", "sleepAfter" }`) → a Docker
  container for heavy/long-running work, bound `env.CONTAINER` — see
  `references/containers.md`

Counts are capped (≤1 each) by the platform, which PROVISIONS the resource and
binds it at deploy. The committed `app/wrangler.jsonc` is build/dev input only;
the platform OVERWRITES its `name` + bindings at deploy — declare infra in
`app/app.manifest.json`.

**KV is eventually consistent** (NOT Redis): config, feature flags, cached reads
— NOT counters, locks, or read-after-write. Use a Durable Object for strong
consistency.

For a **Durable Object** you must ALSO `export class ClassName extends
DurableObject {…}` from `app/src/server.ts` (alongside the default `{ fetch }`
export).

For a **container** — heavy or long-running work a Worker can't do: set
`"container"` in the manifest and follow **`references/containers.md`** (exact
Dockerfile, the platform-fixed `AppContainer` class, keep-alive + 3-hour-deadline
pattern, fnf via container token). Containers are **off by default**.

## Editing map
- Pages / routing → `app/src/routes/**` (file-based; `__root.tsx` is the shell).
- Server logic → `createServerFn` (see `app/src/lib/api/example.functions.ts`) or
  `*.server.ts`.
- Bindings access → `app/src/lib/bindings.server.ts`.
- Infra declaration → `app/app.manifest.json`; `app/wrangler.jsonc` = build/dev input.
- Durable Object class → exported from `app/src/server.ts`.
- Components → custom components per the boards; app-local files in
  `app/src/components/**`. Do not start from `app/src/components/ui/*` unless
  migrating a legacy shadcn piece.
- Styles / theme → `app/src/styles.css` wires Tailwind v4. Websites: a custom
  token layer from the design brief — no q-prefixed utilities, no site-wide
  CTA utility classes.
- D1 schema → `app/migrations/000N_*.sql` (additive; see rule 5).
- Pipeline artifacts → `app/design-brief.md` (Phase 0) + `refs/*.png` (Phase 1);
  commit both.

## Verify + deploy

The trusted platform CI builds the website on **every deploy** (always with
`HF_DESIGN_INSPECTOR=1` and `HF_ENV="production"` — the live site carries the
design inspector), so a deploy already gives you the authoritative type +
build result. Do NOT reflexively `bun install` +
`bun run build` just to check your work. The sandbox cannot deploy/migrate (no
Cloudflare token); the trusted platform CI does that.

**Default:** run the pipeline and pass the Phase 5 gate. Deploy
(`higgsfield website deploy <website_id>`) only with explicit deployment
authorization; it ships the live site immediately. Never publish/list on the
community feed unless the user explicitly authorized that listing.

**Publishing ("show in feed").** Feed publication is a separate operation:
`higgsfield website publish <website_id>` lists the currently deployed version
and does not deploy changes. Run it only with explicit community-listing
consent. Deploy prerequisites are separately authorized under the gate below;
do not deploy just because a user requested a feed listing.

**HARD GATE — the cover is required for a usable feed card.** An empty
`og_image_url` or `marketplace_cover_url` produces a blank cover; an empty
`og_title` makes the listing invisible. The feed card reads `app/src/app-meta.json`.
Before a feed listing:

1. Read `app/src/app-meta.json` and identify each missing real value.
2. Read `references/app-cover.md` for the cover requirements. Reuse an existing,
   user-approved asset when available. Do not substitute a placeholder.
3. If a cover must be created or uploaded, do that only when the explicit
   authorization already covers the selected executor, any credit spend,
   upload/storage, and required project changes. A request to publish authorizes
   the community listing only; it does **not** authorize cover generation, spend,
   upload, a code change, push, or deployment. If a required permission is
   missing, stop before that operation and state which input or authorization is
   needed. Do not publish an incomplete card as a workaround.
4. Fill required fields only from verified, user-approved content and assets:
   `og_title`, `og_description`, `og_image_url`, `marketplace_cover_url`, and
   `favicon_url` as applicable. The cover URLs must use approved assets; do not
   presume a single generation may provide both files unless its actual output
   contains both.
5. Commit, push, and deploy only if each operation is authorized. Deployment is
   a separate live-site change, not included in feed-listing permission. A feed
   listing describes the currently deployed version; if the required metadata
   is not live and deployment is not authorized, stop before listing.
6. Run `higgsfield website publish` only with explicit community-listing consent
   and after required live metadata is ready.

An optional `og_video_url` is also a separate media operation. Offer it and ask
permission before generating; then follow "Cover video" in `references/seo.md`.

Permission is operation-specific throughout this sequence. Existing content or
asset requirements do not authorize creating, uploading, paying for, pushing,
deploying, or publishing them.

`higgsfield website deploy <website_id>` remains the way to ship the live site
WITHOUT a feed listing.

**Run the local checks only when you actually need them** — from `app/`:
```bash
cd app
bun install          # only when you changed dependencies / package.json
bun run typecheck    # tsc --noEmit — only to chase a type error on deploy
bun run build        # local build — only to chase a build error on deploy
```
Run them when: you changed dependencies or build/runtime config, you're debugging
a build/type error, or a command genuinely needs `node_modules`.

**Small edits to an existing site** (copy tweak, one component, styling fix):
the pipeline does not restart. Make the local edit; deploy only with explicit
live-deployment authorization. Otherwise report the prepared change and stop.

**Before claiming a build done / deploying, no placeholders may remain** — no
`<...>`-style tokens, `lorem ipsum`, or scaffold blank-page markers
(`REMOVE_THIS` / `blank-app-v1`). This is covered by the mechanical gate (the
grep checklist in `references/review-rubric.md` §A).
