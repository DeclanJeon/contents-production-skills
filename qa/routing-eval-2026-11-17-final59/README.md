# 전체 케이스 측정 (59케이스, 확장 후 단일 측정)

기존 측정은 53케이스 기준이었다. 실행 축(돈이 걸린 경계)이 9%뿐이라는 감사
지적을 받아 6케이스를 추가하고, 확장된 집합 전체를 한 번에 다시 쟀다.

## 결과

| 항목 | 값 |
|---|---|
| 채점 시도 | **59** |
| 정답 | **59/59 = 100.0%** |
| 안정 정확도 | **59/59** |
| 인프라 실패 | **0** |

기존 53케이스 측정과의 일치: **53/53 동일 route (100%)**
(`routing_repro_check.py`로 확인, 3번째 독립 프로세스)

## 추가한 6케이스 (D01–D06)

실행 축을 늘리려고 만든 **대조 쌍 3개**다. 같은 요청에서 승인 조항만 다르다:

| 쌍 | 승인/보류 조항 | route | media / authority |
|---|---|---|---|
| D01 | "이미지는 다음 회차에" | R10 | text_only / – |
| D02 | "이미지도 이번에 바로 뽑아서" | R24 | executed_media / approved_execution |
| D03 | "블렌더 검증은 다음 단계에서" | R21 | text_only / – |
| D04 | "블렌더로 돌려서 확인" | R22 | executed_media / requested_spatial_verification |
| D05 | "기획부터 배급까지 단계별로" | R14 | varies / – |
| D06 | "촬영 끝난 A롤 영상…검수" | R20 | varies / supplied_media_only |

보류형(D01, D03)은 **실행하면 안 되는 트랩**이다. 6건 모두 2회씩 실행해 12/12
정답이었고, 전체 측정에서도 정답이었다.

## 편중 변화

| media_axis | 53케이스 | 59케이스 |
|---|---|---|
| text_only | 75% | 71% |
| varies | 11% | 14% |
| executed_media | 9% | 12% |
| none_or_stills | 4% | 3% |

여전히 text_only가 71%다. **이 집합의 정확도는 여전히 텍스트 라우팅이
지배한다.** 감사 도구가 그 문장을 매번 출력한다.

## 이 과정에서 실제로 잡힌 오류

D02의 `expected_owner`를 `video-production-assets`로 적었는데, `routing.csv`의
R24 owner는 `creative-production`이었다. **회귀 테스트가 즉시 실패**해서 잡았다
(`owner drift: csv='creative-production' expected='video-production-assets'`).

그래서 감사에 `owner` 검사도 추가했다. 정답 데이터의 오류는 정답 데이터를
검사하는 곳에서 잡히는 게 맞다.

## 재현

```bash
python3 scripts/routing_truth_audit.py       # 정답 자체 감사 (모델 불필요)
python3 scripts/routing_regression.py        # 59케이스 vs routing.csv
ROUTING_EVAL_TMP=/path/with/disk \
  python3 scripts/routing_eval.py --repeat 1 --retries 5 --out qa/routing-eval-<date>
```
