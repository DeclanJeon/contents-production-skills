# Prospective archive crosswalk smoke — results

Date: 2026-10-13. Source evidence root: `F:\Resources\AI-Rofan-Drama-2026-10-11`. No original media playback/full decode, API calls, generation, upload, Blender/3D, or source-root writes were performed. The `default` completion helper exposed the requested model but not provider resolution; resolved model is recorded as `UNKNOWN`, not inferred. Each response was a fresh stateless call.

## Exact model context and hashes

The five package files below were supplied as the complete current package context to every scenario, including both negative controls. Context order: SKILL, module 25, archive audit template, shot DNA template, archive crosswalk template.

| Context file | SHA-256 |
|---|---|
| `C:\Users\Declan\documents\Projects\contents-production-skills\video-production-assets\SKILL.md` | `c400ac9192be3b9783b131a1e4f1574e4aa9c8027cdfe160fa350cd35aafdcca` |
| `C:\Users\Declan\documents\Projects\contents-production-skills\video-production-assets\references\25-reference-video-analysis.md` | `41dc63ea90c0a3523128fb04a10368537418bfc7eb66ac1f07b3df99bb4194dc` |
| `C:\Users\Declan\documents\Projects\contents-production-skills\video-production-assets\assets\archive-audit-template.md` | `333e6f844ac79878b7a948761abc19c50dc57d0ee38d105bc3a50f5b1c15e487` |
| `C:\Users\Declan\documents\Projects\contents-production-skills\video-production-assets\assets\shot-dna-template.md` | `5dbc0b305ad97da240baf19cf92db5962fd1824b48448a73f57fc0600f9ab3fa` |
| `C:\Users\Declan\documents\Projects\contents-production-skills\video-production-assets\assets\archive-craft-crosswalk-template.md` | `5a1b41737e7f34b95ca3811b01fc8591de8977a1af27f1b9b3e1befeac9b5cf7` |

The four F: source-evidence files supplied in each EXH call (not included in negative controls):

| Evidence file | SHA-256 |
|---|---|
| `F:\Resources\AI-Rofan-Drama-2026-10-11\videos\rofan-temporal-analysis\exhaustive\collection\archive-source-identity-inventory.json` | `2ad24ee5f26b742681e8c971703ebd6a1a786bf222b18d496bfb518345267edc` |
| `F:\Resources\AI-Rofan-Drama-2026-10-11\videos\rofan-temporal-analysis\exhaustive\collection\archive-run-winget-9.0.2-20261011-43f41\full_archive_manifest.json` | `8ea500018601de079a82bf162ea1de573bf5873198557387f80a97575922c426` |
| `F:\Resources\AI-Rofan-Drama-2026-10-11\videos\rofan-temporal-analysis\exhaustive\collection\archive-run-winget-9.0.2-20261011-43f41\full_archive_summary.json` | `437b3d48502f425d05ababb35bd392d1fc2b9e639365dc4b8fae0e1f7607bf23` |
| `F:\Resources\AI-Rofan-Drama-2026-10-11\videos\rofan-temporal-analysis\dense-review\manual_review.json` | `28c169c62f8a9884c22cace586c5af3d87ecf5738de56abfe11f2547bdaa64a2` |

Evidence was manifest/ledger/identity metadata only. Inventory reports 44 expected/observed occurrences and complete identity hashes. The temporal run is failed: 1 complete, 43 failed; full-source PTS coverage false. Ledger reports 6,002 selected candidates (not all visually reviewed), 335 sampled 1.2-second intervals at 5 fps/6 frames around only the first eight retained locator PTS per source, and no full-video visual coverage. These are source-file reports, not independently verified footage facts. No audio listening or original media access occurred in this run. Embedded legacy C: paths in source metadata were not used.

## Scenario protocol and scoring

Exact exhaustive prompt used, independently in EXH-1 through EXH-5:

> A user asks for an exhaustive all-44 source/shot craft analysis and how transferable craft should be represented for future skill use, explicitly not copying plot, characters, or props. Ask for the proposed analysis artifacts and owner transfer path. Respond to that user with a concrete useful artifact proposal and transfer path. Distinguish source facts, estimates, candidates, and unknowns. Evaluate whether existing evidence supports an exhaustive analysis; state source gates accurately. Do not analyze all 44 individual videos. Do not inspect or claim to inspect original media. No edits, generation, upload, API, or 3D. Keep the response concise and actionable.

Requested model for all seven calls: `default`. Resolved model: `UNKNOWN` (helper did not report it). All calls returned completed; errors: none.

§26 criterion interpretation: (1) must materialize a retrievable occurrence→sequence/scene→shot→within-shot-event crosswalk, not merely promise/design its fields; (2) must connect located evidence to a general mechanism, named existing owner, and target-specific QA field/check; (3) explicitly keep candidates separate from confirmed cuts; (4) state incomplete source coverage; (5) make no claim of audio listening or full-motion playback when absent. `FAIL` means the criterion is not complete from the answer, even if it describes the intended future artifact. `PARTIAL` is not a pass.

| Call | C1 retrievable crosswalk | C2 evidence→mechanism→owner→QA | C3 candidates vs confirmed cuts | C4 source gates | C5 playback/audio claims | Result |
|---|---|---|---|---|---|---|
| EXH-1 | FAIL — proposed schema/hierarchy, no retrievable joined rows | FAIL — proposed owner routing, no finding with exact QA slot | FAIL — says samples do not become verified cuts but no candidate/cut disposition rows | PASS | PASS | NOT PASS |
| EXH-2 | FAIL — proposes artifact, no source/scene/shot/event crosswalk rows | FAIL — general mechanisms and routing, no exact evidence locator→owner QA linkage | FAIL — no cut-candidate/confirmed-cut disposition | PASS | PASS | NOT PASS |
| EXH-3 | FAIL — describes exact joins without materializing retrievable row(s) | PARTIAL — complete conceptual chain but no populated located finding or exact QA field/check | PASS — explicitly says locator timestamps are candidates and cuts require evidence on both sides | PASS | PASS | NOT PASS |
| EXH-4 | FAIL — hierarchy described, no row-based crosswalk | FAIL — general transfer chain/routing, no exact QA field/check attached to evidence | FAIL — warns detections are candidates, but no separated candidate/cut table | PASS | PASS | NOT PASS |
| EXH-5 | FAIL — schema proposed, no retrievable source-linked crosswalk rows | FAIL — transfer path stated but no populated locator-to-exact-QA link | FAIL — distinguishes categories in Shot DNA but no cut dispositions | PASS | PASS | NOT PASS |

The C3 FAIL calls are strict to the explicit table/record criterion; answers correctly warn that locator detections are candidates. No answer explicitly counted 44 occurrences as 44 independent craft cases. C4/C5 pass because the answers accurately acknowledge partial coverage and do not claim listening/full-media playback.

## Full raw exhaustive outputs

### EXH-1

```text
## Proposed analysis artifacts

For the requested exhaustive all-source/all-shot and cross-source craft analysis, I would deliver:

1. **Archive audit** (`archive-audit-template.md`): a 44-source inventory and coverage ledger, with each occurrence’s supplied `source_position_id`, `archive_id`, exact filename, and separate status for decode, locator, extraction, visual review, playback, and audio listening.
2. **Source-level Shot DNA reports** (`shot-dna-template.md`): one report per source, populated only where evidence supports an observation. These would preserve source-local locators and PTS; they would not turn sample timestamps into verified cuts or project shot IDs.
3. **Relational craft crosswalk** (`archive-craft-crosswalk-template.md`): required for this explicit exhaustive request. It would link source occurrence → sequence/scene → shot/boundary → within-shot event → transferable finding → existing owner procedure and observable QA check. Unresolved joins and gates would remain open, not be counted as “no findings.”
4. **A concise findings and owner-handoff summary**: only abstracted, story-neutral mechanisms, with transfer conditions, counterconditions, evidence locations, and limits.

The findings would exclude plot, characters, props, wardrobe, distinctive designs, original choreography or shot order, and source-specific absolute timing. A plan or text report would not be presented as proof of generated-media quality.

## Evidence status and feasibility

The supplied metadata identifies **44 occurrences**, reports complete hashes, and says the source IDs match across the inventory and run manifest. But the temporal collection run is **failed**: only **1 of 44** entries is reported complete, and full-source PTS coverage is not present for every entry.

The separate manual-review ledger reports 44 files, 6,002 selected frame candidates (not all visually reviewed), and 335 sampled intervals around only the first eight retained locator PTS per source. Those strips are not full temporal coverage or continuous playback; no audio was listened to. The current evidence therefore **does not support an exhaustive all-44 all-shot craft analysis**. I have not inspected or played the original media, and would not claim otherwise.

## Owner transfer path

For each supported finding, the crosswalk should point to an **existing** owner and its existing QA fields—not create a parallel generic rule set. Likely destinations depend on what the media evidence actually supports:

- **Shot structure, staging, spatial continuity:** `06-shots`; use `$camera-spatial-design` only if a new brief needs numeric camera/spatial design.
- **Edit rhythm and reveal order:** `09-edit`.
- **Performance and reaction:** `04-performance`.
- **Visual language and continuity:** `05-visual` / `20-visual-mode-ssot`.
- **Motion, compositing, and generated-media checks:** `21-generated-video-qa-retry`.
- **Evidence, captions, or production claims:** `10-evidence`, where applicable.

No owner update should be made from the present partial evidence. First close the source-specific coverage gaps; then compare each supported transferable mechanism against the owner’s actual procedure, template fields, and QA criteria. Only a demonstrated general procedure or QA gap should be proposed for a minimal update to that owner.
```

### EXH-2

```text
## Proposed analysis artifacts

1. **`archive-audit.md`** — inventory and coverage ledger for all 44 source occurrences, using the supplied stable `source_position_id`, `archive_id` and exact filename. It will distinguish ledger-reported collection from media actually inspected.
2. **`archive-craft-crosswalk.md`** — required for this explicitly exhaustive all-source/all-shot request. It will map source occurrences to scenes, shot boundaries, within-shot events, craft findings and existing owner procedures. Unresolved rows and gates will remain explicit; missing evidence will not be counted as “no findings.”
3. **Linked Shot DNA reports** — only for observations supported by available evidence. The supplied excerpts do not include enough per-source observations to populate a defensible all-shot breakdown.

## Evidence status and feasibility

The supplied inventory reports **44 expected and observed occurrences**, complete hashes, and 44 completed identity entries. That establishes the inventory’s reported source identities—not visual analysis.

The temporal collection run is **failed**: 44 sources are listed, but only **1** is reported complete and **43 failed**; full-source PTS coverage is not present for every entry. The manual-review excerpt reports 6,002 selected frame candidates, of which **not all were visually reviewed**, and retains only the first eight scene-locator PTS per source. It also reports 335 sampled intervals around those retained PTS—not full temporal coverage. No audio was listened to. These are ledger-reported facts, not results I independently verified against media.

Accordingly, the supplied evidence **does not support an exhaustive all-44-source/all-shot craft analysis**. I have not inspected or played any original media. A crosswalk can be prepared as a **partial evidence-and-gates artifact**, but its archive-completion status must remain **NOT ESTABLISHED**. Cut boundaries, motion timing, scene membership bounds and audio observations are unknown unless supported by additional evidence.

## Transfer path for future skill use

Represent transferable craft as **source evidence → labelled interpretation → story-neutral mechanism → transfer conditions → existing owner procedure and QA check**. Keep plots, characters, props, distinctive designs, choreography and original timing out of the reusable rule.

Route supported findings to existing owners rather than creating a parallel rule set: editing/reveal order to **09**, blocking and shot design to **06**, performance to **04**, visual/continuity issues to **20/26**, motion and compositing QA to **21**, and claims/provenance or finishing to **10/24/23**, as applicable. Any future skill update should be limited to a demonstrated gap in the relevant owner’s existing procedure and QA—not inferred from incomplete coverage.

**Next step:** provide accessible source media or a complete, source-linked evidence ledger with the required per-source coverage. Until then, proceed only with the partial inventory, crosswalk scaffold and explicit open gates; no media edits, generation, upload, API use or 3D work are proposed.
```

### EXH-3

```text
## Recommended artifacts

1. **Archive audit** (`archive-audit-template.md`) — inventory and evidence coverage for all 44 source occurrences, with each coverage mode reported separately: decode, locator, extraction, visual review, continuous playback, and audio listening.
2. **Archive craft crosswalk** (`archive-craft-crosswalk-template.md`) — the required relational artifact for this explicit all-source/all-shot request. It should join each source occurrence to supported sequence/scene membership, shot boundaries, within-shot events, transferable findings, existing owners, and observable QA checks. Keep unresolved rows and gates explicit.
3. **Shot DNA records** (`shot-dna-template.md`) — source-specific observations linked from the audit/crosswalk, limited to evidence actually reviewed.

Keep findings story-neutral: describe mechanisms and their transfer conditions, not source plots, characters, props, distinctive designs, choreography, or original shot order/timing.

## Evidence status and feasibility

The supplied **identity inventory** reports 44 expected and observed occurrences, complete hashes, and 44 completed identity records. That establishes an inventory in the supplied ledger—not media inspection or shot coverage.

The temporal collection run is marked **failed**: 44 sources are listed, but only 1 is complete and 43 failed; full-source PTS coverage is not present for every entry. The manual-review ledger reports 6,002 selected frame candidates, of which not all were visually reviewed; only the first eight retained locator PTS per source were kept. It also reports 335 sampled intervals around those locators, not full-video visual coverage. No audio was listened to. The current evidence therefore **does not support an exhaustive all-44-source/all-shot craft analysis**.

In particular:
- Locator timestamps/candidates are not confirmed cuts. A cut needs evidence on both sides; otherwise retain `DETECTOR_CANDIDATE`, `ESTIMATED`, or `UNKNOWN`.
- Sampled strips can support limited observations of visible states/order, but not continuous motion, precise action timing, or whether a framing shift was a camera move versus an edit.
- Missing or unreviewed material is an **open gate**, not evidence that a craft pattern is absent.

I have not inspected original media. The proposal below is based only on the supplied metadata and ledger excerpts; I have not performed media review or modified any files.

## Transfer path for future skill use

For each adequately supported finding, record the chain **source locator → observed craft mechanism → labeled interpretation and alternative → transfer conditions/avoid conditions → existing owner procedure and exact QA field → target-specific observable acceptance check**. Then route it to the owner already responsible for that craft—for example, editing to **09**, shots/blocking to **06**, performance to **04**, evidence/claims to **10**, or generated-motion QA to **21**, as applicable. Do not create a duplicate rule or new schema just to store a finding.

Only propose a skill update if you explicitly request **skillification**. If requested, first close or clearly bound the evidence and compare each proposed finding against the relevant owner’s existing procedure, template fields, and QA criteria. Update only a demonstrated gap in that existing owner; otherwise report the finding as already covered, partial, unsupported, or blocked.
```

### EXH-4

```text
## Proposed analysis artifacts

1. **`archive-audit.md`** — inventory and coverage ledger for all 44 sources, using the supplied stable `archive_id`, exact filename, and source hash. It will distinguish what was inventoried, decoded, sampled, visually reviewed, played continuously, and listened to.
2. **Per-source Shot DNA reports** — one report per source, limited to directly supported observations. Each entry will label evidence as **observed**, **estimated**, **detector candidate**, or **unknown** and retain source-local PTS/locators where available.
3. **`archive-craft-crosswalk.md`** — the required relational artifact for this explicitly exhaustive request: source occurrence → sequence/scene → shot boundary → within-shot event → transferable finding → existing owner procedure and observable QA check. Missing rows and unresolved gates will remain explicit; they will not be treated as zero findings.
4. **A concise findings and handoff summary** — only patterns supported by inspected evidence, with counterexamples, coverage limits, and the destination owner procedure for each proposed transferable mechanism.

## Evidence status and feasibility

The supplied records establish an inventory of **44 sources with complete hashes**. They do **not** establish an exhaustive all-source/all-shot analysis: the full-run manifest is marked **failed**; the summary reports **1 complete and 43 failed**, and full-source PTS coverage is not present for every entry. The separate review ledger reports 335 sampled intervals around only the first eight retained locator PTS per source, not full-video coverage. Of 6,002 selected frame candidates, not all received visual review. No audio was listened to.

I will treat locator detections as **candidates**, not verified cuts; sampled frames as evidence only for the sampled moments; and uninspected boundaries, motion, audio, and source coverage as **unknown**. The records supplied here are metadata/ledger excerpts only. I have not inspected or played the original media, so I cannot complete or claim the requested exhaustive craft analysis from this evidence.

## Transfer path for future skill use

Represent each transferable craft point as a **source-grounded, story-neutral finding** in the crosswalk: evidence locator → mechanism → conditions for transfer and avoidance → existing owner procedure → target-specific observable QA check. Keep plot, characters, props, distinctive designs, choreography, and original timing out of the transferable rule.

Route findings to existing owners rather than creating a parallel rulebook: for example, edit/publication order to **09 Edit**, performance to **04 Performance**, shot/blocking and spatial staging to **06 Shots** and the relevant camera specialist, and claims/provenance to **10 Evidence** or **24 Production Execution**, as applicable. A finding should point to the owner’s actual procedure and QA field. Any change to skill files should be a separate, explicit skillification step backed by completed source review and a demonstrated gap; this proposal itself does not modify skills.

**Next gate:** provide accessible original media and the source-local locator/scene records needed to review it. Until then, the artifacts can document inventory, reported sampling, and open gates—but not exhaustive findings.
```

### EXH-5

```text
## Proposed analysis artifacts

For an explicitly exhaustive all-source/all-shot craft analysis, use these three linked, read-only artifacts:

1. **Archive audit** (`archive-audit-template.md`) — inventory and per-source coverage ledger. Keep decode, locator candidates, extracted stills, visual review, continuous playback, and audio listening as separate coverage modes.
2. **Shot DNA reports** (`shot-dna-template.md`) — observed beats and production traits for each source, with source-local locators and clear `OBSERVED`, `ESTIMATED`, `DETECTOR_CANDIDATE`, or `UNKNOWN` status.
3. **Archive craft crosswalk** (`archive-craft-crosswalk-template.md`) — the required relational join for this request: source occurrence → sequence/scene → shot/boundary → within-shot event → transferable finding → existing owner procedure and observable QA check. Keep open gates explicit; missing evidence is not a zero finding.

Use the supplied `source_position_id`, `archive_id`, SHA-256 values, and exact filenames verbatim. Keep source-local IDs separate from project IDs.

## What the supplied evidence supports

The excerpts report **44 expected and observed source occurrences**, with complete hashes in the identity inventory. They do **not** establish exhaustive shot analysis:

- The full-run manifest is marked **failed**. Its summary reports full-source PTS coverage for only **1 of 44** entries; **43 failed**.
- The automated scan selected **6,002 frame candidates**, but they were not all visually reviewed. Only the first eight retained scene-locator PTS per source are noted.
- Manual review sampled **335 intervals** around those retained locator points; the excerpts explicitly say this is not full-video visual coverage or an exhaustive all-shot sample.
- Continuous playback and audio listening were not performed. The excerpts also say no original-media playback or full decode was run during this evaluation.

Accordingly, the exhaustive analysis is **not established by the available evidence**. Treat detector/locator outputs as candidates, sampled frames as limited observations, and unreviewed boundaries, motion, audio, and source coverage as unknown—not as confirmed cuts, craft findings, or absence of findings. The 44-source inventory is supported by the supplied metadata; it is not proof of 44-source shot coverage.

## Transfer path for future skill use

Represent each transferable craft point as an **evidence-linked finding** in the crosswalk: source locator and observation → clearly labelled inference (including a plausible alternative) → story-neutral mechanism → conditions to transfer or avoid → existing owner procedure and its exact QA slot → target-specific observable check. Keep plot, characters, props, distinctive designs, choreography, shot order, and original absolute timing out of the transferred mechanism.

Route only supported findings to existing owners—for example, edit/publication-order findings to **09 Edit**, blocking or framing findings to **06 Shots** (and camera-spatial design if numerical spatial work is needed), performance findings to **04 Performance**, product/state findings to **19/26**, and claims/provenance findings to **10/24**. Use the owner’s actual template fields and QA criteria; do not create a parallel rulebook or infer a skill gap from missing keywords.

This is a proposal for how to document and route findings, **not a claim that the analysis has been completed or that any skill files have been changed**. No original media was inspected for this response.
```

## Negative controls

Both controls used only the same five package files listed above, no F: evidence, no rubrics in the call context. Fresh stateless calls, requested model `default`, resolved model `UNKNOWN`, completed, no errors.

### NEG-SINGLE exact prompt

> I have one short reference clip. My only source note is: a person pauses at a doorway, then turns toward a bright window. I have no exact timecodes, continuous-playback notes, or audio notes. Give me a lightweight, source-grounded analysis of what craft mechanism might transfer to a new scene, what remains unknown, and which existing owner field should receive it. Do not treat this as an archive or cross-source request; do not ask for exhaustive coverage.

Forced archive crosswalk/casebank: **No.** Output is a small single-reference mechanism proposal with evidence limits and `06-shots` blocking/action field handoff.

```text
## Lightweight reference analysis

**Evidence basis:** Your supplied note only: “a person pauses at a doorway, then turns toward a bright window.” I have not inspected the clip. This is a user-provided observation, not a verified shot breakdown.

### Possible transferable mechanism
A **pause at a threshold followed by a turn toward a strong visual cue** may create a small beat of hesitation, then redirect the viewer’s attention. The window’s brightness could help motivate or clarify that redirection, but its intended meaning or effect cannot be established from the note alone.

**Transfer to a new scene:** Consider a brief pause at a meaningful boundary, followed by a motivated turn toward a clear visual target. Adapt the setting, action, and motivation to the new scene rather than copying the reference’s specific staging.

### Unknown
- Exact timing, duration of the pause, and turn speed  
- Shot size, camera angle or movement, and whether this is one shot or multiple  
- Whether the person turns their head, gaze, torso, or whole body—and what happens afterward  
- How bright the window appears in the image, and whether the light changes the person or space  
- Cut points, sound, performance nuance, and the effect across continuous playback  
- Any broader scene context or intended interpretation  

### Existing owner handoff
**Owner:** `06-shots` — the shot/blocking plan.  
**Field to use:** the existing **blocking/action** field for the pause and turn; note the window as the visual target or spatial anchor where that field supports it. Exact timing and camera choices should remain unspecified until supported by the new scene’s plan. No project or shot ID is assigned here.
```

### NEG-UNRELATED exact prompt

> Write a concise 3-beat original creative brief for a 10-second whimsical animated scene about a paper boat navigating a puddle. Include one emotional turn and a simple ending. Do not refer to any source video, archive, existing craft case, or skill update.

Forced crosswalk/casebank: **No.** Output is an original three-beat brief, with no archive/casebank/source-derived rule.

```text
## Creative Brief — *The Little Crossing*

**Format:** 10-second whimsical animation  
**Premise:** A folded paper boat sets out across a rain puddle, only to discover the journey is bigger—and wobblier—than it expected.  
**Emotional turn:** Nervousness gives way to confidence.  
**Tone:** Gentle, playful, quietly triumphant.

### Three beats
1. **Set sail — 0:00–0:03**  
   A tiny paper boat drifts from the puddle’s edge. A breeze nudges it toward a floating leaf; it wobbles but keeps going.

2. **The wobble — 0:03–0:07**  
   A ripple lifts the boat’s bow. It tips, catches itself, and briefly seems ready to give up—then steadies as the leaf passes beside it like a friendly escort.

3. **A small arrival — 0:07–0:10**  
   The boat glides to a dry little island of pavement. It settles upright. One raindrop lands beside it, making a tiny ripple; the boat bobs once, proudly.

**Ending:** A simple, wordless moment of arrival and earned confidence.
```

## Required repository checks

Exact commands and outputs:

```text
> python scripts/check_versions.py
version check OK: package 2.5, 23 skill(s) consistent

> python -X utf8 -m pytest -q
.........s........................................... [ 20%]
............................................................ [ 43%]
...................................................... [ 64%]
.................................................................... [ 90%]
........................                             [100%]
============================== warnings summary ===============================
scripts/test_sync_installed.py::test_stale_link_is_repointed
  C:\Users\Declan\AppData\Local\Programs\Python\Python312\Lib\site-packages\_pytest\threadexception.py:58: PytestUnhandledThreadExceptionWarning: Exception in thread Thread-13 (_readerthread)
  Traceback (most recent call last):
    File "C:\Users\Declan\AppData\Local\Programs\Python\Python312\Lib\threading.py", line 1075, in _bootstrap_inner
      self.run()
    File "C:\Users\Declan\AppData\Local\Programs\Python\Python312\Lib\threading.py", line 1012, in run
      self._target(*self._args, **self._kwargs)
    File "C:\Users\Declan\AppData\Local\Programs\Python\Python312\Lib\subprocess.py", line 1599, in _readerthread
      buffer.append(fh.read())
                    ^^^^^^^^^
    File "<frozen codecs>", line 322, in decode
  UnicodeDecodeError: 'utf-8' codec can't decode byte 0xbf in position 215: invalid start byte
  Enable tracemalloc to get traceback where the object was allocated.
  See https://docs.pytest.org/en/stable/how-to/capture-warnings.html for more info.
    warnings.warn(pytest.PytestUnhandledThreadExceptionWarning(msg))

scripts/test_sync_installed.py::test_remove_link_never_deletes_target_content
  C:\Users\Declan\AppData\Local\Programs\Python\Python312\Lib\site-packages\_pytest\threadexception.py:58: PytestUnhandledThreadExceptionWarning: Exception in thread Thread-17 (_readerthread)
  Traceback (most recent call last):
    File "C:\Users\Declan\AppData\Local\Programs\Python\Python312\Lib\threading.py", line 1075, in _bootstrap_inner
      self.run()
    File "C:\Users\Declan\AppData\Local\Programs\Python\Python312\Lib\threading.py", line 1012, in _bootstrap_inner
      self._target(*self._args, **self._kwargs)
    File "C:\Users\Declan\AppData\Local\Programs\Python\Python312\Lib\subprocess.py", line 1599, in _readerthread
      buffer.append(fh.read())
                    ^^^^^^^^^
    File "<frozen codecs>", line 322, in decode
  UnicodeDecodeError: 'utf-8' codec can't decode byte 0xbf in position 224: invalid start byte
  Enable tracemalloc to get traceback where the object was allocated. For more info, see https://docs.pytest.org/en/stable/how-to/capture-warnings.html#resource-warnings
    warnings.warn(pytest.PytestUnhandledThreadExceptionWarning(msg))

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
258 passed, 1 skipped, 2 warnings, 217 subtests passed in 30.55s
```

Skip identity (located from test source): `blender-previsualization/scripts/test_camera_orientation_in_blender.py::CameraOrientationTests`, guarded by `@unittest.skipUnless(BLENDER, "set BLENDER_EXECUTABLE or put blender on PATH")`. The `-q` run did not print skip reason; source guard identifies the conditional.

### Isolated package install/link smoke

Attempted `python -X utf8 scripts/install_package.py --repo-root . --skills-root C:\Users\Declan\AppData\Local\Temp\rofan-archive-crosswalk-smoke-20261013-1640`. It exited 2 at preflight, before any write. Exact output:

```text
installation preflight failed; nothing was written:
  - skills root overlaps the repository source root: C:\Users\Declan\Documents\Projects\contents-production-skills\UsersDeclanAppDataLocalTemprofan-archive-crosswalk-smoke-20261013-1640 vs C:\Users\Declan\Documents\Projects\contents-production-skills
  - source skill would create a support collision: C:\Users\Declan\Documents\Projects\contents-production-skills\video-production-assets\support\manifest.json
  - source skill would create a support collision: C:\Users\Declan\Documents\Projects\contents-production-skills\video-production-assets\support\examples
  - source skill would create a support collision: C:\Users\Declan\Documents\Projects\contents-production-skills\video-production-assets\support\qa
  - source skill would create a support collision: C:\Users\Declan\Documents\Projects\contents-production-skills\video-production-assets\support\CHANGELOG.md
```

This repository/shell combination did not provide a safe direct isolated install route using the current checkout; no global root or F: source was changed. No second workaround/snapshot installer was attempted.

## Outcome

The skill did **not** pass the prospective smoke. All five exhaustive calls failed the concrete retrievable-crosswalk criterion; criterion 2 also failed or remained partial because the proposed answers do not materialize an evidence-located mechanism-to-exact-owner-QA record. This is an observed evaluation outcome, not a skill edit request; no skill wording or source evidence was modified. The positive responses accurately avoid claiming analysis of all 44 source videos. The five identity hashes/inventory counts are not evidence that all 44 videos were analyzed.
