# 15단계 영상 제작 플로우 정렬 (Flow Alignment) 구현 계획

날짜: 2026-10-04
범위: 사용자가 제시한 15단계 에이전트 영상 제작 플로우를 스킬군과 대조 평가한 결과를 바탕으로, **승인된 4개 개선 항목만** 스킬 문서에 반영한다. 평가는 커버리지 적용 9 / 부분 5 / 미적용 1(1단계 키워드)로 종료되었다.

## Global Constraints

- 저장소: `C:\Users\Declan\Documents\Projects\contents-production-skills` (branch main). 커밋은 승인, **push는 완료됨(2026-10-04, 13커밋)**. 이후 신규 커밋의 push는 사용자 재확인 후.
- git 작업은 `$env:GIT_MASTER='1'` 접두사 필수. 커밋 푸터는 저장소 관례(하단 참조).
- 한글 포함 파일 수정은 **Write/Edit 도구만 사용** — PowerShell 파이프/here-string으로 한글 리터럴을 전달하면 cp949로 손상됨.
- 설치기 `install_package.py`는 회귀 테스트 대상 — 수정 금지.
- 스킬 문서의 기존 문체: 영문 본문 + 한국어 산출물/예시, `supplied/proposed/approved/unresolved` 상태 어휘, "계획 승인 ≠ 지출 승인" 원칙 유지. **새 스킬 ID·새 상태 필드·새 JSON 스키마를 만들지 않는다.**
- 모든 수정은 `version` frontmatter bump 대상 (`bump_version.py --part minor --bump-skills`로 일괄 처리).

## Review Focus (지양 항목 — 평가에서 채택 거부된 것)

1. **결함 티켓 4필드(사유/수정방식/추가소요/예상시간) 전면 강제 금지.** 11-1(수정/비수정 분리) 개념만 참조할 수 있을 뿐, `preproduction-review`와 `Self-check`을 대체하지 않는다.
2. **블렌더를 콘티 좌표 검증의 필수 도구로 고정하지 않는다.** 기존 `camera-spatial-design` + `blender-previsualization` 분업을 유지.
3. **30분~1시간 통합 파이프라인을 만들지 않는다.** explainer의 `N×10초` 블록 모델은 건드리지 않는다.
4. **키워드 선정을 창작 최상단 단계로 만들지 않는다.** 유통(제목/썸네일/챕터) 후단으로만 문서화한다.
5. 새 모델명·가격·웹 도구를 스킬 본문에 **고정 목록으로 새기지 않는다** (기존 규칙: 라이브 검증 우선). 단, USAGE_GUIDE의 도구 언급은 "예시"로만 허용.

## Task 1 — 감정 단계를 프리프로덕션 spine에 연결 (P0)

**근거:** 사용자 플로우 3번(감정 선택)은 옳은 설계지만 스킬 spine에 필드가 없어 `16-concept-emotion-retention.md`와 분리되어 있다.

- **File:** `orchestrating-video-preproduction/SKILL.md`
  - `## The shared spine` 표에 행 1개 추가: `Emotion` — 목표 감정 여정(순서)과 핵심 감정의 감각/시각 앵커; 미지정이면 `unresolved`. 기존 `Tone` 행과는 별개(테이스트 vs 전달 목표)임을 한 줄로 구분.
  - `## Running the stages`의 **Concept and synopsis** 단락에 1문장 추가: 감정이 미정이면 시놉시스 확정 전에 감정 선택을 좌초시키는 1회 체크포인트로 처리하고, `../video-production-assets/references/16-concept-emotion-retention.md` §2를 참조하되 그 절차는 선택적 심화임을 명시.
- **File:** `orchestrating-video-preproduction/references/video-direction.md`
  - `## Checkpoints` 표에 행 추가: **Emotion** — Present: 주제 확정 후, 감정이 미정일 때만 소수(≤3)의 감정 여정 후보; Exit: 사용자 선택 또는 명시적 위임. `Topic` 다음 `Direction` 앞 순서로 배치.
  - `## Discovery` 절의 inheritance 항목에 "승인된 감정 여정은 재질문하지 않는다" 1줄 추가.
- **검증:** spine 행 ↔ 체크포인트 행 ↔ Concept 단락 참조가 서로 일치, 기존 Tone/Direction 필드와 모호하지 않은 구분, `16번` 참조 링크가 상대경로로 실제로 존재.

## Task 2 — 캐릭터 시트에 음성 설계 3경로 추가 (P0)

**근거:** 사용자 플로우 6-1~6-3(웹 음성 선별 / 직접 합성 / 유사 음성 대체)이 스킬에 없음. 심화 절차는 이미 `22-dialogue-lipsync.md`의 "보이스 선택과 청취"에 존재하므로 **중복하지 말고 연결**한다.

- **File:** `designing-video-character-sheets/SKILL.md`
  - `## Sheet format` 앞에 신규 절 `## Voice profile` 추가:
    - 시트 항목으로 성우/보이스 프로필 **텍스트** 기술: 톤·속도·발성 위치·언어/사투리(제공된 것만)·감정 범위 — 이 스킬은 음성 파일을 생성하지 않음(텍스트+이미지 프롬프트 한정)을 명시.
    - **조달 경로 3분기**를 표로: ① 사용자 제공 음성(업로드/녹음) → 그대로 사용, ② 합성(TTS/클로닝) → 권리·동의 근거 확인 후 오디션 승인, ③ 유사 보이스 대체 → 현재 가용 목록 비교 후 오디션 승인. 각 경로는 "선택된 경로는 downstream `22-dialogue-lipsync.md`의 보이스 선택·청취 절차로 인계"로 연결.
    - 미지정 인구통계 학습 규칙(제공되지 않은 나이/성별 라벨 금지)이 음성 프로필에도 적용됨을 명시 — 음성에서도 "30대 여성" 같은 미제공 라벨을 발명하지 않는다.
  - `## Sheet format`의 시트 항목 번호에 보이스 프로필을 포함시키고, `## Self-check`에 1항목 추가: "보이스 프로필이 제공 사실인가 명시된 제안인가? 미제공 인구통계/권리 추론이 없는가?"
- **검증:** 새 음성 파일 생성·TTS 실행을 이 스킬이 암시하지 않음, `22-dialogue-lipsync`와의 책임 경계가 명시, Self-check과 일치.

## Task 3 — N클립 총 예상비용 고지 게이트 (P0)

**근거:** 사용자 플로우 14→15(모델 선택→제작)에 비용 게이트가 없고, 스킬도 "총 예상 비용 요약"을 승인 인터뷰에 포함하는 규칙이 없음(단가·상한만 존재).

- **File:** `video-production-assets/references/24-production-execution.md` §1 `### 승인 규칙`
  - 1문단 추가: 샷/블록/출력이 N개인 유료·무료 허용량 경로든 **승인 요청 시 N × 현재 단가(또는 견적) = 총 예상 비용 요약을 먼저 제시**한다. 견적 미확인이면 `unknown_cost`로 차단(기존 표와 일치). 승인은 이 요약에 바인딩되며, N이 바뀌면 승인은 stale.
- **File:** `creative-production/references/video-generation-planning.md` §6
  - 첫 항목에 1줄: 제출 전 승인된 범위의 N(샷/출력 수)과 총 예상 비용 요약이 실행 기록에 있는지 확인 — 없으면 제출하지 않는다. (24번 §1이 소유자, 이 문서는 참조만.)
- **검증:** 기존 FREE-FIRST 정책·`unknown_cost` 차단 규칙과 모순 없음, 스키마/필드 신규 추가 없음(기존 `generation_attempts` 활용).

## Task 4 — 완성 이후 체인 + 키워드 후단 문서화 (P1)

**근거:** 사용자 플로우가 15번에서 끝나지만 스킬에는 21(QA/재시도)·09(편집)·23(파이니싱/플랫폼)·15(납품)가 이미 있고, 반대로 키워드(1번)는 어느 스킬에도 없음. **체인은 이미 존재하므로 연결만, 키워드는 후단에 신설 위치만** 문서화한다.

- **File:** `USAGE_GUIDE.md` §3 `전체 영상 제작`
  - 기존 A(기획/프리프로덕션)·B(실행 계획/승인)·C(생성·편집·검사) 뒤에 **`D. 완성 이후: 검증–편집–피니싱–유통`** 소절 추가 (번호 6, 7, 8, 9):
    6. 생성 영상 QA/재시도 → `21-generated-video-qa-retry.md` (실제 미디어 검사, 실패 근거 후 재시도 상한 내)
    7. 편집·오디오 큐·자막 → `09-edit.md`, `15-delivery.md`
    8. 파이니싱·플랫폼 적응 → `23-finishing-platform.md`
    9. **유통 메타데이터(제목·키워드·썸네일·챕터)** — 콘텐츠 확정 이후에 설계. 키워드는 완성 영상의 주제·감정 약속에서 도출하며, `higgsfield-youtube-thumbnail`의 정보격차 컨셉과 연결. 발행 자체는 별도 승인(§5의 기존 규칙 유지).
  - §3 서두에 1문장: 순서는 A→B→C→D이며, D의 각 항목은 별도 요청 없이 자동 실행되지 않는다(기존 승인 원칙).
- **검증:** 기존 §5(수정과 납품) 및 발행 승인 규칙과 중복/모순 없음, 참조 링크 존재, 키워드가 최상단이 아님을 명시.

## Execution order

Task 1 → 2 → 3 → 4 (전부 독립적이나 문서 일관성을 위해 순서대로) → `bump_version.py --part minor --bump-skills` → `check_versions.py` → `pytest scripts -q` (39 통과 기준) → `sync_installed.py --dry-run` → 실제 sync → 커밋.

## Completion evidence

- 4개 Task의 파일별 변경 내용 요약 (근거 문구 인용 포함).
- `version check OK: package X.Y, 17 skill(s) consistent`.
- `pytest scripts -q` 결과, sync dry-run/실행 결과(created/repointed/skip).
- pre-commit 통과 커밋 기록. push 여부는 사용자에게 재확인.

## Commit footer (저장소 관례)

```
-Ultraworked with [Sisyphus](https://github.com/code-yeongyu/oh-my-openagent)
-Co-authored-by: Sisyphus <clio-agent@sisyphuslabs.ai>
```
