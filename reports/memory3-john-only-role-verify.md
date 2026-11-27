# Verify: Memory 3, only John has a Family Role

Plan: plans/2026-11-27-memory3-john-only-role.md    Implementer report: reports/memory3-john-only-role.md    Agent: miso-verifier    Date: 2026-11-27

- **Result:** PASS (quiet checks). The in-game behaviour is left to THJ's own play check (no play session here).
- **Branch:** `main` (uncommitted change).
- **Save reset:** no.

## Compile

Clean. Forced refresh with compile through the Unity MCP (`refresh_unity`, force, compile request) at about 11:59. Editor.log: last build `*** Tundra build success`, then `Reloading assemblies after finishing script compilation.` and `Domain Reload Profiling: 4773ms`; no `error CS` after it. Console: 0 errors. Warnings present are the known "Serialization depth limit 10 exceeded" lines (StatBackedValue / AbilityOrchestrator chains) and one MCP WebSocket line, unrelated to this change.

Note: Editor.log earlier in the session (lines ~2876-2939) holds `error CS0246/CS0103: 'ActionFlowEvent'` in `LevelFamilyRoleSuppressionTests.cs(27,...)` from the implementer's iteration; three successful builds and reloads follow, and the current file compiles.

## Tests

| Run | Total | Passed | Failed | Skipped |
| --- | --- | --- | --- | --- |
| Covering: `LevelFamilyRoleSuppressionTests`, `HearthMemoryJohnTests`, `FactionRoleSuppressionTests` (full class names) | 41 | 41 | 0 | 0 |
| Full EditMode suite (Unity MCP, 120 s) | 3072 | 3071 | 0 | 1 |

- Skipped: `MISO.Core.Systems.AI.EditorTests.AIRegressionTest.Baseline_MatchesCurrentAI` (Skipped:Explicit), as expected.
- No GridToLevel lock flake this run; no `M3DefenceTests` failures seen.
- AI regression not run (no AI graph, AI ability or unit prefab change).

## Acceptance criteria

1. **Feature component, suppression level start to level end, zone hidden, lets go on disable/destroy/level end, Super Time wait, no statics:** Pass. `LevelFamilyRoleSuppressionTests` 15/15 (incl. `Apply_TheListedRolesNeverTriggerAndTheirZonesAreHidden`, `Apply_AnUnlistedUnitKeepsItsRole`, `Disabling_LetsGoOfEverything`, `Destroying_LetsGoOfEverything`, `TheLevelEnding_LetsGoOfEverythingForGood`, `DuringFamilySuperTime_TheRolesWaitForTheEnd`, `AHoldsZoneSwitchShowingTheZone_DoesNotShowAZoneTheLevelHides`). `LevelFamilyRoleSuppression.cs` and `LevelRoleZoneHidden.cs` have no static fields (one `private static` helper method, `RoleOf`).
2. **Wiring lists Linda and Lucy, not John; re-runs keep it:** Pass on the test (`Memory3_SwitchesOffTheRolesOfLindaAndLucyOnly`). Re-run idempotence taken from the implementer's report, not re-run here.
3. **Prefab diff only the new component:** Pass. `git diff --stat` on `GB_m3-john.prefab`: 18 insertions, 0 deletions; the diff is one `m_AddedComponents` entry (`addedObject 147272562868792769`) and the `LevelFamilyRoleSuppression` MonoBehaviour with `units` 7607883068595211265 and 505914430083513819.
4. **Edit-mode tests:** Pass (see above).
5. **No IDs, line endings/BOM:** Pass. No `D-`/`H-` IDs in the four files; all four LF, no BOM (`file` reports ASCII / UTF-8 without CRLF).

In-game behaviour (no Watch / follow-up prompts for Linda and Lucy, zones hidden on select / hover / Shift, John's Shield still prompts, roles back in the next level): **Not run: needs a play session** (THJ plays it himself).

## Asset tree after the runs

`git status --short -- miso/Assets/_Project` is identical to before the runs: only the listed files (`GB_m3-john.prefab`, `HearthMemoryWiring.John.cs` modified; the three new `.cs` files and their `.meta` untracked). Nothing else modified by the runs. Outside `_Project`, `miso/miso.slnx` is modified, as it already was at the session start. Editor left in Edit mode with `PreloadScreen` active, not dirty, as found.

## Bugs found

none

## Editor checks corrections

- Confirmed: Unity MCP `run_tests` with `group_names` as anchored full-class-name regexes (`^MISO\.Core\....ClassName\.`) runs exactly those fixtures; `get_test_job` with `include_failed_tests` lists the skipped Explicit test by name.
- Full EditMode suite on `main` is now 3072 tests, about 120 s through the MCP.
- `refresh_unity` (force, compile request, `wait_for_ready`) returned with `resulting_state: compiling`; the Editor.log end-of-reload markers (`Tundra build success`, `Domain Reload Profiling`) worked to confirm it finished.
