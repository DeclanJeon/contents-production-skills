---
name: orchestrating-video-preproduction
description: Use for text-only video preproduction that spans multiple artifacts — a complete planning package or one idea carried from concept through synopsis, characters, and storyboard. Delegated planning lane under creative-production; returns text and generic image prompts, never media.
---

# Orchestrating Video Preproduction

This lane moves a single brief through whichever planning stages were requested while holding one premise steady across all of them. Answer in Korean unless told otherwise. Deliverables are structured text plus reusable image prompts; nothing here produces or claims images or video.

`creative-production` alone coordinates content and video projects. This skill is its delegated text-planning lane — on a standalone call, consult `creative-production` once to confirm scope and route, then perform only the requested planning. When work arrives already delegated, inherit the coordinator's brief, IDs, versions, and approvals: no call-backs, no re-routing, no second interview or approval ledger. Text planning alone never creates a project folder, `project.json`, stills, or a sample video. Anything beyond text — image-backed packages, generation, editing, delivery, publication — goes back to `creative-production` as a plan and handoff; this lane never executes or picks an executor.

## Choosing the stages

- **Package request:** run the applicable stages in sequence — concept/synopsis via `developing-video-synopses`, characters via `designing-video-character-sheets`, panels via `storyboarding-video`. If a sibling skill is not loaded, follow its `SKILL.md` in the same-named sibling directory (for example `../developing-video-synopses/SKILL.md`).
- **Single-artifact request:** invoke only the matching specialist and return only that artifact. Never build the full package, never ask permission to skip unrequested stages, never treat an omitted stage as an open question.
- Mapping is direct: concept or synopsis → `developing-video-synopses`; a character sheet → `designing-video-character-sheets` without inventing a synopsis; panels → `storyboarding-video` preserving any supplied synopsis.
- Applicability is mode-dependent: omit inapplicable characters and fictional plot elements, not explicitly requested planning artifacts. Character-free, factual and abstract briefs retain their requested concept, informational/visual synopsis, beat planning and panels without fabricating a cast or conflict.

For multi-stage work, first read `references/video-direction.md` in this directory — it holds the lane's interaction modes, direction decision, choice statuses, and checkpoints. The default posture is collaborative: settle direction and concept before drafting later artifacts, and let the user review the storyboard and visual anchors before anything downstream. Only an explicitly delegated one-pass request proceeds with labeled proposals instead of pauses. When running under `creative-production`, these checkpoints feed the coordinator's shared approval flow rather than forming a second ledger.

A checkpoint without an answer ends with the choices on the table — never with unapproved downstream artifacts. Supplied choices and existing approvals are always reused. Each specialist owns its artifact; a specialist's standalone question rules cannot override an active lane checkpoint. Regardless of mode, the lane remains text-only: no folders, no generation, no paid calls, no asset claims.

## The shared spine

One canonical record, captured once, reused verbatim by every stage:

| Field | Contents |
|---|---|
| Choices | Interaction mode; each decision's supplied/proposed/approved/unresolved status; the active checkpoint |
| Direction | Genre, purpose, production method as three independent decisions |
| Mode | Narrative, data/educational, personal/documentary, brand/business, abstract/mood, explanatory metaphor, or a justified combination |
| Goal | Primary purpose, any secondary purpose, the one audience takeaway/promise/question — or an explicit "unresolved" |
| Audience | Only what was stated; no invented demographics |
| Tone | Requested register plus explicit exclusions, tracked apart from genre and method |
| Format | Supplied platform, aspect ratio, runtime only; unspecified stays unspecified |
| Message and facts | One governing message; every claim tagged as supplied/verified, derived arithmetic, interpretation, proposal, unverified, or unknown |
| Constraints | Dialogue, CTA, ending, and content limits; delivery scope; the no-generation boundary |
| Characters | Supplied identities, roles, goals, relationships, approved visual invariants; unknowns left open |
| World | Supplied setting, motifs, art direction, labeled staging proposals |
| Continuity | Prop identity, color, condition, owner and hand, spatial direction, reveal order, intentional changes |

Mark a material assumption at the first artifact it affects. Nothing in the spine may drift — genre, purpose, method, names, audience, cause, runtime, role, tone, prop details, ending. A later stage may attach a clearly labeled visual proposal, but a proposal never becomes confirmed story fact, and a changed approval reopens only the checkpoints it touches.

## Running the stages

**Concept and synopsis** (`developing-video-synopses`): establish mode, audience, purpose, and a structure suited to them. A supplied confirmed synopsis is preserved, never rewritten for convenience. Factual and brand work keeps source facts, arithmetic, interpretation, proposed action, and unknowns in separate buckets. The program or brand is not automatically the hero — put the audience at center when the brief calls for it. Unsupported effects, capabilities, causes, and CTAs stay out.

**Character sheets** (`designing-video-character-sheets`): for each relevant character, preserve role, agency, relationships, and supported change; convert stated traits into filmable behavior and stable visual anchors; keep unknown demographics, history, and motive open. Use customer-as-hero or service-as-guide framing only when the brief calls for those roles, without invented service detail or personification. When the mode needs no character, note "not applicable" internally and skip the stage — a partial request does not surface that note.

**Storyboard** (`storyboarding-video`): once the spine or supplied synopsis is stable. Panels hold one readable beat each — a visible action or information change — with reveal order and continuity anchors. Panels are not shot timings, camera moves, clip splits, or model-specific prompts.

## Integrity standards

- **Factual and documentary:** only supplied or verified claims; derived arithmetic labeled as such; a count change never becomes causation, persistence, a future result, or a program effect; separate periods never sum into "unique participants." Slogans and open endings can imply persistence too — promise nothing that was not supplied.
- **Prompts cannot launder evidence:** if the text calls something unknown, its image prompt must not depict it. Numbers-only briefs get neutral graphics, not invented documentary scenes, people, equipment, facilities, or records.
- **Brand and business:** capabilities only with brief or evidence support; a next step only when requested or warranted; never fabricated contact details, urgency, social proof, guarantees, or outcomes.
- **Personal and documentary:** event truth and perspective preserved; no invented biography, no inferred diagnosis.
- **Fiction:** connective invention is allowed to stage the premise; optional designs stay labeled proposals; fixed endings, dialogue bans, and tone constraints hold.
- Craft techniques apply only within the mode and scope they serve; no craft framework is evidence about a real person, service, statistic, or event.

## Assembling the package

Once the applicable choices are approved — or immediately in one-pass mode — a full package returns:

1. **공유 스토리 스파인** — the canonical fields, including direction and choice status, with unspecified values shown as open.
2. **콘셉트·시놉시스** — brief, logline or concept, synopsis, ordered beats.
3. **캐릭터 시트** — one per relevant character, each with continuity anchors and one reusable image-sheet prompt.
4. **비주얼 바이블** — the consolidated character, product, location, palette, lighting, wardrobe, material, and continuity anchors, with proposals and missing references marked.
5. **스토리보드** — the requested panels, one readable beat each, per-panel image prompts, and an optional unified sheet prompt matching the exact panel count.
6. **일관성·미정 사항** — the consistency check, consequential unresolved choices, review status, and any requested handoff.

Sections the user excluded or never asked for do not appear. Prompts stay in Korean unless another language was requested. No generation status, no rendered preview, no fabricated asset reference.

## Final consistency pass

Before returning, test every stage against the spine:

- Direction, mode, purpose, audience, and takeaway agree; nothing fictional poses as fact and vice versa.
- Runtime, dialogue, CTA, tone, ending, and counts match across outputs.
- Character identity, role, goal, agency, traits, and relationships are identical in synopsis, sheet, and panels.
- Location, style, color, material, condition, possession, screen direction, and reveal order hold; every change happens inside a visible beat.
- Each claim traces to supplied or verified material or wears its label — arithmetic, interpretation, proposal, unknown. No unsupported aggregates, future-continuity slogans, or predictions; prompts carry no smuggled evidence.
- Scope matches the request exactly; shotlists and model-specific prompts remain downstream work.

When two explicit brief values collide, prefer the one tied most directly to the user's stated constraint and disclose the conflict rather than silently reconciling it. If the collision changes the premise and no conservative resolution exists, ask one concise question and complete every unblocked part.

## Handoff

Return or hand off the direction decision, interaction mode, choice statuses, stable panel sequence, Visual Bible, and continuity ledger. Requested next planning stages retain that context. Anything beyond this lane, including timed shot decomposition, model-specific prompts or execution, is handed to `creative-production`, which selects the downstream owner and provider. This lane does not route execution itself. Planning approval is never spend approval.
