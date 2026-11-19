# Review: Masher plow, C2 (miso-reviewer, saved by the coordinator)

Verdict: ESCALATE (Family Roles, already answered by THJ: no additive Linda fix) plus one must-fix and two should-fix inside the Masher's files.

## Must fix

1. `MasherGoblinFactionRoleHandler.Plow.cs`, `AddPlowCandidates`: a plow candidate checks only `_walk.Parameters.radius >= 1` and skips the walk's path-cost budget. Free candidates come from `ComputeTargetSelectionCells`, which applies it. The walk is an `AEffectTransporter` with `ignorePathCost: 0` and returns without moving when `cost > Radius`. A shoved unit on a costly cell would be planned as a valid step, get shoved, and the walk would do nothing (the preview would show a step that never happens). Fix: also require the budget (`GridPathFinding.PathFitsBudget(new List<GridCell>{ Unit.CurrentCell, cell }, _walk.Parameters.radius, <the transporter's IgnorePathCost, or false>)`, or the anchor cell's `GetCellCost()` at most the radius).

## Should fix

1. `MasherPlowGrid.cs` `CanEnter` / `HasNoStashOrBlockingPlant` reads `cell.PlantedEntity` (filters dead entities); `AEffectPusher.TryMoveTo` goes through `FindPathTo(..., mover)` and `mover.IsFootprintEmpty` (raw planted entity). A dead blocking plant passes the plan and fails the push: partial push and no step. Build `CanEnter` on `mover.IsFootprintEmpty(cell)`, keep the provoker exception.
2. Tests: the Immovable case passes a lambda, not the real `plowPushableTagQuery` (None + `EntityState.Unmovable`). Add a test of the real query refusing an Unmovable unit if tags can be set in edit mode. No handler-level `TryPlanAnswer` test (accepted; the play check carries it).

## Acceptance criteria

Met: free path unchanged; units pushed one cell onward (two on a 2 x 2 leading edge); skipped when blocked, Immovable or multi-cell (except the budget hole above); no damage or status (pusher asset has no move effects); abort safety (every exit ends in `Finish`, then `onCompletion`, then `_answerRunning = false`; `StopCounter`, `OnCounterTurnEnded` fine); preview and answer share one plan; preview clears; chain cap, queue, Duo, Stun and Crippled unchanged. Not met: Family Roles (see below).

## Other checks

No new stateful statics; shared Core untouched; conventions OK (new partial, no private IDs, LF, BOMs match siblings).

## Prefab and asset changes

- `Unit_MasherGoblin.prefab` (handler component): `plowPusher` -> guid `9663d4486ffdf1d438a6b4406e40af30`; `plowPushableTagQuery` = None, `EntityState.Unmovable`; plus Unity re-save noise on `qTEProfile` (`preloadOverride: -1`, `showSpeed: 1`), behavior-neutral.
- New `Attack/MasherGoblin_Ability_Counter_Effect_Push.asset` + `.meta`: `AEffectPusher`, speed 5, distance 1, `PushAgainst`, `dragStraightOnly`, no effects.
- `Move/MasherGoblin_Ability_Walk.asset`: re-saved by the builder with new default fields and ~11 filled attribute references. NOT part of the change; do not commit; discard with THJ's yes.
- `miso.slnx`: pre-existing, don't stage.
- One commit is right: code, asset, meta, prefab and builder only work together.

## Linda finding (correct) and THJ's answer

Only Linda's role reacts to a move (`OnUnitEndMoving`, checked late through the wait list). With `counterCanProvokeFamilyRoles` on, a pushed enemy landing in her lane can still draw her shot. Reviewer's smallest additive fix: a `HashSet<GUnit>` of suppressed movers in `FactionRoleProvocationSuppression` (`SuppressMover`, `ReleaseMover`, `IsSuppressedMover`, cleared in `ResetPlayModeState`) plus one check line in `LindaFactionRoleHandler.CheckTriggerConditions`, and the Masher suppressing each pushed unit around its push. **THJ declined it (2026-11-18, D-566 amended): known gap.**

Also noted by the reviewer: with the toggle off there is a small gap when pushes happen but neither the walk nor the slam follows (a later push fails to start, the footprint stays occupied, or the Masher dies): the last action is the provoker's, which isn't suppressed. Same gap, same decision.

## Notes

- Pushes run on the Masher's `GUnit`; if its GameObject is deactivated or destroyed mid-push a pushed unit may be left unplugged between cells (teardown only). Fix the `StopPlow` comment.
- Partial push: a later `TryMoveTo` failing after an earlier one started shoves units and the Masher doesn't step (rare; re-plan runs the same frame).
- Existing `AEffectPusher` behavior (out of scope): a unit that dies mid-lerp is plugged onto the destination anyway.
- Duo preview: the Duo activator, if not the answered partner, may show as pushed though it will move away.
- `thj/cyclone` will conflict in `.Counter.cs`; note it in `branches.md`.
- Play check (THJ's time): hazard cell in the way, wall and grid edge, two units on the leading edge, an Immovable unit, Linda in lane with the toggle on and off.
