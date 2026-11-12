# The Trail after the challenge rebuild: THJ's play, 2026-11-11 (afternoon)

Build: `thj/after-hearth`, M2 Trail C3 (uncommitted at play time; plan `plans/onboarding/2026-11-11-m2-trail-levels-tech.md` C3, design `plans/onboarding/2026-11-11-post-hearth-challenge-design.md` rev 2).
Logs: `C:/Users/javid/AppData/LocalLow/Dead Mage/miso/CombatLogs/20261111-145831_The_Trail.log` (Mark pick, blood route) and `20261111-150621_The_Trail.log` (John pick, tracks route).

## THJ's words

"Played it, check the logs." (No feel verdict given.)

## Numbers (coordinator, from the logs)

| Level | Run | Rounds | Enemy hits | Taken | How it was won |
|---|---|---|---|---|---|
| Trailhead | Mark | 1 | 0 | 0 | Lucy fired Chained Assault (Mark–Lucy Duo): 16 on each west Claw, both dead at full HP. Bow + Explosive on the east pair, Vault, then Watch + Lucy's follow-up killed the last in the enemy phase |
| Follow the blood | Mark | 4 | 2 (4, 4) | 8 | Fought, never went for the end tiles; won by the hidden kill-all. Turn-2 pair arrived on 4,4 / 14,4 as planned. A Claw walked through Lucy's Cyclone for 14 |
| The Pile | Mark | 3 | 2 (2 after barrier, 4) | 6 | Lucy searched 3,3 on her first move; west lane killed by bow + follow-up + Blitz, embers; the last Claw died attacking (Cyclone) |
| Trailhead | John | 3 | 1 (4) | 4 | John's Shield Dash west, Lucy's Cyclone east: the east Claw walked into it (7) and the far one took 7 more on turn 2 |
| Follow the tracks | John | 3 | 2 (3, 3) | 6 | The bell rang turn 1 (Linda's pierce went through 5,2 into the Black Claw: both Claws Taunted). Lucy had already put a Cyclone on 4,2 in front of Linda: 5,2 died walking into it, the Black Claw was killed by Watch ×2 and a Cyclone tick before it ever hit. Called Claws hit Linda 0 times. Turn-2 pair arrived on 9,3 / 9,1 and hit Shield-Up John for 3 each |
| The Pile | John | 3 | 2 (3, 3) | 6 | Embers ×2 + bow on the west front Claw turn 1; John Shield-Up in the east; Shield Dash + Explosive; Watch + follow-up on the west Claw |

Mission totals: Mark run 8 rounds, 14 taken, 7m30s (C1: 5 rounds, 15 taken). John run 9 rounds, 16 taken, 5m26s (C1: 7 rounds, 12 taken). Family down 0 in both. Most damage taken by one hero in one enemy turn: 6.

## What worked

- Every rebuilt beat fired as designed: both arrivals on turn 2, on the right tiles; the Black Claw's call applied Taunted to the pack; the Pile search revealed both groups; Blood's kill-all fallback won without locking.
- Fights last longer (3–4 rounds, not 1–3) and more enemies reach the family than in C1.

## Why it still isn't a challenge

1. **Lucy's Cyclone is a free trap.** The AI walks into it and keeps walking into it: 7 per tick, 49 damage over the two runs, three kills or near-kills, and it erased the bell's cost on the Tracks. The levels place Claws so they must cross the family's front, and the Cyclone sits on that front. (The Cyclone redesign plan already covers walking and AI crossing.)
2. **The Mark–Lucy Duo still wipes.** The design assumed "at 16 HP a Duo cripples three"; in play, with two targets in reach, Chained Assault hit one twice and dealt 16 to each: two full-HP Claws dead in one action on turn 1. The two-front Trailhead was solved before it started.
3. **Free reactions still finish the approach.** Watch (6) + Lucy's follow-up (6) fired in most enemy phases and turned approaching Claws into kills or cripples before they hit (Roles rethink is separate, D-466).
4. **Enemy hits are small.** Claws hit 3–4 (John 3 through Shield Up). Ten enemy hits across six levels, never more than 6 to one hero in a turn; the design's careless-Pile estimate was ~12. With 15–32 HP and potions, a mistake costs nothing visible.
5. **The reach wasn't a demand.** On Blood THJ fought instead of moving; with kill-all as the fallback and small enemy hits, fighting is the safe answer, so the Duos' reach ★ never came up.

So the layouts now set up the situations; the family's free and area damage (Cyclone, Duo, roles) removes their cost, and enemy hits are too small to make a cost felt.

## Side findings

- Cyclone kills are credited to the victim or "other" in the summary (`Kills by unit: DarkClaw #05-02 1 · other 1`). Covered by the Cyclone plan's damage-report chunk.
- **Possible bug, lost skill-tree point:** John run, Lucy's loadout shows `Tree: Sidewinders 1` at the Trailhead and no tree from the Tracks on. In the morning's C1 run (`120958`) the same point stayed on all three levels. The line prints only when the tree has points (`CombatLog.Units.cs:306`), so either the point was really lost between levels or the log reads a stale source. Backlog: Explore, then a fix.
- No notes yet from THJ on the arrival camera, the Black Claw caption order or Blood's blank panel row.

## C4 replay (22:23, Mark pick, tracks route; log `20261111-222313_The_Trail.log`)

THJ: "It was much much better. I think it is okay for now."
Numbers: 8 rounds, 9m02s, 28 taken (C3 Mark run: 14), family down 0. Trailhead 6 taken (Claw 6 on Linda); Tracks 10 taken + a potion: the Black Claw's pack was called and the leader hit Mark for 10 (15 → 5); Pile 12 taken (Claws 6 on Lucy and Mark turn 1). Chained Assault not used. Camera on Linda after arrivals: no complaint.
