# 공통 제작 계약 — 최소 인계

전문 단독 산출물의 기본 계약이다. 원장 작성/수정 때만 [project](contract-project.md), 전체 이미지 기반/FINAL 때 [package](contract-package.md), 패키징/납품 때 [delivery](contract-delivery.md)를 추가한다. 전체 계약 탐색은 [호환 색인](contract.md)을 따른다.

## ID와 단위
- project_id는 프로젝트 내 고유값으로 정한다. scene_id S01, beat_id B01, shot_id SH01, character_id CH01, claim_id CL01, sound_id AU01, artifact_id A01 형식을 권장하되 기존 체계를 우선한다.
- 시간은 초 단위 숫자로 기록한다. 최종 타임라인은 start_s 포함 / end_s 미포함이다. fps는 초당 프레임 수다. 프레임 범위는 시작 포함 / 끝 미포함이며 길이는 (end-start)/fps다.
- 생성/촬영 원본 길이 source_duration_s와 최종 편집 구간 길이를 구분한다. final 구간은 겹치지 않는다. 전환과 오디오 중첩은 별도 레이어 큐로 표현한다.
- 기본 계약의 최종 영상 구간은 0초부터 target_duration_s까지 연속으로 덮는다. 블랙·정지·타이틀도 하나의 shot으로 기록한다.


## 상태와 버전
- artifact 상태: draft / reviewed / approved / generated / verified / stale.
- approved는 실제 사용자 또는 위임된 승인 사실이 있을 때만 기록한다. generated는 실제 파일이 생성됐을 때, verified는 해당 파일을 검사했을 때만 기록한다.
- 버전과 dependency를 기록한다. 상위 각본이 바뀌면 영향을 받는 샷과 계획을 stale로 표시한다.
- `assets/project-template.json`의 빈 배열과 null은 작성 시작 상태다. 검사 통과 예제가 아니다.


## 인계 최소값
각 산출물에 입력 ID와 버전, 생성한 항목 ID, 가정, 실제 검증 결과, 다음 단계 미해결 사항을 붙인다. 재생성에는 바뀐 변수와 실패 타임코드를 남긴다. 같은 정보를 복사해 여러 문서에서 따로 변경하지 말고 공통 원장을 기준으로 조회한다.


## Worker handoff and single writer

현재 단계에 필요한 조각만 인계한다. 이 패킷은 일시적 실행 문맥이며 새 원장/스케줄러가 아니다. 단독 채팅 산출물은 project.json·프로젝트/산출물 ID를 새로 요구하지 않는다. 기존 프로젝트라면 선택된 `<project-root>/project.json`이 정본이고, 설치된 skill/support 폴더에는 제작 데이터를 쓰지 않는다.

**입력 패킷:** 실제 project_root/project_id/project version(존재할 때), 한 개의 assigned stage와 requested output, 담당 artifact/entity/scene/shot/beat/panel/cue ID와 수정 범위, 소비하는 artifact ID→version, 필요한 소스/범위, 잠근 사실·연속성·제외 조건, 관련 승인 근거, 미해결 입력. 이미 확정된 값을 재질문하지 않고 다른 단계의 상세 문서를 미리 읽지 않는다. 별도 원장 없이 필요한 필드만 조회한다.
선택 필드 `craft_refs`: 총괄이 현재 단계에 맞춰 고른 크래프트 참조 경로 목록이며, 담당은 자기 절차와 함께 읽는다. 담당 절차·경로 경계·게이트가 우선하며 참조는 권한·범위를 넓히지 않는다. 원장 필드가 아니다.
source/character/beat/provider ID는 artifact ID가 아니다. dependencies/dependency_versions/input_versions에는 **정본에 등록된 artifact ID만** 넣는다. 등록 여부를 확인하지 못한 입력은 source locator 또는 등록 제안으로 반환하며 실제 dependency라고 꾸미지 않는다.

**워커 반환:** 담당 output ID와 output version, dependencies/dependency_versions 제안, 바뀐 레코드 제안, 실제 파일/공급자 locator와 관찰 상태·검수 근거/한계, 가정과 blocker. ID는 배정된 값 또는 명시적 신규 등록 제안으로 구분한다. 부족한 공간/음성/참조 입력은 scene/shot/beat ID별 요구 패킷 한 개로 반환한다. 워커가 총괄을 재호출하거나 현재 범위를 넓히지 않는다.

**총괄만 작성:** 저장·변경이 허용된 기존 프로젝트에서 현재 입력 버전을 다시 읽고 stale 결과를 거부한다. 담당 변경과 해당 소유 artifact 버전만 반영하고 종속 승인만 stale로 표시한다. 저장 후 다시 읽어 검사하고 다음 배정 단계에 넘긴다. 워커는 project.json을 동시 수정하지 않는다. 명시적 no-save/read-only/chat-only 요청은 반환 제안에서 끝난다. 텍스트만이라도 MD/PDF 저장 요청은 허용된 파일·이력 단계만 수행하며 새 미디어는 생성하지 않는다. 초기 프로젝트 선택·초안 작성은 기존 프리프로덕션 절차이며, 아래 도구는 자동 생성/자동 실행 엔진이 아니다.


## 버전 변경과 범위
변경된 산출물과 그 하위 인계를 stale로 표시하고 입력 버전을 갱신한 뒤 관련 항목만 재검수한다. 계획 패키지가 완성됐어도 실제 영상이 완성된 것은 아니다. 참고 후보·예산·도구 기능이 미정이면 계획에서 가정으로 남기고 실제 실행 직전에 확인한다.
