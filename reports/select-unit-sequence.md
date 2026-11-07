# Report: Select a unit from a sequence, and select Mark after his arrival

Plan: none (size S, coordinator brief, then rework after `reports/select-unit-sequence-review.md`)    Agent: implementer    Branch: thj/onboarding
Outcome: done in code, data and tests. Not yet seen in play: Mark's selection needs the verifier's or THJ's play check (no Play session was started).

Rework: the follow-up coroutine is gone. It let the random pick run first, which played another hero's Switch, maybe a bark, and moved the panel and camera before Mark was selected. It is replaced by a one-shot preferred unit read inside `AutoSelectUnit`, the core edit THJ approved.

## What changed

- `Core/Interactions/Runtime/PlayerController.cs` (core, 4 lines): `partial`; `EndTurn` clears the preference; `AutoSelectUnit` takes the preference before its empty-list check and uses it instead of the random pick.
- `Core/Interactions/Runtime/PlayerController.ScriptedSelection.cs` (new, core): public `TrySelectUnit(GUnit)`, the preference field, and a private decision method.
- `Core/Interactions/Runtime/PreferredAutoSelectUnit.cs` (new, core): the one-shot holder (`Store`, `Clear`, `Take`).
- `Core/Interactions/Runtime/ScriptedUnitSelectRules.cs` (new): the decision enum, the pure rule, `IsFailure`, the warning reasons.
- `Core/Levels/Runtime/SelectUnitSequence.cs` (new): the step, menu `Game/Sequence/SelectUnitSequence`, field `unitNickname`. It ends at once, with no coroutine.
- `Resources/Sequences/Hearth/Memory4Mark/Memory4Mark_Arrival_SelectMark.asset` (new, created through Unity, GUID `9d791e14c5d1c0b4fb755918045772de`): `unitNickname: Mark`.
- `Resources/Sequences/Hearth/Memory4Mark/Memory4Mark_Arrival_SequentialSequence.asset`: one line added; the new step is the last of 12.
- Tests (new): `Core/Interactions/Editor/PreferredAutoSelectUnitTests.cs`, `Core/Interactions/Editor/ScriptedUnitSelectRulesTests.cs`, `Core/Levels/Editor/SelectUnitSequenceTests.cs`, `Features/Onboarding/Editor/HearthMemoryMarkTests.ArrivalSelection.cs`.
- Each new file has its `.meta`.

Removed in the rework: the coroutine, the frame counting, and the public `GetScriptedSelectDecision` (now private).

## What I checked about the step's position (read from the code, not played)

**Is the preference still there when the deferred `AutoSelectUnit` runs? Yes.**

1. `EnemyIntroductionController` is enabled on `Content/Controllers/PlayerController.prefab` and `deactivateUnitIntroductions` is 0, so the reset's `StartTurn` takes `StartTurnWithIntroductions`.
2. `StartTurn` sets `PhaseData.IsInProgress = true`, and `PlayPending` holds `IsRunning` while `SessionLogs.SequenceInProgress`. So at the last step of the arrival the controller is busy, it is the player's turn, and the unit is stored.
3. Nothing can use or clear it before the deferred pick:
   - `RestartTurn` and `StartTurn` don't clear it; only `EndTurn` does.
   - No action can finish, because clicks and ability selection are refused during `IntroductionInProgress`, so `OnUnitTurnComplete` can't run.
   - `HandleReactiveInterrupt` returns during introductions, so the reactive path can't run.
   - `RequestEndTurn` is refused during introductions, and a pending turn switch was cancelled by the reset (`CancelTurnActiveSwitch`), so `EndTurn` doesn't run.
4. When `PlayPending` ends, `AutoSelectUnit` runs and Mark, who has fresh AP, is picked with no random pick first. If a Dark Claw intro did play (a reset seen list), the preference waits through it.

**Can a `RestartTurn` after a direct select silently lose Mark? Not on this list, in practice.**

- `ResetCurrentPhase` defers `RestartTurn` through a `WaitWhile`, and I can't tell from the code whether that resolves in the same frame or the next. So the step must not rely on it.
- Hold-to-skip collapses dialogue and camera steps only. `ShowHUD` is non-instant and still plays. `HideHUD` ran at step 2 and nothing shows the HUD in between (`PostBloom` has no HUD step), so the panels take their full tween, about 0.5 s, between ResetTurn and this step. That is the reason the step must stay after `ShowHUD`. The test pins this.
- So by the time the step runs, either `RestartTurn` has already run (busy, stored) or an action is still in progress (busy, stored, and the restart comes later without clearing it).

**Three narrow cases can still lose it. I left them as they are:**

1. The killing action is still in progress when the step runs and ends with no AP left on the acting unit. `OnUnitTurnComplete` then spends the preference, and the waiting `RestartTurn` picks at random. The action would have to outlast the whole arrival, including `PostBloom`'s walks.
2. That same action frees the controller in the exact frame the step runs, and the step goes before the waiting restart. Mark is selected directly, then lost to the restart.
3. With `deactivateUnitIntroductions` on (off today), `StartTurn` auto-selects at once. The step then selects directly, so the random hero's Switch plays first, as in the old behavior.

## Acceptance criteria

- [x] New `SelectUnitSequence` with `unitNickname`; finds the living unit, asks the controller, next step starts at once: the step never yields. Test: `SelectUnitSequenceTests`. The successful path needs the play check.
- [x] Missing, dead, not a player unit, not in units to play, or another faction's turn logs a warning naming the unit and continues; never hangs or throws: rules in `ScriptedUnitSelectRulesTests`; missing, dead and no-controller warnings in `SelectUnitSequenceTests`; exceptions are caught in the step. The not-a-player-unit and wrong-turn warnings through a real controller need a level, so only the rule is tested.
- [x] A preference can't be stored on another faction's turn: the turn check comes before the busy check. It needs `IsTurnActive` and the handler's current controller to be this one, so a reactive interrupt on an enemy turn doesn't pass. Test: `AnotherFactionsTurn_IsRefused_NeverDeferred_EvenWhileBusy`.
- [ ] Mark is selected every run with the UI showing it, no other hero's Switch or bark first, and the player can act right away: **built, not seen in play.** Verifier or THJ to confirm.
- [x] Selecting doesn't reset AP, end anything or lock input: from reading the code. It uses the click path, and the deferred case changes only which unit the existing auto-select picks. To confirm in play.
- [x] `AutoSelectUnit` with nothing stored behaves as today: `Take` returns null and the same random line runs. Preferred used, ignored if dead or not to play, destroyed, cleared after one use and cleared by `Clear`: `PreferredAutoSelectUnitTests`.
- [ ] Not directly tested: the `Clear` call in `EndTurn` and the `Take` call in `AutoSelectUnit` (a `PlayerController` needs a running level). Only the holder is tested; the two call sites are 1 line each, in the diff.
- [x] Nothing kept across levels: no static. `Faction.GetController()` instantiates the controller per level, and I found no `DontDestroyOnLoad` for it (searched `Core/Interactions`, `Core/Units/Runtime/Factions`, `Core/Levels/Runtime`), so no level-end clear is needed.
- [x] `HearthMemoryMarkTests.TheArrivalSelectsMarkAsItsLastStep_AfterTheTurnResetAndTheHudComeBack`: the step is after ResetTurn, EnablePlayerInput and ShowHUD, and last, with Mark's real nickname.
- [x] Full EditMode suite after the rework: 1452 tests, 1441 passed, 11 failed. All 11 are the expected reds: `AIRegressionTest.Baseline_MatchesCurrentAI` and 10 `HearthMemoryMarkTests` layout tests. All new tests pass. No compile errors.

## Save reset

No.

## Decisions I made

- `PreferredAutoSelectUnit` is a small class on `GUnit`, so its rules run in EditMode.
- `Take` runs before `AutoSelectUnit`'s empty-list check, so the preference is cleared even when nobody can play.
- A direct selection also clears any older preference, so a stale one can't redirect a later auto-select.
- The enum's busy value is now `Deferred`. `IsFailure` decides which results warn.
- `TrySelectUnit` still steps back to unit selection first, because a direct click during action selection could read as "use this ability on that ally".
- A QTE still counts as busy.

## Needs THJ

None.

## Docs to update

- `tech/core-systems.md`, Faction controllers row: `PlayerController` is now partial, with `PlayerController.ScriptedSelection.cs` (`TrySelectUnit`), `PreferredAutoSelectUnit` and `ScriptedUnitSelectRules`; `AutoSelectUnit` uses a one-shot preferred unit, `EndTurn` clears it.
- `build-log.md`: this step, with the hashes.

## Risks and loose ends

- **Deferred is only as good as the next auto-select.** It works after a turn reset. Used elsewhere, for example while an action runs with AP left, no auto-select may follow: the step logs nothing, and the preference waits for a later auto-select in that turn or dies at `EndTurn`. The class comment says to place it after a reset.
- **No warning at the moment of use:** if the stored unit died or lost its AP before the auto-select, the random pick runs silently.
- **No level-end guard:** the review's `IsLevelEnded` note was for the coroutine, so I didn't add it. A select step in an outro would still try to select if the turn is still marked active. None exists today.
- **Test leftover:** this run left `Content/Levels/Greybox/__CameraStartTest/` (2 prefabs), though `GridToLevelCameraStartTests` passed and its `TearDown` should delete that folder. The timestamps fall inside my run, the earlier run left nothing, and none of my tests touch it. **It is still on disk, untracked.** I tried to delete it with the `AssetDatabase.DeleteAsset` call the test uses, but the editor tool's safety check blocked that, and I did not override the check or delete it another way. It is not part of any proposed commit and must not be staged. THJ or the coordinator can delete `Content/Levels/Greybox/__CameraStartTest/` and `__CameraStartTest.meta` in Unity. Cause unknown, so it may recur.
- **Wiring tool is out of date:** `HearthMemoryWiring.Mark.Sequences.cs` builds the arrival without this step and with `LucyRunsAhead` where the asset now has `PostBloom`. The review says its menu entry is retired. Not changed, not run.
- **The arrival-related red:** `TheArrivalBoastsRunsLucyAheadRevealsMarksClawsAndResetsTheTurn` fails with `run` at -1 because the top-level list has the nested `PostBloom` and no `MoveUnitSequence`. Not caused by this step; its expected list needs touching, so I left it as instructed.
- **Known case, left as instructed:** if a Claw dies on an enemy turn, the reset does nothing and the step warns `it is not the player's turn`.
- Non-failing console errors seen in the first test run (`Can't remove GUnit (Script) because MemorableAttackMemoryShare (Script) depends on it`, `Unsupported type Vector2f`, abilities reaching their activation frame without targets). I didn't check whether they predate this work.
- THJ's uncommitted files were left alone; no scenes saved. The only assets I saved are the two above.

## Proposed commits

1. `feat(player): a script can select a unit, or name the one the next auto-select picks`: `Core/Interactions/Runtime/PlayerController.cs`, `PlayerController.ScriptedSelection.cs` + `.meta`, `PreferredAutoSelectUnit.cs` + `.meta`, `ScriptedUnitSelectRules.cs` + `.meta`, `Core/Interactions/Editor/PreferredAutoSelectUnitTests.cs` + `.meta`, `Core/Interactions/Editor/ScriptedUnitSelectRulesTests.cs` + `.meta` (core)
2. `feat(levels): SelectUnitSequence selects a player unit by nickname`: `Core/Levels/Runtime/SelectUnitSequence.cs` + `.meta`, `Core/Levels/Editor/SelectUnitSequenceTests.cs` + `.meta` (plain)
3. `feat(onboarding): Mark is selected after his arrival in his memory`: `Resources/Sequences/Hearth/Memory4Mark/Memory4Mark_Arrival_SelectMark.asset` + `.meta`, `Memory4Mark_Arrival_SequentialSequence.asset`, `Features/Onboarding/Editor/HearthMemoryMarkTests.ArrivalSelection.cs` + `.meta` (plain, this branch only)

Per the play-test rule, these should wait until THJ has played it.

## Other branches

Commits 1 and 2 can go anywhere. Commit 3 is `thj/onboarding` only.

## How to see it

1. Open Memory 4 (Mark's memory) and press Play.
2. Kill a Bloom Claw to finish stage 1, and let the arrival play: boast, reveal, lines, camera on Mark, HUD back.
3. Right as it ends, Mark should be selected: his panel showing, his move range highlighted, his selection marker on. No other hero should play a Switch or bark first, and the camera should stay on Mark. Run it 4 or 5 times, since the old random pick landed on someone else about 3 runs in 4.
4. Move or attack with Mark right away: he should have full AP and input should work.
5. Repeat with the Claw killed by the last AP of the turn: the turn must not end, and Mark is still selected.
6. Hold to skip the dialogue during the arrival: Mark should still end up selected. This is the case the review flagged.
7. Check the console: no `[SelectUnitSequence]` warning.
