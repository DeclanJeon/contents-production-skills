# Voice and Soundtrack Mix Finishing

Local engineering guidelines for polishing approved spoken dialogue and carving background music space to preserve vocal intelligibility.

> [!IMPORTANT]
> The empirical figures cited in this document (frequencies, ratios, decibels, and percentages) stem from a creator's vocal-mixing rule of thumb and represent **optional starting points for listening**, not rigid physical constants.
> Every processing stage is optional: when listening reveals no defects (such as low-end boom, harsh sibilance, or uneven delivery), pass the dialogue with **no processing (bypass)** as the default choice.

## 1. Scope and Boundaries

This reference applies to adopted or approved takes of dialogue and narration, and BGM carving to clear space for the voice.

- **Defect repair belongs to take repair**: If an individual take suffers from acoustic defects (such as steady background noise, microphone pops, harsh sibilance, or unstable recording levels), use [take repair](../../video-production-assets/references/take-repair.md) for smallest-eligible intervention.
- **Ambiguous requests**: If an audio request is ambiguous or lacks stated context (such as "this recording sounds muddy"), do not jump straight to mix finishing. Check take-repair for defect triage or confirm the production stage first.
- **Sequential handoff**: When both defect repair and mix finishing are required, complete take-repair first and then proceed to mix finishing on the approved take.
- **Mute protection**: Requests specifying `no_audio` or silent video are not processed by this finishing reference; mute constraints are strictly preserved.
- **Separate cues and generation**: Voiceover synthesis, BGM composition, and external sound generation are not owned by this document; follow the [audio cue handoff](audio-production-routing.md).

## 2. Listen First; Bypass is Valid

Always listen to the raw audio stems before applying any filter:

1. If vocal clarity is already adequate and no frequency masking occurs between speech and music, proceed without applying any filter (no processing).
2. Apply an intervention when an observed acoustic problem calls for it.

## 3. Optional Listening Starting Points

The following values are derived from a creator's vocal-mixing rule of thumb as optional starting points for listening; adjust or skip them based on actual playback. Additional parameter ranges (such as cut depths or Q values) are design proposals, not from the source.

1. **Subtractive Clean-up (Low-cut and Boxiness)**:
   - **High-pass filter**: 100 Hz serves as an optional starting point for speech to attenuate unnecessary stage rumble. For deep male speech, 80 Hz can be used as a relaxed starting point. If low-end rumble is absent, pass without cutting.
   - **Problematic resonances**: When listening reveals boxiness, a narrow notch across 300–500 Hz (1–3 dB cut, design proposal, not from the source) can be evaluated. When nasal resonance is excessive, 800 Hz–1.5 kHz can be attenuated gently.
   - **Vocal frequency reference**: 60–100 Hz (sub-low), 150–300 Hz (body and warmth), 300–500 Hz (muddiness), 800 Hz–1.5 kHz (nasal resonance), 2–5 kHz (presence), 5–8 kHz (sibilance), and above 8 kHz (air).
2. **Dynamics Control (Compression)**:
   - **Character**: Consider smooth opto-style behavior (such as LA-2A response) for dialogue. Faster FET characteristics (1176 style) can be evaluated for rapid rhythmic speech.
   - **Parameters**: 4:1 compression ratio serves as a perceptible starting point (a 3:1 to 4:1 range is a design proposal, not from the source). Gain reduction of 2–3 dB offers a gentle starting guideline; the creator notes "많이 눌러도 3-5dB까지" (up to 3–5 dB even under heavier compression). Set release times so subsequent syllables are not cut off. If volume is already uniform, skip compression.
3. **De-essing**:
   - When sibilant consonants like sharp 's' sounds protrude, focus de-essing on the 5–8 kHz band as an optional starting point. If sibilance is natural, leave untreated.
4. **Saturation (Subtle Harmonic Warmth)**:
   - When a vocal sounds thin or dry, subtle harmonic saturation with 10–20% dry/wet mix provides an optional starting point. If harmonic depth is already adequate, skip saturation.
5. **Tone Shaping and Air (Additive EQ)**:
   - Prefer cuts; boost sparingly when listening calls for it. The creator's examples are air above 8 kHz and a small 150–300 Hz lift for a thin voice.
6. **Spatial Depth and Pre-delay**:
   - **Depth hierarchy**: Space pushes sounds back while dry signals stay forward. Dialogue is the narrative focal point and should remain up front with minimal reverb compared to BGM and SFX (relative ratio examples: drum 10, guitar 8, piano 4, vocal 2; creator's music-mix example, adapted here as "least reverb on dialogue").
   - **Pre-delay**: When reverb is engaged, a 20 ms pre-delay serves as an optional starting point to let initial consonants pass clearly before reverberation starts.
   - **Delay sync**: When musical delay is desired, tempo-synced 1/4 or 1/8 note delays are an optional starting point; skip delay for standalone dialogue.

## 4. BGM Carving and Ducking

- **Spectral carving**: Because background music accompanies dialogue rather than competing with it, small 1–2 dB cuts (design proposal, not from the source) at 250 Hz (vocal body) and 2 kHz (presence) on the BGM track serve as optional starting points to prevent vocal masking. If no masking occurs, leave BGM equalization untouched.
- **Dynamic ducking**: When music levels overwhelm speech, apply sidechain compression using the dialogue stem as trigger. Refer to the existing ducking chain in [assembly.md](../../higgsfield-video-replicate/references/assembly.md) (L66–68) rather than inventing arbitrary parameters.

## 5. Non-Destructive Local Processing

Always keep original recording stems unaltered and write a new output file for any derived audio.

```bash
# Example local non-destructive chain (example parameter values are design proposals):
ffmpeg -nostdin -n -i voice_raw.wav -af \
  "highpass=f=100,equalizer=f=400:t=q:w=1.5:g=-2,equalizer=f=10000:t=h:g=1.5,deesser=i=0.5:f=0.5:s=o,acompressor=threshold=-18dB:ratio=4:attack=20:release=250" \
  voice_finished.wav
```

## 6. Quality Assurance and Delivery Standards

- **Level-matched A/B comparison**: Evaluate every filter pass by toggling bypass with output levels matched (level-matched A/B comparison), ensuring that loudness increases are not mistaken for quality improvements.
- **Subjective listening verification**: Technical compliance never substitutes for auditory verification; `audio_listening_verified` remains false until personally auditioned.
- **Delivery loudness policy**: This reference sets no own loudness target; master delivery values follow the owning pipeline.
  - For replicated video workflows, delivery follows [assembly.md](../../higgsfield-video-replicate/references/assembly.md) (-14 LUFS, -1.5 dBTP).
  - For community shorts workflows, delivery follows [pipeline-stages.md](../../community-shorts-stills-pipeline/references/pipeline-stages.md) (-16 LUFS, -1.5 dBTP).

## 7. Approval and Cost Boundaries

- **Auto-permitted**: Local non-destructive filtering, parameter calculation, writing new derivative files in workspace directories with `-n` (local only; nothing leaves the machine).
- **Approval required**:
  - Any upload or transfer of audio to an external service, whether free or paid, requires prior approval.
  - Any external remastering, enhancement or regeneration API or service, whether free or paid, requires prior approval.
  - Commercial music licensing, external paid regeneration, overwriting or deleting raw source files, or publishing to public platforms.
