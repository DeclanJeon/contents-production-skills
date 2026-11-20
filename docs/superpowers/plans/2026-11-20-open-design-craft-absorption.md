# open-design 영상 크래프트 흡수 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** open-design 스킬 중 원장에서 `absorb`로 판정한 영상 크래프트를 기존 담당 스킬의 조건부 심화 참조로 각색해 넣고, 출처·고지를 함께 배포하는 패키지 2.63을 만든다.

**Architecture:** 원장 CSV(`status` 열)가 단일 진실 원천이다. 각 작업은 대상 파일 하나에 각색 절을 쓰고, 해당 원장 행을 `planned → absorbed`로 바꾼다. 테스트 하나가 원장과 파일을 대조한다. 라우팅 표와 frontier는 건드리지 않는다.

**Tech Stack:** Python 3.10+ 표준 라이브러리, pytest, Markdown. 원본 조회는 `git ls-remote`와 raw.githubusercontent.com.

**Spec:** `docs/superpowers/specs/2026-11-20-open-design-craft-absorption-design.md` (원장: `docs/superpowers/specs/2026-11-20-open-design-absorption-ledger.csv`)

## Global Constraints

- 흡수 대상 라이선스는 `MIT` 또는 `Apache-2.0`만 허용한다. 원본 저장소의 실제 LICENSE로 확인한다.
- `creative-production/SKILL.md`와 `creative-production/references/routing.csv`는 수정하지 않는다. frontier 약 1,410단어를 유지한다.
- 새 설치형 스킬을 만들지 않는다. `manifest.json`의 `skills` 26개를 유지한다.
- 흡수 파일에 다음 엔진 호출 문자열이 없어야 한다: `openmotion_media_use`, `openmotion_assets_use`, `openmotion_`(도구 호출 형태), `npx hyperframes`, `hyperframes render`.
- 원본 예시 미디어, 템플릿 코드, 바이너리는 들여오지 않는다. 원문을 통째로 붙이지 않고 패키지 말투의 한국어로 다시 쓴다. 수치는 "시작값"으로 표기한다.
- 각색 절 끝에는 정확히 `출처: <repo>@<commit 앞 12자> <slug>` 한 줄을 둔다.
- 실행 수단은 패키지의 기존 레인(remotion, ffmpeg, Blender, 선택된 생성기)과 `policy.md`의 실행 게이트를 가리킨다.
- 버전은 2.63. push와 배포는 하지 않고 로컬 커밋까지만 한다.
- 커밋 훅 `scripts/check_versions.py`를 우회하지 않는다(`--no-verify` 금지).

## Review Focus

1. **원본이 사라졌거나 `blob/main`이 바뀐 항목:** 조회가 404이면 조용히 건너뛰지 않는다. 원장에 `exclude`와 `source unavailable`을 남긴다. → Task 1 `test_unavailable_source_becomes_exclude`
2. **카드에는 MIT라고 나오지만 저장소에 LICENSE가 없는 경우:** 흡수하지 않는다. → Task 1 `test_license_must_match_repo_file`
3. **각색 후에도 엔진 호출이 남은 경우:** 패키지만 설치한 환경에서 실행할 수 없다. → Task 2 `test_no_engine_calls_in_absorbed_files`
4. **설치본에 새 파일·LICENSE가 빠진 경우:** `install_package.install`로 임시 설치한 결과에 새 참조와 `upstream/` 고지가 있어야 한다. → Task 10 `test_installed_pack_contains_absorbed_refs`
5. **원본에 없는 수치나 주장을 지어낸 경우:** 테스트로 잡을 수 없다. 리뷰어가 절마다 원본 SKILL.md와 대조한다(Task 3–9 리뷰 체크).

---

### Task 1: 원장 확정 도구와 원본 고정

**Files:**
- Create: `scripts/open_design_ledger.py`
- Create: `scripts/test_open_design_ledger.py`
- Modify: `docs/superpowers/specs/2026-11-20-open-design-absorption-ledger.csv` (열 추가: `commit, sha256, upstream_license, status`)

**Interfaces:**
- Produces:
  - `parse_source(url: str) -> SourceRef` (`SourceRef(repo: str, ref: str, path: str)`, `ref`는 커밋 해시 또는 `main`/`master`)
  - `resolve_commit(repo: str, ref: str) -> str` (`git ls-remote https://github.com/<repo> <ref>`. 이미 40자 해시면 그대로 반환)
  - `raw_url(ref: SourceRef, commit: str) -> str`
  - `decide(row: dict, fetched: FetchResult) -> dict` (갱신된 행을 돌려준다. `FetchResult(status: int, sha256: str | None, license_id: str | None)`)
  - CLI: `python3 scripts/open_design_ledger.py refresh --cache .cache/open-design` (네트워크 사용. 원본은 git이 무시하는 `.cache/`에 저장)
  - 원장 `status` 값: `planned`(흡수 예정), `absorbed`, `n/a`(exclude·out_of_scope)

- [ ] **Step 1: 실패하는 테스트 작성** — `scripts/test_open_design_ledger.py`
  - `test_parse_pinned_and_main`: `.../blob/709b10f.../library/skills/openmotion-ad-script/SKILL.md` → `repo="nexu-io/openmotion"`, `ref` 40자, `path="library/skills/openmotion-ad-script/SKILL.md"`. `.../blob/main/skills/x/SKILL.md` → `ref="main"`.
  - `test_raw_url`: `raw_url(ref, "abc")`가 `https://raw.githubusercontent.com/nexu-io/openmotion/abc/library/skills/openmotion-ad-script/SKILL.md`와 같다.
  - `test_unavailable_source_becomes_exclude`: `decide({"decision":"absorb",...}, FetchResult(404, None, None))` → `decision=="exclude"`, `reason=="source unavailable"`, `status=="n/a"`.
  - `test_license_must_match_repo_file`: `decide(absorb 행, FetchResult(200, "h", None))` → `exclude`, `reason`에 `"no upstream LICENSE"`가 들어간다. `license_id="MIT"`이면 `status=="planned"`, `sha256=="h"`.
  - `test_ledger_vocabulary`: 실제 원장의 모든 행에서 `decision ∈ {absorb, exclude, out_of_scope}`, `status ∈ {planned, absorbed, n/a}`이고, `absorb ⇔ status ∈ {planned, absorbed}`, `absorb`이면 `upstream_license ∈ {MIT, Apache-2.0}`이고 `commit`은 40자.
- [ ] **Step 2: 실행해 실패 확인** — `python3 -m pytest -q scripts/test_open_design_ledger.py` → ImportError
- [ ] **Step 3: `scripts/open_design_ledger.py` 구현.** LICENSE 판별은 저장소 루트의 `LICENSE`, `LICENSE.md`, `LICENSE.txt`를 순서대로 조회해 첫 줄에서 `MIT`/`Apache License`를 찾는다.
- [ ] **Step 4: `refresh` 실행** 후, `absorb` 행마다 캐시된 원본 SKILL.md를 읽고 `target`을 확정한다. 판정을 바꾸면 `reason`에 이유를 적는다. 특히 hyperframes 계열, dream-loop, design-motion-principles를 확인한다.
- [ ] **Step 5: 테스트 통과 확인** — 같은 명령으로 PASS. 전체 `python3 -m pytest -q scripts`도 통과해야 한다.
- [ ] **Step 6: 커밋** — `git add scripts/open_design_ledger.py scripts/test_open_design_ledger.py docs/superpowers/specs/2026-11-20-open-design-absorption-ledger.csv .gitignore` / `feat(ledger): pin open-design sources and verify licenses`

### Task 2: 출처·고지와 흡수 검사

**Files:**
- Create: `video-production-assets/references/upstream/open-design-provenance.md`
- Create: `video-production-assets/references/upstream/<owner>-<repo>-LICENSE.txt` (`absorb` 행이 있는 저장소마다 하나. Apache 저장소에 NOTICE가 있으면 `-NOTICE.txt`도)
- Create: `scripts/test_open_design_absorption.py`
- Modify: `integrations/package-provenance.md` (새 절 "open-design 크래프트 각색")

**Interfaces:**
- Consumes: Task 1 원장 열
- Produces:
  - `TARGET_PATHS: dict[str, list[str]]`: target → 패키지 기준 파일 목록. `33-motion-style-library`는 색인과 `video-production-assets/references/motion-styles/*.md` glob
    - `30-marketing-story-craft`, `03-screenplay`, `10-evidence`, `06-shots`, `25-reference-video-analysis`, `13-ideation-brand` → 각 기존 파일
    - `08-animation` → `08a-motion-craft.md`, `09-edit` → `09a-short-form-edit-recipes.md`, `19-brand-product-integration` → `19a-product-promo-formulas.md`
    - `23-finishing-platform` → `23a-captions-layout.md`, `11-ai-handoff` → `11a-ai-video-prompting.md`, `29-reference-driven-production` → `29a-template-recreation.md`
    - `storytelling-with-still-images` → `storytelling-with-still-images/references/still-motion-recipes.md`
  - `source_line(row) -> str` = `f"출처: {repo}@{commit[:12]} {slug}"`

- [ ] **Step 1: 실패하는 테스트 작성**
  - `test_absorbed_rows_have_source_line`: `status=="absorbed"`인 행마다 `TARGET_PATHS[target]` 중 한 파일에 `source_line(row)`가 있다.
  - `test_provenance_lists_every_absorb_repo`: `absorb` 저장소마다 provenance 문서에 `https://github.com/<repo>`와 고정 커밋이 있고, LICENSE 사본 파일이 있다.
  - `test_no_engine_calls_in_absorbed_files`: `TARGET_PATHS`의 모든 파일(존재하는 것)에 Global Constraints의 금지 문자열이 없다.
  - `test_absorbed_files_links_resolve`: 그 파일들의 상대 링크가 실제 파일로 해석된다.
  - `test_detects_corruption`: 임시 복사한 원장에서 한 행을 `absorbed`로 바꾸고 출처 줄을 지우면 검사 함수가 그 slug를 실패로 보고한다(오염 시 실패 확인).
- [ ] **Step 2: 실행해 실패 확인** — `python3 -m pytest -q scripts/test_open_design_absorption.py` → provenance·LICENSE 누락으로 FAIL
- [ ] **Step 3: provenance 작성.** im-not-ai provenance 형식을 따른다(원본, 고정 커밋, 확인일, 라이선스, 적용 파일, raw SHA-256 표, 의도적 차이 = 엔진 의존 제거·실행 게이트 치환·예시 미디어 미포함). LICENSE 사본을 넣고, `package-provenance.md`에 이 고지는 각색분에만 적용된다는 절을 추가한다.
- [ ] **Step 4: 테스트 통과 확인** (이 시점에는 `absorbed` 행이 0개라 출처 검사는 빈 집합으로 통과한다)
- [ ] **Step 5: 커밋** — `feat(provenance): open-design upstream notices and absorption checks`

### Tasks 3–9 공통 규칙

- 각 절의 형식:
  ```
  ### <한국어 제목> {#od-<slug>}
  - 쓰는 곳: …
  - 구성·시작값: …
  - 움직임·타이밍: …
  - 피할 것: …
  - 검수: …
  출처: <repo>@<commit12> <slug>
  ```
- 새 파일 맨 위 문단: 언제 여는지, 어느 모듈의 심화인지, 실행은 `policy.md` 게이트와 [24-production-execution](video-production-assets/references/24-production-execution.md)을 따른다는 한 줄, 고지 링크(`upstream/open-design-provenance.md`).
- 분량 상한(설계자 판단): 일반 절 180단어, 모션 스타일 절 120단어, 새 파일 하나당 2,500단어.
- 작업마다 해당 원장 행을 `absorbed`로 바꾼다.
- 단계: ① 원장 행을 `absorbed`로 바꾸고 `test_absorbed_rows_have_source_line` 실행 → FAIL ② 절 작성 ③ 해당 모듈 또는 `module-index.md`에 링크 한 줄 추가 ④ `python3 -m pytest -q scripts` PASS ⑤ 커밋
- 리뷰 체크: 절마다 캐시된 원본과 대조해 지어낸 수치·주장이 없는지, 사실 보호 항목(가격·숫자·후기·보증을 지어내지 않음)이 `10-evidence`와 충돌하지 않는지 확인한다.

### Task 3: 본문 소절 (ad-script 포함)
- Modify: `30-marketing-story-craft.md`(ad-script, growth-teardown), `03-screenplay.md`(presenter-story, editorial-webinar), `10-evidence.md`(step-by-step-tutorial, faceless-explainer), `06-shots.md`(shot-composition), `25-reference-video-analysis.md`(shot-breakdown), `13-ideation-brand.md`(general-video)
- 기존 본문 끝에 `## open-design 각색 절` 소제목을 두고 그 아래에만 추가한다. 링크 추가는 필요 없다.
- ad-script 절에는 원본의 비트 구조(훅 1.5초 이내, 2–5초마다 한 비트, 훅·문제·증명·보상·CTA, CTA는 마지막 2–3초에 하나)와 각도 2–3개 제안 규칙을 반드시 담는다.
- 커밋: `feat(vpa): absorb ad-script and script/evidence craft from open-design`

### Task 4: `08a-motion-craft.md`
- Create: `video-production-assets/references/08a-motion-craft.md` (target `08-animation`의 행 전부)
- Modify: `module-index.md`에 행 추가 — `| 모션 원칙·키프레임·로고 모션·색 움직임·콘티→모션 | [모션 크래프트](08a-motion-craft.md) | 08 템플릿 |`
- 커밋: `feat(vpa): motion craft reference (08a)`

### Task 5: `09a-short-form-edit-recipes.md`
- Create (target `09-edit`), Modify `module-index.md` — `| 편집본→대본·멀티캠·릴스/쇼츠 추출·라이브 클립·비트 싱크 | [숏폼 편집 레시피](09a-short-form-edit-recipes.md) | 09 템플릿 |`
- 커밋: `feat(vpa): short-form edit recipes (09a)`

### Task 6: `19a-product-promo-formulas.md`
- Create (target `19-brand-product-integration`), Modify `module-index.md` — `| 제품 프로모·세일·카운트다운·스펙시트·런칭/기능 데모 영상 공식 | [제품 영상 공식](19a-product-promo-formulas.md) | assets/product-ssot-template.md |`
- 커밋: `feat(vpa): product promo formulas (19a)`

### Task 7: `23a-captions-layout.md` + `11a-ai-video-prompting.md`
- Create 두 파일, Modify `module-index.md` 두 행
  - `| 자막 스타일·이중 언어 자막·비율별 레이아웃·하단 자막·커버 | [자막·레이아웃](23a-captions-layout.md) | — |`
  - `| Seedance식 지시·영상→슈퍼프롬프트·샷크래프트·루프 영상 | [AI 영상 지시법](11a-ai-video-prompting.md) | 11 템플릿 |`
- 커밋: `feat(vpa): captions/layout (23a) and AI video prompting (11a)`

### Task 8: `29a-template-recreation.md` + `still-motion-recipes.md`
- Create `video-production-assets/references/29a-template-recreation.md`, `storytelling-with-still-images/references/still-motion-recipes.md`
- Modify `module-index.md` 행 하나 — `| 레퍼런스 재현·템플릿화·디자인 리믹스·토킹헤드 재현 | [템플릿 재현](29a-template-recreation.md) | 기존 29 절 |`
- Modify `storytelling-with-still-images/SKILL.md`에 조건부 링크 한 줄 — "슬라이드쇼·손그림 스토리·기사 삽화 영상 형식이 필요하면 [스틸 모션 레시피](references/still-motion-recipes.md)."
- 커밋: `feat: template recreation (29a) and still-motion recipes`

### Task 9: 모션 스타일 사전 (77개)
- Create: `video-production-assets/references/33-motion-style-library.md` (색인: 계열 표 + 스타일 이름 → 계열 파일 앵커 링크. 스타일 본문은 넣지 않는다)
- Create: `video-production-assets/references/motion-styles/{kinetic-type,explainer-formats,product-commerce,logo-stings,transitions-overlays,posters-backgrounds,handcraft-textures,data-maps}.md`. 계열이 비면 그 파일은 만들지 않는다. 한 파일이 2,500단어를 넘으면 `-2`로 나눈다.
- Modify: `module-index.md` — `| 모션 스타일(키네틱 타이포·설명 형식·커머스·로고 스팅·전환·포스터·수공예 질감·데이터/지도) 선택 | [모션 스타일 사전](33-motion-style-library.md) — 색인만 먼저, 고른 계열 파일만 | — |`
- `test_open_design_absorption.py`에 `test_style_index_links_every_style`를 추가한다. target `33-motion-style-library`의 `absorbed` 행마다 색인에 `#od-<slug>` 링크가 있어야 한다.
- 커밋: `feat(vpa): motion style library (33) from openmotion and iart recipes`

### Task 10: 릴리스 마무리와 검증

**Files:**
- Modify: `scripts/test_open_design_absorption.py` (마지막 두 테스트 추가), `CHANGELOG.md`, `README.md`, `manifest.json`(bump 스크립트로)
- Create: `qa/2026-11-20-open-design-absorption-validation.md`

- [ ] **Step 1: 테스트 추가**
  - `test_no_planned_rows_remain`: 원장에 `status=="planned"`인 행이 0개다.
  - `test_installed_pack_contains_absorbed_refs(tmp_path)`: `install_package.install(tmp_path/"i", repo_root=ROOT, exclude_derived_support=True)` 결과에 `video-production-assets/references/08a-motion-craft.md`, `33-motion-style-library.md`, `upstream/open-design-provenance.md`, 그리고 각 LICENSE 사본이 있다.
- [ ] **Step 2: 전체 실행** — `python3 -m pytest -q scripts` → 모두 PASS(기준선 476 passed + 새 테스트)
- [ ] **Step 3: 라우팅 회귀** — `python3 scripts/routing_regression.py` → 27/27 일치, frontier 단어 수가 기준(약 1,410)과 같다. `git diff --stat main~N -- creative-production/SKILL.md creative-production/references/routing.csv`가 비어 있다.
- [ ] **Step 4: 행동 확인(가능할 때만)** — `scripts/routing_eval.py`로 기존 65케이스를 돌린다. codex 디스패처가 없으면 BLOCKED로 기록하고 통과로 주장하지 않는다. ad-script 요청 1건을 `--stage handoff`로 실행해 `30-marketing-story-craft.md` 열람 여부를 기록한다.
- [ ] **Step 5: 문서** — CHANGELOG `Unreleased`에 흡수 개수(최종 원장 기준), 대상 파일, 라이선스 범위, 제외 기준, 라우팅 무변경을 적는다. README에 한 단락. QA 기록에는 명령, 결과, 한계(행동 평가 미실행 여부, 지어낸 수치는 리뷰로만 확인)를 남긴다.
- [ ] **Step 6: 버전** — `python3 scripts/bump_version.py 2.63` 후 `python3 scripts/check_versions.py` 통과
- [ ] **Step 7: 커밋** — `release: 2.63 open-design video craft absorption` (push 없음)
