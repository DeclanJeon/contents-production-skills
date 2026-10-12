# Rofan saved craft cases (conditional reference)

Open this reference only when the brief explicitly requests a saved case or a concrete scene problem matches a cue below. Ordinary briefs keep the normal owner route. Reuse of these saved observations does not require fresh source analysis; a request to analyze a new reference still follows [25-reference-video-analysis](25-reference-video-analysis.md).

## Quick use

1. Match the scene problem and action—not only a shared prop noun—to a saved case. For evidence-only or source-access/audio questions, also match the evidence condition across the supporting-cue tables and main index; keep distinct records and locators separate. If none matches, continue with the usual owner procedure without forcing a case.
2. Read that row's bounded observation, transferable mechanism, apply/skip condition, exact owner destination, and observable QA. Keep source observation, interpretation, and new proposal distinct; source timestamps are not new timeline values. Unavailable source details stay `UNKNOWN`; counts never restore missing content.
3. For a requested timed/cut/elision handoff, use the [conditional output contract](#requested-multi-owner-handoff) below; fill only active owners' fields.
4. Adapt examples to the brief: preserve its stated actor count, starting state, posture, required props/wardrobe, and full requested duration/timeline. Example times are illustrative, not defaults: cover the entire requested interval, rebase shot-local and final times to the brief, keep cut intervals adjacent unless the brief specifies otherwise, and state any proposed hold instead of omitting unused duration or inventing new action.
5. Keep protected expression, characters, places, dialogue, styling, props, and branded assets out of the transfer unless the user supplies rights. Transfer the generic mechanism, not expression.

### Applying a saved observation

When asked to apply saved evidence, return these positive parts: **Bounded observation + locator** (name the matching saved note and its limits); **Generic mechanism** (what production principle it supports); **Mapped proposal** (apply it to the supplied brief); **Limit + observable QA** (what remains unknown and how to check the proposal). If the user asks what transfers but supplies no target scene, give fit/skip conditions and one clearly labeled hypothetical/conditional proposal tied to the mechanism—not a claim about the source or an actual target. If the user asks only about evidence or unknowns, do not force a new-scene proposal. When a prompt raises distinct source constraints from separate records, match and address each record independently; one record cannot substitute for another. If no relevant saved observation is available, say so; do not infer one from a nearby case or shared prop.

When the brief includes an apparent close/ending, ending-associated title or credits, bonus/interstitial—or specifically requests file-end verification—plan separate checks for the last decoded picture and container duration using existing [09](09-edit.md)/[21](21-generated-video-qa-retry.md) owner procedures. Without the actual output file, both are `UNKNOWN`/pending; this is a planned check, not an EOS finding. Skip this branch when no ending/file-end question is in scope.

### Requested multi-owner handoff

When the brief requests a timed handoff across owners, return only the applicable parts below, in this order:

1. **Source → proposal:** for each relevant record, return **Bounded observation + locator / Generic mechanism / Mapped proposal / Limit + observable QA**. Keep source evidence, interpretation, proposal, and unknowns distinct; when the request has no target scene, give one clearly labeled conditional/hypothetical proposal only if the user asks what transfers. Address distinct source constraints independently; do not use one record as a substitute for another.
2. **06 shot cues** (when timed phases/cues are requested): use the canonical five-column cue table; times are local to that shot.

| Local time (shot seconds) | Actor phase / contact / visibility | Camera phase | Reveal / hold | Cut-out → cut-in phase |
|---|---|---|---|---|
| | | | | |

3. **09 cut rows** (when cuts are requested): use the [09 edit template](../assets/09-edit-template.md) and return its active six-column cut table, with one row per actual cut and all six active fields: `cut_id`, `shot_id/asset_id`, numeric `final_start_s`, numeric `final_end_s`, `행동·카메라 변화 / 컷아웃→컷인 phase·state + cue time / 컷 이유`, and `reaction/settle hold final start–end s·연속성/검수 상태`. Keep start and end as separate numeric cells; do not combine ranges or omit fields.

| cut_id | shot_id/asset_id | final_start_s | final_end_s | 행동·카메라 변화 / 컷아웃→컷인 phase·state + cue time / 컷 이유 | reaction/settle hold final start–end s·연속성/검수 상태 |
|---|---|---:|---:|---|---|
| | | | | | |

4. **09 elision rows** (whenever a proposed cut or transition omits an event, action portion, or intervening state/time—even if not called “elision”): add a separate row in the exact six-column canonical elision table below. This supplements the cut table and never replaces it; cut-reason prose alone does not satisfy the elision row. Skip elision rows only when no event/action/state/time is omitted.

| cut_id | 획득 방식: 연속배속/인터벌/몽타주/의도적 생략/미확인 | 실제 경과시간·촬영 구간·간격·공백(근거 위치) | 생략 전 상태 | 생략 후 상태 | 후속 컷 유지/리셋 조건 |
|---|---|---|---|---|---|
| | | | | | |

5. **11 handoff** (when tool support is relevant): use `도구 지원 확인`=`UNKNOWN` until the selected endpoint is checked; put the planned check in `검수 실패 위치·수정 변수`.

6. **Ending/file-end QA** (only when the planned ending includes an apparent close, title/credits, bonus or interstitial, or file-end verification is requested): append two separate planned checks using existing [09](09-edit.md)/[21](21-generated-video-qa-retry.md) owner guidance: (a) inspect the last decoded picture; actual result=`UNKNOWN`/pending without the output file; (b) inspect container tail/duration; actual result=`UNKNOWN`/pending without the output file. These are planned checks, not findings. Omit this branch when no ending/file-end question is in scope.

For each final event time, calculate its owning shot's local cue as `shot_local = final_event_time − owning_cut.final_start_s`. Every shot starts at local `0` and ends at its duration. Keep final-timeline ranges in 09; do not substitute them for 06 shot-local cues.


The catalog below covers all 57 saved IDs: C01–C12, P01–P17, O01–O10, L01–L09, E01–E09. Each row is independently usable without the original media or design document. No source-body recovery is implied.

## Problem-to-case index

| ID / cue | Bounded saved observation → generic mechanism | Apply / skip | Existing owner destination → observable QA |
|---|---|---|---|
| **C01** — reveal geography before identity | `fee0`: open field, then silhouette, pair/carry pose, medium and face at recorded points ~5.005–15.382s. A reveal can progress from place to relationship to identity. | Apply when that order serves the brief; skip if the information is already clear. Cause of scale change is unknown. | [06](06-shots.md) framing/reveal; [09](09-edit.md) only for real cuts. Check each reveal adds intended information; don't infer lens/camera cause. |
| **C02** — relationship/contact needs shared frame | `7488`: bed two-shot ~0–2.7, close/reverse views follow with partner edge/window retained. Shared geography can anchor close coverage. | Apply when spatial relationship/contact matters; skip as a universal wide-first rule. | [06](06-shots.md) blocking/axis. Check both actors' relationship reads and anchors don't obscure faces. |
| **C03** — restore geography after detail | `7edd`/`9e0`/`d31`: wide/reset composition follows face, hand or object details. A reset can reorient. | Apply only when brief needs a geography reset; skip if orientation remains clear. Viewer confusion is inference, not observation. | [06](06-shots.md) shot purpose/framing; [09](09-edit.md) if boundary planned. Check the reset supplies needed geography, not redundant coverage. |
| **C04** — high/top view as spatial reset | Separate pilot `e8c1`: high/top bed wide ~35.035–37.6378. A changed viewpoint can clarify spatial relation. | Apply when elevated view serves the brief; skip otherwise. Keep this locator separate from `7edd`/`9e0`. | [06](06-shots.md) framing/POV. Check spatial information is legible; don't merge source identities. |
| **C05** — partner edge anchors reverse | `7488`/`7edf`/`d31`: partner hair/ear/shoulder edge appears in reverse views. Foreground relation can orient eyeline. | Apply when a relationship anchor helps; skip if it blocks face/eyes or isn't needed. | [06](06-shots.md) blocking/axis. Check partner direction reads without obscuring the subject. |
| **C06** — foreground frames reaction | `a600` ~834–843s: foreground shoulders frame a reaction face. Foreground can shape attention. | Apply for an intended framed reaction; skip if the edge masks expression. | [06](06-shots.md) composition. Check face and gaze remain readable. |
| **C07** — three depth planes | `c749` ~37.0667–65.1: two foreground figures and a central background figure. Layered blocking can distinguish relation/depth. | Apply when depth carries story information; skip if overlap harms clarity. Identities/status require brief evidence. | [06](06-shots.md) blocking/eyeline. Check foreground/background and sightlines separate. |
| **C08** — relative height conveys relation | `c749`: low-positioned woman rises ~29.3–30s; starting kneel/sit is unknown. `2464` ~70.07 has raised dais figures. | Apply if height relation matters; skip if it creates unsupported status or starting pose. | [06](06-shots.md) blocking/reveal; [04](04-performance.md) if acting choice needed. Check height relation reads; preserve unknown start pose. |
| **C09** — arrival with stayer attention | `a600` ~120.22–135.803: one actor stays foreground as another moves/stops in background; attention remains through stayer. | Apply for attention handoff; skip if both actors need another arrangement. | [06](06-shots.md) blocking/cue; [04](04-performance.md) for response intention. Check arrival/stop and stayer remain separately readable. |
| **C10** — partial occlusion then reveal | `81d7` partition watcher / `d31` gate face: information appears after partial concealment. Occlusion can control disclosure. | Apply only if withheld/revealed information matters; skip if it hides required action. | [06](06-shots.md) public information/end frame. Check reveal timing; concealed content remains unknown until shown. |
| **C11** — within-shot upward reveal | `2464` ~18s: garment/torso to face in same shot. Reframing can reveal identity/reaction without a cut. | Apply when reveal purpose fits; skip if a real cut is needed for information/POV. | [06](06-shots.md) camera phase/reveal. Check it's one planned shot and face is legible. |
| **C12** — origin/blur/arrival | `fee0` 607.373–607.740: clear origin, rapid blur, clear arrival; candidates are one event. Physical whip/path/lens unknown. | Apply for direction/attention handoff; skip if endpoint is unclear. Never infer several cuts from blur. | [06](06-shots.md) camera/action cue; [09](09-edit.md) only at actual edit. Check origin and arrival; technique stays unknown. |
| **P01** — approach to stop, feet cropped | `03ab` 59.6–67.6: approach, spacing narrows ~64.4, then stop; full feet/gait absent. | Apply when arrival matters; skip unneeded approach detail. Do not claim gait/plant. | [06](06-shots.md) five-column cue; [08](08-animation.md) if motion planned. Check approach/deceleration/stop distinctly; feet remain hidden/unverified. |
| **P02** — lean/rise/stand settle | `03ab` 107.5–114: lean→rise→stand hold with table/candelabra/windows as anchors. | Apply when rising/state change matters; skip if already standing. | [06](06-shots.md), [08](08-animation.md). Check start/end posture and anchor stability. |
| **P03** — threshold foot detail | `0ad` 86.6–90.8: local threshold/boarding foot detail. | Apply for a local foot-contact beat; skip claims about a whole boarding cycle. | [06](06-shots.md), [08](08-animation.md). Check only the specified contact is visible. |
| **P04** — boot pressure/imprint | `0ad` 98.4–104.8667: boot presses snow, leaving imprint. | Apply when surface contact/result matters; skip whole gait or quantified force. | [08](08-animation.md) contact; [21](21-generated-video-qa-retry.md) only for generated result. Check contact and resulting mark. |
| **P05** — partial mount-to-beside state | `fb568` 251.6667 astride→253.1 leg cross→254.3667 beside; support phase missing. | Apply as observed pose progression; skip a complete dismount claim. | [08](08-animation.md) pose/action; [06](06-shots.md) visibility. Check only stated states; missing support remains unknown. |
| **P06** — turn/lookback and paired attention | `81d7` 40–60.967: walk→turn/lookback→paired attention; lower body cropped. | Apply when lookback/attention matters; skip full gait description. | [06](06-shots.md), [08](08-animation.md). Check eyeline/response; gait remains unverified. |
| **P07** — obstacle crossing with scale reset | `f7af` 0–42.233: obstacle/foreground crossing/duck-pass; at ~37.9 cut/scale reset to wide frontal run. | Apply when obstacle/crossing helps; skip describing one continuous tracking move across the reset. | [06](06-shots.md), [09](09-edit.md). Check the cut/reset is explicit; don't infer uninterrupted gait/tracking. |
| **P08** — first touch to settled clasp | `d551` EP9 PTS samples: separation→touch→second hand→settled clasp. | Apply when first contact is required; skip force/intent/consent claims. | [06](06-shots.md) cue; [04](04-performance.md) if response directed. Check contact onset, second hand and settled state separately. |
| **P09** — near-contact anticipation | `fb568` 108.6667–114.2333: hand rises near head/hair; positive touch not established. | Apply for hesitation/proximity; skip treating proximity as touch. | [06](06-shots.md), [04](04-performance.md). Check visible gap/contact state matches proposal. |
| **P10** — already-contact opener | `fd2` 0–3.167: close pair begins in visible mouth contact; no first touch. | Apply when brief starts in contact; skip invented approach/first-touch setup. Occluded hand state may remain unknown. | [06](06-shots.md) opening state; [04](04-performance.md) if response specified. Check mouth contact remains readable; don't conflate unknown hands with unknown mouth contact. |
| **P11** — receiver response after contact | `a600` 152–154: contact then receiver response/recoil/pivot. | Apply if recipient response is a brief goal; skip inferred force/intent. | [04](04-performance.md), [06](06-shots.md). Check contact and response are distinct observable phases. |
| **P12** — maintained contact plus free-hand action | `a600` 257–263: hand contact continues while free hand gestures. | Apply when simultaneous states matter; skip if no contact persistence. | [04](04-performance.md); [08](08-animation.md) if motion detail needed. Check contact remains while free hand acts. |
| **P13** — departure leaves reaction/space | `a600` 263–270: release→exit→extended arm/empty space→remaining actor reaction; `81d7` also has isolated post-departure woman. | Apply if aftermath matters; skip if departure is not in brief. | [04](04-performance.md), [06](06-shots.md); [09](09-edit.md) for actual cut. Check empty space and remaining actor reaction are legible. |
| **P14** — held shot with micro-change | `a600` 160–177/813–834: eye/mouth/head/hand micro-changes; audio not listened to. | Apply when a hold matters; skip speech/silence claims. | [04](04-performance.md), [06](06-shots.md). Check change is readable; dialogue/audio stays `UNKNOWN`. |
| **P15** — ordered third-party/animal reactions | `a600` 190–198: reaction ladder. Mouth motion is not audio evidence; animal naturalness unverified. | Apply if reaction sequence serves brief; skip speech/naturalness inference from image alone. | [04](04-performance.md), [06](06-shots.md); [21](21-generated-video-qa-retry.md) only for actual output. Check reaction order and actual audible evidence separately. |
| **P16** — offer/look/touch/return | `3090` ~1210–1290: offer→receiver look→hand touch→shared bed return; approximate notes. | Apply if this sequence is specified; skip frame-accurate timing/first-touch claims. | [04](04-performance.md), [06](06-shots.md), [09](09-edit.md) if cut. Check each intended beat; source times remain approximate. |
| **P17** — attendant work and reposition | `03ab` 127–135.5: attendants lean in/work/withdraw/reposition beside main actor. | Apply when support work is in the brief; match its exact attendant count—plural actors in the source are not a cast requirement. | [06](06-shots.md) blocking; [09](09-edit.md) if eliding later work. Check the specified helper count, hand visibility, withdrawal, and end state. |
| **O01** — box/paper disclosure | `fee0`: box ~157.057, pair ~178.278, paper ~248.782 in a long scene; not one continuous handoff, text unreadable. | Apply staged reveal only if useful; skip implied single handoff or readable text. | [06](06-shots.md), [09](09-edit.md). Check actual ownership/cut continuity and legibility only if required. |
| **O02** — object question to held gaze | `be746` ~1.5 dark rectangle hold, ~3.3 turn, ~5.267 floor object, ~7.833 face, ~9.166 gaze. Fall/identity/causality unproven. | Apply object-question/reaction rhythm; skip claiming same object fell or caused reaction. | [06](06-shots.md), [09](09-edit.md). Check cue order; object identity/cause only if brief evidence supplies it. |
| **O03** — establish map/surface before point | `81d7` 94.167–109.8: map/table establish, point insert, response. | Apply when spatial reference aids instruction; skip unnecessary insert. | [06](06-shots.md), [09](09-edit.md). Check point and response relate to established surface. |
| **O04** — hand-to-hand prop continuity | `81d7` 129.5–143.333: paper transfer, source/destination hands. | Apply for real transfer; skip invented ownership intent. | [06](06-shots.md); [26](26-state-causality-continuity.md) if inherited state matters. Check source/destination hand, final holder, and no prop jump/fusion. |
| **O05** — contained drink action | `a600` 16.7–19.92: cup raise→mouth→lower, stable composition. | Apply if drinking conveys information; skip decorative action. | [06](06-shots.md), [08](08-animation.md). Check cup path and start/end state. |
| **O06** — food/drink insert changes rhythm | `9e0` ~130–133 pour; food ~136; inserts interrupt face repetition. | Apply if item has information/rhythm purpose; skip automatic decorative insert. | [06](06-shots.md), [09](09-edit.md). Check insert adds intended information. |
| **O07** — eye detail vs full reaction | `9e0` ~156.7 eye detail. | Apply when eye detail communicates distinct information; skip redundant close-up. | [06](06-shots.md). Check shot purpose differs from full-face reaction. |
| **O08** — preparation/result without full dressing | `03ab` 24.1–33.6 lacing/preparation→finished look/reaction; later grooming/shoes/skirt ~33.8–48.2; not continuous full dressing. | Apply only to selected preparation beats; skip continuous dressing claim. | [06](06-shots.md), [09](09-edit.md) for elision. Check before/after wardrobe state and explicit omitted interval. |
| **O09** — mirror/hem reveal | `03ab` 290.1–295.9 hem→mirror/reflection whole-gown reveal; reflection identity unknown. | Apply when mirror reveal fits; skip unanchored identity assumption. | [06](06-shots.md) blocking/end frame; [09](09-edit.md) if cut. Check actual/reflected figures readable and correspondence grounded by brief. |
| **O10** — appearance state changes between scenes | `2464` pale at ~60.06→blue gown ~70.07; `9e0` different jacket/tie ~145; dressing action not shown. | Apply appearance-state continuity; skip claims about how/when dressing happened. | [06](06-shots.md); [09](09-edit.md) elision; [26](26-state-causality-continuity.md) when state persists. Check new state and any required keep/reset. |
| **L01** — room palette across reverse | `9e0`: bright bed→warm dark dining/fire→cool courtyard; reverse continuity. | Apply room-specific palette if it informs brief; skip assigning emotion cause from color alone. | [07](07-lighting.md), [06](06-shots.md). Check reverse continuity and stated palette purpose. |
| **L02** — threshold silhouette/backlight | `d31` opening: narrow blue-gap silhouette, warm right-side source, floor reflection. | Apply threshold reveal when useful; skip physical lighting-equipment claims. | [07](07-lighting.md), [06](06-shots.md). Check silhouette/reveal readability; source hardware unknown. |
| **L03** — fixed geometry, gradual brightness/flare | `430` 65.532–76.943 framed seat/windows with progressive brightness; `d31` 2101.599/2101.683 rising gate flare, no cuts. | Apply light change over held geometry; skip cut/camera move/exposure mechanism claims. | [07](07-lighting.md), [06](06-shots.md); [09](09-edit.md) only if real boundary. Check geometry holds while brightness changes. |
| **L04** — dark/soft shape becomes clearer | `fb568` 244.5–249.533 armour→horse muzzle/pink sleeve, clearer ~246.1–246.7; rig/focus unknown. | Apply staged visibility if useful; skip focus/light mechanism claim. | [07](07-lighting.md), [06](06-shots.md). Check intended subject emerges; technique remains unknown. |
| **L05** — differential sharpness | `9e0` ~266: sharper profile, blurred woman in background. | Apply visual hierarchy; skip asserting rack focus. | [07](07-lighting.md), [06](06-shots.md). Check intended subject is legible; no focus-pull claim without evidence. |
| **L06** — gesture/glow/object trajectory/impact/witness | `a600` 70.17–85.719: gesture/glow, cup separation, travel, impact/break, man/wolf response; candidates 15–28 one within-shot event. | Apply if VFX chain is in brief; skip physical-magic proof or splitting effect phases into cuts. | [06](06-shots.md), [09](09-edit.md) only for actual edit; [11](11-ai-handoff.md) support `UNKNOWN` until endpoint check; [21](21-generated-video-qa-retry.md) for real result. Check separation/path/count/persistence/witness. |
| **L07** — impact then object/witness response | `a600` ~779–784: leg/table contact, dishes/linens shift, woman mouth/hands react. | Apply impact-result sequence if useful; skip force/physics cause claims. | [06](06-shots.md), [08](08-animation.md), [21](21-generated-video-qa-retry.md) only for actual output. Check contact, object response and witness separately. |
| **L08** — paired human/animal contact | `a600` 87.421–95.796: hands/cheeks or muzzle paired contact, head turn. | Apply when contact/response matters; skip unverified anatomical/force naturalness. | [08](08-animation.md), [21](21-generated-video-qa-retry.md) for actual result. Check visible contact boundary and response; actual naturalness needs media QA. |
| **L09** — overlay over continuing scene | `d31` ~2025: ghost-figure overlay while campfire continues. | Apply as separate information layer; skip treating overlay as a new shot or proven chronology. | [06](06-shots.md), [09](09-edit.md). Check underlying shot continuity and overlay boundary separately. |
| **E01** — departure/dark transition/new place | `3090` ~1020–1050 rainy rear-wide carry/recede→near-black→bright palace/title. | Apply for actual time/place compression; skip claiming continuous travel. | [09](09-edit.md), [06](06-shots.md). Check the destination is established and elapsed travel remains unasserted. |
| **E02** — ceremony contact to pair departure | `f7af` 42.233–71.9667: faces/officiant→hands meet→rear aisle pair. | Apply if contact then shared departure suits brief; skip full gait inference. | [06](06-shots.md), [09](09-edit.md). Check contact and final pair relation; no unsupported gait. |
| **E03** — environment motif montage | `b355` 265.557–289.246 sunset pair→hand→meltwater→shoot→garden→animated title. | Apply motif-based compression if brief needs it; skip literal elapsed-time or relationship recap assertion. | [09](09-edit.md), [06](06-shots.md). Check montage conveys intended transition; chronology remains unspecified. |
| **E04** — explicit narrative timecard | `fb568`: card states “3개월 전”. | Apply explicit story-time label when required; skip treating card as proof of physical elapsed time. | [09](09-edit.md). Check card text, timing and actual transition are distinct. |
| **E05** — title over live image | `7edf` ~2.5, `c749` 18–21.033, `a600` 803–813: titles over underlying images; candidate frames can be one overlay. | Apply layered graphics; skip automatic cut count. | [09](09-edit.md), [06](06-shots.md). Check graphic layer and underlying shot are recorded separately. |
| **E06** — apparent ending vs bonus/true ending | `7488`: apparent title, bonus label ~339s, table scene ~342.767, later black/star ending; other locators are partial. | Apply when distinguishing interstitial/EOS; skip inferring whole-work structure from excerpt. | [09](09-edit.md); [21](21-generated-video-qa-retry.md) only for actual file. Check actual last picture and any bonus section. |
| **E07** — picture end vs container tail | `81d7` black 168.4–170.766, container 170.852426; `a600` last visible PTS 843.042, container 843.093. | Apply only when checking actual file ending; skip inferring final picture from duration metadata. | [21](21-generated-video-qa-retry.md), [09](09-edit.md). Check decoded last picture and container end separately. |
| **E08** — blur/flare/motion is not an edit | `fee0` whip blur, `d31` flare, `a600` cup motion: not evidence of multiple cuts. | Apply actual edit boundaries only; skip splitting effect phases into cuts. | [09](09-edit.md), [06](06-shots.md). Check cut against actual boundary, not visual detector candidates. |
| **E09** — same-place angle coverage | `d31` ~2094.843 restrained three/gate frontal→profile, same place. | Apply angle coverage without claiming location/time change. | [06](06-shots.md), [09](09-edit.md) if actual cut. Check location anchors persist across angle. |

## Additional supporting cues

These four locator-backed notes add distinct applications beyond the 57-case index. They preserve saved evidence without implying fresh source review or reconstructing unavailable bodies.

| Cue | Bounded observation → transferable mechanism | Apply / skip | Existing owner → actionable QA |
|---|---|---|---|
| **Rise with an insert and later state** — `0ad-seat-rise-insert-to-standing-state` | `0ad` PTS 201.067708 (3088384): a wide shows rise beginning; shoe insert appears around 212.934; a standing state follows. This is not a continuous full rise cycle. An insert can punctuate a larger action while the later state remains distinct. | Apply when an insert adds a needed local detail to a larger action; skip if it would obscure sequence or if the brief requires continuous proof of the whole rise. | [06](06-shots.md) cue/reveal and [09](09-edit.md) only for actual cuts. Check the insert's relation to the action and the later standing state; do not claim unseen transition/footwork. |
| **Caption cue to attention and geography** — `be746-text-report-to-bedroom-attention` | `be746`: corridor caption ~64.6, pair attention ~66.4, wide ~77.534, door insert ~81.467. Caption visibility is not listened speech evidence and does not identify who operates the door. A visible text cue may connect attention and spatial reorientation. | Apply when the brief uses a visible information cue followed by attention/geography; skip speech, door action, or caption claims the brief does not support. | [06](06-shots.md) public information/blocking, [09](09-edit.md) for actual cut/layer, [10](10-evidence.md) only if a factual caption claim is made. Check caption readability and attention sequence separately; actor/speech/door operator stay unknown. |
| **Wide-to-OTS is one edit** — `7edf-wide-to-ots-is-one-edit-not-two` | `7edf`: wide ~15.5 → OTS ~15.542 → same OTS ~15.584. The adjacent OTS samples are one held OTS state: one wide-to-OTS edit, not two cuts. Sample granularity is not an edit boundary. | Apply when assessing adjacent sampled frames or a similar edit proposal; skip cut creation from repeated frames within the same composition. | [09](09-edit.md), with [06](06-shots.md) axis/anchor if needed. Count one actual wide-to-OTS boundary and verify the OTS remains the same shot state. |
| **Excerpt-only / incomplete or inaccessible source body → title/live-image transition** — `797-opening-title-to-live-bed` | `797`: illustrated opening title at about `0s`, then live bed image at about `0.2s`; only the opening excerpt is recoverable. The transferable mechanism is a title-to-live-image information transition, not evidence about later content. | Apply when a new brief needs this opening distinction; skip inferring subsequent events or whole-work structure. | [06](06-shots.md) if timing/blocking is needed; [09](09-edit.md) only for an actual transition/cut. Check the proposed title-to-live transition is legible; later content remains unknown. |

## Worked proposals using existing owner fields

All times in these four examples are **new illustrative proposals**, not measurements of source footage or generated results. Cue `Local time (shot seconds)` is shot-local; `final_start_s` and `final_end_s` are separate final-timeline values. The exact 06 cue columns and 09 field names below are canonical. Work/reveal labels W1/W2 are document-local labels only, not production IDs. These are text/2D shot plans; no numeric 3D spatial design is implied.

### 1. Already-established mouth-contact opener

**Use when:** the new brief starts with an already-established kiss/contact. Saved `fd2` observation: close pair is already in visible mouth contact at 0–3.167s. This is not a first-touch event. Hands may be occluded; their contact state is unknown. The proposal is a new design, not a claim about the source's cause, force, intent, or consent.

**Shot:** local 0–2s; final timeline 12.0–14.0s.

| Local time (shot seconds) | Actor phase / contact / visibility | Camera phase | Reveal / hold | Cut-out → cut-in phase |
|---|---|---|---|---|
| 0.0 | Already in visible mouth contact; hands may be out of frame, hand-contact state unknown. | Steady two-person composition. | Reveal established mouth contact. | N/A; shot-in already in contact. |
| 1.0 | Contact maintained; optional receiver gaze shift only if brief specifies. | Hold same axis/framing. | Hold response without changing contact type. | N/A; no cut planned. |
| 2.0 | End in same visible mouth-contact state; occluded hands remain unknown. | End frame holds pair. | Endpoint hold. | N/A. |

| Existing field | Proposed value |
|---|---|
| 06 `인물 블로킹` / `시선/축` / `공개 정보` / `관점·감정/구도 의도` | Two actors stay in shared frame on established axis; information is already-established mouth contact, not first touch. |
| 09 `행동·카메라 변화 / 컷아웃→컷인 phase·state + cue time / 컷 이유` | Continuous hold of existing contact; out/in=N/A (no cut); reason=N/A. |
| 09 `final_start_s` | `12.0` (shot-local `0.0`). |
| 09 `final_end_s` | `14.0` (shot-local `2.0`). |
| 09 `reaction/settle hold final start–end s·연속성/검수 상태` | Proposed hold `13.0–14.0s`; verify mouth contact visibility and pair continuity in actual output; not generated/verified. |
| QA expectation (not pass evidence) | Check visible mouth contact, partner/axis anchor and no unintended hand/face fusion. Unknown hand contact does not negate visible mouth contact. |

### 2. Arrival, stop, settle, then stayer response

**Use when:** approach/arrival and the remaining actor's attention both matter. `03ab` records approach, narrowing spacing (~64.4), then stop; it does not record a stayer response. The response below is a new proposal informed by `a600`. Feet are cropped; gait/foot plant stay unverified.

**Shot:** local 0–3s; final timeline 24.0–27.0s.

| Local time (shot seconds) | Actor phase / contact / visibility | Camera phase | Reveal / hold | Cut-out → cut-in phase |
|---|---|---|---|---|
| 0.0–1.0 | Arriving actor approaches; feet cropped, foot plant unverified. Stayer holds position. | Shared two-person frame at room anchor. | Approach begins. | N/A. |
| 1.0–1.2 | Arriving actor decelerates; stayer remains. | Hold; no tracking inferred. | Deceleration before stop. | N/A. |
| 1.2–1.3 | Arriving actor stops; stayer remains. | Hold. | Stop becomes legible. | N/A. |
| 1.3–1.5 | Arriving actor settles at mark; stayer remains. | Preserve both actors and anchor. | Arrival settle. | N/A. |
| 1.8–2.0 | Arriving actor stays settled; stayer begins gaze response. | Maintain shared composition. | Reaction onset, not yet hold. | N/A. |
| 2.0–3.0 | Arriving actor stays settled; stayer holds gaze/reaction. | Maintain shared composition. | Separate stayer reaction hold. | N/A; no cut planned. |

| Existing field | Proposed value |
|---|---|
| 06 `크기/카메라 위치` / `인물 블로킹` / `시선/축` / `공개 정보` | Medium-wide shared frame at a room anchor; arrival frame-left toward table; stayer frame-right; reveal arrival, then stayer attention. |
| 09 `행동·카메라 변화 / 컷아웃→컷인 phase·state + cue time / 컷 이유` | Approach (0.0–1.0)→decelerate (1.0–1.2)→stop (1.2–1.3)→settle (1.3–1.5); stayer response starts 1.8; out/in=N/A, reason=N/A. |
| 09 `final_start_s` | `24.0` (shot-local `0.0`). |
| 09 `final_end_s` | `27.0` (shot-local `3.0`). |
| 09 `reaction/settle hold final start–end s·연속성/검수 상태` | Arrival settle `25.3–25.5s`; response onset `25.8s`; stayer hold `26.0–27.0s`; verify readability and shared timebase after generation. |
| QA expectation (not pass evidence) | Check distinct phases, stayer visibility, spatial anchor and axis; do not claim gait/foot plant from cropped feet. The proposed reaction is not source observation. |

### 3. Attendant work, wardrobe elision, mirror reveal

**Use when:** work and finished appearance should be shown without pretending omitted dressing is continuous. Saved observations are partial preparation/lacing (`03ab`) and appearance changes (`2464`/`9e0`); they do not establish complete dressing, elapsed story time, or mirror identity. The saved source notes multiple attendants, but this illustration uses one helper to match a brief that specifies one. Always preserve the active brief's exact cast count, seated posture, required wardrobe/prop state, and overall duration; W1/W2 times below are illustrative and must be rebased to the requested timeline.

**Two adjacent-shot example:** W1 local 0–2s / final 40.0–42.0s; W2 local 0–2s / final 42.0–44.0s. These canonical illustration values are not project defaults. Both output shots are adjacent; story-time elapsed and capture gap are `UNKNOWN`.

| Local time (shot seconds) | Actor phase / contact / visibility | Camera phase | Reveal / hold | Cut-out → cut-in phase |
|---|---|---|---|---|
| W1 0.0–1.0 | One attendant works at the specified shoulder; hands visible only where framed. Main actor seated. | Medium two-person composition; keep actor/helper readable. | Work in progress. | Cut out after work; next shot begins after intentional elision. |
| W1 1.0–2.0 | The one attendant withdraws/repositions; main actor stays seated. | Hold shared frame. | Work shot settles. | Out=attendant withdrawn, actor seated; in=actor seated before mirror in finished wardrobe. |
| W2 0.0–1.0 | Actor remains seated; hem enters foreground; reflection begins. | Reframe only as brief specifies. | Reveal hem/reflection; reflection identity unknown unless anchored. | Cut-in=finished wardrobe, seated. |
| W2 1.0–2.0 | Actor remains seated and regards mirror. | Hold mirror and actor in readable relation. | Finished look/reaction. | Cut-out=seated finished look; next state preserves or explicitly changes posture. |

| Existing field | Proposed value |
|---|---|
| 06 `인물 블로킹` / `종료 프레임` / `공개 정보` | W1: actor seated; the single specified attendant assists then withdraws. W2: same actor remains seated at mirror in brief-approved wardrobe; preserve the required mirror/wardrobe state. |

| cut_id | final_start_s | final_end_s | 행동·카메라 변화 / 컷아웃→컷인 phase·state + cue time / 컷 이유 | reaction/settle hold final start–end s·연속성/검수 상태 |
|---|---:|---:|---|---|
| W1 | 40.0 | 42.0 | Work/withdrawal; out at 42.0=attendant withdrawn, actor seated; reason=omit unshown preparation. | N/A; no reaction hold in work shot. |
| W2 | 42.0 | 44.0 | Mirror/hem reveal; in at 42.0=same actor seated, finished wardrobe; reason=disclose finished look after intentional elision. | Proposed hold `43.0–44.0s`; verify wardrobe, seated posture, mirror relation/reflection continuity and no unintended identity duplication; not generated/verified. |

**09 intentional-elision fields (canonical six columns):**

| cut_id | 획득 방식: 연속배속/인터벌/몽타주/의도적 생략/미확인 | 실제 경과시간·촬영 구간·간격·공백(근거 위치) | 생략 전 상태 | 생략 후 상태 | 후속 컷 유지/리셋 조건 |
|---|---|---|---|---|---|
| W1→W2 (document-local label) | 의도적 생략 | Story-time elapsed=`UNKNOWN`; capture gap=`UNKNOWN / not measured`; outputs adjacent at final 42.0s. Locator: `03ab` preparation/mirror, `2464`/`9e0` appearance state. | Main actor seated; single attendant withdrawn; work/appearance state as the brief specifies. | Same actor seated at mirror in the brief-required finished wardrobe. | Preserve actor identity, seated posture, required wardrobe and prop ownership; explicitly state any change. |


**QA expectation (not pass evidence):** check actor and reflection readability, ground reflection identity in the new brief, check attendant/hand separation and wardrobe persistence. W1/W2 are document labels only, not production cut IDs.

### 4. Continuous magic-object event and witness response

**Use when:** brief calls for a single readable effect chain. Saved `a600` notes gesture/glow, cup separation, travel, impact/fragments, and witness response; candidate frames 15–28 are one within-shot event. The mechanism below is a design proposal, not proof of physical magic, material behavior, or endpoint support.

**Shot:** local 0–3s; final timeline 70.0–73.0s; one continuous proposed shot.

| Local time (shot seconds) | Actor phase / contact / visibility | Camera phase | Reveal / hold | Cut-out → cut-in phase |
|---|---|---|---|---|
| 0.0–0.5 | Actor gestures; cup held; finger/cup separation visible. | Locked three-quarter framing; trajectory lane visible. | Gesture. | N/A. |
| 0.5–1.0 | Glow appears; cup remains held. | Hold. | Glow reveal. | N/A. |
| 1.0–1.5 | Cup separates; hand remains visible; track cup identity/count. | No unmotivated pan. | Separation. | N/A. |
| 1.5–2.0 | Cup travels past stated landmarks toward impact. | Keep origin/path/destination legible. | Trajectory. | N/A. |
| 2.0–2.5 | Impact/fragments; witness begins response. | Maintain geography. | Result. | N/A. |
| 2.5–3.0 | Fragments settle; witness reaction held. | Hold end composition. | Settle/reaction. | N/A; same shot ends after hold. |

| Existing field | Proposed value |
|---|---|
| 06 `크기/카메라 위치` / `카메라 동작` / `종료 프레임` | Locked three-quarter view; no camera move; end frame keeps fragments and witness in same geography. |
| 06 `핸들` | Proposed 0.25s pre-roll and 0.5s post-roll around the 3.0s action; not a model guarantee. |
| 11 `도구 지원 확인` | `UNKNOWN` until selected endpoint is checked. This field belongs to 11, not 06. |
| 09 `행동·카메라 변화 / 컷아웃→컷인 phase·state + cue time / 컷 이유` | Continuous gesture→glow→separation→trajectory→impact→fragments/witness; no inferred cuts; out/in=N/A; reason=N/A. |
| 09 `final_start_s` | `70.0` (shot-local `0.0`). |
| 09 `final_end_s` | `73.0` (shot-local `3.0`). |
| 09 `reaction/settle hold final start–end s·연속성/검수 상태` | Proposed hold `72.5–73.0s`; verify count, trajectory, impact result, persistence and witness response in actual output; not generated/verified. |
| QA expectation (not pass evidence) | Check cup separation/count, continuous path, impact/fragments persistence, witness readability and spatial continuity. Effect phases alone do not establish cuts; endpoint support remains unknown until checked. |

**Transfer variation: continuous object effects and separate fixed-geometry light changes.** Match by the action problem, not the prop noun. When the brief has a continuous object-VFX chain with distinct phases and a cut-boundary question, L06 can supply only the bounded phase-not-cut lesson; its source-specific path, impact, fragments, witness and cause do not transfer. New movement is a proposal. For a separately specified flare over held geometry, L03 can inform the light-change plan; do not infer focus pull or cut. O05 applies to a cup raise→drink→lower beat, not unrelated cup action. Rebase shot-local and final times to the active brief; the `0–3s` / `70–73s` values above are illustrative only.

## Evidence and source limits

These are bounded observations from saved historical analysis, not fresh playback or frame-level reinspection. Source prefixes are optional provenance locators, not full identities or proof of title, lens, rig, or technique. Recovered material is incomplete: D797 has only an opening excerpt recoverable; D8fba's complete event body and the fde1 dynamic ledger body are inaccessible; C9e26 and Db834 bodies are unrecovered. These are access/recovery limits, not evidence of absence or deletion. Do not reconstruct hidden content from counts. `P14` audio was not listened to: speech and silence are both unknown. `C03` viewer-lost-geography is an interpretation, not observed viewer state.

Recorded correction anchors: `430` is 65.532–76.943s; `L05` is about 266s, not 266.7; `P07` includes a wide frontal reset at ~37.9s; `E06` apparent title is followed by bonus label ~339s and table scene ~342.767s before the later actual ending. Preserve those scopes; all source times remain saved-note locators rather than newly measured frames.

## Common mistakes

- Converting one partial/local observation into a complete action cycle (cropped gait, partial dismount, partial dressing).
- Treating overlay, blur, flare, or effect phases as edit cuts.
- Treating changed sharpness as proven rack focus or brightness change as a camera move.
- Treating unseen information, unlistened audio, unavailable source bodies, or endpoint capability as absent/known.
- Writing a new proposal as if it were source observation or actual QA.
- Copying protected expression instead of transferring a generic mechanism.
- Turning a conditional case into a universal shot, timing, contact, or genre rule.
