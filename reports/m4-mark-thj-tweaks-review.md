# Review: THJ's Memory 4 tweaks (`GB_m4-mark`, uncommitted, 2026-11-06)

Reviewer verdict: **FIX**. Read from the YAML and code; nothing played. The reviewer can't write files, so the coordinator saved this condensed copy. The implementer's test run backs the red-test list (10 Hearth reds). Coordinates are prefab cells; the design drawing's x is one higher.

## Must fix

1. **Two new hidden Claws give XP.** PrefabInstances `8226153317033840670` on (3,7) and `9221823542293816674` on (-1,4), group `left`, lack `lethalDamageXpBonus = 0` and inherit 3. This breaks the Hearth's no-XP rule; `NothingInTheHearthGivesExperience` is red. They also have no health factor override (the reviewer estimates about 9.6 HP, base value not read); THJ to confirm.
2. **Don't run `Tools/Onboarding/Wire Memory 4 (Mark)`.** `BuildSequences` runs first and edits sequence assets, then `PlaceClaws` throws (`Mark.Layout.cs:140`, cell (9,9) deleted). His sequences would be overwritten and the prefab left unsaved. If patched to run through, it would also recreate `Arrival_LucyRunsAhead` under a new GUID, restore old lines, camera and walk targets, move John back to (9,5), drop the `left` group and rewrite stages 2 and 3. Either update it to the prefab or retire it.
3. **`End_CameraToLedge` is one row too high.** `focusPoints` are (4, 5.25); the mother and cub midpoint is now (4, 4.75). `Hold_CameraUp` at (4.5, 4) is also a row high; look at it in play.
4. **Typo.** `GB_m4-mark.prefab:1597`: 'John: Cut the reinforement path.'

## Should fix or decide

5. The Claw moved to (7,7) isn't one of stage 3's five, so the level can win with it alive beside the end tile, and it can block the ending walks to (7,8) and (8,8).
6. The mother on (8,9) and cub on (7,9) now stand on walkable cells (old row 10 deleted). Units can walk onto them.
7. New lines and objective texts aren't in the narrative draft: "Lucy! Keep them busy!", "You deal with them. I'll save the cub.", "We need to cut their reinforcements.", "I'll make sure they stay in their hole.", stages 2 and 3 texts.
8. Lucy's new line uses `side: 0`; her other lines use right. Change only if not intended.
9. `Memory4Mark_Bloom_CameraToDen.asset` is used only by the wiring tool now.
10. The Claw revealed on (-1,4) stays on a pool tile, and `SpawnAt` fails when a unit stands there, so that pool can't spawn while it stays.

## Red tests

| Test | Why |
| --- | --- |
| `HearthMemoryLevelsTests.NothingInTheHearthGivesExperience` | Finding 1: real bug |
| `HearthMemoryMarkTests.TheFourHeroesStartOnTheirTilesAndInPlay` | John on (4,2), expected (9,5) |
| `.EveryClawStandsOnItsTileWithItsHealthAndHiddenState` | 15 Claws against 13; top Claws a row lower |
| `.TheArrivalAndTopGroupsHoldTheirClawsSwitchedOff` | 3 groups against 2; `top` tiles moved |
| `.ThereAreThreeQueuedStages` | Stage 3 group mode All, expected Any |
| `.StageTwoEndsWithJohnOnTheDenMouthAndPlaysTheHold` | Text changed |
| `.StageThreeWinsWhenAllFiveClawsByTheMotherAreDead` | Texts changed |
| `.TheBloomCutInPlaysWhenTheLevelStartsAndLucyCastsOnTheCrossing` | No camera step; Lucy's line changed |
| `.TheArrivalBoastsRunsLucyAheadRevealsMarksClawsAndResetsTheTurn` | Run now nested in `PostBloom` |
| `.TheEndingDropsTheMother...` | Destinations (7,8), (8,8), expected (7,9), (8,9) |

Apart from the XP test, these come from intended tuning: update the tests to the prefab, not the other way round.

## Verified statically

- **Objectives:** stage 1 any of Claws (1,4), (5,4), (3,5), (3,6) or cap 1. Stage 2 John on (6,5) or cap 2. Stage 3 all of (5 dead or turn 4) and (turn 4 or John on (6,5)). All `evaluationMode` 0, correct for a hold. Stage 3 can't complete before the `top` reveal.
- **At the cap** the level wins silently with both objectives unmet; he removed the "Turns left" line, so there is no warning. His choice; noted.
- **Sequence chain:** every GUID resolves, no dangling local fileIDs, reveal ids `arrival`, `top`, `left` exist, no unit moves before its reveal. `Bloom_LucyRunsAhead` keeps the old asset's GUID `eb4e71cc`.
- **Pools:** both `CP_Spawner_Hearth`, on (-1,4) and (3,7), 8 specific turns; all 59 cells under the Tilemap.
- **Facing:** no enemy left of Linda, Lucy or John lacks the override.

## Departures from the plan (all look deliberate)

John starts (4,2) and is scripted to (7,2); Lucy runs to (8,3) in the Bloom cut-in; intro camera sweep, start point (1.75, 1.5); 15 Claws; top Claws, mother and cub one row lower; visible two Claws now inside the Duo's reach from (8,5) (4 and 4; T13 open); stage 3 texts changed and it also needs John on the tile or the cap; new "Keep them busy" line.

Segment 4 of `plans/onboarding/2026-10-26-onboarding-levels.md` (line 306 on) still shows the pre-rework design. Update it from the prefab once tuning settles.

## Commit notes

- `PostBloom_ClawMove*` depend on `findUnitByTile`. Under HEAD's code all three would move Lucy, so commit the code first or in the same unit.
- Stage together: the `Arrival_LucyRunsAhead` deletion, `Bloom_LucyRunsAhead`, and both parent sequences (shared GUID).
- `MoveUnitSequence.cs` has mixed line endings (17 CRLF of 89, HEAD is LF): normalise to LF before committing.

## Needs a play check

- John's 6 steps from (7,2) to (6,5) through the passage (8,3)-(8,4) with Lucy standing on (8,3); stage 2's cap is 2.
- Mark and Lucy reaching the Duo tiles with John in the passage.
- Duo targets from (8,5): (8,7) 2, (9,6) 2, (7,7) 3, (9,7) 3, (9,8) 4, (10,7) 4. The (7,7) Claw could take a chain slot.
- PostBloom moves when stage 1 ends on the cap or after only one Bloom kill; PostBloom has no camera step, so moves may be off screen.
- Lucy's walk in the Bloom cut-in while `levelStarted` and `StartTurn` run in the same frame.
- Left pool timing while the revealed Claw stands on it; the intro sweep; the mother's fall with the corrected camera.
