# Acting twice when playing fast (X-43, chunk 1.13) and move tiles during a move (X-49, chunk 1.16): code findings

Read-only Explore sweep, 2026-11-27, `main`. Nothing edited, nothing checked in play. **Parked by THJ (D-784): "more design issue than tech; should be discussed."** Kept here for that discussion. Paths under `miso/Assets/_Project/`.

## How input flows today

- No input lock while an action resolves. `PlayerInputController.ActiveCheckGuard` (`Core/Interactions/Runtime/PlayerInputController.cs:87-91`) checks only interaction mode (All from turn start, `PlayerController.cs:234`, to EndTurn `:256`) and the lock set (banner, tutorial, mission end, Cyclone Whirl). The click is handled at end of frame (`PlayerController.cs:276-289`), so gating belongs at handling time.
- Click handlers (`HandleGridCellSelection` `PlayerController.cs:527-640`, `TryGivePlantedEntityClick`, `HandleAbilitySelection` `:676-696`) check only `IntroductionInProgress` and `OtherFactionActionInProgress()`, never this controller's own busy flag. In TakeActionState the click falls through to `TryTakeAction()` (`:639`).
- Action lifecycle (`FactionControllerBase.cs:1008-1050`): `TryTakeAction` refuses if `PhaseData.IsInProgress` (`:1010`); after completion a 0.5 s hold (`holdTimeAfterActionCompletion`, `PlayerController.prefab:202`), then in one frame: flag cleared (fires `ActionsProgressComplete`) → next state → auto-select → `abilityPerformed` → `OnActionResolved`. Clicks during the action and hold are dropped silently, no feedback.
- Selection after an action: unit with AP left stays selected; at 0 AP, `AutoSelectUnit` picks a **random** unit (`PlayerController.cs:478-487`).
- "Auto-move/auto-attack": the basic attack's approach (walk then attack; `TryQueueApproachAttack` `:1376-1399`, `OnActionResolved` `:1353-1374` queues the attack with no busy check), and Mark's Continuous Attack `autoAttackNextTarget`.

## Likely causes, most likely first

1. **Parked action (confirmed path, frequency unverified).** `ActivateFactionRole` sets `PhaseData.IsInProgress = true` without a state change (`PlayerController.cs:1591-1596`); roles start from the event bus (incl. on `abilityPerformed`) and from `ActionsProgressComplete`. If one starts between a walk's completion and its queued attack, `TryTakeAction` is refused and the controller stays in TakeActionState with unit A's attack armed. The next click anywhere (e.g. on unit B) reaches `:639` and fires **A's** attack. Same during any role prompt or Super Time: a confirm click parks an action, a later click fires it. During revenge (`_revengeInProgress`, not in `IsInProgress`) actions aren't even refused.
2. **QTE prompts share the left mouse button with the board** (`InputSystem_Actions.inputactions`: Interact, MarkQTE, JohnQTE, LindaQTE, LucyQTE, GenQTE all `<Mouse>/leftButton`). Mark's Continuous Attack prompt (TimedPress, any press succeeds, 1 s) swallows a fast click meant for the next unit, and Mark swings again on his own; that follow-up is in no busy flag. THJ: keep QTE clicks as they are (D-785).
3. **"Unclear whose turn it is":** during the action and the 0.5 s hold no selection change is raised; the ring stays on A, then tweens at 12 u/s to a random next unit; its move range shows only after the hold; clicks in the hold vanish, so players click again.

## Move tiles (X-49)

Drawn on entering ActionSelection with no ability (`FactionControllerBase.cs:476-487`, adds a `GridPlugStateChange` listener `:485`); cleared at action start (`:776` → `:532`, plus `PlayerController.cs:1229-1245`); shown again after completion + hold. A normal ordered walk already hides them. Hypothesis: `GridPlugStateChange` (`:1065-1070`) redraws the range on every plug/unplug (each tile step, `GridCell.cs:798,827`) while ActionSelection is idle, so any move outside the state machine (role, scripted `MoveUnitSequence`/`MoveGroupUnitSequence`, enemy answer, push, swap) redraws the green tiles step by step. Needs THJ to say where he saw it.

## Fix shape proposed (not approved)

One busy rule (`PlayerController.isActionInProgress`, or extend `CancelInputRules.IsBlocked`) gating board, ability and pouch clicks while an action, role, Super Time or hold resolves (reactive-interrupt clicks kept); a refused `TryTakeAction` never stays parked; skip the move-range redraw while busy and redraw on `ActionsProgressComplete`. Options shown to THJ also included a fixed next-unit order instead of random and no hold before the ring moves. Core files: `FactionControllerBase.cs`, `FactionPhaseState.cs`, `PlayerController.cs` (+ partials), `PlayerInputController.cs`, `GridCell.cs`.

## Test ideas

Pure click rule test (like `CancelInputRulesTests`); parked-action test in the style of `ActionCompletionGuardTests.cs` (TakeActionState + `IsInProgress` true → `TryTakeAction` → clear flag → assert nothing stays armed; fails today); an input-binding test if QTE keys ever change.
