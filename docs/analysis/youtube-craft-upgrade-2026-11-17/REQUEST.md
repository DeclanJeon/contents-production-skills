# 지정 YouTube 12편 — 다운로드·자막 MD·스킬 업그레이드 후보 분석

## 사용자 요청
제공한12개영상을Flucto CLI로다운로드하고자막Markdown도저장한뒤, 현재contents-production-skills에서업그레이드할수있는부분을분석하여보고한다.

## 범위
- 개별공개YouTube영상12개만접근. WL/나중에볼동영상재생목록은열지않음.
- MP4는720p선호(실제다운로드해상도는ffprobe로확인),기존설치Flucto1.19.0사용.
- 자막MD는language auto,실제자막기반. 자막미제공/접근실패는보존하며STT/번역/유료서비스로대체하지않음.
- 다운로드24산출요청(MP4 12+MD12),동시최대2CLI,개별MP4최대360초/MD180초,외부재시도0,전체작업최대약25분내상태점검. 이미생긴파일/부분결과를확인하지않고다시받지않음.
- 설치·자동업데이트·로그인·쿠키추출·프록시우회·외부업로드·생성·게시없음. Node filesystem permission으로CLI쓰기대상을이분석폴더로제한하고기존yt-dlp/FFmpeg를명시한다. 자막429의자동binary-refresh가차단되면그실패를기록한다.
- 원본/자막은evidence하위(기존gitignore대상)에저장하고보고서/인벤토리만별도작성. 보호된영상/대사/캐릭터표현을스킬정책으로복제하지않음.
- 기존소스에다른진행중변경이있음. 기존스킬본문/manifest/라우팅/다른분석자료를수정·커밋·배포하지않고현재작업트리기준의개선안만제시한다. Pons재배포없음.
- 프레임표본/자막열람/연속재생/실청취/전체coverage를구분한다. 도구성공·다운로드·decode를시청/청취로표시하지않음.

## 제공 순서 / canonical URL
1. https://www.youtube.com/watch?v=uMi9le1sNpQ
2. https://www.youtube.com/watch?v=ljzVerRYiso
3. https://www.youtube.com/watch?v=ZzDRSxx3zgY
4. https://www.youtube.com/watch?v=OO6J2w_FBnE
5. https://www.youtube.com/watch?v=AROGVvDV4w0
6. https://www.youtube.com/watch?v=ObvCtB1ATnA
7. https://www.youtube.com/watch?v=_X7KQVwsn9U
8. https://www.youtube.com/watch?v=BjZ4viBcpZU
9. https://www.youtube.com/watch?v=74_qWsIW6LI
10. https://www.youtube.com/watch?v=1BzzdY-nK9A
11. https://www.youtube.com/watch?v=cBxKZcalwkM
12. https://www.youtube.com/watch?v=iJiBJAJRRkk

## 작업 체크
- [x]12개MP4/MD획득시도와각각의실제결과·실패기록
- [x]저장파일/hash/ffprobe와선택자막본문검사(전체decode/청취아님)
- [x]각소스의실제검사범위와근거locator기록
- [x]현재오너·참조·템플릿·QA대조:이미커버/부분커버/갭후보/증거부족
- [x]최소업그레이드후보/금지일반화/검증계획/파일경로보고

## 최종 산출과 한계
- MP4 12개, 자동선택 MD 12개 + 제공 언어 지정 추가 MD 6개. 원본 자동선택본 보존.
- REPORT.md, SOURCE_NOTES.md, COVERAGE_RESEARCH.md에 분석/대조 근거.
- 선택 자막 본문 12편과 12장 contact sheet(144표본)를 열람. 연속재생·실제청취·전체디코드·생성재현·수익검증은 미수행.
- 보조 연구는 기존 소유 문서/예시/eval에 대한 읽기 전용 조사이며, 별도의 영상 전체 검수나 최종 승인 아님.
- 최종 저장 파일/해시/로컬 링크 확인은 VALIDATION.json. 원본 스킬·manifest·라우팅·기존 사용자 변경 및 pons 배포는 건드리지 않음.
