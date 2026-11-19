# Masher core fix: review

Reviewer: miso-reviewer (text saved by the coordinator). Verdict: **FIX** (one must-fix; the fix stays inside the approved scope).

## Must fix

1. The new landing guards (`GridCell.cs:945-950` `PassesEmptyFilter`, `AreaShapeDefinition.cs:150-151`, `AIUnitBrain.Landing.cs:14-16` `CanEndMoveOn`) use `!GridCell.FootprintHasWalkBlocker(cell, source)`. `HasWalkBlocker` skips only a planted entity that is the source, while `IsFootprintEmpty` also skips cells the source occupies. So on a board without a Cyclone, a unit standing on a cell holding another planted `DisallowWalk` entity (`AOE_Attack` telegraphs incl. Masher/Queen variants, `CP_Spawner`, `MushroomExplosion`, `Toba_Wall`) now loses its own cells from a `SelfWalkable` `includeSelf` range, loses overlapping multi-cell origins, and the AI refuses those cells for jumps/summons/cell attacks. Fix: guard only the new allowance. Add `FootprintEndsOnClearing(origin, source)` in `GridCell.PlantedPass.cs` (true when some footprint cell not occupied/planted by the source has `!IsWalkable && PlantedClearsFor(source)`) and use `!FootprintEndsOnClearing(...)` in all three places. Add a test: a unit on a rock-like `DisallowWalk` planted cell keeps that cell in a `SelfWalkable` `includeSelf` range and in `CanEndMoveOn` for a non-walk ability.

## Should fix

1. `CycloneHeavyEndsOnItTests.ABurstingCyclone_StillLetsAHeavyEndOnIt_ButBurstsNoMore` (~240): the Queen occupies the Cyclone cell, so the self-occupant rule hides the ring-time rule; place the burster off the Cyclone cell (or call `BurstRoutine(queen)` with her elsewhere) and assert `PlantedClearsFor(other)` and `IsFootprintEmpty(origin covering the cell)` during the ring, false after.
2. AI candidate loop: compute `WalksThere(ability)` once per ability before the loop (`AIUnitBrain.cs:419-427`); avoid a per-cell `List<GridCell>` allocation on the worker thread (reuse a buffer, or only run when a footprint cell is `!IsWalkable`).

## Notes

- Core surface beyond the approved shape (named for THJ): `GridCell.cs`, `AreaShapeDefinition.cs`, `AEffectTransporter.cs` (read-only `MoveMode` getter), `AIUnitBrain.cs`, new `AIUnitBrain.Landing.cs`. Needed to keep jumps, summons and teleports from landing on the Cyclone (Queen's jump is `PathWalkable`; Mountain Deev's summon is `SelfWalkable`). Justified; exactly additive after the must-fix.
- Every `IsFootprintEmpty` / `PassesEmptyFilter` caller matches the report's table; dash approach, duo stop and ranged reach were already guarded.
- Worker-thread safe, deterministic, no new statics.
- No double burst (`HasBurst` set synchronously); a second heavy may end on the cell during the ring only if unoccupied (harmless); nobody ends on a disposed Cyclone.
- Mark's Command can walk a heavy enemy onto the Cyclone and burst it: a combo, THJ's design call; GDD CR-58 / LU-7 should mention it.
- Loose end: AI intent prediction uses the sim range without a mover, so predicted heavy moves never show ending on the Cyclone while live turns can.
- Line endings, BOM, `.meta` files, no private IDs: OK. `tech/core-systems.md` wording must follow the must-fix.
