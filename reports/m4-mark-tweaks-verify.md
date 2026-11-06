# Report: m4-mark-tweaks verify (compile and EditMode suite)

Plan: none (pre-commit check)    Agent: miso-verifier    Branch: thj/onboarding
Outcome: partial (no play checks, by request)

## Result

PASS on the gate under THJ's decision D-405: every failure is in `HearthMemoryMarkTests` or is the known `AIRegressionTest` red. No unexpected failures.

## Compile

Clean. Compile requested via the Unity MCP; `read_console` errors: 0 entries. Only warnings (serialization depth limit on `StatBackedValueBase.factorReadMode`, existing noise). The editor was not in Play mode (a test run started, which needs Edit mode); Editor.log shows no compile errors.

## Tests (EditMode, Test Runner via MCP)

1410 run, 1399 passed, 11 failed, 0 skipped (171 s).

Expected reds (11):
- `MISO.Core.Systems.AI.EditorTests.AIRegressionTest.Baseline_MatchesCurrentAI`: RESULT: FAIL, 713 checks, 42 failures (known).
- `HearthMemoryMarkTests` (namespace `MISO.Core.Features.Onboarding.EditorTests`), 10 tests, first assertion line:
  - `EveryClawStandsOnItsTileWithItsHealthAndHiddenState`: "no Claw outside the layout" Expected 13 but was 15
  - `StageThreeWinsWhenAllFiveClawsByTheMotherAreDead`: Expected "Save the cub." but was "Kill the dark claws near the cub."
  - `StageTwoEndsWithJohnOnTheDenMouthAndPlaysTheHold`: Expected "John: hold the den mouth." but was "John: Cut the reinforcement path."
  - `TheArrivalAndTopGroupsHoldTheirClawsSwitchedOff`: Expected 2 but was 3
  - `TheArrivalBoastsRunsLucyAheadRevealsMarksClawsAndResetsTheTurn`: step indexes ordered and >= 0, but was < 0, 2, -1, 4, 5, 6, 7, 8, 9 >
  - `TheBloomCutInPlaysWhenTheLevelStartsAndLucyCastsOnTheCrossing`: step indexes ordered and >= 0, but was < 0, -1, 2, 3, 6, 7 >
  - `TheEndingDropsTheMotherWalksLucyThenMarkToTheCubAndFadesToTheHearth`: Expected (7, 9) but was (7, 8)
  - `TheFourHeroesStartOnTheirTilesAndInPlay`: Unit_John Expected (9, 5) but was (4, 2)
  - `ThereAreThreeQueuedStages`: "stage 3 also ends at its cap" Expected 1 but was 0
  - `TheScriptedTilesExistAndNobodyStartsOnThem`: InvalidOperationException: Grid cell missing in the level: GridCell - (7, 9)

Unexpected failures outside those two classes: none.

## Acceptance criteria

- [x] Compile clean: no `error CS`, console errors 0.
- [x] Full EditMode suite run: counts above.
- [x] `HearthMemoryLevelsTests.NothingInTheHearthGivesExperience` passes: not in the failure list of a full run with 0 skipped (inferred from absence; the job returns only failures).
- [x] All 10 `MoveUnitSequenceTests` pass: none in the failure list (the file has 10 `[Test]`; same inference).
- Not run: play checks (not requested).

## Save reset

no

## Decisions I made

- Treated the failures in `HearthMemoryMarkTests` as expected per D-405; did not fix or re-baseline anything.

## Needs THJ

none. Note for the follow-up: `TheArrivalBoasts...` and `TheBloomCutIn...` show negative step indexes (steps no longer found, -1), so those tests need the new camera step and sequence names, not only coordinates. The `TheFourHeroes...` John start (4, 2) and `ThereAreThreeQueuedStages` (stage 3 cap) also differ.

## Docs to update

- `tech/editor-checks.md`: with the MCP, `get_test_job` for the full suite (1410 tests on thj/onboarding) takes about 170 s, times out on `wait_timeout` 90 and needs a retry; the final result lists only failures (passed tests are not listed), so "test X passed" is inferred from absence. `jq` is not installed; use `python -I`.

## Risks and loose ends

- Editor state: left as found (Edit mode, nothing saved or opened).

## Proposed commits

none (QA does not commit)

## Other branches

none

## How to see it

1. Window > General > Test Runner > EditMode > Run All.
