# Play check: quiver readability strip

Branch `thj/linda-quiver`. Report: `reports/quiver-readability-strip.md`. Nothing here was run in Unity by the implementer (the editor was open, no batch run).

**Before you start**
- Focus the editor so it compiles. Check the Console for errors.
- Test Runner > EditMode > Run All. Only `AIRegressionTest.Baseline_MatchesCurrentAI` may be red.
- Select `Unit_Linda.prefab` > `LindaQuiver` > Art: body, rim and the two arrow sprites are assigned.

**Setup.** Any level with Linda, John and Mark and a few enemies (M4 is fine). Select Linda so her unit panel shows.

1. **Panel quiver.** Linda's panel shows a quiver at the bottom right of her portrait, with 4 arrows standing out of its mouth and the dark rim over their lower ends. No pips and no "Quiver N/4" text on the panel.
2. **Spend.** Shoot the bow. One arrow leaves the panel quiver at once (the last one). Shoot until empty: the quiver is empty, and the role badge turns orange with its tooltip line.
3. **Pickup.** Walk any Bergson onto an arrow on the ground. The arrow comes back to the panel quiver, and the "+1" cue shows on Linda.
4. **Catch and Encore.** Have Mark catch an arrow, then use Encore. Each refills the panel quiver by the right amount.
5. **Other units.** Select John: the quiver is gone. Select Linda again: it is back, with the right count.
6. **Board text.** Nothing says "+N arrows" on a hovered move path, no "Arrows 3 > 2" beside Linda on her Watch prompt, and no numbers or badges on grounded arrows.
7. **Grounded arrows.** They use the new art (two kinds mixed). A stack of 2 or 3 shows overlapping arrows, and a stack of 5 shows 3. The same stack keeps the same look.
8. **Locked stack.** Let an enemy stand on an arrow: that arrow turns subtly dark (no orange, no outline, no badge). It goes back to normal when the enemy leaves or dies.
9. **HP bars.** Land an arrow under or next to an enemy. The enemy's HP bar is fully readable, never covered by the arrow.
10. **Aim ghost.** Aim the bow, then Explosive Crescendo: a faint ghost of the arrow sits on the landing tile. No ring. It moves as you move the mouse and goes when you stop aiming.
11. **Encore lines.** Hover Encore on the ability bar, then select it. A thin curved line runs from each stack to Linda, like John's role tether. It goes when you stop hovering. With no grounded arrows, no lines.
12. **Unchanged.** The small pips under Linda's feet and the "+1" cues look as before. A greyed arrow ability (empty quiver) still gives its reason in the tooltip.
13. **Panel placement.** Look at the quiver against the portrait and the health bar. Tell me if it covers the health bar, or if the arrows look wrong in the mouth. Placement numbers are in `QuiverHudRules` and `QuiverOverlapRight`.
14. **Restart.** Restart the level and quit to the menu and back. The panel quiver and the board arrows come back right.
