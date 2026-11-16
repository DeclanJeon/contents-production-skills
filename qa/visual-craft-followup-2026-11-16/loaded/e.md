## 정보 위계
- 기본 룩: 비서사 교육용 정적 도표 한 장을 그대로 유지한다. 기존 담당·필드·도표 내용은 변경하지 않는다.
- 핵심 문구: “초안과 확정은 다릅니다.” / “확인되지 않은 값은 비워 둡니다.” 두 문장 모두 승인된 원문을 유지한다.
- 주요 대비 축: 초안/확정의 구분과 미확인 값의 공란 유지. 새 수치·라벨·관계를 추가하지 않는다.
- 제안(배치 미정일 때만): 두 승인 문구는 동등한 위계로 읽히게 하고, 검수 메모는 도표 밖 별도 문서에 둔다. 기존 위계가 있으면 우선한다. 색은 미정으로 남기며 의미를 새로 부여하지 않는다.

## 검수 메모
- 확인 기준: 두 문장의 철자·문장부호 보존, 기존 도표 항목·관계·빈칸 유지, 미확인 값을 0이나 추정치로 대체하지 않음.
- 인물·소품·발화·이야기·마법·시간 생략·음향·카메라 이동·추가 컷은 만들지 않는다.
- 미확인 사항: 도표 원본과 기존 담당 필드가 제공되지 않아 실제 정보 위계·배치·색·가독성은 미검증이다. 이번 산출물은 텍스트 메모이며 실제 미디어 검증이나 승인 완료를 뜻하지 않는다.
- 다음 단계 인계: 기존 담당자가 원본과 대조할 검수 기준으로만 사용한다. 프로젝트 파일은 수정하지 않았다.

### 실제 읽은 참조
- `video-production-assets/SKILL.md`
- `video-production-assets/references/workspace-integration.md`
- `video-production-assets/references/contract.md` (1–170행)
- `video-production-assets/references/05-visual.md`
- `video-production-assets/assets/05-visual-template.md`
- `video-production-assets/references/visual-scene-communication.md`

```acceptance-report
{
  "criteriaSatisfied": [
    {"id":"criterion-1","status":"satisfied","evidence":"Only requested text artifact written; approved wording and uncertainty preserved."},
    {"id":"criterion-2","status":"satisfied","evidence":"References, verification limits and staged-file check recorded."}
  ],
  "changedFiles":["qa/visual-craft-followup-2026-11-16/loaded/e.md"],
  "testsAddedOrUpdated":[],
  "commandsRun":[{"command":"git diff --cached --quiet","result":"passed","summary":"Exit 0; no staged changes."}],
  "validationOutput":["Text checked against supplied wording and exclusions; no media inspected."],
  "residualRisks":["Original diagram unavailable; reviewer acceptance pending."],
  "noStagedFiles":true,
  "diffSummary":"Single Korean hierarchy and inspection memo.",
  "reviewFindings":["No textual blockers identified; independent review required."]
}
```
