# E1 — W1 craft evidence completion / 독립 검토 인계

## 결과와 변경 파일

기존 W1 보고·claim slice를 먼저 읽고 W1-09/10의 미완료 craft 근거를 이어서 처리했다. 점수·전체 완료·행동 평가 PASS를 주장하지 않는다. `claims-E1.tsv`는 40개 claim / 5개 소유 스킬 / 16열이다. borrowed craft·psychology는 source-derived로 유지했다.

변경한 소비 파일:

1. `developing-video-synopses/references/synopsis-craft.md`: personal/documentary, brand, mood, metaphor, emotion-through-action/detail/sound/concerns, data-story 각 소비 지점에 S1–S6 연결. 원본 rendition 경로·SHA-256·bytes·구간·READ-PARTIAL·지원 한계를 설치되는 참조 안에 추가했다. 기존 McKee 메타데이터와 M-09/frozen scope는 보존했다.
2. `storytelling-with-still-images/SKILL.md`: order/montage, hold/rhythm, sound meaning, selective dialogue mix를 원본에 연결. film-to-still 적용은 제안이며 고정 hold 길이나 retention 효과가 아님을 구분했다. 기존 still-only/read-only/assembly/publication·실제 crop 검사 및 v7 한계는 보존했다.
3. `creative-production/references/video-generation-planning.md`: 공식 Gen-4 guide를 직접 읽어 단순한 물리적 행동·motion-focused i2v의 적용 범위를 한정했다. 실제 결함: Gen-4는 negative phrasing을 거부하므로 “minimal negatives”만으로 충분하지 않다. positive target branch를 명시했다. Blender reference를 exact AI continuation으로 오해시키던 recipe/goal 문구도 reference + inspection으로 교정했다. FLF2V·V2V·interactive·ComfyUI capability는 실제 endpoint/workflow 증거 없이 확정하지 않는다.
4. `creative-production/references/video-prompt-dialects.json`: 실제 파일은 `.md`가 아니라 `.json`이다. 네 패턴의 형태·조건은 그대로 보존하고 `_meta.evidence_scope`에 authored serialization과 provider capability의 차이를 명시했다.
5. `qa/skill-completeness-95/claims-E1.tsv`: 실제 지원 구간별 40개 행.
6. 이 보고서.

공유 manifest/README/CHANGELOG/통합 state·ledger·scorecard/canonical sources는 수정하지 않았다. 커밋·리셋·설치·설정/인증 변경·업로드·미디어 생성·지출·훈련·배포·게시 없음. 모든 tests/full arm/linter/formatter는 부모에게 유보했다.

## 파일·claim 범위 전체 대조

| 소유 파일/표면 | E1 범위와 claim | 판정 한계 |
|---|---|---|
| developing-video-synopses/SKILL.md | S15: scope, input, invocation, acceptance, handoff 확인; 변경 없음 | 긴 invocation 표시가 일부 잘림. linked cross-owner 계약을 재인증했다고 하지 않음. M-09 재실행 없음 |
| synopsis-craft.md | S01–S14: 모든 mode bullet, artifact/accuracy/self-check/boundary 구분 | 새 evidence binding 전반은 본 작업자의 직접 부분 원문 읽기. 행동 효과는 fresh-session 검증 전 |
| storytelling-with-still-images/SKILL.md | T01–T05: Principle, scope, Workflow 1–6, cue table, v7, Acceptance 전부 | 실제 still·audio·crop·playback 검사 없음. 새 source binding이 그 검사를 대신하지 않음 |
| creative-production/SKILL.md | C02: routing, stage, approval, state, execution 경계 확인; 변경 없음 | 긴 일부 행 잘림. 전체 lifecycle 통합 테스트/교차 owner 정본 감사 아님 |
| video-generation-planning.md | P01–P06: §§1–7; 특히 prompt 규칙과 모든 hybrid recipe, 57번 긴 composite 행도 별도 직접 읽음 | P05 실제 endpoint/workflow capability는 미검증 |
| video-prompt-dialects.json | D01–D04: `_meta`와 narrative/production-spec/edit-command/interactive 전부 | 실제 JSON 소비 스모크만 실행. provider syntax 실행 아님 |
| production-routing.md | C03: core routes/runtime/state 확인; 변경 없음 | 긴 image-backed package 행 일부 잘림. downstream 정본은 각 owner/부모 |
| production-routing-optional.md | C05: route/catalog/fallback 확인; 변경 없음 | 긴 catalog 설명 일부 잘림. preset·license·ArtCraft feature mapping의 live 증거 미해결 |
| creative-qa.md | C04: 전체 직접 읽음; 변경 없음 | QA 절차를 읽은 것이 실행 증거는 아님 |
| workspace-integration.md | C06: 전체 직접 읽음; 변경 없음 | 조건부 adapter이며 현 호스트에서 ChatGPT Work 도구를 검증하지 않음 |
| marketing-source-adaptation.md | C07–C08: 전체 직접 읽음, Dunford 원본 재독; 변경 없음 | FFmpeg SAR/filter 실행과 법적 보편 명제는 이번 craft correction에서 검증하지 않음 |
| topic-demand-selection/SKILL.md | Q01: 전체 직접 읽음; objective/evidence scope 포함 부모 변경 보존 | 비교·의사결정 정책이지 예측 성능 근거가 아님. 스코프를 새로 변경하지 않음 |
| recording-production-history/SKILL.md | H01–H02: 전체 직접 읽음; 변경 없음 | Python 구현·테스트는 재실행하지 않음. W1-S05를 E1 실행으로 전용하지 않음 |
| recording-production-history/scripts/production_history.py 및 test_production_history.py | 소유 파일이나 E1 craft 수정 비대상, 변경/재검증 없음 | atomicity/masking/platform/path-safety 새 보증 없음 |
| creative-production/{evals/evals.json,agents/openai.yaml,assets/icon.svg}; developing-video-synopses/{evals/evals.json,agents/openai.yaml}; storytelling-with-still-images/evals/evals.json | 파일 inventory만 확인; craft 소비 본문이 아니며 변경 없음 | 내용 직접 읽기·테스트 완료로 주장하지 않음 |

위 표는 모든 소유 파일의 처리/비처리를 설명한다. 다른 owner의 storyboard/shot/production-execution/retry/lifecycle 참조까지 evidence complete로 선언하지 않는다.

## 직접 읽은 원본과 정확한 지원 범위

모든 아래 book 항목은 READ-PARTIAL이다. 전체 책 정독을 주장하지 않는다. 경로·bytes·SHA-256은 claim 행 및 설치 소비 파일에 있다. 해시/bytes는 원본 `Path.stat()`/`read_bytes()`/`hashlib.sha256()`로 관측했다. 원문을 QA에 복제하지 않았다.

| 원본 rendition | 직접 읽은 구간 | 쓰인 주장 / 한계 |
|---|---|---|
| McKee, originals/시놉시스/Story Substance…md, 839168 bytes, SHA `6271c7cab58a80824c95317730b31428e328d2a9da0ed24e32e246402b20e3a2` | L1730–1758; L7850–7880 (인용은 L7855–7876) | 고전 서사의 인과, character wants/value transition. 주변의 “오직 두 감정”을 과학적 사실로 채택하지 않음 |
| Habermas, originals/콘텐츠_제작/md/감정과 서사 - 틸만 하버마스.md, 952320 bytes, SHA `4e7dc3f8b2a1f448fc00df883fa2e5a475b0f590b84af583603ed6a5caa325aa` | L49; L177–189; L239 | concerns/appraisal, author/narrator/protagonist, event selection/blame, past/present, non-plot mood. 진단/정서 반응 보장 아님 |
| Miller, originals/SNS/pdf/Building a StoryBrand 2.0…md, 400763 bytes, SHA `9a85987a81e82ec275fac69bbb5b40faebe056cbacde5983b5d3007bee57c2df` | L1050–1105; 인용 L1054–1083 | customer hero/brand guide의 조건부 framework. 판매 효과나 universal hero 법칙 아님 |
| Heath/Heath, originals/마케팅/Made to Stick…md, 577086 bytes, SHA `6e78a1bccc8c4db25cc41f1581744fd5b0d1068b0fa4a758bce6921532d73656` | L590–610; L1160–1230; 인용 L1176–1225 | core message 우선순위와 familiar schema/analogy 한계. 두 domain/limit 필드는 로컬 정확성 검사 |
| Pearlman, originals/콘텐츠_제작/md/Cutting Rhythms…md, 547079 bytes, SHA `e09d86df3f28ef5e4351e16296a0e26528dfc1ca78aff9abc2c4a7962744e49e` | L149–155; L561 및 후속 conclusion 문맥 | cut point/duration/placement, performance/sound의 emotional rhythm; 자료에 따라 적용. still-only 최적 길이의 실증 아님 |
| Reisz/Millar, originals/콘텐츠_제작/md/Technique of Film Editing…md, 910909 bytes, SHA `0b371150dea868a263f3de41d28b9e220cad8db9a3b21f6e540ce0655a970a55` | L73–79, L97, L235–245 (인용 L239–243), L263, L477–479 | significant detail, juxtaposition/order, sound meaning, documentary theme/reportage, selective dialogue mix. L263은 sequence description이며 dialogue priority 근거로 쓰지 않음 |
| Mason, originals/콘텐츠_제작/md/마음을 담아 쓰기 - 씨에이 메이슨.md, 243115 bytes, SHA `ed4d32cf9e5c369d6269cd99c1024a546a5e8bac9c3c034aff08a8d2f127b684` | L1–9 title 확인, L61–65 | Writing With Heart 실제 title 확인; sensory detail의 문학 craft 조언. 심리 효과 측정치 아님 |
| Lo Duca, originals/콘텐츠_제작/md/생성형 인공지능 데이터 스토리텔링 - 안젤리카 로 두카.md, 648867 bytes, SHA `d25ff3e24574e2b16953eddcb3a8b33aae6a72e07e057ead47380e49b1940791` | L23–29는 TOC discovery만, 실제 증거 L317–319 | insight/context/reflection/next steps. construction order와 audience arc를 구분; question-first를 원문 순서로 위장하지 않음 |
| Dunford, originals/마케팅/Obviously Awesome How to Nail Product Positioning…md | L983–1038 | 기존 W1 alternate rendition binding 재독. metadata 보존; 고객 비교 대안/상대적 차별화만 |
| Ursyn, originals/콘텐츠_제작/md/새로운 스토리텔링 - 안나 우르신.md, 561664 bytes, SHA `14f9613a55dee036425bf06a0c55d18072e785018222d40f6c401ec3d1734862` | L319–323 | 실제 읽었으나 이 부분은 mapping-limit 체계를 입증하지 않아 load-bearing 근거로 채택하지 않음. Heath 구간을 사용 |

공식 provider 원문: [Runway Gen-4 Video Prompting Guide](https://help.runwayml.com/hc/en-us/articles/39789879462419-Gen-4-Video-Prompting-Guide), 2026-10-17 직접 읽기. READ-PARTIAL 범위는 Prompting for Iteration, Best Practices, Image prompts, Subject Motion. simple physical motion, image-carried appearance, positive-only prompting을 지원한다. URL/heading은 locator이며 live HTML의 immutable byte/hash snapshot은 없다. 실제 endpoint 제출이나 결과 품질 입증은 아니다. 최초 `docs.dev.runwayml.com/assets/prompting-guide/`는 404였고 공식 help 검색→직접 읽기로 대체했다. Blender alpha-over 문서의 시도 URL도 404였으며 근거로 채택하지 않았다.

## 실제 로컬 확인과 수동 적용 산출물

### E1-C01 — dialect JSON의 실제 소비 (exit 0)

실행 명령:

```text
python -X utf8 -c "import json; from pathlib import Path; d=json.loads(Path('creative-production/references/video-prompt-dialects.json').read_text(encoding='utf-8')); print(d['_meta']['purpose']); print('PLANNING EXAMPLES ONLY; no endpoint selected, no submission'); [(print(k+' | '+v['condition']+' | '+v['example'])) for k,v in d['genres'].items()]; print('NEGATIVE-PHRASING CASE: Gen-4 planning target = Locked camera. The camera remains still.'); print('HYBRID HANDOFF CASE: Blender camera/composition reference -> generated result remains UNVERIFIED until actual inspection.')"
```

관측: 실제 JSON이 parse되었고 네 패턴의 실제 `condition`과 `example`이 출력됐다. narrative의 flower-bud motion, production-spec의 cup grasp/lift/end-state, edit-command의 background replacement/preserve-list, interactive의 forward/stop target이 각각 출력됐다. 마지막 negative/hybrid 두 줄은 이 작업자가 넣은 설명 문자열이며 **skill engine이 규칙을 준수했다는 테스트가 아니다**. endpoint 선택·제출 없음.

### E1-C09 — claim ledger의 실제 TSV ingestion (exit 0)

```text
python -X utf8 -c "import csv; from collections import Counter; from pathlib import Path; p=Path('qa/skill-completeness-95/claims-E1.tsv'); rows=list(csv.DictReader(p.open(encoding='utf-8'),delimiter='\t')); print('claims',len(rows)); print('skills',dict(Counter(r['skill'] for r in rows))); print('classes',dict(Counter(r['class'] for r in rows))); print('column_counts',dict(Counter(len(r) for r in rows))); print('extra_columns',sum(None in r for r in rows)); print('missing_cells',sum(any(v is None for v in r.values()) for r in rows)); print('unique_ids',len({r['claim_id'] for r in rows})); print('unsupported',[(r['claim_id'],r['claim_summary']) for r in rows if r['class']=='unsupported'])"
```

관측: 40 claims, unique IDs=40, 모든 row 16열, extra_columns=0, missing_cells=0. 분류 18 source-derived / 18 authored-design / 2 provider-contract / 2 unsupported. 스킬별 synopsis 15 / still 5 / coordinator 17 / topic 1 / history 2. 이것은 parsing/범위 확인이며 source sufficiency 또는 behavioral PASS가 아니다.

### E1-M01–07 — 이 작업자의 텍스트 수동 적용 (fresh-session test 아님)

- **M01 personal/documentary:** 합성 입력 “목격자가 10년 전 구조 현장을 회고; 현재 확인된 사실은 신고와 도착뿐”. 산출: narrator=목격자, protagonist=구조 대상, witnessed fact=신고·도착, unknown=구조 원인/타인의 내면. 당시 관찰과 현재 회고를 별도로 쓴다. 구조 영웅 역할이나 타인의 심리를 추가하지 않는다. 사건 순서를 바꿔 원인을 만들어내지 않으며 theme-led 회고는 허용한다.
- **M02 brand/mood:** 합성 입력 “자전거 수리점의 고객 안내; 가격/후기 미제공”. 산출: 고객의 문제=이상 소리, 가이드=점검 절차, 핵심 메시지=확인된 점검 범위 안내. “최저가/반드시 해결/인기”는 없음. 별도 no-plot mood brief는 차가운 색→따뜻한 색 및 잔향 변화의 제안만; 등장인물/CTA/행복한 결말을 넣지 않음. 정서 효과는 제안이지 관측 아님.
- **M03 metaphor:** 합성 교육 입력 “전기 흐름을 물에 비유”. source domain=물의 흐름, target=전기 회로, shared mapping=흐름/저항을 이해하기 위한 제한적 비유, limit=전하를 실제 물 입자와 동일시하거나 모든 전자기 현상을 설명하지 않음. 비유와 실제 회로 설명을 구분한다. 이 예시는 물리학 수업의 검증된 완성 설명이 아님.
- **M04 emotion:** 합성 fiction “인물이 편지를 잃을까 걱정”. 산출: concern=편지 보존, action=주머니를 다시 확인하고 손을 떼지 못함, sensory/sound=종이가 구겨지는 소리. “불안함”이라는 라벨만 되풀이하지 않지만 라벨 금지 법칙도 만들지 않음. 실제 인물 진단이나 특정 관객 반응을 주장하지 않음.
- **M05 data:** 합성 동일 단위 관측 A=12k, B=4k, C=no-data. 산출: A/B=3, C=unknown. 설명 흐름은 질문→관측/산술→같은 window라는 context→원인 unknown→추가 비교 제안. 원인/예측/CTA를 데이터로부터 만들어내지 않음. 이 경로에서 audience arc를 DIKW 제작 순서와 동일하다고 부르지 않음.
- **M06 still cue:** 합성 unseen S1/S2, 총 12초 제안. `0–5 estimated | S1 proposed—not inspected | “주소를 다시 확인했다.” proposed narration | silence/cut`; `5–12 estimated | S2 proposed—not inspected | “편지를 돌려주기로 했다.” proposed narration | silence/end`. 12초는 배분 산술이며 speech duration 측정이 아님. 실제 audio가 8초+7초라면 12초에 억지로 맞추지 않고 hold/runtime conflict를 표시한다. BGM이 없으므로 mix를 실행했다고 하지 않음. S1 callback이나 evidence-arc 전 단계를 강제하지 않음.
- **M07 prompt/hybrid:** Gen-4 planning “카메라 움직임 없이” → positive target `Locked camera. The camera remains still.`; negative field 자동 삽입 없음. input image의 정적 외형을 재서술하기보다 requested motion만 제안. 다른 endpoint가 identity restatement를 요구한다면 해당 계약을 따름. Blender→AI 결과에서 camera/geometry 유지 상태는 아직 UNVERIFIED. FLF2V가 미확인인 상태에서는 긴 시퀀스의 clip 경계 계획은 가능하나 chain submission은 하지 않음. interactive JSON 예시를 Gen-4 batch syntax라고 제시하지 않음.

실제 미디어가 없고 사용자 계약이 tests/full arm을 금지하므로 위 수동 적용은 통합 fresh-session 행동 검증의 대체물이 아니다. JSON 소비와 TSV ingestion 이외의 실행 성공을 주장하지 않는다.

## W1 미해결 항목의 처리와 남은 정확한 gap

- **W1-10:** documentary/personal/brand/metaphor/emotion 세부를 S02–S12로 분해해 직접 원본에 연결했다. S13 data, S07 mood도 함께 커버했다. 인용에 없는 심리적 효과·최적 구조를 authored-design으로 세탁하지 않았다. 적용 절차/승인/사실성/필드만 로컬 계약으로 구분했다.
- **W1-09:** Gen-4 prompt 성격은 P01–P02로 공식 원문에 연결했고, blanket i2v·negative·exact hybrid 표현을 수정했다. **남은 P05:** 특정 실제 endpoint의 first/last-frame role, time-addressed action, reference-to-video, V2V edit verbs 및 실제 ComfyUI node/model/memory contract. endpoint/workflow가 선택되지 않았으므로 보편적 capability를 확정할 수 없다. 로컬 책으로 모델 API를 증명할 수 없다. 이 gap은 실행 전 증거 gate로 그대로 남고 텍스트 planning은 유지된다. 선택된 backend가 있을 때 부모/provider owner가 공식 schema를 읽고 해당 claim만 검증해야 한다.
- **기존 C05:** optional provider preset inventory·ArtCraft license/features/mappings은 live 검증하지 않았다. host discovery를 했다는 새 주장도 없다. W1 보고의 이 한계를 유지한다. 다른 owner의 provider source를 임의 교체하거나 catalog 기능을 지우지 않았다.
- C08의 FFmpeg filter/SAR와 저작권·권리 문장은 이번 요청의 named craft slice 밖이며 재실행/법적 보편 증명 없음. H02 history atomicity/security도 E1이 새로 검증한 것으로 합산하면 안 된다.
- 단일 file citation의 READ-PARTIAL을 full skill evidence complete로 승격하면 안 된다. 원본 읽기와 manual application은 rubric의 exercised independent behavior review를 대신하지 않는다.

## 교차 owner 요청

1. **W4 / canonical sources:** `claims-E1.tsv`의 E1-MCKEE/HABERMAS/MILLER/HEATH/PEARLMAN/REISZ/MASON/LODUCA exact rendition metadata·locators를 해당 canonical work/rendition 아래 연결해 달라. 기존 다른 rendition·source ID를 덮어쓰지 말 것. E1 IDs는 worker-local join key이지 새 canonical 번호가 아니다. source 43 alternate rendition 관계는 W1대로 보존.
2. **Leader:** 네 소비 파일의 evidence/endpoint-scope correction을 버전 및 CHANGELOG에 통합. 독립 설치 때 inline citations가 그대로 전달되는지 확인. synopsis refs에서 S1/S4 같은 내부 rendition 약칭은 같은 설치 파일에 정의돼 있어 QA 디렉터리 의존이 없다.
3. **Provider/runtime owner:** 실제 선택이 생기면 P05 및 optional catalog C05의 각 capability를 live 공식 contract로 판정. Gen-4 guide를 타 모델 endpoint·가격·support의 증거로 재사용하지 말 것.

## 부모 통합에서 실행할 정확 명령 / 시나리오

아래는 **부모에게 넘기는 명령이며 E1은 실행하지 않았다**.

```text
python -X utf8 -m pytest recording-production-history/scripts/test_production_history.py
python -X utf8 -m pytest
python -X utf8 scripts/check_versions.py
python -X utf8 qa/skill-completeness-95/run_cases.py --manifest qa/skill-completeness-95/case-manifest.json --run-dir qa/skill-completeness-95/runs/e1-m09 --case M-09
```

- M-09를 frozen read-only + later finished-panels clause로 standalone synopsis만 설치해 fresh session 실행. 기대: requested narrative artifact만, media/tools/writes 없음.
- M01–M05를 같은 소비 참조가 설치된 fresh session에 적용. 특히 documentary narrator 구분, 고객/brand, no-plot/no-CTA, analogy limit, emotion/concerns, data unknown/원인 구분이 실제 산출물에 반영되는지 판정.
- M06 정상: 실제 synthetic still + supplied measured audio로 계획/assembly 승인 범위를 분리. actual crop/display-size/playback와 runtime conflict 처리 확인. 현재 보고의 unseen cue를 실제 이미지 QA PASS로 합산하지 않음.
- M07 정상/경계: 공식 Gen-4 text-only contract로 positive-only motion prompt, 별도 identity-restatement endpoint fixture로 조건부 분기, 미지원 FLF2V/interactive로 blocked submission 확인. 모델/워크플로가 없으면 실제 생성 효과는 미검증 유지.
- 네 소비 파일 relative-link/독립 설치, 전체 정식 61개, 버전, 기존 suite, 독립 rubric review는 부모의 공유 wave 종료 후 수행. 자체 점수 부여 없음.
