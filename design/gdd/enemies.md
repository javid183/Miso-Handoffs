# Enemies

Owner: game designer (THJ approves) · Scope: `all` · Checked against assets: `main` @ `92853a5a9`, 2026-10-16 (ability presets and boss levels read from the live project) · Mirror: Claude Doc "Miso — Game Design", tab Enemies · Up: [Overview](overview.md)

The Corruption's forces are goblins, beasts and two bosses. Each type asks for a different answer: hitting a Black Claw turns its pack on you, poking the Masher draws a counter-attack, and every Worm you kill splits into smaller ones. All enemies use the same turn rules as the family ([Combat rules](combat-rules.md)); difficulty per level comes from tiers (CR-32).

## Roster

| Enemy | Role | HP | Size | Kill XP | Gold on kill | Status |
| --- | --- | --- | --- | --- | --- | --- |
| Dark Claw | Pack melee | 16 | 1 cell | 3 | 0–1 | Built |
| Black Claw | Pack leader | 40 | 1 cell | 5 | 0–2 | Built |
| Archer Goblin | Ranged | 24 | 1 cell | 4 | 0–1 | Built |
| Dark Shaman | Caster, summoner | 50 | 1 cell | 4 | 1–2 | Built |
| Dark Worm | Minor; splits | 28 | 1 cell | 3 | none | Built (Q3) |
| Masher Goblin | Heavy; counter-attacks | 80 | 2 × 2 | 10 | 1–3 | Built |
| Goblin Queen | Boss | 320 (150 in M10) | 1 × 2 | 30 | 5 | Built (Q1) |
| Mountain Deev | Boss; static | 100 | 3 × 2 | 10 | 1–3 | Built |
| Deevoted | The Deev's tentacles | about 1 | 1 cell | 0 | none | Built, unused on `main` (Q5) |

HP is at the Standard tier; Tutorial ×0.6 and Late ×1.2 ([Combat rules](combat-rules.md) CR-32). Every enemy has 2 AP per turn. Kill XP and gold are paid only when an ability lands the killing blow.

Source: `Features/Enemy/<Name>/Prefab(s)/Unit_<Name>.prefab` (`Specs_Health`, `placementSize`, `lethalDamageXpBonus`, `collectableGResources`), `Resources/Factions/EnemyFaction.asset`.

## Special rules

- **EN-1. Pact Leader (Black Claw).** When a Black Claw is attacked, every Dark Claw within 5 cells of it targets the attacker. Black Claws also share grudges with each other within 10 cells. *Built* (Q4)
- **EN-2. Counter-attack (Masher Goblin).** When the Masher survives a hit, it strikes back at the attacker, walking into range first if it has to. It counters every hit, with no limit per turn, and its slam hits both sides. Hovering the Masher while targeting it shows the counter in advance: its path, the cells it will hit and the damage. *Built* (Q2)
- **EN-3. Immovable (Masher Goblin, Mountain Deev).** Can't be pushed, swapped or moved by Mark's Command. The Masher is also Reckless: it turns on whoever attacks it. *Built*
- **EN-4. Split (Dark Worm).** When a Worm dies, it splits into smaller worms: 12 HP (6 damage), then 6 HP (4 damage), then 4 HP (2 damage). *Built* (Q3)
- **EN-5. Summon (Dark Shaman).** The Shaman calls 1 Dark Claw onto a random empty cell within 2 of itself (1 AP, cooldown 3). There is no cap, and summoned Claws stay when the Shaman dies. *Built*
- **EN-6. Goblin Queen.** A boss with a strike, a jump and a telegraphed charge. Her strike deals 7.5 × damage to each family member within 1 cell of the struck cell. She jumps (no damage) to one of four charge spots, marks the longest straight lane from there (wider than one cell; cooldown 4), and on her next turn charges to its far end: every family member next to a cell she passes takes 10 × damage and is pushed 1 cell. She has no phases. In M4, her death triggers the family's Family Super Time ([Missions and structure](missions-structure.md) MI-23). She is fought again in M10 with 150 HP. *Built.* **On `thj/home-test`:** under the Hungry Moon Omen, she gains +1 AP each turn while below 50% HP (D-011).
- **EN-7. Mountain Deev.** A static boss. In its level (M12) it has three actions: a wind-up that marks 10 random cells; poison pools dropped on those cells on its next action, which deal 6 × damage to a family member on the cell each tick and last 3 turns; and, if it was hit since its last turn, a wave that pushes every family member within 9 cells 2 cells away (no damage). The level removes its Summon, which would spawn 3 Deevoted and make the Deev take no damage until any other enemy dies. So in M12 the Deev can be hit from the first turn. The design says its Deevoted must be destroyed before it can be hit. *Built, differs* (Q5)
- **EN-8. Deevoted.** The Deev's tentacles: no abilities, no rewards, ignored by objectives. They would die at 0 HP (about 1) or when their Inactive status is removed, which nothing does. Only the removed Summon spawns them, so they never appear on `main`. *Built, unused* (Q5)

Source: `MemorableAttackMemoryShare` on `Unit_DarkClaw` and `Unit_BlackClaw`; `Features/Enemy/Masher Goblin/Scripts/MasherGoblinFactionRoleHandler.cs`; `DarkWormPassive` on its prefab (script not read); `Core/Entities/Runtime/Boss/BossGoblinQueen.cs`, `BossMountainDeev.cs` and their prefabs; presets in `Resources/UnitSpecific/Enemy/` (`DarkShaman/Summon/`, `GoblinQueen/`, `MountainDeev/`); `Content/Levels/Generic Levels/Medium/MountainDeev/LevelMountainDeev.prefab` (ability list override); `Resources/Tags/GTagSet.asset`.

## How enemies think

- **EN-9.** Enemies are run by a utility AI. Each unit scores its options (attack, move, use an ability) against a plan for the whole faction, then acts. A Taunted unit must go after its taunter. *Built*
- **EN-10.** The player can see who each enemy plans to hit next, and hovering an enemy shows its threat. New enemy types are introduced with a short close-up the first time they appear. *Built* (no introduction text is written yet; Q6)

Source: `tech/mechanics-brief.md` §7 and §8; `Content/Controllers/AIController.prefab`; `EnemyIntroductionController` on `Content/Controllers/PlayerController.prefab`.

## Enemy faction

| Stat | Value |
| --- | --- |
| AP per turn | 2 (cap 5) |
| HP and damage by tier | See [Combat rules](combat-rules.md) CR-32 |
| Other stats (crit, evasion, damage reduction, speed) | ×1 |

The Neutral and Stranger (Toba's duel) factions have a single tier row; their units also get 2 AP (each faction's `actionPointsPerUnit`, 1 and 3, is not read by the code). Source: `Resources/Factions/EnemyFaction.asset`, `NeutralFaction.asset`, `DomAsEnemyFaction.asset`.

## Open questions

1. **Q1.** The Goblin Queen is still titled "Goblin Shaman" in the data, which is also her save key. Rename it in a way that keeps saves working?
2. **Q2.** Should the Masher's counter have a limit per turn? (open since the October balance pass). The prefab also carries two counter components, one with hand-made ids; if both start, it could counter twice.
3. **Q3.** The Worm's split values (12 / 6 / 4 HP) date from before its HP went to 28. Children spawned with odd HP in playtests. Rebalance the split?
4. **Q4.** The glossary says attacking a Black Claw turns *all* Dark Claws; the data limits it to those within 5 cells. Which is intended?
5. **Q5.** The Deev's tentacles and immunity are unused on `main`: M12 removes the Summon that spawns the Deevoted and switches the immunity on. If it ran, the immunity would end when *any* other enemy dies, and nothing removes the tentacles' Inactive status. Restore the Summon and tie the immunity to the tentacles, as designed?
6. **Q6.** Enemy introductions have no text yet. Who writes them (narrative)?
7. **Q7.** Some enemy abilities carry copied titles and text: the Queen's charge and the Deev's pools are titled "Shield Dash" with John's description, the Deev's wave "Taunt". Fix before any screen lists enemy abilities?

## Related

[Combat rules](combat-rules.md) · [Missions and structure](missions-structure.md) (which enemies appear where) · [`combat-balance.md`](../combat-balance.md) · [`reward-balance.md`](../reward-balance.md) · [Glossary](../../glossary.md)
