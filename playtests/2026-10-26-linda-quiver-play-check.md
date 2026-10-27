# Play check: Linda's Quiver (C1 to C3)

For THJ, 2026-10-26. Branch `thj/linda-quiver` (all three chunks uncommitted). Nothing here has been seen in play yet. Tick or note each step; tell me the failures and the feel notes (pacing, popups) and I turn them into tuning or fixes.

## Setup

- **Levels:** M4 (The White Mothers: Level2-C1, C2, C3-1, C3-2) or M6 (LevelE2-C1 to C3), full squad (Linda, John, Lucy, Mark, Toba). `LevelM1-C3` is the open-board harness if you want a quiet room. Start from the toolbar level picker (Edit mode, Assign Placeholders). For the Lucy and Mark steps, give them the Cyclone scatter unlock and Catch & Return.
- **Reset the save** (Tools > Save Data > Clear Save Data) if a tutorial gets in the way.
- **Cheats** (CheatHandler, hold C+H+T): `K` kills the hovered unit (allies too: use it on an enemy, or on Linda for the revive step), `H` heals it (revive), `]` +1 AP (Shift: full AP and no cooldowns, good for Recall), `L` +99 FTP (Watch), `[` damages a unit. `F12` completes the objective. The quiver has no count UI yet (C4): count by shooting until the bow greys out.
- Silence barks in global settings (`silenceBarks`) only if the popups get in the way; the toss still plays.

## C1: the quiver and landing

1. **Spend and land.** Linda at 4. Bow an enemy, then ground, until the bow greys. Expect 4 shots, an arrow icon on each landing tile, bow greyed after the 4th.
2. **Kill shot.** Kill an enemy with the bow (`[` first to weaken it). Expect the arrow icon on the dead enemy's tile, not at end of range.
3. **Pierce through 2.** Line two enemies up. Expect the icon on the second, one arrow spent.
4. **Hole and wall.** Shoot over a hole, and into a wall. Expect the icon on the last valid cell of the path, toward Linda.
5. **Crescendo and Duos.** Fire Crescendo (icon on its centre cell), then Marks-Sisters and Healing Marks (icon at the line end). Each costs 1.
6. **Super time Crescendo at 0** (D-251). Empty the quiver, reach super time. Expect Crescendo fires anyway, lands nothing, and is not greyed out.
7. **Both arrow Duos at 0.** Linda-Lucy and Linda-Toba Duos, plus bow and Crescendo, grey out at 0 (outside super time).
8. **Watch.** Each Watch trigger spends 1 (and 1 FTP, D-246). At 0 no Watch prompt appears at all.
9. **Tempest Bloom.** Shoot through Lucy's Cyclone with the unlock. Expect 1 spent, 1 icon on the cell one before the Cyclone (you can walk to it). Also try a Marks-Sisters arrow through it.
10. **Catch & Return.** Mark catches (QTE success): quiver count unchanged, nothing on the board. Miss the QTE: the arrow lands normally.
11. **Stacks.** Shoot twice onto the same tile: icon with "2". Shoot an enemy that survives: the icon looks reddish-grey (locked) with a red number; kill it and it turns normal.

## C2: pickup and the hand-back beat

12. **Pickup by walk.** Linda at 1/4, John walks onto a 2-stack. Expect 3/4 (check by shooting), icon gone, a small arrow tossed to Linda, a line from John, Linda's reply about half a second later.
13. **Leftovers.** Linda at 3/4, step on a 2-stack: one comes off, one stays (single icon, no number). At 4/4 nothing comes off.
14. **Other moves.** Pickup also happens when a Bergson is pushed, Commanded, Fist Blitzed or Dances (John-Linda) across an arrow tile.
15. **Linda herself.** She walks onto her own arrow: one line from her, no toss. Also aim an arrow at a tile where John stands: it goes straight back with the beat.
16. **Locked stack.** Step next to it: nothing. Kill the enemy on it, then step on: taken. An enemy that walks onto a free arrow takes nothing and the stack shows the locked look at once; when it leaves the look clears.
17. **Enemies take nothing.** Let an enemy walk over a free arrow in the enemy phase: it stays. Toba's ally (other faction) takes nothing either.
18. **Revive.** Kill a Bergson standing on an arrow (`K`), revive it (`H`): it should take the arrow. If Linda is dead, nothing is picked up and the arrows stay.
19. **The beat's feel.** Is 0.6 s right? Do two stacks in one move (a long move or Fist Blitz over two arrows) pile up badly? Do the popups (fixed 1.2 s, [PLACEHOLDER] tag stripped) read? Tuning fields are on `Unit_Linda`'s `LindaQuiver`.
20. **Next level.** Finish the level (`F12`) and start the next: full quiver, no arrows on the board, no sprites left in the air.

## C3: Recall

21. **Grey-out.** Nothing on the ground: Recall is greyed. Quiver full with arrows grounded (only with extra size, may be unreachable): greyed. 1 or more grounded and room: usable.
22. **Use it.** Ground 2 arrows, one under a living enemy (locked) and one behind a wall. Select Recall, click Linda. Expect: all arrows fly in straight lines to her (look and speed, about 0.45 s), the board is empty, quiver full, no damage, a short line pops up, and the turn waits for the flight.
23. **Cost.** 1 AP. Cooldown 2: not usable on her next turn, usable the turn after (use `]` + Shift to reset it if needed).
24. **Ability bar.** It is the 10th button, with no number key. Check the tooltip: the [PLACEHOLDER] tag may show in the description (known). Check the Self-cast click feels right.
25. **Cleanup.** End the level or kill Linda mid-flight: no leftover sprites.

## Not covered here

Pips, badge, previews and "No arrows" tooltips are C4. Combat log lines are C5. M2's win path is not touched.
