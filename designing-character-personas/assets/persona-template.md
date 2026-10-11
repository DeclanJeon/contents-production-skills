# Persona packet template — `designing-character-personas`

Fill every slot the request scope covers; mark unused slots `N/A` with a reason. Every value carries `supplied | observed | proposal | undecided`. Text packet only — no image/audio and no new project/artifact IDs allocated. Supplied IDs/version references are retained.

## provenance
- request_scope: standalone | delegated-input-to character_sheet SSOT
- input_artifacts: [ {id, version, inspected_scope} ] — retain supplied existing references even on standalone calls; omit empty/unallocated ID placeholders
- delegation: fictional-design scope granted | none
- subject: fictional | real person | existing approved character
- typology_mode: none | mbti | enneagram | both (with precedence reason)

## persona_core
- story_role / outer_goal / protected_value
- core_desire / avoided_state / interpretive_belief (how they read situations)
- conflict_priorities / hard_limit
- surface_attitude vs actual_intent gap
- strength_cost: when the strength becomes the problem, and what it costs
- relation_variants: how openness/trust tactics shift per relationship
- contradictions: each with its trigger condition — condition differences, not random inconsistency

## typology_lens  (N/A with reason when mode=none)
- mbti: {type, design_rationale, limits, per_axis: {position, grounds, character_interpretation, connecting_behavior, exception_condition}} — rationale connects this character's brief/core to the lens; limits state what is undecided or not supported, even in MBTI-only mode
- enneagram: {core_type, desire/avoidance (this character's version), securing_strategy, pressure_vs_settled, optional_wing, design_rationale, limits}
- strength markers (if used): low|mid|high — relative creative marks, never scores
- gaps: where supplied type and approved behavior disagree — behavior wins, gap named

## behavior_rules
Per core trait, the observable chain (needed states only: normal / pressure / trust):
`ground → trigger/stakes → interpretation → intent → observable action/dialogue → choice/cost → exception condition`
Compact standalone requests: traits as needed. Feeding a canonical SSOT: honor its counts (§13 traits 5–7, §20 contradictions ≥3).

## expression_bridge
| rule | behavior | expression/posture/gesture | speech style | per-scene vocal direction | keep/exclude |
|---|---|---|---|---|---|
Rules: observable+audible only; no type→face/build/timbre; locked appearance preserved.

## voice_identity  (N/A + reason for silent roles — never an invented narrator)
- register, timbre/roughness/breathiness, resonance impression, articulation, sentence-end habit, baseline rhythm
- auditory_anchors: [the 2–3 cues that identify this voice]
- allowed_variation: what bends under pressure vs. what must not
- grounds: brief | supplied audio | cast contrast | labeled proposal (never type-derived)
- voice_identity_direction: reusable identity-only instruction preserving auditory anchors; no type label, biography dump or per-scene emotion
- realization: proposed | unresolved | supplied approved selection; actual selection record/reference only if supplied, never a fabricated voice ID/sample

## speech_style  (N/A + non-speaking reason for silent roles)
- sentence length, lexicon, question/command/indirection, honorifics, humor, silence use, per-relationship register
- language/dialect: supplied-only

## performance_cues  (vocal only — silent roles N/A; visual acting goes in expression_bridge)
For every delivered line, a compact record: {exact text, intent, subtext, emotional_pressure, stressed_words, pause, breath, pace, performance_cue}. Do not omit fields to meet a concise format: natural/default/none is explicit when appropriate, unknown scene facts stay undecided.
`performance_cue` is the short executor instruction for that exact line, separate from `voice_identity_direction`; identify fixed anchors vs. variables. A shared default is valid only when the line explicitly references it.

## validation
- which behavior_rules were checked against which states; contradictions verified as conditioned
- cast-overlap check: which characters share goals/judgments/speech and where they actually differ

## unresolved_requirements
- open choices needing delegation or user decision; unsupported controls; stale pins; what the next executor still needs

---

# Worked example (fictional standalone packet — no IDs allocated)

Brief (supplied for this fictional example): equipment handler protecting teammates in a disaster setting; new character design explicitly delegated; speaking role with Korean dialogue; no supplied types. Compact standalone packet, not a full canonical 0–33 SSOT.

- **provenance:** role/goal/Korean dialogue = supplied; motives, lens interpretation, acting and voice below = proposal; subject = fictional; delegation = new character design; mode = both (proposal); no project/artifact IDs allocated or audio inspected.
- **persona_core:** protects teammates; avoids teammates endangered by her; reads situations as "what fails first?"; priority — procedure yields to people when time runs out; surface = brisk checker, intent = keep everyone safe; cost — her checking reads as distrust and slows the team; contradiction — demands confirmation yet moves first unapproved *when danger is immediate and time is short*.
- **typology_lens (proposal):** ISTJ — I checks her own interpretation before asking the team, except immediate danger triggers shared questions first; S starts with observed check results, except incomplete evidence permits an explicitly tentative pattern hypothesis; T uses consistent criteria, except a live threat prioritizes the person over the checklist; J aims to close a check, except new risk reopens it. These are character-specific choices, not type laws. Enneagram 6 — avoids leaving teammates without a dependable safety plan; secures trust by sharing verified risks; pressure raises rechecking, immediate danger overrides it. Wing/directional theory unused.
- **voice_identity (proposal):** clear mid register, crisp consonants, sentences end short; anchors = consonant clarity + clipped endings; allowed variation = pace/attack under pressure, never a different voice. (A lower rougher voice is an equally valid casting proposal — not a type answer.)
- **speech_style (proposal):** one confirmed fact then one request; direct questions rather than blame; trust permits “같이”; supplied Korean, dialect undecided.
- **voice_identity_direction (proposal):** “맑은 중음역과 선명한 자음, 짧게 닫는 말끝을 유지한다. 속도·강세·호흡은 장면 지시에 따라 바꾸되 기본 음색과 조음은 같은 화자로 유지한다.” Voice realization = unresolved; no voice selection, measurement or audition.
- **behavior_rules (proposal):** uncertainty → reads the gap as a shared risk → verifies before handing over → delay costs trust; exception: immediate danger means clearing the exit first. Trusted teammate self-blame → reads isolation as a coordination risk → invites joint checking → accepts shared responsibility; exception: immediate evacuation still comes first.
- **expression_bridge (proposal):** verification rule → checklist/gear eye-line → concise confirmation question → noun emphasis; danger exception → open exit posture → one short instruction → firmer attack; trust → sit beside without forced eye contact → inclusive request → slower delivery. Face/body and auditory identity remain unchanged.
- **performance_cues (proposal):** exact “잠금은 확인했어?” — intent verify, subtext “추정을 확인으로 쓰지 않겠다”, low pressure; cue “발화 전 자연 숨, 잠금 강조, 질문 뒤 짧은 쉼, 일정한 속도”; exact “확인은 나중에. 먼저 나가.” — intent evacuate, subtext “절차보다 너를 먼저”, high pressure; cue “짧은 들숨, 마침표에서 쉼과 숨, 먼저 강조, 짧고 빠른 단호한 발화”; exact “다음엔 같이 확인하자.” — intent share responsibility, subtext “혼자 떠안지 마”, low pressure; cue “한 호흡, 같이 부드럽게 강조, 늦춘 속도, 말이 끝난 뒤 기다림”. All preserve the voice identity direction.
- **validation sketch:** three states differ in behavior but preserve the protected value; no silent substitution anywhere.
- **unresolved_requirements:** actual voice candidate/tool controls/rights and listening approval; no current project/SSOT version was supplied and none is invented.

