# E2 근거 보정 인계 — 독립 검토 대기

점수 주장 없음. 테스트/빌드/linter/formatter/렌더/생성/업로드/지출/설치/커밋 없음. 기존 W2 증거를 새 실행으로 재명명하지 않았다. 변경은 인용과 지원 범위 설명이며 실행 코드/스키마/Acceptance는 변경하지 않았다.

## 변경 파일과 수정한 결함

- `camera-spatial-design/references/sources.md`: W2 Block/Katz 인용에 실제 rendition bytes/SHA256 추가. W2 읽기와 E2 식별 확인을 구분. Williams/Pearlman/Lumet/Stanchfield/Kenworthy 두 권의 직접 읽은 위치·정확 파일명·bytes/hash·지원 한계 추가. 표 전체를 읽음으로 오인할 수 있던 첫 문장 수정.
- `camera-spatial-design/references/motion-timing-lens.md`: W2-C11의 timing/spacing/attention/focus를 읽은 구간에 결속. 자체 시간표·좌표·보간·접촉·인계 계약과 외부 craft를 분리. 정량 광학과 실제 동적 결과는 미검증으로 명시.
- `camera-spatial-design/references/camera-design.md`: 설치 참조에서 Katz/Block bytes/hash를 바로 확인 가능하게 보정. blocking/관계 장벽/동기화/실루엣을 실제 읽은 사례에 연결.
- `camera-motion-reference-analysis/references/motion-analysis.md`: 설치 분석 참조의 Block 인용에 bytes/hash 추가. 역솔브·호흡·리그를 해당 구간이 입증하지 않는다고 명시.
- 신규 QA: `claims-E2.tsv`, 이 보고서. 공유 정본/manifest/README/CHANGELOG/통합 원장은 수정하지 않았다.

## 직접 읽은 원문과 범위

공통 루트 `E:/Book/06_Book/originals/콘텐츠_제작/md/`. 아래는 원본 Markdown을 read로 직접 읽었으며 audit extract/index를 읽음 증거로 대체하지 않았다. 정확 파일명·bytes·SHA256은 설치 `camera-spatial-design/references/sources.md`와 claims-E2.tsv에 있다. 모두 READ-PARTIAL; 원문 이미지/도판 미검사.

| source ID | 실제 읽은 핵심 구간 | 지원 범위 |
|---|---|---|
| E2-WILLIAMS | L95–97, timing/spacing, p.36 및 다음 exercise | 접촉 시점과 프레임별 위치 간격의 구별 |
| E2-PEARLMAN | L119–121, Chapter 2 pp.29–30 | pulse/phrase, 카메라·배우·대사·음향의 조율 |
| E2-LUMET | L103, p.51 | 리허설 블로킹 후 촬영 선택, 촬영감독 run-through와 제작 제약 |
| E2-STANCHFIELD | L67–69 pp.15–16; L223 p.93 | 디테일보다 포즈·행동 실루엣과 기본 형태 가독성 |
| E2-KENWORTHY1 | L175 p.80 Focus In; L183 p.84 Pan and Slide; L301 p.146 Reflections | 반응에 맞춘 push-in, 배우/카메라 동작 분리 조율, 전경/반사상 초점 선택 |
| E2-KENWORTHY2 | L47 Barrier; L57 Swing to Cut 끝; L83 Focus on One; L103 Threshold | 관계 장벽·문턱 사례, 특정 컷 전 settle, push-in 초점 유지 과제 |

긴 줄의 처음 표시가 잘린 경우 raw로 해당 본문을 다시 읽었다. 단일 `:103:raw`/`:67:raw`가 이후 전체를 반환하는 도구 동작은 report_issue에 보고했고 이후 exact N-N:raw를 사용했다. 반환된 나머지 책 전체를 READ-FULL로 간주하지 않는다. Kenworthy1의 글자 사이 OCR 공백은 원본 그대로 읽었으며 정규화 파생본을 만들지 않았다.

Block/Katz는 W2 원문 읽기 범위를 유지하고 E2는 해당 원본 파일의 bytes/hash만 재확인했다. E2 직접 읽음으로 승격하지 않았다.

## 트리거별 coverage와 남은 범위

| owner / triggered reference | E2 처리 | 남은 검증/소유권 |
|---|---|---|
| camera-spatial / sources.md | 여섯 신규 source 항목 직접 읽기; W2 식별 보정 | canonical source ID 통합은 W4 |
| camera-spatial / camera-design.md | blocking·관계·무빙·실루엣 지원 범위 명시 | headroom/leadroom·조명 분리 전체 craft 감사나 관객 반응 실측을 완료한 것은 아님 |
| camera-spatial / motion-timing-lens.md | W2-C11 핵심 timing/spacing/phrase/focus 근거 추가 | 실제 timing playback, rack-focus, gesture render 미실행; 정량 호흡·왜곡·심도·모션블러 미지원 |
| camera-spatial / spatial-contract.md, workspace-integration.md, camera-programs.md | 변경 없음; E2 근거 보정 대상 아님 | W2 수치/권한 계약 및 부모 통합 검증 유지; 새 전수 감사 주장 없음 |
| motion-analysis / motion-analysis.md | 설치 인용 식별자 보정 | W2 sampled-frame 관찰만 기존 증거; 실제 전체 playback/rig/metric solve 미검증 |
| motion-analysis / programs.md | 변경 없음 | 프로그램/API 계약 재감사 안 함 |
| ai-camera / control-contract.md, programs.md | 변경 없음 | W2 중립 패킷 사례만; provider HARD_CONTROL/생성 결과 미검증 |
| Blender / blender-workflow.md, sibling spatial-contract.md/sources.md | sources의 읽기 근거만 갱신 | 기존 W2 SH01 smoke 재실행 안 함; SH02 동적/초점/포즈 검수 아님 |
| orchestrating / video-direction.md, stage-execution.md | 변경 없음 | W2 텍스트 패키지 사례 유지; fresh-agent 평가 아님 |
| cross-owner storyboard-contract.md, contract.md, reference25 | 직접 수정 안 함 | 각 owner 근거 감사/통합 필요; E2가 coverage 완료 주장 안 함 |

W2-C11/C12의 명시된 unread core는 위 구간에 한정해 해소했다. 책을 읽었다는 사실이 실제 출력 성공을 입증하지 않는다. E2-C08에 정량 광학/실행 결과의 남은 unsupported 범위를 따로 남겼다. camera-design의 기타 구도/음영 규칙과 motion-analysis의 lens breathing 등은 이 신규 읽기로 지원됐다고 하지 않는다. 최종 rubric cap/modifier는 부모/독립 검토자가 실제 load-bearing 여부를 판단해야 한다.

## 실제 실행 증거

**E2-IDENTITY**: PowerShell 로컬 비테스트 식별 명령, exit 0. 여덟 원본의 bytes/SHA256을 얻었고 설치 인용에 반영했다:

```powershell
Get-ChildItem -LiteralPath 'E:/Book/06_Book/originals/콘텐츠_제작/md' -File | Where-Object { $_.Name -match 'Williams|Pearlman|Lumet|Stanchfield|Kenworthy|Bruce Block|Steven D. Katz' } | ForEach-Object { [pscustomobject]@{Name=$_.Name;Bytes=$_.Length;SHA256=(Get-FileHash -Algorithm SHA256 -LiteralPath $_.FullName).Hash} } | ConvertTo-Json
```

최초 호출은 외부 shell의 `$` 확장으로 PowerShell 표현식이 손상되어 오류를 냈다. 외부 single-quote로 전달한 수정 호출은 성공했다. 이 식별 명령은 동작 테스트/광학 검증이 아니다. 기존 실패 PATH 검사와 SH01 smoke를 반복하지 않았다.

## Cross-owner 요청

- W4: E2-WILLIAMS/PEARLMAN/LUMET/STANCHFIELD/KENWORTHY1/2를 위 정확 rendition과 읽기 범위로 canonical sources.md에 대응해 달라. QA 전체를 런타임 필수 자료로 만들지 말 것.
- 리더: 공유 changelog/version에 이 citation-only 보정을 기록하고 설치 참조 상대 링크와 정본 연결을 통합 확인할 것. 신규 점수나 전수 완료를 본 보고서에서 추론하지 말 것.

## 부모 통합 후 정확 명령 — E2 미실행

```sh
python camera-spatial-design/scripts/test_spatial_spec.py
python blender-previsualization/scripts/test_build_previs.py
python scripts/check_versions.py
"C:/Program Files/Blender Foundation/Blender 5.2/blender.exe" --background --factory-startup --python blender-previsualization/scripts/build_previs.py -- --spec camera-spatial-design/assets/camera-spec-example.json --output qa/skill-completeness-95/E2-integration-stills --mode stills
```

출력 디렉터리가 이미 있으면 새 이름으로 실행. 위 stills의 SH02 시작/중간/끝은 기존 SH01 smoke 복제가 아니라 미검사 샷 확인용이다. 그러나 이 예제는 rack focus/손 gesture/차량 접촉을 입증하지 않는다. 그런 요청에는 실제 해당 설정/동작을 포함한 승인 spec와 동적 출력 검수가 별도로 필요하다. 링크/설치 검사와 61개 fresh-session 평가는 부모의 실제 runner 명령을 사용하며 여기서 존재하지 않는 옵션을 만들지 않았다.
