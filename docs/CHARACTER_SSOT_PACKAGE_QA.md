# Character SSOT / full-package repair verification

## Implemented contract

The full image-backed chain is synopsis Markdown → per-character persona and 0–33 Character SSOT Markdown + one actual seven-view Identity Sheet A → version-linked technical storyboard → one actual full storyboard PNG. Sheet B/C/D remain prompt specifications, not automatic extra generation. Explicit fictional-design delegation permits labeled proposals for missing attributes; real-person unknowns remain unknown. Narrow text requests do not acquire media, files or spending.

Canonical schema 1.1 is retained. `preproduction` selects package artifacts. Character records link persona, SSOT artifact and matching identity image. Board dependencies consume current synopsis/SSOT versions; shots consume matching identity images. Combined sheet assets record complete ordered panels, actual pixel-source IDs and hashes (source sheet for crops, otherwise clean image).

`--profile preproduction` checks actual nonempty Markdown, image decoding, hashes, coverage, current dependency versions and blockers. Reviewed/approved preproduction reviews and approved execution plans invoke the image-package gate even under plan. Draft/stale incomplete ledgers remain recordable. These checks do not prove seven-view anatomy, identity fidelity, visual storytelling, rights or acceptance.

## Observed verification

- `python -m pytest -q`: **130 passed, 169 subtests passed, two warnings**, exit 0. The warnings are Windows subprocess UTF-8 decoding thread warnings in existing sync tests.
- Regression evidence: the missing-package reviewed fixture failed before the new gate (the original validator returned no errors). During integration the characterless fixture retained an obsolete character-linked image; removing that obsolete fixture record restored the intended narrow-scope case. Actual renderer tests caught missing MARGIN; the layout constant is now defined.
- Actual renderer CLI: five synthetic colored panels, Korean event text, Malgun Gothic font, **1744×1614 PNG**, exit 0. The resulting file was registered with actual hash/order/source maps and strict CLI validation returned valid/exit 0. Opened and inspected all five cells, external Korean captions, synopsis locators, SSOT version, camera start/end and story order. Evidence image: `../qa/ssot-storyboard-render-smoke.png`. This is synthetic rendering proof, not a production character design or ad.
- Actual negative regression paths: corrupted/changed source, output escape, no-overwrite, and crop-source hash mismatch. Crop output was registered and passed strict validation; changing its recorded source hash was rejected.
- Current `productions/132-autumn-25s/project.json` v1.8: actual plan CLI valid/exit 0; strict preproduction CLI rejected/exit 1 with **14 errors**, including stale synopsis/board, missing persona/character SSOT/identity image, missing character inputs, absent combined sheet and four open blockers. No false readiness is claimed.
- `python scripts/check_versions.py`: package 2.4, 17 skills consistent. Changes remain Unreleased.
- `python scripts/sync_installed.py --dry-run`: **51 current junctions skipped**, zero created/repointed/backed up. Codex/Claude/OpenCode already read this repository; no installation overwrite was needed.

## Instruction behavior

Three independent tool-free applications are saved in `../qa/character-ssot-instruction-smoke.json`:

1. Missing full image package: refused video handoff, required per-character seven-view sheets and actual combined board, distinguished plan from strict/visual checks.
2. Delegated fictional text SSOT: selected missing traits as labeled proposals, returned 0–33 and A/B/C/D/master/prefix/negative requirements, no tool/file/media execution.
3. Real-person text-only: did not invent unknown identity/biography/psychology or force a full media package.

These are instruction-following examples, not a statistical benchmark or provider/image-quality evidence. Earlier five baseline applications showed the former optional-combined-board/overrestricted-fiction behavior; the new three prompts are smoke cases, not a matched numerical improvement claim. An earlier pending application batch lost its local runtime before results were collected and is not counted.

## Review and integration

Independent contract review identified crop-source provenance mismatch. Renderer, gate and contract now share the actual pixel-source selection rule, with an actual crop render/register/pass then stale-hash rejection regression. A separate diff-based review excluded new/untracked files and is not accepted as comprehensive approval; parent integration and runtime verification cover those files. No build/test result from an unfinished delegated lane is counted.

Production documents and ledger now explicitly invalidate previous readiness/execution claims. Fixed product-PNG composites and the existing 8-second result remain rejected history, not accepted creative treatment. SH01/SH02/SH04/SH05 sources are preserved; valid single-drop SH03 and the final 25-second ad do not exist. No new production image/video provider call, additional credits or publication occurred in this repair.

The pre-existing worktree had 57 modified tracked files and 42 untracked files before this task. Related edits are left uncommitted to avoid bundling unrelated work; no blanket staging or destructive cleanup was performed.
