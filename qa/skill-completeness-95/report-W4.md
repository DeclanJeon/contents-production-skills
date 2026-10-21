# W4 — 제작 모듈·정본 자료 감사 인계

상태: **review 요청**. 01–28 및 7개 나머지 참조를 읽고 지원 경계를 기록했다. 이는 모든 craft 주장의 원문 결속 완료나 행동 평가 PASS가 아니다. 점수는 부여하지 않는다. 구현 wave 중 테스트/빌드/linter/formatter·fresh model 실행은 하지 않았다.

## 변경 파일과 실제 결함

27개 skill/reference 파일을 수정하고 이 보고서와 `claims-W4.tsv`를 새로 작성했다. metadata/version/manifest/README/CHANGELOG·통합 원장·타 소유자 파일은 수정하지 않았다. 사용자 변경 reset/revert/commit 없음.

- `video-production-assets/SKILL.md`: 근거 답변의 주장별 정확 파일/절·class·실제 구간·분리 문장 인용 계약. 원문 미확인을 authored-design으로 재라벨링하지 않음.
- `references/sources.md`: 기존 역사 탐색 기록과 W4 직접 읽기를 분리. 정확 rendition/path/hash/bytes/구간·지원 한계, 28모듈+나머지 참조 지원 경계, 타 소유자 요청 판본, 공식 provider 문서 범위를 추가. 원문은 복제하지 않음. 사용 가능한 원문을 먼저 탐색하고 정말 없는 구간만 요청하도록 기존 “다시 제공” 문구 교정.
- `references/01-brief.md`, `02-story.md`, `03-screenplay.md`, `04-performance.md`, `05-visual.md`, `06-shots.md`, `07-lighting.md`, `08-animation.md`, `09-edit.md`, `10-evidence.md`, `13-ideation-brand.md`: 기존 근거 절 안에 직접 지원되는 주장과 운영 설계/미결속 craft 범위를 추가. 기존 Acceptance를 복사하지 않음.
- `references/12-qa.md`: 검사 순서·severity·KEEP/REBUILD/DROP·수정 라우팅·회고가 직접 book QA 규격이라는 오독을 막는 정확 분리 문장. 실제 적용 craft는 원 소유자 출처를 별도로 요구.
- `references/16-concept-emotion-retention.md`: S1a용으로 책의 지원 범위를 목표/인과·평가·서술 맥락에 한정하고 엔진/구체 배열/유지 지도는 제작 제안으로 분리. “혼합 상태는 단일 감정보다 오래 남는 경우가 많다”는 읽은 근거 없는 비교 효과를 주장하지 않도록 교정하되 혼합 감정 설계 기능은 유지. 유지율을 설계 문구로 정의하던 단정을 가설로 교정. 10–30초는 연구 수치가 아닌 작업용 감사 간격. S1b의 주장별 locator/class/BASIS·새 브리프의 제안 시간/행동 표기 계약.
- `references/17-genre-comedy.md`, `18-episodic-series.md`, `19-brand-product-integration.md`, `20-visual-mode-ssot.md`, `21-generated-video-qa-retry.md`, `22-dialogue-lipsync.md`, `23-finishing-platform.md`, `24-production-execution.md`, `25-reference-video-analysis.md`, `27-camera-motion-qa.md`, `28-film-production-lifecycle.md`: 파일별 운영 설계와 미결속 외부 craft/현재 provider 근거를 구별. 근거 헤딩을 추가했다고 source support가 생긴 것으로 취급하지 않음.
- `19-brand-product-integration.md §1 step9`: 제품을 제거하면 장면이 붕괴한다는 사실만으로 과의존이라고 단정하던 오류를 양방향 진단 질문으로 교정. 플롯 장치/통합 계획 기능은 보존.
- `23-finishing-platform.md §그레이드 노드 구조와 버전 step2`: Shot Match 노드가 비었다는 사실을 매칭 실패의 증거로 쓰던 오류를 실제 인접 샷 비교로 교정. editable 노드 구조는 보존.
- `references/storyboard-sheet-user-guide.md §빠르게 점검할 항목`: Codex Imagen 예외와 충돌하는 전체 이미지 비용 상한 확인 문구를 실행자별 기존 비용 정책과 일치시킴. 새 비용/생성 권한을 추가하지 않음.

의도적으로 유지한 참조: `11-ai-handoff.md`, `14-production-ops.md`, `15-delivery.md`, `26-state-causality-continuity.md`는 기존 설계 확장/운영 근거 구분이 있어 중복 헤딩을 추가하지 않음. `contract.md`, `preproduction-review.md`, `storyboard-contract.md`, `workspace-integration.md`, `rofan-craft-examples.md`는 직접 읽고 정본 source map/claims에서 범위를 기록했다. 이들 전체 코드 구현/미디어 의미를 검증한 것이 아니다.

## 직접 읽은 원문과 실제 지원

정확 full path·SHA-256·bytes는 `claims-W4.tsv`의 W4-S01–S22 및 정본 `references/sources.md §직접 대조 구간 — 2026-10-16 W4`에 있다. 모든 book 인용은 READ-PARTIAL이다. 도판/페이지 이미지는 검사하지 않았다.

| 읽기 ID | 자료/직접 구간 | 실제 지원 / 제한 |
|---|---|---|
| W4-READ-02 | Alton L187 PRISON SCENES | 막대 그림자 감금 단서만. 기존 L41/47/51은 소개/제작 일화여서 일반 조명 원리 전체 근거 아님. |
| W4-READ-04 | Lumet L37 p18 | 제약·부서 협업·주제 선택·임의 이동에 대한 이견. 일정/원장/승인 규격은 저자의 직접 모델 아님. |
| W4-READ-05 | Katz L75, L333–355, L595–597 | L75는 모델 소개. 실제 축/재정위는 L333–355, 앵글 맥락은 L595–597. 도판/전체 커버리지/키패널 체계 미검증. |
| W4-READ-08a/b | Block originals rendition L31–33, L51–53, L103–117, L161–173, L529–537 | 7요소·대비/유사성·상대 운동·줌/돌리·matched framing의 거리. 기존 L121은 대기 확산 예. exact solve나 모든 회전의 균일 pixel velocity는 입증하지 않음. |
| W4-READ-10a/b | Murch L21, L27, L31–33 | L31–33이 Rule of Six의 정확 위치. 개인적 선호이며 가중 자동점수 아님. L27은 트랙 수≠믹스 품질. |
| W4-READ-13 | Hooks L73, L99–103 | 알고 반응하는 순서·action/objective/obstacle의 연극적 관점. 일반 심리학 실증/모든 장르 강제 갈등 아님. |
| W4-READ-16 | Williams L95–99 pp36–38 | 사건 시점/위치 간격·같은 시간의 다른 spacing. 도판/보편 gait 프레임/AI 제어 보장 아님. |
| W4-READ-20a | McKee production rendition L77 p38 | 장면의 전후 가치 변화. |
| W4-READ-20b | McKee synopsis rendition L1730–1758 | classical causality와 antiplot coincidence 대조. 별도 hash/bytes를 보존. |
| W4-READ-24 | Habermas L351–359 pp160–164 | 서술 정서/관점/수용 맥락·음성/텍스트 불일치 연구와 제한. 기억/유지율/개별 보이스 효과 보장 아님. |
| W4-READ-30 | Lo Duca L375–376 p162 | 사람/사물/장소 주체·원하는 결과·대립자/비교자. 차트/인과성 일반 검증 아님. |
| W4-READ-37 | Young L33 | 구체/일반 자료 수집·조합. 후반 숙성/최종 검토는 이 구간만으로 직접 읽기 인정 안 함. |
| W4-READ-38 | Aaker L73–77 pp25–27 | 브랜드 비전/현재 이미지·core/extended·맥락. 스폰서 통합 효과 아님. |
| W4-READ-39 | Simonson/Rosen L29–33 | 외부 정보·비교와 통제 실험 일반화 한계. 사례 수치/현 기술 상태는 미채택. |
| W4-READ-40 | Goodman L83–89 pp26–29 | 기대 관리·실제 서비스 용량/경험 사례. 전체 여정/성과 배수 검증 아님. |
| W4-READ-41 | Hogan L2404–2406 | 전형적 행위자·목표·인과 맥락. 모든 서사의 보편 필수/기억 우위 아님. |
| W4-READ-42 | Lazarus L2342–2346, L3841–3845, L4319–4323 | 목표 관련성·대처·책임·슬픔/희망 맥락. 표정 확정 진단/시청자 유지 효과 아님. |
| W4-READ-43 | Dunford alternate L983–1038 | 고객의 실제 대안·비교 기준·상대 차별화. 기존 canonical 43 판본의 hash/locator는 보존. |
| W4-READ-45 | Hu L636–661 pp59–61 | staging·screen direction·180축 혼란. L650 좌우 문장은 예시와 불일치하여 미채택. |
| W4-READ-08c | Block top-level Korean-named rendition L275–283 pp137–141 | 대비의 선/윤곽 가시성만. originals와 지문은 같지만 읽은 경로는 별도 기록. |

추가 확인: Malkiewicz original rendition은 406 bytes, SHA-256 `835784c5cdd93b4fb7d9b6f60014924c27f3e44a3a7118c02ab77c07cb7d13ec`. 직접 열린 구간도 공백이며 기존 제외 상태를 유지했다. 이 파일을 모든 조명 기능의 blocker로 만들지 않았다.

W1/W2/W3/W6의 요청은 보고서에서 경로를 찾은 후 위 원문을 W4가 직접 열고 지문을 계산해 결속했다. 동료 보고서를 읽은 것만으로 W4 직접 읽기로 승격하지 않았다. W3의 심리 유형/Voice Design 등 별도 원장 전체를 여기서 직접 읽거나 정본 인덱스에 통합한 것으로 주장하지 않는다.

### Provider 문서 읽기

- W4-WEB-v4: [Eleven v4](https://elevenlabs.io/docs/overview/capabilities/text-to-speech/eleven-v4), `Native accent handling`/`Model variants`: Style/Speed slider 없음·SSML 미지원·Stability/Similarity·교차 언어 동작.
- W4-WEB-prompt: [Best practices](https://elevenlabs.io/docs/overview/capabilities/text-to-speech/best-practices#prompting-eleven-v4), `IPA with Eleven v4`와 v4의 voice selection/audio tags/punctuation. 태그 순응 불완전·SFX 오해 가능·보이스/문구별 IPA 변동.
- W4-WEB-quota: [quota](https://elevenlabs.io/docs/help-center/account/general/do-i-use-quota-on-every-generation), 웹 TTS/Voice Changer 조건·2시간·동일 입력/모델/보이스·새로고침/이탈·API 제외, v3/Studio의 별도 조건.
- W4-WEB-voice: [TTS playground](https://elevenlabs.io/docs/eleven-creative/playground/text-to-speech#voices), Settings/Voices의 일반 권고. 일반 페이지와 v4 개별 문서의 accent/speed 적용 범위를 혼용하지 않음.

확인 기록: 2026-10-16 시작 wave, READ-PARTIAL, Markdown alternate 직접 읽기. 고정 local snapshot/hash/bytes 없음(`N/A-live-web`). 음성 생성·청취·계정/UI 잔여 자격 확인·API 실행은 없음.

## S1a 수동 적용 산출물 — 독립 평가가 아님

아래 표는 수정된 두 파일의 직접 읽은 문장에 대한 W4의 수동 대조다. frozen prompt를 fresh session에서 실행한 PASS가 아니며, 이 세션의 원문/다른 파일 문맥을 격리했다는 주장도 아니다.

| file | derived-from-books | own-design | which-sentence-told-you | unknown |
|---|---|---|---|---|
| `references/16-concept-emotion-retention.md` | §2의 목표/인과·평가·서술 맥락에 한정 | §1 엔진·§2의 구체 감정/앵커·§3 유지 지도/감사 주기 | “서적에서 직접 연결한 범위는 §2의 목표·인과를 통한 감정 맥락(Hogan, 자료 41), 사건의 목표 관련성·대처 선택지를 구분하는 평가 점검(Lazarus, 자료 42), 서술 관점·정서와 수용 맥락의 관계(Habermas, 자료 24)이며, §1 콘셉트 엔진·§2의 구체적 감정 배열/앵커·§3 유지 아키텍처/감사 주기는 이를 제작에 적용한 패키지의 설계 제안이다.” | 파일만 읽어 원문을 직접 읽었다고 할 수 없음. 기억 우위/실제 유지율은 입증되지 않음. |
| `references/12-qa.md` | 이 파일의 직접 book QA 규격 없음; 적용 craft는 원 소유 모듈에서 확인 | 검사/심각도/KEEP·REBUILD·DROP/라우팅/회고 | “이 파일의 검사 순서·blocker/major/minor 분류·KEEP/REBUILD/DROP·수정 라우팅·회고 형식은 패키지가 정한 운영 설계이며, 특정 서적에서 직접 도출한 QA 규격으로 인용하지 않는다.” | 실제 파일 검사/사용자 수락/각 적용 craft의 원문 근거는 이 문장으로 성립하지 않음. |

M-03의 추가 두 파일: `10-evidence.md §근거와 적용 범위`는 자료30의 주체/목표/비교 조건과 패키지 claim/ID/권리 운영을 구별한다. `17-genre-comedy.md §근거와 적용 범위`는 장르 패턴/삼단/콜백의 직접 source 구간이 없다고 명시한다. 후자는 새 heading이 있어도 해당 craft에 `[BASIS-UNSTATED]`가 필요하다.

## S1b 수동 적용 산출물 — 60초 감정/유지 설계만

W4-MANUAL-S1b. 입력: 지역 빵집 주인이 할머니 레시피를 판매하지 않고 지키는 순간. 아래 행동·서류/노트·구간은 **허구의 제작 제안**이며 고객/가족의 실제 이력·계약/손해/효능·이미지 관찰이 아니다. 스크립트/대사·이미지·프로젝트 파일·미디어 생성 없음. 초는 제안 구간, 측정치 아님.

| 제안 구간 | 의도 감정 → 관찰 가능한 제안 | 계속 볼 열린 질문 / 닫히는 정보 | 주장별 package locator / basis |
|---|---|---|---|
| 0–6s | 호기심 → 주인이 판매 제안서 옆의 닳은 레시피 노트에 손을 멈춘다 | 무엇을 팔지 못하고 있는가? 판매 선택이 있다는 맥락만 연다 | `16-concept-emotion-retention.md §2. 감정과 기억 설계`의 관찰 행동·앵커 + `§3. 시청 유지 설계`의 열린 질문: 파일이 적용 설계임을 명시. 행동/6초는 authored-design 제안. |
| 6–16s | 따뜻함 → 노트의 같은 동작을 따라 반죽을 접는다 | 이 노트가 왜 중요한가? 레시피를 계속 사용하는 관계를 행동으로 제시 | 같은 파일 `§2. 감정과 기억 설계`의 시점/목표·감각 앵커: 목표/맥락만 자료24/41/42의 좁은 source-derived, 이 행동/배치는 authored-design 제안. |
| 16–29s | 걱정 → 판매 서류와 노트 사이를 번갈아 보고 펜을 들었다 멈춘다 | 주인은 어느 선택을 하는가? 판매가 가능한 갈림길을 유지 | 같은 파일 `§감정 전환의 평가 점검`: 목표 관련성/대처 선택지는 자료42, READ-PARTIAL; 경제적 곤궁·손실액은 근거 없으므로 넣지 않음. 이 반응/시간은 authored-design 제안. |
| 29–42s | 결단 → 펜을 내려놓고 노트를 작업대 안쪽으로 되돌린다 | 판매하지 않기로 한 선택이 실제 행동으로 이어지는가? 선택 질문을 닫는다 | 같은 파일 `§2. 감정과 기억 설계`의 선택/전환과 `§유지 아키텍처`의 전환/보상: 행동/시간은 authored-design 제안, 관객 감정 확정/유지율 실증 아님. |
| 42–54s | 안도+아쉬움 → 서류는 옆에 두고 같은 노트로 다시 반죽한다 | 지킨 선택이 무엇을 계속하게 하는가? 레시피 보존을 일상 행동으로 회수 | 같은 파일 `§감정 구조 패턴`의 혼합 감정 + `§2. 감정과 기억 설계`의 모티프 재맥락화: 적용 설계 명시. 혼합 감정이 더 오래 기억된다는 효과는 `[BASIS-UNSTATED]`이며 권고 근거로 사용하지 않음. |
| 54–60s | 조용한 자부심/여운 → 노트가 작업대에 남고 만든 빵을 꺼낸다 | 레시피를 지킨 결과를 닫고 끝낸다; CTA는 추가하지 않음 | 같은 파일 `§유지 아키텍처`의 보상/선택 애프터비트, `§2. 감정과 기억 설계`의 결말 앵커: authored-design 제안. 보상/모티프의 일반 기억 효과를 실증한 출처로 말하지 않음. |

수동 대조 결과: 구간은 0→6→16→29→42→54→60으로 연속하며 제안 합계 60초다. 모든 행에 실제 파일/절과 basis 구분이 있다. 이는 원문 지원 범위/작성 형식의 적용 예이며 실제 모델 준수·관객 감정·유지율·음성/화면 품질은 검증하지 않았다. independent S1b replay는 부모 소유다.

## 01–28 모듈별 정상/경계 수동 적용과 검증 coverage

W4-N01–N28. 공통 합성 입력은 위 빵집 상황이며, 18/19/26/28은 해당 요청이 추가됐다는 명시적 변형이다. 표의 산출은 **수동으로 작성한 텍스트 계획 조각**이다. 완성된 28개 제작 패키지·모든 템플릿 필드·61개 formal model 평가를 실행했다고 집계하면 안 된다. 실제 이미지/영상/음성/파일 검사 항목은 전부 NOT RUN이다.

| ID/모듈 | 실제 작성한 정상 출력 조각 | 경계 처리 / 원문·실행 coverage |
|---|---|---|
| N01 brief | 관객=동네 빵집 방문자; 약속=레시피 보존 선택; 길이60s/세로; 영상 실행 제외 | 관객 사실·판매액 미제공은 미정. 자료04 제약만 직접 지원. |
| N02 story | 판매 가능성→노트와 작업의 의미→보존 결정→계속 굽는 결과 | 막/영웅 여정 강제 안 함. 자료20/41 부분 지원, 모티프 효과 별도. |
| N03 screenplay | 장면 목적=노트와 판매 선택의 갈림길을 가시화; 발화=N/A(요청 없음) | S1b를 대본으로 확장하지 않음. 장면 가치만 자료20; 대사 효과 미결속. |
| N04 performance | 행동 동사=멈춘다/비교한다/내려놓는다/되돌린다; 전술 변화=판매 검토→보존 | 배우에게 실제 가족 트라우마 공개 요구 없음. Hooks 목표/행동 직접 읽음; Weston 상세 미결속. |
| N05 visual | 노트가 손/서류와 분리돼 읽히게 명암·위치 대비 제안; 시작/끝 동일 노트 | 색=보편 감정 코드 단정 안 함. Block 정의/거리 지원, 실제 픽셀 미검사. |
| N06 shots | 노트/서류를 같이 읽는 구도→주인의 멈춤→노트 복귀가 읽히는 구도; cue 시간은 위 제안 | 확정 ID/렌즈/좌표를 발명하지 않음. 축은 Katz로 지원, production board/이미지는 미생성. |
| N07 lighting | 작업대의 기존 실용등을 주 광원 동기로 제안; 노트 글/손의 읽힘을 검사 항목으로 둠 | lux/CCT/기구값은 미정. Alton 그림자 예만 직접 지원, 실제 조명 pass 없음. |
| N08 animation | 노트로 손이 가는 같은 1초에 초반 큰 간격/끝 좁은 간격이라는 spacing 제안 | FPS/정밀 프레임 수는 입력 필요; timing/spacing은 Williams 지원. 발 접지/모션 미검사. |
| N09 edit | 최종 제안 구간=0–6/6–16/16–29/29–42/42–54/54–60; source in/out=미제공 | 측정 편집/원본 playback_rate로 쓰지 않음. 끝 화면/컨테이너 tail=실제 파일 없어 UNKNOWN. |
| N10 evidence | “할머니 레시피”는 supplied premise; 실제 고객/효능/판매액 claim은 추가하지 않음 | fiction과 fact 구별; 자료30 틀만 직접 지원. 가짜 후기/차트 없음. |
| N11 AI handoff | 노트/손/서류 시작·끝·보존 요구를 모델 중립으로 넘기되 current endpoint=UNKNOWN | prompt 준비≠생성. 참조·seed로 정체성 보장 없음. |
| N12 QA | 미검증=실제 감정 읽힘/시간 재생/음성; 수정=선택이 안 읽히면 행동/구도 대조 | 사용자 수락·quality pass 기록 없음. 파일 없는 미디어 검수는 unverified. |
| N13 ideation | 각도A=노트로 이어지는 손동작; 각도B=판매 선택의 멈춤; 두 후보는 제안, 미선택 | 수요/브랜드 사실 발명 없음. 수집/비전/기대의 좁은 구간 직접 지원. |
| N14 operations | 작업=텍스트 설계/정지 검토/영상 실행을 분리; 수량/단가/가용시간 미제공=미정 | 월 가능 여부/재시도율 수치 발명 없음. 운영 설계만, 생성/과금 없음. |
| N15 delivery | 목적지=세로 브랜드 영상이나 구체 플랫폼 미정; 자막/codec/audio spec=미정 | 임시 원고 시간을 최종 sync로 쓰지 않음. 납품 파일/권리/규격 통과 없음. |
| N16 emotion/retention | 위 6행의 감정·관찰 행동·열린 질문·제안60초 | 각 행 locator/basis 존재. 실제 유지율·기억 우위는 입증 안 함. |
| N17 genre/comedy | 코미디를 원하지 않는 빵집 brief에는 코미디 장치=N/A; 긴장은 판매/보존 선택에서 제안 | 장르/삼단/콜백을 책에서 검증됐다고 하지 않음. `[BASIS-UNSTATED]` 명시. |
| N18 series | 추가 회차 요청 변형: 상수=레시피 보존; 변수=다음 날 작업; 델타=판매 거절 결정 | 월 가용시간 없으므로 cadence=미결정. 반복 엔진 효과는 미결속. |
| N19 product | sponsor 추가 변형: 제공된 제품/필수문구/고지 없음→요구 입력; 레시피 노트는 일반 prop | 제품을 빼도/못 빼도 단독 실패 아님. 허구 제품 효능/실제 동의 생성 안 함. |
| N20 SSOT | 반복 인물1/노트1/작업대1의 불변 목록 제안; 실제 identity image 미제공 | 텍스트-only라 Sheet A 파일 생성 안 함. tier/view 규격은 authored, 품질 보장 아님. |
| N21 generated QA | 검사 계획=손/노트 접촉 구간·이후 노트 위치·선택 읽힘; 실제 결과=unverified | 영상 없이 접촉/자연스러움 pass 없음. contact3 경고는 측정 모델 한계 아님. |
| N22 dialogue | 발화 미요청→N/A; 향후 보이스 필요시 승인 원고/voice/발음/상한 필요 | 웹 문서 읽기는 실제 발음/한국어/청취 검증 아님. 오디오 생성 없음. |
| N23 finishing | Balance/Shot Match/Look은 작업 구조 제안; 실제 컷 없어 매칭/그레이드 결과 없음 | 빈 Shot Match 노드로 실패 단정 안 함. 플랫폼 알고리즘 효과 보장 없음. |
| N24 execution | 실행 범위=text-only; provider/model/job/result ID 없음; 비용/실행 승인 없음 | 기존 계정/무료/짧은 샘플도 실행 권한 아님. Codex 예외는 책/무료 보장 아님. |
| N25 analysis | 영상 미첨부→분석할 원본/구간 필요; 관찰행=없음; 계획 제안과 구분 | saved Rofan notes≠W4 playback. source 컷/음성/렌즈/권리 발명 없음. |
| N26 state | 노트를 작업대 안쪽으로 되돌리는 변형: 시작=서류 옆, 끝=안쪽, 이후 굽는 구간까지 유지 | 가림/컷이 reset 아님. 원인 구간/후속 실물 파일 없어 전이 QA=unverified. |
| N27 camera QA | 계획 대비 실제 clip/version·전체 재생·목표 cue/오차가 필요하다고 반환 | 실제 clip/허용오차 없음→measured difference도 없음, 임의 pass/점수 없음. |
| N28 lifecycle | 명시 전체 단편 변형: development=텍스트 초안, production/post/distribution=not produced | 단계 분류는 authored; 배급/권리/실제 승인 완료 없음. 단일 S1b 요청엔 적용 안 함. |

나머지 참조 coverage: contract(상태/의존/FINAL), preproduction-review(저장/수락/영상 게이트), storyboard-contract(§1–8 및 접촉/의미 검사), storyboard-sheet-user-guide(프롬프트/비용 예외), workspace-integration(명시 host 조건), sources(역사/직접 읽기), rofan(역사/선택 근거). 모두 직접 읽었다. 각 참조에 기재된 코드의 구현 전체·원 미디어·host capability는 검증하지 않았다.

## 실제 실행한 비테스트 smoke

세 CLI 호출은 모두 exit 0. 실제 프로그램을 실행해 help 출력만 관찰했다. validator 본체·샘플 패키지·미디어·문서 소비 모델의 행동 통과로 확대하지 않는다.

```text
W4-CLI-01
python -X utf8 video-production-assets/scripts/validate_project.py --help
관찰: --profile {plan,preproduction,delivery}, --base-dir, positional project.
설명: never artistic/media quality.

W4-CLI-02
python -X utf8 video-production-assets/scripts/validate_storyboard.py --help
관찰: --base-dir, --require-images, --panels-per-sheet, positional project.
설명: coverage/references/timing only; not artistic/generated-image/approval quality.

W4-CLI-03
python -X utf8 video-production-assets/scripts/package_production.py --help
관찰: --output required, --zip, --require-final, --no-history, --base-dir.
설명: registered available/verified real files; existing output never overwritten.
```

원문 지문 산출은 `powershell -NoProfile -Command 'Get-Item -LiteralPath "<정본 표의 실제 full path>" | ForEach-Object { "{0} | {1} | {2}" -f $_.FullName,$_.Length,(Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash.ToLower() }'` 형태로 실제 실행했다. 처음 double-quoted shell 전달은 `$`/backtick interpolation으로 실패했다. 그 실패는 지문 증거로 쓰지 않고 single-quoted `-Command` 호출의 관찰 값만 기록했다. JSON 한 줄 출력은 도구에서 잘려 파일별 줄 출력으로 다시 산출했다.

도구 한계: `read :187:raw`가 단일 줄 대신 open-ended 대형 출력을 반환해 `xd://report_issue`에 신고했다. `:187-187:raw`로 정확 줄을 다시 읽었다. truncated grep/본문을 완전 읽음으로 집계하지 않음.

## 미해결 근거와 정확한 한계

- W4-U01–U27/옵션행에 남은 구체 외부 craft를 기록했다. source-derived 직접 구간이 있는 모듈도 전체 원리/절차가 지원된 것은 아니다. claims는 직접 결속/운영 설계/식별한 미지원 군을 구별한 audit slice이며 모든 문장을 원자 단위로 분해한 전수 ledger라고 주장하지 않는다.
- 주요 잔여: Weston 결과지시/행동동사·듣기, 포즈/접지/anticipation, Pearlman 리듬 분류·소리 기능, chart/인과성 일반 규칙, Young 숙성 후반/44 세분화, genre/comedy/series craft, sponsor 제거/재질 조명, 군중/모드 효과, 접촉 역학/aliasing/합성, 립싱크 음소, grading/플랫폼 효과, 역광학. 원문은 접근 가능하므로 사용자 U3 요청 사유로 바꾸지 않는다. 이것들은 미결속/추가 읽기 범위이지 실제 source unavailable 진단이 아니다.
- Malkiewicz 공백본은 확인했으나 특정 기능을 그 본문만으로 구현해야 한다는 의존은 확정하지 않았다. 정당한 대체 원문 대조 전 모든 조명 기능을 삭제하거나 사용자 재업로드 요구를 하지 않는다.
- frozen S1a/S1b·M-03/V-01–V-28 및 group cases는 미실행. 기존 baseline/response/hash 파일은 미수정. 수동 예시를 formal PASS나 before/after improvement로 합산하지 않는다.
- actual generated/contact/visual/audio quality·전체 playback·책 도판·독립 설치 링크·provider endpoint runtime·계정 자격·패키지 이식성은 미검증.
- 전수 source 결속·독립 행동/재채점 없이 5점/95%를 주장하지 않는다. unread load-bearing 주장이 남은 실제 범위에 대해 독립 R이 고정 rubric modifier/cap을 적용해야 한다. 책 목록 전체의 unread를 모든 모듈에 일괄 적용할 근거는 아님.

## 소유권 요청 / 통합 후 정확 명령

리더 요청: 변경 스킬의 버전·manifest/README/CHANGELOG 통합, 최종 61개 행동 arm과 독립 review/scorecard, standalone 상대 링크 검사는 리더 소유다. W4는 해당 파일을 수정하지 않았다. W1/W2/W3/W6의 위 source 요청은 정본에 반영했다. W5의 브랜드 craft 전수 지원 요청은 구체 새 claim/직접 구간이 없어 이 인덱스만으로 완료 선언하지 않았다.

다음은 **실행하지 않은 통합 검증 명령**이다. `<fixture-root>`는 리더가 실제 파일/원장을 갖춘 새 로컬 fixture, `<new-output>`은 존재하지 않는 출력 경로다. 계획/미디어/정체성/권리 검사를 섞지 않는다.

```text
python -X utf8 scripts/check_versions.py
python -X utf8 -m pytest -q video-production-assets/scripts
python -X utf8 -m pytest -q
python -X utf8 video-production-assets/scripts/validate_project.py <fixture-root>/project.json --profile plan --base-dir <fixture-root>
python -X utf8 video-production-assets/scripts/validate_storyboard.py <fixture-root>/project.json --require-images --base-dir <fixture-root>
python -X utf8 video-production-assets/scripts/validate_project.py <fixture-root>/project.json --profile preproduction --base-dir <fixture-root>
python -X utf8 video-production-assets/scripts/package_production.py <fixture-root>/project.json --base-dir <fixture-root> --output <new-output> --zip --require-final
python -X utf8 qa/skill-completeness-95/run_cases.py --manifest qa/skill-completeness-95/case-manifest.json --run-dir <new-run-dir> --case S1a
python -X utf8 qa/skill-completeness-95/run_cases.py --manifest qa/skill-completeness-95/case-manifest.json --run-dir <new-run-dir> --case S1b
python -X utf8 qa/skill-completeness-95/run_cases.py --manifest qa/skill-completeness-95/case-manifest.json --run-dir <new-run-dir> --case M-03
```

추가 정상/경계 확인: 제품이 필수 플롯 장치라 제거 시 붕괴하는 경우를 무조건 실패하지 않는지; 다른 노드에서 이미 균형/매칭한 실제 컷을 빈 Shot Match 노드만으로 실패하지 않는지; 비용 예외가 있는 Codex Imagen 정지 이미지와 명시 선택된 다른 공급자의 비용 게이트를 구별하는지; 새 출처 heading이 있어도 실제 미지원 장르/기억/유지 효과에 BASIS를 붙이는지. 이 시나리오도 아직 fresh-session 실행하지 않았다.
