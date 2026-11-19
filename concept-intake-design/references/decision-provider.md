# 판단 공급자 — Jev 1.14 또는 호스트 에이전트

## 무엇을 누가 판단하나

| 종류 | 예 | 공급자 |
|---|---|---|
| 판단(typed) | 9개 요소가 요청에 있나(Noul 0~1), 축별 추천(Choice), 6개 평가 기준 점수(Score) | Jev 1.14 → 호스트 에이전트 → 규칙 기반 기본값 |
| 생성(prose) | 시놉시스·기획안·대본·캐릭터 바이블 | 호스트 에이전트(또는 별도로 지정한 생성 모델) |

## Jev 1.14 (2026-11-19 확인)

- OpenRouter 모델 ID `typesafe/jev-1.14` (고정 버전 `typesafe/jev-1.14-20261014`). TypeSafe의 System One 판단 모델로, 산문 대신 타입이 정해진 답을 돌려준다.
- 질문 유형: Choice(선택지 중 하나 + 확률·신뢰도), Score(순서 있는 등급), Noul(0~1), Box(이미지 영역).
- TypeSafe 직접 API: `POST https://api.typesafe.ai/v1/systemone`, 본문 `{model: "jev-1.14.0", state, questions: {id: {type, instructions, criteria}}}` → `{answers: {id: {...}}}`.
- OpenRouter 경유 요청 형태(System One 질문 맵)는 공개 문서로 확인되지 않았다. CineForge는 이를 실험 기능으로 두고, 응답 형태가 다르면 다음 공급자로 넘어간다.
- 가격(확인 시점): 입력 100만 토큰당 $0.042, 출력 무료. 키는 환경변수(`OPENROUTER_API_KEY` 또는 `TYPESAFE_API_KEY`)로만 받고 파일·로그에 남기지 않는다. 비용이 드는 호출이므로 사용자가 키를 설정한 경우에만 쓴다.

## 호스트 에이전트 모드

키가 없거나 Jev가 실패하면 호스트 에이전트(지금 이 스킬을 실행하는 에이전트)가 같은 질문에 같은 형식으로 답한다. CineForge CLI는 `agent_io/requests/<task>.json`에 질문을 쓰고, 에이전트가 `agent_io/responses/<task>.json`에 답을 쓰면 이어서 진행한다.

```json
{"answers": {"recommend_narrative": {"choice": "ending_first", "confidence": 0.7},
             "hook": {"score": "70"}, "script": {"noul": 0.0}}}
```

## 기록

각 판단에 공급자 이름(`jev-openrouter`, `jev-typesafe`, `host-agent`, `heuristic`)을 남긴다. 폴백이 일어나면 그 이유도 남긴다. 판단 결과는 추천일 뿐, 사용자 승인이나 실행 권한이 아니다.
