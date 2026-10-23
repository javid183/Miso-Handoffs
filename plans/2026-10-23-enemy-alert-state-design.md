# Enemy alert state (Unaware / Alerted)

Size: L    Tier: 3 (new mechanic; THJ decides)    Assigned to: miso-game-designer
Branch: all (built on `main`; `thj/home-test` takes it with `main`)
Status: waiting on THJ

## Why

THJ's request (2026-10-23, not yet a decision): one simple rule. Enemies stay on their tile and don't come for the family until a family member is within their sight range ("not a line but a range"), or something alerting happens to them or near them (an attack or ability on them or on nearby cells, a smaller alert range). Ranges are new per-enemy values, or derived: sight = walk reach + attack reach, alert range = half of that.

## Goal

A rule that turns the opening of every fight into a family decision (where, when and how to engage) without adding a system the player has to study.

## Acceptance criteria (for the design, once approved)

- [ ] Each enemy is **Unaware** or **Alerted**; the rules for waking fit in five lines (EN-12 to EN-17 below).
- [ ] An Unaware enemy never moves or acts; an Alerted one plays exactly as today.
- [ ] The player can tell, before committing, whether a move wakes an enemy (the move ghost), and can see an Unaware enemy's sight area (Shift).
- [ ] Levels can opt out: "all enemies start alert" per level, "starts alert" per placed enemy.
- [ ] `AIRegressionTest` is not re-baselined; no utility graph, utility variable or AI ability changes.

## Scope

In: the state, its triggers, propagation, timing, exceptions, minimal readability (icon, "!" pop, Shift sight area, move-ghost wake marker), level overrides.
Out: facing or vision cones, losing alert again, stealth bonuses (ambush damage), sound and barks beyond a placeholder, Home hooks (Omens, meals), a rebalance of existing levels (only a play check of a sample).

## Touches

Systems: AI turn flow (which units act; core: `AIController`/`AIFactionBrain`, see `tech/core-systems.md`), Shift preview and threat arcs (CR-39, CR-43), move ghost, unit info panel, Black Claw memory share (EN-1), spawners (EN-4, EN-5, corruption pools, wave spawns), level settings.
USPs: Family Roles, Synergies, Duos (interactions only, no rule change); Home neutral.
Docs: `design/gdd/enemies.md` (new EN-12 to EN-17), `design/gdd/combat-rules.md` (CR-54, CR-55 previews), `glossary.md` (names), `design/level-chunks.md` (the "bell" and "sleeping" knobs become real rules).

---

## Problem and evidence

**Symptom (THJ's request):** every enemy rushes the family from turn 1, wherever it stands.

**Root problem:** the board has no "before" moment. Because every enemy converges at once, levels play as one undifferentiated brawl; positioning before contact, choosing which group to engage, and setting up family tools (Pass-by for FTP, Shield Up, Linda's lane) all happen under fire or not at all. Level designers can't build rooms, pods or "wake the pack on your terms" puzzles.

**Evidence:**

- The level-design notes already assume this rule exists and can't be built without it: "the pack sleeps beyond a spike band… Ring the bell so the pack comes the way you want" (`design/level-chunks.md` chunk 15), "a Black Claw asleep beside one" (chunk 11 knobs), "Three Claws wake in the next room" and "Cyclone in the throat on the turn they wake" (`plans/2026-10-21-showcase-levels-design.md`, Lucy's telling), "a pool next to a sleeping Black Claw" (same plan, F).
- EN-1 (Pact Leader) is already a "bell": hitting the Black Claw turns the pack on the attacker. Today the pack is already coming, so the bell only redirects; with an alert state it can also *start* a fight.
- Verified in data: enemy walk reach is `3 × Stat_SPD`, bounded by `StatUB_SPD` (`DarkClaw_Ability_Walk.asset` `radiusV`), costs 1 AP (`apConsumptionType` 1), and enemy basic attacks spend all AP left (CR-6). So the derived "walk + attack reach" equals what an enemy can hit next turn, the same reach CR-43's danger zone shows.
- Verified: no alert, aggro, sight or detection concept exists in code today (search of `Assets/_Project` for those terms found none). "Dormant" in D-151 means `Status.Inactive`, a different thing.
- `AIRegressionTest` is a catalog test: it hashes every utility graph, the utility-variable list, an ability→evaluator catalog and a unit catalog (`tech/mechanics-brief.md` §7; file header read). Any change there fails it. It doesn't run the brain, so a filter in the brain or turn flow leaves it alone; a new utility variable or a graph edit would not (Explore map, 2026-10-23).
- Code facts from the Explore map (2026-10-23, relayed by the coordinator, not re-checked by me): grid distance already exists as Manhattan ("Adjacent") or Chebyshev ("Radial") with footprint distance for multi-tile units, and there is no line-of-sight code. Walk reach = the largest Move radius; attack reach = the largest radius among attack abilities, both cheap. Every hit calls `GotTargeted` on the units hit (Family Role follow-ups, Duos, the Masher counter and Linda included; hazards not), and area hits report their affected cells, so both triggers are detectable. All spawns (summons, splits, pools, waves, revives) go through one spawn path. Per-instance overrides of unit fields work in levels. Status tags can show on the info panel, pop floating text when gained, and be read by AI Tag nodes. The same AI controller runs the allied Toba and the Deer.

---

## Research: how the inspirations do it

From my knowledge of the games, not checked on the web for this plan:

- **Fire Emblem:** many enemies are "stationary until a unit enters their range", and the danger-area toggle shows the exact tiles. Players learn to "pull" one enemy at a time. The lesson: a sight area the player can **see** makes waiting enemies a puzzle, not a trap.
- **XCOM 2:** enemies sit in pods; contact reveals the whole pod at once with a camera beat, and the pod scrambles. Lessons: (1) a reveal is a dramatic moment worth a beat; (2) waking a **group**, not one unit, is what makes the opening move matter; (3) the free scramble move felt unfair to many players, so I don't copy it.
- **Into the Breach:** perfect information. Lesson: every wake should be previewable before the click (our CR rule "what a preview promises, the real action does").
- **Children of Morta:** rooms of enemies that engage as the family enters; the family is the intruder in the Corruption's space. The feel to keep: the dread of a quiet room.

---

## Options compared

### A. The overall shape

| | **A1. Do nothing** | **A2. Sight + noise, derived ranges, chain within the alert range (recommended)** | **A3. Authored pods (XCOM style)** | **A4. Sight only (no noise, no chain)** |
| --- | --- | --- | --- | --- |
| Player experience | Brawl from turn 1, as today | A quiet opening; the player picks where to engage; packs wake together; the bell, shouts and decoys become ways to start a fight | Strong pod reveals, but the player can't predict who belongs to which pod unless the UI shows groups | Enemies ignore a fight 3 tiles away; snipe-from-outside-sight exploit (Linda hits, nothing else wakes) |
| Rules complexity | None | Two triggers (sight, noise), one spread rule, one timing rule | Sight + a group id per enemy + a group display | One trigger |
| Implementation cost | 0 | M: a state, a sight check on moves, a noise check on abilities, a spread step, a turn-skip gate, an icon, a pop, two preview additions | M+: the same plus level authoring of groups and a group UI | S |
| Risk | Levels in level-chunks stay unbuildable | Existing levels may get easier (pulling singles); pacing of empty turns | Authoring burden on every level; invisible groups confuse | Feels dumb; exploitable |
| USP effect | Neutral | Positive: a setup phase for Pass-by, Duos (shout, decoys) and roles | Same as A2 | Weaker |

### B. Sight: distance metric

| | **B1. Manhattan, through walls (recommended)** | **B2. Walking path distance** | **B3. Chebyshev (square)** |
| --- | --- | --- | --- |
| Shape | Diamond, like CR-15's "adjacent" steps | Irregular, follows corridors | Square, diagonals cost 1 |
| Predictable | Yes: count steps, ignore terrain | Hard: changes as units move and block paths | Yes |
| Matches "walk + attack" | Close (the walk is path-based, so through a wall it overstates) | Exactly the danger zone (CR-43) | No: overstates diagonals |
| Walls | Don't block: an enemy "senses" through a thin wall | Block naturally: the next room stays asleep | Don't block |
| Cost | Trivial, fixed at level start | A pathfind per enemy per check; must ignore other units or it flickers | Trivial |
| Risk | "It saw me through a wall": solved by level spacing | Body-blocking a corridor hides the family (exploit); shape flickers | Doesn't match the rest of the grid |

THJ said "not a line but a range", which reads as no line of sight. B1 is the plain reading.

### C. Ranges: derived or authored

| | **C1. Derived, with a floor and a per-prefab override (recommended)** | **C2. Authored per enemy type** | **C3. Derived only** |
| --- | --- | --- | --- |
| Rule | Sight = walk radius + longest Attack reach, at least 3. Alert range = half of sight, rounded up, at least 2 | A number on each prefab | Sight = walk + reach, alert = half |
| Pros | Self-explaining ("it wakes when you're where it could hit you next turn"); follows speed and reach changes; overrides for odd cases | Full control | Simplest |
| Cons | A floor is one more number | Numbers the player can't reason about; drift from the unit's real reach | Worm and Masher get sight 2 and alert 1: practically blind |

### D. Propagation

| | **D1. Chain within the alert range, at the moment of waking (recommended)** | **D2. None** | **D3. Authored groups** |
| --- | --- | --- | --- |
| Rule | When an enemy becomes Alerted, every Unaware enemy within *its* alert range becomes Alerted too, and so on | Each enemy alone | A group id; one wakes, all wake |
| Feel | Packs wake as packs; spacing is the level designer's tool | Pull singles at will: fights trivialize | Precise, but invisible |
| Cost | Small (flood fill) | None | Authoring + UI |

### E. Timing

| | **E1. Player-turn wakes act on the next enemy turn; enemy-turn wakes wait one more (recommended)** | **E2. Every wake acts on the next enemy turn, even mid-enemy-turn wakes that haven't had their slot** | **E3. Every wake costs a turn ("rousing")** |
| --- | --- | --- | --- |
| Feel | Stepping in is a commitment; a pack woken by a reaction during the enemy turn gives the player one turn to answer | Surprise attacks the player couldn't preview | Alpha-strike cheese: wake and kill before they act |

### F. What an Unaware enemy may do

| | **F1. Nothing at all (recommended)** | **F2. Act without moving (attack, heal, summon from its tile)** |
| --- | --- | --- |
| Read | "Unaware = it won't act" | "Unaware = it won't walk", plus exceptions |
| Note | With derived sight, attack reach is always inside sight, so a target in reach has already woken it. F2 only differs for the Shaman (heal, summon) and for overrides | A Shaman healing and summoning while "unaware" contradicts the icon. Cheapest to build (just don't offer move abilities), but attacks that move (the Queen's Charge and Jump, Teleport attacks) would then still "approach": each needs a ruling |
| Cost | Skip the unit in the turn flow: also cheap, and no per-ability rulings | Filter move abilities, plus a list of moving attacks to block |

---

## Lens notes

### Creative

**Target experience:** the family steps into a quiet room of the Corruption and gets one breath before it notices them. In that breath they gather (pass through each other for FTP, Shield Up, take Linda's lane) and decide together who rings the bell. Then the "!" ripples through the pack and it turns. Warmth before the dread.

**The moment I'm designing for:** John raises Shield Up beside the bridge and strikes the sleeping Black Claw. One "!" becomes five as the pack wakes around it, and all of them come for John, into Linda's lane (level-chunks chunk 15, now playable as written).

Secondary moments: Linda stepping one tile too close and seeing three "!" pop (a lesson that sticks); the Family Watchers shout used as a deliberate war cry; a Hide and Seek decoy dropped at the edge of a pack's sight to pull it off the protectee.

Originality: the pull-and-pod structure is genre standard (Fire Emblem, XCOM). What makes it ours is what wakes them: family tools (the bell, the shout, decoys, Pass-by before contact). I'm not adding stealth damage bonuses: that would push toward an assassination game, away from "a family under pressure".

### Systems

**The rules (proposed GDD text, EN-12 to EN-17; the next free EN id is 12):**

- **EN-12. Unaware and Alerted.** At level start, every enemy placed in the level is **Unaware**, unless the level or the unit says it starts alert (EN-17). An Unaware enemy stays on its tile and takes no action on its turn: no move, attack, heal or summon. Reactions still fire once it is Alerted (EN-13). An enemy never goes back to Unaware.
- **EN-13. Sight.** An Unaware enemy becomes Alerted when a unit hostile to it (a Bergson, the allied Toba, a protectee such as the Whitemother stag, a Lucy decoy) **stops** on a tile within its sight. Sight is counted in Manhattan steps from the enemy's nearest tile, through walls and units. Stopping includes the end of a walk, a push or pull, a Blink, the Dance, a Command move, and appearing on the board (deploy, decoys). Passing through sight mid-walk doesn't count. The check also runs at the start of each enemy turn.
- **EN-14. Noise.** An Unaware enemy becomes Alerted when (a) an ability targets or affects it (damage, status, push, Command; evaded hits too), whoever used it, or anything damages it (spikes, Burn); or (b) an ability used by a Bergson or an ally affects a tile within its **alert range** (the tiles the ability hits or lands on, not the flight path). Hazards, status ticks and enemy abilities make no noise around them.
- **EN-15. Spread.** When an enemy becomes Alerted, every Unaware enemy within its alert range becomes Alerted too, and those spread it in turn. Spread happens only at the moment of waking: an Alerted enemy walking past a sleeping one doesn't wake it. The Black Claw's Pact Leader call (EN-1) also alerts every Dark Claw it reaches (within 5) and the Black Claws it shares grudges with (within 10).
- **EN-16. Timing.** An enemy Alerted during the family's turn acts normally on the next enemy turn. An enemy Alerted during an enemy turn (by a Family Role, a Masher counter, a push) starts acting on the following enemy turn, even if its slot hasn't come yet. At level start, enemies that already see a hostile unit start Alerted, with no pop.
- **EN-17. Exceptions.** The rule applies only to factions hostile to the player (the Enemy faction). The allied Toba and neutral units such as the Deer share the AI controller but are never Unaware. Always Alerted: bosses (the Goblin Queen, the Mountain Deev), the enemy Toba of the duel, and every unit that appears mid-fight (Shaman summons, corruption-pool and wave spawns, Worm split children). A level can set "all enemies start alert" (defend, escort, survive-waves and boss levels). A placed enemy can be set "starts alert". A prefab can override its sight (alert range stays half, rounded up).

**Levers and starting values:**

| Lever | Start value | Where |
| --- | --- | --- |
| Sight | Walk radius (read at level start) + the longest reach among its Attack abilities (not heal, summon, jump), at least **3** | Derived; per-prefab override |
| Alert range | Sight ÷ 2, rounded up, at least **2** | Derived |
| Default for levels | Rule **on** in every level; per-level "all start alert" off | Level setting |
| Spread | On, within the waking enemy's alert range | Global |
| Optional anti-stall (not in the first chunk) | "Every enemy wakes at round N" per level, off | Level setting |

Derived values from the presets (walk and reach from `design/level-chunks.md` › Enemy reference, read from the presets; Black Claw walk and Masher reach still to check):

| Enemy | Walk | Longest attack reach | Sight | Alert range |
| --- | --- | --- | --- | --- |
| Dark Claw | 4 | 1 | 5 | 3 |
| Black Claw | 4 (to check) | 1 | 5 | 3 |
| Archer Goblin | 3 | 3 | 6 | 3 |
| Dark Shaman | 3 | 2 (shot; heal and summon don't count) | 5 | 3 |
| Dark Worm | 1 | 1 | 2 → **3** (floor) | 2 |
| Masher Goblin | 1 | 1 from its 2 × 2 edge (to check) | 2 → **3** (floor) | 2 |
| Goblin Queen, Mountain Deev | — | — | Always alert | — |

Family reach for comparison: Linda's arrow 4 (6 with Longshot), Lucy's embers within 3.

**Interactions:**

| With | What happens | Rule change? |
| --- | --- | --- |
| John's role (FR) | Triggers only on an enemy action, so only Alerted enemies; unchanged | No |
| Linda's role | Fires when an enemy ends a move in her lane: Unaware enemies don't move, so no Watch shots on them. Her role arrow is a Bergson ability: it makes noise (EN-14) | No |
| Lucy's role | Her embers may pick an Unaware enemy within 3 of the action; it wakes (it is hit). Usually it was inside the alert range of that action anyway | No |
| Mark's role | Answers an enemy hit, so only Alerted enemies | No |
| Masher counter (EN-2) | The hit wakes it first (EN-14a), then it counters as today, walking in if it must. The counter runs outside the AI brain, so the wake must be applied before the counter check, or the counter must ignore the state | No |
| Moving attacks (Queen Charge and Jump, Teleport attacks) | Never reached while Unaware: F1 skips the whole unit, and the Queen is always Alerted | No |
| Black Claw (EN-1) | The bell now also wakes the pack (EN-15) | Extends EN-1 |
| Shaman heal (EN-11) | An Unaware Shaman doesn't heal or summon. Awake, it may heal an Unaware ally (D-151 allows it); the heal doesn't wake that ally, but the Shaman's own waking already spread to allies within 3, its heal range | No |
| Synergies | Tempest Bloom copies, Shield Flare copies, Catch & Return: each is a Bergson ability hitting tiles, so it wakes what it hits and makes noise | No |
| Duos | Family Watchers (shout, 3–5 around Mark or John) wakes every enemy it marks: a deliberate war cry. Hide and Seek decoys count for sight: drop one at a pack's edge to wake it and pull it. The Dance and the Footrace are moves: sight only, no noise | No |
| Pass-by | Free and silent: the family can gather for FTP before contact | No |
| QTEs | No effect of their own; the ability they boost makes noise as usual | No |
| Lucy's Cyclone | The cast makes noise on its tiles. Afterwards it wakes only what it hits, not what it drifts near | No |
| Taunted | A taunt affects the unit, so it wakes | No |
| Stunned | Waking doesn't remove Stunned; the skip still applies | No |
| Enemy introductions (EN-10) | Unchanged | No |
| Objectives (MI-17) | "Defeat all" still counts Unaware enemies; protectees count for sight | No |

**Failure cases:**

1. **Pulling singles trivializes fights.** Spread (EN-15) and level spacing answer it; packs placed within 3 of each other wake together. Watch HP lost per level against today.
2. **The empty walk.** Turns spent walking toward enemies with nothing awake. Unaware-only enemy turns must end at once (no camera visits). If a level drags, set "all start alert" or use the round-N lever later.
3. **The last sleeper.** "Defeat all" ends with a walk to a far, sleeping enemy. Acceptable at first; it's a level-layout issue.
4. **Kiting.** Linda at 6 (Longshot) hits a Claw (sight 5), retreats. This exists today without the rule; the Claw still closes 4 a turn.
5. **Snipe-from-outside-sight.** Closed: damage always wakes the target (EN-14a), and noise wakes its neighbours.
6. **Enemy-turn surprise.** Closed by EN-16: anything woken during the enemy turn waits a turn.
7. **AI regression test.** The gate lives in the turn flow or brain (skip Unaware units, leave them out of the faction plan and target prediction). The test doesn't run the brain, so that is safe; no utility variable is added and no graph is edited (an AI Tag node reading Unaware is not needed). Whether a new field or component on unit prefabs changes the unit catalog is for the tech plan to check. The test stays known red and is never re-baselined.

### UX

**What the player sees, when:**

| Moment | Shown |
| --- | --- |
| Always | An Unaware enemy carries a small icon over its head (placeholder: a closed eye or "…"). Alerted enemies carry nothing: alert is the normal state, the icon marks the exception. Cheapest route: Unaware as a status tag, which the info panel already lists; removing it fires the "!" |
| Hover / info panel | "Unaware" on the panel; its next-targets list reads "Unaware" instead of targets (EN-10) |
| Shift on an Unaware enemy | Its **sight area** in a new tint, in place of its move range (CR-43's layer), plus its danger zone as today: "come into the yellow and it wakes; once awake, it can reach the red" |
| Move preview | If the ghost tile is in an Unaware enemy's sight, that enemy shows a faint "!" (the wake marker). Threat arcs (CR-39) come only from Alerted enemies and from those this move wakes |
| Ability targeting (second chunk) | Unaware enemies that the hovered target would wake (EN-14b) show the same faint "!" |
| On waking | A "!" pops over the enemy (about 0.6 s); along a spread, the pops stagger about 0.1 s outward so the wave reads; the enemy turns to face what woke it; a short placeholder sound. No camera move during the family's turn |

What the player clicks: nothing new.

**Likeliest misreads:**

1. "Why did that one wake? I wasn't near it." It was spread from a neighbour, or noise from an ability. The staggered pops show the chain; the ability preview's wake marker (second chunk) prevents it.
2. "It's in my Shift red zone but didn't attack." The red zone is what it reaches once awake. The Unaware icon and the sight tint must read clearly as "not yet".
3. Walls: a player expects a wall to hide them. The diamond drawn through the wall on Shift tells them otherwise.

**Proposed names (for the narrative agent and THJ):** **Unaware** and **Alerted**. Avoid "Dormant" (D-151 uses it for `Status.Inactive`), "Watch" (taken by Family Roles, FR-6), "Asleep" (goblins on guard aren't asleep). Tooltip draft: "[PLACEHOLDER] Hasn't noticed the family. Wakes if one of you stops within N tiles, or a fight starts near it."

### Where the lenses disagree

- **Creative wants walls to hide the family** (B2): the next room really is the next room. **Systems and UX want Manhattan** (B1): stable, cheap, drawable. I lean B1: level spacing does the same job, and a shape that flickers as units move would break the readability rule. Revisit if level designers keep fighting it.
- **Creative wants the reveal to be a camera beat** (XCOM). **UX says don't move the camera in the player's turn.** I lean UX: pops and a sound only; the camera already visits enemies on their turn.
- **Systems would like a floor on sight**; THJ asked for a derived rule. I lean toward the floor (one number) because Worm and Masher at 2 read as broken, not as slow.

---

## USP check

- **Family Roles:** neutral, on purpose. No role rule changes. Linda gets fewer early Watch shots (Unaware enemies don't walk into her lane); her lane becomes a place to *pull* a pack into.
- **Synergies:** neutral to slightly positive. Unchanged rules; Tempest Bloom and Shield Flare become ways to wake a pack from a chosen spot.
- **Duos:** positive. Family Watchers becomes a war cry that starts the fight; Hide and Seek decoys pull a pack where the family wants it; the Dance repositions silently.
- **Managing the Home as a Family:** neutral now. A later hook on `thj/home-test` (Omens such as "Restless: every enemy starts alert", a meal for quiet steps) is out of scope.
- **Pass-by** (not a USP, but family): positive; the family can gather and fill FTP before contact.

## Critics

The `miso-design-critic` agent type isn't available in this session, so no critics were spawned. I ran the three lenses against my own leaning; the coordinator may want real critics before THJ decides.

- **Creative critique:** "Unaware" risks making fights feel like chores: walk, poke, fight, walk. *What I did:* chain spread (D1) so the unit of play is the pack, not the single; the round-N lever kept ready.
- **Systems critique:** the sight check on every "stop" (push, Command, Dance, decoys) has many entry points; one missed path means an enemy that should wake doesn't. *What I did:* the enemy-turn-start check as a safety net (EN-13), and a single "a unit stopped on a tile" hook as the stated requirement for the tech plan.
- **UX critique:** two overlapping areas (sight and danger zone) on Shift may blur. *What I did:* sight replaces the move-range layer rather than adding a third; tints to be checked in play like CR-43's.

---

## Recommendation

**A2 + B1 + C1 + D1 + E1 + F1**, rules EN-12 to EN-17 as written above, on by default in every level, with the per-level and per-unit overrides.

**Starting values:** sight = walk + longest Attack reach, at least 3; alert range = half, rounded up, at least 2; spread on; the round-N lever not built.

**Levels to set "all start alert" at once:** every boss level (M4's Queen, M10, M12), M4's protect and escort levels (Level2-C2, Level2-C3-1, Level2-C3-2), M3 Mark Intro C1 (survive waves), the Dom duel, `LevelHomeDefence`. The level owner checks the rest in play.

**First chunk (minimal, playable):**

1. The state and rules EN-12 to EN-17 (sight at stop and at enemy turn start, noise, spread, timing, exceptions, overrides).
2. Unaware enemies skipped in the enemy turn, left out of the faction plan and target prediction, without touching utility graphs, variables or AI abilities.
3. The Unaware icon, the "!" pop with stagger and facing, the "Unaware" line on the info panel and next-targets list.
4. Shift on an Unaware enemy: the sight area.
5. The move-ghost wake marker and threat arcs only from enemies that are or would be Alerted.
6. Edit-mode tests: derived ranges with floors; Manhattan from a multi-tile footprint; spread; EN-16 timing; spawns start alert.

**Second chunk:** the ability-targeting wake marker (EN-14b preview), a real sound, an optional enemy bark (the bark system has trigger graphs for enemy events), the level pass.

**Play check (THJ, after chunk 1):** one Claw level, one Archer level, a Masher level (with sight 3 it holds its corridor like a wall until approached or hit; `LevelT1-C1-MasherBlockWay` has no units placed yet, so whoever populates it should decide whether its Masher starts Unaware), and one of the protect levels with "all start alert" on.

**Playtest signals:**

- *Working:* players spend the first turn positioning (Pass-by, Shield Up, lanes) and say *who* will start the fight; at least one deliberate wake per level (bell, shout, decoy, step in); no one asks why an enemy didn't move.
- *Failing:* more than 2 turns per level with nothing Alerted; "why did it wake?" more than once a session; HP lost per level falls sharply against today (pulling trivializes); players ignore Unaware enemies entirely and finish with a walk.

---

## Questions for THJ

**Q1. Scope: on in every level by default, or opt-in per level?**
- Context: existing Generic Levels were tuned for a rush from turn 1; the rule changes their pace and difficulty.
- Options: (a) on by default, levels opt out with "all start alert" (cost: a sample play check); (b) off by default, levels opt in (safe, but the rule rarely gets played); (c) a global switch in GlobalSettings plus (a).
- Recommendation: (c) — on by default, with a global switch for an instant A/B.
- Blocked: the default in chunk 1. Everything else continues.

**Q2. Sight distance: Manhattan through walls, or walking path?**
- Context: "not a line but a range". Path distance makes walls hide the family but flickers as units move.
- Options: (a) Manhattan, through walls and units (cheap, stable, drawable); (b) walking path distance (the danger zone's shape; costlier, unstable); (c) Chebyshev square.
- Recommendation: (a).
- Blocked: the sight check and the Shift sight area.

**Q3. Ranges: derived, with a floor and override?**
- Context: derived sight gives Worm and Masher 2.
- Options: (a) sight = walk + longest Attack reach, min 3; alert = half rounded up, min 2; per-prefab override; (b) the same without floors; (c) authored per type.
- Recommendation: (a).
- Blocked: values in chunk 1 (one constant each; easy to change later).

**Q4. Does waking spread?**
- Context: without spread, the player pulls enemies one at a time.
- Options: (a) chain within the waking enemy's alert range, at the moment of waking; (b) no spread; (c) authored groups.
- Recommendation: (a), plus the Black Claw's call waking its pack.
- Blocked: the spread step.

**Q5. Timing of a wake.**
- Options: (a) a wake in the family's turn acts on the next enemy turn; a wake during the enemy turn waits one more; (b) every wake acts on the next enemy slot it gets; (c) every wake costs a turn.
- Recommendation: (a): stepping in commits, and nothing woken by a reaction surprises the player.
- Blocked: the turn gate.

**Q6. Can an Unaware enemy do anything?**
- Context: matters for the Dark Shaman (heal, summon) and for prefabs with overridden sight.
- Options: (a) nothing at all; (b) anything except moving.
- Recommendation: (a).
- Blocked: the turn gate.

**Q7. What counts as "seen": decoys and protectees?**
- Context: Hide and Seek decoys and the Whitemother stag are units the enemy would attack.
- Options: (a) any unit hostile to the enemy, decoys and protectees included; (b) Bergsons and the allied Toba only.
- Recommendation: (a): decoys become a lure tool, and protect levels stay honest.
- Blocked: the sight check's unit filter.

Names (Unaware / Alerted) go to the narrative agent; THJ approves.

## Docs to update if approved

- `design/gdd/enemies.md`: new EN-12 to EN-17 (status Planned), a note on EN-1 (the call wakes the pack), the derived-values table with its Source line; the "How enemies think" section links EN-12.
- `design/gdd/combat-rules.md`: **CR-54** (the move-ghost wake marker; arcs only from Alerted or about-to-wake enemies, amending CR-39's text) and **CR-55** (Shift on an Unaware enemy shows the sight area in place of its move range, amending CR-43); the Shift tint table gains the sight tint.
- `design/gdd/missions-structure.md`: the level setting "all enemies start alert" and the levels that use it.
- `glossary.md` (narrative agent): Unaware, Alerted, sight, alert range.
- `design/level-chunks.md`: the "bell" and "sleeping" knobs now refer to EN-13 to EN-15.
- `decisions.md` (coordinator): one row per answered question.

## Risks

- Existing levels change balance (Q1's switch, the sample play check).
- The sight check has many entry points (EN-13's enemy-turn-start safety net).
- `AIRegressionTest` catalogs (keep the gate outside graphs, variables and AI abilities; never re-baseline).
- Core AI turn flow is a core system: the tech plan needs THJ's OK for that change (`tech/core-systems.md`).

## Gates

Compile / EditMode tests (all green except the known-red `AIRegressionTest.Baseline_MatchesCurrentAI`) / review / play check: yes, THJ's time after chunk 1 / docs above.
