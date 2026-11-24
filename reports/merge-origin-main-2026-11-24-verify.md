# Report: Baseline check after merge of origin/main (5a47ca5e0)

Plan: none (baseline check)    Agent: miso-verifier    Branch: thj/onboarding-demo
Outcome: partial (compile clean, 8 test failures, all in one fixture, none from the merge)

## What changed

Nothing. Quiet checks only; no Play mode, no files under miso/ touched.

## Compile

Clean. Forced refresh plus compile request through the Unity MCP; Editor.log has 0 `error CS` lines. `CompileScripts` showed 3 ms, so the editor had already compiled the merged scripts before my refresh (the domain reload itself took about 16 s).

Console (errors and warnings, with stacks): 0 errors. 12 warnings, all one kind: "Serialization depth limit 10 exceeded at StatBackedValueBase.factorReadMode" (cycle through RuntimeAbility._owner / AbilityOrchestrator.abilities), reported for GUnit.abilityOrchestrator, MarkPassiveAbility_ContinuousAttack, JohnPassiveAbility_CommandShieldDash, LindaQuiver, LucyPassiveAbility_PapasShelter, UnitsPassByHandler, UnitsCooperationHandler, PlayerController, RunUpgradeSO.relicItem, DivineRelicPickUp, CycloneEntity, FactionRoleHandlerBase. Console stack traces are empty for these. They come from ability and stat classes this merge did not touch (no ability or stat code in `dcd13167f` / `201df2400`); I did not check them against an earlier session, so "pre-existing" is a judgment, not a measurement.

## Tests

Full EditMode suite through the Unity MCP (job d60e3c23...): **2605 total, 2596 passed, 8 failed, 1 skipped** (the Explicit `AIRegressionTest.Baseline_MatchesCurrentAI`, not run). Duration 434 s. Last known was 2604/2605 with 1 skipped, so 8 new failures.

Failures, all in `MISO.Core.Features.Onboarding.EditorTests.M1RidgeTests`:

| Test | Message |
| --- | --- |
| ClawsAndTheMasherCarryTheirHealthFactors | Unit_DarkClaw on (2, 2): expected 0.8 +/- 0.0001, was 1.0 |
| FourStagesRunThePackTheMasherWithTheLateClawsAndTheRest | expected equivalent to (0,4),(2,4),(1,3); was (5,-1),(5,2),(7,-2) |
| TheBackPairStartsHidden | NullReferenceException |
| TheClueLiesAtTheCorridorsEndAndTheEndClosesInOnIt | InvalidOperationException: Sequence contains no matching element |
| TheLevelIsTheRidgeAtEarlyTierWithEveryEnemyAlert | expected True, was False |
| TheMashersOnlyNeighboursAreBesideItInTheCorridor | expected (4,0),(7,0); was (5,-1),(7,0),(4,1),(5,2),(6,2) |
| ThePairAndTheEnemiesStandOnTheirTiles | index 0: expected (1,0), was (4,-5) |
| TheRoomLedgeAlcoveAndCorridorAreTheGridsCells | expected 38 cells, was 50 |

Predates the merge: yes. The tests (added in `3bf3e14ba`, untouched since) pin tile coordinates, cell count (38) and enemy setup of `GB_m1-ridge.prefab`. THJ's own `f20f9a5ab` "m1 ridge level" (before the merge) rewrote that prefab (1528 insertions, 623 deletions); the actual coordinates (50 cells, tiles out to (7,-2)) show a re-laid-out level. The merge touched none of `GB_m1-ridge.prefab` or `M1RidgeTests.cs` (`git log` on `Features/Onboarding` lists only `f20f9a5ab` and `3bf3e14ba`). Nothing was run between that commit and now, so the suite was first red here. The tests need updating to the new layout, or the layout is not what THJ intended; that is his call. I did not fix or re-baseline anything.

GridToLevel lock flake (D-599): did not occur, no rerun needed. Every non-Ridge fixture passed, including those covering Khash's `GridCell` change.

## Acceptance criteria

- [x] Compile clean: 0 `error CS`, 0 console errors.
- [ ] Full EditMode suite green: 8 failures (all M1RidgeTests, from `f20f9a5ab`).

## Save reset

no

## Needs THJ

Is the new `GB_m1-ridge` layout (from `f20f9a5ab`) final? If yes, `M1RidgeTests` needs rewriting to the new tiles, cell count (50), enemy positions and health factors. If not, the prefab needs fixing. The Phase 1 chunks that touch the Ridge should wait on this.

## Risks and loose ends

- `TheBackPairStartsHidden` (NullReferenceException) and `TheClueLiesAtTheCorridorsEndAndTheEndClosesInOnIt` (no matching element) fail on object lookup, so the new prefab may have renamed or removed objects, not only moved them. A gameplay check of the Ridge would show whether the level still works.
- Editor checks corrections: `get_test_job` with `wait_timeout` dropped the session ("disconnected while awaiting command_result") five times and TimeoutError once during the run, matching the existing note. The run finished after about 7.5 min (434 s of tests) and the sixth poll returned the full result. The TestResults.xml on disk was stale (Nov 23) until the run completed, so don't read it mid-run. No line of `tech/editor-checks.md` was wrong.
