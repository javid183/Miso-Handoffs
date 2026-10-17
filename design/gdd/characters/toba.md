# Toba

Owner: game designer (THJ approves) · Scope: `all` · Checked against assets: `main` @ `92853a5a9`, 2026-10-16 (ability presets read from the live project) · Mirror: Claude Doc "Miso — Game Design", tab Characters › Toba · Up: [Overview](../overview.md)

Toba is the healer and nature lover, and the family's newcomer: he was not in Children of Morta, and the roster shows it. He supports with heals, shields, swaps and taunts rather than damage. He joins after M4 "Into the Rootwell". Formerly called Dom: assets and folders may still say Dom, but the name is always Toba ([Glossary](../../../glossary.md)).

| Item | Value | Status |
| --- | --- | --- |
| Max HP | 24 | Built |
| AP per turn | 2 (family default) | Built |
| FP value (adds to the FTP maximum) | 1 | Built |
| Joins | After M4 "Into the Rootwell" (`unlockedAfterMission`) | Built |
| Family Role | None | Open ([Family systems](../family-systems.md#open-questions) Q1) |
| Duos | Linda–Toba | Built |
| Synergies | None | Built |

Source: `Features/Player/Dom/Prefabs/Unit_Toba.prefab`.

## Abilities

| Ability | Kind | What it does | AP | Cooldown | Status |
| --- | --- | --- | --- | --- | --- |
| Axe Dance | Basic attack | Melee: 10 × damage | 1 | 0 | Built |
| Healing Wind | Heal | One ally within 3, himself included, heals 10 × `Stat_WIS` (×1.5 or ×2 with the Healing Wind node) | 1 | 0 | Built |
| Nature's Gambit (swap) | Utility | Two units within 4 (5 or 6 with the Nature's Gambit node), of either side, trade cells; Toba isn't one of them | 1 | 1 | Built |
| Provoking Presence (taunt) | Utility | Every enemy within 3 (4 with the node) is pulled up to 2 cells toward him, Immovable ones excepted; a Crippled enemy takes 4 × damage per cell. +1 FTP | 1 | 2 | Built |
| Protective Shell | Signature (1 SP to unlock) | One ally within 3 (4 with Guardian's Reach), himself included, takes no damage from the next hit | 1 | 2 | Built |
| Wall | Area | A 3-cell wall (it can be rotated) on empty cells, centre within 3. It lasts 3 turns, blocks walking and can't be targeted | 1 | 0 | Built |

Damage is a base factor × `Stat_DMG`, healing a base factor × `Stat_WIS` ([Combat rules](../combat-rules.md) CR-19). Cooldown 1 means once per turn, 2 every other turn. No ability ends the turn by itself.

Duo trigger on his bar: Linda–Toba ([Family systems](../family-systems.md#duos)). Only Provoking Presence fills FTP ([Combat rules](../combat-rules.md) CR-11). He has no Cleanse.

Source: `abilityOrchestrator` on `Unit_Toba.prefab`; presets in `Resources/UnitSpecific/Player/Dom/` (`Attack/Primary/Dom_Ability_Attack_Axe.asset`, `Abilities/Heal/Dom_Ability_Heal.asset`, `Abilities/Swap/Dom_Ability_Swap.asset`, `Abilities/Taunt/Dom_Ability_Taunt.asset`, `Abilities/Barrier/Dom_Ability_Barrier.asset`, `Abilities/WallAbility/Toba_Ability_Wall.asset`).

## Passives

- **TO-1.** Toba has no passive components, no Family Role, no Pass-by entry, no Revenge and no ATB gauge. Whether each is deliberate for the newcomer is open (Q1). *Built*
- **TO-2.** His healing scales with his Bond to the target (glossary, Demo Spec). Not on `main`: his heals (Healing Wind, the Linda–Toba Duo) read only `Stat_WIS`, and `main` has no Bond. `thj/home-test` was not read. *Planned* (Q3)

## Skill tree

Nodes unlock by the total skill points this character has spent in their tree (the "Unlocks at" column). A node with a "Needs" entry also waits until that node is maxed.

| Node | Unlocks at | Pips | Effect | Needs |
| --- | --- | --- | --- | --- |
| Protective Shell | 0 | unlock | Unlocks Protective Shell | — |
| Healing Wind | 0 | 2 | Healing Wind heals more | — |
| Guardian's Reach | 2 | 1 | Protective Shell reach +1 | Protective Shell |
| Provoking Presence | 2 | 1 | Taunt radius +1 | — |
| Nature's Rhythm | 3 | 1 | AP cap 2 → 3. He still starts each turn with 2 AP; the third point only comes from AP gifts (Father's Resolve) and can be carried into the next turn (Q4) | — |
| Nature's Gambit | 5 | 2 | Swap distance +1 per level | Healing Wind |

Family node kept on Toba's tree: **Healing Marks** (the Linda–Toba Duo heals more, 2 pips).

Source: `skillTree` on `Unit_Toba.prefab` (Nature's Rhythm targets `StatUB_AP`).

## Revenge

None: Toba neither takes nor causes Revenge (both flags off). Q1.

## Gear

| Item | Slot | Stat | Level 1 | Level 2 | Level 3 |
| --- | --- | --- | --- | --- | --- |
| Exquisite Stone Axe | Right hand (weapon) | Damage | +4 (10 Gold, 1 Stone) | +6 (20 Gold, 3 Stone, 1 Timber) | +8 (40 Gold, 3 Stone, 3 Timber) |
| Tribal Necklace | Necklace | Damage reduction | 0.075 (10 Gold, 1 Stone) | 0.1 (20 Gold, 1 Stone, 1 Fabric) | 0.125 (40 Gold, 3 Stone, 3 Fabric) |

The necklace starts at 0.05 for free. Two free slots take the shared Vitality Brooch and Shin Armor. Source: `Resources/Unit Equipments/Dom/*.asset` (descriptions still say "Dom"; Q2).

## Run upgrades

| Upgrade | Effect |
| --- | --- |
| Guardian's Reach | Protective Shell reach +1 level (same as the skill node) |

Source: `Resources/RunUpgrades/TobaShellRadius/RU_TobaShellRadius.asset`.

## Home

**On `thj/home-test`:** Toba's Home talents (tending gives +2 yield and an extra egg, the Mending lesson, Care that ends Wounded at once with double Bond) are in the [Demo Spec](../../demo-spec.md) › Character affinities. He is half of the showcase pair with Linda; his other pairs start lower on Bond.

## Open questions

1. **Q1.** Toba has no Family Role, no Pass-by, no Revenge, no ATB gauge, and carries one item where the others carry two. Deliberate for the newcomer, or missing?
2. **Q2.** The Stone Axe and Tribal Necklace descriptions still say "Dom". Rename to Toba?
3. **Q3.** Where should Bond-scaled healing live (TO-2)?
4. **Q4.** Nature's Rhythm only raises his AP cap. Should it give him a third action every turn?

## Related

[Family systems](../family-systems.md) · [Combat rules](../combat-rules.md) · [`player-skill-trees.md`](../../player-skill-trees.md) · [Glossary](../../../glossary.md)
