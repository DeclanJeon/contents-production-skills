# 경계 케이스 flake 측정 (26개 × 8회 = 208 시도)

도구: `scripts/routing_eval.py --repeat 8 --retries 3`
모델: `gpt-6.1-sol` (Codex CLI 0.167.1)
대상: 사전에 설계한 경계 케이스 **26개 전수**(B01–B25, B01b). 임의 선별 없음.

## 결과

| 항목 | 값 |
|---|---|
| 채점 시도 (인프라 실패 제외) | **208** |
| 라우팅 오류 | **0** |
| `flaky` (시도 간 route가 바뀐 케이스) | **0 / 26** |
| 인프라 실패 | **0** |
| 시도별 오류율 | 0.00% (95% Wilson **0.00–1.81%**) |

## 이 숫자가 실제로 말하는 것

**"절대 흔들리지 않는다"가 아닙니다.** 케이스당 8회로는 부족합니다:

```
케이스당 8회, 0 오류 → 31.2% 이하의 오류율은 여전히 숨을 수 있음
전체 208회, 0 오류 → 1.43% 초과만 배제 가능
1% 오류율을 배제하려면 케이스당 약 298회 필요
```

그래서 인용할 수 있는 것은 **집계 한계 "시도별 라우팅 오류율 < 1.5%"** 하나입니다.
케이스별 "0 flake"는 근거가 약하므로 케이스 단위 주장으로 쓰지 마십시오.
이 계산은 `scripts/routing_flake_report.py`가 출력하며 테스트로 고정돼 있습니다
(`scripts/test_routing_flake_report.py`).

## 측정 도중 발견해 고친 결함 3건

### 1. 장시간 스윕이 영구 정지할 수 있었음

`--timeout 420`을 줬는데도 케이스 B06에서 9분 넘게 멈췄습니다. 출력을 파이프로
읽고 있었기 때문에, 자식이 상속한 descriptor를 붙잡고 있으면 EOF를 영원히
기다립니다. `subprocess.run(timeout=)`은 자식을 kill한 뒤 `communicate()`를 다시
호출하므로 타임아웃이 대기를 제한하지 못합니다.

수정: 출력을 **임시 파일**로 받아 EOF 대기 자체를 없애고, 초과 시
**프로세스 그룹 전체**를 kill(`start_new_session` + `killpg`). 초과는
`dispatch_error`와 구분되는 verdict `timeout`으로 기록합니다.

### 2. 인프라 실패를 라우팅 오류로 세고 있었음

중간 회차에서 `codex exit 101`(MCP transport 오류)이 18건 연속 발생했습니다.
리포터가 이를 "틀린 route"로 집계해 표를 오염시켰습니다. 라우팅 판단과
백엔드 장애는 다른 사건입니다.

수정: `INFRA = {dispatch_error, timeout}`을 채점에서 제외하고 별도로 보고합니다.
크래시 2건 + 동일 응답 1건은 `flaky`가 아닙니다.

### 3. 재시도 부재

`--retries N`을 추가했습니다. **인프라 실패만** 재시도하며, **틀린 route는 절대
재시도하지 않습니다** — 표가 좋아 보일 때까지 주사위를 다시 굴리는 것과 같기
때문입니다. 이 구분은 테스트로 고정돼 있습니다.

## 선별 편향을 피한 방법

당초 "가장 좁은 경계 10개를 골라 20회"를 계획했으나, 표에서 위험도를 계산하려
해보니 **`media_axis`/`authority_axis` 조합은 의미적 이웃을 분리하지 못합니다**
(`text_only` 라우트는 authority가 모두 비어 있어 서로 전부 twin으로 나옴).
즉 데이터로 "좁은 경계"를 고를 수 없습니다. 그래서 손으로 고르는 대신
경계 케이스 26개 전수를 동일 횟수로 측정했습니다.

## 이 결과가 주장하지 않는 것

- 26개 케이스는 **내가 작성한** 프롬프트입니다. 실제 사용자 발화 분포가 아닙니다.
- 모델 1종(`gpt-6.1-sol`)만 측정했습니다.
- 한 세션 안에서 연속 실행했습니다. 세션 간·일자 간 드리프트는 측정하지 않았습니다.
- 정답 route는 `routing.csv`를 정본으로 삼은 제 판단입니다. 표가 틀렸다면 측정은
  "표에 일관되게 답했다"만 보여줍니다.
- LLM 출력은 측정값이며 패키지 사실이 아닙니다.

## 재현

```bash
ROUTING_EVAL_TMP=/path/with/disk \
  python3 scripts/routing_eval.py \
    $(python3 -c "import json;d=json.load(open('creative-production/evals/routing-cases.json'));print(' '.join('--case '+c['case_id'] for c in (d['cases'] if isinstance(d,dict) else d) if c['case_id'].startswith('B')))") \
    --repeat 8 --retries 3 --out qa/routing-flake-<date>
python3 scripts/routing_flake_report.py qa/routing-flake-<date>
```
