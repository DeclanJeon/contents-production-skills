# User-authorized feature push and current Pi deployment

## Authorization and scope

After being told the implementation/review status and the unperformed behavioral evaluation, the user explicitly requested: “커밋하고 푸시해 그리고 현재 에이전트 스킬에 업데이트하고”. This authorizes the feature-branch push and current Pi installation, not execution of the 56 behavioral probes. Semantic/actual-consumption acceptance remains unverified.

- Source implementation/QA commit: `4bd55f1576b3b3d39d0ab18e4f3f048f2e7af4f0`.
- Remote: `https://github.com/DeclanJeon/contents-production-skills.git`.
- Pushed branch: `feat/staged-skill-loading-20261118`; normal push, no force.
- `main` remains `bd5fb689dced7d09d966bff8f1897c06bac6082f`; no merge or adoption of its dirty routing evaluator/tests.

## Current agent update

- Synchronizer: `scripts/sync_installed.py --repo-root <feature-worktree> --root /home/declan/.pi/agent/skills`.
- Dry run and actual result: 25 symlinks repointed, no real-directory displacement.
- All 25 manifest-listed Pi skill links now target `/home/declan/.cache/pi-worktrees/contents-production-loading-20261118/<skill>`.
- Pi settings changed only in `skills`: explicit managed Pi paths plus exact exclusions of the older managed Codex/shared copies prevent shadowing. The rest of the Pi settings is byte-value equivalent after JSON parsing.
- Installed Pi's local resource-resolution/filtering and skill-loading functions selected the new source for all 25 names, with zero diagnostics for these skills. Verification used local filesystem discovery only: no package resolution/install, extension execution or LLM/provider invocation.
- Codex, Claude and shared-agent skill links are unchanged. The two original dirty routing files retain their pre-deployment hashes. Non-manifest skills are not repointed.

## Verification

- Fresh pre-push full suite: **1120 passed, 5 skipped, 533 subtests**. Four skips require Windows junctions; the fifth is the optional real-tokenizer integration test because the old `/tmp/data-gym-cache` entry is no longer present. No cache download/install was attempted. The prior 1121-pass run and the eight reproduced reference totals remain recorded historical evidence.
- Installed `sequence_context.py --help` exposes `--view {full,focus}`.
- Installed pure focus builder returns `sequence-focus-view/1`, read-only and non-executable, for an in-memory fixture.
- Remote branch was queried after the source push and matched `4bd55f1`.

## Reload, source lifetime and rollback

An already-running Pi session still needs **`/reload`** (or restart) to rebuild its skill metadata. Updating files does not rewrite the existing conversation's system prompt.

**Keep this worktree:** it is the active Pi skill source; do not delete it as branch-cleanup scratch. Other agents continue using the original checkout.

Pi settings, previous symlink targets and dirty-file hashes are backed up locally under `.superpowers/deployment-current-pi/` in this worktree. They are deliberately not committed as global machine configuration. Rollback restores those Pi settings/links only; it does not reset the original repository or alter production data.
