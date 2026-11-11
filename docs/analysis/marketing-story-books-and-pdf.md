# 로컬 마케팅·스토리 자료 보완과 스토리보드 PDF

이 문서는 1차 보완 시점의 기록이다. 이후 기본 PDF를 검색 가능한 A4 문서형으로 확장하고 실제 콘티로 검증했다. 현재 구현·검증·최종 샘플은 [후속 기록](storyboard-document-pdf-validation.md)을 참조한다.

## 범위와 실제 읽기

사용자 지정 `/home/declan/Book/마케팅`, `/home/declan/Book/스토리`의 Markdown 24개를 목록/지문으로 조사했다. 마케팅의 `(1)` 중복 4쌍은 SHA-256이 각각 같아 고유 자료는 20개다. 제목·목차·도입부/키워드 탐색으로 범위를 선별하고, 기존 스킬의 포지셔닝·시놉·캐릭터·대사·콘티·편집 지침과 대조했다. **20권 전권 정독이나 전 도판 검수는 하지 않았다.**

직접 근거로 채택한 6권의 정확한 rendition·읽은 줄·SHA-256·한계와 실무 반영은 [30-marketing-story-craft.md](../../video-production-assets/references/30-marketing-story-craft.md)에 있다. 원문 전문·긴 발췌·도판은 프로젝트에 복사하지 않았다.

- Contagious: 공유 이유와 이야기 안의 핵심 메시지/제품 효익 연결. 현재 조회/전환 보장이나 과거 사례 수치 채택 없음.
- Obviously Awesome: 기존 포지셔닝을 실제 대안→차별 속성→가치→적합 고객→범주/장면으로 연결.
- The Mom Test: 구체적 고객 행동과 칭찬·가정적 구매 의향 분리. 고객 답변·수요를 발명하지 않음.
- Creating Character Arcs: 성장형만 강제하지 않고 긍정/flat/부정 아크와 선택 증거 연결.
- Dialogue: 대사를 목적·전술·상대 반응으로 설계. 직접 설명이나 내레이션의 일괄 삭제 금지.
- In the Blink of an Eye: 컷/유지의 감정·이야기·리듬·시선·축·공간 판단. 저자의 비율을 객관 가중치로 채택하지 않음.

그 외 자료는 이번 패치의 새 근거로 승격하지 않았다. Profit First·E-Myth·Retail Product Management는 재무/사업 운영/상품 관리까지 제작 스킬 범위를 넓히지 않도록 제외했다. Day Trading Attention의 플랫폼·사례는 현재 알고리즘/성과 근거로 쓰지 않았으며, 1-Page Marketing Plan의 사업 전체 프로세스를 모든 영상의 의무 funnel로 만들지 않았다. Egri·Storr·Field·Vogler·Kleon·Mascelli·Thomas/Johnston·Rabiger·Katz는 기존 이야기·원천 보존·구도·연속성·보드 가독성 계약을 대체할 근거로 추가하지 않았다. 이는 해당 책 전체에 새 내용이 없다는 판정이 아니라 이번 제한된 탐색에서의 보류다.

## 기존 상태와 변경

기존 정식 이미지 보드 출력은 `render_storyboard_sheet.py`의 PNG 시트 세트와 `split_storyboard.py`의 패널/씬 이미지·manifest였다. PDF 출력 옵션은 없었다.

변경 후 파일 기반 이미지 스토리보드는 사용자 지정 형식이 없으면 PDF를 먼저 안내하고 PNG 시트·clean 컷·manifest를 함께 납품한다. chat-only/prompt-only는 no-save 유지다. PDF는 원래 시트 비율의 144 dpi 래스터 검토본이며 검색 가능한 문서·고정 A4·접근성 태그를 보장하지 않는다. PNG metadata와 기존 strict gate는 변경하지 않았다. 그림 없는 계획 문서는 가용한 문서 렌더러를 사용하며 PNG 변환을 위해 새 이미지를 생성하지 않는다.

`--pdf-output`은 명시적 옵션으로 기존 CLI 호출을 호환 유지한다. 스킬/사용 가이드의 기본 납품 절차에서 이 옵션을 지정한다. PDF 입력 순서는 현재 실행이 만든 PNG 시트 순서이며, sheet index/count를 대조한다. 출력 JSON에는 PDF hash·페이지 수·순서별 PNG hash가 있다. 기존 파일·루트 밖 목적지 거절, 임시 파일 후 no-overwrite 게시를 적용한다. PNG 생성 후 PDF 단계가 실패하면 PNG는 남을 수 있어 부분 완료로 보고한다.

## 실제 검증

- `python3 -m pytest -q video-production-assets/scripts scripts/test_check_versions.py scripts/test_install_package.py`: **203 passed, 200 subtests passed**.
- 한글 캡션을 추가한 PDF 테스트 재실행: **8 passed**.
- 실제 renderer CLI로 5패널/2시트/2페이지 PDF를 생성하고 Poppler `pdfinfo`, `pdftoppm`으로 재렌더했다. 전체 두 페이지를 열어 순서·캡션 경계를 보았고, 첫 페이지를 1600px로 다시 열어 `안녕, 스토리보드 PDF 한글 확인`의 글리프를 확인했다. 합성 단색 테스트 패널이므로 실제 작품의 이미지 품질·창작 QA를 입증하지 않는다.
- 생성/재렌더 샘플: `/tmp/contents-storyboard-pdf-qa/test_real_renderer_cli_and_pdf0/board.pdf`, `pdf-page-1.png`, `pdf-page-2.png`; 한글 확대 `/tmp/contents-storyboard-pdf-qa/korean-page.png`. 임시 파일은 영구 납품/출처 저장소가 아니다.
- 패키지 version checker: **package 2.33, 22 skills consistent**. `git diff --check` 통과.
- 범용 skill-creator `quick_validate.py`는 기존 `version` frontmatter를 허용하지 않아 실패했다. 이 프로젝트의 기존 버전 계약을 삭제해 통과시키지 않았다. 별도 독립 에이전트 행동평가·실제 콘텐츠 제작·유료 생성·게시·설치는 수행하지 않았다.

원본 프로젝트에는 이미 다른 수정/미추적 파일이 있었고 보존했다. 변경은 Unreleased에 추가했으며 커밋·릴리스 버전 변경은 하지 않았다. 관련 설치 스킬은 이 원본 디렉터리의 심볼릭 링크라 별도 동기화가 필요하지 않았다.
