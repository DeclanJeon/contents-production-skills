# 제작 스킬 전수 무게·구조·정합성 감사

기준: 2026-11-18 KST · Git `bd5fb689dced7d09d966bff8f1897c06bac6082f`

## 1. 결론

**최적화가 필요하다. 다만 핵심 문제는 스킬 수 자체보다, 작은 작업에도 큰 공통 계약을 읽는 구조와 한 컷 조회에 전체 시퀀스를 반환하는 구조다.** 문장을 짧게 고치거나 안전 규칙을 삭제하는 것보다 읽기 단위와 조회 출력을 분리하는 편이 우선이다.

가장 효과가 클 것으로 판단하는 순서:

1. **시퀀스 전체 저장 데이터와 에이전트가 읽을 포커스 뷰 분리.** 한 컷 작업인데 전체 투영 JSON을 읽게 하는 경로부터 줄인다.
2. **`video-production-assets` 진입점과 공통 계약 분해.** 단일 조명/각본/검수 요청이 전체 제작·패키징 규격을 함께 읽지 않게 한다.
3. **스토리보드 계약을 단계별로 분리.** 필수 연출·기술 슬롯은 유지하면서, 텍스트 설계에 PDF/PNG 추출/패키지 JSON 전체를 미리 읽지 않게 한다.
4. **불필요한 실행 전제와 충돌 수정.** 특히 대체 이미지 실행자에서도 Higgsfield 로그인·견적을 요구하는 썸네일 지침, `text_only`와 `no-save`의 혼용이다.
5. 이후에 캐릭터/공급자 스킬의 중복 설명, 긴 CLI 예제, 요청 내 중복 probe를 정리한다.

**이 감사에서는 스킬·검증기·배포 설정을 변경하지 않았다.** 새 감사 문서와 측정 스크립트/결과만 이 폴더에 만들었다. 최적화된 스킬의 성능 개선이나 행동 동등성을 측정한 것은 아니다.

## 2. 범위와 측정 방법

- `manifest.json`의 관리 대상 **25개**와, 이 저장소의 디렉터리에 실제 설치 링크가 연결된 비목록 스킬 **4개**, 총 **29개 `SKILL.md` 본문을 모두 읽었다**.
- 25개 관리 대상은 Markdown 205개, 4개 추가 범위까지 합치면 Markdown **274개**다. 전체 파일에 정량·링크·동일 문단 검사를 수행했다. 274개 참조를 모두 동일 깊이로 수동 정독했다는 뜻은 아니다. 공통 policy/contract, 스토리보드 계약, 라우팅, 주요 실행 게이트 및 문제의 소유 참조를 추가 대조했다.
- 생성된 `video-production-assets/support/` 복사본은 제외했다. 같은 문서를 원본과 배포 사본으로 이중 집계하지 않는다.
- 비목록 4개는 `higgsfield-brandkit`, `higgsfield-marketplace-cards`, `higgsfield-product-photoshoot`, `higgsfield-websites`다. 비디오팩 manifest에서 제외하는 것은 의도된 경계이며, **누락 버그라고 판정하지 않았다**. 다만 실제 설치되어 있으므로 무게/내용 검토에는 별도 포함했다. 관리 스크립트가 25개를 검증했다고 이 4개까지 검증했다고 말하면 안 된다.
- 토큰은 CRLF를 LF로 정규화해 읽은 텍스트에 대해 설치된 `tiktoken`의 **`o200k_base` 기준 실측**이다. 현재 모델의 실제 tokenizer, harness 직렬화, 캐시 적중, 청구 토큰, 응답 시간과 동일하다고 주장하지 않는다. 측정 자료는 실제 파일 바이트 SHA256과 정규화 텍스트 SHA256을 구분하며, 초기 측정 대비 274개 소스의 내용이 유지됐는지 확인했다.
- 경로 비용은 **선언된 파일을 각각 한 번씩 전체 읽는 경우의 합집합**이다. 섹션만 읽으면 낮아지고, 조건부 참조·입력 자료·출력·대화가 추가되면 높아진다. 런타임 추적 비용이나 모든 작업의 절대 최소량이 아니다.
- 추가 성능 검사는 외부 공급자 없이 합성 소스에 실제 로컬 validator/FFprobe/해시 함수를 실행했다. 실제 영상 제작 시간이나 모델 비용을 예측하는 실험은 아니다.

재현 자료:

- [측정 스크립트](audit_metrics.py), [전체 지표](metrics.json), [관리 25개 별도 지표](metrics-managed.json), [스킬 CSV](skills.csv)
- [작업별 파일 합집합](profiles.json), [이름·설명 길이](discovery.json), [의존성 확인](dependency-checks.json)
- [포커스 조회 확장 실험](context-scaling.json), [validator 계측 스크립트](benchmark_validation.py), [실행 결과](validation-benchmark.json)
- [비목록 설치 경로](unlisted-installed-skills.json), [기존 회귀 검사](regression-checks.txt)

```bash
python3 docs/analysis/2026-11-18-skills-weight-audit/audit_metrics.py \
  --repo . --include-unlisted --output docs/analysis/2026-11-18-skills-weight-audit
python3 docs/analysis/2026-11-18-skills-weight-audit/benchmark_validation.py \
  --repo . --output docs/analysis/2026-11-18-skills-weight-audit/validation-benchmark.json
```

## 3. 전체 무게: 디스크 크기와 실제 문맥을 구분해야 한다

| 범위 | 기준 tokenizer 토큰 | 해석 |
|---|---:|---|
| 관리 25개 SKILL 본문 합 | 61,031 | 25개를 전부 읽었을 때의 합. 매 작업 자동 주입량이 아님 |
| 추가 4개 SKILL 본문 합 | 11,593 | 별도 비디오 외 스킬 |
| 실제 연결된 29개 SKILL 본문 합 | 72,624 | 총 본문량 |
| 관리 25개 전체 Markdown | 476,555 | 선택적 참조·템플릿·출처 포함, 전부 로드할 이유 없음 |
| 29개 전체 Markdown | 674,471 | 라이브러리 저장량. 이 숫자를 작업당 비용으로 쓰면 잘못된 분석 |
| 29개 이름+description 정규화 합 | 약 3,080 | 스킬 발견 메타데이터의 대용치. 실제 Pi 전체 시스템 프롬프트 크기는 아님 |

**따라서 '스킬이 67만 토큰이라 매번 그만큼 든다'는 결론은 틀리다.** 발견 단계는 이름/설명 중심이고, 본문과 참조가 실제로 읽힐 때 누적된다. 문제는 그 이후의 필수 읽기 전선이다.

### 3.1 무거운 진입점

```text
video-production-assets       7,093  ██████████████
higgsfield-video-explainer    4,620  █████████
higgsfield-generate           4,540  █████████
higgsfield-websites *         4,410  █████████
higgsfield-video-replicate    3,716  ███████
higgsfield-brandkit *         3,407  ███████
blender-previsualization      3,307  ███████
silent-satire-animatic        3,303  ███████
storyboarding-video           3,272  ███████
character-sheets              3,183  ██████
```

`*`는 manifest 비목록 스킬. 그래프는 실측 표의 축약 표시이며 길이 기준은 약 500토큰/블록이다.

줄 수는 무게를 잘 설명하지 않는다. `blender-previsualization`은 47줄이지만 3,307토큰이고 실행 절 한 문단이 1,892토큰이다. `video-production-assets`의 가장 큰 문단은 1,799토큰이다. 긴 단일 행/표를 접었다고 문맥이 줄어들지 않는다. [metrics.json]

## 4. 작업별 읽기 비용

공통 라우팅 전선은 `creative-production/SKILL.md` 1,801 + `routing.csv` 1,460 + `routing-disambiguation.csv` 608 + `policy.md` 980 = **4,849토큰**이다. 현재 문서에 선언된 순서를 따르는 전체 파일 읽기 모델이다. [creative-production/SKILL.md:16–56]

| 대표 작업 | 정적으로 선택한 파일 합 | 포함 범위/한계 |
|---|---:|---|
| 로그라인/시놉 경로 R02 | 8,896 | 공통 전선 + synopsis 진입점 + craft guide. 로그라인 출력 자체보다 준비 읽기가 훨씬 큼 |
| 단일 조명 계획 R13 | 22,538 | 공통 전선 + assets 진입점 + 공통 contract 전체 + 07 + 템플릿 |
| 일반 텍스트 콘티 R10 | 25,058 | 공통 전선 + storyboard 진입점 + storyboard 계약 전체 |
| 위 콘티에서 공통 contract도 전체 열 때 | 33,087 | 파일 읽기 추가 시나리오. 무조건 모든 콘티가 이만큼 읽는다는 뜻은 아님 |
| 신규 캐릭터, typology none 프로필 | 17,375 | R03 전선 + persona 진입점/표현 연결/템플릿. 전체 SSOT는 제외 |
| 신규 허구 캐릭터, 기본 both lens | 19,022 | 위 프로필 + MBTI/Enneagram 참조. 실제 voice/이미지 실행은 제외 |
| 이미지 기반 전체 패키지 R24의 첫 목록 | 33,606 | 캐릭터·각본·카메라 등 후속 전체 작업량은 포함하지 않음 |
| 종속 영상 생성 실행자 + 연속성 게이트 묶음 | 15,726 | generate 진입점 + 26 + sequence-execution + package-gate. 공급자/프로젝트 추가 문맥은 제외 |

[profiles.json]에 각 합계의 정확한 경로 목록을 남겼다. 단순한 링크 전체 재귀 탐색 결과를 필수 읽기량으로 둔갑시키지 않았다.

## 5. 상세 발견 사항과 우선순위

### F01 · P1 · 한 컷 조회에서도 전체 시퀀스가 출력된다

**근거:** `video-production-assets/scripts/sequence_context.py:82–111`. `context`는 포커스와 이웃/이력으로 좁히지만, 반환 객체의 최상위 `cuts`, `links`, `requirements`, 기존 projection/pins는 유지한다. CLI는 그 객체 전체를 stdout으로 출력한다.

실행한 합성 계획 뼈대 실험:

| 프로젝트 샷 수 | 포커스 샷 | context 안 샷 | 반환 cuts | 전체 출력 토큰 | context 부분만 토큰 |
|---:|---:|---:|---:|---:|---:|
| 2 | 1 | 2 | 2 | 3,678 | 2,029 |
| 10 | 1 | 3 | 10 | 6,111 | 1,023 |
| 50 | 1 | 3 | 50 | 23,389 | 1,023 |
| 100 | 1 | 3 | 100 | 45,039 | 1,023 |

이 실험의 추가 샷은 이미지/비트가 아직 없는 **불완전한 합성 계획 뼈대**다. 완성된 100컷 보드가 45,039토큰이라는 예측이나 QA 통과 증거가 아니다. 반환 구조가 전체 영화 길이에 따라 커진다는 재현 증거다. context 부분만으로 generation 검사를 할 수 있다는 뜻도 아니다. [context-scaling.json]

**제안:** 디스크의 전체 실행 투영은 그대로 보존하고, `focus/neighbor/history/current pins/bindings/blockers`만 보여 주는 명시적 읽기 뷰를 추가한다. 전체 원장을 잘라 validator에 넣거나 이력 연결을 지우는 최적화는 금지한다. 전체 커버리지 검사는 실제 실행/납품 게이트에서 유지한다.

### F02 · P1 · assets 진입점과 공통 계약이 너무 넓다

**근거:** `video-production-assets/SKILL.md:25–39,61–107`; `references/contract.md`.

- SKILL 본문 7,093토큰에 단일 모듈 규칙, 전체 패키지, 심화 색인, 이미지/검수/패키징 절차가 같이 들어 있다.
- '단일 산출물에는 해당 모듈만'이라고 하면서 공통 `contract.md` 읽기는 요구한다. contract 전체는 **8,029토큰**이고 전체 프리프로덕션 패키지와 v5.1 무결성 절만 각각 약 1,675/1,794토큰이다.
- 단일 조명 계획에 필요한 시간/ID/인계 규칙과, ZIP relocation·전체 이미지 시트·마스터 계보 전체 명세가 같은 읽기 단위다.

**제안:** 기본 인계/ID/시간 규칙, 기존 프로젝트 수정, 이미지 패키지/FINAL, 납품/ZIP, 실행 투영을 분리하고 적용 조건을 진입점에서 명확히 지정한다. 기존 ID/버전/단일 기록자/연속성의 의미는 유지한다. 문서 이름만 쪼개고 전부 필수로 읽히게 하면 개선이 아니다.

### F03 · P1 · 스토리보드의 완전성 계약과 실행 매뉴얼이 결합돼 있다

**근거:** `storyboarding-video/SKILL.md:11–17,33–45`; `video-production-assets/references/storyboard-contract.md:1–303`.

계약 전체는 **16,937토큰**이다. 모든 샷의 필수 연출·기술 슬롯은 중요하지만, 같은 파일에 이미지 생성/PNG 조립/추출/PDF/Chrome·Poppler/JSON 확장/리듬 스키마까지 들어 있다. §4 실제 이미지/PDF 약 2,645토큰, §8 JSON/리듬 확장 약 2,838토큰은 채팅 전용 연출 설계와 실행 단계가 다르다.

**제안:** `보드 기본·완전성`, `텍스트/샷 설계`, `실제 이미지·시트·추출`, `PDF 납품`, `기계 판독 스키마`를 단계로 나눠 읽는다. **일반 콘티를 몰래 러프 콘티로 낮추거나 필수 기술 슬롯을 없애는 변경은 제안하지 않는다.** 기존 6개 반환 구획, 전체 비트 커버리지, 정체성/소품/프레임 연결은 보존해야 한다.

### F04 · P1 · 썸네일 대체 실행자에 불필요한 공급자 전제가 걸린다

**근거:** `higgsfield-youtube-thumbnail/SKILL.md:18–29` 대 `creative-production/references/policy.md:71–79`, `video-production-assets/references/24-production-execution.md:3,17,47–55`.

썸네일 지침은 Higgsfield 이미지 실행이 금지되어 기본적으로 `codex-imagen`으로 넘기면서도, 실제 렌더 전 Higgsfield 로그인과 검증 견적을 요구한다. 정본 이미지 정책은 Codex Imagen의 usage/price/quota/quote 검사를 명시적으로 제외한다.

**판정:** 문서 수준 전제 충돌이다. 이번 감사에서 실제 이미지 실행을 시도하거나 에이전트 행동을 재현한 것은 아니다. 상위 정책이 우선하더라도, 전문 스킬을 단독 로드한 실행자가 불필요한 로그인·견적 경로에 빠질 위험이 있다.

**제안:** 실행자가 선택된 뒤 그 실행자에 필요한 전제만 검사한다. 이미지 대체 경로에 비사용 공급자의 인증/견적을 요구하지 않는다. 권리·입력·실행 범위는 유지한다.

### F05 · P1 · 필수 외부 조정 스킬이 현재 설치 루트에 없다

**근거:** `creative-production/SKILL.md:66–71`, `manifest.json`의 conditional coordination discipline 항목, [dependency-checks.json].

`ai-delegation-loop`는 반복 제작·다단계 조정 등에 required지만, 확인한 Codex/Claude/shared/Pi의 네 설치 루트에 해당 `SKILL.md`가 없다. manifest가 외부 의존성을 선언하고 있어 '의존성을 전혀 몰랐다'는 문제는 아니다. 본문도 영향을 받지 않는 작업은 계속하라고 한다.

**제안:** 설치 전 점검에서 '어떤 기능의 의존성이 빠졌는지'를 한 번 노출한다. 설치를 자동 수행하거나 필수 조건을 조용히 무시하지 않는다. 외부 스킬을 계속 요구할지, 같은 책임을 이미 가진 내부 계약으로 대체할지는 명시적 설계 결정/검증 대상이다. 현재 상태에서 다단계 전체가 완전히 무의존이라고 안내하면 안 된다.

### F06 · P1 · text-only, chat-only, no-save가 섞여 있다

**근거:** `storyboarding-video/SKILL.md:13,33`; `orchestrating-video-preproduction/SKILL.md:21`; `recording-production-history/SKILL.md:95–103`; 스토리보드 계약의 그림 없는 텍스트 PDF 납품 절.

일부 진입점은 `text-only`를 'files 금지'로 정의하지만, 다른 절은 사용자가 텍스트 계획을 파일로 요청하면 MD/PDF로 저장하는 경로를 제공한다. history의 '단일 텍스트 산출물'도 '채팅-only'와 같은 문장으로 묶여 있다. 따라서 '이미지 없이 콘티를 Markdown으로 저장' 요청에서 매체 범위와 저장 범위가 충돌할 여지가 있다.

**제안:** 미디어 축과 저장 축을 구분한다. 예를 들어 '이미지/영상 생성 없음'과 '파일 저장 없음'을 별개 조건으로 표현한다. 명시적 read-only/no-save는 그대로 강제하고, 명시적으로 요청된 텍스트 파일 저장을 일괄 차단하지 않는다. 이는 문구 축약보다 먼저 정합성을 해결할 항목이다.

### F07 · P2 · 캐릭터 경로가 조건부 참조를 무조건 읽힌다

**근거:** `creative-production/references/routing.csv` R03; `designing-video-character-sheets/SKILL.md:55–59,77`.

R03의 required_read는 `appearance-language-catalog.md`를 항상 포함한다. 그러나 전문 스킬 본문은 헤어·메이크업·의상을 새로 선택/비교할 때만 읽으라고 한다. 이 표만으로 매번 **1,102토큰**이 추가된다.

신규 캐릭터는 compact에서도 persona 전문 패킷을 소비하고, 명시적 신규 허구 위임이면 both lens가 기본이다. 이는 기존 기능 계약이므로 삭제하면 안 되지만, 설명과 출력 양식에 같은 provenance/voice/handoff 의미를 여러 번 적게 된다.

**제안:** appearance 조건을 라우팅/본문에서 일치시키고, persona→sheet 통합에서 공통 정보는 한 번만 작성해 ID로 참조한다. MBTI/Enneagram 기본값이나 필수 음성 큐를 성능 핑계로 임의 변경하지 않는다. full 0–33 SSOT와 compact 분리는 이미 있으므로 그 분기를 실제 읽기 단위까지 반영한다.

### F08 · P2 · 공급자 진입점에 비실행·역사적 레시피가 너무 많다

**근거:** `higgsfield-generate/SKILL.md:29–31,80–156`; `higgsfield-video-replicate/SKILL.md:60–91,126–150`; `higgsfield-video-explainer/SKILL.md:35–65,149–170`.

현재 계약을 확인해야 한다는 원칙은 맞다. 그러나 메인 본문에 역사적 모델 표, 사용 금지 이미지 예제, 여러 종류의 생성 명령, 과거 기능/가격 경고가 남아 있어 현재 실행 경로보다 아카이브 설명을 먼저 읽는 비중이 크다. 반복되는 '현재 스키마 재확인'도 한 실행 요청의 같은 계약을 여러 번 조회하라는 의미로 오독될 수 있다.

Explainer는 2026-10-16의 assembler 미발견 기록과 그 경로의 차단 조건을 보유한다. **이 감사에서 현재 API 가용성을 조회하지 않았으므로 현재도 서비스가 없다고 판정하지 않는다.** 실행 전 빠른 capability 점검으로 막을 일과 전체 10초 블록 제작 매뉴얼은 분리할 수 있다.

**제안:** 코어에는 적격성/범위/참조/타임아웃·재시도 안전성만 남기고, 역사적 모델표와 금지 레시피는 명시적 archive로 옮긴다. 승인된 한 배치 안에서 확인한 계약은 버전·시각·설정과 함께 재사용하되, 입력/계정/모델/서버 revision 변경 시 다시 확인한다. 오래된 표를 현재 사실로 승격시키는 최적화는 금지한다.

### F09 · P2 · 정확한 문장 중복 제거만으로는 충분하지 않다

[metrics.json]에서 여러 파일에 반복되는 긴 동일 문단은 **26종**이고, 단순 공유화의 텍스트 합계상 절감 상한은 약 **3,739토큰**이다. 전체 674,471토큰의 약 **0.55%**다. 이는 실행당 절감량이 아니며, 유용한 국소 안전 포인터도 포함한다.

특히 최근 추가한 종속 생성/연속성 포인터는 3개 실행 진입점에 중복되어 있다. 그러나 바로 그 국소 포인터가 단독 실행 우회를 막는다. 지우기보다 **짧은 발동 조건 + 정본 절차 링크**로 줄여야 한다.

문서 링크 그래프에서 순환이 존재하는 것은 맞지만, 그 자체로 무한 실행 루프를 증명하지 않는다. 기존 스킬들은 delegated/no-reroute 조건을 둔다. 그래프의 모든 노드를 재귀적으로 읽으라는 규칙으로 오해하지 않게 '현재 단계만/한 번/담당 패킷'을 유지하는 편이 안전하다.

### F10 · P2 · 실제 validator에서도 요청 내 중복 검사가 있다

**근거:** `video-production-assets/scripts/generation_handoff.py:92–146`, `validate_sequence.py:34–59,197–200`; [validation-benchmark.json].

| 합성 fixture | 실제 FFprobe 호출 | 서로 다른 명령 | 동일 명령 중복 | hash 호출 / 고유 파일 | 중앙 실행 시간 |
|---|---:|---:|---:|---:|---:|
| 인접 선행 컷 | 5 | 5 | 0 | 41 / 28 | 0.087초 |
| 인서트 뒤 이력 복귀 | 10 | 5 | 5 | 55 / 37 | 0.835초 |

각 fixture를 3회 실행했다. 같은 파일의 stream 조회와 frame 조회는 다른 명령이므로 무조건 중복이라고 세지 않았다. 이력 fixture에서 동일한 5개 명령이 두 번씩 실행되는 것은 재현됐다.

**한계:** 두 fixture는 보드 이미지 크기와 구조도 다르다. 실행 시간 차이를 모두 FFprobe 중복 탓으로 돌리거나 생산 영상 속도 향상률을 예측할 수 없다. 작은 인접 fixture는 이미 0.1초 미만이므로, 현재 우선순위는 CPU보다 문맥/조회 구조다.

**제안:** 한 검증 호출 안의 같은 소스 probe와 테이블 인덱스를 재사용한다. 버전/해시/경로가 달라지면 재사용하지 않는다. 전후 해시 비교는 파일 변경 탐지 목적일 수 있으므로 41회를 고유 파일 수로 무조건 줄이면 안 된다. 실제 호출 직전 재검사, 소스 계보/범위, 최종 이미지/오디오 검수는 유지한다.

### F11 · 별도 비디오 외 범위 · 웹 스킬의 turn 절약 규칙은 과도하다

**근거:** `higgsfield-websites/SKILL.md`의 `Turn economy` 및 '다른 디자인 지침을 찾지 말라' 절; `references/website-flow.md:274–294`.

웹 스킬은 4,410토큰이고 선택적 `design-taste-frontend.md`만 22,031토큰이다. 그러나 그 플레이북은 심화 참조이므로 모든 웹 작업이 이를 필수로 읽는다고 판정하지 않는다. 흐름에서 short recipe와 deep-dive를 구분한 점은 장점이다.

문제는 '파일을 한 번만 완성해서 쓰기', 'write-then-patch 금지', '방금 쓴 파일을 다시 읽지 말기'가 절대 표현으로 적힌 점이다. 이는 실제 테스트 실패/보안 수정/시각 QA 후 수정을 방해할 수 있다. **이번 감사에서 웹 빌드나 사용자 사이트 변경을 수행하지 않았으므로 실행 실패를 재현한 것은 아니다.**

**제안:** 불필요한 반복 읽기/마이크로 편집을 줄인다는 목적만 유지하고, 실패 진단·테스트·실제 수정 확인은 허용한다고 명확히 한다. host/user 지침보다 전문 스킬이 우선하는 것으로 읽히는 표현도 바로잡는다. 이 4개 스킬의 변경은 비디오팩 25개 배포와 별도 범위로 다룬다.

## 6. 29개 개별 판정

아래 우선순위는 이번 무게/정합성 감사의 상대적 판단이며 보안 인증이나 모델 행동 성능 점수가 아니다.

| 스킬 | 본문 토큰 | 판정 | 권장 조치 |
|---|---:|---|---|
| video-production-assets | 7,093 | 최우선 | 단일 모듈/전체 패키지/카탈로그/공통 계약 로딩 분리 |
| higgsfield-video-explainer | 4,620 | 높음 | capability preflight와 블록 제작 실행 매뉴얼 분리 |
| higgsfield-generate | 4,540 | 높음 | 현행 실행 코어와 역사적 모델/금지 이미지 레시피 분리 |
| higgsfield-websites * | 4,410 | 별도 높음 | 세 product type 분기 우선, turn 절약 절대 규칙 완화 |
| higgsfield-video-replicate | 3,716 | 높음 | 모드/예제 표는 선택 참조로; 역사/채택 연속성 게이트 유지 |
| higgsfield-brandkit * | 3,407 | 별도 중간 | apply-existing/extend/create 분기 뒤 필요한 state/모듈만 읽기 |
| blender-previsualization | 3,307 | 높음 | 1,892토큰 실행 문단의 CLI·모드 매뉴얼을 분리 |
| silent-satire-animatic | 3,303 | 중간 | 서사/비트 예산 코어와 구현/클리핑/BGM/썸네일 운영 분리 |
| storyboarding-video | 3,272 | 최우선 | 단계별 계약 로딩; 완전성·전체 커버리지 유지 |
| designing-video-character-sheets | 3,183 | 높음 | compact/full SSOT, appearance 조건, persona 통합 중복 정리 |
| recording-production-history | 2,717 | 중간 | 사용법/라이프사이클과 내부 원자성·보안 상세 설명 분리 |
| camera-spatial-design | 2,690 | 중간 | numeric-only와 실제 검증 분기 선명화; 조건부 카탈로그 절 조회 |
| orchestrating-video-preproduction | 2,277 | 중간 | no-save 용어 충돌 해소; 중복 하위 납품 설명 축소 |
| higgsfield-youtube-thumbnail | 2,127 | 높음 | 비사용 공급자의 auth/quote 전제 제거 우선 |
| higgsfield-product-photoshoot * | 2,091 | 별도 중간 | 사용 불가 private backend 레시피를 코어 밖 보관 |
| higgsfield-soul-id | 1,895 | 중간 | 훈련 코어와 비실행 downstream 이미지 예제 분리; 동의 유지 |
| designing-character-personas | 1,857 | 중간 | 필수 cue 계약 보존; core/선택 typology/선택 voice 구획 개선 |
| creative-production | 1,801 | 중간 | 라우팅 원칙 유지; 누락 의존성 해결; 후속 실행 상세 이동 |
| topic-demand-selection | 1,697 | 낮음 | 수요와 사실 분리 유지; 사례/긴 provenance를 참고로 이동 가능 |
| higgsfield-marketplace-cards * | 1,685 | 별도 중간 | 실제 가능한 narrower path와 비실행 enhancer 아카이브 구분 |
| storytelling-with-still-images | 1,549 | 낮음 | 짧은 cue 절차는 유지; 긴 원전 판본/해시 부록화 후보 |
| silent-visual-storytelling | 1,464 | 낮음 | 범위가 좁고 완료 기준 명확; 예제/긴 복합 문장 가독성 개선 정도 |
| ai-camera-control | 1,399 | 낮음 | HARD/SOFT/미지원 유지; 환경 공통 부분 짧은 포인터화 |
| animatic-direction | 1,240 | 낮음 | 작은 진입점 구조 유지; 시간화와 렌더 경계 보존 |
| searching-social-media | 1,224 | 낮음 | 예산/실패 상태/관측 경계가 이미 분리됨; 과도한 축약 불필요 |
| community-shorts-stills-pipeline | 1,153 | 중간 | 단일 메타데이터/배속 요청도 모든 운영 문서를 열지 않게 단계 선택 |
| developing-video-synopses | 1,083 | 낮음 | logline 등 좁은 요청은 craft의 해당 절만 읽도록 주소 명시 |
| camera-motion-reference-analysis | 975 | 낮음 | 관측/추정 분리와 조건부 도구 조회가 양호 |
| open-3d-production | 849 | 낮음 | 적은 코어 + 선택 모듈 구조가 좋은 비교 사례 |

`*`: manifest 비목록이지만 이 저장소에 연결된 추가 스킬. 별도 패키지 경계를 유지한다.

## 7. 유지해야 할 좋은 설계

1. 라우팅이 CSV의 명시적 owner/required_read를 사용하고, 모호한 '관련 가이드' 문장보다 실제 경로를 제시한다. 비용 때문에 무조건 표를 없애면 정확도 퇴행 위험이 있다.
2. 단독 호출과 delegated 호출의 재라우팅 금지가 있어 불필요한 2차 인터뷰/원장 생성을 억제한다.
3. 사용자 수락·검토 준비·실행/비용·공개 권한을 구분한다.
4. 실제 채택 선행 구간/재등장 이력/오디오를 native selected references와 연결하고, missing/unverified는 차단하는 게이트가 있다. 이를 단순 '이전 컷을 고려하라'로 되돌리면 안 된다.
5. 최종 산출물·소스/파생 계보·버전 핀·실제 검사 상태를 구분한다. 성능 개선은 이 계약 아래에서 해야 한다.
6. manifest 25개 Markdown의 로컬 링크 750개는 파일 대상 누락 0개였다. 추가 4개까지 813개로 넓혔을 때 잡힌 2개는 `inline-widgets.md:26–27` 코드 예제 안의 `/absolute/path/to/board.*` 자리표시자였다. 실제 끊어진 문서 링크로 보고하지 않았다.
7. 버전·라우팅·연속성·패키지 경계 회귀 검사 47개가 통과했다. [regression-checks.txt] 이 감사에서 모든 기존 테스트나 실제 에이전트/공급자 실행을 새로 검증한 것은 아니다.

## 8. 현실적인 최적화 목표와 검증 기준

### 8.1 먼저 할 일

- 포커스 뷰를 도입해 전체 실행 투영을 LLM 읽기 입력으로 자동 덤프하지 않는다. 필요한 이력·선행 소스·버전 핀·실제 호출 참조·blocker를 누락하지 않는 테스트를 함께 둔다.
- assets/core contract/스토리보드 contract를 읽는 단계로 나눈다. 동일한 필수 필드·범위·승인·연속성 판정을 유지하는 것을 회귀 기준으로 삼는다.
- 이미지 실행자별 auth/quote 조건과 text-only/no-save 용어를 정리한다. 이는 '적게 읽기'가 아니라 잘못된 차단·재질문을 없애는 작업이다.

### 8.2 줄일 수 있는 양: 목표와 실측을 구별

**제안 예시이지 달성 결과가 아니다:** 조명 계획 프로필에서 assets 진입점 7,093→1,200토큰, 그 작업의 공통 계약 읽기 8,029→1,800토큰을 목표로 잡으면 파일 합집합 22,538→약 10,416토큰, 약 **54% 축소**다.

계산: `22,538 - (7,093 - 1,200) - (8,029 - 1,800) = 10,416`.

1,200/1,800은 설계 예산일 뿐, 해당 분량으로 모든 계약을 보존할 수 있음이 검증된 값이 아니다. 원래 작업이 두 문서 전체를 읽지 않았다면 절감은 더 작다. 조건부 참조를 다시 많이 읽으면 효과도 줄어든다. 이 숫자를 응답 속도/비용/품질 개선률로 바꾸지 않는다.

### 8.3 최적화 후 합격 기준

1. 같은 대표 요청으로 baseline/변경안의 실제 파일 읽기 경로·토큰·도구 호출·대화 수를 비교한다. 메인 파일만 짧아지고 더 많은 참조를 읽는 경우는 실패다.
2. 로그라인, 단일 조명, compact/full 캐릭터, 일반/러프 콘티, 텍스트 파일 저장, 이미지 패키지, 새 앵글 후속 생성, 인서트 뒤 재등장, 무음, 미지원 transport, 타임아웃 복구를 모두 넣는다.
3. 필수 슬롯/이력·native ref 선택/지원 미확인 차단/사용자 승인 경계를 잃지 않는다. 기존 정상 컷과 입력 버전을 보존한다.
4. 라우팅·required_read의 경로 가시성을 유지한다. 구조 검사만으로 실제 에이전트 준수·시각 품질을 증명했다고 말하지 않는다.
5. 공급자 실제 제출 없이 가능한 계약·fixture 회귀를 먼저 실행한다. 실제 생성 비교는 별도 승인된 범위에서만 한다.
6. 배포 시 관리 25개와 비목록 4개의 소유 경계를 구분하고, 실제 설치 경로/해시/새 세션 재로딩을 확인한다.

## 9. 한계와 상태

- 이번 결과는 직접 수행한 정량/소스/로컬 실행 감사다. 별도 독립 에이전트 리뷰나 29개 스킬의 신선한 문맥 행동 A/B는 수행하지 않았다.
- 현재 공급자 가격·계정·모델/assembler 가용성을 조사하지 않았다. 역사적 예제의 가용성을 현재 사실로 단정하지 않는다.
- 274개 전체 참조의 모든 내용/외부 링크/책 원문/미디어를 수동 정독·재생한 감사는 아니다. 스킬 본문 29개 전수 읽기, 정량 스캔, 핵심 정본/분기 대조와 명시한 실행 실험이 범위다.
- 실제 사용자 제작 폴더, 원본 미디어, 설치 링크, Git 이력은 변경하지 않았다. 기존 미커밋 routing/분석 자료도 보존했다.
- 변경 제안은 아직 구현·커밋·푸시·배포되지 않았다. 이 보고서는 다음 최적화 범위를 정할 근거이며 완료된 최적화의 검증 보고서가 아니다.
