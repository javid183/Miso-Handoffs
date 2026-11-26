# Report: M3 pick, hold and opening (build)

Plan: plans/2026-11-26-m3-pick-build-tech.md    Agent: miso-implementer    Branch: main
Outcome: partial (chunk 8.1 done; 8.2–8.4 to come)

## What changed

- `miso/Assets/_Project/Core/Systems/AbilitySystem/Abilities/Runtime/FactionRoleHandlerBase.cs`: additive per-unit runtime suppression (`SetSuppressed`, `IsSuppressed`, static `JoinsSuperTime`); a suppressed role reads as silenced and fails `CheckActivationMoment`.
- `miso/Assets/_Project/Core/Interactions/Runtime/PlayerController.cs`: `SuperTimeUnits` skips suppressed units; `ActivateFactionSuperTimeIE` iterates `SuperTimeUnits` instead of `AliveUnits`; `CanAffordFactionRole` (reactive interrupt) returns false for a suppressed unit.
- `miso/Assets/_Project/Core/Interactions/Runtime/FactionControllerBase.cs`: `TryPlayFactionRole` refuses a suppressed unit.
- `miso/Assets/_Project/Core/Systems/AbilitySystem/Abilities/Editor/FactionRoleSuppressionTests.cs` (+ `.meta`): 17 new EditMode tests.

## Acceptance criteria

Filled per chunk below; the feature-wide list is filled on the last chunk.

## Chunks

### Chunk 8.1: Core: per-unit Family Role suppression

- Changed:
  - `miso/Assets/_Project/Core/Systems/AbilitySystem/Abilities/Runtime/FactionRoleHandlerBase.cs` (UTF-8 BOM, CRLF kept)
  - `miso/Assets/_Project/Core/Interactions/Runtime/PlayerController.cs` (no BOM, CRLF kept)
  - `miso/Assets/_Project/Core/Interactions/Runtime/FactionControllerBase.cs` (UTF-8 BOM, CRLF kept; added after the coordinator's follow-up decision)
  - `miso/Assets/_Project/Core/Systems/AbilitySystem/Abilities/Editor/FactionRoleSuppressionTests.cs` (new, BOM + CRLF like its neighbours)
  - `miso/Assets/_Project/Core/Systems/AbilitySystem/Abilities/Editor/FactionRoleSuppressionTests.cs.meta` (new, Unity-generated)
- API (on `FactionRoleHandlerBase`, reach it through `unit.AbilityOrchestrator.FactionRoleHandler`):
  - `public void SetSuppressed(object owner, bool on)`: owner-keyed claims (a private `List<object>`). The same owner twice counts once; two owners keep it suppressed until both release; releasing without a claim is a no-op; a null owner throws `ArgumentNullException`. Main thread.
  - `public bool IsSuppressed`: reads a plain cached `bool` field, safe from the AI worker thread.
  - `public static bool JoinsSuperTime(FactionRoleHandlerBase handler)`: handler exists (Unity bool, main thread, same as the old `HasFactionRole`) and is not suppressed.
  - `IsSilenced` is now `_suppressed || (old rule)`. `CheckActivationMoment` returns false while suppressed.
  - Follow-up (coordinator D-754): `PlayerController.CanAffordFactionRole` returns false and `FactionControllerBase.TryPlayFactionRole` refuses (returns false, plays nothing) for a suppressed unit. Each is one early `if (handler.IsSuppressed) return false;` after the existing has-a-role check, so nothing changes while nobody suppresses.
- Criteria met:
  - [x] Additive API, suppressed never triggers: `CheckActivationMoment` false (the unit is never a candidate in `ApplyFactionRolesIfPossible`, never queued in the wait list) and `CheckFeasibility` false via `IsSilenced` (covers wait-list entries queued before the suppression). Covers John, Linda, Lucy and Mark through the base. The Masher's counter does not go through `CheckFeasibility`: its enqueue (`OnDamaged`, `CloseDuo`), its answer gate (`CanAnswer`) and its reaction preview all check `IsSilenced`, so folding suppression into `IsSilenced` stops it with no change to the Masher files. Tests: `Suppressed_NeverTriggers`, `Unsuppressed_TriggersAgain`, `Default_NotSuppressed_TriggersAsBefore`, `Default_ActivationMomentStillFollowsPhaseAndEvents`, the owner tests.
  - [x] No behavior change unless called, no serialized data change: the new fields are private and non-serialized (`List<object>` isn't serializable anyway); with no claim `_suppressed` is false and every changed expression reduces to the old one. `ActivateFactionSuperTimeIE` over `SuperTimeUnits` instead of `AliveUnits` is the same set when nothing is suppressed (units without a handler were already no-ops via `_factionRoleHandler?.ActivateSuperTime()`).
  - [x] `PlayerController.SuperTimeUnits` skips suppressed units: `SuperTimeUnits_SkipsASuppressedUnit`, `SuperTimeUnits_Default_EveryAliveUnitWithARole` (real `PlayerController` with `PhaseData` set by reflection), `JoinsSuperTime_*`. Through `SuperTimeUnits`, a suppressed unit is also out of the Super Time availability check (`GUnit.CheckIfFactionSuperTimeAvailable`), the camera focus, the synergy event and `SuperTimeInProgress`.
  - [x] Instance state only: no new static fields (`JoinsSuperTime` is a static method, no state). No `PlayModeStaticReset` hook needed.
  - [x] AI-thread safe: `IsSuppressed`, `IsSilenced` and `CheckActivationMoment` read plain fields only; no Unity-object API added on those paths.
  - [x] Reactive interrupt and direct play closed too (follow-up): `CanAffordFactionRole_Default_True`, `CanAffordFactionRole_Suppressed_False_AndBackAfterRelease` (real `PlayerController`, unit with an ATB gauge and a free role), `TryPlayFactionRole_Default_Plays`, `TryPlayFactionRole_Suppressed_Refuses_AndPlaysAfterRelease` (real `AIController`, the side the Masher's counter plays from; the test role records the play and leaves it running, so no level singleton is touched).
  - [x] EditMode tests: 17 new in `FactionRoleSuppressionTests`, all pass.
  - [x] Full EditMode suite (rerun after the follow-up): 2899 total, 2898 passed, 0 failed, 1 skipped (`AIRegressionTest.Baseline_MatchesCurrentAI`, Explicit). Last time 2881 + 1 Explicit; +17 new. (First run, before the follow-up: 2895 / 2894 passed / 1 Explicit.) Run in THJ's open editor through the Test Runner (MCP). `AIRegressionTest` not run by name (not in scope).
  - [ ] `tech/core-systems.md`: draft line below, for the coordinator to write.
  - [x] Commit unit: core only (below).
- Decisions and loose ends: see "Decisions I made" and "Risks and loose ends".

## Reviews and checks

- **8.1 core review (miso-reviewer): APPROVE**, nothing to fix. Additive confirmed (IsSilenced, SuperTimeUnits set, ActivateFactionSuperTimeIE, early returns after the has-role check; no serialized change). Owner claims sound; loose ends for 8.2: claims match by `Equals` (destroyed UnityEngine.Object owners compare equal) and there is no clear-all, so the hold component must release in `OnDisable`/`OnDestroy`. Don't change suppression during Family Super Time (a unit dropping out of `SuperTimeUnits` mid-Super-Time stops `SuperTimeInProgress` waiting on it). Worker-safe, no statics, CRLF/BOM kept (report wording corrected), no private IDs, tests real. AI baseline should not move.
- 8.1 full EditMode suite (implementer): 2899, 2898 passed, 0 failed, 1 Explicit.

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

- `tech/core-systems.md`, Family Roles row, draft line to append: "Since 2026-11-26 (D-748): additive runtime suppression on `FactionRoleHandlerBase`: `SetSuppressed(object owner, bool on)` (owner-keyed claims, instance state, never saved) and `IsSuppressed` (plain field, worker-safe). A suppressed role fails `CheckActivationMoment` and reads as `IsSilenced` (so the base feasibility check and the Masher's counter/preview stop too); `PlayerController.SuperTimeUnits` (via static `FactionRoleHandlerBase.JoinsSuperTime`) and `ActivateFactionSuperTimeIE` skip it; `PlayerController.CanAffordFactionRole` (reactive interrupt) and `FactionControllerBase.TryPlayFactionRole` refuse it (D-754). No behavior change while nobody suppresses."

## Risks and loose ends

- Closed after the first hand-off (D-754): the reactive interrupt (`CanAffordFactionRole`) and direct `TryPlayFactionRole`. Through `CanAffordFactionRole` a suppressed unit also loses the Energetic mark, the ATB "usable" display and the reactive-unit pick, which is consistent with "can't play its role".
- Readers of `IsSilenced` (whole `_Project`, game code and editor code): only gates, no UI. `FactionRoleHandlerBase.CheckFeasibility` (base trigger); `MasherGoblinFactionRoleHandler.Preview.cs:58` (`ShowReactionPreview`: no counter preview); `MasherGoblinFactionRoleHandler.Counter.cs:113` (`OnDamaged`: no enqueue), `:219` (`CloseDuo`: no Duo enqueue), `:315` (`CanAnswer`: no answer). No icon, label, badge, tooltip or asset binding reads it (also searched `.asset`/`.prefab`). Nothing would show misleading "silenced" UI for a held unit. Related but not an `IsSilenced` reader: the unit panel's role badge (`Features/UI/Panels/Scripts/UnitPanelUI.RoleBadge.cs`, `GetRoleBadgeState`) reads only `HasFactionRole`, the family's FTP and Linda's quiver, so a held, suppressed pick's badge can still show **Ready** (green) while its role can't fire. That is mildly misleading for the held pick; left unchanged as asked. A fix would be a `Suppressed` badge state or hiding the badge, in that UI file (non-core). 8.2 hides the role zone separately.
- `SetSuppressed` stores the owner by reference. An owner that is destroyed without releasing keeps the role suppressed for the rest of that unit's life. 8.2's hold component should release on disable / level abort (the plan already asks for that).
- A Super Time that is already running when a unit gets suppressed drops that unit from `SuperTimeInProgress` (the wait), since it reads `SuperTimeUnits`. Not a case M3 can reach (suppression happens at the push, outside Super Time).
- `OnboardingMissionGraphTests.cs` shows as modified in `git diff`: that's the uncommitted 7.1 work, not this chunk.

## Proposed commits

1. `feat(core): a unit's Family Role can be suppressed at runtime` (core):
   - `miso/Assets/_Project/Core/Systems/AbilitySystem/Abilities/Runtime/FactionRoleHandlerBase.cs`
   - `miso/Assets/_Project/Core/Interactions/Runtime/PlayerController.cs`
   - `miso/Assets/_Project/Core/Interactions/Runtime/FactionControllerBase.cs`
   - `miso/Assets/_Project/Core/Systems/AbilitySystem/Abilities/Editor/FactionRoleSuppressionTests.cs`
   - `miso/Assets/_Project/Core/Systems/AbilitySystem/Abilities/Editor/FactionRoleSuppressionTests.cs.meta`

## Other branches

none

## How to see it

1. Nothing visible yet: no game code calls the API until 8.2's hold component.
2. Window > General > Test Runner > EditMode, filter `FactionRoleSuppressionTests`, Run Selected: 17 green.
