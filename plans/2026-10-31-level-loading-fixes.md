# Level loading fixes and the level toolbar dropdown

Size: M    Tier: 3 (touches `LevelBase.cs`, core list), approved by THJ 2026-10-31 ("Fix them all. 1 your way by playing it through the sandbox mission")    Assigned to: `miso-implementer` → `miso-reviewer` → THJ play check
Branch: `thj/onboarding`. Status: **in progress**

Found during the grid-to-level C3 play check. All three are older than this branch (the quick-load flow is the SEN-2103 commit `50558f9e1`).

## 1. Inspector Load Level on a level no mission lists

`LevelBase.ID` is a non-serialized property that only `Mission` sets (`SetID`). For an unwired level it is null, and `LevelBase.UnpackID` calls `id.Split` on it: NullReferenceException from `GameDataSO.IsLevelIncluded` (`LevelBase.cs:110`).

Fix:
- `UnpackID` returns false on a null or empty id (no throw).
- The inspector **Load Level** button: when the level is in no mission, play it in a sandbox mission (the toolbar's path, `requireIncluded: false`) instead of the "not included" dialog. A level that a mission lists but that is misconfigured keeps the dialog. Keep the change small, in `EditorLevelLoader`.

## 2. Toolbar Play on an unwired level opens the game from the start

`LevelMainToolbar.OnLoadClicked` → `EditorLevelLoader.LoadLevel(level, requireIncluded: false)` → `EnterPlay` stores the prefab path, written to EditorPrefs on `ExitingEditMode`. `ProgramFlowHandler.Start` reads it and should run `FastForwardLoad` → `LevelFastForwardRoster.TryResolve` → `Mission.CreateSandbox`. THJ instead gets the main menu, so at `Start` both keys are empty (or the flow fails earlier). Cause unknown from reading.

Do: reproduce in THJ's open editor with `GB_24-nook` (temporary log lines are fine, remove them after), find the cause, fix it. Candidates to check: the `playModeStateChanged` handler not firing or firing twice, the prefs being cleared (`Teardown`, `Discard`) before `Start`, `_pendingPrefabPath` empty when the toolbar passes a prefab asset (`AssetDatabase.GetAssetPath` on a component of a prefab asset), Prefab Mode being open when Play starts. The grid window's **Play** (`GridToLevelWindow.cs:338`) uses the same path and must work too.

## 3. Level toolbar dropdown

`LevelMainToolbar.ShowLevelDropdown` lists every level prefab flat. Change, editor-only, in `LevelMainToolbar.cs` (or a new partial/helper beside it):
- Levels as submenus by their folder under `Content/Levels` (GenericMenu `"A/B/Item"` paths).
- **Favourites** at the top, then **Recent** (last 5 loaded or opened from the toolbar, newest first), then a separator, then the folder tree.
- A toggle item "★ Favourite <current level>" / "Remove <current level> from favourites".
- Favourites and recents in EditorPrefs (per machine), stored as asset paths; drop entries whose prefab no longer exists.
- The selected level stays checked wherever it appears.

## Tests

Edit-mode tests for the logic: `UnpackID` with null/empty/valid ids; the menu-path and recent-list helpers (folder path from asset path, recent list order, cap at 5, de-duplication, missing entries dropped). Keep the helpers pure static so they test without the toolbar. Run the EditMode suite: all green except `AIRegressionTest.Baseline_MatchesCurrentAI`.

## Gates

Review / EditMode / THJ plays `GB_24-nook` from the toolbar, from the inspector Load Level and from the grid window, and tries the dropdown. Commits after his play check: the core fix (`LevelBase.cs` and any flow fix) on its own, then the dropdown.
