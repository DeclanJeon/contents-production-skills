# E7 — core technical/craft evidence handoff

상태: **review 요청, 독립 점수 없음**. W4-U20/U21/U22/U23/U25/U27의 접근 가능한 근거를 직접 읽고 좁은 지원 범위를 연결했다. 모든 core craft가 결속됐거나 실제 매체 QA/행동 평가가 통과했다는 보고가 아니다. 테스트·빌드·linter·formatter·모델 평가·provider 호출·미디어 생성/청취/업로드·배포·게시·commit 없음. 부모의 shared edit wave 뒤 검증 계약을 지켰다.

## 변경 파일 / 수정한 결함

아래 여섯 assigned consumer와 `claims-E7.tsv`, 이 보고서만 작성/수정했다. 사용자 dirty 변경을 reset/revert하지 않았고 shared sources/SKILL/manifest/README/CHANGELOG·다른 모듈·통합 state/ledger/scorecard는 수정하지 않았다. 기존 Acceptance heading을 복제하지 않았다.

| 파일 (`video-production-assets/references/`) | 구체 수정 / 보존 |
|---|---|
| `20-visual-mode-ssot.md` | 규모가 인원수보다 위계만으로 만들어진다는 단정을 깊이/크기/질감 계획으로 한정. Block의 실제 깊이 단서만 연결. tier/count/7view/ID는 authored contract로 유지하고 모드별 우위·군중 편집/행동 효과는 미지원으로 남김. |
| `21-generated-video-qa-retry.md` | 무게 이전/전신 대응의 Williams 구간, OpenStax no-slip 조건, PBRT undersampling 원리를 분리. spokes 역회전=실제 rolling failure 또는 aliasing 확정이라는 오독 차단. Blender4.2 alpha 입력 형식 점검을 기존 edge QA에 추가. 합성 순서·contact3·분할 라우팅을 유일 물리 법칙/모델 한계로 주장하지 않음. 전체 합성 craft가 alpha 문서로 지원된다는 주장 없음. |
| `22-dialogue-lipsync.md` | 보편적인 폐쇄음 최우선 순위를 source 범위의 주요 닫힘/모음/구 악센트 비교로 교정. Williams가 일률2frame lead를 비판하는 구간 연결. 코미디 반응 창은 보편 시간/효과 없음, 실제 맥락 검수로 유지. Habermas를 E7도 직접 읽고 지문 기록. 기존 v4 Style/Speed/SSML/IPA/tags/cross-language/quota 범위와 W4 attribution을 보존; 음성 실행 없음. |
| `23-finishing-platform.md` | 여섯 역할을 모든 프로젝트의 필수 six-node 구조로 읽히던 규정을 editable 역할 대응으로 교정. 유효한 group/shared/color-management 처리를 허용하며 무효 조정/빈 노드 추가 금지. `Shot Match` 빈 노드 자체를 실패시키지 않는 기존 수정 보존. BMD의 balance/match/nodes/scopes/실제 비교 기능만 근거로 연결. 플랫폼 효과·전체 texture/material/audio craft 미지원은 유지. |
| `25-reference-video-analysis.md` | 픽셀 입력을 배제하고 정규화만 해상도 불변처럼 취급하던 문구 교정: 실제 pixel/출력크기/크롭을 보존하고 정규화가 crop/distortion 불변은 아님을 명시. OpenCV 식/동일 광선·scale ambiguity·sensor 의존을 직접 읽고 단일프레임 비유일성의 적용 추론을 명시. known geometry/calibration pose solve까지 불가능하다는 확대 방지. |
| `27-camera-motion-qa.md` | Block의 상대 운동, Katz의 축/재정위 구간을 실제 출처/지문에 결속. uniform pan pixel velocity·동적 camera 원인 유일 확정으로 확대하지 않음. 렌즈호흡/안정화/가감속 전체는 미지원. 실제 클립 없는 motion pass·임의 오차 threshold 금지 보존. |

## 직접 읽은 원문 / 지문

모든 book 읽기는 **READ-PARTIAL**, OCR 텍스트 직접 읽기다. audit extracts/index와 동료 보고서는 발견 안내로만 썼다. 전권·도판/사진·원 영상/오디오를 읽거나 봤다고 하지 않는다. 정확 원본 경로·hash·bytes·consumer별 적용은 `claims-E7.tsv`에도 있다.

| ID | 실제 rendition / 읽은 범위 | 지문 / 지원 한계 |
|---|---|---|
| E7-READ-WEIGHT / E7-READ-SYNC | `E:/Book/06_Book/originals/콘텐츠_제작/md/The Animators Survival Kit, Expanded Edition A Manual of Methods, Principles and Formulas for Classical, Computer, Games,… (Richard Williams) (z-library.sk, 1lib.sk, z-lib.sk).md` L535–543(pp256–260), L631–651(pp304–314), L675(청자 눈 반응 예; 인쇄 page marker 미확정). | 390099 bytes; SHA256 `dd1d17e5d57695a274c531287cdf1dce76785229280b0ae68bf850a51e4ca9ef`. 하중/준비/전신 반응, 입모양 개인차·구/악센트·sync 재생 비교·몸/얼굴 태도만. 한국어 mapping/고정2frame lead/웃음 반응 창/모델 품질 보장 아님. |
| E7-READ-BLOCK | `E:/Book/06_Book/originals/콘텐츠_제작/md/The Visual Story Creating the Visual Structure of Film, TV, and Digital Media Third Edition (Bruce Block) (z-library.sk, 1lib.sk, z-lib.sk).md` L75–117(pp37–58), L529–537(pp264–268). 설치 consumer에는 실제 채택한 L95–99/L103–117/L529–537만 인용. | 368221 bytes; SHA256 `403172711929152d7019ccbab9043fc0ba8c512606fc14375ef6e78cc410392c`. 깊이 단서/상대 운동만; crowd 수·위계/컷 배열·모드 우위·모든 회전의 동일pixel speed는 아님. |
| E7-READ-KATZ | `E:/Book/06_Book/originals/콘텐츠_제작/md/Film Directing Shot by Shot Visualizing from Concept to Screen (Steven D. Katz) (z-library.sk, 1lib.sk, z-lib.sk).md` L333–355, The Line of Action/Establishing a New Line/Moving the Camera Over the Line, 인쇄 p130 이후. | 535607 bytes; SHA256 `e8ad5bf5ecc3659fb9b936dd081147a465b03ca09f53e6d690ca286fa4706e9a`. continuity convention과 예외·재정위만; 도판 미검사·모든 axis cross 실패 아님. |
| E7-READ-HABERMAS | `E:/Book/06_Book/originals/콘텐츠_제작/md/감정과 서사 - 틸만 하버마스.md` L351–359(pp160–164). | 952320 bytes; SHA256 `4e7dc3f8b2a1f448fc00df883fa2e5a475b0f590b84af583603ed6a5caa325aa`. 화자 평가/서술·정서/수용 맥락과 불일치 연구의 제한만. 보편 VO 정서 효과/한국어/개별 provider 능력 검증 아님. |

### 직접 읽은 공개 primary docs

2026-10-17, 모두 READ-PARTIAL. 아래는 read 도구가 반환한 live rendition을 실제 읽은 기록이다. **고정 local snapshot/hash/bytes는 없으므로 `N/A-live-web`**로 표시했다. book의 고정 rendition 지문을 웹 근거에 대용하지 않았다. 이 지문 공백은 남은 증거 제한이며 완전한 immutable web evidence로 집계하면 안 된다. 본문을 QA에 복제하지 않았다.

| ID / URL | 직접 읽은 locator / 범위 |
|---|---|
| E7-READ-ROLL — [OpenStax §11.1](https://openstax.org/books/university-physics-volume-1/pages/11-1-rolling-motion) | `Rolling Motion without Slipping` 식11.1–11.3 및 `Rolling Motion with Slipping`의 v−Rω 조건. live HTML reader. 접점/지면의 관계만 채택; 예제 전체나 이미지 직접 검사를 주장하지 않음. |
| E7-READ-SAMPLING — [PBRT4 §8.1](https://pbr-book.org/4ed/Sampling_and_Reconstruction/Sampling_Theory) | 도입의 sampling/reconstruction/animation flicker, §8.1.3 Aliasing(read 반환 L300–440 포함). live HTML reader. spokes 예는 원리 적용 추론/수치 console 예이지 책이 해당 클립 원인을 밝힌 것이 아님. |
| E7-READ-ALPHA — [Blender4.2 Alpha Over](https://docs.blender.org/manual/en/4.2/compositing/types/color/mix/alpha_over.html) | `Inputs`, `Properties` Convert Premultiplied/Premultiply. live HTML reader. latest URL은404여서 검색으로 발견한 versioned4.2 원문을 읽었음; 검색 답변을 직접 읽기로 쓰지 않음. 도구 설치/Blender 실행 없음. |
| E7-READ-GRADE — [Blackmagic Color](https://www.blackmagicdesign.com/products/davinciresolve/color) | Balance Image Color; Auto Balancing and Matching; Secondary Color Correction; Work with Nodes; Professional Scopes; Compare Shots; Find Mismatched Shots. live HTML reader. marketing상의 독점/우월 품질 주장은 채택 안 함. |
| E7-READ-PROJECTION — [OpenCV4.13 calib3d](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html) | Detailed Description pinhole 식, Homogeneous Coordinates의 동일광선/scale ambiguity, Intrinsic parameters from camera lens specifications. 4.x가4.13으로 resolve된 live Markdown content-negotiated rendition의 도입. 4190-line API 전체를 읽었다고 하지 않음. |

Eleven v4의 설치 문장·W4-P01–P04 claim 범위를 읽고 보존했다. E7이 원 v4/IPA/quota/TTS 문서를 재독하거나 현 endpoint를 확인했다는 주장은 없다. claims의 해당 행은 `UNREAD`와 W4 attribution을 명시하며 W4의 직접 읽기 기록은 삭제/무효화하지 않는다.

## Load-bearing coverage / 미해결 특정 주장

`claims-E7.tsv`는 module별 section 집합을 named claim군으로 열거한다. authored workflow와 source-derived craft, provider contract, unsupported effect를 별도 행으로 나눴다. 모든 문장을 원자 단위로 검증한 전수 ledger나 독립 review가 아니다.

| 이전 gap | E7에서 연결한 범위 | 남은 특정 주장 / 사용자 영향 |
|---|---|---|
| W4-U20 | Block의 known size/texture/relative movement 깊이 단서 | 2D turnaround가 실사 질감보다 중요하다는 상대 우위; 3D/stop-motion 참조 팩 효과; crowd micro-action clustering/hero hierarchy/컷 사다리/portal anchor의 지각 효과. 기능 유지 + BASIS-UNSTATED, 효과 입증 안 함. |
| W4-U21 | Williams 하중/전신 반응; OpenStax no-slip; PBRT sampling; Blender alpha contract | lighting/reflection/contact shadow/blur/grain/light wrap 전체 매칭 craft와 특정 순서 우위, complexity 분할·참조강화 재시도의 성공 개선 효과. 모델별 실증/원매체 검사 없음. 순서는 운영 규격, 효능은 미지원으로 분리. |
| W4-U22 | Williams word/phrase accents/닫힘·sync 변동·body attitude, Habermas 맥락 | 코미디 반응 창의 길이/웃음 효과, 한국어 음소별 mapping·다국어 자연스러움, roomtone/mic continuity 전체 craft. v4는 W4 확인 범위만 유지; 새 runtime/발음/무료자격 확인 없음. |
| W4-U23 | BMD balance→creative 일반 workflow/비교/선택처리 기능 | skin/product/material별 실제 색 정확도·texture/audio 후반 craft, 플랫폼 hook/길이/loop/retention 효과. valid 기존 node graph의 실제 editable 상태/결과는 부모가 앱/fixture에서 검증해야 함. |
| W4-U25 | OpenCV 투영/scale ambiguity·sensor 의존, crop/normalization 제한 | 웹 immutable rendition 지문; 화면 압축 느낌만으로의 렌즈 판별·심도/rolling shutter/렌즈호흡 및 source별 실제 camera solve. unknown frame의 단일 확정 금지만 지원; known-geometry pose solve까지 막지 않음. |
| W4-U27 | Block 상대운동, Katz 축/예외/재정위 | 렌즈호흡·안정화 crop·wobble/가감속의 기술 원인과 자연스러움. 실제 clip/계획/승인오차 없으므로 motion pass 없음. |

원문이 접근 불가능하다고 진단한 항목은 없다. 위 잔여를 사용자 재업로드/U3로 돌리지 않는다. 특히 책의 일부를 읽었다고 나머지 craft를 책이 지원하거나 authored invention이라고 재라벨링하지 않았다. fixed rubric의 unread load-bearing 제한/점수는 독립 검토자가 실제 claim 범위에 적용해야 하며 E7은 점수를 부여하지 않는다.

## 실제 실행한 비테스트 local smoke

PowerShell 지문 명령은 직접 읽은 원본4개에 실제 실행했다(exit0). 명령 형태:

```powershell
powershell -NoProfile -Command 'Get-ChildItem -LiteralPath "E:/Book/06_Book/originals/콘텐츠_제작/md" -Filter "*.md" | Where-Object { $_.Name -like "The Animators Survival*" -or $_.Name -like "The Visual Story*" } | ForEach-Object { "{0}`t{1}`t{2}" -f $_.FullName,$_.Length,(Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash.ToLower() }'
```

Katz/Habermas는 위 표의 정확 path를 `$p`로 두고 `Get-Item -LiteralPath $p | ForEach-Object { "{0}`t{1}`t{2}" -f $_.FullName,$_.Length,(Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash.ToLower() }`를 실행했다. 관찰 값은 위 지문과 같다.

문서의 좁힌 수학적 경계를 실제 console에서 계산했다(exit0). 테스트/validator/model/media 실행이 아니라 원리의 합성 수치 예다. 정밀 매체 진단/실제 consumer 준수 증거로 집계하면 안 된다.

```powershell
powershell -NoProfile -Command '$u1=1000.0*1/10; $u2=2000.0*1/20; $u3=1000.0*2/20; "E7-SMOKE-PROJECTION planar point: fx=1000 X=1 Z=10 -> u=$u1; fx=2000 X=1 Z=20 -> u=$u2; scale X=2 Z=20 -> u=$u3"; $r=0.3; $v=3.0; $omega=$v/$r; "E7-SMOKE-ROLL approved synthetic values: R=$r m v=$v m/s omega=$omega rad/s; contact relative velocity=$($v-$r*$omega) m/s"; $spokes=12; $fps=24; $cycles=$spokes*2.0/$fps; $slow=$spokes*1.9/$fps; "E7-SMOKE-SAMPLING ideal repeated spokes: 2rev/s -> $cycles pattern cycles/frame, sampled phase increment=$($cycles-[math]::Round($cycles)); 1.9rev/s -> $slow pattern cycles/frame, wrapped increment=$($slow-[math]::Round($slow))"; "Limits: ideal equations only; no image, clip, audio, tool runtime, test suite, or consumer behavior exercised."'
```

실제 출력:

```text
E7-SMOKE-PROJECTION planar point: fx=1000 X=1 Z=10 -> u=100; fx=2000 X=1 Z=20 -> u=100; scale X=2 Z=20 -> u=100
E7-SMOKE-ROLL approved synthetic values: R=0.3 m v=3 m/s omega=10 rad/s; contact relative velocity=0 m/s
E7-SMOKE-SAMPLING ideal repeated spokes: 2rev/s -> 1 pattern cycles/frame, sampled phase increment=0; 1.9rev/s -> 0.95 pattern cycles/frame, wrapped increment=-0.0500000000000002
Limits: ideal equations only; no image, clip, audio, tool runtime, test suite, or consumer behavior exercised.
```

해석 범위: 두 fx/Z 조합의 한 평면점 투영은 동일, world scale도 미확정; 다층 scene 전체에서 모든 focal/distance가 같은 영상을 만든다는 예는 아니다. 반복spoke의 ideal phase는 실제 셔터 blur·타이어 접촉·camera tracking 진단이 아니다. R/v는 승인된 합성 입력이라고 명시한 수치 예이며 실제 차량 입력이 아니다.

## Cross-owner requests / 부모 통합 검증

- **W4 sources.md:** 위 원본4개 직접 구간/지문과 primary docs5개의 bounded source coverage를 정본 source index에 통합 요청. 새 source ID가 필요하면 W4가 배정한다. E7 label은 감사 ID이지 canonical source 번호를 선점하지 않는다. live web fingerprint 미고정은 그대로 기록한다.
- **Leader:** 여섯 reference 변경의 release docs/version/manifest 통합과 installed-consumer 링크 검사는 leader 소유. 이 보고서/claim slice를 combined ledger로 합칠 때 inherited W4 provider read와 E7 직접 읽기 구분을 보존한다.
- **Evaluation owner:** frozen manifest/assertion 원문은 수정하지 않았다. V-27의 역사 기대문구 `basis -> none stated`는 현재 직접 인용을 추가한 상태와 다르다. 원 prompt/hash를 보존하면서 실제 모듈의 좁은 근거와 미지원 범위를 독립 판정해야 한다. V-22도 word/emotion-mismatch의 기존 historical expectation을 새 임의 규칙으로 바꾸지 않는다.

아래 명령은 **미실행**이며 shared wave 뒤 부모가 실행한다. `<new-E7-integration-run>`은 기존 실패/캐시를 덮어쓰지 않는 새 실제 디렉터리로 치환한다.

```text
python -X utf8 scripts/check_versions.py
python -X utf8 -m pytest -q video-production-assets/scripts
python -X utf8 -m pytest -q
python -X utf8 qa/skill-completeness-95/run_cases.py --manifest qa/skill-completeness-95/case-manifest.json --run-dir <new-E7-integration-run> --case V-20
python -X utf8 qa/skill-completeness-95/run_cases.py --manifest qa/skill-completeness-95/case-manifest.json --run-dir <new-E7-integration-run> --case V-21
python -X utf8 qa/skill-completeness-95/run_cases.py --manifest qa/skill-completeness-95/case-manifest.json --run-dir <new-E7-integration-run> --case V-22
python -X utf8 qa/skill-completeness-95/run_cases.py --manifest qa/skill-completeness-95/case-manifest.json --run-dir <new-E7-integration-run> --case V-23
python -X utf8 qa/skill-completeness-95/run_cases.py --manifest qa/skill-completeness-95/case-manifest.json --run-dir <new-E7-integration-run> --case V-25
python -X utf8 qa/skill-completeness-95/run_cases.py --manifest qa/skill-completeness-95/case-manifest.json --run-dir <new-E7-integration-run> --case V-27
```

추가 read-only integration scenario(미실행):

1. 20:6회 series에 TierA와 배경 extras가 있을 때7뷰 수를 source 보장으로 말하지 않고 계약으로 설명; crowd clip 없이 지각 규모 pass 금지.
2. 21:반복 spokes가 정지/역회전한 영상에서 camera/ground/contact interval 없이 rolling failure 또는 aliasing을 확정하지 않음. straight-alpha edge 문제의 실제 compositor input 형식만 확인; 무조건 lightwrap/grain 추가 안 함.
3. 22:최종 오디오/영상 없는 한 줄에는 annotation/estimated timing만,2frame 자동offset·한국어 phoneme mapping·코미디 반응 시간 발명 안 함. v4 unsupported Speed/SSML과 web 무료재생성의 기존 범위 유지.
4. 23:이미 balance/match가 group node에서 유효한 실제 프로젝트에 빈 Shot Match가 있어도 node 존재만으로 실패/새 조정 안 함. editable 역할 대응과 실제 인접샷 비교 요구; 피부/플랫폼 효과 pass 발명 안 함.
5. 25:fx/Z가 다른 같은 화면 후보에 물리 focal 확정 안 함. known calibration/geometry가 있는 경우까지 불가능으로 거절 안 함. cropped 이미지의 normalized 좌표를 crop-invariant로 취급 안 함.
6. 27:의도된 축 crossing에 재정위 단서가 있을 때 crossing 자체로 실패 안 함. sample still만 있으면 dynamic quality unverified; approved tolerance 없으면 measured difference만 반환.

전체61개 final arm·상대링크/standalone 설치·실제 앱/매체/청취·독립 재채점은 부모가 소유한다. 이 slice의 수학 console smoke나 source reading을 그 검증의 대체 PASS로 쓰지 않는다.
