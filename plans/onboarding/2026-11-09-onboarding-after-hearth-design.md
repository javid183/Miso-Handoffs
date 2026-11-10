# Onboarding after the Hearth: challenge what was taught

Size: L    Tier: 3 (level design and game feel of the first hour, Home flow, small all-scope UI rules)    Assigned to: miso-game-designer
Branch: `thj/after-hearth` (from `main` @ `e9bd6e885`, D-465), scope **all**: `main` now holds the whole onboarding (D-456), so every rule here applies on every branch.
Status: **approved** with THJ's answers of 2026-11-10 (D-466 to D-474; see [Answers](#answers)). Two answers went against the recommendation and are built in: M2 keeps the route choice (D-469); Memory 1's FTP is drained now (D-473). Memory 4 follows THJ's own design (D-471).

Source: [`playtests/2026-11-09-pacing-check.md`](../../playtests/2026-11-09-pacing-check.md), findings P1 to P6 and THJ's answers of 02:13. Builds on the approved [first-hour design](2026-10-25-onboarding-first-hour-design.md), the [paper levels](2026-10-26-onboarding-levels.md) and the C3 to C5 build plans. Runs alongside the Family Roles track: [`plans/2026-11-09-family-roles-rethink-design.md`](../2026-11-09-family-roles-rethink-design.md) (D-460: paper, one house-rule session, a dev switch only if it says yes, else lock as built) and its [round 2/3 draft](../2026-11-09-family-roles-round2-design.md) (D-464, direction: no role works when its Bergson is alone). This plan redesigns no Family Role rule; where it can't hold under every outcome it says so ([Family Role dependencies](#family-role-dependencies)).

History: written 2026-11-09; revised 2026-11-10 after three independent critics ([Critics](#critics)); revised again 2026-11-10 to THJ's answers (route choice back with a Trailhead fight and two reworked routes; Memory 4 by data only; Memory 1 drain back).

## Why

THJ's timed play (2026-11-09): the Hearth works as a tutorial, but nothing after it challenges what it taught. The River, the Ridge and The Trail are too easy ("you do not feel the need of abilities"), The Pile is the weakest level, the Trailhead walk is vague, and the first hour carries "too many mechanics with too little challenge". Timing is fine (about 42 minutes to the end of The Trail) and must stay fast.

## Goal

After the Hearth, every level first challenges what the player already has, and anything new it teaches is one small pair Synergy that is then challenged too, in tighter levels, with Hearth → M4 send-off still at about 45 minutes at THJ's pace.

## Acceptance criteria

- [ ] No tutorial panel and no caption after the Hearth. Post-Hearth teaching is the board, one spoken line, an objective line and the Synergy aim preview (D-467).
- [ ] Each pair mission opens on an **awake** fight whose ★ answer (★ = the intended, best answer; ● = the plain play that still works) is a Hearth tool (John's guard and Wrath, Lucy's Cyclone, Linda's Explosive Arrow, Mark's Fist Blitz chain).
- [ ] In each pair mission's combat log, the plain play costs at least one more round **or** about a third of a hero's HP more than the ★ play, measured under the Family Role setting in force at the play check (no caps exist, so the plain play is never forbidden, only worse).
- [ ] Each pair mission then teaches its pair Synergy (River: Shield Flare; Ridge: Catch & Return) and asks for it again in the same level.
- [ ] M2 is the Trailhead (a one-turn fight), the route choice, one of two reworked routes, then The Pile; no walk longer than one move before the first enemy is in reach; no enemy that only sleeps decides a level.
- [ ] The Linda–Lucy Duo is locked in every M2 level; The Pile ends on the sisters back to back, the tally alone (D-470).
- [ ] No memory has a turn cap; each memory's result screen shows one objective line.
- [ ] Memory 4: the first Duo always kills the three Claws revealed for it and ends the memory (D-471).
- [ ] A new game starts at Home on the storytelling idle (stations locked) and goes into the Hearth by itself; the Family tree opens by itself after the Yard scene.
- [ ] Hearth → M4 send-off plays in about 45 minutes at THJ's pace (paper: ~43); no post-Hearth level runs past 5 rounds.

## Scope

In: the four Hearth memories (caps, result lines, Memory 1's FTP drain, Lucy's multi-shot page, Memory 4's ending), the River, the Ridge, M2 (the Trailhead, both routes, The Pile), the three Home visits' content and the new-game start, what to cut or delay, the all-scope UI items (goal tile colour, objective feedback, result summary line, the Synergy aim preview).
Out: Family Role rules and Memory 3's role exposure (the Family Roles track; this plan hands it one requirement), the Cyclone rules (P9, [`design/cyclone-redesign.md`](../../design/cyclone-redesign.md)), rewards (P7, closed by D-455), the tally line and bug (P8), final text (`miso-narrative`), M4's own levels beyond the send-off (one handoff: the sisters' first Duo, D-470).

## Touches

Systems: level prefabs `GB_m1-linda` to `GB_m4-mark`, `GB_s1-river`, `GB_s2-ridge`, the M2 Trailhead prefab, `GB_m2-blood`, `GB_m2-tracks`, `GB_m2-pile` and their editor wiring tools (`HearthMemoryWiring.*`, `SearchWiring.*`); `LevelObjectives` stages, `HiddenLevelUnits` reveals, `LevelAbilityLock` (four M2 levels), `LevelStartFPFiller`, per-instance HP and alert (data). `M2 - The Trail.asset` level graph unchanged (route choice kept). Non-core code, small: the optional result summary line (`MissionEndPanelUI`); objective feedback (objectives panel); the Synergy aim preview (attack preview; its own tech plan). Home: new-game start with stations locked, visit-1 completion scene gate, Family tree auto-open (C5c panel API, D-356). Core: none.
USPs: Synergies (main), Duos, Home; Family Roles (exposure only).
Docs: see [Docs to update](#docs-to-update).

---

## Problem and evidence

**Symptom:** after the Hearth the levels feel like nothing: no challenge, no real tutorial, no real story, "too much", The Trail worst, The Pile weakest.

**Root problem: the post-Hearth levels were built to *introduce* things, not to *test* them, at a difficulty where the introduction is the whole level.** Each was designed as "the one new thing" (a role, an optional Synergy, FTP, items, Encore, the Asleep state) at Tutorial tier, with sleeping enemies the player picks off one at a time and the obvious play always working. So the player meets eight new things and is never asked to use anything well. THJ's rhythm (teach, challenge, teach, challenge) is missing its challenge half everywhere after the Hearth.

**A second root, found by the systems critic:** with no turn caps, any enemy that sleeps can be picked off safely one at a time. So a beat only challenges if its enemies are awake, or if waking them is visible before the click (it isn't today: no wake marker on the move ghost, `enemies.md` Q8).

| Evidence | Where | What it shows |
|---|---|---|
| The Ridge 3 rounds / 5 kills, Trailhead 1 / 0, Follow the tracks 2 / 3 | Pacing-check logs | Levels end before a question is asked |
| River and Ridge at Tutorial tier (×0.6 HP, ×0.5 damage); enemies start Unaware; the River's ford Archers have 4-tile islands | `GB_s1-river`, `GB_s2-ridge` read back 2026-11-09 with `level_to_grid.py`; C4a/C4b reports | Low threat, fights chosen one at a time; Archers can step off the Shield Flare diagonals (THJ's note) |
| Shield Flare and Catch & Return are "optional, discovered" (D-176): "the obvious play works" | Paper levels, River and Ridge tables | The pair Synergies are never needed, so never learnt |
| Arrow falloff is 1.0 in code, not 0.6 or 0.9 | `reports/onboarding-c4b-ridge.md` (systems critic) | A plain pierce does as much as a Catch & Return per arrow |
| Post-Hearth new things before M4: Asleep state + sight beat, Lucy's role panel, Mark's role panel, Archers, Papa's Shelter, Shield Flare, Catch & Return, FTP drain + Pass-by, the mission map, Encore's cue, Items, the tally, Workshop, skill tree, Bond, Family tree | C4, C5, Bond Lite reports | About 16 introductions in ~30 minutes, after a Hearth that already taught ~20 |
| The Pile: family starts at the north-west, the targets sit 6+ tiles away (one Archer behind the pile), the rear wave spawns at 0,6 / 0,5 on turn 2, on the family's own start | `GB_m2-pile`, C4c report | Exactly THJ's "walk away, then they spawn behind where you were" |
| Free enemy-turn roles carry much of the damage (Linda 46–72%); John's guard redirects every hit within 2 at ×0.5 | `combat-balance.md`, rethink plan evidence 5 | A reason abilities feel unneeded; the River can't be tuned once for both Family Role outcomes |

---

## Options compared

Kept as written before THJ's answers; THJ chose B, with the route choice kept (option b of the old Trail question, D-469).

| | A. Tune numbers only | **B. Teach-and-challenge beats in the same levels, cut the rest (chosen)** | C. One combined search mission | D. Do nothing |
|---|---|---|---|---|
| What changes | Tier up to Early/Standard, more enemies, keep layouts | Each pair mission becomes 2 short beats (an awake Hearth challenge → a Synergy situation that asks for it); every M2 level gets a fight that asks something; post-Hearth panels, the FTP drain, Pass-by and Items panels are cut; one aim-preview rule shows Synergy outcomes | River and Ridge merge into one mission with both pairs; Home visit 1 goes | — |
| Player experience | Harder but still nothing to plan | Every level asks a question with a Hearth tool or a pair Synergy as the answer; a clue on every beat | Saves a visit; loses "two go, two stay" | THJ's notes stand |
| Rules to track | None | Fewer than today (7 introductions cut or delayed, 2 kept, 1 preview rule) | Fewer Home steps | Same |
| Time | Longer (HP sponges) | ~43 min on paper (today ~46 with the last visit) | ~38 | ~46 |
| Cost | Data | Level + wiring-tool work on 9 levels; 3 small non-core codes; the preview's own tech plan; Home tech plan | New mission, roster work, Home rework | 0 |
| Risk | "Abilities not needed" stays | Balance found in play and partly after the Family Roles session | Breaks the approved structure | — |
| USP effect | Neutral | Synergies ++, Duos + (kept as finishers), Home + | Home − | Synergies stay optional |

---

## Summary of the approved plan

In order of what the player meets:

1. **Home, then the Hearth.** A new game opens at Home on the storytelling idle (stations locked) and the Hearth starts by itself.
2. **The Hearth keeps its lessons and loses its caps.** No turn caps, one result line per memory, Memory 1's FTP drained so Watch can't fire (D-473), Lucy's multi-shot page. Memory 4 (D-471): John holds the den mouth while the Claws near the cub die; then three Claws come in, the only targets of the first Duo, which ends the memory. Pools run as built.
3. **The River and the Ridge: an awake challenge, then a Synergy situation that asks for it** (D-468). Layouts now, enemy numbers after the Family Roles session played on them (D-466). The Synergy aim preview shows each Synergy's copies when the player aims into one (D-467).
4. **Home visit 1:** the handover at the door, then the Workshop pick (D-472).
5. **M2 (D-469):** the Trailhead becomes a one-turn fight in the narrow trail, then the route choice. *Follow the tracks*: an awake queue and two ledge Archers that one well-placed pierce kills. *Follow the blood*: two gullies emptying onto one junction, where the free pick's tool hits both at once. *The Pile*: a one-move search that answers something, then an ambush from both sides, ending on the sisters back to back, the tally alone. The sisters' Duo is locked in every M2 level (D-470).
6. **Visit 3:** the Yard, then the Family tree opens by itself.

---

## The Hearth (memories)

THJ: the Hearth feels like a tutorial and that is OK. Changes are small.

| Memory | Change | Work |
|---|---|---|
| All four | **Turn caps removed** (THJ): every "objective or cap" any-group becomes the objective alone; the "Turns left in the memory" line goes. Stages still move on when the objective is met | Data: M1–M3 through `HearthMemoryWiring.Linda/Lucy/John.cs` (editor code, re-run; **check first** that the Lucy wiring tool already carries the ten/two/four gag of D-457 to D-459, so a re-run doesn't undo it); M4 by hand in the prefab (the master, D-405) |
| All four | **One result line per memory** (THJ): the level-won panel shows one summary line instead of each stage's objectives. Text by `miso-narrative` (e.g. M1 "Seven Claws. One arrow.") | **New code, small (all):** an optional summary line on a level; when set, `MissionEndPanelUI` shows it alone. Not core |
| 1 Linda | **No Family Role (D-473).** As built, Watch costs 1 FTP: set the level's FP fill to −99 (drained) instead of full, so Watch can't pay. Linda's kit here needs no FTP (bow, Explosive Arrow, Encore). The "Watch" panel page goes; "Moving and AP" stays; "Each shot spends an arrow." moves into that page (text). Enemy turn 1 becomes a plain enemy turn. Checked on paper (falloff 1.0, systems critic): three arrows up column 2 (6 each, no loss down the line) kill A 14 / B 6 / C 2 over two turns without Watch if C (2,9) is within her 4, i.e. Linda shoots from 2,5. **Accepted risk (THJ):** the FTP meter shows empty on the game's first screen; a new player may read it as broken. Undone (one line in the wiring tool) if the Family Roles redesign makes Linda alone silent | Data (wiring tool) |
| 2 Lucy | **Multi-shot page** (THJ): one page at level start on Fire Embers' extra embers (how many, how their targets are picked), before the first two Claws. Read `Lucy_Ability_PrimaryAttack` before writing it (to check: whether the sidewinders each pick their own target, as the GDD says). **Checked against the stage-1 gag** (10 Claws → "Two." → 8 fade → "Four.", 4 Claws fight; D-457 to D-459): the page plays before the gag and names no Claw count; the result line must not quote a count either | Data (existing `TutorialSequence`); text by `miso-narrative` |
| 3 John | **No change here** (D-473: John-only roles wait for the Family Roles redesign, which already places its first lesson in this memory, round 3 S6) | None |
| 4 Mark | **Ending and Duo by level data** (D-471), below | Prefab by hand |

**Memory 0 for John:** not for now (D-474).

### Memory 4: John holds the mouth, the first Duo finishes it (D-471)

THJ's design, by level data, no new code. Coordinates are **prefab cells** (the paper grid draws them at x + 1; see the [paper levels' Memory 4 section](2026-10-26-onboarding-levels.md#segment-4--marks-telling-and-then-i-arrived)). No grid in this plan changes for Memory 4: the prefab is the master and edited by hand.

**Reading of D-471:** its "stage 1" is read as the first stage after the Bloom. The Bloom stays as its own opening stage (no cap) and plays `Arrival` as built. If THJ meant the Bloom stage to go too, only the first row below changes.

| Stage | Done when | On complete |
|---|---|---|
| 1 Bloom (as built, no cap) | Any Bloom target dead | `Arrival` (as built: boasts, `PostBloom`, Mark's arrival and chain) |
| 2 **Hold and clear** (new, replaces as-built stages 2 and 3) | **Both at once:** John on the den mouth (6,5) **and** the Claws near the cub dead: (9,8), (10,7) by the mother and the den-mouth Claw scripted from (6,4) to (7,7). One paired objective, the form stage 3 already uses (`Both`), caps removed. Visible text (narrative): one line, e.g. "John holds the mouth. Clear the den." | John's line, camera to the den, **reveal the three new Claws** (the existing `top` group and its `RevealUnitsSequence`, retimed from `Hold` to here), unlock the Mark–Lucy Duo (`UnlockAbilitiesSequence`, as built), the Duo lines |
| 3 **The Duo** | The three new Claws dead | Win, then the outro `End` |

Pools: both `CP_Spawner_Hearth` run as built (turns 1 to 8). The left-side Claws stay on the board through the outro; **the outro's lines must not say "the last of them"** (narrative), since the board shows otherwise.

**Paper check: the Duo's targets.** Chained Assault takes up to 3 targets within 4, nearest first (GDD; whether the 4 counts from Mark or from Lucy is still open, T13). It always ends the memory if, from where it is fired, the three new Claws are the only enemies within 4.

- **Left-side Claws are sealed out.** Every left-side tile (the row (-1..6, 4) and the column (3,5)–(3,7), both pools included) reaches the den only through (6,4) → the mouth (6,5); (5,5) and (7,4) are not cells. With John on the mouth, no left Claw can enter the den. The nearest any left Claw can stand to the den is (6,4), below John, or a pool tile, (3,7).
- **Tiles that keep every left tile beyond 4** (grid steps, 4-way): **(7,8), (8,8), (9,8), (10,8), (8,7), (9,7), (10,7), (9,6), (10,6), (10,5)**, the den's top-right block around the cub. Checked against (6,4), (3,5), (3,6) and (3,7): e.g. (8,7) is 5 from (6,4) and 5 from (3,7); (10,5) is 5 from (6,4); (7,8) is 5 from both.
- **Risky tiles:** (6,6), (6,7), (6,8), (7,5), (7,6), (7,7), (8,5), (8,6), (9,5): each is within 4 of (6,4) or (3,7). A Duo fired from there may take a left Claw instead of a new one and leave a new Claw alive.
- **Where the three new Claws appear: keep the `top` tiles (8,7), (9,7), (9,6), 7 HP each.** From every safe tile above, all three are within 4 (e.g. from (10,5): 4, 3, 2; from (7,8): 2, 3, 4; from (10,8): 3, 2, 3). They also stand on the cub's side, so the line reads "they came for the cub".
- **Damage:** (3 + 8) × the lowest mash, 0.7 = 7.7 per target, against 7 HP: every target dies on any mash. Tutorial tier changes only the enemies' damage, not the Duo's.
- **Why the player will usually be on a safe tile:** Mark and Lucy have just killed the Claws by the mother, (9,8) and (10,7), which are in the safe block. They come up the corridor (8,3)–(8,5) and fight at the top right.

**To check in play (Memory 4):**

1. What a reveal does when one of its tiles is taken: Mark or Lucy may be standing on (8,7) or (9,7) after killing the Claws near the cub. If the reveal skips or blocks, move the `top` tiles to free cells in the safe block next to the cub ((7,8), (8,8), (10,8)) and re-check.
2. Where the Duo's 4 counts from (Mark or Lucy), and where cold players fire it from: any Duo fired from a risky tile that leaves a new Claw alive.
3. That the paired condition completes whichever comes last (John's step or the last kill).
4. Whether the three new Claws (alert) act before the Duo if the stage completes after Mark and Lucy have spent their AP: they then walk toward Mark and Lucy, closer still, which only helps.
5. John's walk from (7,2) to the mouth (6 steps, no cap now) and Mark and Lucy reaching the den with John in the passage (open from the paper levels).

---

## The search: the River and the Ridge

**Shared rules for both pair missions.**

- **Tier Early** (×1 HP, ×0.75 damage, CR-32) with **per-instance HP factors** (data). **Layouts now, numbers after the Family Roles house-rule session, played on these two levels** (D-466). The factors below are start values for that session.
- **Fight beats are awake** (D-468). Only the Ridge's corridor sleeps, and there waking it is part of the move, not a decision.
- **No panels, no captions.** The Asleep panel and sight beat go (the marker stays), the role panels go (THJ: the prompt teaches itself). The first-sleeper handle comes off both levels.
- **Teaching = the board, one line, the objective, the aim preview** (D-467). The Synergy's line plays as its stage starts (an `OnCompleteSequence`, data). The objective names the goal, not the steps ("Silence the archers."). No goal tile in either lesson.
- **A clue on every beat, placed in the grids** (`note … clue` with the line it carries).
- **Family moves first on the Ridge** (D-468, reverses D-353).
- Rewards as built (D-455).

### The River (John + Lucy), reworked `GB_s1-river`

Prefab coordinates (no offset; read back 2026-11-09). Cells removed from the as-built map: the island tiles around each Archer (8,5 8,6 9,6, 13,6 14,5 14,6, 8,1 8,0 9,0) and the empty south-east island (13,0 13,1 14,0 14,1). Two Claws added on the far bank. Distances are grid steps (4-way).

```grid id=after-river title="The River, after the Hearth (prefab coordinates)"
# # . . . . # # # # # . # # # # #
# . . . . . . # # a # . # a # # #
# . . . . . c # # # . . . # # c .
U J . . . c . . . . . . . . c . .
# . . . . . c # # # . . . # # . .
# . . . . . . # # a # . # # # # #
# # . . . . # # # # # . # # # # #
--
zone 0,3 1,3 lucy Sheltered
cells 5,3 6,4 6,2 enemy awake at start
cells 9,5 13,5 9,1 enemy awake at start
note 3,3 beat 1
note 6,3 clue R7-2/3 prints and blood
arrow 11,3 10,4 9,5 lucy dy=-6 Flare
arrow 11,3 12,4 13,5 lucy
arrow 11,3 10,2 9,1 lucy
arrow 12,2 11,3 lucy ember John
range 14,3 2 enemy wake together
step 11,3 2
note 12,2 out of their reach
note 16,3 clue R7-4/5
level name The River
level tier early
```

| Item | Plan |
|---|---|
| Source | `GB_s1-river`, cells and units as above. Read back with `level_to_grid.py` first; rebuild plus a re-run of an updated **Wire Search: River** if nothing was hand-edited since |
| Challenges (beat 1, the clearing) | Hearth: **John's guard and Shield Up → Wrath → the punish** (Memory 3) and **Lucy's Cyclone** (Memory 2), under a real rush |
| Teaches and asks (beat 2, the ford) | **Shield Flare**: three awake Archers on 1-tile islands; the only tiles out of all their reach from which anything hits all three are John on 11,3 and Lucy embering him from 12,2 |
| Squad | Lucy 0,3, John 1,3 (Papa's Shelter shown at start, as built) |
| Enemies (start values) | Clearing: 3 Dark Claws (5,3 6,4 6,2), factor 0.6 (≈ 9.6), **start alert**. Ford: 3 Archer Goblins on 1-tile islands 9,5 / 13,5 / 9,1 (cannot move), **start alert**, factor 0.5 (≈ 12). Far bank: 2 Dark Claws 14,3 / 15,4, Unaware, factor 0.6 |
| Beat 1 | Claws move 4: 5,3 reaches 2,3 on enemy turn 1. ★ John Shield Up beside Lucy (his guard takes their hits and stacks Wrath), then a Wrath Shield Dash with Lucy's embers. ★ Cyclone in the clearing to split the rush. ● Sword and embers one at a time: Lucy (15 HP) takes 4–5 a hit if she strays from John. ~2 rounds. Its difficulty is set by the Family Role outcome (F6) |
| Stage 1 → 2 | Clearing dead → sequence: the clue (6,3, R7-2/3), camera across the ford to the islands, then John "Lucy. If it gets hot, aim at me." / Lucy "*At* you?" / John "Trust me." (R7-7 to R7-9). New objective **"Silence the archers."** (the three Archers dead) |
| Beat 2 (verified distances) | Awake Archers (reach 3) shoot anyone within 3. 11,3 is 4 from all three islands; 12,2 is 4 from 13,5 and 9,1 and 6 from 9,5: **both out of every Archer's reach**. From 11,3 each island is 2 diagonal: copies via 10,4, 12,4 and 10,2 (all floor). ★ John: move to 11,3 + Shield Up; Lucy: to 12,2 (2 from John) + ember **him** (the preview shows the copies) → the copies hit all three Archers, nobody in reach. Repeat next turn. ● Lucy embers an island directly: every tile within 3 of an island is in that Archer's reach, so it shoots back (6 × 0.75 = 4.5) unless her volley kills it first, which needs more than its 12 HP (sheltered volley 4 + 3 + 3 = 10) |
| Why 12 HP (start value) | Plain: a sheltered volley never kills an Archer in one turn, so each shoots back at least once. ★: **if every ember of a volley flares** off John, an unsheltered volley (4 + 3) puts 7 on each Archer: two Flares kill all three. **If only the main ember flares**, it puts 4 on each: drop the factor to 0.33 (≈ 8) for two Flares; the ★ then wins on safety. **To check before building:** which embers flare, and whether sidewinders spread or stack |
| Stage 3 | Defeat all (the far-bank pair, woken when John stops on 11,3, 3 from 14,3). End: the far-bank close-up (R7-4/5, as built) |
| FTP | Starts full (8) |
| Fallback | A player who never embers John wins slower and hurt. The aim preview is the lesson; if a cold player still misses it: a `GuidedAbilityHint` pulse on Fire Embers once John has Shield Up on 11,3 (**to check** whether a hint condition can test that) |
| Time | ~5 min (4–5 rounds) |

### The Ridge (Linda + Mark), reworked `GB_s2-ridge`

Prefab coordinates (as built, read back 2026-11-09; the rush pack moves, a Claw is added at 10,1).

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
note 3,2 clue G9-2 herbs
arrow 5,1 8,1 mark dy=-10 Vault
arrow 4,1 8,1 linda dy=6 out
arrow 8,1 4,1 mark dy=12 back
step 8,1 2
note 12,1 clue G9-3/4
level name The Ridge
level tier early
```

| Item | Plan |
|---|---|
| Source | `GB_s2-ridge`; rebuild + an updated **Wire Search: Ridge**, same check as the River |
| Challenges (beat 1, the pack) | Hearth: **Explosive Arrow on a packed group** (Memory 1) and **Fist Blitz + Continuous Attack** (Memory 4) |
| Teaches and asks (beat 2, the corridor) | **Catch & Return**: two Claws queued between Linda and Mark, a third waiting where Mark lands |
| Squad | Linda 1,1, Mark 2,1. **The family acts first** (D-468) |
| Enemies (start values) | Pack: 4 Dark Claws 1,4 / 0,4 / 2,4 / 1,5, **start alert**, factor 0.8 (≈ 12.8). Corridor: 6,1 / 7,1 asleep, factor 0.85 (≈ 13.6). End: 10,1 asleep (wakes when Mark lands on 8,1, 2 away), factor 0.6 |
| Beat 1 (falloff 1.0) | ★ Explosive Arrow from 1,1 on 1,4 (3, within 5): all four take 8 → 4.8 left. Mark to 2,2, Fist Blitz on 2,4 (8) kills, he steps in, Continuous Attack swings at the lowest within 2 (≈ 8, kills; FTP 1), a second swing (FTP 2; total 3 of 5) kills; Linda's second AP: bow (6) finishes the last. **All four in one turn.** ● Two plain shots up column 1 pierce 1,4 and 1,5 for 12 each (< 12.8: none die), Fist Blitz 8 kills nothing so no chain: four Claws hit back (~4.5 each) |
| Stage 1 → 2 | Pack dead → sequence: the clue (3,2, G9-2), camera down the corridor, Mark "Linda. Shoot at me." / Linda "Gladly." / Mark "From the far side." (G9-6 to G9-8; narrative may soften the last line). Objective **"Clear the corridor."** |
| Beat 2 | ★ Mark to 5,1, Vault to 8,1 (3, over the queue, 2 on 7,1; Vault over units: confirm in play); Linda to 4,1, bow along row 1 (the preview shows the return lane "if caught"): 6 on 6,1 and 7,1, then Mark (4 away) → the catch → the return copy hits both again for 6: 7,1 dies (14 vs 13.6), 6,1 at 1.6. Mark's second AP: Fist Blitz on 6,1 kills → Continuous Attack on 10,1 (2 away) kills. **Three Claws, one Linda AP, her arrow back.** ● Linda's two plain shots pierce both for 12, Mark's Blitz and a swing kill both, two arrows land under the last Claw, and 10,1 is untouched. The catch's edge here is an AP and two arrows, not survival |
| Catch prompt | Its first use in the game: if the catch QTE's short wait (D-273) is a per-ability value, use the standard wait on the Ridge (data, **to check**) |
| FTP | Starts full (5). Continuous Attack costs 1, then 2, then 3 FTP in a chain, so 5 buys two swings. With roles as built, Watch and the counter also spend it (F5) |
| Clue | End close-up on 12,1 (G9-3/4, as built) |
| Fallback | The plain play still wins, hurt (beat 1) or slower (beat 2). Hint fallback for the catch: a `GuidedAbilityHint` on Linda's bow once Mark stands past the queue (**to check**) |
| Time | ~4 min (3–4 rounds) |

---

## M2 · The Trail: the Trailhead, the route choice, The Pile (D-469)

**Structure (as built, kept):** the Trailhead → mission map → *Follow the blood* **or** *Follow the tracks* → *The Pile*. `M2 - The Trail.asset` level graph unchanged.

**Mission rules (changed):** Roster Linda, Lucy + John or Mark (D-172). Tier Early. **Every enemy starts alert** in every M2 level (`level alert all`). **The Linda–Lucy Duo is locked in all four M2 levels** (`LevelAbilityLock`, data, D-470). **FTP starts full** at the Trailhead (the −99 drain goes). The Pass-by panel and the Items panel stay cut, and nothing in the route choice needs them back: Pass-by's job was to fill FTP for the Duo, and the Duo is locked; items stay in stock with the pouch bob (CR-52). The tally's rematch line (P8) plays at the Trailhead's start, with the "stays home" line. Encore's cue stays on *Follow the tracks* only (its first use, D-334); *Follow the blood* teaches nothing new.

**Deploy order changes in all three early levels:** Linda in front (2,1), Lucy 1,1, the free pick at the back (0,1). With Pass-by no longer taught here, Linda no longer starts behind the family in a 1-wide trail, and every level's first answer is hers.

**The route choice's two questions:** *tracks* is a ranged question (Archers on a ledge, a queue coming down the trail); *blood* is a melee one (two gullies emptying onto one junction). The free pick's Synergy gets a ★ in both.

### The Trailhead (Linda, Lucy + John or Mark), reworked

The as-built enemy-free corridor, widened to 9 cells, with two awake Claws in the trail. One turn, Linda's pierce from Memory 1. Winning it opens the map, as before (the map opens only after a won level).

```grid id=after-trailhead title="M2 · The Trailhead, a one-turn fight"
# # # # # # # # #
J U L . . c c . .
# # # # # # # # #
--
arrow 2,1 6,1 linda dy=-8 bow pierce: both
note 0,1 the pick
level name The Trailhead
level tier early
level alert all
level deploy 0,1
```

| Item | Plan |
|---|---|
| Source | The Trailhead prefab (name to check in the M2 graph); cells widened from 7 to 9, the exit tile removed; updated **Wire Search: Trail** |
| Question | Two Claws in a 1-wide trail, lined up: does the player use Linda's pierce? |
| Enemies | Dark Claws 5,1 / 6,1 (3 and 4 from Linda: both inside her bow's 4), factor 0.6 (≈ 9.6), alert |
| Answers (falloff 1.0) | ★ Linda's bow along row 1, twice: 6 + 6 on both, both die (12 ≥ 9.6), before they move. ★ Explosive Arrow on 5,1 (8 on both) + one bow shot. ● Lucy can't reach past Linda in the 1-wide trail (3 from 1,1 reaches 4,1 only): the Claws reach Linda and hit her (~4.5 each) |
| Win | Defeat all → the level is won → the mission map opens (as built) |
| Cues | Start: the rematch line (P8) and the "stays home" line (narrative) |
| Time | ~1 min (1 round) |

### Route B · *Follow the tracks* (Linda, Lucy + John or Mark), reworked `GB_m2-tracks`

Prefab coordinates. The as-built map widened by two columns at the east end (9,1 and 10,1 new cells); rows 2–3 end at x5; the Claw on 7,3 moves into the trail.

**Fix (coordinator's flag):** the first revision had Linda pierce both ledge Archers from 4,1, but 4,6 is 5 from 4,1 and her bow reaches 4. Now she fires from **4,2** in the pocket: 4,5 is 3 away and 4,6 is 4, both inside her 4; she stands inside 4,5's reach (3), which doesn't matter when both die on her turn. Still to check: arrows cross the gap row (y4) (the as-built Duo shot through it relied on it too).

```grid id=after-trail title="M2 · Follow the tracks (prefab coordinates)"
# # # # a # # # # # #
# # # # a # # # # # #
_ _ _ _ _ _ _ _ _ _ _
# . . . . . # # # # #
# . . . . . # # # # #
J U L . . . . c c . c
# # # # # # # # # # #
--
range 4,5 3 enemy Archer reach
arrow 4,2 4,6 linda dx=-8 bow pierce: both Archers
arrow 3,1 8,1 linda dy=8 Explosive
note 2,3 clue: tracks
level name Follow the tracks
level tier early
level alert all
level deploy 0,1
```

| Item | Plan |
|---|---|
| Source | `GB_m2-tracks`; rebuild + an updated **Wire Search: Trail**. Keeps its stages (both Archers dead → the Encore cue, then defeat all) |
| Question | An awake queue coming down the narrow trail, and two Archers on a ledge covering the side pocket: kill the Archers first (one well-placed pierce from inside the pocket) or meet the rush? |
| Squad | Linda 2,1, Lucy 1,1, the pick 0,1 |
| Enemies | 2 Archer Goblins on the ledge 4,5 / 4,6 (static), factor 0.25 (≈ 6). Queue: Dark Claws 7,1 / 8,1 / 10,1, factor 0.6. All alert. Early |
| Answers | ★ Linda to 4,2 (3 steps), one bow shot up column 4: 6 on both Archers, both die, the arrow lands on 4,6 (the ledge: Encore later). But the queue arrives (7,1 moves 4, to 4,1 beside her): she spends the turn in the rush's path. ★ Explosive Arrow from 3,1 on 8,1 (5): 8 on 7,1 and 8,1 (→ 1.6), while the Archers keep the pocket (4,2, 3,3, 4,3, 5,3 are within 3 of 4,5). ★ (Mark) Vault over the queue in the trail, Linda's bow along row 1 for the catch. ★ (John) Shield Up in the trail as the queue arrives (guard + Wrath). ● Lucy embers the queue; anyone in the pocket takes Archer fire. No Duo (locked) |
| Encore | Unchanged cue on the "both Archers dead" stage (D-334) |
| Time | ~3 min (3 rounds) |

### Route A · *Follow the blood* (Linda, Lucy + John or Mark), reworked `GB_m2-blood`

Prefab coordinates, as-built cells (read back before rebuilding). Lucy's "Her blood." stays the route's story beat; the trail of blood runs east along row 1.

```grid id=after-blood title="M2 · Follow the blood (prefab coordinates)"
# # # # c # c # #
# # # # c # c # #
# # # # c # . # #
# # # # . # . # #
J U L . . . . . .
# # # # # # # # #
--
arrow 4,1 4,5 linda dx=-8 bow pierce up the gully
step 5,1 1
note 5,1 the junction
arrow 5,1 4,2 lucy Flare (John picked)
arrow 5,1 6,2 lucy
note 7,1 clue: her blood
level name Follow the blood
level tier early
level alert all
level deploy 0,1
```

| Item | Plan |
|---|---|
| Source | `GB_m2-blood`; cells as built; units re-placed (alert, new HP); updated **Wire Search: Trail**. The FTP/Pass-by panel goes |
| Question | Two gullies empty onto the trail two tiles apart. The family meets them at the junction (5,1), where one answer can hit both gully mouths (4,2 and 6,2) at once. Who holds it, and with what? |
| Squad | Linda 2,1, Lucy 1,1, the pick 0,1 |
| Enemies | Gully: 3 Dark Claws 4,3 / 4,4 / 4,5. Side gully: 2 Dark Claws 6,4 / 6,5. All factor 0.6 (≈ 9.6), alert (they come down on enemy turn 1). Early |
| Answers (verified distances) | ★ Linda to 4,1 (2 steps), bow up column 4: 4,3, 4,4, 4,5 are 2, 3, 4 away, all inside her 4: 6 on each (→ 3.6); the side pair comes down onto her. ★ Explosive Arrow on 4,4 from 3,1 (4): 8 on 4,3, 4,4, 4,5, then the column shot kills all three (needs Linda at 4,1 next turn). ★ (John) Shield Up on the junction 5,1: its diagonals are 4,2 and 6,2, the two gully mouths, 1 away (copies reach the first enemy within 2); Lucy embers John from 3,1 (2) → one Flare hits whatever stands at both mouths; his guard covers Linda and Lucy within 2. ★ (Mark) on 5,1: Fist Blitz on a Claw at 4,2 or 6,2, the kill chains Continuous Attack to the other mouth (2 apart). ● Fight each Claw as it comes out; the two gullies arrive together and Linda (front) takes the hits |
| Clue | 7,1, the blood trail onward (narrative) |
| Time | ~3.5 min (3 rounds) |

### The Pile (Linda, Lucy + John or Mark), rebuilt on `GB_m2-pile`'s footprint

Unchanged by THJ's answers. Prefab coordinates, same 10 × 7 footprint, new cells. The search comes first, is one move long and answers something; the fight comes after it, from both sides.

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
arrow 3,4 0,4 linda bow pierce
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
| The search (THJ: low tempo on purpose) | Start: the pile close-up, Lucy "Linda… what if she's in there?" / Linda "Then we find her. Together." (T11-3, T11-4). Objective **"Search the pile."**: any Bergson on a tile beside it (4,5 or 5,5, one move from the start row; the gold goal tile). **The search answers something before the ambush**: a partial-relief line, e.g. Lucy "No white fur… she's not here." (narrative), then the reveal. The rivalry barks stop here |
| After the search | Both hidden groups revealed (alert): three Claws in the west lane, two Claws and an Archer on the east perch. They act on the next enemy turn. Back to back |
| Enemies | West 0,4 / 1,4 / 2,4, east 9,4 / 9,3 Dark Claws, factor 0.6; Archer on the 1-tile perch 9,6, factor 0.25 (≈ 6: one bow shot). Early |
| Answers | West lane: ★ Linda's bow from 3,4 along row 4: 2,4, 1,4, 0,4 are 1, 2, 3 away, all pierced at 6 each; Lucy's embers finish; or Explosive on 1,4. East: ★ Linda's bow on the perch from 5,6 along row 6 (4, outside its reach; across 6,6–8,6, drawn as **rock**: **to check** arrows fly over rock), one shot kills it. ★ (Mark) Fist Blitz + Continuous Attack on the two east Claws once they close. ★ (John) Shield Flare from 7,4 reaches the perch via 8,5 (2; 7,4 is 4 from 9,6): 4 (or 7 if every ember flares) against 6. ★ Lucy's Cyclone on 6,4 or 7,5 splits the east pair (no ★ needs the family to pass it, P9). ● Embers on the perch from 7,5, inside its reach. Linda can't do both sides in one turn with three arrows: that is the pressure |
| The ending | **No Duo** (locked, D-470). The level ends on the last kill, the sisters back to back, the tally alone on screen, then "Still counting?" / "…No." over the quiet. End as built after that (the tally fade, the free pick's line, Lucy's motive line T11-8) |
| FTP | Carried (full at the Trailhead). Spent only by roles (as built) and Continuous Attack |
| Time | ~4.5 min (search + 3 rounds) |

---

## Home

| Moment | Today | Approved | Work |
|---|---|---|---|
| New game | Menu, then the Hearth's levels | **Home on the storytelling idle** (`MargaretStoryNight`, Margaret hosts, D-178), H0-1 to H0-4, then the Hearth starts by itself. **Stations locked** until after the Hearth | Home flow: small code. Tech plan (coordinator) |
| After the Hearth | Hearth close, "Two go out, two stay", World map page | Unchanged | — |
| Visit 1 (after the first pair mission) | The Workshop page only | **The handover at the door** (D-472): the returning pair meets the leaving pair. One real clue line from the returning pair (their mission's end close-up), the go-between joke (V1-2a to V1-4a, or V1-2b to V1-4b by order) and Ben's "You two are next? Hand them over." (V1-1), into the Workshop pick (existing page). About 1 minute | Data: a `DialogNodeSequence` as each pair mission's completion scene. **Small code:** the gate that plays it only after the *first* pair mission (C5c's `GetLastCompletedMission` is a model) |
| Visit 2 | Skill tree page + guided spend; Map Table clue scene on the Trail pin | Unchanged. The Map Table's clue lines (V2-3, V2-6) now repeat clues placed in the grids | — |
| Visit 3 | Yard → Bond Lv 2 → Margaret's point → pan back | **The Family tree opens by itself on the Family tab after the pan back** (reverses C5's "no tab opens by itself"), the sisters' node pulsing (the existing guided-spend marker) | Small code: the upgrades panel API from C5c (D-356) |

---

## What to cut or delay

| Item | Was | Now | Why |
|---|---|---|---|
| Asleep panel + sight beat | Required, first pair mission | **Cut** (the marker stays) | THJ. Safe because no level hinges on a wake |
| Lucy's / Mark's Family Role panels | River / Ridge start | **Cut** | THJ: the prompt teaches itself (F4) |
| Watch in Memory 1 and its panel page | Memory 1 | **Cut** (FTP drained, D-473) | THJ |
| Turn caps and "Turns left in the memory" | All memories | **Cut** | THJ |
| FTP drain + Pass-by panel | M2 trailhead and routes | **Delayed** to after M4 (Pass-by still works) | The Duo is locked in M2, so there's nothing to fill FTP for |
| Items panel | The Pile | **Cut** (items stay in stock) | The pouch bob cues them |
| Empty Trailhead walk | M2 level 1 | **Replaced** by a one-turn fight | THJ: too vague |
| Sisters' Duo in M2 | Open; route A's framed first Duo | **Delayed** to M4, after the Yard (D-470) | Keeps The Pile sad and the Yard's discovery intact |
| Kept | The route choice and mission map (D-469); Papa's Shelter shown at River start; Encore's cue on the tracks route; the tally; Workshop, skill tree, Bond Yard, Family tree | | Each is shown once, at the moment it pays off |

Net: seven introductions cut or delayed (Asleep, two role panels, Watch in Memory 1, FTP drain and Pass-by, Items, the sisters' Duo), two existing optional Synergies made into lessons, one preview rule added.

---

## Family Role dependencies

The Family Roles track runs a three-step test with a stop rule (D-460): roles lock **as built** (A) if its play session says no, else a dev switch for **kept AP** (C; D-462: John one guard per kept AP). Round 3 adds the direction "no role works alone" (D-464). **The levels' layouts hold under each outcome; their difficulty numbers don't**, which is why the River's and the Ridge's numbers wait for the session (D-466).

| # | Place | As built (A) | Kept AP (C) / "no role alone" |
|---|---|---|---|
| F1 | Memory 1 | FTP drained (D-473): Watch can't pay; the meter shows empty | Linda alone is silent (D-464): remove the drain |
| F2 | Memory 3, John's role alone | Waits for the redesign (D-473); all roles fire, as THJ played it | The redesign places its first lesson here (round 3, S6) |
| F3 | Memory 4 | As built | Mostly automatic (turn-1 AP limits) |
| F4 | River / Ridge, no role panels | Lucy's and Mark's prompts appear untaught, under real damage in the River's awake rush; Watch and Mark's counter both first seen in the Ridge pack (family-first helps) | Each needs kept AP, taught in Memory 3; the rushes become keep-or-spend questions |
| F5 | Ridge FTP (max 5) | Watch, the counter and Continuous Attack (1, 2, 3) share it: two role answers leave one swing | Roles spend no FTP: two swings |
| F6 | Difficulty of every John level | His guard redirects every hit within 2 at ×0.5, unlimited: the River's clearing and the blood route's junction are soft; levers: Claw factor up, then Standard tier | One guard per kept AP: much harder; the ford's ★ turn (move + Shield Up) leaves John nothing to keep, so Lucy stands out of reach (12,2, built in) |
| F7 | M2 | Roles spend FTP; with the Duo locked, nothing else competes but Continuous Attack | FTP is spent by Continuous Attack only |

**What this plan asks of the Family Roles track:** that its house-rule session be played on the reworked River and Ridge (D-466), that Memory 3 shows only John's role (D-473), and that Memory 1's drain be removed if Linda alone is silent.

---

## Small UI rules

| Item | Rule | Work | Scope |
|---|---|---|---|
| **Synergy aim preview** (D-467) | **When an aim would set off a Synergy, the preview shows where its copies go and what they hit**, with the usual damage numbers, and nothing on the ally it bounces off. Covers Tempest Bloom (arrow into a Cyclone: the copies' lanes), Shield Flare (Lucy hovering a shielded John: the four diagonal copies), Catch & Return (Linda's lane reaching Mark: the return lane, drawn as "if caught"). Same reach rule as every preview (CR-37). One element: the existing aim preview, extended. No caption | New code in the attack preview (`UnitThreatAnalysis` reach helpers, `PlayerController` preview path; read, not traced); its own tech plan. If priced high: Shield Flare first, the Bloom second, the return third | all |
| Goal tile | The win-objective highlight is no longer green (green means HP bars and heals, CR-49, CR-53). Proposal: a warm gold outline; the art call is THJ's. Used by The Pile's search and Memory 4's mouth | Data: the `gridCellHighlightLevelGoal` sprite or its tint on the `GridCell` prefab | all |
| Objective feedback | When an objective is met, its line ticks and pulses once with a short sound, and the panel unfolds if it was folded | New code, small (objectives panel UI, not core) | all |
| One result line per level | Optional summary line on a level; when set, the level-won panel shows it alone | New code, small (`MissionEndPanelUI`), off by default | all |
| Level-design rule | A ranged enemy meant to stay put stands on a 1-tile island or perch, so a Synergy aimed at it can't be dodged by its own move. Linda (4) outranges any static Archer (3), so a static Archer is her free target: keep its HP to one shot, or put it where her firing tiles cost her something. **A pierce reaches only cells within the bow's 4** (the tracks fix) | Catalogue knob in `design/level-chunks.md` | all |

---

## Lens notes

### Creative

**Target experience.** After the Hearth the family stops telling stories and starts being tested. Each search trip should feel like the habits from the fireside, now needed for real, with one new trick the pair finds together ("Aim at me." / "Shoot at me."), found by aiming. M2 should feel like the family's exam, with one worried choice (her blood or the tracks), and The Pile like the moment the joke dies.

**The moment designed for:** The Pile's last kill. The search found no white fur, so they fight with hope; the sisters stand back to back, the tally alone on screen, nobody scoring; the last Claw drops, and "Still counting?" / "…No." lands on silence. Their first Duo together waits for M4, after the Yard.

Secondary: the River's three islands lit at once by one Flare off Papa's shield; the Ridge's pack gone in one turn; the blood route's two gullies met at one junction; Memory 4's John planted on the mouth while Mark and Lucy clear the den, then the Duo taking the last three.

**Story on every beat.** Each beat's clue is on its grid (R7-2/3, R7-4/5, G9-2, G9-3/4, the tracks, her blood), so visit 2's Map Table recites what the player saw.

### Systems

- **Levers** (start values; River and Ridge set at the Family Roles session): tier Early; per-instance HP: River clearing Claws 0.6, ford Archers 0.5 (0.33 if only the main ember flares); Ridge pack 0.8, corridor 0.85, 10,1 0.6; M2 Claws 0.6, M2 Archers 0.25. Every fight beat alert; Ridge family first; FTP full in M2; sisters' Duo locked in M2; Linda in front in M2's first three levels.
- **Interactions:** Shield Flare needs John's move + Shield Up and Lucy's ember: a full turn of both. Catch & Return is arrow-neutral (LI-9) and gives no AP (D-332). Continuous Attack costs 1, 2, 3 FTP in a chain (MA-2). Hidden groups revealed under "all start alert" come in alert. Arrow falloff 1.0; a pierce reaches cells within 4.
- **Failure cases:** the Flare never found (preview, then hint); the ford's ★ only safer, not faster (factor 0.33); the Ridge chain cut by FTP under A (F5); Memory 4's Duo fired from a risky tile (checked in play); the Pile's perch shot blocked by rock (to check); the tracks pierce blocked by the gap row (to check).
- **Dominant strategy check:** John + Lucy at the ford and John at the blood junction dominate there by design. Linda's range-4 bow against static Archers: kept, made one decisive shot. Under A, John's guard soaks the River and the junction (F6): first lever the Claws' factor, then Standard tier.

### UX

| Moment | Shown | The player clicks | Likeliest misread |
|---|---|---|---|
| River, ford reached | Camera over the islands, John's line, objective "Silence the archers." Shift shows the Archers' reach (awake: attack reach, so 11,3 and 12,2 read as safe) | John to 11,3, Shield Up; Lucy hovers John → the preview shows four copies, three hits, nothing on John | Embers an Archer instead (the habit). Order matters: Shield Up first |
| Ridge, corridor | Camera down the corridor, Mark's line | Mark past the queue; Linda aims along row 1 → preview shows the return lane "if caught" | Linda shoots before Mark is past; misses the catch press (standard wait if it can be set) |
| Trailhead | Two Claws in line in the trail | Linda's bow | Moves Lucy first and blocks nothing: the trail is 1 wide with Linda in front, so only Linda can shoot |
| Tracks, the pocket | The Archers' reach (Shift) and the awake queue | Linda to 4,2 | Fires from 4,1 and hits only 4,5 (the bow's 4): the preview shows which Archers the line reaches |
| Blood, the junction | Two gullies, both groups awake | The pick to 5,1 | Fights each Claw as it comes out; the preview (John) or the chain (Mark) shows the double |
| The Pile, search | "Search the pile." and the gold goal tile beside it | One Bergson one step | Thinks the level is a cutscene and waits: the objective and the tile carry it |
| Memory 4, the hold | "John holds the mouth. Clear the den." with the gold tile on the mouth | John to the mouth; Mark and Lucy into the den | Expects the left-side Claws to count; the objective names the den. Then fires the Duo from beside the mouth (risky tile): checked in play |
| Memory result | One summary line | Continue | — |

**On-screen elements added:** one (the Synergy aim preview, an extension of the existing preview). Removed: six panels, the turn-cap line, the lessons' goal tile.

---

## USP check

- **Family Roles:** neutral on purpose. Memory 1 silenced by data (THJ); everything else handed to the Family Roles track, with the River and Ridge as its test ground.
- **Synergies:** strengthened. Shield Flare and Catch & Return go from optional discoveries to situations that ask for them, re-tested in both M2 routes by the free pick; one aim-preview rule makes every Synergy's outcome visible before the click.
- **Duos:** kept as finishers (THJ). Memory 4's Duo always ends the telling; the sisters' first real Duo moves to M4, after the Yard.
- **Managing the Home as a Family:** strengthened. The game opens at Home; visit 1 gets the handover scene; visit 3 opens the Family tree on the best moment of the hour.

## Critics

**Real, independent critics, run 2026-11-10 by the coordinator:** three read-only Explore agents, each told to read and follow `.claude/agents/miso-design-critic.md`, one lens each (the `miso-design-critic` agent type wasn't available in the session). Each saw this plan and the pacing check, not the others' output. Full text: [`reports/after-hearth-critics/`](../../reports/after-hearth-critics/) (`creative.md`, `systems.md`, `ux.md`). All three: ship B with changes; A, C, D no.

**Superseded by THJ's answers since:** the pools-stop action and the fade-all mode for Memory 4 (D-471: THJ's own design, data only, pools run); the route cut (D-469: kept); dropping Memory 1's drain (D-473: drained now, the UX critic's empty-meter risk accepted).

### Systems critic

| Objection | My response | What changed |
|---|---|---|
| **Strongest:** at the plan's own numbers the plain play beats or matches the ★ in most beats; the River ford goes from trivial (roles as built) to lethal (kept AP); "holds under either outcome" is false for its central beat | Right. Root: no caps + sleeping targets = the safe play is always open | Every fight beat awake; ford Archers awake on islands with 11,3 / 12,2 the only safe Flare tiles; River and Ridge numbers tuned after the Family Roles session (D-466); acceptance criterion rewritten (worse, not forbidden) |
| Arrow falloff is 1.0; Flare copies ≈ 4 each; Continuous Attack costs 1/2/3 FTP | Right | Ridge re-derived; F5 corrected; Flare damage tied to the open check |
| Pools need `ShouldTick = false`; activation actions don't stop them | Right | Moot: pools run as built (D-471) |
| Chained Assault may take a nearer leftover and leave a target alive | Right | THJ's design plus the paper check above: safe tiles listed, the risky ones checked in play |
| Marks-Sisters listed as a ★ in The Trail; the Duo can open The Pile | Right | Sisters' Duo locked in M2 (D-470) |
| Static Archers are free targets for Linda's range 4 | Right | M2 Archers at 6 HP (one shot) |
| The ★ must win in every beat | **Partly disagree.** With no caps nothing can forbid the plain play; the Ridge corridor's catch is an efficiency answer (an AP and two arrows), shown by the preview | Stated in the Ridge table |

### Creative critic

| Objection | My response | What changed |
|---|---|---|
| **Strongest:** The Pile's Duo finisher turns the joke's death into a triumph and empties the Yard scene | Right | Duo locked in M2 (D-470); The Pile ends back to back, tally alone |
| Clue lines unplaced | Right | Clues on every grid |
| A goal tile for John is a tutorial step in disguise | Right | "Silence the archers.", no tile |
| The Pile's search is a genre ambush trigger | Right | The search answers first |
| Memory 4 ends with enemies on the board | Partly addressed | THJ's design (D-471) leaves left-side Claws on the board; the outro lines no longer claim otherwise |
| The route choice was the one place the player voiced worry | THJ agreed | Route choice kept (D-469) |

### UX critic

| Objection | My response | What changed |
|---|---|---|
| **Strongest:** lines and a goal tile don't show the rule; the tile vanishes before Lucy acts; aiming at family reads as friendly fire | Right | Synergy aim preview (D-467); objective persists until the Archers die |
| Waking is a decision but invisible | Right | No level hinges on a wake (all M2 alert, fight beats awake) |
| Memory 4: board and line disagree | Right | Objective names the den; outro lines fixed |
| Memory 1's drained FTP bar reads as broken | Right, THJ accepted the risk | Drain kept (D-473); undone if the redesign silences Linda alone |
| Home start must lock stations; Family tree "spend, then close" | Right | Both in the Home table |

---

## Recommendation

Option B as approved. It fixes both roots (introductions without tests; sleeping targets that make every test optional), cuts seven introductions, adds one preview rule, and keeps the first hour under 45 minutes at THJ's pace.

### Time (THJ's pace; paper estimates, not timed)

| Step | Today (pacing check) | Approved |
|---|---|---|
| Home start + Hearth | ~13 | ~13.5 |
| Home after the Hearth | ~2 | ~2 |
| First pair mission | ~1.5–8 | ~4.5 |
| Visit 1 (handover + Workshop) | ~2 | ~2 |
| Second pair mission | ~1.5–8 | ~4.5 |
| Visit 2 | ~2 | ~2 |
| M2 | ~14 (3 levels + map) | ~10 (pick 0.5, Trailhead 1, map 0.5, route 3–3.5, The Pile 4.5) |
| Visit 3 + send-off | ~3.5 (not logged) | ~3.5 |
| **Total** | **~46** | **~42–43** |

The route choice adds about +2 against the two-level version (the Trailhead fight and the map). A cold player runs about ×1.3: ~55, inside the design's 45–60.

### To check before building (each decides a number or a tile)

1. Which embers of a volley flare off a shielded John, and whether sidewinders spread or stack (River ford factor 0.5 or 0.33).
2. Whether arrows cross a gap row (tracks: the shot from 4,2; John's Flare via 3,4) and rock (The Pile: the perch shot).
3. Whether the catch prompt's wait is per ability (Ridge).
4. What a reveal does on a taken tile (Memory 4's new Claws).
5. Whether the Lucy wiring tool carries the ten/two/four gag before it is re-run.
6. The Trailhead prefab's name and whether its wiring sits in **Wire Search: Trail**.

### Playtest signal (THJ's timed run, then the cold run)

- **Worked:** in each pair mission the combat log shows the ★ (Wrath Shield Dash or Cyclone; a Flare hitting 2+ Archers; Explosive Arrow then Continuous Attack; a catch), and the plain play, where tried, cost a round or a third of a hero's HP more; rounds per level 3–5 (Trailhead 1); THJ says abilities felt needed; cold players hover John at the ford and fire; in Memory 4 the Duo kills all three every time; The Pile's ending is described as sad, not as a win; the Map Table's clues are ones the player remembers.
- **Failed:** the plain play wins at full HP (raise the Claw factors, then Standard tier); Flare or catch unused by a cold player despite the preview (hint fallbacks); a Duo in Memory 4 leaves a Claw alive (move the reveal tiles, re-check); total above ~45 at THJ's pace (cut the tracks route's queue to two Claws, then the blood route's side gully to one).

### Build order

Each its own chunk; data-only chunks need no tech plan.

| # | Chunk | Kind | Waits on |
|---|---|---|---|
| 1 | **Hearth memories 1–3:** caps off, Memory 1 FP drain (−99) and the Watch page out, Lucy's multi-shot page | Data through the wiring tools (editor code re-run; check the Lucy gag first) | — |
| 2 | **Memory 4 (D-471):** stages 2–3 merged into the paired hold-and-clear stage, `top` reveal and Duo unlock retimed to it, (9,8)/(10,7) kept as the cub Claws, caps off, the Duo stage | Data, prefab by hand (THJ or the implementer with his OK) | — |
| 3 | **M2 levels:** the Trailhead fight, *Follow the tracks*, *Follow the blood*, *The Pile* rebuilt from these blocks; the sisters' Duo locked in all four (`LevelAbilityLock`); FTP full; Pass-by and Items panels out; the rematch line's slot | Level + wiring-tool (editor) work and data; no runtime code | — |
| 4 | **River and Ridge layouts** from these blocks, start values in | Level + wiring-tool work | Numbers: the Family Roles house-rule session played on them (D-466) |
| 5 | **Goal tile colour** | Data (sprite or tint) | THJ's art call |
| 6 | **Small UI, one tech plan:** objective feedback + the optional result summary line (the memories' lines from narrative) | Small non-core code (all) | Narrative for the lines |
| 7 | **Synergy aim preview**, its own tech plan | Non-core code in the attack preview (all) | — (the River and Ridge's teaching leans on it before the cold run) |
| 8 | **Home, one tech plan:** new-game start with stations locked, the visit-1 gate (handover scene data), the Family tree auto-open | Small code + data | Narrative for the handover lines |
| 9 | THJ's timed run, then the cold playtest | Play | 1–8 (the Family Roles session for 4's numbers) |

Narrative (parallel): result lines, Lucy's multi-shot page, clue lines at the placed tiles, the River and Ridge objectives, Memory 4's stage-2 line and an outro that doesn't claim the last Claw, the Pile's partial-relief line, the Trailhead's rematch and "stays home" lines, the visit-1 handover.

---

## Answers

THJ, 2026-11-10 (logged by the coordinator).

1. **River and Ridge timing (D-466):** layouts now; enemy numbers after the Family Roles play session, played on these two levels. As recommended.
2. **Teaching after the Hearth (D-467):** the Synergy aim preview rule (Tempest Bloom, Shield Flare, Catch & Return), no caption. Replaces the Bloom-only preview. As recommended.
3. **Difficulty levers (D-468):** Early tier with lower per-enemy HP, every fight awake (the Ridge corridor still sleeps), the family first on the Ridge (reverses D-353); Standard tier as the first lever. As recommended.
4. **M2 structure (D-469):** **keep the route choice** (against the recommendation). The Trailhead gets a one-turn fight and both routes are reworked; built into [M2](#m2--the-trail-the-trailhead-the-route-choice-the-pile-d-469).
5. **The sisters' first Duo (D-470):** locked in M2, first in M4 after the Yard; The Pile ends back to back, the tally alone. As recommended; the lock is in all four M2 levels.
6. **Memory 4 (D-471):** **THJ's own design, data only:** John holds the mouth and the Claws near the cub die (one paired objective), then three new Claws come in, the only Duo targets; the Duo ends the memory; pools run as built. Replaces the pools-off and fade proposal; paper check in [Memory 4](#memory-4-john-holds-the-mouth-the-first-duo-finishes-it-d-471).
7. **Home visit 1 (D-472):** the handover scene, played only after the first pair mission. As recommended.
8. **Family Roles in the Hearth (D-473):** **drain Memory 1's FTP now** (against the recommendation); Memory 3's John-only roles wait for the redesign.
9. **Memory 0 for John (D-474):** no, for now.

---

## Docs to update

Now that the plan is approved, in this order.

- `design/gdd/missions-structure.md`: the onboarding missions (the Hearth's stages with no caps; Memory 1 FP drained; Memory 4's three stages; The River and The Ridge at Early with awake fight beats; M2: the Trailhead fight, both routes reworked, all alert, FTP full, sisters' Duo locked, items unchanged); MI-27's table (all M2 levels "all enemies start alert"; the River's and Ridge's per-instance alert); MI-18 note for the result summary line and the goal-tile colour.
- `design/gdd/combat-rules.md`: the Synergy aim-preview rule beside CR-37 (next free ID) once built.
- `design/gdd/family-systems.md`: a pointer from the Synergies table to the preview rule.
- `design/level-chunks.md`: the 1-tile island/perch knob with the Linda-outranges and pierce-reach caveats; link this plan from chunks 6, 13, 14, 23, 24.
- `plans/onboarding/2026-10-26-onboarding-levels.md`: mark The River, The Ridge and M2 sections superseded by this plan; the Hearth tables' cap rows; Memory 4's stages.
- `plans/onboarding/2026-10-25-onboarding-first-hour-design.md`: the flow table (M2 row; sisters' first Duo in M4), the S8 arc's Pile beat (no Duo).
- `plans/onboarding/onboarding-narrative-draft.md` (`miso-narrative`): the lines listed under Build order.
- Family Roles plans (coordinator relays): the three asks in [Family Role dependencies](#family-role-dependencies).
- `decisions.md` (coordinator): done (D-466 to D-474); the reversals to note: D-353 (Ridge enemy-first), D-355 (Pass-by panel), the levels plan's "Asleep panel required", C5's "no tab opens by itself", route A's framed first Duo.

## Risks

- **Paper balance.** HP factors, Flare copy damage and Archer damage at Early are assumptions; the River and Ridge numbers wait for the Family Roles session; each level has a lever and a to-check row.
- **The Family Roles track slips.** Then the River and Ridge stay at start values; fallback: tune them for roles as built.
- **Memory 4's Duo from a risky tile.** Paper says the usual play lands on a safe tile; the play check confirms.
- **Memory 1's empty FTP meter** (accepted by THJ): watch for it in the cold run.
- **Preview cost.** Three Synergy hooks; Shield Flare first if priced high.
- **Hand-edited prefabs.** Read each level back before rebuilding; Memory 4 by hand only (D-405); the Lucy wiring tool must carry the D-457 gag before any re-run.
- **Cyclone in narrow places** (P9): no ★ needs the family to pass a Cyclone; in the 1-wide trails (Trailhead, routes) a Cyclone is the player's own risk until the redesign.
- **`AIRegressionTest`** may shift with the new levels: stays known red, never re-baselined.

## Gates

Each build chunk: compile / EditMode (known red only) / review for code / THJ play check (feel and level chunks). Play check needs THJ's time: yes, the Family Roles session on the River and Ridge, then a timed run Home → M4 send-off, then a cold playtest.

Grids in this revision, to re-render: **changed** `after-trail` (renamed *Follow the tracks*: deploy order, the shot from 4,2), `after-river`, `after-ridge` and `after-pile` (unchanged since the last render, re-render is harmless); **new** `after-trailhead`, `after-blood`. Command: `python claude-handoff/tools/grid_render.py claude-handoff/plans/onboarding/2026-11-09-onboarding-after-hearth-design.md`.
