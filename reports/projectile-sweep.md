# Report: Projectile sweeps its path and hits each entity once

Plan: coordinator brief of 2026-10-28 (D-300; no plan file)    Agent: miso-implementer    Branch: thj/linda-quiver
Outcome: done (compiled outside the editor; EditMode suite and play check not run, the editor is open)

## What changed

- `miso/Assets/_Project/Core/Entities/Runtime/Projectile.cs` (core): the trigger body moved into one private `TryHitOnContact(Collider2D)`; `OnTriggerEnter2D` now just calls it. A per-projectile hit set (cleared in `Initialize`) blocks a second hit on the same entity. At the start of each `Update` the projectile sweeps the step it moved during the last frame and sends every collider it passed through `TryHitOnContact`. BOM and LF kept.
- `miso/Assets/_Project/Core/Entities/Runtime/ProjectileSweep.cs` (+ `.meta`), new: `ProjectileHitLedger<T>` (the dedupe and accept rule), `ProjectileSweepStep` (which step to sweep, if any) and `ProjectileSweep.Cast` (a non-allocating `Physics2D.CircleCast` with a buffer that grows when it fills up). No statics.
- `miso/Assets/_Project/Core/Entities/Editor/ProjectileSweepTests.cs` (+ `.meta`), new: 16 EditMode tests.

### Exact core diff (Projectile.cs, +71 / -7)

1. **New private fields**: `_hitEntities` (`ProjectileHitLedger<GameEntity>`), `_sweepStep`, `_sweepHits` (`RaycastHit2D[16]`), `_sweepFilter`, `_sweepCollider`, `_sweepRadius`, `_sweepReady`. They are instance fields and not serialized, so there is no prefab or save impact.
2. **`Initialize`** (at the end): clears the hit set and the sweep step, and sets up the sweep: the radius of the root `CircleCollider2D` times the largest lossy scale, or `boundingSize` when there is no circle collider. The filter is `useTriggers = true` plus `Physics2D.GetLayerCollisionMask(gameObject.layer)`.
3. **`Update`**: after the existing `!IsAlive` early-out, `SweepLastStep(); if (!IsAlive) return;`. Just before `_progressTracker +=`, `_sweepStep.Begin(SweepCenter())` records where this frame's move starts. Nothing else in `Update` changed. The end-cell branch (`NotifyIncomingDirection`, `Activate(_targetCell, true)`, `Dispose`) is untouched.
4. **`OnTriggerEnter2D`** → `TryHitOnContact`, with the same body in the same order: the `IsAlive` / `TargetReach` guard, `GetComponent<GameEntity>()` on the contact's GameObject, the owner skip, `MatchesEffectFaction`, the `applyModsOnHit` falloff from `_hitCount`, the `TargetReachAndHit` + `Occupies(_targetCell)` skip, and `_hitCount++`. Two things are added. The entity must be claimable in the hit set, so it is hit once only. And `entity == this` is skipped, because the sweep can find the projectile's own collider and the trigger never could.
5. **New private methods**: `SetUpSweep`, `SweepCenter` (the circle collider's world center) and `SweepLastStep`. `SweepLastStep` runs only when there is a recorded step and the projectile is `enabled`, alive and not `TargetReach`. It casts from where the last move started to where the projectile is now, and calls `TryHitOnContact` for each collider, nearest first.

`CollectPreviewPathHits`, `CheckTrajectoryClearance`, `GetClone`, the public API and serialized fields: unchanged.

## Acceptance criteria

- [x] **A long frame can't skip an enemy.** Every step is swept with the projectile's own circle and layers. Test: `LongStep_OverANarrowCollider_FindsIt` (a 0.2-wide body between two ends that don't touch it). Play check: verifier.
- [x] **The sweep and the trigger share one accept-and-apply path.** `TryHitOnContact` is the only path. Code read.
- [x] **Per-projectile hit set keyed by entity, cleared in `Initialize`.** Tests: `SameEntityTwice_HitOnce`, `SeveralEntities_EachHitOnce_InTheOrderFound`, `NewFlight_CanHitTheSameEntityAgain`. Return and Cyclone copies come from `GetClone`, which makes a new instance and calls `Initialize`, so they can hit again (the return-flight rehit stays, D-274).
- [x] **Frozen projectiles don't sweep.** Mark's catch sets `enabled = false`, so `Update` doesn't run. The guard also passes `enabled && IsAlive`. Test: `NotMoving_NoSweep`. If the catch is declined, the arrow is put back on its path point and switched on again. Its next `Update` then sweeps the step it made before the catch (the catch point is never used as a start), which adds only hits the trigger may have missed.
- [x] **No sweep on the first frame, and none from the origin or through the owner.** The step is recorded at the start of each move in `Update`, not in `Awake`/`OnEnable` (`AEffectSpawner` instantiates at the prefab's origin and positions afterwards). The first `Update` has no step, so nothing is swept. The first sweep runs from the launch point, and the owner is skipped as before. Tests: `FirstFrame_NothingToSweep`, `NewFlight_ForgetsThePreviousStep`.
- [x] **End-cell `Activate(_targetCell)` unchanged, and no double hit.** The sweep goes through the same `Occupies(_targetCell)` skip, so the end-cell occupant is never hit on contact (it is claimed and counted for falloff, as today) and only the arrival hits it. Code read; play check: verifier.
- [x] **Non-arrow projectiles get the same benefit.** All 15 projectile prefabs (5 Linda, 7 Lucy fireballs, Archer Goblin, Dark Shaman, the dev test) have a root trigger `CircleCollider2D` with radius 0.1, offset 0, layer 0, so the sweep radius equals today's collider and `boundingSize`. `TargetReach`-only projectiles skip the cast (they never hit on contact).
- [x] **Main-thread only.** No AI code reads `Projectile` (grep of `AISystem`: only an asset path string in `AIRegressionTest`). The new code runs in `Initialize`, `Update` and `OnTriggerEnter2D`.
- [x] **Domain reload.** No new statics (one `const`).
- [x] **Compiles.** I compiled `Projectile.cs` + `ProjectileSweep.cs` with Unity's Roslyn against `Library/ScriptAssemblies/Assembly-CSharp.dll` and the 6000.3.4f1 engine DLLs: no errors, only warnings that were already there. The test file compiles against the result plus Unity's NUnit. The real editor compile is not checked yet.
- [ ] **EditMode suite passes.** Not run: the editor is open and the Unity MCP didn't connect. THJ or the verifier: Test Runner > EditMode > Run All.

### Why behaviour is unchanged at normal frame rates

- **The sweep runs a frame late on purpose.** It covers the step moved in the *previous* frame, at the start of this frame's `Update`. Physics (50 Hz, `FixedUpdate` mode, auto-sync off) runs before `Update`, so whenever a physics step falls between two frames, the trigger and Mark's catch (trigger and `CatchSweep` in `LateUpdate`) have already seen where the step ended. The sweep then finds only what is already in the hit set, plus what the jump skipped. The order of hits and catches is today's.
- **Frames with no physics step in between** (above 50 fps): the sweep reaches a body the trigger would only have reported at the next physics step, so the hit lands up to one frame earlier. It is the same hit, in path order. Today the trigger at those frame rates can also miss a body it only overlapped between two physics steps; the sweep fixes that too.
- **Same filter and same data.** The sweep only changes *how a contact is found*: same collider radius, same layer mask and triggers, `GetComponent<GameEntity>` on the same GameObject, then the same method.
- **Dedupe.** At normal frame rates each unit has one collider (`UnitBase`: one `BoxCollider2D`), so one trigger enter per pass and the dedupe never fires. It only changes something if a body leaves and re-enters one projectile's circle, or the trigger and the sweep both report it.
- **The arrival is untouched.** The occupant skip and `Activate(_targetCell, true)` are the same, and the last step is swept before the arrival branch runs, so skipped bodies on the last step are hit before the end cell, in path order.

## Save reset

No.

## Decisions I made

- **The sweep runs at the start of the next `Update`, not right after the move.** The brief said "after moving". Sweeping right after the move would run before Mark's `CatchSweep` (`LateUpdate`) and before the physics trigger. On a long frame, that would hit an enemy behind Mark before the arrow is caught: a behaviour change. Sweeping the previous step first lets the catch and the trigger act first, and it is the same set of segments (Tier 2).
- **The sweep goes from where the last move started to where the projectile is now**, not to where it moved to. When Mark's return-flight clamp (`LateUpdate`) puts the return arrow back on Linda, the sweep stops on Linda instead of reaching past her (Tier 2).
- **`TargetReach` projectiles skip the cast.** They can't hit on contact, so this changes nothing and saves a cast per frame (Tier 1).
- **The projectile's own collider is skipped** in `TryHitOnContact` (`entity == this`). The trigger never reported it; the cast can (Tier 1).
- **The buffer** starts at 16 and doubles, up to 256, when a cast fills it, so a long step can't drop its far end (Tier 1).
- **The helpers live in their own file** next to `Projectile.cs`, not in a partial (Tier 1).

## Needs THJ

None.

## Docs to update

- `tech/core-systems.md` › Other combat entities: `Projectile` sweeps the step moved during the last frame (circle cast, own collider and layers) and keeps a per-projectile hit set cleared in `Initialize`; new `Core/Entities/Runtime/ProjectileSweep.cs`.
- `tech/combat-architecture.md` / `mechanics-brief.md`, if they describe projectile hits as "trigger only".

## Risks and loose ends

- **Sleeping bodies.** A projectile without a Rigidbody2D (enemy shots, Lucy's fireballs, the dev test) moved by transform could miss a sleeping unit's body (see the level-flight findings). The sweep is a query, so it sees sleeping bodies. Those projectiles now hit units they used to fly through even at normal frame rates. This is the fix asked for, and the damage preview already predicted those hits, but it is the most visible change outside Linda. For Archer Goblin and Dark Shaman shots in `Hit` modes, this also means more enemy hits on the player.
- **AbilityDamagePreview vs runtime: no new disagreement**, left as is. Both are unchanged and differ as before:
  - the preview's falloff index (`collisionIndex`) goes up for every unique entity it finds, while the runtime's `_hitCount` goes up only for entities the effect targets;
  - the preview lists the end-cell occupant as a path hit (its skip is commented out), while the runtime skips it on contact and hits it on arrival.
  The sweep moves the runtime closer to the preview (no skipped bodies, a dedupe like the preview's `seen` set).
- **A catch on a long frame**: when `CatchSweep` stops the arrow at Mark, enemies between the launch and Mark in that same frame are not hit by the original arrow. The step isn't swept while frozen, and a caught original is never switched back on. The return copy flies back over them. This is the same as today.
- **Stale physics poses**: with auto-sync off, a unit that moved this frame is cast against at its last physics pose. This is the same limit as the trigger.
- The physics tests (`LongStep_…`, `StepThatStopsShort_…`, `FullBuffer_Grows`) query real `Physics2D` in edit mode at (10000, 10000) with a hidden, unsaved GameObject. If edit-mode `Physics2D` behaves differently in this editor, those three fail; the other 13 are pure.
- `ProjectileSweepStep.TryTake` uses `Mathf.Epsilon` as its "didn't move" cutoff, the same as `CatchSweep`.

## Proposed commits

1. `fix(core): projectiles sweep the path they moved each frame and hit each unit once`: `miso/Assets/_Project/Core/Entities/Runtime/Projectile.cs`, `miso/Assets/_Project/Core/Entities/Runtime/ProjectileSweep.cs`, `miso/Assets/_Project/Core/Entities/Runtime/ProjectileSweep.cs.meta`, `miso/Assets/_Project/Core/Entities/Editor/ProjectileSweepTests.cs`, `miso/Assets/_Project/Core/Entities/Editor/ProjectileSweepTests.cs.meta` (core, on its own). It doesn't depend on any of the branch's uncommitted work.

## Other branches

`main` needs this too: same `Projectile.cs` trigger-only hits, the same skip on long frames. The change touches only `Projectile.cs` plus two new files, so it should cherry-pick cleanly if `Projectile.cs` on `main` matches this branch's committed version (check `git diff main thj/linda-quiver -- miso/Assets/_Project/Core/Entities/Runtime/Projectile.cs` first).

## How to see it

Tests (editor open): Window > General > Test Runner > EditMode > Run All. The only accepted red is `AIRegressionTest.Baseline_MatchesCurrentAI`. Worth a look in particular:
- `MISO.Core.Entities.EditorTests.ProjectileSweepTests` (new, 16);
- `CatchReturnWiringTests`, `QuiverWiringTests` (Linda's projectile prefabs);
- `CatchFreezeRulesTests`, `CatchPointRulesTests`, `ReturnFlightClampTests` (Mark's catch around a projectile);
- `DamagePreviewRulesTests` (preview).

Setting the frame rate: no cheat exists for it. For the check, put a throwaway script (not to be committed) on any scene object that sets `QualitySettings.vSyncCount = 0; Application.targetFrameRate = 10;` (or 60) in `Start`. The level-flight case is easiest in "A Wolf's Blood".

1. **Adjacent sideways Watch, 10 fps.** Put a Dark Claw on the tile right next to Linda on her side (in THJ's log, Linda at (6,1), the Claw moving to (7,1)), so Watch fires sideways at it. Expected: the Claw takes the hit and the combat log shows the damage line. Before this change, the arrow often flew through it.
2. **The same at 60 fps.** Same result: one hit, one damage line, no double hit.
3. **A column of worms, 10 fps.** Line up 2 or 3 Dark Worms in one column in Linda's range, with an empty or occupied end cell, and shoot along the column. Expected: every worm on the path is hit once, in path order, with the falloff (first full, then lower), and the end-cell worm is hit once on arrival. The HP lines in the combat log show each worm exactly once, and the damage matches the preview.
4. **The same column at 60 fps.** The same hits and numbers as at 10 fps.
5. **Mark's catch**, optional at both frame rates: Linda shoots through an enemy toward Mark (2+ tiles). Expected: the enemy is hit on the way out, the catch works as before, and the return flight hits the enemy again (intended). If the catch prompt is declined, the arrow flies on and lands as before.
6. **Enemy shots**: an Archer Goblin shoots at a unit. The hit is unchanged at 60 fps. At 10 fps a shot no longer passes through a unit in its path.
