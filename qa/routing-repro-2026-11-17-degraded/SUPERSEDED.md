# 이 회차는 사용 불가입니다 (SUPERSEDED)

53케이스 중 **14케이스가 `codex exit 101`(MCP transport 오류)** 로 실패했고,
재시도 3회로도 회복되지 않았다. 백엔드가 열화된 시간대였다.

이 회차는 재현성 판정에 쓰지 않는다. 대신 백엔드 회복을 확인한 뒤
`qa/routing-repro-2026-11-17/`에서 재실행했고, 그쪽은 53/53 깨끗하다.

## 이 회차가 드러낸 하네스 결함 (수정됨)

크래시 14건이 `stably WRONG` 목록에 **"일관되게 틀린 케이스"로 표기**됐다.
아무것도 답하지 않은 케이스인데 라우팅이 틀린 것처럼 읽히는, 정반대의 보고였다.

수정: 판정을 유효 시도로만 계산하고, 유효 시도가 없으면 `no_data`,
route를 하나도 고르지 않았으면 `unanswered`로 분리했다. `stable_accuracy`의
분모도 크래시가 아니라 **결정된 케이스**로 바꿨다.
회귀 테스트: `test_crashes_are_not_reported_as_stably_wrong`,
`test_unanswered_is_not_stably_wrong`.
