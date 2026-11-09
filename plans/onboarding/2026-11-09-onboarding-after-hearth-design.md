# Onboarding after the Hearth: challenge what was taught

Size: L    Tier: 3 (level design and game feel of the first hour, Home flow, two small all-scope UI rules)    Assigned to: miso-game-designer
Branch: `thj/onboarding` (THJ's working main, D-396). Rules marked **(all)** below should apply on every branch.
Status: waiting on THJ

Source: [`playtests/2026-11-09-pacing-check.md`](../../playtests/2026-11-09-pacing-check.md), findings P1 to P6 and THJ's answers of 02:13. Builds on the approved [first-hour design](2026-10-25-onboarding-first-hour-design.md), the [paper levels](2026-10-26-onboarding-levels.md) and the C3 to C5 build plans. Runs alongside [`plans/2026-11-09-family-roles-rethink-design.md`](../2026-11-09-family-roles-rethink-design.md) (read 2026-11-09; it recommends option C, "Kept AP", behind a dev switch, with "lock as built" as the fallback). This plan redesigns no Family Role rule and holds under either outcome; every place that depends on it is in [Family Role dependencies](#family-role-dependencies).

## Why

THJ's timed play (2026-11-09): the Hearth works as a tutorial, but nothing after it challenges what it taught. The River, the Ridge and The Trail are too easy ("you do not feel the need of abilities"), The Pile is the weakest level, the Trailhead walk is vague, and the first hour carries "too many mechanics with too little challenge". Timing is fine (about 42 minutes to the end of The Trail) and must stay fast.

## Goal

After the Hearth, every level first challenges what the player already has, and anything new it teaches is one small pair Synergy that is then challenged too, in fewer and tighter levels, with Hearth → M4 send-off still at about 45 minutes at THJ's pace.

## Acceptance criteria

- [ ] No tutorial panel after the Hearth. Post-Hearth teaching is one spoken line or a goal tile per new thing (the Asleep panel, its sight beat, the River and Ridge role panels, the Trail's Pass-by and Items panels are gone).
- [ ] Each pair mission opens on a fight whose ★ answer is a Hearth tool (John's guard and Wrath, Lucy's Cyclone, Linda's Explosive Arrow, Mark's Fist Blitz chain), and the plain play costs a hero at least a third of their HP (combat log).
- [ ] Each pair mission then teaches its pair Synergy in a small situation (River: Shield Flare; Ridge: Catch & Return) and challenges it within the same level.
- [ ] The Trail is two levels at most, with no walk longer than one move before the first enemy is in reach, and its first real-combat Duo is the finisher at The Pile.
- [ ] No memory has a turn cap; each memory's result screen shows one objective line.
- [ ] A new game starts at Home on the storytelling idle and goes into the Hearth by itself; the Family tree opens by itself after the Yard scene.
- [ ] Hearth → M4 send-off plays in about 45 minutes at THJ's pace (paper: 41); no post-Hearth level runs past 5 rounds.

## Scope

In: the four Hearth memories (caps, result lines, Family Role exposure, Lucy's multi-shot page, Memory 4's ending and the Duo), the River, the Ridge, The Trail (structure and both levels), the three Home visits' content and the new-game start, what to cut or delay, the all-scope UI items THJ listed (goal tile colour, objective feedback, Tempest Bloom preview).
Out: Family Role rules (the rethink track), the Cyclone rules (P9, [`design/cyclone-redesign.md`](../../design/cyclone-redesign.md)), rewards (P7), the tally line and bug (P8), final text (`miso-narrative`), M4's own levels beyond the send-off.

## Touches

Systems: level prefabs `GB_m1-linda` to `GB_m4-mark`, `GB_s1-river`, `GB_s2-ridge`, `GB_m2-tracks`, `GB_m2-pile` and their editor wiring tools (`HearthMemoryWiring.*`, `SearchWiring.*`); `M2 - The Trail.asset` level graph; `LevelObjectives` stages, `HiddenLevelUnits` reveals, `LevelStartFPFiller`, per-instance HP and alert (data); Home: new-game start, mission completion sequences, the upgrades panel (C5c panel API, D-356); end panel (`MissionEndPanelUI`), objectives panel, `GridCell` goal highlight, Linda's arrow preview (UI, not core). Core: none required by this plan. One optional core item is handed to the rethink track (a per-level role switch, only if roles stay as built).
USPs: Synergies (main), Duos, Family Roles (exposure only), Home.
Docs: see [Docs to update](#docs-to-update-if-approved).

---

## Problem and evidence

**Symptom:** after the Hearth the levels feel like nothing: no challenge, no real tutorial, no real story, "too much", The Trail worst, The Pile weakest.

**Root problem: the post-Hearth levels were built to *introduce* things, not to *test* them, at a difficulty where the introduction is the whole level.** Each was designed as "the one new thing" (a role, an optional Synergy, FTP, items, Encore, the Asleep state) at Tutorial tier, with sleeping enemies the player picks off one at a time and the obvious play always working. So the player meets eight new things and is never asked to use anything well. THJ's rhythm (teach, challenge, teach, challenge) is missing its challenge half everywhere after the Hearth.

| Evidence | Where | What it shows |
|---|---|---|
| The Ridge 3 rounds / 5 kills, Trailhead 1 / 0, Follow the tracks 2 / 3 | Pacing-check logs | Levels end before a question is asked |
| River and Ridge at Tutorial tier (×0.6 HP, ×0.5 damage); enemies start Unaware; the River's ford Archers have 4-tile islands | `GB_s1-river`, `GB_s2-ridge` read back 2026-11-09 with `level_to_grid.py`; C4a/C4b reports | Low threat, fights chosen one at a time; Archers can step off the Shield Flare diagonals (THJ's note) |
| Shield Flare and Catch & Return are "optional, discovered" (D-176): "the obvious play works" | Paper levels, River and Ridge tables | The pair Synergies are never needed, so never learnt |
| Post-Hearth new things before M4: Asleep state + sight beat, Lucy's role panel, Mark's role panel, Archers, Papa's Shelter, Shield Flare, Catch & Return, FTP drain + Pass-by, the mission map, Encore's cue, Items, the tally, Workshop, skill tree, Bond, Family tree | C4, C5, Bond Lite reports | About 16 introductions in ~30 minutes, after a Hearth that already taught ~20 |
| The Pile: family starts at the north-west, the targets sit 6+ tiles away (one Archer behind the pile), the rear wave spawns at 0,6 / 0,5 on turn 2, on the family's own start | `GB_m2-pile`, C4c report | Exactly THJ's "walk away, then they spawn behind where you were" |
| Free enemy-turn roles carry much of the damage (Linda 46–72%) | `combat-balance.md`, rethink plan evidence 5 | A reason abilities feel unneeded, outside this plan's remit; the levels must work with or without it |

---

## Options compared

| | A. Tune numbers only | **B. Teach-and-challenge beats in the same levels, cut the rest (recommended)** | C. One combined search mission | D. Do nothing |
|---|---|---|---|---|
| What changes | Tier up to Early/Standard, more enemies, keep layouts | Each pair mission becomes 2–3 short beats (Hearth challenge → small Synergy lesson → its challenge); The Trail becomes 2 levels; post-Hearth panels, the route choice, the FTP drain and the Items panel are cut | River and Ridge merge into one mission with both pairs (design Q4's fallback); Home visit 1 goes | — |
| Player experience | Harder but still nothing to plan; one-by-one fights get longer | Every level asks a question with a Hearth tool or a pair Synergy as the answer; a story line on each beat | Saves a visit; loses "two go, two stay" and the order choice | THJ's notes stand |
| Rules to track | None | Fewer than today (8 introductions cut or delayed, 2 kept) | Fewer Home steps | Same |
| Time | Longer (HP sponges) | Shorter: ~41 min on paper (today ~46 with the last visit) | ~38 | ~46 |
| Cost | Data | Level + wiring-tool work on 4 existing levels; 2 small UI codes (all); Home tech plan | New mission, roster work, Home rework | 0 |
| Risk | THJ's "abilities not needed" stays | New balance to find in play; some story choice lost (route) | Breaks the approved structure | — |
| USP effect | Neutral | Synergies ++, Duos +, Home + | Home − | Synergies stay optional |

---

## Recommendation (summary)

Option B. In order of what the player meets:

1. **Home, then the Hearth.** A new game opens at Home on the storytelling idle and the Hearth starts by itself.
2. **The Hearth keeps its lessons and loses its caps.** No turn caps, one result line per memory, Lucy's multi-shot page, a Tempest Bloom preview, and Memory 4 ends on John cutting the line and the first Duo killing every enemy left in its reach. Family Roles: **no role before John, John's alone in Memory 3, none in Memory 4** (see dependencies).
3. **The River and the Ridge: challenge, then one pair Synergy, then its challenge.** Early tier with low per-instance HP (fast kills, real hits). River: an awake rush, then Shield Flare at a ford whose Archers stand on 1-tile islands. Ridge: an awake pack built for Explosive Arrow + Fist Blitz chain, then Catch & Return in the gauntlet. Their role panels and the Asleep panel go.
4. **Home visit 1 gets its content:** the handover at the door ("two go, two stay" pays off), then the Workshop pick.
5. **The Trail: two levels, no route choice.** *The Trail* (from Follow the tracks) asks Archers-or-queue with whatever pair Synergy the free pick brings; *The Pile* is a one-move search beat, then an ambush from both sides, finished by the sisters' first real Duo just before "Still counting?".
6. **Visit 3:** the Yard, then the Family tree opens by itself.

Time and the levers follow in [Recommendation](#recommendation).

---

## The Hearth (memories)

THJ: the Hearth feels like a tutorial and that is OK. Changes are small.

| Memory | Change | Work |
|---|---|---|
| All four | **Turn caps removed** (THJ): every "objective or cap" any-group becomes the objective alone; the "Turns left in the memory" line goes. Stages still move on when the objective is met | Data: M1–M3 through `HearthMemoryWiring.Linda/Lucy/John.cs` (editor code, re-run); M4 by hand in the prefab (the master, D-405) |
| All four | **One result line per memory** (THJ): the level-won panel shows one summary line instead of each stage's objectives. Text by `miso-narrative` (e.g. M1 "Seven Claws. One arrow.") | **New code, small (all):** an optional summary line on a level; when set, `MissionEndPanelUI` shows it alone. Not core |
| 1 Linda | **No Family Role.** As built, Watch costs 1 FTP: set the level's FP fill to −99 (drained) instead of full, so Watch can't pay. Linda's kit here needs no FTP (bow, Explosive Arrow, Encore). The "Watch" panel page goes; "Moving and AP" stays; "Each shot spends an arrow." moves into that page (text). Enemy turn 1 becomes a plain enemy turn (the baseline the [opening plan](2026-11-05-opening-family-roles.md) missed). Checked on paper: three arrows up column 2 (6, ×0.6 down the line, GDD) kill A 14 / B 6 / C 2 over two turns without Watch if C (2,9) is within her 4, i.e. Linda shoots from 2,5; from the throat's top (2,4) C survives at 2 HP and stage 1 needs a picked-up arrow, which stage 2 teaches anyway. To play-check | Data (wiring tool). FR-dependent (row F1) |
| 2 Lucy | **Multi-shot page** (THJ): one page at level start on Fire Embers' extra embers (how many, how their targets are picked). Read `Lucy_Ability_PrimaryAttack` before writing it (to check: whether the player picks each ember's target or the sidewinder picks its own, as the GDD says) | Data (existing `TutorialSequence`); text by `miso-narrative` |
| 3 John | **John's role alone.** The sisters' roles should not fire (THJ). Turn 1 already gives John 1 AP and the sisters 0 | FR-dependent (row F2): no build until the rethink decides |
| 4 Mark | **Ending and Duo**, below; **no Family Roles**; **Tempest Bloom preview** | Prefab by hand; preview is new code (all); roles FR-dependent (row F3) |

**Memory 0 for John:** not recommended (Q3). John alone has nobody to guard, so his role can't show; it adds 2–3 minutes to a Hearth already on target; Memory 3's turn 1 is already John's own turn (sisters at 0 AP).

### Memory 4: John cuts the line, the first Duo finishes it

Prefab cells as in the [paper levels' Memory 4 section](2026-10-26-onboarding-levels.md#segment-4--marks-telling-and-then-i-arrived) (prefab x = drawing x − 1).

| Item | As built | Proposed |
|---|---|---|
| Stage 1 | Any Bloom target dead, or cap 1 | Any Bloom target dead |
| Stage 2 | "John: Cut the reinforcement path." John on (6,5), or cap 2 | Same objective, no cap. **On complete (`Hold`), both Corruption pools stop for good** (THJ: John "cuts the line"). Data: an LSB call in `Hold` switching off the two `CP_Spawner_Hearth` objects or their component (`GameObjectActivationManipulationAction` / `MonoBehaviourActivationManuipluationAction`, existing); **to check** that a switched-off spawner stops its turn-specific spawns |
| Stage 3 | Six Claws dead or cap 4, **and** John on (6,5) or cap 4 | **Only the three `top` Claws** (8,7), (9,7), (9,6), 7 HP each. John no longer has to stay on the mouth |
| Enemies | (9,8) and (10,7) by the mother; the (6,4) Claw scripted to (7,7) and counted in stage 3 (D-417) | Remove (9,8) and (10,7). The (6,4) Claw's scripted move ends on the den side (John's fight), out of the Duo's 4, and it leaves stage 3 |
| The Duo | Mark–Lucy unlocks in `Hold`; six Claws in reach, it takes up to 3 | Exactly three enemies in reach and they are the objective. Chained Assault does (3 + 8) × mash 0.7–1.5 = 7.7 at worst per target, against 7 HP: **it always kills all three and ends the memory** (THJ: "the first Duo should finish everyone"). It also closes the open check on which three it picks with six in reach |
| John off the board (THJ's "maybe") | — | Not needed once stage 3 stops asking him to stay. If THJ still wants it: a sequence step that takes a unit out of play (small new code, e.g. a `Hide` beside `HiddenLevelUnits.Reveal`). Q4 |
| Left-side Claws | Fight John and Linda | Unchanged. With the pools off they are finite; whatever is left when the Duo lands ends with the outro ("…and that was the last of them", narrative). Q4 asks whether THJ wants them in stage 3 too (one more turn) |

**Tempest Bloom preview (THJ) (all):** while Linda aims her bow along a lane that enters a Cyclone, the arrow preview continues as the copies' lanes from the Cyclone's tile (each neighbour except back the way it came, SY table), with the usual damage preview on whatever they reach. Same reach rule as every preview (CR-37). One new on-screen element, necessary: without it the Bloom is the one shot in the Hearth the player takes on faith. New code in the attack preview (`UnitThreatAnalysis` reach helpers, `PlayerController` preview path; read, not traced); its own tech plan. It keeps working under the Cyclone redesign (the split rule doesn't change).

---

## The search: the River and the Ridge

**Shared rules for both pair missions.**

- **Tier Early** (×1 HP, ×0.75 damage, CR-32) with **per-instance HP factors**: Dark Claws 0.6 (≈ 9.6 HP), Archers 0.33 (≈ 8). Kills stay as fast as at Tutorial; hits hurt half as much again. Data (the per-instance `Stat_HP` override the Ridge already uses).
- **No panels.** The Asleep panel and sight beat go (THJ; the marker stays), the role panels go (THJ: the prompt teaches itself). The first-sleeper handle comes off both levels; the shared asset stays unused.
- **Teaching = one line + the board.** The Synergy's line plays as the closing beat's stage starts (an `OnCompleteSequence`, data), never as a bark condition (none can test positions, C4 check).
- **A story line on every beat**, not only at the end: each stage's sequence carries one clue line (narrative moves the existing R7 and G9 lines; no new beats).
- Rewards unchanged here (P7 flips them separately).

### The River (John + Lucy), reworked `GB_s1-river`

Prefab coordinates (no offset; read back 2026-11-09). Cells removed from the as-built map: the island tiles around each Archer (8,5 8,6 9,6, 13,6 14,5 14,6, 8,1 8,0 9,0) and the empty south-east island (13,0 13,1 14,0 14,1). Two Claws added on the far bank. `@` builds as floor; the tile is marked by stage 2's goal highlight.

```grid id=after-river title="The River, after the Hearth (prefab coordinates)"
# # . . . . # # # # # . # # # # #
# . . . . . . # # a # . # a # # #
# . . . . . c # # # . . . # # c .
U J . . . c . . . . . @ . . c . .
# . . . . . c # # # . . . # # . .
# . . . . . . # # a # . # # # # #
# # . . . . # # # # # . # # # # #
--
zone 0,3 1,3 lucy Sheltered
cells 5,3 6,4 6,2 enemy awake at start
note 3,3 beat 1
arrow 11,3 10,4 9,5 lucy dy=-6 Flare
arrow 11,3 12,4 13,5 lucy
arrow 11,3 10,2 9,1 lucy
range 14,3 2 enemy wake together
step 11,3 2
note 11,4 Lucy beside him
note 16,3 clue
level name The River
level tier early
```

| Item | Plan |
|---|---|
| Source | `GB_s1-river`, cells and units as above. Read back with `level_to_grid.py` first: today's prefab matches the C4a block, so a rebuild plus a re-run of an updated **Wire Search: River** is safe if nothing was hand-edited since |
| Challenges (beat 1, the clearing) | Hearth: **John's guard and Shield Up → Wrath → the punish** (Memory 3) and **Lucy's Cyclone** (Memory 2), under a real rush |
| Teaches (beat 2, the ford) | **Shield Flare**, small: John holds the one tile 4 from every island; Lucy embers him |
| Challenge of it | Same beat: the Flare must clear the three Archers while two far-bank Claws rush the pair |
| Squad | Lucy 0,3, John 1,3 (Papa's Shelter shown at start, as built) |
| Enemies | Clearing: 3 Dark Claws (5,3 6,4 6,2), **starting alert** (per-instance `startsAlert`, or the existing `Unit_DarkClaw_StartsAlert` variant). Ford: 3 Archer Goblins on 1-tile islands 9,5 / 13,5 / 9,1 (cannot move: no neighbour cells), Unaware. Far bank: 2 Dark Claws 14,3 / 15,4, Unaware. Early, factors above |
| Beat 1 | Claws move 4: 5,3 reaches 2,3 on enemy turn 1. ★ John Shield Up beside Lucy (his guard takes their hits at ×0.5 × 0.6 and stacks Wrath), then a Wrath Shield Dash (4 × up to 2.05, push) with Lucy's embers. ★ Cyclone in the clearing to split the rush. ● Sword and embers one at a time: Lucy (15 HP) takes 4–5 a hit if she strays from John. ~2 rounds |
| Stage 1 → 2 | Clearing dead → sequence: camera across the ford to the islands, then John "Lucy. If it gets hot, aim at me." / Lucy "*At* you?" / John "Trust me." (R7-7 to R7-9). New objective **"John: hold the ford."** (John on 11,3): the goal highlight marks the tile (non-green, below) |
| Beat 2 (verified distances) | 11,3 is 4 from 9,5, 13,5 and 9,1 (Archer range 3: safe) and 2 diagonal from each: copies via 10,4, 12,4 and 10,2 (all floor). John stopping on 11,3 is 3 from 14,3: it wakes and spreads to 15,4 (2 apart, EN-15). Every tile beside John is within 3 of at least one Archer (11,4 → 9,5 and 13,5 are 3), so Lucy needs his guard. ★ John: move + Shield Up; Lucy: step beside him + ember him → one Flare = all three Archers hit. Archers at 8 HP die to two Flares (assumed copy damage = the ember's 4; **to check**, and whether each Sheltered ember flares on its own). Wrath from the Archers' and Claws' hits feeds a Shield Dash at the far-bank Claws. ● Lucy embers each island from 10,4 or 11,5 (2 from 9,5 / 13,5), shot by two Archers at a time. ~2 rounds |
| Stage 3 | Defeat all. End: the far-bank clue close-up (as built) |
| Alert | Default, except the clearing Claws |
| FTP | Starts full (8) |
| Fallback | A player who never embers John wins slower and hurt. The goal tile, the line, and Lucy's targeting already offering a shielded John (GDD Lucy) are the teaching. If the play check shows it missed: a `GuidedAbilityHint` pulse on Fire Embers while John stands on 11,3 with Shield Up (**to check** whether a hint condition can test that; else accept) |
| To check | Shield Flare copy damage and per-ember flaring; Archer damage at Early (assumed ≈ a Claw's) |
| Time | ~5 min (4–5 rounds) |

### The Ridge (Linda + Mark), reworked `GB_s2-ridge`

Prefab coordinates (as built read back 2026-11-09; the rush pack moves, a Claw is added at 10,1).

```grid id=after-ridge title="The Ridge, after the Hearth (prefab coordinates)"
. . . # # # # # # # # # #
. c . # # # # # # # # # #
c c c # # # # # # # # # #
. . . # # # # # # # # # #
. . . . # # # # # # # # #
. L M . . . c c . . c . .
# . . # # # # # # # # # #
--
cells 0,4 1,4 2,4 1,5 1,3 linda Explosive blast
arrow 1,1 1,4 linda Explosive Arrow
arrow 2,2 2,4 mark dx=4 Blitz, then Continuous
step 1,4 1
arrow 5,1 8,1 mark dy=-10 Vault
arrow 4,1 8,1 linda dy=6 out
arrow 8,1 4,1 mark dy=12 back
step 8,1 2
note 12,1 clue
level name The Ridge
level tier early
```

| Item | Plan |
|---|---|
| Source | `GB_s2-ridge`; rebuild + an updated **Wire Search: Ridge**, same check as the River |
| Challenges (beat 1, the pack) | Hearth: **Explosive Arrow on a packed group** (Memory 1) and **Fist Blitz + Continuous Attack** (Memory 4) |
| Teaches (beat 2, the gauntlet) | **Catch & Return**, small: two Claws queued between Linda and Mark |
| Challenge of it | Same beat: it has to land in the one turn before the queue reaches Linda, and Mark lands next to a third Claw |
| Squad | Linda 1,1, Mark 2,1. **The family acts first** (reverses D-353's enemy-first, so the opening is the player's plan, not two prompts; Q6) |
| Enemies | Pack: 4 Dark Claws 1,4 / 0,4 / 2,4 / 1,5 (1,4 is 3 from Linda, so it starts Alerted and its spread wakes the rest, EN-12/15). Gauntlet: 6,1 / 7,1 asleep, HP factor 0.65 (≈ 10.4). End: 10,1 asleep (wakes when Mark lands on 8,1, 2 away). Early |
| Beat 1 (verified distances) | ★ Explosive Arrow from 1,1 on 1,4 (3, within 5): the cell and its 4 neighbours hold all four Claws, 8 each → ≈ 1.6 left. Mark steps to 2,2, Fist Blitz on 2,4 (2 away) kills, he steps in, Continuous Attack swings at the lowest in 2 (1,4, 1,5, 0,4 are 1–2 away). Linda's second AP finishes the last. ● Arrows and single Blitzes: four Claws reach Linda (20 HP) for 4–5 each. ~1–2 rounds |
| Stage 1 → 2 | Pack dead → sequence: camera down the corridor, Mark "Linda. Shoot at me." / Linda "Gladly." / Mark "From the far side." (G9-6 to G9-8), and the tracks line (G9-1) |
| Beat 2 | ★ Mark to 5,1, Vault to 8,1 (3, over the queue; Vault over units was a C4b check and THJ played the Ridge OK, but confirm it in play); Linda to 4,1, bow along row 1: 6,1 and 7,1, then Mark (4 away, ≥ 2) → the catch QTE → the return copy hits both again: ≈ 6 + 5.4 each (C4b's read) ≥ 10.4, plus the Vault's 2 on 7,1. Linda on 4,1 wakes the queue (2 away), so it must happen this turn. Then 10,1 attacks Mark; Fist Blitz or her returned arrow ends it. ● Blitz them one by one while they reach Linda |
| Alert | Default (the pack wakes itself) |
| FTP | Starts full (5). As built, roles and Continuous Attack share it: FR-dependent (row F5) |
| Clue | End close-up on 12,1 (as built) |
| Fallback | The obvious play still wins, hurt. No hint planned |
| Time | ~4 min (3–4 rounds) |

---

## M2 · The Trail: two levels

**Structure.** *The Trail* → *The Pile*. No route choice, so no mission map; the empty Trailhead and "Follow the blood" leave the level graph (assets kept). Data: `M2 - The Trail.asset` level graph. The FTP drain goes with the Trailhead (FTP starts full, CR-10), the Pass-by panel goes (Pass-by still works; taught after M4), the Items panel goes (items stay in stock; the pouch bob, CR-52, cues them). The tally's rematch line (P8 proposal) moves to *The Trail*'s start. The free pick (John or Mark) decides which pair Synergy the player brings: both levels give each one a ★, so The Trail challenges what the River or the Ridge taught.

If THJ keeps the route choice (Q1, option b): the Trailhead keeps its role as the level before the map, gets a one-turn fight (two sleeping Claws in the 1-wide trail: Linda's pierce from Memory 1), and "Follow the blood" gets the same rework as below. About +3 minutes.

### The Trail (Linda, Lucy + John or Mark), reworked `GB_m2-tracks`

Prefab coordinates. The as-built map widened by two columns at the east end (9,1 and 10,1 new cells); rows 2–3 end at x5; the Claw on 7,3 moves into the trail.

```grid id=after-trail title="The Trail (prefab coordinates)"
# # # # a # # # # # #
# # # # a # # # # # #
_ _ _ _ _ _ _ _ _ _ _
# . . . . . # # # # #
# . . . . . # # # # #
L U J . . . . c c . c
# # # # # # # # # # #
--
range 4,5 3 enemy Archer reach
arrow 4,1 4,6 linda dx=-8 bow or Marks-Sisters
arrow 3,1 8,1 linda dy=8 Explosive
arrow 6,1 9,1 mark dy=-10 Vault (Mark picked)
note 10,1 wakes with the queue
note 4,1 wakes the queue
level name The Trail
level tier early
level deploy 2,1
```

| Item | Plan |
|---|---|
| Source | `GB_m2-tracks`; rebuild + an updated **Wire Search: Trail**. Keeps its stages (both Archers dead → the Encore cue, then defeat all) |
| Question | Archers on a ledge you can only hit from range, and a queue asleep in the trail's narrow end: which first, and from where? |
| Challenges | Hearth and pair missions: Linda's range and pierce, Explosive Arrow, **Encore** (her arrows land on the ledge; Memory 1 unlocked it), and the picked pair Synergy |
| Squad | Linda 0,1, Lucy 1,1, the pick on the slot 2,1 |
| Enemies | 2 Archer Goblins on the ledge 4,5 / 4,6 (static: no walkable neighbour), Unaware, factor 0.5 (≈ 12). Queue: Dark Claws 7,1 / 8,1 and 10,1 (2 apart: they wake together), Unaware, factor 0.6. Early |
| Answers (verified distances) | ★ Linda on 4,1 outranges the ledge (4 to 4,5; their reach is 3), but **4,1 is 3 from 7,1 and wakes the queue**: the real decision. ★ Explosive Arrow first from 3,1 on 8,1 (5; 3,1 is 4 from 7,1, so no wake): hits 7,1 and 8,1. ★ Marks-Sisters up column 4 from 4,1: both Archers (12 × mash vs 12, kills at mash ≥ 1.0) as the finisher. ★ (Mark) Vault from 6,1 to 9,1 (3) between the queue and 10,1, Linda's bow from 5,1 down row 1, the catch, the return. ★ (John) Shield Up in the trail as the queue arrives (guard + Wrath); Shield Flare from 2,3 reaches only 4,5 (via the gap 3,4; **to check** that copies fly over gaps), so it's ● here. ● Lucy embers from 4,2 or 4,3 at the ledge: inside the Archers' reach |
| Encore | Unchanged cue on the "both Archers dead" stage (D-334): her arrows are on the ledge |
| FTP | Full at start (no drain) |
| Time | ~3 min (3 rounds) |

### The Pile (Linda, Lucy + John or Mark), rebuilt on `GB_m2-pile`'s footprint

Prefab coordinates, same 10 × 7 footprint, new cells. The beat comes first and is one move long; the fight comes after it, from both sides, to the family.

```grid id=after-pile title="The Pile (prefab coordinates)"
# # L U J . # # # a
# # . . . . . . . #
c c c . _ _ . . . c
# # # . _ _ . . . c
# # # . . . . . . #
# # # . . . . . # #
# # # # # # # # # #
--
zone 4,3 5,4 note the pile
step 4,5 1
note 4,5 search
cells 0,4 1,4 2,4 enemy hidden: west
cells 9,4 9,3 9,6 enemy hidden: east
arrow 3,4 0,4 linda Marks-Sisters
arrow 7,4 8,5 9,6 lucy Flare (John picked)
level name The Pile
level tier early
level alert all
level deploy 4,6
level hidden west 0,4 1,4 2,4
level hidden east 9,4 9,3 9,6
```

| Item | Plan |
|---|---|
| Source | `GB_m2-pile` footprint; new layout, rebuilt from the block; **Wire Search: Trail** updated (hidden groups and a reveal replace the turn-2 `GUnitSpawn` rear wave) |
| Before the beat | *The Trail*'s fight |
| The beat (THJ: low tempo on purpose) | Start: the pile close-up, Lucy "Linda… what if she's in there?" / Linda "Then we find her. Together." (T11-3, T11-4). Objective **"Search the pile."**: any Bergson on a tile beside it (4,5 or 5,5 is one move from the start row). The rivalry barks stop here (narrative). It echoes Memory 4's walk to the cub |
| After the beat | Search done → both hidden groups revealed (alert, `level alert all`): three Claws in the west lane, two Claws and an Archer on the east perch. They act on the next enemy turn. Back to back |
| Enemies | West 0,4 / 1,4 / 2,4, east 9,4 / 9,3 Dark Claws, factor 0.6; Archer on the 1-tile perch 9,6 (no neighbour cells), factor 0.5. Early |
| Answers (verified distances) | West lane: ★ **Marks-Sisters from 3,4** along row 4 (5 cells) hits all three lined up (12 × mash vs 9.6: kills at mash ≥ 0.8), or Linda's bow (6, then less down the line). East: ★ (John) Shield Flare from 7,4 reaches the perch via 8,5 (2; 8,5 is a cell, diagonal to the perch, so the perch keeps no walkable neighbour); 7,4 is 4 from 9,6, outside its reach. ★ (Mark) Fist Blitz + Continuous Attack on the two east Claws once they close. ★ Linda's bow on the perch from 5,6 along row 6 (4, across 6,6–8,6, which the grid draws as **rock, not gap**: **to check** that her arrows fly over rock (coordinator, grid check 2026-11-09); her arrow then lies on the perch for Encore). ★ Lucy's Cyclone on 6,4 or 7,5 splits the east pair's approach (it blocks the family too until the Cyclone redesign, P9; no ★ here needs the family to pass it). ● Embers on the perch from 7,5 (3), inside its reach |
| Finisher | **The sisters' first real-combat Duo is the intended finisher** (THJ: Duos as an ultimate), on the west lane. It counts for both sisters (D-449), the counter rises for both, and the end plays "Still counting?" / "…No." over it. No hint: Marks-Sisters is on both sisters' bars; a `GuidedAbilityHint` pulse is the fallback if the play check shows nobody uses it |
| Win | Defeat all. End as built (the tally fade, the free pick's line, Lucy's motive line T11-8) |
| What THJ's notes asked | No walking (the family starts two tiles from the pile and the enemies come to it), nothing out of reach for long (the perch Archer is in Linda's row from 5,6, 4 tiles across the gap and outside its reach, and on Shield Flare's diagonal from 7,4), no start spawns walking back (the fight starts after the beat, from both sides, on purpose) |
| FTP | Carried from *The Trail* (full at its start; a Duo costs 2) |
| Time | ~4.5 min (search + 3 rounds) |

---

## Home

| Moment | Today | Proposed | Work |
|---|---|---|---|
| New game | Menu, then the Hearth's levels (the Hearth open at Home was a C3 leftover) | **Home on the storytelling idle** (`MargaretStoryNight`, Margaret hosts, D-178), H0-1 to H0-4, then the Hearth starts by itself (THJ) | Home flow: small code. Tech plan (coordinator) |
| After the Hearth | Hearth close, "Two go out, two stay", World map page | Unchanged | — |
| Visit 1 (after the first pair mission) | The Workshop page only; THJ: "nothing in between" | **The handover at the door**: the returning pair meets the leaving pair. One clue line from the returning pair, then the go-between joke (V1-2a to V1-4a, or V1-2b to V1-4b by order) and Ben's "You two are next? Hand them over." (V1-1), which leads into the Workshop pick for the leaving pair (existing page). About 1 minute; "two go, two stay" gets its scene | Data: a `DialogNodeSequence` as each pair mission's completion scene. **Small code** if it must play only after the *first* pair mission (completion scenes can't test that today; C5c's `GetLastCompletedMission` is a model). Q5 |
| Visit 2 | Skill tree page + guided spend; Map Table clue scene on the Trail pin | Unchanged | — |
| Visit 3 | Yard → Bond Lv 2 → Margaret's point → pan back | **The Family tree opens by itself on the Family tab after the pan back** (THJ; reverses C5's "no tab opens by itself") | Small code: the upgrades panel API from C5c (D-356). Scope `thj/onboarding` |

P7 (River and Ridge rewards the wrong way round) touches visit 1's Workshop pick: fix it before this visit is play-checked.

---

## What to cut or delay

THJ: "too many mechanics with too little challenge." This plan removes eight introductions from the first hour and adds two small ones (Shield Flare and Catch & Return as lessons; both already existed as optional discoveries).

| Item | Was | Now | Why |
|---|---|---|---|
| Asleep panel + sight beat | Required, first pair mission | **Cut** (the marker stays) | THJ |
| Lucy's / Mark's Family Role panels | River / Ridge start | **Cut** | THJ: the prompt teaches itself (FR-dependent, row F4) |
| Watch panel and Watch in Memory 1 | Memory 1 | **Cut** | THJ: no role before John |
| Turn caps and "Turns left in the memory" | All memories | **Cut** | THJ |
| Route choice + mission map | M2 | **Delayed** to later content | One screen and one level less; nothing in M2 needs it (Q1) |
| FTP drain + Pass-by panel | M2 trailhead and routes | **Delayed** to after M4 (Pass-by still works) | With FTP full, the Duo is a finisher, not a lesson in scarcity |
| Items panel | The Pile | **Cut** (items stay in stock) | The pouch bob cues them |
| Empty Trailhead | M2 level 1 | **Cut** | THJ: too vague; its job (open the map) goes with the route choice |
| Kept | Papa's Shelter shown at River start; Encore's cue in *The Trail*; the tally; Workshop, skill tree, Bond Yard, Family tree | | Each is shown once, at the moment it pays off |

---

## Family Role dependencies

The rethink plan compares **A** (keep as built), **B** (Pilot 1: free, caps per round) and recommends **C** (Kept AP: outside the family's turn a role answers only with AP its Bergson kept), with A as the fallback. This plan holds under each; the columns say what changes.

| # | Place | As built (A; B is the same here except roles stop costing FTP) | Kept AP (C) |
|---|---|---|---|
| F1 | Memory 1, no Watch | FP drained to 0 (data). Under B (free roles) the drain stops working: needs F2's switch | Nothing to build: a new player who spends both AP sees no Watch. Remove the drain |
| F2 | Memory 3, John's role alone | Needs a **per-level switch that turns off a given hero's role** (core: `FactionControllerBase` or the role handler; Tier 3). Ask the rethink track to include it only if A or B wins. Until then the sisters' roles fire, as THJ played it | Nothing to build: the sisters start at 0 AP and can't keep any; the rethink places its one "keep" line here |
| F3 | Memory 4, no roles | Same switch as F2. Until then, as built | Mostly automatic (turn-1 AP limits; a player rarely keeps AP in the showcase) |
| F4 | River / Ridge, no role panels | Lucy's and Mark's prompts appear untaught; Linda's Watch is first seen in the Ridge together with Mark's counter (both in the opening rush). THJ: fine | Each needs the player to keep AP, already taught in Memory 3; the River's guard for Lucy and the Ridge's rush become keep-or-spend questions (the rethink's own note) |
| F5 | Ridge FTP (max 5) | Watch, the counter and Continuous Attack all spend it: two role answers leave one Continuous Attack swing, and Linda's second AP finishes instead | Roles spend no FTP: the chain has its full 3 |
| F6 | Difficulty of every John level | His guard redirects every hit within 2 at ×0.5, unlimited: the River's pressure is mostly on John's HP. Lever: Standard tier on the River (below) | His guard is limited by kept AP (or exempt, rethink Q3): the River gets harder by itself; lever goes the other way (factor 0.5 on the Claws) |
| F7 | The Pile and *The Trail* | Roles spend the Duo's FTP; with a full pool (8–10) one Duo stays affordable | FTP is the Duo meter only (the rethink's note): cleaner |

**What this plan asks of the rethink track:** if A or B is chosen, a per-level, per-hero role switch (F2, F3); if C, nothing.

---

## Small UI rules THJ listed

| Item | Rule | Work | Scope |
|---|---|---|---|
| Goal tile | The win-objective highlight (MI-18) is no longer green: green already means HP bars and heals (CR-49, CR-53). Proposal: a warm gold outline; the art call is THJ's | Data: the `gridCellHighlightLevelGoal` sprite or its tint on the `GridCell` prefab | **all** |
| Objective feedback | When an objective is met, its line in the objectives panel ticks and pulses once with a short sound, and the panel unfolds if it was folded. No new element: it animates the one that exists | New code, small (objectives panel UI, not core) | **all** |
| One result line per level | Optional summary line on a level; when set, the level-won panel shows it alone (the memories use it) | New code, small (`MissionEndPanelUI`) | **all** (option off by default) |
| Tempest Bloom preview | See Memory 4 | New code, own tech plan | **all** |
| Level-design rule | A ranged enemy meant to stay put stands on a 1-tile island or perch (no walkable neighbour), so a Synergy aimed at it can't be dodged by its own move | Catalogue knob in `design/level-chunks.md` | **all** |

---

## Lens notes

### Creative

**Target experience.** After the Hearth the family stops telling stories and starts being tested. Each search trip should feel like the habits from the fireside, now needed for real, with one new trick the pair finds together ("Aim at me." / "Shoot at me."). The Trail should feel like the family's exam, and The Pile like the moment the joke dies.

**The moment designed for:** The Pile's last turn. The sisters, back to back at the pile, line up the west lane and fire their first Duo together; the counter rises for both of them at once; then "Still counting?" / "…No." The kill they share is the one that ends the count. That's the S8 template paying off without a framed beat.

Secondary: the River's three islands lit at once by one Flare; the Ridge's pack gone in one turn (Explosive Arrow, then Mark's chain); Memory 4's Duo ending the telling.

**Story on every beat.** THJ: "no real story". The pair missions get a clue line at each stage change, not only at the end close-up, from lines that already exist (R7, G9).

### Systems

- **Levers** (start values): tier Early; per-instance HP Claws 0.6, gauntlet 0.65, Archers 0.33 (River) / 0.5 (Trail, Pile); clearing Claws start alert; Pile `level alert all`; Ridge family first; FTP full in M2.
- **Interactions:** Shield Flare needs Shield Up on John (one AP) and Lucy's ember (one AP): a full turn of both, which is the cost that makes it a plan. Catch & Return is arrow-neutral (LI-9) and gives no AP (D-332). The Ridge's chain spends FTP on Continuous Attack (MA-2, 1 then +1) from a pool of 5 (F5). Marks-Sisters at The Pile costs 2 FTP from a full pool. Hidden groups revealed under "all start alert" come in alert (`HiddenLevelUnits`).
- **Failure cases:** the Flare never found (River still won, hurt; hint fallback); the Ridge chain cut short by FTP (F5: Linda's second AP finishes); a player who wakes *The Trail*'s queue early from 4,1 faces Archers and three Claws together (that's the decision, not a bug); the Pile's west lane not lined up because the Claws step out of it on reveal (they act on the next enemy turn, so the lane holds for one player turn after the search only if the search ends the player's turn: **to check**; else the Duo still has 2 in line).
- **Dominant strategy check:** John + Lucy fortress on the River's ford is meant to dominate there; outside that level islands and perches are rare. With roles as built, John's guard soaks every hit (F6): if THJ's play shows no HP pressure, River tier → Standard.

### UX

| Moment | Shown | The player clicks | Likeliest misread |
|---|---|---|---|
| River, ford reached | Camera over the islands, John's line, objective "John: hold the ford." with the (gold) goal tile | John to the tile, Shield Up; Lucy beside him, embers *him* | Embers an Archer instead (the habit). Lucy's targeting offers John only while Shield Up is on: the order matters, and the line says "aim at me" |
| Ridge, gauntlet | Camera down the corridor, Mark's line | Mark past the queue, then Linda's bow | Linda shoots before Mark is past: the arrow hits the queue and lands under the last Claw (LI-6). Costs an arrow, teaches the order |
| The Trail, column 4 | The ledge Archers' reach on Shift (CR-43) | Linda to 4,1 | Doesn't link stopping on 4,1 with the queue waking (the sight tiles show on Shift, CR-54; no panel, per THJ) |
| The Pile, search | "Search the pile." and the goal highlight beside it | One Bergson one step | Thinks the level is a cutscene and waits: the objective line and the tile carry it |
| Memory result | One summary line | Continue | — |

**On-screen elements added:** one (the Bloom preview). Removed: six panels, the turn-cap line, one map screen.

**Where the lenses disagree:** creative wants the Pile's Duo framed (pause, both portraits); the budget says no new element and B6 isn't built. I lean UX: the counter rising for both, then "Still counting?", is the frame.

---

## USP check

- **Family Roles:** neutral on purpose. Exposure only: none before John, John's alone, then each pair's in the pair missions, under either rethink outcome (F1–F7).
- **Synergies:** strengthened. Shield Flare and Catch & Return go from optional discoveries to taught-then-challenged lessons, re-tested in The Trail by the free pick, and Tempest Bloom gets a preview.
- **Duos:** strengthened. The first Duo ends Memory 4 by killing every enemy in its reach; the first real Duo is The Pile's finisher, shared by the sisters. FTP stays full, so the Duo is an ultimate, not a scarcity lesson.
- **Managing the Home as a Family:** strengthened. The game opens at Home; visit 1 gets the handover scene; visit 3 opens the Family tree on the best moment of the hour.

## Critics

**Not spawned.** This session has no agent-spawning tool, so I ran the three `miso-design-critic` lenses myself, one adversarial pass each. The coordinator may want real critics before THJ reads this.

| Lens | Strongest objection | What I did |
|---|---|---|
| Creative | "You turned the search into combat puzzles. THJ also said 'no real story': clues still sit at the end close-up, and cutting the route choice cuts the one story choice in M2 (blood or tracks)." | Took the first half: a clue line on every stage change, from existing lines. Kept the route cut as the recommendation but made it Q1 with the fuller option priced (+3 min); the blood/tracks choice was flavour, both routes led to the same pile |
| Systems | "Early tier with John's unlimited guard still makes the River soft, and the Ridge's FTP pool of 5 can starve the very chain you made its ★ (roles eat it first)." | Accepted as F5 and F6: the Ridge's ★ survives a short chain (Linda's second AP finishes); the River has Standard tier as the first lever. Both flip direction if Kept AP wins |
| UX | "No panels at all after the Hearth means Lucy's and Mark's prompts arrive untaught in fights that now hurt, and Linda's Watch is first seen in the Ridge beside Mark's counter: two new prompts in one rush." | Kept THJ's call (the prompt teaches itself) and named the Ridge double first as F4 and a risk to watch in the timed run. Under Kept AP it becomes one taught rule (Memory 3) plus self-teaching prompts |

What changed my mind: the systems pass moved the Ridge to "family first" (the enemy-first opener made two prompts the first thing in the level, whatever the rethink decides). What I rejected: a third beat in each pair mission (a second wave after the Synergy lesson); it cost about 2 minutes each, and The Trail already re-tests the picked Synergy.

---

## Recommendation

Option B as laid out above. Reasoning: it fixes the root problem (introductions without tests) by turning every post-Hearth level into a question with a taught answer, cuts eight introductions, and makes the first hour shorter, not longer.

### Time (THJ's pace; paper estimates, not timed)

| Step | Today (pacing check) | Proposed |
|---|---|---|
| Home start + Hearth | ~13 | ~13.5 |
| Home after the Hearth | ~2 | ~2 |
| First pair mission | ~1.5–8 | ~4.5 |
| Visit 1 (handover + Workshop) | ~2 | ~2 |
| Second pair mission | ~1.5–8 | ~4.5 |
| Visit 2 | ~2 | ~2 |
| The Trail | ~14 (3 levels + map) | ~8 (pick 0.5, The Trail 3, The Pile 4.5) |
| Visit 3 + send-off | ~3.5 (not logged) | ~3.5 |
| **Total** | **~46** | **~41** |

A cold player runs about ×1.3: ~53, inside the design's 45–60.

### Starting values

As in the level tables and the Systems levers. No GDD rule changes; values are per-level data.

### Playtest signal (THJ's timed run, then the cold run)

- **Worked:** in each pair mission the combat log shows the level's ★ (Wrath Shield Dash or Cyclone; Shield Flare; Explosive Arrow then a Continuous Attack; a catch), and at least one hero drops below two thirds of max HP; rounds per level 3–5; THJ says abilities felt needed; The Pile ends on the Duo; no walk of more than one move without an enemy in reach.
- **Failed:** the obvious play wins at full HP (raise tier, F6 lever); Flare or catch unused by a cold player (hint fallbacks); total time above ~45 at THJ's pace (cut *The Trail*'s queue to two Claws first).

### Approach: build order (each its own plan or chunk)

1. **Memory data** (caps off, Memory 1's FP drain if A, the Watch page out, Lucy's multi-shot page): wiring tools, data. Then **Memory 4 by hand** in the prefab (THJ or the implementer with his OK).
2. **River, Ridge, The Trail, The Pile**: rebuilds from these blocks + updated wiring tools + `M2 - The Trail.asset` graph. Level and editor-tool work, no runtime code.
3. **All-scope UI**: goal tile colour (data), objective feedback, result summary line (small code), one tech plan; the **Tempest Bloom preview** its own tech plan.
4. **Home**: new-game start, visit 1 handover gate, Family tree auto-open: one tech plan (coordinator).
5. Timed run by THJ, then the cold playtest.

Chunks 1 and 2 don't wait on the rethink. F2/F3 (the role switch) wait on it.

---

## Questions for THJ

**Q1. The Trail as two levels with no route choice?**
- Context: The Trail today is an empty Trailhead, a route choice (mission map), one route level and The Pile: ~14 minutes and four introductions (FTP drain, Pass-by, Items, the map). A mission map can only open after a won level (verified in C4-0), which is why the Trailhead exists.
- Options: (a) *The Trail* (reworked Follow the tracks) → *The Pile*; route choice and map delayed to later content; (b) keep the route choice: the Trailhead gets a one-turn fight, both routes reworked (+3 min, one more level to tune); (c) as built.
- Recommendation: (a). Fewer mechanics, and the free pick already gives M2 its choice.
- Blocked: chunk 2's Trail part.

**Q2. Family Roles in the Hearth: none before John, John's alone in Memory 3, none in Memory 4?**
- Context: THJ suggested it and wasn't sure. Memory 1's Watch can be turned off today with data (FP drained, Watch can't pay). Memory 3 and Memory 4 need a per-level, per-hero role switch (core, Tier 3), unless the rethink's Kept AP wins, which gives the same result with no switch (F1–F3).
- Options: (a) yes: Memory 1 now by data; Memory 3–4 follow the rethink (a switch only if A or B wins); (b) Memory 1 off, Memory 3 and 4 as built; (c) all as built.
- Recommendation: (a). It gives the player a plain enemy turn before the first role, and costs nothing until the rethink decides.
- Blocked: Memory 1's FP fill and panel; the request to the rethink track.

**Q3. A short Memory 0 for John before Linda and Lucy?**
- Context: John's role guards someone within 2, so alone he can't show it; the Hearth is ~13 minutes, on target; Memory 3's turn 1 already belongs to John (sisters at 0 AP).
- Options: (a) no; (b) yes, John alone with Shield Up and his sword (+2–3 min, one new level).
- Recommendation: (a).
- Blocked: nothing (only a new level if yes).

**Q4. Memory 4's ending: pools off when John reaches the mouth, John free afterwards, the Duo's three targets as the last objective?**
- Context: THJ: "John should cut the line, not turn limit", "maybe take him off the board", "the first Duo should finish everyone". Today stage 3 wants six Claws and John still on the mouth; the Duo takes three.
- Options: (a) as proposed (two Claws by the mother removed; the (6,4) Claw stays on John's side; the Duo always kills its three and ends the memory; leftover left-side Claws end with the outro); (b) (a) plus the left-side Claws in stage 3 (about one more turn, every enemy truly dead); (c) (a) plus John taken off the board after the hold (small new code).
- Recommendation: (a).
- Blocked: the Memory 4 prefab edits.

**Q5. Home visit 1: the handover scene, or cut the visit?**
- Context: the visit plays only the Workshop page today ("nothing in between"). The V1 lines exist (narrative draft) and aren't built.
- Options: (a) handover at the door (one clue line, the go-between joke, Ben's line into the Workshop pick), ~1 min, small code to play it only after the first pair mission; (b) cut the visit and move the Workshop to visit 2 (two decisions there); (c) as built.
- Recommendation: (a). It is the scene "two go, two stay" promises, and scenes were what landed in Bond Lite.
- Blocked: chunk 4's visit-1 part.

**Q6. Difficulty levers for the pair missions and The Trail.**
- Context: today Tutorial tier and sleeping enemies. Early tier with low per-instance HP keeps kills fast and makes hits hurt. The Ridge opens on the enemies' turn (D-353), so the level starts with two prompts.
- Options: (a) Early + factors (Claws 0.6, Archers 0.33–0.5), clearing and Pile enemies awake, the Ridge family-first (reverses D-353); (b) Standard tier everywhere, HP factors as (a); (c) Early, as-built HP (longer fights).
- Recommendation: (a), with (b) as the first lever if the obvious play still wins at full HP.
- Blocked: the level data in chunk 2.

---

## Docs to update (if approved)

- `design/gdd/missions-structure.md`: the onboarding missions (the Hearth's stages with no caps; The River and The Ridge at Early; M2 as two levels, no route, no FP drain, items unchanged); **MI-27's table** (The Pile: "all enemies start alert"; the River's per-instance alert); MI-18 note for the result summary line and the goal-tile colour; Memory 4's stages.
- `design/gdd/combat-rules.md`: a preview rule for Tempest Bloom beside CR-37 (new ID at the next free number) once built.
- `design/gdd/family-systems.md`: none unless the rethink adds the per-level role switch (F2).
- `design/level-chunks.md`: the 1-tile island/perch knob; link this plan from chunks 6, 13, 14, 23, 24.
- `plans/onboarding/2026-10-26-onboarding-levels.md`: mark The River, The Ridge and M2 sections superseded by this plan; the Hearth tables' cap rows.
- `plans/onboarding/2026-10-25-onboarding-first-hour-design.md`: the flow table (M2 row, FR firsts: first role ≈ Memory 3), acceptance criterion "Role QTE within ~5 min" → "first role in Memory 3".
- `plans/onboarding/onboarding-narrative-draft.md` (`miso-narrative`): the four result lines, Lucy's multi-shot page, the stage-change clue lines, the visit-1 handover, the rematch line's new slot (*The Trail*'s start), the outro line for Memory 4's leftovers.
- `decisions.md` (coordinator): Q1–Q6, and the reversals: D-353 (Ridge enemy-first), D-355 (Pass-by panel), the levels plan's "Asleep panel required", C5's "no tab opens by itself".
- `glossary.md`: "The Trail" now names M2's first level as well as the mission; narrative to rename if confusing.

## Risks

- **Paper balance.** HP factors, Flare copy damage and Archer damage at Early are assumptions; each level has a lever and a to-check row. THJ's timed run decides.
- **The rethink lands mid-build.** Chunks 1 and 2 hold under both outcomes; only F1's drain is undone if Kept AP wins (one line in the Linda wiring tool).
- **Two first prompts in the Ridge** (F4, roles as built). Watch in the timed run.
- **Hand-edited prefabs.** Read each level back before rebuilding; Memory 4 is edited by hand only (D-405).
- **Cyclone in narrow places** (P9): no ★ in this plan needs the family to pass a Cyclone; the redesign would only help.
- **`AIRegressionTest`** may shift with the variant or new levels: stays known red, never re-baselined.

## Gates

Design only. Before build: THJ's answers to Q1–Q6. Each build chunk: compile / EditMode (known red only) / review for code / THJ play check (feel and level chunks). Play check needs THJ's time: yes, a timed run Home → M4 send-off, then a cold playtest. Grids in this plan need drawing: `python claude-handoff/tools/grid_render.py claude-handoff/plans/onboarding/2026-11-09-onboarding-after-hearth-design.md`.
