# Linda's quiver: code map

Owner: coordinator. Written 2026-10-29, when `thj/linda-quiver` merged into `main` (D-326). Design: the GDD Linda page (`design/gdd/characters/linda.md`). History: the plans named at the bottom.

## Where it lives

All of it is feature code in `Features/Player/Linda/Scripts/Quiver/` (Core never imports Linda, D-272). Editor tools and tests sit in `Quiver/Editor/`. Outside that folder:

- `Features/Player/Mark/Scripts/ProjectileCatchAndReturn.cs`, `CatchReturnRules.cs`: Mark's catch, quiver-aware.
- `Features/UI/Panels/Scripts/QuiverUI.cs` (the HUD prefab view, `Features/UI/Panels/Prefabs/UI/HUD/LindaQuiver.prefab`, instanced in `CharacterHUD.prefab`), `UnitPanelUI.Quiver.cs`, and `AbilitiesBarHUDUI` (hides Encore when the switch is off; raises the ability-press event the HUD feedback uses).
- Data: `Stat_LQuiverSize` in `Resources/Attributes/StatAttributes.asset` (base 3) and its entry on `Unit_Linda.prefab`; Encore = `Resources/UnitSpecific/Player/Linda/Abilities/Recall/Linda_Ability_Recall.asset` (2 AP).
- Core it relies on (see `core-systems.md`): `GlobalSettingsSO.lindaQuiverEnabled`; `Projectile` sweep and end cap; `AEffectSwapper` and `AEffectPusher` raising `unitEndMoving` (Watch).

## Main pieces

| Piece | Files | Job |
| --- | --- | --- |
| Quiver | `LindaQuiver` (+ partials `.Size`, `.Switch`, `.KillHandBack`, `.EncoreLine`, `.StackLabel`), `QuiverState`, `QuiverSizeRules` | The count; size from the stat at level start (fallback serialized 3); `LindaQuiver.Of(unit)` is null when the switch is off |
| Switch | `LindaQuiverSwitch`, `LindaQuiver.Switch` | Reads `GlobalSettingsSO.lindaQuiverEnabled` when Linda enters a level; off = everything below is skipped |
| Spending | `QuiverArrow` (on arrow projectiles), `QuiverAbilityInfo` | Spends in `Start`, lands on `onDisposeReady` at `transform.position`; which abilities spend comes from the projectile, not a list |
| Board | `GroundedArrowField` (+ `.Pickup`, `.KillHandBack`, `.Recall`, `.Ensure`), `GroundedArrowStacks`, `GroundedArrowLook`, `ArrowLandingRules`, `ArrowPickupRules`, `QuiverFieldRules` | Arrows on tiles (one icon + `xN`); pickup on plug by Linda's faction; hand-back on John's or Toba's primary kill (serialized preset list) |
| Encore | `RecallRules`, `RecallLines`, `LindaQuiver.EncoreLine` | Pulls her grounded arrows back; curved lines with the threat-line shine |
| Feedback | `QuiverPipsView`, `QuiverPipRules`, `QuiverReturnCue`, `HandBackLines`, `QuiverHudFeedbackRules`, `QuiverAimPresenter`, `QuiverPreviewRules` | Pips under her feet (shown on her Shift panel too; crossed arrow when empty), "+N" cue, HUD tint/lift/punch/glow, aim ghost (also after an auto move) |
| Log | `QuiverLogListener`, `QuiverLogLines` | ` · quiver N/M` suffix on her shot lines, ` · +N arrows` on pickups; no own lines |
| Level access | `QuiverLevelAccess` | Safe lookups during level start and restart |

## Rules worth knowing

- Domain reload is off: the field and switch statics have `PlayModeStaticReset` hooks.
- Toggling the switch takes effect at the next level.
- A Workshop "+1 quiver" item is data only: an `EquipmentSO` with an Additive +1 modifier on `Stat_LQuiverSize`.
- Encore in custom kits: `Tools > Levels > Linda > Add Encore To Custom Kits` (`EncoreKitTool.Levels`, 9 levels); `EncoreKitTests` checks them. A new level that overrides Linda's kit must be added to that list.

## History

`plans/2026-10-26-linda-quiver-tech.md`, `2026-10-28-quiver-readability-strip.md`, `2026-10-28-quiver-feedback-pass.md`, `2026-10-29-quiver-polish-2.md`, `2026-10-29-quiver-switch-size-encore-clamp.md`, `2026-10-29-swap-ends-move.md`.
