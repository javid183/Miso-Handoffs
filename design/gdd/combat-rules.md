# Combat rules

Owner: game designer (THJ approves) · Scope: `all` · Checked against assets: `main` @ `92853a5a9`, 2026-10-16 (ability presets and core scripts read from the live project); [Grid previews and the Shift view](#grid-previews-and-the-shift-view) read from `thj/preview-improvements` @ `f5d263743`, 2026-10-20, now merged into `main`; [Combat feedback](#combat-feedback) from `thj/quick-wins` @ `403de3bf8`, 2026-10-23 (build reports, `pace-timings.md` and the damage-preview rules read) · Mirror: Claude Doc "Miso — Game Design", tab Combat rules · Up: [Overview](overview.md)

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
- **CR-11.** FTP fills during the fight: +1 for each unit in a Pass-by (+2 when two of John, Linda, Lucy and Mark pass each other, +1 when Toba is one of the pair), +1 when John uses Shield Up, Linda Harmonic Slam, Lucy Blink or Toba Provoking Presence, and +5 from the Family Trinket. Some levels also add 3 or 5 FTP when they load ([Missions and structure](missions-structure.md#missions)). It does not refill each turn. *Built* (Pass-by and Trinket to check in play, Q7)
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

## Grid previews and the Shift view

The rule for previews: what a preview promises, the real action does. Role zones, follow zones, cover markers and John's tether are in [Family systems](family-systems.md#role-zones-on-the-grid). These rules are on `main` since the merge of `thj/preview-improvements` (2026-10-20).

- **CR-37.** Every preview of where an attack reaches uses the real attack's rules: its shape, straight lines only when the ability has them, the unit's whole footprint, and ranged reach across missing tiles (Linda's arrow crosses a gap). That covers the ghost's sword icons (basic-attack reach from the ghost tile), the approach preview (attack range from the tile the unit would walk to before attacking, CR-7), the Shift view and the enemy threat arcs. Abilities that preview an affected area keep that preview. *Built*
- **CR-38.** On a multi-tile unit, every tile in reach gets its own sword icon, drawn above the unit's sprite; hovering any of its tiles as a target marks all of them once. The move frame still wraps the whole footprint (D-088, D-089). *Built*
- **CR-39.** Enemy threat arcs: while the player previews a move, a curved line runs from each enemy that could attack the ghost tile after moving, with any Attack ability, without area splash. Like the danger zone (CR-43), the arcs count any Attack ability ready on the enemy's next turn, so an ability with 1 turn of cooldown left draws an arc (D-085, D-090). *Built*
- **CR-40.** Grid hover stops while the pointer is over the on-screen HUD, and entering the HUD clears the hovered tile, so a ghost, follow zone or Shift preview never fires under a panel (D-078). Unit info panels over the board don't block hover. Clicks are unchanged. *Built*
- **CR-41.** Holding Shift shows details: info panels, every Bergson's role zone, and for the hovered unit a move and attack preview on its own layer, softer than and under the real highlights, so it never erases them (D-064, D-071). The preview is recomputed on each Shift press and hover, and isn't shown while the player is picking an ability target. *Built*
- **CR-42.** Shift on a unit that is not hostile to the player (Bergsons, the allied Toba, Deer): sword icons where its basic attack reaches from the tile it stands on, plus its move range, except on the selected unit, whose real move range is already drawn (D-079, D-086). *Built*
- **CR-43.** Shift on a unit hostile to the player: its move range and its danger zone, in enemy tints. The danger zone is every tile it could target after moving with any Attack ability ready on its next turn (cooldowns tick at the start of its turn, so an ability with 1 turn left counts), without area splash: the tiles it can aim at, not those caught next to a target (D-079, D-085, D-086). Its intent cells (its planned action) show as before. *Built*

| Shift tint | Bergson and allies | Hostile |
| --- | --- | --- |
| Move | Grey-teal (0.6, 0.8, 0.8) | Red-brown (0.7, 0.45, 0.4) |
| Attack | Warm white (1, 0.9, 0.75) | Strong red (1, 0.25, 0.2) |

On screen, each preview tile is the normal overlay colour moved 35% toward its tint, at 0.55 opacity, so the red is softer than its value. The tints sit outside the four role colours. If a tile holds both kinds, the Bergson tint wins. Confirmed in play (2026-10-20): the tints read apart from Linda's blue and Lucy's red, and the enemy red is strong enough.

Source: `Core/Interactions/Runtime/UnitThreatAnalysis.cs` (`AttackReachFrom`, `BasicAttackReachFrom`, `GetAttackableCells`, `GetThreateningEnemies`), `ShiftPreviewRules.cs` (`EnemyCooldownTicksAhead` 1, `EnemyIncludeAreaSplash` false), `ShowStatsHoverPreview.cs`, `PlayerController.cs` (ghost, approach, threat arcs), `Core/Systems/GridSystem/Runtime/GridCell.ShiftPreview.cs` (tints, `ShiftPreviewTintBlend` 0.35, `ShiftPreviewAlpha` 0.55), `GridCell.cs` (per-tile attack icons), `GridManager.HoverGate.cs`. Design and the full list of 23 previews: [`plans/2026-10-19-preview-pass-design.md`](../../plans/2026-10-19-preview-pass-design.md).

## Combat feedback

The rule for feedback: **the world shows what the family does; the screen shows what happens to the family.** CR-45 and CR-46 (the damage preview) are on `main` since the 2026-10-22 merge of `thj/quick-wins` (quick wins bundle A). CR-47 to CR-52 (the feedback pass) are on `main` since the 2026-10-23 fast-forward (`f4e9d9158`). Nothing here holds the turn: every effect is fire-and-forget. Every timing and strength, with where to change it, is in [`tech/pace-timings.md`](../../tech/pace-timings.md) (sections "Kill feedback" and "Mini HP bar and low HP"); this section gives the rules only.

- **CR-44.** World and screen. What the family does to others shows in the world: on the victim's sprite and through the camera (kill flash, kill camera kick, CR-47 and CR-48). What happens to the family shows on the screen and the HUD: the red hit flash when a member is hit, the low-HP heartbeat at the screen edges and the HUD signs (CR-51, CR-52). Enemies never get a screen effect. *Built* (the world side and the heartbeat **on `thj/quick-wins`**)
- **CR-45.** Stepped damage preview. While the player picks the targets of a multi-target ability, a target's HP bar shows two segments: the damage of the shots already picked in one tint, the hovered click's damage in a second. A picked target keeps its confirmed segment while the player hovers elsewhere. The last pick, the click that fires the ability, shows its own "fires" cursor (placeholder art). Like every damage preview, it shows exact damage without crit (CR-20, CR-21). *Built* (D-134, D-136)
- **CR-46.** Lethal skull. When the previewed damage would kill, a skull shows on the target's info panel. It means "kills if it lands": it ignores the target's evasion, like the rest of the preview (D-113). On a single-target preview, the skull shows when the damage reaches the target's HP. On a multi-target ability: the normal skull shows when the shots already picked kill on their own; on the firing pick it also shows when those shots plus this click kill, drawn in the "this click" tint; on an earlier pick it never shows for a kill that needs the hovered click. Every attack preview gets it while the `displayLethalMarkPreview` option is on (default on). The skull sprite is a placeholder. *Built* (D-134, D-135)
- **CR-47.** the kill beat. When a unit outside the player's faction dies (enemies, neutrals such as the Deer, the enemy Toba of the duel, units of factions allied to the player but not in its faction), its sprite flashes white and the camera kicks. A death in the player's faction (the Bergsons and the allied Toba) gets none; it keeps its own beat (CR-25). Every death that the game announces gets the beat, so Family Role, Duo and Synergy kills, each Dark Worm split, a boss's fake death (the Dom fight's early end) and a spawn undone by reverting an ability get it too (to check in play). An optional sting plays once per kill chain; none is set yet (D-147). *Built* (D-145, D-146)
- **CR-48.** the kill kick steps up. A kill while a kill kick is still running restarts it one step stronger, up to a third and last step; each victim still gets its own flash. Kill kicks take priority over every other camera shake: while one runs, a hit or ability shake is skipped (not queued); when it ends, shakes behave as before. *Built* (D-146)
- **CR-49.** mini HP bar. Every unit with an info panel shows a thin HP bar under it, with no number, in one green for every side (D-147). It is hidden while that unit's info panel is up (hover, Shift, previews: the panel replaces it in the same spot) and when the unit is dead. A hit leaves a white damage chip that drains away; a second hit during it extends it. The bar draws above unit sprites and grid icons, and under barks, damage numbers and info panels. Units without an info panel get no bar (Deevoted, Lucy's decoy). *Built* (bar length to check in play)
- **CR-50.** low HP. A player-faction unit (a Bergson, or the allied Toba) is low while it is alive and at **25%** of its max HP or less; 0 HP never counts, so a killing blow is not a drop to low. Healing above 25% clears it; dropping again counts as a new drop. A low unit's mini bar turns amber-red and pulses. *Built* (D-113, D-146)
- **CR-51.** the heartbeat. A dark blood-red pulse at the screen edges (the centre stays clear), in heartbeat cycles. It plays: **3 cycles** when a member drops to low (the announcement); once at level start, as turn 1 begins, for every member who starts low (one announcement however many); **1 cycle** when the player selects a low member, at most once per member per player turn; **1 cycle** at the start of each player turn while any member is low, after the turn banner. It never stacks: one heartbeat whatever the number of low members (an announcement can lengthen a single cycle that is running; a second request is dropped). It pauses with the game (pause menu, tutorials) and stays visible over the red hit flash. No sound yet. *Built* (D-146, D-148)
- **CR-52.** HUD signs. While the selected member is low, the HUD shows a dark red track behind its HP bar and a red tint rising from the bottom of its portrait; a glow around the HP bar flashes on each heartbeat beat only. When a low member holding a healing item is selected, the item-pouch button bobs once. There is no steady screen overlay: the HUD signs are the steady signal (D-149). *Built*

Source: `Features/UI/Panels/Scripts/DamagePreviewRules.cs` (`DecideLethalMark`), `EntityInfoPanelUI.cs`, `Core/Units/Runtime/GUnit.cs` (`ShowDamagePreview`), `Core/Managers/GlobalSettingsSO.cs` and `Resources/GlobalSettings.asset` (`displayLethalMarkPreview` 1); feedback pass: `Core/FX/Runtime/CFX/ShakeCameraEffect.cs` (`priority`), `Features/Effects/KillFeedback/` (`KillFeedbackPresenter`, `KillFeedbackRules`), `Resources/UnitSpecific/Common/Kill_`, `Kill2_`, `Kill3_ShakeCameraEffect.asset`, `Features/UI/Panels/Scripts/MiniHealthBar/` (`UnitMiniHealthBar`, `LowHealthRules`), `Features/Effects/LowHealth/` (`LowHealthPresenter`, `LowHealthCadence`), `Features/UI/Panels/Scripts/UnitPanelUI.LowHealth.cs`, `UnitItemPouchButtonUI.cs`, the `KillFeedback` and `LowHealthFeedback` objects in `CombatLevelContainerScene.unity`. Values: [`tech/pace-timings.md`](../../tech/pace-timings.md). Design: [`plans/2026-10-20-feedback-pass-design.md`](../../plans/2026-10-20-feedback-pass-design.md) revision 2; build: [`plans/2026-10-22-feedback-pass-tech.md`](../../plans/2026-10-22-feedback-pass-tech.md).

## Attacks and damage

- **CR-19.** Damage is the effect's base factor × the attacker's `Stat_DMG`, capped at 9999. `Stat_DMG` is built in this order: the family stat (×1 to ×1.3), the unit's own layer (where Weak's ×0.6 sits), the family's shared skill-tree stats, gear as a flat bonus added after those multipliers, then the ability's own level (×). Run upgrades raise a level inside these layers. Mark's unit layer comes after his gear, so Weak also cuts his gear bonus. *Built*
- **CR-20.** Health is a whole number; each hit is rounded (halves to even). The hover preview uses the same rounding, so it shows exact damage and kills. *Built*
- **CR-21.** Crit and evasion are rolled once per target per hit. A critical hit (the attacker's `Stat_CRC` chance) deals ×1.5. Then evasion (the target's `Stat_EVA` chance) cancels the HP loss, but not the hit's pushes or statuses. Otherwise damage taken is × the target's `Stat_DR`: 1 is full damage, 0.8 is 20% less. Burn ticks and push damage can also be evaded and reduced; push damage can crit, Burn can't. The damage preview leaves crit out. *Built*
- **CR-22.** Some area attacks hit both sides (the Masher's slam). A kill caused by something other than an ability (burn, a push, friendly fire) gives no XP or gold. *Built*

Source: `Core/Systems/StatsResourcesSystem/Runtime/StatEvaluation.cs` (`StatResolver.Resolve`), `StatAttributes/StatBackedValue.cs`, `AAttributeModifier.cs`, `RuntimeAAttributeBase.cs` (`ApplyModifiers`), `Features/_Common/Prefabs/UnitBase.prefab` (health modifiers, stat profiles).

## Health, death and revenge

- **CR-23.** A unit at 0 HP dies and leaves the board. *Built*
- **CR-24.** HP carries over between levels of a mission. At the next level, a family member starts at their saved HP, at least 20% of max, plus `Stat_HPG` × max (0 until upgraded). The floor also brings back members who fell in a won level, at 20%. *Built*
- **CR-25.** When a family member dies, each other living member takes Revenge after a short beat: for 2 turns, ×1.5 damage, +20% crit chance, +1 AP and +1 to the AP cap, plus a ready basic attack (which adds nothing on `main`: basic attacks have no cooldown). The values are the same for John, Linda, Lucy and Mark; Toba neither gives nor takes Revenge. *Built* (Q5)
- **CR-26.** **On `thj/home-test`:** the first member downed in a sortie comes home Wounded ([Home](home.md)). *Demo*

Source: `Core/Units/Runtime/GUnit.cs`, `Core/Units/Runtime/Factions/FactionTracker.cs`, `Core/Interactions/Runtime/PlayerController.cs` (revenge), `Resources/GlobalSettings.asset` (`persistHealthsThroughMission` on).

## Statuses

| Status | Shown as | What it does | Status |
| --- | --- | --- | --- |
| Vulnerable | Vulnerable | Takes 20% more damage (`Stat_DR` ×1.2) for 2 turns; reapplying refreshes, doesn't stack | Built |
| Weak | Weak | Deals 40% less damage (`Stat_DMG` ×0.6) for 2 turns | Built |
| Burnt | Burnt | Loses 3 HP at the start of its turn, twice (6 in all); not scaled by damage, can't crit | Built |
| Crippled | Crippled | Can't walk for 1 turn; takes 4 × the mover's damage for each cell it is pushed or pulled. Applied by Linda's Harmonic Slam | Built |
| Stunned | Stunned | Skips its next turn (enemies). Applied by Mark's Vault with Stunning Vault (Q6) | Built |
| Taunted | Taunted | Must target the taunter, through its next turn. No ability read so far applies it (to check) | Built |
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

| Item | State | Decision | Notes |
| --- | --- | --- | --- |
| Bergson Time (Reactive Interrupt, key L) | Deferred | D-038 | Works only with ATB, so it is off with FTP |
| ATB gauge | Dropped | D-036 | Dropped as the direction. The gauge still fills during enemy turns and takes leftover AP, but nothing spends it with FTP |
| Shared AP | Dropped | D-037 | Half-built code remains |
| Action reversion (undo an action for FTP) | Off (`enableActionReversion` 0, cost 0) | — | |
| Several AP for one long move (distance ÷ range, rounded up) | Built | — | No unit turns it on (`allowMultiActivation`) |
| Hit-stop and every time effect, including the kill freeze | Deferred | D-113, D-145 | No time effect for now, on enemies or Bergsons. The existing hit slow-mo on enemy hits is unchanged and also slows the kill flash and kick (CR-47) |
| Steady low-HP screen overlay | Dropped | D-149 | The HUD signs (CR-52) are the steady signal |
| Kill sting and low-HP sounds (sting, heartbeat) | Deferred | D-147 | Hooks built, sound ids empty; waiting on real sounds |
| "Target n/N" label and the pulsing skull | Dropped | D-137 | The stepped preview and the static skull (CR-45, CR-46) made picks clear |

## Branch differences

- **On `main`:** FTP since `92853a5a9` (2026-10-16); before that, ATB.
- **On `thj/home-test`:** FTP. Home adds per-sortie effects at level start: the send-off meal, Omens, Wounded members at 50% HP in the dungeon, and a "From Home" banner ([Home](home.md)).
- the feedback pass (CR-47 to CR-52: kill beat, shake priority, mini HP bar, low HP), committed `07f4e44fe` to `403de3bf8`, merged into `main` on 2026-10-23 (`f4e9d9158`). `thj/home-test` takes it with `main`.

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
10. **Q10.** Answered by THJ (D-090): the threat arcs count attacks ready on the enemy's next turn (`cooldownTicksAhead: 1`), like the Shift danger zone, so the two agree (CR-39). Built in `d1254f7c8`, on `main` since the 2026-10-20 merge.
11. **Q11.** "Danger zone" is a working name. It needs a player-facing name only if it ever appears as text (tutorial, tooltip). Glossary, narrative agent.
12. **Q12.** The low-HP state (CR-50) has no player-facing name. It needs one only if it ever appears as text; not "Wounded", which is a Home term. Glossary, narrative agent.

## Related

- Decisions: D-034 to D-038; previews D-064, D-071, D-072, D-078, D-079, D-085, D-086, D-088 to D-090; feedback D-113, D-134 to D-137, D-145 to D-149
- Detail: [`combat-balance.md`](../combat-balance.md), [`tech/pace-timings.md`](../../tech/pace-timings.md) (every combat timing), [`tech/mechanics-brief.md`](../../tech/mechanics-brief.md), [`tech/combat-architecture.md`](../../tech/combat-architecture.md) (dev cheats)
- [Family systems](family-systems.md) · [Enemies](enemies.md) · [Progression and economy](progression-economy.md)
