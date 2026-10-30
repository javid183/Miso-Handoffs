# John

Owner: game designer (THJ approves) · Scope: `all` · Checked against assets: `main` @ `92853a5a9`, 2026-10-16 (ability presets read from the live project) · Mirror: Claude Doc "Miso — Game Design", tab Characters › John · Up: [Overview](../overview.md)

John is the father and the family's shield: a sword-and-shield tank who takes hits meant for the others and turns that pain into damage. He is the anchor most Duos and Synergies lean on (Linda, Lucy and Mark each have one with him).

| Item | Value | Status |
| --- | --- | --- |
| Max HP | 32 | Built |
| AP per turn | 2 (family default) | Built |
| FP value (adds to the FTP maximum) | 5 | Built |
| Joins | From the start | Built |
| Family Role | Shield: takes an ally's hit ([Family systems](../family-systems.md#family-roles)); costs 1 FTP | Built, differs |
| Duos | John–Linda, John–Lucy, Mark–John | Built |
| Synergies | Papa's Shelter, Shield Flare (with Lucy), Command Shield Dash (with Mark) | Built |

Source: `Features/Player/John/Prefabs/Unit_John.prefab`.

## Abilities

| Ability | Kind | What it does | AP | Cooldown | Status |
| --- | --- | --- | --- | --- | --- |
| Sword Attack | Basic attack | Melee: 8 × damage (×1.2 / ×1.4 / ×1.6 at ability levels 1–3; Tempered Blade adds a level). With Sundering Strikes, the target is Vulnerable for 2 turns | 1 | 0 | Built |
| Shield Dash | Attack | Dashes in a straight line up to 3 cells (4 or 5 with Battering Charge, +1 with Extensive Dash), through allies. Each enemy next to the path or the end cell takes 4 × damage and is pushed 1 cell; a Crippled enemy takes another 4 × damage | 1 | 2 | Built |
| Shield Up | Defence | Until his next turn he takes 60% of damage (50% or 40% with the Shield Up node). Arms Wrath. +1 FTP | 1 | 1 | Built |
| Father's Resolve | Signature (1 SP to unlock) | An ally within 6 cells gets +1 AP (+2 with Decisive Resolve) and its basic attack readied; not usable on an ally at its AP cap | 1 | 1 | Built |
| Cleanse | Shared family ability | 50 × damage to Corruption planted within 1 cell; doesn't hurt units ([Characters](README.md)) | 1 | 1 | Built |

Damage is a base factor × `Stat_DMG`, healing a base factor × `Stat_WIS` ([Combat rules](../combat-rules.md) CR-19). Cooldown 1 means once per turn, 2 every other turn. No ability ends the turn by itself.

Duo triggers on his bar: John–Linda, John–Lucy, Mark–John ([Family systems](../family-systems.md#duos)).

Source: `abilityOrchestrator` on `Unit_John.prefab`; presets in `Resources/UnitSpecific/Player/John/` (`Attack/Primary/John_Ability_Attack_Sword.asset`, `Attack/Secondary/John_Ability_Attack_Dash.asset`, `Abilities/Shield/John_Ability_Shield.asset`, `Abilities/APTransfer/John_APTransfer_Ability.asset`).

## Passives

- **JO-1. Wrath.** Casting Shield Up arms Wrath until his next turn. Each hit he takes while it lasts, or through his Shield role, stores a stack (max 3). His next damaging ability spends all stacks for +35% damage each. *Built* (the 2026-10-08 notes say +40%; Q1)
- **JO-2. Blood Debt.** The last enemy to hurt another family member carries Blood Debt. John deals ×1.3 damage to it, with every damaging ability, until another enemy takes the mark or it dies. *Built*
- **JO-3. Shield Flare.** With Shield Up on, a fireball from Lucy that reaches him is absorbed and relaunched along the four diagonals (range 2). *Built* ([Family systems](../family-systems.md#synergies))
- **JO-4. Command Shield Dash.** When a unit finishes a move from Mark's Command, a press QTE gives John a free Shield Dash. *Built* ([Family systems](../family-systems.md#synergies))

Source: `Features/Player/John/Scripts/JohnPassiveAbility_Wrath.cs`, `JohnPassiveAbility_BloodDebt.cs`, `JohnShieldRelay.cs`, `JohnPassiveAbility_CommandShieldDash.cs` and their components on `Unit_John.prefab`.

## Skill tree

Nodes unlock by the total skill points this character has spent in their tree (the "Unlocks at" column). A node with a "Needs" entry also waits until that node is maxed. Pips are the levels a node can be bought.

| Node | Unlocks at | Pips | Effect | Needs |
| --- | --- | --- | --- | --- |
| Father's Resolve | 0 | unlock | Unlocks Father's Resolve | — |
| Shield Up | 0 | 2 | Damage taken while shielded: 60% → 50% → 40% | — |
| Decisive Resolve | 2 | 1 | Father's Resolve gives 2 AP instead of 1 | Father's Resolve |
| Of the Same Blood | 2 | 1 | Family: every Bergson +20% max HP | — |
| Sundering Strikes | 3 | unlock | Sword Attack applies Vulnerable | — |
| Battering Charge | 5 | 2 | +1 Shield Dash range per level (also the free dash after Command) | Shield Up |

Family nodes kept on John's tree: **John–Linda Dance** (+1 movement in the Duo per level, 2 pips) and **Hide and Seek** (+1 decoy in the John–Lucy Duo per level, 2 pips). See [Progression and economy](../progression-economy.md) for how the trees are paid.

Source: `skillTree` on `Unit_John.prefab`; `JohnFactionSharedStats` (Stat_HP rows 1 / 1.2).

## Revenge

When a family member dies, John gets for 2 turns: damage ×1.5, crit +20%, and +1 AP (and +1 to his AP cap). *Built* ([Combat rules](../combat-rules.md))

## Gear

Workshop upgrades. Level 0 is what he starts with.

| Item | Slot | Stat | Level 1 | Level 2 | Level 3 |
| --- | --- | --- | --- | --- | --- |
| Ancestral Sword | Right hand (weapon) | Damage | +3 (10 Gold, 1 Steel) | +5 (20 Gold, 3 Steel) | +7 (40 Gold, 5 Steel) |
| Ancestral Shield | Left hand | Damage reduction | 0.05 (10 Gold, 1 Steel) | 0.1 (15 Gold, 3 Steel) | 0.15 (40 Gold, 5 Steel) |

Two free slots take the shared Vitality Brooch (HP) and Shin Armor (evasion). Source: `Resources/Unit Equipments/John/*.asset`, `Resources/Unit Equipments/Shared/*.asset`.

## Run upgrades

| Upgrade | Effect |
| --- | --- |
| Extensive Dash | Shield Dash +1 range |
| Tempered Blade | Sword Attack damage +1 level |
| Sundering Strikes | Sword Attack applies Vulnerable for 2 turns (same as the skill node) |

Source: `Resources/RunUpgrades/John*/RU_*.asset`. Rules: [Progression and economy](../progression-economy.md#run-upgrades).

## Home

**On `thj/home-test`:** John's Home talents (Kitchen batch of 3, the War Journal's armory, the Toughness lesson) are in the [Demo Spec](../../demo-spec.md) › Character affinities.

## Open questions

1. **Q1.** Wrath: +35% per stack in the asset, +40% in the 2026-10-08 notes. Which is intended?
2. **Q2.** His Shield role takes the hit at a factor of 0.5; the notes say 0.4 ([Family systems](../family-systems.md#open-questions) Q8). **Answered:** ×0.5 base, lowered by tree upgrades (D-217).
3. **Q3.** The shared ability on every member but Toba is titled Cleanse in the data, while its sounds say Dedication ([Characters](README.md)). Which name should players see?

## Related

[Family systems](../family-systems.md) · [Combat rules](../combat-rules.md) · [`player-skill-trees.md`](../../player-skill-trees.md) · [`combat-balance.md`](../../combat-balance.md) · [Glossary](../../../glossary.md)
