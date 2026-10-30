# Play check: Toba's swap triggers Linda's Watch

For THJ, 2026-10-29. Branch `thj/linda-quiver`, uncommitted. Plan `plans/2026-10-29-swap-ends-move.md` (D-322, D-323).

1. Stop Play mode, Ctrl+R; the Console is clear.
2. EditMode > Run All: only `AIRegressionTest.Baseline_MatchesCurrentAI` fails, message still CHECKS 710 FAILURES 39.
3. Level with Linda and Toba (Watch ready). Toba swaps an ally with an enemy so the enemy lands in Linda's row or column within her range: Watch fires on it, after the swap finishes.
4. Swap two allies, or put the enemy outside her lines: no Watch.
5. Toba swaps Linda with an enemy, ending in her line: Watch may fire on that enemy (allowed). No error.
6. A swap that fails (a target that can't be swapped or can't stand there): nothing fires.
7. Unchanged: John's push still triggers Watch; walking enemies still do.
