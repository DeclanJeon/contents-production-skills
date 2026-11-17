# 최종 측정 (65케이스, 충실한 하네스)

## 결과

| 항목 | 값 |
|---|---|
| 채점 시도 | **65** |
| 정답 | **65/65 = 100.0%** |
| 인프라 실패 | **0** |
| `dangerous` | **0** |
| 쌍 표를 실제로 읽은 케이스 | **65/65** |
| 이전 측정(권한 지정 방식)과 동일 route | **65/65** |

## 이번 회차의 본질: 이전 100%는 하네스가 만든 것이었습니다

기존 하네스의 지시문은 이렇게 시작했다:

> Read `creative-production/references/routing.csv` and
> `creative-production/SKILL.md`.

**읽을 파일을 하네스가 직접 지정**했습니다. 그래서 라우터는 스킬의 자체 열람
목록을 따르지 않아도 100%를 받았습니다. 즉 **측정 대상은 스킬이 아니라 하네스가
적어준 목록**이었습니다.

지시문을 스킬 위임형으로 바꿨습니다:

> Read `creative-production/SKILL.md` and do exactly what its routing step says,
> including every file that step tells you to read. The instruction deliberately
> names no other file, because naming them here would let the router skip its own
> reading list and still score well.

이 변경으로 **쌍 표 열람률이 0/11 → 65/65**가 됐습니다. 이전에는 스킬이
"REQUIRED"라고 적어도 하네스가 다른 파일만 읽으라고 해서 읽히지 않았습니다.

## 이번 회차가 드러낸 결함 2건 (둘 다 제가 만든 것)

### 1. 픽스처 허용 목록이 손으로 적혀 있었음

`AGENTS.md`의 읽기 허용 목록에 `routing-disambiguation.csv`가 없었습니다.
결과적으로 같은 결함이 **`unanswered`(거부)와 `correct`(무시)로 번갈아** 나타나
점수가 무의미해졌습니다. 허용 목록을 `FRONTIER_FILES`에서 파생하도록 고쳤습니다.
손으로 적는 목록은 반드시 낡습니다.

### 2. 판별 문구가 새 오답을 만들었음

R17/R18 행을 "R17 plans camera **inside** a narrative storyboard"라고 적었더니,
에이전트가 그 문구를 인용해 **R17을 제외**하고 R18을 골랐습니다(C17, B14 →
63/65). 판별 표를 넣으면서 회귀를 만든 것입니다.

실제 차이로 다시 썼습니다:

> R17 decides framing, POV and blocking from the scene's narrative intent;
> R18 turns camera and space into numeric design with lens, timing and motion

수정 후 65/65.

## frontier 비용

| 구성 | 단어 | 비고 |
|---|---|---|
| router + routing.csv | 1,426 | 항상 읽음 |
| routing-disambiguation.csv | **+426** (23쌍) | 필수 열람 |
| 합계 | **1,852** | legacy 2,959 대비 **-37%** |

`scripts/routing_regression.py`가 이 값을 매번 출력합니다.

쌍 표를 "동점일 때만" 읽히게 했더니 **11케이스에서 0회** 열렸습니다. 한쪽이 항상
즉시 그럴듯해 보이므로 조건이 발화하지 않습니다. **아무도 안 읽는 파일은 없는
것만 못하므로** 필수로 바꾸고 비용을 정직하게 보고합니다.

## 귀속

`routing.csv` 27행 전부에 판별 정보가 없었습니다. 이번 오류(E02: 새 스틸 생성이
R12인지 R24인지)는 그 정보가 스킬 prose에만 있었기 때문입니다. 23쌍으로 그 구멍을
메웠고, 각 문구는 해당 스킬 문서를 근거로 작성했습니다.

## 재현

```bash
python3 scripts/routing_truth_audit.py
python3 scripts/routing_regression.py
ROUTING_EVAL_TMP=/path/with/disk \
  python3 scripts/routing_eval.py --repeat 1 --retries 5 --out qa/routing-eval-<date>
```
