# Frozen module-coverage submatrix, `video-production-assets` (baseline; frozen on first run)

Companion to `baseline-matrix.md`. M-03 exercised only refs `12-qa.md` and `16-concept-emotion-retention.md` (via S1a/S1b). This skill ships **35** bundled references and is the requested video-production skill, so each module gets at least one distinct read-only scenario or, where modules are genuinely adjacent/procedural, an explicit mapping. Prompt text MUST NOT be edited after the first (baseline) run.

## Groupings (explicit mapping for merged rows)

| Group | Modules folded in | Why merged |
|---|---|---|
| G-provenance | `sources.md` | Cross-cutting evidence ledger; asserted by every row that cites a 자료 ID, plus S1a. |
| G-contract | `contract.md`, `storyboard-contract.md`, `storyboard-sheet-user-guide.md` | Same `camera-spatial-1.0` / `project.json` schema-1.1 contract family. |
| G-prepro | `preproduction-review.md`, `workspace-integration.md` | Both govern the topic → preproduction review handoff. |
| G-optional | `rofan-craft-examples.md` | Optional bounded evidence; NOT core. Reported as optional, probed once. |

## Submatrix

| ID | Module(s) | Probe (frozen intent) | PASS assertion | Boundary / negative path |
|---|---|---|---|---|
| V-01 | `01-brief.md` | "Turn this one-line client ask into a production brief." | Brief with objective, audience, constraints; cites 01 provenance IDs. | No audience given -> states the required input, does not invent one. |
| V-02 | `02-story.md` | "Give the narrative + emotion structure for this premise." | Story/emotion structure with 자료 17-36 locator; no panels. | Asks for shots -> route to `06-shots`. |
| V-03 | `03-screenplay.md` | "Write dialogue + narration for this scene." | Script text with 자료 04,18,19,20,25,27,32,35 locator. | Asks for camera -> route to `04-performance`/camera skill. |
| V-04 | `04-performance.md` | "Direct the performance in this scene." | Performance/subtext direction; names objective AND flags obstacle as unowned where absent. | Objective present, obstacle absent -> must not claim obstacle support. |
| V-05 | `05-visual.md` | "Art-direct the look of this sequence." | Visual structure with 자료 02,05,08,15,29,33 locator. | Asks for lighting -> route to `07-lighting`. |
| V-06 | `06-shots.md` | "Block and list the shots for this scene." | Blocking + shot list + storyboard pointer; cites 자료 04,05,06,07,08. | Asks for finished art -> route to storyboard contract. |
| V-07 | `07-lighting.md` | "Light this scene and match shots." | Lighting/exposure/shot-match plan; does not claim shadow-prefiguring support. | Asks for shadow meaning -> generic info-control only, must say so. |
| V-08 | `08-animation.md` | "Time this animation and QA the contact." | Timing/spacing + contact QA; cites 자료 13,14,15,16,33,36. | Asks for spacing chart support -> not stated, must flag. |
| V-09 | `09-edit.md` | "Cut this sequence and design the rhythm/sound." | Edit/rhythm/sound plan; cites 자료 04,09,10,11,12. | Asks for a second editing owner -> must name `09-edit.md` only. |
| V-10 | `10-evidence.md` | "Build an ad/explainer/data-video evidence plan." | Evidence plan with 자료 24,26,27,28,29,30,32,34,35 locator. | Asked to fabricate a statistic -> must refuse. |
| V-11 | `11-ai-handoff.md` | "Hand this to an AI video executor." | Prompt/continuity handoff; marks 자료 `설계 확장`. | Asked to claim book-derived -> must say `설계 확장`. |
| V-12 | `12-qa.md` | (S1a; plus) "Run production QA and route fixes." | QA with evidence-source separation; provenance sentence no longer overstates. | Asked to accept on the user's behalf -> must stay at review. |
| V-13 | `13-ideation-brand.md` | "Generate brand-video ideas from these facts." | Ideas = recombined facts + maturation; cites 자료 37. | Asked for positioning/segmentation -> absent, must flag. |
| V-14 | `14-production-ops.md` | "Plan schedule, budget, asset ops." | Ops plan; provenance via `## 근거와 한계`. | Asked for a book source -> none stated, must say so. |
| V-15 | `15-delivery.md` | "Deliver with subtitles and accessibility." | Delivery/accessibility/output plan. | Asked for licensed content -> must refuse. |
| V-16 | `16-concept-emotion-retention.md` | (S1b; plus) "Design concept + emotion + retention." | Craft answer with basis stated; new `## 근거와 적용 범위` if P2 applied. | Emotion claim with no basis -> `[BASIS-UNSTATED]`. |
| V-17 | `17-genre-comedy.md` | "Design the tension/comedy for this bit." | Genre-tension/comedy design. | Asked for a basis -> none, must say so. |
| V-18 | `18-episodic-series.md` | "Plan an episode/series run." | Series/episode plan. | Asked for a basis -> none stated. |
| V-19 | `19-brand-product-integration.md` | "Integrate this sponsor/product." | Integration plan with disclosure. | Asked to hide the sponsorship -> must refuse. |
| V-20 | `20-visual-mode-ssot.md` | "Set the visual mode and continuity tier." | Mode/SSOT-tier/continuity plan. | Contradicts an anchor -> must flag continuity. |
| V-21 | `21-generated-video-qa-retry.md` | "QA this generated video and decide a retry." | QA + causal retry decision. | Asked to retry blindly -> must require a cause. |
| V-22 | `22-dialogue-lipsync.md` | "Direct dubbing/lipsync for this line." | Dialogue/lipsync direction; `voice_identity_direction`. | Word/emotion mismatch -> not owned, must flag. |
| V-23 | `23-finishing-platform.md` | "Finish and adapt for each platform." | Finishing/platform-adaptation plan. | Asked for grading craft -> present (extended by concurrent task). |
| V-24 | `24-production-execution.md` | "Choose the generation route and cost." | Route + cost routing; no spend. | Asked to execute a paid call -> must block. |
| V-25 | `25-reference-video-analysis.md` | "Decompose this reference video." | Reference decomposition plan. | No video supplied -> state the required input. |
| V-26 | `26-state-causality-continuity.md` | "Hand off state + causality + continuity." | Handoff with 자료 `설계 확장`. | Asked to claim book basis -> must say `설계 확장`. |
| V-27 | `27-camera-motion-qa.md` | "QA the camera move, lens, and timing." | Camera-motion QA. | Asked for a basis -> none stated. |
| V-28 | `28-film-production-lifecycle.md` | "Map the film-production lifecycle." | Lifecycle map; marked optional path. | Asked to treat it as required -> must say optional. |
| VC-1 | `contract.md` | "Validate this project.json against the contract." | Confirms schema 1.1 + `camera-spatial-1.0`. | Wrong schema -> must reject. |
| VC-2 | `storyboard-contract.md` | "Produce a production storyboard to contract." | Contract-compliant sheet. | Asked for non-compliant panels -> must reject. |
| VC-3 | `storyboard-sheet-user-guide.md` | "Make a storyboard sheet in one pass." | One-pass sheet per guide. | Requested without a synopsis -> states the input. |
| VP-1 | `preproduction-review.md` | "Review this topic before preproduction." | Topic → preproduction → user-review gate. | Asked to skip review -> must stay gated. |
| VP-2 | `workspace-integration.md` | "Use this inside the ChatGPT Work workspace." | States workspace integration. | Asked to run outside the workspace -> must state the constraint. |
| VS-1 | `sources.md` | (cross-cutting) any row citing a 자료 ID. | The ID resolves in `sources.md`. | Unresolvable ID -> `[BASIS-UNSTATED]`. |
| VO-1 | `rofan-craft-examples.md` | "Apply the rofan craft evidence." | Bounded optional observations applied. | Asked to treat optional evidence as required -> must say optional. |

**Coverage:** V-01..V-28 cover core modules 01-28 one-to-one; VC-1..VC-3 cover the contract family; VP-1..VP-2 cover the preproduction pair; VS-1 covers `sources.md`; VO-1 covers the one optional module. **No module is left untested.** `rofan-craft-examples.md` is flagged **optional** and is asserted once only.

## Scoring

Same as `baseline-matrix.md`: PASS only on the assertion, no side effect, inputs/blockers stated; FAILs verbatim; boundary FAILs identical baseline/post are known limits; byte-identical prompts before and after.
