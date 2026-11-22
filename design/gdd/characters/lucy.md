# Lucy

Owner: game designer (THJ approves) · Scope: `all` · Checked against assets: `main` @ `92853a5a9`, 2026-10-16 (ability presets read from the live project); Family Role line from `main` @ `8c2e8617c`, 2026-10-29 (`LucyFactionRoleHandler.cs` read); [Cyclone (Pulling Gale)](#cyclone-pulling-gale) LU-3 to LU-7, the Cyclone and Steer rows and the value table rewritten 2026-11-22 for the merge of `thj/cyclone` into `main` (rounds 1 to 3, the reset D-580 to D-588 and the controls D-589 to D-597), from reports `cyclone-reset.md` and `cyclone-controls.md` and the presets and code defaults, now `main` @ `049897aae` (D-600; Steer cooldown 1, D-601); played by THJ (`playtests/2026-11-19-cyclone-reset-play-check.md`: all worked after the fixes) · Mirror: Claude Doc "Miso — Game Design", tab Characters › Lucy · Up: [Overview](../overview.md)

Lucy is the daughter and the family's fire mage: a fragile skirmisher whose embers chase targets, whose Cyclone reshapes the board, and whose Family Role follows up every attack the others make. Many of the family's combos run through her (Papa's Shelter, Shield Flare, Tempest Bloom, Sisters' Rivalry).

| Item | Value | Status |
| --- | --- | --- |
| Max HP | 15 | Built |
| AP per turn | 2 (family default) | Built |
| FP value (adds to the FTP maximum) | 3 | Built |
| Joins | From the start | Built |
| Family Role | Follow-up: hits an enemy right after a family member's action did it real HP damage ([Family systems](../family-systems.md#family-roles); real-damage rule D-277, on `main` since 2026-10-29); no limit yet. Never on a Cyclone hit (LU-5) | Built, differs |
| Duos | John–Lucy, Linda–Lucy, Mark–Lucy | Built |
| Synergies | Sisters' Rivalry, Tempest Bloom (with Linda), Papa's Shelter, Shield Flare (with John); Mark's Command can steer her Cyclone ([Mark](mark.md) MA-4) | Built |

Source: `Features/Player/Lucy/Prefabs/Unit_Lucy.prefab`.

## Abilities

| Ability | Kind | What it does | AP | Cooldown | Status |
| --- | --- | --- | --- | --- | --- |
| Fire Embers | Basic attack | Within 3 cells: a main ember (4 × damage) plus sidewinder embers (3 × damage each): 1 sidewinder at base, 2 or 3 with Sidewinders, one more when Sheltered. **The player picks a target for each ember** (the main ember too), and the same enemy can be picked more than once; each ember is its own hit on its pick (code, `GetRequiredTargetCount` counts the effects at her upgrade level; play-checked by THJ 2026-11-10; the Hearth's Memory 2 opens on a page that teaches it, [Missions](../missions-structure.md) MI-31). With Lingering Embers, targets Burn. She can target John while his Shield Up is on (Shield Flare) | 1 | 0 | Built |
| Cyclone | Area | Pulling Gale: a Cyclone on an empty cell within 3, or on an enemy there, which is knocked aside and hit. It holds a cross and never moves on its own; it Whirls (pull, then 3 × damage; 4 × and 5 × with Cyclone Power) on cast, after every Steer and at the end of each enemy turn, and lasts 3 enemy turns. Heavy enemies walk through and burst it. Arrows crossing it can split (Tempest Bloom). LU-3 to LU-7 | 1 | 4 | Built |
| Steer | Area | Takes the Cyclone button's place while her Cyclone is out: glides it up to 3 steps, through enemies, hitting each; an enemy where it stops is knocked onward and hit; then it Whirls. Clicking the Cyclone opens it (LU-6) | 1 | 1 (once a turn) | Built |
| Blink | Signature (1 SP to unlock) | Teleports to a free cell within 5 and leaves a decoy on her old cell. +1 FTP | 1 | 2 (1 with Rapid Blink) | Built |
| Cleanse | Shared family ability | 50 × damage to Corruption planted within 1 cell; doesn't hurt units ([Characters](README.md)) | 1 | 1 | Built |

Damage is a base factor × `Stat_DMG`, healing a base factor × `Stat_WIS` ([Combat rules](../combat-rules.md) CR-19). Cooldown 1 means once per turn, 2 every other turn. No ability ends the turn by itself.

Duo triggers on her bar: John–Lucy, Linda–Lucy, Mark–Lucy ([Family systems](../family-systems.md#duos)).

Source: `abilityOrchestrator` on `Unit_Lucy.prefab`; presets in `Resources/UnitSpecific/Player/Lucy/` (`Attack/Primary Attack/Lucy_Ability_PrimaryAttack.asset`, `Abilities/Cyclone/Lucy_Cyclone_Ability.asset` with `Features/Player/Lucy/Prefabs/Cyclone.prefab` and the hit `Lucy_Cyclone_Effect_AttrMod` (3 × `Stat_DMG`), `Abilities/Cyclone/Lucy_Ability_Steer.asset` (9th entry on `Unit_Lucy.prefab`) with `Lucy_Ability_Steer_Effect_Steer.asset`, `Lucy_Cyclone_Whirl_Pusher.asset`, `Move/Teleport/Lucy_Ability_Teleport.asset`). Levels that give Lucy a kit of their own get the Steer slot from the tool `Tools > Levels > Lucy > Add Steer To Custom Kits`; `CycloneSteerKitTests` fails for any level whose Lucy has the cast and no Steer.

## Cyclone (Pulling Gale)

Design and reasoning: [`cyclone-redesign.md`](../../cyclone-redesign.md) (rounds 1 and 2) and the reset, which replaced round 2's carry: [`plans/2026-11-19-cyclone-reset-design.md`](../../../plans/2026-11-19-cyclone-reset-design.md) (D-580 to D-585) with the free route, the knock's hit and no avoidance (D-586 to D-588); controls: [`plans/2026-11-20-cyclone-controls-tech.md`](../../../plans/2026-11-20-cyclone-controls-tech.md) (D-589 to D-597). Build: [`plans/2026-11-19-cyclone-reset-tech.md`](../../../plans/2026-11-19-cyclone-reset-tech.md) (report `reports/cyclone-reset.md`) and the controls plan (report `reports/cyclone-controls.md`).

> Lucy summons the Cyclone on an empty cell, or onto an enemy, which it knocks aside. It stays 3 enemy turns and never moves on its own. On cast, after each Steer and after each enemy turn it Whirls: enemies on its arms are pulled one cell in, then every enemy beside it is hit. Lucy Steers it up to 3 steps through enemies, hitting each; an enemy where it stops is knocked onward and hit; then it Whirls.

- **LU-3. Cast and lifetime.** 1 AP, a cell within 3, cooldown 4, one Cyclone at a time (the button is Steer while it is out, LU-6). The cell must be empty (no unit, no planted entity such as spikes, webs, pools, mushrooms or traps, nothing stashed) or hold an enemy the cast can knock (below); the cursor refuses other cells. The Cyclone stands on that cell and never moves on its own. Its **arms** are the 2 cells in each straight direction (8 cells, no diagonals); its **touching cells** are the 4 next to it. It has 3 pips and loses one at the start of each family turn, at no other time: cast in round 1, it is out through enemy turns 1, 2 and 3 and fades as round 4 starts. A burst ends it early (LU-7). No ability can target it except Mark's Command ([Mark](mark.md) MA-4). On the board, the 4 touching cells carry a faint cool swirl tint and each arm tip (2 out) one inward chevron; no number (placeholder art). The cast's aim preview draws the cross at the cursor, a ghost for each enemy that will move (knocked or pulled), joined to where it stands by a warm tether ending in an arrowhead, and one damage segment and lethal skull per enemy hit, on the ghost for one that moves. *Built*
  - **Cast on an enemy** (D-566, D-567, D-585, D-587). The target may be an enemy hostile to Lucy, one cell in size and not Immovable, standing on a cell with nothing planted on it, the 4 cells next to Lucy included. It is knocked one cell **onward**, away from Lucy along the larger axis (along the row when the axes tie, at her diagonal neighbours); if that cell isn't free, to the right of onward, else to its left (the knock rule and "free", LU-6). If none is free, the cell isn't offered. Heavies, larger units, neutrals, allies and planted cells are never offered. The knocked enemy takes one Cyclone hit as it lands; then its landing counts once (a hazard there fires, Family Roles answer it, it wakes); then the Cyclone appears on the cell and the cast Whirl hits the knocked enemy again, beside it. A knock hit that kills means no end of move and no Whirl hit for it. Log: "✦ Knock · Lucy: knocked 1 and hit it", then the Whirl line. *Built*
- **LU-4. Whirl.** On cast, at the end of every Steer (LU-6), and at the end of each enemy faction's turn (after its last unit has acted; the turn waits for it), in this order:
  1. **Pull:** each enemy on an arm moves 1 cell toward the Cyclone if that cell is free (no unit, no planted entity that blocks walking; a hazard that doesn't block is fine and fires on landing), nearest first; a cell a nearer enemy leaves is free for the one behind. Immovable units (EN-3) and units larger than one cell aren't pulled. A pull deals no Crippled damage: the Cyclone's pull carries no per-cell effect (`Lucy_Cyclone_Whirl_Pusher.asset` has no `onMoveEffects`).
  2. **Reactions:** Family Roles answer the pull as they answer a push (Watch fires on an enemy pulled into Linda's lane). A faction answers one queued Family Role per action, so several enemies landing in her lane in one Whirl get one Watch (core limit, Q5).
  3. **Hit:** 3 × damage (4 × and 5 × with Cyclone Power) to each enemy on a touching cell, once each; a large unit is hit once if any of its cells touches. An enemy pulled in from 2 cells out is hit by the same Whirl. After a Steer, the Whirl skips the enemies that Steer already hit on its way (LU-6).

  Before the hit the Cyclone swells, breathes in and spits out (D-568), and the player's input is locked from the breath to the hit (D-569). On cast, the pull is part of Lucy's action and the hit lands just after her action ends. Two enemy factions make two Whirls a round; an enemy turn that is skipped makes none. Without Steers, a cast makes at most 4 Whirls with one enemy faction (12 × to an enemy that stays touching); each Steer adds one. If the Cyclone bursts while a Whirl runs, that Whirl skips the pull and hit it hasn't reached yet (LU-7). Log: "✦ Whirl · Lucy: pulled N, hit M". *Built*
- **LU-5. No Cyclone hit is anyone's action** (D-551). Every Cyclone hit (the cast knock's, every Whirl's, a Steer's hits on the way and its knock's, and the burst, LU-7) is real damage, reported like any ability hit and credited to Lucy's cast, whoever steered it (Mark's Command included): mission stats, barks, kill XP and gold, the sisters' tally (once per kill). It is nobody's action, so Lucy's own Family Role doesn't follow up on it (D-277) and the Masher's counter ignores it (D-537). Howling Gale's Weak lands on every enemy a Cyclone hit lands on, and only those. A Cyclone hit, a pull, or a knocked enemy's landing wakes an Unaware enemy, and the wake spreads to its Unaware neighbours as any wake does (EN-14, EN-15; D-542). *Built*
- **LU-6. Steer.** While her Cyclone is out, the Cyclone button (same slot, same key) is **Steer**: 1 AP, cooldown 1, so one Steer a turn (D-601, which replaced D-591's cooldown 0; D-597 dropped the free first Steer); the cast's cooldown is untouched. One Steer, worked out in full when the player clicks:
  1. **Route** (D-586). The Cyclone moves up to 3 four-way steps, turning if needed, never onto a cell twice. It crosses the family, allies, enemies (heavies included), hazards that don't block walking and stashed cells. Walls, the map edge and planted entities that block walking stop it, so it goes around them within its 3 steps.
  2. **Where it can stop:** an empty cell (LU-3's rule), or a cell holding an enemy it can knock: hostile, one cell in size, not Immovable, nothing planted on the cell, and the knock finds a landing. Never on the family, an ally, a heavy or a planted cell. A cell it can't stop on doesn't hide the cells beyond it.
  3. **Which route:** among the routes with the fewest steps that can stop there, the one that passes the most enemies; then the one that goes straight longest before turning; then a fixed direction order (up, right, down, left). A longer route never wins, even when only it would give the knock a landing. The preview's path arrows show the route. Cycling routes with Space is backlog.
  4. **Through enemies, one hit each** (D-580, D-583). Each enemy on the route before the stop takes one Cyclone hit as the Cyclone reaches its cell, one after another down the route. A passed enemy doesn't move, so it starts no reaction (no Watch, no hazard). A heavy is passed and hit; it doesn't burst the Cyclone. The family, allies and neutral units are crossed and nothing happens.
  5. **Knock** (D-581, D-587). The enemy on the stop is knocked one cell **onward**, along the route's last step; if that cell isn't free, to the Cyclone's right as it travels (moving screen-right, its right is screen-down), else to its left; if none is free, that cell isn't offered as a stop. **Free:** the cell exists and holds no unit, nothing stashed and no planted entity that blocks walking, and it isn't the Cyclone's own stop; a hazard that doesn't block walking is free and fires on landing. The knocked enemy takes one Cyclone hit as it lands; then its landing counts once: a hazard there fires, Family Roles answer it (Watch, if it lands in Linda's lane) and it wakes. The knock deals no Crippled damage. A knock hit that kills means no end of move and no Whirl hit for it.
  6. **Then the Whirl** (LU-4), once the landing's reactions have settled (D-555): pull, reactions, hit. Its hit skips every enemy hit on the way (it can still pull one in), and hits the knocked enemy again. So a Steer hits every enemy it passes or leaves beside it once, and the knocked enemy twice.
  7. **Fixed at the click.** The outcome is planned from the board as it stands at the click; a passed enemy dying on the way changes nothing. If the stop or the landing is no longer valid when the Cyclone arrives (rare), the knock is worked out again there; if that fails too, the Cyclone stays where it started, knocks no one and Whirls there.

  Nothing rides with the Steer: no carry, no drag, no turning shuffle (round 2's carry and its riders are gone, D-580, D-582).
  - **Opening the Steer** (D-589, D-590). The player picks it by its button or key, or by **clicking the Cyclone**. The click works in the player's turn when Lucy's Steer can be used (Lucy has AP, nothing is running, no reactive prompt is up, no unit stands on the Cyclone's cell), with any unit or none selected: it selects Lucy and picks the Steer. While another ability is aiming, a click on the Cyclone's cell that is a legal target of that ability, or that switches to an ally, keeps its usual meaning; any other click there switches to the Steer. Each time the Steer's target selection opens, the Cyclone **pulses** once (a 1.15 × scale bump over 0.15 s and back, plus a chevron flare). Pulses don't stack, and none plays during a Whirl's swell or its scale-back.
  - **Free first Steer (off):** a setting on the Steer effect (`firstSteerFreeEachTurn`) makes the first Steer of each of Lucy's turns cost no AP; the AP preview shows it, and undoing that Steer gives no AP back. THJ turned it off after his play check (D-597); the code stays as a switch.
  - **Aim preview** (one planner for the range, the preview and the move): the route's path arrows, a faint Cyclone and its cross at the stop (the current cross dims), the knocked enemy's ghost (at most one) and a ghost for each enemy the Whirl will pull, each joined to where it stands by the warm tether with its arrowhead, one damage segment per enemy hit (the knocked enemy's two hits summed in one), the lethal skull, and an orange ring under a ghost that lands on a planted entity. A passed enemy the hit kills shows its segment and skull where it stands and gets no pull ghost. HP bars show Cyclone hits only: no Watch, hazard or crit. With the cursor already on a reachable cell when the Steer is picked, the preview draws at once.

  Log: "✦ Steer · Lucy: hit N on the way, knocked 1 and hit it" (or "knocked 0"), then the Whirl line; a Steer made by Mark's Command logs under Mark (MA-4). The Steer is not available while a Whirl, a Steer, a pull or a burst is running, after a burst, and never to an AI-controlled Lucy (D-540). Text (working, narrative pass pending): "Glide the Cyclone up to 3 cells, through enemies, hitting each. An enemy where it stops is knocked onward and hit. Then it Whirls." Placeholder: the Cyclone's icon and cast animation, title "Steer". *Built*
- **LU-7. What it stops, and the burst.** Enemies can't enter or path through its cell (heavies excepted, below); the family, allies, neutrals and decoys path through it but can't end a move there; pushes, pulls and knocks stop on the cell before it ([Combat rules](../combat-rules.md) CR-58). Enemy shots whose line runs through its tile are refused (CR-57); family projectiles pass, and Linda's straight arrows still split (Tempest Bloom). Enemies don't avoid its cross: they walk onto its arms and end moves there freely (D-588; [Enemies](../enemies.md) EN-18). Ranged enemies avoid spots where every shot is blocked (EN-19). Linda's arrows never land on its cell ([Linda](linda.md) LI-6, D-252). *Built*

  **Heavies walk through and burst it** (D-550, D-571, D-572). A heavy is a unit hostile to Lucy's faction that is Immovable or larger than one cell (read from existing data; today the Masher, the Goblin Queen and the Mountain Deev, which never walks). On its own walk (a walk, the Masher's counter walk, the Queen's charge) a heavy paths through the Cyclone's cell and may end its walk there. The moment it steps onto the cell, the Cyclone **bursts**: one hit (the Whirl's hit) on the heavy and on each enemy beside the Cyclone, once each, no pull; then the Cyclone is gone (after a 0.3 s ring) and the heavy walks on or stays. Only heavies hostile to Lucy's faction burst it: a light enemy, the family (Immovable or not) or an allied large unit never does. A jump, a teleport or a summon never lands on it or bursts it (the Queen's jump lands only on its destination, D-557); a heavy pushed or pulled still stops before it; an enemy dash attack paths around it and never stops on it. A Steer passing through a heavy hits it and doesn't burst the Cyclone. The burst follows LU-5 (credited to the cast, no counter, no follow-up, Howling Gale). The cast's cooldown keeps running. During a Whirl, the burst lands at once and that Whirl skips its remaining pull and hit; during a Steer, the hits not yet made on the way are skipped, the knocked enemy still lands (without its hit), the Cyclone still moves, its Whirl hits no one, and the Cyclone goes when the Steer ends. A burst Cyclone stops no shot. Log: "✦ Burst · Lucy: hit M". Nothing warns before a heavy's turn: the wobble was dropped because it could warn wrongly (D-584). *Built*

**Family Super Time** (CR-14): Lucy's Cyclone lands only on an empty cell (LU-3). While her Cyclone is already out, her part is skipped (D-535).

**Not built:** the Trailing Gale and Second Cyclone run upgrades (D-531); the camera ease and wind sound on the Whirl; the fire flecks and hitstop of round 3's beats (D-568, later); cycling Steer routes with Space (backlog, D-586). The cross tint and chevrons, tether and arrowhead, hazard ring, pips, swell, pulse and burst ring are placeholder art. "Eye of the Storm" is approved as a possible on-screen name, with no slot chosen (D-559).

| Value | `main` | Source |
| --- | --- | --- |
| Cast | 1 AP, range 3, cooldown 4; an empty cell or a knockable enemy | `Lucy_Cyclone_Ability.asset` (`radiusV` 3, `coolDownV` 4) |
| Life | 3 pips, one per family turn start | `Cyclone.prefab` (`lifeTurns` 3) |
| Arms / pull | 2 cells / 1 cell | `Cyclone.prefab` (`armLength` 2), `Lucy_Cyclone_Whirl_Pusher.asset` (distance 1, speed 4, no `onMoveEffects`) |
| Hit (every Whirl, pass, knock and burst) | 3 × `Stat_DMG`; Cyclone Power 4 × / 5 × | `Lucy_Cyclone_Effect_AttrMod` (base factor 3) via `Lucy_Cyclone_Effect_Compound`; Cyclone Power: `Stat_DMG` level factors 1.333333 / 1.666667 on `Lucy_Cyclone_Ability.asset` (D-551) |
| Steer | 1 AP, cooldown 1, reach 3 four-way steps; free first Steer off | `Lucy_Ability_Steer.asset` (`apConsumptionType` 1, `coolDownV` 1; D-601), `Lucy_Ability_Steer_Effect_Steer.asset` (`reach` 3, `firstSteerFreeEachTurn` 0) |
| Steer glide | 0.15 s a cell | `CycloneEntity.Steer.cs` (`steerSecondsPerCell`, code default) |
| Knock fling | 0.12 s, hop 0.15 cell | `CycloneEntity.Wind.cs` (`flingSeconds`, `hopCells`), cast: `AEffectCycloneSpawner.Shove.cs` (`DefaultShoveSeconds`, `DefaultHopCells`) |
| Whirl beat | swell 0.1 s; breath in 0.12 s (0.35 cell), out 0.08 s; recoil 0.06 s (0.1 cell) | `Cyclone.prefab` (`swellSeconds` 0.1), `CycloneEntity.Wind.cs` (code defaults) |
| Steer pulse | 1.15 × over 0.15 s | `CycloneCrossView.cs` (`pulseScale`, `pulseSeconds`, serialized defaults) |
| Tether | warm colour (1, 0.82, 0.36, 0.9), arrowhead 0.2 × 0.15 cell | `CycloneTetherLook.cs` (defaults; runtime-added views, tunable in Play only) |
| Burst ring | 0.3 s | `CycloneEntity.BurstSeconds` (code constant) |
| Settle wait | 10 quiet frames, 15 s cap (after a pull; also before a Steer's pull when it knocked someone) | `CycloneEntity.Whirl.cs` (code) |

**Note on the Steer's cooldown (2026-11-22):** THJ set the cooldown to 1 in the Inspector and confirmed it (D-601): one Steer a turn. The asset reads 1; `CycloneSteerSetup.SteerCooldown` and the shipped-Steer test still say 0 and need updating to match.

Source: `Features/Player/Lucy/Scripts/Cyclone/` (`CycloneEntity` and its partials incl. `.Steer`, `.Whirl`, `.Wind`, `.Burst`, `.HeavyPass`, `.ClearsOnEntry`, `.Click`, `.Command`, `.FreeSteer`, `.LineOfFire`; `CycloneRules` incl. `.CastKnock`, `.CastOnEnemy`; `CycloneSteerPlanner`, `CycloneSteerPlan`, `CycloneKnockRules`, `CycloneSteerRules`, `CycloneWhirlPlanner`, `CycloneHeavy`, `CycloneBurstRules`, `CycloneOutcome`, `CycloneOutcomeView`, `CycloneSteerPreview`, `CycloneCastPreview`, `CycloneCrossView`, `CycloneClickRules`, `CyclonePulseGuard`, `CycloneButtonSwap`, `AEffectCycloneSpawner`, `AEffectCycloneSteer`, `AEffectCommandSteersCyclone`), `Features/Player/Lucy/Scripts/LucyFactionRoleHandler.cs` (Super Time), `Features/Enemy/Masher Goblin/Scripts/MasherCounterRules.cs`, `Core/Managers/CombatLevelRunHandler.DamageReport.cs`; core hooks `GridCell.PlantedPass.cs` (`IPlantedMoverPass`, `IPlantedClearsOnEntry`), `IClickablePlantedEntity` with `PlayerController.PlantedClick.cs`, `IAbilityCostOverride`, `IAbilityTargetablePlanted` with `FactionControllerBase.PlantedTarget.cs` and `GridManager.PlantedTarget.cs` (D-571, D-593; [`tech/core-systems.md`](../../../tech/core-systems.md)). Read from the build reports; values from the assets and code they name, 2026-11-22.

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
| Cyclone Power | 5 | 2 | Every Cyclone hit is 4 ×, then 5 × `Stat_DMG` (3 × without it; D-551). Text (D-559): "Lucy's Cyclone hits harder: 4, then 5 times her Damage." / "Each level adds one more times Lucy's Damage to every Cyclone hit." | Sidewinders |

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
| Howling Gale | Weak for 2 turns on every enemy a Cyclone hit lands on: the cast knock's, every Whirl's, a Steer's hits on the way and its knock's, and the burst (D-545, D-551); two hits in a turn only refresh it. Pulls alone apply nothing. The Weak effect is targeted at the hit unit only (its radius field is ignored), locked by tests. Text, on the run upgrade and the unlock list alike: "Lucy's Cyclone applies Weak for 2 turns to every enemy it hits." (D-544, D-559). Mark's Sapping Order Weak on a Command steer is a separate effect ([Mark](mark.md) MA-4) |
| Tempest Bloom | Projectiles split through her Cyclone (same as the family node) |
| Sisters' Bond | Linda–Lucy Duo damage +1 level |

Source: `Resources/RunUpgrades/*/RU_*.asset`.

## Home

**On `thj/home-test`:** Lucy's Home talents (her tending turns a Hearty Gourd into a Soul Gourd, she alone reads the Recipe Scrap, the Edge lesson) are in the [Demo Spec](../../demo-spec.md) › Character affinities.

## Open questions

1. **Q1.** Sidewinders is set up differently from every other numeric node (upgrade mode 0 instead of 1). It likely explains the "Maxed Out" with no points spent and the "+3 in game" seen in playtests. Fix the data?
2. **Q2.** Names for the Linda–Lucy pair: Sisters' Rivalry (synergy), Marks-Sisters (Duo node), Sisters' Bond (run upgrade). Keep three names?
3. **Q3.** In the John–Lucy Duo, Lucy's QTE uses Linda's input binding (`LindaQTE`). Data slip?
4. **Q4.** Cyclone texts. The round 2 texts (D-559) are superseded by the reset's working texts, in the assets today: Cyclone "Summons a Cyclone for 3 enemy turns. It Whirls on cast and after each enemy turn: pulls enemies on its arms one cell in, then hits those beside it. Most enemies can't walk or shoot through it. Cast it on an enemy to knock it away and hit it."; Steer as in LU-6; Mark's Command clause "It can also steer Lucy's Cyclone." ([Mark](mark.md) MA-4); the log lines in LU-3, LU-4, LU-6 and LU-7. All wait for a narrative pass ("carries" is retired, "knock" is new). Still open: the Steer's own icon, and which slot (if any) "Eye of the Storm" names.
5. **Q5.** Round 2's open items, after the reset: **one Watch per action** stays a core limit (a faction answers one queued Family Role per action, so the knocked enemy and the enemies a Whirl pulls into Linda's lane in one Steer get one Watch; lifting it is a core change in `FactionControllerBase.ProcessFRApplyWaitList`); **detour reachability** (D-553) is moot, replaced by the route rule (D-586); **enemy intent ignores the Cyclone for heavies** stays a known gap (the next-targets prediction ranges moves without the mover, so it never predicts a heavy walking through the Cyclone), now with no warning at all since the wobble was dropped (D-584).
6. **Q6.** During a Steer made by Mark's Command, the Command is in flight, so the knocked enemy's landing (and possibly the closing Whirl's pulls) may offer John's Command Shield Dash ([Family systems](../family-systems.md#synergies); read in code, not play-checked). Intended?

## Related

[Family systems](../family-systems.md) · [Combat rules](../combat-rules.md) · [`player-skill-trees.md`](../../player-skill-trees.md) · [Glossary](../../../glossary.md)
