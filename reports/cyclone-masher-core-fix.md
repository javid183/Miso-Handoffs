# Report: a heavy enemy may end its walk on the Cyclone (core fix for cyclone-masher-blocked)

Plan: bug `cyclone-masher-blocked` (status.md), root cause `reports/cyclone-masher-fix.md` (Option A), approved by THJ as Tier 3 (D-571, D-572); round 2 context `plans/2026-11-17-cyclone-round2-tech.md` C3a to C3c    Agent: miso-implementer    Branch: thj/cyclone
Outcome: done. Compile clean; EditMode 2173 run, 2172 passed, 1 failed (the known red, inner count 43).

## Starting point: what my predecessor left, and what I did with it

A stopped run had left partial edits. I checked each one against the approved scope:

| File | Predecessor's edit | Decision |
| --- | --- | --- |
| `GridCell.PlantedPass.cs` (core) | `IPlantedClearsOnEntry` + `PlantedClearsFor(mover)` | **Kept** as written (the approved shape) |
| `GridPluggableEntity.cs` (core) | one condition in `IsFootprintEmpty` | **Kept** (the approved line) |
| `AEffectTransporter.cs` (core) | read-only `MoveMode` getter | **Kept**: needed by the AI filter below |
| `AIUnitBrain.cs` (core, AI) | candidate filter calls `CanEndMoveOn` | **Kept** |
| `AIUnitBrain.Landing.cs` (new, core, AI) | refused only Jump/Teleport transporters | **Fixed**: now allows the clearing blocker only for a Walk transporter (also covers non-move cell abilities) |
| `CycloneEntity.ClearsOnEntry.cs` (new, Cyclone partial) | heavy enemy of the caster, Cyclone alive | **Kept** (see Decisions: no `!HasBurst`) |
| `MasherCounterCycloneTests.cs` | `Ignore` already removed | **Kept** |
| `CycloneHeavyPassTests.cs`, `CycloneAIHeavyTests.cs` | old "can't stop on it" asserts flipped for heavies, kept for others | **Kept** |
| `CycloneHeavyEndsOnItTests.cs` (new) | 11 tests | **Kept**, 2 tests added |

Nothing was reverted.

## What changed

Core (marked **core**; all additive, no signature removed or changed except one private helper):

- **`Core/Systems/GridSystem/Runtime/GridCell.PlantedPass.cs`** (core, Grid): new interface `IPlantedClearsOnEntry { bool ClearsOnEntry(GridPluggableEntity mover); }` and public `GridCell.PlantedClearsFor(mover)`. It is true when the cell is free except for a planted entity that clears out for this mover. Reads plain fields and does `ReferenceEquals` checks only, so it is safe on the worker thread. Why: the approved hook.
- **`Core/Systems/GridSystem/Runtime/GridPluggableEntity.cs`** (core, Grid): `IsFootprintEmpty` now reads `if (!c.IsWalkable && !c.PlantedClearsFor(this)) return false;`. Why: the approved single stop rule.
- **`Core/Systems/GridSystem/Runtime/GridCell.cs`** (core, Grid; **beyond the suggested shape, needed**): the private `PassesEmptyFilter` now takes the walkability mode. For `SelfWalkable` it also requires `!FootprintHasWalkBlocker`. Why: `SelfWalkable` ranges are landings that don't walk in (jumps, teleports, summons). Without this, **Mountain Deev** (3x2, Unmovable, an enemy) could use its `SelfWalkable` Surrounding summon to place a light goblin on the Cyclone's cell, because the summon range is checked with the Deev's own footprint. The goblin would stand on the Cyclone without bursting it. For any cell without a clearing blocker the result is the same as before.
- **`Core/Systems/AbilitySystem/Abilities/Runtime/AreaShapeDefinition.cs`** (core, Area shapes; **beyond the suggested shape, needed**): the same `SelfWalkable` guard for shape-based ranges. Why: same reason, for shape-based target selection.
- **`Core/Systems/AbilitySystem/Effects/Runtime/AEffectTransporter.cs`** (core, Effects): read-only `public AbilityMovementMode MoveMode => moveMode;`. Why: the AI needs to know whether a move ability walks.
- **`Core/Systems/AISystem/Runtime/AIUnitBrain.cs`** (core, AI): in the Cell candidate filter, `_unit.IsFootprintEmpty(c)` is replaced by `CanEndMoveOn(ability, c)` (1 line).
- **`Core/Systems/AISystem/Runtime/AIUnitBrain.Landing.cs`** (+ `.meta`, new partial, core, AI, LF): `CanEndMoveOn = IsFootprintEmpty && (WalksThere(ability) || !FootprintHasWalkBlocker)`. `WalksThere` means the ability has a top-level Walk transporter, the same top-level scan `HasTransporter` uses. Why this is necessary: the **Goblin Queen's Jump uses a `PathWalkable` range** (`cellApplyWalkabilityMode: 1`, no ranged reach). Its range therefore goes through the walk BFS and would now offer the Cyclone cell; this filter keeps the AI from choosing it. For abilities without a clearing blocker on the board the result is the same as before.

Cyclone (not core):

- `Features/Player/Lucy/Scripts/Cyclone/CycloneEntity.ClearsOnEntry.cs` (+ `.meta`, new partial): `CycloneEntity : IPlantedClearsOnEntry`. It returns true only when the Cyclone is alive, the mover is a live `GUnit`, an enemy of the caster by the level relation, and heavy by `CycloneHeavy.IsHeavy(unit, pullTagQuery)`. Reads plain fields and references only. The round 3 presenter files were not touched.

Tests:

- `Features/Enemy/Masher Goblin/Editor/MasherCounterCycloneTests.cs` (+ `.meta`, new): repro with THJ's cells (Linda [8,-1], Cyclone [10,-2], Masher 2x2 SPD 1 at [11,-2], real prefab and walk). The counter step is onto the Cyclone; the no-Cyclone control picks the same step. Both green.
- `Features/Player/Lucy/Scripts/Editor/CycloneHeavyEndsOnItTests.cs` (+ `.meta`, new), 13 tests:
  - A heavy walks onto the Cyclone, bursts it once, ends plugged on the cell, and the Cyclone is gone.
  - A 2x2 heavy ends with its footprint over the Cyclone.
  - A bursting Cyclone still clears for a heavy but bursts no more.
  - Only a heavy enemy of the caster may end there: a light enemy, the family (even Immovable), an allied large unit, null, or an occupied cell may not.
  - A gone Cyclone and a rock clear for nobody.
  - Ranged reach and `FootprintHasWalkBlocker` still refuse the cell.
  - The dash approach cell is never the Cyclone.
  - The Mark-Linda duo loser stop is never the Cyclone.
  - The Queen's walk candidates include the cell; her jump candidates never land on it (real Queen prefab, real abilities, the brain's own filter).
  - The Queen's charge (the real charge transporter is a Walk) ends on the Cyclone and bursts it once.
  - Worker-thread read of the stop rule.
  - **Added by me:** `ASelfWalkableRange_ForAHeavyEnemy_NeverOffersTheCyclone_TheWalkRangeDoes` (BFS and straight `SelfWalkable` refuse the cell; `PathWalkable` offers it).
  - **Added by me:** `ASelfWalkableAreaShape_ForAHeavyEnemy_LeavesOutTheCyclone`.
- `Features/Player/Lucy/Scripts/Editor/CycloneHeavyPassTests.cs` (modified): a heavy enemy may end on the cell (move range now includes it, path to it exists). Light enemies, other planted blockers and the family keep their "can't end on it" asserts. The prefab implements `IPlantedClearsOnEntry`.
- `Features/Player/Lucy/Scripts/Editor/CycloneAIHeavyTests.cs` (modified): the heavy's move range contains the Cyclone cell; a light enemy's does not.

Doc: `claude-handoff/tech/core-systems.md`, round 2 Grid note: the heavy walk exception now says heavy enemies may end on the cell, and lists the hook and the guards.

## Every caller of `IsFootprintEmpty`, decided

| Caller | Kind | Decision |
| --- | --- | --- |
| `GridActions.cs:66, 241` `FindPath` goal (with mover) | walk | Accepts the cell for heavies (wanted) |
| `GridCell.cs` BFS / straight final filter, `PathWalkable` | walk range | Accepts (wanted: Masher walk range, AI live range, Queen walk/charge) |
| `GridCell.cs` same filter, `SelfWalkable` | landing | **Guarded** (new `FootprintHasWalkBlocker` check) |
| `GridCell.cs:889` ranged reach | landing | Already guarded by `FootprintHasWalkBlocker` |
| `AreaShapeDefinition.cs:149` `SelfWalkable` | landing / summon | **Guarded** |
| `AEffectTransporter.cs:341` walk last step | walk | Accepts (the walk ends on the cell and bursts it) |
| `AEffectCommand.cs:185` commanded walk last step | walk | Accepts: a commanded heavy enemy walks in, so it bursts the Cyclone (consistent with the rule) |
| `AEffectDashAttack.cs:91` approach cell | stop short | Already guarded |
| `UnitsCooperationHandler.cs:1309` Mark-Linda loser stop | stop short | Already guarded |
| `UnitsCooperationHandler.cs:956, 983` John-Linda mirror | family | Unaffected (family never clears) |
| `PlayerController.cs:1431` approach cell | family | Unaffected |
| `OnGridEntity.cs:171, 175, 211` self-moving hazards | not a `GUnit` | Unaffected (`ClearsOnEntry` needs a `GUnit`) |
| `MasherGoblinFactionRoleHandler.Counter.cs:514` planner | walk | Accepts (no Masher code change) |
| `MasherGoblinFactionRoleHandler.cs:84` hover preview | walk range | Accepts (shows the step) |
| `AIUnitBrain.cs` Cell candidate filter | AI | Via `CanEndMoveOn`: Walk transporters only |
| `Transporter` Jump/Teleport execution | landing | No check of its own; protected by the guards above (AI filter, `SelfWalkable` filters) |

## Acceptance criteria

- [x] Repro passes: the Masher steps onto the Cyclone toward Linda (`MasherCounterCycloneTests`). The control test stays green.
- [x] A heavy enemy can end on the cell, and the Cyclone bursts exactly once and is gone; the heavy ends plugged on the cell: `AHeavyEnemy_WalksOntoTheCyclone...`, `ALargeEnemy_Ends...`, `TheQueensCharge_...`.
- [x] Non-heavies are still refused, and so are the family and allies: `OnlyAHeavyEnemyOfTheCaster_MayEndOnIt`, `CycloneHeavyPassTests`.
- [x] Jump, dash approach and duo stop still refuse it: Queen jump candidates, dash test, duo test, and the two new `SelfWalkable` tests.
- [x] Walk range, pathfinding, Masher planner filter, walk last step, AI candidate filter for heavies and the Queen's charge: tests above plus `CycloneAIHeavyTests`.
- [x] Worker-thread safety: plain data and `ReferenceEquals` only; worker-thread test. AIRegression inner count is still **43** (test not touched).
- [x] `tech/core-systems.md` updated.
- Needs THJ's play check: the Masher counter in `LevelE3-C1`, the Queen's charge and a normal heavy turn ending on the Cyclone (burst ring, log), and the Queen's jump never landing on it.

## Test run

- Subset (5 Cyclone/Masher fixtures): 54 / 54 passed.
- Full EditMode (MCP, editor open, not in Play): **2173 run, 2172 passed, 1 failed, 0 skipped**. The only failure is `AIRegressionTest.Baseline_MatchesCurrentAI`, `CHECKS: 714 FAILURES: 43`. No GridToLevel flake this run. Compile: no errors. The one console error ("Objects are trying to be loaded during a domain backup") is the known one tied to THJ's TMP font edit.

## Save reset

No.

## Decisions I made

- **No `!HasBurst` in `ClearsOnEntry`** (my predecessor's choice, kept). The brief said "alive and not yet burst". But a 2x2 heavy's walk can burst the Cyclone on one step and still cover it on its last step, while the 0.3 s ring keeps the Cyclone standing. With `!HasBurst`, the Transporter's last-step check would then stop the walk one cell short of its planned end. The burst itself still fires once (`HasBurst` guards it), and the Cyclone is disposed after the ring. The only difference is during the 0.3 s ring. Tier 2.
- **`SelfWalkable` guards in `GridCell.cs` and `AreaShapeDefinition.cs`**: two more core files than the suggested shape. Needed for Mountain Deev's summon (see above). For every board without a clearing blocker the result is identical. Tier 2, core.
- **AI filter rule "only a walk ends on it"** instead of "jumps and teleports don't". The same for moves, and also safe for non-move cell abilities used by heavies. Tier 2, core.
- Enemy is decided by the level faction relation to the caster, which also covers a heavy family or allied unit (never clears).
- A commanded heavy enemy (`AEffectCommand`) may end its walk on the Cyclone and burst it: it walks in, so the rule applies.

## Needs THJ

None beyond the play check. The scope was approved. Two core files were added (`GridCell.cs`, `AreaShapeDefinition.cs`); both only restore the old rule for `SelfWalkable` landings, flagged here.

## Docs to update

- `tech/core-systems.md`: done.
- GDD (designer): CR-58 and LU-7 ("a heavy enemy may step onto the Cyclone and end there; it bursts"); EN-2 and EN-6 (Masher, Queen). The ring-window detail is optional.
- `status.md` / build log (coordinator).

## Risks and loose ends

- With SPD 1 the Masher's counter step onto the Cyclone leaves it 2 cells from Linda: it bursts the Cyclone but does not slam on this answer (the test asserts this). THJ's "and attacks" holds only when the target is adjacent after the step.
- AI prediction (intent avatars) still uses the sim range without a mover (C3c loose end). Predicted heavy moves don't cross or end on the Cyclone, while live turns now can.
- `FootprintHasWalkBlocker` allocates a small list per call. Only `SelfWalkable` ranges and the AI cell filter call it newly; I saw no cost in the tests.
- `AEffectDashAttack` still paths without a mover (C3a note), unchanged.

## Proposed commits

Depends on the round 2 commits already in `main` of this branch (C3a's `IPlantedMoverPass` is committed). The round 3 Cyclone work in the tree is separate; none of these files belong to it.

1. `feat(grid): a planted walk blocker can let a given mover end its walk on its cell; landings that don't walk in still keep off it` (**core**, own commit; no behavior change until something implements the interface):
   - `miso/Assets/_Project/Core/Systems/GridSystem/Runtime/GridCell.PlantedPass.cs`
   - `miso/Assets/_Project/Core/Systems/GridSystem/Runtime/GridPluggableEntity.cs`
   - `miso/Assets/_Project/Core/Systems/GridSystem/Runtime/GridCell.cs`
   - `miso/Assets/_Project/Core/Systems/AbilitySystem/Abilities/Runtime/AreaShapeDefinition.cs`
   - `miso/Assets/_Project/Core/Systems/AbilitySystem/Effects/Runtime/AEffectTransporter.cs`
   - `miso/Assets/_Project/Core/Systems/AISystem/Runtime/AIUnitBrain.cs`
   - `miso/Assets/_Project/Core/Systems/AISystem/Runtime/AIUnitBrain.Landing.cs` + `.meta`
   (The AI part could be its own commit after the grid part, but it only makes sense with the hook; I'd keep them together.)
2. `feat(lucy): a heavy enemy may end its walk on the Cyclone, bursting it, so the Masher's counter can step onto it` (plain, depends on 1):
   - `miso/Assets/_Project/Features/Player/Lucy/Scripts/Cyclone/CycloneEntity.ClearsOnEntry.cs` + `.meta`
   - `miso/Assets/_Project/Features/Player/Lucy/Scripts/Editor/CycloneHeavyEndsOnItTests.cs` + `.meta`
   - `miso/Assets/_Project/Features/Player/Lucy/Scripts/Editor/CycloneHeavyPassTests.cs`
   - `miso/Assets/_Project/Features/Player/Lucy/Scripts/Editor/CycloneAIHeavyTests.cs`
   - `miso/Assets/_Project/Features/Enemy/Masher Goblin/Editor/MasherCounterCycloneTests.cs` + `.meta`

Check before staging: `CycloneHeavyPassTests.cs` and `CycloneAIHeavyTests.cs` show only this fix's hunks in `git diff` (confirmed today; no round 3 hunks in them).

## Other branches

None (Cyclone lives on `thj/cyclone`; the core hook is additive and goes with the branch merge).

## How to see it

1. Test Runner, EditMode: run `MasherCounterCycloneTests` (2), `CycloneHeavyEndsOnItTests` (13), `CycloneHeavyPassTests`, `CycloneAIHeavyTests`: all green. Then Run All: only `AIRegressionTest.Baseline_MatchesCurrentAI` red (inner 43).
2. Play `LevelE3-C1` with Lucy and Linda. Cast the Cyclone at [10,-2] with the Masher at [12,-2], then shoot the Masher with Linda from [8,-1] (it is pushed to [11,-2]). On its counter the Masher steps onto the Cyclone: the burst ring plays, the Masher and any enemy beside it take the hit, the Cyclone is gone, and the Masher stands on that cell. The log reads "Burst · Lucy: hit N".
3. A Claw next to a Cyclone still stops in front of it. The family still walks through without stopping on it.
4. Goblin Queen: her walk or charge may end over the Cyclone and burst it; her jump never lands on it.

## Fix round (after review `reports/cyclone-masher-core-fix-review.md`)

Agent: miso-implementer. Outcome: done, all four items. Compile clean (warnings only, pre-existing). EditMode full run (MCP job `40820dde44f54293b33ca8614d86093a`): **2174 run, 2173 passed, 1 failed**, the known `AIRegressionTest.Baseline_MatchesCurrentAI` (`CHECKS: 714 FAILURES: 43`). No GridToLevel flake. Subset job `c6aebd8eb56d43318b4e9d9cf25e4a33` (the four Cyclone/Masher fixtures): 39/39.

### What changed

1. **Must fix: the landing guard blocks only the new allowance.**
   - `GridCell.PlantedPass.cs` (**core**, Grid): new `public static bool FootprintEndsOnClearing(GridCell origin, GridPluggableEntity source, List<GridCell> buffer = null)`. True only when a footprint cell that the source neither occupies nor is planted on has `!IsWalkable && PlantedClearsFor(source)`. A 1x1 footprint never allocates; multi-cell footprints use `buffer` when given. Plain fields and `ReferenceEquals` only (worker-safe). The `IPlantedClearsOnEntry` comment now names it.
   - `GridCell.cs` `PassesEmptyFilter`, `AreaShapeDefinition.cs` `PassesWalkability` (SelfWalkable), `AIUnitBrain.Landing.cs`: `!FootprintHasWalkBlocker(...)` replaced by `!FootprintEndsOnClearing(...)`. Since `PlantedClearsFor` is false wherever nothing implements `IPlantedClearsOnEntry`, every such board answers exactly as before the core fix; a live Cyclone that clears for the heavy is still refused to jumps, summons and teleports.
   - Dash approach, Mark-Linda loser stop and ranged reach keep `FootprintHasWalkBlocker` (unchanged, they were like that before the core fix).
2. **Should fix 1: ring-time test.** `ABurstingCyclone_StillLetsAHeavyEndOnIt_ButBurstsNoMore` now bursts with a 2x2 "Burster" standing at (6,0), off the Cyclone's cell; "Other" (2x2 at (0,0)) is checked at origin (3,0), which covers the Cyclone. During the ring it asserts `cell.PlantedClearsFor(other)` and `other.IsFootprintEmpty(origin)`; after the ring it asserts the Cyclone is gone, `ClearsOnEntry(other)` and `PlantedClearsFor(other)` are false and the cell holds no planted entity.
3. **Should fix 2: AI loop.** `AIUnitBrain.cs` computes `walksThere = checkFootprint && WalksThere(ability)` once before the Cell candidate loop and calls the new `CanEndOn(cell, walksThere)`. `AIUnitBrain.Landing.cs` keeps `CanEndMoveOn(ability, cell)` as a thin wrapper (the tests reflect on it) and passes a per-brain reusable `_landingCells` buffer to `FootprintEndsOnClearing` (instance field, not static, so no reset hook needed; same pattern as `_filteredCells`).
4. `claude-handoff/tech/core-systems.md`, round 2 Grid note: the guard wording now names `FootprintEndsOnClearing`, what it checks, and the AI's once-per-ability `WalksThere` and reused buffer.

New test `AUnitOnAnotherPlantedWalkBlocker_KeepsItsOwnCells_ForLandingsThatDontWalkIn` (in `CycloneHeavyEndsOnItTests.cs`, no Cyclone on the board): a 1x1 goblin standing on a rock (`DisallowWalk` planted) keeps its cell in a `SelfWalkable` `includeSelf` range; the real Goblin Queen with a rock under her origin keeps both her cells in that range, and `CanEndMoveOn(GoblinQueen_Ability_Jump, origin)` is true.

### Checked that the tests catch the bug

Temporarily (reverted, not in the tree): `FootprintEndsOnClearing` returning `FootprintHasWalkBlocker` (the old guard) and `ClearsOnEntry` refusing once `HasBurst`. Results: the ring test failed at "still clears out while its ring plays"; the new rock test failed on all three parts (goblin cell missing from the range, the Queen's rock cell missing, `CanEndMoveOn` false for the jump). Both green again after the revert.

### Files changed in this round

- `miso/Assets/_Project/Core/Systems/GridSystem/Runtime/GridCell.PlantedPass.cs` (core; BOM, LF kept)
- `miso/Assets/_Project/Core/Systems/GridSystem/Runtime/GridCell.cs` (core; BOM, LF kept)
- `miso/Assets/_Project/Core/Systems/AbilitySystem/Abilities/Runtime/AreaShapeDefinition.cs` (core)
- `miso/Assets/_Project/Core/Systems/AISystem/Runtime/AIUnitBrain.cs` (core, AI)
- `miso/Assets/_Project/Core/Systems/AISystem/Runtime/AIUnitBrain.Landing.cs` (core, AI; new, LF)
- `miso/Assets/_Project/Features/Player/Lucy/Scripts/Editor/CycloneHeavyEndsOnItTests.cs` (new; now 14 tests)
- `claude-handoff/tech/core-systems.md` (doc)

`CycloneEntity.ClearsOnEntry.cs` was edited only for the temporary check and is back to its reviewed text. The proposed commits above are unchanged: the four core files and `AIUnitBrain.Landing.cs` go in commit 1, the test file in commit 2.

### Decisions I made

- **"False after" for `IsFootprintEmpty` in the ring test:** once the ring ends the Cyclone is disposed and its cell is plain, so `IsFootprintEmpty(origin)` is correctly **true** after the ring. I assert the parts that do turn false (`ClearsOnEntry`, `PlantedClearsFor`) plus "no planted entity left" instead. Same intent: the allowance lasts exactly as long as the Cyclone stands.
- The new rock test lives in the Cyclone test file to reuse its grid, factions and Queen helpers; its name and comment describe the general rule, not the Cyclone.
- `CanEndOn(cell, walksThere)` is a separate name instead of a `CanEndMoveOn` overload, so tests that reflect on `CanEndMoveOn` by name aren't made ambiguous.

### Risks and loose ends

- `IsFootprintEmpty` (pre-existing, unchanged) still allocates a list and uses Unity `==` per call in the AI loop; the new check adds no allocation on top of it.
- Earlier loose ends stand (AI intent prediction without a mover; dash pathing without a mover).
- Needs THJ's play check as before. Save reset: no.
