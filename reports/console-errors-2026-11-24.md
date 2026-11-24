# Console errors from THJ's play check, 2026-11-24 (trace)

Branch `thj/onboarding-demo`. Read-only trace (Explore), written up by the coordinator. Editor.log lines: error 2 at 39782/39811/39840/39869 (Memory2Lucy), error 1 at 40061 (Memory3John). Neither comes from today's uncommitted changes (1.9 Cyclone, X-25, avatar).

## Error 1: NullReferenceException, `FactionPhaseState.cs:73` (core, old, from main)

- Line 73: `ActiveUnit.APConsumer.Consume(ActiveAbility.Parameters.apConsumptionType, count);`. `ActiveAbility` is read fine earlier in the same lambda, so `PhaseData.ActiveUnit` is null.
- `ActiveUnit` is cleared by `UnitSelectionState.SetObject(null)` (`FactionControllerBase.cs:420`, on every entry to UnitSelectionState), `FactionPhaseData.Reinitialize` (`FactionPhaseState.cs:55`, from `StartTurn`), or `PlayerController.DeselectDeadActiveUnit` (guarded, unlikely).
- Not the Cyclone cost override: `IAbilityCostOverride.cs:71` is the pass-through `consume?.Invoke(usualCount)` (no effect answered). Before `9c1cc7705` (2026-11-20) line 748 called `ConsumeActionCost` directly and would have thrown the same way. Line 73 dates from `08ef427c4` (2026-09-15).
- Log: Memory3John, John's Shield Slam wins the level; `EndLevel` → `PlayOutro` starts the outro (`@Memory3John_End_SequentialSequence`) while the slam is still finishing; the slam's completion arrives after the controller left TakeActionState → NRE. `EndLevel` doesn't wait for an in-flight action. Which call cleared `ActiveUnit` is not confirmed (candidates: TakeActionState `GetNextState` returning UnitSelectionState when `!IsTurnActive` after `IsInProgress` was cleared early, e.g. by a Family Role answer; `ForceEndTurnSafe`; an ATB-driven `StartTurn`).
- Harm: the completion chain stops at `FactionControllerBase.cs:748`: no AP charged, `onCompletion` never runs (`IsInProgress` stays true, `abilityPerformed` not raised), `RuntimeAbility.OnCompletionShared` cleanup skipped. Harmless at level end (scene unloads); the same race mid-level would soft-lock the turn (`CanEndTurn` false forever).
- Smallest fix (core: `FactionControllerBase.cs`, `FactionPhaseState.cs`): capture `ActiveUnit` and `ActiveAbility` as locals when the action starts in `SetTakeActionState`'s `ApplyAction`, and charge that unit in the completion lambda (consume overload taking unit + ability). Stopgap: null guard in `UpdateUnitActionPoints` (keeps the chain alive, AP lost).

## Error 2: "_queue data already exists", `EntityInfoPanelUI.cs:176` (not core, Khash's, from main)

- `PlayerInputController.cs:82`: ShowStats (Shift) `performed` → `toggleShowStats(true)`; no `ActiveCheckGuard`, so it fires in dialogs and sequences. Every GUnit listens (`GUnit.cs:318`) → `ShowInfoPanelGlobal` → its own panel's `Show`. Four identical errors = four units in the bad state at one press.
- `EntityInfoPanelUI.Show` keeps `_currentData` + one `_queueData`; priority Damage > FullDetail (hover) > Global (Shift). A lower-priority Show with a full queue logs this error and drops the request; `Hide(mode)` clears only a matching mode. Stuck queue from a stale hover (FullDetail queued behind a damage preview, hover-exit missed during a sequence) or a stale Global (Shift released without `canceled`).
- Log: all four right after `@Memory2Lucy_Interruption_SequentialSequence` ends. Code from `ef3c7a9066` (Khashayar, 2026-05-21).
- Harm: log noise; that unit's Shift overlay doesn't show for that press; panel state stays consistent.
- Smallest fix (not core): Global branch of `Show`: if the queue holds Global, refresh it; if FullDetail, return quietly. Optionally `Hide(Global)` also clears a current Global behind a queued FullDetail.
