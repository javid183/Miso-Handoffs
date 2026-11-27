# Code read: the Masher doesn't move in M3 (Explore, 2026-11-26)

Written by the coordinator from the Explore report. THJ's play check: the revealed Masher never moves; the revealed Claw waves do.

**Cause (core bug, systemic):** `GridCell.GetRangeCells` (`Core/Systems/GridSystem/Runtime/GridCell.cs:901-905`) with `includeSelf` off removes every cell the mover occupies (`result.RemoveAll(source.Occupies)`), not just its anchor. The search starts from the anchor (line 872); the footprint grows +x/+y from the anchor (`GridPluggableEntity.TryGetFootprintCells`, 77-104). With the Masher's walk radius 1 (`MasherGoblin_Ability_Walk.asset`, radius `Stat_SPD` = 1, cooldown 1), the north and east anchors lie inside its own footprint and are removed, so it can only ever step south/west. At 6,1 in M3: west has no tile, south 6,0 once, then stuck. Same symptom as M1's play check ("stuck on its tiles", `playtests/2026-11-23-m1-play-check.md:7`). The AI live turn and the executed action both use this range (`AIUnitBrain.cs:277-289`, `FactionControllerBase.ComputeAbilityRangeCells` 483/496); the next-targets prediction (`AIUnitBrain.cs:291-318`) ranges from every footprint cell, so the preview can disagree. From commit `c6f19ddfc` (multi-tile occupancy); no test for a 2×2 radius-1 walk. The plow (counter step) has its own planner, unaffected.

Ruled out: awareness (`RevealUnitsSequence` → `HiddenLevelUnits.RevealUnit` → `RegisterUnit` → brain + alert tracker, same as the Claws); barricade targeting (legal, relation Enemy; the planner never plans for barricades, units hit them when in reach); objectives/planner (no throw path in M3); hidden 2×2 registration (fine).

**Fixes:**
1. Core: in `GetRangeCells`, for walk modes with a multi-cell source, remove only the anchor; leave the Unconstrained branch (attack ranges). Test: a 2×2 radius-1 unit reaches N/E/S/W anchors. Check `IsLegalAbilityTarget`/`OccupantIntersects` and the transporter's `FindPath(mover)` accept a destination overlapping its own footprint. Changes the Masher's (2×2) and the Goblin Queen's (1×2) walks everywhere.
2. Data workaround: M3 Masher `Stat_SPD` 2 on the level instance: reaches 6,3+, but always moves 2, never 1 north/east.
3. Plans say "the Masher steps to 6,3": impossible as coded; fix the timing note after the core fix.
