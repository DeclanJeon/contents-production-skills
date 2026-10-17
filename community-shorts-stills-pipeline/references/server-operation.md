# 서버 운영

파이프라인을 원격 호스트(예: `ssh pons`, Ubuntu)에서 무인으로 돌리는 구성.

범위/근거: 아래는 별도 운영 프로젝트의 배포 runbook이며 설치된 스킬의 현 서버 관찰이나 번들 구현 보증이 아니다. 호스트·경로·CLI 버전·스코프·egress·멱등성·상태 코드는 해당 배포에서 직접 확인해야 한다. 로그인/설정 변경/배포/루프 기동/업로드/게시/Drive·Sheets 변경은 각각 승인된 범위에서만 실행한다. 읽기 전용 감사에서는 명령을 실행하지 않는다. `publication_hold`를 유지하고 원격 실행 정책을 확인하기 전에는 서비스·타이머·컨테이너를 시작하지 않는다.

## 디렉터리

```
/opt/youtube-community-shorts/
  releases/<release>/{app,episode,renderer,skills}
  venv/bin/python
/etc/youtube-community-shorts/{policy.json,sources.json,provider.env}
/var/lib/youtube-community-shorts/
  state/{runs.sqlite3,latest.json,discovered-sources.json,runner.lock,jobs/,publication/}
  generation/                 # 작업 홈, .codex/skills 는 releases/<release>/skills 심볼릭
```

- `app/`는 러너·프로듀서·퍼블리셔, `renderer/`는 렌더러, `episode/`는 원장+패널+WAV+템플릿.
- `/etc/...`는 root 0700. `provider.env`도 root 0600.

## 정책 파일 (policy.json)

파이프라인 동작을 바꾸는 값들. 특히:

| 키 | 의미 |
| --- | --- |
| `renderer_path` | 배포된 렌더러 스크립트 경로 |
| `renderer_mode` | `scene_card` 또는 `webtoon_page` |
| `renderer_template_path` | `webtoon_page`일 때 에피소드 웹툰 템플릿 |
| `renderer_template_path`의 `channel_label` | 화면에 burn되는 채널명. **바이트 권위는 이 파일**이며, 프레임을 눈으로 읽은 값이 아니다 |
| `speed` | 렌더 후 배속(예: `1.4`). 원장은 60초 그대로 |
| `font_path` | burn-in 폰트 (예: `/usr/share/fonts/truetype/nanum/NanumGothicBold.ttf`) |
| `source_rights_status` / `source_rights_evidence` | 권리 게이트 |
| `typecast_voice_id` / `typecast_model` | TTS 고정 |
| `paid_generation_enabled`, `episode_cost_limit`, `daily_cost_limit`, `cost_currency` | 유료 생성 상한 |
| `max_tts_requests` / `max_model_calls` / `max_image_requests`, `request_cost_upper_bounds`, `request_cost_evidence` | 요청 수·비용 상한 |
| `publication_hold` | `false`여야 발행 진행 |
| `expected_channel_id`, `privacy_status`, `release_slots_kst`, `daily_publish_limit` | 발행 대상·시각 |
| `n8n_container`, `youtube_credential_id` | n8n YouTube OAuth |
| `series_label` | 제목 뒤에 붙는 시리즈 라벨 (예: `쓰멜씬`) |
| `series_playlist_title` / `series_playlist_id` | 시리즈 재생목록 (제목으로 재사용·생성, 또는 고정 ID) |
| `metadata_title_max`, `metadata_description_max` | 제목·설명 길이 상한 |
| `metadata_tag_min/max/length_max` | 태그 개수·길이 상한 |
| `metadata_disclaimer`, `metadata_required_hashtag`, `metadata_forbidden_title_terms` | 코드가 부착/검사하는 고정 문자열 |
| `request_cost_upper_bounds` | 요청당 상한. `model` 키로 LLM 호출도 상한에 포함 |
| `youtube_playlists_disabled` | `true`면 재생목록 편입을 건너뛴다 |
| `delivery_mirror_enabled` | `true`면 납품 미러(Drive 백업 + Sheets 원장)를 수행 |
| `google_credential_id` | n8n Google OAuth 자격증명 ID (Drive + Sheets 공용) |
| `drive_backup_folder_name` | 납품본 백업 폴더명 (없으면 생성) |
| `drive_backup_artifacts` | 백업할 파일명 목록 (예: `video.mp4`, `media-qa.json`, `render-manifest.json`) |
| `ledger_title` / `ledger_sheet_name` | 발행 원장 스프레드시트 제목 / 시트 이름 |
| `ledger_spreadsheet_id` | 고정 스프레드시트 ID(없으면 제목으로 검색·생성하고 상태에 기억) |

## 납품 미러 (Drive + Sheets)

- `delivery_sync.py`가 발행 **후**에 돈다(재생목록 편입과 같은 위치·같은 규칙). 업로드 클레임을 되돌리지 않는다.
- 자격증명은 n8n 컨테이너에서 `google_credential_id`를 export해 `refresh_token → access_token`으로 교환하며
  **메모리에서만** 쓴다. 파일로 쓰지 않는다.
- Sheets 생성·쓰기는 실제 자격증명에 필요한 스코프와 대상 접근 권한이 있을 때만 가능하다. 과거 “스코프 실측/재동의 불필요” 기록은 현재 계정 증거가 아니다. 스코프를 비밀값 노출 없이 확인하고 부족하면 사용자 승인 절차로 차단한다.
- 점검 순서: `--dry-run`으로 폴더·아티팩트·제목을 먼저 확인하고, 실제 실행 후 재실행해
  `drive_verified`와 원장 행 수 불변(헤더 + 1행)을 확인한다.
- 실패 코드: `drive_http_403`(자격증명/스코프), `drive_no_artifacts`(아티팩트 없음),
  `ledger_http_400`(URL/본문 형태 — append는 `values/…:append`여야 한다), `ledger_http_403`(시트 접근).

## 메타데이터 LLM (Codex)

- 실행 파일: `/opt/youtube-community-shorts/tools/codex/node_modules/.bin/codex` (0.162.1).
- `producer`가 `HOME=<generation home>`을 넘겨 실행한다. 따라서 인증은 **`/var/lib/youtube-community-shorts/generation/.codex/auth.json`(0600, owner shorts-generation)** 에 둔다 — `/root/.codex`가 아니다.
- **ChatGPT 인증은 로컬과 공유하지 않는다.** 같은 OAuth 토큰을 두 호스트가 쓰면 리프레시 회전으로 상대가 무효화된다. 서버 전용 자격을 쓴다.
- API 키 인증이면 `codex login --with-api-key`(stdin)로 `auth.json`에 top-level `OPENAI_API_KEY`를 넣고, 키는 `provider.env`(0600)에 둔다. 0.162.1은 `wire_api="chat"` 설정을 제거했다 — 구버전 설정을 복사하지 말 것.
- `-c model=...` 오버라이드 금지: ChatGPT 계정에서는 400 `not supported when using Codex with a ChatGPT account`.
- 인증이 없으면 `run`은 `Blocked('metadata_…')`로 멱등 종료한다(폴백 없음).
- **Codex I/O는 반드시 generation 워크스페이스에 둔다.** `design_metadata`는 스키마·프롬프트·출력
  메시지를 실행기의 `workspace`(`<job>/generation`, `shorts-generation` 소유)에 쓴 뒤
  결과물만 `provider-results`(root 소유 멱등 원장)로 복사한다. Codex는 비권한 계정으로 돌기 때문에
  root 소유 `0700` 디렉터리에는 **쓸 수 없다** — 그곳에 직접 쓰면 매 회차
  `Blocked('metadata_model_packet_missing')`으로 멈춘다(`metadata_executor.workspace`가 스테이징 위치).
- 서버 egress/인증 도달 가능성은 현재 환경에서 확인한다. bare curl의 403/421만으로 정상이나 장애를 확정하지 않는다.
- **전용 계정 device-auth 절차**(사용자 확정 방식; 백그라운드로 돌리고 코드를 사람에게 전달):

```bash
ssh pons 'sudo -n rm -f /tmp/codex-device.log; sudo -n bash -c "nohup runuser -u shorts-generation -- \
  env -i HOME=/var/lib/youtube-community-shorts/generation PATH=/usr/local/bin:/usr/bin:/bin LANG=C.UTF-8 \
  /opt/youtube-community-shorts/tools/codex/node_modules/.bin/codex login --device-auth \
  > /tmp/codex-device.log 2>&1 &"; sleep 10; sudo -n cat /tmp/codex-device.log'
```

  로그의 URL과 일회용 코드(15분 만료)를 사람에게 전달한다. 승인 후
  `sudo -n ls -la /var/lib/youtube-community-shorts/generation/.codex/auth.json`이
  0600·owner `shorts-generation`인지 확인한다. 만료되면 로그를 지우고 다시 띄운다.
  **로컬 `~/.codex/auth.json`을 복사하지 않는다**(리프레시 회전으로 상호 무효화).

## 비밀값

- TTS 키는 **디스크 정책 파일에 넣지 않는다**. root 소유 `provider.env`(0600)로만 주입하고,
  배포 시 ssh stdin으로 넣는다(인자·로그·채팅에 노출 금지).
- 로컬에서는 Windows 자격증명 관리자 등 런타임 저장소에서 읽어 프로세스에 넘긴다.
- 운영 후 키를 회전한다.

## systemd

- `youtube-community-shorts.service` — oneshot, `User=root`, `ExecStart=<venv>/bin/python <release>/app/runner.py`,
  `WorkingDirectory=<release>`. `TimeoutStartSec`은 넉넉히(웹툰 18페이지 + 경계 패스 + 배속 패스).
- `youtube-community-shorts.timer` — `OnBootSec`, `OnUnitInactiveSec`로 주기 실행.
- 먼저 설치된 unit과 systemd 버전을 확인하고 `systemctl cat` / `systemctl show` / `systemctl list-timers`로 실제 스케줄과 상태를 읽는다. 이 패키지에는 운영 unit/runner 구현이 없으므로 특정 서버의 `NEXT=-` 원인이나 중복 방지를 확정하지 않는다.
- 직접 읽은 [systemd.timer 공식 문서](https://www.freedesktop.org/software/systemd/man/latest/systemd.timer.html#OnActiveSec=) (systemd 262, Options의 시작점 표·복수 지시자·과거 OnBootSec 규칙, `READ-PARTIAL`, 2026-10-16)는 `OnUnitInactiveSec`를 대상 unit의 마지막 비활성화 기준으로 정의한다. **다른 지시자도 함께 적용**되며, 이미 지난 `OnBootSec`/`OnStartupSec`는 timer 활성화 때 즉시 발화할 수 있다. `enable --now`가 실행하지 않는다고 가정하지 않는다.
- 수동 start나 timer 활성화도 생성·지출·게시를 유발할 수 있다. 실제 unit, 실행 정책·중복/재조정 구현과 해당 동작의 승인을 확인하기 전에는 실행하지 않는다. 멱등성 주장은 권한이나 안전성의 증거가 아니며, `NEXT=-`만 보고 서비스 강제 실행을 권하지 않는다.
- 리소스 상한이 있으면(`MemoryMax`, `CPUQuota`) 인코딩이 죽지 않는지 첫 실측에서 확인하고 조정한다.
- 릴리스 경로를 바꾸면 두 유닛의 경로를 함께 고치고 `daemon-reload` → `timer` 재시작.

## 차단 목록(probe)

읽기 전용으로 정책이 부족한 항목을 나열한다. 전형적으로: 권리 미확인, `publication_hold`,
YouTube 자격증명 없음, 채널 미설정, 릴리스 정책 미설정, 생성 예산 미설정, TTS 음성 미선택, TTS 인증 없음.
배포 후 이 목록이 비어야 자동 발행이 가능하다.

## 배포 절차

1. 로컬에서 릴리스 tar를 만든다(`app`, `episode`, `renderer`, `skills` 각각).
2. ssh로 임시 디렉터리에 풀고 `sudo mv`로 `releases/<release>/`에 안착.
3. 정책 파일을 갱신하고 `provider.env`를 주입한다.
4. 유닛 경로 갱신 → `daemon-reload` → 타이머 재시작.
5. `runner.py probe`로 차단 목록 확인. 비어 있으면 자동 발행만 남는다.

## 도커 컴포즈 배포 (설치 CLI)

`11_AUTOMATION/deploy/docker/`가 같은 파이프라인을 도커 컴포즈로 올린다. `install.py`가 13단계로
정책·비밀값·자격증명·볼륨·릴리스 자산을 대화형으로 받아 적용하고 스택을 기동한다.

```sh
cd 11_AUTOMATION/deploy/docker
python3 install.py                 # 최초 설치는 반드시 대화형
python3 install.py --non-interactive --skip-up   # 재적용(설정 복구 경로)
```

- 컨테이너는 `ycs-pipeline-bot`(root, 도커 소켓, `n8n-data` ro 마운트)과 `ycs-n8n`(n8n).
  n8n UI는 `127.0.0.1:${YCS_N8N_PORT:-5679}` — 호스트에 이미 n8n이 5678을 쥐고 있어서다.
- `entrypoint.sh`가 systemd 유닛과 동일하게 root·`umask 0077`·`provider.env` source·
  900초 루프·비정상 종료가 루프를 죽이지 않음을 재현한다.
- Google 자격증명은 stdin으로 n8n에 import되고 고정 id(`youtube-account`,`google-drive-account`)로
  upsert되므로 재실행해도 행이 늘지 않는다. Codex는 `--device-auth`로 사람이 브라우저 승인 —
  **`auth.json`을 호스트 간 복사하지 말 것**(refresh token이 회전해 다른 호스트가 로그아웃된다).
- `N8N_ENCRYPTION_KEY`는 `.env`에 1회 생성·보존된다. 잃으면 저장된 refresh token을 복호화할 수 없다.
- 검증: `docker compose exec pipeline-bot ycs-entrypoint {probe,verify,test}`.
  빈 호스트에서 `verify`가 `publication_not_found`를 내는 것은 정상이다(발행 이력이 없으므로).
- **함정**: 봇 기본 명령이 `loop`이고 `restart: unless-stopped`다. 검증용 스택은 `docker stop`이
  아니라 `docker compose down`으로 내려야 한다. 재부팅 시 되살아나 실 채널에 발행을 시작한다.


## 배포 전 확인

- 렌더러가 서버에서 필요한 모듈만 쓰는지(정지 렌더는 표준 라이브러리 + ffmpeg + PIL).
  TTS 어댑터가 `requests`/`soundfile`/`numpy`를 쓰면 venv에 설치돼 있어야 한다.
- ffmpeg/ffprobe 존재, 폰트 경로 존재.
- 에피소드 원장·패널·WAV·템플릿이 릴리스에 모두 들어갔는지.
- 첫 실행은 실제로 돌려 보고 소요 시간·메모리를 실측한다. 추정으로 상한을 정하지 않는다.
