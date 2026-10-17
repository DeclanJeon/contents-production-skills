# scroll-scrub — the animated website (`--type website` only)

This is the **animated website** — the DEFAULT Tier-1 experience for every
`--type website` build. The visitor's scroll plays a generated film while the
page's semantic chapters read over it. By default that is ONE continuous film
(`single-shot`); a multi-scene seam-locked chain is opt-in. Follow this
reference for every website unless the user EXPLICITLY asked for a different
treatment (in which case pick a technique from `references/wow-catalog.md`
instead). It is also the reference for any brief that asks for a scrollable
world, continuous camera journey, diorama fly-through, or browse-through-the-
industry site. In catalog terms this is **A4 — Seam-locked scroll scrub**.

This is a specialized website build, not a Higgsfield app. Media generation,
provider spend, and source-file upload each require their own explicit
authorization under the package gate; this reference does not authorize or
perform those operations. The deployed site uses local assets only, performs no
runtime generation, uses no fnf SDK, and includes no Higgsfield branding.

The bundled Markdown assets provide an SSR-safe React/TanStack implementation,
layout contract, and deterministic video helper. Keep them in `references/`;
materialize only the fenced code needed by the generated site.

## Fit it into the existing website pipeline

Keep the single intake call and every normal website phase. Do not add a second
interview. Resolve missing details in the existing intake or choose defaults in
the design brief.

### Phase 0 — lock the journey

This is the journey block that `Animation mode: animated-website` obligates (see
`references/website-flow.md` Phase 0). The brief is INCOMPLETE — a hard stop —
until these decisions are written into `app/design-brief.md`; the Phase 5 gate
(item 9f) checks that the Journey shape and Journey are present. Write:

#### Journey shape — pick ONE (this is the big cost lever)

- **`single-shot` — the DEFAULT.** ONE continuous ~15s film, generated in ONE
  call, scrubbed end to end. No seams, because there is only one clip. The
  chapters are HTML that read over it. Choose this for a brand, a product, a
  service, a portfolio, a launch — anything whose story is one subject seen
  ever more closely. **When in doubt, single-shot.**
- **`multi-leg` — informed opt-in only when the brief genuinely needs several
  WORLDS.** It means 4–7 distinct environments, one video operation per leg, and
  sequential handoffs with boundary inspection. Before the user chooses it,
  disclose the planned operation count, time, and verified aggregate cost
  before selection. If a current quote is unavailable, stay with `single-shot`;
  a budget cap is not a verified quote or authorization to submit.

"It would look cooler with more scenes" is NOT a reason for `multi-leg`. A
tighter single-shot film beats a loosely-seamed chain, and it reaches the user
far sooner.

- **Journey:** for `single-shot`, 3–6 chapters mapped to moments of the one
  film; for `multi-leg`, 4–7 scenes as a real narrative or value chain. Give
  each a physical subject, one focal point, one short headline, one sentence,
  and at most 0–3 proof tags. Keep the existing eyebrow ratio; do not turn
  every scene label into an eyebrow.
- **World grammar:** lock one byte-identical style preamble, perspective,
  palette, light direction, surface finish, and background behavior across all
  scene prompts. Change only the scene subject and focal action.
- **Camera architecture** (`multi-leg` only): choose A or B below. Default to A for grounded,
  realistic, architectural, product, and first-person work. Use B only when
  the world is explicitly miniature, isometric, map-like, or toy-like.
- **Mobile framing:** include mobile by default, without another question.
  Keep every focal point inside the center-safe area and plan lighter mobile
  encodes. Use a separately generated portrait source only when center-safe
  composition cannot preserve a critical scene.
- **Cost shape:** for `single-shot`, one storyboard image plus ONE film. For
  `multi-leg`, record one entry image plus `N` sequential video legs for A,
  or `N` scene images plus `N` dives and `N-1` connectors for B. The per-scene
  Phase 1 boards already art-direct A's destinations; do not buy unused
  destination stills that cannot participate in its exact-frame handoff. This
  is a deliberate media-heavy cinema build.
- **Delivery budget:** record an aggregate byte budget in the brief. Start at
  ≤32 MiB for all desktop clips and ≤16 MiB for all mobile clips; shorten or
  re-encode before relaxing it.

## The footage contract — what makes a scrub look expensive

The page plays the film forward AND backward at the speed of the user's scroll,
and holds any single frame as a still whenever they pause. That dictates the
footage. Direct it like a high-end product film, and obey these or the scrub
looks broken regardless of how good the render is:

- **One continuous move — no hard cuts.** A cut becomes a jarring jump
  mid-scrub. Stage it as a single unbroken camera move (slow orbit, push-in,
  rise, fly-through) or one continuous transformation of the subject.
- **One hero subject, kept centered, with clean negative space** around it —
  that space is where the chapter copy sits. The video fills the viewport and
  crops the edges (`cover`), so keep the subject center-safe.
- **A background the copy can survive.** Dark, seamless, low-detail (studio
  black/charcoal, a soft gradient, the subject emerging from darkness) is the
  reliable choice. A bright, busy, full-frame environment behind body copy is
  the single most common reason a beautiful film reads as unusable.
- **Slow, steady motion** — constant speed, gentle ease only at the very start
  and end. The scroll supplies the pacing.
- **Locked exposure and white balance, no flicker; minimal motion blur.** Every
  frame is shown as a still, so exposure pumping shimmers and heavy blur smears.
- **Resolves at both ends:** the first frame reads as the establishing shot, the
  last as the closing beauty state. START state ≠ END state, or the scrub has no
  payoff.
- **No on-screen text, logos, or watermarks** — all type is HTML over the video.

Subjects that scrub beautifully: a product slowly orbiting on black; an
exploded-view assembly; a macro detail traveling along a surface; a
transformation or morph; a hero object emerging from darkness. Avoid: cuts,
fast pans, handheld shake, busy bright backgrounds, and colour/exposure flicker.

### Phase 1 — prepare visual references for the chosen journey shape

For `single-shot`, make one 16:9 six-panel storyboard of keyframes from one
continuous camera move, not separate worlds; include no text in the image. Reuse
approved website reference boards for art direction. For opt-in `multi-leg`, use
the planned 4–7 world scenes and create only the needed scene references,
following the approved asset plan and separate image-operation gate.

Keep focal subjects within the mobile-safe area. Create a portrait source only
when visual inspection shows center-safe cropping cannot preserve a required
focal point; authorize that extra image operation separately.

**`single-shot` uses ONE storyboard**, not per-scene source stills. It is one
16:9 six-panel image showing keyframes of a single continuous move, with no
text. Reuse an approved user-supplied storyboard if it fits the brief; inspecting
or using a local supplied asset does not require image-generation authorization.
If a storyboard is missing or unsuitable, create or revise it only through the
eligible executor after explicit authorization for that image operation, model,
inputs, output count, and disclosed cost. Inspect the actual result. Each re-roll
is a separate generation requiring its own authorized scope. If no suitable
storyboard exists and its creation is not authorized or available, record that
blocker; any separate provider upload also requires explicit authorization.

### Phase 2 — generate the film

Use only a verified, currently available eligible video executor. Before each
submission, obtain explicit authorization for that media operation, the
selected model, its input uploads, output count, and disclosed cost; follow the
package gate. Command examples are provider-shape guidance, not proof of CLI
availability or permission. If prerequisites are missing, stop that operation
and report the exact blocker.

#### `single-shot` (the default) — ONE film, no chain

1. Read the current model schema from a trusted source and confirm the required
   video/reference roles. Do not rely on remembered model capabilities.
2. After the operation gate is satisfied, submit one film job with the
   authorized storyboard as a look reference (not a start frame unless the user
   approved that behavior). Ask for a continuous move, no cuts, stable exposure,
   no camera shake, and no on-screen text; request duration, aspect ratio, and
   quality within the quoted/authorized limits.
3. The launch cover/OG is a separate required-by-deployment asset role, not an
   automatic generation companion. Reuse an approved asset or obtain separate
   cover-operation authorization through `references/app-cover.md`. Do not
   infer permission to generate it from film authorization. Build the page while
   authorized media is pending; download and encode only confirmed outputs.
   Inspect the returned film and encoded clip for visual quality and technical
   suitability. There is one clip, so there are no inter-clip seams to inspect.

#### `multi-leg` — the seam-locked chain

1. Verify the currently selected model's schema and documented image/video
   media roles. Do not infer command flags or role compatibility from examples.
2. Plan and authorize only the independent stills required for the chosen A/B
   architecture; do not regenerate supplied approved art. Independent stills
   may run in parallel only if each operation is separately authorized. Hold
   prompts, model, output count, input uploads, and cost to that authorization.
3. Use only confirmed outputs as inputs. Keep source stills in scratch space;
   runtime posters come from the exact encoded clips, not imagined frames.
4. After boundaries exist, submit each dependent video/connector leg in order,
   with separate operation authorization and cost disclosure. Never start a
   downstream leg until its exact required frame exists and has been inspected.
5. When authorized source MP4s are available, read
   `references/scroll-scrub-asset-video.md` and use its deterministic helper
   for boundary frames and scrub encodes:

   ```bash
   bash /tmp/scroll-scrub-video.sh bounds source.mp4 /tmp/scene-a
   bash /tmp/scroll-scrub-video.sh desktop source.mp4 app/public/assets/world/scene-a.mp4
   bash /tmp/scroll-scrub-video.sh mobile source.mp4 app/public/assets/world/scene-a-mobile.mp4
   bash /tmp/scroll-scrub-video.sh poster app/public/assets/world/scene-a.mp4 app/public/assets/world/scene-a-poster.png
   bash /tmp/scroll-scrub-video.sh poster app/public/assets/world/scene-a-mobile.mp4 app/public/assets/world/scene-a-mobile-poster.png
   ```

   Confirm every input/output path and inspect actual boundary images before
   using them. Upload a frame only with explicit file-upload authorization;
   local files are not implicitly upload-approved.

#### Architecture A — continuous forward flight (opt-in multi-leg)

Generate each authorized leg sequentially. Use the approved scene-1 still only
if the verified model schema supports that role. Inspect the actual last frame
before separately authorizing and submitting the next leg; use that exact frame
only when the next operation is authorized to upload it as an input. Reject and
re-plan any boundary whose subject, direction, or motion makes the handoff fail.
Do not use a board or imagined destination still as a handoff. Position and
velocity continuity both require visual review. Wire the legs directly; there
are no connector clips in architecture A.

#### Architecture B — diorama dives plus aerial connectors

Use only when the explicitly selected multi-leg architecture pulls back to a
world map. Authorize each independent dive before submission; extract and
visually inspect its actual boundaries. Each connector is a dependent,
separately authorized operation that may start only after its required boundary
frames exist and are approved for input upload. Use only the exact
start/end-reference roles documented by the selected model. Make each
authorized connector pull out of scene `i`, cross the connected miniature
world, and begin descending into scene `i+1`; do not batch or infer permission.

Require both equalities at every join:

```text
dive[i].last pixels == connector[i].start pixels
connector[i].end pixels == dive[i+1].first pixels
```

Use a very short crossfade only as insurance against encoder/model drift. A
crossfade cannot repair a wrong endpoint or the grounded-world rewind created
by a forward dive followed by a backward pull-out; switch that concept to A.

### Encode direct MP4s for scrubbing

Scrub the optimized MP4 chain directly. Do not export thousands of frame images
for A4.

- Desktop: preserve native resolution, H.264/yuv420p, CRF about 20, GOP 8,
  scene-cut keyframes disabled, audio removed, `faststart` enabled.
- Mobile: cap height at 720px, CRF about 23, GOP 4, audio removed, `faststart`
  enabled. A tighter GOP reduces decoder work during repeated seeks.
- Extract a mandatory poster from the first frame of every final desktop clip,
  including connectors. Extract `mobilePoster` from every mobile clip. Never
  substitute the next scene's still or show a black video box while a clip
  downloads or before iOS paints its first decoded frame.
- Store only selected, encoded assets in `app/public/`; keep raw clips,
  boundary frames, and rejects outside public assets.
- Measure both encoded chains against the brief's aggregate byte budget. The
  controller retains visited Blob assets to keep reverse scroll smooth, so
  oversized clips become memory cost as well as transfer cost.

For this design, the approved entry still, encoded segment posters, and chained
MP4s provide the hero/media treatment. Plan other site roles (logo, icons,
section imagery, OG) from `references/asset-system.md`; reuse approved assets
and generate only missing required items after separate operation
authorization. Do not create a redundant second hero film.

### Phase 3 — assemble the SSR-safe React page

Read both bundled code assets and adapt them:

- `references/scroll-scrub-asset-react.md` — semantic React chapters plus the
  scrub controller (lazy nearby clip loading, Blob seekability, seek
  coalescing, iOS priming, mobile sources, active-section navigation, full
  teardown).
- `references/scroll-scrub-asset-css.md` — layout contract only. Replace its
  composition values through the design brief; do not add generic shared CTA
  chrome.

Extract the fenced sources into
`app/src/components/scroll-scrub/scroll-scrub.tsx` and
`app/src/components/scroll-scrub/scroll-scrub.css`, then provide real scene
data. Render each scene's CTA as its own `actions` node/component from the
brief's CTA inventory. Keep all chapter copy server-rendered in ordinary
semantic `<article>` flow; the client controller owns media time only. Never
drive per-frame values through React state. Keep the `scenes`/`connectors`
arrays as module constants or memoize them in the parent; changing their
identity intentionally rebuilds the controller.

The React asset intentionally does not build a header, generic button system,
scroll hint, or one eyebrow per scene. Compose the site's own nav and bespoke
CTAs around it. Keep the media controller inside `useEffect`; no browser global
may run during SSR.

### Phase 4 — motion and interaction

Let the A4 controller own scroll-to-video time for the scrub stage. Keep the
normal Lenis-to-GSAP ticker bridge for other cinema motion, but do not attach a
second scrub timeline to the same video elements. Use transform-only entrance
motion for surrounding chrome, keep chapter copy fully rendered, and preserve
the initial poster before client initialization.

Support reverse scroll as a first-class path. Every seam that works only in the
forward direction is still broken.

## Runtime requirements

- Fetch same-origin clips to Blob URLs before scrubbing so `currentTime` remains
  seekable even when byte-range behavior differs. Fall back to the poster if a
  clip fails.
- Add `blob:` to the site's CSP `media-src` because the controller assigns Blob
  URLs to `<video src>`. Keep clip fetches same-origin, with `connect-src 'self'`.
  A CSP that allows only `media-src 'self' https:` is incomplete here.
- Load only the active/nearby segment, keep its poster until `loadeddata` plus a
  real painted/seeked frame, and coalesce seeks while `video.seeking` is true. A
  failed source settles on its poster without a retry loop.
- Prime muted inline videos on the first pointer/touch gesture for iOS, then
  pause them; scrolling controls time, never autoplay.
- Ignore touch-browser height-only resize events caused by URL chrome; relayout
  on width/orientation changes and replace an already loaded desktop/mobile
  Blob when the selected source changes.
- Respect safe areas and use `dvh`. Keep focal media center-safe on mobile.
- Under `prefers-reduced-motion`, skip all video fetch/decode and present the
  same semantic chapters over static posters.
- On unmount, abort pending fetches, remove listeners, cancel animation frames,
  remove created video nodes, and revoke every Blob URL.

## A4 pre-deployment QA

Complete all normal Phase 5 checks and exercise the animated page in an
actually reachable browser preview before deployment. A source inspection is
not runtime proof. Do not deploy solely to enable QA, even with deployment
authorization. If no safe authorized preview is available, report the
unverified behaviors as blocked and do not deploy.

- For `single-shot`, verify the one clip's scroll-linked `currentTime`, reverse
  scroll, fast-flick seeking, and first-frame poster behavior. There are no
  inter-clip seams or A/B architecture to validate.
- For opt-in `multi-leg`, inspect every actual frame handoff in both scroll
  directions; verify A's forward velocity continuity or B's intentional
  miniature/map pull-out. Check seam playback on the rendered clips, not from
  source-code structure.
- Desktop selects desktop encodes; a 375px/coarse-pointer viewport selects
  mobile encodes. Test portrait crop, safe areas, rotation, and a 4–6×
  CPU-throttled fast scroll.
- Reduced motion performs zero video fetches and keeps the full story usable.
- Route buttons are keyboard accessible, active state is not hover-only, and
  chapter headings remain in DOM/reading order.
- Browser unmount/remount produces no duplicate listeners, live RAF loop,
  stale video node, or unreleased Blob URL.
- Measure desktop/mobile clip totals against the brief's byte budgets; verify
  requests and decoder behavior under network throttling as well as CPU
  throttling. Record checks that could not be exercised; never infer success
  from read-only code inspection.
