# 공유 프롬프트 시트 전체 반영 대조 (2026-10-30)

## 결과와 범위

사용자가 제공한 [공유 시트](https://docs.google.com/spreadsheets/d/1hhHW1d-JCKo4WYeU0wVb_LqJmZuzcCFNqBL2meghPmw/edit)의 **55개 탭, 비어 있지 않은 3,105행**을 수집했다. 이 중 55행은 헤더, **3,050행은 자료**다. 원문 프롬프트 1,155행, 정제 DB 778행, 날짜별 수집 803행, 공통 템플릿 41행, 평가기준 9행, 모델 근거 64행, 기법 로그 175행, 프레임 등록부 25행이다. 제공된 셀 본문에서 재사용 가능한 절차는 기존 오너에 연결하거나 아래처럼 보완했으며, 그대로 옮기지 않은 내용도 이유를 배정했다.

이는 스킬 지침의 반영 대조이지 실제 영상 제작·이미지 검수·최신 모델 사양 확인이 아니다. 원본 스프레드시트는 수정하지 않았다. 개별 줄거리·캐릭터·대사·제품·특정 렌즈/초수와 모델 카탈로그는 공용 정책으로 복제하지 않았다.

기계 판독 근거는 [전수 대조 JSON](../../qa/2026-10-30-prompt-sheet-integration.json)에 있다. 각 탭의 셀 스냅샷 해시·행 범위·반영/제외 근거와 235개 범위 배정이 헤더 포함 3,105행을 중복·누락 없이 덮는다. 프로젝트 원장이나 새 런타임 계약이 아니다.

## 보완 및 충돌 해소

| 항목 | 시트 근거 gid:row | 반영 오너·위치 | 처리 |
|---|---|---|---|
| loop | `0:543`, `0:614`, `0:673`, `0:731`, `0:734`, `0:736`, `0:769-772`, `0:1027`, `802665128:379` | [09-edit.md](../../video-production-assets/references/09-edit.md) · 요청된 루프의 끝→시작 검수 | implemented |
| realtime | `1913910415:21`, `802665128:240-244`, `802665128:278` | [video-generation-planning.md](../../creative-production/references/video-generation-planning.md) · Real-time state checkpoints | implemented |
| spatial_audio | `802665128:136`, `1247462036:8` | [09-edit.md](../../video-production-assets/references/09-edit.md) · 실행 가능한 편집·사운드 큐 | implemented |
| masked_edit | `1913910415:31`, `802665128:502-504`, `19102026:24-26` | [29-reference-driven-production.md](../../video-production-assets/references/29-reference-driven-production.md) · R5 | implemented |
| frame_asset_truth | `1913910415:19-20`, `1913910415:40-42`, `28102026:2`, `2026103002:2-26` | [24-production-execution.md](../../video-production-assets/references/24-production-execution.md) · 프레임 프롬프트·실제 에셋·추출 프레임의 구분 | implemented |
| mode_preflight | `1913910415:18`, `1913910415:23-42`, `20261020:2-9`, `20261030:2-6` | [24-production-execution.md](../../video-production-assets/references/24-production-execution.md) · 3. 영상 생성 경로 | strengthened |
| audio_transport | `0:83`, `0:317`, `0:358-373`, `0:1084-1091` | [control-contract.md](../../ai-camera-control/references/control-contract.md) · 시간 구간 행동·보존 제약·오디오 분리 | conflict_resolved |
| continuous_motion_and_soft_camera | `0:91`, `0:203`, `0:319-322`, `0:626-639`, `0:741-760` | [21-generated-video-qa-retry.md](../../video-production-assets/references/21-generated-video-qa-retry.md) · 1 / 5 | conflict_resolved |
| utterance_mapping | `1913910415:17`, `1913910415:23` | [11-ai-handoff.md](../../video-production-assets/references/11-ai-handoff.md) · 보드 시간과 실제 제출문 | stale_consumer_clauses_aligned |
| pagination_default | `1913910415:4`, `0:98`, `0:227`, `0:373` | [storyboard-contract.md](../../video-production-assets/references/storyboard-contract.md) · 4. 실제 이미지 생성·시트·clean 컷 | stale_default_8_clause_corrected_to_4 |
| allowed_delta_vs_lock | `802665128:421`, `802665128:719`, `21102026:11` | [26-state-causality-continuity.md](../../video-production-assets/references/26-state-causality-continuity.md) · 인계 최소 슬롯 | clarified |

- 루프는 요청한 경우에만 적용한다. 의도된 리셋과 연속 접합을 나누고, 끝→시작의 동작/카메라 phase·광원·오디오를 실제 반복 재생으로 검사한다.
- 실시간 지시는 전송·수락·노출된 실제 적용·관측 시점을 구별한다. 실행자가 지원하는 승인된 세션만 해당하며 배치 프롬프트로 실시간 기능을 발명하지 않는다.
- 공간음은 청취 관점·음원 위치를 기존 사운드 큐에 적는다. 역방향 컷의 화면 좌우만 보고 스테레오 채널을 뒤집지 않는다.
- 마스크는 선택 도구의 실제 극성·소스/마스크 프레임 대응·시간 경계를 확인한다. 특정 모델의 흰색/검정 규칙을 보편화하지 않는다.
- 프레임 목표/프롬프트, 계획 도식, 생성 정지, 실제 영상 추출을 분리한다. 지원하지 않는 Last 입력은 QA 목표이지 실제 제출 슬롯이 아니다. 원하는 스타일을 보존하고 포토리얼을 강제하지 않는다.
- 입력의 개별 지원과 동시 지원은 다르다. 모드 배타 조건과 first/middle/last/reference 공유 한도를 실제 첨부에 대조한다.
- 별도 오디오 파라미터가 없어도 검증된 공통 요청문이 네이티브 오디오를 받으면 같은 요청의 AUDIO 구획을 쓴다. 카메라 의도는 HARD_CONTROL/SOFT_PROMPT/미지원/미확인으로 구별한다.
- 복합 행동은 먼저 같은 샷의 인과 비트로 검토한다. 자동 분할이나 발화별 얼굴/반응 컷 할당을 강제하지 않는다. 시트는 기본 4·도구 상한 8이며 이야기를 그리드에 맞추지 않는다.
- 변화하는 속성을 동시에 hard lock으로 묶지 않는다. 계획된 소유 이전·점등·재료 변화는 해당 구간의 승인 델타와 그 이후의 새 보존 상태로 적는다.

## 탭별 전수 처리

아래 수량은 각 탭의 헤더를 제외한다. 날짜/ID 후보 연결은 중복 증명이 아니며, 날짜 순서로만 연결된 41행은 별도 잔여 내용으로 검토했다. 10월 5일 25행과 10월 24·25일 기법 로그 50행도 별도로 대조했다.

| 탭 | gid | 자료 행 | 처리 |
|---|---:|---:|---|
| 시트1 | 0 | 1155 | 원문 기법·예시 분리 |
| 2026-09-26 수집 25선 | 440049793 | 25 | 기존/보완 오너에 조건부 연결 |
| 정제 프롬프트 DB | 802665128 | 778 | 기존/보완 오너에 조건부 연결 |
| 평가기준 | 1568858118 | 9 | 차원 재사용·가중치 제외 |
| 2026-09-27 수집 25선 | 2011031124 | 28 | 기존/보완 오너에 조건부 연결 |
| 범용 제작 템플릿 | 1913910415 | 41 | 규칙별 적용/충돌 해소 |
| 2026-09-29 수집 25선 | 1018157599 | 25 | 기존/보완 오너에 조건부 연결 |
| 2026-09-30 수집 25선 | 1888782427 | 25 | 기존/보완 오너에 조건부 연결 |
| 2026-10-01 수집 25선 | 2091968671 | 25 | 기존/보완 오너에 조건부 연결 |
| 2026-10-02 수집 25선 | 1247462036 | 25 | 기존/보완 오너에 조건부 연결 |
| 2026-10-03 수집 25선 | 1728983177 | 25 | 기존/보완 오너에 조건부 연결 |
| 2026-10-05 수집 25선 | 1253274152 | 25 | 기존/보완 오너에 조건부 연결 |
| 2026-10-07 수집 25선 | 956925664 | 25 | 기존/보완 오너에 조건부 연결 |
| 2026-10-08 수집 25선 | 1026080801 | 25 | 기존/보완 오너에 조건부 연결 |
| 2026-10-09 수집 25선 | 1718545322 | 25 | 기존/보완 오너에 조건부 연결 |
| 2026-10-10 수집 25선 | 298571234 | 25 | 기존/보완 오너에 조건부 연결 |
| 2026-10-11 수집 25선 | 11102026 | 25 | 기존/보완 오너에 조건부 연결 |
| 2026-10-12 수집 25선 | 12102026 | 25 | 기존/보완 오너에 조건부 연결 |
| 2026-10-13 수집 25선 | 13102026 | 25 | 기존/보완 오너에 조건부 연결 |
| 2026-10-14 수집 25선 | 14102026 | 25 | 기존/보완 오너에 조건부 연결 |
| 2026-10-15 수집 25선 | 15102026 | 25 | 기존/보완 오너에 조건부 연결 |
| 2026-10-16 수집 25선 | 16102026 | 25 | 기존/보완 오너에 조건부 연결 |
| 2026-10-17 수집 25선 | 17102026 | 25 | 기존/보완 오너에 조건부 연결 |
| 2026-10-18 수집 25선 | 18102026 | 25 | 기존/보완 오너에 조건부 연결 |
| 2026-10-19 수집 25선 | 19102026 | 25 | 기존/보완 오너에 조건부 연결 |
| 2026-10-20 수집 25선 | 20102026 | 25 | 기존/보완 오너에 조건부 연결 |
| 2026-10-20 모델 근거 | 20261020 | 8 | 과거 주장으로 보존·현재 기능으로 이식 안 함 |
| 2026-10-21 수집 25선 | 21102026 | 25 | 기존/보완 오너에 조건부 연결 |
| 2026-10-21 모델 근거 | 20261021 | 5 | 과거 주장으로 보존·현재 기능으로 이식 안 함 |
| 2026-10-22 수집 25선 | 22102026 | 25 | 기존/보완 오너에 조건부 연결 |
| 2026-10-22 모델 근거 | 20261022 | 8 | 과거 주장으로 보존·현재 기능으로 이식 안 함 |
| 2026-10-23 수집 25선 | 23102026 | 25 | 기존/보완 오너에 조건부 연결 |
| 2026-10-23 모델 근거 | 20261023 | 9 | 과거 주장으로 보존·현재 기능으로 이식 안 함 |
| 2026-10-24 수집 25선 | 24102026 | 25 | 기존/보완 오너에 조건부 연결 |
| 2026-10-24 모델 근거 | 20261024 | 4 | 과거 주장으로 보존·현재 기능으로 이식 안 함 |
| 2026-10-24 기법 수집 로그 | 2026102401 | 25 | 기존/보완 오너에 조건부 연결 |
| 2026-10-25 수집 25선 | 25102026 | 25 | 기존/보완 오너에 조건부 연결 |
| 2026-10-25 모델 근거 | 20261025 | 4 | 과거 주장으로 보존·현재 기능으로 이식 안 함 |
| 2026-10-25 기법 수집 로그 | 2026102501 | 25 | 기존/보완 오너에 조건부 연결 |
| 2026-10-26 수집 25선 | 26102026 | 25 | 기존/보완 오너에 조건부 연결 |
| 2026-10-26 모델 근거 | 20261026 | 6 | 과거 주장으로 보존·현재 기능으로 이식 안 함 |
| 2026-10-26 기법 수집 로그 | 2026102601 | 25 | 기존/보완 오너에 조건부 연결 |
| 2026-10-27 수집 25선 | 27102026 | 25 | 기존/보완 오너에 조건부 연결 |
| 2026-10-27 모델 근거 | 20261027 | 5 | 과거 주장으로 보존·현재 기능으로 이식 안 함 |
| 2026-10-27 기법 수집 로그 | 2026102701 | 25 | 기존/보완 오너에 조건부 연결 |
| 2026-10-28 수집 25선 | 28102026 | 25 | 기존/보완 오너에 조건부 연결 |
| 2026-10-28 모델 근거 | 20261028 | 5 | 과거 주장으로 보존·현재 기능으로 이식 안 함 |
| 2026-10-28 기법 수집 로그 | 2026102801 | 25 | 기존/보완 오너에 조건부 연결 |
| 2026-10-29 수집 25선 | 29102026 | 25 | 기존/보완 오너에 조건부 연결 |
| 2026-10-29 모델 근거 | 20261029 | 5 | 과거 주장으로 보존·현재 기능으로 이식 안 함 |
| 2026-10-29 기법 수집 로그 | 2026102901 | 25 | 기존/보완 오너에 조건부 연결 |
| 2026-10-30 수집 25선 | 30102026 | 25 | 기존/보완 오너에 조건부 연결 |
| 2026-10-30 모델 근거 | 20261030 | 5 | 과거 주장으로 보존·현재 기능으로 이식 안 함 |
| 2026-10-30 기법 수집 로그 | 2026103001 | 25 | 기존/보완 오너에 조건부 연결 |
| 2026-10-30 프레임 에셋 등록부 | 2026103002 | 25 | 자료 유형/미검증 상태만 적용 |

## 공통 템플릿 각 행의 처리

전체 템플릿 41행을 최신 행 하나로 대체하지 않고 개별 대조했다. 아래 파일명은 JSON의 실제 저장소 경로로 해석한다. 2026-06 이후 출시 모델만 사용, 고정 3막/3–6샷/4–16키프레임/0.5초 홀드/0.3초 음향 꼬리, 점수·권장 모델표는 수집 자료의 조건 또는 예시이지 런타임 기본값이 아니다.

| 행 | 블록 | 처리 | 오너 |
|---:|---|---|---|
| 2 | MASTER PRODUCTION PROMPT | reuse canonical story, reference-role, causal state, audio, preview and repair owners | `11-ai-handoff.md`, `26-state-causality-continuity.md`, `24-production-execution.md` |
| 3 | CHARACTER SHEET | reuse canonical story, reference-role, causal state, audio, preview and repair owners | `SKILL.md`, `24-production-execution.md` |
| 4 | STORYBOARD SHEET | keep prior 4-default/8-cap pagination; reject fixed 3x3 story quota | `storyboard-contract.md` |
| 5 | FIRST/LAST FRAME | reuse canonical story, reference-role, causal state, audio, preview and repair owners | `26-state-causality-continuity.md`, `24-production-execution.md` |
| 6 | SHOT CARD | reuse canonical story, reference-role, causal state, audio, preview and repair owners | `06-shots.md`, `11-ai-handoff.md` |
| 7 | CONTINUITY LEDGER | reuse canonical story, reference-role, causal state, audio, preview and repair owners | `26-state-causality-continuity.md`, `21-generated-video-qa-retry.md` |
| 8 | MULTI-KEYFRAME BEAT MAP | reuse canonical story, reference-role, causal state, audio, preview and repair owners | `26-state-causality-continuity.md`, `24-production-execution.md` |
| 9 | REFERENCE ROLE MAP | reuse canonical story, reference-role, causal state, audio, preview and repair owners | `29-reference-driven-production.md` |
| 10 | HANDOFF STATE CONTRACT | reuse canonical story, reference-role, causal state, audio, preview and repair owners | `26-state-causality-continuity.md`, `09-edit.md` |
| 11 | LONG-TAKE BEAT MAP | reuse canonical story, reference-role, causal state, audio, preview and repair owners | `video-generation-planning.md`, `06-shots.md` |
| 12 | ASSET AUTHORITY MATRIX | reuse canonical story, reference-role, causal state, audio, preview and repair owners | `29-reference-driven-production.md`, `26-state-causality-continuity.md` |
| 13 | STRUCTURED CRITIC / REPAIR LOOP | reuse canonical story, reference-role, causal state, audio, preview and repair owners | `21-generated-video-qa-retry.md`, `12-qa.md` |
| 14 | AUDIO-VISUAL ACCEPTANCE MATRIX | reuse canonical story, reference-role, causal state, audio, preview and repair owners | `21-generated-video-qa-retry.md`, `22-dialogue-lipsync.md`, `09-edit.md` |
| 15 | DRAFT → FINAL QUALITY GATE | reuse canonical story, reference-role, causal state, audio, preview and repair owners | `24-production-execution.md` |
| 16 | CANONICAL ASSET PACK + SHOT STATE TABLE | reuse canonical story, reference-role, causal state, audio, preview and repair owners | `29-reference-driven-production.md`, `26-state-causality-continuity.md`, `24-production-execution.md` |
| 17 | KEYFRAME AUDIO CONTINUITY | reuse canonical story, reference-role, causal state, audio, preview and repair owners | `22-dialogue-lipsync.md`, `09-edit.md`, `26-state-causality-continuity.md` |
| 18 | MODEL CAPABILITY CONTRACT | reuse source/mode/provenance/QA mechanisms; exclude fixed model catalog, date filter, scores and media claims | `24-production-execution.md` |
| 19 | FIRST/LAST FRAME ASSET GATE | reuse source/mode/provenance/QA mechanisms; exclude fixed model catalog, date filter, scores and media claims | `24-production-execution.md` |
| 20 | EVIDENCE & ASSET TRUTH CONTRACT | reuse source/mode/provenance/QA mechanisms; exclude fixed model catalog, date filter, scores and media claims | `24-production-execution.md`, `12-qa.md` |
| 21 | REALTIME DIRECTOR STATE CHECKPOINT | add conditional realtime sent/accepted/observed state checkpoints | `video-generation-planning.md` |
| 22 | 2026-10-10 UNIVERSAL MODEL ADAPTER + TRUTHFUL ASSET GATE | reuse source/mode/provenance/QA mechanisms; exclude fixed model catalog, date filter, scores and media claims | `24-production-execution.md`, `29-reference-driven-production.md`, `26-state-causality-continuity.md`, `12-qa.md` |
| 23 | 2026-10-11 Vidu Q4 REFERENCE+VOICE CONTRACT | reuse source/mode/provenance/QA mechanisms; exclude fixed model catalog, date filter, scores and media claims | `24-production-execution.md`, `29-reference-driven-production.md`, `26-state-causality-continuity.md`, `12-qa.md` |
| 24 | 2026-10-12 MODE-CONFLICT PREFLIGHT + EVIDENCE-BOUND KEYFRAME GATE | reuse source/mode/provenance/QA mechanisms; exclude fixed model catalog, date filter, scores and media claims | `24-production-execution.md`, `29-reference-driven-production.md`, `26-state-causality-continuity.md`, `12-qa.md` |
| 25 | 2026-10-13 UNIVERSAL PRODUCTION DSL + REFERENCE ORDER GATE | reuse source/mode/provenance/QA mechanisms; exclude fixed model catalog, date filter, scores and media claims | `24-production-execution.md`, `29-reference-driven-production.md`, `26-state-causality-continuity.md`, `12-qa.md` |
| 26 | 2026-10-14 EVIDENCE→PRODUCTION + IP RIGHTS GATE | reuse source/mode/provenance/QA mechanisms; exclude fixed model catalog, date filter, scores and media claims | `24-production-execution.md`, `29-reference-driven-production.md`, `26-state-causality-continuity.md`, `12-qa.md` |
| 27 | 2026-10-15 FRAME-PAIR PROVENANCE + MODE-SPLIT ACCEPTANCE GATE | reuse source/mode/provenance/QA mechanisms; exclude fixed model catalog, date filter, scores and media claims | `24-production-execution.md`, `29-reference-driven-production.md`, `26-state-causality-continuity.md`, `12-qa.md` |
| 28 | 2026-10-16 SHOT AUTHORITY + FRAME PAIR QA | reuse source/mode/provenance/QA mechanisms; exclude fixed model catalog, date filter, scores and media claims | `24-production-execution.md`, `29-reference-driven-production.md`, `26-state-causality-continuity.md`, `12-qa.md` |
| 29 | 2026-10-17 FRAME-PAIR / REFERENCE MODE SPLIT + AUDIO STATE | reuse source/mode/provenance/QA mechanisms; exclude fixed model catalog, date filter, scores and media claims | `24-production-execution.md`, `29-reference-driven-production.md`, `26-state-causality-continuity.md`, `12-qa.md` |
| 30 | 2026-10-18 STORYBOARD→SHOT AUTHORITY + ASSET EVIDENCE V2 | reuse source/mode/provenance/QA mechanisms; exclude fixed model catalog, date filter, scores and media claims | `24-production-execution.md`, `29-reference-driven-production.md`, `26-state-causality-continuity.md`, `12-qa.md` |
| 31 | 2026-10-19 MODEL ROUTER + MASK AUTHORITY + FRAME PROVENANCE v3 | generalize mask verification; exclude cached polarity/model limits | `24-production-execution.md`, `29-reference-driven-production.md`, `26-state-causality-continuity.md`, `12-qa.md` |
| 32 | 2026-10-20 KLING 4.0 OMNI REFERENCE + 10-KEYFRAME ADAPTER | reuse source/mode/provenance/QA mechanisms; exclude fixed model catalog, date filter, scores and media claims | `24-production-execution.md`, `29-reference-driven-production.md`, `26-state-causality-continuity.md`, `12-qa.md` |
| 33 | 2026-10-21 UNIVERSAL STORY→FRAME→MODEL ROUTER v4 | reuse source/mode/provenance/QA mechanisms; exclude fixed model catalog, date filter, scores and media claims | `24-production-execution.md`, `29-reference-driven-production.md`, `26-state-causality-continuity.md`, `12-qa.md` |
| 34 | 2026-10-22 UNIVERSAL STORYBOARD→FRAME PAIR v5 + ASSET PROVENANCE | reuse source/mode/provenance/QA mechanisms; exclude fixed model catalog, date filter, scores and media claims | `24-production-execution.md`, `29-reference-driven-production.md`, `26-state-causality-continuity.md`, `12-qa.md` |
| 35 | 2026-10-23 MODEL CAPABILITY SNAPSHOT + UNIVERSAL v6 | reuse source/mode/provenance/QA mechanisms; exclude fixed model catalog, date filter, scores and media claims | `24-production-execution.md`, `29-reference-driven-production.md`, `26-state-causality-continuity.md`, `12-qa.md` |
| 36 | 2026-10-24 DIRECTOR'S CONTINUITY MATRIX v7 | reuse source/mode/provenance/QA mechanisms; exclude fixed model catalog, date filter, scores and media claims | `24-production-execution.md`, `29-reference-driven-production.md`, `26-state-causality-continuity.md`, `12-qa.md` |
| 37 | 2026-10-25 FRAME PROVENANCE + MODE-AWARE QA v8 | reuse source/mode/provenance/QA mechanisms; exclude fixed model catalog, date filter, scores and media claims | `24-production-execution.md`, `29-reference-driven-production.md`, `26-state-causality-continuity.md`, `12-qa.md` |
| 38 | 2026-10-26 UNIVERSAL STORY→SHOT→FRAME v9 + MODE ROUTER | reuse source/mode/provenance/QA mechanisms; exclude fixed model catalog, date filter, scores and media claims | `24-production-execution.md`, `29-reference-driven-production.md`, `26-state-causality-continuity.md`, `12-qa.md` |
| 39 | 2026-10-27 UNIVERSAL STORY→SHOT→FRAME v10 + CAUSAL STATE VALIDATOR | reuse source/mode/provenance/QA mechanisms; exclude fixed model catalog, date filter, scores and media claims | `24-production-execution.md`, `29-reference-driven-production.md`, `26-state-causality-continuity.md`, `12-qa.md` |
| 40 | 2026-10-28 UNIVERSAL VIDEO PRODUCTION v11 + FRAME ASSET PROVENANCE | reuse source/mode/provenance/QA mechanisms; exclude fixed model catalog, date filter, scores and media claims | `24-production-execution.md`, `29-reference-driven-production.md`, `26-state-causality-continuity.md`, `12-qa.md` |
| 41 | 2026-10-29 UNIVERSAL VIDEO PRODUCTION v12 + API TRUTH GATE | reuse source/mode/provenance/QA mechanisms; exclude fixed model catalog, date filter, scores and media claims | `24-production-execution.md`, `29-reference-driven-production.md`, `26-state-causality-continuity.md`, `12-qa.md` |
| 42 | 2026-10-30 UNIVERSAL VIDEO PRODUCTION v13 + SOURCE/FRAME ROUTER | reuse source/mode/provenance/QA mechanisms; exclude fixed model catalog, date filter, scores and media claims | `24-production-execution.md`, `29-reference-driven-production.md`, `26-state-causality-continuity.md`, `12-qa.md` |

## 기존에 충족된 내용과 제외 이유

- 시놉 비트·서사 목적, 연기·감정 가독성, 카메라·공간·조명·리듬은 02/04/05/06/07/09와 완전한 보드 계약에 이미 있다. 필드 존재나 컷 수를 작품 품질로 간주하지 않는다.
- 참조의 속성별 권한·정체성·제품 형상·소유·보존/허용 변화, 실제 업로드 순서, 시작/끝 상태와 인과·접촉·가림은 11/19/20/26/29에 있다. 정확한 텍스트·UI는 필요한 경우 제어 가능한 레이어로 분리한다.
- 네이티브 음성·화자·침묵·립싱크·J/L 컷·룸톤·음악/접촉 동기점, 사용 구간·확장/부분 수정, 최소 수정·프리뷰/최종 QA·승인/비용은 09/21/22/24/29의 기존 오너를 사용한다.
- 실제 endpoint 기능·입력 조합·지역/계정·가격은 실행 시 확인한다. 시트의 공식 출처 표기나 오래된 모델 수치만으로 지원을 보장하지 않는다. 스타일·주제·장르 예시가 새 강제 규격이 되지 않는다.
- 평가표의 차원은 검토에 활용하지만 가중치·수집자의 자체 고득점을 자동 통과나 실제 영상 점수로 이식하지 않는다.
- 원문 gid 0의 153행은 placeholder뿐이므로 실행 절차로 복원하지 않았다. 262·389·929·957·958·960·962행은 생략/축약 또는 불완전 원문을 포함한다. 제공된 부분만 처리했고 사라진 원문은 만들어내지 않았다. 107·522행의 섞인 꼬리 문장도 공용 규칙에서 제외했다.
- 440→434, 441→436의 정확한 원문 중복은 각 행을 보존해 처리했고 새 기법 수로 부풀리지 않았다. 날짜/패턴 ID의 후보 연결과 정확한 본문 중복은 구분했다.
- gid 28102026의 2행은 P의 CONCEPT_FRAMES와 Q/R의 GENERATED_CINEMATIC_IMAGE가 충돌한다. 실제 파일/이력 확인 전에는 어느 쪽도 인증하지 않았다. gid 2026103002의 2행은 도식 pair와 생성 still pair를 따로 선언한 것이므로 자동으로 충돌 취급하지 않는다.
- 연결된 Drive 이미지/영상·외부 원문·서비스 endpoint는 이번 셀 대조의 실물 검수 대상이 아니다. 실제 생성·업로드·출처·권리·품질을 확인했다고 하지 않으며 이 파일들이 활성 제작 에셋으로 등록된 것도 아니다.

## 검토 방법과 한계

원문 전/후반은 578/577행을 30/56개 비중첩 그룹으로 대조했다. 정제 전반은 389개 패턴과 날짜별 389행을 대조했다. 정제 후반은 389개 패턴·928행의 첫 대조에서 출력 생략 때문에 완전 검토를 인증하지 못했다. 그 상태를 완료로 사용하지 않고 11,661개 고유 문장/메타데이터 조각을 작은 묶음으로 재검토했으며, 구조화된 LLM 보조 분류의 ID를 전수 검산했다. 서버 과부하로 빠진 300개 조각은 150개씩 다시 확인해 배정 누락 0·미확인 조각 0으로 닫았다. 원문이 갖고 있지 않은 내용이나 linked media까지 읽었다는 뜻은 아니다.

자동 검토가 제시한 권리 확인·누락 입력·편집 핸들 항목은 기존 24/11/타임라인 절차로 이미 충족함을 확인했다. Runway 공급 경로와 Kling 모델명이 함께 있다는 이유만으로 출처 충돌이라고 한 후보도 채택하지 않았다. 인과·시간·불변/변화가 실제로 어긋나는 예시는 소스 결함으로 남기며 새 규칙으로 복제하지 않았다.

## 저장소 검증

전체 회귀는 **402 passed / 518 subtests passed (29.30s)**, 버전 검사는 패키지 2.30·26개 스킬 일관성, 설치 동기화 사전 검사는 exit 0이다. JSON 117개 구문 검사와 변경 문서 17개의 로컬 파일/절 링크 검사, CRLF를 고려한 whitespace 검사를 통과했다. 세 핵심 설치 스킬의 링크도 현재 저장소를 가리킨다. JSON 언어 서버 biome은 미설치여서 구문 파싱으로 대체했고 의존성을 추가하지 않았다. 순수 지침 변경에 문구 고정 테스트를 추가하지 않았다. 실제 미디어 품질이나 에이전트 행동 향상을 입증하는 벤치마크는 아니며, 커밋·미디어 생성·게시·시트 수정은 하지 않았다.
