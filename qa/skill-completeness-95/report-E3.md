# E3 provider asset evidence corrections

상태: 독립 검토 요청. 점수/95% 달성/행동 평가 통과 주장 없음. W5 보고와 claim 원본은 수정하지 않았으며 E3 보충 원장 29행으로 이력을 분리했다. 테스트·빌드·린터·formatter는 공유 edit wave 계약에 따라 실행하지 않았다. 생성·업로드·훈련·계정 변경·지출·배포·게시·설치·커밋 없음.

## 변경 파일과 결함

### 독립 검토 지적

- `higgsfield-product-photoshoot/SKILL.md`: frontmatter, opening, UX, Generation, exclusion에서 GPT Image 2/private enhancer를 historical/unverified로 명시. 현재 공식 계약 필요. “Always gpt_image_2”를 현재 보장으로 읽을 수 없게 변경. image ineligible gate와 원래 경로를 유지. aspect enums/default도 help가 입증하지 않는 범위로 구분.
- `higgsfield-marketplace-cards/SKILL.md`: scope 표 바로 위와 표 헤더에 main+5/main+7/full-set 수량이 historical/unverified임을 명시. 승인 범위는 실제 brief/검증된 현재 계약에서 결정하며 표로 수량을 확대하지 않음. frontmatter/opening의 compliance/backend 보장도 해제.
- `higgsfield-product-photoshoot/references/modes.md`: 질문 3–4개 고정 최소를 제거. 미해결 질문만 최대 4개, brief가 완전하면 0개. 모드/슬라이드/비율 taxonomy는 help에서 열거되지 않은 historical 항목으로 구분.
- `higgsfield-soul-id/references/photo-guide.md`: “Higher variety = better”를 clear/same-person/identity-consistent 자료 안에서만 쓰는 제한적 heuristic으로 변경. 8–12도 검증된 optimum으로 취급하지 않음. provider count와 해상도/형식 선호를 구분.

### 전체 triggered provider reference 감사에서 발견한 추가 결함

다음 generate 참조 15개를 모두 직접 읽고 해당 파일에 공식 계약의 실제 지원 범위/미지원 범위를 결속했다.

- `higgsfield-generate/references/package-gate.md`: MCP confirmed-ID vs CLI path auto-upload, unknown outcome, poll interval의 직접 읽은 계약 위치 추가. 패키지 정책을 provider 금지로 포장하지 않음.
- `higgsfield-generate/references/model-catalog.md`: historical/non-exhaustive/current-lookup 범위 명시; “objective attention proxy” 삭제; photoshoot GPT backend 반복 단정도 수정. cached duration/media/count/quality 비교가 검증 결과가 아님을 명시.
- `higgsfield-generate/references/media-inputs.md`: MCP mirror라는 잘못된 설명 수정. 공식 Seedance 2.0 표는 `audio_references`와 별도 `generate_audio`를 선언하므로 output-audio flag 금지 문구 수정.
- `higgsfield-generate/references/image-branches.md`: 공식 image 표에서 실제 읽은 fields와 검증하지 못한 quality mapping/style/craft 선호 분리. image exclusion 유지.
- `higgsfield-generate/references/workflows.md`: 공식 README가 입증하는 discover/create/cost/get/wait와 검증하지 못한 optional pro-mode/media limits 분리.
- `higgsfield-generate/references/prompt-engineering.md`: ~200 token을 provider cap/왜곡 실증으로 단정하지 않음. 보편적 인물/상표 거절 목록 대신 실제 모델 정책/반환 상태 확인. 외부 craft를 실증한 것처럼 재분류하지 않음.
- `higgsfield-generate/references/troubleshooting.md`: timeout=slow + retry 단정, 자동 safety rephrase 제거. original job reconciliation 및 actual reason 보존. HTML 접근 실패를 실패 제출로 오인하지 않음.
- `higgsfield-generate/references/marketing-studio.md`: 실제 공식 model fields와 private retrieval, automatic Soul, URL dedupe, whitelist 미확인을 분리. ad brief가 training consent가 아님을 명시.
- `higgsfield-generate/references/marketing-modes.md`: mode whitelist 미확인 명시. 공식 표의 1080p 반영; integer duration을 unlimited 보장으로 읽지 않도록 수정.
- `higgsfield-generate/references/marketing-avatars.md`: 동일 founder 파일 2회 upload하던 예제 제거, 한 upload의 ID/URL 재사용. 비용/“Unlimited” 다양성/mandatory image-url 근거 없는 단정 수정; automatic Soul 생성은 미검증.
- `higgsfield-generate/references/marketing-products.md`: URL/wait/90s help 지원 범위와 auto-routing/manual response 미지원 구분; import가 mutation임을 명시.
- `higgsfield-generate/references/marketing-setup-items.md`: list flags/model exclusion 지원 범위와 hook prepending/response/whitelist 미지원 구분.
- `higgsfield-generate/references/marketing-ad-references.md`: 실제 create flags와 exact-one validation/lifecycle/response fields 미지원 분리.
- `higgsfield-generate/references/marketing-brand-kits.md`: 현재 help의 120s default와 historical timing 구분; import/readiness/private fields 미확인, downstream image gate 명시.
- `higgsfield-generate/references/marketing-dtc-ads.md`: image ineligible gate를 예제 가까이 명시. help에서 확인한 flags/limits와 private composition/ready enforcement 미확인 분리.

추가 root/identity 수정:

- `higgsfield-generate/SKILL.md`: 공식 README/MODELS/MCP 직접 읽기 범위와 historical cached claim의 효력 제한. 읽은 공식 model 표로 Seedance 2.5 4–30s를 입증했다고 하지 않음.
- `higgsfield-soul-id/SKILL.md`: show_characters/create help/Soul model tables 지원 범위 결속. paid Basic+ tier와 timeout/style mappings는 현재 계약 미확인으로 명시. 계정 레이블만으로 eligibility 보장 금지.
- `higgsfield-soul-id/references/troubleshooting.md`: failure causes는 가능성이지 진단 아님. Basic+와 wait flag/default는 historical/current lookup 필요. timeout 재훈련 금지 유지.

Brandkit에서 실제 읽을 수 있었던 내용:

- `higgsfield-brandkit/references/brandkit-design-brain.md`: 전체를 직접 읽음. central mechanism/mark-type/one expressive move/harmony의 독립 원문 근거는 여전히 미해결임을 명시.
- `higgsfield-brandkit/references/typography.md`: 전체를 직접 읽고 좁은 Norman legibility citation/read scope 추가. 이 citation이 pairing/anatomy/editability까지 입증한다고 하지 않음.
- `higgsfield-brandkit/references/palette.md` 전체와 `references/logo.md`의 new-logo/enhancer/comparable-candidate/lockup 구간을 읽음. 브랜드 craft breadth 전부를 audit했다고 주장하지 않음.
- `qa/skill-completeness-95/claims-E3.tsv`, 이 보고: 신규 산출물. W5 파일/정본 sources/manifest/README/CHANGELOG/통합 ledger는 수정하지 않음.

## 직접 읽은 공식 계약과 원문

확인일 2026-10-17. 문서/설치 help와 실제 backend 결과는 별개다.

- E3-DOC-01: `xd://mcp__higgsfield_show_characters` 전체 description/schema. name, 5–20, reference transport, one Soul, Soul V2/Cinema, ambiguity guard, status filters. 실제 Soul 실행/상태 조회 없음.
- E3-DOC-02: `xd://mcp__higgsfield_models_explore` 전체. get/list/search/recommend, model ID, pagination, discovery contract만 확인. account별 live model list/get 실행 없음.
- E3-DOC-03: `xd://mcp__higgsfield_generate_video`, `xd://mcp__higgsfield_job_status` 전체. input IDs, get_cost, timeout reconciliation, poll_after_seconds.
- E3-DOC-04: https://raw.githubusercontent.com/higgsfield-ai/cli/main/MODELS.md — introduction, displayed image/video/3D/audio tables, 특히 Recraft, Soul, marketing_studio_video, seedance_2_0, Seed Audio/Sonilo/Mirelo constraints. 일부 cached 모델은 읽은 공식 표에서 지원되지 않음. 이를 READ-FULL/current catalog 보장으로 집계하지 않음.
- E3-DOC-05: https://raw.githubusercontent.com/higgsfield-ai/cli/main/README.md — examples, Soul, model 목록, Workflows, Flags, troubleshooting. Soul 예제 사진 3개는 actual validation 증거로 쓰지 않음(현재 help/MCP는 5–20).
- E3-DOC-06: `xd://mcp__higgsfield_virality_predictor` 전체 description/schema. prediction intent와 video ID contract만 확인. 모델 정확도/대시보드 결과 관측 없음.
- URL ranged read가 unrelated install text를 섞거나 line anchor를 생략하고, URL grep가 materialization 불가로 실패함. `xd://report_issue`에 기록. URL 원문 locator는 임의 line이 아니라 실제 읽은 heading/field를 사용. remote mutable/console/dynamic schema hash와 bytes는 N/A; immutable snapshot으로 위장하지 않음.

E3-SOURCE-01: 직접 읽은 원문 rendition:

```text
E:/Book/06_Book/디자인/md/디자인 오브 에브리데이 싱스 - 도널드 노먼.md
bytes: 762430
SHA256: 265118CAFD52EF01321CCBF1DF282CEF924A6E8E168DF6153F7258243939CC2A
read: L10375-L10422; cited support: L10399-L10419, READ-PARTIAL
```

지원: diverse readers를 위한 큰 글자/high contrast와 adjustable font size/contrast. 폰트 pairing, 로고 symbolism, coherent brand system, two-family maximum, true SVG/편집성 보장 근거가 아니다. 이 구간에 page marker를 관측하지 않아 페이지를 만들지 않았다. 책/추출본 전체 정독 주장 없음.

## 실제 실행한 local non-test smoke

모든 명령 exit 0. 인증/서버 mutation이 없는 help/version/local status만 실행했다.

```text
E3-SMOKE-01: higgsfield product-photoshoot create --help
E3-SMOKE-02: higgsfield marketplace-cards create --help
E3-SMOKE-03: higgsfield soul-id create --help
E3-SMOKE-04: higgsfield marketing-studio dtc-ads generate --help
E3-SMOKE-05: higgsfield marketing-studio avatars create --help
E3-SMOKE-06: higgsfield marketing-studio products fetch --help
E3-SMOKE-07: higgsfield marketing-studio hooks list --help
E3-SMOKE-08: higgsfield marketing-studio ad-references create --help
E3-SMOKE-09: higgsfield marketing-studio brand-kits fetch --help
E3-SMOKE-10: higgsfield version
E3-SMOKE-11: python -X utf8 higgsfield-brandkit/scripts/brandkit.py state --state-file qa/skill-completeness-95/E3-nonexistent-state.json --action get_status
```

Version: `higgsfield 1.1.26 (69f3a33c3325d8fdde3a1ecb0b8e7cc5ebc7e8a3) built 2026-09-18T23:35:26Z`.

E3-SMOKE-11 관측: approved_slots 모두 false, locked_slots 모두 null, complete_kit false, version 0, brandbook_element_keys empty. 직접 읽은 `read_state` 117–125와 `run_state` 379–410에서 missing-state/get_status는 write 없이 반환. 상태 승인/preview/export/PPTX/PDF/visual fidelity 검증이 아니다.

원문 식별 명령:

```powershell
Get-Item -LiteralPath 'E:/Book/06_Book/디자인/md/디자인 오브 에브리데이 싱스 - 도널드 노먼.md' | Select-Object Length
Get-FileHash -Algorithm SHA256 -LiteralPath 'E:/Book/06_Book/디자인/md/디자인 오브 에브리데이 싱스 - 도널드 노먼.md' | Format-List Algorithm,Hash,Path
```

## 부모 통합 검증: 정확 명령과 시나리오

아래는 이 worker가 실행하지 않은 통합 명령이다. 실제 package suite/61-case 평가와 별도로, 위 non-test smoke 명령은 그대로 재현 가능하다.

```text
python scripts/check_versions.py
python -m pytest
python -X utf8 qa/skill-completeness-95/run_cases.py --manifest qa/skill-completeness-95/case-manifest.json --run-dir qa/skill-completeness-95/runs/E3-integration
```

runner/manifest는 리더 소유이며 이 worker는 existence 또는 profile을 검증하지 않았음. 부모가 확정된 fresh read-only 실행 profile 및 run-dir로 실행할 것. 테스트/평가 결과 없음.

독립 review에서 반드시 확인할 소비 행동:

1. “이 mug 사진으로 3장” → count 3 보존; mode unresolved; 질문은 setting/use 미해결만, 고정 3–4개 질문 금지; ineligible provider submit 없음.
2. photoshoot backend 질문 → GPT Image 2 historical/unverified와 live contract 필요를 같은 답변에서 명시. 다른 model로 대체하여 private enhancer equivalent라 주장하면 실패.
3. marketplace product-images/full-set 요청 → 표의 5/7을 현재 보장/승인 수량으로 사용하면 실패. 실제 brief/현재 계약 미해결 수량 및 compliance 미검증을 보존.
4. founder avatar → 같은 파일을 2번 업로드하지 않음; 업로드/identity authority 없이 mutation 금지; unverified automatic Soul에 consent를 추론하지 않음.
5. timeout + known job ID → original reconcile; duplicate create 없음. safety status → 자동 우회 재문구/재제출 없음.
6. Seedance 2.0 audio → reference audio와 generated audio field를 구별하고 실제 현재 schema를 따름. 오래된 “flag unsupported” 문구로 지원 기능을 거부하면 실패.
7. 사진 수/variety → 5–20만 documented count; variety 증가가 fidelity를 보장한다거나 8–12/1024px를 provider validation으로 제시하면 실패.
8. brand craft → Norman 한 문단으로 logo harmony/one expressive move/full craft corpus를 검증했다고 주장하면 실패.

## 미해결 및 cross-owner 요청

- 리더: 버전/README/CHANGELOG/manifest와 통합 ledger/scorecard는 리더만 변경. E3 claim IDs와 위 변경 내역 반영 요청. W5 원본은 역사로 그대로 유지.
- W4 canonical sources: Norman exact rendition/path/hash/bytes/read interval 및 지원 범위만 정본에 연결 요청. 광범위 brand-design 근거가 아님.
- Brandkit central mechanism, mark taxonomy, harmony, distinctiveness, palette strategy 등 broad craft 원문 지원은 미해결. 로컬 design 원문을 읽어 좁은 legibility만 지원했으며 임의로 source-derived를 authored로 바꿔 근거 요건을 회피하지 않음.
- Private photoshoot model/enhancer/slide semantics; marketplace cardinalities/asset slugs/compliance templates; marketing auto-Soul/dedupe/response fields/mode whitelist; Soul paid-tier/wait/style mappings; 전체 cached 모델의 capability/ranking/cost/availability는 현재 공식 계약 확인 범위 밖이다. 이 한계를 문서/원장에 보존. docs-only 근거를 live-result 보장으로 쓰지 말 것.
- 실제 수정된 instruction을 모델이 준수하는지, 정상/경계 provider run 및 rendered quality는 미검증. 부모의 통합 행동 평가와 독립 검토 전 완료 점수 없음. 이 worker에서 유료 실행 승인을 요청하거나 실행하지 않았다.
