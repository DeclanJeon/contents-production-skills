# 문서 소비자 사전 QA — gap 근거 인계 시점

## 범위와 판정

최종 DESIGN 합격 판정이 아니다. 현재 게시된 chapter·method에서 **다른 문서 소비자가 잘못 재집계/해석할 수 있는 모순**을 찾았다. 진행 중이라는 이유만의 PARTIAL 항목이나 청취 미수행 자체를 실패로 나열하지 않는다. 아래는 발견/수정 제안을 보존한 원장이며 peer 소유 파일은 수정하지 않았다. 담당자가 고치면 이 항목 ID를 유지하고 재검수 결과를 붙이는 것이 좋다.

- 담당 30 source: V025–V048 및 V005/V013/V014/V016/V023/V024. 나머지 게시 18장에 대해 identity/Markdown 대상 링크를 기계 대조했다. 18장의 모든 시각 판단을 재관찰한 것은 아니다.
- 직접 재독: analysis-method, V002, V012, V015의 관련 절; V001/V003/V004/V006/V007/V008 등의 mode/endpoint 문구; 담당 V048의 마지막 block/count 문구. 기존 chapter 줄 번호는 이 스냅샷의 locator다.
- 18장에 실린 `sha256:` archive ID와 inventory의 archive_id 대조: 불일치 0. 실제 Markdown 링크의 로컬 target 존재 대조: 누락 0. 이는 이미지 내용·시각 관찰 정확성·권리·오디오 검증이 아니다.

## 발견 원장

|ID / 심각도|재현되는 실제 근거|소비자 실패|수정 제안과 재검수|
|---|---|---|---|
|PF01 / MEDIUM · 수량/자료 버전|`videos/V012-ferrari-spec-commercial.md:5`는 25 candidate-neighborhood sheets 및 **26 grouped windows / 28 raw events**, `:22`는 26 groups를 검토했다고 적으나 C01–C25만 나열한다. 실제 `evidence/V012/candidate-neighborhoods.json`의 `group_centers_and_neighborhood_frame_pts[].candidate_group` 고유값은 **25**, `sheets`는 **13**, raw events는 **28**이다.|group·sheet·raw 이벤트를 섞어 26번째 해석 단위가 빠졌다고 오판하거나 구 배치 시트와 현재 manifest를 같은 자료라고 읽는다. source 컷 26개가 검증되었다고 재집계할 위험도 있다.|현재 JSON 배치 기준으로 숫자를 정정하거나, 25개 구 배치 시트를 실제 검토했다면 배치/locator를 별도로 명시한다. 현재 75개 frame record는 25×3이지 75 group이 아니다. `unique(candidate_group)`, `len(sheets)`, raw count, chapter C ID 집합을 동시에 대조하고 실제 cut 수와 분리한다.|
|PF02 / LOW · 담당 chapter의 stale count|`videos/V048-visual-evidence.md:41`의 “후보26과블록28” 문구와 실제 표 `:11–37`의 B01–B27이 다르다. 마지막 `:37` B27은 검정 tail이며 `n680 PTS28.361667`의 최종 검토 locator를 갖는다.|근거 장을 집계하면 28번째 block이 없는 문서로 보인다. 영화 shot이나 source duration과 block 수를 혼동할 가능성이 생긴다.|문구의 block을 27로 고치고 후보 26/관찰 block 27/실제 cuts UNKNOWN을 분리한다. 표 ID 마지막/고유 count와 summary/coverage를 재대조한다. 이 발견은 이전 담당 문서의 오류도 숨기지 않은 기록이다.|
|PF03 / LOW · CTA 텍스트 certainty 충돌|`videos/V002-im8-surreal-product-film.md:28`은 원본 50.8s read에서 `IM8HEALTH.COM`을 읽었다고 명시하지만 `:61`은 website-like text를 “not transcribed”라고 한다.|이미 판독한 엔드카드 텍스트가 UNKNOWN으로 되돌아가 copy/CTA 분석에서 빠진다. 반대로 URL이 보였다는 것을 유효/공식 링크 인증으로 오해할 수 있다.|C34에도 화면 판독 `IM8HEALTH.COM`을 적고 **링크 유효성/캠페인 권리/저자 인증 미확인**만 유지한다. endpoint locator와 C34의 동일 텍스트를 대조하되 50.8 requested seconds를 native last-frame PTS로 인증하지 않는다.|
|PF04 / MEDIUM · mode ledger stale|`videos/V006-musinsa-rain-boot-male-secret.md:7`은 ASR 미사용이라고 하지만 `evidence/V006/asr-hypotheses.json`에는 `faster-whisper small CPU int8 local_files_only=True` 실행 정보, language `ko`, probability 0.9929991960525513 및 segment 2개가 저장돼 있다. V001 `:6`도 “No … ASR”인데 저장 ASR 결과 파일이 존재한다. V007 `:7`의 ASR UNKNOWN도 실행 상태와 가설 내용의 UNKNOWN을 구분할 필요가 있다.|이미 접근한 텍스트 mode를 실행되지 않은 것으로 보고 다시 조사하거나 오디오 가용성 조사 자체를 누락했다고 오판한다. 파일이 있다는 이유로 실청취/확정 대사로 바꾸는 반대 오류도 가능하다.|mode는 `ASR_RUN / HYPOTHESIS_UNVERIFIED`, V001/V007의 segment 0개는 `NO_SEGMENTS_RETURNED` 등으로 내용 부재를 표시한다. V006의 결과를 말소하지 말고 원본 파일/방법/구간과 검증 미수행을 연결한다. listening은 계속 UNKNOWN/NOT_PERFORMED, 음악/SFX/mix/입싱크는 이 결과로 판정하지 않는다. |
|PF05 / MEDIUM · 수치의 certainty 분류|`analysis-method.md:8`은 ESTIMATED를 “measurement/candidate boundary”라고 묶는다. 담당 native frame의 PTS와 ffprobe duration/timebase는 직접 저장된 측정 값이며, 그 주변 컷/phase 경계는 추정치다.|기계에서 읽은 source PTS를 근사 requested second로 오인하거나, 후보 시점을 실제 cut-frame 계측값으로 승격한다. 단일 ESTIMATED 표기로 두 오류를 검출하기 어렵다.|OBSERVED metadata/source-frame measurement와 ESTIMATED boundary bracket를 구분해 정의한다. 후보 score event는 `DETECTOR_CANDIDATE`이며 native PTS는 provenance locator다. 예시 한 행에 requested_s/actual_source_pts/boundary bracket를 같이 설명하고 실제 source tick와 대조한다. 새 촬영값·lens 측정값을 채우라는 뜻이 아니다.|
|PF06 / MEDIUM · 절차 목표/달성 상태|`analysis-method.md:11`은 verified edit cuts에서 SH###로 분리하고 “every boundary is checked”라고 규정한다. 실제 장들은 C/B candidate·관찰 block과 G/SG 해석 그룹을 사용하며, sample 사이 exact cut이나 continuous motion 미검증을 명시한다. 예: V003 `:6–7,18`, V012 `:5,22`, V048 `:7–9,41`.|method를 현재 패키지의 완료 보증으로 읽으면 B/C를 실제 shots로 재집계하고 48 source의 모든 cuts와 행동 phase가 검증되었다고 잘못 주장한다. 각 장의 정직한 한계와 상위 method가 충돌한다.|현재 제공 mode에서는 B/C/G가 무엇인지 공통 legend를 추가하고 SH###는 **source-boundary verified일 때만 부여하는 규칙/추후 검증 목표**로 표시한다. 전체 source의 컷 완전성이 아니라 전체 길이 표본+모든 검출 후보 검토라고 범위를 명시한다. ID hierarchy를 일괄 자동 변환하지 말고 각 source의 경계 확인/UNKNOWN 상태를 유지한다.|

### PF01 자료 스냅샷

`evidence/V012/candidate-neighborhoods.json`의 SHA-256: `1fa87acfe233da52b9d626c20698a3c434a895e66563be661c068d85e2ed6497`. 고유 group 25 / sheet entries 13 / raw candidates 28. 이후 새 자료가 생성되면 이 hash의 발견을 새 자료에 그대로 적용하지 말고 해당 필드와 chapter count를 다시 대조한다. 기존 구 배치 이미지의 보존 자체는 문제로 판정하지 않았고 지우지 않았다.

### PF02 해결 기록 — 담당 문서의 bounded repair

- **RESOLVED:** 원 발견 PF02 행은 보존했다. `videos/V048-visual-evidence.md:41`의 stale “블록28”을 실제 **관찰 블록 27개(B01–B27)**로 수정하고, 검출 후보 26개와 모두 실제 컷 수가 아니라는 제한을 명시했다.
- 실제 표 locator: `videos/V048-visual-evidence.md:11–37`의 B01–B27; 마지막 행 `:37`은 검정 tail과 native `n680 PTS28.361667 / strip-05 cell12`를 가리킨다.
- coverage 대조: `evidence/repo-worker-coverage-merge.json`의 `sources[id=V048].visual_blocks=27`, `block_ids=B01…B27`, `scene_candidates_count=26`, `last_source_frame.frame_n=680 / pts_s=28.361667`. 원장이 이미 올바르므로 수정하지 않았다.
- PF01 및 PF03–PF06의 main 소유 문서는 변경하지 않았다. 이 해결은 최종 DESIGN의 reader-QA 합격 판정이 아니다.

## 이번 gap 문서의 자체 구조 체크

`gap-evidence-fast.md`는 30 source / 70 mechanism 행, PRESENT 30 / PARTIAL 36 / EVIDENCE_INSUFFICIENT 4. 실제 각 장의 B/S.P 행과 교차 대조: 없는 ID 0; 각 행의 chapter/native-evidence target: 없는 경로 0. baseline 기록 집합 295개 SHA 재대조: 변경 0. clause alias는 실제 재독한 경로/줄 지도와 연결하며 source별 매출/주목/바이럴/촬영 파이프라인의 인증은 제공하지 않는다.

## 최종 DESIGN 독립 reader-QA에서 확인할 통과 조건

1. source caption/업로더 선언, observed frame, 제작 해석, 새 proposal controls, 실제 실행 결과가 구분되는가. remaster와 100% 생성, affiliate 장비와 실제 촬영 장비, track credit와 음악 권리가 특히 분리되는가.
2. 기존 25의 archive/mode/메커니즘 chain, 19의 제품·재질, 07의 광원, 04의 목표/받기, 09의 sound/time 계약, 26의 누적 state를 누락 능력으로 제안하지 않는가.
3. proposed mechanism마다 실제 source B/phase와 새 승인 assets·불변·행동/정보 변화·handoff·실패 검수를 찾을 수 있는가. 예쁜 look이라는 말만 있거나 WHY가 관찰 문장의 자동 반복이면 실패다.
4. 기존 참조의 심화와 새 전문 스킬 필요성을 구별하는가. 정확 수치/3D camera proof·endpoint 지원·sound mix 검증이 없는데 구현·합격으로 부르는가.
5. book 근거는 실제 본문 줄/앵커이고 OCR 빈 파일·역사적 광고 효과·주관적 가중치를 현재 보편 법칙으로 가져오지 않는가. 공식 기술 웹의 사실도 원본 영상 실제 제작법을 증명하지 않는가.
6. 숫자/ID/링크는 한 집계 기준으로 읽히고, full decode/frame sample을 continuous playback/listening/all-cut certification으로 부르지 않는가.

프로덕션 코드/기존 스킬/설정 수정·빌드·생성·설치·외부 업로드는 하지 않았다. 최종 DESIGN의 독립 시각/문서 검수는 아직 수행했다고 보고하지 않는다.
