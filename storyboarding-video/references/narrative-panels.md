# Narrative panels: composition, format, continuity, QA

Read this guide once only when the user explicitly asked for a panel exercise, rough narrative beats/thumbnails, or image prompts alone — the narrow storyboard format. Ordinary storyboard requests use [`../../video-production-assets/references/storyboard-contract.md`](../../video-production-assets/references/storyboard-contract.md) instead, never this file. Intake, default-vs-narrow scope, dependency-gap, and return-envelope rules live in the skill's `SKILL.md`.

## Anchoring the brief

Extract the synopsis or brief, requested panel count, mode, characters and objects, fixed facts, constraints, unresolved causes, and existing visual anchors. Supplied information is never re-asked.

- A confirmed synopsis and its ending are locked: no added or removed events, dialogue, characters, resolution, weather, or emotional outcomes. Add only the minimal visible connective action needed to stage what was supplied, and label material staging choices as proposals — a staging choice never becomes a new obstacle, stake, or reaction that alters the stated sequence.
- The requested panel count is exact. With none given, pick a concise count covering the supplied beats without padding.
- Fact and interpretation stay separate. Factual or documentary panels never depict unsupplied people, equipment, places, or records as evidence; counts-and-claims input gets neutral text/number graphics and generic non-evidentiary icons rather than invented archives, staff, scanners, photo stacks, or aged records — unless supplied or explicitly requested as fiction. Unknown causes remain unknown.
- Keep a continuity ledger: character identity, screen position, object location and ownership, color, condition, hand, direction, and other supplied invariants.

## Composing each panel

Every panel carries one dominant action or one informational change readable in a single still; compound actions like "approaches, picks up, hands over" split into their distinct beats. For a state-changing action, show the observable before state, action state, and after state across distinct adjacent panels as needed; state what changed in the transition/continuity field. One still may show only its actual phase, never claim both start and completion. If a necessary state change cannot be depicted from supplied facts, mark the indexed gap instead of inventing it. Every ambiguity resolves to one specific staging choice — labeled a design proposal when the brief leaves it open — used identically in the panel row, its prompt, and the sheet prompt. A storyboard never contains "A or B."

Each panel answers what the viewer learns or feels and why it follows the previous one. Cause, choice, pursuit, comparison, or deliberate reveal motivate transitions; a held reaction, visual pause, or data graphic is legitimate when it serves the story.

- Preserve supplied reveal timing. Stage an existing setup cue without revealing the answer early; if no cue exists, name the setup gap instead of inventing a clue or changing the locked story.
- Every panel earns its place — narrative, emotional, tonal, or informational function; none exist to fill a count.
- Dialogue, captions, and sound appear only when supplied or needed to read the beat — default to none rather than inventing lines, reactions, or factual captions; mark genuinely optional creative text separately.
Choose framing, point of view, and composition to support the intended focal information, then inspect the panel; this is a qualitative, package-authored review choice, not a claim that framing reliably causes an audience effect. Hu ID 45, L235–245 and L259–264, is a partial craft basis for clarity/composition and contrast—not measured attention or comprehension.

## Output format

Use the requested format; otherwise:

1. **연속성 앵커** — the story/visual facts these panels need, plus unresolved items affecting depiction.
2. **패널 표** — one ordered row per panel:
   - **패널 번호 / 기능** — stable panel/beat/scene/shot content IDs (reuse supplied IDs; standalone exercise IDs are local, not project/artifact allocations), source sentence/beat locator, and the beat's purpose;
   - **한 프레임의 행동** — the single readable action or information change;
   - **보이는 대상·시점·구도** — the visible framing at this instant;
   - **보여줄 것 / 감출 것** — what is revealed now versus withheld;
   - **감정·주의 초점** — observable through pose, expression, detail, or graphic hierarchy;
   - **대사·자막·소리** — supplied or needed cue, or "없음"; no invented factual captions;
   - **전환·연속성** — why the next panel follows; which anchors persist or change;
   - **이미지 프롬프트** — one reusable prompt per panel.
3. **시트 레이아웃 프롬프트** — one optional unified storyboard-sheet prompt matching the exact requested count and layout; a fixed-count template is a layout option, never a default.
4. **핸드오프** — ordered panel/beat IDs, unresolved depiction items, and the panel sequence so the next requested stage inherits the board unchanged.

Prompts use the user's requested language — Korean by default, even when a downstream model accepts English. Repeat continuity-critical details in each prompt because panels may be generated separately; prompt only visible content and stable style with no unsupported scenery, text, or objects. The unified sheet prompt preserves identical character and object identities, colors, damage, ownership, and reveal order across all cells.

## Continuity and reveals

- Supplied object color, material, wear, scale, owner/hand, and presence hold constant until an explicit panel action changes them.
- Established screen direction and spatial relationships persist unless a visible transition explains the change. This continuity check is bounded to spatial staging and axis changes; see the directly read Hu passage below.
- Factual graphics label supplied numbers and derived arithmetic separately; a visual metaphor may clarify but never implies an unsupported cause, quantity, person, or event.

## Self-check

- Exact panel count, one dominant beat per panel?
- Each panel follows from the prior beat with a clear function?
- Fixed synopsis, ending, facts, and constraints preserved?
- Props, colors, owners, condition, and direction continuous across descriptions and prompts?
- Supplied setup, reveal timing, and resolution preserved without spoiling or inventing a clue or a closed ending? Missing required story inputs remain indexed gaps; deliberately unresolved endings stay unresolved.
- Factual panels free of invented documentary-looking evidence — including anything labeled "proposal" — with unknowns still unknown?
- Prompts in the requested language, specific enough to hold continuity, with no generation claim?
- Technical planning stays with the requested downstream owner — this narrow format adds no unrequested shot list or media?

Storyboard craft is not factual evidence for the depicted subject.

## Evidence scope

ID 45, Caroline Hu, *Mastering Storyboarding*, local rendition `E:/Book/06_Book/콘티_스토리보드/md/스토리보드 마스터하기 - 캐롤라인 후.md`, L235–245 (clarity/composition), L249–253 (foreground/middle/background and tonal grouping), L259–264 (balance/contrast), and L636–661 (staging/screen direction/axis), `READ-PARTIAL`. The source index records the exact file fingerprint and limits. These passages are practical guidance, not measured audience effects or universal composition rules. L650–655 has inconsistent side labels; do not use them as a fixed screen-side rule.

The rules above for brief preservation, one action/information change per panel, exact-count handling, reveal timing, transition choices, continuity-ledger fields, prompts, and output structure are package-authored safeguards and operating heuristics. They are not attributed to Hu or asserted as external standards. They do not prove audience response or factual truth.

Read-rendition identity: 47562 bytes; SHA-256 `cdd4f9b82b83c2ac6cc87c3d39251a79e4d02b7b57e337945bcb89efc58b5f21`. The partial reading and source inconsistency above refer to this exact copy.
