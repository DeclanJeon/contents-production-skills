# 전체 케이스 측정 (65케이스, 최종)

`none_or_stills` 축이 3%뿐이던 문제를 채운 뒤의 전체 측정.

## 결과

| 항목 | 값 |
|---|---|
| 채점 시도 | **65** |
| 정답 | **65/65 = 100.0%** |
| 인프라 실패 | **0** |
| 기존 59케이스와 일치 | **59/59 (100%)**, 독립 프로세스 |

## 추가한 6케이스 (E01–E06)

가장 어려운 삼분법을 겨냥했다: **종이 위의 콘티 / 이미 있는 스틸 / 새로 만드는 스틸**.

| 쌍 | 차이 | route |
|---|---|---|
| E01 vs E02 | 기존 스틸 vs 새로 뽑는 스틸 | **둘 다 R12** |
| E03 vs E04 | 내가 그릴 콘티 vs 내가 그린 그림으로 편집 | R10 vs R12 |
| E05 vs E06 | 45초 편집만 vs 단편 전체 수명주기 | R12 vs R14 |

## 이 회차가 잡은 것: 제 정답이 틀렸습니다

E02를 처음에 **R24**(새 이미지 생성 포함 패키지)로 기대했습니다. 모델은 **2회 모두 R12**를
답했습니다. 그래서 스킬 문서를 확인했더니:

> `storytelling-with-still-images/SKILL.md:15`
> "Use for new or existing still-image cuts... **If new stills are requested,
> use `codex-imagen`, not a video model.**"

**새 스틸 생성도 R12의 범위 안**이었습니다. 즉 **모델이 맞고 제 기대가 틀렸습니다.**
E02의 정답을 R12로 고쳤습니다.

이건 감사의 자동 검사로는 잡히지 않는 종류의 오류(의미 판단)였고, **실측이 잡았습니다.**
하네스를 만든 이유가 이것입니다.

### 그래서 검사 하나를 새로 만들었습니다

E01/E02는 이제 **route가 같아야 하는 쌍**입니다. "기존 스틸이냐 새 스틸이냐"는 표가
의도적으로 구분하지 않는 차이입니다. 이걸 `SAME_ROUTE_PAIRS`로 선언해 두면,
나중에 누군가 "E02는 R24가 맞다"며 되돌릴 때 감사가 즉시 실패합니다.

대조 쌍(갈려야 하는 쌍)과 비-구분 쌍(갈리면 안 되는 쌍)을 둘 다 선언하는 구조입니다.

## 축 분포 변화

| media_axis | 53케이스 | 59케이스 | 65케이스 |
|---|---|---|---|
| text_only | 75% | 71% | 66% |
| varies | 11% | 14% | 14% |
| executed_media | 9% | 12% | 12% |
| none_or_stills | 4% | 3% | 8% |

**여전히 text_only가 66%입니다.** 이 집합의 정확도는 여전히 텍스트 라우팅이
지배하며, 감사 도구가 그 문장을 매번 출력합니다. 실제 업무 분포를 모르는 상태에서
억지로 균형을 맞추는 것은 오히려 왜곡이므로, 각 축이 **고장을 감지할 수 있는
최소 케이스 수**를 갖추는 것을 목표로 했습니다(`none_or_stills` 5건).

## 재현

```bash
python3 scripts/routing_truth_audit.py    # 정답 감사 (대조 쌍 + 비-구분 쌍 + 편중)
python3 scripts/routing_regression.py     # 65케이스 vs routing.csv
ROUTING_EVAL_TMP=/path/with/disk \
  python3 scripts/routing_eval.py --repeat 1 --retries 5 --out qa/routing-eval-<date>
```
