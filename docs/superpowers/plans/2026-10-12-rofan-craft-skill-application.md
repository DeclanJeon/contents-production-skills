# Rofan Craft Application Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:executing-plans` or `superpowers:subagent-driven-development` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 저장된 Rofan craft inventory를 새 브리프에 조건부로 적용하되 이미 존재하는 owner 절차와 필드를 재사용하는 문서 변경안을 정의한다.

**Architecture:** 기존 `25-reference-video-analysis.md`의 관찰→메커니즘→의도/대안→새 브리프 요구→QA 전이와 A01–A12 라우팅을 유지한다. 조건별 source-linked 사례·반례·다중 owner walkthrough를 한 선택형 reference에 두고, 필요한 경우만 기존 entry route에서 찾게 한다. 새 스키마·코디네이터·전역 규칙은 만들지 않는다.

**Tech Stack:** Markdown documentation only; existing owner references and templates. No runtime or schema changes.

**Spec:** [`../specs/2026-10-12-rofan-craft-skill-transfer-design.md`](../specs/2026-10-12-rofan-craft-skill-transfer-design.md)

## Global Constraints

- 현재 25번 경로와 A01–A12 owner 라우팅은 이미 존재한다. 보강 대상은 누락된 craft capability가 아니라 사례 검색성·반례·오너 간 worked example이다.
- 57개 inventory 행은 정본에 모두 보존한다. 57은 추가 사례 수의 상한이 아니다.
- 저장된 출처 locator와 관찰 범위를 연결한다. 외부 locator는 plain-text provenance이며 repository 상대 링크인 척하지 않는다.
- The future installed artifact copies skill folders only. The proposed casebank must remain usable without `docs/superpowers` or the original Windows media; the canonical spec is historical design/provenance, not a runtime prerequisite. External document/source locators are optional inline-code provenance. Every mandatory internal link must resolve inside the installed skill folders.
- 활성 brief 문제에 맞는 사례만 선택한다. wide-first, first-touch, 특정 보행 수치, 모든 컷신 30초 제한, 보편적 카메라 규칙을 만들지 않는다.
- 기존 canonical field의 이름과 소유 위치를 그대로 쓴다. alias, 프로젝트 스키마, template field, coordinator/micro-skill/새 SSOT/autopromotion은 추가하지 않는다.
- 사례 reference는 생성 승인·실행·실제 미디어 QA 통과를 대신하지 않는다. endpoint 지원을 확인하지 않았으면 `UNKNOWN`이다.
- Any future scene-specific 3D position, movement, composition, blocking or distance design MUST follow camera-spatial-design and include Blender implementation plus visual inspection, even if the request says “design only”. This document-only plan does none of that; never report missing runtime/blocking state as completed 3D work.
- Catalog labels C/P/O/L/E are local row identifiers, not production/source IDs; source IDs and availability stay separate.
- 원본 영상 경로는 `C:\Users\Declan\Documents\Resources\AI-Rofan-Drama-2026-10-11\videos\urls-batch-mp4-20261011-232345`; 재열기·신규 촬영물 분석은 하지 않는다.
- 원본 의미 JSON 중 일부는 현재 복구 불가하다: D797은 95 shot rows가 성공 기록됐으나 opening excerpt만 복구 가능, D8fba 3.4/5.08MB의 310 dense/686 events 전체 본문과 fde1 dynamic ledger 본문은 접근 불가, C9e26/Db834는 내용 본문 미복구. 이는 부재/삭제가 아니라 접근·복구 한계다. 44개 routed source 전부가 의미상 종결된 것은 아니다.

## Review Focus

- Feet가 보이지 않는 approach — `hidden/out-of-frame` 또는 `unverified`; 06/08 기존 분기.
- 이미 시작된 kiss/contact — 이미 성립된 상태를 수용하고 brief가 요구할 때만 transition 계획.
- Attendants/wardrobe elision/mirror — 06 blocking, 09 실제 elision headers, 11 실제 handoff fields의 분리.
- Magic continuous VFX와 real cut — 실제 boundary만 컷; continuous effect는 21/09의 해당 owner로.
- Fixed gate flare와 rack focus — 07 light와 초점 관찰을 구분; 근거 없으면 미확인.
- Bonus title/video EOS/container tail — 그래픽·편집·실제 파일 판정의 구별.
- Source body unavailable — 보존된 사실만 쓰고 미복구 상세는 unknown.
- Canonical field ownership — 실제 template field 확인; alias/오너 간 field 이동 금지.

---


## 파일 맵 및 책임

| 경로 | 계획 변경 | 책임 |
|---|---|---|
| `video-production-assets/SKILL.md` | Updated existing 25 on-demand row with conditional discovery for explicit saved-case reuse or a matching active brief cue; no always-loaded craft catalog | Implemented. |
| `video-production-assets/references/25-reference-video-analysis.md` | Added the conditional casebank pointer at “브리프에 원리를 옮기는 산출물”; preserved analysis procedure and A01–A12 | Implemented; saved-case application does not imply fresh source analysis. |
| `video-production-assets/references/rofan-craft-examples.md` | Self-contained 57-ID problem index and four worked proposals with bounded evidence, generic mechanism, apply/skip, exact owner destination and actionable QA; internal owner links stay in installed package | Implemented; no copied source table, new schema, or runtime dependency on spec/source media. |
| `video-production-assets/references/06-shots.md` | Added one conditional pointer after step 3 in `## 실행 절차` | Implemented; 06 remains shot/blocking owner. |
| `video-production-assets/references/04-performance.md`, `05-visual.md`, `07-lighting.md`, `08-animation.md`, `09-edit.md`, `11-ai-handoff.md`, `19-brand-product-integration.md`, `20-visual-mode-ssot.md`, `21-generated-video-qa-retry.md`, `26-state-causality-continuity.md` | No file edits or extra pointers. Case-bank entries link to these existing owner procedures only when their active conditions apply | Unchanged; ownership preserved. |
| `README.md`, `CHANGELOG.md`, this plan, and canonical spec | Record implementation status, testing-plan link and historical audit scope without implying broader audit or media quality | Updated. |

**Template ownership 확인 상태:** `04-performance-template.md`, `06-shots-template.md`, `08-animation-template.md`, `09-edit-template.md`, `11-ai-handoff-template.md`, `07-lighting-template.md`, `generated-qa-report-template.md`를 직접 확인했다. 04: `scene/beat`, 인물, 목표, 장애, 상대에게 하는 행동, 숨긴 뜻, 듣기 자극, 전술 전환, 물리 과제. 06: `크기/카메라 위치`, `인물 블로킹`, `시선/축`, `공개 정보`, `관점·감정/구도 의도`, `대안·채택/승인 상태`, `카메라 동작`, `종료 프레임`, `핸들`; cue table columns `Local time (shot seconds)`, `Actor phase / contact / visibility`, `Camera phase`, `Reveal / hold`, `Cut-out → cut-in phase`. 08: `포즈/행동`, `시작 프레임`, `끝 프레임(미포함)`, `행동선/무게`, `스페이싱`, `보조 동작`, `접촉 잠금 / 필요한 발 접촉의 가시 구간 또는 hidden·미확인 제한`. 09 (`assets/09-edit-template.md`) cut columns `cut_id`, `final_start_s`, `final_end_s`, `행동·카메라 변화 / 컷아웃→컷인 phase·state + cue time / 컷 이유`, `reaction/settle hold final start–end s·연속성/검수 상태`; elision columns `cut_id`, `획득 방식: 연속배속/인터벌/몽타주/의도적 생략/미확인`, `실제 경과시간·촬영 구간·간격·공백(근거 위치)`, `생략 전 상태`, `생략 후 상태`, `후속 컷 유지/리셋 조건`. 11: `초기 상태`, `주 행동과 구간`, `카메라`, `조명·룩`, `끝 상태`, `유지 규칙`, `도구 지원 확인`, `생성 길이/편집 길이/핸들`, `검수 실패 위치·수정 변수`, 선택적 상태·변화·보존·후속 유지 fields. 07: scene/shot, 광원 동기, 방향/높이, 경도/확산, 색 의도, 키/필 관계, 배경 분리, 그림자 규칙, 노출 상태, 매칭 주의. Generated QA report: 실제 매체·구간·검사모드·미검증 범위, 발견 표의 타임코드/관찰/관객 영향/심각도/추정 원인/권장 경로/재검수 기준, 판정 상태. 각 필드는 해당 template에만 기록한다.


## 시나리오 범위

**포함:** (1) 새 brief가 approach/stop/stayer 또는 foot evidence 문제를 제기, (2) 이미 진행 중인 intimate/contact beat 및 paired reaction을 특정하지 않고 설명, (3) 여러 owner에 걸친 attendants·wardrobe state elision·mirror reveal, (4) continuous magic/VFX, fixed lighting event와 focus change, title/closing boundary 등 편집 구분이 필요한 brief.

**제외:** 57개 사례를 각 SKILL.md에 상시 내장; 저장자료에 없는 상세 source 복원; 새 영상 읽기/재생/프레임·오디오 분석; endpoint 호출·유료 생성·현재 작업에서의 실제 3D/VFX/렌더/편집; 새 스키마/메타데이터 DB/자동 skill mutation; 모든 미래 brief에 사례 강제; 성과·권리·실제 QA를 사례에서 추론. 이 문서 제한은 미래의 scene-specific 3D 작업에 적용되는 camera-spatial-design + Blender implementation/visual-inspection 요건을 면제하지 않는다.

## 적용 흐름

1. 25번의 기존 brief/analysis route를 따른다. 사용자가 새 reference analysis를 원하면 기존 분석 절차를 수행한다. 이미 저장된 inventory 사례를 적용해 달라는 brief는 fresh source inspection을 선결조건으로 삼지 않는다.
2. brief에서 관찰된 문제 cue를 찾고 새 사례 참조의 조건별 index를 사용한다. 일치 사례가 없으면 비슷한 말을 억지 연결하지 않고 기존 owner 절차로만 진행한다.
3. 선택 사례의 locator·접근성·관찰 vs 해석·미확인 caveat를 확인한다. 검색 가능한 요약과 복원 불가 본문을 구분하고, source content의 미확인을 재구성하지 않는다.
4. 기존 25 chain으로 메커니즘을 brief에 이전한다: 관찰 → 메커니즘 → 의도 효과 및 대안(해석으로 명시) → brief-specific 요구 → 실제 확인 가능한 QA 기대. source timing과 새 계획 timing을 분리한다.
5. 활성 조건에 해당하는 owner만 열고 각 기존 template의 실제 필드로 값을 넘긴다. 06/08/09/11/21 및 필요한 04/07/26 등 owner 책임을 유지한다. 적용되지 않는 분기는 비우거나 기존 N/A/미확인 convention으로 이유를 남긴다.
6. plan-only 결과는 계획으로 둔다. endpoint capability는 조회 전 `UNKNOWN`; 실제 출력 없이는 generated media QA를 주장하지 않는다. 실행이 승인되고 가능할 때 기존 owner가 실제 media를 검사한다.

## 신규 사례 reference 구성 결정

`video-production-assets/references/rofan-craft-examples.md` is implemented as a runtime-self-contained reference. Its 57-ID index gives each row a matching problem cue, bounded observation, generic mechanism, apply/skip condition, existing owner destination and actionable QA. It does not copy the 57-row source table; source/design locators are optional provenance, and unavailable bodies are not runtime prerequisites. Four worked examples plus three concise canonical supporting cues are preserved without broadening inventory into a new schema.

### 네 worked example이 보여야 하는 분기

Worked example minimum payload (exact owner mapping; examples are planned/documentary, not actual generated QA):

- Use the actual five-column 06 cue table: `Local time (shot seconds)`, `Actor phase / contact / visibility`, `Camera phase`, `Reveal / hold`, `Cut-out → cut-in phase`.
- State each owning shot's shot-local duration/range and proposed numeric final-timeline `final_start_s` and `final_end_s` as separate actual fields; keep source locator timing separate from proposed timing. In 09, each cut is its own row; for work/reveal use two rows with each shot's numeric final start/end, never one combined “Work 40 / Reveal 42” value cell.
- Use the canonical 09 columns/headers verbatim. For intentional elision use `획득 방식: 연속배속/인터벌/몽타주/의도적 생략/미확인`, `실제 경과시간·촬영 구간·간격·공백(근거 위치)`, `생략 전 상태`, `생략 후 상태`, `후속 컷 유지/리셋 조건`. For cut rows retain `행동·카메라 변화 / 컷아웃→컷인 phase·state + cue time / 컷 이유` and `reaction/settle hold final start–end s·연속성/검수 상태`.
- Tool capability belongs in 11 `도구 지원 확인` and stays `UNKNOWN` until checked against the selected endpoint. 06 cue/QA prose does not own tool support.
- Identify contact type and visibility independently: visible mouth contact can establish the opener while occluded hand contact stays unknown. Speech or silence remains unknown when audio was not listened to.
- A shot-to-shot elision is an edit gap, not a real-time continuous action. Describe failure as a historical recorded failure only when a saved source supports it; otherwise state a future QA expectation, not a failure.


| 사례 | 저장 원리 locator | positive mechanism | counterexample / limit | 기존 destination |
|---|---|---|---|---|
| Contact/approach | 57-row sources: P01 `03ab`, P08 `d551`, P09 `fb568`, P10 `fd2`, P11–P13 `a600` | Approach/deceleration/stop/settle and paired response only if brief requires; visible contact type and hold | Feet cropped/hidden means no gait proof; mouth-contact opener does not need first-touch setup | 06 five-column cues + 04 performance if character response is needed; 09 only if actual planned cut; 21 only for actual media QA |
| Arrival-stop-stayer | P01 `03ab` and P13 `a600` (departure/remaining actor, not P01 reaction) | Proposed actor arrival/stop then stayer response with shared timebase | P01 records no stayer reaction; proposed stayer response is not source observation | 06 shot/cue; 04 if reaction direction is needed; 09 only if cut |
| Attendants/wardrobe/mirror | P17 `03ab`, O08/O09 `03ab`, O10 `2464`/`9e0` | Separately block work/withdraw and mirror reveal; use explicit intentional edit gap and retain same actor/state as brief specifies | Partial grooming is not continuous dressing; reflection identity/state change cause/time may be unknown | 06 blocking/end frame; 09 exact elision/cut/keep fields; 11 handoff only when needed; 26 only when an existing state condition is active |
| Magic/VFX/cut/light | L03 `430`/`d31`, L05 `9e0`, L06/E08 `a600`/`fee0`/`d31` | Continuous event phases, fixed-geometry light vs sharpness cue, real cut only at actual edit boundary | No rack focus from flare alone; no cut from within-shot candidate phases; no physical magic proof | 06 shot/cue, 07 lighting only when lighting plan is needed, 09 real edit boundary, 11 `도구 지원 확인=UNKNOWN` until actual endpoint check, 21 actual media QA |


## Implementation and validation status

- [x] **1단계 — inventory/source 증거 동기화.** canonical design의 57개 catalog row 전부를 runtime 사례집의 concise case index로 옮겼다(12 camera / 17 performance / 10 object-wardrobe / 9 light-VFX / 9 edit). 57개 적용 cue와 source scope를 유지했고 원본 source를 새로 inspection하지 않았다. **완료:** 모든 ID가 자체 bounded observation / mechanism / apply-skip / owner / QA와 함께 조회되며 미복구 source-body 제한을 표시한다.
- [x] **2단계 — 기존 owner contract를 실제 template에 대조.** `## Template ownership 확인 상태`에 기록된 기존 field ownership을 재사용했다; worked examples use actual 06 five-column cues and 09 canonical cut/elision fields. **완료:** 새로운 alias/필드/owner 이동을 만들지 않았다.
- [x] **3단계 — 사례 reference 작성.** `video-production-assets/references/rofan-craft-examples.md`에 모든 57 ID의 problem-cue/apply-skip/owner index와 네 worked proposals를 작성했다. 선택 entry들은 bounded evidence, generic mechanism, limits/unknowns, QA, 정확한 owner destinations를 포함한다. 원문 관찰표·spec·원본 media를 runtime prerequisite로 복사하지 않았다. **완료:** saved entries self-contained; four examples keep source/new-proposal/actual-QA evidence separate.
- [x] **4단계 — 제한된 진입점 연결.** Existing SKILL.md 25 row, 06 step 3, and 25 brief-transfer section point conditionally to the casebank. **완료:** saved-case reuse does not require fresh source analysis; ordinary briefs are not forced through the 57-case index; 25 analysis route/A01–A12 and owner boundaries remain.
- [x] **5단계 — 참조·범위 검증.** Final copied-package smoke verified all 23 manifest IDs and installed files; exact 57 catalog IDs by group; 384 relative links across 69 Markdown files; changed/canonical tables and field contracts; no broken/out-of-root links. `python scripts/check_versions.py` exited 0 (2.5/23); `python -X utf8 -m pytest -q` exited 0 (258 passed, 1 skipped, 2 warnings, 217 subtests passed). Full evidence and warning identities are in the [test plan](../../implementation/2026-10-12-rofan-craft-skill-test-plan.md) and [`qa/rofan-craft-package-smoke.json`](../../../qa/rofan-craft-package-smoke.json).
- [x] **6단계 — 저장자료만으로 reader exercise + 독립 검토.** Frozen suite의 18개 stateless prompt를 active-owner copied-package context로 실행하고 완전한 응답을 독립 검토했다. Corrected score is 15 PASS / 1 PASS_WITH_CONTEXT_LIMIT / 2 PARTIAL_NOT_MET, 0 guard failures; not all-pass.
- [x] **7단계 — copied-package reader exercise.** Frozen T12 18개 prompt를 current-tree 23-skill package의 active-owner context로 실행·수동 채점했다. 결과는 아래 current-run table과 raw artifact에 기록한다. Reader exercise는 실행 완료됐지만 acceptance는 부분 미충족이다; test plan 및 별도 pytest/version/engineering gates는 독립적으로 판정한다.

## Current copied-package active-owner run (T12)

- **Evidence:** [`qa/rofan-craft-green-final-t12-run.json`](../../../qa/rofan-craft-green-final-t12-run.json), run `green_T12_active_owner_v2`; casebank SHA-256 `cae803553b5858c1d201d69868b7ace1a3210a0cc71d1150ca898e9c5e3fdd1b`. The fresh stateless run used the frozen 18 prompts and scenario-specific active-owner package context. The ordinary-brief negative deliberately omitted the casebank; its separate actual reader-flow check supports non-trigger behavior.
- **Grade:** **15 PASS / 1 PASS_WITH_CONTEXT_LIMIT / 2 PARTIAL_NOT_MET; 0 guard failures. This is not all-pass.** Sixteen active context files across scenarios; no causal comparison or statistical improvement claim.
- **PARTIAL_NOT_MET findings:**

| Scenario | Result / unmet criterion |
|---|---|
| reader 07 — unavailable source body / unlistened audio | Unknown/recovery limits and unlistened audio were handled safely, but output gave generic transfer advice without using the preserved bounded excerpt in a concrete application. |
| composite | Requested six active 09 cut columns were present; the 06 time values were explicitly labeled final timeline, not miscomputed shot-local values. The output omitted the canonical six-column 09 elision row and an explicit separate last-visible-picture/container-tail check. No distinct local-time composite view was supplied. |
Reader 08 passes after complete raw-response review: it includes 06 five-column cues, separate numeric 09 final-time columns and canonical 09 elision fields, the held reveal, and `도구 지원 확인: UNKNOWN` for both W1 and W2.

The conditional handoff field-format robustness gate is **NOT_MET** on reader 07's missing concrete bounded-excerpt application and the composite's missing 09 elision/EOS-tail handoff. Reader 08 passes on full raw review. Keep the two unmet criteria separate from correct 09 cut columns and safe guards. The run contains text plans only: naturalness/variance, actual-media quality, generation, endpoint support, and numeric 3D/Blender verification were **NOT RUN**. Engineering and structural checks completed; exact results and warning identities are in the test plan and package-smoke artifact.

## Independent reader exercise results (saved files only)

This section preserves a historic saved-files-only exercise. It is not the copied-package T12 run or an overall acceptance score; do not combine its individual outcomes with the current 18-scenario grade above.

| Input | Observed reader answer | Source/owner anchors | Result |
|---|---|---|---|
| 1. Approach shot with feet out of frame | Treat approach, spacing reduction, deceleration/stop as only the bounded observation. Full gait/plant is unverified, and a reaction/stayer response is a new proposal rather than the source event. | Spec §P01; `video-production-assets/references/06-shots.md` §6; `video-production-assets/assets/06-shots-template.md` cue row; `08-animation.md` step 5 | PASS |
| 2. Already-established kiss/contact opener | Start in visible mouth contact; do not invent approach/first touch. Hands may be outside frame so hand-contact detail is unknown without negating visible mouth contact. | Spec §P10 and Worked example “접촉 상태”; `04-performance.md` steps 3–5; actual fields shown in worked example | PASS |
| 3. Attendants/costume elision/mirror | Use distinct work and reveal shots with an intentional elision, not continuous realtime. The proposed work shot ends at final 42.0s and the reveal starts at 42.0s, so the output intervals are adjacent; story-time elapsed and any capture gap remain unknown. The proposed final hold is 43.0–44.0s. Do not invent an output gap or elapsed time. Preserve seated posture and brief-specified wardrobe/prop ownership; leave reflection identity unconfirmed without an anchor. | Spec §P17, §O08–O10, Worked example “Attendants·wardrobe elision·mirror reveal”; 06 `인물 블로킹`/`종료 프레임`; 09 exact elision headers and separate `final_start_s`/`final_end_s`; 11 only if a handoff is needed | PASS |
| 4. Magic cup continuous VFX vs real cut | The saved event is one within-shot chain; candidate frames do not create cuts. Plan it as continuous unless an actual edit boundary is chosen; tool support stays `UNKNOWN` in 11 until endpoint check, and 21 QA waits for actual output. | Spec §L06/§E08 and Worked example “Magic object”; 11 `도구 지원 확인`; 09 actual combined cut column; 21 actual-media QA | PASS |
| 5. Fixed gate flare vs rack focus | Held framing with brightness change and flare proves neither a camera move, cut nor focus pull. Differential sharpness is not a rack-focus observation; keep the mechanism unknown. | Spec §L03/L05; `07-lighting.md` procedure; 06 camera owner | PASS |
| 6. Bonus title / video EOS | Apparent title is followed by bonus label/table content, then a later black/gold-star ending. Keep title overlay distinct from its underlying shot; picture EOS and container tail require separate checks on the actual file. | Spec §E05–E08; `09-edit.md` §§18–20; `21-generated-video-qa-retry.md` §§53–63 | PASS |
| 7. Unavailable source body / unlistened audio | Use bounded saved observations; D797 excerpt-only and D8fba/fde1/C9e26/Db834 limitations remain access limits, not absence/deletion. P14 says audio was not listened to, so speech/silence is unknown. | Spec §§“근거, 출처 및 신뢰 범위”, “P14”; `25-reference-video-analysis.md` evidence states | PASS |
| 8. Exact owner fields and actual filled cells | Rechecked the saved worked examples against 09, not just the prose contract: P10 has combined cut cell `continuous existing mouth-contact hold; out/in=N/A; reason=N/A`, `final_start_s=12.0`, `final_end_s=14.0`, hold `13.0–14.0`; arrival has action phases `0–1.0→1.0–1.2→1.2–1.3→1.3–1.5`, final interval `24.0–27.0`, settle `25.3–25.5`, response onset `25.8`, hold `26.0–27.0`; elision has method `의도적 생략`, actual elapsed/capture gap unknown, before/after/keep states filled, separate work-cut row `40–42` and reveal-cut row `42–44` each with `final_start_s` and `final_end_s`, and hold `43–44`. Values reconcile to shot-local offsets; there is no output-time hole, unassigned interval, or claimed story-time duration. `도구 지원 확인` belongs only to 11 and remains `UNKNOWN` until endpoint check. | Spec §P10 owner-field rows; arrival owner-field rows; wardrobe elision owner-field rows; actual `assets/09-edit-template.md` headers; `assets/11-ai-handoff-template.md` | PASS |


### Actual document-only verification record

- **Scope and command:** CWD reported by `pwd`: `C:\Users\Declan\documents\Projects\contents-production-skills`. Ran an inline Bun 1.4.3 JavaScript document smoke (`functions.eval`) over `README.md`, this plan, and the final spec; also read `video-production-assets/assets/09-edit-template.md` to compare canonical cut fields. It checks inline-code-excluded relative links/fragments, each Markdown table’s header/delimiter and uniform cell widths, 57 catalog IDs, 09 field/cut-row mapping, source boundary facts, casebank/package boundary wording, and the eight saved-file reader answers. No installed Markdown AST/parser package was available (`markdown-it`, `marked`, `remark-parse`, `commonmark`, `micromark` unresolved); no dependency was installed. This is a syntax/contract smoke, not a claim of full CommonMark parser conformance. The proposed case-bank link remains inline code, not a broken link to an uncreated file; the future copy-package exercise is planned only and was not run.
- **Raw smoke output:**
  ```text
  RELATIVE_LINKS=39; FAILURES=0
  MARKDOWN_TABLES=24; BAD_DELIMITER_OR_WIDTH=0; TABLE_PROSE_BOUNDARY=OK
  CATALOG_ROWS=57; UNIQUE=57; GROUPS={"C":12,"P":17,"O":10,"L":9,"E":9}
  09_TEMPLATE_AND_WORKED_HEADER=OK
  09_WARDROBE_ROWS=W1/40.0/42.0;W2/42.0/44.0;ADJACENT=YES; HOLD=43.0-44.0; STORY_TIME=UNKNOWN
  06_FIVE_COLUMN_CUE_DELIMITER=OK
  SOURCE_BOUNDARY_FACTS=7/7 PASS
  CASEBANK_COPY_BOUNDARY=SPECIFIED; COPY_PACKAGE_READER_EXERCISE=PLANNED_NOT_RUN
  READER_EXERCISES=8/8 PASS
  README_SPEC_POINTER=OK
  TIMING_ARITHMETIC=PASS
  EDIT_ARTIFACTS=NONE
  ERRORS=0
  none
  ```
**Timeline arithmetic output (separate inline Bun eval):**
```text
ARRIVAL_LOCAL_TO_FINAL=OK
CONTACT_LOCAL_TO_FINAL=OK
ELISION_CUT_ADJACENCY_AND_HOLD=OK
ALL_TIMING_ARITHMETIC=PASS
```
- **Reader status:** all eight entries above are saved-file-only reasoning. No footage was reopened; no audio was listened to; no endpoint, generation, runtime, or real-media QA was run.
- Scenario run은 실제 scenario request를 보내지 않는다. reader exercise는 저장된 파일로 수작업 검토이며 생성/endpoint/미디어 검사와 별도다.
- Fresh footage analysis와 real-media QA는 이 범위에서 수행하지 않는다. 훗날 media QA를 승인받아 수행해도 실제 파일 및 도구가 있어야 하며 부재 시 hard/soft UNKNOWN을 명확히 표시한다.
- 문서 변경은 사용자 위임 범위 내에서 완료하되, operating/installed skill files, runtime code, versions, schemas, media/history execution 또는 destructive git operation은 다루지 않는다.
