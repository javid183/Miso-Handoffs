# Progression and economy

Owner: game designer (THJ approves) · Scope: `all` · Checked against assets: `main` @ `92853a5a9`, 2026-10-16 (skill-tree code, item and relic presets read from the live project) · Mirror: Claude Doc "Miso — Game Design", tab Progression and economy · Up: [Overview](overview.md)

The family grows in two lasting ways. Each Bergson earns XP, levels up and spends skill points in their own skill tree; the family shares one wallet of gold and materials that buys family stats and gear upgrades. Inside a mission, run upgrades and Divine Relics add power that is gone when the mission ends. Progression is kept low on purpose: the same enemies appear from M1 to M7, so each main-path mission pays for about one purchase, and replays supply the rest (reasoning in [`reward-balance.md`](../reward-balance.md)).

## Resources

- **PR-1.** Gold, the four materials (Steel, Timber, Fabric, Stone) and Family Skill Points sit in one wallet the family shares. XP and skill points belong to each character. *Built*
- **PR-2.** No resource has a cap. On `main` a new game starts with an empty wallet. *Built*
- **PR-3.** What a mission collects is banked only when the mission ends ([Combat rules](combat-rules.md) CR-34, CR-36). XP counts toward levels at once. *Built*

| Resource | Held by | Earned from | Spent on |
| --- | --- | --- | --- |
| Gold | Family | Mission completion, enemy kills, material picks (M8–M14, MX only) | Family stats, gear upgrades |
| Steel, Timber, Fabric, Stone | Family | Material picks on mission completion | Gear upgrades |
| XP | Each character | Kills, mission completion | Skill points |
| Skill Point (SP) | Each character | XP thresholds | Skill-tree nodes, unlocks |
| Family Skill Point (FSP) | Family | A character's 2nd, 3rd and 5th SP spent | Family nodes, family unlocks |

The data titles FSP "Bergson Skill Point"; the glossary name is Family Skill Point. Source: `Resources/GResources/GResourceSet.asset` (`aggregated` 1 = family wallet), `Core/Units/Runtime/Factions/FactionTracker.cs`.

## Experience and levels

- **PR-4.** XP comes from kills and from completing a mission. A kill pays the enemy's kill XP only when an ability lands the killing blow ([Enemies](enemies.md#roster)). *Built*
- **PR-5.** XP is split evenly, rounded up, among family members: kill XP among everyone who started the level (members who fell included), completion XP among those in the final level. The killer gets no extra share, and members who stayed out of the mission get nothing. *Built* (Q3)
- **PR-6.** Each XP threshold reached gives 1 SP. The first threshold is 0, so a character's first XP of any amount gives 1 SP. There are 10 thresholds, so 10 SP is the cap. *Built*
- **PR-7.** A character's level is the number of SP spent in their tree. Nodes unlock at 0, 0, 2, 2, 3 and 5 SP spent; the trees are on the character sheets ([Characters](characters/README.md)). Each tree costs 8 SP, which leaves 2 SP spare at the cap. *Built, differs* (tier levels, Q2)

| SP earned | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| At total XP | 0 | 75 | 200 | 375 | 600 | 875 | 1200 | 1575 | 2000 | 2475 |

Source: `Resources/Game Data.asset` (`xpLevelThresholds`), `FactionTracker.cs` (`CheckLevelUps`, `CollectResourceSplit`), `Core/Managers/CombatLevelRunHandler.cs` (`AwardResources`, `AwardMissionCompletionResources`).

## Family Skill Points and family level

- **PR-8.** A character's tree also earns the family 1 FSP each time the SP spent in it reaches 2, 3 and 5 (its unlock levels): 3 per character, 15 in all, which is exactly what the family nodes cost. Only purchases in the skill-tree panel count. FSP buy the family nodes, which sit on the characters' trees and upgrade Duos and Synergies ([Family systems](family-systems.md)). *Built, differs* (the design said a character's first 3 SP; Q1)
- **PR-9.** There is no family level. A hidden family level fed by Bond level-ups was proposed in the Home readability pass ([`m9-readability.md`](../m9-readability.md)). *Open* (Q1)
- **PR-10.** **On `thj/home-test`:** the family earns 1 FSP after its second side mission and spends it on the Picnic ([Home](home.md)). *Demo*

Source: `Core/UI/Runtime/Home/UpgradePanel/AbilityUpgradePanelUI.cs` (FSP grants), `SkillTree.cs` (`GetNodeState`), `FactionTracker.cs` (`UnitLevels`), `Resources/Unlockables/UnlockableSet.asset` (FSP costs); design rules in `design/player-skill-trees.md`.

## Family stats

- **PR-11.** Eleven family stats raise every Bergson at once. Each has 3 levels, bought in order with Gold from the wallet; level 0 is free. *Built*
- **PR-12.** On `main` they are sold at three hub stations: the Kitchen, the Training Ground and the Family Room. *Built*
- **PR-13.** **On `thj/home-test`:** the gold panels are off. Stats rise through Yard Lessons and Home Upgrades instead ([Home](home.md)). *Demo*

| Stat | Effect | Level 1 / 2 / 3 | Gold | Station |
| --- | --- | --- | --- | --- |
| Health (`Stat_HP`) | Max HP | ×1.15 / ×1.25 / ×1.4 | 20 / 30 / 50 | Kitchen |
| HP gain (`Stat_HPG`) | HP regained at each new level of a mission, share of max | 10% / 20% / 30% | 20 / 30 / 50 | Kitchen |
| Potion potency (`Stat_HPP`) | Health Potion healing (10 × this: 10 → 25 HP) | ×1.5 / ×2 / ×2.5 | 10 / 15 / 40 | Kitchen |
| Damage (`Stat_DMG`) | Damage dealt | ×1.1 / ×1.2 / ×1.3 | 20 / 30 / 50 | Training Ground |
| Damage reduction (`Stat_DR`) | Damage taken | ×0.9 / ×0.85 / ×0.8 | 15 / 20 / 40 | Training Ground |
| Evasion (`Stat_EVA`) | Chance to cancel a hit | +5% / +9% / +13% | 15 / 20 / 40 | Training Ground |
| Critical chance (`Stat_CRC`) | Chance of a ×1.5 hit | +7.5% / +11% / +15% | 15 / 20 / 40 | Training Ground |
| Family Point (`Stat_FP`) | Added to every roster member's FP value, so the FTP maximum (full family 14 → 19 → 20 → 24; level 2 adds little because of rounding) | +1 / +1.5 / +2 | 20 / 30 / 50 | Family Room |
| FP gain (`Stat_FPG`) | FTP regained at each new level, share of max | 18% / 27% / 35% | 15 / 20 / 40 | Family Room |
| Trinket potency (`Stat_FPP`) | Nothing: no code reads it; the Family Trinket always gives +5 FTP (Q10) | ×1.2 / ×1.35 / ×1.5 | 10 / 15 / 40 | Family Room |
| Wisdom (`Stat_WIS`) | Healing done | ×1.2 / ×1.3 / ×1.4 | 15 / 20 / 40 | All three |

All eleven at level 3 cost 905 Gold. Source: `Resources/Factions/BergsonsFaction.asset` (`statAttributes`), `Features/Home - Imported/___Khashayar/HomeManager.cs`.

## Gear

- **PR-14.** Gear sits in sockets: head, chest, legs, ring, left hand, right hand, necklace. A character wears only items for sockets they have, one item per socket. Most items belong to one character; shared items fit anyone. *Built*
- **PR-15.** Every item exists once: equipping it on one character takes it off another. *Built*
- **PR-16.** Every item has 3 upgrade levels, paid in Gold and materials from the wallet. The level belongs to the item, not to whoever wears it. Gear bonuses are flat and added after every multiplier ([Combat rules](combat-rules.md) CR-19), so the Vitality Brooch adds exactly its listed HP. *Built*
- **PR-17.** Each character starts with their own items equipped; the shared items start owned but unequipped. *Built* (Mark: [Mark](characters/mark.md#open-questions) Q3)
- **PR-18.** **On `thj/home-test`:** only the five weapons can be upgraded, as Workshop orders that Ben finishes in 2 Dawns ([Home](home.md)). *Demo*

Each character's own gear is on their sheet. The shared items:

| Item | Socket | Stat | Base | Level 1 | Level 2 | Level 3 |
| --- | --- | --- | --- | --- | --- | --- |
| Vitality Brooch | Head | Max HP | +3 | +5 (10 Gold, 1 Fabric, 1 Steel) | +10 (20 Gold, 3 Fabric, 3 Steel) | +15 (40 Gold, 3 Fabric, 3 Steel, 3 Stone) |
| Shin Armor | Chest | Evasion | 0.03 | 0.05 (10 Gold, 1 Fabric, 1 Timber) | 0.075 (20 Gold, 3 Fabric, 3 Timber) | 0.1 (40 Gold, 5 Fabric, 5 Timber) |

All 12 items at level 3 cost 845 Gold, 56 Fabric, 34 Steel, 22 Timber and 15 Stone. Source: `Core/Data/Runtime/EquipmentSO.cs`, `EquipmentManager.cs`, `Resources/Unit Equipments/*/*.asset`.

## Unlocks

- **PR-19.** Some nodes unlock a named effect, such as "Fire Embers apply Burn". It is bought once with SP or FSP and kept for good. A run upgrade can grant the same unlock for one mission. *Built*

| Unlock | Cost | Bought on | Same effect as a run upgrade |
| --- | --- | --- | --- |
| Tempest Bloom | 1 FSP | Lucy's tree (family node) | Tempest Bloom |
| Catch & Return | 1 FSP | Mark's tree (family node) | — |
| Move as One | 1 SP | Linda's tree | — |
| Sundering Strikes | 1 SP | John's tree | Sundering Strikes |
| Diminishing Blow | 1 SP | Linda's tree | Diminishing Blow |
| Lingering Embers | 1 SP | Lucy's tree | Lingering Embers |
| Sapping Order | 1 SP | Mark's tree | Sapping Order |
| Stunning Vault | 1 SP | Mark's tree | Vault Stun |
| Cyclone Weak | 1 SP | No node | Howling Gale |
| `JohnResolve` | 1 SP | Not used anywhere | — |

Source: `Resources/Unlockables/UnlockableSet.asset`; references on `Unit_*.prefab` (`skillTree`, passive components) and `Resources/RunUpgrades/*/RU_*.asset`.

## Mission rewards

- **PR-20.** Completing a mission pays its XP and Gold, plus a material pick: a set number of different entries drawn at random from the mission's list, each rolled in its range. Amounts per mission are in [Missions and structure](missions-structure.md#missions). *Built*
- **PR-21.** Winning a level that isn't the last pays only for the kills made in it. *Built*
- **PR-22.** Losing a mission drops the gold collected in it and keeps the XP. The family then gets 20% of the mission's XP and 50% of its Gold, unless the loss came on the first level ([Combat rules](combat-rules.md) CR-34). In the opening mission, before its first completion, a loss restarts the level and pays nothing (CR-35). *Built*
- **PR-23.** Completed missions stay open and pay full rewards every time. There is no first-clear bonus. *Built*
- **PR-24.** Gold comes only from completion and kills; material picks hold materials only. *Built, differs:* M8–M14 and MX still list Gold in their picks, where it displaces materials (not rebalanced yet).
- **PR-25.** **On `thj/home-test`:** the game starts with 100 Gold, 1 Steel and 1 Timber. Drops are paid per cleared level and kept after a loss; a lost sortie loses only its completion reward. Side missions pay 20 XP (30 for Drowned Shrine and Deev Burrow, 60 for the Warren) ([Home](home.md)). *Demo*

| Supply and sinks (derived) | Gold |
| --- | --- |
| Completion Gold, main path M1–M7 (all 8 missions once) | 90 |
| All family stats to level 3 | 905 |
| All gear to level 3 | 845, plus 127 materials |

Kill gold per enemy is in [Enemies](enemies.md#roster). Source: `Core/Levels/Runtime/Mission.cs` (`GetCompletionRewards`, `GetFailureRewards`), `CombatLevelRunHandler.cs` (`AwardMissionFailureResources`), `Core/Managers/GameHandler.cs` (`IsMissionUnlocked`).

## Run upgrades

- **PR-26.** A run upgrade is a boost that lasts one mission. All run upgrades are cleared when a mission starts and when it ends. *Built*
- **PR-27.** The Run Upgrade room's altar lays out up to 3 run upgrades, drawn at random with equal odds. The player takes one for free; the others disappear. The pool is every run upgrade, with none excluded. *Built*
- **PR-28.** An upgrade is offered only when it can do something: its owner is in the squad (both partners for a Duo's), its ability is available, the family doesn't already have it (an unlock already bought counts), and its ability can still level up. Any member can pick an upgrade up; it applies to its owner. *Built*
- **PR-29.** There are three kinds: runes (raise an ability's level or add to a stat), new abilities or unlocks, and passives. A fourth kind, relic, exists in code with no upgrades of that kind. *Built*

| For | Run upgrades (19) |
| --- | --- |
| Whole family | Critical Bergsons: every Bergson +20% critical chance for the mission |
| John | Extensive Dash, Tempered Blade, Sundering Strikes ([John](characters/john.md#run-upgrades)) |
| Linda | Power-Piercing Arrows, Louder Crescendo, Echoing Retreat, Diminishing Blow ([Linda](characters/linda.md#run-upgrades)) |
| Lucy | Stoked Embers, Lingering Embers, Howling Gale, Tempest Bloom (needs Linda in the squad) ([Lucy](characters/lucy.md#run-upgrades)) |
| Linda and Lucy | Sisters' Bond: Linda–Lucy Duo damage +1 level |
| Mark | Iron Knuckles, Long Vault, Vault Stun, Sapping Order, Always Ready ([Mark](characters/mark.md#run-upgrades); Q7) |
| Toba | Guardian's Reach ([Toba](characters/toba.md#run-upgrades)) |

Source: `Core/Systems/RunUpgrades/Runtime/RunUpgradeSO.cs`, `RunUpgradeTracker.cs` (`CanGrant`), `Core/Entities/Runtime/RunUpgradeAltar.cs`, `Resources/RunUpgrades/*/RU_*.asset`.

## Divine Relics

- **PR-30.** A Divine Relic is an item lying in a level; walking onto it takes it. Every family member gets the relic's button, and its 3 uses are shared. Picking up the same relic again adds uses. *Built*
- **PR-31.** A relic lasts the mission. Restarting a level loses a relic picked up in it. *Built*
- **PR-32.** Two relics exist. **Heavenly Sword:** drops a sword on a cell within 5; every enemy in the 3 × 3 around it takes 10 × damage (cooldown 2). It lies in the Divine Relic rooms of M6 and M4 and in the first level of "No More Waiting". **Black Despair:** pulls enemies within 2 cells of a target cell 2 cells inward (not Immovable ones), no damage; no level places it, so it can't be found on `main`. Using a relic is free but needs 1 AP left. *Built* (Q6)

Source: `Core/Entities/Runtime/DivineRelics/DivineRelicPickUp.cs`, `Features/Player/Shared/DivineRelics/DivineRelicPickUp.prefab` (`numberOfUses` 3), `FactionTracker.cs` (`AddUsableItem`), relic presets `DR_Ability_HeavenlySword.asset` and `DR_Ability_BlackDespair.asset` and their pickups.

## The hub on `main`

- **PR-33.** Between missions, the hub offers the three stat stations (PR-12), the skill trees, the Workshop (gear) and the world map. *Built*
- **PR-34.** Stations open as the campaign advances: nothing after M1; the skill trees after the first of M2 and M5, the Kitchen after the second; the Workshop after the first M3, the Training Ground and the Family Room after the second. *Built*

Source: `Features/Home - Imported/___Khashayar/HomeManager.cs`; `Home - Scene.unity` (the three `FactionStatUpgradePanelUI` stat lists; `HomeInteractables.UnlockAfterMissions` on the Grandma Table, the Equipments Cabinet and the station objects).

## Deferred and dropped

| Item | State | Where decided | Notes |
| --- | --- | --- | --- |
| Rune overlaps: a bought node removes its run upgrade from the altar | Deferred | [`player-skill-trees.md`](../player-skill-trees.md) | Deferred by THJ, but already built for unlocks and level-ups. Runes built from stat modifiers (Extensive Dash, Power-Piercing Arrows, Critical Bergsons) are never removed |
| Relic as a run-upgrade kind | Code only; no assets | — | |
| Family Time and Family Lookout family nodes | Dropped | [`player-skill-trees.md`](../player-skill-trees.md) | `main` ran ATB then |
| Material-only picks and new rewards for M8–M14 and MX | Pending | [`reward-balance.md`](../reward-balance.md) §5 | |

## Branch differences

- **On `main`:** as described above.
- **On `thj/home-test`:** a starting wallet, drops kept per level, Yard Lessons and Home Upgrades in place of the stat panels, Workshop orders for weapons only, food, Bond, and 1 FSP for the Picnic. The Rest Room heals 10% of max HP. Rules and numbers: [Demo Spec](../demo-spec.md).

## Open questions

1. **Q1.** How should FSP and a family level work? As built, a character's tree earns 1 FSP at 2, 3 and 5 SP spent (the design said the first 3 SP). Keep that? And should the hidden family level fed by Bond be built?
2. **Q2.** Skill-tree tiers: the data unlocks nodes at 0, 0, 2, 2, 3 and 5 SP spent; [`player-skill-trees.md`](../player-skill-trees.md) says one tier per SP spent (0, 1, 2, 3). Which is intended?
3. **Q3.** Kill XP goes to the whole squad, fallen members included, and completion XP only to the final level's squad. Characters a level places themselves share it too: Linda in M1, Toba in every level of M4 after his duel, before he joins. Intended?
4. **Q4.** Restarting a level keeps the XP and gold collected in the failed attempt. Close it?
5. **Q5.** Shin Armor is authored in the chest socket, where Lucy's Robe and Mark's Tunic also go. Legs intended?
6. **Q6.** Divine Relics: keep the walk-on pickup (3 shared uses, no choice) or move relics to run upgrades (the relic kind)? Black Despair is in no level; place it or cut it?
7. **Q7.** Always Ready only works with ATB but is still offered on `main`. Remove it from the altar?
8. **Q8.** The unlock `JohnResolve` is used nowhere, and Cyclone Weak (Howling Gale) exists only as a run upgrade. Keep both?
9. **Q9.** Answered from the code: flat gear bonuses are added after every multiplier, so the Vitality Brooch adds exactly +3 to +15 max HP and the family Health stat doesn't scale it. Close, or should gear scale?
10. **Q10.** The Trinket potency stat (`Stat_FPP`) is sold for 10 / 15 / 40 Gold, but nothing reads it: the Family Trinket always gives +5 FTP. Wire it up, or remove it from the Family Room?

## Related

[`reward-balance.md`](../reward-balance.md) · [`player-skill-trees.md`](../player-skill-trees.md) · [Characters](characters/README.md) · [Missions and structure](missions-structure.md) · [Home](home.md) · [Glossary](../../glossary.md)
