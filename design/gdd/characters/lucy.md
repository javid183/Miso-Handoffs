# Lucy

Owner: game designer (THJ approves) · Scope: `all` · Checked against assets: `main` @ `92853a5a9`, 2026-10-16 (ability presets read from the live project); Family Role line from `main` @ `8c2e8617c`, 2026-10-29 (`LucyFactionRoleHandler.cs` read); Cyclone on `main` from the Cyclone tech plan's code facts and report C1b (`main` @ `aaae8a7db`); [Cyclone (Pulling Gale)](#cyclone-pulling-gale) LU-3 to LU-7 and the Steer row from the `thj/cyclone` build reports C1a to C5, 2026-11-12; round 2 (carry, burst, previews, Cyclone Power 3 / 4 / 5) from reports `cyclone-r2-c1.md` to `cyclone-r2-c4.md` and the final gate, 2026-11-17 (uncommitted, not play-checked yet) · Mirror: Claude Doc "Miso — Game Design", tab Characters › Lucy · Up: [Overview](../overview.md)

Lucy is the daughter and the family's fire mage: a fragile skirmisher whose embers chase targets, whose Cyclone reshapes the board, and whose Family Role follows up every attack the others make. Many of the family's combos run through her (Papa's Shelter, Shield Flare, Tempest Bloom, Sisters' Rivalry).

| Item | Value | Status |
| --- | --- | --- |
| Max HP | 15 | Built |
| AP per turn | 2 (family default) | Built |
| FP value (adds to the FTP maximum) | 3 | Built |
| Joins | From the start | Built |
| Family Role | Follow-up: hits an enemy right after a family member's action did it real HP damage ([Family systems](../family-systems.md#family-roles); real-damage rule D-277, on `main` since 2026-10-29); no limit yet. **On `thj/cyclone`:** never on a Cyclone hit (LU-5) | Built, differs |
| Duos | John–Lucy, Linda–Lucy, Mark–Lucy | Built |
| Synergies | Sisters' Rivalry, Tempest Bloom (with Linda), Papa's Shelter, Shield Flare (with John) | Built |

Source: `Features/Player/Lucy/Prefabs/Unit_Lucy.prefab`.

## Abilities

| Ability | Kind | What it does | AP | Cooldown | Status |
| --- | --- | --- | --- | --- | --- |
| Fire Embers | Basic attack | Within 3 cells: a main ember (4 × damage) plus sidewinder embers (3 × damage each): 1 sidewinder at base, 2 or 3 with Sidewinders, one more when Sheltered. **The player picks a target for each ember** (the main ember too), and the same enemy can be picked more than once; each ember is its own hit on its pick (code, `GetRequiredTargetCount` counts the effects at her upgrade level; play-checked by THJ 2026-11-10; the Hearth's Memory 2 opens on a page that teaches it, [Missions](../missions-structure.md) MI-31). With Lingering Embers, targets Burn. She can target John while his Shield Up is on (Shield Flare) | 1 | 0 | Built |
| Cyclone | Area | A cyclone on a cell within 4 (`radiusV` 4; this sheet said 3). It lasts 5 turns, moves up to 3 cells a turn toward units and blocks walking; it deals 3 × damage to enemies it reaches or that move into it (7 × until D-518, 2026-11-11; ×1.2 or ×1.4 with Cyclone Power). Arrows crossing it can split (Tempest Bloom). **On `thj/cyclone`:** Pulling Gale: it holds a cross and never moves on its own, Whirls (pull, then 3 ×; 4 × and 5 × with Cyclone Power) on cast, after every Steer and at the end of each enemy turn, lasts 3 enemy turns, range 3, cooldown 4; heavy enemies walk through and burst it (LU-3 to LU-7) | 1 | 2 (**On `thj/cyclone`:** 4) | Built |
| Steer | Area | **On `thj/cyclone` only.** Takes the Cyclone button's place while her Cyclone is out: moves it up to 3 cells, carrying the enemies beside it, then it Whirls (LU-6) | 1 | 1 (once a turn) | Built (`thj/cyclone`) |
| Blink | Signature (1 SP to unlock) | Teleports to a free cell within 5 and leaves a decoy on her old cell. +1 FTP | 1 | 2 (1 with Rapid Blink) | Built |
| Cleanse | Shared family ability | 50 × damage to Corruption planted within 1 cell; doesn't hurt units ([Characters](README.md)) | 1 | 1 | Built |

Damage is a base factor × `Stat_DMG`, healing a base factor × `Stat_WIS` ([Combat rules](../combat-rules.md) CR-19). Cooldown 1 means once per turn, 2 every other turn. No ability ends the turn by itself.

Duo triggers on her bar: John–Lucy, Linda–Lucy, Mark–Lucy ([Family systems](../family-systems.md#duos)).

Source: `abilityOrchestrator` on `Unit_Lucy.prefab`; presets in `Resources/UnitSpecific/Player/Lucy/` (`Attack/Primary Attack/Lucy_Ability_PrimaryAttack.asset`, `Abilities/Cyclone/Lucy_Cyclone_Ability.asset` with `Features/Player/Lucy/Prefabs/Cyclone.prefab` and the hit `Lucy_Cyclone_Effect_AttrMod` (3 × `Stat_DMG`), `Move/Teleport/Lucy_Ability_Teleport.asset`). **On `thj/cyclone`:** also `Abilities/Cyclone/Lucy_Ability_Steer.asset` (9th entry on `Unit_Lucy.prefab`), `Lucy_Ability_Steer_Effect_Steer.asset` and `Lucy_Cyclone_Whirl_Pusher.asset`.

## Cyclone (Pulling Gale)

**On `thj/cyclone`** (D-529 to D-545; round 2 D-547 to D-559), until it merges. On `main` the Cyclone is still the drifting one in the table above. Design and reasoning: [`cyclone-redesign.md`](../../cyclone-redesign.md) and, for round 2, [`plans/2026-11-17-cyclone-round2-design.md`](../../../plans/2026-11-17-cyclone-round2-design.md); build: [`plans/2026-11-11-cyclone-redesign-tech.md`](../../../plans/2026-11-11-cyclone-redesign-tech.md) (reports `reports/cyclone-c1a.md` to `cyclone-c4.md`) and [`plans/2026-11-17-cyclone-round2-tech.md`](../../../plans/2026-11-17-cyclone-round2-tech.md) (reports `reports/cyclone-r2-c1.md` to `cyclone-r2-c4.md`). Round 2 is uncommitted on the branch; none of it is play-checked yet (D-534; play list `playtests/2026-11-17-cyclone-round2-play-check.md`).

> Lucy's Cyclone holds a cross. It pulls enemies on its arms in and hits those beside it, after each enemy turn and every time Lucy casts or Steers it. Enemies beside it move with it.

- **LU-3. Cast and lifetime.** 1 AP, a cell within 3, cooldown 4, one Cyclone at a time (the button is Steer while it is out, LU-6). The cell must be empty: no unit and no planted entity (spikes, webs, pools, mushrooms, traps); the cursor refuses other cells. The Cyclone stands on that cell and never moves on its own. Its **arms** are the 2 cells in each straight direction (8 cells, no diagonals); its **touching cells** are the 4 next to it. It has 3 pips and loses one at the start of each family turn, at no other time: cast in round 1, it is out through enemy turns 1, 2 and 3 and fades as round 4 starts. A burst ends it early (LU-7). Nobody can target it. On the board, the 4 touching cells carry a faint cool swirl tint and each arm tip (2 out) one inward chevron; no number (round 2's redraw; placeholder art). The cast's aim preview draws the cross at the cursor, a ghost (with a faint tether to where it stands) for each enemy the cast Whirl will pull, and the hit's damage segment and lethal skull on each enemy it will hit, on the ghost for a pulled one. *Built*
- **LU-4. Whirl.** On cast, at the end of every Steer (LU-6), and at the end of each enemy faction's turn (after its last unit has acted; the turn waits for it), in this order:
  1. **Pull:** each enemy on an arm moves 1 cell toward the Cyclone if that cell is free (no unit, no planted entity that blocks walking; a hazard that doesn't block is fine and fires on landing), nearest first; a cell a nearer enemy leaves is free for the one behind. Immovable units (EN-3) and units larger than one cell aren't pulled. A pull pays no Crippled damage: the Cyclone's pull carries no per-cell effect (`Lucy_Cyclone_Whirl_Pusher.asset` has no `onMoveEffects`), so only the family's pushes and pulls deal it (round 2's design said the pull would pay it once; as built it doesn't).
  2. **Reactions:** Family Roles answer the pull as they answer a push (Watch fires on an enemy pulled into Linda's lane; one answer per action, see LU-6).
  3. **Hit:** 3 × damage (4 × and 5 × with Cyclone Power) to each enemy on a touching cell, once each; a large unit is hit once if any of its cells touches. An enemy pulled in from 2 cells out is hit by the same Whirl.

  On cast, the pull is part of Lucy's action and the hit lands just after her action ends. Two enemy factions make two Whirls a round; an enemy turn that is skipped makes none. Without Steers, a cast makes at most 4 Whirls with one enemy faction (12 × to an enemy that stays touching); each Steer adds one. If the Cyclone bursts while a Whirl runs, that Whirl skips the pull and hit it hasn't reached yet (LU-7). The combat log shows "✦ Whirl · Lucy: carried N, pulled N, hit M" (carried is 0 except after a Steer). *Built*
- **LU-5. No Cyclone hit is anyone's action** (D-551). Every Cyclone hit (the cast's, a Steer's and the end-of-turn Whirls, and the burst, LU-7) is real damage, reported like any ability hit and credited to Lucy's cast: mission stats, barks, kill XP and gold, the sisters' tally (once per kill). It is nobody's action, so Lucy's own Family Role doesn't follow up on it (D-277) and the Masher's counter ignores it (D-537). Howling Gale's Weak lands on every enemy a Cyclone hit lands on, and only those. A Cyclone hit, a pull, or a carried enemy's landing (LU-6) wakes an Unaware enemy, and the wake spreads to its Unaware neighbours as any wake does (EN-14, EN-15; D-542). *Built* (wake on pull and on landing: play check pending)
- **LU-6. Steer.** While her Cyclone is out, the Cyclone button (same slot, same key) is **Steer**: 1 AP, once a turn (its own cooldown 1; the cast's cooldown is untouched). The Cyclone moves up to 3 four-way steps (the path may turn) and must end on an empty cell (LU-3's rule). It crosses the family, allies and hazards that don't block; walls, planted entities that block walking, and units it can't shove stop it. **Enemies beside it move with it** (the carry, D-548). At each step, in this order:
  1. **In front:** the enemy on the touching cell the Cyclone steps into is shoved one cell ahead. If that cell is blocked (wall, unit, walk-blocking planted entity, the map edge), the step can't be taken. An Immovable or larger-than-one-cell enemy, a neutral or factionless unit, or a stashed entity the caster isn't allied with blocks the step too.
  2. **Beside:** each enemy on a side touching cell moves one cell the same way; one whose next cell is blocked stays and drops out.
  3. The Cyclone moves; then the enemy **behind** follows into the cell it left.

  Riders are worked out again after each step: an enemy that ends a step beside the Cyclone rides the next one, and an enemy two cells ahead becomes the front enemy part-way. Riders are the units the pull can move: Immovable and larger-than-one-cell units never ride, and beside the Cyclone they neither ride nor block. The family and allies are crossed, never carried.
  - **Where it can go:** the cursor and range highlight offer only cells a whole Steer reaches, so a Steer never stops short after the click. A straight line through a blocked front step is never taken, but a cell beyond it is still offered when another route within 3 steps reaches it (around the side, shoving sideways); the preview draws that route (D-553, THJ to judge at play; a hard refusal is the alternative). If the end cell is taken in the meantime (rare), nothing moves.
  - **One landing** (D-549): carried enemies glide with the Cyclone and land once, when it arrives. On the way: no Crippled damage, no hazard on the cells crossed, no pass-through reactions. On landing, a hazard on the landing cell fires, Family Roles answer the move (Watch, if it lands in Linda's lane) and it wakes. Then the Whirl: after the landings settle (D-555), the pull, its reactions, and the hit. Known core limit: a faction answers one queued Family Role per action, so several riders landing in Linda's lane in one Steer get one Watch, not one each (the same holds for several pulled enemies).
  - **Aim preview** (one planner shared by the range, the preview and the move): the path (a way round is drawn as taken), a faint Cyclone and its cross at the landing cell (the current cross dims and hides there), one ghost per enemy that will move (carried or pulled, final cell only) joined to where it stands by a faint tether, the hit's damage segment and lethal skull on the ghost (its health panel moves onto the ghost while shown), and an orange ring under a ghost that lands on a planted entity. HP bars show the Whirl hit only: no Watch, hazard or crit. With the cursor already on a reachable cell when Steer is picked, the preview draws at once.

  Log: "✦ Whirl · Lucy: carried N, pulled N, hit M"; the name "Gust" is retired (D-551). The Steer is not available while a Whirl, a Steer, a pull or a burst is running, after a burst, and never to an AI-controlled Lucy (D-540). Text (D-559): "Glides the Cyclone up to 3 cells, carrying the enemies beside it. Then it Whirls. Once a turn." Placeholder: the Cyclone's icon and cast animation, title "Steer". *Built*
- **LU-7. What it stops, and the burst.** Enemies can't enter or path through its cell; the family, allies, neutrals and decoys path through it but can't end a move there; pushes and pulls stop on the cell before it ([Combat rules](../combat-rules.md) CR-58). Enemy shots whose line runs through its tile are refused (CR-57); family projectiles pass, and Linda's straight arrows still split (Tempest Bloom). Enemies treat its cross as dangerous ground ([Enemies](../enemies.md) EN-18, EN-19). Linda's arrows never land on its cell ([Linda](linda.md) LI-6, D-252 unchanged). *Built*

  **Heavies walk through and burst it** (D-550). A heavy is a unit hostile to Lucy's faction that is Immovable or larger than one cell (read from existing data; today the Masher, the Goblin Queen and the Mountain Deev, which never walks). On its own move (a walk, the Masher's counter walk, the Queen's charge) a heavy paths through the Cyclone's cell, never ending there. The moment it steps onto the cell, the Cyclone **bursts**: one hit (the Whirl's hit) on the heavy and on each enemy beside the Cyclone, once each, no pull; then the Cyclone is gone (after a 0.3 s ring) and the heavy walks on. Only heavies hostile to Lucy's faction burst it: a light enemy, the family (Immovable or not) or an allied large unit never does. A jump never bursts it (the Queen's jump lands only on its destination, D-557); a heavy pushed or pulled still stops before it; an enemy dash attack paths around it and never bursts it. The burst follows LU-5 (credited to the cast, no counter, no follow-up, Howling Gale). The cast's cooldown keeps running. During a Whirl, the burst lands at once and that Whirl skips its remaining pull and hit; during a Steer, the riders still land, its Whirl hits no one, and the Cyclone goes when the Steer ends. A burst Cyclone is no dangerous ground and stops no shot. Log: "✦ Burst · Lucy: hit M". **Warning:** the Cyclone wobbles and its pips flicker while a heavy enemy's shortest path to its nearest family unit crosses the Cyclone within that heavy's move this turn. It is not the AI's actual plan: the game has no enemy intent path, so a heavy going for someone else, or moving twice, may not wobble it (D-558). *Built* (play check pending)

**Family Super Time** (CR-14) **on `thj/cyclone`:** Lucy's Cyclone lands only on an empty cell (LU-3). While her Cyclone is already out, her part is skipped (D-535).

**Not built:** the Trailing Gale and Second Cyclone run upgrades (D-531). The design's camera ease and wind sound on the Whirl are not built; the cross tint and chevrons, tether, hazard ring, pips, swell and burst ring are placeholder art. "Eye of the Storm" is approved as a possible on-screen name, with no slot chosen (D-559).

| Value | `thj/cyclone` | Source |
| --- | --- | --- |
| Cast | 1 AP, range 3, cooldown 4 | `Lucy_Cyclone_Ability.asset` (`radiusV` 3, `coolDownV` 4) |
| Life | 3 pips, one per family turn start | `Cyclone.prefab` (`lifeTurns` 3) |
| Arms / pull | 2 cells / 1 cell | `Cyclone.prefab` (`armLength` 2), `Lucy_Cyclone_Whirl_Pusher.asset` (distance 1, speed 4, no `onMoveEffects`) |
| Hit (every Whirl and the burst) | 3 × `Stat_DMG`; Cyclone Power 4 × / 5 × | `Lucy_Cyclone_Effect_AttrMod` (base factor 3) via `Lucy_Cyclone_Effect_Compound`; Cyclone Power: `Stat_DMG` level factors 1.333333 / 1.666667 on `Lucy_Cyclone_Ability.asset` (were 1.2 / 1.4, which both rounded to 4; D-551) |
| Swell | 0.2 s | `Cyclone.prefab` (`swellSeconds`) |
| Steer | 1 AP, cooldown 1, reach 3 (four-way steps); glide 0.15 s a cell | `Lucy_Ability_Steer.asset`, `Lucy_Ability_Steer_Effect_Steer.asset`, `steerSecondsPerCell` (code default) |
| Burst ring | 0.3 s | `CycloneEntity.BurstSeconds` (code constant) |
| Settle wait | 10 quiet frames, 15 s cap (after a pull; also before a Steer's pull when it carried someone) | `CycloneEntity.Whirl.cs` (code) |

Source: `Features/Player/Lucy/Scripts/Cyclone/` (`CycloneEntity` and its partials incl. `.Burst`, `.HeavyPass`, `.AIDanger`; `CycloneRules`, `CycloneWhirlPlanner`, `CycloneCarryPlanner`, `CycloneSteerRules`, `CycloneHeavy`, `CycloneBurstRules`, `CycloneOutcome`, `CycloneSteerPreview`, `CycloneCastPreview`, `CycloneCrossView`, `CycloneWobble`, `AEffectCycloneSpawner`, `AEffectCycloneSteer`), `Features/Player/Lucy/Scripts/LucyFactionRoleHandler.cs` (Super Time), `Features/Enemy/Masher Goblin/Scripts/MasherCounterRules.cs`, `Core/Managers/CombatLevelRunHandler.DamageReport.cs`, core hooks `GridCell.PlantedPass.cs` (`IPlantedMoverPass`) and `AIEndOfTurnDangerCells.cs` (`IAIEndOfTurnDangerSparesMover`); read from the build reports, values from the assets they name (Cyclone Power factors and ability texts checked in the working tree, 2026-11-17).

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
| Cyclone Power | 5 | 2 | Cyclone hits harder (×1.2, ×1.4). **On `thj/cyclone`:** every Cyclone hit is 4 ×, then 5 × `Stat_DMG` (3 × without it; D-551). Text (D-559): "Lucy's Cyclone hits harder: 4, then 5 times her Damage." / "Each level adds one more times Lucy's Damage to every Cyclone hit." | Sidewinders |

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
| Howling Gale | Cyclone applies Weak for 2 turns. **On `thj/cyclone`:** Weak for 2 turns on every enemy a Cyclone hit lands on: the cast's, every Steer's and the end-of-turn Whirls, and the burst (D-545, D-551); two hits in a turn only refresh it. Carries and pulls alone apply nothing. The Weak effect is targeted at the hit unit only (its radius field is ignored), locked by tests. Text, on the run upgrade and the unlock list alike: "Lucy's Cyclone applies Weak for 2 turns to every enemy it hits." (D-544, D-559) |
| Tempest Bloom | Projectiles split through her Cyclone (same as the family node) |
| Sisters' Bond | Linda–Lucy Duo damage +1 level |

Source: `Resources/RunUpgrades/*/RU_*.asset`.

## Home

**On `thj/home-test`:** Lucy's Home talents (her tending turns a Hearty Gourd into a Soul Gourd, she alone reads the Recipe Scrap, the Edge lesson) are in the [Demo Spec](../../demo-spec.md) › Character affinities.

## Open questions

1. **Q1.** Sidewinders is set up differently from every other numeric node (upgrade mode 0 instead of 1). It likely explains the "Maxed Out" with no points spent and the "+3 in game" seen in playtests. Fix the data?
2. **Q2.** Names for the Linda–Lucy pair: Sisters' Rivalry (synergy), Marks-Sisters (Duo node), Sisters' Bond (run upgrade). Keep three names?
3. **Q3.** In the John–Lucy Duo, Lucy's QTE uses Linda's input binding (`LindaQTE`). Data slip?
4. **Q4.** **On `thj/cyclone`:** Cyclone texts. **Answered (round 2, D-559):** approved as recommended in [`plans/2026-11-17-cyclone-round2-texts.md`](../../../plans/2026-11-17-cyclone-round2-texts.md) and in the working tree: Cyclone "Summons a Cyclone for 3 enemy turns. It Whirls on cast and after each enemy turn: pulls enemies on its arms one cell in, then hits those beside it. Most enemies can't walk or shoot through it."; Steer as in LU-6; Cyclone Power and Howling Gale as in the tables above. "Whirl" and "carries" are on-screen words; "Gust" is retired. The Steer hint line is dropped. The enemy-side burst note goes only where a text field already exists (no new UI). Still open: the Steer's own icon, and which slot (if any) "Eye of the Storm" names.
5. **Q5.** **On `thj/cyclone`:** Cyclone round 2. **Answered** (D-547 to D-551, built C1 to C4, play check pending): LU-3 to LU-7 above. Open from the build, for THJ at the play check:
   - **One Watch per action** (core): a faction answers one queued Family Role per action, so several carried or pulled enemies landing in Linda's lane give one Watch, not one each. The design's "Watch fires twice" moment doesn't happen. Lifting it is a core change (`FactionControllerBase.ProcessFRApplyWaitList`).
   - **Detour reachability** (D-553): a cell past a blocked front enemy is still offered by another route within 3 steps. Keep, or refuse every cell past a blocked front?
   - **Enemy intent ignores the Cyclone for heavies:** the next-targets prediction ranges moves without the mover, so it never predicts a heavy walking through the Cyclone, while the real turn does; a heavy's target can be under-predicted. The wobble (LU-7) is the only warning, and it reads the path to the nearest family unit, not the AI's plan (D-558).

## Related

[Family systems](../family-systems.md) · [Combat rules](../combat-rules.md) · [`player-skill-trees.md`](../../player-skill-trees.md) · [Glossary](../../../glossary.md)
