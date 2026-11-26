# M3 barriers: code read (2026-11-26)

Read-only Explore survey on `main` for the M3 redesign (`plans/2026-11-26-m3-redesign.md`). Saved by the coordinator; the agent could not write files. Paths are under `miso/Assets/_Project/` unless absolute. The AI regression test was not run.

## Summary

- **The rock is the nearest thing that exists.** It's a `UnitBase` variant (a `GUnit` with HP), Neutral, tagged Unmovable and Unable to Swap.
  - Under the default `LevelBase` relations (Bergsons–Neutral Ally, Enemy–Neutral Enemy), a Neutral unit already acts almost like a barrier: Claws can't walk through it and can attack it, and the family walks through it.
  - M3 sets Enemy–Neutral to Ally on purpose, so Claws ignore the stone. Under that setting a Neutral barrier would be walked *through* by Claws and the Masher, since their walks pass allies (`ignoreRelationOnWalk: 1`).
- **Toba's Wall and the mushroom are not units.** Both are planted `HazardEntity` objects that block walking. The Wall can't be targeted and has no death wiring. The mushroom can be targeted and explodes at 0 HP.
- **Nothing attacks whatever blocks it.** An enemy with no path walks to the reachable cell nearest the family and idles there. AI targeting goes only by `GetFactionsRelation`: anything not in the allies map counts as an enemy.
- **Pathfinding:** occupied cells block unless the walker ignores that relation. Only hazards add path cost. There is no "passable if destroyed" notion. The checks live in `GridCell.CheckIfUnitWalkable`, `GridCell.IsWalkable`, `GridPluggableEntity.IsFootprintEmpty` and `IsFootprintWalkable`.
- **Masher:**
  - The counter only answers family hits, so a barrier never provokes it.
  - The plow treats an Unmovable unit or a walk-blocking planted object as a Blocker, so it refuses the step.
  - On its own turn it slams a hostile barrier like any enemy.
  - A barrier that is not Unmovable gets shoved.
  - "Breaks barriers easily" needs data (damage against the barrier's HP); nothing in the Masher code knows about barriers.
- **M3 is already laid out for barriers.**
  - The block's notes mark the necks 2,3 and 8,3 as "open in the greybox, no barrier".
  - These `M3DefenceTests` change on purpose once a barrier is added: `TheNecksAreOpenFloorAndTheGapsBesideThemHaveNoTile`, `TheTilesAndUnitsMatchThePaperBlock`, and `EnemiesAndTheNeutralStoneAreAlliesSoNoClawTargetsIt` (if Neutral turns hostile).
  - Stage 6 is `LivingUnitsLOCondition` ≤ 0: a barrier in the Enemy faction would block "Finish them".
- **AIRegressionTest:** a new `GUnit` prefab outside `Content/Levels/` adds `units.unexpected` and changes `units.count`. A planted hazard prefab doesn't touch the unit catalog. The test is Explicit and already out of date (the rocks aren't in it).

## 1. Destructible and blocking things today

**Rocks** (`Features/NPCs/Rock/Prefabs/Unit_Rock.prefab`):
- A variant of `Features/_Common/Prefabs/UnitBase.prefab`.
- Overrides: `title: Fallen Rock`, `resurrectable: 0`, faction Neutral, `visualizePlayabilityInTurn: 0`, tags `EntityState.Unmovable` + `EntityState.Unable to Swap`.
- HP comes from UnitBase's stat set; death goes HP min → `onMinReached` → `GUnit.Die`.
- `Unit_Rock_Stone0..3` are variants (title Stone, the Visual child shifted 0.1 per step; `MissionWiring.HoldTheYard.Stone.cs`).

**Can enemies target a rock?** Yes, where Enemy–Neutral is hostile:
- `LevelFactionRelations.GetFactionsRelation` returns Ally only if the pair is in the allies map.
- `LevelBase.prefab` has Bergsons–Enemy Enemy, Bergsons–Neutral Ally, Enemy–Neutral Enemy, and Stranger Ally with all three.
- The Claw attack is `targetType: 2` (CellOccupant) with `targetFactionRelation: 2` (Enemy).
- M1 and M3 both flip Enemy–Neutral to Ally (`MakeEnemyAndNeutralAllies`). M1 also makes Neutral–Stranger Enemy, so that `GetFactionEnemies(Neutral)` has a map entry; without it you get a `KeyNotFoundException`.

**Toba's Wall** (`Toba_Ability_Wall` → `Toba_Ability_Wall_PrefabSpawner` → `Toba_Wall.prefab`):
- A `HazardEntity` with `Specs_Health` and an empty `onMinReached` (no death).
- `lifeTurns: 3`, `disallowWalk: 1`, `isTargetable: 0`, faction Bergsons, `passRelation` none.
- It blocks everyone's walk (`GridCell.IsWalkable` refuses `DisallowWalk`; passing only through `PlantedLetsPass`).

**Queen's charge:**
- `ignoreRelationOnWalk: -1`, Unconstrained, transporter `goShortestWhileWalkable: 1`.
- The AI's path estimate ignores the Wall.
- `AEffectTransporter` (around line 341) stops before a cell that fails `IsFootprintWalkable` and applies the end-tile effects to the blocked cell. The Wall survives.
- `BossGoblinQueen` has no wall logic.

**Cyclone:** a `CycloneEntity : OnGridEntity` that blocks walking. Heavy movers pass it through `IPlantedMoverPass` and can end on it through `IPlantedClearsOnEntry` (`GridCell.PlantedPass.cs`).

**Mushroom** (`Features/Hazards/MushroomExplosion/MushroomExplosion.prefab`):
- A `HazardEntity` with `onMinReached` → `PerformMainEffect`.
- `lifeTurns: 25`, `disallowWalk: 1`, `isTargetable: 1`, `movementCostModifier: 1`, faction Enemy.
- Family abilities reach it through the planted-target branches in `FactionControllerBase` (around 253, 588) and `GridManager.GetHoverableCellEntity`.

**Other:** `CP_Spawner` is an Enemy hazard with 10 HP. `Dom_Ability_Barrier*` is a stat buff, not an object. No `Destructible`, `Obstacle` or `Breakable` class exists.

## 2. AI movement and targeting

**Pipeline:**
- `AIController` (around 94-125): `PrepareUnitTurn` → worker → `AIUnitBrain.GetTurnAction` → `PerformAction`. A null action ends the turn.
- `AIFactionBrain.PrepareUnitTurn` takes the main-thread snapshots (`AIEndOfTurnDanger`, `GridLineOfFire`), then `AIStrategyPlanner.Plan` + `AIBlackboard.Update`.
- `AIUnitBrain.GatherAvailableActions` → `GenerateScoredTurnActions` → `GetAbilityCandidateTargets` → filters `RefusesEndingOn` / `RefusesBlockedShot` / `RefusesBlockedFiringSpot` → `EvaluateUtilityScore`. The best score wins if above `CANCEL_ACTION_UTILITY_SCORE_THRESHOLD = -100`.

**Targets:**
- CellOccupant keeps occupants whose relation matches the ability.
- CellPlantedEntity adds any cell with a `PlantedEntity`, with no `IsTargetable` and no relation check.
- Faction relation is the only gate. No tag makes a unit attackable or unattackable.

**Graphs:**
- Claw and Masher walk: `Generic_P_Walk_Melee_UtilityScoreEvaluator` (`DestinationAttractiveness`, `EnemyAttractivenessAtDestination`, `DestinationEnemyPresence`, `NearestEnemyToSelfAtDestination`, `ForeseenPathQuality`, `MemorableOwnerProximity`, `Cooldown`, one Tag node).
- Claw attack: `Generic_MeleeAttack_UtilityScoreEvaluator` (`Status.Taunted`, `TargetMemorableAttackFactor`, ...).
- Masher attack: `MasherGoblin_Attack_UtilityScoreEvaluator` (`DestinationEnemiesInBound`, `TargetMemorableAttackFactor`).

**The pull:**
- `AIStrategyPlanner.HandleLivingUnitsCondition` turns the objective faction's units into influence subjects.
- `AIBlackboard.AccumulateFromCell` spreads influence by BFS over all neighbours, ignoring blockers.
- `EnemyPresence` / `FindNearestEnemyTo` use plain distance over the factions that have a controller.

**No path to the family:**
- Walk candidates are only cells the PathWalkable BFS reaches (it never expands through blockers).
- The scores still point through the blocker, so the unit walks up against it.
- `ForeseenPathQuality` drops to 0.
- With nothing in range it idles or ends its turn.
- The only custom hook is `CustomEval` (`GameEntityMessage`, e.g. `BossGoblinQueen`).

**Factions:**
- A faction with no controller (no units at session start until `HiddenLevelUnits` calls `AddFactionControllerMidWay`) adds no presence.
- It can still be targeted.

## 3. Pathfinding

- **The pathfinder** is `GridActions.cs` `GridPathFinding.FindPath`: A* over `AdjacentCells`, Manhattan heuristic, step cost `GetCellCost()`, optional `avoidCell`. Also `FindAlternativePathsTo`, `CollectBudgetPaths`, `MovePathOverride`.
- **Walkability per neighbour:** the goal must be `IsFootprintEmpty` / `IsWalkable`; a path cell must be `IsFootprintWalkable` / `CheckIfUnitWalkable`. Both can be switched off with the not-walkable-allowed flags.
- **`CheckIfUnitWalkable`:** an occupant blocks unless `ignoreRelation` covers the relation. A planted blocker blocks unless `PlantedLetsPass`.
- **Who passes what:** Claw, Masher and family walks use `ignoreRelationOnWalk: 1` (Ally): they pass allies and can't stop on them.
- **Cost:** `GetCellCost()` is `1 + hazard.MovementCostModifier` for a hazard, else 1. There is no breakable cost. The helpers are safe on the AI worker thread.

## 4. Masher

- **Counter** (`MasherGoblinFactionRoleHandler.Counter.cs`, `MasherCounterRules.Classify`): it ignores anything not from the player faction, and Cyclone Whirls. It answers with one step (`TryPlanAnswer`) and then a slam on the provoker's tile.
- **Plow** (`.Plow.cs`, `MasherPlowRules`, `MasherPlowGrid`):
  - It looks at the four cardinal one-cell steps whose cell isn't `IsFootprintEmpty`.
  - Blocker: no cell, a stash, a planted `DisallowWalk`, a non-unit occupant, a multi-cell unit, or a unit that fails `CanBePushed` (`plowPushableTagQuery` excludes Unmovable).
  - `Plan` returns `Blocked` / `DestinationBlocked`; there are no chain pushes.
- **Cyclone:** for a heavy enemy of the caster it counts as empty, so it's an ordinary walk cell.
- **Stones:** Unmovable, so Blocker. Under Enemy–Neutral Ally the Masher's walk may pass a stone cell but can't stop on it.
- **A barrier in its path:**
  - Unmovable `GUnit`: the plow refuses; the AI turn slams it if it is hostile (the AoE counts it).
  - Not Unmovable: shoved.
  - Planted `DisallowWalk`: Blocker, and not targetable with the current attack data.
  - "Easily" breaking it is data (damage vs HP, or a tag-gated modifier).

## 5. `GB_m3-defence`

- **Files:** `Content/Levels/Greybox/GB_m3-defence.prefab`; wiring `Features/Onboarding/Editor/MissionWiring.HoldTheYard.cs` (+ `.Stone`, `.Sequences`, `.Mission`); menus `Tools/Onboarding/Hold the Yard: Build Level` / `Apply Wiring`; tests `M3DefenceTests.cs`.
- **Waves:**
  - Hidden groups, all Dark Claws at factor 0.8: `w1` (0,0 1,0), `w2` (10,0 9,0 10,1), `w3` (0,2 10,2).
  - Revealed by `RevealUnitsSequence` inside `Arrival(...)`: w1 at the end of the push stage, w2 and w3 at the ends of hold stages 1 and 2 (`BuildNotchWithWave`).
  - `HiddenLevelUnits` (around 120-136) plugs the unit, adds a controller mid-way and registers the unit.
  - Six stages; stage 6 is living units ≤ 0.
- **The stone:**
  - Four Neutral rock variants on 5,8, each in its own hidden group `stone0..3`. A notch is Hide current + Reveal next. The outro hides the last one and reveals `toba`.
  - Turn order: family, Enemy, Neutral. Enemy–Neutral is overridden to Ally; Stranger is Ally with all.
- **Barrier-like:**
  - Nothing is built. `NeckTiles = {2,3},{8,3}`. `GapTiles = {1,3},{9,3}` have no tile.
  - The mushrooms at 1,1 and 9,1 block the lane mouths.
- **Design inputs from earlier:** 20 HP (about four Claw hits); targeted only when blocked; family attacks don't hurt it (T-7).

## 6. Core systems (`tech/core-systems.md`)

- **Listed:**
  - AI: `AIUnitBrain` (+ partials), `AIFactionBrain`, `AIBlackboard`.
  - Grid: `GridCell`, `GridCell.PlantedPass`, `GridManager`, `GridActions` (`GridPathFinding`), `GridPluggableEntity`.
  - Entities: `SpawnableEntity`, `OnGridEntity`, `HazardEntity`.
  - Effects: `AEffectTransporter`, `AEffectPusher`, `AEffectSpawner`.
  - Units, level and relations: `GUnit`, `CombatLevel`, `LevelFactionRelations`.
  - Controllers and messages: `FactionControllerBase`, `AIController`, `GameEntityMessage`.
  - Masher: `MasherGoblinFactionRoleHandler` (+ `.Counter`; `.Plow` is the same class), `MasherCounterRules`, `MasherCounterQueue`.
  - Damage and death: `UnitBase.prefab`'s death wiring.
- **Not listed:**
  - AI and grid support: `AIStrategyPlanner`, `UtilityVariables`, `UtilityScoreEvaluator`, `GridEnums`, `FactionsEnums`, `Constants`.
  - Masher and Queen: `MasherPlowRules`, `MasherPlowGrid`, `BossGoblinQueen`.
  - Features: Cyclone files, the Onboarding wiring and tests, `HiddenLevelUnits`.

## 7. AIRegressionTest

- **What it is:** `Core/Systems/AISystem/Editor/AIRegressionTest.cs` `Baseline_MatchesCurrentAI`, Explicit. A golden master over catalogs written into the file:
  - intent condition types;
  - `UtilityVariable` enum (exact, in order);
  - every evaluator graph (sha1, nodes, edges);
  - every `AbilityPreset`;
  - every `GUnit` prefab outside `/Content/Levels/` with its abilities;
  - custom-eval hosts (existence only);
  - a stress pass.
- **What changes the baseline:**
  - a new `GUnit` prefab outside `Content/Levels/` (`units.unexpected` + `units.count`);
  - a new ability (`abilities.unexpected`);
  - a new or edited graph;
  - a new variable;
  - a new condition type.
- **What doesn't:** a planted hazard with no `GUnit`.
- **Already stale:** the rocks aren't in it. `IsLevelPrefab` (mentioned in `tech/ai-regression-test-triage.md`) isn't on `main`.

## Smallest viable barrier design, as the code suggests

**A. Neutral `GUnit` barrier, relations alone (no code).**
- **What:** `Unit_Barrier` as a variant of `Unit_Rock` (Unmovable, Unable to Swap, ~20 HP by factor, Neutral). In M3, Enemy–Neutral goes back to Enemy.
- **What you get:**
  - Claws and the Masher can't pass the necks and can attack the barrier.
  - The family walks through it and doesn't target it with Enemy-only abilities.
  - The Masher's AoE counts it, and the plow treats it as a Blocker.
  - Its death replans the AI.
- **Costs:**
  - The stone becomes a target too. Move it to another faction, with a relation entry so `GetFactionEnemies` doesn't throw.
  - The barrier attracts and gets targeted whenever scoring likes it, not only when the enemy is blocked.
  - The M3 wiring and tests need rewiring.
  - The regression unit catalog gets an entry.
- **Core impact:** none.

**B. A + feature-side "taunt when blocked".**
- **What:** a barrier component at the enemy turn start (main thread). It finds enemies with no `FindPath` to the family but with one when the barrier counts as free (or that stand next to it) and calls `GUnit.TauntByAbility(barrierAbility)`. `MemorableOwnerProximity` / `TargetMemorableAttackFactor` then pull those units onto the barrier.
- **Costs:**
  - `MemorableAttacksMemory` holds one entry, so this overwrites John's taunt.
  - The taunt tag wakes Unaware units (`EnemyAlertTracker.IsTauntTag`).
  - The barrier needs an ability for `RememberAttack`.
  - A's pull stays.
- **Core impact:** none if `TauntByAbility` / `FindPath` are used as they are. A review should confirm they're safe at turn start.

**C. Core AI rule (Tier 3).**
- **What:** a barrier tag (e.g. `EntityState.Barrier`).
  - `AIUnitBrain.GetAbilityCandidateTargets` (CellOccupant) drops barrier targets unless the unit is "blocked".
  - "Blocked" is a per-job main-thread snapshot on `AIBlackboard` (like `AIEndOfTurnDanger` / `AILineOfFire`): no path to any plan subject, but one when barrier cells count as free.
  - Optionally, exclude barriers from `EnemyPresence` / `FindNearestEnemyTo`, so they never attract unblocked units.
  - "Passable if destroyed" adds a `FindPath` overload with a set of cells treated as free, beside `avoidCell`.
- **Works with:** A's `GUnit` data. A planted `HazardEntity` barrier would also need `CellPlantedEntity` on enemy attacks, plus an `IsTargetable` and relation guard in the planted branch, which today accepts any planted entity (mushrooms, the Cyclone).
- **Core impact:** `AIUnitBrain` (+ a partial), `AIBlackboard`, `AIFactionBrain`, and `GridActions` only for the overload. Catalogs are unchanged unless variables, graphs or abilities change.
