# F1 evidence-closure handoff

Status: assigned edits and 28 supplemental scenarios supplied; independent model replay pending. No score or formal PASS claim.

## Defects and exact changed locations

Defect labels below identify review-source-1.md findings; that review did not assign machine IDs.

| Local defect ID / review location | Changed file under video-production-assets/references/ | Current lines and action |
|---|---|---|
| F1-D01 / review L8,194 ranking conflict | 13-ideation-brand.md | L5 consumes topic-demand-selection/SKILL.md Decision Procedure; discovery consumer retains count/selection only, not fit-first precedence. |
| F1-D02 / review L92-93 comedy | 17-genre-comedy.md | L11,14,20 optional genre patterns; L39-40 removes reaction multiplier/near-forgetting mandate; L59 optional escalation comparison; L67 support boundary; L69 actual Culhane binding. |
| F1-D03 / review L94 2D priority | 20-visual-mode-ssot.md | L28,32 makes adopted attributes and needed view/pose reference explicit, preserves texture-led 2D; L114,117-118 makes crowd choreography/cut/comp routes optional; L133 boundary; L137 original binding. |
| F1-D04 / review L95 broader compositing | 21-generated-video-qa-retry.md | L16 single-generation/comp comparison rather than unconditional routing; L41-45,50,52 observed target-specific comparisons instead of universal order/effect gates; L179 narrow Alpha Over contract; L180 versioned Shadow Catcher evidence. |
| F1-D05 / additional encountered callback mandate | 18-episodic-series.md | L14 optional episode recipe; L34 callback linkage without unverified memory/payoff success gate. |
| F1-D06 / additional encountered platform mandate | 23-finishing-platform.md | L48 optional platform design; L58 permits justified common cut; L68 applicable diagnostic questions, not automatic device/loop/motif/crop failures. |
| F1-D07 / additional encountered sponsor/material prescriptions | 19-brand-product-integration.md | L9 integration-mode/sequence comparisons; L48 material suggestions explicitly conditional, not universal quality gates. |
| F1-D08 / additional encountered sound-effect prescriptions | 09-edit.md | L136 sound-layer, silence/impact and music-placement choices explicitly optional listening comparisons. |

No capabilities were removed: reaction design, callbacks, genre patterns, reference packs, texture-led 2D, crowd design, compositing, sponsor integration, sound planning and platform adaptation remain available. Unsupported empirical guarantees and unrequested device mandates are narrowed; borrowed craft is not relabeled authored invention.

## Direct reading and bounded entailment

Read approved work-order L178-409; fixed rubric-definition.md L1-34; runner-profile-v3.md L1-34; review-source-1.md L1-212; current owner SKILL.md L1-112; topic-demand-selection/SKILL.md L1-56. Read all numbered 01-28 procedures to their displayed ends, including unabridged 25 L33 and L90 separately after the reader flagged truncation. This is procedure inspection, not blanket source closure or model application evidence.

New original: `E:/Book/06_Book/originals/콘텐츠_제작/md/Animation  from script to screen (Culhane, Shamus) (z-library.sk, 1lib.sk, z-lib.sk).md`.

- Measured 668243 bytes, SHA-256 `be4240f517b982d1d78c1417edf0affed31c999cd82ba399be51f85d4d393ca8`.
- READ-PARTIAL L387 entire, printed p174, Double Takes: stimulus, delayed realization, character-dependent interval. Does not support multiplier or callback/forgetting effects.
- READ-PARTIAL L447-449 entire, printed pp200-201, Exercise: Animals: front/profile/back model information; neutral base model versus head/body expressive poses. Does not rank those references above texture or authorize seven views for all 2D projects.
- OCR text only; no original illustration inspection. No book passages reproduced in QA files.

Official documentation directly read 2026-10-17:

1. [Blender 4.2 LTS Alpha Over](https://docs.blender.org/manual/en/4.2/compositing/types/color/mix/alpha_over.html), Inputs/Properties. Premultiplied expectation, straight conversion and nonzero legacy Premultiply overriding checkbox; not a general matching recipe.
2. [Blender 4.2 LTS Cycles Object](https://docs.blender.org/manual/en/4.2/render/cycles/object_settings/object_data.html), Visibility/Mask/Shadow Catcher and Motion Blur. Shadow/indirect-light compositing with pass/viewport approximation distinction; topology-changing deformation blur limitation. Not automatic matching, reflection correctness, other-tool support or executed Blender success.

Web rendition was live reader HTML; SHA/bytes `N/A-live-web`. Versioned title explicitly states 4.2 LTS; pages also expose latest canonical URLs, so retain requested version path and recheck actual runtime before execution. No figures inspected.

## Commands and actual observations

1. Initial PowerShell identity command failed because `$p` was expanded before the nested shell; output was missing LiteralPath arguments, exit 1. No source/file was changed. Corrected with a Python read-only byte/hash command:

   `python -c "import pathlib,hashlib; p=pathlib.Path('E:/Book/06_Book/originals/콘텐츠_제작/md/Animation  from script to screen (Culhane, Shamus) (z-library.sk, 1lib.sk, z-lib.sk).md'); b=p.read_bytes(); print(len(b),hashlib.sha256(b).hexdigest())"`

   Output: `668243 be4240f517b982d1d78c1417edf0affed31c999cd82ba399be51f85d4d393ca8`, exit 0.
2. `python -X utf8 qa/skill-completeness-95/closure-F1/smoke_local.py`, exit 0. This local program uses Pillow.Image.alpha_composite, not Blender. Actual background RGBA [20,40,80,255]; foreground [240,220,180,128]; composite center [130,130,130,255], matching expected alpha arithmetic; outside remained background. Actual 96x64 PNG written and directly opened: centered gray rectangle on dark blue background. This proves only the bounded local overlay observation, not changed-instruction adherence, Blender node execution, contact physics, full temporal QA or provider success.
3. Same local command parsed supplemental JSON: scenario_count=28; stable_ids_complete=true; missing_required_paths=[]. These are catalog/availability observations, not behavioral PASS verdicts. `local-observations.json` records `NOT_RUN_PARENT_FINAL_FREEZE_REQUIRED`.

Evidence artifacts: `claims.tsv` (fixed 16 columns; unique F1-C01..C06), `smoke-prompts.json` (F1-01..F1-28), `smoke_local.py` (retained minimal reproducible local observation), `local-observations.json`, `alpha-composite.png`.

## Exact remaining limitations and handoff

- Parent must invoke all 28 supplemental prompts from the final frozen tree with required checkout reads and independently inspect final responses and structured traces. No fresh-model invocation occurred here. Handmade prompt/check definitions and local alpha output do not satisfy that behavioral acceptance.
- F1-25 is deliberately runnable from synthetic user observation records, not inaccessible external media; output must attribute observations and withhold actual video inspection. F1-12/21/27 similarly distinguish supplied observations/plans from direct inspection. These are valid bounded outputs, not substitute actual-media PASS claims.
- No Blender 4.2 execution, provider generation, paid-success observation, audio listening, full video playback, or audience experiment was performed. No tests/build/lint/formatter or shared whole-suite command ran.
- Empirical effects remain unresolved and optional: joke multiplication; callback memory/optimal delay; three-beat audience effect; 2D view-reference superiority over texture; crowd choreography/cut-order effect; general perspective/blur/grain/light-wrap recipe success; sponsor integration/material perceptual superiority; silence/music impact; platform opener/loop performance. They must not be scored as evidence-bound measured guarantees.
- Other existing source limitations are not blanket closed: 01 explanation-format taxonomy; 02 full act/journey comparison; 05 metaphor/identity-reading generalization; 07 reverse-shot matching and exact reflection reproduction; 08 motion-graphics app equivalence/localization guarantees; 16 individual engines/open-loop memory/retention effects; 19 fluid/skin physical-perceptual effects and real advertising law; 22 locale/voice and endpoint/real listening success; 23 detailed texture/audio effect claims and desktop fallback catalog; 27 lens-breathing/stabilization/acceleration causes. Retained checks against supplied briefs are not evidence of universal effects. Upstream ArtCraft catalog is another owner's finding; no shared/foreign file edited.
- Canonical-source request for leader only: add Culhane exact rendition identity and narrow L387 / L447-449 bindings to sources.md; update stale module support rows for 17/20/21 to point to these current bounded bindings and explicit optional unsupported comparisons; add Blender 4.2 Shadow Catcher versioned contract/scope. Do not mark entire modules source-confirmed. The immutable current sources.md was not edited by F1.
- Integration conflict outside ownership remains leader/other-owner responsibility: orchestrating-video-preproduction/references/stage-execution.md fit-first finding. F1 corrected only its own consumer.
- Shared metadata/package2.10, manifest, README, CHANGELOG, canonical sources.md, combined ledger, runner/parser and frozen61 were not edited by this work. No commits/push/reset, installation/auth/config changes, remote create/deploy/publish, uploads, paid generation or identity training were performed.
