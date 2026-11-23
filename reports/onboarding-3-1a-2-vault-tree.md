# Report: Vault buyable in Mark's skill tree (plus the save fixes it needed)

Plan: plans/2026-11-23-onboarding-m1-m2-build-tech.md (chunk 3.1a-2), extended by the coordinator with D-645, D-646, D-647    Agent: miso-implementer    Branch: thj/onboarding-demo
Outcome: done. Four units, each its own proposed commit. Full EditMode suite green: 2605 tests, 2604 passed, 1 skipped (the Explicit AI baseline). AI baseline run by name: 44 failures, the same as the last recorded count.

## What changed

- `Core/Systems/EnemyAlertSystem/Editor/EnemyAlertDataTests.cs`: the Unaware tag test now expects the tag hidden in game, and is renamed to match.
- `Core/Managers/SaveFileSerializer.cs` (core, Save): when saving a live state, `Normalize` knows the state's type and also converts a dictionary wrapper whose `values` JsonUtility left out.
- `Core/Systems/AbilitySystem/Abilities/Runtime/RuntimeAbility.cs` (core), new partial `RuntimeAbility.SaveRegistration.cs` (+ `.meta`), `FactionRoleHandlerBase.cs` (core): the Super Time copy of an ability no longer registers with `SaveLoadManager`.
- `Core/Systems/AbilitySystem/Abilities/Editor/SuperTimeSaveEntryTests.cs` (+ `.meta`): new test, a shared upgradable preset saves and reloads the bar copy's level.
- `Resources/UnitSpecific/Player/Mark/Vault/Mark_Ability_Attack_Vault.asset`: `upgradable: 1`, unlock cost 1 SP.
- `Resources/UnitSpecific/Player/Mark/Command/Mark_Ability_Attack_Command.asset`: unlock cost removed.
- `Features/Player/Mark/Prefabs/Unit_Mark.prefab`: tree node 0 now unlocks Vault (preset, title, icon, description, upgrade description), and `edges[0]` now leads to Stunning Vault instead of Sapping Order.
- `Features/Player/Mark/Scripts/Editor/MarkStartingKitTests.cs`: updated for the new kit and tree, including a bought-Vault save and reload test.

All paths are under `miso/Assets/_Project/`. Line endings and BOM are kept: assets, prefab and the Mark test are LF with no BOM; `RuntimeAbility*.cs`, `FactionRoleHandlerBase.cs` and the new core test have a BOM like their neighbours. Nothing touched M1, `GB_m2-lucy` or THJ's uncommitted files.

## Acceptance criteria

- [x] **Mark's first tree node unlocks Vault for 1 SP, and Command stays open from the start.** Evidence: `MarkStartingKitTests.TheFirstTreeNodeUnlocksVault`, `VaultCostsOneSkillPoint`, `CommandHasNoUnlockCost`, `CommandIsOpenFromTheStart` and `VaultIsLockedFromTheStart` pass.
- [x] **Command's child isn't gated behind Vault, and Stunning Vault sits behind the Vault node.** Evidence: `SappingOrderIsNotGatedByAnotherNode` and `StunningVaultSitsBehindTheVaultNode` pass. `ABoughtVault_SurvivesASaveAndReload` also checks that Stunning Vault's graph lock opens once Vault is bought.
- [x] **A bought Vault survives a save and reload.** Evidence: `ABoughtVault_SurvivesASaveAndReload`. It buys node 0 on an isolated prefab copy, then reads the save entry (upgrade level 0), then registers again and finds Vault still at 0. With the Super Time fix turned off, this test and `SuperTimeSaveEntryTests` both fail (-1 instead of 0). I checked that once and then restored the fix.
- [~] **The Vault run upgrades appear once Vault is bought.** Covered by mechanism, not by a test: `RunUpgradeTracker.HasRequiredAbility` checks `Available`, and the bought level now sticks. The play check confirms it.
- [x] **The two tests that were failing after the merge now pass.** `SaveFileSerializerTests.DictionaryKeysNamedKeysAndValues_RetainTheirLists` and `EnemyAlertDataTests.UnawareTag_IsInTheRegistry_AndHiddenInGame` both pass in the full run.
- [x] **Full EditMode suite.** Command line, Unity 6000.3.4f1: 2605 total, 2604 passed, 0 failed, 1 skipped (`AIRegressionTest.Baseline_MatchesCurrentAI`, Explicit). The GridToLevel flake didn't appear.
- [x] **AI baseline, run by name:** 731 checks, **44 failures**, the same as recorded. None of them name Mark, Vault or Command. Mark's Vault graph checks all pass. Not re-baselined.

## Chunks

### Unit 1: Unaware tag test follows main (D-645)

- Changed: `Core/Systems/EnemyAlertSystem/Editor/EnemyAlertDataTests.cs`. The test is renamed to `UnawareTag_IsInTheRegistry_AndHiddenInGame` and asserts `ShowInGame` is false, with a plain message. `GTagSet.asset` is untouched.
- Criteria met: the test passes in the targeted and full runs.
- Decisions and loose ends: none.

### Unit 2: Save file serializer keeps a wrapper's keys when JsonUtility drops its values (D-646, core)

- **Root cause**, confirmed with a temporary probe test (deleted afterwards, no files left behind):
  - JsonUtility can't serialize nested collections, so for `SerializationWrapper<string, List<int>>` it writes only the keys: `{"lists":{"keys":["keys","values"]}}`.
  - `Normalize` converted a wrapper only when it saw both `keys` and `values`, so it left this object as it was.
  - `Expand` is driven by the type, so it read the untouched object as an already-converted dictionary with one entry named `"keys"`. Restored: `{"lists":{"keys":["keys"]}}`.
  - The real cause was the mismatch between a shape-based `Normalize` and a type-based `Expand`. The suspected handling of keys literally named `keys`/`values` was not the cause.
- **Fix:**
  - `SerializeState<T>` passes `typeof(T)` to `Normalize`.
  - `Normalize` walks fields the way `Expand` does (new private helpers `IsWrapper`, `ElementType`, `FieldType`).
  - A field typed as a wrapper that has only `keys` is converted too, with null values. Those values could never be saved anyway, and the keys survive.
  - The legacy-file path still calls `Normalize` without a type, so its behaviour is unchanged.
  - Existing shape rules are kept as they are: no other output changes, no format change, and old files load the same.
  - No real save type has nested-collection values today, so real saves are byte-identical.
- Changed: `Core/Managers/SaveFileSerializer.cs` (LF, no BOM).
- Criteria met: all 21 `SaveFileSerializerTests` cases pass, Khash's test unchanged. The other save-related tests in the suite also pass: `RuntimeAbilityInitializeTests`, Home save tests, the faction and stat suites.
- Decisions and loose ends: the opposite case remains. An ordinary class with exactly `keys` and `values` array fields would still be converted by shape and not rebuilt. None exists, as noted in the save read. Making the typed path skip non-wrappers would fix it, but changes behaviour beyond this test, so I left it alone.

### Unit 3: The Super Time copy doesn't register for saving (D-647, core)

- **Where:** new partial `RuntimeAbility.SaveRegistration.cs`:
  - an `internal bool SkipsSaveRegistration { get; set; }` property;
  - a private `RegisterForSave()`, called from both `Initialize` and `InitializePartially` in place of the inline `SaveLoadManager.Register`.
  - `FactionRoleHandlerBase.Initialize` and `InitializePartially` set the flag on `superTimeAbility` before initializing it.
  - **No public signature changes.** The flag is `internal` and isn't serialized.
- **Effect:** a bar ability keeps its save entry when the same preset is also the unit's Super Time. Today only Mark's Vault is in that position. John, Linda and Lucy have no upgradable Super Time preset, so nothing changes for them. A Super Time copy keeps its default level, as before. Nothing reads its level: 3.1a found Mark's Super Time does nothing.
- Changed: `RuntimeAbility.cs`, `RuntimeAbility.SaveRegistration.cs` (+ `.meta`, new GUID), `FactionRoleHandlerBase.cs`, `Editor/SuperTimeSaveEntryTests.cs` (+ `.meta`).
- **Test:** `SuperTimeSaveEntryTests.SharedUpgradablePreset_SavesAndReloadsTheBarCopysLevel`.
  - It loads an isolated copy of `Unit_Mark.prefab` and marks the Super Time preset upgradable in memory, so it doesn't depend on unit 4's data. The flag is restored in TearDown and the asset is never saved.
  - It raises the bar copy's level, invokes the save entry's own save callback, registers again and checks the level.
  - It works on a private copy of `SaveLoadManager`'s registry (via reflection, restored afterwards), so nothing is written to disk.
  - It fails without the fix.
- Decisions and loose ends: `Core/Editor/StatBackedEvaluationProbe.cs:678` (an editor tool) still calls `InitializePartially` on the Super Time copy directly, without the flag. It's editor-only and harmless today. Listed, not changed.

### Unit 4: Vault bought in Mark's tree (D-637)

- Changed:
  - Vault preset: `upgradable: 1`, `unlockResourceRequirements` = 1 × `MainResource_SP`.
  - Command preset: `unlockResourceRequirements: []`.
  - `Unit_Mark.prefab` overrides on node 0:
    - `abilityPreset` → Vault;
    - `title` → `Vault`;
    - `icon` → Vault's preset icon;
    - `description` → "Mark leaps to a nearby tile, fracturing the ground, slightly damaging and pushing enemies back.";
    - `upgradeDescription` → `Unlocks Vault.`;
    - `edges[0].inputNodeGuid` → Stunning Vault's node (`6e2a6359-…`).
  - `MarkStartingKitTests.cs`:
    - `VaultIsNotSaved` replaced by `VaultIsSaved`;
    - `TheFirstTreeNodeStillPointsAtCommand` replaced by `TheFirstTreeNodeUnlocksVault`;
    - new `CommandHasNoUnlockCost`, `VaultCostsOneSkillPoint`, `StunningVaultSitsBehindTheVaultNode`, `SappingOrderIsNotGatedByAnotherNode`, `ABoughtVault_SurvivesASaveAndReload`.
- Unchanged on node 0: guid, Ability mode, `unlockLevel` 0, `upgradeLevels` 0, position. No other prefab overrides Mark's tree.
- Criteria met: 11/11 `MarkStartingKitTests` pass.
- Decisions and loose ends:
  - The node text comes from Vault's own preset line, so it has no `[PLACEHOLDER]` tag. Listed under "Docs to update" for the narrative pass.
  - I left `SkillTreeSmokeTest` (menu tool) alone. Its generic checks assume tier 0/1/2/3 nodes, and Mark's tree uses levels 0/2/3/5, so `N(1, 0)` already finds no node for Mark before this change. Updating it is more than a cheap fix.

## Reviews and checks

- (coordinator: core units 2 and 3 to be reviewed one by one)

## Save reset

No. The tests never write the save file. They use a private copy of the in-memory registry and restore it.

## Decisions I made

- **Unit 2:** the fix is type-guided only on the live save path, and the legacy-file path is unchanged. That's the smallest change that removes the mismatch for this case.
- **Unit 3:** an `internal` flag set by the role handler, instead of a new public overload or a different init order. The public API is unchanged, and the rule is explicit about the Super Time copy, as decided.
- **Unit 3 test:** it marks the preset upgradable in memory so the core commit stands alone before the Mark data commit.
- **Probe:** I used a temporary EditMode probe to confirm the serializer's root cause, then deleted it and its `.meta`.

## Needs THJ

None.

## Docs to update

- `tech/core-systems.md`:
  - Ability data and runtime / Family Roles: the Super Time copy of an ability doesn't register a save entry (`SkipsSaveRegistration`, set by `FactionRoleHandlerBase`). The bar copy owns the key.
  - Infrastructure / Save: `SaveFileSerializer.SerializeState` normalizes with the state's type. A wrapper whose `values` JsonUtility dropped keeps its keys.
- `design/gdd/characters/mark.md` and `progression-economy.md`: Vault is bought in Mark's first tree node for 1 SP, and Command is free from the start. Stunning Vault needs Vault. Sapping Order needs only level 2.
- Narrative pass: node 0 text "Mark leaps to a nearby tile, fracturing the ground, slightly damaging and pushing enemies back." and "Unlocks Vault." (D-348: no tag in the asset).
- `reports/merge-origin-main-2026-11-23-save-read.md`: the Super Time duplicate key is now fixed.

## Risks and loose ends

- **Old dev saves** (as in 3.1a, D-636): a save made before this change has no Vault entry, so Vault starts locked and can be bought. A save that bought Command keeps a Command entry, which is harmless. Use a cleared save for checks.
- The 1 SP that 3.1a freed up for Mark is now spent on Vault again.
- `StatBackedEvaluationProbe` registers the Super Time copy without the flag (editor tool only).
- `SkillTreeSmokeTest`'s Mark section doesn't match Mark's tree layout. This predates the change.
- The batch-mode runs opened the project headless. `ProjectSettings/*` were already modified by THJ before I started. I didn't compare whether the runs rewrote them, so check them before staging.

## Proposed commits

1. `test(enemy-alert): the Unaware tag is hidden in game`: `miso/Assets/_Project/Core/Systems/EnemyAlertSystem/Editor/EnemyAlertDataTests.cs` (plain)
2. `fix(save): keep a dictionary's keys when JsonUtility drops its values`: `miso/Assets/_Project/Core/Managers/SaveFileSerializer.cs` (core)
3. `fix(abilities): a Super Time copy no longer overwrites the ability's save entry`: `miso/Assets/_Project/Core/Systems/AbilitySystem/Abilities/Runtime/RuntimeAbility.cs`, `miso/Assets/_Project/Core/Systems/AbilitySystem/Abilities/Runtime/RuntimeAbility.SaveRegistration.cs`, `miso/Assets/_Project/Core/Systems/AbilitySystem/Abilities/Runtime/RuntimeAbility.SaveRegistration.cs.meta`, `miso/Assets/_Project/Core/Systems/AbilitySystem/Abilities/Runtime/FactionRoleHandlerBase.cs`, `miso/Assets/_Project/Core/Systems/AbilitySystem/Abilities/Editor/SuperTimeSaveEntryTests.cs`, `miso/Assets/_Project/Core/Systems/AbilitySystem/Abilities/Editor/SuperTimeSaveEntryTests.cs.meta` (core)
4. `feat(mark): Vault is bought in Mark's skill tree in place of Command`: `miso/Assets/_Project/Resources/UnitSpecific/Player/Mark/Vault/Mark_Ability_Attack_Vault.asset`, `miso/Assets/_Project/Resources/UnitSpecific/Player/Mark/Command/Mark_Ability_Attack_Command.asset`, `miso/Assets/_Project/Features/Player/Mark/Prefabs/Unit_Mark.prefab`, `miso/Assets/_Project/Features/Player/Mark/Scripts/Editor/MarkStartingKitTests.cs` (plain data + tests; depends on 3, or a bought Vault doesn't stick)

## Other branches

None. The save fixes (2, 3) are general and would also suit `main`, but carry them over only if THJ wants them there.

## How to see it

1. Open Unity and let it recompile. Clear the save outside Play mode (`Tools > Save Data > Clear Save Data`), or use the in-game reset.
2. Play from `Scenes/PreloadScreen.unity` to Home, and give Mark at least 1 SP (play to a level-up, or use `Tools` > faction resource window).
3. Open Mark's skill tree:
   - the first node reads **Vault** with Vault's icon, costs 1 SP, and is upgradable;
   - **Sapping Order** waits only on level 2;
   - **Stunning Vault** shows locked until Vault is bought (and level 3).
4. Buy Vault. Close and reopen the tree, or leave Home and come back: Vault stays owned and the SP stays spent.
5. Start a fight with Mark: his bar shows Fist Blitz, Walk, Command **and Vault**. Over a run, the Vault run upgrades (Long Vault, Vault Stun) can now be offered.
6. Optional: quit Play mode, re-enter and load the save. Vault is still owned.

## Review: SaveFileSerializer (core), 2026-11-23

**APPROVE** (miso-reviewer). Diagnosis right: JsonUtility drops a `values` list it can't serialize (`List<List<int>>`), leaving a keys-only wrapper the old `Normalize` passed through. Output changes only for a known `SerializationWrapper<,>` with nothing but `keys`; no current save type (`EquipmentManager`, `FactionTracker`, `StatAttributeSet` wrappers) can produce one, so existing payloads are unchanged. Loading untouched; legacy path keeps old behaviour. CRLF kept, no BOM, no statics, no private IDs. Should-fix: none. Notes: own commit; tell Khash (about 40 lines inside his `Normalize`); legacy and type-less reads still can't recover a keys-only wrapper (no current type makes one).
