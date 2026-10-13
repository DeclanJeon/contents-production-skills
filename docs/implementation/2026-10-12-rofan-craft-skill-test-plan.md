# Rofan craft skill application test plan

## Purpose and scope

The frozen T13–T20 suite is a historical case-retrieval and owner-field application test: it checks saved-case retrieval, conditional use, output fields, and a Rofan-like composite. It does **not** measure archive-wide craft extraction, positive cross-domain transfer, or skillification behavior. Its prompts/rubrics and all raw/grade artifacts remain frozen and unchanged. This plan now adds a separate fresh cross-domain owner-procedure smoke; do not merge its score into the frozen results.

The frozen prompts and semantic rubrics live in [`qa/rofan-craft-skill-evals.json`](../../qa/rofan-craft-skill-evals.json). Version 2 covers the five inventory families C/P/O/L/E, near-miss and ordinary-brief skips, the corrected L06 gesture→glow→separation→trajectory→impact/fragments→witness reader case, and eight saved-reader scenarios. Baseline artifacts are `qa/rofan-craft-baseline-run.json` and `qa/rofan-craft-baseline-suite-v2-run.json`; earlier v1 and T7/T9 results remain separately preserved. The final T12 active-owner run is `qa/rofan-craft-green-final-t12-run.json`; copied-package and engineering evidence is `qa/rofan-craft-package-smoke.json`. The final run has a per-scenario active-owner context policy, unlike the earlier broad-context baseline; it is not a paired causal comparison.
## Scope correction and current source-ledger status

The initially approved design narrowed the original request—analyze archive craft and distill transferable filmmaking methods into the existing content-production skill—to a 57-case retrieval/reference improvement, and explicitly made universal craft synthesis out of scope. That missed the owner-level transfer goal. The corrected path is archive-pattern synthesis → compare each relevant owner procedure/template/QA → install only an evidenced missing generic procedure/QA in its existing owner, and only on explicit skillification request. The casebank is optional provenance/evidence, not policy or a required prompt lookup; ordinary analysis remains read-only.

**Current F: evidence supersedes T20's historical C:/unavailable-source snapshot; T20 prompts, rubrics, raw responses and grades remain unchanged.** The F: root, manifest, dense-review metadata and semantic ledgers were directly read; no original-media playback was performed by the baseline/current implementation. Inventory: 44 MP4 occurrences from 50 manifest URLs, 44 downloaded and six YouTube HTTP 403s; 7,095,987,672 bytes (~7.095 GB), 33,419.9 seconds. Occurrences are not independent creators. Dense extraction: 44/44 files and 335/335 1.2-second intervals, each six frames at 5 fps, zero extraction failures; intervals cover only the first eight retained locator PTS/source and are not full video, exhaustive shots, human review by extraction alone, or continuous playback. Separately, the mechanical full-source run expected/observed/identified 44, with 1 complete and 43 failed; full-source PTS coverage is false. The distinct detector scan produced 6,002 candidates, retained only the first eight locator PTS/source, with no boundary certification and no motion inference. The current semantic master has 44 source rows, 34/44 materialized (24 complete ingests, one bounded augmentation, six partial actual, two craft-only partial, one endpoint-only), ten unmaterialized; `source_occurrence_count=30` conflicts with 44 rows/34 materialized. The index's 44/44 identities indexed is not closure; these exact global gates remain OPEN: `complete_scene_shot_event_crosswalk`, `all_visual_shot_content_checked_against_native_images`, `all_candidate_free transitions_and_first_last_images`, `all_source_scene_membership_bounds`, `occurrence_vs_independent_cases`. The selected EA6A ledger has 468 shots, 44 scenes, 39 events, 650 dispositions; its source status is `visual_semantic_craft_closed`, but 0.2-second sampling is not full-rate playback and machine audio was not human-listened. Stale schema/snapshot differences remain explicit in the design record. No full-archive completion, all-44 analysis, or prevalence claim follows. See the [current crosswalk design](../superpowers/specs/2026-10-13-rofan-archive-craft-crosswalk-design.md).

The original 5+1+1 prompts and criteria below remain unchanged. The results column records the observed first-smoke outcomes; no prompt or rubric was retroactively regraded. Separate one-row follow-ups and the unrelated baker comparison are recorded below.

## Archive crosswalk QA matrix (original prompt/criteria preserved; actual first-smoke outcomes recorded)

### Preserved exhaustive-mode baseline contract

The baseline is five fresh stateless calls on the exhaustive all-44 request. Baseline outcome: **0/5** supplied a joinable source occurrence→sequence/scene→shot→within-shot-event crosswalk or operational evidence-locator→mechanism→owner→QA chain; **5/5** distinguished detector candidates from confirmed cuts and acknowledged incomplete sources/no audio listening/no full-motion playback. Runner context used manifests/ledgers but did not open original video media; available dense extraction (335/335) was not all-shot source review. Requested model `default`, resolved identity `UNKNOWN`. This is a descriptive sample, not statistical evidence.

Exact baseline prompt (preserve verbatim for EXH-1..5):

> A user asks for an exhaustive all-44 source/shot craft analysis and how transferable craft should be represented for future skill use, explicitly not copying plot, characters, or props. Ask for the proposed analysis artifacts and owner transfer path. Respond to that user with a concrete useful artifact proposal and transfer path. Distinguish source facts, estimates, candidates, and unknowns. Evaluate whether existing evidence supports an exhaustive analysis; state source gates accurately. Do not analyze all 44 individual videos. Do not inspect or claim to inspect original media. No edits, generation, upload, API, or 3D. Keep the response concise and actionable.

Preserved baseline criteria: (1) joinable source occurrence→sequence/scene→shot→within-shot-event crosswalk; (2) operational evidence-locator→generic mechanism→existing owner→target-specific QA chain; (3) distinguish detector candidates from confirmed cuts; (4) explicitly acknowledge incomplete sources; (5) do not claim audio listening or full-motion playback when neither occurred. The runner context included installed `SKILL.md`, module 25, archive-audit and shot-DNA templates, and F: `full_archive_manifest.json`, `full_archive_summary.json`, and `dense-review/manual_review.json`; it read manifests/ledgers but did not inspect original video media. Post-run context must preserve those evidence files and current package routing/template files; do not substitute the older archive-coverage prompt.

### Scenarios and scoring

| ID | Context / request | Repetitions | Pass criteria | Results |
|---|---|---:|---|---|
| EXH-1..5 | Exact baseline prompt above, each in fresh stateless context; same F: manifest/ledger evidence files plus current package context (`SKILL.md`, module 25, archive audit, shot DNA, and new crosswalk template); `default` requested model | 5 | Each response satisfies all five preserved criteria above; output includes required crosswalk, explicit unresolved rows/open gates, and does not treat occurrence count as independent cases. | **NOT PASS** in preserved first post-edit five-call smoke; see linked result below. |
| NEG-SINGLE | Ordinary single-reference analysis; no exhaustive/cross-source scope | 1 | Does not force archive-wide crosswalk, all-source coverage, or casebank lookup; uses lightweight existing reference/shot-DNA path and retains evidence limits. | **PASS** in the preserved first-smoke negative controls; see [smoke result](../../qa/rofan-archive-crosswalk-smoke-results.md). |
| NEG-UNRELATED | Unrelated ordinary brief (no archive/reference craft request) | 1 | No crosswalk, archive audit, Rofan casebank, or source-derived rule is forced. | **PASS** in the preserved first-smoke negative controls; see [smoke result](../../qa/rofan-archive-crosswalk-smoke-results.md). |

Per-call record: exact prompt bytes and hash, fresh-context identifier, context file list/hashes, requested/resolved model, full raw output, criterion-by-criterion manual grade, guard failures, and run status. Do not write expected post-results here before running. Criteria are per-response, not an aggregate-only pass: exhaustive target 5/5; both negative controls must pass. Interpret this small sample descriptively, never as a statistical or causal reliability claim.

### Repository checks

After the instruction scenarios, run the repository's structural/link check and package-version smoke; run relevant tests as repository policy requires. Verify template links and conditional routing, no `project.json`/production schema/version changes, and no changes to frozen T13–T20 raw evidence/rubrics. These checks do not validate source media naturalness, full-source decode, all-shot coverage, or archive completion.

## First post-edit smoke — failed result preserved; context/rubric mismatch

The first post-edit five-call result remains **failed, not a pass**. The preserved scorer recorded C1 retrievable crosswalk **0/5**; C2 evidence→mechanism→owner→QA **0/5 complete, 1/5 partial**; C3 candidate-versus-confirmed outcome **1/5 pass**; C4 source gates **5/5 pass**; and C5 playback/audio claims **5/5 pass**. All five overall results were **NOT PASS**. This is distinct from the earlier baseline contract above. Preserve the original prompt, contexts, metadata, per-call grades, and all five outputs verbatim in the existing [smoke result record](../../qa/rofan-archive-crosswalk-smoke-results.md); the [raw runner output](artifact://8052:raw:1-1) also remains unchanged. Do not edit or replace either result artifact.

**Diagnosis:** this is a test-context/prompt-rubric mismatch, not evidence that the skill lacks source data. The prompt asked for a concrete artifact proposal and owner transfer path while explicitly forbidding an all-44 analysis; the rubric nevertheless demanded populated crosswalk rows. The F: context included only identity inventory, mechanical manifest/summary, and dense-review metadata—not the current semantic source master, provisional craft catalog, or a chosen source-specific semantic ledger. It also lacked the actual owner procedures/templates needed to name exact QA fields. Consequently C1 (joinable source/scene/shot/event row), C2 (evidence→mechanism→owner→QA chain), and C3 (candidate-vs-confirmed boundary outcome) were not sufficiently testable from the supplied context. Retain the observed misses; do not recast them as proof of a skill-data gap.

## One-row follow-up — preserved v1/v2 and known-model history

The original bounded one-row follow-up v1 is **NOT PASS**; its separate capture-failed v2 is **INCOMPLETE / UNGRADABLE**. The first known-model run is **NOT PASS** on coverage status; known-model v2 is **NOT PASS** on C1/C4/C5; index-aware known-model v3 is **NOT PASS** because its otherwise complete 06 field map omitted applicable `크기/카메라 위치` (preserve the frozen v3 rubric/outcome). V4 is separately **PASS** across the new predeclared acceptance, including that field. Preserve every prior result; see [follow-up v1](../../qa/rofan-archive-crosswalk-followup-results.md), [follow-up v2](../../qa/rofan-archive-crosswalk-followup-v2-results.md), [known-model v1](../../qa/rofan-archive-crosswalk-known-model-results.md), [known-model v2](../../qa/rofan-archive-crosswalk-known-model-v2-results.md), [known-model v3](../../qa/rofan-archive-crosswalk-known-model-v3-results.md), and [known-model v4](../../qa/rofan-archive-crosswalk-known-model-v4-results.md). The initial five-call smoke remains [NOT PASS](../../qa/rofan-archive-crosswalk-smoke-results.md); none of these historical outcomes is rewritten.

### One-call prompt

> Using only the supplied current semantic source master, provisional cross-source craft catalog, selected source-specific semantic ledger and candidate-dispositions ledger, plus the listed current owner references/templates, produce exactly ONE bounded, evidence-grounded archive-craft crosswalk row. Use only the predeclared source/scene/shot/event and PTS assertions below; do not analyze all 44 sources or create additional findings. Link the source occurrence → source-local scene → shot interval → linked event and in-shot evidence → craft finding → story-neutral mechanism → applicable and avoid conditions → existing owner and exact target QA fields. Distinguish direct observation from `[INFERENCE]` and state an alternative. Report every unknown and the current global coverage status. Evaluate a candidate-versus-confirmed outcome only for the predeclared candidate records below. Do not inspect or claim to inspect original media, play footage, edit files, or infer source-wide prevalence. Do not copy source story, character identity, props, wardrobe, exact staging, shot sequence, or original timing into the transferable rule. Do not claim the selected source closes the archive.

### Required run context

For the new v3 run only, supply exactly these evidence sources and current package references (record original paths and hashes in run metadata). The v1/v2 contexts and scores remain historical and unchanged. For large JSON evidence files, provide bounded extracts of current status/gate fields and relevant rows; do not substitute stale snapshots:

- F: `videos/rofan-temporal-analysis/exhaustive/semantic/archive-normalized-master-in-progress.json`
- F: `videos/rofan-temporal-analysis/exhaustive/semantic/cross-source-craft-catalog-provisional-v1.json`
- F: `videos/rofan-temporal-analysis/exhaustive/semantic/reviewer-F/ea6a017b14fc647205b30ea896553c8e36e3abbc2983b73757a9c7cb282a8257-canonical-shot-scene-event-ledger.json`
- F: `videos/rofan-temporal-analysis/exhaustive/semantic/reviewer-F/ea6a-native-union/candidate-dispositions.json`
- F: `videos/rofan-temporal-analysis/exhaustive/semantic/archive-semantic-index.json` (resolve the current index through the master pointer and read `global_merge_gates`)
- `video-production-assets/references/25-reference-video-analysis.md`
- `video-production-assets/assets/archive-craft-crosswalk-template.md`
- `video-production-assets/assets/archive-audit-template.md`
- `video-production-assets/assets/shot-dna-template.md`
- `video-production-assets/references/06-shots.md`
- `video-production-assets/assets/06-shots-template.md`

The v3 extracts must include the selected source's exact master status and filename, the relevant CF-13 catalog entry, specified ledger and candidate records, plus the current semantic index `global_merge_gates`. Record exact source pointers. List every currently `OPEN` key and status exactly; 44/44 identities indexed is not closure. These are semantic artifacts; no original media/images in the model context.

### Predeclared evidence assertions (not a filled sample/output)

These assertions define the one row the grader will look for; they are not a generated result:

- **Occurrence/source:** `source_position_id=ea6a017b14fc647205b30ea896553c8e36e3abbc2983b73757a9c7cb282a8257`; SHA/archive ID `sha256:4831e753f691064aaa92b4b3748045b3fbef7d6dc76e0cfb21e37f1b7c4db195`; source video timebase `1/15360`. The exact filename is available in the selected source-status row and must be preserved there, not copied into the mechanism.
- **Scene/shot:** `scene_id=F-EA-SC01`; `shot_id=archive-shot:ea6a017b14fc647205b30ea896553c8e36e3abbc2983b73757a9c7cb282a8257:p0`; half-open shot range `[PTS 0, PTS 77824)` at `1/15360`. Last visible old-shot PTS is 77312; next shot begins at 77824.
- **Linked event and within-shot evidence:** `event_id=archive-event:ea6a017b14fc647205b30ea896553c8e36e3abbc2983b73757a9c7cb282a8257:p0:F01`. It is a multi-shot semantic event (time range 0–12.633333s; linked shots p0, p77824, p94208, p140288), so the row may claim only its bounded p0 in-shot portion. Shot `/shots/0/within_shot` records start PTS 0, an in-shot state PTS 39424, and end PTS 77312; cited dense states include PTS 3072, 9728, 35840, 39424, 42496, and 45568. Preserve the distinction between sampled state evidence and continuous motion.
**Candidate outcomes supported by the included disposition ledger:** `archive-event:ea6a017b14fc647205b30ea896553c8e36e3abbc2983b73757a9c7cb282a8257:77824` at PTS 77824 is `observed_hard_view_change`, supported by native neighbors 77312 / 77824 / 78336 and the linked shot endpoint/entry records; boundary is confirmed. Candidate `archive-event:ea6a017b14fc647205b30ea896553c8e36e3abbc2983b73757a9c7cb282a8257:78848` at PTS 78848 is `continuous_within_shot`, supported by neighbors 78336 / 78848 / 79360; it is not a cut. Do not generalize these outcomes beyond the selected evidence.
- **Craft reference:** provisional catalog finding `CF-13` links this occurrence and shot to a two-person shared-frame approach/response/contact/hold observation. A valid transfer must replace that scene-specific surface with a story-neutral mechanism, label function as `[INFERENCE]`, and retain an alternative (routine coverage or pose progression).
- **Transfer conditions:** applicability is a new brief whose action depends on the viewer reading two participants’ changing relation/response in the same view; avoid forcing a shared frame, contact beat, hold, or cut where the new brief does not need it or where evidence would not make it readable. Do not copy any source timing or staging.
- **Exact existing owner/QA fields:** route new shot planning to `06-shots.md` / `06-shots-template.md` with applicable existing target fields; for this shared-frame case include `shot_id`, `scene_id`, `beat_id`, `shot-local time (s or frames; FPS if frames)`, `인물 블로킹`, `시선/축`, `공개 정보`, `관점·감정/구도 의도`, `대안·채택/승인 상태`, and `종료 프레임`. Map `카메라 동작` only when the new brief makes it applicable; do not infer a source camera move. Separately represent each exact `shot-dna-template.md` `이전 체인` field: `레퍼런스 증거(관찰+위치)`, `메커니즘`, `의도 효과(해석)`, `새 브리프 제작 요구`, `정성 검증 기준`; do not invent a QA field.

- **Coverage status:** state the selected source's exact current master status and locator, exact filename in source provenance (not the mechanism), archive materialized/total and unmaterialized occurrence counts, and every current OPEN `global_merge_gates` key/status from the index referenced by the master. `source_occurrences_indexed=44/44` is not gate closure. Unknown status, counts, or gates remain `UNKNOWN`/`OPEN`; no full-rate playback/audio listening claim.

### Follow-up acceptance

One fresh stateless response passes only if it produces exactly one row traceable to predeclared IDs/locators and exact filename; preserves `[0,77824)` and both supported candidate outcomes without extra cuts; gives a story-neutral mechanism, inference alternative, applicability and avoid conditions; names exact owner/QA fields; separately represents all five Shot-DNA chain fields; and states selected-source status, materialization counts and every currently OPEN index gate accurately. Any omission is a miss. This frozen assertion set is for external grading only and must not be included as a rubric or plan in the model-call context.
 
### V3 one-call prompt (send only as the user task, with the evidence/package context above—not this plan)

> Using the current package and only the supplied bounded semantic evidence, produce exactly one actually filled archive-craft crosswalk row for the selected source/scene/shot/event, plus the two candidate disposition records. Preserve the exact source filename in source provenance and keep it out of the reusable mechanism. Use full verbatim IDs and source PTS/timebase. Include observed evidence, `[INFERENCE]` with an alternative, a story-neutral mechanism, transfer/avoid conditions, exact applicable receiving-owner fields and QA, and separately named/represented values for all five existing Shot-DNA `이전 체인` fields. Report the selected source's exact current master status and locator, archive materialized/total and unmaterialized counts, and each currently OPEN `global_merge_gates` key and status from the index reached through the master pointer. Treat 44/44 indexed identities as distinct from closure. State unknowns and evidence limits. Do not copy story, characters, setting, props, wardrobe, choreography, exact shot order, or source timing into the transferable rule. Do not analyze all 44 sources, inspect/play media, infer unknown statuses, or provide a method-only explanation; return the filled row and candidate records.

V3 model context must omit this plan, all rubrics/assertions, previous outputs and QA results. Include only the V3 prompt, current package files, and bounded extracts from the required master/catalog/selected source ledger/candidate dispositions/current semantic index.

### Actual v3 known-model run

One fresh stateless known-model skill-output call was completed after adding the semantic index to context. Runtime-advertised model identity: `openai-codex/gpt-6-luna`; the task-agent interface exposed no tier/effort suffix. The call had no plan/rubric/prior outputs in context. Manual grade: C1 PASS, C2 PASS, C3 PASS, C4 FAIL (`크기/카메라 위치` omitted from the otherwise detailed 06 map), C5 PASS (selected source status, counts, and all five OPEN index gates). Full raw output and context hashes are in [known-model v3 results](../../qa/rofan-archive-crosswalk-known-model-v3-results.md). Overall NOT PASS; do not mark the status/transfer contract complete.

### V4 prospective acceptance — separate from frozen v3 grade

The v3 result and its frozen rubric remain unchanged. V4 is a new prospective call against the updated current package, using the same bounded semantic evidence plus current semantic index and owner templates. Keep the plan, rubric, v3/v2/v1 outputs and result artifacts out of the model-call context.

V4 acceptance requires one real filled crosswalk handoff with exact source filename and full verbatim occurrence/scene/shot/event/candidate IDs; the predeclared half-open shot interval and two candidate disposition records; selected-source exact status and locator; materialized/unmaterialized counts and every current OPEN global gate; a story-neutral mechanism with inference alternative and transfer/avoid conditions; the complete applicable 06 receiving-owner map including `shot_id`, `scene_id`, `beat_id`, `shot-local time (s or frames; FPS if frames)`, applicable creative/QA fields, and specifically `크기/카메라 위치` for this shared-frame approach/response/contact-state case; and all five Shot-DNA `이전 체인` fields separately represented. Preserve unknowns and all source-modality limits. Any missing required item is a failure; do not infer a pass from a good partial row.

#### V4 one-call prompt

> Using only the current video-production skill package and the supplied bounded semantic source evidence (master, catalog, selected source ledger, candidate dispositions, and current semantic index), produce exactly one filled crosswalk finding and its two candidate disposition records. Preserve exact source filename and full IDs; report exact source status, materialization counts and all current OPEN global gates. Include the 06 shot-planning target identity/time fields and all applicable creative/QA fields, including `크기/카메라 위치` for this shared-frame finding. Separately represent each of the five existing Shot-DNA `이전 체인` fields. Use no source narrative in the reusable mechanism; state observed evidence, `[INFERENCE]` plus alternative, transfer/avoid conditions, and limits. Do not analyze all 44 sources.

#### V4 model context

Include only the current package files needed for the crosswalk and exact receiving-owner mapping plus bounded current extracts from the semantic master, provisional craft catalog, selected source-specific ledger, candidate dispositions and current semantic index. No prior outputs, plan, rubric, or media.

#### Actual V4 known-model run

One fresh stateless call completed against the updated package and bounded semantic evidence/index, without plan/rubric/prior-result context. Runtime identity: `openai-codex/gpt-6-luna`; no separate tier/effort suffix exposed. Manual V4 grade: all criteria PASS, including the exact `크기/카메라 위치` field, full IDs/filename, both candidate outcomes, selected status and gates, and all five Shot-DNA fields. Raw response, hashes, metadata and criterion grade are preserved in [known-model v4 results](../../qa/rofan-archive-crosswalk-known-model-v4-results.md). This does not change the separate v3 NOT PASS result.

### Separate unrelated baker baseline/with-skill comparison

The exact same unrelated 8-second baker prompt was answered once by `openai-codex/gpt-6-luna:medium` against the frozen baseline package (`C:/Users/Declan/AppData/Local/Temp/rofan-craft-final-stable-55mbkjjk/skills`) and once against the current working-tree package. Both actual plans honor the brief and avoid Rofan narrative/staging/timing. Neither consulted a casebank; the current-package answer also correctly omitted module 25 and the crosswalk. The complete plans, path lists and manual check are in [the comparison record](../../qa/rofan-unrelated-brief-baseline-with-skill.md). One sample per arm is descriptive, not causal/statistical evidence.

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
- The frozen T13–T20 suite remains only a saved-case retrieval/owner-field test, not an archive-wide synthesis or positive cross-domain skillification test. The separate smoke below covers generic owner use on unrelated briefs; it remains descriptive and does not establish source-derived prevalence or reliability.
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

## T19 combined owner-contract evaluation

Applied the approved existing-reference clarifications: `09-edit.md` distinguishes full 09 handoffs from scoped projections; the generic no-target saved-observation guidance requires a conditional concrete proposal while retaining source/audio unknowns; and `21-generated-video-qa-retry.md` requires separate planned last-picture and container-tail/duration checks in the existing 09 final-cut QA field. No product schema, frozen prompt, or rubric changed.

T19 used 15 fresh sequential stateless calls with the exact frozen matrix prompts, context-file lists/order, and two-LF content-only system assembly. The isolated root `C:\Users\Declan\AppData\Local\Temp\rofan-craft-t19-eval-clean\skills\video-production-assets` was copied from T18, then only those three references were replaced. Before calls, reconstructed context hashes matched all T17/T18 system SHA-256 values; all T19 context-file hashes matched the working-tree sources, and prompt hashes matched the frozen matrix. Model selection was `default`, resolved identity **UNKNOWN**. All 15 calls completed.

| Scenario | Final reviewed result |
|---|---|
| `reader07` | 3/5 full pass, 2 partial; both partials give generic transfer guidance without applying the bounded opening observation. All five preserve inaccessible-body and unlistened-audio limits. |
| `composite` | 0/5 full pass, 5 partial; active-only six-field cut tables 5/5, canonical elision rows 4/5, and two separate planned endpoint tasks in the existing final-cut QA field 0/5. All five honor the 12-second brief and preserve relevant unknowns/guards. One response lists two checks in QA prose but not in the required existing cut-row field. |
| `ordinary-loaded` | 5/5 full pass; no unrelated saved case was forced. |

Aggregate: **8/15 full pass, 7 partial, 0 not met, 0 guard failures**. The composite ending-check requirement remains unmet in all five outputs; most only mark both results UNKNOWN/pending, while one separately names checks outside the required existing cut-row QA field. The scoped 09 field projection was active-only in 5/5, while the canonical elision row appeared in 4/5. Reader retrieval remains variable. These descriptive results do not establish causality or statistical improvement. Raw outputs: `qa/rofan-craft-t19-reader07-raw.json`, `qa/rofan-craft-t19-composite-raw.json`, `qa/rofan-craft-t19-ordinary-loaded-raw.json`; per-response grade: `qa/rofan-craft-t19-microtest-grade.json`. Frozen matrix SHA-256: `7b8a251e8dc84fbaa4ce7f3fe85f7aef12da017fbcb4c54297235e12e098dff0`. No media generation, source playback, actual-media inspection, 3D/Blender, or endpoint checks were performed (**NOT RUN**).

## T20 casebank transfer and owner-slot evaluation

T20 evaluated the approved casebank-only clarification: mixed transfer/unknown requests now call for a retrieved bounded observation and locator, mechanism, explicit conditional new-scene proposal, and limits/QA; only source-fact/unknown-only requests skip proposals. Multi-owner ending guidance points to separate planned last-picture and container-tail/duration actions in the existing final 09 cut row's QA field. No schema, prompts, rubric, 09 reference, or 21 reference changed.

T20 used 15 fresh sequential stateless calls with the frozen matrix prompts, context-file lists/order, and two-LF content-only assembly. The distinct isolated root was `C:\Users\Declan\AppData\Local\Temp\rofan-craft-t20-final-clean\skills\video-production-assets`; only the casebank was replaced from the working tree. Installed casebank hash matched source (`20c7e02c4b9a332d2874c86cc663a97e5a441f2a78649f6ca6860f869a538642`); installed 09 and 21 hashes remained `f0e60126704540eb33158192dbf88fcb5409ebf2ae7a16e93d8fbad30cc46130` and `5dd6b01af3b504501e09578535b1fa36a406e78f320467ee7b918f28b981a2b1`. Raw metadata records the exact per-file, prompt, response, and system hashes; prompts and rubric matrix were unchanged. Model selection was `default`, resolved identity **UNKNOWN**. All 15 calls completed without errors.

| Scenario | Final reviewed result |
|---|---|
| `reader07` | 4/5 full pass, 1 partial. Raw response index 2 is a pass: it names and applies the bounded D797 title-to-live observation. Only index 4 is generic-only; all five preserve access/audio unknowns. |
| `composite` | 0/5 full pass, 5 partial. Run 1 leaves the specified singular attendant count TBD; run 2 explicitly elides but lacks a canonical elision row; run 3 uses a custom five-column cut table and omits the canonical row; run 4 lacks the canonical row and reports only UNKNOWN/pending without separate planned actions; run 5 wrongly makes the kiss-pair/woman identity continuity conditional. |
| `ordinary-loaded` | 5/5 full pass; no unrelated saved case was forced. |

Aggregate frozen-matrix result: **9/15 full pass, 6 partial, 0 not met, 0 guard failures**. Under matrix line 68, separate endpoint actions are planned somewhere in 4/5 composite outputs (runs 1, 2, 3, 5); run 4 supplies only UNKNOWN/pending status. Secondary owner-placement metrics, not part of that frozen-matrix criterion: active-only cut fields 4/5; canonical elision rows 2/5 (runs 1 and 5); endpoint pair in the final 09 QA field 3/5 (runs 1, 2, 5). This separates semantic endpoint planning from the stricter 09-slot contract. These descriptive results do not establish causality or statistical improvement. Raw outputs: `qa/rofan-craft-t20-reader07-raw.json`, `qa/rofan-craft-t20-composite-raw.json`, `qa/rofan-craft-t20-ordinary-loaded-raw.json`; corrected per-response grade: `qa/rofan-craft-t20-microtest-grade.json`. Frozen matrix SHA-256: `7b8a251e8dc84fbaa4ce7f3fe85f7aef12da017fbcb4c54297235e12e098dff0`.
## Separate cross-domain owner-procedure smoke (not part of T13–T20)

Matrix: [`qa/cross-domain-craft-transfer-smoke-matrix.json`](../../qa/cross-domain-craft-transfer-smoke-matrix.json). Full prompts, per-context/system/prompt/response hashes, all five exact outputs and manual results: [`qa/cross-domain-craft-transfer-smoke-results.md`](../../qa/cross-domain-craft-transfer-smoke-results.md).

Five independent fresh stateless `default` calls completed with no retry or recorded error. Four unrelated positive contexts omitted the Rofan casebank; only the baker negative control included it. Predeclared scenario criteria: **5/5 pass**. Camera/action timing, approach/deceleration/stop/settle with cropped-foot unknowns, progressive nonverbal held-beat cues, 45-second edit/elision, and ordinary-brief skip were observed in the outputs.

Secondary format observation: the edit/elision answer included inactive full-template 09 columns despite a concise scoped request; it passes the smoke's predeclared semantic criteria but not the current 09 active-field projection contract. This is recorded rather than silently grading the matrix after the calls. The smoke uses fictional briefs and current generic owner guidance only; it is not archive analysis and does not validate Rofan-derived craft.
## Sixth cross-domain lighting-owner smoke (not part of T13–T20)

The original five-scenario smoke results above remain unchanged. The matrix now contains those five scenarios plus one unrelated positive lighting scenario; this is one new fresh stateless call, not a regrade or rerun of prior outputs. The bounded source basis is casebank L03: `430` at approximately 65.532–76.943s and `d31` at 2101.599/2101.683s record gradual brightness/flare over held geometry, with no cut established. This supports conditional planning only and no archive-wide prevalence claim.

The 07 owner now asks for proposed shot-local start/change/settle/hold cues and information reveal when the brief requires an in-shot light change; preserve framing/geometric anchors, distinguish lighting from camera/edit changes absent evidence, avoid inferring equipment/exposure/focus, and use existing 07 fields. The template/schema and `21` technical media-QA owner were not changed.

One fresh `default` stateless call completed without retry/error. Result: **1/1 scenario PASS** against the four predeclared lighting acceptance criteria. Exact prompt, context-file hashes, combined system hash, full output, and manual criterion grade are appended to the [smoke results](../../qa/cross-domain-craft-transfer-smoke-results.md). This is a scenario smoke only, not source-derived prevalence, reliability, or a causal claim.
