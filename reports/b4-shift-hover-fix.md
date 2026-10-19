# Report: B4 Shift hover preview revived (ShowStatsHoverPreview bus subscription)

Plan: none (Tier 2 bugfix, D-064)    Agent: miso-implementer    Branch: thj/fr-readability
Outcome: done (fix in; one highlight clash found and reported, other systems untouched)

## What changed

- `miso/Assets/_Project/Core/Interactions/Runtime/ShowStatsHoverPreview.cs`: replaced the inverted `WaitUntil` coroutine with `OnEnable -> Rebind(bus)`, `OnDisable -> Rebind(null)` and an `Update` that rebinds when `GlobalEventBus.Instance` changes (same shape as `RoleZonePresenter`). `Rebind` unsubscribes from the old bus, clears the preview, resets the held/hover/controller state, then subscribes to the new bus if it exists. Subscribes to the same two events as before (`toggleShowStats`, `gridCellEntityHovered`). The `Awake` hosting of the four presenters is unchanged. Removed the now unused `using System.Collections;`. File stays LF, no BOM.
- One small extra inside `ClearPreview`: `_hoveredUnit?.SetFutureTargetsHover(false)` became `if (_hoveredUnit) ...`. `?.` skips Unity's destroyed-object null, and a rebind after a level change would otherwise call into a destroyed unit.

## Acceptance criteria

- [x] Preview subscribes to the live bus: waits for it via `Update` (no frame guard, so no 16 s timeout on slow loads), nothing happens while the bus is missing. Compiles.
- [x] No duplicate subscriptions: every path goes through `Rebind`, which removes before adding. A re-enable removes then re-adds; a new bus instance is a different object so the old one is unsubscribed first.
- [x] Unsubscribes on disable/destroy (`OnDisable` runs on destroy too) and clears only what it set (`_moveCells`, `_attackCells`, future-target hover).
- [x] Role-zone layer unaffected: it is a separate `GridCell` layer (`GridCell.RoleZone.cs`, `SetRoleZone`); the preview never calls it. Both hosts listen independently on the same events.
- [ ] Release/unhover clears only its own cells without side effects: true for cells it set, but see the clash below (not changed, as instructed).
- No test added: the logic is MonoBehaviour wiring and the only decision (`bus != _bus`) is trivial.
- Verification: refresh/compile clean (the only console error is an unrelated "Internal error - unexpected guid mismatch" from the editor). EditMode suite: 175 total, 174 passed, 1 failed = the known red `AIRegressionTest.Baseline_MatchesCurrentAI`. Not play-checked.

## Save reset

no

## Decisions I made

- Used the per-frame `Update` rebind instead of the suggested `WaitUntil` fix, because the brief asked to mirror `RoleZonePresenter` and it also covers bus re-creation per play. Same behaviour for the player.
- Rebind also resets `_playerController` (cached from the previous level's `CombatLevel`) so `CanShowPreview` does not read a destroyed controller.

## Needs THJ

Now that the preview is alive it clashes with the selected unit's range highlight. Decision wanted only if you want it fixed; none of the other systems were changed.

1. Situation: with a player unit selected and a move range or ability range showing, hold Shift and hover a unit.
2. Problem: `GridCell.SetHighlight` and `SetInAttackRange` are plain bools (`GridCell.cs` L351-372, L380-405) with no getters. The preview writes `SetHighlight(true, isMove: true)` on the hovered unit's reachable cells (`ShowStatsHoverPreview.cs` ShowPreview, move loop) and `SetHighlight(false)` on release/unhover. Any cell shared with the selected unit's range is turned off for good: the selected unit's range comes from `PhaseData.ActiveAbilityRangeCells`, set with `SetHighlight(true, isMove: true)` in `FactionControllerBase.cs` L438, L479 (ActionSelection) and cleared at L403/L444/L486. It is not restored until that state re-enters. Hovering the selected unit itself under Shift wipes its whole move range. Likewise `SetInAttackRange(false)` on release wipes cells that `PlayerController.cs` L1017/L1028 (`_attackRangeCells`, cleared L1133), `UnitPanelUI.cs` L267/L281 (role-icon hover) and `UnitsCooperationHandler.cs` L1427/L1439 (John+Linda highlight) set, if they overlap. The ability-target state is already guarded by `CanShowPreview` (`IsSelectingAbilityTarget`), so the AoE preview during target selection is safe; the exposed cases are ActionSelection/move-hover and the HUD icon / duo highlight.
3. Options:
   - A. Skip the preview while the player has a unit selected in ActionSelection (extend `CanShowPreview`). Smallest, one line; loses the preview on your own turn, which is when it is most useful.
   - B. Skip any cell in `PhaseData.ActiveAbilityRangeCells` in the preview (move and attack loops), and on clear only unset cells it set. Keeps the preview, fixes the selected-unit range case, still leaves the HUD icon / duo overlap (rare: needs the mouse on a HUD icon while hovering a unit).
   - C. Ref-count `SetHighlight`/`SetInAttackRange` in `GridCell` (core/shared). Fixes all cases, touches a shared class, own commit.
4. Recommendation: B now, C if the overlaps show up in play.
5. Default if no answer: ship as is; the behaviour is the same class of overlap that already exists between the move hover preview and the HUD icon hover.

## Docs to update

- `reports/b4-r3a-role-zones.md` / status backlog: the "Shift hover preview dead" finding is closed by this fix; clash above becomes the open item.

## Risks and loose ends

- The overlap clash above is the main risk; the preview was dead for the whole life of this code, so its interactions were never play-tested.
- The hover event also fires with `entity == null` for empty cells in `HandleHovering` (`GridManager.cs` L171); `OnEntityHovered` handles it (clears, `_hoveredUnit = null`).
- Unhover calls `ClearPreview` even when Shift is not held, which only touches cells the preview set (empty list then) and `SetFutureTargetsHover(false)`.
- Noticed, not touched: `UnitPanelUI.ClearUnitControlPanel` does not clear the role-icon hover cells (already noted in R3a).

## Proposed commits

1. `fix(interactions): revive the Shift hover preview by subscribing to the live event bus (B4, D-064)`: `miso/Assets/_Project/Core/Interactions/Runtime/ShowStatsHoverPreview.cs` (plain)

## Other branches

none known

## How to see it

1. Enter a combat level, hold Shift and hover a unit: its move cells (blue move frames) and attackable cells (attack-range icon) show; its queued future-action targets highlight if it has one. Release Shift or move off the unit: they disappear.
2. With a player unit selected and Shift held, the role zones (outlines) still show and are not changed by hovering.
3. Check the clash: select a unit with move range showing, hold Shift and hover an enemy near it, then release. Cells shared with the selected unit's range may go dark (the issue above).
4. Hold Shift during an enemy turn and restart a level (new bus): no errors, preview works again after the restart.
5. In target selection of an ability, Shift-hover does nothing (guarded).
