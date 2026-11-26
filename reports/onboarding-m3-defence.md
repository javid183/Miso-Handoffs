# Report: M3 "Hold the yard" greybox build

Plan: plans/2026-11-25-onboarding-m3-greybox-tech.md    Agent: miso-implementer    Branch: thj/onboarding-demo
Outcome: partial (chunk 6.1 done; 6.2 to 6.4 are later runs)

## What changed

Chunk 6.1 only (all new files; no tracked file modified):
- `Features/Onboarding/PickOnTilesLOCondition.cs`: new objective condition, the squad's free pick on the tiles (fixed seats read from the mission roster); exposes `{pick_i}`.
- `Features/Onboarding/PickHeldTilesLOCondition.cs`: new objective condition, the pick held the tiles at N family turn starts since the stage began.
- `Features/Onboarding/Editor/PickOnTilesLOConditionTests.cs`, `PickHeldTilesLOConditionTests.cs`: their EditMode tests.
- `Features/Onboarding/Editor/MissionWiring.HoldTheYard.cs`, `.Stone.cs`, `.Sequences.cs`: menus `Tools/Onboarding/Hold the Yard: Build Level` and `Hold the Yard: Apply Wiring`.
- `Features/Onboarding/Editor/M3DefenceTests.cs`: level tests.
- `Content/Levels/Greybox/GB_m3-defence.prefab` (+ .meta): built from block `m3-defence`, then wired.
- `Features/NPCs/Rock/Prefabs/Unit_Rock_Stone0..3.prefab` (+ .meta): the stone variants.
- `Resources/Sequences/M3Defence/` (+ folder .meta): 40 sequence assets (+ .meta).

## Acceptance criteria

See "Chunk 6.1" below; 6.2 to 6.4 not started.

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

## Reviews and checks

- (coordinator)

## Save reset

No.

## Decisions I made

- Stone notches shown by shifting each variant's art 0.1 to the right; start stone revealed at level start (Tier 1, same behaviour).
- With no fixed seat in the active mission (a level played on its own from the toolbar), every family member counts as the pick (documented in the condition).
- Neutral listed last in the turn order; FP filler lists only the sisters.
- The last stone hides at S3c's end, as the plan says (not at the outro).

## Needs THJ

none

## Docs to update

- `tech/level-tools.md` "Built so far": `GB_m3-defence` (coordinator).
- `reward-tools`' `guidmap.json` (for `level_to_grid.py`): add `Unit_Rock_Stone0..3` if the read-back should name them.

## Risks and loose ends

- **Sandbox play:** from the level toolbar's Play the mission has no fixed seat, so Linda or Lucy on 5,7 also pushes. Through the M3 mission (after 6.2) only the pick does.
- **5,7 isn't lit as a goal tile:** the goal highlight (`CombatLevel`, core) knows only `TilesOccupied` and `UnitTileOccupied`. A hidden companion `TilesOccupied` (Bergsons on 5,7) in S2 would light it at no AI cost, since no enemy is alive during S2. Not done (outside the plan); coordinator's call.
- **5,8 is open during S4:** after the stone rolls away, anyone can step into the cave tile. If someone stands there at the win, Toba comes out on the nearest free cell. Alternative: hide the last stone in the outro, just before Toba.
- **Turn-start count can slip** if a death or new-stage wait spans the family turn start (To check 2).
- **Revealed stone**: the start stone comes in through the normal reveal (initialize, "born"), so it may play a spawn effect at level start. Look at it in the play check.
- The mission still plays the Trail until 6.2: `GB_m3-defence` is reachable only through the level toolbar for now.
- `HelpBox` text on the two conditions mentions `{pick}`, `{held}`, `{needed}`; S3's texts don't use `{held_0}` (they follow the plan's fixed "(1/3)" wording).

## Proposed commits

1. `feat(onboarding): objective conditions for the squad pick on a tile`: `Features/Onboarding/PickOnTilesLOCondition.cs`, `Features/Onboarding/PickHeldTilesLOCondition.cs`, `Features/Onboarding/Editor/PickOnTilesLOConditionTests.cs`, `Features/Onboarding/Editor/PickHeldTilesLOConditionTests.cs` (+ their .meta) (plain)
2. `feat(onboarding): M3 becomes Hold the yard` (6.1 part): `Content/Levels/Greybox/GB_m3-defence.prefab`, `Features/NPCs/Rock/Prefabs/Unit_Rock_Stone0..3.prefab`, `Resources/Sequences/M3Defence.meta` + `Resources/Sequences/M3Defence/` (40 assets), `Features/Onboarding/Editor/MissionWiring.HoldTheYard.cs`, `.Stone.cs`, `.Sequences.cs`, `Features/Onboarding/Editor/M3DefenceTests.cs` (+ every .meta) (plain; depends on 1)

Not to stage: THJ's `LevelM2-C1.prefab`, `PreloadScreen.unity`, `ProjectSettings/*`, `Content/FamilySuperTime/DUO/Inserts/`.

## Other branches

none

## How to see it

1. In Unity (Play stopped), the level is already built and wired. To re-apply: **Tools › Onboarding › Hold the Yard: Apply Wiring** (safe to re-run; changes nothing on a wired level).
2. Level toolbar dropdown → `GB_m3-defence` → **Play** (sandbox; pick John or Mark for the deploy slot).
3. At the start the stone sits on the top tile (5,8) and the Masher's close-up plays. Kill the Masher and the two Claws: "Clear the yard." strikes, the camera goes to the stone, the pick's line plays.
4. Walk the pick to 5,7 (below the stone): the west wave (two Claws) comes in, Linda's bark plays. The objective reads "Hold them off (1/3)".
5. End the turn with the pick on 5,7: at the next family turn start the stone moves a notch and the east wave (three Claws) comes in, before you get input. Step off for a turn and the stone waits.
6. Two more turn starts on 5,7: the third wave (one Claw per lane), then the stone rolls away. "Finish them.": kill the rest.
7. The win: the tally alone, "Still counting?", it fades, "…No.", the camera on the cave, Toba comes out and speaks, the outro.
8. Also try: Linda on 1,4 shooting down column 1 across the gap at 1,3 into the mushroom on 1,1; Lucy's ember the same.
