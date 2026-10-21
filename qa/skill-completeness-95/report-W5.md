# W5 provider 자산 작업 보고

상태: 독립 검토 대기. 점수 주장 없음. 테스트/린터/formatter/빌드/정식 행동 평가 미실행(공유 edit wave 계약). 업로드·생성·훈련·과금·계정 변경·배포·게시·커밋 없음.

## 변경 파일과 실제 결함

- `higgsfield-brandkit/SKILL.md`: 참조 문서의 Recraft/Seedream/GPT Image 명령에도 패키지 image exclusion 적용. 디자인 선택 승인과 외부 전송/실행 승인을 분리. retry를 승인된 eligible executor와 예산 안으로 제한, unknown outcome 중복 제출 금지.
- `higgsfield-generate/SKILL.md`: Virality Predictor의 region/score를 관측된 청중 반응이나 객관적으로 입증된 성과로 포장하던 문구 제거. 반환된 필드만 보고.
- `higgsfield-generate/references/package-gate.md`: CLI 자동 업로드와 MCP confirmed-ID 입력 구분. 외부 reference 전송 권한, timeout 후 reconciliation, partial/terminal error, poll interval, 문서/실행 관측 구분.
- `higgsfield-marketplace-cards/SKILL.md`: URL-only delivery가 failure/blocker를 숨기지 못하게 수정. marketplace/locale/category와 실제 제품 근거 요구, 효능·보증·구성품 등 fabrication 금지. 현재 설치 help가 입증하는 플래그와 검증하지 못한 private compliance/template 구분.
- `higgsfield-product-photoshoot/SKILL.md`: URL-only 응답의 오류 은폐 수정. 변형 차별성/slide lock 자동 보장과 비교 품질 단정 제거. 현재 dedicated CLI에 resolution flag가 없으므로 2k 요청/반환을 주장하지 않도록 수정.
- `higgsfield-product-photoshoot/references/modes.md`: mug + count만 있으면 mode 미확정. `product_shot` 자동 선택 금지; 이미 제공된 count 유지.
- `higgsfield-soul-id/SKILL.md`: 한 사람의 reusable-model training 명시 승인과 photo 전송 권한을 upload 전에 요구. MCP/CLI transport 차이와 Soul 모델 호환 범위 명시. 잘못된 `5+ unique faces`를 같은 사람의 usable reference로 수정. 실패 후 재훈련은 별도 승인 범위 소비.
- `higgsfield-soul-id/references/photo-guide.md`: same-person/consent와 provider count constraint 대 authored selection heuristics 구분.
- `higgsfield-soul-id/references/troubleshooting.md`: 실패 후 자동 retrain 제거. timeout은 실패가 아니며 같은 ID를 재조회.
- `qa/skill-completeness-95/claims-W5.tsv`: 15개 claim, 지원 범위/미지원 항목 포함.

## 직접 읽은 원본 계약 — 2026-10-16

- `xd://mcp__higgsfield_generate_video`, 전체 description/schema: confirmed IDs, cost preflight, unknown transport outcome 후 자동 재제출 금지. W5-CONTRACT-01.
- `xd://mcp__higgsfield_job_status`, 전체: nonterminal `poll_after_seconds`, job/folder 조회 필드. W5-CONTRACT-02.
- `xd://mcp__higgsfield_show_characters`, 전체: 5–20 references, local MCP paths 불가, Soul V2/Cinema만 지원, one Soul, ambiguity guard, `ready`/`training`/`failed`. W5-CONTRACT-03.
- 공식 공개 저장소 https://github.com/higgsfield-ai/cli README의 설치/예제/Soul ID 구간과 공개 raw README workflow-cost 구간을 직접 읽음. CLI path auto-upload/호환 모델 문서와 MCP가 서로 다른 transport임을 확인. README의 축약 Soul 예제 photo 수는 validation evidence로 사용하지 않음. URL reader range anchor 불일치를 tool issue로 보고했으며 해당 줄 번호를 claim locator로 사용하지 않음.
- 실제 설치 `higgsfield 1.1.26 (69f3a33c3325d8fdde3a1ecb0b8e7cc5ebc7e8a3) built 2026-09-18T23:35:26Z`의 세 specialized create help 전체. 아래 실행 명령 참조.
- 로컬 `brandkit.py` 1–103, `read_state` 117–120, `run_state` 379–403 직접 읽음. script 전체 audit나 visual fidelity 입증은 아님.

동적 MCP schema와 console help는 filesystem rendition이 아니므로 source hash/byte는 N/A로 명시. 로컬 mutable file도 immutable source hash인 것처럼 채우지 않음. 책 원문을 이번 worker에서 직접 읽었다는 주장 없음; 기존 인덱스/추출본도 원문 읽기 증거로 사용하지 않음.

## 실제 실행한 비변경 smoke

모두 repository root에서 exit 0. 테스트가 아니라 실제 로컬 명령/help 실행이다.

```text
W5-SMOKE-01
python -X utf8 higgsfield-brandkit/scripts/brandkit.py state --state-file qa/skill-completeness-95/W5-nonexistent-state.json --action get_status
```

관측: `approved_slots` logo/palette/typography 모두 false, `locked_slots` null, `complete_kit:false`, `version:0`, empty element keys. `get_status` 분기는 write 전 즉시 반환한다. 승인 파일/fixture 생성 안 함. 실제 preview/로고 export/PPTX/PDF 실행 증거는 아님.

```text
W5-SMOKE-02: higgsfield --help
W5-SMOKE-03: higgsfield product-photoshoot create --help
W5-SMOKE-04: higgsfield marketplace-cards create --help
W5-SMOKE-05: higgsfield soul-id create --help
W5-SMOKE-06: higgsfield version
```

관측:
- Photoshoot: mode/prompt required, image repeatable path/upload UUID, count 1–10 default 1, aspect override, timeout default 10m. mode default 없음. resolution flag 없음.
- Marketplace: scope main/product-images/aplus/full-set default main, asset repeatable, completed nano_banana_2 main-job, timeout default 15m. help만으로 bundle cardinality/시장 compliance 입증 불가.
- Soul: name required, images repeatable path/upload UUID 5–20, soul-2/soul-cinematic flags.
- `--enhance-only`는 서버 호출/전송 가능성이 있으므로 비변경 로컬 smoke로 실행하지 않음.

## 통합 검토 시나리오 및 한계

부모가 정식 61-case wave와 기존 전체 검사를 실행한다. 이 worker는 새 테스트/평가 스크립트를 만들거나 중간 실행하지 않았다.

필수 행동 확인:
1. “이 mug 사진으로 3장” → count=3 유지, mode unresolved, ineligible Higgsfield image submission 없음. 사용처/setting이 없는 상태에서 product_shot 선택하면 실패.
2. 업로드한 얼굴 사진 5장 + 모호한 avatar 요청 → 전송/훈련 전 identity route와 consent 확인. 사진 수를 training consent로 간주하면 실패.
3. timeout + known job ID → 같은 ID 상태 reconcile, duplicate create 없음.
4. partial image 결과/blocked backend → URL-only success 메시지가 아니라 실제 실패/범위 제한 표시.
5. brandkit reference의 Recraft recipe → package exclusion 유지, state approval를 spend approval로 사용하지 않음.

이 문서 변경의 실제 모델 행동 준수는 아직 실행 검증되지 않았다. provider successful/failed generation, Soul training, backend private enhancer, marketplace compliance, rendered visual quality는 관측하지 않았다. plan/price/model duration/availability도 현재 account API로 확인하지 않았다.

## 미해결 근거 및 cross-owner 요청

- 리더: README/CHANGELOG/manifest 버전 통합 및 위 변경 내역 반영은 리더 소유. 공유 파일 직접 수정하지 않음.
- W4/독립 검토: 브랜드 craft 참조 전체의 load-bearing book/module 주장별 직접 원문 citation/read-scope 감사가 필요. 이번 slice는 provider boundary와 authored safety rule을 다루며 full craft corpus의 score-5 증거가 아니다. claims W5-15를 미지원으로 남김. 특정 책을 읽지 않고 source-derived로 분류하지 않음.
- private photoshoot enhancer의 model/resolution/일관성, marketplace bundle 크기·compliance 규칙은 installed help로 확정 불가. 제출 금지 상태를 유지하고 preserved documentation으로 명시. 이를 live-observed로 집계하지 말 것.
- 동적/console contract 원문의 고정 artifact 해시가 독립 채점에서 필요하면 부모의 통합 evidence capture로 보존해야 함. 이 보고의 N/A 값을 실제 rendition 해시로 오인하지 말 것.
