# 레퍼런스 영상 분해 (온디맨드 심화)

모듈 01·05·06·09의 공통 심화. 사용자가 단일 영상·클립·광고·릴스·숏·영화 장면·시각 레퍼런스의 제작 원리를 추출하거나, 여러 비디오가 있는 폴더/아카이브를 분석해 교차 영상 패턴과 스킬 커버리지/갭을 비교해 달라고 할 때 연다. 명시적으로 기존 스킬에 일반 제작 방법을 이전해 달라고 한 요청도 이 경로를 따른다. 보호된 표현을 복제하는 대신, 근거가 허용하는 범위의 이전 가능한 제작 원리를 추출한다.
사용 가능한 레퍼런스가 없더라도 반환 전에 이 모듈을 읽고 요구 입력을 확인한다. 분석할 영상이 없으면 분석을 시작하지 말고, 부족한 입력만 지정해 멈춘다.

## 레퍼런스 발견과 선택

"레퍼런스를 찾아 달라"는 요청에는 후보 제안과 상세 분석을 분리한다. 상세 분석은 사용자가 후보를 선택·승인한 뒤에만 시작한다.

1. 후보마다 셋을 적는다: 확인 가능한 만큼의 식별자/출처(제목·채널·링크), 해당 채널·관객과의 적합성, 이 브리프에 이전 가능한 구체적 요소 하나.
2. 후보 단계에서는 후보를 제시할 만큼의 공개 메타데이터·미리보기만 본다. 선택되지 않은 자료를 전체 시청하거나 상세 분석하지 않는다.
3. 사용자가 영상·링크·폴더·아카이브를 직접 제공하고 분석을 요청한 경우 이미 선택된 것으로 보고, 별도 승인 없이 바로 분석한다.
4. 선택된 자료를 분석하는 읽기와 재사용·외부 업로드·유료 분석·생성 권한을 구분한다. 분석 요청만으로 외부 전송이나 과금을 승인받았다고 보지 않고, 해당 단계는 기존 승인 범위가 있을 때만 수행한다.

## 절차

1. 형식·길이·화면비·장르·관객·목적을 파악하고 실제로 검사한 소스 버전/구간을 기록한다. 영상 전체를 보지 못했으면 분석 범위와 표본 구간을 먼저 밝힌다.
2. 샷 또는 의미 있는 시각 비트로 분절한다. 실제 컷 시점은 측정하고, 측정할 수 없으면 근사치로 표시한다.
3. 비트마다 피사체·행동의 시작/끝 상태·주요 동작 정점(접촉·충격·제품 공개 등)·프레이밍/스케일·카메라 무빙·조명·팔레트·연기·전환·연속성을 기록한다. 프레임이나 타임코드로 관찰할 수 없는 내용은 추정으로 둔다.
4. 같은 타임라인에 컷 지점·전환 종류와 길이·음악/효과 큐를 놓는다. 화면 변화와 소리의 동기점은 실제 시각·타임코드로 적고, 확인할 수 없는 정밀도는 만들지 않는다.
5. 참조 음원이 분리 stem인지 단일 믹스인지 구분한다. 혼합 음원만 있으면 음악과 효과음을 분리해 들었다고 표현하지 않고, 재사용 권리는 별도 미확인으로 기록한다.
6. **표면 스타일**(의상·팔레트·질감·세트 장식)과 **구조 논리**(정보 공개 순서·스케일 변화·동작/카메라 동기·감정 전환·컷 리듬)를 분리한다. 역동성은 컷 수나 전환 효과가 아니라 실제 피사체/카메라의 시간적 변화와 그 배열로 설명한다.
7. 발견을 재사용 가능한 제작 레시피로 변환한다. 원리는 보존하고, 사용자가 소유하거나 재사용을 허가하지 않은 캐릭터·사건·브랜드 에셋·장소·대사·특정 보호 디자인은 바꾼다. 전문 문제는 아래 경로로 라우팅한다.
### 원본 위치·경계·분석 ID의 증거 수준

아카이브 감사에서는 `archive_id`를 source의 안정된 identity로 사용하고, 원본 장·분석에서 쓰는 locator를 프로젝트의 `scene_id`, `shot_id`, `panel_id`로 승격하지 않는다. `C##`는 detector candidate/neighborhood, `B##`는 관찰 블록, `G##/SG##`는 장면 해석, `S##.P##`는 source shot 안의 action phase를 나타낼 수 있다. 숫자와 접두어만으로 종류를 추정하지 말고 해당 source의 legend를 따른다. 인용하는 모든 occurrence/sequence/scene/shot/event/candidate ID는 원문 그대로 전체를 쓴다—`…`, 기타 생략·잘림, 재생성 alias를 쓰지 않는다.

검출 점수나 프레임 차이는 `DETECTOR_CANDIDATE`다. 후보 하나, contact sheet, 1fps/native sample, 성공한 전체 decode도 컷 경계 검증이 아니다. `SH###`는 경계 양쪽의 원본 증거로 컷을 실제 확인했을 때만 사용하고, 표본 사이의 경계는 bracketed `ESTIMATED` 또는 `UNKNOWN`으로 남긴다. Scene, shot/cut, 한 shot 안의 여러 action phase를 따로 세며 dissolve/morph/wipe가 미확정이면 transition candidate라 한다.

각 locator에는 요청 시각(`requested_s`)과 실제 source frame PTS(`source_pts_s`)를 구분해 기록한다. PTS는 샘플 프레임 위치이지 정확한 cut time이나 action onset이 아니다. 같은 시각의 화면 텍스트는 `OBSERVED`로 쓸 수 있지만 실제 speech timing/부재는 청취가 필요하다. Uploader pipeline/tool credits는 `DECLARED_UPLOADER_CLAIM`; 자동 캡션은 `CAPTION_TEXT_AUTO_UNTIMED`; ASR는 `ASR_RUN / HYPOTHESIS_UNVERIFIED`; 미청취 오디오·미검사 구간은 `UNKNOWN`이다. Frame review ≠ continuous playback; stream metadata ≠ listening.

새 브리프에 옮길 때는 관찰한 source locator와 새 계획의 proposed timing/IDs를 다른 열에 둔다. `assets/shot-dna-template.md`의 source scope, observed/estimated/unknown, transfer chain, reusable mechanism fields를 쓰고, 확인할 실제 생성/렌더/재생은 담당 모듈에 넘긴다. 분석은 컷 전체 인증·제작 경로/권리·효능·성과 승인이 아니다.

When a bounded single-source crosswalk is produced, its existing status/coverage/gate slots MUST separately state the selected source's exact status from the current master with locator, the exact filename in the source-provenance row (never in the reusable mechanism), archive-global materialized/total and unmaterialized occurrence counts, and every current OPEN global gate by exact key/status. Resolve the current semantic index from the master's current index pointer (`source_index_ref` in the current master; follow `current_index_ref` where present), then read the index's `global_merge_gates`; 44/44 identities indexed is not gate closure. Source closure or counts alone are insufficient; unavailable values stay `UNKNOWN`/`OPEN`, not inferred. This requirement applies only when a crosswalk is produced and does not require a crosswalk for ordinary single-reference analysis.

### 제작 레시피 연계

레퍼런스의 메커니즘은 새 브리프에만 적용한다. 카피→행동·콘셉트·정보 순서는 [16 콘셉트 설계](16-concept-emotion-retention.md)와 [09 편집](09-edit.md), 제품 불변 속성·반사·접촉 상태는 [19 제품 통합](19-brand-product-integration.md)·[26 상태 인계](26-state-causality-continuity.md)·[21 생성 QA](21-generated-video-qa-retry.md), 연기·공간 앵커·POV는 [04 연기](04-performance.md)·[06 샷](06-shots.md)·`$camera-spatial-design`, 주장·캡션·provenance·피니싱은 [10 근거](10-evidence.md)·[24 제작 실행](24-production-execution.md)·[23 피니싱](23-finishing-platform.md)에 연결한다. 브리프가 활성화한 분기만 열며 새 계약/템플릿을 만들지 않는다.

| 계열 | 기존 오너 계약 및 분기 |
|---|---|
| A01 카피→행동/명제 | [16 콘셉트](16-concept-emotion-retention.md), [09 편집](09-edit.md) |
| A02 속성→세계/재질; A03 형태·행동 대응 | [19 제품](19-brand-product-integration.md), [20 비주얼 SSOT](20-visual-mode-ssot.md), [21 합성 QA](21-generated-video-qa-retry.md) |
| A04 재질/제품/접촉 상태 | [26 상태](26-state-causality-continuity.md), [19 제품](19-brand-product-integration.md), [21 모션 QA](21-generated-video-qa-retry.md) |
| A05 공간/서비스 동선; A08 POV/스케일 전환/복귀 | [06 샷](06-shots.md), [카메라 공간 설계](../../camera-spatial-design/SKILL.md), [20 비주얼 SSOT](20-visual-mode-ssot.md) |
| A06 차량/지면/접촉; A11 조명/반사 | [21 모션·합성 QA](21-generated-video-qa-retry.md), [26 상태](26-state-causality-continuity.md), [07 조명](07-lighting.md), [19 제품](19-brand-product-integration.md) |
| A07 인물/관계/반응 | [04 연기](04-performance.md), [06 샷](06-shots.md); [17 장르·코미디](17-genre-comedy.md)는 브리프가 해당 기대·반응·마무리를 실제로 요구할 때만 |
| A09 주장/근거/수신자; A10 선언된 제작/리마스터/후반작업; A12 인셋 위계/스케일 | [10 근거](10-evidence.md), [24 제작 실행](24-production-execution.md), [06 샷](06-shots.md), [09 편집](09-edit.md), [23 피니싱](23-finishing-platform.md) |

해당 조건이 있는 경우에만 기존 오너 계약 안에서 다음 하위 레시피를 적용한다: 카피→행동 타이밍(A01b, 09), 장난감/성인 카피 재구성(A07a, 06/20), 기대 위반→목격자 반응(A08a, 04/06), POV 스케일 전환과 portal(A08b, 06/20/카메라 공간 설계), 카테고리 은유와 입증된 출처의 구분(A09a, 10), 시간 미지정 수사문과 실제 발화의 구분(A09b, 09/10), 라이프스타일 대리 표현과 장소/서비스 근거의 구분(A07b, 10/20), 후반 카테고리 개그와 아동/보호자/관객 권리 검토(A09c, 10/20), 표면·의미 대응(A12a, 19/21), 바퀴의 시간적 aliasing(A06a, 21), 지형 질감→제품 공개(A02a, 06/19), 목격자/원인 대상 반응 사다리(A07c, 04/06), 오퍼 홀드→선택적 코다→마지막 브랜드 초기화(A09d, 09/23), 선언된 스펙터클→안전한 제품 클로즈(A11b, 07/19/21). 각 레시피는 해당 브리프 조건이 성립할 때만 켠다; 조건 자체가 주장·CTA·장면·샷 수·에셋 ID·실행 승인을 새로 요구하지 않는다.

### 브리프에 원리를 옮기는 산출물

분석에서 제작 브리프로 실제 action/edit/state handoff가 요청되면, 위 교차표에서 활성화된 오너 절차만 열고 각 오너의 기존 템플릿 필드를 그대로 채운다. `assets/product-ssot-template.md`의 제품 필드, `assets/state-transition-template.md`의 대상·시작/끝 상태·원인 동작·후속 유지 행, `assets/motion-beat-template.md`의 모션 행, `assets/06-shots-template.md`의 shot/cue 열, `assets/09-edit-template.md`의 cut/time/cue 열, `assets/10-evidence-template.md`의 claim/source/limitation 열을 해당할 때 연결한다. 필드명을 임의로 번역·합성해 새 alias를 만들지 않으며, 조건이 없거나 입력이 미정인 행은 기존 `N/A`/미확인 표기를 사용하고 이유를 쓴다. 제안 타이밍은 shot-local cue와 final timeline 시간을 구분한다. text-only 계획은 실제 접촉·재생·청취·렌더·승인을 입증하지 않는다.
저장된 사례집은 선택적 출처 근거·provenance다. 정책·절차의 정본이나 필수 조회 경로가 아니다. 사용자가 저장 관찰 또는 그 provenance를 요청할 때 참고하며, 일반 레퍼런스 분석·새 브리프 적용은 사례집 없이 기존 분석/오너 절차로 수행한다. 사례가 없거나 출처 본문에 접근할 수 없으면 그 범위만 미확인으로 남긴다.
각 필드를 연결하기 전에 인용한 오너 템플릿에서 그 필드의 실제 존재와 소속을 확인한다. 한 오너의 여러 템플릿이 교차표에 함께 적혀 있어도 필드를 임의로 다른 템플릿의 소유로 돌리지 말고, 해당 템플릿 경로와 필드를 짝지어 적는다.

## 분석 축과 증거 상태

해당하는 것만 다섯 축에서 골라 채운다 — 편집/리듬/공개 순서 · 샷/구도/카메라 · 비주얼 스타일 · 사운드 · 서사/감정 효과. 축마다 **관찰**(직접 확인한 프레임·재생·청취 또는 출처를 밝힌 사용자 관찰 기록), **해석/추정**(관찰에서 유도한 의도·기능), **미확인**(범위 밖·권리·성과)을 분리한다. 사용자 기록을 직접 검사로 표현하지 않는다. 확인할 수 없는 타임코드·오디오 내용·재사용 권리·성과 수치를 만들지 않고, 점수나 자동 합격 판정을 붙이지 않는다.

## Shot DNA 필드 (중요한 것만 채운다)

shot_id/근사 또는 측정 시간 · 서사 기능 · 피사체/행동의 시작-정점-끝 · 샷 크기/앵글 · 카메라 무빙/동기 · 조명/색 · 컷/전환 · 음악/효과 큐와 동기점 · 연속성 · 관찰/추정 구분 · (다중 시점 대응·정확한 재현 요구 시) 같은 특징 대응과 광학 역추정 근거 — 아래 "시점 대응과 광학 역추정" 절

`assets/shot-dna-template.md`의 리포트 구조를 쓴다(해당하는 표만 채운다).

## 시점 대응과 광학 역추정 (해당할 때만)

레퍼런스가 같은 대상·구조를 둘 이상의 시점(앞/뒤/측면, 다른 각도·거리)에서 보여주거나, 브리프가 특정 구도·공간·광학 느낌의 정확한 재현을 요구할 때만 적용한다. 해당하지 않으면 `N/A`로 닫고 분위기 참조만으로 이 절차를 채우지 않는다.

**같은 특징의 시점 대응.** 시점 사이에서 같은 특징만 짝짓는다 — 같은 얼굴·면·바느질·개구부·접촉점처럼 대응이 성립하는 특징을 연결하고 각 쌍에 `관찰 / 가림 / 미확인`을 표시한다. 가려져서 안 보이는 특징을 없다고 단정하거나 형상 변화·복원으로 해석하지 않는다. 가림 전 마지막 관측과 재등장 시점의 관측을 구분해 기록하고, 재등장하지 않으면 미확인으로 남긴다. 가림 때문에 안 보이는 면의 특징을 다른 시점 관찰 없이 만들지 않는다.

**광학 역추정(정확한 재현 요구 시).** 소실점·지평선 높이·피사체의 화면 대비 크기·보이는 면의 수·가장자리 왜곡·상대 크기 관계를 화면 정규화 기준점으로 표현한다. 실제 픽셀 대응값이 있으면 출력 크기와 함께 보존한다. 정규화가 크롭·왜곡까지 제거하지는 않는다. 알려진 크롭·출력 화면비는 제약으로 기록하고, 크롭 여부가 미확인이면 그 사실을 명시한다. 각 항목을 **관찰**(프레임에서 직접 읽은 값)/**추정**(관찰에서 유도한 가설)/**미확인**(스케일·기기·위치 정보 부재)으로 분리한다.

한 프레임과 물체 크기 미상 조건에서 카메라 해는 단일이 아니다 — 여러 초점거리·거리·크롭 조합이 같은 화면을 만들 수 있다. 물리 렌즈·센서·거리의 확정값을 만들지 않고, 관측과 양립하는 **후보 범위**와 그 근거를 적는다(예: 압축된 원근은 긴 초점거리+먼 거리 조합과 크롭 모두와 양립). 후보 사이를 실제로 가르는 관측이 무엇인지(민감도)와 반증·확정에 필요한 추가 증거(다른 시점 프레임·파랄랙스·EXIF/제작 기록·알려진 크기의 기준 물체)를 함께 기록한다. 새 제작으로 넘기는 목표는 확정 카메라 값이 아니라 관찰된 화면 특성(원근 압축·심도·왜곡·피사체 화면 대비)이다.

수치 카메라·공간 명세의 설계와 실행은 `$camera-spatial-design`이 담당한다 — 여기서는 역추정의 근거와 불확실성만 기록해 넘긴다. 대응표와 역추정 제약은 [상태·인과·연속성 인계](26-state-causality-continuity.md)의 시점 대응·역추정 근거 슬롯으로 이어 줄 수 있다.


## 아카이브 일괄 분석

폴더/아카이브의 전수 영상 분석 또는 포트폴리오 갭 검토는 단일 레퍼런스 분석과 구분한다. 요청된 영상 범위만 읽고, 요청이 분석이면 원본 수정·외부 업로드·생성·게시 없이 분석한다.

1. 영상 파일을 전부 열거하고 사용자 제공 게시물 ID/캡션과 파일을 연결한다. 발견·요청·실제 분석한 개수를 분리하고, 열 수 없는 파일은 미분석으로 남긴다. 게시물 캡션은 영상 프레임의 관찰로 취급하지 않는다.
2. 각 영상을 개별 항목으로 다룬다. 길이·프레임 크기·화면비·알려진 스트림 메타데이터와 실제 확인한 시각/구간을 `assets/archive-audit-template.md`에 기록한다. 아카이브 요청이면 템플릿의 source별 coverage ledger에 안정된 archive_id(순번 아님)·정확한 파일명·evidence locator와 mode별 개수·정확 구간·timestamp 완전성을 기록하고, decode/locator·추출/실제 시각검토·연속 재생·오디오 청취를 분리한다. 전체 decode나 contact sheet 확인만으로 full temporal analysis라 하지 않는다. 의미 있는 비트는 `assets/shot-dna-template.md`에 연결한다.
3. 각 영상별 직접 관찰·사용자/게시 메타데이터·해석·미확인을 구분한다. 표본 프레임만 본 경우 전체 순서·컷 리듬·모션을 확정하지 않는다. 오디오 스트림 정보만으로 실제 대사·음악·효과음·품질을 주장하지 않는다.
4. 영상별 분해가 끝난 뒤 반복·대조 패턴을 집계한다. 해당 패턴을 뒷받침하는 파일 수와 실제 확인 범위를 함께 적고, 조회수·유지율·전환 데이터가 없으면 성과 판단으로 확장하지 않는다.
5. 각 갭 후보를 현재 스킬의 정확한 참조/절차와 대조해 `이미 커버`, `부분 커버`, `갭 후보`, `증거 부족`으로 분류한다. 누락된 키워드만으로 기능이 없다고 판단하지 않는다.
6. 실제 갭만 수정 후보로 제안하고 기존 절차의 중복 복사를 피한다. 미확인 영상에서의 부재·캡션 불일치·권리 문제를 확정하지 않는다.
7. 사용자가 명시적으로 **전수 all-source/all-shot 분석** 또는 **cross-source craft extraction**을 요청한 경우에만 `assets/archive-craft-crosswalk-template.md`를 REQUIRED로 작성한다. 이는 archive audit 및 shot DNA에 추가되는 관계형 join이며, 각 source occurrence→sequence/scene→shot/boundary→within-shot event→craft finding→기존 owner→target-specific observable QA를 연결하고 미완료 source rows/open gates를 명시한다. 인용 ID는 occurrence/sequence/scene/shot/event/candidate 모두 원문 그대로 전체를 쓰고, `…`·잘림·재생성 alias를 금한다. Detector candidate, confirmed hard cut, soft transition, shot boundary 및 within-shot event를 구별한다. 각 completed finding은 `assets/shot-dna-template.md`의 `이전 체인` 필드 `레퍼런스 증거(관찰+위치)`→`메커니즘`→`의도 효과(해석)`(대안 포함)→`새 브리프 제작 요구`→`정성 검증 기준`에 매핑하고, 적용 가능한 기존 receiving-owner template field(s)와 정확한 QA slot을 해당 owner 파일의 명칭 그대로 쓴다. 관련 owner 열만 포함하고 새 필드/alias를 만들지 않는다. 표기와 체인 모두 기존 템플릿과 대조하는 마지막 row-completeness check에 통과한 finding만 retrievable이다. 누락·미검토 범위는 zero findings가 아니다. 일반/단일 레퍼런스 분석에서는 이 crosswalk를 요구하지 않는다.

## 재사용 규칙 추출

"정확히 이 산과 의상을 쓴다"보다 "얼굴 클로즈업에서 극와이드로 잘라 규모를 드러낸다" 같은 규칙을 우선한다. 오프닝 문법·에스컬레이션 패턴·보상 문법·마무리 문법을 구분해 추출한다.

**이전 가능 메커니즘**(구조 논리·타이밍 관계·공개 순서)과 **보호 표현**(캐릭터·브랜드·특정 디자인·대사·음악)을 분리하고, 메커니즘만 사용자의 새 브리프에 구체적으로 맞춘다. 각 제안은 추적 가능한 체인으로 적는다: 레퍼런스 증거(관찰 + 위치) → 메커니즘 → 의도 효과(해석으로 표기, 대안 포함) → 새 브리프의 제작 요구 → 정성 검증 기준. 아카이브 crosswalk finding은 `assets/shot-dna-template.md`의 `이전 체인` 필드명을 그대로 사용해 이 순서를 매핑하고, 적용 가능한 receiving-owner template field(s)와 정확한 QA slot도 해당 owner 파일의 실제 명칭으로 적는다; 관련 owner 열만 연결하고 새 field/alias는 만들지 않는다. 제안 타이밍은 측정한 원본 시간과 구별해 표기하고, 실제 산출물·샷·패널 ID는 이후 담당 단계가 붙인다 — 이 분석/감사 단계에서 확정 ID를 만들지 않는다. 분석이나 템플릿은 생성·제작을 승인하지 않는다.
Each completed crosswalk handoff MUST separately name and represent all five existing Shot-DNA `이전 체인` fields—`레퍼런스 증거(관찰+위치)`, `메커니즘`, `의도 효과(해석)`, `새 브리프 제작 요구`, `정성 검증 기준`—rather than leaving any mapping implicit in a combined explanation. Use the existing handoff/template structure; add no fields or schema.

06 shot-planning handoffs always name the existing target identity/time fields `shot_id`, `scene_id`, `beat_id`, and `shot-local time (s or frames; FPS if frames)`, plus every applicable existing 06 creative/QA field. For an approach/response/contact-state finding, applicable fields include `크기/카메라 위치`, `인물 블로킹`, `시선/축`, `공개 정보`, `관점·감정/구도 의도`, `대안·채택/승인 상태`, and `종료 프레임`. Apply this field mapping only when 06 is the receiving owner; for other owners, use only their applicable existing fields. Add no schema or aliases.

레퍼런스 요약 · 분석 범위와 측정/근사 구분 · 샷/비트 DNA 표 · 동작·카메라·컷·소리의 타임라인 관계 · 반복 시각·청각 문법 · 숨은 제작 요구 · 이전 체인 표 · 복제하면 안 되는 요소 · 권장 하위 라우팅. 아카이브 분석은 인벤토리·영상별 관찰 범위·교차 영상 스킬 커버리지/갭 표를 함께 낸다.

### 명시적 skillification 요청만 기존 오너 절차를 갱신

일반 분석·요약·새 브리프 적용은 스킬 파일을 수정하지 않는다. 사용자가 기존 스킬의 명시적 skillification/update를 요청한 경우에만 다음 순서를 수행한다:

1. 분석 가능한 아카이브 범위에서 반복·대조 패턴을 종합하고 관찰·해석·미확인과 coverage를 분리한다. 표본/접근 한계를 넘어서는 archive-wide 주장을 하지 않는다.
2. 각 이전 가능 패턴마다 관련 기존 오너의 전체 절차, 실제 템플릿 필드, QA 기준을 대조한다. 이미 커버/부분 커버/갭 후보/증거 부족을 구분하고, 무관한 오너도 범위에서 닫는다.
3. 실제로 입증된 일반 절차 또는 QA 공백만 그 패턴의 정본 오너에 최소 반영한다. 이미 있는 06/08/09/21 또는 전문 카메라 절차를 복사하지 않고, 새 스키마·중복 policy/casebank rule을 만들지 않는다. 근거가 불충분하면 변경 대신 제한을 보고한다.
4. 저장 사례집은 선택적 provenance/evidence로 남긴다. 새 오너 절차는 추출된 원리만 말하며 사례 ID·Rofan 검색·특정 사례 선조회에 의존하지 않는다.

이전 가능한 것은 추상화된 제작 메커니즘뿐이다. 줄거리/사건, 인물·관계, 장소/세트, 소품·의상·제품 디자인, 고유한 샷 배열/안무, 원본의 절대 타이밍을 복사하거나 새 정책으로 일반화하지 않는다. 새 작업의 타이밍과 장면은 새 brief와 실제 오너 절차로 설계한다.

외부 source root 또는 상세 ledger가 부분적으로 접근 불가하거나 materialization이 불완전하면, 실제 읽은 manifest·ledger와 미검사 media를 구분해 기록하고 남은 bounded evidence만 평가한다. 불완전한 표본을 전수 분석으로 표현하지 않고, source-derived skill update가 근거 없으면 수행하지 않는다. Ledger를 읽었다는 사실은 영상 playback/full decode, source별 완결성, 전체 shot coverage를 뜻하지 않는다.

## 출력 형태

일반 분석·질의·텍스트 요청은 결과를 텍스트로 낸다. project.json·타임라인·폴더·미디어 자리를 만들지 않고, 스킬 파일을 쓰거나 갱신하지 않는다. 예외는 사용자가 기존 스킬의 skillification/update를 명시적으로 요청한 경우뿐이며, 위 절차에 따라 증거가 확인된 기존 오너 공백만 변경한다. 패턴으로 자동 개선하지 않는다. 실제 제작 단계로 넘길 때만 담당 모듈이 산출물을 만든다. 분석/템플릿은 생성·제작을 승인하지 않는다.

## 근거와 적용 범위

관찰 등급·coverage·이전 체인·crosswalk·ID/권리/승인 구분은 패키지의 분석 운영 설계다. source-derived 발견은 실제로 검사한 원본 locator에만 귀속하며, 저장 원장 읽기는 원본 재생/청취가 아니다.

**단일 프레임 역추정의 기술 근거:** E7이 [OpenCV 4.13.0 Camera Calibration and 3D Reconstruction](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html)의 `Detailed Description` 중 pinhole 투영식·`Homogeneous Coordinates`·`Intrinsic parameters from camera lens specifications`를 직접 읽었다(2026-10-17, READ-PARTIAL; live Markdown content-negotiated rendition, SHA-256/bytes=`N/A-live-web`). `u=f_x X_c/Z_c+c_x`, `v=f_y Y_c/Z_c+c_y`와 동일 광선 위 점의 같은 투영은 깊이/스케일 미확정의 근거다. 물리 초점거리 환산에는 센서/픽셀 크기가 필요하다. 미지 형상·미지 센서/크롭 조건에서 단일 프레임만으로 물리 렌즈/거리/크롭을 유일 확정하지 않는다는 결론은 이 식의 적용 추론이며, 알려진 형상·보정값을 제공한 pose solve까지 불가능하다는 뜻이 아니다.

정규화 기준점은 해상도에 독립적인 **표현**이지 원본 크롭/왜곡에 불변인 측정이 아니다. 알려진 이미지 크기/크롭 변환을 보존하고, 실제 픽셀 대응이 있으면 그 값·출력 크기도 함께 넘긴다. 원근 압축의 느낌만으로 긴 렌즈와 크롭을 판별하거나 배경 깊이까지 같다고 추정하지 않는다. 이 문서는 렌즈 호흡·rolling shutter·심도 또는 임의 생성 영상의 물리 카메라 존재를 입증하지 않는다. 수치 설계/실행은 기존 카메라 소유자가 맡고 실제 클립 근거와 추론은 계속 분리한다([지원 경계](sources.md#모듈별-지원-경계)).
