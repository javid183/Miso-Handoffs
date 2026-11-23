# Report: Onboarding demo 1.1, memory rules

Plan: plans/2026-11-22-onboarding-1-1-memory-rules.md    Agent: miso-implementer    Branch: thj/onboarding-demo
Outcome: done (play check still to do, batched with the other Phase 1 chunks)

## What changed

- `Resources/Tags/GTagSet.asset`, `Resources/Tags/GTagRegistry.asset`: new tag `Status.NoPassBy` (hidden, after `Status.Inactive`). Added by hand to the set and to the registry's serialized copy, so nothing else in the registry is rewritten.
- `Content/Controllers/PlayerController.prefab` (core component data): `UnitsPassByHandler.excludedTags` gains `Status.NoPassBy`. One line. No code change.
- `Features/Onboarding/LevelPassByOff.cs` (new, not core): a level component that tags every active unit of a faction (default `Bergsons`) with `Status.NoPassBy` when it starts, when the level starts, at every turn start and when a unit is born. No statics. Its handlers skip the AI worker thread.
- `Features/Onboarding/Editor/HearthMemoryWiring.Rules.cs` (new): `HearthMemoryRules.Apply(level, root, fullHealthOnLoad)`. On every family unit it sets `canCauseRevenge = 0` and `items[*].hideIfUsed = 1`, plus `minHpFractionOnLevelLoad = 1` when asked. It adds Cleanse to each hero's `LevelAbilityLock` entry and ensures `LevelPassByOff`. It changes nothing else, and running it again gives the same result.
- `HearthMemoryWiring.Linda.cs`, `.Lucy.cs`, `.John.cs`: each calls `HearthMemoryRules.Apply` after writing its ability lock (full health only for John). All three menus were run.
- `GB_m1-linda.prefab`, `GB_m2-lucy.prefab`, `GB_m3-john.prefab`: changed by those menu runs. The diffs add only the instance overrides, the Cleanse lock and the new component. No sequence or dialogue asset changed.
- `GB_m4-mark.prefab`: edited by hand in YAML. Each of the four heroes gets four overrides, and the new component is added to the level object as an added component. Cleanse was already locked for all four heroes, so the lock is unchanged. I backed the file up first. An editor script over this prefab was refused by the permission check, so I did the hand edit the brief asked for.
- `Core/Systems/BarkSystem/Runtime/BarkManager.cs` (not core) + new partial `BarkManager.PassBy.cs` (follow-up for D-616): `OnUnitsPassedBy` returns early when `PassByBarkAllowed(mover, passed)` is false, i.e. when either unit carries `Status.NoPassBy` (constant `LevelPassByOff.NoPassByTagId`, not duplicated). `BarkManager` became `partial`. The rule uses plain reference checks only.
- Tests: new `LevelPassByOffTests.cs` and `HearthMemoryRulesTests.cs`. The ability-lock tests in `HearthMemoryLindaTests`, `HearthMemoryLucyTests` and `HearthMemoryJohnTests` now expect Cleanse too, and the three test methods were renamed to say so.

## Acceptance criteria

- [x] No hero in memories 3 and 4 can cause Revenge. Set in memories 1 and 2 as well. Evidence: `HearthMemoryRulesTests.NoHeroInAnyMemoryCanCauseRevenge` checks all four memories, and a read of the M4 prefab in the editor shows every hero with `revenge=False`.
- [x] Pass-by never fires in a memory and works as before elsewhere. Evidence:
  - `LevelPassByOffTests.ATaggedUnitIsSkippedAndAnUntaggedOneStillCounts` drives the real `PlayerController.prefab` handler's excluded-tag check.
  - `ThePlayerControllersPassByHandlerExcludesTheNoPassByTag`, `TheNoPassByTagIsDefined`, `OnlyTheConfiguredFactionIsTaggedAndOnlyOnce`.
  - `HearthMemoryRulesTests.EveryMemorySwitchesPassByOffForTheFamily`, and `NoLevelOutsideTheHearthSwitchesPassByOff`, which scans every prefab under `Content/Levels`.
  - The handler excludes a pair when **either** unit has the tag (`CanPassBy`, line 101). That one gate covers the FTP fill, the synergy event, the VFX and the move previews (`PlayerController` and `UnitsCooperationHandler` both call `CanPassBy`). No core code was needed.
  - Pass-by barks (follow-up, D-616): `BarkManager` skips its pass-by bark under the same rule (either unit tagged). Test: `LevelPassByOffTests.APassByBarkIsSkippedWhenEitherUnitIsTaggedAndKeptForAnUntaggedPair` covers a tagged mover, a tagged passed unit and an untagged pair. The full bark path (baked graphs, popups through `DamageNumberManager`) needs a running level, and there are no `BarkManager` tests to build on. So the test checks the manager's own rule, and the one-line early return in `OnUnitsPassedBy` is checked by review. On screen it needs the play check.
  - Why it isn't read from the handler's list: `excludedTags` and `HasExcludedTag` are private on core `UnitsPassByHandler`, and exposing them would be a core code change. The bark check uses the shared tag constant instead, so it covers only `Status.NoPassBy`, not `Status.Inactive`. Barks for `Status.Inactive` units behave as before.
- [x] Cleanse is off every hero's bar in memories 1 to 4. Evidence: `HearthMemoryRulesTests.CleanseIsLockedForEveryHeroInEveryMemory`, plus the three updated lock tests. M4's existing `EveryDuoAndCleanseIsLockedOnEveryHero` still passes. No unlock step in M1 or M2 unlocks Cleanse: each unlocks only its listed presets, and `unlockAll` is off. Memory 4's corruption pools are untouched.
- [x] The item pouch doesn't show in any memory. `hideIfUsed = 1` is set on both items of every placed hero. With the Hearth's empty `initialItemsAvailability`, each item has 0 uses, so `IsHidden` is true and the pouch button stays off (`AbilitiesBarHUDUI.cs:79-81`). Evidence: `EveryHeroItemInAnyMemoryIsHiddenOnceItHasNoUseLeft`. The on-screen result needs the play check.
- [x] Heroes start memories 3 and 4 at full HP. Evidence: `HeroesComeIntoTheThirdAndFourthMemoriesAtFullHealth`, plus a code read of the restore order. `CombatLevelRunHandler.StartLevelIE` initializes the units first (`GUnit.Initialize` ends in `FillCurrentSpecsToMax`). It calls `FactionTracker.PrepareLevel` → `RestoreUnitPersistedStates` only after that, so the restore computes `Max(saved, max × 1)` = max. The plan's assumption holds. The rule is inline in core `GUnit`, so I couldn't test it on its own without a core change. **Needs the play check.**
- [x] Memories 1 to 3 get these through their wiring tools, so a re-run keeps them. Memory 4 was edited by hand. Evidence: the three menus ran and logged "Memory N wired"; diffs as above.
- [x] Tests (after the bark follow-up): bark fixture `RoleBarkRulesTests` plus `LevelPassByOffTests` and `HearthMemoryRulesTests`: 26 of 26 passed. Full EditMode suite: 2501 total, 2500 passed, 0 failed, 1 skipped (the Explicit AI regression test). Before the follow-up: the covering fixtures passed 94 of 94 (LevelPassByOff, HearthMemoryRules, Linda, Lucy, John, Mark, Levels, ResultLine). Full EditMode suite: 2500 total, 2499 passed, 0 failed, 1 skipped (`AIRegressionTest.Baseline_MatchesCurrentAI`, Explicit, not run). Clean compile, no errors in the console.

## Chunks

### Chunk 1.1: memory rules

- Changed: every file listed under "What changed".
- Criteria met: all seven; evidence above.
- Decisions and loose ends: see the sections below.

### Chunk 1.1 follow-up: Pass-by barks off in the memories (D-616)

- Changed: `Core/Systems/BarkSystem/Runtime/BarkManager.cs` (made `partial`; early return in `OnUnitsPassedBy`), new `BarkManager.PassBy.cs` + `.meta`, `Features/Onboarding/Editor/LevelPassByOffTests.cs` (one new test).
- Criteria met: Pass-by criterion now includes barks. Evidence: the new test; 26 of 26 in the bark and Pass-by fixtures; full suite 2501 / 2500 passed / 0 failed / 1 skipped.
- Decisions and loose ends: the rule reads the shared tag constant, because the handler's list is private core data. It covers `Status.NoPassBy` only.

## Reviews and checks

- (coordinator)

### Review (miso-reviewer, 2026-11-23): APPROVE

Pasted by the coordinator (the reviewer is read-only).

- **Must fix:** none.
- **Should fix:** split the commits. Commit 1 should hold only the core data (the tag and `excludedTags`) plus `LevelPassByOff` and its gate test. The bark gate (`BarkManager.cs`, `BarkManager.PassBy.cs`) goes in its own commit 1b, with its test moved out of `LevelPassByOffTests.cs` into its own file, so the barks can be reverted alone. Accepted by the coordinator; queued for the implementer after the stations task.
- **Notes:**
  - **Core:** no core code changed, only data. `excludedTags` changed at `PlayerController.prefab:2338`, plus the new tag in both tag assets; tags are referenced by id string, so no existing reference shifts.
  - **`CanPassBy`:** it gates FTP, the synergy event and the VFX. `BarkManager` is the only other listener.
  - **Core bark system → onboarding constant:** acceptable for now. Move it to a neutral place if a second user appears.
  - **`LevelPassByOff`:**
    - No statics.
    - Worker-thread guarded.
    - Cleaned up on disable.
    - Units added mid-level get tagged.
    - Tags don't persist between levels.
  - **Prefab YAML:**
    - The M1-M3 diffs come from the tools, and the M4 hand edit is correct (unique fileID, right targets).
    - `HearthMemoryRules.Apply` is idempotent.
  - **No other level is affected:** a test scans `Content/Levels`.
  - **Tests and code:**
    - The full-HP test checks the field only; the restore itself needs THJ's play check.
    - No private IDs anywhere.
    - Line endings and BOMs unchanged.
  - **Loose end:** `HearthMemoryWiringMark.Run()` doesn't call `HearthMemoryRules.Apply`. That would be a cheap safety net if M4 is ever regenerated. Outside this plan: backlog.

## Save reset

No.

## Decisions I made

- Tag name `Status.NoPassBy`, following `Status.Inactive`, which already serves as a Pass-by exclusion. Hidden in game, with a short description. No `RemoveSubs` on the `Status` root exists in the data, so Cleanse-style tag stripping can't remove it.
- `LevelPassByOff` lives in `Features/Onboarding` (namespace `MISO.Core.Features.Onboarding`) and follows the subscription pattern of `TurnStartActionPointLimit`. Units are matched by their serialized faction id, so tagging works before the level has resolved factions.
- It tags only active units. A unit that hasn't woken up yet rebuilds its tag set in `Awake` and would re-add the tag as turn-based, so it would expire on the first tick. Units revealed later are caught by the turn-start sweep or by `unitBorn`.
- Revenge and the item rule are set in all four memories: free through the shared helper. Full health only in memories 3 and 4, as the plan says.
- The shared helper is a new file rather than one copy per tool. Same behaviour.
- I hand-edited the registry's serialized tag copy instead of regenerating it. Regenerating would have rewritten unrelated drift in it (the Unaware icon and description), and the registry rebuilds that copy from the sets in `Awake` anyway.

## Needs THJ

None.

## Docs to update

- GDD `family-systems.md`: Pass-by and Revenge are off in the Hearth memories (and so is Cleanse; the item pouch is hidden while it is empty).
- `missions-structure.md`: the memory rows (no Revenge, Pass-by or Cleanse; full HP on entering memories 3 and 4).
- `tech/onboarding-merge.md` if it lists memory rules. `tech/core-systems.md` Pass-by row: `PlayerController.prefab`'s `excludedTags` now also holds `Status.NoPassBy`, set per level by `LevelPassByOff`.

## Risks and loose ends

- Pass-by barks: fixed in the follow-up (D-616, see above). The bark system (`Core/Systems/BarkSystem`) now references `MISO.Core.Features.Onboarding` for the tag constant. Core already references feature code (the duo insert does), but the reviewer may prefer the constant to live elsewhere.
- `HearthMemoryWiringMark.Run()` (no menu) doesn't call `HearthMemoryRules.Apply`. If someone ever re-runs it on M4, the rules there would rely only on the hand edits it keeps. I left the tool alone, as the plan asks.
- Unity touched `Assets/TextMesh Pro/Resources/Fonts & Materials/LiberationSans SDF - Fallback.asset` during the session (dynamic font atlas). It isn't part of this work: leave it out of the commits.
- THJ's uncommitted files weren't touched (they show in `git status` as before).

## Proposed commits

1. `feat(passby): a level switch that turns Pass-by and its barks off for the family` (core data, its own commit):
   - `miso/Assets/_Project/Resources/Tags/GTagSet.asset`
   - `miso/Assets/_Project/Resources/Tags/GTagRegistry.asset`
   - `miso/Assets/_Project/Content/Controllers/PlayerController.prefab`
   - `miso/Assets/_Project/Features/Onboarding/LevelPassByOff.cs` + `.meta`
   - `miso/Assets/_Project/Core/Systems/BarkSystem/Runtime/BarkManager.cs`
   - `miso/Assets/_Project/Core/Systems/BarkSystem/Runtime/BarkManager.PassBy.cs` + `.meta`
   - `miso/Assets/_Project/Features/Onboarding/Editor/LevelPassByOffTests.cs` + `.meta`
2. `feat(hearth): memories have no Revenge, Pass-by or Cleanse, hide the empty item pouch, and start the last two at full health` (plain, depends on 1):
   - `miso/Assets/_Project/Features/Onboarding/Editor/HearthMemoryWiring.Rules.cs` + `.meta`
   - `miso/Assets/_Project/Features/Onboarding/Editor/HearthMemoryWiring.Linda.cs`, `HearthMemoryWiring.Lucy.cs`, `HearthMemoryWiring.John.cs`
   - `miso/Assets/_Project/Content/Levels/Greybox/GB_m1-linda.prefab`, `GB_m2-lucy.prefab`, `GB_m3-john.prefab`, `GB_m4-mark.prefab`
   - `miso/Assets/_Project/Features/Onboarding/Editor/HearthMemoryRulesTests.cs` + `.meta`
   - `miso/Assets/_Project/Features/Onboarding/Editor/HearthMemoryLindaTests.cs`, `HearthMemoryLucyTests.cs`, `HearthMemoryJohnTests.cs`

Commit 1 holds the core prefab data, the new component and the small bark check. It stays separate so it can be reverted on its own. Leave out `Assets/TextMesh Pro/Resources/Fonts & Materials/LiberationSans SDF - Fallback.asset` (Unity noise).

## Other branches

None (the memories exist only on `thj/onboarding-demo`).

## How to see it

1. Open `Scenes/PreloadScreen.unity` and start the Hearth (memory 1) from the toolbar level picker, or play through to it.
2. In each memory: the ability bar has no Cleanse button and no item pouch button.
3. In memory 3 or 4, walk a hero through or next to an ally. No FTP gain, no Pass-by flash on the ally, no Pass-by highlight in the move preview, and no pass-by bark.
4. In memory 2, let Lucy take damage, then win. Memory 3 starts with John, Linda and Lucy at full HP. Do the same into memory 4.
5. Let a hero fall in memory 3 or 4: no Revenge on the allies. The memory is lost as before.
6. In any other level (for example `LevelM1-C3`), Pass-by works as before.
