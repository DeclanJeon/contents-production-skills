# 시퀀스 리듬 계약 구현 계획

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 보드가 선언한 시퀀스 리듬 곡선을 `project.json`에 담고, 구조 검증기와 실측 대조 스크립트로 "계획 대 실측"의 자기 일치를 확인할 수 있게 한다.

**Architecture:** `storyboard.rhythm`(옵트인)을 스키마 정본 `storyboard-contract.md` §8에 선언하고, `validate_storyboard.py`가 구조·커버리지·합계·순서·핸들 선언만 검사한다. 실측은 별도 스크립트 `measure_cut_rhythm.py`가 ffmpeg 장면 검출 또는 명시 컷 CSV로 수행하며 어떤 미학 판정도 출력하지 않는다. 문서 소유는 `06`(설계)/`09`(검증)으로 분리한다.

**Tech Stack:** Python 3 표준 라이브러리(`json`, `csv`, `statistics`, `subprocess`, `shutil`, `argparse`), pytest(기존 unittest 스타일), ffmpeg(선택 의존성).

**Spec:** `docs/superpowers/specs/2026-11-16-sequence-rhythm-contract-design.md`

## Global Constraints

- `energy`: 정수 `1..5`. `cadence`: `steady|accelerando|ritardando|brake|peak|release`. `cut_out_phase`: `pre_action|mid_action|impact|reaction|settle`.
- 핸들 선언 하한: `cut_out_phase`가 `mid_action`/`impact`이면 `exit_handle_frames >= 2`, 그 외 제약 없음.
- 합계 허용오차: `abs(planned_duration_s - Σ(end_s - start_s)) <= max(1/fps, 0.05)`.
- 컷 귀속 허용오차: `max(--match-tolerance-s, 2/fps)`, `--match-tolerance-s` 기본 `0.5`.
- 통계 버킷 기본값: `--short-s 2.0`, `--long-s 8.0`. 코퍼스 값 `2.5`/`6.0`은 **코드·버킷에 쓰지 않는다**(문서 산문에만).
- 단조 구간: 연속 3컷 이상, 길이 차이 `--monotony-pct 10` 이내.
- 종료 코드: `0` 정상, `2` 입력 오류(파싱 불가·fps 불일치·미지 shot_id), `3` 측정 불가(ffmpeg 없음/미디어 디코드 실패).
- 금지 산출물: 에너지↔길이 순위 대조, `moving_static_ratio`, 합격 점수/임계값 판정. 보고서는 `aesthetics: not_judged`를 항상 포함한다.
- 패키지 버전 `2.39 → 2.40`은 `python scripts/bump_version.py 2.40`(`--bump-skills` **없이**). 스킬 frontmatter는 `video-production-assets`·`storyboarding-video` 2개만 수동 minor 범프.
- 문서 판정 어휘: `PASS`/`PASS_WITH_NOTES`/`NEEDS_REVISION`은 **재생 근거가 있을 때만**. 근거 없으면 `UNVERIFIED`.

## Review Focus

1. **`storyboard.rhythm`이 없는 기존 보드**(모든 픽스처)가 새 검증에서 error 0건이어야 한다. — Task 4 Step 1.
2. **한 비트가 두 샷에 걸치는 보드**(계약이 허용)가 곡선 검증에서 통과해야 한다. — Task 4 Step 1.
3. **검출 컷 수 ≠ 계획 샷 수**(휩 팬 오검출·인서트 누락)일 때 순번 추측으로 귀속하면 보고서가 조용히 틀린다. `partial`로 남겨야 한다. — Task 5 Step 1.
4. **`--cuts` CSV의 `shot_id`가 프로젝트에 없을 때** 크래시하지 않고 exit 2로 거부해야 한다. — Task 5 Step 1.
5. **ffmpeg 부재 또는 디코드 불가 미디어**에서 측정을 주장하면 안 된다: `status: unverified`, exit 3. — Task 6 Step 1.

---

### Task 1: 계약 정본 — 스키마 선언과 해석 원칙

**Files:**
- Modify: `video-production-assets/references/storyboard-contract.md` (§8에 `storyboard.rhythm` 선언, §장면 리듬 5 개정, §씬 카메라 수락 검사 7 개정, 소유 경계 표 추가)

**Interfaces:**
- Consumes: 없음(문서 정본)
- Produces: 필드명 `storyboard.rhythm.intent`, `curve[].{id,beat_ids,shot_ids,energy,cadence,planned_duration_s,cut_out_phase,exit_handle_frames,reason}` — Task 3·4·5가 이 이름을 그대로 쓴다.

- [ ] **Step 1: §8 스키마 절에 리듬 확장 선언 추가**

`storyboard` 확장 객체 서술 아래에 선택 필드 `rhythm`을 추가하고, Spec §4.1의 필드 표를 그대로 옮긴다. 필수/선택 표기: `rhythm` 자체는 선택, 존재하면 `intent`와 비어 있지 않은 `curve`가 필수. `validate_storyboard.py --strict-rhythm`으로 존재를 요구할 수 있다는 한 줄을 포함한다.

- [ ] **Step 2: §장면 리듬 5항과 §씬 카메라 수락 검사 7항 개정**

Spec §1.4의 두 인용 블록 문안을 **그대로** 삽입한다(보편 품질 기준 금지 유지 + 선언된 의도의 자기 일관성 검사 + `cadence: steady`로 균등 템포 선언 허용 + 리듬 리뷰에서 `observation: 균등 템포` 1회 보고).

- [ ] **Step 3: 소유 경계·우선순위 표 추가**

Spec §4.2의 우선순위 규칙 3줄과 소유 경계 표, 그리고 "`06-shots.md`에 `rhythm` 필드가 없다는 사실을 결함으로 보고하지 않는다" 주의문을 같은 절에 넣는다.

- [ ] **Step 4: 검증**

Run: `rg -n "storyboard.rhythm|declared intent|자기 일관성|cadence: steady" video-production-assets/references/storyboard-contract.md`
Expected: 스키마 선언 1건, 개정 문안 2건, 소유 경계 1건이 모두 검색됨.

Run: `rg -n "무빙/컷 수·샷 크기 비율" video-production-assets/references/storyboard-contract.md`
Expected: "보편 품질 기준으로 쓰지 않는다" 문장 유지(삭제되지 않음).

- [ ] **Step 5: Commit**

```bash
git add video-production-assets/references/storyboard-contract.md
git commit -m "docs(rhythm): declare storyboard.rhythm schema and self-consistency principle"
```

---

### Task 2: 실행 문서 — 09 편집, 06 샷, 12 QA, 11 인계

**Files:**
- Modify: `video-production-assets/references/09-edit.md` (신규 절 "시퀀스 리듬 계약")
- Modify: `video-production-assets/references/06-shots.md` (액션·스피드 절에 1문단)
- Modify: `video-production-assets/references/12-qa.md` (1줄)
- Modify: `video-production-assets/references/11-ai-handoff.md` (핸들 도출 1문단)

**Interfaces:**
- Consumes: Task 1의 필드명과 개정 원칙
- Produces: 문서가 지정하는 스크립트 호출 경로 `scripts/measure_cut_rhythm.py`(Task 5·6이 구현)

- [ ] **Step 1: `09-edit.md`에 신규 절 추가**

`## 채택 구간·음성 교정의 편집 인계` 앞에 `## 시퀀스 리듬 계약` 절을 넣고 다음 5개를 담는다: (a) Spec §1.4의 해석 원칙 요약 3줄, (b) Spec §4.4의 곡선 작성 4단계, (c) Spec §4.5의 기본값·참조 분포 표 **그대로**, (d) 측정 경로 — `measure_cut_rhythm.py` CLI 사용 예와 "측정은 판정하지 않는다", (e) Spec §4.8 표 하단의 판정 규칙 문장.

- [ ] **Step 2: `06-shots.md` 액션·스피드 절에 1문단 추가**

동일 샷 크기·길이 연속이 속도감을 죽인다는 기존 서술 뒤에: 에너지 배분은 곡선(`storyboard.rhythm`)이 소유하며 이 문서는 컷 설계 원칙만 다룬다는 것, 곡선 표는 `assets/06-shots-template.md`, 검증은 `09-edit.md` §시퀀스 리듬 계약을 따른다는 3줄 + 상대 링크.

- [ ] **Step 3: `12-qa.md` 5항에 1줄 추가**

"리듬이 요청 기준이면 `scripts/measure_cut_rhythm.py`의 계획 대 실측 대조를 기준선으로 쓰고, 측정값만으로 통과/실패를 선언하지 않는다"를 덧붙인다.

- [ ] **Step 4: `11-ai-handoff.md`에 핸들 도출 1문단 추가**

Spec §4.6의 4개 불릿을 그대로 넣는다(중간 국면 컷 클립은 생성 단계에서 핸들 확보, 요구 프레임 = `exit_handle_frames + 2`, 프로젝트 `fps` 기준·생성 fps 다르면 변환값 기록, 핸들 부족 시 `settle`로 낮추고 사유 기록, 확보 여부는 지원 확인 전까지 `UNKNOWN`).

- [ ] **Step 5: 검증**

Run: `rg -n "시퀀스 리듬 계약" video-production-assets/references/09-edit.md video-production-assets/references/06-shots.md`
Expected: 09에 절 제목 1건, 06에 cross-ref 1건.

Run: `rg -n "measure_cut_rhythm" video-production-assets/references/09-edit.md video-production-assets/references/12-qa.md`
Expected: 두 파일 모두 1건 이상.

Run: `rg -n "exit_handle_frames" video-production-assets/references/11-ai-handoff.md`
Expected: 1건 이상.

Run: `rg -n "2\.5s|6\.0s|moving_static" video-production-assets/references/09-edit.md`
Expected: 없음(참조 분포는 4.65/2.36/15.1/29.0 형식으로만 기록).

- [ ] **Step 6: Commit**

```bash
git add video-production-assets/references/09-edit.md video-production-assets/references/06-shots.md video-production-assets/references/12-qa.md video-production-assets/references/11-ai-handoff.md
git commit -m "docs(rhythm): add rhythm contract procedure, QA route and handle derivation"
```

---

### Task 3: 출력 양식 — 곡선 표와 대조 표

**Files:**
- Modify: `video-production-assets/assets/06-shots-template.md` (곡선 표 추가)
- Modify: `video-production-assets/assets/09-edit-template.md` (대조 표 추가)

**Interfaces:**
- Consumes: Task 1의 필드명, Task 2의 절 이름
- Produces: 문서 표의 열 이름 — `rhythm_id`, `energy (1–5)`, `cadence`, `계획 길이 (s)`, `cut_out_phase · handle(f)`, `이 길이·에너지인 이유`, `실측 길이(근거)`, `차이`, `판정(재생 근거 필요)`, `최소 수정`

- [ ] **Step 1: `06-shots-template.md`에 곡선 표 추가**

"씬별 카메라 의도와 리듬" 표 **아래**에 Spec §4.4의 표(헤더·예시 행·최대 8행 권장 주석)를 그대로 넣는다. 패널 상세표와 중복되지 않게 "구간 집계 표이며 컷별 사실은 09 컷 표가 정본"이라는 1줄을 붙인다.

- [ ] **Step 2: `09-edit-template.md`에 대조 표 추가**

기존 컷 표와 "시간 압축·생략" 표 사이에 Spec §4.8의 표와 하단 고정 문구(재생 근거 없으면 `UNVERIFIED`)를 그대로 넣는다. 곡선이 없으면 `N/A`로 적는다는 조건도 명시한다.

- [ ] **Step 3: 검증**

Run: `rg -n "rhythm_id|cut_out_phase · handle" video-production-assets/assets/06-shots-template.md`
Expected: 헤더 2건.

Run: `rg -n "판정(재생 근거 필요)|UNVERIFIED" video-production-assets/assets/09-edit-template.md`
Expected: 헤더 1건 + 하단 문구 1건.

Run: `rg -c "^|" video-production-assets/assets/06-shots-template.md`
Expected: 기존 표가 삭제되지 않음(샷 명세 표·cue 표 헤더 유지).

- [ ] **Step 4: Commit**

```bash
git add video-production-assets/assets/06-shots-template.md video-production-assets/assets/09-edit-template.md
git commit -m "feat(rhythm): add rhythm curve and plan-vs-measured tables to templates"
```

---

### Task 4: 검증기 — `storyboard.rhythm` 구조 검증

**Files:**
- Modify: `video-production-assets/scripts/validate_storyboard.py` (상수 2개, 검증 블록, `--strict-rhythm`)
- Test: `video-production-assets/scripts/test_validate_storyboard.py` (케이스 10개 + 헬퍼)

**Interfaces:**
- Consumes: Task 1의 필드명·enum·허용오차
- Produces: `validate_storyboard(project, base_dir=None, require_images=False, *, check_project=True, panels_per_sheet=8, strict_staging=False, strict_rhythm=False)` — 기존 인자 유지, `strict_rhythm`만 추가. 상수 `RHYTHM_CADENCES`, `RHYTHM_CUT_PHASES`.

- [ ] **Step 1: 실패 테스트 작성**

`test_validate_storyboard.py` 파일 끝에 헬퍼와 케이스를 추가한다.

```python
RHYTHM_VALID = {'intent': 'test intent', 'curve': [
    {'id': 'RB01', 'beat_ids': ['B01'], 'shot_ids': ['SH01'], 'energy': 2,
     'cadence': 'steady', 'planned_duration_s': 2.0, 'cut_out_phase': 'settle',
     'exit_handle_frames': 0, 'reason': 'test reason'},
    {'id': 'RB02', 'beat_ids': ['B02', 'B03'], 'shot_ids': ['SH02'], 'energy': 4,
     'cadence': 'peak', 'planned_duration_s': 2.0, 'cut_out_phase': 'impact',
     'exit_handle_frames': 2, 'reason': 'test reason'},
]}


def with_rhythm(p, rhythm):
    p = copy.deepcopy(p)
    p['storyboard']['rhythm'] = copy.deepcopy(rhythm)
    return p
```

케이스(각각 별도 `unittest` 메서드):

```python
def test_rhythm_absent_keeps_existing_behavior(self):
    self.assertEqual(validate_storyboard(board()), [])
    self.assertEqual(validate_storyboard(board(), strict_rhythm=False), [])

def test_rhythm_valid_curve_passes(self):
    self.assertEqual(validate_storyboard(with_rhythm(board(), RHYTHM_VALID)), [])

def test_rhythm_uncovered_shot_fails(self):
    r = copy.deepcopy(RHYTHM_VALID); r['curve'] = r['curve'][:1]
    errors = validate_storyboard(with_rhythm(board(), r))
    self.assertTrue(any('does not cover this shot' in e for e in errors))

def test_rhythm_beat_must_be_covered(self):
    r = copy.deepcopy(RHYTHM_VALID); r['curve'][1]['beat_ids'] = ['B02']
    errors = validate_storyboard(with_rhythm(board(), r))
    self.assertTrue(any('B03' in e for e in errors))

def test_rhythm_beat_must_belong_to_its_shots(self):
    r = copy.deepcopy(RHYTHM_VALID); r['curve'][0]['beat_ids'] = ['B02']
    errors = validate_storyboard(with_rhythm(board(), r))
    self.assertTrue(any('not among its shots' in e for e in errors))

def test_rhythm_energy_out_of_range_fails(self):
    for bad in (0, 6, 2.5):
        r = copy.deepcopy(RHYTHM_VALID); r['curve'][0]['energy'] = bad
        self.assertTrue(validate_storyboard(with_rhythm(board(), r)), bad)

def test_rhythm_planned_duration_sum_mismatch_fails(self):
    r = copy.deepcopy(RHYTHM_VALID); r['curve'][0]['planned_duration_s'] = 2.5
    self.assertTrue(validate_storyboard(with_rhythm(board(), r)))

def test_rhythm_impact_phase_requires_handle_frames(self):
    r = copy.deepcopy(RHYTHM_VALID)
    r['curve'][1]['exit_handle_frames'] = 0
    self.assertTrue(validate_storyboard(with_rhythm(board(), r)))

def test_strict_rhythm_requires_rhythm_object(self):
    errors = validate_storyboard(board(), strict_rhythm=True)
    self.assertTrue(any('rhythm' in e for e in errors))

def test_rhythm_beat_may_span_segments(self):
    # Review Focus #2: the contract allows one beat across two shots; rhythm must too.
    p = copy.deepcopy(board())
    p['shots'][1]['beat_ids'] = ['B01', 'B02', 'B03']
    r = copy.deepcopy(RHYTHM_VALID)
    r['curve'][1]['beat_ids'] = ['B01', 'B02', 'B03']
    self.assertEqual(validate_storyboard(with_rhythm(p, r)), [])
```

- [ ] **Step 2: 실패 확인**

Run: `cd video-production-assets/scripts && python -m pytest test_validate_storyboard.py -k rhythm -v`
Expected: FAIL — `TypeError: validate_storyboard() got an unexpected keyword argument 'strict_rhythm'` 및 rhythm 케이스 실패.

- [ ] **Step 3: 구현**

`validate_storyboard.py`에 상수와 검증 블록을 추가한다.

```python
RHYTHM_CADENCES = ('steady', 'accelerando', 'ritardando', 'brake', 'peak', 'release')
RHYTHM_CUT_PHASES = ('pre_action', 'mid_action', 'impact', 'reaction', 'settle')
```

시그니처에 `strict_rhythm=False` 추가. `panels` 검증 뒤에 블록 삽입: `sb.get('rhythm')`이 `None`이면 `strict_rhythm`일 때만 error, 아니면 즉시 통과. 존재하면 Spec §4.3 규칙 2~6을 순서대로 검사한다(`beat_ids`는 `shot_ids`의 beat 합집합의 부분집합; beat 커버리지는 1회 이상, shot 커버리지는 정확히 1회; 항목 순서는 커버 샷 `start_s` 오름차순·항목 간 비중복; 합계는 `max(1/fps, 0.05)`; 핸들은 `mid_action`/`impact`에서 `>= 2`). `main()`에 `--strict-rhythm` 플래그를 추가해 전달한다.

- [ ] **Step 4: 통과 확인 (기존 테스트 포함)**

Run: `cd video-production-assets/scripts && python -m pytest test_validate_storyboard.py -v`
Expected: 신규 10개 + 기존 전부 PASS.

Run: `cd video-production-assets/scripts && python -m pytest test_validate_project.py test_render_storyboard_sheet.py test_split_storyboard.py test_storyboard_document.py -q`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add video-production-assets/scripts/validate_storyboard.py video-production-assets/scripts/test_validate_storyboard.py
git commit -m "feat(rhythm): validate storyboard.rhythm structure and coverage (--strict-rhythm)"
```

---

### Task 5: 측정 스크립트 코어 (계획/CSV 모드, 귀속, 통계, 대조)

**Files:**
- Create: `video-production-assets/scripts/measure_cut_rhythm.py`
- Test: `video-production-assets/scripts/test_measure_cut_rhythm.py`

**Interfaces:**
- Consumes: `project.json`의 `storyboard.rhythm`, `shots[]`, `fps`
- Produces:
  - `cuts_from_project(project: dict) -> list[dict]`
  - `read_cuts_csv(path: Path, project: dict, tolerance_s: float) -> tuple[list[dict], dict]` (`meta` = `{'shot_mapping': 'supplied_shot_ids'|'nearest_within_tolerance', 'unmatched_detected': [...], 'unmatched_planned': [...]}`)
  - `compute_stats(cuts: list[dict], shots: list[dict], short_s: float, long_s: float, monotony_pct: float) -> dict`
  - `segment_report(project: dict, cuts: list[dict]) -> list[dict]`
  - `handle_shortfalls(project: dict) -> list[str]`
  - `build_report(project: dict, cuts: list[dict], basis: dict, status: str) -> dict`
  - `main(argv: list[str] | None = None) -> int`
  - 컷 dict 형식: `{'cut_id', 'shot_id'|None, 'start_s', 'end_s', 'duration_s', 'planned_duration_s', 'delta_s'}`

- [ ] **Step 1: 실패 테스트 작성**

```python
import csv, json, statistics, unittest
from pathlib import Path
import tempfile
from measure_cut_rhythm import (cuts_from_project, read_cuts_csv, compute_stats,
                                segment_report, handle_shortfalls, build_report, main)
from test_validate_storyboard import board, with_rhythm, RHYTHM_VALID


def write_csv(dirpath, rows):
    path = Path(dirpath) / 'cuts.csv'
    with path.open('w', newline='') as f:
        w = csv.writer(f); w.writerow(['cut_id', 'start_s', 'end_s']); w.writerows(rows)
    return path
```

케이스:

```python
def test_planned_only_uses_project_shot_boundaries(self):
    cuts = cuts_from_project(board())
    self.assertEqual([c['shot_id'] for c in cuts], ['SH01', 'SH02'])
    self.assertEqual([c['duration_s'] for c in cuts], [2.0, 2.0])
    self.assertTrue(all(c['delta_s'] == 0 for c in cuts))

def test_cuts_csv_durations_and_stats(self):
    with tempfile.TemporaryDirectory() as d:
        p = write_csv(d, [('M1', 0, 4.0), ('M2', 4, 8.1), ('M3', 8.1, 12.3),
                          ('M4', 12.3, 13.3), ('M5', 13.3, 22.3), ('M6', 22.3, 25.3)])
        cuts, meta = read_cuts_csv(p, board(), 0.5)
    stats = compute_stats(cuts, board()['shots'], 2.0, 8.0, 10.0)
    self.assertEqual(stats['count'], 6)
    self.assertAlmostEqual(stats['mean_s'], 4.2167, places=3)
    self.assertAlmostEqual(stats['stdev_s'], 2.4072, places=3)
    self.assertAlmostEqual(stats['short_pct'], 16.667, places=2)
    self.assertAlmostEqual(stats['long_pct'], 16.667, places=2)
    self.assertEqual(stats['same_shot_size_basis'], 'raw_string_equality')

def test_monotony_run_detected(self):
    cuts = [{'cut_id': f'M{i}', 'shot_id': None, 'start_s': s, 'end_s': s + d,
             'duration_s': d, 'planned_duration_s': d, 'delta_s': 0.0}
            for i, (s, d) in enumerate([(0, 3.0), (3.0, 3.1), (6.1, 2.9), (9.0, 7.0)])]
    stats = compute_stats(cuts, [], 2.0, 8.0, 10.0)
    self.assertIn([0, 1, 2], stats['monotony_runs'])

def test_same_shot_size_runs_raw_string_equality(self):
    shots = [{'id': f'SH0{i}', 'start_s': i, 'end_s': i + 1,
              'camera': {'shot_size': size, 'movement': 'static'}}
             for i, size in enumerate(['medium', 'medium', 'close', 'medium'], start=1)]
    cuts = [{'cut_id': f'M{i}', 'shot_id': f'SH0{i}', 'start_s': i, 'end_s': i + 1,
             'duration_s': 1.0, 'planned_duration_s': 1.0, 'delta_s': 0.0} for i in range(1, 5)]
    stats = compute_stats(cuts, shots, 2.0, 8.0, 10.0)
    self.assertIn([0, 1], stats['same_shot_size_runs'])

def test_unmatched_detected_cut_reports_partial(self):
    with tempfile.TemporaryDirectory() as d:
        p = write_csv(d, [('M1', 0, 1.1), ('M2', 1.1, 2.0), ('M3', 2.0, 3.9), ('M4', 3.9, 4.0)])
        cuts, meta = read_cuts_csv(p, board(), 0.5)
    self.assertTrue(meta['unmatched_detected'])
    report = build_report(board(), cuts, {'fps': 24, 'source': 'cuts_csv'}, 'partial')
    self.assertEqual(report['status'], 'partial')

def test_fps_mismatch_exits_2(self):
    with tempfile.TemporaryDirectory() as d:
        proj = Path(d) / 'project.json'
        proj.write_text(json.dumps(board()))
        self.assertEqual(main(['--project', str(proj), '--fps', '30']), 2)

def test_cuts_csv_unknown_shot_id_is_invalid(self):
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / 'cuts.csv'
        with p.open('w', newline='') as f:
            w = csv.writer(f); w.writerow(['cut_id', 'start_s', 'end_s', 'shot_id'])
            w.writerow(['M1', 0, 2.0, 'SH99'])
        with self.assertRaises(ValueError):
            read_cuts_csv(p, board(), 0.5)

def test_handle_shortfall_uses_realized_capacity(self):
    p = with_rhythm(board(), RHYTHM_VALID)
    for s in p['shots']:
        s['source_duration_s'] = s['end_s'] - s['start_s']
    self.assertTrue(any('SH02' in m for m in handle_shortfalls(p)))

def test_segment_report_compares_planned_and_measured(self):
    cuts = [{'cut_id': 'M1', 'shot_id': 'SH01', 'start_s': 0, 'end_s': 2.0,
             'duration_s': 2.0, 'planned_duration_s': 2.0, 'delta_s': 0.0},
            {'cut_id': 'M2', 'shot_id': 'SH02', 'start_s': 2.0, 'end_s': 4.0,
             'duration_s': 2.0, 'planned_duration_s': 2.0, 'delta_s': 0.0}]
    segs = segment_report(with_rhythm(board(), RHYTHM_VALID), cuts)
    self.assertEqual([s['rhythm_id'] for s in segs], ['RB01', 'RB02'])
    self.assertEqual(segs[0]['measured_duration_s'], 2.0)
    self.assertEqual(segs[0]['delta_s'], 0.0)
```

- [ ] **Step 2: 실패 확인**

Run: `cd video-production-assets/scripts && python -m pytest test_measure_cut_rhythm.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'measure_cut_rhythm'`.

- [ ] **Step 3: 구현**

CLI 인자: `--project`(필수), `--cuts`, `--fps`, `--short-s 2.0`, `--long-s 8.0`, `--match-tolerance-s 0.5`, `--monotony-pct 10`, `--out`. `--media`는 Task 6에서 추가한다.

- `main`: 프로젝트 로드 실패·`--fps`가 `project.fps`와 불일치·CSV 파싱/미지 `shot_id` → `2` 반환. `--cuts` 없으면 `cuts_from_project`로 `planned_only`. 그 외 `supplied`.
- `read_cuts_csv`: 헤더에 `shot_id` 열이 있으면 그대로 채택하고 `shot_mapping='supplied_shot_ids'`; 미지 shot_id는 `ValueError`. 없으면 `csv`의 `(start_s, end_s)` 구간을 계획 샷 경계에 최근접 매칭(`tolerance_s`)하고 미매칭은 `meta`의 두 목록에 남기며 `shot_id=None`. 순번·개수 추측 금지.
- `compute_stats`: `count`, `mean_s`, `stdev_s`(모집단 `statistics.pstdev`), `short_s`/`long_s` 및 `short_pct`/`long_pct`, `monotony_runs`(연속 ≥3, 앞 컷 대비 `monotony_pct` 이내), `same_shot_size_runs`(연속 ≥3, 원문자열 동일), `same_shot_size_basis`.
- `segment_report`: 곡선 항목마다 `shot_ids`에 속한 컷 길이 합 = `measured_duration_s`, `delta_s = measured - planned`, `evidence`는 컷이 실측/공급이면 `measured`, 계획이면 `planned`.
- `handle_shortfalls`: 실현 용량 `source_duration_s - source_in_s - (end_s - start_s) * playback_rate`(기본 `source_in_s=0`, `playback_rate=1`)을 요구치(2프레임 = `2/fps` 초)와 대조해 `"SH02: realized handle 0f < required 2f for impact"` 형식 문자열 반환.
- `build_report`: `status`, `basis`, `cuts`, `segments`, `stats`, `curve_check`(`declared_intent`, `handle_shortfalls`, `unmatched_detected`, `unmatched_planned`), `limitations`, `aesthetics: "not_judged"`.

- [ ] **Step 4: 통과 확인**

Run: `cd video-production-assets/scripts && python -m pytest test_measure_cut_rhythm.py -v`
Expected: 9개 PASS.

- [ ] **Step 5: Commit**

```bash
git add video-production-assets/scripts/measure_cut_rhythm.py video-production-assets/scripts/test_measure_cut_rhythm.py
git commit -m "feat(rhythm): add measure_cut_rhythm core (plan, cuts CSV, stats, comparison)"
```

---

### Task 6: ffmpeg 미디어 모드와 정직한 미검증 경로

**Files:**
- Modify: `video-production-assets/scripts/measure_cut_rhythm.py`
- Test: `video-production-assets/scripts/test_measure_cut_rhythm.py`

**Interfaces:**
- Consumes: Task 5의 `build_report`·`main`
- Produces: `detect_cuts(media: Path, threshold: float, min_cut_s: float, fps: float) -> list[float]`; CLI `--media`, `--scene-threshold 0.30`, `--min-cut-s 0.4`

- [ ] **Step 1: 실패 테스트 작성**

```python
def test_detect_cuts_parses_ffmpeg_metadata(self):
    from unittest import mock
    with mock.patch('measure_cut_rhythm.subprocess.run') as run:
        run.return_value = mock.Mock(returncode=0, stdout='',
            stderr='frame:0 pts_time:1.2\nframe:1 pts_time:1.5\nframe:2 pts_time:4.0\n')
        times = detect_cuts(Path('x.mp4'), 0.30, 0.4, 24.0)
    self.assertEqual(times, [1.2, 4.0])

def test_missing_ffmpeg_reports_unverified_exit_3(self):
    from unittest import mock
    with tempfile.TemporaryDirectory() as d:
        proj = Path(d) / 'project.json'; proj.write_text(json.dumps(board()))
        media = Path(d) / 'cut.mp4'; media.write_bytes(b'x')
        with mock.patch('measure_cut_rhythm.shutil.which', return_value=None):
            out = Path(d) / 'r.json'
            self.assertEqual(main(['--project', str(proj), '--media', str(media),
                                   '--out', str(out)]), 3)
        self.assertEqual(json.loads(out.read_text())['status'], 'unverified')
        self.assertEqual(json.loads(out.read_text())['reason'], 'ffmpeg_not_found')

def test_media_mode_measured_status(self):
    from unittest import mock
    with tempfile.TemporaryDirectory() as d:
        proj = Path(d) / 'project.json'; proj.write_text(json.dumps(board()))
        media = Path(d) / 'cut.mp4'; media.write_bytes(b'x')
        with mock.patch('measure_cut_rhythm.shutil.which', return_value='/usr/bin/ffmpeg'), \
             mock.patch('measure_cut_rhythm.detect_cuts', return_value=[1.0, 3.0]):
            out = Path(d) / 'r.json'
            self.assertEqual(main(['--project', str(proj), '--media', str(media),
                                   '--out', str(out)]), 0)
        report = json.loads(out.read_text())
        self.assertEqual(report['status'], 'measured')
        self.assertEqual(report['basis']['source'], 'ffmpeg_scene')

def test_undecodable_media_reports_unverified(self):
    # Review Focus #5: an undecodable file must never be reported as measured.
    from unittest import mock
    with tempfile.TemporaryDirectory() as d:
        proj = Path(d) / 'project.json'; proj.write_text(json.dumps(board()))
        media = Path(d) / 'cut.mp4'; media.write_bytes(b'not-a-video')
        with mock.patch('measure_cut_rhythm.shutil.which', return_value='/usr/bin/ffmpeg'):
            out = Path(d) / 'r.json'
            self.assertEqual(main(['--project', str(proj), '--media', str(media),
                                   '--out', str(out)]), 3)
        self.assertEqual(json.loads(out.read_text())['reason'], 'media_not_decodable')
```

- [ ] **Step 2: 실패 확인**

Run: `cd video-production-assets/scripts && python -m pytest test_measure_cut_rhythm.py -k "ffmpeg or media" -v`
Expected: FAIL — `ImportError: cannot import name 'detect_cuts'`.

- [ ] **Step 3: 구현**

`detect_cuts`: `shutil.which('ffmpeg')`이 없으면 `FileNotFoundError('ffmpeg_not_found')`를 던진다. 있으면 `subprocess.run([ffmpeg, '-v', 'error', '-i', str(media), '-filter:v', f"select='gt(scene,{threshold})',metadata=print", '-an', '-f', 'null', '-'], capture_output=True, text=True)` 후 `pts_time:([0-9.]+)`를 정규식으로 수집, 정렬, `min_cut_s` 미만 간격 병합(앞 컷 유지). `returncode != 0`이면 `ValueError('media_not_decodable')`.

`main`: `--media`와 `--cuts` 동시 지정 → `2`. `--media` 경로에서 `FileNotFoundError('ffmpeg_not_found')`/`ValueError('media_not_decodable')`는 `status: unverified` + `reason` 기록 후 `3`. 검출 시각은 Task 5의 CSV 경로와 같은 `read‑` 귀속 규칙(최근접 매칭, 미매칭 → `partial`)을 재사용해 컷 dict를 만든다. `--out`이 없으면 stdout에 JSON 출력.

- [ ] **Step 4: 통과 확인**

Run: `cd video-production-assets/scripts && python -m pytest test_measure_cut_rhythm.py -v`
Expected: 13개 PASS(기존 9 + 신규 4).

- [ ] **Step 5: Commit**

```bash
git add video-production-assets/scripts/measure_cut_rhythm.py video-production-assets/scripts/test_measure_cut_rhythm.py
git commit -m "feat(rhythm): add ffmpeg media mode with honest unverified fallback"
```

---

### Task 7: 스킬 포인터와 상호참조

**Files:**
- Modify: `video-production-assets/SKILL.md` (실행 명령 목록)
- Modify: `storyboarding-video/SKILL.md` (산출물 목록에 곡선 포인터)
- Modify: `silent-satire-animatic/references/03-beat-budget.md` (see-also 1줄)

**Interfaces:**
- Consumes: Task 5·6의 CLI, Task 2의 절 이름
- Produces: 없음(문서)

- [ ] **Step 1: `video-production-assets/SKILL.md` 명령 목록 확장**

`validate_storyboard.py`·`split_storyboard.py` 안내가 있는 목록에 `python scripts/measure_cut_rhythm.py --project <project.json> [--media <cut.mp4>|--cuts <cuts.csv>] [--out <report.json>]` 1줄과 `validate_storyboard.py --strict-rhythm` 1줄을 추가한다. 측정이 판정을 대신하지 않는다는 반 줄을 붙인다.

- [ ] **Step 2: `storyboarding-video/SKILL.md` 포인터**

장면 리듬 문단(기존 contract 링크 문장 뒤)에 "보드가 시퀀스 리듬 곡선을 선언하면 `storyboard.rhythm`과 `09-edit.md` §시퀀스 리듬 계약을 따른다" 1문장을 넣는다.

- [ ] **Step 3: `03-beat-budget.md` see-also**

비트 길이 하한/상한 절에 "2.0초 하한·8.0초 상한은 `video-production-assets/references/09-edit.md` §시퀀스 리듬 계약과 공유한다" 1줄 + 상대 링크.

- [ ] **Step 4: 검증**

Run: `rg -n "measure_cut_rhythm|strict-rhythm" video-production-assets/SKILL.md`
Expected: 2건 이상.

Run: `rg -n "storyboard.rhythm" storyboarding-video/SKILL.md`
Expected: 1건.

Run: `rg -n "시퀀스 리듬 계약" silent-satire-animatic/references/03-beat-budget.md`
Expected: 1건.

- [ ] **Step 5: Commit**

```bash
git add video-production-assets/SKILL.md storyboarding-video/SKILL.md silent-satire-animatic/references/03-beat-budget.md
git commit -m "docs(rhythm): point skills at rhythm contract and measurement CLI"
```

---

### Task 8: 재현 노트, 검증 기록, 패키지 버전 2.40

**Files:**
- Create: `docs/research/2026-11-16-prompt-corpus-tempo-analysis.md`
- Create: `qa/2026-11-16-sequence-rhythm-validation.json`
- Modify: `manifest.json`, `CHANGELOG.md`, `video-production-assets/SKILL.md` frontmatter, `storyboarding-video/SKILL.md` frontmatter

**Interfaces:**
- Consumes: 모든 이전 태스크
- Produces: 없음

- [ ] **Step 1: 코퍼스 재현 노트 작성**

표준 라이브러리만 쓰는 단일 스니펫(XLSX export → `xl/workbook.xml` 시트 목록 → `sharedStrings.xml` + 셀 직렬화 → `S0\d\s*\[` 카드 수, `[mm:ss–mm:ss]`·`[0–2.0s]` 구간 길이)과 결과 표(400행 중 3샷 300/5샷 25/6샷 75; 1,730구간 19시트 mean 4.65 sd 2.36 ≤2.5s 15.1% ≥6s 29.0%; 평가기준 9항목), 원본 시트 ID·수집 기간, "2차 자료·렌더 미검증" 표기를 담는다.

- [ ] **Step 2: 새 테스트만 먼저 실행**

Run: `cd video-production-assets/scripts && python -m pytest test_validate_storyboard.py -k rhythm test_measure_cut_rhythm.py -v`
Expected: 전부 PASS.

- [ ] **Step 3: 전체 스위트 실행**

Run: `cd /home/declan/Documents/Projects/Products/04_Skills/Skills-and-Automation/contents-production-skills && python -m pytest -q`
Expected: PASS(기존 + 신규). 실패가 있으면 원인 수정 후 재실행.

- [ ] **Step 4: 검증 기록 작성**

`qa/2026-11-16-sequence-rhythm-validation.json`에 다음을 기록한다: 실행 명령, 테스트 수/결과, 태스크별 파일 목록, "미검증 항목"(`--media` 실측은 실제 영상으로 미실행).

- [ ] **Step 5: 문서 링크 해석 검사**

변경된 문서 9종(`storyboard-contract.md`, `09-edit.md`, `06-shots.md`, `12-qa.md`, `11-ai-handoff.md`, 두 템플릿, 두 SKILL)과 `03-beat-budget.md`의 **신규 상대 링크·앵커**가 모두 해석되는지 일회성 파이썬 스니펫으로 확인한다(정규식으로 `](...)` 수집 → `#` 앞 경로 resolve, 같은 파일 앵커는 헤딩 슬러그 대조). 결과를 Step 4의 JSON에 `links: {checked, broken: []}`로 기록한다.

Run: `git diff --name-only HEAD~8 -- '*.md'`
Expected: 링크 검사 대상이 위 목록과 일치. 깨진 링크가 있으면 고친 뒤 재실행해 `broken`을 빈 배열로 만든다.

- [ ] **Step 6: 판정 어휘 금지 문구 점검**

Run: `rg -n "합격|이 수치면|임계값 이상" video-production-assets/references/09-edit.md video-production-assets/references/storyboard-contract.md`
Expected: 합격 판정으로 읽히는 문장 0건(금지 규정을 설명하는 문장만 허용).

Run: `rg -n "not_judged" video-production-assets/scripts/measure_cut_rhythm.py`
Expected: 1건 이상.

- [ ] **Step 7: 버전 범프**

```bash
python scripts/bump_version.py 2.40
```

그 다음 `video-production-assets/SKILL.md`와 `storyboarding-video/SKILL.md`의 frontmatter `version`만 각각 minor 수동 범프(`1.26 → 1.27`, `2.28 → 2.29` — 실제 값은 파일에서 확인).

- [ ] **Step 8: CHANGELOG 항목 확인**

`## 2.40` 절에 다음 불릿이 모두 있는지 확인하고 없으면 추가: 리듬 곡선 스키마, 검증기 `--strict-rhythm`, `measure_cut_rhythm.py`, 핸들 도출 규칙, 참조 분포·3샷 반패턴, `moving_static_ratio`·에너지 순위 대조를 **넣지 않은 이유**.

- [ ] **Step 9: 최종 검증**

Run: `python scripts/check_versions.py`
Expected: PASS.

Run: `python -m pytest scripts/test_video_pack_boundary.py scripts/test_production_policy_consistency.py -q`
Expected: PASS.

Run: `git status --short`
Expected: 의도한 파일만 변경/추가됨.

- [ ] **Step 10: Commit**

```bash
git add docs/research/2026-11-16-prompt-corpus-tempo-analysis.md qa/2026-11-16-sequence-rhythm-validation.json manifest.json CHANGELOG.md video-production-assets/SKILL.md storyboarding-video/SKILL.md
git commit -m "chore(rhythm): bundle 2.40 with corpus note and validation record"
```

---

## 검증 요약 (실행자가 마지막에 확인)

| 항목 | 명령 |
|---|---|
| 신규 검증기 케이스 | `cd video-production-assets/scripts && python -m pytest test_validate_storyboard.py -k rhythm -v` |
| 측정 스크립트 | `cd video-production-assets/scripts && python -m pytest test_measure_cut_rhythm.py -v` |
| 전체 | `python -m pytest -q` |
| 버전·경계 | `python scripts/check_versions.py`, `python -m pytest scripts/test_video_pack_boundary.py -q` |
| 금지 산출물 부재 | `rg -n "moving_static|energy_duration_conflicts" video-production-assets/` → 0건 |
