# Audio Production Routing Implementation Plan

> **For agentic workers:** Use superpowers:executing-plans or superpowers:subagent-driven-development to implement this plan.

**Goal:** Route standalone audio cues to the right default candidate without changing the parent video route or authorizing execution.
**Architecture:** A single coordinator-owned audio decision reference; the preproduction worker returns text requirements and the optional provider catalog describes runtime availability. Retain the existing Suno specialist.
**Tech Stack:** Markdown skill contracts, JSON manifest, Python/pytest reachability checks.
**Spec:** [Audio production routing](../specs/2026-11-21-audio-production-routing-design.md)

- [x] Add reachability and dependency checks; observe two expected failures before implementation.
- [x] Attach the coordinator and preproduction handoffs; preserve the published Suno anchor, normal native routing and no-audio conditions.
- [x] Add input/fallback instructions, execution gates and narration-first timing. Keep ElevenLabs SFX execution unverified.
- [x] Run targeted routing/load/sync and integrity tests: 66 passed, 1 skipped for the optional offline tokenizer cache. No model behavior evaluation or provider execution/listening was performed.
