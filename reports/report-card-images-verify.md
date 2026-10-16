# Verify report: Report-card context images

Plan: plans/2026-10-16-report-card-images.md    Agent: miso-verifier (saved by the coordinator; the verifier's Write was refused)    Branch: thj/home-test
Result: PASS. Compile and tests pass; THJ play-checked it and it worked.

## How it was run

The editor was not open during the verifier run (`miso\Temp` absent, no Unity.exe, Editor.log ends in a clean shutdown), so the command-line route was used.

## Compile and tests

- Compile: clean (`CompileScripts: 15794ms`, no `error CS`).
- Tests: 447 run, 446 passed, 1 failed: the known red `AIRegressionTest.Baseline_MatchesCurrentAI`.
- New `HeadlineContext_*` tests, 4 of 4 passed: `MapsKindsToDefinitionSources`, `BondLevelSkillPointAndNone_ShowNoImage`, `EveryKind_KeepsItsRefIdThroughBuild`, `WeaponRefId_ResolvesToWorkshopItemWithReachableIcon`.
- Existing tests all passed: 9 `Headlines_*`, `SkillPoints_Headline_ComesBeforeTheHouseAndTheKitchenNews`, `Report_SurvivesTheSaveFile_WithItsHeadlines`, `KnowledgeState_RoundTripsThroughSave`.

## Acceptance criteria

- Pass: Bond level and Skill point cards unchanged (kinds map to None, covered by a test).
- Pass: no new fields in `HomeReportEntry`, `HomeDayReport` or `HomeSaveData`; persistence tests pass.
- Pass: pure helper with 4 EditMode tests.
- Pass: compile and suite green apart from the known red. The live editor Console was not inspected by the verifier.
- Pass by code reading: null icon or failed lookup shows nothing.
- Pass by THJ's Play check (2026-10-16, "it worked"): Workshop item card icon, the other card kinds' icons, no stale or doubled images on Next. THJ did not list per-check detail; the null-icon case was not reported separately.

## Bugs found

None.

## Corrections to `tech/editor-checks.md` (D-031)

- "Is the editor open?" rule is fine; add a second check: `tasklist | grep -i unity` and the end of Editor.log. (`miso\Temp` was present when the coordinator checked, then absent at the verifier run, and no Unity process was running.)
- Command-line route worked as written. Exit code 2 was only the known red test. The run took 63 s for 447 tests, including about 16 s of compile. The file's 60 to 80 s figure is for an in-editor reload, a different thing.
- Editor.log path, `CompileScripts` / `error CS` patterns and the NUnit XML reading: confirmed.
- Unconfirmed (not used): Ctrl+R, the Test Runner window and its results file, Auto Refresh, computer use in the desktop app.
- Side effect: Unity created `.meta` files for the two new untracked files, as expected.
