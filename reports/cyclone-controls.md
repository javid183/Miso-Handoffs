# Report: Cyclone controls (click to Steer, Steer pulse, free first Steer, Mark's Command steers)

Plan: plans/2026-11-20-cyclone-controls-tech.md    Agent: miso-implementer    Branch: thj/cyclone
Outcome: partial (K1 done; K2 to K6 to come)

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
