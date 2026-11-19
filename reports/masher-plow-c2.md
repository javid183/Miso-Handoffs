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

---

# C3: overlap (shove and step together)

Approved by THJ 2026-11-18 after playing C2 (committed as `62ed9b895`): "overlap only", no new animation. Outcome: built and EditMode-verified, nothing committed, not play-checked. No scene, prefab or asset changes; no Play mode.

## Investigation (step 1)

- **(a) When a shoved unit leaves its cell:** at once, inside the `TryMoveTo` call. `StartMove` → `owner.StartCoroutine(MoveEntity(...))` runs synchronously up to its first `yield`. Before that yield it raises `unitStartMoving` and calls `entity.CurrentCell.UnplugEntity(entity)`. The unit is plugged into its destination only at the end of its slide (`path[i + 1].PlugEntity`).
- **(b) When the walk reads the step's cells, and when the Masher moves:** also at once. `MasherGoblin_Ability_Walk` is `activationMode: 1` (InstantAnimated) with no minimum duration or wait. So `Orchestrator.ActivateAbility` → `RuntimeAbility.Activate` → `_ActivateAbility` → `StartCoroutine(preset.Activate(...))` → `ApplyMapped` → `AEffectTransporter.ApplyUnguarded` all run in the same call, with no animation-frame delay. `ApplyUnguarded` finds its path right then (`FindPathTo(..., mover)`; `goShortestWhileWalkable: 0`, so the goal needs `IsFootprintEmpty`) and checks the budget. Its `MoveEntity` (started synchronously, no start-tile effects) checks `IsFootprintEmpty` and `IsFootprintWalkable` for the last step again before the first lerp frame, then moves. The Masher starts moving in that same frame. If the cells are not free, the transporter returns early (no path) or plugs the Masher back and ends the move. Either way its completion still fires, so the answer cannot get stuck.
- **(c) Before or only after the pushes?** **Only after the pushes have started.** The walk reads the cells the moment it is activated, and they are free only once each shoved unit's `TryMoveTo` has run. It can start in the very same frame as the pushes (lead 0), but never before. So I made the lead a single non-negative value; a negative value is clamped to 0.
- Speeds, for the play check: the pusher asset slides at speed 5 (one tile in about 0.2 s); the Masher's transporter walks at 2.5 (about 0.4 s). With the overlap, the shoved unit moves ahead faster than the Masher follows. If THJ wants them to move as one block, set the push asset's `speed` to 2.5 (one number on `MasherGoblin_Ability_Counter_Effect_Push.asset`; not changed here).

## Built

- `MasherPlowTiming.cs` (new, pure): `MasherPlowWalkState` (NotStarted, Skipped, Running, Done), `MasherPlowNext` (Wait, StartWalk, Continue, FinishWithoutActing), `ClampLead`, `MaxWaitSeconds = 10`, `TimedOut(elapsed)`, and `Next(allPushesStarted, pushesDone, walk, elapsed, lead)`. The walk starts once the lead has passed, or as soon as every push has ended. The answer goes on only when the walk is done or skipped *and* every push has ended. If a push failed to start, the walk never starts and the answer goes on once the started pushes end. A tripped guard always ends the answer without acting.
- `.Plow.cs`: new `[SerializeField, Min(0)] float plowWalkLeadSeconds = 0.05f`, with a tooltip saying why it can't be negative. The prefab has no saved value, so it takes the default; no prefab change. `PlowIE` now re-plans (unchanged), starts the pushes (unchanged), then loops on `MasherPlowTiming.Next`. At StartWalk it checks `Unit.IsFootprintEmpty(stepCell)` (unchanged rule: a unit that did not leave means no step) and starts the walk with a callback that marks it ended. At Continue it calls the slam step (`Attack`, which checks adjacency). At the safety stop it ends the answer without acting. `elapsed` counts game time (summed `Time.deltaTime`, like the slides; it stays 0 while paused). The safety stop covers the whole push and walk wait, and trips at `MasherPlowTiming.MaxWaitSeconds` (10 s) of that game time. This is the reviewer's should-fix: the old 600-frame guard could trip after 1 to 2 s at 300 to 500 fps, while the walk was still running, and end the answer mid-walk with no slam. The frame counter and `PlowWaitMaxFrames` are gone. `StartPlow` now takes the walk as `Action<Action>` (start the walk, with what to do when it ends).
- `.Counter.cs` (one small edit in `Activate`): the local `Walk` takes its completion callback. The normal path calls `Walk(Attack)` (same as before); the plow path passes `Walk` to `StartPlow`.
- Unchanged: the plan, re-plan, push list, preview, role handling, `StopCounter` → `StopPlow` (stops the wait and ends the answer without acting; a walk still running then ends on its own and only sets a flag nobody reads), and the no-step fallback.

Default lead 0.05 s: the slides take about 0.2 s, so the Masher starts after about a quarter of the slide, while the units are still clearly moving. 0 is safe too (same frame).

## Verified

- After the safety-stop fix: compiles clean (assemblies rebuilt 19:40; no Masher errors in the console).
- Full EditMode suite in the open editor after the fix: **2015 of 2016 passed**. The only failure is the known red `AIRegressionTest.Baseline_MatchesCurrentAI`. The run before the fix was 2012 of 2013.
- New `Editor/MasherPlowTimingTests.cs` (15 tests). The safety-stop tests now work in seconds: `TimedOut` at exactly `MaxWaitSeconds` and not before; the stop is at least 5 s; at the stop every walk state ends the answer without acting (pushes started or not, done or not); just before the stop a running walk still waits. The other tests are unchanged: lead clamp; waits before the lead; starts at the lead; lead 0 starts in the same frame; a negative lead acts as 0; pushes ending before the lead start the walk at once; waits while the walk runs; waits for the pushes after the walk is done; goes on when both are done; a skipped walk goes on once the pushes end; a failed push start never walks and goes on once the started pushes end.

## Not verified (only a play check can show)

- Whether it reads as a bulldozer: the Masher visibly carrying the units ahead of it, and whether 0.05 s (or 0, or matching the push speed to 2.5) looks best.
- Whether a unit ever ends up under the Masher, or the two sprites overlap mid-slide. By the code it can't end under it: the shoved unit's destination is beyond the Masher's new footprint, and both cells are reserved by the plan. Mid-slide overlap is purely visual and depends on the two speeds (with the current 5 vs 2.5, the unit stays ahead).
- Two units on the leading edge sliding together while the Masher steps; the slam right after the step.
- Abort paths in play (a shoved unit dying mid-slide; the Masher disabled mid-step).

## Findings

- The C2 order (wait for every push, then walk) was never needed for correctness: the cells are free the moment the pushes start.
- A walk started too early can't stall the answer. The transporter ends a blocked move gracefully and still completes, and the plan also checks the footprint just before starting it.
- Family Roles: no change. The pushed units' `unitEndMoving` events now fire while the Masher is walking, still inside the answer, so Linda's deferred check still runs after the whole answer, as before (toggle off: suppressed; toggle on: the known gap).

## Files (C3, all under `miso/Assets/_Project/Features/Enemy/Masher Goblin/`)

- `Scripts/MasherPlowTiming.cs` (new, BOM, LF) + `Scripts/MasherPlowTiming.cs.meta` (new)
- `Scripts/MasherGoblinFactionRoleHandler.Plow.cs` (lead field, `StartPlow` signature, `PlowIE` loop with the game-time safety stop, header comment; `PlowWaitMaxFrames` removed)
- `Scripts/MasherGoblinFactionRoleHandler.Counter.cs` (`Activate`: `Walk` takes its completion)
- `Editor/MasherPlowTimingTests.cs` (new, BOM, LF) + `Editor/MasherPlowTimingTests.cs.meta` (new)

Proposed commit: `feat(masher): the counter step walks while the units it shoves are still sliding, so it carries them ahead of it` (all six files; they only work together).

## How to see it

1. Same setup as C2: a unit in the Masher's way with a free cell beyond, provoke the Masher.
2. The unit starts sliding and the Masher starts its step a moment later (0.05 s), so both move together; then the slam if adjacent.
3. To tune: on `Unit_MasherGoblin` › Masher handler › Counter step plow › **Plow Walk Lead Seconds** (0 = same frame). For a "one block" look, set **Speed** on `MasherGoblin_Ability_Counter_Effect_Push` to 2.5 (the Masher's walk speed).
