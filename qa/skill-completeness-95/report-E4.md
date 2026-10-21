# E4 근거 감사 인계 — review 요청

점수/완료 gate 통과 주장은 없다. 테스트·빌드·린터·formatter는 실행하지 않았다. provider 호출·원격 접속·업로드·유료 생성·훈련·배포·게시·설정 변경·커밋 없음. 부모 소유 scripts와 공유 manifest/README/CHANGELOG/sources는 수정하지 않았다.

## 변경 파일 / 관측 결함

- `higgsfield-video-replicate/references/assembly.md`: VO asplit의 미소비 `[sc]` 출력 제거. 동일 인코더명만으로 concat 호환성 확정, 공통 grade가 변동을 숨긴다는 보장, dissolve overlap을 무시한 총길이 설명을 수정. 단일 grade workflow는 보존하되 필요한 source correction 기록 허용.
- `higgsfield-video-replicate/references/prompts.md`: reference가 이미 룩을 보장한다는 표현, 보편 4–30초, 200토큰 초과 왜곡 확정 표현을 제한. 기존 템플릿/기능 보존.
- `higgsfield-video-replicate/references/analysis.md`: scene pass 주석과 본문의 실제 cut 확정 모순 제거. threshold/beat count를 예시로 명시. 현재 선택 모델의 실제 duration 계약 요구.
- `higgsfield-video-replicate/references/consistency.md`: 직접 확인되지 않은 numeric/API 표를 verified로 부르던 문제 수정. exact 30 images/50 media/mode/Soul 조건은 보존하되 현 계약 재검증 전 제출 금지. identity/anchor를 결과 보장으로 부르지 않음.
- `higgsfield-youtube-thumbnail/references/prompt-contract.md`: subject 비율/rig/4K/identity-lock을 house prompt 의도로 한정. preserved CLI는 현 executor 계약이 아님을 명시.
- `higgsfield-youtube-thumbnail/references/text-overlay-bake.md`: always legible/zero dependencies/proven presets/폰트 인기 순위의 무근거 표현 수정. Canvas sample은 frosted pill/marker/backdrop 효과를 구현하지 않는다는 실제 코드 범위 명시; 기능 삭제 없이 해당 preset drawing 또는 inspected HTML 경로 요구. 명시 폰트와 얇은 serif stroke가 기본 체크리스트에 의해 덮이지 않도록 수정. API 근거/nullable export/CORS 한계 추가. 실행 코드 자체는 미수정.
- `higgsfield-websites/references/website-flow.md`: 모든 이미지에 Higgsfield CLI 허용이라는 package gate 충돌 제거. 명시 animation 선택이 있어도 반드시 재질문하던 모순 제거. unresolved 기본값은 지출/업로드/live 권한이 아님.
- `higgsfield-websites/SKILL.md`: two/both flows를 three/shared branch index로 정정. 원래 동의 gate 보존.
- `community-shorts-stills-pipeline/references/delivery-speed.md`: 고정 18 shots를 선언된 1..20으로 정정. historical AAC 숫자를 현 실측/보편 디코더 사실로 쓰지 않음.
- `community-shorts-stills-pipeline/references/server-operation.md`: 별도 운영 runbook/미번들 구현/현재 호스트 미검증 경계. 과거 Sheets scope와 egress 관찰을 현 계정 상태로 취급하지 않음. 운영 명령은 실행하지 않음.
- `community-shorts-stills-pipeline/references/pipeline-stages.md`: cue SRT만으로 실제 word timestamps를 확정하는 잔여 모순 수정. Google scope 과거 실측의 현 계정 승격 금지.
- `qa/skill-completeness-95/claims-E4.tsv`, 이 보고서.

`thumbnail-frameworks.md`의 부모가 추가한 Block metadata는 그대로 보존했다. 프레임워크 전체의 외부 출처나 성과를 새로 입증한 것은 아니다.

## 직접 읽은 원문 / 계약

- Block original rendition `E:/Book/06_Book/콘텐츠_제작/md/비주얼 스토리 - 브루스 블록.md`, raw L275–283 전체, embedded pp137–141, READ-PARTIAL. 368221 bytes; SHA256 `403172711929152d7019ccbab9043fc0ba8c512606fc14375ef6e78cc410392c`. hash/bytes를 로컬 명령으로 직접 확인. 텍스트의 tonal contrast→line/edge/contour 가시성만 지원. 그림을 직접 보지 않았고 16-framework taxonomy, 5 concepts, CTR, 120px/1초 threshold는 지원하지 않는다.
- [MDN FontFaceSet.load](https://developer.mozilla.org/en-US/docs/Web/API/FontFaceSet/load), READ-FULL reader 응답, 2026-10-17: Promise/loaded face, individual glyph coverage 미보증.
- [MDN canvas.toBlob](https://developer.mozilla.org/en-US/docs/Web/API/HTMLCanvasElement/toBlob), READ-FULL reader 응답, 2026-10-17: nullable blob, origin-clean restriction, PNG support. Live URL reader에는 고정 rendition bytes/hash가 없어 TSV에 N/A-live-reader로 기록; 고정 증거 snapshot 요구를 충족했다고 주장하지 않는다.
- `xd://mcp__higgsfield_models_explore` 전체 schema 문서 직접 읽음. get으로 selected model 확인하는 방법만 입증; provider get/list 호출은 하지 않았다.
- 설치된 `ffmpeg -hide_banner -h filter=sidechaincompress` 전체 출력 직접 읽음: main/sidechain 2 inputs, 1 output.
- 공식 FFmpeg filters URL은 첫 300줄 목차만 열림. 상세 atempo/xfade 계약을 읽었다고 주장하지 않는다. URL grep 실패는 xd://report_issue로 보고했다.
- `report-W6.md`, `claims-W6.tsv`, `provider-contract-observations.json` 전체 읽음. 이 기록의 provider 결과는 predecessor/leader 관찰이며 E4 새 관찰이 아니다. missing explainer 조회를 반복하지 않았다.

## Reference coverage — 읽은 범위와 미검사 입력

### Full relevant small references 직접 읽음

- replicate: `analysis.md`, `consistency.md`, `assembly.md`, `prompts.md` 전체.
- thumbnail: `prompt-contract.md`, `text-overlay-bake.md`, `thumbnail-frameworks.md` 전체.
- shorts: `delivery-speed.md`, `server-operation.md`, `pipeline-stages.md` 전체.

### Website: 37개 reference filename inventory, 전체 감사 아님

`SKILL.md` 전체 직접 읽음. 분기 파일은 수정 전 `website-flow.md` L1–98, `app-flow.md` L1–88, `game-flow.md` L1–103만 읽음. 각 나머지 본문은 미검사. 자동 펼침 footer는 읽은 범위로 계산하지 않는다.

다음 34개 reference 본문은 E4가 읽지 않았다:

- 공통/launch: `app-cover.md`, `runtime-and-infra.md`, `security.md`.
- website design/animation: `design-recipe.md`, `wow-catalog.md`, `wow-maker.md`, `reference-boards.md`, `asset-system.md`, `image-to-code.md`, `design-taste-frontend.md`, `review-rubric.md`, `seo.md`, `scroll-scrub.md`, `scroll-scrub-asset-react.md`, `scroll-scrub-asset-css.md`, `scroll-scrub-asset-video.md`.
- app: `app-quickstart.md`, `quanta-design.md`, `app-layouts.md`, `fnf-sdk.md`, `fnf-react.md`, `auth.md`, `containers.md`, `cover-animator.md`, `contest.md`.
- game assets: `game-design-system.md`, `game-stylization.md`, `game-2d-animation.md`, `game-textures.md`, `game-3d-animation.md`, `game-procedural-animation.md`, `game-audio.md`, `game-meshy-api.md`, `game-meshy-input-rules.md`.

website scripts 전부 미검사/미수정. 인벤토리와 flow excerpt로 그 계약의 정확성/보안/접근성/실제 persistence를 승인하지 않는다.

### Other uninspected inputs

E4는 explainer `SKILL.md`/`references/prompts.md`, replicate `SKILL.md`, thumbnail `SKILL.md`, shorts `SKILL.md`/`measured-geometry.md`/scripts를 새로 읽지 않았다. W6가 읽었다는 보고와 구별한다. explainer assembler는 기존 차단 상태를 보존하며 유료 선행 작업 없음.

## 실제 로컬 비테스트 smoke

### E4-SOURCE-01

```powershell
powershell -NoProfile -Command "Get-FileHash -Algorithm SHA256 -LiteralPath 'E:/Book/06_Book/콘텐츠_제작/md/비주얼 스토리 - 브루스 블록.md'; (Get-Item -LiteralPath 'E:/Book/06_Book/콘텐츠_제작/md/비주얼 스토리 - 브루스 블록.md').Length"
```

exit 0, 위 SHA/368221 관찰.

### E4-SMOKE-01

```powershell
ffmpeg -hide_banner -h filter=sidechaincompress
ffmpeg -hide_banner -f lavfi -i sine=frequency=220:duration=1 -f lavfi -i sine=frequency=440:duration=1 -filter_complex "[1:a]asplit=2[voout][scin];[0:a][scin]sidechaincompress=threshold=0.05:ratio=8:attack=50:release=400[duck];[duck][voout]amix=inputs=2:duration=first[mix]" -map "[mix]" -f null -
```

각 exit 0. graph smoke 출력 `time=00:00:01.00`, mono 44100 Hz pcm_s16le, audio 86KiB, null sink. 미소비 split output 없는 실제 filter 실행만 입증. 파일/외부 side effect 없음. 소리 청취, real VO intelligibility, loudnorm, grade, concat, mux, 비디오 QC는 미검증.

## 잔여 exact claims / 통합 요청

1. seedance `30 images/50 references/omni_reference anchors/no Soul`, thumbnail preserved CLI flag/result shapes/version compatibility는 이번 pass의 현 provider 계약으로 입증하지 못했다. safe pre-submit contract blocker를 명시했으며 valid라고 승인하지 않는다. 무료 조회조차 실행하지 말라는 이번 계약을 지켰다.
2. Book scope는 contrast만 지원. taxonomy/information-gap/rig/40–60%/2–4 words/stroke proportions/폰트 효능 등 house recipe의 외부 유래·성과 근거는 미완성. 자체 운영 선택으로 사용 가능하다는 설명이 외부 craft 근거 면제나 score-5 증명이 아니다.
3. overlay sample의 font stylesheet race, null export 처리, preset별 CSS/canvas 동등성, 4K shadow/letter-spacing scaling은 실제 browser 결과가 필요하다. 이 pass는 근거/한계와 checklist 모순을 수정했지 JavaScript를 완성/검증했다고 하지 않는다.
4. 운영 runbook의 OAuth 회전/버전별 옵션/systemd 최초 실행/멱등성/Drive·Sheets 상태 코드 등은 원격 구현·공식 버전 계약이 미검증이다. 권한 없는 호스트 실행으로 증거를 만들지 않았다.
5. website 34개 미열람 reference와 3개 flow 후반은 위 coverage 그대로 독립 reviewer가 제외/잔여로 취급해야 한다. 전체 web audit 완료 또는 37 refs evidence-bound 주장 금지.
6. 부모: verifier speed/hash regression 및 실제 media smoke 소유 유지. E4는 scripts 편집 없음. 리더: 위 변경을 CHANGELOG/version 통합에 반영. W4: Block rendition source ID를 canonical sources에 연결하되 기존 W6 request와 중복 record를 만들지 말 것.

## 부모 통합 smoke/test 명령 — 여기서는 미실행

```powershell
python -X utf8 -m pytest
python -X utf8 scripts/check_versions.py
python -X utf8 community-shorts-stills-pipeline/scripts/render_webtoon_stills.py --help
python -X utf8 community-shorts-stills-pipeline/scripts/verify_delivery.py --help
```

위 E4-SMOKE-01 명령은 공유 편집 후 그대로 재실행 가능하다. 실제 media 경로는 부모 생성 fixture로 정해지므로 가짜 filename을 실행 명령처럼 제시하지 않는다. verifier에 그 fixture와 missing/hash-mismatch/speed-nonfinite variants를 넣어 관찰할 것. 자막 cue-only 입력은 word alignment blocker, local-only website+명시 non-animated 입력은 재질문/원격 동작 없이 로컬 산출, thumbnail explicit serif font는 얇은 stroke와 실제 exported crop/120px preview 검수 시나리오가 필요하다. JS/browser/real-video 경로의 실행 증거는 본 pass에 없으며 정식 61-case 평가와 독립 채점은 부모 소유다.
