# Report: Enemy alert state, C4 (ranges as attributes, Unaware range preview, marker size)

Plan: plans/2026-10-23-enemy-alert-state-tech.md (C4; D-164, D-165)    Agent: miso-implementer    Branch: main (not switched)
Outcome: done. It compiles and EditMode passes 736/737; the one failure is the known red. The look and feel still need THJ's play check.

## What changed

All paths are under `miso/Assets/_Project/`. The EnemyAlertSystem files are still LF with no BOM. `ShowStatsHoverPreview.cs` was LF with no BOM and still is.

Code:
- `Core/Systems/EnemyAlertSystem/Runtime/EnemyAlertRules.cs` (committed in `3378acaca`, changed here):
  - Removed `SightFloor`, `MinAlertRange`, `Sight(...)` and `AlertRange(...)`. This also drops THJ's local edit to 1.
  - Added `RangeWithBonus(float attributeValue, int levelBonus)`: rounds to whole steps (halves away from zero), adds the bonus, clamps at 0.
  - Added `TilesWithinRange(footprint, range)`: every tile within Manhattan range of a footprint, without the footprint's own tiles, each tile once.
  - Updated the header comment.
- `Runtime/EnemyAlertSettings.cs`: removed `sightOverride` and `SightOverride`.
- `Runtime/LevelAlertSettings.cs`: added `sightBonus` and `alertRangeBonus` (int, may be negative) with getters.
- `Runtime/EnemyAlertTracker.cs`:
  - `Watch` no longer stores the ranges, and `WalkReach`, `LongestAttackReach` and `LongestRadius` are gone.
  - New constants `SightAttributeId = "Specs_Sight"` and `AlertRangeAttributeId = "Specs_AlertRange"`.
  - `SightOf` and `AlertRangeOf` read the attribute's `Value` at every check, plus the level bonus, through `RangeWithBonus`.
  - A unit whose attribute set lacks the entry uses the definition's default (cached per id on the instance, not static).
  - Level bonuses are read in `BeginLevel`.
  - New public `TryGetUnawareRanges` and `TryGetUnawareRangeTiles`. Both return false unless the unit is Unaware.
- `Runtime/EnemyAlertTracker.Events.cs`: one line. The noise candidate's alert range now comes from `AlertRangeOf`.
- `Runtime/EnemyAlertVisualRules.cs`: added `MarkerScale`, `MarkerWorldSize` and `MarkerCenterHeight`.
- `Runtime/EnemyAlertTracker.Visuals.cs`:
  - `markerOffset` and `markerScale` are replaced by `markerTileFraction` (0.35), `markerGap` (0.05 world units) and `fallbackTileWorldSize` (0.5). The old fields were never serialized in any prefab, so nothing is lost.
  - Size: the marker's longer side is 0.35 of a tile, measured from the unit's cell to an adjacent cell. The scale is divided by the sprite's own world size, so the icon's resolution doesn't matter.
  - Position: centred on the mini bar. Its bottom edge sits `markerGap` above whichever is higher: the top of the `Body` sprite or the top of the bar's drawn graphics.
- `Core/Interactions/Runtime/ShowStatsHoverPreview.cs`: a new branch `ShowUnawareRanges` (about 30 lines); see "How the preview works". This file is not on the core-systems list.

Tests:
- `Editor/EnemyAlertRulesTests.cs`:
  - Removed the 6 formula tests (the sight and alert range sections).
  - Added `RangeWithBonus` tests: the bonus adds or takes away, the result is never below 0, fractional values round.
  - Added 4 `TilesWithinRange` tests: the diamond shape, a multi-tile footprint, a match against `WithinRange` over a grid, and empty input.
- `Editor/EnemyAlertDataTests.cs`:
  - Both attribute definitions exist, are hidden from the unit panel, have defaults 3 and 2 and are bounded at 0.
  - Start values: UnitBase sight 3 and alert 2, Masher sight 2 and alert 2, Archer sight 3 (inherited).
- `Editor/EnemyAlertVisualTests.cs`: marker scale is the same at any resolution, an empty sprite gives 1, the size is a fraction of a tile, and the marker sits above both the head and the bar.

Data:
- `Resources/Attributes/AAttributes.asset` (the "Specs" attribute set): two new definitions.
  - `Sight`: id `Specs_Sight`, default 3.
  - `AlertRange`: id `Specs_AlertRange`, title "Alert Range", default 2.
  - Both: constant bounds 0 to 99, not indicated, not shown on hover, white, no icon, with a `[PLACEHOLDER]` description.
- `Features/_Common/Prefabs/UnitBase.prefab`: two entries appended to the GUnit `attributeSet` (index 4 Sight, index 5 AlertRange).
  - Each has `overrideDefaultValue` with constants 3 and 2, `changeInInteger` on, no events and no extra mods.
  - Re-serialization noise from the save: default-valued fields that existed in code but had never been saved (the mini bar's 4 low-health fields, and `requireTargetTag` / `targetTagQuery` on two extra mods). These are the same values as the code defaults, so behaviour doesn't change.
  - Each new entry's `sBBounds` block was copied from the FP entry. It is unused (`overrideBounds: 0`, so the definition's 0 to 99 applies).
- `Features/Enemy/Masher Goblin/Prefabs/Unit_MasherGoblin.prefab`: one override, `attributeSet.attributeEntries.Array.data[4].defaultSbValue.constantValue = 2`.
  - Save noise: two existing modifications reordered, and `counterCanProvokeFamilyRoles: 1` written out at its code default.
- `Unit_GoblinQueen.prefab`, `Unit_Deev.prefab`, `Unit_TobaEnemy.prefab`: removed the single `sightOverride: 0` line from each `EnemyAlertSettings` block.

Method: a temporary editor script under `Assets/_TempEnemyAlertData/Editor/`, run once in batchmode with `-executeMethod` (`SerializedObject` plus `PrefabUtility.LoadPrefabContents` / `SaveAsPrefabAsset`). The folder and its `.meta` are deleted. The boss-line removals were done by hand (one line each).

## Attribute choice

I used plain attributes in the GUnit `attributeSet` (the "Specs" group: Health, Stamina, AP, FP), not stats (`Stat_*` in `statAttributes`). Why:
- **Modifiers apply:** `AEffectAttributeModifier` (instant and duration) writes to `attributeSet`, and the tracker reads `RuntimeAAttributeBase.Value`, which includes duration modifiers. Instant changes clamp at the definition's bound of 0, and the rule clamps again after the level bonus.
- **No UI:** the unit panel only lists `Indicated` attributes, and both are off.
- **Per prefab:** a variant overrides one value (the Masher's one line).
- **No save change:** `attributeSet` isn't saved.
- **The stat path is worse here:** stats are factors for stat evaluation (Ability, Unit, Equipment, Faction sources, with policies), saved per unit as upgrade levels, and combined with faction and equipment sets. That is more machinery and more ways for a value to surprise.
- **AI:** the AI only looks attributes up by id (`UtilityScoreEvaluator`), so new entries change nothing there. The regression test builds units with an empty `AAttributeSet`, and its result is unchanged (38/709).

Units without the entries use the definition's default (3 and 2). Two variants override the base array size to 4, so they don't get the entries: `Features/Enemy/Deevoted/Prefabs/Deevoted.prefab` and the Lucy decoy variant. Deevoted therefore uses 3 and 2. To tune it, remove its size override in the Inspector (Revert on the Attribute Set size) and then set its values.

This adds data only. No attribute or stat system code changed.

## How the preview works

- Trigger: hold Shift and hover an enemy, as with the existing Shift hover preview (`ShowStatsHoverPreview`).
- `ShowPreview` first calls `ShowUnawareRanges`. If the unit is hostile to the player and the level's tracker says it is Unaware, it draws the ranges **instead of** the move layer and danger zone. The danger zone would sit on the same two layers (they are bit flags, not counted), and an Unaware enemy doesn't act anyway.
- The tracker is found on the bus's GameObject (`_bus.GetComponent<EnemyAlertTracker>()`), where it lives on LevelBase.
- **Sight tiles** go on `ShiftPreviewLayer.EnemyMove`: the dull red-brown frame.
- **Alert-range tiles** go on `ShiftPreviewLayer.EnemyAttack`: the strong red icon. A tile in both ranges shows the frame and the icon, so the two read apart.
- Tiles are measured Manhattan from the footprint, through walls, without the unit's own tiles.
- Off-board coordinates are dropped by `GridManager.GetCell`. As with every move layer, an inactive cell shows no frame.
- It is cleared exactly like the existing preview.
- This uses only the current `SetShiftPreview` API. No `GridCell` or other core change.
- An Alerted enemy gets false from `TryGetUnawareRangeTiles`, so it shows its usual move layer and danger zone.

Limit: the preview is drawn when Shift is pressed or the hover changes. If the enemy wakes while Shift is held, the old tiles stay until the next press or hover.

## Acceptance criteria (C4)

- [x] `Sight` and `AlertRange` are unit attributes with defaults 3 and 2 on UnitBase and Masher sight 2. Read through `Value` at check time, so modifiers apply. Covered by data tests. Modifiers in play are untested (no effect in the game targets them yet).
- [x] Formula, floors, `sightOverride` and the reach helpers are removed, and the three prefab lines are cleaned. The code has no references left.
- [x] `sightBonus` and `alertRangeBonus` on `LevelAlertSettings`, clamped at 0: rule tests. The hookup needs play.
- [x] Range preview only while Unaware, in two tints, through the current layer API: built, with the tile rule tested. **Needs play.**
- [x] Marker at a fixed world size, above the head and the mini bar: built, with the rules tested. **Needs play** for the look.
- [x] Tests updated; the EnemyAlert suites pass 83/83.
- [x] No core-system code change. No AI graph, variable or ability edit. `AIRegressionTest` untouched. No statics.
- [ ] "Changing `Sight` on a prefab or the level's `sightBonus` visibly changes when that enemy wakes and the drawn tiles": **play check**.

## Test results

- The editor was closed (no `miso/Temp`, no Unity editor process). Batchmode, Unity 6000.3.4f1.
- 737 tests: 736 passed, 1 failed. The failure is `AIRegressionTest.Baseline_MatchesCurrentAI` (the known red, still 38 failures out of 709 checks, unchanged).
- No compile errors. The data-run log and the test log have no missing-script or import errors.
- The test run changed no further asset.
- Logs are in the scratchpad: `c4data.log`, `c4test.log`, `c4results.xml` (`C:\Users\javid\AppData\Local\Temp\claude\E--Work-Projects-miso\4a7b2e15-2aac-45e7-9e97-b6e33d04e813\scratchpad`).

## Save reset

No.

## Decisions I made

- Plain attributes, not stats (above).
- The definitions carry the same defaults as UnitBase (3 and 2). Units outside the UnitBase array (Deevoted) then behave the same. **To tune the global default, change UnitBase**, which is the value every UnitBase variant reads.
- Fractional attribute values round to whole steps, halves away from zero.
- For an Unaware enemy, the preview **replaces** its move layer and danger zone (the layers can't be shared).
- The preview is shown with Shift plus hover. I read "hovering it, and Shift" as the Shift hover preview. Showing it on a plain hover (no Shift) would be a small change in `ShowStatsHoverPreview.OnEntityHovered`. **Coordinator: confirm which one THJ meant.**
- The marker is measured once, when it is created, from the idle `Body` sprite and the bar. It is parented to the unit, so it follows moves.

## Needs THJ

None blocking. One reading to confirm: Shift plus hover versus plain hover (above).

## Docs to update

- `tech/combat-architecture.md` (coordinator):
  - The ranges are `Specs_Sight` and `Specs_AlertRange` attributes plus the level bonuses.
  - The Shift preview for Unaware enemies.
  - The marker's size rule.
- `design/gdd/enemies.md` EN-13 (designer): sight is now an attribute (default 3, Masher 2), and the alert range is an attribute (default 2), not half the sight. Plus the level bonuses.
- `tech/core-systems.md`: nothing (no core change).

## Risks and loose ends

- **Deevoted and the Lucy decoy variant** override the attribute array size to 4, so they miss the new entries and use the definition defaults. That is fine for now; it is listed so nobody is surprised when tuning Deevoted.
- **Re-serialization noise** in `UnitBase.prefab` and `Unit_MasherGoblin.prefab` (listed above): code-default fields written out for the first time. Harmless, but it shows in the diff.
- The marker's height uses the idle sprite at creation. A unit whose animation grows much taller could poke into it.
- The preview doesn't refresh if the enemy wakes while Shift is held.
- No effect in the game modifies Sight or AlertRange yet, so "modifiers apply" is by construction, not tested in play.
- `AIRegressionTest` is unchanged at 38/709.

## Proposed commits (all held work: C1 commit 2, C2, C3, C4)

C4 changes the same files as C1 commit 2 and C2 (the tracker partials, settings and tests), so they can't be split by chunk without partial staging. Each commit below compiles on its own, in this order:

1. `feat(enemies): sight and alert range unit attributes` (data only, plain):
   - `Resources/Attributes/AAttributes.asset`
   - `Features/_Common/Prefabs/UnitBase.prefab`
   - `Features/Enemy/Masher Goblin/Prefabs/Unit_MasherGoblin.prefab`

   Nothing reads them yet, so there is no behaviour change.
2. `feat(enemies): an Unaware status tag in the AI skip-turn query` (data, risky: the AI skip query policy goes from All to Any):
   - `Resources/Tags/GTagSet.asset`
   - `Resources/Tags/GTagRegistry.asset`
   - `Content/Controllers/AIController.prefab`

   No unit carries the tag yet.
3. `feat(enemies): enemies start unaware and skip their turns until they see or hear the family` (risky: every level's pace). Depends on 1 (the data tests read the attributes) and 2:
   - `Core/Systems/EnemyAlertSystem/Runtime/EnemyAlertRules.cs`
   - `Runtime/EnemyAlertTracker.cs` + `.meta`
   - `Runtime/EnemyAlertTracker.Events.cs` + `.meta`
   - `Runtime/EnemyAlertTracker.Visuals.cs` + `.meta`
   - `Runtime/EnemyAlertVisualRules.cs` + `.meta`
   - `Runtime/EnemyAlertSettings.cs` + `.meta`
   - `Runtime/LevelAlertSettings.cs` + `.meta`
   - `Editor/EnemyAlertRulesTests.cs`
   - `Editor/EnemyAlertDataTests.cs` + `.meta`
   - `Editor/EnemyAlertVisualTests.cs` + `.meta`
   - `Content/Levels/LevelBase.prefab`

   This holds C1 commit 2, C2's marker and pop, and C4's attribute read, bonus and marker size.
4. `feat(preview): Shift on an Unaware enemy shows its sight and alert range` (plain): `Core/Interactions/Runtime/ShowStatsHoverPreview.cs`. Depends on 3.
5. `feat(levels): boss units and objective levels start enemies alert` (data, plain). Depends on 3:
   - The 3 boss prefabs (`Unit_GoblinQueen`, `Unit_Deev`, `Unit_TobaEnemy`, now without `sightOverride`).
   - The 11 level prefabs from C3: `Level3-C1`, `LevelM2-C1`, `LevelMountainDeev`, `Level2-C2`, `Level2-C3-1`, `Level2-C3-2`, `LevelMarkIntro-C1`, `LevelMarkIntro-C2`, `LevelMarkIntro-C3`, `LevelDomFight`, `LevelHomeDefence`.

Not ours, leave unstaged: the TextMesh Pro fallback asset, `Packages/*`, `ProjectSettings/*`, and any other level prefab.

Per the play-test-before-commit rule, all five wait for THJ's play check.

## Other branches

`thj/home-test` needs this when it takes `main`.

## How to see it

The tests already ran in batchmode (above). In the editor: open Unity, let it recompile, and optionally re-run the Test Runner's EditMode suite. No Inspector step is required.

1. **Masher (`LevelE3-C1`, `Content/Levels/Generic Levels/Easy/E3/`):**
   - The Unaware marker is small (about a third of a tile) and sits above the head and the mini bar.
   - Hold Shift and hover the Masher: red-brown frames on tiles within 2 steps (its sight), and red icons on tiles within 2 (its alert range), so they overlap.
   - Stop a Bergson 3 steps away: it stays Unaware. Stop at 2: it wakes with a "!". Shift on it now shows its normal move layer and danger zone.
2. **Archer (`LevelE1-C1`, `Generic Levels/Easy/E1/`):**
   - Shift and hover: frames out to 3 steps, icons out to 2.
   - It wakes when a Bergson stops within 3 steps.
   - A Linda arrow on a tile within 2 of it, without hitting it, also wakes it.
3. **Shaman (`LevelM1-C1`, `Generic Levels/Medium/M1/`):** a Shaman and its pack sleep until the family is within 3. When one wakes, Unaware allies within 2 of it wake one after another.
4. **Start-alert level (`Level2-C2`):** no markers, and Shift shows the normal danger zones (nobody is Unaware).
5. **Tuning check:**
   - In a test level, add `LevelAlertSettings` to the level root with Sight Bonus 2: sight frames grow to 5 (the Masher's to 4) and enemies wake from farther away.
   - Set Sight Bonus to -5: frames vanish and enemies only wake from noise.
   - On `UnitBase` (GUnit > Attribute Set > Specs_Sight > Default Sb Value > Constant Value), change 3 to 4: every non-Masher enemy's frames reach 4.
   - Revert both afterwards.
