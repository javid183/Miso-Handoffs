# Report: Onboarding C5b, Home visits as data

Plan: plans/onboarding/2026-11-02-onboarding-c5-home-visits.md (C5b)    Agent: miso-implementer    Branch: thj/onboarding
Outcome: done (play check waiting on THJ)

## What changed

`git diff --stat` of the tracked files this chunk touched (the rest are new files):

```
 Content/Levels/M0 - The Hearth.asset                 |  2 +-
 Content/Levels/M2 - The Trail.asset                  |  6 +--
 Content/Levels/MS1 - The River.asset                 |  2 +-
 Content/Levels/MS2 - The Ridge.asset                 |  2 +-
 Features/Home - Imported/___Khashayar/Home - Scene.unity | 50 ++++++++++-----
 Features/Onboarding/Editor/OnboardingOpeningSetup.Scenes.cs |  1 +
```

New files (all under `miso/Assets/_Project/`, each with its `.meta`):

- `Features/Onboarding/Editor/OnboardingOpeningSetup.Stations.cs`: builder partial. Table of the five stations (found by GameObject name), the Family tab (found by the entry flagged `isFamilyAbilitiesBtn`, not by index) and the Workshop's `tutorialSequence`. Check/Apply handle them, so the existing drift test covers them.
- `Features/Onboarding/Editor/OnboardingOpeningSetup.Scenes.cs`: one line, calls the new step from the Home scene step.
- `Features/Onboarding/Editor/HomeVisitsWiring.cs`: menu **Tools > Onboarding > Wire Home Visits** (re-runnable). Creates the Searching state, the Workshop page and sequence, the clue and Yard sequences, and sets `homeState` (4 missions), `initiationSequence` and `completionSequence` (Trail). Already run.
- `Features/Onboarding/Editor/HomeVisitsTests.cs`: 15 tests (below).
- Data: `Content/Levels/HomeStates-Idles/Searching - HomeState.asset`; `Resources/Tutorials/Workshop_Tutorial.asset`; `Resources/Sequences/HomeVisits/` (`Workshop_FirstOpen_TutorialSequence`, `MapTable_Clues_DialogNodeSequence`, `Yard_Midnight_DialogNodeSequence`, folder `.meta`).
- Mission assets: Hearth, River, Ridge get `homeState`; Trail gets `homeState`, `initiationSequence`, `completionSequence`.
- Home scene, written by Apply Opening Setup: Workshop River OR Ridge (any = true) plus its page; Grandma Table River AND Ridge (any = false); Bookshelf, Training Field, Cooking Cabinet = M4 only; Family tab = The Trail.
- Doc: `claude-handoff/tech/onboarding-merge.md` (a Home scene row, an onboarding-only files note, and the "builder does not re-apply" bullet updated).

## Acceptance criteria

- [x] Workshop opens after River or Ridge; first-open page once per save: `WorkshopOpensAfterTheRiverOrTheRidge`, `WorkshopShowsItsPageOnFirstOpen_OncePerSave` (sequence `PlayJustOnce`, one page, no tag). Play check pending.
- [x] Skill tree after River and Ridge; Family tab after The Trail; Bookshelf, Training Field, Cooking Cabinet after M4: `SkillTreeOpensAfterTheRiverAndTheRidge`, `FamilyTabOpensAfterTheTrail`, `OtherStationsOpenAfterTheWhiteMothers` (x3).
- [x] Searching state on Hearth, River, Ridge, Trail: `SearchingLookIsTheHomeStateOf` (x4); `SearchingLookHasQuietIdlesWithNoSharedCharacter` (no "Wolf" in an idle name, no actor used twice).
- [x] Clue scene = Trail `initiationSequence`, V2-3 to V2-7 (5 nodes: Lucy, Mark, Linda, John, Lucy): `TheTrailPlaysTheClueSceneWhenItsPinIsClicked`.
- [x] Yard stub = Trail `completionSequence`, Y12-1 to Y12-4: `TheTrailPlaysTheYardSceneWhenItIsWon`. No Family point. Q-4 not added (see decisions).
- [x] Scene edits go through Apply Opening Setup and the drift test: Check on the project reports "nothing to change" after Apply (existing `CheckOnTheProject_ReportsNothingToChange_AndLeavesOpenScenesAlone` passes); `ApplyOpeningSetup_RepairsAStationLockInACopyOfTheScene` breaks a station and the Family tab in a copy of the scene and proves Check reports it and Apply repairs it. Rows added to `tech/onboarding-merge.md`.
- [ ] Wrist Wrap equips on Mark in the Workshop: needs the play check.
- [x] Tests: EditMode full suite 1289 run, 1288 passed, only `AIRegressionTest.Baseline_MatchesCurrentAI` red (known). Compiles clean (no new warnings from these files).

## Save reset

No reset done. For the play check: **Tools > Save Data > Clear Save Data** gives a clean start (also replays the once-only Workshop page). There is no debug menu to mark a mission complete. Complete each mission by playing it; in combat F12 (or Numpad 6) completes the objective (traps: K and F11 kill units, see `tech/editor-checks.md`).

## Decisions I made

- Stations are found by GameObject name (`Equipments Cabinet`, `Grandma Table`, `Bookshelf`, `Training Field`, `Cooking Cabinet`); nothing else tells them apart. The Family tab is found by its family flag. A missing name is a reported Problem, not a silent skip.
- The station table is a property, not a static field: static fields of a partial class initialise in an unspecified order across files, and the rows copy the table's mission rows.
- Searching idles (offsets all 0): LucySadSit, JohnWatchCliff, LindaSadLay, MaryReading, BenDrinking, KevinWaterPlant, JoeyFigure. MaryRest (Wolf's Blood state) is left out because it also seats Lucy, which the manager would skip as a conflict; MaryReading comes from the old M2 look. No idle has "Wolf" in its name. Position overlap between the idles is untested in Play.
- The clue scene is a plain `DialogNodeSequence`, **not** play-once: it replays whenever the Trail pin is picked again after another pin. Plan says nothing; set `PlayJustOnce` on it if THJ wants it once.
- Q-4 left out: it follows Y12-6 (the straw-target race), which the stub does not have, so it would read wrong after Y12-4.
- Workshop page: one page, reused existing placeholder image (the "Asleep" panel picture).
- V1-1 to V1-4b (Ben and the go-between jokes) not built: not in the plan's C5b list and they need roster-dependent branching.
- The test that repairs a scene copy ignores Unity's own "Unsupported type Vector2f" log, which Unity writes when it saves the copy (the project scene saved without it).

## Needs THJ

none

## Placeholder lines (untagged, D-348)

- Workshop page, title "Workshop": "• Gear up the pair going out next." / "• Equip each hero here before you pick the next mission."
- Clue scene: Lucy "Her prints, her blood, her fur. And Claws cut down with a stone axe." / Mark "A man's tracks, deep. Carrying something." / Linda "And herbs. A poultice." / John "Someone's carrying her. And tending her." / Lucy "Then where is he taking her?"
- Yard: Linda "It's past midnight." / Lucy "Can't sleep. I keep seeing that pile." / Lucy "If they've hurt her…" / Linda "Then we'll be ready."

## What Home shows after each mission

`homeStateMissionMode` is FurthestCompleted: the completed mission deepest in the graph wins; at equal depth (River and Ridge) the later completion wins. All four missions now carry Searching, so:

- Fresh save (no mission done): `GameData.InitialHomeState` (unchanged, not in this chunk).
- After Hearth, River, Ridge, or Trail: Searching in every case, whichever order the pair is played in.
- After M4 (The White Mothers): M4's own state if set, otherwise the scene default `M4 - HomeState` (unchanged).
- Home stations by then: Workshop after the first pair mission; skill tree after both; Family tab after the Trail; Bookshelf, Training Field, Cooking Cabinet after M4.

## Scene diff noise check

`Home - Scene.unity`: 50 changed lines, all of them the edits above except one block: Unity re-adds nine empty `GlobalEventBus` UnityEvent fields (`onSynergyTriggered`, `onFamilyRoleActivated`, `onRewardsGranted`, `onRunUpgradeGranted`, `levelEnded`, `onCheatUsed`, `onFamilyRolePrompt`, `onFamilyRoleOutcome`, `onFamilyRoleBadgeHover`), about 27 added lines. This is the known noise in `tech/onboarding-merge.md`; left in (no hand-editing of the scene). It is harmless; THJ can accept or strip it.
Also seen: `Scenes/PreloadScreen.unity` has a one-line change (`applyFPSLimit: 1`) that I did not make (editor reimport noise); do not stage it. The `GB_*` prefabs, `AIFactionBrain.cs`, `AIUnitBrain.cs`, `ProjectSettings/` and the two Hearth memory tests were not touched.

## Docs to update

- `tech/onboarding-merge.md`: done (rows added).
- Plan C5b status, `status.md`, `build-log.md`: coordinator.
- `Mission.homeState` tooltip is wrong about "clears idles" (plan code fact); left alone (core).

## Risks and loose ends

- The Home scene's stations are found by name; if home-test renames one, Apply reports a Problem instead of changing it.
- Idle overlap on screen is unchecked (all offsets 0).
- The Hearth open Home state and the Grandma Table badge are still out of scope.
- C5c (guided spend) is not started.

## Proposed commits

Dependency order:

1. `feat(onboarding): builder re-applies the Home station locks, Family tab and Workshop page` (plain): `Features/Onboarding/Editor/OnboardingOpeningSetup.Stations.cs` (+`.meta`), `OnboardingOpeningSetup.Scenes.cs`, `HomeVisitsWiring.cs` (+`.meta`), `HomeVisitsTests.cs` (+`.meta`).
2. `feat(onboarding): Home visit data: Searching look, Workshop page, Trail clue and Yard scenes` (plain, data): `Content/Levels/HomeStates-Idles/Searching - HomeState.asset` (+`.meta`), `Resources/Tutorials/Workshop_Tutorial.asset` (+`.meta`), `Resources/Sequences/HomeVisits/` and `HomeVisits.meta`, the four Mission assets (Hearth, River, Ridge, Trail).
3. `feat(onboarding): Home stations open as the opening progresses` (risky, shared scene): `Features/Home - Imported/___Khashayar/Home - Scene.unity`. Needs commit 2 for its Workshop page reference; own commit so it can be reverted alone.

## Other branches

`thj/home-test` also edits the Home scene: after a merge take its scene whole and run Apply Opening Setup (see `tech/onboarding-merge.md`).

## How to see it

Start with Tools > Save Data > Clear Save Data, then Play from `Scenes/PreloadScreen.unity`.

1. Hearth: play the memories, return Home. Idles are the quiet Searching set. Workshop, skill tree, Bookshelf, Training Field, Cooking Cabinet are all locked; Family tab locked.
2. Play The River. At Home the Workshop opens (hover then click): its page shows once; close it, click again, no page. Equip the Wrist Wrap of Power on Mark. The skill tree is still locked.
3. Play The Ridge. The Grandma Table opens. The Trail pin appears (glowing).
4. Click the Trail pin: the clue scene plays (5 lines), then the mission info panel. Picking another pin and coming back replays it.
5. Play The Trail. Back at Home the Yard stub (4 lines) plays and the Family tab opens. The Bookshelf, Training Field and Cooking Cabinet stay locked until M4 is won.
6. Alternative order: Ridge first, then River: same results (Workshop opens after whichever comes first).
7. Editor side: Tools > Onboarding > Check Opening Setup logs "nothing to change".
