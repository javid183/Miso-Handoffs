# Report: C4a The River (`GB_s1-river`)

Plan: plans/onboarding/2026-11-01-onboarding-c4-search-levels.md (C4a), check: reports/onboarding-c4-0-check.md    Agent: miso-implementer    Branch: thj/onboarding
Outcome: done. It compiles. Full EditMode suite: 1220 run, 1219 pass, and the one failure is `MISO.Core.Systems.AI.EditorTests.AIRegressionTest.Baseline_MatchesCurrentAI` (the name was read from the run results). It has not been play-checked and nothing is committed. The save was not reset, and Play mode was not entered.

## What changed

- **`Content/Levels/Greybox/GB_s1-river.prefab`** (new, plus `.meta`): built from the `river` block (`plans/onboarding/2026-10-26-onboarding-levels.md`) with the grid tool's builder.
  - The block has no `level` lines, so I set the name and tier in code for this build: `Name = "The River"`, `Tier = Tutorial`, and no alert line (enemies start Unaware). The build reported no issues: 79 cells, 8 units, camera start placed.
  - **Round trip:** `level_to_grid.py` reads it back as the same map. `#` and `_` both read as no tile, and `@` reads as floor. It finds 3 Dark Claws, 3 Archer Goblins, John and Lucy, tier Tutorial, and alert not set. The template's scenery is still there (one BecStatue, three cave rocks) and doesn't match the river shape, which is a known limit of the tool.
- **`Features/Onboarding/Editor/SearchWiring.River.cs`** (new, plus `.meta`): menu item **Tools › Onboarding › Wire Search: River**. You can run it again at any time, and it re-applies everything after a rebuild. It:
  - **Start:** turns input off and hides the HUD. Lucy says "Ryker! Ryker!". The camera pans to the clue tile 16,3 and holds 0.8 s, then pans back to the opening view (the level's camera start). Then the Lucy's Family Role panel, then John says "Stay by me.". Input and HUD come back on.
  - **Clue props:** a child `Search Scenery/Clue (placeholder)` on 16,3, rebuilt on every run. It holds five sprite pieces and no colliders: Prints (brown), Blood (red), Fur (white), and two "Fallen Claw" copies of the Dark Claw sprite turned 90°. The Claw sprite and its sorting are read from `Unit_DarkClaw.prefab`; the prefab is not changed. The square sprite is `Resources/Sequences/Search/SearchProp_Placeholder.png`.
  - **End (outro):** input off, HUD hidden, a close-up camera on the clue (`minimal` framing), the clue lines, then the common `OutroCutscene`.
  - **Win:** the template's default is kept: defeat every enemy (`LivingUnits` Enemy ≤ 0).
  - **Mission:** see the next bullet.
- **`Content/Levels/MS1 - The River.asset`:**
  - The graph has one node, `GB_s1-river`, with `isInitialLevel` on and no edges. The node keeps its id.
  - `completionXPReward` 30. `completionGoldReward` 0.
  - `collectableGResources`: Gold 20, Timber 1 and Fabric 1, each a fixed amount with multiplier 1. `resourceCollectionCount` 3, so all three are always given.
  - Roster checked, not changed: John and Lucy fixed, 0 free slots.
- **`Resources/Sequences/Search/`** (new folder, plus `.meta`s): `River/` holds 10 sequence and panel assets, `River_Start_*` and `River_End_*`.
- **`Features/Onboarding/Editor/SearchRiverTests.cs`** (new, plus `.meta`): 9 tests, all passing.

## Acceptance criteria

- [x] Built from the `river` block, Tutorial tier, default alert. Tests check the tier, that the level has no `LevelAlertSettings`, and the level name.
- [x] Family starts 4+ from every enemy. Test (Manhattan distance; Sight is 3).
- [x] The clearing Claws on 5,3 / 6,4 / 6,2 wake together. The test checks each one is within 2 of another (default AlertRange 2, see the check report). The waking itself needs the play check.
- [x] Archers on the islands 9,5 / 13,5 / 9,1, and 11,3 is 4 from each of them. Test.
- [x] Level start: the camera pans to 16,3 and back, then Lucy's role panel, then "Stay by me.". The test checks the order, the focus points and the line. How it looks needs the play check.
- [x] Clue props on 16,3, and the end sequence shows them up close. Test checks the position, 5 sprites, no colliders, the close-up camera and the lines. How it reads needs the play check.
- [x] Win: defeat all. Test.
- [x] Mission: Gold 20, Timber 1 and Fabric 1, always given; XP 30; the graph; the roster. Tests.
- [x] Can a bark condition test "Lucy within 3"? **No**: there is no distance condition (C4-0 check, question 7). The steps for building the bark by hand are below.
- [x] EditMode: only `Baseline_MatchesCurrentAI` is red.

## Decisions I made

- **The level is named "The River"**, the same as the mission. Mission levels are looked up by level name inside their mission, so the same name in two places is harmless.
- **Gold goes in the drops, not in `completionGoldReward`** (set to 0), as the coordinator asked. M10–M13 already put Gold among their drops. The only difference from using `completionGoldReward` would be the failure reward, and a mission with one level gives no failure reward anyway (`CombatLevelRunHandler.AwardMissionFailureResources` returns early on the first level).
- **The block's tier and name are set in the build call, not in the doc:** I don't edit the paper plan. If you add `level name The River` and `level tier tutorial` to the `river` block, a rebuild from the Build Level From Grid window gives the same prefab.
- **The clue props are made in code** (a tinted square and the Claw sprite), and the wiring script rebuilds them on every run. So they are not hand edits, and they survive a rebuild once the wiring is run again.
- **The end uses the common `OutroCutscene`** (enable input, fade the grid in, show the HUD) after the clue lines, as other mission levels do. The grid is never hidden in this level.
- **No per-instance HP:** the table has none for the River (Claw 9.6, Archer 14.4 at Tutorial).
- I copied a camera-sequence helper (about 20 lines) instead of making `HearthMemoryWiringMark.BuildCamera` shared, so I wouldn't edit the Hearth files.

## Hand edits

None. Everything the wiring writes is re-applied by **Wire Search: River**. A rebuild with the grid tool, followed by running the menu item, restores the whole level.

## Needs THJ

None for C4a. The Catch & Return gate (C4-0 check, question 5) is still open for C4b.

## Play check for THJ

1. From the world map, start The River (John and Lucy). Lucy says "Ryker! Ryker!". The camera goes to the far bank on the right, the clue props are visible on 16,3, then it comes back to the family.
2. The panel "Lucy's Family Role", then John says "Stay by me.". Input comes back.
3. Lucy should show as Sheltered next to John, if Papa's Shelter applies at the start. Shelter wasn't wired by me; it is John's own rule.
4. All enemies start Unaware. Step Lucy to 3,3: the clearing should wake (sight 3), and all three Claws together. The ford Archers should stay asleep.
5. John hits 5,3, and Lucy's role prompt appears (embers). Check it costs 1 FTP; the pool starts at 8.
6. Cross to the ford. The Archers wake when someone stops within 3 (8,3 should do it). Stand on 11,3: no Archer should be able to target it.
7. Shield Flare: John on 11,3 with Shield Up, Lucy embers him. Check the copies along the diagonals reach the islands.
8. Kill everything: the camera closes in on the clue, the five lines play, then the level-won and mission-end panels. The rewards should show Gold 20, Timber 1, Fabric 1 and XP 30.
9. Check the clue props sit right (size, layer, not over a unit's head) and that the template's statue and rocks don't read as obstacles.

## Placeholder lines (wording not signed off, untagged in the assets)

- Start: Lucy "Ryker! Ryker!" (R7-1). John "Stay by me." (the plan's wording; the draft's bark R7-6 is "Stand by me, little spark.").
- Panel "Lucy's Family Role": "When a family member's action hits an enemy within 3 tiles of Lucy, she can follow up with an ember. / Press the key shown above her to fire it. It costs 1 family time point." This is my own wording from the role's facts, and it isn't in the draft.
- End: Lucy "Her prints. I'd know them anywhere." / John "Blood. Not much. She was still walking." / Lucy "That's her fur. Dad, she fought." / John "One clean blow each. A stone axe. Someone fought for her." / Lucy "Someone was here with her." (R7-2 to R7-5 and R7-13, all at the end close-up rather than on clue trigger tiles).
- Not placed: R7-6 to R7-12 are barks, built by hand, out of scope.

## Shield Flare discovery bark: steps to build it by hand

There is no "Lucy within 3 of John" condition and no "enemies awake" condition, so the closest gate is "John uses Shield Up in The River". It works like this:

1. Open `Resources/BarkSystemData/Abilities/John/Bark_Ability_John.barkability`, the Performing Ability graph.
2. From the **Bark Entry** node, chain the conditions through their **True** outputs:
   - **Ability Condition**: Ability Phase `Performed`, Ability `John_Ability_Shield` (`Resources/UnitSpecific/Player/John/Abilities/Shield/John_Ability_Shield.asset`).
   - **Performer Condition**: Performer `John`.
   - **Level Condition**: Level Name `The River`.
   - Optional, so it doesn't fire on a turn with nothing left to fight: **Faction Unit Count Condition** with the enemy side, At Least 1 alive.
3. Then the lines, as the graph's existing multi-line barks are chained (or a Dialogue Table):
   - John: "Lucy. If it gets hot, aim at me."
   - Lucy: "*At* you?"
   - John: "Trust me."
4. Turn on **play only once**, so it plays the first time only.
5. Save; the importer bakes it. To test, cast Shield Up in The River.

A real "Lucy within 3" gate needs a new condition node: an editor node in `BarkConditionNodes.cs` plus a case in `BarkManager.EvaluateCondition`. That is feature work in the bark system (not core), for later.

## Risks and loose ends

- **`GB_m3-john.prefab` now shows reimport noise**, not mine: Lucy's `animationEvents` size overrides on the instances, and a `firstTurn: 1` that was written out when the asset was re-serialized. It appeared after the asset refresh and save. `GB_m1-linda.prefab` was already modified before I started. Leave them out of these commits (or commit them separately: the `firstTurn` line matches the committed component).
- `ProjectSettings/*.asset`, the two AI runtime files and the two Hearth test files were already modified before I started; none of them is mine.
- `GridToLevelBuilder.Build` was run from code (the same call the window makes) with the tier and name set on the parsed block. My first build went to `GB_river.prefab`, because the id is `river`, and I removed it. The window would also name it `GB_river`. To keep `GB_s1-river`, a rebuild needs the output path given, or the block's id renamed to `s1-river`.
- The template's scenery (statue, rocks) stays, and the river has no water visuals: `_` is just an empty gap. This is greybox.
- `tech/level-tools.md` "Built so far" could list `GB_s1-river`.

## Proposed commits

1. `feat(onboarding): The River pair mission level and wiring`:
   - `miso/Assets/_Project/Content/Levels/Greybox/GB_s1-river.prefab` + `.meta`
   - `miso/Assets/_Project/Features/Onboarding/Editor/SearchWiring.River.cs` + `.meta`
   - `miso/Assets/_Project/Features/Onboarding/Editor/SearchRiverTests.cs` + `.meta`
   - `miso/Assets/_Project/Resources/Sequences/Search.meta`
   - `miso/Assets/_Project/Resources/Sequences/Search/SearchProp_Placeholder.png` + `.meta`
   - `miso/Assets/_Project/Resources/Sequences/Search/River.meta`
   - `miso/Assets/_Project/Resources/Sequences/Search/River/*` (10 assets + `.meta`s)
   - `miso/Assets/_Project/Content/Levels/MS1 - The River.asset`

   This is plain content, one unit: the mission points at the level, and the tests cover both. No core files.

All files are LF without a BOM (CR count 0 on every file listed).

## Docs to update

- `tech/level-tools.md`: `GB_s1-river` under "Built so far".
- `build-log.md`, `status.md`: C4a built, waiting for the play check.

## Other branches

None.

## How to see it

1. In Unity, the Project window: `Content/Levels/Greybox/GB_s1-river.prefab`. Open it to see the river, the units and `Search Scenery/Clue (placeholder)` on the far right.
2. Select `Content/Levels/MS1 - The River.asset`: XP 30, three drops, and the graph button shows one level.
3. Play from the world map's The River pin, or use the level toolbar's dropdown and **Play** on `GB_s1-river` for a sandbox run (the sandbox has no mission drops). Then follow the play check above.
4. After any rebuild of the level: **Tools › Onboarding › Wire Search: River**.

## Fix round (after review)

Compiles. Full EditMode: 1223 run, 1222 pass, and the only failure is `MISO.Core.Systems.AI.EditorTests.AIRegressionTest.Baseline_MatchesCurrentAI`. I re-ran **Wire Search: River** twice. The second run left `GB_s1-river.prefab` byte-identical, so the wiring is stable on re-runs. Not play-checked, and the save was not reset. Every touched file is LF without a BOM (CR count 0).

1. **Clue sorting** (`SearchWiring.River.cs`, `BuildClueProps`, `ClawLook`, `VerticalLayerIndex`). The pieces now sort the way units do on the clue's row. `GridPluggableEntity.Plug` gives each unit an order within its row plus 10 × the row's index. That index is the highest row's y minus the tile's y, as `GridManager` computes it; the wiring reads it from the cell names, which gives 3 for 16,3.
   - Layer: `Default`, the same as the Claw's `Body`.
   - The ground marks (Prints, Blood, Fur) take order 30, the units' shadow slot. The fallen Claws take 31, the Claw body's slot (1).
   - Both draw over the cell art, which sits at −11 to −6 on `Default`, and the Claws draw over the marks. A unit standing on 16,3 draws at the same level as the props (no deliberate overlap rule).
2. **Re-runs reuse the scenery.** `Search Scenery`, `Clue (placeholder)` and the five pieces are found by name and only their values are reset. Nothing is destroyed, so no new fileIDs appear. The first re-run changed only the five `m_SortingOrder` values on the existing objects (checked with a diff).
3. **"First sleeping enemy" panel** (new, `SearchWiring.Shared.cs`, class `SearchWiringShared`, for C4b to reuse):
   - **Assets** in `Resources/Sequences/Search/Shared/`: `Search_FirstSleepingEnemy_Panels` (title "Asleep"), `…_TutorialSequence`, and `…_SequentialSequence` with **`PlayJustOnce` on**.
   - **Once per save.** `PlayedSequencesTracker` keeps the played set in the save under `PlayedSequences`, keyed by the sequence's asset name, across missions. It is marked when the sequence ends (`SequencePlayer.Play`/`HandleSequencePlayEnded`, `Core/Levels/Runtime/SequencePlayer.cs:21-41`). The flag is only checked when the level's `SequencePlayer.Play` is called on that sequence; a step inside a `SequentialSequence` plays straight through and ignores it (`SequentialSequence.PlaySequence`). So the panel is **not** in the intro.
   - **How it's started.** The level root gets an existing `SequencePlayHandle` component (sequence player = the level's own; sequence = the shared one). The level's event bus `levelStarted` calls `SequencePlayHandle.StartSequence`, the same way the grid tool wires the FTP filler. It plays right after the intro (Lucy's call, the clue pan, the role panel, "Stay by me."), as turn 1 begins.
   - **Ridge:** C4b calls `SearchWiringShared.EnsureFirstSleeperSequence()` and `WireFirstSleeper(root, seq)` on `GB_s2-ridge`. Whichever pair mission is played first shows the panel.
   - `AbilityIntroductionTracker` doesn't fit: its seen-set is keyed by ability presets, and making an enemy ability "introducible" would fire it in the Hearth memory too.
   - **Sight beat: not built.** It can't be triggered as data. The Shift sight preview (`Core/Interactions/Runtime/ShowStatsHoverPreview.cs:155-185`) only reacts to the bus events `toggleShowStats(bool)` and `gridCellEntityHovered(entity, bool)`. Those can't be raised from a sequence or a persistent UnityEvent with a unit argument, and `SignalSequence` only broadcasts a string.
   - **What the sight beat would take:** a small new sequence in `Features/Onboarding`, about 40 lines plus a test, with no core change:
     - Find the Unaware enemy nearest the family.
     - Call the public `EnemyAlertTracker.TryGetUnawareRangeTiles` (`EnemyAlertTracker.cs:455`).
     - Set `GridCell.SetShiftPreview(ShiftPreviewLayer.EnemyMove, true)` on its sight tiles (`GridCell.ShiftPreview.cs:68`), wait about 1.5 s, then clear them.
     - Put it as a second step of the shared once-only sequence.
     - Possible clash: the player holding Shift at the same moment, because both write the same preview layer.
   - **Wording** (placeholder, untagged): "Asleep" / "• A sleeping enemy does nothing until it wakes. • It wakes when it sees you (3 tiles) or when it is hit. • Hold Shift over it to see its sight."
   - **Image:** placeholder. It reuses `Tut-FR-1.png`; no existing shot shows the sleeping marker.
4. **Lucy's role panel image.** `Tut-FR-1.png` is not Linda's Watch. It is the generic "Activate Passive [F]" prompt shot: John, a highlighted Lucy and Claws. The page now plays the existing clip of Lucy's follow-up, `Resources/Tutorials/Tut-FR-2.mp4`, the one the old `Tutorial_FR_Lucy` asset uses on its "Lucy's Family Passive" page (page type Video). `Tut-FR-1` stays as the page's still.

**Tests:** 3 new in `SearchRiverTests`, 12 in all:
- the clue's sorting (layer, row band, marks under the Claws);
- Lucy's panel is the video page with `Tut-FR-2`;
- the first-sleeper panel: the shared asset, `PlayJustOnce`, the handle on the level, a single `levelStarted` call, and not in the intro.

**Files added this round:**
- `Features/Onboarding/Editor/SearchWiring.Shared.cs` + `.meta`
- `Resources/Sequences/Search/Shared.meta`
- `Resources/Sequences/Search/Shared/` (3 assets + `.meta`s)

**Changed this round:** `SearchWiring.River.cs`, `SearchRiverTests.cs`, `GB_s1-river.prefab`, `River_Start_Panels.asset`.

**Commit split:** unchanged, one content commit. Add the shared file and folder to it. `SearchWiringShared` belongs with the River, its first user.

**Play check, added steps:**
- After the River's intro, the "Asleep" panel shows once, as turn 1 begins.
- Restart the level, or play the Ridge later: it doesn't show again. To see it again, reset the save.
- The clue props draw over the ground and under or level with units.
- Lucy's role panel plays the clip.

**Risk:** the panel opens as turn 1 starts. Check it doesn't fight the phase banner or open while input is live.
