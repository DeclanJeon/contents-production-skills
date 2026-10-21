# Camera timing and lens handoff

- shot_id / camera_spec id/version / duration / FPS or PTS basis:
- World/screen conventions / actual rig constraints or unknown:
- Required reveal/contact/emotion beat:

| Local time/frame | Camera position/target | Subject position/action | Phase / speed / interpolation | Information visibility | Lens/focus target |
|---|---|---|---|---|---|

- Sensor/effective gate / focal length mm / subject and focus distance m / f-number:
- Focus plan: focus target (subject/prop ID) / focus distance m at start / pull start / pull finish / end distance / f-number / who must stay sharp and what may go soft:
- Focus plan status: `proposal` / `measured` / `not planned` (N/A reason):
- Start/end framing / hold / cut connection:
- Measured vs estimated vs design proposal:
- Supported schema / companion artifact / unsupported renderer settings:
- Required preview frames and playback / unresolved checks:

## 프리비즈 focus map 파생 (해당 시)

초점 계획이 있으면 Blender 프리비즈의 `--focus-map` 입력을 **이 표에서 파생**한다. focus map은 파생물이지 두 번째 정본이 아니다.

- focus map 파일 경로 / 파생 일자 / 기반 companion 버전:
- 파생 규칙: 표의 start/pull start/pull finish/end 거리와 f-number를 shot-local 프레임으로 옮기고, 표에 없는 프레임은 선형 보간한다.
- 드리프트 방지: companion(위 표)이 바뀌면 focus map을 재생성한다. companion과 focus map이 어긋나면 **companion이 우선**이고 map은 재생성 대상이다. map을 정본처럼 수정하지 않는다.
- 검증: 실제 렌더에서 선명/ 흐림 전환이 의도한 대상·시점에 도달했는지 확인한다. map은 미리보기 근거이지 캘리브레이션 검증이 아니다.
