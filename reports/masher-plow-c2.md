# Report: Masher plow, C2 (runtime, preview, asset, tests)

Plan: plans/2026-11-18-masher-plow-tech.md    Agent: miso-implementer (opus)    Branch: main
Outcome: built, review fixes applied, EditMode-verified. THJ declined the Linda fix (a known gap, see Hard stop). One stray asset re-save must stay out of the commit. Not play-checked.

## Review fixes (reports/masher-plow-c2-review.md)

1. **Must fix, walk budget:** a plow candidate now also passes `MasherPlowGrid.StepFitsWalkBudget(Unit.CurrentCell, cell, _walk.Parameters.radius, ignorePathCost)`. That is `GridPathFinding.PathFitsBudget` on the one-cell anchor path, the rule the walk's `AEffectTransporter` applies. `ignorePathCost` is read from the walk's move effect (`AEffectTransporter`, or `AEffectCommand`), the same way `PlayerController.GetMoveBudget` reads it. A plow cell the walk would refuse (a costly hazard) is no longer a candidate.
2. **Should fix 1:** `MasherPlowGrid.CanEnter` is now built on `mover.IsFootprintEmpty(cell)`, the check the push's path search runs, so a dead walk-blocking planted entity is refused as the push would refuse it. It keeps the provoker exception (a cell the provoker stands on counts as free if it holds no stash and no walk-blocking plant). Its `mover` parameter is now `GridPluggableEntity`.
3. **Should fix 2:** the tag check moved to `MasherPlowGrid.CanBePushed(unit, query)` (the handler calls it). Two new tests read the **real** `plowPushableTagQuery` from `Unit_MasherGoblin.prefab` and check it on units whose tag set is filled in edit mode. A unit tagged `EntityState.Unmovable` is refused (and classified as Blocker); a unit with another tag is accepted. The tag registry loads from Resources in edit mode, so no stand-in was needed.
4. The `StopPlow` comment now says what really happens: a push in flight runs on the Masher's GUnit, so tearing the Masher down mid-push stops it too and may leave the shoved unit unplugged between cells (teardown only).

New tests for these: `CanEnter_DeadPlantedEntityThatBlocksWalking_False_LikeThePush`, `StepFitsWalkBudget_PlainCell_FitsARangeOfOne`, `StepFitsWalkBudget_CostlyHazard_RefusedUnlessTheBudgetCoversIt` (hazard cost 2: refused at budget 1, fits at 2, fits with path cost ignored), `StepFitsWalkBudget_NoRangeOrNoCell_False`, `PrefabQuery_RefusesAnImmovableUnit`, `PrefabQuery_AcceptsAUnitWithoutTheImmovableTag`. `MasherPlowGridTests` now has 24 tests. The handler-level `TryPlanAnswer` wiring has no test (the reviewer accepted that; the play check covers it).

## Built

- **Planning** (`.Plow.cs` `AddPlowCandidates`, called from `TryPlanAnswer` in `.Counter.cs`): after the walk's own (free) cells, the handler builds its own four one-cell cardinal candidates from the anchor (the walk's cell list drops occupied cells; its range is not widened: candidates need `_walk.Parameters.radius >= 1` and pass the same Crippled feasibility gate as before). Only steps whose footprint is not empty and whose `MasherPlowRules.Plan` is Allowed with at least one push are added. They go after the free candidates, so `RankStep` (ties go to the earlier candidate) keeps picking a free step on a tie; a plow step ranks like a free one (walk length 2, the path length `FindPathTo` gives a free one-cell step). The pick's push list comes back through a new optional `pushes` list. `provokerCells` = the target footprint coordinates. With `plowPusher` empty the handler plans exactly as before.
- **Grid lookups** (`MasherPlowGrid.cs`, new public static class so tests can reach it): `Classify` (no cell, stash, walk-blocking planted entity, non-unit occupant, multi-cell unit, unit refused by the pushable query = Blocker; single-cell unit = PushableUnit with list-index id; empty, the Masher itself, or the provoker = Empty) and `CanEnter` (cell exists, no stash or blocking plant, no occupant other than the mover or the provoker). The Masher's own cells are occupied by it, so `CanEnter` refuses them. The provoker counts as free because in the real answer the rules reject its cells first, and in the hover preview the striker leaves its current tile.
- **Immovable**: new serialized `GTagQuery plowPushableTagQuery` on the handler (set to None of `EntityState.Unmovable`, the same shape as the other pusher assets' target queries). `AEffectPusher.TryMoveTo` checks no tags itself.
- **Answer** (`Activate` in `.Counter.cs` + `StartPlow`/`PlowIE` in `.Plow.cs`): `PrepareTargets` stores the plan's pushes; `Activate` hands them to `StartPlow` when there are any (otherwise the walk runs as before). `PlowIE` re-plans first; if the step cell or the push list changed, no step (the existing `Attack()` path slams only if already adjacent). Otherwise every push starts at once with `plowPusher.TryMoveTo(owner = Masher, ...)`, then it waits, then walks if the step footprint is now empty, else no step.
- **Abort safety**: the wait ends when every started push called `onFinished`, or its unit is destroyed or dead, or after 600 frames counted only while `timeScale > 0`. Every exit calls walk or `Attack()`, both of which end in `Finish` → `onCompletion` (clears `_answerRunning` through the pump's callback). `StopCounter` calls `StopPlow()`, which stops the wait and finishes the answer without acting (`Finish(false)`) so the controller is not left in progress; pushes already moving finish on their own (their coroutine runs on the Masher's GUnit, the same GameObject).
- **Preview** (`.Preview.cs` + `.Plow.cs`): `PlanAgainst` passes the striker as provoker and a push list (same `TryPlanAnswer` as the answer). When the picked step plows: each pushed unit's own move ghost on its destination, facing the push, plus a one-cell path highlight from its tile; the Masher's path is drawn as its one-cell step (its `FindPathTo` would fail into occupied cells). All cleared in `ClearReactionPreview` (`ClearPushPreview`).
- **Asset**: `MasherCounterPresetBuilder` gains `Tools/Masher/Build Plow Pusher`: creates `MasherGoblin_Ability_Counter_Effect_Push.asset` (AEffectPusher: speed 5, distance 1, PushAgainst, straight only, `onMoveEffects` empty, no tag queries) and sets the prefab handler's `plowPusher` and `plowPushableTagQuery`. Run once in the editor.
- **No new statics.** No change to `AEffectPusher`, `FactionRoleProvocationSuppression`, `FactionRoleHandlerBase` or any Family Role handler.

## Verified

- After the review fixes: compiles clean (assemblies rebuilt 18:53, no compile errors in the console).
- Full EditMode suite after the review fixes (Unity MCP): **2000 of 2001 passed**. The only failure is the known red `AIRegressionTest.Baseline_MatchesCurrentAI`. The first run, before the fixes, was 1994 of 1995. The console after the run shows only errors that other suites' tests log on purpose (`listener failed`, `Can't remove GUnit ...`, `Unsupported type Vector2f`, abilities without targets, the AI regression report). None come from the Masher files.
- Builder ran: logs "Built ..." and "Set the plow pusher and pushable query ...".
- New tests `Editor/MasherPlowGridTests.cs` (24: the 18 below plus the 6 review-fix tests above): Classify (empty, missing cell, single-cell pushable with stable ids, refused unit, multi-cell on every cell, Downed unit pushed, stash, provoker cell empty), CanEnter (empty / missing / off-grid, other unit, the Masher's own cells, provoker cell), and with `MasherPlowRules.Plan` on a hand-built grid for a 2 x 2 Masher: free path, two units on the leading edge each to its own next cell, push into the grid edge, no chain push, Immovable blocks, push onto the striker's predicted tile refused, striker's current tile counts as free.

## Not verified (needs the play check)

- Pushes actually moving in play, timing, the walk following, and the slam afterwards.
- Preview ghosts and path arrows for pushed units, and that they clear.
- Toggle on and off with Linda, Mark, John nearby (see Hard stop).
- Abort paths (a pushed unit dying or being destroyed mid-push; disabling the Masher mid-push).
- AC1 "free path exactly as before" is held by construction (plow candidates only exist when the footprint is occupied, and come after free ones) and by the unchanged suite; not watched in play.

## Hard stop: pushed units and Family Roles with the toggle on

**THJ's answer (2026-11-18): declined the additive Linda fix; this is a recorded known gap. Nothing built outside the Masher's files.** Analysis kept below for the record.

How roles see the pushes: `AEffectPusher` raises `unitStartMoving`/`unitMoveTileStep`/`unitEndMoving`; these become flow events with `obj` = the moving unit. Of the family, only **Linda** triggers on a move (`triggerEvents: 64`, OnUnitEndMoving, `WaitForProcessesToComplete`); John triggers on action start (pushes raise none), Mark and Lucy on action complete (pushes are not actions). Because the Masher's controller is in progress for the whole answer, Linda's check for a pushed unit is deferred until the answer ends, and runs then with the same session log as the check for the Masher's own step.

- **Toggle off:** covered with no new code. At that deferred check the last action is the answer's walk or slam, both already listed in `FactionRoleProvocationSuppression`, so Linda does not fire for a pushed unit. (Rare gap: if the pushes happen but the walk does not follow and no slam runs, the last action is the provoker's, so a pushed goblin in her lane could draw a shot.)
- **Toggle on (the prefab default):** a pushed **enemy** that ends in Linda's lane can draw her lane shot when the Masher itself does not (her wait list checks the Masher's step first). `InvolvesSuppressedAction()` ignores which unit moved, so nothing in the Masher's files can block the pushed unit's check without also blocking the Masher's step, which the toggle allows. Pushed player units never trigger her (she shoots enemies only).

Options (none built):
1. Additive per-unit suppression: `FactionRoleProvocationSuppression.SuppressMover(GUnit)` / `IsMoverSuppressed(GUnit)` (main thread, reset in `ResetPlayModeState`), the Masher lists its pushed units from push start until the flow next settles, and Linda's `CheckTriggerConditions` adds `obj is GUnit u && IsMoverSuppressed(u)` → false. Small, explicit; touches a core helper (additive) and Linda's handler. **My recommendation.**
2. Same idea, but Linda's handler asks the Masher's handler directly. Couples a family handler to an enemy; worse.
3. Move pushed units with a Masher-side mover that raises no move events. Keeps every change in the Masher's files but breaks listeners that refresh on `unitEndMoving` (role zones, Lucy's shelter, Linda's quiver aim, enemy alerts, John's Command Shield Dash passive). Not recommended.
4. Accept the gap for now (only toggle on, only a pushed enemy ending in Linda's lane while the Masher's own step is not).

## Findings

- **Stray re-save, leave out of the commit:** the builder's `AssetDatabase.SaveAssets()` also saved `Resources/UnitSpecific/Enemy/Masher Goblin/Move/MasherGoblin_Ability_Walk.asset`, which Unity had dirty in memory (new default fields `autoMoveAllowed`, `allyTargetTagQuery`, `ghostSource`, `affectedAreaPreviewSprite`; empty `entityID`s filled with `Specs_Health` in unused stat references). It looks behavior-neutral, but it is not part of this work. My attempt to restore it from HEAD was refused by the permission system. It is still modified in the working tree; the coordinator will ask THJ about discarding it. Do not stage it.
- **Prefab diff** (`Unit_MasherGoblin.prefab`, the handler component): the two new fields (`plowPusher` → the new asset, guid `9663d4486ffdf1d438a6b4406e40af30`; `plowPushableTagQuery` = policy 2 (None) with one entry `EntityState.Unmovable`, Self, Present), plus two lines Unity added to the handler's `qTEProfile` on re-save (`preloadOverride: -1`, `showSpeed: 1`: fields that exist in `QTEProfile` but were never serialized for this prefab). Nothing else changed; LF kept.
- Downed units keep their cell (`IsAlive` stays true), so they are pushed (plan default). Dead units are unplugged; a stashed body on a cell blocks it.
- The footprint is a plain translation of the anchor (`GridPluggableEntity.FootprintCoords`), so the anchor delta is the footprint shift.
- Preview approximation: the slam's damage preview still reads the grid as it is now, so a pushed unit that would end inside the slam cross is not shown as hit (and one leaving it may still be shown).
- `AEffectPusher.IsInProgress` is shared on the asset; with two concurrent pushes it reads false after the first ends. Nothing reads it for this asset.

## Not done / remaining

- Re-review of the four fixes (optional, coordinator's call).
- The play check (THJ's time): goblin and family member in the way, wall and grid edge, two units on the leading edge, an Immovable unit (another Masher or the Deev), toggle on and off with Linda in lane.
- Docs (coordinator): enemies.md, combat-rules.md CR-18 note, combat-architecture.md, the design plan's revision note, decisions, build log, status, branches.md (`thj/cyclone` will conflict in `.Counter.cs` `TryPlanAnswer`/`Activate`).
- Review (miso-reviewer).

## Changed files (all under `miso/Assets/_Project/`)

Code:
- `Features/Enemy/Masher Goblin/Scripts/MasherGoblinFactionRoleHandler.Plow.cs` (new, no BOM, LF, like the other handler partials)
- `Features/Enemy/Masher Goblin/Scripts/MasherGoblinFactionRoleHandler.Plow.cs.meta` (new)
- `Features/Enemy/Masher Goblin/Scripts/MasherPlowGrid.cs` (new, BOM, LF; `Classify`, `CanEnter`, `CanBePushed`, `StepFitsWalkBudget`)
- `Features/Enemy/Masher Goblin/Scripts/MasherPlowGrid.cs.meta` (new)
- `Features/Enemy/Masher Goblin/Scripts/MasherGoblinFactionRoleHandler.Counter.cs` (header line; `StopCounter` calls `StopPlow`; `PrepareTargets` stores pushes; `Activate` runs `StartPlow` when the step plows; `TryPlanAnswer` overloads gain `provoker` and `pushes`, plow candidates appended)
- `Features/Enemy/Masher Goblin/Scripts/MasherGoblinFactionRoleHandler.Preview.cs` (header line; push list through `PlanAgainst`; plow path and push ghosts; clear)
- `Features/Enemy/Masher Goblin/Editor/MasherCounterPresetBuilder.cs` (new menu `Tools/Masher/Build Plow Pusher`)

Tests:
- `Features/Enemy/Masher Goblin/Editor/MasherPlowGridTests.cs` (new, BOM, LF)
- `Features/Enemy/Masher Goblin/Editor/MasherPlowGridTests.cs.meta` (new)

Assets (made by the builder):
- `Resources/UnitSpecific/Enemy/Masher Goblin/Attack/MasherGoblin_Ability_Counter_Effect_Push.asset` (new)
- `Resources/UnitSpecific/Enemy/Masher Goblin/Attack/MasherGoblin_Ability_Counter_Effect_Push.asset.meta` (new)
- `Features/Enemy/Masher Goblin/Prefabs/Unit_MasherGoblin.prefab` (diff above)

Not mine, do not stage: `Resources/UnitSpecific/Enemy/Masher Goblin/Move/MasherGoblin_Ability_Walk.asset` (stray re-save, see Findings). Pre-existing before this session: the TMP fallback font asset and `miso.slnx`.

## Proposed commits

1. `feat(masher): the counter step shoves units in its way one cell onward, with a preview of where they land` — all code, test, asset and prefab files above (they only work together: the prefab references the asset, the handler needs both fields). Touches a core-systems line (Masher counter); no shared Core code changed.

## Save reset

no

## How to see it (after the play check is agreed)

1. Open a level with a Masher Goblin; stand a goblin (or a family member who is not the attacker) on a cell the Masher's 2 x 2 would enter when stepping one tile toward your attacker, with the cell beyond it free.
2. Select the attacker, aim at the Masher, hover it: the Masher's step ghost, and the shoved unit's ghost one tile onward with a path arrow.
3. Attack: the unit slides one tile, the Masher steps in, then slams if adjacent. The shoved unit takes no damage.
4. Repeat with the cell beyond blocked (wall, grid edge, another unit), and with an Immovable unit (another Masher, the Deev) in the way: no shove, the Masher picks another step or stays.
5. With Linda's lane covering where a shoved goblin lands: toggle off, no shot; toggle on, see the hard stop.
