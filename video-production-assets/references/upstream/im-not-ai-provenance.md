# im-not-ai 발화 후편집 이전 기록

- 원본: https://github.com/epoko77-ai/im-not-ai
- 고정 커밋: `b37e0206d31fffd9149bf57168d4d62eb2086bee`
- 확인일: 2026-11-11. 공개 raw 파일 읽기이며 upstream 설치/에이전트 실행은 하지 않았다.
- MIT, Copyright (c) 2026 epoko77-ai. [원문 고지](im-not-ai-LICENSE.txt)를 포함한다. 저장소 전체에 라이선스를 부여하는 고지가 아니다.
- 적용 파일: [절차](../korean-script-postediting.md), [패턴](../korean-script-postediting-patterns.md), [검증기](../../scripts/korean_script_postediting.py), [범위 파서](../../scripts/korean_script_packet.py).

| 직접 확인한 원본 | raw bytes SHA-256 | 이전 내용 |
|---|---|---|
| `LICENSE` | `4cc7e8c439fe42f09d98457599c129ea6df9e5d0e622750d75952b441a38343f` | 전문 고지 |
| `docs/en/integration.md` | `0baa89669c07b0cc75bc6cc143d0aaf9344762d84cd30c82114d1178b3361f00` | 생성/후편집 구분, 빈도 조건, 원문 대조 |
| `skills/humanize-korean/references/quick-rules.md` | `7a8e66c7b9326c1df7413f7a5662d69e89907591e16ba740e5746bf01f544b85` | KP01–KP08 ID/처방, 서법/명칭/인용 보존 |
| `skills/humanize-korean/references/metrics_v2.py` | `6e3ddb40e2789ab37e95ef0bd5974a8fbeb2678919c17ee9afe16e8ae66ca341` | change_rate 구간, 문자 SequenceMatcher·0.30/0.50 참고 |

설계 조사에서 README.en.md, humanize-korean/SKILL.md, prepare_monolith_input.py 경로 판정, verify_change_rate.py와 verify_gates.py도 읽었다. 전체 taxonomy/전체 테스트·모든 의존 코드의 전수 검토/실행은 하지 않았다. 원본 전체·코퍼스·baseline은 배포하지 않는다.

## 의도적인 차이

1. 영문 integration은 bigram 변경률을 설명하지만 고정 코드의 `metrics_v2.change_rate()`는 문자 `difflib.SequenceMatcher(autojunk=False)`다. 후자를 참고하되 NFC 비교 사본·잠금 제외·단위별 집계는 로컬 구현이다. 원본과 동일 정량 시스템이라고 소개하지 않는다.
2. 원본 E-1 장문 삽입, C-11 쉼표 제거, E-7 격식 통일, D-14 비유 제거를 발화 전체에 강제하지 않는다. 인물·연기·장르의 의도적 표현이 우선이다.
3. light/standard/heavy는 논리 깊이만 재사용한다. Claude Agent·고정 opus·원본 workspace·콜 수·risk router·등급 A–D는 제외한다.
4. 범위 밖 bytes·수치 화자 간 이동·명시 잠금, 짧은 발화 대조, 최초 원문 누적 비교, 행동 도입 보류는 로컬 운영 설계다. 정규식은 의미·자연스러움·권한·인용 출처를 인증하지 않는다.
5. 외부 모듈 의존성·서버·학술 원문·개인 자료는 포함하지 않는다. 규칙/처방·변경률 접근의 실질 adaptation에 MIT 고지를 함께 제공한다.

## 갱신

명시적인 유지보수 작업에서만 새 commit·실제 읽은 파일 해시·KP 대응/예외/회귀를 갱신한다. 실행 중 자동 다운로드·자가 규칙 갱신·전역 설치는 없다. 구조 검사와 실제 모델/청취 증거는 분리한다.
