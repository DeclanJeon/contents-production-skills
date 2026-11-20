---
name: concept-intake-design
version: 1.1
description: Use when creative-production opens a new video project whose concept, format,
  narrative structure, or direction axes are still open, to run the single upfront
  selection pass (콘셉트 선택·조합·적합성 검사·평가) before any planning. Do not use for a
  locked brief, a single requested artifact, or mid-project edits.
---

# Concept Intake Design

The one upfront intake of the package. It turns a free-form video request into a
selected, compatibility-checked, scored production concept so that every later
stage runs without another interview. It writes no plan, script, board, or
media; it returns one concept packet to `creative-production`, which stays the
sole coordinator and state writer under [policy.md](../creative-production/references/policy.md).
This skill is that policy's single intake, not a second one.

## When it runs

- Only from `creative-production` Step 0, for a new finished-video goal whose
  concept is open. A locked brief, an approved concept, a single named artifact
  (synopsis only, one character sheet, one prompt), or a resumed project skips it.
- Standalone calls consult `creative-production` once to confirm scope, then
  return only the concept packet.
- It runs once per project. A later change of concept is an impact-analysis
  re-entry decided by the coordinator, never a fresh interview.

## Procedure

1. **Read the request as a brief.** Extract every axis value already stated
   (length, format, genre, style, narrative structure, direction, language,
   exclusions). Never ask for supplied information again.
2. **Judge the nine factors** in [intake-questions.md](references/intake-questions.md):
   script, scenario, reference, plot/concept, lead character, voice, content
   concept, story development, direction. Each is `provided`, `partial`, or
   `missing`; a missing factor is filled by a recorded proposal or selection, never silently.
3. **Infer and propose; ask only what cannot be inferred.** For each open axis
   in [concept-taxonomy.yaml](references/concept-taxonomy.yaml) (in its
   `selection_order`) that the request lets you reasonably infer and that is
   reversible (platform/safe zone, tone, length, structure, style), pick the
   option, record it `inferred` with a one-line reason, and continue. Ask once,
   batched (numbered options, a default, an AI recommendation) only for two
   creative conditions: a core axis cannot be inferred at all (no subject or
   purpose given), or the user asks to choose or discuss ("골라볼래", "같이
   정하자", collaboration). Rights, execution, spend and publication approvals
   are asked at their own gates (G2, S08, S09, publication), never here and
   never inferred. Answers are user values; delegated ("나머지는 알아서") and
   proposed values, including agent-proposed presets, stay `inferred`, never
   user choices. Korean by default.
4. **Combine and check.** Apply the rules in
   [combination-rules.md](references/combination-rules.md) and
   [concept-rules.yaml](references/concept-rules.yaml): compatibility
   (`error` blocks unless the user marks an intentional mix, `warn` proceeds with
   a note), then concept-to-direction packs (for example the 1990s Korean
   melodrama pack: props, forbidden anachronisms, acting, color, music). Run
   `python scripts/concept_check.py <selection.json>` when a shell is available;
   otherwise apply the same rules by reading the YAML.
5. **Evaluate.** Score hook, feasibility, emotion, originality, coherence and
   platform fit (10–90 each; weights .25/.20/.15/.15/.15/.10). Verdict `go` at
   65+ with no blocking issue, `revise` at 50+, otherwise `rework`. Offer at most
   two alternative narrative variants with their scores.
6. **Return the concept packet** (below) to the coordinator; this skill writes
   nothing further. The packet is an input, not a stopping point: for a
   finished-video goal the coordinator continues in the same turn (R05, or R02
   for a synopsis-only goal, with [plan-template.md](references/plan-template.md)
   as the required section order) through the next eligible stages to the first
   real gate or named stop (G1 is a checkpoint, outputs stay `proposed`), and states
   exactly the facts and approval needed next. A bare packet
   with an optional "next steps" offer is not a finished turn.

## Decision provider

Typed decisions (factor presence, recommendations, scores) may come from Jev 1.14
via OpenRouter when the CineForge CLI is configured with a key; otherwise the
host agent decides. See [decision-provider.md](references/decision-provider.md).
Record which provider produced each decision. Jev is a decision model, not a
writer: prose always comes from the host agent or the planning owner.

## Concept packet

```json
{
  "selection": {"format": "short_drama", "genre": ["comedy"], "narrative": "ending_first",
                "direction": {"texture": "cinematic", "expression": "live_action"},
                "duration": "s60", "aspect": "r9_16", "constraints": [], "overrides": [],
                "sources": {"duration": "user", "emotion_arc": "inferred"}},
  "factors": {"script": "missing", "direction": "provided"},
  "concept": {"title_line": "60초 코미디 숏드라마", "chain": "코미디 × 시네마틱 × 결말 선공개형",
              "emotion_arc": "웃음 → 공감"},
  "compatibility": [{"rule": "C008", "severity": "warn", "message": "..."}],
  "direction_rules": {"applied": ["D_comedy"], "forbidden_props": []},
  "evaluation": {"scores": {"hook": 90}, "total": 76.0, "verdict": "go", "provider": "host"},
  "authority": {"accept_plan": false, "execution": false}
}
```

`authority` records only what the user actually said (policy §1). A request to
"run it non-stop" may pre-accept plan and preproduction review gates when the
user says so; it never opens paid generation, which still needs explicit
execution and spend approval.

## Boundaries

- No plan prose, scene breakdown, character sheet, prompt, or media here.
- User-supplied values are never overwritten by recommendations.
- A no-speech constraint removes dialogue/narration options and is passed on.
- Adaptations of existing works borrow structure and rhythm only: no original
  footage, music, dialogue, or characters.
- AI-made content is disclosed through platform labels at publication; no
  in-video corner label is planned.
