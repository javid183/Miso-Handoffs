# Report: Cyclone round 3, C3 the wind's beats (inhale, exhale, grab, drag, fling, input guard)

Plan: plans/2026-11-18-cyclone-round3-tech.md (chunk C3; design plans/2026-11-18-cyclone-round3-design.md §4; beats approved in D-568, no fire flecks or hitstop)    Agent: miso-implementer    Branch: thj/cyclone (on top of the uncommitted C1 and C2)
Outcome: done (compiled clean in the open editor through the Unity MCP; full EditMode suite run, see "Test run"). No core file edited. One existing core API is called (the input lock), see "Decisions I made" and "Needs THJ".

## What changed

All under `miso/Assets/_Project/Features/Player/Lucy/`. LF, no BOM, like the neighbours.

New (each with its `.meta`):
- `Scripts/Cyclone/CycloneWindMotion.cs`: the beats' shapes as pure functions of progress: `EaseIn`, `EaseOut` (never past 1), `Arc` (hop and recoil), `Trail` (a rider starts late, arrives with the Cyclone), `Kick` (front enemy ahead), `Toward`, and `Fling` (root eases out to the landing, the lean and tilt fade, a hop; exactly on the cell at t = 1). Shared by the Whirl, the Steer and the cast shove.
- `Scripts/Cyclone/CycloneUnitDrawings.cs`: moves a unit's drawing without moving it off its cell. The drawing is the unit's `Visual` (the body sprite's parent under the root); the root is left alone, so hover, projectiles and health bars don't move. A unit without such a child (edit-mode test units) has its root moved, as the round 2 glide did. Remembers each rest pose and puts it back (`Restore`, `RestoreAll`). Instance per steps object, no statics.
- `Scripts/Cyclone/CycloneEntity.Wind.cs`: partial of `CycloneEntity`: the serialized beat values (inhale 0.12 s and 35%, exhale 0.08 s, recoil 0.06 s and 0.1 cell, grab 0.08 s and 30%, drag lag 0.25 of a step, drag tilt 8°, kick 0.5 of a step, fling 0.12 s, hop 0.15 cell); the per-action moved set (`NoteMovedThisAction`, `MovedThisAction`, cleared when the Whirl ends); who leans (alive, not moved this action, pullable, one cell); `OnDisable` safety net (releases the input hold and puts every drawing back if the coroutine is killed from outside).
- `Scripts/Editor/CycloneWindBeatsTests.cs`: 20 tests (list under Acceptance criteria).

Changed:
- `Scripts/Cyclone/CycloneEntity.Whirl.cs`: `swellSeconds` default 0.2 → 0.1. The swell plays only when a pull is planned (checked after the post-carry settle; the pull is re-planned right after the swell, at the same moment as before). After the reactions: if anyone is to be hit, wait while paused, then inhale (swell beat here if there was no pull; leaners drawn in, ease-in), exhale (ease-out back to 0), input held on every frame of both; then drawings restored, input released, burst check and target list taken again, and the hit lands in that same frame. After the hit (and the existing Burst beat and log), moved units and heavies get the 0.06 s recoil. Pulled movers are noted as moved. `finally` releases the input, restores drawings and clears the moved set. Header comment extended.
- `Scripts/Cyclone/ICycloneWhirlSteps.cs` + `CycloneWhirlSteps.cs`: `BeatDeltaTime` (game time, as the old `WaitForSeconds` swell), `DrawLeaning(unit, center, cells)`, `RestoreDrawings`, `HoldInput(bool)`. The real `HoldInput` uses `PlayerInputController.Instance.AddInputLock/RemoveInputLock` with the steps object as owner (the turn banner's lock).
- `Scripts/Cyclone/CycloneEntity.Steer.cs`: grab before the glide (only when a start rider exists that isn't the front enemy), drag (front: kick; riders: trail, lean toward the Cyclone's current drawing, tilt `-dir.x × 8° × sin(πt)`; a late joiner is grabbed in the first half of its step; a carried unit not moving this step lets go of its lean), fling (only when the landing will happen), then the one landing frame as before; drawings restored after the landing or stay-put and in `Abort`. Landed riders are noted as moved before the Whirl. `CarryLanding` takes the Cyclone for its values. The Cyclone's drawing is set exactly on each step's end cell. The comment on `SteerSecondsPerCell` (C2's "the cast shove glides at this pace") was removed; the getter stays.
- `Scripts/Cyclone/ICycloneSteerSteps.cs` + `CycloneSteerSteps.cs`: `DrawUnit(unit, position, offset, tilt)`, `RestoreDrawings`.
- `Scripts/Cyclone/ICycloneShoveSteps.cs` + `CycloneShoveSteps.cs` (C2 files): the same two members.
- `Scripts/Cyclone/AEffectCycloneSpawner.Shove.cs` (C2 file): only the glide loop replaced by the fling (`CycloneWindMotion.Fling`, prefab's `FlingSeconds` 0.12 s, hop `HopCells` × one cell), a final draw on the landing cell, drawings restored at the landing and in `finally`; after the spawn, the shoved enemy is noted as moved on the new Cyclone. The landing, the re-check, the spawn and the `finally` logic are as C2 left them. Header comment and the fallback constants updated (0.12 s, hop 0.15).
- `Scripts/Cyclone/CycloneEntity.Burst.cs`: the enemies beside the Cyclone (not the heavy, which walks on) recoil during the first 0.06 s of the existing 0.3 s ring wait; drawings restored after it and in `finally`. No inhale, no new wait.
- `Prefabs/Cyclone.prefab`: the one override `swellSeconds: 0.2` → `0.1` (one-line YAML edit). No other prefab override exists for the new fields.
- Test recorders given the new members (no assertion changed): `Scripts/Editor/CycloneWhirlTests.cs` (2 recorders), `CycloneSteerTests.cs` (2), `CycloneBurstTests.cs` (2), `CycloneCastOnEnemyTests.cs` (1). Steer and shove recorders put `position + offset` on the root, as the real steps do for a unit without a Visual.

Not touched: every core file (`PlayerController`, `PlayerInputController`, `GridManager`, `AEffectPusher`, `AEffectTransporter`, `FactionControllerBase`), `CycloneCrossView.cs` (C1), THJ's `PreloadScreen.unity`, `ProjectSettings/*`, TMP fallback font. No new statics.

## Acceptance criteria (C3 part)

- [x] **Whirl beats.** Swell 0.1 s only before a pull: `Whirl_OrderIsPullReactionsBreathHit_AndTheSwellComesOnlyBeforeAPull`, `Whirl_WithoutAPull_TheInhaleIsTheSwell`, `Whirl_NobodyToHit_NoBreathNoSwellNoHold`. Inhale 35%, ease-in; exhale back, ease-out, no overshoot; the hit as they arrive: `Whirl_StillStandingPullableEnemiesLeanIn_MovedOnesAndHeaviesRecoilInstead` (lean 0.35, no jolt on the leaner), `Shapes_NoOvershoot_AndTheFlingEndsExactlyOnItsCell`. Recoil for moved units and heavies; carried, pulled, shoved skip the inhale; heavies and large units never lean: same test, `Whirl_ALargeEnemy_NeverLeans`, the Steer test (rider recoils, no lean), `TheCastShove_IsTheFling_AndTheShovedEnemySkipsTheInhale`. No inhale when nobody is hit: `Whirl_NobodyToHit_NoBreathNoSwellNoHold`.
- [x] **Steer beats.** Grab 30% on riders, front enemy never leans; fling stops exactly on the landing cell with a hop, no overshoot; landing frame after: `Steer_RidersAreGrabbed_TheFrontEnemyIsNot_AndEveryoneIsFlungExactlyOntoItsLandingCell`. Late joiner grabbed during its step with no extra time: `Steer_ARiderThatJoinsPartWay_IsGrabbedDuringItsStep_WithNoExtraTime`. Trail and kick shapes: `Shapes_...`. Cast shove uses the same fling: `TheCastShove_IsTheFling_...`. The tilt and trailing look: play check.
- [x] **Net time** (recorder clocks at 1 ms frames; each timed loop can run one frame long from rounding):
  - Whirl without a pull, beats before the hit: **0.202 s** (round 2: 0.2 s swell) → **+0.0 s**.
  - Whirl with a pull: **0.302 s** (swell 0.1 + inhale 0.12 + exhale 0.08; round 2: 0.2 s) → **+0.1 s**.
  - Two-step Steer with riders, before its Whirl: **0.504 s**; without riders: **0.302 s** → **+0.2 s** (grab 0.08 + fling 0.12).
  - Two-step Steer with a rider joining on step two: **0.423 s** (glide 0.30 + fling 0.12, no grab).
  - Cast shove fling: **0.121 s** (was the 0.15 s glide).
  - Not in those numbers: the 0.06 s recoil after the hit, when someone recoils (the Whirl ends, and the turn switch is released, 0.06 s later; time to the hit is unchanged).
- [x] **No outcome or order change.** Every round 2 and C2 test passes unchanged (only recorders gained members): pull, reactions, hit, Watch order, one landing. `Whirl_OrderIsPullReactionsBreathHit_...` adds the breath to the order. The burst check and targets are taken after the breath: `Whirl_TheTargetsAreTakenAfterTheBreath_ADeadOrMovedUnitIsNotHit`, `Whirl_ABurstDuringTheBreath_IsTheOnlyHit`. A burst during a heavy's walk has no inhale (the burst routine has none; existing burst tests pass).
- [x] **Input guard.** The input is held on every frame from the first inhale frame to the hit, and released in the hit's frame: `Whirl_TheInputIsHeldOnEveryFrameFromTheInhaleToTheHit_AndReleasedAfter`. Round 2 item 25 (the pull and hit wait for an action started after a Steer) still holds: the settle waits are unchanged and run before the breath. Needs the play check in a level.
- [x] **Abort.** Stopped mid-breath: drawings back, input released, unit still plugged: `Whirl_StoppedDuringTheBreath_PutsEveryDrawingBack_AndReleasesTheInput`. Stopped mid-grab: drawings back, rider on its cell and drawn there: `Steer_StoppedDuringTheGrab_PutsTheDrawingsBack_AndEveryRiderOnItsCell`. Existing Steer and shove abort tests pass (landing cut short, stop during glide, end cell taken, rider dies, enemy dies, landing taken). Real drawing helper: `Drawings_MoveTheVisualNotTheRoot_AndGoBackAtRest`, `Drawings_AUnitWithoutAVisual_HasItsRootMovedInstead`.
- [x] Compile clean (no errors; no new warnings). EditMode: see "Test run".

Needs the verifier's or THJ's play check: the whole look (lean depth, snap, recoil, grab, trail lag, tilt, kick, hop, fling), the input hold in a level (click during the breath does nothing; End Turn button, which is UI and not gated by the lock, still waits on the Whirl's turn-switch hold), item 25 again, a level end or Lucy dying mid-beat.

## Test run

- Before (C2 report): 2134 run, 2132 passed; `AIRegressionTest.Baseline_MatchesCurrentAI` inner **`CHECKS: 714 FAILURES: 43`**; one flaky GridToLevel `m_LockCount` assert.
- After (MCP Test Runner, editor open, no Play mode): **2154 run, 2153 passed, 1 failed**: only `AIRegressionTest.Baseline_MatchesCurrentAI`, inner **`CHECKS: 714  FAILURES: 43`** (unchanged). No GridToLevel flake this run. The 20 new tests make up the difference.
- During the work, a re-wait for reactions after the breath doubled the stuck-reaction cap (`CycloneWhirlTests.Whirl_AStuckReaction_HitsAfterTheReactionCap` failed at 303 frames). Removed; that test passes unchanged.

## Save reset

No.

## Decisions I made

- **Input guard: the existing input lock, not the cast hold.** Holding the cast open until the hit was tried on paper and can't work without changing the order of events: Family Role answers (Watch) fire on `ActionsProgressComplete`, i.e. when the cast's action ends, and the Whirl's reaction wait needs `!ActionInProgress`. Holding the cast past the pull would push Watch after the hit and stall the reaction wait to its 15 s cap. So the Whirl takes `PlayerInputController.AddInputLock` (public, existing; the turn banner, `MissionEndPanelUI` and `OpeningSceneHandoff` use it) from the first inhale frame to the hit, released in the hit's frame and in `finally` and `OnDisable`. No core file edited. Tier 2, flagged below because the brief said to stop if the guard "needs a core file".
- The breath never starts while the game is paused (waits for time to run), so the lock can't keep a pause from being lifted. Tier 1.
- The Whirl's beats run on game time (`Time.deltaTime`, like the old `WaitForSeconds` swell and the Steer glide), the settle and pull caps stay on unscaled time. Tier 1.
- The breath plays (0.2 s) whenever someone is hit, even if nobody leans (all moved or heavy): that is what makes the net times above match the design's budget. Tier 1.
- The target list is taken right before the hit (after the exhale), which is "after the inhale" and also covers the 0.08 s exhale. Tier 1.
- Recoil plays after the hit inside the Whirl (0.06 s, only when someone recoils) rather than in a separate coroutine, so an abort always restores it. Time to the hit unchanged; the Whirl ends 0.06 s later then. Tier 1.
- Burst: neighbours recoil inside the existing 0.3 s ring wait (the plan's "neighbours recoil with the hit"); the heavy doesn't (its walk moves its root). Tier 1.
- Values the plan didn't give, all serialized on `CycloneEntity` for tuning: recoil depth 0.1 cell, drag lag 0.25 of a step, tilt 8° (only on sideways steps, a z-rotation shows nothing on vertical ones), kick 0.5 of a step, hop 0.15 cell, late-joiner grab over the first half of its step (constant). Tier 2 feel values.
- The lean moves the `Visual` child (body sprite's parent, under the root); the body sprite itself is never moved (unit clips animate child positions such as `Shadow`; checked no unit clip animates the Visual's own transform). Shadow moves with the Visual. Tier 1.
- Seams: new members on the existing `ICycloneWhirlSteps`, `ICycloneSteerSteps`, and C2's `ICycloneShoveSteps`; each real steps object owns its own `CycloneUnitDrawings`. Tier 1.

## Needs THJ

1. **Using the existing input lock for the guard** (Tier 2, coordinator's call; Tier 3 only if calling a core API counts as touching core).
   - Context: no player input may land between the inhale and the hit; holding the cast open breaks the Watch order (see Decisions).
   - Options: (a) keep the lock as built (Cyclone code calls `PlayerInputController.AddInputLock/RemoveInputLock`, no core edit); (b) no guard, accept a 0.2 s window in which the player can start an action and the hit lands during it; (c) a new core hook (none needed in my view).
   - Recommendation: (a). Same mechanism and owner pattern as the turn banner; released in the hit's frame, in `finally` and in `OnDisable`; never taken while paused.
   - Blocked: nothing; it is in the build. Reverting to (b) is two lines.

## Docs to update

- `tech/combat-architecture.md` (coordinator): Whirl breath (swell only before a pull, inhale/exhale, targets after the breath, recoil, input lock), Steer grab/drag/fling, cast shove fling, `CycloneUnitDrawings` (Visual child, root fallback), moved-this-action set, `OnDisable` safety net.
- `tech/core-systems.md` (coordinator), Cyclone note: no core edit; the Whirl now uses the existing `PlayerInputController` input lock (third user outside the banner).
- `tech/pace-timings.md` if it lists Cyclone waits: swell 0.1 s, breath 0.2 s per hit Whirl, recoil 0.06 s, grab 0.08 s, fling 0.12 s.
- GDD `characters/lucy.md` value table (designer, after the play check): the values above.

## Risks and loose ends

- **Commit split with C2.** C3 edits four of C2's uncommitted files (`AEffectCycloneSpawner.Shove.cs`, `ICycloneShoveSteps.cs`, `CycloneShoveSteps.cs`, `CycloneCastOnEnemyTests.cs`) and two files C2 also changed (`CycloneEntity.Steer.cs`, `CycloneSteerTests.cs`). C2 and C3 can no longer be committed as two clean commits by file; see "Proposed commits" for the options.
- The cross view's swell scale still eases over its own 0.2 s constant (`CycloneCrossView.SwellTime`, C1's file, not touched). Before a pull the wait is now 0.1 s, and without a pull the swell plays during the 0.2 s breath, so the Cyclone reaches about 60 to 100% of its swell before the burst shrinks it. If THJ wants it crisper, set `SwellTime` to 0.1 (one constant, in C1's file).
- If the game is paused by something other than the pause action (a Duo QTE sets `timeScale` 0) during the 0.2 s breath, the breath waits with the lock held until time runs again. The lock blocks every way a player starts that, so I don't expect it; worth a glance in play.
- One-frame race (as in round 2 for the hit): a click processed in the very frame the reactions settle starts an action before the lock is taken; the hit would then land during that action. Not seen in tests; the round 2 behaviour had the same window.
- The shove's coroutine runs on Lucy; if Lucy is destroyed mid-fling, its `finally` doesn't run and the shoved enemy's Visual keeps its hop offset (same exposure C2 noted for `IsInProgress`). The Cyclone itself has the `OnDisable` safety net.
- `CycloneEntity.SteerSecondsPerCell` (added by C2 for the shove) now has no caller; left in place.
- A dead rider's root is put back on its own cell when the Steer restores drawings (round 2 left it where it was); visual only.

## Proposed commits

C2 and C3 share files (see above), so pick one:

- **(A, recommended) one commit for C2 and C3 together**, after the C1 commit, if THJ plays them together as planned:
  1. `feat(lucy): the Cyclone can be cast on an enemy, which is flung one cell away from Lucy first; the Whirl breathes in and out before its hit and the Steer grabs, drags and flings its riders` (plain): C2's file list from `reports/cyclone-r3-c2.md` plus every file below.
- **(B) two commits**: commit C2 first from its own content (needs THJ or the coordinator to stage the C2 versions of the shared files, which no longer exist on disk), then C3. Not practical without a manual hunk split.

C3's own files (all under `miso/Assets/_Project/Features/Player/Lucy/`):
- `Prefabs/Cyclone.prefab`
- `Scripts/Cyclone/CycloneWindMotion.cs` + `.meta`
- `Scripts/Cyclone/CycloneUnitDrawings.cs` + `.meta`
- `Scripts/Cyclone/CycloneEntity.Wind.cs` + `.meta`
- `Scripts/Cyclone/CycloneEntity.Whirl.cs`
- `Scripts/Cyclone/CycloneEntity.Steer.cs` (shared with C2)
- `Scripts/Cyclone/CycloneEntity.Burst.cs`
- `Scripts/Cyclone/ICycloneWhirlSteps.cs`
- `Scripts/Cyclone/CycloneWhirlSteps.cs` (shared with C2)
- `Scripts/Cyclone/ICycloneSteerSteps.cs`
- `Scripts/Cyclone/CycloneSteerSteps.cs`
- `Scripts/Cyclone/ICycloneShoveSteps.cs` + `.meta` (C2's new file)
- `Scripts/Cyclone/CycloneShoveSteps.cs` + `.meta` (C2's new file)
- `Scripts/Cyclone/AEffectCycloneSpawner.Shove.cs` + `.meta` (C2's new file)
- `Scripts/Editor/CycloneWindBeatsTests.cs` + `.meta`
- `Scripts/Editor/CycloneWhirlTests.cs`
- `Scripts/Editor/CycloneSteerTests.cs` (shared with C2)
- `Scripts/Editor/CycloneBurstTests.cs`
- `Scripts/Editor/CycloneCastOnEnemyTests.cs` + `.meta` (C2's new file)

If THJ prefers C3 on its own commit for reverting, (A) can be split as: C2 + C3 shared files together, then C3-only files (`CycloneWindMotion`, `CycloneUnitDrawings`, `CycloneEntity.Wind`, `CycloneEntity.Whirl`, `CycloneEntity.Burst`, `ICycloneWhirlSteps`, `ICycloneSteerSteps`, `CycloneSteerSteps`, the prefab, `CycloneWindBeatsTests`, `CycloneWhirlTests`, `CycloneBurstTests`), but the first commit would not compile alone (the shared files call C3's helpers), so I don't recommend it.

Do not stage `PreloadScreen.unity`, `ProjectSettings/*` or the TMP fallback font (THJ's).

## Other branches

None (scope: `thj/cyclone`).

## How to see it

1. Test Runner, EditMode: run `CycloneWindBeatsTests` (20 green; the timing tests print the measured seconds in their output), then Run All: only `AIRegressionTest.Baseline_MatchesCurrentAI` red (inner 43).
2. Play a level with Lucy and some Claws. Cast the Cyclone on an empty cell with a Claw beside it and none on an arm: no swell first; just before the hit the Cyclone swells, the Claw leans about a third of a cell toward it, then snaps back as the hit number pops.
3. Cast with a Claw two cells out on an arm and one beside: short swell, the arm Claw is pulled in, Watch reacts if it's in Linda's lane, then only the Claw that stood still leans in; the pulled one jolts outward a little with the hit.
4. Try to click anything during that lean: nothing happens until the hit lands.
5. Steer with Claws beside the Cyclone and one in front: the side Claws lean in first, trail it with a small tilt on sideways steps, the front Claw is kicked ahead each step, then everyone hops onto the cell their ghost showed and lands (spikes, Watch, wake). In the Whirl after, those Claws only jolt outward.
6. Cast on a Claw: it hops one cell away from Lucy, lands, the Cyclone appears on its old cell; at the hit it jolts outward rather than leaning in.
7. Let a Masher walk through the Cyclone: the burst lands at once, no lean; the enemies beside jolt outward.
8. Tune in Play mode: select the Cyclone and change the "Wind beats" fields on its `CycloneEntity` (or on `Cyclone.prefab` to keep them).
