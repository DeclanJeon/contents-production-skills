# 영상·오디오 실제 참조 인계 보완

상태: 사용자가 기존 A 방식의 누락 두 항목 보완과 직접 작업을 요청했다. 기존 시퀀스 실행 설계의 증분이다. 별도 생성/지출/업로드/게시 권한은 없다. 독립 검토를 다시 실행하지 않고 이전에 승인된 직접 구현·테스트 방식을 유지한다.

## 목적과 방식

기존 a85fac2는 이전 채택 구간의 영상 관찰과 편집 후 음향 연결을 검사하지만 생성 전 음향 인계, 실제 MCP reference 선택을 충분히 검사하지 않는다. 설명을 늘리는 대신 generation 게이트에 공통 AV 요구와 실제 wire 입력 어댑터를 연결한다. 모든 도구에 같은 조건을 적용하고 미등록/미확인 transport는 통과시키지 않는다. Ludyte는 현재 contract 1.14.0을 읽어 구체화한다. 다른 도구는 현재 native schema와 검증된 adapter artifact가 있는 명시적 배열 선택 어댑터를 쓴다. 필드/지원이 안 맞으면 별도 경로를 제안하고 조용히 생성하지 않는다.

‘항상 이전을 참조’는 해당 서사 선행 결과를 실제 검토하고 관련 상태·음향을 인계한다는 뜻이다. 첫 컷은 초기 정본, 새 앵글은 새 구도+이전 상태, 시간/장소 전환은 허용 변화와 지속 상태를 따른다. 이전 raw 파일의 실패 꼬리, 앞 대사/효과의 재연, 이전 카메라 복제는 기본값이 아니다.

## 데이터와 실행

project.json은 그대로 정본이다. 기존 sequence-execution/1 투영에 `generation_handoff`를 추가한다. 필수 wire 계약/프로젝트/실행 승인·자산 version/hash는 기존 inputs에 핀한다.

1. 현재 focus 샷의 들어오는 모든 실제 선행 컷을 찾는다. requires_actual_predecessor=false로 임의 면제하지 않는다. 이전 source_range와 observed exit에 더해, 소리가 있는 프로젝트는 이전 source_audio/listening을 현재 선택 범위로 확인한다. 소리가 없는 실제 소스의 N/A는 실제 probe와 이유를 확인하며, global no_audio는 음향 인계 N/A다.
2. 영상 상태, 오디오 맥락, 재등장 목소리 기준을 별도 요구로 계산한다. 같은 voice_artifact_id가 서사상 이전에 사용됐다면 그 승인/검증된 실제 voice anchor를 이어받는다. 새 목소리 첫 등장은 초기 정본에서 시작하며 아직 없는 이전 음성은 발명하지 않는다.
3. bindings는 purpose(visual_state/audio_context/voice_identity/current_composition 등), source_cut_id 또는 voice_artifact_id, 실제 reference_asset_id, modality, native reference/asset ID, role, imports/excludes를 연결한다. 선택 구간에서 추출한 reference는 version/hash와 source_asset_ids 및 sequence_slice(parent/source in/out/FPS)를 가진다. 영상 참조는 채택 출구에서 끝나고, 이미지 대안은 마지막 포함 프레임이어야 한다. 오디오는 없는 stem을 분리했다고 하지 않는다.
4. Ludyte get_session/get_session_assets의 실제 요청+응답 스냅샷, 현재 capability contract, 로컬 파일→완료된 업로드→native ID 연결 기록을 핀한다. message.reference_ids는 **items[].id**이며 asset_id/URL이 아니다. 첨부만 하고 선택하지 않거나 빈 리스트로 이전 선택을 상속하는 것을 허용하지 않는다. 필수 ref는 ready, non-archived, model_requirement=required, 정확한 role이어야 한다. 실제 session 및 expected_revision도 맞춘다.
5. 일반 transport는 canonical verified/approved adapter artifact에 저장한 실제 request/schema/readiness JSONPointer를 사용한다. 선언되지 않은 adapter, 없는 필드, 지원 역할 불명은 차단한다. ID를 텍스트에 쓴 것으로 첨부를 대신하지 않는다.
6. `prepare_generation_request.py`는 기존 generation 검사와 새 인계를 통과한 **정확한 tool+arguments+request SHA**만 반환한다. 외부 호출은 하지 않는다. 코디네이터가 그 패킷으로 실제 도구를 호출하고 호출 기록을 비교한다. `--audit-call`은 실제 tool/arguments 기록이 준비한 요청과 같은지 대조하며, 수신 성공/모델의 conditioning 효과와 구분한다. 타임아웃은 outcome unknown이지 재제출 허가가 아니다.

오디오 유지가 native reference로 미지원이면 거짓 참조를 만들지 않는다. 이미 존재하는 승인된 연속 음향/음성 마스터를 편집에서 재사용하는 계획을 제안할 수 있지만, 승인된 audio delivery plan과 실제 해당 자산/큐가 있어야 한다. 이 경로에서는 생성 오디오는 명시적으로 꺼야 하며, 새 대사를 이전 대사 재생으로 대체하지 않는다. 이 증분은 해당 대안을 설명하고 승인 없는 임의 우회를 막는다. 새로운 TTS/음악/복제 작업은 실행하지 않는다.

## 실제 한계

이 패키지는 Pi/MCP 서버의 전역 호출 interceptor가 아니다. 규정된 스킬 경로의 준비·감사 명령을 통한 입력을 검사한다. 로컬 snapshot과 upload 증거의 진실/서명, 서버 내부에서 어떤 tensor를 썼는지, voice identity/물리/립싱크 품질까지 인증하지 않는다. NOT_EXPOSED는 미노출로 기록하고 실제 출력 재생·청취 검수는 유지한다. 문서/단위 시험을 실제 공급자 생성 성공 또는 fresh-context 행동 검증으로 보고하지 않는다.

## 수락 시험

- 이전 음향 미청취·옛 선택 구간의 청취 기록은 generation에서 차단.
- 영상 ref/오디오 ref/재등장 voice anchor 중 하나라도 누락되면 차단.
- 처음 영상화되는 미래 샷이나 첫 등장 목소리를 과거 자료 부재로 잘못 차단하지 않음.
- Ludyte reference_ids 누락/빈 리스트/asset UUID 혼동, 잘못된 session/revision, pending/candidate/archived ref, 잘못된 role, stale file/upload hash는 차단.
- 새 앵글에서 이전 이미지를 first_frame으로 강제하거나 실패 tail/전체 raw를 인계하면 차단.
- schema 기반 일반 adapter의 실제 배열 필드만 허용하고 unknown 도구는 차단.
- prepare가 생성/업로드를 실행하지 않고 actual-call audit이 다른 첨부/본문을 검출.
- 기존 plan/edit/export·합성 ffmpeg 회귀, 원본 불변, 스킬 진입 경로 유지.
