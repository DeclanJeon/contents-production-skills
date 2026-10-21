# 설계에서 생성 입력으로

## 보존 정보
shot_id/scene_id/beat_id/panel_ids, camera_intent ID/version, 선택한 camera-language catalog IDs, camera_spec ID/version, source asset ID/version, duration/fps/aspect, subject path, camera path/target, lens/focus, reveal/contact timing, 좌표·단위, 정체성/제품/배경 앵커를 보존한다. 선택한 카탈로그 명칭을 임의의 수치 경로나 provider 제어로 바꾸지 않고, shot intent와 구현/지원 상태를 제어 패킷까지 전달한다. 단독 요청에 불필요한 전체 원장을 만들지 않는다.

Each source reference includes a resolvable file/section or supplied-text locator, its shot ID and version; a title such as “approved plan” alone is insufficient. If no version was supplied, record `unversioned supplied text` rather than inventing an approval/version. Carry missing lens, effective gate, duration/FPS or move onset/settle timing as `UNRESOLVED` in the packet and return the affected numeric directive to camera-spatial-design. A request such as “push in” permits a qualitative SOFT_PROMPT draft, not an invented 35 mm lens, two-metre path or four-second duration. Never populate a numeric provider field from that draft.

## 변환과 지원
현재 도구가 실제 받는 duration/aspect/reference/start_frame/end_frame 등의 확인된 필드만 HARD_CONTROL로 표시한다. 참조 지원과 완전한 경로 지원을 구분한다. camera curve·speed·lens의 텍스트 지시는 SOFT_PROMPT이며 생성 후 검사한다. 스키마 한도를 넘는 잠긴 입력을 조용히 잘라 제출하지 않는다. 모델/스키마 확인이 없으면 provider_inputs는 비우고 UNVERIFIED로 남긴다.

카메라 이동·회전·줌·초점·피사체 운동을 각각 명시한다. 복합 움직임은 채널별 시점·동기를 분리한다. 단순화/분할은 제안이며 정보 순서·길이·샷 수를 자동 변경하지 않는다. 일반 텍스트를 정확한 3D 제어로 소개하지 않는다.

## 참조 역할·촬영 표기 대조 (해당 시)

복합 이미지/지도/영상/프리비즈 입력은 [실무 인계 R1](../../video-production-assets/references/29-reference-driven-production.md#reference-roles)로 실제 파일→슬롯→사용/제외 속성→우선 기준을 확인하고 11의 기존 역할표를 참조한다. 직전 클립은 실제 끝 상태, 프리비즈는 지정 카메라/동선에 역할을 한정하고 대역 외형은 제외한다. T-stop/f-number·시차/줌·전경 가림은 [R3](../../video-production-assets/references/29-reference-driven-production.md#space-performance)와 카메라 오너의 lens companion에서 보존한다. 실제 endpoint에 없는 T/렌즈/경로 필드를 발명하거나 문장만으로 HARD_CONTROL을 승격하지 않는다. 이 보강은 GUIDE-01 pp50–55, 64–69, 74–82의 인계 일반화이며 실제 도구 계약/품질 검증이 아니다.

패킷의 참조 역할표는 위 R1 역할표를 **슬롯 단위로 복제하지 않는다.** R1은 속성 계약을 정하고, 이 스킬의 패킷은 실제로 보낸 슬롯 태그(@image1 등)와 그 슬롯이 가져올/버릴 속성·충돌 우선 기준만 적는다. 첨부하지 않은 파일에는 태그를 쓰지 않고, 슬롯 수가 바뀌면 태그와 제출문을 다시 맞춘다.

## 시간 구간 행동·보존 제약·오디오 분리

한 샷 안에서 시간이 지나면서 달라지는 것을 **shot-local 구간**으로 나눈다(예: 0–2초 / 2–5초 / 5–7초 / 7–8초). 각 구간에 피사체 행동, 카메라 상태(고정/이동), 새로 공개되는 정보·감정, 컷·정착 지점을 적는다. 구간 표는 이 스킬이 소유한다. 전체 편집 타임라인 시간은 편집 담당 소유이므로 shot-local basis(frames 또는 FPS를 명시한 seconds)와 섞지 않는다. 카메라가 샷 전체에서 고정이면 한 번만 고정으로 적고 구간마다 되풀이하지 않는다.

**보존 제약(하지 말 것)**은 생성 후에도 유지되어야 하는 상수다: 인물 정체성·의상, 소품의 상태와 소유 손, 이미 확립된 공간·소품 배치, 조명 방향, 화면 방향/180도 축 앵커, 이어서 계속되어야 하는 움직임. 각 항목은 (1) 유지되는 것, (2) 근거가 되는 shot/beat/panel ID 또는 승인 참조, (3) 생성 후 확인 방법(승인 프레임과의 시각 대조) 세 칸으로 적는다. 부정형 지시는 긍정형 계획을 대신하지 않는다. "이게 바뀌면 안 된다"만 쓰지 말고 해당 구간에서 실제로 바뀌는 것을 구간 표에 함께 적는다.

**오디오·대사는 별도 채널이다.** 대사·효과음·앰비언스·음악은 자체 cue ID와 타이밍을 가진 편집 항목이며, 시각 프롬프트에 "박자에 맞춰" 같은 오디오 리듬 지시를 시각 행동으로 옮기지 않는다. 제공자가 오디오 필드를 노출하면 실제 필드명을 명시하고, 아니면 `UNSUPPORTED`로 표시해 편집 담당에 넘긴다. 생성된 소리가 그 시각 행동이 그 시각에 일어났다는 증거가 되지 않는다.

## 수정 사다리
잘못된 기준 방향/미확정 입력 → 명세 수정; 상충 프롬프트 → 지시 축소; 지원 제어 누락 → 입력 보완; 공간/시간 불안정 → 승인된 참조·단순 무빙·분할 검토; 정확한 기하 요구 실패 → 결정적 3D/합성 제안. 모델·비용·샷 수 변경은 기존 권한에 대조한다. 편집으로 고칠 수 있는지도 실제 결과로 확인한다.
