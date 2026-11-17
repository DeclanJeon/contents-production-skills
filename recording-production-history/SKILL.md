---
name: recording-production-history
version: 1.19
description: "Use when content production writes intermediate or final files, when a project needs a chronological audit of actual prompts, methods and outputs, or when interrupted production must be resumed."
---

# 제작 이력 기록

## 이 스킬이 하는 일

실제 파일이 만들어지는 제작 작업이 시작될 때 프로젝트 저장 루트를 초기화하고, 각 생성·검사·납품 작업을 `.history/events/`의 순차적 Markdown 이벤트로 기록한다. 이벤트는 파일 이름 순서가 시간 순서와 일치하는 append-only 기록이며, 중단된 실행은 `status`가 in-flight로 노출하고 `resume`이 중단과 재개를 명시적으로 남긴다. 완료를 꾸미지 않는다.

**`.history`는 감사 기록이지 승인 원장이 아니다.** `<project-root>/project.json`이 정본이며 이 도구는 init 이후 그 파일을 쓰지 않는다. 이 스킬은 산출물의 품질·QA·승인을 판정하지 않는다 — 이벤트 기록은 검수 통과가 아니며, 승인·검수 상태는 기존 계약과 검증 도구가 담당한다. 조정자(orchestrator)가 이 도구를 호출해 각 단계의 사실을 남긴다.

## 저장 위치 (cross-platform)

기본은 실제 사용자 Documents 아래 `Media_Studio/<project-id-slug>`다. Windows는 알려진 Documents 폴더(리디렉션·OneDrive 포함), macOS는 `~/Documents`, Linux는 XDG Documents 설정 또는 `~/Documents`를 사용한다. 사용자명은 하드코드하지 않는다.

실제 파일을 처음 저장하기 전에 **원하는 프로젝트 디렉터리가 있는지 한 번 묻는다**. 명시적으로 선택한 현재 프로젝트, `MEDIA_STUDIO_ROOT`, 저장된 설정 또는 이미 존재하는 기본 스튜디오 루트로 확인되면 다시 묻지 않는다. 새 기본 루트를 선택하면 생성 후 재사용한다. 채팅 전용 작업은 경로나 파일을 만들지 않는다.

경로 선택:
1. `--project-root ROOT`: 프로젝트 폴더 그대로 사용(slug를 덧붙이지 않음).
2. `--media-studio-root ROOT`: 이번 호출의 스튜디오 루트 아래 slug.
3. `MEDIA_STUDIO_ROOT` 환경 변수 → `set-root` 저장 설정 → 실제 Documents의 `Media_Studio`.
4. `--documents PATH`는 Documents 위치를 명시하며, 환경/저장 설정이 없을 때 `PATH/Media_Studio/<slug>`로 해석한다. `STUDIO_DOCUMENTS_DIR`도 Documents 탐지 override다.

설정은 `XDG_CONFIG_HOME/media-studio/config.json` 또는 `~/.config/media-studio/config.json`에 저장한다. 기존 프로젝트는 명시적으로 지정해 재사용하며 자동 이동·이름 변경하지 않는다. 산출물은 스킬 저장소 밖에 둔다.

## 프로젝트 레이아웃

쓰는 폴더만 만든다: `source/`(원본·시놉·대본), `bible/`, `storyboards/`(샷 카드 포함), `assets/`, `audio/`, `edit/`, `qa/`. **최종 납품본은 `final/`에 모은다.** `.history/`는 감사 기록, 루트의 `project.json`은 정본이다.

`init --layout text`(기본)는 `source/`만 만든다. `image`는 source/bible/storyboards/assets/qa, `full`은 모든 작업 폴더를 만든다. 프리셋은 실제 그 폴더들을 사용하는 작업에만 선택하고, 보통은 기본 init 후 필요한 폴더를 `ensure-dir`로 만든다. 이미 `project.json`이 있으면 프리셋 폴더를 추가하지 않고 누락된 감사 폴더만 보완한다.

## 짧은 사용 인터페이스

첫 실제 저장/이벤트 쓰기·중단 복구에서는 [CLI 정본](references/cli-contract.md)의 해당 명령·상태 전이·원자성/루트 안전 계약을 먼저 읽는다. 조회만이면 status/list 해당 절만 필요하다. 아래는 축약 인터페이스이며 실제 prompt/output과 상태를 생략할 허가가 아니다.

```bash
python3 scripts/production_history.py init --project-id ID --project-root ROOT
python3 scripts/production_history.py status --project-root ROOT
python3 scripts/production_history.py record --project-root ROOT --operation TEXT --prompt-file FILE --status started
python3 scripts/production_history.py resume --project-root ROOT
```

실제 작업 전 started, 이후 관찰한 completed/failed/interrupted를 같은 operation ID/attempt로 연결한다. terminal에는 pending 시작이 필요하고 완료 output은 루트 안의 실제 파일이어야 한다. timeout/중단은 공급자 실패가 아니며 원격 job 상태를 확인하기 전 재제출하지 않는다. project completed는 in-flight 0과 요청 output 실제 존재가 필요하다. 단일 기록자·불변 이벤트·비밀값 마스킹·OS lock/원자 게시와 정확한 옵션/오류 코드는 CLI 정본대로 유지한다.

## 언제 쓰나

- 사용자가 파일 기반 제작(스토리보드, 마스터 에셋, 생성 스펙, 영상 산출)을 요청해 실제 쓰기가 일어날 때 init을 먼저 수행하고, 각 미디어·파일 생성 작업을 record한다.
- 중간 산출물과 최종 산출물 모두 `--output`으로 등록하고 사용자에게 실제 절대 경로를 보고한다.
- 프로세스가 죽은 뒤 재진입하면 `status`로 in-flight를 확인하고 `resume`으로 중단을 명시한 뒤 작업을 다시 시작한다.

## 언제 쓰지 않나

- 채팅 전용 답변·파일 없는 논의·명시적 no-save/read-only에는 저장 초기화를 하지 않는다. 단일 텍스트라도 MD/PDF 저장을 명시적으로 요청했으면 허용된 파일 단계와 이력만 기록하며 새 미디어는 만들지 않는다.
- `.history`를 승인 증거·품질 판정·QA 검증·project.json 대체로 사용하지 않는다.
- 실행 증거가 없는 과거 사건은 새 `started`/`completed`로 재연하지 않는다. 사용자가 전한 과거 이력은 사용자 보고로 구분하고 원래 시각·출처·미검증 상태를 설명한다. 파일 존재는 생성 주체·방법·QA 성공의 증거가 아니다.

## 종속성

Python 3.10+ 표준 라이브러리만 사용한다. 외부 패키지 없다.

## Acceptance

An event is recordable only when it describes an operation that actually occurred and its status matches the observed outcome. Every declared output must be reported with its resolved path and existence state; completed outputs must exist within the project root. A project may be marked completed only when no operation is in flight and every requested output exists. Missing prompt, nonexistent operation, out-of-root path, or unobserved result is a blocker; never backfill an invented event.

