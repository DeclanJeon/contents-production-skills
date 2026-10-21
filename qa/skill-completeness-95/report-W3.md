# W3 캐릭터·보드 구현 인계 — review

독립 점수·행동 PASS 판정 없음. 테스트/빌드/린터/formatter는 공유 edit wave 계약에 따라 실행하지 않았다. 아래 합성 텍스트는 직접 작성한 소비 계약 예시와 수동 대조 결과이며 fresh-session 모델 평가나 이미지/음성 검증 결과가 아니다.

## 변경 파일과 수정 결함

- `designing-character-personas/SKILL.md`: 행동 중심 제작법에 Hooks 원문 위치와 제한을 연결. 창작 패킷 구조와 심리학적 사실을 분리.
- `designing-character-personas/references/sources.md`: 실제 직접 읽은 공식 페이지/연구 초록/원본 rendition의 위치와 READ-PARTIAL 범위. 세 voice layer는 저장소 설계이며 vendor의 보장이라는 주장을 하지 않음.
- `designing-character-personas/references/mbti-lens.md`: 공식 질문 5–7/14와 논문 초록 읽기 범위. 관찰 행동 예시는 타입 판별 결과가 아닌 작성 질문임을 명시.
- `designing-character-personas/references/enneagram-lens.md`: 9개 타입 페이지의 Basic Fear/Desire/Key Motivations를 직접 대조. type 3의 exposed-as-failure, 5의 invaded, 7의 trapped, 8의 vulnerable을 기본 공포 필드에서 제거. 날개/방향 이론과 104-sample 연구 초록 범위를 명시.
- `designing-video-character-sheets/SKILL.md`: 세 라벨 설명이 supplied/observed를 합쳐 놓던 충돌을 네 provenance로 정정. 관찰은 승인·권리·심리 사실이 아님. 미위임 승인 캐릭터의 빈칸을 제안으로 채우던 문장을 위임 범위로 제한.
- `designing-video-character-sheets/references/character-craft.md`: action/objective/obstacle 원문 지원과 voice/SSOT/lineage의 authored 계약을 구분.
- `designing-video-character-sheets/references/character-ssot-master-prompt.md`: 전체 형식 요청을 전기/인구학 발명 위임으로 오독하지 않도록 수정. 작은 외형 결점이 실재감·생성 재현성을 만든다는 무근거 인과 단정을 선택적 디자인 제안으로 변경.
- `storyboarding-video/references/narrative-panels.md`: 잠긴 시놉에 단서를 반드시 새로 심게 하던 규칙을 supplied cue 보존/없는 단서는 gap으로 변경. 좁은 패널 표에도 panel/beat/scene/shot content ID와 원문 위치 명시. 실제 읽은 Hu staging/axis 구간 인용 및 원문의 좌우 문장 불일치 제한 기록.
- `qa/skill-completeness-95/claims-W3.tsv`: 22개 claim 행. authored 규칙과 차용된 craft/psychology를 별도 분류. 외부 웹은 라이브 조회여서 파일 hash/bytes를 발명하지 않고 N/A-live-web로 표시.
- 이 보고서.

`storyboarding-video/SKILL.md`, persona template, expression bridge는 실제 읽고 유지: 이미 stage blocker, SSOT/voice selection 소유권, stale pin, silent role, 실제 미디어/텍스트 구분이 있으므로 같은 Acceptance를 추가하지 않았다. manifest/README/CHANGELOG/공유 원장/공유 sources.md는 수정하지 않았다. 버전 통합은 리더 소유다.

## 원문 직접 읽기

1. Hooks, *Acting for Animators*: `E:/Book/06_Book/originals/콘텐츠_제작/md/Acting for Animators (Ed Hooks) (z-library.sk, 1lib.sk, z-lib.sk).md#L99-L103`, READ-PARTIAL. 전체 다섯 줄의 원문을 raw로 읽음. 337169 bytes, SHA-256 `78d7a71fd3f530ae501d8cef6d77db97edded4c0e4ad8f9406af3fbd8944740a`. action/objective/obstacle의 연극적 제작 관점만 채택; 모든 심리 과정의 실증 사실이나 모든 장르에 갈등을 추가할 의무는 채택하지 않음.
2. Hu, *Mastering Storyboarding*: `E:/Book/06_Book/콘티_스토리보드/md/스토리보드 마스터하기 - 캐롤라인 후.md#L630-L678`, 특히 L636–661/인쇄 pp59–61, READ-PARTIAL. 47562 bytes, SHA-256 `cdd4f9b82b83c2ac6cc87c3d39251a79e4d02b7b57e337945bcb89efc58b5f21`. 공간 관계·screen direction·180축 혼란 위험 지원. L650의 좌우 표현은 바로 아래 예시와 불일치하므로 고립된 side assignment를 규칙으로 복제하지 않음. 도판/페이지 이미지 확인 없음.
3. [공식 MBTI Facts](https://www.themyersbriggs.com/en-US/Support/MBTI-Facts): 질문 5–7, 14, READ-PARTIAL. 개발자의 의도/정의이지 독립 검증 아님.
4. [McCrae & Costa 초록](https://pubmed.ncbi.nlm.nih.gov/2709300/): 데이터/결과 문단, READ-PARTIAL. 전 논문 읽기 아님.
5. [Hook et al. 초록](https://pubmed.ncbi.nlm.nih.gov/33332604/): 104 samples·mixed reliability/validity·fewer factors·wing/movement 제한 문단, READ-PARTIAL. 전 systematic review 읽기 아님.
6. [Enneagram system](https://www.enneagraminstitute.com/how-the-enneagram-system-works/): The Wing 및 Directions of Integration/Disintegration, READ-PARTIAL. 모델 전통의 주장으로만 채택.
7. Enneagram [1](https://www.enneagraminstitute.com/type-1/), [2](https://www.enneagraminstitute.com/type-2/), [3](https://www.enneagraminstitute.com/type-3/), [4](https://www.enneagraminstitute.com/type-4/), [5](https://www.enneagraminstitute.com/type-5/), [6](https://www.enneagraminstitute.com/type-6/), [7](https://www.enneagraminstitute.com/type-7/), [8](https://www.enneagraminstitute.com/type-8/), [9](https://www.enneagraminstitute.com/type-9/): 각 in Brief의 Basic Fear/Desire/Key Motivations, 각각 READ-PARTIAL. 유명인 typing·진단·중독·임상 연결은 채택하지 않음.
8. [ElevenLabs Voice Design](https://elevenlabs.io/docs/eleven-creative/voices/voice-design): Overview, Recommended prompt format, Tone/Timbre, Pacing, Text to preview, READ-PARTIAL. 실제 응답은 `.md` alternate. timbre/delivery 구분과 preview 정합성만 지원; 모델 실행·음성 청취·provider 전체의 공통 control 보장 없음.

## 정상 합성 산출물 — 수동 계약 대조

### W3-N01: 독립 persona packet, speaking role

합성 supplied brief: 새 가상 창고 안내자 설계 위임, 말하는 인물, 한국어, typology none, 분실 상자를 찾는 동료에게 현재 위치를 알려준다. 아래 creative 값은 모두 proposal; 언어/역할/목표/mode는 supplied. 파일·오디오·프로젝트/아티팩트 ID는 없다.

- `provenance`: standalone, fictional, delegation granted, input_artifacts 없음, mode none supplied.
- `persona_core`: 목표=동료가 상자 위치를 찾게 함; 보호가치=확인된 정보만 전달; 피하는 상태=추측을 확정처럼 전달; 믿음=확인되지 않은 경로는 헛걸음 비용; 우선순위=정확성 먼저, 급한 상황이면 모름을 즉시 알림; hard_limit=없는 위치 발명 금지; 겉의 짧은 응답/속의 협력 의도; 비용=답이 늦어 보임; 관계=익숙한 동료에게도 확인 절차 유지; 모순=정확성을 원하지만 긴급할 때 확인 미완료를 먼저 알림(조건이 다름).
- `typology_lens`: N/A, explicit none.
- `behavior_rules`: 불확실한 위치 → 오안내 위험으로 해석 → 확인 의도 → 선반 표기를 다시 봄 → 기다림 비용; 예외=긴급 시 확인되지 않았다고 먼저 말함.
- `expression_bridge`: 선반과 동료 사이 시선 이동, 위치 확인 뒤 손으로 선반을 가리킴; 얼굴/체격/인종으로 성향 표현하지 않음.
- `voice_identity`: proposal, 중음역·선명한 자음·짧고 깨끗한 말끝; anchors=자음 선명도/말끝; allowed variation=속도·강세, 음색/조음 유지. `voice_identity_direction`: “선명한 자음과 짧게 닫는 말끝을 유지한다. 장면별 속도와 강세는 달라도 같은 음색을 유지한다.” realization unresolved, selected voice 없음.
- `speech_style`: proposal, 확인한 사실 뒤 짧은 안내, 존댓말; language Korean supplied, dialect undecided.
- `performance_cues`: exact text “확인했어요. 두 번째 선반이에요.”(proposal sample); intent=확인 위치 안내; subtext=추측이 아님을 알림; pressure=낮음(proposal); stressed_words=두 번째; pause=첫 문장 뒤 짧게; breath=자연; pace=일정; performance_cue=동일 auditory anchors 유지, 두 번째에 강세, 문장 사이 쉼.
- `validation`: explicit none 유지, 행동/비용/예외 있음, 모든 delivered line cue 필드 있음, 선택 음성 발명 없음(직접 텍스트 대조).
- `unresolved_requirements`: 실제 voice 후보/권리/오디션/도구 control/청취 결과 없음. 이 패킷은 선택된 음성이나 오디오가 아님.

### W3-N02: compact sheet 소비 seam

합성 delegated input: 기존 `character_sheet=CS01@2`, `character_id=CH01`, `synopsis=SY01@1`, 위 N01과 같은 창작 위임, 영상 없는 compact sheet. 이는 예시 입력 ID이며 실제 저장소 파일/원장 등록이 아니다.

- supplied role/goal/language/mode를 보존. N01 persona/behavior/expression/voice 층을 한 sheet 안에 소비; 두 번째 persona bible을 만들지 않음.
- proposal visual anchors: 청록 작업 조끼, 둥근 사각 명찰 형태, 손바닥을 편 안내 자세. 생물학적 나이/인종은 undecided. 고정=조끼 색/명찰 형태, 허용 상태=팔 위치/시선/표정.
- image-sheet prompt(spec only): “중립 배경의 같은 가상 창고 안내자. 청록 작업 조끼와 둥근 사각 명찰 형태를 유지. 전신 앞·옆·뒤 모습 및 선반을 가리키는 안내 자세. 같은 비율과 의복. 장면 배경·사실 증거·생성 완료 주장은 없음.”
- return: CS01@2/CH01 유지, dependency proposal SY01@1, `persona={role:창고 안내자, personality:확인 후 안내, observable_behavior:선반 표기 확인 후 손으로 안내, speech:확인 사실 뒤 짧은 존댓말 안내}`. voice_profile 파생 시 CS01@2 pin, 실제 voice ID/model/settings는 selection owner로 넘김. 실제 이미지 없음.
- 수동 대조: 정상 compact 요청에 0–33 전체 확장이나 이미지-backed 완료를 주장하지 않음. 실제 project validator용 완성 JSON이 아니므로 validator PASS로 집계하지 않음.

### W3-N03: 명시적 narrow 패널 연습

합성 supplied story(정확히 두 패널): “CH01은 오른손에 든 파란 상자를 본다. 같은 상자를 그대로 내려다본다.” 대사/소리 없음, 텍스트-only 패널 연습. supplied IDs 없는 독립 예시의 B01/B02, SC01, SH01, P01/P02는 local content IDs.

| panel/beat/source | scene/shot | 단일 가시 행동·기능 | 연속성 | 공개/유보·프롬프트 |
|---|---|---|---|---|
| P01/B01/문장1 | SC01/SH01 | 오른손의 상자를 보는 순간; 시선 대상 소개 | CH01, 파란 상자, 오른손, 동일 위치·소유; 소리 없음 | 상자 겉면만 보임, 내용물 미정. “같은 CH01이 오른손에 든 파란 상자를 바라보는 한 순간, 상자 외형만 보이고 내부는 보이지 않음.” |
| P02/B02/문장2 | SC01/SH01 | 내려다보는 정지 지속; 보유 상태 유지 | 손·색·소유·위치 유지, 행동 추가 없음; 소리 없음 | 동일 겉면, 내용물 미정. “같은 CH01이 같은 오른손에 든 같은 파란 상자를 그대로 내려다보는 한 순간, 동일 방향과 소유, 내부 비공개.” |

handoff=P01→P02, supplied count=2, sheet layout prompt optional 미요청이라 생략, 이미지 생성/검수 없음. production board가 아니라 명시적 narrow exercise이므로 shooting technical table을 임의 추가하지 않음. source→beat→panel 연결과 cue/ownership 보존을 직접 텍스트 대조함; 실제 화각/픽셀/정체성은 미검증.

## 경계 합성 산출물

### W3-B01: 승인 캐릭터 + 공급 타입 + 비발화

입력=승인 CH07, supplied type 6, typology 추가 위임 없음, silent. output lens=enneagram supplied 6, MBTI undecided/미추가; 행동이 type 해석과 다르면 approved 행동 보존하고 gap 기록. voice_identity/speech_style/vocal performance_cues 모두 `N/A — 비발화 역할`. visual expression만 expression_bridge에 둠. 타입에서 낮은 음색·불안 표정·얼굴 형태를 추론하거나 narrator를 만들지 않음. type 5를 요청한 변형에서도 invaded를 기본 공포 출처 사실로 복제하지 않음. 수동 대조일 뿐 fresh model 반례 실행은 부모 소유.

### W3-B02: 원본 이미지 관찰 + 미위임 전기

입력=기존 승인 캐릭터의 실제 이미지에서 붉은 코트를 관찰했다고 명시한 합성 packet, 나이·출생지·심리·권리·승인은 불명, 추가 창작 위임 없음, full format 요청. output=코트 observed(입력의 source/version/scope 참조), 나이·출생지·심리 undecided, 관찰만으로 승인/권리 확인했다고 하지 않음. 모든 섹션 번호를 유지하되 template count 충족 때문에 전기를 발명하지 않고 미정/필요 입력 기록. 작은 흉터 추가나 외모 결점으로 reproducibility를 보장하지 않음. 기존 master spec의 gap-proposal/questioning 문장과 main label 충돌을 이 경계로 수동 대조하여 수정함.

### W3-B03: 인덱스·단서·stage blocker

입력 A=잠긴 미스터리, 마지막 P04 발견, 사전 clue 미제공. output indexed gap=`B04/SC01/SH02/P04: 사전 단서 근거 없음; 시놉 담당/코디네이터에 story input 필요; 잠긴 사건은 유지; 새 단서 생성 안 함`. 발견을 조기 노출하거나 탐색 장면을 추가하지 않음.

입력 B=production shooting board에서 SH02 camera/spatial/voice packet 없음. output 한 indexed requirement packet: `SC01/SH02/B04/P04 | camera/spatial | required input=owner camera spec/version | blocking shooting-stage`; `SC01/SH02/B04/P04 | speech | required input=exact approved line + current voice_profile pin | blocking shooting-stage`. 최종 board 완료가 아니라 보완 대기. pitch-only 요청의 `deferred (승인 후)`와 shooting blocker를 혼동하지 않음. 이미지-backed 요청에서 text prompt만 있고 Sheet A/실제 panel/assembled sheet/extractions 없으면 package blocked; 검수/완료 아님. 실제 project validator 실행 전 예시이며 PASS 아님.

## 실행한 로컬 비테스트 관찰

- 원문 파일 두 개 `Get-Item`/`Get-FileHash` PowerShell 명령 성공: 위 bytes/hash 관찰. 첫 double-quoted shell 시도는 `$` 확장으로 오류, 다음 bare PowerShell cmdlet 시도는 command not found. single-quoted `powershell -NoProfile -Command`로 변경해 위 정확 값을 얻음. 실패를 성공으로 숨기지 않음.
- W3-CLI01: `python -X utf8 video-production-assets/scripts/validate_storyboard.py --help` → exit 0. positional project, `--base-dir`, `--require-images`, `--panels-per-sheet` 실제 확인. coverage/references/timing만 검증하며 미감·승인 검증이 아니라는 help 관찰.
- W3-CLI02: `python -X utf8 video-production-assets/scripts/validate_project.py --help` → exit 0. `--profile {plan,preproduction,delivery}`, `--base-dir` 확인.
- 위 CLI help는 진입점 smoke일 뿐 변경된 지시문 행동 검증이 아니다. 테스트·모델평가·이미지·오디오는 실행하지 않음.

## 부모 통합 실행 명령 — 이 wave에서 미실행

현재 실제 validator의 인자 형식(아래 `<...>`는 부모가 실제 통합 프로젝트 경로로 치환):

```text
python -X utf8 video-production-assets/scripts/validate_project.py <project.json> --profile plan --base-dir <project-root>
python -X utf8 video-production-assets/scripts/validate_storyboard.py <project.json> --base-dir <project-root>
python -X utf8 video-production-assets/scripts/validate_project.py <project.json> --profile preproduction --base-dir <project-root>
python -X utf8 video-production-assets/scripts/validate_storyboard.py <project.json> --base-dir <project-root> --require-images --panels-per-sheet 8
```

통합 트리 기존 회귀 검사(파일 경로를 glob으로 확인; 실행하지 않음):

```text
python -X utf8 -m pytest -q video-production-assets/scripts/test_validate_project.py video-production-assets/scripts/test_validate_preproduction.py video-production-assets/scripts/test_validate_storyboard.py video-production-assets/scripts/test_asset_gate.py video-production-assets/scripts/test_project_handoff.py video-production-assets/scripts/test_render_storyboard_sheet.py video-production-assets/scripts/test_split_storyboard.py
python scripts/check_versions.py
python -X utf8 -m pytest -q
```

fresh-session 행동 평가는 부모의 승인된 `run_cases.py`/case manifest로 M-09/M-12 및 persona 정식 case ID를 실제 manifest에서 찾아 수행. 이 worker는 runner·ID를 추측해 실행하지 않음. N01–B03을 추가 반례로 사용할 수 있으나 정식 61개 분모를 바꾸지 않는다.

## 교차 소유자 요청과 남은 제한

- W4 요청: 공유 `video-production-assets/references/sources.md`의 Hooks 13 행에 정확 original rendition/bytes/hash/L99–103 READ-PARTIAL 범위를 연결하고 theatrical craft와 empirical psychology 구분. Hu의 staging/axis 추가가 필요하면 위 rendition/bytes/hash/L636–661을 사용하고 도판 미검사와 L650 불일치 명시. W3가 공유 sources.md를 직접 수정하지 않았음.
- W4 요청: shared storyboard-contract/triggered production modules의 source-derived craft는 W4 claim slice가 필요. W3-C22는 읽은 repo 계약이지 그 전체 차용 서적을 검증했다는 뜻이 아님.
- 리더 요청: 변경 스킬 버전과 manifest/README/CHANGELOG를 기존 통합 관례대로 갱신. standalone install에서 sibling persona/shared sources 접근성을 부모 링크 검사로 확인.
- 웹 original 페이지는 직접 읽었지만 별도 immutable snapshot/hash를 만들지 않음. live-web N/A 값을 읽은 로컬 원본 hash로 오인하지 말 것. 두 논문 full text, 책 전권/도판, 실제 음성/image identity, 실제 generated package 모두 미검증.
- 외부 로그인·업로드·생성·과금·훈련·배포·게시·commit 없음. 점수는 독립 reviewer와 부모의 최종 실행 이후에만 판정.
