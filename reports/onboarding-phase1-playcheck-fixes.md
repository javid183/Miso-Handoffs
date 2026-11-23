# Report: Phase 1 play-check fixes (Encore locked ability, LevelPassByOff run not ready)

Plan: coordinator brief (no plan file)    Agent: miso-implementer    Branch: thj/onboarding-demo
Outcome: done (code and tests written; not compiled or run, the editor is open)

## What changed

- `miso/Assets/_Project/Features/Player/Linda/Scripts/Quiver/QuiverAbilityInfo.cs`: new `EffectsOf(ability)` returns null when `UpgradeLevel < 0`, else `EffectSetLevel?.effects`. `IsRecall`, `TryGetArrow` and `TryGetLindaDuoPartner` use it (so do `NeedOf`, `HiddenFromBar`, `GreyReason` through them). Those were the only `EffectSetLevel` reads in the file.
- `miso/Assets/_Project/Features/Player/Linda/Scripts/Quiver/LindaQuiver.EncoreAp.cs`: the Encore scan moved into `public static FindEncore(RuntimeAbility[])` (same loop, so it can be tested without an AP consumer); `EncoreAp` calls it.
- `miso/Assets/_Project/Features/Onboarding/LevelPassByOff.cs`: `TagLevelUnits` returns early when `run.CurrentFactionControllerOrNull == null`.
- New `miso/Assets/_Project/Features/Player/Linda/Scripts/Quiver/Editor/EncoreLockedAbilityTests.cs`.
- New `miso/Assets/_Project/Features/Onboarding/Editor/LevelPassByOffRunNotReadyTests.cs`.
- No core file touched (`AbilityPreset`, `AEffectBase`, `RuntimeAbility`, `CombatLevelRunHandler`, `Mission.cs`, `GlobalSettings.asset` untouched). All files are LF without BOM, as before.

## Root causes (confirmed in code)

1. `RuntimeAbility.EffectSetLevel` is `preset.GetEffectSetLevel(_upgradeLevel)`; `AbilityPreset.GetEffectSetLevel` does `upgradeLevel == 0 ? baseLevel : higherLevels[upgradeLevel - 1]`, so level -1 reads `higherLevels[-2]`. `QuiverAbilityInfo.IsRecall` read it for every ability in `AllAbilities`. A locked ability (e.g. `lockedByDefault`, `DefaultUpgradeLevel == -1`) listed before Encore threw in `EncoreAp`. On hover that surfaced via `GreyReason`; inside the feasibility check `HasGroundedArrows` the throw was swallowed by the `catch {}` in `AEffectBase`, so the check read false. Note `_encore` is cached only once found, so every call re-threw until then.
2. `CombatLevelRunHandler.Instance` is `_instance` set in `Awake`; `_factionControllers` is null until the faction list is built later. `Controllers` is `_factionControllers.ToArray()`. `LevelPassByOff.Subscribe` calls `TagLevelUnits` right after subscribing, which can run in that window.

## Acceptance criteria

- [x] Locked ability on Linda: hover Encore throws nothing: `IsRecall`/`TryGetArrow`/`TryGetLindaDuoPartner`/`NeedOf` skip locked abilities; covered by tests below. Needs THJ play check for the real hover.
- [x] Encore castable with grounded arrows and AP covering cost: the lookup now returns Encore past a locked ability, so `EncoreAp` is real instead of the swallowed throw; the existing `TheFeasibilityCheck_BlocksAtOneApAndAllowsAtTwo` still covers the rule. Needs play check end to end.
- [x] No NullReference from `TagLevelUnits` at level start: early return. Units are still tagged: safe because `Start` (`TagActiveUnitsUnder`), `levelStarted`, every `turnStarted` and `unitBorn` all tag again, and the faction list exists by `levelStarted`/first turn. No new hook is needed.
- [x] Tests cover both (see below).

## Tests added (run by filter)

- `MISO.Core.Features.Bergsons.EditorTests.EncoreLockedAbilityTests` (4 tests): `ALockedAbilityListedBeforeEncore_DoesNotBreakTheLookup`, `ALockedAbilityIsNeitherEncoreNorAnArrowNorADuo`, `EveryLinda_AbilityCanBeScannedWhileLocked`, `TheLookupHandlesMissingLists`. They load the Linda prefab contents, call `InitializePartially` (same pattern as `RuntimeAbilityInitializeTests`), lock abilities with `SetUpgradeLevel(-1)`, and unload in TearDown.
- `MISO.Core.Features.Onboarding.EditorTests.LevelPassByOffRunNotReadyTests` (3 tests): `TaggingBeforeTheRunBuiltItsFactionsDoesNotThrow`, `TaggingWithAnEmptyFactionListDoesNotThrow`, `UnitsAlreadyInTheLevelAreStillTaggedWhenTheRunIsNotReady`. They put a `CombatLevelRunHandler` into the base class's static `_instance` by reflection and restore it in TearDown (Awake does not run in EditMode).

## Not verified

- Nothing compiled or run (editor open, no Unity MCP). Run both filters above, then the whole EditMode suite.
- No test builds a real `APConsumer`, so the full `HasGroundedArrows` -> `EncoreAp` path with a locked ability ahead is covered through `FindEncore` (the part that threw) plus the existing AP tests, not in one test.
- The new tests assume the Linda prefab has an unlocked Recall in `AllAbilities` (its GUID is referenced in the prefab) and at least two abilities.
- `.meta` files for the two new test files will appear when Unity imports them; they go with the commits.
- Whether the NRE count at level start drops to 0, and the 45 exceptions, need a play check.

## Save reset

no

## Decisions I made

- Skipping locked abilities in `EffectsOf` (not in `AbilityPreset`), per the brief; a locked Encore therefore counts as not Encore.
- Extracted `FindEncore` as a public static for testability (same behavior).
- Early return in `LevelPassByOff` rather than a retry, since later events already retag.

## Needs THJ

none

## Docs to update

- none

## Risks and loose ends

- Other callers of `RuntimeAbility.EffectSetLevel` on a locked ability elsewhere in the repo (core: `GUnit.cs:1394`, `PlayerController.cs:1139/1324`, `UnitThreatAnalysis`, `UtilityVariables`) can hit the same throw; left alone (core).
- `AEffectBase`'s `catch {}` hides this class of bug from the log.

## Proposed commits

1. `fix(linda): skip locked abilities when looking for Encore and quiver abilities`: `miso/Assets/_Project/Features/Player/Linda/Scripts/Quiver/QuiverAbilityInfo.cs`, `miso/Assets/_Project/Features/Player/Linda/Scripts/Quiver/LindaQuiver.EncoreAp.cs`, `miso/Assets/_Project/Features/Player/Linda/Scripts/Quiver/Editor/EncoreLockedAbilityTests.cs` and its `.meta` (plain)
2. `fix(onboarding): do not tag level units before the run has built its factions`: `miso/Assets/_Project/Features/Onboarding/LevelPassByOff.cs`, `miso/Assets/_Project/Features/Onboarding/Editor/LevelPassByOffRunNotReadyTests.cs` and its `.meta` (plain)

(Per CLAUDE.md, no attribution trailers in these commit messages.)

## Other branches

none known

## How to see it

1. Play a level with Linda and a locked ability on her bar; hover Encore: no exception in the console.
2. With grounded arrows and enough AP, Encore casts.
3. Start the onboarding level: no NullReference from `LevelPassByOff.TagLevelUnits`; Pass-by stays off for the family.

---

## Verifier section (miso-verifier, quiet checks only, 2026-11-23)

**Result:** PASS for everything checkable without a play session; the real Encore hover and cast are Not run (THJ replays them).
**Branch:** thj/onboarding-demo (not switched, no git writes)
**Editor state:** was not in Play mode ("Already stopped"); forced refresh plus compile request, waited until tests could run.

**Compile:** clean. No `error CS` lines in Editor.log, no compile errors or warnings from `QuiverAbilityInfo.cs`, `LindaQuiver.EncoreAp.cs`, `LevelPassByOff.cs` or the two new test files. The console held only "Serialization depth limit 10 exceeded" messages (StatBackedValueBase / GTag.subTags cycles via LindaQuiver._encore, FactionRoleHandlerBase.ability and others), not compile output and not from the changed files.

**Tests:**
- `MISO.Core.Features.Bergsons.EditorTests.EncoreLockedAbilityTests`: 4 run, 4 passed, 0 failed.
- `MISO.Core.Features.Onboarding.EditorTests.LevelPassByOffRunNotReadyTests`: 3 run, 3 passed, 0 failed.
- Full EditMode suite: 2583 total, 2582 passed, 0 failed, 1 skipped (the Explicit `AIRegressionTest.Baseline_MatchesCurrentAI`, not run: no AI graph, AI ability or unit prefab changed). 133 s. The GridToLevel lock flake did not appear, so no re-run was needed.

**Acceptance criteria:**
- Locked ability, hover Encore throws nothing: Pass at test level (`ALockedAbilityListedBeforeEncore_DoesNotBreakTheLookup`, `ALockedAbilityIsNeitherEncoreNorAnArrowNorADuo`, `EveryLinda_AbilityCanBeScannedWhileLocked`). The real hover: Not run, needs a play session.
- Encore castable with grounded arrows and AP: Pass at test level (lookup finds Encore past a locked ability; existing AP feasibility tests pass in the full suite). End to end: Not run, needs a play session.
- No NullReference from `TagLevelUnits` at level start: Pass at test level (3 LevelPassByOffRunNotReadyTests). Level-start behavior: Not run.
- Tests cover both: Pass.

**Bugs found:** none.
**Save reset:** no
**Editor checks corrections:** the Editor log is at `%LOCALAPPDATA%\Unity\Editor\Editor.log` (here `C:\Users\Dead Mage\AppData\Local\...`), not under `javid`; the user name differs on this machine. Full-suite count on this branch is now 2583 tests (about 133 s via the MCP); `get_test_job` with `wait_timeout` worked without disconnects. A filtered `run_tests` by full class name reported the right counts (4 and 3).
