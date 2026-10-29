# Report: Quiver polish 2 (arrow abilities, melee recovery, auto move-attack preview)

Plan: plans/2026-10-29-quiver-polish-2.md    Agent: miso-implementer    Branch: thj/linda-quiver (after `7c6f5e57c`)
Outcome: done. Nothing compiled or run here: the editor is open, so THJ compiles and runs the tests.

## What changed

Paths are under `miso/Assets/_Project/`. Q = `Features/Player/Linda/Scripts/Quiver/`.

**Point 1: every arrow ability gets the HUD feedback**
- `Q/QuiverHudFeedbackRules.cs`: new `IsArrowAbility(QuiverNeed)`, true for `Arrow` and `DuoArrow` and false for `Recall` and `None`. Comments now talk about arrow abilities instead of the primary.
- `Features/UI/Panels/Scripts/UnitPanelUI.Quiver.cs`: the panel no longer keeps one primary ability (`_quiverPrimary` and `PrimaryAbilityOf` are gone). Hover, press (button or number key) and selection each ask `QuiverAbilityInfo.NeedOf(ability)`, then `IsArrowAbility`, and also check that the quiver it finds is the one shown on the panel.
  - `NeedOf` is the existing helper. It finds the arrow from the ability's own effects (an `AEffectSpawner` whose projectile carries `QuiverArrow`, which is the component that spends) or from a Duo trigger whose Linda partner fires such a projectile. No hand-made list.
  - Selection: `NeedOf` runs only when the aimed ability changes (cached `_quiverAimedSeen`), not every frame.
  - Hover: moving from one arrow ability to another counts as a new reach (one punch each at 0 arrows). Moving onto a button that isn't an arrow ability drops the lift.
  - From Linda's prefab data this covers the bow, Explosive Crescendo (the Explosive Arrow ability), the Linda–Lucy Duo (fire arrow) and the Linda–Toba Duo (heal arrow). John–Linda and Mark–Linda count only if Linda's side of the Duo spawns a `QuiverArrow` projectile. Encore, Harmonic Slam, Walk and Cleanse don't count.

**Point 2: `xN` closer to its arrow**
- `Q/GroundedArrowField.cs`: `LabelOffset` goes from `(0.14, -0.12)` to `(-0.02, -0.12)` cells, which moves it left by 0.16 cells, my estimate of the drawn "x2" width (font size 1.4 × cell is about 0.14 cells per em, two Fairfax glyphs in bold). The vertical offset is unchanged, so it stays at the arrow's lower right, below its centre line, on the same sorting layer and under the HP bars.

**Point 3: melee kills hand the arrows back**
- `Q/LindaQuiver.KillHandBack.cs` (new partial): serialized `AbilityPreset[] handBackOnKillAbilities` (header "Kill hand-back") and `HandsBackOnKill(preset)`.
- `Q/KillHandBackRules.cs` (new, pure): `HandsBack(lethal, abilityListed, killerAlive, killerOnOwnersSide)` and `IsListed`, which compares by reference.
- `Q/GroundedArrowField.KillHandBack.cs` (new partial): `OnUnitDamageDone`. When the rule passes, it takes the stack on each footprint cell of the killed unit through the existing `ArrowPickupRules.Pickup`, with the same room cap and leftovers. It then plays the existing `PlayHandBack(cell, killer, linda)`, once per kill: the killer's bark, the toss to Linda, her reply. Arrows go in through `_quiver.Add(n, QuiverReturnKind.Pickup)`, so the "+N" cue (`QuiverReturnCue`), the HUD glow and pulse (`OnChanged`) and the log suffix (`QuiverLogListener` → `CombatLog.AnnotateAction`, `· +N arrows, quiver N/4`) all come from the existing paths with no new code.
- `Q/GroundedArrowField.Pickup.cs`: `HookPickup` and `UnhookPickup` also add and remove `onUnitDamageDone` (two lines).
- `Features/Player/Linda/Prefabs/Unit_Linda.prefab`: three YAML lines on the `LindaQuiver` block list `John_Ability_Attack_Sword` (`0db6e57b…`) and `Dom_Ability_Attack_Axe` (`0c8f3d40…`, Toba's primary on both `Unit_Toba` and `Unit_Toba_Ally`).
- **How it learns the killer's ability:** from the existing bus event `GlobalEventBus.onUnitDamageDone(RuntimeAbility ability, GUnit target, float damage, bool lethal)`, which `CombatLevelRunHandler.OnAbilityPerformedOn` raises (Linda's `UnitKillAbilityPointProvider` already uses it the same way). The killer is `ability.Owner` and the listed check is `ability.Preset`. The killed unit keeps `CurrentCell` after `Die` (only its slot is cleared), which gives the tile. No core code.
- Any other kill (her arrows, Lucy, hazards, Mark, unlisted abilities) goes through none of this. The stack unlocks through the existing `Update` poll and stays on the tile.

**Point 4: auto move-attack previews the landing**
- `Q/QuiverPreviewRules.cs`: in `LandingMarkerRules`, the pure `LastEnemyOnLine(origin, end, enemyAt)` and `MarkerCellAfterMove(...)`. The second is `EndOfFlight` from the shot cell, then the last enemy on the flight line (bow only), then `MarkerCell`.
- `Q/QuiverAimPresenter.cs`: when the hovered enemy is out of range, `ShotCellAfterMove` returns the cell she will shoot from, and the ghost is measured from there. It applies only when the aimed ability is the shooter's own basic attack with auto move allowed; Duos never walk. Out of range with no approach, the ghost stays hidden as before.
  - The shot cell is cached per (ability, hovered cell, standing cell) and recomputed only after a board change (`MarkDirty` sets both caches dirty), because it runs a path search.
- **How it gets the shot cell:** `PlayerController.TryFindApproachCell(attack, enemy, out approach)`. It is public, read-only and marked for previews in `core-systems.md`, and it is the same call `TryQueueApproachAttack` uses to queue the real walk, so the cell is the true shot cell. I read it without changing core.
  - I did not use `IMovePreviewPathSource.PreviewPath`. `ClearPathHighlight` doesn't null `_previewPath`; only `RebuildAltPaths` and the take-action state do. So after hovering one approachable enemy and then one with no approach, `PreviewPath` still holds the old enemy's walk, and a ghost built on it would be wrong.
- After a move, the projectile's physics hit preview (`Projectile.CollectPreviewPathHits`, core) always starts at the shooter's current cell, and it has no origin parameter. So after a move the enemies on the line come from the grid along the same Bresenham line the arrow's landing uses. The in-range path is unchanged and still uses the physics preview.

**Point 5: outline on the HUD quiver**
- `Features/UI/Panels/Scripts/QuiverUI.cs`: at `Capture()` (Awake), a uGUI `Outline` goes on the body, the rim and each arrow image.
  - New serialized fields under "Outline": `outline` (on), `outlineColor` (black, alpha 0.9), `outlineWidth` (1.25 canvas px, range 0.5 to 3).
  - `useGraphicAlpha` is on, so a returning arrow's outline fades in with it. The outline ignores the empty tint and scales with the lift and punch, because it lives on the same transforms.
  - An image that already has an `Outline` or `Shadow` keeps its own and gets none added.
  - Tooltip and comment wording changed from "her primary ability" to "her arrow abilities".
  - No prefab edit, nothing moved.

**Tests (new or extended; THJ runs them)**
- `Q/Editor/QuiverHudFeedbackTests.cs`: `ArrowAbilities_AreTheOnesThatSpendAnArrow`.
- `Q/Editor/KillHandBackTests.cs` (new):
  - `ListedLethalHitByALivingAlly_HandsBack`
  - `AHitThatDoesNotKill_LeavesThem`
  - `AKillByAnUnlistedAbility_LeavesThem`
  - `AKillerThatDied_LeavesThem`
  - `AKillerOfTheOtherSide_LeavesThem`
  - `IsListed_MatchesTheSameObjectOnly`
  - `AHandBackKill_TakesTheFreedStackUpToTheRoom`
  - `Linda_ListsJohnsAndTobasPrimaryAttacks`: checks the prefab data, and that Mark's primary and Linda's bow are not listed.
- `Q/Editor/ArrowLandingAfterMoveTests.cs` (new):
  - `LastEnemyOnLine_IsTheFarthestEnemyOnTheFlight`
  - `LastEnemyOnLine_IgnoresTheShootersOwnCellAndOffLineEnemies`
  - `BowAfterMove_LandsOnTheLastEnemyHitFromTheShotCell`
  - `BowAfterMove_RangeCountsFromTheShotCell`
  - `EndOfFlightShotAfterMove_IgnoresEnemiesOnTheLine`
  - `AfterMove_FallsBackAlongThePathWhenTheCellCannotHoldAnArrow`

## Acceptance criteria

- [ ] Any arrow-spending ability lifts the quiver, punches it at 0, and Encore and the others don't: built. The rule is tested (`ArrowAbilities_AreTheOnesThatSpendAnArrow`); the hover, press and select paths need the play check.
- [ ] `xN` about one label width closer: built (constant). Needs the play check; the width is an estimate.
- [ ] A melee kill returns the arrows with the toss, "+N" and the HUD gain, and any other kill leaves them unlocked: built. The rule, the take and the prefab list are tested; the in-game event needs the play check.
- [ ] Auto move-then-shoot shows the ghost on the true landing tile: built. The pure landing-from-shot-cell rule is tested; the wiring needs the play check.
- [ ] Thin black HUD outline, with tint, lift and glow still right: built. Play check only.
- [ ] EditMode passes with only the known red: not run (the editor is open). THJ runs it.

## Save reset

No.

## Decisions I made

- Point 4: I took the shot cell from `PlayerController.TryFindApproachCell` (public, read-only, the real walk's source) instead of `IMovePreviewPathSource.PreviewPath`, because `PreviewPath` can be stale (see above). Both are read-only core reads with no core change. The behaviour matches what the plan asked for. Tier 2, flagged.
- Point 4: after a move, the last enemy on the flight comes from the grid line instead of the projectile's physics preview, because the physics preview can't start from another cell without a core change. Within range nothing changed.
- Point 5: the `Outline` components are added at runtime from `QuiverUI` fields, not baked into `LindaQuiver.prefab`. Same look, no prefab or GUID edits, and one checkbox turns it off. The catch is that it only shows in Play mode, not in the prefab view.
- Point 3: the killed enemy itself never counts as locking its stack, even if its death is still being processed when the damage event fires. A different living enemy on the same footprint would still lock it.
- Point 3: one hand-back beat per kill even when a big unit stood on several stacks. Each stack's `Add` still raises its own "+N".
- Point 2: a fixed offset, not measured from the font at runtime. THJ can tune the one constant.

## Needs THJ

None.

## Docs to update

- `tech/core-systems.md`, "Move preview path" row: `IMovePreviewPathSource` is still unused (the quiver now reads `TryFindApproachCell`), so it is still a candidate to revert. Its "Read by the quiver's '+N arrows' presenter" note is out of date.
- `design/gdd/characters/linda.md` (or wherever the quiver rules live): John's and Toba's primary kills on an arrow tile hand the arrows back at once. The list is data on Linda's quiver.
- `status.md`: quiver polish 2 built, waiting on THJ's play check.

## Risks and loose ends

- **Not compiled here.** Please recompile (Ctrl+R) before running the suite. Unity creates the `.meta` files for the five new `.cs` files on refresh; they go with their files in the commits below.
- **`Unit_Linda.prefab` was edited on disk while the editor is open.** If the prefab has unsaved changes in the editor, saving it there would overwrite the new list. Check that the LindaQuiver Inspector shows two entries under "Kill hand-back".
- **Outline overlap:** a uGUI `Outline` draws four offset copies behind each image, so where an arrow or the rim overlaps the body, the later image's dark contour draws over the body. If that looks doubled, the plan's fallback is one silhouette copy behind the group (not built).
- **Kill event timing:** `onUnitDamageDone` comes from `CombatLevelRunHandler`'s HP snapshot compare after the ability performs on the target. If a melee kill ever reaches `Die` without that event (a kill by a status tick, for example), it isn't a listed attack anyway.
- **Approach rule:** the ghost only shows for an out-of-range enemy when `TryFindApproachCell` finds a cell, matching when the controller offers the walk. It is cached per aim and recomputed on unit move or death, ability perform and bar hover. A change in AP from elsewhere without one of those events could leave it stale until the next hover.
- **Enemy-on-line after a move** uses grid cells, not colliders. A big enemy whose collider the flight would clip without its anchor cell being on the line is missed. The bow lands on the target cell in practice.
- `QuiverAbilityInfo.NeedOf` for a Duo needs the Linda partner to be valid at that moment (alive and on the field). If she isn't, the Duo doesn't lift her quiver; this matches the grey-reason logic.

## Proposed commits

Shared repo, in this order. Each one stands alone; the `.meta` files are the ones Unity generates on refresh.

1. `feat(linda): every arrow ability lifts or punches the HUD quiver`: plain
   - `Features/Player/Linda/Scripts/Quiver/QuiverHudFeedbackRules.cs`
   - `Features/UI/Panels/Scripts/UnitPanelUI.Quiver.cs`
   - `Features/Player/Linda/Scripts/Quiver/Editor/QuiverHudFeedbackTests.cs`
2. `feat(linda): grounded stack count sits closer to its arrow`: plain (could fold into 1)
   - `Features/Player/Linda/Scripts/Quiver/GroundedArrowField.cs`
3. `feat(linda): John's and Toba's primary kills hand the arrows under the enemy back`: plain (gameplay rule plus prefab data)
   - `Features/Player/Linda/Scripts/Quiver/KillHandBackRules.cs` + `.meta`
   - `Features/Player/Linda/Scripts/Quiver/LindaQuiver.KillHandBack.cs` + `.meta`
   - `Features/Player/Linda/Scripts/Quiver/GroundedArrowField.KillHandBack.cs` + `.meta`
   - `Features/Player/Linda/Scripts/Quiver/GroundedArrowField.Pickup.cs`
   - `Features/Player/Linda/Prefabs/Unit_Linda.prefab`
   - `Features/Player/Linda/Scripts/Quiver/Editor/KillHandBackTests.cs` + `.meta`
4. `feat(linda): landing ghost measures from the cell an auto move-then-shoot fires from`: plain
   - `Features/Player/Linda/Scripts/Quiver/QuiverPreviewRules.cs`
   - `Features/Player/Linda/Scripts/Quiver/QuiverAimPresenter.cs`
   - `Features/Player/Linda/Scripts/Quiver/Editor/ArrowLandingAfterMoveTests.cs` + `.meta`
5. `feat(linda): thin dark outline on the HUD quiver`: plain
   - `Features/UI/Panels/Scripts/QuiverUI.cs`

Not touched: `Resources/GlobalSettings.asset`, the TMP fallback, `ProjectSettings` (THJ's local edits), `AIRegressionTest`, any core file.

## Other branches

None.

## How to see it

1. Recompile (Ctrl+R). Run EditMode tests; only `AIRegressionTest.Baseline_MatchesCurrentAI` should be red. The new classes are `KillHandBackTests` and `ArrowLandingAfterMoveTests`, plus one new case in `QuiverHudFeedbackTests`.
2. Open `Unit_Linda.prefab`. LindaQuiver › "Kill hand-back" lists John's sword and Toba's axe.
3. Start a level with Linda, John and Toba. Select Linda. Hover the bow, Explosive Crescendo, and the Lucy and Toba Duo buttons one after another: the HUD quiver lifts for each. Hover Encore, Harmonic Slam or Walk: no lift. Press number keys for those slots: same.
4. Fire until the quiver is empty. Hover or press each arrow ability: one punch each. Encore doesn't punch.
5. Land two arrows on one tile: the `x2` sits about one label width further left than before, still at the arrow's lower right and under HP bars.
6. Land an arrow under an enemy (the stack goes dark). Kill that enemy with John's primary: the arrows fly back to Linda right away (John's bark, the toss, Linda's reply). The "+N" appears on her, the HUD arrows glow, and the combat log line for John's attack ends with `· +N arrows, quiver N/4`. Repeat with Toba's primary.
7. Land arrows under an enemy and kill it with Linda's bow, Lucy or a hazard: the stack turns bright (unlocked) and stays on the tile until someone steps on it.
8. With the bow selected, hover an enemy outside her range that she can reach by walking. The walk path shows, and the ghost arrow sits on the tile where the arrow will land as fired from the end of the walk. Click and check that the arrow lands on that tile.
9. Look at the HUD quiver on her portrait: a thin dark contour around body, rim and arrows. Check it during the lift, the punch, the empty tint and an arrow returning. To compare, untick `QuiverUI › Outline` on the `LindaQuiver` HUD prefab, or set the width in the same section.
