# Report: M3 pick, hold and opening (build)

Plan: plans/2026-11-26-m3-pick-build-tech.md    Agent: miso-implementer    Branch: main
Outcome: partial (chunk 8.1 done; 8.2–8.4 to come)

## What changed

- `miso/Assets/_Project/Core/Systems/AbilitySystem/Abilities/Runtime/FactionRoleHandlerBase.cs`: additive per-unit runtime suppression (`SetSuppressed`, `IsSuppressed`, static `JoinsSuperTime`); a suppressed role reads as silenced and fails `CheckActivationMoment`.
- `miso/Assets/_Project/Core/Interactions/Runtime/PlayerController.cs`: `SuperTimeUnits` skips suppressed units; `ActivateFactionSuperTimeIE` iterates `SuperTimeUnits` instead of `AliveUnits`.
- `miso/Assets/_Project/Core/Systems/AbilitySystem/Abilities/Editor/FactionRoleSuppressionTests.cs` (+ `.meta`): 13 new EditMode tests.

## Acceptance criteria

Filled per chunk below; the feature-wide list is filled on the last chunk.

## Chunks

### Chunk 8.1: Core: per-unit Family Role suppression

- Changed:
  - `miso/Assets/_Project/Core/Systems/AbilitySystem/Abilities/Runtime/FactionRoleHandlerBase.cs` (UTF-8 BOM, LF kept)
  - `miso/Assets/_Project/Core/Interactions/Runtime/PlayerController.cs` (no BOM, LF kept)
  - `miso/Assets/_Project/Core/Systems/AbilitySystem/Abilities/Editor/FactionRoleSuppressionTests.cs` (new, BOM + LF like its neighbours)
  - `miso/Assets/_Project/Core/Systems/AbilitySystem/Abilities/Editor/FactionRoleSuppressionTests.cs.meta` (new, Unity-generated)
- API (on `FactionRoleHandlerBase`, reach it through `unit.AbilityOrchestrator.FactionRoleHandler`):
  - `public void SetSuppressed(object owner, bool on)`: owner-keyed claims (a private `List<object>`). The same owner twice counts once; two owners keep it suppressed until both release; releasing without a claim is a no-op; a null owner throws `ArgumentNullException`. Main thread.
  - `public bool IsSuppressed`: reads a plain cached `bool` field, safe from the AI worker thread.
  - `public static bool JoinsSuperTime(FactionRoleHandlerBase handler)`: handler exists (Unity bool, main thread, same as the old `HasFactionRole`) and is not suppressed.
  - `IsSilenced` is now `_suppressed || (old rule)`. `CheckActivationMoment` returns false while suppressed.
- Criteria met:
  - [x] Additive API, suppressed never triggers: `CheckActivationMoment` false (the unit is never a candidate in `ApplyFactionRolesIfPossible`, never queued in the wait list) and `CheckFeasibility` false via `IsSilenced` (covers wait-list entries queued before the suppression). Covers John, Linda, Lucy and Mark through the base. The Masher's counter does not go through `CheckFeasibility`: its enqueue (`OnDamaged`, `CloseDuo`), its answer gate (`CanAnswer`) and its reaction preview all check `IsSilenced`, so folding suppression into `IsSilenced` stops it with no change to the Masher files. Tests: `Suppressed_NeverTriggers`, `Unsuppressed_TriggersAgain`, `Default_NotSuppressed_TriggersAsBefore`, `Default_ActivationMomentStillFollowsPhaseAndEvents`, the owner tests.
  - [x] No behavior change unless called, no serialized data change: the new fields are private and non-serialized (`List<object>` isn't serializable anyway); with no claim `_suppressed` is false and every changed expression reduces to the old one. `ActivateFactionSuperTimeIE` over `SuperTimeUnits` instead of `AliveUnits` is the same set when nothing is suppressed (units without a handler were already no-ops via `_factionRoleHandler?.ActivateSuperTime()`).
  - [x] `PlayerController.SuperTimeUnits` skips suppressed units: `SuperTimeUnits_SkipsASuppressedUnit`, `SuperTimeUnits_Default_EveryAliveUnitWithARole` (real `PlayerController` with `PhaseData` set by reflection), `JoinsSuperTime_*`. Through `SuperTimeUnits`, a suppressed unit is also out of the Super Time availability check (`GUnit.CheckIfFactionSuperTimeAvailable`), the camera focus, the synergy event and `SuperTimeInProgress`.
  - [x] Instance state only: no new static fields (`JoinsSuperTime` is a static method, no state). No `PlayModeStaticReset` hook needed.
  - [x] AI-thread safe: `IsSuppressed`, `IsSilenced` and `CheckActivationMoment` read plain fields only; no Unity-object API added on those paths.
  - [x] EditMode tests: 13 new in `FactionRoleSuppressionTests`, all pass.
  - [x] Full EditMode suite: 2895 total, 2894 passed, 0 failed, 1 skipped (`AIRegressionTest.Baseline_MatchesCurrentAI`, Explicit). Last time 2881 + 1 Explicit; +13 new. Run in THJ's open editor through the Test Runner (MCP). `AIRegressionTest` not run by name (not in scope).
  - [ ] `tech/core-systems.md`: draft line below, for the coordinator to write.
  - [x] Commit unit: core only (below).
- Decisions and loose ends: see "Decisions I made" and "Risks and loose ends".

## Reviews and checks

- (coordinator)

## Save reset

No.

## Decisions I made

- Owner-keyed claims (`SetSuppressed(object owner, bool on)`) rather than a bare count: makes 8.2's Hold/Release idempotent even if called twice, and two features can't undo each other. Same behavior as the plan's example.
- Suppression folded into `IsSilenced` so the Masher is covered through the base without editing its (core) partials. `IsSilenced` has no UI reader today (only gating: base feasibility, Masher counter and preview), so no "silenced" display appears for a suppressed unit.
- `ActivateFactionSuperTimeIE` changed to loop `SuperTimeUnits`: without it a suppressed unit would still run its Super Time ability even though it is out of `SuperTimeUnits`. Same set when nothing is suppressed.
- Edited `PlayerController.cs` in place (two lines) rather than adding a partial: the change replaces existing lines, so a partial file wouldn't remove them.
- Added `FactionRoleHandlerBase.JoinsSuperTime` as the testable rule `SuperTimeUnits` uses.

## Needs THJ

none

## Docs to update

- `tech/core-systems.md`, Family Roles row, draft line to append: "Since 2026-11-26 (D-748): additive runtime suppression on `FactionRoleHandlerBase`: `SetSuppressed(object owner, bool on)` (owner-keyed claims, instance state, never saved) and `IsSuppressed` (plain field, worker-safe). A suppressed role fails `CheckActivationMoment` and reads as `IsSilenced` (so the base feasibility check and the Masher's counter/preview stop too); `PlayerController.SuperTimeUnits` (via static `FactionRoleHandlerBase.JoinsSuperTime`) and `ActivateFactionSuperTimeIE` skip it. Not gated: the player's reactive-interrupt role play (`PlayerController.CanAffordFactionRole`) and a direct `FactionControllerBase.TryPlayFactionRole` call. No behavior change while nobody suppresses."

## Risks and loose ends

- Not gated by suppression (left out on purpose, the plan names only feasibility, activation moment and Super Time): `PlayerController.CanAffordFactionRole` (the reactive-interrupt role the player can play during the enemy turn, also drives the Energetic mark and the ATB "usable" display) and a direct `FactionControllerBase.TryPlayFactionRole(unit)` call. For M3 this doesn't matter: the held pick is turn-skipped and `CanAffordFactionRole` already returns false for turn-skipped units; only the Masher calls `TryPlayFactionRole`, after its own `IsSilenced` gate. If suppression should also block the reactive path in general, it is one more `&& !handler.IsSuppressed` in `CanAffordFactionRole` (core, additive): coordinator's call.
- `SetSuppressed` stores the owner by reference. An owner that is destroyed without releasing keeps the role suppressed for the rest of that unit's life. 8.2's hold component should release on disable / level abort (the plan already asks for that).
- A Super Time that is already running when a unit gets suppressed drops that unit from `SuperTimeInProgress` (the wait), since it reads `SuperTimeUnits`. Not a case M3 can reach (suppression happens at the push, outside Super Time).
- `OnboardingMissionGraphTests.cs` shows as modified in `git diff`: that's the uncommitted 7.1 work, not this chunk.

## Proposed commits

1. `feat(core): a unit's Family Role can be suppressed at runtime` (core):
   - `miso/Assets/_Project/Core/Systems/AbilitySystem/Abilities/Runtime/FactionRoleHandlerBase.cs`
   - `miso/Assets/_Project/Core/Interactions/Runtime/PlayerController.cs`
   - `miso/Assets/_Project/Core/Systems/AbilitySystem/Abilities/Editor/FactionRoleSuppressionTests.cs`
   - `miso/Assets/_Project/Core/Systems/AbilitySystem/Abilities/Editor/FactionRoleSuppressionTests.cs.meta`

## Other branches

none

## How to see it

1. Nothing visible yet: no game code calls the API until 8.2's hold component.
2. Window > General > Test Runner > EditMode, filter `FactionRoleSuppressionTests`, Run Selected: 13 green.
