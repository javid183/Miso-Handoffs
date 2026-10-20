# Report: Masher C1 verify (incl. D-106 recheck)

Plan: plans/2026-10-20-masher-reckless-tank-tech.md    Agent: miso-verifier    Branch: masher-tweak (uncommitted changes)
Outcome: done

**Result:** PASS (quiet checks only; Play mode out of scope)

## Compile

Clean. Forced refresh + compile via Unity MCP; console errors: 0 (read_console and `error CS` count in Editor.log: 0). Console warnings (50) are all pre-existing: none from `AIController.cs`, `TurnSwitchHoldTests.cs` or `CombatLevelRunHandler.TurnSwitchHolds.cs`. `CombatLevelRunHandler.cs` shows three (CS0108 at line 86, CS8509 at 683, CS8524 at 691); the same code (`ResetPlayModeState`, two `switch` expressions) is in HEAD and the diff hunks (lines 73, 462, 655) don't touch them, so none is new.

## Tests

EditMode Run All: 283 run / 282 passed / 1 failed / 0 skipped (65.7 s). Only failure: `MISO.Core.Systems.AI.EditorTests.AIRegressionTest.Baseline_MatchesCurrentAI` (known red, not touched).
`TurnSwitchHoldTests` (MISO.Core.Interactions.EditorTests), run alone: 10/10 passed (Clear_DropsEveryHold, NoHolds_IsNotHeld, Register_HoldsUntilReleased, ReleaseUnknownOwner_IsNoOp, SameOwnerTwice_IsOneHold, TwoOwners_HeldUntilBothRelease, Watchdog_HeldAtTimeout_ClearsJustPast_AndNamesOwners, Watchdog_NamesUnityOwnerByName, Watchdog_ReleaseThenRegister_RestartsTheTimer, Watchdog_SkippedFrame_RestartsTheTimer).

## Acceptance criteria

- [x] Console clean (no errors, no new warnings from the four files): see Compile.
- [x] EditMode all green except the known red: 282/283, see Tests.
- [x] 10 TurnSwitchHoldTests pass: 10/10.
- [x] D-106 recheck present (read-only `git diff` of `AIController.cs`): `HandleUnits` WaitWhile also waits on `PhaseData.IsInProgress`, and after `ConsumeWorkerError()` a `if (PhaseData.IsInProgress) continue;` drops the plan before `PerformAction`. Code check and compile only; behaviour not play-tested.

## Bugs found

none

## Save reset

no

## Editor checks corrections

- `run_tests` with `test_names: ["TurnSwitchHoldTests"]` (short class name) matched 0 tests and reported "Passed"; the full name (`MISO.Core.Interactions.EditorTests.TurnSwitchHoldTests`) is needed. Beware of a false green.
- Whole-suite `get_test_job` returns a huge payload; `result.summary` holds the counts and `progress.failures_so_far` the failure names (the `results` list is empty unless `include_details`). One call timed out and one returned "plugin session disconnected" before the third call worked.
- Suite size on `masher-tweak`: 283 tests (65.7 s).
- Unity MCP tools were available this session after the reconnect.

## Other branches

none
