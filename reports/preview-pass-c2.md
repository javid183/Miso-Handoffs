# Report: Grid preview pass, C2 Ghost and approach previews use the shared reach (P6)

Plan: plans/2026-10-19-preview-pass-tech.md (chunk C2)    Agent: miso-implementer    Branch: thj/preview-improvements
Outcome: done (the in-game check is left for the C9 play check)

## What changed

- `miso/Assets/_Project/Core/Interactions/Runtime/PlayerController.cs` (core, approved Tier 2 bugfix; LF, no BOM, unchanged): +4 / -40.
  - Ghost sword icons (hover path, about L994-997): the inline `ghostCell.GetRangeCells(...)` on `ghostUnit.DefaultOccupiedCellAbility` became `UnitThreatAnalysis.BasicAttackReachFrom(ghostUnit, ghostCell)`. This is the same ability, but now with ranged reach, footprint, shape definitions and the ghost unit's faction.
  - Approach preview: `AttackReachesFrom` (L1385) and `ShowApproachAttackRange` (L1445) call `UnitThreatAnalysis.AttackReachFrom(unit, ability, origin)`.
  - The private `ComputeAttackRangeFromOrigin` is removed, since it has no other callers.
  - `ShowAffectedArea` abilities still go through `AbilityPreset.ComputeAffectedCells` (the `if` branch above, not touched).
- Nothing else changed: no new statics, no other PlayerController code.

## Acceptance criteria

- [x] The ghost sword icons and the approach preview call `AttackReachFrom`, and `ComputeAttackRangeFromOrigin` is removed. Evidence: the diff.
- [ ] Linda's ghost on (2,4) shows a sword icon on (4,4) when (3,4) is missing. **Play check (C9).** In code it follows from her primary attack (`straightDirectionCellsOnly: 1`, `allowRangedReach: 1`), which now reaches the ghost through `CollectReachFromFootprint` (`allowRangedReach` is passed). The old inline call never passed it. C1's `AttackReachTests` cover the gap-crossing geometry.
- [x] `ShowAffectedArea` abilities keep `ComputeAffectedCells`. Evidence: that branch is unchanged in the diff.
- [x] Compiles: the Editor log has no `error CS` lines, and the PlayerController warning line moved from 1491 to 1455, so the compile included the edit. Only the known warnings remain.
- [x] EditMode suite through the Unity MCP: 199 tests, 198 passed. The only failure is the known red `AIRegressionTest.Baseline_MatchesCurrentAI` (not touched).
- No new EditMode test. The ghost path sits inside `PlayerController`'s hover handler and needs a live controller, `PhaseData`, a `GUnit` and a `RuntimeAbility`, so it can't run without a scene. C1's geometry tests already cover the helper.

## Save reset

no

## Decisions I made

- **Approach preview differences from the old `ComputeAttackRangeFromOrigin`, and why I kept none of them:**
  - **Faction:** the helper uses `unit.Faction` instead of the controller's `Faction`. For the approach preview the unit is always `PhaseData.ActiveUnit`, and unit selection requires `ActiveUnit.Faction == Faction` (`FactionControllerBase.cs:390`). So the faction is the same, and there is no difference.
  - **Cooldown filter:** it applies only to `GetAttackableCells`/`GetThreateningEnemies`, not to `AttackReachFrom`. So there is no difference.
  - **Own tiles without IncludeSelf (D-085):** this one is a small visible change, and the helper has no option to switch it back. Without a `source`, `GetRangeCells` with `allowRangedReach` adds the origin cell itself, so the old approach highlight (`SetHighlight`) lit the approach/ghost cell. This happens for Linda's and Mark's primary attacks, the only auto-move attacks with ranged reach (both `includeSelf: 0`). The helper drops the unit's own tiles, as the real targeting does and as D-085 decided. The approach cell **choice** (`AttackReachesFrom`) is unaffected, because it only tests enemy cells, which can't be in the unit's empty footprint. If the old highlight on the ghost's own cell is wanted back, that needs an option in the helper, which is a C1 API change. I didn't add one.
- I removed the private method instead of keeping a one-line forward, because nothing else calls it.

## Needs THJ

none. **For the coordinator:** please confirm that the D-085 own-tile rule also covers the approach highlight, as described above.

## Docs to update

- `tech/combat-architecture.md` (with C1's note): the ghost icons and the approach preview now use `UnitThreatAnalysis.AttackReachFrom`. `ComputeAttackRangeFromOrigin` no longer exists.

## Risks and loose ends

- The ghost icons now use the ghost unit's faction for walkability (before: `null`). This matters only for basic attacks with `PathWalkable`/`SelfWalkable` application. The player's basic attacks checked above don't use straight or path modes that depend on it, but the play check should look at John and Mark too.
- The ghost icons for multi-cell ghosts now come from the whole footprint, as the real attack does. Before, they came from the anchor cell only.

## Proposed commits

1. `fix(preview): ghost and approach previews use the shared attack reach`: `miso/Assets/_Project/Core/Interactions/Runtime/PlayerController.cs` (core; depends on b678aeecc)

## Other branches

none (it merges to `main` with the branch)

## How to see it

1. Open a level with Linda and an enemy, and make sure a tile is missing in a straight line from a cell Linda can move to. For the plan's case: Linda's ghost on (2,4), with (3,4) missing.
2. Select Linda and hover her move cell (2,4). The ghost appears with sword icons, and (4,4) has one across the gap, as her real attack would.
3. Do the same with Mark (ranged reach, not straight): his icons also show past missing tiles.
4. Select Linda with her primary attack and hover an enemy that's out of reach, so the approach preview runs. The highlighted range from the approach cell is as before, except that the approach cell under the ghost is no longer lit.
5. Hover with an ability that has `ShowAffectedArea`: its area preview is unchanged.
