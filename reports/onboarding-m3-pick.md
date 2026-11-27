# Report: M3 pick, hold and opening (build)

Plan: plans/2026-11-26-m3-pick-build-tech.md    Agent: miso-implementer    Branch: main
Outcome: partial (chunks 8.1, 8.2 and 8.3 done; 8.4 to come)

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

### Chunk 8.3: M3 rewired to `m3-defence-4`

Paths under `miso/Assets/_Project/`. Every `.cs` file is LF with no BOM, like the rest of `Features/Onboarding` (checked with `file`). Worked in THJ's open editor through Unity MCP; no Play session. Play mode was off throughout; the active scene (`PreloadScreen.unity`) was not touched and is not dirty.

**Changed (code):**
- `Features/Onboarding/Editor/MissionWiring.HoldTheYard.cs`: class comment, `BlockId` `m3-defence-4`, `BlockDocument` (the approved block, `level deploy 4,8`, `level hidden masher 6,1`), constants (`DeployTile`, `PushTile`, `OpeningClawTiles`, `MasherGroupId`, `DeploySlotName`, `StageCount` 6, `HoldStageCount` 3, the objective texts), `WireLevel` (no Mark; `WirePickHold`), six stages, `Destroyed` on Enemy, the sisters' level-start lock is the Linda–Lucy Duo only, a `UnitOn` helper. Gone: `MarkTile`, `NoJohnTile`, `MarkObjective`, the Mark Duo paths, `WireDefeatWhenMarkFalls`.
- `Features/Onboarding/Editor/MissionWiring.HoldTheYard.Pick.cs` (+ `.meta`, new): the `HoldPickOutOfCombat` on its own object "The pick at the stone" under the level (`pushTile` 4,11, `abilityLock` the level's), two `SignalAction` listeners (`M3Yard_HoldPick` → `Hold()`, `M3Yard_ReleasePick` → `Release()`), the push stage (`PickOnTilesLOCondition` + `TilesOccupiedLOCondition` on 4,11, as the old greybox's S2), and the defeat when the pick falls.
- `Features/Onboarding/Editor/MissionWiring.HoldTheYard.Sequences.cs`: the level-start tour (stone and Claws → west lane → yard), the cave (S1 end), the push (S2 end), notches 1 and 2 unchanged, notch 3 (roll away + release), the end unchanged. Pick lines go through the pick's dialogue slot (`GenericCharacter_1`, as the Trail's `SpeakAsThePick`).
- `Features/Onboarding/Editor/MissionWiring.HoldTheYard.Stone.cs`: `StoneCount` 4 (start + three notches).
- `Features/Onboarding/Editor/MissionWiring.HoldTheYard.Mission.cs`: writes one free seat (`FreeSeats` = 1) instead of none.
- `Features/Onboarding/Editor/M3DefenceTests.cs`: updated (see Tests).
- `Features/Onboarding/PickFallenLOCondition.cs` (follow-up, D-756): exposes `{pick_i}`, the pick's nickname (watched pick, else the first living free pick; kept after the fall); `PickWatch.Pick`; static `PickVariable`. LF, no BOM, as before.
- `Features/Onboarding/Editor/PickFallenLOConditionTests.cs` (follow-up): +2 tests (`TheWatchedPickIsExposedByName`, `AConditionWithNoPickExposesNothing`).

**Reverted to HEAD** (written back with `git show HEAD:<path> > <path>`, no git write; `git status` shows them clean):
- `Features/Onboarding/HoldUnitsUntilSignal.cs` (drops `holdFromLevelStart`; 8.2 doesn't need a change to it) and `Features/Onboarding/Editor/HoldUnitsUntilSignalTests.cs` (the `partial`).
- `Core/Levels/Editor/OnboardingMissionGraphTests.cs`, `Features/Onboarding/Editor/SearchTrailTests.cs`, `Features/Onboarding/Editor/PickOnTilesLOConditionTests.cs` (back to the free seat).
- `Content/Levels/Greybox/GB_m1-ridge.prefab`: its only change was 7.1's `holdFromLevelStart: 0` line, written by Unity for the field that is now gone. Not in the brief's file list; reverting it is the field's removal, nothing else.

**Removed (7.1 files, untracked, never committed):**
- `Features/Onboarding/HoldUnitsUntilSignalTests.LevelStart.cs` (+ `.meta`), the 7 option tests.
- `Features/Onboarding/Editor/MissionWiring.HoldTheYard.Mark.cs` (+ `.meta`).
- `Features/NPCs/Rock/Prefabs/Unit_Rock_Stone4.prefab` (+ `.meta`): three notches use stone0..3; the level's instance and its `stone4` group were removed first.
- `Resources/Sequences/M3Yard/`: 14 assets (+ `.meta`) with no slot left: `M3Yard_Start_CameraOnMasher`, `_CameraOnEastWall`, `_CameraOnMark`, `M3Yard_Start_Mark_DialogNodeSequence`, `M3Yard_Notch3_Mark_DialogNodeSequence`, all seven `M3Yard_Notch4_*`; and the two step lists whose structure changed (`M3Yard_Start_SequentialSequence`, `M3Yard_Notch3_SequentialSequence`), which the wiring then re-created (it never rewrites an existing step list).

**Assets (written by a one-off script, then by `Apply Wiring`):**
- `Content/Levels/Greybox/GB_m3-defence.prefab`: edited in place, not rebuilt. One-off editor script (run once through MCP `execute_code`, not kept in the repo): removed `Unit_Mark` and his "Mark on the stone" hold object (all his instance data goes with him: tags, the switched-off role, the hold); removed the `Unit_Rock_Stone4` instance and the `stone4` group; placed three `Unit_DarkClaw` on 3,11, 4,11, 5,11 and `Unit_Placeholder` on 4,8 exactly as the grid-to-level builder places them (under the cell's occupant root at its centre; the slot faces right; the Claws on columns 3 and 4 face right, as the builder's facing rule gives with the family's centre at column 4.5); switched the Masher off and listed it in a new group `masher` (after `toba`, the block's order); took `Mark_Linda_Duo_Ability` and `Mark_Lucy_Duo_Ability` out of the sisters' level lock entries. Then `Apply Wiring` (stages, defeat, hold, sequences, factors). `git diff --numstat`: +5984 / −2866 against HEAD (the path is reused by the 7.1 rebuild).
- `Content/Levels/M2 - The Trail.asset`: against HEAD, only the graph payload line (the new level's GUID). `freeSlotsCount` is back to 1.
- `Resources/Sequences/M3Yard/`: 47 assets now (new: `M3Yard_Start_CameraOnStone`, `_CameraOnWestLane`, the four `M3Yard_Cave_*`, the seven `M3Yard_Push_*`, `M3Yard_Notch3_RollAway`, `_ReleasePick`, `_Pick_DialogNodeSequence`).

**Criteria**
- [x] **Layout kept.** Not rebuilt: the one-off edit changes only what the block changes. Opening Claws on 3,11 4,11 5,11 in play; deploy slot on 4,8; no Mark; the Masher hidden at 6,1 in `masher`. Barricades, w1 in play, w2/w3 hidden, mushrooms, the Sword, the Stranger stone on 4,12 and Toba hidden are as built. Tests: `TheTilesAndUnitsMatchThePaperBlock` (now with `P` for the slot), `ThreeClawsStandAtTheStoneInPlay`, `TheSistersStandOnTheirTilesWithOneDeploySlotForThePick`, `NeitherPickIsPlacedInTheLevel`, `TheMasherWaitsHiddenAtTheBottomOfTheEastLane`, `TheBuildBlockParsesCleanWithTheLevelLines`, plus the unchanged barricade, wave, mushroom, stone, Toba, relation and sword tests. Read-back below.
- [x] **Roster:** one free seat, fixed Linda and Lucy. Tests: `TheRosterIsTheTwoSistersAndOneFreeSeatForThePick`; HEAD's `OnboardingMissionGraphTests`, `SearchTrailTests.TheRosterIsTheSistersPlusOneFreePickAndTheItemsArePacked`, `PickOnTilesLOConditionTests` ("a free seat for the pick") pass again.
- [x] **Mark's 7.1 instance data is gone;** `holdFromLevelStart` and its tests dropped; `HoldUnitsUntilSignal.cs` is HEAD's. Test: `NeitherPickIsPlacedInTheLevel` (no Mark, no level-start hold).
- [x] **Stages** (all queued, six):
  - S1 "Clear the yard.": `EntitiesDestroyed` (Enemy, All) on the three opening Claws; w1 isn't listed. End: input off, camera on the stone, the pick's line, camera back, input on. Test: `StageOneIsTheThreeClawsAtTheStoneDeadAndItsEndShowsTheStone`.
  - S2 "{pick_0}: push the stone.": one shown objective, `PickOnTilesLOCondition` (4,11) then `TilesOccupiedLOCondition` (Bergsons, 4,11), All, so 4,11 lights as a goal and only the pick completes it. End: input off, **`M3Yard_HoldPick` signal first**, camera on the east lane, the Masher revealed (`masher`), camera on the pick at the stone, the dialog (pick, then Linda), camera back, input on. Tests: `StageTwoIsThePickOnThePushTileLitAsAGoal`, `StageTwosEndHoldsThePickThenBringsTheMasher`.
  - S3–S5: `TurnReachedLOCondition` (Bergsons, `turn = 1`) each, as 7.1; texts "Hold them off. 3 turns left.", "Hold them off. 2 turns left.", "Hold them off. Last turn.". Ends: notch 1 + w2, notch 2 + w3, notch 3 + roll away (stone3 hides) + **`M3Yard_ReleasePick` signal** + the pick's line. Tests: `EachHoldStageIsOneFamilyTurnStart` (×3), `EachHoldStageEndMovesTheStoneANotch` (×3; the release comes after the roll-away, and no signal on notches 1 and 2).
  - S6 "Finish them.": living Enemy ≤ 0. Outro as built. Tests: `TheLastStageIsEveryEnemyDead`, `TheOutroFadesTheTallyThenBringsTobaOut`.
  - The hold component: one, on "The pick at the stone", wired to both signals. Test: `ThePicksHoldListensForTheHoldAndTheReleaseSignals`.
- [x] **Loss:** second defeat group from level start, Any with the template's. Its objective is `PickFallenLOCondition` alone, "Keep {pick_0} standing.", shown, and **names the pick**: the condition now exposes `{pick_i}` (T-P4, D-756). Tests: `TheLevelIsLostWhenNoBergsonStandsOrThePickFalls`; `PickFallenLOConditionTests` (the fall, moved by 7.1, plus `TheWatchedPickIsExposedByName` and `AConditionWithNoPickExposesNothing`). The template defeat ignores the held pick through 8.2's runtime `IgnoreObjective`. "{pick} has fallen." is 8.4's.
- [x] **Stone notches:** 3. Variants used: `Unit_Rock_Stone0` (start), `Stone1` (notch 1), `Stone2` (notch 2), `Stone3` (notch 3, then rolls away). `Unit_Rock_Stone4` is no longer needed and is deleted. Tests: `TheStoneVariantsAreNeutralRocksTitledStoneEachFurtherToTheSide` (4), `EachStoneWaitsHiddenOnTheStoneTileInItsOwnGroupInTheStonesFaction` (also: no fifth prefab, no `stone4` group).
- [x] **Idempotent:** `Apply Wiring` run twice after the final state; md5 of all 104 written files identical (the level, `_v1`, the mission, every rock/barricade prefab, all 47 M3Yard assets + metas, the pile's end list). The second run logged no warning and no mission change. The covering run and the full suite left them md5-identical too. After the follow-up (D-756) the first run changed only `GB_m3-defence.prefab` (the defeat objective down to one condition); the second run was md5-identical on all 104 files again.
- [x] **Tests:** see below.
- [x] **Report on T-P2, T-P4, T-P5, Inactive targets:** Findings below.

**Tests** (THJ's open editor, MCP test jobs; both started and finished cleanly this time):
- Covering fixtures, `MISO.Core.Features.Onboarding.*` + `MISO.Core.Levels.*` + `BondSourcesTests`: **856 total, 856 passed**, 0 failed; after the follow-up (D-756): **858 total, 858 passed**. Includes `M3DefenceTests` (42 cases), `HoldPickOutOfCombatTests`, `HoldUnitsUntilSignalTests` (HEAD's 14), the pick-condition classes, `OnboardingMissionGraphTests`, `SearchTrailTests`, `HomeVisitsTests`, `M4WhiteMothersTests`, the M1 Ridge tests.
- **Full EditMode suite: 2923 total, 2922 passed, 0 failed, 1 skipped** (`AIRegressionTest.Baseline_MatchesCurrentAI`, Explicit); after the follow-up (D-756): **2925 total, 2924 passed, 0 failed, 1 skipped** (the same Explicit test). Last recorded 2899 (8.1); the difference is 8.2's new tests plus this chunk's changes (−7 option tests, M3 tests reshaped).
- `AIRegressionTest` not run (the verifier's). Expect one line fewer than 7.1's 52: `units.unexpected Unit_Rock_Stone4.prefab` should drop out; `Unit_Barricade` stays.

**`M3DefenceTests` changes:** removed the five Mark tests, `JohnsDrawnTileIsPlainFloor`, `NothingOfTheSquadPickIsLeftInTheLevel`, `FiveQueuedStages…`; added `NeitherPickIsPlacedInTheLevel`, `TheSistersStandOnTheirTilesWithOneDeploySlotForThePick`, `TheRosterIsTheTwoSistersAndOneFreeSeatForThePick`, `TheMasherWaitsHiddenAtTheBottomOfTheEastLane`, `ThreeClawsStandAtTheStoneInPlay`, `SixQueuedStagesFromTheYardToTheLastClaw`, `StageOneIs…`, `StageTwoIs…`, `StageTwosEndHoldsThePickThenBringsTheMasher`, `ThePicksHoldListensForTheHoldAndTheReleaseSignals`; reshaped the block, level-start, stone, lock, hold-stage, notch and defeat tests. The lock test now also checks that Mark's Duos are **not** locked for the sisters at level start.

**Read-back** (`python claude-handoff/tools/level_to_grid.py Content/Levels/Greybox/GB_m3-defence.prefab`):

```grid id=src-gb_m3-defence title="Source: GB_m3-defence (offset x+0, y+0)"
_ _ _ _ T _ _ _ _
_ _ _ c c c _ _ _
. . . . . . . . .
. . . . . . . . .
. . L . . . . U .
. . . . . . . . .
. . . _ _ _ . . .
. . . _ _ _ . . .
. * . _ _ _ . . *
. . . _ _ _ . . .
. . . _ _ _ O O c
c c c _ _ _ O O c
c . c _ _ _ . . c
--
note 0,6 Unit_Barricade
note 1,6 Unit_Barricade
note 2,6 Unit_Barricade
note 4,12 Unit_Rock_Stone0
note 4,12 Unit_Rock_Stone1
note 4,12 Unit_Rock_Stone2
note 4,12 Unit_Rock_Stone3
note 4,8 deploy slot
note 6,6 Unit_Barricade
note 7,6 Unit_Barricade
note 8,10 DR_PickUp_HeavenlySword
note 8,6 Unit_Barricade
level hidden toba 4,12
level hidden masher 6,1
level hidden w2 8,0 8,1
level hidden w3 0,0 2,0 8,2
```

Tool notes: Defence, 82 tiles, Early, all alert. Objectives: Clear the yard. / {pick_0}: push the stone. / Hold them off. 3 turns left. / 2 turns left. / Last turn. / Finish them. / Keep {pick_0} standing. Placed: 11 Dark Claws, Linda, Lucy, the Masher, `Unit_Placeholder`, Toba, stone0..3, 6 barricades, 2 mushrooms, the sword pickup. The stone groups read as "a listed unit that is not a placed unit" (the tool's known gap with the stone variants, as in 7.1).

Against block `m3-defence-4`: `#` reads `_`; `c@` on 4,11 reads `c` (the `@` is a drawing aid); the deploy slot is a note, not a glyph; barricades and stones are notes. Tiles, units, hidden groups (`toba`, `masher`, `w2`, `w3`) and the deploy tile match. No difference otherwise.

**Placeholder lines** (seeded once into new dialogue assets; 8.4 replaces them; texts carried over from 7.1, none new):
- Level start (`M3Yard_Start_Linda_DialogNodeSequence`, kept from 7.1, Linda): "Keep them off him!" — the slot for M3.0.6; the text is 7.1's and doesn't fit the level start yet.
- S1 end (`M3Yard_Cave_Pick_DialogNodeSequence`, pick slot): "There's a cave behind that stone. I'll shift it." (7.1's `MarkStartLine`) — slot for M3.0.2.
- S2 end (`M3Yard_Push_DialogNodeSequence`): pick slot "It's moving... keep them off me!" (7.1's notch-3 line), Linda "Keep them off him!" — slots for M3.0.3 (per-pick text is 8.4's) and M3.0.4; M3.0.1 (Linda on the Masher) and M3.0.5 need nodes added by 8.4.
- Notch 1 / 2 barks: kept (Lucy "More from the east!", Linda "Both sides now!"). No pick notch line on notches 1–2 yet (M3.1.1, M3.1.3 are new slots for 8.4).
- Notch 3 (`M3Yard_Notch3_Pick_DialogNodeSequence`, pick slot): "It's open! The big one's at the wall!" (7.1's notch-4 line) — slot for M3.1.4.
- End: kept.
- Objectives (final, from `design/m3-text.md`): "Clear the yard.", "{pick}: push the stone.", "Hold them off. 3 turns left.", "Hold them off. 2 turns left.", "Hold them off. Last turn.", "Finish them.", "Keep {pick} standing." (written `{pick_0}`, the key the conditions expose).

**Findings (all from reading the code; nothing played)**

- **T-P2: the Masher's 2×2 reveal when a footprint cell is taken.** `HiddenLevelUnits.RevealUnit` switches the unit on, initializes it and calls `GridCell.PlugEntity` on its anchor 6,1. `PlugEntityInternal` checks the whole footprint (`TryGetFootprintCells` + `GridPluggableEntity.CanOccupy`: every cell of 6..7 × 1..2 must exist and have no other occupant). If any is taken, `GetNearestPluggableCell` walks breadth-first over adjacent cells from 6,1 and takes the first anchor whose full 2×2 exists and is free, and the Masher slides there (`translateToPosition`). In this lane the likely fallbacks are 6,0, 7,0/7,1 (8,x is a tile) or 6,2–6,3; never column 5 or lower (no tiles at 3..5 below row 7, so the footprint fails). If no anchor fits anywhere, it is switched off again with a warning and never comes in (the stage still completes; nothing waits on it). Family units can walk through the barricades into the lane, so a sister standing in 6..7 × 1..2 at the push shifts the Masher one or two cells. Not fixed, as asked. Hidden units (w2 on 8,0/8,1) don't block it: they are inactive and not plugged.
- **T-P4: can `{pick}` show in a defeat objective?** Before this chunk, **no**: `PickFallenLOCondition` did not override `ExposeVariables`, so "Keep {pick_0} standing." would have shown the key. Defeat objectives build their text through the same `LevelObjective.UpdateDisplayText` as stages (each condition's `{key_<index>}`), so the fix is on the condition. Coordinator decision (D-756): `PickFallenLOCondition` now exposes `{pick_i}` the way `PickOnTilesLOCondition` does: the watched pick's nickname once seen; before the first evaluation, the first living free pick of the faction (none with no fixed seat); the last name is kept after the fall. The defeat objective is `PickFallenLOCondition` alone, "Keep {pick_0} standing.". (My first hand-off used a never-true `PickOnTilesLOCondition` beside it; that workaround is removed.) Standalone play from the toolbar (no mission, no fixed seats) shows no name: the key stays in the text there. The AI planner still makes no plan from the condition.
- **T-P5: Chained Assault range.** The target pick is the trigger preset `Mark_Lucy_Duo_Ability` (both `Unit_Lucy` and `Unit_Mark` carry it), `radiusV` constant **5** (not 4), selecting cells around **the unit that starts the Duo** (the caster of the trigger). If Lucy starts it from her bar, the range is measured from Lucy; if Mark starts it, from Mark. `Mark_Lucy_Duo_TargetAdjust` then hands the collected targets to both sides; Mark's ghost blitz (`ActivateMarkLucyBlitz`) hits each in turn by distance from Mark, with no range check of its own (his side's 2 × RANGE radius isn't applied to the handed-over targets). So the design's "Lucy on 4,9 has all three within 4" holds with margin (5). The cell count is capped by `_controller.TargetCellCount` and the trigger's `RequiredTargetCount`.
- **Do enemies attack an Inactive unit? Yes.** Nothing filters a turn-skipped (`Status.Inactive`) or objective-ignored unit out of enemy targeting: targets go by faction relation. `IsUnitTurnSkipped` is read by the AI only for its **own** units' turn order (`AIFactionBrain.UpcomingTurnOrder`), by the Masher's counter/preview for the Masher itself, by Catch & Return (8.2) and by the player controller. `IsUnitIgnoredForObjectives` is read by `LivingUnitsLOCondition` only. So a held pick is attacked and shown in next-targets like any family member; the template defeat's `LivingUnits` influence still makes every living Bergson (the held pick included) an AI pull, as in every level. `PickFallenLOCondition` and the naming `PickOnTilesLOCondition` add no pull (no planner handler).

**Decisions (8.3)**
- **The prefab edit as a one-off script, not as wiring.** `BlockDocument` is now `m3-defence-4`, so `Build Level` (only for a missing prefab) would build the same layout; the wiring keeps owning what it owned. The edit placed units the way the builder does, so a rebuild and this edit agree. Same behaviour as "edit only what the block changes".
- **The defeat names the pick through `PickFallenLOCondition.ExposeVariables`** (coordinator decision D-756, replacing my first workaround). The watch struct gained a read-only `Pick`; a static `PickVariable(index, nickname)` builds the variable (tested). No statics with state; main thread only, like the rest of the condition.
- **The hold signal is the first step of S2's end, right after input goes off,** before the Masher camera, so the pick is out of combat before anything else happens. The release comes after the roll-away and before the pick's line on notch 3.
- **Sequence slots:** level-start Linda dialog kept (slot for M3.0.6); new pick-slot dialogs for S1, S2 and notch 3, seeded with 7.1's placeholder texts, not new lines. 7.1 dialogs with no slot (Mark start line, notch 3/4 Mark lines) deleted rather than reused, because their speaker is `Who.Mark` and a seed never changes on an existing asset. `design/m3-text.md` §D8 lets the tech plan rename slots.
- The Linda–Lucy Duo stays the only level-start Duo lock; the 7.1 Mark Duo locks were removed from the asset once by the one-off script (the wiring only adds locks, never removes them).
- `MissionWiring.HoldTheYard.Mission.cs` now writes one free seat, so a re-run puts it back if someone changes it; same asset value as HEAD.
- Kept `PickFallenLOConditionTests.cs` (7.1 moved HEAD's three fall tests there) rather than moving them back into `M3DefenceTests`.

**Risks and loose ends (8.3)**
- **The Masher close-up** (EN-10) is expected to play on first sight when `masher` is revealed in S2's end, inside the sequence with input off. Not checked: whether `EnemyIntroductionController` fires for a unit revealed mid-sequence, and whether it overlaps the camera step. Play check.
- **S2 completes during the family turn the pick ends its move on 4,11.** The hold then runs during the pick's own open turn; 8.2 handles that (`NotifyTurnStarted(true)`, leftover AP not drained but unusable). Play check that the pick greys out at once.
- **Hold during the S2 sequence vs. Family Super Time:** if Super Time is running at that moment, 8.2 defers the role suppression until it ends. Unlikely at a stage end. Play check.
- **The pick on 4,11 before the yard clears** (the design's "parks on 4,11"): S2 is first evaluated right after S1's sequence, completes at once, and the hold follows. Fine by design.
- **Standalone play from the level toolbar** (no mission): `{pick_0}` names the first living Bergson and the fall never triggers; the deploy slot has no roster to fill it. Use the Trail from a save for the play check.
- **Stale managed-reference overrides in the level's YAML.** The level is a variant of the level template, so its objectives are stored as property overrides. Overrides for conditions no longer used stay in the file (Unity doesn't drop them): the removed never-true condition (`managedReferences[…794]`), a `conditions.Array.data[1]` entry past the defeat objective's size of 1, and older ones from 7.1 (Mark's `EntitiesDestroyed`). They are ignored at load (not referenced, or beyond the array size); the tests read the objective as one condition. Unity's "remove unused overrides" would clean them but also rewrites unrelated overrides, so I left it.
- **Placeholders that don't fit yet** (level start "Keep them off him!", the push line) until 8.4.
- **Editor note:** deleting `M3Yard_Start_SequentialSequence` / `M3Yard_Notch3_SequentialSequence` on disk and re-creating them in the same session left two empty step lists the first time (Unity reused the stale in-memory objects). I deleted them again after a refresh and re-ran the wiring; they are filled now and tested. If anyone deletes and re-creates a wired step list, refresh in between.
- Not staged/touched: THJ's `LevelM2-C1.prefab`, `PreloadScreen.unity`, `ProjectSettings/*`, `Content/FamilySuperTime/DUO/Inserts/`, the TMP fallback font, `M3Defence_Notch3_HideLastStone.asset` (+ .meta). 8.1/8.2 files untouched (no bug found in them).
- Save reset: no.

**How to see it (8.3)**
1. Play stopped. Everything is applied. To re-apply: **Tools › Onboarding › Hold the Yard: Apply Wiring** (safe to re-run; changes nothing on applied data).
2. Open `Content/Levels/Greybox/GB_m3-defence.prefab`: three Claws in the alcove (3,11 4,11 5,11), the `Unit_Placeholder` on 4,8, Linda 2,8, Lucy 7,8, no Mark; the Masher at the bottom of the east lane switched off (listed in `HiddenLevelUnits` › `masher`); the object "The pick at the stone" with `HoldPickOutOfCombat` (push tile 4,11) and two `SignalAction`s.
3. From a cleared save, play to the Trail; the roster screen offers one free seat: pick John or Mark.
4. Level start: the camera shows the Claws at the stone, the west lane (w1 walking), the yard; objectives "Clear the yard." and "Keep John standing." (or Mark).
5. Kill the three alcove Claws (w1 doesn't count): camera on the stone, the pick's line, 4,11 lights, "John: push the stone.".
6. Walk the pick onto 4,11: input off, the pick greys out at once (no Role zone, Duos with the pick gone from the sisters' bars, Papa's Shelter off for John), the camera goes to the east lane and the Masher comes in with its close-up, the lines, "Hold them off. 3 turns left.".
7. Next three family turn starts: notch + w2, notch + w3, then the stone rolls away, the pick is released with a full turn, "Finish them.". Enemies should be able to hit the held pick.
8. Let the pick fall at any point: the level is lost and the loss panel lists "Keep John standing" as failed.

#### Should-fix follow-up (after the 8.2+8.3 review)

- Pick fallback guard: `HoldPickOutOfCombat.FindPick`'s fallback now goes through a new `public static GUnit FirstPick(IEnumerable<GUnit> units, ICollection<string> fixedSeats)`. It returns null when there is no fixed seat (or none given), the same guard `PickFallenLOCondition.FindPick` has, so a level played without a mission holds nobody instead of the first unit. The `pushTile` path is unchanged. The `pushTile` tooltip says so. Tests: `HoldPickOutOfCombatTests.FirstPick_NoFixedSeat_IsNobody`, `FirstPick_IsTheFirstLivingUnitOutsideTheFixedSeats`.
- Behaviour tests:
  - `WouldCatch`: `CatchHeldCatcherTests.WouldCatch_IsFalseWhileTheCatcherIsHeld_AndTrueOnceBack`. Full rig: Mark at 0,3 and Linda at 0,0 on grid cells, the same faction, the catch unlocked through the faction tracker, a QTE binding, a real `PlayerController` skip query. Unheld it returns true (the control), held false, true again once the inactive tag goes.
  - `TryCatch`: not rigged. Past the held check it needs a live `Projectile` (owner, prefab source, direction), then it freezes the arrow and runs the return-hit count. A held-only test would pass without the gate too, so I didn't add one. It uses the same `IsCatcherHeld` check as its third line, before any arrow check. Left for the play check: Linda shoots through a held Mark, and the arrow flies on.
  - Papa's Shelter: `PapasShelterReenableTests.SwitchingBackOn_NextToJohn_ShelterComesBack`. Lucy's cell lists John's as adjacent, and both units are in a real `PlayerController`'s faction. Sheltered on enable, the `Status.Sheltered` tag gone on disable, back at once on re-enable with nobody moving.
- Files: no new files. Changed again: `HoldPickOutOfCombat.cs`, `HoldPickOutOfCombatTests.cs`, `CatchHeldCatcherTests.cs`, `PapasShelterReenableTests.cs`. The commit 2/3 file lists stay as they are.
- Runs (THJ's editor, Test Runner through MCP):
  - Covering fixtures `MISO.Core.Features.Onboarding` + `MISO.Core.Features.Bergsons.EditorTests` (Mark, Lucy) + `MISO.Content.Levels.EditorTests` (AbilityLock): 1688 tests, 1687 passed. The 1 failure was the new shelter test using an unregistered tag id; switched to the real `Status.Sheltered`.
  - Full EditMode suite after that fix: 2929 total, 2928 passed, 0 failed, 1 skipped (`AIRegressionTest.Baseline_MatchesCurrentAI`, Explicit). Previous run: 2925 (+4 new tests).

### Chunk 8.5: Core: big units can walk north and east

Status: **done; core review APPROVE** (two should-fixes in the test file, applied below). Fixture, full suite and AI regression run after THJ reconnected the Unity bridge (the first attempt lost the bridge after the recompile; the later runs dropped the session a few times mid-run but each job finished). Core change (grid): Tier 2 bugfix inside a core system, approved by THJ (D-758).

**The change** (`Core/Systems/GridSystem/Runtime/GridCell.cs`, `GetRangeCells`, the `!includeSelf` exit after the BFS/straight/ranged-reach pass): when the source's `EffectivePlacementSize` is bigger than 1x1, only the anchor (`source.CurrentCell`, compared with `ReferenceEquals`, worker-safe) is removed; a 1x1 source still removes `source.Occupies` exactly as before. The Unconstrained branch (attack ranges from every footprint cell) returns earlier and is untouched. File stays UTF-8 with BOM, LF (as it was). No new statics, no Unity-object API added.

**End-to-end check (code read; nothing else needed changing):**
- BFS and straight ranges already step over the mover's own cells: `PassesPathWalk` → `IsFootprintWalkable` and `PassesEmptyFilter` → `IsFootprintEmpty` skip cells the mover occupies. The final `RemoveAll(source.Occupies)` was the only thing taking N/E away.
- `FindPath(mover)`: the goal check is `mover.IsFootprintEmpty(goal)` (own cells skipped), so a path to the N/E anchor is one step, cost 1. The transporter's walk loop unplugs before each step and re-checks `IsFootprintEmpty`/`IsFootprintWalkable`, then `PlugEntity` on the new anchor: fine.
- AI `CanEndOn`: `IsFootprintEmpty` (+ the clearing guard): accepts it. `GetAbilityCandidateTargets`' relation pre-filter keeps a self-occupied cell when the walk's `ignoreRelationOnSelection` is 0 (Masher and Queen walks both 0). `FactionControllerBase.FilterSelectableCells` likewise.
- `IsLegalAbilityTarget` / the target-selection apply condition: `OccupantIntersects(range)` is true for the N/E anchor (the cell itself is in range).
- Who moves: only `Unit_MasherGoblin` (2x2) and `Unit_GoblinQueen` (1x2) are bigger than 1x1. Both walks (`MasherGoblin_Ability_Walk`, `GoblinQueen_Ability_Walk`) and the Queen's jump (`GoblinQueen_Ability_Jump`) are **PathWalkable** targeted ranges (`cellApplyWalkabilityMode: 1`), so the Masher's walk and the Queen's walk and jump now also offer the N (and for the Masher E) anchor. Threat previews (`UnitThreatAnalysis.GetReachableCells`, includeSelf on) were already showing footprint cells and are unchanged.

**AI next-targets prediction (`AIUnitBrain.cs:291-318`, `sim != null`): does NOT agree; gap reported, not fixed.** It ranges from each footprint cell as if 1x1 with no source, unions, and removes the footprint. For a 2x2 at (0,0), radius 1, it offers (-1,0), (0,-1), (-1,1), (0,2), (1,-1), (2,0), (1,2), (2,1) as anchors; the live range is (-1,0), (0,-1), (1,0), (0,1). So it misses N/E and offers diagonal and two-step anchors (CanEndOn then filters by footprint, not by reach). It is not the same small rule: a correct fix needs a source-aware range from a virtual origin (`GetRangeCells(source:)` uses the live `CurrentCell`, and `IsFootprintEmpty` skips cells occupied at the live position, not at the simulated one). Suggest a separate small core task.

**Tests** (new `Core/Systems/GridSystem/Editor/MultiCellWalkRangeTests.cs`, + `.meta` made by Unity; BOM + LF like the folder, `.gitattributes` resolves `eol=lf`; hand-built grid, no level). After the review, `AIWalkCandidates` asserts the walk's radius is at least 1 so a radius-0 light setup fails clearly:
- `ATwoByTwoUnit_RadiusOne_ReachesItsFourAnchors_ButNotItsOwn` (PathWalkable)
- `ATwoByTwoUnit_SelfWalkableAndStraightRanges_AlsoReachNorthAndEast`
- `AOneByTwoUnit_RadiusOne_ReachesItsFourAnchors_ButNotItsOwn`
- `AOneCellUnit_RangeIsUnchanged` (radius 1 and 2 with a blocker; own cell never offered)
- `ATwoByTwoUnit_AnOccupiedCellUnderTheNewFootprint_StillBlocksThatAnchor`
- `ATwoByTwoUnit_FindsAOneStepPath_ToAnAnchorUnderItsOwnFootprint` (`FindPath(mover)`, length 2, cost 1)
- `TheMashersWalk_OffersTheAINorthAndEast` and `TheQueensWalk_OffersTheAINorth`: the real prefabs (isolated copies, light ability setup), `ComputeTargetSelectionCells` + the brain's `CanEndMoveOn`, as the Cyclone heavy tests do.

**Runs** (THJ's editor, Test Runner through MCP):
- `MISO.Core.Systems.GridSystem.EditorTests.MultiCellWalkRangeTests`: 8/8 passed (with the radius assert; both prefab walks have radius >= 1).
- Full EditMode suite: 2939 total, 2938 passed, 0 failed, 1 skipped (`AIRegressionTest.Baseline_MatchesCurrentAI`, Explicit). Previous run 2931 (+8 new tests).
- `AIRegressionTest.Baseline_MatchesCurrentAI` by name: fails as expected, `CHECKS: 738  FAILURES: 51`, the same as the last recorded run (51, 8.3 verification). No new or removed lines: the checks count is unchanged and the failure set has the same lines as that record (`intent.condition-count`, `intent.unit-tile.enemy`, the graph count/node/edge/fingerprint lines, `abilities.count` and the `abilities.unexpected` lines, `abilities.evaluator Mark_Lucy_MARK_Duo_Ability`, `units.count` 21/29, `units.missing Unit_Placeholder`, the `units.unexpected` lines (StuntCamActorSet, Unit_DarkClaw_StartsAlert, Unit_Barricade, Unit_Rock, Unit_Rock_Stone0..3, Unit_DarkClaw_Hearth), the 7 `units.ability` lines, and the final `fatal` NullReferenceException in `AIStrategyPlanner.HandleLivingUnitsCondition`). No Masher or Queen line. Caveat: 8.3 recorded only the count and the line kinds, so the line-by-line comparison is against that description, not a saved list; and the `fatal` stops the run in `RunStress`, so whatever the test would check after it never runs. Not fixed, not re-baselined.

**Loose ends:**
- `OccupantIntersects` now also passes the mover's own anchor and any footprint cell when its footprint touches the range, so a *player-controlled* big unit could pick "walk to my own cell" (the transporter then does nothing: cost 0). No big unit is player-controlled today; the AI never offers it (the anchor is not in its range).
- A walk preset with `ignoreRelationOnSelection` including Ally would still drop the self-occupied N/E anchors (AI pre-filter and `FilterSelectableCells`). Masher and Queen are 0.
- `AEffectCompound.GatherSurrounding` passes a multi-cell `src` with the effect's walk mode; such an effect would now include the big unit's non-anchor footprint cells. No Masher/Queen compound uses a walk mode (all Unconstrained), and the walk-mode compounds in the project are summons/spawners around 1x1 owners.
- The plans' "the Masher steps to 6,3" note needs the timing fix the code read mentions (coordinator/designer).

**Draft line for `tech/core-systems.md` (Grid row):** Since 2026-11-26 (D-758, uncommitted until THJ's M3 play check): `GridCell.GetRangeCells` with `includeSelf` off and a source bigger than 1x1 removes only the anchor (`source.CurrentCell`) on the walk path (PathWalkable/SelfWalkable), not every occupied cell, so the Masher (2x2, PathWalkable walk) and the Goblin Queen (1x2, PathWalkable walk and jump) can walk or jump one step north/east onto anchors under their own footprint. 1x1 sources and the Unconstrained branch (attack ranges) unchanged. The AI's simulated next-targets range (`AIUnitBrain.GetAbilityRangeCells`, sim path) still treats the footprint as 1x1 starts: open item.

**Proposed commit** (core only, its own commit, before commit 4): `fix(core): big units can walk onto tiles their own footprint covers`
- `miso/Assets/_Project/Core/Systems/GridSystem/Runtime/GridCell.cs`
- `miso/Assets/_Project/Core/Systems/GridSystem/Editor/MultiCellWalkRangeTests.cs`
- `miso/Assets/_Project/Core/Systems/GridSystem/Editor/MultiCellWalkRangeTests.cs.meta`

### Chunk 8.4: the approved M3 lines

Paths under `miso/Assets/_Project/`. New `.cs` files LF, no BOM, like the rest of `Features/Onboarding`. Worked in THJ's open editor through Unity MCP; no Play session; Play mode off throughout.

**Changed / new (code):**
- `Features/Onboarding/PickLineDialogSequence.cs` (+ `.meta`, new): the per-pick text option. A `DialogNodeSequence` whose own lines are the default; `entries` (nickname to dialogue) override it for that pick; the pick is read from the mission's generic dialogue slot (`MissionTracker`, slot 1 by default) at play time, nothing in an asset is mutated. Static `Choose(entries, nickname)` is the tested part. Being a `DialogNodeSequence`, a step list's skip still fast-forwards it.
- `Features/Onboarding/UnitsReachTilesSequenceTrigger.cs` (+ `.meta`, new): the west-wall trigger (below).
- `Features/Onboarding/PickFallenLOCondition.cs`: two serialized lines (`standingLine`, `fallenLine`) and a `{pickline_i}` variable (standing line until the pick has fallen, fallen line after; `{pick}` inside a line becomes the nickname). Empty lines expose nothing new, so the old behaviour is unchanged.
- `Features/Onboarding/Editor/MissionWiring.HoldTheYard.Lines.cs` (+ `.meta`, new): every line constant, `BuildPickLine`, `BuildPushRule`, `BuildWestWall`, `WireWestWallWatch`.
- `Features/Onboarding/Editor/MissionWiring.HoldTheYard.Sequences.cs`: old stand-in constants removed; level start is stone + Linda's line + back; cave, push (Masher line, push rule, sisters), notch pick lines, end talk with per-node speakers (`SpeakAsToba` takes the node list), west-wall sequence added.
- `Features/Onboarding/Editor/MissionWiring.HoldTheYard.cs` (`PickObjective` is now `{pickline_0}`; the watch is wired) and `...Pick.cs` (the defeat condition gets the two lines).
- Tests: `Editor/M3DefenceTests.cs` (now `partial`, updated), `Editor/M3DefenceTests.Lines.cs` (+ `.meta`, new), `Editor/PickLineDialogSequenceTests.cs` (+ `.meta`, new), `Editor/PickFallenLOConditionTests.cs` (+4).

**Assets:** `Content/Levels/Greybox/GB_m3-defence.prefab` (the "West wall watch" object; the defeat condition's lines) and `Resources/Sequences/M3Yard/` (dialogues and step lists recreated; `M3Yard_Start_CameraOnWestLane` removed; new `M3Yard_Push_Masher_*`, `M3Yard_Push_Rule_PickLineDialogSequence` (+ its `_John_` entry dialogue), `M3Yard_Notch1/2_Pick_*`, `M3Yard_WestWall_*`). Dialogues are seeded once, so I deleted every M3Yard dialogue and step list (all untracked, still placeholders, no hand edits to keep) with the Unity asset-delete tool and ran `Apply Wiring`, as 8.3 did. Sides follow the text file: Linda left; Lucy, Toba and the pick right.

**Line ID to slot** (all asserted word for word in `M3DefenceTests.Lines.cs`: `TheLineTextsAreTheApprovedOnes` plus the slot tests):

| ID | Slot (asset in `Resources/Sequences/M3Yard/`) | Test |
|---|---|---|
| M3.0.6 Linda | level start, `M3Yard_Start_Linda_DialogNodeSequence` | `TheLevelStartHasOnlyLindasLine` |
| M3.0.7 Lucy, M3.0.8 Linda | `M3Yard_WestWall_DialogNodeSequence`, played by the west-wall trigger | `TheWestWallPairPlaysWhen...`, `TheWestWallPairIsInNoStageAndNotAtTheLevelStart` |
| M3.0.2 pick | S1 end, `M3Yard_Cave_Pick_DialogNodeSequence` | `TheYardClearedGivesThePickTheCaveLine` |
| M3.0.1 Linda | S2 end, after the Masher reveal, `M3Yard_Push_Masher_DialogNodeSequence` | `ThePushPlaysLindaThenThePicksRuleThenTheSisters` |
| M3.0.3 pick (Mark text default, John entry) | S2 end, `M3Yard_Push_Rule_PickLineDialogSequence` | `ThePushLineHasAJohnTextAndMarkIsTheDefault` |
| M3.0.4 Linda, M3.0.5 Lucy | S2 end, `M3Yard_Push_DialogNodeSequence` | same as M3.0.1 |
| M3.1.1 pick | notch 1, `M3Yard_Notch1_Pick_*`, between the stone move and w2 | `TheNotchesGiveThePickItsLines...`, `EachHoldStageEndMovesTheStoneANotch` |
| M3.2.1 Lucy | notch 1 wave bark, `M3Yard_Notch1_Bark_*` | same |
| M3.1.3 pick, M3.2.2 Linda | notch 2, `M3Yard_Notch2_Pick_*`, `_Bark_*` | same |
| M3.1.4 pick | notch 3, `M3Yard_Notch3_Pick_*` (always plays) | same |
| M3.5.1, M3.5.2 | end, `M3Yard_End_StillCounting_*`, `_No_*` (around the tally fade) | `TheOutroFadesTheTallyThenBringsTobaOut` |
| M3.5.3 to M3.5.9 | one dialogue `M3Yard_End_Toba_*`: Toba, Linda, Toba, Toba, Lucy, Toba, pick (M3.5.9 through the pick slot, not a named hero) | `TheOutroFades...`, `TheEndTalkSpeakersFollowTheLineMap` |
| M3.6.9, 6.10, 6.2 to 6.5 (objectives) | unchanged from 8.3, checked against the text | `TheObjectiveTextsAreTheApprovedOnes` |
| M3.6.6, M3.6.7 | defeat objective, see below | `TheLevelIsLostWhenNoBergsonStandsOrThePickFalls`, `PickFallenLOConditionTests` |
| M3.6.8 Barricade | unchanged title | `TheObjectiveTextsAreTheApprovedOnes` |
| M3.3.x, M3.4.x barks | **not wired**, see below | |

`EveryDialogueInTheYardFolderSaysAnApprovedLine` fails if any other text is left in a dialogue.

**The west-wall trigger.** New small Onboarding component `UnitsReachTilesSequenceTrigger` on an object "West wall watch" under the level: every 0.25 s, when a living Enemy unit stands on 0,5 / 1,5 / 2,5 (the tiles just north of the barricades on 0,6 to 2,6) and the level's sequence player is free, it plays the pair once (camera on the wall, Lucy, Linda, camera back). It waits rather than cut off a stage sequence, and it switches no input, because it plays on the enemies' turn. No core: the stages run one after another, so a hidden stage objective could not run beside them; a side component was the least invasive. w3's west Claws also pass these tiles, but the trigger fires once, on w1 (first to arrive). The turn flow already waits for a playing sequence (`IsTurnSwitchBlocked`); the AI keeps acting while the pair shows, as with any stage-end sequence on an enemy turn. Play check: the pair appears when the first Claws reach the west wall, not before.

**The defeat line.** Shown with no core change. The loss panel lists the failed objective's text (first sentence), so the defeat objective's text is now `{pickline_0}`, and `PickFallenLOCondition` exposes the standing line ("Keep {pick} standing.") while the pick stands and the fallen line ("{pick} has fallen.") once it has. On the HUD the objective reads "Keep Mark standing."; after the fall it, and the loss panel's row, read "Mark has fallen" (the panel cuts at the first full stop). Unit tests cover the line switch; the on-screen result needs the verifier's play check (lose with the pick).

**Tally and bark lines (M3.3.1 to M3.3.3, M3.4.1 to M3.4.4): not wired.** The text file allows dropping a row whose trigger isn't cheap. Each needs a new bark event (first barricade destroyed, first attack on the held pick, mushroom blast, tally lead change) plus a bark graph; a bark graph can only be made by editing graph text (see the Ridge's low-health bark), and the tally has no lead-change event. That is a feature of its own, not wiring. Needs a decision: a later chunk, or drop for the demo.

**Tests.** Covering fixtures (`MISO.Core.Features.Onboarding` + `MISO.Core.Levels`): 853 total, 853 passed. (A first attempt had 14 M3 tests failing because the recreated dialogues were saved empty; after deleting and re-wiring once more they were filled; cause not found, probably my first delete/apply overlapped a recompile. The final state is checked on disk and by the tests.) Full EditMode suite: 2960 total, 2957 passed, 1 Explicit (`AIRegressionTest.Baseline_MatchesCurrentAI`), 2 failed on the first full run: `BondNodeGateTests.RealTrees_MarksSistersAndTempestBloomAndRivalry_AreLockedFamilyNodes` and `SilentUnlockableLockTests.AllowList_HoldsOnlyEntriesThatAreStillSilent`, both an unhandled NullReferenceException in `Mission.OnEnable` (`Mission.cs:139`, a null level in a mission while the asset loads, a core file I did not touch). Both pass when run alone straight after (2 of 2), so they look order or editor-state dependent; worth a look by the coordinator, not caused by this chunk as far as I can tell. Last recorded 2939/2938; the +21 are this chunk's new tests.
Idempotent: `Apply Wiring` twice, md5 of the level, the Trail asset and every file in `M3Yard/` identical (112 files).
AIRegressionTest not run (no AI content touched). Save not reset.

**Decisions (8.4).**
- Per-pick text: the push line is a `PickLineDialogSequence` with Mark's text as its own lines and John as an entry (general: any nickname, fallback = own lines).
- The pick's lines sit on the Right side (the text file's suggestion); the 8.3 placeholders were Left.
- Level start: the west-lane camera step is dropped (the pair moved out); `CameraBack` now frames from the Claws.
- The new pick lines on notches 1 and 2 play after the stone moves and before the wave arrives, per the text's order.

**Proposed commit: `feat(onboarding): M3 lines`.** It cannot be separated by file from commit 4: the level prefab, the `M3Yard` assets, `MissionWiring.HoldTheYard*.cs`, `M3DefenceTests.cs` and `PickFallenLOCondition.cs` are new or modified-uncommitted in 4 and carry the 8.4 changes in the same files. Fold it into commit 4. The only clean split is a small commit before 4 for the two new runtime classes and their tests: `Features/Onboarding/PickLineDialogSequence.cs`, `UnitsReachTilesSequenceTrigger.cs`, `Editor/PickLineDialogSequenceTests.cs` (each with its `.meta`). Commit 4 then also holds `Editor/M3DefenceTests.Lines.cs` and `Editor/MissionWiring.HoldTheYard.Lines.cs` (+ `.meta`) and the in-place changes above, and the "Proposed commits" entry 5 above is folded into it.

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
4. `feat(onboarding): Hold the yard round two: barricades, lanes, the Masher in the east lane, the pick held on the stone` (7.1 + 8.3 assets and wiring; after 3, since the wiring and the level use `HoldPickOutOfCombat`). Replaces 7.1's proposed commits 1 and 2 (`reports/onboarding-m3-round-two.md`): the level-start hold option is gone, so there is no separate commit for it.
   - the levels: `miso/Assets/_Project/Content/Levels/Greybox/GB_m3-defence.prefab`, `GB_m3-defence.prefab.meta`, `GB_m3-defence_v1.prefab`, `GB_m3-defence_v1.prefab.meta` (git sees a rename plus a new file once both sides are staged)
   - the mission: `miso/Assets/_Project/Content/Levels/M2 - The Trail.asset` (one line: the graph payload)
   - the barricade: `miso/Assets/_Project/Features/NPCs/Rock/Prefabs/Unit_Barricade.prefab`, `Unit_Barricade.prefab.meta`
   - the sequences: `miso/Assets/_Project/Resources/Sequences/M3Yard.meta` and everything in `miso/Assets/_Project/Resources/Sequences/M3Yard/` (47 assets + 47 `.meta`)
   - the wiring: `miso/Assets/_Project/Features/Onboarding/Editor/MissionWiring.HoldTheYard.cs`, `MissionWiring.HoldTheYard.Stone.cs`, `MissionWiring.HoldTheYard.Sequences.cs`, `MissionWiring.HoldTheYard.Mission.cs`, `MissionWiring.HoldTheYard.Barricades.cs` (+ `.meta`), `MissionWiring.HoldTheYard.Pick.cs` (+ `.meta`)
   - the condition: `miso/Assets/_Project/Features/Onboarding/PickFallenLOCondition.cs` (exposes the pick's name for the defeat text)
   - the tests: `miso/Assets/_Project/Features/Onboarding/Editor/M3DefenceTests.cs`, `miso/Assets/_Project/Features/Onboarding/Editor/PickFallenLOConditionTests.cs` (+ `.meta`)
   - Not in it (back at HEAD, nothing to stage): `HoldUnitsUntilSignal.cs`, `HoldUnitsUntilSignalTests.cs`, `OnboardingMissionGraphTests.cs`, `SearchTrailTests.cs`, `PickOnTilesLOConditionTests.cs`, `GB_m1-ridge.prefab`. Deleted untracked 7.1 files (nothing to stage): `HoldUnitsUntilSignalTests.LevelStart.cs`, `MissionWiring.HoldTheYard.Mark.cs`, `Unit_Rock_Stone4.prefab` (+ metas).
   - Not to stage: THJ's `LevelM2-C1.prefab`, `PreloadScreen.unity`, `ProjectSettings/*`, `Content/FamilySuperTime/DUO/Inserts/`, the TMP fallback font, `Resources/Sequences/M3Defence/M3Defence_Notch3_HideLastStone.asset` (+ .meta).
5. `feat(onboarding): M3 lines` (8.4)

## Other branches

none

## How to see it

1. Nothing visible yet: no game code calls the API until 8.2's hold component.
2. Window > General > Test Runner > EditMode, filter `FactionRoleSuppressionTests`, Run Selected: 17 green.
3. 8.2: nothing visible in a level until 8.3 wires `HoldPickOutOfCombat` into M3. Test Runner > EditMode, filter `HoldPickOutOfCombatTests` (17), `LevelAbilityLockRuntimeTests` (5), `CatchHeldCatcherTests` (5), `PapasShelterReenableTests` (4), `RoleBadgeRulesTests`, `AbilityLockTests`: all green.

## Verification (8.1–8.3)

Verifier: miso-verifier, 2026-11-26. Branch `main`. Unity MCP in THJ's open editor. Quiet checks only, no play session. Save reset: no. No file under `miso/` edited.

- **Result:** PASS (play-only criteria Not run: THJ plays M3 himself).
- **Gate 1, compile:** forced refresh plus compile request. The assets were already compiled (`CompileScripts: 1 ms`, one domain reload, no new errors). The last `error CS` lines in `Editor.log` (`MissionWiring.HoldTheYard.Pick.cs` CS1022) sit before the previous reload, from earlier in the session, and the console has no `error CS` entry now. Console warnings and errors: 18 entries, all "Serialization depth limit 10 exceeded" for existing types (`StatBackedValueBase`, `GTag.subTags`, `RuntimeAbility._owner` cycles), none from the changed files. `warning CS` lines in the log naming the role and controller files (`MarkFactionRoleHandler.cs(66)` CS8509, `JohnFactionRoleHandler._isActive` CS0414, `PlayerController.showFamilyRoleDialogVisual` CS0414) are unused-field and non-exhaustive-switch warnings on lines this feature did not add. No warning from `Features/Onboarding`, `Levels/AbilityLock`, `Player/Lucy` or `UI/Panels`.
- **Gate 2, full EditMode suite:** 2925 total, 2924 passed, 0 failed, 1 skipped (`AIRegressionTest.Baseline_MatchesCurrentAI`, Explicit). 192 s. Same as the implementer's last run.
- **AIRegressionTest.Baseline_MatchesCurrentAI (by name):** fails as expected. `CHECKS: 738  FAILURES: 51` against 52 (7.1): the `Unit_Rock_Stone4.prefab` `units.unexpected` line is gone, `Unit_Barricade.prefab` stays, and the checks count drops by one. The rest is the existing set: graph count, node, edge and fingerprint lines, the `abilities.unexpected` and `abilities.count` lines, `units.count` (21 expected, 29 found), `units.missing Unit_Placeholder.prefab`, the other `units.unexpected` lines (the stone variants 0..3, `Unit_Rock`, `Unit_DarkClaw_StartsAlert`, `Unit_DarkClaw_Hearth`, `StuntCamActorSet`), the `units.ability` lines, and the final `fatal` NullReferenceException in `AIStrategyPlanner.HandleLivingUnitsCondition`. No new line type. Family Roles and Super Time: the only role line is `units.ability Unit_Lucy/Lucy_Ability_FactionRole: ability missing from prefab`. I could not diff it against 7.1's full list (7.1 recorded only the count and "no new line type"); it is a prefab-ability mismatch of a kind the existing set already has (units.ability lines), and nothing in 8.1 touches prefabs, but I did not prove it was already there. No `FactionRoleHandlerBase`, `PlayerController` or Super Time line. Not fixed, not re-baselined.
- **Editor state:** open scene `PreloadScreen` (`Assets/_Project/Scenes/PreloadScreen.unity`), not dirty, Play mode off. Nothing saved.
- **Not run (needs a play session):** the play checks listed under "How to see it (8.3)" and the 8.2 loose items (pick lookup, Super Time deferral, Masher reveal footprint, grey badge, Duo from another bar).
- **Editor checks corrections:** none. Confirmed: `refresh_unity` with compile returns at once; a run through `get_test_job` with `include_failed_tests` saves the large result to a file (the failure text is in `results[0].message`), and the first poll after starting the AI test hit a one-off "plugin session disconnected" and worked on retry.

## Review (8.2 + 8.3 feature pass, miso-reviewer; pasted by the coordinator)

**Verdict: APPROVE.** Must fix: none.

Should fix:
1. `HoldPickOutOfCombat.FindPick` fallback: add the "no fixed seats → null" guard that `PickFallenLOCondition.FindPick` has (standalone toolbar play could hold a sister if 4,11 is empty; unreachable in M3).
2. Behavior tests: `TryCatch`/`WouldCatch` return false while held (today only `IsCatcherHeld` is tested); Papa's Shelter comes back on re-enable when Lucy is next to John (only the stale-on → off direction is tested). Add if the rig allows, else leave to the play check.

Notes: the hold releases on disable/destroy/level end with a stable owner, tracks only what it added, idempotent, release gives a full turn (order checked in `SwitchTurnIE`); forced teardown may change suppression during Super Time (acceptable); John-pick teardown may briefly re-enable the shelter (harmless). `LevelAbilityLock` unchanged for existing callers; `Lock` raises `Changed` (bar rebuild; `GuidedAbilityHint` unaffected). Catch paths all covered. Badge stale until the next panel refresh. M3 wiring checked: S2 end = input off → hold signal → Masher camera/reveal; notch 3 = notch → roll-away → release → line; S1 lists only the opening Claws; defeat Any with `PickFallenLOCondition` alone; free seat 1; 47 M3Yard assets referenced; no Stone4/holdFromLevelStart left. Stale overrides in the level YAML harmless (optional cleanup). No core beyond 8.1, no private IDs, LF/no BOM, no mutable statics. Commits 2→3→4 build in order, no 8.1 file in them.

Left to play: Super Time deferral, the Masher 2×2 slide, John's tether hidden?, the Masher close-up vs the S2 camera, the pick greying at once when held in its own turn.

## Play-check fix 1

Changed: `Features/Onboarding/HoldPickOutOfCombat.cs`, `Features/Onboarding/Editor/HoldPickOutOfCombatTests.cs`. No core files.

**Cause 1 (the crash).** `DuoPresetsOf` read `ability.EffectSetLevel` for every ability of every family unit. A locked or run-unlockable ability has upgrade level -1, so `GetEffectSetLevel` indexed `higherLevels[-2]` and threw. It threw before `Hold(pick, presets)` ran, so nothing was held.

**Fix 1.**
- New `CoOpTriggersOf(preset)` scans the preset's base level and every higher level for `AEffectCoOpTrigger`, so a Duo is found even when the partner's trigger ability is locked. `DuoPresetsOf` uses it and no longer touches `EffectSetLevel`.
- `Hold()` (the signal entry) now wraps the Duo collection in try/catch. On failure it logs a warning and still holds the pick, locking no Duos.

**Cause 2 ("Mark can still move and act after the stone").** This is mostly the same crash. Reading the code also showed a second gap for a hold applied mid-turn:
- The inactive tag only takes effect where the controller reads it. `PhaseData.ToPlayUnits` (the predicate is live), `IsSelectableUnitCell` and `UnitSelectionState.ApplyCondition` do read it, so the pick can't be auto-selected, switched to or clicked.
- A pick that is the current `ActiveUnit` (ActionSelection state) is not re-checked. `TakeActionState.GetNextState` returns ActionSelection again whenever `ActiveUnitActionPoints > 0`, so a still-selected pick with AP left keeps moving and acting.
- `PlayerController` has no public deselect. `GoBackToPreviousState` is protected, and `TrySelectUnit(other)` is deferred while an action is in progress, so it can't be relied on.

**Fix 2.** When the hold starts during the pick's own faction turn, `StartTurnHold` now:
- calls `Hold()` first, then `NotifyTurnStarted(true)`;
- consumes the pick's AP with `APConsumptionType.Closure`.

With 0 AP its abilities and walk are inactive (`Active` needs `CanConsume`), and the turn flow moves on to the next unit or ends the turn. Because `HeldAtOwnTurnStart` is now true, a release during the same turn restores the pick's AP (`ResetToInitial`). That is what the class doc already promised. Before this change the restore never fired, because the turn start was noted before the hold began. Nothing in core was needed.

**Limits.**
- AP mode is PerUnit in `GlobalSettings.asset`. In Shared mode `Closure` does nothing to the pool, so a still-selected pick could keep acting. This was deliberate: draining the shared pool would take the other units' AP.
- The selection highlight stays on the pick until the next selection change (cosmetic).
- The mid-turn drain needs `CombatLevelRunHandler`, so it has no EditMode test. It needs the verifier's play check: hold Mark at the end of S2 while he is selected with AP left, then confirm he can't move or act, the turn goes on, and a release in the same turn gives him his AP back.

**Tests (EditMode, all pass).**
- `DuoPresetsOf_AnAbilityAtUpgradeLevelMinusOne_DoesNotThrow`: a partner with abilities at level -1 and level 5 on a controller with a cooperation handler. It threw before the fix.
- `CoOpTriggersOf_FindsTriggersInTheBaseLevelAndEveryUpgrade`.
- The rig can't build a full cooperation entry with a valid partner, so "Duo found while locked" is covered by the trigger scan test only.
- `HoldPickOutOfCombatTests`: 19/19 pass. Full EditMode suite: 2931 total, 2930 passed, 0 failed, 1 Explicit (`AIRegressionTest` baseline). The Onboarding fixtures ran as part of it.

## Review (8.5 core, miso-reviewer; pasted by the coordinator)

**Verdict: APPROVE** (from reading; conditional on the tests passing once the bridge is back). Must fix: none.

Should fix:
1. `MultiCellWalkRangeTests.AIWalkCandidates` (~217-224): the Masher's radius 1 comes from the light setup by accident; add `Assert.GreaterOrEqual(ability.Parameters.radius, 1, ...)` so a radius-0 setup fails clearly.
2. Same file: save as LF with BOM like the folder (`.gitattributes` resolves `eol=lf`).

Notes: 1×1 path is the old statement word for word; worker-safe, no statics, `GridCell.cs` BOM+LF kept, 13/1 hunk. Destination legal end to end (BFS/straight, `FindPath`, `MoveEntity`, `JumpEntity`, `CanEndOn`, `IsLegalAbilityTarget`, selection pre-filters). Correction: the Masher walk and Queen walk/jump are **PathWalkable**, not SelfWalkable. The surrounding-effect concern doesn't happen (filtered downstream; only the debug list sees it). Other changes acceptable: a player big unit could pick its own cells (no-op; none exist); Mark's Command on the Queen now offers her north anchor (intended); latent `allowRangedReach` + big-unit walk range keeps diagonal footprint cells (no such ability). The AI prediction gap predates the fix (backlog). AI regression will move; compare with 51.
