# Report: Cyclone controls (click to Steer, Steer pulse, free first Steer, Mark's Command steers)

Plan: plans/2026-11-20-cyclone-controls-tech.md    Agent: miso-implementer    Branch: thj/cyclone
Outcome: partial (K1 and K3 committed; K2 built, waiting for review; K4 to K6 to come)

## What changed

- See the chunk blocks below. Filled for the whole feature on the last chunk.

## Acceptance criteria

Filled on the last chunk. K1 only adds the core hook; no acceptance criterion is visible in play until K3.

## Chunks

### Chunk K1: core, planted entities can take a click (D-593)

**Built**
- `miso/Assets/_Project/Core/Entities/Runtime/IClickablePlantedEntity.cs` (new, namespace `MISO.Core.Entities`): `bool TryHandleClick(FactionControllerBase controller)`; true = click consumed. Main thread only.
- `miso/Assets/_Project/Core/Interactions/Runtime/PlantedClickRules.cs` (new, pure static): `ShouldAsk(FactionPhaseStateType? state, Func<bool> isLegalTargetOfActiveAbility)`: UnitSelection and ActionSelection ask; TargetSelection asks only when the legality check says false; TakeAction or no state never asks. The legality check runs only in TargetSelection. `TryGiveClick(IClickablePlantedEntity, state, isLegal, controller)`: null entity = false, nothing evaluated; otherwise asks the entity when `ShouldAsk` allows and returns its answer.
- `miso/Assets/_Project/Core/Interactions/Runtime/PlayerController.PlantedClick.cs` (new partial): `private bool TryGivePlantedEntityClick(GridCell cell)` takes `cell.PlantedEntity` (already alive-filtered by `GridCell`, plus a Unity null check), casts to the interface, calls the rule with `CurrentPhaseState?.Type`, `() => IsLegalAbilityTarget(cell)` and `this`.
- `miso/Assets/_Project/Core/Interactions/Runtime/PlayerController.cs`: one line in `HandleGridCellSelection`, after the two early returns (introduction, other faction acting) and before the state branches:
  `if (TryGivePlantedEntityClick(cell)) return;`
  On true the click is done (no state branch, no `TryTakeAction`). No signature changed. With no planted entity implementing the interface (nothing does yet) the method behaves exactly as before.
- `miso/Assets/_Project/Core/Interactions/Editor/PlantedClickRulesTests.cs` (new, 11 test cases).
- All new files LF, no BOM (`Interactions/` is LF without BOM; `Entities/Runtime/` is mixed, the newer files have no BOM). `PlayerController.cs` is LF (checked `git ls-files --eol`), kept LF; diff is 1 insertion.

**Verified**
- Compiles: `refresh_unity` + `read_console`: no compile errors; only the usual pre-existing warnings and four "Objects are trying to be loaded during a domain backup" editor messages (domain reload noise, not from this code).
- Fixture `MISO.Core.Interactions.EditorTests.PlantedClickRulesTests`: 11/11 passed. Covers: the fake entity is asked and consumes the click in UnitSelection and ActionSelection (and no legality check runs there); in TargetSelection an illegal cell goes to the entity; a legal target of the active ability never asks it; TakeAction and no state never ask; a declining entity leaves the click to the states; a cell without a clickable entity returns false in every state and checks nothing.
- Full EditMode suite: 2365 total, 2363 passed, 1 failed, 1 skipped (`AIRegressionTest.Baseline_MatchesCurrentAI`, Explicit). The failure is `CycloneSteerTests.LiveSteer_CostsOneAP_OnceATurn_AndIsSeparateFromTheCast` ("cooldown 1: once per family turn", expected 1, was 0): it reads `Lucy_Ability_Steer.asset`, whose cooldown THJ set to 0 in the editor. Not related to K1; K4 updates this test with the cooldown change.

**Not verified**
- `PlayerController` itself is not driven in EditMode (it needs a level, grid, phase states and the input controller). The decision (which state, legal target or not, entity present or not) is a pure rule the partial calls, and the rule is what is tested. That the one call sits at the right place and that a real click reaches it is checked by reading the code; the first play check is K3 (Cyclone implements the interface).

**Findings**
- **`Lucy_Ability_Steer.asset` got saved to disk during the full suite run** (file time 14:11:24, about 23 s into the run that started 14:11:01). I never called `AssetDatabase.SaveAssets` or touched the asset. The editor log shows a burst of re-imports at that moment (render textures, many `Content/Levels/M*.asset` missions and the Steer asset), the pattern of a project-wide `SaveAssets`, so some test or editor code in the suite saves all dirty assets. The saved diff is THJ's in-editor change: `coolDownV.constantValue` 1 -> 0, plus Unity re-wrapping the `description` line (same text). No other file changed (`git status` shows only it besides the K1 files and THJ's two known files). I left it as it is. K4 makes cooldown 0 the saved value anyway; THJ should know it is now on disk. Worth a backlog item: find the test that saves assets and stop it (it would also save any other unsaved editor work during a suite run).
- `HandleGridCellSelection` is also called internally with unit cells (auto-select, switch unit, `TrySelectUnit`, after an action reversion, the recursive re-entries after a cancel). The hook is consulted there too, as the plan places it. That only matters when the clicked or selected cell has both a unit and a clickable planted entity. Suggestion for K3: `CycloneEntity.TryHandleClick` returns false when its cell is occupied, so a unit on the cell (a heavy enemy mid-burst, a unit being auto-selected) keeps today's handling; the plan's "Click order" risk asks for that ("only where the click would otherwise be ignored or select nothing").
- Reactive interrupt is not excluded by the core rule (the plan's hook conditions are state-only). `PlayerController.IsReactiveInterrupt` is public, so K3's entity can refuse during one, as the acceptance criterion asks.

**Decisions I made**
- The state and legality decision lives in a pure rule (`PlantedClickRules`), called by the partial, so it is testable in EditMode. Same behaviour as the plan's inline condition.
- States compared by `FactionPhaseStateType` rather than by state instance: each type has exactly one instance in `FactionControllerBase` (checked), so the result is the same.
- The legality check is passed lazily (`Func<bool>`) so `IsLegalAbilityTarget` runs only in TargetSelection and only when a clickable entity is on the cell; a board without one does no extra work.

**Files to stage (K1 commit, core, on its own)**
- `miso/Assets/_Project/Core/Entities/Runtime/IClickablePlantedEntity.cs` + `.meta`
- `miso/Assets/_Project/Core/Interactions/Runtime/PlantedClickRules.cs` + `.meta`
- `miso/Assets/_Project/Core/Interactions/Runtime/PlayerController.PlantedClick.cs` + `.meta`
- `miso/Assets/_Project/Core/Interactions/Runtime/PlayerController.cs`
- `miso/Assets/_Project/Core/Interactions/Editor/PlantedClickRulesTests.cs` + `.meta`

Proposed message: `feat(core): planted entities can take a player's click before the selection states, legal ability targets keep priority`

Not to stage with K1: `GlobalSettings.asset`, `miso.slnx`, `.mcp.json`, `powershell.exe`, `Lucy_Ability_Steer.asset` (goes with K4).

## Reviews and checks

- K1: (written by the coordinator)

## Save reset

No.

## Decisions I made

- See the chunk blocks.

## Needs THJ

- `Lucy_Ability_Steer.asset` is now saved with cooldown 0 (see K1 Findings); nothing to decide unless that was not wanted yet.

## Docs to update

- `tech/core-systems.md`: `IClickablePlantedEntity` + `PlantedClickRules` + `PlayerController.PlantedClick.cs` (the one call in `HandleGridCellSelection`). After the play check, with the other two hooks.

## Risks and loose ends

- A test or editor tool in the EditMode suite saves all dirty assets (see K1 Findings).

## Proposed commits

1. `feat(core): planted entities can take a player's click before the selection states, legal ability targets keep priority`: the K1 files above (core)

## Other branches

none

## How to see it

Nothing visible until K3 (the Cyclone takes the click). K1 alone: play as usual; clicks behave exactly as before.

## K1 review (miso-reviewer, 2026-11-20): FIX

**Must fix:** the hook sits in `HandleGridCellSelection`, which the controller also calls itself (`AutoSelectUnit`, `SwitchSelectedUnit`, reactive select/reselect, `CheckForActionReversion`, `TrySelectUnit`, re-entries after a cancel): an entity can get clicks nobody made, be asked twice per click, and an implementer that selects a unit standing on its own cell would recurse. Move the call to the real click path: in `OnMouseClick` (~:285) `if (TryGivePlantedEntityClick(gridCell)) return;` before `HandleGridCellSelection`, restore :527, and start `TryGivePlantedEntityClick` with the same two guards (`IntroductionInProgress`; `!_reactiveInterrupt && OtherFactionActionInProgress()`).
**Should fix:** (1) legality must mirror the player's TargetSelection condition: `IsLegalAbilityTarget(cell) || (cell.OccupantEntity is GUnit enemy && CanApproachAttackTarget(enemy))` (as `CursorSituationDriver.cs:440`). (2) TargetSelection ally-switch branch (:591-602) runs before Apply: skip the hook when it applies, or document that the entity wins. (3) `PlantedClickRules` fails open when no legality function is given in TargetSelection: refuse instead or drop the branch and its test.
**Notes for K3:** refuse during a reactive interrupt (`IsReactiveInterrupt`, `isActionInProgress`); clicking the Cyclone while the Steer is already aiming re-enters the Steer (pulse guard must cover it).

### Chunk K3: click to Steer and the Steer pulse (D-589, D-590)

**Built** (all under `miso/Assets/_Project/Features/Player/Lucy/Scripts/`, LF, no BOM)
- `Cyclone/CycloneClickRules.cs` (new, pure): `ShouldSteer(controllerIsPlayer, controlsLucysFaction, lucyIsAI, steerActive, actionInProgress, reactiveInterrupt, unitOnCell)`.
- `Cyclone/CycloneEntity.Click.cs` (new partial): `CycloneEntity : IClickablePlantedEntity`. Gathers the facts (Steer found via `CycloneButtonSwap.FindSteer`, `Active`, `AEffectCycloneSteer.IsAIControlled`, `isActionInProgress`, `IsReactiveInterrupt`, occupant on the cell), then `TrySelectUnit(lucy)`, `HandleAbilitySelection(steer)`, `ShowSelectedAbilities(steer)`; true. Already aiming Lucy's Steer: returns true without re-selecting (no second target-selection entry).
- `Cyclone/CyclonePulseGuard.cs` (new, pure): `TryBegin(beatActive)` / `End()`; no start while running or during a beat.
- `Cyclone/CycloneCrossView.cs`: serialized `pulseScale` 1.15, `pulseSeconds` 0.15; `PlayPulse()` (scale bump of the Visual up and back plus chevron flare), `PulseRunning`; remembers its Cyclone in `Show`; a Whirl Swell beat stops a running pulse; target lookup moved into `ResolveSwellTarget` (same behaviour).
- `Cyclone/CycloneSteerPreview.cs`: one line in `OnEnteredTargetSelection`: when the ability is this Cyclone's Steer, `CrossView.PlayPulse()`.
- `Editor/CycloneClickTests.cs` (new, 12 tests): click rule (usable, steer not active i.e. cooldown/no AP, AI Lucy, action in progress, reactive interrupt, unit on cell, other faction, non-player controller), entity declines with no owner, guard once / no stacking / skipped in a beat, view plays once per entry, skipped during a beat and a beat drops a running pulse.

**Verified**: compiles clean; `MISO.Core.Features.Bergsons.EditorTests.Cyclone.*`: 336 run, 335 passed, 1 failed = the known `LiveSteer_CostsOneAP_OnceATurn_AndIsSeparateFromTheCast` (K4).

**Not verified (needs play check)**: the real click path (`TrySelectUnit` + `HandleAbilitySelection` + bar highlight) and the visible pulse; the entity's `TryHandleClick` needs a live level, so only the rule and guard are unit-tested.

**Decisions**: pulse "beat active" = a Whirl Swell..Done beat flag or the Cyclone whirling. Returns true even if `HandleAbilitySelection` refuses after Lucy was selected (click was consumed). No private IDs in code.

**Files to stage (K3 commit, after K1)**: the four new `.cs` files above plus their `.meta` (CycloneClickRules, CycloneEntity.Click, CyclonePulseGuard, CycloneClickTests), and the edited `CycloneCrossView.cs`, `CycloneSteerPreview.cs`.
Proposed message: `feat(lucy): click the Cyclone to select Lucy and open the Steer, and the Cyclone pulses when its Steer is picked`

### Chunk K1 fix round (after the K1 review)

**Must fix, done**
- The hook moved to the real click path. `PlayerController.OnMouseClick`: `if (TryGivePlantedEntityClick(gridCell)) return;` right before `HandleGridCellSelection(gridCell)`. The line in `HandleGridCellSelection` is gone, so the controller's own selections (auto-select, unit switch, reactive select and reselect, action reversion, `TrySelectUnit`, re-entries after a cancel) never ask the entity. `PlayerController.cs` still differs from HEAD by one inserted line (`git diff --stat`: 1 insertion).
- `TryGivePlantedEntityClick` starts with the same two guards as `HandleGridCellSelection` (`IntroductionInProgress`; `!_reactiveInterrupt && OtherFactionActionInProgress()`).
- `IClickablePlantedEntity` doc says so: real clicks only, not when the click is ignored, and target selection asks only when the click would do nothing.

**Should fix, all three done**
1. Target-selection acceptance mirrors the player's TargetSelection condition: `IsLegalAbilityTarget(cell) || (cell.OccupantEntity is GUnit enemy && CanApproachAttackTarget(enemy))` (`IsTargetSelectionClick` in the partial, with a comment), the same as `CursorSituationDriver.ResolveLegal`.
2. The ally-switch branch: `SwitchesToAllyInTargetSelection(cell)` in the partial copies that branch's condition (another family unit; during a reactive interrupt when it can afford its Family Role, otherwise while a Move ability aims; plus a null guard on the active ability). The rule takes it as a second check and doesn't ask the entity when it applies. The switch is checked first, as in target selection itself. Copied rather than extracted so `PlayerController.cs` keeps its one-line diff; if that branch changes, the copy has to follow (comment says it mirrors it).
3. In TargetSelection a missing check (either function null) now means the entity is not asked. Test updated.

`PlantedClickRules` signatures now: `ShouldAsk(state, Func<bool> isAcceptedTarget, Func<bool> switchesToAlly)` and `TryGiveClick(clickable, state, isAcceptedTarget, switchesToAlly, controller)`. Both checks still run only in TargetSelection and only when a clickable entity is on the cell. K3's files were not touched; `CycloneEntity.Click.cs` compiles against the unchanged interface.

**Verified**
- Compiles: `refresh_unity` + `read_console`: no errors.
- `PlantedClickRulesTests`: 12/12 passed (new: ally switch never asks the entity and skips the target check; without both checks the entity isn't asked; target selection with nothing accepted runs both checks once).
- `MISO.Core.Features.Bergsons.EditorTests.Cyclone.*`: 336 run, 335 passed, 1 failed = the known `LiveSteer_CostsOneAP_OnceATurn_AndIsSeparateFromTheCast` (cooldown 0 on disk, K4).
- Full EditMode suite: 2379 total, 2377 passed, 1 failed (the same known one), 1 skipped (`AIRegressionTest.Baseline_MatchesCurrentAI`, Explicit).
- `git status` of `miso/` was identical before and after this suite run (nothing new saved this time).

**Not verified**: the real click in play (K3's play check covers it); the two mirrored conditions are checked by reading, not by a test, since they need a live controller.

**K1 files to stage (final, core commit on its own)**
- `miso/Assets/_Project/Core/Entities/Runtime/IClickablePlantedEntity.cs` + `.meta`
- `miso/Assets/_Project/Core/Interactions/Runtime/PlantedClickRules.cs` + `.meta`
- `miso/Assets/_Project/Core/Interactions/Runtime/PlayerController.PlantedClick.cs` + `.meta`
- `miso/Assets/_Project/Core/Interactions/Runtime/PlayerController.cs` (one inserted line in `OnMouseClick`)
- `miso/Assets/_Project/Core/Interactions/Editor/PlantedClickRulesTests.cs` + `.meta`

Proposed message (unchanged): `feat(core): planted entities can take a player's click before the selection states, legal ability targets keep priority`

**Coordinator (2026-11-20):** K1 fix round checked by reading the diff (call moved to `OnMouseClick`, one line in `PlayerController.cs`, guards and the three should-fixes in); full suite 2377/2379 (1 known K4 failure, 1 Explicit skip). Committed K1 `14f9c43e7` (core, alone) and K3 `3c2a366cd`. Not re-reviewed by the reviewer after the fix round; K3 is reviewed with the feature at the end.

### Chunk K2: core, per-use AP cost override (D-593)

**Built**
- `miso/Assets/_Project/Core/Systems/AbilitySystem/Effects/Runtime/IAbilityCostOverride.cs` (new, namespace `MISO.Core.Systems.AbilitySystem.Effects`, same shape as `ITargetSelectionRangeProvider`): interface `IAbilityCostOverride.TryGetActionCost(RuntimeAbility ability, out int count)` and the pure static `AbilityCostOverride`:
  - `TryGetActionCost(ability, out count)` and an overload over a list of effects: the first top-level effect that answers wins; the count is clamped to 0 or more. Nested compound effects are not searched (as `TargetSelectionRange`).
  - `Charge(ability, usualCount, Action<int> consume, Action recordFree)` (and an effects overload): no answer = `consume(usualCount)`, exactly as before; an answer = `consume(count)`, and when the count is 0 also `recordFree()`.
  - `PreviewAP(ability)`, `PreviewAP(ability, usualAP)` and an effects overload: the override's count in AP (count times the consumption type's AP, Ineffective = 0) when an effect answers, else the usual value.
  - Main thread only (Unity null check on the preset); the AI never calls it.
- `miso/Assets/_Project/Core/Systems/AbilitySystem/Points/Runtime/FreeActionRecord.cs` (new, pure): `RecordFree`, `RecordCharged`, `Clear`, `TakeFreeRevert` (true once after a free action).
- `miso/Assets/_Project/Core/Interactions/Runtime/FactionControllerBase.cs` (core): in the `TakeActionState` completion, `ConsumeActionCost(apCount);` is replaced by `AbilityCostOverride.Charge(PhaseData.ActiveAbility, apCount, ConsumeActionCost, () => PhaseData.ActiveUnit.APConsumer.RecordFreeConsumption())` plus a comment (`git diff --stat`: 3 insertions, 1 deletion). The virtual `ConsumeActionCost` still does the charging, so `PlayerController.ConsumeActionCost` (reactive interrupt pays FTP and ignores the count) is untouched and still runs. No signature changed. The class stays non-partial (one call, no new logic in the file).
- `miso/Assets/_Project/Core/Systems/AbilitySystem/Points/Runtime/APConsumer.cs` (core): a `FreeActionRecord` field; `RecordFreeConsumption()` (new public); `Consume` marks the action charged (after its `count <= 0` early return, so a 0 count still records nothing there); `RevertConsumption` returns at once when the last action was free; `ResetToInitial` clears the record. 8 insertions. With no override nobody calls `RecordFreeConsumption`, the record stays false and every path behaves as before.
- `miso/Assets/_Project/Core/Interactions/Runtime/PlayerController.cs` (core): `OnTargetCellAPPreview` passes `AbilityCostOverride.PreviewAP(ability, apCost)` instead of `apCost` (1 line changed). Without it, hovering a target cell in range would show the usual 1 AP for a free use.
- `miso/Assets/_Project/Features/UI/Panels/Scripts/AbilitiesBarHUDUI.cs` (not core): the four places that showed `(int)ability.Parameters.apConsumptionType` now show `AbilityCostOverride.PreviewAP(ability)`: `ShowAbilityAPPreview` (what `CombatLevelUIManager.ShowAbilityAPPreview` forwards to), the ability button hover (hovered, and back to the selected one), and the `ShowAPUsagePreview` fallback for a non-positive cost (so a 0 from the cell hover falls back to 0, not 1). Plus `using ...Effects`. 5 insertions, 4 deletions.
- `miso/Assets/_Project/Core/Systems/AbilitySystem/Effects/Editor/AbilityCostOverrideTests.cs` (new, 13 tests).
- All files LF; new files without BOM (as their folders); `FactionControllerBase.cs` keeps its BOM.

**Undo: how consumptions are recorded**
- PerUnit (the game's mode, D-037): `ActionPoints.Consume` stores `_lastPoints` (the points before) and `RevertConsumption` sets the attribute back to it. `APConsumer.Consume(type, 0)` returns early, so after a free use `_lastPoints` would still be the previous action's, and an undo of the free use would refund that earlier action's AP. Shared (dormant): the same with `_lastSharedCost` and `_actionsTaken`.
- Chosen: skip the revert consistently. A free use records "last action free" on the unit's `APConsumer`; the next `RevertConsumption` gives nothing back and clears it; any real consumption or a turn reset clears it first. No change to `ActionPoints` or `FactionPhaseState.cs`.

**Verified**
- Compiles: `refresh_unity` (forced, compile requested) + `read_console`: no errors besides the usual three "Objects are trying to be loaded during a domain backup" editor messages.
- Fixture `MISO.Core.Systems.AbilitySystem.Effects.EditorTests.AbilityCostOverrideTests`: 13/13 passed. Covers: no answering effect charges the usual count and records no free use (also with no effects or no ability); an override of 0 charges 0 and records one free use; 2 charges 2; the first answering effect wins and later ones aren't asked; a negative answer counts as 0; the ability is passed to the effect and its preset's effects are read; the preview shows 1 without an override, the caller's usual AP without an override, 0 and 2 with overrides (also over a hovered cell's cost), 0 for an Ineffective type. On a real per-unit `APConsumer` (3 AP): a free use after a charged one spends nothing and its undo refunds nothing (stays 2, not 3); an override of 2 spends 2; without an override, charge and undo are unchanged; a charged use after a free one is refunded by the undo; a turn reset forgets a free use; the record's own sequence.
- Full EditMode suite: 2392 total, 2390 passed, 1 failed, 1 skipped. Failure = the known `CycloneSteerTests.LiveSteer_CostsOneAP_OnceATurn_AndIsSeparateFromTheCast` (cooldown 0 on disk, K4). Skip = `AIRegressionTest.Baseline_MatchesCurrentAI` (Explicit). AI regression not run: no AI graph, AI ability or unit prefab touched.
- `git status` of `miso/` identical before and after the suite (the K2 files plus THJ's `GlobalSettings.asset`, `Lucy_Ability_Steer.asset`, `miso.slnx`); nothing new saved.

**Not verified (needs play)**: nothing implements the interface yet, so nothing changes in play until K4 (the Steer's free first use). The wiring in `FactionControllerBase` and the preview call sites is checked by reading; the helper they call and the `APConsumer` bookkeeping are tested.

**Decisions I made**
- The preview change sits in `AbilitiesBarHUDUI` (what `CombatLevelUIManager.ShowAbilityAPPreview` forwards to) rather than in `CombatLevelUIManager.cs`, which is unchanged. Same behaviour as the plan's "the UI manager shows the overridden cost". The bar also needed it for the button hover and the 0-cost fallback, and `PlayerController.OnTargetCellAPPreview` for the in-range cell hover; without them the criterion "the AP preview on hover shows the real cost" would fail in K4.
- The override's count replaces the charge's count; the consumption type still applies (Singular: count = AP). The preview uses the same rule.
- The charge override also applies to multi-activation abilities (it replaces the distance-based count); the preview does the same.
- A free use is also recorded during a reactive interrupt (the player's override then pays FTP as before). An undo there then gives back no AP instead of resetting AP to a stale value. It only matters once an override answers during a reactive interrupt, which K4's Steer doesn't plan to.
- Shared AP mode (dormant): a free use doesn't count towards the per-unit escalation (`_actionsTaken`) and its undo doesn't lower it. If Shared AP ever comes back and a free use should count, that is a two-line change in `APConsumer`.

**Risks and loose ends**
- Pre-existing, not touched: `ActionPoints.RevertConsumption` sets the main attribute to `_lastPoints`, which includes external AP sources (it could over-refund while an external source holds AP), and a count above 1 records only the last step (an undo of a 2-AP charge refunds 1). Worth a backlog line if multi-AP overrides are ever combined with undo.
- Pre-existing, not touched: a multi-activation ability at distance 0 gets a count of 0 that records nothing (an undo then refunds the action before). Left as is so K2 changes nothing without an override.

**Files to stage (K2 commit, core, on its own)**
- `miso/Assets/_Project/Core/Systems/AbilitySystem/Effects/Runtime/IAbilityCostOverride.cs` + `.meta`
- `miso/Assets/_Project/Core/Systems/AbilitySystem/Points/Runtime/FreeActionRecord.cs` + `.meta`
- `miso/Assets/_Project/Core/Systems/AbilitySystem/Points/Runtime/APConsumer.cs`
- `miso/Assets/_Project/Core/Interactions/Runtime/FactionControllerBase.cs`
- `miso/Assets/_Project/Core/Interactions/Runtime/PlayerController.cs`
- `miso/Assets/_Project/Features/UI/Panels/Scripts/AbilitiesBarHUDUI.cs`
- `miso/Assets/_Project/Core/Systems/AbilitySystem/Effects/Editor/AbilityCostOverrideTests.cs` + `.meta`

Core files changed: `FactionControllerBase.cs` (+3/-1), `APConsumer.cs` (+8), `PlayerController.cs` (+1/-1). `CombatLevelUIManager.cs` and `FactionPhaseState.cs` unchanged. New core files: `IAbilityCostOverride.cs`, `FreeActionRecord.cs`. Non-core: `AbilitiesBarHUDUI.cs` (+5/-4), the test file.

Proposed message: `feat(core): an effect can set what one use of its ability costs in AP, a free use is not refunded by an undo, and the AP preview shows that cost`

Not to stage with K2: `GlobalSettings.asset`, `miso.slnx`, `.mcp.json`, `powershell.exe`, `Lucy_Ability_Steer.asset` (goes with K4).

Docs to update (after the play check, with the other hooks): `tech/core-systems.md`. Effects row: `IAbilityCostOverride` + `AbilityCostOverride` (charge in the `FactionControllerBase` TakeAction completion, previews in `PlayerController.OnTargetCellAPPreview` and `AbilitiesBarHUDUI`). AP row: `APConsumer.RecordFreeConsumption` + `FreeActionRecord` (the undo of a free use refunds nothing).

## K2 review (miso-reviewer, 2026-11-20): APPROVE

No must-fix or should-fix. Checked: additive, charge paths (multi-activation, reactive FTP untouched), undo (free, paid-then-free, free-then-paid, turn reset, Closure), per-unit record, Shared mode, previews unchanged without override, AI on the main thread only, LF/BOM kept. Notes: K4 must re-arm the free Steer on undo of a free Steer (not of a paid one) — sent to the K4 implementer; the override also answers for an AI Lucy (harmless, AI never Steers); the walk+attack auto-move preview ignores overrides (no override uses it); `tech/core-systems.md` entry pending (preview change is in `AbilitiesBarHUDUI`, not `CombatLevelUIManager`).

**Coordinator:** committed K2 `9c1cc7705` (core, alone; `AbilitiesBarHUDUI.cs` with it since it needs the helper).

### Chunk K4: cooldown 0 and the free first Steer (D-591)

**Built** (Lucy files LF, no BOM)
- `Features/Player/Lucy/Scripts/Cyclone/AEffectCycloneSteer.cs`: implements `IAbilityCostOverride`; serialized `firstSteerFreeEachTurn` (default true). `TryGetActionCost` answers 0 when on and Lucy's Cyclone (found through `ability.Owner`) has not used the free Steer this turn, else no answer (1 AP). `TrackFreeSteer(ability, cyclone, reversionContext)` hooks `ability.OnCompletionPerRun` (runs after the action charge) to mark the free Steer used, so the preview and the charge both read "free" until the Steer completes. The effect now overrides both `ApplyUnguarded` forms (4-arg and with `ReversionContext`) through one `Steer` method (same behaviour); the ability comes from `statCtx` (the RuntimeAbility).
- `Cyclone/CycloneEntity.FreeSteer.cs` (new partial): `FreeSteerUsed`, `MarkFreeSteerUsed`, `RearmFreeSteer`, `ResetFreeSteer`. `CycloneEntity.PhaseTick` calls `ResetFreeSteer()` (one line, Lucy's phase start). State is on the Cyclone: no statics.
- Undo (coordinator's note): a free Steer's reversion action re-arms the free Steer; a paid (second) Steer's undo leaves it used. Today the Steer effect asset is `revertible: 0`, so the game never undoes a Steer; the logic is in place and tested anyway.
- Only Lucy's own Steer ability sets the flag (the hook is in the effect's Apply); `CycloneEntity.TrySteer`/`SteerRoutine` do not, so Mark's Command steering later neither uses nor resets it. AI: the override is main-thread only and nothing depends on it (the AI never Steers).
- Assets: `Lucy_Ability_Steer.asset` description set to the new text (cooldown 0 already there); `Lucy_Ability_Steer_Effect_Steer.asset` got `firstSteerFreeEachTurn: 1`. `CycloneSteerSetup.cs`: cooldown 0, same description, comments.
- Tests: `CycloneSteerTests.cs` live test renamed `LiveSteer_CostsOneAP_HasNoCooldown_FirstIsFree_AndIsSeparateFromTheCast` (cooldown 0, setup constant agrees, description, effect flag). New `CycloneSteerTests.FreeSteer.cs` (+ meta), 7 tests: free then 1 AP then free next turn (real APConsumer + preview), readable before the charge and flips only after, setting off = always 1 AP, refused Steer keeps the free one, started Steer hooks completion, a Steer not made by Lucy's ability (Cyclone routine, other caster) never uses it, undo of free re-arms / undo of paid keeps used.

**Verified**: compiles clean. `MISO.Core.Features.Bergsons.EditorTests` (all) + `AbilityCostOverrideTests`: 896 run, 896 passed (CycloneSteerTests alone 70/70). No full suite, no AIRegressionTest (no AI content changed).

**Not verified (play check)**: the real flow (free AP display on the bar, charge of 0 AP, cancel keeps free); `ApplyUnguarded` success path is tested in edit mode only up to starting the Steer.

**Loose ends**: a Cyclone re-cast after a free Steer is a new entity, so the free Steer is available again that turn. Whether the Steer can be picked with 0 AP left (a free Steer with no AP) was not checked; the ability bar's availability rule may still need 1 AP.

**Files to stage (K4 commit)**
- `miso/Assets/_Project/Features/Player/Lucy/Scripts/Cyclone/AEffectCycloneSteer.cs`
- `miso/Assets/_Project/Features/Player/Lucy/Scripts/Cyclone/CycloneEntity.cs`
- `miso/Assets/_Project/Features/Player/Lucy/Scripts/Cyclone/CycloneEntity.FreeSteer.cs` + `.meta`
- `miso/Assets/_Project/Features/Player/Lucy/Scripts/Editor/CycloneSteerSetup.cs`
- `miso/Assets/_Project/Features/Player/Lucy/Scripts/Editor/CycloneSteerTests.cs`
- `miso/Assets/_Project/Features/Player/Lucy/Scripts/Editor/CycloneSteerTests.FreeSteer.cs` + `.meta`
- `miso/Assets/_Project/Resources/UnitSpecific/Player/Lucy/Abilities/Cyclone/Lucy_Ability_Steer.asset`
- `miso/Assets/_Project/Resources/UnitSpecific/Player/Lucy/Abilities/Cyclone/Lucy_Ability_Steer_Effect_Steer.asset`

Proposed message: `feat(lucy): the Steer has no cooldown and the first Steer each turn is free, with a setting on the effect`
Not to stage: `GlobalSettings.asset`, `miso.slnx`, `.mcp.json`, `powershell.exe`.

**Coordinator:** K4 committed `08074905e` (896/896 in the Bergsons group + `AbilityCostOverrideTests`; no full suite, no core). Open for play: the bar's AP display, a real 0 AP charge; whether the Steer can be picked with 0 AP left (unit selection still needs AP > 0, as planned); a re-cast Cyclone after a free Steer gets a new free Steer that turn (rare: the cast has cooldown 4).

### Chunk K5: core, a planted entity as a Command target (D-593)

**Built**
- `miso/Assets/_Project/Core/Entities/Runtime/IAbilityTargetablePlanted.cs` (new, `MISO.Core.Entities`, 27 lines): `bool IsTargetableBy(RuntimeAbility ability)` and `bool TryCollectNextTargetCells(RuntimeAbility ability, int targetIndex, List<GridCell> cells)`. `targetIndex` is the index of the pick being made (1 = the second target), the same indexing as `AbilityPreset.GetTargetTypeAt` / `GetRelativeTargetSpecs`. The list arrives empty; true = exactly these cells (an empty list leaves nothing to pick), false = the ability's own range. Main thread only.
- `miso/Assets/_Project/Core/Interactions/Runtime/PlantedAbilityTargetRules.cs` (new, pure static, 48 lines):
  - `AcceptsPlantedTarget(targetType, targetIndex, cellHasOccupant, planted, ability)`: true only for the first pick (index 0), a pick that takes a cell occupant and not a cell, a cell without an occupant, an implementing entity, and `IsTargetableBy(ability)` true. The entity is not asked otherwise.
  - `TryCollectNextTargetCells(targetIndex, pickedAroundPreviousTarget, previousTarget, ability, cells)`: clears the buffer; true only for index > 0, a pick made around the previous target, a previous target that implements the interface and answers true. A declining entity's cells are dropped.
- `miso/Assets/_Project/Core/Interactions/Runtime/FactionControllerBase.PlantedTarget.cs` (new partial, 66 lines): `ResolvePlantedAbilityTarget(cell, targetIndex)` (reads `cell.PlantedEntity`, casts, calls the rule with the pick's target type and `cell.OccupantEntity`); public `GetHoverablePlantedAbilityTarget(cell)` (only for a Player-handled controller in TargetSelection); `CollectPlantedNextTargetCells(ability)` (previous picked entity, `GetRelativeTargetSpecs(count) != null`, a fresh list or null).
- `miso/Assets/_Project/Core/Systems/GridSystem/Runtime/GridManager.PlantedTarget.cs` (new partial, BOM + LF like the other GridManager files, 22 lines): `GetHoverablePlantedAbilityTarget(cell)`: null unless the cell's planted entity implements the interface; then asks `CombatLevelRunHandler.Instance.CurrentFactionControllerOrNull`.
- `FactionControllerBase.cs` (core, BOM + LF kept, +5/-1):
  - `public class` -> `public partial class` (no behaviour; lets the new logic live in the partial).
  - `IsLegalAbilityTarget`: one `else if` before the final `else return false`: the planted entity becomes `targetEntity`, then every existing check runs on it unchanged (relation skipped as for any non-unit, `CheckTargetSelectionCondition`, `OccupantIntersects(range)`, the preset's tag query, select-by-call).
  - `TargetSelectionState.SetObject`: the same `else if` before `TargetEntities.Add(null)`, so the planted entity is the picked target and `ApplyCondition` checks it like `IsLegalAbilityTarget`.
  - `RefreshTargetSelectionRangeCells`: for a relative next pick, `CollectPlantedNextTargetCells(ability) ?? ComputeRelativeTargetRangeCells(...)`. The cells become `ActiveAbilityRangeCells`, so the highlight, `IsLegalAbilityTarget`, the click's `ApplyCondition`, the cursor and the AP preview all follow them.
- `GridManager.cs` (core, +1/-1): `GetHoverableCellEntity` ends with `return GetHoverablePlantedAbilityTarget(cell);` instead of `return null;` (reached only when the cell has no occupant, no stashed entity and no IsTargetable planted entity). The Command's first pick has the CellEntity subject, so without this the Cyclone cell would show no hover and send no entity-hover event.
- `AEffectCommand.cs` (core, +2, comment only): no logic change needed. Effects signal "running" with `IsInProgress`; `AbilityEffectSetLevel.ApplyMapped` applies every effect, then waits while any is in progress. A first target that isn't a `GUnit` hits the existing early `return` before `IsInProgress = true`, so nothing starts, the other effects already ran, and the wait ends at once. The comment says so at the guard.
- Tests: `miso/Assets/_Project/Core/Interactions/Editor/PlantedAbilityTargetTests.cs` (new, 11 tests), `miso/Assets/_Project/Core/Systems/AbilitySystem/Effects/Editor/AEffectCommandNonUnitTargetTests.cs` (new, 1 test).
- New Interactions and Entities files: LF, no BOM (as K1's new files there). No new statics. No private IDs in code.

**Command preview path, checked by reading (non-unit first target)**
- `ResolveGhostUnit`: `TargetEntities[0] is not GUnit` -> null, no ghost. `ResolveGhostCell` returns the cell for FirstSelectedUnit.
- `OnMoveTargetGridCellHover` (second pick): mover = `pathOrigin.OccupantEntity as GUnit` = null -> `RebuildAltPaths` returns at `!mover`; no path, `GetMoveBudget` not reached. On the first pick this handler doesn't fire (CellEntity subject sends no cell hover).
- `CommitPreviewedMovePath`: second pick -> unit = previous cell's occupant = null -> returns. First pick: `_previewPath` can't end on the Cyclone cell -> returns.
- `AEffectCommand.TryBuildPreviewPath` is only called by the effect itself (after the unit guard) and by `MoveUnitSequence`/transporters.
- `AbilityDamagePreview.ComputeFor`, `AbilityPushPreview.ComputeFor`, `TryTakeAction` (SpawnSource aimed at the target), `AbilityPreset.Activate` (`ForceFaceTowards`/`NotifyIncomingDirection` take any `GridPluggableEntity` in the bundle) don't assume a unit. Nothing throws or draws a Command path/ghost.

**Verified**
- Compiles: `refresh_unity` (forced, compile requested) + `read_console`: 0 errors (usual warnings only).
- Fixtures `PlantedAbilityTargetTests` + `AEffectCommandNonUnitTargetTests`: 12/12 passed. Covered:
  - rules: a first unit pick on an empty cell takes an answering planted entity (asked once, with the active ability); a declining one or none is refused; a unit on the cell, a later pick, a Cell pick, a Cell|CellOccupant pick, a CellPlantedEntity pick or no ability never ask the entity; next-pick cells come exactly from the planted previous target (buffer cleared first, index 1 passed, an empty answer still replaces the range); a declining entity, a non-implementing previous target, a pick not around the previous target, index 0 or no ability keep the usual range and leave the buffer empty.
  - real `FactionControllerBase` (states from `PreparePhaseStates`, hand-made cells, a fake `OnGridEntity` implementing the interface), with a two-pick test ability (unit first, then a cell around it): the planted entity is legal, `SetObject` makes it the target and `ApplyCondition` accepts it; a declining implementing entity and a plain non-targetable `OnGridEntity` are refused (`TargetEntities` gets null as before); a unit on the same cell stays the target and the entity isn't asked; the next pick's cells are the entity's cells, null when the next pick isn't relative or the first target is a unit; the hover returns the entity only for a Player controller in TargetSelection on the first pick, not when it declines.
  - `AEffectCommand` in an effect level with a recording second effect, bundle [planted entity, cell]: `IsInProgress` stays false, the other effect ran on the bundle, the effect wait doesn't keep waiting and the run ends.
- Full EditMode suite: 2411 total, 2410 passed, 0 failed, 1 skipped (`AIRegressionTest.Baseline_MatchesCurrentAI`, Explicit). AI regression not run: no AI graph, AI ability or unit prefab touched.
- `git status` of `miso/` identical before and after the suite (the K5 files plus THJ's `GlobalSettings.asset` and `miso.slnx`); nothing saved by the run.

**Not verified (needs K6 and the play check)**: nothing implements the interface yet, so nothing changes in play. `RefreshTargetSelectionRangeCells` (it calls `SetHighlight`, which needs cell visuals) is not driven in EditMode; the helper it calls is tested and the one changed line is checked by reading.

**Decisions I made**
- The new branch is last in the target-kind chain in both `IsLegalAbilityTarget` and `SetObject`, so it runs only when no existing kind (cell, occupant, stashed, IsTargetable planted) matched. With no implementing entity every path returns what it did before. The planted entity still goes through the ability's usual checks (range, tag query, effect conditions, select-by-call): K6's Cyclone must pass Mark's Command tag query (Unmovable excluded) and its effects' `CheckTargetSelectionCondition` (the Weak compound included).
- First pick only, as the plan says ("a first target of type CellOccupant"), and not for a pick that also takes cells.
- The planted next-pick cells replace the range only for a next pick made around the previous target (the Command's is). For abilities whose later picks are around the owner the range stays: `RefreshTargetSelectionRangeCells` returns early for them and wouldn't restore an owner range on undo, so a planted range could stay highlighted. Same behaviour for the feature; narrower than "any next target".
- Parameter named `targetIndex` (index of the pick being made) instead of `nextTargetIndex`, to match the preset's indexing and not read as an index into `nextTargets`.
- The hover lives in `GridManager` (where the hovered entity is chosen) and asks the current faction controller (Player-handled, in TargetSelection). Legality is not part of the hover, as for units.
- `FactionControllerBase` made `partial` (one keyword) to keep its edits to three call lines.

**Findings / loose ends for K6**
- `GridManager` (Grid row of `tech/core-systems.md`) is a core file the plan's K5 text didn't name; the brief asked for the hover (`GetHoverableCellEntity`). One line plus a partial.
- The Command's first-pick range is the existing owner range (`Stat_RANGE`); the Cyclone counts when its cell is in it.
- `OccupantIntersects` counts a cell whose occupant's footprint touches the range, so a heavy standing on a Steer stop makes its other cells legal second picks too (today's Command semantics). K6's effect should plan from the clicked cell, or check it.
- `JohnPassiveAbility_CommandShieldDash` remembers the last hovered `GUnit` during Mark's Command (`_previewCommandedUnit`). Hover a unit, then pick the Cyclone: John's shield-dash preview can draw for that unit on a Steer stop. Not touched (not in K5); K6 should clear it for a non-unit first target or check it in play.
- `AbilityPreset.Activate` turns targets to face Mark (`forceTargetsFaceUnit: 1` on the Command): the Cyclone gets `FaceTowards(Mark)`. Check in play.
- The entity-hover event is recomputed on hover-out: if the pick changes while the cursor rests on the Cyclone (it was just picked), the entity's "unhovered" event is not sent (the cell's is). The player's previews are cleared by the state change and the cell event; worth a look in play.
- AI: never uses `IsLegalAbilityTarget` or the hover; an AI Command's first pick is a unit cell, where the new branch isn't reached. K6's `IsTargetableBy` can also refuse AI casters.

**Files to stage (K5 commit, core, on its own)**
- `miso/Assets/_Project/Core/Entities/Runtime/IAbilityTargetablePlanted.cs` + `.meta`
- `miso/Assets/_Project/Core/Interactions/Runtime/PlantedAbilityTargetRules.cs` + `.meta`
- `miso/Assets/_Project/Core/Interactions/Runtime/FactionControllerBase.PlantedTarget.cs` + `.meta`
- `miso/Assets/_Project/Core/Interactions/Runtime/FactionControllerBase.cs`
- `miso/Assets/_Project/Core/Systems/GridSystem/Runtime/GridManager.PlantedTarget.cs` + `.meta`
- `miso/Assets/_Project/Core/Systems/GridSystem/Runtime/GridManager.cs`
- `miso/Assets/_Project/Core/Systems/AbilitySystem/Effects/Runtime/AEffectCommand.cs`
- `miso/Assets/_Project/Core/Interactions/Editor/PlantedAbilityTargetTests.cs` + `.meta`
- `miso/Assets/_Project/Core/Systems/AbilitySystem/Effects/Editor/AEffectCommandNonUnitTargetTests.cs` + `.meta`

Core files changed: `FactionControllerBase.cs` (+5/-1), `GridManager.cs` (+1/-1), `AEffectCommand.cs` (+2, comment). New core files: `IAbilityTargetablePlanted.cs`, `PlantedAbilityTargetRules.cs`, `FactionControllerBase.PlantedTarget.cs`, `GridManager.PlantedTarget.cs`.

Proposed message: `feat(core): a planted entity can be an ability's first target where a unit is taken, give the next pick's cells, and show as hovered`
Not to stage: `GlobalSettings.asset`, `miso.slnx`, `.mcp.json`, `powershell.exe`.

Docs to update (after the play check, with the other hooks): `tech/core-systems.md`: Faction controllers row (`IAbilityTargetablePlanted`, `PlantedAbilityTargetRules`, `FactionControllerBase.PlantedTarget.cs`, the three call lines, class now partial); Grid row (`GridManager.PlantedTarget.cs`, the hover fallback); Effects row (`AEffectCommand` with a non-unit first target finishes at once, code unchanged).

## K5 review (miso-reviewer, 2026-11-20): APPROVE

No must-fix. Should fix: (1) `GridManager.ClearLastHoveredCell` recomputes the entity to un-hover; the planted fallback depends on the pick state, so after the Cyclone is picked first the `gridCellEntityHovered(cyclone, false)` is lost — remember the fallback's entity in an instance field and use it on clear. (2) Tests don't show an answering planted entity refused by range or tag query. Notes: K6 must refuse AI casters (AI shares `SetObject`), keep `IsTargetableBy` cheap (per frame), check `forceTargetsFaceUnit` and heavy footprint second picks. Coordinator accepted the `GridManager` hover touch.

**Coordinator:** K5 committed `31788c273` (core, alone). Both should-fixes go in a K5 follow-up core commit after K6 (one writer at a time); notes sent to the K6 implementer.
