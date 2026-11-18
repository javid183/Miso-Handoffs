# Report: Cyclone round 2, C4 (cross drawing and previews) + heavy wobble

Plan: plans/2026-11-17-cyclone-round2-tech.md (chunk C4; design plans/2026-11-17-cyclone-round2-design.md §4 B, §4 C, §5 UX, §9; wobble D-558, Cyclone-only)    Agent: miso-implementer    Branch: thj/cyclone (on top of the uncommitted C1, C2, C3a, C3b, C3c)
Outcome: done (compiled in the open editor through the Unity MCP; EditMode run, see "Test run"). No core file touched; no asset or prefab edited.

## What changed

All under `miso/Assets/_Project/Features/Player/Lucy/Scripts/`. LF, no BOM, like HEAD and the neighbours (checked byte by byte).

New (each with its `.meta`):
- `Cyclone/CycloneOutcome.cs`: `CycloneOutcome` (per moving enemy its path start..final cell, the enemies hit, `LandsOnPlanted`) and `CycloneOutcomePlanner.ForCast(center, ...)` / `ForSteer(plan, ...)`. `ForSteer` takes the carry plan (`AEffectCycloneSteer.PlanFor`, the one plan the Steer executes), then plans the closing Whirl's pull and hit on the board that plan leaves (`plan.OccupantOf`, the start cell counted as free of the Cyclone). Pure (grid slots and predicates).
- `Cyclone/CycloneOutcomeView.cs`: draws an outcome: one ghost per moving enemy (final cell only, `GUnit.ShowGhostAt`), a faint tether in the eye tint along its way (one soft bar per step), the hit's damage segment through `GUnit.ShowDamagePreview` (the bar draws the lethal skull itself), an orange ring under a ghost whose landing cell has something planted. For a moved and hit enemy its own `EntityInfoPanelUI` transform is offset onto the ghost while shown and put back on `Clear`. `Apply()` re-draws every frame; `Clear()` removes everything; `Dispose()` releases its sprites.
- `Cyclone/CycloneHitPreview.cs`: the damage of one Cyclone hit on a unit, modelled on `AbilityDamagePreview` (health modifiers of the hit compound and its unlocked nested compounds, `AbilityDamagePreview.SimulateApply` with the cast's stats and the unit's tags, guaranteed reductions, `NormalizeValueChange`). Crit not previewed, as everywhere. `AbilityDamagePreview` is called, not edited.
- `Cyclone/CycloneCastPreview.cs`: the cast's aim preview (cross at the aimed cell, dimmed; ghosts and tethers for pulled enemies; damage and skull on the ghost, or on the enemy itself when hit where it stands). Bound to `abilitySelectEnteredTargetSelection`, `abilitySelectCancelTargetSelection`, `abilityStarted`, `gridCellHovered`, `levelEnded`. Lives on the level's event bus object (see the next file).
- `Cyclone/CycloneCastPreviewAttach.cs` (fix round): a hidden `DontDestroyOnLoad` watcher made once per Play session at `AfterSceneLoad` (skipped if one exists; no static field). Each frame it compares `GlobalEventBus.Instance` with the last bus it saw and adds `CycloneCastPreview` to each new one, so the preview is there in the normal flow where `ProgramFlowHandler` instantiates the level (and its bus) after the scene loads.
- `Cyclone/CycloneAimState.cs`: pure dim state (not aiming: Normal; aiming: Dimmed; a Steer landing under the cursor: the cross Hidden at the Cyclone and Dimmed at the landing).
- `Cyclone/CycloneCursor.cs`: the cell under the mouse, read like `GridManager.HandleHovering` reads it (`PlayerInputController` mouse world position, `GridManager.GetCell(Vector3)`, nothing over the screen-space HUD using `GridManager.BlocksGridHover`). Read-only; no `GridManager` change.
- `Cyclone/CycloneWobble.cs`: `CycloneWobble` (component) and `CycloneWobbleRules` (`PathCrosses`, `AnyHeavyHeadedThrough`, `HeadsThrough`, `IsHeavyEnemy`, `MoveRange`).
- `Editor/CyclonePreviewTests.cs` (17 tests after the fix round) and `Editor/CycloneSteerTests.Preview.cs` (7 tests, a partial of `CycloneSteerTests` to reuse its recorders).

Changed:
- `Cyclone/CycloneCrossView.cs`: rewritten drawing. One swirl tint (blue-cyan, alpha 0.3) on each touching cell, one inward chevron on each arm tip, no label, no streaks; `ShowAt(center, armLength)` so the previews draw their own copy; `SetLook(Normal | Dimmed | Hidden)` (new enum `CycloneCrossLook`); test read-outs `TintCellsDrawn`, `ChevronCellsDrawn`, `Center`. Beat kept: Streaks flares the chevrons, Burst plays the ring and resets them, Done resets. `BurstTime` is now `CycloneEntity.BurstSeconds` (one constant).
- `Cyclone/CycloneSprites.cs`: `Streak()` (only the cross used it) replaced by `Chevron()`; added `Swirl()` and `Line()`. All made in code and released through `CycloneSprites.Release` by their owners.
- `Cyclone/CycloneRules.cs`: `TouchLabel` removed; `ArmTips(center, armLength)` added.
- `Cyclone/CycloneEntity.cs`: serialized field `whirlHitTimes` and `WhirlHitTimes` removed (only the label read them); header comment; adds and binds `CycloneWobble`, unbinds it in `Dispose`.
- `Cyclone/CycloneWhirlPlanner.cs`: additive optional `occupantOf` on `PlanPulls`, `IsLandable` and `HitTargets` (null reads the grid exactly as before). With an override a unit counts where the board puts it and the cell it leaves is freed for the ones behind.
- `Cyclone/CycloneSteerPreview.cs`: reworked. Plans from `AEffectCycloneSteer.PlanFor` and `CycloneOutcomePlanner.ForSteer`; path arrows (`HighlightPath` of the plan's path, so a way round is drawn as it is taken), Cyclone copy and cross at the landing cell, ghosts, tethers (the step arrows are gone), damage on ghosts, landing hazards. Dims the cross for any Cyclone cast aim or this Steer's aim, hides it while the landing cross shows. First frame: `OnEnteredTargetSelection` arms a one-shot; the first `LateUpdate` in which the Steer is really being aimed draws the cell under the cursor if no hover drew one. Removed on cancel, `abilityStarted`, `levelEnded`, when the Cyclone can no longer be steered (burst, spent) and on `Unbind` (Dispose). Public `Preview(effect, cell)`, `Stop()`, `DamageOf` (test seam), read-outs `Aim`, `Plan`, `Outcome`, `PathShown`, `View`, `LandingCross`.
- `Cyclone/CyclonePipsView.cs`: `SetFlicker(bool)` (pips left fade 1 to 0.25 and back, 4 times a second; spent pips unchanged); `Hide` stops it.
- `Editor/CycloneCastTests.cs`: the `TouchLabel` and `WhirlHitTimes` asserts removed (the 3x hit value is still asserted through the prefab's compound).

## Acceptance criteria (C4 part of the plan: cross drawing, cast preview, Steer preview, one planner; plus the wobble from the AI criterion)

- [x] Cross drawing: tint on the 4 touching cells in a cool hue, one inward chevron per arm tip, no label, no streaks on touching cells: `Cross_TintsTheFourTouchingCells_ChevronsTheFourArmTips_AndWritesNoNumber` (exact cell sets, 8 children only, no TMP text, tint blue > red + 0.3 and alpha < 0.5), `Cross_AtTheBoardEdge_DrawsOnlyTheCellsThatExist`, `ArmTips_AreTheFarCellOfEachArm_PointingBack`. Look in play: play check 1 to 4.
- [x] The cross dims during any aim preview; during a Steer aim it is drawn at the landing cell only: `AimState_DimsWhileAiming_MovesTheCrossToTheLanding_AndComesBack`, `Cross_DimsAndHides_ByLook`, and in the Steer preview test (`Aim.CrossLook` Hidden, landing cross at the landing cell, Dimmed). "Any aim preview" is read as the plan lists it: the Cyclone cast's and the Steer's target selection (see Decisions).
- [x] Cast aim preview: cross at the aimed cell, a ghost per pulled enemy, damage and skull on the ghost (enemy pulled from 2 out shows it on its ghost), on the enemy itself when beside: `CastPreview_GhostsForPulledEnemies_TheHitOnTheGhost_AndNothingLeftAfterwards`. Live wiring and the bar on the ghost: play check 5 to 10.
- [x] Steer aim preview: only reachable cells (the range highlight from C2, unchanged), path, landing Cyclone, one ghost per moving enemy (carried or pulled, final cell only), tether replaces the arrow, damage on the ghosts, landing hazard shown: `SteerPreview_GhostsStandWhereTheExecutedSteerLeavesEveryone_AndTheHitMatches` (side rider onto spikes, front enemy shoved, Whirl pull after the carry; hazard ring on the rider's landing). Detour: `SteerPreview_ACellPastABlockedFront_ShowsTheWayRoundThePlanTakes`. Unreachable cell: `SteerPreview_ToACellItCantReach_DrawsNothingButTheDimmedCross`.
- [x] Drawn at once when the cursor already sits on a cell as the Steer is picked: built (one-shot resolve from the cursor in `LateUpdate`, no core change). Not unit-testable (mouse and camera); play check 18.
- [x] Previews survive the player's own hover refresh: ghosts, carried health bars, damage and path arrows re-applied every `LateUpdate` while aiming (after the controller's hover handlers, which run in `Update`). Play check 19.
- [x] Fully removed on cancel, click, level end, Cyclone spent or burst, Dispose; no leaked subscriptions: `SteerPreview_LeavesNothingBehind_WhenTheAimEnds` (cancel, click, level end, unbind: no path, ghost, damage, hazard, tether objects, landing copy or landing cross; aim over; after Unbind the bus no longer reaches it). Burst or spent: `LateUpdate` stops the preview when `CanBeSteered` turns false (play check).
- [x] One planner, plan equals preview equals execution: the Steer preview test compares `PlanFor`'s path and carry landings with what is drawn, then runs the real `SteerRoutine` with the recorders and checks every unit ends on its ghost's cell and the Whirl hits exactly the units the preview marked.
- [x] `PlanPulls` occupancy override: `PlanPulls_ReadsTheBoardItIsGiven` (pulled into a cell the carry emptied; a carried unit pulled from where the carry left it; `HitTargets` on the same board). Without the override nothing changes (all existing Whirl, Steer, carry and burst tests still pass).
- [x] Preview damage numbers: `HitPreview_ThePrefabsHit_PreviewsThreeFourFiveByCyclonePower` (3 cases): the prefab's real hit compound through `CycloneHitPreview` and `SimulateApply`, with a stat context that applies the cast asset's Stat_DMG level factor and policy through `AAttributeModifier.ModifyWithPolicyBasic` and the family's damage cap (9999), Lucy's damage 1: 3 / 4 / 5. Not the full runtime stat set (see Decisions).
- [x] HP bars show the Whirl hit only: the view only ever shows `CycloneHitPreview`'s hit value; nothing adds Watch or hazard damage.
- [x] `BurstSeconds` and the cross's burst length are one constant: `TheCrossBurstRing_LastsAsLongAsTheBurst`.
- [x] Wobble (Cyclone-only): `Wobble_PathCrosses_OnlyWithinTheMove`, `Wobble_AHeavyEnemyHeadedThroughWithinItsMove_Qualifies` (real mover-aware `FindPathTo` through the Cyclone, range 3 yes, range 2 no), `Wobble_ALightEnemy_NeverQualifies`, `Wobble_AHeavyOfTheFamily_NeverQualifies`, `Wobble_ASpentOrGoneCyclone_NeverQualifies`. The motion and the pip flicker: play check 34.
- [x] Compile clean; EditMode: see "Test run".

## Test run

- Before (C3c report): 2090 run, 2089 passed, 1 failed (the known red, inner `CHECKS: 714 FAILURES: 43`).
- Subset after: `CyclonePreviewTests` + `CycloneSteerTests` 75 / 75 passed (earlier also `CycloneCastTests`, `CycloneWhirlTests`, `CycloneBurstTests`, `CycloneLifeTests` with them: all their existing tests passed).
- Full suite after (MCP Test Runner, editor open, no Play mode): **2113 run, 2112 passed, 1 failed, 0 skipped**. The only failure is `AIRegressionTest.Baseline_MatchesCurrentAI`, inner **`CHECKS: 714 FAILURES: 43`** (unchanged). The 23 new tests (16 + 7) make up the difference from 2090.
- Compile: no errors, no warnings from the Cyclone files.

## Save reset

No.

## Decisions I made

- **Damage on the ghost** without touching core: the unit's own world-space health panel (`EntityInfoPanelUI`, under `Visual/UnitInfoHook`) is moved by the ghost's offset while the preview shows and put back on `Clear` (stored local position). Only for enemies that move and are hit. The small health bar under the unit (`MiniHealthBar`) stays on the unit. Tier 1, visual only; flag at play if THJ prefers the bar left on the unit.
- **Landing hazard** shown as an orange ring under the ghost (own sprite, not a cell overlay, so no other preview clears it). Its damage is not added to the bar (only the Whirl's hit is previewed). Every planted entity other than a Cyclone counts, as the grid's plug activates them all.
- **"Any aim preview"** for dimming is the plan's reading: the Cyclone cast's and the Steer's target selection. Dimming during every ability aim (the default move is a target selection too) would dim the cross most of the player's turn.
- **Detour path**: drawn by the grid's own path arrows along the plan's path, which already is the way round; no extra marker.
- **First frame**: resolved from Cyclone code with the input route the grid itself uses (`CycloneCursor`); no `GridManager` accessor needed.
- **Cast preview host**: the level's event bus object, because no Cyclone exists while the cast is aimed and neither Lucy's prefab nor the level prefab is to be edited. Attached by the hidden watcher (fix round; the first build's scene-load hook missed the bus the program flow instantiates later).
- **Wobble**: rotation only (7 degrees, 5 times a second) on the body sprite, no scale, so it never fights the Whirl's swell (which scales the body's parent). Recomputed only on `turnStarted`, `abilityPerformed`, `unitEndMoving`, `unitDied`, `unitBorn`, the Cyclone's `ReadyChanged` (after a Whirl, a Steer, a burst), and only once no Whirl, Steer or burst runs and no faction controller is acting or thinking (the AI's prediction counts as acting), so it never reads the grid while the AI worker plans. Path: the heavy's mover-aware `FindPathTo` to each family unit, shortest kept; crossing = the heavy's footprint covers the Cyclone's cell at a step within its longest move ability's radius (as `UnitThreatAnalysis` reads reach). Stops for good at burst, dispose, level end.
- **`whirlHitTimes` removed** (field and property): only the label read it. `Cyclone.prefab` still holds `whirlHitTimes: 3`; Unity ignores the orphan key and drops it the next time the prefab is saved. Not edited (no prefab change needed), no rename so no `FormerlySerializedAs`.
- **Preview damage test** uses a stat context built from the cast asset's own Stat_DMG level and policy (the same data path as the existing Cyclone Power test) plus the family cap, not `StatBackedEvaluationProbe`: the probe calls `InitializePartially` on the Lucy prefab asset in memory, which I did not want to run inside THJ's open editor from a test.
- Health modifiers of the hit and its unlocked nested compounds are summed into one `SimulateApply` (the game's preview sums per compound). Same result for the Cyclone's subtractive hit; would differ only for a multiplicative nested damage modifier.

## Needs THJ

None.

## Docs to update

- `tech/core-systems.md` (coordinator), Cyclone note: no core change in C4. Cyclone code now moves an enemy's `EntityInfoPanelUI` transform during its previews (restored on clear), and a hidden `DontDestroyOnLoad` watcher adds `CycloneCastPreview` to each level's `GlobalEventBus` object.
- GDD `characters/lucy.md` LU-4 / LU-6 and the UX table (designer, C5): as built: tint and chevrons, aim cross, tether, hazard ring, wobble rule (within one move, path to the nearest family unit).

## Risks and loose ends

- Commit split across shared files: C4 edits four files that already carry uncommitted earlier chunks: `CycloneEntity.cs` (C3b), `CycloneRules.cs`, `CycloneSteerPreview.cs`, `CycloneWhirlPlanner.cs` (C1/C2). The C4-only hunks of those four are saved at `C:\Users\javid\AppData\Local\Temp\claude\9ec5439f3060d705\487fa4a4-94b4-478d-84dc-b8aae3f336a7\scratchpad\c4-shared-hunks.diff` and the pre-C4 copies in `...\scratchpad\pre-c4\` (also `CycloneCrossView.cs`, `CycloneSprites.cs`, `CyclonePipsView.cs`, `CycloneCastTests.cs`, which were clean at HEAD before C4).
- Play-only: the health panel offset on a ghost, the first-frame resolve, the per-frame survival against the controller's hover refresh, and click/hover on an enemy standing on a newly offered Steer cell (play check 18 to 20).
- The wobble reads "a heavy's way to its nearest family unit", not the AI's actual intent (the game has no enemy intent path; D-558 chose this). A heavy that targets another unit, or moves twice, may not wobble it.
- A Steer aim that ends without any of the bus events (the Cyclone bursts mid-aim) clears its drawings in `LateUpdate`; the cross is disposed with the Cyclone anyway.
- `CycloneSteerPreview.OnDestroy` / `CycloneCrossView.OnDestroy` don't run in edit mode, so the tests clean up by `Stop`/`Unbind`/`Hide`; in play they run as before.
- Known core limit (unchanged, from C2): one Watch per action when several riders land in Linda's lane.

## Proposed commits

Order after the C1, C2, C3a, C3b and C3c commits. One commit, plain (Cyclone code and tests only; everything here works together):

1. `feat(lucy): the Cyclone's cross is a cool tint beside it and a chevron on each arm tip; the cast and the Steer preview every move and hit on ghosts; the Cyclone wobbles while a heavy enemy is headed through it`:
   - `miso/Assets/_Project/Features/Player/Lucy/Scripts/Cyclone/CycloneAimState.cs` + `.meta`
   - `miso/Assets/_Project/Features/Player/Lucy/Scripts/Cyclone/CycloneCastPreview.cs` + `.meta`
   - `miso/Assets/_Project/Features/Player/Lucy/Scripts/Cyclone/CycloneCastPreviewAttach.cs` + `.meta`
   - `miso/Assets/_Project/Features/Player/Lucy/Scripts/Cyclone/CycloneCursor.cs` + `.meta`
   - `miso/Assets/_Project/Features/Player/Lucy/Scripts/Cyclone/CycloneHitPreview.cs` + `.meta`
   - `miso/Assets/_Project/Features/Player/Lucy/Scripts/Cyclone/CycloneOutcome.cs` + `.meta`
   - `miso/Assets/_Project/Features/Player/Lucy/Scripts/Cyclone/CycloneOutcomeView.cs` + `.meta`
   - `miso/Assets/_Project/Features/Player/Lucy/Scripts/Cyclone/CycloneWobble.cs` + `.meta`
   - `miso/Assets/_Project/Features/Player/Lucy/Scripts/Cyclone/CycloneCrossView.cs`
   - `miso/Assets/_Project/Features/Player/Lucy/Scripts/Cyclone/CycloneSprites.cs`
   - `miso/Assets/_Project/Features/Player/Lucy/Scripts/Cyclone/CyclonePipsView.cs`
   - `miso/Assets/_Project/Features/Player/Lucy/Scripts/Cyclone/CycloneEntity.cs` (C4 hunks; see Risks)
   - `miso/Assets/_Project/Features/Player/Lucy/Scripts/Cyclone/CycloneRules.cs` (C4 hunks)
   - `miso/Assets/_Project/Features/Player/Lucy/Scripts/Cyclone/CycloneSteerPreview.cs` (C4 hunks)
   - `miso/Assets/_Project/Features/Player/Lucy/Scripts/Cyclone/CycloneWhirlPlanner.cs` (C4 hunks)
   - `miso/Assets/_Project/Features/Player/Lucy/Scripts/Editor/CyclonePreviewTests.cs` + `.meta`
   - `miso/Assets/_Project/Features/Player/Lucy/Scripts/Editor/CycloneSteerTests.Preview.cs` + `.meta`
   - `miso/Assets/_Project/Features/Player/Lucy/Scripts/Editor/CycloneCastTests.cs`

If THJ wants the wobble apart, `CycloneWobble.cs` + `.meta`, the `CyclonePipsView.cs` flicker, the two `_wobble` lines in `CycloneEntity.cs` and the five `Wobble_*` tests can go in their own commit after this one (`feat(lucy): the Cyclone wobbles and its pips flicker while a heavy enemy is headed through it`), but they share `CycloneEntity.cs` and `CyclonePreviewTests.cs` with the rest.

Do not stage `PreloadScreen.unity`, `ProjectSettings/*` or the TMP fallback font (THJ's).

## Other branches

None (scope: `thj/cyclone`).

## How to see it

1. Test Runner, EditMode: run `CyclonePreviewTests` (17) and `CycloneSteerTests` (now 59), then Run All: only `AIRegressionTest.Baseline_MatchesCurrentAI` is red (inner 43).
2. Play a level with Lucy and some Claws: cast the Cyclone. The four cells beside it carry a faint blue swirl, each arm tip a chevron; no numbers.
3. Aim the cast over empty cells: the dimmed cross follows the cursor; an enemy 2 out on an arm shows its ghost one cell in, tethered, with the hit on the ghost's bar (skull if lethal).
4. With the Cyclone out, pick Steer (try it with the cursor already resting on a reachable cell: drawn at once). The old cross dims, hovering a reachable cell moves the cross to the landing; ghosts and tethers for every enemy that moves, damage on them, an orange ring under a ghost landing on spikes. Cancel: everything goes.
5. With a Masher or the Goblin Queen walking toward the family through the Cyclone's cell within one move: the Cyclone wobbles and its pips flicker until it bursts or the heavy no longer heads through.
6. The full list for THJ: `playtests/2026-11-17-cyclone-round2-play-check.md`.

## Fix round

Review: `reports/cyclone-r2-c4-review.md` (verdict FIX). All items done in Cyclone code; no core, prefab or asset edit.

- **Must-fix (cast preview never attached in the normal flow).** The scene-load hook is gone from `CycloneCastPreview`. New `CycloneCastPreviewAttach`: a hidden `DontDestroyOnLoad` object made at `AfterSceneLoad` (once; `FindAnyObjectByType` guards a second), whose `Update` adds the preview to every new `GlobalEventBus.Instance` it sees (one reference compare a frame; `Attach(bus)` adds at most one). No static field. Test: `CastPreview_IsPutOnTheLevelsEventBusOnce`. The live Preload > Home > level path is a play check (added to the list); I did not start Play mode.
- **Should-fix 1.** `CycloneSteerPreview.LateUpdate`: before the empty-path return, if the aim is on and the player controller is no longer selecting a target (End Turn mid-aim, say), `Stop()`: the cross comes back to full.
- **Should-fix 2.** `TheCrossBurstRing_LastsAsLongAsTheBurst` removed (it compared the constant with itself; the cross view reads `CycloneEntity.BurstSeconds` directly).
- **Should-fix 3.** `Assume.That` in `Wobble_ASpentOrGoneCyclone_NeverQualifies` is now an `Assert`.
- **Should-fix 4.** `OutcomeView_CarriesTheHealthBarOverToTheGhost_AndPutsItBack`: a pulled enemy's `EntityInfoPanelUI` moves by the ghost's offset on Show, an enemy hit where it stands keeps its bar where it is, and Clear restores the local position.

Files touched in this round: `Cyclone/CycloneCastPreview.cs`, `Cyclone/CycloneCastPreviewAttach.cs` (new, + `.meta`), `Cyclone/CycloneSteerPreview.cs`, `Editor/CyclonePreviewTests.cs`. LF, no BOM, no private IDs.

Test run (MCP Test Runner, editor open, no Play mode): `CyclonePreviewTests` + `CycloneSteerTests` 76 / 76. Full EditMode **2114 run, 2113 passed, 1 failed**: only `AIRegressionTest.Baseline_MatchesCurrentAI`, inner **`CHECKS: 714 FAILURES: 43`** (unchanged). Net +1 test against the first round (one removed, two added). Compile clean.
