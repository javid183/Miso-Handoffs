# B4 · Shift, role icon and cell highlights: facts from code

Read-only Explore pass, 2026-10-18, branch `thj/oct-build-fixes` (= `main`). Condensed by the coordinator. Paths under `miso/Assets/`. Input for the designer (C) and for chunk R3.

## Shift (ShowStats)

- Action `ShowStats` (Button), bound only to `<Keyboard>/shift` (either Shift key) in `Settings/Input/InputSystem_Actions.inputactions` (~L127, L464). Wired in `_Project/Core/Interactions/Runtime/PlayerInputController.cs` L71-72: `performed` raises `GlobalEventBus.toggleShowStats(true)`, `canceled` raises false. **Hold**, not toggle.
- **Not gated:** no `ActiveCheckGuard`, no `ActionMode` flag. It fires during enemy turns, QTEs, cutscenes, input locks and with mode `None`.
- Two listeners while held: (1) every initialized living unit, player and enemy, shows its world-space `EntityInfoPanelUI` (HP, tags with remaining turns, AP consumer for players) via `GUnit.cs` L314/433/464-484; hover and ability-preview modes override it; (2) `Core/Interactions/Runtime/ShowStatsHoverPreview.cs` (in `CombatLevelContainerScene`): for the **hovered** unit it highlights move-reachable cells (`SetHighlight(true, isMove: true)`), attackable cells (`SetInAttackRange(true)`) and its queued future-action targets; cleared on release or unhover; skipped while the player is choosing an ability target.
- Role zone is not part of any Shift behaviour.
- **Suspected bug:** `ShowStatsHoverPreview.cs` L28 `WaitUntil(() => GlobalEventBus.Instance == null && guard-- > 0)` waits for the bus to be null, so it likely never subscribes when the bus exists: the hover range preview may be dead. Verify in play.
- Shift is used by nothing else in combat bindings (dev cheats use it as a modifier in `CheatHandler.cs`).

## Role icon on the unit panel

- `UnitPanelUI.SetupFamilyRole` (`Features/UI/Panels/Scripts/UnitPanelUI.cs` L235-287), called from `PopulateUnitControlPanel` (L126). Icon `familyRoleImage`, hover relay `familyRoleHover`. Shown only for the **selected** unit and only if the unit has a `FactionRoleHandlerBase` and the role ability has an icon.
- Hover shows the tooltip (role ability title and description) and lights the cells from the handler's `GetCellsInRange()` with `GridCell.SetInAttackRange(true)` (default in-attack-range icon, no tween). Hover exit clears them. `ClearUnitControlPanel` (L361) does **not** clear lit cells, so if the panel repopulates or hides while hovered the cells stay lit (same stale-hover issue that `ClearItemPreview` handles for items).
- Zones: John `GetRangeCells(radius)` (Adjacent diamond), Mark `GetRangeCells` (straight only if the ability is), Lucy every cell within radius by footprint distance, Linda cells within radius sharing a row or column, Masher Goblin attack cells from its own cell and every cell its walk reaches. The base `GetCellsInRange` throws `NotImplementedException`.

## Cell highlight system

- `Core/Systems/GridSystem/Runtime/GridCell.cs`: separate `SpriteRenderer` layers (L70-81), toggled in `UpdateVisuals` (L436-452): Move (`SetHighlight(true, isMove: true)`), Ability (`SetHighlight(true)`, tinted by level), Targeted / PotentiallyTargeted, In-attack-range icon (`SetInAttackRange(bool, Sprite overrideSprite = null)`, L380-405), Warning, Hover. Cells inside a multi-cell occupant's footprint redirect through `OverlayOrigin`.
- **Clash risk:** `SetInAttackRange` is a plain bool, not ref-counted. Writers: role icon hover (UnitPanelUI L266, L280), Shift hover preview (L96, L110), ability hover AoE (PlayerController L1017, L1028, L1133), John+Linda cooperation (UnitsCooperationHandler L1427, L1439). Whoever clears first erases the others. A role zone drawn on this layer would also look identical to an attack or AoE preview. **A new `GridCell` layer (own sprite) is needed for an always-on role zone**, and a null-safe guard for units off the grid.

## Keys

- Used (Player map): W A S D and arrows (camera), Tab (Switch), Space (CycleMovePath, SkipDialogue, SkipLine), Esc (Pause), Shift (ShowStats), **Alt (Toggle: the John/Linda direction toggle, `UnitsCooperationHandler.cs` L859/868; Alt is also a platform key that can steal window focus)**, L (ReactiveInterrupt), Mouse L (Interact and the role QTE actions GenQTE, JohnQTE, LindaQTE, LucyQTE, **MarkQTE**), Mouse R (Cancel), wheel (Scroll).
- Free: Ctrl, Q, E, R, F, G, H, Z, X, C, V, B, number keys, F-keys.
- So the design plan's proposed hold-Alt "Family watch" is **already taken**.
