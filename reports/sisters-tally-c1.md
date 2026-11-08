# Report: Sisters' tally, C1 (counting core)

Plan: plans/onboarding/2026-11-08-sisters-tally-tech.md    Agent: miso-implementer (opus)    Branch: thj/onboarding
Outcome: done (C1 only; C2–C4 not started)

## What changed

All new files under `miso/Assets/_Project/Features/Onboarding/SistersTally/` (namespace `MISO.Core.Features.Onboarding`, LF, no BOM):

- `SistersTally.cs`: static façade. `Enabled` (off switch, literal `true`), `SistersTallyState` struct, `Current`, `Changed`, `Gate`, `IsEligible`, `IsFaded`, `BeginLevel`, `RefreshFaded`, `ReleaseFadedCheck`, `RecordKill`, `BankAttempt`, `DropAttempt`, `ResetPlayModeState`.
- `SistersTallyRun.cs`: banked (won levels) and attempt counts per sister, keyed by mission entry (copy of `BondMissionRun`).
- `SistersTallyListener.cs`: plain class that turns the level's bus events into the tally (copy of `BondLevelListener`). Listens to `onUnitDamageDone` and `levelEnded`; every handler guarded (skips `AIWorker.IsWorkerThread`, catches and logs exceptions).
- `SistersTallySource.cs`: MonoBehaviour next to `BondSources` on the bus object; mission key `(ActiveMission, GraphSeed)`; serialized `excludedMissions`, `fadeStep`, `returnStep`.
- `Editor/SistersTallyTests.cs`: 29 EditMode tests.
- `.meta` files for the folder, the `Editor` folder and each script (new GUIDs written by hand; Unity accepted them, `SistersTallySource` GUID `4c38bdd340b1415091afdee1778235ff`).
- `miso/Assets/_Project/Content/Levels/LevelBase.prefab`: one component added to the `GlobalEventBus` object (minimal YAML add, LF kept, 17 lines): `SistersTallySource` with `excludedMissions = [M0 - The Hearth]`, both steps empty.
- `miso/Assets/_Project/Core/Managers/PlayModeStaticReset.cs` (core): one line, `MISO.Core.Features.Onboarding.SistersTally.ResetPlayModeState();` after the `BondStore` line.

## Acceptance criteria (C1 parts)

- [x] Switch (counting part): `Enabled` is one property returning a literal. Off: the listener never connects (nothing counts) and `Current` reads `default` (not eligible, 0–0) through `Gate`. Tests: `SwitchOff_ReadsNotEligible_WithNothingCounted`, `SwitchOff_TheLevelDoesNotConnect_AndNothingCounts`, `SwitchOn_ReadsTheStateAsItIs`. The literal itself can't be flipped in a test, so the tests feed `false` through the listener's `enabled` parameter and `Gate`. HUD/results/steps parts are C2–C4.
- [x] Kill rule: counts 1 for Lucy or Linda when `onUnitDamageDone` has `lethal == true`, attacker = `ability.Owner` is a player-faction unit with that Nickname, the target is not a player unit, and the target's health is at its minimum. Tests: `Kill_ASistersLethalHitOnAnEnemyCountsForHer`, `Kill_AHitThatDoesNotKillCountsNothing`, `Kill_AnotherPlayerUnitsKillCountsForNoOne`, `Kill_AnEnemyNamedLikeASisterCountsNothing`, `Kill_OfAPlayerUnitCountsNothing`, `Kill_ALethalReportWithHealthAboveTheMinimumCountsNothing`, `Kill_DamageWithNoAbilityThroughTheBusCountsForNoOne`. Code findings on the excluded cases are below.
- [x] One tally per mission: key `(ActiveMission, GraphSeed)` as in `BondSources`. A won level banks; a lost level and Restart Level drop that attempt; a new entry starts at 0; not saved. Tests: `Mission_AWonLevelBanksItsKills_AndTheNextLevelKeepsThem`, `Mission_ALostLevelDropsOnlyThatAttempt`, `Mission_RestartLevelDropsTheAttempt`, `Mission_TheLastLevelsWinStaysOnScreen_AndARestartFromTheEndCountsOnlyTheReplay`, `Mission_ANewEntryStartsFromNothing`, `ResetPlayModeState_ForgetsEverything`.
- [x] Revert: checked, and reversion **cannot** undo a kill, so no code was written (per the criterion). Evidence: `PlayerController.CheckForActionReversion` calls `ability.Revert()`, which runs `ReversionContext.Execute()`. The only things that add revert actions are `AEffectTransporter` and `AEffectCommand` (they move units back) and `AGUnitSpawner` (it removes spawned units). Nothing restores HP or calls `Resurrect`/`Revive`, and `AEffectAttributeModifier` adds no revert action. So a reverted lethal hit leaves the target dead, and the kill stays counted (it really happened).
- [x] Eligibility: both Lucy and Linda in `ActiveMission.MissionRoster.Units` (fixed and free slots) and the mission not in `excludedMissions`. Read once per level, at `OnEnable`. Tests: `Eligible_WithBothSistersInTheSquad`, `NotEligible_WithOneSisterOrNone`, `NotEligible_InAnExcludedMission`, `NotEligible_NothingCounts`, plus `Asset_EveryLevelHasTheSource_NextToTheBus_LeavingOutTheHearth` (loads the real prefab; checks the component sits next to the bus and the list holds exactly The Hearth). The River and The Ridge have no sister pair (already checked by Bond's asset test `Asset_ANormalRunStaysUnderLevelTwoUntilTheYard...`).
- [x] Faded logic: `IsFaded(hasPlayed, fade, return)` = fade played and return not played; an empty fade step means never faded. Read at level start and again on `RefreshFaded()`. Tests: `Faded_OnlyAfterTheFadeStep_UntilTheReturnStep`, `Faded_NeverWithNoFadeStep_AndForGoodWithNoReturnStep`, `Faded_IsReadAtLevelStart_AndAgainOnRefresh`, `Faded_StillCounts_SoTheReturnShowsTheWholeMission`, `Faded_ALevelGoingAwayDoesNotReleaseTheNextLevelsCheck` (with a fake played set; the real `PlayedSequencesTracker` is never touched).
- [x] Guarding: `AThrowingChangedListener_DoesNotReachTheLevelsEnd`, `Disconnect_StopsListening`.
- [x] EditMode suite: run through the Unity MCP after a recompile: **1646 tests, 1645 passed, 1 failed = `AIRegressionTest.Baseline_MatchesCurrentAI` (the known red)**. No compile errors and no new warnings from the new files.

## Code findings on the excluded kill cases

- **Dom's fake death (`BossDomFight`, `LevelDomFight.prefab`) WOULD be reported lethal.** Its `OnDamaged` is wired to the health attribute's `onValueChanged`, so `FakeDie()` sets `IsAlive = false` during the hit. `CombatLevelRunHandler` then computes `lethal = !target.IsAlive || health <= min`, which is true. HP is still above the minimum (the trigger is a % threshold). Hence the extra health-at-minimum check in the source.
- **Spawner-bound units**: `OnBoundSpawnerDied` → `Die(0)`. If the same area hit also damaged the bound unit, it is reported lethal via `!IsAlive`, with HP above minimum. The same check excludes it.
- **Dark Worm split parents**: not reported lethal. `DarkWormPassiveAbility.HandleDamaged` sets HP to min+1 synchronously (before its first yield) while the health event is still firing. The parent is later removed with `DiePermanently`, with no damage event. With `lethalDamagePreventsSplit` on, the worm really dies and counts as a kill, which is correct.
- **Hazards with no owner**: `onUnitDamageDone` with a null ability is ignored (tested through the real bus).
- **Ally kills**: the raiser only sends Enemy-relation hits; the listener also refuses player-unit targets.

## Public API for C2–C4

```csharp
namespace MISO.Core.Features.Onboarding
public static class SistersTally {
    public static bool Enabled { get; }                    // the off switch
    public static SistersTallyState Current { get; }       // default while off
    public static event Action Changed;                    // main thread; re-read Current
    public static void RefreshFaded();                     // C4: call after PlayedSequencesTracker.MarkPlayed(step)
    public static bool IsFaded(Func<Sequence,bool> hasPlayed, Sequence fade, Sequence ret);
    public const string LindaNickname = "Linda", LucyNickname = "Lucy";
}
public readonly struct SistersTallyState { bool Eligible; bool Faded; int Linda; int Lucy; bool Visible /* Eligible && !Faded */; }
```

- C2 (HUD): subscribe to `Changed` in OnEnable, unsubscribe in OnDisable, show `Current.Visible`, labels from `Current.Linda`/`Lucy`. `Changed` fires at each level start, on each counted kill, on bank/drop and on `RefreshFaded`.
- C3 (results row): read `Current` on enable. It still holds the finished mission's numbers when the mission-end panel opens (state is kept after the level's source disables; see Decisions).
- C4 (steps): assign the two `Sequence` assets to `fadeStep` / `returnStep` on `LevelBase.prefab`'s `SistersTallySource` (serialized names `fadeStep`, `returnStep`). In each step: if `!SistersTally.Enabled`, finish at once. Otherwise `PlayedSequencesTracker.MarkPlayed(this)`, then `SistersTally.RefreshFaded()`. Note `PlayedSequencesTracker` keys by asset name, so the asset names must stay stable.

## Save reset

No.

## Decisions I made

- Added a fourth class, `SistersTallyListener` (plain C#, like `BondLevelListener`), so the rules are testable without a level. Same behaviour as the plan's three-class layout.
- Namespace is `MISO.Core.Features.Onboarding` (the existing Onboarding namespace), not `...Onboarding.SistersTally`: a namespace with the same name as the static class would force full qualification everywhere.
- Kill = lethal **and** target HP at its minimum. The plan said "count on `lethal == true`". Its own criterion excludes fake deaths and spawner-bound deaths, and the code shows those can arrive with `lethal == true` (findings above). This tightens the rule to match the criterion; real kills always have HP at minimum, because death comes from `onMinReached`.
- Did not listen to `onRewardsGranted` ("Mission complete"/"Mission failed"), which the plan's approach lists. Bond needs it to pay; the tally doesn't. "Mission failed" → drop-all would also wipe earlier won levels if the player restarts from that panel, against the "drop only that attempt" criterion. A new entry already resets through the reseeded key. Same criterion behaviour, simpler.
- `levelEnded(MissionComplete)` (the last level's win) does **not** bank. It leaves the kills as the current attempt, which `Current` already includes. Banking there would double-count after a Restart Level from the mission-end panel (same key). `Win` banks and `Defeat` drops.
- Counting happens only while eligible, and it continues while faded, so a return mid-mission would show the whole mission.
- The static state is not cleared when the level's source disables (only its faded check is released, and only if it is still the current one), so C3's mission-end panel can read the numbers after the level ends. The next level start overwrites everything.
- `ResetPlayModeState` also clears `Changed` subscribers.

## Needs THJ

None.

## Docs to update

- `tech/core-systems.md` (coordinator): optional note that `PlayModeStaticReset` resets `SistersTally`.
- First-hour design tally row (designer, "as built"): a kill is the sister's lethal hit with the target at 0 HP; summons credit themselves; the last level's kills stay as the current attempt until the mission ends.
- `status.md` / `build-log.md` (coordinator).

## Risks and loose ends

- **Not play-checked.** The live wiring (the source's `OnEnable` reading `MissionTracker`, and `onUnitDamageDone` arriving in a real fight) is covered only by the code read and the prefab asset test. A quick check: start The Trail, kill an enemy with Linda, then in the console or a debugger read `SistersTally.Current`. The visible check comes with C2.
- Eligibility is read once per level start. A squad change mid-mission can't happen today; if it ever can, the HUD would lag by one level.
- If a level's `OnEnable` ever ran before `MissionTracker.ActiveMission` is set, the key would be `(null, seed)` and the level not eligible. `BondSources` makes the same assumption.
- `MissionStatsTracker` was neither changed nor used.
- Script `.meta` files use the full Unity MonoImporter layout, where the older ones in this folder are the short two-line form. Unity accepted them as written (GUIDs kept).

## Proposed commits

1. `feat(onboarding): sisters' tally counts Lucy's and Linda's kills per mission`: plain, except that it carries the one core line, which only works with these files:
   - `miso/Assets/_Project/Features/Onboarding/SistersTally.meta`
   - `miso/Assets/_Project/Features/Onboarding/SistersTally/SistersTally.cs` (+ `.meta`)
   - `miso/Assets/_Project/Features/Onboarding/SistersTally/SistersTallyRun.cs` (+ `.meta`)
   - `miso/Assets/_Project/Features/Onboarding/SistersTally/SistersTallyListener.cs` (+ `.meta`)
   - `miso/Assets/_Project/Features/Onboarding/SistersTally/SistersTallySource.cs` (+ `.meta`)
   - `miso/Assets/_Project/Features/Onboarding/SistersTally/Editor.meta`
   - `miso/Assets/_Project/Features/Onboarding/SistersTally/Editor/SistersTallyTests.cs` (+ `.meta`)
   - `miso/Assets/_Project/Content/Levels/LevelBase.prefab`
   - `miso/Assets/_Project/Core/Managers/PlayModeStaticReset.cs`

   The `PlayModeStaticReset` line can't go first in a commit of its own: it doesn't compile without `SistersTally`. If THJ wants the core line separable, the order is (a) the feature files, (b) the reset line, (c) the prefab. For one added line, a single commit seems right.

Do not stage THJ's uncommitted `AIFactionBrain.cs`, `AIUnitBrain.cs`, `PreloadScreen.unity` or `ProjectSettings/*`.

## Other branches

None (onboarding-only feature).

## How to see it

1. In Unity, Window > General > Test Runner > EditMode, filter "SistersTally": 29 tests green.
2. Open `Content/Levels/LevelBase.prefab` and select `GlobalEventBus`. Below Bond Sources there is a Sisters Tally Source with Excluded Missions = M0 - The Hearth and both steps empty.
3. Nothing shows in play yet (the HUD counter is C2). To peek, play The Trail with both sisters and watch `SistersTally.Current` in a debugger after a sister's kill.
