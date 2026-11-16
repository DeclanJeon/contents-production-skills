## 정보 위계
- **기본 룩:** 비서사 교육용 정적 도표 한 장을 유지한다.
- **핵심 안내:** 승인 문구는 그대로 보존한다.
  - 초안과 확정은 다릅니다.
  - 확인되지 않은 값은 비워 둡니다.
- **주요 대비 축:** 초안/확정의 구분과 미확인 값의 공란을 유지한다. 기존 라벨·값·연결 관계는 바꾸지 않는다.
- **제안:** 색·배치가 미정일 때만, 기존 정보 위계를 유지하면서 글자 대비와 여백으로 안내 문구와 도표 항목을 구별한다. 색만으로 상태를 구별하지 않는다. 두 문장 사이에 새로운 우선순위를 부여하지 않는다.

## 검수 메모
- 확인 기준: 승인 문구의 글자·문장부호 일치, 미확인 값의 공란 유지, 도표 내용·기존 오너 필드 보존.
- 인물·소품·발화·카메라 이동·컷·이야기·마법·시간 생략·음향은 추가하지 않는다.
- **미확인 사항:** 현재 도표 원본과 기존 오너 필드가 제공되지 않아 실제 정보 위계·색·배치·가독성은 미검증이다. 위 내용은 텍스트 기준과 제안이며 실제 미디어 검수 통과 판정이 아니다.

## 실제 읽은 참조
- `video-production-assets/SKILL.md`
- `video-production-assets/references/workspace-integration.md`
- `video-production-assets/references/contract.md` (1–100행)
- `video-production-assets/references/05-visual.md`
- `video-production-assets/assets/05-visual-template.md`
- `video-production-assets/references/visual-scene-communication.md`

구현: 정보 위계·검수 메모 작성. 변경: 지정 산출물만. 검증: 텍스트 대조, 스테이징 없음. 위험: 원본 미제공. 다음: 기존 담당자의 원본 대조.

```acceptance-report
{
  "criteriaSatisfied": [
    {"id":"criterion-1","status":"satisfied","evidence":"승인 문구와 정적 도표 범위 유지; 색·배치는 제안으로 구분"},
    {"id":"criterion-2","status":"satisfied","evidence":"실제 참조·검수 한계·변경 경로 명시"}
  ],
  "changedFiles": ["qa/visual-craft-followup-2026-11-16/baseline/e.md"],
  "testsAddedOrUpdated": [],
  "commandsRun": [{"command":"git diff --cached --name-only","result":"passed","summary":"출력 없음"}],
  "validationOutput": ["승인 문장 두 개 원문 유지; 미디어 실행 없음"],
  "residualRisks": ["현재 도표 원본 미제공; 독립 검토 대기"],
  "noStagedFiles": true,
  "diffSummary": "요청된 텍스트 산출물만 작성",
  "reviewFindings": ["독립 검토 미실행; 실제 가독성 미검증"]
}
```
