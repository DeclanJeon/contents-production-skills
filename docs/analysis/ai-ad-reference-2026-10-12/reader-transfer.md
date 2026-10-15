# 독자 인계: 영상 근거에서 저장소 레시피 설계로

이 패키지는 기존 skill 변경물이 아니라, 48개 MP4에 대한 **FRAMES_REVIEWED 근거와 DESIGN_PROPOSAL**이다. 권한·프로젝트·생성 요청이 아니며 원본 표현을 다시 만들도록 하는 프롬프트 모음도 아니다.

## 읽는 순서

1. [video-index.md](video-index.md)에서 원하는 V 표시 ID의 source chapter를 고른다. 표시는 대소문자 무시 파일명 정렬 순번이고 불변 신원은 [video-inventory.json](video-inventory.json)의 원본 SHA-256 `archive_id`다.
2. 먼저 장의 첫 부분에서 직접 살펴본 프레임 범위, 원본 PTS 위치, 제작자/업로더가 밝힌 설명, 오디오 검토 방식을 확인한다. 이어 시간표의 G/SG(해석한 장면 묶음), B(관찰 블록), C(묶인 검출 후보), R(해당 원본의 검출 이벤트), action-phase를 구분해 읽는다. 이 표기는 검증된 프로젝트 쇼트 ID가 아니다.
3. 48편 전체와 비교한 기존 역량 조항은 [DESIGN.md](DESIGN.md) 및 [gap-evidence-fast.md](gap-evidence-fast.md)의 source별 행에서 찾는다. 이미 있는 `25-reference-video-analysis`, `shot-dna-template`, `archive-audit-template`와 카메라·조명·연기·편집·제품·claim·audio QA를 새 결함인 것처럼 이름만 바꾸어 반복하지 않는다.
4. 기존 source-specific craft를 새로 사용 허가된 자산에 옮길 때 DESIGN의 전역 recipe `A01–A12`를 적용한다. fast matrix의 로컬 `R01–R12`는 별도 이름 공간이므로 DESIGN의 의미 대응만 따른다. A-family는 저장소의 기존 schema enum이나 구현된 기능이 아니라 설계 제안이다.
5. [repo capability audit](repo-capability-audit.md), [book source notes](book-source-notes.md), [creator provenance](creator-provenance-notes.md), [citation ledger](web-citations-ledger.json)는 맥락과 출처 주장의 기록부다. 책·업로더 설명·자동 자막은 해당 영상이 실제로 어떻게 촬영·생성되었는지 독립적으로 입증하지 않는다.

## 증거 등급과 주의

* `OBSERVED`: 직접 확인한 프레임, 읽을 수 있는 화면 문자, 원본 metadata/native PTS. PTS는 프레임 위치를 찾는 값일 뿐 편집 경계의 정확도를 보장하지 않는다.
* `ESTIMATED`: 관찰 표본 사이로 범위를 좁힌 장면/샷/phase 경계. `DETECTOR_CANDIDATE`: 알고리즘이 검출한 score event. 어느 쪽도 자동으로 cut 또는 `SH###`가 되지 않는다.
* `INTERPRETATION`: 화면의 순서·크기·형태·행동이 왜 기능할 수 있는지에 대한 가설이며, 대안과 확신도를 함께 쓴다. 화면에서 관찰된 이동과 카메라 원인을 분리한다.
* `DECLARED_UPLOADER_CLAIM`, `CAPTION_TEXT_AUTO_UNTIMED`, `ASR_RUN / HYPOTHESIS_UNVERIFIED`는 서로 다른 근거 유형이다. 화면 자막을 들은 대사로 바꾸지 않고, AAC stream의 존재를 음악/VO/SFX를 들은 것으로 기록하지 않는다.
* 장면(scene)·컷/shot·같은 shot 안의 action-phase는 구분한다. 긴 IKEA 방 구성처럼 계속 바뀌는 장면은 행동 단계로 기록할 수 있다. Santa의 반복 반응과 VO처럼 보일 수 있는 한국어 화면 문구는 시간에 따른 화면 수사로 분석하되 실제 음성이라고 인증하지 않는다.
* 확인된 creator pipeline 주장은 보존하되, 추정한 camera rig/focal length/미터·촬영 장소·공식 브랜드 관계·view/performance 주장은 별도 근거 없이 덧붙이지 않는다. 한 프레임에서 차량 바퀴가 멈추거나 거꾸로 도는 것처럼 보여도 aliasing/strobe/temporal sampling 가능성이 남는다.

## 제안된 변경 경로 (승인·구현 전)

P0: 기존 25 archive 절차와 shot-DNA template에 직접 관찰한 원본 metadata와 추정 경계, `requested_s`와 `actual_source_pts_s`, detector candidate와 검증된 `SH###`, C/B/G/action-phase의 구별을 예시로 보강한다. 기존 `archive_id`와 source mode ledger를 유지하고, 두 번째 coordinator/index/project ID 체계를 만들지 않는다.

P1: 기존 19 product integration, 26 state causality, 21 generated-video QA에 재료·액체·접촉·identity·차량·그림자·반사·endcard의 상태 전이 예시를 **조건부**로 덧붙인다. 세부 주제마다 새 skill을 추가하지 않는다. Recipe에는 선행조건, 보호할 불변값, 행동 순서, 상대 시간 조절값, 전환 대안, 인계 지점, 반례, 관찰 가능한 QA를 두고 새 허가 자산으로 검증한다.

P1: 기존 04 performance, 06 shots, 09 edit, 16 concept에 기대 위반 뒤 반응, 매체 안의 반론, 장난감↔성인 정체성 대응, portal scale break, 동사처럼 변하는 단계적 활자, 재료 여정과 claim 증거의 구분, 생활양식 이미지와 부동산 증거의 차이에 관한 원본별 예시를 제안한다. 소비자 반응을 곧바로 “만족한 고객”, 로고 overlay를 제품 사용, 장소 분위기를 실재 부동산으로 추론하지 않는다.

P2: 기존 07 lighting, 20 visual-mode SSOT, camera-spatial-design, 10 evidence, 23 finishing, 24 production execution의 계약에 실제 프레임 사례와 remaster·생성·출처 층위의 구별을 보강한다. 카메라·연기·오디오·조명 역량을 새로 복제하지 않고 적용 깊이만 더한다.

모든 파일/절 경로는 [DESIGN.md priority list](DESIGN.md#현존-skillsdocs에-제안하는-최소-cutover-수정-금지-구현-시에만)에 제안으로만 적었다. 이는 구현 승인이 아니다. 이 작업에서는 기존 `SKILL.md`/code/config/template/eval 파일을 수정하지 않았다.

## 문서 QA 결과와 적용 전 확인

독립 문서 QA는 [QA-REPORT.md](QA-REPORT.md)의 `PASS_DOCUMENT_SCOPE_ONLY` revision 9 판정으로 마쳤고, 보고서는 QA01–QA22를 닫았다. [독립 검사 결과](evidence/qa-reader-checks.json)는 revision 9 본문 해시와 표·링크·native locator 검사를 기록한다. 이 PASS는 문서 범위에 한정되며 컷 경계/연속 움직임 인증, 영상 전 구간 재생이나 오디오 청취를 뜻하지 않는다. 이후 생산 단계에서는 승인된 자산·권리·주장 근거·프로젝트 입력을 확인하고, 실제 렌더/재생·청취 및 출력 가독성을 별도로 승인해야 한다. 이는 미래 제작 관문이지 현재 문서 QA의 미완료 항목이 아니다.
