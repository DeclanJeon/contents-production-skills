# 카메라 무빙 타이밍과 렌즈 디렉팅

## 동기에서 시간 곡선으로
샷마다 관객이 알아야 할 정보와 reveal/contact/emotion_peak를 먼저 정한다. 카메라 움직임을 인물의 action/reaction/hold와 함께 배치한다. 고정 샷 대안과 비교하고 잠긴 샷에는 불필요한 새 후보를 만들지 않는다.
타이밍 테이블에 local seconds/frame basis, camera position/target, subject position/action, motion phase, information visibility, focus target을 기록한다. move_start → acceleration → cruise/track → deceleration → settle/hold가 모두 필요한 것은 아니다. 연속 추적에서 각 키프레임마다 멈추도록 easing을 넣지 않는다. 시작/끝 스틸뿐 아니라 가속 전환·공개/접촉 정점·컷 직전도 검사한다.

## 좌표와 운동
화면 좌우와 world X/Y/Z를 구분한다. 병진/회전/줌/초점을 별도 채널로 쓴다. 카메라 경로와 피사체 동선을 같은 시간 기준으로 맞춘다. 주목 대상의 급변이 카메라 회전 스냅을 만들면 target 전환 또는 컷으로 해결한다. 추적 시 카메라와 피사체 속도를 같은 값으로 강제하지 않고 원하는 상대 프레이밍을 기준으로 설계한다.
거리와 dt가 주어지면 displacement/dt는 구간 평균 속도다. 순간 속도·가속도·jerk를 주장할 때는 사용한 보간과 샘플 간격을 명시한다. 샷 경계를 가로지르는 차분은 계산하지 않는다. 리그 상한은 입력된 운영 제약으로만 검사하고 임의 속도 임계값을 영화 품질의 정답으로 쓰지 않는다. 원본 카메라 속도가 미측정이면 새 수치는 DESIGN_PROPOSAL이다.
camera-spatial-1.0 경로 스키마는 유지한다. 지원되는 interpolation만 사용한다. 복잡한 커브가 스키마에 없으면 companion timing/lens artifact로 설명하고 확인된 실행 어댑터가 지원하지 않는 속성을 실제 실행됐다고 보고하지 않는다.

## 렌즈·초점
프레이밍, 센서/유효 게이트, 초점거리, 피사체 거리, 초점 대상/거리, f-number, 렌즈 왜곡/호흡·모션블러 조건을 알려진 값 또는 제안/미정으로 기록한다. 원근은 시점·거리로 결정된다. 렌즈를 길게 바꾸면서 카메라를 뒤로 이동해야 동일 프레이밍을 유지하는 비교를 제대로 설명할 수 있다. optical/digital zoom·dolly·dolly zoom을 분리한다.
랙 포커스는 카메라 병진이 아니라 선명도 전환이다. 누가 언제 선명해져야 하는지, 공개 전에 흐린 대상이 너무 잘 읽히지 않는지, focus pull의 시작·완료를 설계한다. 초점거리(mm), 초점 맞춘 거리(m), 피사체 거리(m)를 혼용하지 않는다. 얕은 심도로 필수 행동/제품 메시지가 가려지면 초점·조리개·거리·컷을 조정한다.
광학 계산과 미학은 구분한다. 왜곡·호흡·실제 심도/모션블러는 카메라·렌즈 캘리브레이션 또는 해당 렌더 설정에 달려 있다. 현재 Blender BBox 프리비즈는 완전한 렌즈·포커스·물리 리그 검증기가 아니다. 지원 여부를 확인한 설정과 실제 렌더 검사만 검증으로 보고한다.

## 인계
카메라 원본 artifact_id/version, 타이밍·렌즈 companion 버전, 샷/씬/패널 ID와 의도·실제 검사·미확인을 함께 전달한다. 생성 프롬프트 변환은 ai-camera-control, 레퍼런스 역분석은 camera-motion-reference-analysis에 연결한다. 프리비즈·실행·실제 QA를 수치 설계와 분리한다.
