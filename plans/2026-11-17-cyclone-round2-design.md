# Lucy's Cyclone, round 2: Eye of the Storm (design)

Size: L    Tier: 3 (changes an approved design; touches Synergies, the Masher and Queen, and the core walk rule CR-58)    Assigned to: miso-game-designer
Branch: `thj/cyclone` (scope: this branch until it merges)
Status: waiting on THJ

## Why

THJ's first play of the built Pulling Gale ([`playtests/2026-11-12-cyclone-play-check.md`](../playtests/2026-11-12-cyclone-play-check.md) › THJ Play Feedback, notes 1 to 11): it feels too weak, Fire Embers always win the AP, steering isn't fun, the cross drawing misleads, there are no previews, and the Masher is walled off. THJ has already decided D-547: the Steer's Gust pulls **and** hits like a Whirl.

## Goal

Make steering the Cyclone the most fun 1 AP Lucy has. One added rule, the board drawing it honestly, and every Cyclone hit previewed.

## Acceptance criteria (for the design, once approved)

- [ ] The new Steer can be said in one sentence and needs no new on-screen element beyond what it replaces.
- [ ] Every Cyclone action that moves or hits an enemy previews where it ends up and what damage it takes, lethal skull included (CR-37, CR-45, CR-46).
- [ ] No combo with the Cyclone kills a full-HP Dark Claw (16) from 2 AP on its own (Crippled guard, §5 Systems).
- [ ] The Masher and the Queen are never walled off by the Cyclone.
- [ ] Each of D-547's side effects has one stated rule (§8).

## Scope

In: the Steer rule (A), the cross drawing (B), the cast and Steer previews (C), the answer to note 7 (D), heavies against the Cyclone (E), the numbers, D-547's side effects.
Out: Trailing Gale and Second Cyclone (D-531, still not built); the AI regression test (stays known red); new chunk layouts (no grids changed in this plan).

## Touches

Systems: Cyclone (`CycloneEntity` and its partials, `CycloneSteerRules`, `CycloneSteerPreview`, `CycloneCrossView`, `CycloneWhirlPlanner`); `AEffectPusher` (a fixed straight move for carried enemies); `GridCell.CheckIfUnitWalkable` / `PlantedLetsPass` **(core, CR-58)**; AI path cost for heavies **(core, AI scoring)**; `MasherCounterRules` (unchanged code path, see §8).
USPs: Synergies (Watch, Tempest Bloom, Harmonic Slam), Family Roles (Watch).
Docs: GDD `characters/lucy.md` LU-4, LU-5, LU-6, LU-7; `enemies.md` EN-2, EN-3, EN-18; `combat-rules.md` CR-58; `design/cyclone-redesign.md`; `level-chunks.md` (chunks 1, 12, 13, 24 text only); `glossary.md` (narrative: retire "Gust").

## Approach

### 1. Problem and evidence

**The symptom:** "too weak, underwhelming" (5); "spending all AP on embers is always better; pull is very minimal" (10).

**The root problem:** the Steer is a **move with no consequence**. It relocates a 3-damage area, and enemies on the board barely change position. The approved design made the Cyclone a tool (principle 4, "it sets up the family"). But the only thing a Steer did to enemies was a 1-cell pull at the destination. Nothing happened on the way, and nothing came with it. THJ's notes 8 and 11 describe the missing fantasy exactly: the storm should **carry** what it has caught and **shove** what is in its way. Note 7 ("what is the catch if it pulls enemies inside itself?") and note 8 ("moving it keeps moving locked enemies?") show that THJ already plays it as a storm that holds enemies. The rules don't.

Evidence:
- **Numbers** (verified in assets): Whirl 3 × `Stat_DMG`, with Lucy's `Stat_DMG` 1 at base (`UnitBase.prefab`, not overridden on `Unit_Lucy`), so the Whirl hits for 3. Fire Embers: main 4 × plus sidewinder 3 × gives 7 per AP at base, 10 when Sheltered (`PrimaryAttackM` / `PrimaryAttackS`; that M is the main ember and S the sidewinder is read from the names). Dark Claw: 16 HP.
- **Built Steer:** 1 AP for a 1-cell pull of whatever stands on the destination's arms, and no damage (LU-6). That is 0 damage against Embers' 7.
- **EN-18 empties the cross:** enemies avoid ending a move on it, so the free end-of-turn Whirls rarely find a target twice.
- **Cyclone Power** ×1.2 / ×1.4 on 3 gives 3.6 → 4 and 4.2 → 4 (CR-20, half to even). At `Stat_DMG` 1 the second pip does nothing. That is a data bug.

### 2. Options compared, main problem (A)

| | A0. D-547 only (as decided) | A1. D-547 + bigger numbers | **A2. Eye of the Storm: the Steer carries** | A3. Plough aside (note 11 taken literally) |
| --- | --- | --- | --- | --- |
| Rule change | None beyond D-547 | Hit 3 → 4, arms 2 → 3, pull up to 2 | One added sentence: "Enemies beside the Cyclone move with it." | The Steer moves through enemies, pushing each one to the left or right |
| Player experience | 3 per touching enemy per Steer. Still a small area that moves; Embers still win (3 × N against 7) | Bigger numbers, same feeling: nothing memorable happens while steering | Every Steer rearranges the fight: drag two Claws into Linda's lane, shove one onto spikes, pull a pack off a sister. The Into the Breach feeling, in Lucy's voice | Pushes happen, but the side each enemy goes to is arbitrary or needs a second choice |
| Rules complexity | Lowest | Low (data only) | Low for the player (one sentence; the preview shows each outcome); medium inside the rules (per-step order, §5) | Higher: a side rule or a second aim |
| Implementation | Small (about 15 lines, report) | Data, plus a bigger AI danger zone | Medium: a planned, straight multi-cell move for carried enemies in `AEffectPusher`, the per-step plan in `CycloneSteerRules`, and the preview | Medium-high, plus the side choice |
| Risk | Stays underwhelming (THJ's note 5 stands) | Back toward "free damage does the killing" (Trail balance, 2026-11-11) | Combo runaway through Crippled (guarded, §5); preview trust | Ambiguity, misreads |
| USP | Neutral | Neutral, or against (free damage crowds out combos) | **Strengthens Synergies and Roles:** placement feeds Watch, Tempest Bloom and Explosive Crescendo | Similar to A2, but weaker |

**Leaning: A2.** All three critics agreed. A1's numbers stay available as levers.

### 3. The A2 rules (proposed)

> **Lucy's Cyclone holds a cross. It pulls enemies on its arms in and hits those beside it, after each enemy turn and every time Lucy casts or Steers it. Enemies beside it move with it.**

- **Whirl** (unchanged, LU-4): pull arm enemies 1 cell in, then reactions, then hit the touching cells.
- **Steer** (LU-6, changed): 1 AP, once a turn, up to 3 straight steps. **Then a Whirl** (D-547). "Gust" is retired: a Steer is "move, then Whirl".
- **Carry (new).** At each step of the Steer, every enemy on a touching cell moves one cell the same way. The order within a step:
  1. The enemy in front: if the cell ahead of it is blocked (wall, unit, a planted entity that blocks walking, the map edge), the Steer **can't take this step**. The cursor never offers that cell or any cell past it. A Steer never stops short after the player has picked its cell.
  2. Otherwise: the enemy in front moves, then the side enemies (a side enemy whose next cell is blocked stays where it is and drops out), then the Cyclone, then the rear enemy into the cell the Cyclone left.
  3. An enemy that is beside the Cyclone after this step rides along on the next step. An enemy two cells ahead on the path becomes the front enemy and gets shoved ahead.
- **Who rides:** the same units the pull moves. Immovable units (EN-3) and units larger than one cell never ride, and an Immovable unit in front blocks the step.
- **Carrying is not a push.** A carried enemy moves once, along a planned path, and lands once. Crippled's per-cell damage, hazards on the cells it crosses and pass-through reactions don't apply on the way. On landing, everything applies as for any move: a hazard on the landing cell fires, Watch fires if it lands in Linda's lane, and it wakes. Only the Whirl's pull is a push, as today.
- **Order after the last step:** the carried enemies land (Watch, landing hazards), then the Whirl's pull, then its reactions (Watch again), then the hit.

### 4. Problems B to E: options and leaning

**B. The cross drawing (note 2).** Verified in code: arm cells, touching cells included, carry two inward streaks; touching cells also carry the "3 ×" label (`CycloneCrossView`, `CycloneRules.TouchLabel`). On the touching cells the streaks point into the Cyclone, a pull that can't happen there.

| | B1. Eye and tips (leaning) | B2. Drop the drawing; Shift only | B3. Keep the streaks, drop the label |
| --- | --- | --- | --- |
| Board | The 4 touching cells get one swirl tint in the Cyclone's wind hue ("caught here: hit and carried"). The 4 arm tips (2 out) get one inward chevron each. No number | Nothing until the player holds Shift | Streaks stay on all 8 arm cells |
| Elements | Same count as today (streaks and label become tint and chevron) | One fewer | One fewer, but the misread stays |
| Risk | The tint must not read as "danger to the family": wind hue, not warm or red | Enemies avoid the cross (EN-18), so players need to see it | THJ's misread stays |

During any aim preview the always-on cross dims. During a Steer aim, the cross draws at the landing cell and hides at the current one: two crosses at once is the likeliest misread (UX critic).

**C. Previews (notes 3, 4, 6).** Verified: the old drifting Cyclone used the generic spawner preview, which showed an HP preview only on the unit standing on the aimed cell. Its moving and pass-by damage was never previewed. Since the cast now accepts only empty cells, that preview never fires. THJ remembers right, but it was narrow. Today the Steer preview shows the path, the landing cell, and a ghost with a step arrow for each pulled enemy, with no damage (`CycloneSteerPreview`).

| | C1. Full outcome preview (leaning) | C2. Damage only |
| --- | --- | --- |
| Cast aim | The cross drawn at the aimed cell; a ghost for each enemy the cast Whirl pulls; the damage segment and lethal skull **on the ghost** of each enemy the Whirl hits (an enemy pulled in from 2 out shows it on its ghost) | Damage segments on the enemies already beside the cell |
| Steer aim | Path and landing Cyclone; one ghost per enemy that will move (carried or pulled, one style, final cell only), joined to its current cell by a faint tether in the eye tint, which **replaces** the step arrow; damage and skull on the ghosts; a landing hazard that will fire is shown on the ghost; unreachable cells are never offered | Damage only, no ghosts for carried enemies |
| API | `GUnit.ShowDamagePreview`, `DamagePreviewRules`, `AbilityDamagePreview.SimulateApply` (as Tempest Bloom's preview does) | Same |

The preview never promises Watch kills: the HP bars show the Whirl hit only, as Tempest Bloom's preview already does for its own case.

**D. "What is the catch when it pulls enemies in?" (note 7).** From the design as built:
- **The catch for the enemies:** none that holds them. Pulled enemies take 3 and are free on their turn. EN-18 only keeps them from *ending* a move on the cross, so most walk off unless they can attack from there.
- **The catch for the player:** a pull brings enemies toward the family. The Cyclone stands within 3 of Lucy (15 HP), so a Whirl delivers Claws 1 to 4 cells from her, with Whirl damage that doesn't kill.

The gap THJ's notes point at is that nothing "locks" them. A2 answers it on Lucy's turn: what is beside the Cyclone comes with it. That makes the end-of-turn Whirl the setup for the next Steer, and EN-18 keeps enemies already standing beside it from being made to leave. A full **hold** ("enemies beside it can't walk") is a lever, not the plan: Q4.

**E. Heavies (note 9).** Verified: CR-58's pass check reads only the faction relation (`PlantedLetsPass`). The Masher's counter walk and the Queen's charge (`AEffectTransporter`, Walk mode) both stop at the Cyclone. The Queen stops on the cell before it and applies her end-tile effects there.

| | E1. Heavies burst it (leaning) | E2. Heavies can attack it | E3. Leave as built |
| --- | --- | --- | --- |
| Rule | "Heavy enemies walk through the Cyclone. It bursts: one last hit on everyone beside it and on the heavy, then it's gone." | The Cyclone gets HP and can be targeted | Walled off |
| Cost | Core: a per-mover exception in the walk check (CR-58), an AI path that lets heavies cross, a burst on enemy entry | A target, an HP bar, AI scoring: new UI | None |
| Feel | A big body tears through a child's storm, and the storm hits back as it goes. A trade the player can bait | Clunky; breaks "nobody targets it" | THJ: the Masher becomes useless |

Heavy = Immovable (EN-3) **or** larger than one cell, read from existing data with no new tag: the Masher, the Queen and the Deev (which never walks). The burst is a hit with no pull, and it leaves the cast's cooldown running as before.

### 5. Lens notes (A2 with B1, C1, E1)

**Creative.** *Target:* Lucy steers a storm that the family plays around. Every Steer leaves the board looking different, and the family cashes in on it. *The moment:* the end-of-turn Whirl drags two Claws next to the Cyclone. On her turn Lucy Steers it three cells, the Claws ride with it into Linda's row, Watch fires twice, and the closing Whirl hits both. One sister sets up, the other finishes, in one family turn. *Over the bar:* a Masher crashes through the storm and the storm bursts on it and its escorts. A child's storm, broken by a brute, still hits back (warmth against dread). The creative critic wanted per-step pushes (hazards and Watch on every cell crossed) for bigger moments. I side with systems (see below) and keep the big moment on landing, where the preview can show it.

**Systems.**

*Levers:*

| Lever | Start | Range |
| --- | --- | --- |
| Hit per Whirl (cast, Steer, end of enemy turn) | 3 × | 3 to 4 |
| Cyclone Power | flat 3 / 4 / 5 (base factor per level, not ×1.2 / ×1.4) | — |
| Arms / pull | 2 / 1 | arms 3 / pull 2 if still flat |
| Steer | 1 AP, once a turn, 3 steps | 2 to 3 steps |
| Cast | 1 AP, range 3, cooldown 4, 3 pips | unchanged |
| Howling Gale | Weak 2 turns on every enemy a Cyclone hit lands on (Whirl, Steer or burst) | unchanged |
| Burst | 1 hit (same value) to the heavy and to each enemy beside | — |

*AP against Embers (base stats, one enemy faction):*

| Lucy's 2 AP | Damage | Also |
| --- | --- | --- |
| Embers ×2 | 14 (20 Sheltered) | Picks targets |
| Cast + Steer | 3 + 3 to each enemy beside both times; typical 2 enemies gives about 12 | Up to 4 enemies moved up to 3 cells; Watch triggers; the bunch for John and Linda; Weak with Howling Gale |
| Steer + Embers | 3 × N + 7, about 13 | Relocation |
| A1 numbers instead | 4 × N per Whirl, about 16 | No relocation |

Damage stays under Embers; the value is placement. That matches the redesign's principle 5 and the Trail balance's "no free kills". The hit stays 3 for the first play.

*Interactions:*
- **Crippled** (4 × per cell pushed) would make a carried, Slammed enemy take 12 + 3 = 15 to 16: four Claw kills for 2 AP. "Carrying is not a push" closes this; the Whirl's 1-cell pull still pays 4 × once, as built.
- **Watch** has no per-round cap (LI-11), so one Steer can spend 4 or more arrows. The quiver is the limit.
- **Tempest Bloom:** unchanged.
- **EN-18:** enemies already beside the Cyclone aren't made to leave, so most Steers have riders.

*Failure cases:*
- Cursor offers a cell the Steer can't reach: refuse it instead.
- Front enemy blocked at once: the Steer can still go other ways.
- Two enemy factions give two end-of-turn Whirls (as built).
- The Masher's counter walk may burst a Cyclone it wasn't aiming at: accepted as readable ("the Masher smashes through").
- The Queen's charge lane: casting into it now trades the Cyclone for one hit and doesn't cancel the charge. That's fine.

*Implementation (verified):* `TryMoveTo` searches its own route through `FindPathTo`, so a carried enemy needs a planned straight move of its own length (a rider that drops out or joins late has a shorter path). That is size M in `AEffectPusher`. Making the Steer's Whirl hit is about 15 lines, and Masher suppression and Weak come along (`IsCycloneCast`).

**UX.**

| When | Shown |
| --- | --- |
| Always | Eye tint on the touching cells, chevrons on the arm tips, pips. Dimmed under any aim preview |
| Cast aim | The cross at the cursor, ghosts for pulled enemies, damage and skull on ghosts |
| Steer aim | Only reachable cells; path, landing Cyclone and cross at the landing; one ghost per moving enemy, with a tether; damage and skull on ghosts; landing hazards shown |
| Heavy's turn coming | When a heavy's intent path crosses the Cyclone, the Cyclone wobbles and its pips flicker. This reuses the sprite and pips: no new element |
| Hover a heavy | The burst hit shows as a normal damage segment |

*Clicks:* unchanged (one button, one cell).

*Likeliest misread:* riders that join mid-path, since the sentence predicts "beside it at the start". The tether at the source covers it.

*Learning:* hint line "Steer drags enemies beside it, then it Whirls." The first onboarded Steer should have one side rider and one rider that joins mid-path.

*Budget check:* one added rule (carry). New on-screen elements: the tether, which replaces the step arrow; the eye tint and chevron, which replace the streaks and label; the heavy wobble, which reuses the sprite. Net new: none.

### 6. USP check

- **Family Roles:** strengthened. Carried enemies land in Linda's lanes, so Watch fires on Lucy's turn by her choice. Lucy's follow-up is unchanged (it never answers her own actions or a Cyclone hit).
- **Synergies:** strengthened. Tempest Bloom gets bunched targets on the arms; Explosive Crescendo and Shield Flare get bunches delivered. Harmonic Slam with the Cyclone stays a good combo but isn't a runaway (Crippled guard).
- **Duos:** neutral on purpose.
- **Home:** neutral.

### 7. Critics

The `miso-design-critic` agent type isn't installed in this session, so the three lens critiques ran as read-only Explore agents with the same brief, one lens each, without seeing each other.

| Critic | Strongest point | What I did |
| --- | --- | --- |
| Creative | The memorable moment is the drag, so let each carried step work like a push (hazards and Watch on every cell). A silent stop-short eats the input. "Breaks" punishes; make it a burst that pays | **Rejected** per-step pushes (the systems critic's Crippled numbers); the moment stays on landing, where it can be previewed. **Took** "no stop-short" (the cursor refuses those cells) and **took** the burst |
| Systems | Crippled × carry is a dominant combo (15 to 16 per Claw, four kills for 2 AP); fix the per-step order; `TryMoveTo` reroutes, so carried enemies need a planned straight move; "max 4" is automatic | **Took all of it:** "carrying is not a push", the order in §3, the M-size move, dropped "max 4". Took the heavy definition (Immovable or large, no new tag) |
| UX | Two crosses during a Steer aim; mid-path joiners are the misread, so add a tether that replaces the arrow; damage on the ghost, not the real unit; the heavy path through the Cyclone looks like a bug, so make the Cyclone wobble; show landing hazards | **Took all of it.** Rejected nothing; the per-step ghosts and carried-only tint it warned against weren't in the plan |

What changed my mind: Crippled (I had not counted it) and the tether (I had planned a step arrow plus a ghost, which is busier).

### 8. D-547 side effects

- **One rule: "No Cyclone hit is anyone's action."** This covers the Whirl, the Steer's Whirl and the burst. So no Masher counter (D-537 extended; it is already automatic in code, because every hit is credited to the cast) and no Lucy follow-up (unchanged). Crippled damage from a pull gets the same credit.
- **Kill credit:** to Lucy's cast, like every Whirl (XP, gold, stats, barks, the sisters' tally once per kill).
- **Howling Gale (D-545):** Weak on every enemy a Cyclone hit lands on, the Steer's and the burst's included. Its working text already says "every enemy it hits" (D-544), so no text change. Two hits in one turn only refresh Weak.
- **Waking:** unchanged; a hit or a carry wakes.
- **Visuals and log:** the Steer's Whirl uses the full Whirl beat (swell, streaks, burst), and the log reads "✦ Whirl · Lucy: carried N, pulled N, hit M". The Gust line goes.

### 9. Plain bugs and data slips (no design needed)

1. **The cast lost its damage preview.** The generic preview only reads the aimed cell's occupant, and the cast now accepts only empty cells. C1 replaces it.
2. **The Steer preview shows only after the cursor moves** when the cursor already sat on the landing cell (play-check list, C3).
3. **Cyclone Power's second pip is dead** at `Stat_DMG` 1 (3.6 and 4.2 both round to 4). Fixed by the 3 / 4 / 5 values (data).
4. **The touching-cell streaks point inward** to a cell nobody can be pulled into. This is a drawing slip against LU-4's own rule (B1 fixes it).

Everything else in this plan (carry, heavies, the burst, hold) is design.

### 10. Recommendation

**A2 + B1 + C1 + E1**, with the §5 starting values (hit 3, Cyclone Power 3 / 4 / 5, arms 2, pull 1, Steer 1 AP, once a turn, 3 steps), D-547 folded in as "Steer = move, then Whirl", and "carrying is not a push".

**Playtest signals:**
- **Worked:** THJ Steers on most turns while the Cyclone is out, and on at least one turn chooses a Steer over Embers *for placement* (Watch, Bloom or a hazard). He describes a Steer moment unprompted. No Claw dies to the Cyclone alone at full HP. The Masher crosses or bursts the Cyclone at least once in a Masher level.
- **Failed:** Steers made only for the 3 damage (raise the hit to 4); "why did it stop / not go there" (preview trust); carry used every turn to strand enemies out of reach (consider a shorter Steer, 2 steps).

## Questions for THJ

**Q1. Should the Steer carry enemies beside the Cyclone (Eye of the Storm, A2)?**
- Context: notes 5, 8, 10 and 11. This is the main change; it amends LU-6 and the approved design §4.4. It strengthens Watch and Tempest Bloom.
- Options:
  - (a) A2, carry (medium build);
  - (b) A1, D-547 + numbers only (data);
  - (c) A3, plough aside (medium-high, adds a side choice);
  - (d) A0, D-547 as is.
- Recommendation: (a). It is the only option that makes a Steer change the board, with one added sentence.
- Blocked: the Steer tech plan, the preview spec, the GDD LU-6 rewrite. The D-547 hit (about 15 lines) can be built meanwhile; it is part of every option.

**Q2. Is carrying a push (Crippled damage, hazards and Watch on every cell crossed) or one landing?**
- Context: the creative and systems critics disagree. Per-cell is louder, but Harmonic Slam plus a 3-cell carry gives 15 to 16 per Claw: up to four kills for 2 AP.
- Options:
  - (a) one landing; only the Whirl's pull is a push;
  - (b) per-cell push;
  - (c) per-cell for hazards only.
- Recommendation: (a). It can be previewed and has no runaway combo; the big moment still lands in Linda's lane.
- Blocked: the carry implementation.

**Q3. Should the Masher and the Queen (and any heavy: Immovable or larger than one cell) walk through the Cyclone, bursting it?**
- Context: note 9, EN-2, EN-6, and the core walk rule CR-58 (a core change, Tier 3).
- Options:
  - (a) E1, walk through; the Cyclone bursts with one hit on the heavy and on everyone beside it, then is gone;
  - (b) the same but no burst hit ("breaks" only);
  - (c) heavies can attack it (adds HP and targeting);
  - (d) leave as built.
- Recommendation: (a). It is a trade the player can bait, and it reuses the existing Immovable and size data.
- Blocked: a core exception in `CheckIfUnitWalkable` and the AI path cost (both need your OK under `tech/core-systems.md`). Nothing else waits on it.

**Q4. Should enemies beside the Cyclone also be held (can't walk away)?**
- Context: notes 7 and 8 suggest you pictured enemies "locked". The built rule holds nothing. Hold would make the end-of-turn Whirls hit the same enemies again (up to 12 per enemy) and neutralise up to 4 melee enemies.
- Options:
  - (a) no hold; A2's carry is the lock on Lucy's turn;
  - (b) hold (a second new rule, a status-like state);
  - (c) hold only until the next family turn.
- Recommendation: (a) for the first play. Keep (c) as the lever if A2 still feels weak.
- Blocked: nothing.

**Q5. Should every Cyclone hit (Whirl, Steer, burst) be "no one's action" (no Masher counter, no follow-up), and should Howling Gale apply on all of them?**
- Context: D-547's side effects on D-537 and D-545. The code already does both, because every hit is credited to the cast.
- Options:
  - (a) yes, one rule;
  - (b) the Steer's hit provokes the Masher (it's Lucy's deliberate act).
- Recommendation: (a). One rule, no text change.
- Blocked: the GDD wording only.

**Q6. Should "Gust" be retired, with the Steer described as "move, then Whirl", and Cyclone Power changed to a flat hit of 3 / 4 / 5?**
- Context: fewer terms (glossary, narrative agent), and Cyclone Power's second pip is dead today.
- Options:
  - (a) both;
  - (b) keep Gust as the Steer's name for its Whirl;
  - (c) keep ×1.2 / ×1.4.
- Recommendation: (a).
- Blocked: texts (narrative pass) and one data value.

## Docs to update if approved

- **GDD `characters/lucy.md`:**
  - LU-4: the Whirl also closes every Steer.
  - LU-5: "no Cyclone hit is anyone's action"; the burst.
  - LU-6: Steer = carry, then Whirl; Gust retired; the preview.
  - LU-7: heavies pass and burst it.
  - New **LU-8**: carry, if it reads better as its own rule.
  - Value table: Cyclone Power 3 / 4 / 5.
  - Howling Gale row.
  - Q4 texts.
- **GDD `enemies.md`:**
  - EN-2: the counter ignores all Cyclone hits.
  - EN-3: never carried.
  - EN-6: the Queen's charge passes and bursts it.
  - EN-18: heavies cross the cross.
- **GDD `combat-rules.md`:** CR-58, the heavy exception to pass-through.
- **`design/cyclone-redesign.md`:** an as-built note for round 2 (§4.4, §4.6, §6, §7).
- **`level-chunks.md`:** chunks 1, 12, 13 and 24, text only ("Steer drags them into...").
- **`glossary.md`:** narrative agent: retire Gust; "Eye of the Storm" as a possible name, a proposal.

## Risks

- **Preview trust:** the carry's per-step order must be the same in the planner, the preview and the execution (one planner, as the Whirl already does).
- **Core changes:** the walk exception and AI path cost need THJ's OK, each in its own commit.
- **Creep:** if hold, per-cell pushes and higher numbers all come in, the Cyclone tips back to free kills. Change one lever per play.

## Gates

Design only: THJ answers Q1 to Q6 → tech plan (coordinator) → build → compile, tests, review → THJ play check (yes, needs his time) → docs above.
