# 대사 연기 큐

캐릭터: {공급/기존 character_id} | character_sheet: {배정된 artifact ID·version 또는 미배정} | voice_profile: {배정된 ID·version 또는 미배정 — character_sheet에서 파생} | persona 요약: {role/personality/observable_behavior/speech — SSOT 정본에서 파생, 별도 편집 장소 아님}

보이스: {실제 선택 기록의 voice ID·타입·모델/버전·설정 또는 미선정} | 음성 asset_id: {실제 ID 또는 미생성} | 권리/동의: {공급 근거 또는 미확인} | 청취 검수: {실제 결과/범위 또는 미검증}

voice_identity_direction: {모든 발화에 재사용하는 고정 음성 정체성 — 청각 앵커·발음·문장 끝 습관·기본 리듬·허용 변화 범위}

미지원 제어 간극: {요청했으나 현재 도구가 지원하지 않는 제어와 그 처리 — 적용했다고 주장하지 않음}

| 시간/대사 | 화자 | 의도/서브텍스트 | 숨/멈춤 | 강조 | 속도/압력 | 입 우선순위 | 청자 반응 | 신체 행동 |
|---|---|---|---|---|---|---|---|---|

규칙: 각 행은 그 대사의 `performance_cue`다 — 정확한 대사·의도/서브텍스트·숨·멈춤·강조·속도/압력을 생략하지 않는다(특별한 변화가 없으면 자연/기본/없음을 명시, 장면 근거 없으면 미정). 고정 정체성은 위 `voice_identity_direction`에만 둔다. 상태 변주는 음색·발음 앵커를 유지한다. 무언 역할의 음성 큐는 이유를 적은 N/A이며 시각 연기는 별도 표현 연결로 넘긴다. `proposed`/`unresolved`는 선택됨이 아니며 미지원 지시를 TTS 대사 본문에 넣지 않는다.
