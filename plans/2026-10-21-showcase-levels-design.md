# Showcase levels and puzzle patterns

Size: L    Tier: 3 (level content; one new system proposed: Family Feats)    Assigned to: miso-game-designer
Branch: all (levels built on `main`)
Status: **Proposed**, for discussion with THJ. Nothing here is decided.

## Why

THJ asked for level designs, or smaller level chunks, that showcase: Lucy's tutorial, John's tutorial, Lucy's Family Role, the Black Claw, the Masher, spikes, several Corruption pools to cleanse, a protect objective while surrounded, Tempest Bloom, the Duos (Mark–Linda and John–Linda first), Command Shield Dash, Shield Flare, and Catch & Return. Each level should play like a puzzle: a better solve gives a better result, and new layers of challenge arrive gradually.

Read for this draft: `design/gdd/` (overview, family systems, combat rules, enemies, missions, the four character sheets), `plans/2026-10-20-masher-reckless-tank-design.md`, `Features/Hazards/` and `Core/Entities/Runtime/HazardEntity.cs`, and the grids of Level1-C1_TArtEx, LevelM1-C1/C2, Level2-C2 and LevelMarkIntro-C1 (33 to 76 tiles, 9 to 15 wide). Layouts below stay inside that size.

## The plan in one table

Seven pieces: five full levels and two chunks that sit inside other levels. Each one adds one layer to what came before.

| # | Piece | Kind | Squad | Enemies and hazards | Showcases | New layer |
| --- | --- | --- | --- | --- | --- | --- |
| A | Lucy's Telling | Level | Lucy | Dark Claws, 1 Archer | Lucy tutorial | One hero, one kit |
| B | Papa's Telling | Level (ends in room B2) | John, Lucy | Archers, Dark Claws | John tutorial, Lucy's Role, Papa's Shelter, **Shield Flare** (B2) | Two heroes; reactions on the enemy turn |
| C | Chorus | Chunk (a room in an M2 level) | John, Lucy | Dark Claws | **Lucy's Role** in depth | Order of actions matters |
| D | Teeth of the Den | Level | John, Linda, Lucy | Black Claw + pack, **spikes** | **Black Claw**, **spikes** | A hazard's clock; an enemy rule you exploit |
| E | The Bridge | Level | John, Linda, Mark | **Masher**, goblins, spikes | **Masher**, Command Shield Dash | Luring; more than one way to win |
| F | The Weeping Pools | Level | John, Linda, Lucy, Mark | **5–6 Corruption pools** | **John–Linda Dance**, **Mark–Linda Footrace**, **Command Shield Dash** | Racing a clock; splitting the family |
| G | Hold the Ring | Level (capstone) | John, Linda, Lucy, Mark | Pools at four arms, mixed goblins | **Protect while surrounded**, **Tempest Bloom**, **Catch & Return** | Everything under pressure |

Where each showcase lives:

| Showcase | Taught in | Used again in |
| --- | --- | --- |
| Lucy tutorial | A | everywhere |
| John tutorial | B | everywhere |
| Lucy's Family Role | B (it fires on its own), C (as a puzzle) | D, G |
| Shield Flare | B2 | G (south arm), optional |
| Black Claw | D | G variant |
| Spikes | D (gate, then pack) | E (Masher lure), F variant |
| Masher | E | G variant |
| Several pools | F | G (one pool per arm) |
| Protect while surrounded | G | |
| Tempest Bloom | G (north arm); optional earlier chunk in M11 Sisters | |
| John–Linda Dance | F (mirror pools) | E alternate solve, G (swap arms) |
| Mark–Linda Footrace | F (the far pool) | |
| Command Shield Dash | E (bait), F (mobility) | G |
| Catch & Return | G (east arm) | |

Mission placement is a later step, once the first-hour pacing is settled: A and B fit the hearth prologue idea (each Bergson's exaggerated telling) or M1; C fits M2 (John and Lucy); D fits M5 (John, Linda, Lucy); E, F and G need Mark, so they come after he joins.

## How the sketches read

Each cell is one grid tile, drawn in rows from north (top) to south. The same grid becomes `GridCell - (x, y)` objects in a prefab.

```
.  floor            #  rock (blocks walking)       (blank)  no tile: a gap
^  spikes           P  Corruption pool (CP_Spawner) E  exit / goal tile
@  key tile (see the notes)                         R  protectee
J John   L Linda   U Lucy   M Mark
c Dark Claw   b Black Claw   a Archer Goblin   s Dark Shaman
O Masher (its 2 × 2 drawn as four O)
```

Each level has: goal, squad and enemies, beats (the order things are met), the obvious play and the smart play, how a better solve pays, and knobs to vary it.

---

## A. Lucy's Telling (Lucy tutorial)

**Goal:** reach Ryker on the ledge (`Unit on tiles`). Loss: Lucy dies. Tier: Tutorial.
**Teaches:** Fire Embers (sidewinders pick their own targets), Cyclone (blocks walking, hunts units), Blink (crosses gaps, leaves a decoy). Lucy has 15 HP, so the lesson under all three is *stay out of reach*.

```
# # # # # # # # # # # # #         # # #
# . . c # . . . . c . . #         . E #
# U . . c . . . c . . . .         . . E
# . . . # . . . . . c . #         a . #
# # # # # # # # # # # # #         # # #
        ^ throat          ^ edge   gap   ledge
```

| Beat | Situation | What it teaches |
| --- | --- | --- |
| 1. Two at once | A Claw in the room and one in the throat, both within 3 | One cast: the main ember on one, a sidewinder finds the other on its own |
| 2. The throat | Three Claws wake in the next room and come for her through a 1-tile throat | A Cyclone in the throat: nothing walks through it, and it drifts into them (7 × each) |
| 3. The chasm | A 2-tile gap, Ryker beyond, an Archer on the ledge | Blink (5) is the only way across; the decoy left at the edge draws the stragglers |

- **Obvious play:** trade embers with the three Claws in the open room. Lucy reaches the ledge low on HP.
- **Smart play:** Cyclone in the throat on the turn they wake, embers over it. She arrives untouched.
- **Better result:** HP carries into the next level of the mission (CR-24).
- **Note:** Blink is a signature (1 SP). In a *telling* she can have it because it is her story; the real one is earned later. The same license could preview other locked tools in the prologue (see Unlocks).

## B. Papa's Telling (John tutorial, Lucy's Role, Papa's Shelter)

**Goal:** get Lucy to the exit (`Unit on tiles`). Loss: Lucy dies. Tier: Tutorial.
In John's version Lucy is the little one to protect. That frames his whole kit: shield the family, push through, and get angry when they're hurt.

```
    a       a       a                      archers across a chasm
                                           (no tiles: they shoot, nobody walks there)
# # # # # # # # # # # # # # #
# J U . . . . . # . c # c . #
# . . . . . . . . . . . . . E
# . . . . . . . # . c # c . #
# # # # # # # # # # # # # # #
  gallery        corridor with alcoves
```

| Beat | Situation | What it teaches |
| --- | --- | --- |
| 1. The gallery | Three Archers fire across the chasm at Lucy while the pair walks the gallery | **John's Role:** keep Lucy within 2 and he takes the arrow (×0.5); the tether shows who he covers. **Papa's Shelter:** next to John, Lucy throws an extra ember. One rule, "stay by Papa", pays twice |
| 2. The alcoves | Claws in alcoves either side of the corridor | **Shield Dash:** one dash down the corridor hits and pushes every Claw beside the path. **Lucy's Role** fires right after: she follows up on one of them |
| 3. The last pack | Three Claws at the exit, one has already hurt Lucy | **Shield Up** + Wrath: John soaks hits on purpose (stacks), then one swing on the Blood Debt Claw (×1.3, +35% per stack) |

### B2. The Pockets (Shield Flare)

A short final room, or the opening of the next John-and-Lucy level (M2).

```
. . # . # . .
. a # . # a .
# # . . . # #
. . . @ . . .        @ = where John stands
# # . . . # #
. a # . # a .
. . # . # . .
```

Four Archers sit in sealed corner pockets, each 2 tiles diagonal from the centre. Walking can't reach them (movement is four-way) and Linda's lanes don't line up.

- **Obvious play:** Lucy picks them off with embers, one or two a turn, while all four shoot.
- **Smart play:** John steps to `@` and casts Shield Up (his Wrath arms; their arrows feed it). Lucy fires at John: he absorbs the fireball and relaunches it along the four diagonals, one copy into each pocket.
- **Knobs:** three pockets plus a Claw in the fourth (shows "first enemy within 2"); pockets at distance 1 and 2 mixed; later, a Sheltered Lucy with Sidewinders throwing several embers at John (if each ember flares separately: to check).

## C. Chorus (Lucy's Family Role as a puzzle)

A room inside an M2 level (John and Lucy). Three Claws spread around a small room, each tuned so that one John hit plus Lucy's two follow-up embers kills it.

- **The rule being used:** after any other family member's action, Lucy fires 2 embers at an enemy within 3 that the action targeted or hit near, and skips the enemy she hit last. Planned limit: 3 per round.
- **The puzzle:** Lucy must stand within 3 of all three Claws, and John must act near a different Claw each time. Hitting the same Claw twice wastes a follow-up, because she skips it.
- **Smart play:** order John's actions so each one leads Lucy to a fresh target: three kills from one turn of John.
- **Knobs:** a Claw just outside 3 of Lucy (she must step first); a fourth Claw to show the limit; Linda added later, so the player learns whose actions to spend Lucy's 3 follow-ups on.

## D. Teeth of the Den (Black Claw, spikes)

**Goal:** defeat all. Squad: John, Linda, Lucy. Tier: Early.

```
# # # # # # # # # # # # #
# . c . . . . . . c . . #
# . . . c b c . . . . . #      the den
# . . . . . . . . c . . #
# ^ ^ ^ ^ ^ . ^ ^ ^ ^ ^ ^ #      spike band; one safe stone (the bridge)
# . . . . . @ . . . . . #      @ = first tile past the bridge
# . . J . . . . . U . . #
# . . . . . L . . . . . #      Linda below the bridge: its column is her lane
# # # # # # # # # # # # #
```

**Spikes, as built** (my reading of `HazardEntity.cs`; to confirm in play): they tick at the start of the enemy turn. With interval 3, they rise on round 3 and then every 4th round (7, 11, ...): one turn spent re-arming makes the cycle 4 rounds. When they rise they strike whoever stands on them, either side, and anyone who steps on them stays hurt until they drop at the next enemy turn. Damage is small (3 in the asset). The countdown shows on the spike.

| Beat | Situation | What it teaches |
| --- | --- | --- |
| 1. The band | The spike band stands between the family and the den; the countdown is visible | Cross on the safe stone or on a down turn |
| 2. Ring the bell | Hitting the Black Claw sends every Dark Claw within 5 at the attacker | *Who* hits it decides where the pack goes |
| 3. The trap | Lucy's sidewinders pick their own targets | An ember that strays onto the Black Claw sends the pack at Lucy (15 HP) |

- **Obvious play:** fight the Claws one by one; someone (often Lucy, by accident) touches the leader and the pack swarms the weakest member.
- **Smart play:** John casts Shield Up and rings the bell from beside the bridge on the turn before the spikes rise. The pack crosses the band while it's raised, or funnels onto the stone, and the stone's column is Linda's lane, so she shoots each Claw that ends its move there. Every hit on John stacks Wrath; Lucy stands next to him, Sheltered.
- **Robust either way:** if the AI walks over the spikes, it bleeds; if it avoids them, it funnels into Linda's lane. Both are good outcomes for the player who planned.
- **Knobs:** two Black Claws (they share grudges within 10); the bridge off Linda's lane; an Archer that shoots the bell-ringer; a second spike band on another clock.

## E. The Bridge (Masher)

**Goal:** get the family to the far bank (`Tiles occupied`, all of the E tiles). Squad: John, Linda, Mark. Tier: Standard.
Uses the Masher's decided rules (D-092 to D-098): each provoking hit drags it one step toward the attacker; next to its target it slams the target's tile and the four around it, goblins included; Crippled, it can't step; Stunned, it doesn't answer; it can't be pushed or Commanded.

```
. . . . . . . . # # # # # # #      top path to the ledge (x5 to x7)
. # # # # ^ ^ ^ # # # # # # #
. # # # # ^ ^ ^ # # # # # # #      spike bay, open onto the bridge
. . . . . O O . . . . . c a E
J L M . . O O . . . . . c . E
# # # # # # # # # # # # # # #
  west bank   the bridge (2 wide)   far bank
```

The Masher fills the bridge. It can't be moved by force, only lured.

| Beat | What it teaches |
| --- | --- |
| 1. One poke, one step | Linda shoots it from the bank: it steps toward her. The preview shows the step |
| 2. Lure into the teeth | Linda on the ledge shoots down the bay's column: each hit pulls it a step north, into the spike bay. The last step must leave it *in* the bay but *not* next to her, or its slam lands on her tile |
| 3. Crush its own | On the far bank, the Claws gather on whoever crossed first. Mark Commands a Claw next to John (Shield Up); John takes the free Shield Dash (Command Shield Dash) or holds; when the Masher reaches John, its slam hits the Claws beside him too |
| 4. Hold it | Harmonic Slam (Crippled: no step) or Stunning Vault (Stunned: no answer) freezes it, so the rest can pass or hit it safely |

- **Several solves:** lure it into the bay and walk past; Vault over it with Mark and Dance John and Linda across (if the Dance and Vault can cross it: to check); sneak the long way, over the ledge and through the bay on a down turn, never ending a move next to it; or kill it (80 HP, every hit answered). Lure is fastest; killing pays its XP and costs HP.
- **Knobs:** Lucy in the squad (her follow-ups provoke it again, so answers chain); the bay with spikes on a different clock; Archers that shoot whoever stands on the ledge.

## F. The Weeping Pools (several Corruption pools, the Duos)

**Goal:** destroy every pool (`Entities destroyed`, all). Squad: John, Linda, Lucy, Mark. Tier: Standard.
Each pool spawns a Dark Claw every 3 turns (one alive per pool) until cleansed. Cleanse: 1 AP, from within 1 tile; one Cleanse destroys a pool.

```
# # P . . . # . . . P # #      top pair, behind the central wall
# . . . . . # . . . . . #
. . . . . . . . . . . . .
# #     . . . . .     # #
P .     . . . . .     . P      island pools beyond gaps
# #     . . . . .     # #
. . . . . . . . . . . . .
. . P . . . M . . . P . .      low pair, mirrored
. . . . J . U . L . . . .      John and Linda mirrored about the centre
```

The map is mirrored left to right, on purpose.

| Pool | Best answer | Showcase |
| --- | --- | --- |
| Low pair | **John–Linda Dance**: John steps up-left, Linda the mirrored up-right, both land next to a pool; each Cleanses | Dance: two units, two objectives, one action |
| West island | Lucy Blinks across the gap and Cleanses | Blink as mobility |
| East island | Mark Vaults across | Vault as mobility |
| Top-left | Mark Commands John 3 tiles north; John's free Shield Dash carries him the rest | **Command Shield Dash** as a long-range relay |
| Top-right | **Mark–Linda Footrace** to a point beside it: the winner hits the fresh Claw at ×1.5, the loser's +1 AP pays for the Cleanse | Footrace: pick the finish so the right one wins |

- **The clock:** first spawns can be staggered (low pair on turn 2, islands on 3, top pair on 4), so the order the player cleanses in matters.
- **Obvious play:** walk the family around the map together, cleansing one pool at a time while Claws keep coming.
- **Smart play:** split on turn 1 with the Dance and Blink, route moves through allies for Pass-by FTP to pay the second Duo, finish before most pools ever spawn.
- **Better result:** "no pool spawned twice" or "cleansed in 3 turns" is a clean, readable par (see Family Feats).
- **Knobs:** a pool on a spike tile (cleanse from beside it on a down turn); a pool next to a sleeping Black Claw; a near-mirror (one obstacle breaks the symmetry, so the Dance lands one short).

## G. Hold the Ring (protect while surrounded, Tempest Bloom, Catch & Return)

**Goal:** win by **either** surviving 6 turns (`Turn reached`) **or** cleansing all four pools (an `any` group). Loss: the protectee dies, or the family falls. Enemies act first, so it opens already surrounded.

```
          # . P . #
          # c . c #
          # . . . #
          # . @ . #           @ = north arm mouth (the Prism)
# # # # # # . . . # # # # # #
P . c . . . . L . . . . c . P
. . . . . . J R U . . . . . .
. . a . . . . M . . . . a . .
# # # # # # . . . # # # # # #
          # . . . #
          # . . . #
          # c . c #
          # . P . #
```

The protectee (`R`: Ryker, a stag or a wounded villager, narrative's call) is in the centre. Four arms, a pool at each end, more enemies each wave.

**The catch:** John's Role covers family only, so it can't shield the protectee. The family has to wall the arms instead.

| Arm | Answer | Showcase |
| --- | --- | --- |
| Linda's tile (top of the plaza) | Her row runs down both side arms, her column down the north and south arms: one tile watches all four. Her 2 Watch Shots a round (planned limit) can't cover four arms, which is the tension | Lanes |
| North | Lucy's Cyclone in the arm's mouth: nothing walks through it, and Linda's arrows (role arrows too) split inside it into the side files where Claws queue | **Tempest Bloom** (the Prism) |
| East | Mark Vaults behind the queue; Linda's arrow pierces the line, Mark catches it and sends it back through them | **Catch & Return** (the Gauntlet) |
| South | John with Shield Up plugs it, Lucy beside him (Sheltered, covered by his Role); an Archer pocket here can reuse Shield Flare | Shield Flare, Papa's Shelter |
| West | A second Cyclone once her cooldown is back (two can stand at once from turn 3) | Cyclone as wall |

- **Two ways to win:** turtle for 6 turns (safe, costs HP and FTP) or sortie to cleanse the pools (faster, leaves the protectee exposed). The level asks which risk the player prefers.
- **Command Shield Dash:** a Claw that slips into the plaza: Mark Commands it back down an arm, John's free dash follows and pushes the queue.
- **John–Linda Dance:** the side arms mirror each other, so one Dance can swap John and Linda between them.
- **Variants:** a Black Claw in one arm (ringing its bell pulls its pack off the protectee: the inverse taunt as a protect tool); the Masher coming down the wide arm (lure it into its own pack); Toba in the squad (taunt and heals).

---

## Pattern library

The patterns repeat across levels; each one varies with the same few knobs.

| Pattern | The question it asks | Answers | Knobs |
| --- | --- | --- | --- |
| **Throat** | Where do I stop them? | Cyclone, John with Shield Up, Harmonic Slam | Width 1 or 2; room for the Cyclone to drift; enemies act first |
| **Lane** | Who walks into Linda's row or column? | Her Role, Command (counts), a Black Claw pull, a bridge tile | Lane length against range 4 (6 with Longshot); two lanes crossing (a watch tile); her limit of 2 |
| **Pocket** | What can't I reach in a straight line? | Shield Flare, Explosive Crescendo, embers, Blink | Pockets at 1 or 2; Archers or Claws; one pocket not quite diagonal |
| **Spike clock** | When do I make them stand here? | Pushes (Shield Dash, Vault), Command, a Black Claw pull, a Masher lure | A band or scattered spikes; safe stones; two clocks out of step |
| **Bell** | Who should the pack chase? | John with Shield Up and Wrath; a lane; a Cyclone | Pack size; the radius of 5; two leaders sharing grudges; Lucy's stray sidewinders |
| **Bait and bash** | Where will its slam land, and who stands next to it? | John as bait; Command goblins in; Cripple or Stun | Room for the 2 × 2 to step; spikes; Lucy's follow-ups chaining answers |
| **Mirror** | Can two move as one? | John–Linda Dance | Exact or near mirror; the mirror flip; a blocker on one side |
| **Spread pools** | How do I split the family? | Dance, Footrace, Command plus free dash, Blink, Vault, Pass-by for FTP | Count; first-spawn offsets; islands; a pool on spikes |
| **Ring** | Which arms do I wall, which do I fight? | Cyclones, John, Linda's watch tile, a Black Claw pull, Toba's taunt | Two to four arms; turn limit or cleanse; enemies first |
| **Prism** | Where does the arrow split? | Tempest Bloom | Side alcoves; Cyclone drift; Role arrows |
| **Gauntlet** | Can the arrow come back? | Catch & Return | Line length against range; how Mark gets behind; Linda's damage falloff |

## Chains that make the player feel smart

1. **Command → lane → spikes → dash.** Mark Commands a Claw onto a spike tile in Linda's row the turn before the spikes rise. Linda's Role fires (Command moves count), the spikes strike at the enemy turn, and John gets a free Shield Dash to push its neighbour onto the next spike. One AP, four hits.
2. **The bell from the shield.** Shield Up, then John hits the Black Claw: the pack piles onto him, each hit stacks Wrath, and his next swing lands at up to +105%.
3. **It crushes its own.** The Masher's slam on John's tile kills the Claws Mark Commanded beside him.
4. **Mirror cleanse.** One Dance, two pools gone.
5. **Flare in the pockets.** One fireball, four Archers.
6. **The watch tile and the Prism.** Linda on one tile guards four arms, and her Role arrows split in the Cyclone.
7. **The boomerang.** An arrow down the Gauntlet hits every Claw twice.

## How a better solve pays

- **Already built:** HP, FTP and items carry between the levels of a mission (CR-12, CR-24, MI-21). A clean solve in one level is a stronger start in the next, so missions of 2 or 3 of these levels reward good play with no new code.
- **Proposed (new system, THJ's decision): Family Feats.** One optional goal per level, shown at the start and never ending the level: "No pool spawns twice", "The stag takes no damage", "Lucy is never hit", "Done in 4 turns". The objective system already has the conditions (`Turn reached`, `Unit dies`, `Entities destroyed`, groups); what's missing is an objective that doesn't end the level and pays when met. The reward could be Bond on `thj/home-test` (it fits Managing the Home as a Family: the family remembers what they did together) and XP or a material on `main`.

## Unlocks the showcases depend on

| Tool | Locked behind | Needed in |
| --- | --- | --- |
| Blink | Lucy's tree, 1 SP | A, F |
| Command (and so Command Shield Dash) | Mark's tree, 1 SP | E, F, G |
| Harmonic Slam | Linda's tree, 1 SP | E (optional) |
| Tempest Bloom | Family node, or the run upgrade | G |
| Catch & Return | Family node only | G |

Three ways to handle them, not exclusive:

1. **Tellings grant them** (A and B): it is their story, so they can do more than they can yet. Previews the tools before they are earned.
2. **A run-upgrade room before the level** that always offers the needed upgrade (works for Tempest Bloom; Catch & Return has no run upgrade yet).
3. **Solvable without, better with** (recommended for mid-game): the level has a plain solve, and the showcased tool is the smart one.

## To check before building

| # | Question | Why it matters | Where |
| --- | --- | --- | --- |
| 1 | Spikes: rise on round 3 and then every 4th round; strike on the rise and on step-on while up; 3 damage. Correct? | D and E are timed on it | `HazardEntity.cs`, `Spike.prefab`; play check |
| 2 | Does the enemy AI avoid raised spikes? Their move cost modifier is 0 | D works either way, but the hint differs | AI, play check |
| 3 | What does Lucy's Cyclone drift toward: the nearest unit, or the nearest enemy? | Throat and Prism need it to stay put or drift along the corridor | Cyclone prefab |
| 4 | Does each ember that reaches a shielded John flare on its own? | Multi-ember Flare variants in B2 and G | `JohnShieldRelay.cs` |
| 5 | Who wins the Footrace, and where do both end up? | F's top-right pool | `UnitsCooperationHandler.cs` |
| 6 | Does a caught arrow split in a Cyclone? Does Mark catch Linda's Role arrows? | G's east and north arms interact | `ProjectileCatchAndReturn.cs` |
| 7 | Can Vault and the Dance cross a gap or a 2 × 2 unit? Does a rock block Linda's arrow? | E's alternate solves; B2's pockets | Presets, play check |
| 8 | Are the Masher's decided rules (D-092 to D-098) built? | E assumes them | `plans/2026-10-20-masher-reckless-tank-tech.md` |
| 9 | Should John's Role cover an escort or protectee? Today it covers family only | G is designed around "no" | THJ |
| 10 | Can the player see which enemies Lucy's sidewinders may pick? | D's trap is only fair if it can be read | Previews |

## How to show layouts (formats)

| Format | Good for | Cost |
| --- | --- | --- |
| ASCII grids and tables (this doc) | The master copy: diffable, readable by every agent, maps to `GridCell - (x, y)` | Low |
| A visual board (an HTML page) | Discussion and sharing: coloured tiles, ranges, the intended solve turn by turn, "obvious play" against "smart play" | Medium; one page per level |
| Unity greybox prefabs | Playtesting: LevelBase, grid cells, placeholder units and hazards | Per level; a small editor tool could build the greybox from the ASCII grid (a new tool: THJ's call) |

## Related

- [Family systems](../design/gdd/family-systems.md) · [Combat rules](../design/gdd/combat-rules.md) · [Enemies](../design/gdd/enemies.md) · [Missions and structure](../design/gdd/missions-structure.md)
- [`plans/2026-10-20-masher-reckless-tank-design.md`](2026-10-20-masher-reckless-tank-design.md)
