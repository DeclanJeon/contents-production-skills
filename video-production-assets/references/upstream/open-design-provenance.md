# open-design 크래프트 각색 이전 기록

- 원본: open-design 스킬 흡수 원장(`docs/superpowers/specs/2026-11-20-open-design-absorption-ledger.csv`)에서 `absorb`로 정한 공개 스킬 저장소 15곳(아래 표). 저장소별 주소·고정 커밋·라이선스를 모두 적는다.
- 확인일: 2026-11-20. 공개 raw 파일 읽기이며 upstream 설치·에이전트·렌더 실행은 하지 않았다.
- 라이선스는 MIT 또는 Apache-2.0만 흡수했다. 저장소 루트 LICENSE를 직접 읽어 확인했고, 사본은 이 `upstream/` 폴더의 `<owner>-<repo>-LICENSE.txt`에 원문 그대로 둔다.
- 이 고지는 아래 `absorb` 행의 각색분에만 적용되며 패키지 전체나 저장소 전체에 라이선스를 부여하는 고지가 아니다. 원본 저장소 전체·예시 미디어·템플릿 코드·바이너리는 배포하지 않는다.
- Apache-2.0 저장소(GoogleCloudPlatform/vertex-ai-creative-studio, nexu-io/open-design, nexu-io/openmotion, Vincentwei1021/video-shotcraft)는 고정 커밋 루트에서 `NOTICE`, `NOTICE.md`, `NOTICE.txt`를 조회했고 모두 없었다(404). 따라서 `-NOTICE.txt` 사본은 없다.

## 저장소와 고정 커밋

| 저장소 | 고정 커밋 | 라이선스 | 저작권 표시(LICENSE 원문) | 고지 사본 | 사본 SHA-256 |
|---|---|---|---|---|---|
| https://github.com/alchaincyf/huashu-art-motion | `26dba25b2b495c2138848c29a2c90df356a20325` | MIT | 2026 alchaincyf (花叔 · 花生) | [alchaincyf-huashu-art-motion-LICENSE.txt](alchaincyf-huashu-art-motion-LICENSE.txt) | `6d6a2a9caf2e6d2b76974050427053b2892d8aa4c33fd168ce63a537fcee9d96` |
| https://github.com/bytedance/deer-flow | `3f86f071f3d26cb3fcf91841523f6f7be2796914` | MIT | 2025 Bytedance Ltd. and/or its affiliates; 2025-2026 DeerFlow Authors | [bytedance-deer-flow-LICENSE.txt](bytedance-deer-flow-LICENSE.txt) | `b23dff4d4bac8d17b6efaaa7e88c2b730149c4dda45699ce676b719cfdffe7e1` |
| https://github.com/Emily2040/seedance-2.0 | `4668457e560eee06e95d7fcfdf441c8c0bba802e` | MIT | 2026 Iamemily2050 (@iamemily2050) | [Emily2040-seedance-2.0-LICENSE.txt](Emily2040-seedance-2.0-LICENSE.txt) | `c84a6216f6e006b4e4a65e9d056837a61ee9c4ca79f43f386df2992bc690a7f6` |
| https://github.com/gnipbao/story-to-handdrawn-video | `198aefa9b298af3a20d3bd757c93433623d38ccd` | MIT | 2026 gnipbao | [gnipbao-story-to-handdrawn-video-LICENSE.txt](gnipbao-story-to-handdrawn-video-LICENSE.txt) | `481521d963c714f9d79b68e0cde61ab0b012e17dc3b90f4ed877717a0c401fa3` |
| https://github.com/GoogleCloudPlatform/vertex-ai-creative-studio | `0ed98d58d53a648bc0c49c9135cb2fbd2292f8e2` | Apache-2.0 | 원문에 저작권자 줄 없음 | [GoogleCloudPlatform-vertex-ai-creative-studio-LICENSE.txt](GoogleCloudPlatform-vertex-ai-creative-studio-LICENSE.txt) | `58d1e17ffe5109a7ae296caafcadfdbe6a7d176f0bc4ab01e12a689b0499d8bd` |
| https://github.com/iart-ai/data-animation-skills | `8ce2709c3992490251e8a991535b1945f01c6865` | MIT | 2026 iart.ai | [iart-ai-data-animation-skills-LICENSE.txt](iart-ai-data-animation-skills-LICENSE.txt) | `33d6cd35a20903b5e968a76a1e584a7aeae2c83e3e58ea58ecc50b889b83e668` |
| https://github.com/iart-ai/explainer-video-skills | `3e2d411b725d9a72939cf8e5eb81579e751373e7` | MIT | 2026 iart.ai | [iart-ai-explainer-video-skills-LICENSE.txt](iart-ai-explainer-video-skills-LICENSE.txt) | `33d6cd35a20903b5e968a76a1e584a7aeae2c83e3e58ea58ecc50b889b83e668` |
| https://github.com/iart-ai/lower-thirds-skills | `aa8ef7ed9fa59d0a79fc57701e493cfd8197b5d8` | MIT | 2026 iart.ai | [iart-ai-lower-thirds-skills-LICENSE.txt](iart-ai-lower-thirds-skills-LICENSE.txt) | `33d6cd35a20903b5e968a76a1e584a7aeae2c83e3e58ea58ecc50b889b83e668` |
| https://github.com/iart-ai/map-animation-skills | `390ca98bbcf2ea88a430a69c0dcbf423e43d075d` | MIT | 2026 iart.ai | [iart-ai-map-animation-skills-LICENSE.txt](iart-ai-map-animation-skills-LICENSE.txt) | `33d6cd35a20903b5e968a76a1e584a7aeae2c83e3e58ea58ecc50b889b83e668` |
| https://github.com/iart-ai/motion-design-skills | `3c129f769d90a1328c209c386492333c9ac62312` | MIT | 2026 iart.ai | [iart-ai-motion-design-skills-LICENSE.txt](iart-ai-motion-design-skills-LICENSE.txt) | `33d6cd35a20903b5e968a76a1e584a7aeae2c83e3e58ea58ecc50b889b83e668` |
| https://github.com/LottieFiles/motion-design-skill | `d77a9fc8cb371cab1ba5420df5bfd232cd14c9bb` | MIT | 2025 LottieFiles | [LottieFiles-motion-design-skill-LICENSE.txt](LottieFiles-motion-design-skill-LICENSE.txt) | `9fc2e8685daa09e28d54b6afa8a38f168417c5735a3cd676c80c159785e93a80` |
| https://github.com/MengTo/Skills | `ef5f85130d083d33e08cb19f6ee23cdde2d406ab` | MIT | 2026 Meng To | [MengTo-Skills-LICENSE.txt](MengTo-Skills-LICENSE.txt) | `b2a071ba22fefd803f4e9d1f5c777dd79c62d191695586a1a73fd4d0ebd051c6` |
| https://github.com/nexu-io/open-design | `5a0c47777975ddb91d09c1c16b423a3ef74bf572` | Apache-2.0 | 원문에 저작권자 줄 없음 | [nexu-io-open-design-LICENSE.txt](nexu-io-open-design-LICENSE.txt) | `9d95806a26532623360eb84bb17d298f394b55ef73fb4c0796d99b4319b2b0da` |
| https://github.com/nexu-io/openmotion | `2b57cf6908af2a31380955380f5a30eb1857a9c1` | Apache-2.0 | 원문에 저작권자 줄 없음 | [nexu-io-openmotion-LICENSE.txt](nexu-io-openmotion-LICENSE.txt) | `cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30` |
| https://github.com/nexu-io/openmotion | `709b10fd9ac5e33f996e035361cbb365d7ff79ae` | Apache-2.0 | 원문에 저작권자 줄 없음 | [nexu-io-openmotion-LICENSE.txt](nexu-io-openmotion-LICENSE.txt) | `cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30` |
| https://github.com/Vincentwei1021/video-shotcraft | `5ddbf521038b0a7accfb6dc1e0a9eb29c67277ab` | Apache-2.0 | 원문에 저작권자 줄 없음 | [Vincentwei1021-video-shotcraft-LICENSE.txt](Vincentwei1021-video-shotcraft-LICENSE.txt) | `b2ce9877a55547ada9b870150664d1468ff777e67cc9888806a73927d31c5771` |

`nexu-io/openmotion`은 두 커밋을 고정했다. 각 행은 자기 커밋을 쓰며 출처 줄도 그 커밋 앞 12자를 쓴다. 두 커밋의 LICENSE는 바이트 단위로 같아 사본 하나를 공유한다.

## 적용 파일

각색분은 아래 파일에 들어간다. 모든 파일이 작업을 마쳐 생겼으며, 각색 절의 `출처:` 줄이 원장 행과 맞는지는 `scripts/test_open_design_absorption.py`가 검사한다.

| 원장 target | 각색 대상 파일 | 원장 행 수 |
|---|---|---|
| 33-motion-style-library | `video-production-assets/references/33-motion-style-library.md`(색인), `video-production-assets/references/motion-styles/*.md` | 76 |
| 30-marketing-story-craft | `video-production-assets/references/30-marketing-story-craft.md` | 2 |
| 03-screenplay | `video-production-assets/references/03-screenplay.md` | 2 |
| 10-evidence | `video-production-assets/references/10-evidence.md` | 1 |
| 06-shots | `video-production-assets/references/06-shots.md` | 1 |
| 25-reference-video-analysis | `video-production-assets/references/25-reference-video-analysis.md` | 1 |
| 13-ideation-brand | `video-production-assets/references/13-ideation-brand.md` | 1 |
| 08-animation | `video-production-assets/references/08a-motion-craft.md` | 7 |
| 09-edit | `video-production-assets/references/09a-short-form-edit-recipes.md` | 6 |
| 19-brand-product-integration | `video-production-assets/references/19a-product-promo-formulas.md` | 13 |
| 23-finishing-platform | `video-production-assets/references/23a-captions-layout.md` | 6 |
| 11-ai-handoff | `video-production-assets/references/11a-ai-video-prompting.md` | 4 |
| 29-reference-driven-production | `video-production-assets/references/29a-template-recreation.md` | 3 |
| storytelling-with-still-images | `storytelling-with-still-images/references/still-motion-recipes.md` | 2 |

## 직접 확인한 원본과 raw SHA-256

각 행은 고정 커밋의 `SKILL.md` 원본 bytes SHA-256이다(원장 `sha256` 열과 같다). 저장소 루트 LICENSE도 읽었다. 이 목록은 `absorb`로 정한 행이며, 각색이 끝나 원장 `status`가 모두 `absorbed`로 바뀌었다. 원문을 통째로 옮기지 않고 패키지 말투의 한국어 절로 다시 썼다.

### alchaincyf/huashu-art-motion@26dba25b2b49

| slug | 원본 경로 | raw bytes SHA-256 | 대상 |
|---|---|---|---|
| `huashu-art-motion` | `SKILL.md` | `605f45fcd19d7059b4e1bea94618515c766d816a583abf12aeae763404f44d71` | 08-animation |

### bytedance/deer-flow@3f86f071f3d2

| slug | 원본 경로 | raw bytes SHA-256 | 대상 |
|---|---|---|---|
| `video-generation` | `skills/public/video-generation/SKILL.md` | `ca58db5c790c7b417f86e33f763615cacfb70818e87b228764caa0d598d0b7cc` | 11-ai-handoff |

### Emily2040/seedance-2.0@4668457e560e

| slug | 원본 경로 | raw bytes SHA-256 | 대상 |
|---|---|---|---|
| `seedance-20` | `SKILL.md` | `9cc2161b0dad7f0fb75490106eda34f314de503bcadfba515364053cf7bdcd92` | 11-ai-handoff |

### gnipbao/story-to-handdrawn-video@198aefa9b298

| slug | 원본 경로 | raw bytes SHA-256 | 대상 |
|---|---|---|---|
| `story-to-handdrawn-video` | `skill-package/story-to-handdrawn-video/SKILL.md` | `bdd0ee0c779befc50d9b35707f2361e05e85e9a8226d1743bf46583e723db5c3` | storytelling-with-still-images |

### GoogleCloudPlatform/vertex-ai-creative-studio@0ed98d58d53a

| slug | 원본 경로 | raw bytes SHA-256 | 대상 |
|---|---|---|---|
| `genmedia-video-editor` | `experiments/mcp-genmedia/skills/genmedia-video-editor/SKILL.md` | `b24224e0ea40e2e2c29459f478c0e8e002c7b0dbd48cd460e4ec412cdd855927` | 11-ai-handoff |

### iart-ai/data-animation-skills@8ce2709c3992

| slug | 원본 경로 | raw bytes SHA-256 | 대상 |
|---|---|---|---|
| `chart-animation` | `skills/chart-animation/SKILL.md` | `4a77aa776f458a1e474ad411fdedee7091c0cf95fca456f0b481ad00543c5d49` | 33-motion-style-library |

### iart-ai/explainer-video-skills@3e2d411b725d

| slug | 원본 경로 | raw bytes SHA-256 | 대상 |
|---|---|---|---|
| `isometric-animation` | `skills/isometric-animation/SKILL.md` | `7ef259e68a5167463ec991417ad6ce86d5aa056a9cd32bfc3ded6c484afdbf77` | 33-motion-style-library |
| `whiteboard-animation` | `skills/whiteboard-animation/SKILL.md` | `42e9519e7eea3f3170e39edad9fe721a5c95bfe763e725713c6be2b0050fb2c8` | 33-motion-style-library |
| `wrapped-video` | `skills/wrapped-video/SKILL.md` | `9c5b208604746629e1344f84b6199dd9a6d173ecfdae63225c55701ee92c2742` | 33-motion-style-library |

### iart-ai/lower-thirds-skills@aa8ef7ed9fa5

| slug | 원본 경로 | raw bytes SHA-256 | 대상 |
|---|---|---|---|
| `lower-thirds` | `skills/lower-thirds/SKILL.md` | `754a558116f15eabd639977a3c44c4b1ceb80fcd99c96c30806a19c800e9fa36` | 23-finishing-platform |

### iart-ai/map-animation-skills@390ca98bbcf2

| slug | 원본 경로 | raw bytes SHA-256 | 대상 |
|---|---|---|---|
| `map-animation` | `skills/map-animation/SKILL.md` | `cadb7b4c56e0ba44ec58dd39df19fc56d4adeedb584fadb7ec207ca6237eb068` | 33-motion-style-library |

### iart-ai/motion-design-skills@3c129f769d90

| slug | 원본 경로 | raw bytes SHA-256 | 대상 |
|---|---|---|---|
| `beat-sync-editing` | `skills/beat-sync-editing/SKILL.md` | `92118cd6a5821974aa084a9838f263b46ee65fa1f48aaded8e676861f8c2de28` | 09-edit |
| `color-motion` | `skills/color-motion/SKILL.md` | `8c7fcf06c25eee669756f4d7e9213875aa0b59a9e4f7c23611c0a1c086ab796c` | 08-animation |
| `logo-animation` | `skills/logo-animation/SKILL.md` | `e78cc04f320234398c9551be47a569891b43f83c087b2494f37a2e156bce8c3b` | 08-animation |
| `motion-art-direction` | `skills/motion-art-direction/SKILL.md` | `0337edf7c93b8e130bd7658e3d43f546c46f333cacbb2bb970613d65d340c5de` | 08-animation |
| `shot-composition` | `skills/shot-composition/SKILL.md` | `c2bbedc1d615ba9969755054bae4fb9d6733df17226b8010b02e064e7838f0c1` | 06-shots |

### LottieFiles/motion-design-skill@d77a9fc8cb37

| slug | 원본 경로 | raw bytes SHA-256 | 대상 |
|---|---|---|---|
| `motion-design` | `skills/motion-design/SKILL.md` | `c639050706d07e62501db06c90c644d24d4815d5c05908b64771e1bf775778d7` | 08-animation |

### MengTo/Skills@ef5f85130d08

| slug | 원본 경로 | raw bytes SHA-256 | 대상 |
|---|---|---|---|
| `video-to-superprompt` | `agent-skills/codex/video-to-superprompt/SKILL.md` | `2b0db0096fb715f9e5c6be419f2be5caf0df5e1991ac019308185e2d72c2f950` | 11-ai-handoff |

### nexu-io/open-design@5a0c47777975

| slug | 원본 경로 | raw bytes SHA-256 | 대상 |
|---|---|---|---|
| `opendesign-motion-design` | `skills/motion-design/SKILL.md` | `5fdc15676abc9206ab9ca28655da2282fb6be3b99e60e5cac0c60a8c288aec45` | 08-animation |

### nexu-io/openmotion@2b57cf6908af

| slug | 원본 경로 | raw bytes SHA-256 | 대상 |
|---|---|---|---|
| `openmotion-bilingual-captions` | `library/skills/openmotion-bilingual-captions/SKILL.md` | `eab2e76ee4c0556ff50d602a11aba43e6fcf98c418db0f35c2cbf8c05d9781d7` | 23-finishing-platform |

### nexu-io/openmotion@709b10fd9ac5

| slug | 원본 경로 | raw bytes SHA-256 | 대상 |
|---|---|---|---|
| `openmotion-ad-script` | `library/skills/openmotion-ad-script/SKILL.md` | `5795b8183804543bde091a8d924c68e5e2161b13397550b91d7372d596a1c2c2` | 30-marketing-story-craft |
| `openmotion-adaptive-layout` | `library/skills/openmotion-adaptive-layout/SKILL.md` | `ecf04992426e1cbc19acb3778215a1bf29e1faeab349081ba6a3e46c099a8116` | 23-finishing-platform |
| `openmotion-ai-assistant-tour` | `library/skills/openmotion-ai-assistant-tour/SKILL.md` | `c09057f956fdc683c264c046c4a0ef684c325ad57319d25a88028211146e9024` | 19-brand-product-integration |
| `openmotion-archive-collage` | `library/skills/openmotion-archive-collage/SKILL.md` | `49ce40ac632650e95d25c6bb2d1c122371303768c5056af486d64cabd188ada6` | 33-motion-style-library |
| `openmotion-article-illustrations` | `library/skills/openmotion-article-illustrations/SKILL.md` | `ee29e39b21034c916f60b65feeb080cb492ae6b97fcb133a7c8d2a4d85f227ef` | storytelling-with-still-images |
| `openmotion-aurora-gradient` | `library/skills/openmotion-aurora-gradient/SKILL.md` | `bbe161bf6d5fb12dedb288426e849943ccb8fda5eaf2a0ce8a632559c4bcb7f9` | 33-motion-style-library |
| `openmotion-before-after` | `library/skills/openmotion-before-after/SKILL.md` | `5effdd41a28cb3de9a0b6d1d5bfceb605b3ac2bcd31318ac8bc252a6a74aa259` | 33-motion-style-library |
| `openmotion-bold-type-poster` | `library/skills/openmotion-bold-type-poster/SKILL.md` | `a74f2b8db0277dd550a5549343b94edb2a83a7a68b646cf8e7558ebfa1a64269` | 33-motion-style-library |
| `openmotion-brandkit` | `library/skills/openmotion-brandkit/SKILL.md` | `d0efb343d3b12b27ff15e85197a7f06239b2844c118c199e8cff2e2b1b3d5489` | 13-ideation-brand |
| `openmotion-bubble-field` | `library/skills/openmotion-bubble-field/SKILL.md` | `f9e601fbb23168e9ba3289edc8aa117e6b1a322d59822fb27ab862ccad3da30f` | 33-motion-style-library |
| `openmotion-caption-styling` | `library/skills/openmotion-caption-styling/SKILL.md` | `85143dfd3b992667618cb2b261731c1165c0a776b932353ddcaf2cbdd97191aa` | 23-finishing-platform |
| `openmotion-card-carousel` | `library/skills/openmotion-card-carousel/SKILL.md` | `7c746b865fc6a35ef11a80e702153f1880f8c19e45c527e9abd326312344ea4e` | 33-motion-style-library |
| `openmotion-cards-and-text` | `library/skills/openmotion-cards-and-text/SKILL.md` | `223c46d849cf17c0c93af3cbb5120fe86b293998bab6605b67d65124f1380ab9` | 33-motion-style-library |
| `openmotion-chalk-blueprint` | `library/skills/openmotion-chalk-blueprint/SKILL.md` | `3e53eb13a6f3f933fdb20ce18b02e9cd7ac454509207c885b987ea827a8a247f` | 33-motion-style-library |
| `openmotion-cinematic-logo` | `library/skills/openmotion-cinematic-logo/SKILL.md` | `7845c213bbfbb32e5503756ba4be81c06e9d9377dd5be9195a1d63b2c2b31537` | 33-motion-style-library |
| `openmotion-clay-explainer` | `library/skills/openmotion-clay-explainer/SKILL.md` | `19043a6ec673144d348c8f1f555bba741263a716914c9768ee3327107b1c4f16` | 33-motion-style-library |
| `openmotion-color-pop-poster` | `library/skills/openmotion-color-pop-poster/SKILL.md` | `22f5bf4dc42d31c74f6f4018e6ca1feca5e9793b923ee624d64f2b567eb0af75` | 33-motion-style-library |
| `openmotion-content-cover` | `library/skills/openmotion-content-cover/SKILL.md` | `cd5e5d343959d40b226b28d2a03cf6fdf713678f6354a9da46d5b4698838bb8a` | 23-finishing-platform |
| `openmotion-coral-title-cards` | `library/skills/openmotion-coral-title-cards/SKILL.md` | `550a6b11b455ce0a662f04515a3f055bfcd61d25685d399455a00b1eed685ac5` | 33-motion-style-library |
| `openmotion-corner-frames` | `library/skills/openmotion-corner-frames/SKILL.md` | `b2491dfcde1efd84810b347b2826b0d7adec2b822f8bf98cdf1846397db6d847` | 33-motion-style-library |
| `openmotion-dark-premium-poster` | `library/skills/openmotion-dark-premium-poster/SKILL.md` | `e64d42426fd31decf2bbc7cbe3b08b67883f986fa80e14c1103a5b8718c5e6bd` | 33-motion-style-library |
| `openmotion-design-styles` | `library/skills/openmotion-design-styles/SKILL.md` | `4a1c9e79c972556f559c13d642fe1fc31b37de149731c5af34867776f32d36cc` | 33-motion-style-library |
| `openmotion-doc-promo` | `library/skills/openmotion-doc-promo/SKILL.md` | `80e84d3b3d6ff884765b2e58f2155c9e75560896d2622c807effc73dd0b5a7b2` | 19-brand-product-integration |
| `openmotion-echo-stack-type` | `library/skills/openmotion-echo-stack-type/SKILL.md` | `6aca0ead4e15f6a733098a6598542c13405833a70e3dacf0bafac420baad23d8` | 33-motion-style-library |
| `openmotion-edit-to-script` | `library/skills/openmotion-edit-to-script/SKILL.md` | `82273dde6f4c48ea193b680ab17c151bafdb39933afd8b9afd85b04972adf7a4` | 09-edit |
| `openmotion-editorial-explainer` | `library/skills/openmotion-editorial-explainer/SKILL.md` | `c6d8b018ad12d7d3e35ac89831ecc31f694c6b697588bb3fdbaf4dec4be5d1aa` | 33-motion-style-library |
| `openmotion-editorial-poster` | `library/skills/openmotion-editorial-poster/SKILL.md` | `10b7e39b9542c8c92f815894750df6fa533819d75f327fcc943ccebbb3ed4262` | 33-motion-style-library |
| `openmotion-editorial-webinar` | `library/skills/openmotion-editorial-webinar/SKILL.md` | `a5151e97b1a5ee0fade8657a3c273113ef4513d286b36dcbf6592b7a20324a0f` | 03-screenplay |
| `openmotion-electric-impact-type` | `library/skills/openmotion-electric-impact-type/SKILL.md` | `c452f0728f6f6324c92fd5ef248a32481f2dc6311291ee9816f067d098a8a860` | 33-motion-style-library |
| `openmotion-felt-stop-motion` | `library/skills/openmotion-felt-stop-motion/SKILL.md` | `510b61a7d31469d6f91a046962858af25a56a0de4a5528f64a9de07b50fdbcbf` | 33-motion-style-library |
| `openmotion-flat-beat` | `library/skills/openmotion-flat-beat/SKILL.md` | `9fd3f4cb12587f7029a44d9b16a23e5a0b0a5b38a829af6991129b6d1ec288d2` | 33-motion-style-library |
| `openmotion-flat-card-explainer` | `library/skills/openmotion-flat-card-explainer/SKILL.md` | `d677c6b14f0ada71375625e5946f82bccc885f6662b5fa5670e8d3e80f6b91ae` | 33-motion-style-library |
| `openmotion-flat-lay-product` | `library/skills/openmotion-flat-lay-product/SKILL.md` | `ad48dc0c9fe709534ed4ad0ab5ef97311c1b1a4856ef0f36ea2c48eb5cdd1831` | 19-brand-product-integration |
| `openmotion-folder-pop` | `library/skills/openmotion-folder-pop/SKILL.md` | `9fe47ec105f0169fc2c4c506bd0eb0fdf1246e024cc7afaab4eca8ca6eb2b043` | 33-motion-style-library |
| `openmotion-footage-to-handpainted` | `library/skills/openmotion-footage-to-handpainted/SKILL.md` | `c0235a3095a69a121b4ee0953ec137954ae6427153b0975cf4bfad724dfbbcc0` | 33-motion-style-library |
| `openmotion-giant-flip-type` | `library/skills/openmotion-giant-flip-type/SKILL.md` | `992cdfd0cb1e7105f16cf3af8375e0bfcfa3132d181978229db0704a82e7a7dc` | 33-motion-style-library |
| `openmotion-glitch-logo-sting` | `library/skills/openmotion-glitch-logo-sting/SKILL.md` | `fec8669a5acb517e3f976bef1078c8a56de1b3b331f505d5c61bd4d1cb780b8d` | 33-motion-style-library |
| `openmotion-growth-teardown` | `library/skills/openmotion-growth-teardown/SKILL.md` | `fb0c272c6de93693972a6575ac9aa3b1e3161c282a5c92425c65e840e861cc7e` | 30-marketing-story-craft |
| `openmotion-hand-drawn-explainer` | `library/skills/openmotion-hand-drawn-explainer/SKILL.md` | `e58b0dc15181d5a62c898555f54832a03ecf1315fbe399b2999fb0a2e450f33b` | 33-motion-style-library |
| `openmotion-hidden-feature-demo` | `library/skills/openmotion-hidden-feature-demo/SKILL.md` | `99a57041e3b0b36bedf860dbd091b8aeb679e5dbd93589791ad54d959b350bba` | 19-brand-product-integration |
| `openmotion-highlighter-notes` | `library/skills/openmotion-highlighter-notes/SKILL.md` | `b20b0ca52422f2193b58d1df88ea656512de80c104539a2a81e3a1b0f1ff0938` | 33-motion-style-library |
| `openmotion-in-hand-product` | `library/skills/openmotion-in-hand-product/SKILL.md` | `d3a9f282f62c5084361f1d4e0ac1813c2d1ed172c527e5f2a58931e58316c9bd` | 19-brand-product-integration |
| `openmotion-ink-ribbon` | `library/skills/openmotion-ink-ribbon/SKILL.md` | `a8d017f2a5f6a048f0b175efb753b4c8e2cab0e62017b9449277873e8adee504` | 33-motion-style-library |
| `openmotion-isometric-card-flight` | `library/skills/openmotion-isometric-card-flight/SKILL.md` | `d9f34063973aa8fa9489d54f606e42a75615b0c4bf1384f104e4a2515f3f402e` | 33-motion-style-library |
| `openmotion-juicy-splash-poster` | `library/skills/openmotion-juicy-splash-poster/SKILL.md` | `6f6f2fd62e7b16d71ed7e1f50f0b6b02e1183f300f511c27cf7fe731cbddf176` | 33-motion-style-library |
| `openmotion-light-shadow-product` | `library/skills/openmotion-light-shadow-product/SKILL.md` | `349a807cebe9705413e894ffa064b5b45d3207f4607711be87cbfbacd15f43d7` | 19-brand-product-integration |
| `openmotion-liquid-blob` | `library/skills/openmotion-liquid-blob/SKILL.md` | `be57f9d6837f7554f7b28b6c107be2802d7932ab0fcf76ddaf6f7f6fc4062e12` | 33-motion-style-library |
| `openmotion-liquid-glass-logo` | `library/skills/openmotion-liquid-glass-logo/SKILL.md` | `c0c8032198634f6f56d1adcecf8efc0bfc9e1458c1d6f2c186a84f7f16b63bd9` | 33-motion-style-library |
| `openmotion-liquid-logo` | `library/skills/openmotion-liquid-logo/SKILL.md` | `a953bb3473790bcc722829fca80a41e9e6eea61ebdc48ba83693321a7c593896` | 33-motion-style-library |
| `openmotion-livestream-clips` | `library/skills/openmotion-livestream-clips/SKILL.md` | `99dd4dd67dd4f6b31e6953d9f2af40d8667d520c24b4da5dc131d7dcd38b17bf` | 09-edit |
| `openmotion-magnet-particles` | `library/skills/openmotion-magnet-particles/SKILL.md` | `f9ba03edc622fb3c6fa310b5bb49144b02b78b737f6bb28647989ebfbbf122f3` | 33-motion-style-library |
| `openmotion-manifesto-pop` | `library/skills/openmotion-manifesto-pop/SKILL.md` | `0c03f099da734ec2bd29c97591797a3cd93a64b472baf35acb6ef8defe30099a` | 33-motion-style-library |
| `openmotion-monochrome-magazine` | `library/skills/openmotion-monochrome-magazine/SKILL.md` | `ba843e3e4a7d424233887e6c568443d28ebcd78d18caf66563eb0fd425cae808` | 33-motion-style-library |
| `openmotion-motion-graphic-placement` | `library/skills/openmotion-motion-graphic-placement/SKILL.md` | `40f02aab14774604e68535a3f311ee8442033d21bac88aca13013af1c3e6122e` | 23-finishing-platform |
| `openmotion-multi-clips-to-reels` | `library/skills/openmotion-multi-clips-to-reels/SKILL.md` | `f9bc88b32baafa5cbf775b4f4565fc477fae965231d0c4d65cb917273d2870b4` | 09-edit |
| `openmotion-multicam-edit` | `library/skills/openmotion-multicam-edit/SKILL.md` | `c1444cf55d117ef73c39523f3786a9041100179b9b59f722f9eead93c0b0dcc5` | 09-edit |
| `openmotion-mystery-box-reveal` | `library/skills/openmotion-mystery-box-reveal/SKILL.md` | `ffcb9c6ee92e749ac5782fcc3ed42e4cdfc0290faed228306a3c56c2e4ba5690` | 33-motion-style-library |
| `openmotion-neon-outline-type` | `library/skills/openmotion-neon-outline-type/SKILL.md` | `96412dbd27db44e6fffa69e0124a1ce00d0ab552c533e0f98c72d60e50851456` | 33-motion-style-library |
| `openmotion-nova-intro` | `library/skills/openmotion-nova-intro/SKILL.md` | `df483a8d01d19c8351d875e791d7726b9927540a4156ffacf617acea5f4914d2` | 33-motion-style-library |
| `openmotion-one-bit-dither` | `library/skills/openmotion-one-bit-dither/SKILL.md` | `712073c74f174aa81e6fc4ba311045a297027587592746368e3d7e1116591aa2` | 33-motion-style-library |
| `openmotion-orange-unfiltered` | `library/skills/openmotion-orange-unfiltered/SKILL.md` | `23724517883e443a8447f10a6be3975b134ad09577461ee354f9e040f4e140e0` | 33-motion-style-library |
| `openmotion-paper-collage-explainer` | `library/skills/openmotion-paper-collage-explainer/SKILL.md` | `e8e3c332a883426514d0823deb740fe819785e9811e655d0f7ab6ca5608c4ef2` | 33-motion-style-library |
| `openmotion-paper-diorama` | `library/skills/openmotion-paper-diorama/SKILL.md` | `e73926235b055e70a05562632c58b2882f719a262f131e792e55bd4205951e72` | 33-motion-style-library |
| `openmotion-paper-map-journey` | `library/skills/openmotion-paper-map-journey/SKILL.md` | `88fb2498bcbe38237cfa2b3d65d3772fdd0344b77c38aeb6a09f667662f02c25` | 33-motion-style-library |
| `openmotion-paper-stop-motion` | `library/skills/openmotion-paper-stop-motion/SKILL.md` | `76ee9f8f332d77aa200527c36ae652eed86dff82a5c7dca136e240b3c3f12802` | 33-motion-style-library |
| `openmotion-pastel-flat-2d` | `library/skills/openmotion-pastel-flat-2d/SKILL.md` | `a48f1e30e781757771e113472582f151dc313a6804acc65fde7f726c1f413090` | 33-motion-style-library |
| `openmotion-pixel-art-explainer` | `library/skills/openmotion-pixel-art-explainer/SKILL.md` | `7fa4be9a8b794795c1f8b01c863dc69b1262ac03293261ad26a8b07cbbb19d3d` | 33-motion-style-library |
| `openmotion-pop-style` | `library/skills/openmotion-pop-style/SKILL.md` | `75ff3d50ba221cf85559b587f2782060937e89deabcad6378c811d68b848511a` | 33-motion-style-library |
| `openmotion-premium-halo` | `library/skills/openmotion-premium-halo/SKILL.md` | `a76afd836e91a7f84551578c4472540f19bf3ee6172a161727817880f88d00c6` | 33-motion-style-library |
| `openmotion-presenter-story` | `library/skills/openmotion-presenter-story/SKILL.md` | `de693606caa6ac0041d471ddd0f2bfef94c0629fc8dc9ebe0eb903b01037e9b5` | 03-screenplay |
| `openmotion-push-in-type` | `library/skills/openmotion-push-in-type/SKILL.md` | `5066db367993ac069229623454881d8f4953680a63dc3cfb37c0eec517291e95` | 33-motion-style-library |
| `openmotion-quantum-particles` | `library/skills/openmotion-quantum-particles/SKILL.md` | `8cd8e8991d6f9363aece6780d26cab7a9ddc8aa9dfa1351e3d24bb173d691815` | 33-motion-style-library |
| `openmotion-recreate` | `skills/openmotion-recreate/SKILL.md` | `277b0aaea8046c5363b68590fad6ac2d743cb50cb31ba2212824625137a265d6` | 29-reference-driven-production |
| `openmotion-red-pen-archive` | `library/skills/openmotion-red-pen-archive/SKILL.md` | `3be2ea557416e43b064aa83f83c45db83e037aa7a09d79add4ffce78b3ad8dce` | 33-motion-style-library |
| `openmotion-relight-reveal` | `library/skills/openmotion-relight-reveal/SKILL.md` | `763cedcc9c4965e0a7b0762a9249ed33a5980074bc84d576d149e7a715b7d0ee` | 33-motion-style-library |
| `openmotion-retro-flat-scene` | `library/skills/openmotion-retro-flat-scene/SKILL.md` | `e6ebf8c53e68ee9c6f29c5c323a22e93b279817b4cedfb6d182f0c828115caa2` | 33-motion-style-library |
| `openmotion-retro-print-poster` | `library/skills/openmotion-retro-print-poster/SKILL.md` | `4d09c88f9a653c3777a16ed79dd9e9c6dd30896cb56953acda9a1a890fd9bda9` | 33-motion-style-library |
| `openmotion-ring-mask-reveal` | `library/skills/openmotion-ring-mask-reveal/SKILL.md` | `06c52d4c276dcf9157fe85b7a8161024adf774631cf0f8322a40412dd00b032c` | 33-motion-style-library |
| `openmotion-runway-rebel` | `library/skills/openmotion-runway-rebel/SKILL.md` | `9f5adb3e19acca4f1675e1f4183e41ac8a8a9b56b5cddf5fad2c675706509f82` | 33-motion-style-library |
| `openmotion-sale-carousel` | `library/skills/openmotion-sale-carousel/SKILL.md` | `971cbbb76d01afc8147c11d5a4bc77bf2448d8d8a58951c253380724071b0bee` | 19-brand-product-integration |
| `openmotion-sale-countdown` | `library/skills/openmotion-sale-countdown/SKILL.md` | `870a32c1519e0f14621a7a7c4b66cffc4ec70885b895a7f09d08ce5192d526de` | 19-brand-product-integration |
| `openmotion-sale-promo` | `library/skills/openmotion-sale-promo/SKILL.md` | `29d5a6f0553edb07fcd56fecec1009b25ba2e9beea7f81e04b5aea2acd73a400` | 19-brand-product-integration |
| `openmotion-shortlist-shorts` | `library/skills/openmotion-shortlist-shorts/SKILL.md` | `0ffab6e809689402d67329c714e1f39e29618a7e9ba9795dab10688c4353fe3a` | 09-edit |
| `openmotion-shot-breakdown` | `library/skills/openmotion-shot-breakdown/SKILL.md` | `fd9aef1c99bfe619cf2c33f018a3ea174b67a1e5b9f052610000a8fa7c9f27a5` | 25-reference-video-analysis |
| `openmotion-shutter-bands` | `library/skills/openmotion-shutter-bands/SKILL.md` | `15748232e80374d7211852f039cf89b04e45ab1e486f4e0a5082e0f123ba183e` | 33-motion-style-library |
| `openmotion-smooth-wipes` | `library/skills/openmotion-smooth-wipes/SKILL.md` | `250f047480a4e6bbe5c4b47d407f1c4965e9efe48a0a5f4f6872bbb97651f426` | 33-motion-style-library |
| `openmotion-spec-sheet` | `library/skills/openmotion-spec-sheet/SKILL.md` | `a545dd17b4fa1a20f1aa23aee13f2a896c1ef46da61a86e08c0d2c96efa30120` | 19-brand-product-integration |
| `openmotion-splash-float-product` | `library/skills/openmotion-splash-float-product/SKILL.md` | `7b5afd7410fcaa43668370ec4c12ac4cd35442ecf3bf93a5c683ae7ab2ecb614` | 19-brand-product-integration |
| `openmotion-split-slot-type` | `library/skills/openmotion-split-slot-type/SKILL.md` | `0b3b31ca2129e61899064be3886e40d871e39f62c7c989fc248ca43a9330bdf8` | 33-motion-style-library |
| `openmotion-step-by-step-tutorial` | `library/skills/openmotion-step-by-step-tutorial/SKILL.md` | `6bf5d7c729a378fa04bfe0dc48ba522d743ec6ef0a307bd684e54daf29a869fa` | 10-evidence |
| `openmotion-sticker-bounce` | `library/skills/openmotion-sticker-bounce/SKILL.md` | `88a517a11cda7a9429a8b84e6f3247cbadf8974b4471b05a50fd0e1c81976ae9` | 33-motion-style-library |
| `openmotion-sticker-peel` | `library/skills/openmotion-sticker-peel/SKILL.md` | `39c79fcc691f663a320931b5d940f641026c90f234149e367774080ca4e86545` | 33-motion-style-library |
| `openmotion-storyboard-to-motion` | `library/skills/openmotion-storyboard-to-motion/SKILL.md` | `4d8264a747e47227e73f76cf5f5d58cfc9b2ac27a0fb978e1a6862556d072f20` | 08-animation |
| `openmotion-storybook-myth` | `library/skills/openmotion-storybook-myth/SKILL.md` | `2be2c0234601f4b9c9ec292ad4ab98aecc316818364d2c56fc895311d24d5ce3` | 33-motion-style-library |
| `openmotion-surreal-3d-poster` | `library/skills/openmotion-surreal-3d-poster/SKILL.md` | `5d43f08173897c6b80a2b76a4d04b3f9b39847187ecdfb6411191820293358c6` | 33-motion-style-library |
| `openmotion-talking-head-recreation` | `library/skills/openmotion-talking-head-recreation/SKILL.md` | `6a6a0508045cff83b1e0894e742ca2c0ed03a3e53053a1b33628fb45b24cdb40` | 29-reference-driven-production |
| `openmotion-time-freeze` | `library/skills/openmotion-time-freeze/SKILL.md` | `b4762665d593e9804bbcf67fea6e5f42e53f09f716a6226af2f5860f35cab2fc` | 33-motion-style-library |
| `openmotion-translucent-glass` | `library/skills/openmotion-translucent-glass/SKILL.md` | `dc5ff3263adc7b02a906c030147a939c9bb79bd1589203df9a6c2aeb796aa11c` | 33-motion-style-library |
| `openmotion-velocity-lines` | `library/skills/openmotion-velocity-lines/SKILL.md` | `ef99e3f5a2642164c41a519c81d6af3b3e39e4f000baa23ec7992212311f892b` | 33-motion-style-library |
| `openmotion-video-to-template` | `skills/openmotion-video-to-template/SKILL.md` | `58e538d1ef55b475ea0ac76826d550ab22a067043f8b63aa86bfd0ea44cc20cd` | 29-reference-driven-production |
| `openmotion-website-launch` | `library/skills/openmotion-website-launch/SKILL.md` | `2d53a1bf7e16320a000cb77d98950eb9286bb18fb7245d2a840955d7fb08feb6` | 19-brand-product-integration |
| `openmotion-whiteboard-doodle` | `library/skills/openmotion-whiteboard-doodle/SKILL.md` | `1880a31078b11635d21f7b15945682305e9c75a938ad7c4222d5809f26aa1330` | 33-motion-style-library |
| `openmotion-whiteboard-marker` | `library/skills/openmotion-whiteboard-marker/SKILL.md` | `bcf8423b2ec4c743276d6a9a15449f4af101d4a285fe7dd343b3cd2d52490503` | 33-motion-style-library |
| `openmotion-wireframe-style` | `library/skills/openmotion-wireframe-style/SKILL.md` | `eed5922d5998e857e0e297b0257d49d5a3d4a1ab69c7e8e4a0f7483f79f9f695` | 33-motion-style-library |

### Vincentwei1021/video-shotcraft@5ddbf521038b

| slug | 원본 경로 | raw bytes SHA-256 | 대상 |
|---|---|---|---|
| `video-shotcraft` | `SKILL.md` | `12696ad78212f9036cbb76bd46be305094686db64d9cf72f69a6e650eba3ebbc` | 19-brand-product-integration |

## 의도적인 차이

1. 엔진 의존 제거: 원본이 특정 렌더·미디어 도구 호출을 전제하더라도 `openmotion_*` 도구 호출, `npx hyperframes`, `hyperframes render` 같은 엔진 호출은 옮기지 않는다. 각색 절은 구성·시작값·움직임·피할 것·검수만 남긴다.
2. 실행 게이트 치환: 실행 수단은 패키지의 기존 레인(Remotion, ffmpeg, Blender, 선택된 생성기)과 `policy.md`의 실행 게이트, [24-production-execution](../24-production-execution.md)을 가리킨다. 원본의 설치·자동 다운로드·외부 호출 지시는 승인 없이 실행하지 않는다.
3. 예시 미디어·템플릿·코드 미포함: 원본 예시 영상·이미지·오디오·템플릿 코드·바이너리는 들여오지 않는다. 수치는 보증이 아니라 "시작값"으로 표기한다.
4. 사실 보호: 가격·숫자·후기·보증을 새로 지어내지 않으며 [10-evidence](../10-evidence.md)와 충돌하는 각색은 두지 않는다.
5. 각색 절은 정확히 `출처: <repo>@<commit 앞 12자> <slug>` 한 줄로 끝나며, 이 줄이 이 문서의 고정 커밋·SHA-256 표와 대응한다.

## 갱신

명시적인 유지보수 작업에서만 `scripts/open_design_ledger.py refresh`로 새 commit·해시·LICENSE를 확인하고 이 문서를 갱신한다. 실행 중 자동 다운로드·자가 갱신·전역 설치는 없다. 구조 검사(`scripts/test_open_design_absorption.py`)는 출처 줄·고지 사본·엔진 문자열·링크만 확인하며 원본 대비 의미 일치나 법적 검토를 보증하지 않는다.
