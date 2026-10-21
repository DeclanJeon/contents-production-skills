# Peer remediation: verification against the corrected anchors

Scope: read-only verification of the edits made by the single-writer pane `w1:pC` (gate opened when its status flipped `working` -> `idle` at `state_change_seq` 835, after the frozen baseline arm completed 61/61).

## Gate and sequence

- The audit signalled `w1:pC` by pane prompt to HOLD all skill edits while the baseline arm ran, because `codex exec --sandbox read-only` sessions read the live tree and later prompts would otherwise see edited bytes.
- The baseline arm completed and archived before any post-change run (61 result files copied to the scratch `baseline/` dir; the live result dir was then cleared).
- The peer's edits then landed; `git diff --numstat` counted **22 files**, all forward additions except three one-line rewrites and one README/manifest touch.

## Tree state at verification

- HEAD `fed9275`; `git status --porcelain` = 22 modified files + untracked `qa/2026-10-16-corpus-audit/`.
- `python scripts/check_versions.py` -> `version check OK: package 2.8, 24 skill(s) consistent`.
- `python -X utf8 -m pytest -q --basetemp=...pytest-omp-cps5` (baseline, pre-gate) -> `254 passed, 8 skipped, 214 subtests passed`.
- `python -X utf8 -m pytest -q --basetemp=...pytest-omp-cps6` (post-gate) -> `254 passed, 8 skipped, 214 subtests passed`. No regression.

## Anchor-by-anchor check

Every anchor this audit corrected after first-hand reads is used in the landed edits. Checked by reading the added diff lines.

| Planned patch | Corrected anchor (audit) | Used in the edit? | Evidence (added line) |
|---|---|---|---|
| P1 `12-qa.md` | drop the `전체 읽기 가능한 자료의 통합` overstatement, state excerpt-level scope | yes | ``sources.md`는 첨부 자료를 발췌 탐색으로만 기록하며 전권 정독이 아니다` |
| P2 `16-concept-emotion-retention.md` | add a stated-basis section | yes | `## 근거와 적용 범위` with `자료 ID: 설계 확장` plus the READ-PARTIAL book list |
| P2b `16-...md` | Lazarus spot-check inserted between the pattern and honesty blocks | yes | `### 감정 전환의 평가 점검` with `(Lazarus, 자료 42, 발췌 탐색)` |
| P3 `22-dialogue-lipsync.md` | Habermas L351-359, worded as context-sensitive congruence (not a universal voice-identity rule) | yes | `맥락과 맞지 않는 정서적 이탈은 ... 정합성을 맞춘다 ... 정서 일치를 보장하는 규칙은 아니다 (자료 24, READ-PARTIAL...)` |
| P4 `07-lighting.md` | Alton L187-189, indicator-only, "prefigure" dropped | yes | `벽에 드리운 막대 그림자로도 감옥을 읽히게 할 수 있다 ... 선택 가능한 표현이지 모든 장면의 의무 규칙은 아니다 (자료 02, READ-PARTIAL...)` |
| P5 `13-ideation-brand.md` | segmentation method gap stated, Kotler excerpt basis | yes | `관객 세분화가 필요하면 ... 인구통계 라벨만으로 동일한 요구를 가정하지 않는다` plus `44: 마케팅 세분화 변수(발췌 탐색)` |
| P6 `marketing-source-adaptation.md` | Dunford L1135-1140 positioning relative to buyer alternatives | yes | `identify the competitive alternatives buyers actually use as their comparison yardstick ... (Dunford...)` |
| P7 `sources.md` | IDs 41-44 with the corrected OCR lines | yes | rows 41 `974, 1006-1008, 1064, 2404-2406`, 42 `1429, 2342-2346, 3841-3845, 4319-4323, 5193`, 43 `1135-1140, 1167-1171`, 44 `16831-16839, 16871-16895, 17124-17165` |

Also landed, beyond the planned patch set: `sources.md` row 02 Alton OCR lines `41, 47, 51, 187-189`, row 24 Habermas `77, 79, 81, 351-359`, row 30 Lo Duca `77, 81, 83, 375-376`; `creative-production/references/marketing-source-adaptation.md` carries the peer's structured ad-variation section (Saatchi/Dunford-adjacent) and the source IDs 41-44 with per-file SHA-256.

## Verdict

- Every corrected anchor is used. No stale anchor (Lo Duca L25 front matter, Alton "prefigure") survives.
- No edit was made to the frozen prompt bytes: `prompts.sha256` re-verified MATCH against the on-disk `baseline-prompts.md`, `baseline-prompts-exact.md`, `baseline-matrix.md`, `baseline-matrix-vpa.md` after the peer's edits (those files are inside the untracked audit dir the peer did not write).
- The `marketing-source-adaptation.md` §6 addition the handoff asked to preserve is still present and grew from 24 to the full structured section.
