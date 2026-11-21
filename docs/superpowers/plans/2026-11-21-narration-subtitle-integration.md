# Narration and Subtitle Integration Plan

**Spec:** [Narration and subtitle design](../specs/2026-11-21-narration-subtitle-integration-design.md)

- [x] Add red-first tests for coordinator and text handoff pointers and optional dependency registration; observed the expected missing pointer failure.
- [x] Add one handoff reference for narration direction, subtitle depth selection, fallback, versioning and approval. Link it from both owners and document local runtime discovery.
- [x] Package regressions: 57 passed. Original subtitle CLI help loaded and targeted route cases: 10 passed. Broader engine and combined render suites exceeded their command timeouts; no full pass claimed.
- [ ] Integrated agent behavior and actual approved Korean-video render/playback QA.
