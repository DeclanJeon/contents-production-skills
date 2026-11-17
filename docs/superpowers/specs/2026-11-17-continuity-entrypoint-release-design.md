# Continuity entrypoint release design

Approved scope: user approved proceeding with the proposed continuity fixes, related commits, push and installed-agent-skill deployment.

## Intent
Dependent video work must inspect and carry accepted predecessor/history scenes, shots, video ranges, frames and relevant versioned assets into the actual generation request, not merely mention them in prose.

## Approach
Extend the existing whole-storyline gate and sequence/AV handoff implementation. Documentation-only reminders cannot check native request selection; a new global interception system is outside this package's capabilities and is not promised.

## Goals and constraints
- Make the basic continuity gate mandatory across coordinator, production-assets and standalone generation entrypoints; keep detailed state slots conditional.
- Adopt only related existing uncommitted sequence/AV implementation and its required dependencies after review and regression tests.
- Preserve unrelated routing edits, analysis material and existing files. Do not stage everything.
- Actual accepted source ranges and relevant historical state are authoritative, not failed raw tails. First shots, new voices, explicit silence and intentional time/angle changes retain documented exceptions.
- Required missing references, unsupported native inputs or unverified evidence block dependent submission; never claim model conditioning or perceptual QA from structural validation.
- No new media jobs, uploads, purchases, publications or dependency installs.

## Verification and release
Add entrypoint contract regressions before changing guidance; exercise existing sequence/AV request preparation and audit tests, including omitted/mismatched selected references. Record independent behavioral verification separately from static checks. Review staged scope, commit related units, push the explicitly requested current branch without force, and verify live remote HEAD. Run existing synchronization with explicit installed roots including Pi; check targets and hashes. Deployment means local installed skill synchronization, not an unspecified remote server deployment.

## Non-goals
Global MCP interception, guarantees about agent compliance/model output, unrelated routing improvements or analysis publication.
