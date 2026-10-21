# Blender 프리비즈 인계
project_id / scene·shot·beat·panel ID 범위: {값}
camera artifact ID / spec version / spec sha256 / spec 파일: {manifest.camera_spec 및 입력 명세 기록}
Blender version / engine / 실행 명령·mode·render-map: {실제 기록}
워크플로 단계: planned / generated / inspected — 정본 artifact 상태(draft/reviewed/approved/generated/verified/stale)는 별도다. inspected는 실제로 연 파일 증거가 있을 때만 정본 verified 후보가 된다.
실제 .blend 파일: {없으면 null}
샷별 미리보기/시퀀스 위치와 렌더된 로컬 프레임 → 패널 ID 대응(manifest.rendered·blender-inspection.rendered): {실제 파일}
출력 해상도·fps·프레임 수(smoke면 저해상도·1프레임 한정임을 명시): {측정}
수치 검사(numerical-analysis)와 Blender 검사(blender-inspection): {구분}
확인한 프레임과 관찰: {목록}
수정한 명세/샷 ID: {값}
미검증 범위: {목록}

생성 참조로 인계할 때만 — [실무 인계 R1/R3](../../video-production-assets/references/29-reference-driven-production.md):
- 대역 ID/색/이름 → 실제 character ID/버전 대응: {확인된 매핑}
- 가져올 정보: {검사된 카메라/컷/블로킹/타이밍과 해당 근거 프레임; 정지 렌더의 시간 검증 한계 명시}
- 제외할 정보: {대역 얼굴/체형/재질/임시 배경·음향}
- 직전 채택 클립의 실제 종료 상태 / 외형·장소 기준 / 충돌 시 속성별 우선 기준: {각 ID/버전 또는 미해결}
- 대응 시점 비교: {배치→접촉/지지→카메라 경로→컷→끝 상태; 실제 검사 범위만}
- 움직이는 출력: {별도 승인·실제 파일이 없으면 미실행; 정지 프레임을 영상 검사로 보고하지 않음}

camera-intent artifact ID/version / selected camera-language catalog IDs: {해당 시}
기법별 구현 상태(현재 어댑터 / 확장 필요 / 편집 단계 / unsupported·unverified)와 근거: {구현표 ID·증거}
