# Report: M4 R1 + R2 verify

Plan: plans/onboarding/2026-11-05-m4-mark-rework-tech.md    Agent: miso-verifier    Branch: thj/onboarding
Outcome: done (R1 and R2 pass; one expected red that waits on R3)

**Result:** PASS for R1 and R2. 19 of 20 tests passed. The one failure, `HearthMemoryLevelsTests.NothingInTheHearthGivesExperience`, is the check the plan says passes only once R3 places the pool Claws. It is not an R1 or R2 defect.

## Compile

Clean. A forced refresh compiled in about 13.7 s (`CompileScripts: 13661 ms`), followed by a normal reload. No `error CS` after it. No warnings for `CastAbilitySequence.cs` or `HearthPoolClawWiring.cs`/`HearthPoolClawTests.cs` in Editor.log. The earlier `GameEntity` CS0246 errors in the log were from before the `using MISO.Core.Fundamental;` fix. Editor was not in Play mode (Test Runner and menu ran in Edit mode). The console was cleared before the menu runs; the only entries afterwards were the wiring messages and an unrelated 2D SRP Batcher material warning.

## Wire Hearth Pool Claws

Files created under `Features/Onboarding/Hearth/` (all in `PoolClaw/`, plus `PoolClaw.meta` and `Hearth.meta`). No other file appeared under `Hearth/`.

| File | md5 (run 1 = run 2) |
| --- | --- |
| CP_Hearth_GUnitSpawnerEffect.asset | 1feb22d4b4163c50e27f12904e79df5c |
| CP_Hearth_GUnitSpawnerEffect.asset.meta | 091176456a8b5ca10c15eb574b5dfb2b |
| CP_Hearth_SpawnerCompoundEffect.asset | c05db6b77aa0b1798d6e7858a3b24b6a |
| CP_Hearth_SpawnerCompoundEffect.asset.meta | 729d45e08d52b1881a3c1b6badaf17ed |
| CP_Spawner_Hearth.prefab | 8b8e9fe41c89164ec7c9cd9492058390 |
| CP_Spawner_Hearth.prefab.meta | 2025d40bebfd2ec84c4c0c9dee7d7c99 |
| Unit_DarkClaw_Hearth.prefab | 66001cc145222f4ac49e44614ece44b4 |
| Unit_DarkClaw_Hearth.prefab.meta | 91b8a7a5c296666423609c421462ed22 |

- Idempotency: the md5 of all 8 files is identical after the second run (`diff` clean), and the file list is unchanged. The second run changed nothing.
- Console, both runs: "The Hearth pool Claws are wired: the no-experience alert Claw, its spawner and compound effects, and the pool variant." No errors or warnings from the tool.
- md5 lists: `C:\Users\javid\AppData\Local\Temp\claude\E--Work-Projects-miso\fc8a7484-be48-4d45-8fd7-e011d7c2c808\scratchpad\run1.md5` and `run2.md5`.

## Tests

Run through the Unity MCP (job a43c7085..., 14.6 s). Filters used: `MISO.Content.Levels.EditorTests.CastAbilitySequenceTests`, `MISO.Core.Features.Onboarding.EditorTests.HearthPoolClawTests`, `MISO.Core.Features.Onboarding.EditorTests.HearthMemoryLevelsTests` (its namespace is `MISO.Core.Features.Onboarding.EditorTests`). 20 run, 19 passed, 1 failed. The MCP did not drop, so the `TestResults.xml` fallback was not needed.

- CastAbilitySequenceTests (11 of 11 pass): AbilityLookup_ReceivesTheUnitAndPreset, EverythingPresent_Resolves, MissingCell_FailsWithReason, MissingPreset_FailsWithReason, MissingUnit_FailsWithReason, NullLookups_FailInsteadOfThrowing, PickUnit_SkipsUnitsThatAreNotAlive, PresetNotTargeted_FailsWithReason, PresetNotTargetingCells_FailsWithReason, UnitLookup_ReceivesTheNickname, UnitWithoutAbility_FailsWithReason.
- HearthPoolClawTests (6 of 6 pass): TheEffectsPointAtThePoolClaw, ThePoolClawGivesNoExperience, ThePoolClawIsAVariantOfTheStartsAlertClaw, ThePoolClawStartsAlert, ThePoolSummonsOnEveryTurnOfTheMemory, TheSharedAssetsAreUnchanged.
- HearthMemoryLevelsTests (2 of 3 pass): TheExperienceResourceResolves and TheHearthPlaysTheFourMemoryLevelsInOrder pass. **NothingInTheHearthGivesExperience fails.**
  ```
  GB_m4-mark/Grid/Tilemap/GridCell - (0, 4)/OccupantRoot/Unit_DarkClaw: lethalDamageXpBonus = 3
  GB_m4-mark/Grid/Tilemap/GridCell - (6, 4)/OccupantRoot/Unit_DarkClaw: lethalDamageXpBonus = 3
  GB_m4-mark/Grid/Tilemap/GridCell - (3, 5)/OccupantRoot/Unit_DarkClaw: lethalDamageXpBonus = 3
  GB_m4-mark/Grid/GridCell - (-1, 4)/OccupantRoot/CP_Spawner summons Unit_DarkClaw (GUnitSpawnerEffect): lethalDamageXpBonus = 3
  ```
  The `GB_m4-mark` level prefab still holds the stock Claws and the stock spawner (`lethalDamageXpBonus = 3`). It does not use the pool Claw yet, which is R3's job per the plan (line 37). Expected until R3.

`AIRegressionTest` was not run or touched. No full suite run.

## Acceptance criteria

- [x] Compile clean: see above.
- [x] Wiring tool builds the pool Claw, spawner and compound effects, and a second run changes nothing: identical md5 over all 8 files.
- [x] R1 cast sequence logic tests: 11 of 11.
- [x] R2 pool Claw tests: 6 of 6, including `TheSharedAssetsAreUnchanged`.
- [ ] Hearth XP check (`NothingInTheHearthGivesExperience`): fails only because R3 has not placed the pools; the pool variant itself gives no XP (`ThePoolClawGivesNoExperience` passes).

## Save reset

no

## git status --short (Features/Onboarding and Features/Levels)

```
?? miso/Assets/_Project/Features/Levels/Sequences.meta
?? miso/Assets/_Project/Features/Levels/Sequences/
?? miso/Assets/_Project/Features/Onboarding/Editor/HearthPoolClawTests.cs
?? miso/Assets/_Project/Features/Onboarding/Editor/HearthPoolClawTests.cs.meta
?? miso/Assets/_Project/Features/Onboarding/Editor/HearthPoolClawWiring.cs
?? miso/Assets/_Project/Features/Onboarding/Editor/HearthPoolClawWiring.cs.meta
?? miso/Assets/_Project/Features/Onboarding/Hearth.meta
?? miso/Assets/_Project/Features/Onboarding/Hearth/
```

The `Sequences/` and `Hearth/` folders are listed as folders (untracked); their contents are the R1 sources and tests and the 8 PoolClaw files above, each with its `.meta`.

## Needs THJ

none

## Editor checks corrections

- The earlier `tests_running` block cleared once THJ freed the editor. `clear_stuck` reported "No running job to clear" and `refresh_unity` then worked. Worth a line in `tech/editor-checks.md`: `tests_running` with no MCP job means the Test Runner is busy in the editor, so ask THJ.
- Confirmed: `execute_menu_item` runs a Tools menu item and the item's `Debug.Log` shows in `read_console` (use `types: ["all"]`). Test-name filtering by full namespace worked (all three filters matched).
- Confirmed: a forced `refresh_unity` with `compile: request` compiled in about 14 s; a second `refresh_unity` with `wait_for_ready` returned idle.

## Addendum: GridToLevelTests failures from THJ's Run All

- `Content/Levels/Greybox/__Test` is absent (checked before and after both runs).
- `MISO.Core.Levels.CEditor.GridToLevel.EditorTests.GridToLevelTests` run twice in a row through the MCP: run 1 20 of 20 passed (13.3 s), run 2 20 of 20 passed (12.9 s). That includes `Builder_StripsTheTemplatesExtrasAndLeavesNoMissingReferences` and `Builder_WritesNothingWhenThePaletteLacksAPrefab`. No failure messages.
- The folder was absent after both runs too, so TearDown cleans up. `git status` for `Content/Levels` shows only the already-modified `GB_m4-mark.prefab`; nothing left behind.
- Reading: consistent with the leftover-folder hypothesis (the failures were "already exists" and `File.Exists` true, which a stale `__Test` folder from the interrupted 01:07 run would cause; the test's own TearDown deleted it afterwards). I did not see the failing state, so this is not proven. No R1 or R2 file touches these tests or that folder.
