# Onboarding demo D3: groundwork for the paper levels (M1 to M4)

Size: L (design groundwork)    Tier: 3 for every question below (level content, story beats, roster; THJ decides)    Assigned to: miso-game-designer
Branch: `main` (D-602), scope `all`
Status: **groundwork only, waiting on THJ** for (1) a local snapshot of the Claude Doc "Demo tweaks: Hearth to the end of M4" and (2) answers to the six questions below. No paper level is drawn here (D-603).

Parent plan: [`2026-11-22-onboarding-demo.md`](2026-11-22-onboarding-demo.md), Phase 3 (D3) and its open questions. Worked example and history: [onboarding levels](onboarding/2026-10-26-onboarding-levels.md), [after-Hearth design](onboarding/2026-11-09-onboarding-after-hearth-design.md), [post-Hearth challenge](onboarding/2026-11-11-post-hearth-challenge-design.md), [Trail balance](2026-11-11-trail-balance-design.md).

## Why

D3 needs one paper level per mission (M1 The Ridge reworked, M2 The River reworked, M3 a defence that replaces The Trail, M4 in 3 levels), each approved by THJ before it is built. The item texts (M1-01..M1-03, M2-01..M2-06, M3-01..M3-05, M4-01..M4-03, X-19, X-20, X-26) are in the tweak doc, which no agent session can open. This pass does what doesn't need them: it reads the source levels, lists what is true today and what the parent plan says changes, and sets out options for the six open questions.

**Rule kept here:** no item ID is given content the parent plan doesn't state. Where I infer what an item probably means, it is marked *reading* and goes in the to-check table.

## Goal

When the snapshot arrives, each paper level can be drawn in one pass: the sources are read, the facts are sorted into verified and assumed, and every open question has options with a recommendation.

## Acceptance criteria

- [x] Grid reads of every source level (Ridge, River, the four Trail levels, M4's six combat levels), with enemies, hazards, spawns and objectives noted.
- [x] Per mission: what's true today, what the plan says changes, the kit at that point, verified vs assumed facts, a to-check table.
- [x] M1-02, X-26, Q10, Q12, Q14 and Q15: 2 to 3 options each, how each changes the paper level, a recommendation, a USP line.
- [x] Provisional notes for X-20 and X-19.
- [ ] (Next pass) Paper levels, once the snapshot and the answers are in.

## Scope

In: source reads, constraints, options, the X-19 and X-20 notes.
Out: paper levels and grids for new layouts (next pass), the tweak doc's item texts, X-15 (Family Roles) and X-27 (new Duo resource), which are Phase 5 and change numbers, not layouts.

## Touches

Systems (read only here): `GB_s2-ridge`, `GB_s1-river`, `GB_m2-*`, `M4 - The White Mothers.asset` and its levels, `MS1`, `MS2`, `M2 - The Trail` mission assets.
USPs: all four (see each question).
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

Two Corruption pools (1,4 / 1,1), 4 Archers on the top and bottom rims, 4 Dark Claws, 4 webs. "All units reach the exit." Not all-alert. **The only M4 level with pools near the start: the likely "cleanse fight" (reading).**

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

`Mithra's Gift` (`DungeonSafeRooms/LevelDivineRelicRoom 1.prefab`): "Take the Divine Relic from the altar, then reach the exit." (Heavenly Sword, PR-30, PR-32). Not drawn: it's a safe room.

---

## 2. Per mission: today, the plan's changes, the kit, the facts

### What every mission inherits (after the memories)

| Rule | State for D3 | Source |
|---|---|---|
| Revenge | Back on after the Hearth (1.1 removes it only from memory kits) | Plan 1.1 (H-03 to H-05, X-01); RV-1 |
| Pass-by | Works after the Hearth (its panel stays cut until after M4) | Plan 1.1; after-Hearth "What to cut" |
| Cleanse | **Hidden in every kit except M4 level 1**, where a cleansable circle is | Plan 1.1 |
| Family Roles | As built (1 FTP each, no limit) until X-15; Role intros (M1-03, M2-06) built small | Plan Phase 5; FR-3, FR-4 |
| Duos | Linda–Lucy locked until M4 (D-470); other Duos open unless a level locks them | D-470; Trail levels |
| FTP | Will be redone by X-27/X-28 (new Duo resource): keep each level's FTP in its `LevelStartFPFiller` | Plan risks |
| Cyclone | **Redesigned since the Ridge and River were built** (Pulling Gale + Steer, merged 2026-11-22): it never moves on its own, pulls on its Whirl, blocks enemies, family passes; H-21 adds a Steer page after Lucy's first cast | LU-3 to LU-7, D-600 |
| Masher | Counter step plows units in its way (D-573; play check pending) | EN-2 |

### M1 · Linda & Mark (The Ridge reworked; M1-01 to M1-03, X-26)

**Today:** the 2026-11-02 Ridge: enemies first, a 3-Claw rush pack, then a 2-Claw corridor where Mark Vaults over the queue and Linda's arrow is caught (Catch & Return), Tutorial tier.

**The plan says changes:** a Masher and Catch & Return beat, perhaps replacing the corridor beat (M1-02, open); a Family Role element (M1-03 is listed under Family Roles); Mark has **Move instead of Vault** (X-26), so the old setup (Vault over the queue) is gone.

**Kit at M1** (first mission after the Hearth; M1 ∥ M2 in either order):

| Hero | Has | Doesn't have |
|---|---|---|
| Linda | Bow (6, pierce, reach 4 in a line), Explosive Arrow, Encore, quiver 3, Watch (Role) | Marks-Sisters (sister absent) |
| Mark | Fist Blitz (dash within 2, steps in on a kill), Continuous Attack, Atman's Focus, Counter (Role), Catch & Return, Footrace Duo (open unless locked), **Move (X-26)** | **Vault (X-26)**; Command (1 SP; Mark has 0 SP before his first mission's XP, *assumed*) ; Cleanse |

**Facts a paper level must respect:**

| Fact | V/A | Where |
|---|---|---|
| Catch & Return is offered only when the return copy would hit an enemy between Mark and Linda, from 2+ cells | V (GDD) | MA-3, D-560 |
| Watch arrows can be caught too, not only the bow | V (GDD) | MA-3, SY table |
| Masher: 2 × 2 (grows up and right), Immovable, counters every hit on the attacker, walking into range first; plows units in its counter step; sight 2 | V (GDD) | EN-2, EN-3, EN-13 table |
| Masher HP 80 at Standard, ×0.6 at Tutorial (48) | V (GDD) | Enemies table, CR-32 |
| The Ridge corridor is 1 wide: a 2 × 2 Masher can't stand in it | V (grid) | src-ridge |
| A Masher already stands in M4's Level2-C3-1: M1 would be its first appearance and needs its close-up (EN-10) | V (grid) / A (close-up built) | m4-l4, EN-10 |
| Hero move 3, Claw move 4 | V (logs, post-Hearth plan) | |

**To check (M1):**

| # | Question | Decides |
|---|---|---|
| M1-a | What do M1-01 to M1-03 say? | Everything below |
| M1-b | Does Linda's arrow pierce a 2 × 2 unit and fly on (hit once or twice)? | Whether the Masher can be "the queue" |
| M1-c | Does the return copy count as Linda's hit or Mark's for the counter, and does the Masher counter both hits? | Who the Masher walks to |
| M1-d | The Masher's own move and counter walk reach | Safe firing distance for Linda |
| M1-e | X-26: is Vault gone from the demo kit or moved to a node? | Whether a Vault answer may exist at all |

### M2 · Lucy & John (The River reworked; M2-01 to M2-06)

**Today:** the 2026-11-02 River: a sleeping clearing (3 Claws), Archers on 2 × 2 islands, Shield Flare optional, Tutorial, family first.

**The plan says changes:** "the rush is a sequence (`MoveUnitSequence`), the player casts Shield Flare" (chunk 3.2); M2-02 and M2-03 are Synergy items; M2-06 is a Family Role item; **the Pile moves here from The Trail** as Ryker's clue (risks; Q10).

**Kit at M2:** Lucy: Fire Embers (main + sidewinder), Cyclone + Steer, follow-up (Role), Papa's Shelter, Shield Flare. John: Sword, Shield Up, Shield Dash, guard (Role), Wrath, Hide and Seek (Duo, open unless locked). No Cleanse.

**Facts:**

| Fact | V/A | Where |
|---|---|---|
| Shield Flare: Lucy's fireball reaches John under Shield Up → copies on the 4 diagonals, each hits the first enemy within 2 | V (GDD) | SY table |
| Which embers flare (main only, or each) is still unknown | A | level-chunks to-check 3 |
| The tally needs both sisters in the level; the River has only Lucy | V (GDD) | MI-28 |
| The "Still counting?" fade is saved per save | V | MI-28, plan risks |
| A scripted rush (`MoveUnitSequence`) cancels with a warning if the destination is blocked | V | D-404 (Memory 4) |
| The old River ★ "Cyclone splits the rush" assumed the drifting Cyclone; now it pulls and blocks | V | LU-3, LU-4 |

**To check (M2):** M2-a what M2-01 to M2-06 say; M2-b whether the Pile prop set and its search stage move as a block from `GB_m2-pile` (wiring `SearchWiring.Trail`) or are rebuilt; M2-c whether the River keeps its islands (the 11-09 "1-tile islands" rule, so Archers can't step off the Flare diagonals).

### M3 · Defence (replaces The Trail; M3-01 to M3-05, plus M3-06, M3-07 in chunk 3.3)

**Today:** The Trail (four levels above), Standard tier, sisters + pick, the Pile ending, the Yard after it.

**The plan says changes:** a defence level built on the Trail prefabs; **barriers** (M3-03): an object with HP on the waves' path, which a blocked enemy attacks (core AI, chunk 3.0); a **stone push** (Q12); Toba's appearance (M3-06) and the Home beat after it, then the Linda–Lucy scene (M3-07: is it today's Yard?).

**Kit at M3:** the M2 kit of whoever comes (roster not stated in the plan: *assumed* sisters + pick, as the Trail). Toba appears here; whether he fights is not stated.

**Facts:**

| Fact | V/A | Where |
|---|---|---|
| Corruption pools (`CP_Spawner`) give a wave source as data (specific turns, one alive per pool) | V | missions-structure; Memory 4 |
| Hidden groups revealed by stages give announced waves (the Trail's turn-2 pattern) | V | src-tracks, src-blood |
| "Unit on tiles" with Reevaluate can hold a stage on a hero standing somewhere (Memory 4's John on the mouth) | V | MI-18, MI-30 |
| Toba's Wall already blocks walking (3 cells, 3 turns, untargetable) | V (GDD) | Toba abilities |
| A level `LevelHomeDefence` ("Defend Home") exists on `main` | V (GDD) / A (content) | MI-27 table |
| Barriers with HP need the core AI change | V (plan) | Chunk 3.0 |

**To check (M3):** M3-a what M3-01 to M3-05 say, and who "he" is in the stone push; M3-b the roster; M3-c whether `LevelHomeDefence` is worth reading as a source; M3-d whether the tally shows in M3 (per-level eligibility) if Q10 moves "Still counting?" here.

### M4 · 3 levels (M4-01 to M4-03)

**Today:** six fights + Mithra's Gift (above), Standard tier, starting with Toba's duel.

**The plan says changes:** a Mission asset with **3 levels: the cleanse fight, the rest level, the boss**, then the end sequence; **roster Toba fixed + picks**; Cleanse only in level 1; the sisters' first Duo here, after the Yard (D-470); C5a's roster and `M4SquadPickTests` change; the Bond Threads plan's demo section (Toba joins after M4) changes.

**Facts:**

| Fact | V/A | Where |
|---|---|---|
| The existing relic room is named **"Mithra's Gift"** and already sits between M4's fights | V | Mission asset, safe-room prefab |
| Main's Healing Room ("Anahita's Ashiyan") heals the whole family once at its shrine (0.5 × the HP cap stat: a full heal, Q11) | V (GDD) | MI-22 |
| The campfire Rest Room (10% heal, rations) is `thj/home-test` only and uses the Home sim | V (GDD) | MI-15, Demo Spec |
| Level2-C1-TArtEx has 2 pools near the family's start; Cleanse deals 50 × to Corruption within 1 | V | m4-l2, Mark Cleanse row |
| Five M4 levels place Toba already; the roster excludes him | V | Mission asset, grids |
| Goblin Queen 320 HP, enemies first, boss bar, FST on her death; 150 HP in M10 is a precedent for a lower value | V (GDD) | EN-6, MI-23 |
| Toba joins after M4 today (`unlockedAfterMission`); joining before M4 changes that, MI-3, MI-25 (the duel) and the Bond Threads demo section | V | MI-3, Toba sheet |

**To check (M4):** M4-a what M4-01 to M4-03 say; M4-b whether level 1 is Level2-C1-TArtEx reworked or a new level; M4-c whether the safe room's heal value can be set per room (Healing Room uses the HP cap stat).

---

## 3. Open questions: options and recommendations

All six are THJ's (Tier 3). Each ends in the five-part form in [Questions for THJ](#questions-for-thj).

### M1-02 · Does the Masher and Catch & Return beat replace the corridor beat?

| | A. Replace the corridor beat | B. Add it after the corridor | C. Keep the corridor; no Masher in M1 |
|---|---|---|---|
| Paper level | The corridor widens to 2 rows for one stretch; the Masher stands there between Linda's side and Mark's; Catch & Return hits it out and back with one arrow | Today's queue beat, then a Masher room at the end (x 9..12 widened) | Today's layout, Claw queue only; the Masher first appears in M4 (Level2-C3-1) |
| Player experience | One Synergy beat with a twist: the thing between them hits back, so the catch's double hit from range is the clean answer | Two Synergy beats: more practice, longer | Familiar, no new enemy |
| Rules to learn | +1 enemy (counter, Immovable) | +1 enemy | 0 |
| Time | Same as today (~4 min) | +2 to 3 min | Same |
| Risk | Rests on M1-b and M1-c (pierce through a 2 × 2, counter on the return) | Time budget | M4's Masher arrives untaught |
| USP | Synergies + (the catch is the best answer, not an option) | Synergies + | Neutral |

**How the beat would read under A** (to confirm with M1-b to M1-d): Linda fires along the corridor from beyond the Masher's counter reach; Mark stands past it; the arrow hits it, Mark catches, the return hits it again: two hits for one arrow, back in her quiver. Firing from too close draws the slam (and its plow). The counter preview (EN-2) shows the risk before the click once it's awake.

**Lean: A.** One beat keeps M1 short, and the Masher earns its first appearance here, before M4 needs it. If M1-b fails (the arrow stops at a 2 × 2), the fallback is B with Claws in the queue and the Masher at the end.

### X-26 · How does Mark set up the catch without Vault?

| | A. Mark starts past the queue | B. A loop: a side path behind the blocker | C. They come between: the pair splits, enemies walk into the lane |
|---|---|---|---|
| Paper level | The level places Mark at the corridor's far end (like Memory 4's Mark, who starts apart) | A ledge or side passage from the start room rejoins the corridor past the blocker, one Move (3) away for Mark | Linda and Mark start or end the first beat at the corridor's two ends; awake enemies walk into the lane between, and Watch arrows get caught on the enemy turn |
| Player act | None: the setup is given | One move the player chooses, shown by the move ghost | Positioning before the enemy turn; the catch on a Role arrow |
| Teaches | The catch only | "Get on the far side": a habit the player keeps | Role + Synergy together |
| Rules | 0 | 0 | 0 |
| Risk | No decision in the setup | Map grows; a loop can be used by enemies too | Needs awake enemies and AI paths that cooperate (to check) |
| USP | Synergies (weak) | Synergies + | Synergies + Family Roles + |

**Lean: B**, with C as what the layout gives for free (a Watch arrow along the corridor while Mark stands past the blocker is caught too). B keeps the setup a choice the player makes with the plain Move X-26 leaves him, and costs no rule.

### Q10 · The Pile in M2 is Ryker's clue only; does "Still counting?" stay in M3?

| | A. Pile = clue in M2; "Still counting?" moves to M3's ending | B. Pile and its line both in M2 | C. Pile = clue in M2; the line moves to M4, before the first sisters' Duo |
|---|---|---|---|
| Paper level | M2's Pile is a search beat with the clue and no tally; M3's last fight ends with the sisters back to back | Needs Linda in M2 (roster change) or a line without the tally | M2 as A; M4 level 1 (or the boss) opens with the line |
| Story | The tally dies just before the Yard (M3-07), then their first Duo in M4: the D-470 arc, in order | Breaks the joke: Lucy alone can't "count" | The line and the Duo touch; the Yard comes before the line, which is backwards |
| Needs | Both sisters in M3; M3 eligible for the tally; the saved fade still keyed once | A roster change | Tally eligible in M4 (today M4 shows no tally, D-448) |
| USP | Duos + (sets up the first sisters' Duo), Home + (the Yard follows) | − | Duos, neutral on Home |

**Lean: A**, if M3's roster has both sisters (M3-b). Otherwise C.

### Q12 · The stone push: his actions each turn, or by itself once he's there?

"He" isn't named in the plan (M3-a).

| | A. His actions each turn | B. By itself while he stands there | C. By itself, and he has no AP while there |
|---|---|---|---|
| Rule in a sentence | "Spend his action on the stone to move it one tile" | "While he stands at the stone, it moves one tile each turn" | "While he pushes, the stone moves each turn and he can't act" |
| Build | **New tech**: an interact ability or a per-AP trigger | Data: queued stages "he on the push tile" (Reevaluate) whose onComplete moves the stone one tile, Memory 4's pattern | B plus `TurnStartActionPointLimit` per turn (to check it can be set mid-level) |
| Player experience | A real trade every turn (push or fight) | The cost is his position: he's pinned, the others must cover him | A hard anchor; the others carry the fight |
| Risk | Cost, one more button | Too easy if he can still fight from the tile (lever: C) | Feels passive |
| USP | Neutral | Family Roles + (the others protect the anchor: John's guard, Watch lanes), Synergies neutral | Family Roles + |

**Lean: B.** One sentence, no new tech, the shape THJ designed and liked in Memory 4 (John holding the den mouth). C is its lever if play shows no pressure.

### Q14 · Is "Mithra's Rest" the campfire Rest Room?

| | A. Mithra's Gift reworked into Mithra's Rest | B. Main's Healing Room, renamed and given a campfire look | C. Port `thj/home-test`'s campfire Rest Room |
|---|---|---|---|
| Paper level | The existing room slot in M4's graph; heal at the altar (and the relic stays, if X-20 wants it re-given) | A new node: the Healing Room prefab with new art and name | Port the room; rations need the Home sim |
| Build | Data + art: add the Healing Room's shrine function to the relic room | Data + art | Home-sim code on `main` (not cheap) |
| Heal | Set by the shrine (full today, GDD Q11) | Full today | 10% |
| USP | Home neutral; Duos neutral | Neutral | Home + in name only without rations |

**Lean: A**, since the name already points at it ("Mithra's"), the slot exists, and it can carry the relic too. The heal value (full or partial) is THJ's call; full suits a demo before a boss.

### Q15 · The Goblin Queen as the boss, with 4 seats and Toba fixed?

| | A. Queen as built; Toba, Linda, Lucy fixed + 1 pick | B. Queen at a lower HP (M10's 150 as the reference); same seats | C. Toba fixed + 3 free picks |
|---|---|---|---|
| Paper level | Level3-C1 as is; the deploy slot stays for the pick; Toba moves from excluded to fixed (or stays placed) | As A, HP tuned | Three deploy slots; Linda and Lucy no longer guaranteed |
| Story | The family plus the newcomer face the Queen | Same | Same |
| Fit | Keeps D-470 (the sisters' first Duo needs both); 4 units already fight in today's M4 | Shorter fight | Can lose the sisters' first Duo |
| Risk | 320 HP may drag at demo pace | Tuning only | Breaks D-470 |
| USP | Duos + (first sisters' Duo guaranteed), Family Roles neutral (Toba has no Role, FR-7) | Same | Duos − |

**Lean: A**, with B's HP as the first lever after a timed play. Also needed: Toba's `unlockedAfterMission` and the duel (LevelDomFight) go, so MI-3, MI-25 and the Bond Threads demo section change (plan 3.4).

---

## 4. Provisional notes (until the snapshot arrives)

### X-20 · Where a Divine Relic could be introduced before M4

Facts: a relic is a walk-on pickup, 3 shared uses, lasts the mission (PR-30, PR-31); Heavenly Sword hits every enemy in a 3 × 3 within 5 for 10 × (PR-32); Mithra's Gift already gives it in M4.

| Option | Why | Cost |
|---|---|---|
| **M3 defence (lean)** | A wave-clearing tool where waves are the question; the pickup can sit off the defended line, so taking it costs a move away (a choice); M4's room then gives it again, so the player knows it | Data: the pickup prefab placed in the level |
| M1 or M2, near the end | Earlier, but those levels already teach a Synergy each | Data |
| A Mithra's Gift node inside M3 | Teaches the room too | A mission-graph node; M3 grows |

### X-19 · Which `thj/home-test` station could join cheaply

Every home-test station that resolves through seats and day phases (Kitchen, Workshop, Study, Yard Lessons, Porch, Stargaze, Hearth time) needs the Home sim, which `main` doesn't have (`branches.md`, `tech/onboarding-merge.md`). **Lean: none as a station.** If one beat is wanted, the cheapest is presentation only: the **Send-off scene** before M4, or one **Dining Table** line set, each a `DialogNodeSequence` (the player exists on `main`). Re-check against X-19's text, X-24 (Kitchen and stat-up stations) and X-31 (Home stat upgrades).

---

## USP check (for the D3 pass as a whole)

- **Family Roles:** M1-03 and M2-06 are built with the Roles as they are (X-15 later); Q12's B makes the others protect an anchor.
- **Synergies:** M1's catch becomes the best answer to the Masher (M1-02 A) and a positioning habit (X-26 B); M2's Shield Flare is the cast after the rush.
- **Duos:** Q10 A and Q15 A keep the sisters' first Duo in M4, after the Yard (D-470).
- **Managing the Home as a Family:** Q10 A keeps the Yard right after the tally dies; X-19 stays presentation only.

## Questions for THJ

**Q-D1 (M1-02).** Does the Masher and Catch & Return beat replace the Ridge's corridor beat?
- Context: the corridor is 1 wide (the Masher is 2 × 2); M4's Level2-C3-1 already has a Masher, untaught.
- Options: A replace (widen one stretch); B add after (+2 to 3 min); C keep the corridor, no Masher in M1.
- Recommendation: A, with B as the fallback if the arrow stops at a 2 × 2 (to check M1-b).
- Blocked: M1's paper level.

**Q-D2 (X-26).** Without Vault, how does Mark get past the blocker for the catch?
- Context: X-26 gives Mark Move instead of Vault; today's beat relies on Vault.
- Options: A he starts past it; B a side path, one Move away; C the pair splits and enemies walk between.
- Recommendation: B (C comes with it).
- Blocked: M1's layout.

**Q-D3 (Q10).** The Pile in M2 is Ryker's clue only, and "Still counting?" moves to M3's ending?
- Context: the tally needs both sisters; the River has Lucy and John; the fade is saved per save.
- Options: A clue in M2, line in M3; B both in M2 (roster change); C clue in M2, line in M4.
- Recommendation: A if M3 has both sisters, else C.
- Blocked: M2's and M3's paper levels; chunk 3.2's tally handling.

**Q-D4 (Q12).** The stone push: his action each turn, or by itself while he stands there?
- Context: Memory 4's "John holds the mouth" is the same shape and is data only.
- Options: A his action (new tech); B by itself while he's on the tile; C B plus no AP while there.
- Recommendation: B, C as the lever.
- Blocked: M3's paper level, and whether chunk 3.3 needs new tech.

**Q-D5 (Q14).** Is "Mithra's Rest" the existing Mithra's Gift room, turned into a rest?
- Context: the relic room is already "Mithra's Gift" in M4's graph; main's Healing Room heals fully; the campfire Rest Room needs the Home sim.
- Options: A rework Mithra's Gift (heal + relic); B the Healing Room renamed; C port the campfire room.
- Recommendation: A; heal value yours (full suits the boss next).
- Blocked: M4 level 2.

**Q-D6 (Q15).** The Goblin Queen as the boss, 4 seats: Toba, Linda, Lucy fixed + 1 pick?
- Context: today's M4 already fields 4 (levels place Toba); D-470 needs both sisters in M4.
- Options: A Queen as built, those seats; B same seats, lower HP; C Toba + 3 free.
- Recommendation: A, B's HP as the first lever.
- Blocked: M4 level 3, chunk 3.4's roster and tests.

## What the next pass needs from the tweak doc

The text of M1-01 to M1-03, M2-01 to M2-06, M3-01 to M3-05 (and who "he" is in the stone push), M4-01 to M4-03, X-19, X-20, X-26, and the M3 roster; plus THJ's answers to Q-D1 to Q-D6.

## Docs to update (if approved, next pass)

- GDD `missions-structure.md`: the mission table and M4 row (3 levels, roster), MI-3 and MI-25 (Toba joins in M3, no duel), MI-28 (where the tally's line plays), the M2/M3 rows; Source lines to the new levels.
- GDD `enemies.md`: the Masher's first appearance (EN-10 close-up) if M1-02 A.
- GDD `characters/mark.md` (Move vs Vault, X-26) and `characters/toba.md` (joins before M4).
- `design/level-chunks.md` (coordinator or me, once approved): chunk 14's Vault row (X-26), a Masher + Catch & Return chunk, the anchor knob (Q12).
- `plans/2026-11-18-bond-threads-design.md` §10 (Toba in the demo).

## Risks

- The tweak doc's items may contradict a lean here: every lean is marked as one, and nothing is drawn.
- M1-02 A rests on two unverified behaviours (M1-b, M1-c).
- The Masher's plow is not play-checked (D-573).
- M4's 320 HP Queen at demo pace.

## Gates

Design only. Next pass: paper levels with grids, rendered and checked by the coordinator (gate 7), THJ's approval per mission before chunks 3.1 to 3.4.

**Grids in this file (for rendering):** `src-ridge`, `src-river`, `src-trailhead`, `src-tracks`, `src-blood`, `src-pile`, `m4-l1` to `m4-l6`. All are tool reads, not designs.
