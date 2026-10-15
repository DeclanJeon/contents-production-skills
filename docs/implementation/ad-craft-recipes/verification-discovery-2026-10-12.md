# Verification discovery — baseline phase

## Repository commands, not yet executed in this phase

From `README.md:120–126`, the Windows full regression path is:

```powershell
python scripts/check_versions.py
python -X utf8 -m pytest -q
```

Requirements stated by README are pytest and Pillow. No package.json/npm package script exists in the discovered root; this is a Python validation/test repository. No install was performed.

`.github/workflows/ci.yml:20–35` additionally runs:

```powershell
python -X utf8 -c "import json, pathlib; paths=[pathlib.Path('manifest.json'), *sorted(pathlib.Path('qa').glob('*.json'))]; [json.loads(p.read_text(encoding='utf-8')) for p in paths]; print(f'json ok: {len(paths)} file(s)')"
python scripts/sync_installed.py --dry-run --quiet
```

The CI job uses Python 3.12 on Ubuntu and `python -m pytest -q`; Windows should retain README's explicit UTF-8 mode. The actual post-update commands/results will be recorded separately, not overwriting this discovery or the baseline.

## Semantic application and review gates

Rerun the original briefs against the updated source snapshot in a fresh read-only CLI context, without DESIGN/archive expected answers or this assessment. Save actual output and runtime transcript, then compare the decisions to the current contract, not only source-string/regex matches. Add an independent variation brief only if it exercises a meaningful remaining condition without expected-answer leakage. Full tests/version/JSON/dry-run checks are allowed by the explicit QA assignment after integration lands; no mid-flight package/test commands were run.

Review original F1 copy→action mapping and relative onset/read/exit choices; mask/occlusion/reflection/label window; contact and inherited residue across hiding/reset. Review H1 route/landmark/threshold, partner stimulus before reaction, observer POV changes versus action phases, impossible-scale cue and return. Review V1 supported/no-slip versus fantasy branch, aliasing alternatives and actual sequence evidence, body/camera separation, contact/shadow/reflection/wake/residue. Review caption/uploader/ASR versus seen/heard evidence, claim/rights gates, condition-based N/A and no fabricated actual media passes.

Package checks can prove structure, version consistency, real fixture behavior and regression results, not sensory execution, audience comprehension, lawful rights, authenticated source claims, heard VO or final creative quality. Text application is actual consumer behavior but not generated video evidence. No production snapshot/project/package is fabricated for these text-only tasks.

## Runtime outcome

Fresh-context CLI baseline succeeded on the advertised `gpt-6-sol` model after default `gpt-6.1-sol` rejected ChatGPT authentication. Actual baseline prompt/output and full transcript are preserved in distinct neighboring files. If that runtime later fails, record the concrete failure and use an explicitly labelled direct contract-consumer exercise; do not fabricate an agent run.
