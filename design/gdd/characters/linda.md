# Linda

Owner: game designer (THJ approves) · Scope: `all` · Checked against assets: `main` @ `92853a5a9`, 2026-10-16 (ability presets read from the live project) · Mirror: Claude Doc "Miso — Game Design", tab Characters › Linda · Up: [Overview](../overview.md)

Linda is the archer: ranged damage that pierces lines of enemies, and a watchful Family Role that shoots anything moving into her lanes. She is the family's strongest damage dealer today (46–72% of damage in the October playtests), which is why her role is the first to get a limit.

| Item | Value | Status |
| --- | --- | --- |
| Max HP | 20 | Built |
| AP per turn | 2 (family default) | Built |
| FP value (adds to the FTP maximum) | 2 | Built |
| Joins | From the start | Built |
| Family Role | Watch: shoots enemies that end a move in her row or column ([Family systems](../family-systems.md#family-roles)) | Built, differs (no limit yet) |
| Duos | John–Linda, Linda–Lucy, Linda–Toba, Mark–Linda | Built |
| Synergies | Sisters' Rivalry, Tempest Bloom (with Lucy), Catch & Return (with Mark) | Built |

Source: `Features/Player/Linda/Prefabs/Unit_Linda.prefab`.

## Abilities

| Ability | Kind | What it does | AP | Cooldown | Status |
| --- | --- | --- | --- | --- | --- |
| Bow attack | Basic attack | An arrow along her row or column, 4 cells (5 or 6 with Longshot), that pierces every enemy in line: 6 × damage to the first, then ×0.6 of the previous hit for each next enemy (×0.8 or ×1.0 with Power-Piercing Arrows) | 1 | 0 | Built |
| Explosive Crescendo | Attack | An arrow to any cell within 5: 8 × damage to each enemy on that cell and the 4 next to it (×1.2 with Louder Crescendo) | 1 | 2 | Built |
| Harmonic Slam | Signature (1 SP to unlock) | Enemies next to her are Crippled for 1 turn (and Weak for 2 with Diminishing Blow); then she steps to a free cell within 1 (2 with Echoing Retreat). No damage, by design. +1 FTP | 1 | 1 | Built |
| Cleanse | Shared family ability | 50 × damage to Corruption planted within 1 cell; doesn't hurt units ([Characters](README.md)) | 1 | 1 | Built |

Damage is a base factor × `Stat_DMG`, healing a base factor × `Stat_WIS` ([Combat rules](../combat-rules.md) CR-19). Cooldown 1 means once per turn, 2 every other turn. No ability ends the turn by itself.

Duo triggers on her bar: Linda–Lucy, John–Linda, Mark–Linda, Linda–Toba ([Family systems](../family-systems.md#duos)).

Source: `abilityOrchestrator` on `Unit_Linda.prefab`; presets in `Resources/UnitSpecific/Player/Linda/` (`Attack/Primary Attack/Linda_Ability_PrimaryAttack.asset` with `Features/Player/Linda/Prefabs/LindaAttackArrow.prefab`, `Attack/Explosive Arrow/Linda_Ability_ExplosiveArrow.asset`, `Abilities/HarmonicSlam/Linda_Ability_HarmonicSlam.asset`); `design/combat-balance.md` (Harmonic Slam is damage-free by design).

## Passives

- **LI-1. Sisters' Rivalry (her half).** When Lucy kills with a basic attack, Linda gets +1 AP and a ready basic attack. *Built* ([Family systems](../family-systems.md#synergies))
- **LI-2. Move as One.** Once bought in her tree, every Bergson gets +1 movement on their first move of each level (the bonus is spent by that move, or ends after 2 turns). *Built*

Source: `Features/Player/Linda/Scripts/UnitKillAbilityPointProvider.cs`, `LindaFirstMove.cs` and their components on `Unit_Linda.prefab`.

## Skill tree

Nodes unlock by the total skill points this character has spent in their tree (the "Unlocks at" column). A node with a "Needs" entry also waits until that node is maxed.

| Node | Unlocks at | Pips | Effect | Needs |
| --- | --- | --- | --- | --- |
| Harmonic Slam | 0 | unlock | Unlocks Harmonic Slam | — |
| Longshot | 0 | 2 | +1 arrow range per level (0 / 1 / 2) | — |
| Diminishing Blow | 2 | unlock | Harmonic Slam applies Weak | Harmonic Slam |
| Move as One | 2 | unlock | Family: +1 movement on each Bergson's first move (LI-2) | — |
| Louder Crescendo | 3 | 1 | Explosive Crescendo hits harder | — |
| Power-Piercing Arrows | 5 | 2 | Arrows lose less damage per enemy: decay 0.6 → 0.8 → 1.0 | Longshot |

Linda has no family nodes on her own tree; her Duos and Synergies are bought on John's, Lucy's, Mark's and Toba's trees.

Source: `skillTree` on `Unit_Linda.prefab` (Stat_RANGE 0 / 1 / 2, Stat_DMGD 0.6 / 0.8 / 1.0).

## Revenge

When a family member dies, Linda gets for 2 turns: damage ×1.5, +20% crit chance, +1 AP and +1 to her AP cap. *Built*

## Gear

| Item | Slot | Stat | Level 1 | Level 2 | Level 3 |
| --- | --- | --- | --- | --- | --- |
| Crescent Bow | Right hand (weapon) | Damage | +1 (10 Gold, 1 Timber) | +3 (20 Gold, 3 Timber) | +5 (40 Gold, 5 Timber) |
| Stylish Hairband | Head | Evasion | 0.05 (10 Gold, 1 Fabric) | 0.1 (20 Gold, 3 Fabric) | 0.15 (40 Gold, 5 Fabric) |

One free slot takes the shared Shin Armor. Source: `Resources/Unit Equipments/Linda/*.asset` (the hairband's file is named `Equipment_Styllish Hairband.asset`).

## Run upgrades

| Upgrade | Effect |
| --- | --- |
| Power-Piercing Arrows | Arrow damage decay ×1.5 (stacks with the skill node; Q1) |
| Louder Crescendo | Explosive Crescendo damage +1 level |
| Echoing Retreat | Harmonic Slam retreat distance +1 level |
| Diminishing Blow | Harmonic Slam applies Weak for 2 turns (same as the skill node) |
| Sisters' Bond | Linda–Lucy Duo damage +1 level (needs both in the squad) |

Source: `Resources/RunUpgrades/*/RU_*.asset`.

## Home

**On `thj/home-test`:** Linda's Home talents (her violin speeds a tended plot, the Mossy Tablet's timber stand, the Footwork lesson) are in the [Demo Spec](../../demo-spec.md) › Character affinities. She is half of the showcase pair with Toba.

## Open questions

1. **Q1.** Power-Piercing Arrows exists as both a skill node and a run upgrade; the run upgrade can push the decay past 1.0 (more damage on later targets). Cap it, or rename one?
2. **Q2.** Her role has no limit yet and costs 1 FTP ([Family systems](../family-systems.md) FR-3 to FR-5).

## Related

[Family systems](../family-systems.md) · [Combat rules](../combat-rules.md) · [`player-skill-trees.md`](../../player-skill-trees.md) · [`combat-balance.md`](../../combat-balance.md) · [Glossary](../../../glossary.md)
