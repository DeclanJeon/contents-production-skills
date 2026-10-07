---
name: ai-camera-control
version: 1.0
description: Translate camera motion, timing, blocking, lens and continuity plans
  into model-neutral or selected-provider AI video prompts and control packets. Use
  for start/end-frame camera control, camera path prompts, shot decomposition or correction
  of generated camera movement. Exclude camera design from scratch, actual paid submission
  and guarantees of unsupported exact 3D camera control.
---

# AI 카메라 제어

1. shot_id·길이·화면비·주목 대상·camera_spec 버전과 잠긴 입력을 받는다. 설계가 미정이면 camera-spatial-design 또는 최소 미확정 항목으로 돌려보낸다. 텍스트 요청에 미디어나 추가 샷을 자동 생성하지 않는다.
2. [변환 계약](references/control-contract.md)을 읽고 [제어 패킷](assets/camera-control-template.md)을 채운다. 시간·좌표·단위·피사체 동선을 보존한다.
3. 모델 중립안은 프로그램/계정 없이 작성한다. 특정 공급자 입력안 또는 실제 실행이면 선택 공식 플러그인과 현재 도구 스키마에서 입력·길이·화면비·참조 수·시작/끝 프레임·영상/경로 지원을 확인한다. creative-production의 생성 계획 계약을 적용하고 기존 사용자 권한을 재사용한다.
4. 고정 장면 → 피사체 동작 → 카메라 동작 → 시간/공개 → 렌즈/초점 → 연속성 순으로 작성한다. 방향 기준, 움직임 시작·감속·정지, 끝 프레이밍을 명시한다. 상충하는 무빙 단어를 나열하지 않는다.
5. 각 요구를 HARD_CONTROL(스키마로 확인된 입력), SOFT_PROMPT(텍스트 의도), UNSUPPORTED/UNVERIFIED로 분류한다. 프롬프트 수치·시작/끝 이미지가 실제 경로나 중간 움직임을 보장하지 않는다는 한계를 적는다.
6. 비지원 요구는 원래 요구와 차이를 보여준다. 단순 무빙·샷 분할·승인된 참조 영상·Blender 프리비즈·후반 합성을 대안으로 제안한다. 공급자·샷 수·길이·비용·입력 자산을 무단 변경하지 않는다. 분할안은 새 ID 제안과 비트/패널 매핑을 포함한다.
7. 실제 공개/접촉 시점, 시작·끝 구도, 공간 안정성, 속도 변화, 대상 유지, 축/컷 연결의 통과 기준을 쓴다. 실제 결과가 있으면 video-production-assets의 카메라 무빙 QA를 적용하고 문제→증거 시각→최소 수정→재검사 범위를 돌려준다. 재시도는 승인된 범위에서만 한다.

## 인계와 실행 경계
설계/참조 ID·버전, prompt, 실제 지원 provider_inputs, 지원/미지원 표, frame/asset 참조, 검사 기준·미확인을 인계한다. 생성 요청은 선택 공식 플러그인에 전달한다. 초안은 생성된 영상이 아니다. 정확한 궤적이 필수인데 선택 모델이 지원하지 않으면 결정적인 3D 렌더/합성 대안 또는 미충족으로 보고한다.

형제 스킬은 /root/.codex/skills/remote-skills/*/SKILL.md의 정확한 name으로 찾아 읽는다. 채팅 전용은 저장하지 않는다. 실제 파일은 제작 이력·Library 저장을 따른다. 실행 환경은 [프로그램](references/programs.md)을 읽는다.
