# Website/app asset-system — a coherent visual kit

The goal is a visual system grounded in the approved brief and user-supplied
assets, not the maximum number of generated images. This reference proposes
asset roles and composition guidance; it does not authorize remote generation,
spend, or upload.

**Eligibility and authorization:** build-time image creation, edits, cutouts,
outpaints and upscales are ineligible via Higgsfield in this package. If
authorized, use the eligible image executor (`codex-imagen` default); otherwise
report the blocked asset. Video (`seedance_2_0`), `multi_image_to_3d` GLB and
game audio are separate eligible provider operations, each requiring the
applicable package gate and explicit scope. The CLI examples below preserve
provider-contract shapes only; never run them as this package's image executor.

The job names and media flags below are preserved provider-contract references,
not an execution recipe. In this package, never use Higgsfield image jobs for
build-time assets. For separately eligible video/3D/audio work, first obtain
operation-specific authorization and consult the current CLI/model contract;
do not assume async submission, flags, upload behavior, or retries from this
historical inventory.

## Asset kit plan — select by brief, create only within authorized scope

**Precedence rule: the user's own assets always win.** Anything the user
provides (logo, brand marks, product photos, team photos, fonts, existing
icon set) is used as-is — never regenerate a replacement for something they
gave you. Generation fills the GAPS only. The one soft exception: if their
photos clash with the chosen direction, offer a re-grade of THEIR photos
(image-edit, boards as grade reference) — don't substitute generated
strangers for their real product/team.

Every prompt carries the locked palette (name the hexes/mood words), the
narrative spine motif, and "no text, no logos, no watermark" (you set type in
HTML). Download everything into `app/public/assets/` and reference
same-origin. Downscale: hero ≤2k, cutouts ~800px, icons ~256px.

**Baseline roles to plan, not a mandatory generation queue:**

1. **Hero visual** — choose the approved supplied asset or selected
   scroll-scrub media that serves the concept. If a required role is missing,
   plan only that asset operation. Multiple candidates and an interaction pair
   are optional and require explicit scope.
2. **Section plates and content imagery** — include only where the approved
   section plan needs them. Reuse supplied product/team/project material;
   never create fake testimonials, fictional product evidence, or placeholder
   content presented as real. Do not create stock-like filler for a section
   that works without it.
3. **Icons** — use a consistent library set for functional UI. Commission a
   custom set only when the brand/design requires it and the user authorizes
   that image operation; avoid generated icons when their small-size fidelity
   is not inspectable.
4. **Logo / monogram** — use the supplied logo. Create a replacement only if
   the user has none, the brief requires one, and a separate eligible
   image-operation authorization exists.
5. **OG image** — required before feed publication where the metadata contract
   requires it. Reuse an approved asset or compose from approved local
   materials; generating a new image is a separate authorized operation.
   Multi-page sites need distinct cards only where the route-sharing contract
   calls for them.
6. **Head kit** — create the favicon/app-icon files required by the actual
   platform contract from an approved high-resolution logo/mark. Do not
   generate or upscale an unapproved source. Verify the rendered 16px mark and
   platform safe zones; record any missing source that blocks a required file.

**Cinema-tier moving media (only when selected by the approved brief):**

7. **Video or scroll-scrub media** — the animated website uses the selected
   journey shape in `references/scroll-scrub.md`: one continuous film by
   default, or a multi-leg chain only after explicit opt-in. A user-selected
   non-animated treatment follows its own named technique instead. This section
   does not require extra hero-video generation, frame extraction, or an
   interaction pair. Verify the model's current roles and output contract, and
   obtain separate authorization for each video operation, input upload,
   output count, and cost before work starts.

**Spectacle tier adds:**

8. **3D subject** — an approved image may serve as a source for a GLB workflow
   only when the brief requires a 3D scene and the user separately authorizes
   the selected eligible 3D model, source upload, output, and cost.


## Optional personalization assets

When the brief has few supplied assets, propose a compact set that suits the
product. Create a missing asset only after its executor, spend and upload
permissions are authorized. Optional categories are comparisons, not mandatory
counts or evidence of improved user experience.

- **Brand identity kit** — a mark, wordmark and monogram family if the brief
  needs them. Create through an authorized executor; do not replace a supplied
  user mark without explicit direction.
- **Animated logo sting** — optional 1–2s image-to-video mark animation;
  requires separate, eligible video authorization and reduced-motion handling.
- **Brand pattern / texture** — optional tileable motif; inspect the actual tile
  seam before use.
- **Spot illustration set** — optional consistent style for features, process
  steps or about sections. No fixed asset count.
- **State artwork** — optional 404, empty, success, confirmation or loading art
  where it serves a defined state.
- **People** — use approved real people imagery only with the required rights;
  label fictional representations clearly and never fabricate testimonial
  evidence.
- **Product views** — derive proposed angles/context from an approved source
  only within authorized scope. A reference does not guarantee identity;
  inspect each output and exclude unmatched views.
- **Restyling** — only with explicit rights and edit authorization for supplied
  photos; do not silently replace real product/team imagery.
- **Diagrams** — choose an image or implementation based on actual accessibility
  and maintenance needs; there is no universal image-first rule.
- **Brand sound** — optional audio, only with explicit audio-operation approval
  and a user-triggered, non-autoplay control.
- **Micro-animation** — optional clips or frame strips, only within separately
  authorized video scope and reduced-motion behavior.

Choose assets by brief and intended use; category count alone does not prove
coherence or improve user outcomes. List delivered assets and their verified
locations; identify missing work as blocked.

## Rules

- **Submission gate:** finalize the approved brief and board, then verify the
  executor, exact assets, cost/retry budget, upload permission, and operation
  scope before submitting. Do not queue work merely to avoid waiting.
- **Review the actual assets:** compare each output and the set with the brief,
  palette, composition, required text-free areas, and destination crop. User
  review is a separate acceptance step, not a substitute for file/render QA.
  Iterate only inside authorized retry scope; no fixed retry count overrides the
  approved budget. Report failures and unresolved mismatches.
- **Multi-image results:** check whether output is a grid or separate files
  before wiring assets; request count does not establish delivered file count.
- **Failures:** inspect the actual error and model contract. Change approach
  only within approved operations and retries; never evade safety filters or
  silently substitute stock, placeholders, or CSS approximations. Report a
  required unavailable asset as a blocker.
- **Rejected and intermediate files:** keep them out of the public asset
  directory; store them only in an authorized project location.
- **Icon-sheet background:** do not assume slicing removes its background.
  Remove/key it only with an authorized eligible executor or a real local
  deterministic method; report if neither is available.
- **Referenced assets:** ensure every delivered asset used by a route/component
  is tracked; remove or quarantine unused candidates within authorized scope.
- **Monochrome direction:** inspect actual pixels and exported color mode; a
  grayscale prompt alone does not guarantee grayscale output.
- **People imagery:** use approved, rights-cleared imagery and do not imply a
  real customer or testimonial when the subject is fictional.

