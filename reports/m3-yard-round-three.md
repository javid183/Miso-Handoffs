# Report: Hold the yard, round three (walk-in, shorter lanes, a threat during the hold, the cave exit)

Plan: plans/2026-11-27-m3-yard-round-three.md    Agent: miso-implementer    Branch: master (working tree, nothing committed)
Outcome: done (edit-mode verified; not play-checked)

## What changed

Runtime (feature code, `Features/Onboarding/`, no core folder touched):
- `KeepUnitsPassiveUntilSignal.cs` (new): keeps listed enemies Unaware from the level start until `Release()` (signal). Removes only the tag it added; a unit released during its own faction's turn has that turn's points closed (as the alert tracker does when it wakes a unit); a release before the start cancels the hold. No statics.
- `MoveUnitsTogetherSequence.cs` (new): walks units of one faction to tiles together. Each walk names a unit by nickname, or an empty name means "the faction's one other unit in play" (the pick). Walkers whose tile another walker stands on start after the first group. Optional "hide after": fades every walker and takes it off the board (UnitOutOfPlay). No statics.
- `UnitsReachTilesSequenceTrigger.cs`: new serialized option `waitUntilSettled` (default off) plus a 5-argument `Set`. When it is on, the trigger waits while any faction has an action running, so it fires once the hero has stopped, not mid-walk. The west wall watch keeps it off, so its behaviour is unchanged.
- `MoveGroupUnitSequence.cs`: the walk start and the "wait until every walk is over" loop moved into `internal static` helpers (`TryStartWalk`, `WalkTogether`) that the new sequence reuses. Same behaviour; the existing tests pass.

Wiring (`Features/Onboarding/Editor/`):
- `MissionWiring.HoldTheYard.cs`: block `m3-defence-5` (with `level origin -5,1`, `BlockOrigin`), new tile constants for THJ's layout and the removed row, five stages (the last hold turn wins and has no end sequence), the opening = 4 Dark Claws + Black Claw on 4,11, Masher factor only for the east-lane Masher. `FinishObjective` removed.
- `MissionWiring.HoldTheYard.Arrival.cs` (new partial): start tiles (Linda 13,9, Lucy 13,8, deploy slot 14,8), the waves' units and group order, the two enemy holds and their signal listeners, the arrival watch, the shrine, the camera start.
- `MissionWiring.HoldTheYard.Sequences.cs`: new Start (stone + camera on the corridor), new Arrival (camera, walk-in, camera on the stone + Linda's line, camera back, wake signal), Cave + wake-west signal, Notch1 + the archers' walk, new outro. Notch3 is gone.
- `MissionWiring.HoldTheYard.Stone.cs`: a second Stone0 instance (`Unit_Rock_Stone0_Closing`, group `stoneclosed`) closes the cave at the end, because a hidden group comes in only once.
- `MissionWiring.HoldTheYard.Lines.cs`: `OpenLine` removed, `TobaCallLine` added (placeholder), nickname constants, west wall approach tiles moved to row 6.
- `MissionWiring.HoldTheYard.Pick.cs`: comments only (the release now comes from the outro).

Tests (`Features/Onboarding/Editor/`):
- `M3DefenceTests.cs`, `M3DefenceTests.Lines.cs`: updated to the new layout and flow.
- `M3DefenceTests.Arrival.cs` (new): arrival watch, walk-in, enemy holds, wake signals, shrine, camera start.
- `KeepUnitsPassiveUntilSignalTests.cs`, `MoveUnitsTogetherSequenceTests.cs`, `UnitsReachTilesSequenceTriggerTests.cs` (new).

Data:
- `Content/Levels/Greybox/GB_m3-defence.prefab`: row 7 removed and everything below shifted up (one-off step, below), then the wiring applied.
- `Resources/Sequences/M3Yard/`:
  - New: `M3Yard_Arrival_{SequentialSequence, CameraOnYard, WalkIn, CameraOnStone, CameraBack, WakeEnemies}`, `M3Yard_Cave_WakeWestCorridor`, `M3Yard_Notch1_ArchersWalk`, `M3Yard_Start_CameraOnCorridor`, `M3Yard_End_{ReleasePick, HideStone, RevealStone, RollAway, TobaCall_DialogNodeSequence, Rush, StoneCloses}`.
  - Recreated with new GUIDs: `M3Yard_{Start, Cave, Notch1, End}_SequentialSequence`. These step lists are never rewritten once they exist (WiringSeed), so I moved the old ones to the trash before the run. They matched the old wiring exactly (no hand edits), and only the level referenced them; the wiring re-pointed it.
  - Camera assets: re-framed for the shifted rows.
  - Deleted (moved to the trash; also in git): the 8 `M3Yard_Notch3_*` assets, `M3Yard_Start_CameraOnStone`, `M3Yard_Start_CameraBack`. A GUID search found no other references; the pick's "open" line dialogue was among them.

## The prefab: before and after (`level_to_grid.py --no-shift`, prefab coordinates, drawing x -5..14)

Before (THJ's uncommitted layout, snapshot at the scratchpad `snap/GB_m3-defence.before.prefab`; 117 tiles, y 0..15):
```
_ _ _ _ _ _ _ _ . . . _ _ _ _ _ _ _ _ _   y15
_ _ _ _ _ _ _ . . . . . _ _ _ _ _ _ _ _
_ _ _ _ _ _ _ _ _ . _ _ _ _ _ _ _ _ _ _
_ _ _ _ _ _ _ _ _ T _ _ _ _ _ _ _ _ _ _
_ _ _ _ _ _ _ _ c b c _ _ _ _ _ _ _ _ _   y11
O O . . . . * . c . c . * . _ _ _ _ _ _
O O . . . . . . . . . . . . . . . a . _
. . a . . . . L . . . U . . . . a . . .   y8
_ _ _ _ _ . . . . . . . . . _ _ _ _ _ _   y7 (removed)
_ _ _ _ _ . . . _ _ _ . . . _ _ _ _ _ _   y6 (necks)
_ _ _ _ _ . * . _ _ _ . . * _ _ _ _ _ _
_ _ _ _ _ . . . _ _ _ . . . _ _ _ _ _ _
_ _ _ _ _ . . . _ _ _ c c c _ _ _ _ _ _
_ _ _ _ _ . . . _ _ _ O O c _ _ _ _ _ _
_ _ _ _ _ c c c _ _ _ O O c _ _ _ _ _ _
_ _ _ _ _ c . c _ _ _ . . c _ _ _ _ _ _   y0
hidden: toba 4,12 · masher 6,1 · w2 8,0 8,1 · w3 0,0 2,0 8,2; sword 10,9; deploy 4,8
```

After (108 tiles, y 1..15; rows 8 and up and both corridors unchanged):
```
_ _ _ _ _ _ _ _ . . . _ _ _ _ _ _ _ _ _   y15
_ _ _ _ _ _ _ . . . . . _ _ _ _ _ _ _ _
_ _ _ _ _ _ _ _ _ . _ _ _ _ _ _ _ _ _ _
_ _ _ _ _ _ _ _ _ T _ _ _ _ _ _ _ _ _ _
_ _ _ _ _ _ _ _ c b c _ _ _ _ _ _ _ _ _   y11
O O . . . . * . c . c . * . _ _ _ _ _ _
O O . . . . . . . . . . . . . . . a L _
. . a . . . . . . . . . . . . . a . U .   y8
_ _ _ _ _ . . . _ _ _ . . . _ _ _ _ _ _   y7 (necks, barricades)
_ _ _ _ _ . * . _ _ _ . . * _ _ _ _ _ _
_ _ _ _ _ . . . _ _ _ . . . _ _ _ _ _ _
_ _ _ _ _ . . . _ _ _ c c c _ _ _ _ _ _
_ _ _ _ _ . . . _ _ _ O O b _ _ _ _ _ _
_ _ _ _ _ c c c _ _ _ O O c _ _ _ _ _ _
_ _ _ _ _ c w c _ _ _ w w c _ _ _ _ _ _   y1
hidden: toba 4,12 · masher 6,2 · w2 8,1 8,2 7,1 12,9 11,8 · w3 0,1 2,1 8,3 1,1 6,1 · stone0..3 + stoneclosed 4,12
barricades: 0,7 1,7 2,7 6,7 7,7 8,7 -1,8 -1,9 -1,10 · sword 10,9 · shrine 10,10 (off-grid) · deploy 14,8
```
The east-corridor archers (11,8) and (12,9) are now hidden in w2. In the drawing they show as `a` on their tiles.

The row-removal step was a one-off (`execute_code`, not kept as a menu):
- It deleted the 9 cells of row 7 (none had an occupant).
- It moved the 42 cells with y ≤ 6 up 0.5 world units (one row) and renamed them, and their occupants moved with them.
- It also moved the 8 decor props below row 7 up one row (3 rocks, 4 light stands, the statue). The full-map `TestLevel` background stays where it was.

Idempotency: "Hold the Yard: Apply Wiring" was run, then run again. The second run left the prefab byte-identical (checked by diff). I repeated the check after the Masher-factor change below.

## Acceptance criteria

- [x] THJ's layout kept, row 7 removed, everything below up one: grid reads above; `TheTilesAndUnitsMatchThePaperBlock`, `TheNecksAreThreeWideAndTheCentreUnderTheYardHasNoTile`.
- [x] A wiring re-run no longer throws or undoes his layout. The constants follow his prefab (five at the stone, sword 10,9, Lucy's tile, mushrooms, nine barricades). Two runs, the second one changes nothing.
- [x] Start in the east corridor (Linda 13,9, Lucy 13,8, deploy 14,8): `TheSistersAndTheDeploySlotStartAtTheEndOfTheEastCorridor`.
- [x] Shrine art at the off-grid spot (10,10) under Environment, owned by the wiring: `TheShrineSitsUnderTheEnvironmentAboveTheSword`.
- [x] Enemies hold still until a hero stands in the yard; the arrival trigger fires only once the hero has stopped: `TheArrivalPlaysWhenAHeroStopsOnAYardTile`, `EveryEnemyInPlayWaitsForTheWalkInExceptTheWestPair`, `KeepUnitsPassiveUntilSignalTests`, `UnitsReachTilesSequenceTriggerTests`.
- [x] Together-move: Linda 2,8, Lucy 6,8, pick 4,8 at the same time, then the stone camera, Linda's line and the wake: `TheArrivalWalksTheThreeInTogetherThenWakesTheEnemies`, `MoveUnitsTogetherSequenceTests`.
- [x] Level start: stone in, camera on the heroes and the sword, no line: `TheLevelStartBringsTheStoneThenShowsTheHeroesAndTheSword`.
- [x] West Masher and Archer on the board, asleep, woken at yard clear: `TheWestCorridorPairSleepsUntilTheYardIsCleared`, `StageOneIsTheFiveAtTheStoneDead...`, `TheWakeSignalsAreSentOnlyByTheArrivalAndTheYardCleared`.
- [x] Waves:
  - Wave 2 is two Claws, a Worm on 7,1 and the two archers, which walk to 9,9 and 9,8 after the reveal.
  - Wave 3 is two Claws, a Black Claw on 8,3 and Worms on 1,1 and 6,1.
  - Tests: `TheOtherTwoWavesWaitHiddenInGroupOrder`, `TheSecondWavesArchersWalkToTheCorridorMouthAfterTheyComeIn`, `EachWormHasAFreeTileBesideIt` (own-wave check only, see risks).
- [x] Five stages; the last hold turn wins and has no end sequence: `FiveQueuedStages...`, `TheLastStageIsTheLastHoldTurnWithNoEndSequence`.
- [x] Outro order: release the pick, last notch, roll-away, Toba out, Toba's call, the four walk in together and leave the board, the closing stone, tally/question/fade/answer, Toba talk, outro cutscene. Test: `TheOutroRollsTheStoneAwayTakesEveryoneIntoTheCaveAndClosesIt`.
- [x] The "open" line is out of the flow and its asset is deleted (nothing else used it): `TheNotchesGiveThePickItsLinesAndTheWavesTheirBarks`, `EveryDialogueInTheYardFolderSaysAnApprovedLine`.
- [x] Paper block `m3-defence-5` parses clean and matches the constants: `TheBuildBlockParsesCleanWithTheLevelLines`.
- [ ] Play check (verifier/THJ): walk-in timing and camera, the simultaneous walks, archers' walk, the outro rush and stone close. Nothing here was run in Play mode.

## Tests

- Onboarding fixtures (`MISO.Core.Features.Onboarding.EditorTests`) were green after two fixes: a typo in the block (an archer's tile) and the worm test's scope.
- Full EditMode suite: **3150 tests, 3149 passed, 0 failed, 1 skipped** (`AIRegressionTest.Baseline_MatchesCurrentAI`, Explicit).
- `AIRegressionTest.Baseline_MatchesCurrentAI` run by name: **51 failures of 738 checks**, the same as the last recorded 51. Not re-baselined.
- The suite does not change the level prefab (byte-identical before and after the run).

## Chunks

### Chunk 1 (whole plan)

- Changed: all files above.
- Criteria met: all edit-mode criteria above. Play check pending.
- Decisions and loose ends: see the next sections.

## Reviews and checks

- (coordinator)

## Save reset

No.

## Decisions I made

- **Two new runtime parts and one option** (no core change):
  - `KeepUnitsPassiveUntilSignal`, a new component next to `KeepUnitsPassive`, which stays as it is. Two instances: "Enemies wait for the family" and "West corridor asleep". Their unit lists don't overlap, so releasing one never wakes the other.
  - `MoveUnitsTogetherSequence`.
  - `waitUntilSettled` on the tile trigger. Without it, the trigger can fire while the hero is still walking, because a walking unit sits on each tile of its path.
- **Shared walk code.** I extracted the walk helpers in `MoveGroupUnitSequence` so the new sequence reuses them. Behaviour is unchanged.
- **Who waits for the walk-in.** The list is every enemy in play at wiring time except the west pair: five at the stone, wave 1, the east lane = 11. Hidden waves come in after the walk-in, so they aren't listed.
- **The rush.** Walks: Toba 4,15, Linda 3,15, Lucy 5,15, the pick 4,14. They all start together on distinct stop tiles, and their paths cross through allies only (the family walks through allies). All four then fade out and leave the board, including any whose path was blocked. The pick hold is released first, because the held pick carries Unmovable.
- **Closing the cave.** A second instance of the start stone, in its own group (a group can be revealed only once).
- **Wave order and archer walks.** Wave group order is fixed so the archers' walk can name them by place (members 3 and 4 of w2). Units already of the right kind on a wave tile are kept. The Dark Claw on 8,3 was replaced by a Black Claw.
- **Health factors.** The west-corridor Masher keeps its prefab's factor (1). The old "every Masher 0.6" rule would have changed THJ's unit, so the 0.6 now applies only to the east-lane Masher. The first run had already written 0.6 on the west Masher; I reverted that override. Question below.
- **Camera start.** Set by the existing `CameraStartTool` with the tile override 11,9.
- **Arrival trigger tiles.** All 27 yard tiles (x 0..8, y 8..10).
- **Linda's line.** It reuses the old level-start dialogue asset (`M3Yard_Start_Linda_DialogNodeSequence`), so anything written in it in Unity is kept.

## Needs THJ

1. **West Masher health.** It now has full prefab health (factor 1). The east Masher is at 0.6. Keep it, or 0.6 like the east one? Leaving it is the safe choice; the waves are meant to be harder.
2. **Toba's call line** before the rush is a placeholder for narrative: "Inside, quickly. The stone will hold them back." (Toba). Keep, reword, or drop?

## Docs to update

- `design/levels` / wherever the `m3-defence-4` paper block is mirrored: replace it with `m3-defence-5` (in `MissionWiring.HoldTheYard.cs`; block tiles = prefab tiles − (-5,1)).
- `status.md` / `build-log.md`: round three built, play check pending.

## Risks and loose ends

- **Not play-checked.** Things only Play mode can confirm:
  - The arrival trigger's settled check, with a real hero walk.
  - Two hero kinds walking at once. Their move abilities are separate assets, but any end-of-move effect on a hero move is unverified.
  - The archers' walk.
  - The rush through 4,11 and 4,12 with enemies still on the board. Sisters boxed in by enemies don't walk but still fade out.
  - The closing-stone reveal on the freed tile.
- **Worm room.** The worms on 6,1 and 7,1 sit under the hidden Masher's footprint (6..7, 2..3), with no tile below them. They have room to split only if the Masher (in from the push) and the wave-2 worm have moved by then. The test checks the worm's own wave only. Watch it at the play check.
- **Waking enemies before the arrival.** Hitting an enemy from the corridor before anyone stands in the yard does not wake it (the Unaware tag set here is not one the tracker handles). The west pair also ignores hits until the yard is clear.
- **Linda's Watch facing.** The builder used to point it at the west front. After the walk-in she faces wherever her walk ended. Not set by the wiring.
- **Camera boundary** was not re-fitted after the row removal. The old boundary still covers the map, now with one empty row at the bottom. If needed: Tools > Levels > Assign Camera Boundary (Selected Level).
- **Stale override.** The prefab still has a stale override for `winObjectiveGroups.Array.data[5]` ("Finish them."). The array size is 5, so it is ignored in game, but `level_to_grid.py` still lists the text. It can be removed with Revert on that property, or left.
- **Unrelated files in the working tree.** `Content/Levels/Generic Levels/Medium/M2/LevelM2-C1.prefab` (+`canvasGroup` field) and `Scenes/PreloadScreen.unity` (+`applyFPSLimit`) are Unity re-serialisation noise, not this work. `miso.slnx` was already modified. Don't stage any of the three.
- **Trashed assets.** The old step lists and the orphaned assets went to the OS recycle bin, and they are also in git history.

## Proposed commits

1. `feat(onboarding): a sequence that walks named units together, a hold that keeps enemies still until a signal, and a settled-only option on the tile trigger` (plain):
   - `Features/Onboarding/MoveUnitsTogetherSequence.cs`(+.meta)
   - `Features/Onboarding/KeepUnitsPassiveUntilSignal.cs`(+.meta)
   - `Features/Onboarding/UnitsReachTilesSequenceTrigger.cs`
   - `Features/Onboarding/MoveGroupUnitSequence.cs`
   - `Features/Onboarding/Editor/MoveUnitsTogetherSequenceTests.cs`(+.meta)
   - `Features/Onboarding/Editor/KeepUnitsPassiveUntilSignalTests.cs`(+.meta)
   - `Features/Onboarding/Editor/UnitsReachTilesSequenceTriggerTests.cs`(+.meta)
2. `feat(level): Hold the yard opens with a walk-in, has shorter lanes, harder waves and ends with everyone going into the cave` (risky: prefab and regenerated sequence assets):
   - `Features/Onboarding/Editor/MissionWiring.HoldTheYard.cs`, `.Arrival.cs`(+.meta), `.Sequences.cs`, `.Stone.cs`, `.Lines.cs`, `.Pick.cs`
   - `Features/Onboarding/Editor/M3DefenceTests.cs`, `M3DefenceTests.Lines.cs`, `M3DefenceTests.Arrival.cs`(+.meta)
   - `Content/Levels/Greybox/GB_m3-defence.prefab`
   - `Resources/Sequences/M3Yard/`: every new, modified and deleted asset listed under What changed, each with its `.meta` (the deletions as removals).

## Other branches

None (THJ is on `main`; the working tree here is `master` with the same base).

## How to see it

1. In Unity: Tools > Onboarding > Hold the Yard: Apply Wiring (optional; the prefab is already wired, and a re-run changes nothing).
2. Start the Trail mission ("Hold the yard") from Home, or open `GB_m3-defence` through the usual level test path, with John or Mark as the free pick. No save reset needed.
3. **The start.** The stone appears and the camera shows Linda, Lucy and the pick at the far end of the east corridor with the sword on the way. End a turn without entering the yard: no enemy moves.
4. **The arrival.** Walk a hero onto any yard tile (x 0..8, rows 8..10).
   - Once it stops, the three walk together to Linda 2,8, the pick 4,8 and Lucy 6,8.
   - The camera shows the five at the stone (the Black Claw on the push tile) and Linda's line plays.
   - From the next enemy turn, enemies act. The west-corridor Masher and Archer stay still.
5. **The yard cleared.** Kill the five at the stone: the cave line plays, and the west pair acts from then on.
6. **The push.** Push with the pick on 4,11: the pick is held and the east Masher comes in.
   - Notch 1: wave 2 comes in at the bottom of the east lane (Claws + Worm), and the two corridor archers appear and walk to 9,8 and 9,9.
   - Notch 2: wave 3 comes in (two Claws west, a Black Claw east, two Worms).
7. **The win.** The third family turn start after the push wins. Then:
   - The stone moves and rolls away, and Toba comes out and calls.
   - Toba, Linda, Lucy and the pick walk into the cave together and fade out, and the stone comes back.
   - Then the tally, "Still counting?" / "…No.", the talk with Toba, and the outro.
