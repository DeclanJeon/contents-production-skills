# 스킬 지도 — 단계별 담당 스킬과 CineForge 인계 계약

`creative-production`이 프로젝트 하나를 처음부터 끝까지 끊김 없이 진행할 때 쓰는 지도다. 단계마다 담당(owner)은 [routing.csv](routing.csv)의 한 행이며, 이 문서는 순서와 인계만 정리한다. 승인·권한 규칙은 [policy.md](policy.md)가 유일한 기준이다.

## 1. 단계 순서

| 단계 | 하는 일 | route | 담당 스킬(보조) | 다음으로 넘어가는 조건 |
|---|---|---|---|---|
| S00 접수·분석 | 요청 해석, 9개 판단 요소 판정 | — | creative-production | 항상 |
| S01 선택 | 열린 콘셉트 축을 한 번에 선택(대화형) | R33 | concept-intake-design | 필수 축이 모두 채워짐 |
| S02 조합·평가 | 조합, 적합성 검사, 연출 규칙 변환, 6개 기준 평가 | R33 | concept-intake-design | 차단 오류 없음 |
| S03 기획안 | 시놉시스·후킹·타임라인·씬/컷·캐릭터·제작 설계·확인 사항 | R05 (시놉시스만이면 R02) | orchestrating-video-preproduction (developing-video-synopses) | 사전 점검 실패 없음 |
| G1 기획안 검수 | 자동 검수 + 사용자 승인 | — | creative-production | 사용자 승인(또는 사용자가 미리 위임) |
| S04 대본·스토리 | 비트, 대본, 대사 밀도 | R13 | video-production-assets (developing-video-synopses) | 대본 확정 |
| S05 캐릭터·세계관 | 캐릭터 바이블, 페르소나, 의상, 소품, 장소 | R03 / R04 | designing-video-character-sheets / designing-character-personas | 정체성 앵커 고정 |
| S06 연출·스토리보드 | 컷별 상태, 카메라, 동작, 타이밍 | R10, R18, R08, R07 | storyboarding-video, camera-spatial-design, animatic-direction, silent-visual-storytelling | 컷 합계 = 러닝타임 |
| S07 에셋·프롬프트 | 에셋 목록, 시작/끝 프레임, 이미지·영상 프롬프트, 사운드 큐 시트 | R13, R19 | video-production-assets, ai-camera-control | 프롬프트가 SSOT 버전을 참조 |
| S08 선행 작업: 스틸 에셋 생성 (구 S07b, G2 이후 별도 승인 범위) | 캐릭터 7뷰·의상·장소 4뷰·배경·소품·LOOK·컷 프레임 실제 생성 | R13 | video-production-assets, codex-imagen | 참조 의존 순서·최대 5개 병렬·해시 등록; `available`은 `verified` 아님 |
| G2 프리프로덕션 검수 | 연속성·제약·권리·비용 | — | video-production-assets (연속성 게이트) | 오류 없음 + 승인 |
| S08 생성 | 이미지·영상·음성 생성, 테이크 선택 | R28 / R32 | higgsfield-generate 또는 fal 경로 | **실행·비용 승인 필요** |
| S09 편집 | 조립, 사운드 믹스, 색, 자막 | R31 | video-production-assets | **편집 계획 승인 필요** |
| S10 품질 검수 | 연속성·카메라·싱크·전체 검수 | R20 | video-production-assets | 실제 결과물 검사 |
| G3 최종 검수 | 사용자 승인 | — | creative-production | 사용자 승인 |
| S11 출력·이력 | final/ 저장, 이력 기록 | R27 | recording-production-history | 경로 보고 |
| S12 성과 피드백 | 성과 지표 → 다음 기획 가설 | — | topic-demand-selection, searching-social-media | 사용자가 요청할 때만 |

## 2. 경로 밖 보조 스킬

- 소재·주제 선정이 먼저 필요하면 `topic-demand-selection`, 공개 SNS 레퍼런스 검색은 R01 `searching-social-media`.
- 레퍼런스 영상의 카메라 분석은 R16, 실제 3D 검증은 R22/R30, 스틸 이미지 영상은 R12, 무성 풍자 애니메틱은 R09, 스틸 쇼츠 파이프라인은 R29.
- 정체성 고정(Soul ID), 설명 영상, 레퍼런스 복제, 썸네일 같은 공급자 모드는 [production-routing-optional.md](production-routing-optional.md)를 따른다.

## 3. 논스톱 진행 규칙

- PRE·PROD·POST의 [2회 검수 및 호스트 재개 계약](phase-review.md)을 따른다.

- 사용자 선택은 S01에서 한 번만 받는다. 이후 담당 스킬은 콘셉트 패킷을 상속하고 다시 인터뷰하지 않는다.
- 검수 게이트(G1, G2)는 사용자가 "논스톱으로 진행"처럼 명시적으로 미리 위임했을 때만 자동 통과로 기록한다. 위임은 실행·비용 권한을 열지 않는다.
- S08·S09는 실행/편집 권한이 기록되어 있을 때만 진행한다. 없으면 인계 패킷을 만든 채 멈추고 필요한 승인을 정확히 말한다.
- 막힌 단계가 있어도 그와 무관한 계획 작업은 계속한다.

## 4. CineForge CLI 인계 계약(선택 사항)

CineForge는 이 패키지 밖의 개인 프로젝트 CLI다. 설치된 경우에만 쓰며, 없으면 위 순서를 에이전트가 직접 수행한다.

- 프로젝트 폴더의 `progress.json`이 단계 상태(`pending`/`running`/`waiting_user`/`waiting_agent`/`blocked`/`waiting_external`/`done`/`stale`)와 진행률·작업률·검수 상태를 가진다.
- `handoffs/<단계>.json`: `route`, `owner_skills`, `authority_required`, `authority_granted`, `inputs`(SSOT·기획안 경로), `outputs_expected`, `completion_command`. 담당 스킬은 이 패킷을 입력으로 받는다.
- `agent_io/requests/<task>.json` → `agent_io/responses/<task>.json`: CLI가 판단·생성을 호스트 에이전트에게 맡길 때의 요청/응답 파일. 형식은 [decision-provider.md](../../concept-intake-design/references/decision-provider.md).
- 외부 단계가 끝나면 실제 결과 파일을 증거로 `cineforge complete <프로젝트> <단계> --evidence <파일...>`. 증거 없는 완료는 거부된다.
- CineForge는 유료 생성을 직접 호출하지 않는다. 생성·편집은 위 route의 스킬이 사용자 승인 아래 수행한다.
