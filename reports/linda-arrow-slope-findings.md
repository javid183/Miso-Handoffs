# Linda's arrow slope and the catch kink (Explore, read-only, 2026-10-27)

**Root cause.** Arrows spawn at Linda's SpawnSource, local y 0.245 (`Unit_Linda.prefab:270-277`; added with her arms in `c18583734`, April). They fly to the target cell's `AnchorPoint`, the floor at y 0, because of `destinationMode` Cell and `travelEntireRadius` (`Projectile.cs:140-168`). Unit TargetPoints sit at 0.186.

**Affected arrows.**
- Slope: LindaAttackArrow (bow, Watch), LindaAttackFireArrow, LindaAttackHealArrow.
- LindaExplosiveArrow (Crescendo) uses VerticalFactor with an arc.
- The return arrow is already level (0.186 → 0.186).

**The kink.** On a catch, `FreezeArrow` snaps the arrow to `returnSource` (Mark's TargetPoint, 0.186), and the return copy spawns there. The arrow is at about 0.08 when it reaches Mark, so it jumps up.

**Fix chosen (THJ, D-278):**
- (a) On the three straight arrows, set `trajectoryMode` VerticalFactor with a straight-line `verticalFactorCurve` from (0,0) to (1,h), h about 0.19, so the flight is level at about bow height. Runtime movement, triggers, `CollectPreviewPathHits` and the clearance check all share `EvaluatePreviewPathPoint`. `ArrowLandingRules` and the landing marker work in cells.
  - Risk: `QuiverArrow` picks the landing cell as the nearest cell to `transform.position`. An end point 0.245 above the cell sits only 0.01 inside the half-cell. With h about 0.19 the margin is safe. Check the level cell spacing.
- (b) Freeze at the arrow's own path point (the projection of `returnSource` onto its path), and spawn the return copy, with its `_returnFrom`, from that point (`ProjectileCatchAndReturn.cs:148-149, 269-272, 309-319`).

**Height doesn't affect the catch.** `IsOnIncomingPath` uses cells; the sweep tests collider overlap. Mark's box covers y −0.01 to 0.221, so a level path at 0.19 sits inside it.

**Existing preview/runtime mismatch (not new).** The preview aims at the occupant's TargetPoint on an occupied cell; the runtime arrow in Cell mode aims at the floor.
