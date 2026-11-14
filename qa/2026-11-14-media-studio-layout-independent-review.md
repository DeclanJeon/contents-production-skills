# Media_Studio independent final review

## Review

**Merge verdict: BLOCK. Ready to merge: No.**

Two P1 findings remain: studio-relative initialization can write outside the selected studio through a linked project folder, and storage tests can write into the operator’s saved production root.

### Review boundary

Read-only inspection of current implementation, tests, specification, plan, ledger rulings, validation report, scoped documentation and working-tree diff. No files changed or commands executed.

The available diff tool excludes committed ranges. Consequently, **the `e7260dd` → implemented-commits historical diff was not independently reviewed**; current files were inspected directly.

The reported **76 storage tests + 5 subtests** and **786 full-suite tests + 518 subtests** are prior evidence, not results independently reproduced here.

## Correct — strengths

- Minimal default layout and explicit image/full presets are implemented in `recording-production-history/scripts/studio_layout.py:265–271,340–362`.
- Ordinary repeat initialization preserves ledger bytes and creates no preset directories. Tests cover text→full retry without adding `final/`: `recording-production-history/scripts/test_production_history.py:954–977`.
- Explicit project roots bypass studio/config resolution and receive no appended slug: `recording-production-history/scripts/production_history.py:117–125`.
- Existing studio directories are reused without clearing contents: `studio_layout.py:246–251`; corresponding test: `test_studio_layout.py:120–127`.
- Atomic exclusive ledger publication, schema `1.1`, and audit ownership remain intact: `studio_layout.py:276–293`; `recording-production-history/SKILL.md:13`.
- Relevant writers already create missing parents: storyboard sheets (`render_storyboard_sheet.py:702`), splitting (`split_storyboard.py:542`), document PDFs (`storyboard_document.py:65`) and packaging (`package_production.py:423,451`). Static inspection supports lazy-directory compatibility at these seams.
- CI genuinely defines six OS/Python storage jobs: `.github/workflows/ci.yml:8–27`. The validation report correctly distinguishes configuration from executed platform evidence.
- Manifest version `2.34`, its release heading and version declarations for the 22 bundled skills are present.

## Findings

### 1. P1 — Linked project folder escapes the selected studio

**Location:** `recording-production-history/scripts/production_history.py:123`; `studio_layout.py:79–88,303`.

**Evidence:** The new `--media-studio-root` branch appends the slug without validating containment against that studio. The managed-path guard checks descendants of the resulting project root, **not the root itself**. Default resolution also resolves the slug path before a studio-boundary check.

**Repro:** In disposable directories, make `studio/demo` a directory symlink to a separate `outside` directory, then run:

`init --project-id demo --media-studio-root <studio>`

Initialization writes `project.json`, work and audit directories into `outside`, rather than rejecting the escape.

**Impact:** A studio-relative request can modify a different directory without the user selecting it as their project root.

**Smallest fix:** Validate the unresolved slug child against the selected studio before resolving or initializing it. Cover both default/config resolution and explicit `--media-studio-root`; test directory symlinks and Windows junctions.

### 2. P1 — Tests inherit real saved-root configuration

**Location:** `recording-production-history/scripts/test_production_history.py:126–128,138–145,267–272,587–592`; `studio_layout.py:236–243`.

**Evidence:** Numerous tests pass temporary `documents` paths but leave `MEDIA_STUDIO_ROOT` and saved configuration ambient. Those settings intentionally outrank `documents`. No `conftest.py` supplies isolation.

**Repro:** Point an **isolated temporary config** at another disposable directory, then execute `InitTests::test_init_default_layout_creates_only_needed_dirs`. It creates `lazy-one` in the configured studio, outside the test-owned Documents directory.

**Impact:** On an operator machine after `set-root`, the suite can create production projects there. Other tests explicitly rewrite ledgers or create/delete artifacts in the resolved project. Temporary `documents` arguments no longer provide isolation.

**Smallest fix:** Isolate config/home and clear studio overrides for every storage test, including subprocess inheritance. Test precedence separately with explicitly supplied temporary configuration. Do not change production precedence to accommodate tests.

### 3. P2 — Repeat init checks unused preset paths and can reject a no-op

**Location:** `recording-production-history/scripts/studio_layout.py:320–325`.

**Evidence:** The current uncommitted preflight checks every requested preset path **before** determining that an existing ledger means none will be created.

**Repro:** Create an existing project with `source` linked to an ordinary directory inside that same project. Repeat `init --layout full`. Initialization rejects the link despite having no work-directory write to perform.

**Impact:** Existing projects with linked work directories cannot receive the promised preset-independent no-op.

**Smallest fix:** Always validate ledger/audit paths, but validate preset creation paths only for new projects. Add an existing-project linked-work-directory regression test.

### 4. P2 — `ensure-dir` silently creates an uninitialized project root

**Location:** `recording-production-history/scripts/production_history.py:729–731`; `studio_layout.py:378`.

**Evidence:** Unlike the plan’s Task 6 contract, the CLI never calls the existing `_require_project()` guard.

**Repro:** Run `ensure-dir --project-root <temporary-nonexistent-path> --name assets`. It succeeds and creates a bare directory tree without `project.json`.

**Impact:** A mistyped project path silently produces an orphan workspace instead of identifying the wrong destination.

**Smallest fix:** Require an initialized project before `ensure_work_dir()`. Test that rejection leaves the nonexistent destination absent.

### 5. P2 — Non-UTF-8 config/ledger bypasses structured error handling

**Location:** `recording-production-history/scripts/studio_layout.py:194–199,327–333`.

**Evidence:** UTF-8 reads catch `OSError` and JSON syntax errors, but not `UnicodeDecodeError`; `main()` also does not catch that exception.

**Repro:** Write `b'\xff'` to an isolated `media-studio/config.json`, then run `list`. An undecodable existing `project.json` similarly escapes initialization’s error conversion.

**Impact:** Corrupt input produces a traceback rather than the documented broken-config fallback or structured project-preflight error.

**Smallest fix:** Treat undecodable config as empty; convert undecodable ledgers to `UsageError`. Add tests asserting structured failure/fallback and no project writes.

### 6. P2 — Delivery examples contradict the new `final/` contract

**Location:** `video-production-assets/references/storyboard-contract.md:172–187`; `USAGE_GUIDE.md:157–161`.

**Evidence:** The updated delivery examples still place the user-facing PDF in `storyboards/`, while `recording-production-history/SKILL.md:31` requires final deliverables in `final/`.

**Repro:** Following the documented PDF-delivery command puts the deliverable beside working storyboard files.

**Impact:** Coordinator instructions and executable examples disagree about where users should find completed deliverables.

**Smallest fix:** Put delivered PDFs in `final/`; retain intermediate sheet/extraction paths under `storyboards/`. State explicitly when an example is merely a working review draft.

## Disposable reproduction command

**Not executed during this review.** Run from the repository root. All writable destinations/configuration are temporary; bytecode and pytest cache writes are disabled.

```bash
python3 - <<'PY'
import json, os, subprocess, sys, tempfile
from pathlib import Path

repo = Path.cwd()
cli = repo / "recording-production-history/scripts/production_history.py"
with tempfile.TemporaryDirectory(prefix="media-review-") as tmp:
    p = Path(tmp)
    env = os.environ.copy()
    env.pop("MEDIA_STUDIO_ROOT", None)
    env.update(
        HOME=str(p / "home"), USERPROFILE=str(p / "home"),
        XDG_CONFIG_HOME=str(p / "config"),
        STUDIO_DOCUMENTS_DIR=str(p / "documents"),
        PYTHONDONTWRITEBYTECODE="1", PYTHONUTF8="1",
    )
    (p / "home").mkdir()
    config = p / "config/media-studio/config.json"
    config.parent.mkdir(parents=True)

    def run(*args):
        r = subprocess.run(
            [sys.executable, str(cli), *map(str, args)],
            cwd=repo, env=env, capture_output=True, text=True)
        print("CLI:", args, "exit:", r.returncode)
        print((r.stderr or r.stdout)[-1000:])
        return r

    studio, outside = p / "studio", p / "outside"
    studio.mkdir()
    outside.mkdir()
    try:
        (studio / "demo").symlink_to(outside, target_is_directory=True)
    except OSError as exc:
        print("F1 skipped: directory symlinks unavailable:", exc)
    else:
        run("init", "--project-id", "demo", "--media-studio-root", studio)
        print("F1 external ledger:", (outside / "project.json").exists())

    ambient = p / "configured-studio"
    config.write_text(json.dumps({"media_studio_root": str(ambient)}))
    subprocess.run([
        sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider",
        "recording-production-history/scripts/test_production_history.py"
        "::InitTests::test_init_default_layout_creates_only_needed_dirs",
    ], cwd=repo, env=env, check=False)
    print("F2 escaped test fixture:", (ambient / "lazy-one").exists())
    config.unlink()

    existing = p / "existing"
    existing.mkdir()
    (existing / "project.json").write_text('{"project_id":"demo"}')
    (existing / "data").mkdir()
    try:
        (existing / "source").symlink_to(
            existing / "data", target_is_directory=True)
    except OSError as exc:
        print("F3 skipped: directory symlinks unavailable:", exc)
    else:
        run("init", "--project-id", "demo",
            "--project-root", existing, "--layout", "full")

    run("ensure-dir", "--project-root", p / "orphan", "--name", "assets")
    print("F4 orphan created:", (p / "orphan/assets").exists())

    config.write_bytes(b"\xff")
    run("list")
PY
```

## Coordinator-instruction assessment

**Static inspection:** Root selection is substantially clear in `creative-production/SKILL.md:53`, `creative-production/references/production-routing.md:86` and `recording-production-history/SKILL.md:19–27`:

| Scenario | Documented choice |
|---|---|
| Fresh, unresolved first save | Ask once before saving |
| Default accepted | Actual Documents/Media_Studio |
| Existing default studio | Reuse without another question |
| Explicit project directory | Use directly; append neither studio nor slug |
| Environment/saved studio | Use precedence and skip repeated question |
| Resume | Preserve selected root; inspect ledger/files/in-flight work |
| Chat-only | No initialization or file creation |

This is **instruction-level evidence, not observed agent behavior**. Actual pressure tests remain unperformed. The PDF examples identified above weaken otherwise consistent delivery-location guidance.

## Fixed

None; review-only.

## Declined to judge

- Historical commit-by-commit changes: committed-range artifacts and Git inspection tools were unavailable.
- Actual Windows redirected/OneDrive Documents, junction and native case-insensitive behavior: no Windows/macOS execution observed.
- Real coordinator compliance under pressure: static inspection cannot establish behavioral acceptance; child agents were prohibited.
- Automatic legacy migration and changed ZIP projection/schema: explicitly outside scope. Existing project preservation and relevant writer compatibility were inspected.
- Filesystems lacking atomic hard-link publication: existing implementation requirement, explicitly excluded by the validation evidence.
- Unrelated stickman/creator/Matt-writing changes: intentionally excluded.

## Readiness

**BLOCK pending P1 fixes and isolated regression verification.** Ordinary lazy initialization is sound, but studio containment and test isolation are not yet safe. P2 items are separately actionable; actual cross-platform execution and coordinator pressure tests remain outstanding evidence gates.