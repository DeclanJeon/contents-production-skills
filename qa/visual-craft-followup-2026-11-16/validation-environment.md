# 검증 환경 이력

- 첫 전체 실행 `full-pytest.txt`:180초 시간 제한으로 중단,완료/통과 아님. 뒤 실행에서 발견된 quota와 첫 timeout의 인과까지 단정하지 않는다.
- 진단 전체 실행 `full-pytest-diagnostic.txt`:200failed/527passed/4skipped/97errors/325subtests,35.21s. 실제 `/tmp/pytest-of-declan/pytest-394/...` 복사/fixture 생성에서 `Errno122 Disk quota exceeded`가 다수 확인됨. `/tmp`는 `tmpfs ... usrquota`이고 전역 여유 공간/inode가 있어도 사용자 quota를 뜻하지 않음. 제품 수정으로 우회하지 않았음.
- `/home` 별도 임시 경로 실행 `full-pytest-home-temp.txt`:815passed/2failed/4skipped/532subtests,43.66s. 두 Chrome PDF CLI 검사에서 긴 TMPDIR로 인한 `Socket path too long`을 확인. 기존 fixture/렌더 코드를 고치거나 해당 검사를 skip하지 않았음.
- 짧은 사용자 캐시 TMPDIR(`/home/declan/.cache/vcf246t-20261116/tmp`)와 새 owned basetemp(`isolated-2`)에서 동일 전체 suite를 재실행: **817passed/4skipped/532subtests,43.86s**,`full-pytest-final.txt`. 소켓 경로 제한과/tmp quota를 피한 환경 변경만 했음.
- 기존 임시 파일을 정리/삭제/이동하지 않았다. 실패/중단 로그도 보존한다. 생성된 테스트 fixture/PDF는 회귀 도구 검사이며 신규 스토리 미디어/관객 효과 검증은 아니다.
