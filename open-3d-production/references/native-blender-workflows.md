# 콘텐츠 제작용 네이티브 Blender 방법

배정된 결과에 맞는 절만 읽는다. 소유자는 기존 `open-3d-production`, 장면별 공간 검증은 `camera-spatial-design`/`blender-previsualization`이다. 이 문서는 새 실행기·애드온·proxy adapter 옵션이 아니라 **직접 저작할 native 작업 절차**다. 단독 계획은 텍스트로 끝내고, 실제 제작은 요청된 `.blend`·렌더·내보내기만 수행한다.

## 공통 실행 계약

1. 원본 자산·치수 근거·shot/scene/panel ID·카메라 버전·승인 범위를 이어받는다. Blender 버전/엔진, 단위, color management, fps/fps_base, 프레임 범위, 해상도·출력 형식과 목적지를 기록한다.
2. 원본 `.blend`를 보존하고 독립 복사본/프로세스와 새 출력 폴더에서 작업한다. 필요한 프레임·구도에 충분한 blockout을 먼저 검사한다. 이름·controls·seed를 보존해 수정 가능하게 만든다.
3. 작은 native 미리보기 → 실제 요청 출력 → 저장본 재열기 → 요청된 각도/구간 검사 순서로 진행한다. 정지 프레임과 움직임/루프 검증을 구분한다. Blender가 없으면 해당 native 출력만 BLOCKED로 보고한다.
4. 결과 파일·실제 설정·검사 시각·결함·미검증을 기존 오너에게 반환한다. 프로젝트/.history는 기존 writer만 갱신한다. 웹 렌더·유료 생성·오디오·추가 설치는 자동으로 붙이지 않는다.

**근거:** [source register](blender-source-register.md)의 S01–S25. 공식 문서는 **4.5 기준선**이며 최신 버전 주장이나 로컬 호환 테스트가 아니다. 실행할 때 현재 버전에서 필요한 API/노드/엔진을 확인한다. 설치된 런타임이 다르면 문서 기준선과 차이를 기록한다.

## B01. 제품 조명과 반복 가능한 스튜디오

**사용:** 제품의 외곽·표면·반사를 읽히게 하는 광고/설명용 장면. 입력은 실제 제품 스케일·재질·hero camera·배경 목표와 output 규격이다.

1. 제품/배경 collection과 key/fill/rim 역할의 named light를 분리한다. 역할은 출발점이며 모든 컷에 세 조명을 강제하지 않는다.
2. 각 광원을 따로 켜 제품 곡면·로고 가독성·하이라이트를 확인한다. area light 크기·거리·형태와 Normalize 상태를 기록하고, fill은 필요한 암부만 복원한다. 광원 거리만으로 부드러움을 단정하지 않는다.
3. 필요할 때만 receiver/blocker collection과 light linking을 사용해 제품/배경의 영향을 분리한다. 차광판과 반사판은 실제 광학 효과로 검사한다.
4. 위치/방향/세기/색온도·노출을 named control로 유지한다. 특정 유료 procedural-lighting 상품 없이도 native light/empty/collection으로 재사용 구조를 작성할 수 있다.
5. 후반 조정이 배정되면 Cycles Light Groups를 별도 출력하고 합친 결과를 기본 Combined와 비교한다. light linking과 light group은 다른 기능이다.

**완료:** 저장 가능한 rig, 실제 제품/배경의 반사·윤곽·의도한 receiver 검사, 출력/색 관리 기록. light-group 재조합은 이미 렌더된 기여도 조정이지 새 그림자 방향 생성이 아니다. 근거 S01/S02/S13/S21; 추가 제작자 자막 YT05의 조명 분리 원리를 사용했으며 상품/효과 주장은 제외했다.

## B02. 반복 배치와 파라미터형 모델

**사용:** 제품 배열, 패키지 변형, 부품·재료·환경 반복 배치.

1. 실제 source object/collection과 origin·scale·단위를 확인한다. 원본 리그/애니메이션을 무조건 apply하지 않고 Object Info/변환 공간을 먼저 판단한다.
2. surface 분포가 필요하면 `Distribute Points on Faces`, 규칙 배치라면 목적에 맞는 point/curve source를 사용한다. `Instance on Points`에 source를 연결하고 필요한 기본 geometry만 `Join Geometry`로 합친다.
3. count/spacing/selection/scale/rotation/seed를 노출한다. 무작위 회전은 축별 vector, 균일 크기는 같은 축 배율을 유지하는 scalar 등 의도한 변형을 택한다. 반복 생성 시 seed와 instance identity를 고정한다.
4. transform 수정 동안 instance를 유지한다. 실제 mesh 편집/내보내기가 요구하는 부분만 `Realize Instances` 한다. Repeat Zone은 한 번 평가 안의 반복 구성에만 쓴다.
5. 최종 카메라와 몇 개 다른 방향에서 겹침·균일성·중첩 transform·재질을 확인한다. 산출물은 editable node group과 요청된 결과다.

**완료:** controls/seed/source 기록, 작은/큰 parameter 사례 검사, realize 전후 모양·성능 영향 확인. 반복이 빠르다는 일반 보장이나 물리적으로 올바른 분포 주장은 하지 않는다. 근거 S03–S05/S24; YT11 자막의 분포→인스턴스→원본 geometry 결합 원리를 일반화했다.

## B03. Geometry Nodes 모션그래픽

아래는 Geometry Nodes 경로다. 배정된 구현이 native `bpy` mesh/shape-key/F-Curve 경로라면 같은 시간·phase·seed 계약을 쓰되 실제 메커니즘을 기록한다. 임의 프레임 재요청과 `.blend` 재열기가 같은 상태를 내는지 검사하고, 그 성공을 Geometry Nodes graph 자체의 검증으로 바꾸지 않는다.

**사용:** 제품 파도·지연 등장·궤도·반복형 그래픽처럼 매 시각의 상태를 직접 계산할 수 있는 동작.

1. Scene Time seconds와 시작/period를 기준으로 phase를 만든다. 예: `2*pi*(seconds-start)/period`; per-instance offset은 고정 ID와 연결한다. 프레임 고정 타이밍이 목적일 때만 frame 값을 쓴다.
2. phase를 sin/cos·임계/지연·curve mapping 등 의도한 transform에 연결한다. 각 속성이 무엇을 바꾸는지 이름으로 노출하고 원치 않는 random flicker를 제거한다.
3. 이전 프레임이 필요 없는 동작은 analytic하게 작성한다. Simulation Zone은 누적·성장·궤적처럼 실제 이전 상태가 필요할 때만 선택하고, rate 업데이트는 Delta Time을 고려한다.
4. simulation이면 상태 attribute·초기화·warm-up·bake 범위/버전을 기록한다. 비순차 프레임 렌더 전 cache/bake 조건을 확인한다. Repeat Zone을 시간 누적이나 loop 재생으로 오인하지 않는다.
5. 프레임 순서를 달리 요청해 같은 시점이 같은지, motion blur가 필요한 경우 subframe에서도 동작이 일관적인지 검사한다.

**완료:** node controls·fps/time basis·seed·cache 상태와 검사한 시각. periodic transform 하나만으로 전체 장면의 seamless loop를 판정하지 않는다(B08). 근거 S03/S05–S07/S17/S25.

## B04. 실사 플레이트 카메라 트래킹과 CG 배치

**사용:** 실제 촬영 영상의 카메라를 풀어 CG를 공간에 고정해야 할 때. 눈대중 프리비즈 복제와 다른 작업이다.

1. footage 원본·프레임 범위·fps·해상도·렌즈/왜곡 정보와 알려진 실측을 확보한다. 해상도/크롭/리타이밍 변경은 tracking 근거에도 반영한다.
2. 화면 전역·가능하면 여러 깊이의 정지 특징을 추적한다. 움직이는 인물/반사/흐린 점을 카메라 고정 특징으로 쓰지 않는다.
3. 실제 track를 scrub/재생해 튐·미끄러짐을 찾고, 분포/지속 구간을 보존하며 잘못된 track만 정리한다. 숫자를 낮추려고 좋은 track를 무작정 삭제하지 않는다.
4. translation/parallax와 회전 위주 tripod 상황을 구분하고 합리적인 intrinsics/keyframe으로 solve한다. floor/origin/axis/scale은 근거를 기록하며, 추정 scale을 실측으로 바꾸지 않는다.
5. Camera Solver 또는 명시적 bake로 카메라를 연결하고 테스트 geometry가 전 구간에서 지면/특징에 붙는지 확인한다. 중앙뿐 아니라 화면 가장자리·가림 변화도 검사한다.
6. 최종 합성의 undistort/redistort 순서·렌더 카메라·크롭을 명시한다. 튜토리얼의 특정 왜곡 toggle이나 color-management 선택을 그대로 복사하지 않는다.

**완료:** tracking clip/solve 버전·잔차·scale 근거·실제 등록 검사. 낮은 solve error만으로 정확한 카메라·metric reconstruction을 보장하지 않는다. 근거 S08/S09; YT17 자막의 track 정리→solve→orientation→test-object 검사를 보완했다.

## B05. 이미지 투영과 제한된 2.5D 카메라

**사용:** 한 장의 배경/그림을 단순 geometry에 투영해 짧고 제한된 시차를 얻을 때. 카메라 solve나 미관측 공간 복원이 아니다.

1. 원본 이미지·aspect·crop과 재사용할 projector camera를 고정한다. target geometry와 사용할 UV map을 지정한다.
2. UV Project에 projector를 연결하고 negative-Z 투영 방향, perspective/orthographic 모드와 종횡비를 확인한다.
3. viewer camera를 별도로 두고 허용할 이동 범위를 작은 preview로 정한다. projector 뒤 geometry, 측면 늘어짐·빈 영역·투영 경계가 드러나는 시각을 찾는다.
4. 허용 범위를 줄이거나 공급된 추가 면/배경 geometry로 보완한다. 없는 후면을 정확 재현했다고 주장하지 않는다.

**완료:** projector/UV/viewer camera 이름, 실제 요청 이동의 전체 구간 검사와 허용 한계. matte-painting 사례 C01의 접근하지 못한 본문은 구현 근거가 아니다. 근거 S10.

## B06. Grease Pencil 하이브리드 콘티·Line Art

**사용:** 공간 blockout 위의 표정/동작 스케치, 설명선, 제품 윤곽, 2D/3D 혼합 animatic.

1. 2D template인지 3D 장면 위 stroke인지 선택하고 drawing plane·layer·material·카메라를 기록한다. 기존 3D layout/shot IDs를 이어받는다.
2. 수작업 stroke와 자동 Line Art를 분리한다. Line Art source를 scene/collection/object 중 필요한 범위로 좁히고 active/custom camera와 clipping/overscan을 지정한다.
3. 카메라·geometry를 확정한 뒤 필요한 범위만 bake한다. bake 지우기가 수작업 stroke를 함께 제거하지 않도록 layer/복사본을 분리한다.
4. 움직임과 함께 line popping·가림·프레임 끝 단절·읽기 크기를 확인한다. 별도 후반이 필요할 때만 Grease Pencil pass를 출력한다.

**완료:** editable `.blend`, 요청된 그림/sequence와 bake 상태. 구버전 Grease Pencil Python/UI를 현행 계약으로 가정하지 않는다. 분리 pass의 blend mode에 따라 Combined와 합성 결과가 다를 수 있다. 근거 S11–S13/S22.

## B07. 패스·마스크·알파 합성

**사용:** 후반에서 제품/배경/조명을 따로 조절하거나 투명 element를 납품할 때.

1. 용도에 맞는 Combined·Depth/Normal·Cryptomatte·AOV·Light Group만 선택한다. 엔진별 지원과 AA/투명/blur 한계를 확인한다.
2. 배경 제거는 Film Transparent, 유리 처리·그림자 수집은 별도 설정으로 다룬다. 필요한 plate integration에만 실제 engine-supported shadow catcher를 작성한다.
3. File Output으로 beauty/element/mask의 경로·프레임 규칙을 명시한다. RGBA/EXR 등의 선택은 요구 채널·bit depth·색 공간에 맞추고, 파일 확장자만으로 alpha 보존을 가정하지 않는다.
4. premultiplied/straight alpha를 handoff에 기록한다. straight 연산이 필요하면 명시적으로 변환하고 합성 출력이 요구하는 형태로 되돌린다.
5. 밝은/어두운/브랜드 배경에 얹어 halo·검은 테두리·유리·motion-blur 가장자리를 검사하고 Combined와 대조한다. object color ID와 segmentation/Cryptomatte를 혼동하지 않는다.

**완료:** 실제 채널/시퀀스·alpha convention·컴포지터 재열기와 edge 검사. 패스 생성은 모델이 그 입력을 지원한다는 증거가 아니다. 근거 S13–S16/S20.

## B08. 루프와 turntable

**사용:** 반복 재생되는 제품·기계·모션그래픽.

1. 한 period의 실제 길이/fps/고유 프레임 수와 정지 루프·이동 offset 루프 여부를 잠근다.
2. 기존 keyframe은 Cycles F-Curve modifier의 repeat/offset/mirrored 의도를 선택한다. modifier 순서를 확인한다. 절차적 움직임은 B03의 phase를 쓴다.
3. 동일 endpoint를 두 번 납품해 정지하는 것을 피하도록 출력 범위를 정한다. 예: N개 고유 프레임을 쓰는 규약이면 등가 endpoint는 검사용으로만 만들 수 있다. 실제 번호는 장면 시작 프레임을 따른다.
4. 최종 encoded clip을 연속 두 번 이어 보며 last→first 위치·속도·카메라·조명·재질/noise phase·그림자·입자 lifecycle을 검사한다.
5. stateful simulation은 warm-up/초기 state와 recurrence를 별도 설계한다. 단순 crossfade는 진짜 상태 루프나 원본 보존의 증거가 아니다.

**완료:** editable cycle/phase, 실제 sequence/clip과 wrap 시각 검사. 값의 일치만으로 속도·가속도/전체 scene loop가 보장되지 않는다. 근거 S06/S07/S17/S25.

## B09. 재사용 에셋·조명·노드 변형

**사용:** 브랜드 반복 제작에서 제품·재질·조명·generator를 재사용할 때.

1. source `.blend`와 published deliverable을 나누고 scale/origin/재질·이름·노출 controls를 정리한다.
2. 재사용할 data-block만 Mark as Asset하고 source를 등록된 asset library에 저장한다. Mark as Asset만으로 library에 복사된다고 가정하지 않는다.
3. catalog/설명·미리보기·원본 버전과 필요한 외부 texture를 함께 관리한다. 기존 object/asset ID를 보존하고 새 변형은 허용 delta만 노출한다.
4. 새 작업 파일에서 불러와 변형해 보며 경로 누락·scale·node dependency·linked/local 변경 범위를 확인한다.

**완료:** saved library source·catalog·의존성, 실제 새 파일에서 사용 확인. 제작사 custom pipeline 전체나 prototype code를 무단 필수화하지 않는다. 근거 S18/S23.

## B10. GLB/웹·편집 핸드오프

**사용:** 네이티브 장면에서 web/game asset 또는 후반용 렌더를 전달할 때.

1. 목적지가 editable `.blend`, render sequence, GLB/glTF 중 무엇인지 잠근다. 내부 rig/참조 object/work-in-progress를 export scope에서 분리한다.
2. 지원 재질·transform/bone/shape-key animation과 실제 action/track 범위를 확인한다. 임의 shader/physics/animated light가 동일하게 export된다고 하지 않는다.
3. curve 변환·instance realization은 exporter/목적지가 요구할 때만 수행하고 source는 보존한다. Geometry Nodes instance export의 experimental 상태와 대상 viewer extension을 확인한다.
4. actual export를 목적지에 다시 열어 scale/axis·재질·texture·hierarchy·animation names/ranges를 검사한다. 웹 작업이 배정된 경우에만 browser QA를 연결한다.

**완료:** editable source와 별도 published file, exporter 설정·실제 목적지 검사. glTF 설명서의 서로 다른 시기 action 규칙은 버전별로 검증한다. 네이티브 렌더·공간 검증·브라우저 렌더는 서로 대체 증거가 아니다. 근거 S19/S20/S23.

## 반환할 최소 작업 카드

기존 인계/제작 원장에 다음을 기록한다: `선택 B-ID / source IDs / 입력 파일·버전 / 실제 Blender·엔진 / 잠긴 카메라·타임베이스 / 바꾼 controls·seed·cache / 실제 출력 / 열어 본 뷰·구간 / 결함과 미검증`. 새 schema나 별도 승인 원장은 만들지 않는다.

YT05/YT11/YT17은 추가 조사에서 실제 읽은 제작자 자막의 ID다. 각각 `yPekIQMoKYM`(The Blenderender), `aO0eUnu0hO0`(Blender Guru), `ui0JUHE12k8`(Jacob Zirkle)이며, 2026-11-03 Flucto Markdown으로 읽었다. 화면/오디오를 검사한 것으로 표시하지 않는다. 기술적 계약은 S-ID의 공식 버전 문서와 현재 실행 환경이 우선한다.
