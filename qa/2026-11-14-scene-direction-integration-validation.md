# 씬·컷 통합 — C2 최종 결과와 C1 이력

**현재: 남은 소스 구현 반영 / 행동 검증 부분 완료 / 전체 수락·기본 적용 HOLD.**

- 컷별 열 구획 확대 보기와 실제 오너/공통 본문, 첫→중간→끝 상태·카메라/발화·소리/효과·자원/검수·실제 VISUAL/AUDIO 역대조를 기존 보드에 연결했다. 10개 Markdown,131줄 추가/6줄 삭제이며 런타임/스키마/기존 정본·승인 체계는 유지했다.
- C2 실제8회: **6 PASS /2 INCONCLUSIVE**. 원래43관찰은31 PASS/12 INCONCLUSIVE, 별도X1은6 PASS/2 INCONCLUSIVE. 전체 보드의 완료3종에서 통합 조회를 확인했고3대조군은 범위를 보존했다. SD09·SD14의24초 장면은10분 제한에 잘려 미검증이다. 부모 작성자 판정이며 새 독립 리뷰가 아니다.
- 총 **32회 시도=응답완료30+시간초과2**, 남은 허가0, 자동재시도0. 중단 뒤 원문/해시·프로필을 보존하고 미실행 과제만 이어갔다. 완료/실패 표본 재실행·기한/모델 변경은 없다.
- 최신 회귀 **737 passed/4 skipped/525 subtests(56.35s)**, package2.34/22 버전·whitespace·기준판/C1/C2/원리뷰149개 보존 검사 성공. 정적/무결성 통과는 내용·실제 미디어·사용자 수락의 증명이 아니다.
- C1의 SD09 위치 모순/독립 FAIL은 보존한다. C2에 역대조를 구현했지만 해당 사례가 중단돼 새 출력의 수정 통과를 주장하지 않는다. 추가 독립 리뷰·커밋/통합·설치/동기화·미디어 실행/게시도 하지 않았다.

현재 상세: [C2 최종 요약](scene-direction-integration/c2-final-summary.md) · [구현 대응표](scene-direction-integration/c2-implementation-coverage.md) · [별도 수락 기준](scene-direction-integration/expanded-shot-acceptance.md) · [첫 중단/계속 기록](scene-direction-integration/c2-interruption.md).

## 아래 기록의 시점 — C1 종료 당시 이력

이하의 3문서·24/26건·7 PASS/1 FAIL·미구현 B 표현은 **C1 당시**의 범위/판정으로 보존한 것이다. 현재 C2의 전체 변경/결과와 혼합하지 않는다. C1의 독립 채택 관찰41 PASS/2 FAIL은 한 SD09 결함의 두 기준 영향이며, 원래 작성자42 PASS/1 INCONCLUSIVE도 별도로 남긴다.

## 1. 후보와 실제 변경

- 격리 작업 공간: `/home/declan/.cache/pi-worktrees/scene-direction-integration-20261114`
- branch: `feat/scene-direction-integration-20261114`, BASE/현재 HEAD `0e1d9f343fa2bec0d00421ed2cf4488abd41888c`.
- 커밋은 승인되지 않아 범위가 비어 있다. **실제 리뷰 대상은 HEAD의 빈 diff가 아닌 미커밋 세 문서와 평가/설계 자료**다.
- 생산 소스: **3문서, 28줄 추가/3줄 삭제**. package 2.34/22 skills, runtime·schema 1.1·카메라/ID·상태·승인·의존/마스터·파생/ZIP v5.1 투영을 바꾸지 않았다.

| 파일 | 변경 |
|---|---|
| `video-production-assets/references/11-ai-handoff.md` | 기존 04/22/캐릭터 입력을 실제 AUDIO의 화자 고정 앵커/발화 Performance로 투영하고 역대조하는 조건부 절차 |
| `video-production-assets/assets/11-ai-handoff-template.md` | 실제 화자/입력 위치·고정 음성 문장·발화 행·소비 대조/미해결·N/A 슬롯 |
| `creative-production/references/storyboard-timing-to-prompt.md` | 음성/연기 내용을 실제 직렬화 대상에 포함하고 11의 단일 절차로 연결 |

새 감독 스킬·정본·제작 JSON 필드/enum·validator profile·CLI/의미 컴파일러·실행/평가 엔진·런타임 의존성은 추가하지 않았다. `.superpowers`의 JS는 고정된 native 요청을 보존하는 이번 QA 실행 기록이고, shell은 저장 근거 무결성 확인용이며 자동 내용 채점기가 아니다.

## 2. 승인 범위와 평가 자료

Native 구현·한 번의 fresh-context 최종 리뷰, 같은 모델로 최대 26건 텍스트 과제가 승인됐다. E1 실패 미재현 뒤 사용자 승인을 받아 E2 아이디어 출발/독립 Performance 입력을 추가했다. 자동 재시도 0, 다른 CLI/공급자·미디어·설치·Git 통합 권한으로 확대하지 않았다.

- 모델: 실제 영수증의 `openai-codex/gpt-6.1-sol`, high / fresh / 각 600000ms.
- baseline: BASE의 텍스트 **215파일 / 1,873,751 bytes**. C1은 같은 목록 **1,878,321 bytes**, 세 문서만 다르다. 읽기 전용 모드 비트와 정책은 보안 샌드박스가 아니다.
- 사용자 입력/기준은 생성 전에 동결. 생성자에는 `user_request`와 `supplied_context`, 소스 조회 지시만 전달했다. rubric·검토 카드·다른 응답은 숨겼다.
- baseline 전량이 후보 편집보다 먼저다. 최종은 역순, 한 번에 최대 2명의 읽기 전용 children으로 수집했다. 엄밀한 조건 교차/통계 실험이 아니다.
- 실제 **24/26건**, 남은 2건 미사용. 한 사례에는 자료를 읽는 여러 모델 요청이 포함될 수 있으므로 API 요청 수와 같지 않다.
- 실제 도구 **526개 read**, 모두 해당 고정 소스 범위 안. 범위 위반/소스 변조는 관찰되지 않았다. 생성 결과·실패/미검사는 덮거나 성공 표본으로 재추출하지 않았다.
- 사례 runtime 보고 비용 합계 **약 USD 8.3609984**. 청구서 대조·고정 provider 출력 한도·부모/최종 리뷰 포함 전체 작업 비용은 미확인이다.

고정 입력: `qa/scene-direction-integration/cases.json`, `open-brief-cases.json`.
원시 근거 루트: `.superpowers/sdd/2026-11-14-scene-direction-integration/`; E2는 그 아래 `epoch-e2/`.
원본 웹툰 픽셀/대사/캐릭터/특정 배열을 평가 자산에 복사하지 않았다.

## 3. 기준판·형성·최종을 분리한 결과

### 현재 채택한 독립 판정

최종 **7 PASS / 1 FAIL, 관찰 41 PASS / 2 FAIL**이다. SD09-O1과 O3은 동일한 열쇠 위치 결함의 두 기준 영향이며, 별개 결함 두 개가 아니다. 음성 인계 SD09-O5/SD14-O5의 FAIL→PASS는 독립 리뷰도 확인했다.

전이: **38 PASS→PASS / 2 FAIL→PASS / 2 PASS→FAIL / 1 INCONCLUSIVE→PASS**. 원래 SD14-O2 의문을 다른 새 이야기로 해결한 것으로 세지 않는다. SD09의 새 실패가 C1 패치 때문에 생겼다는 인과까지 입증한 것은 아니다.

원시 응답과 기존 작성자 카드는 그대로 두고, 독립 판정을 `epoch-e2/final-c1-adjudicated-reviews/` 및 `final-c1-adjudicated-score-summary.json`에 별도 저장했다. 부모도 인용된 원문·보드 계약을 재확인한 뒤 이를 채택했다. 전체 후보를 무회귀·전부 통과로 표현하지 않는다.

### 작성자 판정 기록 — 독립 리뷰 전, 변경 없이 보존

아래는 **작성자의 전체 응답 의미 검토**다. 독립 판정이 아니며 셀 존재/문자 수/grep/JSON parse/자체 점수로 대체하지 않았다. 무결성 helper는 이미 판정한 카드·입력·출력/소스 해시와 실제 실행 범위만 확인한다.

| 단계 | 사례 | 사례 판정 | 관찰 판정 |
|---|---:|---|---|
| E1 baseline | 8 | 7 PASS / 1 INCONCLUSIVE | 35 PASS / 1 INCONCLUSIVE |
| E2 baseline | 6 | 4 PASS / 2 FAIL | 33 PASS / 2 FAIL / 1 INCONCLUSIVE |
| C1 formative | 2 | 2 PASS | 12 PASS |
| C1 final | 8 | **7 PASS / 1 INCONCLUSIVE** | **42 PASS / 1 INCONCLUSIVE** |

서로 다른 단계의 점수를 합산해 성공률이나 독립 표본 수를 늘리지 않는다. E1 SD06은 원본에 독립 대사별 Performance가 없어 INCONCLUSIVE로 유지한다. E2 SD13의 공급 PERF_PACKET은 이 입력 공백을 다른 과제에서 보완한 것이지 E1의 과거 판정을 고친 것이 아니다.

### 작성자 최종 8쌍 — 리뷰 전 판정 기록

| 과제 | 기준판 → C1 최종 | 의미 |
|---|---|---|
| SD03 | PASS → PASS | 완전 no_audio·의도적 정지 hold/원테이크 보호 |
| SD08 | PASS → PASS | generic 12칸의 내용 부족 지적·구조≠품질·QA-only 범위 보호 |
| SD09 | FAIL → **INCONCLUSIVE** | O5 음성 인계는 PASS. O1의 단일 패널 표면 표현은 미확인 |
| SD10 | PASS → PASS | 무언 능력 조건/1초 접촉·온기 소진·집 손실/떨림 잔류 |
| SD11 | PASS → PASS | 한 얼굴/화면 밖 화자·호칭 공개/반응·고정 음성/이번 연기 |
| SD12 | PASS → PASS | 3타격 신호→몸 이완→얼굴 공개, 같은 시간 basis의 실제 소리 |
| SD13 | PASS → PASS | 12샷/24패널·6발화와 공급 전술/강세/쉼·압력/숨을 실제 3작업에 유지 |
| SD14 | FAIL → PASS | O5 고정 음성/숨 인계 보존. 새 허구의 내부 인과 확인이며 옛 설정 의문 해결로는 세지 않음 |

관찰 전이: **39 PASS→PASS / 2 FAIL→PASS / 1 PASS→INCONCLUSIVE / 1 INCONCLUSIVE→PASS**.

### 확정된 제한 개선

- SD09-O5 baseline `epoch-e2/baseline-outputs/SD09.md:28–33`의 인물 음성이 실제 AUDIO `:319–336`에서 부분 누락됐다. C1 final `final-c1-outputs/SD09.md:56–67`의 앵커가 실제 AUDIO `:279–295`에 들어간다. 중간 음역/건조 음색·자음/말끝과 높은 쪽 음역/얇고 거친 음색·숨/연결 말끝 및 각 발화 연기가 실제 문장으로 남는다.
- SD14-O5 baseline `baseline-outputs/SD14.md:30–35,79–87`의 음성·숨이 실제 요청문 `:209–247`에서 일부 사라졌다. C1 final `final-c1-outputs/SD14.md:31–35,126–130`의 앵커/3개 연기가 실제 AUDIO `:350–386`에 보존된다.
- 형성 2건에서도 같은 보존을 관찰했지만 최종 8쌍에 섞지 않았다. 서로 다른 창작 이야기/seed의 한 표본 비교이며 일반 창작력·통계적 안정성·실제 음성/연기 품질 향상의 증거가 아니다.

### 남은 판정/검토 문제

1. **최종 SD09-O1/O3 — Important, C1에서 미해결:** `final-c1-outputs/SD09.md:188` P08은 “열쇠는 바닥에 놓임”, SH03(:157)과 실제 요청문(:273)은 접수대 위 열쇠다. 독립 이미지 지시를 받는 실행자에게 상판으로 추측하게 하면 안 되며, 바닥 제작이면 설명 없는 이동/복귀가 생긴다. 독립 리뷰의 O1/O3 FAIL을 채택한다. 보고/판정은 정정했지만 원시 응답 자체를 수정·재추출하지 않았고 결함을 해결했다고 주장하지 않는다. O5 음성 인계 PASS는 별개다.
2. **기준판 SD14-O2:** 관계 기억을 모두 쓴 류의 현재 관계 인식이 불분명했다. C1은 다른 인물/규칙을 만든 유효한 새 장면이다. 옛 의문을 수정했다고 주장하지 않는다.
3. **전체 B 범위:** 승인 설계 §9의 새 샷별 열 구획 확대 보기 템플릿과 다른 전문 오너 개편은 C1에 없다. 승인된 E2의 “관찰된 실패만 최소 수정”에 따라 기존 ID 연결 표/오너를 보존했다. 기존 표본이 풍부한 내용을 만든 것과 원래 B 설계의 모든 명시적 구조를 구현한 것은 다르다. Tasks 3/4/5/6/8을 새로 구현 완료로 표시하지 않았고, 독립 리뷰도 이 명시적 구조가 미구현이라고 확인했다. 수정 최소화는 원래 승인 산출물 면제가 아니므로 미완료 작업과 HOLD를 유지한다.

## 4. 호환성·증거 검사

동결 C1에서 기록된 전체 회귀:

```text
python3 scripts/check_versions.py
  version check OK: package 2.34, 22 skill(s) consistent
python3 -m pytest -q
  737 passed, 4 skipped, 525 subtests passed
  latest log: epoch-e2/post-review-c1-pytest.log (48.68s)
  reviewed-stage log: epoch-e2/pre-review-c1-pytest.log (50.96s)
  frozen-stage log: epoch-e2/final-c1-pytest.log
 git -c core.whitespace=cr-at-eol diff --check
  no errors
```

이 수치는 기존 Python 구조/호환성 회귀다. 생성된 자연어 보드에 validator를 실행했거나 의미/가독성·실제 미디어가 통과했다는 뜻이 아니다. Linux에서의 skip을 실제 Windows/macOS 검증으로 세지 않는다. 새로운 프로덕션 런타임 코드는 없다.

- baseline 근거: `verify-baseline-evidence.sh`.
- 형성 근거: `verify-c1-formative-evidence.sh`.
- 최종 작성자 근거: `verify-final-c1-evidence.sh`.
- 독립 판정 반영/원본 보존 근거: `verify-post-review-evidence.sh`; 실제 로그 `epoch-e2/post-review-evidence.log`. 이는 실패가 없어졌다는 자동 판정이 아니라 **7 PASS/1 FAIL의 올바른 보존**을 확인한다.
- frozen source/dispatch/입력: `epoch-e2/final-c1-source-manifest.json`, `final-c1-freeze.json`, `final-c1-inputs/`, `final-c1-dispatch/`.
- 실제 원문/영수증: `final-c1-outputs/`, `final-c1-workflow-receipt.json`, `final-c1-status.json`, `final-c1-execution-audit.json`.
- 작성자 판정: `final-c1-reviews/`, `final-c1-author-score-summary.json` (원본 보존).
- 채택 독립 판정: `final-c1-adjudicated-reviews/`, `final-c1-adjudicated-score-summary.json`.
- 리뷰 당시 문서 버전: `reviewed-c1-documents-manifest.json`과 `reviewed-c1-documents/`. 원래 review bundle의 해시는 이 보존본에 연결하며 이전 manifest를 새 보고서 내용으로 덮지 않았다.

## 5. 독립 리뷰 — 완료, 1회 사용

[리뷰 원문](2026-11-14-scene-direction-integration-independent-review.md)은 native 응답과 바이트 동일하게 보존했다. run `771311aa-4246-45ff-8df6-ca6534b33854`, 실제 `openai-codex/gpt-6.1-sol` / high / fresh / 600000ms, 소요 471855ms. runtime 보고 비용 약 USD 1.4126382는 사례 비용/부모 비용과 별도이며 청구서 검증은 아니다.

- A — 제한적 세 문서 음성 수리는 타당, 목표 두 관찰의 개선 확인. 세 변경 문서 자체의 차단 결함 없음.
- B — 원래 전체 B는 미완료. **Ready to merge: No**, 전체 후보/기본 적용 HOLD.
- Important 1: SD09 소품 위치 결함과 O1/O3 재판정. 보고/채택 판정을 정정했으며 원시 결함은 보존/미해결.
- Important 2: §9 샷별 열 구획 확대 보기 미구현. 원래 B 완료로 처리하지 않음.
- Critical 없음, 별도 Minor 없음.

리뷰어는 8쌍의 입력·기준판/최종 응답 전문 16개와 43개 기준을 대조했다. 추가 E1의 여섯 응답은 과거 대조이며 후보 재실행이 아니다. 형성 2건은 별도 독립 의미 재채점하지 않았다. 현재 상위 정본 변경 뒤 종속물 갱신/승인 보존 동작, 후보 5/20/30초 전체 경로는 검증되지 않았다.

부모가 실제 기록을 확인했다: 54 read / 7 읽기 전용 bash / 1 ls / 12 grep. 명령은 git 조회와 파일/JSON/해시 처리뿐이며 새 모델·미디어/네트워크·수정 도구는 없었다. 모든 16개 응답의 직접 read 경로도 확인했다. 리뷰 후 원래 묶음 149파일 해시가 일치했고, 후속 보고에서 바꾸는 5개 문서는 `reviewed-c1-documents/`에 원본 버전/해시를 보존했다. 상세 영수증/도구 기록은 `final-independent-review-execution-audit.json`이다.

과거 builder check의 한 줄 `No issues found.`는 이 후보 리뷰나 행동/미디어 검증이 아니다. 독립 리뷰는 사용자 수락·설치/통합 권한을 부여하지 않는다.

## 6. 도입·보존 경계

- 전체 B 구현 완료/기본 적용은 **보류**. 음성 인계의 제한적 관찰 개선과 전체 요구 완료를 구별한다.
- 실제 이미지/음성/영상·청취/재생·공간/물리 검증, 실제 입력 준비/권리/실행 승인·사용자 수락은 수행하지 않았다.
- 커밋·merge/push·전역 skill sync/설치·버전 bump·릴리스·업로드/게시 없음. 원래 dirty checkout/기존 설치 링크는 건드리지 않았다. 공유 post-commit sync 훅도 실행하지 않았다.
- 원시/실패 기록은 gitignored 로컬 증거이며 Git 백업이 아니다. 지우거나 외부 업로드하지 않는다. 소스를 더 바꾸면 새 epoch가 필요하고 C1의 최종 결과를 바뀐 후보의 통과 근거로 재사용하지 않는다.
- 정해진 2건의 잔여 사례를 성공 표본 재추출에 쓰지 않는다. 현재 독립 리뷰 1회도 사용했다. 원래 B의 확대 보기/상태 역대조를 보완한 C2는 C1 증거를 재사용할 수 없으며 동결 최종 8건이 필요하다. C1 종료 시 24건 + 새 8건 = 총 32건이 필요해 추가 6건을 요청했다. 이후 사용자 `남은 작업들을 진행해`로 이 한도 내 C2 보완/평가를 진행한다. 당시 승인 전에는 C2를 시작하지 않았으며 C1/원래 26건 기록도 보존했다. 추가 독립 리뷰·Git 통합/설치·미디어 권한을 포함하지 않는다.

## 7. 실행 판단 기록

계획 ledger의 `Ruling:` 원문을 아래에 보존한다. 이는 작성자가 내린 판단/비용이며 독립 승인으로 해석하지 않는다.

1. Ruling: Use an external cache worktree rather than a new unignored `.worktrees/` — avoids modifying the original tree/.gitignore or triggering sync through a setup commit; cost if wrong: the worktree is less discoverable, so its absolute path/branch are recorded here.

2. Ruling: Defer all conditional commit steps until Git write authorization — implementation approval did not explicitly authorize this new task's commits, and existing post-commit synchronizes global installations; cost if wrong: candidate remains uncommitted and needs preservation/explicit integration later.

3. Ruling: Baselines run before any candidate editing; final candidate cases run in reversed case order, not alternating baseline/candidate per case — the plan's alternating-condition clause conflicts with mandatory RED-before-authoring; cost if wrong: chronological model/provider drift remains a comparison limitation, not a controlled interleaved experiment.

4. Ruling: Preserve this plan's ignored evidence/ledger at handoff rather than delete it — raw prompts, outputs and failed/unreviewed records are required by the approved spec; cost if wrong: ignored evidence needs deliberate backup and is not protected by Git commits.

5. Ruling: collect remaining independent read-only baseline cases in number-ordered groups of at most 2 concurrent children rather than strict serial completion — reduces elapsed time while preserving frozen input/model, no shared writes, original 26-case cap, and all-baselines-before-authoring gate; cost if wrong: provider load/completion order becomes an additional timing/nondeterminism limitation. No statistical/causal effect claim.

6. Ruling: pause candidate authoring and additional model runs at the baseline gate because no real behavioral FAIL was reproduced and one criterion lacks a source reference — approved spec/TDD requires observed failure, not manufacturing a RED by reinterpreting successful outputs; cost if wrong: real weaknesses outside these richly supplied inputs remain unaddressed until evaluation scope is recalibrated. See qa/scene-direction-integration/baseline-summary.md.

7. Ruling: reallocate the remaining 18 to 6 E2 baselines + at most 4 formative checks + 8 final cases (new six plus original SD03/08 controls) under the user-approved recalibration — preserves total 26 and final coverage while limiting redundant interim calls; cost if wrong: less granular per-owner behavioral verification, so intermediate text edits are not called GREEN until covered by a real batch/final test. Final independent review 1 remains unused/required.

8. Ruling: fix only the confirmed owner-to-request seam in existing 11 handoff reference/template and timing serializer — world/character/performance creation succeeded in exercised cases, so do not duplicate or rewrite their owners merely to touch every planned file; cost if wrong: unexercised weaknesses elsewhere and the SD14 world-knowledge ambiguity remain unproven and must be disclosed. This is a bounded integration candidate, not blanket artistic improvement.

9. Ruling: do not consume the remaining 2 formative slots without a new observed failure; keep C1 unchanged and test final 8 in reverse order SD14/13/12/11/10/09/08/03 — sufficient for the approved current checkpoint, not statistical assurance — cost if wrong: only sparse per-scenario samples support the candidate. SD14-O2 baseline ambiguity is preserved and not called fixed by a different generated story.

10. Ruling: preserve SD09-O1 as author INCONCLUSIVE rather than infer that “바닥” necessarily means the counter or silently repair the raw answer — one panel surface word is unclear against the consistent surrounding counter states — cost if wrong: this may overstate uncertainty or understate a real state contradiction; final independent reviewer must adjudicate from the actual text. Do not spend remaining calls rerolling it.

11. Ruling: keep full-B readiness HOLD despite the two voice-consumption improvements and compatibility tests — the original expanded-shot presentation is not newly implemented and other owner tasks remain unchanged/partly unverified under E2 minimal-failure scope — cost if wrong: extra integration/testing or an explicit limited-scope acceptance is needed; no full-goal completion or default rollout claim is made.

12. Ruling: use a hash-bound uncommitted diff plus an explicit untracked-document/evidence index for final review rather than the standard review-package helper — its nonempty commit-range guard cannot apply when commits are not authorized and BASE equals HEAD — cost if wrong: review is not backed by a normal committed range, so exact source/file hashes and preserved local evidence are required. No helper success/commit is claimed.

13. Final: Ruling: adopt independent SD09-O1 and O3 FAIL after checking the explicit panel instruction “바닥” against counter states; preserve original author cards/42P1I and raw results, store adjudicated cards separately — an executor must not guess the intended surface, so this is observed nonconformance, not missing evidence — cost if wrong: two criteria are affected by one defect, not two independent defects; no causal claim that the three-document patch produced it. Adopted final grade7PASS/1FAIL,41PASS/2FAIL. O5 voice PASS remains.

14. Final: Ruling: pause the source fix pass at the evaluation-budget boundary, not at generic continuation — a changed C2 source cannot inherit C1 final evidence and needs eight frozen final cases, but only2 of26 remain; request a total cap32 (+6) before proceeding with the original B completion/fix pass — cost if wrong: original B remains incomplete and no deployment claim is possible. Do not spend the last2 calls resampling a failed C1 story. The single authorized independent review is used; no second review is implicitly requested.

15. Final: Ruling: reviewer declined actual media readability/acting/lipsync/sound — leave unverified; no real media/permission — cost if wrong: cannot certify any rendered-quality improvement.

16. Final: Ruling: reviewer declined spatial/contact/walking/physics/VFX feasibility — leave unverified; text-only scene design — cost if wrong: execution may expose physical/visibility errors.

17. Final: Ruling: reviewer declined current provider/voice/prices/rights — not queried or executed; leave unknown until authorized actual selection — cost if wrong: input readiness/cost/rights cannot be assumed.

18. Final: Ruling: reviewer declined statistics/general artistry/audience response — no superiority claim from sparse sequential-condition samples — cost if wrong: observed two fixes may not generalize.

19. Final: Ruling: reviewer declined skipped OS tests/install/deployment — no OS/runtime/install success claim for skipped/unperformed paths — cost if wrong: cross-platform or deployed behavior remains unverified.

20. Final: Ruling: reviewer declined archive-wide comparison/noncopying guarantee — no exhaustive guarantee; retain only recorded113-fragment audit scope and no archive reads in evaluation — cost if wrong: cannot certify all archive material or broader similarity.

21. Final: Ruling: reviewer declined formative independent semantic regrading — retain author-only formative cards, exclude from independent43 final criteria — cost if wrong: formative12PASS is not independent confirmation.
