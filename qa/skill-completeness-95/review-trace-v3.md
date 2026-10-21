# Independent structured-evidence review — v3

Reviewer session: `bg_41`, brief `brief-trace-review-v3.md`; explicit `openai-codex/gpt-6.1-sol`, read/grep/glob only. Returned after 91.51 seconds. No edits, builds, tests, model/provider calls or independent hashing were performed by this reviewer.

## Verdict

No Critical or Important correctness issue established in the reviewed runner/parser path or supplied S1a smoke. This is not acceptance of the 61-case corpus or a skill-score claim.

## Actual read evidence independently inspected

`runs/omp-final-2.10-04/S1a/attempt-0001.stdout`:

- Lines 36–37: correlated first read request/end, Boolean `isError:false`, host `result.details.meta.source.type:path`, absolute checkout path for `16-concept-emotion-retention.md`; display line metadata covers 1–158.
- Lines 67–68: independent equivalent evidence for `12-qa.md`; display line metadata covers 1–68.
- Line 783: completed assistant `message_end`, `stopReason:stop`, table retained separately in attempt JSON.
- Line 785: actual `agent_end`.
- Stderr empty; recorded exit0; equal before/after tree hashes; no missing required reads, external reads, tool errors or protocol errors. Status `completed`, verdict `UNREVIEWED`.
- Command includes `--no-skills`, not `--no-rules`. Owner directive supplies no source content. This is explicit owner-assisted package application, not a skill-discovery benchmark.

Substantive S1a smoke: answer quotes both actual provenance-separation sentences, separates narrowly attributed source claims from package operating/design proposals, preserves individual `[BASIS-UNSTATED]` limitations, and explicitly says original book excerpts were not read in that run. This is a scoped smoke observation, not all-corpus adjudication or source validity proof.

## Boundaries reviewed

- `event_trace.py:83–103`: requested paths from correlated starts; resolved paths from host result metadata; args-only paths cannot certify local reads.
- `event_trace.py:105–124`: completed assistant final only, excluding tool-call messages/deltas/duplicated agent-end messages.
- Malformed JSON, relevant invalid shapes, duplicate/orphan/mismatched/unfinished calls and missing final/end produce protocol errors; runner rejects them.
- `run_cases.py:142–160`: final prose is not searched for failure phrases; process/stderr/deadline evidence controls infrastructure classification.
- `run_cases.py:163–176`: failures/timeouts cannot satisfy successful cache gate; completed protocol plus confirmed required reads required.
- `run_cases.py:263–268`: original stdout/stderr bytes retained separately from extracted final text.
- Prompt/tree/owner-context/required-read/parser/output/profile identity inspected; manifest freshly extracted from four frozen sources with exactly 61 IDs and original prompt line endings.

## Explicit limitations

1. Read occurrence does not prove sufficient read scope. Every case still needs independent scope/answer adjudication using raw display metadata.
2. Host metadata is trusted; source type validation is permissive. Actual smoke used expected absolute `path` metadata.
3. Result SHA256 is canonical result JSON, not original source-file bytes or comprehension/book entailment.
4. Cache trusts saved attempt evidence, without reopening/authenticating raw sidecars against deliberate manual falsification. Reviewer found no ordinary execution path falsely constructing a completed record.
5. Identity is not hermetic: executable/version and selected environment recorded, not every config or executable byte. Rules intentionally remain enabled.
6. Hashes were inspected, not recomputed by this reviewer.

## Parent verification after shared implementation wave

- Targeted parser/runner/delivery regressions: **31 passed, 21 subtests passed**.
- Full suite: **286 passed, 7 skipped, 235 subtests passed**, exit0; `tests-v3.json` retains actual command/environment/output.
- These tests are parent observations, not reviewer-run evidence. No formal case or skill score is inferred from test counts.
