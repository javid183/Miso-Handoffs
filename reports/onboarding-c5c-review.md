# Review: onboarding C5c (guided skill spend)

Reviewer: `miso-reviewer` (read-only; saved by the coordinator) · 2026-11-03 · Branch `thj/onboarding`

**Verdict: FIX**

## Must fix
1. `AbilityTreePanelUI.Highlight.cs:48-55`: start level re-captured when `RefreshTreePanel()` rebuilds the buttons after a purchase, so the `> _highlightStartLevel` stop rule (line 61) never fires; the pulse never stops. Capture once per `HighlightNode` call.
2. Same file line 72: `OnDisable` stops the pulse but keeps `_highlightGuid`, so every later open pulses again (breaks "later opens behave as now"). Clear it on disable; add a lifecycle EditMode test (stops on a level rise across a rebuild; cleared on disable).

## Should fix
1. `GuidedSkillSpend.cs:62`: tracker check (SO create/destroy + Register) runs on every open before the cheap checks; check missions first.
2. `Highlight.cs:41`: `FindIndex` lambda allocates every frame while highlighted; look up on tree change or loop by hand.

## Notes
- Existing panel behaviour unchanged when not guided (only `partial` keyword in old files; Update/OnDisable no-ops).
- Once per save via `PlayedSequencesTracker` (keyed by name, `List<string>`): no save shape change, no new statics, marker SO destroyed in `finally`.
- Fires only on the Grandma Table open after River and Ridge. If The Trail is played before the table is opened, last-completed is the Trail and the guide never shows (matches plan wording; tell THJ).
- Skill points: XP thresholds start at 0, first XP gain grants 1 SP (`FactionTracker.cs:416-438`); River/Ridge give 30 XP split among participants. Very likely ≥1 SP; play check confirms. Node level-1 SP cost not verified.
- Tests scoped (scratch scene, scoped log ignore); conventions OK; commit split sound.
