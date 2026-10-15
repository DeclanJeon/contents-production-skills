# First 24 raw-candidate 보충 검토 — 실제 native PTS 이웃 전수

## 범위와 완료 근거

- 대상은 기존 stable mapping의 **V001–V024**뿐이다. [기계 판독 ledger](raw-candidate-coverage-first24.json)에 원본 SHA-256, 각 raw event, native `n−2 / n / n+2`, 원본 정수 PTS·초, image·sheet·cell 및 실제 관찰 판정을 보존했다. `Vxxx/Rxxx`는 소스별 detector ID이지 장면/검증 샷/전역 DESIGN recipe ID가 아니다.
- **496 raw event / 1,468 unique native frames / 71 strips 전부 실제 이미지로 읽음.** frame reference는 496×3=1,488개이고 겹친 이웃/끝 clamp로 unique 수와 다르다. 같은 사건을 여러 raw 후보로 잡은 경우 그 수를 컷 수로 합산하지 않는다.
- 기존 first24 candidate manifest는 **463 review groups / 1,389 group-neighborhood frame samples**였다. raw center native frame이 기존 파일들에 있던 것은463건;33건의 center는 없었다. 이는 파일 내 frame 존재 측정이지 과거에 사람이 실제 읽었다는 검증이 아니다. 기존 uniform strips에 같은 사건이 있을 수도 있으므로 새 center 확보와 새 장면 발견도 구별한다.
- **FRAMES_REVIEWED**만 추가했다. 연속 playback·청취·새 ASR/caption은 수행하지 않았다. uniform timeline/첫·종단/creator provenance는 기존 ledger를 함께 사용한다. 이 보충 pass도 detector threshold가 놓친 모든 컷을 검증했다는 의미가 아니다. n±2는 모든 중간 프레임/물리적 움직임 연속성 보증이 아니다.
- ffprobe native-PTS dump24/24 rc=0, 성공 FFmpeg select24/24 rc=0. 성공 pass는 소스당1회이며 frame별 FFmpeg 호출이나 fps-grid timestamp 재라벨 없음. V002/V003/V021의 최초 left-deep expression allocation/parser 실패3건은 retained PTS를 재사용하여 **실패 select만** balanced expression으로 재시도했다. 성공한21개 select/24개 probe는 반복하지 않았다.
- script로 모든 raw timestamp/순서를 기존 mechanical candidate manifest와 대조, 모든 native n±2/PTS를 retained ffprobe dump와 대조, 모든 image/sheet 경로 존재, 각 소스의 최종 SHA-25624/24 일치를 확인했다. 기존 skills/code/설정/index/inventory/다른 작업자의 chapter는 수정하지 않았다.

## 소스별 결과

아래 cut은 **frame bracket에서 이미지 교체가 보이는 후보 판정**이다. verified edit count가 아니다. flash/morph도 실제 compositing/생성 pipeline을 인증하지 않는다.

| ID | raw / 이전 group | unique frames / 읽은 strips | 후보 판정 분포 | 실제 보충 관찰 / 기존 chapter 대비 |
|---|---:|---:|---|---|
| V001 | 13 / 13 | 39 / 2 | cut 13 | 수영장/얼굴/라운지/체인 가방의 서로 다른 이미지 교체를 재확인. 담배처럼 보이는 작은 소품의 용도·실제 흡연은 확인하지 않음. [strips](evidence/raw-review-V001/extraction-manifest.json) |
| V002 | 40 / 34 | 118 / 5 | flash 18, cut 18, morph 4 | 빠른 밝은 insert, 같은 runner/병실의 녹색 grade 변화, 둥근 aperture/얼굴 변형을 분리. 40 score event를 40개 장소/샷으로 복제하면 과대계수. [strips](evidence/raw-review-V002/extraction-manifest.json) |
| V003 | 49 / 45 | 145 / 7 | cut 46, flash 3 | 웅덩이 반사→검정→짧은 반사 복귀→검정 blink를 새로 분해. monochrome split/blur도 독립 장소로 세지 않음. [strips](evidence/raw-review-V003/extraction-manifest.json) |
| V004 | 15 / 15 | 45 / 2 | cut 14, flash 1 | TV/태블릿/폰/광고판의 화면 안 화면과 마지막 white glitch 재확인. color bars 위 glitch가 곧 기관 카드가 되는 것은 아님. [strips](evidence/raw-review-V004/extraction-manifest.json) |
| V005 | 2 / 2 | 6 / 1 | cut 2 | 브랜드/office→burger blur, 불의 FRUSH→검정 두 후보 재확인. 소유한 기존 chapter의 phase 내용을 바꿀 새 발견 없음. [strips](evidence/raw-review-V005/extraction-manifest.json) |
| V006 | 19 / 5 | 44 / 3 | cut 5, motion 14 | 19 raw 중 14는 동일 boots/도로 구도 내부 들기·접지·splash 변화. 기존 5개 group center만으로 모든 raw 검토 완료라 말할 수 없었던 구간을 실제 보충. [strips](evidence/raw-review-V006/extraction-manifest.json) |
| V007 | 6 / 6 | 18 / 1 | cut 6 | body-copy pre native PTS15.265250에서 UP TO 80% 직접 판독; 이전40% 기록 수정 전달. 할인 조건/실제 유효성은 별도 미검증. [strips](evidence/raw-review-V007/extraction-manifest.json) |
| V008 | 16 / 16 | 48 / 2 | cut 16 | Santa-like 군중/배송/카드/집/실내/마크 전환 재확인. 카드 뒤 coda도 별도 유지; 실제 배송/공식 캠페인 주장 아님. [strips](evidence/raw-review-V008/extraction-manifest.json) |
| V009 | 14 / 13 | 42 / 2 | cut 14 | 초반 검정/인물 및 blue-fashion shoe/box/brand 교체 재확인. 14raw와13group를 분리; lens/rig는 판정하지 않음. [strips](evidence/raw-review-V009/extraction-manifest.json) |
| V010 | 16 / 16 | 48 / 2 | unknown 7, cut 9 | 같은 분홍 set의 7개 abrupt pose/crop 변화는 unknown: same-set edit 또는 생성 불연속 대안. source PTS 54.467의 dark field, 54.584의 부분 glyph, 55초의 완전한 Dior wordmark-present 상태를 분리. [strips](evidence/raw-review-V010/extraction-manifest.json) |
| V011 | 15 / 15 | 45 / 2 | cut 14, motion 1 | 채소/튀김/빵/불/고기/burger 교체와 동일 fire/coal 내부 brightness 후보1개 분리. cooking montage가 안전한 조리 지시를 증명하지 않음. [strips](evidence/raw-review-V011/extraction-manifest.json) |
| V012 | 28 / 25 | 84 / 4 | cut 20, morph 4, unknown 1, flash 3 | badge→double-exposure person→single person, car scale overlap, purple-white logo bridge의 여러 raw 단계 분해. 동일 transition에서 얻은 여러 event는 여러 장면 수가 아님. [strips](evidence/raw-review-V012/extraction-manifest.json) |
| V013 | 3 / 3 | 9 / 1 | cut 3 | cloud car→다른 cloud field→cloud-hand/sky, overhead valley→road-axis 세 후보 재확인. 기존 소유 chapter의 환경-상태 phase와 정합. [strips](evidence/raw-review-V013/extraction-manifest.json) |
| V014 | 10 / 10 | 30 / 2 | cut 9, flash 1 | blue beam→plain track→blue glow bridge를 flash로 분리; 이후 surface/weather/sole/box 교체 재확인. 기존18B hierarchy 추가 수정 필요 없음. [strips](evidence/raw-review-V014/extraction-manifest.json) |
| V015 | 31 / 31 | 93 / 4 | cut 31 | party/용기/불/최종 blue-card 재확인. R029 한 수평 용기가 두 입을 연결하는 형태는 소비 행동/손-입-용기 QA counterexample이며 이전 chapter도 이미 기록. [strips](evidence/raw-review-V015/extraction-manifest.json) |
| V016 | 12 / 12 | 36 / 2 | motion 1, cut 11 | 첫 snowy aerial 후보는 동일 view 내부 motion, 뒤11개는 road/grille/water/mirror/wheel/lamp/credit 교체. 실제 VFX pipeline은 판단하지 않음. [strips](evidence/raw-review-V016/extraction-manifest.json) |
| V017 | 23 / 23 | 69 / 3 | cut 23 | dune/grain/buried SUV→grille/wordmark/검정 전환 재확인. LINCOLN 화면 브랜드; 실제 desert 주행 성능이나 촬영 방식 증명 아님. [strips](evidence/raw-review-V017/extraction-manifest.json) |
| V018 | 26 / 26 | 77 / 4 | cut 26 | face/surf/wave/horse/engine/car/red Ferrari card→검정 전환 재확인. source끝 post는 마지막 native frame으로 clamp; source technique는 미확인. [strips](evidence/raw-review-V018/extraction-manifest.json) |
| V019 | 25 / 20 | 73 / 4 | morph 1, cut 24 | 20 merged groups에 포함된25raw를 개별 복원. pink-model→shoe variants, white-group→red/white model→pastel group→black tracksuit가 이전 번호/행 내용과 어긋난 지점 전달. [strips](evidence/raw-review-V019/extraction-manifest.json) |
| V020 | 16 / 16 | 48 / 2 | cut 16 | 학생→친구→졸업→면접→무대→아이/태블릿→검정→white graphic field 재확인. 검정/흰 전환 center는 후속 copy/mark가 이미 보이는 시점이 아님. [strips](evidence/raw-review-V020/extraction-manifest.json) |
| V021 | 68 / 68 | 204 / 9 | cut 66, unknown 1, motion 1 | crop/상자/항공/시장/조리/식탁68raw 검토. CLEARED FOR IMPORT EU 추가 판독; chef-pot transfer는 motion, floating tomato 급변은 unknown. 마지막 아이의 pout→smile은 별도 행동 단계. [strips](evidence/raw-review-V021/extraction-manifest.json) |
| V022 | 24 / 24 | 72 / 3 | cut 24 | toy-scale driver에서 traffic/flight fantasy, adult driver, BIG BOY/BIG TOY, Audi card와 driving coda까지 재확인. imagined action과 실제 효능/안전 인증을 혼동하지 않음. [strips](evidence/raw-review-V022/extraction-manifest.json) |
| V023 | 11 / 11 | 33 / 2 | cut 11 | chef/dough→pizza layers→fries→burger→table/copy-facing gestures11raw 재확인. 기존 소유 chapter의 준비/분해/사회적 식탁 phase와 정합. [strips](evidence/raw-review-V023/extraction-manifest.json) |
| V024 | 14 / 14 | 42 / 2 | cut 14 | party/food/game/social group→Always delicious, always real→white icon field→검정 AI title14raw 재확인. food ad와 creator-disclosure tail을 분리 유지. [strips](evidence/raw-review-V024/extraction-manifest.json) |

합계: cut435 / flash26 / morph9 / motion17 / unknown9 =496 raw 판정. 이 수를 샷/장면/제작 recipe 수로 전용하지 않는다.

## 구체적 수정·새로 분해된 근거

### RC01 — V006: 고변화 boot action을 14개의 새 장면으로 오인하지 않기
이전19raw를5group centers로 묶고15frames만 추출했다. 새 [strip01–03](evidence/raw-review-V006/extraction-manifest.json)은 R001–R019 각각의 native 이웃을 보여준다. R004–R017은 같은 낮은 boot/도로 구도에서 들기, 발바닥 접근, 접지/물튀김의 화면 상태가 변한다. 이 범위의14 motion 판정은 새 장소/새 샷14개를 증명하지 않는다. **transfer:** action-state trace를 raw event에 붙이고 접지/물 반응/발 형태를 평가; 실제 낙하·충돌 시간이나 촬영 slow motion을 정지 이미지로 추정하지 않기.

### RC02 — V007: 가능한 원본 카피 판독을 생략하지 않기
R002 pre: source n366/PTS15.265250, [strip01 cell4](evidence/raw-review-V007/raw-strip-01.jpg), `UP TO 80%`. 이전40%와 다른 실제 글자다. peer에게 전달했고 chapter의 body/endcard copy 구분에 반영됨을 읽었다. 할인 적용 조건/기간 진위/실제 SKU는 화면 숫자만으로 검증되지 않는다. **QA:** body, endcard, 법률 고지의 숫자를 각각 판독해 claim SSOT와 대조.

### RC03 — V003: merged-center 아래 사라진 짧은 blink
raw R016 center n396/PTS16.5는 검정, R017/16.708333에는 웅덩이 반사가 잠깐 돌아오고 R018/16.791667에는 다시 검정. [strip02 cell22–24](evidence/raw-review-V003/raw-strip-02.jpg) 및 [strip03 cell1–6](evidence/raw-review-V003/raw-strip-03.jpg). 기존 chapter C16은 어두운 field만 묘사했다. 이 짧은 return을 장면 세 개로 늘리지 않고 transition 내부 세 상태로 유지한다. 실제 flash 길이는 이 점들의 차이만으로 확정하지 않는다.

### RC04 — V010: 같은 set 내부 jump와 wordmark reading state
R001/R004/R005/R006/R009/R012/R015는 같은 pink 모델/set이지만 native 근접 이웃에서 손·팔·crop이 급변해 same-set cut, 생성형 discontinuity 또는 빠른 행동 대안을 열었다. parallax가 없다는 반복 문장을 만들거나 연속 안무로 확정하지 않는다. R016 pre n3266/PTS 54.434는 pink 모델, center n3268/PTS 54.467와 post n3270/PTS 54.5는 dark bokeh이며 글자가 없다([strip02 cell22–24](evidence/raw-review-V010/raw-strip-02.jpg)). 원래 더 넓은 [C16 neighborhood](evidence/V010/candidate-neighborhood-sheets/neighborhood-008.jpg)의 pre n3261/PTS 54.350도 pink 모델이며, post n3275/PTS 54.584에서는 부분 흰 glyph가 이미 보인다. 이 index/PTS는 retained native dump에도 대조했다. 기존 source-PTS 55초 sample은 완전한 Dior 글자-present 상태다. 따라서 글자 가시성의 관찰 bracket은 54.5(없음)→54.584(부분 있음)이며 onset을 55초로 지정하지 않는다. **QA:** dark-card onset, 부분 glyph 출현, 완전한 wordmark reading state와 dwell/소거를 별도 필드로 관리하고 서로 다른 neighborhood 폭의 post를 같은 점으로 취급하지 않는다.

### RC05 — V019: source 번호와 wardrobe/hero 내용의 실제 정합
R002/2.583333의 pre는 splash shoe지만 center/post는 분홍 jacket 인물이다. R003/4.0=분홍 인물→legs/shoes, R004/4.166667와 R005/4.333333는 바지/sole variant 교체, R006/4.833333=gold shoe, R007/6.208333=gold-hood 그룹([strip01](evidence/raw-review-V019/raw-strip-01.jpg)). R010/11.166667 white group, R011/11.291667 red/white model, R012/11.416667 pastel group, R013/11.625 black tracksuit([strip02 cell4–15](evidence/raw-review-V019/raw-strip-02.jpg)). 이전20group의 C번호를25raw와 동치로 쓰면 실제 이미지와 잘못 연결된다. peer 수정 전달. **transfer:** source-local raw→group→shot-candidate→phase join을 explicit하게 하고 model/wardrobe/SKU variation이 선언인지 실패인지 구별.

### RC06 — V021: 원산지 연상과 수입 claim, reaction phase
R017/28.466667 [strip03 cell2/3](evidence/raw-review-V021/raw-strip-03.jpg)의 실제 상자 글자는 `CLEARED / FOR IMPORT / EU`. 다른 상자의 `100% ITALIAN TOMATOES`로 대체하면 별개의 화면 claim을 소거한다. export/import/원산지 글자와 항공 이미지가 실제 통관/원산지 증명을 뜻하지 않는다. R043 chef-pot 인계는 motion, R028 floating-tomato 급변은 unknown으로 유지.
R061 center n2560/PTS85.333333에서 아이/접시→공중 접시, R06285.966667에서 공중 접시→여성 반응, R06386.7에서 여성→접시를 개별 이웃으로 분리했다([strip08 cell13–21](evidence/raw-review-V021/raw-strip-08.jpg)). raw R06898.066667의 아이는 아직 pout; 기존 [native source sheet017](evidence/V021/source-pts-sheets/sheet-017.jpg) PTS99/100에서 smile로 바뀜을 추가 읽었다. 마지막 smile은 실제 관찰이므로 이를 제거하지 않는다. **QA:** reaction cut과 같은 얼굴 내부 표정 phase, 브랜드 overlay가 붙는 상태를 분리.

### RC07 — 이미 있던 counterexample의 재검토: V015
R029/26.633333 [strip04 cell13–15](evidence/raw-review-V015/raw-strip-04.jpg): 한 수평 용기가 두 인물 입 사이를 잇는 비현실적 형태. 기존 chapter:16/20도 이미 기록하여 새로운 발견이라고 주장하지 않는다. 말미 typography는 새 raw-thumb만으로 불명확하다면 판독 포기를 하지 않고 기존 [full-resolution native terminal](evidence/V015/native-terminal.jpg) n900/PTS30.000을 추가 읽어 `Aero Blade`를 확인했다. 브랜드/음료 category 진위는 여전히 미확인. **QA:** 손-입-용기 topology, 브랜드명 판독과 실제 권리/제품 확인을 별도로 검수.

## 판정 전달과 own-error 복구 기록

- peer `video-analysis-design`에게 V007 숫자, V003 blink, V010 same-set pose/card onset, V019 mapping, V021 import-copy를 구체 locator와 전달했다. peer가 관련 chapter/DESIGN 반영했다고 응답. 이 작업자가 main-owned chapter를 직접 수정하지 않았다.
- **내 timestamp 오독·전사 오류도 숨기지 않음:** 전달 과정에서 V003 raw R016을 이전 group-center 16.666667과 혼동했고, V021 R061 85.333333을 strip에서 85.833333으로 오독하여 잘못된 수정 제안을 보냈다. 또한 V010 prose에 요약에서 가져온 54.433450/54.466783/54.500116을 썼으나 retained native dump의 실제 n3266/n3268/n3270 값은 54.434/54.467/54.5였다. JSON의 n/정수 PTS/초는 자동 대조를 통과했고, 이 수치로 prose와 peer 전달을 정정했다. R017/R018 blink, import-copy, dark-card와 뒤늦은 glyph 출현의 내용 발견은 유효하다. timestamp는 요청 시각/merged-center/native raw를 이름부터 구별하고 prose도 숫자를 손전사하지 않고 ledger에서 가져와 검산해야 한다.
- 판정435개 cut을 final verified shot count로 전용하거나, 후보를 전수 읽었다는 이유로 모든 실제 cut/오디오/획득 pipeline을 확인했다고 말하면 안 된다. 이 한계는 단순 claim downgrade 대신 **추가 native 이웃 실제 추출·전수 검토 후** 남는 한계다.

## 후속 소비 계약

1. authoritative per-raw mapping은 `raw-candidate-coverage-first24.json.sources[].events[]`. source hash, native integer PTS, frame n, sheet/cell, 관찰 및 판정을 함께 소비한다.
2. 본 보충 artifact를 원래 uniform/endpoint/provenance ledger와 병합하되 source archive ID는 유지하고 raw/group/scene/shot/phase count를 따로 계산한다. source당 native PTS dump/selection manifest는 `evidence/raw-review-Vxxx/`.
3. 기존6 소유 chapter(V005/V013/V014/V016/V023/V024)는 새로 읽은 사건이 기존 phase/QA를 뒤집지 않아 이번 pass에서는 수정하지 않았다. 기존 skills 구현에는 변경이 없다.
4. 기술적 근거는 기존 [web-source-notes](web-source-notes.md)의 FFmpeg scene/PTS 설명과 연결한다. 후보 판정/책의 미학적 해석은 source의 실제 촬영·합성·음악 권리나 창작 의도를 인증하지 않는다.
