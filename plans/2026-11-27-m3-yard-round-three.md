# Hold the yard, round three: walk-in, shorter lanes, a real threat during the hold, the cave exit (proposal)

Size: M    Tier: 2 inside THJ's requests (2026-11-27)    Assigned to: miso-implementer (opus) after THJ's answers
Branch: all (THJ is on `main`)
Status: built and committed 2026-11-27 (003aa6189, edf2e9b81); THJ's play findings in playtests/2026-11-27-m3-yard-round-three-play.md

Level `Content/Levels/Greybox/GB_m3-defence.prefab`, wiring `Features/Onboarding/Editor/MissionWiring.HoldTheYard*.cs`, tests `M3DefenceTests*.cs`.

THJ's problem: once the yard is clear, ending every turn wins the hold; the enemies never get close.

## THJ's tweaks (uncommitted), read with `tools/level_to_grid.py`

Prefab coordinates (GridCell names):
- Cave interior above the stone: (4,13), (2..6,14), (3..5,15).
- West corridor x -5..-1, rows 8..10; barricades on (-1,8), (-1,9), (-1,10); a Masher (2x2, anchor -5,9) and an Archer Goblin on (-3,8).
- East corridor x 9..13 rows 8..9, plus (14,8); Archer Goblins on (12,9), (11,8); the Heavenly Sword moved to (10,9).
- The stone opening is now five: Dark Claws (3,11), (5,11), (3,10), (5,10) and a Black Claw on the push tile (4,11).
- Lucy (7,8) to (6,8). Mushrooms (1,4), (8,4) to (1,5), (8,5); two more on (1,10), (7,10).
- Three more Dark Claws in play in the east lane: (6,3), (7,3), (8,3).

Conflicts with the wiring (a re-run today would break or undo them):
- `OpeningClawTiles` expects one Dark Claw on 4,11: the run throws (Black Claw). The yard objective must list all five.
- `RelicTile` 8,10: a re-run moves the sword back out of the corridor.
- `LucyTile`, `MushroomTiles`, the six-barricade list, the paper block (`m3-defence-4`) and most `M3DefenceTests` pin the old layout.

## Changes (THJ's 1–9)

1. **Start in the east corridor.** The sisters and the pick's deploy slot on the corridor's far end (proposed: pick 14,8, Linda 13,9, Lucy 13,8). The sword stays on 10,9 on the way.
2. **Shrine art** (`Features/Player/Shared/DivineRelics/Shrine/Shrine.prefab`, art only, no scripts or colliders) as scenery on the off-grid spot (10,10) above the sword, placed the way `LevelDivineRelicRoom` places it (under the level's environment, not a child of the pickup). The wiring owns it.
3. **Arrival.** `UnitsReachTilesSequenceTrigger` (already used here for the west wall) on the yard's east edge plays a sequence: input off, the three heroes walk to Linda 2,8, Lucy 6,8, pick 4,8 **at the same time**, then the camera tour that opens the level today, input on. New: a small feature sequence that moves named heroes together (`MoveGroupUnitSequence` only moves hidden-group members; there is no parallel container). It finds the sisters by nickname and the pick as the other Bergson; walks are planned so paths don't block each other. No core change.
4. **Remove row 7**; everything below it moves up one (lanes become rows 1..7, barricades on row 7, east Masher anchor 6,2, waves +1, mushrooms (1,6), (8,6)). Rows 8 and up and both corridors stay. A one-off editor step moves the cells and their occupants; the wiring constants follow.
5. **East corridor archers** (12,9), (11,8) hidden in the second wave's group; at notch 1 they come in and walk (scripted, `MoveGroupUnitSequence`) to the corridor mouth (proposed 9,8 and 9,9), then the AI takes them.
6. **West Masher** (and its archer, see the questions) on the board but asleep for the yard fight; woken later.
7. **Dark Worms** in the waves (1x1; they split into a free neighbour cell when hit, so each gets room).
8. **Waves slightly harder** (proposal in the questions).
9. **No "Finish them".** Five stages: yard, push, three hold turns. The last hold turn wins. The outro: the stone rolls away, Toba comes out, Toba, Linda, Lucy and the pick rush into the cave together, the stone closes behind them, then the tally lines and the Toba talk, then the outro cutscene. The notch-3 sequence's roll-away, release and the pick's "open" line move into the outro (the last stage's own end sequence never plays); the "open" line hands over to a fight that no longer happens, so it goes. Optional new Toba call line before the rush (narrative).

## THJ's answers (2026-11-27)

- Walk-in: the player walks (D-799). Every enemy holds still (no moves, no attacks) until a hero stands on any yard tile; the arrival sequence then moves the three heroes together and wakes the enemies. If a hero ends the turn short of the yard, the enemies still wait. Level start: the stone comes in and the camera shows the heroes and the sword; the camera on the stone Claws and Linda's start line move into the arrival sequence.
- West Masher and the west archer (-3,8): on the board, asleep through the yard fight, woken when the yard is cleared (D-800). Fallback if too hard: at the push.
- The east Masher (hidden at the bottom of the east lane, comes in at the push) stays as it is.
- Waves (D-801): wave 2 = its two Claws + one Dark Worm (7,1) + the two east archers (walk to 9,8 / 9,9 after the reveal); wave 3 = its three Claws, the east one a Black Claw, + Dark Worms (1,1), (6,1). Tiles after the row removal.

## Build notes

- Holding enemies still and waking them: look at `KeepUnitsPassive` (Unaware tag, no release), `HoldUnitsUntilSignal` (player units only) and `EnemyAlertTracker` (`WakeMovedUnit`, `UnitAlerted`). One small feature component that keeps listed enemies (or all enemies) passive until a signal, usable for both the walk-in and the west pair. No core change; if one is needed, stop and report.
- Revealed waves come in alert (level alert all). The asleep pair must stay asleep under alert-all and despite sight/alert spreading.
- The pick is held at the stone (`HoldPickOutOfCombat`) when the level is won: check the outro's moves work on a held unit (release first if needed).
- The rush into the cave: four walkers through 4,12 (Toba's and the stone's tile); paths must not block each other (Toba first, or staggered). Units walk in and hide (`HideUnitsSequence` / `HideNamedUnitSequence`); then a stone variant comes back on 4,12.
- Row removal: a one-off editor step (not kept as a menu) moves every cell with y ≤ 6 and its occupants up one and deletes row 7; GridCell names follow. Snapshot the prefab to the scratchpad first; afterwards `tools/level_to_grid.py` must show THJ's layout with only row 7 gone and the lower part shifted.
- Re-running "Hold the Yard: Apply Wiring" must keep THJ's layout: constants, the paper block (new id `m3-defence-5`) and the tests follow his prefab, not the reverse. The wiring owns the nine barricades, the sword on 10,9, the shrine, the start tiles.
- New statics need a `PlayModeStaticReset` hook. No private IDs in code, comments, test names. Keep line endings/BOM.

## Test plan

Covering: `M3DefenceTests*`, the new sequence's tests, `UnitsReachTilesSequenceTrigger` tests, Onboarding fixtures. Paper block re-read to `m3-defence-5` (designer gate 7). Then reviewer, verifier full EditMode. AI regression: run it (new enemy placements; report the count against 51).

## Proposed commits (after THJ's play check)

1. The together-move sequence + tests (feature).
2. Hold the yard round three: wiring, block, tests, prefab, sequences.
