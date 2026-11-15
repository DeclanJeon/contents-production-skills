---
name: silent-satire-animatic
version: 1.0
description: Design and review silent (no dialogue, no narration, no captions) satirical animatics built from popular source material, from source selection through script, scene/cut and beat-budgeted timeline. Use for 무성 애니메이션, 대사 없는 애니메이틱, 풍자 애니메이션 기획, silent satire shorts or longform under ten minutes, or judging whether an existing silent edit will hold attention. Excludes actual rendering, publishing, and paid generation.
---

# Silent Satire Animatic

무성(無聲) 풍자 애니메틱의 제작 계약. "무성"은 **인간 발화의 부재**를 뜻하며 소리의 부재가 아니다.

## 경계

| 다룸 | 다루지 않음 |
|---|---|
| 무성 원칙과 판정 | 실제 렌더 실행 |
| 풍자 서사 구조 | 유튜브 게시 |
| 소재 선별 기준 | LLM 이미지/영상 프롬프트 생성 |
| 비트 예산 계산 | 음성/TTS 생성 |
| 썸네일 프레임 선택 | 저작권 법률 판단 |

## 언제 쓰는가

- "무성 애니메이션 만들어줘" / "대사 없는 애니메틱"
- 인기 소재를 풍자하는 콘텐츠 기획
- 기존 무성 편집물이 시선을 붙잡을지 검토
- 10분 미만 애니메틱의 비트/컷 배분

## 무성 원칙 (P1~P6)

정본은 `references/01-silent-principles.md`다. 요약:

| # | 원칙 | 강제 |
|---|---|---|
| P1 | 첫 3초에 상황이 읽힌다 | 첫 비트는 `notice`, ≤3.0초, 인물+문제 오브젝트 동시 등장, 로고/타이틀 컷으로 시작 금지 |
| P2 | 무성은 대사의 부재 | BGM/SFX/비언어 음 허용. TTS·내레이션·대사·자막·말풍선 금지 |
| P3 | 반복 강화 → 펀치라인 | 동일 동작 3회 이상 반복, 매 회차 변주 축 1개 이상 증가, 이후 펀치라인 필수 |
| P4 | 비트는 8초를 넘지 않는다 | 단일 비트 ≤8.0초, 평균 4~6초 |
| P5 | 썸네일은 가장 강한 프레임 | 0초 캡처 금지, 펀치라인의 가독 샷(wide/medium), 본편과 동일 종횡비, 실패 시 릴리스 중단 |
| P6 | 10분 미만 + 완결 | 총 ≤600초, 마지막 비트는 `land`(해소) |

## 제작 순서 (6단계)

```
소재 선택 → 대본 → 씬/컷 → 타임라인 → 렌더 → 게이트/배포
```

각 단계는 검증 가능한 산출물을 남긴다. 상위 단계 실패 시 하위로 진행하지 않는다.

### 1. 소재 선택

인기 규모를 실제 지표로 확인한 소재만 쓴다. 원칙:

- 조회수와 길이를 **실측 지표**로 검증 (추정·추측 금지)
- 원본 미디어는 다운로드하지 않는다. 제목·지표·길이만 사용
- 풍자 대상은 **행동/현상**을 추출한다. 원본 재현이 아니다
- 후보 0건이면 제작하지 않고 `NO_SOURCE`로 종료

### 2. 대본

4막 구조 (`setup → escalate → punchline → resolve`). 정본은 `references/02-satire-structure.md`.

- `silent: true`, `dialogue: []`, `captions: []` 를 구조적으로 강제
- 첫 비트 `notice`, 마지막 비트 `land`
- 결정적(deterministic) 조립을 우선한다. 같은 소재 → 같은 대본
- LLM 대본을 쓸 경우 재현 불가를 명시하고 시드를 고정한다

### 3. 씬/컷

- 컷 1개 = 동작 1개 = 연속 구간
- 같은 동작이 반복되면 변주 축(`speed`/`obstacles`/`scale`/`direction`) 중 하나 이상이 증가
- `direction` 은 증가 축이 아니라 **토글 축**이다. 단조성 검사에서 제외한다
- 카메라 샷은 `wide`/`medium`/`close`/`whip`, 팔로우는 `static`/`track`/`whip`

### 4. 타임라인

정본은 `references/03-beat-budget.md`.

- 총 길이 ≤600초
- 비트 경계는 프레임에 정렬
- 비트 수는 **90~120**
- 40~60비트로는 600초를 채울 수 없다 (비트당 10~15초가 되어 P4 위반)

### 5. 렌더

이 스킬의 범위 밖이다. 호출자는 다음을 요구받는다:

- 관절 articulation 증거 (영수증)
- 썸네일 해상도·샷 검증
- 중간 산출물 정리 정책

### 6. 게이트/배포

- 자동 공개 금지. `publication_ready=false` 로 렌더하고 검수 후 전환
- 중간 산출물은 게시 + 드라이브 저장 확인 **후** 삭제

## 비트 예산 계산

```
비트 수 = 총 길이 ÷ 평균 비트 길이
제약: 평균 비트 길이 ≤ 8초 (P4)
      비트 수 90~120

600초 ÷ 6초 = 100비트   (권장)
400초 ÷ 5초 =  80비트   (최소 미달 → 90으로 올림)
```

비트 수를 먼저 정하고 길이를 맞추지 말 것. **길이가 먼저, 비트 수가 결과**다.

## 변주 축

5개 기본 동작(`notice`/`run`/`trip`/`dive`/`land`)만으로 600초를 채우면 같은 장면이 120회 이상 반복된다. 변주 축이 이를 막는다.

| 축 | 범위 | 시각 효과 |
|---|---|---|
| `speed` | 1.0~3.0 | 위상 압축, 빠른 동작 |
| `obstacles` | 0~5 | 장애물 개수 증가 |
| `scale` | 0.6~1.6 | 인물 크기 |
| `direction` | ±1 | 진행 방향 반전 (토글) |

**상한 주의**: 샷 배율 × 변주 배율이 곱해진다. `close`(2.2) × `scale`(1.6) = 3.5배면 인물이 화면에서 잘린다. 결합 배율을 2.0으로 상한하는 것을 권한다.

## 썸네일

정본은 `references/04-thumbnail-selection.md`.

- 펀치라인 비트의 **wide 또는 medium** 샷에서 캡처 (클로즈업 금지 — 상황이 안 읽힘)
- 본편과 동일 종횡비, 배포 해상도
- 캡처 실패는 **치명적**. 무시하고 진행하지 않는다
- 대상 0초 프레임(오프닝 포즈)은 가장 약한 프레임이다

## BGM

무성이므로 BGM이 유일한 청각 안내다.

- 라이선스 검증된 풀에서 선택하되, 부재/부적합 시 **합성 폴백**
- 저작자 표시 필요 곡은 쓰지 않는다 (설명란에 표기할 자리가 없다)
- 폴백 사유를 기록한다. 조용히 넘어가지 않는다
- 폴백 판정은 기계적이어야 한다: 풀 없음 / 적격 없음 / 파일 불가 / 길이 판독 실패 / 30초 미만

## 안티패턴

| 안티패턴 | 문제 |
|---|---|
| 자막으로 상황 설명 | 무성 원칙 위반. P2 |
| 클로즈업 썸네일 | 상황이 안 읽혀 CTR 하락. P5 |
| 40~60비트로 10분 | 비트당 10~15초 → 지루함. P4 위반 |
| 변주 없는 반복 | "고장난 영상"으로 보임. P3 |
| 원본 영상 재촬영 | 저작권 위험. 풍자 대상은 행동이지 장면이 아니다 |
| BGM 크롤링 자동화 | Content ID 청구 위험. 로컬 검증 풀을 쓴다 |
| 썸네일 실패 무시 | 배포 불가 산출물이 통과됨 |

## 검증 체크리스트

- [ ] `silent: true`, `dialogue == []`, `captions == []`
- [ ] 첫 비트 `notice` ≤3초
- [ ] 마지막 비트 `land`
- [ ] 총 길이 ≤600초
- [ ] 비트 수 90~120
- [ ] 단일 비트 ≤8초
- [ ] 동일 동작 3회 이상 + 변주 증가
- [ ] 관절 articulation 증거 통과
- [ ] 썸네일 펀치라인 프레임, 정확한 종횡비
- [ ] BGM 폴백 사유 기록 (폴백 시)

## 참조

- `references/01-silent-principles.md` — P1~P6 상세
- `references/02-satire-structure.md` — 풍자 서사 문법
- `references/03-beat-budget.md` — 초/비트 계산
- `references/04-thumbnail-selection.md` — 프레임 선택 규칙

## 관련 스킬

- `topic-demand-selection` — 소재의 수요 검증
- `storytelling-with-still-images` — 정지 이미지 기반 무성 편집
- `higgsfield-youtube-thumbnail` — 썸네일 제작 실행
- `video-production-assets` — 일반 영상 제작 총괄
