# Mark's catch: THJ's play findings, explained (Explore, read-only, 2026-10-27)

## A. The arrow passes Mark with no QTE; the return passes Linda
- **Passing Mark.** The arrow moves by transform once per rendered frame and has no sweep. Mark's overlap window along the path is about 0.43 units, so a frame of 80 ms or more can jump right over it; normal 60 fps play never does. Fix: a cast along the step on Linda's arrow calls Mark's `TryCatch`, combined with E. Non-core, S–M.
- **Return passes Linda.** Arrival is checked before the move and progress is never clamped, so the arrow overshoots by one frame's travel (large on a hitch). It also aims at her feet (the cell anchor). Fix: clamp the copy at its destination; set `destinationMode: 1` (Occupant) so it ends at her body. S.
- **Rare third cause:** a prompt already open, or the QTE pool empty.

## B. Lucy follows up although nothing was hit
- Lucy ranks the action's aimed target first, with no hit check (the D-152 rule). The completion echo also marks the aimed occupant as "hit".
- Before the catch the arrow always reached its target. Now the catch can stop it at Mark.
- `onUnitDamageDone` fires too late to use, because Lucy checks before the damage flush.
- Fix: snapshot enemy HP at activation and count only real HP drops, for rank 1 too when the action spawns a projectile. About 25 lines in `LucyFactionRoleHandler` (core).

## C. An enemy hit twice between Linda and Mark
- Confirmed: the return copy hits at factor 1.0.
- It is part of Linda's same action, so damage is flushed once.
- Every role reacts once at most: `onUnitDamageDone`, AP on kill, the Masher counter (one provocation) and Lucy (a set).
- Linda isn't hit when the copy arrives.

## D. Facts
- `minTileDistance` 2 is in the prefab and the GDD (kept, D-274).
- Cyclone copies are never caught: `GetClone` leaves `PrefabSource` null, and the catch rejects null. Copies would mostly fail the path and distance checks anyway, because those are measured from Linda's cell. No design doc covers it.

## E. Freezing the arrow closer to Mark
- Snap the frozen arrow to `returnSource` (Mark's body centre): 2–3 lines.
- On a decline it jumps back about 0.25 units to its path.
