# Report: Onboarding C1, mission graph, missions, recruits, world map

Plan: plans/onboarding/2026-10-26-onboarding-structure-tech.md (C1)    Agent: miso-implementer    Branch: thj/onboarding (no git writes, nothing staged)
Outcome: done (data and scene; not play-checked)

## What changed

New Mission assets (all in `miso/Assets/_Project/Content/Levels/`, each with its `.meta`):
- `M0 - The Hearth.asset` (+ .meta): missionName "The Hearth", number 0, level graph copied from the old M1 (Level1-C1_TArtEx, Level1-C1-2, Level1-C2), roster John + Lucy + Linda fixed, rewards 0 XP / 0 gold, no sequences, no homeState.
- `MS1 - The River.asset` (+ .meta): "The River", number 1, one level `LevelLucyJohn-C1` (places John and Lucy), roster John + Lucy fixed, 40 XP / 5 gold.
- `MS2 - The Ridge.asset` (+ .meta): "The Ridge", number 2, one level `LevelE3-C1` (3 deploy slots), roster Linda + Mark fixed, 40 XP / 5 gold.
- `M2 - The Trail.asset` (+ .meta): "The Trail", number 3, one level `LevelE4-C1` (3 deploy slots), roster Lucy + Linda fixed + 1 free, `forcedExcludedUnits` = Toba, 40 XP / 5 gold.
- Old `M2 - Ryler is Lost` and every other old asset are untouched.

Edited:
- `miso/Assets/_Project/Resources/Game Data.asset`: mission graph rebuilt (see below). Edited through the serialized graph API from the editor, not by hand.
- `miso/Assets/_Project/Features/Player/Mark/Prefabs/Unit_Mark.prefab`: `unlockedAfterMission` M3 Mark Intro -> The Hearth (one GUID on one line). Toba untouched (still M4).
- `miso/Assets/_Project/Scenes/IntroScreen.unity`: `initialMission` M1 -> The Hearth (one line). Needed: this is what New Game starts.
- `miso/Assets/_Project/Scenes/MainMenuScene.unity`: `initialMission` M1 -> The Hearth (one override). Needed: Start checks `initialMission.Completed` to choose Intro vs Home.
- `miso/Assets/_Project/Features/Home - Imported/___Khashayar/Home - Scene.unity` (the Home scene; +44 lines, -4):
  - World map buttons re-pointed (not copied, smaller diff): `MapButton` M1 -> Hearth (renamed `MapButton Hearth`), `MapButton John Linda` M3 Wolf -> River (`MapButton River`), `MapButton 1-1` M5 -> Ridge (`MapButton Ridge`), `MapButton Lucy John` M2 -> Trail (`MapButton Trail`). Positions kept, so the layout reads Hearth -> River / Ridge -> Trail -> M4 (M4's button unchanged).
  - Deactivated the buttons of M6, M7 and M3 Mark Intro (`MapButton 1-2`, `MapButton 1-3`, `MapButton M2 (4)`), the same way M8-M14 are already inactive.
  - Mark's `CharacterSelectButton.unlockedAfterMission` M3 Mark Intro -> The Hearth. Without this Mark never shows in the character select.
  - `UpgradesPanel` characters[3] (Mark) `requiredMissionToUnlock` M3 Mark Intro -> The Hearth.
- `miso/Assets/_Project/Core/Levels/Editor/OnboardingMissionGraphTests.cs` (+ .meta): new, 10 EditMode tests, namespace `MISO.Core.Levels.EditorTests`.

`WorldMapPanel.prefab` was not touched (its own old buttons stay; the Home scene instance carries the overrides above).

### The new graph in `Game Data.asset`

```
M0 The Hearth (initial) -> MS1 The River --\
                        -> MS2 The Ridge ---+-> [AND gate] -> M2 The Trail -> M4 Into the Rootwell
```

Nodes 21 -> 15, edges 21 -> 14. Removed: M1, old M2, both M3s, M5, M6, M7 and the four gate nodes that only served them. Not changed: M4 (kept its node), and the dead branch M8, M9, M11 -> M10, M12-M14 behind the input-less gate (still unreachable as before). The Hearth node is flagged `isInitialLevel`; before, M1 was initial only because it was the single entity node with no incoming edge. Removing (not just un-edging) the old nodes matters: a node with no incoming edge is unlocked from the start.

## Acceptance criteria

- [x] Fresh save: the Hearth is the only open mission. Test `Hearth_IsTheOnlyOpenMissionOnAFreshSave` (graph check with no completions); `InitialMission` = The Hearth (`Hearth_IsTheInitialMission`). `WorldMapPanelUI.Start` hides every button whose mission is not `IsMissionUnlocked`, so the other pins stay hidden.
- [x] After the Hearth, River and Ridge both open (and show as new: `IsNew` = not visited and not completed, set by the existing button code). Test `MissionsOpenInOrderAsTheyAreCompleted`, `RiverAndRidge_DependOnlyOnTheHearth`.
- [x] The Trail opens only when both are complete (AND gate, `CombineMode.AND`). Tests `Trail_NeedsBothRiverAndRidge_ThroughAnAndGate`, `MissionsOpenInOrderAsTheyAreCompleted`.
- [x] M4 opens after the Trail. Tests `RootwellDependsOnTheTrail`, `MissionsOpenInOrderAsTheyAreCompleted`.
- [~] The Trail's character select offers John or Mark only for the free slot: data is right (Lucy + Linda fixed and locked, Toba in `forcedExcludedUnits` -> Unavailable, one free slot; John always available, Mark available once the Hearth is complete). Roster test `Rosters_FollowTheOpeningPlan` and `Mark_JoinsAfterTheHearth_TobaStaysOnTheRootwell`. The panel itself was not opened (needs Play); see "Not verified".
- Also covered by tests: the old opening missions are out of the graph; every new mission has an entry level and a unique name.

## Test counts

Full EditMode suite after the final change: 1056 total, 1055 passed, 1 failed (the known red `AIRegressionTest.Baseline_MatchesCurrentAI`, not touched). 10 of the 1056 are the new tests, all green. No compile errors in the console.

## Not verified

- No Play session (THJ's editor; not entered). Not seen in play: New Game starting the Hearth, the world map pins appearing and hiding, River/Ridge showing as new, the Trail's character select, the Trail's deploy placement with the free pick, M4 opening, and the Hearth's levels playing as a mission with roster John/Lucy/Linda.
- Level display names: reused levels keep their old on-screen names (e.g. "John's Map (1/3)", "Ryker is lost (1/3)", "In My Father's Arms", "Another Old Bergson House (1/2)") until the real levels replace them.
- The scene was saved from the editor; the world map layout (pin positions) was not looked at.

## Save reset

No reset done in this task. Needed to see the flow: delete the game save (or use a fresh one). Missions save under `missionName`; existing saves have M1 etc. completed but those missions are no longer in the graph, so they simply do not load, and the new ones read as new. An old save that completed M1 would still show an empty Home progression until it is reset.

## Decisions I made

- Hearth roster is John + Lucy + Linda fixed, not empty. Reason: `FactionTracker.InitializePoints` builds the family time pool and the family action points from `MissionRoster.Units`. An empty roster means a pool of 0 (`FamilyTimePoints` max is the sum of the roster's FP stat), which would also make the planned "fill FTP at level start" do nothing. The Level1 levels have no placeholders, so the roster spawns nothing extra (`FillRosterSlots` skips heroes already placed). The memory levels in the later chunk should keep this in mind: any hero a memory segment places should be in the Hearth roster to count toward the pool.
- Placeholder levels: River = `LevelLucyJohn-C1` (places exactly John and Lucy), Ridge = `LevelE3-C1` and Trail = `LevelE4-C1` (the only easy levels with 3 deploy slots; no existing level places Linda and Mark together). The Ridge and Trail levels place nobody themselves, so the roster fills the slots in order; the Ridge has 3 slots for 2 heroes (the third placeholder stays unfilled).
- Re-pointed four existing world map buttons instead of copying new ones: smaller scene diff, no change to the panel's `levelButtons` list. The pins were chosen for position (Hearth left, River/Ridge middle, Trail right, towards M4).
- `missionNumber` 0, 1, 2, 3 (shown on the pin) rather than 0, S1, S2, 2 (it is an int). Only the pin label and the dialogue export sheet name use it.
- Names and descriptions are plain, not `[PLACEHOLDER] `-tagged, because mission names are save keys and are not run through the tag stripper (only the Linda lines are). Descriptions say "(Placeholder description.)" in plain words. Names must not contain `|`.
- Rewards: Hearth 0/0; pair missions and the Trail 40 XP, 5 gold (the old M2's numbers), no material picks and no starting items (the plan puts River's Timber + Fabric and the Trail's Health Potion / Family Trinket in the River/Trail chunk). `homeState`, `initiationSequence`, `completionSequence` are empty on all four.
- Changed `IntroScreen.unity` and `MainMenuScene.unity`, and Mark's select button and upgrade tab in the Home scene: not literally in the plan, but without them New Game would start the removed M1 and Mark would never be selectable. All four are one-GUID changes.
- Also set the Hearth node to `isInitialLevel` (the implicit rule would have worked too).

## Needs THJ

None. Two things to be aware of, both in "Risks".

## Unlinked content and what happens to it now

Missions out of the graph: M1 John's Map, old M2 Ryker is lost, M3 A Wolf's Blood, M3 No More Waiting (Mark Intro), M5 The Healer, M6 The Arcanum, M7 In My Father's Arms. Their assets and levels stay.

Mission fields (sequences on the unlinked missions; they never play now because the missions cannot be started):
- M1: completion `Mission1_End_DialogNodeSequence`, homeState `M1 - HomeState`.
- Old M2: initiation `Mission2_Beginning_DialogNodeSequence`, homeState `M2 - HomeState`.
- M3 Wolf: initiation `Home_Mission3_Selected_DialogNodeSequence`, completion `Mission3_End_DialogNodeSequence`, homeState `M3 - Wolf's Blood - HomeState`.
- M3 Mark Intro: initiation `Mission3MarkIntro_Beginning_DialogNodeSequence`, completion `Mission3MarkIntro_End_DialogNodeSequence`, homeState `M3 - Mark Intro- HomeState`.
- M5: initiation `Home_Mission5_Selected_ExitHome_DialogNodeSequence`, completion `Home_Mission5_Finished_EnterHome_DialogNodeSequence`, homeState `M5 - HomeState`.
- M6: completion `Home_Mission6_Finished_EnterHome_DialogNodeSequence`, homeState `M6 - HomeState`. M7: homeState `M7 - HomeState`.
- Not re-homed. The new missions have no sequences or homeState; after each of them Home shows no managed idles (an unassigned homeState clears them).

Home stations (`HomeInteractables.UnlockAfterMissions`, Home scene). All five now wait on missions that can never complete, so **they stay locked for the whole greybox until the Home visits chunk re-homes them**. None has a `tutorialSequence` set.
- Bookshelf: M3 Mark Intro AND M3 Wolf.
- Training Field: M3 Wolf AND M3 Mark Intro.
- Cooking Cabinet: M2 AND M5.
- Grandma Table: M2 OR M5 (one is enough). Likely the planned "Workshop after River or Ridge".
- Equipments Cabinet: M3 Wolf OR M3 Mark Intro (one is enough).
- Fireplace: no requirement.
- Not re-homed: replacing them is the Home visits chunk's job (and which station is which workshop needs THJ's eye). Cost: no upgrades / equipment / cooking until then, so the first-hour flow cannot be played through the stations yet.

Other Home scene references to unlinked missions:
- `UpgradesPanel` characters[5] (the Family tab, `FamilyCharacter`): `requiredMissionToUnlock` = M3 Wolf -> the Family tab never unlocks. Not changed (belongs with the skill tree visit).
- `HomeIdleCharacter` (Ryker): requires M4. Unchanged.
- Dom/Toba `CharacterSelectButton` and `UpgradesPanel` characters[4]: M4. Unchanged.
- `HomeStates-Idles/M4 ... M7 - HomeState.asset`: each lists M3 Mark Intro as a required mission. M4's HomeState is the one the live graph still applies after M4; its requirement can no longer be met, so its idles will not show until it is re-pointed.

Tutorials (all bound to level start sequences, not to missions, so each follows its level):
- `Tutorial 1` (Level1C1) and `Tutorial_Linda` (Level1C1-2): still play, in the Hearth, because the Hearth reuses the Level1 levels.
- `Tutorial_FR_Lucy` (`LevelLucyJohnC1`): still plays, in The River, which reuses `LevelLucyJohn-C1`.
- `Tutorial_LucyLindaKillAP` (`LevelE1C1`, M5): no longer reachable. Fate to decide: re-home onto a River/Ridge/memory level or drop.
- `Tutorial_FR_Linda` (M3 Wolf C1), `Tutorial_Duo_Abilities` (M3 Wolf C2), `Tutorial_FR_John` (old M2 C2), `Tutorial_FR_Use` (old M2 C3): no longer reachable. `Tutorial_AP_Abilities` is not referenced by anything. `Home_Tutorial` (Home scene) is unaffected.

Other references to the old opening that remain by design: `WorldMapPanel.prefab` (own buttons for M1, M2, M3 Wolf, M4-M7), `Home - Scene` HomeInteractables above, HomeState assets above.

## M4's current roster (left alone)

`M4 - The White Mothers`: 3 fixed (John, Linda, Lucy), 0 free, no excluded, no forced included; items 3 / 4 and rewards as before. Its 7 levels have 0 deploy slots and place their own heroes (Toba after his duel), so the planned John-or-Mark pick needs the deploy-slot work in the M4 send-off chunk.

## Docs to update

- `design/gdd/missions-structure.md`: campaign graph and mission table (new opening, unlinked missions), MI-1 and MI-3 (Mark joins after the Hearth). Not edited by me.
- `status.md`, `build-log.md`: C1 built, not play-checked.
- `plans/onboarding/2026-10-26-onboarding-structure-tech.md`: C1 says buttons are in the "Home scene" (true, but they live in the WorldMapPanel instance there); the Hearth roster decision above.

## Risks and loose ends

- **Empty roster hazard (for C3):** see the Hearth roster decision. A mission with no roster has no family time pool.
- **Home is mostly locked** until the Home visits chunk (stations above). The flow Hearth -> map -> River/Ridge -> Trail -> M4 should run without them, but no upgrade can be spent.
- **Mission level order of `GameDataSO.Missions`** changed; I found nothing that relies on it (the all-tests run is green).
- **Reused level prefabs get their level ID from whichever mission initialises last** (`LevelBase.SetID(missionName)`); the old missions are no longer initialised, so the new ones own them now. If a reused level is later put back into an old mission and both are in the graph, the ID would clash.
- Scene noise: opening and saving the Home scene re-serialised nine empty `GlobalEventBus` UnityEvent fields (`onSynergyTriggered`, `onFamilyRoleActivated`, `onRewardsGranted`, `onRunUpgradeGranted`, `levelEnded`, `onCheatUsed`, `onFamilyRolePrompt`, `onFamilyRoleOutcome`, `onFamilyRoleBadgeHover`). I removed those added lines again, so the Home scene diff is only the intended edits. Unity will re-add them the next time that scene is saved; harmless.
- Pre-existing dirty files I did not touch: `AIFactionBrain.cs`, `AIUnitBrain.cs`, `ProjectSettings/*`, the TextMesh Pro fallback font.
- `execute_code` hit one transient "access denied" on its temp DLL partway; a retry worked. Nothing was left half-done.

## Proposed commits

In dependency order:

1. `feat(missions): add placeholder opening missions (Hearth, River, Ridge, Trail)` (plain): the four `.asset` files and their four `.meta` files in `miso/Assets/_Project/Content/Levels/`.
2. `feat(missions): rewire the mission graph, recruits and world map to the new opening` (risky: changes what a new game starts, who unlocks when, and the Home scene): `miso/Assets/_Project/Resources/Game Data.asset`, `miso/Assets/_Project/Features/Player/Mark/Prefabs/Unit_Mark.prefab`, `miso/Assets/_Project/Scenes/IntroScreen.unity`, `miso/Assets/_Project/Scenes/MainMenuScene.unity`, `miso/Assets/_Project/Features/Home - Imported/___Khashayar/Home - Scene.unity`. Needs commit 1.
3. `test(missions): check the opening mission graph, rosters and recruit unlocks` (plain): `miso/Assets/_Project/Core/Levels/Editor/OnboardingMissionGraphTests.cs` and its `.meta`. Needs commits 1 and 2.

Do not stage the four files that were already modified before this task.

## Other branches

`thj/home-test` has its own prologue and day loop; the Game Data graph and the Home scene will conflict there on merge (plan already notes it).

## How to see it

1. Look at the data without playing: select `Resources/Game Data.asset`, press "Open Mission Dependency Editor" (or Tools > Missions > Open Mission Graph): Hearth -> River, Ridge -> gate -> Trail -> M4, with the M8-M14 branch separate.
2. Run the tests: Test Runner > EditMode > `OnboardingMissionGraphTests` (10 tests).
3. In Play, from a reset save: Main Menu > Start. The Hearth (three Level1 levels) should start. When done, Home loads; open the world map: River and Ridge pins show as new, no other pin except the Hearth (completed). Complete one: the Trail stays hidden. Complete both: the Trail pin appears. Pick it: Lucy and Linda are locked in, Toba is greyed out, John and Mark are the free pick (Mark appears because the Hearth is done). Finish it: M4's pin appears.
4. Expect Home stations (Bookshelf, Cooking Cabinet, Training Field, Grandma Table, Equipments Cabinet) to stay locked in this chunk.

## Play check (for THJ)

1. Reset the game save first.
2. Main Menu > Start: the Hearth starts. After it, on the world map only the Hearth pin shows.
3. River and Ridge pins appear, both marked new.
4. Complete one of them: The Trail stays hidden/locked. Complete both: The Trail appears.
5. Pick The Trail: Lucy and Linda locked in, Toba greyed out, free slot offers only John or Mark.
6. Finish The Trail: M4 opens.
7. Mark is selectable once the Hearth is complete.

## Fix round (review)

- Test `Hearth_IsTheOnlyOpenMissionOnAFreshSave` now loops over every mission in the graph and asserts all but the Hearth are locked.
- Ridge level: searched every level prefab under Content/Levels for exactly 2 placeholder slots, or 0 slots placing Linda and Mark. Only `Test_Level_ABK_01` matched (0 slots, but it places all five heroes, a test level), so it does not fit. Left `LevelE3-C1` (3 slots, 2 heroes; the third slot stays unfilled).
