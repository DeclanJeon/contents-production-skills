# Audio cue handoff

`creative-production` owns cue assignment and the existing sound plan. Text preproduction returns requirements only. This handoff adds no primary route, project ledger or execution authority.

## Decide per cue

1. Apply locked scope first: no audio means mute; no music excludes music but not requested speech or SFX; intended silence needs no executor. Preserve named providers, approved voices and supplied assets in their documented roles. Reuse rights-cleared, fit-for-purpose audio instead of regenerating it; flag unusable supplied assets rather than replacing them silently.
2. Separate a cue when requested, when timing depends on a real voice track, or when independent sync, editing, reuse, or continuity requires it. Keep ordinary cues in the [native request](video-generation-planning.md#3b-voice-and-sound-design-are-in-request-by-default) when supported. If native audio is unsupported or unverified, record that and propose a separate cue if needed; do not assume permission to execute it. An indispensable cue cannot quietly become silence.
3. Classify the separate cue by purpose, not length. A door latch is SFX; a one-second harmonic brand signature is music. Select one candidate per cue using the rules below. A named external provider or locked voice/model overrides defaults; if blocked, do not choose a different one without approval.

## Early provider preflight

For actual production, probe each scoped separate cue's required operation as soon as known, before paid or dependent work. Share read-only results for the same provider/account/operation/model across cues; recheck live capability and authority before execution. Skip setup checks for design-only, mute, approved reuse, and supported native audio.

Check discovered MCP or an already configured official CLI/API for the same provider. Use an equivalent path without a new install when its operation, account, data handling and cost fit the approved scope. Check ElevenLabs TTS and SFX independently, and distinguish the Fish engine from its voice ID.

| Status | Instruction |
|---|---|
| `READY` | Required operation/model and account access confirmed. Skip all installation guidance. |
| `MISSING` | No equivalent usable path; absence established and official setup path known. For an unresolved required or provider-pinned cue, tell the user what to install or connect and link the verified instructions. |
| `CONNECT_REQUIRED` | Path exists but is unauthenticated. Ask for connection/sign-in, not reinstallation, if the cue remains blocked. |
| `CAPABILITY_UNAVAILABLE` | Path exists but operation/model/plan does not qualify. Name the missing capability, not the whole provider. |
| `UNVERIFIED` | Cannot prove availability or absence. Do not claim missing or invent an install command; offer paste-ready manual inputs if blocked. |

Select an eligible ready fallback before asking for setup of a replaceable provider. Batch only unresolved required or pinned needs in one early report. Use [setup and non-generating diagnostics](audio-provider-setup.md) for those needs; do not install, authenticate or spend to test availability. Keep independent planning moving; a setup report need not stop it.

## Specialist selection

| Role | Default candidate and handoff |
|---|---|
| Narration or character dialogue | Reuse an approved recording/voice first. For new expressive speech, shortlist Fish Audio `drama-3` → ElevenLabs TTS → Typecast. For a Typecast-established format, start with Typecast → Fish `drama-3` → ElevenLabs TTS, but only consider another voice if recasting is permitted. With an ElevenLabs-established workflow, start with its TTS; rank other eligible voices by fit, using Fish first for new acting direction. Filter by live language, pronunciation, delivery control, allowable voice, speaker count and length before using these tie-breakers. Carry exact spoken text, separate captions, pronunciation, acting/pause notes and any locked voice ID. Onscreen dialogue also requires lip-sync and continuity; cloning is not implied. |
| SFX, Foley or ambience | Propose **ElevenLabs SFX**. Describe source/action, material, perspective, onset/impact/tail, one-shot versus loop and cut anchor. Use only a verified sound-effects executor, never an ElevenLabs speech tool. If none is available, return the sound prompt and fallback choices as blocked for execution. |
| BGM, OST, character song, musical sting or loop | Propose Suno.com and read [suno-music](../../suno-music/SKILL.md). Carry emotional arc, use under speech, instrumentation or voice constraints, and locked lyrics. Keep independent cue sync in the edit plan. A sung character voice does not imply the same identity as the speaking voice. |

## Stage and authority

- At S07 (or for an explicit narrow artifact), record cue ID and scene/shot/beat IDs, source version, role, intended interval/accent, speech overlap, required/optional status, reuse/native/separate decision, selected candidate and draft inputs, rights and approval state. Use the existing cue sheet or handoff, not a new tracker. Design-only stops at drafts.
- On narration-first work, an estimated board or rough cut can proceed; final timing-dependent cuts/captions require the real approved take, listened to and measured. Work on independent tasks while voice is blocked. This is not an instruction to insert synthesis before the general storyboard stage.
- At S08 or the authorized narrow execution stage only, verify the live tool/account, exact model or default, rights, voice permissions, external inputs, estimated spend, calls and output count. Obtain or match scoped approval before submitting. No inferred spend, installation, external transfer or publication. Use the scoped [fallback decision](#fallback-decision) for any change to the approved execution path.

## Fallback decision

1. **Unknown submission:** reconcile a timeout/disconnection against job IDs or history first. Until resolved, neither retry nor try another provider. Reuse an idempotency key only if the same operation supports it and retry is authorized.
2. **Known unavailable before submission, or resolved failure:** filter the remaining candidates by locks, rights and required capabilities. A provider, voice, or model pinned by the user stays pinned. Do not substitute the default Fish model for locked `drama-3`. For a paid but rejected result, record the failed listening check and actual spend before considering another attempt. Keep accepted cues unchanged.
3. **Transfer the plan automatically** to the next eligible ready supplier. For speech, reuse the approved recording when available or correct only the faulty delivery in the locked voice. For SFX, try a rights-cleared library asset, then Foley, then supported native SFX only if an independent track is not needed; no TTS supplier as SFX substitute. For music, try cleared existing or stock music; propose omission only for optional cues. Do not substitute ElevenLabs or embedded BGM for Suno in this music policy. If nothing qualifies, keep required cues unresolved.
4. **Execute the fallback only inside an existing approval:** the recorded scope must cover this cue, provider/model or acceptable alternatives, any voice change, the external inputs, and cumulative cost and attempt limits including prior attempts. If all match, continue without asking again. Otherwise return prepared inputs and request only the missing authority. No costly audition is implied by preflight.
5. **Keep the same cue identity:** pass the cue ID, script/source version, pronunciation and acting requirements, timing intent, exclusions, previous failure and execution/spend evidence. Re-express instructions in the next provider's schema rather than copying its predecessor's tags. If the voice changes, remeasure only dependent cuts and captions after listening. Use the existing cue sheet to record the selection and reasons.

## Acceptance

Record submitted, playable, listened and adopted separately. Verify narration words, pronunciation, pacing and intelligibility; SFX sync, tail and loop seam; music arc, edit points and speech masking. Reconcile the final mix for duplicate native/independent sound. Attach measured intervals and source version/hash to the existing project record when available. Unheard or rights-unverified audio is not final. The coordinator integrates approved results; no worker opens a second ledger.

## Mix finishing

For holistic tone shaping, compression, and BGM carving on an approved take, refer to [voice mix finishing](voice-mix-finishing.md). For localized defect repair on an individual take, use [take repair](../../video-production-assets/references/take-repair.md).
