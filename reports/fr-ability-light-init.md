# Report: Role abilities use the light init on the partial path

Plan: decision D-387 (core bug fix, size S; cause in `reports/hero-animation-events-noise.md`)    Agent: miso-implementer    Branch: thj/onboarding
Outcome: done

## What changed

- `miso/Assets/_Project/Core/Systems/AbilitySystem/Abilities/Runtime/FactionRoleHandlerBase.cs` (core, Family Roles): `InitializePartially` now calls `ability.InitializePartially(orchestrator)` and `superTimeAbility.InitializePartially(orchestrator)` instead of the full `Initialize`. 2 lines. BOM and LF kept.
- `miso/Assets/_Project/Core/Systems/AbilitySystem/Abilities/Editor/FactionRoleHandlerPartialInitTests.cs` + `.meta` (new, BOM, LF): one EditMode test with 3 cases (Linda, Lucy, John).

## The three checks

**(a) Does `RuntimeAbility.InitializePartially` give the partial path everything it needs?** Yes.
- Partial (`RuntimeAbility.cs:206-218`) sets `_owner`, the upgrade level from `preset.DefaultUpgradeLevel`, resets `_temporaryLevelBonus`, registers with `SaveLoadManager` (`{Nickname}-{preset}-sd`, upgradable presets only, so the earlier FR/FST save fix is kept), and prepares `StatAttributes` and `additionalStatSources`.
- Full `Initialize` (`:220-253`) adds only three things on top:
  1. `_coolingDownRemainingTicks = initialCooldown`: combat only. The partial callers (`FactionTracker.InitializePoints`, `CharacterSelectPanelUI.RefreshTotalFP`, `AbilityUpgradePanelUI`) never read the cooldown (grep of the Home UI folders: no `Cooldown` reads). `FamilyTimePoints` and `FamilyActionPoints` don't use the role handler or its abilities at all.
  2. `StatAttributeGlobalSourceRegistry.Register(globalStatAttributeSourceId, ...)`: of the five heroes, only Linda's role ability sets an id (`LindaFR`, `Unit_Linda.prefab:2470`). Nothing in `Assets/` reads `LindaFR` (grep across every `.cs`, `.asset` and `.prefab`), and the real `Initialize` in combat still registers it.
  3. The activation-frame event appended to the serialized `animationEvents`, and `_eventsFrameMap`: these only matter for playing the ability's animation in combat. This is the bug.
- The orchestrator's normal abilities were already on `InitializePartially` along this path (`AbilityOrchestrator.cs:47-48`). The role abilities now get the same treatment. `StatBackedEvaluationProbe` (editor) already calls `factionRole.Ability.InitializePartially` / `SuperTimeAbility.InitializePartially` for the same purpose (`:676-678`).

**(b) Does any subclass rely on the full init in `InitializePartially`?** No.
- John, Linda, Lucy and Mark don't override `InitializePartially` (grep: none). Lucy overrides only `Initialize` and calls the base. Toba has no handler.
- `MasherGoblinFactionRoleHandler.InitializePartially` calls the base and sets `Orchestrator`, nothing more. It doesn't use the frame map or the cooldown.
- `_abilitiesInitialized = true` is still set. With the light init, `StatAttributes` exists, so `CanTickAbility` → `PhaseTick` still works if a partially initialized handler ever got ticked. (Prefab assets aren't ticked.)

**(c) Where does the real initialization happen in play?** `GUnit.Initialize` (`GUnit.cs:308-310`) → `AbilityOrchestrator.Initialize` (`:53-65`) → `_factionRoleHandler.Initialize(this)` → `FactionRoleHandlerBase.Initialize` (`:104-115`), which still calls the full `ability.Initialize` / `superTimeAbility.Initialize`. That runs on the spawned level instances. This path is unchanged.

## Acceptance criteria

- [x] The partial path no longer grows the role abilities' `animationEvents`: covered by `FactionRoleHandlerPartialInitTests.PartialInit_Twice_LeavesRoleAnimationEventsUnchanged` (Linda, Lucy, John).
- [x] The test fails on the old code: I ran it before the fix and all 3 cases were red. Linda's role ability went 17 → 19, Lucy's 18 → 20, John's super time 62 → 64 (one entry per call, 2 calls). All 3 are green after the fix.
- [x] Save registration kept: `RuntimeAbility.InitializePartially` registers the same key under the same condition (code read; no new test).
- [x] Character select FP, skill tree panel and faction points are unaffected: code read (check a). The full suite is green apart from the known red test.
- [x] EditMode Run All: 1344 run, 1343 pass. The only failure is `AIRegressionTest.Baseline_MatchesCurrentAI` with `CHECKS: 712  FAILURES: 41`, the same count as the latest known-red runs (`reports/onboarding-c4c-trail.md`).
- [x] No prefab, scene or asset touched: `git status -- miso/Assets/_Project/Features/Player` is clean after the run.

## Test design

The test loads each hero prefab with `PrefabUtility.LoadPrefabContents`, which makes an isolated preview-scene copy of the file's data, and unloads it in TearDown. The asset in memory is never touched and nothing is saved. On the copy it calls `unit.AbilityOrchestrator.InitializePartially(unit)` twice; that is the exact call `GUnit.InitializePartially` makes. It reads the `ability.animationEvents` / `superTimeAbility.animationEvents` array sizes through a fresh `SerializedObject`, so no core accessor was needed. It asserts first that at least one of the two role abilities is `EventBasedAnimated`, so the test can't pass vacuously.

I didn't call the full `GUnit.InitializePartially`. Its extra steps (resolving the faction and `Faction.Prepare` on the faction asset, equipment, attribute sets) have nothing to do with this bug and would mutate shared assets.

## Save reset

no

## Decisions I made

- The test calls `AbilityOrchestrator.InitializePartially`, not `GUnit.InitializePartially`. It is the same handler path without the side effects on the faction asset (Tier 1).
- The counts are read through `SerializedObject`, without adding a public accessor to `RuntimeAbility`, so the core API is unchanged (Tier 1).

## Needs THJ

none

## Docs to update

- `tech/core-systems.md` (Family Roles row) could note that the handler's partial init now uses the light ability init, so it no longer appends to the serialized animation events.

## Risks and loose ends

- The test's `InitializePartially` registers the heroes' upgradable role abilities in the static `SaveLoadManager` registry in edit mode, pointing at the preview copies (the same thing the existing `StatBackedEvaluationProbe` editor tool does). `PlayModeStaticReset` clears it on the next Play. An edit-mode `SaveLoadManager.Save` called by an editor tool right after the tests would write those copies' state: the default upgrade level, or the level loaded from the save. Low risk.
- Junk entries already in `Unit_Linda/Lucy/John.prefab` and the level-prefab overrides are untouched, as decided (root fix only). If the hero prefabs in THJ's open editor already grew in memory this session, they stay grown until the assets are reimported or the editor restarts.
- Hardening left as a separate option: `RuntimeAbility.Initialize` still appends to the serialized list. Calling it twice on the same object in combat, or on an asset, would still grow it.

## Proposed commits

1. `fix(abilities): role handler's partial init no longer adds animation events to hero prefabs`. Files: `miso/Assets/_Project/Core/Systems/AbilitySystem/Abilities/Runtime/FactionRoleHandlerBase.cs`, `miso/Assets/_Project/Core/Systems/AbilitySystem/Abilities/Editor/FactionRoleHandlerPartialInitTests.cs`, `miso/Assets/_Project/Core/Systems/AbilitySystem/Abilities/Editor/FactionRoleHandlerPartialInitTests.cs.meta` (core). The fix and its test go in one commit so the cherry-pick to `main` stays one unit.

## Other branches

`main` (cherry-pick of the commit above, as planned).

## How to see it

1. Restart Unity, or right-click `Unit_Linda.prefab` > Reimport, to drop any in-memory growth from earlier sessions.
2. Select `Unit_Linda.prefab`, expand `LindaFactionRoleHandler` > Ability > Animation Events, and note the count (17 today, including the old junk).
3. Play a mission start or open the Home character select / upgrade panel a few times, then stop Play.
4. The count is unchanged; before the fix it grew by one each time. Saving a level that holds Linda adds no new `animationEvents` overrides.
5. Test Runner > EditMode > `FactionRoleHandlerPartialInitTests`: 3 green.
