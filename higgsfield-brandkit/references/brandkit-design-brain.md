# Brandkit Design Brain

Internal art-direction layer between user input and Brandkit production. Never
show this analysis as a separate concept or ask the user to approve it.

The Design Brain does not render assets, write Recraft prompts, call tools, or
store approvals. It turns the current brief and selected draft elements into
strong, coherent creative decisions for the next stage.

Read [design source bindings](design-sources.md) before applying the craft rules.
K-brand supports coherent, mutually reinforcing identity elements; A-logo-font
and A-pair support visual-weight pairing and hierarchy; A-logo supports the
one-distinctive-element simplification. These are bounded craft guidance, not
universal aesthetic laws or measured provider/audience guarantees. Fixed candidate
counts and the symbol-only phase are local output contracts.

## Source of truth

Use only:

- Mandatory intake answers
- Uploaded official assets
- Uploaded inspiration/reference signals
- User feedback from prior review stages
- Already selected draft palette/logo/type

Do not run external design research. Do not copy a supplied reference's logo,
layout, artwork, pattern, or distinctive device.

## Compile Creative DNA

Privately extract:

```text
PRODUCT TRUTH
What is materially, functionally, or behaviorally real?

AUDIENCE DESIRE
What does the intended audience want to feel, signal, or achieve?

POSITIONING / VALUES
What promise or value must the identity communicate?

NAME CUES
Meaning, sound, rhythm, initials, and useful letter shapes.

REFERENCE SIGNALS
General palette, form, type, composition, material, and energy preferences.

VISUAL AXES
Restrained–Expressive:
Geometric–Organic:
Familiar–Experimental:

CENTRAL MECHANISM
One specific visual idea that can generate a palette, mark, type relationship,
and applications.

FORBIDDEN CLICHÉS
Generic devices that would make this identity interchangeable.
```

Every recommendation must trace back to at least one Creative DNA field.

## Visual axes

Treat values as directional constraints, not mathematical style recipes:

- Restrained ↔ Expressive controls intensity, contrast, and density.
- Geometric ↔ Organic controls construction and shape language.
- Familiar ↔ Experimental controls category recognition and novelty risk.

Do not invent a value when the user omitted it; use 50 (balanced).

## Action modes

### `PROPOSE_PALETTES`

Input: Creative DNA.

Privately generate several raw candidates, critique them, then return 2–3
distinct palette options for rendering.

Each option defines:

- name
- rationale tied to Creative DNA
- background and text colors
- 2–4 supporting/accent colors
- optional gradient logic only when meaningful
- usage relationships
- what cliché it avoids
- 2–3 rough logo mechanism seeds appropriate to that palette

Palette options must differ in strategic emphasis, not merely hue.
Never omit logo mechanism seeds; the palette review must help the user
understand what kind of identity each palette could support.

### `PROPOSE_LOGO_MECHANISMS`

Input: Creative DNA + selected draft palette.

Return exactly three distinct symbol-only mechanisms. Each defines:

- mark_type
- central_idea
- visual_mechanism
- distinctive_element: one concrete silhouette, negative-space device, motif
  treatment, or unexpected locked color-role pairing
- shape_logic
- treatment
- style_register
- user_style_directive: preserve the user's explicit style wording when supplied
- composition
- palette roles used by the mark (choose one, two, or three as the concept
  requires; three is a maximum, not a target, unless the user explicitly
  requested more)
- forbidden elements

No wordmarks, taglines, descriptors, or Recraft prose. Prompt writing happens
afterwards under the `logo-prompt-enhancer.md` contract.

Each mechanism contains one concept only. State its single visual idea in one
clause. Never fuse two symbolic subjects unless the user explicitly requested
that exact fusion. “Simple” mechanisms still need the `distinctive_element`;
generic geometry or adjectives do not qualify.

### Logo type routing

Compare the following routes against the brief and intended applications
(K-brand / A-logo / A-logo-font in `design-sources.md`). These are optional
starting hypotheses, not exclusive categories or mandatory success tests:

- **lettermark_monogram** — test whether initials/name letterforms can carry a
  brief-specific construction and remain identifiable at the intended size.
- **pictorial** — compare a literal product/process/object cue with less literal
  routes; check category cliché and recognition risks.
- **abstract** — compare a process, benefit, emotion, or relationship expressed
  nonliterally; disclose that its meaning may need explanation.
- **mascot** — compare a character-led route where play, community, or a
  family audience is relevant; check whether the character obscures brand identity.
- **emblem** — compare a badge/seal route where heritage, membership, ritual,
  or label applications matter; check detail loss at small sizes.

Normally return three different mark types (local workflow contract; A-logo/K-brand provide category vocabulary and brief/context guidance, not this fixed count):

1. one name/letter-derived route when viable
2. one product/meaning-derived route
3. one concept/benefit-derived abstract route

If one route is not viable, replace it with the strongest evidence-based type.
Never produce three variations of the same mechanism merely with different
shapes.

### `PROPOSE_TYPOGRAPHY`

Input: Creative DNA + selected draft palette + selected draft SVG mark.

Return 2–3 font-pair proposals. Each defines:

- display family/source/weight/style
- body family/source/weight/style
- why their anatomy complements the selected mark
- why the pair fits the audience and positioning
- official font links when applicable
- risks/avoid rules

Do not create type scales, line-height systems, or letter-spacing systems.

Choose pairs by:

- comparing display-font anatomy with the selected mark's geometry and stroke
  character: explain similar or complementary weight, width, curvature, and
  proportions in the rendered specimen, rather than demanding literal matching
- keeping body text readable and quieter than the display face
- supporting the audience, positioning, and selected visual axes
- ensuring required language/glyph coverage
- using fonts that are actually available through supplied files or Google
  Fonts

Every option must use a unique display/body combination. Do not repeat the same
pair under different names, swap the same two families, or use identical
display/body families unless the input explicitly requests a one-family system.

### `CRITIQUE_ESSENTIAL_KIT`

Input: Creative DNA + selected palette + selected logo + selected typography.

Check:

- Is every element traceable to the brief?
- Do logo, palette, and typography express one central mechanism?
- Could the identity be renamed for another brand without meaningful changes?
- Is the intended expressive hierarchy clear (see “One expressive move” below)?
- Is the mark scalable and producible?
- Does typography complete rather than fight the mark?
- Does the palette support contrast and real applications?
- Does anything copy a supplied reference?
- Does anything rely on generic AI-branding clichés?

Return specific revision instructions for failing elements. Return `PASS` only
when the combined Essential Kit is coherent enough to show for final approval.

### `REVISE_FROM_FEEDBACK`

Input: Creative DNA + current selected drafts + latest user comment.

Change only the element the feedback targets, then re-run downstream coherence:

- Palette change → recheck mark and typography.
- Logo change → recheck typography.
- Typography change → rebuild wordmark/lockup.

Never restart unrelated stages without a concrete dependency reason.

## Anti-slop rules

Reject:

- leaves used as an automatic synonym for organic
- sparkles used as an automatic synonym for premium
- shields used as an automatic synonym for trust
- random gradients used as an automatic synonym for modern
- generic globe/orbit/network marks without product-specific meaning
- arbitrary initials with no construction idea
- gold + serif as an automatic luxury solution
- excessive decorative devices
- several unrelated metaphors combined in one mark
- two metaphors physically fused without an explicit user request
- concepts described only with adjectives
- generic minimal symbols with no described silhouette, negative-space device,
  motif treatment, or unexpected color-role relationship

## One expressive move

For the default direction format, name one dominant expressive mechanism and
make supporting elements quieter. This constrained adaptation of A-logo's
“Own one thing” and A-pair's headline/body hierarchy is not evidence of universal
superiority. Preserve an explicit user multi-device direction; name its reading
order and inspect competing visual weights rather than rejecting the device count.

Default comparisons:

- Expressive mark → compare restrained palette/type.
- Expressive palette → compare simpler mark/layout.
- Expressive typography → compare minimal supporting graphics.

Judge the rendered relationship and the brief, not the presence of these pairings
alone. Record a specific visible conflict before rejecting a direction.

## Internal selection rubric

Score raw candidates privately:

- relevance to brief
- distinctiveness
- ownability
- coherence
- category suitability
- scalability
- production feasibility
- application potential
- cliché risk
- reference-copy risk

Discard weak candidates before producing user-facing options. Never expose
scores, rejected drafts, or internal reasoning.
