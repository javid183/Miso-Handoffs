# Play check: quiver strip-down, tweaks, arrow bodies and the projectile sweep

For THJ, 2026-10-28. Branch `thj/linda-quiver`; all of this is uncommitted. One round covers the strip-down (D-293, D-297, D-298), the tweaks (D-299), the arrow bodies (D-296) and the core sweep (D-300).

## Before playing

1. Let Unity recompile and send me any errors. Unity also creates a few `.meta` files.
2. Run Test Runner > EditMode > Run All. Only `AIRegressionTest.Baseline_MatchesCurrentAI` may fail. New tests: `ProjectileSweepTests`, the `HeldAction_*` tests in `CombatLogTests`, `QuiverLogLinesTests`, and the art and Rigidbody tests in `QuiverWiringTests`.

## Look

3. **No arrow text anywhere** on the board or the panel; only tooltips use words.
4. **HUD quiver:** it sits at the top-left of Linda's portrait, with one arrow inside per arrow she has. It updates on shot, pickup, catch and Encore, and hides when another unit's panel shows.
5. **Pips under her feet and the "+1" cue:** both are about half their old size. Say if they're still too big.
6. **Arrows on tiles:** they use your art. Up to 3 overlap on a stack, an arrow under a living enemy is a little darker, and they never cover an HP bar.
7. **Aiming:** a faint ghost arrow on the landing tile, and no ring.
8. **Encore:** curved lines from each stack to Linda.

## Hits (Mark out of line, Lucy out of the party)

9. **Still worms:** shoot worms that haven't moved for a while. Every one takes damage.
10. **Adjacent and sideways:** let a Dark Claw step next to Linda in her row so Watch fires. It's hit.
11. **Slow frames:** cap the frame rate at 10 with a throwaway script (`QualitySettings.vSyncCount = 0; Application.targetFrameRate = 10;`), then shoot down a column of two or three worms.
    - Every worm is hit.
    - The first one takes the full hit and the later ones less.
    - The damage matches the preview.

    Then repeat at 60.

## Combat log

12. **Shot lines:** her shot and Watch lines end in `· quiver N/4`.
13. **Pickup lines:** a move that picks arrows up ends in `· +N arrows, quiver N/4`.
14. **No separate lines:** there are no separate "Quiver:" lines.
15. **Restart:** restart from the pause menu right after a shot. The new attempt's log doesn't start with the previous attempt's line.

## Unchanged

16. Mark's catch, Encore, pickup and the level-start and restart fixes behave as before.
