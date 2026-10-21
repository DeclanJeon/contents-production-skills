# Image model branches — craft/reference only (ineligible in this package)

Package policy (see `package-gate.md`) excludes Higgsfield image generation and image edits:
in this package none of the recipes below may be submitted. They are preserved for model
selection knowledge and for contexts where this skill runs without the package constraint —
and so that a request can be routed to the right owner or an authorized eligible executor.
Do NOT treat a listed model as currently available or priced; check `higgsfield model get
<jst>` in any context where image generation is actually permitted.

Direct contract read 2026-10-17: [official MODELS.md](https://github.com/higgsfield-ai/cli/blob/main/MODELS.md), image tables, supports listed CLI fields only where the named row exists (including Recraft model_type and Soul quality/soul-id). Taxonomy, quality preferences, backend dimension mappings and style/image exclusions below are not independently validated outcomes; unmatched details remain historical/unverified and require current model/preset contracts. No image submission is authorized by this evidence.

## Routing first — specialized image owners

| Request | Owner |
|---|---|
| Complete brand identity, logo system, palette, typography, brandbook, packaging, signage, coordinated branded asset suite | `higgsfield-brandkit` |
| YouTube thumbnail, Shorts cover, Instagram video cover | `higgsfield-youtube-thumbnail` |
| Brand product visual (Pinterest pin, lifestyle, hero banner, ad pack, virtual try-on) | `higgsfield-product-photoshoot` |
| Marketplace listing main/secondary/A+ images | `higgsfield-marketplace-cards` |
| Branded ad image with avatar + product (Marketing Studio shape) | Marketing Studio Image (`marketing_studio_image`) |
| Train a real person's face for reuse | `higgsfield-soul-id` |

## Image model taxonomy (selection craft)

- Soul Character (reference id from `higgsfield-soul-id`) → Soul 2.0 (`text2image_soul_v2`) for stills, Soul Cinema (`soul_cinematic`) for cinematic.
- New original person — UGC, editorial, fashion, lifestyle → Soul 2.0.
- Cinematic still frame → Soul Cinema (`soul_cinematic`).
- Character sheet, one-shot face from reference photos, or face edit on a real photo → Seedream 5.0 Pro (`seedream_v5_pro`).
- Locations / environments / no-people scenes → Soul Location.
- Logo, icon, vector-like illustration, brand mark, controlled-palette graphic → Recraft V4.1 (`recraft_v4_1`, often with `--model_type vector`).
- Cartoon or illustrated characters, heavily textured photos → Nano Banana 2 (`nano_banana_flash`). The id `nano_banana_2` is an alias for Nano Banana Pro, not Nano Banana 2.
- Default for everything else → GPT Image 2.5: graphic design, UI, banners, typography, product concepts, editing, high-fidelity general generation.
- Cheaper or faster on user request → Nano Banana 2 Lite (`nano_banana_2_lite`) for reference edits, Z Image for drafts.

## 작업 종류별 모델 선택 관찰 (GUIDE-01, craft 참고)

아래는 사용자 제공 제작 가이드북(GUIDE-01, 통합 기록은 [video-production-assets 출처 등록](../../video-production-assets/references/sources.md))이 **실제 제작에서 역할별로 골랐다고 기록한** 이미지 모델의 역할이다. 이 표는 **선택 craft 참고**이며 capability·품질·가격 주장이 아니다. 같은 출처도 모델명이 바뀌는 것(예: GPT Image 2.5의 Flare와 Sunburst을 혼동해 한쪽만 고른 사례)을 경고하므로, 어떤 모델을 쓰든 현재 `higgsfield model get <jst> --json` 계약으로 확인하기 전에는 실재 모델·입력 필드를 단정하지 않는다. **출처의 서비스·모델 기본값을 이 패키지의 기본값으로 채택하지 않는다.**

| 작업 | 가이드북이 기록한 선택 | 관찰된 이유 |
|---|---|---|
| 캐릭터 시트·수정·기본 | GPT Image 2.5 / Nano Banana Pro | 캐릭터 시트·수정의 기본 모델 |
| 실감 조명·배치가 중요한 장면 | WAN 2.7 Image Pro | 실감 조명과 인물 배치 |
| 강한 감정의 키 비주얼 | Seedream 5 Pro | 강한 인물의 키 비주얼 |
| 참고/가져오기 | Nano Banana Pro | Google Nano Banana 모델과 서비스 이름을 구분해 호출 |

이 표는 패키지 정책(Higgsfield 이미지 생성 제외)과 별개로 **다른 이미지 실행 소유자**(`codex-imagen` 기본 경로 등)가 같은 작업 분할을 참고할 수 있게 한다. 어느 경우에도 모델을 바꾸면 동일 인물의 얼굴이 달라질 수 있으므로, 한 프로젝트에서 정체성을 유지해야 하는 이미지는 한 모델·하나의 시트 흐름 안에 묶고, 모델을 갈아탄 순간을 원장에 기록한다. 모델 선택은 프로젝트 단위 결정이며, 위 역할을 기본 라우팅으로 고정하지 않는다.

## CLI shapes (craft reference)

```bash
higgsfield generate create gpt_image_2_5 --prompt "neon city at dusk" --aspect_ratio 16:9 --resolution 2k --wait
higgsfield generate create nano_banana_flash --prompt "anime character concept, expressive pose" --image ./ref.png --wait
higgsfield generate create text2image_soul_v2 --prompt "..." --soul-id <soul_ref_id> --quality 2k --wait
higgsfield generate create marketing_studio_image --prompt "..." --aspect_ratio 1:1 --resolution 2k --wait
```

Soul image quality: for `text2image_soul_v2` and `soul_cinematic`, pass `--quality 1.5k` or
`--quality 2k`. These are UI-facing tiers; the backend maps them to `720p`/`1080p` and
model-specific dimensions from the selected `--aspect_ratio`. `soul_location` has no quality
selector; it uses fixed dimensions per aspect ratio.

Soul style presets: `text2image_soul_v2` accepts `--style_id <uuid>`; list curated styles
with `higgsfield preset list soul-v2` and pass the chosen id. `--style_id` combines with
`--soul-id` but not with an image reference. `soul_cinema_studio` also accepts `--style_id`.
