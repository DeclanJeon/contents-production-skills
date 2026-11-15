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

## 캐릭터 선택 규칙

회전 배정(rotation)이 아니라 **신체 적합성**으로 고른다. 몸이 농담과 모순되면 버그로 읽힌다.

| 종족 | 물리적 능력 | 어울리는 실패 유형 |
|---|---|---|
| humanoid | 범용 | 잔여 전부 |
| gecko | 기어오르기·점착 | 장애물·벽·도주 |
| bat | 매달리기·활공 | 유인·끌림 |
| robot | 정확 반복 | 기계·시스템·루프 |
| pufferfish | 부풀기 | 삼킴·채움·넘침 |
| beetle | 밀기·버티기 | 무거움·저항 |

동일 종족이 여럿이면 시드(소재 ID 등) 해시로 결정론적으로 분기한다. 같은 소재는 항상 같은 캐릭터.

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
