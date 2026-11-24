# Report: Phase 1 leftovers, full-suite gate (1.9 Whirl on passed enemies, 1.7 Mark avatar, X-25 family tree auto-open)

Plan: plans/ (see reports onboarding-1-9-whirl-passed, onboarding-1-7-mark-avatar, onboarding-x25-family-tree-open)    Agent: miso-verifier    Branch: thj/onboarding-demo
Outcome: done

**Result: PASS** (quiet checks only; no Play mode, no files under miso/ touched, read-only git)

## Compile

- Forced refresh + compile through the Unity MCP. Editor.log: 0 `error CS` lines; compile and domain reload finished.
- Console errors: none. Console warnings: only the usual C# compiler warnings (CS0108, CS0114, CS0168, CS0414, CS8509, CS8524, CS0067) in existing files; none in the changed Cyclone, Onboarding, HomeManager or AbilityUpgradePanelUI files.
- Editor.log shows the known "Serialization depth limit 10 exceeded at StatBackedValueBase.factorReadMode" warnings (4 seen after the last reload; 12 across the session per this morning's note). No new warning types.

## Tests

Unity MCP `run_tests`, EditMode, whole suite, 385 s.

- Total 2622, passed 2613, failed 8, skipped 1 (the Explicit `AIRegressionTest.Baseline_MatchesCurrentAI`).
- Versus this morning (2605 / 2596 / 8 / 1): +17 total, +17 passed, failures unchanged. The new Cyclone and X-25 tests are all among the passes.
- Failures, all expected red (`M1RidgeTests`, per THJ):
  - ClawsAndTheMasherCarryTheirHealthFactors
  - FourStagesRunThePackTheMasherWithTheLateClawsAndTheRest
  - TheBackPairStartsHidden
  - TheClueLiesAtTheCorridorsEndAndTheEndClosesInOnIt
  - TheLevelIsTheRidgeAtEarlyTierWithEveryEnemyAlert
  - TheMashersOnlyNeighboursAreBesideItInTheCorridor
  - ThePairAndTheEnemiesStandOnTheirTiles
  - TheRoomLedgeAlcoveAndCorridorAreTheGridsCells
- New failures: none. GridToLevel flake: did not occur, no rerun needed.
- AI regression test: not run (no AI graph, ability or prefab change).

## Acceptance criteria

- [x] Full EditMode suite green apart from the 8 expected `M1RidgeTests`: 2613 passed, 8 failed (all M1Ridge).
- [x] Compile clean: no errors.
- Play-only criteria of the three chunks: Not run (no play session agreed).

## Save reset

no

## Editor checks corrections

- The MCP `get_test_job` disconnected or timed out several times during the 385 s full run (domain reload between fixtures); retrying with `wait_timeout` 45-60 s worked each time, and the final result came through `result.summary`. Matches the existing note.
- `TestResults.xml` was not updated by this MCP run (still 10:46 timestamp at 11:25), so for the MCP route the counts come from `get_test_job`, not the file.
- Writing `sleep N` in Bash is blocked for N around 90; short sleeps worked.
