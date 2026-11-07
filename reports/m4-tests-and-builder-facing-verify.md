# Report: Verify m4 tests and builder facing (full EditMode run)

Plan: plans/m4-tests-and-builder-facing.md    Agent: miso-verifier    Branch: thj/onboarding
Outcome: done

Result: PASS (only the accepted red).

## What changed

- Nothing. Quiet checks only, no Play mode, no edits, read-only git.

## Acceptance criteria

- [x] Console clean: `read_console` errors returned 0 entries; editor not compiling.
- [x] Not in Play mode: `EditorApplication.isPlaying` false; PreloadScreen open.
- [x] Full EditMode suite: 1463 run, 1462 passed, 1 failed, 0 skipped (197 s, Unity MCP `run_tests`).
- [x] Only failure is `MISO.Core.Systems.AI.EditorTests.AIRegressionTest.Baseline_MatchesCurrentAI` (AI regression report: 713 checks, 42 failures; known red, not touched).
- [x] The Mark tests and the new `GridToLevelFacingTests` all passed (no other failure).
- [x] `Content/Levels/Greybox/__CameraStartTest` does not exist after the run (the folder holds only `GB_*` prefabs and `GridLevelPalette.asset`).
- [x] New untracked files in `git status --short -- miso/Assets`: only the four expected, `GridToLevelBuilder.Facing.cs(.meta)` and `GridToLevelFacingTests.cs(.meta)`, all under `Core/Levels/Editor/GridToLevel/`. Nothing else new.

## Save reset

no

## Decisions I made

- none

## Needs THJ

none

## Docs to update

- `tech/editor-checks.md`: the full suite on thj/onboarding is 1463 tests and about 197 s through the Unity MCP. The first `get_test_job` wait dropped once ("plugin session disconnected") and one wait timed out. Calling it again worked. Filtering the finished job with `include_failed_tests` gives the failure's name and output in a large file (read with python; jq is not installed).

## Risks and loose ends

- Modified-but-uncommitted files in the status are the ones listed in the plan report, plus `LiberationSans SDF - Fallback.asset` and `PreloadScreen.unity` (Unity noise, not from this change). `ProjectSettings` changes sit outside `miso/Assets` and were not checked.

## Proposed commits

none (verification only)

## Other branches

none

## How to see it

1. Test Runner > EditMode > Run All; expect 1462 green and `Baseline_MatchesCurrentAI` red.
