# Report: John memory fix-ups and Encore refresh (verify)

Plan: none (coordinator brief)    Agent: miso-verifier    Branch: thj/onboarding
Outcome: partial. Compile clean and both tool re-runs idempotent; the EditMode suite could not be run because the Unity MCP connection kept dropping.

## What changed

Nothing edited by me. Console cleared once (editor state only). The two menu tools were run and wrote nothing (md5 identical).

## Result

PARTIAL.

- **Compile:** forced refresh and compile, no errors. Warnings in the console: only "Serialization depth limit 10 exceeded" (StatBackedValueBase / RuntimeAbility._owner cycles); none from the four changed files.
- **Tests:** not run. `run_tests` (full suite, then the three Onboarding/Encore classes by full name) failed 6 times: "Unity plugin session ... disconnected while awaiting command_result" or TimeoutError. The editor log shows the MCP WebSocket closing and reconnecting in a loop after the menu runs. `TestResults.xml` in LocalLow was never refreshed (still the implementer's 2-test run from 16:58, 2 passed). Editor is open, so no command line route.

## Idempotency

- Before: md5 recorded for GB_m3-john.prefab and the 9 `EncoreKitTool.Levels` prefabs (scratchpad `before.md5`).
- Ran Tools > Onboarding > Wire Memory 3 (John): log "Memory 3 (John) wired: start, hint, win stage and end." (HearthMemoryWiring.John.cs:111).
- Ran Tools > Levels > Linda > Add Encore To Custom Kits: log "[EncoreKitTool] Encore added to 0 kit(s) and refreshed in 0. 0 other level(s) still lack it (see the Console)." The menu call returned a TimeoutError at the MCP, but the log line is there.
- After: `md5sum -c` reports OK for all 10 files. No change at all, not even `-0` noise.

## Acceptance criteria

- (a) HearthMemoryJohnTests, HearthMemoryLevelsTests, EncoreKitTests pass: **Not run** (MCP dropped). Implementer ran EncoreKitTests alone earlier: 2 passed.
- (b) Both tool re-runs leave the prefabs unchanged: **Pass** (md5 identical, 10 of 10; Encore tool 0 added, 0 refreshed).
- (c) John prefab objective text and new claw XP bonus: **Pass** by file inspection. Line 2078: `value: 'Defeat four Claws: {dead_0} of 4.'`. `git diff` shows the new claw (fileID 8578014998512379865 override block) adds `lethalDamageXpBonus` value 0; all 5 claws have the override (5 occurrences).
- (d) RuntimeAbilityInitializeTests passes: **Not run** (MCP dropped).

## Bugs found

None in the change. Tooling: Unity MCP `run_tests` unusable in this session (see Tests).

## git status --short -- miso/

```
 M miso/Assets/TextMesh Pro/Resources/Fonts & Materials/LiberationSans SDF - Fallback.asset
 M miso/Assets/_Project/Content/Levels/Generic Levels/Easy/E1/LevelE1-C1.prefab
 M miso/Assets/_Project/Content/Levels/Generic Levels/Easy/E1/LevelE1-C2.prefab
 M miso/Assets/_Project/Content/Levels/Generic Levels/FamilyLevels/LevelLindaJohn-C1.prefab
 M miso/Assets/_Project/Content/Levels/Generic Levels/FamilyLevels/LevelLindaJohn-C2.prefab
 M miso/Assets/_Project/Content/Levels/Generic Levels/FamilyLevels/LevelLindaJohn-C3.prefab
 M miso/Assets/_Project/Content/Levels/Greybox/GB_m3-john.prefab
 M miso/Assets/_Project/Content/Levels/Level1/Level1-C1-2 1.prefab
 M miso/Assets/_Project/Content/Levels/Level1/Level1-C1-2.prefab
 M miso/Assets/_Project/Content/Levels/Level1/Level1-C2.prefab
 M miso/Assets/_Project/Content/Levels/Level1/Level1-C4.prefab
 M miso/Assets/_Project/Core/Systems/AISystem/Runtime/AIFactionBrain.cs
 M miso/Assets/_Project/Core/Systems/AISystem/Runtime/AIUnitBrain.cs
 M miso/Assets/_Project/Features/Onboarding/Editor/HearthMemoryJohnTests.cs
 M miso/Assets/_Project/Features/Onboarding/Editor/HearthMemoryWiring.John.cs
 M miso/Assets/_Project/Features/Player/Linda/Arts/Animations/AC_Playable_Linda.controller
 M miso/Assets/_Project/Features/Player/Linda/Prefabs/Unit_Linda.prefab
 M miso/Assets/_Project/Features/Player/Linda/Scripts/Quiver/Editor/EncoreKitTests.cs
 M miso/Assets/_Project/Features/Player/Linda/Scripts/Quiver/Editor/EncoreKitTool.cs
 M miso/Assets/_Project/Resources/UnitSpecific/Player/Linda/Abilities/Recall/Linda_Ability_Recall.asset
 M miso/Assets/_Project/Scenes/PreloadScreen.unity
 M miso/ProjectSettings/EditorSettings.asset
 M miso/ProjectSettings/ProjectSettings.asset
?? miso/Assets/_Project/Features/Player/Linda/Arts/Animations/Encore.meta
?? miso/Assets/_Project/Features/Player/Linda/Arts/Animations/Encore/
```

Identical to the starting snapshot: no file changed by the tool runs.

## Save reset

no

## Needs THJ

Run Window > General > Test Runner > EditMode > Run All (or read the pass/fail counts), because the MCP could not. Needed: full suite green except `AIRegressionTest.Baseline_MatchesCurrentAI`, plus HearthMemoryJohnTests, HearthMemoryLevelsTests, EncoreKitTests and RuntimeAbilityInitializeTests.

## Editor checks corrections

- Confirmed: `refresh_unity` with `compile: request` works, and the Editor.log has no "Domain Reload Profiling" line at the tail to wait on; poll the log or `read_console` instead.
- New: `execute_menu_item` can return TimeoutError while the menu item still ran (check the log). After menu runs and a domain reload, `run_tests` can fail repeatedly with "session disconnected" and `read_console` with "ping not answered"; the editor's MCP WebSocket reconnect loops. `TestResults.xml` is only written by a completed run (the implementer's earlier one was the only copy).
- A blocked tool: the Bash tool refuses `sleep N`; wait with `timeout N bash -c 'until ...; do sleep 3; done'`.

## Risks and loose ends

- Warnings in `Editor.log` about line 110 of HearthMemoryWiring.John.cs are a stack trace attached to a material warning (m_LightOverlaySprite, 2D SRP Batcher), not a problem with the wiring.
