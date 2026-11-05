# Report: Shared objective condition checker, splitter and scan test

Plan: plans/onboarding/2026-11-04-linda-memory-tuning.md (chunk G4)    Agent: miso-implementer    Branch: thj/onboarding
Outcome: done (scan test red on purpose, see below)

## What changed

All new, editor-only, in `miso/Assets/_Project/Core/Levels/Editor/` (LF, no BOM, like `LevelXpChecker.cs`), no onboarding dependency, no statics, no runtime/core file touched:
- `SharedObjectiveConditionChecker.cs` (+ `.meta`): `Check(GameObject|path)` returns every condition managed reference used by more than one slot; `Split(GameObject)` / `SplitPrefab(path)` give each repeat after the first its own `Copy()`, return one log line per split. Scans every `[SerializeReference]` slot typed `LevelObjectiveConditionBase` in each `CombatLevel` (so `lObjectives` win/defeat groups AND `decisions[].objectives`).
- `SharedObjectiveConditionTool.cs` (+ `.meta`): menus `Tools/Levels/Split Shared Objective Conditions (Selected Levels)` and `(All Levels)` (with confirm dialog). Logs `[SplitSharedConditions] <prefab> -> <component>: <path> (<type>) split from rid N`. Idempotent (skips prefabs with nothing shared; second run does nothing).
- `SharedObjectiveConditionTests.cs` (+ `.meta`): the scan test over `Content/Levels`, plus checker/splitter tests on temp prefabs in `Assets/__SharedConditionTest` (deleted after), including one on a copy of a real variant prefab (original verified untouched).

## Acceptance criteria

- [x] Checker, reusable from test and menu: yes.
- [x] Menu splitter, deep copy, idempotent, logs: yes. `Copy()` is `MemberwiseClone` (shallow: arrays/struct refs are shared in memory), but the result is assigned to a managed-reference slot and serialized by value, so the saved prefab holds independent data; verified values identical after split (test) and that editing one no longer edits the other.
- [x] Scan test over all level prefabs: present. RED on this branch (expected, see findings).
- [x] Checker/splitter tests on temp copies: 4 pass.
- Not run on real prefabs. Full EditMode: 1315 tests, 4 failed: the new scan test (expected), `AIRegressionTest.Baseline_MatchesCurrentAI` (known), and two not mine: `HearthMemoryLindaTests.TheHiddenClawsAreSwitchedOffInThePrefab` and `HearthMemoryLindaTests.ThreeStagesInAQueue` (onboarding tests, likely tied to the uncommitted Linda work in progress; not investigated).

## Save reset

no

## Decisions I made

- Checked effective (loaded) data via `SerializedObject`, not raw YAML, because almost all level prefabs are variants whose YAML holds only overrides.
- Shared means same managed reference id across any slots in one `CombatLevel` component (also two slots in one objective).

## Needs THJ

none (coordinator to judge the finding below)

## Findings: the shared cases

The scan over all `Content/Levels` prefabs with a `CombatLevel` finds exactly ONE shared condition:
- `Level2/Level2-C2.prefab`: `LivingUnitsLOCondition` (rid 8046274707106824281 in the loaded data) shared by `lObjectives.defeatObjectiveGroups[0].objectives[0].conditions[0]` and `...objectives[1].conditions[0]`. Values: faction Neutral, comparison LessThanOrEqual, count 0, state Exist (defeat when no living neutral unit remains). Objective[0] has empty text; objective[1] text "Whitemother must survive.", both not visible. Runtime state: only `_total/_alive/_dead`, recomputed on every evaluate, so sharing is functionally harmless; objective[1] was added in the variant by the inspector "+" copy (the variant override at ~line 8067 of the prefab points it at the same ref). Both objectives are identical in effect, so sharing looks unintended but is behaviorally neutral. Splitting keeps values.

The other two named cases are NOT shared in effective data:
- `Level2/Level2-C3-2.prefab` (8046274729047228497) and `Level2/LevelDomFight.prefab` (8046274707106824280): those rids are only managed-reference override entries in the variant YAML (and in `LevelBase.prefab`, where 280/281 are two distinct conditions: win LivingUnits Enemy, defeat LivingUnits Bergsons). No slot in the loaded component uses one rid twice.
- In `Level2-C2`, rids ...209 and ...212 are used once each in `decisions.decisions[0]` and `[1]`; the extra override entries pointing `decisions[0].objectives.winObjectiveGroups[1]` at 209 are stale (that group no longer exists in the effective data). Harmless; a stale override remains in the YAML.
- No other level prefab is reported. `GB_m1-linda` is clean.

## Docs to update

- `tech/` Levels note could mention the tool and scan test (coordinator's call).

## Risks and loose ends

- Splitting a variant writes overrides into the variant (verified on a copy only); review the prefab diff after running it for real.
- The new scan test stays red until `Level2-C2` is split (one menu click) or the coordinator accepts it.
- Two Linda onboarding tests fail in the current tree (see above).

## Proposed commits

1. feat(levels): editor check and split tool for shared objective conditions, with a scan test: the six files under `miso/Assets/_Project/Core/Levels/Editor/SharedObjectiveCondition*` (.cs and .meta) (plain). Commit after the data fix, or knowingly with the scan test red.

## Other branches

main (cherry-pick; no onboarding dependency).

## How to see it

1. Select `Content/Levels/Level2/Level2-C2.prefab`, run Tools > Levels > Split Shared Objective Conditions (Selected Levels): console logs the one split; run again: nothing.
2. Test Runner > EditMode > `SharedObjectiveConditionTests`.

## Review fixes

- `SharedObjectiveConditionTests.cs`: `Split_WorksOnCopyOfRealVariantPrefabWithSharedCondition` replaced by `Split_WorksOnVariantPrefabWithSharedConditionOverride`. It is self-contained: a temp base prefab (`MakePrefab(shareFirstTwo: false)`), a variant of it saved in the temp folder, the second objective's condition set to the first's as a variant override, then check, split, check, turns `{4,4,7}`, second split a no-op, base untouched. No level scan. Added a small `Objectives` helper.
- `SharedObjectiveConditionChecker.cs`: the hand-copied -2 is now `UnityEngine.Serialization.ManagedReferenceUtility.RefIdNull` (exists in 6000.3.4f1; compiles).
- Files LF, no BOM (kept). Compiled with 0 errors.

Proposed commit B (the six `SharedObjectiveCondition*` files, .cs and .meta, as in the commit above, now including these fixes): `feat(level-tools): editor check and split tool for shared objective conditions, with a scan test`. Goes before commit C.

## Level2-C2 split

Ran Tools > Levels > Split Shared Objective Conditions (Selected Levels) on `Content/Levels/Level2/Level2-C2.prefab` only (no prefab stage open). Console: split `lObjectives.defeatObjectiveGroups[0].objectives[1].conditions[0]` (LivingUnitsLOCondition) from rid 8046274707106824281; second run: byte-identical.

Diff: 25 insertions, 1 deletion. The second defeat objective's condition slot now points at new rid 8881842456907219243 (the one changed line); the 24 added lines are the override entries creating that reference (type LivingUnitsLOCondition) with values `factionRef.entityID` Neutral, `comparisonStrategy` 3 (LessThanOrEqual), `count` 0, `state` 0 (Exist), `evaluationMode` 0 - identical to the original.

Proposed commit C: `fix(levels): Level2-C2's second defeat objective gets its own condition` with `miso/Assets/_Project/Content/Levels/Level2/Level2-C2.prefab`.

Full EditMode run after all three: 1314/1315 pass; only `AIRegressionTest.Baseline_MatchesCurrentAI` fails (known). The scan test and both Linda tests pass.
