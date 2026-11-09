# Family Roles: give the player the decision

Size: L    Tier: 3 (the rule of a main mechanic and a USP; core controller and settings for the prototype)    Assigned to: miso-game-designer
Branch: all. The prototype is a dev switch built on `thj/onboarding` (THJ's working main, D-396). Its default is the game as built, so no branch changes until THJ flips it. Branch notes are in [Branches](#branches).
Status: waiting on THJ

## Why

THJ, 2026-11-09 (his words in the brief; also [`playtests/2026-11-09-pacing-check.md`](../playtests/2026-11-09-pacing-check.md), "Family Roles themselves"): Family Roles work, players love them, yet they feel wrong. There is no challenge, they're "just a click", "you never know what you did for it to work", and they are too much. ATB, FTP, capping Linda and removing the cost all failed to fix it, and FR has taken months of energy that should have gone to Synergies.

## Goal

Find the root problem, and recommend one direction with a test cheap enough to settle it in days, with a stop rule so FR stops eating the schedule either way.

## Acceptance criteria

- [ ] The root problem is stated apart from the symptoms, with evidence from the docs and the code.
- [ ] At least three real options are compared, including keeping FRs as they are and doing nothing, with an honest account of what each one loses.
- [ ] A paper test on real levels (3 scenarios, grid format) shows the player's decisions under today's rules and under the recommendation.
- [ ] The smallest playable prototype is specified as a dev switch, with the core files and Tier 3 items it touches and its rough size.
- [ ] What the recommendation means for how the Hearth introduces roles.
- [ ] Questions for THJ in the five-part format.

## Scope

In: the FR rule (when the player decides, what an answer costs), the prompt's role, the paper test, the prototype spec, the onboarding implications.
Out: per-role triggers and effects (unchanged), Linda's quiver (unchanged), Duo and Synergy rules (only where FR touches them), enemy AI (a later lever, not in the test), level rebuilds.

## Touches

Systems: Family Roles (core: `FactionRoleHandlerBase`, `FactionControllerBase`, `PlayerController`), settings (core: `GlobalSettingsSO`), role zones and role badge (UI, not core), combat log (additive).
USPs: Family Roles (main), Synergies (strengthened), Duos (cleaner FTP), Home (Fireside mapping only).
Docs: see [Docs to update](#docs-to-update-if-approved).

## Approach

Problem and evidence, then options, the three lenses, my own critic passes (agents couldn't be spawned here), the recommendation, a three-step test (paper, house-rule play, dev switch), and the onboarding note.

---

## Problem and evidence

### What a Family Role is today (as built and as designed)

Each Bergson has one reactive role. When its trigger fires, a 1 s "Activate Passive" prompt appears; pressing fires the role (FR-1, FR-2). Built: each answer costs 1 FTP from the shared pool, with no limit per round (FR-3, FR-4 "Built, differs"; `requiredFTP` 1, `oncePerPhase` 0; verified in `FactionControllerBase.ActivateFactionRoleIfFeasible`, which checks `PointConsumer.CanConsume(FactionRoleRequiredFTP)`). Designed: free, with a limit per round (D-036, D-042; unbuilt); Linda limited by her quiver instead (D-244). John shields a family member an enemy targets within 2 of him; Linda shoots an enemy that ends a move in her row or column within 4; Lucy follows up a family member's damaging action on an enemy within 3; Mark strikes an enemy within 2 that hit family ([Family systems](../design/gdd/family-systems.md#family-roles)).

### The root problem

**A Family Role pays off a plan the player never made.** The prompt is the only decision, and it always answers yes. Nothing on the player's own turn decides whether a role will fire: the trigger zones are the tiles each Bergson covers anyway, the enemies don't know the zones exist, and the price (FTP, later nothing) never makes the player choose between a role and something else. Roles happen *to* the player as a side effect of ordinary play.

That one cause explains all of THJ's symptoms at once:

| THJ's words | Why the root problem produces it |
|---|---|
| "Fun, everybody loved it" | A free reward with a real-time press, during a phase where you'd otherwise watch. Reward without effort is pleasant |
| "Just a click", "no challenge" | The press is the only input, and it has one right answer |
| "You never know what you did for it to work" | You didn't do anything: the setup was incidental, so there is nothing to connect the payoff to |
| "Doesn't feel like a tactics game" | Tactics is choosing under a trade-off. Roles involve none |
| "Too much" | Every Bergson answers every enemy turn, for free, and carries damage the levels then have to absorb |
| "FR killed the energy for Synergies" | Roles hand out the same pleasure as Synergies without the planning, so they compete with the system that *does* ask for a plan |

### Evidence (verified unless marked)

1. **Two of the four zones are not even drawn, because they add nothing.** FR-10 hides the selected Bergson's zone when it equals its basic-attack reach, "Today that hides Linda's and Lucy's". Lucy's role reach and ember reach are both 3 (levels plan, The River: "as soon as she can ember a Claw she is close enough to follow up"). Linda's lane is her bow's lane. So for half the family, standing where you'd attack anyway *is* the setup.
2. **Level design can't stop roles from firing, and plans around it.** Memory 3: "Layout can't prevent it, because a Claw that lands beside a sister is always in her row or column" (levels plan, John segment). Every paper level has a "First trigger" row showing the layout *forcing* the role ("near certain", opening plan; The Ridge: "1,5 runs to 1,1 and strikes Linda... a Watch shot first"). The design process itself treats roles as something that happens to the player.
3. **The enemies don't know the zones exist.** The AI scores destinations with utility variables (`Core/Systems/AISystem/UtilityScore/UtilityVariables.cs`: path cost, enemies along path, attractiveness, attack range...). There is no variable for a Bergson's role zone, so zones exert no board pressure: enemies walk in because they walk in, not because the player made the lane matter.
4. **The press is always yes.** A missed press costs nothing (FR-2), a declined one silences the target (D-063 called it "a decision, not a miss", but nothing makes declining worth it). The cost was 1 FTP from a pool that "fills on mission entry"; with D-036 it would be nothing.
5. **Roles carry the fights, so levels can't be hard without making roles mandatory.** Linda dealt 46–72% of damage "wherever she is", her role firing "3× in one enemy phase" ([`combat-balance.md`](../design/combat-balance.md)). The balance model assumes 2 reactions per hero per round, about 71 family damage per round against 32 from basic attacks alone. The pacing check, the same day as THJ's note: "Too easy... you do not feel the need of abilities" and "too many mechanics with too little challenge". Free reactions are part of why abilities feel unneeded.
6. **Running out was the only time roles meant anything, and it felt bad.** Playtests: "running out of FTP flattens combat". When the price finally bit, it bit as a shortage, not as a choice.

### The coordinator's hypothesis, tested

*"Every past fix changed how often a role fires; none changed when the player decides."* Mostly true, with two exceptions worth learning from:

| Past attempt | What it changed | When the player decides |
|---|---|---|
| ATB (D-036 dropped it) | The resource fills in real time and from leftover AP | Unchanged (the prompt). Also: confusing real-time fill |
| FTP, then free (D-036), then caps (D-039 to D-042) | Price and count | Unchanged |
| Capping Linda, then the quiver (D-241, D-244) | Linda's count, made spatial | Mostly unchanged for Watch: "the arrow count drops on the enemy's turn without the player choosing" (opening plan, fifth problem) |
| Readability (zones, cover icons, tether, barks; D-063 to D-091) | What the player sees | Unchanged: it made firing visible, not chosen |
| **Far Watch (D-266, dropped D-292)** | A bonus if no Bergson was within 2 of Linda at End Turn | **On the player's turn**, but as a positional sum to compute, not a choice to make. Dropped as "too complex" |
| **Bergson Time (key L, deferred D-038)** | Pause the enemy turn and act with ATB | **In the enemy turn**, with a real choice, but ATB-only and heavy |
| Aimed Watch (quiver plan option E, not taken) | Linda picks a lane at turn end | On the player's turn; rejected as "another click per turn" |

So the two times a decision moved, it came with a new calculation or a new step. The lesson for the fix: **move the decision to the player's turn, but make it out of something the player already does**, with no new number, no aim step, no extra click.

---

## Options compared

| | **A. Keep FRs as built; put the energy into Synergies** | **B. Finish the decided Pilot 1** (free, caps per round: D-036, D-042) | **C. Kept AP: roles answer with AP the Bergson kept (recommended)** | **D. Board control: enemies read the zones** | **E. A choice at the prompt** (one family answer per enemy turn; when several roles could fire, the paused prompt asks who) |
|---|---|---|---|---|---|
| The rule in one sentence | As now | "Each role answers up to N times a round, for free" | "**On the enemy's turn, a Family Role answers only with AP its Bergson kept: one answer per AP**" | "Enemies avoid (or fear) Bergsons' zones" | "The family answers once per enemy turn; you choose who" |
| When the player decides | The prompt (always yes) | The prompt (always yes) | **Their own turn**: spend this AP now, or keep it for the role, and stand where it matters | Their own turn: where to stand to deny tiles | The prompt, under a short timer |
| Player experience | Same fun; THJ's "wrong" stays | Less flattening (no FTP drain), Linda tamed; still a click | Roles become planned: "I kept Linda's AP, the Claw walked into her lane". The press stays as the celebration | Into the Breach pressure; roles fire much less, and mostly as denial | A real choice, but a hurried one, and the setup is still incidental |
| Rules for the player to track | None new | A count per role (FR-6 label) | **None new**: leftover AP exists and is lost today (CR-8, D-206) | Enemy behaviour around zones (hidden rules) | A choice screen and a family-wide limit |
| On-screen elements | None | One (uses-left pips) | **None new**: the role zone stays drawn through the enemy turn for Bergsons with kept AP (existing FR-8 icons), the role badge's existing Ready / not-ready states | Zones always on | A chooser (new) |
| Implementation | None | Per-round counter (D-061: new code), core | Small and core: a switch, a counter, the pay check (see [Prototype](#step-3-dev-switch-prototype)) | AI utility variable + graph edits per enemy, golden-master test churn (`AIRegressionTest`), core | Controller wait-list change, a new prompt UI, core |
| Risk | THJ stays stuck; Synergies keep competing with free rewards; "too easy" stays | Fixes symptoms already fixed elsewhere (quiver); THJ said removing the cost didn't help | Roles vanish if keeping AP is never worth it; less originality (overwatch is known); John's unlimited guard ends | Fewer of the loved enemy-turn QTEs; stalling AI | Decision under a 1 s timer; one more screen |
| What it loses that players love | Nothing | Nothing much | Some enemy-turn prompts (fewer, each earned); accidental combos become planned ones; some originality | Most enemy-turn prompts | The flow of the enemy turn |
| USP effect | FR as is; Synergies get the energy | FR neutral | **FR ++** (authored), **Synergies +** (roles become their ingredients) | FR changes identity (denial) | FR + |
| Cost to find out | 0 | One tech plan + M chunk | **A paper test, one house-rule play (no code), then an M chunk** | L chunk before knowing | M–L chunk |

Doing nothing is option A in effect. It is a real option, and it's the fallback if the test fails (see [Recommendation](#recommendation)). The strongest case for it is THJ's own: "maybe that is why it is fun for players: something they haven't seen before. They might begin to feel it after they repeat it as much as I have." Evidence 1, 2 and 5 are structural rather than taste, though: they hold whatever a cold player feels on first contact, and they show up as "too easy" in THJ's own pacing check.

---

## Lens notes

Done on C (leading), with A as the comparison.

### Creative

**Target experience.** The family *keeps watch over each other*. At the end of your turn you look at the board and the next-targets list (EN-10), and you choose who stays alert: Linda holds an arrow on the lane the pack must cross, John stays braced beside Lucy, Mark keeps his fists ready next to the sister the Claws want. Then the enemy turn comes, the Claw steps into the lane, the prompt lights up and Linda's arrow lands, and you *know why*: you set it up. Warmth against dread: the dread is the enemy turn, the warmth is the family member you told to look after the others.

**The moment designed for:** the enemy turn where two kept AP chain. Linda's Watch arrow passes through Lucy's Cyclone (Tempest Bloom) on *their* turn because you put the Cyclone in her lane and kept her shot. Today that is the loved accident; under C it is a plan that pays off with the same fireworks.

**Original, or the genre default?** Honestly, keeping an action for a reaction is XCOM's overwatch, the most familiar reaction in tactics. What stays Miso is the family: four different answers (shield, lane, follow-up, counter) that combine with each other and with Synergies, a press for each, and the framing ("Family Watch" is already Linda's role name, D-328). Some of the "haven't seen this before" is lost. I think it's worth it, because the part players loved (the press on the enemy's turn, the combos) survives, and the part THJ hates (the free, authorless payoff) goes.

**Where creative and systems disagree:** creative wants John to stay instinctive. A father doesn't budget AP to step in front of his daughter, and his role already costs him HP. Systems wants one rule for all four. I lean to one rule for the test (the budget: one sentence, no exceptions) and put John's exemption to THJ as Q3.

### Systems

**The rule (C, prototype v1).**

1. AP a Bergson still has when the family's turn ends is **kept** until the family's next turn starts. Today it is lost (CR-8; in code it turns into ATB steps nothing spends).
2. **Outside the family's turn** (enemy and ally turns), a Bergson's role answers only while it has kept AP, and each answer spends one. A missed or declined press spends nothing (FR-2 unchanged).
3. **On the family's turn**, roles answer as now, but free (D-036): no FTP. (v1 keeps the player-turn side unchanged apart from the cost, so the test changes one thing; v2 is Q2.)
4. Roles never cost FTP in this mode. FTP pays Duos (D-035, D-216: "FTP is for Duos only").
5. Triggers, effects and the quiver are unchanged: Watch still spends an arrow (LI-4), so a kept Linda AP is "a bow shot saved for their turn".

**Levers and starting values.**

| Lever | Start | Range to try | Where |
|---|---|---|---|
| Answers per kept AP | 1 | 1 | Rule |
| Most AP a Bergson can keep | Its AP left (2 at most today; the cap is 2, the global cap 3, CR-5) | — | Existing AP |
| Kept AP expires | At the start of the family's next turn | — | Rule |
| Player-turn roles | Free, no limit (v1) | v2: they spend the Bergson's AP too (Q2) | Switch value |
| John | Same rule (one guard per kept AP) | Exempt: free and unlimited as built, already paid in HP (Q3) | Switch value or handler flag |
| If keeping is rarely chosen | — | (a) the graded QTE already planned (D-034: a press inside the window adds a small bonus); (b) a kept AP that wasn't used becomes +1 FP at turn start (feeds Duos; reverses D-206 for kept AP only) | Later levers, one at a time |
| Enemies reading zones | Off | A small cost on destinations inside a kept zone (option D, partial) | AI, later |

**Why keeping is a real trade, not a free bonus.** Each answer is roughly what the AP would have bought on the Bergson's own turn (Watch is Linda's bow shot; Counter is Mark's Fist Blitz; Lucy's 2 × 3 embers are about one ember attack), but it is *conditional* on enemies doing what you predicted, and it lands at a better moment: Watch fires when the enemy ends its move, before it strikes (as the M1 punchline relies on, D-331); John's guard prevents a hit nothing else can prevent on the player's turn; Mark's counter punishes the attacker. So players will keep AP on approach turns (nothing in reach now), to protect a weak member, and to set up combos, and spend it when a target is in reach. That is the XCOM trade, and it's the decision the game lacks.

**Interactions.**

| With | What happens |
|---|---|
| Linda's quiver | Unchanged. A Watch answer spends a kept AP *and* an arrow. An empty quiver still means no Watch (LI-5), so keeping AP with 0 arrows is a wasted keep: the badge must show it (the existing EmptyQuiver state) |
| Synergies | Planned combos on the enemy's turn: Watch through the Cyclone (Tempest Bloom), Lucy kept + Linda kept (her follow-up chains off the Watch arrow, a family action that took HP), Watch into Mark (Catch & Return: the arrow returns to the quiver), Command Shield Dash unchanged (player's turn) |
| Duos | FTP is no longer drained by roles, so it is purely the Duo meter, which suits THJ's "Duos as finishers, an ultimate". DU-5's lever (3 FTP) may be needed if FTP now piles up |
| Sister's Rivalry | Unchanged (player's turn, basic-attack kills) |
| Masher counter (EN-2) | Its loops with roles (D-097, D-098) are now bounded by kept AP: fewer runaway chains |
| Turn-1 AP limits (`TurnStartActionPointLimit`, onboarding) | A Bergson limited to 0 AP can't keep any, so no role fires for it on enemy turn 1 (see the Hearth note) |
| Fireside (D-040, `thj/home-test`) | "+1 role use in the first round" maps to "+1 kept AP on the first enemy turn" |
| AI | Untouched in the test. AI factions pay nothing for roles today (`canPay` is true for AI), so the Masher's own role is unaffected |

**Failure cases.**

- *Roles vanish:* keeping is chosen on fewer than about 10% of unit-turns. Then levers (a) or (b) above, before calling it failed.
- *The decision is fake:* keeping is chosen almost every turn because AP has nothing better to buy (e.g. units that can't reach anything all fight). Then the levels are the problem (P1 in the pacing check: no challenge), not the rule.
- *Lottery:* enemies don't come where you predicted. The next-targets list (EN-10) and the Shift danger zones (CR-43) already let the player predict. If it still feels random, option D's small zone cost is the lever.
- *Survival drop:* John's unlimited guard ends, so the sisters take more hits. On Tutorial tier this is mild; THJ has said the game is too easy, so this is partly the point. Watch HP at fight end in the combat log.

### UX

| Moment | Shown | The player clicks | Likeliest misread |
|---|---|---|---|
| Own turn, planning | As now. Role zones under FR-9 (selected, Shift); the next-targets list | Moves, attacks, or nothing | "Leaving AP unspent is a waste" (every other game taught that). One line in the Hearth fixes it (see the onboarding note) |
| End Turn with AP left | The zones of every Bergson with kept AP stay drawn into the enemy turn (existing FR-8 icons); each role badge shows Ready | End Turn (as now) | None new; ending early just reads as "on watch" |
| End Turn with all AP spent | No zones; badges in the not-ready state (existing NoFtp state, new text) | — | "Why didn't Linda shoot?" The badge tooltip says why ("No AP kept"), and the zones were visibly absent |
| Enemy turn, a trigger | The prompt, as now. John's tether as now | The key | None: the prompt is now the celebration of a plan |
| Enemy turn, a kept AP unused | Zone stays until the family's turn | — | "It carries over": no; zones clear at turn start |

**On-screen elements:** none new. The zones already exist and the badge already has a ready/not-ready state; C changes *when* they show and what the badge counts. Readability means fewer, clearer signals (D-294): zones on the board during the enemy turn are the one signal, and they now mean something.

---

## USP check

- **Family Roles:** strengthened. Same four roles, same press, now authored: each answer is the payoff of a choice on the player's turn.
- **Synergies:** strengthened. Roles set up on purpose become their ingredients (Watch through the Cyclone, Lucy chaining off a Watch, Watch into Mark's catch), instead of a free reward competing with them. THJ's energy can go to Synergies because roles stop needing patches.
- **Duos:** cleaner. FTP becomes the Duo meter alone (D-216), which fits "Duos as finishers".
- **Managing the Home as a Family:** neutral on purpose. The Fireside payoff maps to one extra kept AP (`thj/home-test`, D-040).

## Critics

**Not spawned.** My session has no agent-spawning tool, so I ran the three `miso-design-critic` lenses myself as adversarial passes. The coordinator may want real critics on this before THJ decides, since it's L and Tier 3.

| Lens | Strongest objection | What I did with it |
|---|---|---|
| Creative | "You're turning the one original thing into XCOM overwatch. Players loved FRs *because* they hadn't seen them, and the fiction is instinct: John shields because he's a father, not because he budgeted an AP." | Accepted part of it: some originality is lost, and I say so in the options table. Kept the press as the payoff and the family-combo layer as the identity. John's instinct is THJ's call (Q3), with the exemption ready as a switch value |
| Systems | "Keeping AP is strictly worse than spending it whenever a target is in reach, so roles will only fire on approach turns, which means you've effectively removed them. And without zone-aware AI, a kept AP is a lottery." | Partly rejected: the answer lands at a better *moment* than the AP would (before the strike, a prevented hit, a punish), so protecting and combos make keeping worthwhile even with targets in reach. Partly accepted: I set a failure threshold (under ~10% of unit-turns), two levers in order (graded QTE, unused keep → +1 FP), and left AI zone-awareness as a later lever. The paper test checks it on three real levels |
| UX | "Ending a turn with AP left looks like a mistake in every other game. Players won't discover it, and the new 'why didn't Linda shoot' is exactly the confusion THJ said roles didn't have." | Accepted: C needs one line of teaching where today's roles need none, and I count it as a cost. It's placed in John's memory, where a turn-1 AP limit already forces the choice. The not-ready badge with a reason, and the zones' absence at End Turn, cover the misread |

What changed my mind: the systems pass made me split the player-turn side out of v1. Making Lucy's follow-up cost AP on the player's turn would turn every follow-up prompt into a 1 s decision under a timer, so it moved to Q2 as a second experiment. What I rejected: an aim step for Linda (the quiver plan's option E objection and D-294's "simplify" both stand; her position is the aim).

---

## Recommendation

**C, Kept AP, behind a dev switch, tested in three steps that stop early if they say no. If the test fails, lock Family Roles as built (option A, with D-036's "free" if THJ wants it) and move FR energy to Synergies.** The stop rule matters as much as the option: after many months, the next step should be a test whose answer ends the loop either way.

**Starting values:** as in the Levers table. v1: one answer per kept AP, kept AP expires at the family's next turn, player-turn roles free and unchanged, John under the same rule, no AI change, no enemy retune.

### Step 1: paper test (about 15 minutes, no build)

Three scenarios on real levels, read from the prefabs with `level_to_grid.py` on 2026-11-09 and drawn in the levels plan's frame. Coordinates: x from the left, y from the bottom; the levels plan's tiles. The AI's exact paths are **assumed** (shortest path to a tile next to its target from the next-targets list); the point is the decisions, not the exact outcome.

**How to run it:** for each scenario, THJ reads the board and writes down, for today's rules and for C: what he decides on his turn, how many prompts come in the enemy turn, and for each prompt whether he could say *why* it fired. Pass if C gives at least one real decision on the player's turn in each scenario and every enemy-turn prompt traces back to one of them.

#### S1. The Ridge, rush pack, turn 1 and enemy turn 1 (Linda + Mark)

Level: `Content/Levels/Greybox/GB_s2-ridge.prefab` (as built; the levels plan draws it one column to the right of the prefab read, and these tiles follow the plan). Tutorial tier (Claw HP 10, Claw damage ×0.5). The rush Claw on 2,4 is 3 from Linda, so it starts Alerted and its spread wakes 1,5 and 3,5 (EN-12, EN-15). The gauntlet (7,1, 8,1) sleeps. Linda's lanes: column 2 within 4 (2,0, 2,2 to 2,5) and row 1 within 4 (1,1, 3,1 to 6,1).

```grid id=frr-s1-today title="S1 The Ridge, today: turn 1 and enemy turn 1 (GB_s2-ridge)"
# . . . # # # # # # # # # #
# c . c # # # # # # # # # #
# . c . # # # # # # # # # #
# . . . # # # # # # # # # #
# . . . . # # # # # # # # #
# . L M . . . c c . . . . @
# # . . # # # # # # # # # #
--
cells 2,0 2,2 2,3 2,4 2,5 1,1 3,1 4,1 5,1 6,1 linda lanes (always on)
arrow 2,1 2,4 linda dx=-8 turn 1: 2 shots
arrow 1,5 1,4 1,3 1,2 1,1 enemy rush
arrow 3,5 3,4 3,3 2,3 2,2 enemy
step 1,1 1
step 2,2 2
note 3,1 Mark: counters both
```

| Today | |
|---|---|
| Player's turn | Linda shoots 2,4 twice (6 + 6 ≥ 10, dead; quiver 3 → 1). Mark can't reach anything (2,4 is 4 from him, Fist Blitz 2). **Decisions that shape roles: none.** Mark's counter range covers 1,1 and 2,2 because he *started* there |
| Enemy turn | 1,5 runs to 1,1 (4 steps): in Linda's row → **Watch prompt** (6, quiver 1 → 0), then it strikes Linda → **Counter prompt** (1,1 is 2 from Mark) → 8, dead. 3,5 reaches 2,2 (or 3,2) and strikes → **Counter prompt** again (no limit built). No Watch: quiver empty |
| Count | 3 prompts, 3 FTP of 5, **0 choices**, 0 of 3 traceable to a decision |

```grid id=frr-s1-kept title="S1 The Ridge, kept AP: plan K3 (Mark steps up, Linda keeps both AP)"
# . . . # # # # # # # # # #
# c . c # # # # # # # # # #
# . c . # # # # # # # # # #
# . . . # # # # # # # # # #
# . . . . # # # # # # # # #
# . L M . . . c c . . . . @
# # . . # # # # # # # # # #
--
cells 2,0 2,2 2,3 2,4 2,5 1,1 3,1 4,1 5,1 6,1 linda lanes live: Linda kept 2
arrow 3,1 3,2 3,3 mark 1 AP
arrow 3,3 2,4 mark Blitz 8
step 3,3 1
note 2,1 keeps 2
```

| Kept AP: the turn-1 question is "who keeps AP, and where do they stand?" | Grade |
|---|---|
| **K1. Kill box at Linda.** Linda shoots 2,4 once (→ 4 HP), keeps 1. Mark stays on 3,1 and keeps 2. Enemy turn: whichever Claw ends in column 2 or row 1 first meets the Watch (kills 2,4 if it steps to 2,2 or 2,3); the others strike Linda and meet up to two Counters (8 each, 10-HP Claws survive at 2) | ★ safe, slow |
| **K2. Spend everything.** Linda kills 2,4 with two shots; Mark walks up two tiles. Enemy turn: no answers at all; Linda and Mark take about 3 a hit | ● works, costs HP |
| **K3. Mark forward, Linda watches (drawn).** Mark steps to 3,3 (1 AP) and Blitzes 2,4 (2 away; 8 → 2 HP). Linda doesn't shoot and keeps both AP (2 Watch answers, 3 arrows). Enemy turn: 2,4 (2 HP) moving to 2,3 next to Mark stays in column 2 → Watch kills it before it strikes; 1,5 coming down to Linda or Mark ends in column 2 or row 1 → second Watch (6). 3,5 strikes Mark (on 3,3) from 3,4 unanswered (Mark kept nothing) | ★ aggressive |
| Count | 0–2 prompts, **each one the payoff of a choice the player made**; K2 shows that a player who doesn't keep AP sees no roles |

#### S2. Memory 3, John's telling (John, Linda, Lucy)

Level: `Content/Levels/Greybox/GB_m3-john.prefab` as built (D-393: five Claws, (4,4) acts first straight at John; turn-1 AP limit John 1, sisters 0; all alert; Tutorial). John's Shield reach is drawn as radial 2 (his shield is a square of side 2r + 1; the metric is assumed). Linda (2,1) and Lucy (6,1) are both 2 from John (4,1).

```grid id=frr-s2-today title="S2 Memory 3, today: enemy turn 1 (GB_m3-john, as built)"
# . . . . . . . #
# . c . . . c . #
# c . . c . . c #
# . . . . . . . #
# . . . . . . . #
# . L . J . U . #
# # # # # # # # #
--
zone 2,1 6,3 john Shield reach
arrow 4,4 4,3 4,2 enemy at John
arrow 2,5 2,4 2,3 2,2 enemy Watch
arrow 1,4 1,3 1,2 1,1 enemy Watch
arrow 6,5 6,4 6,3 6,2 enemy
arrow 7,4 7,3 7,2 7,1 enemy
note 4,1 Shield Up (hinted)
```

| Today | |
|---|---|
| Player's turn | John's only AP: Shield Up (hinted). Sisters 0 AP. **One decision, made for the player by the hint** |
| Enemy turn | (4,4) strikes John (Wrath 1). (6,5) to 6,2 and (7,4) to 7,1 strike Lucy → **2 John prompts** (Wrath 3, capped). (2,5) ends on 2,2 and (1,4) on 1,1, both in Linda's lanes → **2 Watch prompts** (6 each, both survive at 4), then they strike Linda → **2 more John prompts**. Lucy's follow-up doesn't reach (2,2 and 1,1 are 5 from her) |
| Count | **6 prompts, 0 choices.** And the sisters' Watch prompts are the noise the levels plan warned about ("Layout can't prevent it"), which THJ's note asks to remove: "john level only john should have fr" |

```grid id=frr-s2-kept title="S2 Memory 3, kept AP: John 2 AP on turn 1, Shield Up + keep 1"
# . . . . . . . #
# . c . . . c . #
# c . . c . . c #
# . . . . . . . #
# . . . . . . . #
# . L . J . U . #
# # # # # # # # #
--
zone 2,1 6,3 john John kept 1: one guard
arrow 4,4 4,3 4,2 enemy at John
arrow 6,5 6,4 6,3 6,2 enemy at Lucy
arrow 2,5 2,4 2,3 2,2 enemy at Linda
step 4,1 1
note 6,1 save it for Lucy?
```

| Kept AP (needs one data change: John's turn-1 limit 1 → 2 on this level, only in the test) | Grade |
|---|---|
| **Shield Up + keep 1.** (4,4)'s hit on John stacks Wrath 1 under Shield Up; the one guard stacks Wrath 2. The first sister hit comes from a Claw on Linda (20 HP): **decline it and save the guard for Lucy (15 HP)?** A real choice inside the enemy turn, because the guard is limited. Turn 2: Wrath 2 → ×1.7 Sword (13.6) kills a 10-HP Claw: the level's lesson intact | ★ the lesson |
| **Keep 2.** Two guards, no Shield Up, no Wrath: the sisters are safe, the punish is weak | ● |
| **Shield Up + attack.** No guard at all | ✗ for this level |
| The sisters have 0 AP, so they can't keep any: **no Watch, no follow-up, only John's role fires.** THJ's note is satisfied with no mute switch | |
| Count | 1 prompt (2 if he keeps both), **each one answers a choice**; the 2 Watch and 4 John prompts of today are gone |

#### S3. The River clearing, turn 1 (John + Lucy): what v1 leaves alone

Level: `Content/Levels/Greybox/GB_s1-river.prefab` (prefab read matches the plan's tiles). Three Claws asleep within 2 of each other (5,3, 6,4, 6,2). Lucy's role reach is 3, the same as her embers.

```grid id=frr-s3-river title="S3 The River clearing, turn 1 (GB_s1-river)"
# # . . . . # # . . _ . _ . . # #
# . . . . . . # . a _ . _ a . # #
# . . . . . c # _ _ . . . _ _ . .
U J . . . c . . . . . @ . . . . .
# . . . . . c # _ _ . . . _ _ . .
# . . . . . . # . a _ . _ . . # #
# # . . . . # # . . _ . _ . . # #
--
range 3,3 3 lucy follow-up reach = ember reach
arrow 0,3 3,3 lucy dy=-8 step
arrow 1,3 4,3 john dy=8 step + Sword
step 4,3 1
step 3,3 2
```

| | Today | Kept AP v1 | Kept AP v2 (Q2) |
|---|---|---|---|
| Player's turn | Lucy steps to 3,3 (wakes the clearing: 5,3 is 2 away). John steps to 4,3 and strikes 5,3 (8 → 2 HP) → **Lucy follow-up prompt** (5,3 is 2 from her) → 6, dead. **0 choices**: the follow-up came with John's attack | **Unchanged** (player-turn roles stay free and automatic) | Lucy's follow-up spends her AP: the player must have **Lucy wait with an AP** while John strikes first, or she embers on her own. A sequencing choice |
| Enemy turn | 6,4 and 6,2 strike John or Lucy; a hit on Lucy → **John prompt** (she's within 2) | John spent both AP (step + Sword) → no guard. If he'd kept one (step + keep), Lucy would have had to finish 5,3 herself: **a choice** | As v1 |
| Count | 2 prompts, 0 choices | 1 prompt, 0 choices on the player's turn; the enemy-turn side gains one | Both sides have a choice |

S3 is the honest limit of v1: Lucy's player-turn follow-up stays incidental. It is kept out of v1 so the test changes one thing; v2 is Q2.

### Step 2: house-rule play (one session, no code)

The cheapest *playable* test, with no build: THJ plays The Ridge and Memory 3 (and one M4 or M6 fight on `main` rules) under a house rule.

- Before the session, press **L** (+99 FTP, `tech/combat-architecture.md` cheats) so FTP never limits a role.
- At End Turn, note on paper each Bergson's AP left.
- In the enemy turn, **press a role prompt only if that Bergson has a kept AP left**, and cross one off. Otherwise let the prompt time out.
- Player-turn prompts: press freely.

Side effects to ignore: let-pass prompts still appear (pacing), play their decline bark, and silence that target for the rest of the turn (as built). For Memory 3, use **]** (+1 AP) on John at turn 1, or skip it if the limit can't be lifted that way.

**Read after the session:** did keeping AP feel like a decision? Did each pressed prompt feel earned? Did roles still feel fun? Did fights feel harder? If THJ answers no to the first two, stop: **lock FRs (option A) and move to Synergies.** If yes, step 3.

### Step 3: dev switch prototype

A setting beside the existing AP and passive modes, default = the game as built.

**`GlobalSettingsSO.familyRoleCostMode`**: `FamilyPoints` (as built: 1 FTP per answer, any phase) / `KeptAP` (this plan's rule v1). Optional third value later for v2 (`KeptAPBothTurns`).

| What | File (core marked) | Change |
|---|---|---|
| The switch | `Core/Managers/GlobalSettingsSO.cs` **(core)**, `Resources/GlobalSettings.asset` | One enum field beside `pointConsumptionMode` and `aPConsumptionMode`, default `FamilyPoints` |
| Record kept AP | `Core/Interactions/Runtime/PlayerController.cs` **(core)**, `EndTurn` | Before `ConvertUnusedApToAtbSteps` drains the AP into the unused ATB gauge, store each Bergson's AP left as its kept AP (verified: `EndTurn` calls `ConvertUnusedApToAtbSteps` on every living unit in PerUnit mode, and the method computes `unused` there) |
| The counter and rules | New `Core/Systems/AbilitySystem/Abilities/Runtime/FamilyRoleKeptAP.cs` (pure rules + per-unit count, like `FactionRoleRules`) | `CanAnswer(mode, phase, kept)`, `Spend`, `Clear`; cleared when the family's turn starts. EditMode tests |
| The pay check | `Core/Interactions/Runtime/FactionControllerBase.cs` **(core)**: `ApplyFactionRolesIfPossible` → `ActivateFactionRoleIfFeasible` → `ActivateFactionRole` | Pass the phase through (today only `ApplyFactionRolesIfPossible` knows it). In `KeptAP`: player phase pays nothing; other phases need a kept AP and spend one. AI unchanged (`canPay` true). Payment stays at the press (the player override calls the base only after the press, verified), so a missed press spends nothing |
| Zones in the enemy turn | `Core/Systems/RoleZoneSystem/Runtime/RoleZonePresenter.cs` (not on the core list) | Draw the zones of Bergsons with kept AP from End Turn until the family's next turn |
| Badge | `Features/UI/Panels/Scripts/RoleBadgeState.cs`, `UnitPanelUI.RoleBadge.cs` | In `KeptAP`, Ready/not-ready reads kept AP (outside the family's turn) instead of FTP; tooltip line "No AP kept" for the not-ready state (placeholder text) |
| Combat log | `tech/combat-log.md` line format (additive) | Append "kept N" to role lines and to End Turn, so the balance scripts can count keeps per unit-turn |
| Test data | Memory 3's `TurnStartActionPointLimit` | John 1 → 2, only for the test (the component works only in FTP passive mode, which this switch doesn't change) |

**Not touched:** the four role handlers (triggers and effects), the quiver, Duos, AI, `PointConsumer`, ATB code.

**Tier 3 items for THJ:** (1) the rule of a USP mechanic; (2) behaviour changes in `FactionControllerBase` and `PlayerController` (core), even if only behind the switch; (3) a new field in `GlobalSettingsSO` (core settings; D-446 shows THJ prefers code switches for features, see Q4); (4) a new class combat would rely on if adopted (the reviewer decides if it joins `tech/core-systems.md`).

**Size:** M. One implementer session, about 150–250 lines with tests, then review and a ~30 minute play check by THJ (the step-2 levels, switch on and off). Needs a tech plan from the coordinator first.

**Playtest signal (step 3 and the cold playtest).**

- *Worked:* a player can say why each role fired ("I kept Linda's AP and the Claw walked into her lane"); keeping is chosen on roughly 25–60% of unit-turns (combat log); fewer prompts per enemy turn than today, each pressed; at least one planned role + Synergy per fight (Watch through the Cyclone, Lucy off a Watch); fights move toward the 1.6–2.6 rounds target ([`combat-balance.md`](../design/combat-balance.md)).
- *Failed:* keeping under ~10% of unit-turns after one lever (roles vanished); or above ~90% (the choice is fake, which points at the levels); or "why didn't she shoot?" persists after the Hearth line.
- *Then:* failed → switch back to `FamilyPoints`, lock FRs, THJ's energy to Synergies. Worked → v2 question (player-turn side), then the GDD rewrite.

### What this means for the Hearth (the onboarding after the Hearth)

`plans/onboarding/2026-11-09-onboarding-after-hearth-design.md` was not found on 2026-11-09 (the parallel track hasn't written it yet), so here is what C means for whoever writes it:

- **THJ's answer (2026-11-09) holds for the press:** the prompt teaches itself. C adds one thing to teach, once: **keeping AP**. One line, at the moment it matters, not a panel up front.
- **Roles appear when the player opts in.** A new player who spends every AP sees no enemy-turn roles. That gives THJ's "FR off in Memories 1 and 2" without a mute switch. In Memory 1, a Watch fires only if Linda ends with AP left, which is a pleasant discovery rather than rule five on a card. D-331's punchline (2 Watch shots on enemy turn 1, the turn-2 shot her last arrow) would need retuning under the switch.
- **John's memory is the natural first lesson** (THJ: "John's is the first, in Memory 3"). The turn-1 AP limit already forces the choice: John with 2 AP, Shield Up, and one line such as "Keep an action and John will stand guard on their turn". Shield Up + keep 1 is exactly the Wrath loop (S2). The sisters at 0 AP can't keep any, so only John's role fires.
- **After the Hearth (River, Ridge, Trail): challenge it.** "Keep or spend" is the kind of question THJ's rhythm wants ("teach, then challenge"): the Ridge's rush asks who keeps AP for Linda; the River's Archers ask whether John keeps a guard for Lucy; a pair-Synergy setup asks for two kept AP that chain (Linda's lane through Lucy's Cyclone). That points the post-Hearth levels at Synergies, as THJ asked.
- **Duos as finishers:** FTP drained only by Duos makes the Trail's FP lesson cleaner ("FP is for Duos").

---

## Questions for THJ

**Q1. Run the three-step test, with the stop rule?**
- Context: every past fix changed how often or how cheaply roles fire; none gave the player a decision on their own turn without adding a calculation (Far Watch) or a step (aimed Watch). C uses AP the player already has and loses today.
- Options: (a) paper test → house-rule play → dev switch, and if step 2 says no, lock FRs as built and move to Synergies; (b) go straight to the dev switch; (c) lock FRs now (option A) and skip the test; (d) build Pilot 1 as decided (option B).
- Recommendation: (a). Steps 1 and 2 cost one evening and no code, and either answer ends the loop.
- Blocked: the coordinator's tech plan for the switch; any further FR work (the Family Role chunk's items 1 and 10).

**Q2. In the test, should player-turn roles stay free and automatic (v1), or also spend AP (v2)?**
- Context: Lucy's follow-up fires mostly on the player's own turn (S3) and stays incidental under v1. Under v2, every player-turn prompt becomes a "spend her AP now?" choice inside a 1 s window.
- Options: (a) v1 first, v2 as a second switch value only if v1 works; (b) v2 from the start; (c) v1, and later move Lucy's follow-up to a Synergy (automatic, no prompt) instead of v2.
- Recommendation: (a). One variable per test (the D-246 precedent).
- Blocked: the switch's enum values.

**Q3. John: the same rule (one guard per kept AP), or exempt?**
- Context: John's guard is already paid in HP and adds no damage; creatively it's a father's instinct. Under the rule he guards once or twice per enemy turn instead of every hit within 2. S2 shows the limit makes his guard a real choice (decline one hit to save it for Lucy).
- Options: (a) same rule for all four; (b) John exempt: free and unlimited outside the family's turn, as built.
- Recommendation: (a) for the test, with (b) as a switch value ready if the sisters drop too fast.
- Blocked: the rules class.

**Q4. Where should the switch live?**
- Context: the brief asks for it beside the AP and passive modes in Global Settings. For the sisters' tally, THJ preferred a code switch in the feature folder over a Global Settings field (D-446).
- Options: (a) `GlobalSettingsSO.familyRoleCostMode`, beside `pointConsumptionMode` and `aPConsumptionMode`; (b) a code constant in the new rules class.
- Recommendation: (a). It's a combat mode like the other two, and THJ will flip it often during the test.
- Blocked: the tech plan.

**Q5 (information, no decision now). Enemies reading role zones.** Not in the test. If kept AP feels like a lottery because enemies don't go where the player predicted, a small AI cost on destinations inside a kept zone is the lever (option D, partial). It's core AI work with golden-master churn (`AIRegressionTest`), so only after the test says C is right.

The working name "kept AP" needs a player-facing name. "Watch" is taken (Linda's role, D-328; FR-6 notes the clash). For `miso-narrative`.

## Docs to update (if approved)

After the test, and only if C is adopted:

- `design/gdd/family-systems.md`: FR-3 and FR-4 (status: replaced by the kept-AP rule), a new **FR-14** (the rule; next free FR ID), FR-6 (the label, renamed), FR-9 (zones drawn through the enemy turn for Bergsons with kept AP), the role table's "Limit per round" column, the Deferred table (Pilot 1's caps).
- `design/gdd/combat-rules.md`: CR-8 (leftover AP is kept for roles until the family's next turn), CR-6 (roles' cost), CR-13 (FTP pays Duos only).
- Character pages: John (unlimited guard), Linda (LI-11: the quiver and kept AP), Lucy, Mark.
- `design/combat-balance.md`: the reactions-per-round assumption (2 per hero) and Linda's share.
- `plans/family-role-chunk.md`: items 1 and 10 superseded; item 8 (the decline rule) gains weight, since a decline now saves an answer.
- Onboarding plans: Memory 3's turn-1 limit (John 2), Memory 1's Watch punchline, the first-hour design's FR line, and the after-Hearth design (not yet written).
- `glossary.md`: the kept-AP name.
- `decisions.md` (coordinator): the answers to Q1 to Q4.

Grids in this plan, to render: `frr-s1-today`, `frr-s1-kept`, `frr-s2-today`, `frr-s2-kept`, `frr-s3-river`.

## Branches

- **`thj/onboarding`** (working main): build the switch here (D-396). Default `FamilyPoints` keeps every tuned onboarding level as it is.
- **`main`**: fast-forwards from `thj/onboarding` later (0 ahead); takes the switch with it. Pilot 1 (D-042) was meant to be built on `main`; if C is adopted, it replaces Pilot 1's caps.
- **`thj/home-test`**: no quiver, roles at 1 FTP, Fireside "first Family Role free" written against FTP. On merge, the Fireside payoff needs mapping to "+1 kept AP on the first enemy turn" under `KeptAP` (D-040).

## Risks

- **Roles vanish** (keeping is never worth it): thresholds and two levers in order; the test stops early if it fails.
- **Originality loss** (overwatch is known): accepted in part; the family combos and the press stay. THJ judges it in step 2.
- **Teaching cost:** C needs one line where roles needed none. Placed in John's memory, where a turn-1 AP limit already forces the choice.
- **Tuned onboarding levels** (Memory 1's punchline, Memory 3's turn-1 limit) assume today's rules. The switch defaults to as built, so nothing changes until THJ flips it; the levels get retuned only if C is adopted.
- **AI assumptions in the paper test:** the paths are assumed; step 2 is the real check.
- **Scope creep into AI or enemy tuning:** both are out of the test on purpose.

## Gates

Design only. Step 1 needs THJ's time (~15 min, paper). Step 2 needs THJ's time (one session, no code). Step 3: tech plan (coordinator) → implementer (compile, EditMode tests) → reviewer → THJ play check (~30 min) → cold playtest. Docs as listed, only after adoption.
