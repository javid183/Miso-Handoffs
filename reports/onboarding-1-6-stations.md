# Report: Onboarding 1.6 (X-24): stat-upgrade stations unlock after The Trail

Plan: plans/2026-11-22-onboarding-demo.md (chunk 1.6, part X-24)    Agent: implementer    Branch: thj/onboarding-demo
Outcome: done

## What changed

- `miso/Assets/_Project/Features/Onboarding/Editor/OnboardingOpeningSetup.Stations.cs`: Bookshelf, Training Field and Cooking Cabinet rows now use `Trail` instead of `Rootwell`; added a plain-words comment above the rows.
- `miso/Assets/_Project/Features/Onboarding/Editor/HomeVisitsTests.cs`: station test renamed to `OtherStationsOpenAfterTheTrail` and expects `M2 - The Trail`; the scene-copy repair test expects "station 'Bookshelf' unlocks after The Trail".
- `miso/Assets/_Project/Features/Home - Imported/___Khashayar/Home - Scene.unity`: the three stations' `UnlockAfterMissions` now point at The Trail (guid 9901650e...) instead of M4 (a45e197c...).

## Acceptance criteria

- [x] Three stations unlock after The Trail: dry run listed exactly the three changes; apply ran `RunHomeSceneOnly(ProjectTargets(), apply: true)` (via MCP `execute_code`, reflection on the internal method; the menu runs the whole setup, not only the Home step); a second check said "already applied". Read back from the scene: all three show `UnlockAfterMissions=[M2 - The Trail]`.
- [x] Scene diff only station lock changes: `git diff --stat`: 1 file, 3 insertions, 3 deletions (the three guid lines). The apply also re-serialized one extra line, `forceDefaultModeAlways: 0` on `HomeStateManager` (code default is `false`, so no behaviour change). I deleted that line from the YAML so the diff is only the station locks; the scene was never loaded as the active/dirty scene (only PreloadScreen was loaded, not dirty, before and after). Nothing else was unsaved. Note: opening the scene for a Unity re-save will add that line again; harmless.
- [x] Do the stations work once unlocked (read from code, scene and data; no Play session, no save reset):
  - Wiring works on paper: Home scene has `PointerDown` events calling `HomeManager.ShowFamilyRoomStatUpgrades`, `ShowTrainingGroundStatUpgrades` and `ShowKitchenStatUpgrades` (scene lines about 2409, 5581, 6746); each opens a `FactionStatUpgradePanelUI` (`FamilyStatUpgradePanel` 3 rows, `KitchenUpgradePanel` 3 rows, `TrainingGroundUpgradePanel` 4 rows), all assigned in `HomeManager`. The events sit on child objects of the stations, not on the `HomeInteractables` object itself; I did not check which station maps to which panel by name.
  - Data exists on this branch: the ten rows (Stat_FP, FPG, FPP, HP, HPG, HPP, DMG, DR, CRC, EVA) all have an entry in `Resources/Factions/BergsonsFaction.asset`, each with 4 upgrade levels paid in `MainResource_Gold`. The panel reads `GameHandler.GameData.PlayerFaction`; nothing there was modified by this task.
  - Not verified: a real click in Play. The first suspect for "don't open / no feedback" (X-24) was the lock: before this change the stations stayed locked until after M4, with no feedback. Whether a locked click gives feedback was not looked at. Panel behaviour once open (Gold shown, upgrade applied, X-31) is untouched and untested here.
- [x] Tests: `HomeVisitsTests` and `OnboardingOpeningSetupTests` (full class names under `MISO.Core.Features.Onboarding.EditorTests`) via MCP: 43 run, 43 passed, 0 failed. Full suite not run (S task). The run did not change the scene diff (re-checked after).

## Chunks

### Chunk 1: stations after The Trail

- Changed: files above.
- Criteria met: see above.
- Decisions and loose ends: see below.

## Save reset

no

## Decisions I made

- Applied the Home step through `RunHomeSceneOnly` by reflection, because the menu items run the whole setup (mission graph included).
- Removed the single re-serialized `forceDefaultModeAlways: 0` line by hand to keep the scene diff to the three locks.

## Needs THJ

none

## Docs to update

- `design/demo-spec.md` / status: the stat-upgrade stations open after The Trail (was after M4), if the spec names M4. Also the stale comment in `OnboardingOpeningSetup.cs` line 11 mentions Rootwell in a general sense; left alone.

## Risks and loose ends

- Mission names: the mission asset for The Trail is "M2 - The Trail"; "M3" in the brief means the third mission slot. Tests assert the asset name.
- A Play check of the three clicks (with The Trail done) is still outstanding; panels are X-31.
- Working tree has other uncommitted changes from other chunks and THJ; not touched.

## Proposed commits

1. `tweak(onboarding): open the Bookshelf, Training Field and Cooking Cabinet after The Trail`: `miso/Assets/_Project/Features/Onboarding/Editor/OnboardingOpeningSetup.Stations.cs`, `miso/Assets/_Project/Features/Onboarding/Editor/HomeVisitsTests.cs`, `miso/Assets/_Project/Features/Home - Imported/___Khashayar/Home - Scene.unity` (plain; the scene belongs with the builder change)

## Other branches

none

## How to see it

1. Run Tools > Onboarding > Check Opening Setup: "nothing to change" for the Home scene.
2. Open the Home scene, select Bookshelf, Training Field, Cooking Cabinet: Unlock After Missions shows "M2 - The Trail".
3. With a save that has The Trail done, click each station in Play: its stat panel should open.
