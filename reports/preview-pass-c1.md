# Report: Grid preview pass, C1 Shared attack reach (P3)

Plan: plans/2026-10-19-preview-pass-tech.md (chunk C1)    Agent: miso-implementer    Branch: thj/preview-improvements
Outcome: done (in-game checks are left for the C9 play check)

## What changed

- `miso/Assets/_Project/Core/Interactions/Runtime/UnitThreatAnalysis.cs` (LF, no BOM, not core): one attack-reach helper, `AttackReachFrom`, built from `PlayerController.ComputeAttackRangeFromOrigin`. `GetAttackableCells` (Shift) and `GetThreateningEnemies` (threat arcs) now use it. The old `AttackRangeFrom` is gone: it hard-coded `straight: false`, had no ranged reach and no faction. Added a ready-attack filter, an optional area-splash mode and an exact out-of-radius pre-check for threat arcs.
- `miso/Assets/_Project/Core/Interactions/Editor/AttackReachTests.cs` + `.meta` (new, UTF-8 BOM and LF, like `InputLockTests.cs`): 8 EditMode tests on a hand-built grid.
- Not touched: `PlayerController` (C2's job; its private `ComputeAttackRangeFromOrigin` still exists) and `ShowStatsHoverPreview` (it calls `GetAttackableCells(unit)`, which still compiles with the new default arguments).

## API (for C2, C5, C6 and C7)

All of it is in `MISO.Core.Interactions`, static and stateless (no caches, so no `PlayModeStaticReset` hook), main thread only.

```csharp
public readonly struct AttackReachSpec   // geometry inputs; From(ability) or built directly
{
    int Radius; GridCellTraverseMode TraverseMode; WalkabilityMode WalkabilityMode;
    bool Straight; bool IncludeSelf; bool AllowRangedReach; FactionsRelationType IgnoreRelationOnWalk;
    AttackReachSpec(int radius, GridCellTraverseMode traverseMode, WalkabilityMode walkabilityMode,
        bool straight, bool includeSelf, bool allowRangedReach, FactionsRelationType ignoreRelationOnWalk = 0);
    static AttackReachSpec From(RuntimeAbility ability);
}

public static class UnitThreatAnalysis
{
    // (a) reach from one cell
    List<GridCell> AttackReachFrom(GUnit unit, RuntimeAbility ability, GridCell origin);
    void CollectAttackReachFrom(GUnit unit, RuntimeAbility ability, GridCell origin, ISet<GridCell> into);
    List<GridCell> BasicAttackReachFrom(GUnit unit, GridCell origin);           // unit.DefaultOccupiedCellAbility
    bool AttackReaches(GUnit unit, RuntimeAbility ability, GridCell origin, GridCell target,
        HashSet<GridCell> scratch = null);                                      // with the radius pre-check
    void CollectReachFromFootprint(IReadOnlyList<GridCell> footprint, in AttackReachSpec spec,
        Faction requestFaction, ISet<GridCell> into);                           // pure geometry (tests)

    // (b) union over reachable cells of ready Attack abilities
    bool IsReadyAttack(RuntimeAbility ability, int cooldownTicksAhead = 0);     // Attack type, RemainingCooldown - ahead <= 0
    List<RuntimeAbility> GetReadyAttackAbilities(GUnit unit, int cooldownTicksAhead = 0);
    HashSet<GridCell> GetAttackableCells(GUnit unit, int cooldownTicksAhead = 0, bool includeAreaSplash = false);
    List<GUnit> GetThreateningEnemies(GridCell cell, Faction viewer, int cooldownTicksAhead = 0);

    List<GridCell> GetReachableCells(GUnit unit);                               // unchanged
}
```

- **C2:** the ghost icons use `BasicAttackReachFrom(ghostUnit, ghostCell)`. `AttackReachesFrom`/`ShowApproachAttackRange` use `AttackReachFrom(unit, PhaseData.ActiveAbility, origin)`. Note that the faction becomes the unit's own instead of the controller's `Faction`, as the plan asks.
- **C5:** a Bergson gets `BasicAttackReachFrom(unit, unit.CurrentCell)`. The enemy danger zone is `GetAttackableCells(enemy, ticksAhead, includeAreaSplash)`; both arguments are C5's choice (see Needs THJ / coordinator).
- **C6/C7:** `new HashSet<GridCell>(zoneCells).SetEquals(BasicAttackReachFrom(unit, cell))`. Alternatively, collect with `CollectAttackReachFrom` into a set. The pure equality function itself is C6's.

## Acceptance criteria

- [x] `AttackReachFrom(GUnit, RuntimeAbility, GridCell)` handles shape definitions (through `ComputeTargetSelectionCells(..., originOverride: origin)`), footprint, straight lines, ranged reach, the unit's own faction, `IncludeSelf` and `ignoreRelationOnWalk`. It never passes `source:` to `GetRangeCells`. Evidence: code; tests for straight, ranged reach and footprint.
- [x] `GetAttackableCells` and `GetThreateningEnemies` use it. Shield Dash is now straight lines, and ranged reach crosses gaps (tested at the geometry level). The AoE splash and every-attack logic are off by default, and C5 can get them back as `includeAreaSplash: true` over ready attacks. **In-game check of John under Shift and the enemy arcs: play check (C9).**
- [x] EditMode tests on a built test grid: a straight-only ability gives a cross, a missing cell stops plain straight reach but ranged reach crosses it, a 2x2 footprint origin (with and without IncludeSelf), the radius invariant the pre-check relies on, and the footprint exclusion never removes cells collected earlier. Not covered by tests: anything that needs a real `GUnit`/`RuntimeAbility` (`AttackSpec.From`, shape-definition abilities, the ready filter, `AttackReaches`' pre-check through a unit). The play check covers those.
- [x] Performance: measured on a synthetic grid in edit mode, geometry only, with temporary Stopwatch code run through the Unity MCP and nothing left in the files. I didn't time a real level: that needs Play mode. The largest level prefab has about 92 named cells (`Level1-C3 1`), so 144 cells covers it with margin.
  - Shift refresh (`GetAttackableCells`, one unit, 41 reachable origins): 1.3 ms with one ranged attack and 2.1 ms with three attacks on 144 cells (2.6 / 3.4 ms on 400 cells). That is borderline against 2 ms. A per-refresh memo wouldn't help: within one refresh each (origin, ability) pair is already computed once. After C5 a Bergson's Shift is one origin (≈0.05 ms), and only an enemy's danger zone stays at this cost, once per Shift press or hover.
  - Ghost hover (`GetThreateningEnemies`, 8 enemies × 41 origins × 3 attacks): 8.2 ms on 144 cells and 23.9 ms on 400 cells without a pre-check. **With the pre-check now in the code: 0.13 ms and 0.20 ms.** The found threats are the same.
- [x] Compile clean (no `error CS`). EditMode suite through the Unity MCP: 199 tests, 198 passed. The one failure is the known red `AIRegressionTest.Baseline_MatchesCurrentAI` (not touched).
- [x] The AI does not call `UnitThreatAnalysis` (grep): its only callers are `PlayerController.cs:982` and `ShowStatsHoverPreview.cs:113,120`.

## Save reset

no

## Decisions I made

- **Footprint excluded when `IncludeSelf` is off.** `ComputeAttackRangeFromOrigin` doesn't do this. Without a `source`, `GridCell.GetRangeCells` with ranged reach also adds the origin cell itself (distance 0), and a multi-cell unit would reach its own other cells. The real targeting passes `source` and removes them (`set.RemoveWhere(source.Occupies)`), so the exclusion matches the real action. Only the unit's own cells change, so C2's approach check against an enemy is unaffected.
- **Ready filter on `GetAttackableCells`/`GetThreateningEnemies`** (Attack type and `RemainingCooldown == 0`; `Abilities` already filters `Available`). The plan names "ready" for C5. I applied it in C1 as well, because the design calls ignoring Dash's cooldown part of P3. As a result, Shift no longer shows John's Dash lines while Dash is on cooldown.
- **Exact radius pre-check** in `AttackReaches`/`GetThreateningEnemies` instead of a memo, because the threat-arc case was 4× over the 2 ms budget. It skips (origin, ability) pairs whose footprint is out of radius of the target, so the hits are the same. It is turned off for shape definitions and for cost-weighted walks (PathWalkable, not straight), because one hazard has `movementCostModifier: -1`, so a step can cost 0. A test covers the invariant it relies on.
- Splash mode reuses the old `CollectAttackedCells`, with its targets now from `AttackReachFrom`.

## Needs THJ

None. **For the coordinator (C5):** cooldowns tick at the owner's phase start, before it acts (`RuntimeAbility.PhaseTick`), and the AI simulates `RemainingCooldown - 1` (`AIUnitBrain.SimCooldown`). So an enemy ability at cooldown 1 during the player's turn is ready on the enemy's next turn. C1 uses the literal plan ("not on cooldown" = 0) for both Shift and the arcs. C5 and the arcs probably want `cooldownTicksAhead: 1` for enemies, and C5 also decides `includeAreaSplash`. Both are single-argument changes.

## Docs to update

- `tech/combat-architecture.md`: there is one attack-reach helper (`UnitThreatAnalysis.AttackReachFrom`), and any new attack-geometry flag goes through it. Also mention the threat-arc pre-check.

## Risks and loose ends

- `GridCell.GetRangeCells` with `allowRangedReach` and no `source` includes the origin cell itself (core). The helper works around it. C2's ghost path will go through the helper, but anything else that calls `GetRangeCells(..., allowRangedReach: true)` without a source has the same quirk.
- `GridCell.cs` ranged reach scans the whole grid for each origin, which costs about 0.03–0.06 ms per origin. A future speedup belongs in core and wasn't changed.
- Until C2, the approach preview (`PlayerController.ComputeAttackRangeFromOrigin`) still uses the controller's faction and keeps the self-cell quirk. The ghost icons still miss ranged reach (P6).
- The numbers are geometry only. Real calls add `GetReachableCells` (one BFS per enemy) and stat evaluation for `Parameters.radius`. The C9 profile should confirm them on a dense board.

## Proposed commits

1. `fix(preview): share one attack-reach helper for Shift and enemy threat arcs`: `miso/Assets/_Project/Core/Interactions/Runtime/UnitThreatAnalysis.cs` (plain, not core)
2. `test(preview): edit-mode tests for attack reach geometry`: `miso/Assets/_Project/Core/Interactions/Editor/AttackReachTests.cs`, `AttackReachTests.cs.meta` (plain; depends on 1)

They can also be one commit if THJ prefers.

## Other branches

none (the work merges to `main` later with the branch)

## How to see it

1. Open a level with John and at least one enemy (any campaign level through the toolbar level picker from `PreloadScreen`).
2. Hold Shift and hover John while his Shield Dash is ready. The attack icons should be crosses (straight lines) from his reachable cells, not a diamond. Use Dash once, then hold Shift again: the Dash lines are gone while it's on cooldown.
3. Hold Shift over Linda on a map with a missing tile in her line. Her icons continue past the gap.
4. Select a unit and hover move cells next to enemies. Threat arcs come only from enemies that could really hit that tile: ranged enemies across gaps, straight-line enemies only along their lines. Hovering should feel as smooth as before.
5. Still unchanged until C2: the ghost's own sword icons, which still miss ranged reach.
