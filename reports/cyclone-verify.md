# Report: Cyclone redesign, final gate check (C1a to C5)

Plan: plans/2026-11-11-cyclone-redesign-tech.md    Agent: miso-qa    Branch: thj/cyclone (all uncommitted)
Outcome: done. Result: **PASS** (quiet checks only; no play session, so every play check stays with THJ).

## Compile

Clean. Forced refresh plus compile request, then the console read: 0 `error CS`, 0 `warning CS`. The only console warnings are the usual serialization-depth warnings (StatBackedValueBase, GTag.subTags), none from Cyclone files, and the expected log lines the tests print ("Cyclone not cast: ...", "reached its activation frame without targets").

## Tests

Full EditMode suite via MCP: **2016 run, 2015 passed, 1 failed, 0 skipped** (200 s). The one failure is `AIRegressionTest.Baseline_MatchesCurrentAI`, 714 checks, **43 inner failures**, as expected and unchanged. It lists `Lucy_Ability_Steer.asset` as a new ability not in the baseline, which is the known drift. Not re-baselined. No other failures.

## Acceptance criteria (gate)

- [x] Compile clean: see above.
- [x] Full suite green except the known red: 2015/2016, 43 inner failures as expected.
- [x] File coverage: every changed or new Cyclone file is named by a commit below; no named file is unchanged; no missing `.meta` (details below).
- [x] Commit order: written below, no file in two commits.
- [ ] Play checks (Whirl pull, Steer, Gust, wake on pull, blocked archers backing off, etc.): Not run, needs a play session.

## File coverage

`git status --porcelain -uall -- miso`, compared with the union of the reports' latest proposed commits (the C5 fix round moved `EnemyAlertForcedMoveTests.cs` from F to G).

- (a) Changed files no commit names: only THJ's own `PreloadScreen.unity`, `ProjectSettings/EditorSettings.asset`, `ProjectSettings/ProjectSettings.asset` and the TMP fallback font. Nothing else.
- (b) Files a commit names that aren't changed: none.
- (c) Missing `.meta`: none. Every new `.cs`, asset and the new `Scripts/Cyclone/` folder (`Cyclone.meta`) has its `.meta`; no orphan metas.
- (d) Reimport noise: none left. During the test run a transient `Content/Levels/Greybox/__CameraStartTest/` folder (with its `.meta` and `NoLocatorTemplate.prefab`) showed up in `git status`; `GridToLevelCameraStartTests` creates and deletes it, and it was gone when the run ended. Don't stage it if it appears mid-test.

## Final commit order

All paths under `miso/Assets/_Project/`. Each `.cs` and asset takes its `.meta`. Order: **E1, A, A2, B, D1, F, C1 1 to 8, C, D2, D3, E2, E3, G** (20 commits).

1. **E1** `feat(core): enemy shots check a grid line of fire, so a projectile can't be fired along a line crossing a cell that blocks the shooter's faction`
   `Core/Systems/GridSystem/Runtime/GridLineOfFire.cs`, `Core/Systems/AbilitySystem/Effects/Runtime/AEffectSpawner.cs`
2. **A** `feat(core): a planted entity can let units of chosen relations to its owner path through its cell without stopping there`
   `Core/Entities/Runtime/OnGridEntity.cs`, `Core/Systems/GridSystem/Runtime/GridCell.cs`, `Core/Systems/GridSystem/Runtime/GridCell.PlantedPass.cs`
3. **A2** `fix(core): a dash attack and the Mark and Linda duo never stop short on a cell that can only be passed through`
   `Core/Systems/AbilitySystem/Effects/Runtime/AEffectDashAttack.cs`, `Core/Systems/AbilitySystem/Abilities/Runtime/UnitsCooperationHandler.cs`
4. **B** `feat(core): the AI keeps its units off ground that hurts them at turn end unless they can attack from there, never picks a shot with a blocked line of fire, and moves ranged units to cells with a clear shot`
   `Core/Systems/AISystem/Runtime/`: `AIEndOfTurnDanger.cs`, `AILineOfFire.cs`, `AIBlackboard.cs`, `AIFactionBrain.cs`, `AIUnitBrain.cs`, `AIUnitBrain.EndOfTurnDanger.cs`, `AIUnitBrain.LineOfFire.cs`
5. **D1** `feat(core): an ability effect can supply its own target cells, used by the range highlight and the target check`
   `Core/Systems/AbilitySystem/Effects/Runtime/ITargetSelectionRangeProvider.cs`, `Core/Interactions/Runtime/FactionControllerBase.cs`
6. **F** `feat(core): the enemy alert tracker can wake an Unaware unit that a forced move by the player's side moved`
   `Core/Systems/EnemyAlertSystem/Runtime/EnemyAlertTracker.ForcedMove.cs` (its test goes in G)
7. **C1-1** `feat(core): report damage dealt outside an ability's span, credited to the ability that left its source on the board`
   `Core/Managers/CombatLevelRunHandler.DamageReport.cs`
8. **C1-2** `feat(core): raise an end-of-turn event after the turn's actions finish so an effect can hold the switch; the hold watchdog ignores paused time`
   `Core/Managers/CombatLevelRunHandler.cs`, `Core/Managers/CombatLevelRunHandler.TurnSwitchHolds.cs`, `Core/Interactions/Editor/TurnSwitchHoldTests.cs`
9. **C1-3** `feat(lucy): the Cyclone stays where it is cast, whirls on cast and at the end of each enemy turn, pulled enemies wake, shows its cross and pips, casts only on an empty cell; carries the Steer and Gust code`
   - `Features/Player/Lucy/Scripts/Cyclone.meta` and these files in `Features/Player/Lucy/Scripts/Cyclone/`: `AEffectCycloneSpawner`, `AEffectCycloneSteer`, `CycloneButtonSwap`, `CycloneCrossView`, `CycloneEntity`, `CycloneEntity.Ready`, `CycloneEntity.Steer`, `CycloneEntity.Whirl`, `CycloneHitContext`, `CyclonePipsView`, `CycloneRegistry`, `CycloneRules`, `CycloneSprites`, `CycloneSteerPreview`, `CycloneSteerRules`, `CycloneSteerSteps`, `CycloneWhirlPlanner`, `CycloneWhirlSteps`, `ICycloneSteerSteps`, `ICycloneWhirlSteps` (.cs each; NOT `CycloneEntity.AIDanger.cs` or `CycloneEntity.LineOfFire.cs`)
   - `Features/Player/Lucy/Scripts/Editor/CycloneAnchoredSetup.cs`
   - `Features/Player/Lucy/Prefabs/Cyclone.prefab`
   - `Resources/UnitSpecific/Player/Lucy/Abilities/Cyclone/`: `Lucy_Cyclone_Effect_Spawn.asset`, `Lucy_Cyclone_Ability.asset`, `Lucy_Cyclone_Whirl_Pusher.asset`
10. **C1-4** `test(lucy): Cyclone life, cast, Whirl, hit-context and grid-entity lifetime tests`
    `Features/Player/Lucy/Scripts/Editor/`: `CycloneTestGrid.cs`, `CycloneLifeTests.cs`, `CycloneCastTests.cs`, `CycloneWhirlTests.cs`, `CycloneHitContextTests.cs`, `GridEntityLifetimeTests.cs`
11. **C1-5** `chore(core): reset the live Cyclone list between play sessions`
    `Core/Managers/PlayModeStaticReset.cs`
12. **C1-6** `fix(lucy): Super Time casts the Cyclone only on an empty cell and skips with a warning when none is free or hers is already out`
    `Features/Player/Lucy/Scripts/LucyFactionRoleHandler.cs`
13. **C1-7** `fix(onboarding): the sisters' tally counts each kill once, and Cyclone kills count through the damage report`
    `Features/Onboarding/SistersTally/SistersTallyListener.cs`, `Features/Onboarding/SistersTally/Editor/SistersTallyTests.cs`, `SistersTallyTests.Attribution.cs`, `SistersTallyTests.Whirl.cs`
14. **C1-8** `fix(masher): the reckless counter ignores hits from Lucy's Cyclone`
    `Features/Enemy/Masher Goblin/Scripts/MasherCounterRules.cs`, `Features/Enemy/Masher Goblin/Scripts/MasherGoblinFactionRoleHandler.Counter.cs`, `Features/Enemy/Masher Goblin/Editor/MasherCounterWhirlTests.cs`
15. **C** `feat(lucy): the family passes through the Cyclone and enemies treat its cross as dangerous ground`
    `Features/Player/Lucy/Scripts/Cyclone/CycloneEntity.AIDanger.cs`; in `Features/Player/Lucy/Scripts/Editor/`: `CycloneTestFactions.cs`, `CyclonePassTests.cs`, `CycloneAIDangerTests.cs`, `CycloneStopShortTests.cs`
16. **D2** `feat(lucy): while her Cyclone is out, Lucy's Cyclone button becomes Steer: 1 AP once a turn, up to three straight cells through the family, then a Gust pulls enemies on its arms one cell in, with an aim preview`
    `Features/Player/Lucy/Scripts/LucyCycloneProjectileScatter.cs`, `Features/UI/Panels/Scripts/AbilitiesBarHUDUI.cs`, `Features/UI/Panels/Scripts/AbilitiesBarHUDUI.CycloneSteer.cs`, `Features/Player/Lucy/Scripts/Editor/CycloneSteerSetup.cs`, `Resources/UnitSpecific/Player/Lucy/Abilities/Cyclone/Lucy_Ability_Steer.asset`, `Lucy_Ability_Steer_Effect_Steer.asset`, `Features/Player/Lucy/Prefabs/Unit_Lucy.prefab`
17. **D3** `test(lucy): Steer rules, Gust, button swap, ready refresh, scatter and AI danger after a Steer`
    `Features/Player/Lucy/Scripts/Editor/CycloneSteerTests.cs`
18. **E2** `feat(ui): threat previews leave out cells an enemy shot can't reach because its line of fire is blocked`
    `Core/Interactions/Runtime/UnitThreatAnalysis.cs`
19. **E3** `feat(lucy): the Cyclone stops enemy shots whose grid line crosses its cell; the family's arrows still pass`
    `Features/Player/Lucy/Scripts/Cyclone/CycloneEntity.LineOfFire.cs`, `Features/Player/Lucy/Scripts/Editor/CycloneLineOfFireTests.cs`
20. **G** `chore(lucy): Howling Gale's text says it hits every enemy the Whirl hits and the unlock list names the upgrade; tests for the forced-move wake and Howling Gale`
    `Resources/RunUpgrades/LucyCycloneWeak/RU_LucyCycloneWeak.asset`, `Resources/Unlockables/UnlockableSet.asset`, `Features/Player/Lucy/Scripts/Editor/CycloneHowlingGaleTests.cs`, `Core/Systems/EnemyAlertSystem/Editor/EnemyAlertForcedMoveTests.cs`

Flags:
- No file appears in two commits. `CombatLevelRunHandler.TurnSwitchHolds.cs` sits whole in C1-2 (event plus watchdog fix together, so no hunk staging), and `CycloneTestGrid.cs` only in C1-4.
- `EnemyAlertForcedMoveTests.cs` is in G, not F, because it needs `CycloneTestGrid` from C1-4.
- `CycloneEntity.AIDanger.cs` and `CycloneEntity.LineOfFire.cs` live in the `Cyclone/` folder but are excluded from C1-3; stage the folder by file name, not by wildcard.
- E3 needs `CycloneTestFactions` (C), `CycloneTestGrid` (C1-4), E1, B and E2; the order satisfies all of them.
- Only the final tree was compiled and tested; the order was not built commit by commit.

## Bugs found

None.

## Save reset

No.

## Editor checks corrections

none. Note for the file: over MCP the test job runs in the background with the editor unfocused; the failed-test output is huge, so read the saved result with python (`jq` isn't installed).

## Decisions I made

- Treated the transient `__CameraStartTest` folder as test-run noise, not a stray change.

## Needs THJ

The play checks listed in the chunk reports. Each commit still needs THJ's yes.

## Docs to update

none

## Risks and loose ends

- The baseline red now also lists the new Steer ability; re-baselining stays a dedicated session.

## Proposed commits

See "Final commit order" above (QA proposes none of its own).

## Other branches

none

## How to see it

Nothing new for THJ to open; play checks are in the chunk reports.
