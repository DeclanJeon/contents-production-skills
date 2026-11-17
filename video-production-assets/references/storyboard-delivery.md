# 스토리보드 — PDF 파일 납품

텍스트/이미지 PDF 저장·변환을 실제 요청받았을 때 적용한다. [core](storyboard-contract.md)+[direction](storyboard-direction.md)의 필수 설계는 유지한다. 이미지 PDF는 [media](storyboard-media.md)의 정본 PNG/등록/전수 QA를 대체하지 않는다. 텍스트 PDF에 새 이미지를 생성하지 않는다. 명시적 no-save/read-only와 파일 요청이 충돌하면 제약을 임의 해제하지 않는다.

### PDF 공유본 납품

파일 기반 이미지 보드는 사용자 지정 형식이 없으면 **PDF 공유본 + PNG 시트/clean 컷/분할 manifest 원본**으로 납품한다. 채팅-only/프롬프트-only는 기존 no-save 규칙을 유지한다. PDF는 보기·검토용 파생본이며 `storyboard_sheet` PNG 등록·추출·strict gate를 대체하지 않는다.

```bash
python <skill-dir>/scripts/render_storyboard_sheet.py <project.json> --base-dir <project-root> --output storyboards/sheets/board-v01.png --panels-per-sheet 4 --pdf-output final/board-v01.pdf
```

기본 `--pdf-style document` 납품은 **최상위 PDF 하나 + `_internal/`의 편집 원본/최소 검증 자료**다. 이미지 보드는 A4 가로 2패널/페이지가 기본이며 `--pdf-panels-per-page 4`는 짧은 캡션의 개요 보드에서 가독성을 확인한 경우에만 선택한다. `1`은 명시적으로 필요한 상세본이다. 기본 compact와 상세/시험본을 자동으로 병행 생성하지 않는다. 편집 가능한 self-contained HTML은 PDF 옆이 아니라 `_internal/<stem>.html`에 저장한다. 표지의 제목/버전, 페이지 번호, 패널별 clean 그림과 검색·복사 가능한 캡션을 출력한다. 정본 패널 순서로 상세 카드를 배치하며 긴 캡션은 글자를 줄이거나 생략하지 않고 다음 페이지로 흐른다. 그림은 원래 비율로 contain하고 관리 설명은 실제 텍스트로 분리한다. **문서 PDF 페이지 수는 PNG 시트 수와 같지 않다.** 표지·패널 카드·연속 페이지를 기준으로 전체 패널을 대조한다.

문서형에는 설치된 Chrome/Chromium·Poppler `pdfinfo`, Python 3.11+ 환경의 Pillow·markdown-it-py·Pydantic 2와 한글 지원 시스템 폰트가 필요하다. 별도 문서 CLI에는 Typer도 필요하다. 실행 전 확인하며 설치/다운로드는 자동 수행하지 않는다. 필요한 도구가 없으면 차단 사유를 알리고 설치 승인을 받거나 사용자 동의 아래 `--pdf-style sheets`를 선택한다. 이 명시적 구형 옵션은 Pillow만 쓰는 144 dpi 래스터 합본으로 검색 텍스트·A4를 제공하지 않는다. 선택 형식을 납품 시 명시하며 조용히 품질을 낮추지 않는다. PNG metadata는 PDF로 대체되지 않으므로 추출은 PNG에서만 수행한다.

이미 생성된 메타데이터 포함 PNG 시트는 `render_storyboard_document.py --sheet <sheet1.png> --sheet <sheet2.png> --base-dir <project-root> --output final/board-detail-v01.pdf --title <제목> --version <원본버전> --panels-per-page 2`로 재사용한다. index/count·패널 순서·crop bounds를 검증하며 없는 메타데이터를 추측하지 않는다. 원본을 수정하거나 재생성하지 않는다.

**그림 없는 텍스트 콘티**는 아래 경로로 A4 세로 문서형을 만든다. Markdown 제목/문단/목록/코드와 pipe 표를 지원하며 넓은 표는 행별 label/value 카드로 재배치한다. 원본 MD도 함께 납품한다. raw HTML은 실행하지 않고 Markdown 이미지 참조는 텍스트/링크로만 남긴다. 그림 삽입/원격 이미지 다운로드/새 이미지 생성 경로가 아니다. 복잡한 병합 표·수식·확장 Markdown의 완전한 시각 재현은 보장하지 않는다.

```bash
python <skill-dir>/scripts/render_storyboard_document.py <board.md> --base-dir <project-root> --output final/board-text-v01.pdf --title <제목> --version <원본버전>
```

시트 CLI 결과의 `pdf`에는 실제 path/relative_path/sha256/page_count/style, 문서형의 html_path/html_sha256, 순서별 `source_sheet_sha256`가 있다. 독립 문서 CLI는 PDF/HTML 경로·각 hash·페이지 수와 실제 입력 경로/hash를 반환한다. 기존 asset_registry의 문서 에셋(`kind=document`)으로 PDF·HTML 경로/hash와 원본 hash를 기록하고, 현재 보드 버전에 의존하는 기존 보드 artifact의 파일 목록에 포함한다. 새 필수 스키마나 승인 원장을 만들지 않는다. 검증용 페이지 렌더는 임시 위치에서 확인한 뒤 필요 이상 남기지 않고, 내부에는 최종 대조 결과와 필요 시 개관 한 장만 보존한다. 기존 원본·유효 버전·감사 기록은 보존하며 실패본/중복 파일 삭제는 사용자 승인 범위로 한정한다. PNG와 PDF 생성·검수·이동/정리는 실제 수행 상태대로 제작 이력에 남긴다. 목적지 중복·루트 밖 PDF 경로는 PNG 생성 전에 거절하며, 이후 PDF 쓰기 실패 시 이미 만든 PNG는 남을 수 있다. 이때 부분 산출물과 오류를 보고하고 새 PDF 버전으로 재시도한다.

PDF 완료 확인은 **실제 파일 열기/페이지 렌더 → 패널/본문 커버리지·순서 대조 → 텍스트 추출 대조 → 페이지 시각 검토**다. 한글 글리프, 캡션/다음 페이지 연결, 머리말·꼬리말과 본문 겹침, 그림의 전체 경계와 얼굴·손·정보의 읽힘을 확인한다. 문서형은 `pdftotext`로 원문 캡션/대사와 추출 내용을 대조하고, `pdfinfo`로 전 페이지 A4·페이지 수를 확인한다. 구조·전체 개관과 개별 확대 검사 범위를 구분해 보고하며 미열람 페이지를 시각 검사 완료로 표시하지 않는다. 글자가 작으면 문서의 흐름/배치를 수정하고 래스터 시트는 밀도를 낮춘다. PDF 접근성 태그가 생성되더라도 읽기 순서·접근성 적합성 전체를 인증하지 않는다. 파일 헤더나 페이지 수 검사만으로 시각 QA 통과라 하지 않는다. PNG 보드 검사와 PDF 변환 검사는 구분하고, 최종 응답에서 PDF 경로를 먼저, 편집/추출 원본 경로를 뒤에 보고한다.
