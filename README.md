# 🎬 Video Production Skills

![Skill package](https://img.shields.io/badge/package-video%20production-253858?style=flat-square)
![Included skills](https://img.shields.io/badge/skills-8-2f855a?style=flat-square)
![Reuse license](https://img.shields.io/badge/license-not%20granted-lightgrey?style=flat-square)
![GitHub stars](https://img.shields.io/github/stars/DeclanJeon/video-production-skills?style=flat-square)

An eight-skill pack for **content drafting, text video planning, production assets, camera-space design, and Blender previs**. The bundled `creative-production` coordinates scoped specialists and preserves one brief and approval history. Text drafting/planning needs no media account, GPU or agent framework; actual media requires its selected external runtime/provider. The package does not include a final-video renderer or publishing integration.

![Video Production Assets icon](video-production-assets/assets/icon.svg)

## 📦 Included skills

| Skill | Use it for | Not for |
|---|---|---|
| [`creative-production`](creative-production/SKILL.md) | One content/video project coordinator: scoped drafting, specialist routing, shared facts/continuity, approval handoffs, verification and delivery. | Ordinary UI styling, a second state database, or implicit generation/spend/publication. |
| [`video-production-assets`](video-production-assets/SKILL.md) | Source-grounded briefs, story or factual beats, scripts, visual bibles, shot lists, lighting, edit/sound plans, claim ledgers, AI handoffs, budgets, delivery, and QA. | Standalone rendering or publishing. |
| [`camera-spatial-design`](camera-spatial-design/SKILL.md) | Shot size, camera placement, composition, lens/FOV, subject spacing, blocking, and motivated camera paths. | Camera shopping or Blender rendering. |
| [`blender-previsualization`](blender-previsualization/SKILL.md) | Translate a camera/spatial specification into proxy scenes, previs frames, a `.blend`, and geometric inspection reports. | Beauty rendering, full character rigging, or a guarantee of final visual quality. |
| [`orchestrating-video-preproduction`](orchestrating-video-preproduction/SKILL.md) | Internal text-planning lane for concepts, synopsis, applicable characters and storyboards. | A competing project coordinator, generated media or automatic project-folder creation. |
| [`developing-video-synopses`](developing-video-synopses/SKILL.md) | Requested concepts, loglines, synopses and beat maps in narrative, factual or abstract modes. | Unrequested characters/panels, unsupported facts or a universal ad/story formula. |
| [`designing-video-character-sheets`](designing-video-character-sheets/SKILL.md) | Text character identity, visual/behavior anchors, continuity and generic image prompts. | Real generated character imagery or mandatory characters for every video. |
| [`storyboarding-video`](storyboarding-video/SKILL.md) | Narrative/information panels with action, framing, sound and generic prompts. | Actual images/footage, paid calls or unrequested model-specific shot execution. |

The camera and Blender skills share the `camera-spatial-1.0` spatial contract. The production-assets skill bundles 15 selective modules; those modules are not 15 separately installed skills.

## 🧭 Workflow and integration

1. Use bundled `creative-production` as the single entry point for content/video work, including one artifact. Standalone specialist calls consult its scope contract once; delegated work continues without routing back or opening a second interview/approval ledger.
2. Classify the content goal before choosing craft: narrative, factual/educational, advertising, source-derived shortform, abstract/music, or a narrow prompt/edit request.
3. Load only applicable specialists. The bundled text-planning lane returns text and generic prompts, with no automatic project folder, `project.json`, images or sample video. Screenplay, story-commerce, marketing/platform operations and provider execution remain conditional external dependencies.
4. Treat multi-stage `project.json` plans as the canonical production contract. A single prompt, shotlist, or edit does not need a full project manifest.
5. Check the current provider catalog, exact schema, destination requirements, and pricing before external generation. Paid submission needs explicit spend approval; publishing needs a separate request.
6. Report a generated-video deliverable complete only after the real output exists and the applicable technical and visual checks are recorded.

See [`integrations/skill-routing.md`](integrations/skill-routing.md) and [`manifest.json`](manifest.json) for lanes and conditional dependencies. Missing external prerequisites block only the selected stage, not unrelated text planning. Missing bundled core files indicate a broken installation.

Architecture and migration rationale: [package design](docs/superpowers/specs/2026-10-02-creative-production-package-design.md), [implementation plan](docs/superpowers/plans/2026-10-02-creative-production-package.md), and [provenance boundaries](integrations/package-provenance.md).

### Topic-to-video review package

For a new full video project, first choose an exact project directory. All applicable briefs, scripts, shot plans, generated review images, prompts, and QA reports stay under that root, with relative paths in `project.json`. An existing folder is resumed only explicitly; new projects do not overwrite it.

Follow [`preproduction-review.md`](video-production-assets/references/preproduction-review.md). Image-backed packages use the external **`codex-imagen` skill**, which is not bundled here and needs its own installed helper, OAuth access, and applicable usage/spend approval. Missing prerequisites stop image submission; no provider substitution is automatic.

Inspect the actual still images and report `review.md` for user review. Preproduction acceptance covers those versions only. A separate request to proceed opens video-model and live-price planning; actual video generation requires explicit approval of the bounded execution plan. Even a local/free sample video is gated. Changes reopen only affected approvals, and publication remains separate. Source sites, judgment tools, genre, runtime, and framing are current-project choices, not package defaults.


## 🚀 Install

Python 3 is required for the installer and contract checks. The installer reads the skill list from the manifest and copies complete folders plus `manifest.json`, `examples/` and `qa/` under `video-production-assets/support/`. Initial verified host: Windows with the Codex user skill root. Other roots are accepted explicitly; other host/runtime support is not implied.

```powershell
$repo = Join-Path $env:TEMP 'video-production-skills'
$skillRoot = if ($env:CODEX_HOME) { Join-Path $env:CODEX_HOME 'skills' } else { Join-Path $HOME '.codex\skills' }
git clone https://github.com/DeclanJeon/video-production-skills.git $repo
python (Join-Path $repo 'scripts/install_package.py') --skills-root $skillRoot
```

The entire source/support and destination collision check happens before writes. Existing skill folders are never silently merged or overwritten. If your agent also scans another root, supply it with `--alias-root PATH` so duplicate core IDs are checked rather than installing another copy.

For an explicit upgrade or migration, choose a new backup directory. `--replace` backs up existing managed folders before replacement; `--alias-root` migrates only matching core IDs from that supplied root. Unrelated skills remain untouched. Review your old customizations in the backup; package installation does not merge them.

```powershell
$backup = Join-Path $HOME ('.codex/skill-backups/video-production-' + (Get-Date -Format 'yyyyMMdd-HHmmss'))
python (Join-Path $repo 'scripts/install_package.py') --skills-root $skillRoot --replace --backup-dir $backup
# Only when this additional scan root exists and should be migrated:
# Add --alias-root (Join-Path $HOME '.agents/skills') to the command above.
```

No API keys, OAuth setup, external skills, models or executables are installed. Inspect failure output for actual applied paths and retained backups; cross-folder installation is not claimed to be atomic.

After installation, restart or refresh the agent so it scans the new skill directories. To run the package checks locally, use Python 3 from the repository root:

```powershell
python scripts/test_install_package.py
python video-production-assets/scripts/test_validate_project.py
python camera-spatial-design/scripts/test_spatial_spec.py
```

Release 1.3 verification is recorded in [`qa/package-validation.json`](qa/package-validation.json): 35 regression tests, actual install/collision/backed-up upgrade/alias-migration CLI smokes, and 13 core-only model artifact/action probes. The model probes are not tool-enabled media/provider/platform tests. See [CHANGELOG.md](CHANGELOG.md) for the package cutover.

## 🧪 What the checks cover

The included QA report records the package's regression, resource-link, skill-frontmatter, and sample-plan checks. The validators check structured contracts and files; they do **not** decode or listen to finished media, judge aesthetics, validate factual claims, or confirm a provider's current capabilities. Re-check live provider features, schemas, prices, destination requirements, rights, and terms for each production.

The source bibliography documents a selective review, not exhaustive extraction. The package does not include the listed books or claim to reproduce their complete contents.

## ⚖️ Provenance and reuse

This public repository currently has **no reuse license**. Public visibility and the bibliography do not grant permission to reuse the package or any third-party source material. The listed books remain the rights holders' works; no book files are included. No `LICENSE` file is provided because the source package supplied no license and the rights for every component have not been cleared for redistribution under a new license.

New coordinator/text-lane instructions follow this package's operational contracts. Book-summary and external Notion-adapted planning references were not imported into the new lane. See [package provenance](integrations/package-provenance.md) for inclusions, exclusions and limits; this does not grant a new license or claim legal clearance of historical sources.
