# Report: Preview pass fix 1 (Shift narrowing back, visible tether, per-tile sword icons)

Plan: coordinator brief from D-087 and D-088 (findings `reports/preview-pass-fix1-explore.md`, tech plan `plans/2026-10-19-preview-pass-tech.md`)    Agent: miso-implementer    Branch: thj/preview-improvements
Outcome: done. Compile is clean and the suite passes. The in-game look needs THJ's play check.

## What changed

Paths are under `miso/Assets/_Project/`. Every file keeps its line endings (all LF). `GridCell.cs` and `GridCell.ShiftPreview.cs` keep their BOM; the others had none and still have none. No new statics: only `const`s and instance fields.

**Unit 1: D-064 narrowing restored (D-087)**
- `Core/Systems/RoleZoneSystem/Runtime/RoleZoneRules.cs`:
  - Under Shift, hovering a family unit that has a zone shows only that zone again. Hovering a unit without a zone (Toba, an enemy) keeps the full view.
  - A Shift hover no longer gives focus. Only the badge-hovered unit is the focused owner, and its zone is added to the view as in C4.
  - D-080 hide, `SameCellSet`, `ZoneDuplicatesReach` and `WithoutOwner` are unchanged.
- `Core/Systems/RoleZoneSystem/Runtime/RoleZonePresenter.cs`:
  - Removed `FocusScale` and `FocusAlpha`. Every zone, the badge-hovered one too, now draws plain (scale 1, the handler's own alpha).
  - `FocusedOwner` is still there and now reports only the badge owner.
- Tests:
  - `RoleZoneTests.cs`: `Shift_HoverFamilyMember_ShowsOnlyThatZone` is restored, and I added `Shift_HoverSelectedFamilyMember_ShowsOnlyThatZone`.
  - `RoleZoneBadgeHoverTests.cs`: `OldOverload_MatchesNoBadge` now expects no focus, and I added `Badge_UnderShiftHover_AddsItsZoneToTheNarrowedView`.
  - `RoleZoneFocusTests.cs`: the D-076 focus tests are rewritten for narrowing with no focus. I added a test that a duplicate zone still shows on a Shift hover, two tests for a badge combined with a Shift hover, and one for a Shift hover on the moving unit (with D-082 nothing is left to draw). The `WithoutOwner` focus tests now get their focus from the badge. The scale tests (quadrant fit, layer set) are kept, because they cover the core per-entry scale code, which stays.

**Unit 2: the tether is visible (D-088 part 2)**
- `Core/Systems/RoleZoneSystem/Runtime/JohnTetherPresenter.cs`:
  - Always uses the runtime Sprites/Default material. The head anchor still comes from `ThreatLineRenderer`; `FindHead` no longer returns a material.
  - Width is the constant `LineWidth = 0.025f`. The serialized `lineWidth` field (0.015) is gone. The component is only added at runtime by `ShowStatsHoverPreview`, so no saved data is lost; I checked that its GUID appears in no scene or prefab.
  - Alpha is 0.85 (see Decisions).
  - Sorting, set in `Show`:
    - The sorting layer is the one of John's main visual (Default).
    - The line's order is 1 + the highest `sortingOrder` among John's and that ally's SpriteRenderers on that layer, inactive renderers included.
    - The cap's order is the line's + 1.
    - The fixed `CapSortingOrder` is gone.

**Unit 3: per-tile sword icons (D-088 part 1)**
- `Core/Systems/GridSystem/Runtime/GridCell.cs` (core):
  - `SetInAttackRange` no longer redirects to `OverlayOrigin`.
  - The attack icon is out of `_recenterOverlays`, so every cell's icon stays on its own tile. The override icon was never moved, so it is per tile as well.
  - New: in `UpdateVisuals`, the two attack icons switch to the `DynamicTop` sorting layer (same order) when the cell is covered by an occupant with more than one occupied cell. Otherwise they go back to the prefab layer, which is cached in `EnsureOverlayCache`.
- `Core/Systems/GridSystem/Runtime/GridCell.ShiftPreview.cs` (core):
  - Attack layers apply to the cell itself. Move layers still redirect to the anchor and still wrap the footprint.
  - A call that mixes both kinds is split into one call per kind. No caller does this today.
  - `_shiftAttackRenderer` cancels the root's centroid offset, so it stays on its own tile, and it gets the same `DynamicTop` raise. Its order is still the real icon's −1.
- **Review should-fix (`GridCell.cs`).** Plug and unplug used to run `UpdateVisuals` on the anchor only. Now `PlugEntityInternal` and `UnplugEntity` call a new `RefreshAttackIconSorting()` on every footprint cell. It re-applies the attack icons' sorting layer and the Shift attack copy's layer, so an icon already showing on a non-anchor tile can't keep a stale layer when a multi-cell occupant arrives, leaves or dies (death goes through `UnplugEntity`). The AI's `SimAssignOccupant` and `SimReleaseOccupant` are not touched (worker thread). After this fix: refresh clean, no console errors, EditMode suite 273 tests with 272 passing; the one failure is the known red.
- `Core/Interactions/Runtime/PlayerController.cs` (core, caller fix, **flagged**):
  - The targeted-occupant block (around L1016) used to mark only `occupant.CurrentCell` when the anchor wasn't already in the list.
  - Per tile, that would add a second icon on the anchor of a multi-tile enemy when you hover any other of its tiles.
  - Now it marks the occupant's tiles only when none of them is already marked (`OccupantIntersects`), and then it marks every tile of the occupant. For a one-tile unit the behaviour is unchanged.

## Acceptance criteria

- [x] **Shift + hovering a Bergson shows only that unit's zone; the Shift focus enlargement is gone.** Tests: `RoleZoneTests`, `RoleZoneFocusTests`. How it looks on screen: play check.
- [x] **The badge hover still shows its unit's zone, drawn plain.** Tests: `RoleZoneBadgeHoverTests`. Plain drawing: code; how it looks: play check.
- [x] **The C6 P5 hide and its tooltip are unchanged.** The D-080 tests pass unchanged. `RoleZoneAttackMatch` and `UnitPanelUI` are not touched.
- [x] **The core `GridCell.RoleZone.cs` is not touched.**
- [x] **Tether: plain material, head anchor kept, 0.025 width as a constant, John's colour, sorted just above both endpoint units' sprites on their layer (not Overlay), cap one above.** Code. Whether it is visible: **play check**.
- [x] **One sword icon per covered tile on multi-tile occupants, including the override icon and the Shift attack layer. The Shift move frame still wraps the footprint.** Code. **Play check** on the Masher Goblin (2×2), Goblin Queen (1×2) and Mountain Deev (3×2).
- [x] **Clearing stays balanced.** Without the redirect, set and clear always address the same cell. `SetShiftPreview(attack)` returns the cell itself. Shift move entries keep the old "clear locally first" rule. No anchor can be left holding stale entries, because nothing redirects any more (the old redirect state lived only at runtime).
- [x] **Every `SetInAttackRange` caller checked.**
  - Ghost reach (`BasicAttackReachFrom`): per cell, fine.
  - Ability affected area: per cell, fine.
  - Targeted occupant: fixed (see above).
  - Mark–John duo union cells: per cell, fine.
  - Shift preview: per cell for attack.
- [x] **Icons raised only on multi-cell occupied tiles.** Done with `DynamicTop`, same order. Whether the boss sprite still covers them: **play check**.
- [x] **Compile and suite.** Forced refresh through the Unity MCP: the console shows no errors. Full EditMode suite: 273 tests, 272 passed. The only failure is the known red `AIRegressionTest.Baseline_MatchesCurrentAI`, not touched. I ran two of the new tests by name to confirm the new code was compiled in. No Play mode was used.

Test coverage: the Unit 1 rules are covered by EditMode tests. Units 2 and 3 are Unity-object rendering code with no new pure logic, so they need the verifier's play check.

## Save reset

no

## Decisions I made

- **Badge-hovered zone drawn plain.** Removing the focus style breaks nothing: `FocusedOwner` has no other reader, and the scale API in core stays with default 1.
- **Tether alpha 0.85 instead of 0.7.** A 0.025-wide plain line at 0.7 risks still getting lost over busy sprites, and visibility was the bug. It is a single constant if THJ wants 0.7.
- **The sorting-order search includes inactive renderers** on the units' layer, so the arc stays above anything the unit can turn on there. With the +10 per vertical layer, this stays inside the unit's band.
- **The raise switches the sorting layer to `DynamicTop` and keeps the order** (−9 for the icon, −10 for the Shift copy). The icons then draw above every Default-layer unit sprite but below the unit's own DynamicTop sprites (`TargetSelectCounter` and the Swap icon, orders 1 and 2), so the target counter stays on top.
- **"Multi-cell" means the cell's occupant (or planted entity) has more than one `OccupiedCells`.** Non-anchor cells only refresh this when their own `UpdateVisuals` runs, and that always happens when an icon is set, so a stale layer can't show.

## Needs THJ

none. The coordinator should know that the `PlayerController.cs` caller fix touches a core file the brief didn't name. It follows from "check all callers still behave". It is its own commit and can be dropped, but without it a multi-tile enemy hovered off its anchor shows an extra icon on the anchor tile.

## Docs to update

- GDD `family-systems.md` (designer): Shift + hover narrows to one zone again (D-087); no focus enlargement.
- `tech/combat-architecture.md` (or the grid notes): attack icons are per tile. Only the move frame, hover, selection and the other overlays wrap a multi-cell footprint. On tiles under multi-cell occupants, the attack icons draw on `DynamicTop`.

## Risks and loose ends

- With D-082, a Shift hover on the unit whose move preview is up narrows to that unit, whose zone is suppressed. Only the ghost-tile zone from `MovePreviewCoverPresenter` remains. This is tested; it looks intended.
- The `DynamicTop` icons also draw above an ally or another enemy that stands on a neighbouring tile and overlaps the boss tile visually. Only multi-cell occupied tiles are raised, so this is rare.
- A boss sprite that reaches over the tiles north of its footprint can still cover the icons on those (unoccupied) tiles. That case is out of scope.
- The per-entry scale support in `GridCell.RoleZone.cs`, `RoleZoneLayerSet` and `RoleZoneSlot` is now unused in game (kept, as asked).
- The text-only header comment in `RoleZoneSystem/Runtime/MovePreviewCoverPresenter.cs` was not checked for focus wording. Grep found no reference to the focus API there.

## Proposed commits

1. `fix(roles): Shift hover shows only the hovered unit's role zone again`: `miso/Assets/_Project/Core/Systems/RoleZoneSystem/Runtime/RoleZoneRules.cs`, `.../RoleZoneSystem/Runtime/RoleZonePresenter.cs`, `.../RoleZoneSystem/Editor/RoleZoneTests.cs`, `.../RoleZoneSystem/Editor/RoleZoneBadgeHoverTests.cs`, `.../RoleZoneSystem/Editor/RoleZoneFocusTests.cs` (plain)
2. `fix(roles): John's tether uses a plain material, a wider line and sorts above both units`: `miso/Assets/_Project/Core/Systems/RoleZoneSystem/Runtime/JohnTetherPresenter.cs` (plain)
3. `fix(grid): attack icons stay on their own tile under multi-cell occupants`: `miso/Assets/_Project/Core/Systems/GridSystem/Runtime/GridCell.cs`, `miso/Assets/_Project/Core/Systems/GridSystem/Runtime/GridCell.ShiftPreview.cs` (core). The Shift partial uses the sorting helper added in `GridCell.cs`, so the two files go together.
4. `fix(input): a targeted multi-tile occupant marks each of its tiles once`: `miso/Assets/_Project/Core/Interactions/Runtime/PlayerController.cs` (core; depends on 3)

Commits 1 to 3 are independent of each other. Don't stage the `Packages/*` or `ProjectSettings/*` changes.

## Other branches

none (merges to `main` with the preview pass)

## How to see it

1. From PreloadScreen, open a level with all four Bergsons and a multi-tile enemy (e.g. one with the Masher Goblin, Goblin Queen or Mountain Deev).
2. Hold Shift. All four zones show. Hover Mark: only his punch icons stay, at normal size. Move to Linda: only hers. Hover an enemy or Toba: all four come back.
3. Without Shift, hover a Bergson's Family Role badge in the HUD. Its zone shows at normal size and opacity.
4. Select a Bergson whose attack reaches the multi-tile enemy. Every covered tile of the enemy shows its own sword icon, drawn above the enemy sprite. Hover one of the boss's tiles with the attack: the tiles of the area are marked, with no extra icon on the anchor corner.
5. Hold Shift over the boss: its move frame wraps the footprint as before. Shift over a Bergson that reaches the boss: one warm-white icon per covered boss tile.
6. Trigger John's role prompt (an ally next to him gets attacked). An orange arc goes from John's head to the ally's head, drawn over both sprites, with the shield cap on top at the ally's end.
