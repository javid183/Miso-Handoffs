# Report: M3 "Hold the yard" round two

Plan: plans/2026-11-26-m3-redesign-build-tech.md    Agent: miso-implementer    Branch: main
Outcome: partial (chunk 7.1 done; 7.2, the lines, is a later run)

## What changed

Paths under `miso/Assets/_Project/`. Every `.cs` file is LF with no BOM, like the rest of `Features/Onboarding` (checked by byte count and `git ls-files --eol`).

Code:
- `Features/Onboarding/HoldUnitsUntilSignal.cs`: new serialized option `holdFromLevelStart` (default off). On: the hold is in place in `Start` and on the level-started event, both before the first `StartTurn`, and the first turn start catches a missed start. Off: unchanged.
- `Features/Onboarding/Editor/MissionWiring.HoldTheYard.cs`: rewritten for block `m3-defence-3` (the class comment, `BlockDocument`, tiles, turn order, relations, five stages, the Mark defeat group). `Build Level` now moves the old greybox to `_v1` first.
- `Features/Onboarding/Editor/MissionWiring.HoldTheYard.Stone.cs`: five variants; the level's stone instances go into Stranger.
- `Features/Onboarding/Editor/MissionWiring.HoldTheYard.Sequences.cs`: rewritten. The opening camera tour, four notches, the outro. Sequences live in a new folder, `Resources/Sequences/M3Yard`.
- `Features/Onboarding/Editor/MissionWiring.HoldTheYard.Mission.cs`: also sets the Trail's free seats to 0.
- `Features/Onboarding/Editor/MissionWiring.HoldTheYard.Barricades.cs` (new): the barricade prefab and the six placements.
- `Features/Onboarding/Editor/MissionWiring.HoldTheYard.Mark.cs` (new): Mark's tags, his Family Role switched off, the hold.

Tests:
- `Features/Onboarding/Editor/M3DefenceTests.cs`: rewritten, 44 tests.
- `Features/Onboarding/Editor/HoldUnitsUntilSignalTests.cs`: now `partial` (one word).
- `Features/Onboarding/Editor/HoldUnitsUntilSignalTests.LevelStart.cs` (new): 7 tests for the option.
- `Features/Onboarding/Editor/PickFallenLOConditionTests.cs` (new): the three condition tests that lived in `M3DefenceTests`, moved so the kept class keeps its coverage.
- `Core/Levels/Editor/OnboardingMissionGraphTests.cs`: the Trail's free seats are 0 (test file only, not a core system).
- `Features/Onboarding/Editor/SearchTrailTests.cs`: same; test renamed `TheRosterIsTheSistersWithNoFreeSeatAndTheItemsArePacked`.
- `Features/Onboarding/Editor/PickOnTilesLOConditionTests.cs`: dropped the "a free seat for the pick" assert (it read the Trail).

Assets (all written by the menus):
- `Content/Levels/Greybox/GB_m3-defence.prefab` (+ .meta, new GUID `156db430…`): the new level. `git diff --numstat`: +5473 / −2720 (8979 lines). Git shows it as modified because the path is reused.
- `Content/Levels/Greybox/GB_m3-defence_v1.prefab` (+ .meta): the old level, moved with `AssetDatabase.MoveAsset`. Byte-identical to HEAD's `GB_m3-defence.prefab` and `.meta` (`cmp`), so GUID `42d09f99…` is kept. Git sees a rename once both sides are staged.
- `Features/NPCs/Rock/Prefabs/Unit_Barricade.prefab` (+ .meta, 67 lines): variant of `Unit_Rock`.
- `Features/NPCs/Rock/Prefabs/Unit_Rock_Stone4.prefab` (+ .meta, 67 lines): the fifth stone.
- `Resources/Sequences/M3Yard.meta` + `Resources/Sequences/M3Yard/` (43 assets + .meta).
- `Content/Levels/M2 - The Trail.asset`: `freeSlotsCount` 1 → 0, and the graph payload points at the new level (2 lines).
- `Content/Levels/Greybox/GB_m1-ridge.prefab`: +1 line, `holdFromLevelStart: 0`. This is Unity writing the new field's default when something re-saved the prefab during this run (the Ridge tests or menus). M1's behaviour is unchanged. It can go with commit 1 or be left out.

Untouched: `Unit_Rock.prefab`, `Unit_Rock_Stone0..3.prefab`, the old `Resources/Sequences/M3Defence/` (still used by `_v1`), THJ's files (`LevelM2-C1.prefab`, `PreloadScreen.unity`, `ProjectSettings/*`, `DUO/Inserts/`, the TMP fallback font, `M3Defence_Notch3_HideLastStone.asset`). No core file changed.

## Acceptance criteria

See Chunk 7.1 below.

## Chunks

### Chunk 7.1: level, barricades, Mark, stone, stages, roster

**Built, in the plan's order:**
1. The hold option and its tests.
2. The barricade prefab, the fifth stone and the stone faction.
3. `Build Level` (moved the old level to `_v1`, then built 82 tiles and 15 placements), then `Apply Wiring`.
4. The tests.

`Apply Wiring` was run twice. After the second run all 53 written files were byte-identical (md5): the level, `_v1`, the mission, the six rock variants, the barricade, `Unit_Rock` and the 43 sequences. The second run logged no warning and no mission change.

**Criteria**

*Prefabs*
- [x] Old level renamed `GB_m3-defence_v1.prefab` with `MoveAsset`, GUID kept. Test: `TheEarlierGreyboxIsKeptUnderItsOwnName`; `cmp` against HEAD.
- [x] New `GB_m3-defence.prefab` built from `m3-defence-3` with the builder. 4,10 is plain floor, and w3's east Claw is on 8,2. Tests: `TheTilesAndUnitsMatchThePaperBlock`, `JohnsDrawnTileIsPlainFloor`, `TheBuildBlockParsesCleanWithTheLevelLines`.
- [x] Read-back matches (below).
- [x] The mission graph points to the new prefab, and the mission keys still work. Tests: `TheTrailMissionPlaysThisLevelAlone`, plus the unchanged `HomeVisitsTests` (Yard chain, clue scene, home state, station unlocks), `M4WhiteMothersTests` (Toba's button) and `BondSourcesTests`.

*Roster*
- [x] `freeSlotsCount` 0; the fixed seats stay Linda and Lucy. Test: `TheRosterIsTheTwoSistersWithNoFreeSeat`.
- [x] No `Unit_Placeholder`. Tests: `TheSistersStandOnTheirTilesAndNoSlotIsLeftForAPick`, block test.
- [x] Linda 2,8, Lucy 7,8. Same test.
- [x] Pick wiring removed: no pick condition and no `{pick` text anywhere in the level. Test: `NothingOfTheSquadPickIsLeftInTheLevel`. The three condition classes stay, and grep shows they are still used by their own tests. `PickFallenLOCondition`'s tests moved to `PickFallenLOConditionTests.cs`.

*Mark*
- [x] `Unit_Mark` on 4,11, Bergsons, not a roster seat. He comes from the block's `M@` token, placed by the builder. Test: `MarkStandsOnHisTileInTheFamilyAndIsNoRosterSeat`.
- [x] Persistent `EntityState.Unmovable` and `EntityState.Unable to Swap` on the instance, not the prefab. Test: `MarkIsUnmovableUnswappableAndIgnoredByObjectivesOnTheInstanceOnly`. Also `EntityState.IgnoreObjective`, see Decisions.
- [x] Held all level by `HoldUnitsUntilSignal` with `holdFromLevelStart` on, released by nothing. Tests: `MarkIsHeldFromTheLevelStartByOneHold`, the 7 option tests, and the existing 14 hold tests (21/21).
- [x] T-M1 report: Findings below.
- [x] T-M3 report: Findings below. The FP filler lists Linda and Lucy only. Test: `TheFamilyTimePointsAreFilledAtLevelStartThroughTheSistersOnly`.
- [x] T-M4 report: Findings below (yes).

*Barricades*
- [x] `Unit_Barricade.prefab`, a variant of `Unit_Rock`: title "Barricade" (final, D-731), Neutral, Unmovable and Unable to Swap (inherited), no abilities, the unit mini health bar (inherited). Health 8 is set **on the prefab**: the rock's base health attribute reads `baseFactor × Stat_HP`, rock base 1, now 8. The Claw's base is 16. Neutral is never tier-scaled (the tier only scales factions hostile to the family), so a barricade has 8 HP in any level. The placed instances have no factor override. Tests: `TheBarricadeIsANeutralRockTitledBarricadeWithNoAbilities`, `TheBarricadeHasEightHealth`.
- [x] Six barricades on 0,6, 1,6, 2,6, 6,6, 7,6 and 8,6. Test: `SixBarricadesCloseTheTwoNecks`.
- [x] Relations: Enemy–Neutral is Enemy, Bergsons–Neutral is Ally, and `MakeEnemyAndNeutralAllies` is gone. Test: `EnemiesAreHostileToTheBarricadesAndAlliedToTheStone` (runtime `Initialize` on a copy).
- [x] Requirement 3 report: Findings below.
- [x] T-M6 report: Findings below.

*The stone and Toba*
- [x] Stone on 4,12, five variants (`Unit_Rock_Stone4` added). Tests: `TheStoneVariantsAreNeutralRocksTitledStoneEachFurtherToTheSide`, `EachStoneWaitsHiddenOnTheStoneTileInItsOwnGroupInTheStonesFaction`.
- [x] Toba hidden in `toba` on 4,12. Test: `TobaWaitsHiddenUnderTheStone`.
- [x] The stone is no longer Neutral: Stranger, on the level instances. Findings below.
- [x] Test that Enemy–Stranger is Ally and Enemy–Neutral is Enemy in the level, plus `EveryFactionInTheTurnOrderHasAnEnemyList`.

*Enemies and objects*
- [x] Masher at anchor 6,1, factor 0.6. Test: `TheMasherStandsAtTheBottomOfTheEastLaneInPlay`.
- [x] Waves, all Dark Claws at factor 1.0. w1 is in play on 0,1, 1,1 and 2,1; w2 is hidden on 8,0 and 8,1; w3 is hidden on 0,0, 2,0 and 8,2. They come in alert through the level's all-alert setting. Tests: `TheFirstWaveIsInPlayInTheWestLane`, `TheOtherTwoWavesWaitHidden`.
- [x] Mushrooms on 1,4 and 8,4; the Heavenly Sword under 8,10; Early, all alert, FP full. Tests: `TwoMushroomsSitOneRowUnderEachFront`, `OneHeavenlySwordPickupLiesUnderItsTile`, `TheEnemiesAreEarlyTierAllAlertAndTheFamilyMovesFirst`, the FP test.
- [x] Turn order: Bergsons, Enemy, Neutral, Stranger. The stone's faction needs a seat: an unlisted faction added mid-level sorts to index 0 (`IndexForTurnOrder`), and the turn number would tick on its turn. Same test.
- [x] Camera starts on 4,6 (`level camera 4,6`). Test: block parse. The builder warns that 4,6 is not a tile (it is the no-tile centre between the necks); it centres the view on that spot anyway.
- [x] Cleanse and the Linda–Lucy Duo stay locked. Test: `CleanseIsLockedForEveryHeroAndTheSistersDuosForBothSisters`, which also covers Mark's two Duos (see Decisions).

*Stages and defeat*
- [x] S1 to S4: "Hold them off (4)" to "(1)". Each uses the built `TurnReachedLOCondition` and completes at the next family turn start. **Deviation, same behaviour:** `turn` is 1 for each stage, not 2/3/4/5. The condition counts turns since the stage was first checked, not the absolute turn number; see "the stage-condition choice" below. Test: `EachHoldStageIsOneFamilyTurnStart` (×4).
- [x] Stage ends:
  - S1: notch 1, then the w2 arrival.
  - S2: notch 2, then the w3 arrival.
  - S3: notch 3 and Mark's line.
  - S4: notch 4, the roll-away (stone4 hides), then Mark's line.
  - Each runs input off, camera, reveal, bark, camera back, input on.
  
  Test: `EachHoldStageEndMovesTheStoneANotch` (×4).
- [x] S5 "Finish them.": living Enemy ≤ 0, so barricades (Neutral) don't count. Its end is as built, minus the stone hide (the stone has already gone): the tally fade, "Still counting?", Toba revealed, the fade home. Tests: `TheLastStageIsEveryEnemyDead`, `TheOutroFadesTheTallyThenBringsTobaOut`.
- [x] Defeat: the template group stays. A second group, from level start, is `EntitiesDestroyedLOCondition` on Mark with the **shown** objective "Keep Mark standing." (D-733). The pick group is gone. Aggregation is Any. Test: `TheLevelIsLostWhenNoBergsonStandsOrMarkFalls`. "Mark has fallen." is not wired: the loss panel (`MissionEndPanelUI.SetObjectives`) shows each satisfied defeat objective's text (first sentence) as a failed row, plus a generic result line, and there is no per-group defeat message field. So on a loss the panel shows "Keep Mark standing" as failed. A separate "Mark has fallen." needs new plumbing: left for 7.2.
- [x] Level-start cues, in order: input off, stone0 revealed, camera over the Masher, then the east wall, then Mark and the stone, Mark's line, Linda's line, camera back, input on. No John line. Test: `TheLevelStartBringsTheStoneThenShowsTheMasherTheWallAndMark`.

*Lines and code rules*
- [x] Placeholder lines (list below); John's lines are dropped.
- [x] `Build Level` / `Apply Wiring` rebuild and re-wire, and are idempotent (md5 above). The partial files are kept; the barricades and Mark are in new partials; the class comment and `BlockDocument` describe the new block.
- [x] `M3DefenceTests` rewritten: 44 tests covering every listed area.
- [x] No private IDs in code, comments, test names or logs. No core file changed.

**Tests**
- `HoldUnitsUntilSignalTests`: 21/21 (14 existing + 7 new), run before the build.
- Covering set: everything under `MISO.Core.Features.Onboarding.*` and `MISO.Core.Levels.*`, plus `BondSourcesTests`, run after the wiring. **850 passed, 0 failed, 0 skipped.** That includes:

  | Tests | Count |
  |---|---|
  | `M3DefenceTests` | 44 |
  | `HoldUnitsUntilSignalTests` | 21 |
  | `OnboardingMissionGraphTests` | 10 |
  | `SistersTally*` | 166 |
  | `HomeVisitsTests` | 35 |
  | `BondSourcesTests` | 30 |
  | `SearchTrailTests` | 19 |
  | `M4WhiteMothersTests` | 17 |
  | the three pick-condition classes | 7 + 8 + 3 |
  | the M1 Ridge tests | 47 |

  Run synchronously through the Test Runner API from `execute_code`, because the MCP test jobs kept failing to start (see Risks). The wired assets were md5-unchanged after the run.
- Not run: the full suite and `AIRegressionTest` (the coordinator's).

**Read-back** (`python claude-handoff/tools/level_to_grid.py Content/Levels/Greybox/GB_m3-defence.prefab`):

```grid id=src-gb_m3-defence title="Source: GB_m3-defence (offset x+0, y+0)"
_ _ _ _ T _ _ _ _
_ _ _ . M . _ _ _
. . . . . . . . .
. . . . . . . . .
. . L . . . . U .
. . . . . . . . .
. . . _ _ _ . . .
. . . _ _ _ . . .
. * . _ _ _ . . *
. . . _ _ _ . . .
. . . _ _ _ O O c
c c c _ _ _ O O c
c . c _ _ _ . . c
--
note 8,10 DR_PickUp_HeavenlySword
level hidden toba 4,12
level hidden w2 8,0 8,1
level hidden w3 0,0 2,0 8,2
```

Tool notes: Level Defence, 82 tiles, Early, all alert. Objectives: Hold them off (4) (3) (2) (1), Finish them., Keep Mark standing. Placed: 8 Dark Claws, Linda, Lucy, Mark, the Masher, Toba, 2 mushrooms, the sword pickup.

Differences from the drawn block:
- `#` reads as `_`, and `M@` reads as `M` (the `@` is a drawing aid).
- 4,10 has no `J`.
- 8,2 has a `c`, and the w3 hidden list reads 8,2 instead of 8,0.
- The barricades and the stones aren't drawn: "6 prefab GUIDs not in guidmap.json" (Stone0..4 and Barricade); groups stone0..4 read as "a listed unit that is not a placed unit".

Otherwise identical. The template's scenery props (a statue, 3 cave rocks) are sprites only, as before.

**Placeholder lines** (seeded once into new dialogue assets in `M3Yard/`; 7.2 replaces them):
- Level start, Mark: "There's a cave behind that stone. I'll shift it." Linda: "Keep them off him!"
- Notch 1, Lucy: "More from the east!" Notch 2, Linda: "Both sides now!"
- Notch 3, Mark: "It's moving... keep them off me!" Notch 4, Mark: "It's open! The big one's at the wall!"
- Outro, as before: Linda "Still counting?", Lucy "…No.", Toba "You held them. Good." / "I know the way to the Rootwell. And where Ryker is."
- Objectives: "Hold them off (4)" to "(1)", "Finish them.", "Keep Mark standing." (final, D-733). Title "Barricade" (final, D-731).

## Findings ("Report on" and T-M items)

All of these come from reading the code, not from play.

**T-M1: Inactive Mark**
- **His Family Role still fires while Inactive, so I switched it off for this level, with no core code.**
  - Why it would fire: `FactionControllerBase.ApplyFactionRolesIfPossible` picks candidates by `HasFactionRole` and `CheckActivationMoment` only. `ActivateFactionRoleIfFeasible` then checks the FTP cost (`PointConsumer`) and the handler's `CheckFeasibility`. Neither reads the skip-turn tags.
  - `Mark_Ability_Attack_Primary` has an empty `activationTagQuery`. `PlayerController.CanAffordFactionRole` does check `IsUnitTurnSkipped`, but it only feeds the reactive-unit list and the UI.
  - With FP full, an enemy hitting a sister inside his range would fire his Role.
  - The fix, on the level's instance of his `MarkFactionRoleHandler`: `activationPhase` is set to 0 (no phase), so `CheckActivationMoment` is always false, and `showRoleZone` is off, so the Shift view doesn't promise a zone.
  - His prefab is untouched. Test: `MarksFamilyRoleAnswersNoPhaseAndShowsNoZone`.
- **Enemies target him:** yes. AI targets go by faction relation only (Bergsons–Enemy is Enemy). `Status.Inactive` is only in `AIController`'s `objectivesIgnoreTagsQuery`, which filters the AI's own units for objectives, not targets.
- **Next-targets display:** nothing filters Inactive or skipped units out of the AI's predicted targets (`UnitThreatAnalysis`, the AI predict pass), so a Claw planning to hit him should show him. Play check.
- **Pushes, pulls and knocks:**
  - Unmovable is honoured by the Masher's plow (`plowPushableTagQuery`), Lucy's Whirl pull (`pullTagQuery`), the Cyclone heavy rules and `AEffectVortexPull`. Unable to Swap covers swaps. His two Duos with the sisters are locked (see Decisions), so no Duo moves him.
  - **One gap:** `MasherGoblin_Ability_Counter_Effect_Push.asset` has an empty target tag query, and `AEffectPusher` has no tag gate of its own. If Mark stands inside a Masher counter slam's area (a sister next to him hits an adjacent Masher), the push could move him off 4,11 when a free cell lies behind him.
  - The odds are low: the Masher must reach the alcove.
  - Not changed (the Masher's code and data are out of scope). The fix would be a tag filter on that effect asset (an AI ability asset, so `AIRegressionTest` moves).
- John's Shield isn't in this version (no John).

**T-M3: a hero placed outside the roster in a roster mission.** No side effect found that matters.
- `FillRosterSlots`: no placeholder, and the roster's units are already on the board by nickname, so nothing spawns.
- FTP and the family AP pools: `FactionTracker.InitializePoints` builds them from the **roster** (Linda, Lucy), so Mark adds nothing to the FP maximum.
- `PrepareLevel`: `FamilyActionPoints.AssignUnits(_playerUnits)` counts 3 units. That only matters in the Shared AP mode, and `GlobalSettings` is PerUnit. `RunUpgrades.ApplyGrantedToUnits` also applies run upgrades to Mark (harmless).
- XP: the mission's completion XP is a faction resource. Kill XP needs kills, and Mark can't act.
- Bond: `BondLevelListener` pays pairs among the roster squad, Linda and Lucy only.
- Tally: counts the sisters' kills only.
- Party panel: `InitATBGaugeView` runs for every player-faction unit with an ATB gauge, so Mark gets a panel with his HP. The design expects that; how it looks is a play check.
- The FP filler lists Linda and Lucy.
- `PersistUnitStates` stores Mark's state by nickname for the mission run: one level, harmless.
- The template defeat would have counted Mark as standing, so I tagged him `IgnoreObjective` (see Decisions).

**T-M4: does the AI planner read the family's defeat group? Yes.**
- `AIController.PrepareObjectives` hands the planner `LevelObjectives.ActiveObjectives`, which is the active win group plus **all** defeat groups.
- `EntitiesDestroyedLOCondition` has a handler (`HandleEntitiesDestroyedCondition`), which adds a Cell-type influence subject on Mark from level start.
- The template defeat (`LivingUnits` Bergsons ≤ 0) already made every living family unit an influence subject, Mark included: the planner uses `AliveUnits` without the ignore query.
- So every enemy is drawn toward Mark as well as the sisters. The design assumed nothing draws them to him. Reported, not changed. The old pick-fallen condition was a custom type the planner skipped, so this pull is new compared with the greybox.

**Requirement 3: no family effect damages a Neutral unit.** Neutral is the family's ally here.
- Family targeted abilities need an Enemy target (`PassesTargetFactionRelation`), so the barricade can't be picked.
- Area hits go through `AEffectCompound.targetFactionRelation`. Every family, Duo and relic compound whose relation includes allies (value 1 or 3) is a walk, teleport, pass-by buff, barrier, heal, John's Shield or AP transfer: none deals damage. Linda's and Lucy's attacks, Crescendo, the Heavenly Sword and the Duos are Enemy-only.
- Lucy's Whirl and burst hit `CycloneRules.IsEnemyOf(caster)` only.
- Linda's Watch and Lucy's follow-up pick from `GetFactionEnemies(Bergsons)` (not Neutral).
- **Effects that hit all factions:**
  - `Linda_Toba_LINDA_Duo_Ability_Effect_HitCompound` (relation 3), the Linda–Toba Duo. Toba only appears in the outro, so it can't be used here.
  - The mushroom blast, `MushroomExplosionCompoundEffect` (relation −1, everything). No barricade is in a mushroom's ring (rows 3..5).

**T-M6: damage at Early, before crits and evasion.**
- Enemy `Stat_DMG` at Early is ×0.75. `RuntimeAAttribute` rounds each change with `Mathf.Round`, which rounds half to even.
- **Claw:** 6 × 0.75 = 4.5, rounded to **4**. Two hits break an 8 HP barricade.
- **Masher slam:** base 8 × 0.75 = **6**, not the 7.5 the design assumed. Two slams break a barricade, not one or two. A crit would make it one.
- If the design wants a one-slam break, the levers are barricade HP 6 or the Masher's damage. THJ tunes it in play.

**The stone's faction: Stranger, set on the level's five stone instances. The variants stay Neutral.**
- Why Stranger: `LevelBase` has Stranger as an ally of Bergsons, Enemy and Neutral. Nobody targets it, and it counts for no objective. (Enemy would block "Finish them"; the family's faction would put a unit in the party.)
- Why on the instances: it leaves `Unit_Rock` (M1) and the `_v1` greybox's Neutral stones exactly as they were.
- The Ridge lesson: Stranger had no Enemy entry, so `GetFactionEnemies(Stranger)` would throw. `GUnit.UpdateFaceDirection` calls it on any unit, and the AI calls it for a present faction.
  - The stone comes in at level start through the reveal, which adds a Stranger controller mid-level.
  - I set **Neutral–Stranger to Enemy**, as M1 does for Neutral. Neither side has an ability, so nothing comes of it.
  - Test: `EveryFactionInTheTurnOrderHasAnEnemyList`.
- Stranger is also last in the turn order, so its mid-level controller doesn't sort first.
- The console check at level start in Play (no `KeyNotFoundException`) is still the verifier's.

**The stage condition: the built `TurnReachedLOCondition`, with `turn = 1` per stage.**
- `TurnReachedLOCondition.EvaluateInternal` counts `TurnNumber − the turn at the stage's first check`.
- Only the active queued group is evaluated (`TryEvaluateWin`), so a stage starts counting when it becomes active:
  - S1 is first checked at turn 1 (`StartLevelIE` sets `_turnNumber = 1`, then `StartTurn` and `UpdateObjectives`; nothing evaluates objectives before that).
  - Each later stage is first checked by `WaitThenEvaluateNewStage` right after the previous stage's sequence ends, still in that family turn.
  - The turn number ticks at the family turn start (the family is index 0 in the order).
- So each stage completes at the next family turn start: turn 2, 3, 4 and 5, as the plan wanted.
- No feature-side condition was needed.
- Edge case: if a stage's notch sequence ran past the end of the family's turn into the next turn number, that stage would count from there. That can't happen while the sequence holds input. Play check.

**The reveal on 8,2.**
- `HiddenLevelUnits.RevealUnit` plugs the unit into its cell with `cell.PlugEntity`, which falls back to the nearest free cell when someone stands there. With no free cell, the unit is switched off again with a warning.
- By enemy turn 2 a w2 Claw has usually walked up the lane, but one may still stand on 8,2 (the Masher's 6..7 × 1..2 footprint is beside it). w3's east Claw then comes in on a neighbour. That is cosmetic.
- The same applies to Toba on 4,12 in the outro: the stone has gone at notch 4, so an enemy could have walked onto 4,12 before the win. With every enemy dead by then, the tile is free.

## Reviews and checks

- (coordinator)

## Save reset

No.

## Decisions I made

- **Mark's Family Role switched off on his level instance** (`activationPhase` 0, `showRoleZone` off). The plan asked me to report how; the play check needs it off, and it needs no core code, so I did it. Easy to revert (one method in `MissionWiring.HoldTheYard.Mark.cs`).
- **Mark's Duos with the sisters locked** (`Mark_Linda_Duo_Ability`, `Mark_Lucy_Duo_Ability`, for both sisters, through the existing `LevelAbilityLock`). The plan didn't mention them. A Duo would move Mark off the stone; Inactive and Unmovable don't stop his own Duo move. **Coordinator: confirm.**
- **`EntityState.IgnoreObjective` on Mark's instance**, so the template's "no playable Bergson standing" defeat still fires when both sisters fall. Without it, held Mark counts as standing: the family's turns would end empty until the enemies killed him. It doesn't change the Mark defeat (`EntitiesDestroyed`, no tag filter) or the AI pull. **Coordinator: confirm.**
- `TurnReachedLOCondition` with `turn = 1` per stage instead of 2/3/4/5: same behaviour, see Findings.
- Barricade HP on the prefab (base 8), not a per-instance factor.
- Stone faction set on the level instances; Neutral–Stranger made Enemy so Stranger has an enemy list; Stranger added last to the turn order.
- Round two's sequences go in a new folder, `Resources/Sequences/M3Yard` (`M3Yard_*`). The wiring never overwrites an existing step list or dialogue (`WiringSeed`), and the `_v1` greybox still uses the old `M3Defence/` assets.
- `Build Level` does the `_v1` move. `Apply Wiring` refuses to run until both files exist, so it can never wire the old level by mistake.
- The yard framing in the sequences uses 4,8 (the yard's middle). The camera-start tile 4,6 has no GridCell to read a position from.
- `PickFallenLOCondition`'s three tests moved to their own file, so the kept class keeps its coverage.
- Mark comes from the block (`M@`), placed by the builder, not by the wiring.

## Needs THJ

none (the two "confirm" items above are for the coordinator; both are reversible data)

## Docs to update

- `tech/level-tools.md` "Built so far": `GB_m3-defence` is block `m3-defence-3`; `GB_m3-defence_v1` is the old greybox.
- `tech/onboarding-merge.md` M3 rows: the barricade, the `_v1` rename, `Unit_Rock_Stone4`, the Trail with no free seat.
- `reward-tools`' `guidmap.json`: add `Unit_Rock_Stone0..4` and `Unit_Barricade` if the read-back should name them.
- Design (`miso-game-designer`): T-M6 says the Masher slam is 6, not 7.5.

## Risks and loose ends

- **The AI pull toward Mark (T-M4):** every enemy is drawn to him by both defeat groups. That may make the hold harder than the design expects. Watch it in the play check.
- **The Masher's counter push can move Mark** (T-M1, gap above). Low odds; fixing it means touching an AI ability asset.
- **The Masher's close-up** plays on first sight (`EnemyIntroductionController`), and the opening camera tour shows the Masher too. They may overlap. Play check.
- **Builder warning:** the camera tile 4,6 has no tile; the view is still centred there.
- **`TurnReached` edge case:** a notch sequence that outlasts the family turn would delay the next stage by a turn. Play check.
- **AI regression:** not run, as asked. Expect about +2 "unexpected unit" lines (`Unit_Barricade`, `Unit_Rock_Stone4`) against 50. No AI graph or ability changed.
- **The full EditMode suite:** not run by me (the coordinator's). One note for that run: twice, the Unity MCP test jobs failed to start and left the editor in an untitled scene with only a Main Camera, marked dirty (the Test Runner's own temporary scene). I left it alone and ran the tests synchronously through the Test Runner API from `execute_code`. THJ's previously open scene may need reopening.
- **Unused asset from the earlier build:** `Resources/Sequences/M3Defence/M3Defence_Notch3_HideLastStone.asset` (+ .meta) is still unused. Don't stage it.
- **`GB_m1-ridge.prefab`:** +1 line from the field default (see What changed).

## Proposed commits

1. `feat(onboarding): a held unit can be held from level start` (plain)
   - `Features/Onboarding/HoldUnitsUntilSignal.cs`
   - `Features/Onboarding/Editor/HoldUnitsUntilSignalTests.cs`
   - `Features/Onboarding/Editor/HoldUnitsUntilSignalTests.LevelStart.cs` (+ .meta)
   - optional: `Content/Levels/Greybox/GB_m1-ridge.prefab` (the field's default only)
2. `feat(onboarding): Hold the yard round two: barricades, Mark on the stone, the Masher in the east lane` (plain; depends on 1)
   - the levels: `Content/Levels/Greybox/GB_m3-defence.prefab` (+ .meta), `Content/Levels/Greybox/GB_m3-defence_v1.prefab` (+ .meta). Git sees these as a rename plus a new file.
   - the units: `Features/NPCs/Rock/Prefabs/Unit_Barricade.prefab` (+ .meta), `Features/NPCs/Rock/Prefabs/Unit_Rock_Stone4.prefab` (+ .meta)
   - the sequences: `Resources/Sequences/M3Yard.meta`, `Resources/Sequences/M3Yard/` (43 assets + .meta)
   - the mission: `Content/Levels/M2 - The Trail.asset`
   - the wiring: `Features/Onboarding/Editor/MissionWiring.HoldTheYard.cs`, `.Stone.cs`, `.Sequences.cs`, `.Mission.cs`, `.Barricades.cs` (+ .meta), `.Mark.cs` (+ .meta)
   - the tests: `Features/Onboarding/Editor/M3DefenceTests.cs`, `Features/Onboarding/Editor/PickFallenLOConditionTests.cs` (+ .meta), `Features/Onboarding/Editor/PickOnTilesLOConditionTests.cs`, `Features/Onboarding/Editor/SearchTrailTests.cs`, `Core/Levels/Editor/OnboardingMissionGraphTests.cs`
3. `feat(onboarding): M3 lines` (7.2)

Not to stage: THJ's `LevelM2-C1.prefab`, `PreloadScreen.unity`, `ProjectSettings/*`, `Content/FamilySuperTime/DUO/Inserts/`, `TextMesh Pro/.../LiberationSans SDF - Fallback.asset`, `M3Defence_Notch3_HideLastStone.asset` (+ .meta), and any `Content/Levels/Greybox/__CameraStartTest/` a test run leaves behind.

## Other branches

none (`thj/onboarding-demo` is merged into `main`)

## How to see it

1. In Unity (Play stopped), everything is already applied. To re-apply, run **Tools › Onboarding › Hold the Yard: Apply Wiring**. It is safe to re-run and changes nothing on applied data.
2. Open `GB_m3-defence.prefab`:
   - six barricades on the two necks (row 6), Mark on the alcove tile 4,11;
   - the Masher at the bottom of the east lane, three Claws at the bottom of the west lane.
   - Select Mark and look under his `GUnit` tag set: Unmovable, Unable to Swap, IgnoreObjective. Under "Mark on the stone": the hold with "Hold From Level Start" on.
3. `GB_m3-defence_v1.prefab` is the old greybox, kept as it was.
4. From a cleared save, play up to the Trail (no squad pick screen), or pick `GB_m3-defence` in the level toolbar and press Play.
5. At the start:
   - the camera goes to the Masher, then the east wall, then Mark at the stone;
   - Mark and Linda speak, then you get input with Linda and Lucy only;
   - Mark can't be selected, and his panel shows his HP;
   - the objective reads "Hold them off (4)" and "Keep Mark standing.".
6. End the turn. On the enemy turn the west Claws walk up to the barricades and hit them (4 a hit; a barricade has 8). The family can walk through a barricade but not stop on it, and can't target it.
7. Each family turn start, before input:
   - turn 2: the stone shifts and two Claws come in at the bottom of the east lane;
   - turn 3: the stone shifts and three Claws come in (two west, one east on 8,2);
   - turn 4: the stone shifts and Mark speaks;
   - turn 5: the stone shifts, rolls away, and Mark hands over to "Finish them.".
8. Check that Mark's Role never fires when a Claw hits a sister near him, and that enemies attack him if they reach him.
9. Kill every goblin. The win plays the tally alone and "Still counting?", the fade, "…No.", the camera on the cave, Toba, his lines, then home.
10. To see the loss: let Mark fall. The loss panel lists "Keep Mark standing" as failed.

## Review (miso-reviewer, 7.1, pasted by the coordinator; the reviewer is read-only)

**Verdict: APPROVE.** Must fix: none. Should fix: none.

- `holdFromLevelStart`: off = M1 unchanged; on = the hold is in `Start`, before `levelStarted` and the first `StartTurn`; guarded so the tag goes on once; the tag survives `GUnit.Initialize`; worker-thread guard on the new handler; the listener is removed in `OnDisable`; no new statics. The 7 option tests check behavior.
- Relations: every turn-order faction has an "enemies" entry (tested on a runtime copy). Deviation from the plan: Neutral–Stranger is Enemy (needed for Stranger's enemy list); Stranger is last in the turn order. Play console check for `KeyNotFoundException` at the stone reveal is left to play.
- Stages: `turn = 1` per stage is right (relative count); stages complete at turns 2–5. Gap: the test checks data only; the behavior is left to the play check.
- Asset refs: only the Trail points at the new GUID; the old GUID lives only in `_v1`.
- LF / no BOM, no private IDs, no core files, commit grouping sound.
- Carried risks: Masher counter-push has no tag filter (can push Mark); both defeat groups draw enemies to Mark; `WireHold` deletes any other hold in the level (fine now).

## Verification

Verified 2026-11-26 on branch `main`, scope `all`, editor open, Unity MCP. Quiet checks only; no play session, so the M3 play-through is Not run (THJ plays it himself).

- **Result:** PASS (quiet checks)
- **Compile:** clean. Forced refresh plus compile request; no `error CS` entries in the console. The only warnings are "Serialization depth limit 10 exceeded" (StatBackedValueBase / GTag.subTags composition cycles, 18 entries). None mention `Features/Onboarding`; they are the existing serialization-cycle warnings on core types.
- **Tests (full EditMode suite, MCP job):** 2882 total, 2881 passed, 0 failed, 1 skipped (the Explicit `AIRegressionTest.Baseline_MatchesCurrentAI`). 486 s. Last known: 2861 passed + 1 Explicit, so +20 tests, all green.
- **AIRegressionTest.Baseline_MatchesCurrentAI (by name, not fixed or re-baselined):** failed as expected. Report line `CHECKS: 739  FAILURES: 52`, against the last recorded 50. The +2 are `units.unexpected` lines for `Unit_Barricade.prefab` and `Unit_Rock_Stone4.prefab` (the expected ones). I found no other new line type; the remaining failures are the existing set (graph fingerprints, new abilities, units.count / units.missing, units.ability, the final NullReferenceException). The gate does not fail on this.
- **Acceptance criteria:** compile clean: Pass. Full suite green: Pass. Baseline within expectation: Pass. In-game behaviour of M3: Not run, needs a play session.
- **Bugs found:** none.
- **Save reset:** no.
- **Editor state at the end:** the active scene is untitled (empty name and path), not dirty, 1 root object. Nothing was saved by me. Play mode off.
- **Editor checks corrections:** the full-suite MCP run took about 486 s for 2882 tests, and `get_test_job` disconnected during domain reloads three times (retrying with `wait_timeout` worked, as the file says). The Explicit test's failure output via `get_test_job include_failed_tests` is about 195 KB and is saved to a file; read it with Python.
