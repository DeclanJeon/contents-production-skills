# 제작 가이드 범용 스킬 통합

사용자 제공 101페이지 이미지형 PDF를 OCR·페이지 이미지로 검토하고 기존 스킬에 통합했다. 드라마 전용 스킬은 추가하지 않았다.

- [23장 전체 대조·44개 공정/노하우·제외/충돌 해결](../../video-production-assets/references/guide-01-extraction.md)
- [페이지별 스캔 범위·지문·한계](../../video-production-assets/references/guide-01-scan.json)
- [실무 인계 R1–R8](../../video-production-assets/references/29-reference-driven-production.md)
- [후속 누락 점검·영역별 업그레이드·남은 한계](shortdrama-guide-review.md)
- [44항목 오너/템플릿/검수 연결표](../../video-production-assets/references/guide-01-coverage.json)
- [정적 회귀 검사](../../scripts/test_guide_integration.py)
- [행동 시나리오 입력 12개](../../qa/guide-integration-scenarios.json) · [후속 6개](../../qa/guide-followup-scenarios.json) · [실제 18개 응답/별도 판정](../../qa/guide-behavior-review.json)

주요 변경은 참조 속성/우선순위·시트 입력 뷰·다국어 대응 검수·새 생성/수정/실제 확장 구분·국소 발음 교정·채택 구간/비용·재개/납품 검수다. 기존 이미지 실행 경로, 전체 패키지 Sheet A, 실행/비용/복제 승인, project.json schema와 단일 기록자 계약은 유지했다. 기존의 무관한 변경·백업 파일은 건드리지 않았다.

원문 PDF·OCR·페이지 렌더는 배포하지 않는다. PDF에 소개된 원본 영상/음성/Blender 파일은 확보하지 않았다. 후속으로 좁은 시험안의 현재 공급자 카탈로그/견적만 조회했으며, 실제 미디어 품질이나 원문 모델 성능 주장을 검증한 것은 아니다. 전 페이지 OCR과 contact sheet 개관, 최초 28페이지+후속 5페이지(누적 33페이지) 개별 대조는 전문 전사/미디어 실행 검증이 아니다.

## 최초 통합 검증 기록

후속 누락 점검/보완의 최신 결과는 [후속 검토](shortdrama-guide-review.md)를 따른다. 아래 8개/243개는 최초 통합 시점의 실행 기록이다.

2026-10-20, Linux / Python 3.14에서 실행했다. pytest·Pillow·Pydantic은 시스템이 아니라 `/tmp/shortdrama-guide-audit/test-deps`에 준비했다.

- `python3 -m unittest discover -s scripts -p test_guide_integration.py -v`: **8 tests 통과**. 첫 실행의 문자열 기대값 1건 실패는 실제 지침 문구와 테스트 기대값의 불일치여서 테스트를 정정한 뒤 재실행했다.
- `PYTHONPATH=/tmp/shortdrama-guide-audit/test-deps python3 -m pytest -q scripts video-production-assets/scripts recording-production-history/scripts --basetemp=/tmp/shortdrama-guide-audit/pytest`: **최종 재실행 243 passed, 345 subtests passed** (`--basetemp=/tmp/shortdrama-guide-audit/pytest-final`; 첫 회귀 실행은 243 passed, 347 subtests passed). 새 정적 검사도 포함한다. 이 세 디렉터리의 회귀 결과이며 저장소 전체/실제 공급자/Blender/음성·영상 품질 검증이 아니다.
- `python3 scripts/check_versions.py`: **package 2.29 / 25 skills 일관성 통과**. 기존 버전은 유지하고 변경은 Unreleased에 기록했다.
- 이번에 수정한 추적 파일에 한정한 `git -c core.whitespace=cr-at-eol diff --check -- <paths>`: **통과**. 저장소 전체 diff에는 기존 `higgsfield-video-replicate/references/consistency.md`, `topic-demand-selection/SKILL.md` 공백 경고가 남아 있으며 무관한 변경은 수정하지 않았다.
- `/tmp/shortdrama-guide-audit/installed-skills`에 전체 설치 프리플라이트를 시도했으나 **기존 `video-production-assets/support/{manifest.json,examples,qa,CHANGELOG.md}` 충돌로 차단**, 설치 파일 쓰기는 없었다. 이 기존 배포 구조 문제는 이번 PDF 통합 범위에서 변경하지 않았다. 새 출처 대조표/scan JSON은 각 스킬 복사 설치에 포함되는 `video-production-assets/references/` 안에 두어 런타임 출처 조회가 저장소 docs 경로에 의존하지 않게 했다.
- 최초 단계에서 행동 시나리오 12개는 **실행 대기**였다. 이후 6개를 추가하고 총 18종 실제 응답을 실행·별도 검토했다. 최신 판정과 제한은 위 후속 검토를 따른다. 기대값 자체를 통과로 세지 않는다.

정적 통과와 에이전트 행동 개선·생성 성공·실제 청취/시청·품질 향상은 구분한다. 최초 통합 단계에서는 전역 설치·동기화·미디어 생성·원본 업로드·복제·미디어 과금·게시·git commit을 하지 않았다. 이후 별도 승인된 영상 1개·음성 1개의 실제 생성/15.1크레딧 차감과 제한된 QA는 [최신 미디어 시험](../../qa/guide-media-run-01/summary.json)에 기록했다. 전역 배포·원본 업로드·복제·게시는 여전히 하지 않았다.
