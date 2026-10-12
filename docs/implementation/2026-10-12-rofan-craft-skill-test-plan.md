# Rofan craft skill application test plan

## Purpose and scope

Validate that a copied package reader can discover and apply saved Rofan craft examples only when a brief has a matching cue or explicitly asks to reuse a saved case. A successful answer transfers a bounded saved observation into a new proposal, keeps canonical ownership and unknowns intact, and emits usable shot/cut/state/QA decisions. This is a text/2D documentation application test, not an assessment of rendered naturalness or generator controllability.

The frozen prompts and semantic rubrics live in [`qa/rofan-craft-skill-evals.json`](../../qa/rofan-craft-skill-evals.json). Version 2 covers the five inventory families C/P/O/L/E, near-miss and ordinary-brief skips, the corrected L06 gesture→glow→separation→trajectory→impact/fragments→witness reader case, and eight saved-reader scenarios. Baseline artifacts are `qa/rofan-craft-baseline-run.json` and `qa/rofan-craft-baseline-suite-v2-run.json`; earlier v1 and T7/T9 results remain separately preserved. The final T12 active-owner run is `qa/rofan-craft-green-final-t12-run.json`; copied-package and engineering evidence is `qa/rofan-craft-package-smoke.json`. The final run has a per-scenario active-owner context policy, unlike the earlier broad-context baseline; it is not a paired causal comparison.

## Roles

- **Package maintainer / test operator:** builds isolated fixtures, selects the exact package-only context, preserves raw outputs, and records commands, exit status, and paths.
- **Fresh-context scenario runner:** answers one frozen prompt per stateless call using only the supplied copied-package skill context; does not see the design/spec, footage, other scenario answers, or expected assertions.
- **Independent semantic grader:** evaluates each full answer against the corresponding expected semantic assertions and safety-failure conditions. Read every answer; automated string/ID matching may assist navigation but cannot determine pass/fail.
- **Future media QA operator:** only under a separately approved real-output evaluation, checks actual generated media. This role is not exercised here.

## Starting conditions and isolation

1. Preserve a baseline snapshot outside the repository before any skill edit. Copy the current working-tree versions of all 23 manifest skills, including user edits; do not reconstruct them from Git HEAD. Retain the manifest and existing `scripts/install_package.py` needed to install the copy. Exclude `docs/superpowers`, source footage, private/semantic source bodies, and original Windows media paths from runner context.
2. Install the frozen source copy into a unique temporary skill root with the copied `scripts/install_package.py`. Never target `.codex`, `.agents`, or any globally installed root. Record the fixture path and installer argv/stdout/exit code.
3. Copy the full final working-tree package to a separate temporary source fixture after the skill changes land, then install it into a separate temporary skills root. Do not mutate either retained baseline snapshot or global installations.
4. Pass only package files needed for the active scenario. The old baseline suite used the frozen broad context list where those files existed; the final T12 suite used `active-owner-v1`, selecting the skill/contract, relevant casebank, and only active owner references/templates per scenario. The ordinary baker scenario intentionally omitted the casebank under the conditional cue policy. Record each actual context list and hash; these context conditions differ, so do not compare scores as a controlled improvement estimate.
5. Make one fresh-context call per scenario. Do not seed expected answers, use conversation history, or share other scenario answers. Preserve the exact full response, model/runner identifier if available, prompt ID, context file list, timestamp, and failures verbatim.


## Positive owner-field contract wording and context microtests

The saved raw microtest phases are versioned in `qa/rofan-craft-handoff-microtests.json`; they are diagnostic wording/context checks, not a significance test:

1. `control` records five returned outputs per frozen wardrobe/composite prompt from the pre-correction package; one original handle failed with `ECONNRESET` and its separate replacement is recorded, not counted as another scored response.
2. `final` records the T7 content-ready package condition: ten returned outputs across the same two prompts, with one failed attempt and a separate replacement.
3. `post_T9` records ten fresh outputs on the T9 package using the earlier broad 18-file context. It showed output-shape variance; notably, three of five composite repetitions used 16 seconds despite the 12-second brief. These are preserved, not replaced by later answers.
4. T12 received one active-owner-context composite probe, saved separately in `qa/rofan-craft-composite-context-t12-probe.json`. Its requested 12-second duration and event coverage were correct, but it omitted canonical 09 elision fields and explicit actual-file EOS/container-tail checks. Per the user’s gate, no repetitions were run after this probe did not meet the frozen acceptance.

The final full v2 T12 run below supplies one fresh call for every frozen scenario. Read and grade each complete response against its frozen semantic rubric; do not grade source-string echoes, invent additional assertions, or claim convergence/statistical robustness from these small samples.


## Scenario execution steps and expected outcomes

1. Confirm the fixture contains the manifest’s 23 skill IDs and its installed files match the isolated copied source. Confirm the runner system contains no design/spec, this test plan, footage, or other scenario answers.
2. Run the frozen v2 prompts against the old package with one fresh stateless `completion()` call per scenario (`model="default"`). Preserve exact prompts, available package context, raw output, and errors. The baseline composite output and 18-call suite remain at `qa/rofan-craft-baseline-run.json` and `qa/rofan-craft-baseline-suite-v2-run.json`.
3. Install the final working-tree package to a new temporary root. For each T12 scenario, assemble only its recorded active-owner package files; do not include rubrics, expected assertions, other prompts, or repository docs in model context.
4. Run each frozen prompt once in a fresh stateless call. Preserve all 18 responses, exact prompts, context file lists/hashes, and model selection in `qa/rofan-craft-green-final-t12-run.json`. Requested model was `default`; the helper did not expose a resolved model, recorded as `UNKNOWN`.
5. Manually read each complete output against its frozen semantic assertions and safety conditions. Score retrieval/usefulness separately from guard correctness. A correct `UNKNOWN` is safe but can miss positive retrieval; do not add unrequested requirements or grade only case-ID/string echoes.
6. Report context differences and incomplete conditions. Baseline used a broad context; T12 used per-scenario active-owner context, with the casebank omitted for the ordinary brief. Do not claim a paired causal effect or statistical improvement. The separate on-demand reader-flow artifacts are observations, not additional stateless suite responses.
7. Verify negative outcomes: an already-established contact does not acquire first touch, flare does not imply rack focus/cut, and an ordinary baker brief gets no forced saved-case application. Record when the casebank was absent from context separately from a bank-loaded model choice.
8. Record assertion misses, safety failures, safe unknowns, unavailable/unperformed conditions, raw paths, runner identity, and any model/context differences. Do not claim statistical or causal skill improvement from this descriptive sample.

## Acceptance criteria

- Frozen v2 prompts exercise C/P/O/L/E, the eight reader scenarios, near-miss branches, saved-case reuse, and ordinary-brief skip; expected catalog IDs are compared per group against the exact spec row set, not a total alone.
- Every stateless call uses package-only context, the frozen prompt, and the requested `default` model selection; grading assertions are excluded from model context.
- Preserve raw responses and manually read every answer. Retrieval/usefulness and guard/safety are scored separately; a correct `UNKNOWN` is not a safety failure but may miss positive retrieval.
- Positive outputs are usable proposals in existing owner fields, with requested duration, actor counts, source-vs-proposal distinction, exact canonical timing/elision fields, and actionable QA where applicable. A case-ID echo alone does not pass.
- Negative outputs preserve requested state and do not force irrelevant case usage or universal craft rules.
- This is a technique/reference application test, not a discipline-enforcing skill. The owner-field recipe wording microtest is justified by a concrete output-shape defect; pressure-scenario rationalization tables/red flags are not applicable.
- Record copied-package install, link/table/field/timing smoke and version/full-suite command outputs. Do not modify versions or global installation roots.
- Real-media generation/naturalness and endpoint controllability remain **NOT RUN**.
- One response per prompt is descriptive only; no statistical or causal improvement claim.

## Final observed results

- **Final fixture:** source copy `C:\Users\Declan\AppData\Local\Temp\rofan-craft-final-t12-yaxxnwjz\source`; isolated installed root `C:\Users\Declan\AppData\Local\Temp\rofan-craft-final-t12-yaxxnwjz\skills`; casebank SHA-256 `cae803553b5858c1d201d69868b7ace1a3210a0cc71d1150ca898e9c5e3fdd1b`. The existing installer exited 0 and installed 23 skills, package version 2.5; no global install root was passed.
- **Structural smoke:** `qa/rofan-craft-package-smoke.json` records full command stdout and results. All 23 manifest IDs and installed directories matched, installed files matched the copied source apart from installer-generated support content, and the exact case ID sets matched the spec by group (C12/P17/O10/L9/E9; no missing, extra, or duplicate IDs). The eval catalog set also matched. Across 69 Markdown files in the updated skill, 384 relative links were checked; all resolved within the isolated installed skills root, including nine cross-skill links. Changed/canonical tables had no width errors; the exact 06 cue and 09 elision headers, active 09 cut fields, 11 support field, shot-local formula, and requested handoff section were present. A naive broad parser diagnostic on unchanged `20-visual-mode-ssot.md:82` was inspected: the pipe is inline-code prose, not a table; it is not reported as a table defect.
- **Version/test commands:** `python scripts/check_versions.py` exited 0 with `version check OK: package 2.5, 23 skill(s) consistent`. `python -X utf8 -m pytest -q` exited 0: **258 passed, 1 skipped, 2 warnings, 217 subtests passed**. The two warnings are `PytestUnhandledThreadExceptionWarning`/`UnicodeDecodeError` from subprocess reader threads in `scripts/test_sync_installed.py::test_stale_link_is_repointed` (byte offset 213) and `test_remove_link_never_deletes_target_content` (offset 222). Full actual stdout is retained in the package-smoke artifact; no version was changed.
- **Final stateless suite:** `qa/rofan-craft-green-final-t12-run.json` contains all 18 raw responses, exact prompts, context file lists/hashes, model selection (`default`, resolved model `UNKNOWN`), and the manual semantic grade. Results: **15 PASS, 1 PASS_WITH_CONTEXT_LIMIT, 2 PARTIAL_NOT_MET, 0 safety/guard failures**. The limited ordinary-brief result used active-owner context without the casebank; the separate actual reader-flow record above is not counted as an independent stateless repetition.
- **Unmet semantic assertions:** `reader_07_unavailable_source_body_unlistened_audio` gives safe generic access/audio limits but does not identify/apply the preserved bounded excerpt to a concrete transfer, so positive application is partial. `composite_baseline_contact_wardrobe_gate_ending` retrieves the relevant cases and gives safe, usable proposed beats, but omits the exact canonical six-column 09 elision row and explicit separate actual last-picture/container-tail checks. Its six-column active 09 cut table is accepted; inactive columns from the full template are not required. Its 06 time column is expressly final-timeline time; absence of an unrequested 06 cue table is not graded as false local-time arithmetic. Reader 08’s complete raw output includes `도구 지원 확인 = UNKNOWN` for W1 and W2 and is graded PASS; the correction audit is preserved in the raw-run artifact.
- **Other context-flow evidence:** `qa/rofan-craft-green-discovery-followup.json` is the Main runner’s actual on-demand composite retrieval response, re-emitted from its prior call rather than a fresh independent repetition. Retrieval and guard behavior passed, but that T9 response missed shot-local conversion and canonical 09 handoff fields. `qa/rofan-craft-ordinary-brief-followup.json` records one T7 actual ordinary-brief discovery flow that did not consult the casebank. These observations are not part of the T12 18-call grade.
- **Interpretation:** The text/2D application goal is partially met but the frozen suite is **not all-pass**. Baseline and T12 use different context policies, and the small, varying set of calls does not establish statistical or causal improvement.
- **Not run:** Real-media generation, endpoint checks, Blender, playback/naturalness QA, and actual file EOS/container-tail inspection. The future-media recipe and design-proposal threshold below are planning guidance only, not evidence.
- **Post-writer changed-document smoke:** `qa/rofan-craft-package-smoke.json` records the final document-only check. It covered README, CHANGELOG, the canonical spec, application plan, and this test plan: 61 relative links including five fragments, zero missing targets/fragments, and 25 Markdown tables with no width errors. The required result/package-smoke and document targets resolved; all five documents state the same T12 outcome (15 PASS / 1 PASS_WITH_CONTEXT_LIMIT / 2 PARTIAL_NOT_MET, guard 0). The first post-writer check found two `../../../implementation/...` links to the test plan; the writer corrected them to `../../implementation/...`, and the final check passed. This follow-up did not rerun pytest, version checks, or package installation.


## Exact reproduction commands

Commands are run from repository root in PowerShell. `<BASELINE_SOURCE>`, `<BASELINE_SKILLS>`, `<UPDATED_SOURCE>`, and `<UPDATED_SKILLS>` are unique temporary paths, never installed user roots. Build each source snapshot by copying the current 23 manifest skill directories and installer into an isolated source package; include package support inputs required by the installer but remove any copied `video-production-assets/support/` directory from the source skill before calling the installer, since installer itself populates that destination. The baseline fixture is made before source edits; the updated fixture is made after all current changes land.

```powershell
python -X utf8 <BASELINE_SOURCE>\scripts\install_package.py --repo-root <BASELINE_SOURCE> --skills-root <BASELINE_SKILLS>
python -X utf8 <UPDATED_SOURCE>\scripts\install_package.py --repo-root <UPDATED_SOURCE> --skills-root <UPDATED_SKILLS>
```

Run the prompts with the documented `functions.eval` completion helper: in a fresh eval call, read only the available context files from the selected isolated installed package, assemble those files as `system`, then for each `scenario` start `completion(scenario["prompt"], model="default", system=package_context).wait()`. Use a separate completion call per prompt, do not expose rubrics/assertions, and record the actual resolved model only if the helper reports it; otherwise state `UNKNOWN` (requested selection is `default`). Context-file names listed in the eval fixture but absent from the baseline package are omitted and explicitly listed in raw-run metadata. The earlier v1 outputs are preserved at their original prompt version and must not substitute for the corrected v2 prompts. The following repository checks are reproducible after updated content is complete:

```powershell
python scripts/check_versions.py
python -X utf8 -m pytest -q
```

The README documents pytest and Pillow as requirements and specifies UTF-8 mode on Windows. Also record copied-package smoke output and compare the set of installed IDs with the manifest/spec's expected 57-case coverage contract (not just a total); validate mandatory internal links resolve inside the installed skill folders, Markdown tables/canonical fields, and the required eight semantic reader scenarios. Do not report a check as passed unless it was actually run and its output recorded. Version checks do not authorize changing versions.

## Limitations and future real-media test

This evaluation measures whether a reader retrieves and correctly translates documentary saved evidence into a proposed 2D production plan. It cannot establish that a model follows the plan, that generated movement/contact/wardrobe/mirror effects look natural, that timing is convincing, or that a selected endpoint can perform the task. It does not examine or reopen source videos, listen to audio, call endpoints, create images/video, run Blender, or assert a real QA failure.

A future real-media naturalness/production-quality evaluation is **NOT RUN**. It requires the user's explicit approval for actual generation, use of rights-cleared approved character/location/wardrobe assets, endpoint/capability review and budget authorization through existing routes. For a controlled text/2D study, render a short arrival-and-contact shot, a multi-phase magic/event shot, and a work-to-mirror wardrobe reveal with at least three independent outputs per brief from one declared endpoint/model/version/settings; retain all rendered files and prompt/settings. Two reviewers who did not write the prompts should independently score each output on a 1–5 scale for (a) gait/approach legibility and visible-foot evidence, (b) contact-state readability and continuity, (c) event phase/hold/cut-boundary readability, and (d) wardrobe/posture/reflection continuity across the edit; mark any unsupported source claim, invented first-touch, unexplained state jump, or technical defect as a separate binary defect. Record disagreements and adjudicate against the actual video; do not infer quality from plan prose. This future procedure is a concrete proposal only: media, approvals, endpoint, budget, reviewers and results are absent here. It is **NOT RUN**. Actual-output QA remains owned by the existing QA procedure; prose and saved observations cannot substitute for inspection. **Proposed acceptance gate (design proposal, not an established fact):** any hard identity/contact/state/cut defect fails the review; for every applicable 1–5 criterion, each reviewer must score at least 4 before the output meets the proposed gate. If feet are cropped, footfall/gait evidence is **N/A or unverified**, not an automatic pass. Preserve independent scores and resolve disagreements by viewing the actual file, documenting both original scores and the adjudicated rationale. Do not claim quality improvement or a causal skill effect from this media study without a controlled paired baseline using the same prompt, endpoint/model/version, settings, and comparable resource budget; otherwise report observations descriptively.

## Post-T13 skill wording microtest

This is a separate, descriptive 15-call microtest of the finalized saved-case reference, not a rerun or replacement of the old-package baseline or the T12 18-scenario suite. The frozen prompts and rubric remain in `qa/rofan-craft-post-improvement-microtest-matrix.json`; raw text, prompt/context hashes, and the final casebank hash are preserved in the three per-scenario raw files below.

**Setup and call status:** After the implementer’s stable signal, the casebank was independently hashed from the working-tree source and a copied package fixture, then installed into a new temporary skills root. Source and installed `rofan-craft-examples.md` both hash to `5c4cae3f345258eedd018aa4cce09eed2c313ca9ccd06d92ed9c06da4c2ea333`. The fixture copied the 23 current manifest skills and package inputs; `install_package.py` exited 0 and installed 23 skills, package version 2.5, into `C:\Users\Declan\AppData\Local\Temp\rofan-craft-post-t13-src-tkb9lg9w\skills`. No global skill root was changed. One fresh stateless `completion(prompt, model="default", system=package_only_context).wait()` call was made for each of five repetitions per prompt. The package-only active context for the composite prompt includes `21-generated-video-qa-retry.md`; rubrics, expected answers, design/spec docs, other prompts, and footage were not provided to any model call. All **15/15** calls completed; **0** are pending and none were duplicated. The resolved model was not exposed by the helper (**UNKNOWN**).

| Scenario | Results | Final independent-review result |
|---|---:|---|
| `reader_07_unavailable_source_body_unlistened_audio` | 0 full pass, 5 partial; D797 excerpt 0/5, title-to-live hypothetical 0/5; P14 audio/access guards 5/5 | The full casebank and bounded D797 cue were present in the exact context, but all five responses missed the expected D797 opening excerpt and its concrete title-to-live hypothetical. All five preserved P14 audio/access boundaries and unknowns. |
| `composite_baseline_contact_wardrobe_gate_ending` | 0 full pass, 5 partial; retrieval 5/5, active cut fields 5/5; canonical elision row 2/5; separate planned ending checks 0/5; guards 5/5 | Every response retrieves relevant cases, preserves the brief, and passes guards. Two contain the canonical elision row, but none meets the complete requirement including separate planned last-picture/container-duration checks; no actual inspection is claimed. |
| `negative_ordinary_brief_skip_casebank_loaded` | 5/5 full pass | With the casebank loaded, every response correctly avoids forcing unrelated cases and gives practical continuity QA. |

The initial self-grade is **superseded by the final independent review**: across all 15 completed calls, **5 full passes, 10 partial, 0 not met, and 0 safety/unknown-guard failures**. The ordinary loaded-casebank negative control passes 5/5. No calls were rerun for the correction. These are descriptive small samples, not causal or statistical evidence of improvement. The loaded-bank negative control is not compared as a paired result against T12’s bank-absent ordinary-brief call.

**Raw evidence:** `qa/rofan-craft-post-t13-reader07-raw.json`, `qa/rofan-craft-post-t13-composite-raw.json`, and `qa/rofan-craft-post-t13-ordinary-loaded-raw.json`. Per-repetition manual evidence and aggregate grades: `qa/rofan-craft-post-t13-microtest-grade.json`. No T12 or baseline evidence was overwritten. Real-media generation, playback/naturalness review, 3D/Blender, and endpoint capability checks remain **NOT RUN**.

## Post-T14 conditional casebank revision microtest

This frozen 15-call run was an intermediate follow-up before the completed final T15 microtest recorded below. Prompts, rubrics, and context order were identical to T13, with only the casebank changed; source and installed hashes were 31785f6ed7b7a9e99e9830101ceb8bbdebad2d0da54ec45b5b30928a65f8740e. The T13 isolated root was copied, other context-file hashes verified, and the reconstructed prior system SHA matched before calls. Model selection was default, resolved identity UNKNOWN; all 15 calls completed.

| Scenario | Final reviewed result |
|---|---|
| `reader07` | 4/5 full pass, 1 partial; safeguards 5/5. |
| `composite` | 0/5 full pass; ending checks, retrieval/brief/guards 5/5; active cut fields 0/5; elision rows varied. |
| `ordinary-loaded` | 5/5 full pass. |

Aggregate: **9/15 full, 6 partial, 0 not met, 0 guard failures**. Composite responses exposed conflation of the cut table with the elision row and omission of active cut fields, motivating a separate corrective patch. Descriptive small sample only; no causal or statistical claim. No prompts/rubrics changed. Raw outputs: `qa/rofan-craft-t14-reader07-raw.json`, `qa/rofan-craft-t14-composite-raw.json`, `qa/rofan-craft-t14-ordinary-loaded-raw.json`; grade: `qa/rofan-craft-t14-microtest-grade.json`. Media generation/inspection and endpoint checks remain **NOT RUN**.

## Post-T15 final conditional casebank microtest

This is the final tested status for this conditional casebank microtest. The 15 calls used frozen prompts, rubrics, and context order, changing only the casebank against the verified T14 context. Source and installed casebank matched at SHA-256 `5f6318d827249fb41c2409478413e3d086bf963579bb3f9a7702eadf85758c25`; the unchanged context was verified, with only the casebank replaced. Model selection was `default`; resolved identity **UNKNOWN**. All 15 calls completed.

| Scenario | Final reviewed result |
|---|---|
| `reader07` | 3/5 full pass, 2 partial; both misses gave only generic limits and omitted the matching D797 excerpt. Unknown/proposal guards passed 5/5. |
| `composite` | 4/5 full pass, 1 partial; cut fields 5/5, canonical elision 4/5, ending checks 4/5. The partial contradicted the requested 12s with a 14s timeline and omitted elision/file-end planning, with extraneous inactive fields. |
| `ordinary-loaded` | 5/5 full pass; no unrelated cases forced. |

Aggregate: **12/15 full pass, 3 partial, 0 not met, 0 guard failures**. Results retain reader07 misses and composite variance; this descriptive sample supports no causal or statistical claim. No media generation/playback/inspection, 3D/Blender, or endpoint checks were performed (**NOT RUN**). Raw outputs: `qa/rofan-craft-t15-reader07-raw.json`, `qa/rofan-craft-t15-composite-raw.json`, `qa/rofan-craft-t15-ordinary-loaded-raw.json`; grade: `qa/rofan-craft-t15-microtest-grade.json`. Frozen prompts/rubrics were not changed.

## T16 evidence-condition retrieval microtest

After T15, the quick-use rule was clarified generically: evidence-only/source-access/audio questions also match evidence conditions across the supporting-cue tables and main index, keeping distinct records/locators separate. The only skill change was the existing casebank; frozen prompts, context order, and rubric were unchanged.

The 15 fresh calls used isolated root `C:\Users\Declan\AppData\Local\Temp\rofan-craft-t16-final-eyxfizij\skills\video-production-assets`, copied from T15 and replacing only `rofan-craft-examples.md`. Source and installed casebank matched at SHA-256 `e76241a6cfa365ca4467ef8383f3d5b94604dac8c24185f545a91732d5212a33`; all unchanged context file hashes matched T15 metadata. Model selection was `default`; resolved identity **UNKNOWN**.

| Scenario | Final reviewed result |
|---|---|
| `reader07` | 2/5 full pass, 3 partial; two answers identify and concretely transfer the bounded title-to-live-image excerpt; three retain safe generic unknowns but miss that positive retrieval. No unknown/proposal guard failures. |
| `composite` | 0/5 full pass, 5 partial; 5/5 retrieve relevant observations, 2/5 use only the active six-column cut table without inactive columns, 3/5 include a canonical elision row, and 0/5 separately plan actual last-decoded-picture and container-duration checks. |
| `ordinary-loaded` | 5/5 full pass; no unrelated case application. |

Aggregate: **7/15 full pass, 8 partial, 0 not met, 0 guard failures**. The evidence-condition rule coincided with concrete excerpt retrieval in 2/5 responses; the other three remained generic. Composite compliance remains variable and was not further patched. This descriptive sample supports no causal/statistical claim. Raw outputs: `qa/rofan-craft-t16-reader07-raw.json`, `qa/rofan-craft-t16-composite-raw.json`, `qa/rofan-craft-t16-ordinary-loaded-raw.json`; per-response grade: `qa/rofan-craft-t16-microtest-grade.json`. No media generation, actual-media inspection, 3D/Blender, or endpoint checks were performed (**NOT RUN**).

### Repository checks after T16

Against the final casebank SHA-256 `e76241a6cfa365ca4467ef8383f3d5b94604dac8c24185f545a91732d5212a33`:
- `python scripts/check_versions.py` — **PASS**: `version check OK: package 2.5, 23 skill(s) consistent`.
- `python -X utf8 -m pytest -q` — **PASS**: `258 passed, 1 skipped, 2 warnings, 217 subtests passed in 28.35s`. The warnings were Windows subprocess reader-thread UTF-8 decode errors in `scripts/test_sync_installed.py::test_stale_link_is_repointed` (byte 213) and `scripts/test_sync_installed.py::test_remove_link_never_deletes_target_content` (byte 222). Skip identity was not present in the output.

Fresh installation was run separately from the T16 evaluator, which reused its copied T15 root with only the casebank replaced and matching other context hashes. The initial live `--repo-root .` installer attempt found preflight collisions with generated `video-production-assets/support/{manifest.json,examples,qa,CHANGELOG.md}` and wrote nothing. The safe smoke used a clean temporary source snapshot excluding generated `video-production-assets/support/`, copying the manifest, package inputs, installer, and 23 listed skill directories, then installing into a separate empty skills root. Installer exited 0: package 2.5, 23/23 exact skill IDs; source and installed casebank SHA-256 both `e76241a6cfa365ca4467ef8383f3d5b94604dac8c24185f545a91732d5212a33`; 129 casebank links, 0 broken/escaping; 15 tables, 0 width errors. Source snapshot: `C:\Users\Declan\AppData\Local\Temp\rofan-t16-install-smoke-ty_1a58w\source`; skills root: `C:\Users\Declan\AppData\Local\Temp\rofan-t16-install-smoke-ty_1a58w\skills`. No repository files or global root changed.

## T17 scoped 09 field-projection evaluation

Clarified the existing 09 edit reference: full 09 handoffs still use the full template; scoped handoffs project only applicable existing sections and fields, preserve their semantics, omit inactive columns, and keep numeric `final_start_s` / `final_end_s` separate. No new schema was introduced.

T17 ran the full 15-call frozen suite using the T16 installed root copied to `C:\Users\Declan\AppData\Local\Temp\rofan-craft-t17-final-p0o_wusn\skills\video-production-assets`, replacing only `references/09-edit.md`. The reader and ordinary-control system hashes match T16; the composite context differs only by `09-edit.md`. Prompts, context-file order, and rubric were unchanged. Model selection was `default`; resolved identity **UNKNOWN**.

| Scenario | Final reviewed result |
|---|---|
| `reader07` | 3/5 full pass, 2 partial; all five preserve the access/audio unknown guards. One response identifies the excerpt and mechanism but gives no concrete mapped/hypothetical application; another remains generic. |
| `composite` | 0/5 full pass, 5 partial; 5/5 use only the six active cut fields, 5/5 include a canonical elision row, and 0/5 separately plan both actual-picture and container-duration checks. All honor the 12-second brief and preserve the relevant source/brief boundaries. |
| `ordinary-loaded` | 5/5 full pass; no unrelated case application. |

Aggregate: **8/15 full pass, 7 partial, 0 not met, 0 guard failures**. The scoped-field clarification coincided with active-only cut tables in 5/5 composite responses, versus 2/5 in T16; this is a descriptive comparison, not a causal claim. The missing separate ending checks remain an unmet requirement and were not addressed by another rule. Raw outputs: `qa/rofan-craft-t17-reader07-raw.json`, `qa/rofan-craft-t17-composite-raw.json`, `qa/rofan-craft-t17-ordinary-loaded-raw.json`; per-response grade: `qa/rofan-craft-t17-microtest-grade.json`. No media generation, actual-media inspection, 3D/Blender, or endpoint checks were performed (**NOT RUN**).

### Repository checks after T17 source change

- `python scripts/check_versions.py` — **PASS**: `version check OK: package 2.5, 23 skill(s) consistent`.
- `python -X utf8 -m pytest -q` — **PASS**: `258 passed, 1 skipped, 2 warnings, 217 subtests passed in 31.96s`. The warnings were Windows subprocess reader-thread UTF-8 decode errors in `scripts/test_sync_installed.py::test_stale_link_is_repointed` (byte 213) and `scripts/test_sync_installed.py::test_remove_link_never_deletes_target_content` (byte 222).

## T18 planned file-end check evaluation

Added a conditional planning requirement to `references/21-generated-video-qa-retry.md`: for plans ending with a title/credits/bonus/interstitial/apparent close, separately plan a last-decoded-picture check and a container-duration/tail check; without an output file, both actual results remain UNKNOWN/pending. No schema or unrelated-end requirement was added.

T18 ran 15 fresh stateless calls with the frozen prompts, rubric, and context order. Its isolated root `C:\Users\Declan\AppData\Local\Temp\rofan-craft-t18-final-kb89sxrz\skills\video-production-assets` was copied from T17 and only `references/21-generated-video-qa-retry.md` was replaced. Reader07 and ordinary-control context/system hashes match T17 exactly; the composite context differs only in that 21 reference. The casebank and 09 reference remained unchanged. Model selection was `default`; resolved identity **UNKNOWN**. All 15 calls completed.

| Scenario | Final reviewed result |
|---|---|
| `reader07` | 4/5 full pass, 1 partial; each retrieves the bounded excerpt and preserves access/audio limits. The partial gives the mechanism but no concrete mapped/hypothetical adaptation. |
| `composite` | 1/5 full pass, 4 partial; active-only cut fields 1/5, canonical elision row 5/5, explicitly separate planned last-picture/container-tail checks 1/5. All preserve the 12-second brief and applicable guards. |
| `ordinary-loaded` | 5/5 full pass; no unrelated case application. |

Aggregate: **10/15 full pass, 5 partial, 0 not met, 0 guard failures**. The conditional endpoint guidance coincided with an explicit separate planned-check pair in 1/5 composite responses. A second named both actual endpoints but did not plan them as separate checks; 3/5 reported unknown/pending without both planned checks. Compared descriptively with T17, active-only cut fields were 1/5 here versus 5/5, while explicit separate ending checks were 1/5 versus 0/5; this small sample does not establish causality, and output variance remains. Per-response grades: `qa/rofan-craft-t18-microtest-grade.json`; raw outputs: `qa/rofan-craft-t18-reader07-raw.json`, `qa/rofan-craft-t18-composite-raw.json`, and `qa/rofan-craft-t18-ordinary-loaded-raw.json`. Stop prose iteration here; remaining endpoint-check misses are an observed model/contract compliance limitation. No media generation, source playback, actual-media inspection, 3D/Blender, or endpoint checks were performed (**NOT RUN**). Prompts and rubrics were not changed.

### Final isolated install/link/table smoke after T18

A clean temporary source snapshot excluding generated support was installed into a separate empty temporary skills root; installer exited 0 with package 2.5 and 23/23 exact skill IDs. Source and installed hashes matched: casebank `e76241a6cfa365ca4467ef8383f3d5b94604dac8c24185f545a91732d5212a33` (129 links checked, 0 errors; 15 tables, 0 errors); `09-edit` `75eebd8b3bd40fe26507319650142b82cef37b563a233e4b1718a6e31af4a8af` (11 links, 0 errors); `21-generated-video-qa-retry` `f95647cbf0ad27f51435ba0cba3df9c42e73d11bc754b56d420f10d0c99d012d` (2 links, 0 errors; 1 table, 0 errors). Source: `C:\Users\Declan\AppData\Local\Temp\rofan-t18-final-smoke-m_2w311x\source`; skills: `C:\Users\Declan\AppData\Local\Temp\rofan-t18-final-smoke-m_2w311x\skills`. No repository or global-root changes. This final smoke supersedes the T16-only smoke as current final install/link/table evidence.
