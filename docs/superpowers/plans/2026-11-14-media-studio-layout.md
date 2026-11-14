# Media_Studio 프로젝트 저장 레이아웃 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 산출물 저장 루트를 `<Documents>/Media_Studio`로 바꾸고, 프로젝트마다 쓰이는 디렉터리만 지연 생성하며, 멱등 init과 경로 1회 질문으로 중복 디렉터리 생성을 없앤다.

**Architecture:** 순수 로직(slug·경로 안전·Documents 탐지·스튜디오 루트 해석·레이아웃 프리셋·init)을 새 모듈 `studio_layout.py`로 옮기고, `production_history.py`는 이벤트 스토어와 CLI만 담당하도록 얇게 만든다. 새 레이아웃은 v5.1 21개 폴더 트리를 대체하되 `project.json` 스키마와 납품 ZIP 내부 패키지 트리는 건드리지 않는다.

**Tech Stack:** Python 3.10+ 표준 라이브러리, `unittest` + `pytest` 실행.

**Spec:** `docs/superpowers/specs/2026-11-14-media-studio-layout-design.md`

## Resumed execution status (2026-11-14)

- [x] Tasks 1–6 implemented in existing commits 259cfc3 through b10ae52.
- [x] Task 7 documentation updated in place; shared dirty user edits preserved.
- [x] Task 8 working-tree package 2.34 and 22 skill versions; post-review Linux suite 806 passed / 4 Windows-only skips / 524 subtests.
- [x] Boundary fixes verified RED→GREEN; six-job OS/Python CI matrix added.
- [x] One authorized independent current-file review; six findings reproduced and addressed in one fix pass, plus environment-restoration regression.
- [ ] Actual agent-behavior pressure validation (static instruction inspection only).
- [ ] Actual macOS/Windows CI results; no push/submission performed.
- [ ] Additional Git commits (not performed in resumed session).

Evidence: [validation report](../../../qa/2026-11-14-media-studio-layout-validation.md). Earlier step checkboxes below are the original execution recipe, not a claim of unobserved tests or commits.

## Global Constraints

- Python 3.10+ 표준 라이브러리만 사용. 새 외부 의존성 금지.
- 이 머신의 인터프리터는 `python3`. 테스트는 저장소 루트에서 `python3 -m pytest <path> -q`로 실행한다.
- 사용자 홈/이름을 하드코드하지 않는다.
- Documents 해석: Windows `SHGetKnownFolderPath(FOLDERID_Documents)` → winreg → `~/Documents`; macOS `~/Documents`; Linux `XDG_DOCUMENTS_DIR`(`user-dirs.dirs`) → `~/Documents`.
- 모든 명령은 stdout에 JSON 객체 하나를 출력하고 exit code는 0 성공 / 2 사용·프리플라이트 오류 / 1 I/O 실패.
- `..`·경로 구분자·Windows 예약 장치명·casefold 충돌을 거부하고, root 밖 symlink/junction 탈출을 거부한다.
- `project.json` 스키마는 변경하지 않는다(`schema_version: 1.1` 유지).
- 기존 사용자 파일을 덮어쓰거나 기존 프로젝트 폴더를 이름 변경/이동하지 않는다.
- `.history` 이름은 유지한다. 감사 기록이며 승인 원장이 아니다.
- `video-production-assets/scripts/package_production.py`의 패키지 내부 트리 매핑(`00_MANIFEST`…`10_DELIVERY`)은 배포 규격이므로 수정하지 않는다.
- 이 저장소에는 사용자의 기존 미커밋 변경이 있다. 보존하고, 이 계획의 파일만 커밋한다.

## Review Focus

1. **기존 프로젝트에 재실행한 init** — 사용자는 아무 변화 없는 no-op을 기대한다. 실패 모드: 제거된 v5.1 폴더를 다시 만들거나 `project.json`을 재작성함. Task 5가 `existing` 감지 시 레이아웃 폴더 생성 0을 테스트로 고정한다.
2. **사용자가 이미 만들어 둔 `Media_Studio` 디렉터리** — 사용자는 재사용을 기대한다(오류 아님, 재생성 없음). 실패 모드: 존재를 오류로 처리하거나 내용 삭제. Task 5의 루트 재사용 테스트가 담당한다.
3. **`--project-root`를 상대경로/`~`/Documents 밖으로 지정** — 사용자는 `~` 확장과 절대경로, 중첩 `Media_Studio` 없음을 기대한다. 실패 모드: 상대경로를 cwd 기준으로 오해석하거나 기본 루트를 덧붙임. Task 5가 담당한다.
4. **Windows 리디렉션/OneDrive Documents 또는 대소문자만 다른 이름** — 사용자는 알려진 폴더를 따르고 대소문자만 다른 두 프로젝트가 생기지 않기를 기대한다. 실패 모드: 하드코드 `~/Documents` 또는 casefold 미적용. Task 2·3이 담당한다.
5. **init이 만든 폴더에 없는 디렉터리에 도구가 먼저 쓰기** — 예: `assets/`가 아직 없는데 시트 렌더러가 `assets/sheets/x.png`에 쓰기. 사용자는 자동 생성 후 성공을 기대한다. 실패 모드: `FileNotFoundError`. Task 5의 `ensure_parent`와 Task 7의 도구 안내, Task 6의 `ensure-dir`가 담당한다.

---

### Task 1: 순수 로직 모듈 `studio_layout.py` 분리

**Files:**
- Create: `recording-production-history/scripts/studio_layout.py`
- Modify: `recording-production-history/scripts/production_history.py`
- Test: `recording-production-history/scripts/test_studio_layout.py`

**Interfaces:**
- Consumes: 없음(기존 `production_history.py`의 순수 함수를 그대로 옮김).
- Produces: `UsageError(ValueError)`, `slugify(value: str, field: str) -> str`, `_SLUG_BAD/_SLUG_RUNS/_WINDOWS_RESERVED`, `_windows_documents(env, home)`, `_linux_documents(env, home)`, `detect_documents(platform=None, env=None, home=None) -> Path`, `STUDIO_DIRNAME: str`, `resolve_project_root(project_id, documents=None) -> Path`(임시 v1 동작, Task 5에서 교체).

- [ ] **Step 1: 실패 테스트 작성** — `test_studio_layout.py`

```python
"""studio_layout: path/naming/Documents helpers shared with the CLI."""
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import studio_layout as sl  # noqa: E402


class SlugTests(unittest.TestCase):
    def test_casefolds_and_strips_separators(self):
        self.assertEqual(sl.slugify('Demo Film', 'project_id'), 'demo-film')
        self.assertEqual(sl.slugify('DemoFilm', 'project_id'),
                         sl.slugify('demofilm', 'project_id'))

    def test_rejects_traversal_and_reserved(self):
        for bad in ('..', 'a/b', 'a\\b', 'CON', '.'):
            with self.assertRaises(sl.UsageError):
                sl.slugify(bad, 'project_id')


class DocumentsTests(unittest.TestCase):
    def test_linux_uses_xdg_when_configured(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            cfg = home / '.config'
            cfg.mkdir()
            (cfg / 'user-dirs.dirs').write_text(
                'XDG_DOCUMENTS_DIR="$HOME/Eigene Dokumente"\n', encoding='utf-8')
            self.assertEqual(
                sl.detect_documents(platform='linux', env={}, home=home),
                home / 'Eigene Dokumente')

    def test_darwin_and_fallback_use_home_documents(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            self.assertEqual(
                sl.detect_documents(platform='darwin', env={}, home=home),
                home / 'Documents')

    def test_env_override_wins(self):
        with tempfile.TemporaryDirectory() as tmp:
            env = {'STUDIO_DOCUMENTS_DIR': str(Path(tmp) / 'Elsewhere')}
            self.assertEqual(
                sl.detect_documents(platform='linux', env=env,
                                    home=Path('/nonexistent-home')),
                Path(tmp) / 'Elsewhere')


if __name__ == '__main__':
    unittest.main()
```

- [ ] **Step 2: 실패 확인**

Run: `python3 -m pytest recording-production-history/scripts/test_studio_layout.py -q`
Expected: FAIL — `ModuleNotFoundError: No module named 'studio_layout'`

- [ ] **Step 3: 모듈 구현** — `production_history.py`에서 아래를 잘라 `studio_layout.py`로 옮기고, 원본에서 제거한다.

`studio_layout.py`는 다음을 담는다: 모듈 docstring(순수 로직임을 명시), `from __future__ import annotations`, `import os, re, sys, json`, `from pathlib import Path`, `class UsageError(ValueError)`, `_SLUG_BAD`, `_SLUG_RUNS`, `_WINDOWS_RESERVED`, `slugify`, `_windows_documents`, `_linux_documents`, `detect_documents`, `STUDIO_DIRNAME = "studio_production"`, 임시 `resolve_project_root`:

```python
def resolve_project_root(project_id: str,
                         documents: str | os.PathLike | None = None) -> Path:
    """Absolute default storage root: <Documents>/studio_production/<slug>."""
    slug = slugify(project_id, "project_id")
    base = Path(documents).expanduser() if documents else detect_documents()
    return (base / STUDIO_DIRNAME / slug).resolve()
```

`production_history.py` 상단 import에 `from studio_layout import (UsageError, slugify, detect_documents, resolve_project_root, STUDIO_DIRNAME)`를 추가하고, 옮긴 정의를 지운다. `production_history`에서 `ph.slugify`/`ph.detect_documents`/`ph.resolve_project_root`/`ph.UsageError`/`ph.STUDIO_DIRNAME`을 쓰던 기존 테스트가 계속 통과하도록 `production_history`가 이 이름들을 재노출해야 한다(모듈 속성으로 남아 있으면 됨).

- [ ] **Step 4: 통과 확인 (신규 + 기존 회귀)**

Run: `python3 -m pytest recording-production-history/scripts/test_studio_layout.py recording-production-history/scripts/test_production_history.py -q`
Expected: PASS — 신규 테스트 전부 + 기존 48개 통과

- [ ] **Step 5: 커밋**

```bash
git add recording-production-history/scripts/studio_layout.py \
        recording-production-history/scripts/test_studio_layout.py \
        recording-production-history/scripts/production_history.py
git commit -m "refactor(history): extract path/naming helpers into studio_layout"
```

---

### Task 2: Documents 탐지 위임 (동작 보존)

**Files:**
- Modify: `recording-production-history/scripts/studio_layout.py`
- Test: `recording-production-history/scripts/test_studio_layout.py`

**Interfaces:**
- Consumes: Task 1의 `detect_documents`, `_windows_documents`, `_linux_documents`.
- Produces: `detect_documents`는 그대로지만 구현이 `STUDIO_DOCUMENTS_DIR` → OS별 탐지 → `~/Documents` 순으로 명시화된다.

- [ ] **Step 1: 실패 테스트 작성** — `test_studio_layout.py`에 추가

```python
class DetectionPrecedenceTests(unittest.TestCase):
    def test_explicit_env_beats_platform_default(self):
        with tempfile.TemporaryDirectory() as tmp:
            env = {'STUDIO_DOCUMENTS_DIR': str(Path(tmp) / 'Chosen')}
            self.assertEqual(
                sl.detect_documents(platform='darwin', env=env, home=Path(tmp)),
                Path(tmp) / 'Chosen')

    def test_relative_env_override_is_ignored(self):
        with tempfile.TemporaryDirectory() as tmp:
            env = {'STUDIO_DOCUMENTS_DIR': 'relative/path'}
            self.assertEqual(
                sl.detect_documents(platform='darwin', env=env, home=Path(tmp)),
                Path(tmp) / 'Documents')
```

- [ ] **Step 2: 실패 확인**

Run: `python3 -m pytest recording-production-history/scripts/test_studio_layout.py::DetectionPrecedenceTests -q`
Expected: 상대경로 무시 테스트가 FAIL(상대 경로 그대로 반환) 또는 두 테스트 모두 PASS면 Step 3에서 명시화만 하고 Step 4로 진행. 현재 구현이 절대 경로일 때만 반환하므로 둘 다 PASS할 수 있다 — 그 경우 이 테스트는 회귀 고정용이다.

- [ ] **Step 3: 구현 정리** — `detect_documents`에 docstring으로 우선순위를 명시하고, `override`가 절대 경로일 때만 채택(비절대는 무시하고 계속 탐지)하는 동작을 유지·주석한다. `_windows_documents`의 `is_absolute()` 검사와 winreg fallback을 확인한다.

- [ ] **Step 4: 통과 확인**

Run: `python3 -m pytest recording-production-history/scripts/test_studio_layout.py -q`
Expected: PASS

- [ ] **Step 5: 커밋**

```bash
git add recording-production-history/scripts/studio_layout.py \
        recording-production-history/scripts/test_studio_layout.py
git commit -m "test(history): pin Documents detection precedence"
```

---

### Task 3: 경로 안전 helper 이동

**Files:**
- Modify: `recording-production-history/scripts/studio_layout.py`, `recording-production-history/scripts/production_history.py`
- Test: `recording-production-history/scripts/test_studio_layout.py`

**Interfaces:**
- Consumes: Task 1의 `UsageError`, `slugify`.
- Produces: `assert_managed_path(root: Path, target: Path) -> None`(구 `_assert_managed_path`), `resolve_inside(root: Path, raw: str, field: str) -> Path`(구 `_resolve_inside`). `production_history.py`는 `assert_managed_path`만 알면 된다.

- [ ] **Step 1: 실패 테스트 작성** — 추가

```python
class PathSafetyTests(unittest.TestCase):
    def test_assert_managed_path_rejects_escape(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / 'proj'
            root.mkdir()
            with self.assertRaises(sl.UsageError):
                sl.assert_managed_path(root, root.parent / 'outside.txt')

    def test_resolve_inside_keeps_relative_under_root(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / 'proj'
            root.mkdir()
            self.assertEqual(sl.resolve_inside(root, 'assets/x.png', 'output'),
                             (root / 'assets/x.png').resolve())

    def test_resolve_inside_rejects_absolute_outside(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / 'proj'
            root.mkdir()
            with self.assertRaises(sl.UsageError):
                sl.resolve_inside(root, str(Path(tmp) / 'elsewhere.png'), 'output')
```

- [ ] **Step 2: 실패 확인**

Run: `python3 -m pytest recording-production-history/scripts/test_studio_layout.py::PathSafetyTests -q`
Expected: FAIL — `AttributeError: module 'studio_layout' has no attribute 'assert_managed_path'`

- [ ] **Step 3: 구현** — `_assert_managed_path`/`_resolve_inside`를 각각 `assert_managed_path`/`resolve_inside`로 이름을 바꿔 `studio_layout.py`로 옮긴다. `production_history.py`의 호출부를 `assert_managed_path(...)`로 갱신하고, `_resolve_inside` 호출부는 `resolve_inside(...)`로 갱신한다.

- [ ] **Step 4: 통과 확인**

Run: `python3 -m pytest recording-production-history/scripts/test_studio_layout.py recording-production-history/scripts/test_production_history.py -q`
Expected: PASS

- [ ] **Step 5: 커밋**

```bash
git add recording-production-history/scripts/studio_layout.py \
        recording-production-history/scripts/production_history.py \
        recording-production-history/scripts/test_studio_layout.py
git commit -m "refactor(history): move managed-path guards into studio_layout"
```

---

### Task 4: 스튜디오 루트 해석 + 설정 캐시

**Files:**
- Modify: `recording-production-history/scripts/studio_layout.py`, `recording-production-history/scripts/production_history.py`
- Test: `recording-production-history/scripts/test_studio_layout.py`

**Interfaces:**
- Consumes: Task 1~3.
- Produces:
  - `MEDIA_STUDIO_DIRNAME = "Media_Studio"`
  - `config_path(env=None, home=None) -> Path`
  - `read_config(env=None, home=None) -> dict`
  - `write_config(data: dict, env=None, home=None) -> Path` (부모 폴더 생성, 임시파일→원자 교체)
  - `detect_studio_root(documents=None, env=None, home=None) -> tuple[Path, str | None]` — `(root, explicit_request)`; `explicit_request`는 사용자/환경이 명시했으면 그 설명 문자열, 기본값이면 `None`
  - `ensure_studio_root(root: Path) -> bool` — 생성했으면 `True`, 이미 있었으면 `False`

- [ ] **Step 1: 실패 테스트 작성** — 추가

```python
class StudioRootTests(unittest.TestCase):
    def test_media_studio_root_env_wins(self):
        with tempfile.TemporaryDirectory() as tmp:
            docs = Path(tmp) / 'Docs'
            env = {'MEDIA_STUDIO_ROOT': str(Path(tmp) / 'Mine')}
            root, explicit = sl.detect_studio_root(
                documents=docs, env=env, home=Path(tmp))
            self.assertEqual(root, (Path(tmp) / 'Mine').resolve())
            self.assertIsNotNone(explicit)

    def test_default_is_documents_media_studio(self):
        with tempfile.TemporaryDirectory() as tmp:
            docs = Path(tmp) / 'Docs'
            root, explicit = sl.detect_studio_root(
                documents=docs, env={}, home=Path(tmp))
            self.assertEqual(root, (docs / 'Media_Studio').resolve())
            self.assertIsNone(explicit)

    def test_config_cache_is_read_when_no_env(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            env = {}
            sl.write_config(
                {'media_studio_root': str(home / 'Cached')}, env=env, home=home)
            root, explicit = sl.detect_studio_root(
                documents=home / 'Docs', env=env, home=home)
            self.assertEqual(root, (home / 'Cached').resolve())
            self.assertIsNotNone(explicit)

    def test_ensure_studio_root_does_not_recreate(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / 'Media_Studio'
            self.assertTrue(sl.ensure_studio_root(root))
            self.assertTrue(root.is_dir())
            (root / 'keep.txt').write_text('keep')
            self.assertFalse(sl.ensure_studio_root(root))
            self.assertEqual((root / 'keep.txt').read_text(), 'keep')
```

- [ ] **Step 2: 실패 확인**

Run: `python3 -m pytest recording-production-history/scripts/test_studio_layout.py::StudioRootTests -q`
Expected: FAIL — `AttributeError: module 'studio_layout' has no attribute 'detect_studio_root'`

- [ ] **Step 3: 구현**

```python
MEDIA_STUDIO_DIRNAME = "Media_Studio"

def config_path(env=None, home=None) -> Path:
    env = os.environ if env is None else env
    home = Path(home) if home is not None else Path.home()
    base = env.get("XDG_CONFIG_HOME")
    config_dir = Path(base) if base else home / ".config"
    return config_dir / "media-studio" / "config.json"

def read_config(env=None, home=None) -> dict:
    try:
        data = json.loads(config_path(env, home).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return data if isinstance(data, dict) else {}

def write_config(data: dict, env=None, home=None) -> Path:
    path = config_path(env, home)
    path.parent.mkdir(parents=True, exist_ok=True)
    stage = path.with_name(f".config.json.stage-{os.getpid()}-{os.urandom(4).hex()}")
    try:
        with open(stage, "x", encoding="utf-8") as handle:
            json.dump(data, handle, indent=2, ensure_ascii=False)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(stage, path)
    finally:
        stage.unlink(missing_ok=True)
    return path

def detect_studio_root(documents=None, env=None, home=None) -> tuple[Path, str | None]:
    env = os.environ if env is None else env
    override = env.get("MEDIA_STUDIO_ROOT")
    if override:
        return Path(override).expanduser().resolve(), f"MEDIA_STUDIO_ROOT={override}"
    cached = read_config(env, home).get("media_studio_root")
    if isinstance(cached, str) and cached.strip():
        return Path(cached).expanduser().resolve(), "saved studio root"
    base = Path(documents) if documents else detect_documents(env=env, home=home)
    return (base / MEDIA_STUDIO_DIRNAME).resolve(), None

def ensure_studio_root(root: Path) -> bool:
    """Create the studio root only if absent; True if created."""
    if root.is_dir():
        return False
    root.mkdir(parents=True, exist_ok=True)
    return True
```

`production_history.py`에 `set-root` 지원용으로 `studio_layout.write_config`가 이미 여기 있다. `STUDIO_DOCUMENTS_DIR`는 기존 `detect_documents`가 계속 처리한다(우선순위: `MEDIA_STUDIO_ROOT` > `STUDIO_DOCUMENTS_DIR`/OS 기본 > `Media_Studio`).

- [ ] **Step 4: 통과 확인**

Run: `python3 -m pytest recording-production-history/scripts/test_studio_layout.py -q`
Expected: PASS

- [ ] **Step 5: 커밋**

```bash
git add recording-production-history/scripts/studio_layout.py \
        recording-production-history/scripts/test_studio_layout.py
git commit -m "feat(history): resolve Media_Studio root with config cache"
```

---

### Task 5: 지연 생성 레이아웃 + 멱등 init

**Files:**
- Modify: `recording-production-history/scripts/studio_layout.py`, `recording-production-history/scripts/production_history.py`
- Test: `recording-production-history/scripts/test_studio_layout.py`, `recording-production-history/scripts/test_production_history.py`

**Interfaces:**
- Consumes: Task 1~4.
- Produces:
  - `LAYOUT_PRESETS: dict[str, tuple[str, ...]]` — `{"text": ("source",), "image": ("source","bible","storyboards","assets","qa"), "full": ("source","bible","storyboards","assets","audio","edit","qa","final")}`
  - `HISTORY_DIRNAME = ".history"`, `EVENTS_DIRNAME = "events"`, `PROMPTS_DIRNAME = "prompts"`, `PROJECT_JSON = "project.json"`
  - `WORK_DIRS: tuple[str, ...]` — `("source","bible","storyboards","assets","audio","edit","qa","final")`
  - `initialize_layout(root: Path, project_id: str, layout: str = "text") -> dict` — `{"project_root", "studio_root", "project_id", "layout", "created": [...], "kept": [...], "history_dir", "existing": bool}`
  - `ensure_work_dir(root: Path, name: str) -> Path` — 이름 검증 후 생성/보존, 경로 반환
  - `resolve_project_root(project_id, documents=None, env=None, home=None) -> Path` — Task 1의 임시 구현을 `(detect_studio_root(...)[0] / slug).resolve()`로 교체
  - `list_projects(root: Path) -> list[dict]` — `[{"project_id","project_root","layout","files"}]`

- [ ] **Step 1: 실패 테스트 작성** — `test_studio_layout.py`에 추가

```python
class InitializeLayoutTests(unittest.TestCase):
    def test_text_layout_creates_only_source(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / 'proj'
            result = sl.initialize_layout(root, 'Demo Film')
            self.assertTrue((root / 'source').is_dir())
            self.assertTrue((root / 'project.json').is_file())
            self.assertTrue((root / '.history' / 'events').is_dir())
            for absent in ('bible', 'assets', 'final', 'audio', 'edit', 'qa'):
                self.assertFalse((root / absent).exists(), absent)
            self.assertEqual(result['layout'], 'text')
            self.assertFalse(result['existing'])

    def test_image_preset_creates_expected_dirs_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / 'proj'
            sl.initialize_layout(root, 'Demo', layout='image')
            for present in ('source', 'bible', 'storyboards', 'assets', 'qa'):
                self.assertTrue((root / present).is_dir(), present)
            for absent in ('audio', 'edit', 'final'):
                self.assertFalse((root / absent).exists(), absent)

    def test_reinit_on_existing_project_is_noop(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / 'proj'
            sl.initialize_layout(root, 'Demo', layout='full')
            ledger_bytes = (root / 'project.json').read_bytes()
            result = sl.initialize_layout(root, 'Demo', layout='full')
            self.assertTrue(result['existing'])
            self.assertEqual(result['created'], [])
            self.assertEqual((root / 'project.json').read_bytes(), ledger_bytes)
            self.assertEqual((root / 'source').is_dir(), True)

    def test_ensure_work_dir_is_idempotent(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / 'proj'
            sl.initialize_layout(root, 'Demo')
            first = sl.ensure_work_dir(root, 'assets')
            self.assertTrue(first.is_dir())
            self.assertEqual(sl.ensure_work_dir(root, 'assets'), first)
            with self.assertRaises(sl.UsageError):
                sl.ensure_work_dir(root, '../escape')
```

- [ ] **Step 2: 실패 확인**

Run: `python3 -m pytest recording-production-history/scripts/test_studio_layout.py::InitializeLayoutTests -q`
Expected: FAIL — `AttributeError: module 'studio_layout' has no attribute 'initialize_layout'`

- [ ] **Step 3: 구현** — `studio_layout.py`에 상수와 함수 추가.

```python
HISTORY_DIRNAME = ".history"
EVENTS_DIRNAME = "events"
PROMPTS_DIRNAME = "prompts"
PROJECT_JSON = "project.json"
WORK_DIRS = ("source", "bible", "storyboards", "assets", "audio", "edit", "qa", "final")
LAYOUT_PRESETS = {
    "text": ("source",),
    "image": ("source", "bible", "storyboards", "assets", "qa"),
    "full": WORK_DIRS,
}

def _skeleton(project_id: str) -> dict:
    return {"schema_version": "1.1", "project_id": project_id, "version": "v001",
            "target_duration_s": None, "fps": None, "aspect_ratio": None,
            "scenes": [], "characters": [], "shots": [], "claims": [],
            "artifacts": [], "asset_registry": []}

def _write_skeleton_exclusive(root: Path, project_id: str) -> None:
    project_file = root / PROJECT_JSON
    stage = root / f".project.json.stage-{os.getpid()}-{os.urandom(4).hex()}"
    try:
        with open(stage, "x", encoding="utf-8") as handle:
            json.dump(_skeleton(project_id), handle, indent=2, ensure_ascii=False)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.link(stage, project_file)
    except FileExistsError:
        raise UsageError(
            f"project.json appeared during initialization; preserved: {project_file}")
    finally:
        stage.unlink(missing_ok=True)
```

`initialize_layout`의 로직:
1. `slug = slugify(project_id, "project_id")`; `layout`이 `LAYOUT_PRESETS`에 없으면 `UsageError`.
2. `project_file = root / PROJECT_JSON`; `assert_managed_path(root, project_file)`.
3. `existing = project_file.exists()`. 존재하면: 기존 JSON을 읽어 `project_id` slug가 다르면 `UsageError`(기존 동작 유지). `created=[]`, `kept=[PROJECT_JSON]`.
4. `root.mkdir(parents=True, exist_ok=True)`.
5. `existing`이면 프리셋 폴더를 **만들지 않는다**(`kept`에 이미 있는 것만 기록). 아니면 프리셋의 각 rel을 `assert_managed_path` 후 없을 때만 `mkdir`,`created`/`kept` 기록.
6. `.history/{events,prompts}`는 없을 때만 만든다(기존 프로젝트에도 부족분은 보완 — 감사 기록 필수).
7. `existing`이 아니면 `_write_skeleton_exclusive`로 스켈레톤 게시,`created`에 `PROJECT_JSON`.
8. 반환 dict(`studio_root`=`root.parent`).

`ensure_work_dir`:
```python
def ensure_work_dir(root: Path, name: str) -> Path:
    slug = slugify(name, "work dir")
    if slug not in WORK_DIRS:
        raise UsageError(f"unknown work dir: {name!r} (expected one of {WORK_DIRS})")
    target = root / slug
    assert_managed_path(root, target)
    target.mkdir(parents=True, exist_ok=True)
    return target
```

`resolve_project_root` 교체:
```python
def resolve_project_root(project_id, documents=None, env=None, home=None) -> Path:
    root, _ = detect_studio_root(documents=documents, env=env, home=home)
    return (root / slugify(project_id, "project_id")).resolve()
```

`list_projects`:
```python
def list_projects(root: Path) -> list[dict]:
    if not root.is_dir():
        return []
    rows = []
    for child in sorted(root.iterdir()):
        ledger = child / PROJECT_JSON
        if not child.is_dir() or not ledger.is_file():
            continue
        work_dirs = [d for d in WORK_DIRS if (child / d).is_dir()]
        rows.append({"project_id": child.name, "project_root": str(child),
                     "layout": work_dirs, "files": sum(1 for p in child.rglob('*') if p.is_file())})
    return rows
```

- [ ] **Step 4: `production_history.initialize_project`를 위임으로 교체**

`production_history.py`의 `initialize_project` 본문을 `studio_layout.initialize_layout` 호출로 바꾼다. 시그니처는 `initialize_project(project_id, documents=None, *, project_root=None, layout="text", media_studio_root=None) -> dict`로 확장한다.
- `media_studio_root`가 주어지면 그 절대 경로 아래 `slug`로 root 결정.
- `project_root`가 주어지면 그대로(중첩 없음).
- 둘 다 아니면 `resolve_project_root(project_id, documents)`.
- `--documents`와 `--project-root` 동시 지정은 여전히 `UsageError`.
- 기존 반환 키(`project_root`, `documents`, `project_id`, `created`, `kept`, `history_dir`)를 유지하고 `studio_root`, `layout`, `existing`을 추가한다. `documents`는 `str(root.parent)`(기존 테스트가 `root.parent.parent`를 기대하면 Task 6에서 갱신).

기존 `PACKAGE_DIRS`는 `production_history.py`에 남기지 말고 `studio_layout`이 레이아웃을 소유한다. 기존 테스트가 `ph.PACKAGE_DIRS`를 참조하면 Task 6에서 제거한다.

- [ ] **Step 5: 통과 확인**

Run: `python3 -m pytest recording-production-history/scripts/test_studio_layout.py -q`
Expected: PASS (InitializeLayoutTests 포함)

- [ ] **Step 6: 커밋**

```bash
git add recording-production-history/scripts/studio_layout.py \
        recording-production-history/scripts/production_history.py \
        recording-production-history/scripts/test_studio_layout.py
git commit -m "feat(history): lazy Media_Studio layout with idempotent init"
```

---

### Task 6: CLI 배선 + 기존 테스트 갱신

**Files:**
- Modify: `recording-production-history/scripts/production_history.py`
- Test: `recording-production-history/scripts/test_production_history.py`

**Interfaces:**
- Consumes: Task 5의 `initialize_project(..., layout=, media_studio_root=)`, `ensure_work_dir`, `list_projects`, `write_config`, `detect_studio_root`.
- Produces CLI:
  - `init --project-id ID [--documents PATH | --project-root ROOT] [--media-studio-root PATH] [--layout text|image|full]`
  - `set-root --path PATH` — 설정 캐시에 저장(절대경로), 결과 JSON에 저장 경로
  - `ensure-dir --project-root ROOT --name DIR`
  - `list [--media-studio-root PATH | --documents PATH]`
  - 기존 `record`/`status`/`resume`는 그대로.

- [ ] **Step 1: 기존 테스트 갱신** — `test_production_history.py`

`InitTests`에서:
- 기본 루트 기대값을 `Path(tmp) / 'studio_production' / 'demo-film'` → `Path(tmp) / 'Media_Studio' / 'demo-film'`로 바꾼다.
- `for rel in ph.PACKAGE_DIRS:` 전체 폴더 검사 블록을 제거하고, `self.assertTrue((root / 'source').is_dir())`로 대체한다.
- `(root / '02_BIBLE' / 'style_world_bible.md')` 작성/검증을 `(root / 'bible' / 'style_world_bible.md')`로 바꾼다(단, 재실행 프로젝트에서는 `bible/`이 없을 수 있으므로 `(root / 'bible').mkdir(parents=True, exist_ok=True)`를 먼저 하거나 `source/`로 대체).
- `documents` 키 기대값을 새 반환에 맞춘다.
- `test_explicit_project_root_...`에서 `assertFalse((selected / 'studio_production').exists())`는 유지하고 `assertFalse((selected / 'Media_Studio').exists())`도 추가한다.
- `CliSmokeTests`의 기본 루트 기대값 `Path(tmp) / 'studio_production' / 'smoke-test'`를 `Path(tmp) / 'Media_Studio' / 'smoke-test'`로 바꾼다.

- [ ] **Step 2: 실패 확인**

Run: `python3 -m pytest recording-production-history/scripts/test_production_history.py -q`
Expected: FAIL — `Media_Studio` 기대 vs `studio_production` 실제, `ensure-dir`/`set-root`/`list` 미구현

- [ ] **Step 3: 신규 CLI 테스트 작성** — 추가

```python
class NewCliTests(unittest.TestCase):
    def test_set_root_then_init_uses_saved_root(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp) / 'home'
            home.mkdir()
            saved = Path(tmp) / 'Saved'
            env = {'XDG_CONFIG_HOME': str(home / '.config')}
            import os as _os
            old = _os.environ.copy()
            _os.environ.update(env)
            try:
                code, out, err = run_cli(['set-root', '--path', str(saved)])
                self.assertEqual(code, 0, err)
                code, out, err = run_cli(
                    ['init', '--project-id', 'demo', '--documents', str(tmp)])
                self.assertEqual(code, 0, err)
                self.assertEqual(Path(json.loads(out)['project_root']),
                                 saved / 'demo')
            finally:
                _os.environ.clear()
                _os.environ.update(old)

    def test_ensure_dir_creates_named_work_dir(self):
        with tempfile.TemporaryDirectory() as tmp:
            init = run_cli(['init', '--project-id', 'demo', '--documents', tmp])[1]
            root = json.loads(init)['project_root']
            code, out, err = run_cli(
                ['ensure-dir', '--project-root', root, '--name', 'final'])
            self.assertEqual(code, 0, err)
            self.assertEqual(Path(json.loads(out)['path']), Path(root) / 'final')
            self.assertTrue((Path(root) / 'final').is_dir())

    def test_list_reports_projects(self):
        with tempfile.TemporaryDirectory() as tmp:
            run_cli(['init', '--project-id', 'alpha', '--documents', tmp])
            run_cli(['init', '--project-id', 'beta', '--documents', tmp])
            code, out, err = run_cli(['list', '--documents', tmp])
            self.assertEqual(code, 0, err)
            ids = sorted(row['project_id'] for row in json.loads(out)['projects'])
            self.assertEqual(ids, ['alpha', 'beta'])
```

- [ ] **Step 4: 구현** — `_parser()`에 서브커맨드 추가.

```python
init.add_argument("--media-studio-root", default=None,
                  help="studio root; project is created under it")
init.add_argument("--layout", choices=("text", "image", "full"), default="text")

set_root = sub.add_parser("set-root", help="remember the studio root")
set_root.add_argument("--path", required=True)

ens = sub.add_parser("ensure-dir", help="create one work dir on demand")
ens.add_argument("--project-root", required=True)
ens.add_argument("--name", required=True)

lst = sub.add_parser("list", help="list projects in the studio root")
lst.add_argument("--media-studio-root", default=None)
lst.add_argument("--documents", default=None)
```

`main()` 분기:
- `init` → `initialize_project(args.project_id, args.documents, project_root=args.project_root, layout=args.layout, media_studio_root=args.media_studio_root)`
- `set-root` → 경로를 `~` 확장·절대화, 존재하지 않으면 `mkdir(parents=True, exist_ok=True)`, `write_config({**read_config(), "media_studio_root": str(path)})`; 반환 `{"media_studio_root": str(path), "config": str(config_path())}`
- `ensure-dir` → `root = Path(args.project_root).expanduser().resolve()`; `_require_project(root)`; `path = ensure_work_dir(root, args.name)`; 반환 `{"project_root": str(root), "path": str(path)}`
- `list` → `root = Path(args.media_studio_root).expanduser().resolve()` if given else `detect_studio_root(documents=args.documents)[0]`; `_require_project`는 필요 없음(읽기 전용); 반환 `{"studio_root": str(root), "projects": list_projects(root)}` — 루트가 없으면 빈 목록, 폴더를 만들지 않는다.
- `record`/`status`/`resume` 분기 유지.

`production_history.py` 상단 import에 `from studio_layout import (UsageError, slugify, detect_documents, resolve_project_root, assert_managed_path, resolve_inside, initialize_layout, ensure_work_dir, list_projects, detect_studio_root, write_config, config_path, ensure_studio_root, MEDIA_STUDIO_DIRNAME, HISTORY_DIRNAME, EVENTS_DIRNAME, PROMPTS_DIRNAME, PROJECT_JSON, WORK_DIRS)`를 추가한다.

- [ ] **Step 5: 통과 확인**

Run: `python3 -m pytest recording-production-history/scripts/test_production_history.py recording-production-history/scripts/test_studio_layout.py -q`
Expected: PASS (모든 신규·기존 테스트)

- [ ] **Step 6: 전체 스위트 회귀**

Run: `python3 -m pytest -q`
Expected: PASS. 실패가 나오면 이 계획이 건드리지 않은 파일인지 먼저 확인한다(사용자 기존 변경 보존).

- [ ] **Step 7: 커밋**

```bash
git add recording-production-history/scripts/production_history.py \
        recording-production-history/scripts/test_production_history.py
git commit -m "feat(history): add set-root, ensure-dir and list commands"
```

---

### Task 7: 스킬·문서 갱신

**Files:**
- Modify: `recording-production-history/SKILL.md`
- Modify: `creative-production/SKILL.md`, `creative-production/references/production-routing.md`, `creative-production/references/workspace-integration.md`
- Modify: `video-production-assets/references/preproduction-review.md`, `video-production-assets/references/contract.md`, `video-production-assets/references/storyboard-contract.md`, `video-production-assets/references/storyboard-sheet-user-guide.md`, `video-production-assets/references/stickman-animatic.md`, `video-production-assets/references/28-film-production-lifecycle.md`
- Modify: `README.md`, `USAGE_GUIDE.md`

**Interfaces:**
- Consumes: Task 1~6의 실제 CLI/레이아웃.
- Produces: 문서가 코드와 일치. 새 규칙: (a) 경로 지정 우선, (b) 기본 `Media_Studio` 1회 생성·재사용, (c) 프로젝트 slug 멱등, (d) 쓰이는 폴더만 지연 생성, (e) 최종=`final/`, 중간=작업 폴더, 히스토리=`.history/`.

- [ ] **Step 1: `recording-production-history/SKILL.md` 갱신**

"저장 위치 (cross-platform)" 절을 새 규칙으로 바꾼다:
- 기본 루트: 실제 사용자 Documents 아래 `Media_Studio/<project-slug>`.
- 경로 우선순위: `--project-root` > `MEDIA_STUDIO_ROOT` > 설정 캐시(`set-root`) > `<Documents>/Media_Studio`.
- "이미 있으면 다시 만들지 않는다", "프로젝트 slug는 멱등이다".
- v5.1 21개 폴더 문장을 지연 생성 레이아웃 표로 교체:
  `source/`(사용자 자료·원본), `bible/`, `storyboards/`, `assets/`, `audio/`, `edit/`, `qa/`, `final/`(최종 납품본), `.history/`(감사 기록).
- `init` 프리셋 표: `text`=`source`, `image`=`source bible storyboards assets qa`, `full`=전체.
- CLI 계약에 `--media-studio-root`, `--layout`, `set-root`, `ensure-dir`, `list` 추가.
- "언제 쓰나"에 "새 프로젝트를 처음 저장할 때만 경로를 1회 묻는다(도구/캐시/기존 루트로 확인되면 다시 묻지 않는다)"를 명시.

- [ ] **Step 2: 코디네이터·프리프로덕션 참조 갱신**

- `creative-production/SKILL.md:53`·`:63`, `production-routing.md:35`·`:86`, `workspace-integration.md`: `studio_production/<project_id>` → `Media_Studio/<project_id>`. 경로가 캐시/환경/기존 프로젝트로 확인되면 다시 묻지 않는다는 문장 추가.
- `video-production-assets/references/preproduction-review.md:7`·`:32`: 기본 루트를 `Media_Studio/<project-id>`, "init은 프리셋 폴더와 `.history`를 만들고 기존 `project.json`을 덮어쓰지 않는다"로 수정.
- `contract.md`·`storyboard-contract.md`·`storyboard-sheet-user-guide.md`·`stickman-animatic.md`·`28-film-production-lifecycle.md`: 예시 `--output` 경로를 새 이름으로 교체한다. 매핑: `01_SOURCE→source`, `02_BIBLE→bible`, `04_STORYBOARDS→storyboards`, `05_SHOT_CARDS→storyboards`, `06_GENERATION_SPECS→assets`, `07_AUDIO→audio`, `08_ANIMATIC_EDIT→edit`, `09_QA→qa`, `10_DELIVERY→final`, `02_MASTER_ASSETS/*→assets`, `00_MANIFEST→`(자료는 `source`/`final`).
  - `28-film-production-lifecycle.md`의 `01_DEVELOPMENT`…`06_DISTRIBUTION` 매핑 표도 새 이름 기준으로 바꾼다.
  - **예외:** `package_production.py`가 만드는 납품 ZIP 내부 트리(`00_MANIFEST`…`10_DELIVERY`)는 배포 규격이므로 그 설명 문장은 그대로 둔다.

- [ ] **Step 3: README·USAGE 갱신**

- `README.md:34`·`:102`·`:127`, `USAGE_GUIDE.md:131`의 `studio_production` → `Media_Studio`, v5.1 디렉터리 문장 → 지연 생성 레이아웃 설명.
- 플랫폼 줄(Windows/macOS/Linux Documents)은 유지하고 "이미 있으면 재사용"을 덧붙인다.

- [ ] **Step 4: 변경 후 참조 무결성 확인**

Run: `grep -rn "studio_production" --include=*.md . | grep -v "/qa/\|/support/\|CHANGELOG\|/docs/\|\.superpowers\|\.omx\|\.omo"`
Expected: 새 규칙을 설명하는 곳 외에 남은 `studio_production`이 없음(역사 기록/마이그레이션 안내 문구는 허용, 새 기본값으로 쓰이면 안 됨)

Run: `grep -rn "0[0-9]_[A-Z]\{2,\}" --include=*.md recording-production-history creative-production video-production-assets/references | grep -v "package_production\|납품\|ZIP\|배포"`
Expected: 남은 항목은 납품 ZIP/레거시 패키지 설명뿐

- [ ] **Step 5: 커밋**

```bash
git add recording-production-history/SKILL.md creative-production README.md USAGE_GUIDE.md \
        video-production-assets/references
git commit -m "docs: document Media_Studio lazy project layout"
```

---

### Task 8: 버전 bump + 최종 검증

**Files:**
- Modify: `manifest.json`, `CHANGELOG.md`, 그리고 `--bump-skills`가 건드리는 `SKILL.md` version 프론트매터
- Test: 전체 스위트

**Interfaces:**
- Consumes: Task 1~7.
- Produces: 일관된 패키지 버전과 릴리스 노트.

- [ ] **Step 1: 버전 일관성 기준선 확인**

Run: `python3 scripts/check_versions.py`
Expected: `version check OK: package 2.33, 22 skill(s) consistent`

- [ ] **Step 2: CHANGELOG Unreleased 항목 추가** — `## Unreleased` 맨 위에 한 줄 추가

```markdown
- Replace per-project fixed 21-folder v5.1 layout with a lazy `Media_Studio` project layout: one studio root under Documents (`--project-root` / `MEDIA_STUDIO_ROOT` / saved `set-root` / `<Documents>/Media_Studio` precedence), idempotent slug project folders that are reused instead of recreated, presets (`text|image|full`) that create only the work directories a task uses, `final/` separated from work directories, and `.history/` retained as the audit trail. Add `set-root`, `ensure-dir` and `list` commands. Cross-platform Documents resolution and `.history` are unchanged; `project.json` schema and delivery ZIP package tree are unchanged.
```

- [ ] **Step 3: 버전 bump**

Run: `python3 scripts/bump_version.py --part minor --bump-skills`
Expected: exit 0, `manifest.json`이 `2.34`(또는 다음 minor), `CHANGELOG.md`에 `## 2.34 <date>` 헤딩 생성, 스킬 minor 버전 증가

- [ ] **Step 4: 버전 일관성 재확인**

Run: `python3 scripts/check_versions.py`
Expected: `version check OK: package 2.34, 22 skill(s) consistent`

- [ ] **Step 5: 전체 스위트 + 실 동작 스모크**

Run: `python3 -m pytest -q`
Expected: PASS

Run:
```bash
tmp="$(mktemp -d)" && python3 recording-production-history/scripts/production_history.py \
  init --project-id "Demo Film" --documents "$tmp" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d['project_root'], d['created'])"
```
Expected: `<tmp>/Media_Studio/demo-film` 출력, `created`에 `source`와 `project.json`만(빈 v5.1 폴더 없음)

- [ ] **Step 6: 커밋**

```bash
git add manifest.json CHANGELOG.md */SKILL.md
git commit -m "release: 2.34 Media_Studio lazy project layout"
```

---

## Self-Review

- **Spec coverage:** 루트(§5, Task 4·5), 프로젝트 slug 멱등(§5, Task 5), 지연 생성·프리셋(§6, Task 5), 중간/최종/히스토리 분리(§6, Task 5), 기존 프로젝트 보존(§2·6, Task 5·6), 경로 1회 질문(§6, Task 4·6·7), 3 OS 호환(Global Constraints, Task 1·2), 문서 갱신(§7, Task 7), 버전(§7, Task 8).
- **플레이스홀더:** 없음 — 각 Step은 명령·기대 결과·코드 포함.
- **이름 일관성:** `studio_layout.py`의 `slugify`/`detect_documents`/`assert_managed_path`/`resolve_inside`/`detect_studio_root`/`ensure_studio_root`/`initialize_layout`/`ensure_work_dir`/`list_projects`/`WORK_DIRS`/`LAYOUT_PRESETS`가 Task 1~6에서 동일.
- **주의:** Task 5 Step 4의 `initialize_project` 반환 `documents` 키 의미가 `Root.parent.parent` → `Root.parent`로 바뀐다. 기존 단언이 있으면 Task 6 Step 1에서 함께 갱신한다.
