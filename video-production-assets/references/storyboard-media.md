# 스토리보드 — 실제 이미지·시트·추출·전수 QA

실제 이미지 생성/시트·추출·검사 단계의 정본이다. [core](storyboard-contract.md)+[direction](storyboard-direction.md)의 완전 설계를 먼저 적용한다. 전체 이미지 패키지는 [package](contract-package.md)를 함께 지키고, PDF 단계에는 [delivery](storyboard-delivery.md)를 추가한다. 아래 번호는 core의 기존 절 번호다.

## 4. 실제 이미지 생성·시트·clean 컷

[프리프로덕션 검토](preproduction-review.md)의 정확한 폴더·승인·실제 파일 등록을 적용한다. 이미지마다 승인된 캐릭터/소품 reference를 실제 입력으로 연결하고 프롬프트와 입력 버전을 기록한다. 이미지 프롬프트는 §3의 적용성 원칙에 따라 그 순간의 물리적 상태와 장면에 적합한 관찰 가능한 단서만 선택해 묘사한다. **운동 에너지·속도 벡터(동세선·포어쇼트닝·2차 물리 관성)·안면 해부학적 표정·전경/중경/배경 3단 공간 인과**는 해당 장면에 적용할 때만 사용하며, 비인간·얼굴 없음·표정 유보·평면·정적 구도에는 대체 큐 또는 사유 있는 N/A를 허용한다. 승인된 적용 가능한 strict 프로젝트 제약은 유지한다. 프롬프트는 사용자 직관 검수용 `[KO 연출 요약]`과 생성 엔진 최적화용 `[EN 시네마틱 프롬프트]`를 병기할 수 있다. 카메라 경로와 소리는 메타데이터에 남기며 정지 그림이 시간 재생을 실행했다고 말하지 않는다.

개별 clean 이미지로 생성하면 그 파일을 정본 에셋으로 쓰고 검토용 시트는 파생 레이아웃이다. 업로드/생성된 합본 시트만 있으면 전체 panel 인덱스와 셀 pixel 경계를 먼저 확인한다. 없는 셀·오인된 순서·라벨/테두리 포함 crop은 수정 전 추출하지 않는다.

**전체 이미지 기반 프리프로덕션 패키지에서는 합본 보드가 필수 실제 산출물이다.** 개별 clean 이미지가 정본이라는 말은 합본을 생략해도 된다는 뜻이 아니다. 시놉 MD·캐릭터별 페르소나/SSOT MD·실제 7뷰 Identity Sheet A를 먼저 연결하고, 각 shot의 character_ids/asset_ids와 board artifact의 synopsis/character_sheet dependency_versions를 정합한다. 텍스트-only/독립 패널 프롬프트 요청에는 이 이미지 실행을 강제하지 않는다.

`python <skill-dir>/scripts/render_storyboard_sheet.py <project.json> --base-dir <project-root> --output storyboards/sheets/<새-sheet.png> [--font <Unicode-font>] [--panels-per-sheet 1..8]`는 canonical panel 순서대로 실제 파일을 열어 시트 세트를 조립한다. 기본은 한 시트 최대 4패널이다. 세부 판독용 1–2패널 또는 전달 크기에서 읽힘을 확인한 개요용 최대 8패널을 명시적으로 선택할 수 있다. 여러 시트의 파일명은 `<stem>_sNN.png`다. 시놉 원문 위치, 패널별 ID·시간·SSOT·촬영 캡션은 clean 영역 바깥과 PNG metadata에 기록한다. 기존 출력은 덮어쓰지 않으며 Pillow/Unicode 폰트가 필요하다.

각 시트의 path/sha256/panel_ids/sheet_index/sheet_count/source_asset_ids/source_sha256를 `kind=storyboard_sheet` asset과 현재 보드 버전에 의존하는 `type=storyboard_sheet` artifact에 등록한다. `preproduction.storyboard_sheet_artifact_ids`는 한 장도 이야기 순서 배열로 쓴다. 모든 시트의 구간을 이어 붙이면 정본 패널 순서와 정확히 같아야 한다. `source_sheet_asset_id/crop_box`는 입력 이미지의 crop이며 출력 시트 pointer가 아니다. 실제 시트 전수 검수와 아래 필수 분리를 마친 뒤 strict 검사·검토로 인계한다.


생성 직후 `python <skill-dir>/scripts/split_storyboard.py <project.json> --base-dir <project-root> --output <project-root>/storyboards/<새-cut-폴더> --sheet <프로젝트-relative 시트> ...`로 생성된 모든 시트를 순서대로 지정해 clean 패널과 장면 overview를 분리한다. 실제 이미지/hash와 `kind=storyboard_split_manifest` JSON을 등록하고 `preproduction.storyboard_split_asset_id`로 연결한다. 이 모드는 기존 `panel.image_asset_id`를 덮어쓰지 않는다. 입력 crop/clean 파일만 분리하는 별도 요청에는 `--sheet` 없는 입력 모드를 쓸 수 있다. 모든 추출 패널과 장면 이미지를 다시 열어 순서·정체성·가림·해상도·경계를 검수하고 실제 절대 경로를 보고한다.
분할 출력 폴더는 project-root 안의 **새 폴더**여야 한다. 파일명용 panel ID는 `[A-Za-z0-9][A-Za-z0-9_-]*`를 사용하고 대소문자만 다른 중복도 거절한다. 잠긴 원본 ID를 조용히 바꾸지 말고 부적합한 ID는 추출 전 충돌로 보고한다. 합본 셀과 기존 clean 파일 모두 실제 디코딩을 검사하며 JPEG 입력도 픽셀을 PNG로 저장한다. 추출기는 의미/자막 경계를 자동 인식하거나 그림을 보정하는 도구가 아니다.


## 5. 이미지 단독 스토리텔링 게이트

두 번 검수한다: **① 텍스트 설계의 시각적 인과 ② 실제 clean 이미지 전수 검수**. ①만 통과한 것을 이미지 검수 완료라고 하지 않는다.

1. clean 컷을 이야기 순서로 나열하고 보드 라벨·패널 설명·대사 트랙·나레이션·BGM/SFX를 숨긴다. 데이터/교육형에서 사실 자체인 승인된 숫자/그래픽은 남기고 외부 해설만 숨긴다.
2. 이미지에서만 읽은 사건/정보/관계/감정 흐름을 먼저 적는다. 가능하면 승인 시놉을 보지 않은 검토자에게 읽히게 하고, 그렇지 않으면 자기검수 한계를 명시한다.
3. 이를 승인 시놉과 대조한다: 누가/무엇이, 어디에서, 무엇을 발견/선택/변화시켰고, 왜 다음 컷이 따르며, 결말에 무엇이 달라졌는가. 모든 beat를 visible evidence panel ID에 연결한다. 추상/음악형은 의도한 모티프·형식 변화를 기준으로 본다.
4. 소품 이동·점유/손·위치·시선·화면축·정체성·공개 순서·감정 변화가 눈으로 확인되는가. 반전은 조기 공개하지 않되 앞선 단서는 읽혀야 한다.
5. 대사 의존 작품도 영상층의 사건과 관계 변화는 읽혀야 한다. **이미지만으로 전달할 수 없는 명제/정확한 대사는 한계로 명시**하고, 사용자 목표가 이미지 단독 이해라면 허용된 시각 행동/상태로 바꾸거나 변경 승인을 요청한다. 조용히 낮은 기준으로 통과시키지 않는다.

누락/중복·인과 단절·가려진 필수 행동·불명확한 점유/감정·요구된 미검증 공간/이미지는 blocker다. 자막/음악을 더해 결함을 숨기는 대신 구도·시점·행동 가시화·패널 분할·연결컷을 최소 수정한다. 핵심 행동 실루엣, 주목점, 정보 위계가 실제 clean 이미지에서 읽히지 않으면 시각 가독성 blocker로 기록한다. 문서에 쓴 의도는 실제 이미지에서 읽힌 증거가 아니다. 구조 validator 성공·LLM 판단은 이 게이트나 사용자 수락을 대신하지 않는다.
