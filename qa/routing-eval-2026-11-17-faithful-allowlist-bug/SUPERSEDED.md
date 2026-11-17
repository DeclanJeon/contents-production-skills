# 폐기 (SUPERSEDED) — 하네스 허용 목록 결함

62/65. 그러나 이 숫자는 **라우팅 성능이 아니다.**

원인: 픽스처 `AGENTS.md`에 읽기 허용 목록이 **손으로 적혀** 있었고
`routing-disambiguation.csv`가 빠져 있었다. 그래서 에이전트가
"required ... is outside the permitted reading list"라며 라우팅을
거부한 경우가 있었다 — 반면 같은 제약을 무시하고 정상 답한 경우도 있었다.
즉 **동일 결함이 `unanswered`와 `correct`로 번갈아 나타났고**, 점수는 의미가 없다.

수정: 허용 목록을 `FRONTIER_FILES`에서 **파생**하도록 바꿨다. 손으로 적는 목록은
반드시 낡는다. 회귀 테스트 2개 추가
(`test_fixture_allowlist_covers_every_frontier_file`,
`test_every_frontier_file_is_present_in_the_fixture`).

유효한 측정은 `qa/routing-eval-2026-11-17-final/`이다.
