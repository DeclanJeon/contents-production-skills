# 🎬 Video Production Skills

![Skill package](https://img.shields.io/badge/package-video%20production-253858?style=flat-square)
![Included skills](https://img.shields.io/badge/skills-3-2f855a?style=flat-square)
![Reuse license](https://img.shields.io/badge/license-not%20granted-lightgrey?style=flat-square)
![GitHub stars](https://img.shields.io/github/stars/DeclanJeon/video-production-skills?style=flat-square)

A focused skill pack for **video preproduction, camera-space design, and Blender previs**. It helps turn an idea, script, or spatial brief into checked production artifacts. It does not itself render or publish a finished video.

![Video Production Assets icon](video-production-assets/assets/icon.svg)

## 📦 Included skills

| Skill | Use it for | Not for |
|---|---|---|
| [`video-production-assets`](video-production-assets/SKILL.md) | Source-grounded briefs, story or factual beats, scripts, visual bibles, shot lists, lighting, edit/sound plans, claim ledgers, AI handoffs, budgets, delivery, and QA. | Standalone rendering or publishing. |
| [`camera-spatial-design`](camera-spatial-design/SKILL.md) | Shot size, camera placement, composition, lens/FOV, subject spacing, blocking, and motivated camera paths. | Camera shopping or Blender rendering. |
| [`blender-previsualization`](blender-previsualization/SKILL.md) | Translate a camera/spatial specification into proxy scenes, previs frames, a `.blend`, and geometric inspection reports. | Beauty rendering, full character rigging, or a guarantee of final visual quality. |

The camera and Blender skills share the `camera-spatial-1.0` spatial contract. The production-assets skill bundles 15 selective modules; those modules are not 15 separately installed skills.

## 🧭 Workflow and integration

1. Use the existing `creative-production` skill as the single cross-domain coordinator when a request spans planning, model/provider choice, generation, editing, 3D, or delivery.
2. Classify the content goal before choosing craft: narrative, factual/educational, advertising, source-derived shortform, abstract/music, or a narrow prompt/edit request.
3. Load only the applicable production, camera, or Blender skill. Keep existing screenplay, story-commerce, social-content, prompt, editing, and medium-specific skills as focused specialists; they are not bundled in this repository.
4. Treat multi-stage `project.json` plans as the canonical production contract. A single prompt, shotlist, or edit does not need a full project manifest.
5. Check the current provider catalog, exact schema, destination requirements, and pricing before external generation. Paid submission needs explicit spend approval; publishing needs a separate request.
6. Report a generated-video deliverable complete only after the real output exists and the applicable technical and visual checks are recorded.

See [`integrations/skill-routing.md`](integrations/skill-routing.md) for the intent lanes and integration boundaries. The coordinator and other local specialist skills are intentionally not copied into this public package.

## 🚀 Install

The commands below install the three skill folders into the user skill root and preserve the package examples, QA report, and manifest under `video-production-assets/support/`. If any destination skill already exists, back it up and remove it before running the copy step; the script refuses to overwrite existing skills.

```powershell
$repo = Join-Path $env:TEMP 'video-production-skills'
$skillRoot = if ($env:CODEX_HOME) { Join-Path $env:CODEX_HOME 'skills' } else { Join-Path $HOME '.codex\skills' }
$skillNames = @('video-production-assets', 'camera-spatial-design', 'blender-previsualization')

git clone https://github.com/DeclanJeon/video-production-skills.git $repo
New-Item -ItemType Directory -Force -Path $skillRoot | Out-Null
$existing = $skillNames | Where-Object { Test-Path (Join-Path $skillRoot $_) }
if ($existing) { throw "Existing skill directories detected; back them up/remove them first: $($existing -join ', ')" }
foreach ($name in $skillNames) { Copy-Item -Path (Join-Path $repo $name) -Destination $skillRoot -Recurse }

$support = Join-Path $skillRoot 'video-production-assets\support'
New-Item -ItemType Directory -Force -Path $support | Out-Null
Copy-Item (Join-Path $repo 'manifest.json') $support
Copy-Item (Join-Path $repo 'examples') $support -Recurse
Copy-Item (Join-Path $repo 'qa') $support -Recurse
```

After installation, restart or refresh the agent so it scans the new skill directories. To run the package checks locally, use Python 3 from the repository root:

```powershell
python video-production-assets/scripts/test_validate_project.py
python camera-spatial-design/scripts/test_spatial_spec.py
```

## 🧪 What the checks cover

The included QA report records the package's regression, resource-link, skill-frontmatter, and sample-plan checks. The validators check structured contracts and files; they do **not** decode or listen to finished media, judge aesthetics, validate factual claims, or confirm a provider's current capabilities. Re-check live provider features, schemas, prices, destination requirements, rights, and terms for each production.

The source bibliography documents a selective review, not exhaustive extraction. The package does not include the listed books or claim to reproduce their complete contents.

## ⚖️ Provenance and reuse

This public repository currently has **no reuse license**. Public visibility and the bibliography do not grant permission to reuse the package or any third-party source material. The listed books remain the rights holders' works; no book files are included. No `LICENSE` file is provided because the source package supplied no license and the rights for every component have not been cleared for redistribution under a new license.
