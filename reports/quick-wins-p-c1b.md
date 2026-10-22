# Report: Quick wins P, C1b (no player input until the player's banner ends)

Plan: plans/2026-10-22-quick-wins-p-pace-tech.md (C1b, D-142)    Agent: miso-implementer    Branch: thj/quick-wins
Outcome: done (built with the coordinator's mid-task change: reuse the existing input lock, no new lock API)

## What changed

Uncommitted, on top of C1 (`5d1456ea3`). Line endings and BOM kept: all three are LF; `CombatLevelUIManager.cs` has a BOM, the other two don't.

- `miso/Assets/_Project/Core/UI/Runtime/CombatLevelUIManager.cs` (+29 / -2, core): `PlayPhaseAnimation` takes `PlayerInputController.AddInputLock(token)` for the player's faction, using a new `object` token per banner, and passes a finish callback to the banner that releases that token. New `ReleasePhaseBannerLock(object)`. `OnDestroy` also releases the current token. New field `_phaseBannerLock` (instance field, so no static reset is needed).
- `miso/Assets/_Project/Features/UI/Panels/Scripts/PhaseVisualsUI.cs` (+21 / -3, not core): `UpdateValues(name, color, Action onFinished = null)`, an optional additive parameter. A private `Finish()` sets `animationFinished` and calls the current banner's callback once. It is called on sequence complete, in `HideInstant`, in `UpdateValues` before a new banner replaces a running one, and in `OnDestroy`.
- `miso/Assets/_Project/Features/UI/Panels/Scripts/AbilitiesBarHUDUI.cs` (+3 / -0, not core): the ability button's `onClick` returns early while `PlayerInputController.Instance.IsInputLocked`. One check covers button clicks and number-key hotkeys, because hotkeys go through `buttons[index].Click()` → `onClick`.

A first version added a separate interaction-only lock (`AddInteractionLock` and its tests). The coordinator's change of approach came mid-task, so it was fully removed: `PlayerInputController.cs` and `InputLockSet.cs` were restored to HEAD (`git diff` is empty for both) and the new test file was deleted before Unity imported a `.meta` for it.

## Lock mechanism

- **Take:** in `PlayPhaseAnimation`, player faction only: `bannerLock = new object()`, then `AddInputLock(bannerLock)`, then `phaseVisualsUI.UpdateValues(..., () => ReleasePhaseBannerLock(bannerLock))` (`CombatLevelUIManager.cs:209-213`).
- **Release** happens through the banner's one-shot callback, on every way a banner ends:
  - completes: `_sequence.OnComplete(Finish)` (`PhaseVisualsUI.cs:102`)
  - `HideInstant` (HUD hide at level end): `PhaseVisualsUI.cs:91`
  - replaced by a new banner: `UpdateValues` kills the old sequence and calls `Finish()` before storing the new callback (`PhaseVisualsUI.cs:65-69`)
  - banner destroyed: `PhaseVisualsUI.OnDestroy` (`:59`)
  - UI manager destroyed: `CombatLevelUIManager.OnDestroy` releases `_phaseBannerLock` (`:394`)
- **Why a token per banner:** with a fixed owner, a player banner replacing a player banner would have its new lock released by the old banner's callback. With one token per banner, each callback releases only its own lock, whatever the order. `InputLockSet` is keyed by owner, so releasing twice or after the controller has gone is harmless.
- Enemy banners take no lock, so enemy turns behave as in C1.
- Effect: `ActiveActionMode` is `None` while the player's banner plays. Click, cancel, switch unit, toggle, cycle path, camera move/scroll/edge scroll and pause are all off; THJ accepted the camera being locked too. Hover, grid hover previews and the skip/ShowStats keys are not mode-gated and keep working.

## Grid-interaction paths (step 1 audit)

The existing input lock covers these, through `ActiveCheckGuard(ActionMode.Interact)` in `PlayerInputController.cs`:
- left click → `OnMouseClick` (`:58`) → `PlayerController.OnMouseClick` (`PlayerController.cs:116, 273`) → `HandleGridCellSelection` (`:520`): unit, cell and target selection and confirm
- right click → `OnCancel` (`:60`) → `PlayerController.OnCancelInput` (`:117, 186`)
- Switch (next unit) → `OnSwitch` (`:61`) → `SwitchSelectedUnit` (`:118, 482`)
- Toggle (`:62-63`), used by `UnitsCooperationHandler.cs:859` inside an ability
- CycleMovePath (`:66`) → `PlayerController.OnCycleMovePath` (`:119`)

Ability bar, which bypasses the input modes:
- `AbilitiesBarHUDUI.cs:131` `onClick`, shared by button clicks (`UnitAbilityButtonUI.Prepare` → `button.onClick`) and hotkeys 1-9 (`HandleShortcut`, `:312`, `buttons[index].Click()` `:324`). It did **not** respect the input lock. Fixed with the one-line check at `:136`.

Not gated (reported here, not changed):
- **Reactive interrupt key:** `PlayerInputController.cs:67` invokes `ReactiveInterrupt` with no mode guard and no lock check → `PlayerController.HandleReactiveInterrupt` (`:287`) → `TryEnterReactiveInterrupt`, which selects a unit and enters the Family Role targeting. It still works during the player's banner (and under the tutorial lock). The fix would be one line, `if (!IsInputLocked)`, but it sits in core `PlayerInputController` and would also change the tutorial-lock behaviour, so I left it for a decision.
- **End Turn button:** `PhaseControlPanelUI.cs:40` → `OnEndTurnPressed` → `ForceEndTurn` (`CombatLevelUIManager.cs:111`). It shows at the start of the player's turn (C1) and is not input-gated, so End Turn can be pressed during the banner. It is not a grid interaction; whether it should wait is THJ's call.
- **Pouch button and hotkey 0:** `AbilitiesBarHUDUI.cs:317`, `TogglePouch`. It opens or closes the item pouch only; picking an item goes through the gated `onClick`.
- **Shape rotation inputs:** `PlayerController.cs:149`. Preview only, and only in target selection, which the locked click path can't reach.
- **Programmatic selection:** `AutoSelectUnit` (`PlayerController.cs:472`), called from `StartTurn`. The turn still "technically begins" under the banner, so a unit is auto-selected and its bar shown, as THJ allowed.

## Acceptance criteria

- [x] During the player's banner, clicks on units and cells, ability buttons and hotkeys do nothing. Covered by code: the input lock gives `ActiveActionMode == None`, and the bar checks `IsInputLocked`. **Needs the play check.** Exception: the reactive interrupt key and End Turn (see above).
- [~] "...while the camera moves": superseded. THJ's change of approach accepts the camera being locked too.
- [x] Everything works the moment the banner ends: the lock is released in the sequence's `OnComplete`. **Play check.**
- [x] Enemy turns behave as in C1: enemy banners take no lock. **Play check.**
- [x] A level that ends or hides the HUD mid-banner leaves no lock behind: `HideInstant`, replacement, banner `OnDestroy` and UI manager `OnDestroy` all release. **Play check** (by code reading only).
- [x] Compiles clean (Unity MCP recompile, console has no `CS` errors; only the usual warnings). EditMode: 518 total, 517 passed, 1 failed: the known red `AIRegressionTest.Baseline_MatchesCurrentAI`.

No new EditMode tests. The remaining logic is the DOTween callback wiring in two MonoBehaviours with serialized UI references, which EditMode can't drive meaningfully. `InputLockSet` already has tests in `InputLockTests.cs`.

## Save reset

no

## Decisions I made

- Token-per-banner lock owner, released by a one-shot `onFinished` callback on `PhaseVisualsUI` (optional parameter, so it is additive).
- The ability bar check uses the existing `IsInputLocked` (one line, as the coordinator allowed). This also blocks ability clicks and hotkeys while a tutorial holds the lock, which matches what that lock is for.

## Needs THJ

1. Should the reactive interrupt key be blocked during the player's banner (and under the tutorial lock)? It would be a one-line guard in `PlayerInputController.cs:67` (core).
2. Should End Turn be blocked during the player's banner?

## Docs to update

- `tech/core-systems.md` (Combat UI manager row): the player's phase banner holds an input lock until it ends.
- `tech/combat-architecture.md` (turn switch): the player's input is locked for the banner's duration (about 1 s after C3).

## Risks and loose ends

- `EnemyIntroductionController.cs:93` saves `ActiveActionMode` and restores it at `:177`. Under the banner lock it saves `None`. That is harmless today: the player's `StartTurnWithIntroductions` sets `All` straight after (`PlayerController.cs:240-241`), and at that point the requested mode would not have included Interact anyway. Any future save/restore of `ActiveActionMode` under a lock would capture the masked value, not the requested one.
- Pause (Esc) is blocked for the banner's ~1 s, like the camera.
- The banner sequence runs on scaled time. If something sets the time scale to 0 mid-banner (tutorial, pause), the lock is held until time resumes. A tutorial holds its own lock anyway.

## Proposed commits

1. `feat(combat): no unit, ability or target picks until the player's turn banner has ended`: `CombatLevelUIManager.cs`, `PhaseVisualsUI.cs`, `AbilitiesBarHUDUI.cs` (core; one unit, since the three only work together).

## Other branches

`thj/home-test` gets it when it takes `main`, as with C1.

## How to see it

1. Open `CombatLevelContainerScene` (or a test level), enter Play and play the first player turn, then End Turn.
2. When the blue "... Turn" banner slides in after the enemy turn, try to click a unit or cell, click an ability button, press 1-9, right-click, and press the camera keys. Nothing should respond.
3. The moment the banner has slid out, all of those should work at once.
4. Watch an enemy turn: it starts and plays under the red banner as before.
5. Win or lose a level while a player banner is up (or use a cheat to end it). The banner disappears and the next level or retry has normal input.
6. Optional: press the reactive interrupt key and End Turn during the blue banner to see the two open items above.

## Follow-up: End Turn

THJ decision: the End Turn button is also locked during the player's turn banner.

- File: `miso/Assets/_Project/Core/UI/Runtime/PhaseControlPanelUI.cs` (LF, no BOM, kept as is). Added `using MISO.Core.Interactions;` (line 4) and turned the `endTurnButton` listener in `Awake` into a block that returns early while `PlayerInputController.Instance` exists and `IsInputLocked` is true (lines ~41-47), then invokes `OnEndTurnPressed`. Comment is in plain words, matching the abilities bar check.
- Side effect: the lock is the shared one the banner and tutorials hold, so End Turn is also blocked behind an open tutorial.
- `ForceEndTurn` has no other entry point (only `CombatLevelUIManager` subscribes `OnEndTurnPressed`).
- Compile: refreshed via Unity MCP, console shows 0 errors.
- EditMode: 518 total, 517 passed, 1 failed = the known red `AIRegressionTest.Baseline_MatchesCurrentAI` (untouched).
- Not verified: Play check (no Play mode entered). Nothing staged or committed.
