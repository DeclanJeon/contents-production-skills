# 영상 근거 분석 방법

## 범위와 식별
- 제공된 폴더에서 `.mp4` 48개를 재귀 탐색했다. 표시용 `V001…`은 파일명 casefold 정렬 순번일 뿐 식별자가 아니다. 안정 ID는 정확한 원본 바이트 해시 `archive_id = sha256:<hash>`이며 전체 파일명·바이트 크기·해시를 함께 보존한다. 파일명만 보고 캠페인 지위, 인기, 조회수, 주장 또는 출처를 추론하지 않는다.
- 산출물은 근거 기록과 설계 제안이며, 원본 수정·게시·업로드·유료 생성·전체 영상 재배포는 하지 않는다. 추출 프레임/contact sheet는 파생 근거이지 원본 영상 자체가 아니다.

## 근거 상태 표기
- `OBSERVED`는 직접 확인한 프레임/시각 또는 실제로 재생해 들은 음향이다. 직접 조회한 메타데이터와 실제 source-frame PTS도 각각 측정 정밀도를 가진 관찰로 기록한다. `ESTIMATED`는 근거 프레임 사이에 범위를 둔 추정 컷/액션 경계 등이다. `DETECTOR_CANDIDATE`는 시각 확인이 필요한 알고리즘 이벤트이며 컷 판정이 아니다. `INTERPRETATION`은 대안/확신을 동반한 craft 기능 가설, `DESIGN_PROPOSAL`은 표현을 복제하지 않는 전이 기법, `UNKNOWN`은 입증되지 않은 상태다. stream 정밀도의 source PTS를 locator로 보존하고 요청 seek 초와 실제 PTS를 혼동하지 않는다. 화면에 보이는 이동과 카메라 원인을 분리하고, 외형과 persona 추론을 분리한다. 픽셀만으로 정확한 focal length/거리/속도/rig/저작자를 주장하지 않는다.

## 계층과 coverage
- 표시 단위와 증거 단위를 분리한다. `C##`는 하나 이상의 detector event에 매핑될 수 있는 candidate neighborhood, `R###`는 소스별 raw detector event, `B##`는 관찰 visual block, `G##/SG##`는 해석상 scene group이다. 이들은 서로 치환되지 않으며 source 전체에서 유일한 ID도 아니다. archive의 `SH###`는 실제 컷 경계를 충분한 근거로 검증했을 때만 쓴다. scene은 이야기/장소 상위단위이고 shot은 편집된 화면 단위, action-phase는 같은 shot 안의 시간상 행위 단계다. 긴 transformation·조리·차량접촉은 한 장면/shot 안의 여러 phase로 기록할 수 있다. morph/dissolve/wipe/match/generative transformation은 전후 상태를 따로 관찰하되 편집경계가 확정되지 않으면 전환 후보로 남긴다. 검정화면·disclaimer·logo/endcard·짧은 flash도 시간순 coverage에서 제외하지 않는다.

- 각 source에서 discovery, metadata probe, full decode, timestamped extraction, frame review locator/timecode, continuous playback, audio listening, 실제 실행 ASR/caption을 별도 기록한다. `requested_s`는 추출 요청, `actual_source_pts_s`는 실제 source frame 시각이다. PTS 정밀도는 해당 프레임을 식별할 뿐 경계 정밀도를 높이지 않는다. ASR 상태(`NOT_RUN`, `ASR_RUN / HYPOTHESIS_UNVERIFIED`, `NO_SEGMENTS_RETURNED`)는 서로 분리하며, ASR은 청취도·검증대사도 아니다. subtitle/caption은 untimed text로만 기록하고 실제 오디오와 임의 동기화하지 않는다.

## shot 기록에 필요한 항목
안정 source ID, source time range, 컷 경계의 확실도/근거 프레임, scene ID 및 action-phase 구간, 화면 사건, 구도/블로킹, 프레임 기준 관찰 이동 및 camera/subject/zoom 원인 후보, 조명/색/재료, 인물·제품·소품 연속성, 관찰 행동과 persona 추론 분리, 편집/전환/모션 단계, 화면 text/logo/CTA, 실제 음향 관찰 또는 UNKNOWN, 대안/확신을 둔 해석/기능, 보호 표현에서 분리된 재사용 메커니즘, 근거 프레임 경로/시각, 미검증 항목을 포함한다. 읽을 수 있는 timestamped frame evidence를 충분한 밀도로 남기고 추출 절차를 기록한다.
하나의 G/scene/action row가 여러 후보 화면 교체를 포괄할 때는 각 C/R 전이를 별도 하위행이나 근거표에서 다룬다: native PTS·candidate locator, 전/중/후의 framing·screen-motion·새 정보/액션 역할, 해당 지점에서 선택됐을 수 있는 구체 기능, 명시적 `[INFERENCE]` 확신도와 대안, 전환/연속성 실패 조건 및 새 brief로의 전이 QA를 연결한다. 여러 C가 실제 한 shot의 pose/행동 변화라면 cut으로 세지 말고 action-phase의 역할을 분리한다. 기능을 뒷받침할 근거가 부족하면 반복적인 “리듬/질감” 이유를 꾸며내지 않고 `기능 미확정`과 bounded alternative를 기록한다. 후보 이벤트 수를 shot 개수로 맞추기 위한 허위 세분화도 금지한다.

모든 source별 사실 주장은 해당 chapter에서 직접 확인한 원본 프레임/timecode locator 또는 기계 생성 원자료에 연결한다. 별도 미디어 preview·타인의 서술은 독립적으로 보지 않은 한 이 분석의 `OBSERVED` 근거로 승격하지 않는다. Santa의 한국어 화면 글자는 VO를 들었다는 근거가 아니다. 오디오 청취는 별도 mode다.
## 실제 pass의 coverage 경계

- 인벤토리 `coverage.reviewed_native_frames`에는 실제 확인된 이미지의 원본 frame n/PTS/image/sheet 및 review basis가 들어 있다. V001–V024에는 추가 raw-event frame 삼중항/PTS/R ID 배열이 있으며, V025–V048에는 fast worker extraction manifest의 실제 frame IDs/PTS가 병합되었다. V005/V013/V014/V016/V023/V024에는 별도 보충 pass의 337 review-display 수와 58 source/candidate sheets 수를 따로 기록했으며, 중복 가능성이 있으므로 이를 unique-frame 수에 더하지 않는다. `evidence/repo-worker-coverage-merge.json`과 각 strip을 교차 확인할 수 있다. 그 배열/수치는 검토된 표본이지 전체 원본 프레임 집합이나 편집 컷 인증이 아니다.
- 48개 원본 모두 probe 및 FFmpeg full decode 성공(인벤토리 기계 로그), 전체 raw scene-score 후보는 1,035건. 1,035건은 **검출 이벤트 수**이지 컷/장면 수가 아니다. 48개 전부의 candidate neighborhood를 native-source-frame 이웃으로 실제 검토했지만, threshold가 놓친 경계, neighborhood 사이의 프레임, 연속 camera/subject motion은 전수 검증하지 않았다. Raw judgments도 verified `SH###`로 합산/승격하지 않는다.
- First-half raw supplement는 24 source, 496 events, 1,468 unique native frames, 71 visual strips를 기록한다. 이전 463 group representative만으로 raw event coverage를 주장할 수 없었고, 33개 raw center frame은 supplement에서 새로 추출/검토했다. Group/event/frame 수는 각각 다른 coverage 단위다. Second-half coverage는 fast worker의 source evidence/chapter와 `evidence/repo-worker-coverage-merge.json`을 확인한다. 중복 source samples를 unique native frame 수로 더하지 않는다.
- 이 pass는 **FRAMES_REVIEWED**이며 continuous playback 0건, human audio listening 0건. AAC presence는 heard VO/music/SFX를 뜻하지 않는다. 실제로 run된 local ASR는 `ASR_RUN / HYPOTHESIS_UNVERIFIED`; returned caption bodies는 `CAPTION_TEXT_AUTO_UNTIMED`로 분리한다. Creator/uploader text는 `DECLARED_UPLOADER_CLAIM`, preview observation은 그 preview scope에만 한정한다.

모든 source별 범위는 [video-index](video-index.md)와 chapter 상단을 따른다. 모든 boundary는 추정일 수 있으며; “candidate frames read”를 “all cuts verified” 또는 “full playback”으로 바꾸지 않는다.
