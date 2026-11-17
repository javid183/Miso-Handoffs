# Review: Cyclone round 2, C3b (the burst), branch `thj/cyclone`, uncommitted

Reviewer: `miso-reviewer` (saved by the coordinator). Verdict: **APPROVE**. Implementer run: EditMode 2081/2082, known red only, count 43.

## Should fix
1. A spent Cyclone still counts as present to the AI and the shot checks until it is disposed: `CycloneEntity.AIDanger.cs:17` and `CycloneEntity.LineOfFire.cs:17`. After a burst `CollectDangerCells` still lists the arms and `CollectLineOfFireBlockers` still blocks enemy shots, for the 0.3 s ring or longer if a Whirl's reaction wait (up to 15 s) or a Steer defers the dispose. Fix: add `|| HasBurst` to the early return in both (`HasBurst` is a plain auto-property, worker-safe); one assert in a burst test.
2. The burst does not refresh the Steer button: `CycloneEntity.Burst.cs:76`. `CanBeSteered` turns false at the burst but `NotifyReadyChanged` only runs at dispose, so the button can look ready for 0.3 s or more (a click only logs "Steer not done"). Fix: call `NotifyReadyChanged()` right after `HasBurst = true`.

## Notes
- Hook confirmed: `AEffectTransporter.MoveEntity` (line 370) plugs the unit on every path cell and `GridCell.PlugEntityInternal` (791-795) activates every planted entity under the footprint; Queen's charge (Transporter, `moveMode: 0`) and the Masher counter walk (`DefaultEmptyCellAbility`) burst it. Jump and teleport plug only on the landing cell. Pusher and Command walks also plug per cell: a pushed or commanded heavy enemy crossing the cell bursts it too (matches "plugs onto or enters"). Swaps, spawns and `Resurrect` plug only on occupiable cells.
- No false bursts: the AI simulation (`SimMoveTo`/`SimAssignOccupant`) never calls `Activate`; the cast cell is empty and a Steer ends only on a free cell; undo never moves the Cyclone.
- Factions: heavies of any faction pass through (C3a), but only units whose relation to Lucy's faction is Enemy burst it; a neutral, allied or family heavy walks through and leaves the Cyclone standing. Tell the designer for the GDD.
- Mid-walk kill: if the burst kills the heavy it dies inside `PlugEntityInternal`; the Transporter yield-breaks on its next `IsAlive` check without `MovementEnd` (as a hazard kill does); the Masher's `Attack()` checks `Unit.IsAlive` and calls `Finish(false)`. A walk stopped short on the Cyclone cell re-plugs there; `HasBurst` blocks a second burst. End to end is a play check.
- Holds and dispose: every combination of burst, Whirl, Steer and pending pulls disposes once; the burst's hold has its own owner object, released in `finally`; level unload clears holds; `CycloneRegistry.Register` drops dead entries; no new statics.
- Tests are real, but in EditMode `isActiveAndEnabled` is false so the tests that go through the real plug take `TryBurst`'s synchronous branch; starting the coroutine with its hold through `Activate` is covered only in play. `AJumpPastTheCyclone_DoesNotBurstIt` is close to a tautology (harmless).
- CRLF without BOM (as HEAD), `.meta` for the five new files, no private IDs, "Gust" only in a DoesNotContain assert, log line `Burst · Lucy: hit M`, no core file touched in C3b.
- Commits: folding the `CycloneHeavyPassTests.cs` fix into the C3a commit is simplest; the `CycloneEntity.Whirl.cs` / `Steer.cs` hunks need `git apply --cached` or the pre-C3b copies.
- C4: the 0.3 s `BurstSeconds` duplicates the cross view's private `BurstTime`; they must change together.
