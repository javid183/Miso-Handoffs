# Onboarding after the Hearth: challenge what was taught

Size: L    Tier: 3 (level design and game feel of the first hour, Home flow, small all-scope UI rules)    Assigned to: miso-game-designer
Branch: `thj/after-hearth` (from `main` @ `e9bd6e885`, D-460 of 2026-11-10), scope **all**: `main` now holds the whole onboarding (D-456), so every rule here applies on every branch.
Status: waiting on THJ (critics folded in 2026-11-10)

Source: [`playtests/2026-11-09-pacing-check.md`](../../playtests/2026-11-09-pacing-check.md), findings P1 to P6 and THJ's answers of 02:13. Builds on the approved [first-hour design](2026-10-25-onboarding-first-hour-design.md), the [paper levels](2026-10-26-onboarding-levels.md) and the C3 to C5 build plans. Runs alongside the Family Roles track: [`plans/2026-11-09-family-roles-rethink-design.md`](../2026-11-09-family-roles-rethink-design.md) (D-460: paper, one house-rule session, a dev switch only if it says yes, else lock as built) and its [round 2/3 draft](../2026-11-09-family-roles-round2-design.md) (D-464, direction: no role works when its Bergson is alone). This plan redesigns no Family Role rule. **Where it can't hold under every outcome, it says so** ([Family Role dependencies](#family-role-dependencies)).

Revised 2026-11-10 after three independent critics (see [Critics](#critics)). Main changes: every challenge beat re-derived with the arrow falloff at 1.0 and enemies awake; the Synergy lessons taught by an aim preview instead of a goal tile; the sisters' Duo kept out of M2; Memory 4's leftovers fade and the pools visibly die; the Hearth's role changes handed to the Family Roles redesign; the River's and the Ridge's numbers tuned after the Family Roles play session.

## Why

THJ's timed play (2026-11-09): the Hearth works as a tutorial, but nothing after it challenges what it taught. The River, the Ridge and The Trail are too easy ("you do not feel the need of abilities"), The Pile is the weakest level, the Trailhead walk is vague, and the first hour carries "too many mechanics with too little challenge". Timing is fine (about 42 minutes to the end of The Trail) and must stay fast.

## Goal

After the Hearth, every level first challenges what the player already has, and anything new it teaches is one small pair Synergy that is then challenged too, in fewer and tighter levels, with Hearth → M4 send-off still at about 45 minutes at THJ's pace.

## Acceptance criteria

- [ ] No tutorial panel after the Hearth. Post-Hearth teaching is the board, one spoken line, an objective line and, if THJ agrees (Q2), the aim preview.
- [ ] Each pair mission opens on an **awake** fight whose ★ answer (★ = the intended, best answer; ● = the plain play that still works) is a Hearth tool (John's guard and Wrath, Lucy's Cyclone, Linda's Explosive Arrow, Mark's Fist Blitz chain).
- [ ] In each pair mission's combat log, the plain play costs at least one more round **or** about a third of a hero's HP more than the ★ play, measured under the Family Role setting in force at the play check (no caps exist, so the plain play is never forbidden, only worse).
- [ ] Each pair mission then teaches its pair Synergy (River: Shield Flare; Ridge: Catch & Return) and asks for it again in the same level.
- [ ] The Trail is two levels at most, with no walk longer than one move before the first enemy is in reach; no enemy that only sleeps decides a level (no wake-as-decision without a wake marker).
- [ ] No memory has a turn cap; each memory's result screen shows one objective line.
- [ ] Memory 4 ends with no enemy left on the board but the ones the Duo kills.
- [ ] A new game starts at Home on the storytelling idle (stations locked) and goes into the Hearth by itself; the Family tree opens by itself after the Yard scene.
- [ ] Hearth → M4 send-off plays in about 45 minutes at THJ's pace (paper: 41); no post-Hearth level runs past 5 rounds.

## Scope

In: the four Hearth memories (caps, result lines, Lucy's multi-shot page, Memory 4's ending), the River, the Ridge, The Trail (structure and both levels), the three Home visits' content and the new-game start, what to cut or delay, the all-scope UI items THJ listed (goal tile colour, objective feedback, the Synergy aim preview).
Out: Family Role rules and their Hearth exposure (the Family Roles track; this plan hands it one requirement), the Cyclone rules (P9, [`design/cyclone-redesign.md`](../../design/cyclone-redesign.md)), rewards (P7, closed by D-455), the tally line and bug (P8), final text (`miso-narrative`), M4's own levels beyond the send-off (one handoff: the sisters' first Duo, Q5).

## Touches

Systems: level prefabs `GB_m4-mark`, `GB_s1-river`, `GB_s2-ridge`, `GB_m2-tracks`, `GB_m2-pile` and their editor wiring tools (`HearthMemoryWiring.*`, `SearchWiring.*`); `GB_m1-linda` to `GB_m3-john` for caps and pages only; `M2 - The Trail.asset` level graph; `LevelObjectives` stages, `HiddenLevelUnits` reveals, `LevelAbilityLock`, per-instance HP and alert (data). Non-core code, small: a sequence action that stops a Corruption pool (sets the hazard's public `ShouldTick` to false and hides it); an "every enemy except these tiles" mode on `HideUnitsSequence`; an optional result summary line (`MissionEndPanelUI`); objective feedback (objectives panel); the Synergy aim preview (attack preview; its own tech plan). Home: new-game start, visit-1 completion scene, Family tree auto-open (C5c panel API, D-356). Core: none. Nothing is handed to the Family Roles track except one requirement (Q8).
USPs: Synergies (main), Duos, Home; Family Roles (exposure only, deferred).
Docs: see [Docs to update](#docs-to-update-if-approved).

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
| Arrow falloff is 1.0 in code, not 0.6 or 0.9 | `reports/onboarding-c4b-ridge.md` (systems critic) | A plain pierce does as much as a Catch & Return per arrow; this plan's first numbers were too kind to the ★ |
| Post-Hearth new things before M4: Asleep state + sight beat, Lucy's role panel, Mark's role panel, Archers, Papa's Shelter, Shield Flare, Catch & Return, FTP drain + Pass-by, the mission map, Encore's cue, Items, the tally, Workshop, skill tree, Bond, Family tree | C4, C5, Bond Lite reports | About 16 introductions in ~30 minutes, after a Hearth that already taught ~20 |
| The Pile: family starts at the north-west, the targets sit 6+ tiles away (one Archer behind the pile), the rear wave spawns at 0,6 / 0,5 on turn 2, on the family's own start | `GB_m2-pile`, C4c report | Exactly THJ's "walk away, then they spawn behind where you were" |
| Free enemy-turn roles carry much of the damage (Linda 46–72%); John's guard redirects every hit within 2 at ×0.5 | `combat-balance.md`, rethink plan evidence 5 | A reason abilities feel unneeded. It also means the River can't be tuned once for both Family Role outcomes |

---

## Options compared

| | A. Tune numbers only | **B. Teach-and-challenge beats in the same levels, cut the rest (recommended)** | C. One combined search mission | D. Do nothing |
|---|---|---|---|---|
| What changes | Tier up to Early/Standard, more enemies, keep layouts | Each pair mission becomes 2 short beats (an awake Hearth challenge → a Synergy situation that asks for it); The Trail becomes 2 levels; post-Hearth panels, the route choice, the FTP drain and the Items panel are cut; one aim-preview rule shows Synergy outcomes | River and Ridge merge into one mission with both pairs; Home visit 1 goes | — |
| Player experience | Harder but still nothing to plan; one-by-one fights get longer | Every level asks a question with a Hearth tool or a pair Synergy as the answer; a clue on every beat | Saves a visit; loses "two go, two stay"; two untaught Synergies in one mission | THJ's notes stand |
| Rules to track | None | Fewer than today (8 introductions cut or delayed, 2 kept, 1 preview rule) | Fewer Home steps | Same |
| Time | Longer (HP sponges) | ~41 min on paper (today ~46 with the last visit) | ~38 | ~46 |
| Cost | Data | Level + wiring-tool work on 5 levels; 4 small non-core codes; the preview's own tech plan; Home tech plan | New mission, roster work, Home rework | 0 |
| Risk | "Abilities not needed" stays | Balance found in play and partly after the Family Roles session; the route choice's story moment lost | Breaks the approved structure | — |
| USP effect | Neutral | Synergies ++, Duos + (kept as finishers, first sisters' Duo framed later), Home + | Home − | Synergies stay optional |

The three critics all said ship B with changes, and none of the others. Their changes are folded in below.

---

## Recommendation (summary)

Option B. In order of what the player meets:

1. **Home, then the Hearth.** A new game opens at Home on the storytelling idle (stations locked) and the Hearth starts by itself.
2. **The Hearth keeps its lessons and loses its caps.** No turn caps, one result line per memory, Lucy's multi-shot page, and Memory 4 ends on John cutting the line: the pools visibly die, every other Claw fades ("the rest scatter"), and the first Duo kills the last three. Family Roles in the Hearth: left to the Family Roles redesign, with one requirement (Q8).
3. **The River and the Ridge: an awake challenge, then a Synergy situation that asks for it.** Early tier with low per-instance HP. River: an awake rush, then three awake Archers on 1-tile islands that only Shield Flare reaches safely. Ridge: an awake pack built so only Explosive Arrow into Mark's chain clears it in a turn, then Catch & Return in the corridor. The aim preview shows each Synergy's copies when the player aims into one (Q2). Numbers set after the Family Roles play session (Q1).
4. **Home visit 1 gets its content:** the handover at the door, then the Workshop pick.
5. **The Trail: two levels, no route choice.** *The Trail* asks Archers-or-rush against an awake queue; *The Pile* is a one-move search that answers something, then an ambush from both sides, ending on the sisters back to back, the tally alone. The sisters' Duo stays locked through M2 (Q5).
6. **Visit 3:** the Yard, then the Family tree opens by itself.

---

## The Hearth (memories)

THJ: the Hearth feels like a tutorial and that is OK. Changes are small.

| Memory | Change | Work |
|---|---|---|
| All four | **Turn caps removed** (THJ): every "objective or cap" any-group becomes the objective alone; the "Turns left in the memory" line goes. Stages still move on when the objective is met | Data: M1–M3 through `HearthMemoryWiring.Linda/Lucy/John.cs` (editor code, re-run; **check first** that the Lucy wiring tool already carries the ten/two/four gag of D-457 to D-459, so a re-run doesn't undo it); M4 by hand in the prefab (the master, D-405) |
| All four | **One result line per memory** (THJ): the level-won panel shows one summary line instead of each stage's objectives. Text by `miso-narrative` (e.g. M1 "Seven Claws. One arrow.") | **New code, small (all):** an optional summary line on a level; when set, `MissionEndPanelUI` shows it alone. Not core |
| 1 Linda | **No change for Family Roles here** (was: drain FTP so Watch can't pay). The drain shows an empty meter on the game's first screen, which a new player reads as broken (UX critic), and the Family Roles direction "no role works alone" (D-464) silences Linda alone anyway. Q8 | None |
| 2 Lucy | **Multi-shot page** (THJ): one page at level start on Fire Embers' extra embers (how many, how their targets are picked), before the first two Claws. Read `Lucy_Ability_PrimaryAttack` before writing it (to check: whether the sidewinders each pick their own target, as the GDD says). **Checked against the stage-1 gag** (10 Claws → "Two." → 8 fade → "Four.", 4 Claws fight; D-457 to D-459): the page plays before the gag and names no Claw count; the result line must not quote a count either (the fight is 4, the telling said 10) | Data (existing `TutorialSequence`); text by `miso-narrative` |
| 3 John | **No change here** (THJ: only John's role should fire). Left to the Family Roles redesign, which already places its first lesson in this memory (round 3, scenario S6). Q8 | None |
| 4 Mark | **Ending and Duo**, below | Prefab by hand; two small non-core codes |

**Memory 0 for John:** not recommended (Q9). John alone has nobody to guard, and under the Family Roles direction (D-464) no role works alone, so his role can't show at all; it adds 2–3 minutes to a Hearth already on target.

**Tempest Bloom preview:** now part of the one Synergy aim-preview rule (Q2, [Small UI rules](#small-ui-rules)).

### Memory 4: John cuts the line, the first Duo finishes it

Prefab cells as in the [paper levels' Memory 4 section](2026-10-26-onboarding-levels.md#segment-4--marks-telling-and-then-i-arrived) (prefab x = drawing x − 1). No grid in this plan changes for Memory 4: the prefab is the master and edited by hand.

| Item | As built | Proposed |
|---|---|---|
| Stage 1 | Any Bloom target dead, or cap 1 | Any Bloom target dead |
| Stage 2 | "John: Cut the reinforcement path." John on (6,5), or cap 2 | Same objective, no cap |
| On John reaching the mouth (`Hold`) | John's line, reveal `top`, unlock the Duo | **The line is cut, on screen:** (1) both `CP_Spawner_Hearth` pools stop for good and visibly go (a fade or puff; the art is THJ's); (2) John's line at (6,5) (narrative, e.g. "Nothing more comes through here."); (3) **every enemy except the three `top` Claws fades out** ("the rest scatter", Mark's telling); then the existing `top` reveal and Duo unlock |
| Why code, not data | — | **Pools:** switching their GameObject or component off doesn't stop them: `FactionControllerBase.PhaseTick` ticks every registered hazard and `HazardEntity.PhaseTick` checks only its own `shouldTick` (systems critic, read in code). A new sequence action sets the public `ShouldTick` to false, then hides the pool: small, non-core. **Fade:** `HideUnitsSequence` (`25eca99d4`) takes only units of a named hidden group. The `left` group qualifies; the (0,4) and (6,4) Claws are placed visible (data: move them into a group revealed at level start), but **pool-spawned Claws are in no group**. An "every enemy except these tiles" mode on the same step covers them: small, non-core, beside the existing step |
| Stage 3 | Six Claws dead or cap 4, **and** John on (6,5) or cap 4 | **Only the three `top` Claws** (8,7), (9,7), (9,6), 7 HP each. John no longer has to stay |
| Enemies | (9,8) and (10,7) by the mother; the (6,4) Claw scripted to (7,7) and counted in stage 3 (D-417) | Remove (9,8) and (10,7). The (6,4) Claw's scripted move stays as built; it fades with the rest at the hold and leaves stage 3 |
| The Duo | Mark–Lucy unlocks in `Hold`; six Claws in reach, it takes up to 3 | After the fade the three `top` Claws are the only enemies on the board, so Chained Assault (nearest first within 4) can only pick them. (3 + 8) × mash 0.7 = 7.7 at worst per target, against 7 HP: **it always kills all three and ends the memory** (THJ: "the first Duo should finish everyone"). This also closes the open check on which three it picks and from where its range counts |
| John off the board (THJ's "maybe") | — | Optional, Q6 (c). The fade-out step takes any unit of a group, so if John can be placed in a hidden group revealed at level start (to check for a hero) it is data; else the same small mode above with "this unit" |
| What the player sees | Enemies on the board, a line saying none are left | The board shows what the telling says: John holds, the pools go, the rest scatter, the Duo ends it |

Stage 3 is then one turn (Mark and Lucy reach the Duo; the existing check on their path with John in the passage stays open). Linda and John have nothing left to fight in it: fine for a showcase's last beat.

---

## The search: the River and the Ridge

**Shared rules for both pair missions.**

- **Tier Early** (×1 HP, ×0.75 damage, CR-32) with **per-instance HP factors** (data, the per-instance `Stat_HP` override the Ridge already uses). Start values per level below. They are **provisional**: tuned in play, after the Family Roles house-rule session, which this plan suggests running on these two levels (Q1).
- **Fight beats are awake.** A sleeping enemy can always be picked off safely (no caps), so every challenge starts alert. Only the Ridge's corridor sleeps, and there waking it is part of the move, not a decision.
- **No panels.** The Asleep panel and sight beat go (THJ; the marker stays), the role panels go (THJ: the prompt teaches itself). The first-sleeper handle comes off both levels.
- **Teaching = the board, one line, the objective, the aim preview (Q2).** The Synergy's line plays as its stage starts (an `OnCompleteSequence`, data; bark conditions can't test positions, C4 check). The objective names the goal, not the steps: "Silence the archers.", not "John: hold the ford." (creative and UX critics: a goal tile for John reads as a tutorial step and disappears the moment he arrives, before Lucy acts). No goal tile in either lesson.
- **A clue on every beat, placed in the grids** (creative critic: clues left to "narrative later" never land, and the Map Table recites clues the player never saw). Each beat's clue is a `note … clue` on the grid with the line it carries.
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
| Source | `GB_s1-river`, cells and units as above. Read back with `level_to_grid.py` first: today's prefab matches the C4a block, so a rebuild plus a re-run of an updated **Wire Search: River** is safe if nothing was hand-edited since |
| Challenges (beat 1, the clearing) | Hearth: **John's guard and Shield Up → Wrath → the punish** (Memory 3) and **Lucy's Cyclone** (Memory 2), under a real rush |
| Teaches and asks (beat 2, the ford) | **Shield Flare**: three awake Archers on 1-tile islands; the only tiles out of all their reach from which anything hits all three are John on 11,3 and Lucy embering him from 12,2 |
| Squad | Lucy 0,3, John 1,3 (Papa's Shelter shown at start, as built) |
| Enemies | Clearing: 3 Dark Claws (5,3 6,4 6,2), factor 0.6 (≈ 9.6), **start alert** (per-instance `startsAlert`, or `Unit_DarkClaw_StartsAlert`). Ford: 3 Archer Goblins on 1-tile islands 9,5 / 13,5 / 9,1 (cannot move), **start alert**, factor 0.5 (≈ 12; provisional, below). Far bank: 2 Dark Claws 14,3 / 15,4, Unaware, factor 0.6 |
| Beat 1 | Claws move 4: 5,3 reaches 2,3 on enemy turn 1. ★ John Shield Up beside Lucy (his guard takes their hits and stacks Wrath), then a Wrath Shield Dash with Lucy's embers. ★ Cyclone in the clearing to split the rush. ● Sword and embers one at a time: Lucy (15 HP) takes 4–5 a hit if she strays from John. ~2 rounds. **Its difficulty is set by the Family Role outcome** (F6): with roles as built John's guard soaks nearly everything; under kept AP it covers one hit per AP kept |
| Stage 1 → 2 | Clearing dead → sequence: the clue (6,3, R7-2/3), camera across the ford to the islands, then John "Lucy. If it gets hot, aim at me." / Lucy "*At* you?" / John "Trust me." (R7-7 to R7-9). New objective **"Silence the archers."** (the three Archers dead) |
| Beat 2 (verified distances) | Awake Archers (reach 3) shoot anyone within 3. 11,3 is 4 from all three islands; 12,2 is 4 from 13,5 and 9,1 and 6 from 9,5: **both out of every Archer's reach**. From 11,3 each island is 2 diagonal: copies via 10,4, 12,4 and 10,2 (all floor). ★ John: move to 11,3 + Shield Up; Lucy: to 12,2 (2 from John) + ember **him** → the copies hit all three Archers, nobody in reach. Repeat next turn. ● Lucy embers an island directly: every tile within 3 of an island is in that Archer's reach, so it shoots back (6 × 0.75 = 4.5) unless her volley kills it first, which needs more than its 12 HP (sheltered volley 4 + 3 + 3 = 10) |
| Why 12 HP (provisional) | Plain: a sheltered volley (10) never kills an Archer in one turn, so each one shoots back at least once: about 3 × 4.5 on Lucy (15 HP) over six turns. ★: depends on an unchecked fact. **If every ember of a volley flares** off John, an unsheltered volley (4 + 3) puts 7 on each Archer: two Flares kill all three. **If only the main ember flares**, it puts 4 on each: three Flares, and the ★ wins on safety, not speed; then drop the factor to 0.33 (≈ 8): two Flares, and a sheltered plain volley (10) kills one Archer per turn but only from inside its reach. **To check before building:** which embers flare, and whether sidewinders spread or stack (decides the plain volley) |
| Stage 3 | Defeat all (the far-bank pair, woken when John stops on 11,3, 3 from 14,3; Wrath from the Archers' hits feeds a Shield Dash). End: the far-bank close-up (R7-4/5; the Claws someone else cut down, as built) |
| FTP | Starts full (8) |
| Fallback | A player who never embers John wins slower and hurt. With the aim preview (Q2), hovering a shielded John shows the four copies and their damage, which is the lesson. Without it: a `GuidedAbilityHint` pulse on Fire Embers once John has Shield Up on 11,3 (**to check** whether a hint condition can test that) |
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
| Squad | Linda 1,1, Mark 2,1. **The family acts first** (reverses D-353's enemy-first, so the opening is the player's plan, not two prompts; Q3) |
| Enemies | Pack: 4 Dark Claws 1,4 / 0,4 / 2,4 / 1,5, **start alert**, factor **0.8** (≈ 12.8). Corridor: 6,1 / 7,1 asleep, factor **0.85** (≈ 13.6). End: 10,1 asleep (wakes when Mark lands on 8,1, 2 away), factor 0.6 |
| Beat 1 (re-derived, falloff 1.0) | ★ Explosive Arrow from 1,1 on 1,4 (3, within 5): all four take 8 → 4.8 left. Mark to 2,2, Fist Blitz on 2,4 (8) kills, he steps in, Continuous Attack swings at the lowest within 2 (≈ 8, kills; FTP 1), a second swing (FTP 2; total 3 of 5) kills; Linda's second AP: bow (6) finishes the last. **All four in one turn.** ● Two plain shots up column 1 pierce 1,4 and 1,5 for 12 each (< 12.8: none die), Fist Blitz 8 kills nothing so no chain: four Claws hit back (~4.5 each). Why 0.8: at 0.6 two plain shots killed two and the pack died before any enemy turn (systems critic) |
| Stage 1 → 2 | Pack dead → sequence: the clue (3,2, G9-2), camera down the corridor, Mark "Linda. Shoot at me." / Linda "Gladly." / Mark "From the far side." (G9-6 to G9-8; narrative may soften the last line so it names the pairing, not the steps). Objective **"Clear the corridor."** |
| Beat 2 (re-derived) | ★ Mark to 5,1, Vault to 8,1 (3, over the queue, 2 on 7,1; Vault over units: confirm in play); Linda to 4,1, bow along row 1: 6 on 6,1 and 7,1, then Mark (4 away) → the catch → the return copy hits both again for 6: 12 each, 14 on 7,1 → 7,1 dies (13.6), 6,1 at 1.6. Mark's second AP: Fist Blitz on 6,1 kills → Continuous Attack on 10,1 (2 away) kills. **Three Claws, one Linda AP, her arrow back.** ● Linda's two plain shots pierce both for 12, Mark's Blitz and a swing kill both, two arrows land under the last Claw, and 10,1 is untouched. **The catch's edge here is an AP and two arrows, not survival:** stated plainly (see Critics, where I disagree) |
| Catch prompt | Its first use in the game: if the catch QTE's short wait (D-273) is a per-ability value, use the standard wait on the Ridge (data, **to check**). With the aim preview (Q2), Linda's aim shows the return lane as "if caught" |
| Alert | Pack alert; corridor asleep (Linda on 4,1 wakes it the same turn she fires, so the wake decides nothing) |
| FTP | Starts full (5). Continuous Attack costs 1, then 2, then 3 FTP in a chain, so 5 buys two swings. With roles as built, Watch and the counter also spend it (F5): the pack's chain may get one swing, and Linda's second AP finishes |
| Clue | End close-up on 12,1 (G9-3/4, as built) |
| Fallback | The plain play still wins, hurt (beat 1) or slower (beat 2). Hint fallback for the catch: a `GuidedAbilityHint` on Linda's bow once Mark stands past the queue (**to check**, as the River's) |
| Time | ~4 min (3–4 rounds) |

---

## M2 · The Trail: two levels

**Structure.** *The Trail* → *The Pile*. No route choice, so no mission map; the empty Trailhead and "Follow the blood" leave the level graph (assets kept). Data: `M2 - The Trail.asset` level graph. The FTP drain goes with the Trailhead (FTP starts full, CR-10), the Pass-by panel goes (Pass-by still works; taught after M4), the Items panel goes (items stay in stock; the pouch bob, CR-52, cues them). The tally's rematch line (P8 proposal) moves to *The Trail*'s start. The free pick (John or Mark) decides which pair Synergy the player brings. **The Linda–Lucy Duo is locked in both levels** (`LevelAbilityLock`, data; Q5).

If THJ keeps the route choice (Q4, option b): the Trailhead keeps its role as the level before the map, gets a one-turn fight (two Claws in the 1-wide trail, awake: Linda's pierce from Memory 1), and "Follow the blood" gets the same rework as below. About +3 minutes.

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
arrow 4,1 4,6 linda dx=-8 bow pierce: both Archers
arrow 3,1 8,1 linda dy=8 Explosive
note 2,3 clue: tracks
level name The Trail
level tier early
level alert all
level deploy 2,1
```

| Item | Plan |
|---|---|
| Source | `GB_m2-tracks`; rebuild + an updated **Wire Search: Trail**. Keeps its stages (both Archers dead → the Encore cue, then defeat all) |
| Question | An awake queue coming down the narrow trail, and two Archers on a ledge covering the side pocket: kill the Archers first (one well-placed pierce) or meet the rush? |
| Challenges | Hearth and pair missions: Linda's range and pierce, Explosive Arrow, **Encore** (her arrow lands on the ledge; Memory 1 unlocked it), and the picked pair Synergy |
| Squad | Linda 0,1, Lucy 1,1, the pick on the slot 2,1 |
| Enemies | 2 Archer Goblins on the ledge 4,5 / 4,6 (static), factor **0.25** (≈ 6). Queue: Dark Claws 7,1 / 8,1 / 10,1, factor 0.6. **All start alert** (`level alert all`): no wake decision, so no wake marker needed (UX critic). Early |
| Answers (re-derived, falloff 1.0) | ★ Linda to 4,1, one bow shot up column 4: 6 on both Archers, both die, one arrow on the ledge (Encore later). But 4,1 is where the queue arrives (7,1 moves 4): she spends the turn in the rush's path. ★ Explosive Arrow from 3,1 on 8,1 (5): 8 on 7,1 and 8,1 (→ 1.6), then the pocket is the Archers' (4,2, 3,3, 4,3, 5,3 are within 3 of 4,5). ★ (Mark) Vault over the queue in the trail, Linda's bow along row 1 for the catch. ★ (John) Shield Up in the trail as the queue arrives (guard + Wrath). ● Lucy embers the queue; anyone stepping into the pocket takes Archer fire. **No Duo here** (locked, Q5; the first plan wrongly listed Marks-Sisters as a ★, both critics) |
| Encore | Unchanged cue on the "both Archers dead" stage (D-334) |
| FTP | Full at start (no drain) |
| Time | ~3 min (3 rounds) |

Why factor 0.25: Linda outranges every static Archer (4 against 3), so a static Archer is always a free target for her (systems critic). At 12 HP that meant two shots and two arrows lost on the ledge, dead time; at 6 HP it is one decisive shot whose cost is where she has to stand.

### The Pile (Linda, Lucy + John or Mark), rebuilt on `GB_m2-pile`'s footprint

Prefab coordinates, same 10 × 7 footprint, new cells. The search comes first, is one move long and answers something; the fight comes after it, from both sides.

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
| The search (THJ: low tempo on purpose) | Start: the pile close-up, Lucy "Linda… what if she's in there?" / Linda "Then we find her. Together." (T11-3, T11-4). Objective **"Search the pile."**: any Bergson on a tile beside it (4,5 or 5,5, one move from the start row). **The search answers something before the ambush** (creative critic): a partial-relief line, e.g. Lucy "No white fur… she's not here." (narrative), then the reveal. They fight with hope, not as a trap trigger. The rivalry barks stop here (narrative) |
| After the search | Both hidden groups revealed (alert): three Claws in the west lane, two Claws and an Archer on the east perch. They act on the next enemy turn. Back to back |
| Enemies | West 0,4 / 1,4 / 2,4, east 9,4 / 9,3 Dark Claws, factor 0.6; Archer on the 1-tile perch 9,6, factor **0.25** (≈ 6: one bow shot). Early |
| Answers (re-derived) | West lane: ★ Linda's bow from 3,4 along row 4 pierces all three at 6 each (falloff 1.0), Lucy's embers finish; or Explosive on 1,4. East: ★ Linda's bow on the perch from 5,6 along row 6 (4, outside its reach; across 6,6–8,6, which the grid draws as **rock**: **to check** arrows fly over rock), one shot kills it, the arrow lies on the perch. ★ (Mark) Fist Blitz + Continuous Attack on the two east Claws once they close. ★ (John) Shield Flare from 7,4 reaches the perch via 8,5 (2; 7,4 is 4 from 9,6, outside its reach): 4 (or 7 if every ember flares) against 6. ★ Lucy's Cyclone on 6,4 or 7,5 splits the east pair (it blocks the family too until the Cyclone redesign, P9; no ★ needs the family to pass it). ● Embers on the perch from 7,5, inside its reach. Linda can't do both sides in one turn with three arrows: that is the pressure |
| The ending | **No Duo** (locked in M2, Q5). The level ends on the last kill, the sisters back to back, the tally alone on screen, then "Still counting?" / "…No." over the quiet (the first-hour design's Turn: the joke dies under dread, not in a win). End as built after that (the tally fade, the free pick's line, Lucy's motive line T11-8) |
| What THJ's notes asked | No walking (the family starts one move from the pile and the enemies come to it); nothing out of reach for long (the perch Archer dies to one shot from 5,6); no start spawns walking back (the fight starts after the search, from both sides, on purpose); something before the beat (*The Trail*'s fight) and after it (the ambush) |
| FTP | Carried from *The Trail* (full at its start). With the Duo locked, FTP in M2 is spent only by roles (as built) and Continuous Attack |
| Time | ~4.5 min (search + 3 rounds) |

---

## Home

| Moment | Today | Proposed | Work |
|---|---|---|---|
| New game | Menu, then the Hearth's levels | **Home on the storytelling idle** (`MargaretStoryNight`, Margaret hosts, D-178), H0-1 to H0-4, then the Hearth starts by itself (THJ). **Stations locked** until after the Hearth, so nobody clicks the Workshop first (UX critic) | Home flow: small code. Tech plan (coordinator) |
| After the Hearth | Hearth close, "Two go out, two stay", World map page | Unchanged | — |
| Visit 1 (after the first pair mission) | The Workshop page only; THJ: "nothing in between" | **The handover at the door**: the returning pair meets the leaving pair. One real clue line from the returning pair (the clue their mission's end close-up showed), the go-between joke (V1-2a to V1-4a, or V1-2b to V1-4b by order) and Ben's "You two are next? Hand them over." (V1-1), which leads into the Workshop pick (existing page). About 1 minute | Data: a `DialogNodeSequence` as each pair mission's completion scene. **Small code** if it must play only after the *first* pair mission (C5c's `GetLastCompletedMission` is a model). Q7 |
| Visit 2 | Skill tree page + guided spend; Map Table clue scene on the Trail pin | Unchanged. The Map Table's clue lines (V2-3, V2-6) now repeat clues placed in the grids | — |
| Visit 3 | Yard → Bond Lv 2 → Margaret's point → pan back | **The Family tree opens by itself on the Family tab after the pan back** (THJ; reverses C5's "no tab opens by itself"), with the sisters' node already pulsing (the existing guided-spend marker) so "spend, then close" is obvious | Small code: the upgrades panel API from C5c (D-356) |

---

## What to cut or delay

THJ: "too many mechanics with too little challenge." This plan removes eight introductions from the first hour and makes two existing optional Synergies into lessons.

| Item | Was | Now | Why |
|---|---|---|---|
| Asleep panel + sight beat | Required, first pair mission | **Cut** (the marker stays) | THJ. Safe only because no level now hinges on a wake (fight beats awake) |
| Lucy's / Mark's Family Role panels | River / Ridge start | **Cut** | THJ: the prompt teaches itself (F4) |
| Watch panel page in Memory 1 | Memory 1 | **Cut** ("Each shot spends an arrow." moves into the "Moving and AP" page) | THJ; Watch itself left to the Family Roles redesign (Q8) |
| Turn caps and "Turns left in the memory" | All memories | **Cut** | THJ |
| Route choice + mission map | M2 | **Delayed** to later content | One screen and one level less (Q4) |
| FTP drain + Pass-by panel | M2 trailhead and routes | **Delayed** to after M4 (Pass-by still works) | No scarcity lesson needed with the Duo locked in M2 |
| Items panel | The Pile | **Cut** (items stay in stock) | The pouch bob cues them |
| Empty Trailhead | M2 level 1 | **Cut** | THJ: too vague |
| Sisters' Duo in M2 | Open; The Pile's planned finisher | **Delayed** to M4, after the Yard (Q5) | Creative critic: a shared kill before "Still counting?" reads as a win and empties the Yard scene |
| Kept | Papa's Shelter shown at River start; Encore's cue in *The Trail*; the tally; Workshop, skill tree, Bond Yard, Family tree | | Each is shown once, at the moment it pays off |

---

## Family Role dependencies

The Family Roles track runs a three-step test with a stop rule (D-460): if its play session says no, roles lock **as built** (A); if yes, a dev switch for **kept AP** (C; roles answer outside the family's turn only with AP their Bergson kept; John one guard per kept AP, D-462). Its round 3 draft adds the direction "no role works alone" (D-464). **Honest summary: the levels' layouts hold under each outcome; their difficulty numbers don't.** That is why the River's and the Ridge's numbers wait for the session (Q1).

| # | Place | As built (A) | Kept AP (C) / "no role alone" |
|---|---|---|---|
| F1 | Memory 1 | Watch fires as THJ played it. The FTP drain that would stop it shows an empty meter on the first screen: not proposed | Linda alone: silent (D-464). Nothing to build |
| F2 | Memory 3, John's role alone | Needs a per-level, per-hero role switch (core, Tier 3): not proposed; THJ played it with all roles on | The redesign places its first lesson here (round 3, S6). Nothing to build |
| F3 | Memory 4 | As built | Mostly automatic (turn-1 AP limits) |
| F4 | River / Ridge, no role panels | Lucy's and Mark's prompts appear untaught, under real damage in the River's awake rush; Watch and Mark's counter both first seen in the Ridge pack (the family-first fix helps). THJ: fine | Each needs kept AP, taught in Memory 3; the rushes become keep-or-spend questions |
| F5 | Ridge FTP (max 5) | Watch, the counter and Continuous Attack (1, 2, 3) share it: two role answers leave one swing | Roles spend no FTP: two swings |
| F6 | Difficulty of every John level | His guard redirects every hit within 2 at ×0.5, unlimited: the River's clearing is soft; levers: Claw factor up, or Standard tier on the River | One guard per kept AP: the River is much harder; the ford's ★ turn (move + Shield Up) leaves John nothing to keep, so Lucy must stand out of reach (12,2, built in) |
| F7 | The Trail and The Pile | Roles spend FTP; with the Duo locked, nothing else competes | FTP is spent by Continuous Attack only |

**What this plan asks of the Family Roles track:** one requirement for the Hearth, "no role fires before Memory 3, and in Memory 3 only John's" (Q8), and that its house-rule session be played on the reworked River and Ridge (Q1). No switch.

---

## Small UI rules

| Item | Rule | Work | Scope |
|---|---|---|---|
| **Synergy aim preview** (Q2) | **When an aim would set off a Synergy, the preview shows where its copies go and what they hit**, with the usual damage numbers, and nothing on the ally it bounces off. Covers Tempest Bloom (arrow into a Cyclone: the copies' lanes), Shield Flare (Lucy hovering a shielded John: the four diagonal copies), Catch & Return (Linda's lane reaching Mark: the return lane, drawn as "if caught"). Same reach rule as every preview (CR-37). One element: the existing aim preview, extended. Replaces the first plan's Bloom-only preview. Why it's needed: a new player has never aimed a damaging attack at family; with no outcome shown, it reads as friendly fire and they decline (UX critic) | New code in the attack preview (`UnitThreatAnalysis` reach helpers, `PlayerController` preview path; read, not traced); its own tech plan. Holds under the Cyclone redesign | all |
| Goal tile | The win-objective highlight is no longer green (green means HP bars and heals, CR-49, CR-53). Proposal: a warm gold outline; the art call is THJ's. (The lessons no longer use it; The Pile's search and Memory 4's mouth still do) | Data: the `gridCellHighlightLevelGoal` sprite or its tint on the `GridCell` prefab | all |
| Objective feedback | When an objective is met, its line ticks and pulses once with a short sound, and the panel unfolds if it was folded. Animates the element that exists | New code, small (objectives panel UI, not core) | all |
| One result line per level | Optional summary line on a level; when set, the level-won panel shows it alone | New code, small (`MissionEndPanelUI`), off by default | all |
| Level-design rule | A ranged enemy meant to stay put stands on a 1-tile island or perch, so a Synergy aimed at it can't be dodged by its own move. **And:** Linda (4) outranges any static Archer (3), so a static Archer is her free target: keep its HP to one shot, or put it where her 4-away tiles cost her something | Catalogue knob in `design/level-chunks.md` | all |

---

## Lens notes

### Creative

**Target experience.** After the Hearth the family stops telling stories and starts being tested. Each search trip should feel like the habits from the fireside, now needed for real, with one new trick the pair finds together ("Aim at me." / "Shoot at me."), found by aiming, not by following a tile. The Trail should feel like the family's exam, and The Pile like the moment the joke dies.

**The moment designed for (changed after the creative critic):** The Pile's last kill. The search found no white fur, so they fight with hope; the sisters stand back to back, the tally alone on screen, nobody scoring; the last Claw drops, and "Still counting?" / "…No." lands on silence, not on a combo. Their first Duo together waits for M4, after the Yard taught them to set each other up, where "We both did" can be the payoff it was written to be.

Secondary: the River's three islands lit at once by one Flare off Papa's shield, from the one spot the Archers can't reach; the Ridge's pack gone in one turn; Memory 4's pools dying as John plants his feet, the rest scattering, the Duo ending the telling.

**Story on every beat.** Each beat's clue is on its grid (R7-2/3 at the clearing, R7-4/5 at the far bank, G9-2 at the corridor, G9-3/4 at the end, the tracks in *The Trail*'s pocket), so visit 2's Map Table recites what the player saw.

### Systems

- **Levers** (start values, provisional for River and Ridge): tier Early; per-instance HP: River clearing Claws 0.6, ford Archers 0.5 (0.33 if only the main ember flares); Ridge pack 0.8, corridor 0.85, 10,1 0.6; Trail and Pile Archers 0.25, Claws 0.6. Every fight beat alert; Ridge family first; FTP full in M2; sisters' Duo locked in M2.
- **Interactions:** Shield Flare needs John's move + Shield Up and Lucy's ember: a full turn of both. Catch & Return is arrow-neutral (LI-9) and gives no AP (D-332). Continuous Attack costs 1, 2, 3 FTP in a chain (MA-2). Hidden groups revealed under "all start alert" come in alert (`HiddenLevelUnits`). Arrow falloff 1.0 (code).
- **Failure cases:** the Flare never found (River still won, hurt; preview, then hint); the ford's ★ only safer, not faster (if only the main ember flares: factor 0.33); the Ridge chain cut by FTP under A (F5: Linda's second AP finishes); Memory 4's Duo taking a wrong target (closed by the fade); the Pile's perch shot blocked by rock (to check; else move the perch Archer's firing lane).
- **Dominant strategy check:** John + Lucy at the ford dominate there by design. Linda's range-4 bow against static Archers is dominant everywhere: kept, and made one decisive shot. Under A, John's guard soaks the River (F6): the first lever is the Claws' factor, then Standard tier.

### UX

| Moment | Shown | The player clicks | Likeliest misread |
|---|---|---|---|
| River, ford reached | Camera over the islands, John's line, objective "Silence the archers." Shift shows the Archers' reach (awake: attack reach, so 11,3 and 12,2 read as safe) | John to 11,3, Shield Up; Lucy hovers John → the preview shows four copies, three hits, nothing on John | Embers an Archer instead (the habit). The preview only appears if she hovers John; John's line and the targeting offering him (only while Shield Up is on) point there. Order matters: Shield Up first |
| Ridge, corridor | Camera down the corridor, Mark's line | Mark past the queue; Linda aims along row 1 → preview shows the return lane "if caught" | Linda shoots before Mark is past: the arrow lands under the last Claw (LI-6). Misses the catch press: the prompt uses the standard wait if it can (to check) |
| The Trail, column 4 | The Archers' reach (Shift) and the awake queue's move | Linda to 4,1 or 3,1 | None about waking: everything is awake |
| The Pile, search | "Search the pile." and the gold goal tile beside it | One Bergson one step | Thinks the level is a cutscene and waits: the objective and the tile carry it |
| Memory 4, the hold | The pools fade, John's line, the rest fade | The Duo | None about leftovers: only the Duo's three are left |
| Memory result | One summary line | Continue | — |

**On-screen elements added:** one (the Synergy aim preview, an extension of the existing preview). Removed: six panels, the turn-cap line, one map screen, the lessons' goal tile.

**Where the lenses disagree:** the creative critic wants the lessons led by the layout alone; the UX critic wants captions and a persistent objective. I lean between them: the objective names the goal ("Silence the archers."), the aim preview shows the outcome only when the player looks, no caption (THJ's "no tutorial text"). Captions are Q2's option (b).

---

## USP check

- **Family Roles:** neutral on purpose. This plan changes no role exposure itself; it hands the Family Roles track one Hearth requirement and its two pair missions as the test ground.
- **Synergies:** strengthened. Shield Flare and Catch & Return go from optional discoveries to situations that ask for them, re-tested in The Trail by the free pick; one aim-preview rule makes every Synergy's outcome visible before the click.
- **Duos:** kept as finishers (THJ). Memory 4's Duo always ends the telling; the sisters' first real Duo moves to M4, after the Yard, where it's the payoff of the rivalry arc instead of a win stamped on its death.
- **Managing the Home as a Family:** strengthened. The game opens at Home; visit 1 gets the handover scene; visit 3 opens the Family tree on the best moment of the hour, with nothing taken from the Yard scene.

## Critics

**Real, independent critics, run 2026-11-10 by the coordinator:** three read-only Explore agents, each told to read and follow `.claude/agents/miso-design-critic.md`, one lens each (the `miso-design-critic` agent type wasn't available in the session). Each saw this plan and the pacing check, not the others' output. Full text: [`reports/after-hearth-critics/`](../../reports/after-hearth-critics/) (`creative.md`, `systems.md`, `ux.md`). All three: ship B with changes; A, C, D no.

### Systems critic

| Objection | My response | What changed |
|---|---|---|
| **Strongest:** at the plan's own numbers the plain play beats or matches the ★ in most beats; the River ford goes from trivial (roles as built) to lethal (kept AP); "holds under either outcome" is false for its central beat | Right. The root is a second one I'd missed: no caps + sleeping targets = the safe play is always open | Every fight beat starts awake; ford Archers awake on islands with John on 11,3 and Lucy on 12,2 the only safe Flare tiles; River and Ridge numbers made provisional and tuned after the Family Roles session (Q1); the "holds under either" claim withdrawn; acceptance criterion rewritten (worse, not forbidden) |
| Arrow falloff is 1.0, not 0.6/0.9; Flare copies ≈ 4 each; Continuous Attack costs 1/2/3 FTP | Right (C4b report, code) | Ridge re-derived: pack 0.8, corridor 0.85; F5 corrected to two swings; Flare damage tied to the open check (which embers flare), with two value sets |
| Pools need `ShouldTick = false`; activation actions don't stop them | Right (read in code) | A small new non-core action; Memory 4 table rewritten |
| Chained Assault may take a nearer leftover and leave a `top` Claw alive | Right | Every other enemy fades at the hold: the three are the only targets |
| Marks-Sisters listed as a ★ in The Trail contradicts "first Duo at The Pile"; at The Pile the Duo can be fired as the opener | Right | Sisters' Duo locked in M2 (Q5) |
| Static Archers are free targets for Linda's range 4; Encore dead time | Right | Trail and Pile Archers at 6 HP (one shot); the level-design knob gains the caveat |
| The ★ must win in every beat | **Partly disagree.** With no caps nothing can forbid the plain play. For the Ridge corridor I accept an efficiency answer (an AP and two arrows), made visible by the preview, because forcing it would need an arbitrary rule; the pack beat before it carries the challenge | Stated in the Ridge table |

### Creative critic

| Objection | My response | What changed |
|---|---|---|
| **Strongest:** The Pile's Duo finisher turns the joke's death into a triumph, empties the Yard scene's discovery and makes M4's "We both did" a repeat; the plan also lists the Duo at The Trail | Right. I had merged two beats of the rivalry arc | The Pile ends on the sisters apart, back to back, tally alone; Duo locked in M2; first sisters' Duo handed to M4 (Q5) |
| The searches lose the search: clue lines unplaced, the River's stage change plays Synergy lines, not clues | Right | Clues placed on every grid with their line IDs; visit 1 carries a real clue |
| A goal tile for John + an early "aim at me" is a tutorial step in disguise | Right about the tile | Objective "Silence the archers.", no tile. Kept the line at stage start (a bark can't trigger on John's Shield Up near the ford, C4 check) |
| The Pile's search is a genre ambush trigger | Right | The search answers first ("No white fur…"), then the reveal |
| Memory 4 ends with enemies on the board; "cut the line" isn't felt | Right | Pools visibly die, John's line, the rest fade |
| No quiet stretch; the route choice was the one place the player voiced worry | Fair, not enough to keep it | Kept the route cut as the recommendation (Q4 prices keeping it); the Pile's search is the quiet beat, now with an answer |

### UX critic

| Objection | My response | What changed |
|---|---|---|
| **Strongest:** lines and a goal tile don't show the rule; the tile vanishes when John arrives, before Lucy acts; no Flare or return preview, so aiming at family reads as friendly fire; the catch QTE is untaught | Right, and the plan's own Bloom reasoning applies | One Synergy aim-preview rule replaces the Bloom-only preview (Q2); objective persists until the Archers die; catch prompt at the standard wait if per-ability (to check); a hint fallback for the catch |
| Waking is the Trail's decision but invisible before the click (no wake marker) | Right | Removed the wake as a decision (Trail all alert, fight beats awake) rather than build the marker |
| Memory 4: board and line disagree; stage 3's targets unreadable | Right | Fade of every other enemy |
| Memory 1's drained FTP bar reads as broken | Right | Drain dropped; Memory 1 left to the Family Roles direction (Q8) |
| The Pile's Duo needs a hint from the start | Moot | Duo locked in M2 |
| Home start must lock stations; Family tree "spend, then close" must be obvious | Right | Both in the Home table |
| Should a preview, caption or objective line count as allowed teaching? | Right that it's THJ's call | Q2 |

---

## Recommendation

Option B as revised above. It fixes both roots (introductions without tests; sleeping targets that make every test optional), cuts eight introductions, adds one preview rule, and makes the first hour shorter.

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

As in the level tables and the Systems levers; River and Ridge provisional (Q1). No GDD rule changes; values are per-level data.

### To check before building (each decides a number)

1. Which embers of a volley flare off a shielded John, and whether sidewinders spread or stack (River ford factor 0.5 or 0.33).
2. Whether Shield Flare copies cross a gap (The Trail, John's ●) and arrows cross rock (The Pile, the perch shot).
3. Whether the catch prompt's wait is per ability (Ridge).
4. Whether a hero can sit in a hidden group (Memory 4, John off the board, Q6 c).
5. Whether the Lucy wiring tool carries the ten/two/four gag before it is re-run.

### Playtest signal (THJ's timed run, then the cold run)

- **Worked:** in each pair mission the combat log shows the ★ (Wrath Shield Dash or Cyclone; a Flare hitting 2+ Archers; Explosive Arrow then Continuous Attack; a catch), and the plain play, where tried, cost a round or a third of a hero's HP more; rounds per level 3–5; THJ says abilities felt needed; cold players hover John at the ford and fire; nobody in Memory 4 attacks a Claw that isn't there; The Pile's ending is described as sad, not as a win; the Map Table's clues are ones the player remembers.
- **Failed:** the plain play wins at full HP (raise the Claw factors, then Standard tier); Flare or catch unused by a cold player despite the preview (hint fallbacks); total above ~45 at THJ's pace (cut *The Trail*'s queue to two Claws first).

### Approach: build order (each its own plan or chunk)

1. **Memory data** (caps off, the Watch page out, Lucy's multi-shot page): wiring tools, data. **Memory 4 by hand** in the prefab plus its two small codes (pool stop, fade-all mode).
2. **The Trail, The Pile** (no Family Role dependency): rebuilds from these blocks + updated wiring tools + `M2 - The Trail.asset` graph + the Duo locks.
3. **River and Ridge layouts** from these blocks; numbers set at the Family Roles house-rule session played on them (Q1).
4. **All-scope UI**: goal tile colour (data), objective feedback, result summary line (small code), one tech plan; the **Synergy aim preview** its own tech plan.
5. **Home**: new-game start with stations locked, visit-1 handover gate, Family tree auto-open: one tech plan (coordinator).
6. Timed run by THJ, then the cold playtest.

---

## Questions for THJ

Ordered by how much they block.

**Q1. Should the River and the Ridge be rebuilt now and tuned later, once the Family Roles test has decided how roles work?**
- Context: how hard these two levels are depends mostly on the roles. With roles as built, John's guard soaks most of the River's damage; under the "kept AP" test it covers one hit per AP he saved. One set of enemy numbers can't fit both; the layouts fit both.
- Options:
  - (a) Build the layouts now, set enemy health after the Family Roles play session, and play that session on these two levels. No extra cost; the session doubles as their tuning pass.
  - (b) Build and tune now for roles as built; retune if the test changes them. About one extra tuning chunk if roles change.
  - (c) Wait for the Family Roles decision before touching them. The pair missions stall; the Hearth, The Trail and Home go ahead.
- Recommendation: (a).
- Blocked meanwhile: the River and Ridge rebuild and their numbers.

**Q2. After the Hearth, may an aim preview teach a new Synergy, on top of a spoken line and the board?**
- Context: you want no tutorial panels after the Hearth. The critics showed a line plus a goal tile won't teach Shield Flare or Catch & Return: a new player won't fire at their own father without seeing what happens, and the goal tile disappears the moment John reaches it.
- Options:
  - (a) One preview rule: "when your aim would set off a Synergy, the preview shows where the copies go and what they hit" (Tempest Bloom, Shield Flare, Catch & Return). Replaces the Bloom-only preview you asked for; no text; one tech plan, about 2–3 times the Bloom-only cost.
  - (b) As (a), plus a one-line caption the first time each Synergy is possible. Small extra cost; puts text on screen.
  - (c) Lines and the board only, Bloom preview alone. No extra cost; the critics expect both Synergies to go unused, as today.
- Recommendation: (a).
- Blocked meanwhile: the preview's tech plan, and whether the River and Ridge need their hint fallbacks.

**Q3. Should the post-Hearth fights use a harder tier, awake enemies, and let the family act first on the Ridge?**
- Context: today these levels use the easiest tier with sleeping enemies, so the safe play (pick them off one at a time) always works, and with no turn limits it always will unless enemies are awake. The Ridge opens on the enemies' turn, so two new role prompts are the first thing you see there.
- Options:
  - (a) "Early" tier (hits hurt 50% more than now) with lower health per enemy so kills stay quick; every fight starts awake (only the Ridge's corridor sleeps); the family moves first on the Ridge. Data only.
  - (b) As (a) but one tier harder ("Standard"). Data only; more risk of a new player losing a level.
  - (c) Early tier with today's enemy health. Data only; longer fights, about +1–2 minutes per level.
- Recommendation: (a), with (b) as the first lever if the safe play still wins without anyone getting hurt.
- Blocked meanwhile: the level data of all four post-Hearth levels.

**Q4. Should The Trail become two levels (The Trail, then The Pile), with the route choice and mission map moved to later content?**
- Context: today it's an empty walk, a route choice, one route level, then The Pile: about 14 minutes and four new things (FTP drain, Pass-by, Items, the map). The empty walk exists only because a map can open only after a won level. The route choice is also M2's one story choice (her blood or the tracks).
- Options:
  - (a) Two levels, route choice later. About 8 minutes; three fewer new things; the blood-or-tracks choice is lost.
  - (b) Keep the route choice: the opening walk gets a one-turn fight and both routes are reworked. About +3 minutes and one more level to build and tune.
  - (c) As built. No cost; your notes on The Trail stand.
- Recommendation: (a). The free pick of John or Mark already gives M2 a choice.
- Blocked meanwhile: The Trail's rebuild and its level graph.

**Q5. Should the sisters' first real Duo wait until M4, after the Yard scene, instead of finishing The Pile?**
- Context: The Pile ends on "Still counting?" / "…No.", the moment their race stops being funny. A shared Duo kill just before it reads as a win, and it uses up what the Yard scene is there to discover (they do better setting each other up). Memory 4's Duo still ends the Hearth as the first Duo.
- Options:
  - (a) Lock the sisters' Duo in M2 (data, one lock per level). The Pile ends on them fighting back to back, the tally alone; their first Duo comes in M4 after the Yard, framed by "We both did" (M4's design to follow).
  - (b) Duo as The Pile's planned finisher, locked in The Trail only (data), with an ability pulse pointing at it (data).
  - (c) Duo open throughout, as built. No cost; it may fire in The Trail, unframed, or as The Pile's opener.
- Recommendation: (a).
- Blocked meanwhile: The Pile's ending, its lines, and the locks.

**Q6. In Memory 4, when John reaches the den mouth, should the pools visibly die and every other Claw fade out, leaving the Duo's three Claws as the last fight?**
- Context: you said John should "cut the line, not turn limit", "maybe take him off the board", and "the first Duo should finish everyone". Today the pools keep spawning whatever happens, the last stage wants six Claws and John still on the mouth, and the Duo takes only three.
- Options:
  - (a) The pools stop and fade, John says a line, every other Claw fades ("the rest scatter"); the Duo always kills the last three and ends the memory. Two small non-core codes: a step that stops a pool, and the new fade step taught to take "every enemy but these" (pool-spawned Claws aren't in a fade group).
  - (b) The pools stop; the leftovers stay and must be killed. Only the pool step is new; about one more turn, and the Duo may hit a leftover and leave a cub Claw alive.
  - (c) As (a), and John fades out too. Data if a hero can be put in a fade group (to check), else a small addition to the same step.
- Recommendation: (a).
- Blocked meanwhile: the Memory 4 prefab edits.

**Q7. Should Home visit 1 get a short handover scene at the door, rather than being cut?**
- Context: the visit plays only the Workshop page today ("nothing in between"). The returning pair meeting the leaving pair is the scene "two go, two stay" promises; its lines exist in the narrative draft and aren't built.
- Options:
  - (a) Handover at the door: one clue line, the go-between joke, Ben's line into the Workshop pick. About 1 minute; small code so it plays only after the first pair mission.
  - (b) Cut the visit and move the Workshop to visit 2. Saves about 2 minutes; two decisions in one visit.
  - (c) As built. No cost; your note stands.
- Recommendation: (a). Scenes were what landed in Bond Lite.
- Blocked meanwhile: the Home tech plan's visit-1 part.

**Q8. Should the Hearth's Family Role changes (none before John, only John's in Memory 3) be left to the Family Roles redesign instead of patched now?**
- Context: the redesign's direction "no role works when its Bergson is alone" already makes Memory 1 (Linda alone) silent. Patching now means draining Linda's FTP in Memory 1, which shows an empty meter on the game's first screen, and a per-level role switch in core code for Memory 3.
- Options:
  - (a) Leave the Hearth's roles as built and hand the redesign one requirement: no role fires before Memory 3, and there only John's. No cost now.
  - (b) Drain Memory 1's FTP now (data); Memory 3 later. A new player may read the empty meter as broken; undone if the redesign lands.
  - (c) Build a per-level, per-hero role switch now. Core code, needs your OK; may be thrown away by the redesign.
- Recommendation: (a).
- Blocked meanwhile: nothing in this plan.

**Q9. Should John get his own short Memory 0 before Linda and Lucy?**
- Context: your idea. John's role guards someone near him, and under the redesign no role works alone, so alone he can't show it. The Hearth is about 13 minutes, on target, and Memory 3's first turn already belongs to John.
- Options:
  - (a) No.
  - (b) Yes: John alone with Shield Up and his sword. About +2–3 minutes and one new level.
- Recommendation: (a).
- Blocked meanwhile: nothing.

---

## Docs to update (if approved)

- `design/gdd/missions-structure.md`: the onboarding missions (the Hearth's stages with no caps; The River and The Ridge at Early with awake fight beats; M2 as two levels, no route, no FP drain, sisters' Duo locked, items unchanged); MI-27's table (The Trail and The Pile: "all enemies start alert"; the River's and Ridge's per-instance alert); MI-18 note for the result summary line and the goal-tile colour; Memory 4's stages and the hold.
- `design/gdd/combat-rules.md`: the Synergy aim-preview rule beside CR-37 (next free ID) once built.
- `design/gdd/family-systems.md`: a pointer from the Synergies table to the preview rule; nothing on roles.
- `design/level-chunks.md`: the 1-tile island/perch knob with the Linda-outranges caveat; link this plan from chunks 6, 13, 14, 23, 24.
- `plans/onboarding/2026-10-26-onboarding-levels.md`: mark The River, The Ridge and M2 sections superseded by this plan; the Hearth tables' cap rows; Memory 4's hold.
- `plans/onboarding/2026-10-25-onboarding-first-hour-design.md`: the flow table (M2 row; sisters' first Duo in M4), the S8 arc's Pile beat (no Duo).
- `plans/onboarding/onboarding-narrative-draft.md` (`miso-narrative`): the four result lines (no Claw counts for Memory 2), Lucy's multi-shot page, the clue lines at the placed tiles, the River and Ridge objectives, the Pile's partial-relief line, John's line at the mouth and Mark's "the rest scatter", the visit-1 handover, the rematch line's new slot.
- Family Roles plans (coordinator relays): the Hearth requirement (Q8) and the River/Ridge as the session's levels (Q1).
- `decisions.md` (coordinator): Q1–Q9, and the reversals: D-353 (Ridge enemy-first), D-355 (Pass-by panel), the levels plan's "Asleep panel required", C5's "no tab opens by itself", the Pile's Duo finisher.
- `glossary.md`: "The Trail" now names M2's first level as well as the mission; narrative to rename if confusing.

## Risks

- **Paper balance.** HP factors, Flare copy damage and Archer damage at Early are assumptions; the River and Ridge numbers wait for the Family Roles session; each level has a lever and a to-check row.
- **The Family Roles track slips.** Then Q1 (a) stalls the pair missions' tuning; fallback is Q1 (b), tune for roles as built.
- **Preview cost.** Three Synergy hooks in the attack preview; if the tech plan prices it high, Shield Flare first (the lesson the critics doubted most), the Bloom second, the return third.
- **Hand-edited prefabs.** Read each level back before rebuilding; Memory 4 is edited by hand only (D-405); the Lucy wiring tool must carry the D-457 gag before any re-run.
- **Cyclone in narrow places** (P9): no ★ needs the family to pass a Cyclone.
- **`AIRegressionTest`** may shift with the new levels: stays known red, never re-baselined.

## Gates

Design only. Before build: THJ's answers to Q1–Q9. Each build chunk: compile / EditMode (known red only) / review for code / THJ play check (feel and level chunks). Play check needs THJ's time: yes, the Family Roles session on the River and Ridge (Q1), then a timed run Home → M4 send-off, then a cold playtest. Grids changed in this revision (re-render all four): `after-river`, `after-ridge`, `after-trail`, `after-pile`: `python claude-handoff/tools/grid_render.py claude-handoff/plans/onboarding/2026-11-09-onboarding-after-hearth-design.md`.
