# Report: Ability completion charges the unit that acted (core bugfix)

Plan: plans/2026-11-24-ability-completion-charge-fix.md    Agent: miso-implementer    Branch: thj/onboarding-demo
Outcome: blocked (the charge fix is built and tested, but the completion chain still breaks one step later, in turn flow. The plan says to stop there.)

## What changed

- `miso/Assets/_Project/Core/Interactions/Runtime/FactionControllerBase.cs` (core, LF + BOM kept): `SetTakeActionState`'s `ApplyAction` now captures `actingUnit` / `actingAbility` when the action starts. In the completion lambda, after un-targeting cells, a new check runs: if the selection no longer holds that unit and ability, it charges the captured unit (`ChargeAfterSelectionMoved`), calls `onCompletion` and returns. Otherwise the old code runs as before. The AP-count expression moved, unchanged, into `ActionAPCount(unit, ability)`, which this path calls with `PhaseData.ActiveUnit` / `ActiveAbility`.
- `miso/Assets/_Project/Core/Interactions/Runtime/FactionPhaseState.cs` (core, LF + BOM kept): new additive overload `FactionPhaseData.UpdateUnitActionPoints(GUnit unit, RuntimeAbility ability, int count)`. The existing `UpdateUnitActionPoints(int)` is untouched.
- `miso/Assets/_Project/Core/Interactions/Runtime/FactionControllerBase.ActionCompletion.cs` (+ `.meta`, new partial):
  - `public static bool IsSelectionStillOn(GUnit selectedUnit, RuntimeAbility selectedAbility, GUnit actingUnit, RuntimeAbility actingAbility)`: true when both match by reference.
  - `public static bool ChargeUnitThatActed(FactionPhaseData, GUnit, RuntimeAbility, int usualCount)`: goes through `AbilityCostOverride.Charge` with the given-unit consume and that unit's `RecordFreeConsumption`. Returns false and charges nothing if the unit is destroyed, the unit has no APConsumer, or there is no ability.
  - `private ChargeAfterSelectionMoved` (try/catch + `Debug.LogException`, so a late charge never stops the chain) and `private ActionAPCount`.
- `miso/Assets/_Project/Core/Interactions/Editor/ActionCompletionChargeTests.cs` (+ `.meta`, new): 8 EditMode tests.
- Not changed: `ConsumeActionCost(int)` (still virtual; `PlayerController`'s reactive-interrupt override still runs for every normal action), turn flow, `EndLevel`, `PlayerController`, `AIController`.

## Acceptance criteria

- [ ] A late completion charges the unit that acted, raises no exception, and runs its chain to the end. **Partly met.** The charge now goes to the unit that acted and line 73 no longer throws. `RuntimeAbility.OnCompletionShared` is not blocked by our lambda any more. But `onCompletion` (`TryTakeAction`'s delayed block) then throws, so `abilityPerformed` is still not raised. See Needs THJ.
- [x] Normal actions charge exactly as before (same AP, same free-cost override including the Cyclone's free Steer). When the selection still holds the acting unit and ability (every normal action), the lambda runs the old code: the same `ConsumeActionCost` virtual, the same `ActiveUnit` free record, the same AP-count expression (moved into a method). Covering fixtures pass: `MISO.Core.Interactions.EditorTests`, `AbilityCostOverrideTests` and `CycloneSteerTests` (all partials), 218/218.
- [x] EditMode tests for both cases: `ActionCompletionChargeTests`, 8/8 pass.
- [x] Full EditMode suite: 2630 total, 2620 passed, 9 failed, 1 skipped (the Explicit AI regression test). The failures: the 8 expected `M1RidgeTests`, plus `GridToLevelCameraStartTests.Build_CameraLinePutsTheViewOnThatTile` (unhandled editor assert `m_LockCount == 0` from `PrefabUtility.UnloadPrefabContents`). That fixture passes 17/17 on a rerun alone; it is flaky and has nothing to do with this change.
- AI regression (run by name, because AI controllers share this completion lambda): `Baseline_MatchesCurrentAI` gives CHECKS 731, FAILURES 44, the same as the last recorded 44.

## Chunks

### Chunk 1: completion charges the captured unit

- Changed: the 3 runtime files and the test file above, plus 2 `.meta` files.
- Criteria met: normal charge unchanged (covering fixtures 218/218); late charge goes to the unit that acted (tests); full suite clean apart from the expected and flaky failures; AI regression at 44.
- Decisions and loose ends: blocked on the turn-flow step below.

## Why it is blocked (file:line)

With the charge fixed, the chain gets past `FactionControllerBase.cs:~748` and calls `onCompletion`, which is `TryTakeAction`'s delayed block (`FactionControllerBase.cs:1018-1040`):

- 1021: `PhaseData.IsInProgress = false;` now runs, so the turn no longer soft-locks on `CanEndTurn`.
- 1022: `var nextState = CurrentPhaseState.GetNextState();`. This assumes the controller is still in TakeActionState. In the logged case it is already in UnitSelectionState: `ActiveUnit` is null while `ActiveAbility` is set, and only UnitSelectionState's `SetObject(null)` clears it that way. `UnitSelectionState.GetNextState` returns ActionSelectionState, so `SetNextPhaseState(ActionSelectionState)` → `EnterState` → `ActionSelectionState.SetObject(null, true)`. That throws at 480 (`PhaseData.ActiveUnit.DefaultEmptyCellAbility`, ActiveUnit null), and `abilityPerformed` (1030) and `OnActionResolved` never run.
- If another unit was selected meanwhile (not null), the block would instead advance or hijack that new selection's FSM.

So the bug was two deep. Fixing the second level means a guard in `TryTakeAction`'s delayed block, which is turn flow and beyond the completion charge. I stopped there, as the plan says.

## Which call cleared ActiveUnit

Not confirmed. What the code narrows it to:

- `ActiveAbility` was still set when the throw happened, so `FactionPhaseData.Reinitialize` (`StartTurn`) is ruled out: it clears both.
- `PlayerController.DeselectDeadActiveUnit` is ruled out too: it returns while `IsInProgress` is true.
- That leaves an entry into UnitSelectionState while the action was in flight (base `SetObject(null)`, `FactionControllerBase.cs:420`). The paths that do this are `PlayerController.BeginReactiveSelection` (347), `RestoreAfterReactive` (355) and `EnterReactiveTargetSelection` (472), which are reactive interrupt entry and exit, and `HandleGridCellSelection` (544).
- `CombatLevelRunHandler.UpdateObjectives` → `ForceEndTurnSafe` waits on `CanEndTurn`, so it does not move the FSM while `IsInProgress` is true.
- Most likely: a reactive interrupt toggle during the slam, or an `IsInProgress` cleared early by another flow (the trace's Family Role candidate). Pinning it down needs a Play-mode log.

## Reviews and checks

- (coordinator)

## Save reset

no

## Decisions I made

- "Selection moved on" means the selected unit **or** ability differs from the ones captured at the start. Normal actions therefore take the old code path, including `PlayerController`'s virtual `ConsumeActionCost(int)` override.
- The late path skips `SetPotentiallyTargetedCells(false)` and the re-select or cleanup block. Both read the live selection, which belongs to whatever the controller is doing now.
- The AP-count expression moved, unchanged, into a private `ActionAPCount(unit, ability)` so both paths use one formula.
- The late charge is wrapped in try/catch + `Debug.LogException`, so a late charge can never stop the chain.

## Needs THJ

1. **What:** the late completion also needs a guard in `TryTakeAction`'s delayed block (turn flow), or the chain still throws after the charge.
2. **Why:** acceptance asks for `abilityPerformed` and the whole chain on a late completion. With only the charge fixed, the next step (`CurrentPhaseState.GetNextState()` at 1022) advances a controller that already moved on and throws at 480.
3. **Options:**
   - A (recommended): in the delayed block, if `CurrentPhaseState != TakeActionState`, clear `IsInProgress`, raise `abilityPerformed`, call `OnActionResolved` and return, without advancing the FSM or requesting turn end. That is about 4 lines; normal actions are untouched because they are always in TakeActionState there.
   - B: commit only the charge fix as it is. Line 73 is gone and `IsInProgress` now clears (no soft-lock on `CanEndTurn`), but an NRE remains at 480 and `abilityPerformed` is lost.
   - C: also null-guard `ActionSelectionState.SetObject`. That is more turn-flow surface and hides the real cause; not recommended.
4. **Recommendation:** A, in the same core commit.
5. **Impact:** A touches `TryTakeAction`, which every faction controller (player and AI) runs. Rerun the covering fixtures, the full suite and the AI regression after it.

## Docs to update

- `tech/core-systems.md`, Faction controllers row, note text for the coordinator: "Since 2026-11-24 (D-657): `SetTakeActionState` captures the acting unit and ability when an action starts. A completion that arrives after the selection moved on (`IsSelectionStillOn` false) charges that unit through `ChargeUnitThatActed` (same cost override and free-use record) and skips the re-select. New additive API: `FactionPhaseData.UpdateUnitActionPoints(GUnit, RuntimeAbility, int)`, static `FactionControllerBase.IsSelectionStillOn` and `ChargeUnitThatActed` (partial `FactionControllerBase.ActionCompletion.cs`). Normal actions are unchanged." Add the `TryTakeAction` guard line if option A lands.
- `reports/console-errors-2026-11-24.md`, Error 1: the fix is two-level (charge, then the FSM advance in `TryTakeAction`).

## Risks and loose ends

- If an ability ever calls its completion twice, the late path would charge twice. The old path would do the same; I found no evidence that any ability does this.
- On a late completion during a reactive interrupt, the late path charges AP. `PlayerController.ConsumeActionCost` would have charged FTP instead, because it reads the live `ActiveUnit`. This is an edge of an edge; the normal reactive path is unchanged.
- `GridToLevelCameraStartTests.Build_CameraLinePutsTheViewOnThatTile` is flaky in the full suite (editor prefab lock assert).

## Proposed commits

1. `fix(core): an ability's completion charges the unit that acted, even after the selection moved on`: `Core/Interactions/Runtime/FactionControllerBase.cs`, `Core/Interactions/Runtime/FactionPhaseState.cs`, `Core/Interactions/Runtime/FactionControllerBase.ActionCompletion.cs` + `.meta`, `Core/Interactions/Editor/ActionCompletionChargeTests.cs` + `.meta` (core). Hold it until the decision above; with option A, the guard joins this commit.

## Other branches

`main` has the same bug. List it for the next merge.

## How to see it

1. After the decision (and option A if chosen): open Memory 3 (John), play to the final enemy and win with John's Shield Slam.
2. Watch the Console while the outro starts: no `NullReferenceException` at `FactionPhaseState.cs:73` or `FactionControllerBase.cs:480`.
3. Mid-level, play a few normal actions, including Lucy's Cyclone Steer if its free first Steer is on: AP drops exactly as before.
