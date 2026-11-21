# 작업지시서 · Prompt Motion 큐

- [x] Q1 출처/비목표/오너: 인벤토리 5+2와 추천 24개, sibling spec 범위를 확정.
- [x] Q2 모션 참조: `video-production-assets/references/08b-code-motion-production.md`에 쇼릴, 제품/UI, 세션 스토리와 단계 QA를 작성. 08-animation에서 조건부 연결.
- [x] Q3 실시간 참조: `open-3d-production/references/realtime-motion-direction.md`에 대표 샷/스크롤/대체 상태/검증 경계를 작성. 기존 오너 entry에서 조건부 연결.
- [x] Q4 회귀: `scripts/test_prompt_motion_integration.py`로 링크 및 경계 시나리오 텍스트 계약을 검사하고 전체 `scripts` 테스트를 실행. 실행기 설치·미디어 렌더·게시 없음.

## 실행 증거
신규 연결 테스트 2개는 구현 전 실패. 통합 회귀에서 격리 설치본의 저장소 전용 상대 링크가 끊기는 문제를 발견해 공개 원본 링크로 정정. 최종 `PYTHONPATH=.:scripts python3 -m pytest -q scripts`: 629 passed, 1 skipped, 245 subtests passed. `git diff --check` 통과. 텍스트 계약 및 격리 설치 검사이며 실제 에이전트 행동, 브라우저/Blender/영상 렌더는 검증하지 않았다.
