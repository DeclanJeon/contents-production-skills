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

## CLI 계약

아래 `python`은 Python 3.10+ 실행기다(Linux/macOS에서는 보통 `python3`, Windows에서는 `py -3`).

```
python scripts/production_history.py init --project-id ID
    [--project-root ROOT | --media-studio-root ROOT | --documents PATH]
    [--layout text|image|full]
python scripts/production_history.py set-root --path ABS [--print-only]
python scripts/production_history.py ensure-dir --project-root ROOT --name audio
python scripts/production_history.py list [--studio-root ROOT]
```

`--project-root`는 `--documents`/`--media-studio-root`와 함께 지정할 수 없다. `set-root`는 선택한 스튜디오 루트를 만들고 저장한다(`--print-only`는 미리 보기만). `ensure-dir`는 위 8개 작업 폴더 이름만 허용한다. `list`는 읽기 전용 프로젝트 목록이다.

`--project-id`는 Unicode를 보존하는 casefold slug로 정규화한다. 경로 구분자·`..`·Windows 예약 장치명을 거부한다. 동일 slug는 동일 프로젝트를 재사용하며 기존 `project.json`은 소유 ID를 확인하고 바이트 그대로 보존한다. 다른 프로젝트와 충돌하면 중단하고 별도 이름을 확인한다(날짜 접미사로 조용히 복제하지 않음).

새 스켈레톤 `project.json`(schema_version 1.1)은 staging 후 exclusive atomic link로 게시한다. 기존 정본은 덮어쓰지 않는다. init 결과는 절대 경로와 `created`/`kept`, `layout`, `existing`을 포함한다. import API는 `initialize_project(project_id, documents=None, *, project_root=None, layout="text", media_studio_root=None)`, `resolve_project_root(project_id, documents=None)`다.

```
python scripts/production_history.py record --project-root ROOT
    --operation TEXT --prompt-file FILE
    --status started|completed|interrupted|failed
    [--output PATH ...] [--operation-id ID] [--attempt N]
    [--tool NAME] [--model NAME] [--method TEXT] [--details TEXT]
    [--scope operation|project]
```

각 operation 이벤트는 UTC·로컬 타임스탬프, operation 텍스트, 파일에서 읽은 실제 프롬프트 전문(스냅샷은 `.history/prompts/`에 별도 보관, 원본 SHA-256 기록), tool/model/method, 선언된 output의 절대 경로와 존재 여부를 기록한다. `--scope operation`에는 `--prompt-file`이 필수다 — 프롬프트 없는 operation 이벤트는 거부한다.

**전이 규칙 (operation 이벤트):**

- `terminal`(`completed`/`interrupted`/`failed`)은 해당 operation_id에 pending `started`가 있을 때만 기록된다 — 시작 없는 종결은 거부된다.
- in-flight operation에 `started`를 다시 기록하면 거부된다. 종결 후 재시작만 새 attempt다. 명시 attempt ID는 operation 안에서 재사용할 수 없고, 자동 ID는 사용된 정수 중 최댓값 다음 번호를 선택한다.
- `completed`의 `--output`은 모두 프로젝트 루트 안의 실제 파일이어야 한다 — 존재하지 않는 산출물 선언은 거부된다. `failed`/`interrupted`는 미존재 output을 기록할 수 있다.
- 모든 `--output`(절대·상대)은 프로젝트 루트 안으로 해석돼야 하며 루트 밖으로 빠지면 거부된다.

`--scope project`는 프로젝트 수준 라이프사이클 이벤트(예: 최종 완료 선언)로 operations 상태와 구분된다. **project `completed`는 in-flight operation이 없고, 각 operation이 요청한 output이 디스크에 실제 존재할 때만 기록된다** — 중단(interrupted)이나 미생산 output이 남은 채 완료를 선언할 수 없다.

```
python scripts/production_history.py status --project-root ROOT
python scripts/production_history.py resume --project-root ROOT
    [--operation-id ID] [--details TEXT]
```

`status`는 operation_id별 최신 상태와 아직 terminal 이벤트가 없는 `in_flight` 목록을 JSON으로 돌려준다. 읽기 전용 조회이므로 `.history/`가 아직 없으면 빈 상태를 반환해도 폴더나 파일을 만들지 않는다. `resume`은 in-flight operation들을 명시적으로 `interrupted`로 마크하고(완료로 위장하지 않는다) `resumed` 라이프사이클 이벤트를 남긴다. `--operation-id`를 주면 해당 operation만 마크하며, in-flight가 아니면 거부한다. 이전 writer가 죽어도 lock은 OS가 해제하므로 stale lock이 재개를 막지 않는다.

모든 명령은 실제 절대 경로를 포함한 JSON 하나를 stdout에 출력하고, exit code는 0 성공 / 2 사용·프리플라이트 오류 / 1 I/O 실패다.

## 이벤트 파일 규칙

- 이름: `NNNNNN-YYYYMMDDTHHMMSSffffff-<operation-id>-<event>.md` — 정렬하면 시간 순서다. 타임스탬프는 마이크로초까지 기록해 실제 상관관계를 보존한다.
- event 종류: `started`, `completed`, `interrupted`, `failed`, `resumed`. `completed`/`interrupted`/`failed`가 terminal이다.
- 쓰기는 프로젝트별 OS advisory lock으로 직렬화된다(Windows `msvcrt`, POSIX `fcntl`). 한 writer가 다른 writer의 이벤트를 덮을 수 없고, writer가 죽으면 lock은 OS가 해제한다.
- 파일은 staging 후 atomic link로 게시되므로 프로세스가 죽어도 빈/부분 이벤트 파일이 남지 않는다. 이벤트는 불변으로 취급한다 — 수정 대신 다음 이벤트를 남긴다.
- `status.operations[ID].attempts`는 operation-scope `started` 이벤트 수이고, `current_attempt`는 실제 상관관계 ID다. 프로젝트 라이프사이클 이벤트는 이 수에 포함하지 않는다.
- 프롬프트 파일은 원본 bytes로 먼저 SHA-256을 계산한 다음 UTF-8로 decode·mask한다. JSON quoted secret 및 공백·`=`/`:` 주변 설정 형식은 비밀값만 숨긴다.
- history/events/prompts/lock과 산출물 경로는 실제 목적지까지 검사해 root 밖 symlink/junction을 거부한다. project_id·operation_id·파일명은 slug화되고 `..`/경로 구분자·예약 장치명·casefold 충돌은 거부한다.

## 언제 쓰나

- 사용자가 파일 기반 제작(스토리보드, 마스터 에셋, 생성 스펙, 영상 산출)을 요청해 실제 쓰기가 일어날 때 init을 먼저 수행하고, 각 미디어·파일 생성 작업을 record한다.
- 중간 산출물과 최종 산출물 모두 `--output`으로 등록하고 사용자에게 실제 절대 경로를 보고한다.
- 프로세스가 죽은 뒤 재진입하면 `status`로 in-flight를 확인하고 `resume`으로 중단을 명시한 뒤 작업을 다시 시작한다.

## 언제 쓰지 않나

- 채팅 전용 답변, 파일 없는 설계 논의, 단일 텍스트 산출물에는 저장 초기화를 하지 않는다(chat-only는 no-save).
- `.history`를 승인 증거·품질 판정·QA 검증·project.json 대체로 사용하지 않는다.
- 실행 증거가 없는 과거 사건은 새 `started`/`completed`로 재연하지 않는다. 사용자가 전한 과거 이력은 사용자 보고로 구분하고 원래 시각·출처·미검증 상태를 설명한다. 파일 존재는 생성 주체·방법·QA 성공의 증거가 아니다.

## 종속성

Python 3.10+ 표준 라이브러리만 사용한다. 외부 패키지 없다.

## Acceptance

An event is recordable only when it describes an operation that actually occurred and its status matches the observed outcome. Every declared output must be reported with its resolved path and existence state; completed outputs must exist within the project root. A project may be marked completed only when no operation is in flight and every requested output exists. Missing prompt, nonexistent operation, out-of-root path, or unobserved result is a blocker; never backfill an invented event.

