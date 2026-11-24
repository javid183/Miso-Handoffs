# Merge origin/main into thj/onboarding-demo: test check (2026-11-23)

- **Result:** FAIL (2 EditMode failures, neither the known flake)
- **Branch:** thj/onboarding-demo at merge commit 55f51381b. Quiet check, command line, editor closed (no Unity.exe in tasklist, Editor.log ends with a clean layout save, `Temp\` was stale). No files under `miso/` changed.
- **Compile:** clean (0 `error CS` in the full run and the AI run).
- **Tests (full EditMode):** 2599 total, 2596 passed, 2 failed, 1 skipped (the Explicit AI baseline). 150 s. No GridToLevel failures, so no rerun needed.

## Failures

1. `MISO.Core.EditorTests.SaveFileSerializerTests.DictionaryKeysNamedKeysAndValues_RetainTheirLists`
   - Message: `Expected: True  But was: False`, at SaveFileSerializerTests.cs:153 (`JToken.DeepEquals` of `JsonUtility.ToJson(state)` vs the round-tripped state).
   - Changed by merge: yes. Test and `SaveFileSerializer.cs` are both new, from Khash's save restructure.
   - Read: round trip of a `SerializationWrapper<string, List<int>>` with keys literally named "keys" and "values" does not come back equal. Compare `Expand`/`Normalize` in SaveFileSerializer.cs (~lines 152-221, the `obj.Count == 2 && obj["keys"] is JArray` shortcut) with the test's expectation. Likely a bug in Khash's code or a test that relies on Unity's JsonUtility ordering. It fails on his own code, so it probably failed on his branch too (not checked).

2. `MISO.Core.Systems.EnemyAlertSystem.EditorTests.EnemyAlertDataTests.UnawareTag_IsInTheRegistry_AndShownInGame`
   - Message: `Expected: True  But was: False`, at EnemyAlertDataTests.cs:94 (`Assert.IsTrue(tag.ShowInGame)`).
   - Test file NOT changed by the merge (it is ours, from 0d3427685). The code under test's data WAS: `Resources/Tags/GTagSet.asset` came in from main with the Unaware tag `showInGame: 1` changed to `showInGame: 0`. Same merge turned `displayEnemyAwareness` and `displayEnemyTargets` off in GlobalSettings.
   - Read: a deliberate change by Khash, not a regression in our code. The test now contradicts main's data. THJ's call (D-642 follow-up): update the test to the new rule, or set the tag back to shown. Also check that the awareness display still works as intended on our branch, since the tag is hidden.

## AIRegressionTest.Baseline_MatchesCurrentAI (by name)

- Failed with `CHECKS: 731  FAILURES: 44`. Last recorded: 43 (2026-11-18). Count rose by 1. Not fixed or re-baselined.
- The extra one: `units.ability Unit_ArcherGoblin/ArcherGoblin_Ability_WebThrow: ability missing from prefab`. The merge brought both the baseline line adding WebThrow (f04e9b0ae, which edits AIRegressionTest.cs) and the later removal of WebThrow from the Archer Goblin prefab (eeac5ac67). The expected catalog says the ability is on the prefab, the prefab does not have it. Khash's baseline edit was not reverted after he removed the ability. Other failures keep their earlier shape (new evaluators, abilities and unit prefabs not in the baseline; count mismatches abilities 91 vs 99, graphs 29 vs 30, units 21 vs 23; one NullReferenceException in `fatal`; one `intent.unit-tile.enemy`). The WebThrow evaluator and ability assets are in the baseline but not otherwise failing.
- Per the rule, a rise in the count is reportable; nothing else in the failure list points at our branch's changes.

## Save reset
No.

## Editor checks corrections
- Confirmed: "Temp\ may be stale" (Temp present with no Unity process); full EditMode run took 150 s for 2599 tests, not 53-63 s as the file says (suite has grown).
- `-logFile`/`error CS` pattern works; Test result XML read with `test-case result="Failed"` works.
