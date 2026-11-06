# Report: Select a unit from a sequence, and select Mark after his arrival

Plan: none (size S, coordinator brief)    Agent: implementer    Branch: thj/onboarding
Outcome: done in code, data and tests. Not yet seen in play: Mark's selection needs the verifier's or THJ's play check (no Play session was started).

## What changed

- `Core/Interactions/Runtime/PlayerController.cs`: `class` becomes `partial class`. One word, nothing else (core).
- `Core/Interactions/Runtime/PlayerController.ScriptedSelection.cs` (new): public `TrySelectUnit(GUnit)` and read-only `GetScriptedSelectDecision(GUnit)` (core, additive; nothing in the normal turn flow calls them).
- `Core/Interactions/Runtime/ScriptedUnitSelectRules.cs` (new): the decision enum, the pure rule, the free-frame count and the warning reasons.
- `Core/Levels/Runtime/SelectUnitSequence.cs` (new): the step, menu `Game/Sequence/SelectUnitSequence`, field `unitNickname`.
- `Resources/Sequences/Hearth/Memory4Mark/Memory4Mark_Arrival_SelectMark.asset` (new, created through Unity, GUID `9d791e14c5d1c0b4fb755918045772de`): `unitNickname: Mark`.
- `Resources/Sequences/Hearth/Memory4Mark/Memory4Mark_Arrival_SequentialSequence.asset`: one line added; the new step is the last of 12.
- Tests (new): `Core/Interactions/Editor/ScriptedUnitSelectRulesTests.cs`, `Core/Levels/Editor/SelectUnitSequenceTests.cs`, `Features/Onboarding/Editor/HearthMemoryMarkTests.ArrivalSelection.cs`.
- Each new file has its `.meta`.

## Why placement alone can't hold (the brief asked for this)

No position in the arrival list can guarantee the selection, on this level or any other using `PlayerController.prefab`:

1. `EnemyIntroductionController` is on `Content/Controllers/PlayerController.prefab`, enabled with a camera effect, and `deactivateUnitIntroductions` is 0. So the "reset" call's `RestartTurn` > `StartTurn` always takes the `StartTurnWithIntroductions` path, even with nothing to introduce.
2. `PlayPending` sets `IsRunning = true`, then loops while `SessionLogs.SequenceInProgress`. The arrival sequence itself is that sequence, so the controller is busy until the list has finished.
3. While it is busy, `HandleGridCellSelection` returns at once (`IntroductionInProgress`), so a direct selection from any step is ignored.
4. When `PlayPending` ends, `AutoSelectUnit()` picks a random unit, after the last step.

Pending enemy intros: this level's only enemy nickname is `Dark Claw`, and some are active from the start, so the level-start intro or an earlier level has normally marked it seen. Mark's Claws then add no intro, but the busy period in points 2-4 happens anyway. If an intro did play (a reset seen list), it would run after the sequence and the selection would wait for it.

**What I did instead:** the step asks the controller. If the controller is busy, the step ends at once and leaves a small follow-up coroutine on the sequence player (the same pattern as `UnitAnimationSequence.FollowUp`). The follow-up selects once the controller has been free for 2 frames in a row, which puts it after the auto-select and after any late turn restart. The step sits last, after ResetTurn, CameraOnMark, EnablePlayerInput and ShowHUD, so the HUD is back if the selection is immediate (introductions turned off in settings).

## Acceptance criteria

- [x] New `SelectUnitSequence` with `unitNickname`; finds the living unit, asks the controller, next step starts at once: the step never yields. Test: `SelectUnitSequenceTests`. The successful path needs the play check.
- [x] Missing, dead, not a player unit, not in units to play, or another faction's turn logs a warning naming the unit and continues; never hangs or throws: rules in `ScriptedUnitSelectRulesTests`; missing, dead and no-controller warnings in `SelectUnitSequenceTests`; exceptions are caught in the step. The not-a-player-unit and wrong-turn warnings through a real controller need a level, so only the rule is tested.
- [ ] Mark is selected every run with the UI showing it, and the player can act right away: **built, not seen in play.** Reasoned from the code above. Verifier or THJ to confirm.
- [x] Selecting doesn't reset AP, end anything or lock input: from reading the code. It uses the click path (`HandleGridCellSelection`), which never touches `ToPlayUnits`' AP, turn end or input modes; a `TakeAction` state is refused by the busy check. To confirm in play.
- [x] EditMode tests: pure decision, free-frame count, warnings. `HearthMemoryMarkTests.TheArrivalSelectsMarkAsItsLastStep_AfterTheTurnResetAndTheHudComeBack` checks the step comes after ResetTurn and is last, with Mark's real nickname.
- [x] Asset created through Unity with a real GUID and field order.
- [x] Full EditMode suite: 1445 tests, 1434 passed, 11 failed. All 11 are the expected reds: `AIRegressionTest.Baseline_MatchesCurrentAI` and 10 `HearthMemoryMarkTests` layout tests. All new tests pass. No compile errors.

## Save reset

No.

## Decisions I made

- Deferred selection after the sequence, as explained above. Same outcome as the brief, and it needs no edit to `AutoSelectUnit` or `StartTurnWithIntroductions`. Tier 2, flagged for review.
- Two public members instead of one: `TrySelectUnit`, plus read-only `GetScriptedSelectDecision`, which the follow-up polls without selecting. THJ approved "a small additive public method", so this is one more than the wording.
- `partial` on `PlayerController`, per the house rule for big files. Tier 2 core note; no behavior change.
- `TrySelectUnit` steps back to unit selection before selecting. A direct click during action selection could read as "use this ability on that ally" (`IsAllyTargetException`). If the unit is already selected in action selection it does nothing.
- A QTE also counts as busy.

## Needs THJ

None. One thing to look at in play: see "Risks" on the camera.

## Docs to update

- `tech/core-systems.md`, Faction controllers row: `PlayerController` is now partial, with `PlayerController.ScriptedSelection.cs` (`TrySelectUnit`, `GetScriptedSelectDecision`) and `ScriptedUnitSelectRules`.
- `build-log.md`: this step, with the hash.

## Risks and loose ends

- **Brief random selection:** on this path the random auto-select still runs first, so for about 2 frames another unit can be selected. Selection also calls `Focus` on the unit, so if Lucy, Linda or John is picked the camera starts toward them and then goes back to Mark. Possibly a small visible nudge. If it shows, the clean fix is a one-shot "preferred unit" read by `AutoSelectUnit`, which does change a core method, so that's THJ's call.
- **Extra unit ticks:** a selection change runs `UnitTick` on all units (`CombatLevelRunHandler.OnUnitSelectionChanged`). Moving from the random unit to Mark adds the same ticks as a player pressing the switch key.
- **Wiring tool is out of date:** `HearthMemoryWiring.Mark.Sequences.cs` still builds the arrival list without this step, and with `LucyRunsAhead` where the asset now has `PostBloom`. Rerunning it would drop both. I did not change or run it.
- **The arrival-related red:** `TheArrivalBoastsRunsLucyAheadRevealsMarksClawsAndResetsTheTurn` fails with `run` at -1, because the top-level list has the nested `PostBloom` sequence and no `MoveUnitSequence`. That is not caused by this step, and its expected list needs touching, so I left it as instructed.
- If the arrival ever plays when it isn't the player's turn, "reset" does nothing (it requires the Bergsons faction) and the step warns `it is not the player's turn`. Not seen in the code path for this level, but a Claw killed on an enemy turn would do it.
- Console during the test run showed non-failing errors such as `Can't remove GUnit (Script) because MemorableAttackMemoryShare (Script) depends on it`, `Unsupported type Vector2f` and abilities reaching their activation frame without targets. I didn't check whether these predate this work.
- THJ's uncommitted files were left alone; no scenes saved; only the two assets above were saved.

## Proposed commits

1. `feat(player): a script can ask the player controller to select a unit`: `Core/Interactions/Runtime/PlayerController.cs`, `PlayerController.ScriptedSelection.cs` + `.meta`, `ScriptedUnitSelectRules.cs` + `.meta`, `Core/Interactions/Editor/ScriptedUnitSelectRulesTests.cs` + `.meta` (core)
2. `feat(levels): SelectUnitSequence selects a player unit by nickname`: `Core/Levels/Runtime/SelectUnitSequence.cs` + `.meta`, `Core/Levels/Editor/SelectUnitSequenceTests.cs` + `.meta` (plain)
3. `feat(onboarding): Mark is selected after his arrival in his memory`: `Resources/Sequences/Hearth/Memory4Mark/Memory4Mark_Arrival_SelectMark.asset` + `.meta`, `Memory4Mark_Arrival_SequentialSequence.asset`, `Features/Onboarding/Editor/HearthMemoryMarkTests.ArrivalSelection.cs` + `.meta` (plain, this branch only)

Per the play-test rule, these should wait until THJ has played it.

## Other branches

Commits 1 and 2 can go anywhere. Commit 3 is `thj/onboarding` only.

## How to see it

1. Open Memory 4 (Mark's memory) and press Play.
2. Kill a Bloom Claw to finish stage 1, and let the arrival play: boast, reveal, lines, camera on Mark, HUD back.
3. Right as it ends, Mark should be selected: his panel showing, his move range highlighted, his selection marker on. Run it 4 or 5 times, since the auto-select is random and is the thing being overridden.
4. Watch the camera at the end. It should stay on Mark, with at most a tiny nudge (see Risks). Tell me if the nudge bothers you.
5. Move or attack with Mark right away: he should have full AP and input should work. Check also with the Claw killed by the last AP of the turn: the turn must not end.
6. Hold to skip the dialogue during the arrival: Mark should still end up selected.
7. Check the console: no `[SelectUnitSequence]` warning.
