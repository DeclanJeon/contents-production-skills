# Routing eval — boundary sweep (유효 측정)

측정 대상: 이 패키지의 3계층 라우터(`creative-production/SKILL.md` + `routing.csv`)
도구: `scripts/routing_eval.py`
모델: `gpt-6.1-sol` (Codex CLI 0.167.1)
케이스: 53개 (`C` 27 route-coverage + `B` 26 adversarial boundary)

## 결과

| 항목 | 값 |
|---|---|
| 정확도 | **53/53 = 100.0%** |
| `dangerous` (media/authority 축 교차 오답) | **0** |
| `near_miss` | 0 |
| `unanswered` | 0 |
| `isolation_leak` | 0 |

## 격리 검증 (이 회차가 이전 회차보다 신뢰할 수 있는 이유)

하네스는 각 케이스마다 에이전트가 실제로 연 파일 목록(`reads`)을 기록하고,
샌드박스 절대경로를 벗어난 읽기를 `isolation_leak`으로 판정해 **정답에서
제외**한다. 이번 회차는 53건 모두 `leaks: []`였다.

샌드박스 구성:
- `creative-production/SKILL.md`, `creative-production/references/routing.csv`
- `skills/creative-production/` 에 동일 사본 (skill 탐색이 실제 설치본이 아닌
  픽스처를 찾도록)
- `AGENTS.md`에 읽어도 되는 경로를 열거하고 `~/.codex/skills`, `~/.agents`
  읽기를 명시적으로 금지
- `-C <sandbox>`, `-s read-only`, `--ignore-user-config`,
  `skills.search_dirs=[<sandbox>/skills]`, `mcp_servers={}`

## 적대적 경계 케이스 (B01–B25, 26개)

각 케이스는 **경계를 이루는 두 route 중 하나로 오도되도록** 작성했다. 정답
키워드를 일부러 넣지 않았고, `boundary_note`에 왜 적대적인지 기록했다.

| 클러스터 | route | 케이스 |
|---|---|---|
| 콘티 깊이 | R11 러프 / R10 제작용 / R24 이미지 패키지 | B01, B01b, B02, B03, B04 |
| 무성 계열 | R07 서사 / R08 타이밍 / R09 풍자 | B05, B06, B07 |
| 텍스트 기획 vs 이미지 패키지 | R05 / R24 | B08, B09 |
| 카메라 계열 | R17 구도 / R18 설계 / R21 수치만 / R19 제어 변환 / R16 레퍼런스 관찰 | B10–B14 |
| 에셋 모듈 깊이 | R06 검수 / R13 단일 모듈 / R15 교육 기획 | B15, B16, B17 |
| 레퍼런스·감사 | R25 / R26 / R27 | B18, B19, B20 |
| 페르소나 vs 시트 | R04 / R03 | B21, B22 |
| 미디어 축 함정 | R12 / R14 / R20 | B23, B24, B25 |

## 측정 과정에서 표가 실제로 틀렸던 사례 3건

이 회차의 가치는 100%라는 숫자보다, 적대적 케이스가 **표의 실제 모호성을
드러냈다**는 점이다. 세 건 모두 "라우터가 옳고 표가 틀렸다".

1. **R20** — 카메라 무빙 검수가 `executed_media`로 분류돼 있었고
   `authority_axis`가 비어 있었다. 새 생성을 승인하지 않는 재생 검사이므로
   `varies` / `supplied_media_only`로 수정.
2. **R11** — 러프 패널 요청에 대해 에이전트가 `UNASSIGNED`를 반환했다.
   R11은 `text_only`인데 `stop_boundary`가 *이미지 호출 금지*를 명시하지 않아
   "러프 패널 이미지를 그려달라"는 요청이 어느 route에도 안 걸렸다.
   stop_boundary에 이미지 실행은 별도 승인이 필요함을 명시.
3. **R10** — stop_boundary가 "text-only면 미디어 미검증"만 말하고 이미지 생성
   금지를 명시하지 않았다. R24와의 경계를 명확히 하도록 보강.

## 처리한 하네스 결함 (측정 신뢰성)

- **파서**: `ROUTE: R13 — one_production_asset` 형태를 파싱하지 못해 정답을
  UNASSIGNED로 기록 → route id 정규화 추가. `r24.`, `**R24**`도 허용.
- **격리 누수 미감사**: 에이전트가 `~/.codex/skills/`를 읽어도 알 수 없었다 →
  읽기 경로 추출 + 샌드박스 외부 판정 추가.
- **셸 비활성화 부작용**: `features.shell_tool=false`로 하면 픽스처를 읽을 수
  없어 에이전트가 `UNASSIGNED`를 반환했다. 격리는 셸 차단이 아니라 경로 감사로
  달성한다.
- **오탐**: 셸 래퍼(`/usr/bin/bash -lc '...'`)에서 프로그램명을 파일 경로로
  오인해 상대경로를 누수로 판정 → 리더 도구 인자만 추출하도록 수정.
- 이 네 가지는 `scripts/test_routing_eval_harness.py`(8개, 모델 호출 없음)로
  고정했다.

## 이 결과가 주장하지 않는 것

- 53개 케이스는 **내가 작성한** 프롬프트다. 경계마다 route를 하나씩 덮도록
  설계했지만 실제 사용자 발화 분포를 대표하지 않는다.
- 케이스당 1회 실행이다. 샘플링 분산을 측정하지 않았다.
- 모델·프롬프트·케이스 집합이 바뀌면 재측정해야 한다.
- 100%는 "이 지시문이 이 모델에게 이 케이스들에 대해 어떻게 읽혔는가"의
  측정값이며 라우팅 정확도의 보편 지표가 아니다.
- LLM 출력은 측정값이며 패키지 사실이 아니다. 어떤 SKILL.md도 이 결과를
  근거로 자동 수정되지 않는다. 표 수정 3건은 **표의 구조적 결함**을 근거로
  했고, 측정값은 그 결함을 발견하는 수단이었다.

## 재현

```bash
# 모델 없이 구조·문법·파서·격리검사 회귀
python3 scripts/routing_regression.py
python3 -m pytest scripts/test_routing_regression.py \
                  scripts/test_routing_table_lint.py \
                  scripts/test_routing_eval_harness.py

# 실제 측정 (인증된 Codex CLI 필요, 디스크가 있는 경로를 지정)
ROUTING_EVAL_TMP=/path/with/disk \
  python3 scripts/routing_eval.py --out qa/routing-eval-<date>
```

`--out`을 주지 않으면 요약만 출력하고 원본 wire를 저장하지 않는다.
`dangerous`가 1건이라도 있으면 종료 코드가 1이다.
