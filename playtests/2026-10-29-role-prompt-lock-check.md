# Play check: Family Role prompt with a vanished target

For THJ, 2026-10-29. Branch `thj/linda-quiver`. The core fix is uncommitted (D-313). Report: `reports/role-prompt-destroyed-target.md`.

## Before playing

1. Stop Play mode, then press Ctrl+R. You should see no compile errors.
2. Run EditMode > Run All. Only `AIRegressionTest.Baseline_MatchesCurrentAI` may fail. New: `FactionRoleLivingTargetsTests` (13).

## Steps

3. **Recreate it:** in "A Wolf's Blood" 2/2 (or any level with Dark Worms):
   - get a worm low on HP;
   - with John, Shield Dash so the push moves it into Linda's row (or column), which starts its split;
   - when the Watch prompt comes up, wait a moment, then press.

   Expected:
   - no error and no lock;
   - if the worm is gone, the role is skipped and you get control back;
   - the spotlights stay smooth while it vanishes.
4. **Normal roles:** a regular Watch on a healthy enemy, John's role and Lucy's role look and play the same as before.
5. **Barks:** on a skip, the unit may still say its role bark. Tell me if that bothers you.
