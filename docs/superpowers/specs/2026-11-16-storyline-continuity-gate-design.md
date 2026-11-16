# Storyline continuity gate — scoped design

Authority: user explicitly asks to update content-production skills so earlier scenes are always references for later scenes across the whole storyboard. This implements the already-discussed coordinator ownership, incoming/outgoing-state handoff and blocking checks; no media execution, spending, publishing or project-ledger edits.

Approach: strengthen the existing creative-production coordinator and canonical reference26; use the existing edit-template cells and delivery_checks, not a new skill, global state database, approval ledger or provider API. A generic reminder alone leaves the omission possible; literal last-frame chaining alone propagates failed output and fails across scene/angle/time changes.

Requirements:
- Every ordered scene/shot has a predecessor/history reference relationship. Carry accepted character/location/prop/action/audio state, including offscreen persistence and returns after cutaways. First scene uses the canonical initial state.
- This is not pixel identity or attaching every preceding image. Record permitted angle/location/time changes and resets; cross-cut/flashback follows its appropriate narrative-time ancestry.
- Planning binds planned outgoing/incoming states across the entire ordered board without requiring nonexistent generated media. Execution binds actual accepted take/source-out to the next incoming state. Reject a bad end rather than silently making it authority.
- Coordinator owns the gate even if no independent worker exists. Required unresolved/failed continuity blocks the dependent generation, take adoption and completed-film delivery. Independent reachable work may proceed, not the blocked dependency. Draft/PRELIMINARY, hurry, budget exhaustion, cropped contradictions and file/hash/decode checks do not waive the gate.
- Inspect actual selected out/in frames AND adjacent motion; inspect whole assembled sequence at normal speed with audio. Unsupported perception remains unverified, never pass. Intentional elision needs coherent before/after and approval where it changes locked direction.
- Existing domain/schema/IDs, selected provider, budgets and skill activation boundaries stay unchanged. This is an instruction/workflow gate, not an implemented automatic semantic vision detector.

Implementation choice: three instructional surfaces (coordinator, canonical reference26, existing edit template), targeted regression tests and bounded fresh-context pressure scenarios. Preserve all unrelated working-tree files; no commit/push/package release requested.
