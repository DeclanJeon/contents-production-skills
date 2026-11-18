# 연출 용어 크로스워크

입력 문서: `CINEMATIC_DIRECTING_BIBLE_v1.md` v1.0, 2026-11-18, 39,052 bytes, SHA-256 `b2eceb86088ec17d4b65361a55d00c7ad5b39db3294de367d132690efb95e91b`. 이 문서는 사용자가 작성한 **프로젝트용 분류 제안**이며 공인 분류·검증된 효과 연구·서적 근거가 아니다. 어느 항목도 이 패키지의 정본을 대신하지 않는다.

보관 사본: `docs/research/2026-11-18-cinematic-directing-bible-v1.md`(동일 해시).

이 파일은 **조회용 포인터**다. 정의·수치·검수 기준은 각 정본이 소유하고 여기서 다시 쓰지 않는다. 문서 ID(`ST-01` 등)는 검색 편의를 위한 표기이며 패키지 스키마·필드가 아니다. 요청이 문서 용어로 들어오면 이 표로 정본을 찾은 뒤 그 문서의 절차를 따른다.

## 30범주 → 정본

상태: **충족**(정본이 동등 이상), **이관**(이번에 용어·조건을 정본에 추가), **거부**(§이관하지 않은 요소).

| 문서 범주 | 문서 용어 예 | 정본 | 상태 | 주의 |
|---|---|---|---|---|
| 01 Narrative Pacing | build-up, tension & release, pacing contrast | [09 시퀀스 리듬 계약](09-edit.md#시퀀스-리듬-계약), [속도 대비 곡선](09-edit.md#속도-대비-곡선-선택) | 충족 | 곡선은 선택 레시피이며 필수 아치가 아니다 |
| 02 Rhythmic Editing | beat cutting, cutting on action, staccato | [속도·타격 표현 선택표](edit-sound-language-catalog.md#속도타격-표현-선택표), [09 비트 기준](09-edit.md#실행-가능한-편집사운드-큐) | 충족 | 박 시각은 승인된 오디오 마스터에서 측정한다 |
| 03 Speed & Time | speed ramping, time remapping, freeze frame | [B. 이동·촬영 방식](../../camera-spatial-design/references/camera-language-catalog.md#b-카메라-이동촬영-방식전환-24종), [09 배속과 원본](09-edit.md#배속과-원본) | 충족 | 램프는 구간별 `playback_rate`로만 주장한다 |
| 04 Timing & Spacing | event frame, spacing, anticipation, ease, overshoot, follow-through | [08 실행 절차](08-animation.md#실행-절차), [모션 속도·타격 기법](08-animation.md#모션-자체의-속도타격-기법) | 충족 | fps와 노출 프레임 수를 구분한다 |
| 05 Camera Movement | tracking, push-in, whip pan, orbit, handheld | [B. 이동·촬영 방식](../../camera-spatial-design/references/camera-language-catalog.md#b-카메라-이동촬영-방식전환-24종) | 충족 | 문서의 crash zoom은 B04 줌 인의 강도 변형 |
| 06 Action Choreography | action beats, blocking, contact timing, reaction chain | [21 §1 모션·물리](21-generated-video-qa-retry.md#1-ai-모션물리-디렉팅), [26 최소 슬롯](26-state-causality-continuity.md#인계-최소-슬롯) | 충족 | 접촉 우선순위·샷 분할 트리거를 따른다 |
| 07 Visual Effects | motion blur, impact frame, camera shake, particle, light flash, lens | [속도·타격 표현 선택표](edit-sound-language-catalog.md#속도타격-표현-선택표), [21 §2 VFX](21-generated-video-qa-retry.md#2-vfx합성-수퍼비전), [23 피니싱](23-finishing-platform.md#1-시네마틱-피니싱) | 충족 | 섬광은 동기 광원(07), 렌즈 계열은 23 텍스처가 소유 |
| 08 Sound Design | layered impact, whoosh, riser, pre-impact silence, sound bridge, transient | [효과음 설계 선택표](edit-sound-language-catalog.md#효과음-설계-선택표) | 이관 | 층·재질·시점이 실제로 분리될 때만 층 표기를 쓴다 |
| 09 Composition & Continuity | screen direction, 180 axis, eyeline, prop continuity, spatial map | [A. 구도·시점](../../camera-spatial-design/references/camera-language-catalog.md#a-구도시점-24종), [26 연속성 게이트](26-state-causality-continuity.md#전체-스토리라인-참조연속성-게이트-필수) | 충족 | 축 이동은 동기·중립 샷으로 정당화한다 |
| 10 AI Animatic | parallax, Ken Burns, start-end lock, path prompting, interpolation | [Still-image motion](../../storytelling-with-still-images/SKILL.md#still-image-motion) | 이관 | 스틸 모션은 계획이며 이동 속도 측정이 아니다 |
| 11 Acting & Performance | micro-expression, eye acting, breathing, reaction delay, asymmetry | [04 브릿지](04-performance.md#정지-이미지ai-생성용-표정신체-변환-브릿지-anatomical-expression-bridge) | 충족 | 표정 이름보다 생각·목표가 읽히는 포즈를 쓴다 |
| 12 Mise-en-scène | foreground framing, negative space, depth staging, power blocking | [A. 구도·시점](../../camera-spatial-design/references/camera-language-catalog.md#a-구도시점-24종), [공통 시각 연출](visual-scene-communication.md#선택할-축) | 이관(전경 프레이밍 항목) | 3단 깊이는 `focal_hierarchy`가 정본 |
| 13 Cinematography & Optics | focal length, DOF, rack focus, angle, perspective matching | [A. 구도·시점](../../camera-spatial-design/references/camera-language-catalog.md#a-구도시점-24종), [21 §2 매칭](21-generated-video-qa-retry.md#2-vfx합성-수퍼비전) | 충족 | 렌즈 수치만으로 거리·구도를 확정하지 않는다 |
| 14 Lighting | motivated light, ratio, rim, practical, color temp, volumetric | [조명 표현 선택표](lighting-language-catalog.md) | 충족 | 광원 방향·세기를 컷마다 유지한다 |
| 15 Color Grading | exposure match, contrast curve, color separation, look, shot match | [23 시네마틱 피니싱](23-finishing-platform.md#1-시네마틱-피니싱) | 충족 | 그레이드는 구조 결함을 가리지 않는다 |
| 16 Physical Realism | ground contact, center of mass, collision response, cloth inertia | [21 §1](21-generated-video-qa-retry.md#1-ai-모션물리-디렉팅), [08 접촉 검수](08-animation.md#실행-절차) | 충족 | 접촉 그림자·발 미끄러짐을 실제 재생으로 본다 |
| 17 Emotional Direction | emotional beat, reaction priority, restraint, aftermath hold | [16 감정과 기억](16-concept-emotion-retention.md#2-감정과-기억-설계) | 충족 | 절제와 무반응을 구분한다 |
| 18 Advanced Film Grammar | POV, offscreen space, visual subtext, ellipsis, association | [06 정보 단위·POV](06-shots.md#정보-단위와-pov반응-인계), [26](26-state-causality-continuity.md#전체-스토리라인-참조연속성-게이트-필수) | 충족 | 정보 보유자·공개 순서를 기록한다 |
| 19 Temporal Consistency | identity/costume/prop lock, occlusion, lighting state | [26](26-state-causality-continuity.md#전체-스토리라인-참조연속성-게이트-필수), [21 §3 검사 패스](21-generated-video-qa-retry.md#3-생성-매체-qa) | 충족 | 상태 전환에는 실제 행동 컷이 필요하다 |
| 20 Post Pipeline | conform, compositing, Foley, VO, loudness, master | [23](23-finishing-platform.md#1-시네마틱-피니싱), [28 후반 프로필](28-film-production-lifecycle.md#후반작업-프로필) | 충족 | 계획표로 렌더·믹스 완료를 주장하지 않는다 |
| 21 Shot Coverage | master, medium, close, insert, cutaway, reaction | [06 실행 절차](06-shots.md#실행-절차), [A. 구도·시점](../../camera-spatial-design/references/camera-language-catalog.md#a-구도시점-24종) | 충족 | 샷 수를 고정 공식으로 강제하지 않는다 |
| 22 Eye Trace & Perception | eye trace, salience shift, masking, readability | [06 아이트레이스](06-shots.md#액션스피드-씬의-컷-간-스케일-낙차와-아이트레이스-scale-contrast-eye-trace), [21 판독 패스](21-generated-video-qa-retry.md#3-생성-매체-qa) | 충족 | 판독성은 실제 출력 크기에서 본다 |
| 23 Visual Storytelling | foreshadowing, metaphor, juxtaposition, reveal/conceal | [공통 시각 연출](visual-scene-communication.md#선택할-축), [무성 서사](../../silent-visual-storytelling/SKILL.md) | 충족 | 무언 서사에 대사·자막을 자동 추가하지 않는다 |
| 24 Production Design | location bible, costume/prop inventory, material palette | [05 장소·키 비주얼](05-visual.md#장소키-비주얼의-사용-범위), [26](26-state-causality-continuity.md#인계-최소-슬롯) | 충족 | 역방향은 좌우 반전이 아니다 |
| 25 Music Dramaturgy | leitmotif, ostinato, hit point, counterpoint | [음악 설계 선택표](edit-sound-language-catalog.md#음악-설계-선택표) | 이관 | 기준점 이름·오프셋은 09 비트 절이 정본 |
| 26 Spatial Audio | distance, early reflection, occlusion, pan, room tone, muffle | [공간 음향 선택표](edit-sound-language-catalog.md#공간-음향-선택표) | 이관 | 실제 채널 청취 없이는 미검증 |
| 27 Editorial Transitions | match cut, match on action, J/L-cut, smash cut | [17–24. 편집 전환](../../camera-spatial-design/references/camera-language-catalog.md#1724-편집-전환) | 충족 | 정의는 카메라 카탈로그, 인계 조건은 편집 카탈로그 |
| 28 Scene Objectives | want, obstacle, tactics, turning point, exit value | [02 실행 절차](02-story.md#실행-절차), [16 §2](16-concept-emotion-retention.md#2-감정과-기억-설계) | 충족 | 변화 없는 장면은 필요성을 재검토한다 |
| 29 Visual Quality Control | flicker, identity drift, anatomy, warp, contact, readability | [21 §3](21-generated-video-qa-retry.md#3-생성-매체-qa), [12 QA](12-qa.md) | 충족 | 반복 출력은 09 루프 검사로 넘긴다 |
| 30 Distribution & Accessibility | aspect framing, captions, frame-rate conform, color space, loudness, photosensitivity | [15 자막·접근성·납품](15-delivery.md#자막접근성출력납품), [광과민·흔들림 검사](15-delivery.md#광과민흔들림-편안함-검사-해당-시) | 이관(1항목) | 임계 수치를 발명하지 않는다 |

## 장르 조합 레시피 → 정본

문서의 조합 6종은 기존 레시피와 겹치므로 여기서 다시 쓰지 않는다. 필요한 구성 요소만 해당 정본에서 고른다.

| 문서 레시피 | 사용할 정본 | 비고 |
|---|---|---|
| 좀비 복도 추격 | [B. 이동·촬영 방식](../../camera-spatial-design/references/camera-language-catalog.md#b-카메라-이동촬영-방식전환-24종), [21 §1](21-generated-video-qa-retry.md#1-ai-모션물리-디렉팅) | 공간 지도·출구 인지가 합격 조건 |
| 맨손 격투 | [21 §1 접촉 우선순위](21-generated-video-qa-retry.md#접촉-우선순위), [속도·타격 표현](edit-sound-language-catalog.md#속도타격-표현-선택표) | 모든 타격에 슬로모션을 강제하지 않는다 |
| 감정적 이별 | [16 감정과 기억](16-concept-emotion-retention.md#2-감정과-기억-설계), [04](04-performance.md#실행-절차) | 줌·음악 고조를 기본값으로 두지 않는다 |
| 대사 없는 스틱맨 풍자 | [silent-satire-animatic](../../silent-satire-animatic/SKILL.md) | 전용 계약이 우선한다 |
| 공포 공간 탐색 | [A. 구도·시점](../../camera-spatial-design/references/camera-language-catalog.md#a-구도시점-24종), [조명 표현](lighting-language-catalog.md) | 위협 조기 공개를 피한다 |
| 패션·제품 숏폼 | [15](15-delivery.md#자막접근성출력납품), [23](23-finishing-platform.md#2-플랫폼-네이티브-적응) | 제품·의상 판독성 우선 |

## 이관하지 않은 요소

| 요소 | 이유 | 대체 |
|---|---|---|
| 30범주 ID 체계 자체 | 새 분류 스키마는 기존 정본·필드와 이중 체계를 만든다 | 이 표의 ID 범위는 조회용 |
| 샷 지시서 YAML | `06`/`08` 템플릿·`project.json`·`11` 핸드오프가 이미 정본 | 기존 필드에 투영 |
| G1–G7 승인 게이트 | `12`·`21` 검사 순서·`asset_gate`가 더 엄격 | 해당 게이트 이름만 참고 |
| 고정 프레임·초 수치 | 검증된 권장치가 아니다 | 예시 라벨·계산 근거·미검증 표시를 붙여 후보로만 |
| 반복되는 "과용 주의" 문장 | 정본의 실패 조건 열이 이미 소유 | 각 정본의 실패 조건 열 |

## 적용

1. 요청이 문서 용어로 들어오면 이 표에서 정본을 찾고 그 문서의 절차·필드로 인계한다.
2. 이 표에 없는 새 용어는 정본 소유자에게 먼저 넣을지 판단한다. 여기에만 정의를 추가하지 않는다.
3. 표의 링크가 실제 앵커로 해석되는지는 `scripts/test_crosswalk_navigation.py`가 검사한다.
