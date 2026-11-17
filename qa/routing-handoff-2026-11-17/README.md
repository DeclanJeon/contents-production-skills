# 핸드오프 측정 (65케이스) — 요구사항 분석과 스킬 실제 사용

## 결과

| 항목 | 값 |
|---|---|
| route 정답 | **65/65** |
| owner SKILL.md 실제 열람 | **65/65** |
| 세 슬롯(요구사항 분석) 일치 | **65/65** |
| `required_read` 참조 파일 열람 | **전부** |
| 인프라 실패 | 0 |

## 왜 이 측정이 필요한가

기존 측정은 **route_id 선택**만 봤습니다. 그 숫자로는 알 수 없는 것이 있습니다:

> 라우터가 `R18`을 고르고도 `camera-spatial-design/SKILL.md`를 **한 번도 열지 않은 채**
> 기억으로 카메라 설계를 낼 수 있다. 라벨은 맞고 산출물은 스킬이 승인한 적 없다.

첫 확인에서 실제로 그랬습니다 — route 정답 65건 전부, 열람한 파일은 3개뿐이었습니다
(`SKILL.md`, `routing.csv`, `routing-disambiguation.csv`). 다만 그것은 eval이
"ROUTE/WHY 한 줄만 답하라"고 멈추게 설계했기 때문이므로, 결론이 아니라 **측정 공백**으로
다뤘습니다. `--stage handoff`를 추가해 계속 진행하게 했습니다.

## 진짜 원인은 `required_read`가 산문이었다는 것

라우터 Step 1은 "선택한 owner SKILL.md와 그 `required_read`를 읽으라"고 지시합니다.
그런데 그 컬럼에는 경로가 아니라 **문장**이 들어 있었습니다:

```
R02  developing-video-synopses stage guide
R15  relevant text owner and only applicable evidence module
R24  video-production-assets preproduction-review + storyboard-contract + contract full-package
```

27행 중 **18행이 실행 불가능**했습니다(빈칸 9, 산문 9). 모델은 어느 파일인지 추측해야
했습니다. `required_read`를 `;` 구분 패키지 상대 경로로 바꿨고(16행 명시, 11행은
owner SKILL.md만), 린트가 다음을 거부합니다: 경로 아닌 항목, 존재하지 않는 파일,
패키지 밖 경로. 조건부 의존(페르소나 설계, Blender)은 이미 각 owner SKILL.md 안에
있어서 잃은 정보는 없습니다.

### A/B — 이 수정이 실제로 작동하는가

산문을 되돌려 같은 조건으로 재측정:

| `required_read` 형태 | 참조 파일 열람 |
|---|---|
| 산문 (수정 전) | **1/4** (C02, C03, C24 실패) |
| 경로 (수정 후) | **10/10** |

## 슬롯 65/65가 되기까지 — 8건이 어긋났다

첫 전체 실행에서 슬롯은 57/65였습니다. **원인 세 가지가 섞여 있었습니다:**

1. **검사기 버그 4건** — 모델의 `none`을 `bool("none") == True`로 읽어 "승인 있음"으로
   오판했습니다. 실제로는 "승인 없음"의 올바른 표현입니다.
2. **검사기 버그 3건** — R14의 `media_axis`가 `varies`인데 구체 축 선언을 불일치로 셌습니다.
   `varies` 행에 축을 확정하는 것은 행을 읽은 결과입니다.
3. **실제 결함 1건** — C08에서 모델이 R08에 `approved_storyboard`를 적었습니다.
   승인된 보드는 *입력*이지 지출 승인이 아닙니다. 컬럼 정의가 모호했던 것이므로
   `authority_axis`를 "**지출·실행** 승인만"으로 명시했습니다.
   수정 후 C08은 승인 축을 비워서 답했습니다 — 검사기를 느슨하게 해서 통과시킨 것이
   아니라 **답이 바뀐 것**입니다.

## 무엇을 증명하고 무엇을 증명하지 않는가

증명: 65개 요청에 대해 코디네이터가 (a) 같은 route를 고르고, (b) 그 route의 owner
SKILL.md와 명시된 참조를 **실제로 열고**, (c) 산출물 종류·미디어 축·승인 축을 표와
같게 선언한다.

증명하지 않음:
- 산출물의 **품질**. 파일을 열었다는 것은 내용을 따랐다는 뜻이 아니다.
- 요구사항 분석의 **타당성**. 슬롯이 표와 일치한다는 것은 표를 읽었다는 뜻이며,
  표와 실제 업무가 맞는지는 별개다.
- `--repeat 1`이므로 flakiness는 이 실행에서 측정되지 않았다.
- 단일 모델(`gpt-6.1-sol`), 같은 날, 저자가 쓴 프롬프트.

## 재현

```bash
ROUTING_EVAL_TMP=/path/with/disk \
  python3 scripts/routing_eval.py --stage handoff --repeat 1 --retries 5 \
    --out qa/routing-handoff-<date>
```

`--stage route`(기본)는 route만 봅니다. 핸드오프 항목은 `--stage handoff`에서만
보고됩니다 — 라벨 정확도가 스킬 사용을 대신하지 않기 때문입니다.
