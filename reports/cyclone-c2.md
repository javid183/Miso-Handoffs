# Report: Cyclone redesign, C2 (who walks through the Cyclone, and how the AI treats its cross)

Plan: plans/2026-11-11-cyclone-redesign-tech.md    Agent: miso-implementer (opus)    Branch: thj/cyclone
Outcome: done (THJ play check pending). Core changes as approved (D-533), each in its own proposed commit.

## What changed

Paths under `miso/Assets/_Project/`. All files LF; BOMs kept (new core files under `GridSystem/` and `AISystem/` have a BOM like their siblings, `AIUnitBrain.EndOfTurnDanger.cs` none like `AIUnitBrain.cs`). Metas were made by Unity.

### A. Walk rule (core)
- `Core/Entities/Runtime/OnGridEntity.cs`: new serialized `passRelation` (`FactionsRelationType`, default 0 = none) + `PassRelation` getter, with a tooltip. Additive. Every existing planted entity reads 0 and behaves as before.
- `Core/Systems/GridSystem/Runtime/GridCell.cs`: the planted clause of `CheckIfUnitWalkable` gets one extra `|| PlantedLetsPass(oge, requestFaction)`. `IsWalkable` (the "can stop" check) is untouched.
- `Core/Systems/GridSystem/Runtime/GridCell.PlantedPass.cs` (+ .meta, new partial): `PlantedLetsPass`. It passes only when the pass relation isn't 0, the mover has a faction, and the entity's owner has one, and `passRelation` contains `GetFactionsRelation(requestFaction, ownerFaction)`. It reads plain fields with `ReferenceEquals` null checks, so it's safe on the AI worker.
- `Features/Player/Lucy/Prefabs/Cyclone.prefab`: `passRelation: 1` (Ally). `disallowWalk` stays 1.

Relations: levels have only Ally and Enemy, and the level base makes Neutral an ally of the Bergsons. So passing on Ally covers the family, allies, neutrals and decoys (a decoy is in the family's faction). Enemies get Enemy and are blocked. A null faction (pushes, pulls, entity moves) is blocked, so they stop on the cell before.

### B. AI cross danger (core)
- `Core/Systems/AISystem/Runtime/AIEndOfTurnDanger.cs` (+ .meta, new):
  - interface `IAIEndOfTurnDanger.CollectDangerCells(Faction, ICollection<Vector2Int>)`.
  - static `AIEndOfTurnDanger`, stateless:
    - `Snapshot(faction)`: main thread. Scans `GridManager.GridCells` for planted entities that implement the interface and returns plain coordinates.
    - `Touches(footprint, danger)`.
    - `AllowsEndingOn(dangerous, canAttackFromThere)`.
- `AIBlackboard.cs`: holds the job's danger set (`SetEndOfTurnDanger`, `HasEndOfTurnDanger`, `EndOfTurnDanger`).
- `AIFactionBrain.cs`: `PrepareUnitTurn` and `RequestPredictAllTargets` take the snapshot on the main thread before `AIWorker.Run`. The job sets it on the blackboard first. So the real turn and the intent preview see the same danger.
- `AIUnitBrain.cs`: now `partial`. In `GenerateScoredTurnActions` the target loop has one added line: `if (RefusesEndingOn(ability, targets[t], sim)) continue;`.
- `AIUnitBrain.EndOfTurnDanger.cs` (+ .meta, new partial): `RefusesEndingOn`. It applies to plain moves only: abilities with a transporter that aren't attacks themselves. A move whose footprint at the destination touches the danger set is dropped, unless an attack is left this turn that reaches an enemy from there. That check simulates the turn after the move (remaining AP by the same spending rule as `ApplySimAction`, the cooldowns live or simulated, the range from the destination through the existing `GetAbilityRangeCells`). In the editor, the AI log says "Skipped: ends on dangerous ground…".
- `Features/Player/Lucy/Scripts/Cyclone/CycloneEntity.AIDanger.cs` (+ .meta, new partial): the Cyclone implements `IAIEndOfTurnDanger`. It returns its arm cells (`CycloneRules.ArmCells`, 2 each way) for factions that are enemies of its owner's faction (the same relation the Whirl uses). It returns nothing when it isn't alive.

No new statics: the snapshot travels with each job and lives on the blackboard instance, so `PlayModeStaticReset` needs no new hook.

### C. Leftovers
- `CycloneEntity.Whirl.cs:84-85`: comment now says the hold is registered by `WhirlRoutine` when it starts.
- `reports/cyclone-c1b.md` Risks: "300-frame cap" changed to "the 3 s pull cap (real seconds, paused time not counted)".

### D. Tests (new, in `Features/Player/Lucy/Scripts/Editor/`, + .meta each)
- `CycloneTestFactions.cs`: a test combat level with family, ally, neutral and enemy factions. The level instance is set by reflection and restored on Dispose.
- `CyclonePassTests.cs` (12 cases) and `CycloneAIDangerTests.cs` (6).

## Acceptance criteria (C2)

- [x] **Enemies can't enter or path through the Cyclone's cell:** `Enemies_CantEnterOrPathThrough` (walk check false; no path in a one-cell corridor; the move reach stops at the cell before).
- [x] **A push or pull into it stops on the cell before:** `APushIntoTheCyclone_StopsOnTheCellBefore(True/False)` runs the real `AEffectPusher.TryGetPushPreview` with distance 5 on an enemy and on a family unit. Both stop at the cell before. The control `APushWithoutTheCyclone_GoesItsFullDistance` covers the empty row. `NoFaction_IsBlocked`. The Whirl's own pull already never lands on the centre (C1b).
- [x] **The family, allies, neutrals and decoys path through but can't end a move on it:** `FamilyAlliesNeutralsAndDecoys_PassThrough_ButCantStop` (walk check true for each; `IsWalkable` false) and `Family_PathsThroughTheCyclone` (the A* path crosses its cell). The real move (`AEffectTransporter`) plugs a passing unit on the cell for one step. `CycloneEntity.Activate` does nothing, and the next step moves it on. That runtime pass is a **play check**.
- [x] **Linda's grounded arrow still never lands on it:** `TheGroundedArrow_IsStillRefusedOnItsCell`. `LivePrefab_LetsAlliesOfLucyPass` pins `disallowWalk` 1 and `passRelation` Ally on the prefab.
- [x] **Other planted blockers unchanged:** `OtherPlantedBlockers_KeepEveryoneOut` (default pass relation 0, blocked for family, neutral, enemy and no faction, even when the family owns it) and `PlantedEntityThatDoesntBlock_StaysWalkableForEveryone`.
- [x] **The family's own move range is unchanged:** `FamilyMoveRange_IsUnchangedByTheCross` (the same reach as an empty row, minus the Cyclone's own cell, which can't be a stop; every cross cell costs 1). `GetCellCost` isn't touched.
- [x] **The AI treats the cross as dangerous ground**, in three set-ups:
  - `AnotherRouteExists_TheEnemyTakesIt`: without the rule it would end on an arm; with it, it ends off the cross and still closes in.
  - `WalkingInReachesATarget_TheEnemyWalksIn`: it walks onto the arm cell next to Linda, and the same cell is refused when no attack follows.
  - `SealedOffWithNothingReachable_TheEnemyWaitsOutsideTheArms`: in a one-cell corridor it stops 3 cells from the Cyclone.
  - Plus `Snapshot_TheCrossIsDangerousForEnemiesOnly`, `Snapshot_AFadedCycloneIsNoDanger` and `Touches_AnyFootprintCellOnTheCross`.

  What the tests cover: the real grid reach, the real snapshot and the real keep-or-drop rule. The score stands in for a movement graph (closer is better) and the attack check is melee reach 1. The brain's hook (`RefusesEndingOn` with real abilities, AP and cooldowns) isn't driven end to end. EditMode can't build a full `AIUnitBrain` with abilities, so in a level it is a **play check**.

**EditMode suite:** 1965 run, 1964 passed. The only failure is the known red `AIRegressionTest.Baseline_MatchesCurrentAI`, not re-baselined. Its report: 713 checks, **42 inner failures**. None of the 42 names the Cyclone or the AI danger. They are all graph, ability and unit catalog drift, `intent.unit-tile.enemy`, and a `fatal` in `HandleLivingUnitsCondition` during the stress run. C2 adds no utility variable, graph, ability or unit and doesn't touch the planner, so by construction it doesn't move this test. The build log last recorded 41 (the Hearth Claw variant round). I didn't measure the count before C2 in this tree, so I can't attribute the +1. Compile clean, no console errors.

## Save reset

No.

## Decisions I made

- **Where the pass field lives:** a serialized field on `OnGridEntity` (the plan's "field on the entity"), default none, rather than a virtual on the subclass. It's general and additive, and no other prefab changes. This is a small core touch in `OnGridEntity`, inside the walk-exception commit.
- **The pass ignores the mover's `ignoreRelation`.** Only the entity's pass relation against its owner's faction counts. A family move that doesn't pass allies still passes the Cyclone, which matches "family passes through".
- **AI design choice.** First, what decides the outcome:
  - The danger is only where an enemy ends its turn. The Whirl fires at the end of the enemy turn, and walking across an arm does nothing.
  - The AI chooses a destination cell with a utility graph, and the transporter computes the path later with `GetCellCost`.

  So the smallest change that gives the three behaviours is to filter move destinations: drop a cross destination unless an attack is left from there this turn.
  - Not a path cost: raising `GetCellCost` shrinks everyone's moves (ruled out), and a separate AI-only path cost would change routes, not where units end.
  - Not a new `UtilityVariable`: it would need every movement graph edited (AI content), and the regression test pins the variable list, so it would go further red.
  - Not a score penalty: the scale differs from graph to graph. A drop is exact: another destination if one scores, walk in to attack, otherwise wait (no cell kept means no move, or a safer one).

  The same rule runs in the intent prediction, so previews match what happens. Attacks that move the unit themselves (charges, dash attacks) aren't filtered.
- **The snapshot scans the grid** for planted entities with the interface, instead of a registry. That means no new static and no reset hook, and the AI core doesn't reference Lucy's code.

## Needs THJ

None.

## Docs to update

- `tech/core-systems.md` (coordinator):
  - `GridCell.CheckIfUnitWalkable` gains the planted pass exception (`OnGridEntity.passRelation`, compared with the owner's faction; null faction blocked; `IsWalkable` unchanged).
  - AI: `IAIEndOfTurnDanger` / `AIEndOfTurnDanger.Snapshot` taken in `AIFactionBrain` before each job, `AIBlackboard.EndOfTurnDanger`, and the destination filter in `AIUnitBrain.RefusesEndingOn`.
- `tech/combat-architecture.md` (coordinator): "dangerous ground" for the AI is any planted entity that implements `IAIEndOfTurnDanger`.
- The AI regression fix session: the test doesn't drive the brain, so the destination filter needs no baseline entry. The count is 42 now.
- GDD (designer, C5): enemies wait outside the arms unless they can attack from them. Immovable enemies also avoid the far arm cells, though nothing would pull them (see risks).

## Risks and loose ends

- **Play checks:** enemies routing around the cross, walking in to attack, waiting outside, and intent previews matching. The family walking through the Cyclone in a real move (Lucy, John's dash, Command moves, decoys). Watch / Command Shield Dash when a family unit passes the cell.
- A unit whose move is cut short (a movement-block tag, death) while on the Cyclone's cell would stop there. The transporter's existing rule decides that. Rare, and not handled specially.
- The danger set is per faction, not per unit. Immovable enemies (Masher) also avoid the distance-2 arm cells, where they wouldn't be pulled or hit. They still avoid distance 1 correctly. Cheap to refine later if it matters.
- An enemy already standing on the cross with nothing to attack isn't pushed to leave. Only destinations are filtered, so its graph decides whether it moves.
- "Can attack after the move": for targeted attacks it uses the brain's own range. For area attacks around the unit it uses the ability radius from the destination. It ignores `IgnoreRelationOnSelection` and the target-cell conditions of individual effects, so it may rarely allow a destination whose attack the graph then doesn't pick.
- The dead Cyclone copies under the Linda folders keep `passRelation` 0 (they block everyone, as before).
- The AI regression test stays red with 42 inner failures (see above).

## Proposed commits

C2 comes after C1 commits 1–8 in `cyclone-c1b.md`. Two staging notes:
- **Exclude `Features/Player/Lucy/Scripts/Cyclone/CycloneEntity.AIDanger.cs` (+ .meta) from C1 commit 3**: it needs the AI interface from commit 10. C1 commit 3 adds the untracked `Cyclone/` folder, so name its files explicitly.
- `Cyclone.prefab` and `CycloneEntity.Whirl.cs` are C1 files too. The Whirl comment fix just rides in commit 3. The prefab's `passRelation: 1` line can ride in commit 3 as well (Unity ignores an unknown field until commit 9 adds it, so no behaviour changes in between), or be staged by hunk into commit 11.

9. `feat(core): a planted entity can let units of chosen relations to its owner path through its cell without stopping there; pushes and enemies stay blocked` (**core**): `Core/Entities/Runtime/OnGridEntity.cs`, `Core/Systems/GridSystem/Runtime/GridCell.cs`, `Core/Systems/GridSystem/Runtime/GridCell.PlantedPass.cs` (+ .meta). It changes no behaviour by itself (default none).
10. `feat(core): the AI keeps its units from ending a move on ground that hurts them at turn end unless they can attack from there` (**core**, risky: AI behaviour): `Core/Systems/AISystem/Runtime/AIEndOfTurnDanger.cs` (+ .meta), `AIBlackboard.cs`, `AIFactionBrain.cs`, `AIUnitBrain.cs`, `AIUnitBrain.EndOfTurnDanger.cs` (+ .meta). It is inert until something implements the interface.
11. `feat(lucy): the family passes through the Cyclone and enemies treat its cross as dangerous ground` (plain; depends on 3, 9 and 10): `Features/Player/Lucy/Scripts/Cyclone/CycloneEntity.AIDanger.cs` (+ .meta), `Features/Player/Lucy/Prefabs/Cyclone.prefab` (the `passRelation` line, if not in 3), plus in `Features/Player/Lucy/Scripts/Editor/` (each + .meta): `CycloneTestFactions.cs`, `CyclonePassTests.cs`, `CycloneAIDangerTests.cs`.

Don't stage THJ's files (PreloadScreen, ProjectSettings, the TMP fallback font).

## Other branches

`thj/home-test` lacks the redesign; it merges later with the rest.

## How to see it

1. Open a level with Lucy and enemies (a Trail fight). Cast the Cyclone in a corridor or between the family and the enemies.
2. Select John or Linda and look at the move range: cells behind the Cyclone are reachable through it, but the Cyclone's own cell isn't a stop. Move through it; the unit walks over the cell and ends beyond.
3. Push or pull an enemy toward the Cyclone (John's shield push, a Gust later in C3): it stops on the cell before.
4. Linda's grounded arrow never lands on the Cyclone's cell.
5. End the turn:
   - An enemy with another way round goes around the cross.
   - An enemy that can reach a family member only by standing on an arm walks onto the arm and attacks (then gets pulled and hit by the Whirl).
   - In a one-cell corridor sealed by the Cyclone, the enemy stops 3 or more cells away instead of stepping onto the arm.
6. Hover an enemy for its intent preview before ending the turn: it matches what it then does.
7. Tools > AI log viewer (editor): a refused destination shows "Skipped: ends on dangerous ground with no attack after the move".
