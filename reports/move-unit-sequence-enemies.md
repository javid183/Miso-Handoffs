# Report: MoveUnitSequence works for enemies

Plan: none (size S bugfix)    Agent: miso-implementer    Branch: thj/onboarding
Outcome: done

## What changed

- miso/Assets/_Project/Core/Levels/Runtime/MoveUnitSequence.cs: new public static `PickMoveAbility<T>` (default empty-cell ability if it has a transporter, else first ability in `AbilityOrchestrator.Abilities` with an `AEffectTransporter`); `PlaySequence` uses it. Warnings now name the real unit (`unit.Nickname`) once found; when looked up by tile and not found, the warning names the tile. THJ's `findUnitByTile` edit is kept.
- miso/Assets/_Project/Core/Levels/Editor/MoveUnitSequenceTests.cs (new, plus .meta from Unity): four tests for the selection.

## Acceptance criteria

- [x] Unit whose walk preset isn't the default empty-cell action finds its transporter: tests `FallsBackToFirstTransporterAbilityWhenNoDefault` and `FallsBackWhenDefaultHasNoTransporter` (pure helper). Real Claw play check still needed.
- [x] Heroes keep their default move ability: `DefaultAbilityWithTransporterWins`; the default is tried first.
- [x] Warnings name the real unit: by reading; needs a play check to see the log.
- [x] Compile clean, EditMode suite: 1404 run, 4 new pass. Failures: `AIRegressionTest.Baseline_MatchesCurrentAI` (known) and 10 Hearth tests (below), none touched.

Failing Hearth tests (THJ's uncommitted GB_m4-mark/sequence edits, not fixed): `HearthMemoryLevelsTests.NothingInTheHearthGivesExperience` (Claws at (-1,4) and (3,7) have lethalDamageXpBonus 3); `HearthMemoryMarkTests`: `EveryClawStandsOnItsTileWithItsHealthAndHiddenState` (15 Claws, 13 expected), `StageThreeWinsWhenAllFiveClawsByTheMotherAreDead` (objective text), `StageTwoEndsWithJohnOnTheDenMouthAndPlaysTheHold`, `TheArrivalAndTopGroupsHoldTheirClawsSwitchedOff` (3 not 2), `TheArrivalBoastsRunsLucyAheadRevealsMarksClawsAndResetsTheTurn`, `TheBloomCutInPlaysWhenTheLevelStartsAndLucyCastsOnTheCrossing`, `TheEndingDropsTheMotherWalksLucyThenMarkToTheCubAndFadesToTheHearth` ((7,9) vs (7,8)), `TheFourHeroesStartOnTheirTilesAndInPlay` (John at (4,2), expected (9,5)), `ThereAreThreeQueuedStages`.

## Save reset

no

## Decisions I made

- "Prefer Walk mode" is not done: `AEffectTransporter.moveMode` is private with no public accessor, and the brief limits the change to this file. It takes the first transporter ability in orchestrator order. Heroes are unaffected (default first). A unit with several transporter abilities and no default could pick a jump or dash; an accessor on `AEffectTransporter` would fix that if needed.
- The helper is generic (`Func<T, AEffectTransporter>`) and `public`, because the tests are in the separate editor assembly (no InternalsVisibleTo) and `RuntimeAbility` is hard to build outside a level.
- The ability list used is `Abilities` (available only), same as `DefaultEmptyCellAbility`.
- Same bug elsewhere: the preset has `defaultEmptyGridCellAction: 0` on Deer, ArcherGoblin, BlackClaw, DarkClaw, DarkShaman, DarkWorm, GoblinQueen, MasherGoblin and DomEnemy walk presets; all benefit from the fallback.

## Needs THJ

none

## Docs to update

- none

## Risks and loose ends

- Line endings: the working copy of MoveUnitSequence.cs is mixed (17 CRLF lines of 89, from THJ's edit; HEAD is pure LF). I did not normalise; my added lines are LF. No BOM. Git warns about CRLF. The brief said CRLF; it was not.
- The same ability's `ignoreRelationOnWalk` is passed to the effect (DarkClaw walk: 1 = Ally), so Claws walk through other Claws. Because of that, a Claw is probably fine to pass through but not to end on.
- The sequence plays the walk animation and stops it even when no move happens (see ClawMove2).

## Proposed commits

1. fix(levels): move-unit sequence falls back to any transporter ability and names the real unit in warnings: MoveUnitSequence.cs, Core/Levels/Editor/MoveUnitSequenceTests.cs(.meta) (plain). Note MoveUnitSequence.cs also holds THJ's uncommitted `findUnitByTile` edit, so the commit takes both; split if THJ wants.

## Other branches

none

## How to see it

1. Open GB_m4-mark, Play. The Claw moves in Memory 4 should now walk (see read-through below for ClawMove2).
2. Console: no "has no transporter" warning for Claws. Run EditMode > MoveUnitSequenceTests.

## Read-through of the three moves (no changes made)

Common: effect params are Radius=int.MaxValue and ignoreRelationOnWalk=Ally (from the preset), mover = the Claw. `FindPath` (A*, 4-neighbours, cost 1 per cell, no tie-break; first lowest f in the open list wins) treats a non-goal cell as walkable if empty or occupied by a unit whose faction relation to the mover is in the ignore flags, i.e. an ally. It assumes a faction counts as its own ally in the level's relations map (not checked). The goal cell must be truly empty (`IsFootprintEmpty` uses `IsWalkable`, so no ally exception). Transporter settings: Walk, `ignoreAlliesWhileWalking` 0, `goShortestWhileWalkable` 0, `ignorePathCost` 0. `MoveEntity` unplugs the unit from the cell it leaves; a cell occupied by an ally is entered visually (the unit lerps onto it) but `CanOccupy` fails, so it fires the passed-by event and continues without plugging. `CurrentCell` stays on the last plugged cell, so the next `UnplugEntity` finds nothing and returns (no null error). It plugs on the first free cell and on the final cell.

- **PostBloom_ClawMove, 6,4 to 7,7:** Manhattan 4, so a four-step path exists if 7,7 is empty and the cells on the route are empty or hold Claws. Which of the equal-length routes A* returns depends on cell order and I can't tell without the grid; any Claw on it is walked through, with a passed-by event. Fails silently only if 7,7 is occupied (see ClawMove2) or enclosed by non-ally blockers.
- **ClawMove1, 0,4 to 2,4 through 1,4:** path [0,4; 1,4; 2,4]. 1,4 is an ally cell, so allowed; 2,4 must be empty. The Claw unplugs from 0,4, slides onto 1,4 (visually overlapping the other Claw, passed-by event), slides on and plugs at 2,4. Tile effects of each path cell are applied as it leaves it, including 1,4. It works, assuming 2,4 is empty and the map treats same-faction as allies.
- **ClawMove2, 3,7 to 3,5 with 3,6 passable and 3,5 occupied:** the goal 3,5 is occupied, so `FindPath` never expands into it, returns null with length and cost 0. `ApplyUnguarded` returns at the `cost <= 0` check, so nothing moves, no warning, `IsInProgress` stays false and the sequence continues straight away. Side effect: `AEffectBase.Apply` runs `GotTargeted(owner)` on the occupant of 3,5 before that, so the Claw on 3,5 is marked as targeted by the mover. The fix is in the level data: pick a free destination cell (for example move the Claw off 3,5 first, or end on an empty cell).

---

# Round 2

Editor check first: Edit mode, no Prefab Mode stage open, only PreloadScreen loaded, so the prefab and asset edits went ahead.

## What changed

- Core/Levels/Runtime/MoveUnitSequence.cs: the destination is checked before the animation or the transporter. It calls `AEffectTransporter.TryBuildPreviewPath` with the same `AEffectParameters` as `Apply`, and also `unit.CanOccupy(destCell)`. If either fails it logs a warning naming the unit, its tile and the destination, then ends the coroutine (the base `Play` ends the sequence, so the chain continues). A cancelled move never reaches `Apply`, so `GotTargeted` is not called on the occupant. File normalised to LF, no BOM (0 CRs).
  - `TryBuildPreviewPath` respects modes: Walk uses the same path search and cost check as `Apply`; Teleport and Jump return a two-cell path unless start equals destination. The `CanOccupy` check covers the occupied goal for those two. Preview does not consult `MovePathOverride`; the sequence never sets one.
- Content/Levels/Greybox/GB_m4-mark.prefab: `lethalDamageXpBonus = 0` override added on PrefabInstances 8226153317033840670 (3,7) and 9221823542293816674 (-1,4), HP untouched; `winObjectiveGroups[1].objectives[0].displayTextTemplate` now 'John: Cut the reinforcement path.' Text edits to the YAML only (no Unity re-save), so nothing else moved; the file was already modified by THJ, so its diff also shows his earlier changes.
- Resources/Sequences/Hearth/Memory4Mark/Memory4Mark_End_CameraToLedge.asset: both `focusPoints` now (4, 4.75).
- Features/Onboarding/Editor/HearthMemoryWiring.Mark.cs: `[MenuItem("Tools/Onboarding/Wire Memory 4 (Mark)")]` removed (that line only); `Run()` and the constants stay.

## Acceptance

- [x] Compile clean.
- [x] `NothingInTheHearthGivesExperience` green.
- [x] Run of 1404 tests: failures are only `AIRegressionTest.Baseline_MatchesCurrentAI` and the 9 `HearthMemoryMarkTests` layout tests (EveryClawStandsOnItsTile..., StageThreeWinsWhen..., StageTwoEndsWith..., TheArrivalAndTopGroups..., TheArrivalBoasts..., TheBloomCutIn..., TheEndingDrops..., TheFourHeroesStart..., ThereAreThreeQueuedStages). No other failure; the layout tests were not touched.
- [x] Prefab changes this round are exactly the three items above (inserted by text edit).
- No test for the reachability check: it needs a live grid, cells and a unit, so it can't run in edit mode cleanly. Needs the verifier's play check: ClawMove2 should now log the warning, not animate, and carry on.

## Proposed commits (round 2)

1. fix(levels): move-unit sequence falls back to any transporter ability, names the real unit and cancels blocked moves: Core/Levels/Runtime/MoveUnitSequence.cs, Core/Levels/Editor/MoveUnitSequenceTests.cs(+.meta) (plain). Also contains THJ's `findUnitByTile` edit.
2. chore(onboarding): retire the Memory 4 wiring menu item: Features/Onboarding/Editor/HearthMemoryWiring.Mark.cs (plain).
3. fix(onboarding): Memory 4 level data (hidden Claws give no XP, objective typo, ledge camera): GB_m4-mark.prefab, Memory4Mark_End_CameraToLedge.asset. This commit depends on THJ's own uncommitted edits. The prefab diff also holds his layout changes and the camera asset may be new or changed by him, so with it staged the commit would contain his work plus these three changes; the three changes alone are: two `lethalDamageXpBonus` overrides, the typo fix, the two camera focus points.

---

# Round 3 (review fixes)

Editor was in Edit mode. No prefab or asset changes.

## What changed

- Core/Levels/Runtime/MoveUnitSequence.cs:
  1. Tile lookup is now `FindUnitOnCell(cell)` = `cell.OccupantEntity as GUnit`. Checked: `OccupantEntity` returns null for a dead occupant, and `PlugEntityInternal` calls `SetSlot` on every footprint cell, so a big unit is found from any of its cells.
  2. `Radius = int.MaxValue - 1` with a comment (the transporter adds 1).
  3. The wait is `transporter.IsInProgress && unit && unit.isActiveAndEnabled`.
  4. Nickname lookup requires `u.IsAlive`.
  6. Removed the unused `using MISO.Core.Systems.AbilitySystem.Abilities` (mine) and `using MISO.Core.Management` (compiles without it), put `System.Collections.Generic` in order, removed the stray blank line and the trailing whitespace. LF, no BOM.
  - New small public helpers for the tests: `FindUnitOnCell` and `CanReachDestination` (the preview path plus `CanOccupy`, used by the sequence).
- Core/Levels/Editor/MoveUnitSequenceTests.cs: now in `MISO.Core.Levels.EditorTests`, with hand-built cells and units (reflection on the cell fields, like `AttackReachTests`). New tests: living occupant found, dead unit skipped, empty or null cell gives null, free neighbour accepted, occupied destination rejected, no path rejected. Plus the four selection tests. All 10 pass.
- Features/Onboarding/Editor/HearthMemoryWiring.Mark.cs: the summary now says the tool is retired, `GB_m4-mark` is hand-edited, and the code stays for the test constants.

## Acceptance

- [x] Compile clean.
- [x] Full EditMode run, 1410 tests: failures are only `AIRegressionTest.Baseline_MatchesCurrentAI` and the 9 `HearthMemoryMarkTests` layout tests.

## Open notes

- Point 3 does not cover a refused `Apply` while the flag is stuck on from another unit: the mover is still active, so the wait lasts as long as the flag does. A refusal cannot be told apart from a slow walk here. The pre-check (`CanReachDestination`) removes the usual refusals (no path, occupied end), so the remaining case is a leftover flag from an earlier interrupted walk of any unit sharing the effect asset. Fixing that belongs in `AEffectTransporter` (per-mover progress), a core change for THJ.
- Not done by instruction: a `moveMode` accessor on `AEffectTransporter` (so the fallback could prefer Walk), and the ability upgrade-level edge case.

## Proposed commits

Same three as round 2; `MoveUnitSequence.cs` and its test file go in commit 1, `HearthMemoryWiring.Mark.cs` (menu item and summary) in commit 2.
