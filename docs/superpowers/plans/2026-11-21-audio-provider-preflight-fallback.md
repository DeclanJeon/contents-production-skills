# Audio Provider Preflight and Fallback Implementation Plan

> Implement with superpowers:executing-plans or superpowers:subagent-driven-development.

**Goal:** Check the necessary audio tools before dependent work and continue through eligible, authorized fallbacks without redundant install prompts.
**Architecture:** Extend the existing coordinator-owned audio cue contract and optional runtime manifest; no new ledger or executor.
**Spec:** [Preflight and fallback](../specs/2026-11-21-audio-provider-preflight-fallback-design.md)

- [x] Add static wiring checks for early preflight, fallback and separate ElevenLabs runtime declarations; observed the expected missing preflight link failure before implementation.
- [x] Add the preflight and fallback decision contract to the existing audio cue reference, link it from the coordinator, and update optional dependency metadata and user docs.
- [x] Run reachability, routing, sync and integrity regressions: 67 passed, 1 skipped (optional offline tokenizer cache). Provider execution and model behavior evaluation were not performed.
