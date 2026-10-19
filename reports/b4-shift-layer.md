# Report: B4 Shift hover preview on its own GridCell layer (option D)

Plan: none (coordinator brief, D-071 option D)    Agent: miso-implementer    Branch: thj/fr-readability
Outcome: done (compiles, EditMode 174/175 with only the known red; not play-checked)

## What changed

- `miso/Assets/_Project/Core/Systems/GridSystem/Runtime/GridCell.ShiftPreview.cs` (new, LF + BOM like its neighbours) and its `.meta` (Unity-generated): the Shift preview layer. `[Flags] enum ShiftPreviewLayer { None, Move, Attack }` and `GridCell SetShiftPreview(ShiftPreviewLayer layer, bool show)`. It works like `SetRoleZone`: removal is local first, otherwise it redirects to `OverlayOrigin` (the anchor cell of a multi-cell occupant) and returns the cell that holds the entry. The renderers are created on first use under a new `ShiftPreview` root. That root is a sibling of the real overlays under `Visual` (same parent as the RoleZone/CoverIcons roots), so it stays out of the footprint-fit cache. Three renderers copy the real ones at runtime (sprite, draw/tile mode, shared material, sorting layer, base transform from the overlay cache): `ShiftMove` from `gridCellHighlightMoveVisual`, `ShiftMoveGlow` (a child of `ShiftMove`, the same nesting as in the prefab) from `gridCellHighlightMoveGlowVisual`, and `ShiftAttack` from `gridCellIconInAttackRangeVisual`. The move frame and glow grow to a multi-cell footprint and the attack icon is only re-centred, both following `FitOverlaysToOccupantFootprint`. Every renderer access is null-guarded (`if (!sr) return;`). The layer reads `_isActive`, `OverlayEntity` and the overlay cache. It never writes another layer's flags or renderers.
- `miso/Assets/_Project/Core/Systems/GridSystem/Runtime/GridCell.cs` (core, +1 line): `SetAlphaAll` now also calls `SetShiftPreviewFade(alpha)`, so the layer follows the grid fade (it recolours only while something is shown). This is the only change in the main file.
- `miso/Assets/_Project/Core/Interactions/Runtime/ShowStatsHoverPreview.cs`: keeps the uncommitted revive fix (Rebind, hosting lines unchanged). The four calls became `SetShiftPreview(ShiftPreviewLayer.Move/Attack, true/false)`, and the preview now stores the returned cell, so clearing hits the cell that holds the entry. The `CanShowPreview` comment was updated to say why the guard is still needed (future-target hover, see Risks). No other logic changed. LF, no BOM.

## Values chosen (consts in GridCell.ShiftPreview.cs)

| What | Value | Effect |
|---|---|---|
| `ShiftPreviewAlpha` | 0.55 | alpha relative to the real highlight; the grid fade multiplies on top |
| `ShiftPreviewTintBlend` | 0.35 | real colour lerped 35 % toward the tint |
| `ShiftPreviewMoveTint` | (0.55, 0.75, 1.0) | move frame/glow: vertex colour white becomes (0.84, 0.91, 1.0), so the teal-green shader frame turns slightly cooler and bluer |
| `ShiftPreviewAttackTint` | (0.85, 0.30, 0.65) | attack icon: prefab red (0.57, 0.15, 0.15) becomes (0.67, 0.20, 0.32), slightly pinker and lighter |
| `ShiftPreviewSortingOffset` | -1 | each Shift renderer sorts one order below the real one it copies: Move -8 to -9, Move glow -7 to -8, InAttackRange -9 to -10 |
| `ShiftPreviewDepthNudge` | 0.01 world +Z | where a Shift renderer ties with a different real visual (Shift move -9 vs the real attack icon/targeted/path at -9; Shift glow -8 vs the real Move/Ability frame at -8), it draws below. Transparency sort mode is Default (camera distance), checked in GraphicsSettings and Renderer2D |

These are consts, not serialized fields, so the GridCell prefab's serialized shape does not change. Tweaking them means editing the file.

## Acceptance criteria

- [x] Own layer, lazily created, separate root, OverlayOrigin redirect, null-guarded, never touches the other layers' flags: code review; compiles.
- [x] Copies the move and attack-range visuals at runtime: `CopyOverlayRenderer` from the serialized renderers.
- [x] Respects the grid fade: `SetAlphaAll` hook (1 line in the core file).
- [x] Readability: alpha 0.55, a different tint, sorting just below the real highlights, z-nudge tie-break. Needs a visual play check.
- [x] Clears on cell destroy: the renderers are children of the cell and are destroyed with it. The preview's stored cells are Unity-null-checked before clearing. No `OnDestroy` was added (none of the other layers have one).
- [x] Preview swapped to the layer API; hosting and Rebind kept.
- [ ] Release keeps the selected range lit, 2x2 footprint, fade, look: needs the verifier's or THJ's play check (steps below).
- Tests: none added. The only pure piece is the colour formula (`internal static ShiftPreviewColor`), and `internal` is not visible to the editor test assembly. Making it public just for a trivial lerp was not worth it.
- Verification: refresh + compile clean (the only console error is the known unrelated "Internal error - unexpected guid mismatch"). EditMode: 175 total, 174 passed, 1 failed = the known red `AIRegressionTest.Baseline_MatchesCurrentAI`.

## Save reset

no

## Decisions I made

- API is `SetShiftPreview(ShiftPreviewLayer, bool)` with flags rather than `SetShiftPreview(bool move, bool attack)`. The preview sets move and attack in two separate loops, so a two-bool setter would switch off the move frame when the attack loop marks the same cell.
- Plain flags, no per-owner ref-count: the Shift preview is the only writer of this layer. If several cells redirect to one anchor, the duplicate set or clear is idempotent.
- Like `SetHighlight`, an inactive cell does not show the move part. The attack part has no such guard, the same as `SetInAttackRange`.
- Fade is applied through a one-line hook in `SetAlphaAll` instead of reading the base renderer's alpha at show time, so the layer also follows a fade that runs while the preview is shown.
- Only the default attack-range icon is copied, not `gridCellIconInAttackRangeOverrideVisual` (the preview never used the sprite override).

## Needs THJ

none (the look of the values above is for the playtest; change the consts if it reads wrong)

## Docs to update

- `reports/b4-shift-hover-fix.md` / status backlog: the move/attack clash from the revive is resolved by this layer. The future-target clash (below) stays open.
- `tech/` grid notes (if any list GridCell layers): add the Shift preview layer next to RoleZone and CoverIcon.

## Risks and loose ends

- **Future-target hover has the same class of clash, unchanged as instructed.** `GUnit.SetFutureTargetsHover` (GUnit.cs ~L1334) writes `GridCell.SetPotentiallyTargeted(true/false)`, a plain bool. The same bool is written by `FactionControllerBase.SetPotentiallyTargetedCells` (target selection with `ShowPotentiallyTargetedHighlight`, ~L593/615/690), `AEffectCompound.SetPotentiallyTargetedCells`, and the Masher Goblin role preview (`MasherGoblinFactionRoleHandler.cs` L417/L454). Releasing Shift clears overlapping cells. The target-selection case is covered by the `CanShowPreview` guard (`IsSelectingAbilityTarget`). The Masher Goblin role preview overlap is still possible if it is up while you Shift-hover a unit whose future action targets the same cells. `SetPotentiallyTargeted` also hides the hover visual on those cells.
- Core file touched: `GridCell.cs` gets one line in `SetAlphaAll`, plus the new partial, which is part of a core class. Separate commit below.
- The z-nudge assumes the camera looks along world +Z with Default sort mode (true for the current settings). With a different camera or sort axis the tie-break may not hold, but the sorting offsets still keep each Shift renderer below its real counterpart.
- The layer is fitted when it is set. If a 2x2 occupant moves while Shift is held and the preview is not refreshed, the frame keeps the old footprint until the next hover. RoleZone has the same limitation.
- The tint goes through vertex colour. The move material is a URP Sprite Unlit shader graph (`SH_ColorReplacer`), which multiplies by vertex colour (the existing grid fade depends on that too). If it did not, the alpha would not show; verify in play.
- Hovering the selected unit itself now draws the softer copy under its real range, so the cells look almost unchanged. That is expected.

## Proposed commits

1. `feat(grid): Shift preview layer on GridCell with its own renderers, softer tint, below the real highlights (B4, D-071)` (core):
   - `miso/Assets/_Project/Core/Systems/GridSystem/Runtime/GridCell.ShiftPreview.cs`
   - `miso/Assets/_Project/Core/Systems/GridSystem/Runtime/GridCell.ShiftPreview.cs.meta`
   - `miso/Assets/_Project/Core/Systems/GridSystem/Runtime/GridCell.cs`
2. `fix(interactions): revive the Shift hover preview on the live bus and draw it on the Shift layer (B4, D-064, D-071)` (plain; depends on 1):
   - `miso/Assets/_Project/Core/Interactions/Runtime/ShowStatsHoverPreview.cs`

Do not stage `Packages/*` or `ProjectSettings/*` (pre-existing unrelated changes).

## Other branches

none known

## How to see it

1. Enter a combat level with nothing selected. Hold Shift and hover a unit: its reachable cells show a softer, slightly bluer move frame, and its attackable cells show a softer, pinker attack icon. Release Shift or move off: they disappear.
2. Select a player unit so its move range is lit. Hold Shift and hover a nearby unit whose range overlaps: on shared cells the selected unit's real frame stays bright on top. Release Shift: the selected unit's range must still be fully lit, with no dark holes.
3. With the unit selected, Shift-hover the selected unit itself: no change to its real range, and after release the range is still lit.
4. With Shift held and a unit selected, the role-zone outlines still show and are unchanged.
5. Shift-hover a 2x2 unit and a unit next to one: a 2x2 occupant in the attack range shows one centred attack icon on its footprint, and move frames are not doubled.
6. Hover a HUD role icon (attack-range icons) and Shift-hover a unit at the same time if you can, then release: the HUD icon's cells stay.
7. Grid fade: with Shift held at a level transition, or during a sequence that fades the grid, the Shift layer fades with the grid.
8. Readability check: on overlapping cells you should be able to tell the real range (bright) from the Shift copy (soft). If not, tune `ShiftPreviewAlpha` / tints in `GridCell.ShiftPreview.cs`.
