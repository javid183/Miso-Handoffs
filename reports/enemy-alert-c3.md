# Report: Enemy alert state, C3 (data pass)

Plan: plans/2026-10-23-enemy-alert-state-tech.md (C3)    Agent: miso-implementer    Branch: main (not switched)
Outcome: done (all 3 boss prefabs and all 9 levels done; EditMode 726/727, only the known red fails)

## What changed

Method: a temporary editor script (run once in batchmode with `-executeMethod`, then deleted along with its folder and `.meta`; nothing of it is left in the tree) loaded each prefab with `PrefabUtility.LoadPrefabContents`, added the component to the root, set the one flag through `SerializedObject`, and saved. Hand YAML was not needed. All files LF, no BOM, unchanged by the save.

Every level is a prefab variant of `LevelBase`, so the component is stored as a prefab-instance added component on the root (`m_AddedComponents` entry targeting the `LevelBase` root GameObject, plus a stripped GameObject doc and the MonoBehaviour doc). The root is the object that carries `Level`. Each level diff is 25 lines: that block only. Unit prefab diffs are the same pattern (added component on the root, 18 lines; `Unit_TobaEnemy` 27 lines because it also gets a stripped-GameObject fixup).

Boss prefabs (`EnemyAlertSettings`, `alwaysAlert = true`), under `miso/Assets/_Project/Features/`:
- `Enemy/Goblin Queen/Prefab/Unit_GoblinQueen.prefab`
- `Enemy/Mountain Deev/Prefabs/Unit_Deev.prefab`
- `Player/Dom/Prefabs/Unit_TobaEnemy.prefab`: the duel's enemy Toba is its own variant (`Unit_TobaEnemy`, separate from `Unit_Toba_Ally` and `Unit_Toba`), and `LevelDomFight` uses it. So the flag is on the prefab, not on the level instance. The allied Toba is untouched.

Levels (`LevelAlertSettings`, `allEnemiesStartAlert = true`), under `miso/Assets/_Project/Content/Levels/`. Each path confirmed from the Mission asset's level list, the units in the level and its objective text:
- `Level3/Level3-C1.prefab`: M4 Queen boss level (M4 mission; contains `Unit_GoblinQueen`; objective "Eliminate all enemies").
- `Generic Levels/Medium/M2/LevelM2-C1.prefab`: M10 (The Parasite mission lists only this level; has `Unit_GoblinQueen`, 3 placeholder units, 4 spawners).
- `Generic Levels/Medium/MountainDeev/LevelMountainDeev.prefab`: M12 (sole level of the mission; `Unit_Deev`).
- `Level2/Level2-C2.prefab`: M4 protect level ("The stag must survive", "Reach the Pathmother").
- `Level2/Level2-C3-1.prefab`: M4 escort ("Escort the fawns out", "Pathmother must survive").
- `Level2/Level2-C3-2.prefab`: M4 escort ("Escort the fawns out / new pathmother to safety").
- `Generic Levels/FamilyLevels/MarkIntro/LevelMarkIntro-C1.prefab`: M3 Mark Intro C1 ("Survive N turns", turn-reached condition).
- `Level2/LevelDomFight.prefab`: the Dom duel ("Defeat the stranger!"; `Unit_TobaEnemy`).
- `Generic Levels/Easy/LevelHomeDefence.prefab`: "Defend Home".

Line endings: the two files the coordinator asked to convert (`Runtime/EnemyAlertTracker.Visuals.cs`, `Editor/EnemyAlertVisualTests.cs`) were already LF with no BOM when I checked (0 CR bytes, no BOM, verified by byte count; I rewrote them with LF anyway, content identical). All 10 `.cs` files in the folder are LF, no BOM. No C1/C2 code was changed.

## Skipped

None skipped. Every name matched exactly one level. Two to double-check:
- "M4 Queen level" resolved to `Level3/Level3-C1` (the only M4 level with the Goblin Queen).
- M10's only level is `LevelM2-C1`, which also holds the Goblin Queen (the file name says M2 but it is the generic Medium level M10 uses). If M10 is meant to be a different Parasite boss level, this is not it.

## Suggestions (not changed)

Levels whose objective suggests enemies should come from turn 1, by objective text and condition types:
- `Generic Levels/FamilyLevels/MarkIntro/LevelMarkIntro-C3.prefab`: "Survive for 3 turns" (same pattern as C1). Strongest candidate, likely an oversight.
- `Generic Levels/FamilyLevels/MarkIntro/LevelMarkIntro-C2.prefab` (and `_BKP`): "Leave the area to reach Lucy". Enemies may need to chase the family.
- `Level1/Level1-C3.prefab` (also `Level1-C3 1`, `New Temp Levels/Level1-C3 - Test Khashayar`): "Allies must survive".
- `Level2/Level2-C1-TArtEx.prefab` (M4): "All units reach the exit". Reach-the-exit, not timed; probably fine Unaware, a design call.
- `Level2/Level2-C3-old.prefab`: same objectives as C3-1/C3-2 but not in any mission; leave unless it returns.
- DungeonSafeRooms (reach-the-exit rooms): probably fine as is.
- The M4 `Level2-C1`, `LevelM1-*`, `E*`, `T1` Masher level: plain "eliminate all"; Unaware is the intent there.

## Acceptance criteria (C3 part)

- [x] `alwaysAlert` on Goblin Queen, Mountain Deev, duel Toba: three prefab diffs.
- [x] `allEnemiesStartAlert` on the 9 listed levels, paths confirmed above.
- [ ] Play check (a bosses level starts alert, a flagged level starts alert, an unflagged level starts Unaware): not run; needs THJ.

## Test results

Batchmode, Unity 6000.3.4f1, editor closed. Scratch dir `C:\Users\javid\AppData\Local\Temp\claude\E--Work-Projects-miso\4a7b2e15-2aac-45e7-9e97-b6e33d04e813\scratchpad` (`results.xml`, `test.log`, `c3run.log`, `c3run2.log`). 727 tests, 726 passed, 1 failed: `AIRegressionTest.Baseline_MatchesCurrentAI` (known red; its log shows its usual `HandleLivingUnitsCondition` NRE and "ability missing" lines, unrelated). No missing-script or compile errors on the edited prefabs in the test log or the two data-run logs.

Import noise: during the first data run, saving `Level3-C1` and `LevelDomFight` logged a `NullReferenceException` from `Mission.UpdateLevelsInMission` (`Mission.cs` line 138, a `Mission.OnEnable` that reads a level during reimport). It is existing code reacting to a level being reimported; the second run (all levels already saved) had none. Not touched. The saved prefabs are intact.

No asset other than the 12 listed changed (`LevelBase.prefab`, `AIController.prefab`, tag assets etc. remain the C1 working-tree diffs; `LevelBase.prefab` still 13 lines).

## Save reset

No.

## Decisions I made

- Editor script instead of hand YAML (the allowed alternative), because added components on a variant also need a stripped GameObject doc.
- Flag on the `Unit_TobaEnemy` prefab rather than the level instance, since it is not shared with the ally.

## Needs THJ

None blocking. Confirm that M10 is `LevelM2-C1` and M4's Queen level is `Level3-C1` as listed above, and look at the suggestions (MarkIntro C3 first).

## Docs to update

- `design/gdd/missions` level list (designer): add the flagged levels above.

## Risks and loose ends

- This commit uses `EnemyAlertSettings` and `LevelAlertSettings`, so it **depends on the held C1 commit 2 (and C2)**. Committed alone, the prefabs would reference missing scripts. Commit it after them.
- `Unit_GoblinQueen` and `Unit_Deev` are used wherever they are placed, so `alwaysAlert` applies in every level with a Queen or Deev, not just the boss levels.

## Proposed commits

1. `feat(levels): boss units and objective levels start enemies alert` (data only, plain): the 3 unit prefabs and 9 level prefabs listed under "What changed". No new `.meta` files. Commit after the held C1/C2 commits; do not include `LevelBase.prefab` or `AIController.prefab`, which belong to C1 commit 2.

## Other branches

`thj/home-test` needs this when it takes `main` (same as the rest of the feature).

## How to see it

1. Open `Level3-C1` (M4 Queen) in Play: all enemies should act from turn 1, no Unaware markers.
2. Open a plain level (for example `LevelM1-C1`): enemies start Unaware with the marker.
3. Select `Unit_TobaEnemy` in the Project window: `EnemyAlertSettings` shows Always Alert ticked. On `LevelHomeDefence` the root shows `LevelAlertSettings` with All Enemies Start Alert ticked.
