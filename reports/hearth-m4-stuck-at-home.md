# Stuck at Home after Hearth Memory 4 (investigation, 2026-11-11; nothing changed)

## What the log shows (`%LOCALAPPDATA%/Unity/Editor/Editor.log`, THJ's run on `main`)
`Memory4Mark_End_SequentialSequence` starts → warning `TransitionToNextLevel has no next level to load.` (`HomeMemoryTransition.cs:148`, from `TransitionScene.cs:34`) → the sequence ends → nothing else: no mission end, no scene load. Then only key presses.

## Cause
- Memory 4's end step list (teammate, origin/main) is: input off → camera → mother falls → **fade grid** → mother dialogue → walks → **TransitionToHome** → cub dialogue → cutaway → **TransitionToNextLevel** → keep grid hidden.
- Memory 4 is the **last level of the Hearth mission**, so `TransitionToNextLevel` finds no next level, logs the warning and returns. The Home view that `TransitionToHome` put up stays on screen.
- `CombatLevelRunHandler.EndLevel` (`:768`) then queues the normal mission-complete panel (`EndMission(true)` on its button), because `IsChangingLevel` is false. That panel doesn't appear above the Home view. Most likely the full-screen transition overlay (`sortingOrder -1`) covers the HUD canvas. That last link isn't confirmed by play: a quick look at the hierarchy while stuck would settle it.

## Teammate's or the merge?
The teammate's. Evidence:
- `main`'s Memory 4 end step list is byte-for-byte origin/main's. `thj/after-hearth` never touched that asset: its version equals the base `e9bd6e885`.
- `MissionEndPanelUI.cs` is identical on both sides.
- Neither side changed the Hearth mission's level list.

Expected to reproduce on origin/main alone (not run).

## Fix options (THJ's call; the code is the teammate's, Core/ProgramFlow)
- **a.** `TransitionToNextLevel` with no next level and the mission complete hands over to `GameHandler.EndMission(true)` from the Home view, with no panel. This is a seamless end to the Hearth at Home. A small code change in `HomeMemoryTransition`.
- **b.** Memory 4's end drops `TransitionToNextLevel` (data), and the mission-complete panel is drawn above the transition overlay. That puts a panel back at the end of the Hearth.
- **c.** Ask the teammate, since it's their flow.
