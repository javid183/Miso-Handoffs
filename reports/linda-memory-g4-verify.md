# Report: Diagnose two Linda test failures after G4 (linda-memory-g4-verify)

Result: both failures reproduce alone. They are NOT caused by the G4 files. The committed `GB_m1-linda.prefab` does not contain the wiring the tests expect.
Branch: thj/onboarding (HEAD 67fb2d3bf). Save reset: no.

## Steps
1. Console / temp folder: the console held no compile errors (only the AI regression report text and two Unity serialization warnings). `Assets/__SharedConditionTest` is gone: `AssetDatabase.IsValidFolder` false, folder and .meta absent on disk.
2. `MISO.Core.Features.Onboarding.EditorTests.HearthMemoryLindaTests` alone (note the namespace is `MISO.Core.Features...`, not `MISO.Features...`; a wrong guess matched 0 tests and reported a false green): 8 run, 6 passed, 2 failed.
   - TheHiddenClawsAreSwitchedOffInThePrefab: "Unit_DarkClaw stays out of play until revealed. Expected: False But was: True" (HearthMemoryLindaTests.cs:139)
   - ThreeStagesInAQueue: "Expected: 4 But was: 2" (HearthMemoryLindaTests.cs:73, the turn-cap check of stage 0)
3. Order effect: not applicable, since they fail alone. The full run (step 5) includes SharedObjectiveConditionTests and gave the same two failures with the same messages.
4. Inspection of what the tests read:
   - Effective (loaded) data of `GB_m1-linda.prefab` through AssetDatabase: turn caps are 2 / 3 / 4 for stages 0 / 1 / 2 (ids ...035, ...193, ...195), and all 7 `Unit_DarkClaw` objects are active. Both match the test failures.
   - `AssetDatabase.IsDirty` is false, so the prefab is not modified in memory.
   - Raw YAML on disk shows the same: overrides `managedReferences[...035].turn = 2`, `[...193].turn = 3`, `[...195].turn = 4`, and no `m_IsActive: 0` lines.
   - `git hash-object` of the file equals `HEAD:` blob `f8dd3af36...`, so disk equals the commit. HEAD~1 also had only the `035.turn = 2` override.
   - Force reimport of the prefab and rerun: same two failures, so it is not a stale import cache.
   - The tests want turn cap `HearthMemoryWiringLinda.TurnCap` = 4 on every stage and the hidden claws switched off. `HearthMemoryWiring.Linda.cs` sets these when "Wire Memory 1 (Linda)" runs.
5. Full EditMode: 1315 total, 1311 passed, 4 failed (155 s).
   - HearthMemoryLindaTests.TheHiddenClawsAreSwitchedOffInThePrefab
   - HearthMemoryLindaTests.ThreeStagesInAQueue
   - SharedObjectiveConditionTests.NoLevelPrefabSharesAnObjectiveCondition (expected; flags `Level2/Level2-C2.prefab`)
   - AIRegressionTest.Baseline_MatchesCurrentAI (known red)

## Best cause
The committed (and on-disk) `GB_m1-linda.prefab` is in a state that was never wired to the final spec: turn caps 2/3/4 instead of 4/4/4, and the claws active. The L1 verify run (15:13, 1309/1310) passed with the tool-run prefab. Disk has an mtime of 19:53, after the 19:03 commit, but its content is identical to HEAD. So either the wired state was lost before the commit (the prefab was open in THJ's editor during the tool run, so a later save, revert or git restore may have replaced it) or the commit captured an earlier save. The G4 report says it did not touch `GB_m1-linda` (it is "clean" in the scan), and the G4 files only create or delete temp assets under `__SharedConditionTest`. The cause is not an order effect and not an in-memory change.

## Fix suggestion (not done: read-only)
Re-run Tools > Onboarding > Wire Memory 1 (Linda) with the prefab closed. Then rerun HearthMemoryLindaTests; both should go green. Review the resulting diff before committing it. Do not rely on the L1 verify result for the committed state.

## Bugs found
Committed `GB_m1-linda.prefab` lacks the stage turn caps (4/4/4) and the switched-off claws. Repro: run the two tests; expected pass, actual fail as above.

## Editor checks corrections
- Confirmed again: a test name filter with a wrong namespace matches 0 tests and reports Passed. `HearthMemoryLindaTests` is in `MISO.Core.Features.Onboarding.EditorTests`.
- Full suite via Unity MCP: `get_test_job` disconnected once, and the final result (61k chars) was saved to a file; read it with Python. About 155 s on this branch (1315 tests).
