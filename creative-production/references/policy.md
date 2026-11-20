# Policy layer (single source of truth)

Every skill in this package defers to this file for cross-cutting rules. If a
skill restates one of these rules, this file wins; fix the duplication rather
than the copy. Do not add a parallel approval ledger, a second intake, or a
rival authority table.

## 1. Authority hierarchy

Four decisions are separate and none implies another:

1. **Content acceptance** — the user accepts the artifact's content.
2. **Review readiness** — a reviewer/worker says the artifact is ready.
3. **Execution/spend authorization** — the user approves running a paid or
   external operation.
4. **Publication authorization** — the user approves publishing/delivery.

Record only authority the user actually supplied. Missing decisions stay
unresolved; silence is not approval. Workers may recommend readiness, never
impersonate user acceptance. Review readiness is not acceptance, execution
approval, or permission to run.

Creative direction that is open needs supplied, accepted, or explicitly
delegated authority, except that reversible open axes (platform/safe zone, tone,
length, structure, style) may proceed as labelled `inferred` proposals; a
proposal is never acceptance. Ask only for consequential choices unavailable
from tools or sources. Rights, execution, spend and publication approvals are
asked at their own gates, never at intake and never inferred.

## 2. Scope boundary

A coordinator activates only for an explicit request inside its own boundary.
A related subject or incidental mention is not enough. Loading or considering a
skill never creates folders, files, projects, media, or spend. Do not create
workspace folders as a side effect of routing.

Once the requested deliverable is returned, stop. Coordinate does not enlarge
the request: only the requested artifact, stages, and depth.

## 3. Read-only and no-generation probes

A read-only / no-generation probe stays constrained for the whole turn. A later
request in the same turn does not release it. Name the conflict and ask for
explicit release before any media call or side effect. The same holds for a
text-only request that says "render later": "later" is a handoff requirement,
not authorization to render now.

`text_only` forbids new image/audio/video generation, not an explicit MD/PDF
file request. Saving is an independent axis: `no-save` / `read-only` / `chat-only`
forbid writes; an explicit MD/PDF request opens only that text-file stage and its
history, never new media. Do not auto-save an unspecified text-only request.
If a file request conflicts with an explicit no-save/read-only constraint,
report the conflict rather than silently releasing either constraint.

## 4. Single writer

Exactly one canonical state writer exists per project: the coordinator. Workers
return proposals; they never write the ledger or the history. One
`project.json`, one chronological `.history`. Package manifests, support
manifests, and derived adapters are not production ledgers.

Domain bibles and provider adapters are linked versioned artifacts, not
rewritten schemas. Do not build a parallel schema or rival approval ledger.

## 5. Evidence and provenance

Separate evidence, calculation, interpretation, and proposal. Mark inferred
assumptions `inferred`; never overwrite user-supplied values with inferences.
Unreadable or unavailable material stays `UNVERIFIED` — not failed, not passed.

Provenance claims need the actual submitted content: a file's existence, a
matching trait, a filename mention, or a hash label is not consumption
evidence. Record actual submitted prompts and actual input-reference hashes.

Schema success, file existence, and decode success are not visual quality,
continuity evidence, rights clearance, or user approval. Detector and tool
output enters as `DETECTOR_CANDIDATE`/`ESTIMATED` until inspected.

## 6. Execution gate

Only before an actual requested runtime/provider operation, verify the selected
runtime/auth, live schema/capabilities, destination, and rights/consent. Report
missing prerequisites. Installation is separate explicit scope — never
automatic.

`codex-imagen` is the default still-image executor; do not check price, usage,
quota, or block on unknown cost for it. Higgsfield image and AI Influencer
generation remain excluded. A selected route lacking runtime/auth/capability
gets an exact blocker report plus reachable preparation — never silent provider
substitution or fake output.

Parallelize only independent work. Dependency chains and uncertain async status
never justify duplicate paid submission. No extra retries, batches, covers,
training, analysis, or live deploy is inferred.

## 7. History lifecycle

The coordinator owns the history lifecycle as well as canonical state writes.
Log the operation's actual prompt and method before execution, then observed
outputs and the completed/failed/interrupted outcome. On resumption, inspect
pending operations, record the interruption/resume, and reconcile remote jobs
before retrying; interrupted orchestration is not provider failure.

Project completion requires the requested deliverables and exercised QA. It is
separate from operation completion.

## 8. Honesty about the runtime

Within one session, reuse only the same applicable sections actually read at
the same version/hash. A parent saying it read a file, a path mention, or file
existence is not consumption. New workers/sessions read their own mandatory
owners. Recheck execution gates when current inputs, account, model, native
roles or server revision change; no persistent capability cache is implied.

This package is instruction modules plus local tools. Markdown and agent
settings alone do not run workers, schedule stages, or persist ledgers. Actual
execution and recording are performed by the host and the coordinator. Never
claim an unperformed check, an unrendered geometry result, or an unreachable
provider backend as done.
