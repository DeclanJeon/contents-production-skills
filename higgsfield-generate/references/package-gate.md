# Package gate — execution eligibility and canonical handoff

One shared source for every `higgsfield-*` skill in this package. Load it whenever a skill
reaches for an actual submission or delegation return; SKILL bodies hold only a pointer.
Preparation/text-only returns use the handoff section only: no auth, installer, model catalog or quote checks until an eligible actual execution is requested.

Authoritative parents (read when a conflict appears; this file summarizes, never overrides):

- **Execution/spend eligibility:** `creative-production/references/production-routing.md`
  [`#selected-runtime-gate`](../../creative-production/references/production-routing.md#selected-runtime-gate) and
  `video-production-assets/references/24-production-execution.md` (cost policy §1, image
  executor §2).
- **Worker handoff / single writer:** `video-production-assets/references/contract.md`
  [`#worker-handoff-and-single-writer`](../../video-production-assets/references/contract.md#worker-handoff-and-single-writer),
  schema `1.1`.

## Runtime check — never auto-install

1. Verify `higgsfield` exists on `$PATH` and `higgsfield account status` succeeds. A missing
   runtime or failed auth is a **blocker to report**, not a silent install. Installation is a
   separate operation only when the user explicitly requests it; the official installer is
   `curl -fsSL https://raw.githubusercontent.com/higgsfield-ai/cli/main/install.sh | sh` —
   offer it, never run it unprompted.
2. Inspect the live contract at execution time: `higgsfield model get <jst> --json`
   (plus `higgsfield model list --json` when routing is uncertain). Historical "verified"
   tables in this package are documentation, not current truth — no fixed price, ranking,
   capability, or availability claim is authoritative.
3. Auth success, installed CLI, visible credits, a paid plan, or a free allowance are NOT
   execution or spend approval.

## Entry gate — required before ANY actual submission

All of these must hold for each bounded batch of actual provider jobs:

1. **Eligible operation.** This package executes eligible video / audio / 3D / workflow /
   analysis operations on the current schema. Higgsfield **image generation and image edit
   recipes are ineligible in this package** — see "Image branches" below.
2. **Verified cost status.** Unknown cost blocks. For N bounded outputs the approval request
   itself presents the aggregate verified quote (style key + all N jobs + auxiliary jobs +
   retries, N × current unit or verified quote) BEFORE submission; only approval bound to
   that summary is valid, and a changed N makes it stale. Included/free-allowance paths still
   need execution-scope approval.
3. **Bounded approval.** Approved counts, settings, retry ceiling, and cost ceiling bind the
   run. Retries stay inside the approved `retry_budget` — a local "retry twice" habit is a
   workflow limit, not authorized spend. Auxiliary operations (training, style keys, covers,
   analysis, reference creation) are each authorized operations inside the approved scope,
   never free riders.
4. **Current inputs.** Delegated input artifact/asset IDs and versions must still be current.
5. **Supplied choices reused.** A supplied or approved choice (model, style, voice, duration,
   cover) is consumed as-is — validated against the live contract, never re-interviewed. Ask
   only what is materially unresolved. A native aesthetic/model/style selection is NOT
   execution or spend approval; "you choose" does not approve cost.

## Image branches — craft/reference only in this package

Package policy (production execution §2) excludes Higgsfield image generation/editing even
when the user selects it or free credits exist: no `generate create` or dedicated command may
submit an image-generation or image-edit job, regardless of model. The image craft in these
skills — model selection tables, mode taxonomies, prompt contracts, CLI shapes — is preserved
as craft/reference for use elsewhere; it is not executable here.

- **Existing images are eligible inputs** where the operation permits: supplied local files,
   extracted frames, CMS-imported media, prior uploads/jobs referenced as media inputs.
- **A missing required image goes to an explicitly authorized eligible image executor**
   (`codex-imagen` is the package default), with truthful scope: report what the substitution
   cannot reproduce. No silent fallback, no widening into a different recipe.
- **No fake backend equivalence.** Skill-specific backend enhancers (private prompt templates,
   marketplace-compliance logic, enhancer pipelines) are NOT reproduced by renaming a generic
   image model. When the backend path is ineligible, report the original backend execution as
   blocked, and offer the authorized executor only as a truthfully-scoped alternative —
   never as "the same" workflow.
- Provider UUIDs, URLs, and `reference_id`s produced by image operations are locators, not
   canonical assets; see the handoff join below.

## Delegated work — canonical handoff

Follow `#worker-handoff-and-single-writer` in `contract.md` (schema `1.1`).

**Inbound:** consume the selected project root/id/version (when one exists), the assigned
stage and requested output, assigned focus IDs, input artifact/asset IDs + versions,
continuity/exclusion constraints, and referenced approvals. Reuse these values — do not
re-interview. A request without a selected project is standalone work.

**Outbound (internal return, not the user-facing reply):**

- assigned output IDs + version: artifact/asset/shot/block/panel IDs the coordinator assigned,
  or a proposed registration when the stage creates new outputs;
- `dependency_versions` proposal for consumed input versions;
- actual local file paths + hashes when obtained, and **provider locators** (job UUIDs, upload
  IDs, `reference_id`s, website IDs, `folder_id`s) mapped to the canonical IDs they back;
- observed terminal status, inspection evidence and its limits, measured cost/attempts;
- assumptions, remaining blockers, changed-record proposals.

**Locator discipline:** `generation_attempts.result_asset_id` must resolve to a real canonical
available/verified asset — never a bare provider UUID or URL. Provider mappings are linked
adapter/domain data (kept with the skill's own state where one exists), not a rival production
ledger. The coordinator is the sole `project.json` writer; workers never write it or any
second ledger.

**Ledger helpers are the coordinator's, not yours.** `video-production-assets/scripts/project_index.py`
is a read-only derived view of a selected shot/artifact's cross-references — context for the
current stage, never a second ledger and never a way to guess the stage from file existence.
`update_project.py` is a coordinator-only delta writer; workers return changed-record
proposals, they do not run it.

**Explicit entity joins.** When the coordinator allocates typed entities, return them explicitly:
a narrator/voice selection joins the allocated `voice_profile` entity (plus the provider
`voice_id`/`voice_type` locator); a numeric camera/spatial input is a `camera_spec`/`spatial_spec`
artifact, story sources are `synopsis`/`script`/`beat_map`. Do not smuggle provider IDs into
those typed fields.

**Standalone one-off work** creates no project and allocates no invented canonical IDs:
deliver the media and locators directly.
