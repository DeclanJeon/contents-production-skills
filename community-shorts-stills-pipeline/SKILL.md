---
name: community-shorts-stills-pipeline
version: 1.0
description: 'Produce Korean community-story YouTube Shorts from still illustrations only: measured webtoon-page layout, panel-fill geometry, emotion-cluster narration direction, word-timestamp captions, loudness normalisation, delivery-speed retiming and fail-closed publication. Use for converting an already-drawn still episode into a publishable 9:16 Short, for the panel-fill/head-margin measurement, for post-render speed changes (setpts/atempo), or for auditing such a pipeline on a remote host. Do not activate for generative video models, live-action shoots, or standalone image generation.'
---

# 커뮤니티 썰 정지화면 쇼츠 파이프라인

정지 일러스트만으로 한국 커뮤니티 사연 쇼츠를 만드는 **측정 기반** 파이프라인. 생성형 영상 모델을 쓰지 않는다.

관련 스킬(중복 구현 금지, 참조만): `video-production-assets`(project.json 원장·검증기·스토리보드 계약), `recording-production-history`(이력 기록), `storytelling-with-still-images`(정지 이미지 조립), `storyboarding-video`(샷 분해).

## 적용 순서

1. [파이프라인 단계](references/pipeline-stages.md) — 사연 → 원장 → 내레이션 → 렌더 → 자막 → 라우드니스 → 배속 → 발행 전 게이트.
2. [측정 기하](references/measured-geometry.md) — 웹툰 페이지 템플릿 수치, 패널 채움/머리 여백 계산, 함정(비전 오독) 목록.
3. [배속 전달](references/delivery-speed.md) — 렌더 후 `setpts`/`atempo` 규칙, 원장 비재타이밍 원칙, QA 필드.
4. [서버 운영](references/server-operation.md) — 릴리스 디렉터리, 정책 파일, systemd, 차단 목록, 배포 절차.

## 불변 규칙

- **원장은 60초 기준으로 고정.** `target_duration_s=60`, 샷 윈도우, `audio_cues`, `captions`는 배속 때문에 다시 쓰지 않는다. 배속은 완성 마스터의 타임베이스 변경이다.
- **정지 화면만.** 켄번즈/크롭/컷은 허용, 생성형 모션 모델은 금지.
- **검증 없는 청구 금지.** 비전 모델의 레이아웃 판독은 픽셀 측정과 충돌하면 픽셀이 이긴다.
- **비밀값 비영속.** TTS API 키는 런타임에 자격증명 저장소/환경에서 읽고 `project.json`·이력·로그·커밋·CLI 인자에 남기지 않는다.
- **덮어쓰기 금지.** 렌더러는 기존 출력이 있으면 거부한다. 납품본은 새 버전 파일명으로만 만든다.

## 스크립트

`scripts/render_webtoon_stills.py` — 웹툰 페이지 렌더러 + 배속 패스 (참조 구현, 프로젝트 사본이 정본).
`scripts/verify_delivery.py` — 납품본 기하/길이/프레임/오디오 검증.
