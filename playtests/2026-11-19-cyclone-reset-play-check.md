# Cyclone reset: play check

Branch `thj/cyclone`, commits `d9cb1f2ce` to `3b566e5bf` (plan `plans/2026-11-19-cyclone-reset-tech.md` incl. its addendum, design `plans/2026-11-19-cyclone-reset-design.md`, D-580 to D-588). Mark each item OK / not OK with a note. The round 2 and round 3 lists are retired by this reset.

**The rule to check against:** Lucy summons the Cyclone on an empty cell; it stays 3 rounds and never moves on its own. On cast, after each enemy turn and after each Steer, it Whirls: enemies in its four lines are pulled one cell in, then every enemy beside it is hit. Once a turn Lucy Steers it up to 3 steps, turning and around walls, through enemies (one hit each); the route is the shortest that can stop there, then the one passing the most enemies, then straight before turning. An enemy on the cell where it stops is knocked one cell onward along the last step (else to the Cyclone's right, else its left) and takes a full hit; then it Whirls (the knocked enemy takes the Whirl's hit too). Enemies no longer avoid the cross.

## Steer: where it can go

1. Steer range lights every cell reachable in up to 3 steps, around corners and walls (not only straight lines).
2. Walls, the map edge and walk-blocking objects are gone around, never through; a hazard that doesn't block is crossed.
3. A Claw's cell lights when some shortest route lets it be knocked (onward along the last step, right or left). One that can't be knocked by any shortest route stays dark; cells beyond still light if free.
4. Family, allies, a Masher or other heavy, and planted cells are never a stop; the Cyclone crosses the family and allies.
5. **Screenshot 2 layout** (Claw above, family around): the Steer is offered.

## Steer: what happens

6. **Screenshot 1 layout** (row of Claws ahead): steer onto the first Claw: it's knocked to the Cyclone's right of travel (screen-down when moving screen-right), or left if that's taken, and takes a hit. Also try a route that turns into the row.
7. Each enemy passed takes one hit as the Cyclone reaches its cell, one after another down the line. Passed enemies don't move. **(New beat, your call: does the sequence read as a sweep?)**
8. The closing Whirl doesn't hit a passed enemy again, but **can still pull it in** (it moves, no second hit). Intended?
9. The knocked enemy takes a hit as it lands where its ghost showed, then the Whirl hits it again (its preview bar shows both together). A knock that kills: no Whirl pull or hit for it.
10. Knock into Linda's lane: Watch answers the knock, before the Whirl's pull and hit. Passing an enemy through her lane does nothing.
11. Knock onto a hazard: the hazard fires.
12. Steer through a Masher: it takes a hit, the Cyclone doesn't burst, the Masher doesn't counter.
13. Combat log: one line "Steer · Lucy: hit N on the way, knocked 1 and hit it" (or "knocked 0"), then "Whirl · Lucy: pulled N, hit M".

## Preview

14. Hovering a stop shows: the route's path arrows (with turns), the landing Cyclone and cross, at most one knock ghost, the Whirl's pull ghosts, and exactly one damage segment per enemy that will be hit (skull when lethal). Nothing on the family.
15. **Screenshot 3 layout**: you can tell what a move will do before clicking.
16. What the preview shows is what happens (check 3 or 4 different Steers).

## Cast on an enemy

17. Cast on an adjacent-row enemy: knocked away from Lucy; if blocked, to the right, else left of that direction; refused (cell dark) if none is free.
18. Cast diagonally next to Lucy: knocked along the row, then right/left of that. It may now land on Lucy's side (rule change from the old row-then-column).
19. Empty-cell casts unchanged.

## Gone

20. No wobble or pips flicker when a heavy heads for the Cyclone.
21. Nothing rides along with a Steer: no side or rear enemies dragged, no grab/drag animation.
21b. Enemies walk onto and end their moves on the Cyclone's cross freely (they no longer keep off it).
21c. Cast on an enemy: the knocked enemy takes a hit, then the cast Whirl's.

## Unchanged (spot check)

22. Heavies still walk through and burst it; enemy shots still blocked; the family walks through; 3 pips, one per family turn.

## Feel (answer in a line)

- Is Steering fun now? Can you predict it before hovering?
- Does the knock direction ever surprise you? (Lever: "onward, else refuse".)
- Does the Steer out-damage Embers? (Lever: a lighter graze on the pass.)
- Do you miss the drag? (Lever: the enemy right behind follows.)

## Added after the review

23. Pass-kill a Claw that sits behind the stop on the same line, with another enemy behind it: the preview shows no pull ghost for the dying Claw, only its damage with a skull; the enemy behind is pulled as shown. Same for a knock that kills, and a knock onto a hazard where hazard plus hit kills (the preview ignores the hazard's damage: rare mismatch).

## THJ's play notes, 2026-11-20

Screenshot `playtests/img/2026-11-20-cyclone-4-no-steer-no-cast-preview.webp`.

- **Bug:** after summoning the Cyclone, it can't be Steered (Lucy's slot 3 shows the Cyclone greyed with a 3, no Steer).
- **Bug:** casting on an empty cell next to enemies, the cast preview doesn't show the cast Whirl's damage.

## Controls (added 2026-11-20)

Commits `14f9c43e7` to `5ee450844` (plan `plans/2026-11-20-cyclone-controls-tech.md`, D-589 to D-593).

**Click to Steer and the pulse**
24. Click the Cyclone with nothing selected, or another family member selected: Lucy becomes selected, the Steer is picked, its range and preview show.
25. Click it when the Steer can't be used (Lucy at 0 AP, during an enemy turn, while something is still moving): nothing new happens.
26. In another ability's targeting: if the Cyclone's cell is a legal target of that ability, the click does what it did before. If not, it switches to Lucy's Steer.
27. Picking the Steer (button, hotkey or click on the Cyclone) makes the Cyclone pulse once. Undoing a target pick and re-entering doesn't stack pulses.

**Free first Steer**
28. First Steer of Lucy's turn: her AP doesn't drop, and the hover AP preview shows no cost. The second Steer that turn costs 1 AP. Next turn the first is free again.
29. Undo a free Steer: no AP comes back and the next Steer is free again. Undo a paid one: 1 AP comes back.
30. Untick "First Steer Free Each Turn" on the Steer effect asset: every Steer costs 1 AP.

**Mark's Command steers**
31. With Mark's Command picked, the Cyclone's cell lights as a first target. Picking it lights exactly the Steer's stops; hovering a stop shows the same preview as Lucy's Steer. The Command's own path arrows and ghost don't draw for the Cyclone.
32. Execute: the same Steer and Whirl as Lucy's. Mark spends his 1 AP and the Command goes on its cooldown. Lucy's AP, her free Steer and the Steer's state are untouched (she can still Steer free after).
33. The enemy on the stop cell turns to face Mark before it's knocked. Harmless, but does it look odd?
34. John's shield dash: hover a unit with Mark's Command, then pick the Cyclone instead. No leftover dash preview.
35. **Your call (Weak):** with Mark's Weak upgrade owned, steering onto an enemy that gets knocked also makes that enemy Weak (the Cyclone itself never gets it). Keep it as a bonus, or remove it?

**Combat log**
36. Lucy's Steer: "Steer · Lucy: hit N on the way, knocked 1 and hit it". Mark's: "Steer · Mark: steered Lucy's Cyclone, hit N on the way, knocked ...". Cast on an enemy: "Knock · Lucy: knocked 1 and hit it", then the Whirl line. A free Steer isn't marked, because the log shows no AP.
