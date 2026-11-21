# Suno Music Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development or superpowers:executing-plans. Steps use checkbox syntax.

**Goal:** Produce usable Suno inputs and route the music specialist from the existing production coordinator only when selected.

**Architecture:** The coordinator loads a conditional provider pointer without changing the primary stage or adding a ledger. The Suno specialist owns music prompts and checks the live provider before any approved execution. Text preproduction returns indexed requirements instead of selecting or executing a provider.

**Tech Stack:** Markdown skill instructions, JSON manifest, Python/pytest reachability checks, optional official Suno MCP.

**Spec:** [Suno design](../specs/2026-11-21-suno-music-design.md)

## Global constraints and review focus

Keep standalone requests outside video intake, ordinary video audio in-request, planned cut sync separate from generated length, existing tracks reusable, and generation behind its own approval. Stings and loops use Sounds; missing provider never grants a fallback or spend authority.

## Task: Package and route the Suno specialist

- [x] Add red-first registered reachability and explicit coordinator/text-handoff wiring assertions in `scripts/test_skill_reachability.py`.
- [x] Implement `suno-music/SKILL.md` and `suno-music/references/suno-inputs.md`; register it and its optional runtime in `manifest.json` and document discovery in `README.md`.
- [x] Attach conditional route at `creative-production/SKILL.md` and `creative-production/references/production-routing-optional.md`; add indexed text-only handoff at `orchestrating-video-preproduction/SKILL.md`.
- [x] Run reachability, routing, loading/sync regressions. Two red assertions reproduced the missing registration and coordinator pointer; the targeted suite then reported 61 passed, 1 skipped (optional offline tokenizer cache).
- [ ] Independent model-based behavior evaluation remains unrun. No Suno generation or listening was performed.
