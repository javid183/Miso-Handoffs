# Report: M3 pick, hold and opening (build)

Plan: plans/2026-11-26-m3-pick-build-tech.md    Agent: miso-implementer    Branch: main
Outcome: partial (chunks 8.1 and 8.2 done; 8.3–8.4 to come)

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

### Chunk 8.2: Holding the pick out of combat

- Changed (all LF, no BOM, like the files they sit next to):
  - `miso/Assets/_Project/Features/Levels/AbilityLock/AbilityLockSet.cs`: `Unlock(unit, ability)` for one unit.
  - `miso/Assets/_Project/Features/Levels/AbilityLock/LevelAbilityLock.cs`: runtime `Lock(string unitNickname, IEnumerable<AbilityPreset>)` returns the presets it newly locked and raises `Changed`; `Unlock(string unitNickname, IEnumerable<AbilityPreset>)` unlocks for that unit only and raises `Changed`.
  - `miso/Assets/_Project/Features/Player/Mark/Scripts/ProjectileCatchAndReturn.cs`: `public static bool IsCatcherHeld(GridPluggableEntity)` (the catcher is a `GUnit` its faction controller turn-skips); `TryCatch` and `WouldCatch` return false while held. `CatchSweep` reaches the catch only through `TryCatch`, so it needed no change.
  - `miso/Assets/_Project/Features/Player/Lucy/Scripts/LucyPassiveAbility_PapasShelter.cs`: `OnDisable` resets `_set` (before the bus early return); `OnEnable` calls `RefreshState()` first (a no-op before the level starts, since `_ability` is still null).
  - `miso/Assets/_Project/Features/UI/Panels/Scripts/RoleBadgeState.cs`: new `RoleBadgeState.Suppressed` and `RoleBadgeRules.Evaluate(hasRole, canPay, quiverEmpty, suppressed)` (suppressed wins, never Ready).
  - `miso/Assets/_Project/Features/UI/Panels/Scripts/UnitPanelUI.RoleBadge.cs`: reads `FactionRoleHandler.IsSuppressed`; grey colour for Suppressed; no FTP line and no "same tiles as the basic attack" line for it.
  - `miso/Assets/_Project/Features/Onboarding/HoldPickOutOfCombat.cs` (+ `.meta`, new): the hold component.
  - `miso/Assets/_Project/Features/Onboarding/HoldRoleZoneHidden.cs` (+ `.meta`, new): a small `IRoleZoneVisibility` component the hold puts on the pick (the interface is read with `GetComponents` on the unit, so it has to sit there).
  - Tests (new, + `.meta`): `Features/Onboarding/Editor/HoldPickOutOfCombatTests.cs` (15), `Features/Levels/AbilityLock/Editor/LevelAbilityLockRuntimeTests.cs` (5), `Features/Player/Mark/Scripts/Editor/CatchHeldCatcherTests.cs` (4), `Features/Player/Lucy/Scripts/Editor/PapasShelterReenableTests.cs` (3). Extended: `Features/Levels/AbilityLock/Editor/AbilityLockTests.cs` (+2), `Features/UI/Panels/Editor/RoleBadgeRulesTests.cs` (+4).
- The component, `HoldPickOutOfCombat` (goes on the level; 8.3 wires `SignalAction` → `Hold()` / `Release()`):
  - Serialized: `pushTile` (GridCell; the unit standing there is the pick; fallback: the first living free pick of the player faction, by `PickOnTilesLOCondition.IsPick` with the active mission's fixed seats) and `abilityLock` (optional; fallback: the level's `LevelAbilityLock`, else one added to this object).
  - `Hold()` (signal) finds the pick and calls `Hold(GUnit pick, IEnumerable<AbilityPreset> duoPresets)` with `DuoPresetsOf(pick)`: the pick's partner preset in every Duo entry of its faction, found by walking every unit's abilities for `AEffectCoOpTrigger` → `CooperationHandler.TryGetEntry` → partners whose `Unit == pick`. Locking those (pick, preset) pairs hides every Duo with the pick from every bar, whoever starts it (the rule `HiddenFromBar` already applies to Awake locks).
  - Hold does: a `HoldUnitsUntilSignal` on a new child object "Pick turn hold", `Set([pick])` + `Hold()` (if the pick's own faction turn is open, `NotifyTurnStarted(true)` first, so the pick shows as done and a release in a later turn of its faction restores AP); persistent tags `EntityState.Unmovable`, `EntityState.Unable to Swap`, `EntityState.IgnoreObjective` (only those it added are removed later); `FactionRoleHandlerBase.SetSuppressed(this, true)`; `HoldRoleZoneHidden.Hidden = true` on the pick; `LevelAbilityLock.Lock(pick.Nickname, duoPresets)` (remembers only what it newly locked); if the pick is "John", every enabled `LucyPassiveAbility_PapasShelter` on the faction's units is switched off (remembered).
  - `Release()` undoes each item, only what the hold did: `HoldUnitsUntilSignal.Release()` (full AP when released during the family's turn that started under the hold, code-read item 6), then the child object is destroyed; tags removed; suppression released; zone flag off; `Unlock(nickname, those presets)`; the shelters it switched off switched back on.
  - Family Super Time: suppression changes wait while `PlayerController.SuperTimeInProgress` (checked again in `Update`). Every other item applies at once.
  - Idempotent: a second `Hold()` while holding and a `Release()` without a hold do nothing; a hold after a release holds again (fresh turn hold).
  - Lifetime: `OnDisable`, `OnDestroy` and the bus's `levelEnded` (worker-thread guarded) let go of everything, including a suppression still waiting on Super Time. The `HoldUnitsUntilSignal` is released through its plain reference even when its object is already being torn down with this one, so the inactive tag never stays.
  - Suppression owner: the component itself (`this`), always released before it is destroyed.
  - No mutable statics (only the read-only `HoldTags` array), so no `PlayModeStaticReset` hook.
- Criteria met:
  - [x] `LevelAbilityLock.Lock(...)`, additive, raises `Changed`, mirror of `Unlock`; `HiddenFromBar` then hides the partner's Duo button through the existing rule. Evidence: `LevelAbilityLockRuntimeTests` (lock raises once; already locked returns nothing and stays quiet; per-unit unlock leaves another unit's lock and raises), `AbilityLockTests.UnlockForOneUnit_*`. The bar hiding the button: verifier's play check (the existing `HiddenFromBar` tests cover the rule).
  - [x] Catch & Return: no catch and no preview while the catcher is turn-skipped, through `TryCatch` (and so the sweep) and `WouldCatch`. Evidence: `CatchHeldCatcherTests` (no catcher, no faction, in the turns, inactive tag on then off, with the real `PlayerController.prefab` skip query), `HoldPickOutOfCombatTests` (`IsCatcherHeld` true while held, false after). Linda's arrow flying past a held Mark: play check.
  - [x] Papa's Shelter refreshes on re-enable. Evidence: `PapasShelterReenableTests` (disable forgets; re-enable after level start re-evaluates; enable before level start evaluates nothing). The shelter coming back next to John at release: play check.
  - [x] Role badge: Suppressed state, never Ready. Evidence: `RoleBadgeRulesTests.Suppressed_IsNeverReady`, `NotSuppressed_SameAsBefore`, `Suppressed_WithoutARole_ShowsNoBadge`, `TooltipLine_Suppressed_IsEmpty`. The grey on screen: play check.
  - [x] Onboarding component, Hold/Release toggle every item, idempotent, safe with a dead pick, lets go on disable. Evidence, `HoldPickOutOfCombatTests`: `Hold_SwitchesEveryItemOn`, `Release_SwitchesEveryItemBackOff`, `Release_LeavesTheLevelsOwnLockAndATagThePickAlreadyHad`, `APickOtherThanJohn_LeavesPapasShelterAlone`, `AShelterAlreadyOff_StaysOffAfterTheRelease`, `HoldTwice_ReleaseTwice_ActsOnce`, `ReleaseWithoutHold_DoesNothing`, `HoldAgainAfterARelease_HoldsAgain`, `ADeadPick_IsNotHeld`, `NoPick_IsNotHeld`, `APickThatFallsWhileHeld_IsStillLetGo`, `Disabling_LetsGoOfEverything`, `Destroying_LetsGoOfEverything`, `TheLevelEnding_LetsGoOfEverything`, `TheIgnoreTagIsWhatThePlayerControllersObjectivesIgnore`. The rig uses a real `PlayerController` with the prefab's skip-turn and objective-ignore queries, so "turn-skipped" and "ignored for objectives" are checked through the controller, not only the tags.
  - [x] Full AP on release in the same family turn: through `HoldUnitsUntilSignal.Release` (its existing tests); the open-turn wiring in a level: play check.
  - [ ] Not covered by EditMode tests (needs a level): `Hold()`'s pick lookup (`pushTile` / fallback), `DuoPresetsOf` against the real cooperation entries, the Super Time deferral, the zone presenter redraw. Verifier's play check after 8.3.
- Tests run (THJ's open editor, Test Runner through MCP, no Play session):
  - `MISO.Core.Features.Onboarding` + `MISO.Content.Levels.EditorTests` + `MISO.Content.UI.UnitPanel.EditorTests` + `FactionRoleSuppressionTests` + the two new Mark/Lucy fixtures: 765 total, 763 passed, 2 failed on the first run (`CatchHeldCatcherTests`: a test-rig bug, the unit's tag set wasn't created). Fixed, then:
  - `MISO.Core.Features.Bergsons.EditorTests` (every Mark and Lucy feature test, the fixed fixture included): 973 total, 973 passed.
  - Full suite not run (not required for this chunk). `AIRegressionTest` not run (no AI graph, AI ability or unit prefab change).
- Decisions and loose ends: see "Decisions I made" and "Risks and loose ends" (the 8.2 items).

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
- 8.2: `Lock` returns the presets it newly locked, and a per-unit `Unlock(nickname, presets)` was added (plus `AbilityLockSet.Unlock(unit, ability)`). The existing `Unlock(presets)` unlocks a preset for every unit, so the hold's release would also have removed a level's own lock on the same preset. Same behaviour as planned, safer release.
- 8.2: `RoleBadgeState.Suppressed` is added in `RoleBadgeState.cs` (the badge's rule file next to `UnitPanelUI.RoleBadge.cs`) instead of reusing NoFtp, whose tooltip says "Needs N FTP" and would be wrong. Grey, no tooltip line, so no new player-facing text.
- 8.2: the role zone is hidden by a separate small component, `HoldRoleZoneHidden`, on the pick, because `RoleZoneVisibility` reads `IRoleZoneVisibility` with `GetComponents` on the unit. It stays on the unit after the release with `Hidden = false` (the presenter's `Update` sees the flip and redraws).
- 8.2: Catch & Return's held check is `IsUnitTurnSkipped` on the catcher's faction controller (the plan's "turn-skipped"), so any skip-turn tag stops catches, not only this hold. In the shipped data the skip query is `Status.Inactive`.
- 8.2: Papa's Shelters are found through the pick's faction units (`TryGetComponent`), not a scene search, so tests don't touch the open scene.
- 8.2: a hold during the pick's own open turn calls `HoldUnitsUntilSignal.NotifyTurnStarted(true)` before `Hold()` (the open turn read from `CombatLevelRunHandler.CurrentFactionControllerOrNull`). Without it the freshly added hold would think no turn is open: the pick wouldn't show as done. The pick's leftover AP that turn is not drained (a direct `Consume` could reach a shared AP pool); it can't be selected anyway, and its next turn start closes it.
- 8.2: when the level has no `LevelAbilityLock`, the hold adds one to its own object at the hold (only when there are Duo presets to lock). 8.3 can wire the serialized `abilityLock` instead.
- 8.2: `HoldUnitsUntilSignal` is used through its HEAD API only (`Set`, `Hold`, `Release`, `NotifyTurnStarted`), so 8.3 can revert 7.1's `holdFromLevelStart` without touching this.

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
- 8.2: the unit panel's role badge refreshes on FTP changes and when the shown unit changes, not when suppression changes. If the pick's panel is on screen at the moment of the hold, the badge turns grey at the next refresh (an FTP change or a reselect). A held pick can't be selected, so this is short-lived; a fix would be a refresh call in `UnitPanelUI.cs` (outside this chunk's files).
- 8.2: the role zone presenter only notices a newly added `HoldRoleZoneHidden` at its next redraw (selection, hover, move end, turn start, ability performed). The release flip is seen at once.
- 8.2: `HoldPickOutOfCombatTests` uses `SuppressionTestRole` from 8.1's `FactionRoleSuppressionTests.cs`, so the 8.2 commits must land after the 8.1 core commit (the badge also reads `IsSuppressed`).
- 8.2: the held pick keeps any action points it had left on reaching the push tile until its faction's next turn start (it can't be selected; the turn doesn't wait for it). Its AP pips may still show for that turn. A release in that same turn (not M3's flow) would leave those points, not top them up.
- 8.2: the Super Time deferral waits on `PlayerController.SuperTimeInProgress`; not tested in EditMode (needs running Super Time actions).
- 8.2: the Duo lock relies on the action bar being the way to start a family Duo. Nothing else excludes a held partner (`CooperationEntry.Available`); I found no other player entry point, but the play check should try a Duo with the held pick from another unit's bar.

## Proposed commits

1. `feat(core): a unit's Family Role can be suppressed at runtime` (core):
   - `miso/Assets/_Project/Core/Systems/AbilitySystem/Abilities/Runtime/FactionRoleHandlerBase.cs`
   - `miso/Assets/_Project/Core/Interactions/Runtime/PlayerController.cs`
   - `miso/Assets/_Project/Core/Interactions/Runtime/FactionControllerBase.cs`
   - `miso/Assets/_Project/Core/Systems/AbilitySystem/Abilities/Editor/FactionRoleSuppressionTests.cs`
   - `miso/Assets/_Project/Core/Systems/AbilitySystem/Abilities/Editor/FactionRoleSuppressionTests.cs.meta`
2. `feat: a held unit doesn't catch, shelter or join Duos` (8.2 feature files and the badge; after 1):
   - `miso/Assets/_Project/Features/Levels/AbilityLock/AbilityLockSet.cs`
   - `miso/Assets/_Project/Features/Levels/AbilityLock/LevelAbilityLock.cs`
   - `miso/Assets/_Project/Features/Levels/AbilityLock/Editor/AbilityLockTests.cs`
   - `miso/Assets/_Project/Features/Levels/AbilityLock/Editor/LevelAbilityLockRuntimeTests.cs`
   - `miso/Assets/_Project/Features/Levels/AbilityLock/Editor/LevelAbilityLockRuntimeTests.cs.meta`
   - `miso/Assets/_Project/Features/Player/Mark/Scripts/ProjectileCatchAndReturn.cs`
   - `miso/Assets/_Project/Features/Player/Mark/Scripts/Editor/CatchHeldCatcherTests.cs`
   - `miso/Assets/_Project/Features/Player/Mark/Scripts/Editor/CatchHeldCatcherTests.cs.meta`
   - `miso/Assets/_Project/Features/Player/Lucy/Scripts/LucyPassiveAbility_PapasShelter.cs`
   - `miso/Assets/_Project/Features/Player/Lucy/Scripts/Editor/PapasShelterReenableTests.cs`
   - `miso/Assets/_Project/Features/Player/Lucy/Scripts/Editor/PapasShelterReenableTests.cs.meta`
   - `miso/Assets/_Project/Features/UI/Panels/Scripts/RoleBadgeState.cs`
   - `miso/Assets/_Project/Features/UI/Panels/Scripts/UnitPanelUI.RoleBadge.cs`
   - `miso/Assets/_Project/Features/UI/Panels/Editor/RoleBadgeRulesTests.cs`
3. `feat(onboarding): hold the pick out of combat` (8.2 component; after 1 and 2):
   - `miso/Assets/_Project/Features/Onboarding/HoldPickOutOfCombat.cs`
   - `miso/Assets/_Project/Features/Onboarding/HoldPickOutOfCombat.cs.meta`
   - `miso/Assets/_Project/Features/Onboarding/HoldRoleZoneHidden.cs`
   - `miso/Assets/_Project/Features/Onboarding/HoldRoleZoneHidden.cs.meta`
   - `miso/Assets/_Project/Features/Onboarding/Editor/HoldPickOutOfCombatTests.cs`
   - `miso/Assets/_Project/Features/Onboarding/Editor/HoldPickOutOfCombatTests.cs.meta`

## Other branches

none

## How to see it

1. Nothing visible yet: no game code calls the API until 8.2's hold component.
2. Window > General > Test Runner > EditMode, filter `FactionRoleSuppressionTests`, Run Selected: 17 green.
3. 8.2: nothing visible in a level until 8.3 wires `HoldPickOutOfCombat` into M3. Test Runner > EditMode, filter `HoldPickOutOfCombatTests` (15), `LevelAbilityLockRuntimeTests` (5), `CatchHeldCatcherTests` (4), `PapasShelterReenableTests` (3), `RoleBadgeRulesTests`, `AbilityLockTests`: all green.
