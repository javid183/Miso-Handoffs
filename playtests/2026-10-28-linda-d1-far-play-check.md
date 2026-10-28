# Play check: Linda at a distance, Far Watch (D1-C1 and D1-C2)

Branch `thj/linda-quiver`. Reports: `reports/linda-d1-c1.md`, `reports/linda-d1-c2.md`. Text is placeholder; art is placeholder (an eye ring around a tilted arrow, in Linda's sky blue).

**Before you start**
- Focus the editor so it compiles, then run Test Runner > EditMode > Run All. Only `AIRegressionTest.Baseline_MatchesCurrentAI` may be red, and its message should read as before.
- Select `Assets/_Project/Features/Player/Linda/Data/LindaDistanceTuning.asset`: Far Watch on, near 5, Far 7.5, off 6, radius 2.
- Select `Unit_Linda.prefab` > `LindaQuiver` > Distance test: the asset is assigned.

**Setup.** A level with Linda, John and Mark, and Lucy too for steps 14 and 15 (M4 is fine). It helps to have a lane where an enemy walks into Linda's Watch.

**Damage numbers.** Shoot an enemy with the bow and note the hit without a crit: that is **X** (6 × her damage). Crits are ×1.5, so ignore crit hits. Expected:
- Watch near = 5/6 X;
- Watch Far = 1.25 X;
- Watch with Far Watch off = X;
- a second enemy pierced by the same arrow takes 0.6 of the first hit.

For example, with X = 12: near 10 (then 6), Far 15 (then 9), off 12. The hit numbers and the combat log's damage lines show each value.

## Damage (C1)

1. **Near, locked.** End the turn with John 2 cells from Linda (diagonals count as 1). In the enemy phase an enemy walks into her lane; accept Watch. Expect 5/6 X, and 0.6 of that on a second pierced enemy.
2. **Far, locked.** End the turn with no Bergson within 2 of Linda. Watch in the enemy phase hits 1.25 X.
3. **The lock holds.** Same as 2, and in that enemy phase an enemy pushes or pulls Mark next to Linda before another Watch. That Watch still hits 1.25 X.
4. **Who counts.**
   - Toba in the squad within 2 at End Turn: near (5/6 X).
   - A Lucy decoy (Blink, or Hide and Seek) within 2 and no Bergson within 2: still Far (1.25 X).
   - A downed or dead Bergson within 2: still Far.
5. **Live in the player phase.** On your turn, with nobody within 2, have Mark Command an enemy into Linda's lane. Watch hits 1.25 X. Move John next to her, Command again: 5/6 X.
6. **Turn 1 (the reviewer's check).** On the level's very first player turn, before any End Turn, with nobody within 2 of Linda: Mark Commands an enemy into her lane. Watch hits **1.25 X** (live, Far), not 5/6 X. Then put John within 2 and repeat on that turn: 5/6 X.
7. **Enemies first.** If a level opens with the enemy phase, a Watch then hits 5/6 X (she counts as near before the family's first End Turn).
8. **Only Watch.** Whatever her distance, the bow, Explosive Crescendo and the arrow Duos hit as in the setup (the bow stays X).
9. **Preview.** If a Watch target pick shows a damage preview on the enemy's health bar, it equals the hit (near and Far).
10. **Off.** Untick Far Watch on the asset (this works during Play). Watch hits X in every case above.

## Readability (C2)

11. **The mark.** On your turn, move Linda so no Bergson is within 2.
    - The mark (a sky-blue ring with an arrow) appears to the right of her arrow pips.
    - Move John within 2: it goes away. Move him out: it's back.
    - It draws under every unit's HP bar, including an enemy one tile below her.
12. **Lock pip.** End the turn while Far: in the enemy phase the mark stays, with a small white square beside it. End the turn near: no mark in the enemy phase.
13. **Ghost tile.** Select Linda and hover move destinations.
    - Where that tile would be Far (nobody within 2 of it, everyone else where they stand), the mark shows on the ghost tile.
    - Where it wouldn't, there's no ghost mark.
    - End the turn on a tile that showed the mark: step 12's lock pip appears. On a tile without it: no mark.
14. **"Far lost".** With Linda Far, select John (or Lucy, Mark, Toba) and hover a destination within 2 of her.
    - Over Linda: the mark struck through in red, with "Far lost" beside it.
    - Hover a destination farther away: back to the plain mark.
    - Tab-cycle paths to the same tile: same result.
15. **"Far" gained.** With only John within 2 of Linda (so she's near and has no mark), select John and hover a destination 3 or more from her: the mark appears over Linda. Hover back near: it goes.
16. **Box.** Hover Linda's role badge on her unit panel, or hold Shift.
    - The 24 tiles around her (2 cells, diagonals included, her own tile left out) tint faintly sky blue, over the grid and under the units, and only tiles that exist.
    - Release: gone.
    - It follows her if she moves while Shift is held.
17. **Prompt.** Trigger a Watch prompt.
    - The cost line reads `Arrows 3 > 2 · Far 7.5×` when Far, or `Arrows 3 > 2 · 5×` when near.
    - Check that `·` and `×` render, not as boxes. If the font lacks them the line reads `- Far 7.5x` instead.
    - In the enemy phase it follows the lock; on your turn it follows the live state.
18. **Tooltip.** Hover Linda's role badge.
    - Under the role description: `Watch: 5×. Far (no squad member within 2 at End Turn): 7.5×.`
    - If the panel's tooltip font lacks `·` or `×`, it reads `5x` and `7.5x`; note which you see.
    - Change near to 4.5 on the asset (in Play): the line says 4.5.
19. **Off.** Untick Far Watch.
    - No mark, no lock pip, no ghost mark, no "Far lost", no box.
    - The prompt is `Arrows 3 > 2` alone, and the tooltip has no Far line.
20. **Linda dead.** Kill Linda (cheat): no mark, no box on Shift. No errors.
21. **Restart and leave.** Restart the level, and leave Play mode, with the mark and the box showing: no errors in the console, and no leftover `FarMark` or `FarBox` objects outside Linda in the hierarchy.
22. **Performance.** With the Profiler's GC Alloc column, hold a Linda move preview on your turn. `LindaFarState`, `LindaFarMarkView`, `LindaFarPreviewPresenter` and `LindaFarBoxView` allocate nothing per frame.
