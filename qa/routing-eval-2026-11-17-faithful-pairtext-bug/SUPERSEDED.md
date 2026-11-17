# 폐기 (SUPERSEDED) — 판별 문구가 만든 회귀

63/65. 남은 실패 2건은 **제가 쓴 판별 문구 때문에 생긴 것**이었다.

`routing-disambiguation.csv`의 R17/R18 행은 이렇게 적혀 있었다:

> R17 plans camera **inside** a narrative storyboard; ...

에이전트의 답변 이유가 정확히 그 문구를 인용했다:
"서사 스토리보드 **내부** 설계인 R17은 제외" → R18 선택.

즉 판별 표를 추가하면서 **새로운 오답을 만들었다.** 스토리보드 없이 장면의
구도·POV를 정하는 요청은 R17이 맞다. 문구를 실제 차이로 고쳤다:

> R17 decides framing, POV and blocking from the scene's narrative intent;
> R18 turns camera and space into numeric design with lens, timing and motion

수정 후 C17/B14 포함 6케이스 6/6.

유효한 측정은 `qa/routing-eval-2026-11-17-final/`이다.
