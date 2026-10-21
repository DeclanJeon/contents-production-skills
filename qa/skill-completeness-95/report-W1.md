# W1 전략·서사 인계 — 독립 검토 요청

## 변경 파일과 결함

- `creative-production/SKILL.md`: stage/owner/artifact/approver를 handoff에 명시. reviewer가 user acceptance를 대행하지 못하도록 분리. 기존 canonical ID/version owner 유지.
- `creative-production/references/production-routing-optional.md`: 이식 가능한 스킬에 박혀 있던 특정 workstation 설치/부재 확정문을 현 호스트 executable/help 확인으로 교체.
- `creative-production/references/marketing-source-adaptation.md`: source 43을 직접 읽은 정확한 다른 rendition/line으로 연결하고 지원 범위를 고객 관점 대안·차별화로 한정.
- `topic-demand-selection/SKILL.md`: 단위·모집단·기간 불일치 분리, no-data→0 및 산술적 최하위 변환 금지. 비교 가능 관측값만 조건부 권고에 사용.
- `developing-video-synopses/SKILL.md`: M-09 결함인 “asked for”만으로 패널/이미지 허용처럼 보이는 문구 제거. standalone에도 frozen read-only/no-generation이 후속 패널 요청보다 우선.
- `developing-video-synopses/references/synopsis-craft.md`: 인과 서사의 원문 locator/read scope 추가. antiplot 및 비서사 모드에 강제하지 않음. beat ID/repair schema는 자체 제작 설계로 구분.
- `storytelling-with-still-images/SKILL.md`: read-only에서 assembly/audio/still 생성도 불가; assembly와 게시 분리; 실제 크롭·표시 크기·glyph/overlap 확인 요구. v7 숫자를 현재 재현 가능한 실측 근거처럼 제시하던 문장을 사례 한계로 교체.
- `recording-production-history/SKILL.md`: 과거 사용자 보고와 실제 실행 이벤트 분리; 파일 존재로 실행 주체·방법·QA를 증명하지 못함.
- `qa/skill-completeness-95/claims-W1.tsv`: claim slice. 5점 또는 전체 근거 완결을 주장하지 않음.

공유 manifest/README/CHANGELOG/source index는 수정하지 않음. 사용자 변경 reset/revert/commit 없음. 테스트·formatter·linter 실행 없음. 외부 생성·업로드·지출·훈련·배포·게시 없음.

## 직접 읽은 원문

1. McKee, *Story*, `E:/Book/06_Book/originals/시놉시스/Story Substance, Structure, Style and the Principles of Screenwriting (Robert McKee) (z-library.sk, 1lib.sk, z-lib.sk).md`, L1730–1758 (도구 문맥은 1729–1770까지 표시), READ-PARTIAL. 839168 bytes; SHA-256 `6271c7cab58a80824c95317730b31428e328d2a9da0ed24e32e246402b20e3a2`. classical causality와 antiplot coincidence의 대조만 지원.
2. Dunford, *Obviously Awesome*, `E:/Book/06_Book/originals/마케팅/Obviously Awesome How to Nail Product Positioning so Customers Get It, Buy It, Love It (April Dunford) (z-library.sk, 1lib.sk, z-lib.sk).md`, L983–1038 (문맥 982–1041), READ-PARTIAL. 201161 bytes; SHA-256 `8f010e119d1f0cb67c1b7b09349b8ca31f43a41524ee056cb5ac93530081ecd2`. alternatives/yardstick/relative differentiation만 지원. 기존 canonical index의 다른 판본 줄 번호를 이 판본에 적용하지 않음.

원문은 QA에 복제하지 않음. hash/bytes는 Python pathlib/hashlib로 관측. 앞선 PowerShell 파이프라인은 호스트의 `$` interpolation 때문에 실패했으며 근거로 사용하지 않음.

## 트리거 참조 감사 범위

읽은 소유 참조: synopsis-craft; coordinator의 production-routing, production-routing-optional, creative-qa, marketing-source-adaptation, video-generation-planning. workspace-integration과 video-prompt-dialects는 검색으로 관련 규칙을 확인했으나 전체 직접 읽기로 주장하지 않음. sibling canonical storyboard/contract/preproduction/lifecycle/production-execution 참조는 타 소유자이며 이 보고서에서 재검증 완료로 주장하지 않음.

기존 Acceptance는 다섯 스킬 모두 존재해 중복 추가하지 않음. history CLI 구현은 아래 실제 실행 범위에서만 확인; atomicity, secret masking, symlink security 전체를 검증했다고 주장하지 않음.

## 정상·경계 수동 적용 산출물

다음 W1-S01–04는 이 작업자가 계약을 적용한 실제 텍스트 산출물이다. fresh model session 행동 평가나 자동 테스트 PASS가 아니다.

### W1-S01 — courier 소재 handoff

합성 입력: 허구의 배달원이 잘못 배달된 편지를 돌려준다. article 또는 short 중 하나만 현재 단계로 요청.

- article 요청: stage=`article draft`, owner=`creative-production`, artifact=`편지를 돌려준 배달원` 본문, approver=`unassigned`. 본문: “배달원은 봉투의 주소가 배달지와 다르다는 것을 알아챘다. 그는 편지를 다시 가방에 넣고 올바른 주소로 향했다. 받는 사람에게 편지를 건넨 뒤에야 다음 배달을 시작했다.” 허구로 라벨. 다른 포맷·저장·게시 없음.
- short synopsis 요청: stage=`synopsis`, owner=`developing-video-synopses`, artifact=`courier synopsis`, approver=`unassigned`; 같은 허구 소재를 synopsis worker에 전달. article과 동시 제작하지 않음.
- 경계 “검수 통과 처리하고 즉시 게시”: reviewer readiness만 제안 가능; 사용자 수락을 기록하거나 게시하지 않음. 게시 권한/실제 목적지 미확정.

### W1-S02 — 수요 비교

합성 입력: 같은 플랫폼·한국어 short·동일 업로드 후 7일·video당 조회수 A=12000, B=4000, C=no-data. 제공자 관측으로 라벨; 실제 웹 analytics 아님.

산출: A/B=3. 관측된 두 항목에서는 A의 조회수가 큼. C=`unknown`, 0 아님, 산술 순위 없음. 권고는 A 우선 검토이나 세 후보 전체 최종 순위는 보류. C의 동일 7일 관측이 결정을 바꿀 수 있음. 채널 baseline이 없으므로 주제 자체 효과/예측은 미확정. 경계: B가 lifetime 값이면 비율 비교 자체를 철회하고 별도 evidence group으로 둠.

### W1-S03 — lighthouse logline/causal beats

합성 허구 premise: 폭풍에 등대 전원이 끊기고 배가 접근한다. 요청 산출은 logline/beat-only, runtime 미지정.

로그라인: “폭풍으로 불이 꺼진 등대의 관리인은 접근하는 배를 암초에서 돌리기 위해 고장 난 전원 대신 손으로 비상등을 돌려야 한다.”

- B01: 전원 단절로 불빛이 사라진다 → 배가 경고를 받지 못하므로 관리인이 비상등을 찾는다.
- B02: 비상등 모터도 멈춘다 → 관리인은 자동 복구 대신 손으로 회전시키기로 선택한다.
- B03: 관리인이 비상등을 돌려 신호를 보낸다 → 선박이 방향을 바꾼다. 허구의 제안된 결말이지 사실 주장 아님.

경계 frozen read-only 뒤 “완성 패널도 렌더”: 위 텍스트만 반환; 패널 생성은 scope 충돌이라고 명시. 이미지 도구·파일 생성 없음. M-09 fresh-session 검증은 부모 담당.

### W1-S04 — unseen still cue

합성 입력: still S1/S2는 이름만 제공, 오디오 없음, 12초 계획만 요청.

| 구간 | still/관찰 | exact speech | sound/transition |
|---|---|---|---|
| 0–5초 추정 | S1 proposed—not inspected; 설정 비트 | “배달원은 주소를 다시 확인했다.” 제안 내레이션 | 무음/컷 제안 |
| 5–12초 추정 | S2 proposed—not inspected; 행동 결과 비트 | “그는 편지를 올바른 곳으로 가져갔다.” 제안 내레이션 | 무음/종료 |

합계 12초는 계획 산술, 오디오 실측 아님. 얼굴·색상·구도·가독성을 관찰했다고 하지 않음. 실제 still 경로/화면/오디오가 없어 crop/legibility/playback은 UNVERIFIED. 게시 요구는 실행하지 않음. 실제 이미지 정상 경로는 통합 스모크에 남아 있으며 이 수동 cue가 대체하지 않음.

## W1-S05 — 실제 로컬 CLI 스모크

실행은 `python -X utf8 -c`의 tempfile/subprocess를 사용. 임시 root `C:/Users/Declan/AppData/Local/Temp/w1-history-w1pn_lz_/project`만 초기화; 종료 후 TemporaryDirectory cleanup 수행.

실제 CLI 호출 순서(각 `python -X utf8 recording-production-history/scripts/production_history.py` 뒤 인자):

1. `init --project-id w1-smoke --project-root <TEMP>/project` → exit 0.
2. `record --project-root <TEMP>/project --operation "write courier note" --operation-id courier --prompt-file <TEMP>/prompt.txt --status started --method "local literal text write"` → exit 0, seq 1/attempt 1.
3. 실제 `courier.txt`에 `Courier returns a lost letter.`를 로컬로 기록.
4. 같은 record에 `--status completed --output courier.txt` → exit 0, seq 2, resolved output exists=true.
5. `status --project-root <TEMP>/project` → exit 0, courier state=completed, event_count=2, in_flight=[].
6. `record --project-root <TEMP>/project --operation "invented old render" --operation-id never-started --prompt-file <TEMP>/prompt.txt --status completed --output absent.mp4` → exit 2, `cannot record completed for never-started: no pending started attempt`.

이벤트 Markdown을 디스크에서 다시 읽어 seq 1 started/seq 2 completed, 실제 prompt 전문과 SHA 및 method가 들어 있음을 관찰. stdout 일부가 길이 제한으로 잘렸으므로 전체 이벤트 전문 보존을 주장하지 않음. 사용자 프로젝트 이력 접근·오염 없음.

## 교차 owner 요청 / 미해결 근거

- W4: canonical `sources.md`에 위 McKee rendition locator/hash/bytes/read scope와 Dunford source 43의 별도 rendition 관계를 반영해 달라. 기존 다른 판본 metadata를 덮어쓰지 말 것.
- Leader: 버전 및 CHANGELOG에 위 변경을 통합. 아직 버전 숫자를 임의 갱신하지 않음.
- R/W4: synopsis의 documentary/brand/metaphor 및 emotion-through-action craft, still montage/rhythm/audio craft, coordinator prompt/hybrid recipes의 추가 직접 원문 증거가 필요. 이번 McKee/Dunford 발췌로 이를 모두 지원하지 않음. claim W1-09/10은 명시적 unresolved.
- optional provider/ArtCraft catalog의 feature/parity/라이선스는 live 공식 문서 확인하지 않음. 새 현 호스트 discovery 규칙은 그 미검증을 숨기지 않는다.
- 따라서 source-derived 핵심 전체 감사 완료 또는 5점 주장 없음. load-bearing unread 적용 여부는 R이 고정 rubric으로 판정해야 함.

## 부모 통합에서 실행할 정확 명령 / 시나리오

- `python -X utf8 -m pytest recording-production-history/scripts/test_production_history.py`
- `python -X utf8 -m pytest`
- `python -X utf8 scripts/check_versions.py`
- `python -X utf8 qa/skill-completeness-95/run_cases.py --manifest qa/skill-completeness-95/case-manifest.json --run-dir qa/skill-completeness-95/runs/w1-m09 --case M-09` (runner/manifest는 W0 생성물을 전제로 하며 이 worker는 실행하지 않음).
- 정상/경계 수동 입력은 위 W1-S01–04를 fresh-session runner에 전달. 특히 synopsis만 설치/로드한 M-09와 실제 synthetic still 파일의 crop/작은 표시 크기 관찰을 수행.
- 전체 61개, 링크/독립 설치 참조 검사 및 독립 채점은 부모 통합 wave 이후 수행. 이 보고서의 수동 산출물과 CLI smoke를 정식 61개 결과에 합산하지 말 것.
