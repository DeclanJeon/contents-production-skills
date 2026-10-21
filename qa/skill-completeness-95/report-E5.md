# E5 — 01–09 핵심 craft 원문 결속 인계

상태: review 요청. 점수/95% 달성/정식 행동 PASS 주장은 없다. 9개 모듈을 끝까지 직접 읽고 핵심 주장군을 아래와 TSV에 분류했다. 원문 접근 가능성과 직접 읽은 범위는 구별했다. 테스트·빌드·formatter·linter·모델 평가·renderer·provider 작업은 실행하지 않았다.

## 변경 파일 / 고친 결함

소유 모듈 `video-production-assets/references/01-brief.md`부터 `09-edit.md`까지 9개와 `qa/skill-completeness-95/claims-E5.tsv`, 이 보고서만 작성/수정했다. `sources.md`, SKILL.md, templates, metadata, README, CHANGELOG, 통합 ledger/scorecard는 수정하지 않았다. reset/revert/commit, 설치/인증/전역 설정, 업로드/생성/과금/훈련/배포/게시 없음.

- 01: 독자 관점/광고 설득 순서의 정확 Bly 구간을 결속. 광고/설명/드라마의 삼항 병렬표 전체가 책의 직접 분류라는 오독을 차단.
- 02: McKee 가치 단위·인과 대 우연·setup/payoff를 읽고 결속. 기존 §실행 절차 3과 §완료 조건이 비선형/실험 허용 절과 충돌해 모든 사건 배열을 인과 서사로 교정하던 오류를 수정. 인과 서사는 인과 기준, 의도된 우연/단절 형식은 그 의도/탐색 경로로 검토한다. 기능 삭제 없음.
- 03: 행동/반응 비트·서사 씬/시퀀스/막과 subtext 근거 추가. 장소/시간으로 나눈 제작 씬이 McKee의 가치 전환 씬과 같지 않음을 명시. 교육의 직접 설명을 드라마 금지 원칙으로 제거하지 않음.
- 04: 공백 OCR을 실제 읽어 Weston 결과 지시/playable 대안·action verb·listening 미결속 해소. 단순 ‘걷는다’와 상대에게 작용하는 action verb 구별. 한 변수 리허설 기록/사적 경험 보호는 운영 규격으로 좁힘.
- 05: Block 7요소·맥락적 색 의미·수학적 품질 보장 부정의 직접 범위 추가. Williams profile 행동 판독의 좁은 근거 결속. 은유·모든 실루엣/의상 식별 효과는 미결속 유지.
- 06: Katz camera cutting 대 coverage·전체 행동/반응 shot의 tradeoff 결속. Williams storytelling key/contact 계획은 08의 설치 내 근거로 연결. 패널 슬롯 이름·ID·수량은 책의 원래 분류가 아니라 패키지 규격임을 명시.
- 07: Alton 동기 광원/측광/분리, Blender 공식 발광면 크기와 그림자/거리 감쇠, ARRI 공식 유효 확산면/경도/색 매칭/close-up key 위치 구간 추가. spot cone Blend와 물체 그림자 softness 혼동 방지. 거리별 경도 정량 법칙·역방향 전체 매칭은 미결속 유지.
- 08: Williams key/extreme/breakdown, 최초 contact 대 체중 실림, 작은 anticipation, profile 판독을 결속. timing/spacing도 같은 원문을 E5가 직접 재독. 도판/AI 제어/보편 gait 프레임·성별 일반화는 채택하지 않음.
- 09: Pearlman physical/emotional/event는 하나의 리듬을 진단하는 구분으로 결속. Reisz 사전 경고·대사 bridge·counterpoint·음향 체감 속도·중복 소리의 맥락 가치 결속. Foley/청점/침묵·음악 배치 전체를 이 인용으로 인증하지 않음.

새 Acceptance boilerplate를 만들지 않았다. 기존 W4 인용은 삭제/확장하지 않았고, E5가 읽은 판본의 path/hash/bytes/line/read state는 각 설치 모듈의 기존 §근거와 적용 범위에 직접 들어 있다. 06이 05/08, 03이 09를 읽는 링크는 같은 설치 references 디렉터리 안의 근거 절이다. 외부 원본 경로가 없는 사용자 설치에서 원문까지 접근할 수 있다고 주장하지 않는다.

## 원문 직접 읽기 기록

모든 book 원문은 READ-PARTIAL이며 원문 문장/도판을 QA 파일로 복제하지 않았다. 8개 로컬 원문은 PowerShell Get-Item/Get-FileHash 실제 실행으로 bytes/SHA-256을 계산했다(2호출 모두 exit 0). 정확 전체 경로와 값은 `claims-E5.tsv` E5-S01–S18 및 소비 모듈에 있다. 동료의 read state를 E5 읽기로 승격하지 않았다.

| verification_id | 원문 / 실제 읽은 구간 | 지원 / 제한 |
|---|---|---|
| E5-READ-BLY | 광고_상세페이지/md의 Bly L1499–1511, L2494–2512 | 독자 이해/필요, 설득 공식. 실제 광고 반응 수치/설명 영상 일반론 아님 |
| E5-READ-MCKEE | originals/콘텐츠_제작/md McKee L77–89, L95–111, L469–475, L497–505 | 가치 단위, 인과/우연, setup/payoff, subtext. 저자의 정신건강/문화 일반화는 채택하지 않음 |
| E5-READ-WESTON | 같은 md/Weston L49–59, L79–93 | result direction, listening, playable verbs/facts/images/events/tasks. 문자 사이 공백 OCR; 이 구간 인쇄 페이지 번호 없음 |
| E5-READ-BLOCK | 같은 md/Block L31–37 | 7요소·색 의미 맥락·공식적 이미지 보장 부정. W4 거리/대비 구간을 E5가 재독한 것은 아님 |
| E5-READ-KATZ | 같은 md/Katz L389–393 | coverage tradeoff·반응 shot. 도판/축 전체 재독 없음 |
| E5-READ-ALTON | 같은 md/Alton L137–141 | 동기 광원/측광/명암 분리. 현대 조명 규격이나 역방향 전체 매칭 아님 |
| E5-READ-WILLIAMS | 같은 md/Williams L95–99, L137–155, L235–239, L525, L569–579 | timing/spacing, pose/contact, 체중/down, profile, anticipation. L527–533도 탐색 중 읽었으나 지원 근거로 사용하지 않음. 도판 정확 포즈/trajectory 검증 없음 |
| E5-READ-PEARLMAN | 같은 md/Pearlman L227–237 pp83–88 | 3 rhythm 구분/통합, event의 정보/방향 변화. guild 점수표를 패키지에 도입하지 않음 |
| E5-READ-REISZ | 같은 md/Reisz L97–105 pp26–30 | 맥락과 소리, 사전 경고, 반응 위 대사, counterpoint, pace. 모든 소리 기능 입증 아님 |
| E5-READ-BLENDER | https://docs.blender.org/manual/en/latest/render/lights/light_object.html — Point/Spot Radius, Beam Shape, Area Light | 직접 reader 텍스트, 2026-10-17; 페이지는 Blender 5.2 LTS로 표시. 로컬 설치 버전/renderer 실행 아님 |
| E5-READ-ARRI | https://www.arri.com/resource/blob/83996/409091c612f371b0c68b41d9dcb636db/arri-lighting-handbook-english-data.pdf — ©2016 Fourth Edition pp5–8,10–17 | 공식 PDF 텍스트 직접 읽음, 2026-10-17. 확산면·경도·색/close-up key·경계. 도판/홍보 성능 수치 채택 안 함 |

웹 자료는 read 도구 rendition을 직접 읽었으나 고정 로컬 파일을 만들지 않아 hash/bytes=`N/A-live-web`이다. 로컬 해시가 있는 증거처럼 집계하면 안 된다. 검색 결과의 초기 ARRI URL(resource/blob/127830/...)은 404였고, 공식 handbook landing page를 직접 열어 현 링크(resource/blob/83996/...)로 복구했다. 검색 답변의 ‘reverse match’ 요약은 원문 근거로 사용하지 않았다.

## 전체 모듈 핵심 주장군 coverage

이는 핵심 주장군별 감사다. 단순 제목 수/인용 수를 완료 점수로 환산하지 않는다. 아래 표의 보존된 W4 근거는 W4 소유의 좁은 범위이며 E5 직접 읽기와 다르다. TSV 36행 = source-derived 18 + authored-design 9 + unsupported 9; 뒤 두 군은 군별 추적이며 원자적 모든 문장 인증이 아니다.

| 모듈 | 실제 읽은 전체 절 | 직접 결속 | 운영 설계 / 잔여 외부 craft |
|---|---|---|---|
| 01 | 입력/절차/스타일/개발/완료/근거/템플릿/심화 | E5-S01; 드라마는 04 경유 | E5-A01 가정/버전/선택/권한; E5-U01 설명 삼항·개발 용어 전체 |
| 02 | 입력/절차/개발 문서/완료/근거/템플릿/심화 | E5-S02,S03 가치·인과·회수 | A02 문서/ID/소유; U02 내적 필요·아크/막·여정 비교·모티프 전체 |
| 03 | 입력/절차/단위/완료/근거/템플릿/심화 | S04,S05; sound 중복은 S18 | A03 시간/claim/수정; U03 외부 포맷/문서 용어 전체 |
| 04 | 입력/절차1–8/완료/근거/템플릿/심화 | S06–S08 Weston; W4 Hooks 보존 | A04 관찰/권리/변수 기록; U04 AI 적용 품질·hold 큐 실제 효과 |
| 05 | 입력/절차1–6/완료/근거/템플릿/심화 | S09,S10; W4 대비/거리 보존 | A05 룩/출력 검수; U05 은유·모든 식별/원근 효과 |
| 06 | 절차1–11/POV 인계 전체/네 산출물/완료/근거/템플릿/전문·심화 | S11 coverage, 08의 S15 키/접촉, 05의 S10 판독 | A06 ID/phase/상태/라우팅. U06 축(W4 support만)·동작/portal/inset/반응 사다리 등 특수 staging 효과 전체 |
| 07 | 절차1–7/하이라이트/완료/근거/템플릿 | S12–S14 동기/크기/색·경계 | A07 목표/실측/cue/AI 상태; U07 거리 경도 정량·reverse 전체/반사 띠 정확 재현 |
| 08 | 절차1–6/완료/근거/템플릿/심화/모션 그래픽 표·규칙1–5 | S15,S16 pose/contact/weight/anticipation/timing | A08 FPS/실행 상태·레이어 인계; U08 관절/행동선/립싱크/모션 그래픽 효과/앱 등가 전체 |
| 09 | 절차/종료/완료/근거/템플릿/배속/압축/큐/오디오 의도/권리/후반 단계/심화/소리 기능 전체 | S17,S18 rhythm/sound; W4 Murch 보존 | A09 시간/ID/권리/승인/상태/QC. U09 나머지 개별 소리 효과·실제 playback/청취 |

외부 craft 잔여를 authored-design으로 일괄 변경하지 않았다. 명백한 book-derived 표현은 근거 미결속으로 남겼다. W4-U04의 지정 Weston 결함은 결속했지만 실제 연기 효과까지 검증한 것은 아니다. 다른 W4-U01–U09는 해당 claim군의 일부를 해소했고 TSV의 좁은 residual이 남는다. 접근 불가 사용자 입력 blocker로 보고하지 않는다.

## 실제 검증과 제한

E5-CLI-01: `python -X utf8 qa/skill-completeness-95/run_cases.py --help` 실제 실행, exit 0. 출력에 `--manifest`, `--run-dir`, `--case`(S1a/S1b, V-01–V-28 포함), `--model`과 ‘Execution success is never an automatic PASS.’ 확인. help만 실행했다. 정식 평가·모델 실행·모듈 준수의 smoke 통과가 아니다.

원문 파일 지문 산출 2회 exit 0 외에 테스트/빌드/렌더/미디어 재생은 없다. 의미 있는 행동 수정(02 비인과 경계)은 아래 부모의 fresh-session 시나리오로 검증해야 하며 현재 NOT RUN이다. 원문 읽기만으로 exercised verification rubric gate를 충족했다고 보지 않는다. 기존 사용자 변경 내용은 보존했다.

## 부모 통합 명령 / 실패시 볼 기준

아래는 실행하지 않은 명령이다. runner 인터페이스만 위 help로 확인했다. output run-dir는 이 worker가 만들지 않았다.

```text
python -X utf8 qa/skill-completeness-95/run_cases.py --manifest qa/skill-completeness-95/case-manifest.json --run-dir qa/skill-completeness-95/runs/E5-integration --case S1a
python -X utf8 qa/skill-completeness-95/run_cases.py --manifest qa/skill-completeness-95/case-manifest.json --run-dir qa/skill-completeness-95/runs/E5-integration --case S1b
python -X utf8 qa/skill-completeness-95/run_cases.py --manifest qa/skill-completeness-95/case-manifest.json --run-dir qa/skill-completeness-95/runs/E5-integration --case M-03
python -X utf8 qa/skill-completeness-95/run_cases.py --manifest qa/skill-completeness-95/case-manifest.json --run-dir qa/skill-completeness-95/runs/E5-integration --case V-01
python -X utf8 qa/skill-completeness-95/run_cases.py --manifest qa/skill-completeness-95/case-manifest.json --run-dir qa/skill-completeness-95/runs/E5-integration --case V-02
python -X utf8 qa/skill-completeness-95/run_cases.py --manifest qa/skill-completeness-95/case-manifest.json --run-dir qa/skill-completeness-95/runs/E5-integration --case V-03
python -X utf8 qa/skill-completeness-95/run_cases.py --manifest qa/skill-completeness-95/case-manifest.json --run-dir qa/skill-completeness-95/runs/E5-integration --case V-04
python -X utf8 qa/skill-completeness-95/run_cases.py --manifest qa/skill-completeness-95/case-manifest.json --run-dir qa/skill-completeness-95/runs/E5-integration --case V-05
python -X utf8 qa/skill-completeness-95/run_cases.py --manifest qa/skill-completeness-95/case-manifest.json --run-dir qa/skill-completeness-95/runs/E5-integration --case V-06
python -X utf8 qa/skill-completeness-95/run_cases.py --manifest qa/skill-completeness-95/case-manifest.json --run-dir qa/skill-completeness-95/runs/E5-integration --case V-07
python -X utf8 qa/skill-completeness-95/run_cases.py --manifest qa/skill-completeness-95/case-manifest.json --run-dir qa/skill-completeness-95/runs/E5-integration --case V-08
python -X utf8 qa/skill-completeness-95/run_cases.py --manifest qa/skill-completeness-95/case-manifest.json --run-dir qa/skill-completeness-95/runs/E5-integration --case V-09
python -X utf8 scripts/check_versions.py
python -X utf8 -m pytest -q
```

별도 정상/경계 smoke 입력과 기대(모두 NOT RUN):

1. **인과 정상**: ‘인과 드라마. 주인공이 경고를 숨겨 사고가 나고 이를 공개한다. 비트 인과/가치 변화만 검토.’ → 원인/선택/결과 연결, 상반된 가치·정보 변화 식별. runtime 보장이나 새 인물 사실을 만들지 않음.
2. **비인과 경계**: ‘실험 콜라주. 서로 원인 없는 도시 조각, 반복 색이 점차 바뀌며 결말 인물 선택은 없음. 02로 구조만 검토.’ → 선택한 단절과 색 변화/탐색 규칙을 검토하고 결말을 인물 선택/강제 갈등으로 고치지 않음.
3. **Weston**: ‘더 슬프게라는 지시를 playable 대안·듣기 비트로 바꾸고 출처 제시.’ → 상대에게 무엇을 하는지와 자극/응답 구별; ‘걷는다’만 action verb라고 답하거나 개인 트라우마를 요구하면 실패.
4. **contact**: ‘발꿈치가 막 닿은 포즈와 체중이 실린 down이 같다.’ → Williams L151 대 L235–239를 구별; 도판 검사/보편 FPS/AI 제어 보장하면 실패.
5. **light**: ‘spot Blend를 올리면 물체 그림자도 무조건 부드러워지는가?’ → beam edge와 object shadow 구별; 광원 유효 면/거리/실제 검수 구별. reverse 전체 보장하면 실패.
6. **sound**: ‘반응 샷 위 대사와 Foley 재질 표현 둘 다 읽은 Reisz 구간으로 입증.’ → 전자는 좁은 support, 후자는 아직 개별 미결속임을 밝힘. 전체 소리 기능 인증하면 실패.

## 소유권 요청

- W4/리더: `sources.md`에 E5-S01–S18의 정확 판본/구간을 기존 관례로 통합 요청. 웹 두 건은 고정 local hash가 없는 상태를 유지. 잔여 E5-U01–U09를 지우거나 모두 source-derived로 승격하지 말 것.
- 리더: README/CHANGELOG/version 및 combined ledger/state는 소유자 통합. 독립 리뷰에서 원문/consumer claim을 대조하고 미검증/미결속 modifier를 실제 범위에 적용. 전권을 안 읽었다는 이유로 무관한 모듈 전체를 일괄 판정하지 않되 남은 load-bearing 미결속을 숨기지 말 것.
- R: 5점 판단은 actual fresh-session verification과 지원 범위를 확인한 뒤 수행. 이 보고서는 점수 승인이 아니다.
