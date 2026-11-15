# E2 커버리지 — 생성 전 고정

사용자 승인: 기존 8종을 보존하고 남은 18건 안에서 아이디어 출발 평가를 보강한다.
기준판: 0e1d9f3 / package 2.34. profile은 기존 native delegate / gpt-6.1-sol high / fresh / 600000ms 그대로다.

| Case | 입력 성격 / 포착할 실패 | 기준판 | 후보 |
|---|---|---|---|
| SD09 | 규칙을 어기는 현실 드라마 한 줄 → 선택/비용 없는 소개문, 인물/대본과 무관한 컷 | FAIL: O5 음성 앵커 인계 누락 | C1 독립 FAIL: O1/O3 같은 위치 결함; O5 PASS |
| SD10 | 눈보라 속 도움의 선택 → 능력 조건/지지/비용·환경 반응/잔류 누락 | PASS | C1 PASS |
| SD11 | 한 얼굴/화면 밖 목소리 → 관계·반응 근거 없는 반전, 추가 얼굴 컷/음성 혼동 | PASS | C1 PASS |
| SD12 | 소리로 귀환 인지 → 장르 이름뿐인 음악, 청점/원인/공개·반응 불일치 | PASS | C1 PASS |
| SD13 | 독립된 6개 Performance 큐 → 실제 AUDIO에 음색만 남고 이번 연기가 소실 | PASS | C1 PASS |
| SD14 | 기억 통행료 → 세계 법칙·인물 선택/대가가 서술에만 있고 실제 샷/요청문에서 사라짐 | FAIL: O5 음성/숨 인계 누락; O2 INCONCLUSIVE | C1 PASS; 새 이야기이며 옛 O2 의문을 고쳤다는 뜻 아님 |

각 6개, 총 36개 관찰을 baseline 생성 전에 동결했다. 실제 baseline 수집/검토 후 작성자 판정은 33 PASS / 2 FAIL / 1 INCONCLUSIVE다. [근거와 한계](open-brief-baseline-summary.md)를 함께 본다. 실제 문서 수/샷 수/문자 수·키워드가 아니라 입력 잠금·응답 내부의 인과/정본 소비·시간/상태·전문 내용과 최종 요청문을 위치/인용으로 대조한다.

- 원래 E1의 7 PASS / 1 INCONCLUSIVE는 그대로다. 새 과제가 옛 성공을 실패로 바꾸지 않는다.
- E2 baseline 6건의 실제 실패를 검토한 뒤 기존 11 인계/템플릿·timing serializer 세 문서만 C1 후보로 수정했다. C1 형성 2건은 작성자 의미 검토에서 통과했다. 최종 작성자는 7 PASS / 1 INCONCLUSIVE였으나 독립 리뷰 후 채택 결과는 8건(기존 SD03/08 포함)에서 **7 PASS / 1 FAIL, 41 PASS / 2 FAIL 관찰**이다. SD09의 한 위치 결함이 O1/O3에 함께 영향을 준다. 확정 음성 인계 누락 2축은 FAIL→PASS이나 전체 B 완료를 뜻하지 않는다. [최종 검증 보고](../2026-11-14-scene-direction-integration-validation.md)를 본다. 사례를 자동 추가하지 않는다.
- 예산은 이미 쓴 8 + 이 기준판 6 + 형성 최대 4 + 최종 8 = 최대 26. 최종 8은 SD09–14와 기존 SD03/08 보호 대조군이다.
- 응답 내부 창작 정본의 버전/소비를 비교하며, 후보가 다른 허구 이름/소품/줄거리를 택한 것만으로 FAIL이나 개선을 주장하지 않는다.
- 최종 독립 리뷰 1회 완료. 전체 B 미구현/최종 상태 결함 때문에 HOLD다. 실제 미디어/청취·공간 검증·설치/배포는 미수행이다.

프로토콜: [open-brief-protocol.md](open-brief-protocol.md).
원시 근거/고정 입력/실행 영수증: 이 worktree의 `.superpowers/sdd/2026-11-14-scene-direction-integration/epoch-e2/`.
