# Report: Verify Cyclone round 2, C1 (quiet checks only)

Plan: plans/2026-11-17-cyclone-round2-tech.md (chunk C1)    Agent: miso-verifier    Branch: thj/cyclone (uncommitted change)
Outcome: done (quiet checks only; no play session, so play checks not run)

Result: PARTIAL (all quiet checks pass; play-only criteria not run)

## Checked

- Compile: forced script recompile through the Unity MCP, refresh finished idle. Console (errors and warnings) shows no CS compile errors and nothing from the Cyclone files. Only noise: a MCP WebSocket receive warning and the usual "Serialization depth limit 10" warnings (StatBackedValueBase.factorReadMode, GTag.subTags), none in Cyclone code.
- Full EditMode suite via the MCP Test Runner: 2030 run, 2029 passed, 1 failed, 0 skipped reported.
- Cyclone tests: filtered run of CycloneSteerTests, CycloneWhirlTests, CycloneHowlingGaleTests, MasherCounterWhirlTests (namespace `MISO.Core.Features.Bergsons.EditorTests`): 56 run, 56 passed. This covers the new `CyclonePower_HitIsThreeFourFiveTimesDamage` and `SteerAction_StaysOpenThroughTheGlideAndThePullOnly` cases, which are inside CycloneSteerTests.
- `Lucy_Cyclone_Ability.asset`: loads in the editor (manage_asset get_info returns AbilityPreset, no console errors). Stat_DMG upgradeLevels factors in the file are 1, 1.333333, 1.666667 (lines 144 to 152), with MainResource_SP amount 1 on levels 2 and 3.

## Not checked

- Play checks (Steer glide, swell, pull, hit, damage numbers; combat log line "Whirl · Lucy: carried 0, pulled N, hit M"; Masher not countering a Steer hit; Howling Gale Weak on Steer hits; real Cyclone Power damage 3 / 4 / 5 on a live Lucy). Not run: needs a play session (THJ has not agreed one).
- The Cyclone Power test is a formula check (stat step plus rounding), not the full ability runtime, per the implementer report.
- "No Gust left" grep was not repeated.

## Failures

- `MISO.Core.Systems.AI.EditorTests.AIRegressionTest.Baseline_MatchesCurrentAI`: the known red. Inner report: `RESULT: FAIL CHECKS: 714 FAILURES: 43`. Same 43 as before C1. Does not fail the gate.
- No other failures.

## Counts

- Full EditMode: total 2030, passed 2029, failed 1 (the known red).
- Cyclone and Masher subset: 56 / 56 passed.
- AIRegression inner failures: 43 (expected 43).

## Save reset

no

## Bugs found

none

## Editor checks corrections

- The MCP `get_test_job` returns the full failure message of the AIRegression test (about 60k characters) on every poll once it has failed, and ignores `wait_timeout` after that, so the call overflows the tool output and is saved to a file. Read failure counts from the saved file with Python (`jq` is not installed in the Git Bash here). A poll with `include_failed_tests` false does not avoid it.
- A full suite run in the background (editor unfocused) took about 8 minutes and the MCP session dropped once mid-run; the job kept going and was readable afterwards.
- `run_tests` `test_names` takes full class names with namespace; a wrong namespace silently runs 0 tests with "Passed".

## Docs to update

- none from this run

## Risks and loose ends

- Play check of the Steer Whirl, Masher and Howling Gale paths still open until THJ agrees a session.
