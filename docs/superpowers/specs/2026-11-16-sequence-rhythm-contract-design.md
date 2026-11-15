# 시퀀스 리듬 계약(Sequence Rhythm Contract) 설계

**날짜:** 2026-11-16
**상태:** 승인 대기 (v2.40 후보)
**범위:** `video-production-assets`(참조 5종·템플릿 2종·검증기·신규 측정 스크립트), `storyboarding-video` 포인터 1문장, `silent-satire-animatic` 상호참조 1문장, 패키지 버전·체인지로그.

---

## 1. 배경 및 문제 진단

### 1.1 사용자 관찰

개별 생성 클립의 퀄리티는 수용 가능하지만, 이어붙인 결과가 평평하고 늘어진다(② 유형). v2.36의 kinetic staging은 **정지 키프레임의 역동성**(① 유형)을 다루므로 이 증상의 원인이 아니다.

### 1.2 패키지 진단

리듬은 여러 문서에 걸쳐 있으나, **설계 도구가 없고 금지 규정만 있다.**

| 위치 | 현재 문안 | 결과 |
|---|---|---|
| `storyboard-contract.md` §장면 리듬 5 | "무빙/컷 수·샷 크기 비율·일정 초 간격을 품질 기준으로 쓰지 않는다" | 리듬 설계를 수치로 잡을 수단이 없음 |
| `storyboard-contract.md` §씬 카메라 수락 검사 7 | "의도적인 정지·균등 템포·반복은 그 자체로 실패가 아니다" | 균등 템포를 선언·검증할 자리가 없음 |
| `assets/09-edit-template.md` | 컷 표 12열에 `행동·카메라 변화 / 컷아웃→컷인 phase·state + cue time / 컷 이유`가 **이미 있다**(컷별 사실 기록) | 컷별 기록은 충분하나 **구간 요약·계획 길이·실측 대조**가 없어 시퀀스 기울기를 볼 수 없음 |
| `assets/06-shots-template.md` | 씬 리듬 열은 서술형("축적·변화·쉼"), 샷 표에 `핸들` 열이 **이미 있다** | 결손은 필드가 아니라 **곡선(구간 집계)** 이며, 핸들은 샷 단위로만 존재해 리듬 요구와 연결되지 않음 |

> 즉 이 설계는 **없는 필드를 채우는 일이 아니라, 이미 흩어져 있는 컷별 사실을 곡선 수준으로 집계하고 측정과 연결하는 일**이다. 새 사실 필드를 만들지 않으며, 같은 값을 두 번 타이핑하지 않는다(§4.2 우선순위).
| `08-animation.md` | "모든 동작에 큰 예비동작을 강제하지 않는다" | 방어적. 대체 설계 없음 |
| `12-qa.md` | 리듬이 요청 기준이면 완성 시퀀스로 검사 | **검사 대상 기준선이 없다** (무엇과 대조할지 미정의) |

패키지 전체에서 `에너지/템포/페이싱/비트 예산` 어휘는 각 문서 2~4회 수준이고, `unverified/강제하지 않는다/미검증` 가드가 압도적이다. 즉 **"틀리지 않게" 만드는 장치는 두껍고 "세게" 만드는 장치는 얇다.**

### 1.3 외부 코퍼스 진단 (사용자 수집 시트, 130장)

사용자가 2026-09-26~11-15 수집한 AI 영상 프롬프트 시트(Google Sheets `1hhHW1d-JCKo4WYeU0wVb_LqJmZuzcCFNqBL2meghPmw`)를 전수 파싱해 확인한 사실:

1. **균일 리듬 공장:** 프롬프트 400행 중 **300행(75%)이 정확히 3샷 카드**(`S01 establish / S02 action / S03 hold`). 19개 시트의 샷 구간 1,730개 실측 분포는 **평균 4.65초, 표준편차 2.36, 2.5초 이하 15.1%, 6초 이상 29.0%**.
2. **평가표에 리듬 항목 없음:** 100점 배점 9항목 중 리듬·에너지·동세는 `시간축·동작 15점`("관찰 가능한 동작과 인과적 진행이 있는가") 하나뿐. 밋밋해도 100점이 나온다.

**따라서 코퍼스는 리듬 처방의 출처가 될 수 없다.** 다만 (a) 3샷 균등 분할은 **반패턴 증거**로, (b) 1,730개 구간 분포는 **참조 분포(목표 아님)** 로만 채택한다.

### 1.4 해석 원칙 (이 설계의 핵심)

기존 금지 규정은 *"보편 리듬 공식을 합격 기준으로 쓰지 않는다"*는 뜻이고, 이는 유지한다. 이번 설계가 더하는 것은 **선언된 의도(declared intent)의 자기 일관성 검사**다.

- **금지 유지:** 실제 컷 길이가 "4.65초 평균에 가까운가" 같은 외부 표준 대조 → 하지 않는다.
- **신규 요구:** 보드가 리듬 곡선을 **선언하면**, 검사 대상은 ① 선언 내부의 모순(비트 누락·길이 합 불일치·에너지 순서 충돌), ② 선언과 실제 편집본의 차이다. 둘 다 **자기 대조**이므로 보편 공식화가 아니다.
- **균등 템포:** 여전히 실패가 아니다. 다만 리듬이 리뷰 항목일 때 **선언 없이 균등**하면 관찰(observation)로 보고한다. 판정 어휘는 `PASS / PASS_WITH_NOTES / NEEDS_REVISION / UNVERIFIED`를 유지하고 곡선 불일치는 NOTES로만 기록한다.

새 문서 문안(v2.36의 소유 경계 관행에 맞춰 명시):

> §장면 리듬 5 개정: "무빙/컷 수·샷 크기 비율·일정 초 간격을 **보편 품질 기준**으로 쓰지 않는다. 보드가 `storyboard.rhythm`을 선언한 경우 검사 대상은 선언과 계획·실측의 **자기 일관성**이며, 외부 표준과의 일치는 검사하지 않는다. 선언이 없으면 기존 규칙 그대로다."

> 수락 검사 7 개정: "동일 크기·길이·구도·무빙의 반복은 기능과 중요한 비트의 가독성으로 판단한다. **의도적 균등 템포는 `cadence: steady`와 사유를 곡선에 적으면 그대로 통과한다.** 선언 없이 균등한 경우도 실패는 아니지만, 리듬 리뷰에서는 `observation: 균등 템포`로 1회 보고한다."

---

## 2. 목표 / 비목표 / 안티골

### 목표

1. **설계 시점(A):** 시퀀스 리듬 곡선을 설계 산출물로 만든다 — 비트별 에너지·케이던스 의도·계획 길이·컷 이탈 phase·사유.
2. **검증 시점(C):** 조립된 컷(또는 명시 컷 목록)에서 실제 컷 길이를 측정해 선언 곡선과 대조하고, 최소 수정 지점을 보고한다.
3. 두 산출물이 **같은 어휘**(energy 1–5 / cadence enum / cut_out_phase enum)를 쓰도록 `06`(설계)과 `09`(검증)의 소유를 분리한다.
4. 컷 온 액션의 **물리적 전제**인 클립 핸들을 곡선에서 도출해 생성 인계에 요구한다.
5. 기존 픽스처·검증기·테스트를 깨지 않는다(옵트인, 하위 호환).

### 비목표

- ① 유형(한 클립 안의 모션 캡처·"밋밋한 클립 자체")의 프롬프트·모델 문법 이식. 코퍼스의 브래킷 카메라 토큰·생체역학 동작 체인·모델/모드 매트릭스는 **다음 사이클 후보**로 남긴다.
- 시트의 100점 평가표 개정, 새 점수·순위·합격 임계값 도입.
- 음악 비트 자동 검출·정렬, 자동 리듬 최적화, 생성 재시도 자동 트리거.
- `silent-satire-animatic`의 비트 예산 로직 변경(참조만 한다).

### 안티골 (기술적으로 동작해도 실패)

- 리듬 곡선을 모든 프로젝트의 필수 입력으로 만든다 → 옵트인 위반.
- `measure_cut_rhythm.py` 결과를 합격/불합격으로 쓰게 만든다 → 판정 오염.
- 미디어 없이 "리듬 검증 완료"를 선언할 수 있게 만든다.
- 곡선 표가 늘어 컨텍스트에서 창작 문장이 밀려난다(v2.36이 걷어낸 문제의 재발).

### 제약

- `validate_storyboard.py`의 기존 계약(구조 검증만, 미학 판정 금지)과 `--require-images`/`--strict-staging` 관행을 따른다.
- 판정 어휘·`UNVERIFIED` 규율·`[BASIS-UNSTATED]` 표기 관행을 그대로 쓴다.
- 모든 수치는 `DESIGN_PROPOSAL`이거나 출처 표기 대상이며, 렌더 검증으로 승격하지 않는다.

---

## 3. 접근 비교와 채택

| 안 | 내용 | 장점 | 기각/채택 이유 |
|---|---|---|---|
| **A. 시퀀스 리듬 계약** | 곡선 설계 + 필드·검증기 | 원하는 리듬이 설계물로 존재하고 조립까지 살아남음 | **채택** |
| **B. 템포 대비 계약** | 금지 패턴 + 숫자 기본값만 | 가볍고 평평함을 직접 때림 | 단독 기각: 규칙을 지켜도 리듬이 안 생기는 경우를 못 잡고, 숫자가 곧 공식이 되어 패키지 원칙과 충돌. **A의 "기본값(비합격기준)"으로 흡수** |
| **C. 조립 후 리듬 진단** | 측정 → 평평함 지표 → 최소 수정 | 진짜 문제 지점, 미디어 근거 | 단독 기각: 다음 프로젝트에 남는 자산이 없고, 설계 시점에 리듬을 못 만든다. **A와 결합** |

**채택: A + C 최소 조합.** 설계 시점에 곡선과 컷 길이 근거를 만들고(A), 조립 후 측정해 곡선과 대조(C). B의 수치는 A 안의 기본값으로만 쓰고 합격 기준으로 쓰지 않는다.

---

## 4. 설계

### 4.1 스키마 — `storyboard.rhythm` (옵트인)

`project.json`의 `storyboard` 확장 객체에 선택 필드로 추가한다. 없으면 기존과 완전히 동일하게 동작한다.

```json
"storyboard": {
  "rhythm": {
    "intent": "2연타 가속 → 브레이크 → 정점 → 여운",
    "curve": [
      {
        "id": "RB01",
        "beat_ids": ["B01", "B02"],
        "shot_ids": ["SH01", "SH02"],
        "energy": 2,
        "cadence": "steady",
        "planned_duration_s": 4.25,
        "cut_out_phase": "settle",
        "exit_handle_frames": 0,
        "reason": "관객이 거리와 위협을 먼저 읽는다. 다음 세그먼트의 가속을 위해 길게 둔다."
      }
    ]
  }
}
```

| 필드 | 형식 | 의미 |
|---|---|---|
| `intent` | 비공백 문자열 | 곡선 전체의 한 줄 의도. 곡선 판독의 기준점 |
| `curve[]` | 비어 있지 않은 배열 | 시퀀스 구간(보통 3~8개). **샷 1개가 아니라 리듬 구간 1개** |
| `curve[].id` | 고유 비공백 문자열 | `RB01` 형식 권장 |
| `curve[].beat_ids` | 비어 있지 않은 배열 | `storyboard.beats` 참조. 비트 커버리지 검사 대상 |
| `curve[].shot_ids` | 비어 있지 않은 배열 | `shots` 참조. 타임라인 순서 검사 대상 |
| `curve[].energy` | 정수 1–5 | 1=정적·정보 전달, 3=표준 진행, 5=정점·충돌. 절대 척도가 아니라 **이 프로젝트 안의 상대값** |
| `curve[].cadence` | `steady`\|`accelerando`\|`ritardando`\|`brake`\|`peak`\|`release` | 다음 구간으로 넘어가는 템포 의도 |
| `curve[].planned_duration_s` | 양의 유한수 | 이 구간의 계획 길이. 커버 샷 길이 합과 대조된다 |
| `curve[].cut_out_phase` | `pre_action`\|`mid_action`\|`impact`\|`reaction`\|`settle` | 이 구간을 **어느 동작 국면에서 떠나는가**. 컷 온 액션의 위치 계약 |
| `curve[].exit_handle_frames` | 0 이상 정수 | `cut_out_phase`를 확보한 뒤 남겨둘 여유 프레임. 생성 인계의 핸들 요구로 전달 |
| `curve[].reason` | 비공백 문자열 | 이 길이·에너지인 이유. 사후 검토의 유일한 근거 |

### 4.2 소유 경계 (오탐 방지)

**우선순위 규칙(두 출처 충돌 방지):**

- **사실값**(실측 시각, 실제 핸들 용량, 실제 클립 상태)은 `09` 컷 표·`asset_registry`·클립이 정본이다. 곡선은 사실을 주장하지 않는다.
- **계획 의도**(에너지·케이던스·계획 길이·컷 이탈 국면)는 `storyboard.rhythm`이 정본이다.
- 따라서 `09`의 `컷아웃→컷인 phase·state + cue time`은 **컷별 실행 기록**, 곡선의 `cut_out_phase`는 **구간 요약 의도**이며, 검증기는 둘을 대조하지 않는다(자유 서술이라 기계 대조 불가). 문서 간 같은 숫자를 두 번 입력하지 않는다.

| 문서 | 소유 범위 | `rhythm` 취급 |
|---|---|---|
| `storyboard-contract.md` §8 | 스키마 선언 | **정본** — `storyboard.rhythm`의 소속·필드·필수 여부 선언 |
| `storyboard-contract.md` §장면 리듬 | 해석 원칙 | **정본** — §1.4 개정 문안 |
| `assets/06-shots-template.md` | 설계 출력 양식 | **정본** — 곡선 표(설계) |
| `assets/09-edit-template.md` | 검증 출력 양식 | **정본** — 계획 vs 실측 대조 표 |
| `references/09-edit.md` | 리듬 실행 절차·기본값 | **정본** — 곡선 문법, 기본값, 측정 경로 |
| `references/06-shots.md` | 컷 설계 원칙 | 비소유 — 에너지 배분·길이 배분 원칙과 cross-ref만 |
| `references/12-qa.md` | QA 라우팅 | 비소유 — 측정 경로 1줄 |
| `references/11-ai-handoff.md` | 생성 인계 | 비소유 — 핸들 도출 규칙 1문단 |
| `scripts/validate_storyboard.py` | 구조 검증 | 곡선 **구조·커버리지·합계·순서**만. 미학·리듬 품질 판정 금지 |
| `scripts/measure_cut_rhythm.py` | 실측·대조 | **정본** — 측정·차이·관찰만. 판정 금지 |

> 검증 시 주의: `06-shots.md`에 `rhythm` 필드가 없다는 사실을 결함으로 보고하지 않는다. 스키마 완결성은 `storyboard-contract §8` + 템플릿 2종 + 검증기 정합으로만 판정한다.

### 4.3 검증기 확장 — `validate_storyboard.py`

동작 규칙:

1. `storyboard.rhythm`이 **없으면** 아무것도 바뀌지 않는다(기존 픽스처·테스트 무영향).
2. **있으면** 항상 구조 검증: `intent` 비공백, `curve` 비어 있지 않음, 각 항목의 id 고유·`beat_ids`/`shot_ids` 실존·`energy` 1..5 정수·`cadence`/`cut_out_phase` enum·`planned_duration_s` > 0·`exit_handle_frames` ≥ 0 정수·`reason` 비공백.
3. **있으면** 항상 커버리지 검증:
   - 모든 shot이 **정확히 1회** 커버된다. 미커버 shot은 `SH03: rhythm curve does not cover this shot` error.
   - 모든 beat는 **1회 이상** 커버된다(정확히 1회가 아니다). 한 비트가 여러 샷·여러 구간에 걸치는 것은 `storyboard-contract.md` §8과 `test_same_beat_in_multiple_shots_allowed`가 이미 허용하므로 계약 충돌을 만들지 않는다.
   - 각 항목의 `beat_ids`는 **자기 `shot_ids`들의 beat 합집합의 부분집합**이어야 한다(`RB01: beat B02 is not among its shots` error). 반대 방향(샷이 쓰는 beat가 어느 구간에도 없음)은 위 커버리지 규칙으로 이미 잡힌다.
4. **있으면** 항상 순서 검증: 각 항목의 커버 샷이 타임라인(`start_s`) 오름차순이고, 항목 간 순서도 겹치지 않는다.
5. **있으면** 항상 합계 검증: `|planned_duration_s − Σ(end_s − start_s)| ≤ max(1/fps, 0.05)`.
6. **있으면** 핸들 선언 하한: `cut_out_phase ∈ {mid_action, impact}`이면 `exit_handle_frames ≥ 2`(프레임 정렬·1프레임 미세 조정 여유). 그 외 phase는 제약 없음. 이 하한은 **그 구간의 `shot_ids` 마지막 샷**(컷이 실제로 발생하는 샷)에 적용된다.
7. `--strict-rhythm` 추가: 리듬 객체 **존재 자체를 요구**한다. `--strict-staging`과 동일한 옵트인 관행이며 기본값은 off.
8. 검증기는 **에너지 곡선의 단조·다양성·품질을 판정하지 않는다.** 실측 대조는 §4.7 측정 보고서 몫이다. 검증기는 `source_duration_s`로 계산되는 **실제 핸들 용량**도 대조하지 않는다(§4.7 `handle_shortfalls`).

### 4.4 설계 문법 — `06-shots-template.md` 곡선 표

기존 "씬별 카메라 의도와 리듬" 표 아래에 **소형 표 하나**를 추가한다(권장 최대 8행 — 컨텍스트 억제).

| rhythm_id | beat / shot | energy (1–5) | cadence | 계획 길이 (s) | cut_out_phase · handle(f) | 이 길이·에너지인 이유 |
|---|---|---|---|---|---|---|
| RB01 | B01 / SH01 | 2 | steady | 4.25 | settle · 0 | 거리와 위협을 먼저 읽힌다 |

표 상단 주석: *"곡선은 선언된 의도다. 외부 표준과의 일치를 검사하지 않는다. 균등 템포를 의도하면 `cadence: steady`와 사유를 적는다."*

곡선 작성 순서(문서에 4단계로 명시):

1. 시퀀스의 정점(클라이맥스·충돌·펀치라인)을 먼저 하나 고른다.
2. 정점 직전에 **브레이크 구간 1개**(`brake`, 낮은 energy, 긴 길이)를 배치한다 — 대비가 없으면 정점이 정점으로 읽히지 않는다.
3. 시작은 `steady`로 두되 첫 비트는 정보 전달 우선(에너지 ≤ 3).
4. 정점 후 `release`(여운) 길이를 정하고, 마지막 컷은 정착 상태를 유지한다.

### 4.5 기본값과 참조 분포 (합격 기준 아님)

`references/09-edit.md`의 새 절에 명시. **모두 "출발점"이며 검증기가 검사하지 않는다.**

| 항목 | 값 | 성격·출처 |
|---|---|---|
| 비트(컷) 길이 하한 | **2.0초** | `silent-satire-animatic` 비트 예산의 실측 결론(1.3초/컷은 깜빡임으로 읽힘). 이 패키지 공유 하한 |
| 비트 길이 상한 | **8.0초** | 위 문서의 실측 결론(넘으면 분할). 정적 정보 컷은 예외로 사유 기록 |
| 연속 3컷 동일 길이(±10%) | **재검토 신호** | 관찰 보고 대상. 금지 아님 |
| 정점 직전 브레이크 구간 | **1개 이상** | 기본값 제안. 아주 짧은 광고(≤6초)에는 적용하지 않음 |
| 참조 분포(코퍼스 1,730구간) | mean 4.65s / sd 2.36 / ≤2.5s 15.1% / ≥6s 29.0% | **참조용**. 이 코퍼스는 3샷 균등 템플릿(75%)이므로 포화값이며 목표로 삼지 않는다 |
| 3샷 균등 분할(S01/S02/S03) | **반패턴** | 같은 이유로 코퍼스에서만 관찰된 값. 계획서에 이 구조를 기본값으로 쓰지 않는다 |

### 4.6 컷 핸들 요구 (리듬의 물리적 전제)

`06-shots-template.md`의 샷 표에는 이미 `핸들` 열이 있고, `project.json`은 `source_duration_s ≥ source_in_s + (end_s − start_s) × playback_rate`로 핸들 용량을 이미 강제한다. **따라서 새 필드·새 스키마 변경은 없다.** 이번에 추가하는 것은 **곡선에서 요구 핸들을 도출하는 규칙**이다. `references/11-ai-handoff.md`에 1문단 추가:

- 곡선의 `cut_out_phase`가 `mid_action`/`impact`인 구간을 포함하는 클립은 **생성 요청 단계에서 앞뒤 핸들을 확보**한다.
- 요구 핸들 프레임 = `exit_handle_frames` + 2 (프레임 정렬·미세 조정 여유). **프레임 단위는 프로젝트 `fps` 기준**이며, 생성 엔드포인트 fps가 다르면 변환값과 기준 fps를 핸드오프에 함께 적는다. 생성 길이 = 편집 길이 + 요구 핸들(이 식은 문서 산문이며 JSON 스키마 필드가 아니다).
- 핸들이 없으면 컷 온 액션이 불가능하므로, 그 경우 계획은 `cut_out_phase: settle`로 낮추고 사유를 곡선에 적는다. **핸들 부족을 사후 트림으로 덮지 않는다.**
- 핸들 확보 여부는 모델/모드 지원 확인 전까지 `UNKNOWN`으로 두는 기존 규칙을 따른다.

### 4.7 측정 스크립트 — `scripts/measure_cut_rhythm.py` (신규)

```
python scripts/measure_cut_rhythm.py --project project.json \
    [--media assembled.mp4 | --cuts cuts.csv] \
    [--fps 24] [--scene-threshold 0.30] [--min-cut-s 0.4] \
    [--short-s 2.0] [--long-s 8.0] [--match-tolerance-s 0.5] \
    [--out rhythm-report.json]
```

**검출 컷 → 샷 귀속 규칙(반드시 결정적이어야 함):**

1. `--cuts` CSV에 `shot_id` 열이 있으면 그 값을 신뢰한다(`basis: supplied_shot_ids`).
2. 없으면 검출 경계를 계획 샷 경계에 **최근접 매칭**(허용 오차 `max(--match-tolerance-s, 2/fps)`)으로 붙인다.
3. 매칭되지 않은 검출 컷은 `unmatched_detected[]`, 매칭되지 않은 계획 샷은 `unmatched_planned[]`에 남기고 `status: partial`로 보고한다. **개수 추정·순번 추측·`shot_id` 발명으로 메우지 않는다.** 검출/계획 개수가 같다는 이유만으로 순번 대응하지 않는다(휩 팬 오검출·인서트 누락이 정확히 이 경우다).
4. `--fps`가 `project.json`의 `fps`와 다르면 exit 2로 거부한다(시간 기준 혼용 방지).

- `--media`: `ffmpeg` 장면 검출(`select='gt(scene,T)'`, `metadata=print`)로 컷 시각을 뽑고, `--min-cut-s` 미만 간격은 병합한다. `ffmpeg`이 없으면 **실패를 꾸미지 않고** `status: unverified`, `reason: ffmpeg_not_found`로 종료 코드 3.
- `--cuts`: `cut_id,start_s,end_s` CSV. 사용자가 실측·수동 지정한 값을 그대로 쓴다(`status: supplied`).
- 둘 다 없으면 `project.json`의 샷 경계로 `status: planned_only` 보고(설계 대조만, 실측 아님을 명시).
- 출력(JSON, stdout 또는 `--out`):

```json
{
  "status": "measured|supplied|planned_only|partial|unverified",
  "basis": {"fps": 24, "source": "ffmpeg_scene", "shot_mapping": "nearest_within_tolerance"},
  "cuts": [{"cut_id":"M01","shot_id":"SH01","start_s":0.0,"end_s":3.2,
            "duration_s":3.2,"planned_duration_s":3.2,"delta_s":0.0}],
  "segments": [{"rhythm_id":"RB01","planned_duration_s":4.25,
                "measured_duration_s":4.10,"delta_s":-0.15,"evidence":"measured"}],
  "stats": {"count":12,"mean_s":3.4,"stdev_s":1.9,
            "short_pct":18.0,"long_pct":8.0,"short_s":2.0,"long_s":8.0,
            "monotony_runs":[[4,5,6]],
            "same_shot_size_runs":[[1,2,3]],"same_shot_size_basis":"raw_string_equality"},
  "curve_check": {"declared_intent":"...",
                  "handle_shortfalls":["SH07: realized handle 1f < required 2f for impact"],
                  "unmatched_detected":[],"unmatched_planned":[]},
  "limitations": ["scene detection cannot distinguish a whip pan from a cut"],
  "aesthetics": "not_judged"
}
```

- **판정하지 않는 것:** 좋다/나쁘다, 합격/불합격, 재생성 필요 여부. **에너지와 길이의 순위를 대조하지 않는다** — 그건 보편 리듬 공식을 만드는 일이므로 하지 않는다. 보고서가 하는 비교는 **계획 대 실측(자기 대조)** 하나뿐이다.
- `monotony_runs`: 연속 3컷 이상 길이가 ±10% 안에 있는 구간의 인덱스(관찰). 임계값은 `--monotony-pct 10`으로 조정 가능하다.
- `same_shot_size_runs`: 연속 3컷 이상 `shot_size` **문자열이 같은** 구간(관찰). 값 체계(`CU`/`close-up`)가 자유 서술이므로 정규화하지 않고 `same_shot_size_basis: raw_string_equality`를 함께 보고해 한계를 숨기지 않는다.
- **삭제된 지표:** `moving_static_ratio`는 넣지 않는다. `§장면 리듬 5`가 "무빙/컷 수 비율을 품질 기준으로 쓰지 않는다"고 못박았고, 이 지표는 리뷰어에게 사실상 점수로 읽힌다.
- `handle_shortfalls`: 선언값이 아니라 **실현된 핸들 용량**(`source_duration_s − source_in_s − (end_s − start_s) × playback_rate`)을 요구치와 대조한다. 그래야 이 항목이 실제로 발화할 수 있다.
- 구간 통계 버킷의 기본값은 패키지 기본값(2.0s / 8.0s)이며, 코퍼스 참조값(2.5 / 6.0)은 **문서 산문에만** 남기고 스크립트 버킷으로 쓰지 않는다(참조값이 기준으로 승격되는 것을 막는다).
- 종료 코드: 0 정상, 2 입력 오류(프로젝트/CSV 파싱 불가, fps 불일치), 3 측정 불가(ffmpeg 없음).

### 4.8 검증 출력 양식 — `09-edit-template.md` 대조 표

기존 컷 표를 건드리지 않고 **아래 소형 표 하나**를 추가한다(곡선 선언 시 필수, 없으면 N/A).

| rhythm_id | 계획 energy / cadence | 계획 길이 | 실측 길이(근거) | 차이 | 판정(재생 근거 필요) | 최소 수정 |
|---|---|---|---|---|---|---|
| RB01 | 2 / steady | 4.25 | 4.10 (ffmpeg scene 12컷) | −0.15 | UNVERIFIED → 재생 후 PASS_WITH_NOTES | 컷 OUT 2f 앞당김 |

표 하단 고정 문구: *"숫자만으로 판정하지 않는다. `판정` 칸은 완성 시퀀스를 실제 재생한 근거가 있을 때만 `PASS`/`PASS_WITH_NOTES`/`NEEDS_REVISION` 중 하나로 채우고, 재생 전에는 `UNVERIFIED`로 둔다. 측정값은 판정의 근거가 아니라 수정 지점을 찾는 도구다."*

즉 판정 어휘는 **사람이 재생한 결과**에만 쓰이고, 측정 스크립트는 어떤 판정도 출력하지 않는다(§6.7의 금지는 스크립트 출력에만 적용된다).

---

## 5. 파일별 변경 범위

| 파일 | 변경 |
|---|---|
| `video-production-assets/references/storyboard-contract.md` | §8에 `storyboard.rhythm` 스키마 선언, §장면 리듬 5·수락 검사 7 개정, §4.2 소유 경계 표 추가 |
| `video-production-assets/references/09-edit.md` | 신규 절 "시퀀스 리듬 계약": 곡선 문법·작성 4단계·기본값 표(§4.5)·측정 경로·**판정 금지** 문안 |
| `video-production-assets/references/06-shots.md` | 기존 액션·스피드 절에 에너지 배분 1문단 + `09-edit` 곡선 cross-ref (스키마 비소유 명시) |
| `video-production-assets/references/12-qa.md` | 리듬이 요청 기준이면 `measure_cut_rhythm.py` 결과를 기준선으로 대조하라는 1줄 |
| `video-production-assets/references/11-ai-handoff.md` | §4.6 핸들 도출 1문단 |
| `video-production-assets/assets/06-shots-template.md` | 곡선 표(§4.4) + 상단 주석 |
| `video-production-assets/assets/09-edit-template.md` | 대조 표(§4.8) + 하단 고정 문구 |
| `video-production-assets/scripts/validate_storyboard.py` | `RHYTHM_CADENCE`/`RHYTHM_CUT_PHASE` 상수, 구조·커버리지·순서·합계·핸들 검증, `--strict-rhythm` |
| `video-production-assets/scripts/measure_cut_rhythm.py` | 신규(§4.7) |
| `video-production-assets/scripts/test_validate_storyboard.py` | 신규 케이스 10종(§6) |
| `video-production-assets/scripts/test_measure_cut_rhythm.py` | 신규 |
| `video-production-assets/SKILL.md` | 실행 명령 목록에 `measure_cut_rhythm.py`·`--strict-rhythm` 1줄 추가(기존 `validate_*` 목록 자리) |
| `storyboarding-video/SKILL.md` | 리듬 곡선 포인터 1문장(기존 산출물 목록 자리) |
| `silent-satire-animatic/references/03-beat-budget.md` | 2.0s·8.0s 하한/상한을 `09-edit`와 공유한다는 see-also 1줄 |
| `docs/research/2026-11-16-prompt-corpus-tempo-analysis.md` | §8 코퍼스 수치의 재현 노트(사용한 파싱 코드·시트 목록·결과 표 포함, 기계 실행 없이 재현 가능) |
| `manifest.json` / `CHANGELOG.md` | `2.39 → 2.40` (`bump_version.py 2.40`, `--bump-skills` **사용 안 함**) |
| `video-production-assets/SKILL.md`·`storyboarding-video/SKILL.md` frontmatter | 해당 2개 스킬만 minor 수동 범프(`--bump-skills`는 23개 전체를 올리므로 쓰지 않는다) |
| `qa/2026-11-16-sequence-rhythm-validation.json` | 검증 기록(테스트 결과·문서 링크 검사) |

---

## 6. 완료 기준 (Acceptance)

1. **하위 호환:** 기존 `test_validate_storyboard.py`·`test_validate_project.py`·`test_render_storyboard_sheet.py`·`test_split_storyboard.py`·`test_storyboard_document.py` 전부 통과. `rhythm`이 없는 기존 픽스처는 새 error 0건.
2. **검증기 신규 케이스:** ① rhythm 없음 → pass ② 정상 곡선 → pass ③ beat 미커버 → fail ④ shot 미커버 → fail ⑤ `energy` 0/6/비정수 → fail ⑥ `planned_duration_s` 합 불일치 → fail ⑦ `cut_out_phase: impact` + `exit_handle_frames: 0` → fail ⑧ `--strict-rhythm`인데 rhythm 없음 → fail. ⑨ `--strict-rhythm` 없이 잘못된 rhythm → 여전히 fail(있으면 항상 검사) ⑩ 한 비트가 두 샷에 걸치는 보드(계약이 허용) → pass.
3. **측정 스크립트:** `--cuts` CSV로 합성 컷 목록 → `count/mean/stdev/monotony_runs` 정확히 계산. `--media` 없음 → `planned_only`. `ffmpeg` 부재(monkeypatch) → `status: unverified`, exit 3. 디코드 불가 미디어 → `reason: media_not_decodable`, exit 3. 잘못된 CSV → exit 2. `--fps`가 프로젝트 fps와 다름 → exit 2. 검출 경계 1개를 인위적으로 제거/추가하면 `status: partial` + `unmatched_*`가 채워지고 순번 대응으로 메워지지 않는다. `--cuts`에 `shot_id` 열이 있으면 그대로 채택된다.
4. **문서 링크:** 신규 상대 링크 100% 유효(`§4.2` 소유 경계 표 기준), 기존 앵커 깨짐 0건.
5. **경계 테스트:** `test_video_pack_boundary.py`·`test_production_policy_consistency.py`·`check_versions.py` 통과, `manifest.json` 2.40 및 SKILL 버전 정합.
6. **컨텍스트 예산:** 곡선 표 1개(≤8행) + 대조 표 1개(≤8행)만 추가. 기존 대형 관리 표는 늘리지 않는다.
7. **판정 어휘 분리:** 측정 스크립트 출력에는 판정·점수·임계값 판정이 없고 `aesthetics: not_judged`가 있다. 템플릿의 `판정` 칸은 재생 근거가 있을 때만 채우며, 증거 없는 기본값은 `UNVERIFIED`다. 문서 어디에도 "이 수치면 합격" 같은 임계값 문장이 없다.

---

## 7. 빌더 재량으로 남기는 것

- 표의 열 순서·문장 톤·예시 개수(단, §4.4·§4.8의 필드는 고정).
- `09-edit.md` 신규 절의 위치(편집 절차 뒤 권장)와 곡선 작성 4단계의 서술 밀도.
- ffmpeg 필터 문자열 세부(임계값 기본 0.30, 최소 컷 0.4초)와 파싱 구현 방식.
- 테스트 픽스처 크기·명명, 오류 메시지 문구("형식"만 §4.3에 고정).
- `storyboarding-video/SKILL.md`·`03-beat-budget.md`·`video-production-assets/SKILL.md`의 정확한 문장 위치.
- `--monotony-pct`·`--match-tolerance-s`의 기본값 미세 조정(10% / 0.5s에서 시작).
- `docs/research/` 노트의 서술 밀도(단 §8의 수치와 재현 코드는 고정).

---

## 8. 코퍼스 증거 재현 기록

| 항목 | 방법 | 결과 |
|---|---|---|
| 시트 전수 파싱 | Google Sheets XLSX export → `xl/workbook.xml` 시트 130장 → 셀 직렬화 | 시트 130장 확인 |
| 3샷 카드 비율 | 프롬프트 열에서 `S0\d\s*\[` 카드 수 집계 | 400행: 3샷 300, 5샷 25, 6샷 75 |
| 샷 구간 분포 | `[mm:ss–mm:ss]`·`[0–2.0s]` 두 표기 모두 파싱 | 1,730구간 (19시트): mean 4.65 / sd 2.36 / ≤2.5s 15.1% / ≥6s 29.0% |
| 평가표 | `평가기준` 시트 9항목 확인 | 리듬·에너지 항목 없음(`시간축·동작 15`) |

**증거 성격:** 시트는 사용자 수집 2차 자료이며 렌더 검증이 아니다. 값은 §4.5에서 참조 분포·반패턴으로만 쓰고, 모델 능력·성능 주장의 근거로 쓰지 않는다.

**재현성:** 위 수치는 이 문서에만 있으면 재현 불가하므로, 파싱 코드·시트별 집계·원본 시트 ID를 `docs/research/2026-11-16-prompt-corpus-tempo-analysis.md`에 함께 남긴다(§5). 표준 라이브러리만 쓰는 단일 스니펫으로 적어 외부 의존성 없이 재실행 가능해야 한다.
