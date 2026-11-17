# Report: Cyclone round 2, C3c (AI heavy handling, core) + C3b review should-fixes

Plan: plans/2026-11-17-cyclone-round2-tech.md (chunk C3, sub-chunk C3c; core AI approved D-533 / D-550; design plans/2026-11-17-cyclone-round2-design.md §4 E, §5 "Heavy's turn coming")    Agent: miso-implementer    Branch: thj/cyclone (on top of the uncommitted C1, C2, C3a, C3b)
Outcome: **partial**. Items 1, 2, 4, 5 done and green. Item 3 (wobble on a heavy's intent path) **not built: blocked on a wrong premise.** The game has no enemy intent path to hook. Options are listed under "Needs a decision".

## What changed

Core (AI, 2 files edited + 1 new; additive; BOM and LF kept as at HEAD):

- `miso/Assets/_Project/Core/Systems/AISystem/Runtime/AIEndOfTurnDangerCells.cs` (new, + `.meta`, LF, no BOM like its sibling `AIUnitBrain.EndOfTurnDanger.cs`):
  - New neutral interface `IAIEndOfTurnDangerSparesMover { bool SparesMover(GridPluggableEntity mover); }`.
  - New class `AIEndOfTurnDangerCells : HashSet<Vector2Int>`: the danger set exactly as before, plus a list of (unit, its own cells) for units that some source spares. `For(mover)` returns that unit's own set, or `this`. It scans with `ReferenceEquals` only, so it is safe on the worker thread.
- `miso/Assets/_Project/Core/Systems/AISystem/Runtime/AIEndOfTurnDanger.cs` (BOM kept):
  - `Snapshot(Faction)` now returns `AIEndOfTurnDangerCells`. This is source-compatible: it is still a `HashSet<Vector2Int>`, so `AIFactionBrain` (3 call sites), `AIBlackboard.SetEndOfTurnDanger` and the existing tests compile and behave unchanged.
  - Each source's cells are collected into their own set and unioned. The union is the same set as before.
  - Only when some source implements the new interface and has cells, a new private `AddSparedMovers` runs on the main thread. It goes through the faction's units on the board (a large unit is counted once) and asks each sparing source about each unit. For each spared unit it stores the cells of the sources that don't spare it.
  - New `CellsFor(ICollection<Vector2Int> danger, GridPluggableEntity mover)`, worker-safe: it returns `snapshot.For(mover)` when `danger` is a snapshot, otherwise `danger` itself.
- `miso/Assets/_Project/Core/Systems/AISystem/Runtime/AIUnitBrain.EndOfTurnDanger.cs`: `RefusesEndingOn` passes `AIEndOfTurnDanger.CellsFor(_blackboard.EndOfTurnDanger, _unit)` instead of the blackboard set (1 line changed, 2 added). For a non-heavy unit, or when no source spares anyone, this is the very same set object as before.

Not touched in core: `AIFactionBrain.cs`, `AIBlackboard.cs`, `AIUnitBrain.cs`, `UtilityVariables.cs`, `GridCell*`, `GUnit.cs`, `AIController.cs`, any UI.

Cyclone (`miso/Assets/_Project/Features/Player/Lucy/Scripts/Cyclone/`, LF no BOM, as at HEAD; note: the brief said CRLF, but HEAD and the working tree are LF):

- `CycloneEntity.AIDanger.cs`:
  - Implements `IAIEndOfTurnDangerSparesMover`: `SparesMover(mover) => CycloneHeavy.IsHeavy(mover, pullTagQuery)`. The heavy predicate stays defined once.
  - `CollectDangerCells` returns early `|| HasBurst` (review should-fix 1).
  - Header comment updated, `using MISO.Core.Systems.GridSystem` added.
- `CycloneEntity.LineOfFire.cs`: `CollectLineOfFireBlockers` returns early `|| HasBurst` (review should-fix 1).
- `CycloneEntity.Burst.cs` (C3b file): `NotifyReadyChanged()` is called right after `HasBurst = true` (review should-fix 2).

Tests (`miso/Assets/_Project/Features/Player/Lucy/Scripts/Editor/`):

- `CycloneAIHeavyTests.cs` (new, + `.meta`), 8 tests:
  - `Snapshot_SparesHeavies_NotLightEnemies`
  - `CellsFor_APlainSet_IsTheSameSetForEveryone`
  - `AHeavyDoesNotRefuseTheCross_ALightEnemyStillDoes` (all 8 arm cells)
  - `ALargeUnitWithOneCellOnAnArm_IsNotRefused`
  - `AnotherDangerSource_StillCountsForAHeavy` (a second Cyclone with an empty pull filter does not spare a 1x1 Immovable unit, and its arm overlaps the first Cyclone's)
  - `NoSourceSparesTheUnit_ItReadsTheFactionsSet`
  - `TheWorkerThreadReads_TheSnapshotForEachUnit` (`CellsFor` + `RefusesEndingOn` on a real `System.Threading.Thread`: no exception, correct answers)
  - `AHeavyWalksThroughTheCyclone_AndEndsOnTheArm_ALightEnemyGoesAround` (the heavy's move range never contains the Cyclone cell; with the real reach and snapshot the heavy ends on the arm beside Lucy even with no attack; a light enemy ends off the cross)
- `CycloneBurstTests.cs` (C3b file), main burst test, new assertions:
  - Before the burst, the danger snapshot and the line-of-fire snapshot are non-empty.
  - After the burst's first step (ring still playing, Cyclone alive), both are empty and `ReadyChanged` has fired once.
  - After dispose, `ReadyChanged` has fired twice.

## Design: why a snapshot subclass and a second interface

- Danger is snapshotted per faction on the main thread and handed to the worker as plain coordinates. A per-unit exception needs to know about the unit, but the worker must not touch the danger entities.
- So the snapshot itself computes, on the main thread, the cells that still count for each spared unit, and the worker only looks them up by reference.
- Making the snapshot a subclass of the existing `HashSet<Vector2Int>` keeps every existing signature and reader unchanged. There are no edits to `AIFactionBrain` (3 snapshot sites) or `AIBlackboard`, and the brain change is one call.
- A second interface instead of a default-implemented member on `IAIEndOfTurnDanger`: the same as the C3a `IPlantedMoverPass` pattern. It is opt-in, and core never names "heavy" or Lucy types.
- `SparesMover` runs on the main thread only, so the worker never calls Cyclone code for this. It also means `CycloneHeavy.IsHeavy`'s worker safety isn't relied on here. It does still hold, and C3a's walk check relies on it.
- Cost: when no source spares anyone (every level without a Cyclone, and the AI regression scenes), no units are scanned. The set is identical to before except that it is a subclass instance.

## Acceptance criteria (C3c part)

- [x] A heavy's end-of-turn filter does not refuse the cross; non-heavies keep their current behaviour exactly. Covered by the snapshot, refusal, large-footprint, mixed-source, no-spare and choose-destination tests above. A non-heavy gets `AreSame(snapshot)`: the same object, not just equal contents.
- [x] Worker-thread safe. The worker reads only `ReferenceEquals` lookups in a structure built on the main thread (worker-thread test). No new statics, no Unity-object calls on the worker.
- [x] AI movement and path (item 2, by reading):
  - `UtilityVariables.GetBestForeseenPath` (line 396) and `ResolvePath` (line 445) both pass `mover: unit`.
  - The live turn's move candidates come from `GetAbilityRangeCells(..., source: _unit)` (sim == null), which is mover-aware since C3a (`IsFootprintWalkable`).
  - The AI never plans a move ending on the Cyclone cell: `GetRangeCells` drops footprints with a walk blocker (`FootprintHasWalkBlocker`), and `GetAbilityCandidateTargets` also requires `_unit.IsFootprintEmpty(c)`. Tested in `AHeavyWalksThroughTheCyclone...` and C3a's range test.
  - No path cost was added. The burst is the cost of passing (one hit), and the walk cost stays `GetCellCost` like every other cell, as the danger design intends ("walking through costs nothing extra"). Adding a cost would change `GridCell.GetCellCost` for everyone.
- [x] Line of fire unchanged for a live Cyclone (enemy shots still blocked). A burst Cyclone blocks no shot (should-fix 1).
- [x] Determinism: the AI regression inner count stays 43 (before 43, after 43).
- [ ] **Wobble when a heavy's intent path crosses the Cyclone: not built** (see "Needs a decision").
- [x] Should-fix 1 (`|| HasBurst` in danger and line of fire) and should-fix 2 (`NotifyReadyChanged` at the burst), each with asserts.

Coverage: everything ticked is EditMode. The brain's own call (`AIUnitBrain.RefusesEndingOn` with real abilities on the worker) is covered by the static calls it makes. End to end it is a play check: a Masher or Queen ends its move on the cross, and a Claw still avoids it.

## Test run

- Before (C3b report): 2082 run, 2081 passed, 1 failed (the known red, inner `CHECKS: 714 FAILURES: 43`).
- Subsets: `CycloneAIHeavyTests` + `CycloneBurstTests` 24 / 24. Earlier run with AIDanger, LineOfFire and Steer tests: all their existing tests passed.
- Full suite after (MCP Test Runner, editor open, no Play mode): **2090 run, 2089 passed, 1 failed, 0 skipped**. The only failure is `AIRegressionTest.Baseline_MatchesCurrentAI`, inner **`CHECKS: 714 FAILURES: 43`** (unchanged). The 8 new tests make up the difference. Compile: no errors (existing warnings only).

## Save reset

No.

## Decisions I made

- Snapshot subclass plus opt-in interface, with spared units resolved on the main thread (reasons above). Tier 2, core, additive. Same behaviour as the brief's suggestions (a default member or a second interface), fewer core files.
- Only units on the board when the snapshot is taken are resolved. A unit not on a cell at that moment (for example, mid-carry) reads the faction's full set, which is the conservative choice.
- No path cost for crossing the Cyclone (reason above).
- Dropped a test-only danger `MonoBehaviour` in the Editor folder: Unity refuses to attach Editor-folder scripts. A second Cyclone with an empty pull filter stands in as a source that does not spare a 1x1 Immovable unit.

## Needs a decision (coordinator, possibly THJ): the wobble trigger

1. **What:** the plan says "when a heavy's intent path (the enemy intent preview) crosses a live Cyclone, the Cyclone wobbles". The game has no enemy intent path.
2. **Found:**
   - `AIController.UpdateFutureTargets` (on `abilityPerformed` and `turnStarted`) runs `AIFactionBrain.RequestPredictAllTargets`. Its result per unit is `(targets, chosenAction)`, applied as `GUnit.SetFutureTargets`. This draws only the target avatars (`FutureTargetsPanelUI`) and, on hover, the attack's affected cells (`SetFutureTargetsHover`).
   - `chosenAction` is the predicted attack, never the move. `CollectTargets` returns false for Transporter moves, and the simulated moves (`ApplySimAction`) are thrown away. `_futureAction` is private on `GUnit`, and there is no event.
   - The prediction ranges moves with the sim branch of `GetAbilityRangeCells`, which passes no `source`/mover. So **predicted** heavy moves never cross the Cyclone, while the live turn's moves do (C3a). The intent avatars can therefore under-predict a heavy whose target is reachable only through the Cyclone.
   - The hover threat preview (`ShowStatsHoverPreview` → `UnitThreatAnalysis.GetReachableCells`) is a reach area, not a path.
3. **Options:**
   - (a) Cyclone-only, no core: on the same public events the intent refresh uses (`turnStarted`, `abilityPerformed`, `unitDied`) plus Cyclone spawn and Steer, the Cyclone wobbles while some live heavy enemy's mover-aware shortest path to its nearest family unit crosses its cell within that heavy's move reach. Stop on burst or dispose, when no heavy qualifies, and at level end. Roughly 1 partial + 1 pure rule + tests. It is "a heavy is coming through", not "the intent".
   - (b) Core, additive, Tier 3: make the prediction keep the heavy's predicted move. That means the sim move destination in `AIUnitBrain.PredictNextTargets`, carried through `AIFactionBrain` → `AIController` → a read-only `GUnit.FutureMove` or an event, and ideally the sim range made mover-aware too. This touches `AIUnitBrain`, `AIFactionBrain`, `AIController` and `GUnit`, and prediction changes can move the AI regression count.
   - (c) Cyclone-only, at the heavy's own turn: when an AI heavy enemy is selected (`unitSelectionChanged`) and its live move path crosses, wobble until it moves. The window is short (camera focus + wait), and the live path is only known when the move starts.
4. **Recommendation:** (a). It is honest to the design's intent (a warning before the heavy walks in), stays in Cyclone code, and adds no AI regression risk. (b) only if THJ wants the wobble tied to the AI's exact plan.
5. **Also worth a decision:** whether to make the prediction's sim range mover-aware for heavies (part of (b)), so the target avatars match the live turn.

## Docs to update

- `tech/core-systems.md` (coordinator), AI row and Cyclone note: `IAIEndOfTurnDangerSparesMover`, `AIEndOfTurnDangerCells` (`Snapshot` returns it; per-unit cells resolved on the main thread; `CellsFor` on the worker), the brain uses `CellsFor`, the Cyclone spares heavies, and a burst Cyclone is no danger and blocks no shot.
- GDD `enemies.md` EN-18 (designer): heavies are exempt from avoiding the cross.

## Risks and loose ends

- **Prediction versus live turn for heavies** (above): the intent avatars come from a sim range that is not mover-aware. Not changed here.
- A heavy may now end its move on a touching cell. If the Cyclone is still alive at that turn end (the heavy reached the cell without crossing the Cyclone), the end-of-turn Whirl hits it. This is the intended trade-off ("heavies don't refuse the cross").
- `AEffectDashAttack` still paths without a mover (C3a note). Unchanged.
- Commit split: `CycloneEntity.Burst.cs` and `CycloneBurstTests.cs` are new, uncommitted C3b files. The should-fix lines in them fold into the C3b commit. `CycloneEntity.AIDanger.cs` and `CycloneEntity.LineOfFire.cs` were clean before this chunk.

## Proposed commits

Order after the C1, C2, C3a and C3b commits. The should-fix lines in the two new C3b files (`CycloneEntity.Burst.cs`, `CycloneBurstTests.cs`) go into the C3b commit.

1. `feat(ai): a dangerous-ground source can spare chosen units, read per unit by the unit brain` (**core**, own commit; builds alone, no behaviour change until something implements the interface):
   - `miso/Assets/_Project/Core/Systems/AISystem/Runtime/AIEndOfTurnDangerCells.cs` + `.meta`
   - `miso/Assets/_Project/Core/Systems/AISystem/Runtime/AIEndOfTurnDanger.cs`
   - `miso/Assets/_Project/Core/Systems/AISystem/Runtime/AIUnitBrain.EndOfTurnDanger.cs`
2. `feat(lucy): heavy enemies may end a move on the Cyclone's cross; a burst Cyclone is no danger and stops no shot` (plain; depends on 1 and on C3b's `HasBurst`):
   - `miso/Assets/_Project/Features/Player/Lucy/Scripts/Cyclone/CycloneEntity.AIDanger.cs`
   - `miso/Assets/_Project/Features/Player/Lucy/Scripts/Cyclone/CycloneEntity.LineOfFire.cs`
   - `miso/Assets/_Project/Features/Player/Lucy/Scripts/Editor/CycloneAIHeavyTests.cs` + `.meta`
   - If C3b is already committed by then, also `CycloneEntity.Burst.cs` and `CycloneBurstTests.cs` (the should-fix lines).

## Other branches

None (Cyclone lives on `thj/cyclone`; the core change is additive).

## How to see it

1. Test Runner, EditMode: run `CycloneAIHeavyTests` (8 green) and `CycloneBurstTests` (16 green), then Run All. Only `AIRegressionTest.Baseline_MatchesCurrentAI` is red (inner 43).
2. In play: cast the Cyclone between Lucy and a Masher (or the Goblin Queen), with a Claw nearby.
   - On the enemy turn the Masher walks through (bursts it) or stops on an arm cell next to the family without hesitating.
   - The Claw still keeps off the arms unless it can attack from there.
3. After a burst, during the short ring, the Steer button is already off. An enemy archer's shot through the spent Cyclone's cell is allowed (threat preview included).
4. No wobble yet (pending the decision above).
