# 조합 규칙 — 적합성 검사와 콘셉트→연출 규칙 변환

원본 데이터는 [concept-rules.yaml](concept-rules.yaml)이다. 이 문서는 그 요약이며 YAML이 우선한다.

## 1. 적합성 검사(Compatibility)

- `when`의 모든 조건이 참이면 발동한다. 값이 목록이면 그중 하나만 맞아도 된다.
- `error`는 진행을 막는다. `override: true`인 규칙만 사용자가 '의도적 혼합'으로 표시해 통과시킬 수 있다(선택 패킷의 `overrides`에 규칙 ID 기록).
- `warn`은 진행하되 기획안 '제작 전 확인할 사항'에 남긴다. `info`는 참고만.
- C100(코드 규칙): 대사 없음 제약인데 사운드 축이 대사/내레이션 중심이면 error, override 불가.

| ID | 심각도 | override | 조건 | 메시지 | 해결 |
|---|---|---|---|---|---|
| C001 | error | 가능 | production_method ∈ ['stickman_method'] AND direction.texture ∈ ['photoreal'] | 스틱맨 제작 방식과 포토리얼 질감은 충돌합니다. | 질감을 레트로/필름룩으로 바꾸거나 제작 방식을 실사로 바꾸세요. |
| C002 | warn | 가능 | production_method ∈ ['two_d_anim', 'three_d_anim', 'stop_motion_method', 'motion_comic_method'] AND direction.reality ∈ ['hyperrealism'] | 애니메이션 계열 제작 방식에 극사실주의는 결과 편차가 큽니다. |  |
| C003 | error | 불가 | direction.viewpoint ∈ ['cctv'] AND direction.camera ∈ ['fast_camera', 'handheld'] | CCTV 시점은 고정 화각이 전제라 빠른 카메라 워크/핸드헬드와 함께 쓸 수 없습니다. | 카메라를 고정 카메라로 바꾸세요. |
| C004 | warn | 가능 | direction.viewpoint ∈ ['pov'] AND direction.camera ∈ ['locked_off'] | 1인칭 POV에 고정 카메라는 체감이 약합니다. 핸드헬드를 권장합니다. |  |
| C005 | error | 가능 | direction.color_light ∈ ['black_white'] AND visual_aesthetic ∈ ['cyber_neon'] | 흑백 조명과 사이버 네온 미학은 충돌합니다. |  |
| C006 | error | 불가 | format ∈ ['interview', 'talk_show', 'podcast_video', 'street_interview', 'debate', 'counseling', 'lecture'] AND direction.sound ∈ ['silent'] | 말이 핵심인 형식에 무성 사운드는 성립하지 않습니다. | 사운드를 대사/내레이션 중심으로 바꾸거나 형식을 바꾸세요. |
| C007 | warn | 가능 | format ∈ ['short_doc', 'human_doc', 'observational_doc', 'nature_doc', 'history_doc', 'crime_doc'] AND world ∈ ['magic', 'high_fantasy', 'isekai', 'isekai_base', 'xianxia_world', 'murim_world', 'system'] | 다큐멘터리 형식에 판타지 세계관이 들어갔습니다. 페이크 다큐/모큐멘터리로 바꾸는 것을 권합니다. |  |
| C008 | warn | 가능 | duration ∈ ['s15'] AND narrative ∈ ['parallel', 'time_loop_structure'] | 15초에 평행 서사/타임루프는 정보량이 과합니다. 30초 이상을 권합니다. |  |
| C009 | warn | 가능 | duration ∈ ['s15', 's30'] AND format ∈ ['miniseries', 'omnibus', 'short_film', 'web_drama'] | 선택한 형식은 보통 30초보다 깁니다. 회차 분할(시리즈) 또는 길이 확대를 고려하세요. |  |
| C010 | warn | 가능 | direction.sound ∈ ['asmr_sound'] AND direction.edit_rhythm ∈ ['hyper_montage'] | ASMR 사운드와 초고속 몽타주는 리듬이 상충합니다. |  |
| C011 | info | 가능 | genre ∈ ['horror'] AND emotion_arc ∈ ['laughter'] | 공포+웃음 조합(호러 코미디)은 의도적 장르 혼합으로 기록됩니다. |  |
| C012 | warn | 가능 | era ∈ ['joseon', 'three_kingdoms_kr', 'ancient_china', 'medieval_europe'] AND world ∈ ['cyberpunk_world', 'system', 'game_fantasy'] | 역사 시대에 고기술/게임 세계관 — 의도적 시대착오(퓨전)라면 override로 표시하세요. |  |
| C013 | warn | 가능 | direction.camera ∈ ['one_take', 'long_take'] AND production_method ∈ ['live_action_ai'] | AI 실사 생성에서 원테이크/롱테이크는 클립 길이 제한 때문에 이어붙이기 설계가 필요합니다(비용·난이도 상승). |  |
| C014 | warn | 가능 | direction.sound ∈ ['silent'] AND format ∈ ['music_video', 'lyric_video', 'dance_film'] | 음악 형식에 무성 사운드가 선택되었습니다. |  |
| C015 | info | 가능 | culture_style ∈ ['kr_makjang', 'telenovela', 'turkish_melo'] AND emotion_arc ∈ ['laughter'] | 격정 멜로 스타일에 웃음 목표 — 패러디 톤으로 해석합니다. |  |
| C016 | warn | 가능 | direction.edit_rhythm ∈ ['long_take_based'] AND duration ∈ ['s15'] | 15초에 롱테이크 중심 편집은 컷 1~2개뿐이라 후킹이 약할 수 있습니다. |  |

## 2. 콘셉트 → 연출 규칙 변환(Direction Rules)

선택이 팩의 `when`과 맞으면 그 팩의 규칙이 합쳐진다. 목록 값은 합집합, 단일 값은 먼저 적용된 팩이 이긴다. `forbidden_props`는 이후 프롬프트·컷 묘사 검수(CQ10)에 그대로 쓰인다.

| 팩 | 조건 | 규칙 키 |
|---|---|---|
| D_kr_melo_1990s | era ∈ ['y1990s'] | props_wardrobe, forbidden_props, acting_dialogue, color_texture, music_sfx, emotion_intensity, camera_edit, conflict_pattern |
| D_joseon | era ∈ ['joseon'] | props_wardrobe, forbidden_props, acting_dialogue, color_texture, music_sfx, emotion_intensity, camera_edit, conflict_pattern |
| D_y2k | era ∈ ['y2k'] | props_wardrobe, forbidden_props, color_texture, music_sfx, camera_edit |
| D_near_future | era ∈ ['near_future'] | props_wardrobe, color_texture, music_sfx |
| D_k_drama | culture_style ∈ ['k_drama'] | acting_dialogue, camera_edit, conflict_pattern, emotion_intensity |
| D_kr_makjang | culture_style ∈ ['kr_makjang'] | acting_dialogue, camera_edit, music_sfx, conflict_pattern, emotion_intensity |
| D_jp_pure | culture_style ∈ ['jp_pure_romance'] | acting_dialogue, color_texture, camera_edit, emotion_intensity |
| D_nordic_noir | culture_style ∈ ['nordic_noir'] | color_texture, music_sfx, camera_edit, conflict_pattern |
| D_cn_xianxia | culture_style ∈ ['cn_xianxia'] | props_wardrobe, color_texture, music_sfx, camera_edit |
| D_us_sitcom | culture_style ∈ ['us_sitcom'] | acting_dialogue, camera_edit, music_sfx |
| D_stickman | production_method ∈ ['stickman_method'] | props_wardrobe, acting_dialogue, camera_edit, music_sfx |
| D_live_animatic | production_method ∈ ['live_animatic_method'] | camera_edit, music_sfx |
| D_comedy | genre ∈ ['comedy'] | camera_edit, music_sfx |
| D_horror | genre ∈ ['horror'] | color_texture, camera_edit, music_sfx |

### 예시: 1990년대 한국 멜로 (`D_kr_melo_1990s`)

- **props_wardrobe**: 삐삐·공중전화·카세트 워크맨·필름 카메라; 통 넓은 청바지, 니트 조끼, 헤어밴드; 브라운관 TV, 다이얼 전화
- **forbidden_props**: 스마트폰; 무선 이어폰; LED 간판; QR코드
- **acting_dialogue**: 존댓말·반말 전환이 감정의 신호; 직설적 고백보다 머뭇거림
- **color_texture**: 따뜻한 황색 톤, 약한 할레이션; 필름 그레인, 가벼운 VHS 노이즈
- **music_sfx**: 어쿠스틱 발라드/피아노 테마; 삐삐 수신음, 동전 떨어지는 소리, 빗소리
- **emotion_intensity**: 중상 — 눈물은 참는 쪽
- **camera_edit**: 줌 인/아웃을 감정 강조에 사용; 디졸브 전환, 느린 컷
- **conflict_pattern**: 엇갈림(연락이 닿지 않음); 말하지 못한 진심

## 3. 평가 기준

| 기준 | 가중치 | 의미 |
|---|---|---|
| hook | 0.25 | 첫 1~3초에 질문을 만드는 힘(서사 구조의 hook_weight 반영) |
| feasibility | 0.20 | AI 제작 난이도(제작 방식·카메라의 ai_difficulty, 길이 대비 컷 수) |
| emotion | 0.15 | 감정 곡선의 선명도 |
| originality | 0.15 | 조합의 신선함(흔한 조합은 감점, 의도적 혼합은 가점) |
| coherence | 0.15 | 속성 간 충돌 없음(적합성 경고 수 반영) |
| platform_fit | 0.10 | 숏폼(9:16, 60초 이하) 적합성 |

등급은 10/30/50/70/90. 합계 65 이상이고 차단 오류가 없으면 `go`, 50 이상 `revise`, 그 밖은 `rework`.
