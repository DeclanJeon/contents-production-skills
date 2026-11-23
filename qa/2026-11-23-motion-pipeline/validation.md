# 모션그래픽 파이프라인·Prompt Motion 흡수 검증 기록 (2026-11-23)

설계: `docs/superpowers/specs/2026-11-23-prompt-motion-corpus-absorption-design.md` · 작업지시서: `docs/superpowers/plans/2026-11-23-motion-pipeline-work-order.md`

| 항목 | 판정 | 증거 |
|---|---|---|
| 원장 450행·고유 키·열거값·변형별 개수 | PASS | `scripts/test_prompt_motion_corpus.py` 8/8 |
| 흡수 기법 16개, 정본 한 곳·출처 줄·근거 표현 | PASS | 같은 테스트(`test_each_absorbed_technique_has_one_canonical_section`, `test_sections_cite_ledger_rows_and_match_evidence`) |
| 원문 복제 없음(8단어·한글 20자) | PASS | `prompt_motion_ledger.py verify` problems 0 |
| 저장소에 원문·GIF·설치 명령 없음 | PASS | `test_hygiene_no_archive_media_or_prompt_text` |
| 시각 확인 | PASS(일부) | 근거 행 5건 판정(pass 4, mismatch 1), 형식 대표 14건 pass. 무음 정지 프레임으로 확인할 수 없는 기법은 비워 둠 |
| M1~M6 문서·분석표 11칸·평가 기준 4개·매트릭스=CineForge RECIPES·해상도 | PASS | `scripts/test_motion_pipeline.py` 13/13 |
| 코드 렌더러(결정성·네트워크 차단·음원 길이·구간·다른 파일시스템) | PASS | `video-production-assets/scripts/test_render_html_motion.py` 7/7 |
| CineForge code-motion 레인·motion_brief 스키마·핸드오프 참조 | PASS | `tests/test_code_motion_lane.py` 10/10, `tests/test_pipeline_cli.py` |
| 실제 렌더 시연 3편(M1~M6) | PASS | `~/Documents/Media_Studio/motion-pipeline-demo/qa/{A,B,C}-review.md` |
| CineForge CLI 흐름(승인→봉투→영수증) | PASS(부분) | `motion-pipeline-demo/qa/cineforge-flow.md`. 픽스처 프로젝트, 재생 검수·납품 단계는 미확인 |
| 행동 프로브 pm1~pm4 × 3 | **FAIL(기준 미달)** | `probe-results.md`: 모션 판정 pm3 2/3. 전체 판정은 기존 F1 마감 줄 결함으로 더 낮음 |
| 회귀 | PASS | 스킬 저장소 1360 passed/5 skipped, check_versions OK, routing 79/0, CineForge 180 passed/2 skipped |

## 스킬팩 후속 QA

- 라우팅 전 컷 확인으로 바꾼 뒤 pm3는 모션 문서를 3/3회 열었고 pm4는 3/3회 열지 않았다. 전체 판정은 마감 줄 문제 때문에 각각 2/3이었다. 위 표는 초기 검증 결과다.
- 실제 CineForge CLI와 복제한 테스트 봉투로 제출 검사 확인: 4초 세로 컷에 30초 가로 MP4를 넣으면 거부되고 영수증이 생성되지 않았다. 1080×1920, 4초, 120프레임 MP4는 영수증에 `accepted`로 기록됐다. 별도 자동 테스트에서 같은 종횡비의 길이 불일치와 손상 파일도 거부했다.
- 스킬팩 pytest 1364 passed / 5 skipped, 라우팅 79/0. CineForge 코드 변경과 최종 납품은 이번 후속 범위에 포함하지 않았다. `code-motion` 레인을 지원하는 CineForge 설치가 필요하다.

알려진 한계
- 근거 대부분(개선본)은 결과 예제가 없는 Prompt Motion 템플릿 변형이다. 해당 기법은 "관찰된 프롬프트 패턴"으로 표시했다.
- 시연 영상은 모두 무음이다. 승인 음원 합성(`--audio`)은 테스트로만 확인했다.
- 데모 A의 제작 이력 이벤트는 작업 뒤에 기록했다(`.history`에 사후 기록이라고 명시).
- 데모 C의 local 컷은 `cineforge motion` CLI(G2 게이트 필요)가 아니라 같은 렌더 함수를 직접 호출했고, 조립은 FFmpeg concat이다.
- 패키지 버전(2.63)은 올리지 않았다. 기존 Unreleased 항목과 함께 릴리스할지 정해야 한다.
