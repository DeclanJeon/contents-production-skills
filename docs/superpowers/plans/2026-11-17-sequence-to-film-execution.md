# Sequence-to-film execution Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 기존 제작 스킬에서 대본 요구·계획 프레임·실제 채택 구간·최종 출력의 연결을 실행 가능한 도구로 검증하고 편집한다.

**Architecture:** 기존 project.json을 정본으로 유지한다. sequence-execution/1 파생 문맥을 읽기 전용으로 구성하고 단계별 구조·증거 게이트와 프레임 추출/편집 어댑터가 소비한다. 의미 관찰·수정 결정은 코디네이터가 맡고 실제 미디어 검사 없이 품질을 통과시키지 않는다.

**Tech Stack:** 기존 Python 3/pytest/argparse·표준 라이브러리 관례, 설치된 ffmpeg/ffprobe, 기존 이미지 도구의 Pillow. 새 의존성 설치 없음.

**Spec:** ../specs/2026-11-17-sequence-to-film-execution-design.md

## Global Constraints
- project.json 정본, schema_version=1.1, 기존 artifact/attempt/check enum 유지.
- 원본/기존 출력/타 작업 dirty 파일 보존. 실제 작품·공급자 호출·과금·게시·Git 커밋/브랜치 전환 없음.
- 0-based 정수 프레임과 [in,out), FPS는 Fraction. planned는 관측 증거가 아니다.
- 사용자 승인: A 방식, 유연 길이 정책, 직접 구현·테스트. 독립 검토 생략은 사용자 명시 승인으로 기록한다. 새 subagent를 실행하지 않는다.
- 비정본 payload와 코드의 구조·기술 시험은 실제 지각·스킬 준수 행동 시험의 대체물이 아니다. 그 미검증 범위는 완료 보고에 명시한다.

## Review Focus
- 잘못된/빈 JSON·bool 시간·중복 ID·NaN·경로 탈출은 동작 전에 거절한다(Tasks 1–3).
- 오래된 선택 구간/해시와 부모 실패 꼬리는 후속 준비 상태가 될 수 없다(Tasks 2–3).
- 요청 FPS와 실제 출력이 다르거나 컷 프레임이 한 장 어긋나면 기술 시험이 실패해야 한다(Task 4).
- 음향 핸들·무음 정책·혼합 원본은 새 stem을 발명하거나 대사를 잘라 숨기지 않는다(Tasks 3–4).
- 시간 변경은 고정 anchor/연결 cue·패널·원장 버전과 함께 원자적으로 검사한다(Task 5).

---

### Task 1: 시간·파일·파생 형식 경계
**Files:** Create scripts/sequence_contract.py and test_sequence_contract.py under video-production-assets/.
**Interfaces:** SequenceError(code, locator, detail); FrameSpan(start,end); frame_at(seconds,fps); project_file(root,path); read_projection(path); checked_assets(project,root,ids).
- [x] Test: 반개구간·Fraction 변환·bool/NaN/소스 초과·루트 탈출·해시 변경·잘못된 JSON 입력을 검사한다.
- [x] Run pytest test_sequence_contract.py; 신규 모듈 부재로 RED를 확인한다.
- [x] Implement 표준 라이브러리 타입/명시적 오류·프로젝트 루트 파일 검증·형식 파싱.
- [x] Run 같은 시험; GREEN을 기록한다.

### Task 2: 시퀀스 문맥과 실제 선행 인계
**Files:** Create scripts/sequence_context.py, test_sequence_context.py.
**Interfaces:** build_sequence_context(project, shot_ids, projection=None) -> JSON document; CLI project --shot ID [--projection FILE].
- [x] Test: 두 샷 중 후행 조회가 편집 선행·관련 서사 이력·패널/초→프레임과 시도 기록을 포함하고 최신 raw를 선택하지 않는다. 빈/알 수 없는 범위·서사 순환을 거절한다.
- [x] Run 신규 시험 RED, implement 읽기 전용 projection/bootstrap와 scope closure.
- [x] Run GREEN 및 기존 test_project_handoff.py.

### Task 3: 생성 전부터 출력까지 준비/증거 검사
**Files:** Create scripts/validate_sequence.py, test_validate_sequence.py.
**Interfaces:** validate_sequence(project, projection, phase, base_dir=None) -> report with ready/blockers/checks/aesthetics; CLI --phase plan|generation|edit|export.
- [x] Test: 요구 누락·계획 이미지 미검사·상태 충돌·허용 변화·이력/버전/선택 출구 변경·실제 증거 없는 pass·실행 승인 없음·원테이크 내부 컷·고정 anchor 이동을 각각 막는다.
- [x] Run RED; implement 단계별 게이트와 실제 source/출력 파일·인접 모션/정속/청취 증거 요구.
- [x] Run GREEN. 검사 ready는 지각 품질 인증/실행 허가가 아님을 JSON에서 구분한다.

### Task 4: 프레임 비교 자료와 실제 편집 어댑터
**Files:** Create scripts/sequence_media.py, inspect_sequence_frames.py, render_sequence.py, test_sequence_media.py.
**Interfaces:** probe_media(path); render_sequence(project, projection, root, output); inspect_sequence_frames(project, projection, root, output, mode).
- [x] Test: 설치된 ffmpeg로 소스 2개와 오디오 펄스를 만들어 hard cut 후 정확한 24fps/프레임 수·경계 소스·원본 불변을 검사한다. 출력 덮어쓰기/해시 차이/미지원 전환/다른 FPS의 암묵 conform/무음 위반은 거절한다.
- [x] Run RED; implement bounded subprocess, project-root confinement, 재인코딩 trim, 명시 출력 설정·음향 레이어, 새 디렉터리 출력과 probe/lineage 증거.
- [x] plan 모드에서는 실제 패널 비교 자료만, source/export 모드에서는 정확한 프레임/인접 클립과 매핑을 만든다. 생성이나 지각 pass를 주장하지 않는다.
- [x] Run GREEN, CLI --help와 실제 subprocess 오류 경로도 검사한다.

### Task 5: 유연 타임라인 원자 승격
**Files:** Modify scripts/update_project.py; Create scripts/sequence_timing.py, test_sequence_timing.py.
**Interfaces:** validate_timing_change(current, candidate, delta) -> None or SequenceError; existing prepare_update/apply_update 반환 호환 유지.
- [x] Test: target_duration_s 변경은 현재 approved edit_plan의 timing_policy와 input_versions 없으면 실패한다. 고정 길이/anchor·cue 초과·패널 초과는 거절하고 원장은 불변이다. 유효한 전부 갱신은 성공한다.
- [x] Run RED; narrow allowlist에 target_duration_s·storyboard.rhythm 추가, 승인된 정책/anchor/연관 시간과 owner version을 검사한다.
- [x] Run GREEN 및 기존 updater/storyboard suite.

### Task 6: 스킬 실행 경로·참조·예시 연결
**Files:** Add references/sequence-execution.md와 assets/sequence-execution-example.json; Modify creative-production/SKILL.md의 짧은 기존 연속성 경로 및 소유 참조 26/09/11/21/contract/storyboard-timing-to-prompt.
**Interfaces:** 실제 구현된 CLI 경로·형식만 문서화. 정상화/의미 관찰은 agent 책임으로 명시한다.
- [x] 실제 기계 소비 예제의 plan→문제 발견→수정→edit→render 경로를 시험한다. 기존 참조/라우팅 회귀를 실행한다.
- [x] 확인된 도구 공백에 한해 사용법/실행 순서를 연결하고 가상의 자동 의미 감지·스킬 준수 행동 검증을 주장하지 않는다.
- [x] 사용자 승인에 따라 독립 검토는 생략. fresh-context 행동 검증은 미실시로 명시한다.

### Task 7: 통합·회귀·완료 보고
**Files:** qa/sequence-execution-v01/PROGRESS.md and VERIFICATION.md; design status update.
- [x] 신규 시험·기존 video-production-assets/scripts·storyline/route 구조 시험을 실행하고 결과를 기록한다.
- [x] 문서 예제를 CLI로 실행하고 실패/성공 경계·실제 렌더 frame lineage를 확인한다.
- [x] 자가 검토 후 중요한 결함은 회귀 RED→GREEN으로 수정한다.
- [x] 변경 파일·통과/미실시·원본 불변·기존 dirty 보존을 보고한다. 실제 작품의 품질 성공과 혼동하지 않는다.

## Execution rulings
- 사용자가 재차 직접 구현을 승인했으므로 별도 계획 승인 질문을 반복하지 않고 inline으로 진행한다.
- 지정 저장소의 동시 dirty 변경을 보존하기 위해 브랜치 전환·Git 작업 없이 좁은 파일 패치로 통합한다. 새 모듈을 우선하고 기존 dirty SKILL.md는 필요한 짧은 문구만 교체한다.
- 외부 독립 검토/에이전트 행동 실험은 사용자 승인에 따라 실행하지 않는다. 자가 검토·도구 실행 시험과 이를 구분해 보고한다.
