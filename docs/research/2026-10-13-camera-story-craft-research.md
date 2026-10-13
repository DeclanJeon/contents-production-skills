# Primary-source research memo: camera and story craft for short-form video

**Research date:** 2026-10-13  
**Scope:** reusable craft relevant to romance/fantasy short-form video: shot size, angle and lens; camera movement; blocking and eyelines; actor-camera timing; cut/coverage; visual storytelling and reveals; screen direction and continuity; story techniques.  
**Boundary:** This memo is not an analysis of Rofan footage. No user video content was accessed or copied. Sources support general craft and generation-prompt guidance, not claims about any particular footage or genre’s universal conventions.

## Primary-source evidence

### OpenAI: archived Sora 2 Prompting Guide

[OpenAI, “Sora 2: Prompting Guide”](https://developers.openai.com/cookbook/examples/sora/sora2_prompting_guide) — the page identifies itself as an **archived recipe that may reference outdated models or APIs**. It says it was updated March 2026, but that date does not make its API instructions current after archiving. Use it as first-party documentation of prompting guidance, not as assurance of present endpoint behavior.

- Under **“Before you prompt,”** it frames prompting as briefing a cinematographer who has not seen the storyboard. It says specificity about a shot’s purpose helps direct consistency, while leaving details open can enable variation. It explicitly describes prompts as creative guidance rather than contracts and warns that repeated generations vary.
- Under **“Prompt anatomy that works,”** it recommends describing a shot like a storyboard: framing, depth of field, action beats, lighting and palette. It says that when several shots are included, keep each shot block distinct: “one camera setup, one subject action, and one lighting recipe at a time.” This is vendor guidance for the named generation system, not a universal filmmaking law.
- Under **“Camera direction and framing,”** it offers aesthetic heuristics: wide/high framing can emphasize space and context; a close-up at eye level can focus attention on emotion; shallow focus can separate a subject from the background, while deep focus retains foreground and background sharpness. These are choices whose effect depends on the image and scene, not deterministic technical facts.
- Under **“Control motion and timing,”** it advises keeping motion simple, with one clear camera move and one clear subject action per shot, and describing actions in beats/counts, including pauses. Its example contrasts “Actor walks across the room” with a countable sequence of steps, pause, and curtain pull in the final second. Treat this as model-oriented prompt guidance; actual timing and performance still require inspection.
- Under **“API Parameters,”** it distinguishes prose-controlled content from API parameters such as model, size, duration, and character references, which must be set through the API rather than requested in prose. This is a technical statement about that documented API, with currentness caveat due to archival status.
- Under **“Iterate with video edits,”** it recommends controlled, one-at-a-time changes and simplifying a misfiring shot before adding complexity. This is a useful experimental method, not a guarantee that an edit preserves all unchanged properties.

### BFI: continuity craft and the 180-degree convention

[BFI, David Parkinson, “Where to begin with G.W. Pabst,” 29 April 2019](https://www.bfi.org.uk/features/where-begin-gw-pabst). In **“Why this might not seem so easy,”** the article describes Pabst’s development of continuity editing: “Pabst refined cutting on movement to produce smooth transitions, while pioneering motivated point-of-view shots such as the eyeline match, as well as the shot-reverse-shot method of constructing a conversation.” It also describes directing actors for the camera as a component of this work. This is historical/critical interpretation of Pabst’s filmmaking and craft, not a technical production standard.

[BFI / Sight and Sound, Thom Andersen, “Ozu Yasujirô: the master of time,” updated 13 November 2019](https://www.bfi.org.uk/sight-and-sound/ozu-yasujiro-master-time). The essay explains the conventional continuity rule: “A fundamental rule of standard continuity requires that the camera always stay on one side of an axis created by the actors’ gazes.” It then discusses Ozu’s systematic crossing of that axis, showing that screen-direction continuity is a legibility convention that a filmmaker may deliberately break—not a physical law. The article is an interpretive essay, not a standards document.

### ASC: leads for camera-led reveals and lens/story choices

- [American Cinematographer, “Lighting The Day of the Jackal”](https://staging.ascmag.com/articles/lighting-the-day-of-the-jackal) was surfaced in search as a cinematographer breakdown of a moving opening shot, with framing and movement used to reveal clues and stage a body reveal. A direct page read failed with HTTP 522 during this research, so the description is search-result-level and **not treated as verified close-reading or quoted evidence**.
- [American Cinematographer, “Visual Analysis: Contact (1997)”](https://staging.ascmag.com/articles/visual-analysis-contact-1997) was surfaced as a first-party visual-analysis lead discussing wide-angle lens choice and a moving composition shifting attention among characters. It was not successfully read here; treat this as a source lead only, not as an evidentiary quotation.

These ASC links are first-party cinematography-publication sources, but because their text was unavailable for direct inspection in this research session, no actionable claim below depends on their unverified details.

## Generalized craft recommendations

These recommendations synthesize the evidence above with common narrative-design practice; they are **craft judgments**, not official rules or proven genre formulas.

- **Motivate shot size, angle, and lens by audience attention.** Decide what information and emotion a frame should carry; choose wide/medium/close and viewpoint accordingly. For romance, a shared frame can establish spatial and relational proximity; a tighter reaction frame may make a changed response legible. Do not prescribe close-ups as a romance requirement.
- **Stage gaze and blocking so relationship beats read.** Establish who looks at whom and at what; preserve the intended eyeline across coverage. Let a glance, withheld response, or movement toward/away from another character complete its beat before cutting when that pause carries meaning. These are optional timing choices, not fixed durations.
- **Design fantasy reveals as information release.** State what is concealed, which visual or behavioral cue comes first, when movement/focus/framing exposes the information, and what reaction makes its significance readable. Use a cut, occlusion, focus shift, or camera move only when it supports that intended discovery. The sources do not establish a universal reveal formula.
- **Keep shot action temporally legible.** In short clips, a simple sequence—readable initial state, one salient action or gaze shift, pause/reaction/reveal, ending state—gives a viewer and a video model a coherent beat path. Avoid stacking unrelated camera moves and actor actions in one shot unless the complexity is intentional and the result remains readable.
- **Treat coverage and cutting as information/POV choices.** A wide/master, singles, reverse, reaction, or insert should each contribute information or emotional perspective. Use shot/reverse-shot and cutting on movement when they clarify interaction; a continuous shot can contain several phases only if the camera can actually see the relevant actions and reactions. Respect screen direction for clarity, or deliberately break it with a legible reorientation or purposeful disjunction.
- **Separate aesthetic intent from technical control.** Prompt language can describe a desired lens, movement, or timing, but it does not prove that a generator supports or will obey that direction. Check the specific endpoint’s documented parameters and inspect generated footage before claiming continuity or performance fidelity.

## Repo-local skill coverage and gap assessment

This is a targeted read of the named references and skill summaries, not a complete audit of every story skill.

- `video-production-assets/references/06-shots.md` already covers blocking, character positions and movement, gaze/action axes and 180-degree continuity, shot purpose and new information, coverage selection, movement motivation/start/end, reaction/POV phase separation, panel legibility, and shot-to-edit handoff. It explicitly delegates numerical camera position, lens, angle, framing, and path design to `camera-spatial-design`.
- `video-production-assets/references/09-edit.md` already covers emotionally/informationally motivated cuts, rhythm and reaction placement, reveal/hiding information, action-phase continuity across cuts, and temporal/editorial constraints.
- `camera-motion-reference-analysis` owns analysis of supplied reference footage: observed motion vs inferred cause, camera vs subject motion, timing, and evidence status. It is not the general authoring owner for new scene/story design.
- `camera-spatial-design` owns camera position/angle, lens/framing, blocking and motivated paths, spatial staging, axis checks, and movement timing. It is not a replacement for narrative beat or performance design.
- Existing coverage is therefore substantial for the requested generic camera/cut/continuity craft. A romance/fantasy application can be expressed as a use case within existing shot/storyboard/story workflows; this research does **not establish a clearly absent skill owner**, and does not recommend creating a new general camera/story skill.
- `storyboarding-video` and story-structure-related skills were not opened during this research, so their detailed overlap is **unverified**. The no-gap conclusion is limited to the explicitly inspected coverage above; it means no clear absent owner was identified, not that every conceivable story technique is exhaustively covered.

## Evidence limits

The BFI articles are film-history/critical sources; their observations support craft interpretation, not technical requirements. The OpenAI source is first-party but archived and vendor-specific. The ASC URLs are reputable first-party leads but could not be directly inspected in this research, so their discovered descriptions are not relied on as verified findings. None of these materials is evidence about Rofan footage or about copying any user video.