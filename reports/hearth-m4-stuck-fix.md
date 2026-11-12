# Report: Hearth Memory 4 no longer leaves the game stuck at Home

Plan: coordinator brief (bug fix, size S; THJ decision D-528; investigation `reports/hearth-m4-stuck-at-home.md`)    Agent: miso-implementer    Branch: main
Outcome: done (code and EditMode tests). The in-game check is THJ's play.

## What changed

- `miso/Assets/_Project/Core/ProgramFlow/Runtime/HomeMemoryTransition.cs` (LF, no BOM, kept): `TransitionToNextLevel` now chooses one of three steps through a new pure `ResolveNextStep(nextLevelLoadable, hasNextLevel, currentLevelCompleted)`:
  - next level loadable: unchanged (`IsChangingLevel = true`, `ChangeLevel`).
  - no next level and the current level is in `MissionTracker.CompletedLevelNames`: sets `IsChangingLevel = true` (so `CombatLevelRunHandler.EndLevel` skips its panel) and starts `EndMissionFromHome`. That coroutine waits exactly like `ChangeLevel` (the sequence player stops playing and `IsEndingLevel` turns false), runs `TransitionToHome()` (a no-op when Home is already up, as it is in Memory 4), freezes the mission timer (`Stats.EndMission()`), then calls `GameHandler.Instance.EndMission(true)`.
  - anything else (not completed, a next level missing from GameData, no tracker or GameHandler): the same warning as before.
  - `ChangeLevel` is untouched. I left its wait loop in place rather than sharing a helper, so its frame timing can't shift.
- `miso/Assets/_Project/Core/ProgramFlow/Editor/HomeMemoryTransitionTests.cs` (+ `.meta`, new): 4 tests on `ResolveNextStep`.
- `miso/Assets/_Project/Core/ProgramFlow/Editor.meta` (new folder meta).

## Acceptance criteria

- [x] No next level and the mission complete: ends the mission from Home with `EndMission(true)`, no panel. Covered by `NoNextLevel_CurrentLevelCompleted_EndsMission` (decision). The coroutine and the scene flow need THJ's play.
- [x] Warning kept for the real misconfiguration. Tests `NoNextLevel_CurrentLevelNotCompleted_ReportsSetupError` and `NextLevelMissingFromGameData_ReportsSetupError`.
- [x] Normal next-level path unchanged. Test `LoadableNextLevel_LoadsIt`. The code path is the same as before.
- [x] "Mission complete" is detected the way `EndLevel` sees it. `EndLevel` calls `MarkCurrentLevelCompleted()` before `PlayOutro()`. Memory 4's end sequence is the outro of `GB_m4-mark.prefab` (`outroSequence`), so the current level is already completed when `TransitionToNextLevel` runs. `GetNextLevel` false is the same test `EndLevel` uses (`HasNextLevel()`) to choose `MissionComplete`.
- [x] Nothing is awarded twice or skipped. Checked by reading the code. `EndLevel` awards `AwardMissionCompletionResources()` and raises `levelEnded(MissionComplete)` before the panel check at ~768, whatever `IsChangingLevel` says. Our coroutine waits until `EndLevel` has finished (`IsEndingLevel` false), so `EndMission(true)` runs after both, once. The panel path did only two things: `MissionTracker.Stats.EndMission()`, which freezes the mission timer for the panel's readout (now called by us too), and `EndMission(true)` from its button. `_uiManager.DeInitialize` still runs in `EndLevel`.
- [x] The persistent controller isn't left stuck. `EndMission(true)` → `SaveLoadManager.Save` → `ProgramFlowHandler.GoHome()` → `LoadScene` → `HandleSceneLoading(showLoadingScreen: true)`, which calls `HomeMemoryTransition.Instance.HideForSceneLoad()` first. That existing reset clears `IsChangingLevel`, `IsHomeVisible`, `_animating` and `_revealing`, disables the overlay and sets its progress to 0, puts the home copy back to inactive, and `StopAllCoroutines()` ends our coroutine (`EndMission` is its last statement). This is the same path the panel button took. Needs THJ's play to confirm on screen.
- [x] No new statics.
- [x] Compiles: console shows no errors (only the existing CS0108/CS0618/CS0414 and serialization-depth warnings). EditMode: 1897 tests, 1896 pass. The only failure is the known `AIRegressionTest.Baseline_MatchesCurrentAI`. The 4 new tests pass (also run on their own).

## Save reset

No.

## Decisions I made

- I also call `MissionTracker.Instance.Stats.EndMission()` before `EndMission(true)`, to match the skipped panel's only side effect (freezing the mission timer). Same behavior as the panel path. Tier 1.
- `EndMissionFromHome` runs `TransitionToHome()` before ending, like `ChangeLevel` does. It's a no-op in Memory 4. In a sequence without a home step, Home fades in before the loading screen instead of cutting straight to it. Tier 1.
- `ResolveNextStep` and its `NextStep` enum are `public`: tests compile into `Assembly-CSharp-Editor` and there is no `InternalsVisibleTo`. Tier 1.

## Needs THJ

None.

## Docs to update

- `tech/home-system.md` or `tech/combat-architecture.md` (wherever the memory transition is described): `TransitionToNextLevel` on a mission's last completed level ends the mission from Home with no panel. A missing next level before that still only warns.

## Risks and loose ends

- `HomeMemoryTransition` is the teammate's code (Core/ProgramFlow). The change is limited to the no-next-level branch. `MissionTracker` and `GameHandler` are used only through their public API.
- If `EndLevel` ever stopped awarding before the panel check, this path would lose the awards. Today the order is fixed in `EndLevel`.
- In a fast-forward sandbox run, `EndMission(true)` stops Play mode, as the panel button did.

## Proposed commits

1. `fix(home-memory): a transition to the next level on a mission's completed last level ends the mission from the home view instead of leaving the game stuck there`: `miso/Assets/_Project/Core/ProgramFlow/Runtime/HomeMemoryTransition.cs`, `miso/Assets/_Project/Core/ProgramFlow/Editor.meta`, `miso/Assets/_Project/Core/ProgramFlow/Editor/HomeMemoryTransitionTests.cs`, `miso/Assets/_Project/Core/ProgramFlow/Editor/HomeMemoryTransitionTests.cs.meta` (plain; the fix and its tests in one unit)

Don't stage THJ's uncommitted files (`AIFactionBrain.cs`, `AIUnitBrain.cs`, `PreloadScreen.unity`, `ProjectSettings/*`, the TMP fallback font).

## Other branches

None known. Other branches that carry Memory 4's end sequence and this controller need the same fix.

## How to see it

1. Play the Hearth from Memory 4 (or fast-forward to it through the normal mission flow, not the sandbox, which stops Play at the end by design).
2. Win Memory 4. The end sequence runs: the mother falls, the grid fades, dialogue plays, the Home view comes up, then the cub dialogue and the cutaway.
3. Expected: no "TransitionToNextLevel has no next level to load." warning and no mission-complete panel. Shortly after the sequence ends, the loading screen appears and the Home scene loads with the Hearth recorded as complete (its completion sequence, if any, plays at Home). Mission-completion resources are granted once.
4. At Home, no transition overlay is left over the screen, and Home input works.
