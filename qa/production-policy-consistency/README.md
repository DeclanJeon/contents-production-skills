# Production policy consistency

## Scope

- `22-dialogue-lipsync.md` owns interval-scoped visual lip-sync applicability: approved nonvisible intervals may be N/A, unmet required readability needs revision, and uninspected/unheard evidence remains unverified. Audio checks remain separate.
- `29-reference-driven-production.md` delegates these verdicts to22; its reference-scope guidance is unchanged.
- The coordinator and README follow the existing default/explicit eligible image-executor policy, provider exclusions and Codex Imagen still-image cost exception. Other executors retain their approval requirements.
- The manifest declares the existing conditional `ai-delegation-loop` requirement as external, unverified and not automatically installed.
- Only the two affected skill versions change; package version2.34 is retained.

## Verification

```sh
python3 -m pytest -q scripts/test_production_policy_consistency.py scripts/test_guide_integration.py scripts/test_video_pack_boundary.py
python3 scripts/check_versions.py
python3 -m pytest -q -rs
```

The new regression invokes the real installer in a temporary directory and verifies copied external-dependency metadata without bundling or installing that dependency. It does not simulate agent instruction compliance. One final read-only review found no actionable defects in the owned changes.

These are structural/document checks, not provider availability, instruction-compliance efficacy or audiovisual-quality evidence. No new reference-usage rule is added; prepared behavioral evaluations have not been executed. Raw research, local diagnostic paths and unrelated concurrent work are intentionally excluded from this commit.
