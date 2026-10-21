# Skill inventory (leader, 2026-10-16)

Package `contents-production-skills` v2.8, 24 installed skills, entry `creative-production`, support `video-production-assets`.

## A. Package skills, size and structure

`SKILL B` = `SKILL.md` bytes; `refs`/`refB` = bundled reference files and their bytes.

| Skill | ver | SKILL B | refs | refB | bound | acceptance | examples |
|---|---|---|---|---|---|---|---|
| creative-production | 1.3 | 16657 | 7 | 55322 | named-sub-skill | yes | yes |
| topic-demand-selection | 1.0 | 6002 | 0 | 0 | yes | no | no |
| video-production-assets | 1.2 | 13205 | 35 | 378421 | named-sub-skill | no | yes |
| camera-spatial-design | 1.0 | 4093 | 6 | 21686 | named-sub-skill | no | yes |
| camera-motion-reference-analysis | 1.0 | 1904 | 2 | 4826 | named-sub-skill | no | no |
| ai-camera-control | 1.0 | 1822 | 2 | 4489 | named-sub-skill | yes | no |
| blender-previsualization | 2.4 | 3532 | 1 | 3518 | named-sub-skill | no | no |
| orchestrating-video-preproduction | 2.6 | 6952 | 2 | 23094 | named-sub-skill | yes | no |
| developing-video-synopses | 2.4 | 5319 | 1 | 5745 | named-sub-skill | yes | no |
| designing-video-character-sheets | 2.6 | 11025 | 2 | 40775 | named-sub-skill | yes | no |
| designing-character-personas | 1.0 | 8142 | 4 | 13434 | named-sub-skill | no | no |
| storyboarding-video | 2.5 | 7245 | 1 | 6297 | named-sub-skill | yes | no |
| storytelling-with-still-images | 1.0 | 3459 | 0 | 0 | named-sub-skill | no | no |
| recording-production-history | 1.0 | 5498 | 0 | 0 | named-sub-skill | no | no |
| higgsfield-brandkit | 0.17.0 | 14871 | 24 | 111790 | provider | no | no |
| higgsfield-generate | 0.17.0 | 18367 | 15 | 75672 | provider | no | yes |
| higgsfield-marketplace-cards | 0.17.0 | 5953 | 0 | 0 | provider | no | yes |
| higgsfield-product-photoshoot | 0.17.0 | 7363 | 1 | 4625 | provider | no | yes |
| higgsfield-soul-id | 0.17.0 | 4974 | 2 | 1319 | provider | no | no |
| higgsfield-video-explainer | 0.18.0 | 17036 | 1 | 5572 | provider | no | no |
| higgsfield-video-replicate | 0.17.0 | 14371 | 4 | 17481 | provider | yes | yes |
| higgsfield-websites | 0.17.0 | 16747 | 37 | 652849 | provider | no | no |
| higgsfield-youtube-thumbnail | 0.17.0 | 9376 | 3 | 21987 | provider | no | yes |
| community-shorts-stills-pipeline | 1.2 | 2581 | 4 | 26153 | provider | no | no |

Total instruction bytes ≈ 1.68 MB (~420k tokens) if every reference is loaded, a real token-burden finding: a worker that follows every link pays for `higgsfield-websites` (652 KB) and `video-production-assets` (378 KB) alone.

**Observations already evidenced (no book needed):**
- No skill declares a `when-to-use` section as a heading; `topic-demand-selection` is the only one with a `Use whenever…` trigger line, and it has no bundled reference at all.
- 8 skills carry no acceptance/QA criteria in `SKILL.md`: `topic-demand-selection`, `video-production-assets` (delegated to refs), `camera-spatial-design`, `camera-motion-reference-analysis`, `designing-character-personas`, `storytelling-with-still-images`, `recording-production-history`, `blender-previsualization`.
- 4 of 24 skills have zero bundled references: topic-demand-selection, storytelling-with-still-images, recording-production-history, higgsfield-marketplace-cards.

## B. Book-to-module provenance (existing, from `video-production-assets/references/sources.md`)

The package already records a **40-book excerpt pass**: 36 original + 4 added, each mapped by concept and OCR line position. **Scope of that pass is partial by its own statement** ("전권 정독…을 완료했다는 뜻이 아니다", it is not full-book reading).

- 01 Film Lighting is excluded: **no body text** (matches the still-empty stub file found in the corpus).
- 03, 06, 34 have OCR damage; only clean spans used.
- Mapped book IDs feed refs **01-11 and 13 only**.

**Concrete coverage gap (checkable):** refs **12, 14-28** carry no book provenance row: `12-qa`, `14-production-ops`, `15-delivery`, `16-concept-emotion-retention`, `17-genre-comedy`, `18-episodic-series`, `19-brand-product-integration`, `20-visual-mode-ssot`, `21-generated-video-qa-retry`, `22-dialogue-lipsync`, `23-finishing-platform`, `24-production-execution`, `25-reference-video-analysis`, `26-state-causality-continuity`, `27-camera-motion-qa`, `28-film-production-lifecycle`. Whether that is correct (operational topics need no book) or a gap (craft topics do) is what the reading pass must decide per reference.

## B2. Provenance-form inconsistency (evidence: module bytes, this audit)

Three different provenance forms coexist, each with a different level of traceability:

| Form | Modules | Traceability |
|---|---|---|
| `## 근거와 적용 범위` + `자료 ID: <list>` + `sources.md` pointer | 01-10, 11, 12, 13¹, 26 | per-concept source ID and search position |
| `## 근거와 한계` + inline ID list, **no** `sources.md` pointer | 13, 14, 15 | inline statement only; cannot be re-resolved from `sources.md` |
| `자료 ID: 설계 확장` (self-authored extension) | 11, 12, 26 | correctly marked as design extension, not book-derived |
| **no provenance section at all** | **16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 27, 28** | **zero stated basis for craft claims** |

¹ `13-ideation-brand.md` has a `## 근거와 한계` heading with IDs 37-40 inline but is the only module with an inline ID list that does *not* point at `sources.md`.

**Defect (verifiable, read-only):** refs **14-28** make craft claims with no stated basis, and 12 of them have no provenance heading whatsoever. Two are directly contradicted by their content:
- `16-concept-emotion-retention.md` states full concept/emotion/retention craft (concept engines, emotion-memory design, retention architecture, retention diagnosis) and names **no** source, yet its sibling `13-ideation-brand.md` claims IDs 37-40 and `02-story.md` claims 17-36. Emotion theory is the domain of the `감정구조/` books (w4 worklist, 12 works), none of which is cited anywhere. `[INFERENCE]` candidate gap, pending w4 extract.
- `12-qa.md:22` claims `자료 ID: 전체 읽기 가능한 자료의 통합; 검수 규격은 설계 확장` ("integration of all readable sources; the inspection spec is a design extension"). The `검수 규격은 설계 확장` half is honest; the first half is **broader than the recorded evidence**, `sources.md` maps no QA concept to any of the 40 books and the module cites no ID. The content itself (evidence-source separation, blocker classification, stale propagation) is sound self-authored design; only the provenance sentence overstates it. Minimal fix: drop the "통합" half.

`11-ai-handoff.md` and `26-state-causality-continuity.md` are honest: both say `설계 확장`. This is the correct pattern for non-book procedures and should be the standard for the rest.

## C. Corpus size vs. what the package can absorb

| Metric | Value |
|---|---|
| (A) all `.md` under `E:\Book\06_Book` | 1559 |
| (B) book-text `.md` | 1086 |
| unique book works after content-hash dedup | 1073 |
| works assigned for reading this audit | **213 paths = 136 distinct works** (w1 37, w2 16, w3 73, w4 12); 77 redundant paths, 36% of queued read effort |
| works in the package's earlier 40-book pass | 40 (excerpt-level) |
| novel-corpus works (`소설/**`, evidence-only) | 294 |
| excluded non-craft | 231 |

**Rendition effect (measured this audit):** the 1073 distinct-work figure is an upper bound; the same work is stored as multiple renditions (top-level vs `originals/<X>/`, `epub/`, `md/`, `pdf/`) with differing OCR whitespace, which byte-hash dedup misses. Within the reading set, 213 paths collapse to 136 works. Note `originals/시놉시스/` and `originals/콘텐츠_제작/md/` hold the same English screenwriting classics in differing renditions.

## D. Overlap / duplication candidates to verify by reading

| Suspected overlap | Owners | Question |
|---|---|---|
| Character persona vs. character sheet | `designing-character-personas`, `designing-video-character-sheets` | Two owners for one character; routing doc says sheet "consumes" persona, is the boundary stated in both? |
| Camera design vs. camera control vs. camera QA | `camera-spatial-design`, `ai-camera-control`, `camera-motion-reference-analysis`, ref 27 | Four files speak to camera; where is the seam? |
| Still-image video vs. Shorts pipeline | `storytelling-with-still-images`, `community-shorts-stills-pipeline` | Both assemble stills into a video; different output contract? |
| Story ref 02 vs. synopsis skill vs. orchestrating-preproduction | `02-story.md`, `developing-video-synopses`, `orchestrating-video-preproduction` | Three story-level owners. |
| Emotion/retention ref 16 has no book source | `16-concept-emotion-retention.md` | Reading pass must supply or refute a basis. |
