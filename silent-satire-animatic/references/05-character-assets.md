# 캐릭터 자산 연결 (필수)

무성 애니메틱에서 캐릭터 시트를 쓰지 않는 것은 선택이 아니라 **결함**이다.

## 왜 필수인가

무성 콘텐츠는 대사·자막이 없다. 시청자가 인물을 식별하는 단서는 **실루엣·색·비율·부속 파츠**뿐이다. 이것을 기본 도형으로 대체하면:

- 시리즈 연속성이 끊긴다 (회차마다 같은 캐릭터로 보이지 않음)
- 캐릭터 시트 제작 비용이 전부 매몰된다
- 채널 정체성이 "아무 스틱맨"으로 희석된다

## 연결 누락의 전형적 징후

파이프라인이 캐릭터 팩을 로드하지 않아도 **렌더는 성공하고 검증도 통과한다.** 이것이 가장 위험한 실패 모드다.

| 징후 | 확인 방법 |
|---|---|
| manifest 에 `character` 키가 없음 | 산출물 manifest 키 목록 검사 |
| 결과물이 항상 같은 기본 색 | 프레임에서 인물 색 추출 |
| 캐릭터 팩 로딩 함수 호출 0회 | `grep -rn "load_pack" <파이프라인>` |

**검증 게이트로 강제할 것**: manifest 에 `character.character_id` 와 `pack_source` 가 없으면 릴리스 생성 중단.

## 팩 구조 (stickverse 기준)

```
assets/characters/
├── characters.json          # {"schema_version", "characters": ["CH01_시안", ...]}
└── CH0x_<이름>/
    ├── character.json        # palette, silhouette, parts, identity_text, metadata
    ├── identity.md           # 시각 연속성 잠금 텍스트
    ├── sheet.png             # 통합 시트 (상단4뷰 + 하단4뷰)
    └── views/                # 개별 뷰 8장
```

`character.json` 에서 렌더에 실제로 쓰이는 필드:

| 필드 | 용도 |
|---|---|
| `palette.body/ink/accent/paper` | 채색 |
| `silhouette.head.radius` | 머리 크기 |
| `silhouette.eyes` | 눈 흰자/동공 |
| `silhouette.limb.thickness` | 팔다리 굵기 |
| `silhouette.ground_offset` | 지면 정렬 |
| `parts[]` | 꼬리·날개 등 부속 파츠 |
| `metadata.title_template` | **채널 제목 형식** |

## 조용한 폴백 금지

캐릭터 팩이 없을 때 하드코딩 기본 캐릭터로 **자동 대체하면 안 된다.** 그러면 캐릭터 미사용 문제가 경고 없이 재발한다.

```
if 팩 없음:
    raise CastError("supplied character pack not found")   # 중단
```

렌더가 실패하는 편이, 캐릭터 없는 영상이 조용히 나오는 것보다 낫다.

## 캐릭터 배정 — 코드가 추론하지 않는다

**가장 흔한 실패**: 소재 키워드를 보고 종족을 자동 매칭하는 것. 하지 말 것.

캐릭터 시트는 각자 `역할/행동/표현` 절에 자기 역할을 명시하고, **"새 역할·줄거리·관계·성장 서사는 만들지 않는다"**고 못박는다. 소재가 무엇이든 코드가 역할을 재해석하면 시트 계약 위반이다.

| 하지 말 것 | 이유 |
|---|---|
| 키워드 → 종족 자동 매칭 | 시트가 규정한 역할을 코드가 덮어씀 |
| 소재 기반 회전 배정 | 시리즈 주인공이 매회 바뀜 |
| "이 소재엔 이 캐릭터가 어울려" | 제작자 판단을 코드가 대신함 |

**올바른 방식**

```
character_id 미지정 → 시트가 "기존 주인공"이라 밝힌 캐릭터 (단일 주연)
character_id 지정   → 그 캐릭터 (제작자의 명시적 결정)
```

채널이 단일 주연("Stickman")으로 운영된다면 **매회 같은 캐릭터**가 나와야 한다. 앙상블이 필요하면 제작자가 `character_id`로 지정한다.

## identity_text 를 읽어라

`character.json`의 `identity_text`에 역할·행동 규칙·대표 표정이 들어 있다. 렌더에 직접 쓰이지 않아도, **캐릭터를 배정하거나 연출할 때 이 텍스트가 유일한 근거**다.

예 (CH01): "위기에는 눈이 커지고 손을 펼치며 놀라지만 충전 목표를 향해 집중하고 행동한다"
→ `notice` 비트의 표정 설계가 여기서 나온다.

## 제목은 팩 템플릿을 쓴다

`metadata.title_template` 이 채널의 실제 형식을 담고 있다. 직접 만든 형식은 시리즈 일관성을 깬다.

```
[스틱버스] {name}의 {prop} 대작전 #Shorts
```

**실패 사례**: 팩을 무시하고 `[스틱버스] {풍자대상} #Shorts` 를 직접 생성 → 기존 게시물 35건과 형식 불일치.

## 검증 체크리스트

```
- [ ] load_pack 이 호출되고 source_index 가 asset pack 이다 (legacy_hardcoded 아님)
- [ ] plan.figure 가 채워져 있다
- [ ] plan.palette 가 4색을 모두 정의한다
- [ ] parts 가 팩 정의와 일치한다
- [ ] manifest.character.character_id 가 기록된다
- [ ] 제목이 팩 title_template 을 사용한다
- [ ] 렌더된 프레임에서 인물 색이 팩 palette.body 와 일치한다
- [ ] 육안 확인: 시트 뷰와 같은 실루엣·부속 파츠
```

마지막 두 항목이 핵심이다. 코드가 팩을 "읽었다"는 것과 화면에 "나왔다"는 것은 다르다.
