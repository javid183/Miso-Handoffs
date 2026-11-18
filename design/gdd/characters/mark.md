# Mark

Owner: game designer (THJ approves) · Scope: `all` · Checked against assets: `main` @ `92853a5a9`, 2026-10-16 (ability presets read from the live project); MA-3 from `main` @ `8c2e8617c`, 2026-10-29 (`ProjectileCatchAndReturn.cs`, `Unit_Mark.prefab` read); MA-3 offer rule and preview from `main` @ `2cf617358`, 2026-11-17 (from the build reports, code not re-read) · Mirror: Claude Doc "Miso — Game Design", tab Characters › Mark · Up: [Overview](../overview.md)

Mark is the monk and Zen master: a fast melee fighter who chains kills, builds Focus into a barrier, commands allies across the board, and strikes back at anyone who hurts the family. He joins after "No More Waiting" (M3) and has a Duo with every sibling and John.

| Item | Value | Status |
| --- | --- | --- |
| Max HP | 15 | Built |
| AP per turn | 2 (family default) | Built |
| FP value (adds to the FTP maximum) | 3 | Built |
| Joins | After M3 "No More Waiting" (`unlockedAfterMission`) | Built |
| Family Role | Counter: strikes back at an enemy that hit family ([Family systems](../family-systems.md#family-roles)); no limit yet | Built, differs |
| Duos | Mark–Lucy, Mark–Linda, Mark–John | Built |
| Synergies | Catch & Return (with Linda), Command Shield Dash (with John) | Built |

Source: `Features/Player/Mark/Prefabs/Unit_Mark.prefab`.

## Abilities

| Ability | Kind | What it does | AP | Cooldown | Status |
| --- | --- | --- | --- | --- | --- |
| Fist Blitz | Basic attack (also his role attack) | Dashes to an enemy within 2 cells and strikes: 8 × damage (×1.2 or ×1.4 with Heavy Hands). If it dies, he steps into its cell | 1 | 0 | Built |
| Vault | Attack | Leaps to a cell within 3 (4 with Long Vault). Every enemy next to where he lands takes 2 × damage and is pushed 1 cell (and Stunned for 1 turn with Stunning Vault) | 1 | 1 | Built |
| Command | Signature (1 SP to unlock) | Any unit within 4 that isn't Immovable, ally or enemy, walks to a cell within 3 of it that he picks. An enemy moved this way is Weak for 2 turns with Sapping Order. A finished Command move offers John a free Shield Dash | 1 | 1 | Built |
| Cleanse | Shared family ability | 50 × damage to Corruption planted within 1 cell; doesn't hurt units ([Characters](README.md)) | 1 | 1 | Built |

Damage is a base factor × `Stat_DMG`, healing a base factor × `Stat_WIS` ([Combat rules](../combat-rules.md) CR-19). Cooldown 1 means once per turn, 2 every other turn. No ability ends the turn by itself.

Duo triggers on his bar: Mark–Lucy, Mark–Linda, Mark–John ([Family systems](../family-systems.md#duos)).

Source: `abilityOrchestrator` on `Unit_Mark.prefab`; presets in `Resources/UnitSpecific/Player/Mark/` (`Primary/Mark_Ability_Attack_Primary.asset`, `Vault/Mark_Ability_Attack_Vault.asset`, `Command/Mark_Ability_Attack_Command.asset`).

## Passives

- **MA-1. Atman's Focus.** Each basic attack he lands adds 1 Focus (max 5). Focus adds damage (+1 to +5) and a barrier that soaks incoming damage before health (3, 5, 7, 8, 9). A hit costs 2 Focus; a hit bigger than the barrier breaks it. *Built* (the tooltip says Focus comes from kills; Q1)
- **MA-2. Continuous Attack.** When his Fist Blitz kills, a press QTE swings again at the lowest-health enemy in range. It costs 1 FTP, then +1 for each further use in the same turn. *Built, differs.* **Planned (D-216):** free, with a per-turn limit (value not set); FTP pays for Duos only.
- **MA-3. Catch & Return.** Once bought, when Linda's bow or Watch arrow reaches him from 2 or more cells away along its line, and the return copy would hit at least one enemy, the arrow stops at Mark and a press QTE ("Catch Arrow") offers the catch (D-257, D-260; a shorter prompt wait than other QTEs, D-273). *Built* (on `main` since 2026-10-29, D-326; the offer rule since 2026-11-17, D-560):
  - **Offered only with an enemy between:** the catch is offered only if the return copy (Mark back to Linda) would hit an enemy. Allies and neutral units don't count. With no enemy between Linda and Mark there is no prompt and the arrow flies on as if Mark weren't there, whether or not enemies stand past him (D-560). If the return can't be worked out, the catch is offered as before.
  - **Pressed:** the arrow is caught at Mark and never reaches the enemy behind him. A return copy flies from Mark back to Linda, damaging enemies on the way, and ends at her (D-261, D-276). An enemy between them is hit on the way out and again on the way back (D-274). With the quiver on, the arrow goes straight back into her quiver ([Linda](linda.md) LI-9); with it off, no arrow is involved and the damaging return is all (D-315, D-320).
  - **Aim preview:** while Linda aims through Mark and the catch would be offered, the return shows on the board and its damage as a second segment on the HP bar; the forward hits past Mark keep their normal red preview, and only what the return hits gets the second colour (D-564; [Combat rules](../combat-rules.md) CR-56). When it wouldn't be offered, only the normal shot shows.
  - **Not pressed:** the same arrow carries on with its remaining range and falloff, and lands as usual.
  - No refund: bounce only; the node text that promises a refund gets fixed (D-218). **Planned (D-228):** the node becomes "Return to Sender", once per turn refunding Linda's shot (+1 AP).

Source: `Features/Player/Mark/Scripts/MarkPassiveAbility_AtmanFocus.cs`, `MarkPassiveAbility_ContinuousAttack.cs`, `ProjectileCatchAndReturn.cs` (with `CatchSweep.cs`; the offer rule in `CatchOfferRules.cs`) and their components on `Unit_Mark.prefab` (catch: `returnMode` BounceBack, `triggerWithQTE` on, `minTileDistance` 2, one whitelisted arrow, `returnPrefab` `LindaAttackArrowReturn`, unlock `_MarkLindaSynergy`). (`MarkPassiveAbility_AtmanBarrier.cs` exists but is not on the prefab.)

## Skill tree

Nodes unlock by the total skill points this character has spent in their tree (the "Unlocks at" column). A node with a "Needs" entry also waits until that node is maxed.

| Node | Unlocks at | Pips | Effect | Needs |
| --- | --- | --- | --- | --- |
| Command | 0 | unlock | Unlocks Command | — |
| Heavy Hands | 0 | 2 | Fist Blitz hits harder | — |
| Sapping Order | 2 | unlock | Command applies Weak | Command |
| Flowing Guard | 2 | 1 | Family: every Bergson +5% evasion | — |
| Stunning Vault | 3 | unlock | Vault stuns the enemies next to where he lands | — |
| Atman Body | 5 | 2 | Takes less damage: damage reduction 0.1 / 0.2 | Heavy Hands |

Family nodes kept on Mark's tree: **Chained Assault** (Mark–Lucy Duo damage, 2 pips), **Family Watchers** (+1 shout radius in the Mark–John Duo, 2 pips), **Head Start** (race cooldown −1 in the Mark–Linda Duo, 1 pip) and **Catch & Return** (unlock; 1 Family Skill Point).

Source: `skillTree` on `Unit_Mark.prefab`; `MarkFactionSharedStats` (evasion 0 / 0.05).

## Revenge

When a family member dies, Mark gets for 2 turns: damage ×1.5, +20% crit chance, +1 AP and +1 to his AP cap. *Built*

## Gear

| Item | Slot | Stat | Level 1 | Level 2 | Level 3 |
| --- | --- | --- | --- | --- | --- |
| Wrist Wrap of Power | Right hand (weapon) | Damage | +2 (10 Gold, 1 Fabric) | +4 (20 Gold, 3 Fabric) | +6 (50 Gold, 5 Fabric) |
| Monk's Tunic | Chest | Evasion | 0.05 (10 Gold, 1 Fabric) | 0.1 (20 Gold, 3 Fabric) | 0.15 (40 Gold, 5 Fabric) |

Mark starts with no gear equipped, and he has no weapon slot for the Wrist Wrap (Q3). Source: `Resources/Unit Equipments/Mark/*.asset`.

## Run upgrades

| Upgrade | Effect |
| --- | --- |
| Iron Knuckles | Fist Blitz damage +1 level |
| Long Vault | Vault range +1 level |
| Vault Stun | Vault stuns (same as the skill node; title is a placeholder) |
| Sapping Order | Command applies Weak for 2 turns (same as the skill node) |
| Always Ready | Starts each turn with at least 1 ATB step (ATB only, so inactive with FTP). Kept, but out of the altar pool; an FTP replacement is to design (D-187) |

Source: `Resources/RunUpgrades/Mark*/RU_*.asset`.

## Home

**On `thj/home-test`:** Mark's Home talents (tea master, focused reader, the Focus lesson, the only one who can chart The Crown) are in the [Demo Spec](../../demo-spec.md) › Character affinities.

## Open questions

1. **Q1.** Atman's Focus: the tooltip says kills give Focus; the code gives it on every basic attack that lands. Which is intended?
2. **Q2.** Catch & Return's node says it refunds his attack; the data only bounces the arrow back ([Family systems](../family-systems.md#open-questions) Q9). **Answered:** bounce only; fix the node text (D-218).
3. **Q3.** The Wrist Wrap of Power uses a weapon slot Mark doesn't have, so it can't be equipped on `main`. The Demo Spec lists it as his Workshop weapon.
4. **Q4.** Data copied from Lucy: his role and Continuous Attack QTEs use Lucy's input binding (`LucyQTE`), his hit sound is Lucy's, and his revenge line ("Noooo!") is hers. Fix?
5. **Q5.** The Mark–Lucy Duo and its node are Chained Assault for now (THJ); the skill-tree notes say "Sidewinder Blitz" and the glossary says "Fist Blitz". Not final: Duo names wait for a narrative pass ([Family systems](../family-systems.md#open-questions) Q2). **Answered:** Chained Assault for now (D-223).

## Related

[Family systems](../family-systems.md) · [Combat rules](../combat-rules.md) · [`player-skill-trees.md`](../../player-skill-trees.md) · [`combat-balance.md`](../../combat-balance.md) · [Glossary](../../../glossary.md)
