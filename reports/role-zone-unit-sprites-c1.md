# Report: Role zones, each unit's own icon in its own slot (C1, code)

Plan: plans/2026-10-19-role-zone-unit-sprites.md    Agent: miso-implementer    Branch: thj/fr-readability
Outcome: done (C1 only; C2 data not started, as asked)

## What changed

- `miso/Assets/_Project/Core/Systems/RoleZoneSystem/Runtime/RoleZoneSlot.cs` (new, + `.meta`): enum `RoleZoneSlot` (TopLeft=0, TopRight=1, BottomLeft=2, BottomRight=3), struct `RoleZoneSlotFit` (Center, Size) and pure static `RoleZoneSlotLayout.Fit(slot, box, spriteSize, padding)`.
- `Core/Systems/RoleZoneSystem/Runtime/RoleZoneLayerSet.cs`: stores a Sprite and a RoleZoneSlot per owner, next to the colour (`SpriteAt`, `SlotAt`). `Set(ownerId, color, sprite, slot)` returns true when any of the three changed. The sprite is compared with `ReferenceEquals`, so the set stays pure.
- `Core/Systems/AbilitySystem/Abilities/Runtime/FactionRoleHandlerBase.cs` (**core**, additive): `[SerializeField] protected Sprite roleZoneSprite;` and `[SerializeField] protected RoleZoneSlot roleZoneSlot;`, each with a "UI only" tooltip, right after `showRoleZone`. Read-only accessors `RoleZoneSprite` and `RoleZoneSlot`.
- `Core/Systems/GridSystem/Runtime/GridCell.RoleZone.cs` (**core**, additive):
  - The new signature is `SetRoleZone(int ownerId, bool show, Color color, Sprite sprite, RoleZoneSlot slot)`. Renderers are `Simple`, one per entry, each fitted into its slot's quadrant with `RoleZoneSlotLayout.Fit`.
  - The box is the Move frame times `RoleZoneBoxInset = 0.9` plus the footprint's extra cell steps. Padding is `RoleZoneSlotPadding = 0.03` of the one-cell frame's shorter side.
  - The nested-inset constants are gone. `RoleZoneSpritePath` is back to `GridOverlays/RoleZoneOutline` only, which replaces THJ's ShieldOutline test line. The fallback sprite is cached per cell.
- `Core/Systems/RoleZoneSystem/Runtime/RoleZonePresenter.cs`: passes `handler.RoleZoneSprite` and `RoleZoneSlot` to the cells. It warns once per handler when the sprite is empty, and once if the fallback itself is missing.
- `Core/Systems/RoleZoneSystem/Runtime/MovePreviewCoverPresenter.cs`: the follow zone uses the moving unit's sprite and slot. The stale "outermost outline" comment is updated.
- `Core/Systems/RoleZoneSystem/Editor/RoleZoneTests.cs`: the existing LayerSet tests now call the 4-argument `Set` (null sprite, default slot). Assertions are unchanged.
- `Core/Systems/RoleZoneSystem/Editor/RoleZoneSlotTests.cs` (new, + `.meta`):
  - Fit: quadrant centres, aspect kept (wide and tall sprites), padding, four slots never overlapping and staying inside the box, footprint box, degenerate inputs.
  - LayerSet: sprite and slot kept per owner, unchanged values return false, a sprite or slot change counts as a change, remove keeps the lists aligned, order by owner id.

Encoding: every file kept its line endings and BOM. All files here are LF. `GridCell.RoleZone.cs` and `FactionRoleHandlerBase.cs` keep their BOM, and `FactionRoleHandlerBase.cs` still has no final newline. The new files match their folder: LF, no BOM.

`git diff --stat` (tracked files under `miso/Assets/_Project/Core`):

```
 .../Abilities/Runtime/FactionRoleHandlerBase.cs    | 11 +++
 .../GridSystem/Runtime/GridCell.RoleZone.cs        | 86 +++++++++++++++-------
 .../Systems/RoleZoneSystem/Editor/RoleZoneTests.cs | 22 +++---
 .../Runtime/MovePreviewCoverPresenter.cs           |  8 +-
 .../RoleZoneSystem/Runtime/RoleZoneLayerSet.cs     | 23 +++++-
 .../RoleZoneSystem/Runtime/RoleZonePresenter.cs    | 18 ++++-
 6 files changed, 120 insertions(+), 48 deletions(-)
```
Untracked: `RoleZoneSlot.cs` (56 lines) + `.meta`, `RoleZoneSlotTests.cs` (183 lines) + `.meta`.

Note: the `GridCell.RoleZone.cs` diff against HEAD also includes reverting THJ's uncommitted ShieldOutline line, so HEAD's `RoleZoneOutline` constant is kept.

## Acceptance criteria

- [x] Two Inspector fields next to `showRoleZone` (`roleZoneSprite`, `roleZoneSlot`), each with a tooltip and a public read-only accessor. Compiles.
- [ ] The prefabs are set (John/Mark/Linda/Lucy sprites and slots): **C2, not in this chunk.** Until C2 lands, all four handlers have an empty sprite (fallback outline) and slot TopLeft (enum default 0). Each presenter warns once per handler.
- [x] Each entry draws its owner's sprite in its owner's quadrant: aspect kept (uniform scale from `Fit`), tinted with `RoleZoneColor`, follow zone opaque as before. Four zones never overlap: tests `Fit_FourSlots_NeverOverlap_AndStayInsideTheBox` and `Fit_CentresInItsQuadrant`. The on-screen look needs the play check.
- [x] A lone zone stays in its owner's quadrant: the position depends only on the slot, never on the entry count or index. Play check.
- [x] Multi-cell occupants: one icon per unit in the footprint box's quadrant. The anchor/footprint rule is unchanged (redirect to the anchor, centroid offset); the box adds `(cells-1) * cellStep`. Test `Fit_FootprintBox_UsesQuadrantsOfTheWholeBox`; the play check covers Mark and a big enemy.
- [x] Empty sprite falls back to `Resources/GridOverlays/RoleZoneOutline`, fitted the same way. Warnings: once per handler for an empty sprite, once if the fallback is missing. If the fallback is missing, entries without a sprite are hidden; entries with their own sprite still draw. Play check (console).
- [x] Move-preview follow zone uses the moving unit's sprite and slot. Play check.
- [x] `RoleZoneSpritePath` names only `GridOverlays/RoleZoneOutline`, and the ShieldOutline line is gone.
- [x] Sorting order -10, the Move highlight's layer and `gridBaseVisual`'s material and sorting layer are unchanged. Cover icons, the Shift preview layer, the tether and the enemy handler are untouched.
- [x] EditMode tests for the quadrant fit and for the layer set's sprite and slot (set, update, remove, order). Full suite: 191 total, 190 passed, 1 failed (only the known red `AIRegressionTest.Baseline_MatchesCurrentAI`, 35 failures in its report, not touched). The RoleZoneSystem group run alone passes 90/90. I ran it through the Unity MCP in THJ's open editor, after a refresh: compile clean, no new CS errors or warnings.

Coverage: the fit and the bookkeeping have tests. The rendering (sprite assignment, scale, footprint box, warnings) needs the verifier's play check.

## Save reset

No.

## Decisions I made

- **Separate warning set.** The empty-sprite warning uses its own `_warnedNoSpriteHandlers` set rather than the existing `_warnedHandlers`. A shared set would let a sprite warning silence a later "could not give its role zone" exception warning for the same handler. The behavior is still once per handler for each warning. The fallback warning is guarded by an instance bool (`_warnedNoFallback`), not a static.
- **Root scale.** The role-zone root is now unscaled (`localScale = one`), and the box is computed in overlay space (`frame = baseSize * |baseScale|`), the way `GridCell.CoverIcon.cs` sizes its icons. This keeps the icon's aspect even if the Move frame's scale is non-uniform. The box is the same world size the old code produced.
- **Padding.** `Fit`'s padding is kept free on every side of the icon inside its quadrant. In `GridCell` it is a fraction (0.03) of the one-cell frame's shorter side, so big footprints don't get bigger margins.
- **Degenerate fit.** An entry whose sprite is missing (no own sprite and no fallback) or has zero size is hidden instead of drawn at size zero.
- **Unknown slot values.** Undefined enum values fall to BottomRight (the right/bottom branch of `IsLeft`/`IsTop`).
- Renderer objects are named `RoleZoneIcon_<i>` (was `RoleZoneOutline_<i>`). They are created at runtime only, so nothing references the name. The private cache is renamed `_roleZoneFallbackSprite` and loaded lazily once per cell. It is an instance field, not serialized, and no static was added.

## Needs THJ

None for C1.

## Docs to update

- `tech/combat-architecture.md`: the role-zone layer note now reads "one Simple renderer per owner; owner's sprite (fallback RoleZoneOutline) in its RoleZoneSlot quadrant of the frame×0.9 + footprint box", where it used to read "nested sliced outlines".
- `plans/2026-10-19-role-zone-unit-sprites.md`: tick C1 and log the hash once committed.
- `build-log.md`: a C1 section.

## Risks and loose ends

- **Follow zone draw order.** The plan says the opaque follow zone draws on top of the moving unit's own zone ("later owner id"). In fact `FollowZoneOwnerId = int.MinValue` sorts first, and both renderers share sorting order -10, so which one is on top is not guaranteed. The follow zone is opaque, so it should read either way. Watch for it in the play check. If it looks wrong, a +0 / depth-nudge fix is a small follow-up (not done; it would change behavior).
- **Until C2,** all four Bergsons are in TopLeft with the fallback outline, so their zones overlap on shared cells and each logs one warning. This is expected until the prefabs are set.
- **Fallback look.** `RoleZoneOutline` is a 9-slice frame. Drawn Simple in a quadrant, it shows as a small square outline in the corner. This is only a fallback.
- **Unity error.** The console shows one "Internal error - unexpected guid mismatch" after the refresh. It is not a compile error, and it is most likely from asset import (THJ's untracked PNGs were imported in the same refresh). I didn't investigate; worth a glance if it repeats.
- The downscaling and shimmer risk of the large icons is still open (import settings, THJ's call; C2/play check).

## Proposed commits

1. `feat(grid): draw each role zone as its unit's own icon in its own quadrant` (**core**, plain otherwise). Files:
   - `miso/Assets/_Project/Core/Systems/RoleZoneSystem/Runtime/RoleZoneSlot.cs`
   - `miso/Assets/_Project/Core/Systems/RoleZoneSystem/Runtime/RoleZoneSlot.cs.meta`
   - `miso/Assets/_Project/Core/Systems/RoleZoneSystem/Runtime/RoleZoneLayerSet.cs`
   - `miso/Assets/_Project/Core/Systems/AbilitySystem/Abilities/Runtime/FactionRoleHandlerBase.cs`
   - `miso/Assets/_Project/Core/Systems/GridSystem/Runtime/GridCell.RoleZone.cs`
   - `miso/Assets/_Project/Core/Systems/RoleZoneSystem/Runtime/RoleZonePresenter.cs`
   - `miso/Assets/_Project/Core/Systems/RoleZoneSystem/Runtime/MovePreviewCoverPresenter.cs`
   - `miso/Assets/_Project/Core/Systems/RoleZoneSystem/Editor/RoleZoneTests.cs`
   - `miso/Assets/_Project/Core/Systems/RoleZoneSystem/Editor/RoleZoneSlotTests.cs`
   - `miso/Assets/_Project/Core/Systems/RoleZoneSystem/Editor/RoleZoneSlotTests.cs.meta`

   One commit, as the plan says. The new signatures of `SetRoleZone` and `RoleZoneLayerSet.Set` break every caller and test unless they land together, so the commit can't be split without leaving a non-compiling state. Don't stage the other dirty files (`Packages/*`, `ProjectSettings/*`, the PNGs; the PNGs are C2).

## Other branches

None.

## How to see it

1. Stop Play mode if needed, then Ctrl+R in Unity.
2. Open any Bergson unit prefab (e.g. `Features/Player/John/Prefabs/Unit_John.prefab`). On its role handler, under Show Role Zone, you should see **Role Zone Sprite** and **Role Zone Slot**, each with a tooltip.
3. Before C2: start a combat level, select a Bergson and hold Shift. Each zone shows the small fallback outline in the top-left quadrant, and the console has one "has no roleZoneSprite" warning per handler.
4. To preview what C2 will do, set the sprite and slot by hand on the four prefabs in Play (or in the prefab, then undo): John ShieldOutline TopLeft, Mark PunchOutline TopRight, Linda Arrow BottomLeft, Lucy Fireball BottomRight. Then hold Shift: overlapping zones show up to four tinted icons on a cell, one per corner. Also check Mark's and a big enemy's footprint (one icon per unit per footprint quadrant) and the move preview of John or Mark (the follow zone in their own corner, opaque).
