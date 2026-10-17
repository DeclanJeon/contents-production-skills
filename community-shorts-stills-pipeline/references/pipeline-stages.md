# 파이프라인 단계

사연 하나가 발행 가능한 쇼츠가 되기까지의 순서. 각 단계는 **앞 단계의 산출물을 근거로만** 진행한다.

## 1. 사연 확보와 권리

- 소스는 공개 원문 URL + 인용 위치(locator). 원문 제목/시각을 원장에 그대로 보존한다.
- 권리 상태가 `cleared`가 아니면 이후 단계로 가지 않는다. 증거 문자열(`source_rights_evidence`)이
  함께 있어야 하며, 정책과 에피소드 양쪽 모두에서 확인한다.
- 발견 단계는 커뮤니티 게시판을 주기적으로 스캔해 `discovered-sources.json`에 후보를 쌓고,
  수요 판정(`demand_verdict`)을 붙인다. 수요가 `limited`여도 사용자가 고정(pin)하면 진행한다.

## 2. 원장(project.json)과 샷 윈도우

- 원장은 `target_duration_s=60`, `fps=30`, `aspect_ratio="9:16"`, `audio_mode="dialogue"`를 고정한다.
- 샷 윈도우는 **프레임 정렬**이다. 각 경계는 1/30초의 정수배, 합계는 정확히 1800프레임=60.000초.
  임의 소수점 윈도우는 렌더러가 거부한다.
- 샷마다 `role=='hold'` 패널이 정확히 하나, `kind=='narration'` 발화가 정확히 하나 있어야 한다.
  샷 수는 1..20 범위이며 18로 하드코딩하지 않는다.
- 패널·아이덴티티 시트는 sha256으로 고정한다. 픽셀이 바뀌면 `panel_missing_or_changed`로 중단한다.
- 감정/템포 연출은 샷의 7필드 `performance` 문자열에서 클러스터 키 `(감정, 템포)`로 뽑는다.
  같은 클러스터는 같은 지시(happy/1.25 등)를 재사용한다 — 샷마다 새로 지시하지 않는다.

## 3. 내레이션 (TTS)

- **고정된 내레이션이 있으면 재합성하지 않는다.** 원장의 발화(`speech`)와 녹음은 아티팩트의
  `asset_ids`로 이어진다. 각 발화의 녹음은 `<speech_id>-WAV-V###` 중 **가장 높은 버전**을 고르고,
  sha256이 일치할 때만 복사한다. 파일명을 추정하지 않는다. 이 경로에서는 Typecast를 부르지 않는다.
  녹음이 하나도 없을 때만(=미제작 에피소드) 처음 합성한다.
- 고정 자막 트랙(`<...>-CAPTIONS-SRT-V###`)에서 제공된 타임스탬프를 읽되, cue 단위 SRT를 실제 단어 타이밍으로 승격하지 않는다. 단어 정렬 근거가 없으면 정렬 단계는 차단한다. 추정 자막은 쓰지 않는다.
  `caption_source`는 실제 산출물 출처·버전·해시와 정렬 방식을 기록한다. Typecast 생성 증거가 있을 때만 "actual Typecast word timestamps"라고 적는다. SRT 존재만으로 단어 단위 실측을 주장하지 않는다.
- 새로 합성할 때만 샷별 WAV(44100/1ch/16-bit)를 남기고, 불확실한 결과는 `provider_outcome_uncertain`으로
  막고 사람이 판단하게 한다.
- **각 녹음은 자기 샷 윈도우 안에 놓인다.** 렌더러는 `apad -t <샷 윈도우>`로 샷을 채우므로 녹음이
  윈도우보다 길면 잘린다 → `narration_overruns_shot`으로 중단한다. 타임베이스 게이트는 뒤로 이어붙인
  녹음 길이 합이 아니라 **원장의 샷 윈도우 합(정확히 60초)** 을 본다(`narration_outside_target` 폐기).
- 음성/모델 ID는 정책에서 고정한다. 같은 텍스트·음성 조합은 이력에서 재사용하고 재과금하지 않는다.

## 4. 렌더

- `references/measured-geometry.md`의 수치로 웹툰 페이지를 한 장씩 그린다.
- 샷마다 페이지 1장 → 클립 1개 → concat → 스트림 경계 패스 → (배속 시) 배속 패스.
- 정지 화면만. 켄번즈/크롭/컷은 허용, 생성형 모션 모델은 금지.

## 5. 자막 burn-in과 라우드니스

- 워드 타임스탬프로 ASS를 만들고 burn-in한다. 자막 텍스트는 원장의 `captions`와 일치해야 한다.
- 라우드니스는 `loudnorm=I=-16:TP=-1.5:LRA=11`을 **측정값 기반 2-pass**로 적용한다.
  이 단계는 60초 타임베이스에서 수행한다 — 배속보다 먼저.

## 6. 배속 (선택)

- `references/delivery-speed.md` 참조. 렌더·자막·라우드니스가 끝난 뒤 마지막에 한 번만.
- 원장은 손대지 않는다.

## 7. 메타데이터 설계 (LLM)

업로드 **전에** 제목·설명글·태그를 사연별로 설계한다 (`metadata.py`).

- 모델은 **hook(제목 앞부분)·body(설명 본문)·tags만** 공급한다. 시리즈 라벨(`｜쓰멜씬`), 면책 문구,
  출처 URL, 필수 해시태그(`#Shorts`)는 **코드가 결정적으로 부착**한다 — 모델이 귀속 정보를 빠뜨릴 수 없다.
- 모델 호출은 `codex exec --sandbox read-only`(ChatGPT 인증, 모델 오버라이드 금지). 사연 본문은
  **untrusted data**로 프롬프트에 명시한다.
- **fail-closed**: 게이트가 하나라도 실패하면 `Blocked('metadata_' + code)`로 발행을 중단한다.
  폴백 메타데이터는 **금지**한다.
- 게이트(`validate_metadata`)는 I/O 없는 순수 함수다. 검사 항목: 제목 길이(정책 상한)·시리즈 라벨 포함·
  개행/마크업(`#`/`@`)/작화 태그(`/`)/금지어 부재, 설명의 출처·면책·해시태그 포함과 길이,
  태그 개수(8..15)·중복·`#` 접두·길이.
- 정책 키: `series_label`, `metadata_title_max`, `metadata_description_max`,
  `metadata_tag_min/max/length_max`, `metadata_disclaimer`, `metadata_required_hashtag`,
  `metadata_forbidden_title_terms`, `request_cost_upper_bounds.model`.

## 8. 발행 전 게이트

통과해야 할 것 (하나라도 실패하면 업로드 시도 자체를 하지 않는다):

- `passed: true`, `full_decode_verified: true`, 기하 1080×1920, 오디오 트랙 존재
- `58 <= delivered_s × speed <= 60.15`
- sidecar의 `video_sha256`이 실제 파일 해시와 일치
- sidecar의 `speed`와 에피소드가 선언한 `speed`가 일치
- 정책·에피소드 양쪽 권리 `cleared` + 증거
- `publication_hold`가 `false`, 채널 ID 일치, `privacy_status`, 승인된 `release_slots_kst` 내 시각
- 일일 발행 한도 미초과

`audio_listening_verified`는 **실제 청취 전까지 false**로 둔다. 렌더 성공은 청취 검증이 아니다.

이 저장소의 `verify_delivery.py`는 미디어 스트림·길이·프레임·해시·디코드 검사다. 패널 머리 여백, 자막 내용/단어 정렬, 실제 청취, 2-pass 라우드니스 결과, 메타데이터·권리·발행 승인을 대신 검증하지 않는다. 각 항목은 별도 산출물과 관찰 결과로 확인하고, 렌더러 QA sidecar만으로 전체 발행 게이트를 통과시켜서는 안 된다. `metadata.py`, 업로더, 미러/백필 스크립트는 프로젝트 운영 구현의 이름이며 이 스킬에 번들된 실행 파일이 아니다. 해당 구현/정책이 없으면 그 단계는 차단하고 렌더 결과만 반환한다.

## 9. 시리즈 재생목록 편입

- 업로드 직후(`_update("processing","upload_accepted")` 다음) 영상을 시리즈 재생목록에 넣는다.
  **private+예약 상태에서 편입**하면 공개 전환 시 자동 반영된다.
- 정책은 `series_playlist_id`(고정 ID, 우선) 또는 `series_playlist_title`(동일 제목 재사용, 없으면
  **이 채널 소유**로 새로 생성) 중 하나. 둘 다 없으면 편입하지 않는다.
- **편입 실패는 업로드 클레임을 되돌리지 않는다.** `playlist_status`에 `playlist_failed_<code>`로
  별도 기록하고, `_verify_claim`이 후속 패스에서 재시도한다. 업로드 슬롯은 이미 소비된 것으로 본다.
- **편입은 멱등**: 삽입 전에 멤버십을 먼저 확인한다. 이미 들어 있으면 `playlist_verified`로 기록하고
  아무것도 삽입하지 않는다. 중복 삽입이 발생하면(예: 백필 후 `verify` 재실행) 정리한다.
- 준비 코드: `playlist_item_added`, `playlist_verified`, `playlist_complete`.

### 기존(백필) 영상

메타데이터 설계 이전에 업로드된 영상은 `backfill_episode01.py`로 처리한다:
`videos.update(part=snippet)`으로 제목·설명·태그를 교체(카테고리·언어·발행시각 등 나머지 필드는 보존)하고
재생목록 편입을 보장한다. **upload claim과 영상 상태(예약 시각 포함)는 건드리지 않는다.** 멱등이다.

## 10. 납품 미러 (Drive 백업 + Sheets 원장)

발행 부작용. 재생목록과 완전히 같은 규칙을 따른다: **업로드 클레임을 되돌리지 않는다.**

- 업로드가 `scheduled`/`*_verified`로 확인된 뒤 실행한다. 상태는 `delivery_status`,
  `drive_file_id`, `ledger_status` 컬럼에 별도 기록한다.
- 실패는 `delivery_partial`/`delivery_failed`로만 남기고 `_verify_claim`이 후속 패스에서 재시도한다.
  `delivery_mirror_enabled`가 `true`가 아니면 아무 것도 하지 않는다.
- **Drive 백업**: `drive_backup_folder_name` 폴더에 `drive_backup_artifacts`를 올린다.
  파일에는 `source_key` / `bundle_sha256` 앱 프로퍼티를 붙인다 → 같은 번들이면 재업로드하지 않고,
  번들이 바뀌었으면 업로드 후 이전 사본을 지운다.
- **Sheets 원장**: `ledger_title` 스프레드시트의 `ledger_sheet_name` 시트에 헤더 1행 + 사연 1행.
  키는 `(release_date, source_key)` — 재실행은 append가 아니라 **해당 행을 갱신**한다.
- 원장 `title`은 **실제 발행된 제목**을 쓴다. `claims.video_title`은 업로드 시 모델 제안으로 기록되지만,
  `verify`가 원격 snippet 제목을 읽어 **권위로 삼는다**(운영자가 업로드 후 제목을 바꿀 수 있다).
  불일치가 감지되면 원격 제목을 저장하고 미러를 재실행해 원장 행을 교정한다 —
  `delivery_complete`라도 제목이 어긋나면 스킵하지 않는다.
- 자격증명은 n8n Google OAuth 자격증명을 런타임에 export/refresh해 **메모리에서만** 쓴다.
  필요한 API 스코프·대상 접근 권한을 해당 자격증명에서 확인한다. 과거 실측 기록만으로 현재 계정의 재동의 불필요를 주장하지 않는다. 비밀값을 파일로 쓰지 않는다.
- CLI: `delivery_sync.py --state … --policy … --source-key … [--title|--title-file|--credential|--dry-run]`.
  제목처럼 셸 인용이 깨지는 값은 `--title-file`로 넘긴다.

## 실패 시 원칙

- 실패는 대체 경로로 넘어가지 않고 **중단**한다. 유료 생성 결과는 보존한다.
- 차단 코드·메시지를 남기고 사람이 결정하게 한다. 자동 재시도로 재과금하지 않는다.
