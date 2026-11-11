# App flow — `type: "app"` (Higgsfield-integrated, Quanta)

You are building ONE per-website Cloudflare Worker: a **React 19 + TanStack
Start** app that is **server-rendered (SSR)** and deploys as a single Worker
served at the app's own subdomain. A `type: "app"` product is tightly
integrated with Higgsfield: its users **Sign in with Higgsfield** and generate
images/videos through the **fnf SDK**, and the app must look and feel like a
Higgsfield product — apps render INSIDE Higgsfield, indistinguishable from its
own tools. There is no independent brand and no wow/marketing pipeline here:
the craft bar is Quanta's UX-craft rules.

Package gate applies throughout this flow (see `../SKILL.md`): the runtime check never auto-installs; every cover/asset generation is an authorized operation inside the approved scope; image jobs run through the authorized eligible image executor in-package, video/audio/3D stay eligible provider jobs.

**Repo layout.** The project lives in **`app/`** — its own `package.json`,
`src/`, `packages/`, `migrations/`, build config, and the deploy inputs
(`app.manifest.json`, `wrangler.jsonc`). Run every `bun`/build command from
there.

## What you have to build with

- **Quanta** (`@higgsfield/quanta`) — Higgsfield's design system, vendored in
  the template. MANDATORY: use its components before writing custom chrome.
  `references/quanta-design.md` is the working guide (tokens, components,
  UX-craft rules, the Higgsfield integration rules); the canonical API
  reference is `app/packages/quanta/ai/AGENTS.md` — RELY ON IT for props/APIs;
  do NOT open or grep the component `.tsx` source to re-derive prop names.
- **The six code layouts** (`references/app-layouts.md` +
  `app/src/layouts/AGENTS.md`) — Studio (`studio.tsx`), Preset (`preset.tsx`),
  App detail (`app-detail.tsx`), AI Stylist (`ai-stylist.tsx`), Skin Enhancer
  (`skin-enhancer.tsx`), and Shots (`shots.tsx`), shipped as REAL CODE in the
  template (not screenshots). Start from the closest one, copy it into your
  route, and adapt it — build from the code plus the reusable pieces in
  `app/src/components`, never from a screenshot.
- **Custom components for gaps** — for anything Quanta lacks (date picker,
  calendar, data table, …), build a small component from Quanta primitives +
  `q-` tokens in the app's own `app/src/components/`. Never add a third-party
  UI library, never edit the vendored `@higgsfield/quanta` package, never
  restyle a Quanta component (see `references/quanta-design.md` rule 5).
- **Icons** — Google Material Symbols outlined 400, imported per icon
  (`@material-symbols/svg-400/outlined/<name>.svg?react`). The generate-button
  sparkle is the branded `@/assets/icon-sparkles-soft.svg?react`.
- **fnf SDK** (`references/fnf-sdk.md`) + **React bindings**
  (`references/fnf-react.md`) — generation jobs, media, profile, workspace,
  credits. `@higgsfield/fnf` ships the SDK core plus ONE bundled adapter:
  `createWorkflowPlatformAdapter` at `@higgsfield/fnf/workflow-platform` (the
  old `@higgsfield/fnf/adapters` subpath no longer exists; other adapters live
  in `@higgsfield/fnf-adapters`, which generated apps do not use). Package
  guides are canonical for APIs: `app/packages/fnf/ai/AGENTS.md` and
  `app/packages/fnf-react/ai/AGENTS.md` — rely on them; do NOT grep the SDK
  source to re-derive method names/params.
- **Higgsfield auth** (`references/auth.md`) — the `/api/user` proxy,
  `/__auth/login`/`/__auth/logout`, server-side re-checks. Mandatory for every
  app (see rule 3).
- **Infra** — D1 / R2 / KV / Durable Objects / containers via
  `app/app.manifest.json` (rules 4-6; heavy/long-running work:
  `references/containers.md`). Runtime + routing:
  `references/runtime-and-infra.md`. Security: `references/security.md`.
- **Launch cover** (`references/app-cover.md`) — the branded 3:2 cover + OG
  image. REQUIRED before every publish (`og_image_url` +
  `marketplace_cover_url` are mandatory feed-card fields).

**Separate app functionality from build-time assets.** When the requested product
itself offers Higgsfield generation, implement the user-facing fnf feature under
the app’s auth, submission-confirmation, and cost contracts below. That does not
authorize the assistant to generate the app’s own design, state, icon, favicon,
or cover assets. Build-time images follow `../SKILL.md`’s eligible-image and
operation-specific authorization gates; use the authorized eligible image
executor or report the missing permission/capability as a blocker.

## Non-negotiable app design rules

These come from `references/quanta-design.md` — read it before building:

1. **Never customize Quanta styles, never modify Quanta** — compose, don't
   restyle. Build anything Quanta lacks as your own small component from Quanta
   primitives + `q-` tokens in `app/src/components/`; never add a third-party
   UI library.
2. **No app header/top bar** — apps render inside Higgsfield; the host chrome
   provides the global header and account controls. Never credits/balance or
   sign-out UI. In-app navigation is a Quanta `Sidebar` or inline controls.
3. **Always dark** — `data-theme="default-dark"` is pinned; no theme toggle,
   no light mode, no `dark:` styling.
4. **Container width** — `mx-auto w-full max-w-7xl` on every shell except the
   cinema-studio full-bleed workspace.
5. **Buttons** — variant colors do NOT follow the names: `primary` = flat
   lime, `secondary` = solid white, `tertiary` = dark white/10 glass. The
   generation CTA is always `marketingPrimary` with the credit cost inside the
   button (`{label} {sparkles icon} {credits}`, credits in the label's font);
   ordinary/nav actions use the dark `tertiary`/`ghost`.

## How to build an app

**Plan first, then narrate progress.** Right after intake, post a short plan
to the user — the screens/features you're about to build, in product terms
(per the SKILL.md "Talking to the user" rule). As you work, send a one-line
update whenever a step completes ("Screens are built — wiring up generation
next", "4 of 6 done") so the user always knows how much work remains. Never
go silent for a long stretch of the build.

**Read the guides, then BUILD — do not spelunk the package source.** Your whole
API surface is already written down: `references/app-quickstart.md` (the
copy-paste critical path — auth, generation submit/poll, result rendering, and
the common Quanta components — READ IT FIRST), `references/quanta-design.md`
plus the in-repo `app/packages/quanta/ai/AGENTS.md` for component props/tokens,
and `references/fnf-sdk.md` + `references/fnf-react.md` (canonical in-repo
mirrors: `app/packages/fnf/ai/AGENTS.md` and `.../fnf-react/ai/AGENTS.md`) for
the SDK + hooks. Those guides plus the chosen code layout are ENOUGH to
build the whole app. **Do NOT open, `cat`, or `grep`
`app/packages/{quanta,fnf,fnf-react}/src/**`** — every prop and method you need
is in the guides, and reading package source is the single biggest time sink in
a build (it also bloats context and slows every later step). If a specific prop
or field is genuinely missing from a guide, make the reasonable call. Once you
have read the guides + the chosen code layout, you have enough — start writing.

1. **Intake** (one creative round): confirm `type: "app"` when unclear, app
   purpose/model needs and brand direction, plus whether to list it on the
   community feed when ready. A listing “yes” authorizes only that listing.
   Answered creative decisions are not reopened; any missing operation
   authorization is requested separately at its explicit gate.
2. **Create** — run `higgsfield website create --type app` only when remote
   project creation is explicitly authorized. Otherwise stop before the command
   and identify the missing permission.
3. **Plan the screens** — pick the closest of the six code layouts in
   `app/src/layouts` (studio / preset / app-detail / ai-stylist / skin-enhancer
   / shots; see `references/app-layouts.md`) and read its code +
   `app/src/layouts/AGENTS.md`
   for the composition; list the screens/states (including first-run/empty
   state) and the app's own product state for D1.
4. **Build with Quanta** — adapt the chosen code layout using
   Quanta components per `references/quanta-design.md`. NEVER customize or
   modify Quanta; when a component doesn't exist or doesn't fit as-is, build a
   small custom component from Quanta primitives in `app/src/components/`
   (`quanta-design.md` rule 5). Real copy in every state (empty, busy, error)
   — no placeholders.
5. **Wire fnf end-to-end** — auth first (`references/auth.md`), then
   generation/media through server functions per `references/fnf-sdk.md` +
   `references/fnf-react.md`, product state in D1 (rules 3/3a below). Poll
   jobs, render real results.
6. **Cover + metadata — required for a complete app and before deployment.**
   Preserve supplied, user-approved assets. Complete `og_title`,
   `og_description`, `favicon_url`, `og_image_url`, and
   `marketplace_cover_url` with verified content and approved assets. Create or
   upload missing assets only when the particular eligible executor, any spend,
   and upload/storage are authorized under `../SKILL.md`'s package gate. If
   authorization or an eligible capability is missing, stop and report the
   blocker instead of silently substituting or claiming completion.
   `og_video_url` is separately permission-gated. Offer a cover video, but
   generate it only with its specific approval (`references/cover-animator.md`).
Before deployment, exercise the actual app in a local runtime or safely
reachable preview with authorized access: signed-out/login handling, the
model-specific cost confirmation path, result/history rendering, and relevant
persistence. Do not trigger a paid generation unless that specific provider
operation is authorized. If a path needs paid-provider authorization or no safe
preview is available, report it blocked and do not deploy or claim that path was
verified.
7. **Deploy** only after the cover and metadata are ready, and only if live
   deployment is explicitly authorized (`higgsfield website deploy <website_id>`
   ships publicly with no preview). Report a live URL only after
   `higgsfield website status` confirms it; otherwise hand off the prepared app
   as not live.
8. **Publish.** A feed-listing opt-in authorizes that listing only. Run
   `higgsfield website publish <website_id>` after the app is live with required
   metadata and approved assets, and only when the separately authorized project,
   upload, push, and deployment prerequisites are satisfied. If any prerequisite
   authorization is absent, stop before that operation and name it; do not
   interpret the opt-in as blanket consent. Otherwise publish only when explicitly
   asked. After a successful listing, you may suggest the contest; entry itself
   requires separate, explicit consent, because it also publishes the app
   (`references/contest.md`).

---

## Functional routing

| Task | Read |
|---|---|
| **START HERE** — the working critical path: auth, generation submit/poll, result rendering, the common Quanta components | **`references/app-quickstart.md`** |
| fnf SDK: generation jobs, media upload, profile/workspace/credits, adapters | `references/fnf-sdk.md` + `references/auth.md` + `references/runtime-and-infra.md` |
| React query/cache/controllers for fnf | `references/fnf-react.md` + `references/auth.md` |
| Higgsfield-SDK app UI (generation console, fnf-backed tool) | `references/app-layouts.md` + `references/quanta-design.md` + `references/fnf-sdk.md` + `references/fnf-react.md` + `references/auth.md` (component gaps: build from Quanta primitives) |
| Cover / OG image ("cover", "обложка", "OG image", publish prep) | `references/app-cover.md` — branded 3:2 cover + capsule OG mask |
| Cover video / "animate the cover" (`og_video_url`, permission-gated) | `references/cover-animator.md` — ~5s end-frame reveal via `seedance_2_0` |
| App contest ("enter the contest", "$100k contest", `higgsfield website contest`) | `references/contest.md` — entry auto-publishes; submit with social links |
| Auth, current user, login/logout, `/api/user`, `__auth` routes | `references/auth.md` + `references/runtime-and-infra.md` |
| Protected/authenticated `/api/...` file downloads inside the Higgsfield iframe | `references/auth.md` — credentialed fetch → Blob download; signed URLs for large files |
| TanStack Start routes, SSR, server functions, Cloudflare Worker runtime | `references/runtime-and-infra.md` |
| Heavy / long-running work (ffmpeg, headless browser, background jobs), containers | `references/containers.md` |

Do NOT search the skill library for other design guidance — everything is here.

## Hard rules

### 0a. Higgsfield packages and template modules

The `app/packages/` directory contains managed snapshots vendored from the
upstream Higgsfield web app: `@higgsfield/fnf`, `@higgsfield/fnf-react`, and
`@higgsfield/quanta`. Do not edit these manually unless the task explicitly
asks to patch a package snapshot. Template-owned infrastructure lives in
`app/src/module/**`.

### 0b. Supercomputer Design mode inspector

Generated apps support a Higgsfield design inspector bridge for editing in
Supercomputer Design mode. The split is strict:

- The Higgsfield editor (parent window) owns the iframe UI, hover overlay,
  edit popover, origin/session checks, and edit prompt submission.
- This template owns the child iframe runtime through
  `app/src/module/design-inspector`.
- Agents never manually implement inspector code, refs, source markers, or
  `data-hf-*` attributes.

Local scripts: `bun run build` (inspector-free by default; set
`HF_DESIGN_INSPECTOR=1` in the env for the inspector-enabled build) and
`bun run dev:design` — for LOCAL work only. The platform CI sets
`HF_DESIGN_INSPECTOR=1` on every deploy build, so the live deployed site always
carries the inspector and IS the surface Supercomputer Design mode opens. There
is ONE deploy (`higgsfield website deploy <website_id>`) and it ships the live
public site immediately; never hard-code `HF_DESIGN_INSPECTOR=1` into the
`build` script or hand-edit the build scripts to toggle the inspector.

### 1. SSR-safe rendering
Every route renders on the server per request. NEVER touch browser-only
globals (`window`, `document`, `localStorage`, `navigator`) at module top
level or during render — only inside `useEffect`/event handlers, or guarded
with `typeof window !== "undefined"`. A top-level `window` reference crashes
SSR.

### 2. Server-only code stays server-only
Put server logic in `createServerFn(...).handler(...)` or a `*.server.ts`
module (the `.server.ts` suffix keeps it out of the client bundle). Secrets
and bindings are read **server-side, per request** — never shipped to the
browser.

### 3. Higgsfield (fnf) calls are BACKEND-ONLY — and auth is MANDATORY

Call Higgsfield internal services exclusively from server code at
`https://fnf.internal/*` (the platform attaches the user's identity on server
egress, so tokens never live in app code). NEVER call `https://fnf.internal/*`
from client components.

Every app is an authenticated surface. Before shipping you MUST implement the
Higgsfield auth contract exactly as written in `references/auth.md`: the
`GET /api/user` server proxy (returns the upstream status and JSON unchanged),
signed-out state that links to `/__auth/login?return=<path>`, and a server-side
auth re-check before every SDK operation. Logout remains platform-owned; do not
add an app logout endpoint or sign-out link. Do not invent your own login UI,
email/password form, or token handling, and do not build anonymous generation
flows unless the user explicitly asks for an offline/mock demo.

**Sign-in on the deployed site is platform-owned — do NOT improvise a cause if
it fails.** `/__auth/login` is a platform-injected route that hands off to
Higgsfield's auth service, then redirects back to `return` so `/api/user`
succeeds. If a user reports sign-in failing on a DEPLOYED SITE, FIRST confirm
the app side is correct (links to `/__auth/login?return=<path>`, proxies
`/api/user` unchanged); if it is, the failure is on the platform/auth side —
say so plainly instead of inventing an app-code cause.

If the app also needs its own user accounts (e.g. team members of the app's
customers), keep that separate — never replace Higgsfield auth with app-local
auth for generation.

Treat Higgsfield authentication, model-specific cost preview/confirmation, and a
usable generation feed/history as mandatory acceptance criteria for a generation
app. Workspace selection appears only when the selected account/SDK contract
requires it; wallet balance, account-credit, profile, and sign-out chrome remain
host-owned and must not be duplicated in the app.

Generation history cards must render SDK `Generation.results`, not status-only
placeholders. Compose result cards from Quanta `Media`/`Card` using the
helpers in `app/src/lib/higgsfield-generation-results.ts` (they map a
Generation to its preview URL with the right precedence). A completed job
without a result URL must show an explicit "preview unavailable" state with
refresh behavior.

When creating SDK clients, use only
`createWorkflowPlatformAdapter({ baseUrl: 'https://fnf.internal' })` — imported
from `@higgsfield/fnf/workflow-platform` (NOT `@higgsfield/fnf/adapters`; that
subpath no longer exists) — from server-side code. Do not use public/dev fnf
URLs, env-selected backend URLs, `createFnfWebAdapter`,
`createDevFnfWebAdapter`, apps-marketplace adapters, bearer tokens, or dev
user headers in generated app code.

Generation submits require the SDK's confirmation gate: a browser confirmation
modal (model + settings + cost preview) before the generate call, and the
adapter's `confirm` option wired server-side. A declined confirmation is the
typed `confirmation_rejected` error — render it as a cancelled state. See
`references/fnf-sdk.md`, "Submission Confirmation Gate".

### 3a. An app is end-to-end — real backend + real DB, never a mock

An app MUST ship as a real, end-to-end product — NOT a front-end mock,
prototype, or "demo" that fakes the backend. All three are required:

- **A real backend.** Every data operation runs through a TanStack **server
  function** or **server route** — fnf calls server-side, reads/writes
  server-side.
- **Real persistence (D1).** Opt into D1 (`"db": true` in
  `app/app.manifest.json`) and persist the app's OWN product state:
  saved/favorited generations, collections, presets, share records, settings.
  Schema in `app/migrations/000N_*.sql` (additive; rule 5).
- **Real fnf integration.** Generations, media, profile, and credits come from
  the live SDK against `https://fnf.internal`, never hardcoded fixtures.

fnf is the source of truth for the generations themselves — do NOT mirror
fnf's tables into D1. D1 is for YOUR product layer on top.

**These are NOT a backend and are bugs:** in-memory arrays or module-level
state as "the database"; `localStorage` as the persistence layer;
hardcoded/fixture/`lorem` data; a static JSON file faking a list endpoint;
`setTimeout` faking latency; memory/mock SDK adapters shipped as the product.
The ONLY exception is when the user **explicitly** asks for an offline/mock
demo — then say plainly that it is a mock and why.

### 4. Cloudflare bindings via `cloudflare:workers`
Any infra you opt into (D1 `DB`, R2 `STORAGE`, KV `KV`) is read server-side
through `app/src/lib/bindings.server.ts`
(`import { env } from "cloudflare:workers"`). Each binding is present ONLY if
declared in `app/app.manifest.json`, so the typed accessors are optional —
guard before use. Do not thread `env` through React props or read it at
module top level.

### 5. Opted-in storage is LIVE — one deploy, one database
If you opt into D1, R2, or KV, each is a SINGLE instance backing the ONE live
deploy. There is no staging copy: every migration and data change hits **live
production data** directly. `env.HF_ENV` is always `"production"` on deployed
builds; there is no separate database/bucket to test against. A destructive
migration you run "just to test" destroys **production data**. Prefer additive
migrations (`CREATE TABLE IF NOT EXISTS`, `ADD COLUMN`), and get explicit user
approval before any destructive change.

### 6. `app/app.manifest.json` declares infra — NOTHING is provisioned by default
A new app gets **no D1, no R2, no KV, no Durable Object**. Opt in only when
the app actually needs it: `"db": true` → D1 (`env.DB`); `"r2": true` → R2
(`env.STORAGE`); `"kv": true` → KV (`env.KV`); `"durableObject": "ClassName"`
→ a Durable Object (`env.ROOMS`, ALSO `export class ClassName extends
DurableObject {…}` from `app/src/server.ts`); `"container": true` → a Docker
container for heavy/long-running work (`env.CONTAINER` —
`references/containers.md`). Counts are capped (≤1 each); the platform
provisions and binds at deploy; the committed `app/wrangler.jsonc` is
build/dev input only. **KV is eventually consistent** (NOT Redis) — use a
Durable Object for strong consistency.

## Editing map
- Pages / routing → `app/src/routes/**` (file-based; `__root.tsx` is the shell).
- Server logic → `createServerFn` (see `app/src/lib/api/example.functions.ts`)
  or `*.server.ts`.
- Bindings access → `app/src/lib/bindings.server.ts`.
- Infra declaration → `app/app.manifest.json`; `app/wrangler.jsonc` = build/dev
  input.
- Components → Quanta components first (`@higgsfield/quanta/*` — Button,
  Input, Textarea, Dropdown, Modal, Tabs, Sidebar, Chip, …), app-local
  composition in `app/src/components/**`; layout per
  `references/app-layouts.md`; gaps → your own component from Quanta primitives.
- Generation result UI → compose from Quanta `Media`/`Card` +
  `app/src/lib/higgsfield-generation-results.ts`.
- Styles / theme → `app/src/styles.css` (Tailwind v4 + Quanta wiring).
  Quanta's `q-` tokens ARE the theme; the app is permanently dark.
- D1 schema → `app/migrations/000N_*.sql` (additive; see rule 5).

## Deploy, publication, and contest gates

The trusted platform CI performs the authoritative build on deployment. The
sandbox cannot deploy or migrate; a deploy ships the live public app with no
preview.

**Deploy only when explicitly authorized.** The local app build or a feed-listing
opt-in does not grant deployment permission. Apply steps 6–8 above; check
`higgsfield website status` before describing the app as live.

**Feed publication is separate.** `higgsfield website publish <website_id>`
lists the currently deployed app; it does not deploy or repair metadata. A feed
opt-in authorizes that listing only. Complete required metadata and use approved
assets. Missing assets or permissions block publication: request only the
missing authorization, and do not generate, spend, upload, push, deploy, or list
without its separate scope.

Required metadata: `og_title`, `og_description`, `favicon_url`, `og_image_url`,
and `marketplace_cover_url`. Reuse user-approved assets and compose them with
the deterministic local tool in `references/app-cover.md`. Any new image,
edit, cutout, or upscale uses an eligible executor and separate operation
authorization; output upload/storage is also separate. Verify the actual two
required files from the compositor; do not assume one provider generation
returns both. `og_video_url` is optional and separately approved; offer it,
never generate it unprompted (`references/cover-animator.md`).

**Contest entry is another separate public action.** It may publish the app as
part of entry. Require explicit contest-entry authorization including that
effect; independently gate project creation, assets, push, and deployment.
Submit only for a live, metadata-complete app with the user's required public
social-post URLs. Follow `references/contest.md`.

Local type/build checks are optional; use them only for a changed dependency or
build configuration, to investigate a concrete build/type error, or when a
command requires local dependencies. CI remains the authoritative deploy build.

**Adding a dependency:** `bun add` (from `app/`); update and check the lockfile.


**Small edits to an existing app** (copy tweak, one component, styling fix): make
the local edit; deploy only with explicit live-deployment authorization.
