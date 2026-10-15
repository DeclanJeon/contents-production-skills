# 서버 운영

파이프라인을 원격 호스트(예: `ssh pons`, Ubuntu)에서 무인으로 돌리는 구성.

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

## 비밀값

- TTS 키는 **디스크 정책 파일에 넣지 않는다**. root 소유 `provider.env`(0600)로만 주입하고,
  배포 시 ssh stdin으로 넣는다(인자·로그·채팅에 노출 금지).
- 로컬에서는 Windows 자격증명 관리자 등 런타임 저장소에서 읽어 프로세스에 넘긴다.
- 운영 후 키를 회전한다.

## systemd

- `youtube-community-shorts.service` — oneshot, `User=root`, `ExecStart=<venv>/bin/python <release>/app/runner.py`,
  `WorkingDirectory=<release>`. `TimeoutStartSec`은 넉넉히(웹툰 18페이지 + 경계 패스 + 배속 패스).
- `youtube-community-shorts.timer` — `OnBootSec`, `OnUnitInactiveSec`로 주기 실행.
- **`OnUnitInactiveSec` 타이머는 서비스가 systemd로 한 번도 실행된 적이 없으면 다음 시각이 없다**
  (`systemctl list-timers`가 `NEXT=-`, `NextElapseUSecMonotonic=infinity`). `enable --now`만으로는
  발화하지 않는다. `sudo systemctl start youtube-community-shorts.service`로 1회 실행해
  `InactiveEnterTimestamp`를 만들면 그 시점부터 주기가 성립한다. 서비스는 멱등이므로 안전하다.
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

## 배포 전 확인

- 렌더러가 서버에서 필요한 모듈만 쓰는지(정지 렌더는 표준 라이브러리 + ffmpeg + PIL).
  TTS 어댑터가 `requests`/`soundfile`/`numpy`를 쓰면 venv에 설치돼 있어야 한다.
- ffmpeg/ffprobe 존재, 폰트 경로 존재.
- 에피소드 원장·패널·WAV·템플릿이 릴리스에 모두 들어갔는지.
- 첫 실행은 실제로 돌려 보고 소요 시간·메모리를 실측한다. 추정으로 상한을 정하지 않는다.
