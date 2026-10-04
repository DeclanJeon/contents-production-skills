---
name: storyboarding-video
version: 2.3
description: Use to turn a synopsis, scene, visual sequence, or story beat into ordered storyboard panels, a storyboard sheet, or per-panel image prompts.
---

# Storyboarding Video

Convert a supplied or clearly stated story into ordered, readable panels — the storyboard itself in Korean by default, plus reusable generic image prompts. Prompts are text; no image is ever claimed to exist.

The core panel unit is a narrative/information beat, not a timed model clip. For **production-ready/detailed storyboards, complete storyboard sheets, or supplied production-board QA**, REQUIRED: read [the complete storyboard contract](../video-production-assets/references/storyboard-contract.md). Integrate shot/camera/spatial/VFX/speech/audio plans through its specialist owners **before the final board**; preserve one readable beat per image. A narrow narrative-panel request retains the text-only format below. Model-specific serialization and clip execution remain downstream.
Default **storyboard/콘티** work uses that complete production contract. Use the narrow narrative-panel format only when the user explicitly asks for a panel exercise, rough narrative beats/thumbnails or image prompts alone. A supplied panel count remains exact; if that count cannot cover the approved story visibly, report the conflict and ask to revise count or story rather than silently omitting events.

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
- Attention is guided through framing, point of view, and composition. In a narrow narrative-panel request, leave timings/movement to the requested next owner; a production board includes their linked technical specifications under the complete contract, without pretending a still image performs movement.

## Output format

Use the requested format; otherwise:

1. **연속성 앵커** — the story/visual facts these panels need, plus unresolved items affecting depiction.
2. **패널 표** — one ordered row per panel:
   - **패널 번호 / 기능** — the beat's purpose in the sequence;
   - **한 프레임의 행동** — the single readable action or information change;
   - **보이는 대상·시점·구도** — the visible framing at this instant; production boards additionally link the shot's camera-movement specification rather than describing motion as visible inside one still;
   - **보여줄 것 / 감출 것** — what is revealed now versus withheld;
   - **감정·주의 초점** — observable through pose, expression, detail, or graphic hierarchy;
   - **대사·자막·소리** — supplied or needed cue, or "없음"; no invented factual captions;
   - **전환·연속성** — why the next panel follows; which anchors persist or change;
   - **이미지 프롬프트** — one reusable prompt per panel.
3. **시트 레이아웃 프롬프트** — one optional unified storyboard-sheet prompt matching the exact requested count and layout; a fixed-count template is a layout option, never a default.
4. **핸드오프** — production boards include the contract's full beat/scene/shot/panel/character/audio mapping, image-count plan and image-only review status. Link generation-planning §4 for downstream timed model-clip decomposition and §3 for requested model-specific prompts.

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
- For a production board, all applicable camera/spatial/VFX/speech/audio slots, stable indices and start/peak/end image accounting present; actual clean-image sequence reviewed without explanatory labels/audio, or explicitly unverified? For narrow panels, technical planning stays with the requested downstream owner.

## Handoff

Production boards follow [the complete contract](../video-production-assets/references/storyboard-contract.md) through indexed correction, clean-cut extraction and visual story review. Timing, camera and spatial specifications are inherited from their specialist owners; model-specific clip decomposition uses `creative-production`'s generation-planning §4 preserving panel IDs, beat order, reveal timing and continuity. Actual image-only review and user acceptance are separate from structure checks and execution approval. Storyboard craft is not factual evidence for the depicted subject.
