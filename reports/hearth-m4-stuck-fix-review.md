# Review: Memory 4 ends the mission from the Home view (D-528)

Reviewer: `miso-reviewer` (read-only; filed by the coordinator, 2026-11-12). **Verdict: APPROVE**, nothing to fix.

1. **The "mission complete" test.** It is correct at outro time. `MarkCurrentLevelCompleted` runs only on a Win, before `PlayOutro`, and `!hasNextLevel` is the same test `EndLevel` uses. It can't fire on a defeat, a replay (`SetMission` clears the completed list), a mid-mission level or a non-combat level type.
2. **No double award and nothing skipped.** `IsChangingLevel` is set before `:768`, so no panel is queued and `EndMission(true)` runs once, after the awards, `levelEnded` and `DeInitialize`. `stats.EndMission()` is reproduced.
3. **The wait mirrors `ChangeLevel`.** `GoHome` → `HideForSceneLoad` clears the flags, the overlay and the home copy.
4. **Destroyed mid-wait.** Safe: the coroutine dies with the controller, and any scene load stops it.
5. **`ResolveNextStep` public for the tests.** Acceptable: there are no asmdefs, and it's a pure function.
6. **The tests can fail.** No IDs, LF kept, no statics. `GameHandler`, `MissionTracker` and `CombatLevelRunHandler` are unchanged.

## Notes
- The tests cover only the decision. The data gathering, the coroutine and the scene flow are checked by reading the code. THJ's play of Memory 4 is the real acceptance check.
- Minor: `GameHandler.Instance.EndMission(true)` at `HomeMemoryTransition.cs:206` has no null check after the wait. It's persistent and checked on entry.
- Already there before this change: `HomeMemoryTransition.ResetPlayModeState` uses `[RuntimeInitializeOnLoadMethod]`, not the `PlayModeStaticReset` hook. Backlog.
