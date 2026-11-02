# Report: C4-0 risk check (the search levels)

Plan: plans/onboarding/2026-11-01-onboarding-c4-search-levels.md (C4-0)    Agent: miso-implementer    Branch: thj/onboarding
Outcome: done (read-only). No Unity file changed, no git write, no Play mode. Paths are under `miso/Assets/_Project/` unless they start with `claude-handoff/`.

**Headline:** almost everything works as data or with small editor-tool work. **One stop:** Catch & Return is **not** open by default on this branch (question 5). Turning it on means changing global data or adding a run-upgrade grant, and THJ has to pick. No core-system code change is needed anywhere else.

---

## 1. Pair-mission levels from the default template

**Verdict: works as data.**

- **Placed heroes and fixed rosters.** `CombatLevelRunHandler.FillRosterSlots` (`Core/Managers/CombatLevelRunHandler.cs:264-316`) collects the units already in the level and their nicknames (`:266-267`). It then spawns only the roster units whose nickname is **not** already placed, into `GUnitPlaceHolder`s (`:305-315`). If the River places John and Lucy and its roster has the same two as fixed slots, nothing gets spawned and the placed units play. The Hearth already runs this way (C3: fixed John, Lucy, Linda, with the heroes placed).
- **FTP "starts full" with no filler.** `FactionTracker.EnterMission` → `InitializePoints` (`Core/Units/Runtime/Factions/FactionTracker.cs:139-144, 54-62`) builds `FamilyTimePoints` from the **roster** units. The constructor sets `Value = _maxValue` (`Core/Systems/AbilitySystem/Points/Runtime/FamilyTimePoints.cs:44-49`). `GameHandler.InitiateMission` (`Core/Managers/GameHandler.cs:83-93`) does not call `OnLevelLoad`, so the first level gets no extra gain. A restart of the first level resets to full (`FactionTracker.cs:201-209`). Result: River 5+3 = 8, Ridge 2+3 = 5, both full. The default template `LevelM1-C2` has **no** `LevelStartFPFiller` (0 references in the prefab), and the builder says so (`Core/Levels/Editor/GridToLevel/GridToLevelBuilder.Fp.cs:12-16`). So no `level fp` line is needed. Its objectives are the defaults: defeat all, lose when the family is down (`GridTemplateObjectives.cs:8-10`).
- **Palette.** `Content/Levels/Greybox/GridLevelPalette.asset` maps J/L/U/M/c/a to the shared prefabs. `a` → guid `24c5a391…` = `Features/Enemy/Archer Goblin/Prefabs/Unit_ArcherGoblin.prefab`, the same as the built-in table (`GridPalette.cs:49`). The template is `LevelM1-C2` (guid `3def4f87…`).
- **What the three missions point at today** (all placeholders):

| Asset | Level graph | Roster | Drops / XP |
|---|---|---|---|
| `Content/Levels/MS1 - The River.asset` | one node → `Generic Levels/FamilyLevels/M2/LevelLucyJohn-C1.prefab`, `isInitialLevel 0`, no edges | fixed John (`7e82…`) + Lucy (`a18c…`), 0 free | XP 40, Gold 5, `resourceCollectionCount 0`, no collectables |
| `Content/Levels/MS2 - The Ridge.asset` | one node → `Generic Levels/Easy/E3/LevelE3-C1.prefab` | fixed Linda (`a526…`) + Mark (`2946…`), 0 free | XP 40, Gold 5, none |
| `Content/Levels/M2 - The Trail.asset` | one node → `Generic Levels/Easy/E4/LevelE4-C1.prefab` | fixed Lucy + Linda, **1 free**, Toba (`fb08…`) force-excluded | XP 40, Gold 5, none; `initialItemsAvailability: []` |

  `isInitialLevel 0` is fine. `SerializableDependencyGraph.GetEntry` falls back to the first entity that has no incoming edge (`Core/Utilities/SerializableDependencyGraph.cs:220-227`).
- **Drops as data.** `Mission.GetCompletionRewards` (`Core/Levels/Runtime/Mission.cs:230-249`) always gives `completionXPReward` and `completionGoldReward`. On top of that it gives `resourceCollectionCount` random picks from `collectableGResources`, without replacement (`Core/Utilities/MathUtils.cs:111-117`). So for "Timber 1 + Fabric 1, always", set exactly those two entries with min = max = 1 and multiplier constant 1 (as in M6), and set `resourceCollectionCount 2`. Put Gold 20 in `completionGoldReward`, not in the collectables. Ridge: one Steel entry with amount 2, count 1. XP: `completionXPReward 30`.

## 2. Deploy slots (`level deploy x,y`, D-351)

**Verdict: needs editor-tool work (small). Runtime is unchanged.**

- **How a level declares one.** A deploy slot is an instance of `Features/Player/PlaceHolder/Unit_Placeholder.prefab` (component `GUnitPlaceHolder`, `Core/Units/Runtime/GUnitPlaceHolder.cs:22-25`, a `GridPluggableEntity` with `placementSize 0,0`). It sits under a cell's occupant root, the same way a unit does. Levels that use them: `LevelM1-C1/C2/C3`, `LevelM2-C1`, `LevelE2-C1/C2/C3`, `LevelE3-C1`, `LevelE4-C1`, `LevelEasy-Temp`, the three `DungeonSafeRooms`, and `Level1-C3 - Test Khashayar` (14 prefabs). The template `LevelM1-C2` is one of them, and the builder strips its slots (`GridToLevelBuilder.cs:158-167`, "story actors, deploy slots").
- **How the free slots fill it.** See `FillRosterSlots` above. Roster `Slots` lists fixed slots first, then free ones (`Mission.cs:36-42`), minus any already placed. Units are paired with placeholders in `FindObjectsByType` order. Each spawned unit copies the slot's `InitialDirection` (`CombatLevelRunHandler.cs:270-277`). With the sisters placed and one free slot, exactly one unit is left for the one slot, so the order doesn't matter. The pick is set by `CharacterSelectPanelUI.OnContinueClicked` → `MissionRoster.AssignFreeUnits` (`Core/UI/Runtime/Home/CharacterSelect/CharacterSelectPanelUI.cs:316-322`) before the mission starts. So the FTP pool counts the pick: Lucy 3 + Linda 2 + John 5 or Mark 3.
- **What the grid line must do:**
  - **Parse** (`GridBlockParser.ReadLevelLines`, `:220-305`): new key `deploy`, one or more `X,Y` (follow `ReadHidden`, `:311-357`). Add `GridLevelSettings.Deploy` (a list of tiles) in `GridBlock.cs:92-108`, and add `deploy` to the "unknown level setting" message (`:301`).
  - **Validate:** error when the tile is not a floor tile of the block. Warning when the same tile appears twice. For a tile that already holds a unit, pick one rule:
    - (a) **Recommended:** if the unit is a player unit, the slot replaces it, with a warning. The paper blocks draw `J` on 2,1 / 2,5 with "note … or Mark", so the drawing stays readable. An enemy or hazard on the tile is an error.
    - (b) Always an error. The four Trail blocks then change `J` → `.`.
  - **Preview:** list the deploy tiles in the window (`GridToLevelWindow.cs`), and show the slot on the tile in the drawn preview.
  - **Build:** after `BuildGrid`, instance `Unit_Placeholder.prefab` on the anchor cell's occupant root at the cell centre, as `BuildGrid` does for units (`GridToLevelBuilder.cs:268-298`). Set `initialDirection` to (1, 0): the hand-made levels set `initialDirection.x = 1` on their slots (`LevelM1-C2.prefab:337, 601`), and the prefab's default (0,0) would override the spawned unit's facing. Put the prefab path on `GridPalette` and `GridLevelPalette` (a `deploySlotPrefab` field with the built-in default), so it isn't hard-coded.
  - **Tests:** parse (valid tile, off-block tile, duplicate, the unit-tile rule), and a build that places one `GUnitPlaceHolder` on the right cell, facing right.
- **Things to know:**
  - A placeholder that nothing fills stays on the board and its `Visual` sprite shows (`Unit_Placeholder.prefab:92-141`; only `Spawn` destroys it). So use one slot per free slot.
  - The tool's **Play** sandbox already handles slots: `LevelPlaceholderAssignWindow` (`LevelBase.cs:196`) and `LevelFastForwardRoster` (`Core/Levels/Runtime/LevelFastForwardRoster.cs:86-122`).
  - `claude-handoff/tools/level_to_grid.py:64` reads a slot back as a `note … deploy slot`. It could emit the new line instead (a coordinator tool, not mine).
  - Doc: `tech/level-tools.md` "Known limits" lists "deploy slots"; update it.

## 3. Mission map with two branches (MI-11)

**Verdict: works as data.**

- **What opens it.** After a won level, `CombatLevelUIManager` (`Core/UI/Runtime/CombatLevelUIManager.cs:285-288`) runs `ShowMissionMapThenLoad` (`:305-327`). That shows the map only if `MissionTracker.ShouldShowMissionMap` is set. Otherwise it loads the next level directly. `ShouldShowMissionMap` is computed once, in `SetMission` (`Core/Managers/MissionTracker.cs:47`), as "not linear". It becomes true when any level in the run has more than one entity neighbour, upstream or downstream (`MissionTracker.cs:123-138`, `SerializableDependencyGraph.HasMultipleEntityNeighbors :188-193`). The trailhead with two children turns it on for the whole mission.
- **How to mark the branches.** Trailhead → Blood and Trailhead → Tracks as plain edges. Then **both routes → an OR InterNode → the pile**. Don't connect both routes straight to the pile: an Entity node's inputs are `PreviousNodes.All(...)` (`Core/Levels/Runtime/MissionRouteProgress.cs:91-99`), so with direct edges the pile would need both routes and turn "Missed" once the other route is abandoned (`:36-49, 70`). Existing example: M6 (`Content/Levels/M6 - Hidden Sanctuary - Third Step.asset`, graph edges): `9b91… → {3ce8…, 6121…} → OR c59c… (nodeType 1, combineMode 1) → …`.
- **What the map needs per level.** Nothing beyond the level asset. Nodes show `LevelBase.LevelName` (`Core/UI/Runtime/MissionGraph/MissionMapNodeUI.cs:56-70`) and the icons of the level's `SpecTags` (`MissionMapUI.cs:103-117`). Positions are laid out automatically, or come from the graph editor (`MissionMapUI.cs:44`). So the route names come from `level name Follow the blood` / `level name Follow the tracks`. Level names must be unique inside the mission, because levels are looked up by name (`Mission.GetLevel :181-185`). No button or scene data is needed.
- **Side effect:** the map also opens after the chosen route is won, with only the pile available, so that's one extra click. To avoid it, the mission would have to switch to linear partway through, which is Missions core behaviour (`MissionTracker`). I'd accept the extra click.
- **Trailhead without enemies:** the default objective "defeat all" has to be replaced by an exit objective, `UnitTileOccupiedLOCondition` (`Core/Levels/Runtime/LevelObjectiveConditions.cs:183`), as segment 4's "Reach the cub" did. `E` builds as plain floor (`GridBlockParser.cs:112-116`). Levels without enemies already exist: `Content/Levels/DungeonSafeRooms/*`.

## 4. `LevelStartFPFiller` with a negative amount

**Verdict: works as data. The grid line can't write it, so it's set by the wiring script.**

- `LevelStartFPFiller.OnLevelStarted` (`Core/Levels/Runtime/LevelStartFPFiller.cs:20-37`) calls `units[0].Faction.Controller.FamilyTimePoints.Produce(fpAmountToFill)`. `Produce` → `SetValue(Value + value)` → `Mathf.Clamp(value, 0, MaxValuePractical)` (`FamilyTimePoints.cs:51, 71`). So `-99` clamps to 0 and fires `OnValueChanged`. It works. There is also `Consume` and `Drain()` (`:52-53`), but no component calls them, so the filler at −99 is the data path.
- Conditions:
  - (a) `units` must list a placed player unit, or the filler returns early (`:22-23`). The Trail places Lucy and Linda, and `RebindStartFiller` points it at them (`GridToLevelBuilder.cs:326-374`).
  - (b) Set `atbGaugeAmountToFill 0` and `heal off`.
  - (c) It must be wired to the bus `levelStarted`, as `EnsureFullFpFiller` does (`GridToLevelBuilder.Fp.cs:41-42`).
  - (d) It runs on `levelStarted`, after the intro (`CombatLevelRunHandler.cs:185-194`). So the bar reads full during the trailhead intro, then drops.
- **A fresh mission starts full, not at 0** (question 1), so the drain is needed.
- **Tool options:**
  - (i) The wiring script adds or sets the filler: amount −99, ATB 0, wired to the bus.
  - (ii) Extend `level fp` to accept `empty` (−99) next to `full`. It's small, with a test, in the same file.

  Either is the same behaviour. (ii) survives a rebuild.
- **Carry-over to the route level:** `GameHandler.LoadLevel` → `OnLevelLoad(…, false)` adds `round(FPGain × Max)` (`FactionTracker.cs:211-213`). The Bergsons' `Stat_FPG` is 0 at level 0 (`Resources/Factions/BergsonsFaction.asset:296-317`), but it can be bought for Gold 15. A player who spent the River or Ridge gold on it starts the route level with +1 to +2 FTP instead of 0. To keep it at exactly 0, also put a −99 filler on both route levels. That doesn't hurt the lesson: Pass-by fills the pool after the start.

## 5. Catch & Return and the Vault over units

**Catch & Return: STOP. It is not open by default. A decision is needed (data, but global).**

- Gate: `ProjectileCatchAndReturn.TryCatch` returns false unless `faction.Tracker.GetUnlockableState(unlockLiteral)` (`Features/Player/Mark/Scripts/ProjectileCatchAndReturn.cs:146-147`). Mark's prefab sets `unlockLiteral _MarkLindaSynergy` (`Features/Player/Mark/Prefabs/Unit_Mark.prefab:2974`). `GetUnlockableState` = learned literal, **or** `UnlockedByDefault`, **or** a run upgrade that grants it (`FactionTracker.cs:468-477`). The entry in `Resources/Unlockables/UnlockableSet.asset:64-73` reads **`unlockedByDefault: 0`**, with a cost of `MainResource_FamilySP 1`. It is Mark's skill-tree node 9 (`Unit_Mark.prefab:1239-1240`). On a fresh save the catch never triggers, and the Ridge's Catch & Return can't be discovered.
- Options:
  - (a) Set `unlockedByDefault: 1` on `MarkLindaSynergy` (one data line). It is open everywhere, on every branch that shares the asset and in existing saves. Mark's Family-tree node then reads as already owned until its new effect (Q5 of the paper plan) exists. This is what D-177 literally says.
  - (b) Make a run upgrade (copy of `Resources/RunUpgrades/LindaLucyCycloneSpreadUnlock/RU_LindaLucyCycloneSpreadUnlock.asset`, `grantUnlockable _MarkLindaSynergy`, unit Mark). Grant it on `GB_s2-ridge` with the existing `LevelStartRunUpgradeGrant` (the C3 pattern). It is scoped to the Ridge and cleared when the mission ends (`FactionTracker.cs:150, 160`), so it isn't open in the Trail unless granted there too. No global change, but it isn't "open by default".
  - (c) Leave it locked in C4 and drop the catch from the Ridge's lesson.

  I'd recommend (a) if D-177 still stands, with the node's new effect tracked separately. (b) if THJ wants no global change before C5.
- Mode: `returnMode: 1` = `BounceBack`, no AP refund (`Unit_Mark.prefab:2962`; enum `ProjectileCatchAndReturn.cs:19-24`; refund only for modes ≠ BounceBack, `:42-43, 233`). This matches D-332. The arrow goes back into the quiver on the catch (`:205, 389-394`).
- **The returned arrow's damage:** the return copy is `LindaAttackArrowReturn.prefab`, made by `Projectile.GetClone`. It carries the original's owner, parameters and stat context (`Core/Entities/Runtime/Projectile.cs:124-131`), so it hits with Linda's arrow effect. It is a new projectile with `_hitCount = 0` (`:102`), and each hit is multiplied by `factor ^ hitCount` (`:488-504`). Its `onHitExtraModifier` is the same as the bow arrow's: `Stat_DMGD`, read from the ability (`LindaAttackArrowReturn.prefab:238-245`). So the first enemy on the way back takes the full arrow damage, the second takes × the falloff, as the paper assumes (6 then 3.6 if `Stat_DMGD` is 0.6). The return stops at Linda (`travelEntireRadius 0`, `destinationMode 1`).

**Vault over units: works as data.** `Resources/UnitSpecific/Player/Mark/Vault/Mark_Ability_Attack_Vault.asset` has `allowRangedReach 1` and `cellApplyWalkabilityMode 2` (SelfWalkable: the landing cell must be free) (`:134-136`). Ranged reach adds every cell within Manhattan radius, whatever lies between (`Core/Systems/GridSystem/Runtime/GridCell.cs:872-891`). The transport is `moveMode 2` = Jump, a straight start → destination path with no walk (`Mark_Ability_Attack_Vault_Effect_UnitTransport.asset`; `AEffectTransporter.cs:72-76`; enum `AbilityEnums.cs:12-17`). Radius: base 3 from `Stat_RANGE` (level 0 factor 0, +1 at the SP level), bounded above by Mark's `StatUB_SPD` (`Vault.asset:82-101, 218-229`). 6,1 → 9,1 over 7,1 / 8,1 is 3. Confirm the 3-tile reach at level 0 in play (the upper bound is Mark's own stat).

## 6. Archer Goblin

**Verdict: works as data.**

- **Range 3:** the attack's `radiusV` constant is 3, traverse Adjacent (Manhattan), `allowRangedReach 1` (`Resources/UnitSpecific/Enemy/ArcherGoblin/Attack/ArcherGoblin_Ability_Attack.asset:215-217, 410-413`). The AI uses the same flag (`Core/Systems/AISystem/Runtime/AIUnitBrain.cs:292, 308`).
- **Over water and rock gaps:** yes. Ranged reach ignores the missing cells (above), and the projectile hits by contact, not by grid path (`Projectile.cs:467-505`). Lucy's attack and role, and Linda's attack, also use ranged reach (`allowRangedReach: 1` in their presets), so the family can hit the islands too.
- **HP:** the unit's HP base factor is 24 (Claw 16) (`Unit_ArcherGoblin.prefab:395-436`; `Unit_DarkClaw.prefab:264-305`), times the enemy faction's `Stat_HP` row for the tier: Standard 1, **Early 1**, **Tutorial 0.6**, Late 1.2 (`Resources/Factions/EnemyFaction.asset:24-35`; tier index `CombatLevel.cs:29-35`, applied in `CombatLevelRunHandler.ApplyEnemyTier :318-366`). Archer: **Tutorial 14.4, Early 24**. Claw: Tutorial 9.6, Early 16. Damage rows: Tutorial 0.5, Early 0.75.
- **Per-instance HP** (Ridge gauntlet 8, blood gully 12): there's no grid line for it. Use the C3 pattern instead: override the instance's `statAttributes.attributeEntries.Array.data[0].upgradeLevels.Array.data[0].factor` (`Content/Levels/Greybox/GB_m4-mark.prefab:2239-2240`). Claw HP = 16 × factor × tier factor:
  - Ridge HP 8 at Tutorial → factor **0.8333**
  - Blood gully HP 12 at Early → **0.75**
  - Side gully 16 → default 1
- **Palette `a`:** yes, `Unit_ArcherGoblin.prefab` (question 1).
- **Walks across `_`?** No. `_` means "no GridCell" (`GridBlock.cs:148-152, 162`). The Archer has a Walk ability, but no cell means no path. The River islands (pockets {8,5 9,5 8,6 9,6}, {13,5 14,5 13,6 14,6}, {8,1 9,1 8,0 9,0}) are sealed. 11,3 is 4 from every tile an Archer can stand on except its own 9,5 / 13,5 / 9,1, which are exactly 4. So 11,3 is safe at range 3.

## 7. Bark conditions

**Verdict: neither condition exists. Adding them is feature code in the bark system (not a core system). Out of C4 scope, as planned.**

- The condition nodes (`Core/Systems/BarkSystem/Editor/Nodes/BarkConditionNodes.cs:39-641`): turn number, fallen unit, level, mission, dead enemy type, killer, killing ability, level index, participant, visit count, ability, performer, target, use count, idle, phase direction, objective, faction unit count, `UnitStateCondition` (Any / Alive / Fallen / HPBelowPercent, `BarkGraphData.cs:59`), damage receiver / dealer / amount / fatality, FP delta, FP full, selected unit, pass-by units, encountered enemy.
- There is **no distance or proximity condition** ("Lucy within 3 of John") and **no arrow or quiver count** ("Linda has ≥ 1 arrow"). `BarkManager.EvaluateCondition` (`Core/Systems/BarkSystem/Runtime/BarkManager.cs:1363`) has no cases for them. Each needs a new editor node plus a runtime case, and the arrow count would read `LindaQuiver`.
- **Bark graphs by hand: confirmed.** `BarkGraphSeeder` can only seed defaults (an Entry node, a subgraph input) through reflection, because "Graph Toolkit 0.4 has no public API for creating nodes" (`Core/Systems/BarkSystem/Editor/BarkGraphSeeder.cs:10-20`).

## 8. Starts-alert variant for the pile's rear wave

**Verdict: works as data.**

- `GUnitSpawnManipulationAction` (`Core/Levels/Utilities/Runtime/LevelSpecificBehaviour.cs:100-196`) calls `GUnit.SpawnAt` (`Core/Units/Runtime/GUnit.cs:405-430`). That instantiates the prefab, plugs it in and calls `Faction.Controller.RegisterUnit`, which raises `unitBorn` (`Core/Interactions/Runtime/FactionControllerBase.cs:125-131`). `EnemyAlertTracker.OnUnitBorn` → `Register` (`EnemyAlertTracker.Events.cs:99-109`) reads `unit.GetComponent<EnemyAlertSettings>().StartsAlert` (`EnemyAlertTracker.cs:125-133`) and skips Unaware for it (`EnemyAlertRules.StartsUnaware :150-154`). So a variant of `Unit_DarkClaw` with `EnemyAlertSettings.startsAlert = true` spawns alert. The field's tooltip says "placed unit", but the code path is shared.
- Spawned units read the level's tier, because it is applied on the faction (`CombatLevelRunHandler.cs:318-325`).
- Trigger: the stage's `OnCompleteSequence` → `LSBExecutionSequence` → an LSB call holding the GUnitSpawn action (the C3 `motherFalls` pattern). Spawn cells are the `GridCell` references for 0,6 / 0,5, which the wiring script finds by name.
- Check: `SpawnAt` fails silently if the cell is occupied (`CanOccupy`, `GUnit.cs:408`). A family member standing on 0,6 or 0,5 at turn 2 blocks that Claw.

## 9. What the blocks ask for that the tool or data can't express

| Item | Status |
|---|---|
| **"Wake together"** (River clearing) | Data, already true. Default Sight 3, AlertRange 2 (`Features/_Common/Prefabs/UnitBase.prefab:2504-2508, 2561-2565`); spread is recursive within alert range (`EnemyAlertRules.cs:82-88`). 5,3 / 6,4 / 6,2 are 2 apart from each other, and 4 or more from the islands, so the islands don't wake with them. |
| **Ridge rush wakes at start** | Data, already true: 2,4 is 3 from Linda at 2,1 → starts alert by sight and spreads to 1,5 and 3,5 (`EnemyAlertTracker.cs:131-136`). |
| **"Family starts 4+ from enemies"** | True in all six blocks as drawn (River John 1,3 → Claw 5,3 = 4; Ridge Mark 3,1 → 7,1 = 4; blood 2,1 → 4,3 = 4). The tool doesn't check it. A preview warning would be optional, not needed. |
| **Per-instance HP** | Not in the tool (`tech/level-tools.md` Known limits). Wiring script, factors in question 6. |
| **Props** (clue on 16,3 / 13,1, the pile's carcasses on 4,3-5,4, water visuals) | Not in the tool. Placeholder objects added by the wiring script under the level root (the C3 "Memory Scenery" pattern). The template's scenery stays and doesn't match the shape (Known limits). |
| **`_` water** | Builds as "no tile", same as `#` (`GridBlock.cs:148-152`). Gameplay is right (nothing walks there, shots cross it). No water is drawn; that's a prop or visual job. |
| **`@` safe tile, `note`, `arrow`, `zone`, `range`, `cells` lines** | Drawing aids only: `@` builds as plain floor (`GridBlock.cs:152`), notes are skipped (`GridBlockParser.cs:12-14`). Nothing marks 11,3 in game. |
| **`E` exit** (trailhead) | Plain floor with a warning (`GridBlockParser.cs:112-116`). The exit objective goes in the wiring script (`UnitTileOccupiedLOCondition`). |
| **"or Mark" on 2,1 / 2,5** | The new `level deploy` line (question 2). |
| **Turn-2 rear wave on 0,6 / 0,5** | Wiring: a queued stage `TurnReachedLOCondition` (`LevelObjectiveConditions.cs:209`) whose `OnCompleteSequence` spawns. The "defeat all" stage queued after it, so the level can't end before the wave. |
| **Encore cue on "both Archers dead"** | Wiring: a stage with a `UnitDeathLOCondition` per Archer (`:112`) or `LivingUnits` filtered to them; `OnCompleteSequence` = camera, then line. |
| **FTP drain** | Question 4 (wiring script, or `level fp empty`). |

## Needs THJ

1. **Catch & Return gate** (question 5). It is locked on this branch (`UnlockableSet.asset:64-73`, `unlockedByDefault: 0`).
   - (a) Recommended if D-177 stands: open it by default (a global data line, `MarkLindaSynergy`).
   - (b) A Ridge-only run-upgrade grant (new RU asset plus the existing `LevelStartRunUpgradeGrant`).
   - (c) Leave it locked in C4.

   Until this is answered, C4b's catch acceptance check can't pass.
2. **(Coordinator call, Tier 2) Deploy line on a tile with a drawn hero:** replace it with a warning (recommended), or make it an error and edit the four Trail blocks.

## What each chunk needs

**C4a The River.**
- Build `river` with `level name The River`, `level tier tutorial`. No `fp` or `alert` line.
- Wiring script (`Wire Search: River`):
  - Intro: camera pan to 16,3 and back; Lucy's Family Role panel; John "Stay by me."
  - Clue props on 16,3; an end sequence with the close-up.
- Mission data: graph → `GB_s1-river` (one node); `completionXPReward 30`; `completionGoldReward 20`; collectables Timber 1 + Fabric 1 with `resourceCollectionCount 2`.
- The roster stays as it is.
- Tests: graph, drops, roster, intro and outro, no `[PLACEHOLDER]` tag.
- No tool or code change.
- Answer for the plan: "Lucy within 3" has no bark condition.

**C4b The Ridge.**
- **Needs THJ's answer to question 5 first.**
- Build `ridge` (`tier tutorial`).
- Wiring: gauntlet Claws 7,1 / 8,1 HP factor 0.8333; clue props on 13,1; end sequence.
- Mission data: graph; XP 30; Gold 20; Steel 2 (count 1).
- If 5(b) is chosen: RU asset + grant component.
- Tests as C4a.
- No tool change.
- Play check: the 3-tile Vault at level 0, and the return damage (question 5).

**C4c The Trail.**
- **Tool first (own commit):** `level deploy x,y` (parse, validate, preview, build `Unit_Placeholder` facing right, a palette field, tests, the `tech/level-tools.md` line). Optional: `level fp empty`.
- **Then the levels.** Build four levels:
  - `m2-trailhead`, `level name` e.g. "The Trailhead"
  - `m2-blood`, `level name Follow the blood`
  - `m2-tracks`, `level name Follow the tracks`
  - `m2-pile`

  All four `tier early`, each with `level deploy` on the "or Mark" tile.
- **Wiring:**
  - Trailhead: exit objective on the `E` tile; filler −99 (also on both route levels if the bought FTP gain must not leak); the "stays home" line.
  - Blood: gully Claws HP factor 0.75; the FTP and Pass-by panel.
  - Tracks: a stage for "both Archers dead" with the Encore `OnCompleteSequence`.
  - Pile:
    - New prefab variant `Unit_DarkClaw_StartsAlert` with `EnemyAlertSettings.startsAlert` (beside the Claw; the shared prefab is not edited).
    - An LSB `GUnitSpawn` on the 0,6 / 0,5 cells, played from a queued `Turn reached 2` stage, then a "defeat all" stage.
    - The items panel, the tally lines, the end clue.
- **Mission data:**
  - Graph: trailhead → blood and trailhead → tracks; blood and tracks → **OR InterNode** → pile (the M6 pattern).
  - `initialItemsAvailability`: Health Potion 2, Family Trinket 1.
  - XP and Gold per plan.
  - The roster stays as it is (Lucy and Linda fixed, 1 free, Toba excluded).
- **Tests:** graph shape including the OR node and two entry children, deploy slot count = 1 per level, filler −99 wired to `levelStarted` and pointed at the placed sisters, variant `startsAlert`, stages.
- Expected: the map opens after the route as well, with only the pile to choose (question 3).
- Optional, coordinator: `level_to_grid.py` could read slots back as `level deploy`.

## Save reset

No (no Play mode).

## Risks and loose ends

- `ShouldShowMissionMap` is fixed for the whole mission, so the map shows after every won level of the Trail except the last.
- Spawns are skipped silently on occupied cells (the rear wave).
- Unfilled deploy slots stay visible.
- A bought `Stat_FPG` upgrade adds FTP when a route level loads.
- `LevelStartFPFiller` uses `units[0]`. A Trail level with no placed player units would skip the drain silently.

## Proposed commits

None (read-only check).

## How to see it

Nothing to see; this is a code read. C4a can start right away. C4b needs THJ's answer on the Catch & Return gate.
