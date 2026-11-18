# YouTube craft 후보 5건 — 기존 커버리지 대조

## 범위·판정 기준

현재 **작업트리**의 지정 원문 6개와 연관 템플릿·eval·교육 예시를 읽었다. 기존 변경은 건드리지 않았다. 네트워크·설치·미디어 생성·재생·청취·위임은 수행하지 않았다. 로컬 튜토리얼 자막 일부는 텍스트 근거로만 확인했다. **12편 전체의 craft를 빠짐없이 검증한 보고서는 아니다.**

- **있음(Present):** 해당 원칙/절차가 명시됨.
- **부분(Partial):** 구성 요소는 있지만 후보가 요구하는 연결 레시피·검증 방법은 덜 구체적임.
- **부재(Absent):** 아래 확인 범위에서 특정 절차를 찾지 못함. 저장소 전체의 절대 부재를 뜻하지 않음.
- **미확인(Unknown):** 실제 실행·결과나 자료 근거가 없어 판단 불가.

## 커버리지 매트릭스

| 후보 | 판정 | 기존 근거: 정확한 경로·절·줄 | 실제 증분 |
|---|---|---|---|
| ① 다중 화자·음성 선행 스틸 애니매틱 실행 | **부분 — 기본 기능은 있음** | `storytelling-with-still-images/SKILL.md` §Workflow L21–26: 화자/트랙 잠금, 대사 보존, 실제 음성·쉼 측정, hold 재배분, 믹스·조립·검수. §Cue-table contract L28–34. `video-production-assets/references/22-dialogue-lipsync.md` §절차 L37–50: 음성 선행, 화자·보이스·반응 연결. `animatic-direction/SKILL.md` §인계 L20–28: 실제 스틸 편집의 기존 소유자 명시. | 새 기능보다 **분산된 절차를 연결하는 다중 화자 예제**가 유효. 음성 파일→확인된 화자→측정된 턴/쉼→스틸 hold→최종 조립 검수의 한 사례. 특정 실행기 명령까지 검증된 범용 레시피는 이 지정 원문에서 확인하지 못함. |
| ② 공급자 선택 전 과업별 비교 가능한 모델 시험 | **부분 — 적합성 평가·프리뷰는 있음; 비교시험 프로토콜은 확인 범위에서 부재** | `video-production-assets/references/24-production-execution.md` §3 절차 L124–129: hard 요구·현재 endpoint·가격·권리 검증. §5 L180–198: 최소 충분 프리뷰, 대상·상한·판정·최종 재검수. `video-production-assets/assets/video-model-routing-template.md` §승인·프리뷰 L22–27: 입력 버전·횟수·근거. `video-production-assets/references/29-reference-driven-production.md` R7 L138–139: 원인 가설·단일 변경·제한된 재시도. | **문서상 지원 확인 ≠ 과업 성공의 실험 근거.** 허용된 영상 후보에 한해 동일 과업·평가기준·비교 조건을 명시하는 선택적 trial 설명을 보완할 여지. 모든 공급자 시험을 의무화하거나 기본 이미지 실행자를 바꾸는 제안은 아님. |
| ③ 결정론적 숫자·문자 설명 그래픽 검증 | **부분 — 경로·사실 검수·산술 예시 있음** | `video-production-assets/references/24-production-execution.md` §3 L139–141: 정확 텍스트·UI·타이밍의 결정론적 그래픽 분리. `video-production-assets/references/21-generated-video-qa-retry.md` §2 L52, §5 L157·186: 정확 아트워크/합성, 반복 생성 중단. `video-production-assets/references/10-evidence.md` §실행 절차 L9–15·§완료 조건 L27–28: 분모·단위·축·claim 연결·수치 정합. `examples/15-second-education/plan-ko.md` §산술 근거 L25–26·§QA L28–31: 2+3=5의 직접 계산/집합 확인과 실제 영상 미검증 구분. | “결정론적 그래픽 없음”은 오판. **데이터→계산/표시 문자열→도형/라벨→렌더 결과**를 함께 대조하는 재사용 가능 검증 예시는 확인 범위에서 찾지 못함. 코드가 정확히 실행돼도 잘못된 수치·단위·축을 그릴 수 있음. |
| ④ native audio·stem·클립 간 연속 스코어 | **부분 — 핵심 계약은 있음; 생성 믹스의 후반 처리 레시피만 보완 가능** | `video-production-assets/references/09-edit.md` §실행 가능한 편집·사운드 큐 L124–134: 시퀀스 음악 큐, gain/fade/동기, 혼합 참조·없는 stem 금지, 전체 청취. §오디오 의도와 실행 경로 L140–151: 인-리퀘스트 기본 생성, 제외 의도, 미지원 시 별도 승인 경로. `video-production-assets/references/29-reference-driven-production.md` R5 L108–110: 확장 접합 음악/잔향 점프 검사. `video-production-assets/references/21-generated-video-qa-retry.md` §4 L125–134: 최종 믹스 재생·혼합 트랙 구분. | **클립마다 baked music이 달라지는 경우**를 기존 큐/믹스 메모로 해결하는 조건부 사례. 실제 제공 stem / 별도 승인 분리 결과 / 혼합 원본을 구별하고, 연속 스코어는 기존 시퀀스 큐로 표현. 자동 분리나 음악 제거 성공은 보장하지 않음. |
| ⑤ 프롬프트 재시도 전 참조 모순 진단 — 운전대 사례 | **있음 — 사례 보강 수준** | `video-production-assets/references/29-reference-driven-production.md` R1 L20–33: 가져올/제외 속성·우선 기준, 미해결 충돌은 실행 blocker. R2 L46: 인물/화면 좌우 및 반전 구별. R7 L138: 얼굴·의상은 참조, 공간 모순은 공간 명세로 환류. `video-production-assets/references/21-generated-video-qa-retry.md` §5 L167–178: SSOT·실제 출력·나쁜 초기 프레임 등 진단, 최소 개입, 참조 교정. | 새로운 재시도 정책은 불필요. **“좌측으로 내리라”는 지시와 실제 운전석/문 위치가 충돌하면 참조부터 대조**하는 짧은 예시·회귀 시나리오만 추가 가치. 우측 운전대 자체를 오류로 일반화하면 안 됨. |

## 기존 eval이 입증하는 범위

- `storytelling-with-still-images/evals/evals.json` L5–15(id 1), L19–28(id 2): 이미지 전용·대사 보존·화자별 사실·실측 음성에 맞춘 재타이밍을 이미 요구한다. **다중 화자의 실제 파일 조립 성공 증거는 아님.**
- `creative-production/evals/evals.json` L65–75(id 10–11): 지원 설정·최소 프리뷰·기존 승인 재사용·최종 QA. **동일 과업의 공급자 간 비교시험은 아님.**
- 같은 파일 L41–57(id 7–8), L83–87(id 13): 혼합 음원을 stem으로 오인하지 않기, 청취/싱크 미검증, 미지원 오디오 제어와 별도 승인 경계. **분리 후 잔류 음악·대사 손상 검수의 실제 성공은 미확인.**
- `storyboarding-video/evals/evals.json` L65–73(id 6): 40→52 숫자 표시·원인 미정·무음 계약. **렌더된 숫자·계산·차트의 결정론적 검증 테스트는 아님.**
- `video-production-assets/support/qa/rofan-craft-skill-evals.json` §method L5–10: 텍스트/2D 계획·수동 의미 평가이며 실제 미디어·endpoint 검증을 명시적으로 제외한다. 이 자료를 다섯 후보의 실매체 성능 근거로 쓸 수 없다.

## 튜토리얼 근거와 미확인

아래는 모두 `docs/analysis/youtube-craft-upgrade-2026-11-17/evidence/` 아래 **로컬 자막 텍스트** 위치다. 재생·실청취·현재 공급자 기능 검증으로 승격하지 않았다.

- ② `BjZ4viBcpZU/md/Best_AI_Video_Generator_2026_(Watch_Before_You_Buy_20261117.md` L14·42: 같은 prompt/settings로 네 모델을 시험했다는 제작자 설명. 동일 입력이 곧 공정한 비교나 보편적 순위임을 뜻하지 않는다.
- ③ `AROGVvDV4w0/md/How_to_Make_YouTube_Explainer_Videos_With_AI_(No_E_20261117.md` L14: 화면 숫자가 정확히 표시됐다는 설명. **결정론적 검증법 자체의 근거가 아니라 검증 필요성을 제기하는 사례**다.
- ④ `_X7KQVwsn9U/md/How_to_Make_Studio-Quality_AI_Animation_(Full_Guid_20261117.md` L58: baked music이 장편 편집에서 끊기므로 분리 후 별도 스코어를 쓰자는 설명. 무료 여부·분리 품질·현재 지원은 미확인이다.
- ⑤ `1BzzdY-nK9A/md-selected-en/How_I_Get_Perfect_AI_Realism_in_Every_Shot_(3_Step_20261117.md` L247–262: 퇴장 방향과 운전대 참조의 모순을 발견하고 참조를 교정했다는 설명. 자막 확인이지 수정 전후 영상의 독립 검증은 아니다.
- ① “다중 화자·음성 선행·스틸 전용” 세 조건을 모두 충족하는 특정 튜토리얼의 완결 실행 근거는 이번 조사에서 **미확인**이다. 사용자 제시 후보로서 저장소와 대조했으며, 특정 영상의 검증된 공정이라고 단정하지 않는다.

## 최소 증분 제안 — 구현하지 않음

1. **우선: ③ 검증 예제.** 기존 10 근거/21 QA의 연결 사례로 승인 수치 40·52 → 증가 12, 증가율 30%(분모 40) → 표시 문자열·차트 비율·단위 → 최종 화면/읽기 hold를 대조한다. 잘못된 분모·반올림·누락 단위·렌더 글리프 손상은 별도 실패로 적는다. 원인 설명은 추가하지 않는다. 기존 claim/QA 필드로 기록하며 코드 프레임워크를 강제하지 않는다.
2. **우선: ② 선택적 과업 trial.** 24의 기존 프리뷰 설명에 승인된 영상 후보·같은 입력 버전·같은 과업/수락 기준·공통 지원 설정·실제 요청/출력·횟수/비용·관측 실패를 연결하는 사례를 둔다. 공통 설정이 없으면 차이를 밝히고 비동등 비교로 처리한다. 한 번의 성공을 성공률로 일반화하지 않는다. 실제 실행은 기존 승인 범위 안에서만 한다.
3. **다음: ① 연결 예제.** `storytelling-with-still-images`의 기존 cue 표로 두 화자와 내레이터의 확인된 녹음→턴/쉼 실측→hold/반응 배치→speech 우선 믹스→실제 출력 검수 사례를 제시한다. 화자 미확인 트랙·고정 runtime 초과·금지된 자막·스틸에 불필요한 립싱크 강제를 회귀 조건으로 둔다. 새 오디오 생성이나 영상 모델을 기본 추가하지 않는다.
4. **다음: ④ 후반 오디오 사례.** 09에 서로 다른 음악이 내장된 두 클립을 예로, 제공된 실제 stem이 있으면 사용하고 없으면 승인된 분리/별도 음향 대안만 제안한다. 분리 결과는 대사 자음·호흡 손상, 잔류 음악, 룸톤/잔향 점프를 원본 및 최종 믹스로 들어 대조한다. 연속 스코어는 기존 `shot_id` 없는 시퀀스 큐에 연결한다. 기본 native-audio 경로는 바꾸지 않는다.
5. **낮은 우선: ⑤ 예시/회귀만.** 29 R1 또는 21 §5에 승인된 차량 설정·공간 좌우·실제 참조 운전석/문·프롬프트 퇴장 방향을 먼저 대조하는 예를 둔다. 모순이 미해결이면 기존 blocker로 반환하고 승인된 참조를 몰래 재설계하지 않는다. 좌핸들/우핸들 정답을 세계 공통 규칙으로 만들지 않는다.

모든 제안은 **기존 소유자·승인·정체성 시트(전체 image_backed의 인물당 Sheet A 7뷰 포함)·라우팅·원장/스키마/enum을 그대로 유지**하는 문서/예시/eval 증분이다. `higgsfield-video-explainer/SKILL.md` L5–7·22·100–104의 단일 내레이터·고정 블록 영상 공정은 ①의 다중 화자 스틸 공정과 다르므로 대체안으로 합치지 않는다.

## 수행·검증 기록

- 수행: 읽기 전용 coverage 조사 및 이 외부 Markdown 노트 작성. 저장소 코드/문서 변경·추가 테스트 없음.
- 명령: `nl -ba`, `sed`, `find`, `rg`로 원문/관련 파일 확인; 무시된 로컬 evidence는 `rg --no-ignore` 및 읽기 전용 `python3` 텍스트 탐색으로 확인. `python` 호출 1회는 실행 파일 부재로 실패했고 `python3`로 재실행했다.
- 시작/종료 `git status --short`에 기존 변경 목록이 유지됐다. `git diff --cached --name-only` 출력은 비어 있었다. 테스트/eval 실행·실매체 검증은 하지 않았다.
- 남은 위험: 작업 중인 원문의 후속 변경에 따라 줄 번호가 달라질 수 있다. 검사 범위 밖의 중복 절차 존재와 실제 미디어/공급자 성능은 미확인이다.
- 권장 다음 단계: 리뷰어가 ②·③의 좁은 검증 공백을 먼저 확인한 뒤 기존 파일 내 예시/eval 추가 여부를 결정한다.

```acceptance-report
{
  "criteriaSatisfied": [
    {"id": "criterion-1", "status": "satisfied", "evidence": "요청한 다섯 후보를 지정 원문·연관 eval과 대조했고 저장소 수정 없이 기존 계약 내 증분만 제안했다."},
    {"id": "criterion-2", "status": "satisfied", "evidence": "매트릭스에 정확한 경로·절·줄을 제공하고 자막 설명·실매체 관찰·미확인을 분리했다."}
  ],
  "changedFiles": ["/home/declan/.pi/agent/sessions/--home-declan--/subagent-artifacts/outputs/d9cdabf6-308b-4ea6-8332-3d92b4d5058e/coverage-research.md"],
  "testsAddedOrUpdated": [],
  "commandsRun": [
    {"command": "git status --short", "result": "passed", "summary": "시작/종료 기존 변경 목록 확인; 이 작업의 저장소 수정 없음."},
    {"command": "git diff --cached --name-only", "result": "passed", "summary": "출력 없음; staged 파일 없음."},
    {"command": "nl -ba / sed / find / rg / rg --no-ignore", "result": "passed", "summary": "지정 원문·연관 참조/예시/eval·로컬 자막 위치 확인."},
    {"command": "python (읽기 전용 자막 탐색)", "result": "failed", "summary": "python 실행 파일 부재; 파일 변경 없이 종료."},
    {"command": "python3 (읽기 전용 자막 탐색)", "result": "passed", "summary": "로컬 자막의 후보 관련 문장과 줄 위치 확인."},
    {"command": "테스트·eval·미디어 실행", "result": "not-run", "summary": "읽기 전용 조사 범위이며 테스트 파일도 변경하지 않음."}
  ],
  "validationOutput": ["기본 계약은 다섯 후보 모두 관련 부분이 존재한다. 비교시험 프로토콜과 숫자/텍스트의 데이터-렌더 연결 검증이 우선적인 좁은 보완 후보다.", "다중 화자 스틸 완결 실행과 실제 공급자/미디어 성능은 미확인이다."],
  "residualRisks": ["저장소 전체의 절대 부재를 주장하지 않음.", "12편 전체 재생·실청취 및 실행 성능 검증 미실시.", "진행 중인 원문 변경으로 줄 번호가 변할 수 있음."],
  "noStagedFiles": true,
  "diffSummary": "저장소 diff 없음; 지정된 외부 연구 노트만 작성.",
  "reviewFindings": ["no blockers; 독립 리뷰 필요"],
  "manualNotes": "읽기 전용 과제이므로 구현·테스트 추가를 하지 않은 것이 의도된 결과다. 기존 사용자 변경은 보존했다."
}
```
