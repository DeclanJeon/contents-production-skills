# DELIVERY01 v1.2 — 실제 파일과 미완성 범위

**최종 25초 MP4는 없다.** `delivery/132-autumn-25s.mp4`를 생성·납품했다고 주장하지 않는다.

## 실제 산출물
- [실제 제작 QA](qa/report.md), [정지 패널 검수](review.md), [중단된 실행 계획](execution-plan.md)
- [시놉시스](synopsis.md), [비주얼 바이블](visual-bible.md), [상세 콘티](storyboard.md), [카메라 설계](camera_spec.json)
- `images/`: 선택 clean 패널 10개. P02는 `P02_SH02_start_v2.png`. 초기/미선택 생성 출력은 보존했다.
- [정지 엔드카드 레이아웃](delivery/endcard-layout.png): 제공 원본 제품 합성과 결정론적 3줄 타이포그래피. 완성 영상이 아니다.
- [실제 6초 Flow 원본](videos/SH01_actual_partial_prompt.mp4): 720×1280, H.264, 24fps, 비디오 144프레임, AAC. 첫 설명 문단만 제출된 부분 프롬프트 결과이며 카메라 이동 때문에 선택 SH01로 채택하지 않았다.
- [입력 사고·잔액 기록](qa/flow-execution-incident.json), [Flow 실패 화면](qa/flow-blocked.webp), [단일행 무제출 smoke](qa/safe-input-smoke.json)
- [실제 편집기](scripts/render_ad.py), [편집 계획](edit-plan.md): 5개 실제 선택 영상이 있을 때만 4/5/6/6/4초, 1080×1920/30fps로 합성·인코딩한다. 없는 파일은 실패시키며 반복 정지로 대신하지 않는다.

## 현재 한계
실패 카드 11개는 UI에서 미청구를 표시했다. 완료 요청 1개를 확보한 뒤 잔액 893→883을 확인했다. 실제 사용량 관측은 10크레딧 차이이며 결제 거래 장부/환불 완료를 별도 확인하지 않았다. 입력 도구의 다중행 Enter 제출 문제와 Flow unusual-activity 응답으로 추가 자동 제출을 중단했다. 도구 문제는 신고했고 단일행 텍스트 입력의 무제출 동작은 검사했다. Flow 서비스 상태 해소는 미검증이다.

방울 낙하와 도포/분리, 25초 컷 연결, 최종 750프레임·오디오·자막 검수는 미실시다. 정지 패널이나 한 개의 배경 원본을 최종 광고로 포장하지 않는다. 모델 대체·신규 결제·게시·인증/봇 보호 우회는 하지 않았다.

## 스킬 업데이트
설계 커밋 `a3cb49e`, 스킬 보강 커밋 `35ea1a6`은 기존 작업에서 실제 생성한 기록이다. 저장소 QA는 `docs/STATE_CAUSALITY_QA.md`와 `qa/state-causality-*.json`에 있다. 이번 마지막 재실행은 118 tests/156 subtests passed, 기존 Windows subprocess 디코딩 경고 2개. 문서 인계 보강을 실제 영상 생성 품질 개선으로 주장하지 않는다.

Ultragoal의 G001–G005/ledger는 보존한다. 현재 mounted tools에 Codex get_goal/create_goal/update_goal이 없어 서버 목표 완료를 주장하지 않는다. CLI annotate로 실제 산출물과 G005 제작 차단을 기록한다.
