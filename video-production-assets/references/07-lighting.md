# 조명·노출·샷 매칭

## 입력과 산출물
입력: 룩, 샷·블로킹, 장소·시간대, 사용 장비

산출물: 광원 계획, 노출 의도, 조명 연속성표

## 실행 절차
1. 장면에서 보이는 광원과 광원이 있다고 느낄 방향을 정한다. 자연광·실용등·표현 조명의 동기를 구분한다.
2. 키·필·배경·분리광의 필요를 검토하되 모든 장면에 네 개를 의무 배치하지 않는다. 그림자로 무엇을 감추고 언제 드러낼지 정한다.
감금·구속을 나타내는 조명이라면 벽에 드리운 막대 그림자로도 감옥을 읽히게 할 수 있다. 이 단서를 쓰면 최종 프레임에서 그림자 패턴이 구별되는지 확인한다; 이는 선택 가능한 표현이지 모든 장면의 의무 규칙은 아니다 (자료 02, READ-PARTIAL; `sources.md`).
3. 광원 방향·높이·상대 크기·확산·색·피사체 거리를 기록한다. 광원 크기와 거리를 함께 고려해 그림자의 경도를 설계한다.
4. 인물 동선 전 구간의 얼굴과 배경 분리를 확인한다. 역방향 샷에서 광원 위치와 그림자 논리가 이어지게 한다.
5. 명암비·색온도·노출 수치는 목표값으로 표시하고 현장 측정과 테스트로 확정한다. 역사적 필름 장비·전압·감도 관행을 현대 디지털 장비에 그대로 적용하지 않는다.
6. AI 영상은 광원 방향·색·그림자 규칙을 프롬프트와 연속성에 포함한다. 실제 조도·물리 노출을 제어했다고 주장하지 않는다.
7. 브리프가 한 샷 안의 조명 변화·리빌을 요구하면 proposal로 shot-local `start → change → settle → hold` cue와 그때 새로 읽히는 정보를 적는다. 프레이밍과 기하학적 기준점은 유지한다. 실제 변화 경계와 원인이 직접 확인되지 않으면 이를 `unknown`으로 기록하고, 컷·카메라 이동·조명 변화를 단정하지 않는다. 외관만으로 조명기구·노출·초점 메커니즘을 추론하지 않는다. 기존 템플릿의 matching notes/shadow rule 등 해당 칸을 사용하고 새 필드나 보편 타이밍을 만들지 않는다.

반사 하이라이트가 제품/카피의 핵심일 때만 추가로 지정한다: 라벨 읽기 영역, 반사 띠의 형태와 이동 방향, 투명·반사면에서 읽혀야 할 실루엣/내용물. 이것이 실제 광원·반사인지 별도 그래픽 레이어인지 구분해 기존 조명 칸에 적는다. 광원기구·렌즈·노출이 보이지 않으면 추정하지 않는다. 검수는 승인된 정지 이미지/연속 프레임/렌더의 표본과 최종 크롭에서 하이라이트 이동, 로고·라벨 가독성, 인접 샷 일관성을 대조한다. 정확한 라벨 반사/가림은 [제품 통합](19-brand-product-integration.md)과 [생성 영상 QA](21-generated-video-qa-retry.md)에 넘긴다.

## 공간에 고정된 광원과 노출 표기 (해당 시)

역방향/카메라 회전/날씨·시간대 변형에는 [실무 인계 R3](29-reference-driven-production.md#space-performance)를 적용한다(GUIDE-01 pp44–47, 51–55). 기존 `방향/높이`, `그림자 규칙`, `노출 상태`, `매칭 주의`에 공간상의 광원/랜드마크 기준과 각 샷의 화면상 방향을 구별한다. 카메라가 돌아섰다는 이유로 광원 자체를 반대편으로 옮기지 않으며, 의도된 보조광/표현광 예외는 이유를 적는다. f-number/T-stop이 등장하면 실제 입력 표기를 보존하고 임의 변환하지 않는다. T값만으로 피사계 심도를 판정하거나 UI에 없는 T 제어를 적용했다고 하지 않는다. 주요 대상/접촉 부위의 실제 선명도를 별도로 검사한다. 경험서의 표기 선호는 광학 효능/AI 품질 보장이 아니다.

## 완료 조건
의도한 얼굴·소품이 읽히는가? 광원과 그림자가 일치하는가? 반대 샷에서도 룩이 이어지는가?

## 근거와 적용 범위
자료 ID: 02,04,08. `sources.md`에서 파일 상태와 탐색 위치를 확인한다. 절차와 템플릿은 여러 자료의 개념을 결합한 독자 설계다. 저자의 규칙을 그대로 재현한 요약이나 공식 인증된 방법론으로 표현하지 않는다.
02 L187 `PRISON SCENES`(READ-PARTIAL)은 위 막대 그림자 단서만 직접 지원한다. 목표 수치/실측/AI 제어 구분은 운영 규격이다. 본문 없는 01을 보충 근거로 쓰지 않는다.

E5 직접 읽기(READ-PARTIAL): `E:/Book/06_Book/originals/콘텐츠_제작/md/Painting With Light (John Alton) (z-library.sk, 1lib.sk, z-lib.sk).md`, SHA-256 `19beb6f8d6d3d44888e675941d30a493e4e3cf2a386b0d963d99370e74dded7f`, 560865 bytes, L137–141(p30 이후 `LIGHTING`/`THE PURPOSE OF ILLUMINATION`). 실용등에서 오는 것처럼 보이는 key 위치 선정·측광·전경/배경 명암 분리를 지원한다. 역사적 기구/필름 수치를 현대 장비에 이식하거나 네 광원을 의무화하지 않는다.

광원 크기와 경도: [Blender 공식 Light Objects 문서](https://docs.blender.org/manual/en/latest/render/lights/light_object.html)의 `Point Light > Radius`, `Spot Light > Radius/Beam Shape`, `Area Light`(2026-10-17 직접 읽음, READ-PARTIAL, 페이지 표기 Blender 5.2 LTS). 큰 발광면의 부드러운 그림자, 광원 거리의 감쇠, spot cone 가장자리의 Blend와 물체 그림자의 경도는 별개라는 기술 범위만 지원한다. live 문서라 로컬 rendition/hash/bytes 없음(`N/A-live-web`), 설치 버전/렌더 실행 미확인이다. 거리와 상대 크기를 함께 적는 계획은 유지하되 이 문서만으로 거리별 경도 수치나 역방향 샷 매칭 전체를 입증하지 않는다. 역방향의 광원/그림자 논리·반사 띠의 정확한 재현은 아직 개별 원문 미결속이며 실제 인접 샷 검수가 필요하다.

추가 공식 원문: [Bill Holshevnikoff, ARRI Lighting Handbook, Fourth Edition ©2016](https://www.arri.com/resource/blob/83996/409091c612f371b0c68b41d9dcb636db/arri-lighting-handbook-english-data.pdf), pp5–8 `Light Quality/Hard vs. Soft Light`, pp10–15 `A Note on Color/Basic Definitions`, pp16–17 `Shadow Edge Transfer`(2026-10-17, READ-PARTIAL, 웹 PDF 텍스트 직접 읽기, rendition=위 URL, hash/bytes=`N/A-live-web`, 도판 미검사). 확산지의 실제 조명된 면이 유효 광원이 된다는 설명, 크기와 shadow edge의 관계, 광원 색과 주변광 매칭, close-up별 key 위치와 불필요한 separation light 생략을 지원한다. 따라서 기구 출력만이 아니라 유효 발광면·그림자 경계를 비교한다. 역방향 전체 매칭과 거리별 경도 정량 법칙은 이 구간의 직접 주장이 아니며 미결속으로 유지한다.
추가 직접 읽기(READ-PARTIAL): Alton, `E:/Book/06_Book/originals/콘텐츠_제작/md/Painting With Light (John Alton) (z-library.sk, 1lib.sk, z-lib.sk).md`, SHA-256 `19beb6f8d6d3d44888e675941d30a493e4e3cf2a386b0d963d99370e74dded7f`, 560865 bytes, L285(p103). 반사 각도와 피부결에 따라 meter reading과 보이는 반사 밝기가 달라질 수 있다는 사례다. 특정 제품의 움직이는 반사 띠, 모든 역방향 매칭, 혹은 거리별 그림자 경도 공식의 직접 근거는 아니다.

## 출력 템플릿
`assets/07-lighting-template.md`를 복사해 채운다.
