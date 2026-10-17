# Lucy

Owner: game designer (THJ approves) · Scope: `all` · Checked against assets: `main` @ `92853a5a9`, 2026-10-16 (ability presets read from the live project) · Mirror: Claude Doc "Miso — Game Design", tab Characters › Lucy · Up: [Overview](../overview.md)

Lucy is the daughter and the family's fire mage: a fragile skirmisher whose embers chase targets, whose Cyclone reshapes the board, and whose Family Role follows up every attack the others make. Many of the family's combos run through her (Papa's Shelter, Shield Flare, Tempest Bloom, Sisters' Rivalry).

| Item | Value | Status |
| --- | --- | --- |
| Max HP | 15 | Built |
| AP per turn | 2 (family default) | Built |
| FP value (adds to the FTP maximum) | 3 | Built |
| Joins | From the start | Built |
| Family Role | Follow-up: hits an enemy right after a family member's action ([Family systems](../family-systems.md#family-roles)); no limit yet | Built, differs |
| Duos | John–Lucy, Linda–Lucy, Mark–Lucy | Built |
| Synergies | Sisters' Rivalry, Tempest Bloom (with Linda), Papa's Shelter, Shield Flare (with John) | Built |

Source: `Features/Player/Lucy/Prefabs/Unit_Lucy.prefab`.

## Abilities

| Ability | Kind | What it does | AP | Cooldown | Status |
| --- | --- | --- | --- | --- | --- |
| Fire Embers | Basic attack | Within 3 cells: a main ember (4 × damage) plus sidewinder embers (3 × damage each) that each pick a target: 1 sidewinder at base, 2 or 3 with Sidewinders, one more when Sheltered. With Lingering Embers, targets Burn. She can target John while his Shield Up is on (Shield Flare) | 1 | 0 | Built |
| Cyclone | Area | A cyclone on a cell within 3. It lasts 5 turns, moves up to 3 cells a turn toward units and blocks walking; it deals 7 × damage to enemies it reaches or that move into it (×1.2 or ×1.4 with Cyclone Power). Arrows crossing it can split (Tempest Bloom) | 1 | 2 | Built |
| Blink | Signature (1 SP to unlock) | Teleports to a free cell within 5 and leaves a decoy on her old cell. +1 FTP | 1 | 2 (1 with Rapid Blink) | Built |
| Cleanse | Shared family ability | 50 × damage to Corruption planted within 1 cell; doesn't hurt units ([Characters](README.md)) | 1 | 1 | Built |

Damage is a base factor × `Stat_DMG`, healing a base factor × `Stat_WIS` ([Combat rules](../combat-rules.md) CR-19). Cooldown 1 means once per turn, 2 every other turn. No ability ends the turn by itself.

Duo triggers on her bar: John–Lucy, Linda–Lucy, Mark–Lucy ([Family systems](../family-systems.md#duos)).

Source: `abilityOrchestrator` on `Unit_Lucy.prefab`; presets in `Resources/UnitSpecific/Player/Lucy/` (`Attack/Primary Attack/Lucy_Ability_PrimaryAttack.asset`, `Abilities/Cyclone/Lucy_Cyclone_Ability.asset` with `Features/Player/Lucy/Prefabs/Cyclone.prefab`, `Move/Teleport/Lucy_Ability_Teleport.asset`).

## Passives

- **LU-1. Sisters' Rivalry (her half).** When Linda kills with a basic attack, Lucy gets +1 AP and a ready basic attack. *Built*
- **LU-2. Papa's Shelter.** Next to John, Lucy is Sheltered and her basic attack gains a level (one more ember) until she moves away. *Built*

Source: `Features/Player/Linda/Scripts/UnitKillAbilityPointProvider.cs`, `Features/Player/Lucy/Scripts/LucyPassiveAbility_PapasShelter.cs` and their components on `Unit_Lucy.prefab`. Both are described in [Family systems](../family-systems.md#synergies).

## Skill tree

Nodes unlock by the total skill points this character has spent in their tree (the "Unlocks at" column). A node with a "Needs" entry also waits until that node is maxed.

| Node | Unlocks at | Pips | Effect | Needs |
| --- | --- | --- | --- | --- |
| Blink | 0 | unlock | Unlocks Blink | — |
| Sidewinders | 0 | 2 | +1 sidewinder ember per level | — |
| Rapid Blink | 2 | 1 | Blink cooldown −1 | Blink |
| Kindled Spirits | 2 | 1 | Family: every Bergson +10% crit chance | — |
| Lingering Embers | 3 | unlock | Fire Embers apply Burn | — |
| Cyclone Power | 5 | 2 | Cyclone hits harder | Sidewinders |

Family nodes kept on Lucy's tree: **Tempest Bloom** (unlock: projectiles split through her Cyclone; costs 1 Family Skill Point) and **Marks-Sisters** (Linda–Lucy Duo damage, 2 pips).

Source: `skillTree` on `Unit_Lucy.prefab`; `LucyFactionSharedStats` (crit 0 / 0.1).

## Revenge

When a family member dies, Lucy gets for 2 turns: damage ×1.5, +20% crit chance, +1 AP and +1 to her AP cap. *Built*

## Gear

| Item | Slot | Stat | Level 1 | Level 2 | Level 3 |
| --- | --- | --- | --- | --- | --- |
| Pyromancer's Ring | Ring (weapon order at Home) | Crit chance | 0.1 (10 Gold, 1 Steel) | 0.15 (20 Gold, 3 Steel) | 0.2 (40 Gold, 5 Steel) |
| Pyromancer's Robe | Chest | Max HP | +5 (10 Gold, 1 Fabric) | +7 (20 Gold, 3 Fabric) | +10 (40 Gold, 5 Fabric) |

One free slot takes the shared Vitality Brooch. Source: `Resources/Unit Equipments/Lucy/*.asset`.

## Run upgrades

| Upgrade | Effect |
| --- | --- |
| Stoked Embers | Fire Embers damage +1 level |
| Lingering Embers | Fire Embers apply Burn for 2 turns (same as the skill node) |
| Howling Gale | Cyclone applies Weak for 2 turns |
| Tempest Bloom | Projectiles split through her Cyclone (same as the family node) |
| Sisters' Bond | Linda–Lucy Duo damage +1 level |

Source: `Resources/RunUpgrades/*/RU_*.asset`.

## Home

**On `thj/home-test`:** Lucy's Home talents (her tending turns a Hearty Gourd into a Soul Gourd, she alone reads the Recipe Scrap, the Edge lesson) are in the [Demo Spec](../../demo-spec.md) › Character affinities.

## Open questions

1. **Q1.** Sidewinders is set up differently from every other numeric node (upgrade mode 0 instead of 1). It likely explains the "Maxed Out" with no points spent and the "+3 in game" seen in playtests. Fix the data?
2. **Q2.** Names for the Linda–Lucy pair: Sisters' Rivalry (synergy), Marks-Sisters (Duo node), Sisters' Bond (run upgrade). Keep three names?
3. **Q3.** In the John–Lucy Duo, Lucy's QTE uses Linda's input binding (`LindaQTE`). Data slip?

## Related

[Family systems](../family-systems.md) · [Combat rules](../combat-rules.md) · [`player-skill-trees.md`](../../player-skill-trees.md) · [Glossary](../../../glossary.md)
