# 전체 스킬 감사와 최적화 — v2.4

## 결론과 범위

17개 전부의 진입·입력·산출물·인계·경계와 관련 구현을 검토했다. 문제는 숫자 자체보다 중복 라우팅/재질문, 전체 문서 선로드, 모호한 원장 인계, 공급자 정책 충돌이었다. 전문 역할을 유지하고 **현재 단계 소유자 하나 → 필요한 guide → 버전 인계 → 총괄 기록/검사**로 정리했다. 새 스킬이나 자동 에이전트 엔진은 추가하지 않았다.

이 패키지는 지침 모듈과 로컬 도구다. Markdown/agents 설정만으로 17개 워커가 자동 실행되거나 원장이 자동 저장되는 것은 아니다. 실행·기록은 실제 호스트와 총괄이 수행한다. 감사 범위는 이 저장소/연결된 설치 패키지이며 사용자 컴퓨터 전체에 원장이 없다는 결론이 아니다.

## 원장: 발견 위치와 실제 작성

정본은 **`<선택한 사용자 제작 프로젝트>/project.json`**, schema **1.1**이다. 저장소에서 확인한 제작 원장 두 개는 다음 예제다.

- `examples/20-second-animation/project.json`
- `examples/15-second-education/project.json`

`video-production-assets/assets/project-template.json`은 빈 시작 템플릿이며 유효한 완성 계획이 아니다. `manifest.json`, support manifest와 qa 기록은 패키지/감사 자료다. 이번 감사에서 실제 운영 프로젝트 루트가 선택됐다는 근거는 찾지 못했고 사용자 운영 원장을 수정하지 않았다.

`camera_spec.json`은 수치 공간 authority, Brandkit 상태는 브랜드 도메인 상태, 공급자 blocks/job/folder ID는 adapter/locator다. project.json에 버전·dependencies·실제 에셋으로 연결하며 경쟁 전역 원장을 만들지 않는다.

이번에 추가한 실제 도구:

- `video-production-assets/scripts/project_index.py`: 선택한 shot/artifact의 scene/character/beat/panel/voice/audio/claim/asset와 provenance·artifact dependency를 조회한다. 읽기 전용이고 다음 단계를 추측하지 않는다.
- `video-production-assets/scripts/update_project.py`: 총괄이 유효한 **기존** 원장에 부분 레코드를 upsert한다. project/input 버전, 담당 content-owner artifact의 신규 버전, 후보 구조·참조·파일 루트를 검사하고 임시 파일을 원자 교체한다. 영향받는 종속 항목만 stale로 전파하고 독립 승인·미변경 필드를 보존한다.
- 초기 빈 프로젝트 생성·헤더 설계·삭제·사용자 권한 인증·자동 워커 스케줄링은 이 도구의 기능이 아니다. 초기 선택/초안은 기존 프리프로덕션 절차를 따른다. 저장 금지/텍스트 전용 작업은 제안만 반환한다.
- lock은 협력 작성자를 보호한다. 관찰된 비협력 수정은 원본 재확인으로 거부하지만 마지막 순간 비협력 경합/정전 내구성을 보장하는 DB는 아니다. 소유 관계·승인 사실은 실제 사용자 문맥으로 판단해야 한다.

## 17개 역할과 수정 결과

| 스킬 | 현재 담당/산출물 | 구성·인계 수정과 남은 경계 |
|---|---|---|
| creative-production | 유일한 프로젝트 총괄 | 현재 owner만 선택; 단일 산출물은 해당 워커 직행; focused packet/sole writer. 자동 엔진 아님 |
| video-production-assets | 요청된 제작 모듈/기술 통합 | 전체 모듈 재독 금지; 필요한 계약·참조·템플릿만. 렌더러 아님 |
| orchestrating-video-preproduction | 명시된 여러 텍스트 산출물 순서 | 별도 총괄/승인 원장 없음; 확정 spine 재사용, 기술 입력 부족은 indexed requirement 반환 |
| developing-video-synopses | 시놉·안정 beat·원문 locator | 상세 craft 조건 로드, 배정 artifact/version/dependency 제안; 사실/인물 없는 모드 보존 |
| designing-video-character-sheets | 인물/연속성/voice profile | 배정 character/sheet/voice artifact ID; 미제공 나이·신체·과거·반복 개그를 채우지 않음 |
| storyboarding-video | 기본은 완전한 제작 콘티 | 러프는 명시적 요청에만; story/scene/shot/panel 기술 슬롯·전체 이미지 의미 검수 유지 |
| camera-spatial-design | camera_spec와 수치 검사 | 잠근 카메라 재설계 생략; 내용 버전/project/scene/shot/fps/frames/subject reconcile, subset 허용 |
| blender-previsualization | 실제 proxy/프레임/검사 파일 | 지정 action peak와 panel map; spec hash/version/scene/beat 보존; smoke 첫 샷/프레임·긴 변320 이하. 실제 bpy 미검증 |
| higgsfield-generate | 선택된 video/audio/3D/분석 실행 | 이미지/Marketing Studio 상세 조건 로드; 견적 회피/자동 설치 제거; 공급자 locator와 canonical ID 분리 |
| higgsfield-brandkit | 브랜드 도메인 revision/결정적 export | 선택된 root 사용; brand state를 버전 artifact로 연결. 이미지 생성 recipe는 실행 불가 |
| higgsfield-marketplace-cards | listing/A+ craft | 고유 private compliance enhancer는 현 이미지 정책상 실행 불가; generic Codex 동등 결과로 가장하지 않음 |
| higgsfield-product-photoshoot | 제품 촬영 모드/craft | 모드·인터뷰 guide 조건 로드, 확정값 재사용. 전용 enhancer 실행 불가를 명시 |
| higgsfield-soul-id | 명시된 실제 인물 identity training | 동의·별도 비용/실행 scope; reference_id는 identity locator, 이미지/캐릭터 ID가 아님 |
| higgsfield-video-explainer | narrated audio→clips→assembly | 확정 style/voice/settings 재사용; 기존/CMS/허가된 eligible style 입력, 전체 비용 상한·typed join |
| higgsfield-video-replicate | 권리 있는 영상 remake/assembly | 추출/등록된 참조 사용; 이전 프레임 의존 컷은 순차, 독립 컷만 병렬 |
| higgsfield-websites | 명시된 별도 web/app/game lifecycle | 콘티에서 로드하지 않음; website/app cover 브랜드 분리, 실제 visual QA, live deploy와 feed publication 별도 |
| higgsfield-youtube-thumbnail | 사실에 맞는 thumbnail craft/overlay | 긴 prompt doctrine 조건 로드; 원본 사실·identity·실제 canvas/QA 보존. Higgsfield 이미지 생성은 실행 불가 |

현재 정책의 Higgsfield 이미지 제외는 기존 공통 정책이다. 이번에는 충돌하던 하위 지시를 일치시켰다. 전용 enhancer 기능을 실제로 다른 실행기로 재현했다고 주장하지 않는다. craft 준비와 별개로 원래 backend 실행에는 명시적 blocker가 남는다.

## 실제 발견·보완한 참조 결함

수정 전 실행으로 확인한 오류: 없는 source_asset_ids, 없는 character entity_id, 선언되지 않은 dependency_versions 키, 폴더 밖 실제 파일 경로를 통과했고 큰 유한 fps의 프레임 곱은 예외로 종료됐다. 추가로 존재하는 잘못된 종류의 synopsis/voice/spatial artifact, 없는 shot claim, 승인된 review 없이 approved execution plan이 통과했다.

현재는 위 항목을 거부한다. stale artifact만 과거 input version을 보존할 수 있고 현재 승인/실행으로 사용할 수 없다. source/character/beat/provider ID를 등록 artifact dependency로 섞지 않는다. 다른 entity_type의 entity_id는 전문 바이블 locator이며 임의 새 테이블을 강제하지 않는다.

숫자 공간은 실제 등록 JSON이 있을 때 project_id/content version/scene/shot/fps/frame 길이/subject와 연결한다. 실제 이미지 인계의 numeric 공간에는 등록 JSON이 필요하다. 기존 소스 spec 일부만 맡은 작업은 정당하게 허용한다. 이미지 존재/JSON 성공은 이미지 이야기 가독성·음성 품질·승인/동의 사실을 증명하지 않는다.

## 문서량과 판단 부담

같은 방식(Python Unicode 문자 수)으로 SKILL.md 본문+frontmatter만 측정했다.

| 측정 | 이전 | 이후 | 변화 |
|---|---:|---:|---:|
| 총괄 main | 12,405 | 6,525 | 47.4% 감소 |
| 17개 main 합계 | 175,469 | 151,278 | 13.8% 감소 |
| 설치 skill 수 | 17 | 17 | 유지 |

세부 craft는 조건부 참조에 남아 있다. 따라서 **전체 읽기량·토큰·모델 지연·품질의 개선율이 아니다**. 일부 실행 main은 권한·인계 안전장치를 넣어 늘었다. 실제 효과는 미래 단계/provider 문서 미로드, 단일 산출물의 내부 orchestration 생략, 확정 선택 재질문 생략, 같은 수치/원장 조회 중복 제거다. 현재 stage guide 자체는 필요한 만큼 읽어야 한다.

## 준비율: 무엇이 통과했는가

동일 가중치 **24개 점검 기준 중 20개 계약/로컬 구현 충족, 4개 실제 실행 미검증 → 체크리스트 준비율 83.3%**. 작품 완성도, 성공률, 속도, 실제 provider 준수율을 뜻하지 않는다. 소스·로컬 코드 증거와 실제 미디어 증거를 혼합해 100%라 하지 않는다.

20개 충족 기준: 단일 owner, 직접/위임 경계, compact packet, stage-local loading, 승인값 재사용, 워커 ID/version 반환, 안정 synopsis beats, 일관된 완전 콘티 기본값, 전체 board coverage, semantic artifact type, provenance refs, 정확한 dependency versions, focused lookup, camera/project reconcile, previs panel/version join, bounded smoke 구현, canonical ledger authority, guarded single-writer persistence, provider namespace join, 실행 정책 일관성. 상세 before/pass/partial/fail은 QA JSON에 기록했다.

미검증 4개:

1. 실제 공급자 인증·live schema/가격/사용량·실제 terminal 결과.
2. 전체 clean-image 순서의 이야기/소유/인과/감정 가독성과 사용자 수락.
3. 실제 음성 청취·동기화·오디오 결과.
4. 실제 Blender 렌더/.blend 재열기/생성 PNG와 runtime API.

Blender source/frame/resolution helpers를 실행한 증거는 4번 통과를 의미하지 않는다. 초기 draft/자동 DAG/외부 승인 인증까지 제공한다고 계산하지 않는다.

## 수행한 검증

- `python -m pytest -q`: 최종 **118 tests, 156 subtests 통과**, 기존 Windows junction subprocess UTF-8 경고 **2개**. 경고를 수정/숨겼다고 주장하지 않는다.
- 마지막 bounded-smoke 수정 뒤 Blender helper suite: **9 tests, 4 subtests 통과**(기존 전체 결과에 포함된 테스트와 중복이므로 합산하지 않는다).
- 실제 CLI **11개**: focused shot/artifact lookup/없는 ID 거부, 변경 저장·재로드·stale 전파·독립 승인 보존, 오래된 update 거부, registered camera 정상 reconcile/잘못된 fps 거부, 실제 폴더 밖 파일 거부, 거대한 frame product 오류 반환. 같은 batch의 부분 재작성 순서가 downstream stale을 숨기던 edge도 수정 전 재현하고 저장 CLI로 수정 후 확인했다.
- 실제 pure helpers: midpoint 아닌 frame17→P04 매핑, 첫 샷/frame0만 smoke, portrait180×320와 큰 해상도 경계. CLI --help 표면도 확인했다. bpy mock은 사용하지 않았다.
- tool-free instruction scenario **3개**: 제한 패널 재개/no-save, 인물 없는 사실 시놉, 텍스트 제품 사진 기획/no-backend-equivalence. 실제 원장·provider 실행 증거는 아니다. 시놉 trace의 dependency 제안은 registry 확인 전 적용할 수 없으며 공통 계약에서 source/artifact ID 구분을 명시했다.

증거: [최적화 QA](../qa/orchestration-optimization.json), [기준선](../qa/orchestration-baseline.json). 실제 CLI 파일은 격리된 임시 fixture였고 운영 제작 파일·과금·게시를 변경하지 않았다.

## 남은 개선/추가 판단

**새 스킬 추가는 필요 없다.** 우선순위는 기존 실행 표면의 증거다.

1. 실제 선택된 runtime에서 사용자 승인 범위의 최소 작업을 실행해 네 미검증 게이트를 닫는다. 이 감사 자체는 지출/생성 승인이 아니다.
2. 실제 프로젝트 generation_attempts/검수에 소요 시간·시도·비용과 실패 분류를 기록하면 병목을 측정할 수 있다. 문서 길이를 latency로 환산하지 않는다.
3. 원장 기반 읽기 전용 상태/변경 영향 뷰가 필요하면 기존 focused index를 활용한다. 별도 dashboard DB/전역 캐시/새 인터뷰·에이전트 층은 지금 추가하지 않는다.
4. 초기 불완전 draft의 기계적 writer나 완전 자동 DAG가 실제로 필요해질 때만 별도 요구·권한·복구/동시성 계약으로 설계한다. 현재 instruction package에 몰래 자동 실행 기능을 넣지 않는다.
