# Verify: merge of thj/cyclone into main (049897aae)

Branch: main    Agent: miso-verifier    Editor closed, Unity 6000.3.4f1 batch
Result: FAIL (1 test)

## Compile
Clean: 0 `error CS` in test-main.log and test-ai.log.

## Tests
- Full EditMode: 2431 total, 2429 passed, 1 failed, 1 skipped (the Explicit AI baseline).
- Failure: MISO.Core.Features.Bergsons.EditorTests.CycloneSteerTests.LiveSteer_CostsOneAP_HasNoCooldown_FirstIsNotFree_AndIsSeparateFromTheCast
  Message: "no cooldown: any number of Steers a turn. Expected: 0.0f But was: 1.0f"
  at CycloneSteerTests.cs:386 (asserts steer.GetParameters(0).coolDownV.rawValue == 0).
  The asset Lucy_Ability_Steer.asset on main has coolDownV.constantValue: 1; CycloneSteerSetup.SteerCooldown = 0 (so the test and setup tool agree, the asset differs). Last touched by 13e8bab62.
- AIRegressionTest.Baseline_MatchesCurrentAI (run by full name): CHECKS: 714, FAILURES: 43. Same as the last recorded 43; gate not failed by it.

## Bugs found
Steer asset cooldown is 1, but the design (and test) says 0. Either the asset was not re-run through the setup tool or the test is stale. Not investigated further (read-only).

## Save reset
no

## Editor checks corrections
none (command-line route worked; full suite took about 170 s including import after the branch switch).
