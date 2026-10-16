# AI regression test: failing on `thj/home-test` (updated 2026-09-29)

Test: `MISO.Core.Systems.AI.EditorTests.AIRegressionTest.Baseline_MatchesCurrentAI` (`Core/Systems/AISystem/Editor/AIRegressionTest.cs`; also **Tools/AI/Run Regression Test**). It compares the current AI graphs, abilities and unit prefabs against a baseline catalog embedded in the test file, then runs a stress pass.

Status: was 33 failures out of 680 checks; after the M2 fix it was **18 failures out of 665** (re-run by THJ, compile succeeded). Still FAIL. THJ confirmed on 2026-09-29 that the team has not started on the remaining failures. The counts were not re-taken after the `origin/main` merge (51a4e608), which touched Toba's wall ability and Lucy's decoy assets, so the numbers may differ slightly. Not part of any Home milestone: leave it red until the AI owner picks it up.

## Caused by Home M2: fixed and confirmed

The unit scan skipped only `/Content/Levels/`, so the 14 sortie level copies under `Content/Home/Sorties/Levels/` were counted as "new unit prefab is not in today's baseline". Fix: `IsLevelPrefab(path)` helper (skips both folders), used by `CheckUnits` and `CheckCustomEvalHosts`. Those 14 lines and the `units.count` failure are gone.

## Remaining 18, probably older, owner unknown (needs someone who knows the AI system)

Not verified against the commit before M2 (none of the remaining lines mention M2 content). Suspected source: the Dom → Toba rename and AI graph edits.

- New ability `Resources/UnitSpecific/Player/Dom/Abilities/WallAbility/Toba_Ability_Wall.asset` is not in the baseline (`abilities.count` expected 80, found 81).
- "ability missing from prefab": Unit_Toba_Ally (FamilyDedication, HealthPotion, John_Ability_Taunt, John_Ability_Walk), Unit_TobaEnemy (FamilySuperTime), Unit_Lucy (Lucy_Ability_FactionRole), Unit_Mark (Linda_Lucy_Duo_Ability, Lucy_Ability_FactionRole).
- Graph fingerprints changed: Generic_I_Walk, Generic_P_Walk_Melee, Generic_P_Walk_Ranged, Generic_Teleport (UtilityScoreEvaluators).
- `Features/Player/PlaceHolder/Unit_Placeholder.prefab` reported "unit prefab missing" (baseline lists it; not confirmed why it is no longer found). `Content/FamilySuperTime/DUO/StuntCamActorSet.prefab` reported as a new unit prefab.
- `intent.unit-tile.enemy`: enemy unit-tile intent should target that unit.
- **Fatal, triage first:** `NullReferenceException` in `AIStrategyPlanner.HandleLivingUnitsCondition` at AIStrategyPlanner.cs:163 (`influenceSubjects = cCondition.Faction.Controller.AliveUnits...`, the branch taken when there are no attacked units), reached from `AIRegressionTest.RunStress` (AIRegressionTest.cs:662, `LivingUnitsLOCondition` created with no faction). Likely the test's condition has no `Faction`/`Controller`, but a real level objective built without a faction would crash the same way. Decide which before re-baselining.

## Suggested order

1. Triage the fatal NullReference (real bug vs test stub).
2. Confirm each remaining diff is intended (Toba changes, graph edits, Unit_Placeholder), then regenerate the baseline before merging the branch to main. Do not regenerate over unreviewed diffs.
