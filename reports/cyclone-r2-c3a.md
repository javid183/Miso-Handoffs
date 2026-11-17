# Report: Cyclone round 2, C3a (Walk exception, core)

Plan: plans/2026-11-17-cyclone-round2-tech.md (chunk C3, sub-chunk C3a; core approval D-550, rule CR-58)    Agent: miso-implementer    Branch: thj/cyclone (on top of the uncommitted C1 and C2)
Outcome: done (compiled in the open editor through the Unity MCP; EditMode run, see "Test run")

## What changed

Core (3 files, all under `miso/Assets/_Project/Core/Systems/GridSystem/Runtime/`; 27 lines added, 3 changed; BOM and LF kept):

- `GridCell.cs`: `CheckIfUnitWalkable(faction, ignoreRelation)` now forwards to a new additive overload `CheckIfUnitWalkable(faction, ignoreRelation, GridPluggableEntity mover)` with `mover: null`. The body is the old one; only its last clause passes the mover on (`PlantedLetsPass(oge, requestFaction, mover)`). With a null mover the result is identical to before. Why: the walk check needs to know who moves to let a heavy through.
- `GridCell.PlantedPass.cs`: new core interface `IPlantedMoverPass { bool LetsMoverPass(GridPluggableEntity mover); }` (neutral, no Lucy reference) and a private overload `PlantedLetsPass(planted, faction, mover)` = the old faction rule OR (the move has a faction AND a mover is given AND the planted entity implements the interface AND it says yes). The old 2-argument `PlantedLetsPass`, `FootprintHasWalkBlocker` and `HasWalkBlocker` are unchanged. Why: lets a planted blocker name movers it lets through without core knowing what "heavy" is.
- `GridPluggableEntity.cs`: `IsFootprintWalkable` passes `this` as the mover to the new overload (one line). Signature unchanged. Why: this is the single check behind `FindPathTo(mover:)` / `FindPath(mover:)` / `FindAlternativePathsTo`, the Transporter's per-step stop check (`AEffectTransporter.MoveEntity`), `AEffectCommand`'s step check, `AreaShapeDefinition` PathWalkable and `GetRangeCells(source:)` PathWalkable, so heavies pass in all of them without editing `GridActions.cs` or `AEffectTransporter.cs`.

Cyclone side (`miso/Assets/_Project/Features/Player/Lucy/Scripts/`):

- `Cyclone/CycloneHeavy.cs` (new, + `.meta`): the one definition of heavy. `IsHeavy(bool failsPullFilter, Vector2Int placementSize)` (pure) and `IsHeavy(GridPluggableEntity mover, GTagQuery pullFilter)`: fails the Cyclone's pull tag query (the prefab's query leaves out `EntityState.Unmovable`, the same query `CycloneWhirlSteps.IsPullable` uses) or effective footprint larger than 1x1. An empty query counts as "nobody left out", so only the size counts then. Reads `TagSet`, `PlacementSize` and the tag registry only; no Unity-object calls. For C3b (burst) and C3c (AI) to reuse.
- `Cyclone/CycloneEntity.HeavyPass.cs` (new partial, + `.meta`): `CycloneEntity : IPlantedMoverPass`, `LetsMoverPass(mover) => CycloneHeavy.IsHeavy(mover, pullTagQuery)`.
- `Editor/CycloneHeavyPassTests.cs` (new, + `.meta`): 15 tests (see Acceptance criteria).

Not touched: `GridActions.cs`, `AEffectTransporter.cs`, `AEffectDashAttack.cs`, `UnitsCooperationHandler.cs`, `OnGridEntity.cs`, the Cyclone prefab, any asset, `IsWalkable`, `FootprintHasWalkBlocker`. C1/C2 files untouched. THJ's `PreloadScreen.unity`, `ProjectSettings/*` and TMP font untouched.

## Design: why an interface on the planted entity

The brief suggested a flag on `OnGridEntity` (e.g. `PassesHeavyMovers`, set on the prefab) plus a mover-side heavy predicate in core. I chose a core interface the Cyclone implements instead, because:

- "Heavy" is then defined exactly once, in Cyclone code (`CycloneHeavy`), and core never names it. With a flag, core would need its own heavy predicate (a second definition, and the Unmovable tag id or the pull query hard-coded in core) or a reference from core to Lucy feature code.
- No new serialized field, no prefab edit, no `[FormerlySerializedAs]` question; the Cyclone's own pull filter already holds the Unmovable query.
- It follows the existing pattern of the Cyclone's other core hooks (`ILineOfFireBlocker`, `IAIEndOfTurnDanger`).
- Default behaviour for every other planted entity is untouched: they don't implement the interface, so the new clause is false for them.

## Acceptance criteria (C3a part)

- [x] A heavy mover (Immovable tag or footprint larger than 1x1) paths and walks through the Cyclone cell: `ImmovableEnemy_PathsAndWalksThroughTheCyclone_ButCantStopOnIt` (FindPath with mover through a one-cell corridor; the Transporter's step check `IsFootprintWalkable(next, ownerFaction, ignore)` passes), `LargeEnemy_PathsThroughTheCyclone` (2x2 across a 2-row board whose every crossing covers the Cyclone; step check passes with the Cyclone inside the footprint), `ImmovableEnemy_MoveRange_ReachesPastTheCycloneButNotOntoIt` (move range `GetRangeCells(source:)` = 1, 2, 3, 5, 6, 7).
- [x] Heavy cannot stop (end a move) on the Cyclone cell: same tests assert `IsWalkable` false, `IsFootprintEmpty` false, no path with the Cyclone cell as destination, the range omits it. Stop rule (`IsWalkable`, `FootprintHasWalkBlocker`) unchanged.
- [x] Non-heavy enemies still blocked and stop short: `LightEnemy_IsStillKeptOut` (mover-aware check false, no path, the Transporter step check fails so the walk stops on the cell before, range 1, 2, 3). The existing `CyclonePassTests` and `CycloneStopShortTests` still pass unchanged.
- [x] Family still passes and cannot stop: `Family_StillPasses_AndCantStop` (with and without an Unmovable tag on the family mover).
- [x] Faction-less moves (pushes, pulls, entity moves) still stop before it, heavy or not: `AHeavyMovedWithoutAFaction_StillStopsBeforeIt`.
- [x] A non-Cyclone planted blocker still blocks heavies: `OtherPlantedBlockers_StillKeepHeaviesOut` (Immovable and 2x2).
- [x] Consumers of the pass rule still behave: dash approach `Dash_ByAHeavyThroughTheCyclone_NeverApproachesFromItsCell`; duo loser stop `DuoLoserStop_ForAnImmovableLoser_StillAvoidsTheCyclone`. `GetRangeCells` ranged reach keeps `FootprintHasWalkBlocker` (unchanged code; covered by the existing `RangedReach_NeverOffersTheCycloneCellAsALanding`). Masher counter walk: `TryPlanAnswer` calls `FindPathTo(..., Unit.Faction, ignore, Unit)` and filters candidates with `IsFootprintEmpty`, so a heavy Masher now plans steps past the Cyclone but never onto it (by code reading; the counter itself is C3b's play check).
- [x] Heavy definition: `Heavy_IsImmovableOrLargerThanOneCell`, `Heavy_ReadsTheLivePrefabsPullFilter` (the real prefab's query), `Heavy_AnEmptyPullFilter_LeavesOnlyTheSize`, `LivePrefab_LetsHeaviesPass`.
- [x] Worker safety: `LetsMoverPass` / `CycloneHeavy.IsHeavy` read `ReferenceEquals`, `TagSet`, `PlacementSize` and the tag registry match (the same `TagSet.Match` path `AEffectBase`'s feasibility check already runs on the AI worker). Core uses `ReferenceEquals` for the mover null check. No new statics.
- Not in C3a (later chunks): burst on entry (C3b), AI end-of-turn filter and wobble (C3c).

Coverage: everything above is EditMode. Needs a play check (with C3b, since without the burst a heavy now crosses a live Cyclone): Masher counter walk and Queen's charge crossing the Cyclone in a level.

## Test run

- Before (C2 report, final): 2051 run, 2050 passed, 1 failed (the known red, inner 43).
- New subset after: `CycloneHeavyPassTests` 15 / 15 passed.
- Full suite after (MCP Test Runner, editor open, no Play mode): 2066 run, 2065 passed, 1 failed, 0 skipped. The only failure is `AIRegressionTest.Baseline_MatchesCurrentAI`, inner `CHECKS: 714 FAILURES: 43` (unchanged). The 15 added tests make up the difference from 2051. Compile: no errors (existing warnings only).

## Save reset

No.

## Decisions I made

- Interface on the planted entity instead of a flag on `OnGridEntity` (same behaviour; reasons above). Tier 2 (core, additive).
- The heavy exception needs a move with a faction, like the existing pass rule: a heavy that is pushed or pulled (no faction) still stops on the cell before. Keeps pushes exactly as they were; the brief's "walk through" is about a unit's own move.
- `IsFootprintWalkable` itself became mover-aware (its signature unchanged) rather than adding a new `IsFootprintWalkable` overload and editing every caller. This is the least invasive way to cover `FindPathTo(mover:)` and the Transporter's stop check together; the only behaviour change is for a heavy mover next to a planted entity that implements `IPlantedMoverPass` (today only the Cyclone).
- Heavy by tag = "fails the Cyclone's pull filter", so it reads the same serialized query `IsPullable` uses (the plan's "same query"). If THJ later adds tags to the pull filter, they also make a unit heavy.
- Transporter walk tested through its exact per-step check (`IsFootprintWalkable(next, ownerFaction, ignore)`) and the mover path it builds (`FindPathTo(..., mover: entity)`); the coroutine itself does not run in EditMode.

## Needs THJ

None.

## Docs to update

- `tech/core-systems.md` (coordinator): Grid row, Cyclone note: additive `GridCell.CheckIfUnitWalkable(faction, ignore, mover)` overload, `IPlantedMoverPass` (GridCell.PlantedPass.cs), `GridPluggableEntity.IsFootprintWalkable` passes itself as the mover; the Cyclone implements it via `CycloneHeavy`.
- `design/gdd/combat-rules.md` CR-58 (designer): heavy exception, only for a unit's own move (pushes and pulls still stop before).

## Risks and loose ends

- **Until C3b lands, a heavy crosses a live Cyclone without bursting it.** Don't play-test C3a alone expecting the burst.
- **The AI already sees the new reach.** The AI's move range (`GetRangeCells(source: unit)`) and its mover paths go through `IsFootprintWalkable`, so heavy enemies may plan moves across the Cyclone from C3a on. The end-of-turn danger filter (C3c) still refuses destinations on the cross for them, which is C3c's job. `UtilityVariables` calls `GridPathFinding.FindPath` (lines ~396, ~445); whether those pass a mover was not checked here, for C3c.
- **`AEffectDashAttack` paths without a mover** (`FindPathTo(..., requestFaction)` only), so a heavy's dash still routes around the Cyclone. The Queen's charge is a Transporter (`GoblinQueen_Ability_Charge_Effect_UnittTransport`), so it is covered; any enemy dash ability is not. Changing the dash path is out of C3a scope.
- **Transporter `movementBlockTagQuery`** (a tag that stops a walk mid-path) could stop a heavy on the Cyclone cell; the same is already true for the family. C3b's burst on entry removes the Cyclone, so this stops mattering then.
- An enemy that gets `EntityState.Unmovable` temporarily (any effect that applies it) counts as heavy while it has it, by the definition.
- Thread safety of `TagSet.Match` relies on `GlobalSettingsSO.Instance` being loaded on the main thread first (already true in play; existing `AEffectBase` precedent).

## Proposed commits

1. `feat(grid): a planted walk blocker can let chosen movers pass through its cell` (core, own commit): `miso/Assets/_Project/Core/Systems/GridSystem/Runtime/GridCell.cs`, `miso/Assets/_Project/Core/Systems/GridSystem/Runtime/GridCell.PlantedPass.cs`, `miso/Assets/_Project/Core/Systems/GridSystem/Runtime/GridPluggableEntity.cs`. Builds alone (no behaviour change until something implements the interface).
2. `feat(lucy): heavy units walk through the Cyclone but can't stop on it` (plain): `miso/Assets/_Project/Features/Player/Lucy/Scripts/Cyclone/CycloneHeavy.cs` + `.meta`, `miso/Assets/_Project/Features/Player/Lucy/Scripts/Cyclone/CycloneEntity.HeavyPass.cs` + `.meta`, `miso/Assets/_Project/Features/Player/Lucy/Scripts/Editor/CycloneHeavyPassTests.cs` + `.meta`. Depends on 1. (C1 and C2 commits come first in the plan's order; this one does not touch their files.)

## Other branches

None (Cyclone lives on `thj/cyclone`; the core change is additive and merges with `main` when the branch does).

## How to see it

1. Test Runner, EditMode: run `CycloneHeavyPassTests` (15 green), then Run All: only `AIRegressionTest.Baseline_MatchesCurrentAI` red (inner 43).
2. In play (better after C3b): cast the Cyclone in a corridor between the family and a Masher (or the Goblin Queen). On the enemy turn the Masher walks through the Cyclone's cell and ends on a cell past it, never on it; a Claw in the same spot still stops before it; family units still walk through and can't end on it.
