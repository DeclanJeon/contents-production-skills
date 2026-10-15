# 배속 전달 (Delivery speed)

배속은 **원장 변경이 아니라 완성 마스터의 타임베이스 변경**이다.

## 왜 렌더 후인가

기존 게이트가 강제한다:

| 게이트 | 조건 |
|---|---|
| 내레이션 준비 | `58 <= elapsed <= 60` |
| 최종 영상 계약 | `58 <= actual <= 60.15` 이고 `abs(actual - elapsed) <= 0.15` |
| 발행 | QA `actual_duration_s`가 `58 <= d <= 60.15` |

따라서 `target_duration_s=60`, 18개 샷 윈도우, `audio_cues`, `captions`는 그대로 두고, 저장된 마스터를 검증한 **뒤에** 배속 패스를 적용한다. 원장 델타는 없다.

## 규칙

- 마스터는 항상 `BASE_DURATION_S = 60.0`으로 제작한다.
- 배속 허용 범위 `SPEED_MIN..SPEED_MAX = 0.25..4.0`. 비유한값·불리언·범위 밖은 거부.
- 허용 오차 `SPEED_TOLERANCE_S = 0.15`.
- 필터: 비디오 `setpts=PTS/<speed>`, 오디오 `atempo=<speed>` — **반드시 함께** 적용.
- 1.4배속 납품본: 약 42.857 s, 약 1286 프레임.

## 인코더 패딩 함정 (중요)

여러 개의 AAC 클립을 concat한 마스터는 각 클립의 인코더 패딩이 누적된다. 디코더는 이 패딩을 **전부** 돌려주므로 오디오 디코드 길이가 비디오보다 길어진다(실측 예: 비디오 60.000 s, 오디오 디코드 60.674 s, 컨테이너 60.023 s — 0.65 s 차이). 그대로 `atempo`를 걸면 납품 오디오가 비디오보다 0.45 s 긴 **무음 꼬리**를 갖는다.

대응:

1. **마스터 단계**에서 concat 결과의 두 스트림을 각각 `trim`/`atrim`으로 60.000 s에 묶고 다시 인코딩한다.
2. **배속 패스**에서도 두 스트림을 각각의 선언된 길이로 다시 묶은 뒤 필터를 걸고 `-t <expected>`로 출력을 자르고, 결과에서 `abs(audio - video) <= 0.15`와 `abs(audio - source_audio/speed) <= 0.15`를 검사한다.

## QA 필드

배속을 적용한 납품본의 사이드카(`*.qa.json`)는 다음을 담는다:

| 필드 | 의미 |
|---|---|
| `runtime_seconds`, `frames` | **납품본** 실측 |
| `master_runtime_seconds`, `master_frames` | 원장 60 s 기준 마스터 |
| `speed` | 적용 배속 |
| `target_runtime_seconds` | `60/speed` |
| `full_decode_verified` | 전체 디코드 통과 |
| `audio_listening_verified` | 실제 청취 전에는 **항상 false** |

## 발행 게이트 연동

발행기가 42.86 s 납품본을 받아들이려면 발행기의 길이 게이트를 넓혀야 한다: `abs(duration * speed - elapsed) <= 0.15`도 허용하되 나머지 게이트는 그대로 유지한다.
