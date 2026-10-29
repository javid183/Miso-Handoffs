# Play check: quiver polish 2

For THJ, 2026-10-29. Branch `thj/linda-quiver`; the work is uncommitted. Plan `plans/2026-10-29-quiver-polish-2.md` (D-306 to D-309). The steps come from `reports/quiver-polish-2.md` › How to see it.

## Before playing

1. Press Ctrl+R and send me any errors.
2. Run EditMode. Only `AIRegressionTest.Baseline_MatchesCurrentAI` may fail. The new tests are `KillHandBackTests`, `ArrowLandingAfterMoveTests` and one case in `QuiverHudFeedbackTests`.
3. Open `Unit_Linda.prefab`. Under LindaQuiver › "Kill hand-back" you should see John's sword and Toba's axe. If the list is empty, Unity overwrote the on-disk edit. Tell me, don't save.

## Steps

4. **Arrow abilities:**
   - Hover the bow, Explosive, and the Lucy and Toba Duo buttons, or press their number keys. The HUD quiver grows for each.
   - Encore, Harmonic Slam and Walk don't make it grow.
5. **At 0 arrows:** each arrow ability pops the quiver once when hovered or pressed. Encore doesn't.
6. **`x2`:** with two arrows on one tile, the count sits about one label width further left, still under the HP bars.
7. **Melee hand-back:**
   - Land an arrow under an enemy, then kill it with John's primary. The arrows fly back to Linda at once, with the toss, the "+N" and the HUD glow.
   - John's log line ends with `· +N arrows, quiver N/4`.
   - Repeat with the playable Toba's primary.
   - Watch for a short bright flicker of the stack before it flies back.
8. **Other kills:** kill an enemy standing on arrows with Linda's bow, Lucy or a hazard. The stack turns bright and stays on the tile.
9. **Walk then shoot:**
   - With the bow selected, hover an enemy she has to walk to. The ghost arrow sits where the arrow will land after the walk. Click and check that the arrow lands there.
   - Hovering an ally gives no walk-then-shoot ghost.
10. **Outline:** the HUD quiver has a thin dark outline that holds up during the grow, the pop, the empty tint and the glow. You can untick it, or change its width, under `QuiverUI` › Outline on the HUD prefab.
