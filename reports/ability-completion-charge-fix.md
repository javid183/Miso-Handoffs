# Report: Ability completion charges the unit that acted (core bugfix)

Plan: plans/2026-11-24-ability-completion-charge-fix.md    Agent: miso-implementer    Branch: thj/onboarding-demo
Outcome: done (charge fix D-657 + turn-flow guard D-660, one core change set; THJ's play check pending)

## What changed

- `miso/Assets/_Project/Core/Interactions/Runtime/FactionControllerBase.cs` (core, LF + BOM kept):
  - `SetTakeActionState`'s `ApplyAction` captures `actingUnit` / `actingAbility` when the action starts. In the completion lambda, after un-targeting cells, it checks whether the selection still holds them. If it doesn't, it charges the captured unit (`ChargeAfterSelectionMoved`), calls `onCompletion` and returns. Otherwise the old code runs; its AP-count expression moved, unchanged, into `ActionAPCount(unit, ability)`.
  - `TryTakeAction` captures `actingAbility` before `Apply`. In the delayed block, right after `PhaseData.IsInProgress = false;`, one new line: `if (TryFinishActionOutsideTakeAction(actingAbility)) return;`. The rest of the block is untouched.
- `miso/Assets/_Project/Core/Interactions/Runtime/FactionPhaseState.cs` (core, LF + BOM kept): additive overload `FactionPhaseData.UpdateUnitActionPoints(GUnit unit, RuntimeAbility ability, int count)`. The existing `UpdateUnitActionPoints(int)` is untouched.
- `miso/Assets/_Project/Core/Interactions/Runtime/FactionControllerBase.ActionCompletion.cs` (+ `.meta`, new partial):
  - `public static bool IsSelectionStillOn(GUnit selectedUnit, RuntimeAbility selectedAbility, GUnit actingUnit, RuntimeAbility actingAbility)`
  - `public static bool ChargeUnitThatActed(FactionPhaseData, GUnit, RuntimeAbility, int usualCount)`: same `AbilityCostOverride.Charge` and free-use record; false, charging nothing, when the unit, its APConsumer or the ability is gone.
  - `public static bool LeftTakeActionBeforeCompletion(FactionPhaseState current, FactionPhaseState takeAction)`
  - `protected bool TryFinishActionOutsideTakeAction(RuntimeAbility ability)`: when the controller has left TakeActionState, raises `abilityPerformed`, calls `OnActionResolved` and returns true. It does not change state and does not request turn end.
  - Private `ChargeAfterSelectionMoved` (try/catch + `Debug.LogException`) and `ActionAPCount`.
- `miso/Assets/_Project/Core/Interactions/Editor/ActionCompletionChargeTests.cs` (+ `.meta`, new): 8 tests.
- `miso/Assets/_Project/Core/Interactions/Editor/ActionCompletionGuardTests.cs` (+ `.meta`, new): 4 tests.
- Not changed: `ConsumeActionCost(int)` (still virtual; `PlayerController`'s reactive-interrupt override still runs on normal actions), `EndLevel`, `PlayerController`, `AIController`.

## Acceptance criteria

- [x] An ability whose completion arrives after the controller left TakeActionState charges the unit that acted, raises no exception, and runs its completion chain to the end.
  - Charge: `ChargeUnitThatActed` tests (no unit selected, another unit selected, free use, gone unit).
  - Chain: our lambda calls `onCompletion`. Then `TryTakeAction`'s delayed block clears `IsInProgress` and the guard raises `abilityPerformed` once and calls `OnActionResolved`, without entering a state (guard tests). `RuntimeAbility.OnCompletionShared` finishes because nothing in our callback throws any more.
  - The full in-scene flow needs THJ's play check.
- [x] Normal actions charge exactly as before (same AP, same free-cost override, including the Cyclone's free Steer).
  - The only additions on the normal path are two reference comparisons that come out "still on" and "still in TakeAction". Everything after them is the old code.
  - Covering fixtures pass 222/222: `MISO.Core.Interactions.EditorTests` (including the 12 new tests), `AbilityCostOverrideTests` and `CycloneSteerTests` (all partials).
  - A guard test confirms a normal completion takes the usual flow and the guard raises nothing.
- [x] EditMode tests for both cases: 12 new, all pass.
- [x] Full EditMode suite (final run): 2634 total, 2624 passed, 9 failed, 1 skipped (the Explicit AI test).
  - 8 failures are the expected `M1RidgeTests` (D-651).
  - The ninth is a GridToLevel flake: `GridToLevelTests.Builder_BigUnitsSitOnTheirAnchorAtTheFootprintCentre`, an unhandled editor assert `m_LockCount == 0` from `PrefabUtility.UnloadPrefabContents`. Rerun alone, `GridToLevelTests` passes 20/20. The earlier run had the same flake on `GridToLevelCameraStartTests.Build_CameraLinePutsTheViewOnThatTile`, which passed 17/17 alone.
- AI regression (run by name; the AI shares this action path): `Baseline_MatchesCurrentAI` gives CHECKS 731, FAILURES 44, the same as the recorded 44 (D-644).

## Chunks

### Chunk 1: completion charges the captured unit (D-657)

- Changed: `FactionControllerBase.cs` (capture + late branch in `SetTakeActionState`), `FactionPhaseState.cs`, the new partial, `ActionCompletionChargeTests.cs` and the `.meta` files.
- Criteria met: the late charge goes to the unit that acted (tests); the normal charge is unchanged (fixtures).
- Decisions and loose ends: the chain still threw one step later, in `TryTakeAction`'s delayed block (`CurrentPhaseState.GetNextState()` advanced from UnitSelectionState into ActionSelectionState, then NRE at `FactionControllerBase.cs:480` on a null `ActiveUnit`). Reported; THJ chose option A.

### Chunk 2: turn-flow guard on a late completion (D-660)

- Changed: `FactionControllerBase.cs` (`TryTakeAction`: one captured local, one guard line), the partial (`LeftTakeActionBeforeCompletion`, `TryFinishActionOutsideTakeAction`), `ActionCompletionGuardTests.cs` and its `.meta`.
- Criteria met: a late completion after a state change finishes without throwing, raises `abilityPerformed` once with the acting ability, and leaves the current state alone with no state entered (tests). A normal completion's guard does nothing (test). Full suite and AI regression as above.
- Decisions and loose ends:
  - The guard reports the ability captured before `Apply` (the acting one), not `PhaseData.ActiveAbility` read at completion, which may be null or another ability once the controller moved on. The normal path keeps its own `ability` local, unchanged.
  - The guard runs after `IsInProgress = false`, as THJ specified. It does not call `OnUnitTurnComplete` or `RequestEndTurnSafe`, because the controller is already doing something else.

## Reviews and checks

- (coordinator)

## Save reset

no

## Decisions I made

- "Selection moved on" means the selected unit or ability differs by reference from the ones captured at the start. Normal actions therefore take the old code path, including `PlayerController`'s virtual `ConsumeActionCost(int)`.
- The late charge skips `SetPotentiallyTargetedCells(false)` and the re-select or cleanup block. Both read the live selection.
- The AP-count expression moved, unchanged, into a private `ActionAPCount`, so both paths share one formula.
- The late charge is wrapped in try/catch + `Debug.LogException`, so a late charge can never stop the chain.
- The guard tests drive the real `FactionControllerBase` (protected fields set and the protected method invoked by reflection) with a test `GlobalEventBus`, following `LevelWonBeforeOutroTests`.

## Which call cleared ActiveUnit

Not confirmed. `ActiveAbility` was still set when the throw happened, which rules out `FactionPhaseData.Reinitialize` (`StartTurn`). `PlayerController.DeselectDeadActiveUnit` returns while `IsInProgress` is true, so it is ruled out too. That leaves an entry into UnitSelectionState while the action was in flight (base `SetObject(null)`, `FactionControllerBase.cs:420`). The paths that do this: `PlayerController.BeginReactiveSelection` (347), `RestoreAfterReactive` (355), `EnterReactiveTargetSelection` (472), which are reactive interrupt entry and exit, and `HandleGridCellSelection` (544). `ForceEndTurnSafe` waits on `CanEndTurn`, so it does not move the FSM mid-action. Pinning it down needs a Play-mode log.

## Needs THJ

none (play check below)

## Docs to update

- `tech/core-systems.md`, Faction controllers row, note text for the coordinator: "Since 2026-11-24 (D-657, D-660): an action that completes after the controller moved on no longer throws. `SetTakeActionState` captures the acting unit and ability at the start. A completion that arrives after the selection moved on (`IsSelectionStillOn` false) charges that unit through `ChargeUnitThatActed` (same cost override and free-use record) and skips the re-select. `TryTakeAction`'s delayed block then calls `TryFinishActionOutsideTakeAction`: if the controller already left TakeActionState, it clears `IsInProgress`, raises `abilityPerformed` once and calls `OnActionResolved`, without changing state or requesting turn end. New additive API (partial `FactionControllerBase.ActionCompletion.cs`): static `IsSelectionStillOn`, `ChargeUnitThatActed`, `LeftTakeActionBeforeCompletion`; protected `TryFinishActionOutsideTakeAction`; `FactionPhaseData.UpdateUnitActionPoints(GUnit, RuntimeAbility, int)`. Normal actions are unchanged. Also on `main` (list for the next merge)."
- `reports/console-errors-2026-11-24.md`, Error 1: fixed in two levels (the charge, then the state advance in `TryTakeAction`).

## Risks and loose ends

- If an ability ever calls its completion twice, the late path would charge twice. The old path would do the same; I found no evidence that any ability does this.
- On a late completion during a reactive interrupt, the late path charges AP. `PlayerController.ConsumeActionCost` would have charged FTP, because it reads the live `ActiveUnit`. This is an edge of an edge; the normal reactive path is unchanged.
- `abilityPerformed` listeners now also fire for a late completion; before, it was never raised. That is intended by the acceptance, but listeners that read the controller's live state see the new state.
- The GridToLevel builder tests flake in the full suite (editor prefab lock assert, a different test each run). They pass when run alone.

## Proposed commits

1. `fix(core): an ability's completion charges the unit that acted, even after the selection moved on` (core, alone):
   - `miso/Assets/_Project/Core/Interactions/Runtime/FactionControllerBase.cs`
   - `miso/Assets/_Project/Core/Interactions/Runtime/FactionPhaseState.cs`
   - `miso/Assets/_Project/Core/Interactions/Runtime/FactionControllerBase.ActionCompletion.cs` + `.meta`
   - `miso/Assets/_Project/Core/Interactions/Editor/ActionCompletionChargeTests.cs` + `.meta`
   - `miso/Assets/_Project/Core/Interactions/Editor/ActionCompletionGuardTests.cs` + `.meta`

## Other branches

`main` has the same bug. List it for the next merge.

## How to see it

1. Open Memory 3 (John) and play to the last enemy. Win with John's Shield Slam.
2. Watch the Console while the outro starts: no `NullReferenceException` (previously `FactionPhaseState.cs:73`), and nothing at `FactionControllerBase.cs:480`. The win panel follows as usual.
3. In any level, play a few normal actions and end the turn: AP drops exactly as before, and the next unit or turn follows as usual. If the Cyclone's free first Steer is on, it still costs nothing.
4. Optional: let an enemy turn run with AI actions. Turns hand over as before.
