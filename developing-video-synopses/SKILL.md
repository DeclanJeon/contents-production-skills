---
name: developing-video-synopses
version: 2.1
description: Use to develop a video concept, logline, synopsis, plot outline, or story beats (콘셉트, 시놉시스, 줄거리, 비트) before production.
---

# Developing Video Synopses

This skill turns a premise or brief into narrative planning artifacts — concept, logline, synopsis, beat map. Show the artifact itself in Korean by default; a report that one was written is not the deliverable.

Narrative planning is where this skill ends. Character sheets, panels, images, and model-specific prompts belong to `designing-video-character-sheets` and `storyboarding-video` and are produced only when asked for.

## Inputs

Read the request as a brief and extract what is already known — never ask the user to repeat supplied information:

- the purpose, intended audience, and any single takeaway, question, or intended change;
- the video's mode — narrative/fiction, data/educational, personal/documentary, brand/business, abstract/mood, explanatory metaphor;
- genre and production method when supplied or selected, tracked separately from tone, narrative mode, and model/input type;
- format, platform, runtime, tone, constraints, and the exact deliverable requested;
- for factual briefs, the supplied claims, their sources, and explicit unknowns.

Invocation context matters. Under a multi-stage coordinator or `orchestrating-video-preproduction`, inherit its direction, interaction mode, and choice statuses and honor its active checkpoint — a synopsis request is not authorization to complete later stages, and delegated work never calls back to `creative-production` or opens another interview. Standalone calls consult `creative-production` once to confirm scope and route, then produce only the requested artifact.

Ask one concise question only when a missing answer would change the mode or central premise; otherwise proceed, label material assumptions, and leave optional details open. When coordinated, return candidate concepts for the coordinator's concept checkpoint instead of expanding an unselected option. An unspecified runtime stays unspecified — "short" is not a duration — and no deadline, platform, demographic, or evidence source is manufactured.

## Mode-matched shaping

Choose the structure that fits; no formula is universal, and familiar arcs are diagnostic aids, not checklists.

- **Narrative/fiction:** establish who wants what, why now, what resists, the stakes, the attempts, and the choice or consequence that changes things. Beats connect through cause, opposition, or deliberate reveal — not "and then." Flat or non-linear shapes are valid when the brief wants them.
- **Data/educational:** open on the audience's question and keep supplied facts, derived arithmetic, interpretation, proposed action, and unknowns apart. A workable arc is question → verified insight → context → reveal or reflection → next step; include a CTA only when requested or warranted, and never infer cause, trend, persistence, or prediction from a data change alone.
- **Personal/documentary:** select the event for its relevance, define who narrates and whose perspective holds, and connect past to present without distorting the event or inflating the narrator's role. Never diagnose a real person.
- **Brand/business:** put the audience or customer at center when the brief calls for it; the brand may guide without being the hero. One governing message, evidence behind claims, objections treated fairly, and no fabricated urgency, shame, or coercion.
- **Abstract/mood/music:** build intentional progression from visual, sonic, or movement motifs while honoring stated invariants — no protagonist, plot, moral, CTA, or happy ending the user excluded.
- **Explanatory metaphor:** name the source domain and target concept, map only their shared structure, and state where the analogy stops; a metaphor never substitutes for or distorts the factual explanation.

Running inside the shared lane, `../orchestrating-video-preproduction/references/video-direction.md` supplies the direction-axis and checkpoint conventions — following them neither widens a standalone request nor overrides explicit no-CTA, factual, or ending constraints. Routing and approvals stay with `creative-production`.

## Writing the artifact

Unless another format is requested, a concept/synopsis deliverable contains:

1. **콘셉트 브리프** — genre, purpose, production method if known, mode, audience, central promise/question, tone, format/runtime, constraints, and fact/approval status when relevant.
2. **로그라인** — subject plus goal or question plus central resistance plus stakes or change; non-narrative work gets a one-sentence concept rather than a forced protagonist.
3. **시놉시스** — a concise beginning-to-end account at the requested detail level showing how the situation changes, without becoming a storyboard or shot list.
4. **비트 맵** — ordered beats, each with its purpose, the event or visible change, why the next beat follows, and what information or emotion shifts.
5. **구조 선택과 가정** — why this structure fits and only the assumptions that materially affect the output.

A request scoped to a logline, premise, or beat outline returns exactly that — never inflate a small request into a production packet.

## Accuracy discipline

- Timestamps appear only when a runtime is supplied or requested; allocations are approximate, sum to the stated runtime, and imply no frame accuracy.
- When supplied numbers shape the story, show the arithmetic; source data, calculation, interpretation, and unknown cause stay distinct.
- A claim with no supplied source is labeled unverified or dropped. Plausible explanations, methodological claims, and a proposal's effectiveness are never written as established — avoid unsupported universal wording like "the only way." Collecting more data is not promised to explain a cause or predict an outcome unless the measurement design supports it; frame it as an optional suggestion or omit it.
- Fiction may invent connective detail serving the premise, but fixed facts, constraints, and endings never change silently.

## Self-check

- Is the central question or promise clear and right for this audience?
- Does every beat carry narrative, emotional, tonal, or informational weight?
- Are transitions motivated by action, obstacle, choice, reveal, or deliberate formal shift?
- Does the character or subject hold agency appropriate to the mode?
- Does the ending answer the central question — or leave it open in a way the brief allows?
- Do emotions surface through action, perspective, detail, or sound rather than names, and do they fit the character's concerns?
- Can each factual claim be traced, with unknowns still unknown?
- Are constraints — no dialogue, no CTA, non-narrative form, fixed ending — intact?
- Is the actual artifact present rather than a completion report?

Cut any beat that adds nothing; conflict is never added just to satisfy a formula.

## Handoff

The next stage inherits the spine unchanged: direction decisions, mode, audience, the one promise or question, tone, runtime/format if known, fixed facts with their status, constraints, world and character anchors, and inherited interaction mode and approvals. `designing-video-character-sheets` takes characters; `storyboarding-video` takes panels; anything beyond text planning returns to `creative-production` or `orchestrating-video-preproduction` — this skill never routes execution. Creative approval is not permission to generate paid assets.

Craft techniques apply only within the mode they serve: data-to-insight arcs belong to factual work, persuasion structures to briefs that warrant them, and autobiographical or clinical material is an empathy and consistency aid — never a diagnosis. No craft guidance is factual evidence.
