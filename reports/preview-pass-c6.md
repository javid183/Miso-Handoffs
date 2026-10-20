# Report: Preview pass C6, focus instead of narrowing and the P5 hide

Plan: plans/2026-10-19-preview-pass-tech.md (C6)    Agent: miso-implementer    Branch: thj/preview-improvements
Outcome: done (in-game look and the real Linda/Lucy match need the C9 play check)

## What changed

All files LF. `GridCell.RoleZone.cs` keeps its BOM; the others have none, as before. No new statics (two `const`s only).

- `miso/Assets/_Project/Core/Systems/GridSystem/Runtime/GridCell.RoleZone.cs` (core partial, additive): `SetRoleZone(..., float scale = 1f)`. The scale is stored per entry and passed to the quadrant fit. Existing callers are unchanged.
- `miso/Assets/_Project/Core/Systems/RoleZoneSystem/Runtime/RoleZoneLayerSet.cs`: per-entry scale (`ScaleAt`, `Set(..., float scale = 1f)`). A scale change counts as a change.
- `miso/Assets/_Project/Core/Systems/RoleZoneSystem/Runtime/RoleZoneSlot.cs`: new overload `RoleZoneSlotLayout.Fit(slot, box, spriteSize, padding, scale)`. The old overload forwards with scale 1.
- `miso/Assets/_Project/Core/Systems/RoleZoneSystem/Runtime/RoleZoneRules.cs`:
  - D-064's narrowing is removed. New 8-argument `OwnersToShow(..., Func<T,bool> zoneIsAttackDuplicate, out focused)`; the 5- and 7-argument overloads forward to it with no duplicate check.
  - Focus goes to the badge-hovered unit first, otherwise under Shift to the hovered unit if its zone is shown.
  - New pure `SameCellSet<T>(a, b, ignored = null)`.
- `miso/Assets/_Project/Core/Systems/RoleZoneSystem/Runtime/RoleZoneAttackMatch.cs` (+ `.meta`, new): the one D-080 check.
  - `ZoneEqualsBasicAttack(GUnit)` compares the handler's `GetCellsInRange()` with `UnitThreatAnalysis.BasicAttackReachFrom(unit, unit.CurrentCell)`.
  - `ZoneEqualsBasicAttack(GUnit, IReadOnlyCollection<GridCell> zoneCells, GridCell origin)` is the overload for C7's ghost cell.
  - Stateless, and it fails safe: any exception, an empty zone or an empty reach gives false, so the zone stays drawn.
- `miso/Assets/_Project/Core/Systems/RoleZoneSystem/Runtime/RoleZonePresenter.cs`: passes `RoleZoneAttackMatch.ZoneEqualsBasicAttack` to the rules. The focused owner is drawn with alpha `FocusAlpha = 1` and `FocusScale = 1.15`; the other zones are unchanged.
- `miso/Assets/_Project/Features/UI/Panels/Scripts/RoleBadgeState.cs`: `RoleBadgeRules.ZoneMatchesAttackLine = "Same tiles as the basic attack; Shift shows them."` (D-084, final wording, so no placeholder tag).
- `miso/Assets/_Project/Features/UI/Panels/Scripts/UnitPanelUI.RoleBadge.cs`: `RoleBadgeTooltipSuffix` appends the FTP line (as before), then the new line when `RoleZoneAttackMatch.ZoneEqualsBasicAttack(unit)` is true. It is computed when the badge is hovered.
- `miso/Assets/_Project/Features/UI/Panels/Scripts/UnitPanelUI.cs`: removed `using System.Collections.Generic;` and `using MISO.Core.Systems.GridSystem;`. Both stopped being used when C4 removed the `List<GridCell>` loops; the compile is clean without them. The other usings are still used (`Action`, `IEnumerator`, `Where`/`ToArray`, `RuntimeAbility`, ...).
- Tests:
  - `RoleZoneTests.cs`: `Shift_HoverFamilyMember_ShowsOnlyThatZone` became `Shift_HoverFamilyMember_KeepsEveryZone`.
  - `RoleZoneBadgeHoverTests.cs`: `AfterExit_BackToSelectedOnly_AndNoFocus` became `NoBadge_SelectedOnly_AndNoFocus`, without the first `Show` call, which had no effect. `OldOverload_MatchesNoBadge` now expects the Shift-hovered Mark to be focused (D-076).
  - `RoleZoneFocusTests.cs` (+ `.meta`, new): 28 tests covering focus rules, the D-080 hide rules, `SameCellSet`, the focus fit and clamp, and the layer-set scale.

## Acceptance criteria

- [x] **Every zone stays under Shift; focused owner = Shift-hovered Bergson or badge-hovered unit.** Tests: `Shift_HoverFamilyMember_KeepsAll_AndFocusesIt`, `Shift_HoverSelectedUnit_FocusesIt`, `Shift_HoverUnitWithoutZone_NoFocus`, `Shift_HoverUnitNotShown_NoFocus`, `NoShift_HoverGivesNoFocus`, `Shift_BadgeWinsFocusOverHover`, plus the C4 badge tests.
- [x] **The focused entry draws at full alpha and scale 1.15 in its quadrant; the others are unchanged.** Code. The fit and its clamp are tested. How it looks on screen: play check (C9).
- [x] **The selected unit's zone is hidden when it equals `BasicAttackReachFrom(unit, committed cell)`; Shift and the badge hover still draw it.** Rule tests: `NoShift_SelectedDuplicate_IsHidden`, `Shift_SelectedDuplicate_IsStillShown_AndPredicateNotAsked`, `Badge_OnSelectedDuplicate_ShowsIt_Focused`, `Badge_OnOtherUnit_SelectedDuplicateStaysHidden`. Equality tests: order, duplicates, nulls, subsets, ignored cells. The check reads `CurrentCell` only, never the ghost. **That Linda's and Lucy's zones really match in game: play check** (see Decisions, own tile).
- [x] **Tooltip line when the hide condition holds, using the presenter's function.** Both call `RoleZoneAttackMatch.ZoneEqualsBasicAttack(GUnit)`. The text is a constant next to `TooltipLine`. Not unit-tested (it needs a real `GUnit`): play check.
- [x] **C4 should-fixes.** Both done (see above).
- [x] **No new statics; BOM and LF kept per file.** Checked byte by byte after the edits.
- [x] **Compile and suite.** Forced refresh through the Unity MCP: no errors. Full EditMode suite: 246 tests, 245 passed, 1 failed, the known red `AIRegressionTest.Baseline_MatchesCurrentAI` (not touched). The first run had one more failure, `OldOverload_MatchesNoBadge`, a C4 test that pinned "no focus" under a Shift hover; I updated it for D-076. No Play mode was used.

## Save reset

no

## Decisions I made

- **The unit's own footprint is left out of the D-080 comparison.** Both zones include the tiles the unit stands on: Linda's at distance 0 in her row, Lucy's at distance 0. Their basic attacks have `includeSelf: 0`, and `AttackReachFrom` drops the footprint. A literal set equality would therefore never hold, and the hide would never fire, although D-080 and the plan expect it for Linda and Lucy today. `SameCellSet` takes an `ignored` set, and `RoleZoneAttackMatch` passes the unit's footprint on the origin. The rest of the data matches: Unconstrained walkability, ranged reach, straight for Linda, the same radius. That doesn't prove the sets match on every board, so the C9 play check should confirm the hide. This is close to a behaviour call: the coordinator may want THJ to know.
- **Focus clamp: zero overlap.** The 1.15 icon grows around the quadrant's centre and may use up its padding, but it is clamped to the quadrant edge, so it never covers a neighbour's icon. With today's constants (box 0.9 of the frame, padding 0.03), the plain fit is 0.39 of the frame and 1.15× is 0.4485, just under the 0.45 quadrant, so 1.15 applies in full on a one-cell unit. On a multi-cell footprint the padding is relatively smaller, and the growth can be clamped below 1.15 there.
- **Alpha goes through the entry's colour** (the presenter sets `a = 1` for the focused owner). `RoleZoneLayerSet` already stored colour per entry, so it gains only a scale. The behaviour is the same as a separate alpha field.
- **Badge focus beats hover focus.** With C3's hover gate the two can't really happen together.
- **A Shift hover focuses any unit whose zone is shown** (also a selected unit outside the family list). A hovered unit whose zone isn't shown gives no focus.
- **The tooltip line needs a badge** (`state != None`) and is computed on hover, from the committed cell. It appears even when the panel shows a unit that isn't selected, because the zone would be hidden on its selection too.
- **Cost:** for the selected unit, the handler's `GetCellsInRange()` runs twice per redraw (once for the check, once to draw). Redraws are event-driven, so I kept the single check function instead of threading the cells through.

## Needs THJ

none. The own-tile exclusion above is for the coordinator to pass on if wanted.

## Docs to update

- GDD `family-systems.md` (designer): the Shift view keeps every zone and the hovered or badge one is emphasised (full alpha, 1.15). The selected unit's zone is hidden when it matches its basic attack (own tiles ignored), and the tooltip line explains it.
- `tech/combat-architecture.md`: `RoleZoneAttackMatch` is the one D-080 check; C7 reuses its 3-argument overload.

## Risks and loose ends

- **For C7:** call `RoleZoneAttackMatch.ZoneEqualsBasicAttack(unit, followZoneCells, ghostCell)`. It already ignores the unit's footprint on the ghost cell. `GetCellsInRange()` takes no origin today, so C7 needs its own way to get the zone from the ghost tile.
- If the sets differ on some board by an edge case (a cell where ranged reach and the zone's distance rule disagree), the zone just stays drawn. That is the fail-safe direction, with no flicker.
- `Lucy_Ability_FactionRole` traverse mode and her attack's: both are 1 (Adjacent) by the assets. If either changes, the hide turns off by itself.
- `GridCell.ShiftPreview.cs` was committed by THJ during this run (`ce104f51e`). C5's `ShowStatsHoverPreview.cs`, `ShiftPreviewRules*.cs` are still uncommitted and untouched by me.

## Proposed commits

1. `feat(grid): per-entry icon scale on the role-zone layer`: `miso/Assets/_Project/Core/Systems/GridSystem/Runtime/GridCell.RoleZone.cs`, `miso/Assets/_Project/Core/Systems/RoleZoneSystem/Runtime/RoleZoneLayerSet.cs`, `miso/Assets/_Project/Core/Systems/RoleZoneSystem/Runtime/RoleZoneSlot.cs` (core, additive; compiles alone thanks to the default arguments)
2. `feat(role-zones): Shift hover focuses a zone instead of hiding the others, and the selected zone hides when it matches the basic attack`: `miso/Assets/_Project/Core/Systems/RoleZoneSystem/Runtime/RoleZoneRules.cs`, `RoleZoneAttackMatch.cs`, `RoleZoneAttackMatch.cs.meta`, `RoleZonePresenter.cs`, `miso/Assets/_Project/Core/Systems/RoleZoneSystem/Editor/RoleZoneTests.cs`, `RoleZoneBadgeHoverTests.cs`, `RoleZoneFocusTests.cs`, `RoleZoneFocusTests.cs.meta` (plain; depends on 1)
3. `feat(ui): role badge tooltip explains a role zone that matches the basic attack`: `miso/Assets/_Project/Features/UI/Panels/Scripts/RoleBadgeState.cs`, `miso/Assets/_Project/Features/UI/Panels/Scripts/UnitPanelUI.RoleBadge.cs` (plain; depends on 2)
4. `chore(ui): drop unused usings from the unit panel`: `miso/Assets/_Project/Features/UI/Panels/Scripts/UnitPanelUI.cs` (plain; independent)

Don't stage C5's files or the `Packages/*` and `ProjectSettings/*` changes.

## Other branches

none (merges to `main` with the preview pass)

## How to see it

1. From PreloadScreen, open a level with all four Bergsons (e.g. *In My Father's Arms*, `LevelE3-C1`).
2. Select Linda. Only her move range shows, with no arrow icons in her row or column. Do the same with Lucy: no fireball icons. Select John or Mark: his zone shows as before.
3. Hover Linda's Family Role icon in the HUD. Her zone appears, larger and fully opaque, and the tooltip ends with "Same tiles as the basic attack; Shift shows them." On John the line is absent.
4. Hold Shift: all four zones show. Hover Mark on the grid: his punch icons grow slightly and turn fully opaque in the top-right quadrant, without covering the other quadrants. The other three zones stay as they were. Move to Linda: the emphasis follows.
5. Release Shift with Linda selected: her zone goes away again.
