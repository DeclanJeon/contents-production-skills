# 비-Higgsfield 연기·음성·음질 보정 후보 조사

2026-11-19. 공식 원문과 현재 세션에서 노출된 도구 스키마를 직접 대조했다. 문서/도구 노출은 계정 인증·권한·실행·품질 증거가 아니다. 설치, 업로드, 생성, 과금은 하지 않았다.

| 문제 | 확인한 원문·경로 | 한계 |
|---|---|---|
| 기존 연기의 타이밍·감정을 유지하고 음색 변경 | ElevenLabs 공식 [`voice-changer/SKILL.md`](https://github.com/elevenlabs/skills/blob/main/voice-changer/SKILL.md)는 실제 설치형 스킬이다. 입력은 기존 녹음, 출력은 선택된 기존 보이스로 변환한 음성(speech-to-speech). | 틀린 대사나 어색한 연기를 자동 수정하는 기능이 아니다. 유지 가능성은 서비스 설명이며 실제 듣고 확인한다. 이 세션에서 전용 실행 도구를 확인하지 못했으므로 설치나 API 연동은 별도다. |
| 발음·문구·감정·억양을 바꿔 짧은 구절을 다시 연기 | 현재 Fish Audio MCP의 `text_to_speech`에 `drama-3` 모델과 톤·강세·속도 지시가 노출된다. [Fish 공식 감정 문서](https://docs.fish.audio/developer-guide/core-features/emotions), [공식 모델 저장소](https://github.com/fishaudio/fish-speech). 한국어 보이스 후보는 [Typecast 공식 문서](https://typecast.ai/docs) 및 현재 Typecast MCP `generate_speech`의 감정 옵션을 참조한다. | 둘 다 기존 파형의 편집이 아니라 재발화다. 같은 승인 보이스로도 숨·톤이 이어지는지 들어봐야 한다. 로컬 Fish 모델을 고려할 때 코드/가중치의 라이선스 조건을 모델별로 확인한다. |
| 음질: 잡음·치찰음·레벨 | 로컬 [FFmpeg 필터 원문](https://github.com/FFmpeg/FFmpeg/blob/master/doc/filters.texi)과 설치 바이너리에서 `afftdn`, `deesser`, `acompressor`, `loudnorm` 확인. 심한 음성 잡음에는 [DeepFilterNet](https://github.com/Rikorose/DeepFilterNet) 후보. | FFmpeg 필터 노출만 확인했으며 청취 검증은 미수행. DeepFilterNet은 48 kHz WAV용 `deep-filter` 경로를 문서로 확인했으며 설치/실행하지 않았다. 숨·속삭임·룸톤이 과도하게 손상되는지 전후 청취한다. |
| Foley/환경음·효과음 부족 | ElevenLabs 공식 [`sound-effects/SKILL.md`](https://github.com/elevenlabs/skills/blob/main/sound-effects/SKILL.md). 별도 SFX 생성 후 큐에 맞춰 배치. | 노이즈 제거, 원본 대사 복원, 실제 장면과의 자동 싱크가 아니다. |
| 영상 속 연기 또는 입 모양 | [Runway 공식 API](https://docs.dev.runwayml.com/api/#tag/Start-generating/paths/~1v1~1character_performance/post)에서 `character_performance` 후보 확인. [LatentSync](https://github.com/bytedance/LatentSync)는 음성 조건부 립싱크 구현이다. | Runway는 캐릭터 연기 생성 후보로, 이미 채택한 컷의 표정만 보정한다고 검증되지 않았다. LatentSync는 Agent Skill이 아니며 GPU·가중치·라이선스·정체성 보존 검증이 필요하다. 실행·품질 미확인. |

## 통합 제안

새 공급자별 스킬을 전부 설치하거나 이를 하나의 만능 스킬로 취급하기보다, 기존 `video-production-assets`의 [최소 발음 교정](../../video-production-assets/references/29-reference-driven-production.md#dialogue-repair), [대사·립싱크](../../video-production-assets/references/22-dialogue-lipsync.md), [편집·사운드](../../video-production-assets/references/09-edit.md)를 재사용한다. `creative-production`은 실제 결함의 타임코드·보존 요소를 기록하고 다음 순서로 가장 덜 바뀌는 경로를 선택한다.

1. 연기와 대사가 맞으면 음질만 로컬 처리한다. 음색만 다르면 권한이 있는 speech-to-speech 후보를 검토한다.
2. 발음·감정이 틀리면 동의된 기존 보이스의 최소 구절을 재발화하거나 짧게 ADR 녹음한다. 입이 실제 보이고 유의한 싱크 불일치가 있을 때만 별도 립싱크를 검토한다.
3. 영상의 시선·몸 연기가 원인이면 음성 보정으로 덮지 않는다. 기존 테이크/대체 커버리지를 먼저 비교하고, 권한 안에서 필요한 컷만 재작업한다.
4. 원본은 유지하고 타임라인에 수정 범위를 기록한다. 동일한 청취 레벨에서 원본과 비교하고 발음·음색·감정·룸톤·입·전후 컷을 재검수한다. 채택 후 나머지 제작은 계속하고 사용자 검수는 전편 편집·QA 이후 요청한다. 실제 얼굴·음성 참조 업로드, 음색 복제, 비용은 권리와 실행 권한 확인이 별도다.

가장 작은 검증은 권리 확보된 10–15초 한국어 대사 장면에서 (a) 잡음만 있는 원본, (b) 발음/감정 오류가 있는 원본을 분리해 비교하는 것이다. (a)는 로컬 정리, (b)는 구절 교체를 먼저 비교하고, 입이 보이는 컷에서만 립싱크 필요성을 판단한다. 이 조사는 해당 시험을 수행하거나 설계·스킬에 실행 경로를 탑재한 결과가 아니다.
