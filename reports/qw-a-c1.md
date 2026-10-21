# Report: Quick wins A, C1: one-click right-click cancel (Q9)

Plan: plans/2026-10-21-quick-wins-a-tech.md (C1)    Agent: miso-implementer    Branch: thj/quick-wins
Outcome: done (code written; not compiled or tested here, see below)

## What changed

- `miso/Assets/_Project/Core/Interactions/Runtime/PlayerController.cs` (core, private only): the cancel subscription in `Start()` now uses a named `OnCancelInput()` handler instead of the `() => GoBackToPreviousState()` lambda; `OnDestroy()` unsubscribes it. `OnCancelInput()` returns early if `PhaseData` is null, asks `CancelInputRules` whether it is blocked, then either steps back once (in `TargetSelectionState` with `TargetCells.Count > 0`: undo the last pick) or runs `while (GoBackToPreviousState()) ;` (full deselect to `UnitSelectionState`). No public API change. CRLF, no BOM, kept.
- `miso/Assets/_Project/Core/Interactions/Runtime/CancelInputRules.cs` (+ `.meta`, new): pure static helper with no state. `IsBlocked(introductionInProgress, qteActive, actionInProgress, reactiveInterrupt, otherFactionActing)` and `Decide(blocked, pickingWithTargets) -> None | StepOnce | ToUnitSelection`, plus the `CancelInputAction` enum. CRLF, no BOM (same as `ShiftPreviewRules.cs`).
- `miso/Assets/_Project/Core/Interactions/Editor/CancelInputRulesTests.cs` (+ `.meta`, new): 10 EditMode tests, namespace `MISO.Core.Interactions.EditorTests` (same as the other Interactions tests). CRLF + BOM (same as its neighbours).

## Acceptance criteria

- [ ] Q9, ability armed, one right-click returns to unit selection with no range shown: by reading. From `TargetSelectionState` with no picks, the loop steps Target to Action (its cancel runs `ActionSelectionState.Cleanup`, which clears the range) to Unit (`ActionSelectionState.CancelAction` runs `UnitSelectionState.Cleanup`: cell deselected, range cleared, `unitSelectionChanged(null)`), then `UnitSelectionState.GetPreviousState` is null and the loop stops. Decision rule covered by `Decide_NotBlocked_NoTargetsPicked_GoesToUnitSelection`. Needs the play check.
- [ ] Q9, during multishot picking a right-click removes the last picked target: by reading, one `GoBackToPreviousState()`; covered by `Decide_NotBlocked_TargetsPicked_StepsOnce`. Needs the play check.
- [ ] Q9, right-click does nothing during a QTE, a Family Role prompt, the level intro, or while another faction acts: covered by the `IsBlocked_*` tests. A Family Role prompt is covered twice: `ActivateFactionRole` sets `PhaseData.IsInProgress = true` for the whole role, and the prompt itself is a QTE (`QuickTimeEventHandler.IsEventActive`). Needs the play check.
- [ ] Compile clean; EditMode suite green except `AIRegressionTest.Baseline_MatchesCurrentAI`: Not run. The Unity MCP was not connected and the editor is open (so no command-line run). THJ: Ctrl+R, then Test Runner > EditMode > Run All.

Checked by reading, as the plan asked:
- Reactive interrupt: `TargetSelectionState.GetPreviousState` (PlayerController, `SetTargetSelectionState`) maps Action to Unit while `_reactiveInterrupt`; the full deselect still ends at `UnitSelectionState`. The other-faction check is skipped in a reactive interrupt, as in `HandleGridCellSelection`, so cancel still works while the enemy's action is frozen.
- Approach attack: `TryQueueApproachAttack` sets the pending fields only right after a successful `Apply` that moves straight on to `TakeActionState` and `TryTakeAction`; they are consumed in `OnActionResolved`. There is no cancel window in which they are set and the player is in a cancellable state.
- `TakeActionState.CancelCondition = () => false`: `GoBackToPreviousState()` returns false at once, so mid-action cancel stays a no-op (and `PhaseData.IsInProgress` blocks it first anyway).

## Save reset

no

## Decisions I made

- Tier 1: split the helper into `IsBlocked(...)` and `Decide(blocked, pickingWithTargets)` instead of only `Decide`, so the guard set (including the reactive-interrupt exception) is tested too. Same behaviour as the plan.
- Tier 1: the guard passes `!_reactiveInterrupt && OtherFactionActionInProgress()` as `otherFactionActing`, so `OtherFactionActionInProgress()` is not called during a reactive interrupt (short-circuit, same as `HandleGridCellSelection`). `IsBlocked` applies the reactive exception again, which is redundant but harmless.
- Tier 1: added `if (PhaseData == null) return;` before the guard, because the new handler reads `PhaseData` and the old lambda did not. Before initialization the old handler was a no-op too (`CurrentPhaseState` null), so behaviour is unchanged.
- Tier 1: wrote the two `.meta` files by hand (new GUIDs) so they go in the commit with their scripts.

## Needs THJ

none

## Docs to update

- `tech/combat-architecture.md`: cancel input. A right-click undoes the last picked target while targets are picked, otherwise it fully deselects to unit selection. It is blocked during the level intro, a QTE or Family Role prompt, the faction's own action, and while another faction acts (except in a reactive interrupt). The rule is in `CancelInputRules`.
- `build-log.md`, `status.md`: coordinator.

## Risks and loose ends

- Not compiled here. The code uses only members already in scope in `PlayerController` (`PhaseData`, `CurrentPhaseState`, `TargetSelectionState`, `IntroductionInProgress`, `OtherFactionActionInProgress`, `QuickTimeEventHandler.IsEventActive`, all in namespace `MISO.Core.Interactions`). No name clashes for `CancelInputRules`, `CancelInputAction` or `OnCancelInput` elsewhere under `Assets`.
- Play mode: Editor.log showed the last Play session had ended (the scene backup was reloaded after it), so the editor looked stopped when I edited. I could not confirm this from inside the editor.
- Existing behaviour, unchanged: undoing the only picked target of a multi-target ability lands in `ActionSelectionState`, because `TargetSelectionState.GetPreviousState` is read after the pick is removed. The ability is then no longer armed (unit still selected, move range shown). That matches "one step back" and D-130's "undo the last target", but it may read as "the ability disarmed" in play. If THJ wants it to stay armed with 0 picks, that is a separate change to the state machine.
- Existing, not touched: the other `Start()` subscriptions (`OnMouseClick`, the `OnSwitch` lambda, `ReactiveInterrupt`) are still never unsubscribed in `OnDestroy()`. Only cancel was in scope.
- `AIRegressionTest`: not affected (nothing here is read by the AI).

## Proposed commits

1. `fix(input): one right-click deselects fully, or undoes the last picked target`: `miso/Assets/_Project/Core/Interactions/Runtime/PlayerController.cs`, `miso/Assets/_Project/Core/Interactions/Runtime/CancelInputRules.cs`, `miso/Assets/_Project/Core/Interactions/Runtime/CancelInputRules.cs.meta`, `miso/Assets/_Project/Core/Interactions/Editor/CancelInputRulesTests.cs`, `miso/Assets/_Project/Core/Interactions/Editor/CancelInputRulesTests.cs.meta` (core: faction controller, private behaviour only). The tests go in the same commit because they only build with the helper.

## Other branches

`thj/home-test` gets this when it takes `main` (per the plan).

## How to see it

1. Ctrl+R, then Test Runner > EditMode > Run All. `CancelInputRulesTests` (10 tests) should be green, and only `AIRegressionTest.Baseline_MatchesCurrentAI` red.
2. Play any combat level. Select a Bergson (move range shows) and right-click: the unit is deselected and no range shows.
3. Select a unit, arm an ability (e.g. John's attack) so its range shows, and right-click once: back to unit selection, no unit selected, no range.
4. Select Lucy, arm her Primary Attack (multishot), and pick two targets. Right-click: the last target is removed and the counter drops by one. Right-click again: the first pick is removed (you land with Lucy selected and her move range shown). Right-click again: fully deselected.
5. Trigger a Family Role prompt and right-click while the prompt is up: nothing changes. Right-click during the level intro, and while an enemy is acting on its turn: nothing changes.
6. In a reactive interrupt (if the point mode allows one), pick a role target and right-click: back to unit selection.

## Rev 1 (after review)

- `PlayerController.cs`, `OnCancelInput()`: `otherFactionActing` is now `OtherFactionActionInProgress()` unmasked, so `CancelInputRules.IsBlocked` alone owns the reactive-interrupt exception and the tested rule is the one in effect. `OtherFactionActionInProgress()` is read-only, so calling it during a reactive interrupt has no side effects. This replaces the second Tier 1 note under "Decisions I made". Line endings unchanged (CRLF, no BOM). Still not compiled here; the commit proposal is unchanged.
