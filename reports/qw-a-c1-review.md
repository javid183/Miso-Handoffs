# Review: quick wins C1 (one-click cancel)

Reviewer: miso-reviewer (read-only; saved by the coordinator)    Branch: thj/quick-wins    Date: 2026-10-21
Verdict: **APPROVE**

## Must fix

None.

## Should fix

1. `PlayerController.cs:189` passes `!_reactiveInterrupt && OtherFactionActionInProgress()` as `otherFactionActing`, and `CancelInputRules.IsBlocked` applies the reactive-interrupt exception again, so the helper's exception (and `IsBlocked_OtherFactionActingDuringReactiveInterrupt_NotBlocked`) never changes the outcome at the call site. Pass `OtherFactionActionInProgress()` unmasked and let the helper own the exception. Same behaviour either way.

## Notes

- Compile (by reading): only existing `PlayerController` members are used; `QuickTimeEventHandler.IsEventActive` is public static; the test namespace `MISO.Core.Interactions.EditorTests` resolves the types; `CancelInputRules` is public. Not compiled yet.
- Guards match `HandleGridCellSelection` (intro, other faction acting with the reactive exception); the QTE and `PhaseData.IsInProgress` checks are stricter, as planned. Uses `PhaseData.IsInProgress`, not `isActionInProgress` (which would block every cancel in a reactive interrupt). Cancel during the revenge sequence is still allowed, as before.
- The deselect loop ends: picks strictly fall in TargetSelection, then Action → Unit, Unit's previous is null; `TakeActionState.CancelCondition` is false.
- Reactive interrupt: Action → Unit override, so the deselect ends at UnitSelection; once the role fires, IsInProgress and the QTE block cancel.
- Approach attack: no cancellable window with the pending fields set.
- Subscriptions symmetric (Start once, OnDestroy with a Unity null check). No statics, no AI or serialization changes, no private IDs. Line endings and BOM match neighbours. `.meta` GUIDs unique.
- One commit is right (core change; helper and tests only make sense with it).
- Undoing the only picked target lands in ActionSelection (ability disarmed, move range shown): **existing behaviour, not a regression**; D-130 is met. Lucy with 2 picks takes 3 right-clicks to fully deselect. Keeping the ability armed at 0 picks would change `TargetSelectionState.GetPreviousState`, shared core state-machine behaviour the AI controller also uses: its own decision, not C1. Judge in the play check.
- The reversion QTE block has no effect today (`enableActionReversion: 0`).
