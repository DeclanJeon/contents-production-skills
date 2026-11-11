# 추가 YouTube Blender 조사

조사일: 2026-11-03. Flucto 1.19.0으로 YouTube native 검색 4회, 질의당 6개, 중복 제거 후 24개 후보를 확보했다. 네 검색 모두 `ok`이며 web-index fallback은 없었다. 검색 순서는 추천 순위·품질·인기도 평가가 아니다. 원본 JSON: `/home/declan/Documents/studio_production/blender-methods-2026-11-03/youtube-candidates.json`. 게시일·조회 지표는 이 연구의 채택 기준으로 쓰지 않았다.

## 후보 목록

검색 메타데이터만 확인한 항목은 영상을 시청한 근거가 아니다. 아래 세 항목만 추가 자막을 내려받아 읽었고, 추가 영상의 프레임·오디오 검사는 하지 않았다.

| ID | 제목 / 제작자 | URL | 검사 범위 |
|---|---|---|---|
| YT01 | Product Reveal Animation Blender using Lights / madebyomkar | https://www.youtube.com/watch?v=_nl4kcb05sQ | 검색 메타데이터만 |
| YT02 | How to get Perfect Lighting for Product Animation in Blender / Aryan | https://www.youtube.com/watch?v=f5Jb_mO4e40 | 검색 메타데이터만 |
| YT03 | Simple Cinematic Product Lighting Tutorial in Blender and Cycles / Kyrik | https://www.youtube.com/watch?v=FRXOXkCywcE | 검색 메타데이터만 |
| YT04 | Professional Product Lighting in Blender 4.0 [Product Animation Masterclass: Part 3] / The Blenderender | https://www.youtube.com/watch?v=-WXnwW6Bnvw | 검색 메타데이터만 |
| YT05 | The Only Product Lighting Video You'll Ever Need (Blender Tutorial) / The Blenderender | https://www.youtube.com/watch?v=yPekIQMoKYM | 자막 Markdown 읽음; 화면 미검사 |
| YT06 | Light Animation Tutorial / Blender 2.93 / Product Animation Full Tutorial / Creative Sav | https://www.youtube.com/watch?v=lYQ1ETiBV4A | 검색 메타데이터만 |
| YT07 | Really cool geometry nodes for making flowers #blender #blender3d #3dart / Pantheon | https://www.youtube.com/watch?v=cKbk6lX1G1E | 검색 메타데이터만 |
| YT08 | Power of nodes: A blender tutorial #blender #blender3d #motiongraphics / Viscous Realm | https://www.youtube.com/watch?v=wT8k9XCzC8I | 검색 메타데이터만 |
| YT09 | Geometry Nodes for Beginners (Blender Tutorial) / Ryan King Art | https://www.youtube.com/watch?v=188IeRY-ch0 | 검색 메타데이터만 |
| YT10 | How to Understand Geometry Nodes / Blender for Beginners / Yesway™ | https://www.youtube.com/watch?v=ETOXG3qdMKg | 검색 메타데이터만 |
| YT11 | Blender Tutorial: Geometry Nodes for Beginners - Part 1 / Blender Guru | https://www.youtube.com/watch?v=aO0eUnu0hO0 | 자막 Markdown 읽음; 화면 미검사 |
| YT12 | Easy Motion Graphics Setup with Geometry Nodes / Bouncing Rays / Bouncing Rays | https://www.youtube.com/watch?v=evxRGwtqYrM | 검색 메타데이터만 |
| YT13 | Blender Motion Tracking Introduction / Add 3D elements to your Footage / Tutorial / Twan_Olig | https://www.youtube.com/watch?v=vB07Bws8bmY | 검색 메타데이터만 |
| YT14 | 3D Tracking in Blender: Step-by-Step CGI Tutorial for Beginners / ProductionCrate | https://www.youtube.com/watch?v=J2JbXoK3dKQ | 검색 메타데이터만 |
| YT15 | Learn Blender Object Tracking in 8 Minutes! / Kenan Proffitt | https://www.youtube.com/watch?v=LMU3yMQlZTw | 검색 메타데이터만 |
| YT16 | Blender Camera Tracking Beginner Tutorial / Add 3D Objects to Real Footage / Grid Effect Studios | https://www.youtube.com/watch?v=5bu2u6LwqrY | 검색 메타데이터만 |
| YT17 | A Beginner's Guide to Camera Tracking in Blender 4.0 / Jacob Zirkle | https://www.youtube.com/watch?v=ui0JUHE12k8 | 자막 Markdown 읽음; 화면 미검사 |
| YT18 | Camera Tracking in Blender for Beginners / Motion Tracking Tutorial / 3Dnot2D | https://www.youtube.com/watch?v=IvyfdxkABKU | 검색 메타데이터만 |
| YT19 | 2D Blender Grease Pencil Basics: Start Animating In 10 Minutes / Micah Buzan ANIMATION | https://www.youtube.com/watch?v=ZkqZRe9IXQ8 | 검색 메타데이터만 |
| YT20 | How I Made This 2D Animation in Blender Grease Pencil / Juhas | https://www.youtube.com/watch?v=tc64RVqgzJk | 검색 메타데이터만 |
| YT21 | How To ANIMATE FASTER in Blender 4.5 Grease Pencil / SHIN LOGIC | https://www.youtube.com/watch?v=4K3ROb4NTzQ | 검색 메타데이터만 |
| YT22 | EVERYTHING You Need to Animate with Blender Grease Pencil (Beginner Guide) / kdsketch | https://www.youtube.com/watch?v=cprYwZ9sFSo | 검색 메타데이터만 |
| YT23 | My Secret Workflow for Fast 2D Animation in Blender / Savonne Draws | https://www.youtube.com/watch?v=PgBYbNMcxvk | 검색 메타데이터만 |
| YT24 | The Easiest Way to Animate in Blender (Grease Pencil Introduction) / Martin Klekner | https://www.youtube.com/watch?v=-Io7esCKSdg | 검색 메타데이터만 |

## 자막으로 심화한 방법

- **YT05 / The Blenderender:** key/fill/rim을 따로 조정하고 제품 윤곽·반사·배경을 분리한다. light linking과 차광판, 반복 사용 가능한 조명 rig로 변형을 비교하는 원리를 채택했다. 유료 procedural-lighting 상품은 설치하지 않았다. “항상 작동”, “유일/최신”, 조명 거리와 부드러움에 대한 단정은 일반 규칙으로 옮기지 않았다. 광원 크기·거리·노출의 실제 결과를 비교한다.
- **YT11 / Blender Guru:** `Distribute Points on Faces → Instance on Points → Join Geometry`와 Object Info, Random Value로 반복 배치·변형을 제어한다. 회전 vector와 균일 scale float의 목적을 구분한다. 원본의 사탕/설탕 모델과 수치를 재사용하지 않고 제품 파츠·환경 반복 배치에 일반화한다. scale 적용은 원본 자산/리그 계약에 따라 판단하며 무조건 적용하지 않는다.
- **YT17 / Jacob Zirkle:** 공간에 분산된 고정 특징점, track 정리, parallax가 있는 solve 구간, floor/origin/scale 설정 후 테스트 물체의 sliding을 확인한다. 원문 자동 선택이 **아랍어 자막**이므로 번역/전사 오류 가능성을 남긴다. 튜토리얼의 solve-error 수치·추정 실측·Standard 색 관리·노드 삭제·왜곡 토글은 그대로 처방하지 않는다. 현재 버전과 실제 원본/왜곡/합성 조건을 먼저 확인한다.

자막 파일 3개는 연구 프로젝트 `tutorials/`에 보관했다. 각 문서의 frontmatter에 제목·제작자·URL·다운로드 시각·길이가 있다. Flucto 자동 Markdown의 장 구분이 거칠어 자막 문장을 정밀 시각 근거로 쓰지 않았다. 전체 자막을 저장소에 복제하지 않는다.

실행 가능한 재사용 절차는 [native Blender workflows](../../open-3d-production/references/native-blender-workflows.md)에, 공식/제작자 웹 근거는 [출처 조사](2026-11-03-blender-production-sources.md)에 연결한다.
