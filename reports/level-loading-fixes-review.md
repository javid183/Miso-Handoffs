# Review: level loading fixes and toolbar dropdown

Reviewer: `miso-reviewer` (read-only; saved by the coordinator), 2026-10-31. Plan: `plans/2026-10-31-level-loading-fixes.md`. Report: `reports/level-loading-fixes.md`.

**Verdict: FIX**

Root cause confirmed: the old `EnterPlay` read `GetAssetPath(level)`, `level.ID` and `GetCurrentPrefabStage()` after `OpenScene`, by which time the prefab-asset reference was unloaded and Prefab Mode closed. The fix captures them first; it covers the toolbar, the inspector button, `GridToLevelWindow.cs:338` and the deferred `LevelPlaceholderAssignWindow` path. Reset hook wired. Line endings clean (i/lf w/lf, no CR, no BOM, 47+/12-). No private IDs.

## Must fix

1. `LevelBase.cs:158-173`: a wired level opened in Prefab Mode gets the "not included" dialog. The stage copy's `ID` is null (only the assets get `AssignLevelIDs`). Fix: when `GetAssetPath(level)` is empty and a prefab stage is open, swap in the stage asset's `LevelBase` before reading the ID, `IsLevelIncluded` and `OpenIfNeeded`.

## Should fix

1. `LevelBase.cs:159-176`: a level with no prefab path (scene object, prefab instance in a scene) silently goes to the main menu. Try `PrefabUtility.GetPrefabAssetPathOfNearestInstanceRoot`, else a dialog and return.
2. `LevelMainToolbar.Menu.cs:15-29`: missing prefabs are hidden but never pruned from EditorPrefs; dead entries eat the 5 recent slots. Prune before `PushRecent` or save the pruned lists.
3. `LevelMainToolbar.cs:83`, `.Menu.cs:93-98`: folder tree in file-name order; sort by `LevelToolbarMenu.MenuPath`.
4. `.Menu.cs:64,71`: same file name in two folders → identical favourite/recent labels; use `MenuPath` on collision.
5. Commit grouping: split dropdown tests into `LevelToolbarMenuTests.cs` (commit 2); keep `UnpackID`/`ResolvePrefabPath` tests in `LevelLoadingTests.cs` (commit 1).
6. `LevelLoadingTests.cs:4`: namespace `MISO.Core.Levels.CEditor.EditorTests` vs neighbour `MISO.Core.Levels.EditorTests`.

## Notes

- `TextMesh Pro/.../LiberationSans SDF - Fallback.asset` modified (TMP dynamic atlas during play runs): don't stage.
- Recent as a `Recent/` submenu: THJ's call at the play check.
- `IsListedInAnyMission` reads `gData.Missions`; `FindOwner` reads `GameHandler.Instance.AllMissions`; could diverge.
- Pre-existing quirk left alone: `IsLevelIncluded` compares against the open stage root, so Load Level on a wired asset while a different prefab is open still shows the dialog.
- Play check should cover: a wired level from the inspector, the same from Prefab Mode, a listed-but-misconfigured level, a level with placeholders, an unlisted level (toolbar, inspector, grid window).

## Fix round re-check (2026-10-31): APPROVE

Must-fix and all six should-fixes done correctly, no new issues; LF, no BOM, no private IDs, metas present. Commits compile on their own in order (1: `LevelBase.cs`, `PlayModeStaticReset.cs`, `LevelLoadingTests.cs`; 2: toolbar files + `LevelToolbarMenuTests.cs`).

Notes:
- The one main-menu run after a play-stop: a scripted `LoadLevel` during the previous run's `EnteredEditMode` delivery lets the old handler unsubscribe the new run's handler, so no prefs are written at `ExitingEditMode`. Same pattern before this change; hand clicks almost never hit it. Hardening (follow-up): write the two prefs directly in `EnterPlay` before `isPlaying = true`.
- The placeholder window now reads the saved asset, so unsaved Prefab Mode placeholder edits don't show in it (matches what plays).
- Edge: two same-name prefabs both at the levels root (or both outside it) still share a label. Not worth a fix.
