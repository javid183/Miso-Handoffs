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
