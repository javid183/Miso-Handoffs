# Cyclone reset: straight run-through Steer, knock, carry and wobble removed (tech)

Size: L    Tier: 3 (design approved: D-580 to D-585)    Assigned to: miso-implementer (one chunk at a time)
Branch: thj/cyclone
Status: built 2026-11-19 (C1 `d9cb1f2ce`, C2 `15a107cbd`, C3 `774dabef7`, C4 `d8db54ddf`, C5 `359882aed`, review fixes `e426c36c8`, `b62e2a7fd`); waiting on THJ's play check

## Why

THJ's 2026-11-19 play check: the Cyclone became too complex to predict (`playtests/2026-11-18-cyclone-round3-play-check.md`, last section; screenshots `playtests/img/2026-11-19-cyclone-*`). Design reset `plans/2026-11-19-cyclone-reset-design.md` (core K1 to K5 plus the run-through Steer), all six answers taken: D-580 to D-585.

## Goal

The Cyclone behaves exactly as THJ's three sentences, with one shared planner for range, preview and execution:

1. Lucy summons it on an empty cell; it stays 3 rounds and never moves on its own.
2. On cast, after each enemy turn and after each Steer, it Whirls: enemies in its four lines are pulled one cell in, then every enemy beside it is hit.
3. Once a turn Lucy Steers it up to 3 cells in a straight line, through enemies (one hit each); an enemy on the cell where it stops is knocked one cell onward; then it Whirls.

## The rules the code must implement (from D-580 to D-585)

**Steer line.** From the Cyclone's cell, in each of the 4 straight directions, cells 1 to `reach` (3). The line ends before: no cell (wall, map edge) or a planted entity that blocks walking (the Cyclone's own slot is exempt). Non-blocking planted entities (hazards) are crossed.

**Passing.** Every unit on the line cells before the stopping cell is passed. Enemies of Lucy's faction (heavies included; a large unit counts once) each take one Cyclone hit as the Cyclone enters their cell, in order. Family, allies and units without a faction: nothing. A passed unit does not move, raises no move events, starts no Watch or hazard.

**Where it can stop** (each line cell that qualifies is a destination; cells past a refused one stay offered):
- an empty cell: `CycloneRules.IsValidCastCell` (no unit, nothing planted, nothing stashed); or
- a cell holding one knockable enemy: hostile, 1x1 (`EffectivePlacementSize == one`), passes the pull filter (not `Unmovable`, same as `IsPullable`), nothing planted on the cell, and the knock rule finds a landing.
- Never on family, an ally, a heavy, or a planted cell.

**Knock rule (shared by Steer and cast; D-581, D-585).** Given the knocked cell and an *onward* direction: try `cell + onward`, then `cell + right(onward)`, then `cell + left(onward)`; the first free cell wins; none free → no knock (the cell isn't offered). *Free* = the cell exists, no unit, nothing stashed, no walk-blocking planted entity, and not the Cyclone's destination. A non-blocking hazard is free (it fires on landing). `right` and `left` are the Cyclone's right and left as it travels, seen on screen: moving screen-right, its right is screen-down. The implementer checks the grid's y axis (whether +y is screen-up) and writes one test per direction that pins it.
- Steer: onward = the Steer's direction.
- Cast on an enemy: onward = away from Lucy along the larger axis; at a diagonal tie, along the row (as today). Then right/left of that onward. This replaces today's "row, then column" diagonal fallback and adds a fallback to non-diagonal casts.

**Order at the end of a Steer.** Glide → pass hits fire as the Cyclone enters each enemy's cell → at the stopping cell, the knocked enemy is flung to its landing (start-of-move event, unplug, plug: a hazard there fires; end-of-move: Watch answers; it wakes) → the Cyclone takes the cell → reactions settle (as today after a carry landing, D-555) → the Whirl.

**One hit per enemy per Steer (D-583).** The closing Whirl skips every unit already hit by this Steer's pass. The knocked enemy wasn't passed, so the Whirl hits it if it is beside (it always lands beside, unless it died). Cast Whirls and enemy-turn Whirls are unchanged.

**Fixed at the click.** The plan is computed once from the board at the click. A passed enemy dying changes nothing. Safety net at landing only: if the stopping cell or the knock landing is no longer valid (for example a death spawned a unit there), re-run the knock rule live; if that fails too, the Cyclone goes back to its start cell (today's `StayPut` path), no knock, and still Whirls there. Covered by a test.

**Credit.** Pass hits go through the same hit and report path as Whirl hits (`ICycloneWhirlSteps.Hit` + `Report`, `CycloneHitContext`): cast credit, Howling Gale Weak, kill XP and gold, the sisters' tally, Masher counter ignores them, Lucy's follow-up doesn't answer them, an Unaware enemy wakes (whatever a Whirl hit does today).

**No Crippled damage** from the knock (no per-cell effect on the move, as today).

## Acceptance criteria

- [ ] The Steer range highlight shows only cells on the 4 straight lines, up to 3 out, that qualify above. A Claw on the line stays unlit when it can't be knocked; the cell beyond still lights if it qualifies.
- [ ] Screenshot 1 (row of Claws ahead): steering onto the first Claw's cell knocks it to the row on the Cyclone's right (or left if that's blocked); steering onto the empty cell before the row is also offered.
- [ ] Screenshot 2 (Claw above, family around): the Steer is offered; up through the Claws hits each passed Claw once.
- [ ] Hovering a destination shows: the straight path, the landing Cyclone and its cross, the knocked enemy's ghost and tether (at most one), the Whirl's pull ghosts, the hazard ring, and exactly one damage segment per enemy that will be hit (passed or Whirl-hit), skull when lethal. What is shown is what happens (planner shared; a test compares them).
- [ ] Executing: pass hits pop in order down the line; the knocked enemy lands where the ghost showed; Watch answers the knock; the Whirl then pulls and hits, skipping passed enemies.
- [ ] Cast on an enemy: knocked away from Lucy; when blocked, to the right, else left of that direction; refused when none is free. Empty-cell casts unchanged.
- [ ] No carry anywhere: no side or rear enemy moves with a Steer; no turning path; no grab or drag beats; no wobble or pips flicker.
- [ ] Combat log: the Whirl line reads "pulled N, hit M"; a Steer adds one line "✦ Steer · Lucy: hit N on the way, knocked K" (working text).
- [ ] Ability descriptions (Steer, Cyclone) match the new rules (working text from the design, narrative pass later).
- [ ] All EditMode tests pass (the Explicit AI regression test excluded; it's not run: no AI content changes).

## Scope

In: Steer planner, execution, preview and range; the knock rule shared with the cast on an enemy; removal of the carry, turning search, rider beats, wobble and pips flicker; log lines; ability description texts; tests.
Out: Whirl rules and timings, cast rules on empty cells, life/pips, enemy-side rules (CR-57, CR-58, heavies burst, EN-18, EN-19), AI, any core system, Tempest Bloom, numbers (hit stays 3 × Cyclone Power 4 / 5), the dead Linda Cyclone copies.

## Touches

Systems: Lucy's Cyclone feature code only (`Features/Player/Lucy/Scripts/Cyclone/`, its `Editor/` tests and setup tool, two ability assets). **No core system** (the Explore map confirmed every rider and wobble line is feature code and no core hook becomes unused; `ITargetSelectionRangeProvider`, `AEffectPusher`, `PlayerInputController` lock, `ReportDamageOutsideAbility`, `EnemyAlertTracker.WakeMovedUnit` stay in use).
USPs: Family Roles (Watch answers the knock; passing starts none), Synergies (Whirl bunch unchanged).
Docs: GDD `characters/lucy.md` LU-3 to LU-7 and value table, `enemies.md` EN-3 and EN-18, `design/cyclone-redesign.md` reset note (designer); glossary and texts (narrative); `tech/core-systems.md` note line 112 (coordinator: `CycloneWobble`, `CycloneCarryPlanner` gone).

## Approach

Code facts (Explore, 2026-11-19): `CycloneSteerRules.Search` is the breadth-first turning search; `CycloneCarryPlanner` holds the carry and all plan types (`CycloneCarryPlan`, `Step`, `Move`, `Role`, `Rules`) and its `Shove` serves the cast; `CycloneEntity.Steer.cs` `SteerRoutine` + nested `CarryLanding` run it; `CycloneOutcomePlanner.ForSteer/ForCast` feed the preview; `CycloneWobble` is wired in `CycloneEntity.cs` 37, 51-52, 103. Files are LF, no BOM; namespace `MISO.Core.Features.Bergsons` (tests `.EditorTests`). No carry or wobble field is serialized in `Cyclone.prefab`, so removing them changes no YAML.

### C1. Pure rules: knock and straight Steer plan (new files, nothing wired) — sonnet, review with the feature

- New `CycloneKnockRules.cs`: `Right(dir)`, `Left(dir)`, `Landing(cell, onward, isFree)` → cell or null (onward, right, left).
- New `CycloneSteerPlan.cs` (data): `Start`, `End`, `Direction`, `Path` (start excluded, straight cells up to End), `Passed` (ordered `(GUnit unit, GridCell cell)`, enemies only, each unit once), `Knock` (nullable `CycloneKnock { GUnit Unit; GridCell From; GridCell To; }`, shared type, also used by the cast).
- New `CycloneSteerPlanner.cs` (pure, board-reading through delegates like the Whirl planner so tests use `CycloneTestGrid`): `Lines(from, reach, rules)` → every destination with its plan; `PlanTo(from, to, reach, rules)` → plan or null. Rules object carries: `Self`, `IsEnemy`, `IsKnockable`, `CellAt`. Implements "The rules" above (line end, passing, stopping, knock, free).
- Cast knock: new pure `CycloneRules.CastKnock(lucyCell, cell, rules)` → `CycloneKnock?` using `CastShoveDirections`' first direction as onward, then `CycloneKnockRules`. Not wired yet.
- Tests (new `CycloneSteerPlannerTests.cs`, `CycloneKnockRulesTests.cs`): right/left per direction against the grid's y axis; lines stop at walls, edge, blocking planted, pass hazards; family and allies passed silently; heavy passed and hit once, never a stop; enemy cell offered only with a landing; onward/right/left order; a refused cell doesn't hide cells beyond; screenshot 1 and 2 layouts as fixtures; no destination at distance 0.
- Covering fixtures: the two new test classes.
- Commit: own commit ("pure rules for the straight Steer and the knock, with tests").

### C2. Runtime: Steer and cast use the new plan; carry removed — opus, review with the feature

- `AEffectCycloneSteer`: range (`TryCollectTargetSelectionCells`), target check and execution use `CycloneSteerPlanner`; `TrySteer` takes the destination cell (or the plan) and re-plans at the click; `IsValidSteerPath` and `PathFor` go. AI gate unchanged.
- `CycloneEntity.Steer.cs`: rewrite `SteerRoutine`: glide straight over `Path` at `steerSecondsPerCell`; on entering each `Passed` cell, if that unit is alive, `WhirlSteps.Hit` + `Report` (pop per hit); at `End`, if `Knock`, run the knock with the cast shove's motion and steps (start-of-move, fling with `flingSeconds` / `hopCells`, unplug, plug, landed); then `Relocate` the Cyclone; then the Whirl with the passed set excluded. Safety net per "Fixed at the click". Delete `CarryLanding`, grab and drag beats.
- Reactions before the Whirl: keep today's mechanism (Whirl step-0 wait and `SteerActionOpen` keeping the action open until the pull), renamed from `carried`/`CarryLanded` to the knock (`knocked`/`KnockLanded`).
- Whirl exclusion: `WhirlRoutine` gets an optional `IReadOnlyCollection<GUnit> skipHits`; both `HitTargets` calls filter it (the second call at the breath recompute too).
- Cast on an enemy: `AEffectCycloneSpawner` / `.Shove.cs` / `CycloneRules.CastOnEnemy.cs` switch to `CastKnock`; `ShoveThenCast` takes a `CycloneKnock`. Remove `PlanCastShove`'s carry-plan use.
- Remove: `CycloneCarryPlanner.cs` (+ meta) and every type in it; `CycloneSteerRules.Search`/`Explore`/`PathTo`/`CanSteerTo` (keep `DefaultReach`, `IsFriendly`, `CanEndOn` if still used, `SteerActionOpen`); `CycloneWindMotion.Trail`/`Kick`; fields `grabSeconds`, `grabDepthCells`, `dragLag`, `dragTiltDegrees`, `kickPortion`; rider-only members of `ICycloneSteerSteps` / `CycloneSteerSteps` (keep `PositionOn`, `DeltaTime`, `Relocate`; the knock uses `ICycloneShoveSteps` through a `ShoveSteps` seam on the entity, swappable in tests).
- Log: `CycloneRules.WhirlLogDetail(pulled, hit)` ("pulled N, hit M"); `ICycloneWhirlSteps.Log` drops `carried`; new Steer log via `GlobalEventBus.RaiseSynergy(caster, "Steer", "hit N on the way, knocked K", targets)` through a new member on the Steer's steps (keep the bus call inside the steps class).
- Tests: delete `CycloneSteerTests.Carry.cs` except the four concepts worth keeping, rewritten for the knock (one landing fires only the landing hazard; no Crippled field on the steps; the action closes after the pull; a Steer with no knock pulls without waiting). Rewrite the BRK tests listed in the Explore map: `CycloneSteerTests` (straight reach, enemies passed, no detour, log, `SteerActionOpen`), `CycloneSteerTests.Preview` ghost test (C3 owns it if it's preview-only), `CycloneWindBeatsTests` (delete rider tests, keep Whirl and cast beats), `CycloneCastOnEnemyTests` direction tests (new fallback; line 309 now asserts a knockable enemy cell can be a Steer stop), `CycloneBurstTests` 472 (a burst during a Steer: the knocked enemy still lands, then the Cyclone goes), every recorder that implements a changed interface. New runtime tests: pass hits in path order, each enemy once; passed enemy not re-hit by the Whirl; knocked enemy hit by the Whirl; a passed enemy that dies mid-glide changes nothing; the safety net; family passed with no event; Watch answers the knock only.
- Covering fixtures: all `MISO.Core.Features.Bergsons.EditorTests` Cyclone classes (`Cyclone*`), plus `MasherCounterCycloneTests`, `MasherCounterWhirlTests`, `EnemyAlertForcedMoveTests`.
- Commit: own commit ("the Steer glides in a straight line through enemies and knocks the one where it stops; the carry is gone").

### C3. Preview — sonnet, review with the feature

- `CycloneOutcome`: add `PassHit` (ordered units); `Hit` stays the Whirl's; add a helper for "every unit hit once" (union, passed first). `CycloneOutcomePlanner.ForSteer(plan, …)` from `CycloneSteerPlan`: Moves = the knock only (one-cell path), Whirl computed on the board after the knock with the Cyclone at `End`, `Start` vacated, passed units removed from the Whirl's `Hit`. `ForCast` takes `CycloneKnock?`.
- `CycloneSteerPreview`: straight path arrows from `plan.Path`; one damage segment per hit unit (passed units' bars where they stand; knocked unit on its ghost).
- `CycloneOutcomeView`: unchanged except the damage map fed from the union.
- Tests: rewrite `SteerPreview_GhostsStand…` for the knock; delete `SteerPreview_ACellPastABlockedFront…`; new: preview equals execution for screenshot 1 and 2 layouts (pass set, knock landing, Whirl hits); one segment per enemy; no ghost for passed units.
- Covering fixtures: `CycloneSteerTests` (Preview partial), `CyclonePreviewTests`, `CycloneCastOnEnemyTests`.
- Commit: own commit.

### C4. Remove the heavy-warning wobble (D-584) — sonnet, review with the feature

- Delete `CycloneWobble.cs` (+ meta) and `CycloneWobbleRules`; unwire in `CycloneEntity.cs`; remove `CyclonePipsView` flicker (`SetFlicker`, `IsFlickering`, the `Update` flicker and the `leftAlpha` path if only the flicker uses it).
- Delete the five `Wobble_*` tests in `CyclonePreviewTests.cs`.
- Covering fixtures: `CyclonePreviewTests`, `CycloneLifeTests`.
- Independent of C1 to C3; own commit (revertable alone).

### C5. Texts and setup tool — sonnet, review with the feature

- `Lucy_Ability_Steer.asset` description and `CycloneSteerSetup.cs` line 31: working text "Glide the Cyclone up to 3 cells in a line, through enemies, hitting each. An enemy where it stops is knocked onward. Then it Whirls. Once a turn."
- `Lucy_Cyclone_Ability.asset`: add the knock to the cast text (working: "… Cast it on an enemy to knock it away.").
- Small YAML edits on the two assets only.
- Then the whole feature: one review (no core chunk, D-575), the full EditMode suite once (D-577), then the commit proposal per chunk.

## Risks

- **Statics:** none added (no `PlayModeStaticReset` change). `CycloneRegistry` unchanged.
- **AI thread:** the Steer's AI gate and range provider are unchanged; the planner is never called by the AI. No AI content touched, so the Explicit `AIRegressionTest` isn't run.
- **Serialized renames:** none on prefab fields; removed fields aren't in YAML. The stale `whirlHitTimes` key stays (out of scope).
- **Save data:** none.
- **Coroutines and locks:** the rewritten `SteerRoutine` keeps the `finally` cleanup (restore drawings, re-plug a knocked unit left off a cell, release the hold and input lock, deferred dispose). Test: dispose and stop mid-glide and mid-knock.
- **Preview trust:** one planner for range, preview and execution; C3 adds the comparison test.
- **Knock direction reads arbitrary** (design risk): the fallback order is isolated in `CycloneKnockRules`; switching to "onward or refuse" (D-581 lever) is a one-line change plus tests.
- **Pass damage creep:** the hit value is unchanged and shared; the graze lever (D-583) would be a separate hit compound later, not in this plan.
- **Other branches:** `main` doesn't have the Cyclone; nothing to port. When `thj/cyclone` merges into `main`, the Masher plow note in `branches.md` still applies.
- **Line endings:** all Cyclone files LF, no BOM; keep them.
- **Presentation (THJ's area, first pass of a new beat):** the pass hits popping in sequence down the line is a new beat; its timing follows the glide (one hit as the Cyclone enters each cell). THJ judges it at the play check; tuning values are serialized fields (Tier 2 after that, D-578).

## Gates

- Compile after each chunk; covering fixtures per chunk (named above); full EditMode suite once after C5.
- Review: once, after C5, for the whole feature (no core chunk).
- Play check: **yes, needs THJ's time** (list written with the build: screenshots 1 to 3 layouts, a knock onto a hazard, a knock into Linda's lane for Watch, a pass through a heavy, cast on an enemy with each fallback, a Steer through a Masher's counter-range).
- Docs after THJ's play check: GDD Lucy LU-3 to LU-7 and value table, `enemies.md` EN-3, EN-18, `design/cyclone-redesign.md` reset note (designer); glossary "carries" retired, "knock" (narrative); `tech/core-systems.md` Cyclone note (coordinator); Claude Docs mirror for `lucy.md`.
- Commits: C1, C2, C3, C4 and C5 each their own, in that order (C4 can land any time).
