# Continuity entrypoint release verification

## Scope

Related sequence/AV execution implementation plus mandatory continuity navigation in production-assets, standalone Higgsfield generation, replication and explainer entrypoints. Unrelated routing edits, artifact QA data and analysis materials are excluded from the release index.

## Observed checks

- Initial existing storyline/AV tests: 53 passed.
- Added entrypoint regressions: 8 failed / 8 passed before guidance changes; 16 passed afterward. These are structural/discoverability checks, not semantic vision or behavior proof.
- A fresh-context read-only baseline application probe read the replication entrypoint and its normal references. For a new-angle continuation and return after an insert, it explicitly permitted submission without accepted predecessor media in native references when no frame-chaining anchor was assigned. This demonstrated the navigation/concurrency loophole; a single probe is not a statistical compliance measurement.
- Removed the raw-tail extraction recipe from replication guidance and distinguished same-angle accepted out−1 anchors from new-angle approved composition.
- Full original working tree: 1039 passed, 4 skipped, 533 subtests (67.81s). This includes unrelated dirty routing tests, so it is not the release-only result.
- Exact index-only export, without excluded dirty/untracked files: 1027 passed, 6 skipped, 533 subtests (67.45s). Two additional skips concern Git integrity checks in an export without `.git`; the actual repository run includes them.
- First `/tmp` export test run ended with `OSError: [Errno 122] Disk quota exceeded` during pytest session finish; it is not counted as passing. Re-exporting the same index on the home filesystem with a dedicated test temporary directory passed. Only this session's generated temporary files were cleaned.
- Version checker: package 2.54, all 25 skills consistent. `git diff --cached --check` passed. Five sequence CLI entrypoints loaded with `--help`.
- Installed skill synchronization dry-run: 100 correct links (25 skills x Codex, Claude, shared agents, Pi), zero creations, repoints or displacements.
- Explicit realpath and SHA256 comparisons for seven updated entrypoint/reference/helper paths in each of four roots matched the repository source.

## Limits

No paid jobs, uploads, new provider requests, visual playback/listening acceptance, or model-conditioning guarantees are part of this verification. Native reference preparation and actual-call audit validate declared snapshots, file hashes and the supplied client-call record; they are not a global MCP interceptor and do not authenticate agent observations. Unsupported or unregistered native transports block dependent submissions rather than falling back silently. Existing local symlinks expose the working source immediately, including unrelated edits still present locally; release-only correctness is checked separately in the index export.

## Independent review and verified fix pass

The fresh reviewer applied the new-angle/insert scenario and required the accepted predecessor/history and native selected references, unlike the baseline probe. It found three release blockers in the adopted code, not in the intended entrypoint wording:

1. Historical shots were declared but only adjacent predecessor bindings/inspection were enforced. A valid three-shot, image-backed return-after-insert fixture demonstrated missing native history bindings, missing historical playback/listening and a self-history bypass. Four negative cases failed before the fix, while the complete fixture passed. Shared historical-cut resolution now feeds source inspection and native AV handoff; all 30 handoff tests passed afterward.
2. Incomplete explicit readiness descriptors could compare missing state fields as `None == None`, and missing asset fields disabled correlation. Nine new descriptor negatives reproduced the incomplete-contract behavior. Complete nonempty readiness/asset configuration is now mandatory, with existing pending-state and wrong-upload checks retained.
3. External audio could render without a projection version/hash pin. The missing-pin render test reproduced this; every external track now requires the current pin before creating output. Transport and real-media tests: 31 passed after those fixes.

Review was read-only; its assertions about actual Git push and installed hashes were deliberately deferred to operator-side commands. The eight preexisting local commits, unrelated routing/analysis changes, provider conditioning, observation authenticity and perceptual quality remain outside this review; existing-commit push is explicitly user-approved, and no new media/provider execution is authorized.

After all three fixes, the full working-tree suite passed: **1058 passed, 4 skipped, 533 subtests** (61.98s). The final release-only index export passed **1046 tests, 6 skips, 533 subtests** (59.77s), without unrelated dirty/untracked files. Live remote commit equality and post-release synchronization are recorded after their actual execution; do not infer those outcomes from test results.
