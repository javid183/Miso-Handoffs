# B4 Phase 1 · Family Role barks

Narrative agent, 2026-10-18, branch `thj/oct-build-fixes`. Read-only on `miso\`. Inputs: `plans/2026-10-18-family-role-readability-design.md` (Creative, UX table, Q7), `reports/b4-family-role-facts.md`, the GDD character pages, and THJ's direction that a decline is a choice, not a failure (no "too slow").

All lines are **Tier 2** (new UI text in an established voice). Max 4 words; each sits over the role unit's head for about 1.2 s. Toba is excluded (D-048).

## Current values (prefab overrides)

| Unit | Field (prefab line) | Current | Problem |
| --- | --- | --- | --- |
| John | `unitFamilyRolePromptText` (`Unit_John.prefab` l.379) | `No!` | None |
| John | `unitFamilyRoleExecuteText` (l.383) | `I got you!` | None |
| Linda | `unitFamilyRolePromptText` (`Unit_Linda.prefab` l.372) | `Get them Linda!` | Spoken *to* Linda. The bark plays at the role unit, so Linda would be calling her own name |
| Linda | `unitFamilyRoleExecuteText` (l.376) | `'Have them on my sight! '` | Wrong idiom ("in my sights") and a trailing space |
| Lucy | `unitFamilyRolePromptText` (`Unit_Lucy.prefab` l.455) | `All yours Lucy!` | Spoken to Lucy, same problem as Linda; also missing the comma before "Lucy" |
| Lucy | `unitFamilyRoleExecuteText` (l.459) | `My turn!` | Identical to Mark's line, so the two characters sound the same |
| Mark | `unitFamilyRolePromptText` (`Unit_Mark.prefab` l.273) | `All yours Mark!` | Spoken to Mark; copied from Lucy (like his `LucyQTE` binding) |
| Mark | `unitFamilyRoleExecuteText` (l.277) | `My turn!` | Identical to Lucy's |

(`UnitBase.prefab` and `Lucy_Decoy.prefab` have both fields empty; leave them.)

## Proposed lines

When each plays:
- **Prompt** plays when the QTE appears, before the player decides, so it must read well whether or not they press.
- **Execute** plays with the insert panel when the role fires.
- **Decline** plays when the player lets the prompt pass.

| Unit | Prompt → `unitFamilyRolePromptText` | Execute → `unitFamilyRoleExecuteText` | Decline 1 (first time) | Decline 2 (later times) | Feel |
| --- | --- | --- | --- | --- | --- |
| **John** | `No!` (keep) | `I got you!` (keep) | `Hold fast.` | `Hang in there.` | The father. A decline is still him speaking to the one taking the hit: encouragement, not apology |
| **Linda** | `In my sights.` | `Clean shot.` | `Not this one.` | `I'll wait.` | Calm, precise archer. Letting a target walk is her own call |
| **Lucy** | `Leave some for me!` | `Catch this!` | `Next time!` | `Saving it.` | The cheeky youngest fighter, all spark. The decline is upbeat, never sulky |
| **Mark** | `Not my family.` | `Breathe. Strike.` | `Patience.` | `Another moment.` | The monk. Quiet resolve on the prompt, his discipline on the strike, stillness on a decline |

Checks:
- No decline blames the player or mentions speed.
- Each one is complete on its own, so turning declines off (the planned setting) loses nothing the player needs.
- No line names a mechanic, so they still hold when FTP becomes per-round uses (D-036/D-042).

## Notes for the implementer

- **Prompt and execute**: paste into the existing fields on each `Unit_<Name>.prefab` (the override lines listed above). John's are unchanged.
- **Decline needs a new field.** Nothing exists for it today. Suggested: `unitFamilyRoleDeclineTexts` as a `string[]` on `GUnit`, next to the other two (`GUnit.cs` l.149-150), or on the handler if the TD prefers. The code is yours to add.
  - Order: element 0 = Decline 1, element 1 = Decline 2.
  - Play element 0 the first time in a fight, then element 1 for later declines (or alternate).
  - The decline setting turns all of them off; when it's off, play nothing in their place.
- Barks go through `FactionRoleVisual.ShowWithDialogue` / the over-head bark, as the design plan says.
- **The design plan is out of date here.** The `Missed` row ("Too slow...") and the Creative "counter-moment" ("John mutters 'Too slow...'") still describe a miss as a failure. THJ's direction replaces that with the decline lines above; the coordinator should update the plan.
- Glossary: no new terms. Nothing to add unless THJ wants these lines recorded.
