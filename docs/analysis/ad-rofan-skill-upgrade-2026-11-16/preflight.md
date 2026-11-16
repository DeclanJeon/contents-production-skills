# 광고·로판 스킬 업그레이드 — 실행 전 읽기 전용 점검

## 범위·승인 기록

- 2026-11-16, 사용자가 R1 설계 및 재QA 결과를 제시받은 뒤 “응 진행해줘”라고 응답했다. 직전 질문의 범위는 **이 설계로 실행 계획 작성과 검사 경로 사전점검**이었다.
- 승인된 설계 SHA-256: `dbcc3dd61fe7360abcc875db42b2b28daafb61f5614213e212df9ddc16132875`.
- 이 승인으로 영상 분석 전량 실행, 외부 업로드·새 설치·모델 다운로드·별도 과금·생성·게시를 시작하지 않았다.
- 검토된 설계 스냅샷은 보존했다. 문서의 예정 체크박스 대신 이 기록이 현재 승인 범위를 설명한다.

## 실제 확인 결과

| 경로 | 수행한 확인 | 현재 상태 | 아직 입증하지 않은 것 |
|---|---|---|---|
| FFmpeg/ffprobe | `-version`; 기존 probe 기록 재사용 | 7.0.2-static 명령 정상, Python 3.14.4 | 새 full decode·실제 프레임 검사·연속 재생 |
| Craft Anything CLI | 별도 `craft-anything-cli --help`, `commands`, `capabilities` | v0.6.0, exit0, 선언 명령322개 | 원본 영상 분석·음향 청취·영상 편집 기능 |
| Whisper | offline 환경에서 `whisper --help`; 기존 cache 파일명/크기 열거 | CLI 정상 종료, `small.pt` 483,617,219 bytes 존재 | 가중치 무결성/모델 로드·전사 실행·정확성·실제 음향 청취 |
| 실제 image read | 현재 harness가 정지 이미지 read를 제공 | 기능 선언 확인; 파일럿 미실행 | 원본별 검토·타임코드 정합·GO gate |
| 연속 동작/직접 음향 검사 | 실제로 지원되는 검사 경로 없음 | **STOP / 경로 미검증** | 모션·표정 시간 관계·발화·음악·효과음·동기 |
| 로판 기존 근거 | master head, 현재 index 포인터와 gates, count 충돌 위치를 직접 읽음 | 현재34/44 materialized, 10 unmaterialized, 전역5 gate OPEN | 현재 원본92개와 전부 해시 대응·기존 분석의 의미/품질 재검증 |

**GO/STOP 의미:** CLI 도움말 성공이나 캐시 존재는 B→C GO가 아니다. 정적 프레임 경로도 파일럿+장편 stress 검증 전에는 전량 확장 GO가 아니다. 전량 내용 분석은 현재 열리지 않았다.

## Craft Anything 경로 정정

이전 `craft-anything --help`는 103MB짜리 앱 실행 파일에 대한 호출이었으며 제한 시간 안에 반환하지 않았다. 같은 배포판에는 별도 34MB 실행 파일이 있다:

```text
/home/declan/.local/opt/craft-anything-0.6.0-linux-x86_64/bin/craft-anything-cli
```

이번에 실행한 것은 이 별도 CLI의 도움말·카탈로그뿐이다. 앱 실행 파일의 timeout 원인 자체를 진단·수리한 것은 아니다.

```bash
timeout 15s /home/declan/.local/opt/craft-anything-0.6.0-linux-x86_64/bin/craft-anything-cli --help
timeout 20s /home/declan/.local/opt/craft-anything-0.6.0-linux-x86_64/bin/craft-anything-cli --format json capabilities
timeout 20s /home/declan/.local/opt/craft-anything-0.6.0-linux-x86_64/bin/craft-anything-cli --format json commands
```

카탈로그의 17개 toolset은 native/.NET/Android/Java/웹/런타임/파일 형식 조사와 재구축 중심이다. 선언된 tool/command 이름에서 전용 video/audio/media/transcription/FFmpeg/OCR/speech/subtitle 분석 명령은 확인되지 않았다. 일반 도구로 어떤 미디어 작업도 불가능하다는 증명은 아니지만, 현재 요청의 영상/음향 검사기로 채택할 근거는 없다. ArtCraft/FilmCraft 등 다른 제품의 기능을 이 CLI에 있다고 가정하지 않는다. `chat`, `triage`, `rebuild`, `setup`, engine install 또는 MCP 등록을 실행하지 않았다.

근거: `preflight/craft-cli-help.json`, `craft-catalog-summary.json`, `craft-command-names.json`, `craft-commands-help.json`.

## Whisper 경로

```bash
HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 timeout 20s /home/declan/.local/bin/whisper --help
```

exit0이며 도움말의 기본 모델은 `turbo`, 기본 실행 장치는 `cpu`다. 기본 실행은 모델 다운로드를 유발할 수 있으므로 사용하지 않는다. 추후 승인된 ASR 검사라면 기존 `/home/declan/.cache/whisper/small.pt` 파일 경로를 명시하고, 로컬 가중치/장치를 먼저 검증해야 한다. 이번에는 모델을 로드하거나 파일에 전사하지 않았다. ASR가 성공하더라도 `HYPOTHESIS_UNVERIFIED`이며 듣기·음악/효과음·립싱크 검수와 다르다.

근거: `preflight/whisper-cli-help.json`, `versions-and-existing-cache.json`.

## 기존 로판 원장의 현재 상태

원본 경로를 수정하지 않고 다음 Linux 파일을 조회했다:

- master: `/run/media/declan/Data/Resources/AI-Rofan-Drama-2026-10-11/videos/rofan-temporal-analysis/exhaustive/semantic/archive-normalized-master-in-progress.json`
- index: 같은 `semantic/archive-semantic-index.json`.
- master의 `source_index_ref`와 `current_index_ref`는 `semantic/archive-semantic-index.json`; 아카이브의 `exhaustive` root 기준으로 해석해 실제 파일을 확인했다.
- master head: `source_occurrence_count_total=44`, `materialized_source_occurrence_count=34`.
- master 1717109행 부근: `source_occurrence_count=30`, `unmaterialized_source_occurrences=10`. 30과44/34의 충돌을 보존하며 자동 수정하지 않는다.
- master SHA-256: `f62effd762239c581992213ad4e371b79aa6c22f0682c50b921a43d563135a6e`.
- index SHA-256: `93ec30254ccf99f53695629be4eb91aee50fa0497f813ac068ee76bd8b4952b2`.

현재 index의 `global_merge_gates`에서 OPEN인 exact key:

1. `complete_scene_shot_event_crosswalk`
2. `all_visual_shot_content_checked_against_native_images`
3. `all_candidate_free transitions_and_first_last_images`
4. `all_source_scene_membership_bounds`
5. `occurrence_vs_independent_cases`

전체 값/사유는 `preflight/current-global-gates.json`의 bounded read에 보존했다. `source_occurrences_indexed`의44/44는 identity 색인 상태이지 이 다섯 gate의 닫힘이 아니다. `creator_intent`, `camera_and_gait`의 제한도 유지한다. 원장의 “active” 표기는 저장된 상태이며 현재 프로세스 실행을 확인했다는 뜻이 아니다.

master는 약122MB, index는 약206KB다. 전체 JSON을 read 도구 출력으로 받아 parse하려 하지 말고, bounded locator read 또는 승인된 로컬 구조화 처리를 사용한다. 이번 계획 조사 중 큰 register read 응답의 truncation 표식을 JSON으로 parse하려다 실패한 도구 호출이 1회 있었고, 즉시 bounded read로 전환했다. 원본 JSON 손상이나 분석 실행 실패로 해석하지 않는다.

## 다음 단계

[실행 계획](../../superpowers/plans/2026-11-16-ad-rofan-archive-skill-upgrade.md)을 검토하고 실행 방식을 선택한다. 권장은 현재 세션 직접 실행(Native)이다. 승인 후에도 먼저 인벤토리·지원 경로의 파일럿/stress를 수행하며, 미지원 모드는 STOP으로 유지한다. 전량 실제 시청각 분석을 원래 범위대로 끝내려면 미검증 검사 능력의 해결이 필요하다.
