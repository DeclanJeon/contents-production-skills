# Video direction contract

Shared decision contract for the text-planning lane. `orchestrating-video-preproduction` applies it; the specialist skills follow its conventions when they run under that lane. It governs how creative choices are framed, recorded, and paused on — nothing else. `creative-production` owns project routing, shared state, and provider/spend approvals; this contract creates no project artifacts, calls no tools, and authorizes no spend.

## Interaction modes

- **Collaborative** — the default for multi-stage planning. Reuse answers already supplied, resolve consequential creative choices with the user, and pause at the checkpoints below. Asking for a video or a full package grants no approval for any proposed direction.
- **One pass** — only when the user explicitly delegates creative choices or asks to proceed without intermediate questions. Produce the requested work with labeled proposals and assumptions; ask only when constraints collide badly enough to block a valid result. This mode waives creative pauses, never the production/spend boundary.
- **Single artifact or locked brief** — when the direction already exists or does not matter for the artifact, deliver it without ceremony. Interrupt only for a gap that would change the artifact itself; a character sheet, synopsis, or locked storyboard never grows into a project-wide interview.

Use the host's available structured question or dialogue tool when one exists; otherwise present numbered choices in the user's language. Group related questions together, give each a small set of options with a short trade-off, and mark a recommended option where one is defensible — including an "unsure; recommend for me" choice when useful. Users may answer freely. Never re-ask supplied or approved values.

## Recording choices

Every creative choice carries one status: **supplied** (the user stated it), **proposed** (the lane suggested it), **approved** (the user confirmed it), or **unresolved**. A recommendation is a proposal, not an approval. Record decisions once and reuse them; do not keep parallel copies that can drift. When an approved choice changes, show the downstream impact and reopen only the checkpoints it touches — an earlier creative approval never authorizes a changed scope or spend.

## The direction decision

Before drafting concepts, decide the direction on three independent axes:

- **Genre** — what kind of video this is. Genre does not determine tone.
- **Purpose** — what the audience should take away. Record one primary purpose and, if present, a secondary one; purpose is not the job of an individual beat.
- **Production method** — how it should look and be performed. Method is not a model, input type, or provider name; a hybrid production assigns each segment its own method while sharing one visual identity.

The axes are independent: a supplied value on one fixes nothing about the others, and the brief's own vocabulary takes precedence over any preset list. For an underspecified brief, offer two or three plausible direction combinations — each with a one-line trade-off — and ask which to develop, rather than committing silently. Missing evidence constrains what may be claimed, not which direction the user may choose.

## Shared brief

The lane keeps one canonical brief covering the direction axes, mode, audience, takeaway, format/runtime, message, fact status, constraints, anchors, and continuity decisions — the field list lives in `orchestrating-video-preproduction`'s SKILL.md so there is exactly one source of truth. This contract adds the discipline around it: capture each field once, carry it through every handoff unchanged, mark material assumptions where they first matter, and never let a later stage quietly convert a proposal into an approved fact.

## Checkpoints

Apply only the checkpoints inside the request; each has a clear exit condition.

| Checkpoint | Present | Exit |
|---|---|---|
| Direction | Known brief plus a small set of direction combinations, or the missing axis choices | User confirms a direction or explicitly delegates the choice |
| Concept | A small set of distinct concepts fitting the direction, each with its hook and trade-off | Selected concept; a supplied approved concept skips this checkpoint |
| Plan review | The requested later artifacts — storyboard and fixed visual anchors where applicable — with unresolved references visible | User accepts or revises before downstream work |

Production and results gates belong to the downstream execution owner, not to this lane; a planning approval is never spend approval. Reuse existing approvals instead of stopping again at a cleared checkpoint. A partial request needs no approval to omit unrequested stages. An unanswered checkpoint ends with the choices themselves — never with downstream artifacts.

## Handoff boundary

This lane ends at text artifacts and their review. Shot decomposition, model-specific prompts, execution, editing, and delivery are downstream work selected by `creative-production`; do not route or run them here, and do not expand delivery beyond the requested scope. When handing off, pass the direction decision, choice statuses, the canonical brief, and the continuity ledger — the receiving stage inherits them as-is rather than re-interviewing.
