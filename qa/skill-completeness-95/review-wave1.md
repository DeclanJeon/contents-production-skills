# Independent review wave 1 — integration record

Reviewer: explicit-model read-only OMP employee `bg_11`; complete original review is in the leader session's delivered process result. Reviewer used read/grep only and did not execute tests. Scope: W0 runner, W1 strategy, W6 provider video. Spec and quality verdicts: REQUEST CHANGES; no Critical finding. W0 acceptable only as unverified implementation, not a completed arm.

| ID | Finding | Evidence | Required correction / state |
|---|---|---|---|
| R1-01 | Missing/empty/null artifact SHA bypasses binding | verify_delivery.py hash check; leader's delivery-smoke-before.json independently reproduces missing hash passing actual MP4 | Require digest and exact match; regression test added, code correction pending |
| R1-02 | Contradictory publication fields accepted | verify_delivery.py AND condition; leader reproduces publishable=true passing actual MP4 | Require both false publishable and exact unapproved state; regression test added, code correction pending |
| R1-03 | Invalid speed still used in arithmetic | verify_delivery.py speed/division; leader reproduces zero-speed exception | Structured failure before dependent calculations; regression test added, code correction pending |
| R1-04 | Decision objective absent from required intake/selection | topic-demand-selection intake/Acceptance | Leader added explicit objective/evidence scope and blocked final selection while allowing bounded evidence comparisons; scoped re-review pending |
| R1-05 | Rendition identity stranded in QA | marketing-source-adaptation, synopsis-craft, thumbnail-frameworks | Leader added exact byte count/SHA256 to all three installed references; canonical multi-rendition source-index integration and re-review pending |

Runner review: exact 61 case set, byte-preserving extraction, manifest rederivation, cache/profile/tree identity, failed-attempt preservation, mutation invalidation and no automatic PASS were inspected positively. Optional remaining coverage: CLI run-directory identity mismatch and corrupted frozen-source refusal.

Source review: reviewer directly confirmed narrow McKee classical-causality support, Dunford customer-relative comparison support, and Block tonal contour visibility. No support inferred for neighboring craft or performance guarantees.

Unverified at review time: all formal 61-case behavior, final narrowed read-only profile, actual media/thumbnail crop normal-path proof, live explainer assembler and website deployment. No 95% or 5-point claim justified by this review.
