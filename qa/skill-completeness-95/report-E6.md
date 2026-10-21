# E6 — core module source binding

상태: **review 요청, 독립 승인/점수 없음**. 소유한 7개 모듈을 처음부터 끝까지 직접 읽고 원문을 대조했다. 수정 7개 reference + 신규 `claims-E6.tsv`/이 보고서. shared sources/SKILL/12QA/manifest/README/CHANGELOG/통합 상태·원장·scorecard는 수정하지 않았다. commit/reset/revert, delegation, tests/build/lint/format, provider/media/훈련/배포/게시/과금은 실행하지 않았다.

## 변경 파일·결함·전체 coverage

| 파일 | 직접 읽은 coverage | 수정 / 보존 / 남은 한계 |
|---|---|---|
| `video-production-assets/references/10-evidence.md` | 입력·산출물; 실행 절차 1–6; 광고 시각 은유·문구·근거 분리; 완료 조건; 근거; 템플릿 | 범주 비교/시간 변화와 막대·선의 축 규칙을 ONS에 결속. 모든 축 절단을 같은 왜곡으로 취급하지 않게 구별. CDC 비교집단/관찰·실험/단면 연구의 인과 한계를 결속. claim ID·관찰/창작·권리·CTA 경계 유지. 자료30은 W4의 읽기 기록이며 E6가 직접 읽었다고 승격하지 않음. 관할 광고 입증/불확실성 표기 전체는 미검증. |
| `video-production-assets/references/13-ideation-brand.md` | 실행 절차 1–8; 입력·산출물; 근거·한계; 템플릿; 심화 링크 | Young L39–45의 후반 숙성·통찰·현실 수정/비평을 직접 결속. 에이전트 무의식·대기·성과 약속 없음. 44의 필요/행동/지역/사용 상황/추구 편익 원문을 결속. 후보 수·선택·승인 규칙 유지. 38–40은 기존 W4 범위 유지, E6 직접 읽기로 주장하지 않음. |
| `video-production-assets/references/15-delivery.md` | 실행 절차 1–7; 입력·산출물; 자막 파일/타이밍; 근거; 템플릿; 배급의 에셋/목적지/권리/제출/반응; 심화 링크 | WCAG 공식 해설의 실제 criterion·예외·레벨을 결속. 색만의 구별 금지와 텍스트 금지를 혼동할 표현 교정. 대사 번역 자막≠captions, 시각 설명≠captions, A 텍스트 대체≠AA 음성 설명 구별. final-audio timing·재생/청취·권리/목적지 미확인 게이트 유지. 목적지 규격은 미선택이므로 unverified 유지. |
| `video-production-assets/references/16-concept-emotion-retention.md` | 콘셉트 엔진 12종·신기함; copy→행동; 기대 위반/목격 반응; 감정/기억 8절차·7패턴; 평가/정직성; 시청 유지·지도·실제 분석 진단; 근거·라우팅 | 24/41/42를 E6도 직접 읽고 정확 rendition/hash/bytes/line을 소비 파일에 기록. 하락의 '흔한 원인' 단정을 후보 가설로 좁힘. **S1a 정확 분리 문장과 S1b per-claim locator/class/BASIS 정책은 수정하지 않았다.** 혼합 감정 기억 우위·특정 훅 초/유지율 효과·장치 자체 발명 주장 없음. 상세 모티프/열린 고리 craft는 여전히 미결속. |
| `video-production-assets/references/17-genre-comedy.md` | 장르 설계 1–8·9 장르 패턴; comedy 1–9·10 기제·사다리; 근거·관련 모듈 | McKee 장르 관습/기대/변주·혼합, 셋업/펀치·기대/결과 간극을 직접 결속. 독립 개그 허용이라는 원문 한계 명시. 삼단/콜백 효과·반응 배수·공포 일반식·정확 패턴 배열은 BASIS-UNSTATED 유지. 기능 삭제나 authored 발명 재분류 없음. |
| `video-production-assets/references/18-episodic-series.md` | 시리즈 엔진 1–9; 월 제작량/cadence 1–6; 규칙 6개; 산출물·링크·근거 | Nash 엔진/세계 구별 및 episodic/serialized/혼합 원문 결속. 모든 회차 독립성 강제를 형식별로 교정, 모든 연작 갈등 강제도 제거하고 반복 문제/관계/탐구 원천으로 설명. 단일 원장·델타·stale·월 용량 미확인 경계 유지. callback 효과·정확 비트 템플릿은 미결속. |
| `video-production-assets/references/19-brand-product-integration.md` | 스폰서 1–9·점검·규칙; 제품 visual 1–8; 분리부품/소유/사용전 상태; 형태/환경 은유·스펙터클; 산출물·근거 | Miller 고객 목표 관점과 Alton 반사 소품 설명, broncolor 투명/불투명 병과 금속 카드 사례 결속. 금속 외관=환경이라는 절대식 교정. 제품 제거 결과를 자동 실패/효과로 취급하지 않는 기존 양방향 진단 유지. artwork/claim/접촉/캡·소유 인계·위험 환상 경계 유지. 모든 sponsor 모드·유체/피부·긴 하이라이트 효과의 근거로 확대하지 않음. |

기존 Acceptance를 복제하지 않았다. 본문 삭제로 근거 없는 기능을 감추지 않았다. 소비 reference의 근거 절은 source-derived의 지원 범위와 미결속 항목을 구분한다.

## 직접 읽은 원문 — 정확 주소는 claims-E6.tsv와 소비 파일

모든 책은 READ-PARTIAL. 디스크 바이트·SHA-256은 PowerShell `Get-Item`/`Get-FileHash -Algorithm SHA256`를 실제 실행해 관찰했다. 원문을 QA 산출물에 복제하지 않았다.

| ID | 직접 읽은 원문 범위 / 실제 지원 |
|---|---|
| E6-READ-37 | Young originals/마케팅/md rendition L39–45 **전체 raw**. Mental Digestive Process→Final Stage, 인간의 숙성/통찰/실용 수정과 비평. 초기 표시의 잘린 L33–49를 전체 읽기로 집계하지 않음. |
| E6-READ-44 | Kotler/Armstrong 마케팅/epub rendition L16820–16895, L17124–17168. Market Segmentation·변수 조합·사용 상황·Benefits Sought. 표 7.1은 추출 텍스트만; 원 도판 검사 없음. |
| E6-READ-20a/b | McKee **콘텐츠_제작/md** rendition L177–189 전체 raw(pp88–94), L483 전체 raw(p241), L705–711 전체 raw(pp352–355). 장르·셋업/펀치·Comic Design. **시놉시스 rendition으로 대체하지 않음.** 부가 L719–725, L737–741도 읽었으나 adaptation/character 구간으로 comedy 입증에 쓰지 않음. 본문 인쇄 페이지와 말미 index의 페이지 숫자가 일치하지 않아 직접 구간의 인쇄 표식을 사용. |
| E6-READ-Nash1/2 | Nash originals/시놉시스 rendition L610–640, L868–902 전체. story engine·세계, episodic/serialized 구분. 이 구간 인쇄 페이지는 미표시. |
| E6-READ-41 | Hogan 감정구조/md L2404–2406 전체 raw. prototypical agent/goal/causal sequence. |
| E6-READ-42 | Lazarus 감정구조/md L2342–2352 전체 raw(p134 표식 전후). primary 목표 관련성/일치, secondary 책임/대처/미래 기대. |
| E6-READ-24 | Habermas originals/콘텐츠_제작/md L351–359 전체 raw(pp160–164). 서술 정서/관점·맥락과 음성/텍스트 불일치 연구 한계. |
| E6-READ-Miller | StoryBrand 2.0 광고_상세페이지/md L1160–1199, A Character. 고객을 주인공·브랜드를 돕는 역할로 보는 저자 권고만. 보편 구매 효과는 미채택. |
| E6-READ-Alton | Painting With Light originals/콘텐츠_제작/md L113–115 전체 raw(pp18–19 Props). 반사 소품과 specular highlights만. |

### 직접 읽은 공식 웹 — 2026-10-17

책 출처나 provider 계약으로 혼동하지 않는다. 웹은 reader HTML rendition을 읽었고 고정 로컬 snapshot/SHA-256/bytes는 **N/A-live-web**이다. 따라서 정확 고정 웹 rendition 지문 요건까지 완료했다고 주장하지 않는다. 도판·링크 예제의 실제 화면은 미검사.

- E6-WEB-ONS: [bar charts](https://service-manual.ons.gov.uk/data-visualisation/chart-types/bar-charts) 도입/When to use/Axis; [axes](https://service-manual.ons.gov.uk/data-visualisation/guidance/axes-and-gridlines) Axis start point/Consistent axis scales; [principles](https://service-manual.ons.gov.uk/data-visualisation/guidance/principles) When to use/Showing the important comparison/What data to include/Using derived variables. 차트 구성 권고만, overview의 기억/뇌 효과는 미채택.
- E6-WEB-CDC: [Lesson1 Section7](https://archive.cdc.gov/www_cdc_gov/csels/dsepd/ss1978/lesson1/section7.html) Analytic Epidemiology·Experimental/Observational studies·마지막 요약. 연관/인과와 비교 집단의 보건 연구 설명, 광고 법규가 아님.
- E6-WEB-WCAG: W3C Understanding [1.2.2](https://www.w3.org/WAI/WCAG22/Understanding/captions-prerecorded.html), [1.2.3](https://www.w3.org/WAI/WCAG22/Understanding/audio-description-or-media-alternative-prerecorded.html), [1.4.1](https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html), [1.4.3](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html) SC/Intent 및 소비 파일에 명시한 정의·예외. 규범 페이지 최초 요청은 W3C API가 abstract/metadata만 반환했으므로 criterion 읽기로 집계하지 않고 실제 해설 페이지의 criterion을 직접 읽었다. 전체 Understanding 문서/전체 WCAG를 READ-FULL로 표시하지 않음.
- E6-WEB-bron: Urs Recher [reflection elements](https://broncolor.swiss/news/how-to-shoot-with-reflection-elements) 불투명/투명 도입과 diffusion panel 문단; [work tool](https://broncolor.swiss/news/how-to-show-the-aesthetic-side-of-a-work-tool) 금속 팁 흰 카드와 검정 창 문단. 실제 제작자의 사례 텍스트만. 이미지·노출 설정의 재현·유지 성과는 미검증.

## 실제 로컬 비테스트 smoke

E6-SMOKE-01 — 다음 **비테스트 산술 명령**을 실행, exit 0. 소스 텍스트 assertion/테스트 runner 아님. 합성 데이터로 축 절단의 길이 비율과 제안 시간 합만 관찰했다. 문서 소비 모델·차트 렌더·오디오·접근성·관객 행동의 통과 증거가 아니다.

```powershell
powershell -NoProfile -Command '$a=92; $b=100; $zeroRatio=$a/$b; $croppedRatio=($a-90)/($b-90); "synthetic category values=92,100; zero-baseline length ratio=$zeroRatio; baseline-90 length ratio=$croppedRatio"; "same observations; no treatment assignment or comparison design supplied; causal effect not computed"; $beats=6,10,13,13,12,6; "proposed emotion beat total_seconds=$(($beats | Measure-Object -Sum).Sum); measured media duration=unavailable"'
```

관찰 원문:

```text
synthetic category values=92,100; zero-baseline length ratio=0.92; baseline-90 length ratio=0.2
same observations; no treatment assignment or comparison design supplied; causal effect not computed
proposed emotion beat total_seconds=60; measured media duration=unavailable
```

지문 명령 2회도 exit 0, 총 9개 실제 책 경로/bytes/hash를 반환했다. 첫 묶음 Young40774/Kotler3360340/McKee856699/Nash422398/Alton560865, 둘째 Hogan805530/Lazarus1803443/Habermas952320/Miller414893. 명령 형식:

```powershell
powershell -NoProfile -Command '$paths = @("<claims-E6.tsv의 실제 rendition_path>"); Get-Item -LiteralPath $paths | ForEach-Object { "{0} | {1} | {2}" -f $_.FullName,$_.Length,(Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash.ToLower() }'
```

## 수동 소비 적용 — fresh model 실행 아님

- **E6-MANUAL-10:** 합성 범주값92/100은 막대의 0 기준선 길이비0.92. 90부터 그리면0.2가 되어 범주 차이를 과장하므로 0 baseline/dot plot 대안. 동일 값이 시간계열이면 비영점 선 축은 맥락/눈금과 함께 검토 가능. 함께 증가했다는 관측만으로 영상 때문이라고 하지 않음. Locator: 10 §차트·인과성의 직접 근거 → ONS-axis/CDC-analytic → source-derived. 실제 chart rendering 없음.
- **E6-MANUAL-13:** 자료가 관객 연령만 주면 편익/사용 상황은 미확인. 두 후보를 서로 다른 편익 가설로 제안할 수 있으나 실제 segment 크기를 만들지 않음. Young의 마지막 단계에 따라 제작 제약·비평으로 수정할 점을 기록하며 '무의식을 돌렸다'고 하지 않음. Locator: 13 §발상·세분화 직접 근거 →37/44→source-derived, 후보 구성/수량은 authored proposal.
- **E6-MANUAL-15:** 가상 웹 동기화 영상에서 문을 두드리는 소리가 사건 단서이면 `[문 두드리는 소리]`를 captions 범위에 넣고, 음성에 없는 중요한 화면 글자는 별도 시각 설명/미디어 대체를 검토. 최종 음성 없으면 시각=provisional·sync=unverified. A 텍스트 대체만으로 AA 주장하지 않음. Locator: 15 §접근성의 직접 근거→1.2.2/1.2.3→source-derived. 실제 파일/청취/contrast measurement 없음.
- **E6-MANUAL-16:** 빵집 레시피 보존의 0–6/6–16/16–29/29–42/42–54/54–60은 창작 제안60초. 인물이 목표와 대처 선택지를 가지는 점만 §2→41/42 source-derived, 감정 순서·노트 앵커·시간은 proposal. 혼합 감정 기억 우위/유지율 개선은 unsupported. 원문을 묻는 S1a에는 기존 정확 분리 문장을 사용하며, S1b에는 각 행의 파일/절·class·근거 범위를 붙여야 한다. 실제 응답 준수·감정/시청률 측정 없음.
- **E6-MANUAL-17:** 정상 규칙→기대→다른 결과라는 comedy beat는 17 §근거→McKee L711로 설명 가능. '세 번이면 웃는다'나 '잊었을 때 회수하면 기억이 좋아진다'는 삼단/콜백 효과는 BASIS-UNSTATED. 특정 장르별 화살표를 원문의 정식 beat sheet라고 하지 않음.
- **E6-MANUAL-18:** 주1회 새 사건을 푸는 에피소딕과 이전 편 결정을 이어받는 직렬 연속극을 나눔. 후자에 전회 지식이 필요하다는 이유로 무조건 실패하지 않으며 필요한 선행 사건을 기재. 월 가용시간 없으면 cadence 미결정. Locator:18 §2 규칙/근거→Nash L868–902 source-derived; 월 용량 원장은 authored 운영. 실제 series 패키지·모델 실행 없음.
- **E6-MANUAL-19:** sponsor 제품이 사건 해결에 필수라 제거 시 장면이 붕괴해도 자동 과의존 실패하지 않음. 반대로 제품을 빼도 같은 환경 노출이면 brief와 비교. 투명 병의 투과광과 금속 팁의 카드 반사는 근거 있는 설계 후보, 로고/효능 증명은 별도. Locator:19 §1 step9 authored 진단 질문, §제품 서사·재질 조명→Miller/Alton/bron 사례 source-derived. 실제 라벨·조명·접촉 frame 미검사.

## genuinely unresolved / 주장별 한계

- **W4-U10:** 차트·인과 경계는 새 원문으로 부분 해소. 관할 광고 사전 입증 규칙은 미해소. FTC policy HTML과 PDF 각각403, eCFR255.1은 Request Access로 연결됨. 검색 요약은 원문 읽기 증거로 사용하지 않음. 법규 준수/efficacy 허가 선언 없음.
- **W4-U13:** Young 후반·44 세분화 gap은 직접 구간으로 결속. 책 이론을 실제 수요/성과·에이전트 심리로 확대하는 것은 여전히 금지.
- **W4-U15:** WCAG 해설로 caption/시각 대체/색·대비 범위 결속. 실제 목적지 미선택, final audio/media 미제공이므로 출력 규격·동기·가독성·법적 인증은 미검증. 전체 WCAG 적합성을 검토한 것이 아님.
- **W4-U16:** 혼합 감정 기억 우위·특정 훅 초·유지율 개선 효과 근거 없음. 구조 기능은 유지하되 non-guarantee·BASIS와 인과 가설 정책 보존. 개별 콘셉트 엔진/모티프/open-loop 장치 전수 원문 결속 아님.
- **W4-U17:** 장르 기대/변주와 기대-결과 간극은 결속, 정확 장르 배열·공포 일반식·삼단/콜백/반응 배수 효과는 미결속. McKee와 Nash에서 관련 구간/검색을 읽었지만 그 읽기를 특정 삼단/콜백 근거로 확장하지 않음. 이는 source unavailable 진단이 아니라 추가 원문 탐색/대조 잔여.
- **W4-U18:** 반복 엔진과 형식별 독립성은 결속. callback 효과/정확 회차 배열은 미결속. 일상·탐구 연작에 강제 갈등 규칙은 쓰지 않도록 교정.
- **W4-U19:** 고객 관점/반사·투과 사례는 결속. 정확 통합 모드/진입 순서·제품 제거와 효과 관계·긴 하이라이트 우위·크림/액체 물성·피부 지각 효과는 미결속. 광학 사례를 제품 효능·동일 모델 결과 보장으로 쓰지 않음.
- 웹 근거에 고정 snapshot 지문 없음. 책은 정확 지문을 소비 파일/ledger에 기록했지만 웹을 동일한 frozen bytes 증거라고 주장하지 않음.
- 61개 행동 평가·S1a/S1b·M-03·actual delivery/visual/audio QA·전체 링크/패키지 검증·독립 채점 모두 미실행. 5점/95%/PASS 주장 없음.

## 교차 소유 요청 — 직접 편집하지 않음

**W4 / canonical sources.md:** claims-E6의 E6-S01–S11·W01–W10을 실제 path/hash/bytes/line/read scope 그대로 추가하고 지원 경계13/15/17/18/19의 과거 '직접 구간 없음'을 이번 읽기만큼 갱신 요청. 기존 W4 역사 기록을 E6 READ-FULL로 덮지 말 것. 신규 source ID는 여기서 쓴 `E6-Nash`, `E6-Miller`, ONS/CDC/WCAG/bron alias를 기존 canonical 번호와 충돌 없이 매핑할 것. 16의 원 분리 문장은 보존하고 새 원문 결속 범위를 넘기지 말 것. 필요하면 공식 웹 고정 rendition 확보를 별도 증거 작업으로 남길 것.

**리더:** 7개 참조의 docs/changelog/version 통합, class schema/상대 링크 확인, 새 규칙 normal/boundary replay와 독립 채점 요청. shared 파일은 수정하지 않음.

## 통합 후 정확 smoke/test 명령 — 아래는 실행하지 않음

부모가 wave 종료 뒤 실행. existing fixture의 실파일/승인 상태를 사용해야 하며 계획 상태를 납품 성공으로 바꾸지 않는다.

```text
python -X utf8 scripts/check_versions.py
python -X utf8 -m pytest -q video-production-assets/scripts
python -X utf8 -m pytest -q
python -X utf8 qa/skill-completeness-95/run_cases.py --manifest qa/skill-completeness-95/case-manifest.json --run-dir qa/skill-completeness-95/runs/e6-s1a --case S1a
python -X utf8 qa/skill-completeness-95/run_cases.py --manifest qa/skill-completeness-95/case-manifest.json --run-dir qa/skill-completeness-95/runs/e6-s1b --case S1b
python -X utf8 qa/skill-completeness-95/run_cases.py --manifest qa/skill-completeness-95/case-manifest.json --run-dir qa/skill-completeness-95/runs/e6-m03 --case M-03
```

출력 디렉터리는 부모가 사용 이력/manifest/tree profile을 확인해 새 run으로 선택한다. 위 이름이 이미 있으면 같은 attempt를 덮지 않는다. 추가 수동 smoke 입력은 위 E6-MANUAL-10/13/15/16/17/18/19를 fresh 세션에서 주고, 원문 읽기/제안/unsupported를 구별하는지 관찰한다. 특히 episodic/serialized·비영점 line/bar·A/AA·제품 제거 양방향을 boundary로 확인한다. 이는 전수61개나 실제 미디어 품질 검증의 대체가 아니다.
