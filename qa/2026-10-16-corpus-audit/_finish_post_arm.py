#!/usr/bin/env python
"""Wait for the codex usage-limit reset, then finish the post-change arm.

Two phases, run in order:
  1. all still-missing frozen rows from `_blocks.json` (this includes the
     boundary probes M-04 / M-09, which were cleared so they replay fresh
     against the 2.9 boundary patch);
  2. the two S1 probes, which live only in `baseline-prompts.md`.

`_run_baseline.py` caches by result-file existence, so only missing rows run.
"""
import json
import pathlib
import re
import subprocess
import sys
import time
from datetime import datetime, timedelta

REPO = pathlib.Path(r"C:/Users/Declan/Documents/Projects/Skills-and-Automation/contents-production-skills")
AUDIT = REPO / "qa" / "2026-10-16-corpus-audit"
SCRATCH = pathlib.Path(r"C:/Users/Declan/AppData/Local/Temp/cpsbook")

target = datetime.now().replace(hour=10, minute=20, second=0, microsecond=0)
if target < datetime.now():
    target += timedelta(days=1)
wait = (target - datetime.now()).total_seconds()
print("waiting", int(wait), "s until", target, flush=True)
time.sleep(max(0, wait))

# Phase 1: frozen rows (M-04 and M-09 among them, freshly cleared).
print("phase 1: frozen rows", flush=True)
subprocess.run([sys.executable, "-X", "utf8", str(AUDIT / "_run_baseline.py"), "all"], cwd=str(REPO))

# Phase 2: S1a / S1b from baseline-prompts.md fenced text blocks.
print("phase 2: S1 probes", flush=True)
text = (AUDIT / "baseline-prompts.md").read_text(encoding="utf-8")
blocks = re.findall(r"```text\n(.*?)\n```", text, re.S)
for name, block in zip(("S1a", "S1b"), blocks):
    out = SCRATCH / f"bl_{name}.json"
    if out.exists():
        try:
            if json.loads(out.read_text(encoding="utf-8")).get("stdout", "").strip():
                continue
        except Exception:
            pass
    prompt = block + "\n\n[END OF PROMPT. Answer the question above directly. Do not edit any file.]"
    r = subprocess.run(
        [r"C:/Users/Declan/AppData/Roaming/npm/codex.cmd", "exec", "--sandbox", "read-only", "--skip-git-repo-check", prompt],
        cwd=str(REPO), capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=900)
    out.write_text(json.dumps({"key": name, "prompt": block, "stdout": r.stdout,
                               "stderr": r.stderr[-3000:], "rc": r.returncode}, ensure_ascii=False), encoding="utf-8")
    print("ran", name, r.returncode, len(r.stdout or ""), flush=True)

missing = []
for p in sorted(SCRATCH.glob("bl_*.json")):
    d = json.loads(p.read_text(encoding="utf-8"))
    if not d.get("stdout", "").strip():
        missing.append(p.stem[3:])
print("post arm retry complete; empty/missing:", missing, flush=True)
