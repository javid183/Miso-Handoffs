# Verify: Masher reckless tank, C3 (data)

Plan: plans/2026-10-20-masher-reckless-tank-tech.md (C3)    Agent: miso-verifier    Branch: masher-tweak
Outcome: PARTIAL (quiet checks all pass; Play check not run)

## Result

PARTIAL. Every quiet criterion passes. The "did not initialize its role ability" warning check needs Play and was not run.

## Compile

Clean. Forced refresh plus compile request, then the console read for errors and warnings. No errors. The only warnings are the known "Serialization depth limit 10 exceeded" ones (RuntimeAbility / FactionRoleHandlerBase.ability and similar). Nothing from the Masher files.

## Tests

EditMode Run All through the MCP: 327 run, 326 passed, 1 failed, 0 skipped (48 s). The one failure is `MISO.Core.Systems.AI.EditorTests.AIRegressionTest.Baseline_MatchesCurrentAI` (known red; CHECKS: 706, FAILURES: 35).

## Acceptance criteria

- [x] One `MasherGoblinFactionRoleHandler` on the prefab: scratch `execute_code` on `LoadPrefabContents` (unloaded, nothing saved) found handlers = 1, on `Unit_MasherGoblin` (root).
- [x] Handler ability preset is `MasherGoblin_Ability_Counter` (`ability.preset`).
- [x] Unit ability list is exactly Attack and Walk: `GUnit.abilityOrchestrator.abilities[0]` = `MasherGoblin_Ability_Attack`, `[1]` = `MasherGoblin_Ability_Walk`.
- [x] Both Attack and Counter have `targetType` = 2 (CellOccupant), read through SerializedObject.
- [x] Counter damage equals the slam's: iterating every serialized property of the two assets, the only differences are the `m_Name` characters. All object references (spawner effect, evaluator and so on) are the same assets, so the 10 x Stat_DMG chain is shared and identical.
- [x] EditMode: only `Baseline_MatchesCurrentAI` red (see Tests).
- [ ] "Did not initialize its role ability" warning gone in Play: Not run. Entering Play would mean choosing a level and passing the Assign Placeholders dialog, which needs driving the game. I did not enter Play mode. The editor state is unchanged.

## Bugs found

None.

## Save reset

No.

## Editor checks corrections

- Confirmed: the MCP `refresh_unity` with `compile: request` returns while compiling. After about 5 s the console was readable, and no compile errors showed.
- `get_test_job` for the full suite: first 60 s wait timed out, second returned (as the implementer noted). The result is over 58k characters and saved to a file. `failures_so_far` held the failing test's `full_name`. The `result.summary` has the counts.
- `execute_code` here uses the CodeDom compiler (C# 6) and fails on unknown namespaces. `MasherGoblinFactionRoleHandler` is in `MISO.Core.Features.Bergsons`, not a FamilyRoles namespace. Matching by `GetType().Name` avoids the problem.

## Branch

masher-tweak (uncommitted change).
