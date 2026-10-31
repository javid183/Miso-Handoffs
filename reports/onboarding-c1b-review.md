# Review: onboarding C1b (merge-safety builder)

Reviewer: `miso-reviewer` (read-only; saved by the coordinator), 2026-10-31. Branch `thj/onboarding`.

**Verdict: FIX** (approve once must-fix 1 is done). Checked against `thj/home-test`'s files: graph (home-test only adds 8 edge-less sortie nodes), pins (`WorldMapPanel.prefab` unchanged there; old-mission pins found by mission), Mark's select button and `UpgradesPanel` `characters[3]` (found by `Mark_DialogueCharacter`); the serialized field names the builder reads are the same.

## Must fix

1. `OnboardingOpeningSetup.cs:221` `AssetDatabase.SaveAssets()` saves every dirty asset in the project. Delete it; each step already saves its own target.

## Should fix

1. Preflight (`.Scenes.cs:24-37`) checks only target scenes: also abort Apply if `Game Data.asset` is dirty in memory, or `Unit_Mark.prefab` is open in Prefab Mode with unsaved changes.
2. `EditScene` (`.Scenes.cs:48-69`): a target scene in THJ's Hierarchy but unloaded gets removed from the Hierarchy on close. Track "in Hierarchy" separately from "loaded"; close with `removeScene: false` in that case.
3. `CloneNode` (`.Graph.cs:61-75`) copies `NodeData` fields by hand; a field added later on another branch would be reset. Deep-copy generically (re-point `payload`) or add a reflection test.
4. Initial flag (`.Graph.cs:145-149`): clear `isInitialLevel` on every other entity node and report it (`GetEntry` takes the first).
5. Removals (`.Graph.cs:80-123`): warn for any surviving entity node that lost its incoming edges and now has none (would open from the start).
6. Test `ApplyOnTheGraph_ReplacesTheOldOpening` (`Tests.cs:127-140`): assert the old gate is gone and the River/Ridge AND gate has exactly those inputs and outputs to the Trail.

## Notes

1. home-test adds **8** sortie nodes, not 4 (GoblinCamp, OldWatchtower, MossyHollow, DrownedShrine, DeevBurrow, GoblinQueensWarren, GoblinScoutPost, ShamansCircle), none with edges; all kept.
2. home-test sets `UpgradesPanel` `characters[5].requiredMissionToUnlock` (Family tab) to null; onboarding still has M3 Wolf. C5 should expect null on the merged scene.
3. home-test's `WorldMapPanelUI.RefreshHomeMode` hides every pin when a `HomeDayRunner` is present and shows clones bound to the Home sim's missions (prologue: `PrologueMapMission`). On the merged branch the restored pins only show outside Home mode: part of the "which opening wins" question.
4. Apply saves an open, clean target scene in place when it changes something.
5. Scene/pin/recruit/prefab steps have no unit tests; on another file version they are covered only by the one-off proof. Read the first real merge run's report lines.
6. Fine: editor-only, namespace, LF/no BOM, metas, no statics, no private IDs, files match the report, no core change, no AI impact. One commit is right.
