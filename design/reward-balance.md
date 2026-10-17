# Reward Balance: reference for future changes

Last updated 2026-10-17 (branch `main`): current values replaced with links to the GDD (D-047). The rewards themselves were applied on 2026-10-06 and 2026-10-07 and are not yet verified in play.
**Current values live in the GDD:** mission rewards in [Missions and structure](gdd/missions-structure.md#missions), kill XP and gold in [Enemies](gdd/enemies.md#roster), XP thresholds, family stats, gear and the hub in [Progression and economy](gdd/progression-economy.md). This file keeps the design rules and their reasoning, the map of code and data files, the tools and the change history.
Design doc (tables, reasoning, decisions; values as of 2026-10-07): "Miso Reward Balance M1–M7",
https://claude.ai/code/artifact/22659269-7bac-4508-b45d-4f966ca8e5e5
This file is the "where is everything" companion. `claude-handoff/` is excluded from the shared repo (it is its own private repo); never stage it there.

All paths below are relative to `miso/Assets/_Project/` unless they start with `claude-handoff/`.

## 1. Design rules (short)
- Low progression: the same enemies are used from M1 to M7, so each main-path step pays for about ONE purchase at the station that just opened. Replays (full rewards) and future side missions supply the rest.
- Gold only from fixed `completionGoldReward` + kills. `collectableGResources` = materials only (it is a random pick, gold there displaces materials). GDD [PR-24](gdd/progression-economy.md#mission-rewards); M8–M14 and MX still break it.
- Kill rewards live ONLY on enemy prefabs. No per-level overrides (THJ removed them 2026-10-06).
- M2/M5 and the two M3s can be played in either order: keep each pair's gold similar.
- Hub unlocks: the order is GDD [PR-34](gdd/progression-economy.md#the-hub-on-main). The first rule pairs each step's rewards with the station that step opens.

## 2. How rewards are computed (code)
| What | Where |
|---|---|
| Mission completion / failure rewards | `Core/Levels/Runtime/Mission.cs`: `GetCompletionRewards` (XP + gold + `collectableGResources.RandomElements(resourceCollectionCount)`), `GetFailureRewards` (the share kept after a loss: [PR-22](gdd/progression-economy.md#mission-rewards)), `GetCompletionRewardResources` (loot preview) |
| Random pick | `Core/Utilities/MathUtils.cs` `RandomElements`: N DISTINCT entries, shuffled; count ≥ list length = all guaranteed |
| Amount roll | `CollectableGResource.Collect` (`Core/Systems/StatsResourcesSystem/Runtime/GResources/GResource.cs`) → `IntBounds.RandomValue` (`Core/Utilities/DataStructures.cs`) = `Random.Range(min, max + 1)`, **inclusive** since 2026-10-07 (before: max excluded, so 0–1 always gave 0). `Core/Entities/Runtime/Pickup.cs` uses the same `RandomValue`. |
| Kill trigger | `CombatLevelRunHandler.OnAbilityComplete` → `onAbilityPerformedOn` → `OnAbilityPerformedOn`: for each enemy an ability hit, compares HP against the snapshot taken at `OnAbilityActivationStart`; if HP reached min it is a kill → `AwardAbilityDamageResources` + `ShowRewardPopups` ("+N XP" cyan, "+N Gold" gold, via `DamageNumberManager`). Kill gold is stored per mission and reaches the wallet at `QuitMission` (`FactionTracker.WrapUpResourceCollection`); on defeat `ClearCollectedResources` drops it. Rules: [CR-22](gdd/combat-rules.md#attacks-and-damage) (only ability kills pay), [PR-3](gdd/progression-economy.md#resources), [CR-34](gdd/combat-rules.md#winning-losing-and-leaving) |
| Kill rewards | `Core/Units/Runtime/GUnit.cs` fields `abilityDamageXpReward` (0 everywhere), `lethalDamageXpBonus`, `resourceCollectionCount`, `collectableGResources`; `GetAbilityDamageRewards` (~line 1030). Drops roll only on a lethal hit |
| Awarding | `Core/Managers/CombatLevelRunHandler.cs` `AwardResources`, `AwardAbilityDamageResources`, `AwardMissionCompletionResources`, `AwardMissionFailureResources` (~line 750–850) |
| Split | `Core/Units/Runtime/Factions/FactionTracker.cs` `CollectResourceSplit`: non-aggregated resources (XP, SP) split evenly over the player units in the level, **rounded up** (`Mathf.CeilToInt`, changed 2026-10-06 from RoundToInt). In practice only XP goes through it: SP is added directly in `CheckLevelUps`, and no mission or enemy lists SP as a reward (the `MainResource_SP` hits in level prefabs are skill-tree cost overrides on placed player units). Aggregated ones (Gold, Steel, Timber, Fabric, Stone, FamilySP) go to the shared wallet. Who shares: [PR-5](gdd/progression-economy.md#experience-and-levels) |
| Level-ups | `FactionTracker.CheckLevelUps`: SP count = number of thresholds ≤ total XP. Thresholds in `Resources/Game Data.asset` field `xpLevelThresholds` (hex little-endian int32 array); values in [PR-6](gdd/progression-economy.md#experience-and-levels) |
| Resource definitions | `Resources/GResources/GResourceSet.asset` (ids `MainResource_<Gold|XP|SP|FamilySP|Steel|Timber|Fabric|Stone>`, `aggregated` flag) |
| Mission order | `Resources/Game Data.asset` `missionDependencyGraph` (all gates are AND gates). The graph: [Missions and structure](gdd/missions-structure.md#campaign) (MI-1, MI-5) |

## 3. Data files (values in the GDD)

### Missions (`Content/Levels/`)
Roster, XP, Gold, material pick and starting items per mission: [Missions and structure](gdd/missions-structure.md#missions).

| File | Name in game | Note |
|---|---|---|
| `M1 - Hidden Sanctuary - First Step.asset` | John's Map | |
| `M2 - Ryler is Lost.asset` | Ryker is lost | Filename typo |
| `M5 - Hidden Sanctuary - Second Step.asset` | The Healer | |
| `M3 - Blood Trail of A Wolf.asset` | A Wolf's Blood | |
| `M3 - Mark Intro.asset` | No More Waiting | Has one CR inside its description; keep bytes |
| `M4 - The White Mothers.asset` | Into the Rootwell | |
| `M6 - Hidden Sanctuary - Third Step.asset` | The Arcanum | |
| `M7 - Hidden Sanctuary - Finale.asset` | In My Father's Arms | |
| M8–M14, MX | | Not rebalanced yet: Gold is still in their pick lists ([PR-24](gdd/progression-economy.md#mission-rewards)) |

Fields: `completionXPReward`, `completionGoldReward`, `resourceCollectionCount`, `collectableGResources[]` (`resourceRef.entityID`, `amountRange.min/max`, multiplier constant 1).

### Level prefabs per mission
The order played, the route choice, the enemy tier and deploy slots of every level: [Missions and structure](gdd/missions-structure.md#missions) (second table). Where the prefabs are, under `Content/Levels/`:
- M1: `Level1/` (`Level1-C1_TArtEx`, `Level1-C1-2`, `Level1-C2`)
- M2: `Generic Levels/FamilyLevels/M2/` (`LevelLucyJohn-C1` to `-C3`)
- M5: `Generic Levels/Easy/E1/` (`LevelE1-C1`, `-C2`)
- M3 Wolf: `Generic Levels/FamilyLevels/` (`LevelLindaJohn-C1`, `-C2`)
- M3 Mark Intro: `Generic Levels/FamilyLevels/MarkIntro/` (`LevelMarkIntro-C1` to `-C3`; C1's Dark Claw waves are its spawner's `unitPrefab` entries)
- M4: `Level2/` (`LevelDomFight`, `Level2-C1-TArtEx`, `Level2-C2`, `Level2-C3-1`, `Level2-C3-2`) and `Level3/Level3-C1` (Goblin Queen), plus a copy of the Divine Relic room
- M6: `Generic Levels/Easy/E2/` (`LevelE2-C1` to `-C3`) and `DungeonSafeRooms/` (`LevelDivineRelicRoom`, `LevelRunUpgradeRoom`, `LevelHealingRoom`)
- M7: `Generic Levels/Easy/E3/LevelE3-C1`
- Graph is the hidden `levelDependencyGraph` on the Mission asset (open with the asset's "Open Level Dependency Editor" button).

### Enemies (`Features/Enemy/`), prefab variants of `Features/_Common/Prefabs/UnitBase.prefab`
Kill XP and gold per enemy: [Enemies](gdd/enemies.md#roster).

| Enemy | Prefab |
|---|---|
| Dark Claw | `Dark Claw/Prefabs/Unit_DarkClaw.prefab` |
| Black Claw | `Dark Claw/Prefabs/Unit_BlackClaw.prefab` (variant of Dark Claw, with its own overrides) |
| Dark Worm | `Dark Worm/Prefabs/Unit_DarkWorm.prefab` |
| Archer Goblin | `Archer Goblin/Prefabs/Unit_ArcherGoblin.prefab` |
| Dark Shaman | `Dark Shaman/Prefabs/Unit_DarkShaman.prefab` |
| Masher Goblin | `Masher Goblin/Prefabs/Unit_MasherGoblin.prefab` |
| Mountain Deev | `Mountain Deev/Prefabs/Unit_Deev.prefab` |
| Goblin Queen | `Goblin Queen/Prefab/Unit_GoblinQueen.prefab` (note `Prefab/`, singular) |

Kill XP before 2026-10-06: Claw/Black Claw/Worm/Shaman 9, Archer 12, Masher/Deev 30, Queen 120. Gold min defaults to 0 when only max is overridden.

### Sinks (what rewards are spent on)
- Skill trees: SP only, authored on the unit prefabs `Features/Player/<John|Lucy|Linda|Mark>/Prefabs/Unit_*.prefab`, `Features/Player/Dom/Prefabs/Unit_Toba.prefab` (`skillTree` field). Costs and unlock levels: [PR-6 to PR-8](gdd/progression-economy.md#experience-and-levels); each tree is on its [character sheet](gdd/characters/README.md); the redesign's intent is in `claude-handoff/design/player-skill-trees.md`.
- Family stats: `Resources/Factions/BergsonsFaction.asset` `statAttributes.attributeEntries[].upgradeLevels[]` (`factor`, `resourceRequirements`). Factors, prices and which station sells each: [Family stats](gdd/progression-economy.md#family-stats) (PR-11, PR-12). Dump the live values with `reward-tools/faction_stats.py`.
  - Stations: Home scene `Features/Home - Imported/___Khashayar/Home - Scene.unity`, panels driven by `Features/Home - Imported/___Khashayar/HomeManager.cs`, UI `Core/UI/Runtime/Home/UpgradePanel/FactionStatUpgradePanelUI.cs`. Panel objects: `KitchenUpgradePanel`, `TrainingGroundUpgradePanel`, `FamilyStatUpgradePanel` ("Family Room" / bookshelf).
- Workshop: `Resources/Unit Equipments/<Unit>/Equipment_*.asset` (12 items). Costs and bonuses: [Gear](gdd/progression-economy.md#gear) and each character sheet's Gear section. UI `Core/UI/Runtime/Home/WorkshopPanelUI.cs`, logic `Core/Data/Runtime/EquipmentManager.cs`. Only items of unlocked units show.
- Run-upgrade shop room (`DungeonSafeRooms/LevelRunUpgradeRoom`): not a sink ([PR-27](gdd/progression-economy.md#run-upgrades)).

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
- [ ] Tightest step: the second M3 pays ~15 gold against the level 1 prices at the Training Ground and the Family Room ([Family stats](gdd/progression-economy.md#family-stats)). Check in play.
- [ ] Rebalance M8–M14 + MX (still Gold in pick lists, [PR-24](gdd/progression-economy.md#mission-rewards); kill XP now lower everywhere).

## 6. Change log
| Date | Change |
|---|---|
| 2026-10-17 | Current values replaced with links to the GDD (D-047): the mission, enemy and family-stat tables, the XP thresholds and the hub order. Four things here disagreed with the assets as the GDD read them on 2026-10-16 and were fixed: the mission graph (both M3s together gate M4 and M6), M6's route (the relic or upgrade room comes before `LevelE2-C2`, the Healing Room after it), M4's missing Divine Relic room and `UnitBase.prefab`'s path. |
| 2026-10-07 | `IntBounds.RandomValue` made max-inclusive; `Pickup` switched to it. Enemy gold and mission material ranges now roll their full stated range. |
| 2026-10-06 | BergsonsFaction prices raised (HP/HPG/DMG/FP 20/30/50, potions 10/15/40, rest 15/20/40), HP L1 x1.15 (THJ). |
| 2026-10-06 | Black Claw raised to 5 XP, 0–2 gold (THJ); last two archer overrides removed (THJ). |
| 2026-10-06 | Missions M1–M7 rewards rewritten (now in the GDD's [Missions](gdd/missions-structure.md#missions) table). Enemy kill values lowered. Per-level kill overrides removed (THJ). XP split rounds up. |
