# 캐릭터 SSOT 템플릿

전체 형식 규격은 [`designing-video-character-sheets/references/character-ssot-master-prompt.md`](../../designing-video-character-sheets/references/character-ssot-master-prompt.md)를 따른다. 섹션 0–33은 그 순서·번호 그대로 유지하고, 적용 불가 섹션만 이유를 적어 `N/A`로 둔다.

## 작성 규칙

- 각 값의 근거를 구분한다: `supplied`(사용자 제공·확정) / `proposal`(디자인 제안) / `observed`(실제로 열어 확인한 소스에서 읽음 — 소스 에셋 ID·버전·실제 검사 범위를 함께 적는다) / `미정`(열린 미해결). 읽지 못한 공급 시트는 `unverified`로 남긴다.
- **명시적 창작 위임**(허구 인물 설계 위임)이 있으면 연령·성별·체형·과거사를 포함한 창작 속성을 주제에 맞게 `proposal`로 채운다 — 위임된 허구 SSOT의 빈 슬롯은 실패 출력이다.
- **실존 인물**은 문서화되지 않은 사실·심리·약력을 만들지 않는다. 미공급 사실은 `미정`으로 둔다.
- **이미 승인된 인물**의 공급된 선택은 보존하고 비어 있는 필드만 `proposal`로 채운다.
- **무관한 정확 수치**(이야기·디자인에 필요 없는 정밀 수치)는 누구에게도 만들지 않는다.
- 공급되지 않고 위임도 없는 항목은 비워 두거나 `미정`으로 남긴다. 필드가 있다는 이유로 값을 만들지 않는다 — 특히 연령·체형·성별·과거사·캐치프레이즈/개그. 그런 경우 구체성은 포즈·의상·재질·팔레트·소품으로 만든다.
- **페르소나 패킷 소비:** 신규·심화 시트는 [`designing-character-personas/SKILL.md`](../../designing-character-personas/SKILL.md)의 패킷 슬롯을 채워 넣는다 — `persona_core`/`behavior_rules` → §13–14·§20, `typology_lens` → §13 명시 슬롯, `expression_bridge` → §10–11, `voice_identity`/`speech_style`/`performance_cues` → §12. 이미 완전한 공급 시트는 재설계 없이 재사용하고 적용 범위만 기록한다.

# CHARACTER SSOT

## 0. SSOT Metadata
- character_id:
- sheet_version: (이 시트 자체의 버전; 위임 작업은 조정자가 할당한 artifact ID·버전을 그대로 쓴다)
- created_from: (시놉시스 artifact ID·버전 또는 단독 브리프)
- primary_use: general-image | video | story
- tier: full | lite | archetype
- visual_mode: photoreal | stylized-real | 2d | 3d | stop-motion | illustration | hybrid

## 1. Character Summary
-

## 2. One-Line Character DNA
- `[인물 유형]이지만 [반전되는 특성]을 가진 인물로, [시각적 특징]과 [행동적 특징] 때문에 한번 보면 쉽게 잊히지 않는다`

## 3. Core Identity
- 이름 / 영문명 / 별칭:
- 성별:
- 실제 연령 / 보이는 연령:
- 생일: (관련 있을 때만)
- 국적·문화 / 출생지·거주지 / 사용 언어:
- 직업 / 사회적 위치 / 세계 내 역할:
- 아키타입: 이야기 역할 / 첫인상 vs 실제 성격 / 욕망·두려움·결핍·약점·숨은 강점·모순 / 키워드 3–5개

## 4. Visual Identity Lock (신체)
- 키 또는 상대 스케일:
- 체형 카테고리: (불필요한 정밀 수치 없이)
- 어깨 / 몸통 / 허리 / 골반 / 팔다리 비율:
- 손 / 발:
- 기본 자세·걸음걸이:

## 5. Face Identity Lock
- 얼굴형·세로/가로 비: 이마 / 광대 / 볼 / 턱 / 턱끝
- 눈: 크기 / 형태 / 기울기 / 간격 / 눈꺼풀 / 동공 / 홍채 / 시선 / 속눈썹 / 눈밑
- 눈썹: 형태 / 굵기 / 각도 / 색
- 코: 콧대 / 길이 / 끝 / 콧날개 / 옆모습
- 입: 크기 / 윗입술 / 아랫입술 / 입꼬리 / 쉬는 표정 / 치아
- 귀:
- 피부: 톤 / 언더톤 / 결 / 주근깨 / 점 / 흉터 / 특징 표지

## 6. Hair Identity Lock
- 스타일 / 길이 / 가르마 / 앞머리 / 옆·뒷라인 / 밀도 / 굵기 / 컬 / 기본색 vs 빛 반사색 / 실루엣
- 필수 앵커:

## 7. Identity Anchors (3–7개)
| Feature | Description | Lock Level (IMMUTABLE/STABLE/VARIABLE) |
|---|---|---|
| | | |

## 8. Color Identity
- primary / secondary / accent / 피부 / 머리 / 눈 / 의상 — 이름·역할·(유용할 때 HEX)

## 9. Costume DNA
- 패션 장르 / 실루엣 / 재질 / 색 / 피하는 색 / 액세서리 / 신발 / 가방 / 장신구 / 안경
- 시그니처 의상: 상의 / 하의 / 겉옷 / 신발 / 액세서리 / 재질 / 색 / 착용 상태 / 핏 / 새 정도
- 의상 변경은 고정 정체성을 덮지 않는다.

## 10. Expression DNA
- neutral / gentle smile / genuine laugh / sad / angry / irritated / surprised / afraid / confident / embarrassed / concentrating / exhausted — 각각 눈·눈썹·입·턱·근육·고개 각도로 정의
- 페르소나 표현 연결(expression bridge): 각 핵심 행동 규칙이 어떤 표정·자세·제스처로 보이는지. 유형명에서 얼굴·체형·음색을 유도하지 않는다.
## 11. Body Language
- 기본 자세 / 서기 / 앉기 / 긴장 / 자신감 / 분노 / 거짓말 / 웃기 / 시선 / 걸음 / 달리기 / 습관 동작 / 무의식 동작 / 퍼스널 스페이스
- 관계·압박 상태 변주는 명명된 상태로 기록 — 새 정체성이 아니다.

## 12. Voice Identity · Speech Style · Performance
- **고정 음성(Voice Identity):** 기본 음역 / 음색·거칠기·숨 섞임 / 공명 인상 / 발음·문장 끝 습관 / 기본 리듬 / 볼륨 / **청각 앵커**(식별 서명) / **허용 변화 범위**(압박이 구부릴 수 있는 것 vs 유지할 것). 음색은 유형에서 자동 유도 금지; 근거 없는 Hz·수치 금지.
- **말투(Speech Style):** 문장 길이 / 어휘 / 질문·명령·완곡 / 존댓말·관계별 레지스터 / 유머 / 침묵 사용 / 억양 / 반복 구 / 금지 구
- **대사별 연기(Performance):** 실제 대사마다 의도·서브텍스트·감정 압력·강조 단어·멈춤·숨·속도 변화. 압박 상태는 새 보이스가 아니다 — 유지할 음색·발음 앵커를 명시.
- **재사용 지시:** `voice_identity_direction`(모든 발화에 그대로 재사용할 고정 정체성 한 줄)과 대사별 `performance_cue`를 분리.
- **실제 구현 참조:** 선택한 보이스 ID·타입·모델·설정·청취 검수는 [`../references/22-dialogue-lipsync.md`](../references/22-dialogue-lipsync.md)의 보이스 선택 기록에서 관리. 이 프로필은 파생물로서 정확한 `character_sheet` artifact ID·버전을 가리키고, `proposed`/`unresolved` 상태를 선택됨으로 기록하지 않는다.
- 샘플 대사(최대 3, 적절할 때만):
- 무언 역할이면 `N/A`와 이유 — 내레이터로 바꾸거나 오디오 파일을 주장하지 않는다.

## 13. Personality (5–7개)
- 각 특성: `특성 → 관찰 가능한 행동 → 강점 → 문제 되는 상황`
- 유형 렌즈(해당 시, 명시 슬롯): `mode: none|mbti|enneagram|both` / 공급 또는 제안 유형(그대로 보존) / 캐릭터별 축·동기 해석 / `design_rationale` / `limits` / 기록된 예외 — 유형 전형표·검사 점수 주장 금지. 공급 행동과 유형 해석이 어긋나면 승인 행동을 보존하고 간극을 기록.

## 14. Psychology
- 욕망 / 필요 / 두려움 / 수치 / 후회 / 자부심 / 비밀 / 스스로 인정 못하는 사실 / 스트레스·사랑·분노·실패·성공 반응
- 이야기 근거가 있는 경우 충돌하는 가치·책임, 우선순위·넘지 않는 선, 압박/위험/특정 관계가 그 판단을 바꾸는 조건
- 각 핵심 성향: `근거/성향 → 촉발 상황·이해관계 → 해석 → 의도 → 관찰 가능한 행동·대사 → 선택/비용 → 예외 조건` (페르소나 패킷 `behavior_rules` 소비).
- 판단 검산 1회: `상황·이해관계 → 생각 → 감정 → 관찰 가능한 반응·대사 → 선택`이 등록된 성격·관계·한계와 맞는지 확인. 검산은 이야기에 없는 선택이나 장면을 정본으로 추가하지 않는다.

## 15. Backstory
- 인과적으로 필요한 것만: 유년기 / 가족 / 전환점 사건 / 교육 / 관계 / 성공·실패·상실 / 현재 역할. 무의미한 연대기 없이.

## 16. Relationships
- 낯선 사람 / 친구 / 가족 / 연인 / 상사 / 부하 / 라이벌 / 적 / 아이 / 동물 — 해당 없는 유형은 이유와 함께 N/A

## 17. Likes & Dislikes (각 5–10개, 구체적)
- 좋아함:
- 싫어함:

## 18. Habits & Micro Details (≥10개, 의미 있는 미세 디테일)

## 19. Skills & Limitations
- good / average / poor / learning / impossible

## 20. Character Contradictions (전체 위임 허구 설계 시 ≥3개)

## 21. Silhouette Specification
- 머리 / 어깨선 / 비율 / 자세 / 의상 형태 / 액세서리 형태 — 식별성을 높이되 무작위 장식 없이

## 22. Turnaround Specification
- 정면 / 3·4 전면 / 측면 / 3·4 후면 / 후면 — 각 뷰가 보존할 것: 얼굴 기하·코 돌출·턱·두개골·머리 볼륨·어깨·신체선·의상 길이·액세서리 위치

## 23. Proportion Reference
- 머리 대 전신 비 / 어깨·다리·팔·손·발 관계. 스타일라이즈드 모드면 일관된 카툰 비율 사용.

## 24. Variable States
- 의상 / 스타일링 / 메이크업 / 표정 / 부상 / 계절 / 날씨 / 소품 / 연령 / 직업 / 감정 — 각 항목은 무엇을 바꿀 수 있고 무엇은 건드리면 안 되는지 명시. 불변 앵커는 덮지 않는다.
- 발화 역할: 상태별로 바뀌어도 되는 연기 매개변수(속도·압력·온기·멈춤)와 유지할 청각 앵커를 명시 — 압박은 상태이지 새 보이스가 아니다.

## 25. DO NOT CHANGE (5–15개, 디자인 특정 항목)
- 발화 역할: 청각 앵커·발음/문장 끝 습관 등 고정 음성 정체성도 여기 포함.

## 26. Anti-Drift Rules
- 얼굴 기하·눈 크기/간격·홍채·신체·연령·문화 디자인·기본 색·비대칭·표지 보존. 조명은 새 머리색이 아니고, 뷰티 필터는 새 정체성이 아니다.
- 음성 anti-drift: §12 청각 앵커·발음 습관·기본 리듬은 장면·감정 상태를 가로질러 유지 — 감정 태그가 음색·억양을 바꾸는 면허가 아니다.

## 27. Reference Character Sheet Prompts
- **Sheet A — Identity Sheet**: 실제 필수 이미지(이미지 기반 전체 패키지에서 인물당 1장). 한 장의 중립 스튜디오 이미지에 전신 정면·3/4 전면·측면·후면 + 얼굴 정면·3/4·측면(총 7뷰). 동일 인물·중립 표정·부드러운 중립 조명·명확한 비율. 장면·동작·배경 서사 없음. 글래머 초상은 대체 불가.
- **Sheet B — Expressions (프롬프트 스펙)**: 동일 인물 표정 9종 — neutral/smile/laugh/anger/sadness/fear/surprise/confidence/embarrassment.
- **Sheet C — Costumes (프롬프트 스펙)**: signature/casual/formal/work/seasonal — 신체·얼굴 불변.
- **Sheet D — Action/Poses (프롬프트 스펙)**: 성격이 드러나는 행동 6–10종.
- B/C/D는 스펙일 뿐이며 승인된 패키지 너머의 추가 생성·과금을 승인하지 않는다.

## 28. Image Generation Master Description (150–300단어)
- 연령·성별·문화 시각 디자인·얼굴·눈·코·입술·피부·머리·신체·앵커·의상·분위기. 장면·동작·배경·카메라 없이.

## 29. Character Identity Prefix (60–120단어)
- 불변+안정 특성을 담아 이미지/영상 프롬프트에 그대로 재사용. 모델 정체성 보장을 주장하지 않는다.

## 30. Negative Identity Prompt
- 이 인물이 망가지는 구체적 방식의 드리프트 제외 목록(일반 네거티브가 아님).

## 31. Story Function
- 시놉시스가 필요로 하는 만큼만: 목적 / 관객 정서 / 도입 상태 / 중반 / 핵심 선택 / 변화 / 최종 상태. 공급된 스파인은 보존.

## 32. Appeal Evaluation
| Criterion | Score (0–10) | Reason |
|---|---|---|
| visual distinctiveness | | |
| memorability | | |
| emotional appeal | | |
| personality depth | | |
| story potential | | |
| silhouette recognition | | |
| production consistency | | |
| originality | | |

- 점수 비교 전에 신원·해부·승인 설정·필요 뷰의 필수 조건을 검사한다. 다른 얼굴/설정 위반은 평균 점수로 상쇄하지 않는다. 실제 이미지가 없으면 실제 신원/아트 검수는 unverified다.
- 7 미만 영역은 수정한다. 점수를 부풀리지 않고, 자체 평가를 아트 QA나 사용자 수락으로 표현하지 않는다. 범위 밖 기준은 N/A로 정직하게 표시.

## 33. Final Character Lock Summary
- ABSOLUTE IDENTITY (불변): (발화 역할 — 음색 앵커·발음 습관 포함)
- STABLE IDENTITY (선언된 가변 상태로만 변경): (발화 역할 — §24 선언된 연기 범위)
- VARIABLE (범위 내 자유): (발화 역할 — 대사별 performance_cue)

## 캐스트 구별 (2명 이상)
- CAST DIFFERENTIATION MATRIX: `Character | Face | Silhouette | Color | Personality | Decision/Behavior | Voice | Key Anchor` — 목표·판단·관계·말투·음성 앵커의 실제 겹침을 확인. 유형명만 바꾸거나 얼굴만 바꾼 구별은 구별이 아니다.

## 정본 레코드 매핑 (이미지 기반 전체 패키지)

조정자가 `project.json`에 기록하고, 이 스킬은 버전 패킷으로 반환한다:

| 정본 필드 | 내용 |
|---|---|
| `characters[].persona` | `{role, personality, observable_behavior, speech}` — 모두 비어 있지 않은 문자열; 무언 역할의 speech는 이유가 적힌 `N/A` |
| `artifacts[]`의 `type=voice_profile` | §12 음성 설계에서 파생된 인계 artifact. `dependencies`와 `dependency_versions`로 정확한 `character_sheet` ID·버전을 고정하고 발화의 `voice_artifact_id`로 참조한다. `characters[]`에 새 필드를 만들지 않는다. 실제 voice ID·모델·설정·권리·청취 결과는 별도 선택 기록이며 `proposed`/`unresolved` 설계를 선택됨으로 기록하지 않는다. |
| `characters[].ssot_artifact_id` | `type=character_sheet` artifact — 실제 SSOT Markdown 에셋을 연결하고 시놉시스 artifact·버전에 의존 |
| `characters[].identity_sheet_asset_id` | 이미지 기반 전용 — `kind=character_identity_sheet`, `entity_type=character`, `entity_id`=character_id; 실제 Sheet A 이미지 |
| `preproduction` | `{mode: text|image_backed, synopsis_artifact_id, storyboard_artifact_id, storyboard_sheet_artifact_ids, storyboard_split_asset_id}` — 합본 시트는 정렬된 artifact ID 배열(시트당 최대 8패널; 한 장도 배열), split pointer는 실제 장면·패널 추출 manifest asset |

## 생성 메타데이터 (실제 확인분만)
- provider:
- model:
- workflow:
- 승인 에셋 ID:

## 참조 팩 메모
- 필요 뷰·표정·소품 상호작용은 섹션 22·27과 샷 필요로 조정한다.
- 프롬프트는 생성된 시트가 아니다. 공급자 성공은 정체성 QA가 아니다 — 반환된 시트 이미지를 실제로 열어 선언 앵커와 비교한다.

시트/입력 뷰 인계가 있으면 [실무 인계 R2](../references/29-reference-driven-production.md#sheet-inputs)에 따라 아래를 채운다. 기존 섹션 22/24/27과 실제 에셋 ID/버전을 참조하는 보조 표이며 별도 정본/새 JSON 필드가 아니다. 전체 패키지 Sheet A 7뷰는 유지한다.

| 뷰·원본/시트 asset ID·버전 | 부모 신원/의상·현재 상태 | 답할 수 있는 질문 / 답할 수 없는 질문 | 인물 기준 비대칭 앵커·바닥선/축척 | 실제 검사 범위·다음 입력에서 사용/제외 |
|---|---|---|---|---|

- 개별 원본과 통합 시트 연결 / 잘림·얼굴 삭제·미관측 후면 제안:
- 후보 비교 조건·단일 비교 축·필수 조건 실패·선호 선택 이유:
- 공유본이 요청된 경우에만: {원본과 분리한 삭제본·작은 얼굴/썸네일/첨부 확인; 신원 생성용 아님}
