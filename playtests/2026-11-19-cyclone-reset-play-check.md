# Cyclone reset: play check

Branch `thj/cyclone`, commits `d9cb1f2ce` to `359882aed` (plan `plans/2026-11-19-cyclone-reset-tech.md`, design `plans/2026-11-19-cyclone-reset-design.md`, D-580 to D-585). Mark each item OK / not OK with a note. The round 2 and round 3 lists are retired by this reset.

**The rule to check against:** Lucy summons the Cyclone on an empty cell; it stays 3 rounds and never moves on its own. On cast, after each enemy turn and after each Steer, it Whirls: enemies in its four lines are pulled one cell in, then every enemy beside it is hit. Once a turn Lucy Steers it up to 3 cells in a straight line, through enemies (one hit each); an enemy on the cell where it stops is knocked one cell onward (else to the Cyclone's right, else its left); then it Whirls.

## Steer: where it can go

1. Steer range lights only cells on the 4 straight lines, up to 3 out. No cells around corners.
2. A wall, the map edge or a walk-blocking object ends a line; a hazard that doesn't block is crossed.
3. A Claw on a line with a free cell beyond it (onward, right or left): its cell lights. One that can't be knocked anywhere: its cell stays dark, the cell beyond still lights if free.
4. Family, allies, a Masher or other heavy, and planted cells are never a stop; the Cyclone crosses the family and allies.
5. **Screenshot 2 layout** (Claw above, family around): the Steer is offered.

## Steer: what happens

6. **Screenshot 1 layout** (row of Claws ahead): steer onto the first Claw: it's knocked to the Cyclone's right of travel (screen-down when moving screen-right), or left if that's taken. Steering onto the empty cell before the row is also offered.
7. Each enemy passed takes one hit as the Cyclone reaches its cell, one after another down the line. Passed enemies don't move. **(New beat, your call: does the sequence read as a sweep?)**
8. The closing Whirl doesn't hit a passed enemy again, but **can still pull it in** (it moves, no second hit). Intended?
9. The knocked enemy lands where its ghost showed, then the Whirl hits it if it's beside.
10. Knock into Linda's lane: Watch answers the knock, before the Whirl's pull and hit. Passing an enemy through her lane does nothing.
11. Knock onto a hazard: the hazard fires.
12. Steer through a Masher: it takes a hit, the Cyclone doesn't burst, the Masher doesn't counter.
13. Combat log: one line "Steer · Lucy: hit N on the way, knocked K", then "Whirl · Lucy: pulled N, hit M".

## Preview

14. Hovering a stop shows: a straight path, the landing Cyclone and cross, at most one knock ghost, the Whirl's pull ghosts, and exactly one damage segment per enemy that will be hit (skull when lethal). Nothing on the family.
15. **Screenshot 3 layout**: you can tell what a move will do before clicking.
16. What the preview shows is what happens (check 3 or 4 different Steers).

## Cast on an enemy

17. Cast on an adjacent-row enemy: knocked away from Lucy; if blocked, to the right, else left of that direction; refused (cell dark) if none is free.
18. Cast diagonally next to Lucy: knocked along the row, then right/left of that. It may now land on Lucy's side (rule change from the old row-then-column).
19. Empty-cell casts unchanged.

## Gone

20. No wobble or pips flicker when a heavy heads for the Cyclone.
21. Nothing rides along with a Steer: no side or rear enemies dragged, no grab/drag animation.

## Unchanged (spot check)

22. Heavies still walk through and burst it; enemy shots still blocked; the family walks through; 3 pips, one per family turn.

## Feel (answer in a line)

- Is Steering fun now? Can you predict it before hovering?
- Does the knock direction ever surprise you? (Lever: "onward, else refuse".)
- Does the Steer out-damage Embers? (Lever: a lighter graze on the pass.)
- Do you miss the drag? (Lever: the enemy right behind follows.)
