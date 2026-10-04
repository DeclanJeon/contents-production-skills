# Local Assembly (ffmpeg)

Phase 5: turn N generated clips + audio into one finished MP4. Local ffmpeg is standard for this skill (video-explainer's ffmpeg ban applies only to its own narrated pipeline).

## 0. Preflight

```bash
for f in shots/*.mp4; do ffprobe -v error -select_streams v:0 \
  -show_entries stream=width,height,r_frame_rate,codec_name -show_entries format=duration \
  -of default=noprint_wrappers=1 "$f"; done
```

Record width/height/fps/duration per clip. Pick the **target format** once (usually the reference's: e.g. 1280×720, 24fps) and convert everything to it.

## 1. Normalize every clip

```bash
mkdir -p norm
ffmpeg -i shots/shot_01.mp4 \
  -vf "scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,fps=24,format=yuv420p" \
  -c:v libx264 -crf 18 -preset slow -an norm/01.mp4
```

Repeat per shot (`02.mp4`, `03.mp4`, …). `-an` strips per-clip audio; the soundtrack is rebuilt in step 4. If a clip should keep diegetic sound, keep its audio and treat it as an additional mix input instead.

## 2. Cut in beat order

Same encoding everywhere → concat demuxer (instant, lossless):

```bash
printf "file 'norm/01.mp4'\nfile 'norm/02.mp4'\nfile 'norm/03.mp4'\n" > list.txt
ffmpeg -f concat -safe 0 -i list.txt -c copy cuts.mp4
```

Dissolves (only where the beat sheet marks one, ~0.5s):

```bash
ffmpeg -i norm/01.mp4 -i norm/02.mp4 -filter_complex \
  "[0:v][1:v]xfade=transition=fade:duration=0.5:offset=6.5[v]" \
  -map "[v]" -c:v libx264 -crf 18 -preset slow seg12.mp4
```

Default is hard cuts. The offset equals shot 1's duration minus the fade length.

## 3. One shared grade

Apply a single grade chain **after** the cut so every shot gets byte-identical treatment (this is what hides AI shot-to-shot variation):

```bash
ffmpeg -i cuts.mp4 -vf \
  "eq=contrast=1.05:saturation=1.04:brightness=0.01,colorbalance=rs=-0.02:bs=0.03:rm=0.01:bm=-0.01" \
  -c:v libx264 -crf 18 -preset slow graded.mp4
```

Tune the constants against one QC frame per beat until it matches the style bible. If a `.cube` LUT is available, use `lut3d=file.cube` inside the same `-vf` chain. Never grade clips individually.

## 4. Soundtrack

```bash
# fit BGM to total duration (loop or trim)
ffmpeg -i bgm.wav -t 43.5 -af "afade=t=in:d=0.5,afade=t=out:st=42.5:d=1" bgm_fit.wav

# optional: duck BGM under a SFX / VO stem
ffmpeg -i bgm_fit.wav -i vo.wav -filter_complex \
  "[1:a]asplit=2[vo][sc];[vo]asplit[voout][scin];[0:a][scin]sidechaincompress=threshold=0.05:ratio=8:attack=50:release=400[duck];[duck][voout]amix=inputs=2:duration=first[mix]" \
  -map "[mix]" mixed.wav

# single soundtrack, no stems → just use bgm_fit.wav
```

Cue SFX at beat timestamps with `adelay=14200` (ms) summed via `amix` when needed.

### Loudness (two-pass loudnorm)

```bash
# pass 1 — measure
ffmpeg -i mixed.wav -af loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json -f null -

# pass 2 — apply the measured_* values printed by pass 1
ffmpeg -i mixed.wav -af \
  "loudnorm=I=-14:TP=-1.5:LRA=11:measured_I=..:measured_TP=..:measured_LRA=..:measured_thresh=..:offset=..:linear=true" \
  final_audio.wav
```

## 5. Mux + export

```bash
ffmpeg -i graded.mp4 -i final_audio.wav \
  -c:v libx264 -crf 18 -preset slow -pix_fmt yuv420p \
  -c:a aac -b:a 192k -shortest -movflags +faststart final.mp4
```

Optional burned subtitles: add `subtitles=subs.ass` to `-vf` on the video (generate the ASS/SRT from narration timing first).

## 6. QC frames

```bash
mkdir -p qc
ffmpeg -ss 14.2 -i final.mp4 -frames:v 1 -q:v 2 qc/beat3.jpg    # one per beat timestamp
```

Compare each against the reference frame of the same beat (composition, grade, character) — this is Phase 6's evidence.

## Failure notes

- `format=yuv420p` missing → some players reject the file; always include it.
- Concat error `dimensions differ` / `timebase mismatch` → a clip skipped step 1; re-normalize.
- Audio drift over long films → you concat'd video with attached audio; keep audio separate until step 5 (as shown).
- Output duration wrong → check `-shortest` vs beat-sheet total; total must equal the sum of shot durations.
