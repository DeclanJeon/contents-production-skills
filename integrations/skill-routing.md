# Contents production routing and consolidation map

## Canonical owners

- **Project coordinator:** [creative-production](../creative-production/SKILL.md). It owns scope, selected lanes, shared facts/continuity and approval handoffs.
- **Multi-stage production state:** [project.json contract](../video-production-assets/references/contract.md). Single text artifacts need no project database.
- **Video craft/assets:** [video-production-assets](../video-production-assets/SKILL.md), 15 selective modules plus on-demand specialist references. These references are not extra installed skills.
- **Text planning lane:** [orchestrating-video-preproduction](../orchestrating-video-preproduction/SKILL.md) with requested synopsis, character and storyboard specialists.
- **Spatial/runtime boundary:** [camera-spatial-design](../camera-spatial-design/SKILL.md) designs numeric space; [blender-previsualization](../blender-previsualization/SKILL.md) implements and inspects an actual proxy with the available runtime.

Installed IDs come from [manifest.json](../manifest.json). No duplicate global coordinator, budget database, SSOT database or provider-manifest source of truth is added.

## Request routing

| Requested output | Bundled owner/reference | Boundary |
|---|---|---|
| Source-grounded article, blog or social draft | Coordinator; [marketing/source adaptation](../creative-production/references/marketing-source-adaptation.md) when applicable | Actual requested text. No implied CTA, campaign, media or publishing. |
| Campaign copy or strategy | Marketing/source reference; requested deeper specialist | Supported facts, requested channel/variant count/voice; no forced website, SEO or brand-kit deliverables. |
| Source-derived Shorts/interview adaptation | Source inspection tool plus marketing/source reference | Actual source context, timecodes, caption/framing choices; transcript is not proof of visual/audio observations. |
| Text concept/synopsis/character/panels | Text planning lane and requested specialists | Text and generic prompts. No automatic folder, images or footage. |
| One script, claim, shot, lighting, edit, budget or delivery plan | Only applicable production-assets modules | No full-package expansion or generation. |
| Model-specific prompt, shot decomposition, live model routing or hybrid pipeline plan | [Generation planning](../creative-production/references/video-generation-planning.md), [generic serialization patterns](../creative-production/references/video-prompt-dialects.json) | Current endpoint contract, not static model rankings/caps/prices; recommendation is not execution approval. |
| Existing generated-media critique and correction | [Canonical generation QA/retry](../video-production-assets/references/21-generated-video-qa-retry.md) | Actual observations vs supplied observations vs hypotheses; no invented viewing/listening or automatic retry. |
| Full image-backed preproduction | [Preproduction review](../video-production-assets/references/preproduction-review.md) | Exact folder, applicable actual stills/artifacts, real inspection, version-bound user review. |
| Authorized media generation, assembly or publishing | Selected available executor/runtime | Verify live schema/auth/cost/destination; bounded execution and separately requested publication. |
| Ordinary UI/brand implementation | Existing design/development owner | Media can share its visual contract; content orchestration does not take over app development. |

## Currently active skill capabilities: integrated or conditional

The following maps active skill roles, not a claim that every runtime or resource is bundled, authenticated or legally cleared. Read an external specialist only when that branch is requested. Complete reachable preparation before reporting its precise missing prerequisite.

| Active capability | 2.0 treatment |
|---|---|
| `creative-production` | Maintained single bundled coordinator; current scope/review/execution/publication behavior retained. |
| `content-production-marketing` | Generic campaign/copy/source-caption/framing workflow integrated; deeper platform/channel workflow optional. |
| `video-prompt`, `video-shotlist`, `video-model-router`, `video-pipeline` | Integrated into generation planning; no additional install ID or obligatory generic external planning skill. Runtime/node/model files are not bundled. |
| `video-critique` | Integrated into canonical actual-media QA and bounded repair routing, not a second score/attempt ledger. |
| `video-prompt-atlas` | Optional actual corpus lookup via configured path; absent corpus does not block an ordinary prompt. Private paths, unverified counts and examples not imported. |
| `youtube`, `podcast`, `youtube-content` | Conditional real source retrieval/inspection and specialized adaptation; supplied source text can be drafted directly. |
| `tistory-blog`, `wordpress-blog` | Conditional platform formatting/live operations; no server credentials or personal site configuration imported. |
| `humanizer`, `grounded-citations`, `research` | Optional requested prose/evidence specialists; coordinator preserves source fidelity and voice without making them baseline dependencies. |
| `story-pipeline`, `synopsis-craft`, `script-craft`, `char-design`, `storyboard-craft` | Explicit story-commerce lane remains specialized; fixed contracts are not imposed on generic educational/narrative content. |
| `sw-workflow`, `sw-premise-theme`, `sw-story-structure`, `sw-character-conflict`, `sw-dialogue`, `sw-scene-craft`, `sw-format-adaptation` | Conditional screenplay/scene craft with its own linked bible/artifacts, not another global production state. |
| `baoyu-article-illustrator`, `baoyu-comic`, `banner-design`, `canvas-design`, `pons-blog-story-image`, `book-longform-thumbnail` | Conditional specific static-art/illustration/thumbnail craft; selected executor produces actual images. |
| `codex-imagen` | Default actual content/review image executor. Its current helper/auth/input/output/usage contract stays external; missing readiness blocks submission. Apply production execution §2 rather than automatic provider discovery. |
| `higgsfield-generate`, `fal-video-production`, `comfyui` | Conditional selected video/audio executors; provider discovery/upload/rights/spend contracts remain external. Higgsfield image generation is excluded; no automatic fallback. |
| `remotion-create`, `remotion-docs`, `remotion-markup`, `remotion-interactivity`, `remotion-captions`, `remotion-maps`, `remotion-multimedia`, `remotion-render`, `remotion-studio`, `remotion-saas` | Conditional actual React/timeline/caption/map/multimedia/render/runtime workflow. Load only the surface the brief needs. Maintenance/upgrade is not a default production stage. |
| `songwriting-and-ai-music`, `heartmula`, `audiocraft-audio-generation`, voice tools | Conditional lyrics/music/voice specialist or runtime; text remains text, actual audio needs listening and applicable execution/spend approval. |
| `songsee`, `ascii-video`, `manim-video`, `p5js` | Conditional requested analysis/format/animation techniques, not obligatory modules for every production. |
| `deep-interview`, `interactive-collaboration`, `plan`, `ultragoal`, `team`, `orchestration` | Host integrations only when available and needed; no mandatory framework, no second interview or approval database. |
| Deprecated aliases (`baoyu-infographic`, `gpt-taste`, `imagegen-frontend-*`, `web-artifacts-builder`, `theme-factory`, etc.) | Not imported; use their active owner only when the actual requested branch needs it. |

## memorable-video v6: all 28 skills reconciled

The supplied nested v6 stack and archive are superseded, not installed beside this package. Existing user-project SSOTs/bibles/assets remain user data; map them with stable IDs and version dependencies rather than deleting them.

| v6 skill | Canonical destination / disposition |
|---|---|
| `memorable-video-orchestrator` | Retired duplicate; `creative-production` owns the normalized brief, selected lanes, scoped execution and delivery. |
| `production-state-ledger` | Retired rival DB; reusable provenance, version/dependency/approval and generation records belong to project.json and linked artifacts. |
| `generation-budget-controller` | [Production execution](../video-production-assets/references/24-production-execution.md); no paid-by-default, bounded current quote and execution approval; no separate budget state. |
| `generation-retry-controller` | [Generation QA/retry](../video-production-assets/references/21-generated-video-qa-retry.md), canonical attempt records and approved retry scope. |
| `image-model-router` | Production execution and live image discovery; image-backed review uses the selected available executor and preserves explicit provider choices. |
| `video-model-router` | Generation planning plus production execution requirements; live per-shot schema/cost checks, no static ranking. |
| `creative-concept-engine` | [Concept/emotion/retention](../video-production-assets/references/16-concept-emotion-retention.md) and existing ideation module. |
| `emotional-memory-design` | Concept/emotion/retention; motivated emotional turn, perspective, motif and payoff. |
| `attention-retention-engine` | Concept/emotion/retention; brief-fit attention/payoff, not fabricated urgency or universal cliffhangers. |
| `genre-tension-engine` | [Genre/comedy](../video-production-assets/references/17-genre-comedy.md). |
| `comedy-entertainment-design` | Genre/comedy; setup/payoff/reaction/variation and continuity-safe comedy. |
| `episodic-series-engine` | [Episodic series](../video-production-assets/references/18-episodic-series.md); linked series bible and episode deltas. |
| `branded-entertainment-integrator` | [Brand/product integration](../video-production-assets/references/19-brand-product-integration.md), supported claims and brief-fit exposure. |
| `product-visual-director` | Brand/product integration; locked product appearance and deterministic critical text. |
| `visual-style-director` | [Visual mode/SSOT](../video-production-assets/references/20-visual-mode-ssot.md) plus existing visual module. |
| `character-ssot-planner` | Visual mode/SSOT; full/lite/archetype/crowd depth proportional to actual continuity need. |
| `character-continuity-engine` | Visual mode/SSOT and existing continuity assets; preserve supplied identities and intentional state changes. |
| `visual-asset-factory` | Visual mode/SSOT plus canonical asset_registry/artifact dependencies; no independent manifest schema. |
| `ai-motion-physics-director` | Existing animation/action and generation QA references; staged contact, weight, persistence and observable state changes. |
| `crowd-spectacle-director` | Animation/action and visual SSOT guidance; shared archetypes, spatial density and readable hero action. |
| `vfx-compositing-supervisor` | Animation/action and generation QA; layer separation, deterministic graphics, plate/light/contact/edge matching. |
| `generated-video-qa` | Canonical generation QA/retry; actual media inspection and evidence-bound verdicts. |
| `content-quality-judge` | Existing production QA and marketing/source draft critique; creative effectiveness is separate from rendering fidelity. |
| `voice-lipsync-performance` | [Dialogue/lipsync](../video-production-assets/references/22-dialogue-lipsync.md) and performance module; consent, words, timing and actual listening. |
| `sound-music-storytelling` | Existing edit/sound module plus dialogue/finishing references; sonic function and cue timing. |
| `platform-native-video` | [Finishing/platform](../video-production-assets/references/23-finishing-platform.md) and delivery; verify current destination specifications. |
| `cinematic-finishing` | Finishing/platform; structure/continuity/sound stable before color/texture/output polish. |
| `reference-video-deconstructor` | [Reference analysis](../video-production-assets/references/25-reference-video-analysis.md); real timecoded observations, transferable grammar, no literal copying. |

Independent attempt-budget/state schema helpers are not retained as another authority; the canonical project contract owns their useful records. The old stack's README/OLD README, execution guide, master prompts, input template, completeness checklist and top-level SSOT/asset-manifest examples are replaced by this routing index, current usage guide and owning production templates. No obsolete internal v6 links are required.

## Gates and verification

Read [preproduction-review.md](../video-production-assets/references/preproduction-review.md) before project writes or media calls in the full image-backed lane. Keep the model unresolved through review. A separate proceed request opens live execution planning; current-version acceptance, bounded execution/spend and publication scopes remain distinct. Free/local media does not bypass execution authorization.

Use structural validators only for the records they actually check. Actual visual QA needs viewed frames/sequence; audio QA needs listening. Partial API success is not complete delivery. Missing selected tool/auth/schema/price stops that stage without silently changing the provider or inventing a result.
