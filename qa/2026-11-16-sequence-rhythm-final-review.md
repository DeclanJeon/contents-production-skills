# Sequence rhythm final review and fix evidence

This record supersedes the media-tail success claim and media-status ruling in `2026-11-16-sequence-rhythm-validation.json` and the execution ledger. Release remains 2.41; no push/publication performed.

## Independent review

Two requested Opus reviewer launches failed with provider access errors (403/401); they did not review anything. The successful independent read-only reviewer used `opengateway/deepseek/deepseek-v4.1-flash-eco`. It inspected repository content but explicitly did not execute tests or verify the historical commit range. Its findings were checked against the local source before implementation. A successful agent response is not itself test evidence.

## Fixed Important findings (one fix pass)

- **F1:** media unmatched boundaries previously reported `measured`. Now `partial`, consistently with CSV attribution. Regression `test_f1_media_unmatched_is_partial`: RED → GREEN. The former ledger ruling reserving `partial` for CSV was wrong and is withdrawn.
- **F2:** no end-of-media boundary previously omitted the last cut. Probe the video duration using existing ffprobe, include the terminal boundary, and report unavailable duration as `unverified`/exit 3 instead of inventing it. `stats.total_s` and `curve_check.planned_total_s` expose totals; temporal CSV gaps/overlaps are reported and make the report partial. Regression tests for final tail, no-transition video, unavailable duration and CSV gap: RED → GREEN. Integration test creates a 6-second three-color clip with existing ffmpeg, verifies three attributed cuts totaling 6 seconds (including SH03 at 4–6s), and checks probed duration. The earlier two-cut smoke result was truncated and was not valid whole-media evidence.
- **F3:** CSV NaN/infinite times previously emitted invalid JSON and disappeared from statistics. Reject non-finite times as invalid input. Parameterized regressions for NaN/+Inf/-Inf: RED → GREEN.

No second independent review was dispatched; regression tests and the full suite verify the single fix pass.

## Deferred Minor findings

- **F4:** structurally malformed project JSON can still raise rather than returning structured exit 2. Use a validated project as input; nonexistent media may be described as undecodable.
- **F5:** matching is conservative when multiple starts fall within tolerance: a unique nearest candidate is not selected. Unmatched results remain explicit, not guessed.
- **F6:** malformed planned times may carry null durations but zero delta. Planned-only output is not measurement evidence.
- **F7:** handle-shortfall text says “realized” even for estimated project source durations. The earlier QA note claiming planned projects report no shortfalls is incorrect; they can report shortfalls computed from their declared source capacity. Do not treat this wording as independently verified clip metadata.
- **F8:** defaults table typo `평짌` remains.
- **F9:** corpus reproduction snippet is incomplete (directory creation, optional shared strings, final aggregation); published corpus numbers are not reproducible from that note alone. Those corpus figures remain reference observations only, not a QA standard.

## Disposition of reviewer exclusions

- Commit provenance/test execution: verified by the parent on the current local tree; no historical test run inferred from the reviewer.
- Actual aesthetic improvement: not claimed. Requires production-sequence playback and user acceptance; passing structural checks is insufficient.
- Scene-detection thresholds/minimum interval: retained as tunable heuristics, not ground truth. A whip pan can still be mistaken for a cut and very short cuts can be merged.
- Chained monotony tolerance: retained as defined in the plan (relative to previous duration); it is an observation, not a global spread limit or score.
- Playback-rate/fps handle conversions: retained project-fps contract and prose handoff. This report does not certify source endpoint conversion.
- Concurrent duplicate changelog sections and pre-existing anchor issues: left untouched; unrelated cleanup is not authorized by this fix pass.

## Rulings made during execution (including costs)

1. Work was committed directly on main to avoid installation-hook/worktree path effects. Cost: changes landed before independent review. No new integration or push performed here.
2. Foreign `path_map.py` work was excluded via exact-path staging. Cost if staging were wrong: unrelated changes could enter a commit.
3. Replaced an impossible corpus-number grep with checks of defaults and absent scoring metrics. Cost: weaker automatic detection of reference-number leakage.
4. Shared-beat test fixture also links the beat from the corresponding panels. Cost: no production semantic change; coherent fixture required.
5. Repeated shot sizes require three consecutive entries, as specified, rather than the plan test's two. Cost: two-cut repetitions go unreported.
6. ffmpeg filter uses escaped comma plus metadata output; actual integration now confirms it. Cost if incorrect: missed scenes.
7. Former CSV-only partial ruling is withdrawn (F1 fix); both modes flag unmatched observations. Cost if wrong: users could read unaligned cuts as complete measurements.
8. Replaced the empty generated 2.41 changelog placeholder with actual release notes. Cost if wrong: inaccurate release history.
9. Pre-existing anchor issues were left out of scope. Cost: those pre-existing links remain problematic.
10. ffprobe is a new optional prerequisite for complete media measurement; absent/unusable duration produces unverified rather than truncated success. Cost: some environments need their existing ffprobe made available; nothing is automatically installed.

## Fresh verification

- Before fixes: `python3 -m pytest video-production-assets/scripts/test_rhythm_review_regressions.py -q` → **8 failed** on the intended F1/F2/F3 behavior.
- After fixes: same file → **9 passed** (includes real ffmpeg/ffprobe integration).
- Measurement + review regressions together before integration addition → **22 passed**.
- `python3 -m pytest -q` → **800 passed, 4 skipped, 532 subtests passed**.
- `python3 scripts/check_versions.py` → package **2.41**, **23 skills consistent**.
- `git diff --check` → clean.

Full-suite skips are not evidence of coverage. No production footage, listening test or actual audience-response evaluation was performed.
