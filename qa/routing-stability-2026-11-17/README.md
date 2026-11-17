# Routing stability — 3회 반복 측정 (유효 측정)

측정 대상: 3계층 라우터(`creative-production/SKILL.md` + `routing.csv`)
도구: `scripts/routing_eval.py --repeat 3`
모델: `gpt-6.1-sol` (Codex CLI 0.167.1)
케이스: 53개 (route-coverage 27 + adversarial boundary 26), 각 3회 = 159 시도

## 결과

| 항목 | 값 |
|---|---|
| 시도 정확도 | **159/159 = 100.0%** |
| 안정 정확도 (모든 시도가 정답인 케이스) | **53/53 = 100.0%** |
| `flaky` (시도 간 route가 바뀐 케이스) | **0** |
| `stable_wrong` (일관되게 틀린 케이스) | **0** |
| `dangerous` (media/authority 축 교차) | **0** |
| `isolation_leak` (샌드박스 밖 읽기) | **0 / 159** |

즉 53개 경계 케이스 전부에서 같은 질문에 3번 모두 같은 route를 골랐다.
"한 번 맞고 한 번 틀리는" 불안정 라우팅은 관측되지 않았다.

## 안정성을 어떻게 판정하는가

`--repeat N`은 케이스 순서를 **라운드로빈**으로 돌린다(모든 케이스 1회차 → 모든
케이스 2회차 …). 한 회차 안에서 뒤쪽 케이스에만 시간 경과 편향이 몰리지 않게
하기 위해서다. 케이스별 판정:

- `stable_correct` — 모든 시도가 같은 route이고 전부 정답
- `stable_wrong` — 모든 시도가 같은 route이고 전부 오답 (발견 사항이지 0% flake가 아니다)
- `flaky` — 시도 간 route가 다름. **정답이 섞여 있어도 성공으로 세지 않는다.**

이 판정 로직은 `scripts/test_routing_eval_harness.py`에 모델 호출 없이 고정돼
있다(`test_stability_judgement_distinguishes_flaky_from_wrong`,
`test_stable_wrong_is_not_hidden_by_majority`).

## 이 회차에서 실제로 고친 샌드박스 누수

첫 안정성 스윕(중단됨, `qa/routing-stability-2026-11-17-leaky-partial/`)에서
**159건 중 1건**이 `isolation_leak`으로 잡혔다. 원인은 `CODEX_HOME`이 실제
설치본을 가리켜, 에이전트가 `~/.codex/skills/superpowers/using-superpowers/SKILL.md`
를 읽을 수 있었던 것이다. `skills.search_dirs` 설정만으로는 부족했다.

수정: 픽스처 안에 **봉인된 `CODEX_HOME`**을 만들고 `auth.json`(mode 0600)만
복사한다. 그러면 설치된 스킬 트리가 아예 탐색되지 않는다. 같은 케이스(C09)를
재실행해 픽스처 파일만 읽는 것을 확인한 뒤 전체를 다시 돌렸다.

중단된 부분 스윕은 누수 증거로만 남긴다. 그 숫자를 인용하지 마십시오.

## 이 결과가 주장하지 않는 것

- 53개 케이스는 **내가 작성한** 프롬프트다. 경계마다 route를 하나씩 덮도록
  설계했지만 실제 사용자 발화 분포가 아니다.
- 케이스당 3회는 **샘플링 분산을 측정할 만큼 충분하지 않다.** 3회 모두 같았다는
  것은 "이 3회에서 흔들리지 않았다"는 뜻이며, 낮은 확률의 불안정을 배제하지
  않는다. flake rate의 신뢰구간을 얻으려면 케이스당 수십 회가 필요하다.
- 모델 `gpt-6.1-sol` 1개만 측정했다. 다른 모델·모델 버전·reasoning 설정에서는
  재측정해야 한다.
- 100%는 "이 지시문이 이 모델에게 이 케이스들에 대해 어떻게 읽혔는가"의 측정값이며
  라우팅 정확도의 보편 지표가 아니다.
- LLM 출력은 측정값이며 패키지 사실이 아니다. 어떤 SKILL.md도 이 결과를 근거로
  자동 수정되지 않는다.

## 재현

```bash
# 구조·문법·채점기 회귀 (모델 호출 없음)
python3 scripts/routing_regression.py
python3 -m pytest scripts/test_routing_regression.py \
                  scripts/test_routing_table_lint.py \
                  scripts/test_routing_eval_harness.py \
                  scripts/test_repo_integrity.py

# 반복 안정성 측정 (인증된 Codex CLI, 디스크가 있는 경로 지정)
ROUTING_EVAL_TMP=/path/with/disk \
  python3 scripts/routing_eval.py --repeat 3 --out qa/routing-stability-<date>
```

`dangerous`가 1건이라도 있으면 종료 코드가 1이다. `flaky`는 종료 코드에 영향을
주지 않지만 표준출력에 목록과 각 케이스의 관측 route 집합을 출력한다.
