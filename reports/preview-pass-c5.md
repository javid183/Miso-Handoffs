# Report: Grid preview pass, C5 Shift model and tints (P7, G3)

Plan: plans/2026-10-19-preview-pass-tech.md (chunk C5)    Agent: miso-implementer    Branch: thj/preview-improvements
Outcome: done. The in-game look is left for the C9 play check. The enemy danger-zone timing is over the 2 ms target on the heavier synthetic cases (see Needs THJ / coordinator).

## What changed

- `miso/Assets/_Project/Core/Systems/GridSystem/Runtime/GridCell.ShiftPreview.cs` (core partial, UTF-8 BOM and LF kept): `ShiftPreviewLayer` gains `EnemyMove = 1 << 2` and `EnemyAttack = 1 << 3`, an additive enum change. They draw on the same renderers as `Move`/`Attack` (frame + glow, attack icon), with the same sorting, alpha and blend, and only the tint differs. The old move-blue and attack-pink tints are replaced by four named constants: `ShiftPreviewBergsonMoveTint` (0.6, 0.8, 0.8), `ShiftPreviewBergsonAttackTint` (1, 0.9, 0.75), `ShiftPreviewEnemyMoveTint` (0.7, 0.45, 0.4), `ShiftPreviewEnemyAttackTint` (1, 0.25, 0.2). Two internal pickers (`ShiftPreviewMoveTintFor`, `ShiftPreviewAttackTintFor`) choose the tint from the cell's flags; Bergson wins if both kinds are on one cell. The inactive-cell rule now masks both move kinds. The D-071 mechanics (own renderers, sorting offset, depth nudge, footprint fit, alpha 0.55, blend 0.35) are unchanged.
- `miso/Assets/_Project/Core/Interactions/Runtime/ShiftPreviewRules.cs` + `.meta` (new, LF, no BOM, like `UnitThreatAnalysis.cs`): pure rules. `PlanFor(isPlayerFaction, isSelectedUnit)` returns the move layer (or None), the attack layer and the attack source (`BasicAttackFromCurrentCell` or `DangerZone`). It also holds the constants `EnemyCooldownTicksAhead = 1` and `EnemyIncludeAreaSplash = false` (D-085). Constants only, no static state.
- `miso/Assets/_Project/Core/Interactions/Runtime/ShowStatsHoverPreview.cs` (LF kept): `ShowPreview` follows the plan. Bergson: `BasicAttackReachFrom(unit, unit.CurrentCell)`, plus its move layer unless it is `PlayerController.CurrentlySelectedUnit`. Enemy: move layer + `GetAttackableCells(unit, 1, false)`, both in the enemy kinds. Two instance fields remember the layer flags used, so clearing removes exactly those flags. The preview is still recomputed on every Shift press and hover.
- `miso/Assets/_Project/Core/Interactions/Editor/ShiftPreviewRulesTests.cs` + `.meta` (new, UTF-8 BOM and LF, like `AttackReachTests.cs`): 6 EditMode tests.
- `UnitThreatAnalysis.cs` needed no change.

## Acceptance criteria

- [x] Shift on a Bergson: the attack icons are `BasicAttackReachFrom(unit, unit.CurrentCell)`, which is `AttackReachFrom(unit, unit.DefaultOccupiedCellAbility, unit.CurrentCell)`. The selected unit gets no Shift move layer; other Bergsons keep theirs. Evidence: code; tests `SelectedBergson_NoMoveLayer_BasicAttackFromCurrentCell` and `OtherBergson_MoveLayer_BasicAttackFromCurrentCell` cover the selection logic. **In game: C9 play check.**
- [x] Shift on an enemy: move layer + danger zone = `GetAttackableCells(enemy, cooldownTicksAhead: 1, includeAreaSplash: false)`, which is the union of `AttackReachFrom` over reachable cells and ready Attack abilities. It is recomputed on each Shift press and hover (`OnToggleShowStats` and `OnEntityHovered` both call `ShowPreview`, which clears first). Evidence: code; tests `Enemy_EnemyMoveAndDangerZone` and `DangerZone_CountsNextTurnCooldowns_WithoutSplash`. **In game: C9.**
- [x] Tints are named constants in `GridCell.ShiftPreview.cs` with the design values, and the enemy/Bergson split is two additive enum values. Alpha unchanged. Evidence: test `Tints_MatchDesignValues_AndPickByKind` (reads the internal pickers by reflection).
- [x] D-071 layer mechanics unchanged (diff: only the enum, the tint constants, two mask constants, the tint pick and the inactive-cell mask).
- [x] No new mutable statics. The only new static fields are `static readonly Color` tint values (Color can't be `const`), the same pattern as the old two, plus `const`s. No `PlayModeStaticReset` change needed. BOM and LF kept on every touched file (checked with `xxd` and a CR count).
- [~] Performance (temporary Stopwatch code run through the Unity MCP `execute_code`, nothing left in the files). Geometry only, on a synthetic grid built like `AttackReachTests`: center origin, move radius 4 gives 41 reachable cells. Attacks: a straight radius-4 attack with ranged reach, a radius-1 melee, a radius-2 diamond. Best of 20:
  - 12x12: 1 ranged attack **1.29 ms**; 3 attacks **2.71 ms** (mean 2.91).
  - 20x20: 1 ranged attack **2.43 ms**; 3 attacks **3.91 ms** (mean 4.06).
  - Bergson one-origin ranged reach: 0.03 ms (12x12), 0.06 ms (20x20), well under target.
  - The enemy case runs once per Shift press or hover, not per frame. A one-attack enemy on a normal level (largest level has about 92 cells) is under 2 ms; a 3-attack enemy or a large board is over. No memo added (see Needs THJ / coordinator).
- [x] Compile clean (no errors in the console after a forced refresh; only pre-existing warnings). Full EditMode suite through the Unity MCP: **218 tests, 217 passed, 1 failed = the known red `AIRegressionTest.Baseline_MatchesCurrentAI`** (not touched). The 6 new tests pass on their own as well.

## Save reset

no

## Decisions I made

- **"Bergson" means `unit.Faction == CombatLevel.Instance.PlayerFaction`**, the same test as `GUnit.isPlayerUnit`, but null-safe. Every other unit, including any non-player ally faction, gets the enemy model and tints. The plan names only these two cases.
- **Selected unit** = `PlayerController.CurrentlySelectedUnit`, read only once the controller's `Faction` is set (its `PhaseData` is created in the same `Initialize` call), so the read can't throw before init. The preview is still skipped during target selection, as before.
- **Enemy split as two flag values, not a bool parameter.** They reuse the same renderers, so a cell never draws two frames. Clearing passes the exact flags that were set.
- **Kept the tint blend (0.35 toward the tint) and the alpha (0.55).** The design values replace the tint constants that feed the blend, so on screen the colours are the real visual's colour pushed 35% toward these tints, as before. If THJ wants the pure tints, raise `ShiftPreviewTintBlend` (one lever, affects all four).
- **Pure rules in a new non-core file** (`ShiftPreviewRules`), so the selection logic is testable without a level.

## Needs THJ

None for THJ. **For the coordinator:** the enemy danger zone measured 2.7 ms (12x12, 3 attacks) and 3.9 ms (20x20, 3 attacks) against the 2 ms target. The cost is one hitch per Shift press or hover, not per frame. C1 already found that a per-refresh memo doesn't help: each (origin, ability) pair is computed once. The cost is in core `GridCell` ranged reach, which scans the whole grid for each origin, plus the non-straight walks. Options:
- A: accept it and confirm on a dense real board in C9 (recommended: real enemies mostly have 1 to 2 attacks, and the largest level is about 92 cells).
- B: an instance-scoped cache in `ShowStatsHoverPreview` keyed on the hovered enemy, cleared on Shift release. It only saves repeat hovers within one Shift hold, and it can go stale if something moves mid-hold.
- C: a core speedup of ranged reach in `GridCell` (Tier 3, separate task).

## Docs to update

- `design/gdd/combat-rules.md` (Shift view, by the designer): Bergson = basic-attack reach from the current tile, no move frames on the selected unit; enemy = move + danger zone (ready Attack abilities counting next-turn cooldowns, no splash), in red tints.
- `tech/combat-architecture.md`: the Shift layer has Bergson and enemy kinds (`ShiftPreviewLayer.EnemyMove/EnemyAttack`); the rules live in `ShiftPreviewRules`.

## Risks and loose ends

- The timings are geometry only. Real calls add `GetReachableCells` (one BFS) and stat evaluation for `Parameters.radius`. C9 should profile Shift over a multi-attack enemy on the densest level.
- Non-player ally factions (if any level has them) now show a red danger zone under Shift. Check in C9 whether any such unit exists (Toba as ally?) and whether that reads wrong.
- The tints are blended and alpha'd, so the enemy red is softer than (1, 0.25, 0.2) on screen. Tune `ShiftPreviewTintBlend` if it isn't distinct enough from the real attack icons.
- `FactionControllerBase.CurrentlySelectedUnit` dereferences `PhaseData` without a null check (core, not changed). The preview guards it from outside.

## Proposed commits

1. `feat(grid): split Shift preview tints into Bergson and enemy kinds`: `miso/Assets/_Project/Core/Systems/GridSystem/Runtime/GridCell.ShiftPreview.cs` (**core**, additive enum values + tint values). It stands alone: it compiles with the current caller, and on its own it re-tints the existing Shift move and attack layers to the Bergson colours.
2. `feat(preview): Shift shows current-tile reach for Bergsons and a danger zone for enemies`: `miso/Assets/_Project/Core/Interactions/Runtime/ShiftPreviewRules.cs`, `ShiftPreviewRules.cs.meta`, `miso/Assets/_Project/Core/Interactions/Runtime/ShowStatsHoverPreview.cs`, `miso/Assets/_Project/Core/Interactions/Editor/ShiftPreviewRulesTests.cs`, `ShiftPreviewRulesTests.cs.meta` (plain; depends on 1, whose new enum values it uses)

The tests can be split out of commit 2 as `test(preview): edit-mode tests for Shift preview rules` if preferred; they need commit 1's pickers and commit 2's rules.

## Other branches

none (the work merges to `main` later with the branch)

## How to see it

1. Open a level with at least two Bergsons and an enemy (toolbar level picker from `PreloadScreen`).
2. Select John. Hold Shift and hover John: no move frames, and warm-white sword icons only where his basic attack reaches from his tile.
3. Still holding Shift, hover another Bergson (for example Linda): grey-teal move frames plus warm-white icons from her tile only (no longer most of the map).
4. Hold Shift and hover an enemy: red-brown move frames and a strong-red danger zone wherever it could attack after moving. An ability with one turn of cooldown left counts; area splash doesn't.
5. Release Shift: everything clears, and the selected unit's real move range is untouched.
