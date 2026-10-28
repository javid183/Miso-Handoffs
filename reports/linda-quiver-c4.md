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

## Review fixes

Still not compiled or run (the editor is open). All fixes below are in the files named; LF kept, no BOM, a `.meta` for each new file.

**Must fix 1 (commit units):** the arrow-landing fix and the scripts are one unit now (see the updated units below).

**Should fix**
1. `QuiverReturnCue`: cues and flashes are destroyed in `OnDisable` (a shared `ClearViews`), so nothing freezes when Linda is deactivated at death.
2. Catch flash: it now looks through all `ProjectileCatchAndReturn` components and takes one whose unit is alive and in Linda's faction.
3. Role badge tooltip: the "Same tiles as the basic attack; Shift shows them." line is skipped for the empty-quiver state.
4. Dead code removed: `ArrowIcon`, `NoteArrowIcon` (and its call in `QuiverArrow`), `QuiverPipRules.ZoneShown` and its test. The zone check is now the `IRoleZoneVisibility` property (below); `LindaQuiver.IsEmptyFor(unit)` replaces the old static (the badge uses it).
5. The closed-field test now passes a real `GridCell` (added to a test object), so it checks the refusal for the reason it claims. Renamed `ClosedField_RefusesALandingOnARealCell_...`. If `AddComponent<GridCell>()` misbehaves in edit mode, that is the test to look at first.
6. Placeholder text: every string I wrote that carries words is tagged `[PLACEHOLDER] ` (the grey reasons, badge line, "Quiver full", the Watch prompt, the panel label, the "+N arrow(s) (N left)" label), and stripped where shown with `QuiverTextRules.Show`, which uses the existing `HandBackLines.Strip`. `QuiverTextRules.WithReason` strips both the description and the reason, so the Encore tooltip no longer shows the tag (`AbilitiesBarHUDUI` needed no further change). The "+N" return cue is a symbol, not words, so it is untagged. Tests compare the stripped text.
7. Sorting on the board: outline 49, icon 50, badge 51, count 52, toss 53.
8. `QuiverAimPresenter`: the stack list for Encore's lines is a reused buffer, and the landing marker no longer recomputes (or re-runs `CollectPreviewPathHits`) every frame when there was no landing cell to show.

**Core hook (approved), item 7**
- `Core/Interactions/Runtime/IMovePreviewPathSource.cs` (+ `.meta`): the interface now lives in `MISO.Core.Interactions`; the copy in the quiver folder is gone.
- `PlayerController.cs`: exactly two additive lines: `, IMovePreviewPathSource` on the class and `public IReadOnlyList<GridCell> PreviewPath => _previewPath;`. Nothing else changed.
- `_previewPath[0]` is the mover's cell: `CommitPreviewedMovePath` itself refuses a path whose first cell is not the unit's cell. The presenter still checks first cell = mover, last cell = hovered cell, and that the active ability is a move. One edge: `_previewPath` is not cleared when the path highlight is cleared by moving the pointer off the range, so the guard on the hovered cell is what keeps a stale path from showing.

**Core no longer imports Linda's folder**
- `Core/Systems/RoleZoneSystem/Runtime/IRoleZoneVisibility.cs` (+ `.meta`): `IRoleZoneVisibility { bool HidesRoleZone }` and a small `RoleZoneVisibility.Hidden(unit)` helper. `LindaQuiver` implements it (true while empty). `RoleZonePresenter` and `MovePreviewCoverPresenter` query it; `RoleZonePresenter` redraws when any such component's value changes. It has no `using` of the Bergsons namespace now.
- Follow zone: it still hides at 0 arrows, even on a path that would pick arrows up. Left as it was (it would need the path in the zone presenters).

### Updated commit units (each builds on the ones before it)

1. `feat(player): expose the previewed move path to the preview layer`: `Core/Interactions/Runtime/IMovePreviewPathSource.cs` + `.meta`, `PlayerController.cs`. **Core hook, own commit.**
2. `feat(roles): let a unit hide its own role zone`: `Core/Systems/RoleZoneSystem/Runtime/IRoleZoneVisibility.cs` + `.meta`, `RoleZonePresenter.cs`, `MovePreviewCoverPresenter.cs`. Shared presenters, own commit.
3. `feat(linda): quiver readability and arrows that always find their way back`: everything under `Scripts/Quiver/` (new scripts, edits to `LindaQuiver.cs`, `QuiverArrow.cs`, `GroundedArrowField*.cs`, all `.meta`, `Editor/QuiverReadabilityTests.cs`). This includes the landing fix (merged, per the review). Needs 1 and 2.
4. `feat(ui): quiver pips, empty-quiver badge and arrow reasons on Linda's panel`: `UnitPanelUI.Quiver.cs`, `UnitPanelUI.cs`, `UnitPanelUI.RoleBadge.cs`, `RoleBadgeState.cs`, `AbilitiesBarHUDUI.cs`, `FactionRoleVisual.cs`, `Editor/RoleBadgeQuiverTests.cs` (+ `.meta`). Needs 3.
5. `chore(linda): show Encore as the ability name`: `Linda_Ability_Recall.asset`, `Scripts/Quiver/Editor/QuiverWiringTests.cs`. Needs 3.

Never stage the TMP fallback asset or the two ProjectSettings files.

### Tests for THJ to look at (EditMode, Run All; only `AIRegressionTest.Baseline_MatchesCurrentAI` may fail)

- Compile first. New or changed test classes: `QuiverReadabilityTests` (all), `RoleBadgeQuiverTests` (all), and in `QuiverWiringTests`: `ReadabilityLayer_FindsEncoreAndTheBowFromTheirData`, `Recall_...` title check (now "Encore").
- Watch these by name if anything is red:
  - `ClosedField_RefusesALandingOnARealCell_SoTheArrowGoesBackToTheQuiver` (builds a `GridCell` in edit mode).
  - `Quiver_ReportsEmptyOnlyAtZero`, `Quiver_RaisesOneReturnEventPerAddWithTheCountThatWentIn`, `Quiver_ACatchAndARecallAreOneEventEach`, `Quiver_NothingWentInMeansNoEvent`, `Quiver_PlainAddIsAReturnOfKindOther` (build a `LindaQuiver` on a bare object).
  - `ReadabilityLayer_FindsEncoreAndTheBowFromTheirData` (loads the real Encore and bow assets by path).
  - `WithReason_PutsTheReasonOnItsOwnLine` (checks the tag is stripped).
- Existing suites untouched: `RoleBadgeRulesTests`, the C1 to C3 quiver tests, `AIRegressionTest` (no new preset).
- Play: after the hook, hover a move across arrows to see "+N arrow(s)" (How to see it, step 8); the other steps are unchanged except that all on-screen texts show without `[PLACEHOLDER]`.

## Pips draw order

- `QuiverPipsView.cs`: pips moved from "WorldUI" order 49 to "DynamicTop" order -1 (D-280). Linda's body is on Default and the UnitBase HP bar parts are DynamicTop at 0 to 2, so -1 sits above bodies and below every bar. John (99) and the Deev (-9) bodies on DynamicTop do not matter for Linda's pips. No test asserted the old values; not compiled or run (editor open).
- Play: put an enemy one tile below Linda with arrows in the quiver; the pips draw under that enemy's HP bar, and still over Linda's own sprite.

## PlayerFaction null fix

- New `Quiver/QuiverLevelAccess.cs` (`PlayerControllerOrNull`, `RelationsReady`); used in `QuiverAimPresenter.cs` (2 sites), `QuiverMovePreviewPresenter.cs`, and in the enemy checks of `GroundedArrowField.cs` and `QuiverArrow.cs` (`GetFactionsRelation` hits the same null field). The `.meta` is created when Unity refocuses.
- CombatLevel has no public ready check, so the helper returns null unless `CombatLevel.Instance`, `GameHandler`, its `GameData` and the player faction's controller all exist; it reads the player faction from `GameData`, not the level. Not compiled or run (editor open).
- THJ most likely hit it on level load (CombatLevel exists, `Initialize` not yet run) or unload; both leave `_factionRelations` null while Update runs.
