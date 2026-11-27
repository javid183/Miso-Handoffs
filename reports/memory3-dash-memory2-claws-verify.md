# Verify: Memory 3 Shield Dash on turn 2, Memory 2 Claw fade fix (+ Memory 3 role suppression)

Plans: `plans/2026-11-27-memory3-dash-memory2-claws.md`, `plans/2026-11-27-memory3-john-only-role.md`
Implementer report: `reports/memory3-dash-memory2-claws.md`
Agent: miso-verifier (quiet checks only, Unity MCP, THJ's open editor). Date: 2026-11-27.

- **Result:** PARTIAL. Every quiet check passes; the in-game criteria are not run (no play session; THJ plays afterwards).
- **Compile:** clean. `refresh_unity` (force, compile requested), then waited until the editor was idle. Console: 0 errors. The warnings are the "Serialization depth limit 10 exceeded" warnings that were already there, plus one MCP WebSocket warning. `Library/ScriptAssemblies/Assembly-CSharp(.dll, -Editor.dll)` were written at 14:03:01–02, after the newest source edit (`HearthMemoryWiring.John.cs` 14:02:19), and no `.cs` under `Assets/_Project` is newer. The only `error CS` lines in `Editor.log` are old ones (lines ~2874–2939 of 29298: `LevelFamilyRoleSuppressionTests.cs(27,..) ActionFlowEvent`). Later compiles in the same session succeeded.
- **Tests:** full EditMode suite (Unity MCP `run_tests`, job `8f0c299d…`): **3079 total, 3078 passed, 0 failed, 1 skipped** (`MISO.Core.Systems.AI.EditorTests.AIRegressionTest.Baseline_MatchesCurrentAI`, Skipped:Explicit), 146 s, resultState Passed. There were no failures, so nothing was rerun. The AI baseline was not run by name because no AI graph, AI ability or unit prefab logic is in scope. `Unit_John.prefab` changed, but only in THJ's Shield factor, as the coordinator noted.

## Acceptance criteria

### Memory 3 role suppression (earlier plan)
- Component, zone hiding, release on disable/level end, no statics: **Pass (by tests)**. `LevelFamilyRoleSuppressionTests` runs in the green full suite.
- Wiring lists Linda and Lucy only: **Pass (by tests)**. `HearthMemoryJohnTests` is in the green suite.
- No IDs in code: **Pass**. No `D-`/`H-`-style IDs in the added lines of `Features/Onboarding` or in the new files (grep).
- Only John's role works in play: **Not run: needs a play session**.

### A. Memory 3 Shield Dash
- `TurnStartAbilityUnlock` unlocks only at the given faction and turn, once, only listed presets: **Pass**. `TurnStartAbilityUnlockTests` is in the green suite.
- Wiring: lock entry, unlock at turn 2, two hints matched by preset: **Pass**. `HearthMemoryJohnTests.ShieldDashIsLockedForJohnUntilTheSecondTurnAndPulsesWhenItOpens` and `TheShieldUpButtonPulsesOnTheFirstTurn` are in the green suite.
- Claw positions follow THJ's layout: **Pass**. `TheClawsAreOnTheBoardFromTheStartAndFirstTurnPointsAreLimited` is in the green suite.
- Prefab diff limited to the planned changes: not re-checked by me. The implementer's diff against the pre-run copy is in that report.
- Shield Dash hidden on turn 1, appears and pulses on turn 2: **Not run: needs a play session**.

### B. Memory 2 Claws
- Tile constants and fade keep tiles, 12 hidden Claws inactive, camera point recomputed: **Pass (by tests)**. `HearthMemoryLucyTests` (incl. `TwelveCuedClawsAreHiddenInTwoGroupsOnTheirTiles`, which checks they are inactive, and `TheInterruptionBringsInTenFadesEightAndBringsInTwoBetweenTheLines`) is in the green suite.
- Four Claws after "Two." / "Four." in play: **Not run: needs a play session**.

### C. `HiddenLevelUnits.cs` editor guard
- **Pass (by reading).** The only `UnityEditor` use in the file is `UnityEditor.Selection.objects` at line 49. It sits inside `SelectInEditor` (with its `[Button]`), wrapped by `#if UNITY_EDITOR` (line 40) … `#endif` (line 51). The file has no `using UnityEditor;`. `ToggleVisibleInEditor` stays outside the guard and uses only runtime API. No other runtime (non-`Editor/`) file in `Features/Onboarding` references `UnityEditor`. Line endings: `git ls-files --eol` gives `i/lf w/lf`, the file has 0 CR bytes, and it is LF as git stores it. No player build was made.

## Files changed by the runs

None. `git status --short -- miso/Assets/_Project` was identical before and after (9 modified, 10 untracked, as in the coordinator's list). The md5 of every modified/untracked file under `miso/Assets/_Project` was also identical before and after. Snapshots are in the scratchpad: `status-before.txt`, `status-after.txt`, `hash-before.txt`, `hash-after.txt`.

## Bugs found

None.

- **Branch:** main
- **Save reset:** no
- **Editor state:** Play mode never entered. The active scene stayed `Scenes/PreloadScreen.unity` (not dirty).

## Editor checks corrections

- Confirmed: Editor log at `C:\Users\Dead Mage\AppData\Local\Unity\Editor\Editor.log` on this device.
- Confirmed: `refresh_unity` with `compile: request` returns while still `compiling`. A second `refresh_unity` (`mode: if_dirty`, `wait_for_ready: true`) waits until the editor is idle, so it can stand in for polling `mcpforunity://editor/state` when no resource-read tool is loaded.
- Suite size on `main` today: 3079 EditMode tests, 146 s through the MCP. `get_test_job` with `wait_timeout: 300` returned the full result in one call, without dropping.
