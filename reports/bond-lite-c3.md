# Report: Bond Lite C3 (mission-end and help sources, Home activity API, level-up queue)

Plan: plans/onboarding/2026-10-26-bond-lite-tech.md    Agent: miso-implementer    Branch: thj/bond-lite
Outcome: done, review fixes applied (see "Review fixes"). One sub-source narrowed as instructed (only John's Family Role names who it helped), and one prefab touched that the plan didn't list (`LevelBase.prefab`). The in-game path needs the verifier's play check, and **one hole stays open: Esc > Quit on the mission-end panel can pay twice** (see Risks).

Paths are under `miso/Assets/_Project/`.

## What changed

- `Core/Systems/HomeSystem/Runtime/BondLite/BondMissionRun.cs` (+ `.meta`): new. The unsaved per-mission help tally: won levels and current attempt kept apart, cap applied on read, `PairsAmong`, and the `Paid` flag for this entry.
- `Core/Systems/HomeSystem/Runtime/BondLite/BondLevelListener.cs` (+ `.meta`): new. Plain class: bus events to tally, and one `Add` per squad pair on `"Mission complete"`, first completion only. Handlers guarded against the worker thread and against exceptions, and each pair's `Add` guarded on its own.
- `Core/Systems/HomeSystem/Runtime/BondLite/BondSources.cs` (+ `.meta`): new. Thin component next to the bus; connects in `OnEnable`, disconnects in `OnDisable`. No statics.
- `Core/Systems/HomeSystem/Runtime/BondLite/BondStore.cs`: `Settings`, `MissionRun`, `PendingLevelUps`, `AddHomeActivity`, `TakeNextLevelUpScene`; `Add` queues reached levels and saves them before raising `BondLevelReached`; `BondLevelUp`; `BondSaveData.pendingLevelUps`.
- `Core/Systems/HomeSystem/Runtime/BondLite/BondSettingsSO.cs`: `missionEndPoints`, `helpBonusPoints`, `helpBonusCapPerMission`, `homeActivityPoints`, `missionsWithNoBond`, `helpSynergies`, `levelUpScenes`, `GivesBond`, `FindLevelUpScene`.
- `Resources/BondSettings.asset`: the values below, The Hearth on the no-Bond list, the Rivalry help entry. 11 added lines, nothing else changed.
- `Content/Levels/LevelBase.prefab`: `BondSources` added on the `GlobalEventBus` object. 13 added lines, no other change. All 64 mission levels inherit it.
- `Core/Systems/HomeSystem/Editor/BondSourcesTests.cs` (+ `.meta`), `BondLevelUpQueueTests.cs` (+ `.meta`), `BondSourcesWiringTests.cs` (+ `.meta`): new, 41 tests (30, 9 and 2).

No core system file changed. `CombatLevelRunHandler`, `GlobalEventBus` and `GameHandler` are read only.

## Acceptance criteria

- [x] Values come from the settings asset: `Asset_*` tests read the real asset; the listener and `AddHomeActivity` read only settings.
- [x] No gain for a pair not in the squad: `MissionComplete_APairNotInTheSquadGainsNothing`, `Help_ForAPairNotInTheSquadIsNotPaid`.
- [x] Cap respected, across every level of a mission: `Help_IsHeldToTheCapPerMission`, `Restart_TheCapCoversEveryLevelOfTheMission`.
- [x] No `Add` and no save during combat: `Help_NeverSavesOrReachesTheStoreDuringCombat`. One `Add` per pair at the end: `MissionComplete_AddsOncePerPair_HelpAndEndTogether`.
- [x] Failed mission gives nothing and drops the tally: `MissionFailed_DropsTheWholeTally_AndGivesNothing`.
- [x] Restart is fair: `Restart_ALostAttemptsHelpIsForgotten_AndTheWonLevelsStay`, `Restart_FromThePauseMenuForgetsTheAttemptToo`, `ANewEntryIntoAMission_StartsFromNothing`.
- [x] The Hearth adds nothing, by data: `MissionComplete_AMissionOnTheNoBondListGivesNothing_AndForgetsItsHelp`, `Asset_TheHearthIsTheOnlyMissionWithNoBond`.
- [x] Free slot read at that moment: `MissionComplete_ReadsTheFreeSlotsChoiceAtThatMoment`, `MissionComplete_AnEmptyFreeSlotIsSkipped`.
- [x] AI faction events don't count: `Help_DuoFromAnotherFactionDoesNotCount`, `Role_OfAnEnemyDoesNotCount`. **The worker-thread guard itself has no test:** `AIWorker` is internal to the game assembly, and the tests are in the editor one.
- [x] Level-up queue: `BondLevelUpQueueTests` (order, save round trip, old save, scenes taken once, levels with no scene dropped).
- [x] Every level has the listener: `EveryMissionLevel_HasBondSourcesNextToItsBus`, `LevelBase_CarriesBondSourcesOnItsBus` (64 levels at last count; fails on an empty list or a level with no bus).
- [x] A mission's end pays once per entry: `RestartAfterTheMissionsEnd_DoesNotPayAgain_AndANewEntryDoes`.
- [x] A replay of a completed mission pays nothing (THJ's decision): `AReplayOfACompletedMission_PaysNothing_AndForgetsItsHelp`.
- [x] One failing subscriber costs only its own pair: `AThrowingLevelUpListener_DoesNotReachTheLevelsEnd`, now with a three-hero squad.
- [x] EditMode suite after the last edit: 1558 of 1559 passed. The only failure is the known red `AIRegressionTest.Baseline_MatchesCurrentAI`, not touched. The plugin session dropped once during the wait; calling again returned the result. No `__*` folder under Greybox. No console errors after compile.
- [ ] **Not verified: a real mission in Play.** I did not start Play. Steps are under "Verifier steps".

## Tuning arithmetic

Values: mission end 5, help 1 per event, cap 3 per pair per mission, Home activity 5.

| Linda-Lucy | Least | Most (full cap) |
| --- | --- | --- |
| Start | 15 | 15 |
| The Hearth (no-Bond list) | +0 | +0 |
| The River (John, Lucy) | +0 | +0 |
| The Ridge (Linda, Mark) | +0 | +0 |
| M2 The Trail (Linda, Lucy + free slot) | +5 = 20 | +5 + 3 = 23 |
| Yard (+5) | 25 = Lv 2 | 28 = Lv 2 |

So low 20s after M2, under 25 even at the cap, and the Yard crosses 25 with no help at all. `Asset_ANormalRunStaysUnderLevelTwoUntilTheYard_WhichAlwaysCrossesIt` checks this, including the real rosters and that River and Ridge have no free slot. It's 17 points short of Lv 3 at most, so one Yard can't double-cross. No test or number assumed a replay paid, so first-completion-only changes none of this; it only removes the way to exceed these numbers by replaying.

## What the events carry

All of it read in code; the in-game firing is not yet seen in Play.

- **Thread:** `AISystem/Runtime` calls none of `Execute`, `Activate` or `ActivateAbility`, so nothing the AI plans with raises these events. Duo: `AEffectCoOpTrigger` then `Execute`. Rivalry: `onUnitDamageDone`, from `CombatLevelRunHandler.OnAbilityPerformedOn`. Role: `PlayerController`'s role flow after the press. I still return early on `AIWorker.IsWorkerThread`, because `EnemyAlertTracker` shows some bus events can reach that thread.
- **Duo:** `unit` is the activator and `targets` are the partners, activator included. The pair comes from those, not from parsing the id.
- **Rivalry:** `unit` is the sister who receives the AP; the killer is only in the detail text. So the pair comes from the `helpSynergies` entry instead of parsing that text.
- **Family Role:** the event carries the handler, and `handler.Targets` decides it.
  - John: `Targets` are the covered allies, so **it counts**.
  - Linda, Lucy, Mark: `Targets` are the enemy they strike. Mark works out `hitAlly` in `PrepareTargets` but doesn't keep it. **Dropped for these three**, per your instruction, rather than guessing from `SessionLogs`.
  - The rule is generic: a friendly unit among the targets counts. So **Family Roles never add help between Linda and Lucy today**; only John's pairs earn from this source.
- **Roster:** `_assignedFreeUnits` has two writers, `CharacterSelectPanelUI.OnContinueClicked` and `LevelFastForwardRoster`, both before the level. It is still set at `"Mission complete"`.

## Tally lifetime

- Lives on the store instance as `BondStore.MissionRun`: not saved, no new static, and it goes with the existing `ResetPlayModeState`. `RestoreState` doesn't touch it, so `Instance`'s re-register can't wipe it.
- The mission entry is `(ActiveMission, GraphSeed)`, as in `CombatLog`. `SetMission` rerolls the seed, and a level restart keeps it.
- Level start: a different entry clears everything; the same entry clears only the attempt. That covers defeat retries and pause-menu restarts.
- `levelEnded(Win)` banks the attempt; `levelEnded(Defeat)` drops it; `"Mission failed"` drops all. Leaving through the menu is cleared by the next entry's new seed.
- `Paid` is set when the end pays, and only a different entry clears it. Restart Level from the end panel builds a new level with the same key, and its end fires the event again; without the flag that paid twice.
- `mission.Completed` is read at the event. `RecordCompletion` runs later, in `GameHandler.EndMission`, so false means first completion and true means replay.
- Order at the end of a mission: `"Mission complete"` is raised before `levelEnded`, so the last level's attempt is counted directly, without banking.

## Level-up queue (built, nothing plays it)

- `Add` queues every level reached as plain `{a, b, level}` in the save (`pendingLevelUps`), so it survives a restart. Saved before `BondLevelReached` is raised.
- `levelUpScenes` on the settings maps pair and level to a `Sequence`. It is **empty**: no scene exists yet.
- `TakeNextLevelUpScene()` returns the oldest waiting scene, drops levels with none, and saves. **Nothing calls it**, since C5 is the only user. `HomeManager` is untouched.
- Nothing subscribes to `BondLevelReached` in this chunk, and no scene object holds a store reference.

## Save reset

No. `SaveData.json` keeps its 17:24 timestamp from before my work. Tests use local stores.

## Decisions I made

- **Component on `LevelBase.prefab`, on the bus object.** It follows the per-level pattern, needs no core edit and no bootstrap, and `GetComponent` gets the level's own bus without waiting. The plan didn't list this prefab; the guard test catches a level without it. Small YAML edit, kept in its own commit.
- Listener split from the component, so tests can drive a real local bus with fake events (`OnEnable` doesn't run in EditMode).
- Every handler catches and logs exceptions. `"Mission complete"` is raised inside `EndLevel`'s coroutine, and I didn't want a Bond bug or a future `BondLevelReached` subscriber to risk the end panel.
- Help for a pair outside the roster is not paid, even if both fought together, as you decided. Consequence: Toba placed by the level in M4 earns nothing with Linda from `Linda_Toba_Duo`, since he's not in the roster.
- Cap is per pair per mission, not per level.
- `AddHomeActivity(x, y)` is the Home API; C5's once-only guard (`PlayJustOnce`) stays with the sequence.
- `missionsWithNoBond` holds `Mission` references, so `BondSettings` in Resources now references The Hearth. `GameData` already holds it, so no new load.
- Added `pendingLevelUps` to `BondSaveData`, additive. Old saves load with an empty queue (`TheQueue_SurvivesASaveRoundTrip_AndAnOldSaveHasNone`). Covered by this plan's yes for the new key, which hasn't shipped.

## Needs THJ

None to answer from this chunk. THJ decided the replay question: mission-end Bond pays on first completion only. A replay pays nothing, help included.

Two consequences THJ may want to hear (both under Risks): the Esc > Quit hole, and saves that already have The Trail completed.

## Docs to update

- `tech/home-system.md`: Bond sources, `BondMissionRun`, `LevelBase.prefab` wiring, the queue and its save field.
- `design/gdd/family-systems.md` or `progression-economy.md`: the values above; Family Roles count as help only for John; mission-end Bond pays on first completion only.
- `tech/core-systems.md`: no change.

## Risks and loose ends

- **C4:** `"Sisters' Rivalry"` in the settings must match the literal at `UnitKillAbilityPointProvider.cs:50`. Nothing ties the two together, so if C4 rewrites that call, keep the id. A renamed id would silently stop the help. Rivalry being locked after C4 also means the Trail's help can come only from the Duo; the cap and arithmetic hold either way.
- **Open hole: Esc > Quit on the mission-end panel pays twice.** Bond is saved at `"Mission complete"`, before the panel. The pause menu's Quit calls `GameHandler.EndMission(false)`, so the mission is not recorded as complete. The next entry has a new key and `Completed` is still false, so it pays again. Exit Game, or closing the window, does the same. This comes from reading `PauseMenu.cs`; not played. Closing it needs a saved per-mission "paid" record, which is beyond this brief, so I left it. It's +5 to +8 per round trip, and each round trip also leaves the mission unrecorded.
- **Saves with The Trail already completed:** they count as replays, so Linda-Lucy stays at 15 and the Yard's +5 gives 20, not Lv 2. **Test C4 and C5 on a save that hasn't completed The Trail**, or the nodes will look broken. Anyone with such a save (THJ's, possibly) stays locked until a save reset or further activity. Not fixed: no migration was asked for.
- **`BondLevelReached` is a plain multicast:** the per-pair catch protects the other pairs, but one throwing subscriber still stops later subscribers and any higher level crossed in that same `Add`. Points and queue are saved first, so nothing is lost.
- **C5:** the Yard grants its point and shows its scene regardless of what `AddHomeActivity` returns (from the review). Lv 2 can already be reached or can stay out of reach, as above, so the return value must not gate the story.
- **C5:** the Yard's `AddHomeActivity` will queue Lv 2 for Linda-Lucy too. With no `levelUpScenes` entry, the next `TakeNextLevelUpScene` just drops it. If an entry is added for that level, it plays on the *next* visit, on top of the Yard. C5 must call `TakeNextLevelUpScene` from Home; that call is what makes this work at all.
- **Saves at the end of a mission:** each pair's `Add` saves at `"Mission complete"`, so a three-hero squad writes the save three times there.
- **Editor only:** `_assignedFreeUnits` is `NonSerialized` on an asset, so with domain reload off a free-slot pick can survive between Play sessions. A mission entered without the panel would read that stale pick.
- **`source` in `Add` is still unused** (noted in C1). The help tally moved out of the store, so nothing needs it now; kept as the merge-friendly signature.
- **`helpSynergies` and Duo text:** other pair synergies (`"Mark-Linda Race"`, `"Pass-By"`) add nothing, per the plan's list. One more is one line of data if it has a fixed pair.
- **Merge with `thj/home-test`:** the new `LevelBase.prefab` component and `pendingLevelUps` need carrying over; that branch uses `BondSceneDefinition` for level-up scenes.
- Not mine and left alone: `AIFactionBrain.cs`, `AIUnitBrain.cs`, the TMP font, `PreloadScreen.unity`, `ProjectSettings/*`.

## Proposed commits

Nothing staged. Order matters: 2 needs 1 (the script's GUID), and tests need both.

1. `feat(home): Bond from a mission's first completion and capped help, Home activity points and a level-up queue` (save data, additive field; plain otherwise):
   - `miso/Assets/_Project/Core/Systems/HomeSystem/Runtime/BondLite/BondStore.cs`
   - `miso/Assets/_Project/Core/Systems/HomeSystem/Runtime/BondLite/BondSettingsSO.cs`
   - `miso/Assets/_Project/Core/Systems/HomeSystem/Runtime/BondLite/BondMissionRun.cs` + `.meta`
   - `miso/Assets/_Project/Core/Systems/HomeSystem/Runtime/BondLite/BondLevelListener.cs` + `.meta`
   - `miso/Assets/_Project/Core/Systems/HomeSystem/Runtime/BondLite/BondSources.cs` + `.meta`
   - `miso/Assets/_Project/Resources/BondSettings.asset`
   - `miso/Assets/_Project/Core/Systems/HomeSystem/Editor/BondLevelUpQueueTests.cs` + `.meta`
   - `miso/Assets/_Project/Core/Systems/HomeSystem/Editor/BondSourcesTests.cs` + `.meta`
2. `feat(levels): every level listens for Bond through LevelBase` (prefab shared by all levels, own commit so it can be reverted alone):
   - `miso/Assets/_Project/Content/Levels/LevelBase.prefab`
   - `miso/Assets/_Project/Core/Systems/HomeSystem/Editor/BondSourcesWiringTests.cs` + `.meta` (these tests fail without the prefab change)

## Other branches

`thj/home-test`, at merge (see Risks).

## How to see it

There's no Bond UI, so the points show in the save file and the panel's lock.

1. Select `Assets/_Project/Resources/BondSettings.asset`: see the values, The Hearth under Missions With No Bond, and the Rivalry entry.
2. Open `Content/Levels/LevelBase.prefab`, select `GlobalEventBus`: `Bond Sources` is on it.
3. Window > General > Test Runner > EditMode, filter on `BondSourcesTests` and `BondLevelUpQueueTests`, Run Selected.
4. In Play, on a save past The River and The Ridge that hasn't completed The Trail: complete The Trail with John or Mark in the free slot. Open `%USERPROFILE%/AppData/LocalLow/Dead Mage/miso/SaveData.json`, find the `Bond` entry: Linda-Lucy 20 to 23, and the free-slot hero with each sister at 5 to 8. Bond Lv 2 is not reached, so the Family-tree lock stays.
5. Lose a level and retry it: the numbers at the end count only the replay. Abandon a mission: nothing in the `Bond` entry changes.
6. Replay The Trail from the world map and complete it: the `Bond` entry doesn't change.

## Verifier steps

Use a save that hasn't completed The Trail; a reset is fine, say so. Read points from the `Bond` entry in `SaveData.json` (path above).

1. **Numbers after The Trail with a free-slot hero:** note the entry, complete The Trail with John or Mark picked. Linda-Lucy 20 to 23 (15 + 5 + help up to 3). The hero with each sister 5 to 8. The hero not picked: no change. River and Ridge add nothing between the sisters; each pays its own pair 5 to 8.
2. **Esc on the mission-end panel, Restart Level:** complete a mission, Esc while the end panel shows, Restart Level, win again. The entry must not change the second time (the `Paid` flag).
3. **Esc on the mission-end panel, Quit:** this is the known hole. Complete a mission, Esc, Quit to main menu, re-enter and complete it. Expect a second payment, and the mission unrecorded after the quit. Please confirm or correct what I read in code, and whether the end panel accepts Esc at all.
4. **The level key:** it is `(ActiveMission, GraphSeed)`. With a two-level mission (or a debugger on `BondMissionRun.BeginLevel`): win level 1 with help, lose level 2 with help, retry, and complete. Only level 1's help and the retry's count, held to 3. A restart must keep the seed; leaving and re-entering must change it, so a fresh entry starts with no help.
5. **Failure:** lose with Return Home available: nothing changes. **The Hearth:** complete it: no `Bond` change.
6. **Replay:** replay a completed mission: nothing changes.
7. **Throughout:** the end panel appears normally in all of the above, and the console has no Bond errors.

## Review fixes

Applied from the review (verdict FIX), then the full suite was re-run.

1. Double pay through Restart Level: `Paid` flag on `BondMissionRun`, cleared only by a different key; `CompleteMission` returns early. Tested.
2. First completion only (THJ): `mission.Completed` at the event; a replay pays nothing and forgets its help. Tested. No arithmetic test assumed a replay paid.
3. One throwing subscriber: catch per pair; the test now uses a three-hero squad and checks the other two pairs are paid.
4. `Role_OfAnEnemyDoesNotCount`: the enemy owner is nicknamed "Lucy", so it can fail now.
5. `Role_TargetingAnEnemy...`: the enemy target is named "Linda", so it can fail now.
6. River and Ridge also assert `FreeSlotsCount == 0`.
7. `LevelBase.prefab:513`: `m_Name: ` with Unity's trailing space. Confirmed in the bytes.
8. The two wiring tests moved to `BondSourcesWiringTests.cs`, for the prefab commit.

`LevelBase` stays as the location, as the review confirmed.

## Review (coordinator's condensed copy, 2026-11-06)

**FIX.** Read only. Must fix: double pay via Restart Level. Should fix: per-pair catch, two tests that can't fail, free-slot check, prefab trailing space, commit split. `LevelBase` location confirmed. Tally trace correct otherwise. Values verified: 15, The Trail 20 to 23, the Yard 25 to 28; only The Trail has both sisters before the Yard.

**For THJ, not in this chunk:** Pause may stay live on the end screen because `SwitchTurnIE`'s `EndTurn` has no `_levelEnded` check (`CombatLevelRunHandler.cs:469-478`, `PlayerController.cs:255`, `:1002`). A core issue. The end panel's input lock (`7e5d28da5`) may already cover it; unverified.
