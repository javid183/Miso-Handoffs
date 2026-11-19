# Report: Cyclone round 3, C2 cast on an enemy (rule, shove, preview, tests)

Plan: plans/2026-11-18-cyclone-round3-tech.md (chunk C2; design plans/2026-11-18-cyclone-round3-design.md §3, §6; decisions D-566, D-567, tie rule "the free cell, else along the row")    Agent: miso-implementer    Branch: thj/cyclone (on top of the uncommitted C1)
Outcome: done (compiled in the open editor through the Unity MCP; EditMode run, see "Test run"). No core file touched; no asset, prefab or scene edited.

## What changed

All under `miso/Assets/_Project/Features/Player/Lucy/Scripts/`. LF, no BOM (like the neighbours).

New (each with its `.meta`):
- `Cyclone/CycloneRules.CastOnEnemy.cs`: partial of `CycloneRules`. `IsEnemyOf(unit, caster)` and `IsPullableBy(unit, caster, pullFilter)` (the Whirl's pull filter on plain arguments, extracted from `CycloneWhirlSteps`); `CastRulesFor(caster, pullFilter)` (carry rules for the cast: nobody crossed, ride = pullable and not `CycloneHeavy.IsHeavy`); `CastShoveDirections(lucy, target)` (larger axis; at a tie the row (x), then the column (y)); `PlanCastShove(lucyCell, cell, rules)` (refuses any planted or stashed entity on the cell, then tries the directions through `CycloneCarryPlanner.Shove`, first that works wins); `CastShoveCell`; the overload `IsValidCastCell(cell, lucyCell, rules)` (empty, or a shovable enemy).
- `Cyclone/AEffectCycloneSpawner.Shove.cs`: partial of the spawner. `CastShoveFor(owner, cell)` (null for an AI-controlled caster, via `AEffectCycloneSteer.IsAIControlled`; reads the prefab's pull filter), `ShoveThenCast(owner, cell, shove, spawn)` (the routine: glide at the prefab's `SteerSecondsPerCell` while the enemy keeps its cell, one landing (unplug, plug on the landing cell, end-of-move event, wake), re-check the cell is empty, spawn, wait for the cast Whirl's pull; `IsInProgress` held throughout, released in `finally`), `ShoveSteps` seam.
- `Cyclone/ICycloneShoveSteps.cs` + `Cyclone/CycloneShoveSteps.cs`: the shove's steps (position, delta time, start-of-move event, unplug, plug, landed = `unitEndMoving` + `WakeIfUnaware`), the same grid calls and events as `CycloneSteerSteps`' carry.
- `Editor/CycloneCastOnEnemyTests.cs`: 19 tests (list under Acceptance criteria).

Changed:
- `Cyclone/AEffectCycloneSpawner.cs`: now `partial` and implements `ITargetSelectionRangeProvider`. `CheckTargetSelectionCondition` = empty cell or `CastShoveFor != null`. `TryCollectTargetSelectionCells` = the cast's normal range (`AbilityPreset.ComputeTargetSelectionCells`, the multi-activation multiplier only for a move, as `RuntimeAbility` counts it) filtered by that check. `ApplyUnguarded`: empty cell exactly as before; an enemy cell starts `ShoveThenCast` (spawning on the cell, never on the shoved unit); anything else keeps the "Cyclone not cast: cell ... is not empty" warning (text extended with "and holds no enemy it can shove"). Header comment updated.
- `Cyclone/CycloneCarryPlanner.cs`: the front-shove test of `CanTakeStep` extracted into `CanShoveFront` (same expression, same result); new `Shove(cell, direction, rules)` builds a plan with the Cyclone on `cell` and the one front move. The Steer and the cast now run literally the same rule.
- `Cyclone/CycloneWhirlSteps.cs`: `IsEnemy` / `IsPullable` delegate to `CycloneRules.IsEnemyOf` / `IsPullableBy` (same checks, including the worker-thread guard).
- `Cyclone/CycloneCastPreview.cs`: on an enemy cell, plans the shove with `_spawner.CastShoveFor` (the execution's function) and passes it to `ForCast`; `IsPullable` / `IsEnemy` use the shared filter; header comment updated.
- `Cyclone/CycloneOutcome.cs`: `ForCast` gains an optional `shove` plan: the shoved enemy's way comes first, the Whirl plans on `shove.OccupantOf` (the board after the shove).
- `Cyclone/CycloneRules.cs`: `partial`; one comment line on `IsValidCastCell` (it stays the empty-cell rule for the Steer's end and Super Time).
- `Cyclone/CycloneEntity.Steer.cs`: read-only `SteerSecondsPerCell` getter (the shove's glide pace).
- `Editor/CycloneSteerTests.cs`: `TargetSelectionRange_SuppliedByTheSteerOnly_AroundTheCyclone` asserted "the cast keeps its normal range"; the cast now supplies its range, so the test is renamed `TargetSelectionRange_TheSteerAroundTheCyclone_TheCastAroundLucy` and checks the cast's cells are around Lucy, not her cell. The Steer half is unchanged.

Not touched: C1's `CycloneCrossView.cs` and `CyclonePreviewTests.cs` (still uncommitted, as given), every core file (`PlayerController`, `GridManager`, `AEffectPusher`, `AEffectTransporter`, `AbilityDamagePreview`, `AEffectSpawner`, `FactionControllerBase`), `LucyFactionRoleHandler.cs`, THJ's `PreloadScreen.unity`, `ProjectSettings/*`, TMP fallback font. No new statics.

## Acceptance criteria (C2 part)

- [x] **Rule.** A one-cell, non-Immovable enemy hostile to Lucy is shoved one cell along the larger axis away from her, then the Cyclone is planted on its old cell, then the cast Whirl plays: `Shove_GoesOneCellAlongTheLargerAxis_AwayFromLucy_OnEachAxis` (up, left, 2-right-1-up along x, 1-left-2-down along y), `TheShove_LandsOnce_ThenTheCycloneIsCast_AndTheShovedEnemyStandsWhereTheWhirlHits` (events exactly `start, unplug, plug (3, 5), hazard Spikes, landed, spawn`; the cell is empty at spawn; the shoved enemy is in `HitTargets`). The Whirl is the spawned Cyclone's own `Initialize → StartWhirl`, unchanged (pull, reactions, hit).
- [x] Shove is free, lands once, hazard on the landing cell fires, no hazard on cells crossed, no Crippled damage: same test (one plug, one hazard event, no pusher is involved: `CycloneShoveSteps` only unplugs and plugs, like the carry). `AHazardOnTheLandingCell_DoesNotStopTheShove`.
- [x] Watch answers the landing, the enemy wakes: `TheRealSteps_MoveTheEnemyOnTheGrid_AndRaiseItsMoveEventsOnce` (real `CycloneShoveSteps` on prefab cells: `unitStartMoving` once, `unitEndMoving` once, the event Linda's Watch listens to; wake through the existing `WakeIfUnaware`). Watch's actual arrow: play check.
- [x] Diagonal neighbour: the free one; both free: along the row. The grid's row axis is x (`LevelBase.prefab` Grid: rectangle layout, XYZ swizzle; coordinates come from `Grid.WorldToCell`, x is screen-horizontal). `Directions_LargerAxisOnly_AndRowThenColumnAtATie`, `Shove_AtEachDiagonalNeighbourOfLucy_GoesAlongTheRow_WhenBothCellsAreFree` (all four), `Shove_AtADiagonalNeighbour_TakesTheFreeCell_AndIsRefusedWhenNeitherIsFree`.
- [x] Not offered (click refused) when the shove cell is a wall, the edge, a unit, a walk-blocking planted entity or a stashed entity: `Refused_WhenTheShoveCellIsAWall_TheEdge_AUnit_AWalkBlocker_OrStashed` (no chain push: the unit behind stays). Heavies (Immovable), large, neutral, ally, family: `Refused_ForHeavyLargeNeutralAllyAndFamilyUnits`. Planted cell with an enemy on it: `Refused_OnACellWithAPlantedEntity_EvenWithAnEnemyOnIt`.
- [x] Range highlight includes castable enemy cells and excludes refused ones: `TheRangeHighlight_OffersCastableEnemyCells_AndNotRefusedOnes` (via `TryCollectTargetSelectionCells`, which `FactionControllerBase.ComputeAbilityRangeCells` reads through the existing `ITargetSelectionRangeProvider` hook). The highlight in the level: play check.
- [x] Empty cells castable as before; cells next to Lucy castable on enemies: `EmptyCells_AreCastableAsBefore_AndAnEnemyNextToLucyIsCastable`, and every existing `CycloneCastTests` test passes unchanged.
- [x] `IsValidCastCell(cell)` unchanged for the Steer's end and Super Time; an AI-controlled Lucy only gets empty cells: `TheEmptyCellRule_IsUnchanged_ForTheSteersEndAndFamilySuperTime`, `AnAIControlledLucy_CastsOnEmptyCellsOnly`. `LucyFactionRoleHandler.cs:246` still calls the one-argument rule.
- [x] Preview from the same planner move as the execution, with ghost, tether, damage, hazard ring and pull ghosts: `ThePreview_ShowsTheShoveTheCastMakes_ThenTheWhirlOnTheBoardItLeaves` (ghost on (3, 5), hazard ring, 3 damage on the shoved enemy's ghost, the arm enemy's pull ghost on the board after the shove, then the executed shove lands on the ghost's cell). The skull is drawn by the health bar itself (unchanged `CycloneOutcomeView`). Look in play: play check.
- [x] While aiming the cast, an enemy on a castable cell opens no unit hover panel and no attack cursor; a refused enemy shows "the normal panel": **no code needed, and no core change.** Evidence: the cast's `targetType` is `Cell` (`Lucy_Cyclone_Ability.asset` `targetType: 1`), so `PlayerController`'s target-selection state sets the grid's subject to `Cell` and `GridManager.HandleHovering` raises only `gridCellHovered`, never `gridCellEntityHovered`; `CombatLevelRunHandler.OnUnitHovered` also refuses the full-detail panel while any target is being selected; the approach attack (`CanApproachAttackTarget`) is for basic attacks only. A click on the cell goes to `TargetSelectionState.Apply(cell)` with the cell as the target, judged by the new check. Today's "normal" during the cast aim is therefore no panel for any enemy, castable or refused (the contrast is the highlight and the preview instead). Play check.
- [x] Shared pull filter: `ThePullFilter_IsSharedByTheWhirlAndTheCast` (enemy yes; Immovable, family, dead no; the live Whirl steps give the same answers).
- [x] Abort paths: `ALandingCellTakenDuringTheGlide_LeavesTheEnemyOnItsCell_AndCastsNothing`, `AnEnemyThatDiesDuringTheGlide_IsNotPutOnACell_AndTheCycloneIsStillCast`, `ALandingCutShort_PutsTheEnemyBackOnItsCell` (cast released in every case).
- [x] Compile clean (no errors, no warnings from the changed files); EditMode: see "Test run".

Needs the verifier's or THJ's play check: the glide (placeholder, C3 replaces it with the fling), the range highlight on a real board, the preview drawing, hover and click on castable and refused enemies, Watch's arrow on a shove into Linda's lane, the enemy waking, the cooldown when a shove-cast fails.

## Test run

- Before (C1 report): 2115 run, 2114 passed, 1 failed (the known red, inner `CHECKS: 714 FAILURES: 43`).
- Subset after (all `MISO.Core.Features.Bergsons.EditorTests`): 643 / 643 passed.
- Full suite after (MCP Test Runner, editor open, no Play mode): **2134 run, 2132 passed, 2 failed**. `AIRegressionTest.Baseline_MatchesCurrentAI`, inner **`CHECKS: 714 FAILURES: 43`** (unchanged). `GridToLevelHiddenTests.Build_HiddenUnitsAreInactiveAndListed` failed on the Unity-internal `Assertion failed on expression: 'm_LockCount == 0'` from `PrefabUtility.UnloadPrefabContents`, while the MCP plugin was disconnecting. Rerun of the GridToLevel group alone: that test passed, two other GridToLevel tests hit the same assert instead. This is the known flaky assert in the build log; GridToLevel shares no code with the Cyclone. The 19 new tests make up the difference from 2115.

## Save reset

No.

## Decisions I made

- New partials (`CycloneRules.CastOnEnemy.cs`, `AEffectCycloneSpawner.Shove.cs`) instead of growing the files; `CycloneRules` and the spawner became `partial`. Same behaviour. Tier 1.
- "Reuse `CanTakeStep`/`TakeStep`" done by extracting the front-shove expression into `CanShoveFront` and adding `CycloneCarryPlanner.Shove`. `CanTakeStep` itself needs a start cell one step before the target, which may not exist (a hole next to the target), and `TakeStep` also moves side and rear riders, which the cast must not. One rule, two callers. Tier 1.
- **Range highlight** through `ITargetSelectionRangeProvider` on the spawner. The plan assumed the highlight already filtered through the target check. It doesn't: the cast's highlight was every cell in Manhattan 3, so occupied and planted cells were highlighted and only the click refused them. To meet "refused cells not highlighted (heavies, family, allies, planted)", the highlight is now exactly the cells the check accepts. Side effect: empty-rule refused cells (family, allies, planted, stashed) are no longer highlighted either. Castability of empty cells is unchanged. Tier 2, visible; easy to narrow to "drop refused enemy cells only" if THJ prefers.
- The glide uses the Cyclone prefab's `steerSecondsPerCell` (0.15 s; 0.15 fallback without a prefab), read through a new getter. C3 replaces it with the fling. Tier 1.
- The cast's action stays open through the glide, the landing, the spawn and the cast Whirl's pull, in the same routine, the way `HoldCastWhileWhirlPulls` holds an ordinary cast. So the Watch answer to the shove's landing (queued during the action) plays after the pull, in the Whirl's reaction wait, before the hit. Order: shove lands → Cyclone planted → pull → reactions → hit. Under the one-Watch-per-action limit the shove's landing may take the one answer (accepted in the plan). Tier 1.
- A shove that can't land as planned (the landing taken meanwhile, the enemy moved or dead) leaves the enemy on its cell. The Cyclone is cast only if the cell is empty by then (a dead enemy frees it); otherwise warning "Cyclone not cast: cell ... is still not empty after the shove" and no Cyclone. The ability's AP and cooldown are spent at the ability level as for any failed cast today (same as the existing "cell not empty" refusal). Tier 1.
- `IsPullableBy` treats a unit without a tag set as passing the filter (no tags to leave it out), as `CycloneHeavy` already does. In a level every unit has a tag set; before, the Whirl's filter would have thrown on a null set. Found because edit-mode `AddComponent` units have none. Tier 1.
- The AI keeps empty cells through `CastShoveFor` returning null for an AI-controlled caster (the check the controller applies on its picks), so an AI-controlled Lucy behaves as before. Tier 1.

## Needs THJ

None (the highlight side effect above is flagged for the play check, not a question).

## Docs to update

- `tech/combat-architecture.md` (coordinator): the cast on an enemy (spawner check and range provider, `ShoveThenCast`, shared `CanShoveFront`, shared pull filter `CycloneRules.IsPullableBy`); the cast's range highlight now shows only castable cells.
- `tech/core-systems.md` (coordinator), Cyclone note: no core change in C2. The spawner now uses the existing `ITargetSelectionRangeProvider` hook (second user after the Steer).
- GDD `characters/lucy.md` LU-3 (designer, after the play check): the rule as built (direction, tie along x, refusals, free shove landing once, AI and Super Time empty-only, failed-shove behaviour, highlight shows castable cells only).

## Risks and loose ends

- The shove's glide is the round 2 lerp of the unit's root, a placeholder until C3's fling. C3 should replace the glide loop in `ShoveThenCast` and keep its landing and `finally` as they are.
- If the owner's coroutine is stopped from outside (Lucy destroyed mid-shove), Unity does not run the `finally`, so `IsInProgress` could stay set. The existing `WaitForPull` has the same exposure; a unit off its cell is impossible there since unplug and plug happen in one frame.
- `CycloneCastPreview`'s own `_range` still comes from `ComputeTargetSelectionCells` (unfiltered) and then the check, which is equivalent.
- `CycloneWhirlSteps.cs` and `CycloneCastPreview.cs` keep a few `using` lines they no longer need (harmless).
- The flaky GridToLevel `m_LockCount` assert showed up again during MCP disconnects (known).

## Proposed commits

Order: after the C1 commit (`CycloneCrossView.cs`, `CyclonePreviewTests.cs`). One commit, plain (Cyclone code and tests only; everything works together):

1. `feat(lucy): the Cyclone can be cast on an enemy, which is shoved one cell away from Lucy first; the range and the aim preview show the shove`:
   - `miso/Assets/_Project/Features/Player/Lucy/Scripts/Cyclone/AEffectCycloneSpawner.cs`
   - `miso/Assets/_Project/Features/Player/Lucy/Scripts/Cyclone/AEffectCycloneSpawner.Shove.cs` + `.meta`
   - `miso/Assets/_Project/Features/Player/Lucy/Scripts/Cyclone/CycloneRules.cs`
   - `miso/Assets/_Project/Features/Player/Lucy/Scripts/Cyclone/CycloneRules.CastOnEnemy.cs` + `.meta`
   - `miso/Assets/_Project/Features/Player/Lucy/Scripts/Cyclone/ICycloneShoveSteps.cs` + `.meta`
   - `miso/Assets/_Project/Features/Player/Lucy/Scripts/Cyclone/CycloneShoveSteps.cs` + `.meta`
   - `miso/Assets/_Project/Features/Player/Lucy/Scripts/Cyclone/CycloneCarryPlanner.cs`
   - `miso/Assets/_Project/Features/Player/Lucy/Scripts/Cyclone/CycloneWhirlSteps.cs`
   - `miso/Assets/_Project/Features/Player/Lucy/Scripts/Cyclone/CycloneCastPreview.cs`
   - `miso/Assets/_Project/Features/Player/Lucy/Scripts/Cyclone/CycloneOutcome.cs`
   - `miso/Assets/_Project/Features/Player/Lucy/Scripts/Cyclone/CycloneEntity.Steer.cs`
   - `miso/Assets/_Project/Features/Player/Lucy/Scripts/Editor/CycloneCastOnEnemyTests.cs` + `.meta`
   - `miso/Assets/_Project/Features/Player/Lucy/Scripts/Editor/CycloneSteerTests.cs`

Do not stage `PreloadScreen.unity`, `ProjectSettings/*` or the TMP fallback font (THJ's).

## Other branches

None (scope: `thj/cyclone`).

## How to see it

1. Test Runner, EditMode: run `CycloneCastOnEnemyTests` (19 green), then Run All: only `AIRegressionTest.Baseline_MatchesCurrentAI` red (inner 43); a GridToLevel `m_LockCount` failure, if one shows, is the known flaky assert.
2. Play a level with Lucy and some Claws. Pick the Cyclone cast: the highlight now covers empty cells and the Claws that can be shoved; a Masher, the Queen, family members, allies and cells with spikes or webs are not highlighted.
3. Hover a Claw 2 cells straight above Lucy: the dimmed cross sits on the Claw's cell, the Claw's ghost stands one cell further up with a tether and the Whirl's damage on the ghost's bar (skull if lethal). With spikes on that cell, an orange ring under the ghost. An enemy two out on an arm of that cross shows its pull ghost too.
4. Hover a Claw diagonally next to Lucy: the ghost goes sideways (along the row); put something on that side cell and it goes up or down instead; block both and the cell isn't offered.
5. Click: the Claw glides one cell, lands (spikes fire, Linda's Watch answers if it lands in her lane, an Unaware Claw wakes), the Cyclone appears on the cell it left, pulls and hits it with the others beside it.
6. Hover a Claw that can't be shoved (wall or unit behind it): no highlight, no preview, and the click does nothing.
