# Report: Feedback pass C5, HUD glow, portrait tint, item-pouch bob

Plan: plans/2026-10-22-feedback-pass-tech.md (section C5; design rev. 2, UX "Portrait and HUD" and the item-pouch row; D-146 to D-148)    Agent: miso-implementer    Branch: thj/quick-wins (on top of `31b8473d7`)
Outcome: done (compiles clean, EditMode green except the known red; not play-tested). The steady overlay (D-148) is not built.

## What changed

All files are LF; the new test file has a BOM like its neighbours. No scene, prefab or asset changes.

| File (under `miso/Assets/_Project/Features/`) | Lines | What |
|---|---|---|
| `UI/Panels/Scripts/UnitPanelUI.LowHealth.cs` (+ `.meta`, 2) | +248 (new) | new partial: follows the shown unit's mini bar, glow and tint images, pouch-bob trigger |
| `UI/Panels/Scripts/LowHealthHudRules.cs` (+ `.meta`, 2) | +28 (new) | pure statics: `BeatStrength`, `GlowAlpha`, `ShouldBob`, `BobScale` |
| `UI/Panels/Scripts/Editor/LowHealthHudRulesTests.cs` (+ `.meta`, 2) | +70 (new) | 8 EditMode tests |
| `UI/Panels/Scripts/UnitPanelUI.cs` | +3 / -0 | `SetupLowHealth(unit)` after the abilities bar is populated; `ForgetLowHealthSelection()` in `Hide`; `DisposeLowHealth()` in `OnDestroy` |
| `UI/Panels/Scripts/UnitPanelUI.RoleBadge.cs` | +5 / -1 | the existing `OnDisable` also calls `ForgetLowHealthSelection()` (a class can only have one) |
| `UI/Panels/Scripts/AbilitiesBarHUDUI.cs` | +7 / -0 | `BobItemPouch()` (the pouch button is private to the bar) |
| `UI/Panels/Scripts/UnitItemPouchButtonUI.cs` | +41 / -0 | `Bob()`, per-frame bob clock, `OnDisable` reset; serialized `bobPeakScale` 1.15, `bobDuration` 0.3 |
| `Effects/LowHealth/LowHealthPresenter.cs` | +11 / -0 | read-only `BeatStrength` (0..1) |

**Prefab hunks: none.** The task allowed prefab children; I built the glow and tint in code instead (the role badge pattern in `UnitPanelUI.RoleBadge.cs`): same behaviour, no YAML to hand-edit or clean. The new serialized fields on `UnitPanelUI` (foldout "Low health") take their defaults from the code, so `UnitPanel.prefab` does not change. If THJ wants to tune a colour in the inspector, Unity will write the value then.

## How it works

**Low state.** `SetupLowHealth` runs when the panel shows a unit: it takes that unit's `UnitMiniHealthBar` (`GetComponentInChildren`, including inactive) and uses its `IsLow` and `LowHealthChanged` event. No rule is duplicated (player faction only, 25%, dead is not low all come from C4). The subscription is dropped when another unit is shown, when the panel hides, on disable and on destroy. A unit with no mini bar, or whose bar is switched off (Deevoted, Lucy's decoy), never glows.

**Glow.** A child `LowHealthGlow` of the `UI_Element_FillBar` object (the `_healthBarFill` object, the bar's root), first sibling so it sits behind the bar's own children, stretched `pad` (10 canvas units, `lowGlowSize`) past the bar on every side. It has a `LayoutElement` with ignore-layout, raycasts off. The sprite is generated in code: a 32 x 32 texture, 9-sliced with an 8 px border, clear in the middle, brightest at the bar's edge, quadratic fade to clear at the outer edge, rounded corners. Sprite and texture are destroyed in `OnDestroy`. The root has no layout group and its mask sits on the `Mask_Shape` child, so nothing clips the glow (checked in the prefab hierarchy).

**Sync with the beat.** `LowHealthPresenter.BeatStrength` is the vignette's current alpha divided by `firstPeak`, clamped 0..1, set each `Update` from the same alpha the vignette uses and on the presenter's pausable clock (so it is 0 between beats and holds while paused). The panel reads it in `LateUpdate` (after the presenter's `Update`, so no frame of lag) and sets the glow alpha with `GlowAlpha(beat, steady, peak)`: 0.25 between beats (`lowGlowSteadyAlpha`), up to 0.9 at the first pulse (`lowGlowPeakAlpha`). The second pulse reaches about 0.69 of that, so the lub-dub reads as strong then weaker. The presenter is found with `FindFirstObjectByType` when the glow first shows and cached; no static, no new event. Without a presenter in the scene the glow just stays at the steady alpha. Glow colour `(0.85, 0.12, 0.08)`, serialized.

**Portrait tint.** A child `LowHealthTint` of `unitImage`, stretched to it, raycasts off, ignore-layout. The sprite is generated (4 x 64, white, alpha 1 at the bottom to 0 at the top); the image colour is the vignette's dark red `(0.42, 0.04, 0.04)` with alpha 0.35 (`lowPortraitTintColor`, `lowPortraitTintAlpha`), so the bottom is 0.35 and the top clear. Static (no pulse).

**Both clear** when the unit stops being low (event), dies (the bar clears its state), another unit is shown (`SetupLowHealth` releases the old bar first), or the panel hides or is disabled.

**Pouch bob.** `UnitPanelUI.SetupLowHealth` calls `abilitiesBar.BobItemPouch()` when `LowHealthHudRules.ShouldBob(isLow, newSelection, holdsHealingItem)`: the unit is low, this is a new selection, and it holds a healing item. "New selection" = a different unit from the one last shown, or the panel was hidden or disabled since (so re-populating the same unit, e.g. after a relic pick-up, does not bob again; selecting someone else and coming back does). The bob runs in `UnitItemPouchButtonUI.Update`: scale `1 + 0.15 * sin(pi * t / 0.3)` on the button's transform, `t` advanced by `LowHealthRules.PausableStep(unscaledDelta, timeScale)`, so it ignores slow-mo and stops at timeScale 0. There is no tween: the scale is set from the clock and restored on end, on disable and (via disable) on destroy; nothing to kill. The scale is multiplied onto the scale the button had when the bob began.

**HP-restoring item check.** For each item in `unit.AbilityOrchestrator.Items` that is not null, not `IsHidden` and `HasUsesLeft`: `ItemEffectPreview.GetHealthIncrease(item, unit) > 0`. That is the same check the pouch's hover preview uses: it reads the item's effects for modifiers on the global health attribute, simulates them on the unit's current health and clamps to the health it is missing. So only items whose effects change health, with uses left, that would heal something now. Items that cost only FP or AP do not count.

## Acceptance criteria

- [x] Pure logic (beat strength, glow alpha, bob decision, bob curve): `LowHealthHudRulesTests` (8 tests).
- [ ] Glow on the HUD bar pulsing with the heartbeat, steady glow between, portrait tint, both clearing on heal, death and selection change, bob once per selection, pause during the glow, no layout change: by construction, needs THJ's play check.
- [x] Compile clean: forced refresh and recompile through the Unity MCP (answered). The console shows only the project's existing warnings and, once after the domain reload, "Objects are trying to be loaded during a domain backup", which is the editor's own message.
- [x] EditMode **606/607**; the one failure is `AIRegressionTest.Baseline_MatchesCurrentAI` (the known red, untouched). 599 before plus 8 new.

## Save reset

No.

## Decisions I made

- **Built the glow and tint in code, no prefab edits** (same behaviour; the role badge does it this way).
- **Bob only on selection**, as written. A member who becomes low while already selected (e.g. by a counter-hit) glows but does not bob.
- **Bob waits for nothing**: it plays as the panel is populated, which is while the panel slides in. If THJ wants it after the slide-in, it is a small delay in `SetupLowHealth`.
- **The glow lives on the bar's root**, not its parent, so the glow follows the bar if the HUD moves it.

## Needs THJ

None blocking. Colours, glow size (10) and the 0.25 / 0.9 alphas are placeholders for your eye at the play check.

## Docs to update

- `design/gdd/combat-rules.md` "Combat feedback" (game designer): the HUD glow, portrait tint and pouch bob rows.
- Plan commit log (coordinator).

## Risks and loose ends

- **Panel `LateUpdate`:** `UnitPanelUI` had no `LateUpdate`; it now has one that returns at once unless a unit is low.
- **Glow over the bar's frame art:** the glow is a child of the bar root, so its ring is drawn over the root's own `Image` (the frame) and under the `Mask_Shape` child. The ring is clear inside the bar, so only its outer part shows. If the frame art looks tinted in play, the pad or the sprite needs adjusting.
- **Portrait is `UnitAvatar`** with an aspect ratio fitter; the tint is stretched to it, so it matches whatever the fitter gives.
- **Faction check:** units in an allied faction other than the player's never go low (C4 note), so they get no glow or bob.

## Proposed commits

1. `feat(ui): low-health glow, portrait tint and pouch bob on the HUD` (one unit; the partial needs the presenter's beat and the pouch hook; the tests go with it):
   - `miso/Assets/_Project/Features/UI/Panels/Scripts/UnitPanelUI.LowHealth.cs` + `.meta`
   - `miso/Assets/_Project/Features/UI/Panels/Scripts/LowHealthHudRules.cs` + `.meta`
   - `miso/Assets/_Project/Features/UI/Panels/Scripts/Editor/LowHealthHudRulesTests.cs` + `.meta`
   - `miso/Assets/_Project/Features/UI/Panels/Scripts/UnitPanelUI.cs`, `UnitPanelUI.RoleBadge.cs`, `AbilitiesBarHUDUI.cs`, `UnitItemPouchButtonUI.cs`
   - `miso/Assets/_Project/Features/Effects/LowHealth/LowHealthPresenter.cs`

   Not `Packages/` or `ProjectSettings/` (changes there predate this task).

## Other branches

`thj/home-test` gets it with `main`.

## How THJ can see it

Bring a Bergson to 25% HP or less (cheat menu or an enemy hit).

1. **Select a low member:** click the low Bergson. The HP bar in the HUD gets a red glow around it, steady and faint, flaring with each heartbeat (the vignette beat on selection, and the turn-start one). The portrait gets a red tint from the bottom, fading to clear at the top. Hit the member while selected so they cross 25%: the glow and tint appear with the announcement's three beats.
2. **Switch to a healthy member:** the glow and tint vanish at once. Switch back to the low one: they return.
3. **Heal a low member above 25%** while selected (item or ability): glow and tint disappear and the mini bar goes green. Drop them again: they return.
4. **Death:** let a selected low member die: glow and tint are gone.
5. **Pouch bob, with and without a healing item:** select a low member who holds a health item with uses left: the item pouch button bobs once (about 15% bigger and back in 0.3 s). Select a low member with no healing item (or only an FP/AP item, or an empty one): no bob. Select a healthy member holding a healing item: no bob. Selecting the same member again after another one bobs again; clicking a tile or ability on the same selected member does not.
6. **Pause during the glow:** open the pause menu mid-heartbeat: the glow freezes with the vignette and carries on at resume; a bob caught by the pause freezes mid-scale and finishes after.
7. **Layout:** the HUD panel does not move or resize when the glow appears or goes away.

## Review fixes

After the reviewer's APPROVE, these two should-fixes and nothing else:

1. **Glow and tint toggle the `Image` components, not the objects.** `SetLowHealthShown` is reached from the panel's `OnDisable`, so `SetActive` there could log "already being activated or deactivated". The two children are now created once with their image disabled, and shown or hidden with `Image.enabled`. (`UnitPanelUI.LowHealth.cs`)
2. **`BeatStrength` moved to `LowHealthRules`** (the heartbeat feature's own rules) with its two tests (`LowHealthRulesTests.cs`). `LowHealthPresenter` calls `LowHealthRules.BeatStrength`, and the added `using MISO.Content.UI.UnitPanel;` is gone. `LowHealthHudRules` keeps only the glow alpha, bob decision and bob curve (its test file lost the two tests).

Checks: forced refresh and recompile, no new errors. EditMode 606/607, only the known `AIRegressionTest.Baseline_MatchesCurrentAI` failing. Line endings and BOMs unchanged.

## Tint fix and bar background

Only `UnitPanelUI.LowHealth.cs` changed (LF).

- **Why the tint was faint:** the colour and alpha were applied once, when the tint image was created, so Inspector edits in Play did nothing. They are now re-applied every `LateUpdate` while the tint is shown.
- **Is the tint above the portrait?** Yes. In `CharacterHUD.prefab` (as nested in `UnitPanel.prefab`), `UnitAvatar` (sprite `Avatar_John` etc., `unitImage`) is the first child of `CharacterHUD`, whose own image is only the background art (`HUD_Background_0`) behind its children. Nothing is parented to the avatar and no mask or overlay frame sits over it, so the tint, a child of `unitImage`, draws right above the portrait art. The other siblings (fill bar, name bar, bottom bar) are elsewhere on the panel. No reparenting was needed. The main cause was the low default plus the live-edit bug.
- **Defaults:** tint alpha 0.5 at the bottom (was 0.35); the gradient now reaches clear about two-thirds of the way up (was the full height).
- **Bar background:** it is the `Image` on the bar's `Mask_Shape` child (`Mask_InsidePanels`, the dark track behind the fill; the bar root's `Panel_Fat_0` is the frame and is left alone). While low it is lerped from its original colour toward `lowBarBackgroundColor` (0.42, 0.04, 0.04) by `lowBarBackgroundBlend` (default 0.3), re-applied each `LateUpdate` so edits are live. Its original colour is stored once, the first time it is needed, and restored exactly when the unit stops being low, on another selection, on hide, and on disable or destroy (all go through the same release path). The glow is unchanged (0.25 resting, 0.9 peak).

Checks: forced refresh and recompile, no new errors. EditMode 606/607 (one failure). This run's results omitted the per-test list, so the failing test's name could not be read; the count matches the known red `AIRegressionTest.Baseline_MatchesCurrentAI`, and the AI regression report was printed to the console as before. Not play-tested.

### Bar track overlay (replaces the colour blend)

THJ's screenshot showed no red on the track. Cause: the blend target was the `Image` on `Mask_Shape`, but that `Mask` has `showMaskGraphic` off, so its image only masks and draws nothing; the lerp changed an invisible colour.

- **What draws the black:** the bar root's own `Image` (`Panel_Fat_0`, sliced), the frame art with the dark interior. It is left untouched.
- **The overlay:** `LowHealthTrack`, a child `Image` (no sprite, so a flat colour; raycasts off, ignore-layout) of `Mask_Shape`, set as its first sibling. Hierarchy: `UI_Element_FillBar` (frame, draws the black) > `Mask_Shape` (index 0 `LowHealthTrack`, then 1 `MainBarFill_Mask` with the green fill, then the decrease, secondary, locked and increase fills, and `BarNumLbl` last). So it draws after the frame, is clipped to the bar's masked shape, and sits under the fill, the damage and heal previews and the HP text.
- **Look:** `lowBarTrackColor` (0.42, 0.04, 0.04) at `lowBarTrackAlpha` 0.45, shown only while low (`Image.enabled`), re-applied each `LateUpdate` so edits are live.
- **Removed:** the colour lerp on `Mask_Shape` and its stored original colour (`lowBarBackgroundColor`/`lowBarBackgroundBlend` fields are gone), so nothing of the prefab's colours is touched any more.

Only `UnitPanelUI.LowHealth.cs` changed. Recompiled with no new errors; EditMode 606/607, the failure being `MISO.Core.Systems.AI.EditorTests.AIRegressionTest.Baseline_MatchesCurrentAI` (known red). Not play-tested.

Glow rest alpha set to 0 (`lowGlowSteadyAlpha` default 0, was 0.25): the HUD glow now follows the heartbeat only, 0 up to 0.9 and back, and is invisible between beats and after them. `LowHealthHudRules.GlowAlpha` and its tests take the rest value as an argument, so they needed no change. Recompiled clean; EditMode 606/607, failing test `AIRegressionTest.Baseline_MatchesCurrentAI` (known red).
