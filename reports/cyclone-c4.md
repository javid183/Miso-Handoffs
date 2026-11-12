# Report: Cyclone redesign, C4 (enemy ranged attacks blocked by the Cyclone)

Plan: plans/2026-11-11-cyclone-redesign-tech.md    Agent: miso-implementer (opus)    Branch: thj/cyclone
Outcome: done (THJ play check pending). Core touches as approved (D-533): the AI candidate loop and intent, the `AEffectSpawner` execution check; plus one new additive core file, `GridLineOfFire.cs` in `GridSystem/` (flagged below).

## Fix round (after the C4 review)

Review: `reports/cyclone-c4-review.md` (APPROVE, three should-fixes).

1. **The firing-spot filter keeps cells where something else has a target.**
   - `RefusesBlockedFiringSpot` now asks `AnythingElseToDoFrom`: any ability other than a shot that is still usable after the move.
     - A melee attack needs an enemy in reach.
     - A heal, buff or summon needs a valid target in its range.
     - An ability aimed at the area around the unit always has one.
   - The target match is the new pure `AILineOfFire.HasValidTarget(rangeCells, targetType, relation, unit)`. It is a light version of the candidate-target rule; `GetAbilityCandidateTargets` can't be reused because its buffers are in use while candidates are scored.
   - `AnyUsableAttackAfterMove` gains `attacksOnly` (default true, so C2's dangerous-ground check is unchanged).
   - `CanAttackAfterMovingTo` loses the now-unused `includeShots`.
   - `RefusesFiringSpot`'s predicate is renamed `anythingElseFromThere`.
   - So the Dark Shaman still walks to heal or summon: the summon is aimed at the area around it, so it keeps every destination while it is off cooldown.
   - Test: `AI_HasValidTarget_KeepsCellsWhereAHealOrSummonHasATarget`:
     - a heal on an ally in range: kept;
     - only an enemy in range: not kept;
     - never itself;
     - an empty cell for a cell-targeted summon: kept;
     - an occupied cell for a cell target: not kept.
   - The existing `RefusesFiringSpot` test covers the "something else is left" keep.
2. **`IsProjectileShot`** reads `EffectSetLevel?.GetEffects(Preset.BaseEffectSetLevels)`, so a level that only updates parameters counts the base level's effects. No enemy has upgrade levels today, so no test changed.
3. **Worker cost.**
   - All three brain hooks first call `LineOfFireApplies()`. It is false at once when the board has no blockers, or when the unit has no projectile ability.
   - The "has a shot" scan runs once per AI job: the key is the blocker set the faction brain hands the blackboard per job. It is an instance field on the brain, not a static.
   - The firing-spot buffers (spot footprint, enemy list, a footprint pool, the seen set) are reused instead of allocated per destination.
4. **Backing off out of range:** not changed. Preferring a clear-line cell over a cell out of range needs a pre-pass over all of a move's destinations (or a score nudge, which is AI content), so it isn't a tiny change. Without care it would also change how unblocked archers pick cells. Left as a **play check**: a blocked Archer with a reachable clear-line cell should take it rather than retreat.

Files touched in this round:
- `Core/Systems/AISystem/Runtime/AIUnitBrain.LineOfFire.cs`, `AIUnitBrain.EndOfTurnDanger.cs`, `AILineOfFire.cs`
- `Core/Systems/AbilitySystem/Effects/Runtime/AEffectSpawner.cs`
- `Features/Player/Lucy/Scripts/Editor/CycloneLineOfFireTests.cs` (now 20 cases)

Line endings and BOMs are kept. The commit order is unchanged.

**EditMode after the fix round:** 2010 run, 2009 passed. The only failure is the known red `AIRegressionTest.Baseline_MatchesCurrentAI`: 714 checks, still **43** inner failures, not re-baselined. Compile clean.

The sections below describe the first build; where the fix round changed something, the fix round wins.

## What changed

Paths under `miso/Assets/_Project/`. All files LF. New core files follow their siblings: `GridLineOfFire.cs` and `AILineOfFire.cs` have a BOM, `AIUnitBrain.LineOfFire.cs` has none (like `AIUnitBrain.cs`). Edited files keep theirs (`AEffectSpawner.cs`, `AIBlackboard.cs`, `AIFactionBrain.cs` BOM; the others none). Metas made by Unity.

### Core
- `Core/Systems/GridSystem/Runtime/GridLineOfFire.cs` (+ .meta, new, **core folder, additive**):
  - interface `ILineOfFireBlocker.CollectLineOfFireBlockers(Faction shooterFaction, ICollection<Vector2Int>)`.
  - static `GridLineOfFire`: `Snapshot(faction)` (main thread; scans planted entities for the interface, like `AIEndOfTurnDanger.Snapshot`), and pure `CellsBetween`, `Crosses`, `IsBlocked(shooterFootprint, targetFootprint, blockers)`, `FootprintOf`, `FootprintAt`, `TargetFootprintOf`. Plain values and `ReferenceEquals` only; no statics.
- `Core/Systems/AbilitySystem/Effects/Runtime/AEffectSpawner.cs` (**core, approved**):
  - new `public static bool IsProjectileShot(RuntimeAbility)`: the ranged detection (below). Worker-safe.
  - `CheckTargetSelectionCondition`: for a projectile, refuses when the owner's faction has blockers on the board and the grid line is blocked; then the existing `ClearPathRequired` physics check as before. Non-projectile spawners (the Cyclone cast, area warnings, hazards, summons) are untouched.
- `Core/Systems/AISystem/Runtime/AILineOfFire.cs` (+ .meta, new, **core**): the two pure keep-or-drop decisions the unit brain calls: `RefusesShot(ability, shooterFootprint, target, blockers)` and `RefusesFiringSpot(spotFootprint, enemiesInShotReach, blockers, otherAttackFromThere)`.
- `Core/Systems/AISystem/Runtime/AIUnitBrain.LineOfFire.cs` (+ .meta, new partial, **core**): `RefusesBlockedShot`, `RefusesBlockedFiringSpot`, `ShotFromFootprintRefused`. AI log lines in the editor: "Skipped: the line of fire is blocked", "Skipped: every shot from there is blocked".
- `Core/Systems/AISystem/Runtime/AIUnitBrain.cs` (**core**): two lines in the `GenerateScoredTurnActions` target loop, after C2's `RefusesEndingOn`.
- `Core/Systems/AISystem/Runtime/AIUnitBrain.EndOfTurnDanger.cs` (**core**, C2 file): the "can attack after the move" check now counts a shot only when its line is clear (`HasEnemyIn` takes the ability and footprint), and the usable-attack loop is factored into `AnyUsableAttackAfterMove` so the firing-spot rule shares it. `CanAttackAfterMovingTo` gains `includeShots` (default true). Same behaviour when nothing blocks.
- `Core/Systems/AISystem/Runtime/AIBlackboard.cs` (**core**): `SetLineOfFireBlockers`, `HasLineOfFireBlockers`, `LineOfFireBlockers`, next to C2's danger set.
- `Core/Systems/AISystem/Runtime/AIFactionBrain.cs` (**core**): `PrepareUnitTurn` and `RequestPredictAllTargets` take `GridLineOfFire.Snapshot(_faction)` on the main thread beside the danger snapshot and set it on the blackboard at the start of the job; the unused sync `PredictNextTargets(GUnit)` snapshots both when called off the worker.

### Not core
- `Core/Interactions/Runtime/UnitThreatAnalysis.cs`: `CollectAttackReachFrom` (the one source of every attack-reach preview) leaves out, for a shot, every cell whose line from the unit's footprint at that origin is blocked. Blockers are read once per query (`ShotBlockersFor`, `ShotBlockersPerAttack`) and passed down through private overloads, so `GetAttackableCells` (Shift view), `GetThreateningEnemies` / `AttackReaches` (ghost threats) and `BasicAttackReachFrom` (hover) all follow without a grid scan per origin. Public signatures unchanged.
- `Features/Player/Lucy/Scripts/Cyclone/CycloneEntity.LineOfFire.cs` (+ .meta, new partial): the Cyclone implements `ILineOfFireBlocker`. It adds its cell for factions that are enemies of its owner's faction (the same relation as the Whirl and the cross danger), only while alive.
- `Features/Player/Lucy/Scripts/Editor/CycloneLineOfFireTests.cs` (+ .meta, new, 19 cases).

No new statics, so no `PlayModeStaticReset` hook: the snapshot travels with each AI job (blackboard instance), the target check and previews read the board live.

## The line choice

**A line through cell centres that blocks only on cells whose inside it passes through; touching a corner doesn't count.** Implemented as an exact integer grid walk that steps diagonally when the line passes exactly through a corner.

- Straight and diagonal shots: blocked by a Cyclone standing on them.
- Knight-move and shallow offset lines: blocked by any cell they run through (a knight move enters both middle cells).
- A diagonal that only grazes the Cyclone's corner passes, even between two blockers.
- The crossed cells are the same in both directions.

Why not the others:
- **Bresenham** picks one side at ties and isn't symmetric. An archer could shoot Linda while Linda's mirror shot would be "blocked", and which side counts depends on draw order. That reads as random.
- **Supercover** blocks on corner touches. A diagonal shot that visibly passes beside the Cyclone would be stopped, so the Cyclone would feel bigger than its tile.

The chosen rule reads as "the shot is stopped when its line goes through the Cyclone's tile".

**Adjacent:** never blocked (also diagonally), since no cell lies between neighbours. There is an explicit early-out for footprints.

**Large units:** a shot is allowed when any cell of the shooter's footprint has a clear line to any cell of the target's footprint (fire from any part, at any visible part). It is blocked only when every pair is crossed. This matches how range already works for large units (reach from every footprint cell, `OccupantIntersects`). A cell aimed at counts with its occupant's whole footprint; an empty cell is itself.

## The ranged detection

**A shot = an ability whose own top-level effects include an `AEffectSpawner` that spawns a `Projectile`** (`AEffectSpawner.IsProjectileShot`). Checked against the data:
- **Shots:** Archer attack (`ShootingArrow`) and Dark Shaman attack (`ShamanShootingProjectile`) are the only enemy projectile spawners.
- **Not shots:**
  - the Masher and Queen attacks spawn area warnings (`OnGridEntity`);
  - the Mountain Deev spawns a poison pool;
  - melee attacks (Claws) spawn nothing;
  - the Shaman heal is an attribute modifier.

Who is stopped is decided by the blocker, not the ability: the Cyclone stops shots fired by factions hostile to Lucy's. So family projectiles (Linda's arrows, Tempest Bloom copies) are never refused, and their physics split on the Cyclone is untouched. Only Cyclone cells block; rocks and other blockers don't implement the interface.

## Acceptance criteria (C4)

- [x] **The AI doesn't pick a blocked shot.**
  - `AIUnitBrain.GenerateScoredTurnActions` drops the candidate through `RefusesBlockedShot`, which calls `AILineOfFire.RefusesShot`.
  - The shooter's footprint comes from the live cell or the simulated origin; the target's footprint follows the occupant's live or simulated cell.
  - Test `AI_RefusesShot_OnlyForAShotWhoseLineIsBlocked`, through the same helper with the live Archer and Claw presets:
    - blocked behind the Cyclone;
    - clear beside it;
    - adjacent never blocked;
    - melee never refused;
    - the family's snapshot never blocks;
    - a different (simulated) origin with a clear line passes.
  - Test `AI_RefusesShot_ALargeTargetPartlyBehindTheCyclone_IsStillAShot`.
  - The brain's two-line hook itself is a **play check**. As in C2, EditMode can't build a full `AIUnitBrain` with abilities, AP and cooldowns.
- [x] **The intent prediction doesn't show it.** `PredictAllTargets` → `PredictNextTargets` → `GetTurnAction(sim)` → the same `GenerateScoredTurnActions` loop, with the blockers snapshotted in `RequestPredictAllTargets`. A refused shot is never chosen, so `CollectTargets` never lists its target. Evidence: by construction (same loop) plus the helper tests; the preview in a level is a **play check**.
- [x] **Execution refuses it for enemy-faction owners.** Tests:
  - `TargetCheck_RefusesAnEnemyShotAcrossTheCyclone_AndAllowsAClearOne`: the live Archer spawn effect, aimed at a unit and at a cell behind the Cyclone, refused; a line beside it allowed.
  - `TargetCheck_WithoutACycloneOrWithARock_IsUnchanged`.
  - The player's and AI's target selection both go through `RuntimeAbility.CheckTargetSelectionCondition` → this check (`FactionControllerBase` :267, :617). `AIController.PerformAction` already returns false on a refused target.
- [x] **A family shot is never refused:** `TargetCheck_AFamilyShotIsNeverRefused` (Linda's live primary arrow; and the Archer's projectile fired by a family unit).
- [x] **The threat preview doesn't show it:** `ThreatPreview_AnEnemyShotsReach_LeavesOutTheCellsBehindTheCyclone`. The Archer's real reach from its cell contains the cell behind the Cyclone before the cast and not after. The cell in front stays, and exactly the line-blocked cells are gone. The Shift view, the ghost threat count and hover reach use the same method; drawing them is a **play check**.
- [x] **Only Cyclone cells block; rocks unchanged:** `Snapshot_RocksAndOtherBlockersDontStopShots`, plus the rock case above.
- [x] **Who is stopped:** `Snapshot_TheCycloneStopsEnemyShotsOnly_AndOnlyWhileItIsOut` (enemy only; not family, ally, neutral; nothing once faded).
- [x] **The line rule:**
  - `Line_Straight_IsBlockedOnlyByACellOnIt`, `Line_Diagonal_RunsThroughTheDiagonalCellsOnly`, `Line_ThatOnlyGrazesACorner_IsNotBlocked`, `Line_KnightMoveAndOffset_RunThroughEveryCellTheyEnter`, `Line_IsTheSameInBothDirections`, `Line_AdjacentShooterAndTarget_AreNeverBlocked`.
  - Large units: `Line_LargeTarget_IsHitWhenAnyPartHasAClearLine`, `Line_LargeShooter_FiresFromAnyOfItsCells`, `Footprint_OfALargeUnit_CoversItsPlacementSize`.
- [x] **Ranged detection:** `Shots_AreProjectileAbilities_NotMeleeAreaWarningsOrMoves` (live Archer and Shaman attacks yes; Claw melee, Masher area warning, Archer walk, null no).
- [x] **Ranged enemies move to a cell whose line is clear.** It does **not** fall out by itself:
  - The Archer's walk graph (`Generic_P_Walk_Ranged`) scores enemy presence, attractiveness, cooldown and foreseen path. It knows nothing about attacks, so once its blocked shot is dropped it could walk to another blocked cell or stay.
  - Added: `RefusesBlockedFiringSpot`. A plain move destination is dropped when, after the move, a usable shot has enemies in reach but every one of them is behind a blocker, and no other attack (melee) is left from there.
  - Destinations with any clear shot, or with no enemy in reach (closing in), are kept. So the graph picks among cells with a clear line, or approaches.
  - Decision tested through `AI_RefusesFiringSpot_WhenEveryEnemyInReachIsBehindABlocker` (also that the melee check is asked only when every shot is blocked).
  - C2's "can attack from there" (walking onto the cross) now counts a shot only with a clear line. So an Archer no longer steps onto an arm for a shot the Cyclone blocks.
  - Repositioning in a level is a **play check**.

**EditMode suite:** 2009 run, 2008 passed (1990 before C4 + 19 new). The only failure is the known red `AIRegressionTest.Baseline_MatchesCurrentAI`: 714 checks, **43 inner failures, unchanged**, not re-baselined. C4 adds no utility variable, graph, ability or unit. Compile clean, no new warnings.

## Save reset

No.

## Decisions I made

- **The helper's home:** `GridSystem/` (a new file). `AEffectSpawner` (abilities), the AI and the threat preview (interactions) all use it, and `GridSystem` is the layer they share. The blocker is an interface, like C2's `IAIEndOfTurnDanger`, so core never references Lucy's code.
- **Blockers per shooter faction, decided by the blocker:** this gives "family projectiles unaffected" for free, with no faction special case in the spawner.
- **Any projectile fired by a blocked faction is stopped, whatever its target.** Today only the Archer and Shaman attacks are enemy projectiles, both aimed at enemies.
- **Firing-spot filter as a destination drop** (same style as C2's dangerous ground), not a utility variable or graph edit. That keeps AI content and the regression catalog untouched.
- **Execution check reads the board live** (grid scan) instead of a registry: no static, no reset hook. It runs on the main thread only. I checked every caller of `CheckTargetSelectionCondition`; the AI brain never calls it.
- **Threat preview filtered inside `CollectAttackReachFrom`:** it covers the Shift view, ghost threats and hover reach together. Family callers (`PlayerController` approach and range, role zones) see no change, because nothing blocks the family.

## Needs THJ

None. Flag only: `GridLineOfFire.cs` is a new additive file in the core `GridSystem/` folder. It has no callers outside the D-533 set plus the threat preview, and changes nothing when no blocker is on the board.

## Docs to update

- `tech/core-systems.md` (coordinator):
  - Grid row: `GridLineOfFire` / `ILineOfFireBlocker`, pure and worker-safe except `Snapshot`.
  - Effects row: `AEffectSpawner.IsProjectileShot`; a projectile's target check refuses a blocked line.
  - AI row: blocker snapshot per job (`AIBlackboard.LineOfFireBlockers`); `AILineOfFire.RefusesShot` / `RefusesFiringSpot` in `GenerateScoredTurnActions`; the cross-danger attack check counts clear shots only.
- `tech/combat-architecture.md` (coordinator): "line of fire" means any planted entity implementing `ILineOfFireBlocker`. Shots are projectile spawners, checked on the grid, not by physics.
- GDD `combat-rules.md`, `characters/lucy.md` (designer, C5): the line rule as built (centre to centre; corners don't block; adjacent never blocked; large units any part). Enemy shots only; family shots pass.
- AI regression fix session: C4 adds nothing to the catalog; count stays 43.

## Risks and loose ends

- **Play checks:**
  - an Archer behind the Cyclone doesn't shoot through it and repositions to a clear cell (or closes in);
  - the intent preview matches;
  - the Shift view and ghost threat count drop cells behind the Cyclone;
  - a diagonal shot past its corner still fires;
  - the Shaman the same;
  - Linda's arrows still split through it;
  - the AI log lines.
- An Archer whose every reachable cell is blocked (a corridor sealed by the Cyclone) drops all its moves and waits. That matches the "sealed off" behaviour in C2.
- An Archer already standing at a blocked spot moves only if its walk graph scores a kept destination above the cancel threshold. The filter only removes blocked destinations; it doesn't force a move. If it stays put in play, the next step would be a small score nudge, which is AI content.
- The firing-spot check uses the shot's range from the destination through the brain's own `GetAbilityRangeCells` (simulated path). Like C2, it ignores per-effect target conditions other than the line.
- The dead Linda-folder Cyclone copies don't implement the blocker (different class, unused).
- AI regression stays red at 43, unchanged.

## Proposed commits

C4 edits four files already in commit **B** (`AIUnitBrain.cs`, `AIUnitBrain.EndOfTurnDanger.cs`, `AIBlackboard.cs`, `AIFactionBrain.cs`), so with whole files B can't stay as it was. B's files now call into C4's helpers. Order that builds at every step:

**E1, A, A2, B (widened), D1, C1 1–8, C, D2, D3, E2, E3**

- **E1** (new, first; core, approved): `feat(core): enemy shots check a grid line of fire: a projectile can't be fired along a line that crosses a cell blocking the shooter's faction`.
  - Files: `Core/Systems/GridSystem/Runtime/GridLineOfFire.cs` (+ .meta), `Core/Systems/AbilitySystem/Effects/Runtime/AEffectSpawner.cs`.
  - Depends on nothing new, and is inert on its own: nothing implements `ILineOfFireBlocker` yet. It can also go right before B if you prefer.
- **A, A2:** as in `cyclone-c2.md`.
- **B** (widened; core, risky: AI behaviour):
  - Message: `feat(core): the AI keeps its units off ground that hurts them at turn end unless they can attack from there, never picks a shot whose line of fire is blocked, and moves ranged units to cells with a clear shot`.
  - Files: C2's set (`AIEndOfTurnDanger.cs` (+ .meta), `AIBlackboard.cs`, `AIFactionBrain.cs`, `AIUnitBrain.cs`, `AIUnitBrain.EndOfTurnDanger.cs` (+ .meta)), plus `Core/Systems/AISystem/Runtime/AILineOfFire.cs` (+ .meta) and `AIUnitBrain.LineOfFire.cs` (+ .meta).
  - Depends on E1. D-533 allows the line-of-fire AI part grouped with the AI core commit.
  - Split option: the two AI behaviours share `AIUnitBrain.cs` and `AIUnitBrain.EndOfTurnDanger.cs` whole, so they can't be split without partial staging.
- **D1, C1 1–8, C, D2, D3:** as in `cyclone-c3.md`. C1 commit 3 still takes the whole `Cyclone/` folder **except** `CycloneEntity.AIDanger.cs` (in C) **and `CycloneEntity.LineOfFire.cs`** (in E3).
- **E2** (plain): `feat(ui): threat previews leave out cells an enemy shot can't reach because its line of fire is blocked`.
  - Files: `Core/Interactions/Runtime/UnitThreatAnalysis.cs`.
  - Depends on E1. Inert until a blocker exists, so it can go anywhere after E1.
- **E3** (plain): `feat(lucy): the Cyclone stops enemy shots whose grid line crosses its cell; the family's arrows still pass`.
  - Files: `Features/Player/Lucy/Scripts/Cyclone/CycloneEntity.LineOfFire.cs` (+ .meta), `Features/Player/Lucy/Scripts/Editor/CycloneLineOfFireTests.cs` (+ .meta).
  - Depends on E1, B, E2, C1 3 (`CycloneEntity` partial) and the test helpers (`CycloneTestGrid` in C1 4, `CycloneTestFactions` in C).

Don't stage THJ's files (PreloadScreen, ProjectSettings, the TMP fallback font).

## Other branches

`thj/home-test` lacks the redesign; it merges later with the rest.

## How to see it

1. Open a level with Lucy, Linda and an Archer Goblin (or Dark Shaman) in a row or diagonal with open ground around.
2. Cast the Cyclone on a cell between the Archer and Linda, on the straight line between them.
3. Hold Shift (threat view) or hover the Archer: the cells behind the Cyclone, as seen from the Archer, aren't in its attack reach. Cells beside the line still are.
4. Hover the Archer for its intent before ending the turn: it doesn't target Linda through the Cyclone.
5. End the turn:
   - The Archer doesn't shoot through the Cyclone. It walks to a cell with a clear line and shoots, or closes in.
   - Tools > AI log viewer: "Skipped: the line of fire is blocked" on the blocked target, and "Skipped: every shot from there is blocked" on refused destinations.
6. Put Linda diagonally so the line only touches the Cyclone's corner: the Archer can shoot her.
7. Linda shoots through the Cyclone: her arrow passes (and splits with Tempest Bloom), as before.
