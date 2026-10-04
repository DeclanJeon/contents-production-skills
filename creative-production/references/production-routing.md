# Content and video lanes

`creative-production` selects requested outputs and coordinates shared facts, continuity, dependencies and approvals. Specialists own craft or provider execution. Load only the applicable branch; direct calls consult the coordinator contract once and delegated stages never route back.

## Core lanes

| Request | Owner | Result boundary |
|---|---|---|
| Article/blog/social text from supplied sources | Coordinator drafts directly; requested source/platform specialist only when needed | Actual text and source/claim check; no implied video, CTA, files or publication |
| Text video planning | `orchestrating-video-preproduction` with requested `developing-video-synopses`, `designing-video-character-sheets`, `storyboarding-video` | Concepts/synopsis, applicable character anchors and/or narrative/information panels. No actual images or footage. Production boards add the required `video-production-assets/references/storyboard-contract.md` |
| Production/detailed storyboard, full storyboard sheet, video production package | `video-production-assets` under the required [storyboard contract](../../video-production-assets/references/storyboard-contract.md), craft owners integrated before the final board | Beat-mapped panels, timed shots with camera/spatial/VFX/speech/audio fields, KEEP/FIX/unverified review. Technical plans integrate per cut before the board is final, not as a blanket downstream pass |
| One brief, script, shot/lighting/edit plan, claim ledger, budget or delivery checklist | `video-production-assets`, only the relevant existing module | Requested asset, not a complete production packet |
| Factual/educational video plan | Text lane and relevant production evidence modules | Verified claims and interpretation separated. No invented protagonist, causation, customer testimony or commercial objective |
| Camera-space specification | `camera-spatial-design` | Existing numeric spatial contract and actual calculated inspection |
| Blender proxy/previs | `blender-previsualization` | Actual proxy scene/render with available Blender runtime; not beauty rendering/final footage |
| Video prompt, shot decomposition, model routing, generation critique, pipeline recipe | Coordinator with [video-generation-planning.md](video-generation-planning.md) + [video-prompt-dialects.json](video-prompt-dialects.json) | Planning artifact: dialect-correct prompt, per-shot requirements/route, QA verdict. Not spend or submission authorization |
| Image-backed full production package | `video-production-assets` [review contract](../../video-production-assets/references/preproduction-review.md), default `codex-imagen` | Exact project folder, applicable actual artifacts/stills, executor restrictions in production execution §2, inspection and user review |

For links to craft resources, open the corresponding sibling `SKILL.md`. A missing core skill is a broken installation, not a normal optional dependency.

## Optional specialist/execution lanes

The installed package manifest at `video-production-assets/support/manifest.json` lists conditional external dependencies. It is an installation/availability record, not a second production state file. Named external skills below must be present before delegating their actual specialist stage; inspect the host's real tools rather than pretending a skill invocation exists.

| Request | Selected specialist | Scope |
|---|---|---|
| Campaign strategy, conversion-led copy, marketing evidence | [marketing-source-adaptation.md](marketing-source-adaptation.md); external `content-production-marketing` when installed for deeper channel workflows | Marketing only. CTA/advertising structure follows the actual brief |
| YouTube/interview/podcast adaptation | `youtube` / `podcast` for source inspection, `youtube-content` for YouTube transformation | Preserve source context, distinguish quotation from proposal, don't infer publication |
| Tistory/WordPress-specific content or operations | `tistory-blog` / `wordpress-blog` | Draft-only remains text-only; requested live changes use actual platform checks |
| Explicit story-commerce | `story-pipeline` and requested `synopsis-craft`, `script-craft`, `char-design`, `storyboard-craft` | Preserve that lane's format/contracts, not universal requirements |
| Screenplay/series or scene craft | `sw-workflow` and requested `sw-*` | Preserve story bible and stage approvals; no implied generation |
| Story/visual craft depth (concept/emotion/retention, genre/comedy, series, brand/product integration, visual mode/SSOT/continuity, dialogue/lip-sync, finishing/platform fit, reference deconstruction) | `video-production-assets` references `16-concept-emotion-retention`, `17-genre-comedy`, `18-episodic-series`, `19-brand-product-integration`, `20-visual-mode-ssot`, `22-dialogue-lipsync`, `23-finishing-platform`, `25-reference-video-analysis` | Load only for the specific craft need; never a second coordinator or state ledger |
| Selected Fal execution | `fal-video-production` | Selected provider's verified live endpoint and approved exact scope |
| Selected Higgsfield video/audio execution | Applicable `higgsfield-*` and connected tools | Preserve actual workflow, upload, rights and billing contracts; image generation is excluded by production execution §2 |
| ComfyUI/Remotion/FFmpeg runtime work | Selected installed tool surface | Design lives in the bundled generation-planning reference; runtime checks only when that branch executes |
| Music/lyrics/voice work | `songwriting-and-ai-music` for requested writing; selected available audio executor | Voice selection/creation: [dialogue reference](../../video-production-assets/references/22-dialogue-lipsync.md); SFX-only and music sourcing/rights: [edit reference](../../video-production-assets/references/09-edit.md); translated/SRT delivery: [delivery reference](../../video-production-assets/references/15-delivery.md). Actual audio needs applicable approval and listening QA |
| Illustration/thumbnail/product creative | Requested available image craft skill plus default `codex-imagen` | Brief-specific static asset, not implied video; apply the same image executor restrictions and live contract |
| Ordinary UI/brand identity | Existing design/development owner, not this production pipeline | Hybrid media shares its supplied visual contract without taking over UI ownership |

A generic draft does not require an optional platform or marketing skill. A requested platform operation does. If the chosen branch is unavailable, report its exact prerequisite and complete reachable preparation. Do not silently switch provider or describe a substitute as the requested completed result.

## State and gates

Carry source/fact status, constraints, IDs/versions, continuity, actual outputs and version-bound approval evidence through handoffs. Supplied uploads, synopses, character sheets, voices and boards are reused with version/source/inspected scope recorded; unreadable items stay unverified, never reinvented. Single text artifacts need no manifest. Multi-stage production under the existing contract uses canonical `project.json`; specialist bibles/manifests and executor adapters remain linked lane artifacts.

Topic-to-video or image-backed work follows sibling `video-production-assets/references/preproduction-review.md`: exact project root and actual review stills before review. Text-only work remains text. Review acceptance does not select a video model or authorize a sample. A separate proceed request opens live catalog/schema/price planning, then explicit bounded execution/spend approval permits submission. Publication remains separate. Changed inputs invalidate only affected dependent approvals.

Existing host interview/plan/design/browser/parallel-agent integrations can be reused when available. None is a mandatory framework for a locked text artifact. Check only the selected lane's tools and preserve one active approval flow.
