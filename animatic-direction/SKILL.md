---
name: animatic-direction
version: 1.0
description: Use when an approved story or board needs an animatic timing plan, cut and hold revision, or timed-board playtest plan. Includes 애니매틱 시간화 and 재생 검수 계획; not every storyboard, still-image edit, or request for silent storytelling.
---

# 애니매틱 시간 연출

**무엇을 읽고 기다리고 확인할 시간인지부터 정하고, 그 시간을 샷 안과 컷 사이에 배치한다.** 이 스킬은 요청된 시간화·검수 계획의 작은 진입점이며 렌더러가 아니다.

## 진행

1. **입력을 이어받는다.** 승인된 이야기·보드 버전과 scene/beat/shot/panel ID, 보존할 공개 순서·행동·결과, 요청 산출물을 적는다. 확정 브리프는 재인터뷰하지 않는다. runtime이 고정인지 유연한지, FPS·전환/크레딧 포함 여부를 확정 또는 미정/제안으로 표시한다. `no_dialogue`, `no_audio`, 자막/화면 글자 금지는 독립 조건이다. 내레이션·노래·비언어 발성·SFX·음악도 허용 범위를 따른다.
2. **단위를 나눈다.** key panel은 한 시점의 상태, shot은 컷 사이의 연속 구간, phase는 그 안의 접근·접촉·전환 등 변화, hold는 읽기·기대·유보·반응을 유지하는 시간이다. 패널 수로 컷 수나 동일 길이를 계산하지 않는다. 실제 상태가 변하면 한 장의 hold 패널로 동작 전체를 대신하지 않는다.
3. **목적별 시간을 제안한다.** 관객이 알아차릴 정보→행동/접촉→반응·선택→남는 상태 중 필요한 국면에 시간을 준다. 짧은 충격, 긴 고요, 여러 정점, 의도적 균등 템포 모두 가능하다. 길이는 기능으로 설명하며 최소/최대 컷 길이·필수 에너지 곡선·결말·해부학 큐를 강제하지 않는다. 기존 화면을 먼저 쓰고 임의의 카메라 해법을 추가하지 않는다.
4. **기존 표에 시간화한다.** 아래 표의 소유 필드로 연결한다. 수치 시간표, action cut, 프레임 변환 또는 재생 검수 계획을 작성할 때는 [시간·검수 참조](references/timing-and-review.md)를 읽고 해당 절을 적용한다. 09 final 시간이 정본이며 06/08은 같은 시간을 shot-local로 투영한다. FPS 미정이면 초 제안을 유지하고 프레임을 발명하지 않는다.
5. **길이 충돌을 해결한다.** 고정 runtime이면 필수 인과·공개·반응을 보존하며 중복을 줄이고 국소 재배분한다. 성립하지 않으면 초과 위치와 필요한 축소/연장 승인을 반환한다. 유연하면 읽힘 우선 길이와 더 짧은 대안을 제안한다. 전체 비례 압축이나 재생속도 변경으로 필수 사건을 숨기지 않는다.
6. **검사 범위를 반환한다.** 합계·순서·컷 연결·접촉/소유·잔류 상태·반응/정착 구간을 대조한다. 텍스트 계획 / 실제 이미지 읽힘 / 시간 재생을 구분해 대상 버전·위치·관찰·미검증을 적는다. 실제 재생이 없으면 리듬은 `UNVERIFIED`; 스틸에서 원래 초수/FPS/소리를 복원하거나 문서만으로 PASS하지 않는다.

## 인계 — 깊은 소유자는 그대로

| 필요한 일 | 정본 / 받는 내용 |
|---|---|
| 공개·유보, 샷 내부 큐 | `video-production-assets` [06](../video-production-assets/assets/06-shots-template.md): `shot-local time (s or frames; FPS if frames)`, `공개 정보`, `종료 프레임`와 기존 cue 표 |
| 포즈·접촉·스페이싱 | [08](../video-production-assets/assets/08-animation-template.md): `포즈/행동`, `시작 프레임`, `끝 프레임(미포함)`, `스페이싱`, 기존 접촉 열 |
| 컷·소스/최종 시간·여운 | [09](../video-production-assets/assets/09-edit-template.md): `source_in_s`/`source_out_s`, `final_start_s`/`final_end_s`, 기존 컷 이유·reaction/settle 열 |

이야기 수정은 `silent-visual-storytelling`/각본 소유자, 보드·패널 수정은 `storyboarding-video`, 실제 스틸 전용 편집은 `storytelling-with-still-images`, 수치 카메라는 `camera-spatial-design`, 실제 QA는 12가 소유한다. 전문 단계로 배정되면 상위 계약을 따르고 별도 원장·스키마를 만들지 않는다. 전용 풍자 계약은 명시적 풍자 요청에만 적용한다.

## 완료

요청 범위의 시간표·국면/hold·컷 이유·연속 상태·길이 충돌·재생 검사 계획과 미검증을 반환하면 계획 완료다. 실제 보드/재생이 필요한 수락은 별도이며 생성·업로드·설치·지출·원본 추가 연구를 자동 실행하지 않는다.
