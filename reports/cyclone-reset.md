# Report: Cyclone reset (straight Steer, knock, carry and wobble removed)

Plan: plans/2026-11-19-cyclone-reset-tech.md    Agent: miso-implementer    Branch: thj/cyclone
Outcome: partial (C1 of C1 to C5 built; compiled offline, tests not run)

## What changed

- C1 only so far; see the Chunks section.

## Acceptance criteria

Judged on the whole feature at the last chunk. C1 covers only the pure rules (knock, straight plan, cast knock).

## Chunks

### Chunk 1: Pure rules, knock and straight Steer plan (new files, nothing wired)

Built (all under `miso/Assets/_Project/Features/Player/Lucy/Scripts/`, LF, no BOM, namespace `MISO.Core.Features.Bergsons`):

- `Cyclone/CycloneKnockRules.cs`: `Right(dir)`, `Left(dir)`, `Landing(cell, onward, isFree)` (onward, right, left; null when none; null for a non-straight `onward`).
- `Cyclone/CycloneSteerPlan.cs`: data. `CycloneKnock { Unit, From, To }` (readonly struct, shared with the cast), `CycloneSteerPass { Unit, Cell }`, `CycloneSteerPlan { Start, End, Direction, Path, Passed, Knock }` (`Knock` is `CycloneKnock?`).
- `Cyclone/CycloneSteerPlanner.cs`: `CycloneSteerPlanRules { Self, IsEnemy, IsKnockable }` and the static `CycloneSteerPlanner` with `Lines(from, reach, rules)` and `PlanTo(from, to, reach, rules)`; also public helpers `CanKnock(unit, rules)` and `IsFreeLanding(cell, cyclonesCell, rules)` that the cast knock reuses.
- `Cyclone/CycloneRules.CastKnock.cs`: `CycloneRules.CastKnock(lucyCell, cell, rules)` returning `CycloneKnock?` (onward = first of `CastShoveDirections`, then the knock rule). Not wired; `CycloneRules.CastOnEnemy.cs` untouched.
- `Editor/CycloneKnockRulesTests.cs` and `Editor/CycloneSteerPlannerTests.cs`.

Grid y-axis finding: +y is screen-up. Evidence: `GridManager` gives each cell `verticalLayerAddUpFactor - cellCoords.y` as its vertical layer index (higher y sorts further back, i.e. higher on screen), and cell coordinates come from the Unity `Grid.WorldToCell` of the cell's world position with a normal 2D up axis. Moving screen-right, the right-hand side is screen-down: `Right(right) = (0,-1)`, `Right(down) = (-1,0)`, `Right(left) = (0,1)`, `Right(up) = (1,0)`; `Left` is the opposite. Each is pinned by one test row. The screenshot 2 layout confirms it by eye (the Cyclone sits on the bottom row and "above" is +y).

Criteria met (evidence, tests written but not run, see Not verified):

- Range lines (4 straight lines, up to 3, claw that can't be knocked stays unlit, cell beyond still lit): `Lines_*`, `ARefusedCellDoesNotHideTheCellsBeyondIt`, `AnEnemyCellIsOffered_OnlyWhenItHasALanding`.
- Screenshot 1 layout: `RowOfClaws_StopsOnTheFirstClawAndKnocksItToTheRightHandRow`, `RowOfClaws_KnocksToTheLeftHandRow_WhenTheRightHandCellIsTaken`.
- Screenshot 2 layout: `ClawAboveWithTheFamilyAround_StillOffersTheSteer_AndPassesEachClawOnce`.
- Cast knock (onward away from Lucy along larger axis, row at a tie, then right, then left, refused when none): `CycloneKnockRulesTests.CastKnock_*`.
- Passing rules (family, allies, neutral, no faction passed silently; heavy and large passed once, never a stop; a passed enemy never knocked): `Passed_*`, `AHeavyIsPassedAndHitOnce_NeverAStop`, `ALargeEnemyCountsOnce_*`.
- No destination at distance 0, off line, or beyond reach: `PlanTo_HasNoDestinationAtDistanceZero_*`; `PlanTo` equals `Lines` for every cell: `PlanTo_AgreesWithLines_ForEveryCell`.

Verified:

- Offline compile with Unity 6000.3.4f1's bundled Roslyn (`csc.dll`), referencing the project's `Library/ScriptAssemblies` and the UnityEngine modules, over the 4 new source files, the 2 new test files, `CycloneTestGrid.cs`, `CycloneTestFactions.cs`, `CycloneRules.cs` and `CycloneRules.CastOnEnemy.cs`. The new files produced no errors or warnings. The one error left (`AIWorker` is inaccessible in `CycloneRules.CastOnEnemy.cs`) is an artifact of compiling outside the real assembly (internals-visible) and is in an existing file I did not touch.

Not verified:

- No tests were run. The Unity MCP (`unity`) failed to connect (ECONNREFUSED), the editor is open on the project so batch mode can't be used, and so `CycloneKnockRulesTests`, `CycloneSteerPlannerTests` and `CycloneCastOnEnemyTests` are all unrun. Expected counts: I wrote them to pass by hand-tracing every case, but that is not a run. THJ or the coordinator should run those three fixtures from the Test Runner (EditMode, filter "Cyclone").
- Unity's own compile of the new files in the editor (the offline compile is a close proxy).
- `.meta` files: not created by me. The editor is open, so Unity will generate them on its next refresh (focus the editor). Stage them with the files once they exist.

Decisions and loose ends:

- Rules object has no `CellAt` delegate (the plan listed one). The planner steps through `GridCell.AdjacentCellsMap`, as the old carry planner did, so a missing neighbour is a wall or edge and tests use `CycloneTestGrid` holes. Same behaviour. If C3's preview needs to read a different board, add a delegate then.
- `IsKnockable` is the pull filter only (plan: "same as `IsPullable`"); the planner adds hostile (`IsEnemy`), one cell in size and alive. In the live game `IsEnemy` must be false for units without a faction (the planner itself treats only `IsEnemy` units as hit); `CycloneRules.IsEnemyOf` would throw for a null faction in the test level, so the tests guard with `unit.Faction != null`.
- Order of `Lines`: the four directions in `CycloneRules.StraightDirections` order (up, right, down, left), nearest cell first inside each. Not "nearest first overall" as the old `Explore` did; nothing consumes the order yet.
- A non-unit occupant on a line cell (a destructible crate, say) is crossed silently, same as the family, because the plan only ends a line at a missing cell or a walk-blocking planted entity. Check this at the play check if levels have such occupants.
- A stashed cell is crossed and never a stop (the plan's text doesn't mention it; the cast's empty-cell rule excludes it as a stop).
- Landing is "free" for a stashed cell: no. A planted hazard that doesn't block walking: yes.
- The knocked enemy's landing never equals another unit's cell, so passed enemies never move (they are occupied cells).
- Nothing else in the plan looked wrong. Heads-up for C2: a knocked cell can only be the stop; the Whirl pull's rule `IsLandable` is separate and unchanged.

Files to stage for C1 (the `.meta` files appear when Unity refreshes; add each next to its file):

- `miso/Assets/_Project/Features/Player/Lucy/Scripts/Cyclone/CycloneKnockRules.cs` + `.meta`
- `miso/Assets/_Project/Features/Player/Lucy/Scripts/Cyclone/CycloneSteerPlan.cs` + `.meta`
- `miso/Assets/_Project/Features/Player/Lucy/Scripts/Cyclone/CycloneSteerPlanner.cs` + `.meta`
- `miso/Assets/_Project/Features/Player/Lucy/Scripts/Cyclone/CycloneRules.CastKnock.cs` + `.meta`
- `miso/Assets/_Project/Features/Player/Lucy/Scripts/Editor/CycloneKnockRulesTests.cs` + `.meta`
- `miso/Assets/_Project/Features/Player/Lucy/Scripts/Editor/CycloneSteerPlannerTests.cs` + `.meta`

## Reviews and checks

- (coordinator fills in)

## Save reset

no

## Decisions I made

- C1: no `CellAt` delegate on the planner rules; adjacency map used instead (same behaviour).
- C1: `Lines` ordering is by direction then distance.

## Needs THJ

none

## Docs to update

- (at the last chunk)

## Risks and loose ends

- C1 tests are unrun (see Not verified). Run `CycloneKnockRulesTests`, `CycloneSteerPlannerTests`, `CycloneCastOnEnemyTests` before relying on them.

## Proposed commits

1. test and rules, C1: "feat(lucy): pure rules for the straight Steer and the knock, with tests": the six files above plus their metas (plain).

## Other branches

none

## How to see it

Not visible in game yet (C1 wires nothing). Run the fixtures in Window > General > Test Runner > EditMode, filter "CycloneSteerPlannerTests" and "CycloneKnockRulesTests".
