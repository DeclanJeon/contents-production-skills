# Matt writing integration — Task 4 offline preparation

상태: **평가 계획·스냅샷·수동 판정 집계의 오프라인 구현/검증 완료. Task 4 전체는 실제 baseline 미실행으로 진행 중**.

이 문서는 [이전 G1 결과](2026-11-11-matt-writing-offline-evaluation.md)의 후속이다. 작업 위치는 `contents-production-skills-matt-writing-craft` worktree이며 원본·전역 설치 스킬은 수정/병합하지 않았다.

## 이번 구현

- `writing_eval_manifest.py`: 입력 14개 × 두 조건 × 5회 = 계획 140건. 다회차를 포함해 사용자 메시지 응답 단계 170회. 반복마다 baseline/candidate 순서를 교차한다. 입력은 실제 접두사·후속 메시지·오너와 함께 해시화하며 루브릭은 모델 입력에서 제외한다.
- `writing_eval_snapshot.py`: 현재 작업 트리의 manifest-listed runtime 파일만 고정 복사한다. QA/테스트/support/숨김 파일을 제외하고 symlink를 거부한다. 복사 중 원본 변경, 이후 파일 추가·변조, snapshot 지문 불일치를 검사한다. manifest symlink는 내용 파싱 전에 거부한다.
- `writing_eval_review.py`: 수동 판정 카드의 증거 경로·해시·run/input ID·snapshot hash·오너 읽기·허용 도구·회차별 final/settled 수를 검사한다. 누락/오류/미검증은 PASS가 아니다. candidate의 각 입력 5회 PASS가 필요하며 baseline의 발견용 FAIL을 candidate 실패로 오판하지 않는다. blocker는 평균으로 상쇄하지 않는다.
- `run_writing_evaluation.py`: `prepare`와 `aggregate` CLI. 기본 모델이나 예산을 지정하지 않고 `live_authorized=false`로 준비한다. 단일 `run_case` API는 명시 승인·입력 일치·fixture 쓰기 승인·snapshot 보존·출력 충돌을 검사하고 외부에서 주입한 backend를 한 번만 호출한다. timeout은 기록하고 자동 재시도하지 않는다.
- 기존 Python 도구의 타입 표기·반환값 처리 정리: 과거 24 warnings에서 **0 errors / 0 warnings**로 개선했다. 진단 억제나 type-ignore/cast 우회는 넣지 않았다.

**실제 모델 제출용 기본 backend나 live batch CLI는 아직 연결하지 않았다.** budget profile의 유효성 검사/기록은 provider의 과금 상한 집행을 검증했다는 뜻이 아니다. 실제 제출 전 선택된 provider/model에 맞는 backend, 호출/토큰/비용 상한·취소/중단 처리와 승인 범위를 확인해야 한다. 임의 backend의 내부 동작이나 비용을 이 API가 보증하지 않는다.

## 실제 dry-run

명령 (worktree 루트):

```bash
python3 scripts/run_writing_evaluation.py prepare \
  .superpowers/sdd/2026-11-11-matt-pocock-writing-craft-integration/dry-run-v1
```

관찰 결과:

- `PLANNED: 140 cases / 170 response stages; live_authorized=false`
- 실제 provider/model: **미선택**. 모델 평가 호출: **0회**.
- baseline runtime 파일: **279개**. QA/기대 답은 snapshot에 넣지 않았다.
- baseline SHA-256: `4fc678fb54e670741df6e0c307abb2796586a5b5bbcce9c610ae748724011fff`.
- candidate snapshot: **없음**. 실제 baseline 실패가 없으므로 보강 후보나 콘텐츠 지침을 먼저 만들지 않았다.
- 준비 후 snapshot 파일 지문을 재검사했다. source snapshot은 파일 해시와 읽기 전용 파일 모드로 고정했으며, 이를 전체 OS 샌드박스와 동일하다고 주장하지 않는다.

[실행 계획 JSON](../../.superpowers/sdd/2026-11-11-matt-pocock-writing-craft-integration/dry-run-v1/run-manifest.json)

## 검증 결과

| 검사 | 실제 결과 | 로그 |
|---|---|---|
| 전체 Python 회귀 | **457 passed / 518 subtests passed** | task-4-full-python.log |
| Node fixture 회귀 | **11 passed** | task-4-full-node.log |
| basedpyright, 새 평가 Python 7개 모듈 | **0 errors / 0 warnings / exit 0** | python-types-next.log |
| Python 규칙 감사, 신규·수정 9개 파일 | **no violations** | task-4-audit.log |
| 패키지 버전 | **2.33 / 22 skills consistent** | task-4-versions.log |
| dry-run CLI | **140/170 PLANNED, live_authorized=false** | dry-run-cli.log |

모든 로그는 [계획 전용 workspace](../../.superpowers/sdd/2026-11-11-matt-pocock-writing-craft-integration/)에 있다. 합성 증거/가짜 backend로 집계기를 검사한 결과이며 모델의 실제 글쓰기 품질·사용자 이해·독립 리뷰 통과가 아니다.

RED→GREEN으로 확인한 경계:

- backend가 TimeoutError를 던져도 증거를 남기고 다음 시도를 자동 실행하지 않는다.
- 마지막 회차가 빠진 다회차 증거를 PASS로 집계하지 않는다.
- baseline FAIL → candidate 5/5 PASS의 대비를 별도로 보고한다. 이미 baseline PASS였던 사례를 개선 성과로 세지 않는다.
- 증거 hash/source/input/run ID 불일치, 경로 탈출, 허용되지 않은 bash 도구를 거부한다.
- null assistant content는 성공한 응답으로 세지 않는다.
- manifest symlink가 private JSON을 가리켜도 파싱 오류에 해당 내용을 노출하지 않는다.

## 원본 변경 대조

복사 기준과 비교해 원본의 기존 파일 **10개 변경**, 신규 파일 **21개 추가**를 확인했다. 관찰된 변경은 한국어 대본 후편집 모듈·그 평가 도구/검증 문서 연결이다. 이 작성자의 도구 변경으로 귀속시키지 않으며 원본을 수정하지 않았다.

- 구조/비트 집필 보강과 표현 후편집은 기능상 구분할 수 있다.
- `03-screenplay.md`, `12-qa.md` 등 연결 파일이 겹친다. 참조 문구 10개만 복사하면 신규 참조·스크립트가 누락될 수 있어 자동 병합하지 않았다.
- 현재 dry baseline은 **기존 고정 worktree 기준이며 최신 원본의 후편집 모듈을 포함하지 않는다**. 실제 평가 전 이 기준을 유지할지 최신 원본을 반영해 새 snapshot을 만들지 결정해야 한다.
- 대조 자료: source-comparison.json, source-added-files.json 및 source-diff-*.patch (위 workspace).

## 다음 게이트

1. 평가 기준 선택: 현재 고정 snapshot / 최신 원본의 후편집 변경을 반영한 새 snapshot.
2. provider/model, 총 비용·호출·토큰 상한, timeout/재시도 상한 확정. 현재 자동 재시도는 허용하지 않는다.
3. 선택된 모델의 실제 제출 backend와 예산 중단 동작 검증 후 baseline 70개 사례 실행·수동 판정.
4. 실제 FAIL에 한해 콘텐츠 집필 참조를 구현하고 candidate 평가. 신규 제작 원장/스키마나 다른 채널 스킬은 추가하지 않는다.
5. 독립 리뷰는 여전히 **미실행/BLOCKED**. 저자의 오프라인 검사로 독립 수락을 대체하지 않는다. 커밋·merge·설치본 동기화·게시도 하지 않았다.
