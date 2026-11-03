# Report: HomeVisits scratch-scene test flaky log

Plan: none (S-size task from coordinator)    Agent: implementer    Branch: thj/onboarding
Outcome: done

## What changed

- miso/Assets/_Project/Features/Onboarding/Editor/HomeVisitsTests.cs: new helper `WithoutSceneCopyLogFailures` (suspends `LogAssert.ignoreFailingMessages` around one Unity call, restores it in `finally`). It wraps `AssetDatabase.CopyAsset(HomeScenePath, ScratchScene)` and `EditorSceneManager.SaveScene(scene)`. The comment says why. The builder's `RunHomeSceneOnly` Check and Apply calls stay outside it. LF endings kept (file was LF, ASCII).

## Where the log came from (evidence)

Editor.log (`%LOCALAPPDATA%/Unity/Editor/Editor.log`) holds several "Unsupported type Vector2f" entries with stack traces from the earlier runs:
- `EditorSceneManager.SaveScene` called from the test (the case the old ignore covered).
- `AssetDatabase.CopyAsset` called from `HomeVisitsTests.ApplyOpeningSetup_RepairsAStationLockInACopyOfTheScene` at line 191 (twice). This one was NOT covered, so it failed the test when it appeared.

Unity logs it when it imports or serializes the copy of the Home scene, and not on every run. A single run alone showed no log in the console. No entry came from opening the scene or from the builder's Apply.

## Acceptance criteria

- [x] Ignore widened to exactly the copy and save steps, Check/Apply outside: see the diff.
- [x] Full EditMode suite passes except the known red test: run 1 was 1291 total, 1290 passed, 1 failed; run 2 was 1291 total, 1290 passed, 1 failed. Both failures were `AIRegressionTest.Baseline_MatchesCurrentAI` (not touched).
- [x] `git status` shows no new changes: only HomeVisitsTests.cs is new. The other modified files (Greybox prefabs, AI brain files, HearthMemory tests, PreloadScreen, ProjectSettings) were already modified at session start. Home scene and GameData are untouched, and no scratch scene is left.
- Caveat: the log is intermittent, so two green runs show nothing regressed but cannot prove it can never appear again. The cause is covered from the log evidence.

## Save reset

no

## Decisions I made

- Used a small generic helper instead of repeating the try/finally twice. Same behavior as the plan asked for.

## Needs THJ

none

## Docs to update

- none

## Risks and loose ends

- If the Home scene serializer log also fires from the builder's Apply save in some run, that would still fail the test. It was never seen in the log; I left it outside on purpose.
- The test takes about 20 s alone (scene copy and import).

## Proposed commits

1. `test(onboarding): ignore the Unity scene-copy log in the HomeVisits station-repair test` : miso/Assets/_Project/Features/Onboarding/Editor/HomeVisitsTests.cs (plain)

## Other branches

none

## How to see it

1. Test Runner > EditMode > run `HomeVisitsTests`, or Run All; only `AIRegressionTest.Baseline_MatchesCurrentAI` should be red.
