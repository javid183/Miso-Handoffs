# Onboarding demo D3: paper levels for M1 to M4

Size: L    Tier: 3 (level content, story beats, roster; THJ approves each paper level before it's built)    Assigned to: miso-game-designer
Branch: `thj/onboarding-demo` (D-604, reverses D-602's "build on `main`"), scope this branch
Status: **paper levels written, waiting on THJ** (2026-11-23). The six groundwork questions are answered (D-605 to D-608, D-612, D-613; Cleanse D-614; stations D-618). New questions in [Questions for THJ](#questions-for-thj).

Parent plan: [`2026-11-22-onboarding-demo.md`](2026-11-22-onboarding-demo.md), Phase 3 (D3). Item source: [`design/demo-tweaks-snapshot.md`](../design/demo-tweaks-snapshot.md) (THJ's snapshot of the tweak doc, 2026-11-23), sections 1, 6 and 7. Worked example and history: [onboarding levels](onboarding/2026-10-26-onboarding-levels.md), [after-Hearth design](onboarding/2026-11-09-onboarding-after-hearth-design.md), [post-Hearth challenge](onboarding/2026-11-11-post-hearth-challenge-design.md), [Trail balance](2026-11-11-trail-balance-design.md).

## Why

Phase 3 builds four missions from paper levels (snapshot section 1, rows 7 to 11):

| Mission | Squad | Snapshot |
|---|---|---|
| M1 · Linda & Mark (The Ridge) | Linda, Mark | A Masher Goblin; Catch & Return is the answer to it (M1-01 to M1-03, X-26) |
| M2 · Lucy & John (The River) | Lucy, John | One level; Shield Flare; Dark Worms; ends on the Pile (M2-01 to M2-06) |
| M3 · Defence (replaces The Trail) | Linda, Lucy + John or Mark | One level: barriers, enemy waves, exploding mushrooms, a Black Claw; ends with Toba (M3-01 to M3-07) |
| M4 · 3 levels | Toba (fixed) + picks | An open cleanse fight with a Dark Shaman; a healing room; the boss and saving Ryker (M4-01 to M4-03) |

## Goal

Four paper levels that a builder can greybox without asking a design question, each within THJ's decisions, with every new-tech touch flagged.

## Acceptance criteria

- [x] Source grids of every level reworked (section 1, unchanged from the groundwork pass).
- [x] One paper level per mission with the skill's table (source, teaches, twist, squad, enemies, turns, first trigger, win/loss, cues, alert, FTP and clue, fallback, time), a grid block for every new layout, and the build lines.
- [x] Every distance a ★ relies on is counted on the grid in the text (not yet checked in a drawing: the coordinator renders, gate 7).
- [x] New to-checks in one table; new tech marked **!**.
- [x] X-20 and X-19 finalized against the snapshot.
- [ ] THJ's approval per mission.

## Scope

In: M1, M2, M3, M4 level 1 (grids); M4 level 2 (Mithra's Rest) and level 3 (the Queen) as change lists; the mission assets' shape; X-19, X-20.
Out: Home beats (M3-07, chunk 3.3), final text (`miso-narrative`), X-15 and X-27 (they change numbers, not layouts), M4-03's end sequence content.

## Touches

Systems: `GB_s2-ridge`, `GB_s1-river` (rebuilt from the blocks below, GUIDs kept, as D-502 did for the Trail), a new `GB_m3-defence`, a new `GB_m4-cleanse`, `DungeonSafeRooms/LevelDivineRelicRoom 1.prefab`, `Level3/Level3-C1.prefab`; mission assets `MS2 - The Ridge`, `MS1 - The River`, `M2 - The Trail` (becomes M3), `M4 - The White Mothers`; wiring tools `SearchWiring.Ridge/River/Trail`, `M4SquadSlots`, tests `SearchTrailTests`, `M4SquadPickTests`; `Unit_Toba.prefab` (`unlockedAfterMission`); **(core: AI)** barriers, chunk 3.0.
USPs: all four (see [USP check](#usp-check)).
Docs: see [Docs to update](#docs-to-update).

---

## 1. Source levels as read

All blocks below are the **verbatim output of `tools/level_to_grid.py`**, run 2026-11-22 on `main` by a read-only Explore agent (the designer has no shell). Titles carry the offset: grid x = prefab x + the title's x shift (for example "offset x-1" means prefab x = grid x + 1). y = 0 is the bottom row. `_` = no GridCell; `.` may hold a rock prop (props block nothing). Coordinates in my prose are **grid** coordinates of each block.

The tool's guidmap (`reward-tools/guidmap.json`) is out of date (no `GB_*`, potions, Home states); the tool only needs unit and terrain GUIDs, so nothing was missed in the grids. Rebuild it before the next tool use that needs level GUIDs.

### M1 source: The Ridge (`Content/Levels/Greybox/GB_s2-ridge.prefab`)

```grid id=src-ridge title="Source: GB_s2-ridge (offset x-1, y+0)"
. . . _ _ _ _ _ _ _ _ _ _
c . c _ _ _ _ _ _ _ _ _ _
. c . _ _ _ _ _ _ _ _ _ _
. . . _ _ _ _ _ _ _ _ _ _
. . . . _ _ _ _ _ _ _ _ _
. L M . . . c c . . . . .
_ . . _ _ _ _ _ _ _ _ _ _
```

| Item | As built (verified from the YAML unless marked) |
|---|---|
| Size | 31 cells: a 3-wide room (x 0..2, y 2..6, plus 3,2), the start row y1, a 1-wide corridor 3,1 → 12,1, two cells below (1,0 2,0) |
| Squad | Linda 1,1, Mark 2,1 (placed; `MS2 - The Ridge`: Linda + Mark fixed, no free slot) |
| Enemies | 5 Dark Claws: rush pack 0,5 / 2,5 / 1,4; corridor 6,1 / 7,1. No HP overrides (Tutorial ×0.6: about 9.6) |
| Tier, alert, turn order | Tutorial; no `LevelAlertSettings` (Unaware by default; the pack wakes by sight at start, C4b); **turn order overridden: enemies first** (D-353) |
| Objectives | Default: defeat all |
| FTP, locks | No `LevelStartFPFiller`, no `LevelAbilityLock` (so Catch & Return, Footrace and every ability are open; Catch & Return open by default, D-352) |
| Sequences | Intro and outro set; level start plays the shared sleeper panel (C4b; the after-Hearth plan cut it, not checked if removed) |
| Rewards | XP 30, Gold 20 + Steel 2 fixed |
| Not built | The `after-ridge` blocks of 2026-11-09 and 2026-11-11 (Early tier, family first, a Claw at 10,1) were never built (D-501 queued them; the Trail balance plan says the Ridge is untouched) |

### M2 source: The River (`Content/Levels/Greybox/GB_s1-river.prefab`)

```grid id=src-river title="Source: GB_s1-river (offset x+0, y+0)"
_ _ . . . . _ _ . . _ . _ . . _ _
_ . . . . . . _ . a _ . _ a . _ _
_ . . . . . c _ _ _ . . . _ _ . .
U J . . . c . . . . . . . . . . .
_ . . . . . c _ _ _ . . . _ _ . .
_ . . . . . . _ . a _ . _ . . _ _
_ _ . . . . _ _ . . _ . _ . . _ _
```

| Item | As built |
|---|---|
| Size | 79 cells: the clearing x 0..6, the ford x 7..14 with four 2 × 2 islands (8..9 × 5..6, 13..14 × 5..6, 8..9 × 0..1, 13..14 × 0..1) and the middle strip, the far bank x 15..16 |
| Squad | Lucy 0,3, John 1,3 (Papa's Shelter at start) |
| Enemies | Clearing: Dark Claws 5,3 / 6,4 / 6,2. Ford: Archer Goblins 9,5 / 13,5 / 9,1 on islands (they can step inside their island). No HP overrides |
| Tier, alert, turn order | Tutorial; Unaware by default; family first |
| Objectives | Default: defeat all |
| FTP, locks | No filler, no locks |
| Rewards | XP 30, Gold 20 + Timber 1 + Fabric 1 fixed |
| Not built | The `after-river` blocks (1-tile islands, alert, Early) |

### M3 source: The Trail (`M2 - The Trail.asset`: Trailhead → Blood **or** Tracks → The Pile)

As built: post-Hearth challenge revision 2 (C3, `9e9e0ca63`) at Standard tier (C4, `75d97cd05`, D-516). All four: all enemies start alert; Linda and Lucy placed, a deploy slot for the free pick (John or Mark); the Linda–Lucy Duo locked; no FTP filler. Mission: Lucy + Linda fixed, 1 free, Toba excluded; Health Potion 2, FP Potion 1; XP 40, Gold 5; completion sequence = the Yard (`Yard_Midnight_SequentialSequence`), initiation = the Map Table clue scene.

```grid id=src-trailhead title="Source: GB_m2-trailhead (offset x+0, y+0)"
c . . U L . . . c c . .
. c . . . . _ . . . . .
--
note 3,0 deploy slot
```

Front and back: Claws 0,1 / 1,0 behind, 8,1 / 9,1 ahead. Default objective (defeat all).

```grid id=src-tracks title="Source: GB_m2-tracks (offset x+0, y+0)"
_ _ . . . . . . . _
. . . . _ . . . . c
L U . . . c . b . .
. . . . . . _ . . c
_ _ . . . . . . c _
--
note 0,1 deploy slot
level hidden pack 9,3 9,1
```

Black Claw 7,2 (health factor 0.75 → 30), Dark Claws 5,2 / 8,0, hidden pair 9,3 / 9,1 revealed by a hidden "turn 1 reached (enemy)" stage. Then "Eliminate all enemies."

```grid id=src-blood title="Source: GB_m2-blood (offset x+0, y+0)"
_ _ _ _ c _ _ _ _ . _ _ _ _ c _ _ _ _ _
_ _ _ _ . _ _ _ _ c _ _ _ _ . _ _ _ _ _
_ _ _ _ c _ _ _ _ . _ _ _ _ c _ _ _ _ _
L U . . . . . . . . . . . . . . . . . .
. . . . . . _ _ . c . . . . . . _ _ . .
--
note 0,0 deploy slot
level hidden gullies 4,4 14,4
```

Reach objective: "Follow the blood. Two of you, to its end." (tiles 18,1 / 19,1 / 19,0), hidden kill-all; turn-2 gully pair. (The aggregation enum was read as "count 2", not looked up.)

```grid id=src-pile title="Source: GB_m2-pile (offset x+0, y+0)"
_ _ _ U L . _ _ _ _ _
. c . . . . . _ . . .
. _ _ . _ _ . . . c .
. . . . _ _ . . . . _
. . . . . . . . . . c
_ c . . . . . . . . _
--
note 5,4 deploy slot
level hidden west 1,4 1,0
level hidden east 9,3 10,1
```

"Search the pile." (any Bergson on 3,3 or 6,3) → both sides revealed → defeat all; the tally's "Still counting?" / "…No." ending (MI-28; its fade is saved per save).

### M4 source: `M4 - The White Mothers.asset` ("Into the Rootwell")

Roster: **Lucy + Linda fixed, 1 free pick, Toba excluded** (C5a); but five of its levels **place Toba themselves** (MI-3), so most M4 fights already field 4 Bergsons-side units (sisters, the pick, Toba). Items: Health Potion 3, FP Potion 4. Rewards: XP 120, Gold 20, 4 materials. Home state after: `M4 - HomeState`. Graph (straight line, two AND pass-through nodes): **LevelDomFight → Level2-C1-TArtEx → Mithra's Gift (Divine Relic room) → Level2-C2 → Level2-C3-1 → Level2-C3-2 → Level3-C1**. Labels still read (1/5) to (5/5) with a (4.5/5) (GDD MI Q4).

```grid id=m4-l1 title="Source: LevelDomFight (offset x-6, y+4)"
_ . . . . . . _
. L . . . . . .
. . . . . . . .
. U . . . . . .
_ . . . . . . _
--
note 2,2 deploy slot
note 6,2 Toba (as enemy)
```

Toba's duel (MI-25): "Defeat the stranger!", all alert; Ryker placed off the grid.

```grid id=m4-l2 title="Source: Level2-C1-TArtEx (offset x+0, y+5)"
_ _ _ _ . a . . a . _ _ _ _
_ P . _ _ _ _ . _ _ _ . . _
. . . c % . % c . . % . L .
. . c . . . c . % . . T U .
_ P . _ . _ _ _ _ _ _ . . _
_ _ _ _ . a . . a . _ _ _ _
--
note 11,3 deploy slot
note 13,3 Ryker
```

Two Corruption pools (1,4 / 1,1), 4 Archers on the top and bottom rims, 4 Dark Claws, 4 webs. "All units reach the exit." Not all-alert.

```grid id=m4-l3 title="Source: Level2-C2 (offset x+10, y-1)"
. . . . . _ _ _ _ _ _
. . . . c _ _ _ _ _ _
_ _ . . . . _ _ _ _ _
_ _ % . . . . % . P _
_ _ . . % . . . % . _
_ _ . c _ _ . . _ _ _
_ _ . . _ _ % . _ _ _
P . a . . % c % . . _
P . . c . b . . . . U
_ _ a . . . . . . T .
_ _ . . _ _ _ _ _ . .
_ _ P P _ _ _ _ _ . L
--
note 0,10 Deer
note 10,1 deploy slot
```

Five pools, a Black Claw, 4 Claws, 2 Archers, 7 webs, the Whitemother (Deer). "Reach the Pathmother." / "Whitemother must survive." / defeat all. No loss on a wipe (GDD MI Q12).

```grid id=m4-l4 title="Source: Level2-C3-1 (offset x+25, y-8)"
_ _ _ . . . _ . . _ _ _
_ _ _ . . . * . . . _ _
_ . U . . . . a . . . _
. T . . . . O O c . . .
. . . . . . O O c . . .
_ L . . . . . a . . . _
_ _ . . . . * . . . _ _
_ _ _ . . . _ . . _ _ _
--
note 0,4 Deer
note 2,3 deploy slot
```

**A Masher** (2 × 2 at 6,3), 2 Claws, 2 Archers, 2 exploding mushrooms; escort the fawns, the Pathmother must survive.

```grid id=m4-l5 title="Source: Level2-C3-2 (offset x+25, y-8)"
_ _ _ . P . _ P . P _ _ _ _ _ _ _
_ _ _ . . . * . . . . _ _ _ _ _ _
_ U . . . . c . a . . . _ _ _ _ _
. . T . . . . c . . . . . . . . .
. . . . . . . c . . s . . . . . .
_ L . . . . c . a . . . _ _ _ _ _
_ _ . . . . * . . . . _ _ _ _ _ _
_ _ _ . P . _ P . P _ _ _ _ _ _ _
--
note 0,4 Deer
note 2,3 deploy slot
```

Six pools, a Dark Shaman, 4 Claws, 2 Archers, 2 mushrooms; escort the new Pathmother. FTP +5 and heal 7 at load (GDD).

```grid id=m4-l6 title="Source: Level3-C1 (offset x-6, y+5)"
_ _ _ . . . _ _ _
_ _ . . . . . _ _
. . . . . . . . .
L T . . . . . . .
U . . . . . . . .
. . . . . . . . .
_ _ . . . . . _ _
_ _ _ . . . _ _ _
--
note 1,1 Ryker
note 1,3 deploy slot
note 8,3 Goblin Queen (1 x 2)
```

The Goblin Queen (EN-6; 320 HP at Standard), all alert, enemies first, Family Super Time on her death (MI-23). Its hero HP overrides are ignored (pre-rename fields, D-363).

`Mithra's Gift` (`DungeonSafeRooms/LevelDivineRelicRoom 1.prefab`): "Take the Divine Relic from the altar, then reach the exit." Not drawn: it's a safe room. **Read 2026-11-23: no `DivineRelicPickUp` is placed in either relic room prefab, and it has no `SafeRoomFunction`** (to check how the relic is given today, T-12).

---

## 2. Facts the paper levels rest on

Read 2026-11-23 from the assets by a read-only Explore agent (paths in its report; summarised here). V = verified in the asset or code; A = assumed.

| Fact | V/A | Where it matters |
|---|---|---|
| Hero move 3 (`radiusV` 3 × `Stat_SPD`; SPD's base value not found, assumed 1) | V formula, A value | Every route |
| **Masher:** 2 × 2, Unmovable, can't be swapped; walk 1 × SPD; attack and counter target a 4-way neighbour and slam a plus of 5 cells, every faction; damage 8 × `Stat_DMG` (enemy DMG by tier 1 / 0.75 / 0.5 / 1, so 6 at Early); sight 2; HP 80 × tier | V | M1 |
| **Masher counter:** answers the attacker by walking (its walk range only) to a cell next to them, or strictly closer; slams only if it ends next to them; can plow one-cell units out of its step | V | M1 |
| **A 2 × 2 can only step where two cells side by side are free** (its footprint) | V (footprint rule, skill) | M1's alcove |
| **Linda's arrow pierces a 2 × 2 and flies on**; each unit is hit once per arrow; falloff ×0.9 per earlier hit on that arrow (`onHitExtraModifier` 0.9) | V | M1 (C4b's "no falloff" and the Trail logs' "6 then 4" disagree with the code: T-1) |
| **Catch & Return copy is Linda's** (owner, stats); a fresh hit ledger, so a unit between them is hit out and back; the Masher answers both hits **once, against Linda**, after the action | V (code; not played) | M1 |
| Dark Worm: placed worm splits on death (a kill still splits) into 2 worms of the next size, on its cell and the nearest free cell: 12 HP / 6 dmg, then 6 / 4, then 4 / 2, which die normally. Move 1, melee | V | M2 |
| Exploding mushroom: set off by any hit, 1.5 s delay, flat 7 to every unit around it (radius 1 radial: read as the 8 cells), both sides; re-arms after 3 turns; blocks walking; the AI doesn't avoid it (not found) | V / A (shape) | M3 |
| Dark Shaman: move 3, bolt 2, heal 3, summon 2, 50 HP | V | M4-1 |
| Corruption pool: a Dark Claw about every 4th turn (interval 3, first at about turn 3) on a free neighbour, one alive per pool; pool health 10; **one Cleanse (50 × DMG, radius 1, diagonals likely) destroys it** | V | M4-1 |
| Healing Room heal: `SafeRoomFunction.healHpModifer`, per prefab; Anahita's Ashiyan = 0.5 × the HP cap (half of max HP, not a full heal: GDD MI-22 Q11 needs fixing) | V | M4-2 |
| `TurnStartActionPointLimit`: one chosen turn per level load, not "while a condition holds" | V | M3 lever |
| Hidden unit revealed onto a taken cell: moves to the nearest free cell | V | M2, M3 |
| Sisters' tally: on automatically when both sisters are deployed and the mission isn't excluded; the "Still counting?" fade is `SistersTally_FadeOut` (played inside the Pile's end sequence today), saved by asset name | V | M3 |
| `TurnReached` counts from the moment its stage starts; no built "every turn while X holds" sequence | V | M3's push |
| `MoveUnitSequence` moves GUnits only; a neutral GUnit (the Deer is a model) could be a stone; Toba's Wall has no HP and can't be moved | V | M3 |
| Mark's kit on the prefab: Fist Blitz, Move (walk), **Vault (open by default)**, Command (locked; node "Command", whose text starts "Mark commands an ally to move"), Cleanse, his Duos | V | M1, X-26 (T-2) |

### Rules every mission inherits

| Rule | For D3 | Source |
|---|---|---|
| Revenge, Pass-by | Back on after the Hearth | H-03, H-04 |
| Cleanse | **Locked in every level except M4 level 1** (`LevelAbilityLock` per level, or locked by default and unlocked in M4-1) | D-614, X-01 |
| Family Roles | As built (1 FTP each, no limit) until X-15 | X-15 |
| Linda–Lucy Duo | Locked through M3; first used in M4 (D-470) | D-470 |
| Turn order | Family first in every mission level (D-468 for the Ridge; the others are already family first) except the Queen (enemies first, as built) | D-468, MI-23 |
| FTP | Kept in each level's `LevelStartFPFiller` so X-28 is one sweep | Plan risks |
| Grounded arrows | Return to the quiver when a level is won, before its ending (H-08) | H-08 |

---

## 3. Paper levels

Coordinates in each block start at 0,0 (bottom left). `#` = no GridCell. Big units' footprints grow up and right from their anchor; the Masher is drawn on all four of its cells, as chunk 8 draws it (T-3: confirm the builder reads it as one Masher).

### M1 · Linda & Mark: "The wall that waits" (rebuilds `GB_s2-ridge`)

**Decided:** the Masher and Catch & Return beat replaces the corridor beat, in a widened stretch (D-605); Mark reaches the catch spot by a side path (D-606). The arrow does pierce a 2 × 2 (section 2), so the fallback isn't needed.

**The design move.** The Masher stands in a 2 × 2 alcove cut into the 1-wide corridor. With no second cell beside it in any direction, it **can't take a single step**: it can only slam whoever ends next to it. That makes its rule readable in one sentence ("never stand next to it") and makes the catch's value clear: Linda's plain arrows land under it and stay there (LI-6, LI-7), so plinking empties her quiver, while every caught arrow hits it twice and comes back.

**Why Mark stands next to it for a moment.** Linda's bow reaches 4. With a 2-cell Masher between them and one cell of space on Linda's side, Mark's catch tile is 4 from her and next to the Masher. So the rhythm is: Mark steps in (Move), Linda fires twice (two catches), Mark steps back out (Move). Nobody ends the turn next to it.

```grid id=s2-ridge title="M1 · The Ridge: the wall that waits"
c c c c # # # # # # # # #
. c . . . . . . . # # # #
. . . . # # # # . # # # #
. . . . # O O # . # # # #
. L M . . O O . . . . . .
--
cells 1,4 3,4 enemy hidden: back (turn 2 of the Masher stage)
zone 4,3 8,3 mark the ledge
arrow 3,3 8,3 8,0 mark dx=-8 the side path
arrow 3,0 7,0 linda dy=-8 bow
arrow 7,0 3,0 mark dy=8 caught, back
step 7,0 1
step 3,0 2
step 8,0 3
note 7,0 catch tile
note 8,0 rest tile
note 12,0 clue
level name The Ridge
level tier early
level alert all
level hidden back 1,4 3,4
```

The block has 5 rows, so y runs 0..4 (bottom row y = 0).

| Item | Plan |
|---|---|
| Source | `GB_s2-ridge`, rebuilt from this block (GUID kept); `SearchWiring.Ridge` updated (stages, sequences, clue props, HP). Today's corridor queue and Vault beat go |
| Teaches | **Catch & Return as the answer to the Masher** (M1-02), after **Watch and Mark's Counter** in the opening fight (M1-03) |
| Twist | A wall that never moves but punishes anyone beside it; plain arrows get stuck under it |
| Squad | Linda 1,0, Mark 2,0. Kit: no Vault (X-26), no Cleanse (D-614) |
| Cells | Room x 0..3, y 0..4 (20). Corridor y 0: 4,0, the Masher's alcove 5..6 × 0..1, then 7,0 to 12,0. Ledge 4,3 to 8,3, down 8,2 and 8,1 to 8,0. **Missing on purpose:** 4,1, 7,1 (no sideways step), 5,2 and 6,2 (no step up); there is no row below y 0 (no step down). So the Masher's only neighbours are 4,0 and 7,0 |
| Enemies | **Pack** (alert): Dark Claws 0,4, 2,4, 1,3, factor 0.8 (≈ 13). **Masher** anchor 5,0, alert, factor 0.45 (≈ 36 at Early). **Hidden `back`:** Dark Claws 1,4, 3,4, factor 0.8, revealed at the start of the Masher stage's second family turn |
| Beat 1: the pack (Roles) | Family first. 1,3 is 3 from Linda (1,0), 2,4 is 4 from Mark (2,0), 0,4 is 5 from Linda: all three reach a hero on enemy turn 1. At 13 HP nothing dies to one hit (bow 6, Explosive 8, Blitz 8), so enemy turn 1 comes: a Claw that ends its move in Linda's row 0 or column 1 within 4 **draws Watch** (her first real use: it was off in Memory 1), and a Claw that hits Linda within 2 of Mark **draws his Counter**. ★ Explosive Arrow on 1,4 from 1,0 (4 away) hits 0,4, 2,4, 1,3 and 1,4's empty cell: 8 on all three; Mark finishes one; Watch and the Counter take the rest on the enemy turn. ● Bow and Blitz one at a time: a round longer |
| Stage 1 → 2 | Pack dead → sequence: camera along the corridor to the Masher (its first-appearance close-up, EN-10, plays here: last, before control returns, H-01) → the setup lines (below) → objective **"Get past the Masher."** |
| The setup (M1-02: "a short setup shows how the Masher works") | Mark: "I'll knock it over." · Linda: "Don't stand next to it. Look." The player sees the rule on the board: the Masher is alert, so hovering it shows its counter preview (EN-2: path, cells, damage), and its only two neighbour tiles are the danger. Option b in Q-N2: a scripted Fist Blitz that shows a slam |
| Beat 2: the catch (distances on the grid) | Linda on **3,0**: the Masher's nearest cell 5,0 is 2 away, so she's never next to it, and it can't step to her. Her bow along row 0 reaches 4,0, 5,0 (Masher), 6,0 (same unit), **7,0**: 4 tiles, inside her 4. **Mark** goes up the ledge: from the room's 3,3 to 8,3 is 5 steps, then 8,2, 8,1, 8,0 (3 more): from the ledge's end, **one Move** drops him on the rest tile **8,0** (2 from the Masher's 6,0: safe). Each turn: Mark 8,0 → 7,0 (1 AP), Linda fires twice from 3,0 (the arrow passes the Masher, reaches Mark 4 away with an enemy between: the catch is offered, MA-3), Mark 7,0 → 8,0 (1 AP). Each catch hits the Masher out and back: 6 + 6 = 12, and the arrow returns to her quiver |
| Answers | ★ **Catch & Return** as above: 24 a turn, quiver full, the Masher dies in 2 of Linda's turns (36 HP). ● **Linda alone from 3,0:** 6 a shot, and each arrow lands under the Masher, locked until it dies: three arrows = 18, then she's empty (Encore: T-4). ● **Explosive Arrow** on the Masher from 3,0: 8, then a grounded arrow too (LI-4, to confirm). ✗ **Mark hits it** (Fist Blitz ends next to it): it slams Mark (6) and the plus around him; his Counter answers, which provokes another slam: a loop paid in FTP and HP (chain cap 10). ✗ **Ending the turn on 7,0 or 4,0:** it slams on its turn |
| Pressure | The hidden `back` pair arrives in the room on the stage's second family turn (camera and bark), acts the next enemy turn: from 3,4, three steps (3,3, 3,2, 3,1) put a Claw beside Linda on 3,0. So plinking alone gets her hit from behind; the catch kills the Masher first. Mark's Counter can't reach them from 8,0: Linda deals with them (Watch on column 3 or row 0) |
| Win / loss | Stage 1 the pack dead (hidden objective). Stage 2 "Get past the Masher." = the Masher dead; a hidden "turn 1 reached" stage reveals `back` (the Trail pattern). Stage 3 "Clear the ridge." (defeat all). Loss: default (family down) |
| Cues | Level start: one line each for the Roles (M1-03; placeholders, `miso-narrative`): Linda "Anything that steps into my line gets an arrow." · Mark "Anything that touches her answers to me." Stage 2: the setup lines; when Mark first stands on 7,0: Mark "Linda. Shoot at me." · Linda "Gladly." (G9-6/7). Arrival bark for `back` |
| First trigger | Watch and Counter on enemy turn 1 (pack within 4 of both); Catch & Return on the first Linda shot with Mark on 7,0 (the aim preview shows the return, CR-56) |
| Alert | `level alert all` (so the Masher's counter preview shows from the start; EN-2 hides it while Unaware) |
| FTP, clue | FTP full at start (Linda 2 + Mark 3 = 5; roles 1 each, Continuous Attack 1, 2, 3). Clue on 12,0: the end close-up (G9-3/4, as built, moved). Rewards as built |
| Fallback | If Mark never takes the ledge: Linda's plain arrows and Encore still kill it, slower, and the `back` pair hits her. Hint: a `GuidedAbilityHint` on Linda's bow while Mark stands on 7,0 (T-5); Mark's "Shoot at me." line already points at it |
| Time | ~5 min (beat 1 ~2 rounds, beat 2 ~3: Mark's walk is 2 turns from the room) |

**Note on "one Move" (D-606).** Strictly, no path around a 2 × 2 is one Move: the shortest loop from the tile beside it to the tile beyond it is 5 steps. The ledge keeps Mark 2 cells from the Masher all the way and ends one Move above the rest tile; the whole walk from the room is about 2 turns. If THJ wants it shorter, Q-N1.

### M2 · Lucy & John: "At me!" (rebuilds `GB_s1-river`)

**Decided:** one level (M2-01); John rushes in, is surrounded, and the player casts Shield Flare (M2-03: a `MoveUnitSequence` moves him, Lucy's embers on him are the play); Dark Worms (M2-05); the Pile at the end is Ryker's clue only (D-607). The ford Archers go: they were the old Shield Flare lesson, and the ring replaces them.

```grid id=s1-river title="M2 · The River: at me!"
# # . . . . # # # # # # # # # # #
# . . . . . . # . . . . . . . # #
# . . . . . c # c . c . . . . # #
U J . . . c . . . . . . . . . # #
# . . . . . c # c . w . . . . # #
# . . . . . . # . . . . . . . # #
# # . . . . # # # # # # # # # # #
--
cells 8,4 10,4 8,2 10,2 enemy hidden: ring
step 9,3 1
note 9,3 John rushes here
arrow 7,3 9,3 lucy ember John
arrow 9,3 8,4 lucy dy=-6 Flare
arrow 9,3 10,4 lucy
arrow 9,3 8,2 lucy
arrow 9,3 10,2 lucy
zone 15,2 16,4 note the Pile (props, no cells)
level name The River
level tier early
level alert all
level hidden ring 8,4 10,4 8,2 10,2
```

| Item | Plan |
|---|---|
| Source | `GB_s1-river`, rebuilt (GUID kept); the clearing's cells as built; the islands and Archers go; the ford becomes open shallows x 8..14, y 1..5, joined to the clearing by 7,3; the far bank holds the Pile (props on missing cells 15..16 × 2..4, as the Trail's Pile was drawn). `SearchWiring.River` updated |
| Teaches | **Shield Flare** (M2-02, M2-03), after **Lucy's follow-up and John's guard** in the opening fight (M2-06) |
| Twist | John charges ahead and is surrounded; the worm in the ring splits around him |
| Squad | Lucy 0,3, John 1,3 (Papa's Shelter at start, as built). No Cleanse |
| Enemies | **Clearing** (alert): Dark Claws 5,3, 6,4, 6,2, factor 0.8 (≈ 13). **Hidden `ring`** (revealed around John): Dark Claws 8,4, 10,4, 8,2, factor 0.45 (≈ 7); **Dark Worm** 10,2, factor 0.3 (≈ 8), splitting into 12 HP / 6 HP / 4 HP worms around its cell (built values, section 2) |
| Beat 1: the clearing (Roles) | Family first. 5,3 is 5 from Lucy. ★ John strikes a Claw within 3 of Lucy: **her follow-up** fires (2 × 3 on it, LU-5). Enemy turn: a Claw that targets Lucy within 2 of John **is taken by John's guard** (×0.5). ★ Lucy's Cyclone in the clearing's mouth (the arms pull and block, LU-3, LU-4). ● Sword and embers one by one |
| Stage 1 → 2 (M2-03) | Clearing dead → sequence: John "There, by the water. Fur." (he sees the clue) → `MoveUnitSequence` John to **9,3** → reveal `ring` (the four diagonal neighbours of 9,3) → `CastAbilitySequence` John's Shield Up → John "Lucy! At me!" · Lucy "*At* you?" (M2-02, placeholders) → **turn reset** (LSB `reset`, Memory 4's Hold pattern: a fresh family turn with AP) → `GuidedAbilityHint` on Lucy's Fire Embers until used → input on. Objective **"Help John."** (the ring dead) |
| Beat 2: the Flare (distances on the grid) | John on 9,3 under Shield Up. Each ring unit sits on a diagonal of 9,3, 1 away: Shield Flare's copies fly along the four diagonals and hit the first enemy within 2 (SY table), so **one Flare hits all four**. Lucy needs John within her embers' 3: **7,3** is 2 from John (inside his guard's 2, so a ring hit on her goes to John) and reachable in one Move from anywhere in the clearing at x ≥ 4; **8,3** is next to John (Papa's Shelter: one more ember, so one more Flare) but beside 8,4 and 8,2. ★ Lucy to 7,3 or 8,3, embers on John: the aim preview shows the four copies (CR-56). Damage: 4 a copy from the main ember (7 if every ember flares, T-6): two Flares, or one Flare + John's Sword, clear the Claws; the worm splits beside John and the follow-up and next Flares mop up. ● Embers on each ring unit directly (slower; the worm's splits pile up). ✗ John walks out of the ring (gives up the Shield Up turn, the ring follows) |
| Stage 3 | "Clear the river." (defeat all, the worm's children included) |
| Win / loss | Stage 1 the clearing dead (hidden); stage 2 the ring units dead; stage 3 defeat all. Loss: default |
| End (M2-04) | The Pile: camera to the far bank, the Pile close-up, Ryker's clue (prints, white fur, the axe-killed Claws of R7-4/5), John and Lucy's lines (placeholders). **No tally beat here** (Linda is absent; D-607) |
| Cues | Level start: John "Stay by me." (built) and one Lucy line about her follow-up (M2-06, placeholder). Stage 2 as above |
| Alert | All alert (the ring comes in alert) |
| FTP, clue | Full at start (John 5 + Lucy 3 = 8). Clue as above. Rewards as built |
| Fallback | The pulse on Fire Embers and the preview; if the player still doesn't ember John, the ring dies slower and John (24 HP, Shield Up 60%) takes it |
| Time | ~5 min |

**Worm risk.** Built, one worm becomes 2 + 4 + 8 = 14 children over its life (108 HP in all). One worm, in the Flare's reach, is the start value. If the play check shows a slog, Q-N4.

### M3 · Defence: "Hold the yard" (new `GB_m3-defence`, in the `M2 - The Trail` mission asset)

**Decided:** the stone moves by itself while the pusher stands at it (D-608); "Still counting?" plays here (D-607); roster as today: Lucy and Linda fixed, plus 1 pick (D-607). Snapshot M3-02: "the third member (John or Mark) rushes off ... pushes the stone off the cave that hides Toba's camp, for 3 turns to start"; M3-03 barriers (**!**); M3-04 the sisters compete with exploding mushrooms; M3-05 a Black Claw; M3-06 Toba appears and the family goes home.

**Who pushes.** The snapshot says the pick, John or Mark. THJ said it "might be Mark, not John". This level works for either, so I recommend **whoever is picked** (no roster change). The question is Q-N3.

```grid id=m3-defence title="M3 · Defence: hold the yard"
# # # # # T # # # # #
# # # c . @ . c # # #
# # . . . c . . . # #
# # . . . . . . . # #
# . . . L . U . . . #
# # . # # # # # . # #
c . . # # # # # . . c
. * # # # # # # # * c
c c # # # # # # # c b
--
cells 2,3 8,3 note barrier (HP): chunk 3.0
note 5,8 the stone; Toba hidden under it
note 5,7 push tile
cells 0,0 1,0 enemy hidden: w1
cells 10,0 9,0 10,1 enemy hidden: w2 (Black Claw 10,0)
cells 0,2 10,2 enemy hidden: w3
arrow 1,4 1,1 linda dx=-8 bow into the mushroom
arrow 9,4 9,1 lucy dx=8 the east mushroom
level name Defence
level tier early
level alert all
level deploy 5,4
level hidden toba 5,8
level hidden w1 0,0 1,0
level hidden w2 10,0 9,0 10,1
level hidden w3 0,2 10,2
```

| Item | Plan |
|---|---|
| Source | New level (`GB_m3-defence`), dressed like the Trail (H-11's first pass). **Mission asset:** keep `M2 - The Trail.asset` and make its graph one node, this level. That keeps everything keyed to it: the Yard as its completion sequence, the Map Table clue scene, its Home state, the tally, and the station unlocks after M3 (D-618: Bookshelf, Training Field, Cooking Cabinet). **If a new mission asset is made instead, the station rows and the Yard gate must move to it** |
| Teaches | Nothing new as a system: it's the sisters' exam and the first defence. New enemy rules: barriers (one sentence: "they break walls"), the Black Claw (met on the Trail before; now first here) |
| Twist | The third member leaves the sisters to it; they compete for kills (M3-04) until the end, where they stop |
| Squad | Linda 4,4, Lucy 6,4, the pick on the deploy slot 5,4 (John or Mark). Linda–Lucy Duo locked (D-470). No Cleanse |
| Cells | The yard x 2..8, y 4..6, plus 1,4 and 9,4 (the bulges), y 7 x 3..7 with the push tile **5,7**, the stone's cell 5,8. Two necks 2,3 and 8,3 (the barriers). Lanes: west 0,0, 1,0, 0,1, 0,2, 1,2, 2,2; east mirrored (10,0, 9,0, 10,1, 10,2, 9,2, 8,2). Mushrooms on 1,1 and 9,1 (cells, they block walking) |
| Enemies | **Opening** (alert, in the yard): Dark Claws 3,7, 7,7, 5,6, factor 0.8 (≈ 13). **Waves**, hidden groups in the lanes: **w1** west, Claws 0,0, 1,0; **w2** east, Black Claw 10,0 ×0.5 (≈ 20) + Claws 9,0, 10,1; **w3** one Claw each side, 0,2 and 10,2. Claws ×0.8. No pools: pools are the cleansable circles Cleanse answers in M4 (D-614), and the player can't cleanse here |
| Barriers (**!**, chunk 3.0) | On 2,3 and 8,3: an object with HP that blocks walking; an enemy whose way is blocked attacks it (M3-03). Start value 20 HP (about four Claw hits at Early, 4.5 each). The only way into the yard is through them. Rules the paper assumes and 3.0 must settle: enemies target it only when blocked; family attacks don't hurt it (Linda's pierce, the mushroom's blast: T-7) |
| The mushrooms (M3-04) | 1,1's blast covers 0,0, 1,0, 0,1, 0,2, 1,2, 2,2 (the west lane's mouth), not the barrier on 2,3 (2 away). Linda on the bulge **1,4** fires down column 1: across the gap 1,3, through a Claw on 1,2, into the mushroom on 1,1 (3 away, inside her 4), on to 1,0. Lucy on 1,4 reaches it with an ember (3). Mirror on the east (9,4 → 9,1). 7 to everything in the lane mouth + a bow hit (6) = 13, a kill: that's the tally race. Who gets credit for a blast kill: T-8. **Crossing the gap at 1,3 / 9,3 is not verified in code (T-15).** Fallback: make 1,3 and 9,3 present cells that block walking (a permanent untargetable blocker entity), never plain walkable cells, which would open a way into the yard around the barrier |
| Stages | **S1** "Clear the yard." (the opening three dead). → sequence: the pick: "There's a cave behind that stone." (placeholder) + camera on the stone. **S2** "*{Pick}*: push the stone." = a Bergson on 5,7 (T-9: the deploy slot's unit as the condition, else any Bergson) → reveal w1, line "Keep them off him!". **S3a, S3b, S3c** "Hold them off (1/3)", "(2/3)", "(3/3)": each = **the pusher on 5,7 (Reevaluate) and 1 turn passed since the stage began** → on complete: the stone shifts one notch (a prop swap or a short move, T-10), reveal the next wave (w2 after S3a, w3 after S3b). After S3c: the stone rolls away (sequence). **S4** "Finish them." (defeat all) |
| How the push reads (D-608) | One sentence: "While he stands at the stone, it moves; if he leaves, it stops." The queued stages give one notch per turn at most and pause while he's off the tile. Data only; no new tech. The pusher can still act from 5,7 (attack what reaches him, John's Shield Up, Mark's Blitz). Lever if it's too easy: he gets no AP while pushing, **which needs new code (!)**: `TurnStartActionPointLimit` sets one turn per level, not "while on the tile" |
| Distances | Breach to pusher: from the neck 2,3 to 5,7 is 7 steps, so a Claw that breaks a barrier needs two turns to reach him; the sisters on the bulges are 1 from the necks' yard side. From 5,4 (the deploy slot) to 5,7: 3, one Move |
| The Black Claw (M3-05) | w2, east. Hitting it calls every Dark Claw within 5 onto the hitter (EN-1). ★ Ring it from a sister's bulge (9,4, through the gap down column 9) so its pack turns on her and away from the barrier and the pusher (chunk 18, "the bell as a shield"). ✗ The pusher rings it (its pack comes for the stone) |
| Answers (the hold) | ★ Split the fronts: Linda on one bulge, Lucy on the other, each firing down her column into the lane and its mushroom. ★ Cyclone on a lane's mouth (2,2 or 8,2): its arms hold the lane and pull Claws into the mushroom's blast. ★ The bell, as above. ● Both sisters on one side: the other barrier falls a turn later and the pusher gets company |
| End | S4 won → end sequence (Q-N5 for the order): the tally alone on screen, Linda: "Still counting?" · Lucy: "…No." (`SistersTally_FadeOut`, moved here from the Pile) → camera on the cave → reveal Toba (non-hostile, `toba` group, after the stone is gone) → his lines: he knows the way to the Rootwell and where Ryker is (M3-06, placeholders) → fade, home (M3-07 is chunk 3.3) |
| Cues | Arrival barks and camera on each wave (the Trail's arrival pattern: input off, camera, reveal, bark, camera back); barks for the tally race (X-02/X-03 if built) |
| Alert | All alert; waves come in alert |
| FTP, items, clue | FTP full at start (`LevelStartFPFiller`). Items as the Trail (Potion 2, FP Potion 1). The clue is Toba. X-20's relic (Q-N6) would lie on 8,6 |
| Fallback | No caps. If the pusher leaves the tile, the stone waits; if both barriers fall, the yard fight still wins. A loss is the whole mission (one level) |
| Time | ~6 min (S1 2 rounds, hold 3, finish 1) |

### M4 · three levels

**Decided:** the Queen as built is the boss; seats Toba, Linda, Lucy fixed + 1 pick; the duel goes (D-613); Mithra's Gift becomes Mithra's Rest, a heal plus the relic (D-612); Cleanse only in level 1 (D-614).

**Mission asset (`M4 - The White Mothers`).** Graph: **`GB_m4-cleanse` → Mithra's Rest → `Level3-C1`**, labels (1/3) to (3/3). Roster: Toba, Linda, Lucy fixed, 1 free (John or Mark); Toba no longer excluded. `Unit_Toba.prefab`'s `unlockedAfterMission` becomes the M3 mission (`M2 - The Trail`). `M4SquadSlots` and `M4SquadPickTests` follow. The old levels (duel, C1-TArtEx, C2, C3-1, C3-2) leave the graph and stay as maps. Bond Threads §10 (Toba joins after M4) changes.

#### M4-1 · "The circles" (new `GB_m4-cleanse`)

Snapshot M4-01: an open level with a cleanse objective, room for Synergy planning, the demo's only real fight; a Dark Shaman.

```grid id=m4-cleanse title="M4-1 · The circles"
# # # . . . . . . . # # #
# # . . . P c . . . . # #
# . . . . . . . . . . . #
. . . . . . . . c . . P .
L . . . . . . c . s . . .
U T . . . . . . c . . . .
. . . . . . . . . . . . #
# . . . . P c . . . . # #
# # # . . . . . . . # # #
--
cells 8,4 7,4 9,4 8,5 8,3 linda Explosive on 8,4
arrow 4,4 9,4 linda dy=-8 Marks-Sisters
note 1,4 deploy slot
note 5,7 pool
note 11,5 pool
note 5,1 pool
level name The circles
level alert all
level deploy 1,4
```

| Item | Plan |
|---|---|
| Source | New level; dressing from Level2-C1-TArtEx (the old M4 level with pools) |
| Teaches | **Cleanse** (its only level, D-614) and the **sisters' first Duo** (Marks-Sisters, D-470), in the demo's one real fight |
| Twist | Three circles keep spawning while a Dark Shaman heals and summons behind a screen; the family must split to cleanse |
| Squad | Linda 0,4, Lucy 0,3, Toba 1,3, the pick on 1,4. Cleanse unlocked here only (Toba has none) |
| Enemies | Standard tier, no overrides. **Screen:** Dark Claws 7,4, 8,5, 8,3 around the empty 8,4; **Dark Shaman** 9,4 (heals within 3, summons within 2). **Guards:** Dark Claws 6,7 (north circle), 6,1 (south circle). **Circles:** pools 5,7, 11,5, 5,1 (a Claw about every 4th turn each, one alive per circle) |
| Setup turn | All alert, family first. Nearest enemy 7,4 is 6 from the pick's slot (1,4): its 4 steps end on 3,4, 2 short of a hero. The first turn is for positioning |
| Synergy planning (distances) | ★ **Explosive Arrow on 8,4** from 3,4 (5, inside its 5): the cross hits 7,4, 9,4 (the Shaman), 8,5, 8,3, 8 each. ★ **Marks-Sisters** (first use) from Linda on 4,4: row 4, 5 cells, 5..9: hits 7,4 and the Shaman 9,4, 12 × (×0.7 to 1.5). ★ **Tempest Bloom:** Lucy's Cyclone on 8,4 (Lucy on 5,4, 3 away): its Whirl hits all four touching enemies, and Linda's arrow down row 4 into it splits into the screen. ★ **Toba:** Provoking Presence pulls enemies within 3 two cells toward him (off a circle); Healing Marks with Linda. ● The pick's Synergy with a sister (Shield Flare or Catch & Return) on whatever closes |
| The circles | Each sits 5 to 11 from the start. Cleanse needs the cleanser within 1 (diagonals likely): north 5,7 from 4,6 / 5,6 / 6,6; south 5,1 from 4,2 / 5,2 / 6,2; east 11,5 from 10,4 / 10,5 / 10,6, behind the Shaman. One Cleanse each (pool health 10 vs 50 × DMG) |
| Win / loss | One stage, two objectives together: **"Cleanse the circles."** (all three pools destroyed) and **"Defeat the dark claws."** (defeat all). Loss: default |
| Cues | Level start: Toba points at the circles (line, placeholder); the Cleanse button pulses once (`GuidedAbilityHint`, WhenUnlocked) |
| FTP | Full at start (`LevelStartFPFiller` 99), so Marks-Sisters (2 FTP) is affordable on turn 1 |
| Fallback | No caps; circles keep spawning until cleansed (one alive each), so a slow player meets more Claws but never an endless flood |
| Time | ~8 min |

#### M4-2 · Mithra's Rest (reworks `LevelDivineRelicRoom 1.prefab`, no grid change)

| Item | Plan |
|---|---|
| What changes | Name "Mithra's Rest". Add a `SafeRoomFunction` with its heal (the Healing Room's component) to the relic room; place the Heavenly Sword pickup (`DR_PickUp_HeavenlySword`) on the altar (none is placed today, T-12); campfire props; `LevelStartFPFiller` 99 (the "refill" of M4-02). Objective: "Rest by the fire, take the relic, then go on." |
| Heal value (THJ's) | **Recommend 100% of max HP** (`healHpModifer` `baseFactor` 1.0 on `StatUB_HP`; the Healing Room uses 0.5). The boss is next, and the demo's last fight should start fresh. Q-N7 |
| Scene | A short campfire scene when the heal triggers: the family recovers; Toba's line (narrative tech, placeholder). Rations need the Home Kitchen: not in this demo (snapshot M4-02) |

#### M4-3 · The Goblin Queen (`Level3-C1`, no grid change)

| Item | Plan |
|---|---|
| What changes | Roster only: Toba placed (as built) is one of the fixed seats; the sisters placed; the deploy slot for the pick. Check that a fixed roster Toba and the placed Toba don't double (T-11). End sequence: saving Ryker (M4-03, narrative tech) |
| Values | Queen 320 HP at Standard, enemies first, Family Super Time on her death (as built). Lever after a timed play: 150 (the M10 value). The level's hero HP overrides are ignored (D-363) and stay that way |

---

## 4. X-20 and X-19 (final, against the snapshot)

### X-20 · Where a Divine Relic is introduced before M4

The snapshot's candidates: an M1, M2 or M3 reward, or a Home visit. A relic lasts the mission (PR-31), so a mission-end reward is gone before it can be used; a Home visit can show it but not use it.

**Recommendation: a walk-on Heavenly Sword in M3, on 8,6** (the yard's east corner, 2 steps off the hold line; picking it up costs a sister a move during the hold). Three uses, a 3 × 3 of 10 × within 5: it clears a lane mouth the turn a wave arrives. Mithra's Rest then gives it again before the Queen, so the player knows it. Data only (the pickup prefab). Q-N6.

### X-19 · Can a `thj/home-test` station join cheaply?

| Station (home-test) | What it needs on `main` | Cost | Adds before M4 |
|---|---|---|---|
| Kitchen, Workshop (sim), Study, Yard Lessons, Porch, Homestead | The Home sim (seats, day phases, resolve order) | High: the sim isn't on this branch | Little: the demo has no days |
| Stargaze, Hearth time, Dining Table at dusk | The sim's night and dusk phases | High | Bond and lines |
| Send-off scene, one Dining Table line set | A `DialogNodeSequence` (built) | Low: data and text | A family moment before M4 |

**Recommendation: no station.** If one Home beat is wanted, a **Send-off scene before M4** as a sequence (the family sends the squad, Toba among them). The stations that matter for the demo are `main`'s own (X-24, X-31; unlocked after M3, D-618).

---

## 5. To check (new; each decides a tile or a number)

| # | Question | Decides | Owner |
|---|---|---|---|
| T-1 | Linda's arrow falloff in play: code ×0.9 per earlier hit; C4b said none without the run upgrade; the Trail logs show 6 then 4 | Every pierce number (M1 uses only first hits) | implementer, read + play |
| T-2 | X-26 "Mark's skill tree unlocks Move instead of Vault": is "Move" his walk or Command ("commands an ally to move")? Either way Vault leaves his starting kit. If Command is in his kit at M1, it can't move the Masher (Immovable) but could move Linda | M1's kit | THJ / coordinator |
| T-3 | The grid builder places one Masher from four `O` cells (anchor bottom left) | M1 build | implementer |
| T-4 | What Encore does with arrows locked under a living Masher | M1's ● | play |
| T-5 | A `GuidedAbilityHint` condition "Mark on 7,0" | M1 fallback | implementer |
| T-6 | Which embers flare off John's Shield Up (main only, or each) | M2's HP values | play (level-chunks to-check 3) |
| T-7 | Barriers: do family attacks (pierce, mushroom blast, Cyclone) damage them? | M3, chunk 3.0 | 3.0 tech plan |
| T-8 | Who gets tally credit for a mushroom-blast kill (the sister whose hit set it off, or nobody)? | M3-04's race. If nobody, crediting it is new code (**!**) | implementer, read |
| T-9 | An objective condition on the deploy slot's unit (the pick) rather than any Bergson | M3 S2 and S3 | implementer, read |
| T-10 | The stone: a neutral GUnit on 5,8 (modelled on the Deer, Unmovable) removed or moved by sequence, or a prop over a cell another unit can't enter | M3 | implementer |
| T-11 | A roster-fixed Toba plus a level-placed Toba: one unit or two? | M4 levels | implementer, read |
| T-12 | How Mithra's Gift gives the relic today (no pickup placed in either prefab) | M4-2 | implementer, read |
| T-13 | `MoveUnitSequence` from wherever John stands at stage 1's end to 9,3 (path length, blockers) | M2 | play |
| T-15 | Do Linda's arrow and Lucy's ember travel across a missing GridCell (M3's 1,3 and 9,3)? Only play evidence so far, for the bow alone: the Trail tracks log shows an arrow from 4,2 to 4,6 across the gap row (post-Hearth challenge plan, evidence table). Lucy's ember and the code paths are not verified | M3's bulge shots. Fallback above: blocking cells instead of gaps | implementer, read the code + play |
| T-14 | Stage order on a turn: does a "1 turn passed" stage complete at the family turn's start (so the stone notch and the next wave come before input)? | M3 | play (the Trail's arrivals suggest yes) |

## 6. New tech (marked !) and small new pieces

| Item | Where | Size |
|---|---|---|
| **! Barriers** (an object with HP on the waves' path; a blocked enemy attacks it). Core: `AIUnitBrain` | M3 | Chunk 3.0: tech plan, review, full suite, its own commit; a branch if risky (D-602 exception, now off this branch) |
| **! Pusher has no AP while on the tile** (only if the lever is needed) | M3 | Small, not core |
| **! Tally credit for mushroom kills** (only if T-8 says nobody gets it) | M3 | Small, not core |
| Stone (neutral GUnit or prop), the push stages, the notch swaps | M3 | Data / a prefab variant (~) |
| Heal + relic in one safe room | M4-2 | Data (~): two existing components in one prefab |
| Cleanse locked in every level but M4-1 | All | Data |
| Everything else (stages, reveals, turn reset, `MoveUnitSequence`, `CastAbilitySequence`, hints) | M1, M2, M3 | Built |

---

## USP check

- **Family Roles:** strengthened. M1 and M2 each open with a fight where both partners' Roles fire on enemy turn 1 (Watch, Counter, the follow-up, the guard), with one line each (M1-03, M2-06). M3's pusher is protected by the sisters and his own Role.
- **Synergies:** strengthened. Catch & Return is the answer to the Masher (the plain play empties the quiver); Shield Flare is the answer to the ring; M4-1 sets up Tempest Bloom and the pick's Synergy.
- **Duos:** strengthened. The sisters' first Duo is a planned shot in M4-1 (D-470), right after "Still counting?" / "…No." and the Yard.
- **Managing the Home as a Family:** neutral on purpose. Keeping M3 in the Trail's mission asset keeps the Yard, the station unlocks (D-618) and the Home states as they are; X-19 adds no station.

## Questions for THJ

**Q-N1 (M1, D-606's "one Move").** Is a ledge that ends one Move from the catch spot (about 2 turns of walking from the room) what you meant?
- Context: no path around a 2 × 2 is one Move (5 steps minimum). The ledge keeps Mark 2 cells from the Masher and drops him one Move from the rest tile.
- Options: (a) the ledge as drawn; (b) Mark starts the level nearer the ledge (beat 1 shrinks); (c) the corridor shorter, so the ledge is 3 cells shorter.
- Recommendation: (a), with (c) if the walk feels long in play.
- Blocked: M1's build.

**Q-N2 (M1, the Masher setup's form).** How does "a short setup shows how the Masher works" play?
- Context: M1-02 asks for it. The counter preview already shows the slam when the Masher is hovered.
- Options: (a) camera, two lines and the preview (data, safe); (b) a scripted Fist Blitz by Mark that draws a real slam (6 HP on Mark; whether a sequence cast provokes the counter is untested).
- Recommendation: (a); (b) if cold players still walk Mark into it.
- Blocked: M1's stage-2 sequence.

**Q-N3 (M3, who pushes).** The pick (John or Mark), or Mark only?
- Context: the snapshot says the third member, John or Mark. You said it "might be Mark". The level works with either.
- Options: (a) whoever is picked; (b) Mark only (a roster change: Mark fixed in M3, and the pick goes).
- Recommendation: (a).
- Blocked: M3's roster and S2's condition.

**Q-N4 (M2, the worm's split).** Keep the built split (one worm becomes 14 children), or use the planned one for the demo?
- Context: EN-4 plans that the placed worm and its first split pop on any hit and only the last children have real HP (D-192); built, the chain is 108 HP. M2 places one worm.
- Options: (a) as built, one worm; (b) build EN-4's planned split first (a rule change, all worms); (c) as built, but the worm out of the ring (a side encounter).
- Recommendation: (a) and decide after the play check.
- Blocked: nothing now; the M2 play check.

**Q-N5 (M3, where "Still counting?" plays).** After the last kill and before Toba?
- Context: D-607 puts it in M3. The hold ends with the stone rolling away, then a "finish them" stage.
- Options: (a) end sequence: the tally line, then Toba; (b) when the stone rolls away, mid-fight; (c) after Toba, before going home.
- Recommendation: (a): the race ends on its own, then the story moves on.
- Blocked: M3's end sequence.

**Q-N6 (X-20).** Introduce the Heavenly Sword as a walk-on pickup in M3?
- Context: a relic lasts the mission, so a mission-end reward can't be used; Mithra's Rest gives it again in M4.
- Options: (a) in M3 on 8,6; (b) in M1 or M2; (c) only in M4's Rest.
- Recommendation: (a).
- Blocked: M3's item placement.

**Q-N7 (M4-2, heal value).** How much does Mithra's Rest heal?
- Context: the Healing Room heals 50% of max HP (not a full heal, as the GDD says); the Queen is next.
- Options: (a) 100% and FTP full; (b) 50% (as built) and FTP full; (c) 50%, no FTP refill.
- Recommendation: (a).
- Blocked: M4-2's values.

## Docs to update (if approved)

- GDD `missions-structure.md`: the mission table and level table (M1 to M4 as here), MI-3 and MI-25 (Toba joins after M3; no duel), MI-22 and Q11 (the Healing Room heals 50%, not full), MI-28 (the tally line in M3), M4's row; Source lines.
- GDD `enemies.md`: the Masher's first appearance; EN-4 if Q-N4 (b).
- GDD `characters/mark.md` (X-26), `characters/toba.md` (joins before M4).
- `design/level-chunks.md`: chunk 14's Vault row (X-26); a new chunk "the wall that waits" (a stuck Masher and Catch & Return); the knob "the anchor" (a hero who must stay put, M3); the facts in section 2 (Masher, mushroom, worm values) into the enemy and hazard references.
- `plans/onboarding/2026-10-26-onboarding-levels.md`: mark its `s1-river` and `s2-ridge` blocks superseded (this file reuses those ids to rebuild the same prefabs).
- `plans/2026-11-18-bond-threads-design.md` §10; `tech/onboarding-merge.md` (M4 rows).

## Risks

- The barrier AI (core) gates M3; until 3.0 lands, M3 can be greyboxed with the necks open.
- AI paths differ from paper (the pack's landing tiles in M1 and M2, the waves' targets in M3).
- The Masher's plow (D-573) and Catch & Return's single answer are read in code, not played.
- M3 is one level, so a loss replays the mission; there's no cap, so the risk is HP, not time.

## Gates

Design only. The coordinator renders and checks the four new grids (gate 7): `s2-ridge`, `s1-river`, `m3-defence`, `m4-cleanse` (plus the twelve source grids, unchanged). THJ approves each mission before chunks 3.1 to 3.4; chunk 3.0 (barriers) has its own tech plan first.
