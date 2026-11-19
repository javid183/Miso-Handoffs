# Lucy's Cyclone: reset to the original problems, then one fun layer (design)

Size: L    Tier: 3 (resets approved rules LU-3 to LU-7; THJ's areas: rules a player sees, game feel)    Assigned to: miso-game-designer
Branch: `thj/cyclone` (until it merges; `main` still has the drifting Cyclone)
Status: waiting on THJ

## Why

THJ played rounds 1 to 3 on `thj/cyclone` on 2026-11-19 and stopped the play check: **the rules have lost their simplicity, and a player can't tell what a move will do** ([`playtests/2026-11-18-cyclone-round3-play-check.md`](../playtests/2026-11-18-cyclone-round3-play-check.md) › THJ's play feedback, 2026-11-19; screenshots `playtests/img/2026-11-19-cyclone-1/2/3`). His direction: "Jump back to the original questions which caused the cyclone redesign. Start anew: first solve the original problems only, then add fun things with a more minimal approach." He proposes the fun layer himself: the Steer runs through enemies.

## Goal

The smallest Cyclone that fixes the four original hidden rules, plus one fun layer (THJ's run-through Steer). Lucy's tooltip fits in about three short sentences, and a player can predict every outcome from the board before acting.

## Acceptance criteria (for the design, once approved)

- [ ] Each core rule names the original problem it solves; nothing else is core.
- [ ] One-breath test: the Cyclone and the Steer each read in two or three short sentences, with no rider re-counting, no turning path and no per-step order.
- [ ] Every enemy a Steer touches takes the same, single hit, and where every unit ends up follows from the board and one fixed rule.
- [ ] Screenshot 2's "no Steer at all" can only happen when terrain closes all four lines.
- [ ] No new on-screen element. The preview pieces that already exist are reused, and the carry's are removed.

## Scope

In: the original problems; the core rule set; THJ's Steer proposal, its landing push and its fallback; the readings of "only drag those against the direction of the pull"; a keep or drop verdict on every built rule (rounds 1 to 3); questions.
Out: the tech plan (coordinator), with only high-level remove or switch-off notes here; numbers beyond start values; level chunk grids (none changed); final texts (`miso-narrative`); the AI regression baseline.

## Touches

Systems: Cyclone (`CycloneCarryPlanner`, `CycloneSteerRules`, `CycloneSteerSteps`, `CycloneSteerPreview`, `CycloneRules.CastOnEnemy`, `AEffectCycloneSteer`, `CycloneWobble`, `CycloneWindMotion` / `CycloneUnitDrawings` presenters, `CycloneHitContext`). Core systems: none need changing. The approved core hooks (CR-57, CR-58, the heavy pass, D-571) stay as built under the recommendation, and get removed only if THJ picks Q5 (b).
USPs: Family Roles (Watch), Synergies (Tempest Bloom, bunching).
Docs: GDD `characters/lucy.md` LU-3 to LU-7, `combat-rules.md` CR-58 (only if Q5 b), `enemies.md` EN-3 (rider wording), EN-18 (wobble mention); `design/cyclone-redesign.md` (a reset note); `glossary.md` ("carries" retired; narrative).

## Approach

### 1. Problem and evidence

**The original problems** (the redesign's §1 and §2, D-055, Q21, S10), one line each:

| # | Problem | Kind |
| --- | --- | --- |
| P1 | It moved on its own at the start of **every** faction's turn, not once a round (`TurnGeneralTick` listens to every faction's turn start) | Code accident |
| P2 | It chose its targets by hidden scoring (+10 / +20), skipped enemies already inside it, and **wandered to a random cell** when it found no candidate | Hidden rule, partly a bug |
| P3 | Damage came at two unclear moments (a hit on the landing cell, plus contact on the way). Q21: "damage at the start of its turn" (D-530 read this as a complaint about the old Cyclone) | Hidden rule |
| P4 | Its life drained about 3 pips a round (one on Lucy's phase plus one on every faction's turn start), so it lasted about 1.7 rounds against the 5 shown (D-055) | Code accident |
| P5 | When its target cell already held a planted entity, it **slid to the nearest free cell**; it blocked everyone except units already inside it | Hidden rule (side effect of P2) |
| S10 | "Improve its movement and prototype a pull towards the centre" | Request |

**The symptom now:** three screenshots.
1. **A row of four Claws** (screenshot 1). THJ wants to steer through the row and break it. The built Steer stops at the first Claw: a front enemy is shoved and can't go anywhere (LU-6 step 1).
2. **No Steer offered** (screenshot 2). The Cyclone sits in a corner, with a Claw above it, another Claw behind that one, and family members close by. Read from the image (not verified in play): up is refused because the front Claw has nowhere to go; left and down look off the board; right, every cell is either family (the Steer crosses family but can't end there) or not a legal end. Any one of these refusals is plausible under LU-6, and that is the point: the player can't tell which one applies.
3. **No idea what a move does** (screenshot 3). One Claw is beside the Cyclone and one sits diagonally. Moving right drags the side Claw into the diagonal one, so it drops out. The diagonal Claw then becomes a rider for the next step. Every direction gives a different reshuffle.

**The root problem.** The original problems were all fixed in round 1 (anchored, Whirl, 3 pips, empty-cell cast). What broke predictability came later: the **carry** (round 2). It makes the board depend on the path: riders are re-counted each step, side riders drop out, and a rear rider follows. Then come the **turning path and detours** (D-553) that the carry needed, and the planner searches up to 36 paths to find them. Round 3 put more motion on top (grab, drag, fling) and a second shove rule (cast). THJ's three screenshots all trace back to the carry and its "front enemy blocks the step" rule. The Whirl is not the problem, and neither is the cast or the lifetime.

### 2. The core rule set (solves P1 to P5 and S10, nothing else)

> **Cyclone:** "Summons a Cyclone on an empty cell for 3 rounds. When summoned, and after each enemy turn, it Whirls: enemies in its lines are pulled one cell in, then every enemy beside it is hit. It moves only when Lucy Steers it."
> **Steer (core):** "Moves the Cyclone up to 3 cells in a straight line. Then it Whirls."

| Core rule | Solves | Built today? |
| --- | --- | --- |
| **K1.** It never moves on its own and never picks a target | P1, P2 | Yes (LU-3) |
| **K2.** Cast: 1 AP, an **empty** cell within 3 (no unit, no planted entity), cooldown 4 | P5 (no slide, nobody inside) | Yes (LU-3, before round 3) |
| **K3.** Life: 3 pips, one lost at the start of each family turn, shown on it | P4 | Yes (LU-3) |
| **K4.** **Whirl** is the only kind of Cyclone hit: pull enemies on the arms (2 out, straight) one cell in, then hit every enemy beside it. It happens at named moments only: on cast, after a Steer, at the end of each enemy turn | P3, S10 (the pull) | Yes (LU-4) |
| **K5.** **Steer:** 1 AP, once a turn, up to 3 cells **in a straight line**, ending on an empty cell. It crosses the family; walls, walk-blocking planted entities and (core only) enemies stop it. Then a Whirl | S10 (movement is Lucy's choice), P1 | Partly: built with turns and the carry |

The Steer's closing Whirl hits, as decided in D-547. The cast Whirl is kept because the cast is the moment Lucy acts (principle 1, "every hit has one named moment"), and the cast preview already draws it.

**Not core, judged in §4:** everything about what the Cyclone blocks (CR-57, CR-58, heavies and the burst, EN-18 and EN-19), the carry, the cast on an enemy, the beats. None of them solves P1 to P5. The Cyclone has to say what happens when someone walks into its cell, but "nobody inside" already follows from K2 and K5. Which units it stops is a role question (principle 4), not one of the original problems.

**Why the core alone isn't the plan.** The core Steer is round 1's Steer, and THJ already found that one not fun ([`playtests/2026-11-12-cyclone-play-check.md`](../playtests/2026-11-12-cyclone-play-check.md), notes 5, 10, 11: "steering should be super fun"; "steering it through enemies pushes them away"). His note 11 from round 1 is the same idea as today's proposal. So the core is the base, and the fun layer below ships with it.

### 3. The first fun layer: THJ's run-through Steer

#### 3.1 Options compared

| | A. Core only | **B. Run-through Steer (leaning)** | C. Keep the built carry, straight line only |
| --- | --- | --- | --- |
| Rule | Enemies stop the Steer | The Steer glides **through** enemies, hitting each. An enemy on the cell where it stops is knocked off. Then the Whirl | Front shoved, sides dragged, rear follows, but no turns |
| Player experience | Round 1's flat Steer (THJ: not fun) | Screenshot 1's fantasy: roll through a pack, scatter its head, the Whirl bunches the rest | Still a per-step shuffle of up to 4 riders. Screenshot 3 stays unreadable |
| Rules for the player | Lowest | One sentence, plus one fixed landing rule | Three roles and a re-count each step |
| Build | Small (remove the carry) | Medium: the planner becomes a straight scan, plus the pass hits, the landing knock and its preview | Small (clamp the path) |
| Risk | Underwhelming again | Pass damage against Embers (§5); the landing fallback's readability (Q2) | THJ's complaint stays |
| USP | Neutral | Strengthens Watch (the knocked enemy lands once, Whirl pulls land too) | As built |

#### 3.2 The B rules

> **Steer:** "Glide the Cyclone up to 3 cells in a line, through enemies, hitting each. An enemy where it stops is knocked onward. Then it Whirls." (Working text; narrative does the final words.)

1. **Line.** Up to 3 cells in one straight direction (four-way). The path never turns. Walls (no cell), the map edge and planted entities that block walking stop the line at the cell before them.
2. **Through.** The Steer passes through every unit in the line. The family and allies: nothing happens. **Enemies, heavies included: each takes the Cyclone's hit as the Cyclone enters its cell.** A passed enemy doesn't move, so its passing starts no reaction (no Watch, no hazard).
3. **Where it can stop:** an empty cell (no unit, nothing planted, as K2), or a cell held by an enemy it can knock: one cell in size and not Immovable (the pull's filter, EN-3), with nothing planted on the cell. It can't stop on the family, an ally, a heavy or a planted entity.
4. **Knock.** The enemy on the stopping cell is knocked **one cell onward**, in the Steer's direction. If that cell isn't free, see Q2 (the fallback). If no allowed cell is free, the stopping cell isn't offered (cells before it and past it in the line still are). The knock happens once: a hazard on the landing cell fires, Family Roles answer it (Watch), and it wakes the enemy. It does no damage of its own: no Crippled damage, the same as today's Cyclone moves (LU-4).
5. **Then the Whirl** (K4, unchanged): pull, reactions, hit.
6. **One hit per enemy per Steer** (Q4). An enemy already hit while the Steer passed isn't hit again by its Whirl. Put another way: **every enemy the Steer passes through or leaves beside it takes one hit.** The knocked enemy wasn't passed, so it takes its hit in the Whirl.
7. **Planned before it moves.** The whole outcome is worked out on the board as it stands at the click. A passed enemy that dies doesn't change the landing (systems critic).

The **cast on an enemy** (round 3, D-566) uses the same landing rule: "onward" is away from Lucy along the larger axis, and along the row at her diagonal neighbours (Q6).

**Screenshot checks:**
- **Screenshot 1:** from the Cyclone's cell, the line east crosses the torch's cell (if its entity doesn't block walking; not checked) and the empty cell, then reaches the first Claw. Its next cell holds a Claw, so onward is blocked. Under Q2 (a), the first Claw is knocked to the row below, the Whirl hits it and the second Claw, and the row is broken. Under Q2 (b), the Claw's cell isn't offered and the Steer stops on the empty cell before it.
- **Screenshot 2:** the line up passes the two Claws (both hit) to the empty cell beyond, or stops on the second Claw and knocks it on. **"Can't be steered" goes away.** The Steer is now refused in a direction only by terrain, the map edge, or a line holding nothing but family, heavies and planted cells. No Steer at all needs all four lines closed that way.
- **Screenshot 3:** moving right (or any way) shows a single result: the line, the passed enemies hit, at most one enemy knocked, and the Whirl's pulls from the new lines. Nothing rides.

#### 3.3 "Only drag those against the direction of the pull": readings

| Reading | Rule | Fits "runs through"? | Predictable? |
| --- | --- | --- | --- |
| R1. Wake drag | The enemy right **behind** the Cyclone when it sets off follows it and lands on the cell behind where it stops | Yes | One unit, but its landing cell often holds a passed enemy (a second "blocked" case) |
| R2. Shove ahead | Enemies **ahead** in the line are pushed along instead of passed | No: it replaces "through" | Bulldozer, so the round 2 blocked-front problem comes back |
| R3. Axis Whirl | The Steer's closing Whirl pulls only along the line it moved, not from the side arms | Yes | Two kinds of Whirl to learn |
| **R4. No drag (leaning)** | Nothing rides. The Whirl's pull at the new spot is the only drag | Yes | Zero new rules |

**Leaning: R4**, with R1 as the named lever if THJ misses the dragging after playing B. All three critics independently chose R4 (Q3).

### 4. Strip list: every built rule, keep or drop

"Remove" means built code goes. "Switch off" means data or a branch in code is enough. Both are high-level guesses for the tech plan to confirm.

| Built rule (source) | Verdict | Why | Code, high level |
| --- | --- | --- | --- |
| Anchored, never moves on its own; one Cyclone (LU-3) | **Keep, core** (K1) | P1, P2 | None |
| 3 pips, one per family turn (LU-3) | **Keep, core** (K3) | P4 | None |
| Cast on an empty cell within 3, cooldown 4 (LU-3) | **Keep, core** (K2) | P5 | None |
| Whirl: pull 1 from 2 out, then hit beside; on cast, after a Steer, at the end of each enemy turn; Immovable and large not pulled (LU-4) | **Keep, core** (K4) | P3, S10 | None |
| No Cyclone hit is anyone's action; credit, Howling Gale, waking (LU-5) | **Keep** (fun layer: pass hits join it) | Already one rule, and the pass hit is a Cyclone hit | Pass hits go through the same hit report |
| Steer 1 AP once a turn, reach 3, then a Whirl (LU-6, D-547) | **Keep, core** (K5) | S10 | None |
| **The path may turn** (LU-6) and **detours past a blocked front** (D-553) | **Drop** | Unpredictable routes, made necessary by the carry | Remove: the planner's breadth-first search over every simple path (`CycloneSteerRules.Search`) becomes a 4-line straight scan |
| **The carry:** front shoved, sides dragged, rear follows, riders re-counted per step (LU-6 steps 1 to 3, D-548, D-549) | **Drop** | The source of screenshots 1 to 3 | Remove: side and rear moves and rider re-counting in `CycloneCarryPlanner`, the carry execution in `CycloneSteerSteps`, "carried N" in the log. The single front-shove move (`Shove`) is reused for the knock |
| "A front enemy that can't be shoved blocks the step" (LU-6 step 1) | **Drop** | The Steer passes through instead | Replaced by the pass rule |
| Steer crosses the family and non-blocking hazards; walls and blocking planted entities stop it (LU-6) | **Keep, core** | Terrain is readable | None |
| Steer ends only on an empty cell (LU-6) | **Keep, core**, extended by the knock (fun layer) | P5 | `CanEnd` accepts a knockable enemy cell |
| Aim preview: landing Cyclone and cross, a ghost and tether per moved enemy, damage and skull on ghosts, hazard ring, reachable cells only (LU-3, LU-6) | **Keep**, simpler | Fewer ghosts: at most one knocked enemy plus the pulls | The preview reads the new plan; damage segments go on passed enemies too |
| **Cast on an enemy**, knocked away from Lucy (round 3, D-566); allowed next to Lucy (D-567) | **Keep (fun layer)**, under the shared landing rule (Q6) | The same sentence as the Steer's knock; THJ asked for it; built | Its shove switches to the shared knock (and the fallback if Q2 a) |
| Whirl inhale and exhale before the hit, with the input lock (round 3, D-568, D-569) | **Keep** | It marks the hit moment (principle 1); presentation only; THJ asked for it | None |
| Grab and drag beats of riders (round 3) | **Drop** with the carry | No riders | Remove the rider lean and lag paths; keep the fling for the knock |
| Fling (round 3) | **Keep**, as the knock's motion | One mover | Reused |
| Enemies can't walk through it; the family passes and can't stop (CR-58, LU-7) | **Keep (role layer)** (Q5) | Not an original problem, but one sentence, built, and it holds enemies for the family (principle 4) | None |
| Enemy shots can't cross it (CR-57) | **Keep (role layer)** (Q5) | Same reasons | None |
| Heavies walk through and burst it (D-550, D-556, D-571, D-572; EN-2, EN-6) | **Keep (role layer)** (Q5) | THJ's round 1 note 9: otherwise the Masher is walled off. Enemy-side, one sentence | None |
| **Heavy warning wobble** (D-558, LU-7) | **Drop** | A warning that can be wrong: it reads the path to the nearest family member, not the AI's plan. A signal that sometimes lies hurts prediction more than no signal | Remove `CycloneWobble` (Cyclone-only code, no core) |
| Enemies avoid ending on the cross (EN-18); ranged firing spots (EN-19) | **Keep** (AI, invisible) | The player never computes it. Lever: EN-18 empties the cross, which round 2 named as a reason it felt weak | None |
| Super Time on empty cells, skipped while it's out (D-535); never a Steer for AI-controlled Lucy (D-540) | **Keep** | Unchanged | None |
| Cross drawing: swirl tint on touching cells, chevrons on arm tips (round 2) | **Keep** | It shows the Whirl's reach | None |

**Net for the player:** removed: the carry (three roles), re-counting, the turning path, detours, the "blocked front" refusal, the wobble. Added: "through enemies, hitting each" and "an enemy where it stops is knocked onward".

### 5. Lens notes (B with R4)

**Creative.** *Target:* Lucy sends her storm through the pack. It bowls through the line, knocks the last foe out of its place, and then breathes in the rest for the family. A small girl breaking a formation that the adults then finish off. *The moment:* the screenshot 1 row. Lucy Steers through the head of the line, the first Claw is knocked out of formation into Linda's row, and Watch fires. The Whirl pulls the next Claw in and hits both. The creative critic's strongest point: make the result serve the family (Linda's lane), not just the damage tally. The knock is where that happens: one enemy, a predictable cell, landing in Linda's lane. Presentation note (THJ's area, first pass of a new beat): the pass hits land one after another down the line as the Cyclone enters each cell, so a single hit reads as a sweep. The critic asked for this, and it adds no extra hits.

**Systems.**

*Levers and start values:*

| Lever | Start | Range / fallback |
| --- | --- | --- |
| Hit (pass and Whirl alike) | 3 × `Stat_DMG` (Cyclone Power 4 / 5) | Pass hit 1 × ("graze") if Steers out-damage Embers |
| Hits per enemy per Steer | 1 (Q4) | Uncapped (THJ's literal reading) |
| Steer reach | 3, straight | 2 |
| Knock | 1 cell; fallback per Q2 | — |
| Cast, life, arms, pull | 1 AP, range 3, cd 4; 3 pips; arms 2; pull 1 | Unchanged |

*Damage against Embers* (base: Embers about 7 for 1 AP, focused; Claw 16 HP). A B Steer hits each enemy it touches once, for 3: 2 enemies typical (6), 3 to 4 in a pack (9 to 12). The worst realistic case is 2 passed, 1 knocked and 2 already beside the stopping cell: 5 × 3 = 15, spread out, with no kill on a full-HP Claw. Uncapped, the enemy passed last also takes the Whirl, which adds 3 to 6. The systems critic warns that the Steer can out-damage Embers in packs, and that cast plus Steer every turn becomes the default line. The answer: the cap at the start, and the graze as the next lever. The Steer stays once a turn and the Cyclone lasts 3 rounds with cooldown 4. Its value should stay placement first. Playtest signal below.

*Interactions:*
- **Watch:** passed enemies don't move, so they start no Watch (no fishing down a line). The knocked enemy and the Whirl's pulls do. Still one answer per action (known core limit, round 2 open item 1).
- **Hazards:** a knock onto spikes or a pool fires them (a combo, as the pull is).
- **Crippled:** the knock pays none (the same as today's Cyclone moves; there is no per-cell effect on the move).
- **Burst:** a Steer passing through a heavy hits it and doesn't burst the Cyclone. The burst stays a heavy's own walk (LU-7).
- **Kills mid-pass:** the plan is fixed at the click, so a death changes nothing.
- **Tempest Bloom, line of fire, EN-18:** unchanged.

*Failure cases:* Steering through the same wall of Claws every turn (accepted: 1 AP for spread 3s, and the knock is what breaks the wall). Stranding: the knock is one cell, so it can't strand. Disengage by cast (D-567): unchanged, still a cut lever.

*Implementation (verified in code, read-only):* `CycloneCarryPlanner.Shove` already gives the one-unit knock with the planner's free-cell check. `CycloneSteerRules.Search` is the 4 × 3^(reach-1) search that a straight scan replaces. `CycloneCarryPlanner.CanEnd` is where "a knockable enemy cell" gets accepted. The one-hit set across the pass and the Whirl needs a per-Steer record that the Whirl reads (the systems critic suggests `CycloneHitContext`; assumed, not read).

**UX.**

| When | Shown |
| --- | --- |
| Steer picked | Range highlight on the cells it can stop on, in up to four straight lines. A Claw it passes through stays unlit while the cell beyond it lights, which reads as "through, not on" |
| Hover a cell | The line, the faint landing Cyclone and its cross (current cross dimmed), **one** damage segment per enemy that will be hit, passed or beside (on the ghost if it moves), the knocked enemy's ghost and tether, the pull ghosts, the hazard ring |
| Click | One click, as today |
| Steer resolves | The glide; hits pop down the line as it enters each enemy; the fling of the knocked enemy; then the Whirl's swell, pull, inhale, exhale and hit |

*Likeliest misread:* the knock's fallback direction, if Q2 (a). The ghost shows it, but a player can't call it from the board until they've seen it once or twice. The UX critic's strongest point. *Second:* reading a passed enemy as a blocker. The rook-line highlight answers it. The tooltip says "through enemies".
*Budget:* new on-screen elements: none. The carry's riders, tethers and wobble go. The UX critic proposed a "blocked" X mark on cells not offered. I didn't take it (a new element): with straight lines and pass-through, a cell not offered has its reason in plain sight (something stands right behind the enemy).

**Where the lenses disagree:** the landing fallback. THJ asked for "any free cell if the natural one isn't free", which is the only rule that breaks screenshot 1's row sideways. All three critics want onward-or-refuse (F1) for readability, which the complexity budget also favours. I lean to THJ's fallback, shortened to one sideways rule with no "back" (Q2 a). Only one unit is ever affected and its ghost shows it. F1 stays the switch if he is ever surprised by where a knocked enemy went.

### 6. USP check

- **Family Roles:** strengthened. The knocked enemy and the Whirl's pulls land once, in a cell the player chose, which is the Watch setup. Passing starts no reaction, so it can't be farmed. Lucy's follow-up is unchanged (it never answers a Cyclone hit).
- **Synergies:** kept. Tempest Bloom, Explosive Crescendo and Shield Flare get the Whirl's bunch, as before. Breaking a row also opens Linda's lanes.
- **Duos:** neutral on purpose.
- **Managing the Home:** neutral on purpose.

### 7. Critics

Three `miso-design-critic` agents, one lens each, in parallel, without seeing each other. The creative and UX critics worked from the brief only; the systems critic read the planner code.

| Critic | Strongest point | What I did |
| --- | --- | --- |
| Creative | The moment is the "bowling run", and B only half delivers it unless the result sets up Linda. Make one hit feel big by landing the pass hits in sequence. "Right of travel" handedness feels arbitrary: F1, or "back" only as a bounce. R4. Keep the heavies' drama, but give the burst a telegraph if the wobble goes | **Took** the sequenced pass hits (presentation), R4, the Linda framing (the knock is the setup). **Partly took** the fallback: dropped "back" from my order, kept one sideways rule (Q2). **Rejected** a new burst telegraph: a warning that can lie is worse than none. The burst is the enemy's move, seen when it happens |
| Systems | Pass damage can make the Steer beat Embers, and cast plus Steer every turn becomes the default. Price the pass (a graze) or exclude passed enemies from the Whirl. F1 over the decision tree. Define planted cells under an enemy as refused, fix the plan at the click (kills), no reactions on passing, no Crippled on the knock | **Took:** the exclusion (my cap, now Q4), the graze as the next lever, planted cells refused, the plan fixed at the click, no reactions on passing, no Crippled. **Fallback:** raised as Q2 with F1 as the alternative |
| UX | The landing fallback is a four-step tree the board can't show; ship F1. Cells not offered need a visible reason (an X mark). One damage segment per enemy. A rook-line highlight. A shorter tooltip; don't say "knocked aside" | **Took:** one segment per enemy, the rook highlight, "knocked onward" in the text, the shorter fallback. **Rejected** the X mark (a new element; the reason is on the board). **Fallback:** Q2 |

What changed my mind: "back" in the fallback order (all three called the tree too long, and back mostly hits a passed enemy anyway); passing must start no reactions; the plan has to be fixed at the click.

### 8. Recommendation

**Core K1 to K5 plus fun layer B with R4**, built together (the core alone is the Steer THJ already found unfun). Strip per §4: drop the carry, the turning path, the detours, the wobble and the rider beats. Keep the cast on an enemy under the shared knock, the Whirl breath, and the enemy-side rules.

**Start values:** hit 3 × (Cyclone Power 4 / 5) for passes and Whirls alike; one hit per enemy per Steer; Steer 1 AP, once a turn, 3 cells straight; knock 1 cell, onward, else to the Cyclone's right, else its left, else that cell isn't offered; cast 1 AP, range 3, cd 4; 3 pips; arms 2; pull 1.

**Playtest signals:**
- **Worked:** THJ predicts a Steer's result before hovering, including where the knocked enemy goes. He Steers through a group at least once a level and calls it fun. Screenshot 2's "no Steer" doesn't come back. A Steer feeds Watch or a hazard at least once, by his choice. No full-HP Claw dies to the Cyclone alone.
- **Failed:** "why did it go there?" on a knocked enemy (switch Q2 to F1, a data or branch switch); Steers chosen for damage over Embers every turn (pass hit becomes the 1 × graze); "it should drag them along" (add R1); refused cells read as "can't" (revisit the X mark idea, or F1's opposite, a back fallback).

## Questions for THJ

**Q1. Should the Cyclone reset to core K1 to K5, plus your run-through Steer (B), with the strip list in §4?** *Tier 3.*
- **Context:** the core fixes the original problems and is mostly built. B replaces the carry, and the path becomes a straight line. Removed: carry, turns, detours, wobble, rider beats.
- **Options:**
  - (a) Core + B, built together.
  - (b) Core only first, B after a play.
  - (c) B, but keep the turning path.
- **Recommendation:** (a). The core Steer alone is round 1's, which you found flat. A straight line is what makes B readable.
- **Blocked:** the tech plan and the GDD rewrite of LU-6.

**Q2. When the enemy on the stopping cell can't be knocked onward, where does it go?** *Tier 3. The same rule applies to the cast on an enemy (Q6).*
- **Context:** your proposal: any free cell. It has to be one fixed, drawable rule. All three critics prefer refusing the cell, for readability. Only (a) breaks screenshot 1's row sideways.
- **Options:**
  - (a) Onward; else to the Cyclone's right (as it travels), else its left; else the cell isn't offered.
  - (b) Onward, else the cell isn't offered (the round 3 cast rule).
  - (c) Onward, else back into the cell the Cyclone came through, else not offered.
  - (d) As (a), with "back" as a last resort.
- **Recommendation:** (a). It's your fantasy, only one unit is affected, and the ghost shows it. Switch to (b) the first time a knock surprises you. A screen-fixed side order instead of "the Cyclone's right" (up before down, left before right) is a Tier 2 detail if you prefer it.
- **Blocked:** the knock planner and preview.

**Q3. What did you mean by "only drag those against the direction of the pull"?** *Tier 3.*
- **Context:** §3.3.
- **Options:**
  - (a) R4: nothing rides; the Whirl's pull at the new spot is the only drag.
  - (b) R1: the enemy right behind the Cyclone follows it and lands behind its stopping cell.
  - (c) R2: enemies ahead are shoved along, not passed (this replaces "through").
  - (d) R3: the Steer's Whirl pulls only along the move line.
- **Recommendation:** (a) for the first play, (b) as the lever if you miss the drag. If you meant something else, a sentence is enough.
- **Blocked:** the final planner rules (B can be planned with (a) and (b) as a switch).

**Q4. Does an enemy the Steer passes through also take the closing Whirl's hit?** *Tier 3 (balance, readability).*
- **Context:** your words read as both (a pass hit, then the usual Whirl), so an enemy passed last, which ends beside the Cyclone, takes 6. One hit each makes the rule "every enemy it passes or ends beside takes one hit", gives one damage segment per enemy, and keeps a Steer near Embers.
- **Options:**
  - (a) One hit per enemy per Steer.
  - (b) Hits stack.
  - (c) Stack, but the pass is a 1 × graze.
- **Recommendation:** (a).
- **Blocked:** the hit planner and preview.

**Q5. Keep the enemy-side rules as built (enemies can't walk or shoot through it, the family passes, heavies walk through and burst it, AI avoids the cross), minus the heavy-warning wobble?** *Tier 3.*
- **Context:** none of them solves an original problem, but each is one sentence, built, invisible or enemy-side, and they hold enemies for the family. The wobble can warn wrongly (D-558).
- **Options:**
  - (a) Keep all; drop the wobble.
  - (b) Strip to "a rock that blocks everyone" (removes the per-faction pass, the heavy exception, the burst, D-538 / D-571 hooks; the Masher is walled off again, your round 1 note 9).
  - (c) Keep all, the wobble included.
- **Recommendation:** (a).
- **Blocked:** nothing in B. (b) would add core removals to the tech plan.

**Q6. Keep casting on an enemy (D-566, D-567), using the same knock as the Steer?** *Tier 3.*
- **Context:** the same sentence as the Steer's knock ("away from Lucy" is its onward), and built. It adds the diagonal tie (along the row).
- **Options:**
  - (a) Keep, under the Q2 rule.
  - (b) Back to empty cells only for this play.
- **Recommendation:** (a).
- **Blocked:** a small change to the cast's shove if Q2 is (a), (c) or (d).

## Docs to update if approved

- **GDD `characters/lucy.md`:** card sentence. LU-3 (cast on an enemy, written in for the first time, with the knock rule). LU-4 (unchanged, except the log line). LU-5 (pass hits are Cyclone hits). LU-6 rewritten: straight line, through, stopping cells, knock, one hit per Steer; carry, turns, detours, the 1-Watch note for riders removed. LU-7 (wobble removed). Value table (Steer row, beats). Status lines and Source.
- **`enemies.md`:** EN-3 (no "carried"; knocked by a Steer or cast landing), EN-18 (wobble mention removed).
- **`combat-rules.md`:** CR-58 only if Q5 (b).
- **`design/cyclone-redesign.md`:** a reset note at the top linking here, superseding the round 2 carry and the round 3 drag beats.
- **`glossary.md` (narrative):** "carries" retired, "knock" proposed.
- **Texts (narrative):** Cyclone and Steer descriptions (working text in §2 and §3.2).
- **Level chunks 1, 12, 13, 24:** text only, if they say "drags"; no grids change.

## Risks

- **The fallback reads as random** (Q2 a): a switch to (b) is ready, and the playtest signal says when.
- **Pass damage creep:** the one-hit cap at the start, the graze as the next lever. Change one lever per play.
- **Preview trust:** one planner for the range, the preview and the execution (the round 2 pattern), with a test that compares them.
- **Removal churn:** the carry code has tests and a presenter. The tech plan should remove it in one chunk, not leave it dead behind a flag.

## Gates

Design only: THJ answers Q1 to Q6 → tech plan (coordinator) → build → compile, tests, review → THJ play check (needs his time: yes) → docs above.
