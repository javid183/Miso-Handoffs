# Play check: quiver switch, size stat, Encore kits, projectile clamp

For THJ, 2026-10-29. Branch `thj/linda-quiver`; the work is uncommitted. Plan `plans/2026-10-29-quiver-switch-size-encore-clamp.md` (D-314 to D-320). The steps are from `reports/quiver-switch-size-encore-clamp.md` › How to see it.

## Before playing

1. **Compile:** stop Play mode, then press Ctrl+R. The Console should be clear.
2. **Encore tool:** run Tools > Levels > Linda > Add Encore To Custom Kits. Expect "Encore added to 8 kit(s). 1 other level(s) still lack it", with a warning naming `LevelLindaJohn-C1`.
3. **Tests:** run EditMode > Run All. Only `AIRegressionTest.Baseline_MatchesCurrentAI` may fail. Tell me whether its message looks the same as before.

## Steps

4. **Size 3:** in a level with Linda (for example `LevelLindaJohn-C2`), the HUD quiver shows 3 arrows and the pips show 3. After three shots the bow greys.
5. **Size from the stat:** on `Unit_Linda`, set the `Stat_LQuiverSize` stat's level factor to 4, then play: 4 arrows and 4 pips. Discard the change afterwards.
6. **Slow frames:** cap the frame rate low (your `EditorFPSLimiter`). Fire Explosive Arrow at a cell:
   - the sprite stops on that cell and doesn't fly past or rise;
   - the grounded arrow lies on the aimed cell.

   Other projectiles look the same at normal fps.
7. **Switch off:** in `Resources/GlobalSettings`, untick Linda Quiver Enabled. Don't commit that asset. Then check:
   - no HUD quiver, pips or "+1";
   - shots are never blocked;
   - no arrows land on the board;
   - **Encore isn't on her bar**;
   - no quiver notes in the log;
   - no aim ghost.
8. **Mark's catch, switch off:** shoot through Mark and press the prompt.
   - The copy flies back to Linda and damages on the way.
   - Nothing goes into the quiver.
   - The enemies behind Mark and behind Linda aren't hit.
9. **Toggle back:** tick the switch on and go to the next level. The quiver is back, full at 3.
