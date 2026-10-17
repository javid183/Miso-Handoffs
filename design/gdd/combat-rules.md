# Combat rules

Owner: game designer (THJ approves) · Scope: `all` · Checked against assets: `main` @ `92853a5a9`, 2026-10-16 (ability presets and core scripts read from the live project) · Mirror: Claude Doc "Miso — Game Design", tab Combat rules · Up: [Overview](overview.md)

A level is a grid fight played in rounds: the family takes its turn, then each other faction takes its own. Every unit acts with its own AP. The family shares one pool of FTP, which pays for Duos. Reactions (Family Roles, QTEs) happen on both turns, so the player is never just watching. Lines marked "(to check in play)" are read from the data but not yet confirmed in a playtest.

## Turns and rounds

- **CR-1.** Factions take turns in a fixed order: the family (Bergsons) first, then enemies, then neutral factions. A level can set its own order. A round ends when the order comes back to the first faction. *Built*
- **CR-2.** At the start of a faction's turn, each of its units gets its AP back. A unit tagged Inactive (family) or Stunned (enemies) skips the turn. Then cooldowns, stat effects and status lifetimes tick. *Built*
- **CR-3.** The family's turn ends when the player ends it or when no unit has AP left. Enemies act one unit at a time, then end their turn. *Built*
- **CR-4.** Objectives are checked at the start of each turn, after every ability and right after deaths. A win or loss ends the level at once. *Built*

Source: `Core/Managers/CombatLevelRunHandler.cs`, `Core/Interactions/Runtime/FactionControllerBase.cs`, `FactionPhaseState.cs`, `Resources/Factions/*.asset` (turn order).

## Action points (AP)

- **CR-5.** AP is fixed and per unit (D-037): every unit has its own AP for the turn. Family members have 2 AP; enemies have 2. *Built*
- **CR-6.** Each action has one of three costs: free (items, Family Roles, Pass-by), 1 AP (every family move and ability) or all the AP left, which ends the unit's turn (every enemy basic attack). Any action, even a free one, needs at least 1 AP left. No hero ability ends the turn by itself. *Built*
- **CR-7.** Clicking an enemy out of reach walks into range, then attacks, if the unit has AP for both. *Built*
- **CR-8.** AP left at the end of the family's turn is lost. (In code it still turns into ATB steps that nothing spends; see Q3.) *Built*
- **CR-9.** **On `thj/home-test`:** the Quickberry Tart meal gives +1 AP on turn 1 of the sortie ([Home](home.md)). *Demo*

| Faction | AP per turn | AP cap |
| --- | --- | --- |
| Bergsons | 2 (`Stat_AP`) | 2 (`StatUB_AP`) |
| Enemy | 2 | 5 |

A global cap of 3 also applies: an AP gain that would take a unit above 3 is refused whole, not trimmed. Source: `Resources/Factions/BergsonsFaction.asset`, `EnemyFaction.asset`, `Features/_Common/Prefabs/UnitBase.prefab` (`Specs_AP`), `Resources/GlobalSettings.asset` (`aPConsumptionMode` PerUnit, `aPCap` 3), `Core/Systems/AbilitySystem/Points/Runtime/ActionPoints.cs` (`APConsumptionType`, `CanConsume`, `Produce`).

## Family Time Points (FTP)

- **CR-10.** FTP is one pool the family shares. It is created when a mission starts, from the mission's roster (not from who a level deploys), and it starts full. Its maximum is the sum of each roster member's FP value: their base (table below) plus the family's `Stat_FP` level, each rounded (halves to even). When a member dies, the maximum stays, but until the next level the pool is capped at the FP of the roster members still alive in that level (so in a level that doesn't place the whole roster, the first death also drops the absent members' share); points above the new cap are lost. *Built* (Q2, Q9)
- **CR-11.** FTP fills during the fight: +1 for each unit in a Pass-by (+2 when two of John, Linda, Lucy and Mark pass each other, +1 when Toba is one of the pair), +1 when John uses Shield Up, Linda Harmonic Slam, Lucy Blink or Toba Provoking Presence, and +5 from the Family Trinket. Some levels also add 3 or 5 FTP when they load ([Missions and structure](missions-structure.md#missions)). It does not refill each turn. *Built (Pass-by and Trinket to check in play, Q7)*
- **CR-12.** Between levels of the same mission, FTP carries over and grows by `Stat_FPG` × the maximum (0 until upgraded). The first level gets no growth. Restarting the mission's first level refills the pool; restarting a later level keeps the FTP of the failed attempt. It is cleared when the mission ends. *Built*
- **CR-13.** FTP pays for Duos (2 each; the check before use tests only 1 per partner). Today it also pays for Family Roles (1 each, free by design) and Mark's Continuous Attack (1, then +1 per use in the same turn). See [Family systems](family-systems.md). *Built, differs*
- **CR-14.** Family Super Time: every living member with a Family Role runs a special action at once. It costs no FTP. On `main` the player can't trigger it: the only ability that does (1 AP, needs a full pool) is carried by the enemy Toba of the duel, and the game fires it once when the Goblin Queen dies in M4. *Built, differs* (Q4)

| Member | FP value (`Specs_FP` base; + family `Stat_FP` level) |
| --- | --- |
| John | 5 |
| Linda | 2 |
| Lucy | 3 |
| Mark | 3 |
| Toba | 1 |

The full family's maximum is 14, 19, 20 and 24 at `Stat_FP` levels 0 to 3 (level 2 gains little because of the rounding). The FP-fill effect assets (`*_FC_FPFill`) are used by no ability; the fills in CR-11 come from each ability's own `FPFillAmountV`.

Source: `Core/Units/Runtime/Factions/FactionTracker.cs` (`InitializePoints`, `OnLevelLoad`), `FamilyTimePoints.cs`, `Core/Units/Runtime/GUnit.cs` (`ProduceFTP`, `CheckIfFactionSuperTimeAvailable`), `Core/Interactions/Runtime/PlayerController.cs` (`UpdateCap`, `ActivateFactionSuperTime`), `RuntimeAbility.cs` (`FPFillAmountV`), `Unit_*.prefab` (`Specs_FP`), `Features/Player/Shared/Abilities/TagFPFill/Bergson_PassBy_Ability_PointsFill.asset`, `Features/Player/Shared/Items/`.

## Grid and movement

- **CR-15.** The board is a square grid. "Adjacent" counts steps in four directions; "radial" counts in eight (diagonals cost one step). *Built*
- **CR-16.** Units path around obstacles and other factions' units. Large units can take several cells. Hazards can raise a cell's move cost; other terrain costs are not built yet. *Built*
- **CR-17.** The player can cycle up to 8 alternative move paths, including paths through allies that trigger Pass-by. *Built*
- **CR-18.** Pushes and pulls move units along the grid. Immovable units can't be pushed, pulled, swapped or moved by Mark's Command, except by John's Family Super Time pull, which ignores it, and probably Mark's Vault push (to check in play). *Built* (Q8)

Source: `Core/Systems/GridSystem/Runtime/GridCell.cs` (distances, `GetCellCost`), `GridActions.cs` (`FindAlternativePathsTo`), the push effects in `Resources/UnitSpecific/Player/**`.

## Attacks and damage

- **CR-19.** Damage is the effect's base factor × the attacker's `Stat_DMG`, capped at 9999. `Stat_DMG` is built in this order: the family stat (×1 to ×1.3), the unit's own layer (where Weak's ×0.6 sits), the family's shared skill-tree stats, gear as a flat bonus added after those multipliers, then the ability's own level (×). Run upgrades raise a level inside these layers. Mark's unit layer comes after his gear, so Weak also cuts his gear bonus. *Built*
- **CR-20.** Health is a whole number; each hit is rounded (halves to even). The hover preview uses the same rounding, so it shows exact damage and kills. *Built*
- **CR-21.** Crit and evasion are rolled once per target per hit. A critical hit (the attacker's `Stat_CRC` chance) deals ×1.5. Then evasion (the target's `Stat_EVA` chance) cancels the HP loss, but not the hit's pushes or statuses. Otherwise damage taken is × the target's `Stat_DR`: 1 is full damage, 0.8 is 20% less. Burn ticks and push damage can also be evaded and reduced; push damage can crit, Burn can't. The damage preview leaves crit out. *Built*
- **CR-22.** Some area attacks hit both sides (the Masher's slam). A kill caused by something other than an ability (burn, a push, friendly fire) gives no XP or gold. *Built*

Source: `Core/Systems/StatsResourcesSystem/Runtime/StatEvaluation.cs` (`StatResolver.Resolve`), `StatAttributes/StatBackedValue.cs`, `AAttributeModifier.cs`, `RuntimeAAttributeBase.cs` (`ApplyModifiers`), `Features/_Common/Prefabs/UnitBase.prefab` (health modifiers, stat profiles).

## Health, death and revenge

- **CR-23.** A unit at 0 HP dies and leaves the board. *Built*
- **CR-24.** HP carries over between levels of a mission. At the next level, a family member starts at their saved HP, at least 20% of max, plus `Stat_HPG` × max (0 until upgraded). The floor also brings back members who fell in a won level, at 20%. *Built*
- **CR-25.** When a family member dies, each other living member takes Revenge after a short beat: for 2 turns, ×1.5 damage, +20% crit chance, +1 AP and +1 to the AP cap, plus a ready basic attack (which adds nothing on `main`: basic attacks have no cooldown). The values are the same for John, Linda, Lucy and Mark; Toba neither gives nor takes Revenge. *Built (Q5)*
- **CR-26.** **On `thj/home-test`:** the first member downed in a sortie comes home Wounded ([Home](home.md)). *Demo*

Source: `Core/Units/Runtime/GUnit.cs`, `Core/Units/Runtime/Factions/FactionTracker.cs`, `Core/Interactions/Runtime/PlayerController.cs` (revenge), `Resources/GlobalSettings.asset` (`persistHealthsThroughMission` on).

## Statuses

| Status | Shown as | What it does | Status |
| --- | --- | --- | --- |
| Vulnerable | Vulnerable | Takes 20% more damage (`Stat_DR` ×1.2) for 2 turns; reapplying refreshes, doesn't stack | Built |
| Weak | Weak | Deals 40% less damage (`Stat_DMG` ×0.6) for 2 turns | Built |
| Burnt | Burnt | Loses 3 HP at the start of its turn, twice (6 in all); not scaled by damage, can't crit | Built |
| Crippled | Crippled | Can't walk for 1 turn; takes 4 × the mover's damage for each cell it is pushed or pulled. Applied by Linda's Harmonic Slam | Built |
| Stunned | Stunned | Skips its next turn (enemies). Applied by Mark's Vault with Stunning Vault | Built (Q6) |
| Taunted | Taunted | Must target the taunter, through its next turn | Built (no ability read so far applies it; to check) |
| Sheltered | Sheltered by John | Lucy next to John: her Fire Embers gain one ember (Papa's Shelter) | Built |
| Shield Up | (hidden) | John's Shield Up is active | Built |
| Blood Debt | Blood Debt | Marked by John (the last enemy to hurt the family) | Built |
| Reckless | Reckless | Masher Goblin: when an ability hurts it and it survives, it at once walks to the attacker and strikes | Built |
| Immovable | Immovable | Can't be pushed or commanded | Built |
| Pact Leader | Pact Leader | Black Claw: attacking it turns the pack on the attacker | Built |
| Inactive | (hidden) | Skips its turn; ignored by objectives and by Pass-by | Built |

Durations count the affected unit's own turns. Source: `Resources/Tags/GTagSet.asset`; the status effects in the ability presets (`John_Ability_Attack_Sword_Effect_Vulnerable*`, `*_Effect_Weak*`, `Lucy_Ability_PrimaryAttack_Effect_Burn*`, `Linda_Ability_HarmonicSlam_CompundEffect`, `Mark_Ability_Attack_Vault_Effect_Stun`); timing in `AAttributeSet.cs` and `GameEntity.PhaseTick`.

## QTEs

- **CR-27.** A QTE is a timed prompt. There are four types: Press (any press in time), Mash (fill a meter that drains), Time window (press inside the marked band; a press outside fails) and Time-window mash. *Built*
- **CR-28.** QTEs appear on both turns: Family Roles (press, 1 s), Duo partners (mash for 2 s, or a time window of 2 × 1 s), Command Shield Dash (press) and Continuous Attack (press). *Built*
- **CR-29.** Only one QTE is up at a time. The click used for a QTE never also clicks the board. *Built*

Source: `Core/Interactions/Runtime/QTEProfile.cs`, `QTEBehavior.cs`, `QuickTimeEventHandler.cs`, `Content/Controllers/PlayerController.prefab`.

## Items

- **CR-30.** Each mission gives the family a shared stock of two items that any member can use on themselves: the Health Potion (heals 10 × `Stat_HPP`, so 10 to 25 HP; not at full HP) and the Family Trinket (+5 FTP; not when FTP is full). Both are free but need 1 AP left. Counts are set per mission ([Missions and structure](missions-structure.md)). *Built* (the trinket's potency stat does nothing: [Progression and economy](progression-economy.md) Q10)
- **CR-31.** Restarting a level gives back the items used in it. *Built*

Source: `Features/Player/Shared/Items/HealthPotion/Bergsons_Ability_HealthPotion.asset`, `Items/FPPotion/Bergsons_Ability_FPPotion.asset`, `Core/Units/Runtime/Factions/FactionTracker.cs` (`ItemTracker`), `Content/Levels/M*.asset` (`initialItemsAvailability`).

## Enemy tiers

- **CR-32.** A level can set an enemy tier. At level start, every hostile faction's `Stat_HP` and `Stat_DMG` move up that many levels on the faction's rows. The family is never affected. *Built*

| Tier | Name | Enemy HP | Enemy damage |
| --- | --- | --- | --- |
| 0 | Standard | ×1 | ×1 |
| 1 | Early | ×1 | ×0.75 |
| 2 | Tutorial | ×0.6 | ×0.5 |
| 3 | Late | ×1.2 | ×1 |

Source: `Core/Managers/CombatLevelRunHandler.cs` (`ApplyEnemyTier`), `Resources/Factions/EnemyFaction.asset`. Which levels use which tier: [Missions and structure](missions-structure.md).

## Winning, losing and leaving

- **CR-33.** Winning a level that isn't the last loads the next one; when the route offers a choice, the mission map opens first ([Missions and structure](missions-structure.md) MI-11). Winning the last level completes the mission and pays its rewards. *Built*
- **CR-34.** Losing ends the mission. The family keeps the XP and skill points earned; gold and materials collected are lost. The family then gets a share of the mission's rewards, except after a loss on its first level ([Progression and economy](progression-economy.md) PR-22). *Built*
- **CR-35.** In the opening mission, before it is first completed, a loss restarts the level instead. *Built*
- **CR-36.** Leaving a mission banks the resources collected and clears FTP, saved HP and run upgrades. *Built*

Source: `Core/Managers/CombatLevelRunHandler.cs`, `Core/Managers/GameHandler.cs`, `Core/Units/Runtime/Factions/FactionTracker.cs`.

## Deferred and dropped

| Item | State | Decision |
| --- | --- | --- |
| Bergson Time (Reactive Interrupt, key L) | Deferred; works only with ATB, so it is off with FTP | D-038 |
| ATB gauge | Dropped as the direction. The gauge still fills during enemy turns and takes leftover AP, but nothing spends it with FTP | D-036 |
| Shared AP | Dropped; half-built code remains | D-037 |
| Action reversion (undo an action for FTP) | Off (`enableActionReversion` 0, cost 0) | — |
| Several AP for one long move (distance ÷ range, rounded up) | Built; no unit turns it on (`allowMultiActivation`) | — |

## Branch differences

- **On `main`:** FTP since `92853a5a9` (2026-10-16); before that, ATB.
- **On `thj/home-test`:** FTP. Home adds per-sortie effects at level start: the send-off meal, Omens, Wounded members at 50% HP in the dungeon, and a "From Home" banner ([Home](home.md)).

## Open questions

1. **Q1.** FTP's on-screen name: FTP, FP, Family Points (the stat descriptions), Family Time Points (the code) or Family Passive Points (the glossary)?
2. **Q2.** How should the FTP maximum be set? Today it is the sum of the mission roster's FP values (John 5, Linda 2, Lucy 3, Mark 3, Toba 1, plus the family stat), and the pool starts full. The Demo Spec describes 3 × (heroes − 1) on `thj/home-test`.
3. **Q3.** Leftover AP is lost at the end of the turn. Should it do something with FTP (for example, fill FTP)?
4. **Q4.** Family Super Time: on `main` only the Goblin Queen's death triggers it, and it costs nothing. Keep it as a feature? What should it cost, and how should the player trigger it?
5. **Q5.** Revenge on an ally's death: a designed family mechanic, or legacy? Where should it live in this document?
6. **Q6.** Family members tagged Stunned are not skipped (only Inactive skips their turn). Intended?
7. **Q7.** Pass-by and the Family Trinket add FTP through a message that passes a decimal number to a whole-number function. Unity may reject such a call, in which case both add nothing. Check the Console in play ("Failed to call function ProduceFTP").
8. **Q8.** John's Family Super Time pull, and probably Mark's Vault push, move Immovable units (the Masher, the Deev). Fix?
9. **Q9.** After a death, FTP is capped below its maximum until the next level, so the pool can't be full and Family Super Time can't fire for the rest of that level. Intended?

## Related

- Decisions: D-034 to D-038
- Detail: [`combat-balance.md`](../combat-balance.md), [`tech/mechanics-brief.md`](../../tech/mechanics-brief.md), [`tech/combat-architecture.md`](../../tech/combat-architecture.md) (dev cheats)
- [Family systems](family-systems.md) · [Enemies](enemies.md) · [Progression and economy](progression-economy.md)
