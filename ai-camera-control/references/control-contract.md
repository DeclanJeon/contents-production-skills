# 설계에서 생성 입력으로

## 보존 정보
shot_id/scene_id/beat_id/panel_ids, camera_spec ID/version, source asset ID/version, duration/fps/aspect, subject path, camera path/target, lens/focus, reveal/contact timing, 좌표·단위, 정체성/제품/배경 앵커. 단독 요청에 불필요한 전체 원장을 만들지 않는다.

## 변환과 지원
현재 도구가 실제 받는 duration/aspect/reference/start_frame/end_frame 등의 확인된 필드만 HARD_CONTROL로 표시한다. 참조 지원과 완전한 경로 지원을 구분한다. camera curve·speed·lens의 텍스트 지시는 SOFT_PROMPT이며 생성 후 검사한다. 스키마 한도를 넘는 잠긴 입력을 조용히 잘라 제출하지 않는다. 모델/스키마 확인이 없으면 provider_inputs는 비우고 UNVERIFIED로 남긴다.

카메라 이동·회전·줌·초점·피사체 운동을 각각 명시한다. 복합 움직임은 채널별 시점·동기를 분리한다. 단순화/분할은 제안이며 정보 순서·길이·샷 수를 자동 변경하지 않는다. 일반 텍스트를 정확한 3D 제어로 소개하지 않는다.

## 수정 사다리
잘못된 기준 방향/미확정 입력 → 명세 수정; 상충 프롬프트 → 지시 축소; 지원 제어 누락 → 입력 보완; 공간/시간 불안정 → 승인된 참조·단순 무빙·분할 검토; 정확한 기하 요구 실패 → 결정적 3D/합성 제안. 모델·비용·샷 수 변경은 기존 권한에 대조한다. 편집으로 고칠 수 있는지도 실제 결과로 확인한다.
