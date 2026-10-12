# Unrelated-brief baseline and with-skill comparison

## Run metadata

- **Exact user prompt, both arms:** “Plan an 8-second text-only 2D scene of an adult baker placing three rolls on a cooling rack, wiping flour from their hands, and smiling at a customer. Give a concise shot outline and practical continuity QA. No additional constraints or referenced footage supplied.” Each arm was required to return the actual plan in at most 350 words.
- **Model:** `openai-codex/gpt-6-luna:medium` in both arms.
- **Baseline package:** frozen installed package at `C:/Users/Declan/AppData/Local/Temp/rofan-craft-final-stable-55mbkjjk/skills`.
- **With-skill package:** current working-tree package `video-production-assets/`.
- **Run records:** `history://ordinary-brief-baseline` and `history://ordinary-brief-with-skill`.
- **Baseline paths consulted:**
  - `video-production-assets/SKILL.md`
  - `video-production-assets/references/contract.md`
  - `video-production-assets/references/06-shots.md`
  - `video-production-assets/references/08-animation.md`
  - `video-production-assets/references/12-qa.md`
- **With-skill paths consulted:**
  - `video-production-assets/SKILL.md`
  - `video-production-assets/references/contract.md`
  - `video-production-assets/references/06-shots.md`
  - `video-production-assets/references/08-animation.md`
  - `video-production-assets/references/09-edit.md`
- Neither run consulted a casebank. The with-skill run did not consult module 25 or create/use the archive crosswalk; it correctly kept the unrelated brief on the regular production route.

## Complete actual baseline plan (verbatim)

**8-second 2D scene — text-only shot outline**

| Time | Shot and action |
|---|---|
| 0:00–0:02 | Medium-wide, steady view of the bakery counter. The adult baker stands behind it, cooling rack centered on the counter; a customer waits opposite. The baker places three rolls on the rack, one after another, with each hand-to-roll contact visible. |
| 0:02–0:04 | Hold the same composition. The baker withdraws both hands, then wipes flour from them with a small towel beside the rack. Keep all three rolls visible and undisturbed. |
| 0:04–0:06 | The baker finishes wiping, lowers the towel, and shifts their gaze from the rack to the customer. |
| 0:06–0:08 | The baker smiles at the customer. Hold the shared eyeline and readable smile through the end. |

**Practical continuity QA**
- Keep the baker, customer, counter, and rack positions consistent; preserve screen direction and eyelines.
- Track the three rolls: show each placement, then keep their count, spacing, and positions unchanged.
- Keep the towel available at the baker’s side; show the hands release the rolls before wiping, and lower the towel before the smile.
- Make flour visibly present before wiping and reduced afterward; avoid sudden changes to clothing, hands, or props.
- Ensure the placing, wiping, and smile read clearly in silhouette and within the short timing. Check that the smile is directed toward the customer.
- This is a text plan only; timing, pose readability, and continuity remain unverified in animation.

**Package paths consulted**
- `video-production-assets/SKILL.md`
- `video-production-assets/references/contract.md`
- `video-production-assets/references/06-shots.md`
- `video-production-assets/references/08-animation.md`
- `video-production-assets/references/12-qa.md`

## Complete actual with-skill plan (verbatim)

### 8-second text-only 2D scene — shot outline

*One continuous shot; proposed timing, not measured footage.* A warm, simple bakery interior. Keep the baker, counter, cooling rack, three rolls, towel, and customer clearly readable in the same composition. The customer waits across the counter.

- **0–3 s:** Baker places the three rolls on the cooling rack, one at a time. Make each hand-to-roll contact and each roll’s resting position clear.
- **3–5 s:** Baker withdraws both hands and wipes flour from them with a towel. Keep the rack and all three rolls visible and undisturbed.
- **5–8 s:** Baker looks up toward the customer and smiles; hold the shared eyeline and smile briefly to land the friendly beat.

### Practical continuity QA

- Confirm exactly three rolls are placed, remain on the rack, and do not shift or multiply between actions.
- Track each hand through placement, withdrawal, and wiping; avoid unexplained position jumps or towel swaps.
- Keep flour visible before the wipe and reduced afterward; preserve the towel’s hand and position.
- Maintain baker/customer positions, eyeline direction, rack placement, and screen direction throughout.
- Check that hand-to-roll contact, the wiping action, and the final smile read clearly in silhouette and at small display size.
- This is a text plan only; no frames or animation have been rendered or visually checked.

**Package paths consulted:** `video-production-assets/SKILL.md`; `video-production-assets/references/contract.md`; `video-production-assets/references/06-shots.md`; `video-production-assets/references/08-animation.md`; `video-production-assets/references/09-edit.md`.

## Manual comparison

Both plans honor the brief’s 8-second duration, adult baker, three-roll placement, flour wiping, customer smile, 2D text-only nature, concise shot outline, and practical continuity QA. Neither adds any Rofan story, character, setting, choreography, or timing content; neither consulted a casebank. The current with-skill arm correctly does not route this unrelated prompt to reference-video module 25 or require/create the archive crosswalk.

This is one sample per arm. The comparison is descriptive only; it is not causal evidence, a statistical estimate, or a general performance claim.
