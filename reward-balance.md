# Reward Balance: reference for future changes

Last updated 2026-10-07 (branch `main`). Values applied on that date, not yet verified in play.
Design doc (tables, reasoning, decisions): "Miso Reward Balance M1–M7",
https://claude.ai/code/artifact/22659269-7bac-4508-b45d-4f966ca8e5e5
This file is the "where is everything" companion. `claude-handoff/` is git-excluded; never stage it.

All paths below are relative to `miso/Assets/_Project/` unless they start with `claude-handoff/`.

## 1. Design rules (short)
- Low progression: the same enemies are used from M1 to M7, so each main-path step pays for about ONE purchase at the station that just opened. Replays (full rewards) and future side missions supply the rest.
- Gold only from fixed `completionGoldReward` + kills. `collectableGResources` = materials only (it is a random pick, gold there displaces materials).
- Kill rewards live ONLY on enemy prefabs. No per-level overrides (THJ removed them 2026-10-06).
- M2/M5 and the two M3s can be played in either order: keep each pair's gold similar.
- Hub unlocks: after M1 nothing (mission select only) · first of M2/M5 → skill tree · second → Kitchen · first M3 → Workshop · second M3 → Training Ground + Family Room.

## 2. How rewards are computed (code)
| What | Where |
|---|---|
| Mission completion / failure rewards | `Core/Levels/Runtime/Mission.cs`: `GetCompletionRewards` (XP + gold + `collectableGResources.RandomElements(resourceCollectionCount)`), `GetFailureRewards` (20% XP, 50% gold; none if failed on the mission's first level), `GetCompletionRewardResources` (loot preview) |
| Random pick | `Core/Utilities/MathUtils.cs` `RandomElements`: N DISTINCT entries, shuffled; count ≥ list length = all guaranteed |
| Amount roll | `CollectableGResource.Collect` (`Core/Systems/StatsResourcesSystem/Runtime/GResources/GResource.cs`) → `IntBounds.RandomValue` (`Core/Utilities/DataStructures.cs`) = `Random.Range(min, max + 1)`, **inclusive** since 2026-10-07 (before: max excluded, so 0–1 always gave 0). `Core/Entities/Runtime/Pickup.cs` uses the same `RandomValue`. |
| Kill trigger | `CombatLevelRunHandler.OnAbilityComplete` → `onAbilityPerformedOn` → `OnAbilityPerformedOn`: for each enemy an ability hit, compares HP against the snapshot taken at `OnAbilityActivationStart`; if HP reached min it is a kill → `AwardAbilityDamageResources` + `ShowRewardPopups` ("+N XP" cyan, "+N Gold" gold, via `DamageNumberManager`). Kills not caused by an ability (burn ticks) pay nothing. Kill gold is stored per mission and reaches the wallet at `QuitMission` (`FactionTracker.WrapUpResourceCollection`); defeat keeps only XP/SP (`ClearCollectedResources`). |
| Kill rewards | `Core/Units/Runtime/GUnit.cs` fields `abilityDamageXpReward` (0 everywhere), `lethalDamageXpBonus`, `resourceCollectionCount`, `collectableGResources`; `GetAbilityDamageRewards` (~line 1030). Drops roll only on a lethal hit |
| Awarding | `Core/Managers/CombatLevelRunHandler.cs` `AwardResources`, `AwardAbilityDamageResources`, `AwardMissionCompletionResources`, `AwardMissionFailureResources` (~line 750–850) |
| Split | `Core/Units/Runtime/Factions/FactionTracker.cs` `CollectResourceSplit`: non-aggregated resources (XP, SP) split evenly over the player units in the level, **rounded up** (`Mathf.CeilToInt`, changed 2026-10-06 from RoundToInt). In practice only XP goes through it: SP is added directly in `CheckLevelUps`, and no mission or enemy lists SP as a reward (the `MainResource_SP` hits in level prefabs are skill-tree cost overrides on placed player units). Aggregated ones (Gold, Steel, Timber, Fabric, Stone, FamilySP) go to the shared wallet |
| Level-ups | `FactionTracker.CheckLevelUps`: SP count = number of thresholds ≤ total XP. Thresholds in `Resources/Game Data.asset` field `xpLevelThresholds` (hex little-endian int32 array): 0, 75, 200, 375, 600, 875, 1200, 1575, 2000, 2475. First SP is free at 0 XP |
| Resource definitions | `Resources/GResources/GResourceSet.asset` (ids `MainResource_<Gold|XP|SP|FamilySP|Steel|Timber|Fabric|Stone>`, `aggregated` flag) |
| Mission order | `Resources/Game Data.asset` `missionDependencyGraph`: M1 → {M2, M5} → AND → {M3 Wolf, M3 Mark Intro}; M3 Wolf → {M4, M6}; M6 → M7. Mark Intro gates nothing |

## 3. Data files and current values

### Missions (`Content/Levels/`)
| File | Name in game | Roster | XP | Gold | Pick / list |
|---|---|---|---|---|---|
| `M1 - Hidden Sanctuary - First Step.asset` | John's Map | John, Lucy | 40 | 5 | none |
| `M2 - Ryler is Lost.asset` (filename typo) | Ryker is lost | Lucy, John | 40 | 5 | 1 / Steel 1 |
| `M5 - Hidden Sanctuary - Second Step.asset` | The Healer | John, Linda, Lucy | 90 | 5 | 1 / Timber 1 |
| `M3 - Blood Trail of A Wolf.asset` | A Wolf's Blood | John, Linda | 65 | 10 | 1 / Timber 1 |
| `M3 - Mark Intro.asset` (has one CR inside its description; keep bytes) | No More Waiting | Mark, Lucy | 60 | 10 | 1 / Fabric 1 |
| `M4 - The White Mothers.asset` | Into the Rootwell | John, Linda, Lucy (+Toba last 2 levels) | 120 | 20 | 4 / Steel, Timber, Stone, Fabric 1 each |
| `M6 - Hidden Sanctuary - Third Step.asset` | The Arcanum | John + 2 free | 90 | 15 | 2 / Steel, Timber, Stone, Fabric 1 each |
| `M7 - Hidden Sanctuary - Finale.asset` | In My Father's Arms | John + 2 free | 165 | 20 | 2 / Steel, Timber, Stone, Fabric 1–2 each |
| M8–M14, MX | | | not rebalanced yet (still old style with Gold in the pick list) | | |

Fields: `completionXPReward`, `completionGoldReward`, `resourceCollectionCount`, `collectableGResources[]` (`resourceRef.entityID`, `amountRange.min/max`, multiplier constant 1).

### Level prefabs per mission (order played)
- M1: `Content/Levels/Level1/Level1-C1_TArtEx`, `Level1-C1-2`, `Level1-C2`
- M2: `Content/Levels/Generic Levels/FamilyLevels/M2/LevelLucyJohn-C1`, `-C2`, `-C3`
- M5: `Generic Levels/Easy/E1/LevelE1-C1`, `-C2`
- M3 Wolf: `Generic Levels/FamilyLevels/LevelLindaJohn-C1`, `-C2`
- M3 Mark Intro: `Generic Levels/FamilyLevels/MarkIntro/LevelMarkIntro-C1` (wave spawner of Dark Claws, `unitPrefab` entries), `-C2`, `-C3`
- M4: `Level2/LevelDomFight` → `Level2-C1-TArtEx` → `Level2-C2` → `Level2-C3-1` → `Level2-C3-2` → `Level3/Level3-C1` (Goblin Queen)
- M6: `Generic Levels/Easy/E2/LevelE2-C1` → (`DungeonSafeRooms/LevelDivineRelicRoom` or) `LevelE2-C2` → `LevelRunUpgradeRoom` / `LevelHealingRoom` → `LevelE2-C3` (3–4 fights)
- M7: `Generic Levels/Easy/E3/LevelE3-C1`
- Graph is the hidden `levelDependencyGraph` on the Mission asset (open with the asset's "Open Level Dependency Editor" button).

### Enemies (`Features/Enemy/`), prefab variants of `Content/Levels/_Common/Prefabs/UnitBase.prefab`
| Prefab | Kill XP | Gold |
|---|---|---|
| `Dark Claw/Prefabs/Unit_DarkClaw.prefab` | 3 | 0–1 |
| `Dark Claw/Prefabs/Unit_BlackClaw.prefab` (variant of Dark Claw, tougher; own overrides) | 5 | 0–2 |
| `Dark Worm/Prefabs/Unit_DarkWorm.prefab` | 3 | none |
| `Archer Goblin/Prefabs/Unit_ArcherGoblin.prefab` | 4 | 0–1 |
| `Dark Shaman/Prefabs/Unit_DarkShaman.prefab` | 4 | 1–2 |
| `Masher Goblin/Prefabs/Unit_MasherGoblin.prefab` | 10 | 1–3 |
| `Mountain Deev/Prefabs/Unit_Deev.prefab` | 10 | 1–3 |
| `Goblin Queen/Prefab/Unit_GoblinQueen.prefab` (note `Prefab/`, singular) | 30 | 5 |
Old values: Claw/Black Claw/Worm/Shaman 9, Archer 12, Masher/Deev 30, Queen 120 XP. Gold min defaults to 0 when only max is overridden.

### Sinks (what rewards are spent on)
- Skill trees: SP only, authored on the unit prefabs `Features/Player/<John|Lucy|Linda|Mark>/Prefabs/Unit_*.prefab`, `Features/Player/Dom/Prefabs/Unit_Toba.prefab` (`skillTree` field). 6 nodes, 8 pips, tiers at 0/1/2/3 SP spent. See `claude-handoff/player-skill-trees.md`.
- Family stats: `Resources/Factions/BergsonsFaction.asset` `statAttributes.attributeEntries[].upgradeLevels[]` (`factor`, `resourceRequirements`). 11 upgradable stats, 905 gold to max all. Values as of 2026-10-06 (THJ raised prices, HP L1 to x1.15):
  | Stat | L1 / L2 / L3 factor | Cost L1 / L2 / L3 (gold) |
  |---|---|---|
  | Stat_HP | 1.15 / 1.25 / 1.4 | 20 / 30 / 50 |
  | Stat_HPG (HP gain) | 0.1 / 0.2 / 0.3 | 20 / 30 / 50 |
  | Stat_HPP (HP potion) | 1.5 / 2 / 2.5 | 10 / 15 / 40 |
  | Stat_DMG | 1.1 / 1.2 / 1.3 | 20 / 30 / 50 |
  | Stat_DR | 0.9 / 0.85 / 0.8 | 15 / 20 / 40 |
  | Stat_EVA | 0.05 / 0.09 / 0.13 | 15 / 20 / 40 |
  | Stat_CRC | 0.075 / 0.11 / 0.15 | 15 / 20 / 40 |
  | Stat_FP | 1 / 1.5 / 2 | 20 / 30 / 50 |
  | Stat_FPG (FP gain) | 0.18 / 0.27 / 0.35 | 15 / 20 / 40 |
  | Stat_FPP (FP potion) | 1.2 / 1.35 / 1.5 | 10 / 15 / 40 |
  | Stat_WIS | 1.2 / 1.3 / 1.4 | 15 / 20 / 40 |
  Dump the live values with `reward-tools/faction_stats.py`.
  - Stations (Home scene `Features/Home - Imported/___Khashayar/Home - Scene.unity`, panels driven by `Features/Home - Imported/___Khashayar/HomeManager.cs`, UI `Core/UI/Runtime/Home/UpgradePanel/FactionStatUpgradePanelUI.cs`): KitchenUpgradePanel = HP, HPG, HPP, WIS · TrainingGroundUpgradePanel = DMG, DR, EVA, CRC, WIS · FamilyStatUpgradePanel ("Family Room" / bookshelf) = FP, FPG, FPP, WIS.
- Workshop: `Resources/Unit Equipments/<Unit>/Equipment_*.asset` (12 items), levels Lv2/Lv3/Lv4 cost 10/20/40 gold + 1/3/5 material (Wrist Wrap 50 at the top level, Shield 15 at the middle one, Axe/Necklace/Shin/Brooch mix materials). UI `Core/UI/Runtime/Home/WorkshopPanelUI.cs`, logic `Core/Data/Runtime/EquipmentManager.cs`. Only items of unlocked units show.
- Run-upgrade shop room (`DungeonSafeRooms/LevelRunUpgradeRoom`) costs nothing.

## 4. Tools (`claude-handoff/reward-tools/`, Python 3, no Unity needed, read YAML directly)
Run from that folder. First `python3 build_guidmap.py` if prefabs were added or moved (a `guidmap.json` from 2026-10-06 is there).
- `mission_rewards.py`: print all missions' rewards (read-only).
- `lvl.py "<level prefab path>" ...`: goals, enemy counts, effective kill XP/gold per level, including any per-level overrides.
- `mods.py <prefab> ...`: list reward overrides inside a prefab (on a level prefab, any line = an override to remove).
- `units.py`: list base kill values of all enemy prefabs.
- `faction_stats.py`: print every BergsonsFaction stat's factors and costs per level.
- `set_mission_rewards.py`, `set_enemy_rewards.py`: write values (tables at the top hold the 2026-10-06 state). They edit text in place and keep line endings. Let Unity reimport, then check the Inspector.
Over the device bridge, scanning whole folders is slow (`grep -r` over `_Project` times out); target folders like above. `git diff` on the whole repo is slow too: scope it to a path.

## 5. Open items (2026-10-06)
- [x] Leftover archer overrides in `Level1-C2` (M1) and `LevelE1-C1` (M5) removed by THJ. (`Level1/Level1-C4.prefab` still has overrides but is not in any M1–M7 graph.)
- [ ] Recompile + EditMode tests after the `FactionTracker` change.
- [ ] Playtest M1–M7: each step leaves an affordable purchase.
- [x] Family stat L1 made less dominant: prices raised, HP L1 x1.15 (THJ). If late fights still feel easy, lower DMG/DR L1 next.
- [ ] Tightest step: second M3 gives ~15 gold vs Training Ground / Family Room L1 prices of 10-20. Check in play.
- [ ] Rebalance M8–M14 + MX (still Gold in pick lists; kill XP now lower everywhere).

## 6. Change log
| Date | Change |
|---|---|
| 2026-10-07 | `IntBounds.RandomValue` made max-inclusive; `Pickup` switched to it. Enemy gold and mission material ranges now roll their full stated range. |
| 2026-10-06 | BergsonsFaction prices raised (HP/HPG/DMG/FP 20/30/50, potions 10/15/40, rest 15/20/40), HP L1 x1.15 (THJ). |
| 2026-10-06 | Black Claw raised to 5 XP, 0–2 gold (THJ); last two archer overrides removed (THJ). |
| 2026-10-06 | Missions M1–M7 rewards rewritten (table in section 3). Enemy kill values lowered. Per-level kill overrides removed (THJ). XP split rounds up. |
