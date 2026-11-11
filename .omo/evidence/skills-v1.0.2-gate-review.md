# Independent gate review: skills v1.0.2

Date: 2026-11-03
Reviewer: omo-native-gate-reviewer, task st_01a1a0be

## Decision

recommendation: REJECT

The canonical Q3 repair works, including the original B99 mutation with --sources. The broader requested re-QA found a source-reference false-pass in specialist integration outputs. The package must not be described as having completed issue-free overall QA yet.

blockers:

- id: GATE-1
  - severity: HIGH
  - violatedCriterion: Q3-source-linkage; overall-QA. These labels refer to the supplied requirements that finding source_ids be nonempty and resolve to inventory, skill and actual provenance, and that newly discovered functional false-passes inside declared contracts block overall completion.
  - observation: Integration findings are checked against step.source_provenance, not actual_output.provenance, and an empty source_ids array passes every(). Removing only B30 from T2-ux actual_output.provenance leaves its finding citing B30 and B01, yet the actual package validation entrypoint with --sources reports 5033 checks, failed=0, saved_executions=115, integration_steps=10 and succeeds. Separately, source_ids=[] is also accepted by validateIntegration.
  - evidencePointer: P/scripts/integration-validation.mjs:228-232; P/schemas/skills/ux-usability-review.output.schema.json:87-93; P/tests/integration/manual-results.json:535-610; the reproducible read-only probe and observed results below.
  - contractPointer: Supplied review brief, finding-source requirement; P/README.md:32; P/skills/design/ux-usability-review/SKILL.md:61-63.
  - action: Enforce nonempty finding sources and their presence in the actual output provenance as well as the existing verified skill/step sources. Add real integration regressions for empty finding IDs and a cited source removed only from actual_output.provenance. Preserve valid subsets and the documented no-finding stop behavior. Re-run overall QA before packaging approval.

This is newly discovered during overall QA, not a claim that the v1.0.2 delta introduced the integration bug: integration-validation.mjs is unchanged from v1.0.1. The request explicitly includes defects outside the original canonical Q3 reproduction. It is a mechanical broken-reference acceptance, not an objection about book semantics, live services, or architecture taste.

## Original intent and user outcome

originalIntent: The user requested overall QA and goal completion only if no issues remained. That QA found canonical finding B99 passing even with --sources, and the user selected "fix Q3 then re-QA".

desiredOutcome: Preserve all 23 original skill contracts and all 115 canonical cases, outputs and adjudications; repair canonical source-reference validation without regressing Q1/Q2; honestly report the overall re-QA outcome; preserve the immutable published v1.0.1 ZIP and keep source-recovery/live-execution limits explicit. A separate v1.0.2 archive is a later step, not a prerequisite for this review.

userOutcomeReview: The canonical repair is implemented at the evidence-validation boundary, not by changing the saved answers. B99 now fails and loses execution credit. Valid provenance subsets and the original legitimate design stops remain accepted. However, the CLI still certifies an integration output whose finding cites a source absent from that output's provenance. The overall outcome requested by the user is therefore not achieved, despite a green existing suite and green unmodified corpus.

## Paths and scope

P = /home/declan/Documents/Projects/Products/04_Skills/agent_skills_foundation_v1

B = /tmp/skills-v102-review-baseline-j3nq9qow/agent_skills_foundation_v1

Published baseline archive = /home/declan/Documents/Projects/Products/04_Skills/agent_skills_foundation_v1.0.1.zip

Reviewer report = /home/declan/Documents/Projects/Skills-and-Automation/contents-production-skills/.omo/evidence/skills-v1.0.2-gate-review.md

The actual B/P recursive comparison found only the declared changes: evidence validator, two test files, release target, README/CHANGELOG/current reports, validation.json, the new Q3 report and historical gate rename. It found no differences in original SKILL.md files, canonical cases/outputs/adjudications, schemas, specialist integration logic or integration fixtures. No Git checkout or implementation edit was performed.

The published archive independently hashes to:

```text
8bb521b7ff12bae7a43a9caf60a977bcd7f5cac6c70d253c2c7a922c53746f1c
```

## Direct evidence for GATE-1

### Why the implementation admits the invalid output

At P/scripts/integration-validation.mjs:229, every actual provenance entry must match a verified registry entry and a step provenance entry. That correctly validates entries which are present, but cannot detect a cited entry that is missing.

At :232, finding IDs need only occur in step.source_provenance. They are not joined to actual_output.provenance, and there is no positive length check. The output schema at P/schemas/skills/ux-usability-review.output.schema.json:87-93 supplies only the array/string shape, so it does not close either gap.

The inspected T2-ux record starts at P/tests/integration/manual-results.json:535. Its LINK-F1 finding cites B30 and B01 at :578; its actual provenance starts at :610; its separate step provenance starts at :697. The reproduction removes B30 only from the actual output array, leaving the registry, step provenance, finding, status, input, handoff and manual verdict untouched.

The original on-disk integration record is valid. The finding is about the validator's acceptance of a corrupted result, not a claim that the shipped record already contains that corruption.

### Read-only reproduction method

To honor read-only product/source access, the reviewer used a process-local readFile overlay for exactly tests/integration/manual-results.json. All other reads used the real filesystem. The production validation entrypoint, evidence validator, integration validator, schemas, registry, inventory and source Markdown were real. No validator return value or schema result was mocked, and no fixture or implementation file was written.

The same harness passed the unchanged baseline and a valid subset, and rejected B99 with the production error "T2/T2-ux: finding source IDs not in step provenance". These controls establish that the mutation reaches the real validation path and that the harness does not simply force success.

Runnable reproduction from P:

```sh
MODE=missing-actual-source bun --eval '
import { mock } from "bun:test";
import * as fs from "node:fs/promises";
import { resolve } from "node:path";
const read = fs.readFile;
const path = resolve("tests/integration/manual-results.json");
const rows = JSON.parse(await read(path, "utf8"));
const output = rows.find(r => r.scenario_id === "T2")
  .steps.find(s => s.id === "T2-ux").actual_output;
if (process.env.MODE === "missing-actual-source") {
  output.provenance = output.provenance.filter(p => p.source_id !== "B30");
} else if (process.env.MODE === "empty-finding-sources") {
  output.findings[0].source_ids = [];
} else if (process.env.MODE === "B99-control") {
  output.findings[0].source_ids = ["B99"];
}
mock.module("node:fs/promises", () => ({
  ...fs,
  readFile: async (file, ...args) => resolve(String(file)) === path
    ? JSON.stringify(rows)
    : read(file, ...args)
}));
process.argv.push("--sources");
await import("./scripts/validate_package.mjs");
'
```

The full CLI-entrypoint run was executed for missing-actual-source. Its observation was:

```json
{
  "mutation": "Remove only B30 from T2-ux actual_output.provenance",
  "findingSourceIds": ["B30", "B01"],
  "actualSourceIds": ["B01", "B01", "B01", "B09"],
  "filesystemWrites": 0
}
```

```json
{
  "checks": 5033,
  "passed": 5033,
  "failed": 0,
  "failures": [],
  "source_files_checked": 38,
  "scenario_cases": 115,
  "saved_executions": 115,
  "integration_scenarios": 5,
  "integration_steps": 10,
  "integration_handoffs": 5
}
```

The command succeeded. The counts for canonical executions remaining at 115 are not themselves the bug: canonical files were unchanged. The decisive failure is failed=0 and successful package validation despite the invalid integration source reference.

Additional direct validateIntegration observations, each starting with an independently cloned original record:

| Mutation/control | Checks | Failures | Result |
| --- | ---: | --- | --- |
| Unchanged baseline | 260 | [] | Expected acceptance |
| Finding source_ids=[B99] | 260 | T2/T2-ux: finding source IDs not in step provenance | Expected rejection; harness negative control |
| Valid actual subset containing B01 and B30 | 260 | [] | Expected acceptance |
| Remove B30 only from actual_output.provenance | 260 | [] | False-pass, GATE-1 |
| Finding source_ids=[] | 260 | [] | False-pass, GATE-1 |

All rows retained five scenarios, ten records and five handoffs. The control/probe process explicitly printed PROBE_EXIT=0; that is the probe's completion, not approval of the mutated records.

## Canonical Q3 and regression verification

| Criterion | Observation | Disposition |
| --- | --- | --- |
| Preserve original contracts and evidence | Actual tree diff shows no original SKILL.md/case/output/adjudication changes | PASS |
| Registry provenance resolves to inventory | Implemented at evidence-validation.mjs:52-63 | PASS by inspection and corpus execution |
| Actual canonical provenance copies verified entries exactly | Deep comparison includes locator and metadata at :157-163; negative tests exercise three departments | PASS |
| Canonical findings have nonempty, resolved sources | Inventory/skill/actual-output join at :165-173 | PASS |
| Valid subsets remain accepted | Existing new subset regression passes | PASS |
| Legitimate design stops remain accepted | All original 115 cases pass, including original design stop records; stopped schemas forbid findings | PASS |
| Original B99 fails with --sources and loses credit | Direct CLI reproduction reports failed=1, saved_executions=114, tested_skill_evidence=22/23, exit 1 | PASS |
| Q1 status/reason/manual verdict and credit behavior | Full existing canonical and CLI regressions pass | PASS within tested scope |
| Q2 input/output handoffs and ERROR -> NOT_RUN | Existing integration regression suite passes | PASS within tested scope; does not negate GATE-1 |
| Overall declared source-reference behavior | Integration accepts orphaned/empty finding references | FAIL, GATE-1 |
| Preserve v1.0.1 and separate release target | Archive SHA matches; package_release.mjs:10 targets v1.0.2 | PASS for pre-packaging review |

### Independently observed commands

A complete visible regression run produced:

```text
bun test tests/evidence-validation.test.mjs tests/integration-validation.test.mjs tests/package-validation.test.mjs
134 pass
0 fail
419 expect() calls
Ran 134 tests across 3 files. [8.55s]
```

The chained next command ran, establishing the test command exited 0:

```sh
bun scripts/validate_package.mjs --sources
```

It reported 5033 checks, 5033 passed, failed=0, 38 source files, 115/115 canonical executions, 23/23 fully evidenced skills, and integration 5 scenarios/10 records/5 handoffs. Its chained audit command then started, establishing this validator also exited 0. These results match the inspected P/reports/validation.json. The reviewer did not use --report or regenerate the registry.

The canonical B99 check used the supplied existing directory:

```text
/tmp/skills-q3-source-qa-FuxIu6/agent_skills_foundation_v1
```

Its scripts, schemas, registry and inventory match P. Recursive comparison found only the deliberately changed canonical evidence plus two earlier report versions. The reviewed creator script is /tmp/skills-q3-source-qa.mjs. Running the existing copied CLI with --sources gave:

```text
failed=1
ux-usability-review/normal-1: finding 0 source_ids must resolve to inventory, skill and actual provenance
source_files_checked=38
saved_executions=114
scenario_cases=115
tested_skill_evidence=22/23
B99_CLI_EXIT=1
```

An independent in-memory Bun build of build_registry.mjs, validate_package.mjs and package_release.mjs completed successfully with three output bundles and no logs. write:false prevented output-file creation. This verifies parsing/bundling, not TypeScript diagnostics.

## Direct remove-ai-slops and programming review

Loaded and consulted both available skills:

- /home/declan/.omo/binary-runtime/5.1.35/plugin/skills/remove-ai-slops/SKILL.md
- /home/declan/.omo/binary-runtime/5.1.35/plugin/skills/programming/SKILL.md

Their review criteria were applied directly to the actual diff, production validators and tests. Their editing/delegation procedures do not override this task's one-reviewer, report-only scope. The executable delta is JavaScript .mjs; no TypeScript rewrite, new dependency or architectural refactor is imposed.

- Root cause and shared paths: The canonical patch is placed at its evidence boundary rather than hard-coding B99 or a single fixture. The sibling integration path was also inspected and exercised; its missing actual-provenance join is the actionable false-confidence finding GATE-1.
- Excessive/useless tests: The Q3 additions cover distinct boundary classes and department readers. The CLI regression separately proves exit/report behavior. No new useless test was identified. A pre-existing dedicated P1 null API test overlaps the generic engineering null test; this small duplication is a maintenance note, not a blocker.
- Deletion-only/requested-removal tests: None in the Q3 delta. Removing data from a temporary fixture to test required-field/reference rejection is behavioral fault injection, not a test that pins deletion of production code.
- Tautological/implementation-mirroring tests: No new assertion derives expected success from the validator's own result. Tests inspect failures and execution credit from real mutated package fixtures. The original unmodified corpus supplies an independent positive baseline. The prose-edit regression tests independence from review wording, not a phrase or snapshot.
- Coverage gaps: Integration tests at tests/integration-validation.test.mjs:86-89 cover unknown sources and changed entries but omit the two GATE-1 cases. Canonical tests cover these classes; that does not establish parity in another consumer. A green aggregate count was insufficient evidence.
- Parsing/normalization/extraction: The patch adds one inventory load, one source-ID set and local comparisons. It introduces no new production extraction layer, string normalization, compatibility fallback or one-use helper. isDeepStrictEqual reuses the existing standard-library comparison and preserves the exact-copy contract.
- Boundary validation: Additional checks apply to untrusted saved JSON at the validator boundary. The design empty-provenance exception is explained and constrained by existing stopped-output schemas; existing fixtures were not weakened.
- Determinism and integration: New tests use unique temporary roots, awaited reads/writes and cleanup, without sleeps or polling. They call the real validators/CLI; no mock supplies desired validation results.
- Maintenance/scope: Existing long validator/test modules and bounded schema machinery remain maintenance considerations. No claimed success criterion requires a refactor merely for size or taste. No new type/test suppression, unrelated dependency or source-recovery work was found.
- Skill-perspective report coverage: The prior v1.0.1 full gate explicitly documents both skills and overfit/slop checks, but it is historical. Current Q3_CONTRACT_QA.md and QA_REPORT.md do not explicitly document the full two-skill perspective checklist. No separate current code-review report or notepad path was supplied or located. This report does not pretend that its direct inspection proves a missing earlier review occurred. The input gap is a NOTE, not the reason for rejection.

## Other observations and known limits, not blockers

- A separate read-only probe changed T2-ux verification[0].result from PASS to FAIL while retaining COMPLETE; validateIntegration accepted it. This is not used as an additional blocker: the UX contract defines COMPLETE as review completion, not product quality, and allows FAIL verification results. The broader canonical readiness rule may deserve clarification, but imposing a new integration success-status meaning would exceed demonstrated criteria.
- The 209 source-recovery items remain BLOCKED. Original missing PDFs/pages, book-wide semantic integration, real service/persona/account data, rendering, campaigns, transactions and live product certification are not required to repair this mechanical reference defect.
- The manual integration records remain bounded synthetic/self-reviewed slices. Successful structural validation does not prove narrative truth, book interpretation or live outcomes. No failure was invented from the lack of such evidence.
- Final v1.0.2 ZIP, regenerated manifest, extraction/hash roundtrip and final summary gate are explicitly scheduled after a favorable verdict. Their absence now is not a blocker. The package release script was not executed.
- LSP was requested independently and failed to initialize: "Could not find a valid TypeScript installation." No clean LSP/typecheck is claimed. No separate configured lint/security run was established in this scope.
- Python audit --check was started with PYTHONDONTWRITEBYTECODE=1. Its completion was not available in the tool output at report time, so the executor's nine-exact-artifact claim is not independently certified here. The visible combined command auto-detached while that audit was running, after tests and package validation completed. No audit failure is inferred. This missing completion is not needed to establish GATE-1.
- Background completion/output tools were not exposed in this reviewer session. Initial background test/CLI/audit handles did not yield completion output, so a foreground collection run was used to obtain the complete test and package-validator output above. It too detached on the long audit. Only observed results are claimed.
- The original design DOCX was identified but not independently extracted/read; original intent is taken from the explicit user brief, the original Q3 QA report and the inspected acceptance/contract documents. Full historical semantic re-execution of every saved answer was not performed.

## Checked artifacts

Directly read or inspected by actual diff/search under P:

- AGENTS.md, README.md, CHANGELOG.md, KNOWN_LIMITATIONS.md.
- scripts/evidence-validation.mjs, scripts/integration-validation.mjs, scripts/schema-validation.mjs, scripts/validate_package.mjs, scripts/package_release.mjs.
- tests/evidence-validation.test.mjs, tests/integration-validation.test.mjs, tests/package-validation.test.mjs.
- tests/integration/manual-scenarios.json; the T2-ux and adjacent provenance/record sections of tests/integration/manual-results.json.
- tests/ux-usability-review/evidence/normal-1.json; skills/design/ux-usability-review/SKILL.md output/branch sections; schemas/skills/ux-usability-review.output.schema.json.
- Source/output contract references across skills/*/*/SKILL.md, including COO/content provenance requirements and all four design finding/provenance contracts.
- reports/QA_REPORT.md, reports/Q3_CONTRACT_QA.md, reports/KNOWN_LIMITATIONS.md is not a path claimed: the actual limitations file is P/KNOWN_LIMITATIONS.md.
- reports/EVIDENCE_CONTRACT_QA.md, reports/INTEGRATION_CONTRACT_QA.md, reports/ACCEPTANCE_MATRIX.md, reports/RELEASE_CHECKLIST.md, reports/GATE_REVIEW_v1.0.1.md, reports/validation.json.
- scripts/audit_sources.py entrypoint/check-only behavior and initial definitions; not every scanner implementation line.

Other checked paths:

- /home/declan/Documents/Projects/Products/04_Skills/QA_FULL_REVIEW_v1.0.1_2026-11-03.md.
- The published v1.0.1 ZIP hash and supplied extracted baseline B, with recursive B/P comparison and exact changed-code/test diffs.
- /tmp/skills-q3-source-qa.mjs and its existing fixture's changed canonical JSON; fixture/P recursive comparison and actual source-aware copied CLI.
- /home/declan/Documents/Projects/Skills-and-Automation/contents-production-skills/.omo/evidence/skills-v1.0.1-gate-review.md, explicitly treated as historical rather than current approval.

The reproduced test suite and package validator additionally read all canonical cases, output schemas, evidence/adjudications, selected input schemas, integration fixtures, registry, inventory and 38 referenced source files. Runtime traversal is not represented as manual line-by-line semantic review.

## Report placement and reviewer writes

No JS eval tool was available. The equivalent SDK status call was executed through Bun using OMO_AGENT_TOOLKIT_SDK_ROOT and returned ULW_LOOP_PLAN_MISSING for child session 01a1a0be-2e91-72c8-a826-3361f30cb787. The explicitly authorized fallback path is therefore used.

The reviewer authored only this report. No implementation/test/schema/product-source edits, fixes, commits, packaging or delegation were performed. Existing test suites created their own temporary fixtures. Adversarial integration probes were process-local read overlays with zero filesystem writes.
