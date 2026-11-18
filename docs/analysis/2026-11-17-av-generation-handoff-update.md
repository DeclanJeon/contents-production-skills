# 생성 전 AV 및 native 호출 인계 보완

## 변경 범위

기존 sequence-execution/1의 generation 경로만 보완했다. project.json 외의 원장, 새 root 상태 enum, 전역 MCP hook, 실제 영화 생성/업로드/과금은 추가하지 않았다. 앞서 게시한 a85fac2와 달리 이번 보완은 아직 미커밋이다.

- `generation_handoff.py`: 실제 선행 채택 구간, 연속 재생·음향 청취 근거, 원본 버전/해시/FPS/in/out에 묶인 파생 참조, 현재 구도, 재등장 voice anchor를 검사한다. 첫 컷/최초 목소리/global no_audio는 별도로 처리한다.
- `generation_transport.py`: Ludyte Task reference ID의 명시적 선택, 정확한 session/revision, required/ready/non-archived·실제 role/kind·업로드 바이트 대응을 검사한다. 일반 MCP는 승인/검증된 실제 schema-pointer adapter에서만 허용하며 native prompt/model/audio behavior/readiness도 대조한다.
- `prepare_generation_request.py`: 검증된 native tool/arguments와 해시를 준비하고 실제 호출 기록을 감사한다. 자체 네트워크·업로드·생성은 없다. 패킷/실제 첨부·본문·설정 변경과 JSON 타입 차이를 검출한다. timeout은 unknown이고 감사로 재제출 권한을 부여하지 않는다.
- `validate_sequence.py`와 기존 owner reference 11/29/sequence-execution에 위 필수 경로를 연결했다. 실행·계정·모델·가격·Unlimited·권리·게시 승인 게이트는 유지한다.

## 검증

모든 native 수신/업로드 기록과 승인 표시는 합성 fixture다. 실제 공급자 업로드, 실제 영화 재생/청취, 모델 conditioning 시험이 아니다.

- 이전 누락 21개, 실제 prompt 절/부모 hash 2개: 기존 RED→GREEN 증거를 재사용했다.
- 일반 어댑터의 prompt/model/audio/readiness 검증: 5개 실패를 확인한 후 수정했다.
- 준비·감사 CLI: 모듈 미구현 실패 → 구현 → 정상/누락/변경/timeout/실패/파일 불변/CLI round-trip을 검사했다. 정수·실수의 Python 동등성으로 실제 JSON 타입 변경이 숨는 실패도 재현 후 수정했다.
- 현재 추가 테스트 45개: handoff 25, transport 8, prepare/audit 12. 합성 ffmpeg 영상/오디오의 실제 probe와 파일 해시를 사용한다.
- feature worktree 전체 pytest: **939 passed, 4 skipped, 533 subtests passed / 55.20s**. 4개 skip은 Linux에서 Windows junction을 시험할 수 없는 기존 플랫폼 제한이다.
- `git diff --check`, 준비 CLI `--help` 통과. 원래 설치 소스에는 기존 4개 파일의 a85fac2 바이트 일치와 새 10개 경로의 부재를 확인한 후 소유 파일 14개만 반영했다. 설치 링크는 원래 소스를 유지한다.
- 원래 설치 소스의 `video-production-assets/scripts` + `scripts/test_storyline_continuity_gate.py`: **401 passed, 195 subtests passed / 33.57s**. 별도 동시 작업을 포함한 원래 저장소 전체 suite를 통과했다고 표기하지 않는다.
- 최종 대응 해시는 `mirror-verification.json`, 설치 소스 검증은 `installed-regression.log`에 남겼다. Git commit/push는 이번 보완에서 실행하지 않았다.
- 로컬 로그: 원래 저장소의 `.superpowers/sdd/2026-11-17-av-generation-handoff/` 아래 `explicit-red.log`, `task2-complete.log`, `task3-red.log`, `task3-green.log`, `audit-types-red.log`, `final-full-suite.log`.

## 의도된 제한

- 준비됨 ≠ 실제 제출됨 ≠ 생성 성공 ≠ 동일 목소리/자연스러운 편집/음향. 실제 영상·오디오·최종 연결 QA가 여전히 필요하다.
- client/native 선택 문법과 required 입력은 검사하지만 공급자 내부 conditioning 효과·live 모델 지원/계정 entitlement를 이 검사기로 증명하지 않는다. 실제 모드 지원과 가격/Unlimited는 기존 실행 경로에서 확인한다. 미확인은 제출 전에 차단한다.
- 실제 호출 기록/업로드 선언 자체의 진실성을 자동 인증하거나 다른 MCP 호출을 전역 가로채지 않는다. 코디네이터가 필수 경로를 따라 실제 기록을 저장해야 한다.
- 일반 어댑터가 없거나 현재 native 입력 문법을 입증하지 못한 서비스는 미지원이다. 다른 공급자/모델/TTS/과금을 자동 대체하지 않는다.
- 이번 준비기는 native_reference 인계만 허용한다. 별도 승인된 연속 음향 master/editorial 경로의 자동 실행은 구현하지 않았고 이를 설정만으로 우회할 수 없다.
- 독립 검토 및 fresh-context 행동 시험은 이전 실패 후 사용자가 허용한 생략을 유지했다. 직접 테스트를 독립 검증으로 표기하지 않는다.
- 실제 《내 딸이다》 소스·project.json·채택/거절 상태는 이번 작업의 수정 대상이 아니다. 새 생성/게시·추가 시도 승인도 아니다.
