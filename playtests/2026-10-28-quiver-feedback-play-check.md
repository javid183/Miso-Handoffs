# Play check: quiver feedback pass

For THJ, 2026-10-28. Branch `thj/linda-quiver`; the work is uncommitted. Plan `plans/2026-10-28-quiver-feedback-pass.md` (D-301 to D-305).

Sizes and timings are starting values. Tell me what to change, or tweak them yourself:
- `QuiverUI` fields in the Inspector (lift, punch, glow, tint);
- the constants at the top of `QuiverPipsView`, `GroundedArrowField` and `QuiverAimPresenter`.

## Before playing

1. Open Unity and let it recompile. Send me any errors.
2. Run EditMode > Run All. Only `AIRegressionTest.Baseline_MatchesCurrentAI` may fail.

## Under her feet

3. **Shift:** hold Shift with Linda on the board. Her arrow row sits on the top edge of her info panel and shows the right count. Let go: the row goes back under her feet.
4. **Neighbour:** put a unit on the tile just north of Linda and hold Shift. Her row never covers that unit's HP bar or panel.
5. **Empty:** spend all her arrows. The row under her feet shows a single grey arrow with a thin red slash. Hold Shift: it shows the same on her panel.

## HUD quiver (your prefab)

6. **Look:** the quiver is where you placed it, with as many arrows as she has. It shows only on her panel.
7. **Bow armed:** hover her bow on the bar, then press 1. The quiver grows a little, and shrinks back when you hover off or cancel.
8. **No arrows:** at 0 arrows, hover or press the bow, or press 1. The quiver pops bigger once and comes back. The quiver also has a muted tint while it's empty.
9. **Getting arrows back:** pick up arrows, have Mark catch one, and use Encore. Each time, the new arrows glow briefly and the quiver pulses.
10. **Nothing gets stuck:** switch units in the middle of a pop, and restart the level. The quiver is never left big or tinted when it shouldn't be.

## Board

11. **Arrows on tiles:** one arrow per tile, a bit right of where it was. A small `xN` appears when there are 2 or more. Arrows under an enemy are still a little darker and never cover an HP bar.
12. **Aiming:** the ghost arrow sits where the real arrow will land.
13. **Encore lines:** thinner and slightly see-through, with a shine moving from each arrow to Linda.
14. **Encore cost:** the button, the tooltip and the AP preview show 2. With 2 AP it spends 2. With 1 AP it can still be cast (you accepted this for now).

## Unchanged

15. Her shot, Watch, Mark's catch, pickups and restarts behave as before.
