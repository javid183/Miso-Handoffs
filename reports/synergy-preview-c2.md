# Report: Synergy aim preview, chunk C2 (Tempest Bloom preview)

Plan: plans/onboarding/2026-11-10-synergy-aim-preview-tech.md (section "C2 / C3 revised", D-494)    Agent: miso-implementer    Branch: thj/after-hearth
Outcome: done (play check pending). One finding needs THJ: the real Bloom very likely sends a fourth copy back toward Linda (see Needs THJ).

## Step 1: who draws what (investigation)

None of this needed a core edit. Every piece is a public core method the presenter only calls.

| Visual | Drawn by | Core? | How the preview uses it |
| --- | --- | --- | --- |
| Linda's lane tiles (the glowing tiles) | `FactionControllerBase` lights `PhaseData.ActiveAbilityRangeCells` with `GridCell.SetHighlight(true, level, …)` when the ability is picked (her bow has `straightDirectionCellsOnly`, so the range is her four lanes). Nothing redraws them on hover. | yes (called only) | Reads the public `AbilityRangeCells` getter. Hides with `SetHighlight(false)`, gives them back with `SetHighlight(true, sameLevel)` (the controller's level formula), and lights copy lanes with `SetHighlight(true)`, so they get exactly the same look. |
| The chevrons (blue >>> by her feet) | `GridCell.SetAimDirectionPreview`, one `aimDirectionPreviewVisual` per cell. `PlayerController` sets it on her `ActiveCell` (and an approach cell) and clears only those. | yes (called only) | Sets it on each copy-lane cell (the overlay cell of a unit standing there), clears its own cells only, and never touches Linda's cell. |
| HP preview (bars and skull) | `PlayerController.ShowDamagePreview` → `AbilityDamagePreview.ComputeFor` → `GUnit.ShowDamagePreview` → `EntityInfoPanelUI`. `HideDamagePreviews` hides only its own `_damagePreviewUnits`. | yes (called only) | Calls `GUnit.ShowDamagePreview` / `ShowInfoPanel(false, Damage)`. Merge: see below. |

Merging with PlayerController's damage preview works cleanly through public calls:
- The normal preview doesn't know about the Cyclone: it carries the bow's damage on past the Cyclone (`Projectile.CollectPreviewPathHits`). While the Bloom is on, the presenter works out the whole shot: the normal damage (the same `AbilityDamagePreview.ComputeFor` call the controller makes) counts only for units before the Cyclone, and each copy's damage is added on top. Units past the Cyclone that no copy reaches lose their bar. It re-applies its values every frame while on, because the controller redraws on every hover.
- Giving back: the presenter's hover listener runs before the controller's (the controller re-subscribes each time it enters target selection, so it always comes later). So when a hover turns the Bloom off, the presenter hides its bars and restores her tiles first, and then the controller draws the new aim normally. Cancel, ability switch, end of turn and end of level are caught by `LateUpdate`, after the controller has already cleared its own.

## What changed

Paths under `miso/Assets/_Project/`. All files are LF with no BOM, like their neighbours.

- `Features/Player/Lucy/Scripts/TempestBloomGeometry.cs` (new, + `.meta`): pure helper, grid coordinates only, no Unity objects. It covers:
  - the copy directions: existing orthogonal neighbours, in the grid's adjacency order, except the one exactly opposite the incoming direction;
  - `IncomingDirection` (the projectile's own sign rule);
  - the copy's end: the farthest existing cell within the full reach from the Cyclone, crossing missing cells, which mirrors `Projectile.Initialize`'s travel-entire-radius walk;
  - the copy lane cells, plus `StepsAlong` and `StraightStep`.
- `Features/Player/Lucy/Scripts/LucyCycloneProjectileScatter.cs`:
  - The trigger now skips directions through `TempestBloomGeometry.IsScatterDirection` and gates through a new public `WouldScatter(prefab)` (whitelist + the owner faction's unlock), which the preview also calls.
  - New read-only getters `Cell`, `IsInPlay` and `ScatterSourcePosition`.
  - Behaviour is unchanged: same checks in the same order, same loop over `AdjacentCellsMap`, same clone call.
- `Features/Player/Shared/Synergies/SynergyLanePresenter.cs`: now `partial`. The hover listener calls `RefreshBloom()`; `OnDisable` and `OnDestroy` call `ClearBloom()`. The header comment is updated. The Flare code is unchanged.
- `Features/Player/Shared/Synergies/SynergyLanePresenter.Bloom.cs` (new, + `.meta`): the Bloom preview. It turns on when all of these hold:
  - the player is aiming in their own turn;
  - the hovered cell is legal;
  - the next click fires a projectile spawner;
  - the aim is a straight lane;
  - a Cyclone on the flight (up to the arrow's lane end) has `WouldScatter(thatPrefab)`.

  When on, it:
  - hides her range tiles past the Cyclone that no copy flies over;
  - lights the copy-lane tiles that aren't already range tiles;
  - puts chevrons along every copy lane;
  - works out each copy's hits: physics samples from the Cyclone's scatter point to the copy's end cell, using the arrow prefab's own collider radius and layer mask with triggers, the same contacts its sweep and trigger find. Only units the arrow's effect targets are hit and count toward the falloff, and the owner is skipped, all as in `ProjectileHitLedger`. The falloff is factor^hit as `Projectile.TryHitOnContact` applies it, or full damage for an arrow without falloff;
  - merges the copies' damage with the normal preview (above).

  No statics, so no play-mode reset is needed.
- `Features/Player/Shared/Synergies/TempestBloomPreviewRules.cs` (new, + `.meta`): pure rules: `CollectHits` (hit order and falloff index), `Falloff`, `Merge` (normal before the Cyclone + copies, mute the unreached) and `SplitLaneTiles` (which tiles to hide and which to light).
- `Features/Player/Shared/Synergies/Editor/TempestBloomPreviewTests.cs` (new, + `.meta`): 16 EditMode tests.

No scene, prefab or asset edits. The presenter object from C1 already sits in the container scene, and the Bloom part has no new inspector fields.

## Acceptance criteria

- [x] **The preview appears only when the real shot would Bloom.** The gate is `WouldScatter`, the same method the trigger now uses (whitelist + unlock). On top of that: the Cyclone is alive and on its cell, it lies on the arrow's flight (the arrow flies its whole reach and stops at the first Cyclone), and the aim is legal. *Play check:* aim through a Cyclone with the Bloom locked (no preview) and unlocked (preview). Aim at a lane without a Cyclone (no preview).
- [x] **Copy lanes match where the real copies go.** One source: the trigger and the preview both use `TempestBloomGeometry`. The preview feeds it the incoming direction the real arrow will have: from Linda's `SpawnSource` to the anchor of her lane's end cell, with the same sign rule as `Projectile.Direction`. *Tests:* the helper equals the split as originally written, for all 9 incoming directions on 5 boards. Also: straight right gives forward, up and down; full reach from the Cyclone; holes crossed; grid edge; missing neighbour; lane order. *Play check:* aim, fire, compare. **See Needs THJ: this most likely shows 4 lanes, not 3.**
- [x] **Linda's lanes past the Cyclone hide while it's on and come back when it's off.** In practice the forward copy flies over the same tiles further out, so those tiles stay lit (as copy lane). Only tiles no copy covers go dark, for example past a hole right after the Cyclone. They come back only while the controller still lights them (same ability, still in its range); otherwise the controller redraws them itself. *Test:* `SplitLaneTiles`. *Play check.*
- [x] **Chevrons run along the copy lanes:** one on every copy-lane cell, pointing along the copy. *Play check* for the look; see loose ends.
- [x] **HP previews on the enemies the copies hit; none on allies the real shot wouldn't hurt.** Hits are filtered by the arrow effect's target relation, as the projectile does, and the owner is never hit. *Tests:* `CollectHits` (owner skipped, an ally neither hit nor weakening the arrow, one hit per unit), `Falloff`, `Merge`. *Play check:* enemies on copy lanes show bars and skull. An ally on a copy lane shows nothing. An enemy past the Cyclone shows the copy's damage, not the old bow value.
- [x] **Everything clears on cancel, ability switch, end turn and level end.** `RefreshBloom` runs every `LateUpdate` and on hover. When the aim stops being a Bloom (the aimed ability turns null outside the player's target selection, or the level has ended), it unlights its tiles, clears its chevrons and hides its bars. `OnDisable` and `OnDestroy` do the same. *Play check* for each case.
- [x] **Console clean:** no new errors or warnings after the recompile (the existing CS0108/CS8509/CS0168 warnings are unchanged).
- [x] **EditMode:** 1850 run, 1849 passed. The only failure is the known `AIRegressionTest.Baseline_MatchesCurrentAI`. The Bergsons test group ran alone first: 390/390 after one fix (below).
- [x] **No core file edited.**

## Save reset

No.

## Decisions I made

- Tier 1: put the helper in Lucy's scripts beside the scatter, which owns the rule, rather than in `Synergies/`. Same namespace as before.
- Tier 1: the preview walks the main arrow on the grid, not by physics: straight lane, farthest existing cell within reach, first Cyclone on it. The arrow flies through everything to its lane end, so the first Cyclone on the lane is the one its trigger meets.
- Tier 2 (flag): the copy damage formula repeats `AbilityDamagePreview.AddDamage` in the presenter, built only from public methods: `SimulateApply`, the guaranteed decrement mods, the per-hit falloff, `NormalizeValueChange`. `AddDamage` is private and core. Making it public would be the Tier 3 way to drop the copy. If `AddDamage` changes, this copy must change with it; the comment on `HitDamage` says so.
- Tier 2 (flag): copy hits count the falloff the way the **real arrow** does (only targeted units count). The core bow preview (`CollectPreviewPathHits`) also counts allies and other entities it passes, so it under-shows damage behind an ally. That is a core preview bug, not touched.
- Tier 1: three projectile settings the preview relies on are private on core `Projectile`: travels its whole reach, hits along its flight, aims at the cell. Rather than adding getters (core), a data test reads them from every arrow on the Cyclone's whitelist with `SerializedObject` and fails if one changes. The first run showed the sisters' Duo arrow (`LindaAttackFireArrow`) has no per-hit falloff. The presenter now treats such an arrow as full damage on every hit, as the runtime does, and the test no longer requires falloff.
- Tier 1: chevrons on every copy-lane cell, including the last. Copy lanes use highlight level 0, which equals her own level within reach.
- Tier 1: did not move `QuiverLevelAccess` / `GroundedArrowField.CellSpacing`. This chunk doesn't touch them; it only calls `QuiverLevelAccess` as C1 does.

## Needs THJ

**The real Tempest Bloom very likely splits into 4 copies, one flying back toward Linda.** I found this by reading the code; it isn't play-confirmed.

1. **What:** the split skips the neighbour whose offset equals minus `projectile.Direction`. That direction is the sign of each axis of the arrow's world flight vector, and an axis counts as zero only when it is exactly 0. Linda's arrow starts at her `SpawnSource`, local offset (0.009, 0.245) above her cell's anchor, and flies to the lane end's anchor. So a horizontal shot reads (±1, −1) and a vertical shot (±1 or −1, ±1). No orthogonal neighbour equals minus a diagonal, so nothing is skipped: a fourth copy flies back over Linda's own lane, through her (she isn't hit) and past her. It hits enemies between her and the Cyclone a second time, and enemies behind her.
2. **Why it matters:** the GDD (family-systems Tempest Bloom row) says "except back the way it came", and THJ's mental model is 3 copies. The preview shows what the game really does, so the play check will show a 4th lane through Linda, and extra damage on enemies between her and the Cyclone (normal hit + back copy).
3. **Options:**
   - (a) Keep it as it is (a 4-way burst).
   - (b) Fix the split to use the grid step instead. For example, the trigger passes the step from the arrow's start cell toward the Cyclone, or `TempestBloomGeometry.IncomingDirection` drops the minor axis. That is a one-line change in the feature file `LucyCycloneProjectileScatter`, plus the matching line in the presenter's `IncomingDirection`. The shared helper keeps the preview in step either way. A test (`ArrowWhoseFlightIsNotPerfectlyLevel_SkipsNoNeighbour`) documents today's behaviour and would flip.
4. **Recommendation:** (b), since it matches the GDD and the 3-copy intent. It is a gameplay change, so it needs THJ's yes.
5. **Check first:** in Memory 4, aim through the Cyclone and fire. Does a copy fly back toward Linda? The preview's 4th lane shows the same thing before firing.

## Docs to update

- `tech/combat-architecture.md` (coordinator): the Bloom geometry lives in `TempestBloomGeometry` (shared by `LucyCycloneProjectileScatter` and the preview), and the Bloom preview is `SynergyLanePresenter.Bloom.cs`. It calls `SetHighlight`, `SetAimDirectionPreview` and `GUnit.ShowDamagePreview` on its own cells and units only.
- GDD `combat-rules.md` (preview rule beside CR-37) and `family-systems.md` (designer, per the plan's gates). If THJ picks (a), the Tempest Bloom row should say 4 copies.

## Risks and loose ends

- **Back copy (Needs THJ above).**
- **Duplicate damage math:** see Decisions. Any change to `AbilityDamagePreview.AddDamage` must be mirrored in `HitDamage`.
- **The core bow preview's falloff counts allies and other entities** (`Projectile.CollectPreviewPathHits` increments its index for every entity), unlike the real hit. It affects units before the Cyclone in this preview and every bow preview. Core bugfix (Tier 2) if wanted.
- **Listener order assumption:** the hover listener runs before `PlayerController`'s because the controller subscribes on each entry into target selection. If that ever changes, a hover that turns the Bloom off could hide a fresh controller bar on a unit both touched; the next hover fixes it. The comment in `SynergyLanePresenter.OnCellHovered` says so.
- **Non-hover redraws by the controller** (shape-rotation input on `ShowAffectedArea` abilities, which includes Linda's bow) overwrite the presenter's bars only until the next frame, when they are re-applied.
- **Not covered:** Mark catching the arrow before the Cyclone (C3 territory; the preview assumes it reaches the Cyclone), and the Linda–Lucy Duo arrow (aimed through `UnitsCooperationHandler`, not the bow's target selection, so no Bloom preview there). Copies never split again at a second Cyclone (they have no `PrefabSource`), and the preview matches that.
- **Chevron look along a lane:** I couldn't see it in Play. If one per cell looks busy, the lane cells are easy to thin out.
- **Copy collider radius:** the preview uses the arrow prefab's `CircleCollider2D` (the runtime sweep's radius), not the preview-only `boundingSize` the bow preview uses. So copy reach can differ slightly from the bow preview's for a unit at the edge of a lane.

## Proposed commits

1. `feat(combat): aiming Linda's bow through a Cyclone that would split it shows the copies' lanes and chevrons, and the damage each copy deals` (plain; the extraction, the preview and the tests only work together)
   - `miso/Assets/_Project/Features/Player/Lucy/Scripts/LucyCycloneProjectileScatter.cs`
   - `miso/Assets/_Project/Features/Player/Lucy/Scripts/TempestBloomGeometry.cs` + `.meta`
   - `miso/Assets/_Project/Features/Player/Shared/Synergies/SynergyLanePresenter.cs`
   - `miso/Assets/_Project/Features/Player/Shared/Synergies/SynergyLanePresenter.Bloom.cs` + `.meta`
   - `miso/Assets/_Project/Features/Player/Shared/Synergies/TempestBloomPreviewRules.cs` + `.meta`
   - `miso/Assets/_Project/Features/Player/Shared/Synergies/Editor/TempestBloomPreviewTests.cs` + `.meta`

Leave out THJ's uncommitted files: `AIFactionBrain.cs`, `AIUnitBrain.cs`, `PreloadScreen.unity`, `ProjectSettings/*` and the TMP fallback font.

## Other branches

`main`, when this branch merges.

## How to see it

1. Open Memory 4 (the Hearth's Mark segment, `GB_m4-mark`). Its `LevelStartRunUpgradeGrant` unlocks Tempest Bloom at level start, and Lucy and Linda are both there. Any sandbox with Lucy and Linda also works if the `LindaLucyCycloneSpreadUnlock` run upgrade or the Family node is owned. Press Play.
2. With Lucy, cast her Cyclone on a cell in one of Linda's straight lanes, two or three tiles away, ideally with enemies beside and beyond it.
3. Select Linda and her bow. Hover a cell in the lane that runs through the Cyclone:
   - her lane tiles up to the Cyclone stay as they are;
   - from the Cyclone, the copy lanes light up in the same tile look, with blue chevrons along each;
   - the enemies on the copy lanes show the normal damage bars (skull when lethal), and an enemy past the Cyclone shows the copy's damage;
   - an ally standing on a copy lane shows no bar.
4. **Count the lanes.** Expect 3 (forward, left, right) by design. If a 4th runs back over Linda, that is the real behaviour (Needs THJ). Fire and check the copies follow the lanes.
5. Hover a different lane (no Cyclone): everything Bloom goes away and her normal lanes and bars are back.
6. Clearing: with the Bloom preview up, (a) right-click or cancel, (b) pick another ability, (c) end the turn, (d) finish the level with the aim up if you can. No leftover tiles, chevrons or bars each time.
7. Lock check: in a level without the Bloom unlocked (for example Memory 3 if it has a Cyclone, or a sandbox without the upgrade), the same aim shows no Bloom preview; the bow preview is unchanged.
8. Console: no new errors or warnings.

## Round 2: Bloom makes 3 copies; review should-fixes

THJ chose to fix the Bloom (D-number with the coordinator): 3 copies, never one back the way the arrow came. Review `reports/synergy-preview-c2-review.md` was APPROVE.

### 1. The back-skip fix (a gameplay change, THJ's yes)

- **New rule:** "back" is read on the grid, from the cell the arrow was shot from to the Cyclone's cell, as one step along the main axis. It is no longer the sign of the arrow's flight on screen, which always leans because the arrow leaves from the bow, 0.245 above Linda's cell.
- **Shared helper:** `TempestBloomGeometry.IncomingDirection(Vector2Int shotFrom, Vector2Int cyclone)` replaces the float version.
- **Real shot:** `LucyCycloneProjectileScatter` calls the helper with the shooter's cell (`projectile.Owner` as a grid entity, `CurrentCell`) and the Cyclone's cell. With no shooter on a cell, or the shooter on the Cyclone's own cell, it falls back to `projectile.Direction` as before. Linda doesn't move while her arrow flies, so her cell is where the shot came from.
- **Preview:** calls the same helper with Linda's cell and the Cyclone's cell. The old spawn-point/flight-vector reading is removed.
- **Straight lanes** (the bow is straight-lane only): 3 copies, forward, left and right.
- **Diagonal shots:** none of Linda's straight-lane shots can be diagonal. An arrow that reached a Cyclone off the line would skip the neighbour opposite the axis it travelled furthest on. An exact diagonal has no main axis, so it skips no neighbour and makes 4 copies, because no orthogonal neighbour lies exactly behind a diagonal. I know of no shot that does this today (the role arrow and the Duo arrow go to a target, and I didn't check whether either can cross a Cyclone diagonally).

Tests:
- `ArrowWhoseFlightIsNotPerfectlyLevel_SkipsNoNeighbour` became `ArrowShotFromTheBow_NeverSendsACopyBack_EvenThoughItsFlightLeans`. Linda is level with the Cyclone, the copies are right, up and down, and left (toward her) is checked absent.
- `IncomingDirection_IsTheStepAlongTheMainAxis_FromShooterToCyclone` covers lanes in three directions, off the line (main axis), an exact diagonal and the same cell. It replaces the old float sign test.
- `ExactDiagonalShot_SplitsTowardEveryNeighbour` documents the diagonal case.
- The equivalence test is kept and still pins the split loop: the literal adjacency walk from the trigger (grid order, existing neighbours, skip the key equal to minus the incoming direction) against the shared helper. It runs for all 9 incoming values on 5 boards. What changed is only where the incoming direction comes from, and the 9 values cover everything the new rule can return. Its comment says so.

### 2. S1: no dependence on listener order

- When the cursor leaves a cell (`hovered == false`, which `GridManager` sends to every listener before the new cell's `true`), the presenter now calls `ClearBloom()`. That gives back its bars, restores her tiles (same ability, still in range), unlights its copy tiles and clears its chevrons.
- The hover-in pass no longer refreshes. The next `LateUpdate` (same frame) redraws the preview for the new cell if it still blooms.
- The comment about listener order is gone.
- Side effect: moving the cursor along a Bloom lane gives back and redraws the tiles and chevrons within the same frame (nothing renders in between). If the lane glow has an animation, it may restart on each cell change. Worth a look in the play check.

### 3. S2: per-frame allocations

- `CellExists` is a cached static delegate. The shooter-cell check is one instance delegate created once (it reads a `_laneShooter` field).
- `SplitLaneTiles` takes a reusable `HashSet` instead of building one each call.
- The lanes are rebuilt only when the shot key changes: ability, shooter cell, lane step, Cyclone cell, and the controller's range list and count. Otherwise nothing is diffed or applied.
- When the Bloom is off and the preview holds nothing, `RefreshBloom` returns right after reading the shot.
- The damage pass still allocates a little (lambdas, the hit set) but runs only when the shot changes, not every frame.

### 4. S3: `WouldScatter` null guards

It returns false with no whitelist, no `selfEntity` or no `Owner`. Before, it would have thrown. That changes nothing for the real split.

### 5. S4: no code change

See the play-check step below.

### Verified

- Compile clean. The console has no errors or warnings from these files. The one error after the recompile is the known `Objects are trying to be loaded during a domain backup` (noted in C1, likely THJ's TMP fallback font).
- EditMode: 1851 run, 1850 passed. The only failure is the known `AIRegressionTest.Baseline_MatchesCurrentAI`.
- The editor was not in Play mode. I checked right after writing the edits, before the recompile, so I stopped nothing.

### Files

The same 6 scripts and 4 `.meta` files as round 1; no new files. The commit stays as proposed above. Its message can say the Bloom now splits into three copies, for example: `feat(combat): Tempest Bloom splits into three copies, never back toward the shooter; aiming Linda's bow through a Cyclone shows the copies' lanes, chevrons and damage`. Optionally split it: (1) the scatter fix + `TempestBloomGeometry` + its tests, (2) the preview.

### Play check additions

- Fire through a Cyclone in Memory 4. Three copies go forward, left and right, and none flies back toward Linda. The preview shows the same three lanes.
- Move the cursor along the lane through the Cyclone and back out to another lane. The tiles, chevrons and bars follow with no leftovers, and nothing flickers or restarts noticeably.
- **Multi-cell target (S4):** if a level has a big unit (a boss) standing past a Cyclone, or one whose footprint reaches across Linda's lane, aim through the Cyclone at it. Check that its bar shows the copy's damage, and that tiles of Linda's lane *before* the Cyclone don't go dark under its footprint. Hiding is keyed by the grid's overlay cell, the unit's anchor, so a footprint that straddles the Cyclone line could hide a tile it shouldn't. I know of no such level among the Hearth memories.

## Round 3: only the Cyclone path keeps its glow; one chevron per lane

THJ's play check: her other lanes still glowed, and a >>> showed on every copy-lane tile.

What changed:
- **Tiles that lose their glow while the Bloom is on:** every one of her range tiles except the aimed lane from her up to and including the Cyclone. So her other three lanes go fully dark, and so does the aimed lane past the Cyclone. Pure rule: `TempestBloomPreviewRules.KeepsGlow(stepsAlongAimedLane, cycloneSteps)`, true for steps 1..cycloneSteps; -1 (another lane) and 0 (her own tile) give false. Her own tile is never touched.
- **Copy lanes:** they still light from the Cyclone in the same look. A dimmed tile that a copy flies over stays lit as that copy's lane: the aimed lane past the Cyclone is the forward copy's lane. That is `SplitLaneTiles`, whose first argument is now "her tiles that lose their glow".
- **Chevrons:** exactly one per copy lane, on its first tile past the Cyclone, pointing along the copy (`TempestBloomPreviewRules.TryGetChevronTile`). Linda's own >>> on the tile in front of her is the controller's and is never touched.
- **Give-back:** unchanged mechanism, now over more tiles.
  - On the `hovered == false` pass (and on cancel, ability switch, end turn, level end via `LateUpdate`), each dimmed tile is relit with the controller's own call and level, while the controller still owns it (same ability, still in its range).
  - The copy tiles it lit go dark, and its chevrons clear.
  - Moving to another lane: the leave pass gives everything back first. Then `LateUpdate` either draws nothing (no Cyclone on the new lane, so all four lanes and her normal >>> are as the controller drew them) or rebuilds for the new lane's Cyclone. Within one lane, nothing is rebuilt until the cursor leaves a cell.
- **Tests (4 new or changed, 19 Bloom tests in all):**
  - `KeepsGlow_OnlyTheAimedLaneFromLindaUpToTheCyclone`;
  - `ChevronTile_IsTheLanesFirstTile_AndNoneForAnEmptyLane`;
  - `BloomOn_DimsHerOtherLanesAndPastTheCyclone_LightsTheCopyLanes_OneChevronEach`: Linda at (0,0) with reach 4 and the Cyclone at (2,0). Her other three lanes are hidden; (1,0) and (2,0) are kept; (3,0) and (4,0) stay lit as the forward copy's lane; the up and down copy lanes and (5,0)-(6,0) light up; chevrons sit only on (3,0), (2,1) and (2,-1);
  - the old lane-tile test reworded as `LaneTiles_DimmedTilesFlownByACopyStayLit_AndHerOwnCellIsNeverLit`.
- **Verified:** compile clean, and no errors or warnings from these files. The only console error is the known `Objects are trying to be loaded during a domain backup`. EditMode: 1854 run, 1853 passed; the only failure is the known `AIRegressionTest.Baseline_MatchesCurrentAI`. The editor wasn't in Play, so I stopped nothing.
- **Files:** same list as before, nothing new.

Play check:
1. Aim through the Cyclone. Only Linda → Cyclone keeps her glow; her other three lanes are dark; the three copy lanes glow. Her >>> sits in front of her, and one >>> sits on each copy lane's first tile.
2. Move to a lane without a Cyclone. All four lanes and her >>> are back exactly as normal.
3. Move back, then cancel, switch ability and end turn. Nothing is left dark or lit.
4. Plus the multi-cell check from round 2.
