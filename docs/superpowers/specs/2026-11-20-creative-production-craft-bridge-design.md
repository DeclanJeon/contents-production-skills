# creative-production 크래프트 브릿지 설계

- 작성일: 2026-11-20 · 상태: 사용자 승인(접근 A) · 브랜치: `feat/open-design-absorption`
- 선행: [open-design 흡수 설계](2026-11-20-open-design-craft-absorption-design.md), [목표 중심 제작 설계](2026-11-19-goal-driven-creative-production-design.md)(main에 2.5로 반영됨)

## 1. 의도

사용자 요구: 영상 제작 요청이 들어오면 `creative-production`이 그 요청에 필요한 모든 스킬과 크래프트를 연결(브릿지)해, 사용자가 스킬 이름이나 단계를 몰라도 **논스톱으로 영상 제작이 진행**되어야 한다.

논스톱 진행 규칙(목표 판정, 단계 자동 진행, 전편 QA, 실행·비용 게이트)은 2.5에 이미 있다. 2.63 QA(실제 에이전트 시험)가 찾은 남은 구멍은 두 가지다.

1. **입구:** 설명이 "명시적 영상 제작 요청에만"이라서, 쇼츠 편집·자막·광고 대본 같은 영상의 일부 작업 요청에서는 스킬이 아예 실행되지 않았다(p3).
2. **다리:** 단계 지도(S00–S12)는 담당 스킬만 가리킨다. 라우터가 다른 담당을 고르면 그 단계의 크래프트(예: 스틸 경로에서 19a 제품 영상 공식)에 닿지 못했다(p4).

## 2. 목표 / 비목표 / 실패 조건

**목표**
- 총괄이 인계할 때마다, 현재 단계와 요청 조건에 맞는 크래프트 참조를 인계 묶음에 실어 담당이 누구든 읽게 한다.
- 영상의 일부 작업(쇼츠·릴스 편집, 자막·로어서드, 광고·프로모 영상 대본, 모션 그래픽 스타일, 기존 영상 재편집) 요청에서도 총괄이 입구가 된다.
- 실제 에이전트 시험으로 브릿지와 논스톱 진행을 확인한다.

**비목표**
- `routing.csv`에 경로를 추가하지 않는다. 33개 경로와 라우팅 회귀 결과(79케이스 0 실패)를 유지한다.
- 실행·비용·게시 권한 규칙을 바꾸지 않는다.
- 영상이 아닌 작업(단독 글쓰기, SNS 글, 단독 이미지, 일반 디자인, 앱 개발)으로 입구를 넓히지 않는다.

**실패 조건**
- 영상이 아닌 요청에서 총괄이 실행된다.
- 라우팅 회귀가 하나라도 바뀌거나, frontier(경로 선택 전에 읽는 분량)가 크게 늘어난다(상한 +60단어).
- 브릿지 표가 존재하지 않는 파일이나 앵커를 가리킨다.
- 논스톱 시험에서 실행·비용 승인 없이 생성·제출을 주장한다.

## 3. 설계 (접근 A)

### 3.1 크래프트 브릿지 표
- 새 파일 `creative-production/references/craft-bridge.csv`. 열: `stage`(S00–S12), `when`(요청 조건, 한국어 짧은 구), `craft_ref`(패키지 기준 경로 + 선택적 `#앵커`), `note`.
- 행 예:
  - `S04, 제품·앱 광고 대본, video-production-assets/references/30-marketing-story-craft.md#od-openmotion-ad-script`
  - `S06, 모션 스타일 선택, video-production-assets/references/33-motion-style-library.md`
  - `S09, 숏폼·멀티캠·비트싱크 편집, …/09a-short-form-edit-recipes.md`
  - `S09, 자막 스타일·로어서드·커버, …/23a-captions-layout.md`
  - `S04·S07, 제품 프로모·세일·데모, …/19a-product-promo-formulas.md`
- 2.63에서 흡수한 참조(08a, 09a, 11a, 19a, 23a, 29a, 33, still-motion-recipes, 30 ad-script)는 반드시 한 행 이상에 들어간다. 기존 심화 참조 중 단계 연결이 자연스러운 것(예: 16 콘셉트·유지, 22 대사·립싱크, take-repair)도 넣을 수 있다. 행 수는 설계자 판단으로 40행 이내.

### 3.2 총괄의 사용 시점
- `creative-production/SKILL.md` Step 4(Hand off)에 한 문장을 추가한다. "패킷을 만들기 전에 [craft-bridge.csv](references/craft-bridge.csv)에서 현재 단계 행 중 요청 조건에 맞는 것만 골라 `craft_refs`로 패킷에 넣는다. 담당은 자기 절차와 함께 그 참조를 읽는다. 담당 경로가 무엇이든 같다."
- 표는 Step 4에서만 읽으므로 frontier에 들어가지 않는다.
- `skill-map.md`의 단계표 아래에 표 링크 한 줄을 추가한다.
- 인계 계약(`contract-core.md`의 worker handoff)에 선택 필드 `craft_refs`(경로 목록)를 한 줄로 명시한다. 새 스키마나 원장 필드는 만들지 않는다.

### 3.3 입구 확장
- `creative-production` frontmatter `description`을 다음 뜻으로 고친다(영어, 기존 형식): 영상 제작 또는 영상 콘티 시트 요청에 사용. 쇼츠·릴스 편집, 기존 영상 재편집·클립 추출, 영상 자막·로어서드, 광고·프로모 영상 대본, 모션 그래픽 스타일 같은 영상의 일부 작업도 포함. 단독 글쓰기, SNS 글, 단독 이미지, 일반 디자인, 앱 개발, 오디오만의 작업은 제외.
- `version` 2.5 → 2.6.

### 3.4 시험 도구
- `scripts/agent_read_probe.py`: 격리 설치본을 만들고 `pi --print --mode json --no-skills --skill <설치본> --tools read,ls,find,grep --model <모델>`로 프롬프트를 실행해, 열린 파일 목록과 최종 답을 JSON으로 저장한다. 케이스는 `creative-production/evals/agent-read-probes.json`(id, prompt, expect_any_read, forbid_read, kind=positive|negative|nonstop).
- pytest에서는 모델을 호출하지 않는다. 케이스 파일 형식과 파서만 오프라인으로 시험한다.

## 4. 검증
- 기존: `pytest scripts` 전체, `routing_regression.py` 0 실패이며 main 대비 케이스 결과 동일, `check_versions.py`.
- 새 오프라인 테스트: 브릿지 표의 모든 경로·앵커 해석, 단계 어휘, 흡수 참조 전부 포함, frontier 단어 증가 ≤60, 설명에 제외 목록 유지.
- 실제 에이전트 시험(sonnet-5-5, 1회씩):
  - 양성 5건(2.63 QA의 p1–p5. p3은 스킬 이름 없이, p4는 사진이 있다고 말한다)에서 기대 참조를 연다.
  - 음성 3건(인스타 캡션 글쓰기, 단독 로고 이미지, 블로그 글)에서 creative-production을 열지 않는다.
  - 논스톱 1건("30초 브랜드 영상 만들어줘…", 읽기 전용 도구)에서 기획→대본→콘티 단계를 이어서 산출하고, 이미지·영상 실행 직전에 필요한 승인만 정확히 묻는다.
- 시험은 1회·1모델이다. 안정성은 측정하지 않으며 QA 기록에 그렇게 적는다.

## 5. 사용자가 정한 것
- 접근 A(단계별 크래프트 지도 + 입구 확장), 경로 추가 없음.
- 2.63 브랜치 위에서 이어서 작업한다.

## 6. 설계자 판단
- 표 형식 CSV, 열 이름, 40행 상한, frontier 상한 +60단어, 설명 문구, 시험 케이스 구성, 버전 2.6.
- 패키지 버전은 2.63에 포함한다(아직 배포 전). CHANGELOG 2.63 항목을 보강한다.
