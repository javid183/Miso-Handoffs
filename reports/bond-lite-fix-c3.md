# Report: Bond Lite play fixes, C3: station pages play on unlock

Plan: plans/onboarding/2026-11-07-bond-lite-play-fixes.md (C3 + "Text and adjustments"; D-431, D-436)    Agent: miso-implementer (opus)    Branch: thj/bond-lite
Outcome: done (code, data, tests); the camera and the feel need THJ's play check

## What changed

Runtime (Assembly-CSharp), `miso/Assets/_Project/Features/Home - Imported/___Khashayar/`:
- `HomeInteractables.cs`: `class` → `partial class` (one word).
- `HomeInteractables.PageOnUnlock.cs` (new): serialized `playPageOnUnlock` (default off, tooltip); `Page`, `PlaysPageOnUnlock`, `IsUnlocked` (re-reads the lock, same rule as the click), `PageState()`, `FocusPoint` (centre of the station's Collider2D).
- `HomeStationPageRules.cs` (new): pure rule. A page plays when the station asks for it, is unlocked, has a `PlayJustOnce` page, and `PlayedSequencesTracker` doesn't list it; `PagesToPlay` returns indexes in the order given (scene order).
- `HomeManager.cs`: `class` → `partial class`; `StartIE` gets one step after the (now empty) InitialTutorial step and before `SetInteractionMode(All)`/`EndOpening()`: `yield return PlayStationPagesOnUnlock();`. The `OpeningInProgress` doc comment mentions the pages.
- `HomeManager.StationPages.cs` (new): collects the scene's `HomeInteractables` in hierarchy order (root objects, then depth-first), applies the rule, and for each station: input mode None and edge scroller off, `cameraHandler.Focus(station.FocusPoint)`, waits for the focus (3 s cap), `sequencePlayer.Play(page, onComplete)` and waits for it to close. After the last page the camera eases back to where the opening left it. Non-yield parts sit in try/catch: an exception is logged and the step moves on, so `EndOpening` still runs. A flagged station with no once-per-save page logs a warning and is skipped.

Editor tooling, `miso/Assets/_Project/Features/Onboarding/Editor/`:
- `HomeVisitsWiring.cs`: Workshop page text moved to `WorkshopPageText` with item 5's change ("• This is the Workshop. Gear up the pair going out next." / "• Equip each Bergson here before you pick the next mission."). `Run()` also builds the skill tree page. The log line says "station pages".
- `HomeVisitsWiring.SkillTree.cs` (new): `EnsureSkillTreeSequence()` creates `Resources/Tutorials/SkillTree_Tutorial.asset` (title "Skill Tree", item 2's three bullets, same placeholder image as the other pages) and `Resources/Sequences/HomeVisits/SkillTree_FirstOpen_TutorialSequence.asset` (`PlayJustOnce`).
- `OnboardingOpeningSetup.Stations.cs`: the Workshop-only page step (`EditWorkshopTutorial` and its two constants) is removed; `EditStations` calls `EditStationPages` instead.
- `OnboardingOpeningSetup.StationPages.cs` (new): table of rows (Equipments Cabinet → Workshop page, Grandma Table → skill tree page). Sets `tutorialSequence` and `playPageOnUnlock` on each. Messages: "station 'X' shows its page on first open" (unchanged wording, so the existing repair test still matches) and "station 'X' plays its page by itself when it opens". Covered by the drift test `CheckOnTheProject_ReportsNothingToChange`.

Data (made by Wire Home Visits, then Apply Opening Setup: "3 change(s), 0 problem(s)"):
- `Resources/Tutorials/Workshop_Tutorial.asset`: new text.
- `Resources/Tutorials/SkillTree_Tutorial.asset` + `.meta` (new).
- `Resources/Sequences/HomeVisits/SkillTree_FirstOpen_TutorialSequence.asset` + `.meta` (new, guid `df1f13e7346bf034f9a37b54371230a2`).
- `Home - Scene.unity`: scene diff below.

Tests:
- `Onboarding/Editor/HomeStationPageRulesTests.cs` (new, 8 tests): each condition of the rule, scene order with mixed stations, empty or null input, and `HomeInteractables.PageState()` on a real component (flag, unlocked with no missions, a page that can replay doesn't count).
- `Onboarding/Editor/HomeVisitsTests.StationPages.cs` (new partial, 6 tests): both stations have their page and the flag; the skill tree page's title and text (3 bullets); the Workshop page text ("This is the Workshop.", "Bergson", no "hero"); the two pages have different names (the played list goes by name); Apply Opening Setup repairs the Grandma page and both flags in a scratch copy of the scene.

### Scene diff (`Home - Scene.unity`, made by Apply Opening Setup)
- All six `HomeInteractables` get the new field: `playPageOnUnlock: 0` on four, `playPageOnUnlock: 1` on Equipments Cabinet (`&1402771017`) and Grandma Table (`&2034088533`).
- Grandma Table: `tutorialSequence: {fileID: 0}` → `{fileID: 11400000, guid: df1f13e7346bf034f9a37b54371230a2, type: 2}`.
- Nothing else (12 added lines, 1 changed).

## Acceptance criteria

- [x] Flag on `HomeInteractables`, default off; its `tutorialSequence` is the page: code; the default is serialized as 0 on the other four stations.
- [x] Pages play after the completion sequence and the empty InitialTutorial step, before `EndOpening()`, in scene order, with the camera on the station: code. The order and filter are covered by `HomeStationPageRulesTests`. The camera move and the wait for each page need a play check.
- [x] Once per save through `PlayJustOnce` + `PlayedSequencesTracker`, not PlayerPrefs: the auto path calls the same `SequencePlayer.Play` as the click, which marks the page played when it ends. The rule skips a page the tracker already lists, so a page seen by clicking doesn't auto-play. A later click on a page that already played is skipped by `SequencePlayer.Play`, as before. Rule covered by tests; the save round trip is a play check.
- [x] Stations stay blocked until the pages finish: the step runs before `EndOpening()`, inside the existing `OpeningInProgress` window. Play check.
- [x] A page that throws or is missing is logged and skipped, so `EndOpening` still runs: try/catch around selection, focus and `Play`; a missing page never qualifies, and a flagged station without one logs a warning. Limit: an exception *inside* the page's own coroutine can't be caught from here (see Risks).
- [x] Grandma Table page (`TutorialDataSO` + `PlayJustOnce` `TutorialSequence`, item 2's text) made by `HomeVisitsWiring`; the setup sets it and both flags; the drift test covers them: tests pass, Check reports nothing to change.
- [x] Workshop text tweaks (item 5): test.
- [ ] Play check (verifier/THJ): Workshop page plays by itself on the first Home load after River or Ridge, camera on the cabinet; skill tree page on the first load after both; neither replays; clicks work after; nothing plays on loads with no newly open station; `GuidedSkillSpend` still runs on the skill tree's first click; after The Trail the Yard chain plays first (no page is due on that load in the normal order); the Hearth close on the first load is unchanged (no station is open then).

EditMode suite: 1610 tests, 1609 passed. The only failure is the known `AIRegressionTest.Baseline_MatchesCurrentAI`. `GridToLevelSettingsTests.Settings_MissingTemplateIsAnErrorAndWritesNothing` passed this run. The onboarding subset (48 tests, new ones included) was re-run separately: all pass. No compile errors.

## Save reset

No. No save shape changes: the played list only gains asset names. Testing it needs a save from before River/Ridge, or a fresh save.

## Decisions I made

- **Pages need `PlayJustOnce`** (Tier 1): a flagged station whose page can replay is skipped with a warning instead of playing on every load. Without the flag, once per save can't be tracked through the same mechanism as the click.
- **Scene order = hierarchy order** (root objects in order, then depth-first children), found at runtime from `HomeManager`'s scene. No serialized station list, so no extra scene wiring.
- **Camera returns after the pages** (Tier 1, small addition): after the last page the camera eases back to where the opening left it, then the existing `cameraHandler.Initialize()` runs as before. Otherwise Initialize would snap from the last station to the start view. Easy to drop if THJ prefers the snap.
- **Input re-locked before each focus**: a closed page calls `OnPanelClosed` → `StartCameraMovement` (mode All, edge scroller on), which already happens with the Hearth's World map page. Before each focus the step sets mode None and turns the scroller off again, so a player's camera move can't cancel the focus. The existing code then sets mode All before `EndOpening` as before.
- **Focus point** = centre of the station's `Collider2D` (the click area), falling back to its transform.
- **Setup refactor (same behaviour):** the Workshop-only page step became the table-driven `EditStationPages`. The Workshop's existing message wording is kept, so the existing repair test still matches.
- Acceptance follows the brief and D-436 (Workshop page after River or Ridge), not the plan's older "after the Hearth" line.

## Needs THJ

None blocking. Play check as listed above.

## Docs to update

- `tech/home-system.md` (or the onboarding Home notes): station pages on unlock: `HomeInteractables.playPageOnUnlock`, `HomeManager.StationPages.cs`, rule `HomeStationPageRules`, set by Apply Opening Setup's station-page table.
- `tech/classic-fallback.md`: the flag defaults off and only the opening setup sets it, so classic Home is unaffected.
- Plan log: C3 commits.

## Risks and loose ends

- **Camera vs the intro animator (play check):** `Anim_IntroAnimation` animates the parent `Camera Controller` position, the `CameraHandler` enabled flag and the camera's orthographic size. The focus moves the child `CameraHandler` transform, so they shouldn't fight, but whether the cabinet ends up centred depends on the animator state after the intro. If the camera doesn't reach the station, this is the first place to look.
- **An exception inside a page's own coroutine** (e.g. the tutorial panel throws while the page is up) still leaves the opening waiting, the same known limit as the rest of the opening. A timeout would cut off a page the player is still reading, so I didn't add one.
- **Mid-opening input:** between pages and after the last one, closing a page briefly hands the camera to the player before the opening ends (an existing behaviour of `OnPanelClosed`). Clicks stay blocked by `OpeningInProgress`.
- **Old saves:** a save that already has the Workshop open but never clicked it gets the Workshop page on its next Home load. A save where it was clicked gets nothing.
- Between proposed commits 2 and 3 the drift test `CheckOnTheProject_ReportsNothingToChange` fails, because the setup expects the flags that commit 3's data brings. Each commit compiles.
- The class summary of `HomeVisitsWiring` still says "the Workshop's first-open page"; the skill tree page has its own summary in its partial. Left as is.

## Proposed commits

1. `feat(home): a station can play its page by itself the first time Home opens with it unlocked` (risky: every Home load):
   `Features/Home - Imported/___Khashayar/HomeInteractables.cs`, `HomeInteractables.PageOnUnlock.cs` + `.meta`, `HomeStationPageRules.cs` + `.meta`, `HomeManager.cs`, `HomeManager.StationPages.cs` + `.meta`, `Features/Onboarding/Editor/HomeStationPageRulesTests.cs` + `.meta`.
2. `feat(onboarding): opening setup gives the Workshop and the skill tree their pages on unlock` (plain, editor only):
   `Features/Onboarding/Editor/HomeVisitsWiring.cs`, `HomeVisitsWiring.SkillTree.cs` + `.meta`, `OnboardingOpeningSetup.Stations.cs`, `OnboardingOpeningSetup.StationPages.cs` + `.meta`.
3. `feat(onboarding): Workshop and skill tree pages play by themselves when the stations open` (plain, data + tests):
   `Resources/Tutorials/Workshop_Tutorial.asset`, `Resources/Tutorials/SkillTree_Tutorial.asset` + `.meta`, `Resources/Sequences/HomeVisits/SkillTree_FirstOpen_TutorialSequence.asset` + `.meta`, `Features/Home - Imported/___Khashayar/Home - Scene.unity`, `Features/Onboarding/Editor/HomeVisitsTests.StationPages.cs` + `.meta`.

All paths under `miso/Assets/_Project/`. Not staged: `AIFactionBrain.cs`, `AIUnitBrain.cs`, `PreloadScreen.unity`, `ProjectSettings/*` (pre-existing, not mine).

## Other branches

None (onboarding-only data; the runtime flag defaults off).

## How to see it

1. Play from `Scenes/PreloadScreen.unity` with a save that has The Hearth done but neither River nor Ridge (or a fresh save played through The Hearth).
2. Win The River (or The Ridge). Back at Home: after the intro (and any completion lines), the camera eases to the Equipments Cabinet and the "Workshop" page opens ("This is the Workshop. ..."). Close it: the camera eases back, and the stations take clicks.
3. Click the Workshop: the panel opens with no page. Leave Home and come back: no page.
4. Win the other mission. Back at Home: the camera goes to the Grandma Table and the "Skill Tree" page opens. Close it, then click the table: the panel opens on the sister from the mission just played with her node pulsing (guided spend), with no page.
5. Any later load: no station page.
6. Inspector: the Home scene's Equipments Cabinet and Grandma Table show "Play Page On Unlock" ticked. `Tools > Onboarding > Check Opening Setup` reports nothing to change.
