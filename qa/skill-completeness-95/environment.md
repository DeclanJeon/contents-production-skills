# W0 runtime evidence

## Observed in this worker

- `omp --help` exited 0 and reported **omp v18.11.1**. Help documents `--model`, `--tools`, `--no-lsp`, `--no-extensions`, `--no-session`, `--max-time`, and `-p`.
- No security/rules-disabling flags used. Runner fixes tools to `read,grep,glob`, disables LSP and extension discovery, and does not expose arbitrary backend commands. Codex backend deliberately unsupported: no verified read-only tool boundary for it in this worker.
- `python -X utf8 qa/skill-completeness-95/run_cases.py --manifest qa/skill-completeness-95/case-manifest.json --build-manifest` exited 0: `Frozen hashes verified; wrote 61 unique cases (59 + S1a/S1b).`
- Manifest creation directly read original repository prompt/matrix bytes and verified all four historical sizes/SHA-256 values. No book-derived implementation claims; no book originals required for this runner.
- No installations, authentication/config changes, external uploads, media generation, training, deployment, publication, commits, or resets performed.

## Provided evidence, not independently re-executed

Parent contract states explicit-model `omp --model openai-codex/gpt-6.1-sol --tools read,grep,glob --no-session --max-time 90 -p ...` successfully read repository manifest version 2.9 / 24 skills. Native task-worker failure `No model selected` is parent-reported ground truth, not retried here. Neither observation is a worker-run behavioral case.

## Execution identity and limits

New series: `omp-readonly-explicit-model-v1`; not identical to historical Codex or alternate arms. Default concurrency 1; explicit default model `openai-codex/gpt-6.1-sol`; fresh ephemeral process per case; 90-second model limit and 105-second process timeout. Model alias resolution and inherited provider configuration remain runtime dependencies; identity records requested model, binary path/version, selected profile environment, runner hash, prompt hash, manifest hash, and repository tree hash. Global auth/profile content is not exported or hashed because it may contain secrets; changing inherited global provider configuration requires a new run directory and must be reported by the operator.

Tree hash covers repository files recursively, including installed skill code, assets, references and root/config dotfiles; excludes all QA evidence, `.git`, `node_modules`, Python caches. Frozen QA inputs are separately verified and runner is separately hashed. Tree mutation before a case stops execution; mutation during a case marks its attempt ERROR and stops the series. This detects persistent differences, not write-and-revert activity; read-only tool selection is the primary boundary, not mutation detection.

Tests and fresh-session M-03/M-04/S1a runs deferred to parent after shared edits. No full arm launched. The tightened no-LSP/no-extension profile requires fresh-session verification; parent-reported prior probe is not asserted to prove this exact profile. Read tools can access non-repository locations permitted by inherited runtime rules; no filesystem sandbox is claimed. Output is conservatively screened for common read/auth/transport errors; semantic failures without those markers require independent review. Completed attempts remain UNREVIEWED, never automatic PASS.

## Subsequent leader verification

- The exact tightened profile (`--tools read,grep,glob --no-lsp --no-extensions --no-session --max-time 90`, explicit `openai-codex/gpt-6.1-sol`) successfully used the read tool on `manifest.json` and returned package 2.9 / 24 skills with `$.version` and `$.skills` locators; process bg_23 exited 0. This is a runtime preflight, not a formal case or before/after evidence.
- The new runner and real-media delivery regression tests were executed together after their implementation: 21 passed / 9 subtests passed. Formal-case responses remain pending final tree freeze and independent adjudication.
- Blender was found outside PATH at `C:/Program Files/Blender Foundation/Blender 5.2/blender.exe`. Actual Cycles CPU six-keyframe render and fresh `.blend` reopening succeeded; the leader inspected the six-render contact sheet. Scope and Blender 6.0 deprecation limits are in `smoke-results.md`.
- No user login, new secret, administrator installation, global settings change or safety bypass was needed for these observed execution paths.
