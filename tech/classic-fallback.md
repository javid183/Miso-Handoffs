# Classic-opening fallback recipe

Owner: coordinator. Decision D-396 (2026-11-05). Branch scope: `thj/onboarding` (the working main) → a `classic-intro` branch cut from it when needed.

**When:** THJ has to show the game and the onboarding isn't ready. This recipe swaps the opening back to the classic missions and keeps every general improvement made since.

**Keep it current:** any onboarding change that adds or moves a wiring point updates this file in the same task (coordinator, at Sync docs).

**Rehearsed:** not yet (planned, D-396).

Facts from the Explore audit of 2026-11-05 (`thj/onboarding` @ `4a0c8c080` vs tag `classic-intro-base` = `main` @ `194bd566b`). Paths are under `miso/Assets/_Project/`.

## The classic opening (as tagged)

New Game starts on M1 (the scenes' `initialMission`). Graph: M1 → AND → (M2, M5) → AND → (M3 Blood Trail, M3 Mark Intro) → AND → (M4, M6); M6 → M7.

| Mission | Squad | Levels |
|---|---|---|
| M1 "John's Map" | John, Lucy | `Level1-C1_TArtEx`, `Level1-C1-2`, `Level1-C2` |
| M2 "Ryker is lost" | Lucy, John | `LevelLucyJohn-C1/C2/C3` |
| M5 "The Healer" | John, Linda, Lucy | `LevelE1-C1/C2` |
| M3 Blood Trail | John, Linda | `LevelLindaJohn-C1/C2` |
| M3 Mark Intro | Mark, Lucy | `LevelMarkIntro-C1/C2/C3` |
| M6 / M7 | John + 2 picks | E2 levels + safe rooms / `LevelE3-C1` |
| M4 "Into the Rootwell" | John, Linda, Lucy | 7 Level2/Level3 levels |

The onboarding didn't edit any classic mission, level or tutorial sequence. It only dropped their nodes from the graph, except M4 (W5). Classic levels touched since then got only general changes: the Encore animation data `4a0c8c080`, and the `Level1-C1-2` sprites moved under Environment (`89f4981fe`).

## Wiring points and how to undo each

Restore **all of them together**. Partial restores break play: Mark never unlocks, or New Game starts on a mission that isn't in the graph. **Never run Tools › Onboarding › Apply Opening Setup or Apply M4 Squad Slots afterwards.** Both are forward-only.

| # | What | Files (commit) | Undo |
|---|---|---|---|
| W1 | Mission graph: Hearth → River and Ridge → Trail → M4 | `Resources/Game Data.asset` (`bb9982c87`) | `git checkout classic-intro-base -- <file>` (graph-only diff) |
| W2 | New Game start mission = Hearth | `Scenes/IntroScreen.unity`, `Scenes/MainMenuScene.unity` (`bb9982c87`) | take both from the tag |
| W3 | Home: map pins renamed or hidden; Mark's select button, Mark tab and Family tab unlocks; station locks (Workshop after River or Ridge with its first-open page, skill tree after both, Bookshelf / Training / Cooking after M4); `GuidedSkillSpend` on the UpgradesPanel | `Features/Home - Imported/___Khashayar/Home - Scene.unity` (`bb9982c87`, `b2659da27`, `14330fd06`) | take from the tag (nothing general mixed in) |
| W4 | Mark unlocks after the Hearth | `Features/Player/Mark/Prefabs/Unit_Mark.prefab` (`bb9982c87`) | **mixed file** (Mark's socket and default gear `8826a11f1`, `106edafec` are general): edit only `unlockedAfterMission` back to M3 Mark Intro, guid `c15aeee0903ebe8498e07d7ca1590150` |
| W5 | M4 squad: Lucy + Linda + 1 pick (no Toba); John's placed unit swapped for a deploy slot in 7 levels | `Content/Levels/M4 - The White Mothers.asset`; `Level2/LevelDomFight`, `Level2-C1-TArtEx`, `Level2-C3-1`, `Level2-C3-2`, `Level3/Level3-C1`, `DungeonSafeRooms/LevelDivineRelicRoom 1` (`f6648ed08`) | take the asset and the 6 levels from the tag, together |
| W5b | same, `Level2/Level2-C2` | `f6648ed08` + general `9ba3b8421` (objective split) | take from the tag, then run Tools › Levels › Split Shared Objective Conditions; or `git show f6648ed08 -- <file> \| git apply -R` (overlap not checked) |
| W6 | Catch & Return open from the start | `Resources/Unlockables/UnlockableSet.asset` (`a7320be82`) | take from the tag (`MarkLindaSynergy.unlockedByDefault` back to 0) |

**Checked and inert:** no auto hooks start the onboarding. The only new `[InitializeOnLoadMethod]` is general editor tooling. Onboarding `Resources/` assets are only reached by direct reference. `LevelAbilityLock` does nothing unless a level has one. Everything else onboarding-only goes inert once W1 to W6 are undone: the Hearth, River, Ridge and Trail missions and levels, `Features/Onboarding`, the sequences.

## Tests that go red after the restore (expected; mark Ignore or delete on the fallback branch)

- `OnboardingMissionGraphTests`: the graph tests and `Mark_JoinsAfterTheHearth…`. The roster and level tests should still pass.
- `OnboardingOpeningSetupTests.CheckOnTheProject_ReportsNothingToChange…`
- `HomeVisitsTests`: `WorkshopOpensAfterTheRiverOrTheRidge`, `SkillTreeOpensAfterTheRiverAndTheRidge`, `FamilyTabOpensAfterTheTrail`, `WorkshopShowsItsPageOnFirstOpen_OncePerSave`
- `GuidedSkillSpendTests.HomeSceneSkillTreePanelHasTheGuidedSpend`
- `M4SquadPickTests`: slot and roster tests
- `SearchRidgeTests.CatchAndReturnIsOpenByDefault`
- Only if done wrong: `MarkWeaponSocketTests` (`Unit_Mark` taken whole), `SharedObjectiveConditionTests` (`Level2-C2` taken whole without the split).

## Steps

1. THJ: commit or stash the work in progress, close Unity, create `classic-intro` from the current `thj/onboarding`, and switch to it. Git writes need his yes.
2. Implementer: undo W1 to W6 as in the table, in one commit.
3. Implementer: handle the red tests above (Ignore with a plain reason, or remove), in their own commit.
4. Open Unity, Ctrl+R, EditMode: only the known AI red may remain.
5. **Optional, the shortened classic** (THJ's route, D-396): M1 → M2 or M3 Mark Intro → M5 (optional) → M4, M7 out. That's a graph edit in `Game Data.asset` plus the Home station and pin unlocks that name the removed missions (W3's classic values reference M2, M5, M3 Blood Trail, M3 Mark Intro). Needs a small design pass for which unlock follows which mission.
6. **Tutorial bits the memory absorbed** that the classic shortening would lose: Linda's Watch and the Duo, taught in classic M3 Blood Trail. If M3 Blood Trail is dropped, move those beats into M2 or M5 (design pass).
7. THJ plays M1 → M4. Make a player build.

## Log

- 2026-11-05: written from the audit; tag `classic-intro-base` made.
