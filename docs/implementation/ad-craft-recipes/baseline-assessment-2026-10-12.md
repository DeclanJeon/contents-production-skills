# Current-skill baseline application assessment

## Scope and provenance

Original, newly authored briefs are in `baseline-briefs-2026-10-12.json`. They use fictional STILLWATER fragrance, Lantern Quay hospitality space and ORBIT vehicle; no archive brands, copy or archived expected-answer exercise was used. The baseline CLI was explicitly prohibited from reading `docs/analysis`, `qa/` and expected-answer archives. The evaluator read approved DESIGN to understand acceptance requirements, but the consumer did not receive DESIGN or expected outputs.

Actual fresh-context consumer output: `baseline-consumer-output-2026-10-12.md`. Actual complete CLI stderr/tool transcript: `baseline-cli-transcript-2026-10-12.txt`. These are text-only production handoffs, not rendered media or approved production artifacts.

Runtime discovery: `where.exe codex claude opencode` found Codex and OpenCode, not Claude. `codex --version` returned 0.157.1; `codex login status` returned Logged in using ChatGPT. Initial default-model invocation exited 1: HTTP 400, model `gpt-6.1-sol` not supported using a ChatGPT account. Read the local model cache and selected its advertised `gpt-6-sol`; retry exited 0 in 197.66 seconds. Invocation used `exec --ephemeral --sandbox read-only --color never --model gpt-6-sol`, original prompt via stdin. No install, download, media generation, payment, commit or push occurred. CLI startup also reported unrelated installed-skill YAML errors and ignored legacy configuration. Initial shell reads displayed Korean mojibake; the consumer subsequently used UTF-8 Python reads. Those caveats are retained in the raw transcript, not hidden.

No root AGENTS.md or package.json was discovered by glob. Existing repository evidence conventions put real outcomes and bounded claims in `qa/` and `docs/evidence/`; this assignment explicitly requires the new distinct `docs/implementation/ad-craft-recipes/` location. No original frozen analysis/source media/books were edited.

## Actual decisions and omissions

### F1 — STILLWATER

Actual output proposes five shots: placement/settle 0–2.4s; cap lift/set-down 2.4–5.0s; one wrist spray 5.0–7.8s; green light and return 7.8–9.6s; readable bottle hold 9.6–12s. Locks verbal bottle silhouette, cap offset, color and label position; defers exact artwork and rights. Separates mood from physiological efficacy and rejects unseen second spray.

- **Copy→action: partial.** Copy appears at 7.8s, then can clear at 11s; no onset/settle/read/exit breakdown. The door/hurry premise is not visibly enacted or deliberately interpreted as a metaphor. Late text over wrist/light is a proposal, not a literal fulfillment of the line. This is a craft-shaping omission, not missing brand/concept functionality.
- **Reflection/logo: partial.** Actual response says mirror shape and label must be consistent and reflected label must not become contradictory artwork; it names a controlled package layer. It does not fill reflection-mask dependencies, foreground hand occlusion, reflected graphic orientation, or a specific highlight-versus-logo readable window. Ref19 already has glossy highlights, label fidelity and spatial composite integration; ref21 already has reflection/shadow/layer checks.
- **Contact/residue: mixed.** Actual hand ownership is specified: stabilize bottle, left hand lifts/sets cap, left wrist becomes free, index depresses once. It requires interval evidence, not endpoint-only proof. However, response says to preserve visible residue “until it is hidden or explicitly cleared.” Hiding cannot discharge persistence; ref26 explicitly preserves inherited obligations through occlusion until documented reset and requires reappearance comparison. This is an actual baseline consumer contradiction to an existing rule, not evidence the rule is missing.
- **Existing fields: partial.** Uses `product_id`, `kind`, proposed shot IDs and start/end state prose, but not a populated existing product/state/motion/edit table shape or explicit `후속 유지 범위 / 리셋 조건` row. Artifact IDs are clearly proposals, not registered facts.

### H1 — Lantern Quay

Actual output defines south entry, east lantern turn, curtain threshold, north window and reversed return. It declares the layout fictional, refuses floorplan/offer/testimonial claims and names spatial/continuity/VFX handoffs. Host goal and guest goal are playable; host reacts after arrival/guest glance. Cup ownership transfers only after the guest grip is secure.

- **Spatial disclosure/partner reaction: substantially present.** Path, landmarks, threshold, eyeline and return relationships are specified, with fallback neutral landmark/reorientation view.
- **POV and unit distinction: partial.** SH06 is described as “Host reaction ... then guest POV” in one shot. That is an unmarked point-of-view change: either separate source shots/edit boundaries or an explicitly designed continuous POV change is needed. The output does not establish that distinction. Earlier single-shot contact phases are correctly not automatically counted as cuts.
- **Fantasy condition: present.** Miniature garden is declared impossible, window frame is anchor, ordinary topology returns, and ordinary glimpse/reflection/curtain alternatives are offered. It does not claim an actual camera solve; no 3D geometry/Blender work is requested.
- **Timing: partial.** Shared windows are given, but stimulus→reaction and scale-change/recovery windows are not individually allocated in edit fields.

### V1 — ORBIT

Actual output gives rolling 0–4.2s, approach 4.2–6s, levitation 6–10.3s, landing/stop 10.3–12.2s and stopped reveal 12.2–14s. It separates camera motion from body motion and specifies support/contact patch/shadow/reflection changes.

- **Conditional no-slip: present in this output.** Applied to ordinary supported rolling and landing, not unsupported fantasy. Five-spoke/wheel-count/stripe/shape invariants are preserved. This was explicitly prompted in the brief, so it is not evidence of spontaneous retrieval or a statistically measured improvement.
- **Wheel aliasing: present.** Single backward-spoke still is not a failure; compare successive frames, hub translation, terrain, contact patch, camera, shadows and reflection, then record interval before severity. Existing general motion/interval QA supports this, although baseline consumer notices no dedicated wheel aliasing procedure.
- **Residue: mostly present.** Water sheen persists through flight/return until shown reset or plausible dissipation. Sand is N/A with reason. The output does not settle whether levitation disturbs water; a wake is conditional on actual disturbance, not assumed evidence.
- **Evidence/claim gates: present but not fully typed.** Uploader/model mention and untimed captions are metadata, not observed footage/heard audio or rights. No range/safety/speed claim is invented. It does not populate explicit declared-uploader/caption evidence-mode rows, requested timestamp versus actual PTS, detector-event versus verified-shot boundary handling; no actual source was supplied to exercise those rows.

## Retrieval evidence and domain coverage

The raw CLI transcript records real reads of skill/workspace/common contract, product integration (19), motion/VFX/QA (21), state continuity (26), shots (06), lighting (07), edit (09), evidence (10), performance (04), visual mode (20), execution (24), reference analysis (25), and corresponding product/state/motion/VFX/edit/shot/DNA/continuity/claim templates. Some tool outputs were long/truncated; the consumer performed later targeted UTF-8 reads. Do not represent all files as perfectly understood merely because commands opened them.

Existing refs19/21/26 already cover product invariants, reflective materials/compositing, contact phases, interval evidence, inherited residue, occlusion, coupling and state reset. Observed failures justify clearer recipes and populated handoff slots, not a new product/physics/state domain, new DB, new coordinator or claim of NOT_FOUND.

## What this baseline does not prove

One agent session with three explicitly condition-rich briefs is an application sample, not a benchmark, causal proof or five-repetition wording trial. No reference source was decoded, played or heard. No image, contact sequence, soundtrack, editable comp, rights document or final export was inspected. No media QA pass, approval, exact boundary, actual lens/rig, source PTS or generated asset is asserted. Required later verification must preserve those distinctions.
