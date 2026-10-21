# Report: Masher reckless tank, C5 (preview)

Plan: plans/2026-10-20-masher-reckless-tank-tech.md (C5)    Agent: miso-implementer    Branch: masher-tweak
Outcome: done (compiles clean; EditMode 356 of 357 pass, the one red is the known `AIRegressionTest.Baseline_MatchesCurrentAI`). The preview itself needs the play check.

## What changed

Paths under `miso/Assets/_Project/`.

**Commit A (core, additive, D-105)**
- `Core/Interactions/Runtime/PlayerController.cs`: `TryFindApproachCell(RuntimeAbility, GUnit, out GridCell)` and `ResolveGhostCell(RuntimeAbility, GridCell, out bool)` go from private to public, plus a one-line comment each. No body change. LF kept.

**Commit B (Masher preview)**
- `Features/Enemy/Masher Goblin/Scripts/MasherGoblinFactionRoleHandler.Preview.cs` (+ `.meta`), new: the whole hover preview (event handlers, `ShowReactionPreview`, end-tile prediction, Duo partner pick, drawing and clearing). LF, no BOM, like its siblings.
- `.../MasherGoblinFactionRoleHandler.cs`: preview code, its four fields, `TryPickAttackCell` and the Masher's own `TryFindApproachCell` removed (nothing else used them). `DistanceToEnemyFrom` and `TryScoreTargetCell` stay (role zone).
- `.../MasherGoblinFactionRoleHandler.Counter.cs`: `TryPlanAnswer(GUnit ...)` now builds the target coordinates and calls a new overload `TryPlanAnswer(List<Vector2Int> targetCoords, ...)` with the unchanged body. Plus an `Overlaps` helper and one skip in the step-candidate loop (see Decisions).

## Acceptance criteria

All need the play check; no new pure logic, so no new EditMode tests (the rules it calls, `MasherCounterRules`, are already covered).
- [ ] Preview shows after the first answer in a turn: the `ActivatedAtThisPhase` gate is gone. Play check.
- [ ] Step ghost and path at any range, slam tiles only when it ends adjacent: `TryPlanAnswer` gives `stepCell` and `slamsAfter`; ghost and path drawn when `stepCell` differs from the current tile; the cross only when `slamsAfter`. Play check.
- [ ] Slam centred on the striker's tile: the struck cell is `MasherCounterRules.PickAttackCell` over the striker's end footprint, and the area comes from `ComputeAffectedCells(ability, Unit, thatCell)`. Play check.
- [ ] Crippled: no step, because `TryPlanAnswer` fails the walk's feasibility check. Play check.
- [ ] Damage on every unit in the cross, goblins included, all cleared: `AbilityDamagePreview.ComputeFor(ability, Unit, attackCell)`, tracked in `_previewDamageUnits`. Play check.
- [ ] End tile: basic-attack approach via `TryFindApproachCell`; `IGhostDestinationProvider` via `ResolveGhostCell`; other moving abilities use the current tile. Play check.
- [ ] Lethal hit: no preview (check kept). Play check.
- [ ] Duo: see Decisions. Play check.

## Save reset

no

## Decisions I made

- The preview uses the role counter ability (`ability`), not `_attack` (the unit's main slam) as before, since that is what the real answer plays.
- Out of range, the approach is only tried for a basic attack with `AutoMoveAllowed` (the same gate PlayerController uses on hover); another out-of-range ability gives no preview.
- `TryPlanAnswer` skips step cells whose footprint overlaps the target footprint. In the real answer the striker occupies those cells, so they were already excluded by `IsFootprintEmpty`; in the preview the striker's end tile is empty now, so without this the Masher could "step onto" it. No change to real behaviour.
- Striker damage when it is not yet on its end tile: the grid is read as it is now, so the cross may not list the striker. The preview then gives it the damage of another unit in the cross (a same-faction one first). Exact when the striker stays put. The slam deals the same ability modifiers to all, but a per-target resist or tag modifier could make the number differ; if the cross lists nobody, no damage shows for the striker.
- Duo: the entry is read from the selected ability's `AEffectCoOpTrigger` (`TriggerID`, `CooperationHandler.TryGetEntry`). Struck = the partner's ability `ComputeFor` the Masher's cell includes this Masher; reachable = `PlanAgainst` slams; ActedOrder = entry index; then `MasherCounterRules.PickDuoPartner`, the same pick as the real answer. The activator is measured from its predicted end tile, other partners from their current tile (their own approach or dash is not predicted). If no entry is found, it previews the activator. If the entry is found and no partner would strike, no preview.

## Needs THJ

none

## Docs to update

- `tech/combat-architecture.md` / Masher notes: preview now in `.Preview.cs`, uses `TryPlanAnswer(coords)`.
- `tech/core-systems.md`: `PlayerController.TryFindApproachCell` and `ResolveGhostCell` are public (D-105).
- `plans/...-tech.md` commit log: C5 hashes once committed.

## Risks and loose ends

- Shield Dash and Vault (non-provider moving abilities) preview from the striker's current tile (D-105, follow-up). A partner's own approach or dash in a Duo is likewise not predicted.
- The step planner measures free cells with the striker still on its current tile; the real step happens after the striker has moved, so a cell the striker will vacate is seen as blocked. Rare.
- `ComputeAffectedCells` takes the Masher at its current position; fine for the plus-shaped targeted slam, but a Surrounding/self-centred shape would be centred on the old tile (not the case for the counter preset).
- `PlayerController.TryFindApproachCell` reads `PhaseData.ActiveUnit` and the AP check; it is only valid while the striker is the selected unit, which the preview already requires.

## Proposed commits

1. `refactor(player): expose approach and ghost-destination lookups read-only for previews`: `Core/Interactions/Runtime/PlayerController.cs` (core, additive, own commit; first).
2. `feat(masher): preview the answer from the striker's end tile, keep it after the first answer, show damage on the whole cross`: `Features/Enemy/Masher Goblin/Scripts/MasherGoblinFactionRoleHandler.Preview.cs` + `.meta`, `MasherGoblinFactionRoleHandler.cs`, `MasherGoblinFactionRoleHandler.Counter.cs` (plain; after 1).

## Other branches

`thj/home-test` would need both at merge (same as C1 to C4).

## How to see it

1. Open `LevelE3-C1` (or `LevelM1-C3`) with a Masher alive; select a player unit and a ranged or melee ability.
2. Hover the Masher: the ghost and path show where it steps, the plus-shaped tiles appear only if it would end next to the striker, and every unit in the cross (goblins too) shows its damage.
3. Hover with a basic attack from range (the striker would walk in): the cross is centred on the tile the striker walks to. Hover with a dash attack: centred on its landing tile.
4. Let the Masher answer once, select another unit, hover again: the preview is still there.
5. Cripple the Masher: ghost and path gone. Aim a lethal hit: nothing shows.
6. Select a Duo trigger and hover the Masher: the preview follows the partner that would be answered.
