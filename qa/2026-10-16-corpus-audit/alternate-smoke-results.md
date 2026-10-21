# Supplementary acceptance-gate probes (non-baseline)

Date: 2026-10-16. Scope: one read-only probe per skill that received a new Acceptance section in this work session.

## Method and limit

Each probe used the exact frozen user-request text from `_blocks.json`, with the current `SKILL.md` content injected as context into a stateless `completion(model="slow")` call. This avoided the unavailable local Codex shell runner. It is **not** the frozen Codex execution arm: model, session/tool environment, and context-loading method differ. Results are supplementary spot checks only; do not compare numerically with `baseline-results.md`, count them as the 61-case post arm, or claim behavior improvement from one example.

## Observed outcomes

| ID | Target | Observation against frozen assertion |
|---|---|---|
| M-02 | `topic-demand-selection` | Ranked only the two topics with supplied monthly search figures; marked DSLR demand unknown and requested comparable measurement context. No invented metric. |
| M-04 | `camera-spatial-design` | Produced a text-only provisional kitchen plan and labeled assumed dimensions/coordinates as estimates; stated no schema validation or 3D inspection occurred and refused the requested unapproved render. |
| M-05 | `camera-motion-reference-analysis` | Blocked analysis without video; requested the reference and optional time range; did not infer movement. |
| M-06 | `ai-camera-control` | Preserved the stated push-in; labeled it soft prompt; marked lens and timing unresolved rather than inventing a value. |
| M-07 | `blender-previsualization` | Stated no Blender run/render occurred and requested a numerical scene spec and shot/frame scope. |
| M-13 | `storytelling-with-still-images` | Kept unseen images as proposed, gave a provisional 90-second cue plan, disclosed unverified assembly, and refused publication. |
| M-14 | `recording-production-history` | Returned an event chronology schema, distinguished chat-only from actual file work, and refused to log a step that never happened. |
| M-16 | `higgsfield-generate` | Routed the generic image to the authorized image executor, stated Higgsfield image ineligibility, and refused bypass/submission. |
| M-17 | `higgsfield-marketplace-cards` | Treated the request as a read-only card preview; stated missing product inputs and the package image-job blocker; no purchase/submission. |
| M-18 | `higgsfield-product-photoshoot` | Identified missing photo/style/count/use inputs and package ineligibility; no generation or spend. The assumed `product_shot` mode remains a judgment risk worth reviewing against the interview contract. |
| M-19 | `higgsfield-soul-id` | Listed missing name/photos/rights/account/cost checks and refused training under read-only scope. |
| M-20 | `higgsfield-video-explainer` | Identified four 10-second blocks, described live preset resolution, named unresolved settings and aggregate approval gate, and did not submit. |
| M-21 | `higgsfield-video-replicate` | Blocked without an accessible reference video and described shot-anchor continuity requirements; no submission. |
| M-22 | `higgsfield-websites` | Classified the bakery as a standalone website, named required choices and create/deploy separation, and refused create/deploy/publish under read-only scope. |
| M-24 | `community-shorts-stills-pipeline` | Declined to invent pixel measurements without source stills, stated the still-only/60-second contract and separate publish/delivery checks, and performed no publication. |

These 15 spot checks exercise the newly added acceptance instructions, but do not establish a score-4 rubric rating without the full matching frozen arm and a separate rescore. They do not test the 24 production modules, source provenance, links, or any provider/media execution.
