# Contents Production Skills

콘텐츠 제작과 영상 제작을 하나의 브리프·승인 흐름으로 조율하는 에이전트 스킬 패키지. 프로젝트 이름은 `contents-production-skills`, 패키지 버전은 **2.0**이다.

저장소: [DeclanJeon/contents-production-skills](https://github.com/DeclanJeon/contents-production-skills).

`creative-production`이 유일한 총괄이다. 기존 영상 제작·텍스트 기획·카메라·Blender 전문 스킬을 유지하고, 현재 적용된 콘텐츠/영상 스킬의 범용 절차와 memorable-video v6의 유효한 제작 기법은 필요한 때만 읽는 참조로 통합한다. 중복 총괄·상태 원장·28개 마이크로 스킬을 함께 설치하지 않는다.

## 포함된 8개 스킬

| 스킬 | 책임 | 경계 |
|---|---|---|
| [creative-production](creative-production/SKILL.md) | 원고·소셜·캠페인·이미지·오디오·영상의 요청 분류, 제작 순서, 담당, 검토와 납품 | 단일 총괄. UI 개발이나 별도 전역 DB를 소유하지 않는다. |
| [video-production-assets](video-production-assets/SKILL.md) | 브리프, 서사/정보 비트, 각본, 연기, 시각, 샷, 조명, 애니메이션, 편집/사운드, 근거, AI 인계, QA, 발상/브랜드, 제작 운영, 납품 | 15개 선택형 모듈과 통합 전문 참조. 실제 렌더·게시 도구와 구분한다. |
| [orchestrating-video-preproduction](orchestrating-video-preproduction/SKILL.md) | 콘셉트→시놉시스→필요한 캐릭터→스토리보드의 텍스트 기획 | 총괄의 내부 레인. 텍스트만 요청하면 이미지·영상·폴더를 만들지 않는다. |
| [developing-video-synopses](developing-video-synopses/SKILL.md) | 콘셉트·로그라인·시놉시스·비트 | 사실·서사·추상 모드에 맞춰 작성한다. |
| [designing-video-character-sheets](designing-video-character-sheets/SKILL.md) | 캐릭터 정체성·행동·시각 앵커·연속성·범용 이미지 프롬프트 | 텍스트 시트. 등장인물이 없는 작업에는 생략한다. |
| [storyboarding-video](storyboarding-video/SKILL.md) | 읽을 수 있는 내러티브/정보 패널과 범용 이미지 프롬프트 | 실제 이미지·샷 타이밍·모델별 실행 입력과 구분한다. |
| [camera-spatial-design](camera-spatial-design/SKILL.md) | 카메라 위치·화각·피사체 거리·블로킹·경로의 수치 설계 | `camera-spatial-1.0` 계약. Blender 실행과 구분한다. |
| [blender-previsualization](blender-previsualization/SKILL.md) | 실제 Blender 프록시 장면·프리비즈·공간 검사 | Blender 런타임 필요. 최종 영상 품질을 보증하지 않는다. |

설치 목록의 원본은 [manifest.json](manifest.json)이다. 전문 참조는 추가 설치 스킬이 아니다.

## 제작 흐름

1. 요청한 산출물과 제외 사항을 확정하고, 공급된 출처·제품 정보·SSOT·승인을 보존한다.
2. 목적과 형식에 맞는 레인만 로드한다. 원고 한 편이나 프롬프트 하나를 전체 제작으로 확대하지 않는다.
3. 실제 원고·기획·모듈 에셋을 작성한다. 사실, 계산, 해석, 창작 제안, 미확인을 구분한다.
4. 다단계 영상만 기존 `project.json`을 정본으로 사용한다. 시리즈 바이블·SSOT·공급자 입력은 버전이 있는 종속 에셋으로 연결한다.
5. 이미지 기반 전체 프리프로덕션은 [검토 계약](video-production-assets/references/preproduction-review.md)에 따라 정확한 프로젝트 폴더, 실제 정지 이미지, 검사와 사용자 검토를 갖춘다.
6. 별도 영상 진행 요청 뒤 현재 도구·모델·입력 스키마·가격을 확인한다. 샷/산출물 수, 설정, 실행·재시도·비용 상한을 승인받은 뒤에만 실행한다. 무료/로컬 샘플도 실행 승인 범위에 포함한다.
7. 실제 결과를 검사하고 요청한 형식으로 납품한다. 계획, 파일 생성, 기술/시청각 검사, 사용자 수락, 게시 상태를 따로 보고한다.

단독 전문 스킬은 총괄의 범위 계약을 한 번 확인한다. 이미 위임받은 전문 스킬은 총괄로 재귀 호출하거나 인터뷰·승인 원장을 다시 만들지 않는다. 수정 시 영향을 받는 종속 에셋과 승인만 stale로 처리한다.

레퍼런스 기반 작업은 후보 선택 → 관찰/해석/미확인 분리 → 제작 원리의 새 소재 적용 → 필요한 프로젝트 스타일 브리프 → 정성 QA로 연결한다. 주제·시놉시스 탐색을 요청한 영상에만 [탐색 계약](orchestrating-video-preproduction/references/video-direction.md#discovery-topic-and-synopsis)의 단계별 기본 5개를 적용하며, 명시 개수·확정 입력·단일 산출물은 보존한다. 회고는 요청된 프로젝트 기록/제안이다. 자동 스킬 개선·승격·브랜드 프로필 갱신과 숫자 유사도 기반 통과/재시도는 지원하지 않는다.

## 외부 실행 도구

텍스트 원고와 텍스트 영상 기획에는 GPU, 미디어 계정, 특정 에이전트 프레임워크가 필요 없다. 실제 이미지·영상·음악·음성·편집·게시에는 선택한 도구의 설치/인증과 현재 기능 확인이 필요하다.

- 콘텐츠/검토 이미지: `codex-imagen`을 기본 실행자로 사용하고 현재 인증·입력·출력·사용량/비용 조건을 확인한다. 준비되지 않으면 blocker로 보고하며 자동 공급자 전환을 하지 않는다. 이미지 실행 제한은 [생성 경로·비용 라우팅 §2](video-production-assets/references/24-production-execution.md#2-이미지-생성-경로-정지-에셋)를 따른다.
- 실제 영상/오디오 생성·편집: 선택된 Higgsfield, Fal, ComfyUI, Remotion, FFmpeg 또는 해당 실행기. Higgsfield 이미지 생성은 제외한다. 고정 모델 순위·가격표를 정답으로 사용하지 않는다.
- 전문 각본/스토리커머스, 출처 조회, 플랫폼 운영: 요청한 레인에 해당하는 외부 스킬과 도구만 사용한다.
- 글 리라이트나 검토 수락은 생성 과금·게시·DB 수정·배포를 허가하지 않는다.

선택한 단계의 의존성이 없으면 도달 가능한 준비를 끝내고 정확한 부족 항목을 보고한다. 설치된 스킬이 있다는 사실만으로 인증·실행 가능·권리 확보를 주장하지 않는다.

세부 사용법: [USAGE_GUIDE.md](USAGE_GUIDE.md). 역할과 이전 기능의 통합 위치: [skill-routing.md](integrations/skill-routing.md). 출처·권리 경계: [package-provenance.md](integrations/package-provenance.md).

## 설치 및 업데이트

Python 3.10 이상. 저장소 루트에서 실행한다.

```powershell
$skillRoot = if ($env:CODEX_HOME) { Join-Path $env:CODEX_HOME 'skills' } else { Join-Path $HOME '.codex\skills' }
python scripts/install_package.py --skills-root $skillRoot
```

전체 스킬·지원 파일·대상 충돌·경로 중첩을 쓰기 전에 검사한다. 기존 폴더를 자동 병합/덮어쓰기하지 않는다. 명시적 교체에는 새로운 백업 경로가 필요하다.

```powershell
$backup = Join-Path $HOME ('.codex/skill-backups/contents-production-' + (Get-Date -Format 'yyyyMMdd-HHmmss'))
python scripts/install_package.py --skills-root $skillRoot --replace --backup-dir $backup
# 추가 검색 루트도 이전할 때만 --alias-root (Join-Path $HOME '.agents/skills') 지정
```

지원 자료는 `video-production-assets/support/`에 복사된다. 무관한 스킬, 외부 실행기, 키/OAuth, 모델 가중치, 호스트 설정은 변경하지 않는다. I/O 실패는 실제 적용 경로와 남은 백업을 보고하며 여러 폴더의 원자적 설치를 보장하지 않는다. 설치 후 에이전트의 스킬 목록을 새로고침한다.

이 프로젝트 업데이트 자체는 사용자 전역 스킬 설치본을 덮어쓰지 않는다. 정본은 저장소이며 설치는 위 명령으로 별도 수행한다.

## 검증

```powershell
python scripts/test_install_package.py
python video-production-assets/scripts/test_validate_project.py
python camera-spatial-design/scripts/test_spatial_spec.py
```

실제 실행한 패키지·설치·기획 시나리오 증거는 [qa/consolidation-validation.json](qa/consolidation-validation.json)에 둔다. 텍스트 결과 12개(현재/이전 총괄 각 6개)는 [평가 뷰어](qa/evaluation-review.html)와 [자동 분류 결과](qa/behavior-benchmark.json)에서 비교할 수 있다. 이번 표본에서 자동 분류 기준 충족 수는 양쪽 모두 15/18이며 품질 향상을 입증한 벤치마크가 아니다. 이전 릴리스 기록은 [qa/package-validation.json](qa/package-validation.json)에 보존한다. 구조 검사는 미디어 디코딩·시청·청취·사실 진위·권리·공급자의 현재 기능을 검증하지 않는다. 텍스트 평가를 실제 미디어 제작 성공으로 보고하지 않는다.

## 버전 일관성과 자동 동기화 (Junction)

이 저장소가 단일 원본(SSOT)이며, 설치된 하네스는 전부 Junction으로 이 저장소를 가리킵니다. 저장소를 고치면 `~/.codex/skills`(Codex), `~/.claude/skills`(Claude Code), `~/.agents/skills`(OpenCode)가 동시에 같은 내용을 읽습니다.

```powershell
# 저장소 -> 설치 루트로 링크 (기존 실체 폴더는 백업 후 교체, 멱등)
python scripts/sync_installed.py            # 실제 동기화
python scripts/sync_installed.py --dry-run  # 계획만 확인

# 버전 일관성 검사 / 일괄 범프 (manifest + CHANGELOG + 전 스킬 frontmatter)
python scripts/check_versions.py
python scripts/bump_version.py --part minor --bump-skills

# git 훅 설치: 커밋 전 version check(차단), 커밋/머지/리베이스 후 자동 싱크
python scripts/install_hooks.py
```

- `post-commit` / `post-merge` / `post-rewrite`: 커밋·풀·리베이스가 끝나면 설치 루트를 자동 재싱크합니다.
- `pre-commit`: 버전 일관성이 깨지면 커밋을 차단합니다 (`git commit --no-verify`로 우회).
- GitHub Actions (`.github/workflows/ci.yml`): push/PR 시 `check_versions.py`와 pytest로 검증합니다.
- 파생 산출물 `video-production-assets/support/`는 싱크 시 재생성되며 gitignore됩니다.
- 기존 복사본은 `~/.skills-sync-backup/<타임스탬프>/`에 백업됩니다.

## 출처와 재사용

이 저장소에는 재사용 라이선스가 없다. 공개 저장소, 출처 표기, AI 판단은 재배포 허가가 아니다. 기존 서적·원문·Notion 자료, 개인 서버/계정 설정, 인증 자료, 모델 가중치와 사용자 프로젝트 산출물은 새 패키지에 반입하지 않는다. 현재 스킬에서 검토한 범용 제작 절차는 패키지의 기존 계약에 맞춘 운영 지침으로 정리하며 외부 helper/코드의 라이선스를 임의로 전용하지 않는다.
