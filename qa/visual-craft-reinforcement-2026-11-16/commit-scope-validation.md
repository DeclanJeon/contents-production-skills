# Commit-scope validation

- Product commit: `7e2a2dfce42ecd96908c89513df7a7f66c7f16cd` — `feat(craft): strengthen visual storytelling and animatic direction (2.45)`.
- Product tree: `1e6ab7e3c9c7c29d1e3f895ef6ff18b180f348fa`; 37 owned product/test paths.
- Extracted the staged index with `git checkout-index --all --prefix=…/index-tree/` and tested that isolated tree, not the mixed working directory.
- `python3 -B scripts/check_versions.py`: package 2.45 / 25 skills consistent.
- `python3 -B -m pytest -q`: **804 passed, 4 skipped, 532 subtests passed in 51.36s**. Full captured output: [commit-scope-pytest.txt](commit-scope-pytest.txt).
- `git diff --cached --check` and a credential/private-key pattern scan passed before the product commit. Commit hooks ran normally.
- Excluded the pre-existing continuity-gate paragraph in `creative-production/SKILL.md`, the pending changes in `video-production-assets/assets/09-edit-template.md` and `video-production-assets/references/26-state-causality-continuity.md`, and the separate continuity/ad-rofan plans, tests and QA. No working file was rewritten to achieve partial staging.
- Earlier 812-test receipts describe their explicitly recorded mixed/overlaid checkout. This fresh 804-test result describes the committed product scope without the separate uncommitted continuity tests. Neither result is generated-media, playback or audience-effect verification.
- The raw docs/QA whitespace check flags three intentional Markdown hard-break lines in `qa/visual-craft-expansion-2026-11-16/loaded-0.md` and single-space blank context lines in the historical `owned-product.patch`. These evidence files are preserved verbatim; each flagged line was checked against those exact forms, and all other staged paths pass the standard whitespace check.
- Existing reports, snapshots and before/publication artifacts retained alongside this record are historical local implementation evidence, not alternative production owners or new runtime schemas. Their absolute paths and pre-commit Git states identify that original execution environment.
