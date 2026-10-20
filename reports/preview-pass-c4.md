# Report: Preview pass C4, badge drives the role-zone layer

Plan: plans/2026-10-19-preview-pass-tech.md (C4)    Agent: miso-implementer    Branch: thj/preview-improvements
Outcome: done (play check pending, C9)

## What changed

- `miso/Assets/_Project/Core/Managers/GlobalEventBus.cs` (core, additive): new `public UnityEvent<GUnit, bool> onFamilyRoleBadgeHover = new ();` next to `onFamilyRolePrompt` / `onFamilyRoleOutcome`, same declaration pattern, with a comment. 4 added lines, nothing else touched. BOM + LF kept.
- `miso/Assets/_Project/Features/UI/Panels/Scripts/UnitPanelUI.cs`: the role badge hover lambda keeps the tooltip and calls `BeginRoleBadgeHover(unit)` / `EndRoleBadgeHover()`. Both `SetInAttackRange` loops (and their `GetComponent<FactionRoleHandlerBase>().GetCellsInRange()` calls) are gone. `EndRoleBadgeHover()` is also called from `Hide()`, `ClearUnitControlPanel()` (so every unit change and clear) and `OnDestroy()`.
- `miso/Assets/_Project/Features/UI/Panels/Scripts/UnitPanelUI.RoleBadge.cs` (partial): `_roleBadgeHoveredUnit`, `BeginRoleBadgeHover`, `EndRoleBadgeHover` and a new `OnDisable() => EndRoleBadgeHover()`. Each begin is paired with exactly one `hovered = false`. A begin on another unit ends the previous one first. Raising is null-safe when no bus exists.
- `miso/Assets/_Project/Core/Systems/RoleZoneSystem/Runtime/RoleZoneRules.cs`: new overload `OwnersToShow(selected, showAllHeld, hovered, badgeHovered, family, hasZone, out focused)`. The old signature forwards to it with no badge, so its behaviour is unchanged. A badge-hovered unit that has a zone is always added once and becomes `focused`.
- `miso/Assets/_Project/Core/Systems/RoleZoneSystem/Runtime/RoleZonePresenter.cs`: subscribes and unsubscribes `onFamilyRoleBadgeHover` in the existing `Subscribe` (via `Rebind`, OnEnable/OnDisable/bus change). `_badgeHovered` is set on enter. On exit it is cleared only if the exit is for that unit (or the unit is null). It is also cleared on `unitDied` and in `ResetState` (disable, bus change after a scene or level reload, `levelEnded`). It draws through the normal `Apply`. New `public GUnit FocusedOwner { get; private set; }` is set on each redraw for C6.
- `miso/Assets/_Project/Core/Systems/RoleZoneSystem/Editor/RoleZoneBadgeHoverTests.cs` (+ `.meta`, new): 10 EditMode tests of the new overload.

## Acceptance criteria

- [x] `GlobalEventBus.onFamilyRoleBadgeHover(GUnit, bool)` is declared like `onFamilyRolePrompt` and raised by `UnitPanelUI` on badge enter and exit. Covered by code and compile. Raising it needs the play check.
- [x] `UnitPanelUI` no longer calls `SetInAttackRange` for the badge: both loops are removed (diff).
- [x] `RoleZonePresenter` shows the badge-hovered unit's zone without selection or Shift, and clears it on exit, presenter disable and scene or level change. The rule is tested (`Badge_NotSelected_NoShift_ShowsItsZone_AndFocusesIt`, `AfterExit_*`, `Badge_UnderShift_*`, `Badge_OnSelectedUnit_IsOneEntry`, `OldOverload_MatchesNoBadge`). The event wiring and clearing need the C9 play check. The focus style is C6: it draws as a normal entry for now and is reported as `FocusedOwner`.
- [x] Badge and zone show the same cells: the badge draws nothing itself now, and the only drawing is the presenter's `handler.GetCellsInRange()`.
- [x] Exit fires when the panel hides, the unit changes or the panel is disabled or destroyed while hovered (`Hide`, `ClearUnitControlPanel`, `OnDisable`, `OnDestroy`). Covered by code; needs the play check.
- [x] No new statics. Line endings (LF everywhere) and BOM (GlobalEventBus only) are kept.
- [x] Compile is clean (no errors after a forced refresh through the Unity MCP). Full EditMode suite: 212 tests, 211 passed, 1 failed: the known red `AIRegressionTest.Baseline_MatchesCurrentAI`. The RoleZoneSystem group passes 100/100, including the 10 new tests. No Play mode was used.

## Save reset

no

## Decisions I made

- Overload instead of changing the signature: the existing `OwnersToShow` tests and any other caller keep compiling unchanged. Same behaviour.
- Badge precedence: a badge-hovered unit with a zone is always shown, even under the D-064 Shift narrowing. Under Shift with the cursor on Mark and the badge on John, both are shown and John is focused. C6 removes the narrowing anyway. With C3's hover gate the cursor can't be on a grid unit while it is on the badge, so this case shouldn't come up.
- The badge zone shows for any unit whose handler has a zone, family or not. The panel decides which unit has a badge. While the grid is faded out, nothing is drawn, as before.
- A late exit for a unit other than the current `_badgeHovered` doesn't clear it, so an out-of-order end can't drop a newer hover.
- `FocusedOwner` is a public read-only property and not a private field, so there is no CS0414 warning until C6 reads it.

## Needs THJ

none

## Docs to update

- `tech/combat-architecture.md` (coordinator): the new bus event `onFamilyRoleBadgeHover` and that the role badge drives the role-zone layer (no `SetInAttackRange`).
- GDD `family-systems.md` (designer, after C6): the badge hover shows the zone.

## Risks and loose ends

- The Unity `GlobalEventBus` component serializes UnityEvent fields. The level prefab or scene that holds it gains an empty `onFamilyRoleBadgeHover` entry the next time it is saved (YAML noise, like D-068's). Nothing was saved in this run.
- `UnitPanelUI.cs` still has `using MISO.Core.Systems.GridSystem;`, which may now be unused. Left as is (no drive-by edits).
- `Hide()` ends the hover while the pointer may still be on the badge. The zone reappears only after the pointer leaves and re-enters. That seems right, but check it in C9.
- Not reproduced in Play: P1 itself. Put the two-minute repro from design P1 in C9.

## Proposed commits

1. `feat(events): add a family role badge hover event`: `miso/Assets/_Project/Core/Managers/GlobalEventBus.cs` (core, additive; compiles alone)
2. `feat(role-zones): the role badge hover shows the unit's zone on the role-zone layer`: `miso/Assets/_Project/Features/UI/Panels/Scripts/UnitPanelUI.cs`, `miso/Assets/_Project/Features/UI/Panels/Scripts/UnitPanelUI.RoleBadge.cs`, `miso/Assets/_Project/Core/Systems/RoleZoneSystem/Runtime/RoleZoneRules.cs`, `miso/Assets/_Project/Core/Systems/RoleZoneSystem/Runtime/RoleZonePresenter.cs`, `miso/Assets/_Project/Core/Systems/RoleZoneSystem/Editor/RoleZoneBadgeHoverTests.cs`, `miso/Assets/_Project/Core/Systems/RoleZoneSystem/Editor/RoleZoneBadgeHoverTests.cs.meta` (plain)

Don't stage the unrelated `Packages/*` and `ProjectSettings/*` changes that were already in the tree.

## Other branches

none (merges to `main` with the rest of the preview pass)

## How to see it

1. Open a combat level with John and Linda (e.g. *In My Father's Arms*, `LevelE3-C1`) from PreloadScreen.
2. Select John (the panel shows the selected unit) and hover the small role badge or Family Role icon in the HUD unit panel. John's zone shows as shield icons in his quadrant on the grid, with no red sword icons. It matches his zone under Shift exactly.
3. Move the pointer off the badge: the zone goes, except when John is selected, where his zone stays as usual.
4. With the badge hovered, select another unit through a hotkey or a click, or end the turn so the panel hides: the badge zone goes away.
5. Mark–John duo cells: they no longer lose their sword icons when you hover and unhover the badge.
