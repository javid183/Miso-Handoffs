# Lucy

Owner: game designer (THJ approves) · Scope: `all` · Checked against assets: `main` @ `92853a5a9`, 2026-10-16 (ability presets read from the live project); Family Role line from `main` @ `8c2e8617c`, 2026-10-29 (`LucyFactionRoleHandler.cs` read); Cyclone on `main` from the Cyclone tech plan's code facts and report C1b (`main` @ `aaae8a7db`); [Cyclone (Pulling Gale)](#cyclone-pulling-gale) LU-3 to LU-7 and the Steer row from the `thj/cyclone` build reports C1a to C5, 2026-11-12 (not play-checked yet) · Mirror: Claude Doc "Miso — Game Design", tab Characters › Lucy · Up: [Overview](../overview.md)

Lucy is the daughter and the family's fire mage: a fragile skirmisher whose embers chase targets, whose Cyclone reshapes the board, and whose Family Role follows up every attack the others make. Many of the family's combos run through her (Papa's Shelter, Shield Flare, Tempest Bloom, Sisters' Rivalry).

| Item | Value | Status |
| --- | --- | --- |
| Max HP | 15 | Built |
| AP per turn | 2 (family default) | Built |
| FP value (adds to the FTP maximum) | 3 | Built |
| Joins | From the start | Built |
| Family Role | Follow-up: hits an enemy right after a family member's action did it real HP damage ([Family systems](../family-systems.md#family-roles); real-damage rule D-277, on `main` since 2026-10-29); no limit yet. **On `thj/cyclone`:** never on a Whirl hit (LU-5) | Built, differs |
| Duos | John–Lucy, Linda–Lucy, Mark–Lucy | Built |
| Synergies | Sisters' Rivalry, Tempest Bloom (with Linda), Papa's Shelter, Shield Flare (with John) | Built |

Source: `Features/Player/Lucy/Prefabs/Unit_Lucy.prefab`.

## Abilities

| Ability | Kind | What it does | AP | Cooldown | Status |
| --- | --- | --- | --- | --- | --- |
| Fire Embers | Basic attack | Within 3 cells: a main ember (4 × damage) plus sidewinder embers (3 × damage each): 1 sidewinder at base, 2 or 3 with Sidewinders, one more when Sheltered. **The player picks a target for each ember** (the main ember too), and the same enemy can be picked more than once; each ember is its own hit on its pick (code, `GetRequiredTargetCount` counts the effects at her upgrade level; play-checked by THJ 2026-11-10; the Hearth's Memory 2 opens on a page that teaches it, [Missions](../missions-structure.md) MI-31). With Lingering Embers, targets Burn. She can target John while his Shield Up is on (Shield Flare) | 1 | 0 | Built |
| Cyclone | Area | A cyclone on a cell within 4 (`radiusV` 4; this sheet said 3). It lasts 5 turns, moves up to 3 cells a turn toward units and blocks walking; it deals 3 × damage to enemies it reaches or that move into it (7 × until D-518, 2026-11-11; ×1.2 or ×1.4 with Cyclone Power). Arrows crossing it can split (Tempest Bloom). **On `thj/cyclone`:** Pulling Gale: it holds a cross and never moves on its own, Whirls (pull, then 3 ×) on cast and at the end of each enemy turn, lasts 3 enemy turns, range 3, cooldown 4 (LU-3 to LU-7) | 1 | 2 (**On `thj/cyclone`:** 4) | Built |
| Steer | Area | **On `thj/cyclone` only.** Takes the Cyclone button's place while her Cyclone is out: moves it up to 3 cells, then a Gust (LU-6) | 1 | 1 (once a turn) | Built (`thj/cyclone`) |
| Blink | Signature (1 SP to unlock) | Teleports to a free cell within 5 and leaves a decoy on her old cell. +1 FTP | 1 | 2 (1 with Rapid Blink) | Built |
| Cleanse | Shared family ability | 50 × damage to Corruption planted within 1 cell; doesn't hurt units ([Characters](README.md)) | 1 | 1 | Built |

Damage is a base factor × `Stat_DMG`, healing a base factor × `Stat_WIS` ([Combat rules](../combat-rules.md) CR-19). Cooldown 1 means once per turn, 2 every other turn. No ability ends the turn by itself.

Duo triggers on her bar: John–Lucy, Linda–Lucy, Mark–Lucy ([Family systems](../family-systems.md#duos)).

Source: `abilityOrchestrator` on `Unit_Lucy.prefab`; presets in `Resources/UnitSpecific/Player/Lucy/` (`Attack/Primary Attack/Lucy_Ability_PrimaryAttack.asset`, `Abilities/Cyclone/Lucy_Cyclone_Ability.asset` with `Features/Player/Lucy/Prefabs/Cyclone.prefab` and the hit `Lucy_Cyclone_Effect_AttrMod` (3 × `Stat_DMG`), `Move/Teleport/Lucy_Ability_Teleport.asset`). **On `thj/cyclone`:** also `Abilities/Cyclone/Lucy_Ability_Steer.asset` (9th entry on `Unit_Lucy.prefab`), `Lucy_Ability_Steer_Effect_Steer.asset` and `Lucy_Cyclone_Whirl_Pusher.asset`.

## Cyclone (Pulling Gale)

**On `thj/cyclone`** (D-529 to D-545), until it merges. On `main` the Cyclone is still the drifting one in the table above. Design and reasoning: [`cyclone-redesign.md`](../../cyclone-redesign.md); build: [`plans/2026-11-11-cyclone-redesign-tech.md`](../../../plans/2026-11-11-cyclone-redesign-tech.md), reports `reports/cyclone-c1a.md` to `cyclone-c4.md`. None of it is play-checked yet (D-534).

> Lucy's Cyclone holds a cross. At the end of the enemy turn, enemies on its arms are dragged in and hit. The family passes through but can't stop in it.

- **LU-3. Cast and lifetime.** 1 AP, a cell within 3, cooldown 4, one Cyclone at a time (the button is Steer while it is out, LU-6). The cell must be empty: no unit and no planted entity (spikes, webs, pools, mushrooms, traps); the cursor refuses other cells. The Cyclone stands on that cell and never moves on its own. Its **arms** are the 2 cells in each straight direction (8 cells, no diagonals); its **touching cells** are the 4 next to it. It has 3 pips and loses one at the start of each family turn, at no other time: cast in round 1, it is out through enemy turns 1, 2 and 3 and fades as round 4 starts. Nobody can target it. *Built*
- **LU-4. Whirl.** On cast, and at the end of each enemy faction's turn (after its last unit has acted; the turn waits for it), in this order:
  1. **Pull:** each enemy on an arm moves 1 cell toward the Cyclone if that cell is free (no unit, no planted entity that blocks walking; a hazard that doesn't block is fine and fires on landing), nearest first; a cell a nearer enemy leaves is free for the one behind. Immovable units (EN-3) and units larger than one cell aren't pulled.
  2. **Reactions:** Family Roles answer the pull as they answer a push (Watch fires on an enemy pulled into Linda's lane).
  3. **Hit:** 3 × damage (×1.2 or ×1.4 with Cyclone Power) to each enemy on a touching cell, once each; a large unit is hit once if any of its cells touches. An enemy pulled in from 2 cells out is hit by the same Whirl.

  On cast, the pull is part of Lucy's action and the hit lands just after her action ends. Two enemy factions make two Whirls a round; an enemy turn that is skipped makes none. With one enemy faction a cast makes at most 4 Whirls (12 × to an enemy that stays touching). The combat log shows "✦ Whirl · Lucy: pulled N, hit M". *Built*
- **LU-5. Whirl damage is real damage, but no one's action.** Each hit is reported like any ability hit, credited to Lucy's cast: mission stats, barks, kill XP and gold, the sisters' tally (once per kill). It is nobody's action, so Lucy's own Family Role doesn't follow up on it (D-277) and the Masher's counter ignores it (D-537). A Whirl hit or a pull (Whirl or Gust) wakes an Unaware enemy, and the wake spreads to its Unaware neighbours as any wake does (EN-14, EN-15; D-542). *Built* (wake on pull: play check pending)
- **LU-6. Steer and Gust.** While her Cyclone is out, the Cyclone button (same slot, same key) is **Steer**: 1 AP, once a turn (its own cooldown 1; the cast's cooldown is untouched). The Cyclone moves up to 3 straight steps; it can cross the family, allies and hazards that don't block, but not walls, enemies or planted entities that block walking; it must end on an empty cell (LU-3's rule). Then a **Gust** at the new cell only: LU-4's pull, no hit, no report; nothing is pulled along the path. The aim preview shows the path, a faint Cyclone on the landing cell, and a ghost and step arrow for every enemy the Gust will move. Log: "✦ Gust · Lucy: pulled N". The Steer is not available while a Whirl, a Steer or a pull is running, and never to an AI-controlled Lucy (D-540). Placeholder: the Cyclone's icon and cast animation, title "Steer". *Built*
- **LU-7. What it stops.** Enemies can't enter or path through its cell; the family, allies, neutrals and decoys path through it but can't end a move there; pushes and pulls stop on the cell before it ([Combat rules](../combat-rules.md) CR-58). Enemy shots whose line runs through its tile are refused (CR-57); family projectiles pass, and Linda's straight arrows still split (Tempest Bloom). Enemies treat its cross as dangerous ground ([Enemies](../enemies.md) EN-18, EN-19). Linda's arrows never land on its cell ([Linda](linda.md) LI-6, D-252 unchanged). *Built*

**Family Super Time** (CR-14) **on `thj/cyclone`:** Lucy's Cyclone lands only on an empty cell (LU-3). While her Cyclone is already out, her part is skipped (D-535).

**Not built:** the Trailing Gale and Second Cyclone run upgrades (D-531). The design's camera ease and wind sound on the Whirl are not built; the cross, pips, swell, streaks and burst ring are placeholder art.

| Value | `thj/cyclone` | Source |
| --- | --- | --- |
| Cast | 1 AP, range 3, cooldown 4 | `Lucy_Cyclone_Ability.asset` (`radiusV` 3, `coolDownV` 4) |
| Life | 3 pips, one per family turn start | `Cyclone.prefab` (`lifeTurns` 3) |
| Arms / pull | 2 cells / 1 cell | `Cyclone.prefab` (`armLength` 2), `Lucy_Cyclone_Whirl_Pusher.asset` (distance 1, speed 4) |
| Hit | 3 × `Stat_DMG` per Whirl | `Lucy_Cyclone_Effect_AttrMod` via `Lucy_Cyclone_Effect_Compound`; `whirlHitTimes` 3 (label) |
| Swell | 0.2 s | `Cyclone.prefab` (`swellSeconds`) |
| Steer | 1 AP, cooldown 1, reach 3; glide 0.15 s a cell | `Lucy_Ability_Steer.asset`, `Lucy_Ability_Steer_Effect_Steer.asset`, `steerSecondsPerCell` (code default) |

Source: `Features/Player/Lucy/Scripts/Cyclone/` (`CycloneEntity` and its partials, `CycloneRules`, `CycloneWhirlPlanner`, `CycloneSteerRules`, `AEffectCycloneSpawner`, `AEffectCycloneSteer`), `Features/Player/Lucy/Scripts/LucyFactionRoleHandler.cs` (Super Time), `Features/Enemy/Masher Goblin/Scripts/MasherCounterRules.cs`, `Core/Managers/CombatLevelRunHandler.DamageReport.cs`; read from the build reports, values from the assets they name.

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
| Cyclone Power | 5 | 2 | Cyclone hits harder (×1.2, ×1.4; **on `thj/cyclone`:** the Whirl hit) | Sidewinders |

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
| Howling Gale | Cyclone applies Weak for 2 turns. **On `thj/cyclone`:** every enemy a Whirl hits is Weak for 2 turns; a Gust (no hit) applies nothing. The Weak effect is targeted at the hit unit only (its radius field is ignored), locked by tests (D-545). Text: "Lucy's Cyclone applies Weak for 2 turns to every enemy it hits." (D-544) |
| Tempest Bloom | Projectiles split through her Cyclone (same as the family node) |
| Sisters' Bond | Linda–Lucy Duo damage +1 level |

Source: `Resources/RunUpgrades/*/RU_*.asset`.

## Home

**On `thj/home-test`:** Lucy's Home talents (her tending turns a Hearty Gourd into a Soul Gourd, she alone reads the Recipe Scrap, the Edge lesson) are in the [Demo Spec](../../demo-spec.md) › Character affinities.

## Open questions

1. **Q1.** Sidewinders is set up differently from every other numeric node (upgrade mode 0 instead of 1). It likely explains the "Maxed Out" with no points spent and the "+3 in game" seen in playtests. Fix the data?
2. **Q2.** Names for the Linda–Lucy pair: Sisters' Rivalry (synergy), Marks-Sisters (Duo node), Sisters' Bond (run upgrade). Keep three names?
3. **Q3.** In the John–Lucy Duo, Lucy's QTE uses Linda's input binding (`LindaQTE`). Data slip?
4. **Q4.** **On `thj/cyclone`:** Cyclone texts are working text, applied (D-544, `reports/cyclone-c5-text.md`); THJ approves the wording at play, and the terms Whirl, Gust, Steer, arms and cross stay glossary proposals. Cyclone: "Summons a Cyclone for 3 enemy turns. On cast and after each enemy turn, it pulls enemies on its arms one cell in, then hits those beside it. Enemies can't pass or shoot through it." Steer: "Moves the Cyclone up to 3 cells, not through walls or enemies. Then it pulls enemies on its arms one cell in, without hitting them. Once a turn." Cyclone Power unchanged ("Lucy's Cyclone hits harder."). Howling Gale: "Lucy's Cyclone applies Weak for 2 turns to every enemy it hits." (its unlock entry is now titled Howling Gale). Still open: the Steer's own icon.
5. **Q5.** **On `thj/cyclone`, proposal (not approved):** Cyclone round 2 after THJ's first play. The proposal covers the Steer carrying the enemies beside the Cyclone and then Whirling (D-547), the cross drawing, the previews, heavies bursting it, and Cyclone Power 3 / 4 / 5. LU-4 to LU-7 stay as built until THJ answers the plan's questions: [`plans/2026-11-17-cyclone-round2-design.md`](../../../plans/2026-11-17-cyclone-round2-design.md).

## Related

[Family systems](../family-systems.md) · [Combat rules](../combat-rules.md) · [`player-skill-trees.md`](../../player-skill-trees.md) · [Glossary](../../../glossary.md)
