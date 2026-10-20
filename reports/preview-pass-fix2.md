# preview-pass-fix2 (D-090)

Enemy threat arcs in `PlayerController` (~L982) now call `UnitThreatAnalysis.GetThreateningEnemies(ghostCell, previewFaction, cooldownTicksAhead: 1)`, matching the Shift danger zone. The method already had the `cooldownTicksAhead` parameter and never includes splash, so `UnitThreatAnalysis.cs` is unchanged. No existing test covers the ticks argument of that method, so no test change.

Verified: compiled, console clean, EditMode suite 273/273 run; only `AIRegressionTest.Baseline_MatchesCurrentAI` failed (known red). No Play mode.
