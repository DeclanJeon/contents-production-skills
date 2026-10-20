# 설계에서 생성 입력으로

## 보존 정보
shot_id/scene_id/beat_id/panel_ids, camera_spec ID/version, source asset ID/version, duration/fps/aspect, subject path, camera path/target, lens/focus, reveal/contact timing, 좌표·단위, 정체성/제품/배경 앵커. 단독 요청에 불필요한 전체 원장을 만들지 않는다.

Each source reference includes a resolvable file/section or supplied-text locator, its shot ID and version; a title such as “approved plan” alone is insufficient. If no version was supplied, record `unversioned supplied text` rather than inventing an approval/version. Carry missing lens, effective gate, duration/FPS or move onset/settle timing as `UNRESOLVED` in the packet and return the affected numeric directive to camera-spatial-design. A request such as “push in” permits a qualitative SOFT_PROMPT draft, not an invented 35 mm lens, two-metre path or four-second duration. Never populate a numeric provider field from that draft.

## 변환과 지원
현재 도구가 실제 받는 duration/aspect/reference/start_frame/end_frame 등의 확인된 필드만 HARD_CONTROL로 표시한다. 참조 지원과 완전한 경로 지원을 구분한다. camera curve·speed·lens의 텍스트 지시는 SOFT_PROMPT이며 생성 후 검사한다. 스키마 한도를 넘는 잠긴 입력을 조용히 잘라 제출하지 않는다. 모델/스키마 확인이 없으면 provider_inputs는 비우고 UNVERIFIED로 남긴다.

카메라 이동·회전·줌·초점·피사체 운동을 각각 명시한다. 복합 움직임은 채널별 시점·동기를 분리한다. 단순화/분할은 제안이며 정보 순서·길이·샷 수를 자동 변경하지 않는다. 일반 텍스트를 정확한 3D 제어로 소개하지 않는다.

## 참조 역할·촬영 표기 대조 (해당 시)

복합 이미지/지도/영상/프리비즈 입력은 [실무 인계 R1](../../video-production-assets/references/29-reference-driven-production.md#reference-roles)로 실제 파일→슬롯→사용/제외 속성→우선 기준을 확인하고 11의 기존 역할표를 참조한다. 직전 클립은 실제 끝 상태, 프리비즈는 지정 카메라/동선에 역할을 한정하고 대역 외형은 제외한다. T-stop/f-number·시차/줌·전경 가림은 [R3](../../video-production-assets/references/29-reference-driven-production.md#space-performance)와 카메라 오너의 lens companion에서 보존한다. 실제 endpoint에 없는 T/렌즈/경로 필드를 발명하거나 문장만으로 HARD_CONTROL을 승격하지 않는다. 이 보강은 GUIDE-01 pp50–55, 64–69, 74–82의 인계 일반화이며 실제 도구 계약/품질 검증이 아니다.

## 수정 사다리
잘못된 기준 방향/미확정 입력 → 명세 수정; 상충 프롬프트 → 지시 축소; 지원 제어 누락 → 입력 보완; 공간/시간 불안정 → 승인된 참조·단순 무빙·분할 검토; 정확한 기하 요구 실패 → 결정적 3D/합성 제안. 모델·비용·샷 수 변경은 기존 권한에 대조한다. 편집으로 고칠 수 있는지도 실제 결과로 확인한다.
