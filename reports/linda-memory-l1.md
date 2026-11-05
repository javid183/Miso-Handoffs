# Report: Linda memory wiring follows the reworked level (L1)

Plan: plans/onboarding/2026-11-04-linda-memory-tuning.md    Agent: miso-implementer    Branch: thj/onboarding
Outcome: done (code and tests only; prefab not touched, tests not run)

## What changed

- `miso/Assets/_Project/Features/Onboarding/Editor/HearthMemoryWiring.Linda.cs`: `WireLevel` now calls new `WireStages` + `HideTheHiddenClaws` instead of forcing one stage. `TurnCap` 2 -> 4. New consts: `InterruptionSequencePath`, `HiddenGroupId` ("hidden"), `LindaUnitName`, `GatherTile` (2,7).
  - queue on, 3 groups, all `Any`. Stage 1: enemies dead (visible, "Eliminate all enemies. {alive_0} remaining.") + turn cap 4 (hidden). Stage 2: "Gather your arrows." (visible; `UnitTileOccupiedLOCondition`, `Unit_Linda`, tile `GridCell - (2, 7)`) + turn cap (hidden), `onCompleteSequence` = existing `Memory1Linda_Interruption_SequentialSequence` asset (loaded, not regenerated; throws if missing). Stage 3: enemies dead + turn cap, both visible, no onComplete.
  - Reuses Lucy's `SetObjectives`/`Claim<T>`/`Living`/`Turns`, so every objective gets its own condition instance (a condition already used earlier in the same run is replaced by a fresh one). Re-running on a correct prefab keeps its instances.
  - `HideTheHiddenClaws`: the wiring did not touch units before; it now `SetActive(false)` on the units of `HiddenLevelUnits` group "hidden".
  - Values taken from the prefab diff (texts, visibility, turn 4, `Enemy` faction on all conditions). Not changed: End vs Reset on the "reset" call, `allEnemiesStartAlert`, turn cap on every stage, outro text.
- `.../HearthMemoryLindaTests.cs`: `WinningNeedsAllEnemiesDeadOrTheTurnCap` replaced by `ThreeStagesInAQueue`, `TheFirstAndLastStagesWantAllEnemiesDead`, `TheSecondStageWantsLindaOnTheGatherTileThenPlaysTheInterruption`, `TheConditionsAreNotSharedBetweenObjectives`, `TheHiddenClawsAreSwitchedOffInThePrefab`.

Line endings: both files LF, no BOM, unchanged. Nothing outside `Features/Onboarding/Editor/`.

## Acceptance criteria

- [x] Wiring reproduces the 3-stage design: covered by the tests above (after the tool run).
- [x] Unique condition per objective: `TheConditionsAreNotSharedBetweenObjectives` (6 distinct ids).
- [x] Hidden claws inactive: `TheHiddenClawsAreSwitchedOffInThePrefab`.
- [ ] Idempotence: by construction (Claim reuses a matching unused instance); not run. Verifier: run the tool twice, `git diff` the prefab after the second run should be empty.
- [ ] Compiles: `read_console` showed 0 errors, but I could not confirm a recompile happened after my edits. Treat as unverified.

## Save reset

no

## Decisions I made

- Group objectives use the Lucy helpers' defaults (objective aggregation All, evaluationMode 0, playersConcern off), which match THJ's values.
- Stage 1 (index 0) objective 0 text is set explicitly to the template's text so it does not depend on the base prefab.

## Needs THJ

none

## Docs to update

- none

## Risks and loose ends

- Expected to fail until the tool is run (current prefab): `ThreeStagesInAQueue` is likely fine on his prefab except the shared ids; definitely failing: `TheConditionsAreNotSharedBetweenObjectives` (shared rids 8881...035 x3 and 8046...280 x2) and `TheHiddenClawsAreSwitchedOffInThePrefab` (claws active). The others (`ThreeStagesInAQueue`, `TheFirstAndLastStagesWantAllEnemiesDead`, `TheSecondStage...`) should already pass against his prefab; all five pass after the run.
- Run order matters: THJ must save and close the prefab first, or the tool and the open prefab stage will overwrite each other.
- The tool also rewrites start/end sequences and panels as before (content unchanged by this task).
- The tool saves the prefab via `SaveAsPrefabAsset`; expect the diff to also re-serialize THJ's other overrides unchanged. Check `git diff` for anything beyond: new rids for the duplicated conditions, `m_IsActive: 0` on 4 claws.
- Can't reproduce: nothing found in the objectives/claws; grid cells, unit placement, hidden group, the "reset" LSB call and the alert flag are left as he made them.
- Unrelated findings from the review (outro "Three Claws", chain-completing at turn 4, End vs Reset) remain open.

## Proposed commits

1. `fix(onboarding): Linda memory wiring builds the three-stage level with unique conditions and hidden claws`: `HearthMemoryWiring.Linda.cs`, `HearthMemoryLindaTests.cs` (plain). Commit before or with THJ's prefab/asset commit; the tests only pass once the prefab has been re-wired.

## Other branches

none

## How to see it

1. In Unity: save and close the `GB_m1-linda` prefab stage (and any scene that has it open).
2. Wait for recompile; check the console is clean.
3. Tools > Onboarding > Wire Memory 1 (Linda). Console: "Memory 1 (Linda) wired".
4. Run it a second time; `git diff` on `GB_m1-linda.prefab` should not change from the first run.
5. Test Runner > EditMode > `HearthMemoryLindaTests`: all pass.
6. Inspect the prefab: Level > Objectives shows 3 stages, each condition separately editable; the four claws under HiddenLevelUnits are greyed out (inactive).

## Review fixes

- Class summary and log line now say "three win stages"; the duplicate "level wiring" section header is removed.
- Linda unit and gather tile lookups use `FirstOrDefault` and throw an `InvalidOperationException` naming what is missing.
- Tests read conditions through a `Condition<T>` helper that asserts the type first, so a wrong type fails an assert instead of throwing a cast exception. Still uncompiled/unrun.

## Follow-up: hidden claws give no XP

- Cause: the 4 claws THJ added to the "hidden" group kept the enemy prefab's `lethalDamageXpBonus = 3`; the three original claws had a `0` override from the grid tool's `xp none`.
- Change: `HideTheHiddenClaws` in `Features/Onboarding/Editor/HearthMemoryWiring.Linda.cs` now also zeroes `LevelXpChecker.UnitXpFields` (`abilityDamageXpReward`, `lethalDamageXpBonus`) on each hidden-group unit through a SerializedObject, only writing when the value is not already 0 (idempotent). Added `using MISO.Core.Levels.CEditor;`. Log line now mentions the hidden claws. LF, no BOM kept.
- Ran Tools > Onboarding > Wire Memory 1 (Linda) in the open editor (0 compile errors). Prefab diff vs before: exactly 4 new `lethalDamageXpBonus: 0` overrides (target unit fileID 8578014998512379865 of the claw prefab), nothing else. Second run: prefab md5 identical (`6d04267c...`).
- EditMode `HearthMemoryLevelsTests` + `HearthMemoryLindaTests`: 11/11 pass. Full suite left to the verifier.
- Commit with the earlier wiring commit: the wiring file plus THJ's prefab.

## Follow-up: per-stage caps

THJ decided: keep the tuned caps 2 / 3 / 4 and save the 4 hidden claws inactive.

- `HearthMemoryWiring.Linda.cs`: the single `TurnCap = 4` constant is now `TurnCaps = { 2, 3, 4 }` (stage 1, 2, 3); the three stages use `TurnCaps[0..2]`. The claw switch-off was already there (`SetActive(false)`, saved as `m_IsActive: 0`).
- `HearthMemoryLindaTests.cs`: `ThreeStagesInAQueue` expects `TurnCaps[i]` per stage and `{ 2, 3, 4 }`.
- Ran Tools > Onboarding > Wire Memory 1 (Linda) twice. The working-tree `GB_m1-linda.prefab` already differed from HEAD by exactly the 4 claws `m_IsActive` 1 -> 0 (4 lines each way) and the run changed nothing further (byte-identical before/after, and run 2 identical to run 1). So the diff vs HEAD is only the 4 claws becoming inactive; caps were already 2/3/4. No prefab was open in Prefab Mode.
- EditMode full run: 1314/1315 pass; only the known red `AIRegressionTest.Baseline_MatchesCurrentAI` fails. Both Linda tests pass.

Files: `miso/Assets/_Project/Features/Onboarding/Editor/HearthMemoryWiring.Linda.cs`, `.../HearthMemoryLindaTests.cs`, `miso/Assets/_Project/Content/Levels/Greybox/GB_m1-linda.prefab`.

Proposed commit A: `fix(onboarding): Linda's memory keeps per-stage turn caps 2/3/4 and saves the hidden claws inactive` with those three files.
