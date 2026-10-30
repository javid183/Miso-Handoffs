# Review: onboarding structure C1

Reviewer: `miso-reviewer` (read-only; saved by the coordinator), 2026-10-30. Branch `thj/onboarding`.

**Verdict: FIX.** Data, scene and graph work correct. One must-fix (commit grouping), two should-fix.

## Must fix

1. **Proposed commits 2 and 3 only work together.** Commit 2 alone removes M1, old M2, M3 Wolf and M5 from the graph while the Home scene's map buttons still point at them (no pins, flow dead-ends after the Hearth), and moves Mark's unlock to the Hearth while his select button and upgrade tab (scene) still wait on M3 Mark Intro. Fix: one commit = `Game Data.asset`, `Unit_Mark.prefab`, `IntroScreen.unity`, `MainMenuScene.unity`, `Home - Scene.unity`, flagged risky. Commits 1 (mission assets + metas) and 4 (tests) stay.

## Should fix

1. `OnboardingMissionGraphTests.cs:59-64`: `Hearth_IsTheOnlyOpenMissionOnAFreshSave` checks only River, Ridge, Trail, M4. Loop over every mission in `_data.Missions` and assert all but the Hearth are locked (guards against an edge-less node, incl. the M8–M14 branch behind an input-less gate).
2. The Ridge placeholder level `LevelE3-C1` has 3 `Unit_Placeholder` slots for 2 fixed heroes; `FillRosterSlots` leaves the third visible on a cell. Use a 2-slot level, or say so in the play check.

## Answers

1. **Remove vs unlink:** removal is right. `SerializableDependencyGraph.IsEntityUnlocked` returns true for a node with no previous nodes. New graph: 15 nodes; the Hearth is the only entity with no incoming edge and is `isInitialLevel`; the new gate is AND (River, Ridge → Trail); Trail → M4. Dead branch stays behind the input-less gate (false). Nothing throws: leftover references (`HomeInteractables`, `HomeState.requiredMissions`, the Family tab, old `WorldMapPanel.prefab` buttons) only read `.Completed`, which stays false. Parking old missions behind the input-less gate would bring back level-ID clashes (Level1, `LevelLucyJohn-C1` shared).
2. **Hearth roster John+Lucy+Linda:** no extra spawns (no placeholders in the Level1 prefabs). The FTP pool now includes Linda's FP in every memory level (old M1 was John+Lucy): fine for the greybox, C2 fills FTP. Mark in segment 4 must be in the Hearth roster to count toward the pool, the character panel and run upgrades: decide in C3.
3. **IntroScreen / MainMenuScene:** one line each, M1 → Hearth; no noise.
4. **Mark's button and upgrade tab:** targets verified (CharacterSelectorPanel "Mark" button, `UpgradesPanel.characters[3]`). Map buttons: `MapButton` → Hearth, `John Linda` → River, `1-1` → Ridge, `Lucy John` → Trail; M6, M7, M3 Mark Intro pins deactivated. Scene diff is only the intended edits.
5. **Tests:** meaningful (real assets, AND gate both ways), right folder/namespace, no private IDs, LF. Gap: should-fix 1.
6. **Save keys:** unique, no clashes. Old saves read as a new campaign but keep faction XP, skills, equipment: reset the save for the check.

## Notes

- Editor tools that read the graph (`AllLevels`, Quick Level Loader, the level prefab's `LoadLevel` button, dialogue export, dev `LevelSelectUI`) no longer see the removed missions' levels.
- The Hearth pin stays visible after completion (replayable), as M1 did.
- Pin labels show `missionNumber`: Hearth "0", Trail "3".
- Five Home stations, the Family tab and M4 HomeState idles stay locked until C5.
- No core code, no statics, no AI impact. File list matches the diff; LF kept.
- `thj/home-test` will conflict on `Game Data.asset` and the Home scene at merge.
