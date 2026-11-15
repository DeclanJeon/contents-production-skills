# 프롬프트 코퍼스 템포 분석 — 재현 기록 (2026-11-16)

**목적:** `video-production-assets/references/09-edit.md` §시퀀스 리듬 계약이 참조하는 "수집 코퍼스 1,730구간 / 평균 4.65초 / 3샷 균등 템플릿 75%" 수치의 출처와 재현 방법을 고정한다.

**증거 성격:** 사용자 수집 **2차 자료**이며 렌더 검증이 아니다. 값은 (a) 3샷 균등 분할의 **반패턴 증거**, (b) 템포 **참조 분포**로만 쓴다. 모델 성능·효과 보장·합격 기준의 근거가 아니다.

## 원본

| 항목 | 값 |
|---|---|
| 문서 | Google Sheets `1hhHW1d-JCKo4WYeU0wVb_LqJmZuzcCFNqBL2meghPmw` |
| 수집 기간 | 2026-09-26 ~ 2026-11-15 (시트 제목 기준, 일자별 `수집 25선` 외 모델 근거·기법 로그·프레임 에셋 시트 포함) |
| 시트 수 | 130 |
| 분석 대상 | 프롬프트 행이 있는 시트 전수(아래 스니펫은 `시트1`·`정제 프롬프트 DB`를 제외하고 집계) |

## 재현 절차 (표준 라이브러리만)

```bash
# 1) 공개 공유 문서의 XLSX export를 받는다
curl -sSL -o /tmp/sheet.xlsx \
  "https://docs.google.com/spreadsheets/d/1hhHW1d-JCKo4WYeU0wVb_LqJmZuzcCFNqBL2meghPmw/export?format=xlsx"
```

```python
# 2) 각 시트를 TSV로 펼친 뒤 두 지표를 센다 (의존성 없음)
import zipfile, re, glob, statistics, collections, xml.etree.ElementTree as ET

NS = '{http://schemas.openxmlformats.org/spreadsheetml/2006/main}'
RID = '{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id'
z = zipfile.ZipFile('/tmp/sheet.xlsx')
sst = [''.join(t.text or '' for t in si.iter(NS + 't'))
       for si in ET.fromstring(z.read('xl/sharedStrings.xml'))]
wb = ET.fromstring(z.read('xl/workbook.xml'))
rels = {r.get('Id'): r.get('Target')
        for r in ET.fromstring(z.read('xl/_rels/workbook.xml.rels'))}
for sheet in wb.find(NS + 'sheets'):
    rows = []
    xml = ET.fromstring(z.read('xl/' + rels[sheet.get(RID)]))
    for row in xml.iter(NS + 'row'):
        cells = []
        for c in row:
            v, inline = c.find(NS + 'v'), c.find(NS + 'is')
            if c.get('t') == 's' and v is not None:
                cells.append(sst[int(v.text)])
            elif inline is not None:
                cells.append(''.join(t.text or '' for t in inline.iter(NS + 't')))
            else:
                cells.append(v.text if v is not None else '')
        rows.append('\t'.join(x.replace('\t', ' ') for x in cells))
    name = re.sub(r'[^\w가-힣.-]+', '_', sheet.get('name'))
    open(f'/tmp/sheets/{name}.tsv', 'w').write('\n'.join(rows))

# 3) 샷 카드 수 분포 (S01/S02/... 카드 개수)
def shot_cards(text):
    return len(re.findall(r'\bS0\d\s*\[', text))

# 4) 샷 구간 길이: 두 표기([mm:ss–mm:ss] 와 [0–2.0s])를 모두 파싱
def tosec(txt):
    txt = txt.strip().rstrip('s')
    return int(txt.split(':')[0]) * 60 + float(txt.split(':')[1]) if ':' in txt else float(txt)

span = re.compile(r'\[?\s*((?:\d{1,2}:)?\d{1,3}(?:\.\d+)?)s?\s*[–\-~]\s*((?:\d{1,2}:)?\d{1,3}(?:\.\d+)?)s\s*\]')
```

## 결과

### 1) 샷 카드 구조 (프롬프트 400행)

| 샷 카드 수 | 행 수 | 비중 |
|---|---|---|
| 3 (`S01` establish / `S02` action / `S03` hold) | 300 | 75.0% |
| 5 | 25 | 6.3% |
| 6 | 75 | 18.8% |

→ 프롬프트 템플릿이 **3샷 균등 구조**로 포화. 이것이 반패턴 증거의 근거다.

### 2) 샷 구간 길이 분포 (19시트, 1,730구간)

| 지표 | 값 |
|---|---|
| 평균 | 4.65초 |
| 표준편차(모집단) | 2.36 |
| 2.5초 이하 | 15.1% |
| 6초 이상 | 29.0% |

시트별 표본(상위 6):

| 시트 | 구간 수 | 평균 |
|---|---|---|
| `2026-11-15 수집 25선` | 150 | 4.55 |
| `2026-11-14 수집 25선` | 150 | 3.83 |
| `2026-11-09 수집 25선` | 150 | 5.72 |
| `2026-11-08 수집 25선` | 150 | 6.28 |
| `2026-11-07 수집 25선` | 150 | 5.27 |
| `2026-11-13 수집 25선` | 75 | 4.51 |

### 3) 평가표 (`평가기준` 시트, 9항목 100점)

`서사/시놉시스 15` · `캐릭터·제품 일관성 15` · `Storyboard·Shot 설계 15` · `시간축·동작 15` · `Camera·Lens 10` · `Lighting·Color 10` · `First/Last Frame 10` · `Audio 5` · `모델 적합성 5`.

리듬·에너지·동세 전용 항목이 없고, 가장 가까운 항목은 `시간축·동작`("관찰 가능한 동작과 인과적 진행이 있는가")이다. 밋밋한 결과도 100점이 가능하다.

## 이 기록을 어떻게 쓰는가

- **쓰는 곳:** `09-edit.md` §기본값과 참조 분포의 참조 행(목표 아님 표기), 3샷 균등 분할 반패턴.
- **쓰지 않는 곳:** 스크립트 버킷·임계값(기본값은 2.0초/8.0초), 모델 선택 근거, 품질 판정. `measure_cut_rhythm.py`의 `--short-s`/`--long-s` 기본값은 코퍼스 값(2.5/6.0)이 아니다.
