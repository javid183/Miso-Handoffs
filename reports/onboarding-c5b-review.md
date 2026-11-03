# Review: onboarding C5b (Home visits as data)

Reviewer: `miso-reviewer` (read-only; saved by the coordinator) · 2026-11-02 · Branch `thj/onboarding`

**Verdict: FIX** (one must-fix in test code; data, scene and builder correct)

## Must fix

1. `HomeVisitsTests.cs` ~215-225 `RepairAStationLockInACopyOfTheScene`: redirects only the Home scene, then runs `OnboardingOpeningSetup.Run(targets, apply: true)`, which also applies the graph (GameData), initial-mission scene and recruit-prefab steps to the real project files. When the project has drifted (e.g. after a home-test merge), running the suite would silently rewrite shared files and, by test order, hide the drift `CheckOnTheProject_ReportsNothingToChange` should catch. Fix: run only the scene/station step on the copy, or redirect every target to scratch, or `Assert.Inconclusive` when the `apply: false` pass reports any non-"Home scene" change/PROBLEM.

## Should fix

1. `HomeVisitsTests.cs:205-209`: `LogAssert.ignoreFailingMessages = true` hides every error; expect only the "Unsupported type Vector2f" message (regex), after confirming its log type.
2. The drift proof doesn't break the `oneUnlockedMissionCompletionIsEnough` flag (e.g. Grandma Table) or the Workshop `tutorialSequence` (null); add both breaks and their asserts.
3. `OnboardingOpeningSetup.Stations.cs` is CRLF; sibling partials are LF. Save as LF.
4. Commit order: data → scene → builder + tests, so no intermediate commit is red.

## Notes

- Clue scene `PlayJustOnce: 0` (coordinator D-365 wants 1): set it in `HomeVisitsWiring.EnsureClueScene`, re-run Wire Home Visits, assert it. A skipped sequence still calls `onComplete`, so the info panel opens (`WorldMapPanelUI.cs:86-93`).
- Builder idempotent; missing station name reported; duplicates caught by tests (`Station()` asserts one match). 6 `HomeInteractables` in the scene (5 changed + Fireplace). Family entry found by `isFamilyAbilitiesBtn`.
- GUIDs checked: Workshop River+Ridge any=1, tutorial `Workshop_FirstOpen_TutorialSequence` PlayJustOnce 1; Grandma Table River+Ridge any=0; Bookshelf/Training Field/Cooking Cabinet M4; Family tab Trail.
- HomeState: furthest = deepest mission node, later completion wins ties; all four missions share Searching, so it shows in either order until M4.
- Assets Unity-shaped; dialogue lines match V2-3..V2-7, Y12-1..Y12-4. Mission diffs 1–3 lines each. Scene diff: 5 station blocks, Family override, 9 known `GlobalEventBus` empty fields.
- No private IDs, no core code, no runtime statics.

## Fix round 1 re-review (2026-11-02): FIX (one small item)

Must fix: the single `LogAssert.Expect(... "Unsupported type Vector2f")` fails if Unity logs it 0 or 2 times. Instead, set `LogAssert.ignoreFailingMessages = true` only around the test's own `SaveScene` call (restore in `finally`) and drop the `Expect`; builder Check/Apply errors still fail the test.

Checked OK: `RunHomeSceneOnly` runs only `RunHomeSceneStep` on the redirected scene (no graph, GameData, initial-mission or recruit steps; skips Preflight and the Play guard, fine for an internal test-only entry, don't wire it to a menu). `Run`/`ApplyMenu`/`CheckMenu` unchanged; the only pre-existing file change is one `EditStations` line in `.Scenes.cs`. LF normalisation touched no pre-existing file. Drift test breaks four edits and asserts each; clue scene `PlayJustOnce: 1` asserted.

## Fix round 2 (2026-11-02): APPROVE (coordinator check)

`HomeVisitsTests.cs:215-218`: `ignoreFailingMessages` saved, set only around the test's own `SaveScene`, restored in `finally`; `Expect` removed. Matches the reviewer's fix exactly; EditMode 1288/1289 known red only.
