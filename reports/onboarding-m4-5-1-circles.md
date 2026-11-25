# Report: M4 "The White Mothers" build (The circles, Mithra's Rest, the Queen)

Plan: plans/2026-11-25-onboarding-m4-build-tech.md    Agent: miso-implementer    Branch: thj/onboarding-demo
Outcome: partial (chunk 5.1 done; 5.2 and 5.3 not started)

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

none

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

## Other branches

none

## How to see it

1. In Unity, open `Content/Levels/Greybox/GB_m4-cleanse.prefab` in Prefab Mode: 13 × 9 octagon of cells over the TArtEx cave room. Linda 0,4, Lucy 0,3, Toba 1,3, the placeholder on 1,4; Claws around the empty 8,4 with the Shaman on 9,4; pools at 5,7, 11,5 and 5,1 with a Claw beside the north and south ones.
2. Select the root: `CombatLevel` › level name "The circles", turn order Bergsons then Enemy, one win group with "Cleanse the circles." and "Defeat the dark claws."; a `GuidedAbilityHint` on `CleanseAbility` (turns 1..99); a `SequencePlayHandle` on `M4Circles_Start_SequentialSequence`; no `LevelAbilityLock`. The `GlobalEventBus` child has the `LevelStartFPFiller` (99).
3. To play it before 5.2 puts it in the mission: pick `GB_m4-cleanse` in the level toolbar's dropdown and press Play (sandbox mission; the roster is whoever the level places, so the slot on 1,4 may stay empty). Expect: the camera goes to the three pools, Toba's stand-in line, the camera comes back, the Cleanse button pulses, FTP full. Check that Explosive Arrow and the Linda–Lucy Duo can be used on turn 1. Then check that a pool spawns a Claw on round 3, not again while that Claw lives, that a Cleanse from an adjacent cell destroys a pool, and that the level is won once the pools are gone and every enemy is dead.
4. Re-run `Tools/Onboarding/The circles: Apply Wiring`: no diff. `Tools/Onboarding/The circles: Build Level` only warns that the level exists.
