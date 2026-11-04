# Report: Verify Linda memory wiring (L1)

Plan: plans/onboarding/2026-11-04-linda-memory-tuning.md    Agent: miso-verifier    Branch: thj/onboarding
Outcome: partial. Wiring steps pass; the EditMode gate has one unexpected failure.

Result: FAIL (gate) because `HearthMemoryLevelsTests.NothingInTheHearthGivesExperience` is red. Steps 1 to 5 and 7 pass. No play session.

## What changed

- Nothing edited by QA except this report. The tool run modified `GB_m1-linda.prefab` (expected, see below).

## Acceptance criteria

- [x] Compile (step 1): forced refresh and recompile, waited until ready. 0 `error CS` entries; only pre-existing warnings (UtilityScoreGraphView CS0108, AssetOpener CS0618, HelperOverlayPanel CS0414) and serialization depth notices.
- [x] Tool run (step 3): Tools > Onboarding > Wire Memory 1 (Linda). Log: "Memory 1 (Linda) wired: start and end sequences, panels, and the three win stages."
- [x] Prefab diff (step 4): `git diff` vs HEAD is too noisy to compare (it re-orders), so I rebuilt the before-file (HEAD plus the saved before.diff) and diffed it against the file after run 1. Only 78 changed lines (75 added, 3 changed):
  - 4 x `m_IsActive: 0` (4 added lines each, 16 lines) on target 7286543995762015030, the 4 Dark Claws (4 separate prefab instances).
  - New managed references 8881842456907219193 (TurnReachedLOCondition, turn 4), ...194 (LivingUnitsLOCondition, count 0, state 0, comparisonStrategy 3), ...195 (TurnReachedLOCondition, turn 4), each with evaluationMode 0 and factionRef Enemy (59 added lines).
  - 3 changed lines: the objective condition refs repointed from 8881...035, 8046...280, 8881...035 to ...193, ...194, ...195.
  - No other value changed (no texts, turn, tile, sequence ref, flags, LSB, cells, units).
- [x] Idempotence (step 5): second run, prefab file byte-identical to after run 1 (`cmp`), and `git diff` output byte-identical.
- [ ] Tests (step 6): 1310 run, 1308 passed, 2 failed.
  - `AIRegressionTest.Baseline_MatchesCurrentAI`: known red.
  - `MISO.Core.Features.Onboarding.EditorTests.HearthMemoryLevelsTests.NothingInTheHearthGivesExperience`: FAIL. Message: the four `Unit_DarkClaw` on `GB_m1-linda` at cells (6,7), (7,8), (8,7), (7,6) each have `lethalDamageXpBonus = 3`; expected none. The prefab data carries this; it is not in the tool's diff (the tool did not touch the value), so it comes from THJ's rework or the base DarkClaw prefab. Not confirmed whether it was red before the run.
  - All 8 `HearthMemoryLindaTests` pass (re-run alone), including the 5 new ones: ThreeStagesInAQueue, TheFirstAndLastStagesWantAllEnemiesDead, TheSecondStageWantsLindaOnTheGatherTileThenPlaysTheInterruption, TheConditionsAreNotSharedBetweenObjectives, TheHiddenClawsAreSwitchedOffInThePrefab.
- [x] Console (step 7): no warnings from HiddenLevelUnits or the wiring.

## Save reset

no

## Decisions I made

- Rebuilt the before-state from HEAD plus the saved diff, because comparing two `git diff` outputs showed large phantom differences that the file-level diff does not have.

## Needs THJ

- `NothingInTheHearthGivesExperience` fails on the 4 claws' `lethalDamageXpBonus = 3`. Decide whether the claws should lose the bonus (prefab or test rule). I did not touch it.

## Docs to update

- none

## Risks and loose ends

- The test run in the open editor drops the MCP connection a couple of times; polling again works.
- Editor checks corrections: none.

## Proposed commits

none (QA)

## Other branches

none

## How to see it

1. Test Runner > EditMode > HearthMemoryLevelsTests.NothingInTheHearthGivesExperience to see the failure message.
