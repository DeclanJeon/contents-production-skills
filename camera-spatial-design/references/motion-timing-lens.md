# 카메라 무빙 타이밍과 렌즈 디렉팅

## 동기에서 시간 곡선으로
샷마다 관객이 알아야 할 정보와 reveal/contact/emotion_peak를 먼저 정한다. 카메라 움직임을 인물의 action/reaction/hold와 함께 배치한다. 둘 다 움직이면 동일한 shot-local seconds 또는 frames basis(FPS 명시)에 카메라 phase와 subject action을 맞춰 쓴다. 적용되는 move onset/change, reveal/contact, stop/settle, hold, cut만 cue로 남긴다; 고정 샷이나 불필요한 phase는 비워 둔다. 결과·반응 hold가 필요하면 샷 시간 안에 배정한다. 고정 샷 대안과 비교하고 잠긴 샷에는 불필요한 새 후보를 만들지 않는다.
타이밍 테이블에 local seconds/frame basis, camera position/target, subject position/action, motion phase, information visibility, focus target을 기록한다. move_start → acceleration → cruise/track → deceleration → settle/hold가 모두 필요한 것은 아니다. 연속 추적에서 각 키프레임마다 멈추도록 easing을 넣지 않는다. 시작/끝 스틸뿐 아니라 가속 전환·공개/접촉 정점·컷 직전도 검사한다.

## 좌표와 운동
화면 좌우와 world X/Y/Z를 구분한다. 병진/회전/줌/초점을 별도 채널로 쓴다. 카메라 경로와 피사체 동선을 같은 시간 기준으로 맞춘다. 주목 대상의 급변이 카메라 회전 스냅을 만들면 target 전환 또는 컷으로 해결한다. 추적 시 카메라와 피사체 속도를 같은 값으로 강제하지 않고 원하는 상대 프레이밍을 기준으로 설계한다.
거리와 dt가 주어지면 displacement/dt는 구간 평균 속도다. 순간 속도·가속도·jerk를 주장할 때는 사용한 보간과 샘플 간격을 명시한다. 샷 경계를 가로지르는 차분은 계산하지 않는다. 리그 상한은 입력된 운영 제약으로만 검사하고 임의 속도 임계값을 영화 품질의 정답으로 쓰지 않는다. 원본 카메라 속도가 미측정이면 새 수치는 DESIGN_PROPOSAL이다.
camera-spatial-1.0 경로 스키마는 유지한다. 지원되는 interpolation만 사용한다. 복잡한 커브가 스키마에 없으면 companion timing/lens artifact로 설명하고 확인된 실행 어댑터가 지원하지 않는 속성을 실제 실행됐다고 보고하지 않는다.

## 렌즈·초점
프레이밍, 센서/유효 게이트, 초점거리, 피사체 거리, 초점 대상/거리, f-number, 렌즈 왜곡/호흡·모션블러 조건을 알려진 값 또는 제안/미정으로 기록한다. 원근은 시점·거리로 결정된다. 렌즈를 길게 바꾸면서 카메라를 뒤로 이동해야 동일 프레이밍을 유지하는 비교를 제대로 설명할 수 있다. optical/digital zoom·dolly·dolly zoom을 분리한다.
랙 포커스는 카메라 병진이 아니라 선명도 전환이다. 누가 언제 선명해져야 하는지, 공개 전에 흐린 대상이 너무 잘 읽히지 않는지, focus pull의 시작·완료를 설계한다. 초점거리(mm), 초점 맞춘 거리(m), 피사체 거리(m)를 혼용하지 않는다. 얕은 심도로 필수 행동/제품 메시지가 가려지면 초점·조리개·거리·컷을 조정한다.
광학 계산과 미학은 구분한다. 왜곡·호흡·실제 심도/모션블러는 카메라·렌즈 캘리브레이션 또는 해당 렌더 설정에 달려 있다. 현재 Blender BBox 프리비즈는 완전한 렌즈·포커스·물리 리그 검증기가 아니다. 지원 여부를 확인한 설정과 실제 렌더 검사만 검증으로 보고한다.

## 차량 접촉·공간 연속성의 조건부 검사

브리프가 일반적인 물리적 굴림을 명시적으로 요구할 때만 승인된 차량 형상과 바퀴/지면 접촉을 정하고, 같은 샷 로컬 시간축에서 회전을 차량의 이동과 대조한다. 카메라 경로는 따로 본다. 추적 카메라가 화면상 차체 이동을 상쇄해도 차량의 지면 기준 이동은 남을 수 있다. 휠 반경·속도·프레임레이트·노면 형상이 없으면 미설정/가정으로 두고 한 이미지에서 계산하지 않는다. 스타일화된 드리프트나 공중/portal 구간에서는 일반 지면 접촉/no-slip을 비활성화하고, 지지가 화면에 돌아올 때 다시 적용한다.

여러 샷의 동선은 승인된 공간도 또는 새로 설계한 scene/world reference에 입구·문턱·landmark·방위·복귀 경로를 선언하고 샷별 frame/POV에 연결한다. 의도된 topology/scale break는 앞뒤의 안정된 시각 anchor가 있는 디자인 전환으로 표시한다; 실제 지리 측정이나 복원된 카메라 경로로 보고하지 않는다. geometry나 정확한 카메라 배치가 필요하면 기존 camera-spatial/Blender handoff를 따르고 실제 장면 출력을 검사한다. 텍스트 anchor는 계획 의도이지 공간 검증이 아니다.

## 인계

카메라 원본 artifact_id/version, 타이밍·렌즈 companion 버전, 샷/씬/패널 ID와 의도·실제 검사·미확인을 함께 전달한다. 생성 프롬프트 변환은 ai-camera-control, 레퍼런스 역분석은 camera-motion-reference-analysis에 연결한다. 프리비즈·실행·실제 QA를 수치 설계와 분리한다.

## 주장별 근거와 검증 한계

정확한 원문 경로·rendition bytes·SHA256·읽은 위치는 설치 참조 [sources.md](sources.md)의 E2 인용에 붙어 있다. 각 항목은 `READ-PARTIAL`이며 도판은 미검사다.

- **동기에서 시간 곡선으로**: E2-WILLIAMS L95–97은 사건 시점(timing)과 연속 위치 간격(spacing)을 구별한다. E2-PEARLMAN L119–121은 강조점과 카메라/배우/대사/음향의 구절 조율을, E2-KENWORTHY1 L175는 반응에 맞춘 push-in을 지원한다. onset/contact/reveal/hold 슬롯과 공통 local-time 테이블은 이를 납품하기 위한 자체 설계다. 특정 easing이나 보편적인 hold 길이를 책에서 도출하지 않는다.
- **좌표와 운동**: E2-KENWORTHY1 L183의 배우 회전과 카메라 병진/팬은 별도 동작을 조율하는 사례다. 좌표축·차분·평균 속도·보간·샷 경계 처리와 `camera-spatial-1.0`은 자체 구현 계약이며 심미적 법칙이 아니다.
- **렌즈·초점**: 시점/거리와 줌의 구별은 sources.md의 W2-Block 범위, 반응/주의에 맞춘 초점 선택은 E2-KENWORTHY1 L301, push-in 중 초점 유지 과제는 E2-KENWORTHY2 L83에 한정한다. 반사상 사례를 모든 랙 포커스의 성공 보장으로 일반화하지 않는다. focus 시작/완료·필수 정보 가림 검사는 자체 QA 적용이다. 호흡/왜곡/심도·모션블러의 정량 관계는 여기서 입증하지 않으며 실제 설정/캘리브레이션 없이는 미확인이다.
- **차량 접촉·공간 연속성 / 인계**: 조건부 no-slip·topology 표시·버전/ID 필드는 자체 설계다. 위 책 구간은 차량 역학이나 portal의 정확성을 지원하지 않는다. 실루엣/포즈 가독성은 E2-STANCHFIELD L67–69, L223의 원리이며 BBox로 대신 검증하지 않는다.

기존 실행 기록 W2-NUMERIC/W2-BLENDER는 좌표 예제와 첫 샷 첫 프레임만 다룬다. 이번 인용 보정은 새 timing playback·rack-focus·gesture 렌더 검증이 아니다. 해당 동적 결과는 실제 출력 검수 전까지 UNVERIFIED다.
