# Cyclone C5 review

Reviewer: `miso-reviewer` (read-only; saved by the coordinator), 2026-11-12. **Verdict: APPROVE.**

## Should fix (sent as a short round)
1. `EnemyAlertTracker.ForcedMove.cs:8`: add `if (AIWorker.IsWorkerThread) return;` like every other path into `WakeOne`.
2. `EnemyAlertForcedMoveTests.cs`: both tests pass on `!_levelActive`; seed the tracker by reflection and assert `UnitAlerted` fires once (depth 0), or label as smoke tests.
3. `CycloneSteerSetup.cs:28`: stale "placeholder until the narrative pass" comment → working text until THJ signs off; must match `Lucy_Ability_Steer.asset`.
4. `CycloneHowlingGaleTests.cs` `TheHitCompound_AppliesItsDamageAndWeakToTheSameTarget`: assert the parent's `targetType` is CellOccupant, or rename.

## Answers
- `WakeMovedUnit`: additive, one line over private `WakeOne` (same path as damage/taunt/evade wakes); main thread in practice; safe without tracker, outside a level, awake, dead; wakes only on a started pull, once per pull, Whirl and Gust. Spread measured from the cell pulled from (one cell off). Recommend adding `EnemyAlertTracker` to `core-systems.md` (THJ's call).
- Howling Gale: Targeted, CellOccupant, Enemy, no area shape, 2 turns; radius never read; works under `CycloneHitContext` by reading. Tests can fail (one weak).
- Watch/CSD reasoning correct (CSD returns unless `_commandInFlight`; pre-existing gap if a Command never completes).
- Texts: valid YAML, only intended fields; setup constant matches the asset.
- Commit order: F before C1 3; G last; compiles; metas with assets.
- Hygiene OK; no statics.
Open: Memory 4 / Lucy memory onboarding check (THJ play).
