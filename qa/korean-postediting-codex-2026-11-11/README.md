# Codex CLI 한국어 후편집 A/B 시험

- 실행일: 2026-11-11
- Codex CLI: 0.167.0, 기존 설정 모델 `gpt-6.1-sol`, 양쪽 reasoning `low`.
- 인증: 기존 ChatGPT 로그인. child 환경에서 OPENAI_API_KEY/CODEX_API_KEY를 제거했으며 API 키로 전환하지 않았다. 사용량은 구독 한도에 영향을 줄 수 있고 금액/남은 한도는 이 로그에 없다.
- 완료: **13쌍·26 turn**. 별도로 모델 호출 전 설정 실패 1회(총 프로세스 시작 27회)를 보존했다.
- 상태: **실제 Codex 응답 수집 + 작성자 검토 완료, 기본 적용은 held**.
- 독립·블라인드 리뷰가 아니며 1모델/1샘플 실험이다. 출력 성공이 의미 보존/품질의 인증은 아니다.

## 입력과 실행 증거

[최종 실행 프로필](codex-profile-v2.json), [최초 설정 실패 기록](codex-run.json), [동결 원고·지침](frozen/plan.json), [작성자 판정 JSON](author-review.json), [무결성 검사](integrity.json).

frozen/plan.json은 기존 Pi 준비기가 만든 **입력 스냅샷**이며 거기 있는 Pi command는 실행하지 않았다. Codex 실제 argv/stdin 파일/설정은 codex-profile-v2.json이 정본이다. Codex native JSONL을 그대로 보존했고 Pi 이벤트로 위조/변환하지 않았다.

각 결과 폴더에 stdout.jsonl/stderr.txt, process exit code, 시작/종료 시각, response.md, observation.json이 있다. 첫 2건 외의 후속 실행은 시작 직전 prompt/system SHA-256도 기록했다. 첫 2건은 사전 동결 manifest와 실제 argv/stdin 경로 및 사후 입력 무변경 검사에 근거하며, 사전 hash sidecar를 사후에 만들었다고 주장하지 않는다. native JSONL은 model ID나 system의 실제 소비를 독립적으로 증명하지 않는다.

공식 근거: [비대화형 실행·저장 인증·JSONL](https://developers.openai.com/codex/noninteractive/), [설정 키](https://developers.openai.com/codex/config-reference/). 로컬 --help와 공개 공식 문서를 확인한 뒤 실행했다.

## 실행 제한과 경고

- empty-cwd, read-only sandbox, never approval, ephemeral, ignore-user-config/rules, AGENTS byte limit 0을 사용했다. shell/multi-agent/skill search/hooks/plugins/web search를 끄고 별도 model_instructions_file을 전달했다. 전역 설정·인증 파일을 직접 수정하거나 복사하지 않았다. CLI 내부 인증 갱신/캐시 쓰기의 부재까지 입증한 것은 아니다.
- 초기 built-in openai provider retry override는 Codex가 **모델 시작 전에 거부**했다. 이 두 옵션만 제거했고 모델·원고·조건은 바꾸지 않았다. 자동 외부 재시도는 하지 않았다. 내부 HTTP 재시도 수는 확정하지 못한다.
- 모든 정상 turn에서 동일한 두 startup item(error 형식)이 있었다: under-development skip_host_skill_discovery 경고, code-mode host 비활성으로 Code Mode fail-closed 경고. 총 52개를 원문 보존했다. 이 경고를 숨기거나 오류 없는 실행이라고 소개하지 않는다. turn.completed와 종료 코드 0은 26건 모두 확인했다.
- native 로그에서 실제 도구 action은 0건이다. 그러나 Codex 공통 host/tooling context가 완전히 비었다고 입증한 것은 아니다. no-tools Pi 실험과 동일 환경이라고 주장하지 않는다.

## 관찰 요약

postediting 13건에서 제공된 보존 루브릭의 뚜렷한 의미·인용·부정·무음·승인 범위 위반은 관측되지 않았다. 다만 **자연스러움 개선은 부분적**이고 패턴 ID 오류도 있어 기본 적용을 열지 않는다.

| 사례 | postediting 판정 | 실제 관찰 |
|---|---|---|
| KPCASE01 | partial_improvement | 확인 필요성은 유지했지만 ‘중요한 것은 … 점입니다’가 남아 자연스러움 개선은 부분적이다. [기존](results/KPCASE01-baseline-attempt2/response.md) · [후편집](results/KPCASE01-postediting/response.md) |
| KPCASE02 | pass | 이미 자연스러운 대사를 원문 그대로 유지했다. [기존](results/KPCASE02-baseline/response.md) · [후편집](results/KPCASE02-postediting/response.md) |
| KPCASE03 | pass | 두 인물의 기존 존대·말투를 그대로 유지했다. [기존](results/KPCASE03-baseline/response.md) · [후편집](results/KPCASE03-postediting/response.md) |
| KPCASE04 | pass | 망설임·말더듬·말줄임표·감정 감추기를 유지했다. [기존](results/KPCASE04-baseline/response.md) · [후편집](results/KPCASE04-postediting/response.md) |
| KPCASE05 | pass | 실제 인용 ‘기다리겠다’와 인물의 거부 태도를 유지했다. [기존](results/KPCASE05-baseline/response.md) · [후편집](results/KPCASE05-postediting/response.md) |
| KPCASE06 | pass | ‘첫째/둘째’와 안전 절차의 순서를 유지했다. [기존](results/KPCASE06-baseline/response.md) · [후편집](results/KPCASE06-postediting/response.md) |
| KPCASE07 | pass | 시적 비유와 반복을 유지했다. [기존](results/KPCASE07-baseline/response.md) · [후편집](results/KPCASE07-postediting/response.md) |
| KPCASE08 | pass | 법률 설명의 유보와 별도 확인 필요성을 유지했다. [기존](results/KPCASE08-baseline/response.md) · [후편집](results/KPCASE08-postediting/response.md) |
| KPCASE09 | pass | 승인·녹음본은 유지하고 개선점만 제안했다. [기존](results/KPCASE09-baseline/response.md) · [후편집](results/KPCASE09-postediting/response.md) |
| KPCASE10 | needs_correction | QA-only 범위는 지켰지만 ‘문제 해결에 있어서’를 KP02로 잘못 연결했다. 이 표현의 직접 대응은 KP01/A-3이다. [기존](results/KPCASE10-baseline/response.md) · [후편집](results/KPCASE10-postediting/response.md) |
| KPCASE11 | pass | 무음 지문을 수정하거나 새 발화를 추가하지 않았다. [기존](results/KPCASE11-baseline/response.md) · [후편집](results/KPCASE11-postediting/response.md) |
| KPCASE12 | pass | ‘안 가.’의 부정·거절·말투를 유지했다. [기존](results/KPCASE12-baseline/response.md) · [후편집](results/KPCASE12-postediting/response.md) |
| KPCASE13 | pass | 재시도를 늘리지 않고 최초 원문 유지와 문제 반환을 제안했다. [기존](results/KPCASE13-baseline/response.md) · [후편집](results/KPCASE13-postediting/response.md) |

### 우선 보완점

1. **진단 ID 정확성:** KPCASE10이 ‘~에 있어서’를 KP02로 붙였다. 로컬 패턴의 직접 대응은 KP01/A-3이다. 문제 위치/이유는 맞아도 분류를 임의 생성하면 안 된다.
2. **실제 표현 개선:** KPCASE01은 일부 번역투를 줄였지만 ‘중요한 것은 … 점입니다’가 남았다. 안전하게 덜 고치는 것만으로 자연스러운 결과를 얻었다고 할 수 없다.
3. **보고문 과다:** 좋은 원고도 원문 뒤에 ‘자체 대조/도구·청취 미검증’이 자주 붙는다. 내부 검사 상태와 사용자에게 필요한 보고량을 분리할 여지가 있다. 현재 요청에서 보고를 금지한 것은 아니므로 사실 위반으로 채점하지 않는다.

## 실제 CLI 사용량

| 조건 | turn | input tokens | cached input (input에 포함) | output tokens | reasoning output (output에 포함) |
|---|---:|---:|---:|---:|---:|
| baseline | 13 | 100260 | 63232 | 830 | 230 |
| postediting | 13 | 154691 | 63232 | 1257 | 216 |

postediting 입력은 이 표본에서 **54.3% 증가**했다. 단일 콜에 지침 전체를 전달한 실험이며 비용 절감·호출 수 절감·최적화 검증이 아니다. 금액 환산이나 무료 여부는 추정하지 않는다.

## 후속 상태

이 시험만으로 공용 스킬 규칙이나 전역 설치본을 자동 수정하지 않았다. 위 보완점은 별도 수정/재시험 대상으로 남기며, 자동 기본 적용·전역 설치·게시·추가 모델 호출은 하지 않는다.

시험 후 `python3 -m pytest -q -rs`: **535 passed / 518 subtests passed** (58.35s), 버전 package 2.33/22 skills consistent, `git diff --check` 통과. 이는 소프트웨어 회귀이며 위 모델 출력의 품질 통과 점수가 아니다.
