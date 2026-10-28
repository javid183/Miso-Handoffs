# Report: Linda's straight arrows fly level, no kink at the catch

Plan: decision D-278 (no plan file)    Agent: miso-implementer    Branch: thj/linda-quiver (HEAD 91f40e903)
Outcome: done (written and API-checked only; the editor is open, so nothing was compiled or run)

## What changed

- `Features/Player/Linda/Prefabs/LindaAttackArrow.prefab`, `LindaAttackFireArrow.prefab`, `LindaAttackHealArrow.prefab`: `trajectoryMode` 0 -> 2 (VerticalFactor). `verticalFactorCurve` replaced by two keys, (0,0) and (1,0.19), slopes 0.19, tangentMode 21 (broken, linear both sides), pre/post wrap ClampForever (8). The old arc curve was unused leftover data. New field `travelsWholeRange: 1` on their QuiverArrow.
- `Features/Player/Linda/Scripts/Quiver/QuiverArrow.cs`: new serialized `travelsWholeRange` plus the `TravelsWholeRange` getter (default false, so Explosive and Return are unchanged).
- `Features/Player/Linda/Scripts/Quiver/QuiverAimPresenter.cs`: the landing marker now passes `arrow.TravelsWholeRange` instead of `TrajectoryMode != VerticalFactor`.
- `Features/Player/Mark/Scripts/CatchPointRules.cs` (+ .meta): pure helper `FreezePoint(arrow, hand, pathDirection)`.
- `Features/Player/Mark/Scripts/ProjectileCatchAndReturn.cs`: `TryCatch` computes the catch point once; `FreezeArrow` and `PrepareProjectileClone` (and so `_returnFrom`) both use it.
- `Features/Player/Mark/Scripts/Editor/CatchPointRulesTests.cs` (+ .meta): 6 pure tests.
- `Features/Player/Linda/Scripts/Quiver/Editor/LevelFlightWiringTests.cs` (+ .meta): 7 wiring tests.

LeftUntouched: LindaExplosiveArrow, LindaAttackArrowReturn, `Projectile.cs` (core, read only), AIRegressionTest. All files LF, no BOM, as before.

## h and the margin

h = 0.19. Cells are 0.5 world units (`m_CellSize` 0.5 in LevelBase; the 1.0 one is only the tile palette), so half a cell is 0.25.
- Path at progress t = bow point + t * (aimed cell anchor - bow point) + (0, 0.19 t). At t=1 it ends at anchor + (0, 0.19), not at the floor. Bow height is 0.245, so the height goes 0.245 -> 0.19 over the flight (a 0.055 total drop, was 0.245), which reads as level.
- For a vertical shot the end sits 0.19 above the aimed anchor. Nearest-cell margin = 0.25 - 0.19 = 0.06 (0.245 would have left 0.005, which is why not exactly level). Horizontal shots are unaffected by it. The last-frame overshoot is also harmless: curve is clamped, so it can't wrap back to 0.
- If landing ever misbehaves on vertical shots, lower h toward 0.17 (margin 0.08). The wiring test caps h at HalfCell - 0.05.

## Code checks (VerticalFactor)

- Runtime `Update` -> `GetPathPointInterpolated`, `CollectPreviewPathHits` and (via `GetPathPointInterpolated`) `CheckTrajectoryClearance` all go through `EvaluatePreviewPathPoint`. `OnTriggerEnter2D` is physics overlap of the collider that Update moves, so it follows the same path. Verified in `Projectile.cs`.
- Nothing else branches on `trajectoryMode` except: the Path-only preview spline build (not used by Direct/VerticalFactor, same as before), `OnDrawGizmos` (editor drawing only), and the presenter. `travelEntireRadius` is read in `Initialize` and `ResolvePreviewTargetCell` and is independent of the mode, so range, targeting and destination are unchanged. Damage, hit activation use `effectActivationMode`, not the mode.
- The presenter inference was the only reader of `TrajectoryMode` in game code, and it would have flipped to "stops at the aimed cell" for these arrows. `travelEntireRadius` is private on the core `Projectile` with no getter, so I added a serialized `travelsWholeRange` on the non-core `QuiverArrow` instead (set 1 on the three arrows; a wiring test checks it equals the projectile's flag on all five Linda arrows, so they cannot drift). Same marker behaviour as before: whole-range for bow/Fire/Heal, aimed-cell for Explosive.
- `QuiverReadabilityTests` calls `MarkerCell` with the bool directly; no test assumed the mode, no change needed.

## The catch

- Catch point = Mark's `returnSource` position projected onto the line through the arrow along `DirectionNormal` (so Mark's x for a horizontal shot, the arrow's own height; a long frame that carried it past him is put back on him). It stays inside Mark's collider (box y -0.01..0.221 vs the arrow's ~0.19-0.245, plus its own 0.1 circle) and each arrow is looked at once anyway.
- `FreezeArrow` moves the arrow to the catch point; `_pathPosition` is still saved first, so a decline restores it. The return copy spawns at the same point and `_returnFrom` is the same point, so `ReturnFlightClamp` still gets (`_returnFrom`, Linda's destination).
- If `returnSource` is not set the hand falls back to the catcher's transform (the old spawn fallback); the arrow is then moved along its path to it, where before it stayed put. Mark has it set.

## Acceptance criteria

- [x] Three arrows VerticalFactor, linear curve ending at h: `LevelFlightWiringTests` (needs a run).
- [x] Explosive and Return unchanged: tests `ExplosiveArrow_KeepsItsArc`, `ReturnArrow_KeepsItsDirectFlight`.
- [x] Marker inference reads the whole-range flag: wiring test + play check.
- [x] Freeze-point projection: `CatchPointRulesTests`.
- [ ] Looks level / no kink / landing tile correct: play check only.

## Save reset

No.

## Decisions I made

- Flag on `QuiverArrow` rather than reflection into the core `Projectile` (no behaviour change; core untouched).
- ClampForever on the new curves (the old ones were Loop) so the overshoot frame cannot drop the arrow.
- Projection uses the grid `DirectionNormal`, as the brief said, not the arrow's heading.

## Needs THJ

none

## Docs to update

- Quiver tech note (if any) can mention `QuiverArrow.travelsWholeRange` must match the projectile's `travelEntireRadius`.
- build-log and status after play-check.

## Risks and loose ends

- Not compiled or run (editor open). Run the tests below first.
- Preview/runtime aim mismatch on occupied cells (preview aims at the occupant's TargetPoint, Cell-mode runtime at the floor) is untouched and now slightly more visible only in height, not in cells.
- Any other prefab or scene that overrides these three arrows' trajectory fields would need checking; none was found under `_Project`.

## Tests for THJ (Test Runner > EditMode)

- `MISO.Core.Features.Bergsons.EditorTests.LevelFlightWiringTests` (7)
- `MISO.Core.Features.Bergsons.EditorTests.CatchPointRulesTests` (6)
- Existing: `CatchReturnWiringTests`, `QuiverReadabilityTests`, `QuiverWiringTests`, `ReturnFlightClampTests`, `CatchFreezeRulesTests`, and the full suite (only `AIRegressionTest.Baseline_MatchesCurrentAI` may stay red).

## Proposed commits

1. `feat(linda): marker reads a whole-range flag on the arrow instead of the trajectory mode`: `QuiverArrow.cs`, `QuiverAimPresenter.cs` (plain; must land with 2)
2. `feat(linda): straight arrows fly level from the bow`: the three `.prefab` files, `LevelFlightWiringTests.cs` + `.meta` (data; builds with 1; wiring test needs the flag from 1, so commit 1 and 2 can be squashed if preferred)
3. `fix(mark): a caught arrow stops on its own path and the return starts from the same point`: `CatchPointRules.cs`, `ProjectileCatchAndReturn.cs`, `CatchPointRulesTests.cs`, and the three `.meta` files (plain, independent of 1-2)

Never stage the TMP fallback asset or the two ProjectSettings files.

## Other branches

main needs the level-flight change too (prefab data and the `QuiverArrow` flag with the presenter change), if it has Linda's quiver arrows; the catch fix needs it as well if main has Mark's catch.

## How to see it

1. Close nothing; let Unity recompile (Ctrl+R) and run the tests above.
2. Play a level with Linda. Fire the bow in all four directions (left, right, up, down): the arrow should fly level, no tilt into the floor; check on the ground arrow the landing tile is the same as before (end of range, or last enemy hit), and the landing marker while aiming shows the same tile.
3. Same for Watch (Fire/Heal arrows) and both Duos that fire Linda's arrow.
4. Crescendo (Explosive) still arcs and its marker is on the aimed cell.
5. Mark behind a shot: catch with the prompt (no V needed beyond the press): the arrow stops in his hand without jumping, and the return arrow leaves from that exact spot and ends on Linda.
6. Decline the prompt: the arrow carries on from where it was on its path and lands as usual.

## Review fixes (after the reviewer's FIX)

Not compiled or run (editor open).

- **Landing cell (must fix).** `QuiverArrow.LogicalEndCell` now gives the end cell of a whole-range shot from the grid: the owner's cell at launch, the shot direction (`Projectile.DirectionNormal`, public), the radius from the shot's ability (`StatAttributesContext as RuntimeAbility`, `Parameters.radius`), through the existing pure `LandingMarkerRules.EndOfFlight` (farthest existing cell along the line). No core change needed. The last-enemy-hit cell is unchanged, and `ArrowLandingRules` still picks the landing. Position (`NearestCell`) is only the fallback when the arrow is not whole-range (Crescendo, the return arrow: unchanged behaviour, it ends on the floor with a zero lift), has no owner cell (copies), or the ability or direction can't be read.
  - Limit: the direction comes from `DirectionNormal` (rounded), which equals Projectile's sign-based direction for aimed lines and diagonals, the only aims Linda's rays allow. A knight-move aim would differ, as it does nowhere else in the quiver code.
  - Horizontal shots had the same overshoot exposure in Direct mode (0.25 margin, so rare); the logical end removes it too. Because of this, the 0.19 lift no longer affects landing at all, so the margin argument above is moot for landing.
- **Test:** the constant-vs-constant test is replaced by `LogicalEnd_IsTheFarthestCellInRange_InEveryDirection` (up, down, left, right) and `LogicalEnd_StopsAtTheLastCellThatExists`, on the real rule.
- **Tangents:** all six keys now `tangentMode: 69`.
- **Comments:** "Mark's hand" wording fixed in `ProjectileCatchAndReturn.cs` (three places, comment at the freeze rewrapped) and `CatchSweep.cs`.
- **Commit units now:** (1) `QuiverArrow.cs`, `QuiverAimPresenter.cs`, the three prefabs, `LevelFlightWiringTests.cs` + `.meta`: `feat(linda): straight arrows fly level and land by the grid`; (2) the catch point: `CatchPointRules.cs`, `ProjectileCatchAndReturn.cs`, `CatchSweep.cs`, `CatchPointRulesTests.cs`, and the `.meta` files: `fix(mark): a caught arrow stops on its own path and the return starts from the same point`.
- **Extra play steps:** fire upward at an empty row so the arrow misses everything: it must land on the end-of-range tile, not one past it. Do it at about 30 and at 60 fps (Application.targetFrameRate or the Game view stats), several times, for up, down, left and right. Also watch for low-collider enemies on horizontal shots (the arrow now flies at about 0.19-0.245).
