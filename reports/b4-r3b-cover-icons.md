# Report: B4 R3b · Cover icons and the following role zone in the move preview (B)

Plan: plans/2026-10-18-family-role-phase0-1.md (chunk R3b = item B)    Agent: miso-implementer    Branch: thj/fr-readability
Outcome: done, with the reviewer's should-fixes and D-067 applied (see "Review round" below). It compiles, and the EditMode suite is green except the known red. A play check is still needed.

## Review round (reviewer APPROVE with should-fixes; D-067)

1. **Presenter early return.** `TryGetMovePreview` now returns `false` right after computing `playerTurnActive` and `inTargetSelection`, before it reads the getters backed by `PhaseData` (`CurrentlySelectedUnit`, `ActiveAbility`, `AbilityRangeCells`). A hover before the player controller is initialized can no longer throw every frame.
2. **Dead code removed** (the smaller change): the `destinationValid` parameter of `IsMovePreview` (always true; the presenter already returns early when no cell is hovered) and the `ZoneOrigin` helper (always gave the destination). The presenter passes `destination` directly. Removed tests: the three `ZoneOrigin_*` tests and the `MovePreview_NoHoveredCell_IsOff` case.
3. **`JohnFactionRoleHandler.cs`:** I restored the existing whitespace-only blank line. `git diff --numstat` for John is now `14 0`, Mark `12 0` and `ShowStatsHoverPreview.cs` `2 0`: only added lines.
4. **D-067, strict fist:** `CoverIconRules.FistCovers(neighbours, isAttackSpot, inZone)`. The fist shows only if **every** melee attack spot next to the destination lies in Mark's zone, taken from where Mark stands now.
   - The neighbours are `GridCell.AdjacentCells`: the 4-neighbours that exist, so off-grid cells are simply absent.
   - `IsMeleeAttackSpot` (presenter) counts a free walkable cell, the moving unit's own cell (it will be vacated) and a cell held by a unit hostile to the player. It does not count obstacles, blocking hazards, stashed entities or allied units. The destination itself is empty, because it is a move target.
   - If there is no melee attack spot at all, there is no fist: there is nothing to promise.
   - The shield rule is unchanged.
   - **What the fist promises:** "a melee attacker next to you gets punished". It does **not** cover ranged attackers: Mark's role checks the attacker's cell, and a ranged attacker can stand outside his zone. The icon has no tooltip, so the note lives here and in the docs to update.
   - New tests: `StrictFist_AllMeleeSpotsInZone_Covers`, `StrictFist_OneMeleeSpotOutsideZone_DoesNotCover`, `StrictFist_DestinationInZoneButNeighboursNot_DoesNotCover`, `StrictFist_EdgeOfGrid_OnlyExistingNeighboursCount`, `StrictFist_BlockedNeighbourIsNotCounted`, `StrictFist_NoMeleeSpotAtAll_DoesNotCover`, `StrictFist_RangedAttackSpotsAreNotConsidered`, `StrictFist_NullInputs_DoNotCover`.

After the round: no console errors. EditMode: **147 tests, 146 passed, 1 failed**, the known red `AIRegressionTest.Baseline_MatchesCurrentAI` (35 failures, unchanged). The total includes the R4 badge tests that are in the working tree from another agent. My file has 27 tests: 23 − 4 + 8.

## What changed

Paths are under `miso/Assets/_Project/`. All `.cs` files are LF. `GridCell.CoverIcon.cs` has a BOM, like `GridCell.cs` and `GridCell.RoleZone.cs`. The other new files have none, like their `RoleZoneSystem` neighbours.

**Core (Family Roles), additive only**
- `Features/Player/John/Scripts/JohnFactionRoleHandler.cs`: new overload `public List<GridCell> GetCellsInRange(GridCell origin)`. It gives John's zone as if he stood on `origin`: the same radius, traverse mode, Unconstrained walkability and ranged reach, with `origin` itself removed. That matches the existing method, which removes his own cells through `source: Unit`. When `origin` is null or his current cell, it returns `GetCellsInRange()`. The existing `GetCellsInRange()` is unchanged.
- `Features/Player/Mark/Scripts/MarkFactionRoleHandler.cs`: the same overload. It makes the same `GetRangeCells` call as the existing method, started from `origin`. The existing method is unchanged.
- `FactionRoleHandlerBase` is **not** touched.

**Core (Grid), additive only**
- `Core/Systems/GridSystem/Runtime/GridCell.CoverIcon.cs` (+ `.meta`) is a new partial. `GridCell` is already partial since R3a. New public API: `void SetCoverIcons(bool showShield, Color shieldColor, bool showFist, Color fistColor)`, plus `internal const string CoverShieldSpritePath` and `CoverFistSpritePath`.
  - It is its own overlay: a `CoverIcons` child in the cell's overlay space, centred on the Move frame, holding two `SpriteRenderer`s that are created on first use. The shield goes in the lower-left corner and the fist in the lower-right. Each icon is 0.3 of the Move frame's width. Both use sorting order -5 on the base sprite's sorting layer and material: above every grid highlight (Hover glow is -6), below the direction arrows (-1) and the units.
  - There is no footprint redirect, because a move destination is an empty cell.
  - No other `GridCell` code changed.

**Non-core**
- `Core/Systems/RoleZoneSystem/Runtime/CoverIconRules.cs` (+ `.meta`): pure C#. It holds `[Flags] enum CoverIcons { None, Shield, Fist }`, the struct `CoverSource<TUnit>`, and four rules: `IsMovePreview(...)`, `FistCovers(...)` (D-067, strict fist), `ShowsFollowZone(...)` and `IconsFor(moved, sources)` (eligible sources that cover the destination, never the moving unit itself).
- `Core/Systems/RoleZoneSystem/Runtime/MovePreviewCoverPresenter.cs` (+ `.meta`): a MonoBehaviour with no statics. The only constant is `FollowZoneOwnerId = int.MinValue`.
  - **Detecting the preview:** each frame it reads `PlayerController`'s existing public getters: `CurrentPhaseType`, `CurrentlySelectedUnit`, `ActiveAbility`, `AbilityRangeCells`, and `CombatLevelRunHandler.CurrentFactionControllerOrNull`. `CursorSituationDriver` already reads them the same way. It tracks the hovered cell from `gridCellHovered`. The preview counts as on only when all of these hold: it is the player's turn, the controller is in TargetSelection, the active ability is the unit's default move (`Preset.DefaultEmptyGridCellAction`), the hovered cell is in the ability range (`OccupantIntersects`, as `PlayerController` uses), and the hovered cell is not the unit's own cell.
  - **Recomputing:** only when the moving unit or the hovered cell changes, or after `unitDied`, `unitEndMoving`, `abilityPerformed` or a grid fade.
  - **Icons:** for each living player unit with a John or Mark handler (identified by handler type), eligibility is the same test as R3a's `HasZone`: alive, on the grid, role initialized, `showRoleZone` on. The presenter reads the handler's `GetCellsInRange()` and checks whether the destination is inside. Icons are tinted with the role unit's `RoleZoneColor` at full alpha: John's shield orange, Mark's fist green.
  - **Following zone:** when the moving unit is John or Mark, it calls the new `GetCellsInRange(destination)` overload and draws the result on R3a's role-zone layer under `FollowZoneOwnerId`, at the handler's colour, full alpha. R3a's committed zone (owner = handler instance id) stays as it is.
  - **Clearing and errors:** everything is cleared when the preview stops (unhover, cancel, confirm into TakeAction, selection change, turn change, level end, grid fade). A throwing `GetCellsInRange` is caught and logged once per handler.
- `Core/Systems/RoleZoneSystem/Editor/CoverIconRulesTests.cs` (+ `.meta`): 27 EditMode tests.
- `Core/Interactions/Runtime/ShowStatsHoverPreview.cs`: `Awake()` gains one line that adds the `MovePreviewCoverPresenter`, the same hosting as R3a's `RoleZonePresenter`. No scene edit.
- `Resources/GridOverlays/CoverShield.png` and `CoverFist.png` (+ `.meta`): **new placeholder sprites.** No existing project art is a plain shield or fist glyph: John's role icon is "Shield Blessing" and Mark's is "Assault Blitz", both painted character icons that don't read at tile-corner size. Each new sprite is 16×16 pixel art with a white fill, a dark outline and light-grey detail, so a tint keeps the outline. Import settings are copied from `RoleZoneOutline.png.meta`: point filter, PPU 100, Sprite, no 9-slice, no mipmaps. Each has a new GUID and sprite id. They are loaded with `Resources.Load` on first use.

## Acceptance criteria

- [x] **B: the hovered destination shows a shield inside John's zone, and a fist when every melee attack spot next to it is inside Mark's zone (D-067).** *Tests:* `StrictFist_*` (8). The zone test is each handler's own `GetCellsInRange()`. *Tests:* `InJohnsZone_ShowsShield`, `InMarksZone_ShowsFist`, `InBothZones_ShowsBoth`, `OutsideBothZones_ShowsNothing`. *Visuals: play check.*
- [x] **Exclusions:** a unit doesn't cover itself (John moving gets no shield from John, Mark moving gets no fist from Mark). Only living, player-faction, role-bearing handlers with `showRoleZone` on take part. *Tests:* `JohnMoving_GetsNoShieldFromHimself_ButMarksFist`, `MarkMoving_GetsNoFistFromHimself_ButJohnsShield`, `ShowRoleZoneOffOrDead_GivesNoIcon`. The player-faction rule comes from iterating the player controller's `AliveUnits`, so it is checked in code only.
- [x] **When the moving unit is John or Mark, their zone follows the preview:** it is drawn from the hovered cell, on the R3a layer under a distinct owner id, and the unit itself does not move. *Tests:* `FollowZone_*` (3). *Geometry and the nested look: play check.*
- [x] **`showRoleZone` false turns off that unit's icon and its following zone.** It goes through the same eligibility flag. *Tests:* `ShowRoleZoneOffOrDead_GivesNoIcon`, `FollowZone_OffWhenNotEligible`.
- [x] **Separate overlay layer, no clash with the path or AP preview.** The icons are their own child renderers, and `PlayerController` is not modified. *Play check.*
- [x] **Clears on hover exit, selection change, confirm, cancel, turn end and level end; null-safe in enemy turns, off the grid and with dead units.** Clearing is driven by the per-frame state check. *Tests:* `MovePreview_*_IsOff` (6 cases) plus `MovePreview_AllConditionsMet_IsOn`. *The live transitions need a play check.*
- [x] **No change to when a role fires, FTP, AP or AI.** The new code only reads, and the AI never calls it. The `AIRegressionTest` failure count is unchanged at 35.
- [x] **Compiles with no console errors.** Only warnings that were already there; the CS8509 in John and Mark is the old `PrepareTargets` switch. EditMode after the review round: **147 tests, 146 passed, 1 failed**, the known red `AIRegressionTest.Baseline_MatchesCurrentAI` (35 failures, the same as R3a).

## Save reset

No.

## Decisions I made

- **No hook in `PlayerController`.** The presenter polls `PlayerController`'s existing public getters each frame, so nothing in `PlayerController` changes. The work per frame is a handful of reference checks; zones are recomputed only on a change.
- **"Move preview" means target selection with the unit's default move ability** (`DefaultEmptyGridCellAction`), the walk that shows the ghost and path. Dash attacks, Command (moving another unit) and other movement abilities don't show cover icons. See Risks.
- **Overloads on the John and Mark handlers only, not on the base class.** The presenter picks the icon by handler type (John → shield, Mark → fist), so it needs those types anyway. This keeps the core change smallest.
- **The following zone sits next to the committed one:** the brief said not to erase it. It uses owner `int.MinValue`, so it sorts first and is the outermost outline on a cell they share, at full alpha. The committed zone stays at alpha 0.75.
- **Icons are tinted with the role unit's zone colour**, so the shield matches John's outline and the fist matches Mark's.
- **Placement:** the lower corners. The ghost unit stands in the middle of the tile and its sprite extends upward.

## Needs THJ

None.

## Docs to update

- `tech/combat-architecture.md`: the cover-icon layer (`GridCell.SetCoverIcons`, sorting order -5, the two Resources sprites), `MovePreviewCoverPresenter` and where it is hosted, the `GetCellsInRange(GridCell origin)` overloads on the John and Mark handlers, and the following-zone owner id `int.MinValue`.
- `design/gdd/family-systems.md` (designer): cover icons in the move preview, under the FR-8 draft. The fist is strict (D-067): it promises melee attackers next to you get punished, and does not cover ranged attackers.
- `build-log.md`: an R3b entry (coordinator).

## Risks and loose ends

- **Reviewer, core:** two additive public overloads on core handler classes. The existing methods are byte-identical. Please check that John's overload matches the `source: Unit` path for a one-cell John (`GridCell.GetRangeCells` uses the source's occupied cells as origins and then removes them; the overload starts from `origin` and removes `origin`). A multi-cell John would differ, but he is one cell. Also check one additive partial on `GridCell` (thread-sensitive): the new fields are touched only from the main thread, and the AI never calls `SetCoverIcons`.
- **Meaning of Mark's fist (settled by D-067):** the fist is strict and promises melee only. Attack spots are judged on the current board: an ally next to the tile now could move away, and a hazard could expire.
- **The icon checks range only.** John's `targetSelectTagQuery` (which allies he may cover) is not applied, as briefed ("only the range rule"). If a player unit fails John's tag query, it would still get a shield.
- **Scope of "move":** only the default walk. Command (Mark moves another unit), dashes and teleports don't show icons or a following zone.
- **Visual tuning untested:** the icon size of 0.3 of the frame, the corner offsets, the placeholder art, how readable the tint is on dark tiles, and the following zone at full alpha nested with the committed one.
- **Hover over UI:** the icons follow `GridManager`'s hover events, so they behave like the existing ghost and path when the pointer moves over UI.
- **Not mine, in the working tree:** `Features/Player/Lucy/Prefabs/Unit_Lucy.prefab` has `roleZoneColor` alpha changed from 0.749 to 1, and `Packages/`/`ProjectSettings/` are modified. These look like THJ's editor changes. They are not part of these commits.

## Proposed commits

Paths are under `miso/Assets/_Project/`. Each commit compiles on top of the ones before it.

1. `feat(roles): John and Mark role zone from a given cell, for the move preview (B4 R3b)` (**core**, Family Roles, additive):
   - `Features/Player/John/Scripts/JohnFactionRoleHandler.cs`
   - `Features/Player/Mark/Scripts/MarkFactionRoleHandler.cs`
2. `feat(grid): cover-icon overlay layer on GridCell (B4 R3b)` (**core**, Grid, additive):
   - `Core/Systems/GridSystem/Runtime/GridCell.CoverIcon.cs` + `GridCell.CoverIcon.cs.meta`
   - `Resources/GridOverlays/CoverShield.png` + `CoverShield.png.meta`
   - `Resources/GridOverlays/CoverFist.png` + `CoverFist.png.meta`
3. `feat(ui): shield and fist cover icons and the following role zone in the move preview (B4 R3b, D-063, D-067 strict fist)` (plain; uses 1 and 2):
   - `Core/Systems/RoleZoneSystem/Runtime/CoverIconRules.cs` + `CoverIconRules.cs.meta`
   - `Core/Systems/RoleZoneSystem/Runtime/MovePreviewCoverPresenter.cs` + `MovePreviewCoverPresenter.cs.meta`
   - `Core/Systems/RoleZoneSystem/Editor/CoverIconRulesTests.cs` + `CoverIconRulesTests.cs.meta`
   - `Core/Interactions/Runtime/ShowStatsHoverPreview.cs`

Do not stage `Unit_Lucy.prefab`, the R4 badge files (`Features/UI/Panels/Scripts/UnitPanelUI.cs`, `UnitPanelUI.RoleBadge.cs`, `RoleBadgeState.cs`, `Features/UI/Panels/Editor/` and their metas), `Packages/manifest.json`, `packages-lock.json` or `ProjectSettings/*`.

## Other branches

`thj/home-test`, on its next merge of `main`, together with R3a.

## How to see it

1. Open Unity, recompile (Ctrl+R), and start a combat level with John, Linda, Lucy and Mark.
2. Select **Lucy** and click an empty tile to enter the move preview. Hover destinations:
   - Inside John's orange zone: a small orange **shield** in the tile's lower-left corner.
   - All four sides of the tile that an attacker could step onto are inside Mark's green zone: a green **fist** in the lower-right corner. If only the tile itself, or only some of its sides, are inside his zone, there is no fist.
   - Inside both: both icons. Outside: none.
   - The path, ghost, threat lines and AP preview look as before.
3. Select **John** and enter the move preview. Hover a destination: an orange outline of his zone appears around the hovered tile, as the outermost ring. His current zone stays drawn. No shield on his own destination; a fist if the tile is in Mark's zone. Move the cursor and the preview zone follows. Leave the grid, right-click to cancel, or confirm the move: the preview zone and the icons disappear. After the move, the committed zone redraws at his new place.
4. Do the same with **Mark**: a green following zone, no fist on his own destination, a shield if the tile is in John's zone.
5. Switch units with Tab while hovering, and end the turn: nothing stays behind. Hover tiles during the enemy turn: no icons.
6. Untick `Show Role Zone` on John's role handler (Inspector, on the unit in play or on the prefab): no shields anywhere, and no following zone when moving John.
7. Kill John (cheats) and preview a move with Lucy: no shields.
8. Win or lose the level: no icons or outlines remain.
