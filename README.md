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

1. Use the existing `creative-production` skill as the single entry point and cross-domain coordinator when a request spans planning, model/provider choice, generation, editing, 3D, or delivery. The skills in this package are scoped specialists: on a standalone call they confirm scope/route with `creative-production` once, then produce only the requested artifact; under delegation they continue without routing back or opening a second approval ledger.
2. Classify the content goal before choosing craft: narrative, factual/educational, advertising, source-derived shortform, abstract/music, or a narrow prompt/edit request.
3. Load only the applicable production, camera, or Blender skill. Keep existing screenplay, story-commerce, social-content, prompt, editing, and medium-specific skills as focused specialists; they are not bundled in this repository. For text-only story planning (concept → synopsis → character → storyboard), the coordinator may delegate to the separate `orchestrating-video-preproduction` skill, which returns text and generic prompts only — it creates no project folder, `project.json`, generated stills, or sample video, and hands downstream work back to `creative-production`.
4. Treat multi-stage `project.json` plans as the canonical production contract. A single prompt, shotlist, or edit does not need a full project manifest.
5. Check the current provider catalog, exact schema, destination requirements, and pricing before external generation. Paid submission needs explicit spend approval; publishing needs a separate request.
6. Report a generated-video deliverable complete only after the real output exists and the applicable technical and visual checks are recorded.

See [`integrations/skill-routing.md`](integrations/skill-routing.md) for the intent lanes and integration boundaries. The coordinator and other local specialist skills are intentionally not copied into this public package.

### Topic-to-video review package

For a new full video project, first choose an exact project directory. All applicable briefs, scripts, shot plans, generated review images, prompts, and QA reports stay under that root, with relative paths in `project.json`. An existing folder is resumed only explicitly; new projects do not overwrite it.

Follow [`preproduction-review.md`](video-production-assets/references/preproduction-review.md). Image-backed packages use the external **`codex-imagen` skill**, which is not bundled here and needs its own installed helper, OAuth access, and applicable usage/spend approval. Missing prerequisites stop image submission; no provider substitution is automatic.

Inspect the actual still images and report `review.md` for user review. Preproduction acceptance covers those versions only. A separate request to proceed opens video-model and live-price planning; actual video generation requires explicit approval of the bounded execution plan. Even a local/free sample video is gated. Changes reopen only affected approvals, and publication remains separate. Source sites, judgment tools, genre, runtime, and framing are current-project choices, not package defaults.


## 🚀 Install

The commands below install the three skill folders into the user skill root and preserve the package examples, QA report, and manifest under `video-production-assets/support/`. If any skill or support destination already exists, back it up and remove it before running the copy step; the script refuses to overwrite or merge with existing destinations.

```powershell
$repo = Join-Path $env:TEMP 'video-production-skills'
$skillRoot = if ($env:CODEX_HOME) { Join-Path $env:CODEX_HOME 'skills' } else { Join-Path $HOME '.codex\skills' }
$skillNames = @('video-production-assets', 'camera-spatial-design', 'blender-previsualization')

git clone https://github.com/DeclanJeon/video-production-skills.git $repo
New-Item -ItemType Directory -Force -Path $skillRoot | Out-Null
$existingSkills = $skillNames | Where-Object { Test-Path (Join-Path $skillRoot $_) }
if ($existingSkills) { throw "Existing skill directories detected; back them up/remove them first: $($existingSkills -join ', ')" }

$support = Join-Path $skillRoot 'video-production-assets\support'
$supportDestinations = @(
  $support,
  (Join-Path $support 'manifest.json'),
  (Join-Path $support 'examples'),
  (Join-Path $support 'qa')
)
$existingSupport = $supportDestinations | Where-Object { Test-Path $_ }
if ($existingSupport) { throw "Existing package support destinations detected; back them up/remove them first: $($existingSupport -join ', ')" }

foreach ($name in $skillNames) { Copy-Item -Path (Join-Path $repo $name) -Destination $skillRoot -Recurse }

New-Item -ItemType Directory -Path $support | Out-Null
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
