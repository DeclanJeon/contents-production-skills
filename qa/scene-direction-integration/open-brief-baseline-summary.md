# E2 baseline — 아이디어에서 제작 요청문까지

## 범위와 결과

고정 SD09–SD14 6건을 수정 전 같은 215개 소스에서 실행했다. Native delegate / `openai-codex/gpt-6.1-sol`, high, fresh, 600000ms. 실패 시 자동 재시도 0. 실제 사례 수 누계는 **14/26**, 남은 12건은 형성 최대 4 + 최종 8이다.

| Case | 작성자 의미 판정 | 관찰 |
|---|---|---|
| SD09 | FAIL | 5 PASS / 1 FAIL — 새로 정한 인물의 고정 음성 앵커가 실제 AUDIO에서 누락 |
| SD10 | PASS | 6 PASS — 무언 선택/능력 조건·대가/잔류와 요청문 연결 |
| SD11 | PASS | 6 PASS — 고정 원테이크/화면 밖 화자·관계 재해석, 음성·연기 인계 |
| SD12 | PASS | 6 PASS — 소리 인지→반응→얼굴 공개와 구간별 실제 요청문 |
| SD13 | PASS | 6 PASS — 공급 PERF_PACKET v1의 6개 연기가 3작업 AUDIO에 보존 |
| SD14 | FAIL | 4 PASS / 1 FAIL / 1 INCONCLUSIVE — 고정 음성·일부 숨 인계 누락; 기억 소진 뒤 관계 인식은 불명확 |

합계 **4 PASS / 2 FAIL**, 관찰 **33 PASS / 2 FAIL / 1 INCONCLUSIVE**. E1의 7 PASS / 1 INCONCLUSIVE(35 PASS / 1 INCONCLUSIVE 관찰)는 그대로다. 전체는 11 PASS / 2 FAIL / 1 INCONCLUSIVE 사례, 68 PASS / 2 FAIL / 2 INCONCLUSIVE 관찰이다.

## 확정 RED와 최소 수정 지점

- **SD09-O5:** `baseline-outputs/SD09.md:28–33`의 민서 음성은 “중역, 약간 마른 숨결”과 분명한 단어 경계를 고정한다. `:225–353`의 전체 복사용 요청문, 특히 `:319–336`의 AUDIO에는 대사별 강세/쉼/빠르기는 있지만 그 고정 음역·숨결이 없다. 실제 보이스/오디오 입력도 없어 빈 앵커를 보완하지 못한다.
- **SD14-O5:** `baseline-outputs/SD14.md:30–35,79–87`에서 은/류의 음역·마른 음색·명료 자음/짧은 말끝, 부드러운 중저음/둥근 모음과 발화별 숨을 설계한다. `:209–247`의 요청문 AUDIO에는 이것이 부분적으로 빠졌다. “앞의 은과 같은 음색”은 앞 발화에 기준 음색이 없는 상태라 충분하지 않다.
- **대조:** SD11은 본문에 고정 음성+대사 연기를 보존했고 SD13은 독립 공급된 6개 Performance를 모두 보존했다. 능력 전체의 부재가 아니라 **새로 창작한 오너 내용→실제 제출문으로 기본 인계하는 경로**의 누락이다.

따라서 C1은 기존 11 handoff 참조·템플릿과 timing serializer의 세 문서만 수정한다. 발화가 있는 경우 실제 AUDIO 화자 헤더에 원문의 고정 앵커, 기존 발화 행에 이번 Performance를 투영하고 소비 위치를 역대조한다. 인물/보이스·연기의 정본은 기존 오너에 남는다. 원문 없는 값/실제 voice_id를 만들거나 무발화·no_audio에 보이스를 강제하지 않는다. 새 director/원장/JSON 필드·enum/validator/CLI/런타임은 없다.

SD14-O2의 “관계 기억을 모두 쓴 류가 현재 관계를 어떻게 인식하는가”는 불명확하다. 이를 모순이라고 확정하거나 설정을 대신 채워 PASS시키지 않는다. 이 의문만으로 세계관 오너를 수정하지도 않는다. 다른 기존 오너의 관찰된 PASS는 보호 대상으로 남기며, 모든 파일을 수정했다거나 모든 미평가 약점을 해결했다고 주장하지 않는다.

## 실행 근거와 한계

- E2 실제 **165개 read** 모두 고정 소스 범위 안; 위반 0. E1 포함 271개 read. 입력/출력·원시 실패를 고치지 않았고 baseline 소스 해시가 유지됐다.
- E2 runtime 보고 비용 USD **2.6644584**, E1 포함 **4.2361036**. 청구서 대조/고정 출력 한도/전체 작업 비용은 확인하지 않았다. 사례당 source-reading tool turn으로 모델 요청이 여러 번 발생할 수 있다.
- C1 기계적 호환성: `check_versions.py` 2.34/22, `diff --check`, pytest **737 passed / 4 skipped / 525 subtests**. 이는 문서 소비·인계 개선의 behavioral GREEN이 아니다.
- 작성자 직접 의미 검토이며 독립 판정이 아니다. 사례당 1회, baseline 먼저 실행, 최대 2건 병렬이다. 서로 다른 창작안을 허용하며 취향·샷/문자/키워드 수나 출처 문자열 파싱으로 우열을 판정하지 않는다.
- 정해진 26건 한도 안의 형성/최종 시나리오만 사용한다. 문구 변형별 5회 반복/분산 실험은 하지 않으므로 통계적 안정성·일반적 창작 품질 개선을 주장할 수 없다.
- 실제 이미지·오디오·영상/청취·물리 검증·사용자 수락·독립 최종 리뷰·커밋·설치/배포는 이 단계에서 미수행이다.

근거 루트: `.superpowers/sdd/2026-11-14-scene-direction-integration/epoch-e2/`의 `baseline-reviews/`, `baseline-outputs/`, `baseline-execution-audit.json`, `baseline-score-and-diagnosis.json`. 원시 근거는 gitignored이며 Git 백업이나 외부 업로드가 아니다.
