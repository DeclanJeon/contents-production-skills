# 모션그래픽 파이프라인·Prompt Motion 코퍼스 흡수 작업지시서

> 실행: superpowers:executing-plans(인라인, 서브에이전트 미승인). 아래 **큐**가 유일한 진행 원장이다. 항목을 끝내면 `[x]`와 증거를 적고, 막히면 `[!]`와 이유를 적는다. 큐가 소진될 때까지 진행한 뒤 진행률(완료 항목 수 ÷ 전체 항목 수)을 보고한다.

**설계:** [2026-11-23-prompt-motion-corpus-absorption-design.md](../specs/2026-11-23-prompt-motion-corpus-absorption-design.md) (승인됨)
**목표:** 모션 요구 감지 → 분석 → 연출 판단 → 설계 → 실제 렌더 → 검수(M1~M6)를 기존 스킬에 넣고, Prompt Motion 코퍼스에서 추출한 형식과 기법으로 판단 근거를 제공한다.
**저장소:** S = `contents-production-skills`(이 저장소), C = `~/Documents/Projects/Products/01_Persnal_Work/cineforge`
**입력(읽기 전용):** A = `~/Documents/Media_Studio/hwasan-seoyun-68-69/source/prompt-motion/`(prompts.csv sha256 `1bc3b16ebdf61d3176bcaaf9ddb9dc6c2157bbd33b9fae13d5cff7d789f55e8e`, gifs/)
**기준선:** S pytest 1331 통과/5 건너뜀, C pytest 156 통과/2 건너뜀(2026-11-23)

## 공통 규칙
- 기존 미커밋 변경(`docs/superpowers/plans/2026-11-21-audio-caption-resume.md`, `.ultragoal/`, `.worktrees/`, `ai-delegation-loop/`, 2026-11-21 스펙 2개)은 건드리지 않는다.
- 아카이브 원문·GIF·CSV는 S에 넣지 않는다. 원문에서 연속 8단어(한국어는 연속 20자) 이상을 그대로 옮기지 않는다.
- 코드 변경은 테스트를 먼저 쓰고 실패를 확인한 뒤 구현한다.
- 커밋과 푸시는 사용자 확인 후에 한다(이 작업지시서 범위 밖).
- 렌더 시연 산출물은 `~/Documents/Media_Studio/motion-pipeline-demo/` 아래에 둔다.

## 파일 지도
| 파일 | 책임 |
|---|---|
| S `scripts/prompt_motion_ledger.py` | 아카이브 → 원장 키·해시·묶음·근거 생성, 수동 코딩 병합, `--verify` 원문 대조 |
| S `docs/research/prompt-motion-coding.csv` | 묶음 대표별 수동 코딩(format, techniques, disposition, target, reason) — 원문 없음 |
| S `docs/research/prompt-motion-absorption-ledger.csv` | 생성된 450행 원장(대체: `prompt-motion-gallery.tsv` 삭제) |
| S `scripts/test_prompt_motion_corpus.py` | 원장·위생·단일 정본·근거 표현 검사 |
| S `video-production-assets/scripts/render_html_motion.mjs` | Chrome CDP + ffmpeg 결정적 렌더러 |
| S `video-production-assets/scripts/test_render_html_motion.py` | 렌더러 테스트(Chrome 없으면 건너뜀) |
| S `creative-production/references/motion-pipeline.md` | M1~M6 정본, 분석표, 후보 비교, 구현 매트릭스 |
| S `creative-production/references/motion-selection.md` | 리다이렉트 한 줄 |
| S `video-production-assets/assets/code-motion-brief-template.md` | 6칸 브리프 |
| S `scripts/test_motion_pipeline.py` | 파이프라인 문서·매트릭스·템플릿·포인터 검사 |
| S 08b, 08a, realtime-motion-direction, SKILL 3개, module-index, craft-bridge.csv | 기법 정본 반영과 포인터 |
| S `scripts/agent_read_probe.py`, `creative-production/evals/agent-read-probes.json` | `expect_none_read`·`expect_text` 판정 추가, pm1~pm4 |
| C `cineforge/execution_plan.py`, `jobs.py`, `schemas`/검증 지점, tests | `code-motion` 레인, `motion_brief` 필드 |

## 큐

### Q01 프로브 확장과 기준선(RED)
- [x] Q01.1 `scripts/test_agent_read_probe.py`에 테스트 추가: positive 케이스에 `expect_none_read`의 파일이 열리면 실패, `expect_text`의 문자열 그룹(각 그룹은 대안 목록, 하나라도 있으면 그룹 충족)이 빠지면 실패. 실패 확인. — 증거: 2 failed(새 테스트)
- [x] Q01.2 `agent_read_probe.judge` 구현. 기존 케이스 id 목록 테스트를 pm1~pm4 포함으로 갱신. — 증거: 판정 테스트 통과
- [x] Q01.3 `agent-read-probes.json`에 pm1~pm4 추가: — 증거: 13 케이스
  - pm1 positive "앱 출시 30초 모션그래픽 영상 만들어줘. 앱: 가계부 앱 '모아', 시청자: 사회초년생." expect_any_read=[motion-pipeline.md], expect_text=[["분석"],["연출안","후보"],["브리프"],["경로","local","code"]]
  - pm2 positive "재귀가 뭔지 설명하는 1분 모션 영상 기획해줘" expect_any_read=[motion-pipeline.md], expect_text=[["diagram_data","explainer","설명형"]]
  - pm3 positive "실사 카페 광고 30초, 마지막 컷에 가격표 애니메이션" expect_any_read=[motion-pipeline.md], expect_text=[["가격표"],["실사"]]
  - pm4 positive "실사 인터뷰 영상 컷 편집 계획 세워줘. 그래픽은 넣지 않아." expect_any_read=[creative-production/SKILL.md], expect_none_read=[motion-pipeline.md, 08b-code-motion-production.md]
- [x] Q01.4 기준선: 현재 패키지로 `python3 scripts/agent_read_probe.py --only pm1,pm2,pm3,pm4 --out qa/2026-11-23-motion-pipeline/baseline` 1회 실행. 결과 기록(motion-pipeline.md가 아직 없으므로 pm1~pm3은 실패가 정상). — 증거: qa/2026-11-23-motion-pipeline/baseline (pm1~3 FAIL, pm4 PASS)

### Q02 코퍼스 원장
- [x] Q02.1 `scripts/test_prompt_motion_corpus.py` 작성(원장 450행, 고유 키, 열거값, 변형별 234/211/2/3, absorb·example의 target 존재, reference·exclude의 reason, 위생 검사). 실패 확인. — 증거: 5 failed(원장 없음)
- [x] Q02.2 `scripts/prompt_motion_ledger.py` 구현: `build ARCHIVE --coding CODING --out LEDGER`, `--verify ARCHIVE`(스냅샷 해시와 S의 마크다운에서 원문 8단어 연속 일치 탐지). 원문은 출력하지 않는다. — 증거: build/groups/verify 명령, 원장 450행 생성
- [x] Q02.3 묶음 대표(원문 203 + 개선본 158 + 템플릿 2 + 스킬 3)를 읽고 `prompt-motion-coding.csv`에 형식·기법·처분을 코딩한다. 코딩은 `dup_group` 단위로 하고, 형식별 5행 이상은 재검토한다. — 증거: 묶음 365개 코딩(정규식 초안 → 365줄 전수 판독 후 형식 49건 수정)
- [x] Q02.4 기법별 근거 집계(서로 다른 묶음 수와 근거 수준) → absorb/example 확정. 집계표를 `docs/research/prompt-motion-inventory.md`에 기록. — 증거: 인벤토리 기법 근거표, absorb 48 묶음(기법 16개 × 대표 3), style-as-concept 문턱 미달
- [x] Q02.5 원장 생성, `prompt-motion-gallery.tsv` 삭제, 인벤토리 링크 갱신. 원장 테스트 통과. — 증거: TSV 삭제, 원장 테스트 4/5 통과(target 앵커는 Q05·Q06에서 해소)

### Q03 시각 확인
- [x] Q03.1 absorb 근거 예제와 형식별 대표 2개씩의 GIF에서 컨택트 시트(균등 8프레임)를 `/tmp` 아래에 만든다. — 증거: 24개 GIF 컨택트 시트(/tmp/pmc/sheets, 임시)
- [x] Q03.2 시트를 직접 보고 기법이 실제로 보이는지 판정해 코딩 CSV의 `visual_check`에 기록하고 원장을 다시 생성한다. — 증거: visual_check pass 17 · mismatch 1, 인벤토리 '시각 확인' 절

### Q04 코드 렌더러
- [x] Q04.1 `test_render_html_motion.py` 작성: 픽스처 HTML(0.5초, 12fps, 160×90)을 렌더해 프레임 수 6, 길이, 해상도, 결정성 pass, 리포트 필드, 비결정 픽스처(`Math.random`) 거부, 외부 URL 요청 거부, 음원 길이 불일치 실패, 컨택트 시트 생성을 확인. 실패 확인. — 증거: 6 failed(스크립트 없음)
- [x] Q04.2 `render_html_motion.mjs` 구현(Node 24 내장 WebSocket, Chrome `--headless=new`, `Page.captureScreenshot`, ffmpeg `image2pipe` → H.264 yuv420p). 테스트 통과. — 증거: 6 passed(프레임 수·결정성·네트워크 차단·계약 누락·음원 길이·구간 재렌더)

### Q05 파이프라인 문서
- [x] Q05.1 `scripts/test_motion_pipeline.py` 작성: motion-pipeline.md의 M1~M6 절, 분석표 11칸, 평가 기준 4개, downgrade 기록 규칙, 매트릭스 `local` 행 = C `local_motion.RECIPES`(C 없으면 건너뜀), 브리프 6칸, Step 1 포인터, craft-bridge 행, 08b의 렌더 경로 절과 렌더러 경로, motion-selection 리다이렉트. 실패 확인. — 증거: 12 failed(문서 없음)
- [x] Q05.2 motion-pipeline.md, 브리프 템플릿, motion-selection 리다이렉트 작성. — 증거: motion-pipeline.md(M1~M6·분석표 11칸·형식 표·레시피 표·매트릭스), 브리프 템플릿, motion-selection 리다이렉트
- [x] Q05.3 `creative-production/SKILL.md` Step 1 모션 문장 교체(frontier 2,900 단어 상한 유지), craft-bridge.csv 갱신, video-production-assets SKILL·module-index 포인터. — 증거: Step 1 교체(frontier 2,898→2,895 단어), craft-bridge 행 추가·08b 비고, VPA SKILL·module-index·README·인벤토리 링크
- [x] Q05.4 테스트 통과, 기존 craft-bridge·frontier·routing 테스트 통과. — 증거: test_motion_pipeline 11/12(08b 렌더 절은 Q06), craft-bridge·entry·closing 테스트 통과

### Q06 기법 정본 반영
- [x] Q06.1 테스트 추가(test_prompt_motion_corpus): absorb 기법마다 `{#t-…}` 앵커 정본이 정확히 한 파일에 있음, 출처 줄 있음, untested만 근거인 절에 "확인"·"효과" 같은 주장 단어 없음, "예제에서 확인" 문구 절은 visual_check=pass 행을 가짐. 실패 확인. — 증거: 기법 정본·출처 줄·근거 표현 테스트 2 failed 확인
- [x] Q06.2 08b(형식 구조, 기법 절, 코드 렌더 경로 절), 08a, realtime-motion-direction 반영. 08b 증가분 +120줄 초과 시 08c 분리. — 증거: 08b +101줄(코드 렌더 경로, 기법 11개), 08a 기법 3개, realtime T-3d-gotchas, 브리프 T-inputs-default — 08c 분리 불필요
- [x] Q06.3 테스트 통과, `prompt_motion_ledger.py --verify A` 통과(원문 8단어 일치 0). — 증거: test_prompt_motion_corpus 8/8, verify problems 0(숫자 위주 run 제외·생성 support 제외 보정)

### Q07 CineForge 연결
- [x] Q07.1 C 테스트: 실행 계획 레인 `{kind: video_cut, provider: code-motion, model, max_jobs}` 허용(비용 필드 없음), 다른 kind에 code-motion 거부, 작업 봉투의 tool=`render_html_motion`, 영수증 기록과 해시 고정, `production_spec.motion_brief` 키·열거값 검증(잘못된 route 거부). 실패 확인. — 증거: tests/test_code_motion_lane.py 8 failed(레인·tool·스키마 미구현) 확인
- [x] Q07.2 구현. C 전체 테스트 통과. — 증거: execution_plan·jobs·plan.schema(motion_brief, route_by_cut은 [{cut, route}] 목록)·pipeline craft_refs(motion-pipeline·브리프 템플릿)·planner 지시. C 전체 166 passed/2 skipped

### Q08 실제 렌더 시연(GREEN 증거)
- [x] Q08.1 데모 A `product_film` 16:9 30초(가상 앱, 플레이스홀더 자산): M2 분석표, M3 후보 비교, M4 브리프와 컷 표 작성 → code 경로 렌더 → 리포트, 결정성, 컨택트 시트, M6 체크리스트 판정. — 증거: ~/Documents/Media_Studio/motion-pipeline-demo/edit/A-product-film.mp4(1920×1080·30s·900f, 결정성 6/6), qa/A-review.md 10개 항목 PASS, 출력 기반 수정 4회
- [x] Q08.2 데모 B `explainer` 9:16 20초: 동일 절차, code 경로. — 증거: edit/B-explainer.mp4(1080×1920·20s·600f, 결정성 6/6), qa/B-review.md 8개 항목 PASS, 출력 기반 수정 2회
- [x] Q08.3 데모 C `showreel` 9:16 15초: local(`cineforge motion` kinetic_type) 컷과 code 컷 혼합 → 조립 → 검수. — 증거: edit/C-showreel.mp4(720×1280·15s·450f), local 1컷 + code 2컷, qa/C-review.md 6개 항목 PASS. 정정: local 해상도는 720×1280(문서·설계 수정, 테스트 추가)
- [x] Q08.4 데모 하나를 C 프로젝트 흐름(`code-motion` 레인 → 봉투 → results 영수증)으로 기록. — 증거: motion-pipeline-demo/qa/cineforge-flow.md — 실행 계획(비용 없음)→승인→봉투 20작업(tool render_html_motion)→영수증 sha256 고정·변조 거부. 픽스처 프로젝트 사용, 납품 단계 미확인

### Q09 검증
- [x] Q09.1 프로브 pm1~pm4를 3회 실행(`qa/2026-11-23-motion-pipeline/run{1,2,3}`). 기존 9건 중 영향받을 수 있는 p 계열은 1회 회귀. — 증거: qa/2026-11-23-motion-pipeline/probe-results.md — 모션 판정 pm1 3/3·pm2 3/3·pm3 2/3·pm4 3/3(기준선 pm1~3 FAIL). 전체 판정은 기존 F1 마감 줄 결함으로 pm1 2/3·pm2 0/3·pm3 2/3·pm4 3/3. 설계 기준(각 3/3) 미달: pm3. 회귀 p2~p5·n1~n3 PASS, p1 마감 줄 FAIL
- [x] Q09.2 S 전체 pytest, `check_versions.py`, `routing_regression.py`. C 전체 pytest. — 증거: S pytest 1360 passed/5 skipped, check_versions OK(27 skills), routing_regression 79건 실패 0, C pytest 180 passed/2 skipped(작업 중 다른 세션의 CineForge 변경 포함)

### Q10 마감
- [x] Q10.1 버전 올림(video-production-assets 1.34, creative-production 2.8, open-3d-production 1.2, 패키지 2.64), CHANGELOG 기록, `scripts/sync_installed.py` 실행. — 증거: creative-production 2.8·video-production-assets 1.34·open-3d-production 1.2, CHANGELOG Unreleased 항목 5개, sync_installed skipped=81(링크 정상). 패키지 버전 2.64 승격은 기존 Unreleased 항목까지 묶는 릴리스 결정이라 하지 않음
- [x] Q10.2 검증 기록 `qa/2026-11-23-motion-pipeline/validation.md` 작성(각 항목 PASS/FAIL/UNVERIFIED와 증거). — 증거: qa/2026-11-23-motion-pipeline/validation.md(12항목: PASS 9·부분 PASS 2·FAIL 1)
- [x] Q10.3 진행률 산출과 보고. — 증거: 큐 31/31 실행(100%). 수락 기준 미달 1건(행동 프로브 pm3 2/3)
