# Archive crosswalk ledger-grounded follow-up — one-call result

**Result:** one fresh stateless `default` call completed without error. Overall **NOT PASS** against the predeclared §88 criteria: C2 and C4 fail. This is a separate follow-up only; it does not regrade or replace the five-call first smoke, its two already-recorded passing negative controls, or frozen T13–T20 evidence. No skill wording, prior QA artifact, or F: file was edited. No original media, images, video playback/full decode, generation, upload, API, Blender, or 3D work was performed. This does not claim all 44 archive videos were analyzed.

## Run metadata and evidence boundary

- Prompt source: `docs/implementation/2026-10-12-rofan-craft-skill-test-plan.md`, §54, with the exact bounded data described in §58–84; one stateless call only. Prompt SHA-256: `0ddf84bc7b1d9c27f7b19296c5675ac9e34fc81ebd93d52ecd71502e29142911`.
- Requested model: `default`. Resolved model: `UNKNOWN` (helper did not expose it). Error: none. Combined package/evidence system-context SHA-256: `e762de71a11d64bf300da1d2b088d75e1258b79aa0205bd25f77f03137f013a2`.
- Context used the bounded current source master/open gates, CF-13 provisional record, selected F-EA scene/shot/event ledger records and specified candidate-disposition records, plus the six current package owner/reference files below. No rubrics/spec were supplied in model context. IDs/PTS and template QA fields were directly checked against these files before context assembly.
- F: `F:\Resources\AI-Rofan-Drama-2026-10-11\videos\rofan-temporal-analysis\exhaustive\semantic\archive-normalized-master-in-progress.json` — SHA-256 `f62effd762239c581992213ad4e371b79aa6c22f0682c50b921a43d563135a6e`.
- F: `F:\Resources\AI-Rofan-Drama-2026-10-11\videos\rofan-temporal-analysis\exhaustive\semantic\cross-source-craft-catalog-provisional-v1.json` — SHA-256 `63984d67816a38d40c33f55120b5e30702f607981eeadab0b4feebe64adadb6f`.
- F: `F:\Resources\AI-Rofan-Drama-2026-10-11\videos\rofan-temporal-analysis\exhaustive\semantic\reviewer-F\ea6a017b14fc647205b30ea896553c8e36e3abbc2983b73757a9c7cb282a8257-canonical-shot-scene-event-ledger.json` — SHA-256 `2226407c876bd979cc236e55ddb17db6276f2059893d55e9ced81a6c8a134d8a`.
- F: `F:\Resources\AI-Rofan-Drama-2026-10-11\videos\rofan-temporal-analysis\exhaustive\semantic\reviewer-F\ea6a-native-union\candidate-dispositions.json` — SHA-256 `a986c48e1ce3f007ea07bff44efbde2afabee004854a480c2db5ae9c4ebb52e2`.
- Package: `video-production-assets/references/25-reference-video-analysis.md` — SHA-256 `41dc63ea90c0a3523128fb04a10368537418bfc7eb66ac1f07b3df99bb4194dc`.
- Package: `video-production-assets/assets/archive-craft-crosswalk-template.md` — SHA-256 `5a1b41737e7f34b95ca3811b01fc8591de8977a1af27f1b9b3e1befeac9b5cf7`.
- Package: `video-production-assets/assets/archive-audit-template.md` — SHA-256 `333e6f844ac79878b7a948761abc19c50dc57d0ee38d105bc3a50f5b1c15e487`.
- Package: `video-production-assets/assets/shot-dna-template.md` — SHA-256 `5dbc0b305ad97da240baf19cf92db5962fd1824b48448a73f57fc0600f9ab3fa`.
- Package: `video-production-assets/references/06-shots.md` — SHA-256 `ee493732d45b82fc5f640a9af8041fca3e78e363da6183de14d59115e5de6b5e`.
- Package: `video-production-assets/assets/06-shots-template.md` — SHA-256 `506c83f3814c04ed1ebb429301d0f92ee9644e30207de74d03a4d032e18ae860`.

## Manual criteria review (§88)

1. **One row traceable to predeclared identifiers/locators — PASS.** The row gives full occurrence/source-position and archive IDs, filename, `F-EA-SC01`, full p0 shot ID, bounded event ID, 1/15360 timebase, sampled within-shot states and the p0-only portion of the multi-shot event.
2. **Preserves `[0,77824)` and supported candidate outcomes without extra cuts — FAIL.** Shot interval and last-old/next-start PTS are correct, and both candidate outcomes and native-neighbor triplets are described correctly. But candidate locators are emitted as `archive-event:…:77824` and `archive-event:…:78848`, not the exact predeclared full candidate IDs. The abbreviated IDs do not preserve retrievable locator identity; no unsupported extra cut is invented.
3. **Story-neutral mechanism, inference alternative, applicability and avoid conditions — PASS.** Mechanism is generic, role is marked `[INFERENCE]`, an alternative is stated, and applicability/avoid constraints reject transferring source staging/timing or unsupported gait/force/consent/intent claims.
4. **Exact existing owner and QA fields — FAIL.** Names the existing 06-shots owner and some actual columns, but omits exact listed fields `shot_id`, `scene_id`, `beat_id`, `시선/축`, and `대안·채택/승인 상태`. It also fails to identify the five required `shot-dna-template.md` `이전 체인` columns (`레퍼런스 증거(관찰+위치)`, `메커니즘`, `의도 효과(해석)`, `새 브리프 제작 요구`, `정성 검증 기준`). The `Actor phase / contact / visibility` cue mention does not supply these omitted required owner fields.
5. **Selected-source versus archive-global status — PASS.** Correctly distinguishes selected-source closure from 34/44 archive materialization and ten unmaterialized sources, lists global gates as open, and does not claim full-rate playback, human audio listening, archive closure, or prevalence.

## Exact prompt

> Using only the supplied current semantic source master, provisional cross-source craft catalog, selected source-specific semantic ledger and candidate-dispositions ledger, plus the listed current owner references/templates, produce exactly ONE bounded, evidence-grounded archive-craft crosswalk row. Use only the predeclared source/scene/shot/event and PTS assertions below; do not analyze all 44 sources or create additional findings. Link the source occurrence → source-local scene → shot interval → linked event and in-shot evidence → craft finding → story-neutral mechanism → applicable and avoid conditions → existing owner and exact target QA fields. Distinguish direct observation from `[INFERENCE]` and state an alternative. Report every unknown and the current global coverage status. Evaluate a candidate-versus-confirmed outcome only for the predeclared candidate records below. Do not inspect or claim to inspect original media, play footage, edit files, or infer source-wide prevalence. Do not copy source story, character identity, props, wardrobe, exact staging, shot sequence, or original timing into the transferable rule. Do not claim the selected source closes the archive.
>
> [The call then received the bounded evidence extracts and package references listed above, not the test-plan assertions/rubric. The frozen test-plan prompt's assertion text is recorded at `docs/implementation/2026-10-12-rofan-craft-skill-test-plan.md` §73–84; it was used by the grader, not placed in the model context.]

## Full raw response

```text
## 범위 및 현재 커버리지

**범위:** 선택된 단일 source occurrence의 지정된 scene/shot/event만. 원본 미디어를 검사하거나 재생하지 않았고, 다른 source occurrence를 분석하지 않았다.

**현재 전체 아카이브 상태:** master는 `IN_PROGRESS_ACTIVE_PARTITION_V5`: 44 source occurrence 중 34 materialized, 10 unmaterialized. Archive crosswalk, native-image, candidate-free transition/first-last, scene-bound, occurrence-vs-case gates는 열려 있다. 선택된 source의 visual-semantic review 완료 상태는 archive 완결을 뜻하지 않는다. Full-rate playback이나 human audio listening도 확인되지 않았다.

## 단일 craft crosswalk finding

| finding_id | source occurrence → scene → shot interval → event | 직접 관찰 및 근거 | `[INFERENCE]` 기능 및 대안 | Story-neutral mechanism | 적용 조건 / 피할 조건 | 기존 owner 및 정확한 QA 필드 | 대상별 관찰 가능 확인 기준 | 미확인·상태 |
|---|---|---|---|---|---|---|---|---|
| CF-13 bounded case | **Occurrence:** `source_position_id` `ea6a017b14fc647205b30ea896553c8e36e3abbc2983b73757a9c7cb282a8257`; `archive_id` `sha256:4831e753f691064aaa92b4b3748045b3fbef7d6dc76e0cfb21e37f1b7c4db195`; 파일명 `AI 로판 드라마 ｜ 몰아보기 EP.1~9 ｜ 버려진 약혼녀에게 집착이 시작됐다 🗝️.mp4`. **Scene:** `F-EA-SC01`, bounds 0–5.033333333333333 s; 한 shot. **Shot:** `archive-shot:ea6a017b14fc647205b30ea896553c8e36e3abbc2983b73757a9c7cb282a8257:p0`; timebase 1/15360; visible PTS 0–77312 inclusive, shot interval **[0, 77824)**; 다음 shot 시작 PTS 77824. **Linked event:** `archive-event:ea6a017b14fc647205b30ea896553c8e36e3abbc2983b73757a9c7cb282a8257:p0:F01`, 0–12.633333 s로 여러 shot/scene에 걸침. 이 finding에는 p0 scene 내 bounded portion만 연결하며, event 전체를 scene에 귀속하지 않는다. | **직접 관찰(ledger의 dense sampled states/native endpoints; 연속 동작 확인 아님):** 시작은 profile composition이며, 두 번째 인물이 들어오고 근접/접촉이 증가한 뒤 close state가 PTS 77312까지 유지된다. 근거 샘플에는 PTS 0, 3072, 9728, 35840, 39424, 42496, 45568 및 within-shot state PTS 39424가 포함된다. 이는 표본 상태이지 연속 모션·보행 증거가 아니다. | **[INFERENCE, low]:** 두 인물이 함께 보이는 구도가 접근과 접촉의 관계를 읽기 쉽게 할 수 있다. **대안:** routine coverage, 별도 연출·생성 뷰 또는 편집된 극적 이미지일 수 있다. | 접근과 파트너의 반응을 공유된 2인 프레임에서 읽을 수 있게 유지하고, 접촉이 등록된 뒤 편집으로 리셋한다. | **적용:** 새 brief에서 접근·접촉 관계 자체가 중요한 동작일 때. **피하기/제한:** 보행 궤적이나 발 디딤이 핵심인 경우, 또는 근거 없이 힘·동의·의도를 나타내야 하는 경우에는 이 사례를 gait·force·consent·intent 규칙으로 확장하지 않는다. 원본 staging·이야기·절대 타이밍은 이전하지 않는다. | **Owner:** 기존 [06-shots.md](video-production-assets/references/06-shots.md)의 블로킹·샷 절차. **정확한 06 템플릿 QA 필드:** `shot-local time (s or frames; FPS if frames)`, `인물 블로킹`, `공개 정보`, `관점·감정/구도 의도`, `종료 프레임`; 해당하는 경우 샷 계획의 `Actor phase / contact / visibility` cue에 접촉 가시성을 기록한다. **대상별 확인:** 계획된 새 샷에서 접근과 파트너 반응이 한 프레임 안에 읽히는지, 접촉 상태가 관찰 가능하게 등록되는지, 종료 프레임까지 의도한 상태가 유지되는지 확인한다. 이는 계획 기준이며 실제 생성·촬영 결과의 합격을 뜻하지 않는다. | **전이 후보:** provisional catalog CF-13; core fields는 기존 owner coverage에 이미 포함된 추가 source case이지 새 보편 규칙의 증거가 아니다. **전이 금지/미확인:** literal path, footfall count, full gait, measured camera move, force, consent, intent, unpictured action 및 heard dialogue는 성립하지 않는다. Archive crosswalk와 관련 global gates는 OPEN이며, 전체 아카이브 완결 또는 prevalence는 주장하지 않는다. |

## 사전 지정 candidate 기록의 bounded 판정

- Candidate PTS **77824** (`archive-event:…:77824`): `observed_hard_view_change`; 77312/77824/78336 native neighbors로 outgoing view와 새 view의 급격한 변화가 시각적으로 확인됐다고 기록되어 있다. 경계는 확인됐으나 제작 원인은 미확인이다.
- Candidate PTS **78848** (`archive-event:…:78848`): `continuous_within_shot`; 78336/78848/79360에서 같은 view/eyeline로 기록되어 있으며, 이 후보는 cut이 아니다.

이 판정은 위 두 사전 지정 candidate에만 해당하며 다른 경계·전환을 평가하지 않는다.
```

## Required repository checks

- `python scripts/check_versions.py` — exit 0; exact output: `version check OK: package 2.5, 23 skill(s) consistent`.
- `python -X utf8 -m pytest -q` — exit 0; 258 passed, 1 skipped, 217 subtests passed; exact summary: `258 passed, 1 skipped, 2 warnings, 217 subtests passed in 27.30s`. Skip identity was not named in the captured pytest output. Two warnings: `PytestUnhandledThreadExceptionWarning` from subprocess reader threads / `UnicodeDecodeError` in `scripts/test_sync_installed.py::test_stale_link_is_repointed` (byte 215) and `scripts/test_sync_installed.py::test_remove_link_never_deletes_target_content` (byte 224). Full output captured in the execution record.

## Isolated install/link smoke

Executed from repository root using `python -c` to create a unique clean temporary source snapshot of the current manifest's 23 skill folders, package installer and required package support inputs. Removed only the copied generated `video-production-assets/support/` from that temporary snapshot (installer creates it); repository/global roots were not targets. Installer argv was `[sys.executable, <temp>\source\scripts\install_package.py, --skills-root, <temp>\installed-skills]`; exit 0. Temp root: `C:\Users\Declan\AppData\Local\Temp\rofan-ledger-followup-knintdj5`; installed root: `C:\Users\Declan\AppData\Local\Temp\rofan-ledger-followup-knintdj5\installed-skills`. Exact installer stdout reported `Installed 23 skill(s) ... (package version 2.5).`, each of the 23 manifest skill destinations, and the generated support directory; stderr was empty. The installed `video-production-assets/assets/archive-craft-crosswalk-template.md` exists. Its two relative Markdown links resolve within the installed tree: `archive-audit-template.md` and `shot-dna-template.md` (both `exists=True`, `within_install=True`). No package files, global roots, or F: paths were written.
