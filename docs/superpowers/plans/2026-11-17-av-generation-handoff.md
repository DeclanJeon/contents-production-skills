# AV Generation Handoff Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 생성 직전 이전 영상·음향의 실제 검수/참조 선택 누락을 막고 검증된 MCP 호출 패킷을 준비·감사한다.
**Architecture:** 기존 generation 게이트에서 새 generation_handoff 모듈을 호출한다. Ludyte native selection 및 검증된 schema-pointer adapter만 허용하며 실제 외부 호출은 코디네이터가 수행한다.
**Tech Stack:** 기존 Python 표준 라이브러리/pytest/argparse, 설치된 ffmpeg/ffprobe. 설치/과금 없음.
**Spec:** ../specs/2026-11-17-av-generation-handoff-design.md

## Global Constraints
- project.json과 기존 enum·권한·검사 진위의 한계를 유지한다.
- 기존 clean feature worktree에서 작업한다. original main의 다른 dirty 변경은 보존한다.
- 실제 영화 파일·MCP 세션/업로드/생성은 변경하지 않는다. capability 조회만 read-only로 허용.
- 직접 구현·테스트와 독립 검토 생략에 대한 기존 사용자 결정을 유지한다.

## Review Focus
- native reference ID와 asset ID 혼동(T2), empty/inherited selection(T2).
- raw tail/잘못된 소스·FPS·변경된 선택 구간(T1/T2).
- 오디오 track 존재와 실제 청취/동일 voice conditioning 혼동(T1/T3).
- 새 앵글의 구도 강제·새 목소리 최초 등장·무음 반례(T1/T3).
- 전역 interceptor/서버 모델 내부 conditioning까지 검증했다는 과장(T3/T4).

### Task 1: 생성 전 AV 요구와 증거
Files: scripts/validate_sequence.py, scripts/generation_handoff.py, scripts/test_generation_handoff.py (video-production-assets 아래).
Interface: validate_generation_handoff(project, projection, root, inspected) -> blocker rows; existing validate_sequence report compatible.
- [x] RED: 이전 audio listening 누락, actual predecessor 임의 면제, 재등장 voice anchor 누락을 재현.
- [x] Implement 실제 선행·AV/voice 요구와 현재 scope의 증거 검사. 첫 샷/무음/첫 목소리는 정확히 분기.
- [x] GREEN: 같은 시험과 기존 generation/plan/edit 회귀.

### Task 2: 실제 wire 참조 검사
Files: scripts/generation_handoff.py, scripts/generation_transport.py, scripts/test_generation_transport.py.
Interface: inspect_transport(project, projection, request, root) -> native binding inspection or SequenceError.
- [x] RED: Ludyte 잘못된 선택 ID·빈 참조·session/revision·pending/candidate/role·업로드 bytes·raw tail 위반.
- [x] Implement 현재 schema·실제 snapshot·등록된 local/native ID 매핑. 일반 어댑터는 검증된 artifact + 실제 schema/JSONPointer 기반으로만 허용.
- [x] GREEN: 정상 수신기록 fixture, unknown/unsupported 경로 fail-closed, 실제 source-derived reference bounds 검증.

### Task 3: prepare / audit CLI
Files: scripts/prepare_generation_request.py, scripts/test_prepare_generation_request.py.
Interface: prepare_request(project, projection, root) -> tool, arguments, request_sha256, submitted=false; audit_call(packet, actual_call) -> comparison report.
- [x] RED: 검사 실패 시 호출 패킷 없음, 실제 호출의 다른 첨부·다른 본문 검출.
- [x] Implement 외부 실행 없는 준비/감사. 정상 재생/청취/conditioning 성공으로 승격하지 않음.
- [x] GREEN: CLI round-trip·원장/파일 불변·비호환 schema 실패.

### Task 4: 스킬 연결·회귀·live 작업 트리 반영
Files: references/sequence-execution.md, references/11-ai-handoff.md, references/29-reference-driven-production.md, docs/analysis/2026-11-17-av-generation-handoff-update.md.
- [x] 실제 구현된 필수 단계와 receipt/role/voice/unsupported 대안 지침을 연결한다. fresh-context 행동 검증은 미실시로 명시한다.
- [x] bare pytest 전체 suite와 CLI/화이트스페이스 검사를 실행하고 실패/범위를 전부 기록한다.
- [x] 검증된 소유 파일만 원래 작업 트리에 동일 base/hash를 확인하며 반영한다. 독립적인 다른 변경은 건드리지 않는다.

Final evidence: feature full suite 939 passed / 4 Windows-only skipped / 533 subtests (55.20s); installed original-source related suite 401 passed / 195 subtests (33.57s). 14 owned files mirrored after four exact-base checks and ten absent-path checks. No new provider job, upload, spending, commit or push; independent/fresh-context review remains waived/unperformed.

Ruling: 기존 요구의 누락 보완에 대한 직접 실행 요청이므로 같은 A 범위 내 설계/계획 질문을 반복하지 않는다. 공급자 직전 참조 기능의 실제 효과 검증은 새 영상 생성 허가 없이 수행하지 않는다.
