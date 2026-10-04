---
name: storyboarding-video
version: 2.2
description: Use to turn a synopsis, scene, visual sequence, or story beat into ordered storyboard panels, a storyboard sheet, or per-panel image prompts.
---

# Storyboarding Video

Convert a supplied or clearly stated story into ordered, readable panels — the storyboard itself in Korean by default, plus reusable generic image prompts. Prompts are text; no image is ever claimed to exist.

The unit of work is the narrative beat, not the shot. Timed shotlists, camera-move plans, clip breakdowns, and model-specific prompts belong to [generation planning](../creative-production/references/video-generation-planning.md) under `creative-production`; complete text packages route through `creative-production` → `orchestrating-video-preproduction`.

`creative-production` alone coordinates projects. Standalone calls consult it once to confirm scope and route, then deliver only the requested storyboard. Work delegated by `creative-production` or `orchestrating-video-preproduction` continues on the inherited spine and approvals — no call-backs, re-routing, second interview, or second approval ledger.

## Anchoring the brief

Extract the synopsis or brief, requested panel count, mode, characters and objects, fixed facts, constraints, unresolved causes, and existing visual anchors. Supplied information is never re-asked.

- A confirmed synopsis and its ending are locked: no added or removed events, dialogue, characters, resolution, weather, or emotional outcomes. Add only the minimal visible connective action needed to stage what was supplied, and label material staging choices as proposals — a staging choice never becomes a new obstacle, stake, or reaction that alters the stated sequence.
- The requested panel count is exact. With none given, pick a concise count covering the supplied beats without padding.
- Fact and interpretation stay separate. Factual or documentary panels never depict unsupplied people, equipment, places, or records as evidence; counts-and-claims input gets neutral text/number graphics and generic non-evidentiary icons rather than invented archives, staff, scanners, photo stacks, or aged records — unless supplied or explicitly requested as fiction. Unknown causes remain unknown.
- Keep a continuity ledger: character identity, screen position, object location and ownership, color, condition, hand, direction, and other supplied invariants.

## Composing each panel

Every panel carries one dominant action or one informational change readable in a single still; compound actions like "approaches, picks up, hands over" split into their distinct beats. Every ambiguity resolves to one specific staging choice — labeled a design proposal when the brief leaves it open — used identically in the panel row, its prompt, and the sheet prompt. A storyboard never contains "A or B."

Each panel answers what the viewer learns or feels and why it follows the previous one. Cause, choice, pursuit, comparison, or deliberate reveal motivate transitions; a held reaction, visual pause, or data graphic is legitimate when it serves the story.

- A supplied reveal is foreshadowed through a visible cue but never shown early.
- Every panel earns its place — narrative, emotional, tonal, or informational function; none exist to fill a count.
- Dialogue, captions, and sound appear only when supplied or needed to read the beat — default to none rather than inventing lines, reactions, or factual captions; mark genuinely optional creative text separately.
- Attention is guided through framing, point of view, and composition — not shot duration, lens specs, camera-move verbs, or clip segmentation.

## Output format

Use the requested format; otherwise:

1. **연속성 앵커** — the story/visual facts these panels need, plus unresolved items affecting depiction.
2. **패널 표** — one ordered row per panel:
   - **패널 번호 / 기능** — the beat's purpose in the sequence;
   - **한 프레임의 행동** — the single readable action or information change;
   - **보이는 대상·시점·구도** — subjects, viewpoint, framing, composition (never moving-camera instruction);
   - **보여줄 것 / 감출 것** — what is revealed now versus withheld;
   - **감정·주의 초점** — observable through pose, expression, detail, or graphic hierarchy;
   - **대사·자막·소리** — supplied or needed cue, or "없음"; no invented factual captions;
   - **전환·연속성** — why the next panel follows; which anchors persist or change;
   - **이미지 프롬프트** — one reusable prompt per panel.
3. **시트 레이아웃 프롬프트** — one optional unified storyboard-sheet prompt matching the exact requested count and layout; a fixed-count template is a layout option, never a default.
4. **핸드오프** — link the coordinator's generation-planning reference §4 only when timing, camera moves or clip decomposition come next, and §3 only when a model-specific prompt is requested.

Prompts use the user's requested language — Korean by default, even when a downstream model accepts English. Repeat continuity-critical details in each prompt because panels may be generated separately; prompt only visible content and stable style with no unsupported scenery, text, or objects. The unified sheet prompt preserves identical character and object identities, colors, damage, ownership, and reveal order across all cells.

## Continuity and reveals

- Supplied object color, material, wear, scale, owner/hand, and presence hold constant until an explicit panel action changes them.
- Ownership or condition changes appear as the panel event where they happen — never switched silently between prompts.
- Established screen direction and spatial relationships persist unless a visible transition explains the change.
- In a mystery or search, plant the clue before the discovery panel without displaying the answer early.
- Factual graphics label supplied numbers and derived arithmetic separately; a visual metaphor may clarify but never implies an unsupported cause, quantity, person, or event.

## Self-check

- Exact panel count, one dominant beat per panel?
- Each panel follows from the prior beat with a clear function?
- Fixed synopsis, ending, facts, and constraints preserved?
- Props, colors, owners, condition, and direction continuous across descriptions and prompts?
- Reveals foreshadowed without spoiling; designated panel resolves the question?
- Factual panels free of invented documentary-looking evidence — including anything labeled "proposal" — with unknowns still unknown?
- Prompts in the requested language, specific enough to hold continuity, with no generation claim?
- Timings, camera moves, and model dialects left to the downstream generation-planning owner?

## Handoff

Timing, camera-move and clip-decomposition requests inherit ordered panels, stable anchors, reveal order and unresolved continuity choices through `creative-production`'s [generation-planning reference](../creative-production/references/video-generation-planning.md) §4, preserving the beat sequence. Model-specific prompts use §3 with approved story facts and visual anchors. Execution and provider selection stay with the coordinator, never this skill. Storyboard craft is not factual evidence for the depicted subject.
