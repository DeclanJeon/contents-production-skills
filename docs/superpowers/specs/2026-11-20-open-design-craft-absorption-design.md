# open-design 영상 크래프트 흡수 설계 (2.62 → 2.63)

- 작성일: 2026-11-20
- 상태: 사용자 검토 대기
- 흡수 원장: [2026-11-20-open-design-absorption-ledger.csv](2026-11-20-open-design-absorption-ledger.csv)

## 1. 의도

사용자는 https://open-design.ai/ko/skills/ 에 공개된 스킬 407개 중 영상 제작에 쓸 수 있는 노하우를
이 패키지에 흡수하려 한다. 배포는 **이 패키지(contents-production-skills)로만** 한다.
CineForge는 이 패키지를 스킬팩으로 쓰므로(`CINEFORGE_SKILL_PACK`) 따로 설치하지 않는다.

이 패키지는 herdr-org 조직의 콘텐츠 제작팀이 기본으로 쓰는 스킬팩이 된다. 사용자가 직접 지목한 스킬은
`openmotion-ad-script`이다.

## 2. 목표 / 비목표 / 실패 조건

**목표**
- 원장에서 `absorb`로 판정한 139개의 영상 크래프트(대본 구조, 편집 방식, 자막·레이아웃, 모션 원칙,
  제품 영상 공식, AI 영상 지시법, 모션 스타일 레시피)를 기존 담당 스킬의 조건부 참조로 녹인다.
- 출처, 원본 커밋, 라이선스 고지를 패키지 안에 함께 배포한다.

**비목표**
- 새 설치형 스킬, 새 총괄, 새 라우트를 만들지 않는다. `routing.csv`의 경로 수를 유지한다.
- OpenMotion, HyperFrames, Motion Canvas, Lottie 같은 실행 엔진을 설치하거나 의존성으로 추가하지 않는다.
- 웹·UI, PPT, 브랜드 시스템, UX 리서치, 단독 이미지 스킬(원장 `out_of_scope` 224개)은 이 패키지에 넣지 않는다.

**실패 조건**
- 라우팅 회귀(65/65), 라우팅 표 lint, repo integrity 중 하나라도 깨진다.
- 첫 담당 스킬을 고르기 전에 읽는 분량(frontier, 현재 약 1,410단어)이 늘어난다.
- 원문을 출처·고지 없이 복사하거나, MIT·Apache가 아닌 자료가 섞인다.
- 흡수한 지침이 원본 엔진의 도구 호출(`openmotion_media_use`, `openmotion_assets_use` 등)을 그대로 요구해서,
  패키지만 설치한 환경에서 실행할 수 없다.

## 3. 제약

- 패키지 원칙: 단일 총괄 `creative-production`, 마이크로 스킬 금지, 정책 정본은 `creative-production/references/policy.md`.
- 저장소는 공개되어 있지만 재사용 라이선스가 없다(`integrations/package-provenance.md`).
  따라서 외부 자료는 원본 커밋, 약관, 고지를 확인한 뒤에만 들여온다. 약관을 모르면 들여오지 않는다.
- 선례: `video-production-assets/references/upstream/im-not-ai-*` 방식(provenance 문서 + 원본 LICENSE 동봉).
- 큰 모듈 분량: 09-edit 3,335단어, 19-brand 1,438단어, 08-animation 1,221단어. 본문에 직접 붙이면 읽기 비용이 커진다.

## 4. 검토한 방식

| 방식 | 내용 | 결정 |
|---|---|---|
| A | 원본 스킬을 각각 설치형 스킬로 추가 | 기각: 마이크로 스킬 금지 원칙과 라우팅 정확도 훼손 |
| **B** | 기존 담당 스킬의 조건부 참조로 녹이고 고지를 동봉 | **채택(사용자 선택)** |
| C | B + 엔진이 필요한 항목을 manifest 외부 의존성으로 등록 | 기각: 엔진 항목은 흡수 대상에서 뺀다 |

## 5. 원장 판정 기준

원장 열: `slug, name, repo, license, decision, target, reason, source`.

| 판정 | 개수 | 기준 |
|---|---|---|
| absorb | 139 | MIT 또는 Apache-2.0이면서 영상 제작에 바로 쓰는 크래프트 |
| exclude | 44 | 엔진 자체(openmotion core, hyperframes, motion-canvas, text-to-lottie, pixel2motion, after-effects, manim, figma), 이미 manifest의 외부 레인에 있는 것(baoyu-comic, remotion-* 등), 그리고 MIT·Apache가 아닌 것 |
| out_of_scope | 224 | 영상이 아닌 UI·웹·PPT·브랜드·리서치·정적 이미지 |

원장은 키워드 규칙으로 만든 초안이다. 구현 첫 단계에서 각 원본 SKILL.md를 읽고 판정과 대상 모듈을 확정한다.
판정을 바꾸면 원장에 사유를 남긴다.

## 6. 흡수 위치

본문은 늘리지 않는다. 대상 모듈마다 **심화 참조 파일 하나**를 새로 만들고, 기존 모듈에는 그 파일로 가는
조건부 링크 한 줄만 추가한다.

| 대상(원장 target) | 개수 | 새 파일 | 내용 |
|---|---|---|---|
| 33-motion-style-library | 77 | `video-production-assets/references/33-motion-style-library.md`(색인) + `references/motion-styles/<family>.md` | openmotion 스타일 레시피. 스타일마다 쓰는 곳·화면 구성·움직임·피할 것·검수 기준. 6~8개 계열(키네틱 타이포, 설명 영상 형식, 제품·커머스, 로고·브랜드 스팅, 전환·오버레이, 포스터·배경, 수공예 질감, 데이터·지도)로 나눈다 |
| 19-brand-product-integration | 13 | `19a-product-promo-formulas.md` | 제품 영상 공식, 세일·카운트다운·스펙시트, 런칭·기능 데모 |
| 08-animation | 12 | `08a-motion-craft.md` | 모션 원칙, 키프레임, 로고 애니메이션, 색 움직임, storyboard-to-motion |
| 09-edit | 8 | `09a-short-form-edit-recipes.md` | edit-to-script, 멀티캠, 릴스·쇼츠 추출, 라이브 클립, 비트 싱크 |
| 23-finishing-platform | 6 | `23a-captions-layout.md` | 자막 스타일, 이중 언어 자막, 화면 비율별 레이아웃, 하단 자막, 커버 |
| 11-ai-handoff | 6 | `11a-ai-video-prompting.md` | Seedance식 지시, video-to-superprompt, shotcraft, 루프 영상 |
| 29-reference-driven-production | 5 | `29a-template-recreation.md` | 레퍼런스 재현, 템플릿화, 디자인 리믹스, 토킹헤드 재현 |
| 30-marketing-story-craft | 2 | 30번 본문에 짧은 절로 추가 | **ad-script**(사용자 지정), growth-teardown |
| 03-screenplay, 10-evidence, 06-shots, 25, 13 | 각 1~2 | 해당 모듈 본문에 짧은 절로 추가 | presenter-story, 튜토리얼·faceless 설명 영상, shot-composition, shot-breakdown, general-video |
| storytelling-with-still-images | 3 | `storytelling-with-still-images/references/still-motion-recipes.md` | 슬라이드쇼, 손그림 스토리, 기사 삽화 영상 |

모든 새 파일 이름과 번호는 설계자 판단이며, 기존 번호 체계와 충돌하면 구현 단계에서 조정한다.

## 7. 각색 규칙

1. **원문을 그대로 붙이지 않고 패키지 말투로 다시 쓴다.** 수치(팔레트, 타이밍, 비트 길이)는 "시작값"으로 유지한다.
2. **엔진 의존을 걷어낸다.** `openmotion_*` 호출, HyperFrames 명령, 원본 저장 방식은 패키지의 실행 게이트
   (`policy.md`: 사전검토·사용자 수락·실행 승인, 단일 project.json writer)로 바꾼다.
   실행 수단은 기존 레인(remotion, ffmpeg, Blender, 선택된 생성기)을 가리킨다.
3. **사실 보호 규칙을 유지한다.** 가격·숫자·후기·보증을 지어내지 않는다는 원본의 Avoid 항목은 `10-evidence` 규칙과 맞춘다.
4. 각 절 끝에 `출처: <repo>@<commit> <slug>`를 단다.
5. 원본에 있던 예시 미디어, 템플릿 코드, 바이너리는 들여오지 않는다.

## 8. 출처와 라이선스

- `video-production-assets/references/upstream/open-design-provenance.md`
  - upstream 저장소별 원본 커밋, 흡수한 slug, 대상 파일, 원문 해시
- `upstream/<repo>-LICENSE.txt`: 저장소별 원본 LICENSE 사본. Apache-2.0은 NOTICE 파일이 있으면 함께 넣는다.
- 원본 커밋이 open-design 카드에 고정되어 있지 않은 항목(`blob/main`)은 흡수 시점의 커밋 해시를 직접 확인해 고정한다.
- `integrations/package-provenance.md`에 "open-design 크래프트 각색" 절을 추가한다. 이 고지는 해당 각색분에만 적용되며 패키지 전체의 라이선스가 아님을 명시한다.

## 9. 라우팅과 읽기 비용

- `routing.csv`에는 행을 추가하지 않는다. 필요하면 기존 행의 `required_read`에도 새 파일을 넣지 않는다.
  새 파일은 담당 스킬이 선택된 뒤 요청 내용에 맞을 때만 읽는다.
- `creative-production/SKILL.md`(frontier)는 수정하지 않는다.
- `video-production-assets/SKILL.md`의 모듈 목록에는 새 심화 참조를 한 줄씩만 추가한다.

## 10. 검증

- 기존 회귀: `scripts/routing_regression.py`, `test_routing_table_lint.py`, `test_routing_truth_audit.py`, `test_repo_integrity.py`, `pytest`.
- 새 테스트 `scripts/test_open_design_absorption.py`
  1. 원장의 `absorb` 행마다 대상 파일 안에 해당 slug의 출처 줄이 있다.
  2. `absorb` 행의 라이선스는 MIT 또는 Apache-2.0뿐이다.
  3. provenance에 나오는 모든 repo의 LICENSE 사본이 있다.
  4. 흡수 파일에 `openmotion_media_use`, `openmotion_assets_use`, `npx hyperframes` 같은 엔진 호출이 남아 있지 않다.
  5. 새 파일 링크가 모두 해석된다.
  - 각 검사는 원장을 일부러 오염시켰을 때 실패하는지도 확인한다(기존 truth audit 방식).
- 행동 검증: 기존 라우팅 평가(65/65)를 다시 돌려 경로 변화가 없음을 확인한다. ad-script 요청 1건으로
  30번 모듈에서 새 절을 실제로 읽는지 확인한다.
- QA 기록: `qa/2026-11-20-open-design-absorption-validation.md`.

## 11. 릴리스

- manifest `version` 2.62 → 2.63, CHANGELOG, README 요약 한 단락.
- 공개 저장소이므로 push와 배포는 사용자가 따로 승인한다. 이번 범위는 로컬 커밋까지다.
- 기존 설치본은 `scripts/install_package.py`로 사용자가 명시적으로 갱신한다.

## 12. 사용자가 정한 것
- 배포는 contents-production-skills로만 한다. CineForge에는 따로 설치하지 않는다.
- 흡수 방식 B: 기존 담당 스킬의 참조로 녹인다.
- ad-script는 반드시 포함한다.

## 13. 설계자 판단 (변경 가능)
- MIT·Apache만 흡수하고, 엔진 자체와 이미 외부 레인에 있는 것은 제외한다.
- 모듈 본문 대신 심화 참조 파일로 분리한다. 새 파일 이름과 번호, 모션 스타일 계열 구분도 설계자 판단이다.
- 라우팅 행을 추가하지 않는다.
- push 없이 로컬 커밋까지만 한다.

## 14. 구현 단계에서 정할 것
- 원장의 각 항목을 원본 SKILL.md 기준으로 다시 판정한다(특히 hyperframes 계열, dream-loop, design-motion-principles).
- 모션 스타일 계열 구분과 계열별 파일 분량 상한.
- `blob/main`으로만 연결된 항목의 원본 커밋 해시.
