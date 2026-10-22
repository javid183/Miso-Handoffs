# Review: quick wins bundle P, C1c (turn-start pause after an automatic turn end)

Reviewer: miso-reviewer (read-only; saved by the coordinator from its hand-back), 2026-10-22.
Plan: `plans/2026-10-22-quick-wins-p-pace-tech.md` C1c (D-143). Implementer report: `reports/quick-wins-p-c1c.md`.

**Verdict: APPROVE.** No must-fix items.

## Should fix (dev tool only; can wait)

1. `Core/Interactions/Runtime/AIController.cs:169`: `AIController.RequestEndTurn` overrides without calling base (it forwards through `GuardedRequestEndTurnIE` → `OnEndTurnRequested`), so `TurnEndedByButton` is never set for an AIController. Matters only when the player faction runs `AutoPlayerController.prefab` (AIController with `autoPlayer: 1`): End Turn then still gets the 0.5 s pause. The flag can't go stale (base `StartTurn`/`EndTurn` clear it). Fix: a protected `MarkEndRequestFromButton()` on the base, called from base `RequestEndTurn` and from the AI override after its `IsTurnActive` check.

## Notes

- **Button path traced:** `PhaseControlPanelUI` (input-lock gate) → `OnEndTurnPressed` → `EndTurnFromButton` (pending, cleared in `finally`) → `ForceEndTurn` → `GoBackToPreviousState` loop → `UnitSelectionState` check → `PlayerController.RequestEndTurn` (returns early during introductions: no mark; else base) → base sets the flag only when `IsTurnActive` → `OnEndTurnRequested` → `TrySwitchTurn` → `SwitchTurnIE` reads it after the `WaitWhile`, before `EndTurn()`. All `StartTurn`/`EndTurn` overrides call base.
- **Stale/misread:** an auto end already waiting when End Turn is pressed skips the pause (acceptable). Scripted `CancelTurnActiveSwitch` → `Reset` → `RestartTurn` → `StartTurn` clears it; `EndCurrentPhase` leaves it set (that scripted end also skips the pause; harmless). Restart and level end clear it. Skipped factions: the pause is the next playable faction's, with the ended faction's flag. `_lockTurnIndex`: the same faction's own pause.
- **Placement:** after the gap and the existing `_levelEnded`/`CanPlayTurn` break; `_levelEnded` re-checked; `finally` resets `_turnSwitchInProgress`. Turn-switch holds are only checked before `EndTurn`, so a hold added during gap or pause isn't respected (pre-existing for the gap; the window is longer now). A cancel during the pause behaves like a cancel during the gap today.
- **Player pause > 0 (not the case now):** the player couldn't act during it (`PlayerController.EndTurn` leaves Camera|Pause; `RequestEndTurn` refuses; the banner lock starts after the pause). Pause menu and camera would work.
- **Conventions:** no rename or save impact; `[Min(0f)]`; plain tooltip; prefab line in declaration order; `PlayerController.prefab` and `AutoPlayerController.prefab` use the default 0; no statics; nothing the AI thread reads changed; line endings fine; test file BOM, namespace and folder match neighbours.
- **Tests** cover the pure decision incl. the clamp; the flag lifecycle is left to THJ's play check (per plan).
- **One core commit** is right. Docs to update: `tech/core-systems.md`, `tech/combat-architecture.md` (new `FactionControllerBase` members, End Turn → `EndTurnFromButton`, `SwitchTurnIE` order).
- **C3:** the prefab line sits next to C3's `holdTimeAfterActionCompletion` edit (`AIController.prefab:47`); check whichever lands second.
