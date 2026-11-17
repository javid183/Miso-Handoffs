# Report: Cyclone round 2, C2 (Carry)

Plan: plans/2026-11-17-cyclone-round2-tech.md (chunk C2; design plans/2026-11-17-cyclone-round2-design.md section 3)    Agent: miso-implementer    Branch: thj/cyclone (on top of the uncommitted C1)
Outcome: done (compiled in the open editor through the Unity MCP; EditMode run, see counts)

## What changed

All under `miso/Assets/_Project/Features/Player/Lucy/Scripts/`. Nothing in `Core/` touched; no `AEffectPusher`, `AEffectTransporter`, `AbilityDamagePreview`, `PlayerController`, `GridManager` edit; no asset, prefab or AbilityPreset change.

- `Cyclone/CycloneCarryPlanner.cs` (new, + `.meta`): the pure, worker-safe per-step carry planner. `Start`, `CanTakeStep`, `TakeStep`, `CanEnd`, `Simulate(start, path, rules)`, `CanRide`; plan types `CycloneCarryPlan` (Cyclone path, steps, carried units in first-move order, each unit's own path `PathOf/StartOf/LandingOf`, the simulated board `OccupantOf`), `CycloneCarryStep` (from, to, direction, ordered moves front/sides/rear, `DroppedOut`, `Riders` after the step), `CycloneCarryMove`, `CycloneCarryRole`, and `CycloneCarryRules` (self, crossable, rider filter). Reads plain slots, references, `IsAlive`, `EffectivePlacementSize` and the rules' delegates only.
- `Cyclone/CycloneSteerRules.cs`: `CrossRule`/`CanCross` replaced by `RulesFor(cyclone)` (crosses allies of the caster's faction, riders = `WhirlSteps.IsPullable`, the pull's own filter). `Explore` now returns one plan per reachable end cell (breadth first over every simple path, fixed direction order); `Destinations`, `PathTo`, `CanSteerTo` and new `PlanTo` all go through it. `CanEndOn` kept for the live end check.
- `Cyclone/AEffectCycloneSteer.cs`: new `PlanFor(cyclone, cell)` (the one plan the target check, the range highlight and, in C4, the preview share); `PathFor` reads it; target check and `TryCollectTargetSelectionCells` use the carry rules, so unreachable cells are never offered. Class comment rewrapped (review nit).
- `Cyclone/CycloneEntity.Steer.cs`: `IsValidSteerPath` = the planner's `Simulate`. `SteerRoutine` plans the carry, glides each step's movers in step with the Cyclone (riders keep their cells during the glide), then in one frame: riders off their cells, Cyclone relocated, each rider put on its landing cell (only that cell's hazard fires), then each landed rider's end-of-move event and wake; then the Whirl with `carried` N. A nested `CarryLanding` handles the glide, landing, skipped riders and abort.
- `Cyclone/CycloneEntity.Whirl.cs`: `WhirlRoutine(holdOwnerSource, carried = 0)` logs the real carried count; header comment.
- `Cyclone/ICycloneSteerSteps.cs`, `Cyclone/CycloneSteerSteps.cs`: new `UnitPositionOn`, `CarryStarted` (raises `unitStartMoving`), `Unplug`, `Plug` (`GridCell.PlugEntity`, nearest-cell fallback built in), `Landed` (raises `unitEndMoving`, then `WakeIfUnaware`). The bus events are public `UnityEvent`s already raised the same way by `AEffectSwapper`, so no core API was needed.
- `Cyclone/CycloneWhirlSteps.cs`: `IsEnemy` worker-safe (ReferenceEquals and `IsAlive`; the old Unity null checks kept on the main thread through `AIWorker.IsWorkerThread`, so main-thread results are unchanged); `WakeIfUnaware` made `internal` so the carry shares it.
- `Editor/CycloneSteerTests.cs`: now `partial`; the recorder implements the carry steps (records start, unplug, plug with the planted entity firing as the grid's plug does, landed; can throw once on a plug); `Path` uses `RulesFor`. Four existing tests updated to the new rule (see Decisions).
- `Editor/CycloneSteerTests.Carry.cs` (new, + `.meta`): 17 carry tests.

## Acceptance criteria

- [x] Per-step order front, sides, Cyclone, rear; blocked side drops out; riders recomputed after each step (late and mid-path joiners): `Carry_TheEnemyInFront_IsShovedAheadOnEveryStep`, `Carry_TheEnemiesBesideIt_MoveTheSameWay`, `Carry_ASideEnemyWhoseNextCellIsBlocked_StaysAndDropsOut`, `Carry_TheEnemyBehind_FollowsIntoTheCellTheCycloneLeft`, `Carry_AnEnemyBesideItAfterAStep_RidesTheNextStep`, `Carry_AnEnemyTwoCellsAhead_BecomesTheFrontEnemyPartWay`.
- [x] Immovable and larger-than-one-cell units never ride; in front they block the step; beside they neither ride nor block: `Carry_ImmovableAndLargeUnitsBesideIt_NeverRideAndDontBlock`, `Carry_AnImmovableOrLargeUnitInFront_BlocksTheStep`.
- [x] A blocked front is never offered (cursor and range highlight refuse that cell and every cell past it): `Carry_ABlockedFrontEnemy_RefusesThatCellAndEveryCellPastIt` (Destinations, `TryCollectTargetSelectionCells` and `CheckTargetSelectionCondition` agree), `Carry_OnAnOpenBoard_TheBlockedStraightLineIsNeverTaken`. A Steer never stops short: `TrySteer` only accepts a path the planner fully accepts.
- [x] One landing; no hazard on crossed cells; hazard on the landing cell; end of move (Watch) and wake on landing; carried land before the Whirl starts: `Carry_OneLanding_OnlyTheLandingCellsHazardFires_BeforeTheWhirl`. The hazard firing is the grid's plug rule, mimicked by the recorder (edit-mode cells can't run the real plug); the live hazard and Watch need the play check.
- [x] Harmonic Slam plus carry cannot deal per-cell Crippled damage: `HarmonicSlamThenACarry_CrippledDealsNothingOnTheWay` (data path: Harmonic Slam's tag mod applies `Status.Crippled`; the damage is John's Taunt push's per-tile `onMoveEffects` compound conditioned on `Status.Crippled`; the Whirl's pusher has no `onMoveEffects`; the Steer steps hold no effect; a Claw carried 3 cells takes exactly one hit, the Whirl's). The 15 to 16 number itself is a play check.
- [x] Plan equals execution, and every rider keeps its cell on every glide frame: `Carry_ThePlanIsWhatHappens` (front, two sides, a rear follower, a side that drops out on a blocked step, a path with a turn; every unit lands where the plan says and is plugged there; log count = plan count).
- [x] Whirl log `carried N` real: asserted in the tests above and `Steer_TheEnemyBehindFollowsIntoTheCellTheCycloneLeft_CarriedNotPulled` (`(1, 0, 1)`).
- [x] Failure handling: `Carry_AStopDuringTheGlide_LeavesEveryRiderOnItsCell`, `Carry_ALandingCutShort_PutsEveryRiderBackOnACell` (a plug that throws mid-landing: every rider back on its own cell), `Carry_ARiderThatDiesOnTheWay_IsLeftOut`, `Carry_IfTheEndCellIsTakenMeanwhile_TheCycloneAndItsRidersStay`.
- [x] Turn-switch hold and watchdog: unchanged and still correct. The glide length is the same as before (the carry adds no frames: riders glide with the Cyclone and land in the Cyclone's relocation frame), the Steer still registers no hold of its own while gliding, the Whirl holds as in C1 (`Steer_WhirlHoldsTheTurnSwitchOnce_AndReleasesItAtTheEnd`, `Steer_StoppedPartWayThroughItsWhirl_ReleasesTheHold` still pass).
- [x] Worker-safe, no new statics: the planner and `RulesFor` read plain data; `IsPullable` is now worker-safe. No static field added, so no `PlayModeStaticReset` change.
- [x] Compile clean; EditMode counts: see "Test run".

## Test run

- Before (C1 verify): 2030 run, 2029 passed, 1 failed (the known red, inner 43).
- Cyclone subset after: `CycloneSteerTests` + `CycloneWhirlTests` 67 / 67 passed.
- Full suite after (MCP Test Runner, editor open, no Play mode): 2047 run, 2046 passed, 1 failed, 0 skipped. The only failure is `AIRegressionTest.Baseline_MatchesCurrentAI`, inner `CHECKS: 714 FAILURES: 43` (unchanged). The 17 added tests make up the difference from 2030.

## Save reset

no

## Decisions I made

- **Riders keep their cells during the glide; each is moved off and onto its landing cell in the Cyclone's relocation frame** (the plan said "unplug at start ... plug only at the landing cell"). Same visible result (they glide in step, land once, only the landing hazard fires, events on landing), and it is exactly the `Relocate` pattern the plan points to. It means no rider is ever off a cell across frames, so a level end or stop mid-glide can't strand one: abort just redraws them on their own cells. A landing cut short (exception) re-plugs every rider still off a cell on its own cell. This is the "last valid cell" of the plan, since nothing has moved on the grid before the landing.
- **Paths are searched over every simple path, breadth first, fixed direction order**, because with the carry the board depends on the way taken (the old per-cell BFS dedupe would lose reachable cells). With nothing to carry it picks the same path as before. At most 52 plans for reach 3.
- **A cell past a blocked front can still be offered if a different way reaches it within the reach** (for example around the side, shoving the enemy sideways); the preview will show that path. The straight line through the blocked step is never taken. Tell me if THJ wants "every cell past it" to mean a hard refusal even when a detour exists.
- **What counts in front**: an enemy that may ride is shoved; the family and allies are crossed as before; anything else (Immovable or large enemy, a neutral or factionless unit, a stashed entity the caster isn't allied with) blocks. A shoved or dragged enemy needs a cell with no unit, nothing stashed and no walk-blocking planted entity; a non-blocking hazard is fine (it fires only if it is the landing cell).
- **Rider filter** = the Whirl steps' `IsPullable` (the pull's own filter) plus the one-cell size check in the planner; to make that worker-safe I changed `CycloneWhirlSteps.IsEnemy` to read plain references off the main thread (main-thread results unchanged).
- **Events**: `unitStartMoving` when the glide starts, `unitEndMoving` and the wake after all riders are on their landing cells (so a listener reads a settled board). Riders' facing is not changed (the pusher's face flip is not reproduced).
- **Existing tests changed by the new rule**: `Steer_RefusesPlantedAndOccupiedCells...` (the enemy that blocks is now Immovable), `Steer_CantCrossEnemiesOrBlockingEntities...` renamed `Steer_CantPassAnImmovableEnemyOrBlockingEntities_CrossesTheFamily` (an ordinary enemy in the corridor is now shoved), `Steer_EndsInAFullWhirlAtTheDestinationOnly` (the enemy that stood beside the path would now ride; moved onto a passed cell's arm), `Steer_WhirlCanPullIntoTheCellTheCycloneLeft_AndThePreviewPlansTheSame` replaced by `Steer_TheEnemyBehindFollowsIntoTheCellTheCycloneLeft_CarriedNotPulled` (the enemy behind now rides instead of being pulled).

## Needs THJ

none (no core change was needed: the move events are public bus events, already raised from non-pusher code by `AEffectSwapper`).

## Docs to update

- `tech/core-systems.md` Cyclone note: no core change in C2. `EnemyAlertTracker.WakeMovedUnit` now also used by the carry.
- GDD `characters/lucy.md` LU-6 and `design/cyclone-redesign.md` (C5 owners): the as-built details above (detour rule, what blocks in front, riders' cells during the glide).
- Steer's ability text and `CycloneSteerSetup.Description` still say "not through walls or enemies" and "without hitting them": C5 text pass.

## Risks and loose ends

- **Plan miss (C4):** `CycloneSteerPreview` still plans the Whirl's pull ghosts on the live board, so with riders its ghosts can be wrong until C4 reworks it on `AEffectCycloneSteer.PlanFor`. C4 will also need the Whirl's pull planned on the board after the carry: `CycloneWhirlPlanner.PlanPulls` reads `cell.OccupantEntity` directly, so it needs an occupancy override (e.g. `plan.OccupantOf`) to preview the post-carry pull. Not done here (no behavior need in C2).
- Plan miss: the design says the Whirl's pull "may pay Crippled once, as built". As built it doesn't: `Lucy_Cyclone_Whirl_Pusher.asset` has no `onMoveEffects`. Only the family's pushers deal Crippled.
- Unity does not run a coroutine's `finally` on `StopCoroutine` or destroy (reviewer note from C1). With riders never off a cell across frames this no longer matters for the carry; the landing itself is one synchronous block.
- If a rider is moved by something else during the glide (not expected on Lucy's turn) and lands on another rider's planned cell, `PlugEntity`'s nearest-cell fallback puts the second one beside it.
- C1 is still uncommitted and shares most files with C2 (see Proposed commits).

## Proposed commits

C1 is not committed yet and C2 edited eight of its files, so the two cannot be split by whole files (only `git add -p`, which the coordinator can't run here). Two options:

1. Preferred, one commit for both: `feat(lucy): a Steer carries the enemies beside the Cyclone and ends in a full Whirl, and Cyclone Power hits for 3, 4 and 5 times damage` (plain):
   - `miso/Assets/_Project/Features/Player/Lucy/Scripts/Cyclone/AEffectCycloneSteer.cs`
   - `miso/Assets/_Project/Features/Player/Lucy/Scripts/Cyclone/CycloneCarryPlanner.cs`
   - `miso/Assets/_Project/Features/Player/Lucy/Scripts/Cyclone/CycloneCarryPlanner.cs.meta`
   - `miso/Assets/_Project/Features/Player/Lucy/Scripts/Cyclone/CycloneEntity.Steer.cs`
   - `miso/Assets/_Project/Features/Player/Lucy/Scripts/Cyclone/CycloneEntity.Whirl.cs`
   - `miso/Assets/_Project/Features/Player/Lucy/Scripts/Cyclone/CycloneRules.cs`
   - `miso/Assets/_Project/Features/Player/Lucy/Scripts/Cyclone/CycloneSteerPreview.cs`
   - `miso/Assets/_Project/Features/Player/Lucy/Scripts/Cyclone/CycloneSteerRules.cs`
   - `miso/Assets/_Project/Features/Player/Lucy/Scripts/Cyclone/CycloneSteerSteps.cs`
   - `miso/Assets/_Project/Features/Player/Lucy/Scripts/Cyclone/CycloneWhirlPlanner.cs`
   - `miso/Assets/_Project/Features/Player/Lucy/Scripts/Cyclone/CycloneWhirlSteps.cs`
   - `miso/Assets/_Project/Features/Player/Lucy/Scripts/Cyclone/ICycloneSteerSteps.cs`
   - `miso/Assets/_Project/Features/Player/Lucy/Scripts/Cyclone/ICycloneWhirlSteps.cs`
   - `miso/Assets/_Project/Features/Player/Lucy/Scripts/Editor/CycloneSteerTests.cs`
   - `miso/Assets/_Project/Features/Player/Lucy/Scripts/Editor/CycloneSteerTests.Carry.cs`
   - `miso/Assets/_Project/Features/Player/Lucy/Scripts/Editor/CycloneSteerTests.Carry.cs.meta`
   - `miso/Assets/_Project/Features/Player/Lucy/Scripts/Editor/CycloneWhirlTests.cs`
   - `miso/Assets/_Project/Resources/UnitSpecific/Player/Lucy/Abilities/Cyclone/Lucy_Cyclone_Ability.asset`
2. If THJ wants C1 and C2 apart: THJ stages the C1 hunks by hand (`git add -p`) for the eight shared files (`AEffectCycloneSteer.cs`, `CycloneEntity.Steer.cs`, `CycloneEntity.Whirl.cs`, `CycloneSteerRules.cs`, `CycloneSteerSteps.cs`, `ICycloneSteerSteps.cs`, `CycloneWhirlSteps.cs`, `CycloneSteerTests.cs`) plus the C1-only files, using C1's message from `reports/cyclone-r2-c1.md`; then a second commit `feat(lucy): a Steer carries the enemies beside the Cyclone: shoved in front, dragged beside, followed behind, one landing each` with the rest (C2-only files: `CycloneCarryPlanner.cs` + `.meta`, `CycloneSteerTests.Carry.cs` + `.meta`).

Do not stage `PreloadScreen.unity`, `ProjectSettings/*` or the TMP fallback font (THJ's).

## Other branches

none (scope: `thj/cyclone`)

## How to see it

1. In Unity, Test Runner, EditMode, Run All: only `AIRegressionTest.Baseline_MatchesCurrentAI` red (inner 43).
2. Play a level with Lucy; cast the Cyclone, wait for an enemy turn so enemies end up beside it (or cast next to a Claw).
3. Pick Steer. The range highlight should leave out any cell whose front enemy can't be shoved (an enemy with a wall, a unit or a rock right behind it, an Immovable or large enemy in front) and every cell past it on that line.
4. Steer up to 3 cells with a Claw beside it: the Claw glides along with the Cyclone and lands next to it, then the Cyclone swells, pulls arm enemies, and hits. An enemy in front is shoved one cell ahead each step; one behind follows.
5. Put spikes on a cell a carried enemy passes over: no damage there. Spikes on its landing cell: they fire.
6. Steer a Claw into Linda's lane: Watch fires once for it, before the Whirl's hit.
7. Harmonic Slam a Claw (Crippled), then carry it 3 cells: it takes only the Whirl's hit (3), no Crippled damage on the way.
8. Combat log: "Whirl · Lucy: carried N, pulled N, hit M" with the real carried count.
9. Note: the Steer preview's pull ghosts are not carry-aware yet (C4).
