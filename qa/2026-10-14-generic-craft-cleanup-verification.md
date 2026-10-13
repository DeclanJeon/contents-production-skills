# Generic craft cleanup — verification record

Detailed evidence (verbatim frozen prompts, exact worker/session metadata, actual read paths/search calls, manual outcomes, and transcript references): [`2026-10-14-generic-craft-cleanup-verification.json`](2026-10-14-generic-craft-cleanup-verification.json).

## Probe record

All six independent workers ran as `openai-codex/gpt-6.1-sol`, thinking level `medium`, with `resolvedModelIsFallback: false`. The five ordinary applications (motion, performance, lighting, initial ending, product) did not read the Rofan casebank. The sixth worker read `video-production-assets/references/rofan-craft-examples.md:1-90` only for its explicit source-evidence request. It reported bounded P01/P14 evidence and unknowns; it did not inspect source media. The JSON records exact user prompts, session IDs, actual file reads, lookup calls, and `history://` transcript references for the complete outputs.

| Worker / independent session | Result |
|---|---|
| `generic-cleanup-motion-probe` — `01a135f8-bce2-7682-876b-1161ef890525` | **PASS** — 06 repair-shop plan plus applicable QA; approach, deceleration, stop, settle, and response are separated. |
| `generic-cleanup-performance-probe` — `01a135f8-bcf5-710f-9604-107a9ef5bfed` | **PASS** — actor-executable nonverbal hold, without invented inner story or dialogue. |
| `generic-cleanup-lighting-probe` — `01a135f8-bd06-7703-9cdf-e316c0ef03f2` | **PASS** — intentional lighting proposal is separated from two-still evidence limits; unsupported causes and transitions stay unknown. |
| `generic-cleanup-ending-probe` — `01a135f8-bd19-746e-bd54-c03c82f224a7` | **Initial FAIL (field placement)** — last-picture and container-tail plans were only in next-step prose, not the final-cut QA field. |
| `generic-cleanup-product-probe` — `01a135f8-bd2e-7373-8744-44e87775f907` | **PASS** — 6-second 06 product demo and applicable readability QA; no 3D/Blender expansion. |
| `generic-cleanup-evidence-probe` — `01a135f8-e256-762b-9837-81c1837e287b` | **PASS** — explicit source request answered with bounded evidence, attribution, and UNKNOWNs; no media review claim. |

### Same-session ending retest

The ending worker’s second output is **targeted PASS only**, not an independent sample: same session `01a135f8-bd19-746e-bd54-c03c82f224a7`, second user prompt/output in `history://generic-cleanup-ending-probe`. After rereading the changed 09 owner, template, and 21 QA route, t2 embeds both checks in the existing final-cut QA field: (1) last decoded picture and (2) container duration/tail. Both actual outcomes remain `UNKNOWN / pending`; numeric ranges remain 0–3 and 3–8, with hold 6.5–8. Do not report an independent repeat or statistical improvement.

Current owner files reviewed: `video-production-assets/references/09-edit.md:1-65`, `video-production-assets/assets/09-edit-template.md:1-30`, and `video-production-assets/references/21-generated-video-qa-retry.md:77-160`. The earlier baseline has model `UNKNOWN`; it remains ungradable, was not regraded or overwritten, and supports no paired improvement rate. These six fresh probes are not three repetitions of each frozen A/B brief.

## Existing repository validation evidence

Captured from the `request-audit` worker; not rerun for this artifact:

```text
python scripts/check_versions.py
version check OK: package 2.5, 23 skill(s) consistent
Wall time 0.27 seconds

python -X utf8 -m pytest -q scripts/test_check_versions.py
.........                                                                [100%]
9 passed in 0.15s
Wall time 1.07 seconds
```

This is the version validator and its nine targeted tests, **not** a full repository test-suite result.

## Boundaries and hash caveat

- Blender work is preserved: `blender-previsualization/scripts/build_previs.py` has the separate quaternion-mode change; `blender-previsualization/scripts/test_camera_orientation_in_blender.py` remains untracked and was not run.
- Ad-craft work remains separate and untouched: `docs/analysis/ai-ad-reference-2026-10-12/` and `docs/implementation/ad-craft-recipes/`.
- No whole-set T12–T20 raw-QA hash-invariance claim is made: there is no before-hash snapshot for the complete set. The tracked files have no working diff against HEAD; eight T19/T20 artifacts are untracked and cannot be compared to HEAD. No pre/post hash claim is inferred from a current checksum.
- No source video/frame decode, audio listening, or Blender run was performed. No further model probes, CLI discovery, or tests were run for this artifact.
