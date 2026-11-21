# Prompt Motion: 모션 그래픽 통합 후보 인벤토리

출처: [Customize](https://prompt-motion.com/customize), [Templates](https://prompt-motion.com/templates), [갤러리](https://prompt-motion.com/), [About](https://prompt-motion.com/about), 각 행의 원본 저장소. 공개 HTML/DOM에 열거된 범위. About의 소개 수치 240과 실제 홈에서 발견한 `Prompt` 234 + `Skill` 5 = 239는 구분한다. Customize 첫 목록의 프롬프트 24개는 전체 갤러리와 별개인 추천 목록이다. 숨겨졌거나 이후 추가된 항목까지 확인했다는 뜻은 아니다.

## 설치형 Skill — 홈에서 발견한 5개 전부

| 사이트 항목 | 고정한 원본 | 저장소 표시 라이선스 | 반영 제안 |
|---|---|---|---|
| [Cinetic skill launch film](https://prompt-motion.com/lexnlin-f9b3bd8) | [`cinetic`](https://github.com/Leonxlnx/cinetic/blob/f4bbfc844877891fe92279d47b7874fb44d485ae/skills/cinetic/SKILL.md) | MIT | **우선**. 코드 기반 영상의 씬 구성, 박자·전환, 제품 UI 진위, 렌더 및 재생 확인을 모션·편집 참조에 각색. 광범위한 자동 호출 규칙/독립 총괄은 가져오지 않는다. 자체 skill LICENSE도 별도 검토. |
| [HTML app demo skill](https://prompt-motion.com/mengto-a7f4679) | [`html-demo`](https://github.com/MengTo/Skills/blob/3ec2dc0857d36e45d032d10063f62f2c773329a3/agent-skills/web-design/html-demo/SKILL.md) | MIT | **우선**. 단일 시간축 기반 UI 상태 재현, 포인터, 고정 스테이지, reduced motion과 구간 검수. 라이브 데모와 영상 렌더를 구분. |
| [TasteSkill dashboard showcase](https://prompt-motion.com/lexnlin-6161a6) | [`design-taste-frontend`](https://github.com/Leonxlnx/taste-skill/blob/f6b76575f949707b4e3c37cd86cb44b0b98643e8/skills/taste-skill/SKILL.md) | MIT | **부분 적용**. 실제 UI를 담는 컷에만 시각 계층·간격·타이포 기준을 참고. 사이트 전체 제작·라우팅은 제외. |
| [Reddit marketing tool launch video](https://prompt-motion.com/anthonyriera-9b1b2a) | [`product-film`](https://github.com/Rieranthony/product-film-skill/blob/fe11efc429d5903e37274d0b294e1b95745b2881/plugins/product-film/skills/product-film/SKILL.md) | MIT | **우선**. 실제 제품 컴포넌트와 디자인 토큰, 기능→사용 장면, 음악·전환·최종 렌더 검증을 상품 프로모·편집 심화에 연결. |
| [Animated agent session story](https://prompt-motion.com/jake11moran-a269c4) | [`session-story`](https://github.com/heygen-com/hyperframes-community-skills/blob/ba7a0bb6d3567d124c51f6074625043bfe0b32eb/skills/session-story/SKILL.md) | Apache-2.0 | **선택 적용**. 작업 로그를 문제→시도→변화의 장면으로 요약하는 설계만. 런타임·별도 라이선스가 있는 엔진·로컬 세션 읽기 및 부작용은 이식 범위에서 제외. |

저장소 라이선스 표시는 모든 하위 코드·폰트·영상·음원·템플릿의 재배포 허가가 아니다. 실제 복사 전 파일별 라이선스, NOTICE/귀속, 번들 의존성을 다시 대조한다. 설치 명령과 원본 코드는 실행하지 않았다.

## 공식 Customize 템플릿 — 2개

- [3D template](https://prompt-motion.com/templates/realtime/customize): 주제, 스타일, 대표 샷, 샷 순서, 해상도와 창의성/속도/완성도 범위. **대표 구도 중심의 Three.js 실시간 장면 설계**에 적합. 영상 계획과 실시간 웹 실행은 분리한다.
- [Showreel prompt](https://prompt-motion.com/templates/showreel/customize): 콘셉트, 서체, 팔레트, 길이, BPM, 해상도와 창의성/속도/완성도 범위. **하나의 주제로 씬 변주, 박자-컷 매핑, 프레임 단위 렌더 QA**를 활용. 원문의 BPM·길이·FPS·모션 블러는 보편 기본값이 아니다.
- Explainer, Product film, Short film은 Templates 페이지의 예고다. 공개 공식 템플릿으로 세지 않았다. 위 `product-film`은 별도의 창작자 스킬이다.

## Customize 추천 프롬프트 — 표시된 24개 전부

아래 분류는 카드 제목·태그를 바탕으로 한 통합 후보 분류이지 영상 전체 시청이나 프롬프트 재현 시험이 아니다. 링크 기준 URL은 `https://prompt-motion.com/customize/`다.

| 기법 후보 | 항목 제목과 링크 끝부분 |
|---|---|
| 쇼릴·키네틱 타이포·범퍼 | Claude motion designer showreel (`stephanlivera-df17a2`), Bold kinetic type showreel (`shneural-2abdfa`), Motion designer showreel (`himanshutwtxs-5f4b43`), TechHalla kinetic type bumper (`techhalla-90b8ec`), TypingMind logo reveal (`tdinh-me-815acb`) |
| 형태·추상·3D / 스크롤 | Shape morphing through UI states (`twoclipping-5cba86`), Abstract motion design reel (`ajith-io-b5626e`), Landing page 3D scroll (`twoclipping-d89be5`), Engraving-style Claude ad (`lexnlin-038035`) |
| 제품·서비스 홍보 | Photo print app launch film (`twoclipping-221cab`), Enxovaly baby app promo (`gabrielbuzziv-4ff0c6`), Travel visa service promo (`thismacapital-dfba20`), Distilbook product video (`ajith-io-c52e09`), UGC ad generator promo (`twoclipping-6dd14e`), ViralGrow product promo (`samuel-yostt-891f87`), Dub promo video (`steventey-0d20e4`), Shin Majin-shiki promo (`majin-appsheet-2d3c1a`), AjustaCV Pro pricing promo (`thayto-dev-44b911`), Lightspark social promo video (`davidmarcus-a28a60`) |
| 설명·절차·정보 구조 | Negroni recipe animation (`ror-fly-9950f1`), Recursion explained in genres (`emollick-8661a8`), Animated business explainer (`alex-prompter-1ea044`) |
| 비교·후반 편집 | Launch video remake comparison (`notdwd-c2037d`), Talking-head clip edit (`sab8a-364a5a`) |

페이지의 발견 태그: Product UI, Phone, Charts, Diagrams, Kinetic type, Shapes, Particles, Characters, Photos, Music, Code. 중복 태그이며 독립 스킬이 아니다. 사이트는 영상·프롬프트의 창작자 소유를 명시한다. 사용을 위한 복사 허용을 패키지 재배포 허용으로 해석하지 않는다.

## 상세 페이지 후속 대조

추천 24개 상세 페이지에서 공개 프롬프트 섹션(`Improved prompt` 또는 `Prompt`)을 확인했다. 제목과 프롬프트의 계열은 항상 같지 않다. 특히 Abstract reel, Enxovaly, Himanshu showreel, Bold Kinetic, Claude showreel, AjustaCV, Travel visa 등 7개는 상세 페이지에서 같은 범용 쇼릴 골격을 제시한다. 이를 독립 기법 일곱 개나 일곱 편의 재현 증거로 세지 않는다.

- UI morph는 단일 시각 객체와 사용자 동작에 따른 전이, 제품 영상은 검증된 실제 화면과 장면을 잇는 한 객체, 사진 론칭은 프레임/마스크가 다음 구도로 연결되는 원리를 제공한다.
- 로고 공개는 조각→인식 시점, 범퍼는 루프 경계, 레시피는 재료가 들어갈 때만 수치 공개, 재귀 설명은 스타일 전환 자체가 개념의 일부가 되는 원리를 제공한다.
- Talking-head는 발화 컷과 정보 그래픽의 타이밍, 랜딩 3D는 일관된 카메라 이동과 읽을 수 있는 대표 구도를 보여주는 프롬프트다. 고정 초수·FPS·브랜드·문구는 공용 기본값으로 옮기지 않는다.
- `diagram_data`와 `character_photo`의 넓은 선택 조건은 사이트 태그 및 기존 제작 사전에서 보강한 제안이다. 24개 안에 모든 계열의 완전한 원본 구현이나 차트 데이터가 있다는 뜻은 아니다.

결과를 [위임 브리프 선택표](../../creative-production/references/motion-selection.md)에 반영했다.

### 전체 공개 갤러리 후속 수집

[갤러리 인덱스 TSV](prompt-motion-gallery.tsv)의 **234개 URL 모두**에서 비어 있지 않은 Prompt 본문을 확보했다. 본문에서 사이트 UI와 출처 안내를 빼고 소문자·공백으로 정규화한 SHA-256 기준 **203개 고유 그룹**, 최대 반복 그룹 **22개**다. 이 값은 문자 정규화 기준이며 의미가 같은 모든 레시피를 합친 수가 아니다. TSV에는 ID·URL·제목·공개 태그·해시·첫 등장 ID만 저장하고 본문은 재배포하지 않는다.

누락 링크가 없도록 전체 목록을 기계 대조한 뒤 차트/절차, 파티클/보상, 형태/사진 마스크, 로고/루프의 상세 사례를 선별 대조해 [모션 제작 참조](../../video-production-assets/references/08b-code-motion-production.md)에 구현 순서와 탈락 조건을 추가했다. 모든 사례의 의미 단위 전문 리뷰·영상 재생·재현 검증을 했다는 뜻은 아니다.

## 기존 오너에 연결할 순서

1. `video-production-assets`의 모션·편집·상품 프로모 및 [모션 스타일 사전](../../video-production-assets/references/33-motion-style-library.md)과 대조: 새로 보강할 항목은 상태 전이, BPM/컷 매핑, 코드 렌더 검수, 제품 UI 출처 검증. 기존 타이포·로고·데이터 가족 전체를 중복 작성하지 않는다.
2. `open-3d-production`은 실시간 3D와 스크롤 장면만 받는다. `html-demo`의 라이브 화면과 편집용 클립에는 다른 완료 조건을 둔다.
3. CineForge/creative-production이 기존 승인과 기록을 유지한다. 선택된 소스의 참조만 보강하고, 원본 skill 설치나 새 자동 트리거 추가는 뒤로 미룬다. 카탈로그/출처 조사만 수행했으며 스킬 구현·설치·렌더는 아직 하지 않았다.
