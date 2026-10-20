# masher-c2 review (miso-reviewer, 2026-10-20; saved by the coordinator)

Verdict: **APPROVE**

- All rules match D-092 to D-100 and plan C2; no static state, no Unity-object APIs; BOM + LF; in scope. 44 tests assert real values incl. 2 × 2 cases. Spec-gap choices sensible (D-112); cap as a sealed class is fine.
- Should fix (carried into C4's brief): `MasherCounterRules.cs:144-150` `Classify` doc comment must name every caller-side exclusion (Pass-by, allied AI units such as Toba as ally and the Deer) and define `ownerIsPlayerFaction` as a player-controlled family unit.
- Notes for C4: `PickAttackCell` returns the first adjacent cell in `OccupiedCells` order (2 × 2 targets; watch in play). Compute Duo "reachable" with the same rule as the step (adjacent, or `RankStep` finds a cell).
- Keep Packages/ProjectSettings out of the commit; stage the three `.meta` files.
