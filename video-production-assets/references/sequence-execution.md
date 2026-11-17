# 시퀀스 실행 — 대본·계획 프레임·채택 구간·최종 출력 연결

전체 콘티의 영상화, 선행 결과를 사용하는 후속 생성, 시퀀스 편집/납품에서 사용한다. 코디네이터가 아래 도구 결과를 읽고 문제를 수정하며 사용자가 컷별 상태표를 작성하지 않는다. 연속성 기준은 [26](26-state-causality-continuity.md#storyline-continuity-gate), 편집 판단은 [09](09-edit.md), 실제 매체 판정은 [21](21-generated-video-qa-retry.md)이 소유한다.

도구는 실제 파일·버전·시간·기록을 검사한다. 이미지 의미/물리/연기/청취를 자동 판정하지 않는다. `ready`는 그 단계의 **기록·구조 준비 상태**이며 미감 인증이나 새로운 실행 허가가 아니다. 검토 자료 생성·렌더는 실제 미디어 작업이므로 현재 승인 범위에서만 수행한다. 외부 생성 호출은 여기서 실행하지 않는다.

## 1. 먼저 환경과 잠금 조건을 확인한다

대본·각본·현재 콘티·참조의 ID/버전을 읽고 필수 사건·정확한 대사·화자·카메라·공개 시각·고정 길이·원테이크·예산/재시도 범위를 확인한다. 실제 이미지 열기, 영상 정속 지각, 청취, 편집 실행 가능 여부를 구분한다. 도구 목록/재생기 존재만으로 시청·청취 능력을 주장하지 않는다. 필요한 능력이 없으면 반복 생성 전에 blocker를 보고하고 가능한 계획 작업을 계속한다.

## 2. 계획 문맥을 조회하고 실제 콘티를 대조한다

아래 `scripts/`는 이 스킬 폴더 기준이다. `<root>`는 기존 작품 폴더이며 공유 스킬 폴더에 작품 데이터를 저장하지 않는다.

```bash
python scripts/sequence_context.py <root>/project.json --all > <root>/source/sequence-v01.json
# 후속 작업: 기존 선택/관찰을 유지하면서 필요한 앞뒤 문맥을 조회한다.
python scripts/sequence_context.py <root>/project.json --shot SH02 --projection <root>/source/sequence-v01.json
python scripts/inspect_sequence_frames.py <root>/project.json <root>/source/sequence-v01.json --mode plan --output qa/plan-review-v01
```

처음 조회한 결과는 **미완성 계획 뼈대**다. `owner.artifact_id/artifact_version`에 현재 소유 산출물을 연결하고 입력 버전·실제 사용 에셋의 버전/해시를 핀한다. 코디네이터가 원문에서 요구를 추출해 `requirements`의 자동 beat/speech/direction 대응을 보완한다. 자유 서술을 읽지 않은 채 코드의 자동 대응만으로 연출 해석이 끝났다고 하지 않는다.

검토 자료의 실제 이미지를 열어 **샷 내부 start→정점→end, 인접 컷 출구→입구, 씬 전체, 인서트/시간선 뒤 재등장**을 대조한다. 먼저 픽셀에서 보이는 사실을 관찰하고 대본과 비교한다. 설명문을 이미지 증거로 대신하지 않는다.

각 `links` 행의 `relation`을 확정한다: `continuous_action`, `angle_change`, `reaction`, `spatial_move`, `time_elision`, `cross_cut`, `flashback`, `intentional_discontinuity`. `state_out/state_in`에는 대상·손·소품·상태·공개 등의 관측/계획값을 구분해 넣는다. 차이가 허용되면 `allowed_changes`에 `{field, from, to, reason, source_locator}`를 기록한다. 재등장은 `history_shot_ids`와 `history_state_evidence`에 관련 서사 이력을 연결한다. 화면 좌우와 해부학적 좌우, 역방향 카메라를 혼동하지 않는다.

생성 전에 실제 컷별 **앞 scene/shot/panel → 뒤 scene/shot/panel, final 마지막 포함 프레임 → 다음 첫 프레임, 컷아웃→컷인 행동 단계, 유지/변화, 문제, 수정, 재대조 결과**를 완성한다. 필요한 계획 타임드보드를 재생하고 `plan_timing` 근거를 기록한다. 임시/네이티브 음성이 아직 없으면 발화 시간은 추정이며 실제 음성 검수는 유보한다.

오류는 원문 요구→문제 이미지/프레임→수정 소유자→보존 조건→실제 수정→재대조로 처리한다. 패널 수정 프롬프트만으로 실제 이미지가 고쳐졌다고 하지 않는다. 잠긴 연출·샷 수/원테이크·예산 변경은 승인 범위를 확인한다.

```bash
python scripts/validate_sequence.py <root>/project.json <root>/source/sequence-v01.json --phase plan
```

필수 blocker를 닫은 뒤 제출 단계로 진행한다. 텍스트-only 계획은 미디어 게이트를 통과하지 않아도 텍스트 산출물로 완료할 수 있지만 영상 제작 준비 완료라고 하지 않는다.

## 3. 생성 요청과 실제 앞 테이크를 연결한다

모델의 현재 schema/options·참조 역할·파라미터·길이/오디오·포함/비용을 확인한다. 최종 편집 길이와 생성 길이를 분리하고 동작/대사를 늘여 최소 생성 길이를 채우지 않는다. 정확한 컷은 가능한 경우 편집기로 통제한다. 같은 앵글 연장, 새 앵글, 실제 Extend를 구분한다.

조회의 `focus.shot_ids`는 **이번 제출 대상**이다. 미래 샷의 아직 없는 테이크까지 요구하지 않는다. 대신 이번 샷에 들어오는 실제 선행 출구는 `source_asset_id`, source in/out, FPS/실측 frame count, 현재 핀, 해당 구간 검수와 `predecessor_state_evidence: observed`를 갖춰야 한다. 최신 실패 raw tail을 사용하지 않는다. 새 앵글의 시작 구도는 승인 패널에서 받고 앞 테이크에서는 관련 상태만 계승한다.

현재 승인된 `video_execution_plan`을 `execution_artifact_id`와 `inputs.artifact_versions`에 연결한다. 그 artifact의 `execution_scope`는 `shot_ids`와 `operations: ["generation"]`로 실제 승인 범위를 명시한다. 기존 승인 근거에서 구조화하되 권한을 확대하지 않는다. 요구 행마다 실제 제출문 `request_clause`와 `control_status: HARD_CONTROL|SOFT_PROMPT`를 대응시킨다. 제출 전체 본문·파라미터·참조 슬롯을 원문과 역대조하고 실제 최종 요청 JSON을 등록·핀해 `submission_asset_id`로 연결한다. 도구는 매핑한 문장이 그 요청의 실제 문자열에 있는지도 검사한다. 참조 역할·연출 의미의 충족은 코디네이터가 별도로 확인한다.

```bash
python scripts/validate_sequence.py <root>/project.json <root>/source/sequence-v01.json --phase generation
```

통과 후에도 기존 실행/에셋/가격 게이트와 공급자 도구 절차를 따른다. 도구 호출의 타임아웃은 실패 확정이나 재제출 허가가 아니다. 실제 요청/child/result binding을 조정한 뒤 원본을 등록한다.

## 4. 사용할 실제 구간을 고르고 씬 단위로 편집한다

원본 전체를 실제 검사한 뒤 앞/뒤 컷과 함께 선택한다. 각 컷에 `source_asset_id`, `source_in_frame/source_out_frame`, 실제 `source_fps/source_frame_count`, `final_in_frame/final_out_frame`, `playback_rate: 1`을 연결한다. 프레임은 0-based `[in,out)`다. 마지막 포함 프레임은 out−1이다. 초 단위 편집 표는 정수 프레임에서 파생한다.

불필요한 시작 대기·중복 행동·무기능 꼬리는 제거한다. 원인·접촉·결과·반응·대사·긴장/침묵·여운은 보존한다. 내부 구간 제거는 새 접합이므로 재검사한다. 잠긴 원테이크에 점프 컷을 삽입하지 않는다. 필수 행동이 없으면 크롭/배속/음악으로 숨기지 말고 실제 수정 경로로 돌린다.

실제 양쪽 상태를 다시 관찰해 연결 행을 `evidence: observed`로 갱신한다. 전체 클립 판정·선택 구간 판정·편집 후 판정을 분리하고 과거 reject 기록을 지우지 않는다.

현재 승인된 `edit_plan`에는 `execution_scope: {shot_ids: [...], operations: ["edit", "export"]}`를 둔다. `execution_artifact_id`와 현재 버전을 핀한다. `include_source_audio: true`는 실제 원본 혼합 음향을 사용한다. 별도 실제 음원이 있으면 `audio_tracks`에 `asset_id, source_in_s, source_out_s, final_start_s, gain_db, fade_in_s, fade_out_s`를 연결한다. 원본에 없는 stem을 발명하지 않는다. 무음 프로젝트는 두 경로 모두 비워 둔다.

```bash
python scripts/inspect_sequence_frames.py <root>/project.json <root>/source/sequence-v01.json --mode source --output qa/source-review-v01
python scripts/validate_sequence.py <root>/project.json <root>/source/sequence-v01.json --phase edit
python scripts/render_sequence.py <root>/project.json <root>/source/sequence-v01.json --output final/sequence-v01
```

`source` 비교 자료는 구간 검사 기록이 아직 없어도 실제 등록된 후보를 열어 검사할 수 있도록 생성한다. 검수 전 preview의 `quality`는 unverified다. 렌더는 필요한 실제 구간/경계/요구 검사 기록이 갖춰진 뒤에만 진행한다.

V1 실행 범위는 **같은 CFR/FPS·해상도·1배속 원본의 프레임 정밀 트림, hard cut, 실제 음향 레이어 trim/offset/gain/fade/mix**다. libx264 MP4 또는 ffv1 Matroska를 지원한다. 다른 FPS/VFR/배속·디졸브·복잡 합성은 이 어댑터가 몰래 변환하지 않는다. 명시적으로 conform된 파생본과 raw 계보를 준비하거나 해당 승인된 별도 실행자로 인계한다. 지원하지 않는 연출을 삭제하지 않는다.

## 5. 검사 기록은 실제로 검사한 범위에만 작성한다

`checks`의 한 행:

- `target`: `panel:P01`, `cut:SH01`, `link:SH01->SH02`, `requirement:<key>`, 또는 `scope`.
- `kind/method`: plan_image/opened_image, plan_timing/continuous_playback, source_range/continuous_playback, source_audio/listening, boundary_motion/continuous_playback, boundary_audio/listening, selected_requirement/continuous_playback, playback/continuous_playback, final_requirements/continuous_playback, listening/listening.
- `status`, 실제 `evidence_asset_id`, `observed_asset_ids`, 실제 관찰 `observation`과 해당 `asset_versions`.
- selected_requirement 검사에는 `event_ranges` 배열로 해당 사건의 실제 `{cut_id, source_asset_id, source_in_frame, source_out_frame, final_in_frame, final_out_frame}`를 기록한다. 선택 범위 밖의 사건이나 잘못된 소스→출력 매핑은 거절한다.
- 실제 선택 검사에는 `cut_ranges`로 관련 cut별 `{source_asset_id, source_in_frame, source_out_frame, final_in_frame, final_out_frame}`를 핀한다. source_range/source_audio는 같은 source 3필드를 행에도 둔다.

근거 파일도 현재 asset/version/hash로 등록한다. 정속/청취하지 않았다면 pass를 쓰지 않는다. 자동 전사·파형·파일 디코딩은 청취나 물리/연기 판단을 대신하지 않는다. 선택 구간을 바꾸면 기존 cut_ranges와 달라져 경계/요구 검사를 다시 해야 한다.

## 6. 실제 출력 검사와 시간 승격

렌더 결과의 manifest는 FPS/실측 count/PTS·소스 계보·해시를 제공하지만 `quality: unverified`다. 실제 출력 파일을 등록·핀한 뒤 `output_asset_id`로 연결한다.

```bash
python scripts/inspect_sequence_frames.py <root>/project.json <root>/source/sequence-v01.json --mode export --output qa/export-review-v01
python scripts/validate_sequence.py <root>/project.json <root>/source/sequence-v01.json --phase export
```

모든 실제 컷 경계·인접 모션·재등장과 전체 출력 정속/필요 청취를 대조하고 최종 요구가 읽히는지 확인한다. 해당 `delivery_checks`에 현재 출력과 검사 근거를 연결한다. 저장 파일 자체를 검사하지 않고 납품 통과로 표시하지 않는다.

명시적 고정 시간이 없으면 이야기 우선으로 길이를 조정한다. 고정 전체 시간/공개 프레임은 보존한다. 원장 시간 승격은 기존 `update_project.py`의 한 트랜잭션으로 `project.target_duration_s`, shots, 관련 패널/리듬/cue/자막, owner artifact 버전을 함께 갱신한다. 현재 approved edit_plan의 `timing_policy`와 입력 버전이 필요하다:

```json
{"duration":"flexible","anchors":[{"table":"shots","id":"SH38","field":"start_s","frame":4440}]}
```

위 SH38/4440은 형식 예시이지 현재 작품의 자동 잠금 변경/해제 지시가 아니다. anchors는 shots/audio_cues/captions/panels의 실제 ID와 start_s/end_s/frame_time_s를 기존 FPS 프레임으로 잠근다. 정책이 fixed이거나 anchor를 옮기면 거절한다. 후보 전체가 유효하지 않으면 원장은 그대로다. 기존 lock을 자동 제거하지 않는다.

채택 구간 변경은 소유 edit_plan 버전을 올리고 그 선택을 실제로 소비한 다음 입력·경계 QA·씬 편집·출력 dependency를 연결해 stale을 전파한다. 정상인 원본은 재사용하되 변경된 경계 근거는 재검사한다. 한 샷이 여러 raw 구간이면 허용된 편집에서 실제 precomp와 전체 계보로 정규화한다. 원래 필수 샷/씬 삭제는 별도 변경이며 현재 upsert 도구의 삭제 기능으로 위장하지 않는다.
