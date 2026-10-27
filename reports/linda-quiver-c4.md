# Report: Linda's Quiver, C4 (Readability)

Plan: plans/2026-10-26-linda-quiver-tech.md (chunk C4 and the "added after the play check" items)    Agent: miso-implementer    Branch: thj/linda-quiver
Outcome: partial. Everything is built and written but **not compiled or run** (the Unity editor is open, so no batch run; the editor had not recompiled when I checked its log). Item 7 (the move preview "+N arrows") is built only up to a hook that needs one small core change; it shows nothing until that lands. No core-system code was changed.

THJ: please let Unity recompile, then run Window > General > Test Runner > EditMode > Run All. If anything fails to compile, send me the first error lines.

## What changed

Paths under `miso/Assets/_Project/`. LF, no BOM, a `.meta` for every new file. All strings say "Encore" (code and asset names stay Recall).

New, `Features/Player/Linda/Scripts/Quiver/` (all with `.meta`):
- `QuiverPipRules.cs`: pure. Pip count, filled state, when pips show, pip offsets, "Quiver 3/4", zone hidden when empty.
- `QuiverTextRules.cs`: pure. `QuiverNeed` enum; Watch prompt "Arrows 3 > 2"; grey reasons; tooltip join; "+N arrow(s) (N left)".
- `QuiverPreviewRules.cs`: pure. `QuiverPreviewRules.ArrowsPicked` (path count), `LandingMarkerRules` (marker cell through `ArrowLandingRules`), `ReturnCueRules` (cue count, text, fade).
- `QuiverSprites.cs`: placeholder art drawn in code (arrow, glow, ring, pixel); nothing cached, the quiver owns what it makes.
- `QuiverAbilityInfo.cs`: finds the arrow abilities, the Duos with a Linda arrow, and Encore from their own effect data (no name matching). Gives the grey reason.
- `QuiverPipsView.cs`: arrow pips under Linda's unit (world sprites, a sibling of the mini health bar, added at run time by `LindaQuiver`).
- `QuiverReturnCue.cs`: the "+N" cue on Linda for every return, plus a short glow on Mark when he catches. Added at run time by `LindaQuiver`.
- `QuiverAimPresenter.cs`: landing marker while aiming the bow, Crescendo or an arrow Duo; Encore lines from each grounded stack to Linda while Encore is hovered on the bar or selected. Lives on the level's field object.
- `QuiverMovePreviewPresenter.cs`: "+N arrows" at the move preview's destination. Dormant until the player controller reports its preview path (see Needs THJ).
- `QuiverPromptLabel.cs`: the "Arrows 3 > 2" line beside Linda while the Watch prompt is up.
- `Editor/QuiverReadabilityTests.cs`: about 45 tests.

New elsewhere (with `.meta`): `Features/UI/Panels/Scripts/UnitPanelUI.Quiver.cs` (panel pips + "Quiver 3/4" label, hover forwarding for Encore lines), `Features/UI/Panels/Editor/RoleBadgeQuiverTests.cs` (5 tests).

Edited:
- `LindaQuiver.cs`: `QuiverReturnKind` enum; `Add(amount, kind)` and the `OnReturned` event (one per return, after `OnChanged`; `Add(int)` still works); `ArrowIcon`, sprite accessors owned and destroyed by the quiver; `HidesRoleZone`; adds the pips view and return cue in `Start`.
- `QuiverArrow.cs`: **the arrow-with-nowhere-to-land fix**: if the field is missing, closed, or the cell is gone, the arrow goes back to the quiver (`QuiverReturnKind.Landed`) instead of vanishing. The catch return is tagged `Catch`. Exposes `Mode`; tells the quiver its icon.
- `GroundedArrowField.cs` / `.Pickup.cs` / `.Recall.cs`: locked look (below), pickups and Recall tagged with their kind, `Quiver` getter, `StackIconPosition`, `CellSpacing` now internal, the two presenters added in `GetOrCreate`.
- `Features/UI/Panels/Scripts/`: `RoleBadgeState.cs` (new `EmptyQuiver` state, 3-arg `Evaluate`, tooltip line), `UnitPanelUI.RoleBadge.cs` (state source, colour, tooltip), `UnitPanelUI.cs` (4 one-line hooks), `AbilitiesBarHUDUI.cs` (tooltip reason, `AbilityHovered` event), `FactionRoleVisual.cs` (one call in `SetData`).
- `Core/Systems/RoleZoneSystem/Runtime/RoleZonePresenter.cs` and `MovePreviewCoverPresenter.cs`: Linda's zone is not drawn at 0 arrows (also the follow zone in the move preview, for consistency); `RoleZonePresenter` redraws when her quiver empties or refills. These are UI presenters, not on the core list.
- `Resources/UnitSpecific/Player/Linda/Abilities/Recall/Linda_Ability_Recall.asset`: `title` is now "Encore". `QuiverWiringTests.cs`: title check updated, plus one test that finds Encore and the bow from their data.
- `ProjectileCatchAndReturn.cs` is **not touched** (C3b can rework it): the catch cue and flash come from the quiver's `Catch` return, and the flash finds Mark through the component in the scene.

## Acceptance criteria

EditMode coverage is the pure rules. Everything else needs a play check (nothing was run).

- [x] Arrow pips under Linda: `QuiverPipRules` tested. Play: step 1.
- [x] Pips on the unit panel: rules tested. Play: step 2.
- [x] Badge empty-quiver state: `RoleBadgeQuiverTests`. Play: step 3.
- [x] Zone hidden at 0: `ZoneShown` tested. Play: step 4.
- [x] Watch prompt "Arrows N > N-1": tested. The TMP default font (`LiberationSans SDF`, static, no fallbacks) has no U+2192, so the prompt uses ">". Play: step 5.
- [x] Grey reasons: tested ("No arrows", "Linda has no arrows", "No grounded arrows", "Quiver full"). Play: step 6.
- [x] Landing marker: `LandingMarkerRules` tested against `ArrowLandingRules`; the bow's last-enemy-hit comes from `Projectile.CollectPreviewPathHits`. Play: step 7.
- [ ] Move preview "+N arrows": counting rule and label tested; the polling presenter is written but inactive (needs the hook). See Needs THJ. Play: step 8 after the hook.
- [x] Encore lines: play only (drawing). Step 9.
- [x] Return cue for catch, any pickup (own, instant on landing), Encore, plus Mark's flash: event count tested (`Quiver_Raises...`, `ReturnCueRules`). Play: step 10.
- [x] Locked look and count badge on a single arrow: play only (visual). Step 11.
- [x] Arrow with nowhere to land goes back: the contract (`Land` refuses on a closed field) is tested; the `QuiverArrow` branch itself is not (needs a live projectile). Play: step 12.

## Save reset

No.

## Decisions I made

- **Pips are world sprites on Linda's unit, added at run time** by `LindaQuiver.Start`, not a prefab edit. Same behavior, no YAML.
- **Placeholder art is drawn in code** (`QuiverSprites`), because the arrow sprite is only known after the first shot and the pips must show from turn one. The quiver owns and destroys its sprites, so there are no statics and nothing to reset.
- **Reasons come from the abilities' own effects** (spawner with a `QuiverArrow` projectile, `AEffectFunctionCaller` "Recall", `AEffectCoOpTrigger` to the cooperation entry's Linda partner), because `activationFeasibilityCheckFunction` is protected.
- **Cues listen to `LindaQuiver.OnReturned`**, not to the field, so they do not depend on the stacks having redrawn.
- **Mark's flash finds him with `FindFirstObjectByType<ProjectileCatchAndReturn>`** to keep that file untouched. Fine with one Mark; C3b may replace it with an event carrying the catcher.
- **Lobbed vs ranged shot** for the marker is read from the projectile's public `TrajectoryMode` (Crescendo is `VerticalFactor`; the others travel their whole range), since `travelEntireRadius` is private.
- **Locked look:** every grounded arrow now has a dark outline (a larger copy of the sprite behind it) so it reads on busy art; locked is bright orange, red outline, red count badge, fully opaque. The count badge shows on single arrows too.
- **Encore lines and landing marker** are separate objects on the field, so they vanish with the level.
- Encore's `description` text is unchanged (still the tagged placeholder).

## Needs THJ

**Item 7 needs a small additive core change, so I stopped there.**
- Context: the move preview's walking path (and which of the Tab-cycled paths is shown) is held in `PlayerController._previewPath`, private. The path cells' highlight sprite is a private field on `GridCell`. Nothing public tells a presenter which path is drawn.
- Options: (a) the additive hook below; (b) compute the first path myself, which is wrong after Tab; (c) skip the label.
- Recommendation: (a). Two lines in `PlayerController.cs`: `public class PlayerController : FactionControllerBase, IMovePreviewPathSource` and `public IReadOnlyList<GridCell> PreviewPath => _previewPath;` (the interface already exists in `QuiverMovePreviewPresenter.cs`; `_previewPath` is a `List<GridCell>`; `using System.Collections.Generic;` is already there for the field). No behavior change.
- Blocks: only the "+N arrows" label. Everything else works without it.

Also for the coordinator: whether the two `RoleZone` presenter edits count as touching a core system (the list names the handlers, not the presenters).

## Docs to update

- `tech/combat-architecture.md`: the readability layer (components above, where each lives, the `OnReturned` event).
- `status.md` / `build-log.md`: C4 built, not compiled; item 7 waits on the hook.
- `glossary.md` (narrative): the on-screen name is Encore.

## Risks and loose ends

- **Not compiled.** I read every API I call, but treat a first compile error as likely. Highest-risk spots: `QuiverAimPresenter` (definite assignment in the ability if/else chain), `QuiverMovePreviewPresenter` (pattern `is not` with a later use), `QuiverSprites`.
- **Layout guesses to tune in play:** pip size and gap under the unit, the "+N" cue position (right of her head, away from barks), the prompt line (beside her), the panel pips over the bottom of the portrait. All are constants at the top of each script.
- The prompt line uses `FactionRoleVisual.SetData`, which runs once per role prompt for any role; it only draws for Linda.
- **The tooltip "No arrows" shows whenever the quiver is empty and you hover the ability**, even if it is also on cooldown.
- Encore's hover lines only work while the unit panel shows Linda (the button must be on screen).
- The catch flash needs Mark's `ProjectileCatchAndReturn` in the scene; no Mark, no flash.
- An arrow that goes back at level end (field closed) gets no cue by design.
- Statics: none added. `PlayModeStaticReset` not touched.
- AI worker thread: nothing the AI reads changed (`HidesRoleZone` and the readability code are main thread only).
- `AIRegressionTest` untouched; no new `AbilityPreset`, so its message should be unchanged.

## Proposed commits

1. `fix(linda): an arrow with nowhere to land goes back to the quiver`: `Scripts/Quiver/QuiverArrow.cs` (the Apply branch only; the Mode getter and icon note in the same file can ride with it) (plain). Note: `QuiverArrow.cs` also carries the `Catch`/`Landed` tags that need `QuiverReturnKind` from unit 2, so commit 2 first, or accept one combined commit of 1 and 2 if you prefer; the file cannot be split cleanly without `git add -p`.
2. `feat(linda): quiver readability scripts and tests`: new `Scripts/Quiver/` files (rules, sprites, ability info, pips view, return cue, aim presenter, move preview presenter, prompt label, `Editor/QuiverReadabilityTests.cs`, all `.meta`), edits to `LindaQuiver.cs`, `GroundedArrowField*.cs` (plain).
3. `feat(ui): quiver pips, empty-quiver badge and arrow reasons on Linda's panel`: `UnitPanelUI.Quiver.cs`, `UnitPanelUI.cs`, `UnitPanelUI.RoleBadge.cs`, `RoleBadgeState.cs`, `AbilitiesBarHUDUI.cs`, `FactionRoleVisual.cs`, `RoleBadgeQuiverTests.cs` (+ `.meta`) (plain).
4. `feat(linda): hide Linda's role zone while her quiver is empty`: `RoleZonePresenter.cs`, `MovePreviewCoverPresenter.cs` (own commit: shared presenters).
5. `chore(linda): show Encore as the ability name`: `Linda_Ability_Recall.asset`, `QuiverWiringTests.cs` (plain).

Never stage the TMP fallback asset or the two ProjectSettings files. Order: 2, 1, 3, 4, 5 (1 after 2).

## Other branches

`thj/home-test` and `thj/onboarding` once this reaches `main`.

## How to see it

Run the EditMode suite first (only `AIRegressionTest.Baseline_MatchesCurrentAI` may fail). Then play a level with Linda (for example M4).

1. **Pips under Linda:** four amber arrow pips under her feet. Shoot: one goes dark. Pick one up: it lights again. She dies: they hide.
2. **Panel pips:** select Linda: pips and "Quiver 3/4" over the bottom of her portrait. Select John: gone.
3. **Badge:** spend all four arrows. The role badge by her role icon turns orange; hover it: "No arrows; walk over them or use Encore."
4. **Zone:** with 4 arrows select Linda: her Watch zone shows. At 0 it is not drawn (also not as the follow zone while previewing a move). Pick an arrow up: it returns.
5. **Watch prompt:** an enemy ends a move in her lane with 3 arrows: beside her "Arrows 3 > 2" while the prompt is up, gone when you answer.
6. **Reasons:** at 0 arrows hover the bow and Crescendo: "No arrows" under the description. Hover the Linda-Lucy and Linda-Toba Duo buttons: "Linda has no arrows". With nothing on the ground hover Encore: "No grounded arrows". With a full quiver and an arrow on the ground (cannot normally happen) "Quiver full".
7. **Landing marker:** select the bow, hover a cell along a row with an enemy: a cyan ring with an arrow on the last enemy in line; with no enemy, on the end of range; into a wall or hole, the last valid cell. Crescendo: on the hovered cell. Both arrow Duos: on the end of the line from Linda.
8. **Move preview (after the hook):** with arrows on the ground, hover a move that crosses them: "+1 arrow" at the destination, changing as you Tab between paths. "+1 arrow (1 left)" if the quiver cannot take all. Before the hook nothing shows.
9. **Encore lines:** with arrows on the ground, hover Encore on the bar: a golden line from each stack to Linda. Select it: the lines stay until you act.
10. **Return cue:** a green "+1" and a small arrow float up beside Linda on: walking John over an arrow (also the toss beat), Linda picking up her own, an arrow that lands under a Bergson, Encore (one "+N" for the whole recall), and Mark's catch (also a short warm glow on Mark). One cue per event.
11. **Locked look:** shoot an enemy so the arrow lies under it: bright orange arrow, red outline and a red count badge showing "1". A free arrow is white with a dark outline and a dark badge, also showing "1". Check on a busy enemy sprite.
12. **Safety:** hard to trigger by hand; kill the last enemy with an arrow still in flight: the quiver shows 4/4 and no arrow icon is left.
