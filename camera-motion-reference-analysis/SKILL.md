---
name: camera-motion-reference-analysis
version: 1.0
description: Analyze camera movement in supplied reference video or time-coded observations.
  Use for camera walking, dolly, tracking, pan, tilt, orbit, handheld, reveal timing,
  lens/motion discrimination or a reference-derived motion brief. Separate observed
  image motion from inferred 3D camera motion. Exclude generation and exact camera
  solving without tracking evidence.
---

# 레퍼런스 카메라 무빙 분석

1. 요청한 영상·구간·관객이 볼 대상·산출물을 확인한다. creative-production의 패킷을 받은 경우 shot_id·버전·범위를 유지한다. 일반 레퍼런스 분석은 video-production-assets의 reference25와 연결하고 카메라 부분만 맡는다.
2. [분석 절차](references/motion-analysis.md)를 읽는다. 실제 영상을 볼 수 있는지 확인한다. URL·제목만 읽었으면 영상을 봤다고 말하지 않는다. 사용자 관찰만 있으면 사용자 기록에 대한 분석으로 끝낸다.
3. 추출·정밀 트래킹이 필요할 때만 [프로그램과 검사 경계](references/programs.md)를 읽는다. 설치·로그인·전체 영상 다운로드를 기본 작업으로 확대하지 않는다.
4. 컷 경계와 샷 내 움직임을 구분한다. 원본 타임코드/PTS, 샷 로컬 초, FPS·프레임 기준과 실제 검사 범위를 기록한다. VFR을 CFR 프레임번호로 오인하지 않는다.
5. 움직임 시작·변화·정지, 가림/공개/행동 정점 전후를 관찰한다. 스틸 3장만으로 속도와 흔들림을 판정하지 않는다. 재생이 없으면 동적 품질은 미검증이다.
6. 고정 배경 특징, 깊이별 시차, 피사체 위치·크기, 가장자리와 소실점, 초점 변화를 비교한다. 팬/틸트·병진·줌/크롭·피사체 이동·랙 포커스를 분리하되 혼합/판별불가도 허용한다.
7. 관찰된 화면 변화 → 가능한 원인/대안 → 정보·감정 기능(해석) → 새 소재 적용 제안을 쓴다. 방향은 screen/world/subject 기준을 명시한다. 카메라의 미터 거리·속도·초점거리·리그를 픽셀 움직임만으로 확정하지 않는다.
8. 필요한 경우에만 Blender 카메라 솔브를 제안한다. 정적 트랙·시차·렌즈/스케일 근거·실제 솔브 결과·재투영 검사 없이 정확한 복원이라 주장하지 않는다. 회전만 있는 영상·평면·모션블러·AI 배경 변형의 제약을 남긴다.
9. [인계 템플릿](assets/motion-analysis-template.md)을 채워 camera-spatial-design에 전달한다. 관찰과 새 설계를 분리한다. 미터 경로·시간 곡선·렌즈 선택의 정본은 그 스킬에서 설계한다.

## 완료와 저장
원본 구간, 근거 종류, 카메라/피사체/렌즈 구분, 시간 구간, 가설·미확인, 재사용할 무빙 의도와 실제 검사 범위를 납품한다. 직접 관찰은 OBSERVED, 사용자 기록은 USER_REPORTED, 추정은 ESTIMATED, 새 제작 수치는 DESIGN_PROPOSAL로 표시한다. 창작 해석을 성과 측정으로 표현하지 않는다.

상대 스킬 폴더명은 설치 후 달라질 수 있으므로 /root/.codex/skills/remote-skills/*/SKILL.md의 정확한 name으로 찾아 참조를 연다. 파일 요청은 기존 제작 이력·Library 저장 흐름을 따른다. 채팅 전용은 파일을 만들지 않는다. 실제 생성은 담당 스킬에 인계한다.
