# 카메라 무빙·렌즈·시간 검수

## 대상과 근거
camera_spec와 companion timing/lens 계획의 현재 버전, 원본/생성 클립, 샷·패널·비트, 목표 공개/접촉 시각과 승인된 허용 오차를 받는다. 실제 재생·프레임/타임코드·도구 측정·사용자 기록·추론을 구분한다. 미디어 없이 텍스트 계획만 검사하면 실제 motion 품질은 unverified다. 샘플 스틸로 동적 흔들림이나 속도를 통과 판정하지 않는다.

## 검사
1. 전체 샷 재생, 가속/감속 전환, 공개/접촉 정점, 필수 프레이밍과 앞뒤 컷을 본다. 빠르거나 문제 있는 구간은 더 촘촘히 검사하고 실제 검사 범위를 적는다.
2. 이동 방향·대상 유지·start/end/hold, pan/tilt/translation/zoom/focus의 분리, 피사체와 카메라의 상대 움직임을 계획과 대조한다.
3. 공간 앵커·시차·가림 순서·제품 비례·배경 직선이 안정적인지 본다. 비강체 배경 변형, 인물 foot sliding, floating, 생성된 wobble을 자연스러운 카메라 움직임과 구분한다. 원인 미확인은 가설로 기록한다.
4. 급가속·회전 스냅·불필요한 키프레임 정지·원치 않은 horizon roll·클리핑·미끄러운 안정화 크롭을 검사한다. 의도된 핸드헬드/롤/스냅은 잠긴 연출과 대조하고 자동 결함 처리하지 않는다.
5. focus 대상과 전환 시점, 필수 행동·제품·표정의 가독성, 렌즈 호흡·블러·노출 변화가 의도에 맞는지 본다. 랙 포커스를 카메라 이동 성공으로 기록하지 않는다.
6. 180도 축/시선·피사체 순서·이동 방향·매치 액션·샷 간 상대 속도가 이어지는지 본다. 의도된 축 변경은 관객 재정위 단서를 검사한다.
7. 승인된 공개/접촉 목표와 실제 timecode/PTS를 비교한다. 오차 허용이 없으면 measured difference로 보고하고 임의 pass 임계값을 만들지 않는다. source reference timing은 새 제작의 승인 목표와 구분한다. 숫자 유사도/flow 점수만으로 미학 통과나 자동 재생성을 하지 않는다.

## 결과와 수정 담당
issue_id / severity / shot·panel ID / actual clip version / source evidence time / OBSERVED 또는 USER_REPORTED / expected vs actual / impact(interpretation) / cause hypothesis / minimum fix / owner / affected dependents / reinspection range를 적는다.
경로·렌즈·타이밍 설계 문제는 camera-spatial-design, 관찰 근거 부족은 camera-motion-reference-analysis, 상충/미지원 생성 입력은 ai-camera-control, actual render 구현은 blender-previsualization, 컷/안정화/속도 조절은 해당 편집 모듈로 보낸다. 편집으로 공간 오류가 실제 해결되는지도 확인한다. 설정·입력·샷 수·모델·비용의 변경은 기존 승인 범위에 대조한다.

판정은 pass / pass_with_notes / needs_revision과 검사 범위를 함께 기록한다. 핵심 움직임/공개가 미검증이면 실제 영상 카메라 통과를 선언하지 않는다. 구조·기술 검사, 작품 판단, 사용자 수락은 별개다. 수정 뒤 해당 샷과 앞뒤 컷을 재검사하고 정본 버전 및 영향을 받는 종속 에셋만 갱신한다.
