# creative-production 크래프트 브릿지 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development. Steps use checkbox (`- [ ]`) syntax.

**Goal:** 총괄이 단계별 크래프트 참조를 인계 묶음에 실어 담당 경로와 무관하게 닿게 하고, 영상 일부 작업까지 입구를 넓혀 논스톱 제작을 실제 에이전트로 확인한다.

**Architecture:** `craft-bridge.csv`(단계×조건→참조)를 Step 4에서만 읽고 `craft_refs`로 넘긴다. frontmatter 설명 확장. 모델을 호출하는 시험 도구는 pytest 밖에 두고 케이스 파일만 오프라인 검사한다.

**Tech Stack:** Python 3.10+ 표준 라이브러리, pytest, Markdown/CSV, `pi` CLI(시험 실행만).

**Spec:** `docs/superpowers/specs/2026-11-20-creative-production-craft-bridge-design.md`

## Global Constraints
- `routing.csv` 행 추가·변경 금지. `routing_regression.py` 79케이스 0 실패, 출력이 main과 같아야 한다(frontier 단어 줄 제외).
- frontier 단어 증가 ≤ 60(`routing_regression.py`가 보고하는 값 기준).
- 비영상 제외 목록(standalone writing, social posts, standalone images, ordinary design, application development, audio-only)을 설명에 유지한다.
- 실행·비용·게시 규칙 변경 금지. 새 스키마·원장 필드 금지(`craft_refs`는 인계 패킷의 선택 목록일 뿐).
- `--no-verify` 금지, push 금지, `.superpowers` 스테이징 금지.

## Review Focus
1. 브릿지 표가 실제 앵커가 없는 `#od-…`를 가리킴 → Task 1 `test_bridge_refs_resolve`
2. 흡수 참조 하나가 표에서 빠짐 → Task 1 `test_bridge_covers_absorbed_refs`
3. 설명 확장이 제외 목록을 지움 → Task 2 `test_description_keeps_exclusions`
4. frontier 급증 → Task 2 `test_frontier_growth_bounded`
5. 시험 케이스 파일 오타로 기대 경로가 존재하지 않음 → Task 3 `test_probe_cases_valid`

---

### Task 1: 크래프트 브릿지 표와 Step 4 연결
**Files:** Create `creative-production/references/craft-bridge.csv`, `scripts/test_craft_bridge.py`; Modify `creative-production/SKILL.md`(Step 4 한 문장), `creative-production/references/skill-map.md`(링크 한 줄), `video-production-assets/references/contract-core.md`(worker handoff에 `craft_refs` 선택 필드 한 줄)
- [ ] RED 테스트: `test_bridge_columns`(헤더 정확히 `stage,when,craft_ref,note`), `test_bridge_stage_vocab`(S00–S12 또는 `S04·S07`처럼 `·`로 묶은 조합만), `test_bridge_refs_resolve`(경로 파일 존재, 앵커가 있으면 대상 파일에 `{#앵커}` 또는 해당 제목 슬러그 존재), `test_bridge_covers_absorbed_refs`(08a, 09a, 11a, 19a, 23a, 29a, 33-motion-style-library, still-motion-recipes, `30-marketing-story-craft.md#od-openmotion-ad-script` 모두 포함), `test_bridge_row_cap`(≤40), `test_step4_links_bridge`(SKILL.md Step 4 절 안에 `craft-bridge.csv` 링크와 `craft_refs` 문자열), 오염 시 실패 확인 1건.
- [ ] 표 작성: 각 행의 `when`은 실제 참조의 쓰는 곳에 근거. 스틸 경로 조건(사진·삽화만으로 만드는 제품/세일 영상)에서 19a, 23a, still-motion-recipes가 걸리게 한다.
- [ ] 전체 pytest, routing_regression 확인 후 커밋 `feat(cp): craft bridge table carried in stage handoffs`

### Task 2: 입구 확장과 버전
**Files:** Modify `creative-production/SKILL.md` frontmatter(`description`, `version: 2.6`), 관련 버전 표기가 요구되는 곳(check_versions가 요구하는 경우만); Create `scripts/test_creative_production_entry.py`
- [ ] RED 테스트: `test_description_keeps_exclusions`(제외 6종 문구), `test_description_covers_partial_video_work`(shorts/reels, re-edit or clip, captions/lower thirds, ad/promo video script, motion graphics style 다섯 개념이 설명에 있음), `test_frontier_growth_bounded`(main 기준 frontier 단어 수를 상수로 고정하고 증가 ≤60).
- [ ] 설명 수정. 기존 형식 유지(영어, 접힌 YAML). 버전 2.6.
- [ ] 전체 pytest, routing_regression, check_versions 후 커밋 `feat(cp): widen entry to partial video work, keep non-video exclusions`

### Task 3: 실제 에이전트 시험 도구와 실행
**Files:** Create `scripts/agent_read_probe.py`, `creative-production/evals/agent-read-probes.json`, `scripts/test_agent_read_probe.py`, `qa/2026-11-20-craft-bridge-probes/`(결과 요약), Modify `qa/2026-11-20-open-design-absorption-validation.md`(절 추가), `CHANGELOG.md`(2.63 항목 보강), `README.md`(한 줄)
- [ ] RED 테스트(오프라인): `test_probe_cases_valid`(id 유일, kind∈{positive,negative,nonstop}, expect_any_read 경로 존재), `test_parse_reads`(고정 JSONL 픽스처에서 read/grep 경로와 최종 답 추출).
- [ ] 도구 구현: `install(tmp)` → 케이스별 `pi` 실행(병렬 ≤5, 타임아웃 900초) → `<out>/<id>.reads.txt`, `<id>.final.md`, `summary.json`(id, kind, opened, pass, reason). 판정: positive = expect_any_read 중 하나 이상 열람; negative = `creative-production/SKILL.md` 미열람; nonstop = 최종 답에 기획·대본·콘티 산출이 모두 있고(키워드 판정 + 결과 보존) 실행 승인 요청이 있으며 생성 완료를 주장하지 않음 — nonstop 판정은 도구가 후보만 표시하고 컨트롤러가 최종 답을 직접 읽어 확정한다.
- [ ] 케이스: 2.63 QA의 p1–p5 프롬프트(p3은 스킬 이름 없이), 음성 3건, 논스톱 1건.
- [ ] 실행(모델 `anthropic/claude-sonnet-5-5`), 결과 요약을 qa 폴더에 커밋. 실패 케이스는 숨기지 않고 기록한다.
- [ ] CHANGELOG·README·QA 기록 갱신, 전체 pytest 후 커밋 `qa(cp): agent read probes for craft bridge and entry`
