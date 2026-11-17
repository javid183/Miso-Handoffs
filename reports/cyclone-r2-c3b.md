# Report: Cyclone round 2, C3b (Burst)

Plan: plans/2026-11-17-cyclone-round2-tech.md (chunk C3, sub-chunk C3b; design plans/2026-11-17-cyclone-round2-design.md §4 E, §5, §8; decisions D-550, D-551, D-557)    Agent: miso-implementer    Branch: thj/cyclone (on top of the uncommitted C1, C2, C3a)
Outcome: done (compiled in the open editor through the Unity MCP; EditMode run, see "Test run"). No core file touched.

## What changed

Cyclone code (`miso/Assets/_Project/Features/Player/Lucy/Scripts/Cyclone/`):

- `CycloneEntity.Burst.cs` (new partial, + `.meta`): the burst. `BurstsOn(entity)` (a live enemy of the caster, heavy by `CycloneHeavy.IsHeavy(unit, pullTagQuery)`, whose footprint covers the Cyclone's cell, while the Cyclone is alive and not yet burst), `TryBurst` (called from `Activate`), `BurstRoutine(heavy, holdOwnerSource, playRing)`: first step lands the hits (heavy first, then every enemy beside, once each) through `WhirlSteps.HealthOf` / `Hit` / `Report` exactly like the Whirl's hit, plays `CycloneWhirlBeat.Burst`, logs; then waits `BurstSeconds` (0.3 s, the cross's burst ring length, on the Whirl steps' unscaled clock, 0 while paused); `finally` releases the turn-switch hold and calls `Dispose()` (which defers itself while a Whirl or Steer runs). New state: `HasBurst` (spent), `IsBursting`, `LastBurstHit`, `BurstSteps` (test-swappable). The hold uses its own owner object (`BurstHold`, per instance, not static) so it never releases the Whirl's hold (`TurnSwitchHoldSet` treats one owner as one hold).
- `CycloneBurstRules.cs` (new, + `.meta`): pure `Targets(center, heavy, cellAt, isEnemy)` (heavy, then `CycloneWhirlPlanner.HitTargets`, deduplicated, so a large heavy that also covers a touching cell is hit once), `LogId = "Burst"`, `LogDetail(hit) = "hit M"`.
- `ICycloneBurstSteps.cs` + `CycloneBurstSteps.cs` (new, + `.meta`): the burst's only own step, the log line (`GlobalEventBus.RaiseSynergy(caster, "Burst", "hit M", targets)`, the same channel as the Whirl's line). A separate interface so `ICycloneWhirlSteps` and its three test recorders stay untouched.
- `CycloneEntity.cs`: `Activate(entity)` (was empty) now calls `TryBurst(entity)`; `Dispose` also defers while `IsBursting`; header comment updated.
- `CycloneEntity.Whirl.cs`: `StartWhirl` refuses once `HasBurst`; `WhirlRoutine` ends at once if already burst, plans no pull if burst, and skips its hit (and log) if a burst happened while it ran (3 small hunks).
- `CycloneEntity.Steer.cs`: `CanBeSteered` is false once `HasBurst` (1 line).

Tests (`miso/Assets/_Project/Features/Player/Lucy/Scripts/Editor/`):

- `CycloneBurstTests.cs` (new, + `.meta`): 16 tests (list under Acceptance criteria). Uses cells made from the game's `GridCell.prefab`, so the grid's real `PlugEntity` / `UnplugEntity` and the Cyclone's real `Dispose` run.
- `CycloneTestGrid.cs`: additive `CycloneTestGrid.WithPrefabCells(w, h)` (builds cells from `Content/Levels/_Common/Prefabs/GridCell.prefab`); the public constructor is unchanged and forwards to it with no prefab.
- `CycloneHeavyPassTests.cs` (C3a review fix): the always-true assertion at line 185 is now "some step of the path puts the 2x2 footprint over `_grid[4,0]`" via `TryGetFootprintCells`.

Not touched: any core file (`GridCell*`, `AEffectTransporter`, `MasherGoblinFactionRoleHandler*`, `MasherCounterRules`, `CombatLevelRunHandler*`), assets, prefabs, `ICycloneWhirlSteps`, `CycloneWhirlSteps`, `CycloneWhirlPlanner`. THJ's `PreloadScreen.unity`, `ProjectSettings/*` and TMP font untouched. No new statics.

## The hook: confirmed, no fallback needed

By reading:
- `AEffectTransporter.MoveEntity` (walk mode: Queen's charge, Masher counter walk `_walk`, normal enemy moves) calls `path[i + 1].PlugEntity(entity)` on **every** cell of the path whenever `entity.CanOccupy(next)`, not only the last.
- `GridPluggableEntity.CanOccupy` checks only the occupant slot for a unit, never the planted slot, so a heavy (let through by C3a's walk check) plugs onto the Cyclone's cell.
- `GridCell.PlugEntityInternal` then calls `planted.Activate(entity)` for every planted entity under the unit's whole footprint (so a 2x2 Queen covering the Cyclone with any of its cells triggers it).
- `JumpEntity` / `TeleportEntity` plug only on the destination, which can never be the Cyclone's cell (`IsFootprintEmpty` / `IsWalkable` refuse it): a jump never bursts it (D-557).

By test: `AHeavyWalkingThroughTheCyclone_BurstsItOnItsCell_AndWalksOn` and `ALargeEnemyCharging_BurstsItOnce_ThoughSeveralStepsCoverIt` replay the Transporter's per-step grid calls (unplug, `IsFootprintWalkable` / last-step `IsFootprintEmpty` stop check, `PlugEntity`) on real prefab cells along the mover-aware `FindPath`; the burst lands the moment the Masher is plugged on the Cyclone cell, and the walk is never stopped short. The Transporter coroutine itself does not run in EditMode (frame and `Time.deltaTime` driven), so the end-to-end walk is a play check.

## Rules I chose (as asked: "define what happens")

- **Hit timing:** the hits land synchronously inside the grid's plug call (the routine's first step), while the heavy stands on the cell, exactly as a hazard planted under a walk path hits (`SpawnableEntity.Activate` also applies in the first coroutine step). This is the safest point: hitting a frame later would find the heavy unplugged mid-lerp, and a heavy killed then would be plugged again by the Transporter after its lerp. A heavy killed on the cell ends its walk the way a hazard kill does (`MoveEntity` checks `IsAlive` each step).
- **Burst during a Whirl** (cast, end of turn, or the Steer's closing Whirl): the burst lands at once; the running Whirl then skips the pull and hit it has not reached yet (and logs nothing), so no enemy takes two Cyclone hits in one moment; the Cyclone is disposed when the Whirl ends (existing deferred dispose). Both turn-switch holds coexist and are released in their own `finally`.
- **Burst during a Steer's glide:** the burst lands at once at the cell the Cyclone still holds; the Steer finishes its glide and its riders' landing as planned (so no carried unit is ever left off a cell; stopping the coroutine from outside would skip its `finally`), its Whirl pulls and hits no one, and the Cyclone is disposed when the Steer ends.
- **Spent:** after a burst, a second heavy, an end-of-turn Whirl (`StartWhirl`) and a Steer (`CanBeSteered`) do nothing. During the 0.3 s ring the Cyclone still stands (blocks light units, lets heavies pass), then goes.
- **Level ended:** no hits, the Cyclone still goes.
- **Inactive Cyclone object** (cannot run a coroutine): the burst lands and the Cyclone is disposed at once, without the ring wait.

## Acceptance criteria (C3b part)

- [x] A heavy entering the Cyclone cell bursts it once: one hit (same compound, `WhirlSteps.Hit`) on the heavy and each enemy beside, no pull, Cyclone gone after: `TheBurst_HitsTheHeavyAndEveryEnemyBesideOnce_NoPull_ThenTheCycloneIsGone` (family beside, diagonal enemy and an arm enemy 2 out are neither hit nor pulled; heavy not moved; planted slot empty after), `ALargeHeavyAlsoBesideTheCyclone_IsHitOnce`.
- [x] Credit to the cast like a Whirl hit: each hit goes through `WhirlSteps.Report` once (same test, report list), which in the real steps is `ReportDamageOutsideAbility(cast, ...)` (kill XP and gold, stats, barks, sisters' tally: the C1/Whirl path, unchanged).
- [x] No Masher counter, no Lucy follow-up: same path as the Whirl. The report's source is the cast, so `MasherGoblinFactionRoleHandler.ClassifyHit` → `IsCycloneCast(source)` → `Ignore` (covered by `MasherCounterWhirlTests`); the hit runs with `CycloneHitContext`, so no effect-performed event and no relay (covered by `CycloneHitContextTests`). The counter's `OnDamaged` only enqueues (ignored here) and never touches a walk in progress, and the burst never moves the heavy (asserted), so a Masher bursting the Cyclone during its counter walk keeps walking; end to end: play check.
- [x] Howling Gale Weak on exactly the units hit: the burst calls `Hit` only on its targets (asserted hit lists), and the Weak is a nested Targeted compound on the hit compound (`CycloneHowlingGaleTests`).
- [x] Log "Burst · Lucy: hit M", no "Gust": `TheLogLine_ReadsBurstHitM`; log called once with M (burst tests).
- [x] Burst beat shown: `CycloneWhirlBeat.Burst` played (asserted); the visual itself is a play check.
- [x] Non-heavy, family, ally never burst: `OnlyAHeavyEnemyOnTheCell_BurstsIt` (with the real Whirl steps' enemy rule: light enemy, Immovable family unit, allied 2x2 all refused; heavy elsewhere refused), `TheFamilyWalkingThrough_DoesNotBurstIt` (an Immovable Lucy walks through on real cells).
- [x] Large heavy by footprint: `ALargeEnemyWhoseFootprintCoversTheCell_BurstsIt`.
- [x] A jump doesn't burst: `AJumpPastTheCyclone_DoesNotBurstIt` (unplug, plug on the landing only, as `JumpEntity` does).
- [x] Queen's charge (Transporter walk) bursts at the cell and continues: `ALargeEnemyCharging_BurstsItOnce_ThoughSeveralStepsCoverIt` (two consecutive steps cover the Cyclone, one burst, charge reaches its end); Masher walk: `AHeavyWalkingThroughTheCyclone_BurstsItOnItsCell_AndWalksOn`.
- [x] No double burst: `ASecondHeavy_DoesNotBurstItAgain`, and the charge test above.
- [x] No double fire with a Whirl: `ABurstDuringAWhirl_TheWhirlSkipsItsHit_AndTheCycloneGoesWhenTheWhirlEnds`, `AfterABurst_NoWhirlAndNoSteer`, `ABurstDuringASteer_TheRidersStillLand_ThenTheCycloneGoes`.
- [x] Turn-switch hold registered and released: `TheBurst_HoldsTheTurnSwitchUntilTheCycloneIsGone`, `ABurstStoppedPartWay_StillReleasesItsHold` (iterator disposed mid-ring), and the Whirl test (both holds released).
- [x] Level end: `AfterTheLevelEnded_NoHit_TheCycloneStillGoes`.
- [x] Cast cooldown keeps running: the burst never touches the cast ability (nothing in the burst path reads or resets it).
- [x] C3a review nit fixed (`CycloneHeavyPassTests` line 185).

Needs THJ's play check (with C3c, since until then the AI's end-of-turn filter still avoids the cross for heavies): Masher counter walk through the Cyclone (bursts, slams after), Queen's charge through it, a heavy's normal move, the burst ring and the log line, Weak with Howling Gale owned.

## Test run

- Before (C3a report): 2066 run, 2065 passed, 1 failed (the known red, inner 43).
- Subset: `CycloneBurstTests` + `CycloneHeavyPassTests` 31 / 31 passed.
- Full suite after (MCP Test Runner, editor open, no Play mode): 2082 run, 2081 passed, 1 failed, 0 skipped. The only failure is `AIRegressionTest.Baseline_MatchesCurrentAI`, inner `CHECKS: 714 FAILURES: 43` (unchanged). The 16 new tests make up the difference from 2066. Compile: no errors.

## Save reset

No.

## Decisions I made

- Hits land synchronously in the plug (same moment as a hazard), not a frame later (reason above). Tier 1.
- Burst during a Whirl or Steer: burst at once, the running Whirl skips its pending pull and hit, the Steer finishes its carry, dispose deferred. Tier 1 (the plan asked me to choose the safest rule).
- The Cyclone stays 0.3 s for the ring, then goes; held turn switch over that time. Tier 1.
- A small `ICycloneBurstSteps` for the log instead of adding a member to `ICycloneWhirlSteps`, so the Whirl interface and its three test recorders (C1/C2 files) are untouched. Same behaviour. Tier 1.
- `CycloneTestGrid.WithPrefabCells` so tests can run the grid's real plug; additive. Tier 1.

## Needs THJ

None.

## Docs to update

- `tech/core-systems.md` (coordinator), Cyclone note: no core change in C3b; the planted-entity `Activate` hook in `GridCell.PlugEntityInternal` is now load-bearing for the Cyclone (the burst), fired on every cell of a walk.
- GDD `characters/lucy.md` LU-5 / LU-7 and `enemies.md` EN-2, EN-6 (designer): the burst rules above (once, synchronous hit, jump doesn't burst, burst during a Whirl or Steer replaces their pending hit).

## Risks and loose ends

- **Commit split across shared files.** `CycloneEntity.Whirl.cs` and `CycloneEntity.Steer.cs` already carry uncommitted C1/C2 changes; C3b adds 3 hunks and 1 hunk to them. `CycloneTestGrid.cs`, `CycloneEntity.cs` were clean before C3b; `CycloneHeavyPassTests.cs` is a C3a new file. Interactive staging isn't available here, so to commit C1/C2/C3a before C3b the coordinator needs `git apply --cached` with a patch. The C3b-only hunks for these five files are saved at `C:\Users\javid\AppData\Local\Temp\claude\9ec5439f3060d705\487fa4a4-94b4-478d-84dc-b8aae3f336a7\scratchpad\c3b-shared-hunks.diff` (diff of each file before and after this chunk; the pre-C3b copies are in `...\scratchpad\pre-c3b\`). Simplest alternative: fold the `CycloneHeavyPassTests.cs` fix into the C3a commit and commit the Whirl/Steer hunks with C3b after C1/C2 are committed from the pre-C3b copies.
- Until C3c, the AI still keeps heavies' end-of-turn destinations off the cross, and its path planning already crosses the Cyclone (C3a); the burst now makes that crossing real.
- `AEffectDashAttack` paths without a mover (C3a note), so a heavy's dash still routes around and never bursts the Cyclone. Only Transporter walks burst it.
- Other code that plugs a unit onto a cell (e.g. `GridCell.PlugEntity`'s nearest-free-cell fallback, reversion contexts) could put a heavy enemy on the Cyclone's cell and burst it; such a heavy would also be standing on the Cyclone, so the burst is the right outcome.
- The burst hits happen inside the grid's plug call. A heavy killed by the burst dies during `PlugEntityInternal` (before its `gridCellPlugStateChanged` raise), the same order a hazard kill already has.
- `BurstSeconds` (0.3) duplicates the cross view's private `BurstTime`; keep them equal if the ring is retimed (C4 touches the cross).

## Proposed commits

Order after the C1, C2 and C3a commits.

1. `feat(lucy): a heavy enemy walking through the Cyclone bursts it: one last hit on it and the enemies beside it, then the Cyclone is gone` (plain, Cyclone code and tests):
   - `miso/Assets/_Project/Features/Player/Lucy/Scripts/Cyclone/CycloneEntity.Burst.cs` + `.meta`
   - `miso/Assets/_Project/Features/Player/Lucy/Scripts/Cyclone/CycloneBurstRules.cs` + `.meta`
   - `miso/Assets/_Project/Features/Player/Lucy/Scripts/Cyclone/ICycloneBurstSteps.cs` + `.meta`
   - `miso/Assets/_Project/Features/Player/Lucy/Scripts/Cyclone/CycloneBurstSteps.cs` + `.meta`
   - `miso/Assets/_Project/Features/Player/Lucy/Scripts/Cyclone/CycloneEntity.cs`
   - `miso/Assets/_Project/Features/Player/Lucy/Scripts/Cyclone/CycloneEntity.Whirl.cs` (C3b hunks only, see Risks)
   - `miso/Assets/_Project/Features/Player/Lucy/Scripts/Cyclone/CycloneEntity.Steer.cs` (C3b hunk only)
   - `miso/Assets/_Project/Features/Player/Lucy/Scripts/Editor/CycloneBurstTests.cs` + `.meta`
   - `miso/Assets/_Project/Features/Player/Lucy/Scripts/Editor/CycloneTestGrid.cs`
2. `test(lucy): the large-enemy path test checks that its footprint really covers the Cyclone` (plain): `miso/Assets/_Project/Features/Player/Lucy/Scripts/Editor/CycloneHeavyPassTests.cs` (or fold into the C3a commit, since that file is new in C3a).

## Other branches

None (Cyclone lives on `thj/cyclone`).

## How to see it

1. Test Runner, EditMode: run `CycloneBurstTests` (16 green) and `CycloneHeavyPassTests` (15 green), then Run All: only `AIRegressionTest.Baseline_MatchesCurrentAI` red (inner 43).
2. In play (better after C3c): in a Masher level, cast the Cyclone in a corridor between Lucy and the Masher, with a Claw beside the Cyclone. Hit the Masher with a family action so it counter-walks through the Cyclone: when it steps on the Cyclone's cell the ring bursts, the Masher and the Claw each take the Whirl's hit (3 at Cyclone Power 0), the Cyclone disappears, the Masher keeps walking and slams; no second counter answers the burst. The combat log reads "Burst · Lucy: hit 2".
3. Same with the Goblin Queen's charge through the Cyclone: one burst, the charge goes on. With Howling Gale owned, the units hit show Weak. Lucy's Cyclone cast stays on cooldown.
4. A Claw walking toward the Cyclone still stops in front of it; the family still walks through without bursting it; the Queen's jump over it does nothing to it.
