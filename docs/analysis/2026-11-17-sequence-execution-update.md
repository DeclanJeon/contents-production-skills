# 시퀀스 제작·편집 실행 계층 업데이트 결과

작성일: 2026-11-17

## 반영 범위

사용자가 선택한 접근 A와 직접 구현·테스트 승인에 따라 기존 스킬·정본 계약을 확장했다. 독립 검토는 실패 후 사용자 명시 승인으로 생략했다. 실제 작품의 원장/콘티/원본/생성 작업은 변경하지 않았으며 외부 생성·과금·구매·게시를 하지 않았다. 미디어 시험은 ffmpeg의 합성 패턴/톤만 사용했다.

### 추가 도구

`video-production-assets/scripts/` 아래:

- `sequence_context.py`: 대본 beat/speech/direction과 계획 프레임, 편집 선행·관련 서사 이력, 실제 선택을 연결하는 비정본 조회. 최신 테이크를 자동 채택하지 않는다.
- `validate_sequence.py`: plan/generation/edit/export별 요구/버전/해시/상태/프레임/검사 기록 게이트. 실제 제출 JSON의 문장 대응, 현재 생성 scope, 실제 선행 출구, 필수 사건의 source→final 범위도 검사한다.
- `inspect_sequence_frames.py`: 실제 계획 이미지·선택 source의 첫/마지막 포함 프레임·모션 preview·출력 경계 비교 자료. 검수 전에 자료를 만들 수 있으며 미래의 미생성 테이크 때문에 첫 소스 검사가 막히지 않는다.
- `render_sequence.py`: 검토 기록이 갖춰진 동일 CFR/FPS·해상도·1x 선택 구간을 정밀 트림/hard cut·실제 오디오 레이어로 렌더하고 probe/해시/프레임 계보 manifest를 반환한다. `quality`는 항상 unverified로 반환해 실제 최종 시청/청취와 구분한다.
- 공통 모듈: `sequence_contract.py`, `sequence_media.py`, `sequence_timing.py`.

기존 `update_project.py`는 승인된 edit_plan의 timing_policy/input_versions를 소비하는 제한적 `target_duration_s` 변경과 필요한 `storyboard.rhythm` 교체를 지원한다. 고정 길이/anchor·owner 버전·cue/패널 등 전체 후보 검증·원자 저장·기존 lock 보호를 유지한다.

### 스킬 경로

`creative-production/SKILL.md`와 `video-production-assets/SKILL.md`에 필수 도구 경로를 연결했다. 기준 소유 문서 26/09/11/21/contract와 타임라인→프롬프트 인계에서 `video-production-assets/references/sequence-execution.md`를 읽도록 연결했다. 기존 다른 라우팅 수정은 유지하고 이번에 필요한 짧은 부분만 추가했다.

사용법과 실제 필드 계약은 `../../video-production-assets/references/sequence-execution.md`, 형식 예시는 `../../video-production-assets/assets/sequence-execution-example.json`이다. 예시는 실제 프로젝트/승인/검수 증거가 아니며 비어 있는 승인·소스 필드를 성공 값으로 채우지 않는다.

설치된 `~/.codex/skills/creative-production`, `~/.codex/skills/video-production-assets`가 이 저장소의 해당 디렉터리로 resolve되는 것을 확인했다. 별도 재설치·전역 링크 변경 없이 현재 수정 파일이 노출된다.

## 직접 검증

최종 명령:

```bash
python3 -m pytest video-production-assets/scripts \
  scripts/test_storyline_continuity_gate.py \
  scripts/test_repo_integrity.py \
  scripts/test_routing_table_lint.py \
  -q -p no:cacheprovider --basetemp=<저장소 밖 고유 테스트 폴더>
```

**373 passed, 195 subtests passed (31.33s).** 새 시퀀스 시험은 77개다. 이 결과는 위 관련 suite이며 저장소 전체의 모든 테스트를 실행했다는 뜻이 아니다. 관련 파일의 `git diff --check`도 통과했다.

직접 확인한 핵심 동작:

- 실패하는 시험을 먼저 실행하고 시간/문맥/게이트/미디어/원자 시간 갱신을 구현했다.
- 두 실제 합성 원본에서 48+48프레임을 선택해 24fps/96프레임으로 렌더했고, 출력 전체의 decoded frame MD5 목록이 선택 원본 프레임 목록과 정확히 같았다.
- 같은 시험에서 입력 원본들의 SHA256이 그대로임을 확인했다.
- 실제 CLI에서 context/plan gate/render를 실행하고 기존 출력 덮어쓰기를 거절했다.
- 의미상 필수 사건의 관측 source 구간이 채택 범위 밖이면 거절했다. 이 시험의 관측은 합성 선언이므로 실제 인과 판정의 증거는 아니다.
- 선택 구간을 바꾸면 이전 boundary/event 검사 기록이 무효가 됐다.
- 요구 카메라 명세 누락, 계획 상태를 실제 상태로 재사용, 존재하지 않는 선행 결과, 승인 범위 밖 샷, 계획 이미지 관측 버전 변경을 막았다.
- JSON overflow/잘못된 중첩 메타데이터, 24000/1001 FPS, out-exclusive, 다른 FPS 암묵 변환을 검사했다.
- 고정 시간/공개 anchor 이동, 짧아진 타임라인 밖의 cue를 거절하고 원장 원본 바이트와 lock 정리가 유지됐다.
- 비영점 원본 PTS에서도 선택 오디오가 누락되지 않는 합성 톤·샘플 수 회귀를 통과했다.

시험 과정의 초반 QA 폴더가 사라져 최초 일부 원시 로그는 보존됐다고 주장하지 않는다. 이후 기록은 `.superpowers/sdd/2026-11-17-sequence-to-film-execution/`로 옮겼다. 최종 로그는 `final-verification.log`다. pytest basetemp를 패키지 QA/저장소 내부에 두면 symlink/installer overlap 문제가 생기므로 최종 검증은 저장소 밖 고유 cache 폴더를 사용했다. 중간에 관측한 라우팅 lint 실패는 마지막 실행에서 통과했으며 타 작업 코드를 이번 수정으로 되돌리거나 수정하지 않았다.

## 커밋 분리 검증

이후 사용자가 커밋·푸시를 승인했다. 다른 작업의 로컬 미푸시 커밋 7개와 미커밋 라우팅 변경을 포함하지 않도록 `origin/main`의 `657db90`에서 `feat/sequence-to-film-execution-20261117` 브랜치를 만들고 이번 소유 변경만 분리했다. 공용 coordinator/SKILL에는 이번 시퀀스 실행 경로만 추가하고 다른 라우팅 변경은 가져오지 않았다.

분리된 작업 트리에서 다음을 새로 실행했다:

```bash
python3 -m pytest video-production-assets/scripts \
  scripts/test_storyline_continuity_gate.py \
  -q -p no:cacheprovider --basetemp=<저장소 밖 고유 테스트 폴더>
```

**356 passed, 195 subtests passed (65.78s).** 앞의 373개 실행은 원래 작업 트리에 있던 추가 라우팅/저장소 검사도 포함한 결과다. 그 별도 작업의 검사 파일은 이 브랜치에 포함하지 않았으므로 분리 검증의 개수가 다르다. 이 분리는 원래 main의 작업 파일·브랜치·다른 미푸시 커밋을 변경하거나 되돌리지 않는다.

## 구현 판단과 미검증

- 직접 지정한 저장소에 좁은 패치를 적용했고 브랜치 변경·커밋·리셋·머지·푸시는 하지 않았다. 다른 작업의 dirty 변경을 보존했다.
- 기존 표준 라이브러리/argparse 인터페이스를 유지하고 의존성을 설치하지 않았다.
- 원안의 자동 CFR conform 생성은 이 버전에서 구현하지 않았다. **이미 명시적으로 conform된 CFR·동일 FPS/해상도·1x 입력**만 실행한다. 다른 FPS/VFR/retime은 오류로 막고 별도 승인된 conform/편집 실행 경로와 계보를 요구한다. 디졸브·복잡 합성·NLE round-trip도 자동 실행하지 않는다.
- 새로운 전역 DB/프로젝트 단계 enum/자체 스케줄러를 만들지 않았다. 파생 준비 상태는 실제 지각 품질 인증이 아니다.
- 독립 검토·fresh-context 압박/대조 행동 시험은 **미실시**다. 사용자가 검토 생략 후 직접 구현·테스트를 승인한 사실을 행동 검증 통과로 바꾸지 않았다.
- 실제 영화의 자연스러운 동작·연기·음성·립싱크·장면 리듬을 검증하지 않았다. 코드가 검사 기록의 진위를 인증하지도 않는다. 후속 제작에서 코디네이터가 실제 이미지/영상/소리를 검사하고 실패를 수정해야 한다.
- 따라서 이번 완료는 **기본 실행 계층과 스킬 연결의 업데이트·관련 직접 회귀 검증**이다. 기존 거절/조건부 클립을 채택하거나 영화가 완성됐다는 뜻이 아니다.
