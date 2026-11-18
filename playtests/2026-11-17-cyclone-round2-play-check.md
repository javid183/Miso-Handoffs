# Cyclone round 2 (Eye of the Storm): THJ play check list (branch `thj/cyclone`)

Built back to back without per-chunk play: C1 (Steer ends in a Whirl, Cyclone Power), C2 (carry), C3a (heavies walk through), C3b (burst), C3c (AI heavy handling), C4 (cross drawing, previews, wobble). THJ plays everything here, then the commits are proposed. Collected from `reports/cyclone-r2-c1.md` to `cyclone-r2-c4.md` and their reviews. Mark each item OK / not OK with a note.

Setup that helps: a level with Lucy, Linda, a few Claws, and a Masher or the Goblin Queen (Masher level, or Memory with the Queen). Cheats for AP if needed.

## Cross drawing (always on)

1. Cast the Cyclone. The four cells touching it show a faint blue swirl tint each (cool wind hue). It must not read as danger to the family (not warm, not red). Nothing on the diagonals.
2. Each arm tip (2 cells out, four of them) shows one chevron pointing at the Cyclone. No chevrons or streaks on the touching cells, no "3 ×" label anywhere, no numbers.
3. The pips under the Cyclone still read; the drawing scales with the grid; at the board edge only the cells that exist are drawn.
4. Whirl beat with the new drawing: swell, the chevrons brighten while the pull runs, then the ring bursts and the Cyclone shrinks back. Same on cast, end of enemy turn and after a Steer.

## Cast aim preview

0. Play the normal flow: start Play from PreloadScreen, go through Home into a level (not TestLevel or SampleScene). The cast preview below must work there too (it attaches to the level's event bus after the level is created).
5. Pick the Cyclone cast and hover an empty cell in range: the cross (dimmed) is drawn at the cursor.
6. An enemy standing 2 out on a straight arm of the hovered cell: its ghost appears one cell in, joined to the enemy by a faint blue tether. The damage segment (3 at Cyclone Power level 1) shows on the ghost's health bar, with the lethal skull if 3 kills it.
7. An enemy already beside the hovered cell: no ghost; the damage segment shows on the enemy itself.
8. Diagonal enemies, Immovable or large enemies: no ghost (they are not pulled); Immovable/large beside the cell still show damage (they are hit).
9. Hover a cell that is not allowed (a unit, a planted entity, out of range): nothing is drawn. Move between cells: the preview follows without leftovers.
10. Cancel the cast (right click / Esc): every ghost, tether, damage segment and the aim cross go. Click to cast: same, then the real Whirl matches what was shown.

## Steer aim preview

11. Pick Steer. The Cyclone's own cross dims. The range highlight offers only reachable cells (a blocked front enemy refuses that cell and the cells past it on that line).
12. Hover a reachable cell: the path arrows, a faint copy of the Cyclone on the landing cell, and the cross drawn at the landing cell only (the cross at the current cell disappears: never two crosses).
13. One ghost per enemy that moves (carried beside it, shoved in front, following behind, or pulled by the closing Whirl), on its final cell only, each tethered to where it stands now. No step arrows any more.
14. A rider that joins part-way (an enemy that ends up beside the Cyclone after a step) gets its ghost and tether too: the tether starts at its current cell.
15. Damage and lethal skull on the ghosts of every enemy the closing Whirl hits (carried enemies included, and enemies pulled in by that Whirl). Enemies hit where they stand show it on themselves. The bars show the Whirl's hit only, never Watch arrows.
16. A carried or pulled enemy whose landing cell has a hazard (spikes, a web, a pool): an orange ring under its ghost.
17. Detour: put a Claw in front of the Cyclone with a rock behind it. The cell past the rock in a straight line is not offered; the Claw's own cell is reached around the side, and the path arrows show that way round. The ghosts match it.
18. First frame: put the cursor on a reachable cell, then press the Steer key (no mouse move): the preview is drawn at once.
19. Previews survive the player's own hover refresh: move across enemies and empty cells while aiming; ghosts, tethers, damage and the landing cross never flicker off or stick on the wrong cell.
20. Hover and click an enemy standing on a newly offered cell (an enemy the Steer would shove): it aims the Steer and does not open the unit hover panel or an attack cursor.
21. Cancel the Steer: everything goes, the cross is back at full strength at the Cyclone. Click: the preview goes and the Steer plays. Press End Turn while aiming the Steer: the cross is back at full strength too.

## Carry and the closing Whirl (C1, C2)

22. Carry feel: riders glide with the Cyclone step by step and land once. Then a short pause (the swell and a short settle) before the pull. Time it: no long stall before the hit.
23. Watch: steer a Claw into Linda's lane. Watch fires on the landed Claw before the Whirl's pull and hit.
24. Several riders landing in Linda's lane in one Steer: only one Watch fires (known core limit: one Family Role answer per action). Note how it feels.
25. Act right after a Steer that carried an enemy (start Lucy's or another unit's action at once): nothing interleaves badly, the pull and hit wait for your action.
26. Spikes on a cell a carried enemy only passes over: no damage there. Spikes on its landing cell: they fire.
27. Harmonic Slam a Claw (Crippled), then carry it 3 cells: it takes only the Whirl's hit, no Crippled damage on the way.
28. Combat log: "Whirl · Lucy: carried N, pulled N, hit M". No "Gust" anywhere.
29. Masher beside the Cyclone does not counter a Steer's hit. With Howling Gale owned, the hit enemies show Weak.

## Heavies (C3a, C3b, C3c)

30. Masher counter walk through the Cyclone: hit the Masher with a family action so it counter-walks across the Cyclone's cell. It bursts it on entry (one hit on the Masher and on each enemy beside the Cyclone), keeps walking and slams. No second counter answers the burst. Log "Burst · Lucy: hit M".
31. Goblin Queen's charge through the Cyclone: one burst, the charge goes on. The Queen's jump over it does nothing to it.
32. On an enemy turn, a Masher or Queen may end its move on the cross; a Claw still keeps off the arms unless it attacks from there.
33. After a burst, during the short ring, the Steer button is already off; an archer's shot through the spent Cyclone's cell is allowed.
34. Wobble: with a Masher or Queen whose way to the nearest family unit runs through the Cyclone within one move, the Cyclone's sprite wobbles and its pips flicker. It starts or stops after turns start, abilities end and units move (not continuously). It stops when the heavy no longer heads through (moved away, died), once the Cyclone bursts, and at level end. A Claw never makes it wobble.

## Numbers and texts

35. Cyclone Power tooltips and hits: 3 / 4 / 5 at levels 1 / 2 / 3 (Lucy's damage 1); the previews show the same values.
36. Steer and Cyclone texts: final wording is the narrative pass (C5); note anything that still says the old rule.

## Known gaps to look at, not bugs

- The aim cross, tint, chevrons, tether and hazard ring are placeholder sprites made in code.
- The intent avatars of a heavy may under-predict a target reachable only through the Cyclone (the AI prediction does not use the heavy's walk-through; reported in C3c).
