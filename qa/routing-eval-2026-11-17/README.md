# Routing accuracy measurement — 2026-11-17

측정 대상: 이 패키지의 3계층 라우터(`creative-production/SKILL.md` + `routing.csv`)
측정 도구: `scripts/routing_eval.py`
모델: `gpt-6.1-sol` (Codex CLI 0.167.1)

## 방법

각 케이스 프롬프트를 **격리된 read-only 샌드박스**에 디스패치했다. 샌드박스에는
라우터 frontier(라우터 SKILL.md + routing.csv)와 owner 후보들의 SKILL.md만
복사되며, 저장소·프로젝트·자격증명은 노출되지 않는다. 에이전트는 route_id
하나만 응답한다. 원본 wire는 각 케이스별 `*.wire.jsonl`에 보존했다.

판정 등급:

- `correct` — 기대 route_id와 일치
- `near_miss` — 다른 route이지만 media_axis가 같고 권한 축이 겹침
- `dangerous` — **media/authority 축을 넘는 오답** (text-only 요청이 실행 route로
  가는 등 가장 비싼 오류)
- `unanswered` — UNASSIGNED

## 결과

| 회차 | 정확도 | dangerous | 비고 |
|---|---|---|---|
| run1 (`qa/routing-eval-2026-11-17-run1`) | 26/27 = 96.3% | **0** | C20이 UNASSIGNED |
| run2 (`qa/routing-eval-2026-11-17`) | **27/27 = 100.0%** | **0** | R20 표 수정 후 |

## run1의 유일한 miss와 그 처리

C20 프롬프트: `이 영상 실제 카메라 무빙 검수해줘`

에이전트 응답:

```
ROUTE: UNASSIGNED
WHY: Actual camera movement QA requests no generation or edit; R20 requires executed_media.
```

**라우터가 옳았고 표가 틀린 사례다.** 카메라 무빙 검수는 실제 재생 증거가
필요하지만 새로운 생성·편집을 승인하지는 않는다. R20은 `executed_media`로
분류되어 있었고 `authority_axis`가 비어 있었다. 수정:

- `media_axis`: `executed_media` → `varies`
- `authority_axis`: `` → `supplied_media_only`
- `stop_boundary`: 이미 공급/생성된 미디어만 검사하며 새 실행을 승인하지 않음을 명시

이 수정은 C20만 재실행(2회, 모두 통과)한 뒤 전체 스윕(run2)으로 확인했다.

## 이 결과가 주장하지 않는 것

- 이 숫자는 **이 패키지의 라우터 지시문이 이 모델에게 어떻게 읽히는지**의
  측정값이지, 라우팅 정확도의 보편적 성능 지표가 아니다. 모델·프롬프트·케이스
  집합이 바뀌면 다시 측정해야 한다.
- 케이스 27개는 각 route를 하나씩 덮도록 **내가 작성한** 프롬프트다. 실제
  사용자 발화 분포를 대표하지 않는다. 구어체·복합 요청·모호한 요청에서의
  성능은 이 측정 범위 밖이다.
- LLM 출력은 측정값이며 패키지 사실이 아니다. 어떤 SKILL.md도 이 결과를
  근거로 자동 수정되지 않는다.
- 각 케이스는 1회 실행이다. 샘플링 분산을 측정하지 않았다.

## 재현

```bash
# 스모크 (케이스 2개)
python3 scripts/routing_eval.py --case C01 --case C24

# 전체
ROUTING_EVAL_TMP=/path/with/disk python3 scripts/routing_eval.py --out qa/routing-eval-<date>

# 오프라인 구조 검증 (모델 호출 없음)
python3 scripts/routing_regression.py
python3 -m pytest scripts/test_routing_table_lint.py scripts/test_routing_regression.py
```

`--out`을 주지 않으면 요약만 출력하고 원본 wire를 저장하지 않는다.
