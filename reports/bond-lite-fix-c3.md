# Report: Bond Lite play fixes, C3: station pages play on unlock (+ Marks-Sisters node text)

Plan: plans/onboarding/2026-11-07-bond-lite-play-fixes.md (C3 + "Text and adjustments"; D-431, D-436; THJ's follow-ups after his C3 play: no camera focus, the Marks-Sisters node text)    Agent: miso-implementer (opus)    Branch: thj/bond-lite
Outcome: done. The flow was played by THJ; the version without the camera needs a quick re-check.

## What changed

Runtime (Assembly-CSharp), `miso/Assets/_Project/Features/Home - Imported/___Khashayar/`:
- `HomeInteractables.cs`: `class` → `partial class` (one word).
- `HomeInteractables.PageOnUnlock.cs` (new): serialized `playPageOnUnlock` (default off, tooltip); `Page`, `PlaysPageOnUnlock`, `IsUnlocked` (re-reads the lock, same rule as the click), `PageState()`.
- `HomeStationPageRules.cs` (new): pure rule. A page plays when the station asks for it, is unlocked, has a `PlayJustOnce` page, and `PlayedSequencesTracker` doesn't list it; `PagesToPlay` returns indexes in the order given (scene order).
- `HomeManager.cs`: `class` → `partial class`. `StartIE` gets one step after the (now empty) InitialTutorial step and before `SetInteractionMode(All)`/`EndOpening()`: `yield return PlayStationPagesOnUnlock();`. The `OpeningInProgress` doc comment mentions the pages.
- `HomeManager.StationPages.cs` (new): collects the scene's `HomeInteractables` in hierarchy order, applies the rule, and for each eligible station calls `sequencePlayer.Play(page, onComplete)` and waits for the page to close. There is no camera move and no input handling. Selection and `Play` sit in try/catch: an exception is logged and the step moves on, so `EndOpening` still runs. A flagged station with no once-per-save page logs a warning and is skipped.

Editor tooling, `miso/Assets/_Project/Features/Onboarding/Editor/`:
- `HomeVisitsWiring.cs`: the Workshop page text moved to `WorkshopPageText` with item 5's change ("• This is the Workshop. Gear up the pair going out next." / "• Equip each Bergson here before you pick the next mission."). `Run()` also builds the skill tree page. The class summary and the log line say "station pages".
- `HomeVisitsWiring.SkillTree.cs` (new): `EnsureSkillTreeSequence()` creates `Resources/Tutorials/SkillTree_Tutorial.asset` (title "Skill Tree", item 2's three bullets, same placeholder image as the other pages) and `Resources/Sequences/HomeVisits/SkillTree_FirstOpen_TutorialSequence.asset` (`PlayJustOnce`).
- `OnboardingOpeningSetup.Stations.cs`: the Workshop-only page step (`EditWorkshopTutorial` and its two constants) is removed; `EditStations` calls `EditStationPages` instead.
- `OnboardingOpeningSetup.StationPages.cs` (new): a table of two rows (Equipments Cabinet → Workshop page, Grandma Table → skill tree page). Sets `tutorialSequence` and `playPageOnUnlock` on each. Messages: "station 'X' shows its page on first open" (the old wording, so the existing repair test still matches) and "station 'X' plays its page by itself when it opens". The drift test `CheckOnTheProject_ReportsNothingToChange` covers them.

Data (made by Wire Home Visits, then Apply Opening Setup: "3 change(s), 0 problem(s)"):
- `Resources/Tutorials/Workshop_Tutorial.asset`: the new text.
- `Resources/Tutorials/SkillTree_Tutorial.asset` + `.meta` (new).
- `Resources/Sequences/HomeVisits/SkillTree_FirstOpen_TutorialSequence.asset` + `.meta` (new, guid `df1f13e7346bf034f9a37b54371230a2`).
- `Home - Scene.unity`: scene diff below.
- `Features/Player/Lucy/Prefabs/Unit_Lucy.prefab`: the override `skillTree.nodes.Array.data[7].description` is now "Lucy and Linda combine their ranged skills into one powerful coordinated shot." (the "[Duo] " prefix is dropped). One 2-line YAML hunk, checked with a load after refresh. The other heroes' "[Duo]" nodes are untouched.

Tests:
- `Onboarding/Editor/HomeStationPageRulesTests.cs` (new, 8 tests): each condition of the rule, scene order with mixed stations, empty or null input, and `HomeInteractables.PageState()` on a real component.
- `Onboarding/Editor/HomeVisitsTests.StationPages.cs` (new partial, 6 tests): both stations have their page and the flag; the skill tree page's title and text; the Workshop page text; the two pages have different names; Apply Opening Setup repairs the Grandma page and both flags in a scratch copy of the scene.

### Scene diff (`Home - Scene.unity`, made by Apply Opening Setup)
- All six `HomeInteractables` get the new field: `playPageOnUnlock: 1` on Equipments Cabinet (`&1402771017`) and Grandma Table (`&2034088533`), `0` on the other four.
- Grandma Table: `tutorialSequence: {fileID: 0}` → `{fileID: 11400000, guid: df1f13e7346bf034f9a37b54371230a2, type: 2}`.
- Nothing else (12 added lines, 1 changed).

## Camera: found, then dropped (THJ)

THJ's play found the framing wrong: forest outside the house during both pages. Cause, confirmed in Play: before `cameraHandler.Initialize()` runs, the `MainCamera` lens sits at a scene offset of (-12.69, -24.38) from the `CameraHandler` rig. `Initialize()` zeroes it, and the offset is what makes the intro end on the start view. `CameraHandler._targetZoom` is also still 0 then, so a focus zooms in to `minZoom`. The rig did reach the cabinet (10.89, 0.14), but the lens rendered (-1.8, -24.2). Calling `Initialize()` before the focus fixed it: lens on the cabinet, zoom 7, checked with a screenshot. THJ then decided against any station focus ("the page's image is enough"), so the focus, the ease-back, the input re-lock, `HomeInteractables.FocusPoint` and the focus timeout are all removed. The pages now play over the normal start view. `CameraHandler` was not changed.

## Acceptance criteria

- [x] The flag is on `HomeInteractables`, default off, and its `tutorialSequence` is the page: code; the other four stations serialize the default 0.
- [x] Pages play after the completion sequence and the empty InitialTutorial step, before `EndOpening()`, in scene order: code. Order and filter are covered by `HomeStationPageRulesTests`.
- [x] Once per save through `PlayJustOnce` + `PlayedSequencesTracker`, not PlayerPrefs: the step uses the same `SequencePlayer.Play` as the click. A page seen by clicking doesn't auto-play (rule test), and a later click doesn't replay it. THJ's play: the pages play once.
- [x] Stations stay blocked until the pages finish (inside the `OpeningInProgress` window). THJ's play: clicks are fine after.
- [x] A page that throws or is missing is logged and skipped, so `EndOpening` still runs (code; see Risks for the limit).
- [x] The Grandma Table page and both flags come from the setup and are covered by the drift test: tests pass.
- [x] Workshop text tweaks (item 5): test.
- [x] Marks-Sisters node text without "[Duo] ": checked by loading the prefab.
- [ ] Quick re-check by THJ: the pages now play with no camera move (the view stays on the start view).

EditMode suite after the final change: 1610 tests, 1609 passed. The only failure is the known `AIRegressionTest.Baseline_MatchesCurrentAI`. No compile errors.

## Save reset

No. To reproduce the page in Play, I removed the Workshop page's name from the in-memory played list (through reflection on `SaveLoadManager`'s cached entry). I then marked it played again before stopping, so THJ's save on disk ends with the same played set (possibly in a different order). No save shape changes.

## Decisions I made

- **Pages need `PlayJustOnce`** (Tier 1): a flagged station whose page can replay is skipped with a warning instead of playing on every load.
- **Scene order = hierarchy order** (root objects, then depth-first), found at runtime from `HomeManager`'s scene. No serialized station list, so no extra scene wiring.
- **Setup refactor (same behaviour):** the Workshop-only page step became the table-driven `EditStationPages`, keeping the Workshop's message wording.
- **No input handling in the step:** without camera moves it isn't needed. Closing a page still calls `OnPanelClosed` (input mode All) before `EndOpening`, as the Hearth's World map page already does; clicks stay blocked by `OpeningInProgress`.
- **Prefab text edit by hand:** a 2-line, well-scoped YAML change to the existing override, so no editor script.

## Needs THJ

None.

## Docs to update

- `tech/home-system.md` (or the onboarding Home notes): station pages on unlock: `HomeInteractables.playPageOnUnlock`, `HomeManager.StationPages.cs`, rule `HomeStationPageRules`, set by Apply Opening Setup's station-page table. No camera move.
- `tech/classic-fallback.md`: the flag defaults off and only the opening setup sets it, so classic Home is unaffected.
- A camera fact worth keeping in `tech/home-system.md`: at Home, until `CameraHandler.Initialize()` runs, the `MainCamera` lens carries a scene offset from the rig and the zoom target is 0. Any focus during Home's opening must call `Initialize()` first. This matters for C4's planned yard camera-focus step.
- Plan log: the C3 commits.

## Risks and loose ends

- **C4's yard focus** (a camera-focus step before Y12-1) will hit the same problem if it plays during the opening: see the camera fact above.
- **An exception inside a page's own coroutine** still leaves the opening waiting (the known opening limit). There is no timeout, because the player may still be reading.
- **Old saves:** a save that already has the Workshop open but never clicked it gets the Workshop page on its next Home load.

## Proposed commits

1. `feat(home): a station can play its page by itself the first time Home opens with it unlocked` (risky: every Home load):
   `Features/Home - Imported/___Khashayar/HomeInteractables.cs`, `HomeInteractables.PageOnUnlock.cs` + `.meta`, `HomeStationPageRules.cs` + `.meta`, `HomeManager.cs`, `HomeManager.StationPages.cs` + `.meta`, `Features/Onboarding/Editor/HomeStationPageRulesTests.cs` + `.meta`.
2. `feat(onboarding): the Workshop and the skill tree play their pages by themselves when they open` (plain: setup + data + tests):
   `Features/Onboarding/Editor/HomeVisitsWiring.cs`, `HomeVisitsWiring.SkillTree.cs` + `.meta`, `OnboardingOpeningSetup.Stations.cs`, `OnboardingOpeningSetup.StationPages.cs` + `.meta`, `HomeVisitsTests.StationPages.cs` + `.meta`, `Resources/Tutorials/Workshop_Tutorial.asset`, `Resources/Tutorials/SkillTree_Tutorial.asset` + `.meta`, `Resources/Sequences/HomeVisits/SkillTree_FirstOpen_TutorialSequence.asset` + `.meta`, `Features/Home - Imported/___Khashayar/Home - Scene.unity`.
3. `fix(home): Marks-Sisters node no longer reads as the Duo itself` (plain, data):
   `Features/Player/Lucy/Prefabs/Unit_Lucy.prefab`.

All paths are under `miso/Assets/_Project/`. Each commit compiles on its own. Not staged: `AIFactionBrain.cs`, `AIUnitBrain.cs`, `PreloadScreen.unity`, `ProjectSettings/*` (pre-existing, not mine).

## Other branches

None (onboarding-only data; the runtime flag defaults off). Commit 3 is plain text; whether `main` has the same node is for the coordinator to check.

## How to see it

1. Play from `Scenes/PreloadScreen.unity` with a save that has The Hearth done but neither River nor Ridge.
2. Win The River (or The Ridge). Back at Home, after the intro and any completion lines, the "Workshop" page opens over the start view ("This is the Workshop. ..."). Close it: the stations take clicks.
3. Click the Workshop: the panel opens with no page. Leave Home and come back: no page.
4. Win the other mission. Back at Home, the "Skill Tree" page opens. Close it and click the Grandma Table: the panel opens with the guided spend and no page. Lucy's Family tree shows the Marks-Sisters node text without "[Duo] ".
5. Any later load: no station page.
6. `Tools > Onboarding > Check Opening Setup` reports nothing to change.
