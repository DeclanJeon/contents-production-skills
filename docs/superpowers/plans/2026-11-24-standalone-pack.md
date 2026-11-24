# Standalone skill pack — implementation plan

- [x] Verify the boundary with a failing source and copy-install regression test.
- [x] Remove consumer-owned manifest metadata, schema, inventory, runtime wrappers, and CI/release wiring. Keep standalone install, archive creation, and tests.
- [x] Remove consumer-specific instructions from active skill content; retain neutral craft and safety gates. Preserve historical evidence and old release notes as archives.
- [x] Run full tests, version check, diff check, and build/inspect the standalone archive. Do not publish or change installed packages in this task.

Evidence: 1,370 passed, 5 skipped, 534 subtests passed. Package/skill version check and diff check passed. Local archive checksum verified and archive excludes the removed integration inventory, stage guide, and submitter. Consumer-side mounting and migration are outside this change.
