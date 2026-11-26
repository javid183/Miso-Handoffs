# Report: M3 "Hold the yard" greybox build

Plan: plans/2026-11-25-onboarding-m3-greybox-tech.md    Agent: miso-implementer    Branch: thj/onboarding-demo
Outcome: partial (chunks 6.1 and 6.2 done; 6.3 and 6.4 are later runs)

## What changed

New:
- `Features/Onboarding/PickOnTilesLOCondition.cs`: new objective condition, the squad's free pick on the tiles (fixed seats read from the mission roster); exposes `{pick_i}`.
- `Features/Onboarding/PickHeldTilesLOCondition.cs`: new objective condition, the pick held the tiles at N family turn starts since the stage began.
- `Features/Onboarding/Editor/PickOnTilesLOConditionTests.cs`, `PickHeldTilesLOConditionTests.cs`: their EditMode tests.
- `Features/Onboarding/Editor/MissionWiring.HoldTheYard.cs`, `.Stone.cs`, `.Sequences.cs`, `.Mission.cs`: menus `Tools/Onboarding/Hold the Yard: Build Level` and `Hold the Yard: Apply Wiring` (the level; from 6.2 also the mission graph, the Trail renames and the pile's tally steps).
- `Features/Onboarding/Editor/MissionWiring.RiverCleanseLock.cs`: menu `Tools/Onboarding/The River: Lock Cleanse`.
- `Features/Onboarding/Editor/M3DefenceTests.cs`, `RiverCleanseLockTests.cs`: tests.
- `Content/Levels/Greybox/GB_m3-defence.prefab` (+ .meta): built from block `m3-defence`, then wired.
- `Features/NPCs/Rock/Prefabs/Unit_Rock_Stone0..3.prefab` (+ .meta): the stone variants.
- `Resources/Sequences/M3Defence/` (+ folder .meta): sequence assets (+ .meta).

Moved (guids and contents identical, checked with `cmp` against HEAD):
- `Content/Levels/Greybox/GB_m2-trailhead|blood|tracks|pile.prefab` (+ .meta) → `GB_m2-*_legacy.prefab`.

Modified (tracked):
- `Content/Levels/M2 - The Trail.asset`: the graph is one node, `GB_m3-defence`.
- `Content/Levels/Greybox/GB_s1-river.prefab`: a `LevelAbilityLock` with Cleanse locked for every hero (+31 lines).
- `Resources/Sequences/Search/Trail/Trail_Pile_End_SequentialSequence.asset`: the two tally steps removed (−2 lines).
- `Features/Onboarding/Editor/SearchWiring.Trail.cs`: legacy paths, no mission wiring, no tally steps at the pile.
- `Features/Onboarding/Editor/SearchTrailTests.cs`: follows the move.

## Acceptance criteria

See the chunk sections below; 6.3 and 6.4 not started.

## Chunks

### Chunk 6.1: level, stone and stages

**Built.** The two conditions; `GB_m3-defence` built through the grid-to-level builder from the paper block (plus `level fp full`, as M4's circles); the wiring menu (idempotent: a second run leaves the level and the four stone prefabs byte-identical, md5 checked); `M3DefenceTests`.

**Files and diff stat** (all untracked/new, line counts):

| File | Lines |
|---|---|
| `Features/Onboarding/PickOnTilesLOCondition.cs` | 94 |
| `Features/Onboarding/PickHeldTilesLOCondition.cs` | 94 |
| `Features/Onboarding/Editor/PickOnTilesLOConditionTests.cs` | 59 |
| `Features/Onboarding/Editor/PickHeldTilesLOConditionTests.cs` | 94 |
| `Features/Onboarding/Editor/MissionWiring.HoldTheYard.cs` | 454 |
| `Features/Onboarding/Editor/MissionWiring.HoldTheYard.Stone.cs` | 144 |
| `Features/Onboarding/Editor/MissionWiring.HoldTheYard.Sequences.cs` | 262 |
| `Features/Onboarding/Editor/M3DefenceTests.cs` | 554 |
| `Content/Levels/Greybox/GB_m3-defence.prefab` | 6154 |
| `Features/NPCs/Rock/Prefabs/Unit_Rock_Stone0..3.prefab` | 63 / 67 / 67 / 67 |
| `Resources/Sequences/M3Defence/*.asset` | 40 assets |

Each file has its `.meta`. All new `.cs` files LF, no BOM (as the Onboarding folder). No new statics (the conditions hold their state on the instance; the held count is a struct field reset in `Initialize`).

**Criteria**
- [x] New `GB_m3-defence.prefab` from block `m3-defence` with the builder; read-back matches (block below). Necks 2,3 and 8,3 plain floor, nothing on them; 1,3 and 9,3 no tile. Test: `TheTilesAndUnitsMatchThePaperBlock`, `TheNecksAreOpenFloorAndTheGapsBesideThemHaveNoTile`.
- [x] Squad Linda 4,4, Lucy 6,4, `Unit_Placeholder` 5,4; Early tier, all alert, family first. Tests: `TheSquadStandsOnItsTiles...`, `TheEnemiesAreEarlyTierAllAlertAndTheFamilyMovesFirst`.
- [x] Opening Masher anchor 3,6 (0.45), Dark Claws 7,7 and 5,6 (0.8), in play. Hidden `w1` 0,0 1,0; `w2` 10,0 9,0 10,1; `w3` 0,2 10,2, all 0.8, alert (the level's "all alert" covers revealed units). Mushrooms 1,1 and 9,1. Tests: `TheOpeningIsTheMasherAndTwoClawsInPlay`, `TheThreeWavesWaitHiddenInTheLanes`, `TwoMushroomsSitAtTheLaneMouths`.
- [x] Stone: four variants of `Unit_Rock` (`Unit_Rock_Stone0..3`, title "Stone", neutral), each in its own hidden group `stone0..3` on 5,8; start stone comes in when the level starts; each notch = Hide current then Reveal next; Toba in `toba` on 5,8, revealed in the outro after the last stone has hidden. Enemy–Neutral = Ally. Tests: `TheStoneVariantsAre...`, `EachStoneWaitsHidden...`, `TobaWaitsHiddenUnderTheStone`, `TheStartStoneComesInWhenTheLevelStarts`, `EachHoldStageEndMovesTheStoneANotch`, `EnemiesAndTheNeutralStoneAreAllies...`.
- [x] Heavenly Sword pickup under cell 8,6 at local zero. Test: `OneHeavenlySwordPickupLiesUnderItsTile`.
- [x] Cleanse locked for every hero prefab (reuses `MissionWiringWhiteMothers.LockCleanse`), Linda–Lucy Duo locked for both sisters, FP filled at start (filler lists the two sisters). Tests: `CleanseIsLocked...`, `TheFamilyTimePointsAreFilled...`.
- [x] Two feature-side conditions in `Features/Onboarding/`, no Core file changed, with EditMode tests (15 tests). Fixed units read from the mission roster's fixed seats (cheap: same rule `MissionTracker` uses for the generic dialogue slots), no hard-coded names.
- [x] Stages S1, S2, S3a/b/c, S4 with their sequences and the outro (tally show-alone, Linda's question, `SistersTally_FadeOut`, Lucy's answer, camera on the cave, reveal `toba`, his lines, `OutroCutscene`). Tests: the six stage tests and `TheOutroFadesTheTallyThenBringsTobaOut`.
- [x] Masher close-up: nothing built. A fresh demo save has not seen "Masher Goblin" before M3 by level contents: no instance of `Unit_MasherGoblin` in the Hearth memory levels (`GB_m1-linda`, `GB_m2-lucy`, `GB_m3-john`, `GB_m4-mark`), M1 (`GB_m1-ridge`) or M2 (`GB_s1-river`). The prefab's only level users are old/unplayed levels (`Level1-C3 1`, `Level2-C3*`, `LevelM1-C3`, `LevelE3-C1`, `LevelDomLinda-C1/C2`, art test levels). A save that played the old M1 has it marked seen (`EnemyIntroductionTracker`), so use a cleared save for the play check.
- [x] Wiring menu `Tools/Onboarding/Hold the Yard: Apply Wiring`, idempotent, Play-mode guard, partial files; `M3DefenceTests` (25 tests).

**Tests**
- `M3DefenceTests` + `PickOnTilesLOConditionTests` + `PickHeldTilesLOConditionTests`: 43/43 pass (Test Runner via UnityMCP).
- Extra safety run, every test under `MISO.Core.Features.Onboarding.*` and `MISO.Core.Levels.*`: 740/740 pass. (Full suite not run: no core system touched and this isn't the last chunk.)
- `AIRegressionTest.Baseline_MatchesCurrentAI` by name: **50 failures vs 46**. The +4 are `units.unexpected Unit_Rock_Stone0..3.prefab` (new unit prefabs not in the baseline, as `Unit_Rock` did). The `intent.condition-count` line was already failing (it listed `FactionTurnLOCondition`); it now also lists the two new types, still one line. Nothing else changed. Not re-baselined.

**Read-back** (`python claude-handoff/tools/level_to_grid.py "Content/Levels/Greybox/GB_m3-defence.prefab"`):

```grid id=src-gb_m3-defence title="Source: GB_m3-defence (offset x+0, y+0)"
_ _ _ _ _ T _ _ _ _ _
_ _ _ O O . . c _ _ _
_ _ . O O c . . . _ _
_ _ . . . . . . . _ _
_ . . . L . U . . . _
_ _ . _ _ _ _ _ . _ _
c . . _ _ _ _ _ . . c
. * _ _ _ _ _ _ _ * c
c c _ _ _ _ _ _ _ c c
--
note 5,4 deploy slot
note 8,6 DR_PickUp_HeavenlySword
level hidden toba 5,8
level hidden w1 0,0 1,0
level hidden w2 10,0 9,0 10,1
level hidden w3 0,2 10,2
```

Tool notes: Level Defence; 45 tiles; Early; all alert. Objectives: Clear the yard. / {pick_0}: push the stone. / Hold them off (1/3) (2/3) (3/3) / Finish them. Hidden groups stone0..3 each "a listed unit that is not a placed unit" (the tool doesn't know the new variants' GUIDs: "4 prefab GUIDs not in guidmap.json"). Differences from the paper block: `@` on 5,7 reads back as `.` (drawing aid only), `#` reads as `_` (both no tile); the stones don't draw. Otherwise identical.

**To check (each)**
1. *Hide + Reveal on the same cell*: by code, yes. `HideUnitsSequence` takes the stone out (`UnitOutOfPlay.TakeOut` unplugs it from 5,8) and only then the next step reveals the next stone, which plugs into its own cell (free by then), so it can't fall back to a neighbour. The order is in the asset and tested (`EachHoldStageEndMovesTheStoneANotch`). Needs the play check for the look.
2. *Pick-held completes at the family turn start, wave before input*: by code, yes. `SwitchTurnIE` runs `StartTurn(); Tick(); UpdateObjectives();` in one go, and the turn number ticks when the order wraps to index 0, which is the family (`TurnOrder` = Bergsons, Enemy, Neutral). The condition counts the first evaluation in the family phase with a new turn number; the stage's sequence starts right away and its first step turns input off. One caveat: `UpdateObjectives` returns early while a death-evaluation wait or a new-stage wait is running. If one of them is still running when the family turn starts, the count happens at the first evaluation after it ends, by which time the player may have moved the pick. Play check.
3. *Shots across 1,3 / 9,3*: not checkable in EditMode; the level has the gaps as drawn. Play check (Linda 1,4 → 1,1; Lucy the same).
4. *AI planner*: no M3 stage uses `TilesOccupied` or `UnitTileOccupied`. The new conditions are skipped (the planner's map is keyed by exact type), so nothing in the objectives draws enemies to 5,7. S1 (`EntitiesDestroyed`) and S4 (`LivingUnits`) have handlers, as every level does. The waves come in on normal utility (toward the nearest family member). Whether that matches the paper's paths is for the play check.

**Deviations (same behaviour)**
- The start stone is in group `stone0` and comes in when the level starts, through a level-start sequence (`SequencePlayHandle` on the level-started event, `PlayJustOnce` off). `HiddenLevelUnits` switches off any listed unit at Awake, so a stone listed in a group can't start visible. On screen it's the same: the stone is on 5,8 before the first turn.
- A notch reads as movement: each variant's art (`Visual`) sits 0.1 world units further right (0, 0.1, 0.2, 0.3; a tile is 0.5). Only the title and that offset differ from `Unit_Rock`.
- S3c's end runs the third notch (stone2 → stone3), then hides stone3 ("rolls away"). From then on 5,8 is an open tile until the end (see Risks).
- S2's text names the pick through a variable the new condition exposes: `{pick_0}: push the stone.`.
- Turn order includes `Neutral` last. Unlisted, it would sort first (index -1) and the turn counter would tick on the stone's turn instead of the family's.
- The builder's start filler listed Toba (hidden, not initialized at level start). The wiring sets it to Linda and Lucy.
- A `Hold the Yard: Build Level` menu (refuses to overwrite), as in M4's circles; the build ran once.
- The outro mirrors the Pile's end: `SistersTally_ShowAlone`, then Linda, `SistersTally_FadeOut`, Lucy. The Pile still has its own fade until 6.2 moves it.

**Placeholder lines** (seeded once in the dialogue assets, no marker in the text; 6.4 replaces them):
- S1 end, the pick: "There's a cave behind that stone." (`M3Defence_Cave_DialogNodeSequence`)
- S2 end, Linda: "Keep them off him!" (`M3Defence_Push_Bark_DialogNodeSequence`)
- S3a end, Lucy: "More from the east!" (`M3Defence_Notch1_Bark_DialogNodeSequence`)
- S3b end, Linda: "Both sides now!" (`M3Defence_Notch2_Bark_DialogNodeSequence`)
- S3c end, the pick: "It's moving... it's open!" (`M3Defence_Notch3_DialogNodeSequence`)
- Outro, Linda: "Still counting?" · Lucy: "…No." (from the paper; `M3Defence_End_StillCounting_*`, `M3Defence_End_No_*`)
- Outro, Toba: "You held them. Good." / "I know the way to the Rootwell. And where Ryker is." (`M3Defence_End_Toba_DialogNodeSequence`)
- Objective texts: "Clear the yard.", "{pick}: push the stone.", "Hold them off (1/3)…(3/3)", "Finish them." (from the plan)
- Stone title "Stone".

**How to see it (6.1)**: see "How to see it" below.

### Chunk 6.1 follow-ups (coordinator decision, built with 6.2)

**(a) 5,7 lit as a goal tile.** S2 is now one shown objective with two conditions, both needed: `PickOnTilesLOCondition` (first, so `{pick_0}` still names the pick) and `TilesOccupiedLOCondition` Bergsons on 5,7. A sister on 5,7 makes only the second true, so S2 doesn't complete; the pick on 5,7 makes both true. **Deviation (same intent):** the brief said a *hidden* objective. The goal highlight (`CombatLevel.RefreshGoalHighlights`, core, read only) skips objectives with `visibleToUser` off, so a hidden one would never light 5,7. The extra condition therefore sits inside the shown objective; the stage text is unchanged. AI: S2 is the only stage with a `TilesOccupied` condition, and no enemy is alive while it runs (the opening is dead, `w1` comes in at its end), so the planner has nobody to steer. Re-run safe: the push objective is written in place with two condition slots, so a second run keeps both managed references (md5 unchanged). Test: `StageTwoIsThePickOnThePushTileLitAsAGoalAndItsEndBringsTheFirstWave`.

**(b) The last stone stays through S4.** S3c's end now only moves the stone to its last notch (stone2 → stone3) and plays the pick's line. The outro hides stone3 (`M3Defence_End_HideLastStone`) right after the camera reaches the cave and before `toba` is revealed, so 5,8 is blocked until the win and free for Toba. `WiringSeed` keeps existing step lists on a re-run, so the wiring updates the two lists the first build wrote only when they are still exactly as written; a hand-edited list is left alone, with the usual warning. Tests: `EachHoldStageEndMovesTheStoneANotch` (no roll-away before the outro), `TheOutroFadesTheTallyThenBringsTobaOut` (roll-away after the fade, before Toba).
- Loose end: `Resources/Sequences/M3Defence/M3Defence_Notch3_HideLastStone.asset` (+ .meta) is now unused. The permission check refused my attempt to delete it, so it is still on disk, untracked. Don't stage it; delete it in Unity.

### Chunk 6.2: mission and the old Trail

**Built.** `Hold the Yard: Apply Wiring` now also does three things (`MissionWiring.HoldTheYard.Mission.cs`):
- It renames the four Trail prefabs to `GB_m2-*_legacy.prefab` with `AssetDatabase.MoveAsset`, only when the old path exists and the new one doesn't.
- It sets the graph of `M2 - The Trail.asset` to one node. The existing start node is reused (same node guid, position 0,0) and pointed at `GB_m3-defence`; the other four nodes and five edges go. Nothing else in the asset changed: the diff is the payload line plus the removed nodes and edges. The name, roster, items, Yard completion sequence, Map Table initiation sequence and Home state are untouched. The station unlocks and Toba's select button read the mission asset, so they still wait for it.
- It removes the two tally steps (`SistersTally_ShowAlone`, `SistersTally_FadeOut`) from the old pile's end step list, matched by type. The other six steps keep their order.

`SearchWiring.Trail` follows the new paths and no longer touches the mission. Its `WireMission` is gone, and a summary comment says why: the mission plays Hold the yard, and `MissionWiringHoldTheYard` owns its graph. The menu still wires the kept levels for reference. Its pile end no longer lists the tally steps, so a re-run of the Trail menu doesn't warn about the edited list.

New criterion: the River level. `Tools/Onboarding/The River: Lock Cleanse` adds a `LevelAbilityLock` to `GB_s1-river` with Cleanse locked for every hero. It reuses `MissionWiringWhiteMothers.LockCleanse` and saves only when something changed. `Wire Search: River` doesn't touch locks, so re-running it keeps this. A rebuild of the River with the grid tool would drop the lock; re-run the menu then.

**Re-run check:** both menus were run twice. After the second run these are byte-identical: `GB_m3-defence.prefab`, `M2 - The Trail.asset`, `GB_s1-river.prefab`, the M3 End and Notch3 step lists, and the pile end list.

**Diff stat (tracked)**, `git diff --stat -- miso/Assets` (paths shortened):
```
 Content/Levels/Greybox/GB_m2-blood.prefab            | 4904 ---   (moved, see below)
 Content/Levels/Greybox/GB_m2-blood.prefab.meta       |    7 -
 Content/Levels/Greybox/GB_m2-pile.prefab             | 5228 ---
 Content/Levels/Greybox/GB_m2-pile.prefab.meta        |    7 -
 Content/Levels/Greybox/GB_m2-tracks.prefab           | 4490 ---
 Content/Levels/Greybox/GB_m2-tracks.prefab.meta      |    7 -
 Content/Levels/Greybox/GB_m2-trailhead.prefab        | 3079 ---
 Content/Levels/Greybox/GB_m2-trailhead.prefab.meta   |    7 -
 Content/Levels/Greybox/GB_s1-river.prefab            |   31 +
 Content/Levels/M2 - The Trail.asset                  |   59 +-
 Features/Onboarding/Editor/SearchTrailTests.cs       |   80 +-
 Features/Onboarding/Editor/SearchWiring.Trail.cs     |   99 +-
 Resources/Sequences/Search/Trail/Trail_Pile_End_SequentialSequence.asset | 2 -
```
The four "deleted" prefabs and metas reappear untracked as `_legacy`, identical byte for byte (checked with `cmp` against HEAD), so git shows them as renames once both sides are staged. `LevelM2-C1.prefab` and `PreloadScreen.unity` also show in the diff; they are THJ's uncommitted changes, untouched.

**Criteria**
- [x] The graph is one node, `GB_m3-defence`, and everything keyed to the mission stays. Test: `M3DefenceTests.TheTrailMissionPlaysThisLevelAlone`. These pass unchanged: `HomeVisitsTests` (Yard chain, clue scene, home state, station and Family tab unlocks), `OnboardingMissionGraphTests` (mission order and roster), `M4WhiteMothersTests` (Toba's button gate) and `BondSourcesTests` (sisters in the Trail).
- [x] The four Trail prefabs are renamed `_legacy` with guids kept, and are out of the graph. `SearchWiring.Trail` and `SearchTrailTests` follow the new paths and pass, and a comment says why the menu no longer wires a level the mission plays. Tests: `M3DefenceTests.TheTrailsOldLevelsAreKeptUnderLegacyNames`, `SearchTrailTests.TheMissionNoLongerPlaysTheseLevels`.
- [x] The River level locks Cleanse for every hero. Test: `RiverCleanseLockTests.CleanseIsLockedForEveryHero`.
- [x] `SistersTally_FadeOut` plays at M3's end only. Tests: `SearchTrailTests.ThePileOutroNoLongerShowsOrFadesTheTally`, `M3DefenceTests.TheOutroFadesTheTallyThenBringsTobaOut`. Decision: `SistersTally_ShowAlone` left the pile too. It pins the counter alone for the fade, and without the fade it has nothing to pair with, so the whole tally beat now lives in M3's end. The pile's other steps are unchanged.
- [x] `OnboardingMissionGraphTests`, the Home tests that read the Trail mission, and the tally tests pass.

**Tests that pinned the old Trail graph** (rewritten in `SearchTrailTests`):
- `TheGraphRunsTrailheadToEitherRouteToThePileThroughAnOrJoin` (5 nodes, OR join, 5 edges): replaced by `TheMissionNoLongerPlaysTheseLevels`.
- `TheRouteMapOffersBothRoutesThenOnlyThePile` (route map over that graph): removed, since a one-node mission has no route map.
- `ThePileOutroShowsTheTallyAloneForLindasLineThenFadesItBeforeLucyAnswers`: replaced by `ThePileOutroNoLongerShowsOrFadesTheTally`.
No other test pinned the graph.

**Tests run:** every test under `MISO.Core.Features.Onboarding.*` and `MISO.Core.Levels.*`, plus `BondSourcesTests`: **772/772 pass**. That covers `M3DefenceTests` (27), the condition tests, `SearchTrailTests`, `SearchRiverTests`, `RiverCleanseLockTests`, `OnboardingMissionGraphTests`, the `SistersTally*` tests, `HomeVisitsTests`, `M4WhiteMothersTests` and `OnboardingOpeningSetupTests`. The AI regression was not re-run: 6.2 changed no AI graph, AI ability or unit prefab (still 50 failures against 46, from 6.1).

**Decisions (6.2)**
- The mission graph, the renames and the pile's tally steps sit in `Hold the Yard: Apply Wiring`, one menu for M3. Each step is safe to re-run.
- The River's lock has its own small menu. Putting it in `Wire Search: River` would re-save the River's clue props and sequences on every run.
- The mission's items stay as they are in the asset (2 Health Potions, 1 FP Potion; `SearchTrailTests` still checks them). Nothing writes them now.

## Reviews and checks

- (coordinator)

## Save reset

No.

## Decisions I made

- Stone notches shown by shifting each variant's art 0.1 to the right; start stone revealed at level start (Tier 1, same behaviour).
- With no fixed seat in the active mission (a level played on its own from the toolbar), every family member counts as the pick (documented in the condition).
- Neutral listed last in the turn order; FP filler lists only the sisters.
- (6.1) The last stone hid at S3c's end. The coordinator's follow-up changed that: it now hides in the outro, before Toba comes out.
- (6.1 follow-up) The goal-tile condition sits inside S2's shown objective, because the goal highlight skips hidden objectives.
- (6.2) `SistersTally_ShowAlone` leaves the pile along with the fade. The mission graph, the renames and the pile edit live in the Hold the yard menu. The River lock has its own menu.

## Needs THJ

none

## Docs to update

- `tech/level-tools.md` "Built so far": `GB_m3-defence` (coordinator).
- `tech/onboarding-merge.md` M3 rows: the Trail's four levels renamed `_legacy`, the mission graph down to one node, the River's Cleanse lock (coordinator).
- `reward-tools`' `guidmap.json` (for `level_to_grid.py`): add `Unit_Rock_Stone0..3` if the read-back should name them.

## Risks and loose ends

- **Sandbox play:** from the level toolbar's Play the mission has no fixed seat, so Linda or Lucy on 5,7 also pushes. Through the M3 mission only the pick does.
- **Turn-start count can slip** if a death or new-stage wait spans the family turn start (6.1 To check 2).
- **Revealed stone**: the start stone comes in through the normal reveal (initialize, "born"), so it may play a spawn effect at level start. Look at it in the play check.
- **Unused asset:** `Resources/Sequences/M3Defence/M3Defence_Notch3_HideLastStone.asset` (+ .meta). Delete it in Unity; don't stage it.
- **River lock and the grid tool:** rebuilding `GB_s1-river` with the grid tool drops the lock; re-run `The River: Lock Cleanse` after a rebuild.
- **Saves that played the old Trail:** use a cleared save for the M3 play check.
- The `HelpBox` text on the two conditions mentions `{pick}`, `{held}` and `{needed}`. S3's texts don't use `{held_0}`; they follow the plan's fixed "(1/3)" wording.

## Proposed commits

1. `feat(onboarding): objective conditions for the squad pick on a tile`: `Features/Onboarding/PickOnTilesLOCondition.cs`, `Features/Onboarding/PickHeldTilesLOCondition.cs`, `Features/Onboarding/Editor/PickOnTilesLOConditionTests.cs`, `Features/Onboarding/Editor/PickHeldTilesLOConditionTests.cs` (+ their .meta) (plain)
2. `feat(onboarding): M3 becomes Hold the yard and the Trail's levels leave the mission`:
   - the level and stone: `Content/Levels/Greybox/GB_m3-defence.prefab`, `Features/NPCs/Rock/Prefabs/Unit_Rock_Stone0..3.prefab`;
   - the sequences: `Resources/Sequences/M3Defence.meta` + `Resources/Sequences/M3Defence/` (every asset except `M3Defence_Notch3_HideLastStone.asset`);
   - the wiring and tests: `Features/Onboarding/Editor/MissionWiring.HoldTheYard.cs`, `.Stone.cs`, `.Sequences.cs`, `.Mission.cs`, `Features/Onboarding/Editor/M3DefenceTests.cs`;
   - the mission and the old Trail: `Content/Levels/M2 - The Trail.asset`, the four `GB_m2-*.prefab` (+ .meta) removed and the four `GB_m2-*_legacy.prefab` (+ .meta) added (renames), `Resources/Sequences/Search/Trail/Trail_Pile_End_SequentialSequence.asset`, `Features/Onboarding/Editor/SearchWiring.Trail.cs`, `Features/Onboarding/Editor/SearchTrailTests.cs`;
   - every .meta goes with its file.
   (plain; depends on 1)

   The plan proposed two commits here (the level, then the Trail leaving the mission). They can't be split cleanly: `MissionWiring.HoldTheYard.Mission.cs` uses the `_legacy` paths defined in `SearchWiring.Trail.cs`, and `M3DefenceTests` checks the mission graph and the renames. A split commit 2 would fail to compile or fail its tests. A split is possible only if the `.Mission.cs` part and its two tests move into the second commit; coordinator's call.
3. `feat(onboarding): Cleanse is locked in The River`: `Content/Levels/Greybox/GB_s1-river.prefab`, `Features/Onboarding/Editor/MissionWiring.RiverCleanseLock.cs`, `Features/Onboarding/Editor/RiverCleanseLockTests.cs` (+ .meta) (plain; independent of 1 and 2)

Not to stage: THJ's `LevelM2-C1.prefab`, `PreloadScreen.unity`, `ProjectSettings/*`, `Content/FamilySuperTime/DUO/Inserts/`; and the unused `M3Defence_Notch3_HideLastStone.asset` (+ .meta).

## Other branches

none

## How to see it

1. In Unity (Play stopped), everything is already applied. To re-apply, run **Tools › Onboarding › Hold the Yard: Apply Wiring** and **Tools › Onboarding › The River: Lock Cleanse**. Both are safe to re-run and change nothing on data that is already applied.
2. Open `M2 - The Trail.asset`: its level graph shows one node, `GB_m3-defence`.
3. Play it one of two ways:
   - Through the mission: from a cleared save, play up to the Trail.
   - Quicker: in the level toolbar dropdown pick `GB_m3-defence`, then **Play**. This is a sandbox run; pick John or Mark for the deploy slot.
4. At the start the stone sits on the top tile (5,8) and the Masher's close-up plays. Kill the Masher and the two Claws: "Clear the yard." strikes, the camera goes to the stone and the pick's line plays. The tile 5,7, below the stone, is lit as a goal.
5. Walk the pick to 5,7: the west wave (two Claws) comes in and Linda's bark plays. The objective reads "Hold them off (1/3)". Through the mission, a sister alone on 5,7 does nothing.
6. End the turn with the pick on 5,7. At the next family turn start, before you get input, the stone moves a notch and the east wave (three Claws) comes in. Step off for a turn and the stone waits.
7. Hold 5,7 for two more turn starts: the third wave comes in (one Claw per lane), then the stone takes its last notch. It still blocks 5,8. "Finish them.": kill the rest.
8. The win plays in this order:
   - the tally alone on screen, Linda's "Still counting?";
   - the tally fades, Lucy's "…No.";
   - the camera on the cave, the stone rolls away;
   - Toba comes out on 5,8 and speaks;
   - the outro, then the Yard at Home as before.
9. Play The River: Cleanse is missing from every hero's bar.
10. Also try: Linda on 1,4 shooting down column 1, across the gap at 1,3, into the mushroom on 1,1. Then Lucy's ember the same way.

## Chunk 6.3 (tally credit for mushroom blast kills)

Built (feature-side; no core file touched; Play not started):
- `Features/Onboarding/SistersTally/SistersTallyListener.Blast.cs` (new partial): the first ability that touches an alive `HazardEntity` (heard on `onAbilityEffectPerformedOn`) opens a window for that mushroom. A sister owner credits her; an enemy, another player unit or an ownerless ability opens a window crediting no one (first touch wins, so a later sister hit can't take over an enemy-set blast). An enemy that dies (`unitDied`) at minimum health while a credited window is open counts for her, claiming it in `_killedByPlayer`, so a later lethal report from the arrow on the same Claw adds nothing (and the reverse order also counts once). Skipped when a Duo or a Bloom already holds the enemy.
- Window closing: the hazard's `onDisposeReady` / `onDestroy` (public `SpawnableEntity` events, no core edit), level end, new level (`ForgetLevel`), `Disconnect`. Unwatch delegates remove the listeners from the hazard; no statics added, so no `PlayModeStaticReset` hook needed.
- `SistersTallyListener.cs`: `partial`, four one-line hooks (touch, death, level end, ForgetLevel) and a doc paragraph.
- `Editor/SistersTallyTests.Blast.cs`: 16 tests with fake mushroom seams (`IsBlastSource`, `WatchBlastEnd` public properties).

Diff stat: `SistersTallyListener.cs` 11+/2-; two new files (`SistersTallyListener.Blast.cs` ~110 lines, `SistersTallyTests.Blast.cs` ~230 lines, + .meta).

Tests: arrow-set -> Linda, ember-set -> Lucy, enemy-set / ownerless / other player unit -> no one, first-touch wins, arrow + blast on the same Claw counts once (both orders), Duo and Bloom claims respected, min-health only, each enemy once, window closed after the mushroom is gone / level end / new level / disconnect, non-mushroom entity opens nothing. SistersTallyTests 85/85. Full EditMode suite 2778 passed, 0 failed, 1 skipped (the Explicit AI baseline). `M3DefenceTests` and the Bond classes are inside the suite. AIRegressionTest not run (no AI content changed).

Deviations / limits (for the play check):
- The window is not bounded to the blast's own moment: there is no bus event for the blast, so any enemy that dies at minimum health between the mushroom being touched and its disposal counts for the sister who touched it, including a death from another source in that span (there is no sister ability running then in practice). A sister touching a hazard that never explodes keeps a window open until it is disposed or the level ends.
- A chain blast (a mushroom's blast setting off a second mushroom) has no touch event: the second one's kills count for whoever's window is open, else no one.
- Assumes an enemy's `unitDied` fires synchronously on the blast's damage, before the mushroom's dispose. Play check: Linda's bow from 1,4 into the mushroom on 1,1 with a Claw beside it; the tally should rise by one.

Proposed commit (after the play check, own commit): `feat(sisters-tally): mushroom blast kills count for the sister who set it off`
- `Features/Onboarding/SistersTally/SistersTallyListener.cs`
- `Features/Onboarding/SistersTally/SistersTallyListener.Blast.cs` (+ .meta)
- `Features/Onboarding/SistersTally/Editor/SistersTallyTests.Blast.cs` (+ .meta)

---

## Review (6.1–6.3) — miso-reviewer, 2026-11-25 (pasted by the coordinator)

**Verdict: FIX.** No core file edited; the planner only reads `IsSatisfied`/`GetType()` and skips the new types; no statics; Trail renames keep GUIDs and bytes; the mission diff is the graph only; level wiring, stages, pick conditions, outro order, River lock and commit split are sound.

Must fix:
1. `SistersTally/SistersTallyListener.Blast.cs:47-57, 79-92, 94-108`: the window closes only on the mushroom's dispose/destroy, but `MushroomExplosion.prefab` survives its blast (`disposeOnActivation 0`, `lifeTurns 25`; re-arms after 3 ticks), so the window stays open for the level. `unitDied` is synchronous and precedes `onUnitDamageDone`, so `RecordBlastDeath` claims later kills (Lucy's, the pick's, enemy-side) for the window's sister; an enemy-first touch blocks sister credit for the level. Fix: (a) open only when the hazard can blast now (`HazardEntity.CanPerform` and alive); (b) also close at the end of the turn it opened in (`turnEnded`) besides dispose/destroy/level end/new level; (c) ignore deaths while any ability is in progress (`_inProgress.Count > 0`). Tests: mushroom alive after the blast and a later Lucy kill counts for Lucy; a pick kill after a Linda-set blast counts for no one; the window is closed by the next turn.

Should fix:
1. `MissionWiring.HoldTheYard.cs:216-221`: comments use plan stage labels (S1, S2, S3a–S3c, S4): plain words instead.
2. `MissionWiring.HoldTheYard.Sequences.cs:135-138, 187-189, 192-198`: remove the first-build migration code (`EarlierLastStoneHideName`, the `earlier` lists, `StepListUpgrading`'s upgrade branch); a plain `BuildSequential` is enough.

Notes: **the pick dying softlocks S2/S3** (only the pick completes them; only defeat is "no Bergson standing"); a dead pick before S2 shows a raw `{pick_0}` → design decision for THJ. Pick-held condition resets on every level load; early-count edge case harmless; the faction-identity check is play-check only. Sandbox: every family member counts as the pick (documented). Stone order tested. Menus guarded, re-run safe. AI 50 accepted (D-715).

## Review fixes (6.1–6.3), implementer

Must-fix 1 (mushroom window, `SistersTallyListener.Blast.cs`, + one line in `SistersTallyListener.cs`):
- (a) A window opens only for a hazard that is alive and `CanPerform`.
- (b) Windows age on `turnEnded`. **Deviation from the review text:** a window closes at the *second* turn end after it opened, not the first. The blast lands ~1.5 s after the touch, and the player's turn can end inside that gap, so closing at the first end would lose the credit. The other close paths stay (dispose, destroy, level end, new level, disconnect). Say if you want the strict first-end version.
- (c) `RecordBlastDeath` ignores deaths while any ability is in progress (`_inProgress.Count > 0`).
- Arrow + blast once, both orders, in tests: blast lands while the arrow's ability runs -> ignored by the blast, counted once by the arrow's lethal report (the blast damage is in the health it measures); blast lands after the ability ended -> counted once by the blast, and the arrow's late effect report on the corpse adds nothing.
- New tests (SistersTallyTests.Blast.cs, 23 total): later Lucy kill stays Lucy's with the mushroom still armed; a pick kill after a Linda-set blast counts for no one; enemy-side death during an ability counts for no one; window closed by the next turn end; mushroom that cannot blast opens nothing; the two arrow-order tests.

Should-fix 1: stage-label comments in `MissionWiring.HoldTheYard.cs` are plain words.
Should-fix 2: `MissionWiring.HoldTheYard.Sequences.cs`: `EarlierLastStoneHideName`, `StepListUpgrading` and both `earlier` lists removed; `BuildSequential` called directly. Hold the Yard menu re-run (twice): all 41 files under `Resources/Sequences/M3Defence` byte-identical (md5) to before; the level prefab changed once (the defeat group below) and then stayed identical on the second run.

Pick-falls defeat (THJ decision, feature-side):
- New `Features/Onboarding/PickFallenLOCondition.cs` (+ .meta): the pick is the first unit of the family faction on the board whose nickname is not a fixed roster seat (same rule as `PickOnTilesLOCondition`); once seen it is watched, and the condition is true when it is no longer alive. A destroyed object (level teardown) is not a fall.
- Sandbox choice: with no fixed seat in the active mission there is no pick and it never triggers; likewise before a pick is seen.
- Wiring (`MissionWiring.HoldTheYard.cs`, `WireDefeatOnPickFalling`): the template's defeat group stays as is; a second defeat group holds the new condition (invisible objective); the level's defeat aggregation is set to Any so either group loses. Re-run safe (checked).
- Tests in `M3DefenceTests`: wiring (two defeat groups, Any, template kept, condition and faction); pick dies -> true, sister dies -> false; no fixed seat -> never; only fixed seats on board -> no pick yet.
- Play check: lose with the pick (John/Mark) dead from the start; a sister dying does not lose by itself.

Tests: full EditMode suite 2803 passed, 1 failed, 1 skipped (Explicit AI baseline). The failure, `GridToLevelCameraStartTests.Build_CameraLinePutsTheViewOnThatTile`, is an engine assertion (`m_LockCount == 0`) in `PrefabUtility.UnloadPrefabContents` during a grid-builder test, unrelated to these files; the whole class passed (17/17) when re-run alone, so it looks like an editor-state flake from the earlier menu runs. No Play run.

Proposed commits: the 6.3 commit now also includes the review fix (unchanged files list). The pick-defeat belongs with the M3 level commit: `Features/Onboarding/PickFallenLOCondition.cs` (+ .meta), `MissionWiring.HoldTheYard.cs`, `M3DefenceTests.cs`, and the level prefab. Sequence/comment cleanups go with their existing commit.

## Re-check (review fixes) — miso-reviewer, 2026-11-25 (pasted by the coordinator)

**Verdict: FIX.**

Must fix: `SistersTallyListener.Blast.cs:116` (used :57): the `CanPerform` check runs after the blast has started (`AEffectCompound.Apply` applies effects, then raises `onAbilityEffectPerformedOn`, `AEffectCompound.cs:161-167`; the mushroom's health decrease → `PerformMainEffect` → `onMainEffectPerformed` sets `CanPerform = false` before the 1.5 s delay), so no window ever opens and blast kills are never credited. Tests replace `IsBlastSource` (`SistersTallyTests.Blast.cs:35`), so they miss it. Fix: drop `CanPerform` (keep alive), or read "can blast" before the damage (e.g. `onMainEffectPerformed`); add a test with the default check on a real `HazardEntity`; update the class doc (:17).

Deviation (b) (second turn end): reasoning sound, but the window spans the whole enemy turn: deaths outside abilities then (the other mushroom set off by an enemy, damage over time, hazard ticks, sequence damage) go to the sister; a blast landing while an enemy ability runs is lost. Low stakes for M3. Should fix (optional): tie the window to the blast's timing (blast delay + margin, injectable clock) or close at the first turn end unless the blast is pending; credit a death only to the window of the mushroom that just blew up.

Pick-falls defeat: no issues (dead units deactivate, not destroy; pick seen at level start; sandbox safe; no statics; planner skips it; template group's meaning unchanged under Any; win checked before defeat). Should-fixes from the first review: done. Notes: the loss panel shows no reason when the pick falls (empty objective text) → a line like "{pick} fell" (6.4 text); re-run `GridToLevelCameraStartTests` before the commit.
