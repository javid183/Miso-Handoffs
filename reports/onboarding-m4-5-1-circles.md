# Report: M4 "The White Mothers" build (The circles, Mithra's Rest, the Queen)

Plan: plans/2026-11-25-onboarding-m4-build-tech.md    Agent: miso-implementer    Branch: thj/onboarding-demo
Outcome: partial (chunks 5.1 and 5.2 done; 5.3 not started)

## What changed

Chunk 5.1 only: the new level `GB_m4-cleanse` ("The circles"), its build and wiring menus, its start sequence, and `M4CirclesTests`. Details under "Chunks". Nothing existing was edited: no level, mission, roster, `M4SquadSlots`, Mithra's Rest or `Level3-C1`; no core-systems file.

## Acceptance criteria

The 5.1 criteria are ticked under Chunk 5.1. The 5.2 and 5.3 criteria belong to later runs.

## Chunks

### Chunk 5.1: M4-1 The circles (`GB_m4-cleanse`)

**Changed files.** All new (untracked), so line counts instead of `git diff --stat`. Paths under `miso/Assets/_Project/`.

```
 new  Content/Levels/Greybox/GB_m4-cleanse.prefab                                   8157 lines (+ .meta, GUID 505b171229d13d14ab0ce24d29de3edb)
 new  Features/Onboarding/Editor/MissionWiring.Circles.cs                             343 lines (+ .meta)
 new  Features/Onboarding/Editor/MissionWiring.Circles.Dressing.cs                    105 lines (+ .meta)
 new  Features/Onboarding/Editor/M4CirclesTests.cs                                    371 lines (+ .meta)
 new  Resources/Sequences/M4Circles/ (+ M4Circles.meta)
        M4Circles_Start_SequentialSequence.asset                                       23 lines (+ .meta)
        M4Circles_Start_CameraOnPools.asset                                            53 lines (+ .meta)
        M4Circles_Start_CameraBack.asset                                               53 lines (+ .meta)
        M4Circles_Start_Toba_DialogNodeSequence.asset                                  26 lines (+ .meta)
```

The `.cs` files are LF with no BOM, like the other onboarding editor files. (`MissionWiring.Circles.cs` holds a UTF-8 "·" in the block's title, copied from the paper block.) The prefab is large because of its 95 GridCells; 8157 lines is in line with the other built greybox levels. THJ's uncommitted files (`LevelM2-C1.prefab`, `PreloadScreen.unity`, `ProjectSettings/*`, `Content/FamilySuperTime/DUO/Inserts/`) were not touched; `git status` after the work shows them as before.

**How it was built.** Two menus in a new partial-class pair, class `MissionWiringCircles` (pattern of `MissionWiring.Ridge*.cs`):

- **`Tools/Onboarding/The circles: Build Level`** parses the block (a copy of the paper block `m4-cleanse`, held as a constant in the script, since the shared repo can't read `claude-handoff/`) and calls `GridToLevelBuilder.Build` with the palette, default template `LevelM1-C2`. It adds one builder line to the paper block: `level fp full`. It **refuses** when the prefab exists (logs a warning, writes nothing), so a hand-edited level is never replaced (D-621). A test checks that.
- **`Tools/Onboarding/The circles: Apply Wiring`** opens the built prefab and edits it in place. Run twice: the prefab and the four sequence assets were byte-identical after the second run (md5 checked).

What the wiring does:

- Level name "The circles"; turn order overridden to Bergsons, Enemy (family first).
- One win stage, `aggregationMode` All, not queued, two visible objectives: **"Cleanse the circles."** = `EntitiesDestroyedLOCondition` (All) on the three pool `HazardEntity`s; **"Defeat the dark claws."** = `LivingUnitsLOCondition` Enemy, alive ≤ 0. That counts every enemy GUnit (the Claws, the Shaman and any Claw a pool spawned). Pools are hazards, so they are not counted there. The template's defeat (no Bergson standing) is left as it is.
- No `LevelAbilityLock` at all (removed if present; the template has none), so Cleanse and everything else is usable.
- One `GuidedAbilityHint` on Cleanse (`CleanseAbility.asset`): see Decisions for the start mode.
- Checks that the build's start filler is there and set to 99 (it throws if not).
- Start sequence through `SearchWiringShared.WirePlayOnLevelStart` (a `SequencePlayHandle` on the level root, called by the bus's `levelStarted`): input off, HUD off, camera from the squad to the three pools, Toba's line, camera back on the squad, HUD on, input on.
- Dressing (see below).

**`level_to_grid.py` read-back** (after the last wiring run):

```grid id=src-gb_m4-cleanse title="Source: GB_m4-cleanse (offset x+0, y+0)"
_ _ _ . . . . . . . _ _ _
_ _ . . . P c . . . . _ _
_ . . . . . . . . . . . _
. . . . . . . . c . . P .
L . . . . . . c . s . . .
U T . . . . . . c . . . .
. . . . . . . . . . . . _
_ . . . . P c . . . . _ _
_ _ _ . . . . . . . _ _ _
--
note 1,4 deploy slot
```

- Level: The circles; 95 tiles; enemy tier not set (Standard); all enemies start alert: yes
- Objective text: Cleanse the circles.
- Objective text: Defeat the dark claws.
- Placed: 3 × CP_Spawner, 5 × Unit_DarkClaw, 1 × Unit_DarkShaman, 1 × Unit_Linda, 1 × Unit_Lucy, 1 × Unit_Placeholder, 1 × Unit_Toba
- Not drawn (decor, controllers, nested prefabs): Cave_LightStand, LevelBase

(The read-back right after the build, before wiring, was the same block; it also listed the template's scenery props, 1 × BecStatue and 3 × Cave_Obstacle_Rock_01, which the dressing removed.) Every row matches block `m4-cleanse`: `#` reads back as `_`, pools as `P`, and the deploy slot on 1,4 as the note. No origin offset, so block tiles are the GridCell names.

**Criteria met**

- [x] New prefab `Content/Levels/Greybox/GB_m4-cleanse.prefab` built from block `m4-cleanse` with the grid-to-level builder; the read-back above matches the block (terrain, units, pools, deploy slot 1,4). Nothing existing was overwritten. Tests: `TheTilesAndUnitsMatchThePaperBlock` (rebuilds the 13 × 9 block from the prefab's cells, pools, slot and units and compares it string for string), `TheBuildBlockIsThePaperBlockAndParsesClean`, `TheBuildNeverReplacesTheLevel`.
- [x] Squad: Linda 0,4, Lucy 0,3, Toba 1,3; one `Unit_Placeholder` on 1,4. Test: `TheSquadStandsOnItsTilesWithOneDeploySlotForThePick`.
- [x] Enemies at Standard tier, no stat overrides: Dark Claws 7,4, 8,5, 8,3, 6,7, 6,1; Dark Shaman 9,4; pools 5,7, 11,5, 5,1, each a Claw about every 4th round with at most one alive; 8,4 empty. Tests: `TheShamanStandsBehindAScreenOfClawsAroundAnEmptyTile`, `TheEnemiesAreStandardTierWithNoStatOverrides`, `ThreePoolsSpawnAClawEveryFourthTurnWithOneAliveEach`. The only instance overrides on the enemies are the builder's facing (`initialDirection`) and transform. **Pool values: see Decisions** (prefab defaults, not `Level2-C1-TArtEx`'s overrides).
- [x] All alert; family first. Test: `EveryEnemyStartsAlertAndTheFamilyMovesFirst`.
- [x] One stage, two objectives together, default loss. Tests: `OneStageNeedsEveryPoolDestroyedAndEveryEnemyDead`, `TheLossIsTheTemplatesDefault`. **Play check:** that "Cleanse the circles" completes when the last pool dies, and that the pools stop when cleansed.
- [x] Cleanse usable (no `LevelAbilityLock`); the Cleanse button pulses (one `GuidedAbilityHint`); Toba's level-start line plays (stand-in text). Tests: `NothingIsLockedSoCleanseIsUsable`, `TheCleanseButtonPulsesFromTheFirstTurnUntilUsed`, `TobasLinePlaysWhenTheLevelStartsBetweenTheCameraMoves`. **Play check:** the pulse, the camera moves and the line on screen.
- [x] `LevelStartFPFiller` 99 at level start, wired to the bus's `levelStarted`. Test: `TheFamilyTimePointsAreFilledAtLevelStart`. **Play check:** Marks-Sisters affordable on turn 1.
- [x] Dressing: the cave room from `Level2-C1-TArtEx` copied under `Environment/Dressing (Level2-C1-TArtEx)`, aligned to the grid; no gameplay objects. Test: `TheDressingIsArtOnly`. Details below. **Play check:** lighting and the look in game.
- [x] Editor menu wires it idempotently (`Tools/Onboarding/The circles: Apply Wiring`, partial files in `Features/Onboarding/Editor/`), with `M4CirclesTests`.

**Tests** (open editor, Unity MCP):

| Run | Result |
|---|---|
| `MISO.Core.Features.Onboarding.EditorTests.M4CirclesTests` (new) | 16/16 passed |
| `AIRegressionTest.Baseline_MatchesCurrentAI`, by name | **46 failures, same as the recorded 46 (D-687).** The same lines as before; nothing from this chunk (no new unit prefab, ability or graph). Not re-baselined. |
| Full EditMode suite (not required for 5.1; run because some tests scan all levels) | 2714 tests: 2713 passed, 0 failed, 1 skipped (the Explicit AI test) |

Console: no compile errors; only the usual "Serialization depth limit" and older compiler warnings. One log from the build: `[CameraHandler] grid width (9.50) is smaller than the viewport at minZoom (10.67) — widened boundary to compensate`, the builder's normal camera-boundary note.

**To-checks from the plan for this chunk**

- **Pool values used:** prefab `CP_Spawner` defaults, no overrides: `intervalMode` Recurring, `initialInterval` 3, `interval` 3 (the counter starts at 3, drops once per enemy phase tick and fires at 0, then re-arms at 3: fires on rounds 3, 7, 11, ..., every 4th), `enableSpawnLimit` on, `spawnLimit` 1, faction Enemy, health `Specs_CorruptionHealth` 10, `lifeTurns` 25, spawn effect `CP_SpawnerCompoundEffect` → `GUnitSpawnerEffect` → `Unit_DarkClaw`. `Level2-C1-TArtEx`'s two pools override these to `SpecificTurns` [3, 5, 7] and [2, 4, 6]: three spawns two rounds apart, then never again. That doesn't match "about every 4th turn" or "keep spawning until cleansed", so I didn't copy it (Decisions).
- **Shaman preset:** `Unit_DarkShaman.prefab` unchanged; abilities `DarkShaman_Ability_Attack`, `DarkShaman_Ability_Walk`, `DarkShaman_Summon_Ability`, `DarkShaman_Ability_Heal` (under `Resources/UnitSpecific/Enemy/DarkShaman/`). Standard tier, no overrides.
- **Explosive Arrow / Marks-Sisters for the sisters at this point of a fresh demo save:** both available, by data and code (not play-checked). There is no save-based ability gate: the only ability locks are per level (`LevelAbilityLock`), and this level has none. `Linda_Ability_ExplosiveArrow` is on `Unit_Linda.prefab`'s bar with `lockedByDefault` 0, and no skill-tree node grants or gates it. `Linda_Lucy_Duo` is a `PlayerController.prefab` cooperation entry with trigger `Linda_Lucy_Duo_Ability` (`lockedByDefault` 0). Its earlier lock (D-470) is level data in M2's levels, which doesn't reach this level. Test: `TheSistersDuoAndExplosiveArrowAreOpen`. So no stop was needed. Play check: both buttons usable on turn 1 with FTP full.
- **Pools set to one alive each:** yes (`enableSpawnLimit` 1 / `spawnLimit` 1, the prefab's own values).
- **Dressing:** done, cheaply, with one caveat. `Level2-C1-TArtEx`'s `Environment` object is switched off. What shows in that level is its root art: the `Background` sprite (the cave room, `Temple_03_0`), five `Broken_Pillar_*` raised blocks, four `Mighty-Tree_02_R2_0` silhouettes and four `Cave_LightStand`s. Copied: `Background`, the three tree silhouettes at the top corners, and the two lamps beyond the grid's top edge. Left out, because they would stand on the new floor: the five pillars (in the old level they sat on holes in its grid), the silhouette over the bottom-left corner, and the two lamps that land on tiles (one on the Shaman's 9,4). The art is shifted by (-0.5, +3.0), whole tiles, so the drawn flagstones keep lining up with the cells. The room's floor is about as tall as the 9-row grid, so the top row (y 8) touches the foot of the back wall. An unlit snapshot of the dressed level looked right: grid on the floor, nothing over the tiles. The template's greybox scenery (TestLevel art, 3 rocks, light stands, BecStatue) was removed when the dressing was made. **Not checked:** the in-game lighting (Light2D from the two lamps and the level's global light) and any foreground sorting issue.

**Decisions and loose ends:** see "Decisions I made" and "Risks and loose ends" below.

### Chunk 5.2: mission, roster, Toba, Mithra's Rest, the Queen

**Read the follow-up block at the end of this chunk first: THJ's decisions changed Toba's gates, the labels and Ryker after this text was written.**

**Changed files** (paths under `miso/Assets/_Project/`; no core-systems file edited):

```
 M  Content/Levels/M4 - The White Mothers.asset                      +-107  graph and roster (data)
 M  Content/Levels/DungeonSafeRooms/LevelDivineRelicRoom 1.prefab    +-336  Mithra's Rest (edited in place)
 M  Content/Levels/Level3/Level3-C1.prefab                           +-33   label (3/3) and the Cleanse lock
 M  Features/Player/Dom/Prefabs/Unit_Toba.prefab                     1 line: unlockedAfterMission -> M2 - The Trail
 M  Features/Onboarding/Editor/M4SquadSlots.cs                       table cut to the 3 levels; ApplyAll(); stale-decision code dropped
 M  Features/Onboarding/Editor/M4SquadPickTests.cs                   rewritten
 M  Core/Levels/Editor/OnboardingMissionGraphTests.cs                2 lines: Toba test now expects the Trail
 new Features/Onboarding/Editor/MissionWiring.WhiteMothers.cs        (+ .meta) mission, roster, Toba, Cleanse lock, the Queen
 new Features/Onboarding/Editor/MissionWiring.WhiteMothers.Rest.cs   (+ .meta) Mithra's Rest
 new Features/Onboarding/Editor/M4WhiteMothersTests.cs               (+ .meta) 14 tests
```
`git diff --stat` of the tracked files: 7 files changed, 483 insertions, 176 deletions. THJ's own files (`LevelM2-C1.prefab`, `PreloadScreen.unity`, `ProjectSettings/*`, `Content/FamilySuperTime/DUO/Inserts/`) were not touched.

**How.** One menu, `Tools/Onboarding/White Mothers: Apply Mission Wiring` (class `MissionWiringWhiteMothers`), re-runnable (a second run changed nothing; it only saves what differs). It also runs `M4SquadSlots` for the three levels. `Tools/Onboarding/Apply M4 Squad Slots` still works on its own.

**Criteria met**

- [x] **Graph** `GB_m4-cleanse` -> `LevelDivineRelicRoom 1` -> `Level3-C1`, one initial node, no gates. The duel, `Level2-C1-TArtEx`, `Level2-C2`, `Level2-C3-1`, `Level2-C3-2` left the graph; their files are unchanged. Tests: `TheGraphIsTheThreeLevelsInOrder`, `TheOldLevelsAreOutOfTheGraphButTheirFilesStay`. **Labels: see Decisions** (level names, not "(n/3)" on all three).
- [x] **Roster** Linda, Lucy, Toba fixed + 1 free; `forcedExcludedUnits` empty. Test: `TheRosterIsLindaLucyAndTobaPlusOneFreePickAndNobodyIsForcedOut`. **Fill order checked in tests:** the game's fill rule (roster units whose Nickname is not already placed, first in roster order) repeated on a copy of the mission for each of the three levels and for John and for Mark: exactly one unit is left, the pick, and one slot exists (`ThePickTakesTheDeploySlotNotAFixedSeatWhoeverThePickIs`, `NoSecondTobaIsDeployedAndNoFixedHeroIsLeftForTheSlot`). One placed Toba per level (`TobaIsPlacedOnceInEveryLevel`). The real spawn is only play-checkable.
- [x] **Toba's unlock** `Unit_Toba.prefab` `unlockedAfterMission` = `M2 - The Trail` (one line in the prefab). Tests: `TobaUnlocksAfterTheTrail`; `OnboardingMissionGraphTests.Mark_JoinsAfterTheHearth_TobaAfterTheTrail` (was `...TobaStaysOnTheRootwell`) updated to match. **Readers and Home effect: see "Toba's unlock" below. Needs a decision.**
- [x] **`M4SquadSlots`** table is the three graph levels (slot cells: circles 1,4; rest 10,-4; Queen 7,-2, all facing +x). The FP filler check applies to the circles and Mithra's Rest and compares the set of nicknames (Linda, Lucy, Toba), not the order (the builder lists them Lucy, Toba, Linda). Dead code for the levels that left (stale decisions entry, the FP fix for `Level2-C3-2`) removed. Re-run: all three levels "already up to date". `M4SquadPickTests` rewritten (3 fixed, Toba not excluded, graph levels, fill order, one Toba).
- [x] **Mithra's Rest** (`LevelDivineRelicRoom 1.prefab`, in place): level title "Mithra's Rest"; objective "Rest by the fire, take the relic, then go on." (the room's one objective, a Bergson on the exit tile, otherwise unchanged). A `SafeRoomFunction` on the room's own `ObjectiveTrigger` with the Healing Room's heal copied value for value (`Specs_Health`, `baseFactor` 0.5 of `StatUB_HP`); the call is added to that trigger's `TriggerOverlapTerminal` entry event (tag Player, `disableAfterTrigger` on, so it runs once). `LevelStartFPFiller` 99 on the event bus, wired to level start, listing Linda, Lucy, Toba (gauges left alone). Cleanse locked. Campfire props: two `Cave_LightStand` lamps under `Environment/Campfire (placeholder)` at (4.6, 0.6) and (5.5, 0.6), above the altar gap where no tile is. Tests: `MithrasRestIsNamedAndHasItsOneObjective`, `TheHealIsHalfOfMaxHpAndIsTheHealingRoomsOwn`, `TheHealRunsOnceFromTheRoomsTrigger`, `TheFamilyTimePointsAreFullAtLevelStart`, `TheCampfirePropsAreThere`.
- [x] **The relic** `DR_PickUp_HeavenlySword` was already in the room and stays: on cell **10,-2** (world 5.25, -0.75), 3 uses, reachable on foot from every placed hero by a walk over neighbouring tiles; the room's trigger box (5.26, -0.44, 0.5 x 0.5) overlaps that tile's top edge. Test: `TheRelicIsPlacedOnACellTheFamilyCanReachAndGivesThreeUses`.
- [x] **`Level3-C1`** roster works as built (Toba, Linda, Lucy placed, one slot on 7,-2); nothing else changed besides the label and the lock. Queen values untouched.
- [x] **Cleanse locked** in Mithra's Rest and `Level3-C1`: a `LevelAbilityLock` on each level root, one entry per hero prefab (John, Linda, Lucy, Mark, Toba, matched by Nickname so the pick is covered), each holding only Cleanse. Tests: `CleanseIsLockedInMithrasRestAndTheQueenForEveryHeroWhoCanBeThere`, `TheLocksOnlyHoldCleanseAndAreMatchedByNickname`, `CleanseIsOnlyUsableInTheFirstLevel`.
- [x] **Tests** all above; `OnboardingMissionGraphTests` still pass.

**Tests run** (editor open, Unity MCP)

| Run | Result |
|---|---|
| `M4SquadPickTests` (8), `M4WhiteMothersTests` (14), `M4CirclesTests` (16), `OnboardingMissionGraphTests` | all pass (one graph test first needed the graph's in-memory links initialised, fixed) |
| Full EditMode suite (includes `HomeVisitsTests` and every test that scans levels or missions) | 2730 tests: 2729 passed, 0 failed, 1 skipped (the Explicit AI baseline) |
| `AIRegressionTest.Baseline_MatchesCurrentAI` | not run: no AI graph, ability or unit prefab changed |

**Toba's unlock: what reads it, and what changes at Home after M3**

The field is `GUnit.unlockedAfterMission` on `Unit_Toba.prefab`. One thing reads it: `GUnit.IsUnitUnlocked()`, called by `WorkshopPanelUI.ShowPanel`, which lists the equipment that is generic or specific to an unlocked unit. Toba has two specific items (`Equipment_Exquisite Stone Axe`, `Equipment_Tribal Necklace`), so **after M3 the Home Workshop lists those two (unless their state is Hidden) instead of after M4.** That is the whole visible change from the field itself. Nothing else reads it: no Bond Threads or station code, no sequence (`HomeVisitsTests` and the Bond tests pass).

Toba is also gated by **five separate serialized values that are still "after M4"** (not this field; not changed):
1. `WorldMapPanel.prefab`: Toba's character select button, `unlockedAfterMission` = M4. **This matters for M4 itself:** `CharacterSelectButton.SetState` hides the button while its mission is not completed, and M4 is not completed while it starts, so Toba's tile is hidden on the pre-mission roster screen even though he is a fixed seat (the roster still includes him; `ApplyRosterStates` adds him to the fixed list first). The seat works but is invisible; the selected count may look short by one.
2. `UpgradesPanel.prefab` characters[4] (Toba) `requiredMissionToUnlock` = M4, and the same override in `Home - Scene.unity` and `Home - Memory.unity`: his skill-tree entry.
3. `FamilyMenu.prefab` Toba row `requiredMission` = M4: the Family tree entry.
4. `HomeIdleCharacter.missionRequirement` = M4 in `Home - Scene.unity`, `Home - Memory.unity` and `HomeMemory.prefab`: an idle figure at Home (which character: not verified).
5. `HomeInteractables.UnlockAfterMissions` = M4 on three objects in `HomeMemory.prefab` and `Home - Memory.unity`: hover props (which characters: not verified).

Result: with only the plan's field changed, Toba appears in the Workshop after M3 but in the select screen, skill tree, Family tree and Home scene only after M4. Moving those five to the Trail would make Toba appear everywhere after M3, but it would also open his skill tree and Family entry (the guided skill-spend flow and the Family tab) and change the Home scene, which is Home flow beyond "Toba appearing", so I stopped. **Decision for the coordinator/THJ:** at least (1) is probably needed for M4 to show his seat; (2) to (5) are the "Toba appears at Home after M3" change. Each is a single-field edit.

**Cleanse status of every other level in the demo's mission graph** (read from the prefabs; none changed here)

| Mission / level | Cleanse |
|---|---|
| M0 Hearth: Memory 1 Linda, Memory 2 Lucy, Memory 3 John, Memory 4 Mark | locked for each placed hero |
| MS1 The River (`GB_s1-river`) | **unlocked** (no `LevelAbilityLock` at all; John and Lucy placed) |
| MS2 The Ridge (`GB_m1-ridge`) | locked for Linda and Mark (the two placed) |
| M2 The Trail: The Trailhead, Follow the blood, Follow the tracks, The Pile | **unlocked** (each has a `LevelAbilityLock` but no Cleanse entry; Lucy and Linda placed, plus the free pick) |
| M4: The circles | unlocked on purpose; Mithra's Rest and the Queen locked |

So the River and the whole Trail (M3) can still Cleanse. The paper says M3 gets its lock in its own plan.

**Decisions I made (5.2)**

- **Level names, not "(1/3)" to "(3/3)" on all three.** 5.1 names the first level "The circles", the plan names the second "Mithra's Rest", and the Trail (M3) also uses plain unique names. Only the Queen's level carried an old "Into the Rootwell  (5/5)", wrong now, so it reads "Into the Rootwell  (3/3)". If the labels should be on all three, it is one constant per level (the circles' constant is in 5.1's wiring, which I did not touch). Level names are part of the level ids (`missionName|levelName`), so a save made mid-level in the old M4 would not match; play checks use a cleared save.
- **The heal is on the room's existing trigger, not a copy of the Healing Room's strip.** The relic room already has a `TriggerOverlapTerminal` beside the altar (Player tag, fires once) that plays the room's old scene; the heal is added to the same event, in the Healing Room's order (sequence, then heal). Same behaviour as the plan (heal once on a trigger, with the Healing Room's component and value); the heal and the scene that 5.3 builds fire together.
- **Heal value copied from the Healing Room's data** rather than typed, so the two cannot drift; a test checks 0.5 on `StatUB_HP` and equality with the Healing Room.
- **Cleanse lock lists all five heroes** (John, Linda, Lucy, Mark, Toba), by unit prefab, so the pick is covered whoever it is. Toba has no Cleanse; his entry is harmless.
- **`M4SquadSlots` filler check is a set comparison** (see above).
- **Edited `OnboardingMissionGraphTests`** (a test file under `Core/`) because it asserted Toba unlocks after M4, which this plan changes.

**Risks and loose ends (5.2)**

- **The room still plays its old scene and has Ryker in it.** `LevelDivineRelicRoom 1` is the old "Mithra's Gift" room: `Ryker` (an NPC at cell 13,-2) and `Shrine` stand in it, a `SequenceTrigger` plays `Level1C1_Mid_SequentialSequence`, and the trigger beside the altar plays `LevelHealingRoom_Mid_SequenctialSequence` (then dims the room). Their existing content was not touched; 5.3 replaces the campfire scene. Ryker standing in Mithra's Rest contradicts "saving Ryker" at the Queen's end: needs a decision for 5.3 (hide or remove him).
- **Look not checked.** The campfire lamps are placeholders placed by coordinates without a visual check; THJ dresses them.
- **The heal happens when a hero reaches the altar tile**, not on arrival at the level (the trigger fires when a Player-tagged collider overlaps its 0.5 x 0.5 box at the altar). If the paper means "heal on arrival", it needs a start call instead (the start filler has a `heal` option, off here).
- **Not play-checked:** the heal firing once, FTP full on turn 1, the pick landing on the slot in a real run, the relic grant (3 uses), Toba's tile on the select screen.
- **Mission blurb is old.** `missionName` "Into the Rootwell" and its description ("Follow the clue John and Linda found...") were not in the plan; they still show on the map.

#### Chunk 5.2 follow-up: THJ's decisions (2026-11-25), built

This block replaces the parts of the 5.2 text above that say otherwise: Toba's unlock (the unit prefab is back on M4 and only his select button moved), the level labels (now on all three), and Ryker (removed).

**1. Toba's gates**
- **Unit prefab:** `Unit_Toba.prefab` `unlockedAfterMission` is back on `M4 - The White Mothers` (no diff against HEAD). The two `OnboardingMissionGraphTests` lines are back as they were (no diff against HEAD). The wiring no longer touches the unit prefab.
- **Moved to after the Trail:** only the select button on the roster screen, the `unlockedAfterMission` override on the Dom button in `WorldMapPanel.prefab`. One line changed (`git diff --stat`: 1 file, 1 insertion, 1 deletion). Saving the panel through Unity rewrote eight unrelated sibling-order values in it, so the wiring changes that one value as a text edit and re-imports the asset (the code explains why). Re-run: no change.
- **"His home presence": there is no gate for Toba to move.** Nothing of Toba stands at Home (`HomeMemory/Entities/Bergsons` lists Mary, John, Linda, Lucy, Ben, Kevin and Ryker). All three `HomeIdleCharacter` gates (`Home - Scene.unity`, `Home - Memory.unity`, `HomeMemory.prefab`) are **Ryker's** (`Ryker.prefab`, appears at Home after M4: left as is, it fits "Ryker is found after the Queen"). The three `HomeInteractables` gated on M4 in `HomeMemory.prefab` and `Home - Memory.unity` are the **Bookshelf, the Cooking Cabinet (kitchen) and the Training Field**: stations, not Toba's presence, so left alone as asked. **No Home scene was edited** (scene diff stat: none; the only scene in `git status` is THJ's `PreloadScreen.unity`).
- **Kept after M4:** the `UpgradesPanel.prefab` skill-tree entry (and its overrides in the Home scenes) and the `FamilyMenu.prefab` row; Workshop gear (the unit prefab field) too.
- **Test:** `TobasSelectButtonOpensAfterTheTrail` (the one Dom button in the panel unlocks after `M2 - The Trail`) and `TobasUnitSkillTreeAndFamilyEntryStayAfterThisMission` (unit prefab, skill-tree entry and Family row all on M4). Replaces `TobaUnlocksAfterTheTrail`.
- **What now changes at Home after M3:** nothing visible. Toba's tile shows on the roster screen of M4 (so the fixed seat is visible); the Workshop gear, skill tree and Family entry still open after M4.

**2. Mithra's Rest, old room removed** (`LevelDivineRelicRoom 1.prefab`, this prefab only; no asset file deleted)
- **Removed objects:** `Ryker` (a `Ryker.prefab` instance), `Shrine` (root child with its `Visual`, the altar art and its two lights) and `Environment/SequenceTrigger` (a `LevelSequenceTrigger` that played `Level1C1_Mid_SequentialSequence`).
- **Removed on the altar trigger (`ObjectiveTrigger`):** the `SequencePlayHandle` (it played `LevelHealingRoom_Mid_SequenctialSequence`), the `LevelSpecificBehaviour` ("DisableRoomFunction", which dimmed the shrine's `Light` and `Top`) and the entry event's call to start that sequence. It keeps its collider, `TriggerOverlapTerminal` (one call: the heal, once) and `SafeRoomFunction`.
- **Dangling references:** none. Those references pointed only into the removed objects (the `LevelSpecificBehaviour` actions into the shrine's lights; the sequence handle into the trigger's own call). Test `NothingInTheRoomPointsAtAMissingObject` scans every component's serialized references for missing targets and `TheOldRoomIsGoneLeavingTheFireAndTheRelicOnly` checks the trigger's components. The objective (Bergson on the exit tile) and the level's own sequences (`SistersTally_*` on the event bus, unrelated) are intact. The five old sequence assets stay in `Resources/Sequences` (`Level1C1_Mid_*`, `SafeRoomSequences/LevelHealingRoom_Mid_*`); nothing else in the project was edited for this.
- **Side effect to know:** the shrine was the altar's art. The relic still sits on cell 10,-2, with no altar drawn behind it, and the two campfire lamps stand in the gap where the shrine was. The heal now fires silently (no scene) until 5.3 builds the campfire scene on that trigger. The room's objective, the relic, the heal and the family time points are as before.

**3. Labels:** `The circles  (1/3)`, `Mithra's Rest  (2/3)`, `Into the Rootwell  (3/3)`. The circles' title is a new constant (`MissionWiringCircles.LevelTitle`, the block's own name stays `LevelName`, so `M4CirclesTests` is unchanged and passes); this is the one edit to a 5.1 file, and the circles' wiring writes it too. `LevelNamesAreUniqueInTheMission` updated.

**4.** Heal on reaching the altar tile, once: accepted as built.

**Re-run results**

| Run | Result |
|---|---|
| `M4SquadPickTests`, `M4WhiteMothersTests` (now 17), `M4CirclesTests`, `OnboardingMissionGraphTests` | 50/50 pass |
| `HomeVisitsTests` and every other Home test (in the full suite) | pass |
| Full EditMode suite | 2733 tests: 2731 passed, 1 skipped (Explicit AI baseline), **1 failed: `GridToLevelFacingTests.Build_HiddenEnemiesGetTheFacingToo`**, an unhandled Unity-internal log (`Assertion failed on expression: 'm_LockCount == 0'` from `PrefabUtility.UnloadPrefabContents` inside the builder test). It passed in the first full run and passes on its own with its whole class (13/13) on re-run; the editor session dropped its MCP connection during the long run, which is the likely trigger. Not related to a file in this chunk, but not a clean single full-suite pass: please run the suite once more in the editor. |

**Diff stat now** (tracked files, `git diff --stat`): `LevelDivineRelicRoom 1.prefab` 721 lines (removals of the three objects and the scene wiring plus the heal, filler and lamps), `Level3-C1.prefab` 33, `M4 - The White Mothers.asset` 107, `WorldMapPanel.prefab` 2, `M4SquadSlots.cs` 71, `M4SquadPickTests.cs` 106. `Unit_Toba.prefab` and `OnboardingMissionGraphTests.cs` no longer differ from HEAD. New files: `MissionWiring.WhiteMothers.cs`, `MissionWiring.WhiteMothers.Rest.cs`, `M4WhiteMothersTests.cs` (+ `.meta`). `MissionWiring.Circles.cs` (5.1, untracked) gained the one constant.

**Proposed commit 2 is now:** the mission asset, `LevelDivineRelicRoom 1.prefab`, `Level3-C1.prefab`, `WorldMapPanel.prefab`, `M4SquadSlots.cs`, `M4SquadPickTests.cs`, `MissionWiring.WhiteMothers.cs` + `.meta`, `MissionWiring.WhiteMothers.Rest.cs` + `.meta`, `M4WhiteMothersTests.cs` + `.meta`. Not in it any more: `Unit_Toba.prefab` and `OnboardingMissionGraphTests.cs` (unchanged). `MissionWiring.Circles.cs` goes with commit 1 (one added constant).

## Reviews and checks

- 5.1: none yet. The plan has one `miso-reviewer` pass over 5.1 to 5.3.

## Save reset

No. Play mode was never started.

## Decisions I made

- **Pool spawn settings: the `CP_Spawner` prefab's defaults, not `Level2-C1-TArtEx`'s overrides.** The plan asked for TArtEx's settings and described the behaviour as "a Claw about every 4th turn, at most one alive per pool". TArtEx's pools use specific turns (2-4-6 / 3-5-7, three spawns then none), which contradicts that and the paper's "circles keep spawning until cleansed". The prefab TArtEx's pools derive from gives exactly the described behaviour, with no override. Same behaviour as the plan describes; the values are listed above.
- **The Cleanse pulse runs on the turn window (first turn 1, last turn 99), not `WhenUnlocked`.** `GuidedAbilityHint` in `WhenUnlocked` mode, with no lock on the level, starts at once anyway but logs a warning on every play ("waits for an unlock, but the level does not lock …"). Turn mode 1..99 behaves the same way: it pulses from the family's first turn until Cleanse is used, and it ends when Cleanse is used. It doesn't warn. If 5.3 wants the pulse to begin exactly after Toba's line: input is off until the start sequence ends, so the player first sees the pulse then anyway.
- **The block lives in the script.** `Build Level` holds a copy of the paper block, with `level fp full` added (the builder's own line, which the plan's FP filler needs). The shared repo can't read `claude-handoff/`, and the test compares the built level against its own copy of the block.
- **No origin offset.** Block tiles are GridCell names; the art was moved to the grid instead.
- **Default template `LevelM1-C2`, art copied from TArtEx** (as the plan says), not TArtEx as the builder's template. TArtEx as a template would have brought its own objectives, decisions, Ryker and its switched-off environment.
- **Toba's line uses the Dom dialogue character** (`Dom_DialogueCharacter.asset`, `CharacterEnum.Dom`, side Left). The shared line writer has no Toba, so the line is seeded through it and then given his speaker. Seeded once: `WiringSeed` keeps an existing dialogue's lines.
- **Toba's line is a visible stand-in:** "(placeholder) The circles. Cleanse them." Following `conventions.md` › Text, it carries no `[PLACEHOLDER] ` tag (dialogue shows the tag, and onboarding tests forbid it). The "(placeholder)" prefix marks it on screen instead. The text from `design/m4-text.md` §1 is not used (not approved).
- **Turn order written as an override** (Bergsons, Enemy), so "family first" doesn't depend on the faction registry's order.
- **Not edited:** `GB_m1-ridge`, `GB_m2-lucy`, the mission asset, `M4SquadSlots`, Mithra's Rest, `Level3-C1`. The level is in no mission graph yet (5.2 adds it).

## Needs THJ

Decided (see the 5.2 follow-up). Open: one more full EditMode run in the editor (one unrelated builder test failed once on a Unity-internal log and passes alone); whether the altar art (the removed shrine) should be redrawn for Mithra's Rest.

## Docs to update

- `tech/level-tools.md` › "Built so far": add `GB_m4-cleanse` (coordinator).
- `claude-handoff/reward-tools/guidmap.json`: nothing new needed (`level_to_grid.py` names every unit here).

## Risks and loose ends

- **5.3: Toba's line won't update by re-running the wiring.** `WiringSeed` keeps an existing dialogue, so 5.3 must rewrite `M4Circles_Start_Toba_DialogNodeSequence.asset`'s lines itself (or delete the asset and re-run), and add the sister lines (1.3, 1.4) and the pick line (1.5) if THJ takes them. The step list (`M4Circles_Start_SequentialSequence`) is also kept once it exists; added dialogue steps don't count as a structural change.
- **Pools expire after 25 rounds** (`lifeTurns` 25 on the prefab): an untouched pool disposes itself on its 25th tick. "Cleanse the circles" would then complete without a Cleanse. That's far beyond the paper's ~8 minutes, so I left the prefab value. Setting `lifeTurns` 0 on the three instances would make them permanent if THJ wants that.
- **The pools' spawned Claws are plain prefab instances** (Standard tier stats, XP as the prefab). Expected; noted for the XP checker.
- **The objective text says "dark claws" but also needs the Shaman dead** (`LivingUnits` on the whole Enemy faction). That's as the plan wrote it. `design/m4-text.md` suggests capitalising "Dark Claws".
- **Stale override in the prefab:** `turnOrders.Array.data[2]` = Neutral stays in the root's modification list after the array shrank to 2 (the template's order had three entries). Harmless, and the same thing 4.1a saw with stages. Left alone.
- **Dressing:** the top row touches the back wall's foot. The lighting is untested in play. The dressing is made only once (a re-run leaves it and any hand edit alone); delete `Environment/Dressing (Level2-C1-TArtEx)` to make it again.
- **Fill order (T-11) is 5.2's:** with Linda, Lucy and Toba placed, the pick should land on the placeholder. Not tested here because the level isn't in the mission yet.

## Proposed commits

1. `feat(onboarding): add The circles, a new opening level for the White Mothers mission` (plain): `miso/Assets/_Project/Content/Levels/Greybox/GB_m4-cleanse.prefab` + `.meta`; `miso/Assets/_Project/Features/Onboarding/Editor/MissionWiring.Circles.cs` + `.meta`; `miso/Assets/_Project/Features/Onboarding/Editor/MissionWiring.Circles.Dressing.cs` + `.meta`; `miso/Assets/_Project/Features/Onboarding/Editor/M4CirclesTests.cs` + `.meta`; `miso/Assets/_Project/Resources/Sequences/M4Circles.meta`; `miso/Assets/_Project/Resources/Sequences/M4Circles/M4Circles_Start_SequentialSequence.asset` + `.meta`; `.../M4Circles_Start_CameraOnPools.asset` + `.meta`; `.../M4Circles_Start_CameraBack.asset` + `.meta`; `.../M4Circles_Start_Toba_DialogNodeSequence.asset` + `.meta`. One unit: the tests read the prefab and the sequences, and the menus made them. The plan's commit 1 (after THJ's play check).

2. `feat(onboarding): M4 runs The circles, Mithra's Rest and the Queen with Toba in the squad` (plain): `miso/Assets/_Project/Content/Levels/M4 - The White Mothers.asset`; `miso/Assets/_Project/Content/Levels/DungeonSafeRooms/LevelDivineRelicRoom 1.prefab`; `miso/Assets/_Project/Content/Levels/Level3/Level3-C1.prefab`; `miso/Assets/_Project/Features/Player/Dom/Prefabs/Unit_Toba.prefab`; `miso/Assets/_Project/Features/Onboarding/Editor/M4SquadSlots.cs`, `M4SquadPickTests.cs`, `MissionWiring.WhiteMothers.cs` + `.meta`, `MissionWiring.WhiteMothers.Rest.cs` + `.meta`, `M4WhiteMothersTests.cs` + `.meta`; `miso/Assets/_Project/Core/Levels/Editor/OnboardingMissionGraphTests.cs`. Depends on commit 1 (the graph points at the circles prefab). If THJ wants Toba's unlock apart, `Unit_Toba.prefab` plus the test line can be its own commit (the test fails without it).

## Other branches

none

## How to see it

1. In Unity, open `Content/Levels/Greybox/GB_m4-cleanse.prefab` in Prefab Mode: 13 × 9 octagon of cells over the TArtEx cave room. Linda 0,4, Lucy 0,3, Toba 1,3, the placeholder on 1,4; Claws around the empty 8,4 with the Shaman on 9,4; pools at 5,7, 11,5 and 5,1 with a Claw beside the north and south ones.
2. Select the root: `CombatLevel` › level name "The circles", turn order Bergsons then Enemy, one win group with "Cleanse the circles." and "Defeat the dark claws."; a `GuidedAbilityHint` on `CleanseAbility` (turns 1..99); a `SequencePlayHandle` on `M4Circles_Start_SequentialSequence`; no `LevelAbilityLock`. The `GlobalEventBus` child has the `LevelStartFPFiller` (99).
3. To play it before 5.2 puts it in the mission: pick `GB_m4-cleanse` in the level toolbar's dropdown and press Play (sandbox mission; the roster is whoever the level places, so the slot on 1,4 may stay empty). Expect: the camera goes to the three pools, Toba's stand-in line, the camera comes back, the Cleanse button pulses, FTP full. Check that Explosive Arrow and the Linda–Lucy Duo can be used on turn 1. Then check that a pool spawns a Claw on round 3, not again while that Claw lives, that a Cleanse from an adjacent cell destroys a pool, and that the level is won once the pools are gone and every enemy is dead.
4. Re-run `Tools/Onboarding/The circles: Apply Wiring`: no diff. `Tools/Onboarding/The circles: Build Level` only warns that the level exists.
5. (5.2) Run `Tools/Onboarding/White Mothers: Apply Mission Wiring` (already run; a re-run changes nothing). Open `M4 - The White Mothers.asset` in the mission graph window: three levels in a line. Open `LevelDivineRelicRoom 1.prefab`: root `CombatLevel` name "Mithra's Rest"; `ObjectiveTrigger` has `SafeRoomFunction` and its `TriggerOverlapTerminal` calls it once; `GlobalEventBus` has a `LevelStartFPFiller` (99); `Environment/Campfire (placeholder)` has two lamps; the relic is on cell 10,-2. `Level3-C1.prefab` and the room each have a `LevelAbilityLock` with Cleanse for the five heroes. From a cleared save, play M4 with John once and Mark once: the pick should stand on the slot in each level, one Toba, Cleanse usable only in The circles, a heal and full FTP in Mithra's Rest.
