# 문서형 스토리보드 PDF 구현·실제 사례 검증

## 사용자 요청에 따른 최종 단순화

아래는 최초 구현의 역사 기록이다. 이후 사용자가 파일/페이지 과다를 지적하고 정리를 승인했다. 현재 기본값은 이미지 보드 2패널/A4 가로 페이지, 최종 PDF 하나이며 편집 원본/최소 검증/기록은 `_internal/`에 모은다. 4패널은 간결한 개요본에 선택하고 1패널 상세본은 필요할 때만 만든다. 기존 제작 프로젝트는 수정하지 않았다.

최종 샘플: `/home/declan/Documents/studio_production/storyboard-document-pdf-qa/스토리보드.pdf` — 표지 포함 **19페이지(본문 2패널씩)**. 원래 36패널·캡션 689조각을 보존했고 텍스트 추출 누락/페이지 경계 위반은 0이다. 전 19페이지 개관과 3페이지 확대 검토를 수행했다. 이전 37페이지본·텍스트/스트레스 시험 PDF·중복 HTML·페이지별 렌더는 사용자 승인으로 정리하며, 아래 과거 산출물 경로를 현재 납품 링크로 사용하지 않는다.

## 변경 범위

기존 PNG 시트/분할 계약과 1차 래스터 합본을 유지하면서, `render_storyboard_sheet.py --pdf-output`의 기본을 `--pdf-style document`로 확장했다. 구형 래스터는 명시적 `--pdf-style sheets`로 계속 사용할 수 있다. 채팅-only에 파일 저장을 추가하지 않는다.

- A4 세로, 제목/버전 표지, 페이지 번호, 패널별 clean 그림과 실제 텍스트 캡션.
- 긴 캡션의 연속 페이지 처리. 패널 순서와 내용을 보존하며 PNG 시트 수와 PDF 페이지 수를 구별한다.
- self-contained HTML도 함께 저장해 문서 편집·재출력 경로를 제공한다. 원본 PNG/MD와 기존 asset/artifact/승인 규칙은 그대로다.
- `render_storyboard_document.py board.md ...`로 그림 없는 계획 문서를 출력한다. 넓은 pipe 표는 행별 label/value 카드로 풀며 raw HTML 실행·이미지 다운로드·새 이미지 생성은 하지 않는다.
- `render_storyboard_document.py --sheet ...`는 기존 PNG metadata의 패널 순서·캡션·정확한 crop bounds를 사용한다. 메타데이터 없는 과거 합본의 구조를 추측하지 않는다.
- 입력/출력 해시, 독립 브라우저 프로필, 출력 루트 제한, PDF/HTML 충돌 거절, 새 파일 no-overwrite 게시. `--base-dir`, `--output`은 필수다.

## 실행 환경과 권한

실제 검증 환경: Linux, Python 3.14.4, Google Chrome 157.0.8103.38, Poppler `pdfinfo/pdftotext/pdftoppm`, Noto Sans CJK KR, Pillow 12.1.1, markdown-it-py 3.0.0, Pydantic 2, Typer. 모두 이미 설치된 도구를 사용했다. 패키지 설치·새 브라우저 다운로드·유료 생성·외부 게시·원본 프로젝트 변경은 하지 않았다.

문서 CLI의 선언 런타임은 Python 3.11+다. 문서형의 Chrome/Chromium·Poppler와 Python 의존성은 실행 환경에서 사전 확인한다. 한글 가독성에는 한글 지원 시스템 폰트가 필요하다. 다른 OS/브라우저 버전·폰트 환경의 같은 결과나 접근성 적합성을 보장하지 않는다. Chrome이 tagged PDF를 출력했지만 스크린리더 읽기 순서·PDF/UA 인증은 수행하지 않았다.

## 실제 입력과 최종 샘플

작업 루트: `/home/declan/Documents/studio_production/storyboard-document-pdf-qa`.
기존 실제 제작 폴더는 읽기 전용 입력으로만 사용했다. 원본에 기록된 미검증 사실·PRELIMINARY/승인 상태를 이번 출력으로 승격하지 않았다. 아래 경로는 작업 루트 기준이다.

| 사례 | 원본/성격 | 최종 PDF | 페이지 | 내용 대조 |
|---|---|---|---:|---:|
| 실제 이미지 콘티 | `hanseoyun-ep02-yeogiseo-naeryeoyo-20261106`의 v001r1 PNG 9시트/36패널 | `04_STORYBOARDS/ep02-image-v03.pdf` | 37 | 원본 캡션 689조각 누락 0, P01–P36 순서 일치 |
| 실제 텍스트 콘티 | `reels01_storyboard/04_STORYBOARDS/storyboard_v001.md`, 5씬/10샷 | `04_STORYBOARDS/reels01-text-v04.pdf` | 6 | 원문 Markdown 텍스트 72조각 누락 0 |
| 긴 한글 대사 | 형식 시험용 합성 MD, 3씬/8열 표/100대사 | `04_STORYBOARDS/long-dialogue-v04.pdf` | 6 | 텍스트 135조각 누락 0 |
| 혼합 비율·긴 캡션 | 형식 시험용 도형 PNG, 세로/가로/정사각·100줄 캡션 | `04_STORYBOARDS/mixed-aspects-v03.pdf` | 6 | 문장/끝표식 102조각 누락 0 |

동일 stem의 `.html`이 편집용 원본이다. 형식 시험용 도형·문장은 실제 콘텐츠 제작 성과로 분류하지 않는다. 실제 원본 전문/그림은 스킬 저장소에 복사하지 않았고 QA 샘플은 작업 루트 안에만 있다.

## 실제로 수행한 QA

- **210 tests passed, 200 subtests passed**: `python3 -m pytest -q video-production-assets/scripts scripts/test_check_versions.py scripts/test_install_package.py`.
- 추가 PDF 두 테스트 모듈 재실행: **15 passed**. 신규 문서 모듈과 PDF helper/테스트 6파일의 no-excuse 정적 검사 위반 0.
- 패키지 버전 검사: **2.33 / 22 skills consistent**. `git diff --check` 통과. 릴리스 버전·커밋은 변경하지 않았다.
- 최종 4문서 **55페이지 전부** PDF→페이지 이미지로 재렌더하고 A4 크기·단어 bbox의 페이지 바깥 이탈을 검사했다. 크기/경계 위반 0.
- 원본과 추출 텍스트 **총 998조각**을 공백 정규화 후 대조했다. 누락 0. 이는 원문의 사실성/창작 품질 판정이나 텍스트 복사 UI를 직접 조작한 검사가 아니라 실제 PDF 텍스트 추출 검사다.
- 최종 모든 페이지의 contact overview 10장을 열어 배치/순서/큰 잘림을 확인했다. 별도로 8페이지를 1000px 단일 페이지로 열어 한글·줄바꿈·긴 캡션의 연속·머리말/꼬리말 분리·세로/가로 그림의 전체 테두리를 확인했다. **전 페이지 모든 작은 글리프의 개별 확대 검수라고 표현하지 않는다.**
- 독립 에이전트 검토·실물 프린터 출력·다른 PDF 뷰어에서의 선택/복사 조작·시각장애인 보조기기 검증은 수행하지 않았다.

## 실제 사례에서 발견하고 고친 문제

1. PNG용 캡션 줄마다 문단 여백이 붙어 36패널이 63페이지가 되었다. 줄 텍스트를 단일 흐름 블록으로 보존하여 그림/캡션 글자를 줄이지 않고 37페이지로 정리했다.
2. 음수 top의 fixed running header가 Chrome 인쇄에서 하단 본문과 겹쳤다. 실제 텍스트 추출 대조에서 한 문장 불일치와 페이지 이미지에서 겹침을 발견했다. 고정 요소를 제거하고 `@page` margin box로 분리했다. 최종 대조 누락 0이며 긴 문장 전체 대조로 테스트를 강화했다.
3. 짧은 표 행이 페이지 사이에서 끊겨 씬 라벨이 앞장에 남았다. 일반 행 카드는 가능한 한 통째로 유지하되, 한 페이지보다 긴 내용은 정상적으로 흐르게 했다. 단일 페이지에 강제 축소하지 않았다.
4. dangling PDF symlink를 따라 새 타깃에 쓰지 않도록 경로 해결 전에 기존 링크 자체를 거절하고 회귀 테스트를 추가했다.

중간 v01/v02와 v03/v04의 이전 조합은 QA 과정 증거로 남겼으며 최종 납품 목록과 구분한다. 실행 이력은 작업 루트 `.history`, 기계 판독 대조 결과는 `09_QA/automated-results-final.json`, 각 문서의 추출 텍스트/bbox/페이지 렌더/overview는 `09_QA/<최종 stem>/`에 있다.
