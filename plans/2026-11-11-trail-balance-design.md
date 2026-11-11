# The Trail: a balance round where the family's combos are the way through

Size: L (balance)    Tier: 3 (global Duo and Cyclone numbers; first-hour game feel; THJ decides)    Assigned to: miso-game-designer
Branch: `thj/after-hearth`, scope **all**. The Trail values live in the four `GB_m2-*` levels (onboarding content, `main` once merged). The Duo and Cyclone values are global assets: they reach every branch that merges them (`thj/home-test` only when it takes `main`).
Status: **waiting on THJ** (draft 2026-11-11, critics reconciled below)

## Why

THJ, after playing the C3 Trail rebuild (D-512): "Balance. Also tweak it to support synergies." The rebuilt levels set up the situations they were built for, but the family's free and area damage removes their cost, and enemy hits are too small to make any cost felt ([`playtests/2026-11-11-trail-c3-play.md`](../playtests/2026-11-11-trail-c3-play.md)).

## Goal

On the Trail, a careless line visibly costs a hero's HP and a combo line between two or three family members wins cleanly, using value changes only: no new rule, no new on-screen element, the revision-2 layouts kept.

## Acceptance criteria

- [ ] In THJ's next timed run (each pick, both routes), at least one enemy phase per level lands **6 or more on one hero** when he plays the Hearth habit (fire everything at the nearest target).
- [ ] A combo line keeps every hero except John to **one Claw hit (6) or less** per level, and the level's total to at most half of what the careless line cost. John's anvil and the Tracks' ★ A are paid in his HP on purpose (up to about 16 on the Tracks), and that is the only exception.
- [ ] No Trail kill comes from Lucy's Cyclone alone: the combat log shows no Cyclone kill of a Claw above 3 HP. Kills through it by Tempest Bloom don't count against this, if Q4 opens it.
- [ ] Chained Assault never kills a full-HP Claw with one target slot (log: no Duo line `16→0` on a target hit once).
- [ ] A Synergy or Duo other than Chained Assault fires in **every level** of the run (Papa's Shelter, Shield Flare, Catch & Return, Hide and Seek, the Dance, the Footrace, Tempest Bloom if Q4), and THJ says a combo was the reason a fight went well.
- [ ] Family down 0 in THJ's runs, and M2 stays within about 12 minutes at his pace (C3: 7m30s and 5m26s).
- [ ] No new rule, status, number display or UI element.

This replaces revision 2's "at least two enemy actions land per level" with a criterion that rewards a combo line for avoiding them: the round's aim (D-512) is that the combo is the way through.

## Scope

In: enemy tier and per-instance HP on the four Trail levels; the Mark–Lucy Duo's damage and its preview (Q5); the Cyclone's damage and cooldown, as a stopgap ahead of its redesign; Tempest Bloom granted for M2 (Q4); the walkthroughs; the playtest signals.
Out: layouts (revision 2 stays, D-511, except one conditional knob below), Family Role rules and numbers (the rethink, D-466), the Cyclone redesign's rules and its open questions Q1–Q5 (not answered here), the River and Ridge (Tutorial tier, untouched by the tier change), new enemy types, text.

## Touches

Systems: level prefabs `GB_m2-trailhead`, `GB_m2-tracks`, `GB_m2-blood`, `GB_m2-pile` via the grid blocks and **Wire Search: Trail** (`SearchWiring.Trail.cs`, editor code) and `SearchTrailTests.cs`; ability data `Mark_Lucy_MARK_Duo_Effect_AttrMod.asset`, `Lucy_Cyclone_Effect_AttrMod.asset`, `Lucy_Cyclone_Ability.asset`; the M2 run-upgrade grant of `RU_LindaLucyCycloneSpreadUnlock` (Q4, the Memory 4 wiring pattern). No runtime code, no AI code, in the values. Q5 alone is a code change (`AbilityDamagePreview`, possibly core; to check against `tech/core-systems.md`).
USPs: Synergies and Duos (the point of the round), Family Roles (as built; untouched), Home (neutral).
Docs: see [Docs to update](#docs-to-update).

---

## Problem and evidence

**Symptom (the logs):** six levels, ten enemy hits, never more than 6 to one hero in a turn; the Trailhead solved by one Duo; the bell's cost erased; the Blood reach ignored.

**Root problem: on the Trail the family's damage that needs no decision is larger than the enemy's threat.** Three things in today's data make it so, and the revision-2 design assumed numbers that were wrong for two of them:

1. **Free damage does the killing.** Lucy's Cyclone (7 per contact, hunting toward units) and Linda's Watch (6 per arrow) dealt about 56 damage each over the two runs; Lucy's follow-up added about 29. None of it was a choice made on the family's turn. Watch + follow-up is 12 on any Claw that ends a move in Linda's lane within 3 of Lucy; any Claw already hit by an area attack dies to it.
2. **Chained Assault is a solo wipe, not a combo.** Its per-target damage is **15 × mash** (Lucy's sidewinder 3 + Mark's ghost **12**, read in the asset), so any mash above ×1.07 kills a full 16-HP Claw per slot. Revision 2 assumed 11 (the GDD's "8 ×" for the ghost) and wrote "at 16 HP a Duo cripples three". It was wrong in the data before it was wrong in play.
3. **Enemy hits are too small to make a mistake visible.** The Trail plays at Early tier: a Claw hits 6 × 0.75 = 4.5 (logged 4; 3 through Shield Up), the Black Claw 10 × 0.75 = 7.5 (never landed). Against 15 to 32 HP and two potions, nothing a Claw does in one enemy phase matters.

Revision 2's layouts are not the problem: every beat fired as designed (both arrivals on turn 2, the bell taunted the pack, the Pile search revealed both sides).

### Evidence (verified in the logs and the assets unless marked)

| Evidence | Where | What it shows |
|---|---|---|
| Chained Assault `→ #01-00, #00-01, #00-01`: 16 and 16, both dead at full HP, turn 1 | Log 145831, Trailhead R1 | The Duo alone decided a two-front level; the third slot can repeat a target |
| Mark's ghost hit `baseFactor 12 × Stat_DMG`; trigger `radiusV 5`, cooldown 2, three effect slots; Lucy's part spawns her sidewinder embers (S1 to S3) | `Resources/Abilities/Cooperation/Mark_Lucy/Mark/Mark_Lucy_MARK_Duo_Effect_AttrMod.asset`, `Trigger/Mark_Lucy_Duo_Ability.asset`, `Lucy/Mark_Lucy_LUCY_Duo_Ability.asset` | 15 per slot at mash ×1.0. The GDD's "8 ×" and "within 4" are out of date (sidewinder value 3 assumed from the S-ember effect name; the projectile wasn't traced) |
| Cyclone damage `baseFactor 7`; cooldown 2; `radiusV` 4; entity hunts (TowardsUnits, move 3, life 5) | `Resources/UnitSpecific/Player/Lucy/Abilities/Cyclone/Lucy_Cyclone_Effect_AttrMod.asset`, `Lucy_Cyclone_Ability.asset`; entity facts from the Cyclone tech plan's code read | Contact and cast deal the same 7; the Cyclone moves into Claws on its own as well as being walked into |
| Cyclone lines: 7, 14 (one Claw, one move), 7, 7 "friendly fire", 7, 7, 4 (kill), 2 (kill); two of the three Black-Claw-pack deaths on the Tracks | Both logs | About 56 damage over two runs from a single cast per level, no decision after the cast |
| Watch: 9 shots, about 56 damage; 5 of them followed by Lucy's follow-up | Both logs | The approach is where Claws die; most of those Claws had taken an area hit first |
| Claw attack `6 × Stat_DMG`, one per turn (`apConsumptionType` all); Black Claw `10 ×`; tier rows `Stat_DMG` 1 / 0.75 / 0.5 / 1, `Stat_HP` 1 / 1 / 0.6 / 1.2 | `DarkClaw_Ability_Attack_Effect_AttrMod.asset`, `BlackClaw_Ability_Attack_Effect_AttrMod.asset`, `Resources/Factions/EnemyFaction.asset` | Early is "Standard HP, three-quarter damage". Standard tier is the same HP with full damage |
| Trail levels `enemyTier` 1 (Early); River, Ridge and the four Hearth memories `enemyTier` 2 (Tutorial) | The `GB_*` prefabs | A Trail tier change touches no other onboarding level |
| Tempest Bloom (`CycloneArrowScatter`) and Sisters' Rivalry `unlockedByDefault 0`; Bond reaches Lv 2 at the Yard, after the Trail (BO-2); the Tracks log shows Linda's bow crossing the Cyclone without splitting | `Resources/Unlockables/UnlockableSet.asset`; log 150621 Tracks R1 | The sisters have **no** open Synergy on the Trail; their Duo is locked by the level (D-470) |
| Catch & Return `unlockedByDefault 1` | Same asset; `SearchRidgeTests.CatchAndReturnIsOpenByDefault` | Open on the Trail with the Mark pick, never used in C3 |
| Shield Flare, Hide and Seek, the Dance, the Footrace, Catch & Return: 0 uses in six levels; Papa's Shelter on 4 times, by accident of position | Both logs | Solo and free damage was always enough; no combo was ever needed |

**Where revision 2's assumptions failed.** "A Duo cripples three": the ghost is 12, not 8. "Careless Pile about 12 taken": that figure assumed Claws hitting at full value and no Cyclone; at 4.5 per hit, with the Cyclone and Watch taking the approach, the worst enemy phase in six levels was 6.

---

## The family's combos on the Trail, as built

The Trail squad is Linda, Lucy and one pick (Mark or John).

| Combo | Kind | Pair | Open on the Trail? | C3 uses |
|---|---|---|---|---|
| Lucy's follow-up on another's hit (6) | Role, cross-hero | Lucy + anyone | Yes | 7 |
| Watch on an enemy pushed into Linda's lane (Shield Dash, Vault, Command) | Role, cross-hero (D-318) | Linda + John or Mark | Yes | 1 |
| John's guard (redirect at ×0.5) | Role | John + a sister | Yes | 0 (John took hits directly) |
| Mark's counter | Role | Mark + whoever is hit | Yes | 1 |
| **Chained Assault** | Duo | Mark + Lucy | Yes | 1 (the wipe) |
| **Catch & Return** (12 out and back on each enemy between) | Synergy | Linda + Mark | Yes, open by default | 0 |
| **Family Footrace** | Duo | Mark + Linda | Yes | 0 |
| **Papa's Shelter** (Lucy next to John: 3 embers, 10) | Synergy | John + Lucy | Yes | 4, never planned |
| **Shield Flare** (ember into Shield-Up John: diagonal copies, range 2) | Synergy | John + Lucy | Yes | 0 |
| **Hide and Seek** (2 decoys) | Duo | John + Lucy | Yes | 0 |
| **John–Linda Dance** | Duo | John + Linda | Yes | 0 |
| Tempest Bloom, Sisters' Rivalry | Synergy | Linda + Lucy | **No** (Bond Lv 2 node, after the Trail) | — |
| Marks-Sisters | Duo | Linda + Lucy | **No** (locked by the level, D-470) | — |

**The combos the Trail should make the efficient answer:**

- **Mark pick: "start it, then finish it together."** Linda opens a group (Explosive 8 on a cross, or the bow), then Chained Assault finishes up to three (10 per slot after the change below). Catch & Return turns one arrow into 12 on every Claw between Linda and Mark, and gives the arrow back. Mark's Vault push into Linda's lane sets up Watch.
- **John pick: "Papa's anvil."** John stands between the sisters with Shield Up; his guard takes hits meant for a sister within 2 at ×0.5 (×0.3 with Shield Up), arming Wrath; Lucy stays next to him (Papa's Shelter, 10 per Embers); Wrath pays out on a Shield Dash that pushes Claws into Linda's lanes. Hide and Seek decoys soak a hit apiece. Shield Flare pays when Claws queue on his diagonals.
- **Both: Lucy's follow-up stays the glue.** It already fires only on another member's hit; nothing here changes it.
- **The sisters: Tempest Bloom, if THJ opens it for M2 (Q4).** Lucy places the wind, Linda shoots through it. Without Q4 the sisters have no Synergy of their own on the Trail.

Nothing here raises a Synergy's numbers. The combos become the efficient answer because the solo and free damage that made them unnecessary comes down, and because an enemy hit is now worth preventing.

---

## Options compared

| | A. Per-level knobs only | **B. Trail level values + two global ability values** | C. AI and rule changes | D. Wait for the Cyclone redesign and the roles test |
|---|---|---|---|---|
| What changes | Trail tier Standard; Tracks overrides removed; a Claw added per side; the Cyclone and the Mark–Lucy Duo locked on the Trail with `LevelAbilityLock` | Trail tier Standard and Tracks overrides removed (Trail-only), **plus** Chained Assault's ghost 12 → 7 and the Cyclone's damage 7 → 3 and cooldown 2 → 4 (global data; the Cyclone pair only until its redesign lands) | The Cyclone redesign's C1 + C2 brought forward (anchored, AI avoids its cross); AI treats Linda's lanes as danger; Chained Assault can't repeat a target | Nothing now; replay after the redesign and the roles test |
| Player experience | Harder, but the two loudest family tools vanish on the first post-Hearth mission | Claws that reach you hurt; the Duo is a finisher; the Cyclone wounds and blocks; combos win | Cleverer enemies; Watch has to be set up with pushes; the Cyclone becomes a wall and a pull | THJ's notes stand for weeks |
| New things to track | 0 (but two tools gone) | 0 | 0 rules for the player; enemies behave differently | 0 |
| Build | Data + wiring | Data + wiring; three asset values | Core AI scoring on the worker thread, grid walking, turn hold (the redesign's Q4); weeks | 0 |
| Risk | Duos and Lucy's identity hit on the mission that should show them | The global values touch the Hearth (Memories 2 and 4), the River and M4; Standard tier on a cold player | Big; first-hour difficulty from AI is hard to read; moves `AIRegressionTest` | No progress on the challenge |
| USP effect | Duos −, Synergies − | Duos + (a combo, not a nuke), Synergies + (needed again), Roles neutral | Synergies + (pull + Watch, push + Watch), Roles changed indirectly | Neutral |
| Other missions touched | None | Duo: Hearth Memory 4, M3 "No More Waiting" (classic). Cyclone: Hearth Memories 2 and 4, the River, M4, any Lucy level | All levels (AI) | None |

**Recommended: B.** A spends the USPs to buy difficulty. C is right in the long run for the Cyclone (the redesign is already planned and owns it) but too big and too AI-dependent for a balance round. B uses three asset numbers and two level settings, all reversible by a revert, and two of the three asset numbers are the Cyclone redesign's own, so they don't move again when it lands.

---

## Lens notes

### Creative

**Target experience.** The first time after the Hearth that the family is in real danger and gets out of it *together*: Papa plants his shield between his daughters and the Claws break on him; Linda opens the pack and Mark and Lucy finish it as one; a careless turn leaves Lucy bleeding into the next level. Warmth against dread: the dread is a Claw reaching Lucy for 6; the warmth is the family arranging itself so it doesn't.

**The moment designed for:** the Trailhead with John. Turn 1, Lucy steps next to her father, he raises his shield, Linda blasts the far pair. Enemy turn: three Claws come, John's tether arcs to each daughter, he takes every hit at a third, Wrath glowing. Turn 2, he swings with Wrath ×2 and the fight is over. That is a family role, a Synergy and a protective instinct in one picture, and it only reads as good play if the hits he took would have hurt the girls.

Secondary: the Tracks' bell rung on purpose on Papa; Linda's Explosive followed by Chained Assault finishing all three on the cross ("we did that"); the Pile, where a careless search costs a sister most of her HP in one enemy turn.

**Originality.** Raising enemy damage is the genre default. What is Miso's own is where the damage is aimed: every value here makes a *family* answer better than a solo one, and the combos (the anvil, start-and-finish, catch and return) are ones only this family has.

### Systems

**Kill price, after the change** (16-HP Claw, mash ×1.0 unless noted):

| Source | Today | After | Kills a fresh Claw alone? |
|---|---|---|---|
| Watch + follow-up (free, enemy phase) | 12 | 12 | No (4 left) |
| Cyclone contact (free) | 7 | 3 | No |
| One Chained Assault slot | 15 (×1.5: 22) | 10 (×1.5: 15) | **No, at any mash** |
| Two slots on one target | 30 | 20 | Yes: "kill one, or finish three" |
| Explosive + one Duo slot | 23 | 18 | Yes (each on the cross) |
| Bow + follow-up + one Duo slot | 27 | 22 | Yes |
| Catch & Return (out and back) | 12 | 12 | No; + follow-up 6 = yes |
| **Watch caught by Mark** (enemy phase: Watch out and back + follow-up) | 18 | 18 | **Yes**, and the arrow goes back into the quiver (systems critic: Watch uses `LindaAttackArrow`, which Mark's catch accepts). Limited by FTP (1 per Watch), not arrows. Kept on purpose: it needs Mark planted down Linda's lane as bait and the catch pressed, so it is a set-up three-member combo, the kind this round wants. To watch in play: if a "Mark down the lane" turtle wins the Tracks and the Pile untouched, it is the first combo to tax |
| Tempest Bloom (Q4): bow through the Cyclone | — (shut) | 6 per copy, three copies | No alone; a copy + the follow-up or a Duo slot = yes |
| Lucy Embers ×2 (her whole turn) | 14 | 14 | No |
| Lucy Embers ×2 next to John (Shelter) | 20 | 20 | Yes, a combo |
| Mark Blitz ×2 (Focus) | 17 | 17 | Yes, his whole turn |
| John sword with Wrath ×2 | 13.6 | 13.6 | No; + follow-up = yes |

**Threat, after the change** (Standard tier): Claw 6 per hit (John with Shield Up 4; through his guard 3, with Shield Up 2); Black Claw 10 (6 on Shield-Up John, 5 through his guard). Two Claws on Lucy = 12 of 15. A careless enemy phase is one sister at a third of her HP. (Guard ×0.5 and Shield Up ×0.6 multiply on `Stat_DR`, verified by the systems critic.) The Cyclone's Weak (×0.6 enemy damage) is locked behind Howling Gale (`Lucy_Cyclone_Effect_WeakCompound` `lockedByDefault 1`, `_LucyCycloneWeak`), so it doesn't soften these numbers in base play.

**FTP is the combos' price.** The pool carries between levels and refills only by pass-by, Shield Up (+1) and the Trinket (CR-10 to CR-12). Every role press costs 1 and a Duo 2, so the Mark pick can reach the Pile short of FTP if it presses everything; the John pick gets 1 back per Shield Up. That is a real choice (spend now or keep the Duo for the Pile) and stays as built; the playtest watches FTP at the Pile's start.

**Levers in order** (if play disagrees): (1) the Cyclone path (Q3); (2) the Pile back to Early if a cold player loses there; (3) the ghost 7 → 8 if the Duo feels flat (a near-perfect mash then kills); (3b) the Tracks' leader 30 → 40 if it never lands a hit; (4) a third Claw per side at the Trailhead if its careless line still costs under 6; (5) the roles rethink's test, which the Trail will feel most (Watch and the follow-up).

**Interactions.**
- *Cyclone redesign (its Q1–Q5 open with THJ):* the stopgap uses the redesign's own numbers (Whirl 3, cooldown 4), so when it lands nothing here moves. Its C2 (enemies can't enter the Cyclone and the AI avoids its cross) changes level geometry: **the Trailhead's rock on 6,0 makes 6,1 a one-cell choke that a Cyclone would seal for three enemy turns** (Lucy cast on 6,1 in the John run). If the redesign is built, move or remove that rock in the same change (conditional knob, below). The Blood's two chokes are sealed on purpose (★ A). The Tracks' and the Pile's open floors have no one-cell choke.
- *Roles rethink (D-466):* untouched. If "kept AP" lands, Watch and the follow-up fire less and the Trail gets harder; first lever back: the Pile at Early.
- *Tier change and the AI:* the AI's scoring reads damage values, so its choices on the Trail may shift slightly (to watch in play, not designed against). `AIRegressionTest` may move with the Cyclone data (its catalog names both Cyclone paths): it stays known red and is never re-baselined without THJ.

**Dominant strategies checked.**
- *Duo on a fresh target* (two slots, 20): kills one, and the Duo's cooldown is 2; it is now one good action, not a level.
- *Turtle in a corner and let Watch + follow-up do it* (Tracks, Pile): fresh Claws survive 12 and hit for 6; the corner is where two of them reach the same sister.
- *John + clump:* still the strongest pick, and paid in John's HP across three levels (the anvil costs him 4 to 16 per level).
- *Cyclone as a wall* under today's code: it still hunts, so it doesn't stand still; under the redesign, see the rock knob.

**Failure cases.** The Standard tier on a cold player at the Pile (a loss replays the mission, CR-34; lever 2); Hearth Memory 2's clear gets slower with a 3-damage Cyclone (play check); THJ mashes well, so the Duo's ceiling matters more than its floor (15 at ×1.5 is the reason for 7, not 8).

### UX

| Moment | Shown | The player clicks | Likeliest misread |
|---|---|---|---|
| Trailhead, enemy turn 1 | Next-target lines from three Claws; John's tether when his guard prompts | Press the guard | "John is taking everything": the tether and the ×0.5 number are the read; no change needed |
| Any Duo aim | The aim preview with damage per slot, worked out at mash ×1.0 (`AbilityDamagePreview`); the skull where that kills | Pick slots | **The skull lies near the threshold** (UX critic): the mash comes after the commit and scales 0.7 to 1.5, so a skulled Claw at 8 survives a weak mash (7) and an unskulled one at 11–14 dies to a good one. At 15 per slot this never mattered; at 10 it decides kills. Q5 |
| Cyclone cast | The Cyclone, its hits as numbers | Place it | Expecting kills; the 3s read as chip, which is the intent |
| Pile, enemy phase | Two Claws' lines converging on one sister | Next turn: heal or re-form | "The game got harder for no reason": the change is in the tier, which the player never sees; the numbers above the Claws (6) say it |

**On-screen elements added:** none. **Text:** none. The Duo's description in data should drop to the new value when the GDD is fixed (it isn't shown with a number today; to check in the ability panel).

---

## USP check

- **Family Roles:** neutral on purpose (the rethink owns them). John's guard and Shield Up become worth pressing, because the hits they redirect are worth 6.
- **Synergies:** strengthened. Solo and free damage stops being enough, so Papa's Shelter, Shield Flare and Catch & Return have a job; nothing is locked, nothing new to learn. With Q4, Tempest Bloom takes over the Cyclone's damage and gives the sisters their combo. The open risk is discovery (creative critic): numbers make combos worth it, not visible.
- **Duos:** strengthened in meaning, weakened in raw numbers. Chained Assault goes from a level-solving nuke to the family's best finisher (Linda opens, Mark and Lucy close), which is what a Duo should feel like. Hide and Seek's decoys matter for the first time (a decoy soaks a 6).
- **Managing the Home as a Family:** neutral. HP carried through M2 makes the Home visit after it a little more welcome.

---

## Recommendation

**Option B.** Two Trail-only level values, three global ability values and one Trail-only Synergy grant (Q4). Every one is data or existing wiring; each is one revert. One small preview change follows (Q5).

### Value table

| # | Thing | Current (file) | Proposed | Data or code | Global or Trail | Tier 3? | Why |
|---|---|---|---|---|---|---|---|
| 1 | Enemy tier, all four Trail levels | Early, `enemyTier` 1 (`GB_m2-trailhead/-tracks/-blood/-pile.prefab`; block line `level tier early`) | **Standard** (0): Claw 6, Black Claw 10; HP unchanged | Data (block line + rebuild + rewire) | Trail only | Game feel of the first hour: to THJ with the plan | Mistakes must cost a visible share of HP; protective combos (guard, Shield Up, Shelter, decoys) must have something to protect against |
| 2 | Tracks Dark Claw HP | ×0.8 = 13 (wiring `SetHealth`, `SearchWiring.Trail.cs`) | **×1.0 = 16** (override removed) | Data (wiring) | Trail only | No (D-507 gave HP per level to the designer) | Watch + follow-up (12) killed every 13-HP Claw already scratched; at 16 a fresh one arrives and hits. Every Dark Claw in M2 is then at its own HP |
| 3 | Tracks Black Claw HP | ×0.5 = 20 (same) | **×0.75 = 30** | Data (wiring) | Trail only | No (D-507) | Free damage shredded it (Watch ×2, a pierce, the Cyclone) before it landed a hit. At 30 it survives turn 1's free damage (about 16) and lands its 10 once if nobody deals with it. Not 40: its call isn't previewed and a reflex Watch press or Mark's counter rings it, so a leader alive for 3–4 turns punishes reflexes more than choices (UX critic). 40 is the lever if it never lands a hit |
| 4 | Chained Assault, Mark's ghost hit | `baseFactor` 12 (`Mark_Lucy_MARK_Duo_Effect_AttrMod.asset`) | **7** | Data | **Global** | **Yes** (Duo number) | Per slot 10 × mash. Each hit is rounded on its own (`RoundToInt`, systems critic), so a perfect ×1.5 slot is 4 + 10 = 14: one slot never kills a full Claw; one slot plus any other family hit does. The Duo becomes a finisher. Its Family-SP levels (×1.2 / ×1.35 / ×1.5) would bring back the solo kill, but the first Family SP comes at the Yard, after the Trail (BO-3; *assumed* no earlier source) |
| 5 | Cyclone damage (cast and contact) | `baseFactor` 7 (`Lucy_Cyclone_Effect_AttrMod.asset`) | **3** (the redesign's Whirl) | Data | **Global** | **Yes** (Lucy's ability; Q3) | 56 free damage over two runs; at 3 it wounds and blocks, it doesn't kill. Only if the redesign isn't built first |
| 6 | Cyclone cooldown | 2 (`Lucy_Cyclone_Ability.asset` `coolDownV`) | **4** (the redesign's) | Data | **Global** | **Yes** (Q3) | One Cyclone per Trail fight; same number the redesign ships, so it moves once |
| 7 | **Tempest Bloom on the Trail** (Q4) | Shut: `CycloneArrowScatter` `unlockedByDefault 0`; Bond Lv 2 opens the node at the Yard, after the Trail (BO-4) | **Granted for M2 only**, as Memory 4 does (`RU_LindaLucyCycloneSpreadUnlock`, `HearthMemoryWiring.Mark.Level.cs:219`) | Data (wiring, an existing pattern) | Trail only | **Yes** (a Synergy and a Bond gate) | The Cyclone's damage moves from Lucy alone (cut to 3) to Linda shooting through it (each copy keeps the arrow's 6): the sisters' combo that playtests liked most (`vision.md`), and the sisters' only open Synergy on the Trail |
| 8 | Trailhead rock 6,0 | Rock (`m2-trailhead` block) | **Only if the redesign's C2 is built:** move the rock to 6,... (designer picks with the build) or remove it | Data (block) | Trail only | No | Under C2 a Cyclone on 6,1 seals the east front for three turns |

**Not proposed (and why):** Lucy's follow-up limit and Watch (the rethink owns roles, D-466; the table above shows they no longer kill fresh Claws alone); AI that avoids Linda's lanes (good later, too big and too hard to read in the first hour); a "no repeated target" rule for the Duo (code, and 7 already makes a repeat an honest "kill one" choice); raising any Synergy's numbers (the River's Shield Flare lesson is built on its current diagonals, and Catch & Return already kills with the follow-up; the gap the creative critic named is discovery, not numbers); Late tier (+20% HP: "all HP" again).

**For the GDD, not a change:** the Chained Assault row says Mark's ghost is 8 × and the reach 4; the assets say 12 and 5. Whatever THJ decides, the row gets fixed.

### Walkthroughs with the new values

Prefab coordinates, x from the left, y from the bottom. Hero move 3, 2 AP each. Claw 16 HP, move 4, hits 6. Black Claw 30, hits 10. Mash ×1.0. AI moves are taken from the C3 logs where the same situation came up, and marked *assumed* where not. Damage from the new values in **bold** where it changes the outcome.

#### The Trailhead

```
y1  A . . U L . . . C D . .      A 0,1  B 1,0 (behind)   C 8,1  D 9,1 (ahead)
y0  . B . P . . # . . . . .      Lucy 3,1, Linda 4,1, pick 3,0, rock 6,0
```

**Mark picked, careless (THJ's C3 line, replayed).** Lucy fires Chained Assault first, two slots on B, one on A: B **20, dead**; A **10 → 6** (C3: both dead). Linda bow on C (6 → 10), Explosive on C (8 → 2) and D (8 → 8); quiver 1. Lucy walks to 6,1; Mark walks to 5,1 and Vaults to 7,1: C dead. *Enemy turn:* A walks to 3,1, ends in Linda's row: Watch (last arrow), dead. D steps to 8,1 beside Mark; no arrow left for Watch; **hits Mark 6**; Mark's counter kills it. Win in 1 round, **Mark −6 (C3: 0)**, carried to the route.

**Mark picked, combo line ("start it, finish it together").** Mark Blitzes B from 3,0 (8 → 8), Lucy's follow-up 6 (B at 2). Linda's bow west along row 1 reaches A (6 → 10), follow-up 6 (A at 4). Lucy's Chained Assault: B (2, dead), A (4, dead), and a slot on C if it is offered (5 from Lucy; *assumed*; in C3 only the west pair was picked): **10 → 6**. Linda's Explosive on C/D: C dead, D 8. Mark walks to 5,1. *Enemy turn:* D steps to 6,1 beside Mark, in Linda's row: Watch 6 → 2, Lucy's follow-up (3 away) kills it. Win in 1 round, **0 taken**, every kill a two- or three-member combo.

**John picked, careless (THJ's C3 line, replayed).** John Shield Dashes west (A and B 4 each, B pushed to 0,0), follow-up on A (6). John's sword on B (8 → 4). Linda's bow kills A, Linda walks west to pick up the arrow (0,1). Lucy casts a Cyclone on 6,1. Lucy is now alone at 3,1: John's guard reaches 2, he is 3 away. *Enemy turn:* B **hits John 6**. C takes a **Cyclone contact 3** (C3: 7), reaches 4,1 beside Lucy: Watch 6 and follow-up 6 leave it at 1; it **hits Lucy 6**. D can't reach. *Turn 2:* Lucy's Embers finish C and hit D (7 → 9), John finishes B, Linda's bow (after a walk) D 6 → 3. *Enemy turn:* D **hits Lucy 6**. Turn 3 finishes it. **John −6, Lucy −12: 18 taken (C3: 4), Lucy at 3/15 going into the route.**

**John picked, combo line ("Papa's anvil").** Lucy stays on 3,1, next to John: Papa's Shelter, 10 per Embers. Lucy's Embers on B (10 → 6) and on A (10 → 6). Linda's Explosive on C/D (8 → 8, 8 → 8) and bow on C (6 → 2); quiver 1. John: Shield Up; he stays on 3,0, where his guard covers both sisters (Lucy 1 away, Linda 2). *Enemy turn:* A walks to 2,1, in Linda's row: Watch (last arrow), dead. B reaches 2,1's neighbour and goes for Lucy: **guard, John takes 2** (6 × 0.5 × 0.6), Wrath 1. C steps to 5,1 and goes for Linda: **guard, 2**, Wrath 2. D can't reach anyone (the rock forces the long way) and ends on 6,1, 3 from Lucy (*assumed*). *Turn 2:* Lucy, still Sheltered, Embers D (reach 3; 10, dead); John steps to 2,0 and swings with Wrath ×2 (13.6) on B, dead; Lucy's second Embers on C (dead). **John −4, sisters 0.** The sentence the player says afterwards: "Papa held them."

#### Follow the tracks

```
y4  # # . . . . . . . #
y3  . . . . # . . . . h      Black Claw b 7,2 (30); Claws 5,2 and 8,0 (16)
y2  L U . . . c . b . .      hidden pack h 9,3 and 9,1 (16), revealed on turn 2
y1  P . . . . . # . . h      Linda 0,2, Lucy 1,2, pick 0,1; rocks 4,3 and 6,1
y0  # # . . . . . . c #      the call: every Dark Claw within 5 (eight-way) of the leader
```

**John picked, careless (THJ's C3 line, replayed).** John walks to 3,1; Lucy casts a Cyclone on 4,2; Linda walks to 3,2 and pierces east: 5,2 (6 → 10) and the leader (4 → 26). The bell rings **on Linda**: 5,2 and 8,0 Taunted. Lucy walks to 3,3; John to 5,1. *Enemy turn:* 5,2 meets the Cyclone (**3 → 7**; C3: 7, dead), ends beside Linda in her row: Watch and follow-up kill it. The leader steps to 6,2: Watch 6 → 20. 8,0 reaches 7,2: Watch's pierce, 6 on the leader (14) and 4 on the Claw (12); quiver 0. *Turn 2 (the pack appears):* the leader is **alive at 14** (C3: killed by a Cyclone tick at the turn start). Someone must stop it: John walks beside it and swings (8 → 6), which **rings the bell on John**, who has no AP left for Shield Up; Lucy finishes the leader if she can get within 3 (Embers 7), otherwise it lives; Linda Encores. *Enemy turn 2:* 8,0 **hits John 6**; the leader, if alive, **hits John 10**; the pack walks in (*assumed* one reaches: 6). **John −6 to −22 on this level (C3: 6)**, depending on whether Lucy could reach the leader: the bell costs what the player failed to prepare.

**John picked, combo line (★ A: ring it on Papa, on purpose).** Turn 1: John walks to 3,1 and raises Shield Up; Lucy steps to 2,1 (next to him: Sheltered); Linda to 2,2 (guarded, 2 from John). Nobody touches the leader. *Enemy turn:* 5,2 ends on 3,2 in Linda's row: Watch 6 and follow-up 6 → 4; it goes for Linda: **guard, 2**, Wrath 1. The leader comes in and ends beside John on 4,1 (*assumed*: in C3 it stopped at 6,2 because the Cyclone and John were in the way); Linda's Watch prompts on it on the way: **decline**. It **hits John 6** (10 × 0.6), Wrath 2. 8,0 arrives at 4,0, no hit. *Turn 2 (the pack appears, within 5 of the leader):* John swings with Wrath ×2 (14 → 16) and **rings the bell on himself**: every Claw now targets the shielded father; his second AP: Shield Up again (*assumed*: its cooldown of 1 has run out by his next turn; if not, he takes the pack at full 6 and the line costs him about −24). Lucy (Sheltered) Embers: the main ember kills 3,2's Claw (4), the two sidewinders go on the leader (6 → 10); second Embers on the leader (10, **dead**). Linda steps to 2,0 and bows 4,0 (6 → 10), follow-up 6 → 4. *Enemy turn 2:* 4,0, taunted onto John, steps to 3,0 in Linda's row: Watch, dead. The pack, taunted onto John, walks the long way round the rocks (*assumed*: no hit yet). *Turns 3–4:* the pack reaches the anvil and hits John at 4 each while Linda's lanes and Lucy's embers take them. **John about −12 to −16 over the level, sisters 0.** ★ A is paid in Papa's HP, as designed; ★ B (never touch the leader until the rest are dead) costs spread hits instead.

**Mark picked, careless (pierce the leader on turn 1).** Lucy casts a Cyclone on 4,2; Linda walks to 3,2 and pierces 5,2 (6 → 10) and the leader (4 → 26): the bell rings on Linda. Mark walks to 3,1. *Enemy turn:* 5,2 meets the Cyclone (3) and Watch + follow-up: dead. The leader steps into Linda's row: Watch 6 → 20. 8,0 can't reach. *Turn 2 (the pack appears):* Mark walks to 4,1 and Blitzes the leader (8 → 12), follow-up 6 → 6: **the bell now rings on Mark**, and 8,0 and both new Claws are within 5 of the leader. Lucy's Embers on the leader (7, dead) if she is within 3; otherwise it lives. Linda Encores. *Enemy turn 2:* 8,0 reaches Mark: **6**, counter; the leader, if alive, **hits Mark 10**; one of the pack may reach him (*assumed*: 6). **Mark −6 to −22 of 15**: from a scratch to down (Revenge then fires), depending on whether the family could finish the leader. The trap is the one the level promised, and it is sprung by a choice (the turn-1 pierce), not by a reflex.

**Mark picked, combo line ("start it, finish it together", on the leader).** Turn 1: nobody touches the leader. Linda stays on 0,2 (her row is clear to 4,2), Lucy steps to 1,3, Mark to 2,1. *Enemy turn:* 5,2 ends on 2,2 in Linda's row: Watch 6 and follow-up 6 → 4; it **hits Mark 6**; his counter kills it. The leader walks to 3,2 (*assumed*), in Linda's row: Watch prompts: **decline**. It ends beside nobody, no hit. 8,0 walks 4, no hit. *Turn 2 (the pack appears on 9,3 and 9,1, 6 columns from the leader: outside its call).* All three on the leader before it acts: Linda's Explosive on 3,2 (8 → 22; the bell rings on Linda, but only 8,0 is within 5), Lucy's follow-up 6 → 16, Mark's Blitz from 2,1 (8 → 8), Lucy's Chained Assault: one slot on the leader (**10, dead**) and two on 8,0 if it is in reach (**20, dead**). *Enemy turn 2:* 8,0, taunted onto Linda, walks into her row: Watch, dead (or it hits Linda 6 if it comes round off her lanes). The pack is still on its way. **Mark −6, sisters 0 to −6.** The leader dies to a three-member combo without ever landing its 10; the order matters (Linda opens, the Duo closes), and that is the Duo's new job. The same Duo fired at the leader on turn 1, alone, would have taken it to 10, left it standing, and rung the bell on Lucy (15 HP) with both placed Claws in range.

#### The other two levels (short)

- **Follow the blood:** six Claws at 6 per hit make "fight everything" cost about 12 to 18 over the level; moving with the Dance or the Footrace, the Cyclone (or, under the redesign, a sealed choke) behind, costs a hit or two. The reach goal becomes the cheaper answer instead of a curiosity.
- **The Pile:** the careless search (the pick on 6,3 alone, sisters split) is now about **18 in one enemy turn** (one Claw on the searcher, two on a sister), the number revision 2 was aiming at; the back-to-back ★ lines cost 6 to 8. The Pile is where a cold player is most at risk (lever 2: the Pile back to Early).

### Other missions each global change touches

| Change | Hearth | River | Ridge | M4 | Other |
|---|---|---|---|---|---|
| Chained Assault 12 → 7 | **Memory 4**: the Hold's three Claws have 7 HP (`TopHiddenClawHealth`), so 10 × mash still kills each at any mash ≥ 0.7: unchanged | — (no Mark) | — (no Lucy) | — (no Mark) | M3 "No More Waiting" (classic, Mark + Lucy): weaker Duo |
| Cyclone 7 → 3, cooldown 2 → 4 | **Memory 2** (Cyclone unlocked mid-level, ten-Claws stage): the clear is slower (play check). **Memory 4** (cast by a sequence on the Bloom crossing): the Bloom Claws have 6/6/6/3 HP and die to the split arrows (6), not the Cyclone: unchanged, play check | Lucy's Cyclone chips 9.6-HP Claws for 3 instead of 7 (play check; not the lesson) | — | Lucy's Cyclone weaker against Standard enemies | Every classic Lucy level |
| Trail tier Standard, Tracks overrides off | — | — | — | — | — |

### How a playtest shows it worked or failed

- **Worked:** THJ takes a visible hit (6+) when he fires at the nearest target; he finds a combo (the anvil, Explosive + Duo, Catch & Return) and says so; no Claw dies to the Cyclone at full HP; no Duo slot kills a full Claw; family down 0; M2 about 12 minutes or less.
- **Failed, too soft:** a level again with 0 to 4 taken whatever he does. Next: the third Claw per side at the Trailhead, then the roles test.
- **Failed, too hard:** a hero down on THJ's run, or a cold player loses at the Pile. Next: the Pile at Early, then the Tracks' leader ×0.75.
- **Failed, no combos:** he wins hurt without a Synergy or a Duo (just more HP spent). Then the round's premise is wrong, and the next step is the layouts hosting a combo on purpose (a Catch & Return lane, a diagonal queue for Shield Flare), not more numbers.

---

## Critics

Three independent critics, run 2026-11-11 as read-only Explore agents told to follow `.claude/agents/miso-design-critic.md` (that agent type isn't available in this session), one lens each. Each saw the draft and the evidence, not the others' output. All three: **B, ship with changes**; A, C and D rejected.

### Systems critic

| Objection | Response | What changed |
|---|---|---|
| **Strongest:** two lines bring back solo or free kills. (1) Watch arrows are `LindaAttackArrow`, which Mark's catch accepts: Watch + return + follow-up = 18 kills a fresh Claw, the arrow goes back to the quiver, so only FTP limits it. (2) The Duo's Family-SP levels (×1.2, ×1.35) bring back the one-slot kill | (1) Right, and a find. But it needs Mark planted down Linda's lane as bait and the catch pressed: a set-up three-member combo, which is what this round wants. FTP limits it. (2) Right on the data; no Family SP exists before the Yard, after the Trail (BO-3) | (1) Added to the kill-price table as a kept combo with a play watch: if a "Mark down the lane" turtle wins the Tracks and the Pile untouched, tax it first. (2) Noted on row 4; to check that nothing grants Family SP earlier |
| The combo walkthroughs miss the acceptance criterion (John's Tracks line about −16) | Right | Criterion rewritten: John's anvil is the one line paid in HP on purpose; everyone else at most one hit, and the level at most half the careless cost |
| The Cyclone's Weak (×0.6 enemy damage) is missing | Checked: it is behind Howling Gale (`lockedByDefault 1`, `_LucyCycloneWeak`), so not in base play | Noted under Threat |
| FTP running dry isn't analysed | Right | An "FTP is the combos' price" note; the playtest watches FTP at the Pile's start |
| Verified: per-hit rounding (a ×1.5 slot is 14), guard × Shield Up multiply, Wrath 13.6, follow-up fires in the enemy phase. Doubts: Embers reach 3 in a Trailhead line; Shield Up cooldown in the John Tracks line | Right on both | Trailhead line fixed (D ends on 6,1, 3 from Lucy); the Shield Up assumption marked with its fallback cost |
| Linda's dead Cyclone copy also points at Lucy's damage effect; the orphaned `PassByEffect_AttrMod` is also 7 | Right; both dead | Noted for the implementer (row 5 edits only `Lucy_Cyclone_Effect_AttrMod`) |

### Creative critic

| Objection | Response | What changed |
|---|---|---|
| **Strongest:** cutting the reasons a combo isn't needed doesn't make a combo visible. Five combos had 0 uses in six levels; the likeliest answer to harder hits is the genre default (focus fire, Shield Up, a potion) and "won hurt, no combo" | Right, and the round's biggest risk. A values-only round can't fully answer it; THJ asked for balance, not layouts (D-512) | Criterion tightened to a combo **in every level**, and the "failed, no combos" signal leads to a layout round that hosts a combo on purpose (not more numbers). Q4 adds the one combo the player already knows how to find |
| Lucy loses her signature on the first mission after the Hearth taught it, and the sisters have no combo on the Trail; open Tempest Bloom there so the Cyclone's damage goes through Linda instead of being cut | Right: it turns the round's thesis into a value, and the player learned the shot in Memory 4. The cost is the Yard's reveal (Bloom is one of the three nodes Bond Lv 2 opens) | **Row 7 and Q4**, recommended: grant Bloom for M2 only, the Memory 4 pattern |
| The Mark careless Trailhead still wins in 1 round for −6 | Right; the Trailhead stays the warm-up | Kept, with lever 4 (a third Claw per side) |
| The Duo cut reads as a step back from Memory 4 | Partly; Memory 4's targets still die (7 HP), and the Duo's job changes to finisher | No change; Q5 makes the finisher honest on screen |
| Catch & Return could be buffed | Its 12 + the follow-up already kills; the gap is discovery | Kept unbuffed; reason stated |

### UX critic

| Objection | Response | What changed |
|---|---|---|
| **Strongest:** the Duo's preview is computed at mash ×1.0, but the mash (0.7 to 1.5) comes after the commit; at 10 per slot the skull is wrong both ways on exactly the finisher the round sells. My draft said the preview would show it honestly: it won't | Right; my claim was wrong | UX table corrected; **Q5**: preview the Duo at its mash floor (the skull means a sure kill, the mash only adds) |
| The bell at 40 HP is unreadable under reflex prompts: the call isn't previewed, Watch and Mark's counter can ring it in a 1-second press, and a leader alive 3–4 turns gives many more chances | Right | Leader **×0.75 (30)**, not 40: it survives the free damage to hit once, and dies within a turn of being focused. 40 is the lever. Whether a Cyclone contact rings it is unconfirmed (to check) |
| Papa's Shelter is invisible before the move (no move-ghost marker) | Right; out of this round's budget (a new element) | Accepted as a discovery; a Shelter marker in the move preview is a candidate for a later UX pass (backlog note, not this plan) |
| The tier change is invisible; Lucy's follow-up unpreviewed makes threshold math harder; Cyclone at 3 looks like a nerf | Partly; the first 6 is the read, the follow-up stays a bonus (no line relies on it alone), and Q4 gives the Cyclone a visible payoff | Q4; no other change |

**What changed my mind most:** the UX critic's skull point (the Duo can't be a finisher the player can trust without Q5) and the creative critic's Tempest Bloom (the cleanest way to make the Cyclone a family tool instead of just weaker). **What I rejected:** taxing Catch & Return on Watch now (it's the kind of combo the round wants; watched instead), a Duo upgrade lock (no Family SP before the Yard), and a Shelter marker (a new element).

---

## Questions for THJ

**Q1. The Trail at Standard tier, the Tracks' Claws at their own HP and its leader at ×0.75?**
- Context: the Trail is Early tier (Claw hits 4.5; three-quarter damage). Ten enemy hits in six levels, never more than 6 to one hero in a turn: nothing a Claw does costs anything visible. Standard keeps HP and gives full damage (Claw 6, Black Claw 10). The Tracks' ×0.8 Claws and ×0.5 Black Claw died to free damage before they hit; at 16 (the Claws' own HP) and 30 (the leader at ×0.75) they arrive and hit. Trail only: the River, Ridge and the Hearth are Tutorial tier and unaffected.
- Options: (a) Standard on all four levels, Tracks Claws at their own HP and the leader at ×0.75; (b) Standard on the Trailhead, the Tracks and Blood, the Pile stays Early (safer at the mission's last, emotional level); (c) Early kept, overrides only (fights longer, hits still small).
- Recommendation: (a), with (b) as the first lever if a run goes down at the Pile.
- Blocked: the Trail wiring values and every walkthrough number.

**Q2. Chained Assault: Mark's ghost hit 12 → 7 (global)?**
- Context: per target slot the Duo deals Lucy's sidewinder 3 + Mark's ghost 12 = 15 × mash, so one slot kills a full 16-HP Claw at any mash above ×1.07; with two targets in reach, THJ's Duo killed both on turn 1. At 7 a slot deals 10 (15 at a perfect mash): it never kills a full Claw alone, but finishes any Claw another family member has hit (Explosive 8 + 10, bow 6 + follow-up 6 + 10). Two slots on one target still kill it. Touches every Mark + Lucy fight: Hearth Memory 4's Duo targets (7 HP) still die; M3 "No More Waiting" (classic) gets a weaker Duo. The GDD row (8 ×, reach 4) is out of date either way.
- Options: (a) 7: never a solo kill; (b) 8, the GDD value: a perfect mash (×1.46 or more) still kills one; (c) keep 12 and lock the Duo on the Trail (the USP loses its best showcase).
- Recommendation: (a).
- Blocked: the Mark-pick walkthroughs; the Duo asset value.

**Q3. Lucy's Cyclone on the Trail: stopgap now, or the redesign first?**
- Context: the Cyclone dealt about 56 damage over the two runs from one cast per level, mostly by moving into Claws or being walked into, and erased the bell's cost on the Tracks. Its redesign (anchored, Whirl 3, cooldown 4, AI avoids the cross) fixes this and waits on your Q1–Q5 in [`plans/2026-11-11-cyclone-redesign-tech.md`](2026-11-11-cyclone-redesign-tech.md); its Q5 recommends building it *after* the challenge round. This question doesn't answer those; it only asks what the Trail plays with meanwhile.
- Options: (a) **stopgap:** damage 7 → 3 and cooldown 2 → 4 in data now, the redesign's own numbers, so they don't move again when it lands; (b) build the redesign's C1 + C2 before the next Trail play (no stopgap; then the Trailhead's 6,0 rock moves in the same change, row 8 of the table); (c) leave the Cyclone and balance around it (the Trail stays soft wherever Lucy casts).
- Recommendation: (a). If you'd rather build the redesign now, (b) is better than (a) and makes (a) unnecessary.
- Blocked: the Cyclone values; whether row 8 applies.

**Q4. Tempest Bloom open for the Trail (granted for M2 only)?**
- Context: on the Trail the sisters have no open combo: Bloom and Sister's Rivalry wait for Bond Lv 2 at the Yard, after the Trail (BO-4), and their Duo is locked by the level (D-470). With the Cyclone cut to 3 (Q3), Lucy's showiest spell shrinks on the first mission after the Hearth taught it. Granting Bloom for M2, the way Memory 4 already grants it for its own mission (`RU_LindaLucyCycloneSpreadUnlock`, wiring only), moves the Cyclone's damage from "Lucy alone" to "Linda shooting through Lucy's wind" (three copies, 6 each): the combo playtests liked most (`vision.md`), and one the player already knows how to aim (the aim preview shows the copies' lanes, CR-56). The cost: the Yard's Bond Lv 2 opens Bloom "for good" as one of three nodes, so the player will have seen it twice before; Bond Lite itself doesn't change (it still gates the node).
- Options: (a) grant Bloom for M2 only; (b) keep it shut until the Yard (the sisters' combos stay a Home reward; the Trail has none for them); (c) open the node earlier for good (changes Bond Lite's reward, BO-4).
- Recommendation: (a).
- Blocked: row 7 (wiring); the sisters' line in the Synergy plan.

**Q5. Chained Assault's preview: show the damage at the mash floor?**
- Context: the aim preview works out the Duo at mash ×1.0, but the mash (×0.7 to ×1.5) comes after the commit. Today a slot deals 15, so the mash never decides a kill. At 10 (Q2) it does: a skulled Claw at 8 survives a weak mash; an unskulled Claw at 11–14 dies to a good one. The skull means "kills if it lands" (CR-46), so on the round's showcase finisher it would be wrong both ways. Previewing at the floor (7 per slot) makes the skull a promise and leaves the mash as pure upside. A preview change in code (`AbilityDamagePreview`; core-system status to check), no new element. The other mash Duos (Marks-Sisters, Healing Marks) have the same gap.
- Options: (a) preview mash Duos at their floor (×0.7); (b) show a range ("7–15") on each slot (a new number display; against the budget); (c) leave it at ×1.0 and accept the misreads.
- Recommendation: (a), as its own small change after Q2; Q2 can ship first.
- Blocked: nothing in the values; the Duo's readability as a finisher.

---

## Docs to update

If approved:

- **GDD** `design/gdd/family-systems.md`: the Chained Assault row (Mark's ghost 7 ×, reach within 5, per-target total 10 × mash; status line), source unchanged.
- **GDD** `design/gdd/characters/lucy.md`: the Cyclone row (3 ×, cooldown 4; note the asset reach 4 against the row's 3) if Q3 (a); a note that it is a stopgap toward the redesign.
- **GDD** `design/gdd/missions-structure.md`: the M2 rows: tier Standard, no HP overrides (the rows still describe the classic `LevelLucyJohn` levels; the onboarding Trail needs its own rows, which the C3 docs pass already owes).
- **GDD** `design/gdd/enemies.md`: the Black Claw's attack (10 × damage) and the Dark Claw's (6 ×), which no GDD table states today.
- `design/level-chunks.md`: the "Kill price" knob from revision 2 becomes **12** (Watch + follow-up), not 6; and "a one-cell choke is a Cyclone wall" once the redesign's C2 is built.
- `plans/onboarding/2026-11-11-post-hearth-challenge-design.md`: a note at the top that its HP and Duo assumptions are superseded by this plan (the layouts stand).
- `plans/onboarding/2026-11-11-m2-trail-levels-tech.md` (coordinator): a C4 for the values (blocks' `level tier standard`; the wiring: Tracks Claws no override, leader ×0.75, Bloom granted for M2 if Q4; `SearchTrailTests` factors, tier and the grant; the three asset values if Q2 and Q3 (a); only `Lucy_Cyclone_Effect_AttrMod` changes, not the orphaned `PassByEffect_AttrMod` or the dead Linda-folder copy). Q5 is its own small code task if approved.
- **GDD** `design/gdd/family-systems.md` Tempest Bloom row: "**On the Trail (M2):** granted for the mission" if Q4.

## Risks

- **Paper against AI.** Several walkthrough moves are assumed (marked); the numbers that decide outcomes (6 per hit, 10 per Duo slot, 3 per Cyclone contact, 12 per Watch + follow-up) are from the assets.
- **First-hour difficulty.** Standard tier at the Pile for a cold player; lever 2.
- **Global spread.** The Duo and Cyclone numbers touch the Hearth, the River and classic missions; the table above lists each and its play check.
- **The Cyclone redesign.** The stopgap's numbers are the redesign's; if THJ changes the redesign's numbers (its Q1), these move with them.
- **`AIRegressionTest`** may move (Cyclone data is in its catalog): known red, never re-baselined without THJ.
- **Time.** Fewer free kills means a little more time per fight; M2 within about 12 minutes is the check.

## Gates

Design only. If approved: coordinator's C4 on the M2 tech plan (data + wiring + tests; EditMode known red only), reviewer, then THJ's timed play of M2 with each pick and both routes (needs THJ's time: yes), then a cold run for the Pile risk. No grids changed (row 8 changes `m2-trailhead` only if the redesign's C2 is built).
