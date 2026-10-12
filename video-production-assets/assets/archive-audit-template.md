# 아카이브 영상 감사

> 읽기 전용 분석 산출물. 영상별 관찰은 `assets/shot-dna-template.md`에 연결하고, 이 문서는 인벤토리·범위·교차 영상 비교를 보관한다.
For an explicit exhaustive all-source/all-shot or cross-source craft extraction, also use [`archive-craft-crosswalk-template.md`](archive-craft-crosswalk-template.md) for the relational source-occurrence→sequence/scene→shot→within-shot-event→finding→existing-owner/QA join. This crosswalk is conditional; it is not required for single-reference or ordinary archive inventory work. Missing rows and open gates remain explicit, never “zero findings.”

## 범위와 커버리지

- 아카이브/경로: {경로 또는 사용자 제공 이름}
- 요청된 범위: {폴더 전체 / 지정 영상 / 필터}
- 발견한 영상: {개수}
- 처리 상태: {모드별 대상/완료/미검토/실패 수; 상세는 아래 coverage ledger}
- 분석 방식과 제한: {전체 재생 / 표본 프레임 / 타임코드·구간 / 오디오 청취 여부}
- 사용한 외부 메타데이터: {게시글 ID·캡션·날짜 등과 출처}

## Coverage ledger

한 행은 안정된 `archive_id` 하나와 한 coverage mode 조합이다. ID는 파일의 고정 경로/식별 정보에 연결하고 정렬 순번·`#6`·`AV06`처럼 위치에서 만들지 않는다. 모든 행에 정확한 파일명과 evidence locator를 적는다. `추출/발견` 수와 실제 `검토` 수를 분리하고, 미실행·미보존은 `0`/`미실행`/`부분(첫 N)`처럼 명시한다.

| archive_id (stable; not ordinal) | exact filename | coverage mode | attempted/completed or extracted → actually reviewed | exact source range / sampling | timestamp-list completeness | evidence locator | status / limits |
|---|---|---|---|---|---|---|---|
| {stable ID} | {full filename} | full-source decode | {files/sources attempted and completed} | {whole source duration or exact decoded range} | N/A | {decode log / metadata path} | {return status; decode is not visual review} |
| {stable ID} | {full filename} | scene locator / timestamps | {candidates found; timestamp entries retained / candidates} | {exact PTS/ranges and locator threshold} | {complete / first N only / partial / none} | {locator manifest / log} | {locator events are candidates, not certified cuts} |
| {stable ID} | {full filename} | still/strip extraction | {images or intervals extracted} | {exact source intervals; sample rate / frames per interval} | {timestamp source and completeness} | {image paths / extraction manifest} | {sampling limits} |
| {stable ID} | {full filename} | manual visual review | {extracted items / items actually inspected} | {exact reviewed intervals or source ranges} | {timestamp source and completeness} | {review record / exact image locator} | {sample review is not continuous playback} |
| {stable ID} | {full filename} | continuous playback | {sources / segments actually watched} | {exact played ranges; say full source only if watched continuously} | N/A | {playback notes / locator} | {0 / not reviewed when applicable} |
| {stable ID} | {full filename} | audio listening | {sources / segments actually heard} | {exact listened ranges} | N/A | {listening notes / locator} | {metadata alone is not listening} |

For each source, include every relevant mode—even if `0 / not reviewed`; do not infer a completed mode from another mode's success.
Scene-locator evidence는 `DETECTOR_CANDIDATE`/timestamp hypothesis와 실제 경계 확인을 분리한다. 샘플을 요청한 `requested_s`와 추출 프레임의 실제 `source_pts_s`를 locator/evidence note에 모두 보존하고, 원본 PTS를 정확한 컷 시각으로 부르지 않는다. `C/B/G/S.P`는 영상별 분석 locator일 수 있으며 `archive_id`나 프로젝트 shot ID가 아니다. `SH###`는 경계 양쪽을 확인한 경우에만 shot/cut ID로 사용한다.


| archive_id (stable; not ordinal) | exact filename / post ID | supplied caption/context | duration/frame size/fps/stream metadata | actual inspected ranges | linked Shot DNA | status / unknowns |
|---|---|---|---|---|---|---|
| {stable archive_id} | {exact filename} | | | | | |

## 영상별 분석

각 영상은 별도 항목으로 다룬다. Shot DNA에는 샘플에서 관찰한 비트만 연결하고, 측정되지 않은 컷·구간은 만들지 않는다.

| archive_id (stable; not ordinal) | exact filename | Shot DNA/artifact link | directly observed beats/on-screen text | caption/user info | interpretation/audience function | audio inspection scope | limits/unknowns |
|---|---|---|---|---|---|---|---|---|
| {stable archive_id} | {exact filename} | | | | | | |

## 아카이브 전체 패턴과 스킬 대조

반복 패턴은 이를 직접 뒷받침하는 영상 ID와 확인 범위를 적는다. 조회수·유지율·전환 데이터가 제공되지 않으면 성과에 대한 결론을 적지 않는다.

| 패턴·기법 | 근거 영상 ID와 표본 범위 | 예외·미검사 범위 | 현재 스킬의 파일/절차 | 판정 | 최소 수정 후보 |
|---|---|---|---|---|---|
| | | | | 이미 커버 / 부분 커버 / 갭 후보 / 증거 부족 | |

## 우선순위 권고

| 순위 | 제안된 변경 | 사용자/제작 문제와 근거 | 기존 절차와의 중복 여부 | 확인 기준 |
|---|---|---|---|---|
| | | | | |

## 판정 규칙

- 캡션·게시 메타데이터·프레임에서 직접 본 것·분석자의 해석을 분리한다.
- 표본에서 보이지 않은 요소는 영상 전체에 없다고 단정하지 않는다.
- 오디오 스트림 메타데이터는 청취 결과가 아니다. 듣지 않은 대사·음악·효과·싱크는 미검증이다.
- `이미 커버`는 현재 스킬의 정확한 절차/참조를 적는다. 새 갭은 기존 경로로 해결되지 않는 작업 단계일 때만 제안한다.
- 분석만 요청된 경우 원본 변경·외부 업로드·생성·편집·게시를 수행하지 않는다.
