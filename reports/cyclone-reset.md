# Report: Cyclone reset (straight Steer, knock, carry and wobble removed)

Plan: plans/2026-11-19-cyclone-reset-tech.md    Agent: miso-implementer    Branch: thj/cyclone
Outcome: partial (C1 and C2 of C1 to C5 built; C2 compiled in the editor, covering fixtures 323/323)

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

- C1: 77/77 covering fixtures (coordinator, Unity MCP); committed `d9cb1f2ce`.
- C2: 323/323 covering fixtures (implementer, Unity MCP); coordinator checked the 36 paths, no CRLF, no private IDs; committed `15a107cbd`. Feature review after C5.
- C3: 319/319 Cyclone fixtures (implementer, Unity MCP); coordinator checked 4 files, no CRLF, no private IDs; committed `774dabef7`.
- C4: Cyclone fixtures 314/314 (5 wobble tests deleted); committed `d8db54ddf`. C5: committed `359882aed` (descriptions, LF kept).
- Full EditMode suite after C5 (coordinator, Unity MCP): 2345 total, 2344 passed, 0 failed, 1 skipped (the Explicit AI regression test), 147 s.

## Save reset

no

## Decisions I made

- C1: no `CellAt` delegate on the planner rules; adjacency map used instead (same behaviour).
- C1: `Lines` ordering is by direction then distance.
- C2: pass hit on arrival at the cell; Cyclone relocates before the knocked enemy's end-of-move event; no more pass hits after a burst; Steer log always written (unless the level ended), untagged; cast keeps "same landing or no knock"; shared fling in new `CycloneKnockMotion`; `CastShoveFor` → `CastKnockFor`. Details in Chunk 2.

## Needs THJ

none

## Docs to update

- (at the last chunk)

## Risks and loose ends

- C1 tests are unrun (see Not verified). Run `CycloneKnockRulesTests`, `CycloneSteerPlannerTests`, `CycloneCastOnEnemyTests` before relying on them. (Since run: 77/77, and again inside C2's 323/323.)
- C2: a passed enemy can still be pulled in by the closing Whirl (left out of the hit only); play-check item.
- C2: until C3, the Steer preview shows no pass damage and may mark a passed enemy as Whirl-hit.

## Proposed commits

1. test and rules, C1: "feat(lucy): pure rules for the straight Steer and the knock, with tests": the six files above plus their metas (plain). Committed `d9cb1f2ce`.
2. runtime, C2: the 36 paths listed under Chunk 2 "Files to stage" (including 4 deletions), one commit: "feat(lucy): the Steer glides in a straight line through enemies, hitting each once, and knocks the one where it stops; the cast on an enemy uses the same knock; the carry is gone".

## Other branches

none

## How to see it

Not visible in game yet (C1 wires nothing). Run the fixtures in Window > General > Test Runner > EditMode, filter "CycloneSteerPlannerTests" and "CycloneKnockRulesTests".

**C1 verified and committed (coordinator, 2026-11-19).** Unity MCP: forced refresh, compile clean, console 0 errors, metas generated. Covering fixtures `CycloneSteerPlannerTests`, `CycloneKnockRulesTests`, `CycloneCastOnEnemyTests`: 77/77 passed. Coordinator read `CycloneSteerPlanner.cs` (no findings). Committed `d9cb1f2ce` (12 files). Review comes with the feature.

### Chunk 2: Runtime, Steer and cast use the new plan; carry removed

Built (all under `miso/Assets/_Project/Features/Player/Lucy/Scripts/`, LF, no BOM, no new statics):

- `Cyclone/CycloneEntity.Steer.cs` rewritten. `TrySteer(CycloneSteerPlan)` (refuses a plan that doesn't start on the Cyclone's cell). `SteerRoutine(CycloneSteerPlan, holdOwnerSource)`: straight glide over `plan.Path` at `steerSecondsPerCell`; on reaching each path cell, every `Passed` entry on that cell gets `WhirlSteps.Hit` + `Report` (skipped when the unit is dead, the Cyclone has burst or the level ended); at `End`: safety net, then the knock (`ShoveSteps.ShoveStarted`, `CycloneKnockMotion.Fling` with `flingSeconds`/`hopCells`, `Unplug`, `Plug`), then `Relocate`, then `Landed` (end of move + wake) and `NoteMovedThisAction`; then the Steer log line; then `WhirlRoutine(hold, afterKnock: KnockLanded, skipHits: hitOnTheWay)`. New `ShoveSteps` seam on the entity (`ICycloneShoveSteps`, real `CycloneShoveSteps`). `CarryLanded` renamed `KnockLanded`. `finally`: re-plug a knocked unit left off its cell, restore knock drawings, put a mid-fling unit's drawing back, put the Cyclone's own drawing back on its cell if it never relocated, clear flags, deferred dispose. `CarryLanding`, grab/drag/fling-of-riders code gone.
- Safety net (fixed at the click): a planned knock must still hold (unit still on the stop, still knockable, nothing planted/stashed there, landing still free); an empty stop must still be empty. If not, `CycloneSteerPlanner.TryStopOn` re-reads the stop live (may knock a newcomer, or send the knock to the right/left); if that fails, the Cyclone goes back to its start (no relocation, no knock) and still Whirls there. After the fling, the landing happens only if the unit is still there and the landing still free; the Cyclone takes the cell only if it is empty by then.
- `Cyclone/CycloneEntity.Whirl.cs`: `WhirlRoutine(hold, bool afterKnock = false, IReadOnlyCollection<GUnit> skipHits = null)`; step-0 reaction wait now keyed on `afterKnock`; both `HitTargets` calls (before the breath and the recompute after it) drop `skipHits`; log is `Log(pulled, hit, targets)`. Cast and enemy-turn Whirls pass nothing, so they are unchanged.
- `Cyclone/CycloneEntity.Wind.cs`: fields `grabSeconds`, `grabDepthCells`, `dragLag`, `dragTiltDegrees`, `kickPortion` removed (none was in any prefab/asset YAML, checked by grep); `OnDisable` restores the knock steps' drawings instead of the Steer steps'.
- `Cyclone/CycloneKnockMotion.cs` (new): the fling coroutine shared by the cast's knock and the Steer's knock (the cast's former inline loop, same timing and hop).
- `Cyclone/ICycloneSteerSteps.cs` / `CycloneSteerSteps.cs`: down to `PositionOn`, `DeltaTime`, `Relocate`, plus new `Log(hitOnTheWay, knocked, targets)` → `GlobalEventBus.RaiseSynergy(caster, "Steer", "hit N on the way, knocked K", targets)` (targets = passed units hit + the knocked unit). `CycloneSteerSteps.LogId = "Steer"`.
- `Cyclone/ICycloneWhirlSteps.cs` / `CycloneWhirlSteps.cs`: `Log(pulled, hit, targets)`; `CycloneRules.WhirlLogDetail(pulled, hit)` = "pulled N, hit M"; new `CycloneRules.SteerLogDetail(hitOnTheWay, knocked)`.
- `Cyclone/CycloneSteerRules.cs`: now only `DefaultReach`, `RulesFor(cyclone)` → `CycloneSteerPlanRules` (IsEnemy = `unit is { Faction: not null } && whirl.IsEnemy(unit)`, IsKnockable = `whirl.IsPullable`), `CanEndOn`, `SteerActionOpen(..., knockLanded)`. `IsFriendly`, `Explore`, `Destinations`, `PlanTo`, `PathTo`, `CanSteerTo`, `Search` removed.
- `Cyclone/CycloneSteerPlanner.cs` (C1 file): private `TryStop` made public as `TryStopOn` (plus a null guard) for the safety net. Same rule.
- `Cyclone/AEffectCycloneSteer.cs`: range = `CycloneSteerPlanner.Lines(...).End`; target check and execution through `PlanFor` → `CycloneSteerPlan` (re-planned at the click, passed to `TrySteer`); `PathFor` gone; `WaitForSteer` reads `KnockLanded`. AI gate unchanged.
- Cast on an enemy: `CycloneRules.CastOnEnemy.cs` keeps `IsEnemyOf`, `IsPullableBy`, `CastShoveDirections`; `CastRulesFor` now returns `CycloneSteerPlanRules` (faction-null guard on IsEnemy; knockable = pullable and not heavy); `PlanCastShove`, `CastShoveCell` and the 3-argument `IsValidCastCell` removed (unused). `AEffectCycloneSpawner`: `CastShoveFor` → `CastKnockFor` returning `CycloneKnock?` via `CycloneRules.CastKnock`; `ShoveThenCast(owner, cell, CycloneKnock? knock, spawn)` uses `CycloneKnockMotion`; the landing still requires the re-planned knock to give the same unit and landing (unchanged behaviour: otherwise the enemy stays and nothing is cast).
- Removed: `Cyclone/CycloneCarryPlanner.cs` + `.meta` (all its types), `CycloneWindMotion.Trail`/`Kick`.
- Preview, minimal to compile (C3 owns the rest): `CycloneOutcomePlanner.ForSteer(CycloneSteerPlan, ...)` (moves = the knock only, Whirl at `End` with `Start` vacated on the board after the knock) and `ForCast(..., CycloneKnock? knock)`; `CycloneSteerPreview.Plan` is a `CycloneSteerPlan`, path arrows = `Start` + `Path`, landing = `End`; `CycloneCastPreview` calls `CastKnockFor`. Passed units are NOT yet removed from the preview's Whirl `Hit` and there is no `PassHit` (C3).
- Comments updated where they named the carry (`CycloneEntity.Burst.cs`, `CycloneShoveSteps.cs`, `ICycloneShoveSteps.cs`, `CycloneWindMotion.cs`, `CycloneOutcome.cs`).

Tests:

- Deleted `Editor/CycloneSteerTests.Carry.cs` + `.meta`. New `Editor/CycloneSteerTests.Knock.cs` (15 tests): hits on the way in path order at the cell (position checked), each once, not re-hit by the Whirl, no move events for passed units; heavy passed and hit once; family/ally/neutral crossed without a trace; an enemy dying mid-glide changes nothing; knock lands once, only the landing hazard fires, order start → unplug → plug → relocate → landed, before the Whirl, Whirl hits the knocked enemy; knock to the right when onward is taken; Crippled guard (no effect field on `CycloneShoveSteps`/`CycloneSteerSteps`); action closes after the knock and the pull waits for reactions; no knock → pull without waiting; plan is what happens (every enemy hit once); safety net ×3 (newcomer on the stop is knocked; landing taken → knocked right; stop untakeable → back to start, no knock, Whirls there); stop mid-glide; knock cut short (plug throws) → re-plugged.
- `Editor/CycloneSteerTests.cs` rewritten for straight lines (reach, no corner/diagonal, stops vs crossing, walk blocker, wall), Plan helper, recorders implement the new interfaces, Whirl/Steer log tuples, "nothing carried" test, `SteerActionOpen` cases renamed for the knock, log-line test for both lines.
- `Editor/CycloneSteerTests.Preview.cs`: ghost test rewritten for the knock (board: Brute knocked onto spikes, Shaman pulled; preview = execution); `SteerPreview_ACellPastABlockedFront…` deleted now (it tested the way-round path, which no longer exists and failed in C2; the plan had it in C3).
- `Editor/CycloneWindBeatsTests.cs`: rider tests deleted (grab, join part-way, riders' time, stop during grab), `Trail`/`Kick` asserts removed; new knock-fling test (exact landing, hop, no overshoot, recoils instead of leaning), Steer time with a knock (0.42 s) and without (0.3 s, a passed enemy doesn't move), stop mid-knock (drawing back, enemy and Cyclone on their cells).
- `Editor/CycloneCastOnEnemyTests.cs`: `CastKnockFor`; diagonal and blocked-onward tests rewritten for right-then-left; new "refused when onward, right and left are all blocked"; the empty-cell test now asserts a knockable enemy cell is a Steer stop.
- `Editor/CycloneBurstTests.cs`: burst during a Steer rewritten (no more hits on the way after the burst, the knocked enemy still lands, nobody hit twice, the Cyclone goes). `CycloneWhirlTests.cs`, `CycloneHeavyEndsOnItTests.cs`: `Log` signature.

Verified:

- Unity MCP forced refresh + compile: `Assembly-CSharp.dll` and `Assembly-CSharp-Editor.dll` rebuilt (17:33), console 0 errors, 0 Cyclone warnings; metas generated for the two new files.
- Covering fixtures (regex groups `MISO.Core.Features.Bergsons.EditorTests.Cyclone*`, `MasherCounterCycloneTests`, `MasherCounterWhirlTests`, `MISO.Core.Systems.EnemyAlertSystem.EditorTests.EnemyAlertForcedMoveTests`): **323/323 passed**, 0 failed, 0 skipped. Separately the three non-Cyclone fixtures: 8/8 (3 + 2 + 3, matches their test counts).
- Grep: no reference left to `CycloneCarry*`, `CarryLanded`, `CarryStarted`, `PathFor`, `CycloneSteerRules.PathTo/PlanTo/Destinations/Explore/CanSteerTo/IsFriendly`, `IsValidSteerPath`, `PlanCastShove`, `CastShoveCell`, `CastShoveFor`, `Trail`, `Kick`, old `Log(carried, ...)`. No private IDs in code. LF, no BOM, no CR in the changed files.

Not verified:

- Full EditMode suite (not asked for this chunk; due after C5). AI regression test not run (no AI content touched).
- Nothing seen in Play mode: pass-hit timing, the knock fling in a level, Watch answering the knock, the combat log lines on screen.

Decisions (same behaviour as the plan, or choices the plan left open):

- Pass hit fires when the glide reaches the passed cell (arrival), not half-way into it. One frame of difference per cell; tunable after the play check.
- Knock event order: unplug, plug (landing hazard fires), then the Cyclone relocates, then `Landed` (end of move, wake). The plan lists "knocked enemy lands (… end-of-move …) → the Cyclone takes the cell"; I kept the old carry's order (Cyclone placed before the end-of-move event) so Watch reads the final board. All in one frame.
- After a burst mid-Steer, the remaining hits on the way are skipped (a burst Cyclone hits no more), but the knock still lands and the Cyclone still relocates before it goes (as the plan's burst test asks).
- Steer log line: always logged after the knock unless the level ended (also "hit 0 on the way, knocked 0"); targets = units hit on the way + the knocked unit. Not tagged `[PLACEHOLDER]` (log details aren't tagged anywhere, the Whirl's included); wording is working text.
- Cast knock keeps the old cast's "landing must be the planned one" check (no live re-route for the cast; the plan's safety net is the Steer's).
- `ShoveThenCast` keeps its name and takes `CycloneKnock?`; `CastShoveFor` renamed `CastKnockFor`. Existing cast test names that say "Shove" were left as they are.
- The shared fling went into a new `CycloneKnockMotion` (one new file + meta) rather than duplicating the loop.
- `CycloneSteerRules.RulesFor` guards a null faction with a pattern check (`unit is { Faction: not null }`), safe off the main thread.

Findings / loose ends:

- A passed enemy can still be pulled by the closing Whirl (it is only left out of the hit). Example: Cyclone passes an enemy and stops two cells beyond it → the Whirl pulls it in beside the Cyclone, unhit. This follows the plan ("skips every unit already hit") but may read oddly; THJ to judge at the play check. Covered by `ThePlanIsWhatHappens_EveryEnemyHitOnce`.
- Preview between C2 and C3: the Steer preview's Whirl hit still includes passed units that end beside the Cyclone, and shows no pass damage; C3 fixes both.
- `CycloneWindMotion.Fling` still takes a starting offset/tilt that the knock always passes as zero (the old riders used them); harmless, left for the review.
- Plan said C3 deletes `SteerPreview_ACellPastABlockedFront…`; it had to go in C2 (it fails without the turning search).

Files to stage for C2:

- Modified (Cyclone): `AEffectCycloneSpawner.Shove.cs`, `AEffectCycloneSpawner.cs`, `AEffectCycloneSteer.cs`, `CycloneCastPreview.cs`, `CycloneEntity.Burst.cs`, `CycloneEntity.Steer.cs`, `CycloneEntity.Whirl.cs`, `CycloneEntity.Wind.cs`, `CycloneOutcome.cs`, `CycloneRules.CastOnEnemy.cs`, `CycloneRules.cs`, `CycloneShoveSteps.cs`, `CycloneSteerPlanner.cs`, `CycloneSteerPreview.cs`, `CycloneSteerRules.cs`, `CycloneSteerSteps.cs`, `CycloneWhirlSteps.cs`, `CycloneWindMotion.cs`, `ICycloneShoveSteps.cs`, `ICycloneSteerSteps.cs`, `ICycloneWhirlSteps.cs`
- Modified (Editor): `CycloneBurstTests.cs`, `CycloneCastOnEnemyTests.cs`, `CycloneHeavyEndsOnItTests.cs`, `CycloneSteerTests.Preview.cs`, `CycloneSteerTests.cs`, `CycloneWhirlTests.cs`, `CycloneWindBeatsTests.cs`
- New: `Cyclone/CycloneKnockMotion.cs` + `.meta`, `Editor/CycloneSteerTests.Knock.cs` + `.meta`
- Deleted (stage the deletions): `Cyclone/CycloneCarryPlanner.cs` + `.meta`, `Editor/CycloneSteerTests.Carry.cs` + `.meta`
- 36 paths in all (32 tracked changes incl. 4 deletions, plus 4 new). Leave out THJ's `GlobalSettings.asset`, `miso.slnx`, `.mcp.json`, `powershell.exe`.
- Suggested message: "feat(lucy): the Steer glides in a straight line through enemies, hitting each once, and knocks the one where it stops; the cast on an enemy uses the same knock; the carry is gone"

### Chunk 3: Preview (pass hits, one damage segment per enemy)

Built (under `miso/Assets/_Project/Features/Player/Lucy/Scripts/`, LF, no BOM):

- `Cyclone/CycloneOutcome.cs`: new `PassHit` (units the Steer passes and hits, path order, each once; empty for a cast), `Hit` stays the Whirl's, new `AllHit()` (passed first, then Whirl hits not already passed). `ForSteer` fills `PassHit` from `plan.Passed`; the Whirl's `Hit` drops passed units (a passed unit can still be pulled: its ghost moves, no second segment). Moves = the knock only, Whirl at `End` with `Start` vacated: already so from C2.
- `Cyclone/CycloneOutcomeView.cs`: the damage map is fed from `outcome.AllHit()` (a dictionary, so one segment per unit); a passed unit has no ghost unless the Whirl pulls it, and then its bar rides its ghost (existing panel move). Comments updated.
- `Cyclone/CycloneSteerPreview.cs`: comments only. Path arrows from `plan.Path` were already done in C2.
- `Editor/CycloneSteerTests.Preview.cs`: the knock ghost test was already rewritten in C2 and kept. New tests (4): row of Claws (screenshot 1) and Claw above with the family around (screenshot 2), each previewing then executing and comparing pass set, knock landing, every ghost's cell and the enemies hit (helper `PreviewThenExecute`); a passed enemy that isn't pulled has no ghost, no tether and one segment where it stands; a passed-and-pulled enemy has one segment on its ghost.

Verified: Unity MCP forced compile, console 0 errors; regex group `MISO.Core.Features.Bergsons.EditorTests.Cyclone.*` (covers CycloneSteerTests all partials, CyclonePreviewTests, CycloneCastOnEnemyTests, CycloneSteerPlannerTests and the other Cyclone fixtures): 319/319 passed, 0 failed (C2 had 315 in the same classes, plus the 4 new). Not run: full suite, AI regression test (not asked).

Not verified: Play mode (how the bars and ghosts look for a passed and pulled enemy; the bar offset uses the existing ghost panel move).

Decisions: `AllHit()` is a method (an enumerable), not a stored list; `SteerPreview_ACellPastABlockedFront...` was already deleted in C2.

Files to stage for C3 (no new files, so no metas):
- `miso/Assets/_Project/Features/Player/Lucy/Scripts/Cyclone/CycloneOutcome.cs`
- `miso/Assets/_Project/Features/Player/Lucy/Scripts/Cyclone/CycloneOutcomeView.cs`
- `miso/Assets/_Project/Features/Player/Lucy/Scripts/Cyclone/CycloneSteerPreview.cs`
- `miso/Assets/_Project/Features/Player/Lucy/Scripts/Editor/CycloneSteerTests.Preview.cs`
Suggested message: "feat(lucy): the Steer preview shows one damage segment per enemy it hits on the way or by the Whirl, and what it shows is what happens"

### Chunk 4: Remove the heavy-warning wobble

Built (under `miso/Assets/_Project/Features/Player/Lucy/Scripts/`, LF, no BOM):

- Deleted `Cyclone/CycloneWobble.cs` + `.meta` (held `CycloneWobble` and `CycloneWobbleRules`).
- `Cyclone/CycloneEntity.cs`: removed the `_wobble` field, its `AddComponent`/`Bind` in `Initialize`, the `Unbind` in `Dispose`, and the header comment mention.
- `Cyclone/CyclonePipsView.cs`: removed `SetFlicker`, `IsFlickering`, the flicker fields and constants, `Update`, and the `leftAlpha` path (nothing else used it; `Refresh` now colours the pips directly).
- `Editor/CyclonePreviewTests.cs`: deleted the five `Wobble_*` tests and the helpers only they used (`TagSetWith`, `Corridor`, `Masher`, `ImmovableTag`). Unused `using`s left alone.
- Grep of `miso/Assets/_Project` (cs, meta, asset, prefab, unity) for `CycloneWobble`, `SetFlicker`, `IsFlickering`, `Wobble`: no references left.

Verified: forced compile, console 0 errors. `CyclonePreviewTests` 13/13 (was 18), `CycloneLifeTests` 8/8. Regex group run once after C5 (see below).
Not verified: Play mode.

Files to stage for C4:
- `miso/Assets/_Project/Features/Player/Lucy/Scripts/Cyclone/CycloneWobble.cs` (deleted, stage the deletion)
- `miso/Assets/_Project/Features/Player/Lucy/Scripts/Cyclone/CycloneWobble.cs.meta` (deleted)
- `miso/Assets/_Project/Features/Player/Lucy/Scripts/Cyclone/CycloneEntity.cs`
- `miso/Assets/_Project/Features/Player/Lucy/Scripts/Cyclone/CyclonePipsView.cs`
- `miso/Assets/_Project/Features/Player/Lucy/Scripts/Editor/CyclonePreviewTests.cs`
Suggested message: "refactor(lucy): remove the Cyclone's heavy-warning wobble and pip flicker"

### Chunk 5: Texts and setup tool

Built (all LF, one-line edits):
- `Resources/UnitSpecific/Player/Lucy/Abilities/Cyclone/Lucy_Ability_Steer.asset` line 16 (inline text, not a string table key): `Glide the Cyclone up to 3 cells in a line, through enemies, hitting each. An enemy where it stops is knocked onward. Then it Whirls. Once a turn.`
- `Features/Player/Lucy/Scripts/Editor/CycloneSteerSetup.cs` line 31: same text.
- `Lucy_Cyclone_Ability.asset` line 16 (inline, single-quoted): appended ` Cast it on an enemy to knock it away.`; the old text said nothing about casting on an enemy, so nothing replaced.
- No test pinned the old Steer description (grepped).

Verified: regex group `MISO.Core.Features.Bergsons.EditorTests.Cyclone.*`: 314/314 passed, 0 failed (C3 had 319; minus the 5 deleted Wobble tests). Console 0 errors. Not run: full suite, AI regression.
Note: the Steer asset text is `[PLACEHOLDER]`-untagged working text from the design; final wording by narrative.

Files to stage for C5:
- `miso/Assets/_Project/Resources/UnitSpecific/Player/Lucy/Abilities/Cyclone/Lucy_Ability_Steer.asset`
- `miso/Assets/_Project/Resources/UnitSpecific/Player/Lucy/Abilities/Cyclone/Lucy_Cyclone_Ability.asset`
- `miso/Assets/_Project/Features/Player/Lucy/Scripts/Editor/CycloneSteerSetup.cs`
Suggested message: "feat(lucy): working descriptions for the straight Steer and the cast on an enemy"
