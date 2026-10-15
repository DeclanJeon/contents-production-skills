# 기술 판단용 공식 웹 근거

접근일: 2026-10-12. task-local `web-citations-ledger.json`의 실제 발급번호를 사용한다. 제작자 의도/실제 사용도구/성과/저작권을 확정하는 근거가 아니다.

## [1] 20.17 select / 11.171 minterpolate

scene은 새로운 scene일 가능성 값이며 실제 hard cut의 인증이 아니다. PTS와 n은 다른 값. motion interpolation은 출력 프레임 생성 경로이므로 느려 보이는 영상만으로 고속촬영을 확정할 수 없다.[1]

- 정확한 관찰 구절: `value between 0 and 1 to indicate a new scene; a low value reflects a low
probability for the current frame to introduce a new scene` / `Convert the video to specified frame rate using motion interpolation.`
- 적용 경계: 이번 파일의 제작 경로를 증명하지 않는다.

## [2] Camera / Lens

프리셋만으로 왜곡계수/주점이 결정되지 않는다. optical center는 정규화 좌표다.[2]

- 정확한 관찰 구절: `But such settings as distortion coefficients and principal point are not included in the presets and` / `The values are given in normalized image coordinates.`
- 적용 경계: 프레임만 보고 실제 mm/센서/거리 확정하지 않음.

## [3] Solve / Tripod / Refine

회전만 있는 tripod footage는 실제 feature 3D 위치를 결정 못하고 relative rotation을 푼다. intrinsics refine도 대략 초기값이 필요하다.[3]

- 정확한 관찰 구절: `it is impossible to determine the actual feature points in space due to a lack of information.` / `But you still have to know approximate initial values –`
- 적용 경계: 사진/고정 공간을 완전한 3Dsolve 근거로 취급하지 않음.

## Sources

[1] https://ffmpeg.org/ffmpeg-filters.html
[2] https://docs.blender.org/manual/en/latest/movie_clip/tracking/clip/sidebar/track/camera.html
[3] https://docs.blender.org/manual/en/latest/movie_clip/tracking/clip/toolbar/solve.html
