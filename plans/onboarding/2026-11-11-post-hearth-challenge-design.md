# Post-Hearth challenge: a turn where the family must give something up

Size: L    Tier: 3 (level design and game feel of the first hour; THJ decides)    Assigned to: miso-game-designer
Branch: `thj/after-hearth`, scope **all** (onboarding content; `main` holds the whole onboarding, D-456)
Status: **revision 2, to THJ's answers** (D-507 to D-510); waiting on THJ's look at the new *Follow the tracks*

> **Revision 2 (2026-11-11, THJ's answers).** D-507: HP per level is the designer's call (×1.0 or ×0.8 with more enemies), and existing enemy types may be used. D-508: *Follow the blood* as proposed. D-509: late arrivals as proposed. D-510: "Those archers are not good. Encore is taught in earlier levels. Redesign the level." So **Follow the tracks is redesigned from scratch around a Black Claw** ("who rings the bell"); the perch Archers, the arrow-budget puzzle and old rule 5 are gone; **the Pile's perch Archer is replaced by a second east Claw** (it served only as a cheap east target, and Linda's lane to it crossed unverified rock). Coordinator's grid checks fixed: the Pile's lane (moot now), the Duo distance to 9,3 (7), and the Trailhead's threat line (Claws walk through allies: `ignoreRelationOnWalk` = Ally on `DarkClaw_Ability_Walk`). The critics' tables below are kept as history of revision 1; where they mention Archers on the tracks or the Pile, revision 2 supersedes them.

Source: THJ's play of the reworked Trail ([`playtests/2026-11-11-trail-rework-play.md`](../../playtests/2026-11-11-trail-rework-play.md)), the four logs it cites, and D-505 (this round). Builds on the approved [after-Hearth design](2026-11-09-onboarding-after-hearth-design.md) (D-466 to D-475) and the C1 build committed as the base (D-503, D-506). Family Roles are being rethought separately ([rethink](../2026-11-09-family-roles-rethink-design.md)); nothing here depends on a new role rule.

## Why

THJ, 2026-11-11: "still sense no challenge… I did not even have to stop a second to think twice… It was all HP." In the logs the first family turn decides every Trail fight, and enemies land 0 to 3 hits per level.

## Goal

Every post-Hearth level has at least one turn where the player must choose what to give up, and the family's first turn never decides the fight, with no new rule, no new on-screen element, and M2 at most about 1.5 minutes longer.

## Acceptance criteria

- [ ] In each Trail level's combat log (THJ's timed run), at least one enemy group acts after the family's best first turn, and at least two enemy actions land per level.
- [ ] Each level has a named decision turn (in its table) with **two good plays that pay in different currencies** (arrows against HP, this sister against that one, tempo against safety). No level is a single ★ plus a trap.
- [ ] Every competing demand is on screen, or announced, **before** the turn its cost is paid. Waves appear at least one full player turn before they act, never on or next to the family's start tiles.
- [ ] No new rule, status or UI element: level data, existing objective conditions, existing reveals, per-instance HP.
- [ ] No post-Hearth level runs past 5 rounds; M2 at THJ's pace stays within about 11.5 minutes (the 11-09 plan: 10).
- [ ] After the timed run, THJ says he had to stop and think in each level.

## Scope

In: the four Trail levels (`m2-trailhead`, `m2-tracks`, `m2-blood`, `m2-pile`; they replace the built blocks), the River and Ridge paper blocks (`after-river`, `after-ridge`; they replace the unbuilt 11-09 blocks), M2's per-instance HP, catalogue knobs.
Out: Family Role rules (the rethink), the Hearth, Home, Duo and Synergy rules, final text (`miso-narrative` writes the lines named here), new enemy types (Q5 only).

## Touches

Systems: level prefabs `GB_m2-trailhead`, `GB_m2-tracks`, `GB_m2-blood`, `GB_m2-pile` (rebuilt from the blocks), their wiring tool `SearchWiring.Trail.cs` and `SearchTrailTests.cs` (editor code only); the River and Ridge blocks for after-Hearth chunk 4 (not built). Runtime code: none. Core: none.
USPs: Family Roles (as built), Synergies, Duos (the movement Duos get their first ★), Home (neutral).
Docs: see [Docs to update](#docs-to-update).

---

## Problem and evidence

**Symptom (THJ):** no challenge, no need to think, "all HP".

**Root problem: no turn ever asks for more than the family can do in it.** Each level poses one problem (one group, one goal, kill everything), places it where the family's whole first turn reaches it, and lets the family act first. With one demand and enough tools to meet it, there is nothing to give up, so there is no decision; the aim preview then makes the one right answer visible. Three facts in the build make that true, and all three have to change together:

1. **One demand at a time.** Each level has one group in one place (or two that one area answer covers) and "defeat all" as its only goal. Nothing competes for the family's AP, arrows or position.
2. **The kill is too cheap.** At ×0.6 a Claw has 10 HP. Any one family action, or one action plus Lucy's free follow-up (two sidewinders, 3 each = 6), kills it: Explosive 8, Blitz 8, sword 8, bow 6 + 6. Watch + follow-up killed a fresh Claw in the enemy phase (tracks log). Six AP plus free reactions kill four to six Claws a turn wherever they stand near Lucy. No spacing survives "every hit is a kill".
3. **Enemies never threaten first.** Every Claw starts 4+ tiles away, the family moves first, and the free enemy-phase roles (Watch, the follow-up, Mark's counter) finish whatever the volley crippled. Nothing on the board ever needs protecting.

The 11-09 premise ("challenge what the Hearth taught": one ★ Hearth tool per beat) produced levels whose ★ *is* the level. The fix is not a harder ★; it is a second demand.

| Evidence | Where | What it shows |
|---|---|---|
| Trailhead won in 1 round, 0 damage, both runs | Logs 120958, 121912 | The fight ends before an enemy acts |
| 0 to 3 enemy hits per level; 12 and 15 damage over the whole mission | Same logs, coordinator's table | Enemies barely act |
| Explosive 8 on three Claws in the gully column / the Pile's west lane, then Watch and the follow-up finish | Blood and Pile logs | The layouts line enemies up for the area answer |
| Watch 6 + the follow-up killed a fresh 10 HP Claw (tracks); Watch killed two crippled Claws (Pile) | Tracks and Pile logs | Free reactions turn every cripple into a kill |
| Chained Assault killed three Claws in one action, twice; fired by Lucy on 3,6 at 0,4 (5 steps) | Blood and Pile logs; `Mark_Lucy_Duo_Ability.asset` `radiusV` 5 (read) | The Duo reaches 5 from the activator, and 10 HP never survives it |
| Archers at 6 HP: one Cyclone, one ember volley or one arrow kills | Tracks and Pile logs | Archers are never a threat |
| Mark went down once, after running alone into the Pile's east group (THJ: "reckless") | Pile log, Mark run | Damage lands only when the player walks into it |
| Bow falloff ×0.6 in play (6, then 4) | Every log | The pierce cripples the second enemy; the 11-09 paper (falloff 1.0) overstated it |
| Hero move 3; arrows cross a gap row | Every log; tracks log (4,2 → 4,6 over row 4) | Used for every distance below |
| Every logged follow-up and ember hit was capped by the target's remaining HP (`4→0`, `2→0`, `6→0`) | All logs | The draft's "follow-up 4" came from capped lines; the presets give 6 (systems critic) |

River and Ridge: their logs are level-complete cheats (no evidence), and their after-Hearth layouts (chunk 4) aren't built. They're in scope because the same premise drew them.

---

## Options compared

| | A. Numbers only | **B. Two demands per turn** | C. A second objective in every level | D. Take tools away | E. New enemy types | F. Do nothing |
|---|---|---|---|---|---|---|
| What changes | Standard tier or more HP everywhere | Each level puts two demands on one turn: fronts that no single answer covers, late arrivals announced a turn ahead, groups that start in reach, one existing enemy type where it sharpens the question (rev. 2: a Black Claw on the tracks); the M2 HP override removed so a kill costs two actions | Protect, reach, escape or timer goals added everywhere | Lock all Duos, drain FTP, fewer arrows | Black Claw (hit it and its pack turns on you) or Dark Shaman (heals its kind) in M2 | — |
| Player experience | Longer fights, same answer | Each level has a turn where something gets through, and the player picks what | Strong choices, but every level becomes a special case | Fewer answers, not harder questions | A direct counter to the volley; one more thing to learn | THJ's notes stand |
| New things to track | 0 | 0 (one existing objective type, a reach tile, on one route) | 1 per level | 0, but known tools vanish | 1 per enemy | 0 |
| Build | Data | Rebuild 4 Trail levels from blocks, wiring (editor code), tests; 2 paper blocks for chunk 4 | Same, plus objective wiring and story changes per level | Data | Data, plus intro close-up text (built, untexted) | 0 |
| Risk | "All HP" again (THJ's exact objection) | AI paths differ from paper; the Pile sits at the emotional peak | Story strain; time | Duos USP weakened; feels like a nerf | Complexity budget; the Shaman reads as later content | — |
| USP effect | Neutral | Roles + (each pick's role holds one front), Synergies +, Duos + | Mixed | Duos − | Roles + (John rings the bell) | Neutral |

---

## Recommendation

**Option B**, with one objective from C on one route (*Follow the blood*: reach the end of the trail, two of you) and E only as a question (Q5).

Five rules for the level designer. The player learns nothing new from them.

1. **Two demands, one turn, two good answers.** At the decision turn, two threats each need the family's best answer and the family has one. The two plays pay in different currencies, and both are defensible. Fronts sit far enough apart that John's 2-tile guard covers one sister, Lucy's follow-up (within 3) reaches one side, and a blast or a pierce takes one side.
2. **Nothing lines up for free.** At level start no row or column in Linda's reach holds more than two enemies, and no blast cross more than two.
3. **Someone acts, and the player sees it coming.** At least one group starts within 5 of a hero (a Claw's move 4 + 1). Late arrivals appear at the start of the family's turn 2 with a camera beat and a bark, and act on enemy turn 2: one full player turn ahead (the Into the Breach rule), never on or next to the family's start tiles.
4. **A kill costs two actions** (where Lucy's follow-up is in play). M2 Claws lose their HP override and play at their Early value, ×1.0 = **16 HP** (the tracks use ×0.8, see below). The best single action plus a free follow-up is 14 (Explosive, Blitz or sword 8 + 6), so it never kills a Claw; two actions do (Blitz + Blitz with Focus, Explosive + bow + follow-up). Chained Assault (11 × mash) needs a strong mash plus another hit. This is the tier's own number, not "more HP": the 11-09 plan's ×0.6 is what made every hit a kill.
5. ~~A shot at a perch costs an arrow for the fight.~~ **Dropped in revision 2** (D-510: the perch Archers didn't play well, and Encore is taught earlier). No post-Hearth Trail level uses a perch Archer now; the River keeps its ford Archers, which are the Shield Flare lesson (11-09, approved).

**HP per level (D-507):** Claws ×1.0 (16) at the Trailhead, on the blood route and at the Pile, where Lucy's follow-up decides kills; ×0.8 (13) on the tracks, where the Black Claw's call walks the pack into the family's reactions and the question is who gets hit, not how fast they die.

### Starting values

| Lever | Today (C1) | Proposed | Note |
|---|---|---|---|
| Claw HP, M2 | ×0.6 (10) | **×1.0 (16)** (override removed) on the Trailhead, the blood route and the Pile; **×0.8 (13)** on the tracks | D-507. River and Ridge: D-466 timing; start values in their sections |
| Archers, M2 | Two on the tracks, one at the Pile, ×0.25 | **None** | D-510 |
| Black Claw, M2 | None | **One, on the tracks, ×0.5 (20)** | D-507; [its learning, showing and cost](#the-black-claw-what-the-player-learns) |
| Tier | Early | Early (×0.75 damage: Claw 4, Archer 3) | Unchanged |
| Alert | All alert | All alert; reveals come in alert | Unchanged |
| Turn order | Family first | Family first everywhere | Weighed and rejected: enemy-first hits the player can't answer are a tax, and Watch + follow-up eat an enemy-first approach anyway |
| Duos | Sisters' Duo locked; the pick's open | Unchanged | At 16 HP a Duo cripples three; it no longer wipes |
| FTP | Full at the Trailhead | Unchanged | |
| Late arrivals | None (C1 removed the Pile's rear wave) | **Tracks: 2 Claws; Blood: 2 Claws**, at the start of turn 2 | D-509. Hidden groups revealed by a stage (the Pile's pattern) with a camera move and a bark |

### What each pick changes (roles as built)

| | Mark picked | John picked |
|---|---|---|
| Strength | Two Blitzes kill one Claw; Continuous Attack chains; a counter on every hit within 2 | Guard redirects every hit within 2 at ×0.5; Shield Up + Wrath; Shield Flare |
| What the levels ask | Hold one side alone (15 HP): the counter pays only if Mark is the one being hit | Choose which sister to cover |
| The give-up | Mark's HP (it carries through M2, CR-24) | The uncovered sister's HP, or John's across three levels |
| If roles become "kept AP" (rethink option C) | Fewer free kills: harder. First lever: Claws ×0.8 | The guard stops being free: much harder. Same lever |

---

## The Trail, level by level

Prefab coordinates, x from the left, y from the bottom. Values: hero move 3; Claw move 4 (reach 5); Black Claw's call: every Dark Claw within 5 (eight-way) targets whoever used an ability on it (EN-1); Linda's bow 4 in a line (6, then ×0.6), Explosive within 5 (8 on a cross), three arrows; Lucy's embers within 3 (main 4, each sidewinder 3), her follow-up 6 on an enemy within 3 of her; Mark's Blitz 8 within 2; John's sword 8; Chained Assault up to 3 targets within 5 of the activator. Damage at Early: Claw 4, Archer 3.

### 1. The Trailhead, "front and back" (replaces `m2-trailhead`)

The family stops in the trail; Claws come at them from ahead and from behind. One to two rounds.

```grid id=m2-trailhead title="M2 · The Trailhead: front and back (prefab coordinates)"
c . . U L . . . c c . .
. c . J . . # . . . . .
--
cells 0,1 1,0 enemy behind: reach Lucy now
cells 8,1 9,1 enemy ahead: reach Linda now
arrow 4,1 8,1 linda dy=-8 Explosive, then the bow
arrow 3,0 1,0 mark dy=8 the pick turns round
level name The Trailhead
level tier standard
level alert all
level deploy 3,0
```

| Item | Plan |
|---|---|
| Source | `GB_m2-trailhead`, rebuilt: a 12 × 2 trail with one rock (6,0); units re-placed |
| Question | They're on both sides. Where does Lucy's fire go? |
| Squad | Lucy 3,1, Linda 4,1, the pick 3,0 (deploy) |
| Enemies | Behind: Claws 0,1, 1,0. Ahead: Claws 8,1, 9,1. ×1.0 (16), alert, Early |
| Threat on turn 1 (verified) | 0,1 and 1,0 are 3 from Lucy (1,0 is 2 from the pick): both hit this enemy turn. Ahead, Claws walk through each other (`ignoreRelationOnWalk` = Ally), but Linda has one free side within their reach: 5,1 (3 steps from 8,1, 4 from 9,1 through 8,1). 4,0 is 6 steps from either (the rock on 6,0 forces the detour), and Lucy holds 3,1. Whichever moves first takes 5,1 and hits Linda; the other ends in her row (6,1 or 7,1): Watch. Which one is the AI's order (to check); the outcome is the same |
| Decision turn | **Player turn 1.** Neither side dies to one hero. Lucy's embers and follow-ups (within 3) can serve the rear or, if she walks east, the front, not both |
| ★ A: Lucy stays back (Mark run) | Mark Blitz 1,0 (8) + follow-up (6), second Blitz kills, Continuous Attack (1 FTP) on 0,1 (8) + follow-up (6), Lucy's main ember kills. Linda alone ahead: Explosive on 8,1 from 4,1 (8 and 8), bow on 8,1 (6): 8,1 at 2, 9,1 at 8. Enemy turn: Watch on 9,1 (to 2), both hit Linda: **Linda −8, the rear safe** |
| ★ B: Lucy goes forward | Lucy to 5,1 (sidewinders and follow-ups on 8,1 and 9,1 within 3), the pick holds the rear alone: the front pair dies over two turns, and the rear pair, one of them alive after the pick's turn, hits the pick or follows Lucy: **about −8 on the pick or Lucy**. John run: John Shield Up between, guarding Lucy; his HP pays |
| Careless loses | The Hearth habit: everyone faces east, Linda pierces (6, 4: nothing dies at 16). Both rear Claws hit Lucy and the front pair hits Linda: **about 16 spread, carried into the route** |
| Cues | Start: the rematch line and the "stays home" line (C2, THJ's pick pending). The pick's bark on the rear pair ("Behind us!", narrative) as the level opens, while the camera shows both pairs |
| Win | Defeat all → mission map (as built) |
| Time | ~2 min (2 rounds) |

### 2a. Follow the tracks, "the bell" (replaces `m2-tracks`; revision 2, from scratch)

The tracks are big, and a pack's: a Black Claw leads two Dark Claws down the hollow, and two more answer its call on turn 2. The route's question is not where to go (that's the blood route) but **who gets hit**: whoever strikes the Black Claw draws its whole pack.

```grid id=m2-tracks title="M2 · Follow the tracks: the bell (prefab coordinates)"
# # . . . . . . . #
. . . . # . . . . c
L U . . . c . b . .
J . . . . . # . . c
# # . . . . . . c #
--
range 7,2 5 enemy the Black Claw's call
cells 9,3 9,1 enemy hidden: answer on turn 2
arrow 1,2 7,2 linda dy=-8 the trap: the pierce reaches the leader
note 4,3 rock
note 6,1 rock
level name Follow the tracks
level tier standard
level alert all
level deploy 0,1
level hidden pack 9,3 9,1
```

| Item | Plan |
|---|---|
| Source | `GB_m2-tracks`, rebuilt: a 10 × 5 hollow with two rocks (4,3, 6,1); the islands, the perches and the gap row go |
| Why this route | Contrast with the blood route. Blood asks *where do you go* (tempo against safety, a reach goal). Tracks asks *who takes the hits* (whose HP pays), with defeat-all as the goal |
| Question | Strike the leader with the one who can take it, or never strike it until the rest are gone? |
| Squad | Linda 0,2, Lucy 1,2, the pick 0,1 (deploy) |
| Enemies | **Black Claw** 7,2, ×0.75 (30); Dark Claws 5,2 and 8,0, no override (16). **Hidden:** Dark Claws 9,3, 9,1, no override (16), revealed at the start of turn 2 (stage "turn 2 reached", onComplete camera + bark + reveal). All alert, Standard. 94 HP in all (D-516) |
| The call (EN-1, built) | Any ability used on the Black Claw makes every Dark Claw within 5 of it (eight-way) target the user through their next turn. All four Dark Claws, the late pair included, start within 5 of 7,2 (5,2: 2; 8,0: 2; 9,3: 2; 9,1: 2) |
| Threat on turn 1 (verified) | 5,2 is 4 from Lucy: it walks to 2,2 and hits her. 8,0 (9 from the nearest hero) and the Black Claw (6 from Lucy) arrive; the Black Claw on 3,2 or 4,2 ends in Linda's row within 4: **Watch prompts on it**, and pressing rings the bell on Linda. The press is the player's (FR-2: a missed or declined press costs nothing) |
| Decision turn | **Player turn 2.** The leader is near, the late pair has just appeared inside its call, and every hit on the leader now pulls four Claws onto whoever lands it |
| ★ A: ring it on the tank (pays the tank's HP) | John steps beside the Black Claw, sword (8): all four Claws turn on John; Shield Up with his second AP (60% taken, Wrath stacking to 3). The sisters hit freely while the pack queues on John, and the queue walks through Linda's lanes (Watch). Turn 3: Wrath Shield Dash into the clump. Mark: Blitz the leader from a tile behind Linda's lanes, so the called Claws must cross them; counter each one that reaches him. Mark's 15 HP and Linda's arrows pay |
| ★ B: leave it alone (pays tempo and spread hits) | Kill 5,2, then 8,0 and the late pair; keep every lane, blast and ember off the leader (Explosive on 5,2's cross doesn't touch 7,2; one on 6,2 would); decline Watch on it. The leader fights unrung and its hits spread; it dies last, to everyone at once |
| Careless loses | The Hearth habit: Linda steps to 3,2 and pierces 5,2 and the leader in one line (the aim preview shows damage on the leader: that's the warning). Four Claws and the leader on Linda: **up to 20, Linda down** (Revenge then fires for the others) |
| Levers | If reflex presses ring the bell too often in play (Watch on the leader, or Lucy's follow-up after someone else hits it): first start the leader on 7,3 so its approach runs along row 3, off Linda's start row; then the leader ×0.4. If the bell never rings: the late pair one tile closer, so ★ B costs more |
| Cues | The Black Claw's first-appearance close-up (EN-10, built) with one intro line; the pick's bark at the start ("That big one leads them.", narrative); the late pair's camera and bark on turn 2 |
| Time | ~4 min (3–4 rounds) |

#### The Black Claw: what the player learns

- **Rule (one sentence):** "Hit the big one and its whole pack comes for you."
- **How the level shows it (no new UI):** the built first-appearance close-up (EN-10) with one line; its bigger sprite; the "Pact Leader" status on its info panel when hovered; the pick's bark; Linda's aim preview showing damage on the leader when her line reaches it. After a hit, every Claw's next-target line swings to the hitter (EN-10), so the rule shows itself the first time.
- **What isn't shown before the click:** the call itself isn't previewed (the same limit as the Masher's counter, EN-2, Q9). The level puts the trap where the preview already warns (the pierce line) and keeps it survivable (Linda 20 HP; Revenge if she falls).
- **Cost:** data only. `Unit_BlackClaw` exists (`b` in the grid tool, `GridPalette.cs`); per-instance HP via the wiring's `SetHealth`; the intro line is text. No code.
- **Family Roles:** John's guard and Shield Up are the natural bell-ringer (D-217's "father's instinct"); Mark's counter pays per called Claw; Watch is both the trap (pressing on the leader) and the reward (the called queue walks through her lanes).

**Encore on the tracks:** the old Encore cue was on "both Archers dead"; with no Archers, that stage goes (THJ: Encore is taught earlier, D-510). The level is one stage after the reveal stage: defeat all.

### 2b. Follow the blood, "two of you, to its end" (replaces `m2-blood`)

The blood runs east through two 1-tile chokes, past three gullies. **The objective is to reach the end of the trail, two of you**, not to kill everything. Claws come down the gullies, and more follow.

```grid id=m2-blood title="M2 · Follow the blood: two of you, to its end (prefab coordinates)"
# # # # c # # # # . # # # # c # # # # #
# # # # . # # # # c # # # # . # # # # #
# # # # c # # # # . # # # # c # # # # #
L U . . . . . . . . . . . . . . . . . .
J . . . . . # # . c . . . . . . # # . .
--
cells 18,1 19,1 19,0 note the end: two of you
cells 4,4 14,4 enemy hidden: come down on turn 2
note 6,1 choke
note 16,1 choke
arrow 5,1 8,1 mark dy=-8 Vault
note 5,0 Cyclone seals the trail behind
level name Follow the blood
level tier standard
level alert all
level deploy 0,0
level hidden gullies 4,4 14,4
level camera 18,1
```

| Item | Plan |
|---|---|
| Source | `GB_m2-blood`, rebuilt: a 20 × 5 trail, gullies at columns 4, 9 and 14, chokes at 6,1–7,1 and 16,1–17,1 |
| Question | The trail goes on and they keep coming. Fight here, or move? |
| Objective | Line: **"Follow the blood. Two of you, to its end."** (narrative may polish; it replaces the line, it doesn't add one). Win: an any-group of "Tiles occupied, at least 2 of 18,1 / 19,1 / 19,0" (`AggregationMode.AtLeast`, target 2: exists, read in `LevelObjectiveConditions.cs`; the `Tiles()` helper in the wiring hard-codes Any, a one-line editor change) **or** "every enemy dead", that second one **hidden** from the objectives panel. A fallen hero leaves its cell, so it can never hold or block a goal tile. The opening camera shows the end tiles (`level camera`), then pans back |
| Squad | Linda 0,1, Lucy 1,1, the pick 0,0 (deploy) |
| Enemies | 4,2 (gully 1), 9,3 (gully 2), 9,0 (on the trail past choke 1), 14,2 (gully 3). **Hidden:** 4,4 and 14,4, revealed at the start of turn 2 (one behind the convoy, one ahead) with a camera move and a bark. ×1.0, alert, Early |
| Distance | Linda 18 steps to 18,1, Lucy 17: three turns of moving with nothing in the way, so the convoy meets the late pair whatever it does |
| Threat on turn 1 (verified) | 4,2 reaches Lucy (4,1, 3,1, 2,1): hits her. 9,3 walks to choke 1 (9,2, 9,1, 8,1, 7,1); 14,2 to 11,1; 9,0 into the trail. Linda can't be hit at the start (rock, Lucy and the pick around her) |
| Decision turns | **Every turn:** each AP spent killing is an AP not spent walking. **Turn 2 is the sharp one:** a Claw is behind the convoy and one ahead, both seen a turn before they act |
| ★ A: run (tempo) | John: Shield Dash along row 1 (3, through allies, hits and pushes each enemy beside the path) opens a choke; the **John–Linda Dance** moves both 4; the guard covers whoever's within 2. Mark: **Vault** over a choke blocker (3); the **Mark–Linda Footrace** sends both runners. Lucy: **Cyclone** in the trail behind (it blocks walking under the current rules and under the planned Pulling Gale; this ★ uses only the blocking, not its drift or damage), so gully 1 and the late Claw behind can't follow. Pays in HP: everything left alive gets a swing |
| ★ B: clear as you go (safety) | Kill each blocker before stepping past it; Explosive when two bunch at a choke. Pays in tempo: the late pair joins, five rounds |
| Careless loses | Fights gully 1 to the last Claw, then meets three more at choke 1: **12 to 16 spread, carried to the Pile**; or one runner alone ahead (the objective needs two) |
| Clue | The end tiles are the clue beat: arriving plays the "her blood" close-up (narrative), then the win |
| Time | ~4 min (3–4 rounds) |

### 3. The Pile, "back to back" (replaces `m2-pile`)

The search stays one move long and answers something (D-504). The ambush comes from both sides, spread so no single answer catches a side, and the east side falls fastest so the last enemy is usually at the sisters.

```grid id=m2-pile title="M2 · The Pile: back to back (prefab coordinates)"
# # # U L . # # # # #
. c . . . J . # . . .
. # # . _ _ . . . c .
. . . . _ _ . . . . #
. . . . . . . . . . c
# c . . . . . . . . #
--
zone 4,2 5,3 note the pile
cells 3,3 6,3 note search (either tile)
arrow 4,5 1,4 linda dy=8 Explosive west
arrow 6,4 9,3 linda dy=-8 Explosive east
level name The Pile
level tier standard
level alert all
level deploy 5,4
level hidden west 1,4 1,0
level hidden east 9,3 10,1
```

| Item | Plan |
|---|---|
| Source | `GB_m2-pile`, rebuilt: 11 × 6; pile props on 4,2–5,3. **Revision 2:** the perch Archer (7,5) is gone and 7,5 is rock; a second east Claw stands on 10,1. The Archer served only as a cheap east target, and the only lane to it crossed rock (6,5), never verified for arrows |
| Squad | Lucy 3,5, Linda 4,5, the pick 5,4 (deploy) |
| Search | "Search the pile.": any Bergson on 3,3 or 6,3 (2 steps from the pick, 2 from Lucy, 3 from Linda). Then Lucy "No white fur… she's not here." (D-504), then the reveal with the camera on each side (as built) |
| Enemies (revealed, alert) | West: Claws 1,4, 1,0. East: Claws 9,3, 10,1. All ×1.0: 64 HP (C1: 56, in lines). C1's 10,0 Claw is removed |
| Threat after the reveal (verified) | 1,4 reaches 3,3 (3), 3,4 (2), Lucy on 3,5 (3). 1,0 reaches 3,3 (5) and 3,2. 9,3 reaches 6,3 (3) and 6,4 (4). 10,1 reaches 6,2 (5) but not 6,3 (6): it arrives and strikes on turn 2. Chained Assault from 3,4 reaches 1,4 (2) only: 1,0 is 6, 9,3 is 7, 10,1 is 10 |
| Decision turn | **The first full turn after the reveal** (the searcher's other AP plus everyone else). West: two Claws coming for the sisters at once. East: one now, one next turn, on the pick. Each ★ pays a different hero |
| ★ A: break the east, brace the west | Linda to 6,4 (through the pick on 5,4, 3 steps), Explosive on 9,3 (4 away): 8; the pick finishes it (Mark: to 7,3 via 6,4 and 6,3, Blitz 9,3 from 2 away: 8, dead; John: Shield Dash or sword next turn). 10,1 comes alone next turn. The west pair hits a sister: **about −8 on Lucy or Linda**, and the last kill usually lands at the sisters (the ending's shot) |
| ★ B: break the west, brace the east | Linda's Explosive on 1,4 from 4,5 (4 away), Lucy's embers from 3,4 and her follow-ups: 1,4 dies; 1,0 arrives alone. The pick holds the east under 9,3 now and 10,1 next turn: **about −4 to −8 on the pick** |
| Careless loses | The pick searches 6,3 first, alone; the family spreads: 9,3 hits the searcher, 1,4 and 1,0 hit whoever stands at 3,3 to 3,5: **about 12 in one enemy turn**, more on turn 2 when 10,1 joins. A mission loss needs all three down, so it's unlikely, but it is the risk to watch (CR-34: a loss ends the mission) |
| Ending | Unchanged: the last kill, back to back, the tally alone, "Still counting?" / "…No." (D-470). 10,1 arriving a turn late and the west pair arriving together make a west kill, at the sisters, the usual last one; if the pick lands it far away, the outro still stages the sisters together (to check in play) |
| Time | ~4.5 min (search + 3 rounds) |

---

## The River and the Ridge (paper; chunk 4, not built)

The same five rules, with the smallest change to the 11-09 blocks. Their numbers still wait for the Family Roles session (D-466); the start values below follow rule 4.

### The River: the far bank comes when the ford opens (replaces `after-river`)

One change: the far-bank pair is hidden and revealed alert when stage 2 starts (with the camera pan over the ford), instead of sleeping until John's step wakes it unseen. So the ford stage opens on two demands, seen together: the Archers (the Shield Flare lesson) and two Claws crossing.

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
cells 14,3 15,4 enemy hidden: come at stage 2
note 7,3 out of every Archer's reach
arrow 11,3 10,4 9,5 lucy dy=-6 Flare
arrow 11,3 12,4 13,5 lucy
arrow 11,3 10,2 9,1 lucy
arrow 12,2 11,3 lucy ember John
step 11,3 2
note 12,2 out of their reach
note 16,3 clue R7-4/5
level name The River
level tier early
level alert all
level hidden farbank 14,3 15,4
```

| Item | Plan (changes from the 11-09 table only) |
|---|---|
| Far bank | Claws 14,3, 15,4: hidden group `farbank`, revealed alert in stage 1's onComplete, with the ford camera pan. They cross on the next enemy turn (14,3 → 10,3) |
| Decision turn (verified) | **Stage 2's first turn.** The Claws reach the ford mouth; 8,3 to 10,3 are in Archer reach (9,5: 8,3 at 3, 9,3 at 2; 9,1: 8,3 at 3); 7,3 is out of every Archer's reach (4 from 9,5 and 9,1). ★ A: hold 7,3 and let them come (safe, a round slower). ★ B: go for the Flare tiles now, with two Claws on John and Lucy (John's guard makes it affordable as built; under kept AP it isn't). Pays tempo against John's HP |
| Flare tiles | Unchanged: 11,3 is 4 from all three islands; 12,2 is 6, 4 and 4 |
| Start values | Clearing and far-bank Claws ×1.0 (sword 8 + follow-up 6 = 14 < 16); ford Archers per the 11-09 Flare check; final after the Family Roles session (D-466) |

### The Ridge: one Claw already behind them (replaces `after-ridge`)

The 11-09 pack (a plus on 1,4) is exactly the "one blast clears it" layout. Now three pack Claws are spread so a blast takes two, and one stands beside Mark in the south pocket from the start.

```grid id=after-ridge title="The Ridge, after the Hearth (prefab coordinates)"
. . . # # # # # # # # # #
c . c # # # # # # # # # #
. . . # # # # # # # # # #
. c . # # # # # # # # # #
. . . . # # # # # # # # #
. L M . . . c c . . c . .
# . c # # # # # # # # # #
--
cells 0,5 2,5 linda Explosive takes these two
arrow 1,1 1,5 linda Explosive Arrow
note 2,0 already behind Mark
arrow 5,1 8,1 mark dy=-10 Vault
arrow 4,1 8,1 linda dy=6 out
arrow 8,1 4,1 mark dy=12 back
step 8,1 2
note 3,2 clue G9-2 herbs
note 12,1 clue G9-3/4
level name The Ridge
level tier early
```

| Item | Plan (changes from the 11-09 table only) |
|---|---|
| Pack | Claws 0,5, 2,5, 1,3 (alert) and 2,0 (alert, beside Mark). The only blast that takes two is Explosive on 1,5 (0,5 and 2,5); 1,3 stands alone in Linda's column, 2 away |
| Threat on turn 1 (verified) | 1,3 is 2 from Linda; 0,5 is 5 (down column 0 to 0,1); 2,5 is 4 from Mark (to 2,2); 2,0 is beside Mark and one step from Linda. All four can hit on enemy turn 1. Family first (D-468) |
| Decision turn | **Turn 1.** ★ A: Mark kills 2,0 (two Blitzes), Linda blasts the north pair and arrows 1,3; Watch and the counter take the cripples as they come; about 8 taken. ★ B: Mark chains north (Continuous Attack, FTP 1 then 2) and leaves 2,0 to hit him (counter). The FTP is 5 and shared by Continuous Attack, Watch and the counter: it can't pay all three |
| Corridor | Unchanged (Catch & Return) |
| Start values | Pack ×0.8 (no Lucy here: the best single action is 8, so 13 already takes two), corridor ×0.85, 10,1 ×0.6; final after the Family Roles session (D-466) |

---

## Lens notes

### Creative

**Target experience.** The Trail is the first time the family is outnumbered and has to protect each other rather than hit harder: Papa covers one daughter and not the other; Mark holds a side alone; the sisters stand back to back because nobody else can. Warmth against dread: the dread is "they're on both sides"; the warmth is the family choosing who stands where.

**The moment designed for:** the Pile's turn after the reveal. The search answers ("she's not here"), relief for one breath, then Claws on both sides; the player looks at the board and decides who faces which way, with the tally still on screen. The east falls, the last Claw comes for the sisters, and they finish it back to back.

Secondary: the Trailhead's "Behind us!"; the blood trail's Cyclone sealing the gully behind the convoy; the end of the blood trail as the clue's reward.

**Originality.** Two fronts and announced arrivals are genre staples (Into the Breach, XCOM pods, Fire Emblem reinforcements). Miso's own: the give-up is spent in family terms (whose HP, which sister John covers, who rings the bell), and the movement Duos answer a reach objective nobody has asked for before.

### Systems

- **Levers, in order:** late-arrival size (2 → 1 or 3), Claw factor (1.0 → 0.8 or back toward 0.6 only for a cold-player fix), the Black Claw's factor (0.5 → 0.4) and its distance from the late pair (outside 5, the call no longer reaches them), the Blood goal's distance, front distance.
- **Interactions:** Lucy's follow-up (6, no limit as built) is the main multiplier, so each level keeps her follow-up radius to one side. Chained Assault reaches 5 (data), so it can touch both fronts at the Trailhead; at 16 HP it cripples rather than wipes. The Black Claw's call answers any ability on it, Watch and Lucy's follow-up included (EN-15): a role press on the leader rings it, and declining the press is the counter (FR-2). Hidden units aren't counted by objectives until revealed (`HiddenLevelUnits`). Revealed units come in alert under "all start alert" (C1's risk note).
- **Dominant strategies checked:** John + clump: the Pile's and the Trailhead's fronts put one sister outside the guard; still the strongest pick, paid in John's HP across the mission. Sit in a safe corner (tracks): the north-bank pair lands inside it. One runner (Blood): needs two. Sprint (Blood): 17 to 18 steps means three turns, and the late pair is on the trail by turn 2. Kill-all fallback (Blood): the late pair isn't counted until revealed, but killing all four placed Claws on turn 1 is out of reach at 16 HP.
- **Failure cases:** AI paths differ from paper (each arrival is to check); the Pile at the emotional peak (lever: the 10,1 Claw out, then one west Claw); the Blood route a slog for a player who never moves (costs time and HP only, no cap); M2 runs past 11.5 minutes (lever: the Tracks late pair to one Claw).

### UX

| Moment | Shown | The player clicks | Likeliest misread |
|---|---|---|---|
| Trailhead, turn 1 | Both pairs on screen; the pick's "Behind us!"; next-target lines from the rear pair to Lucy | Lucy's side; Linda's blast ahead | Everyone faces east (the Hearth habit); the rear target lines are the warning |
| Tracks, start | The Black Claw's close-up and intro line; the pick's "That big one leads them."; "Pact Leader" on its info panel | Kill 5,2 without touching the leader | Pierces 5,2 and the leader in one line; the aim preview's damage on the leader is the warning |
| Tracks, enemy turn 1 | Watch prompts on the leader as it enters Linda's row | Decline, or press on purpose | Presses by reflex and rings the pack on Linda: the riskiest read in the plan (to check in play; fallback in the Tracks table's levers) |
| Tracks, turn 2 | Camera and bark: two Claws answer the call, seen a full turn before they act | Who rings it, or nobody | Rings it with Lucy's embers (the pack on Lucy, 15 HP) |
| Blood, start | Camera on the gold end tiles, then back; the line "Follow the blood. Two of you, to its end." | Move | Treats it as defeat-all (the habit); the line, the camera and the tiles say otherwise, and the kill-all fallback stays hidden |
| Blood, turn 2 | Camera and bark: one Claw behind, one ahead | Cyclone behind, keep moving | Turns back to fight the one behind |
| Pile, reveal | Both sides at once, the camera on each | Who faces which way | Sends everyone to one side; the other side's target lines show who pays |

**On-screen elements added:** none. **Text:** three lines (the Trailhead bark, the Blood objective line, the two late-arrival barks) for `miso-narrative`.

**Lucy's follow-up is never the only way a ★ kills.** It isn't previewed (no skull), so every ★ above kills by previewed hits alone; a follow-up that lands first is a bonus the player discovers.

---

## USP check

- **Family Roles:** strengthened, as built. Each pick's role holds one front: John's guard covers a sister, Mark's counter pays only when he holds a side (and per called Claw on the tracks), Watch is both the trap and the reward on the tracks, Lucy's follow-up radius decides where she stands. No level needs a new role rule; "kept AP" makes every level harder (lever: Claws ×0.8).
- **Synergies:** kept. Papa's Shelter and Shield Flare answer the River, Catch & Return the Ridge; the Pile's layout keeps Mark's catch from eating Linda's key shot.
- **Duos:** strengthened. The movement Duos (John–Linda Dance, Mark–Linda Footrace) get their first ★ (the Blood's reach); Chained Assault becomes a choice of targets and timing (cooldown 2), not a wipe. The sisters' Duo stays locked (D-470).
- **Managing the Home as a Family:** neutral on purpose. HP carried through M2 gives the Home visit after it a little more weight, nothing more.

---

## Critics

Three independent critics, run 2026-11-11 as read-only Explore agents told to follow `.claude/agents/miso-design-critic.md` (the `miso-design-critic` agent type isn't available in this session). Each saw the draft and the evidence, not the others' output. All three: **ship with changes**.

### Systems critic

| Objection | Response | What changed |
|---|---|---|
| **Strongest:** Lucy's follow-up is 6 (two sidewinders at 3), not 4; the draft took 4 from log lines capped by the target's HP. At 13 HP every pick kills with one action + follow-up (14). Chained Assault reaches 5, not "radial 4" | Right. I checked: every follow-up and ember line in the logs is capped; `radiusV` is 5 in the Duo asset | Claws ×1.0 (16), Archers ×0.5 (12); all walkthroughs redone with 6 and 4/3; Duo reach 5 in every distance; the Trailhead now works without a perfect solve |
| Tracks' west corner is a fortress (single-file entry into Watch's lane); 3,2 is a gap (no "Mark on 3,2"); 4,4 is a dead end | Right | The late pair moved to the north bank (1,4, 2,4), inside the corner's reach; the far-bank 8,4 Claw cut; no unit placed on a gap |
| Blood: sprinting wins on turn 2, before the wave acts; kill-all can fire before hidden units exist | Right | The trail is now 20 long (17 to 18 steps), three gullies, two chokes: three turns of moving minimum; the late pair is on the trail by turn 2. Kill-all stays (it prevents a lock) and is out of reach on turn 1 at 16 HP |
| Wave timing: bring it in so it acts on enemy turn 1 | **Disagree** (the UX critic's fairness point wins) | Late arrivals appear at the start of turn 2 and act on enemy turn 2; the longer trail does the systems job instead |
| Trailhead still breaks D-505 (move the front pair to 10,1 / 11,0) | Right on the problem; the HP fix solves it without moving them | At 16 HP neither side dies to one hero: Lucy's fire goes one way, something always lands |
| Pile: the Duo from 3,4 plus Watch decides it; move 0,2 to 1,0; Lucy's start is in the Archer's reach | Right | West Claw now 1,0 (6 from 3,4: out of the Duo); the start row changed so the Archer's reach and Linda's lane are both by layout |
| The arrow budget ignores pickups; only island shots really cost | Right | Rule 5 rewritten: a shot at a perch is the cost |

### UX critic

| Objection | Response | What changed |
|---|---|---|
| **Strongest:** the key trades are decided blind; the Tracks turn-1 arrow choice is punished by a wave nobody announced; the Pile's 6,3 cost comes from hidden enemies; the Blood's gully-head wave feels like the old rear wave | Mostly right | Rule 3: late arrivals appear at the start of turn 2 with a camera move and a bark, a full player turn before they act, never next to the start tiles. The Tracks' real arrow choice is now turn 2, after the arrival is on screen. **Kept blind on purpose:** the Pile's ambush (the story beat), with the decision moved to the turn after the reveal, which is fully readable |
| Lucy's follow-up is the lethal part of two ★s and isn't previewed: the skull says "not lethal" | Right | Archers at 12: every ★ kills with previewed hits (two arrows, skull on the second); the follow-up is a bonus |
| Mark's catch silently eats Linda's Pile shot | Right | Layout fix: the pick's slot is 5,4; Linda's row-5 lane is empty by design |
| The Blood goal will be read as defeat-all | Right | The line itself carries "Two of you, to its end."; the kill-all fallback is hidden; the opening camera shows the end tiles |
| Wave camera beats don't exist for Claws (EN-10 is for new types only) | Right | Each arrival is a stage onComplete sequence (camera + bark + reveal), the Pile's own pattern; to check that a "turn 2 reached" stage completes at the start of the family's turn |
| (Also suggested: make the Pile's Archer visible from the start) | **Rejected:** a visible Archer turns the quiet search into a fight before it starts (THJ: low tempo on purpose) | — |

### Creative critic

| Objection | Response | What changed |
|---|---|---|
| **Strongest:** every level is still one ★ plus a trap; D-505 asks for a cost the player chooses; only the Pile had two defensible plays | Right, and the sharpest point of the round | Acceptance criterion rewritten (two good plays, different currencies); every level now has ★ A and ★ B with what each pays |
| Trailhead fails by its own admission (add the Archer) | Right on the problem | Solved by the HP fix instead (one less unit): Lucy's fire can only serve one side |
| Tracks: hiding west is free, and Encore's cue goes silent | Right | The north-bank pair (same fix as systems); Encore's cue moves to "an Archer dead", where its arrows now lie on the island |
| The give-up is felt only as an HP number; add a family bark on each give-up | Partly. A bark on "the uncovered sister is hit" is new tech (a hit-reaction trigger), outside the budget | Barks kept where a sequence already fires (the Trailhead's opening, each late arrival); hit-reaction barks noted for `miso-narrative` as a later idea, not in this plan |
| The Pile risks its own ending (loss replays the Trail; last kill far from the sisters) | Right | 10,0 Claw removed now; the east (Archer and one Claw) is built to fall first so the last enemy is usually west, at the sisters; outro staging to check |
| 13 HP will read as "more HP" | Right on the framing | The threshold is now the tier's own value (the override removed), and it's said that way to THJ (Q1) |

**What changed my mind most:** the systems critic's numbers (the threshold was wrong) and the creative critic's "one ★ plus a trap". **What I rejected:** waves that act on the turn they appear (systems), a visible Pile Archer (UX), new hit-reaction barks (creative).

---

## Paper turn: the Trailhead, Mark picked (the check behind ★ A)

Mark Blitz 1,0: 8, follow-up 6 (Lucy on 3,1 is 3 away): 14 of 16. Second Blitz: dead, Mark steps to 1,0; Continuous Attack (1 FTP) on 0,1 (2 away): 8 + follow-up 6: 14. Lucy's main ember: 0,1 dead. Linda: Explosive on 8,1 (8 and 8), bow on 8,1 (6): 8,1 at 2, 9,1 at 8, quiver 1. Enemy turn: 9,1 ends in row 1, Watch: 6, to 2; 8,1 and 9,1 hit Linda: 8. Board after round 1: two Claws at 2 HP, Linda 12/20. Round 2 clears. Nothing in this line is a trap; it is the "rear first" answer, paid in Linda's HP.

---

## Questions for THJ

**Answered by THJ, 2026-11-11 (revision 2).** Q1 and Q5 → D-507 (either HP approach; existing enemy types allowed: used here as Claws ×1.0 on three levels, ×0.8 plus a Black Claw on the tracks). Q2 → D-508 (as proposed). Q3 → D-509 (as proposed). Q4 → D-510 (the tracks redesigned without Archers; Encore's cue stage goes).

**No new questions.** The new *Follow the tracks* uses the latitude D-507 gave (one existing enemy type, one rule to learn, data only); THJ's look at it is the only open item. The original questions are kept below as history.

**Q1. M2's enemy HP: the tier's own value (Claws 16, Archers 12)?**
- Context: at ×0.6 (10 HP) any one action, or one action plus Lucy's free follow-up, kills a Claw, so no layout survives the first turn. At 16, the best single action plus a follow-up (14) never kills; two actions do. This removes an override rather than adding HP: Early tier is ×1.0.
- Options: (a) Claws ×1.0, Archers ×0.5; (b) Claws ×0.8 (13) and more Claws per level (longer fights, and a Blitz + follow-up still kills); (c) keep ×0.6 and rely on layout (the logs say the first turn still wins).
- Recommendation: (a).
- Blocked: every walkthrough's numbers; the M2 wiring values.

**Q2. *Follow the blood* becomes a reach level: "two of you, to its end", with kill-all as a hidden fallback?**
- Context: the only route where winning isn't killing. It gives the movement Duos (Dance, Footrace) their first ★ and makes every turn a fight-or-move choice. "Two" keeps a fallen hero from locking the level and stops a lone runner.
- Options: (a) reach, two of you; (b) reach, any one (faster, a lone runner can win hurt); (c) keep defeat-all with late arrivals only.
- Recommendation: (a).
- Blocked: the Blood grid and its objective wiring.

**Q3. Late arrivals: two Claws revealed at the start of turn 2 on the tracks and the blood route, announced by a camera move and a bark?**
- Context: you disliked the old rear wave (it appeared on the family's start tiles, unseen). These appear a full player turn before they act, from a side the camera shows, never next to the start tiles. Built as hidden groups revealed by a "turn 2 reached" stage, the Pile's pattern (no runtime code; to check the stage completes at the start of your turn).
- Options: (a) yes, as described; (b) on the board from the start, out of reach (no surprise; the maps grow); (c) no arrivals (the levels lose their second demand on turn 2).
- Recommendation: (a).
- Blocked: the Tracks and Blood wiring.

**Q4. Encore's cue on the tracks: "an Archer dead" instead of "both Archers dead"?**
- Context: a player may now leave one Archer alive on purpose (★ B), and the cue would never play. With perch arrows out of reach, the first dead Archer is exactly when Encore pays.
- Options: (a) move the cue; (b) keep it on both dead.
- Recommendation: (a).
- Blocked: the Tracks stage wiring.

**Q5 (information; no decision needed now). A new enemy in M2?**
- Context: a Black Claw (hit it and its pack turns on the hitter) or a Dark Shaman (heals its kind) would counter the volley directly, at the cost of one more rule to learn in the first hour.
- Options: (a) not now: try B first; (b) a Black Claw on the tracks route; (c) a Shaman at the Pile.
- Recommendation: (a). Revisit only if THJ's timed run still says "no challenge".
- Blocked: nothing.

---

## Docs to update

If approved:

- **GDD** `design/gdd/missions-structure.md`: the M2 rows (Trailhead front and back; the tracks with a Black Claw ×0.5, Claws ×0.8 and two late Claws; *Follow the blood* won by reaching its end, two of you; the Pile with four Claws; Claws ×1.0 elsewhere; no Archers in M2; late arrivals as revealed groups); MI-27's table unchanged (M2 stays all alert). No rule ID changes; status "Built, differs" on the M2 rows until the rebuild lands.
- **GDD** `design/gdd/combat-rules.md`: none (no rule changes). `characters/lucy.md`: correct nothing in the rule text, but the follow-up damage (6) and ember values (4 main, 3 side) should be stated in plain numbers where the role row says "3 × damage", as the logs misled this round.
- `design/level-chunks.md`: pattern knobs **"Two demands"** (two fronts, two good answers in different currencies), **"Kill price"** (one action + Lucy's follow-up must not kill), **"Late arrivals"** (revealed at the start of the family's turn, act a turn later, never by the start tiles); the Duo's reach 5 in the coverage notes; the tracks level as a worked example of chunk 18 ("the bell as a shield") with roles as built; to-check rows below.
- `plans/onboarding/2026-11-09-onboarding-after-hearth-design.md`: mark the M2 section and the `after-river` / `after-ridge` blocks superseded by this plan (keep them for history; no two live blocks with one id).
- `plans/onboarding/2026-11-11-m2-trail-levels-tech.md` (coordinator): a C3 for the rebuild (blocks, wiring: Claw HP override removed except the tracks ×0.8, the Black Claw ×0.5, hidden groups and "turn 2 reached" stages with camera and bark, the Blood objective with `AtLeast 2` and a hidden kill-all, the tracks' Archer stage and Encore cue removed, the Pile's Archer and 10,0 removed, 10,1 added, slot 5,4; tests).
- `plans/onboarding/onboarding-narrative-draft.md` (`miso-narrative`): the Trailhead bark, the Black Claw's intro line and the pick's "That big one leads them." bark, the Blood objective line, the two arrival barks, the Blood end clue line.
- `decisions.md` (coordinator): done (D-507 to D-510).

### To check before building (each decides a tile or a number)

1. A "turn 2 reached" stage completes at the start of the family's turn 2, before input, so the reveal's camera and bark play then (Tracks, Blood).
2. A reveal on a tile that is occupied (by a unit or a Cyclone) at reveal time: skip, shift or fail (Tracks 9,3 / 9,1; Blood 4,4 / 14,4).
8. The Black Claw's damage at Early (its attack effect reads the stat; the value isn't in the GDD) and that its call reaches revealed units that appear after the hit only if the leader is hit again (EN-1 calls at the moment of the hit).
9. Whether a revealed or called Claw that is taunted walks through Linda's lanes as the paper assumes (AI pathing with `ignoreRelationOnWalk` = Ally).
3. Lucy's follow-up and ember damage in play, uncapped (the logs only show capped hits): 6 and 4/3 assumed from the presets.
4. Vault over units onto the trail past a 1-tile choke (Blood).
5. A Cyclone in a 1-tile choke stops Claws from following (Blood ★ A).
6. The objectives panel can hide one objective of a group (Blood's kill-all fallback).
7. Claw move 4 (no move longer than 3 shows in the logs; every logged move ended beside its target).

## Risks

- **Paper against AI.** Arrivals and targets are the AI's choice; every level has a lever and a to-check row.
- **The Pile at the peak.** A cold player losing it replays M2; the 10,0 Claw and the Archer are out; next levers: the 10,1 Claw out, then one west Claw.
- **The bell's reflex press.** Watch or Lucy's follow-up on the Black Claw rings it without the player choosing; declining is possible (FR-2) but fast. Watched in THJ's run; lever in the tracks table.
- **Time.** M2 about 11.5 minutes at THJ's pace (Trailhead 2, tracks 4 or blood 4, Pile 4.5, picks and map 1); lever: the Tracks late pair to one Claw.
- **Family Roles outcome.** Kept AP makes every level harder; the Claw factor is the one lever.
- **`AIRegressionTest`** may shift with new levels: stays known red, never re-baselined.

## Gates

Design only. If approved: the coordinator's tech plan (C3 on the M2 plan), implementer (editor code, data, tests; EditMode known red only), reviewer, then THJ's timed play of M2 with each pick (needs THJ's time: yes), then the cold run. Grids to render and check: `m2-trailhead`, `m2-tracks`, `m2-blood`, `m2-pile`, `after-river`, `after-ridge`, all in this plan.
