# Report: Bond Lite C1 (store, settings, save, reset, lock rules, silent-lock test)

Plan: plans/onboarding/2026-10-26-bond-lite-tech.md    Agent: miso-implementer    Branch: thj/bond-lite
Outcome: done

Paths are under `miso/Assets/_Project/`.

## What changed

- `Core/Systems/HomeSystem/Runtime/BondLite/BondStore.cs`: new. Saved pair points, `PairKey`, `BondLevel`, `GetBond`, `GetLevel`, `Add` (returns the levels crossed), `BondLevelReached` event, `BondSource` enum, `BondPair` and `BondSaveData`, new save key `"Bond"`, `ResetPlayModeState()`.
- `Core/Systems/HomeSystem/Runtime/BondLite/BondSettingsSO.cs`: new. Thresholds and starting values, loaded from Resources.
- `Core/Systems/HomeSystem/Runtime/BondLite/HomeLockRules.cs`: new. Port of `thj/home-test`'s file listing Sisters' Rivalry and Tempest Bloom (Linda-Lucy, Lv 2).
- `Resources/BondSettings.asset` (+ `.meta`): new. `{10, 25, 45}`, Linda-Lucy 15. Created through `AssetDatabase`, not hand-written.
- `Core/Managers/PlayModeStaticReset.cs`: one line, fully qualified, so no new `using`. **Core file.**
- `Core/Systems/HomeSystem/Editor/BondStoreTests.cs`, `HomeLockRulesTests.cs`, `SilentUnlockableLockTests.cs`: new tests.
- Folder metas Unity generated: `Core/Systems/HomeSystem/Runtime.meta`, `Runtime/BondLite.meta`, `Editor.meta`, plus each script's `.meta`.

## Acceptance criteria

- [x] Pair points saved and loaded: `SaveRoundTrip_KeepsEveryPair` runs the store through `JsonUtility` the way `SaveLoadManager` does. **The real file path is not exercised**, because `SaveFilePath` can't be redirected without a core API change and THJ's save must stay untouched. Needs the verifier's play check.
- [x] Levels at 10/25/45: `Level_FollowsTheThresholds`, `Thresholds_AreTenTwentyFiveFortyFive_InTheDefaultsAndTheAsset`.
- [x] `Add` reports crossed levels: `Add_ReportsOnlyTheLevelsItCrossed`, `Add_FromTheStartingValue_DoesNotReportLevelsAlreadyHeld`.
- [x] Linda-Lucy starts at 15 on a new save, others 0: `Asset_StartsLindaLucyAt15_AndOthersAt0` reads the real asset.
- [x] Old saves load empty and give starting values on first read: `OldOrEmptySave_LoadsEmpty_AndGivesStartingValues`.
- [x] Pair key symmetry and ordering match `thj/home-test` (`string.CompareOrdinal`): `PairKey_IsTheSameInEitherOrder_AndSortsOrdinally`.
- [x] Play-mode reset: `ResetPlayModeState_DropsTheInstance`; hook added to `PlayModeStaticReset`.
- [x] Silent-lock check reads the real assets and lists offenders: `EveryUnlockableOffByDefault_CanBeUnlockedByANodeOrARunUpgrade`; the detection itself is covered with made-up data in `FindSilentLocks_FlagsOnlyEntriesNothingCanTurnOn`.
- [x] Allow-list with plain reasons for `__DoNotRemove_` and `_JohnResolve`; `AllowList_HoldsOnlyEntriesThatAreStillSilent` fails if one stops being silent.
- [x] Rivalry's literal is plain text, not resolved at load, and not required by the tests.
- [x] EditMode suite: 1505 of 1506 passed. The only failure is the known red `AIRegressionTest.Baseline_MatchesCurrentAI`, not touched. Console shows no Bond errors.

## Save reset

No. `SaveData.json` still has its 17:24 timestamp from before the run and no `Bond` key. Tests use local stores with no save callback.

## Decisions I made

- Starting values are read, not written: a pair stays out of the store until it first earns points. Same result as "starting values on first read", reads never change state, and untouched pairs follow later tuning of the asset.
- `Add` saves at once. It has to: `SaveLoadManager.Register` restores the last saved state on every re-registration, so unsaved points would be lost on the next `Instance` access. `AbilityIntroductionTracker` and `PlayedSequencesTracker` work the same way.
- The per-mission help-bonus cap is left to C3. The plan's piece 1 mentions it, but C1's acceptance doesn't and the chunk table puts "cap respected" in C3. `Add` already takes `source` for it; **`source` is unused until then.**
- Thresholds live in the settings asset under `thj/home-test`'s field name `bondLevelThresholds`, rather than in code.
- `UnlockableGroup` is `""` here instead of `"Home"`, because this branch's set has an empty group title. So Rivalry's literal is `_SistersRivalry`.
- Ported `HomeLockRules` without `PassBy`, `PassByPairs`, `OpenLockIds`, the Linda-Toba Duo and Command Shield Dash, since their locks aren't listed here. `All` is one array, so a third node is one line.
- The silent-lock test reads nodes from `GameDataSO.PlayerUnits` and skips `hideInSkillTree` nodes, since neither enemy trees nor hidden nodes can be bought. That is slightly stricter than the plan's wording. No node is hidden today, so the result is the same.
- The test ignores run-upgrade grants of `__DoNotRemove_`. The run-upgrade assets hold 31 references to it (`grantUnlockable` and `requiredUnlockable` together) as an untouched default, and a grant among them would otherwise count it as reachable.
- Added `TempestBloomLock_NamesARealEntryOfTheUnlockableSet`, not in the plan: it catches a typo in the literal. It skips Rivalry for now.

## Needs THJ

None. `_JohnResolve`'s allow-list reason ("no code reads it") comes from a grep of `.cs`, `.prefab` and `.asset` files, where the only hit is the set itself.

## Docs to update

- `tech/home-system.md`: Bond Lite (store, save key `"Bond"`, settings asset path, `Instance` rule).
- `tech/core-systems.md`: no API change; `PlayModeStaticReset` gains one call.
- `branches.md`: merge note, see below. The plan puts these at the end of the feature, not this chunk.

## Risks and loose ends

- **C2:** `HomeLockRules` has no lookup by literal yet (it wasn't in C1's scope, and `thj/home-test` doesn't have one). The gate needs one.
- **C3:** read `BondStore.Instance` every time and don't cache it. A kept reference misses a later `SaveLoadManager.Load`, and its points never reach the file.
- **C3:** help bonuses will save mid-combat, once per `Add`, and each one writes the whole save. Barks and enemy introductions also save on their own triggers, but I did not trace whether those fire mid-combat, so check what a mid-mission save captures.
- **C3:** subscribers to `BondLevelReached` are lost at play-mode reset, since it is an instance event. Subscribe after the reset, not once forever.
- **C4:** Rivalry's `UnlockableSet` entry must have the id `SistersRivalry` to match `_SistersRivalry`. Its node then satisfies the silent-lock test with no test edit.
- **Sandbox:** `SaveLoadManager.Save` does nothing in a sandbox level, so once a save with a `Bond` entry exists, points added there disappear at the next `Instance` access. The trackers share this. It doesn't matter for the mission-end source (skipped in the sandbox) but could confuse a help-bonus check run in one.
- **Same-session save wipes:** `ClearSaveData` leaves the store's memory intact until restart, as with the trackers. `LevelSelectUI`'s reset button and the editor's Clear Save Data used during Play don't quit, so old points can be written back by the next save. Not fixed: it needs a core change.
- **Merge with `thj/home-test`:** that branch defines `BondPair` and `HomeLockRules` in the same namespace, so the BondLite copies must be deleted at merge. Its Bond data lives inside `HomeSaveData`, and its Rivalry literal is `Home_SistersRivalry`, so saved points under `"Bond"` and a bought `_SistersRivalry` need carrying over if those saves must survive.
- **Existing test leaves a scratch folder (not fixed):** the full run left `Content/Levels/Greybox/__XpTest/`, timestamped during the run, while the plugin session dropped twice. I suspect the drop, but didn't confirm it. Re-running `GridToLevelXpTests` (6/6 passed) removed it through its own TearDown, and the folder is gone. If it shows up in `git status` again, don't stage it.
- Not mine and left alone: `AIFactionBrain.cs`, `AIUnitBrain.cs`, the TMP font, `PreloadScreen.unity`, `ProjectSettings/*`.

## Proposed commits

1. `feat(home): saved pair Bond store with lock rules and a silent-lock test` (core touch, one line in `PlayModeStaticReset`; save data, new key):
   - `miso/Assets/_Project/Core/Managers/PlayModeStaticReset.cs`
   - `miso/Assets/_Project/Core/Systems/HomeSystem/Runtime.meta`
   - `miso/Assets/_Project/Core/Systems/HomeSystem/Runtime/BondLite.meta`
   - `miso/Assets/_Project/Core/Systems/HomeSystem/Runtime/BondLite/BondStore.cs` + `.meta`
   - `miso/Assets/_Project/Core/Systems/HomeSystem/Runtime/BondLite/BondSettingsSO.cs` + `.meta`
   - `miso/Assets/_Project/Core/Systems/HomeSystem/Runtime/BondLite/HomeLockRules.cs` + `.meta`
   - `miso/Assets/_Project/Resources/BondSettings.asset` + `.meta`
   - `miso/Assets/_Project/Core/Systems/HomeSystem/Editor.meta`
   - `miso/Assets/_Project/Core/Systems/HomeSystem/Editor/BondStoreTests.cs` + `.meta`
   - `miso/Assets/_Project/Core/Systems/HomeSystem/Editor/HomeLockRulesTests.cs` + `.meta`
   - `miso/Assets/_Project/Core/Systems/HomeSystem/Editor/SilentUnlockableLockTests.cs` + `.meta`

The core line stays in this commit even though core changes normally get their own: the hook doesn't compile without `BondStore`, and `BondStore` leaks state between Play sessions without the hook. It can't be reverted alone either way.

## Other branches

`thj/home-test`, at merge (see Risks).

## How to see it

Nothing changes in the game yet: C1 has no UI, sources or gate.

1. Window > General > Test Runner > EditMode, filter on `BondStoreTests`, `HomeLockRulesTests` and `SilentUnlockableLockTests`, then Run Selected.
2. Select `Assets/_Project/Resources/BondSettings.asset`: thresholds 10, 25, 45 and Linda / Lucy at 15.
3. To see the silent-lock test work, set a spare entry in `Resources/Unlockables/UnlockableSet.asset` so nothing unlocks it, run the test, read the id in the failure, then undo.

## Review (coordinator's condensed copy, 2026-11-06)

**APPROVE.** Read only. Commit split: `SilentUnlockableLockTests.cs` + `Editor.meta` first, then the rest. `Add`'s immediate save is sound (`Register` restores `LastSave`; `Save` is synchronous; mid-combat saves already happen), but C3 must not `Add` in combat: see the plan. `ClearSaveData`: a real New Game quits first, so it doesn't inherit Bond; `LevelSelectUI.cs:49` and the editor's clear during Play do. If a no-quit New Game is added, `GameHandler.ResetProgress` needs `_instance?.RestoreState(null)`. Silent-lock test can fail for real. Real-file save round trip stays on the play check.
