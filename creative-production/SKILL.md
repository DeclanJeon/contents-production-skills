---
name: creative-production
version: 2.6
description: Use when the user requests video production or a storyboard sheet for
  a video, including partial video work such as shorts/reels editing, re-editing
  existing video or extracting clips, video captions and lower thirds, ad or promo
  video scripts, and motion-graphics style for video. Do not use for standalone
  writing (including turning a video into an article or post), social posts,
  standalone images, ordinary design, application development, or audio-only work.
---

# Creative Production

Sole coordinator and sole state writer for video production. Skills here are
instruction modules; use the host's real tools and workers, not a presumed
scheduler.

## Step 0 — Upfront intake (once per new project)

For a new finished-video goal whose concept, format, narrative structure or
direction is still open, route R33 to `concept-intake-design` first: it judges
the nine intake factors, records reversible choices it can infer
(platform/safe zone, tone, length, structure, style) as `inferred` with a
one-line reason and continues, and returns a checked, scored concept packet. It
asks one batched turn only when a core axis cannot be inferred (no subject or
purpose) or the user asks to choose or discuss ("골라볼래", "같이 정하자").
Rights, execution, spend and publication approvals are asked at their own gates,
never at S01 and never inferred. The packet is an input, not a stopping point:
for a finished-video goal, continue in the same turn through the next eligible
stages (synopsis/script, storyboard, prompts/asset plan) to the first real gate
or explicit stop, then state exactly which approval is needed next; never end at
the packet with an optional offer. Later owners inherit it, never re-interview.
Skip Step 0 for a locked brief, an approved concept, a single named artifact, or
a resumed project. Pre-accepted review gates never open spend. The stage-by-stage owner
map and the CineForge CLI handoff contract are in
[skill-map.md](references/skill-map.md).

Still assets the story repeats (character 7-view sheets, wardrobe, location
4-view sheets, background plates, props, LOOK, cut start/end frames) are not
done when their prompts are written. Produce them under
[still asset generation jobs](../video-production-assets/references/32-still-asset-generation-jobs.md):
dependency order, at most five concurrent jobs, no automatic retry of an
uncertain job, and SHA-256 registration. Codex Imagen stills skip the paid-quote
gate, but reference transmission and output scope stay inside the user's
authorization; `available` is not `verified`.

## Step 1 — Goal, then current-stage route

For an ordinary new video request, retain the finished video as the project goal.
For an explicit limit, supplied-material workflow, or downstream-only request,
retain that scope instead. The goal does not grant execution or spend authority.
Select the current eligible stage separately; a route’s stop boundary ends the
assignment, not an unfinished project goal.

Read [routing.csv](references/routing.csv) and select exactly one `route_id`.
Columns: `deliverable_kind`, `media_axis` (text_only / none_or_stills /
executed_media / varies), `authority_axis`, `owner`, `required_read`,
`stop_boundary`.

Read [routing-disambiguation.csv](references/routing-disambiguation.csv) in the
same step. REQUIRED, not conditional. It holds one row per confusable
pair (`route_a`, `route_b`) and the line that separates them; do not re-derive
it from keywords.

State all three slots before naming a route; one chosen without them is a
keyword guess:

- **deliverable_kind** — which artifact the user asked for.
- **media_axis** — what media the request actually permits. Default `text_only`
  unless the user asked for generated media or an actual edit.
- **authority_axis** — which **spend or execution** approvals are already
  supplied. Empty means none, and paid media stays closed. An approved brief,
  storyboard or cast is an *input*, not an authority: write it empty and keep
  the approval in the brief, otherwise the money axis reads as already open.

Once the route is chosen, open [craft-bridge.csv](references/craft-bridge.csv),
take the rows for the current stage whose `when` fits the request, and read
those `craft_ref` files with the owner's own procedure before producing the
stage, whether you hand off or do it yourself. Owner rules and gates still win.

Craft triggers (attach only; route unchanged; bridge notes apply): ad/promo script:
[30](../video-production-assets/references/30-marketing-story-craft.md#od-openmotion-ad-script); sale/discount/product
promo, photo-only too: [19a](../video-production-assets/references/19a-product-promo-formulas.md); captions/lower
thirds/cover: [23a](../video-production-assets/references/23a-captions-layout.md); shorts/reels/multicam/beat-sync
edit: [09a](../video-production-assets/references/09a-short-form-edit-recipes.md); motion style/kinetic type:
[33 index](../video-production-assets/references/33-motion-style-library.md); motion principles/logo motion:
[08a](../video-production-assets/references/08a-motion-craft.md); model-specific video prompts:
[11a](../video-production-assets/references/11a-ai-video-prompting.md); recreate/templatize:
[29a](../video-production-assets/references/29a-template-recreation.md); illustration/hand-drawn story:
[still-motion-recipes](../storytelling-with-still-images/references/still-motion-recipes.md).

Then open the selected `owner` SKILL.md. Open every path in that row's
`required_read` too: it is a `;`-separated list of package-relative paths, and an
empty cell means the owner SKILL.md is the only file. These files authorise
the work; output from a route named without opening them is unsanctioned. Do not preload future craft, provider catalogs, or full-pipeline checklists. Two matches on one narrow artifact: pick the narrowest
and say which one you skipped.

For an ordinary finished-video goal, keep the goal in the coordinator and route
the next unfinished assignment, not the whole lifecycle: use R05 for needed
multi-artifact text planning and R24 only with current image-backed execution
authority. R14 is for explicitly requested film-lifecycle or stage-handoff
guidance. A local edit/export of supplied footage or adopted takes uses R31
and its own edit-plan gate. Assign selected authorized Higgsfield and Fal video
operations to R28 and R32 respectively; R32 resolves `fal-video-production`
from the host as a required optional owner before executing.

`UNASSIGNED` means no current-stage route fits. Say so and ask for the missing slot instead of
stretching a route.

## Step 2 — Apply policy

Read [policy.md](references/policy.md) for authority hierarchy, scope boundary,
read-only probes, single writer, evidence, execution gate, and history. This
package restates none of it elsewhere; if a skill contradicts `policy.md`, that
skill is wrong.

## Step 3 — Scope and stage

Preserve language, exclusions, fixed facts, selected tools, continuity, source
versions, and actual approvals. Reuse approved choices and the active interview
flow. For a finished-video goal, use the [goal progression contract](references/production-routing.md#goal-progression)
and hand off text planning in coordinator-delegated one-pass mode unless the
user requested collaboration. A named stop changes the stopping point, not
interaction mode: carry it in the handoff and work up to it. For “show me the
script, then wait,” deliver the script without a routine earlier question and
wait before downstream work. Actual blockers still apply.

For recurring production, multi-stage coordination, reuse of approved
resources, or repeated output corrections, **REQUIRED SUB-SKILL:
`ai-delegation-loop`** applies once here. Resolve it by exact name in the host's
available skill sources. If unreachable, record the missing source and leave
only the dependent coordination step unresolved. Record the roots checked once per session; do not repeat a failed
search until sources or configuration change.
Do not install, remove, or silently substitute this dependency.

When a request asks to apply craft already integrated into this package, use the
packaged procedure (for reference-driven production,
[R1–R8](../video-production-assets/references/29-reference-driven-production.md))
rather than asking for the original book. An unavailable original blocks only
fresh quotation or source inspection.

When a request names a technique or an external document's term (an `ST-01`-style
ID, "impact frame", "leitmotif", "whip pan"), resolve it through the
[directing vocabulary crosswalk](../video-production-assets/references/directing-vocabulary-crosswalk.md)
before drafting.

## Step 4 — Hand off

State one current stage, one owner, the exact requested artifact, and the actual
approver (or `unassigned`). Canonical handoff IDs and versions live in the
[worker handoff and single-writer contract](../video-production-assets/references/contract-core.md#worker-handoff-and-single-writer).

Build one compact packet: assigned stage/output/focus IDs; source IDs and
versions; locked facts, continuity, exclusions; approval references; required
inputs and blockers. For an existing ledger query/update, read
[project contract](../video-production-assets/references/contract-project.md).
Keep full execution projections on disk; display with `sequence_context.py
--shot <ID> --projection <full.json> --view focus`, never execute that display.
Do not infer a stage from file presence.
Carry the Step 1 craft paths as `craft_refs` (omit if none fit).

A worker returns indexed changes, actual evidence, and checks performed. When
dependencies are missing it also returns one indexed missing-input packet naming
each scene/shot/beat slot, the required input, and the blocker. Select each
missing owner from `routing.csv` once, integrate the return with inherited
IDs and versions, and resume the blocked stage — no second intake or re-route.
On a valid return, run applicable internal QA and take the next eligible stage
until the project goal or explicit stop is reached. A blocked stage does not
stop independent in-scope work.

## Step 5 — Persist and deliver

Read [workspace-integration.md](references/workspace-integration.md) before
applying storage, sibling paths, image execution, or provider instructions.

Use **REQUIRED SUB-SKILL: `recording-production-history`** before the first
content-file write. Reuse an existing approved, asset-complete project when one
is selected; otherwise resolve the user's Documents folder and initialize
`Media_Studio/<project_id>`. Ask once for a project directory before the first
saved production unless an active path, environment/config choice, or existing
default studio root already resolves it. Before reusing or resuming a root,
inspect its `project.json`, actual files, approvals, and `.history` in-flight
operations; missing files or pending work is not a clean restart.

Every intermediate and final output is saved outside this skill repository,
registered with observed paths, and reported by absolute path. Final
deliverables go in `final/`.

For a full topic-to-video or image-backed package, read
[preproduction-review.md](../video-production-assets/references/preproduction-review.md)
before project writes or media calls, and read
[production-routing.md](references/production-routing.md) for the
`R24` sequence detail, v5.1 asset gate, and finality rules.

Before whole-storyboard finalization, dependent generation/take adoption, or
sequence delivery, **REQUIRED:** apply the
[whole-storyline continuity gate](../video-production-assets/references/26-state-causality-continuity.md#storyline-continuity-gate).
The coordinator owns predecessor/history references and continuity acceptance
even without a separate reviewer. Required failed/unverified continuity blocks
dependent generation, take adoption and completed-film delivery; independent
reachable planning may continue. Planned references are not accepted take
outpoints.
For storyboard-to-video execution, dependent generation, or sequence editing,
**REQUIRED:** use the [sequence execution tools](../video-production-assets/references/sequence-execution.md)
to compare actual planned frames before generation, resolve blockers, carry selected
source ranges forward, and inspect the rendered cut boundaries and whole output.

When the deliverable needs voice or sound and nothing selects another route,
design voice and sound into the video request itself, per the canonical
[voice and sound design in-request](../creative-production/references/video-generation-planning.md#3b-voice-and-sound-design-are-in-request-by-default)
rule. Before any duration grouping or final video request, read
[storyboard timing to prompt](references/storyboard-timing-to-prompt.md) and
reconcile all board intervals with the actual submitted VISUAL/AUDIO schedule. A
5/10/20/30-second job changes grouping and local timestamps, not the approved
cuts, expression beats or dialogue.

Keep video-model/endpoint choice unresolved during preproduction. Current-version
review acceptance/readiness is not user acceptance, execution approval, or
permission to run video. Open the live-verified bounded plan under
[video-generation-planning.md](references/video-generation-planning.md) only
on an explicit proceed request or existing explicit authority covering that
plan. Submit only under current execution and applicable spend approval.

Use [creative-qa.md](references/creative-qa.md) for the requested surface.
Record file and `.history` paths internally as work proceeds. Share the relevant
paths, checks and lifecycle state at a requested checkpoint, a real blocker, or
delivery. A progress update is not an approval pause. Distinguish plan, generated file,
inspection, user acceptance, and publication. API success, prompts, empty
directories, and predictions are not delivery.
