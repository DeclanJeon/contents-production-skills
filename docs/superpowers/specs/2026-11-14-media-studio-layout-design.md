# Media_Studio 프로젝트 저장 레이아웃 재설계

## 1. 의도와 이유

콘텐츠 제작 스킬은 산출물을 저장할 때마다 프로젝트 폴더에 **고정 21개 디렉터리 트리**(`00_MANIFEST`…`10_DELIVERY` + `02_MASTER_ASSETS/*` 10개)를 사용 여부와 무관하게 전부 생성한다. 그 결과:

- 실제 프로젝트 루트가 21개 이상의 폴더로 부풀고, 절반 이상이 빈 폴더로 남는다.
- 프로젝트가 늘수록 사용자가 무엇이 최종 산출물이고 무엇이 중간물인지 알 수 없다.
- 저장 루트가 `studio_production` 하나로 고정되어, 사용자가 원하는 프로젝트 경로를 지정할 방법이 없고 이미 쓰던 폴더가 있어도 다시 만든다.
- 실제 관찰: `~/Documents/studio_production/` 아래 항목 36개, 그중 여러 프로젝트에서 `02_BIBLE`·`03_SCENE_PACKS`·`05_SHOT_CARDS`·`07_AUDIO`가 0개. `pokemon-ai-short`는 다른 이름(`01_SOURCES`/`09_REPORT`), 루트에는 `01_최종아웃풋`·`02_레퍼런스영상`이라는 별도 구조, `_MASTER-LOG.md` 예외 파일까지 공존한다.

목표: **사용자가 한 번 정한 프로젝트 경로에서, 꼭 필요한 디렉터리만, 단순한 이름으로 만들고, 중간산출물·최종산출물·작업 히스토리를 분리해 한눈에 관리되게 한다.** Linux·macOS·Windows 모두에서 동작한다.

## 2. 목표 / 비목표 / 안티골

**목표**
- 유저가 프로젝트 경로를 미리 지정하면 그곳에서 작업한다 (`--project-root` 우선).
- 지정이 없으면 기본은 실제 사용자 Documents 아래 `Media_Studio`. 이미 있으면 다시 만들지 않는다.
- 프로젝트 폴더는 slug 하나. 같은 이름으로 다시 호출하면 새 폴더를 만들지 않고 기존 폴더를 이어 쓴다(멱등).
- 디렉터리 이름은 번호 없는 단순 명사: `source/ bible/ storyboards/ assets/ audio/ edit/ qa/ final/`.
- 디렉터리는 **실제로 처음 쓰일 때만** 생성한다(지연 생성).
- 중간산출물과 최종산출물을 분리한다: 최종은 `final/`, 나머지는 작업 폴더, 히스토리는 `.history/`.
- 첫 실행 시 "따로 원하는 프로젝트 디렉터리가 있냐"고 한 번 묻고, 답을 기억해 다시 묻지 않는다.

**비목표**
- 기존 36개 프로젝트의 자동 마이그레이션(원하면 별도 작업).
- `project.json` 원장 스키마 변경. `schema_version: 1.1`을 그대로 유지한다.
- 납품 ZIP의 안정적인 내부 패키지 레이아웃 변경(`package_production.py`의 `00_MANIFEST`…`10_DELIVERY` 투영은 배포 산출물 규격으로 존속).
- 승인·검수·품질 판정 로직 변경. `.history`는 여전히 감사 기록이지 승인 원장이 아니다.

**안티골**
- "사용 안 하는 빈 폴더 생성"이 다시 생기면 실패다.
- 이미 존재하는 사용자 폴더/프로젝트를 덮어쓰거나 이름을 바꾸면 실패다.
- 새 레이아웃이 기존 프로젝트나 기존 도구를 깨뜨리면 실패다.

## 3. 제약

- Python 3.10+ 표준 라이브러리만 사용(기존 도구 계약).
- 사용자 홈/이름 하드코드 금지. `Windows`: `SHGetKnownFolderPath(FOLDERID_Documents)` → 레지스트리 → `~/Documents`. `macOS`: `~/Documents`. `Linux`: XDG `user-dirs.dirs` → `~/Documents`.
- 경로는 root 밖 symlink/junction·`..` 탈출을 거부한다(기존 `_assert_managed_path`/`_resolve_inside` 재사용).
- 출력 JSON 하나 + exit 0/2/1 계약 유지.
- 기존 `--documents`, `STUDIO_DOCUMENTS_DIR`, `--project-root` 동작 호환.

## 4. 접근 (검토한 대안)

| 안 | 구조 | 장점 | 단점 |
|---|---|---|---|
| A 최소 3층 | `source/ work/ final/ _history/`, `work/` 안에 세부 | 루트가 가장 단순(4개) | 실제 자료 찾기가 한 단계 깊어짐 |
| **B 타입별 폴더(채택)** | `source/ bible/ storyboards/ assets/ audio/ edit/ qa/ final/` | 이름만 보고 찾음, 지연 생성으로 빈 폴더 0 | 폴더 종류가 8개 |
| C 번호 유지 | 기존 `04_STORYBOARDS` 유지 + 지연 생성 | 기존 프로젝트 호환 최고 | "단순한 이름" 요구에 미달, 번호가 여전히 존재 |

**채택: B.** 대안 A는 최종/중간 분리는 명확하지만 `work/` 아래로 들어가야 해 "쉽게 찾기"가 약하고, C는 사용자가 없애려는 번호 체계를 그대로 둔다. B는 이름이 곧 내용물이며, 지연 생성과 결합하면 실제로 쓰는 폴더만 남는다.

## 5. 결정 사항 (사용자가 확정)

- **루트**: 기본 `<Documents>/Media_Studio`, 한 번만 만들고 있으면 재사용.
- **프로젝트 폴더**: `<주제>-<길이>` slug 1개, 멱등(있으면 재사용, 중복 생성 금지). 충돌 시에만 `-YYYYMMDD`.
- **분리**: 최종=`final/`, 중간=작업 폴더, 히스토리=`.history/`(숨김 이름 유지 — 기존 도구/테스트가 이 경로에 묶여 있음).
- **기존 프로젝트**: 건드리지 않음. 새 프로젝트부터 새 레이아웃.
- **호환**: Linux/macOS/Windows 전부.

## 6. 최종 레이아웃

```
<Documents>/Media_Studio/                ← 스튜디오 루트 (최초 1회 생성, 있으면 보존)
└── <project-slug>/                      ← 프로젝트 = 폴더 1개
    ├── project.json                     ← 정본 원장 (기존 1.1 그대로)
    ├── source/                          ← 사용자 제공 자료·원본·시놉·대본·비트
    ├── bible/                           ← LOOK·스타일·월드 바이블
    ├── storyboards/                     ← 보드·패널·시트·(하위)샷 카드
    ├── assets/                          ← 마스터·생성 이미지/영상 원본 (하위 scenes/ 등)
    ├── audio/                           ← 음성·음악·SFX
    ├── edit/                            ← 애니매틱·컷 편집
    ├── qa/                              ← 검수 근거
    ├── final/                           ← 최종 납품본만
    └── .history/                        ← 감사 기록 (events/, prompts/)
```

**지연 생성 규칙**
- `init`은 항상 `project.json`, `.history/{events,prompts}`, `source/`만 만든다.
- `--layout text|image|full` 프리셋:
  - `text`(기본): `source/`
  - `image`: `source/ bible/ storyboards/ assets/ qa/`
  - `full`: `source/ bible/ storyboards/ assets/ audio/ edit/ qa/ final/`
- `ensure-dir --name <dir>`로 필요한 작업 폴더를 그때 만든다.
- 파일을 쓰는 도구는 부모 폴더를 자동 생성한다(안전망).

**"이미 사용 중이면 다시 만들지 않음"**
- 스튜디오 루트: 디렉터리가 이미 있으면 그대로 쓴다. 없을 때만 만든다.
- `project.json`이 이미 있는 루트: `init`은 **레이아웃 폴더를 새로 만들지 않는다**(기존 프로젝트 보존). `.history`가 없을 때만 만든다.

**경로 선택 순서 (묻지 않을 조건 포함)**
1. `--project-root PATH` (프로젝트 단위 최우선)
2. 환경 변수 `MEDIA_STUDIO_ROOT` (절대 경로)
3. 설정 캐시 `~/.config/media-studio/config.json`의 `media_studio_root` (`XDG_CONFIG_HOME` 존중, `set-root`가 기록할 때만 생성)
4. `<Documents>/Media_Studio`
환경/캐시/기존 루트로 결정되면 **다시 묻지 않는다.** 아무것도 없어 처음 만드는 경우에만 코디네이터가 "따로 원하는 경로가 있냐"고 1회 묻고, 다른 경로를 원하면 `set-root`로 캐시에 저장한다.

## 7. 코드 변경 범위

| 파일 | 책임 |
|---|---|
| `recording-production-history/scripts/studio_layout.py` (신규) | slug/경로 안전, Documents 탐지, 스튜디오 루트 해석·설정 캐시, 프리셋, `ensure_work_dir`, `initialize_layout`, `resolve_project_root` |
| `recording-production-history/scripts/production_history.py` | `initialize_project`가 layout에 위임, `--layout`/`--media-studio-root`/`set-root`/`ensure-dir`/`list` CLI 추가 |
| `recording-production-history/scripts/test_production_history.py` | 새 레이아웃·멱등·경로 해석 테스트로 갱신 |
| `recording-production-history/scripts/test_studio_layout.py` (신규) | studio_layout 모듈 단위 테스트 |
| `recording-production-history/SKILL.md` | 저장 위치·CLI 계약·언제 쓰나 갱신 |
| `creative-production/SKILL.md`, `references/production-routing.md` | `studio_production` → `Media_Studio`, 경로 질문 1회 규칙 |
| `creative-production/references/workspace-integration.md` | 경로 저장 규칙 |
| `video-production-assets/references/preproduction-review.md` | 기본 루트·경로 예시 |
| `video-production-assets/references/contract.md` | 경로 예시(`01_SOURCE`→`source` 등) |
| `video-production-assets/references/storyboard-contract.md`, `storyboard-sheet-user-guide.md`, `stickman-animatic.md` | `--output` 경로 예시 새 이름 |
| `README.md`, `USAGE_GUIDE.md`, `CHANGELOG.md`, `manifest.json` | 문서·버전 |

**변경하지 않는 것**: `video-production-assets/scripts/package_production.py`의 납품 패키지 내부 투영(배포 규격), `validate_*`(base_dir 상대경로라 레이아웃 무관), `project.json` 스키마.

## 8. 남은 판단(빌더 재량)

- `set-root`/`list`를 이번에 넣을지. → `set-root`는 UX상 필요(다시 묻지 않기), `list`는 읽기 전용 편의.
- `--layout` 기본값. → `text`(가장 가벼움).
- 스튜디오 루트 표식 파일은 두지 않는다. "이미 사용 중"은 디렉터리 존재로 판정한다.
