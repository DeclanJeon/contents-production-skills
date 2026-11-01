# 헤어·메이크업·의상 선택과 정체성 보존

새 외형 선택이나 요청된 스타일 변형에만 읽는다. 정본은 [SSOT §4–9·24–26](character-ssot-master-prompt.md), 일반 시트는 [character craft](character-craft.md)다. 전체 SSOT를 간단한 스타일 질의에 강제하지 않는다. 사용자 제공/관찰/디자인 제안/미정을 보존한다. 실제 이미지를 보지 않고 그 이미지의 헤어·메이크업을 관찰했다고 하지 않는다.

자료 진입점은 [제작 참조 색인](../../video-production-assets/references/production-reference-index.md)이며 개별 사진의 재사용·업로드 권리는 별도다. 다음은 자체 작성한 묘사 축이지 사이트 이미지 전수 분석·유행 순위·얼굴형별 효능의 검증이 아니다.

| 분야 | 독립적으로 선택할 축·어휘 예 | 기존 SSOT 위치 | 보존/실패 검사 |
|---|---|---|---|
| 헤어 구조 | 길이: ear/chin/shoulder-length; 가르마: center/side; 앞머리: blunt/curtain/swept; 층: blunt/layered | §6 Hair Identity Lock | 가르마 좌우는 인물/화면 기준 구분. 한 뷰로 뒷라인 확정 금지 |
| 헤어 질감·부피 | straight/wavy/curly/coiled; crown/side volume; density; flyaways; tied/loose | §6·§21 실루엣, §24 상태 | 길이·헤어라인·얼굴형을 함께 바꾸지 않음. 외형을 성격/인종/MBTI에서 도출하지 않음 |
| 헤어 색 | 기본색·하이라이트·뿌리·빛 반사색 | §6·§8 Color Identity | 조명 반사색을 염색으로 재정의하지 않음 |
| 메이크업 피부 | 적용 부위·coverage; matte/satin/dewy finish; 색조·광택 강도 | §24 메이크업 상태, 피부 고정점은 §5 유지 | 마감 변화가 피부색·얼굴 비율·나이·점/흉터를 지우는지 확인 |
| 눈·눈썹·입술 | liner의 범위·방향, shadow 위치, brow grooming, lip 색·edge·matte/gloss | §24 상태; §5 얼굴 구조 보존 | 화장과 눈 크기·간격·입술 구조 변경 구분. 좌우 비대칭 앵커 보존 |
| 의상 형태 | fitted/relaxed/oversized; neckline·sleeve·length; 레이어·여밈 방향 | §9 Costume DNA, WARDROBE ID | 앞뒤 여밈·단추·소매/허리 높이·신발 연속성; 미관측 후면은 제안 |
| 의상 재질·상태 | 소재 관찰값·표면/두께/드레이프; clean/wet/worn/damaged | §9·§24, 장면 derivative | 사진만으로 실제 섬유 성분 확정 금지. 상태 변화는 부모 버전과 델타로 관리 |

## 선택·생성 입력

1. 잠긴 인물을 재캐스팅하지 않는다. 요청한 변화 축과 유지할 앵커를 먼저 분리한다.
2. 비교가 필요하면 선택 이유를 설명할 수 있는 대안만 만든다. 정해진 후보 수·유행·미감 점수를 강제하지 않는다.
3. 채택한 헤어/의상/메이크업 상태를 같은 SSOT 안에 기록한다. 별도 persona/appearance 정본이나 새 project field를 만들지 않는다. 허용된 scene state는 master 버전을 가리키는 derivative다.
4. 실제 생성 입력은 [29 R1/R2](../../video-production-assets/references/29-reference-driven-production.md#sheet-inputs)로 뷰의 사용/제외 속성·한계를 명시한다. 헤어 사진의 얼굴·의상·배경은 신원 참조로 자동 수입하지 않는다.
5. 11의 `참조`, `조명·룩`, `유지 규칙`, `참조 역할표`에 실제 상태/버전과 제출 문장을 연결한다. 예: `the approved center-parted, shoulder-length wavy hairstyle; preserve the established hairline and facial landmarks`는 텍스트 의도이며 특정 서비스의 identity-lock 파라미터가 아니다.
6. 실제 결과의 정면/필요 방향·의상 경계·원본 크기·납품 크기를 비교한다. 인물이 회전/가려지는 장면은 실제 연속 재생으로 재등장 시 앵커를 확인한다. 미관측 뷰/시간은 미검증이며 뷰티 이미지 한 장으로 전체 정체성 통과를 주장하지 않는다.
