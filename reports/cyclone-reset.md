# Report: Cyclone reset (straight Steer, knock, carry and wobble removed)

Plan: plans/2026-11-19-cyclone-reset-tech.md    Agent: miso-implementer    Branch: thj/cyclone
Outcome: complete (C1 to C5 built, reviewed and approved with five should-fixes; the fix round below applied all five)

## What changed

The Steer glides in a straight line (up to 3 cells) through enemies, hits each once on the way, and knocks the enemy at its stop onward (else right, else left); the carry is gone. A cast on an enemy uses the same knock. The aim previews draw the same plan (one ghost per enemy that moves, one damage segment per enemy hit, none for a passed enemy a lethal pass hit kills) and the heavy-warning wobble and pip flicker are removed. Working texts for the Steer and the cast on an enemy. The fix round after review: lethal pass hits left off the preview's Whirl board, stale carry/wobble wording gone, carry leftovers removed (`Fling`, `DrawUnit`, the cast's knock direction), comment lines rewrapped. Last Cyclone group run: 315/315.

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

## Fix round (after the feature review)

All five should-fixes applied. Base: `Features/Player/Lucy/Scripts/` (LF, no BOM). Verified: regex group `MISO.Core.Features.Bergsons.EditorTests.Cyclone.*`: 315/315 passed, 0 failed (314 + the new test); console clean after compile. Not run: full suite, AI regression.

1. Lethal pass hit in the preview. `CycloneOutcomePlanner.ForSteer` takes an optional `diesOnPass` predicate. A passed unit it flags is removed from the board the closing Whirl is planned on (no pull, no cell it holds, no second hit) and keeps its single damage segment (skull) where it stands. `CycloneSteerPreview` passes `LethalOf ?? IsLethal`; `IsLethal` is the hit's damage (same `HitDamage` / `DamageOf` the view uses) against the unit's own health, false for a unit without an attribute set (edit-mode test units). New public test hook `LethalOf` beside `DamageOf`. Test: `SteerPreview_APassedEnemyTheHitKills_IsNotPulled_HasOneSegmentWhereItStands_AndEqualsTheExecution` (a lethal pass enemy two cells behind the stop, which would otherwise get a pull ghost; preview then execute, plus a bystander still pulled).
   Decision: the dead unit's cell is treated as empty on the planned board. In the live game the dead unit's cell is freed once it dies; if it ever stays occupied until after the Whirl, a pull into that cell could differ. Play-check item (kill a Claw by passing it, with another enemy behind it on the same arm).
2. `CycloneSteerPlannerTests.cs`: section comment now "A row of Claws ahead; a Claw above with the family around". No other "screenshot" wording left in Lucy code.
3. Stale carry/wobble wording fixed: `CyclonePreviewTests.cs` (header, section comment, "Rider" renamed "Knocked", assert messages, one test renamed `OutcomeView_MovesTheHealthBar...`), `CycloneWhirlPlanner.cs`, `CycloneCrossView.cs`, `CycloneUnitDrawings.cs`, `CycloneOutcomeView.cs` ("carried over" now "moved over"), `CycloneWindBeatsTests.cs` ("Carried" unit now "Knocked"), `CycloneSteerTests.cs` (test renamed `..._NothingMovesWithIt`). Grep of "carry/carried/rider/wobble/drag/screenshot" over `Features/Player/Lucy` now only hits the unrelated fireball summary and the real `dragStraightOnly` field.
4. Carry leftovers: `CycloneWindMotion.Fling(fromRoot, toRoot, hop, t, out root, out offset)` (no `fromOffset`/`fromTilt`/`tilt`); `ICycloneShoveSteps.DrawUnit(unit, position, offset)` and `CycloneShoveSteps`, `CycloneUnitDrawings.Draw` lost the tilt (the offset stays: it is the fling's hop). Four test recorders and the Fling and Drawings tests updated (the tilt asserts are gone). `CycloneRules.CastShoveDirections` is now `CastKnockOnward(lucy, target)` returning `Vector2Int?` (null for Lucy's own cell); `CastKnock` uses it; test is `KnockOnward_LargerAxisOnly_AndTheRowAtATie`.
5. Rewrapped to 120 columns: `AEffectCycloneSteer.cs` (the cost sentence), `CycloneEntity.Whirl.cs` header, `CycloneOutcome.cs` header, `CycloneOutcomeView.cs` header, `CycloneSteerPreview.cs` header, `CycloneWhirlPlanner.cs` header line.

Docs: `tech/core-systems.md` line 112 still lists `CycloneWobble` and `CycloneCarryPlanner` (coordinator's file, not touched).

Files to stage (all `miso/Assets/_Project/Features/Player/Lucy/Scripts/`, no new files, no `.meta`):
- `Cyclone/`: `AEffectCycloneSteer.cs`, `CycloneCrossView.cs`, `CycloneEntity.Whirl.cs`, `CycloneKnockMotion.cs`, `CycloneOutcome.cs`, `CycloneOutcomeView.cs`, `CycloneRules.CastKnock.cs`, `CycloneRules.CastOnEnemy.cs`, `CycloneShoveSteps.cs`, `CycloneSteerPreview.cs`, `CycloneUnitDrawings.cs`, `CycloneWhirlPlanner.cs`, `CycloneWindMotion.cs`, `ICycloneShoveSteps.cs`
- `Editor/`: `CycloneBurstTests.cs`, `CycloneCastOnEnemyTests.cs`, `CyclonePreviewTests.cs`, `CycloneSteerPlannerTests.cs`, `CycloneSteerTests.Preview.cs`, `CycloneSteerTests.cs`, `CycloneWindBeatsTests.cs`
Suggested commits: (a) `fix(lucy): the Steer preview leaves an enemy its pass hit kills off the closing Whirl` (CycloneOutcome.cs, CycloneSteerPreview.cs, CycloneSteerTests.Preview.cs); (b) `refactor(lucy): drop the carry's leftover fling and draw arguments and the cast knock's unused second direction` (the rest of the code and test files); comment rewraps and wording fixes can ride in (b).

## Addendum: free route, knock damage, no avoidance (D-586 to D-588)

Plan: the "Addendum, 2026-11-19 later" section of `plans/2026-11-19-cyclone-reset-tech.md`. Built on `b62e2a7fd`. All paths below are under `miso/Assets/_Project/Features/Player/Lucy/Scripts/`. LF, no BOM (checked with `file`, no CR), no new statics, no core file touched, no new files (one deletion). Grep of the diff: no private IDs, no playtest or screenshot wording. Covering fixtures after every chunk: regex group `MISO.Core.Features.Bergsons.EditorTests.Cyclone.*` plus `MasherCounterCycloneTests`, `MasherCounterWhirlTests`, `MISO.Core.Systems.EnemyAlertSystem.EditorTests.EnemyAlertForcedMoveTests` (Unity MCP, editor open). No AI editor test under `Core/Systems/AISystem/Editor` references the Cyclone (grepped), so none was added to the group. Full EditMode suite not run (the coordinator runs it).

### Chunk R1: Free route

Built:
- `Cyclone/CycloneSteerPlanner.cs`: `Lines` is now a depth-first search over every simple four-way path from the Cyclone's cell, up to `reach` steps (never back onto the start, never a cell twice; a step can't go onto a missing cell or a walk-blocking planted entity other than the Cyclone's own; everything else is crossed). Each reached cell keeps its fewest steps; only routes of that length count (a longer route never wins). Among them, only routes that make the cell a stop are kept: `TryStopOn` (unchanged) with onward = that route's last step. The cell is offered if any shortest route makes it a stop; its route is then the one with the most distinct enemies on the route cells before it, then the latest first turn (index of the first step that differs from step one; a straight route counts as never turning), then `CycloneRules.StraightDirections` order at the first differing step. The plan's `Passed` is read off the kept route, its knock from that route's stop check. `Lines` returns one plan per stop, fewest steps first, then search order. `PlanTo` returns early past the reach in Manhattan distance, else picks the stop out of `Lines`. Plain grid slots, `ReferenceEquals` and the rules' delegates only; small lists, no dictionary keyed by a Unity object. At reach 3 the search visits at most 4 + 12 + 36 = 52 path prefixes.
- `Cyclone/CycloneSteerPlan.cs`: comments only (`Direction` = last step, the knock's onward; `Path` = four-way steps, no cell twice).
- Comments/tooltip only: `AEffectCycloneSteer.cs` (header; `reach` tooltip "in four-way steps", tooltip text only, no serialized rename), `CycloneSteerRules.cs` header, `CycloneEntity.Steer.cs` header, `CycloneSteerPreview.cs` header.
- No other runtime change was needed: the glide already walked `plan.Path` cell by cell, the safety net already read `plan.Direction`, the preview's path arrows already drew `Start + Path` with the grid's own arrows (which drew the old turning paths).

Tests:
- `Editor/CycloneSteerPlannerTests.cs`: straight-line cases rewritten for routes (every cell within 3 steps offered, by its fewest steps; reach in steps; map edge; round a hole and a pillar, never through; the Cyclone's own slot crossed; hazard and stash crossed, never a stop; the `Direction` filters replaced by cell filters). New: `Routes_GoRoundAWallWithinReach_CountingEveryStep` (null at 3, the 4-step way round at reach 4, up before down), `Routes_NeverVisitACellTwice_NorTheStart_AndMoveOneFourWayStepAtATime`, `Route_OfTwoEqualRoutes_TakesTheOneThatPassesMoreEnemies`, `Route_OfTwoEqualRoutesPassingAsManyEnemies_TakesTheDirectionOrderAtTheFirstStep`, `Route_GoesStraightAsLongAsItCan_BeforeTurning`, `Route_PassingMoreEnemies_ComesBeforeGoingStraight`, `TheKnock_AfterATurn_GoesOnwardFromTheLastStep`, `OfTwoShortestRoutesArrivingDifferently_OnlyTheOneWhoseKnockLands_IsTaken` (two 2-step routes to a Claw arriving by different last steps; the one the direction order prefers has no landing, so the other is taken and knocks to the left of up), `ALongerRouteNeverWins_EvenWhenOnlyItsKnockWouldLand` (the 1-step route has no landing; a 3-step way round would, and the cell is still refused); `PlanTo_AgreesWithLines_ForEveryCell` also compares `Direction`.
- `Editor/CycloneSteerTests.cs`: `Steer_ReachesUpToThreeFourWaySteps_RoundACornerToo` (was "never round a corner"), `Steer_GoesRoundAWall_OnlyWithinItsReach` (was "never goes round a wall"), the range test asserts a cell round a corner is offered (was "four lines only"), header.
- `Editor/CycloneSteerTests.Knock.cs`: new `TheGlide_FollowsTheRouteRoundTheCorner_AndHitsTheEnemyOnTheWayAtItsCell` (every glide frame on the two route segments, never across the corner; the pass hit at the passed cell).
- `Editor/CycloneSteerTests.Preview.cs`: new `SteerPreview_EqualsTheExecution_OnARouteThatTurns` (path arrows follow the route, knock onward from the last step, Whirl pull ghost, then `PreviewThenExecute`).

Verified: compile clean (console: no `error CS`, no Cyclone warning); covering group **333/333 passed**, 0 failed (the fix round had 315 in the Cyclone classes + 8 in the other three; +10 new). One first-run failure was a test bug (indexing the hole cell), fixed. After the switch to "shortest routes that make a stop" (done after R3, on top of all three chunks): covering group **330/330 passed**, 0 failed (R3's 329 + the one extra planner test).

Not verified: Play mode (how the turning path arrows read, a glide round a corner on screen).

Decisions:
- **Shortest routes that make a stop, then the tie-break** (coordinator's call, after I first built "route first, then the stop"). Among the fewest-step routes to a cell, only those whose stop holds (empty, or a knock with a landing onward from that route's last step) compete; the cell is offered if any does. A longer route never wins. A landing still can't be a route cell or the start: on a shortest route only the previous cell touches the stop, and the knock never goes back.
- `Lines` order is now fewest steps first (nothing depends on it; the range and the target check read it as a set).
- Distinct enemies for the tie-break count a large unit once and never the stop's own unit.

### Chunk R2: Knock damage

Built:
- `Cyclone/CycloneEntity.Steer.cs`: the knocked enemy takes one Cyclone hit through the Whirl's own `Hit` + `Report` right after it is plugged on its landing cell and the Cyclone has relocated, before its end of move (`Landed`: Watch, wake); a hit that kills it skips `Landed`. `HitOnTheWay` now wraps a shared `HitOnce` (same guards: nothing once burst, level ended, or dead). The Whirl's skip set still holds the passed enemies only, so the Whirl hits the knocked enemy again beside it. Header comment rewrapped and updated. Steer log line unchanged ("hit N on the way, knocked K"; the knock's hit is not counted in N).
- `Cyclone/AEffectCycloneSpawner.Shove.cs`: `ShoveThenCast(..., Action<GUnit> hitOnLanding = null)`, called on the knocked enemy right after its landing, before `Landed`; a hit that kills it skips `Landed` and it isn't noted as moved. The live cast passes `HitOnLanding(owner, unit, statCtx)`: the Cyclone prefab's hit effect with the cast's stats and one report credited to the cast (nothing once the level is over).
- `Cyclone/CycloneWhirlSteps.cs`: the hit, report and health read moved into three `internal static` helpers (`ApplyHit`, `ReportHit`, `HealthOfUnit`) that the instance methods call, so the cast's knock hit uses the same path before the Cyclone exists. Same behaviour for the Whirl.
- `Cyclone/CycloneOutcome.cs`: `KnockHit` (the knocked unit), `HitCount(unit)` (on the way + knock + Whirl), `AllHit()` = passed, then knocked, then the Whirl's, each once. `ForSteer` and `ForCast` take `diesOfOneHit` (was `diesOnPass` on `ForSteer`; `ForCast` gains it): a passed or knocked enemy one hit kills is taken off the board the Whirl is planned on (no pull, no cell it holds, no Whirl hit) and keeps its one segment.
- `Cyclone/CycloneOutcomeView.cs`: a unit's segment is one hit's damage times `HitCount` (knock + Whirl summed); still one segment per unit.
- `Cyclone/CycloneSteerPreview.cs`, `Cyclone/CycloneCastPreview.cs`: comments; the cast preview passes a new `IsLethal` (one hit's damage against the unit's health, as in the Steer preview).

Tests:
- `Editor/CycloneSteerTests.Knock.cs`: `TheKnock_LandsOnce_...` expects the knock's hit before the Whirl begins, two hits on the Claw, two reports, Whirl log (0, 1); `ThePlanIsWhatHappens_...` expects Passed, Knocked (knock), then the Whirl's Knocked and OnArm. New `TheKnockedEnemy_IsHitOnItsLandingCell_AfterTheCycloneMoves_BeforeItsEndOfMove`, `AKnockThatKills_HasNoEndOfMove_NoWhirlHit_AndFreesItsCellForThePull` (the enemy behind it on the arm is pulled into the freed cell).
- `Editor/CycloneSteerTests.Preview.cs`: `PreviewThenExecute` and the ghost test compare the executed hits with the preview's hits counted (`HitCount`); the ghost test checks the knocked Brute's segment is 6 (3 + 3) and the Shaman's 3. New `SteerPreview_AKnockThatKills_ShowsOneHit_NoWhirlHit_FreesItsCell_AndEqualsTheExecution`.
- `Editor/CycloneCastOnEnemyTests.cs`: new `TheKnockedEnemy_TakesOneHitAsItLands_BeforeItsEndOfMove_ThenTheCycloneIsCast` (order: start, unplug, plug, hit on the landing cell, landed, spawn), `AKnockThatKills_HasNoEndOfMove_AndTheCycloneIsStillCast`, `ThePreview_SumsTheKnocksHitAndTheWhirls_AndALethalKnockLeavesTheWhirlsBoard` (`HitCount` 2, one segment; lethal: 1, no Whirl hit, the enemy behind pulled into the freed cell); header.

Verified: compile clean; covering group **339/339 passed**, 0 failed (+6 new).

Not verified: Play mode; the live `HitOnLanding` wiring of the cast (the effect needs real units with attributes; the tests inject the hit). Kill XP/gold, Howling Gale and waking follow from using the same effect and report as the Whirl; not seen in a level.

Decisions:
- **Order:** the knock's hit lands on the landing cell before the knocked enemy's end of move (Watch) and wake, so a knock that kills raises no end of move. Steer: after the Cyclone relocates. Cast: before the Cyclone is planted.
- **Cast hit before the spawn, not through the new Cyclone.** The cast Whirl starts inside the spawn and, with nothing to swell for, plans its pull in that same frame; a hit after the spawn would leave a dead knocked enemy's cell blocking that plan while the preview showed it free. So the cast's knock hit goes through the shared static hit and report with the prefab's effect and the cast's stats. Consequence: the hit lands even if the Cyclone is then refused (already out, or cell taken), cases the target check normally rules out.
- `diesOnPass` renamed `diesOfOneHit` (parameter only; same meaning, widened to the knock).
- Steer log line kept as is (plan: "keep the line as is").

### Chunk R3: No avoidance

Built:
- Deleted `Cyclone/CycloneEntity.AIDanger.cs` + `.meta` (`IAIEndOfTurnDanger`, `IAIEndOfTurnDangerSparesMover`). The core danger snapshot and hooks are untouched; the Cyclone is no longer a source.
- Stale comments: `Cyclone/CycloneHeavy.cs` ("the walk check, the burst and the AI share" now "the walk check and the burst share"), `Cyclone/CycloneEntity.LineOfFire.cs` ("the same relation the Whirl uses").

Tests:
- `Editor/CycloneAIDangerTests.cs` rewritten: `Snapshot_TheCrossIsNoDangerForAnyone` (empty for enemy, family, ally, neutral; the Cyclone isn't an `IAIEndOfTurnDanger`), `AnEnemyEndsOnAnArm_WhenThatIsItsBestCell`; kept the two core-rule tests on a hand-made set (`Touches_...`, `RefusesEndingOn_...`, the only coverage of those core functions). Deleted: cross is danger for enemies, faded is no danger, another route, walking in to attack, sealed off.
- `Editor/CycloneAIHeavyTests.cs`: kept `CellsFor_APlainSet_IsTheSameSetForEveryone` and the walk test, now `AHeavyWalksThroughTheCyclone_AndEndsOnTheArm_ALightEnemyNeverEndsOnTheCyclone` (snapshot empty; the light enemy no longer has to go round). Deleted the six cases that pinned heavy sparing, the other danger source and the worker-thread read of the Cyclone's set.
- `Editor/CycloneSteerTests.cs`: deleted `AfterASteer_TheAIsDangerIsTheNewCross`; header.
- `Editor/CycloneBurstTests.cs`: dropped the two danger asserts from the burst test (the line-of-fire asserts stay).

Verified: compile clean; covering group **329/329 passed**, 0 failed (339, minus 12 deleted, plus 2 new); 330/330 after the R1 rule switch. `MISO.Core.Systems.AI.EditorTests.AIRegressionTest.Baseline_MatchesCurrentAI` run by name: **FAIL, CHECKS 714, FAILURES 43**, the same count as the last recorded 43; not re-baselined.

Not verified: enemies walking onto the arms in a level (play check).

Decision: kept the generic core-rule tests (`Touches`, `RefusesEndingOn`, `CellsFor` on a plain set) in the Cyclone fixtures rather than deleting them; nothing else covers those core functions.

### Files to stage, per chunk

A file touched by two chunks is listed under the later chunk, except `Editor/CycloneSteerTests.cs`, which the coordinator moved into R1 so every commit's tests are green: it carries R3's deletion of `AfterASteer_TheAIsDangerIsTheNewCross` and one header line, harmless before R3 (the danger source still exists then, the test just isn't there). At the R1 commit the old `CycloneSteerTests.Knock.cs` and `.Preview.cs` only steer along straight lines (one shortest route), so they stay green with the new planner; at R1 and R2 the old AI danger tests still test the still-present danger source. Every commit compiles.

R1 (6 files):
- `Cyclone/CycloneSteerPlanner.cs`
- `Cyclone/CycloneSteerPlan.cs`
- `Cyclone/AEffectCycloneSteer.cs`
- `Cyclone/CycloneSteerRules.cs`
- `Editor/CycloneSteerPlannerTests.cs`
- `Editor/CycloneSteerTests.cs` (also R3: one test deletion and a header line)
Message: "feat(lucy): the Steer takes a free four-way route of up to 3 steps, round corners and through enemies: fewest steps, then most enemies passed, then straight first"

R2 (10 files):
- `Cyclone/CycloneEntity.Steer.cs` (also R1: header comment)
- `Cyclone/CycloneSteerPreview.cs` (also R1: header comment)
- `Cyclone/AEffectCycloneSpawner.Shove.cs`
- `Cyclone/CycloneCastPreview.cs`
- `Cyclone/CycloneOutcome.cs`
- `Cyclone/CycloneOutcomeView.cs`
- `Cyclone/CycloneWhirlSteps.cs`
- `Editor/CycloneSteerTests.Knock.cs` (also R1: the glide round the corner test)
- `Editor/CycloneSteerTests.Preview.cs` (also R1: the turning-route preview test)
- `Editor/CycloneCastOnEnemyTests.cs`
Message: "feat(lucy): a knocked enemy takes one Cyclone hit as it lands, on the Steer and the cast; the preview sums it with the Whirl's"

R3 (7 paths, 2 of them deletions):
- `Cyclone/CycloneEntity.AIDanger.cs` (deleted)
- `Cyclone/CycloneEntity.AIDanger.cs.meta` (deleted)
- `Cyclone/CycloneEntity.LineOfFire.cs`
- `Cyclone/CycloneHeavy.cs`
- `Editor/CycloneAIDangerTests.cs`
- `Editor/CycloneAIHeavyTests.cs`
- `Editor/CycloneBurstTests.cs`
Message: "feat(lucy): the Cyclone is no longer end-of-turn danger for the AI; enemies don't avoid its arms"

Leave out THJ's `GlobalSettings.asset`, `miso.slnx`, `.mcp.json`, `powershell.exe`.

### Risks and loose ends (addendum)

- An enemy cell is refused when no shortest route gives its knock a landing, even if a longer way round would (`ALongerRouteNeverWins_...`).
- The ability text still says "in a line" (`Lucy_Ability_Steer.asset`, `CycloneSteerSetup.cs` line 31); outside the addendum's scope, narrative pass.
- A lethal knock: the dead enemy's ghost and the ghost of the enemy pulled into its cell share a cell in the preview (correct, may read oddly). Play check.
- The freed-cell assumption (a unit a hit kills leaves its cell before the Whirl plans) now covers the knock too; same play-check item as the lethal pass.
- Play-check items on straight lines (1, 3, 5, 6) need rewriting for routes; enemies now end turns on the arms freely, so the Whirl pulls and hits more often.
- `tech/core-systems.md`: the Cyclone is no longer an `IAIEndOfTurnDanger` source; the core danger hooks now have no source in the game (coordinator's note).

### How to see it (addendum)

1. In a level with Lucy and enemies, cast the Cyclone, then pick Steer: the range lights every cell up to 3 steps away, round corners (not through walls or rocks); hovering a cell round a corner draws the turning path arrows.
2. Hover a diagonal cell with a Claw on one of the two equal routes: the route goes through the Claw (most enemies passed) and its bar shows one hit.
3. Steer onto a Claw after a turn: it is knocked onward along the last step; its ghost bar shows two hits (knock + Whirl). Click: the hit pops as it lands, then the Whirl hits it again.
4. Cast the Cyclone on an enemy: its bar shows two hits; on cast it takes one as it lands, then the Whirl's.
5. End the turn with the Cyclone out: enemies walk onto its arms when that is their best cell, then get pulled and hit at the end of their turn.

## Play bugs 2026-11-20

THJ played `LevelE1-C1` (the Console of that session: "Sequence Started: @LevelE1-C1_Start..."). Screenshot `playtests/img/2026-11-20-cyclone-4-no-steer-no-cast-preview.webp`. The Unity MCP was reachable for this round: compile, Console and EditMode runs went through it; no Play session was started.

### 1. No Steer after the cast

**Cause: level data, not code, and not a reset commit.** The Cyclone button only swaps to a Steer that is in Lucy's own kit (`CycloneButtonSwap.FindSteer` over `AbilityOrchestrator.Abilities`). The Steer is slot 9 of `Unit_Lucy.prefab`'s kit (added 2026-11-16, `22ecc78d8`). Eight level prefabs give their Lucy a kit of their own by overriding the kit's size (2 to 7 slots, set in October), so the kit ends before slot 9: the cast is in it, the Steer is not, and the button keeps showing the cast, greyed, with the cast's own cooldown (4, so the "3" in the screenshot is the round after the cast). Evidence: the registry entry left over from THJ's session (domain reload is off; it is cleared at the next Play), read in the editor: Lucy's runtime kit was `PrimaryAttack, Walk, Cyclone_Ability, Teleport` only; the Cyclone was alive, not whirling or steering, no pending pulls, 2 pips, so `CanBeSteered` and `HasLiveFor` were both true. `LevelE1-C1.prefab` overrides only `abilityOrchestrator.abilities.Array.size: 4` on Lucy. It failed the same way before the reset (`4b84d47f1` has the same level data and slot). Greybox levels (full kit) were never affected, which is why earlier rounds saw the Steer.

Levels whose Lucy has the cast and no Steer (from the repro test): `Generic Levels/Easy/E1/LevelE1-C1`, `LevelE1-C2`, `Generic Levels/FamilyLevels/M2/LevelLucyJohn-C2`, `LevelLucyJohn-C3`, `Generic Levels/FamilyLevels/MarkIntro/LevelMarkIntro-C1`, `LevelMarkIntro-C3`, `Level1/Level1-C2`, `Level1-C4`.

**Fix: the same pattern as Linda's Encore (`EncoreKitTool`, `55cde5ce5`).** New editor tool `Tools > Levels > Lucy > Add Steer To Custom Kits` (`CycloneSteerKitTool`). For every level prefab whose Lucy kit has the Cyclone cast and no Steer, it appends the Steer slot copied from `Unit_Lucy`'s default kit: animation `Cyclone`, activation frame 10, the `PlaySFX A_SFX_Lucy_Cyclone` event and the stat sources. The event's target is an FX runner inside `Unit_Lucy`, so the tool points it at the same object of that level's Lucy. Kits without the cast and kits that already have the Steer are left alone, so a second run changes nothing.

**The tool has NOT been run.** The permission classifier refused running it from `execute_code`, because it rewrites 8 level prefabs, so the level prefabs are unchanged. Next step: THJ (or the coordinator, with THJ's OK) runs `Tools > Levels > Lucy > Add Steer To Custom Kits` once in the open editor. The dialog should say "Steer added to 8 kit(s). 0 level(s) still lack it". Then re-run `CycloneSteerKitTests`. Expected diff, per level prefab: Lucy's kit size +1 and the new slot's overrides (as in the Encore commit, roughly 10 to 60 YAML lines each).

No game code changed. Read and found fine: the swap, `CheckActivationFeasibility`, `CanBeSteered`, `NotifyReadyChanged`/`ReadyChanged`, the `IsSteering`/`IsWhirling` flags after the cast Whirl and the cast knock, and the `ShoveThenCast` path.

**Tests.** New `CycloneSteerKitTests.EveryLevelThatGivesLucyTheCycloneCast_GivesHerTheSteer_SetUpAsInHerDefaultKit` scans every level prefab with a Lucy. Each kit with the cast must have the Steer, with the default slot's animation, activation frame, events and stat sources, and a sound-event target inside that level. It fails now on the 8 levels above (the repro). Its slot checks already pass on the levels that inherit the full kit. Run: `MISO.Core.Features.Bergsons.EditorTests.Cyclone.*` + `MasherCounterCycloneTests` + `MasherCounterWhirlTests` + `EnemyAlertForcedMoveTests` = 330/331. The one failure is this repro, which passes once the tool has run. Whole EditMode suite not run (no game code or core system touched). `AIRegressionTest` not run (no AI graph, AI ability or unit prefab changed; the tool touches level prefabs, not unit prefabs).

**Files to stage, commit A (tool and test):**
- `miso/Assets/_Project/Features/Player/Lucy/Scripts/Editor/CycloneSteerKitTool.cs`
- `miso/Assets/_Project/Features/Player/Lucy/Scripts/Editor/CycloneSteerKitTool.cs.meta`
- `miso/Assets/_Project/Features/Player/Lucy/Scripts/Editor/CycloneSteerKitTests.cs`
- `miso/Assets/_Project/Features/Player/Lucy/Scripts/Editor/CycloneSteerKitTests.cs.meta`

Message: "feat(levels): a tool that puts the Steer into every level kit of Lucy's that has the Cyclone, and a test that checks those levels"

**Commit B, after the tool has run.** It gets its own commit so it can be reverted alone. It holds the 8 level prefabs listed above; `git status` will show exactly which, and nothing else should change.

Message: "feat(levels): Lucy's Steer in the 8 levels that give her a kit of her own with the Cyclone"

### 2. Cast preview shows no Whirl damage

**Not reproduced. Cause not found from code. No change made.**

For a cast on an empty cell, the preview takes the same path before and after the reset:
- `ForCast` with a null knock never calls `diesOfOneHit` (`KnockedUnit` returns first).
- It plans the Whirl on `cell.OccupantEntity`, exactly as the pre-reset `ForCast(..., shove: null)` did.
- `KnockHit` is null and `PassHit` is empty, so `AllHit()` is the Whirl's `Hit` and `HitCount` is 1 for each of them.
- `CycloneOutcomeView.Show` multiplies one hit's damage by 1.

`CycloneHitPreview.DamageOn` is the same call the Steer preview makes: the prefab's hit, Lucy as owner, the cast's `RuntimeAbility` as stats, which is also the live Cyclone's stat context.

The existing EditMode tests (`CastPreview_GhostsForPulledEnemies_...`) show the planner and the view draw a segment for an enemy beside an empty cell. The real `CycloneCastPreview.Preview` path can't be driven with real damage in EditMode: test units have no health attribute, and `_cast` must be a live `RuntimeAbility`. So no failing repro test could be written.

Also checked and ruled out:
- The generic hover preview (`PlayerController.ShowDamagePreview`): it runs when the hover event fires, and ours is drawn again every `LateUpdate`.
- The Linda-Lucy Duo and the Bloom/Catch presenters: they only run for other aims.
- The info panel's mode queue and the grid's hover event order.
- E1-C1's enemies: their info panels are wired.
- E1-C1's Lucy cast slot: inherited unchanged; only the kit size is overridden.

The Console of THJ's session has no exception.

What would settle it (needs THJ's OK for a Play session, or THJ's own look): in E1-C1, aim the cast at an empty cell beside a Claw and note whether the dimmed aim cross is drawn at the cursor.
- Cross drawn but no segment: the damage comes out as 0, or something hides it after our `LateUpdate`. Next step: log `HitDamage` and `outcome.Hit.Count` in `CycloneCastPreview.Preview`.
- No cross either: the preview never runs. Either it isn't attached to that level's bus, `IsAiming()` is false, or the cell isn't in `_range`.

Also worth one check in a Greybox level, to see whether it happens in E1-C1 only.

### Risks and loose ends (play bugs)

- The repro test for bug 1 stays red until the tool has run. Commit A and commit B together, or accept the red test in between.
- The dev scenes `Scenes/DevScenes/TestLevel.unity`, `SampleScene 1.unity` and `Scenes/RosScene.unity` also hold a Lucy. The tool and the test only look at level prefabs under `Content/Levels`.
- Any new level that overrides Lucy's kit size will drop the Steer again; the test catches it.
- `AbilitiesBarHUDUI.Populate` asks the level ability lock about the cast, not about the Steer shown in its place (`HiddenFromBar(ability)` gets the original ability). Harmless today; noted only.
