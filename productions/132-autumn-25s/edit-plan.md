# EDIT01 v1.3 — 편집 계획 (deterministic post-render assembly)

실행 스크립트: `scripts/render_ad.py`. 정본 원장은 `project.json`이다. 이 문서는 편집 결정만 기록하며, 실제 실행 결과는 스크립트가 `qa/assembly.json`에 쓴다.

## 1. 입력과 계약

- 입력: `videos/SH01.mp4 … SH05.mp4` — Flow Omni 1.1 Flash가 부모가 다운로드한 실제 클립(예정 720p, 9:16, 6s). 부모는 다운로드만 소유하고 이 스크립트는 후반만 담당한다.
- 출력: `delivery/132-autumn-25s.mp4` — 1080x1920, 30fps, 750f, H.264, yuv420p, `+faststart`, 무음 마스터.
- 트림: 소스 시각 0에서 SH01 4s / SH02 5s / SH03 6s / SH04 6s / SH05 4s (합 25.0s). 시간 선택이며 시간 압축이 아니다.
- 원본 길이가 트림보다 짧으면 스크립트는 실패한다 — 정지 반복이나 임의 연장으로 대체하지 않는다.
- SH01/SH05의 Flow 입력은 **빈 배경 플레이트**였으므로, 이 단계에서 제공된 제품 RGBA 오버레이(`images/P01_product_overlay.png`, `images/P10_product_overlay.png`)를 그대로 0:0에 정적 합성한다. 위치·크기는 `scripts/composite_products.py`와 `qa/product-compositing.json`의 기록값이다.

## 2. 샷별 편집 지시

| 샷 | 소스 | 트림(s) | 길이(f@30) | 제품 오버레이 | 자막 |
|---|---|---|---|---|---|
| SH01 | videos/SH01.mp4 | 0–4.0 | 120 | P01_product_overlay.png (하단 1360px) | 없음 |
| SH02 | videos/SH02.mp4 | 0–5.0 | 150 | 없음 | 없음 |
| SH03 | videos/SH03.mp4 | 0–6.0 | 180 | 없음 | 없음 |
| SH04 | videos/SH04.mp4 | 0–6.0 | 180 | 없음 | 없음 |
| SH05 | videos/SH05.mp4 | 0–4.0 | 120 | P10_product_overlay.png (하단 1300px) | SH05 전체 4초 고정 가독 |

정규화 체인(샷 공통): `scale=1080:1920:force_original_aspect_ratio=increase:flags=lanczos → crop=1080:1920 → fps=30 → format=yuv420p → setsar=1`. 가운데 크롭으로 채우며, 시뮬레이션 모션/정지 대체는 사용하지 않는다.

## 3. 클로징 타이포그래피 (SH05 전용)

프로젝트 카피(project.json CAP01/CAP02)의 세 줄을 마지막 4초에 올린다:

- `가을의 저녁, 빛을 담는 루틴.` — 56px, 아이보리 `#F0ECE2`
- `132 · VITA-C25.5` — 64px, 골드 `#D8B676` (위에 가는 골드 룰)
- `15ml · 132.co.kr` — 40px, 아이보리

레이아웃: 텍스트 블록은 y≈1410–1700px — 제품 하단(SH01 1360 / SH05 1300px) 아래, 프레임 하단 세이프 마진 150px 안쪽. 블록 뒤로 네이비 `#0D1528` 그라디언트 밴드(알파 최대 ~190→전역 불투명도 0.8 적용 시 ~152)를 깔아 라이브 플레이트 위 가독성을 확보한다. 폰트는 설치된 한글 지원 폰트만 쓴다(`C:\Windows\Fonts\malgun.ttf` 우선, 없으면 `malgunbd.ttf` → `NotoSansKR-VF.ttf` → `gulim.ttc`). 캡션 PNG(`delivery/caption-sh05.png`)는 스크립트가 Pillow로 실행 시에만 생성한다; 패널/라벨에 문자를 굽지 않는다.

## 4. 오디오

`no_dialogue`. `-an`으로 모든 입력 오디오를 버리고 무음으로 납품한다. Flow 네이티브 오디오가 확인돼도 이 스크립트는 음악/앰비언스를 만들지 않는다 — 무음 마스터가 허용 범위다.

## 5. 인코딩과 산출

- 세그먼트 중간파일: libx264, preset medium, CRF 14(근-무손실), yuv420p, `-an`. `delivery/segments/`.
- 최종 결합: concat demuxer → libx264, preset slow, CRF 18, yuv420p, 30fps, `-movflags +faststart`, `-an`.
- 기록: `qa/assembly.json`에 ffmpeg/ffprobe 버전, 입력별 해시·해상도·fps·길이·실제 트림, 실행한 명령 전체, 출력 해시·길이·코덱·fps를 남긴다. 부모가 `ffprobe -count_frames`로 750f를 입증한다.

## 6. 실행

```powershell
cd productions/132-autumn-25s
python scripts/render_ad.py            # 입력 검사 → 렌더 → qa/assembly.json
python scripts/render_ad.py --dry-run  # ffprobe만, ffmpeg 미실행
```

차단 조건: `videos/SH0x.mp4` 누락, 원본 길이 < 트림, ffmpeg/ffprobe/Pillow 부재, 한글 폰트 부재 → 스크립트는 치환 없이 종료한다.

초기 조립은 SH01 누락으로, 정상 SH01 확보 뒤 최신 호출은 `videos/SH02.mp4` 누락으로 종료했다(`qa/assembly-after-recovery.json`). `delivery/caption-sh05.png`와 `delivery/endcard-layout.png`는 실제 생성·열람한 정지 타이포그래피 자료다. 복구된 `videos/SH01.mp4`의 공급자 워터마크 처리와 제품 영상 합성은 아직 검수하지 않았다. 부분 프롬프트 원본이나 정지 패널을 나머지 4개 소스 대신 넣지 않는다. 최종 25초/750프레임은 아직 검증하지 않았다.
