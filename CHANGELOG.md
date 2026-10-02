# Changelog

## 1.3 — 2026-10-02

- Package `creative-production` as the single content/video coordinator alongside the three existing production/camera/Blender specialists and four text-planning skills: eight core skills total.
- Make locked text drafting and text-only planning independent of provider accounts, GPUs, Blender and particular agent frameworks. Preserve inherited briefs/checkpoints, requested artifact scope and separate review, execution/spend and publication authorization.
- Add complete planning resources, host discovery metadata and synthetic behavior evals. Exclude newly imported book-summary/Notion references; preserve existing source and reuse limitations without granting a new license.
- Extend the one package manifest with the entry skill, support host and conditional external dependencies. No external skills, auth setup, models or tools are installed automatically.
- Add `scripts/install_package.py`: complete source/support/collision preflight, refusal to overwrite/merge by default, explicit backed-up replacement and optional second-root duplicate migration. Unrelated skills remain outside managed scope. Partial I/O failures report affected destinations and retained backups; installation is not atomic.
- Keep existing production schema 1.1 and camera-spatial-1.0 contracts and validators unchanged.
- Verification: 21 installer tests, 8 production-contract tests and 6 spatial tests pass; actual fresh-install, collision, backup-upgrade and alias-migration CLI smokes; installed resource checks; educational/spatial validator smokes; 13 core-only model artifact/action probes. The latter are not tool-enabled provider/media or platform execution tests. Repository QA retains the detailed verification record.
