# Role zones: each unit's own icon, in its own slot

Size: M    Tier: 3 (Family Roles UI; additive changes to two core files)    Assigned to: miso-implementer
Branch: thj/fr-readability
Status: waiting on THJ (go-ahead for the core changes)

## Why

R3a draws every Bergson's role zone with one sprite named in `GridCell.RoleZone.cs` (`RoleZoneSpritePath`; THJ's uncommitted test points it at `ShieldOutline`). THJ wants each unit to show its own icon (D-075). The new icons are white silhouettes, not 9-slice frames, so today's nesting (each further owner one step smaller inside the last) makes their lines cross. Each unit therefore gets a fixed quadrant of the cell instead.

## Goal

Every Bergson's role zone draws that unit's own icon, tinted with its role-zone colour and keeping the icon's aspect, in that unit's own quadrant of the cell. Sprite and quadrant are set in the Inspector on its role handler.

## Acceptance criteria

- [ ] `FactionRoleHandlerBase` has two Inspector fields next to `showRoleZone`: `roleZoneSprite` (Sprite) and `roleZoneSlot` (enum `RoleZoneSlot`: TopLeft, TopRight, BottomLeft, BottomRight), each with a tooltip and a public read-only accessor.
- [ ] The prefabs are set: John = `ShieldOutline`, TopLeft; Mark = `PunchOutline`, TopRight; Linda = `Arrow`, BottomLeft; Lucy = `Fireball`, BottomRight (all in `Resources/GridOverlays/`).
- [ ] On a cell, each zone entry draws its owner's sprite in its owner's quadrant. The sprite is fitted inside the quadrant with its aspect kept and is tinted with `RoleZoneColor`; the follow zone uses its colour made opaque, as today. Up to four zones on one cell never overlap.
- [ ] A lone zone on a cell still sits in its owner's quadrant; it does not move to the centre.
- [ ] Multi-cell occupants: the quadrants are quadrants of the whole footprint box (same anchor/footprint rule as today), so one icon per unit covers the footprint's quadrant, not one per cell.
- [ ] Empty `roleZoneSprite`: falls back to `Resources/GridOverlays/RoleZoneOutline`, fitted the same way. `RoleZonePresenter` warns once per handler for an empty sprite, and once in total if the fallback itself is missing.
- [ ] The move-preview follow zone (`MovePreviewCoverPresenter.DrawFollowZone`) uses the moving unit's sprite and slot.
- [ ] `RoleZoneSpritePath` goes back to naming only the fallback (`GridOverlays/RoleZoneOutline`). THJ's uncommitted ShieldOutline test line is replaced.
- [ ] Sorting order, layer and material are unchanged (−10, the move highlight's layer, `gridBaseVisual`'s material). Cover icons, the Shift preview layer and the John tether are untouched.
- [ ] EditMode tests: the quadrant fit (pure function: slot, box size, sprite aspect → centre and size) and the layer set keeping sprite and slot per owner (set, update, remove, order). The full suite passes except the known red.

## Scope

In: the core files `FactionRoleHandlerBase.cs` and `GridCell.RoleZone.cs` (both additive); `RoleZoneLayerSet.cs`; a new `RoleZoneSlot` and its layout helper in `RoleZoneSystem/Runtime`; `RoleZonePresenter.cs`; `MovePreviewCoverPresenter.cs`; tests; the four `Unit_*.prefab` files; the four sprite PNGs and their `.meta` files (untracked today).
Out: the cover icons (`CoverFist`/`CoverShield`); `BowArrow.png` (untracked, not used here; THJ to say what it is for); texture import settings (see Risks); the enemy `MasherGoblinFactionRoleHandler` (no zone drawn); the Shift preview layer.

## Touches

Systems: Grid (`GridCell`, core), Family Roles (`FactionRoleHandlerBase`, core), RoleZoneSystem (B4 code).
USPs: Family Roles (UI only; no rule change).
Docs: `tech/combat-architecture.md` (role-zone layer note), `plans/2026-10-18-family-role-phase0-1.md` (R3a follow-up row in its commit log), `build-log.md`, GDD `family-systems.md` (one line: each zone shows the unit's icon in its quadrant; designer).

## Approach

**C1: code** (model: opus; core). One commit.
1. `RoleZoneSystem/Runtime/RoleZoneSlot.cs`: the enum, plus a pure static `RoleZoneSlotLayout.Fit(RoleZoneSlot slot, Vector2 box, Vector2 spriteSize, float padding)`. It returns the local centre offset and the drawn size: the quadrant is half the box in each axis, minus padding, and the sprite is scaled uniformly to fit inside it. No Unity-object calls; EditMode-testable.
2. `RoleZoneLayerSet`: store `Sprite` and `RoleZoneSlot` per owner next to the colour (`SpriteAt`, `SlotAt`). `Set(ownerId, color, sprite, slot)` returns true when any of the three changed. Keep it pure (a Sprite reference is only stored and compared).
3. `FactionRoleHandlerBase`: add `[SerializeField] protected Sprite roleZoneSprite;` and `[SerializeField] protected RoleZoneSlot roleZoneSlot;` with tooltips ("UI only"), plus accessors `RoleZoneSprite` and `RoleZoneSlot`. These are new fields, so no rename and no `FormerlySerializedAs`.
4. `GridCell.RoleZone.cs`: `SetRoleZone(int ownerId, bool show, Color color, Sprite sprite, RoleZoneSlot slot)`. Callers are only the two presenters, and the removal calls pass defaults. Renderers become `SpriteDrawMode.Simple`, one per entry. Each gets `sr.sprite` = the entry's sprite (or the cached fallback), `sr.color`, and a localPosition/localScale from `RoleZoneSlotLayout.Fit`, inside a box = the move-highlight frame times a box inset constant (start at 0.9, named, tunable) plus the footprint extension already computed. Drop the nested-inset constants that become unused. Keep the cached fallback load (the cell-level `_roleZoneSprite` becomes the fallback only).
5. `RoleZonePresenter` and `MovePreviewCoverPresenter`: pass `handler.RoleZoneSprite` and `handler.RoleZoneSlot`. Change the OnEnable warning as in the criteria (per handler via the existing `_warnedHandlers` set).
6. Tests in `RoleZoneSystem/Editor/RoleZoneTests.cs` (or a new partial-style file `RoleZoneSlotTests.cs`).

**C2: data** (model: sonnet). One commit, after C1.
1. Stage the four PNGs and their `.meta` files as they are (THJ's assets; don't change their import settings).
2. In the four `Unit_*.prefab` files, set `roleZoneSprite: {fileID: 21300000, guid: <png guid>, type: 3}` and `roleZoneSlot: <0..3>` on the role handler component. Small YAML edits. If a field isn't serialized yet, add it at the end of that component's block. Guids: ShieldOutline `f24adfc063e819a4e8f50657d382633f`, PunchOutline `035591a4171ef2842a331a2c8ebb3798`, Fireball `7017ede89b3c1f449972307ef1bd25c4`, Arrow `69ff1ba09f0a37747bc89d57c2db5e82`. Check each meta's sprite fileID (single-sprite mode is `21300000`); if a meta lists a different id, use that one.

## Risks

- **Core files:** both changes are additive, and `SetRoleZone` has two callers, so the reviewer checks it. Its own commit can be reverted alone.
- **Statics:** none new. The fallback sprite cache stays per cell (instance field), as today.
- **Prefabs:** small YAML edits with the editor open. Unity picks them up on refresh; the verifier refreshes first. Don't touch any other part of the prefabs (D-066's Lucy blacklist is in the same file).
- **Downscaling:** the icons are 550–1046 px drawn at about a quarter of a cell, with no mipmaps and point filtering. They may shimmer or look jagged. That's a play-check item; the fix is an import setting (Max Size 128/256, or mipmaps) and THJ's call, not part of this plan.
- **Readability:** a lone zone is now a small corner icon, not a full outline. THJ chose that (D-075); the play check confirms it reads.
- **Follow zone** on the same cell as the same unit's own zone: both draw in the same quadrant, the opaque one on top (later owner id, as today). This is acceptable; note it in the report if it looks wrong.
- **AI:** not touched. **Save:** no change. **Other branches:** none (B4 lives on this branch).

## Gates

Compile clean / EditMode suite (known red only) / reviewer (core files) / play check: yes, needs THJ's time (Shift view with all four Bergsons, overlapping zones, Mark's footprint, a big enemy's footprint, the move-preview follow zone) / docs: as listed above.
