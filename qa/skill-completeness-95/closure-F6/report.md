# F6 근거 폐쇄 인계

판정 범위: `review-source-2.md:172–220`의 Brandkit craft/source 및 Generate prompting/readiness 결함. 아래 결함 ID는 이 인계를 위한 별칭이다. 최종 점수·95%·정식 행동 PASS를 선언하지 않는다.

| 결함 ID | 원 검토 위치 | 조치 / 남은 상태 |
|---|---|---|
| F6-D1 | Brandkit :179–194 — taxonomy / central mechanism | Keller 원문과 Adobe 공식 guidance에 직접 결속. 마크 계열은 모두 유지했다. 출처가 입증하지 않는 업종별 `only for` 배타 조건은 선택적 비교 가설로 수정했다. 세 후보·symbol-only 단계는 기존 로컬 출력 계약으로 구별한다. 독립 모델 replay 미실행. |
| F6-D2 | Brandkit :180–187 — anatomy / pairing | Adobe의 complementary style, icon/text visual weight, headline/body hierarchy를 실제 유지 규칙에 연결했다. 문자 형태의 literal matching을 보편 필수조건으로 취급하지 않는다. 대비 자체가 실패라는 해석을 제거하고 실제 의도하지 않은 경쟁/가독성 문제를 기준으로 삼는다. |
| F6-D3 | Brandkit :181–194 — one expressive move / optical balance | Adobe “Own one thing”의 제한된 craft adaptation으로 명시했다. 기본 단일 dominant mechanism은 유지하고, 명시적 사용자 multi-device 방향은 유지한다. optical QA는 실제 시각적 dominance/spacing 문제와 구체 수정으로 기록한다. 수치 중앙정렬이나 미측정 인지도 우월성을 증거로 쓰지 않는다. |
| F6-D4 | Brandkit :191–194 — deterministic exercise 부재 | 합성 state → 실제 HTML preview → Chrome 렌더/PNG 열람 성공. 실제 logo-export와 canonical brandbook-build는 둘 다 exit1, `rsvg-convert is unavailable in the local environment`. 완성 SVG/PNG export·PPTX·PDF 증거는 미충족이다. |
| F6-D5 | Generate :206–218 — universal static-redescription / most-models negative_prompt | 정적 anchor 포함/생략을 선택적 draft 비교로 바꾸고, 필드 존재는 모델/transport의 inspected schema로만 판단하도록 수정했다. No-people 같은 사용자 exclusion은 review constraint로 유지한다. 비용·승인·reconciliation gate는 변경하지 않았다. |
| F6-D6 | Generate :216–218 — bounded preparation/error handoff | 실제 read-only model schema와 CLI recovery help를 확인하고 bounded preparation/unknown-outcome 인계를 작성했다. 인계는 수동 작성 계약 exercise이며 fresh-model invocation이나 실제 job reconciliation 증거가 아니다. 독립 replay용 정상/경계 prompt 6개를 제출한다. |

## 변경 파일과 정확한 구간

기존 파일 수정은 아래 네 파일뿐이다. 스크립트 구현, SKILL metadata/package2.10, shared sources/ledger/runner/parser/manifest/README/CHANGELOG 및 다른 owner 파일을 수정하지 않았다.

- `higgsfield-brandkit/references/brandkit-design-brain.md:10–15`: source pointer / 근거 범위. `:130–143`: 다섯 마크 경로를 선택적 비교 가설로 표현. `:172–174`: 실제 anatomy의 similar/complementary 관계. `:194`: hierarchy critique. `:236–249`: one-expressive-mechanism 기본 계약과 명시적 사용자 예외.
- `higgsfield-brandkit/references/typography.md:5–11`: pairing source와 Norman 범위 분리. `:45`: 실제 rendered competition/legibility 기준; 대비 자체는 실패가 아님.
- `higgsfield-brandkit/references/qa-and-iteration.md:5–7`: craft/source pointer. `:79–81`: 실제 visual-weight/spacing optical review 기준.
- `higgsfield-generate/references/prompt-engineering.md:25–33`: static-anchor/motion draft 비교, schema 의존. `:37–47`: negative_prompt의 endpoint 의존, optional positive wording, 사용자 exclusion 보존과 execution gate.
- 새 owner reference `higgsfield-brandkit/references/design-sources.md:1–21`: 직접 읽은 원문/공식 guidance identity, locator, read-state, 실제 지원 범위와 불채택 주장.
- 새 QA 파일은 모두 `qa/skill-completeness-95/closure-F6/` 아래. 핵심 인계: `claims.tsv`, `smoke-prompts.json`, 이 보고서. 재현/관찰 파일: `local_smoke.py`, `commands.json`, `source-identities.json`, `artifact-identities.json`, `visual-inspection.json`, `preparation-handoff.json`, `essential-preview.png`, `source-symbol.png`, `synthetic-brand/` payload/state/HTML.

## 직접 읽기와 bounded entailment

먼저 `video-production-assets/references/sources.md`를 읽고 디자인/브랜드 기존 항목을 검색했다. 기존 Brandkit 항목은 Norman의 legibility에 한정됐다. `E:/Book/06_Book/디자인` 및 corpus의 Design/Type/Brand/Logo/한국어 대응 filename을 탐색했다. 사용 가능한 디자인 폴더는 Norman이었고, marketing 원문 중 Keller의 정확한 rendition을 추가로 읽었다. 원문 부족을 이유로 사용자에게 이미 존재하는 자료를 재요청하지 않았다.

| 직접 읽은 자료 | identity / 범위 | 지원 / 한계 |
|---|---|---|
| Keller / Swaminathan, Strategic Brand Management | `E:/Book/06_Book/originals/마케팅/md/Strategic Brand Management (Kevin Lane Keller, Vanitha Swaminathan) (z-library.sk, 1lib.sk, z-lib.sk).md`; 2583958 bytes; SHA256 `ab37f2b8d583706796380f04944513a87831f099886eaee93faf83c9b93a46c6`; READ-PARTIAL L309–315 (printed pp154–157), L333–337 (pp166–168) | word/pictorial/abstract/character 구분, 추상 마크 의미전달 위험, 상호 지원하는 일관된 identity. 업종별 유일한 정답이나 최적 후보 수는 입증하지 않는다. 도판은 열람하지 않았다. |
| Norman | `E:/Book/06_Book/디자인/md/디자인 오브 에브리데이 싱스 - 도널드 노먼.md`; 762430 bytes; SHA256 `265118cafd52ef01321ccbf1df282cef924a6e8e168df6153f7258243939cc2a`; READ-PARTIAL L10399–10419 | 크기·대비와 조절 가능한 presentation. taxonomy/pairing 근거로 확장하지 않는다. 이 읽기에서 printed page는 확정하지 않았다. |
| Adobe [logo fonts](https://www.adobe.com/express/learn/blog/best-logos-for-brand.md) | 35656 bytes; SHA256 `a918969d73a9849ca9378b934a630ac954bafe6fc68abbc637c66d0a27c1f6b5`; READ-PARTIAL “Tips for choosing logo fonts”, “Text-only logo fonts”, “Text and icon logo fonts”, “Monogram logo fonts” | complementary style, icon/type visual weight, quieter secondary type, hierarchy, readable small use. 폰트의 보편적 심리 효과나 실제 인지도/전환은 채택하지 않는다. |
| Adobe [font pairings](https://www.adobe.com/express/learn/blog/10-ways-to-pair-fonts-for-maximum-impact.md) | 49418 bytes; SHA256 `589b02214c56565e65b431b294d757ae8f0094769ead220b5f4c3ada975dd8d4`; READ-PARTIAL sections 1 Event flyers, 2 Social media ads, 5 Resumes | expressive heading / readable quieter body와 weight contrast. 특정 조합의 실증적 우월성은 입증하지 않는다. |
| Adobe [logo design](https://www.adobe.com/express/learn/blog/how-to-design-a-logo.md) | 50201 bytes; SHA256 `cd4d25aac10c0514d510ece19e3f8edabb7b1be18c1bee4bed8e99830bd3ab89`; READ-PARTIAL logo types/core components, steps 1/3/5/7/8, best practices / Own one thing | lettermark/emblem 정의, proportion/negative-space/context check, 한 distinctive element craft guidance. “Abstract mark” 항목이 combination 정의를 중복하는 실제 오류를 발견하여 그 정의는 불채택하고 Keller를 사용했다. article의 통계와 blanket best-type 권고도 불채택. |

공식 문서는 검색 snippet이 아니라 원 페이지의 `.md` rendition 본문을 직접 읽었다. 해당 `.md` URL 바이트를 별도로 읽어 hash/bytes만 기록했다. 공개 페이지는 가변이다. 원문 책 문장을 QA에 복제하지 않았다. Google Fonts pairing URL은 metadata shell만 반환하여 본문 근거에서 제외했다. 출처가 증명하지 않는 배타적 mark routing이나 “모든 폰트는 마크를 닮아야 한다”는 보편 법칙을 authored라는 이름으로 재라벨링하지 않았다. 동일 기능을 유지하면서 근거 범위에 맞춰 비교/검수로 표현했다.

## F6-LOCAL-01 — 실제 로컬 실행

도움말을 먼저 실행했다:

```text
python higgsfield-brandkit/scripts/brandkit.py --help
python higgsfield-brandkit/scripts/brandkit.py preview --help
python higgsfield-brandkit/scripts/brandkit.py state --help
python higgsfield-brandkit/scripts/brandkit.py logo-export --help
python higgsfield-brandkit/scripts/build_brandbook.py --help
python higgsfield-brandkit/scripts/render_brandbook_pdf.py --help
```

모두 exit0. payload reference와 세 스크립트의 실제 관련 구현/선행조건도 읽었다. 후속 실행:

```text
python -X utf8 qa/skill-completeness-95/closure-F6/local_smoke.py
```

harness exit0은 모든 export 성공을 의미하지 않는다. `commands.json`에 subprocess별 정확한 argv/stdout/stderr/exit가 있다:

| 순서 | 실제 경로 | exit / 관찰 |
|---|---|---|
| 0 | isolated state get_status | 0; version0, 모든 slot false |
| 1 | logo-inspect synthetic local SVG | 0; source color `#101820`; fingerprint `a19ce3f57b7056050426f97d858d31c1e7521b54953e13687b18a43a3813d97f` |
| 2–4 | lock_authoritative_palette/logo/typography | 각 0; 합성 fixture만 state version1→2→3, 세 slot revision1. 실제 사용자 승인으로 표현하지 않았다. |
| 5 | get_essential_kit | 0; 세 slot true, complete true |
| 6 | preview | 0; `synthetic-brand/reviews/brandkit-review-1-synthetic-corner.html` 생성 |
| 7 | logo-export | 1; `rsvg-convert is unavailable in the local environment` |
| 8 | brandbook-build | 1; 같은 missing-prerequisite 오류. 동일 오류 재시도나 대체 builder 없음. |
| 9 | preview with empty reviews | 1; `input requires one to three reviews`; 실패를 PASS로 집계하지 않음 |

상태/출력 경로는 전부 closure-F6 아래이며 사용자 brandkit state를 읽거나 수정하지 않았다. fixture symbol은 직접 만든 117-byte SVG이고 provider 출력이 아니다. installed Georgia Bold / Arial Regular 경로를 사용했고 폰트 파일을 재배포하지 않았다.

Playwright Python과 설치된 Chrome으로 실제 HTML과 원 SVG를 열었다. `document.fonts.ready` 후 screenshot을 만들고 두 PNG를 이미지 도구로 직접 열어 보았다:

- [essential-preview.png](essential-preview.png): 1440×1100. Paper/Ink/Signal의 세 swatch, 오른쪽 angular L symbol, Georgia headline과 Arial body가 보인다. 텍스트 겹침/가로 잘림은 이 viewport에서 관찰되지 않았다. 본문은 제목보다 작고 조용하며 symbol에는 별도 장식 장치가 없다. 이는 실제 hierarchy가 보이는 fixture이지 한 expressive move의 보편적 우월성 실험이 아니다.
- [source-symbol.png](source-symbol.png): 1440×1100. 어두운 직각 L 경로를 직접 확인했다. export 결과가 아니라 원 SVG의 browser rendering이다.
- `visual-inspection.json`: Georgia weight700, Arial weight400 모두 `loaded`; document width1440 = viewport1440. body text도 실제 DOM에서 기록했다.
- 실제 PNG pixel count: Paper `(247,247,245)` 1530820 pixels; Ink `(16,24,32)` 26036; Signal `(0,174,239)` 11098. Pillow 측정은 `getdata` deprecation warning을 냈지만 값 출력은 완료됐다. 색 pixel 수는 가독성/심미성의 합격 증명이 아니다.
- 실제 export에서 형상 fingerprint 보존, 작은 인쇄 lockup의 optical balance, PPTX/PDF matching은 실행되지 못했다. 원본 fingerprint를 export 보존 증거로 오용하지 않는다.

현재 도구 탐색: `rsvg-convert`, `magick`, `soffice`, `pdffonts`, `fc-cache`, `fc-match`는 PATH에서 발견되지 않았다. PATH의 `convert`는 `C:/Windows/system32/convert.EXE`여서 ImageMagick이라고 간주하지 않았다. `where.exe soffice`도 not-found. 설치 app roots/Local Programs, 예상 portable 위치, Calibre/Git/Tesseract 후보를 추가 탐색했다. Calibre의 `pdftoppm.exe`와 Tesseract의 `libfontconfig-1.dll`은 발견됐지만 canonical contract에 필요한 실행 파일 세트를 대신하지 못한다. 사용자 홈 전체 glob은 timeout으로 partial 결과였으므로 완전 부재 증거로 사용하지 않았다. 설치·PATH/전역 config 변경·대체 렌더링 backend는 수행하지 않았다.

## F6-PREP-01 — 실제 read-only schema / 수동 인계

실제 실행:

```text
higgsfield model get cinematic_studio_video --json
higgsfield generate --help
higgsfield generate get --help
higgsfield generate list --help
higgsfield generate cost --help
```

모두 exit0. 모델 응답은 `type=video`, `duration` 5/10, aspect ratio에 16:9, `sound` boolean, `start_image` object|null, `end_image requires start_image` rule을 반환했다. `negative_prompt`는 이 응답에 없었다. 이 단일 관찰을 most-models 주장으로 일반화하지 않는다. `preparation-handoff.json`에 관찰 JSON을 구조적으로 옮겨 적었다; raw CLI byte log라는 주장은 하지 않는다.

`get/list` 도움말에서 실제 recovery 표면 `generate get <id> --json`, `generate list --video --size 50 --json`을 확인했다. 실제 job 조회는 하지 않았다. `cost --help`는 비생성 견적이라도 local paths를 auto-upload한다고 명시했다. 따라서 preparation에서 cost에 파일을 넘기지 않았다. quote/cost/approval은 미해결 상태로 남겼다.

추가 직접 읽기: 공식 `https://raw.githubusercontent.com/higgsfield-ai/cli/main/MODELS.md`의 introduction/media transport와 `cinematic_studio_video` 표; mounted `xd://mcp__higgsfield_generate_video` timeout/confirmed-ID/get_cost 계약과 `xd://mcp__higgsfield_job_status`의 nonterminal `poll_after_seconds` 계약. discovery/aggregate cost/bounded approval/unknown reconciliation 규칙은 변경하지 않았다.

`preparation-handoff.json`은 다음을 명시하는 **수동 작성 exercise**이다: 한 5초 silent shot, budget0, approved_jobs0, retries0, optional motion/static-anchor drafts, 사용자 no-people constraint, quote null, actual source/외부전송 권한 미확정. unknown-timeout 경계는 원 요청 context/receipt→ID 회복→해당 transport status/history 조회→미확정이면 unknown 유지→확정 결과와 retry/cost 권한 후에만 재시도 순서다. 실제 이전 submit이나 paid success를 만들지 않았다. Parent의 fresh-model replay 결과를 대체하지 않는다.

## 반환물 검사와 남은 인계

- `claims.tsv`: 새 ID F6-01…F6-12, 12행, 각 16열. 기존 combined ledger에서 `^F6-` 검색 결과 없음. combined ledger는 수정하지 않았다.
- `smoke-prompts.json`: synthetic user facts/request만 포함한 6개 supplemental scenario. expected answer/source passages는 prompt에 주입하지 않았고, required_reads/checks는 별도 필드다. original-book opening은 required_reads에 없다. frozen61 변경 없음.
- JSON/TSV 구조 측정 command의 실제 출력: `claim_rows 12 column_counts [16]`; 6 prompt ID가 parse됨; `handoff_kind manually_authored_contract_exercise_not_fresh_model_invocation`; subprocess exits `[0,0,0,0,0,0,0,1,1,1]`.
- tests/build/lint/formatter/공유 전체 suite는 실행하지 않았다. 허용된 local media/CLI smoke만 실행했다. git commit/push/reset, 설치/auth/config 변경, paid generation, upload, training, remote create/deploy/publish 없음.

남은 prerequisite / 조치:

1. **U2 / F6-D4:** canonical export/Brandbook 성공 증거에는 실제 `rsvg-convert`, ImageMagick, LibreOffice, Poppler `pdffonts`, Fontconfig `fc-cache`/`fc-match` 실행 가능한 환경이 필요하다. 현재 정확한 두 실행 오류와 추가 탐색은 위와 같다. 최소 입력은 기존 허가된 toolchain 경로 또는 사용자가 별도로 승인·준비한 toolchain 환경이다. 이 세션은 설치 권한을 요청받지 않았으므로 설치하지 않았다. 준비 후 같은 isolated payload로 실제 export/build→전체 페이지 열람→폰트/형상/시각 대조를 수행해야 한다. 그 전까지 이 두 결과는 미검증/차단이며 점수 상향 근거가 아니다.
2. **Parent replay:** 최종 root freeze 후 6 supplemental prompts를 독립 fresh model에 replay하고 checkout required_reads/actual final/tool errors를 source-confirmed trace로 심사한다. F6-D1/2/3/5의 새 문구가 실제 정상/경계 응답에 적용됐다는 증거는 아직 없다. error는 PASS가 아니다.
3. **Parent 통합:** 승인 시 shared source index의 역사적 E3 “Norman only” 표기와 새 owner-local `design-sources.md` 근거 연결, root changelog 반영은 shared-file owner가 처리한다. F6는 해당 파일을 쓰지 않았다.
4. 원문에서 확인하지 못한 독점적 type-to-industry 법칙이나 모든 multi-device 방향의 열등성은 주장하지 않는다. 새 규칙은 taxonomy 기능을 제거하지 않고 evidence 범위 안의 제안/검수로 유지한다. 실제 인지도·차별성·권리 clearance·paid provider success는 이 증거로 입증되지 않는다.
