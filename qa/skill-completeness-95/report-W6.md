# W6 구현 인계 — 독립 검토 필요

점수는 부여하지 않는다. 테스트/린터/빌드는 공유 편집 후 부모 실행으로 유예했다. 외부 생성·업로드·훈련·배포·게시·커밋·설정 변경 없음.

## 변경 파일과 수정 결함

- `higgsfield-video-explainer/SKILL.md`: 10초를 보편 모델 제한으로 취급하지 않도록 명시. 현 조립 모델 부재를 MCP와 CLI 양쪽에서 확인하고 유료 선행 작업 전에 차단. 단어 수/예상 조립 길이와 실제 측정 분리.
- `higgsfield-video-replicate/references/analysis.md`: 장면 검출은 후보임을 명시. 시각 추정 렌즈/룩을 메타데이터 실측으로 보고하지 않도록 관찰 방법·구간·확신도·unknown 계약 추가.
- `higgsfield-youtube-thumbnail/SKILL.md`: 실제 납품 크롭과 약 120px 미리보기 검수, UI 가림 미검증 표기.
- `higgsfield-youtube-thumbnail/references/thumbnail-frameworks.md`: 직접 읽은 대비 원문과 지원 범위 명시. CTR/1초/120px/프레임워크 개수는 입증된 성과가 아닌 authored heuristic.
- `higgsfield-websites/SKILL.md`: 하위 flow 전체에 원격 생성·업로드·유료 자산·live deploy·feed listing·contest 동의 범위 적용. 상태 혼동 금지.
- `community-shorts-stills-pipeline/references/measured-geometry.md`: 원본 식별 없는 과거 측정값을 현재 재측정 사실로 표시하던 문제 수정. 수치는 템플릿으로 보존.
- `community-shorts-stills-pipeline/references/pipeline-stages.md`: SRT만으로 Typecast 단어 타임스탬프 출처를 고정하던 문제 수정. 실제 verifier 범위와 별도 운영 스크립트 미번들 경계 명시.
- `qa/skill-completeness-95/claims-W6.tsv`: 주장별 증거와 미검증 상태.

## 직접 읽은 근거

- 원문 rendition: `E:/Book/06_Book/콘텐츠_제작/md/비주얼 스토리 - 브루스 블록.md`, L275–283, embedded pp137–141, READ-PARTIAL. 368221 bytes, SHA256 `403172711929152d7019ccbab9043fc0ba8c512606fc14375ef6e78cc410392c`. 대비에 의한 선/윤곽 가시성만 지원. 전권/다른 rendition 읽음 주장 없음.
- 공식 `get_workflow_instructions({})` catalog: 현재 `faceless-video` v2.4 존재. 기존 lane을 무단 교체하지 않음.
- 공식 `models_explore` schema 및 get 응답: `gemini_omni` 4–10초/720p/16:9·9:16, `explainer_video` not found.
- 공식 `deploy_website`, `publish_website` 문서/전체 schema 직접 읽음. deploy는 live, listing과 별개. publish 미배포 fallback도 있을 수 있으므로 도구 이름만으로 비배포를 보장하지 않음.
- 로컬 `verify_delivery.py` L1–126 전체 직접 읽음. render acceptance 전체를 검사하는 도구가 아님.
- replicate `analysis.md`, `consistency.md`; thumbnail `thumbnail-frameworks.md`; shorts `pipeline-stages.md`, `measured-geometry.md`; 지정 SKILL 관련 구간 직접 읽음.

## 실제 실행한 비테스트 smoke

### W6-SMOKE-01

```powershell
python -X utf8 -c "import runpy,tempfile,pathlib; m=runpy.run_path('community-shorts-stills-pipeline/scripts/verify_delivery.py'); d=tempfile.TemporaryDirectory(); p=pathlib.Path(d.name)/'unapproved.mp4'; p.write_bytes(b'local fixture, not media'); print(m['verify'](p)); d.cleanup()"
```

관찰: `{'ok': False, 'problems': ['missing QA sidecar unapproved.qa.json']}`. 임시 입력 자동 정리. 실제 미디어 정상 경로/기하/음성 품질 증명이 아님.

### W6-SMOKE-02

```powershell
higgsfield model get explainer_video --json
```

관찰: `Error: No model with job_type "explainer_video".`, exit 4. MCP not-found와 독립적인 CLI 조회. 생성 없음. 따라서 현 lane end-to-end live 완료는 차단 상태.

### W6-SOURCE-01

```powershell
powershell -NoProfile -Command "Get-FileHash -Algorithm SHA256 -LiteralPath 'E:/Book/06_Book/콘텐츠_제작/md/비주얼 스토리 - 브루스 블록.md'; (Get-Item -LiteralPath 'E:/Book/06_Book/콘텐츠_제작/md/비주얼 스토리 - 브루스 블록.md').Length"
```

위 원문 hash/bytes 관찰. 초기 `$p` 변수 방식은 외부 shell 확장으로 실패했으며 직접 경로 명령으로 해소했다. `python`, `ffmpeg`, `ffprobe`, `higgsfield` 실행 경로 발견; 실제 렌더 미실행.

## 남은 증거/통합 요청

- 모든 triggered web/game/SDK reference의 전수 주장 감사 완료를 주장하지 않는다. `prompt-contract.md`, `text-overlay-bake.md`, replicate assembly/prompts, shorts speed/server refs와 website 대형 reference tree의 전체 T3 provenance 검토는 미완료 범위다. 현재 파일 존재나 과거 점수를 새 읽기 근거로 승격하지 않는다.
- W4 요청: canonical `sources.md`에 W6-BLOCK-VISUAL의 exact rendition/hash/bytes/부분 읽기 구간과 좁은 지원 범위를 결속. 공유 파일은 수정하지 않음.
- 리더 요청: 위 변경을 CHANGELOG에 기록, 필요시 패키지 버전 통합. manifest/README/CHANGELOG는 소유권상 미수정.
- 독립 리뷰 필요: 동의 계약이 하위 자동 deploy/publish recipe보다 우선 적용되는지 경계 사례 평가. 계정/생성/배포/게시 실제 동작은 미검증.
- verifier의 잘못된 speed 처리와 hash 필수성 등 코드 문제는 이번 문서 편집에서 수정/테스트하지 않았다. 부모가 코드 검토 범위에 포함할 것. 이 문서는 verifier 전체 안전성을 보증하지 않는다.

## 부모 실행용 정확 명령과 시나리오

```powershell
python -X utf8 community-shorts-stills-pipeline/scripts/render_webtoon_stills.py --help
python -X utf8 community-shorts-stills-pipeline/scripts/verify_delivery.py --help
python -X utf8 community-shorts-stills-pipeline/scripts/verify_delivery.py <actual-local-delivery.mp4> --json
python -X utf8 scripts/check_versions.py
```

`<actual-local-delivery.mp4>`는 부모의 승인된 로컬 fixture 경로로 치환해야 한다. 본 직원은 이 help/통합 명령을 실행하지 않았다. 정상 fixture와 sidecar 변조/누락 fixture, 작은 썸네일 crop 실물, 추정 렌즈 값만 있는 reference 분석, local-build-only 웹 요청, feed opt-in 없는 live deploy 요청을 평가할 것. 전체 테스트/61개 정식 runner 명령은 W0 manifest와 최종 트리가 확정된 부모 소유 계약을 따른다. 완료 점수나 61개 PASS를 주장하지 않는다.
